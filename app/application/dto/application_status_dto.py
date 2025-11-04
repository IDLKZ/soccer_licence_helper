"""
Data Transfer Objects for ApplicationStatus
DTO для передачи данных статуса заявки между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CreateApplicationStatusDTO:
    """DTO для создания статуса заявки"""
    title_ru: str
    title_kk: str
    category_id: int
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    previous_id: Optional[int] = None
    next_id: Optional[int] = None


@dataclass
class UpdateApplicationStatusDTO:
    """DTO для обновления статуса заявки"""
    status_id: int
    title_ru: Optional[str] = None
    title_kk: Optional[str] = None
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    category_id: Optional[int] = None
    previous_id: Optional[int] = None
    next_id: Optional[int] = None


@dataclass
class SetStatusCategoryDTO:
    """DTO для установки категории статуса"""
    status_id: int
    category_id: int


@dataclass
class SetPreviousStatusDTO:
    """DTO для установки предыдущего статуса в workflow"""
    status_id: int
    previous_status_id: Optional[int]


@dataclass
class SetNextStatusDTO:
    """DTO для установки следующего статуса в workflow"""
    status_id: int
    next_status_id: Optional[int]


@dataclass
class LinkStatusesDTO:
    """DTO для связывания статусов в workflow"""
    from_status_id: int
    to_status_id: int


@dataclass
class UnlinkStatusDTO:
    """DTO для отвязывания статуса от workflow"""
    status_id: int


@dataclass
class ApplicationStatusTranslationDTO:
    """DTO для переводов статуса"""
    title_ru: str
    title_kk: str
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None


@dataclass
class ApplicationStatusDTO:
    """DTO для отображения статуса заявки"""
    id: int
    category_id: Optional[int]
    previous_id: Optional[int]
    next_id: Optional[int]
    title_ru: str
    title_kk: str
    title_en: Optional[str]
    description_ru: Optional[str]
    description_kk: Optional[str]
    description_en: Optional[str]
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    workflow_position: Optional[str] = None  # first, middle, last, standalone
    has_previous: Optional[bool] = None
    has_next: Optional[bool] = None


@dataclass
class ApplicationStatusListDTO:
    """DTO для списка статусов с пагинацией"""
    statuses: List[ApplicationStatusDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class ApplicationStatusWithRelationsDTO(ApplicationStatusDTO):
    """DTO статуса с информацией о связанных статусах"""
    category_title: Optional[str] = None
    previous_status_title: Optional[str] = None
    next_status_title: Optional[str] = None
    applications_count: Optional[int] = None


@dataclass
class ApplicationStatusShortDTO:
    """Краткая информация о статусе"""
    id: int
    title_ru: str
    title_kk: str
    category_id: Optional[int]
    workflow_position: str


@dataclass
class ApplicationStatusLocalizedDTO:
    """DTO для отображения статуса на определенном языке"""
    id: int
    title: str
    description: Optional[str]
    category_id: Optional[int]
    workflow_position: str
    language: str  # ru, kk, en


@dataclass
class ApplicationStatusFilterDTO:
    """DTO для фильтрации статусов"""
    category_id: Optional[int] = None
    has_previous: Optional[bool] = None
    has_next: Optional[bool] = None
    workflow_position: Optional[str] = None
    search_query: Optional[str] = None


@dataclass
class StatusWorkflowChainDTO:
    """DTO для цепочки статусов в workflow"""
    category_id: int
    statuses: List[ApplicationStatusShortDTO]
    total_steps: int
    start_status: Optional[ApplicationStatusShortDTO]
    end_status: Optional[ApplicationStatusShortDTO]


@dataclass
class StatusTransitionDTO:
    """DTO для перехода между статусами"""
    from_status_id: int
    to_status_id: int
    is_valid: bool
    can_transition: bool


@dataclass
class StatusesByCategoryDTO:
    """DTO для группировки статусов по категориям"""
    category_id: int
    category_title: str
    statuses: List[ApplicationStatusShortDTO]
    count: int


@dataclass
class BulkMoveToCategoryDTO:
    """DTO для массового переноса статусов в категорию"""
    status_ids: List[int]
    category_id: int


@dataclass
class StatusWorkflowValidationResultDTO:
    """DTO для результата валидации workflow статусов"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    has_cycles: bool
    orphaned_statuses: List[int]


@dataclass
class StatusWorkflowPathDTO:
    """DTO для пути от одного статуса к другому в workflow"""
    from_status_id: int
    to_status_id: int
    path: List[int]  # IDs статусов в пути
    path_length: int
    is_reachable: bool


@dataclass
class StatusStatsDTO:
    """DTO для статистики статуса"""
    status_id: int
    total_applications: int
    active_applications: int
    average_time_in_status: Optional[float] = None  # В днях


@dataclass
class StatusWorkflowDiagramDTO:
    """DTO для диаграммы workflow статусов"""
    category_id: int
    nodes: List[ApplicationStatusShortDTO]
    edges: List[dict]  # [{from_id, to_id}]
    total_nodes: int
    total_edges: int


@dataclass
class ReorderStatusWorkflowDTO:
    """DTO для переупорядочивания статусов в workflow"""
    category_id: int
    status_chain: List[int]  # Упорядоченный список ID статусов


@dataclass
class StatusHistoryDTO:
    """DTO для истории изменений статуса"""
    status_id: int
    changes: List[dict]  # [{timestamp, field, old_value, new_value, user_id}]


@dataclass
class CategoryStatusMapDTO:
    """DTO для карты статусов по категориям"""
    categories: List[StatusesByCategoryDTO]
    total_categories: int
    total_statuses: int


@dataclass
class StatusDisplayInfoDTO:
    """DTO для информации отображения статуса"""
    id: int
    title: str
    description: Optional[str]
    category_id: Optional[int]
    workflow_position: str
    has_previous: bool
    has_next: bool


@dataclass
class StatusTransitionHistoryDTO:
    """DTO для истории переходов между статусами"""
    application_id: int
    transitions: List[dict]  # [{from_status_id, to_status_id, timestamp, user_id}]


@dataclass
class StatusExportDTO:
    """DTO для экспорта статусов"""
    statuses: List[ApplicationStatusWithRelationsDTO]
    export_format: str  # csv, excel, pdf, json
    include_workflow: bool
    generated_at: datetime


@dataclass
class ValidateStatusTransitionDTO:
    """DTO для валидации перехода статуса"""
    from_status_id: int
    to_status_id: int
    is_valid: bool
    error_message: Optional[str] = None
