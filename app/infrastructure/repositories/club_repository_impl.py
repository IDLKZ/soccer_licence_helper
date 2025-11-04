"""
Club Repository Implementation
Реализация репозитория для клубов
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.club_repository import IClubRepository
from app.domain.entities.club import Club
from app.infrastructure.database.models.club import ClubModel
from app.infrastructure.mappers.entity_mapper import EntityMapper
from app.infrastructure.repositories.base_repository import BaseRepository


class ClubRepositoryImpl(BaseRepository[ClubModel], IClubRepository):
    """Реализация репозитория для Club"""

    def __init__(self, session: AsyncSession):
        super().__init__(ClubModel, session)
        self.mapper = EntityMapper()

    async def get_by_id(self, club_id: int) -> Optional[Club]:
        """
        Получить клуб по ID

        Args:
            club_id: ID клуба

        Returns:
            Club или None
        """
        model = await super().get_by_id(club_id)
        if not model:
            return None
        return self.mapper.to_club_entity(model)
