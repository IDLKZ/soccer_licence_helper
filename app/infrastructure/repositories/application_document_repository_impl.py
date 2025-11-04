"""
Application Document Repository Implementation
Реализация репозитория для документов заявки
"""
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.application_document_repository import IApplicationDocumentRepository
from app.domain.entities.application_document import ApplicationDocument
from app.infrastructure.database.models.application_document import ApplicationDocumentModel
from app.infrastructure.mappers.entity_mapper import EntityMapper
from app.infrastructure.repositories.base_repository import BaseRepository


class ApplicationDocumentRepositoryImpl(
    BaseRepository[ApplicationDocumentModel],
    IApplicationDocumentRepository
):
    """Реализация репозитория для ApplicationDocument"""

    def __init__(self, session: AsyncSession):
        super().__init__(ApplicationDocumentModel, session)
        self.mapper = EntityMapper()

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
            Список ApplicationDocument
        """
        query = (
            select(ApplicationDocumentModel)
            .where(
                ApplicationDocumentModel.application_id == application_id,
                ApplicationDocumentModel.category_id == category_id
            )
            .options(
                selectinload(ApplicationDocumentModel.document),
                selectinload(ApplicationDocumentModel.category)
            )
        )

        result = await self.session.execute(query)
        models = result.scalars().all()

        return [self.mapper.to_application_document_entity(model) for model in models]
