"""
User Repository Interface
Интерфейс репозитория для пользователей
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User


class IUserRepository(ABC):
    """Интерфейс репозитория для User"""

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Получить пользователя по ID

        Args:
            user_id: ID пользователя

        Returns:
            User или None если не найден
        """
        pass
