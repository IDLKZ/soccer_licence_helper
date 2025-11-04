"""
Domain entity for ApplicationDocument
Бизнес-сущность документа заявки - чистая модель без зависимостей от БД
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ApplicationDocument:
    """
    Бизнес-сущность документа заявки

    Attributes:
        id: Уникальный идентификатор
        application_id: ID заявки
        category_id: ID категории документа
        document_id: ID документа
        file_url: URL файла документа
        title: Название документа
        info: Дополнительная информация о документе

        uploaded_by_id: ID пользователя, загрузившего документ
        uploaded_by: Текстовая информация о загрузившем

        first_checked_by_id: ID пользователя первичной проверки
        first_checked_by: Текстовая информация о проверяющем
        first_comment: Комментарий первичной проверки

        checked_by_id: ID пользователя обычной проверки
        checked_by: Текстовая информация о проверяющем
        industry_comment: Комментарий индустриальной проверки

        control_checked_by_id: ID пользователя контрольной проверки
        control_checked_by: Текстовая информация о проверяющем
        control_comment: Комментарий контрольной проверки

        is_first_passed: Прошел ли первичную проверку
        is_industry_passed: Прошел ли индустриальную проверку
        is_final_passed: Прошел ли финальную проверку

        deadline: Дедлайн для документа
        created_at: Дата создания
        updated_at: Дата последнего обновления
    """
    file_url: str
    title: str
    id: Optional[int] = None
    application_id: Optional[int] = None
    category_id: Optional[int] = None
    document_id: Optional[int] = None
    info: Optional[str] = None

    # Upload info
    uploaded_by_id: Optional[int] = None
    uploaded_by: Optional[str] = None

    # First check info
    first_checked_by_id: Optional[int] = None
    first_checked_by: Optional[str] = None
    first_comment: Optional[str] = None

    # Industry check info
    checked_by_id: Optional[int] = None
    checked_by: Optional[str] = None
    industry_comment: Optional[str] = None

    # Control check info
    control_checked_by_id: Optional[int] = None
    control_checked_by: Optional[str] = None
    control_comment: Optional[str] = None

    # Status flags
    is_first_passed: Optional[bool] = None
    is_industry_passed: Optional[bool] = None
    is_final_passed: Optional[bool] = None

    # Deadline
    deadline: Optional[datetime] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def mark_as_uploaded(self, user_id: int, user_info: str) -> None:
        """
        Отметить как загруженный

        Args:
            user_id: ID пользователя
            user_info: Информация о пользователе
        """
        self.uploaded_by_id = user_id
        self.uploaded_by = user_info
        self.updated_at = datetime.utcnow()

    def mark_first_check(self, user_id: int, user_info: str, passed: bool, comment: Optional[str] = None) -> None:
        """
        Отметить первичную проверку

        Args:
            user_id: ID проверяющего
            user_info: Информация о проверяющем
            passed: Прошел ли проверку
            comment: Комментарий проверяющего
        """
        self.first_checked_by_id = user_id
        self.first_checked_by = user_info
        self.is_first_passed = passed
        self.first_comment = comment
        self.updated_at = datetime.utcnow()

    def mark_industry_check(self, user_id: int, user_info: str, passed: bool, comment: Optional[str] = None) -> None:
        """
        Отметить индустриальную проверку

        Args:
            user_id: ID проверяющего
            user_info: Информация о проверяющем
            passed: Прошел ли проверку
            comment: Комментарий проверяющего
        """
        self.checked_by_id = user_id
        self.checked_by = user_info
        self.is_industry_passed = passed
        self.industry_comment = comment
        self.updated_at = datetime.utcnow()

    def mark_control_check(self, user_id: int, user_info: str, passed: bool, comment: Optional[str] = None) -> None:
        """
        Отметить контрольную проверку

        Args:
            user_id: ID проверяющего
            user_info: Информация о проверяющем
            passed: Прошел ли проверку
            comment: Комментарий проверяющего
        """
        self.control_checked_by_id = user_id
        self.control_checked_by = user_info
        self.is_final_passed = passed
        self.control_comment = comment
        self.updated_at = datetime.utcnow()

    def update_file(self, file_url: str) -> None:
        """
        Обновить файл документа

        Args:
            file_url: Новый URL файла
        """
        self.file_url = file_url
        self.updated_at = datetime.utcnow()

    def update_title(self, title: str) -> None:
        """
        Обновить название документа

        Args:
            title: Новое название
        """
        self.title = title
        self.updated_at = datetime.utcnow()

    def update_info(self, info: str) -> None:
        """
        Обновить информацию о документе

        Args:
            info: Новая информация
        """
        self.info = info
        self.updated_at = datetime.utcnow()

    def set_deadline(self, deadline: datetime) -> None:
        """
        Установить дедлайн

        Args:
            deadline: Дата дедлайна
        """
        self.deadline = deadline
        self.updated_at = datetime.utcnow()

    def extend_deadline(self, days: int) -> None:
        """
        Продлить дедлайн

        Args:
            days: Количество дней для продления
        """
        if self.deadline:
            from datetime import timedelta
            self.deadline = self.deadline + timedelta(days=days)
            self.updated_at = datetime.utcnow()

    def is_overdue(self) -> bool:
        """
        Проверить, просрочен ли дедлайн

        Returns:
            True если дедлайн прошел
        """
        if not self.deadline:
            return False
        return datetime.utcnow() > self.deadline

    def days_until_deadline(self) -> Optional[int]:
        """
        Количество дней до дедлайна

        Returns:
            Количество дней (отрицательное если просрочено)
        """
        if not self.deadline:
            return None
        delta = self.deadline - datetime.utcnow()
        return delta.days

    def is_fully_passed(self) -> bool:
        """
        Проверить, прошел ли документ все проверки

        Returns:
            True если все проверки пройдены
        """
        return (
            self.is_first_passed is True and
            self.is_industry_passed is True and
            self.is_final_passed is True
        )

    def is_partially_passed(self) -> bool:
        """
        Проверить, прошел ли хотя бы одну проверку

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

    def get_failed_stages(self) -> list[str]:
        """
        Получить список проваленных этапов

        Returns:
            Список названий этапов
        """
        failed = []
        if self.is_first_passed is False:
            failed.append("first_check")
        if self.is_industry_passed is False:
            failed.append("industry_check")
        if self.is_final_passed is False:
            failed.append("control_check")
        return failed

    def get_current_stage(self) -> Optional[str]:
        """
        Получить текущий этап проверки

        Returns:
            Название текущего этапа
        """
        if not self.uploaded_by_id:
            return "not_uploaded"

        if self.is_final_passed is not None:
            return "control_check_completed"

        if self.is_industry_passed is not None:
            return "industry_check_completed"

        if self.is_first_passed is not None:
            return "first_check_completed"

        return "uploaded"

    def get_all_comments(self) -> list[dict]:
        """
        Получить все комментарии проверок

        Returns:
            Список словарей с комментариями
        """
        comments = []

        if self.first_comment:
            comments.append({
                "stage": "first_check",
                "comment": self.first_comment,
                "checked_by": self.first_checked_by,
                "passed": self.is_first_passed
            })

        if self.industry_comment:
            comments.append({
                "stage": "industry_check",
                "comment": self.industry_comment,
                "checked_by": self.checked_by,
                "passed": self.is_industry_passed
            })

        if self.control_comment:
            comments.append({
                "stage": "control_check",
                "comment": self.control_comment,
                "checked_by": self.control_checked_by,
                "passed": self.is_final_passed
            })

        return comments

    def reset_checks(self) -> None:
        """Сбросить все проверки"""
        self.is_first_passed = None
        self.is_industry_passed = None
        self.is_final_passed = None
        self.first_comment = None
        self.industry_comment = None
        self.control_comment = None
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

    def has_file(self) -> bool:
        """
        Проверить, есть ли файл

        Returns:
            True если file_url не пустой
        """
        return bool(self.file_url)

    def can_be_rechecked(self) -> bool:
        """
        Проверить, можно ли перепроверить документ

        Returns:
            True если есть проваленные проверки
        """
        return self.has_failed_checks()

    def needs_review(self) -> bool:
        """
        Проверить, требуется ли проверка

        Returns:
            True если есть непроверенные этапы
        """
        return (
            self.is_first_passed is None or
            self.is_industry_passed is None or
            self.is_final_passed is None
        )
