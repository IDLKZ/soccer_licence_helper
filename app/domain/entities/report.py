"""
Domain entity for Report
Бизнес-сущность отчета - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class ReportStatus(str, Enum):
    """Статусы отчета"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportType(str, Enum):
    """Типы отчетов"""
    LICENSE_SUMMARY = "license_summary"
    LICENSE_DETAILS = "license_details"
    EXPIRATION_REPORT = "expiration_report"
    CUSTOM = "custom"


@dataclass
class Report:
    """
    Бизнес-сущность отчета

    Attributes:
        id: Уникальный идентификатор
        name: Название отчета
        report_type: Тип отчета
        status: Текущий статус
        parameters: Параметры генерации отчета
        file_path: Путь к сгенерированному файлу
        created_at: Дата создания
        updated_at: Дата последнего обновления
        completed_at: Дата завершения генерации
        error_message: Сообщение об ошибке (если есть)
    """
    name: str
    report_type: ReportType
    status: ReportStatus = ReportStatus.PENDING
    parameters: Optional[dict] = None
    id: Optional[int] = None
    file_path: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    def mark_as_processing(self) -> None:
        """Отметить отчет как обрабатывающийся"""
        self.status = ReportStatus.PROCESSING
        self.updated_at = datetime.utcnow()

    def mark_as_completed(self, file_path: str) -> None:
        """
        Отметить отчет как завершенный

        Args:
            file_path: Путь к сгенерированному файлу
        """
        self.status = ReportStatus.COMPLETED
        self.file_path = file_path
        self.completed_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def mark_as_failed(self, error_message: str) -> None:
        """
        Отметить отчет как неудачный

        Args:
            error_message: Сообщение об ошибке
        """
        self.status = ReportStatus.FAILED
        self.error_message = error_message
        self.updated_at = datetime.utcnow()

    def is_completed(self) -> bool:
        """Проверить, завершен ли отчет"""
        return self.status == ReportStatus.COMPLETED

    def is_processing(self) -> bool:
        """Проверить, обрабатывается ли отчет"""
        return self.status == ReportStatus.PROCESSING

    def is_failed(self) -> bool:
        """Проверить, провалился ли отчет"""
        return self.status == ReportStatus.FAILED

    def can_be_regenerated(self) -> bool:
        """Проверить, можно ли перегенерировать отчет"""
        return self.status in [ReportStatus.FAILED, ReportStatus.COMPLETED]
