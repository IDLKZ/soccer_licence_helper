"""
Department Report Generation DTOs
DTOs для генерации отчета департамента
"""
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class DepartmentReportDocumentDTO:
    """DTO для документа в отчете департамента"""
    document_id: str
    title_with_status: str


@dataclass
class DepartmentReportItemDTO:
    """DTO для элемента отчета (по эксперту)"""
    date: str
    expert: str
    documents: List[Dict[str, str]]  # [{document_id: "title - статус"}]


@dataclass
class DepartmentReportDataDTO:
    """DTO для данных отчета департамента"""
    department: str
    position: str
    date: str
    club: str
    reports: List[DepartmentReportItemDTO]
    logo_base64: str
    sign_img: str
