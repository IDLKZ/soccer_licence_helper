"""
Report Generation DTOs
DTOs для генерации отчетов
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class GenerateReportRequest:
    """DTO для запроса генерации отчета"""
    report_id: int


@dataclass
class DocumentItemDTO:
    """
    DTO для отдельного документа в статье отчета

    Attributes:
        name: Название документа (title_ru)
        status: Статус ("Принят" или "Отклонен")
        note: Примечание (комментарий или стандартный текст)
    """
    name: str
    status: str  # "Принят" или "Отклонен"
    note: str


@dataclass
class ArticleDTO:
    """
    DTO для статьи отчета (группа документов)

    Attributes:
        title: Название статьи (из document.title_ru)
        documents: Список документов в этой статье
    """
    title: str
    documents: List[DocumentItemDTO]


@dataclass
class ReportDataDTO:
    """
    DTO для данных отчета, передаваемых в шаблон

    Attributes:
        director: Директор и его должность
        expert: Эксперт и его должность
        date: Дата создания отчета (формат dd/mm/yyyy)
        club: Полное название клуба на русском
        articles: Список статей с документами
        summary: Итоговый текст заключения
        signed_by: ФИО подписавшего (проверявшего)
        signed_date: Дата подписи (формат dd.mm.yyyy)
        status: Общий статус (все документы приняты = True)
        logo_base64: Логотип в формате base64
    """
    director: str
    expert: str
    date: str
    club: str
    articles: List[ArticleDTO]
    summary: str
    signed_by: Optional[str]
    signed_date: str
    status: bool
    logo_base64: str


@dataclass
class CategoryExpertMapping:
    """
    Маппинг категорий документов на должности экспертов

    Используется для определения должности эксперта на основе category.value
    """
    legal_documents: str = "Эксперт по правовым критериям"
    financial_documents: str = "Эксперт по финансовым критериям"
    sport_documents: str = "Эксперт по спортивным критериям"
    infrastructure_documents: str = "Эксперт по инфраструктурным критериям"
    social_documents: str = "Эксперт по критериям социальной и экологической ответственности"
    hr_documents: str = "Эксперт по кадровым и административным критериям"

    def get_position(self, category_value: str, user_full_name: str, category_title_ru: str) -> str:
        """
        Получить должность эксперта для категории

        Args:
            category_value: Значение категории (например, "legal_documents")
            user_full_name: ФИО пользователя
            category_title_ru: Название категории на русском (fallback)

        Returns:
            Строка с должностью эксперта
        """
        mapping = {
            "legal-documents": f"{self.legal_documents} - {user_full_name}",
            "financial-documents": f"{self.financial_documents} - {user_full_name}",
            "sport-documents": f"{self.sport_documents} - {user_full_name}",  # Без имени для спортивных
            "infrastrukturnye-kriterii": f"{self.infrastructure_documents} - {user_full_name}",
            "kriteriy-socialnoy-i-ekologicheskoy-otvetstvennosti": f"{self.social_documents} - {user_full_name}",
            "kadrovye-i-administrativnye-kriterii": f"{self.hr_documents} - {user_full_name}",
        }
        return mapping.get(category_value, category_title_ru)
