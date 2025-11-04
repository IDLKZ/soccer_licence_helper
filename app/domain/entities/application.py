"""
Domain entity for Application
Бизнес-сущность заявки на лицензию - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class ApplicationStatus(str, Enum):
    """Статусы заявки"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


@dataclass
class Application:
    """
    Бизнес-сущность заявки на лицензию

    Attributes:
        id: Уникальный идентификатор
        user_id: ID пользователя, создавшего заявку
        license_id: ID лицензии, на которую подается заявка
        club_id: ID клуба, для которого подается заявка
        category_id: ID категории статуса заявки
        is_ready: Готова ли заявка к отправке
        is_active: Активна ли заявка
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    id: Optional[int] = None
    user_id: Optional[int] = None
    license_id: Optional[int] = None
    club_id: Optional[int] = None
    category_id: Optional[int] = None
    is_ready: bool = False
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def mark_as_ready(self) -> None:
        """Отметить заявку как готовую к отправке"""
        self.is_ready = True
        self.updated_at = datetime.utcnow()

    def mark_as_not_ready(self) -> None:
        """Отметить заявку как не готовую"""
        self.is_ready = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Активировать заявку"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивировать заявку"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def is_application_active(self) -> bool:
        """
        Проверить, активна ли заявка

        Returns:
            True если заявка активна
        """
        return self.is_active is True

    def can_be_submitted(self) -> bool:
        """
        Проверить, можно ли отправить заявку

        Returns:
            True если заявка готова и имеет все необходимые данные
        """
        return (
            self.is_ready and
            self.user_id is not None and
            self.license_id is not None and
            self.club_id is not None
        )

    def can_be_edited(self) -> bool:
        """
        Проверить, можно ли редактировать заявку

        Returns:
            True если заявка еще не отправлена или активна
        """
        # Можно редактировать если не готова или активна
        return not self.is_ready or self.is_active is True

    def update_user(self, user_id: int) -> None:
        """
        Обновить пользователя заявки

        Args:
            user_id: Новый ID пользователя
        """
        self.user_id = user_id
        self.updated_at = datetime.utcnow()

    def update_license(self, license_id: int) -> None:
        """
        Обновить лицензию заявки

        Args:
            license_id: Новый ID лицензии
        """
        self.license_id = license_id
        self.updated_at = datetime.utcnow()

    def update_club(self, club_id: int) -> None:
        """
        Обновить клуб заявки

        Args:
            club_id: Новый ID клуба
        """
        self.club_id = club_id
        self.updated_at = datetime.utcnow()

    def update_category(self, category_id: int) -> None:
        """
        Обновить категорию статуса заявки

        Args:
            category_id: Новый ID категории
        """
        self.category_id = category_id
        self.updated_at = datetime.utcnow()

    def has_required_data(self) -> bool:
        """
        Проверить, заполнены ли все обязательные данные

        Returns:
            True если все обязательные поля заполнены
        """
        return (
            self.user_id is not None and
            self.license_id is not None and
            self.club_id is not None
        )

    def validate(self) -> tuple[bool, str]:
        """
        Валидация заявки

        Returns:
            Tuple (валидность, сообщение об ошибке)
        """
        if self.user_id is None:
            return False, "User ID is required"

        if self.license_id is None:
            return False, "License ID is required"

        if self.club_id is None:
            return False, "Club ID is required"

        return True, ""

    def reset(self) -> None:
        """Сбросить статусы заявки"""
        self.is_ready = False
        self.is_active = None
        self.updated_at = datetime.utcnow()

    def submit(self) -> bool:
        """
        Отправить заявку на рассмотрение

        Returns:
            True если заявка успешно отправлена

        Raises:
            ValueError: Если заявка не готова к отправке
        """
        is_valid, error_message = self.validate()
        if not is_valid:
            raise ValueError(f"Cannot submit application: {error_message}")

        if not self.is_ready:
            raise ValueError("Application is not ready for submission")

        self.is_active = True
        self.updated_at = datetime.utcnow()
        return True

    def cancel(self) -> None:
        """Отменить заявку"""
        self.is_active = False
        self.is_ready = False
        self.updated_at = datetime.utcnow()

    def is_complete(self) -> bool:
        """
        Проверить, завершена ли заявка

        Returns:
            True если заявка готова и активна
        """
        return self.is_ready and self.is_active is True

    def get_status_summary(self) -> str:
        """
        Получить текстовую сводку статуса заявки

        Returns:
            Строка со статусом
        """
        if not self.is_ready:
            return "draft"
        elif self.is_active is True:
            return "active"
        elif self.is_active is False:
            return "inactive"
        else:
            return "pending"

    def can_be_deleted(self) -> bool:
        """
        Проверить, можно ли удалить заявку

        Returns:
            True если заявка не активна
        """
        return self.is_active is not True

    def clone_for_new_license(self, new_license_id: int) -> 'Application':
        """
        Клонировать заявку для новой лицензии

        Args:
            new_license_id: ID новой лицензии

        Returns:
            Новый экземпляр Application
        """
        return Application(
            user_id=self.user_id,
            license_id=new_license_id,
            club_id=self.club_id,
            category_id=self.category_id,
            is_ready=False,
            is_active=None
        )
