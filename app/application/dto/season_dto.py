"""
Data Transfer Objects for Season
DTO для передачи данных сезона между слоями
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class CreateSeasonDTO:
    """DTO для создания сезона"""
    title_ru: str
    title_kk: str
    value: str
    start: date
    end: date
    title_en: Optional[str] = None
    is_active: bool = False


@dataclass
class UpdateSeasonDTO:
    """DTO для обновления сезона"""
    season_id: int
    title_ru: Optional[str] = None
    title_kk: Optional[str] = None
    title_en: Optional[str] = None
    value: Optional[str] = None
    start: Optional[date] = None
    end: Optional[date] = None
    is_active: Optional[bool] = None


@dataclass
class UpdateSeasonDatesDTO:
    """DTO для обновления дат сезона"""
    season_id: int
    start: date
    end: date


@dataclass
class SeasonTranslationDTO:
    """DTO для переводов сезона"""
    title_ru: str
    title_kk: str
    title_en: Optional[str] = None


@dataclass
class SeasonDTO:
    """DTO для отображения сезона"""
    id: int
    title_ru: str
    title_kk: str
    title_en: Optional[str]
    value: str
    start: date
    end: date
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    status: Optional[str] = None  # current, past, future
    days_remaining: Optional[int] = None
    is_current: Optional[bool] = None


@dataclass
class SeasonListDTO:
    """DTO для списка сезонов с пагинацией"""
    seasons: list[SeasonDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class SeasonWithStatsDTO(SeasonDTO):
    """DTO сезона со статистикой"""
    total_licenses: Optional[int] = None
    active_licenses: Optional[int] = None
    total_leagues: Optional[int] = None


@dataclass
class SeasonShortDTO:
    """Краткая информация о сезоне"""
    id: int
    title_ru: str
    title_kk: str
    value: str
    start: date
    end: date
    is_active: bool
    status: str


@dataclass
class SeasonLocalizedDTO:
    """DTO для отображения сезона на определенном языке"""
    id: int
    title: str
    value: str
    start: date
    end: date
    is_active: bool
    status: str
    language: str  # ru, kk, en


@dataclass
class ActivateSeasonDTO:
    """DTO для активации сезона"""
    season_id: int


@dataclass
class DeactivateSeasonDTO:
    """DTO для деактивации сезона"""
    season_id: int


@dataclass
class SeasonFilterDTO:
    """DTO для фильтрации сезонов"""
    is_active: Optional[bool] = None
    status: Optional[str] = None  # current, past, future
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None
    end_date_from: Optional[date] = None
    end_date_to: Optional[date] = None
    search_query: Optional[str] = None  # Поиск по названию или value


@dataclass
class SeasonOverlapCheckDTO:
    """DTO для проверки пересечения сезонов"""
    start: date
    end: date
    exclude_season_id: Optional[int] = None  # Исключить этот сезон из проверки


@dataclass
class BulkActivateSeasonsDTO:
    """DTO для массовой активации сезонов"""
    season_ids: list[int]


@dataclass
class BulkDeactivateSeasonsDTO:
    """DTO для массовой деактивации сезонов"""
    season_ids: list[int]


@dataclass
class CurrentSeasonDTO:
    """DTO для текущего активного сезона"""
    season: Optional[SeasonDTO]
    has_current: bool
    message: str
