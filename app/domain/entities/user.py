"""
Domain entity for User
Бизнес-сущность пользователя - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """
    Бизнес-сущность пользователя

    Attributes:
        id: Уникальный идентификатор
        role_id: ID роли пользователя
        email: Email адрес (уникальный)
        phone: Номер телефона (уникальный)
        username: Имя пользователя (уникальное)
        first_name: Имя
        last_name: Фамилия
        patronymic: Отчество
        iin: ИИН (Индивидуальный идентификационный номер) - 12 символов
        position: Должность
        image_url: URL изображения профиля
        password: Хэш пароля
        is_active: Активен ли пользователь
        verified: Верифицирован ли пользователь
        remember_token: Токен для "запомнить меня"
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """

    def __init__(self):
        pass

    email: str
    phone: str
    username: str
    first_name: str
    id: Optional[int] = None
    role_id: Optional[int] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    iin: Optional[str] = None
    position: Optional[str] = None
    image_url: Optional[str] = None
    password: Optional[str] = None
    is_active: bool = True
    verified: bool = False
    remember_token: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_full_name(self) -> str:
        """
        Получить полное имя пользователя

        Returns:
            Полное имя в формате: Фамилия Имя Отчество
        """
        parts = []
        if self.last_name:
            parts.append(self.last_name)
        parts.append(self.first_name)
        if self.patronymic:
            parts.append(self.patronymic)
        return " ".join(parts)

    def get_short_name(self) -> str:
        """
        Получить короткое имя пользователя

        Returns:
            Короткое имя в формате: Фамилия И.О.
        """
        if not self.last_name:
            return self.first_name

        parts = [self.last_name]

        if self.first_name:
            parts.append(f"{self.first_name[0]}.")

        if self.patronymic:
            parts.append(f"{self.patronymic[0]}.")

        return " ".join(parts)

    def activate(self) -> None:
        """Активировать пользователя"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Деактивировать пользователя"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def verify(self) -> None:
        """Верифицировать пользователя"""
        self.verified = True
        self.updated_at = datetime.utcnow()

    def unverify(self) -> None:
        """Снять верификацию пользователя"""
        self.verified = False
        self.updated_at = datetime.utcnow()

    def update_profile(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        patronymic: Optional[str] = None,
        position: Optional[str] = None,
        image_url: Optional[str] = None
    ) -> None:
        """
        Обновить профиль пользователя

        Args:
            first_name: Новое имя
            last_name: Новая фамилия
            patronymic: Новое отчество
            position: Новая должность
            image_url: Новый URL изображения
        """
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if patronymic is not None:
            self.patronymic = patronymic
        if position is not None:
            self.position = position
        if image_url is not None:
            self.image_url = image_url
        self.updated_at = datetime.utcnow()

    def change_role(self, role_id: Optional[int]) -> None:
        """
        Изменить роль пользователя

        Args:
            role_id: Новый ID роли
        """
        self.role_id = role_id
        self.updated_at = datetime.utcnow()

    def is_verified(self) -> bool:
        """Проверить, верифицирован ли пользователь"""
        return self.verified

    def is_user_active(self) -> bool:
        """Проверить, активен ли пользователь"""
        return self.is_active

    def can_login(self) -> bool:
        """
        Проверить, может ли пользователь войти в систему

        Returns:
            True если пользователь активен и верифицирован
        """
        return self.is_active and self.verified

    def validate_iin(self) -> bool:
        """
        Валидация ИИН (должен быть 12 символов)

        Returns:
            True если ИИН валиден или отсутствует
        """
        if self.iin is None:
            return True
        return len(self.iin) == 12 and self.iin.isdigit()
