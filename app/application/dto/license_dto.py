"""
Data Transfer Objects for License
DTO для передачи данных лицензии между слоями
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class CreateLicenseDTO:
    """DTO для создания лицензии"""
    title_ru: str
    title_kk: str
    start_at: date
    end_at: date
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    season_id: Optional[int] = None
    league_id: Optional[int] = None
    is_active: bool = True


@dataclass
class UpdateLicenseDTO:
    """DTO для обновления лицензии"""
    license_id: int
    title_ru: Optional[str] = None
    title_kk: Optional[str] = None
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    start_at: Optional[date] = None
    end_at: Optional[date] = None
    season_id: Optional[int] = None
    league_id: Optional[int] = None
    is_active: Optional[bool] = None


@dataclass
class UpdateLicenseDatesDTO:
    """DTO для обновления дат лицензии"""
    license_id: int
    start_at: date
    end_at: date


@dataclass
class ExtendLicenseDTO:
    """DTO для продления лицензии"""
    license_id: int
    days: int


@dataclass
class LicenseTranslationDTO:
    """DTO для переводов лицензии"""
    title_ru: str
    title_kk: str
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None


@dataclass
class LicenseDTO:
    """DTO для отображения лицензии"""
    id: int
    title_ru: str
    title_kk: str
    title_en: Optional[str]
    description_ru: Optional[str]
    description_kk: Optional[str]
    description_en: Optional[str]
    start_at: date
    end_at: date
    season_id: Optional[int]
    league_id: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    status: Optional[str] = None
    days_until_expiry: Optional[int] = None
    is_valid_now: Optional[bool] = None


@dataclass
class LicenseListDTO:
    """DTO для списка лицензий с пагинацией"""
    licenses: list[LicenseDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class LicenseWithRelationsDTO(LicenseDTO):
    """DTO лицензии с связанными сущностями"""
    season_name: Optional[str] = None
    league_name: Optional[str] = None
    total_users: Optional[int] = None


@dataclass
class LicenseShortDTO:
    """Краткая информация о лицензии"""
    id: int
    title_ru: str
    title_kk: str
    start_at: date
    end_at: date
    is_active: bool
    status: str


@dataclass
class LicenseStatsDTO:
    """DTO для статистики лицензии"""
    license_id: int
    total_users_assigned: int
    active_users: int
    total_reports_generated: int
    days_remaining: int
    is_expiring_soon: bool


@dataclass
class LicenseFilterDTO:
    """DTO для фильтрации лицензий"""
    season_id: Optional[int] = None
    league_id: Optional[int] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None  # active, expired, upcoming
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None
    end_date_from: Optional[date] = None
    end_date_to: Optional[date] = None
    search_query: Optional[str] = None  # Поиск по названию


@dataclass
class LicenseLocalizedDTO:
    """DTO для отображения лицензии на определенном языке"""
    id: int
    title: str
    description: Optional[str]
    start_at: date
    end_at: date
    is_active: bool
    status: str
    language: str  # ru, kk, en


@dataclass
class BulkActivateLicensesDTO:
    """DTO для массовой активации лицензий"""
    license_ids: list[int]


@dataclass
class BulkDeactivateLicensesDTO:
    """DTO для массовой деактивации лицензий"""
    license_ids: list[int]


@dataclass
class LicenseExpirationReportDTO:
    """DTO для отчета по истекающим лицензиям"""
    expiring_soon: list[LicenseShortDTO]  # Истекают в ближайшие дни
    expired: list[LicenseShortDTO]  # Уже истекли
    upcoming: list[LicenseShortDTO]  # Будущие лицензии
    threshold_days: int  # Порог для "истекает скоро"
