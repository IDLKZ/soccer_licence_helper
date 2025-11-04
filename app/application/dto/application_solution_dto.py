"""
Data Transfer Objects for ApplicationSolution
DTO для передачи данных решения по заявке между слоями
"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List


@dataclass
class CreateApplicationSolutionDTO:
    """DTO для создания решения по заявке"""
    application_id: int
    secretary_id: int
    secretary_name: str
    meeting_date: Optional[date] = None
    meeting_place: Optional[str] = None
    department_name: Optional[str] = None


@dataclass
class UpdateApplicationSolutionDTO:
    """DTO для обновления решения по заявке"""
    solution_id: int
    application_id: Optional[int] = None
    secretary_id: Optional[int] = None
    secretary_name: Optional[str] = None
    meeting_date: Optional[date] = None
    meeting_place: Optional[str] = None
    department_name: Optional[str] = None


@dataclass
class ScheduleMeetingDTO:
    """DTO для назначения встречи"""
    solution_id: int
    meeting_date: date
    meeting_place: str
    department_name: Optional[str] = None


@dataclass
class RescheduleMeetingDTO:
    """DTO для переноса встречи"""
    solution_id: int
    new_date: date
    new_place: Optional[str] = None


@dataclass
class CancelMeetingDTO:
    """DTO для отмены встречи"""
    solution_id: int
    cancelled_by_id: int
    reason: Optional[str] = None


@dataclass
class SetSecretaryDTO:
    """DTO для назначения секретаря"""
    solution_id: int
    secretary_id: int
    secretary_name: str


@dataclass
class UpdateMeetingDateDTO:
    """DTO для обновления даты встречи"""
    solution_id: int
    new_date: date


@dataclass
class UpdateMeetingPlaceDTO:
    """DTO для обновления места встречи"""
    solution_id: int
    new_place: str


@dataclass
class UpdateDepartmentDTO:
    """DTO для обновления департамента"""
    solution_id: int
    department_name: str


@dataclass
class ApplicationSolutionDTO:
    """DTO для отображения решения по заявке"""
    id: int
    application_id: Optional[int]
    secretary_id: Optional[int]
    secretary_name: Optional[str]
    meeting_date: Optional[date]
    meeting_place: Optional[str]
    department_name: Optional[str]
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    meeting_status: Optional[str] = None
    days_until_meeting: Optional[int] = None
    is_complete: Optional[bool] = None
    has_meeting_scheduled: Optional[bool] = None


@dataclass
class ApplicationSolutionListDTO:
    """DTO для списка решений с пагинацией"""
    solutions: List[ApplicationSolutionDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class ApplicationSolutionWithRelationsDTO(ApplicationSolutionDTO):
    """DTO решения с связанными данными"""
    application_title: Optional[str] = None
    application_user: Optional[str] = None
    application_club: Optional[str] = None
    secretary_full_name: Optional[str] = None
    secretary_email: Optional[str] = None


@dataclass
class ApplicationSolutionShortDTO:
    """Краткая информация о решении"""
    id: int
    application_id: Optional[int]
    secretary_name: Optional[str]
    meeting_date: Optional[date]
    meeting_status: str


@dataclass
class ApplicationSolutionFilterDTO:
    """DTO для фильтрации решений"""
    application_id: Optional[int] = None
    secretary_id: Optional[int] = None
    department_name: Optional[str] = None
    meeting_date_from: Optional[date] = None
    meeting_date_to: Optional[date] = None
    meeting_status: Optional[str] = None  # not_scheduled, past, today, upcoming
    has_meeting: Optional[bool] = None


@dataclass
class ApplicationSolutionStatsDTO:
    """DTO для статистики решений"""
    total_solutions: int
    with_scheduled_meetings: int
    past_meetings: int
    upcoming_meetings: int
    today_meetings: int
    by_secretary: dict[int, int]  # {secretary_id: count}
    by_department: dict[str, int]  # {department_name: count}


@dataclass
class BulkScheduleMeetingsDTO:
    """DTO для массового назначения встреч"""
    solution_ids: List[int]
    meeting_date: date
    meeting_place: str
    department_name: Optional[str] = None


@dataclass
class BulkSetSecretaryDTO:
    """DTO для массового назначения секретаря"""
    solution_ids: List[int]
    secretary_id: int
    secretary_name: str


@dataclass
class BulkCancelMeetingsDTO:
    """DTO для массовой отмены встреч"""
    solution_ids: List[int]
    cancelled_by_id: int
    reason: Optional[str] = None


@dataclass
class SolutionsByMeetingDateDTO:
    """DTO для группировки решений по дате встречи"""
    meeting_date: date
    solutions: List[ApplicationSolutionShortDTO]
    count: int


@dataclass
class SolutionsBySecretaryDTO:
    """DTO для группировки решений по секретарю"""
    secretary_id: int
    secretary_name: str
    solutions: List[ApplicationSolutionShortDTO]
    count: int


@dataclass
class SolutionsByDepartmentDTO:
    """DTO для группировки решений по департаменту"""
    department_name: str
    solutions: List[ApplicationSolutionShortDTO]
    count: int


@dataclass
class MeetingScheduleDTO:
    """DTO для расписания встреч"""
    by_date: List[SolutionsByMeetingDateDTO]
    total_meetings: int
    upcoming_meetings: int
    past_meetings: int


@dataclass
class SolutionValidationResultDTO:
    """DTO для результата валидации решения"""
    solution_id: int
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    is_complete: bool


@dataclass
class MeetingReminderDTO:
    """DTO для напоминания о встрече"""
    solution_id: int
    application_id: int
    meeting_date: date
    meeting_place: str
    secretary_id: int
    secretary_name: str
    days_until: int
    urgency_level: str  # critical, warning, normal


@dataclass
class SolutionSummaryDTO:
    """DTO для сводки по решению"""
    solution_id: int
    application_id: int
    secretary_name: Optional[str]
    meeting_date: Optional[date]
    meeting_place: Optional[str]
    department_name: Optional[str]
    meeting_status: str
    is_ready_for_decision: bool


@dataclass
class UpcomingMeetingsReportDTO:
    """DTO для отчета по предстоящим встречам"""
    upcoming_today: List[ApplicationSolutionShortDTO]
    upcoming_this_week: List[ApplicationSolutionShortDTO]
    upcoming_this_month: List[ApplicationSolutionShortDTO]
    total_upcoming: int


@dataclass
class PastMeetingsReportDTO:
    """DTO для отчета по прошедшим встречам"""
    past_meetings: List[ApplicationSolutionWithRelationsDTO]
    total_past: int
    by_department: dict[str, int]
    by_secretary: dict[str, int]


@dataclass
class SolutionExportDTO:
    """DTO для экспорта решений"""
    solutions: List[ApplicationSolutionWithRelationsDTO]
    export_format: str  # csv, excel, pdf
    filters_applied: ApplicationSolutionFilterDTO
    generated_at: datetime


@dataclass
class MeetingConflictCheckDTO:
    """DTO для проверки конфликтов встреч"""
    meeting_date: date
    secretary_id: int
    conflicting_solutions: List[int]  # IDs решений с конфликтами
    has_conflicts: bool
