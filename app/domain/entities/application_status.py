"""
Domain entity for ApplicationStatus
Бизнес-сущность статуса заявки - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from app.domain.entities.license import Language


@dataclass
class ApplicationStatus:
    """
    Бизнес-сущность статуса заявки

    Attributes:
        id: Уникальный идентификатор
        category_id: ID категории статуса
        previous_id: ID предыдущего статуса в workflow
        next_id: ID следующего статуса в workflow
        title_ru: Название на русском
        title_kk: Название на казахском
        title_en: Название на английском
        description_ru: Описание на русском
        description_kk: Описание на казахском
        description_en: Описание на английском
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    title_ru: str
    title_kk: str
    id: Optional[int] = None
    category_id: Optional[int] = None
    previous_id: Optional[int] = None
    next_id: Optional[int] = None
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_title(self, language: Language = Language.RU) -> str:
        """
        Получить название на указанном языке

        Args:
            language: Язык (по умолчанию русский)

        Returns:
            Название статуса на указанном языке
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
            Описание статуса на указанном языке
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
        Обновить переводы статуса

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

    def set_category(self, category_id: int) -> None:
        """
        Установить категорию статуса

        Args:
            category_id: ID категории
        """
        self.category_id = category_id
        self.updated_at = datetime.utcnow()

    def set_previous_status(self, status_id: Optional[int]) -> None:
        """
        Установить предыдущий статус в workflow

        Args:
            status_id: ID предыдущего статуса
        """
        self.previous_id = status_id
        self.updated_at = datetime.utcnow()

    def set_next_status(self, status_id: Optional[int]) -> None:
        """
        Установить следующий статус в workflow

        Args:
            status_id: ID следующего статуса
        """
        self.next_id = status_id
        self.updated_at = datetime.utcnow()

    def has_previous(self) -> bool:
        """
        Проверить, есть ли предыдущий статус

        Returns:
            True если есть предыдущий статус
        """
        return self.previous_id is not None

    def has_next(self) -> bool:
        """
        Проверить, есть ли следующий статус

        Returns:
            True если есть следующий статус
        """
        return self.next_id is not None

    def is_first_in_workflow(self) -> bool:
        """
        Проверить, является ли статус первым в workflow

        Returns:
            True если это начальный статус
        """
        return self.previous_id is None

    def is_last_in_workflow(self) -> bool:
        """
        Проверить, является ли статус последним в workflow

        Returns:
            True если это финальный статус
        """
        return self.next_id is None

    def belongs_to_category(self, category_id: int) -> bool:
        """
        Проверить, принадлежит ли статус указанной категории

        Args:
            category_id: ID категории для проверки

        Returns:
            True если статус принадлежит категории
        """
        return self.category_id == category_id

    def can_transition_to(self, target_status_id: int) -> bool:
        """
        Проверить, можно ли перейти к указанному статусу

        Args:
            target_status_id: ID целевого статуса

        Returns:
            True если это следующий статус в workflow
        """
        return self.next_id == target_status_id

    def can_transition_from(self, source_status_id: int) -> bool:
        """
        Проверить, можно ли перейти из указанного статуса

        Args:
            source_status_id: ID исходного статуса

        Returns:
            True если это предыдущий статус в workflow
        """
        return self.previous_id == source_status_id

    def unlink_from_workflow(self) -> None:
        """Отвязать статус от workflow"""
        self.previous_id = None
        self.next_id = None
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
        Валидация статуса

        Returns:
            Tuple (валидность, сообщение об ошибке)
        """
        if not self.title_ru or not self.title_ru.strip():
            return False, "Title in Russian is required"

        if not self.title_kk or not self.title_kk.strip():
            return False, "Title in Kazakh is required"

        # Проверка на циклическую ссылку
        if self.id and (self.previous_id == self.id or self.next_id == self.id):
            return False, "Status cannot reference itself"

        return True, ""

    def is_valid_transition(self, from_status_id: int, to_status_id: int) -> bool:
        """
        Проверить валидность перехода между статусами

        Args:
            from_status_id: ID исходного статуса
            to_status_id: ID целевого статуса

        Returns:
            True если переход валиден
        """
        # Если это переход из текущего статуса
        if from_status_id == self.id:
            return self.can_transition_to(to_status_id)
        # Если это переход в текущий статус
        elif to_status_id == self.id:
            return self.can_transition_from(from_status_id)
        return False

    def get_display_info(self, language: Language = Language.RU) -> dict:
        """
        Получить информацию для отображения

        Args:
            language: Язык

        Returns:
            Словарь с информацией для отображения
        """
        return {
            "id": self.id,
            "title": self.get_title(language),
            "description": self.get_description(language),
            "category_id": self.category_id,
            "workflow_position": self.get_workflow_position(),
            "has_previous": self.has_previous(),
            "has_next": self.has_next()
        }
