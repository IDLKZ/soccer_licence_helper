"""
Generate Certificate Use Case
Use Case для генерации сертификата лицензии
"""
import os
import tempfile
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.models.license_certificate import LicenseCertificateModel
from app.infrastructure.database.models.application_solution import ApplicationSolutionModel
from app.infrastructure.database.models.application import ApplicationModel
from app.infrastructure.database.models.license import LicenseModel
from app.infrastructure.database.models.club import ClubModel
from app.application.dto.certificate_dto import CertificateDataDTO


class GenerateCertificateUseCase:
    """Use Case для генерации сертификата лицензии"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(
        self,
        certificate_id: int,
        logo_base64: str,
        bg_image_en: str,
        bg_image_kk: str,
        sign_img: str
    ) -> CertificateDataDTO:
        """
        Выполнить генерацию данных сертификата

        Args:
            certificate_id: ID сертификата
            logo_base64: Логотип в формате base64
            bg_image_en: Фон для английской версии в base64
            bg_image_kk: Фон для казахской версии в base64
            sign_img: Подпись в формате base64

        Returns:
            CertificateDataDTO с данными для шаблона

        Raises:
            ValueError: Если сертификат не найден
        """
        # Получаем сертификат со связями
        certificate = await self._get_certificate_with_relations(certificate_id)
        if not certificate:
            raise ValueError(f"Certificate with id {certificate_id} not found")

        # Получаем club
        club = certificate.club
        if not club:
            raise ValueError(f"Club not found for certificate {certificate_id}")

        # Получаем license
        license_entity = certificate.license
        if not license_entity:
            raise ValueError(f"License not found for certificate {certificate_id}")

        # Получаем первое решение по application_id
        solution = await self._get_first_solution(certificate.application_id)
        if not solution:
            raise ValueError(f"Solution not found for application {certificate.application_id}")

        # Форматируем дату окончания лицензии
        license_end_at = license_entity.end_at.strftime("%d/%m/%Y") if license_entity.end_at else ""

        # Форматируем дату решения
        sol = datetime.strptime(solution.created_at.strftime("%d/%m/%Y"), "%d/%m/%Y")
        solution_day = f"{sol.day:02d}"
        solution_month = sol.strftime("%m")
        solution_year = sol.strftime("%Y")

        # Формируем DTO
        certificate_data = CertificateDataDTO(
            type_en=certificate.type_ru if certificate.type_ru else "to participate in UEFA club tournaments",
            type_kk=certificate.type_kk if certificate.type_kk else "«Қазақстан Футбол федерациясы» Қауымдастығы <br> ЗТБ-мен ұйымдастырылатын жарыстарына қатысу үшін",
            club_full_name_kk=club.full_name_kk if club.full_name_kk else "",
            club_full_name_en=club.full_name_en if club.full_name_en else "",
            club_bin=club.bin if club.bin else "",
            license_end_at=license_end_at,
            certificate_id=certificate.id,
            solution_day=solution_day,
            solution_month=solution_month,
            solution_year=solution_year,
            logo_base64=logo_base64,
            bg_image_en=bg_image_en,
            bg_image_kk=bg_image_kk,
            sign_img=sign_img
        )

        return certificate_data

    async def _get_certificate_with_relations(self, certificate_id: int) -> LicenseCertificateModel:
        """Получить сертификат со всеми связями"""
        query = (
            select(LicenseCertificateModel)
            .where(LicenseCertificateModel.id == certificate_id)
            .options(
                selectinload(LicenseCertificateModel.club)
            )
            .options(
                selectinload(LicenseCertificateModel.license)
            )
            .options(
                selectinload(LicenseCertificateModel.application)
            )
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def _get_first_solution(self, application_id: int) -> ApplicationSolutionModel | None:
        """Получить первое решение по application_id"""
        query = (
            select(ApplicationSolutionModel)
            .where(ApplicationSolutionModel.application_id == application_id)
            .order_by(ApplicationSolutionModel.created_at.asc())
            .limit(1)
        )

        result = await self.db.execute(query)
        return result.scalars().first()
