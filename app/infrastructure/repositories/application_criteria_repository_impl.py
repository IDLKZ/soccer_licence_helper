"""
Application Criteria Repository Implementation
Реализация репозитория для критериев заявки
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.application_criteria_repository import IApplicationCriteriaRepository
from app.domain.entities.application_criteria import ApplicationCriteria
from app.infrastructure.database.models.application_criteria import ApplicationCriteriaModel
from app.infrastructure.mappers.entity_mapper import EntityMapper
from app.infrastructure.repositories.base_repository import BaseRepository


class ApplicationCriteriaRepositoryImpl(
    BaseRepository[ApplicationCriteriaModel],
    IApplicationCriteriaRepository
):
    """Реализация репозитория для ApplicationCriteria"""

    def __init__(self, session: AsyncSession):
        super().__init__(ApplicationCriteriaModel, session)
        self.mapper = EntityMapper()

    async def get_by_id_with_relations(self, criteria_id: int) -> Optional[ApplicationCriteria]:
        """
        Получить критерий по ID со всеми связанными данными

        Args:
            criteria_id: ID критерия

        Returns:
            ApplicationCriteria со связями или None
        """
        query = (
            select(ApplicationCriteriaModel)
            .where(ApplicationCriteriaModel.id == criteria_id)
            .options(
                selectinload(ApplicationCriteriaModel.application),
                selectinload(ApplicationCriteriaModel.category),
                selectinload(ApplicationCriteriaModel.first_checked_user),
                selectinload(ApplicationCriteriaModel.checked_user),
                selectinload(ApplicationCriteriaModel.control_checked_user)
            )
        )

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self.mapper.to_application_criteria_entity(model)
