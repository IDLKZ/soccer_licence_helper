"""
License Repository Interface
Интерфейс репозитория для лицензий
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.license import License


class ILicenseRepository(ABC):
    """Интерфейс репозитория для License"""

    @abstractmethod
    async def get_by_id_with_relations(self, license_id: int) -> Optional[License]:
        """
        Получить лицензию по ID со всеми связанными данными (season, league, etc.)

        Args:
            license_id: ID лицензии

        Returns:
            License со связями или None
        """
        pass
