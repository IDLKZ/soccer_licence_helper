"""
Club Repository Interface
Интерфейс репозитория для клубов
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.club import Club


class IClubRepository(ABC):
    """Интерфейс репозитория для Club"""

    @abstractmethod
    async def get_by_id(self, club_id: int) -> Optional[Club]:
        """
        Получить клуб по ID

        Args:
            club_id: ID клуба

        Returns:
            Club или None если не найден
        """
        pass
