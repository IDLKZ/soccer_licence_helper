"""
Generate Report Use Case
Use Case для генерации отчета по заявке
"""
from typing import List, Optional
from app.domain.repositories.application_report_repository import IApplicationReportRepository
from app.domain.repositories.application_criteria_repository import IApplicationCriteriaRepository
from app.domain.repositories.club_repository import IClubRepository
from app.domain.repositories.license_repository import ILicenseRepository
from app.domain.repositories.application_document_repository import IApplicationDocumentRepository
from app.domain.repositories.user_repository import IUserRepository
from app.domain.repositories.category_document_repository import ICategoryDocumentRepository
from app.domain.entities.application_report import ApplicationReport
from app.domain.entities.application_criteria import ApplicationCriteria
from app.domain.entities.application_document import ApplicationDocument
from app.application.dto.report_generation_dto import (
    ReportDataDTO,
    ArticleDTO,
    DocumentItemDTO,
    CategoryExpertMapping
)


class GenerateReportUseCase:
    """
    Use Case для генерации данных отчета

    Получает все необходимые данные из репозиториев,
    строит структуру отчета и возвращает DTO для рендеринга
    """

    def __init__(
        self,
        report_repository: IApplicationReportRepository,
        criteria_repository: IApplicationCriteriaRepository,
        club_repository: IClubRepository,
        license_repository: ILicenseRepository,
        document_repository: IApplicationDocumentRepository,
        user_repository: IUserRepository,
        category_repository: ICategoryDocumentRepository
    ):
        self.report_repository = report_repository
        self.criteria_repository = criteria_repository
        self.club_repository = club_repository
        self.license_repository = license_repository
        self.document_repository = document_repository
        self.user_repository = user_repository
        self.category_repository = category_repository
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
        # Валидация
        report = await self._validate_report(report_id)

        # Построение данных отчета
        report_data = await self._build_report_data(report, logo_base64)

        return report_data

    async def _validate_report(self, report_id: int) -> ApplicationReport:
        """
        Валидировать существование отчета

        Args:
            report_id: ID отчета

        Returns:
            ApplicationReport

        Raises:
            ValueError: Если отчет не найден
        """
        report = await self.report_repository.get_by_id_with_relations(report_id)
        if not report:
            raise ValueError(f"Report with id {report_id} not found")
        return report

    async def _build_report_data(
        self,
        report: ApplicationReport,
        logo_base64: str
    ) -> ReportDataDTO:
        """
        Построить данные отчета

        Args:
            report: Сущность ApplicationReport
            logo_base64: Логотип в base64

        Returns:
            ReportDataDTO со всеми данными
        """
        # Получаем критерии со всеми связями
        criteria = await self.criteria_repository.get_by_id_with_relations(
            report.criteria_id
        )
        if not criteria:
            raise ValueError(f"Criteria with id {report.criteria_id} not found")

        # Получаем клуб
        club = await self.club_repository.get_by_id(criteria.application_id)
        if not club:
            raise ValueError(f"Club not found for application {criteria.application_id}")

        # Получаем лицензию
        license_entity = await self.license_repository.get_by_id_with_relations(
            criteria.application_id  # Предполагаем что application имеет license_id
        )
        if not license_entity:
            raise ValueError("License not found")

        # Получаем документы
        application_documents = await self.document_repository.get_by_application_and_category(
            application_id=criteria.application_id,
            category_id=criteria.category_id
        )

        # Строим articles
        articles = self._build_articles(application_documents, report.status)

        # Строим summary
        summary = self._build_summary(
            application_documents=application_documents,
            report_status=report.status,
            club_name=club.full_name_ru,
            category_title=criteria.category_id,  # Потребуется получить category
            season_title=license_entity.id  # Потребуется season.title_ru
        )

        # Определяем директора и эксперта
        director = await self._build_director_string(criteria)
        expert = await self._build_expert_string(criteria)

        # Формируем DTO
        report_data = ReportDataDTO(
            director=director,
            expert=expert,
            date=report.created_at.strftime("%d/%m/%Y"),
            club=club.full_name_ru,
            articles=articles,
            summary=summary,
            signed_by=criteria.checked_by if hasattr(criteria, 'checked_by') else None,
            signed_date=report.created_at.strftime("%d.%m.%Y"),
            status=self._calculate_overall_status(application_documents, report.status),
            logo_base64=logo_base64
        )

        return report_data

    def _build_articles(
        self,
        application_documents: List[ApplicationDocument],
        report_status: int
    ) -> List[ArticleDTO]:
        """
        Построить articles из документов

        Args:
            application_documents: Список документов заявки
            report_status: Статус отчета (0 = все документы, 1 = только принятые)

        Returns:
            Список ArticleDTO
        """
        # Фильтрация документов в зависимости от report_status
        if report_status == 1:
            # Только документы со статусом True
            filtered_docs = [doc for doc in application_documents if doc.status]
        else:
            # Все документы
            filtered_docs = application_documents

        # Группировка по document_id
        grouped = {}
        for doc in filtered_docs:
            doc_id = doc.document_id

            if doc_id not in grouped:
                # Предполагаем что doc.document существует и имеет title_ru
                # В реальности это нужно будет получить из связанной сущности
                grouped[doc_id] = {
                    "title": getattr(doc, 'document_title_ru', 'Документ'),
                    "documents": []
                }

            # Определяем статус и примечание
            status_value = "Принят" if doc.status else "Отклонен"
            note_value = (
                "Соответствует требованиям процедуры лицензирования. "
                "Не противоречит действующему законодательству РК."
                if doc.status
                else (doc.comment_ru or "Не указано")
            )

            grouped[doc_id]["documents"].append(
                DocumentItemDTO(
                    name=doc.title_ru,
                    status=status_value,
                    note=note_value
                )
            )

        # Сортировка по document_id и преобразование в ArticleDTO
        sorted_items = sorted(grouped.items(), key=lambda item: item[0])
        articles = [
            ArticleDTO(
                title=item[1]["title"],
                documents=item[1]["documents"]
            )
            for item in sorted_items
        ]

        return articles

    def _build_summary(
        self,
        application_documents: List[ApplicationDocument],
        report_status: int,
        club_name: str,
        category_title: str,
        season_title: str
    ) -> str:
        """
        Построить итоговый текст заключения

        Args:
            application_documents: Список документов
            report_status: Статус отчета
            club_name: Название клуба
            category_title: Название категории
            season_title: Название сезона

        Returns:
            Итоговый текст на русском языке
        """
        # Фильтрация статусов в зависимости от report_status
        if report_status == 1:
            statuses = [doc.status for doc in application_documents if doc.status]
        else:
            statuses = [doc.status for doc in application_documents]

        # Базовый текст
        base_text = (
            f"В результате проведенного анализа документов, предоставленных "
            f"Соискателем лицензии – {club_name} в Департамент лицензирования, "
            f'на предмет их соответствия разделу "{category_title}", согласно требованиям '
            f"«Правил по лицензированию футбольных клубов для участия в соревнованиях, "
            f"организуемых КФФ», выпуск {season_title} г., "
        )

        # Определяем окончание на основе статусов
        if all(statuses):
            conclusion = "все предоставленные документы соответствуют требованиям процедуры лицензирования."
        elif not any(statuses):
            conclusion = "все документы были отклонены как не соответствующие требованиям."
        else:
            conclusion = "некоторые документы не соответствуют требованиям и были отклонены."

        return base_text + conclusion

    def _calculate_overall_status(
        self,
        application_documents: List[ApplicationDocument],
        report_status: int
    ) -> bool:
        """
        Вычислить общий статус (все документы приняты?)

        Args:
            application_documents: Список документов
            report_status: Статус отчета

        Returns:
            True если все документы приняты
        """
        # Фильтрация в зависимости от report_status
        if report_status == 1:
            statuses = [doc.status for doc in application_documents if doc.status]
        else:
            statuses = [doc.status for doc in application_documents]

        return all(statuses) if statuses else False

    async def _build_director_string(self, criteria: ApplicationCriteria) -> str:
        """
        Построить строку с информацией о директоре

        Args:
            criteria: Критерии заявки

        Returns:
            Строка "Должность - ФИО"
        """
        # Предполагаем что criteria имеет first_checked_user и first_checked_by
        position = getattr(criteria, 'first_checked_user_position', '')
        name = getattr(criteria, 'first_checked_by', '')
        return f"{position} - {name}" if position or name else ""

    async def _build_expert_string(self, criteria: ApplicationCriteria) -> str:
        """
        Построить строку с информацией об эксперте

        Args:
            criteria: Критерии заявки

        Returns:
            Строка "Эксперт по ... критериям - ФИО"
        """
        # Получаем пользователя
        if not hasattr(criteria, 'checked_user_id') or not criteria.checked_user_id:
            return ""

        user = await self.user_repository.get_by_id(criteria.checked_user_id)
        if not user:
            return ""

        # Получаем категорию
        category = await self.category_repository.get_by_id(criteria.category_id)
        if not category:
            return ""

        # Используем маппер для определения должности
        position = self.expert_mapper.get_position(
            category_value=category.value,
            user_full_name=user.get_full_name(),
            category_title_ru=category.title_ru
        )

        return position
