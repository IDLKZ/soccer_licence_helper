"""
Data Transfer Objects for Report
DTO для передачи данных между слоями
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from app.domain.entities.report import ReportStatus, ReportType


@dataclass
class CreateReportDTO:
    """DTO для создания отчета"""
    name: str
    report_type: ReportType
    parameters: Dict[str, Any]


@dataclass
class UpdateReportDTO:
    """DTO для обновления отчета"""
    report_id: int
    status: Optional[ReportStatus] = None
    file_path: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class ReportDTO:
    """DTO для отображения отчета"""
    id: int
    name: str
    report_type: ReportType
    status: ReportStatus
    parameters: Dict[str, Any]
    file_path: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    error_message: Optional[str]


@dataclass
class ReportListDTO:
    """DTO для списка отчетов с пагинацией"""
    reports: list[ReportDTO]
    total: int
    page: int
    page_size: int
    total_pages: int


@dataclass
class GenerateReportResultDTO:
    """DTO для результата генерации отчета"""
    report_id: int
    status: ReportStatus
    message: str
    file_path: Optional[str] = None
