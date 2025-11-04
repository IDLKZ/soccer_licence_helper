import base64
import os
import tempfile
from sys import platform

import pdfkit
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from app.adapters.dto.application_criteria.application_criteria_dto import ApplicationCriteriaRDTO
from app.adapters.repositories.application_criteria.application_criteria_repository import (
    ApplicationCriteriaRepository,
)
from app.adapters.repositories.application_document.application_document_repository import (
    ApplicationDocumentRepository,
)
from app.adapters.repositories.application_report.application_report_repository import (
    ApplicationReportRepository,
)
from app.adapters.repositories.category_document.category_document_repository import CategoryDocumentRepository
from app.adapters.repositories.club.club_repository import ClubRepository
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ApplicationReportEntity, ApplicationDocumentEntity
from app.helpers.position_helper import PositionHelper
from app.i18n.i18n_wrapper import i18n
from app.use_case.base_case import BaseUseCase

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

# Конфигурация для Windows
if platform == "win32":
    path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
else:
    # На Linux wkhtmltopdf будет найден автоматически
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")

options = {
    "enable-local-file-access": None,  # Разрешает локальные файлы
    "encoding": "UTF-8",  # Рекомендуется для кириллицы
    "quiet": "",  # Убирает лишний вывод
    # Можно добавить 'no-stop-slow-scripts': '' если требуется
}


class GenerateApplicationDepartmentReportCase(BaseUseCase):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = ApplicationReportRepository(db)
        self.criteria_repository = ApplicationCriteriaRepository(db)
        self.club_repository = ClubRepository(db)
        self.application_document_repository = ApplicationDocumentRepository(db)
        self.user_repository = UserRepository(db)
        self.category_repository = CategoryDocumentRepository(db)
        self.position_helper = PositionHelper(db)
        self.model: ApplicationReportEntity | None = None

    async def execute(self, report_id: int):
        await self.validate(report_id=report_id)
        data = await self.transform()

        # Получаем путь к директории app (на два уровня выше)
        app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        # Путь к логотипу
        logo_path = os.path.join(app_dir, "templates", "logo_white.png")
        sign_img = os.path.join(app_dir, "templates", "sign_img.png")

        with open(sign_img, "rb") as img_file:
            data["sign_img"] = base64.b64encode(img_file.read()).decode("utf-8")
        with open(logo_path, "rb") as img_file:
            data["logo_base64"] = base64.b64encode(img_file.read()).decode("utf-8")

        # return data

        template = env.get_template("department_report_template.html")
        html_content = template.render(**data)
        # Создаем временный файл
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdfkit.from_string(
            html_content, temp_file.name, configuration=config, options=options
        )
        # return data
        # Возвращаем файл
        return FileResponse(
            temp_file.name, media_type="application/pdf", filename="report.pdf"
        )

    async def validate(self, report_id: int) -> None:
        self.model = await self.repository.get(
            report_id, options=self.repository.default_relationships()
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self):
        club = await self.club_repository.get(self.model.application.club_id)
        reports = await self.repository.get_with_filters(
            filters=[
                self.repository.model.application_id == self.model.application_id,
                self.repository.model.criteria_id.is_not(None),
                self.repository.model.status == 1,
            ],
            options=self.repository.default_relationships(),
        )
        application_documents = (
            await self.application_document_repository.get_with_filters(
                filters=[
                    self.application_document_repository.model.application_id
                    == self.model.application_id
                ],
                options=self.application_document_repository.default_relationships(),
            )
        )
        docs, department_user = await self.build_articles(
            reports, application_documents
        )

        data = {
            "department": department_user.full_name if department_user else "",
            "position": department_user.position if department_user and department_user.position else '',
            "date": self.model.created_at.strftime("%d/%m/%Y"),
            "club": club.full_name_ru,
            "reports": docs
        }

        return data

    async def build_articles(
            self,
            reports: list[ApplicationReportEntity],
            application_documents: list[ApplicationDocumentEntity],
    ):
        """
        Преобразует список ApplicationDocumentEntity в структуру articles.
        Убирает дубли документов внутри каждого отчёта.
        """
        # Определяем пользователя департамента (если есть хоть один документ с first_checked_by_id)
        filtered_docs = [doc for doc in application_documents if doc.first_checked_by_id is not None]
        if filtered_docs:
            department_user = await self.user_repository.get(filtered_docs[0].first_checked_by_id)
        else:
            department_user = None

        # Индексация документов по category_id для ускорения выборки
        docs_by_category: dict[int, list[ApplicationDocumentEntity]] = {}
        for doc in application_documents:
            docs_by_category.setdefault(doc.category_id, []).append(doc)

        grouped: dict[int, dict] = {}

        for report in reports:
            expert = await self.user_repository.get(report.criteria.checked_by_id)
            position = await self.position_helper.get_position_by_criteria(criteria=report.criteria, fullname=expert.full_name)
            report_id = report.id

            grouped[report_id] = {
                "date": report.created_at.strftime("%d.%m.%Y"),
                "expert": f"{position}",
                # Создаем список для хранения документов
                "documents": [],
            }

            # Создаем временный набор для быстрого отслеживания уже добавленных ID
            added_doc_ids = set()

            for doc in docs_by_category.get(report.criteria.category_id, []):
                doc_id_str = str(doc.document_id)

                # Проверяем, был ли этот документ уже добавлен
                if doc_id_str not in added_doc_ids:
                    status_value = "критерий выполнен;" if report.status else "критерий выполнен частично;"
                    # Добавляем ID в набор и сам документ в список
                    added_doc_ids.add(doc_id_str)
                    grouped[report_id]["documents"].append({doc_id_str: f"{doc.document.title_ru} - {status_value}"})

        # Преобразуем словарь документов обратно в требуемый формат: список словарей {id: title_with_status}
        articles = []
        for report_id, data in grouped.items():
            # Сортируем список словарей по ключу, преобразованному в целое число
            # list(doc.keys())[0] извлекает строковый ID, который затем преобразуется в int
            data["documents"].sort(key=lambda doc: int(list(doc.keys())[0]))
            articles.append(data)

        return articles, department_user
