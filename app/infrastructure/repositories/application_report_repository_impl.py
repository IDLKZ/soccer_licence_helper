"""
Application Report Repository Implementation
Реализация репозитория для отчетов по заявкам
"""
from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.application_report_repository import IApplicationReportRepository
from app.domain.entities.application_report import ApplicationReport
from app.infrastructure.database.models.application_report import ApplicationReportModel
from app.infrastructure.mappers.entity_mapper import EntityMapper
from app.infrastructure.repositories.base_repository import BaseRepository


class ApplicationReportRepositoryImpl(BaseRepository[ApplicationReportModel], IApplicationReportRepository):
    """Реализация репозитория для ApplicationReport"""

    def __init__(self, session: AsyncSession):
        super().__init__(ApplicationReportModel, session)
        self.mapper = EntityMapper()

    async def get_by_id(self, report_id: int) -> Optional[ApplicationReport]:
        """
        Получить отчет по ID

        Args:
            report_id: ID отчета

        Returns:
            ApplicationReport или None
        """
        model = await super().get_by_id(report_id)
        if not model:
            return None
        return self.mapper.to_application_report_entity(model)

    async def get_by_id_with_relations(self, report_id: int) -> Optional[ApplicationReport]:
        """
        Получить отчет по ID со всеми связанными данными

        Args:
            report_id: ID отчета

        Returns:
            ApplicationReport со связями или None
        """
        query = (
            select(ApplicationReportModel)
            .where(ApplicationReportModel.id == report_id)
            .options(selectinload(ApplicationReportModel.criteria))
        )

        result = await self.session.execute(query)
        model = result.scalar_one_or_none()

        if not model:
            return None

        return self.mapper.to_application_report_entity(model)
