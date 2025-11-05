"""
Initial Report API Schemas
Pydantic модели для API endpoints начальных отчетов
"""
from pydantic import BaseModel, Field


class GenerateInitialReportRequest(BaseModel):
    """Запрос на генерацию начального отчета"""

    report_id: int = Field(..., description="ID отчета для генерации", gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "report_id": 1
            }
        }
