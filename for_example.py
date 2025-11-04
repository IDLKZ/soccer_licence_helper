import base64
import os
import tempfile
from sys import platform

import pdfkit
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

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
from app.adapters.repositories.licence.licence_repository import LicenceRepository
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ApplicationReportEntity
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


class GenerateApplicationReportByIdCase(BaseUseCase):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = ApplicationReportRepository(db)
        self.criteria_repository = ApplicationCriteriaRepository(db)
        self.club_repository = ClubRepository(db)
        self.application_document_repository = ApplicationDocumentRepository(db)
        self.license_repository = LicenceRepository(db)
        self.user_repository = UserRepository(db)
        self.category_repository = CategoryDocumentRepository(db)
        self.model: ApplicationReportEntity | None = None

    async def execute(self, id: int):
        await self.validate(id=id)
        data = await self.transform()

        # Получаем путь к директории app (на два уровня выше)
        app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        # Путь к логотипу
        logo_path = os.path.join(app_dir, "templates", "logo_white.png")

        with open(logo_path, "rb") as img_file:
            data["logo_base64"] = base64.b64encode(img_file.read()).decode("utf-8")

        # return data

        template = env.get_template("report_template.html")
        html_content = template.render(**data)
        # Создаем временный файл
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdfkit.from_string(
            html_content, temp_file.name, configuration=config, options=options
        )

        # Возвращаем файл
        return FileResponse(
            temp_file.name, media_type="application/pdf", filename="report.pdf"
        )

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(
            id, options=self.repository.default_relationships()
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self):
        global statuses
        criteria = await self.criteria_repository.get(
            self.model.criteria_id,
            options=self.criteria_repository.default_relationships(),
        )
        club = await self.club_repository.get(criteria.application.club_id)
        license = await self.license_repository.get(
            criteria.application.license_id,
            options=self.license_repository.default_relationships(),
        )
        application_documents = (
            await self.application_document_repository.get_with_filters(
                filters=[
                    self.application_document_repository.model.application_id
                    == criteria.application_id,
                    self.application_document_repository.model.category_id
                    == criteria.category_id,
                ],
                options=self.application_document_repository.default_relationships(),
            )
        )
        articles = self.build_articles(application_documents)
        # Проверяем статусы всех документов
        # Фильтруем документы в зависимости от self.model.status
        if self.model.status == 1:
            statuses = [doc.status for doc in application_documents if doc.status]
        elif self.model.status == 0:
            # Берем все документы — фильтрация не нужна
            statuses = [doc.status for doc in application_documents]

        if all(statuses):
            summary = (
                f"В результате проведенного анализа документов, предоставленных Соискателем лицензии – {club.full_name_ru} "
                f'в Департамент лицензирования, на предмет их соответствия разделу "{criteria.category.title_ru}", '
                f"согласно требованиям «Правил по лицензированию футбольных клубов для участия в соревнованиях, "
                f"организуемых КФФ», выпуск {license.season.title_ru} г., все предоставленные документы соответствуют требованиям процедуры лицензирования."
            )
        elif not any(statuses):
            summary = (
                f"В результате проведенного анализа документов, предоставленных Соискателем лицензии – {club.full_name_ru} "
                f'в Департамент лицензирования, на предмет их соответствия разделу "{criteria.category.title_ru}", '
                f"согласно требованиям «Правил по лицензированию футбольных клубов для участия в соревнованиях, "
                f"организуемых КФФ», выпуск {license.season.title_ru} г., все документы были отклонены как не соответствующие требованиям."
            )
        else:
            summary = (
                f"В результате проведенного анализа документов, предоставленных Соискателем лицензии – {club.full_name_ru} "
                f'в Департамент лицензирования, на предмет их соответствия разделу "{criteria.category.title_ru}", '
                f"согласно требованиям «Правил по лицензированию футбольных клубов для участия в соревнованиях, "
                f"организуемых КФФ», выпуск {license.season.title_ru} г., некоторые документы не соответствуют требованиям и были отклонены."
            )
        director = f"{criteria.first_checked_user.position if criteria.first_checked_user else ''} - {criteria.first_checked_by if criteria.first_checked_by else ''}"
        expert = f"{await self.get_employee_position(criteria.checked_user.id, criteria.category_id) if criteria.checked_user else ''}"
        data = {
            "director": director,
            "expert": expert,
            "date": self.model.created_at.strftime("%d/%m/%Y"),
            "club": club.full_name_ru,
            "articles": articles,
            "summary": summary,
            "signed_by": criteria.checked_user.full_name if criteria.checked_user else None,
            "signed_date": self.model.created_at.strftime("%d.%m.%Y"),
            "status": all(statuses)
        }
        return data

    def build_articles(self, application_documents: list):
        """
        Преобразует список ApplicationDocumentEntity в структуру articles.
        """
        grouped = {}

        # Фильтруем документы в зависимости от self.model.status
        if self.model.status == 1:
            application_documents = [doc for doc in application_documents if doc.status]
        elif self.model.status == 0:
            # Берем все документы — фильтрация не нужна
            pass

        for doc in application_documents:
            doc_id = doc.document_id

            if doc_id not in grouped:
                grouped[doc_id] = {"title": doc.document.title_ru, "documents": []}

            status_value = "Принят" if doc.status else "Отклонен"
            note_value = (
                "Соответствует требованиям процедуры лицензирования. Не противоречит действующему законодательству РК."
                if doc.status
                else doc.comment_ru
            )

            grouped[doc_id]["documents"].append(
                {"name": doc.title_ru, "status": status_value, "note": note_value}
            )

        # Получаем пары (ключ, значение) из словаря
        # и сортируем их по ключу (document_id)
        sorted_items = sorted(grouped.items(), key=lambda item: item[0])

        # Создаем новый список, состоящий только из значений (title и documents)
        # в отсортированном порядке
        return [item[1] for item in sorted_items]

    async def get_employee_position(self, user_id: int, category_id: int) -> str:
        category = await self.category_repository.get(category_id)
        user = await self.user_repository.get(user_id, options=self.user_repository.default_relationships())
        if category:
            switcher = {
                "legal_documents": f"Эксперт по правовым критериям - {user.full_name}",
                "financial_documents": f"Эксперт по финансовым критериям - {user.full_name}",
                "sport_documents": f"Эксперт по спортивным критериям",
                "infrastructure_documents": f"Эксперт по инфраструктурным критериям - {user.full_name}",
                "social_documents": f"Эксперт по критериям социальной и экологической ответственности - {user.full_name}",
                "hr_documents": f"Эксперт по кадровым и административным критериям - {user.full_name}",
            }
            return switcher.get(category.value, category.title_ru)

        return ''