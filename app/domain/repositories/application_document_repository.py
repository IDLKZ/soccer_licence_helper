"""
Application Document Repository Interface
Интерфейс репозитория для документов заявки
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities.application_document import ApplicationDocument


class IApplicationDocumentRepository(ABC):
    """Интерфейс репозитория для ApplicationDocument"""

    @abstractmethod
    async def get_by_application_and_category(
        self,
        application_id: int,
        category_id: int
    ) -> List[ApplicationDocument]:
        """
        Получить все документы заявки для определенной категории

        Args:
            application_id: ID заявки
            category_id: ID категории документов

        Returns:
            Список ApplicationDocument со связанными данными
        """
        pass
