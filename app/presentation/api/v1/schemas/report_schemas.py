"""
Report API Schemas
Pydantic модели для API endpoints отчетов
"""
from pydantic import BaseModel, Field


class GenerateReportRequest(BaseModel):
    """Запрос на генерацию отчета"""

    report_id: int = Field(..., description="ID отчета для генерации", gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "report_id": 1
            }
        }
