"""
Data Transfer Objects for League
DTO для передачи данных лиги между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CreateLeagueDTO:
    """DTO для создания лиги"""
    title_ru: str
    title_kk: str
    value: str
    level: int
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = False


@dataclass
class UpdateLeagueDTO:
    """DTO для обновления лиги"""
    league_id: int
    title_ru: Optional[str] = None
    title_kk: Optional[str] = None
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    value: Optional[str] = None
    level: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass
class UpdateLeagueLevelDTO:
    """DTO для обновления уровня лиги"""
    league_id: int
    level: int


@dataclass
class UpdateLeagueImageDTO:
    """DTO для обновления изображения лиги"""
    league_id: int
    image_url: str


@dataclass
class LeagueTranslationDTO:
    """DTO для переводов лиги"""
    title_ru: str
    title_kk: str
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None


@dataclass
class LeagueDTO:
    """DTO для отображения лиги"""
    id: int
    title_ru: str
    title_kk: str
    title_en: Optional[str]
    description_ru: Optional[str]
    description_kk: Optional[str]
    description_en: Optional[str]
    value: str
    level: int
    image_url: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    level_name: Optional[str] = None
    is_top_level: Optional[bool] = None
    has_image: Optional[bool] = None


@dataclass
class LeagueListDTO:
    """DTO для списка лиг с пагинацией"""
    leagues: list[LeagueDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class LeagueWithStatsDTO(LeagueDTO):
    """DTO лиги со статистикой"""
    total_licenses: Optional[int] = None
    active_licenses: Optional[int] = None
    total_teams: Optional[int] = None


@dataclass
class LeagueShortDTO:
    """Краткая информация о лиге"""
    id: int
    title_ru: str
    title_kk: str
    value: str
    level: int
    image_url: Optional[str]
    is_active: bool


@dataclass
class LeagueLocalizedDTO:
    """DTO для отображения лиги на определенном языке"""
    id: int
    title: str
    description: Optional[str]
    value: str
    level: int
    level_name: str
    image_url: Optional[str]
    is_active: bool
    language: str  # ru, kk, en


@dataclass
class ActivateLeagueDTO:
    """DTO для активации лиги"""
    league_id: int


@dataclass
class DeactivateLeagueDTO:
    """DTO для деактивации лиги"""
    league_id: int


@dataclass
class LeagueFilterDTO:
    """DTO для фильтрации лиг"""
    is_active: Optional[bool] = None
    level: Optional[int] = None
    min_level: Optional[int] = None
    max_level: Optional[int] = None
    search_query: Optional[str] = None  # Поиск по названию или value
    has_image: Optional[bool] = None


@dataclass
class LeaguesByLevelDTO:
    """DTO для группировки лиг по уровням"""
    level: int
    level_name: str
    leagues: list[LeagueShortDTO]
    count: int


@dataclass
class BulkActivateLeaguesDTO:
    """DTO для массовой активации лиг"""
    league_ids: list[int]


@dataclass
class BulkDeactivateLeaguesDTO:
    """DTO для массовой деактивации лиг"""
    league_ids: list[int]


@dataclass
class LeagueHierarchyDTO:
    """DTO для иерархической структуры лиг"""
    levels: list[LeaguesByLevelDTO]
    total_leagues: int
    total_levels: int


@dataclass
class ReorderLeaguesDTO:
    """DTO для переупорядочивания уровней лиг"""
    league_level_mapping: dict[int, int]  # {league_id: new_level}
