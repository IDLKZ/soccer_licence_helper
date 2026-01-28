"""
Generate Initial Report Use Case
Use Case для генерации начального отчета - работает со SQLAlchemy моделями напрямую
"""
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.application_initial_report import ApplicationInitialReportModel
from app.infrastructure.database.models.application_criteria import ApplicationCriteriaModel
from app.infrastructure.database.models.application_document import ApplicationDocumentModel
from app.infrastructure.database.models.application import ApplicationModel
from app.application.dto.initial_report_dto import (
    InitialReportDataDTO,
    InitialReportDocumentDTO
)


class GenerateInitialReportUseCase:
    """
    Use Case для генерации данных начального отчета
    Работает со SQLAlchemy моделями напрямую для упрощения доступа к связям
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, report_id: int, logo_base64: str, sign_img: str) -> InitialReportDataDTO:
        """
        Выполнить генерацию данных начального отчета

        Args:
            report_id: ID начального отчета
            logo_base64: Логотип в формате base64
            sign_img: Подпись ответственного

        Returns:
            InitialReportDataDTO с данными для шаблона

        Raises:
            ValueError: Если отчет не найден
        """
        # Получаем отчет со всеми связями
        report = await self._get_report_with_relations(report_id)
        if not report:
            raise ValueError(f"Initial report with id {report_id} not found")

        # Получаем критерии
        criteria = report.criteria
        if not criteria:
            raise ValueError(f"Criteria not found for report {report_id}")

        # Получаем заявку
        application = report.application if report.application else criteria.application
        if not application:
            raise ValueError(f"Application not found for report {report_id}")

        # Получаем клуб
        club = application.club
        if not club:
            raise ValueError(f"Club not found for application {application.id}")

        # Получаем категорию
        category = criteria.category
        if not category:
            raise ValueError(f"Category not found for criteria {criteria.id}")

        # Получаем документы
        application_documents = await self._get_documents(
            application_id=application.id,
            category_id=category.id
        )

        # Строим данные для шаблона
        expert = f"Эксперту по отделу - {category.title_ru}"
        director = criteria.first_checked_by if criteria.first_checked_by else ""
        date = report.created_at.strftime("%d.%m.%Y")
        club_name = club.full_name_ru

        # Строим список документов
        documents = self._build_documents_list(application_documents)

        # Формируем DTO
        report_data = InitialReportDataDTO(
            expert=expert,
            director=director,
            date=date,
            club=club_name,
            documents=documents,
            sign_img=sign_img
        )

        return report_data

    async def _get_report_with_relations(self, report_id: int) -> ApplicationInitialReportModel:
        """Получить начальный отчет со всеми связями"""
        query = (
            select(ApplicationInitialReportModel)
            .where(ApplicationInitialReportModel.id == report_id)
            .options(
                selectinload(ApplicationInitialReportModel.application)
                .selectinload(ApplicationModel.club)
            )
            .options(
                selectinload(ApplicationInitialReportModel.criteria)
                .selectinload(ApplicationCriteriaModel.application)
                .selectinload(ApplicationModel.club)
            )
            .options(
                selectinload(ApplicationInitialReportModel.criteria)
                .selectinload(ApplicationCriteriaModel.category)
            )
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _get_documents(
        self,
        application_id: int,
        category_id: int
    ) -> List[ApplicationDocumentModel]:
        """Получить документы заявки"""
        query = (
            select(ApplicationDocumentModel)
            .where(
                ApplicationDocumentModel.application_id == application_id,
                ApplicationDocumentModel.category_id == category_id
            )
            .options(selectinload(ApplicationDocumentModel.document))
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    def _build_documents_list(
        self,
        application_documents: List[ApplicationDocumentModel]
    ) -> List[InitialReportDocumentDTO]:
        """Построить список документов для начального отчета"""
        documents = []

        for idx, doc in enumerate(application_documents, start=1):
            # Имя документа
            doc_name = doc.title if doc.title else (
                doc.document.title_ru if doc.document else "Документ"
            )

            document_title = doc.document.title_ru if doc.document else "Документ"

            # Дата подачи
            submission_date = doc.created_at.strftime("%d.%m.%Y") if doc.created_at else ""

            # Примечания
            notes = doc.info if doc.info else ""

            documents.append(
                InitialReportDocumentDTO(
                    number=idx,
                    name=doc_name,
                    submission_date=submission_date,
                    notes=notes,
                    document_title=document_title
                )
            )

        return documents
