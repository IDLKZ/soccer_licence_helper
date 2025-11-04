"""
Domain entity for ApplicationSolution
Бизнес-сущность решения по заявке - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional


@dataclass
class ApplicationSolution:
    """
    Бизнес-сущность решения по заявке

    Attributes:
        id: Уникальный идентификатор
        application_id: ID заявки
        secretary_id: ID секретаря (пользователя)
        secretary_name: Имя секретаря (текстовое для истории)
        meeting_date: Дата встречи
        meeting_place: Место проведения встречи
        department_name: Название департамента
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    id: Optional[int] = None
    application_id: Optional[int] = None
    secretary_id: Optional[int] = None
    secretary_name: Optional[str] = None
    meeting_date: Optional[date] = None
    meeting_place: Optional[str] = None
    department_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def set_secretary(self, secretary_id: int, secretary_name: str) -> None:
        """
        Установить секретаря

        Args:
            secretary_id: ID секретаря
            secretary_name: Имя секретаря
        """
        self.secretary_id = secretary_id
        self.secretary_name = secretary_name
        self.updated_at = datetime.utcnow()

    def update_secretary_name(self, secretary_name: str) -> None:
        """
        Обновить имя секретаря

        Args:
            secretary_name: Новое имя секретаря
        """
        self.secretary_name = secretary_name
        self.updated_at = datetime.utcnow()

    def schedule_meeting(
        self,
        meeting_date: date,
        meeting_place: str,
        department_name: Optional[str] = None
    ) -> None:
        """
        Назначить встречу

        Args:
            meeting_date: Дата встречи
            meeting_place: Место встречи
            department_name: Название департамента
        """
        self.meeting_date = meeting_date
        self.meeting_place = meeting_place
        if department_name:
            self.department_name = department_name
        self.updated_at = datetime.utcnow()

    def update_meeting_date(self, new_date: date) -> None:
        """
        Обновить дату встречи

        Args:
            new_date: Новая дата встречи
        """
        self.meeting_date = new_date
        self.updated_at = datetime.utcnow()

    def update_meeting_place(self, new_place: str) -> None:
        """
        Обновить место встречи

        Args:
            new_place: Новое место встречи
        """
        self.meeting_place = new_place
        self.updated_at = datetime.utcnow()

    def update_department(self, department_name: str) -> None:
        """
        Обновить название департамента

        Args:
            department_name: Название департамента
        """
        self.department_name = department_name
        self.updated_at = datetime.utcnow()

    def has_meeting_scheduled(self) -> bool:
        """
        Проверить, назначена ли встреча

        Returns:
            True если встреча назначена
        """
        return self.meeting_date is not None and self.meeting_place is not None

    def has_secretary_assigned(self) -> bool:
        """
        Проверить, назначен ли секретарь

        Returns:
            True если секретарь назначен
        """
        return self.secretary_id is not None

    def is_meeting_past(self) -> bool:
        """
        Проверить, прошла ли встреча

        Returns:
            True если дата встречи в прошлом
        """
        if not self.meeting_date:
            return False
        return self.meeting_date < date.today()

    def is_meeting_today(self) -> bool:
        """
        Проверить, встреча сегодня

        Returns:
            True если встреча сегодня
        """
        if not self.meeting_date:
            return False
        return self.meeting_date == date.today()

    def is_meeting_upcoming(self) -> bool:
        """
        Проверить, встреча в будущем

        Returns:
            True если встреча еще не прошла
        """
        if not self.meeting_date:
            return False
        return self.meeting_date > date.today()

    def days_until_meeting(self) -> Optional[int]:
        """
        Количество дней до встречи

        Returns:
            Количество дней (отрицательное если уже прошла) или None
        """
        if not self.meeting_date:
            return None
        delta = self.meeting_date - date.today()
        return delta.days

    def is_complete(self) -> bool:
        """
        Проверить, заполнены ли все данные решения

        Returns:
            True если все обязательные поля заполнены
        """
        return (
            self.application_id is not None and
            self.secretary_id is not None and
            self.meeting_date is not None and
            self.meeting_place is not None
        )

    def validate(self) -> tuple[bool, str]:
        """
        Валидация решения

        Returns:
            Tuple (валидность, сообщение об ошибке)
        """
        if self.application_id is None:
            return False, "Application ID is required"

        if self.secretary_id is None:
            return False, "Secretary ID is required"

        if self.meeting_date is None:
            return False, "Meeting date is required"

        if self.meeting_place is None or not self.meeting_place.strip():
            return False, "Meeting place is required"

        if len(self.meeting_place) > 512:
            return False, "Meeting place is too long (max 512 characters)"

        if self.department_name and len(self.department_name) > 512:
            return False, "Department name is too long (max 512 characters)"

        return True, ""

    def get_meeting_status(self) -> str:
        """
        Получить статус встречи

        Returns:
            Строка со статусом: not_scheduled, past, today, upcoming
        """
        if not self.has_meeting_scheduled():
            return "not_scheduled"

        if self.is_meeting_past():
            return "past"
        elif self.is_meeting_today():
            return "today"
        elif self.is_meeting_upcoming():
            return "upcoming"

        return "unknown"

    def cancel_meeting(self) -> None:
        """Отменить встречу"""
        self.meeting_date = None
        self.meeting_place = None
        self.updated_at = datetime.utcnow()

    def reschedule_meeting(self, new_date: date, new_place: Optional[str] = None) -> None:
        """
        Перенести встречу

        Args:
            new_date: Новая дата встречи
            new_place: Новое место встречи (опционально)
        """
        self.meeting_date = new_date
        if new_place:
            self.meeting_place = new_place
        self.updated_at = datetime.utcnow()

    def clear_secretary(self) -> None:
        """Убрать секретаря"""
        self.secretary_id = None
        self.secretary_name = None
        self.updated_at = datetime.utcnow()

    def get_meeting_info_summary(self) -> str:
        """
        Получить краткую информацию о встрече

        Returns:
            Строка с информацией о встрече
        """
        if not self.has_meeting_scheduled():
            return "Meeting not scheduled"

        parts = []

        if self.meeting_date:
            parts.append(f"Date: {self.meeting_date}")

        if self.meeting_place:
            parts.append(f"Place: {self.meeting_place}")

        if self.department_name:
            parts.append(f"Department: {self.department_name}")

        if self.secretary_name:
            parts.append(f"Secretary: {self.secretary_name}")

        return ", ".join(parts)

    def is_ready_for_decision(self) -> bool:
        """
        Проверить, готово ли решение для принятия

        Returns:
            True если встреча прошла и все данные заполнены
        """
        return self.is_complete() and self.is_meeting_past()
