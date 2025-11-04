"""
Domain entity for ApplicationStatusCategory
Бизнес-сущность категории статуса заявки - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from app.domain.entities.license import Language


@dataclass
class ApplicationStatusCategory:
    """
    Бизнес-сущность категории статуса заявки

    Attributes:
        id: Уникальный идентификатор
        cat_previous_id: ID предыдущей категории в workflow
        cat_next_id: ID следующей категории в workflow
        title_ru: Название на русском
        title_kk: Название на казахском
        title_en: Название на английском
        description_ru: Описание на русском
        description_kk: Описание на казахском
        description_en: Описание на английском
        value: Уникальное значение (например, "draft", "submitted")
        role_values: Список значений ролей, имеющих доступ
        is_active: Активна ли категория
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    title_ru: str
    title_kk: str
    value: str
    id: Optional[int] = None
    cat_previous_id: Optional[int] = None
    cat_next_id: Optional[int] = None
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    role_values: Optional[List[str]] = None
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Инициализация значений по умолчанию"""
        if self.role_values is None:
            self.role_values = []

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

    def get_description(self, language: Language = Language.RU) -> Optional[str]:
        """
        Получить описание на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Описание категории на указанном языке
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
        Обновить переводы категории

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

    def set_previous_category(self, category_id: Optional[int]) -> None:
        """
        Установить предыдущую категорию в workflow

        Args:
            category_id: ID предыдущей категории
        """
        self.cat_previous_id = category_id
        self.updated_at = datetime.utcnow()

    def set_next_category(self, category_id: Optional[int]) -> None:
        """
        Установить следующую категорию в workflow

        Args:
            category_id: ID следующей категории
        """
        self.cat_next_id = category_id
        self.updated_at = datetime.utcnow()

    def has_previous(self) -> bool:
        """
        Проверить, есть ли предыдущая категория

        Returns:
            True если есть предыдущая категория
        """
        return self.cat_previous_id is not None

    def has_next(self) -> bool:
        """
        Проверить, есть ли следующая категория

        Returns:
            True если есть следующая категория
        """
        return self.cat_next_id is not None

    def is_first_in_workflow(self) -> bool:
        """
        Проверить, является ли категория первой в workflow

        Returns:
            True если это начальная категория
        """
        return self.cat_previous_id is None

    def is_last_in_workflow(self) -> bool:
        """
        Проверить, является ли категория последней в workflow

        Returns:
            True если это финальная категория
        """
        return self.cat_next_id is None

    def activate(self) -> None:
        """Активировать категорию"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивировать категорию"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def add_role(self, role_value: str) -> None:
        """
        Добавить роль к категории

        Args:
            role_value: Значение роли для добавления
        """
        if self.role_values is None:
            self.role_values = []

        if role_value not in self.role_values:
            self.role_values.append(role_value)
            self.updated_at = datetime.utcnow()

    def remove_role(self, role_value: str) -> None:
        """
        Удалить роль из категории

        Args:
            role_value: Значение роли для удаления
        """
        if self.role_values and role_value in self.role_values:
            self.role_values.remove(role_value)
            self.updated_at = datetime.utcnow()

    def has_role(self, role_value: str) -> bool:
        """
        Проверить, есть ли роль у категории

        Args:
            role_value: Значение роли для проверки

        Returns:
            True если роль присутствует
        """
        return self.role_values is not None and role_value in self.role_values

    def set_roles(self, role_values: List[str]) -> None:
        """
        Установить список ролей для категории

        Args:
            role_values: Список значений ролей
        """
        self.role_values = role_values if role_values else []
        self.updated_at = datetime.utcnow()

    def clear_roles(self) -> None:
        """Очистить все роли категории"""
        self.role_values = []
        self.updated_at = datetime.utcnow()

    def has_any_roles(self) -> bool:
        """
        Проверить, есть ли у категории роли

        Returns:
            True если есть хотя бы одна роль
        """
        return bool(self.role_values)

    def get_roles_count(self) -> int:
        """
        Получить количество ролей

        Returns:
            Количество ролей в категории
        """
        return len(self.role_values) if self.role_values else 0

    def is_accessible_by_role(self, role_value: str) -> bool:
        """
        Проверить, доступна ли категория для указанной роли

        Args:
            role_value: Значение роли для проверки

        Returns:
            True если роль имеет доступ (или если role_values пустой - доступ всем)
        """
        # Если role_values пустой или None, доступ есть у всех
        if not self.role_values:
            return True

        return role_value in self.role_values

    def can_transition_to(self, target_category_id: int) -> bool:
        """
        Проверить, можно ли перейти к указанной категории

        Args:
            target_category_id: ID целевой категории

        Returns:
            True если это следующая категория в workflow
        """
        return self.cat_next_id == target_category_id

    def can_transition_from(self, source_category_id: int) -> bool:
        """
        Проверить, можно ли перейти из указанной категории

        Args:
            source_category_id: ID исходной категории

        Returns:
            True если это предыдущая категория в workflow
        """
        return self.cat_previous_id == source_category_id

    def unlink_from_workflow(self) -> None:
        """Отвязать категорию от workflow"""
        self.cat_previous_id = None
        self.cat_next_id = None
        self.updated_at = datetime.utcnow()

    def get_workflow_position(self) -> str:
        """
        Получить позицию в workflow

        Returns:
            Строка с позицией: first, middle, last, standalone
        """
        if self.is_first_in_workflow() and self.is_last_in_workflow():
            return "standalone"
        elif self.is_first_in_workflow():
            return "first"
        elif self.is_last_in_workflow():
            return "last"
        else:
            return "middle"

    def validate(self) -> tuple[bool, str]:
        """
        Валидация категории

        Returns:
            Tuple (валидность, сообщение об ошибке)
        """
        if not self.title_ru or not self.title_ru.strip():
            return False, "Title in Russian is required"

        if not self.title_kk or not self.title_kk.strip():
            return False, "Title in Kazakh is required"

        if not self.value or not self.value.strip():
            return False, "Value is required"

        # Проверка на циклическую ссылку
        if self.id and (self.cat_previous_id == self.id or self.cat_next_id == self.id):
            return False, "Category cannot reference itself"

        return True, ""
