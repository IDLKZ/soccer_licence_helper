"""
Domain entity for ApplicationCriteria
Бизнес-сущность критерия заявки - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from enum import Enum


class CheckStage(str, Enum):
    """Этапы проверки критерия"""
    UPLOAD = "upload"
    FIRST_CHECK = "first_check"
    REGULAR_CHECK = "regular_check"
    CONTROL_CHECK = "control_check"


@dataclass
class ApplicationCriteria:
    """
    Бизнес-сущность критерия заявки

    Attributes:
        id: Уникальный идентификатор
        application_id: ID заявки
        category_id: ID категории документа
        status_id: ID статуса заявки

        uploaded_by_id: ID пользователя, загрузившего документ
        uploaded_by: Текстовая информация о загрузившем (для истории)

        first_checked_by_id: ID пользователя первичной проверки
        first_checked_by: Текстовая информация о проверяющем (для истории)

        checked_by_id: ID пользователя обычной проверки
        checked_by: Текстовая информация о проверяющем (для истории)

        control_checked_by_id: ID пользователя контрольной проверки
        control_checked_by: Текстовая информация о проверяющем (для истории)

        is_ready: Готов ли критерий
        is_first_passed: Прошел ли первичную проверку
        is_industry_passed: Прошел ли индустриальную проверку
        is_final_passed: Прошел ли финальную проверку
        can_reupload_after_ending: Можно ли перезагрузить после завершения
        can_reupload_after_endings_doc_ids: Список ID документов для перезагрузки

        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    id: Optional[int] = None
    application_id: Optional[int] = None
    category_id: Optional[int] = None
    status_id: Optional[int] = None

    # Upload info
    uploaded_by_id: Optional[int] = None
    uploaded_by: Optional[str] = None

    # First check info
    first_checked_by_id: Optional[int] = None
    first_checked_by: Optional[str] = None

    # Regular check info
    checked_by_id: Optional[int] = None
    checked_by: Optional[str] = None

    # Control check info
    control_checked_by_id: Optional[int] = None
    control_checked_by: Optional[str] = None

    # Status flags
    is_ready: bool = False
    is_first_passed: Optional[bool] = None
    is_industry_passed: Optional[bool] = None
    is_final_passed: Optional[bool] = None
    can_reupload_after_ending: Optional[bool] = None
    can_reupload_after_endings_doc_ids: Optional[List[int]] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Инициализация значений по умолчанию"""
        if self.can_reupload_after_endings_doc_ids is None:
            self.can_reupload_after_endings_doc_ids = []

    def mark_as_uploaded(self, user_id: int, user_info: str) -> None:
        """
        Отметить как загруженный

        Args:
            user_id: ID пользователя
            user_info: Информация о пользователе для истории
        """
        self.uploaded_by_id = user_id
        self.uploaded_by = user_info
        self.updated_at = datetime.utcnow()

    def mark_first_check(self, user_id: int, user_info: str, passed: bool) -> None:
        """
        Отметить первичную проверку

        Args:
            user_id: ID проверяющего
            user_info: Информация о проверяющем
            passed: Прошел ли проверку
        """
        self.first_checked_by_id = user_id
        self.first_checked_by = user_info
        self.is_first_passed = passed
        self.updated_at = datetime.utcnow()

    def mark_industry_check(self, user_id: int, user_info: str, passed: bool) -> None:
        """
        Отметить индустриальную проверку

        Args:
            user_id: ID проверяющего
            user_info: Информация о проверяющем
            passed: Прошел ли проверку
        """
        self.checked_by_id = user_id
        self.checked_by = user_info
        self.is_industry_passed = passed
        self.updated_at = datetime.utcnow()

    def mark_control_check(self, user_id: int, user_info: str, passed: bool) -> None:
        """
        Отметить контрольную проверку

        Args:
            user_id: ID проверяющего
            user_info: Информация о проверяющем
            passed: Прошел ли проверку
        """
        self.control_checked_by_id = user_id
        self.control_checked_by = user_info
        self.is_final_passed = passed
        self.updated_at = datetime.utcnow()

    def mark_as_ready(self) -> None:
        """Отметить как готовый"""
        self.is_ready = True
        self.updated_at = datetime.utcnow()

    def mark_as_not_ready(self) -> None:
        """Отметить как не готовый"""
        self.is_ready = False
        self.updated_at = datetime.utcnow()

    def is_fully_passed(self) -> bool:
        """
        Проверить, прошел ли критерий все этапы проверки

        Returns:
            True если все проверки пройдены успешно
        """
        return (
            self.is_first_passed is True and
            self.is_industry_passed is True and
            self.is_final_passed is True
        )

    def is_partially_passed(self) -> bool:
        """
        Проверить, прошел ли критерий хотя бы одну проверку

        Returns:
            True если хотя бы одна проверка пройдена
        """
        return (
            self.is_first_passed is True or
            self.is_industry_passed is True or
            self.is_final_passed is True
        )

    def has_failed_checks(self) -> bool:
        """
        Проверить, есть ли проваленные проверки

        Returns:
            True если хотя бы одна проверка провалена
        """
        return (
            self.is_first_passed is False or
            self.is_industry_passed is False or
            self.is_final_passed is False
        )

    def get_current_stage(self) -> Optional[CheckStage]:
        """
        Получить текущий этап проверки

        Returns:
            Текущий этап проверки или None если еще не загружено
        """
        if not self.uploaded_by_id:
            return None

        if self.is_final_passed is not None:
            return CheckStage.CONTROL_CHECK

        if self.is_industry_passed is not None:
            return CheckStage.REGULAR_CHECK

        if self.is_first_passed is not None:
            return CheckStage.FIRST_CHECK

        return CheckStage.UPLOAD

    def get_next_stage(self) -> Optional[CheckStage]:
        """
        Получить следующий этап проверки

        Returns:
            Следующий этап или None если все этапы завершены
        """
        current = self.get_current_stage()

        if current == CheckStage.UPLOAD:
            return CheckStage.FIRST_CHECK
        elif current == CheckStage.FIRST_CHECK and self.is_first_passed:
            return CheckStage.REGULAR_CHECK
        elif current == CheckStage.REGULAR_CHECK and self.is_industry_passed:
            return CheckStage.CONTROL_CHECK
        elif current == CheckStage.CONTROL_CHECK and self.is_final_passed:
            return None  # Все этапы завершены

        return None

    def can_proceed_to_next_stage(self) -> bool:
        """
        Проверить, можно ли перейти к следующему этапу

        Returns:
            True если можно перейти к следующему этапу
        """
        current = self.get_current_stage()

        if current == CheckStage.UPLOAD:
            return True
        elif current == CheckStage.FIRST_CHECK:
            return self.is_first_passed is True
        elif current == CheckStage.REGULAR_CHECK:
            return self.is_industry_passed is True
        elif current == CheckStage.CONTROL_CHECK:
            return self.is_final_passed is True

        return False

    def enable_reupload(self, document_ids: Optional[List[int]] = None) -> None:
        """
        Разрешить перезагрузку документов

        Args:
            document_ids: Список ID документов для перезагрузки
        """
        self.can_reupload_after_ending = True
        if document_ids:
            self.can_reupload_after_endings_doc_ids = document_ids
        self.updated_at = datetime.utcnow()

    def disable_reupload(self) -> None:
        """Запретить перезагрузку документов"""
        self.can_reupload_after_ending = False
        self.can_reupload_after_endings_doc_ids = []
        self.updated_at = datetime.utcnow()

    def can_reupload_document(self, document_id: int) -> bool:
        """
        Проверить, можно ли перезагрузить документ

        Args:
            document_id: ID документа

        Returns:
            True если можно перезагрузить
        """
        if not self.can_reupload_after_ending:
            return False

        if not self.can_reupload_after_endings_doc_ids:
            return True  # Если список пустой, можно все

        return document_id in self.can_reupload_after_endings_doc_ids

    def add_reuploadable_document(self, document_id: int) -> None:
        """
        Добавить документ в список разрешенных для перезагрузки

        Args:
            document_id: ID документа
        """
        if self.can_reupload_after_endings_doc_ids is None:
            self.can_reupload_after_endings_doc_ids = []

        if document_id not in self.can_reupload_after_endings_doc_ids:
            self.can_reupload_after_endings_doc_ids.append(document_id)
            self.updated_at = datetime.utcnow()

    def remove_reuploadable_document(self, document_id: int) -> None:
        """
        Удалить документ из списка разрешенных для перезагрузки

        Args:
            document_id: ID документа
        """
        if self.can_reupload_after_endings_doc_ids and document_id in self.can_reupload_after_endings_doc_ids:
            self.can_reupload_after_endings_doc_ids.remove(document_id)
            self.updated_at = datetime.utcnow()

    def reset_checks(self) -> None:
        """Сбросить все проверки"""
        self.is_first_passed = None
        self.is_industry_passed = None
        self.is_final_passed = None
        self.is_ready = False
        self.updated_at = datetime.utcnow()

    def get_completion_percentage(self) -> float:
        """
        Получить процент завершенности проверок

        Returns:
            Процент от 0 до 100
        """
        total_checks = 3
        passed_checks = 0

        if self.is_first_passed is True:
            passed_checks += 1
        if self.is_industry_passed is True:
            passed_checks += 1
        if self.is_final_passed is True:
            passed_checks += 1

        return (passed_checks / total_checks) * 100
