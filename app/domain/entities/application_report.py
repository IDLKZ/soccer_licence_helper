"""
Domain entity for ApplicationReport
Бизнес-сущность отчета по критерию заявки - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import IntEnum


class ReportStatus(IntEnum):
    """Статусы отчета по критерию заявки"""
    PENDING = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    APPROVED = 3
    REJECTED = 4
    REQUIRES_REVISION = 5
    CANCELLED = 6


@dataclass
class ApplicationReport:
    """
    Бизнес-сущность отчета по критерию заявки

    Attributes:
        id: Уникальный идентификатор
        application_id: ID заявки
        criteria_id: ID критерия заявки
        status: Статус отчета (integer)
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    status: int
    id: Optional[int] = None
    application_id: Optional[int] = None
    criteria_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def get_status_enum(self) -> ReportStatus:
        """
        Получить статус как enum

        Returns:
            ReportStatus enum
        """
        try:
            return ReportStatus(self.status)
        except ValueError:
            return ReportStatus.PENDING

    def update_status(self, new_status: int) -> None:
        """
        Обновить статус отчета

        Args:
            new_status: Новый статус

        Raises:
            ValueError: Если статус невалиден
        """
        try:
            ReportStatus(new_status)
            self.status = new_status
            self.updated_at = datetime.utcnow()
        except ValueError:
            raise ValueError(f"Invalid status value: {new_status}")

    def set_status_enum(self, status: ReportStatus) -> None:
        """
        Установить статус через enum

        Args:
            status: ReportStatus enum
        """
        self.status = status.value
        self.updated_at = datetime.utcnow()

    def mark_as_pending(self) -> None:
        """Отметить как ожидающий"""
        self.status = ReportStatus.PENDING.value
        self.updated_at = datetime.utcnow()

    def mark_as_in_progress(self) -> None:
        """Отметить как в процессе"""
        self.status = ReportStatus.IN_PROGRESS.value
        self.updated_at = datetime.utcnow()

    def mark_as_completed(self) -> None:
        """Отметить как завершенный"""
        self.status = ReportStatus.COMPLETED.value
        self.updated_at = datetime.utcnow()

    def mark_as_approved(self) -> None:
        """Отметить как одобренный"""
        self.status = ReportStatus.APPROVED.value
        self.updated_at = datetime.utcnow()

    def mark_as_rejected(self) -> None:
        """Отметить как отклоненный"""
        self.status = ReportStatus.REJECTED.value
        self.updated_at = datetime.utcnow()

    def mark_as_requires_revision(self) -> None:
        """Отметить как требующий доработки"""
        self.status = ReportStatus.REQUIRES_REVISION.value
        self.updated_at = datetime.utcnow()

    def mark_as_cancelled(self) -> None:
        """Отметить как отмененный"""
        self.status = ReportStatus.CANCELLED.value
        self.updated_at = datetime.utcnow()

    def is_pending(self) -> bool:
        """Проверить, ожидает ли отчет"""
        return self.status == ReportStatus.PENDING.value

    def is_in_progress(self) -> bool:
        """Проверить, в процессе ли отчет"""
        return self.status == ReportStatus.IN_PROGRESS.value

    def is_completed(self) -> bool:
        """Проверить, завершен ли отчет"""
        return self.status == ReportStatus.COMPLETED.value

    def is_approved(self) -> bool:
        """Проверить, одобрен ли отчет"""
        return self.status == ReportStatus.APPROVED.value

    def is_rejected(self) -> bool:
        """Проверить, отклонен ли отчет"""
        return self.status == ReportStatus.REJECTED.value

    def requires_revision(self) -> bool:
        """Проверить, требуется ли доработка"""
        return self.status == ReportStatus.REQUIRES_REVISION.value

    def is_cancelled(self) -> bool:
        """Проверить, отменен ли отчет"""
        return self.status == ReportStatus.CANCELLED.value

    def is_final_status(self) -> bool:
        """
        Проверить, является ли статус финальным

        Returns:
            True если статус: approved, rejected или cancelled
        """
        return self.status in [
            ReportStatus.APPROVED.value,
            ReportStatus.REJECTED.value,
            ReportStatus.CANCELLED.value
        ]

    def can_be_edited(self) -> bool:
        """
        Проверить, можно ли редактировать отчет

        Returns:
            True если статус не финальный
        """
        return not self.is_final_status()

    def can_be_approved(self) -> bool:
        """
        Проверить, можно ли одобрить отчет

        Returns:
            True если отчет завершен
        """
        return self.status == ReportStatus.COMPLETED.value

    def can_be_rejected(self) -> bool:
        """
        Проверить, можно ли отклонить отчет

        Returns:
            True если отчет в процессе или завершен
        """
        return self.status in [
            ReportStatus.IN_PROGRESS.value,
            ReportStatus.COMPLETED.value
        ]

    def can_be_cancelled(self) -> bool:
        """
        Проверить, можно ли отменить отчет

        Returns:
            True если статус не финальный
        """
        return not self.is_final_status()

    def get_status_display(self) -> str:
        """
        Получить человекочитаемое название статуса

        Returns:
            Название статуса
        """
        status_names = {
            ReportStatus.PENDING.value: "Ожидает",
            ReportStatus.IN_PROGRESS.value: "В процессе",
            ReportStatus.COMPLETED.value: "Завершен",
            ReportStatus.APPROVED.value: "Одобрен",
            ReportStatus.REJECTED.value: "Отклонен",
            ReportStatus.REQUIRES_REVISION.value: "Требует доработки",
            ReportStatus.CANCELLED.value: "Отменен"
        }
        return status_names.get(self.status, "Неизвестно")

    def validate_transition(self, new_status: int) -> tuple[bool, str]:
        """
        Валидация перехода между статусами

        Args:
            new_status: Новый статус

        Returns:
            Tuple (валидность, сообщение об ошибке)
        """
        # Из финального статуса нельзя переходить
        if self.is_final_status():
            return False, f"Cannot change from final status: {self.get_status_display()}"

        # Проверка валидных переходов
        valid_transitions = {
            ReportStatus.PENDING.value: [
                ReportStatus.IN_PROGRESS.value,
                ReportStatus.CANCELLED.value
            ],
            ReportStatus.IN_PROGRESS.value: [
                ReportStatus.COMPLETED.value,
                ReportStatus.REQUIRES_REVISION.value,
                ReportStatus.REJECTED.value,
                ReportStatus.CANCELLED.value
            ],
            ReportStatus.COMPLETED.value: [
                ReportStatus.APPROVED.value,
                ReportStatus.REJECTED.value,
                ReportStatus.REQUIRES_REVISION.value
            ],
            ReportStatus.REQUIRES_REVISION.value: [
                ReportStatus.IN_PROGRESS.value,
                ReportStatus.CANCELLED.value
            ]
        }

        allowed_statuses = valid_transitions.get(self.status, [])
        if new_status not in allowed_statuses:
            return False, f"Invalid status transition from {self.get_status_display()}"

        return True, ""

    def transition_to(self, new_status: int) -> None:
        """
        Перейти к новому статусу с валидацией

        Args:
            new_status: Новый статус

        Raises:
            ValueError: Если переход невалиден
        """
        is_valid, error_message = self.validate_transition(new_status)
        if not is_valid:
            raise ValueError(error_message)

        self.update_status(new_status)

    def reset(self) -> None:
        """Сбросить отчет к начальному состоянию"""
        if self.can_be_edited():
            self.status = ReportStatus.PENDING.value
            self.updated_at = datetime.utcnow()
