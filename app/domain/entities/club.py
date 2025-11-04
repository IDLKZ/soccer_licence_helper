"""
Domain entity for Club
Бизнес-сущность клуба - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.entities.license import Language


@dataclass
class Club:
    """
    Бизнес-сущность клуба

    Attributes:
        id: Уникальный идентификатор
        image_url: URL изображения/логотипа клуба
        parent_id: ID родительского клуба (для иерархии)
        type_id: ID типа клуба
        full_name_ru: Полное название на русском
        full_name_kk: Полное название на казахском
        full_name_en: Полное название на английском
        short_name_ru: Краткое название на русском
        short_name_kk: Краткое название на казахском
        short_name_en: Краткое название на английском
        description_ru: Описание на русском
        description_kk: Описание на казахском
        description_en: Описание на английском
        is_active: Активен ли клуб
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    full_name_ru: str
    full_name_kk: str
    short_name_ru: str
    short_name_kk: str
    id: Optional[int] = None
    image_url: Optional[str] = None
    parent_id: Optional[int] = None
    type_id: Optional[int] = None
    full_name_en: Optional[str] = None
    short_name_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_full_name(self, language: Language = Language.RU) -> str:
        """
        Получить полное название на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Полное название клуба на указанном языке
        """
        if language == Language.RU:
            return self.full_name_ru
        elif language == Language.KK:
            return self.full_name_kk
        elif language == Language.EN:
            return self.full_name_en or self.full_name_ru
        return self.full_name_ru

    def get_short_name(self, language: Language = Language.RU) -> str:
        """
        Получить краткое название на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Краткое название клуба на указанном языке
        """
        if language == Language.RU:
            return self.short_name_ru
        elif language == Language.KK:
            return self.short_name_kk
        elif language == Language.EN:
            return self.short_name_en or self.short_name_ru
        return self.short_name_ru

    def get_description(self, language: Language = Language.RU) -> Optional[str]:
        """
        Получить описание на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Описание клуба на указанном языке
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
        full_name_ru: Optional[str] = None,
        full_name_kk: Optional[str] = None,
        full_name_en: Optional[str] = None,
        short_name_ru: Optional[str] = None,
        short_name_kk: Optional[str] = None,
        short_name_en: Optional[str] = None,
        description_ru: Optional[str] = None,
        description_kk: Optional[str] = None,
        description_en: Optional[str] = None
    ) -> None:
        """
        Обновить переводы клуба

        Args:
            full_name_ru: Новое полное название на русском
            full_name_kk: Новое полное название на казахском
            full_name_en: Новое полное название на английском
            short_name_ru: Новое краткое название на русском
            short_name_kk: Новое краткое название на казахском
            short_name_en: Новое краткое название на английском
            description_ru: Новое описание на русском
            description_kk: Новое описание на казахском
            description_en: Новое описание на английском
        """
        if full_name_ru is not None:
            self.full_name_ru = full_name_ru
        if full_name_kk is not None:
            self.full_name_kk = full_name_kk
        if full_name_en is not None:
            self.full_name_en = full_name_en
        if short_name_ru is not None:
            self.short_name_ru = short_name_ru
        if short_name_kk is not None:
            self.short_name_kk = short_name_kk
        if short_name_en is not None:
            self.short_name_en = short_name_en
        if description_ru is not None:
            self.description_ru = description_ru
        if description_kk is not None:
            self.description_kk = description_kk
        if description_en is not None:
            self.description_en = description_en
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Активировать клуб"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивировать клуб"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def has_parent(self) -> bool:
        """
        Проверить, есть ли родительский клуб

        Returns:
            True если есть родительский клуб
        """
        return self.parent_id is not None

    def is_root_club(self) -> bool:
        """
        Проверить, является ли клуб корневым (без родителя)

        Returns:
            True если это корневой клуб
        """
        return self.parent_id is None

    def set_parent(self, parent_id: Optional[int]) -> None:
        """
        Установить родительский клуб

        Args:
            parent_id: ID родительского клуба

        Raises:
            ValueError: Если пытаемся установить сам клуб как родителя
        """
        if parent_id == self.id:
            raise ValueError("Club cannot be its own parent")

        self.parent_id = parent_id
        self.updated_at = datetime.utcnow()

    def remove_parent(self) -> None:
        """Убрать родительский клуб (сделать корневым)"""
        self.parent_id = None
        self.updated_at = datetime.utcnow()

    def set_type(self, type_id: int) -> None:
        """
        Установить тип клуба

        Args:
            type_id: ID типа клуба
        """
        self.type_id = type_id
        self.updated_at = datetime.utcnow()

    def update_image(self, image_url: str) -> None:
        """
        Обновить изображение клуба

        Args:
            image_url: Новый URL изображения
        """
        self.image_url = image_url
        self.updated_at = datetime.utcnow()

    def has_image(self) -> bool:
        """
        Проверить, есть ли изображение у клуба

        Returns:
            True если image_url не пустой
        """
        return bool(self.image_url)

    def validate(self) -> tuple[bool, str]:
        """
        Валидация клуба

        Returns:
            Tuple (валидность, сообщение об ошибке)
        """
        if not self.full_name_ru or not self.full_name_ru.strip():
            return False, "Full name in Russian is required"

        if not self.full_name_kk or not self.full_name_kk.strip():
            return False, "Full name in Kazakh is required"

        if not self.short_name_ru or not self.short_name_ru.strip():
            return False, "Short name in Russian is required"

        if not self.short_name_kk or not self.short_name_kk.strip():
            return False, "Short name in Kazakh is required"

        # Проверка на циклическую ссылку
        if self.id and self.parent_id == self.id:
            return False, "Club cannot be its own parent"

        return True, ""

    def get_hierarchy_level(self) -> int:
        """
        Получить уровень в иерархии

        Returns:
            0 для корневого клуба, 1+ для дочерних
            (требует загрузку родителей для точного расчета)
        """
        if self.is_root_club():
            return 0
        return 1  # Упрощенно, для точного расчета нужна вся цепочка родителей
