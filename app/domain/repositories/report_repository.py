"""
Repository interface for Report
Интерфейс репозитория - абстракция для работы с хранилищем данных
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.report import Report, ReportStatus, ReportType


class IReportRepository(ABC):
    """
    Интерфейс репозитория для работы с отчетами
    Определяет контракт для работы с хранилищем данных
    """

    @abstractmethod
    async def create(self, report: Report) -> Report:
        """
        Создать новый отчет

        Args:
            report: Сущность отчета

        Returns:
            Созданный отчет с ID
        """
        pass

    @abstractmethod
    async def get_by_id(self, report_id: int) -> Optional[Report]:
        """
        Получить отчет по ID

        Args:
            report_id: ID отчета

        Returns:
            Отчет или None если не найден
        """
        pass

    @abstractmethod
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ReportStatus] = None,
        report_type: Optional[ReportType] = None
    ) -> List[Report]:
        """
        Получить список отчетов с фильтрацией

        Args:
            skip: Количество пропускаемых записей
            limit: Максимальное количество записей
            status: Фильтр по статусу
            report_type: Фильтр по типу отчета

        Returns:
            Список отчетов
        """
        pass

    @abstractmethod
    async def update(self, report: Report) -> Report:
        """
        Обновить отчет

        Args:
            report: Обновленная сущность отчета

        Returns:
            Обновленный отчет
        """
        pass

    @abstractmethod
    async def delete(self, report_id: int) -> bool:
        """
        Удалить отчет

        Args:
            report_id: ID отчета

        Returns:
            True если удален успешно
        """
        pass

    @abstractmethod
    async def count(
        self,
        status: Optional[ReportStatus] = None,
        report_type: Optional[ReportType] = None
    ) -> int:
        """
        Подсчитать количество отчетов

        Args:
            status: Фильтр по статусу
            report_type: Фильтр по типу отчета

        Returns:
            Количество отчетов
        """
        pass
