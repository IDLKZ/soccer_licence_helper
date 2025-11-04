"""
Domain entity for CategoryDocument
Бизнес-сущность категории документов - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from app.domain.entities.license import Language


@dataclass
class CategoryDocument:
    """
    Бизнес-сущность категории документов

    Attributes:
        id: Уникальный идентификатор
        title_ru: Название на русском
        title_kk: Название на казахском
        title_en: Название на английском
        value: Уникальное значение (например, "financial_reports")
        level: Уровень категории в иерархии (1 - корневой, 2+ - подкатегории)
        roles: Список ID ролей, имеющих доступ к этой категории
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    title_ru: str
    title_kk: str
    value: str
    level: int
    id: Optional[int] = None
    title_en: Optional[str] = None
    roles: Optional[List[int]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Инициализация значений по умолчанию"""
        if self.roles is None:
            self.roles = []

    def get_title(self, language: Language = Language.RU) -> str:
        """
        Получить название на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Название категории на указанном языке
        """
        if language == Language.RU:
            return self.title_ru
        elif language == Language.KK:
            return self.title_kk
        elif language == Language.EN:
            return self.title_en or self.title_ru
        return self.title_ru

    def update_translations(
        self,
        title_ru: Optional[str] = None,
        title_kk: Optional[str] = None,
        title_en: Optional[str] = None
    ) -> None:
        """
        Обновить переводы категории

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

    def update_level(self, new_level: int) -> None:
        """
        Обновить уровень категории

        Args:
            new_level: Новый уровень категории

        Raises:
            ValueError: Если уровень меньше 1
        """
        if new_level < 1:
            raise ValueError("Category level must be at least 1")

        self.level = new_level
        self.updated_at = datetime.utcnow()

    def is_root_level(self) -> bool:
        """
        Проверить, является ли категория корневой

        Returns:
            True если level == 1
        """
        return self.level == 1

    def is_subcategory(self) -> bool:
        """
        Проверить, является ли категория подкатегорией

        Returns:
            True если level > 1
        """
        return self.level > 1

    def add_role(self, role_id: int) -> None:
        """
        Добавить роль к категории

        Args:
            role_id: ID роли для добавления
        """
        if self.roles is None:
            self.roles = []

        if role_id not in self.roles:
            self.roles.append(role_id)
            self.updated_at = datetime.utcnow()

    def remove_role(self, role_id: int) -> None:
        """
        Удалить роль из категории

        Args:
            role_id: ID роли для удаления
        """
        if self.roles and role_id in self.roles:
            self.roles.remove(role_id)
            self.updated_at = datetime.utcnow()

    def has_role(self, role_id: int) -> bool:
        """
        Проверить, есть ли роль у категории

        Args:
            role_id: ID роли для проверки

        Returns:
            True если роль присутствует
        """
        return self.roles is not None and role_id in self.roles

    def set_roles(self, role_ids: List[int]) -> None:
        """
        Установить список ролей для категории

        Args:
            role_ids: Список ID ролей
        """
        self.roles = role_ids if role_ids else []
        self.updated_at = datetime.utcnow()

    def clear_roles(self) -> None:
        """Очистить все роли категории"""
        self.roles = []
        self.updated_at = datetime.utcnow()

    def has_any_roles(self) -> bool:
        """
        Проверить, есть ли у категории роли

        Returns:
            True если есть хотя бы одна роль
        """
        return bool(self.roles)

    def get_roles_count(self) -> int:
        """
        Получить количество ролей

        Returns:
            Количество ролей в категории
        """
        return len(self.roles) if self.roles else 0

    def is_accessible_by_role(self, role_id: int) -> bool:
        """
        Проверить, доступна ли категория для указанной роли

        Args:
            role_id: ID роли для проверки

        Returns:
            True если роль имеет доступ (или если roles пустой - доступ всем)
        """
        # Если roles пустой или None, доступ есть у всех
        if not self.roles:
            return True

        return role_id in self.roles

    def validate_level(self) -> bool:
        """
        Валидация уровня категории

        Returns:
            True если уровень валиден (>= 1)
        """
        return self.level >= 1

    def get_depth_level_name(self, language: Language = Language.RU) -> str:
        """
        Получить человекочитаемое название уровня глубины

        Args:
            language: Язык

        Returns:
            Название уровня
        """
        level_names = {
            Language.RU: {
                1: "Корневая категория",
                2: "Подкатегория 1-го уровня",
                3: "Подкатегория 2-го уровня",
                4: "Подкатегория 3-го уровня"
            },
            Language.KK: {
                1: "Түбірлік санат",
                2: "1-деңгейлі санат",
                3: "2-деңгейлі санат",
                4: "3-деңгейлі санат"
            },
            Language.EN: {
                1: "Root Category",
                2: "Subcategory Level 1",
                3: "Subcategory Level 2",
                4: "Subcategory Level 3"
            }
        }

        lang_dict = level_names.get(language, level_names[Language.RU])
        return lang_dict.get(
            self.level,
            f"Подкатегория {self.level-1}-го уровня" if language == Language.RU else f"Subcategory Level {self.level-1}"
        )
