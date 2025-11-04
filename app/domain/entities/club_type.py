"""
Domain entity for ClubType
Бизнес-сущность типа клуба - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.entities.license import Language


@dataclass
class ClubType:
    """
    Бизнес-сущность типа клуба

    Attributes:
        id: Уникальный идентификатор
        title_ru: Название на русском
        title_kk: Название на казахском
        title_en: Название на английском
        description_ru: Описание на русском
        description_kk: Описание на казахском
        description_en: Описание на английском
        value: Уникальное значение (например, "football_club", "academy")
        is_active: Активен ли тип
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    title_ru: str
    title_kk: str
    value: str
    id: Optional[int] = None
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
            Название типа клуба на указанном языке
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
            Описание типа клуба на указанном языке
        """
        if language == Language.RU:
            return self.description_ru
        elif language == Language.KK:
            return self.description_kk
        elif language == Language.EN:
            return self.description_en or self.description_ru
        return self.description_ru

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
        Обновить переводы типа клуба

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

    def activate(self) -> None:
        """Активировать тип клуба"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивировать тип клуба"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def validate(self) -> tuple[bool, str]:
        """
        Валидация типа клуба

        Returns:
            Tuple (валидность, сообщение об ошибке)
        """
        if not self.title_ru or not self.title_ru.strip():
            return False, "Title in Russian is required"

        if not self.title_kk or not self.title_kk.strip():
            return False, "Title in Kazakh is required"

        if not self.value or not self.value.strip():
            return False, "Value is required"

        return True, ""
