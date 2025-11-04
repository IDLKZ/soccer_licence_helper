"""
Department Report API Schemas
Схемы для API работы с отчетами департамента
"""
from pydantic import BaseModel, Field


class GenerateDepartmentReportRequest(BaseModel):
    """Запрос на генерацию отчета департамента"""
    report_id: int = Field(..., description="ID отчета (application_reports.id)", gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "report_id": 1
            }
        }
