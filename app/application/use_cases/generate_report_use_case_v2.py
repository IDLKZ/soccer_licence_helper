"""
Generate Report Use Case V2
Use Case для генерации отчета - работает со SQLAlchemy моделями напрямую
"""
from typing import List
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.application_report import ApplicationReportModel
from app.infrastructure.database.models.application_criteria import ApplicationCriteriaModel
from app.infrastructure.database.models.application_document import ApplicationDocumentModel
from app.infrastructure.database.models.category_document import CategoryDocumentModel
from app.infrastructure.database.models.application import ApplicationModel
from app.infrastructure.database.models.license import LicenseModel
from app.application.dto.report_generation_dto import (
    ReportDataDTO,
    ArticleDTO,
    DocumentItemDTO,
    CategoryExpertMapping
)


class GenerateReportUseCaseV2:
    """
    Use Case для генерации данных отчета
    Работает со SQLAlchemy моделями напрямую для упрощения доступа к связям
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.expert_mapper = CategoryExpertMapping()

    async def execute(self, report_id: int, logo_base64: str) -> ReportDataDTO:
        """
        Выполнить генерацию данных отчета

        Args:
            report_id: ID отчета
            logo_base64: Логотип в формате base64

        Returns:
            ReportDataDTO с данными для шаблона

        Raises:
            ValueError: Если отчет не найден
        """
        # Получаем отчет со всеми связями
        report = await self._get_report_with_relations(report_id)
        if not report:
            raise ValueError(f"Report with id {report_id} not found")

        # Получаем критерии
        criteria = report.criteria
        if not criteria:
            raise ValueError(f"Criteria not found for report {report_id}")

        # Получаем заявку
        application = criteria.application
        if not application:
            raise ValueError(f"Application not found for criteria {criteria.id}")

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

        # Получаем категорию
        category = criteria.category
        if not category:
            raise ValueError(f"Category not found for criteria {criteria.id}")

        # Получаем документы из list_documents отчета
        if report.list_documents:
            application_documents = await self._get_documents_by_ids(
                report.list_documents,
                application.id
            )
        else:
            application_documents = []

        # Строим articles
        articles = self._build_articles(application_documents, report.status, report.list_documents if report.list_documents else [])

        # Строим summary
        summary = self._build_summary(
            application_documents=application_documents,
            report_status=report.status,
            club_name=club.full_name_ru,
            category_title=category.title_ru,
            season_title=season.title_ru
        )

        # Определяем директора и эксперта
        director = self._build_director_string(criteria)
        expert = await self._build_expert_string(criteria, category)

        # Формируем DTO
        report_data = ReportDataDTO(
            director=director,
            expert=expert,
            date=report.created_at.strftime("%d/%m/%Y"),
            club=club.full_name_ru,
            articles=articles,
            summary=summary,
            signed_by=criteria.checked_by if criteria.checked_by else None,
            signed_date=report.created_at.strftime("%d.%m.%Y"),
            status=self._calculate_overall_status(application_documents),
            logo_base64=logo_base64
        )

        return report_data

    async def _get_report_with_relations(self, report_id: int) -> ApplicationReportModel:
        """Получить отчет со всеми связями"""
        query = (
            select(ApplicationReportModel)
            .where(ApplicationReportModel.id == report_id)
            .options(
                selectinload(ApplicationReportModel.criteria)
                .selectinload(ApplicationCriteriaModel.application)
                .selectinload(ApplicationModel.club)
            )
            .options(
                selectinload(ApplicationReportModel.criteria)
                .selectinload(ApplicationCriteriaModel.application)
                .selectinload(ApplicationModel.license)
                .selectinload(LicenseModel.season)
            )
            .options(
                selectinload(ApplicationReportModel.criteria)
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
            .options(selectinload(ApplicationDocumentModel.document))
        )

        result = await self.db.execute(query)
        return list(result.scalars().all())

    def _build_articles(
        self,
        application_documents: List[ApplicationDocumentModel],
        report_status: int,
        list_documents: List[str]
    ) -> List[ArticleDTO]:
        """Построить articles из документов в порядке list_documents"""
        # Фильтрация документов в зависимости от report_status
        # if report_status == 1:
        #     filtered_docs = [doc for doc in application_documents if doc.is_industry_passed]
        # else:
        #     filtered_docs = application_documents
        filtered_docs = application_documents

        # Создаем словарь по ID записи application_documents
        docs_by_id = {doc.id: doc for doc in filtered_docs}

        # Группировка по document_id для объединения документов с одним document_id
        grouped = {}
        for doc in filtered_docs:
            doc_id = doc.document_id

            if doc_id not in grouped:
                grouped[doc_id] = {
                    "title": doc.document.title_ru if doc.document else "Документ",
                    "documents": [],
                    "app_doc_ids": []  # Храним id записей application_documents
                }

            # Определяем статус и примечание
            status_value = "Принят" if doc.is_industry_passed else "Отклонен"
            note_value = (
                "Соответствует требованиям процедуры лицензирования. "
                "Не противоречит действующему законодательству РК."
                if doc.is_industry_passed
                else (doc.industry_comment or "Не указано")
            )

            grouped[doc_id]["documents"].append(
                DocumentItemDTO(
                    name=doc.title or "Документ",
                    status=status_value,
                    note=note_value
                )
            )
            grouped[doc_id]["app_doc_ids"].append(doc.id)

        # Сортировка по порядку в list_documents
        # list_documents содержит ID записей application_documents
        articles = []
        added_doc_ids = set()  # Чтобы не добавлять дубли

        for app_doc_id_str in list_documents:
            app_doc_id = int(app_doc_id_str)
            doc = docs_by_id.get(app_doc_id)

            if doc and doc.document_id not in added_doc_ids:
                added_doc_ids.add(doc.document_id)
                articles.append(
                    ArticleDTO(
                        title=grouped[doc.document_id]["title"],
                        documents=grouped[doc.document_id]["documents"]
                    )
                )

        return articles

    def _build_summary(
        self,
        application_documents: List[ApplicationDocumentModel],
        report_status: int,
        club_name: str,
        category_title: str,
        season_title: str
    ) -> str:
        """Построить итоговый текст заключения"""
        # Фильтрация статусов
        if report_status == 1:
            statuses = [doc.is_industry_passed for doc in application_documents if doc.is_industry_passed]
        else:
            statuses = [doc.is_industry_passed for doc in application_documents]

        # Базовый текст
        base_text = (
            f"В результате проведенного анализа документов, предоставленных "
            f"Соискателем лицензии – {club_name} в Департамент лицензирования, "
            f'на предмет их соответствия разделу "{category_title}", согласно требованиям '
            f"«Правил по лицензированию футбольных клубов для участия в соревнованиях, "
            f"организуемых КФФ», выпуск {season_title} г., "
        )

        # Определяем окончание
        if all(statuses):
            conclusion = "все предоставленные документы соответствуют требованиям процедуры лицензирования."
        elif not any(statuses):
            conclusion = "все документы были отклонены как не соответствующие требованиям."
        else:
            conclusion = "некоторые документы не соответствуют требованиям и были отклонены."

        return base_text + conclusion

    def _calculate_overall_status(
        self,
        application_documents: List[ApplicationDocumentModel]
    ) -> bool:
        """Вычислить общий статус"""
        statuses = [doc.is_industry_passed for doc in application_documents]

        if all(statuses):
            result = 1
        elif any(statuses):
            result = 0
        else:
            result = -1

        return result

    def _build_director_string(self, criteria: ApplicationCriteriaModel) -> str:
        """Построить строку с информацией о директоре"""
        # В БД хранится только имя в текстовом поле
        name = criteria.first_checked_by if criteria.first_checked_by else ''
        return name

    async def _build_expert_string(
        self,
        criteria: ApplicationCriteriaModel,
        category: CategoryDocumentModel
    ) -> str:
        """Построить строку с информацией об эксперте"""
        if not criteria.checked_by:
            return ""

        # В БД хранится имя в текстовом поле
        user_full_name = criteria.checked_by
        print(f"user_full_name: {user_full_name}")
        # Используем маппер для определения должности
        position = self.expert_mapper.get_position(
            category_value=category.value,
            user_full_name=user_full_name,
            category_title_ru=category.title_ru
        )

        return position

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
