"""
Generate Solution Use Case
Use Case для генерации решения - работает со SQLAlchemy моделями напрямую
"""
from typing import List, Dict
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.application_solution import ApplicationSolutionModel
from app.infrastructure.database.models.application_criteria import ApplicationCriteriaModel
from app.infrastructure.database.models.application_document import ApplicationDocumentModel
from app.infrastructure.database.models.application_step import ApplicationStepModel
from app.infrastructure.database.models.application import ApplicationModel
from app.infrastructure.database.models.license import LicenseModel
from app.infrastructure.database.models.club import ClubModel
from app.application.dto.solution_generation_dto import (
    SolutionDataDTO,
    SolutionCriteriaDTO,
    SolutionArticleDTO,
    SolutionDocItemDTO,
)
from app.application.dto.report_generation_dto import CategoryExpertMapping

# Константы статусов (можно вынести в отдельный файл)
APPLICATION_STATUS_APPROVED_ID = 6  # Утвержден
APPLICATION_STATUS_REJECTED_ID = 8  # Отклонен
APPLICATION_STATUS_REVOKED_ID = 7   # Отозван
APPLICATION_STEP_CONTROL_STATUS_ID = 4  # Контроль


class GenerateSolutionUseCase:
    """Use Case для генерации данных решения"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.expert_mapper = CategoryExpertMapping()

    async def execute(self, solution_id: int, logo_base64: str) -> SolutionDataDTO:
        """
        Выполнить генерацию данных решения

        Args:
            solution_id: ID решения
            logo_base64: Логотип в формате base64

        Returns:
            SolutionDataDTO с данными для шаблона

        Raises:
            ValueError: Если решение не найдено
        """
        # Получаем решение со всеми связями
        solution = await self._get_solution_with_relations(solution_id)
        if not solution:
            raise ValueError(f"Solution with id {solution_id} not found")

        # Получаем заявку
        application = solution.application
        if not application:
            raise ValueError(f"Application not found for solution {solution_id}")

        # Получаем клуб
        club = application.club
        if not club:
            raise ValueError(f"Club not found for application {application.id}")

        # Получаем лицензию
        license_entity = application.license
        if not license_entity:
            raise ValueError(f"License not found for application {application.id}")

        # Получаем сезон
        season = license_entity.season
        if not season:
            raise ValueError(f"Season not found for license {license_entity.id}")

        # Получаем документы из list_documents решения
        if solution.list_documents:
            application_documents = await self._get_documents_by_ids(
                solution.list_documents,
                application.id
            )
        else:
            application_documents = []

        # Получаем шаг контроля
        control_step = await self._get_control_step(application.id)

        # Получаем статус заявки из control_step (если есть) или из criteria
        application_criteria = await self._get_application_criteria(application.id)
        application_status_id = control_step.status_id if control_step else (application_criteria.status_id if application_criteria else 0)

        # Строим summary
        summary = (
            f"Комиссия по лицензированию футбольных клубов (далее по тексту - КЛФК), "
            f"рассмотрев представленные Директором Департамента лицензирования "
            f"отчет и учетное дело «{club.full_name_ru}» для получения Лицензии «{license_entity.title_ru}», "
            f"организуемый Казахстанской Федерацией футбола в сезоне "
            f"«{season.title_ru}» года (далее по тексту - «Лицензия»)"
        )

        # Строим данные
        experts = await self.build_experts(application_documents, application.id)
        criteria = await self.build_criteria(application_documents, application.id, application_status_id)
        articles = await self.build_articles(application_documents, application.id, application_status_id)
        conclusion = self.build_conclusion(
            articles=articles,
            club=club.full_name_ru,
            season=season.title_ru,
            license=license_entity.title_ru,
            cancel_reason=control_step.result if control_step else "",
            application_status_id=application.category_id
        )

        # Формируем DTO
        solution_data = SolutionDataDTO(
            meeting_date=(
                solution.meeting_date.strftime("%d/%m/%Y")
                if solution.meeting_date
                else solution.created_at.strftime("%d/%m/%Y")
            ),
            meeting_place=(
                solution.meeting_place
                if solution.meeting_place
                else "г.Астана, пр. Бауыржана Момышулы 5а."
            ),
            department_name=(
                solution.department_name
                if solution.department_name
                else "Комиссия по лицензированию футбольных клубов КФФ"
            ),
            control_position=(
                control_step.responsible.position
                if control_step and control_step.responsible and hasattr(control_step.responsible, 'position') and control_step.responsible.position
                else "Председатель КЛФК"
            ),
            control_name=(
                self._get_user_full_name(control_step.responsible)
                if control_step and control_step.responsible
                else " "
            ),
            experts=experts,
            club_fullname=f"{club.full_name_ru} (БИН {club.bin})",
            club_shortname=club.short_name_ru,
            license=license_entity.title_ru,
            season=season.title_ru,
            criteria=criteria,
            documents=articles,
            secretary_name=solution.secretary_name if solution.secretary_name else "Н.Еламанов",
            summary=summary,
            conclusion=conclusion,
            logo_base64=logo_base64
        )

        return solution_data

    async def _get_solution_with_relations(self, solution_id: int) -> ApplicationSolutionModel:
        """Получить решение со всеми связями"""
        query = (
            select(ApplicationSolutionModel)
            .where(ApplicationSolutionModel.id == solution_id)
            .options(
                selectinload(ApplicationSolutionModel.application)
                .selectinload(ApplicationModel.club)
            )
            .options(
                selectinload(ApplicationSolutionModel.application)
                .selectinload(ApplicationModel.license)
                .selectinload(LicenseModel.season)
            )
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _get_documents(self, application_id: int) -> List[ApplicationDocumentModel]:
        """Получить все документы заявки"""
        query = (
            select(ApplicationDocumentModel)
            .where(ApplicationDocumentModel.application_id == application_id)
            .options(selectinload(ApplicationDocumentModel.category))
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def _get_documents_by_ids(
        self,
        document_ids: List[str],
        application_id: int
    ) -> List[ApplicationDocumentModel]:
        """Получить документы по списку ID записей application_documents"""
        if not document_ids:
            return []

        # Преобразуем строковые ID в целые числа
        int_ids = [int(doc_id) for doc_id in document_ids]

        query = (
            select(ApplicationDocumentModel)
            .where(
                and_(
                    ApplicationDocumentModel.id.in_(int_ids),
                    ApplicationDocumentModel.application_id == application_id
                )
            )
            .options(selectinload(ApplicationDocumentModel.category))
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def _get_control_step(self, application_id: int) -> ApplicationStepModel | None:
        """Получить шаг контроля (status_id = 5)"""
        query = (
            select(ApplicationStepModel)
            .where(
                ApplicationStepModel.application_id == application_id,
                ApplicationStepModel.status_id.in_([9, 10, 11, 12])
            )
            .options(selectinload(ApplicationStepModel.responsible))
            .order_by(ApplicationStepModel.created_at.desc())  # Берем самый свежий
            .limit(1)  # Ограничиваем до одной записи
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def _get_application_criteria(self, application_id: int) -> ApplicationCriteriaModel | None:
        """Получить критерии заявки (первую запись)"""
        query = (
            select(ApplicationCriteriaModel)
            .where(ApplicationCriteriaModel.application_id == application_id)
            .limit(1)
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def build_criteria(
        self,
        application_documents: List[ApplicationDocumentModel],
        application_id: int,
        application_status_id: int
    ) -> List[SolutionCriteriaDTO]:
        """
        Построить список критериев (выполненность требований по категориям)
        """
        grouped: Dict[int, Dict] = {}

        for doc in application_documents:
            # Получаем критерии для документа
            criteria = await self._get_criteria_for_category(doc.category_id, application_id)
            if not criteria:
                continue

            group = grouped.setdefault(
                criteria.id,
                {
                    "title": doc.category.title_ru if doc.category else "Категория",
                    "failed_titles": []
                }
            )

            # Считаем, что control_comment => требование не выполнено
            if doc.is_final_passed is None:
                group["failed_titles"].append(doc.title or "Документ")

        # Финальная сборка
        result = []
        for group in grouped.values():
            failed = group["failed_titles"]
            status = False
            if failed:
                joined_titles = ", ".join(failed)
                description = f"не выполнены требования  - {joined_titles};"
            else:
                description = "выполнены все требования;"
                status = True

            result.append(
                SolutionCriteriaDTO(
                    title=group["title"],
                    description=description,
                    status=status
                )
            )

        return result

    async def build_articles(
        self,
        application_documents: List[ApplicationDocumentModel],
        application_id: int,
        application_status_id: int
    ) -> List[SolutionArticleDTO]:
        """
        Построить список статей с невыполненными требованиями
        """
        grouped: Dict[int, Dict] = {}

        for doc in application_documents:
            # Получаем критерии для документа
            criteria = await self._get_criteria_for_category(doc.category_id, application_id)
            if not criteria:
                continue

            group = grouped.setdefault(
                criteria.id,
                {
                    "title": doc.category.title_ru if doc.category else "Категория",
                    "failed_docs": []
                }
            )

            # control_comment => требование не выполнено
            if doc.is_final_passed is None:
                deadline_str = (
                    f"Устранить несоответствие в срок до {doc.deadline.strftime('%d.%m.%Y')}"
                    if doc.deadline
                    else "Устранить несоответствие в установленный срок"
                )

                group["failed_docs"].append(
                    SolutionDocItemDTO(
                        title=doc.title or "Документ",
                        comment=doc.control_comment if doc.control_comment else doc.industry_comment,
                        deadline=deadline_str
                    )
                )

        # Формируем результат только для непустых docs
        result = [
            SolutionArticleDTO(
                title=group["title"],
                docs=group["failed_docs"]
            )
            for group in grouped.values()
            if group["failed_docs"]  # фильтруем пустые списки
        ]

        return result

    async def build_experts(
        self,
        application_documents: List[ApplicationDocumentModel],
        application_id: int
    ) -> List[str]:
        """Построить список экспертов с использованием CategoryExpertMapping"""
        grouped = {}

        for doc in application_documents:
            # Получаем критерии для документа
            criteria = await self._get_criteria_for_category(doc.category_id, application_id)
            if not criteria or not criteria.checked_by:
                continue

            # Получаем категорию
            category = doc.category
            if not category:
                continue

            # Формируем ключ для группировки по категории
            category_key = category.id

            if category_key not in grouped:
                # Используем маппер для определения должности эксперта
                position = self.expert_mapper.get_position(
                    category_value=category.value,
                    user_full_name=criteria.checked_by,
                    category_title_ru=category.title_ru
                )
                grouped[category_key] = f"<b>{position}</b>"

        return list(grouped.values())

    def build_conclusion(
        self,
        articles: List[SolutionArticleDTO],
        club: str,
        license: str,
        season: str,
        cancel_reason: str,
        application_status_id: int
    ) -> Dict[int, str]:
        """Построить заключение в зависимости от статуса заявки"""

        if application_status_id == APPLICATION_STATUS_REJECTED_ID:
            return {
                1: f"Отказать в выдаче лицензии «{club}», организуемый КФФ в сезоне «{season}» года.",
                2: f"<b>Причина отказа:</b> «{cancel_reason if cancel_reason else ''}»"
            }

        if application_status_id == APPLICATION_STATUS_REVOKED_ID:
            return {
                1: f"Отозвать лицензию у «{club}», организованного КФФ в сезоне «{season}» года.",
                1: f"«{club}» отказать в выдаче Лицензии на право участия в турнирах, организуемых КФФ в сезоне «{season}» г.г.",
                2: f"Настоящее решение может быть обжаловано в Апелляционной комиссии по лицензированию футбольных клубов в порядке, определенном «Правилами по лицензированию футбольных клубов РК для участия в соревнованиях, организуемых КФФ»."
            }

        if not articles:
            # Случай 1 — нет нарушений
            return {
                1: f"Выдать «{club}» Лицензию «{license}», организуемый КФФ в сезоне «{season}» года.",
                2: f"Настоящее решение может быть обжаловано в Апелляционной комиссии по лицензированию футбольных клубов в порядке, определенном «Правилами по лицензированию футбольных клубов РК для участия в соревнованиях, организуемых КФФ»."
            }

        # Случай 2 — есть нарушения
        sections = ", ".join(article.title for article in articles)

        return {
            1: (
                f"Согласно Приложению III Правил по лицензированию:<br>"
                f"- за невыполнение требований по разделам «{sections}» применить санкцию <b>«Замечание»</b>."
            ),
            2: (
                f"Выдать «{club}» Лицензию «{license}», организуемый КФФ в сезоне «{season}» года."
            ),
            3: (
                "В случае невыполнения решения в установленный срок, "
                "Комиссией по лицензированию будут приняты <b>дополнительные дисциплинарные санкции "
                "(штраф, снятие турнирных очков, отзыв Лицензии)</b> в соответствии Приложением III Правил по лицензированию."
            ),
            4: (
                "Настоящее решение может быть обжаловано в Апелляционной комиссии по лицензированию футбольных клубов в порядке, определенном «Правилами по лицензированию футбольных клубов РК для участия в соревнованиях, организуемых КФФ»."
            )
        }

    async def _get_criteria_for_category(
        self,
        category_id: int,
        application_id: int
    ) -> ApplicationCriteriaModel | None:
        """Получить критерии для категории"""
        query = (
            select(ApplicationCriteriaModel)
            .where(
                ApplicationCriteriaModel.category_id == category_id,
                ApplicationCriteriaModel.application_id == application_id
            )
            .options(selectinload(ApplicationCriteriaModel.category))
            .limit(1)  # Добавляем ограничение, чтобы избежать множественных записей
        )

        result = await self.db.execute(query)
        return result.scalars().first()

    def _get_user_full_name(self, user) -> str:
        """Получить полное имя пользователя"""
        if not user:
            return ""

        parts = []
        if user.first_name:
            parts.append(user.first_name)
        if user.last_name:
            parts.append(user.last_name)
        if user.patronymic:
            parts.append(user.patronymic)

        return " ".join(parts)
