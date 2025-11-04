"""
Data Transfer Objects for ClubType
DTO для передачи данных типа клуба между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class ClubTypeDTO:
    """DTO для отображения типа клуба"""
    id: int
    title_ru: str
    title_kk: str
    title_en: Optional[str]
    description_ru: Optional[str]
    description_kk: Optional[str]
    description_en: Optional[str]
    value: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class ClubTypeShortDTO:
    """Краткая информация о типе клуба"""
    id: int
    title_ru: str
    title_kk: str
    value: str
    is_active: bool


@dataclass
class ClubTypeLocalizedDTO:
    """DTO для отображения типа клуба на определенном языке"""
    id: int
    title: str
    description: Optional[str]
    value: str
    is_active: bool
    language: str  # ru, kk, en
