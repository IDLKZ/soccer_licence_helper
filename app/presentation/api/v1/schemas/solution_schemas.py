"""
Pydantic schemas for Solution API
Схемы для API решений
"""
from pydantic import BaseModel, Field


class GenerateSolutionRequest(BaseModel):
    """Запрос на генерацию решения"""
    solution_id: int = Field(..., description="ID решения", gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "solution_id": 1
            }
        }
