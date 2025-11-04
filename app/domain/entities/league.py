"""
Domain entity for League
Бизнес-сущность лиги - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.entities.license import Language


@dataclass
class League:
    """
    Бизнес-сущность лиги

    Attributes:
        id: Уникальный идентификатор
        title_ru: Название на русском
        title_kk: Название на казахском
        title_en: Название на английском
        description_ru: Описание на русском
        description_kk: Описание на казахском
        description_en: Описание на английском
        value: Уникальное значение (например, "premier_league")
        image_url: URL изображения лиги
        level: Уровень лиги (например, 1 - высшая лига, 2 - первая лига и т.д.)
        is_active: Активна ли лига
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    title_ru: str
    title_kk: str
    value: str
    level: int
    id: Optional[int] = None
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_title(self, language: Language = Language.RU) -> str:
        """
        Получить название на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Название лиги на указанном языке
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
            Описание лиги на указанном языке
        """
        if language == Language.RU:
            return self.description_ru
        elif language == Language.KK:
            return self.description_kk
        elif language == Language.EN:
            return self.description_en or self.description_ru
        return self.description_ru

    def activate(self) -> None:
        """Активировать лигу"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивировать лигу"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def update_level(self, new_level: int) -> None:
        """
        Обновить уровень лиги

        Args:
            new_level: Новый уровень лиги

        Raises:
            ValueError: Если уровень меньше 1
        """
        if new_level < 1:
            raise ValueError("League level must be at least 1")

        self.level = new_level
        self.updated_at = datetime.utcnow()

    def update_image(self, image_url: str) -> None:
        """
        Обновить изображение лиги

        Args:
            image_url: Новый URL изображения
        """
        self.image_url = image_url
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
        Обновить переводы лиги

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

    def is_top_level(self) -> bool:
        """
        Проверить, является ли лига высшей

        Returns:
            True если level == 1
        """
        return self.level == 1

    def is_lower_than(self, other_level: int) -> bool:
        """
        Проверить, ниже ли эта лига по уровню

        Args:
            other_level: Уровень для сравнения

        Returns:
            True если уровень этой лиги больше (ниже по иерархии)
        """
        return self.level > other_level

    def is_higher_than(self, other_level: int) -> bool:
        """
        Проверить, выше ли эта лига по уровню

        Args:
            other_level: Уровень для сравнения

        Returns:
            True если уровень этой лиги меньше (выше по иерархии)
        """
        return self.level < other_level

    def get_level_name(self, language: Language = Language.RU) -> str:
        """
        Получить человекочитаемое название уровня

        Args:
            language: Язык

        Returns:
            Название уровня
        """
        level_names = {
            Language.RU: {
                1: "Высшая лига",
                2: "Первая лига",
                3: "Вторая лига",
                4: "Третья лига"
            },
            Language.KK: {
                1: "Жоғары лига",
                2: "Бірінші лига",
                3: "Екінші лига",
                4: "Үшінші лига"
            },
            Language.EN: {
                1: "Premier League",
                2: "First League",
                3: "Second League",
                4: "Third League"
            }
        }

        lang_dict = level_names.get(language, level_names[Language.RU])
        return lang_dict.get(self.level, f"{self.level}-я лига" if language == Language.RU else f"League {self.level}")

    def validate_level(self) -> bool:
        """
        Валидация уровня лиги

        Returns:
            True если уровень валиден (>= 1)
        """
        return self.level >= 1

    def has_image(self) -> bool:
        """
        Проверить, есть ли изображение у лиги

        Returns:
            True если image_url не пустой
        """
        return bool(self.image_url)
