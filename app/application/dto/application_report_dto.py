"""
Data Transfer Objects for ApplicationReport
DTO для передачи данных отчета по критерию заявки между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CreateApplicationReportDTO:
    """DTO для создания отчета по критерию заявки"""
    application_id: int
    criteria_id: int
    status: int = 0  # PENDING by default


@dataclass
class UpdateApplicationReportDTO:
    """DTO для обновления отчета по критерию заявки"""
    report_id: int
    status: Optional[int] = None
    application_id: Optional[int] = None
    criteria_id: Optional[int] = None


@dataclass
class UpdateReportStatusDTO:
    """DTO для обновления статуса отчета"""
    report_id: int
    status: int


@dataclass
class TransitionReportStatusDTO:
    """DTO для перехода статуса с валидацией"""
    report_id: int
    new_status: int
    transition_by_id: Optional[int] = None
    comment: Optional[str] = None


@dataclass
class MarkReportAsPendingDTO:
    """DTO для отметки отчета как ожидающего"""
    report_id: int


@dataclass
class MarkReportAsInProgressDTO:
    """DTO для отметки отчета как в процессе"""
    report_id: int


@dataclass
class MarkReportAsCompletedDTO:
    """DTO для отметки отчета как завершенного"""
    report_id: int


@dataclass
class ApproveReportDTO:
    """DTO для одобрения отчета"""
    report_id: int
    approved_by_id: int
    comment: Optional[str] = None


@dataclass
class RejectReportDTO:
    """DTO для отклонения отчета"""
    report_id: int
    rejected_by_id: int
    reason: str


@dataclass
class RequestRevisionDTO:
    """DTO для запроса доработки отчета"""
    report_id: int
    requested_by_id: int
    revision_notes: str


@dataclass
class CancelReportDTO:
    """DTO для отмены отчета"""
    report_id: int
    cancelled_by_id: int
    reason: Optional[str] = None


@dataclass
class ApplicationReportDTO:
    """DTO для отображения отчета по критерию заявки"""
    id: int
    application_id: Optional[int]
    criteria_id: Optional[int]
    status: int
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    status_display: Optional[str] = None
    is_final: Optional[bool] = None
    can_be_edited: Optional[bool] = None


@dataclass
class ApplicationReportListDTO:
    """DTO для списка отчетов с пагинацией"""
    reports: List[ApplicationReportDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class ApplicationReportWithRelationsDTO(ApplicationReportDTO):
    """DTO отчета с связанными данными"""
    application_title: Optional[str] = None
    criteria_category: Optional[str] = None
    user_name: Optional[str] = None
    club_name: Optional[str] = None


@dataclass
class ApplicationReportShortDTO:
    """Краткая информация об отчете"""
    id: int
    application_id: Optional[int]
    criteria_id: Optional[int]
    status: int
    status_display: str


@dataclass
class ApplicationReportFilterDTO:
    """DTO для фильтрации отчетов"""
    application_id: Optional[int] = None
    criteria_id: Optional[int] = None
    status: Optional[int] = None
    status_list: Optional[List[int]] = None
    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None


@dataclass
class ApplicationReportStatsDTO:
    """DTO для статистики отчетов"""
    total_reports: int
    by_status: dict[int, int]  # {status: count}
    pending_reports: int
    in_progress_reports: int
    completed_reports: int
    approved_reports: int
    rejected_reports: int
    requires_revision_reports: int
    cancelled_reports: int


@dataclass
class BulkUpdateReportStatusDTO:
    """DTO для массового обновления статуса отчетов"""
    report_ids: List[int]
    new_status: int


@dataclass
class BulkApproveReportsDTO:
    """DTO для массового одобрения отчетов"""
    report_ids: List[int]
    approved_by_id: int


@dataclass
class BulkRejectReportsDTO:
    """DTO для массового отклонения отчетов"""
    report_ids: List[int]
    rejected_by_id: int
    reason: str


@dataclass
class ReportsByStatusDTO:
    """DTO для группировки отчетов по статусам"""
    status: int
    status_display: str
    reports: List[ApplicationReportShortDTO]
    count: int


@dataclass
class ReportStatusDistributionDTO:
    """DTO для распределения отчетов по статусам"""
    by_status: List[ReportsByStatusDTO]
    total_reports: int


@dataclass
class ReportValidationResultDTO:
    """DTO для результата валидации отчета"""
    report_id: int
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    can_transition_to: List[int]  # Список доступных статусов для перехода


@dataclass
class ReportTransitionHistoryDTO:
    """DTO для истории переходов статусов отчета"""
    report_id: int
    transitions: List[dict]  # [{from_status, to_status, timestamp, user_id, comment}]


@dataclass
class ReportsByApplicationDTO:
    """DTO для группировки отчетов по заявкам"""
    application_id: int
    application_title: Optional[str]
    reports: List[ApplicationReportShortDTO]
    total_reports: int
    completed_reports: int
    approved_reports: int


@dataclass
class ReportsByCriteriaDTO:
    """DTO для группировки отчетов по критериям"""
    criteria_id: int
    criteria_category: Optional[str]
    reports: List[ApplicationReportShortDTO]
    count: int


@dataclass
class ReportProgressDTO:
    """DTO для прогресса отчета"""
    report_id: int
    current_status: int
    current_status_display: str
    is_final: bool
    next_possible_statuses: List[int]
    completion_percentage: float


@dataclass
class ReportSummaryDTO:
    """DTO для сводки по отчету"""
    report_id: int
    application_id: Optional[int]
    criteria_id: Optional[int]
    status: int
    status_display: str
    created_at: datetime
    updated_at: datetime
    is_editable: bool
    is_approvable: bool


@dataclass
class ReportExportDTO:
    """DTO для экспорта отчетов"""
    reports: List[ApplicationReportWithRelationsDTO]
    export_format: str  # csv, excel, pdf
    filters_applied: ApplicationReportFilterDTO
    generated_at: datetime


@dataclass
class ResetReportDTO:
    """DTO для сброса отчета"""
    report_id: int
    reset_by_id: int
