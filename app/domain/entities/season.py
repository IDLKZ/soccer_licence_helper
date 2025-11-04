"""
Domain entity for Season
Бизнес-сущность сезона - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional
from app.domain.entities.license import Language


@dataclass
class Season:
    """
    Бизнес-сущность сезона

    Attributes:
        id: Уникальный идентификатор
        title_ru: Название на русском
        title_kk: Название на казахском
        title_en: Название на английском
        value: Уникальное значение (например, "2023-2024")
        start: Дата начала сезона
        end: Дата окончания сезона
        is_active: Активен ли сезон
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    title_ru: str
    title_kk: str
    value: str
    start: date
    end: date
    id: Optional[int] = None
    title_en: Optional[str] = None
    is_active: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_title(self, language: Language = Language.RU) -> str:
        """
        Получить название на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Название сезона на указанном языке
        """
        if language == Language.RU:
            return self.title_ru
        elif language == Language.KK:
            return self.title_kk
        elif language == Language.EN:
            return self.title_en or self.title_ru
        return self.title_ru

    def is_current(self) -> bool:
        """
        Проверить, является ли сезон текущим

        Returns:
            True если текущая дата находится в диапазоне сезона
        """
        today = date.today()
        return self.start <= today <= self.end

    def is_past(self) -> bool:
        """
        Проверить, завершен ли сезон

        Returns:
            True если текущая дата больше даты окончания
        """
        return date.today() > self.end

    def is_future(self) -> bool:
        """
        Проверить, будет ли сезон в будущем

        Returns:
            True если дата начала еще не наступила
        """
        return date.today() < self.start

    def days_until_start(self) -> int:
        """
        Количество дней до начала сезона

        Returns:
            Количество дней (отрицательное если уже начался)
        """
        return (self.start - date.today()).days

    def days_until_end(self) -> int:
        """
        Количество дней до окончания сезона

        Returns:
            Количество дней (отрицательное если уже закончился)
        """
        return (self.end - date.today()).days

    def duration_days(self) -> int:
        """
        Общая продолжительность сезона в днях

        Returns:
            Количество дней между началом и окончанием
        """
        return (self.end - self.start).days

    def activate(self) -> None:
        """Активировать сезон"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивировать сезон"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def update_dates(self, start: date, end: date) -> None:
        """
        Обновить даты сезона

        Args:
            start: Новая дата начала
            end: Новая дата окончания

        Raises:
            ValueError: Если дата окончания раньше даты начала
        """
        if end < start:
            raise ValueError("End date cannot be earlier than start date")

        self.start = start
        self.end = end
        self.updated_at = datetime.utcnow()

    def update_translations(
        self,
        title_ru: Optional[str] = None,
        title_kk: Optional[str] = None,
        title_en: Optional[str] = None
    ) -> None:
        """
        Обновить переводы сезона

        Args:
            title_ru: Новое название на русском
            title_kk: Новое название на казахском
            title_en: Новое название на английском
        """
        if title_ru is not None:
            self.title_ru = title_ru
        if title_kk is not None:
            self.title_kk = title_kk
        if title_en is not None:
            self.title_en = title_en
        self.updated_at = datetime.utcnow()

    def validate_dates(self) -> bool:
        """
        Валидация дат сезона

        Returns:
            True если даты валидны
        """
        return self.end >= self.start

    def get_status(self) -> str:
        """
        Получить текущий статус сезона

        Returns:
            Строка со статусом: current, past, future, inactive
        """
        if not self.is_active:
            return "inactive"
        if self.is_past():
            return "past"
        if self.is_future():
            return "future"
        return "current"

    def overlaps_with(self, other_start: date, other_end: date) -> bool:
        """
        Проверить, пересекается ли этот сезон с другим периодом

        Args:
            other_start: Начало другого периода
            other_end: Конец другого периода

        Returns:
            True если периоды пересекаются
        """
        return not (self.end < other_start or self.start > other_end)

    def contains_date(self, check_date: date) -> bool:
        """
        Проверить, содержится ли дата в диапазоне сезона

        Args:
            check_date: Дата для проверки

        Returns:
            True если дата находится в диапазоне сезона
        """
        return self.start <= check_date <= self.end
