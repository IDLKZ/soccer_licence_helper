"""
User Repository Implementation
Реализация репозитория для пользователей
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.user_repository import IUserRepository
from app.domain.entities.user import User
from app.infrastructure.database.models.user import UserModel
from app.infrastructure.mappers.entity_mapper import EntityMapper
from app.infrastructure.repositories.base_repository import BaseRepository


class UserRepositoryImpl(BaseRepository[UserModel], IUserRepository):
    """Реализация репозитория для User"""

    def __init__(self, session: AsyncSession):
        super().__init__(UserModel, session)
        self.mapper = EntityMapper()

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Получить пользователя по ID

        Args:
            user_id: ID пользователя

        Returns:
            User или None
        """
        model = await super().get_by_id(user_id)
        if not model:
            return None
        return self.mapper.to_user_entity(model)
