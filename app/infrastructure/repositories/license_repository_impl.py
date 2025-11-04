"""
License Repository Implementation
Реализация репозитория для лицензий
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.license_repository import ILicenseRepository
from app.domain.entities.license import License
from app.infrastructure.database.models.license import LicenseModel
from app.infrastructure.mappers.entity_mapper import EntityMapper
from app.infrastructure.repositories.base_repository import BaseRepository


class LicenseRepositoryImpl(BaseRepository[LicenseModel], ILicenseRepository):
    """Реализация репозитория для License"""

    def __init__(self, session: AsyncSession):
        super().__init__(LicenseModel, session)
        self.mapper = EntityMapper()

    async def get_by_id_with_relations(self, license_id: int) -> Optional[License]:
        """
        Получить лицензию по ID со всеми связанными данными

        Args:
            license_id: ID лицензии

        Returns:
            License со связями или None
        """
        query = (
            select(LicenseModel)
            .where(LicenseModel.id == license_id)
            .options(
                selectinload(LicenseModel.season),
                selectinload(LicenseModel.league)
            )
        )

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self.mapper.to_license_entity(model)
