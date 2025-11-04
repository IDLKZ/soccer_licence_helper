"""
Data Transfer Objects for ApplicationDocument
DTO для передачи данных документа заявки между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CreateApplicationDocumentDTO:
    """DTO для создания документа заявки"""
    file_url: str
    title: str
    application_id: int
    category_id: Optional[int] = None
    document_id: Optional[int] = None
    info: Optional[str] = None
    deadline: Optional[datetime] = None


@dataclass
class UpdateApplicationDocumentDTO:
    """DTO для обновления документа заявки"""
    document_id: int
    file_url: Optional[str] = None
    title: Optional[str] = None
    info: Optional[str] = None
    application_id: Optional[int] = None
    category_id: Optional[int] = None
    deadline: Optional[datetime] = None


@dataclass
class UploadDocumentDTO:
    """DTO для загрузки документа"""
    document_id: int
    file_url: str
    uploaded_by_id: int
    uploaded_by_info: str


@dataclass
class MarkFirstCheckDocumentDTO:
    """DTO для первичной проверки документа"""
    document_id: int
    checked_by_id: int
    checked_by_info: str
    passed: bool
    comment: Optional[str] = None


@dataclass
class MarkIndustryCheckDocumentDTO:
    """DTO для индустриальной проверки документа"""
    document_id: int
    checked_by_id: int
    checked_by_info: str
    passed: bool
    comment: Optional[str] = None


@dataclass
class MarkControlCheckDocumentDTO:
    """DTO для контрольной проверки документа"""
    document_id: int
    checked_by_id: int
    checked_by_info: str
    passed: bool
    comment: Optional[str] = None


@dataclass
class SetDeadlineDTO:
    """DTO для установки дедлайна"""
    document_id: int
    deadline: datetime


@dataclass
class ExtendDeadlineDTO:
    """DTO для продления дедлайна"""
    document_id: int
    days: int


@dataclass
class UpdateFileDTO:
    """DTO для обновления файла документа"""
    document_id: int
    file_url: str


@dataclass
class ApplicationDocumentDTO:
    """DTO для отображения документа заявки"""
    id: int
    application_id: Optional[int]
    category_id: Optional[int]
    document_id: Optional[int]
    file_url: str
    title: str
    info: Optional[str]

    # Upload info
    uploaded_by_id: Optional[int]
    uploaded_by: Optional[str]

    # First check
    first_checked_by_id: Optional[int]
    first_checked_by: Optional[str]
    first_comment: Optional[str]

    # Industry check
    checked_by_id: Optional[int]
    checked_by: Optional[str]
    industry_comment: Optional[str]

    # Control check
    control_checked_by_id: Optional[int]
    control_checked_by: Optional[str]
    control_comment: Optional[str]

    # Status flags
    is_first_passed: Optional[bool]
    is_industry_passed: Optional[bool]
    is_final_passed: Optional[bool]

    # Deadline
    deadline: Optional[datetime]

    created_at: datetime
    updated_at: datetime

    # Дополнительные вычисляемые поля
    current_stage: Optional[str] = None
    completion_percentage: Optional[float] = None
    is_overdue: Optional[bool] = None
    days_until_deadline: Optional[int] = None
    is_fully_passed: Optional[bool] = None


@dataclass
class ApplicationDocumentListDTO:
    """DTO для списка документов с пагинацией"""
    documents: List[ApplicationDocumentDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class ApplicationDocumentWithRelationsDTO(ApplicationDocumentDTO):
    """DTO документа с связанными данными"""
    application_title: Optional[str] = None
    category_title: Optional[str] = None
    document_title: Optional[str] = None
    uploaded_by_user: Optional[str] = None
    first_checked_by_user: Optional[str] = None
    checked_by_user: Optional[str] = None
    control_checked_by_user: Optional[str] = None


@dataclass
class ApplicationDocumentShortDTO:
    """Краткая информация о документе"""
    id: int
    application_id: Optional[int]
    title: str
    file_url: str
    is_fully_passed: bool
    is_overdue: bool
    deadline: Optional[datetime]


@dataclass
class ApplicationDocumentFilterDTO:
    """DTO для фильтрации документов"""
    application_id: Optional[int] = None
    category_id: Optional[int] = None
    document_id: Optional[int] = None
    uploaded_by_id: Optional[int] = None
    is_first_passed: Optional[bool] = None
    is_industry_passed: Optional[bool] = None
    is_final_passed: Optional[bool] = None
    is_overdue: Optional[bool] = None
    deadline_from: Optional[datetime] = None
    deadline_to: Optional[datetime] = None


@dataclass
class ApplicationDocumentStatsDTO:
    """DTO для статистики документов"""
    total_documents: int
    fully_passed: int
    partially_passed: int
    failed: int
    overdue: int
    pending_first_check: int
    pending_industry_check: int
    pending_control_check: int
    average_completion: float


@dataclass
class DocumentCheckCommentDTO:
    """DTO для комментария проверки"""
    stage: str
    comment: str
    checked_by: Optional[str]
    passed: Optional[bool]


@dataclass
class DocumentCheckHistoryDTO:
    """DTO для истории проверок документа"""
    document_id: int
    title: str
    upload_info: Optional[dict] = None
    checks: List[DocumentCheckCommentDTO] = None


@dataclass
class BulkResetChecksDocumentDTO:
    """DTO для массового сброса проверок"""
    document_ids: List[int]


@dataclass
class BulkSetDeadlineDTO:
    """DTO для массовой установки дедлайна"""
    document_ids: List[int]
    deadline: datetime


@dataclass
class DocumentsByStageDTO:
    """DTO для группировки документов по этапам"""
    stage: str
    stage_name: str
    documents: List[ApplicationDocumentShortDTO]
    count: int


@dataclass
class DocumentProgressReportDTO:
    """DTO для отчета о прогрессе документов"""
    by_stage: List[DocumentsByStageDTO]
    total_documents: int
    completion_rate: float


@dataclass
class OverdueDocumentsReportDTO:
    """DTO для отчета по просроченным документам"""
    overdue_documents: List[ApplicationDocumentShortDTO]
    total_overdue: int
    by_application: dict[int, int]  # {application_id: count}


@dataclass
class DocumentValidationResultDTO:
    """DTO для результата валидации документа"""
    document_id: int
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    can_proceed: bool


@dataclass
class ReplaceDocumentFileDTO:
    """DTO для замены файла документа"""
    document_id: int
    new_file_url: str
    replaced_by_id: int
    reason: Optional[str] = None


@dataclass
class DocumentCheckSummaryDTO:
    """DTO для сводки по проверкам документа"""
    document_id: int
    title: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    pending_checks: int
    failed_stages: List[str]
    needs_review: bool


@dataclass
class ApplicationDocumentsGroupedDTO:
    """DTO для группировки документов заявки по категориям"""
    application_id: int
    by_category: dict[int, List[ApplicationDocumentShortDTO]]
    total_documents: int
    completed_documents: int


@dataclass
class UpdateDocumentCommentDTO:
    """DTO для обновления комментария проверки"""
    document_id: int
    stage: str  # first_check, industry_check, control_check
    comment: str


@dataclass
class DocumentDeadlineAlertDTO:
    """DTO для оповещения о дедлайне документа"""
    document_id: int
    title: str
    deadline: datetime
    days_remaining: int
    application_id: int
    urgency_level: str  # critical, warning, normal
