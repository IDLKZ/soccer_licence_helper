"""
Certificate Generation DTOs
DTOs для генерации сертификата лицензии
"""
from dataclasses import dataclass


@dataclass
class CertificateDataDTO:
    """DTO для данных сертификата"""
    club_full_name_kk: str
    club_full_name_en: str
    club_bin: str
    license_end_at: str
    certificate_id: int
    solution_day: str
    solution_month: str
    solution_year: str
    logo_base64: str
    bg_image_en: str
    bg_image_kk: str
    sign_img: str
