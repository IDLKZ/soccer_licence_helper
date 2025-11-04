"""
Data Transfer Objects for ApplicationStatusCategory
DTO для передачи данных категории статуса заявки между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CreateApplicationStatusCategoryDTO:
    """DTO для создания категории статуса заявки"""
    title_ru: str
    title_kk: str
    value: str
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    cat_previous_id: Optional[int] = None
    cat_next_id: Optional[int] = None
    role_values: Optional[List[str]] = None
    is_active: bool = True


@dataclass
class UpdateApplicationStatusCategoryDTO:
    """DTO для обновления категории статуса заявки"""
    category_id: int
    title_ru: Optional[str] = None
    title_kk: Optional[str] = None
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None
    value: Optional[str] = None
    cat_previous_id: Optional[int] = None
    cat_next_id: Optional[int] = None
    role_values: Optional[List[str]] = None
    is_active: Optional[bool] = None


@dataclass
class SetPreviousCategoryDTO:
    """DTO для установки предыдущей категории в workflow"""
    category_id: int
    previous_category_id: Optional[int]


@dataclass
class SetNextCategoryDTO:
    """DTO для установки следующей категории в workflow"""
    category_id: int
    next_category_id: Optional[int]


@dataclass
class LinkCategoriesDTO:
    """DTO для связывания категорий в workflow"""
    from_category_id: int
    to_category_id: int


@dataclass
class UnlinkCategoryDTO:
    """DTO для отвязывания категории от workflow"""
    category_id: int


@dataclass
class UpdateCategoryRolesDTO:
    """DTO для обновления ролей категории"""
    category_id: int
    role_values: List[str]


@dataclass
class AddRoleToCategoryDTO:
    """DTO для добавления роли к категории"""
    category_id: int
    role_value: str


@dataclass
class RemoveRoleFromCategoryDTO:
    """DTO для удаления роли из категории"""
    category_id: int
    role_value: str


@dataclass
class ApplicationStatusCategoryTranslationDTO:
    """DTO для переводов категории"""
    title_ru: str
    title_kk: str
    title_en: Optional[str] = None
    description_ru: Optional[str] = None
    description_kk: Optional[str] = None
    description_en: Optional[str] = None


@dataclass
class ApplicationStatusCategoryDTO:
    """DTO для отображения категории статуса заявки"""
    id: int
    title_ru: str
    title_kk: str
    title_en: Optional[str]
    description_ru: Optional[str]
    description_kk: Optional[str]
    description_en: Optional[str]
    value: str
    cat_previous_id: Optional[int]
    cat_next_id: Optional[int]
    role_values: List[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    workflow_position: Optional[str] = None  # first, middle, last, standalone
    has_previous: Optional[bool] = None
    has_next: Optional[bool] = None
    roles_count: Optional[int] = None


@dataclass
class ApplicationStatusCategoryListDTO:
    """DTO для списка категорий с пагинацией"""
    categories: List[ApplicationStatusCategoryDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class ApplicationStatusCategoryWithRelationsDTO(ApplicationStatusCategoryDTO):
    """DTO категории с информацией о связанных категориях"""
    previous_category_title: Optional[str] = None
    next_category_title: Optional[str] = None
    applications_count: Optional[int] = None


@dataclass
class ApplicationStatusCategoryShortDTO:
    """Краткая информация о категории"""
    id: int
    title_ru: str
    title_kk: str
    value: str
    is_active: bool
    workflow_position: str


@dataclass
class ApplicationStatusCategoryLocalizedDTO:
    """DTO для отображения категории на определенном языке"""
    id: int
    title: str
    description: Optional[str]
    value: str
    workflow_position: str
    is_active: bool
    language: str  # ru, kk, en


@dataclass
class ApplicationStatusCategoryFilterDTO:
    """DTO для фильтрации категорий"""
    is_active: Optional[bool] = None
    has_previous: Optional[bool] = None
    has_next: Optional[bool] = None
    workflow_position: Optional[str] = None
    role_value: Optional[str] = None
    search_query: Optional[str] = None


@dataclass
class WorkflowChainDTO:
    """DTO для цепочки категорий в workflow"""
    categories: List[ApplicationStatusCategoryShortDTO]
    total_steps: int
    start_category: Optional[ApplicationStatusCategoryShortDTO]
    end_category: Optional[ApplicationStatusCategoryShortDTO]


@dataclass
class CategoryTransitionDTO:
    """DTO для перехода между категориями"""
    from_category_id: int
    to_category_id: int
    is_valid: bool
    can_transition: bool


@dataclass
class CategoryAccessCheckDTO:
    """DTO для проверки доступа к категории по роли"""
    category_id: int
    role_value: str
    has_access: bool


@dataclass
class BulkActivateCategoriesDTO:
    """DTO для массовой активации категорий"""
    category_ids: List[int]


@dataclass
class BulkDeactivateCategoriesDTO:
    """DTO для массовой деактивации категорий"""
    category_ids: List[int]


@dataclass
class BulkUpdateCategoryRolesDTO:
    """DTO для массового обновления ролей категорий"""
    category_ids: List[int]
    role_values: List[str]


@dataclass
class WorkflowValidationResultDTO:
    """DTO для результата валидации workflow"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    has_cycles: bool
    orphaned_categories: List[int]


@dataclass
class CategoryWorkflowPathDTO:
    """DTO для пути от одной категории к другой в workflow"""
    from_category_id: int
    to_category_id: int
    path: List[int]  # IDs категорий в пути
    path_length: int
    is_reachable: bool


@dataclass
class CategoryStatsDTO:
    """DTO для статистики категории"""
    category_id: int
    total_applications: int
    active_applications: int
    completed_applications: int
    average_time_in_category: Optional[float] = None  # В днях


@dataclass
class WorkflowDiagramDTO:
    """DTO для диаграммы workflow"""
    nodes: List[ApplicationStatusCategoryShortDTO]
    edges: List[dict]  # [{from_id, to_id}]
    total_nodes: int
    total_edges: int


@dataclass
class ReorderWorkflowDTO:
    """DTO для переупорядочивания категорий в workflow"""
    category_chain: List[int]  # Упорядоченный список ID категорий


@dataclass
class CategoryHistoryDTO:
    """DTO для истории изменений категории"""
    category_id: int
    changes: List[dict]  # [{timestamp, field, old_value, new_value, user_id}]


@dataclass
class WorkflowConfigDTO:
    """DTO для конфигурации workflow"""
    workflow_name: str
    categories: List[ApplicationStatusCategoryDTO]
    start_category_id: int
    end_category_ids: List[int]
    total_steps: int


@dataclass
class CategoryExportDTO:
    """DTO для экспорта категорий"""
    categories: List[ApplicationStatusCategoryWithRelationsDTO]
    export_format: str  # csv, excel, pdf, json
    include_workflow: bool
    generated_at: datetime
