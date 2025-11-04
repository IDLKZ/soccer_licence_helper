"""
Category Document Repository Implementation
Реализация репозитория для категорий документов
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.category_document_repository import ICategoryDocumentRepository
from app.domain.entities.category_document import CategoryDocument
from app.infrastructure.database.models.category_document import CategoryDocumentModel
from app.infrastructure.mappers.entity_mapper import EntityMapper
from app.infrastructure.repositories.base_repository import BaseRepository


class CategoryDocumentRepositoryImpl(
    BaseRepository[CategoryDocumentModel],
    ICategoryDocumentRepository
):
    """Реализация репозитория для CategoryDocument"""

    def __init__(self, session: AsyncSession):
        super().__init__(CategoryDocumentModel, session)
        self.mapper = EntityMapper()

    async def get_by_id(self, category_id: int) -> Optional[CategoryDocument]:
        """
        Получить категорию документов по ID

        Args:
            category_id: ID категории

        Returns:
            CategoryDocument или None
        """
        model = await super().get_by_id(category_id)
        if not model:
            return None
        return self.mapper.to_category_document_entity(model)
