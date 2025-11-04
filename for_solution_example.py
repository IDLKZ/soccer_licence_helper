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
from app.adapters.repositories.application_solution.application_solution_repository import (
    ApplicationSolutionRepository,
)
from app.adapters.repositories.application_step.application_step_repository import (
    ApplicationStepRepository,
)
from app.adapters.repositories.club.club_repository import ClubRepository
from app.adapters.repositories.licence.licence_repository import LicenceRepository
from app.adapters.repositories.season.season_repository import SeasonRepository
from app.adapters.repositories.user.user_repository import UserRepository
from app.core.app_exception_response import AppExceptionResponse
from app.entities import ApplicationSolutionEntity, ApplicationDocumentEntity
from app.i18n.i18n_wrapper import i18n
from app.shared.db_value_constants import DbValueConstants
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


class GenerateApplicationSolutionByIdCase(BaseUseCase):
    def __init__(self, db: AsyncSession) -> None:
        self.repository = ApplicationSolutionRepository(db)
        self.criteria_repository = ApplicationCriteriaRepository(db)
        self.club_repository = ClubRepository(db)
        self.application_document_repository = ApplicationDocumentRepository(db)
        self.license_repository = LicenceRepository(db)
        self.season_repository = SeasonRepository(db)
        self.secretary_repository = UserRepository(db)
        self.application_step_repository = ApplicationStepRepository(db)
        self.model: ApplicationSolutionEntity | None = None

    async def execute(self, id: int):
        await self.validate(id=id)
        data = await self.transform()

        # Получаем путь к директории app (на два уровня выше)
        app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        # Путь к логотипу
        logo_path = os.path.join(app_dir, "templates", "logo_white.png")

        with open(logo_path, "rb") as img_file:
            data["logo_base64"] = base64.b64encode(img_file.read()).decode("utf-8")

        template = env.get_template("solution_template.html")
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

    async def validate(self, id: int) -> None:
        self.model = await self.repository.get(
            id, options=self.repository.default_relationships()
        )
        if not self.model:
            raise AppExceptionResponse.not_found(message=i18n.gettext("not_found"))

    async def transform(self):
        club = await self.club_repository.get(self.model.application.club_id)
        if not club:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
        licence = await self.license_repository.get(
            self.model.application.license_id,
            options=self.license_repository.default_relationships(),
        )
        if not licence:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
        season = await self.season_repository.get(licence.season_id)
        if not season:
            raise AppExceptionResponse.bad_request(message=i18n.gettext("not_found"))
        application_documents = (
            await self.application_document_repository.get_with_filters(
                filters=[
                    self.application_document_repository.model.application_id
                    == self.model.application_id
                ]
            )
        )
        control = await self.application_step_repository.get_first_with_filters(
            filters=[
                self.application_step_repository.model.application_id
                == self.model.application_id,
                self.application_step_repository.model.status_id == 5,
            ],
            options=self.application_step_repository.default_relationships(),
        )
        summary = (
            f"Комиссия по лицензированию футбольных клубов (далее по тексту - КЛФК), "
            f"рассмотрев представленные Директором Департамента лицензирования "
            f"отчет и учетное дело «{club.full_name_ru}» для получения Лицензии «{licence.title_ru}», "
            f"организуемый Казахстанской Федерацией футбола в сезоне "
            f"«{season.title_ru}» года (далее по тексту - «Лицензия»)"
        )
        experts = await self.build_experts(application_documents)
        criteria = await self.build_criteria(application_documents, self.model.application.status_id)
        articles = await self.build_articles(application_documents, self.model.application.status_id)
        conclusion = self.build_conclusion(
            articles=articles,
            club=club.full_name_ru,
            season=season.title_ru,
            licence=licence.title_ru,
            cancel_reason=control.result_ru
        )
        data = {
            "meeting_date": (
                self.model.meeting_date
                if self.model.meeting_date
                else self.model.created_at.strftime("%d/%m/%Y")
            ),
            "meeting_place": (
                self.model.meeting_place
                if self.model.meeting_place
                else "г.Астана, пр. Бауыржана Момышулы 5а."
            ),
            "department_name": (
                self.model.department_name
                if self.model.department_name
                else "Комиссия по лицензированию футбольных клубов КФФ"
            ),
            "control_position": (
                control.responsible.position
                if control.responsible.position
                else "Председатель КЛФК"
            ),
            "control_name": control.responsible.full_name if control.responsible else " ",
            "experts": experts,
            "club_fullname": f"{club.full_name_ru} (БИН {club.bin})",
            "club_shortname": club.short_name_ru,
            "license": licence.title_ru,
            "season": season.title_ru,
            "criteria": criteria,
            "documents": articles,
            "secretary_name": (
                self.model.secretary_name if self.model.secretary_name else "Н.Еламанов"
            ),
            "summary": summary,
            "conclusion": conclusion,
        }

        return data

    async def build_criteria(
        self, application_documents: list[ApplicationDocumentEntity], application_status_id: int
    ):
        """
        Форматирует список ApplicationDocumentEntity:
          - если все документы выполнены → ["выполнены все требования;"]
          - если есть невыполненные → ["не выполнены требования  - title1, title2, ...;"]
        """
        grouped: dict[int, dict[str, list[str]]] = {}

        for doc in application_documents:
            criteria = await self.criteria_repository.get_first_with_filters(
                filters=[
                    self.criteria_repository.model.category_id == doc.category_id,
                    self.criteria_repository.model.application_id
                    == self.model.application_id,
                ],
                options=self.criteria_repository.default_relationships(),
            )

            group = grouped.setdefault(
                criteria.id, {"title": criteria.category.title_ru, "failed_titles": []}
            )

            # Считаем, что control_comment_ru => требование не выполнено
            if doc.control_comment_ru and application_status_id != DbValueConstants.ApplicationStatusApprovedID:
                group["failed_titles"].append(doc.title_ru)

        # Финальная сборка
        result = []
        for group in grouped.values():
            failed = group["failed_titles"]
            status = False
            if failed:
                joined_titles = ", ".join(failed)
                docs = f"не выполнены требования  - {joined_titles};"
            else:
                docs = "выполнены все требования;"
                status = True

            result.append(
                {"title": group["title"], "description": docs, "status": status}
            )

        return result

    async def build_articles(
        self, application_documents: list[ApplicationDocumentEntity], application_status_id: int
    ):
        grouped = {}

        for doc in application_documents:
            criteria = await self.criteria_repository.get_first_with_filters(
                filters=[
                    self.criteria_repository.model.category_id == doc.category_id,
                    self.criteria_repository.model.application_id
                    == self.model.application_id,
                ],
                options=self.criteria_repository.default_relationships(),
            )

            group = grouped.setdefault(
                criteria.id, {"title": criteria.category.title_ru, "failed_titles": []}
            )

            # control_comment_ru => требование не выполнено
            if doc.control_comment_ru and application_status_id != DbValueConstants.ApplicationStatusApprovedID:
                group["failed_titles"].append(
                    {
                        "title": doc.title_ru,
                        "comment": doc.control_comment_ru,
                        "deadline": f"Устранить несоответствие в срок до {doc.deadline.strftime("%d.%m.%Y")}",
                    }
                )

        # Формируем результат только для непустых docs
        result = [
            {"title": group["title"], "docs": group["failed_titles"]}
            for group in grouped.values()
            if group["failed_titles"]  # фильтруем пустые списки
        ]

        return result

    async def build_experts(
        self, application_documents: list[ApplicationDocumentEntity]
    ):
        grouped = {}
        for doc in application_documents:
            criteria = await self.criteria_repository.get_first_with_filters(
                filters=[
                    self.criteria_repository.model.category_id == doc.category_id,
                    self.criteria_repository.model.application_id
                    == self.model.application_id,
                ],
                options=self.criteria_repository.default_relationships(),
            )
            expert_key = criteria.checked_by  # группируем по имени эксперта
            if expert_key not in grouped:
                grouped[expert_key] = (
                    f"{criteria.checked_user.position} - <b>{criteria.checked_by}</b>"
                )
        return list(grouped.values())

    def build_conclusion(self, articles: list, club: str, licence: str, season: str, cancel_reason: str):
        if self.model.application.status_id == DbValueConstants.ApplicationStatusRejectedID:
            return {
                1: f"Отказать в выдаче лицензии «{club}», организуемый КФФ в сезоне «{season}» года.",
                2: f"<b>Причина отказа:</b> «{cancel_reason if cancel_reason else ''}»"
            }
        if self.model.application.status_id == DbValueConstants.ApplicationStatusRevokedID:
            return {
                1: f"Отозвать лицензию у «{club}», организованного КФФ в сезоне «{season}» года."
            }
        if not articles:
            # Случай 1 — нет нарушений
            return {
                1: f"Выдать «{club}» Лицензию «{licence}», организуемый КФФ в сезоне «{season}» года."
            }

        # Случай 2 — есть нарушения
        # Собираем список названий разделов через запятую
        sections = ", ".join(article["title"] for article in articles)

        return {
            1: (
                f"Согласно Приложению III Правил по лицензированию:<br>"
                f"- за невыполнение требований по разделам «{sections}» применить санкцию <b>«Замечание»</b>."
            ),
            2: (
                f"Выдать «{club}» Лицензию «{licence}», организуемый КФФ в сезоне «{season}» года."
            ),
            3: (
                "В случае невыполнения решения в установленный срок, "
                "Комиссией по лицензированию будут приняты <b>дополнительные дисциплинарные санкции "
                "(штраф, снятие турнирных очков, отзыв Лицензии)</b> в соответствии Приложением III Правил по лицензированию."
            ),
        }
