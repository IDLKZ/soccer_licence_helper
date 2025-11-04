"""
Data Transfer Objects for Application
DTO для передачи данных заявки между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CreateApplicationDTO:
    """DTO для создания заявки"""
    user_id: int
    license_id: int
    club_id: int
    category_id: Optional[int] = None
    is_ready: bool = False
    is_active: Optional[bool] = None


@dataclass
class UpdateApplicationDTO:
    """DTO для обновления заявки"""
    application_id: int
    user_id: Optional[int] = None
    license_id: Optional[int] = None
    club_id: Optional[int] = None
    category_id: Optional[int] = None
    is_ready: Optional[bool] = None
    is_active: Optional[bool] = None


@dataclass
class MarkApplicationReadyDTO:
    """DTO для отметки заявки как готовой"""
    application_id: int


@dataclass
class SubmitApplicationDTO:
    """DTO для отправки заявки на рассмотрение"""
    application_id: int
    submitted_by_id: int


@dataclass
class ActivateApplicationDTO:
    """DTO для активации заявки"""
    application_id: int


@dataclass
class DeactivateApplicationDTO:
    """DTO для деактивации заявки"""
    application_id: int


@dataclass
class CancelApplicationDTO:
    """DTO для отмены заявки"""
    application_id: int
    reason: Optional[str] = None


@dataclass
class CloneApplicationDTO:
    """DTO для клонирования заявки"""
    application_id: int
    new_license_id: int


@dataclass
class ApplicationDTO:
    """DTO для отображения заявки"""
    id: int
    user_id: Optional[int]
    license_id: Optional[int]
    club_id: Optional[int]
    category_id: Optional[int]
    is_ready: bool
    is_active: Optional[bool]
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    status_summary: Optional[str] = None
    can_be_submitted: Optional[bool] = None
    can_be_edited: Optional[bool] = None
    has_required_data: Optional[bool] = None


@dataclass
class ApplicationListDTO:
    """DTO для списка заявок с пагинацией"""
    applications: List[ApplicationDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class ApplicationWithRelationsDTO(ApplicationDTO):
    """DTO заявки с связанными данными"""
    user_name: Optional[str] = None
    user_email: Optional[str] = None
    license_title: Optional[str] = None
    license_start: Optional[str] = None
    license_end: Optional[str] = None
    club_name: Optional[str] = None
    category_name: Optional[str] = None


@dataclass
class ApplicationWithCriteriaDTO(ApplicationWithRelationsDTO):
    """DTO заявки с критериями"""
    total_criteria: Optional[int] = None
    completed_criteria: Optional[int] = None
    pending_criteria: Optional[int] = None
    criteria_completion_percentage: Optional[float] = None


@dataclass
class ApplicationShortDTO:
    """Краткая информация о заявке"""
    id: int
    user_id: Optional[int]
    license_id: Optional[int]
    club_id: Optional[int]
    is_ready: bool
    is_active: Optional[bool]
    status_summary: str


@dataclass
class ApplicationFilterDTO:
    """DTO для фильтрации заявок"""
    user_id: Optional[int] = None
    license_id: Optional[int] = None
    club_id: Optional[int] = None
    category_id: Optional[int] = None
    is_ready: Optional[bool] = None
    is_active: Optional[bool] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None


@dataclass
class ApplicationStatsDTO:
    """DTO для статистики заявок"""
    total_applications: int
    ready_applications: int
    active_applications: int
    inactive_applications: int
    pending_applications: int
    by_license: Optional[dict[int, int]] = None  # {license_id: count}
    by_club: Optional[dict[int, int]] = None  # {club_id: count}
    by_user: Optional[dict[int, int]] = None  # {user_id: count}


@dataclass
class ApplicationValidationResultDTO:
    """DTO для результата валидации заявки"""
    application_id: int
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    can_submit: bool


@dataclass
class BulkActivateApplicationsDTO:
    """DTO для массовой активации заявок"""
    application_ids: List[int]


@dataclass
class BulkDeactivateApplicationsDTO:
    """DTO для массовой деактивации заявок"""
    application_ids: List[int]


@dataclass
class BulkMarkAsReadyDTO:
    """DTO для массовой отметки как готовые"""
    application_ids: List[int]


@dataclass
class ApplicationsByStatusDTO:
    """DTO для группировки заявок по статусу"""
    status: str
    status_name: str
    applications: List[ApplicationShortDTO]
    count: int


@dataclass
class ApplicationProgressDTO:
    """DTO для прогресса заявки"""
    application_id: int
    total_steps: int
    completed_steps: int
    current_step: str
    completion_percentage: float
    next_action: Optional[str] = None


@dataclass
class ApplicationTimelineDTO:
    """DTO для таймлайна заявки"""
    application_id: int
    events: List[dict]  # [{timestamp, event_type, description, user_id}]


@dataclass
class ApplicationSummaryDTO:
    """DTO для сводки по заявке"""
    application_id: int
    user_name: str
    club_name: str
    license_title: str
    status: str
    is_ready: bool
    is_active: Optional[bool]
    total_criteria: int
    completed_criteria: int
    created_at: datetime
    updated_at: datetime


@dataclass
class UpdateApplicationCategoryDTO:
    """DTO для обновления категории заявки"""
    application_id: int
    category_id: int


@dataclass
class ApplicationReportDTO:
    """DTO для отчета по заявкам"""
    period_start: datetime
    period_end: datetime
    total_applications: int
    by_status: dict[str, int]
    by_license: dict[str, int]
    by_club: dict[str, int]
    completion_rate: float


@dataclass
class ApplicationExportDTO:
    """DTO для экспорта заявок"""
    applications: List[ApplicationWithRelationsDTO]
    export_format: str  # csv, excel, pdf
    filters_applied: ApplicationFilterDTO
