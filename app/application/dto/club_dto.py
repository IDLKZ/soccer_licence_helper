"""
Data Transfer Objects for Club
DTO для передачи данных клуба между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class ClubDTO:
    """DTO для отображения клуба"""
    id: int
    image_url: Optional[str]
    parent_id: Optional[int]
    type_id: Optional[int]
    full_name_ru: str
    full_name_kk: str
    full_name_en: Optional[str]
    short_name_ru: str
    short_name_kk: str
    short_name_en: Optional[str]
    description_ru: Optional[str]
    description_kk: Optional[str]
    description_en: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    has_parent: Optional[bool] = None
    is_root: Optional[bool] = None
    has_image: Optional[bool] = None


@dataclass
class ClubWithRelationsDTO(ClubDTO):
    """DTO клуба с связанными данными"""
    parent_full_name: Optional[str] = None
    parent_short_name: Optional[str] = None
    type_title: Optional[str] = None
    children_count: Optional[int] = None


@dataclass
class ClubShortDTO:
    """Краткая информация о клубе"""
    id: int
    short_name_ru: str
    short_name_kk: str
    image_url: Optional[str]
    is_active: bool


@dataclass
class ClubLocalizedDTO:
    """DTO для отображения клуба на определенном языке"""
    id: int
    full_name: str
    short_name: str
    description: Optional[str]
    image_url: Optional[str]
    is_active: bool
    language: str  # ru, kk, en


@dataclass
class ClubHierarchyNodeDTO:
    """DTO для узла иерархии клубов"""
    id: int
    full_name_ru: str
    short_name_ru: str
    parent_id: Optional[int]
    children: Optional[List['ClubHierarchyNodeDTO']] = None


@dataclass
class ClubsByTypeDTO:
    """DTO для группировки клубов по типу"""
    type_id: int
    type_title: str
    clubs: List[ClubShortDTO]
    count: int
