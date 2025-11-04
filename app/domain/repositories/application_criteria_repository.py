"""
Application Criteria Repository Interface
Интерфейс репозитория для критериев заявки
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.application_criteria import ApplicationCriteria


class IApplicationCriteriaRepository(ABC):
    """Интерфейс репозитория для ApplicationCriteria"""

    @abstractmethod
    async def get_by_id_with_relations(self, criteria_id: int) -> Optional[ApplicationCriteria]:
        """
        Получить критерий по ID со всеми связанными данными
        (application, category, users, etc.)

        Args:
            criteria_id: ID критерия

        Returns:
            ApplicationCriteria со связями или None
        """
        pass
