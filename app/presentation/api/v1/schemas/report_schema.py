"""
Pydantic schemas for API validation
Схемы для валидации запросов и ответов API
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.domain.entities.report import ReportStatus, ReportType


class ReportCreateRequest(BaseModel):
    """Схема запроса на создание отчета"""
    name: str = Field(..., min_length=1, max_length=255, description="Название отчета")
    report_type: ReportType = Field(..., description="Тип отчета")
    parameters: Dict[str, Any] = Field(..., description="Параметры генерации отчета")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Monthly License Report",
                "report_type": "license_summary",
                "parameters": {
                    "date_from": "2024-01-01",
                    "date_to": "2024-01-31"
                }
            }
        }
    )


class ReportResponse(BaseModel):
    """Схема ответа с данными отчета"""
    id: int
    name: str
    report_type: ReportType
    status: ReportStatus
    parameters: Dict[str, Any]
    file_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ReportListResponse(BaseModel):
    """Схема ответа со списком отчетов"""
    reports: List[ReportResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class GenerateReportResponse(BaseModel):
    """Схема ответа на запрос генерации отчета"""
    report_id: int
    status: ReportStatus
    message: str
    file_path: Optional[str] = None


class MessageResponse(BaseModel):
    """Схема простого ответа с сообщением"""
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    """Схема ответа с ошибкой"""
    error: str
    detail: Optional[str] = None
    status_code: int
