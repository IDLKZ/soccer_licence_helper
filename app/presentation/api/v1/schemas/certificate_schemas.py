"""
Certificate API Schemas
Схемы для API работы с сертификатами
"""
from pydantic import BaseModel, Field


class GenerateCertificateRequest(BaseModel):
    """Запрос на генерацию сертификата"""
    certificate_id: int = Field(..., description="ID сертификата (license_certificates.id)", gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "certificate_id": 1
            }
        }
