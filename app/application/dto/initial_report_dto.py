"""
Initial Report Generation DTOs
DTO для генерации начальных отчетов
"""
from dataclasses import dataclass
from typing import List


@dataclass
class InitialReportDocumentDTO:
    """DTO для документа в начальном отчете"""
    number: int
    name: str
    submission_date: str
    notes: str


@dataclass
class InitialReportDataDTO:
    """DTO для данных начального отчета"""
    expert: str  # Эксперту по отделу - {category.title_ru}
    director: str  # От кого
    date: str  # Дата отчета
    club: str  # Заявитель
    documents: List[InitialReportDocumentDTO]  # Список документов
