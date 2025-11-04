"""
Generate Department Report Use Case
Use Case для генерации отчета департамента
"""
from typing import List, Dict
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.application_report import ApplicationReportModel
from app.infrastructure.database.models.application_document import ApplicationDocumentModel
from app.infrastructure.database.models.application_criteria import ApplicationCriteriaModel
from app.infrastructure.database.models.application import ApplicationModel
from app.infrastructure.database.models.club import ClubModel
from app.infrastructure.database.models.user import UserModel
from app.application.dto.department_report_dto import (
    DepartmentReportDataDTO,
    DepartmentReportItemDTO,
)


class GenerateDepartmentReportUseCase:
    """Use Case для генерации отчета департамента"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, report_id: int, logo_base64: str, sign_img: str) -> DepartmentReportDataDTO:
        """
        Выполнить генерацию отчета департамента

        Args:
            report_id: ID отчета
            logo_base64: Логотип в формате base64
            sign_img: Подпись в формате base64

        Returns:
            DepartmentReportDataDTO с данными для шаблона

        Raises:
            ValueError: Если отчет не найден
        """
        # Получаем отчет со связями
        report = await self._get_report_with_relations(report_id)
        if not report:
            raise ValueError(f"Report with id {report_id} not found")

        # Получаем application через criteria
        application_id = report.application_id

        # Получаем клуб
        club = await self._get_club(application_id)
        if not club:
            raise ValueError(f"Club not found for application {application_id}")

        # Получаем все отчеты для данной заявки со статусом 1 и criteria_id не null
        reports = await self._get_application_reports(application_id)

        # Получаем все документы заявки
        application_documents = await self._get_application_documents(application_id)

        # Получаем пользователя департамента (из первого документа с first_checked_by_id)
        department_user = await self._get_department_user(application_documents)

        # Строим список отчетов
        reports_data = await self.build_reports(reports, application_documents)

        # Формируем DTO
        department_report_data = DepartmentReportDataDTO(
            department=self._get_user_full_name(department_user) if department_user else "",
            position=department_user.position if department_user and department_user.position else "",
            date=report.created_at.strftime("%d/%m/%Y"),
            club=club.full_name_ru,
            reports=reports_data,
            logo_base64=logo_base64,
            sign_img=sign_img
        )

        return department_report_data

    async def _get_report_with_relations(self, report_id: int) -> ApplicationReportModel:
        """Получить отчет со всеми связями"""
        query = (
            select(ApplicationReportModel)
            .where(ApplicationReportModel.id == report_id)
            .options(
                selectinload(ApplicationReportModel.application)
            )
            .options(
                selectinload(ApplicationReportModel.criteria)
                .selectinload(ApplicationCriteriaModel.category)
            )
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _get_club(self, application_id: int) -> ClubModel:
        """Получить клуб по application_id"""
        query = (
            select(ClubModel)
            .join(ApplicationModel, ApplicationModel.club_id == ClubModel.id)
            .where(ApplicationModel.id == application_id)
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _get_application_reports(self, application_id: int) -> List[ApplicationReportModel]:
        """Получить все отчеты для заявки с criteria_id и status=1"""
        query = (
            select(ApplicationReportModel)
            .where(
                and_(
                    ApplicationReportModel.application_id == application_id,
                    ApplicationReportModel.criteria_id.is_not(None),
                    ApplicationReportModel.status == 1
                )
            )
            .options(
                selectinload(ApplicationReportModel.criteria)
                .selectinload(ApplicationCriteriaModel.category)
            )
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def _get_application_documents(self, application_id: int) -> List[ApplicationDocumentModel]:
        """Получить все документы заявки"""
        query = (
            select(ApplicationDocumentModel)
            .where(ApplicationDocumentModel.application_id == application_id)
            .options(
                selectinload(ApplicationDocumentModel.document)
            )
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def _get_department_user(self, documents: List[ApplicationDocumentModel]) -> UserModel | None:
        """Получить пользователя департамента из документов"""
        # Ищем первый документ с first_checked_by_id
        for doc in documents:
            if doc.first_checked_by_id:
                user = await self._get_user(doc.first_checked_by_id)
                if user:
                    return user
        return None

    async def _get_user(self, user_id: int) -> UserModel | None:
        """Получить пользователя по ID"""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def build_reports(
        self,
        reports: List[ApplicationReportModel],
        application_documents: List[ApplicationDocumentModel]
    ) -> List[DepartmentReportItemDTO]:
        """
        Построить список отчетов с документами
        Группирует документы по отчетам (по category_id)
        """
        # Индексация документов по category_id
        docs_by_category: Dict[int, List[ApplicationDocumentModel]] = {}
        for doc in application_documents:
            docs_by_category.setdefault(doc.category_id, []).append(doc)

        result = []

        for report in reports:
            # Получаем эксперта
            expert = await self._get_user(report.criteria.checked_by_id)

            # Формируем позицию эксперта
            expert_position = self._get_expert_position(expert, report.criteria)

            # Собираем документы для данного отчета
            documents_list = []
            added_doc_ids = set()

            category_id = report.criteria.category_id
            for doc in docs_by_category.get(category_id, []):
                doc_id_str = str(doc.document_id)

                # Проверяем, был ли документ уже добавлен (убираем дубли)
                if doc_id_str not in added_doc_ids:
                    status_value = "критерий выполнен;" if report.status else "критерий выполнен частично;"
                    added_doc_ids.add(doc_id_str)

                    # Формат: {document_id: "title - статус"}
                    documents_list.append({
                        doc_id_str: f"{doc.document.title_ru} - {status_value}"
                    })

            # Сортируем документы по ID
            documents_list.sort(key=lambda d: int(list(d.keys())[0]))

            result.append(
                DepartmentReportItemDTO(
                    date=report.created_at.strftime("%d.%m.%Y"),
                    expert=expert_position,
                    documents=documents_list
                )
            )

        return result

    def _get_expert_position(self, expert: UserModel | None, criteria: ApplicationCriteriaModel) -> str:
        """Получить позицию эксперта"""
        if not expert:
            return "Эксперт"

        # Если есть position, используем его
        if expert.position:
            return f"{expert.position} - {self._get_user_full_name(expert)}"

        # Иначе формируем строку на основе категории
        category_title = criteria.category.title_ru if criteria.category else "Раздел"
        return f"Эксперт по разделу «{category_title}» - {self._get_user_full_name(expert)}"

    def _get_user_full_name(self, user: UserModel | None) -> str:
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
