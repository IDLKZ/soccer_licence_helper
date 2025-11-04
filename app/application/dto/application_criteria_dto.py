"""
Data Transfer Objects for ApplicationCriteria
DTO для передачи данных критерия заявки между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CreateApplicationCriteriaDTO:
    """DTO для создания критерия заявки"""
    application_id: int
    category_id: int
    status_id: Optional[int] = None
    is_ready: bool = False


@dataclass
class UpdateApplicationCriteriaDTO:
    """DTO для обновления критерия заявки"""
    criteria_id: int
    application_id: Optional[int] = None
    category_id: Optional[int] = None
    status_id: Optional[int] = None
    is_ready: Optional[bool] = None


@dataclass
class MarkAsUploadedDTO:
    """DTO для отметки загрузки документа"""
    criteria_id: int
    uploaded_by_id: int
    uploaded_by_info: str


@dataclass
class MarkFirstCheckDTO:
    """DTO для отметки первичной проверки"""
    criteria_id: int
    checked_by_id: int
    checked_by_info: str
    passed: bool


@dataclass
class MarkIndustryCheckDTO:
    """DTO для отметки индустриальной проверки"""
    criteria_id: int
    checked_by_id: int
    checked_by_info: str
    passed: bool


@dataclass
class MarkControlCheckDTO:
    """DTO для отметки контрольной проверки"""
    criteria_id: int
    checked_by_id: int
    checked_by_info: str
    passed: bool


@dataclass
class EnableReuploadDTO:
    """DTO для разрешения перезагрузки"""
    criteria_id: int
    document_ids: Optional[List[int]] = None


@dataclass
class DisableReuploadDTO:
    """DTO для запрета перезагрузки"""
    criteria_id: int


@dataclass
class AddReuploadableDocumentDTO:
    """DTO для добавления документа в список перезагрузки"""
    criteria_id: int
    document_id: int


@dataclass
class RemoveReuploadableDocumentDTO:
    """DTO для удаления документа из списка перезагрузки"""
    criteria_id: int
    document_id: int


@dataclass
class ApplicationCriteriaDTO:
    """DTO для отображения критерия заявки"""
    id: int
    application_id: Optional[int]
    category_id: Optional[int]
    status_id: Optional[int]

    # Upload info
    uploaded_by_id: Optional[int]
    uploaded_by: Optional[str]

    # First check info
    first_checked_by_id: Optional[int]
    first_checked_by: Optional[str]

    # Regular check info
    checked_by_id: Optional[int]
    checked_by: Optional[str]

    # Control check info
    control_checked_by_id: Optional[int]
    control_checked_by: Optional[str]

    # Status flags
    is_ready: bool
    is_first_passed: Optional[bool]
    is_industry_passed: Optional[bool]
    is_final_passed: Optional[bool]
    can_reupload_after_ending: Optional[bool]
    can_reupload_after_endings_doc_ids: List[int]

    created_at: datetime
    updated_at: datetime

    # Дополнительные вычисляемые поля
    current_stage: Optional[str] = None
    next_stage: Optional[str] = None
    completion_percentage: Optional[float] = None
    is_fully_passed: Optional[bool] = None


@dataclass
class ApplicationCriteriaListDTO:
    """DTO для списка критериев с пагинацией"""
    criteria: List[ApplicationCriteriaDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class ApplicationCriteriaWithRelationsDTO(ApplicationCriteriaDTO):
    """DTO критерия с связанными данными"""
    application_title: Optional[str] = None
    category_title: Optional[str] = None
    status_title: Optional[str] = None
    uploaded_by_user: Optional[str] = None
    first_checked_by_user: Optional[str] = None
    checked_by_user: Optional[str] = None
    control_checked_by_user: Optional[str] = None


@dataclass
class ApplicationCriteriaShortDTO:
    """Краткая информация о критерии"""
    id: int
    application_id: Optional[int]
    category_id: Optional[int]
    status_id: Optional[int]
    is_ready: bool
    is_fully_passed: bool
    completion_percentage: float


@dataclass
class ApplicationCriteriaFilterDTO:
    """DTO для фильтрации критериев"""
    application_id: Optional[int] = None
    category_id: Optional[int] = None
    status_id: Optional[int] = None
    is_ready: Optional[bool] = None
    is_first_passed: Optional[bool] = None
    is_industry_passed: Optional[bool] = None
    is_final_passed: Optional[bool] = None
    uploaded_by_id: Optional[int] = None
    checked_by_id: Optional[int] = None
    can_reupload: Optional[bool] = None


@dataclass
class ApplicationCriteriaStatsDTO:
    """DTO для статистики критериев"""
    total_criteria: int
    ready_criteria: int
    fully_passed: int
    partially_passed: int
    failed: int
    pending_first_check: int
    pending_industry_check: int
    pending_control_check: int
    average_completion: float


@dataclass
class CheckHistoryDTO:
    """DTO для истории проверок критерия"""
    criteria_id: int
    upload_info: Optional[dict] = None  # {user_id, user_name, timestamp}
    first_check_info: Optional[dict] = None
    industry_check_info: Optional[dict] = None
    control_check_info: Optional[dict] = None


@dataclass
class BulkMarkAsReadyDTO:
    """DTO для массовой отметки как готовые"""
    criteria_ids: List[int]


@dataclass
class BulkResetChecksDTO:
    """DTO для массового сброса проверок"""
    criteria_ids: List[int]


@dataclass
class CriteriaByStageDTO:
    """DTO для группировки критериев по этапам"""
    stage: str
    stage_name: str
    criteria: List[ApplicationCriteriaShortDTO]
    count: int


@dataclass
class CriteriaProgressReportDTO:
    """DTO для отчета о прогрессе критериев"""
    by_stage: List[CriteriaByStageDTO]
    total_criteria: int
    completion_rate: float


@dataclass
class CanReuploadCheckDTO:
    """DTO для проверки возможности перезагрузки"""
    criteria_id: int
    document_id: int
    can_reupload: bool
    reason: Optional[str] = None


@dataclass
class CriteriaValidationResultDTO:
    """DTO для результата валидации критерия"""
    criteria_id: int
    is_valid: bool
    errors: List[str]
    warnings: List[str]


@dataclass
class UpdateCriteriaStatusDTO:
    """DTO для обновления статуса критерия"""
    criteria_id: int
    status_id: int
    updated_by_id: int
    comment: Optional[str] = None


@dataclass
class CriteriaCheckSummaryDTO:
    """DTO для сводки по проверкам критерия"""
    criteria_id: int
    total_checks: int
    passed_checks: int
    failed_checks: int
    pending_checks: int
    can_proceed: bool
    next_action: Optional[str] = None
