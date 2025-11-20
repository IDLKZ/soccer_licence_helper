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

        # Получаем пользователя департамента (из первого документа с first_checked_by_id)
        department_user = await self._get_department_user(application_id)

        # Строим список отчетов
        reports_data = await self.build_reports(reports, application_id)

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

    async def _get_documents_by_ids(self, document_ids: List[str], application_id: int) -> List[ApplicationDocumentModel]:
        """Получить документы по списку ID документов"""
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
            .options(
                selectinload(ApplicationDocumentModel.document)
            )
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def _get_department_user(self, application_id: int) -> UserModel | None:
        """Получить пользователя департамента из документов заявки"""
        # Находим первый документ с first_checked_by_id
        query = (
            select(ApplicationDocumentModel)
            .where(
                and_(
                    ApplicationDocumentModel.application_id == application_id,
                    ApplicationDocumentModel.first_checked_by_id.is_not(None)
                )
            )
            .limit(1)
        )

        result = await self.db.execute(query)
        document = result.scalar_one_or_none()

        if document and document.first_checked_by_id:
            return await self._get_user(document.first_checked_by_id)

        return None

    async def _get_user(self, user_id: int) -> UserModel | None:
        """Получить пользователя по ID"""
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def build_reports(
        self,
        reports: List[ApplicationReportModel],
        application_id: int
    ) -> List[DepartmentReportItemDTO]:
        """
        Построить список отчетов с документами
        Для каждого отчета используется его list_documents
        """
        result = []

        for report in reports:
            # Получаем эксперта
            expert = await self._get_user(report.criteria.checked_by_id)

            # Формируем позицию эксперта
            expert_position = self._get_expert_position(expert, report.criteria)

            # Собираем документы для данного отчета из list_documents
            documents_list = []

            # Проверяем наличие list_documents в отчете
            if report.list_documents:
                # Получаем документы по ID из list_documents (это ID записей application_documents)
                report_documents = await self._get_documents_by_ids(
                    report.list_documents,
                    application_id
                )

                # Создаем словарь для быстрого доступа к документам по ID записи application_documents
                docs_dict: Dict[int, ApplicationDocumentModel] = {
                    doc.id: doc for doc in report_documents
                }

                # Обрабатываем документы в порядке list_documents
                for doc_id_str in report.list_documents:
                    doc_id = int(doc_id_str)
                    doc = docs_dict.get(doc_id)

                    if doc:
                        status_value = "критерий выполнен;" if doc.is_industry_passed else f"критерий выполнен частично; ({doc.industry_comment})"

                        # Формат: {document_id: "title - статус"}
                        documents_list.append({
                            doc_id_str: f"{doc.document.title_ru} - {status_value}"
                        })
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
