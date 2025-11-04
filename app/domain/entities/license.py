"""
Domain entity for License
Бизнес-сущность лицензии - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from enum import Enum


class Language(str, Enum):
    """Поддерживаемые языки"""
    RU = "ru"
    KK = "kk"
    EN = "en"


@dataclass
class License:
    """
    Бизнес-сущность лицензии

    Attributes:
        id: Уникальный идентификатор
        season_id: ID сезона
        league_id: ID лиги
        title_ru: Название на русском
        title_kk: Название на казахском
        title_en: Название на английском
        description_ru: Описание на русском
        description_kk: Описание на казахском
        description_en: Описание на английском
        start_at: Дата начала действия лицензии
        end_at: Дата окончания действия лицензии
        is_active: Активна ли лицензия
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    title_ru: str
    title_kk: str
    start_at: date
    end_at: date
    id: Optional[int] = None
    season_id: Optional[int] = None
    league_id: Optional[int] = None
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_title(self, language: Language = Language.RU) -> str:
        """
        Получить название на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Название лицензии на указанном языке
        """
        if language == Language.RU:
            return self.title_ru
        elif language == Language.KK:
            return self.title_kk
        elif language == Language.EN:
            return self.title_en or self.title_ru
        return self.title_ru

    def get_description(self, language: Language = Language.RU) -> Optional[str]:
        """
        Получить описание на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Описание лицензии на указанном языке
        """
        if language == Language.RU:
            return self.description_ru
        elif language == Language.KK:
            return self.description_kk
        elif language == Language.EN:
            return self.description_en or self.description_ru
        return self.description_ru

    def is_valid_now(self) -> bool:
        """
        Проверить, действительна ли лицензия на текущий момент

        Returns:
            True если лицензия активна и даты действительны
        """
        if not self.is_active:
            return False

        today = date.today()
        return self.start_at <= today <= self.end_at

    def is_expired(self) -> bool:
        """
        Проверить, истекла ли лицензия

        Returns:
            True если текущая дата больше даты окончания
        """
        return date.today() > self.end_at

    def is_upcoming(self) -> bool:
        """
        Проверить, будет ли лицензия активирована в будущем

        Returns:
            True если дата начала еще не наступила
        """
        return date.today() < self.start_at

    def days_until_start(self) -> int:
        """
        Количество дней до начала действия лицензии

        Returns:
            Количество дней (отрицательное если уже началась)
        """
        return (self.start_at - date.today()).days

    def days_until_expiry(self) -> int:
        """
        Количество дней до истечения лицензии

        Returns:
            Количество дней (отрицательное если уже истекла)
        """
        return (self.end_at - date.today()).days

    def duration_days(self) -> int:
        """
        Общая продолжительность лицензии в днях

        Returns:
            Количество дней между началом и окончанием
        """
        return (self.end_at - self.start_at).days

    def activate(self) -> None:
        """Активировать лицензию"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивировать лицензию"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def extend_period(self, days: int) -> None:
        """
        Продлить период действия лицензии

        Args:
            days: Количество дней для продления
        """
        from datetime import timedelta
        self.end_at = self.end_at + timedelta(days=days)
        self.updated_at = datetime.utcnow()

    def update_dates(self, start_at: date, end_at: date) -> None:
        """
        Обновить даты действия лицензии

        Args:
            start_at: Новая дата начала
            end_at: Новая дата окончания

        Raises:
            ValueError: Если дата окончания раньше даты начала
        """
        if end_at < start_at:
            raise ValueError("End date cannot be earlier than start date")

        self.start_at = start_at
        self.end_at = end_at
        self.updated_at = datetime.utcnow()

    def update_translations(
        self,
        title_ru: Optional[str] = None,
        title_kk: Optional[str] = None,
        title_en: Optional[str] = None,
        description_ru: Optional[str] = None,
        description_kk: Optional[str] = None,
        description_en: Optional[str] = None
    ) -> None:
        """
        Обновить переводы лицензии

        Args:
            title_ru: Новое название на русском
            title_kk: Новое название на казахском
            title_en: Новое название на английском
            description_ru: Новое описание на русском
            description_kk: Новое описание на казахском
            description_en: Новое описание на английском
        """
        if title_ru is not None:
            self.title_ru = title_ru
        if title_kk is not None:
            self.title_kk = title_kk
        if title_en is not None:
            self.title_en = title_en
        if description_ru is not None:
            self.description_ru = description_ru
        if description_kk is not None:
            self.description_kk = description_kk
        if description_en is not None:
            self.description_en = description_en
        self.updated_at = datetime.utcnow()

    def is_expiring_soon(self, days_threshold: int = 30) -> bool:
        """
        Проверить, истекает ли лицензия в ближайшее время

        Args:
            days_threshold: Порог в днях (по умолчанию 30)

        Returns:
            True если лицензия истекает в течение указанного периода
        """
        if self.is_expired():
            return False

        days_left = self.days_until_expiry()
        return 0 <= days_left <= days_threshold

    def validate_dates(self) -> bool:
        """
        Валидация дат лицензии

        Returns:
            True если даты валидны
        """
        return self.end_at >= self.start_at

    def get_status(self) -> str:
        """
        Получить текущий статус лицензии

        Returns:
            Строка со статусом: active, expired, upcoming, inactive
        """
        if not self.is_active:
            return "inactive"
        if self.is_expired():
            return "expired"
        if self.is_upcoming():
            return "upcoming"
        return "active"
