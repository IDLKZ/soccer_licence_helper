"""
Application Report Repository Interface
Интерфейс репозитория для отчетов о заявках
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.application_report import ApplicationReport


class IApplicationReportRepository(ABC):
    """Интерфейс репозитория для ApplicationReport"""

    @abstractmethod
    async def get_by_id(self, report_id: int) -> Optional[ApplicationReport]:
        """
        Получить отчет по ID

        Args:
            report_id: ID отчета

        Returns:
            ApplicationReport или None если не найден
        """
        pass

    @abstractmethod
    async def get_by_id_with_relations(self, report_id: int) -> Optional[ApplicationReport]:
        """
        Получить отчет по ID со всеми связанными данными

        Args:
            report_id: ID отчета

        Returns:
            ApplicationReport со связями или None
        """
        pass
