"""
Category Document Repository Interface
Интерфейс репозитория для категорий документов
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.category_document import CategoryDocument


class ICategoryDocumentRepository(ABC):
    """Интерфейс репозитория для CategoryDocument"""

    @abstractmethod
    async def get_by_id(self, category_id: int) -> Optional[CategoryDocument]:
        """
        Получить категорию документов по ID

        Args:
            category_id: ID категории

        Returns:
            CategoryDocument или None если не найден
        """
        pass
