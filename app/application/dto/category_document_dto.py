"""
Data Transfer Objects for CategoryDocument
DTO для передачи данных категории документов между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CreateCategoryDocumentDTO:
    """DTO для создания категории документов"""
    title_ru: str
    title_kk: str
    value: str
    level: int
    title_en: Optional[str] = None
    roles: Optional[List[int]] = None


@dataclass
class UpdateCategoryDocumentDTO:
    """DTO для обновления категории документов"""
    category_id: int
    title_ru: Optional[str] = None
    title_kk: Optional[str] = None
    title_en: Optional[str] = None
    value: Optional[str] = None
    level: Optional[int] = None
    roles: Optional[List[int]] = None


@dataclass
class UpdateCategoryLevelDTO:
    """DTO для обновления уровня категории"""
    category_id: int
    level: int


@dataclass
class UpdateCategoryRolesDTO:
    """DTO для обновления ролей категории"""
    category_id: int
    roles: List[int]


@dataclass
class AddRoleToCategoryDTO:
    """DTO для добавления роли к категории"""
    category_id: int
    role_id: int


@dataclass
class RemoveRoleFromCategoryDTO:
    """DTO для удаления роли из категории"""
    category_id: int
    role_id: int


@dataclass
class CategoryDocumentTranslationDTO:
    """DTO для переводов категории"""
    title_ru: str
    title_kk: str
    title_en: Optional[str] = None


@dataclass
class CategoryDocumentDTO:
    """DTO для отображения категории документов"""
    id: int
    title_ru: str
    title_kk: str
    title_en: Optional[str]
    value: str
    level: int
    roles: List[int]
    created_at: datetime
    updated_at: datetime
    # Дополнительные вычисляемые поля
    is_root_level: Optional[bool] = None
    level_name: Optional[str] = None
    roles_count: Optional[int] = None


@dataclass
class CategoryDocumentListDTO:
    """DTO для списка категорий с пагинацией"""
    categories: List[CategoryDocumentDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class CategoryDocumentWithAccessDTO(CategoryDocumentDTO):
    """DTO категории с информацией о доступе"""
    role_names: Optional[List[str]] = None
    is_public: Optional[bool] = None  # True если roles пустой


@dataclass
class CategoryDocumentShortDTO:
    """Краткая информация о категории"""
    id: int
    title_ru: str
    title_kk: str
    value: str
    level: int
    roles_count: int


@dataclass
class CategoryDocumentLocalizedDTO:
    """DTO для отображения категории на определенном языке"""
    id: int
    title: str
    value: str
    level: int
    level_name: str
    roles: List[int]
    language: str  # ru, kk, en


@dataclass
class CategoryDocumentFilterDTO:
    """DTO для фильтрации категорий"""
    level: Optional[int] = None
    min_level: Optional[int] = None
    max_level: Optional[int] = None
    role_id: Optional[int] = None  # Фильтр по роли
    has_roles: Optional[bool] = None  # Есть ли роли
    search_query: Optional[str] = None  # Поиск по названию или value


@dataclass
class CategoryDocumentsByLevelDTO:
    """DTO для группировки категорий по уровням"""
    level: int
    level_name: str
    categories: List[CategoryDocumentShortDTO]
    count: int


@dataclass
class CategoryDocumentHierarchyDTO:
    """DTO для иерархической структуры категорий"""
    levels: List[CategoryDocumentsByLevelDTO]
    total_categories: int
    total_levels: int


@dataclass
class CategoryDocumentTreeNodeDTO:
    """DTO для узла дерева категорий"""
    id: int
    title_ru: str
    title_kk: str
    title_en: Optional[str]
    value: str
    level: int
    roles: List[int]
    children: Optional[List['CategoryDocumentTreeNodeDTO']] = None
    parent_id: Optional[int] = None


@dataclass
class CategoryDocumentTreeDTO:
    """DTO для дерева категорий"""
    root_categories: List[CategoryDocumentTreeNodeDTO]
    total_categories: int
    max_depth: int


@dataclass
class BulkUpdateCategoryRolesDTO:
    """DTO для массового обновления ролей категорий"""
    category_ids: List[int]
    roles: List[int]


@dataclass
class CategoryAccessCheckDTO:
    """DTO для проверки доступа к категории"""
    category_id: int
    role_id: int
    has_access: bool


@dataclass
class CategoryDocumentStatsDTO:
    """DTO для статистики категории"""
    category_id: int
    total_documents: int
    total_subcategories: int
    accessible_by_roles: List[int]
    is_public: bool


@dataclass
class MoveCategoryDTO:
    """DTO для перемещения категории на другой уровень"""
    category_id: int
    new_level: int
    new_parent_id: Optional[int] = None
