"""
Report Repository Implementation
Реализация репозитория отчетов
"""
from typing import List, Optional
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.report import Report, ReportStatus, ReportType
from app.domain.repositories.report_repository import IReportRepository
from app.infrastructure.database.models import ReportModel


class ReportRepositoryImpl(IReportRepository):
    """Реализация репозитория отчетов через SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, report: Report) -> Report:
        """Создать новый отчет"""
        db_report = ReportModel(
            name=report.name,
            report_type=report.report_type,
            status=report.status,
            parameters=report.parameters,
            file_path=report.file_path,
            error_message=report.error_message
        )

        self.session.add(db_report)
        await self.session.flush()
        await self.session.refresh(db_report)

        return self._map_to_entity(db_report)

    async def get_by_id(self, report_id: int) -> Optional[Report]:
        """Получить отчет по ID"""
        stmt = select(ReportModel).where(ReportModel.id == report_id)
        result = await self.session.execute(stmt)
        db_report = result.scalar_one_or_none()

        if db_report:
            return self._map_to_entity(db_report)
        return None

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ReportStatus] = None,
        report_type: Optional[ReportType] = None
    ) -> List[Report]:
        """Получить список отчетов с фильтрацией"""
        stmt = select(ReportModel)

        # Применение фильтров
        if status:
            stmt = stmt.where(ReportModel.status == status)
        if report_type:
            stmt = stmt.where(ReportModel.report_type == report_type)

        # Сортировка и пагинация
        stmt = stmt.order_by(ReportModel.created_at.desc())
        stmt = stmt.offset(skip).limit(limit)

        result = await self.session.execute(stmt)
        db_reports = result.scalars().all()

        return [self._map_to_entity(db_report) for db_report in db_reports]

    async def update(self, report: Report) -> Report:
        """Обновить отчет"""
        stmt = select(ReportModel).where(ReportModel.id == report.id)
        result = await self.session.execute(stmt)
        db_report = result.scalar_one_or_none()

        if not db_report:
            raise ValueError(f"Report with id {report.id} not found")

        # Обновление полей
        db_report.name = report.name
        db_report.report_type = report.report_type
        db_report.status = report.status
        db_report.parameters = report.parameters
        db_report.file_path = report.file_path
        db_report.error_message = report.error_message
        db_report.completed_at = report.completed_at

        await self.session.flush()
        await self.session.refresh(db_report)

        return self._map_to_entity(db_report)

    async def delete(self, report_id: int) -> bool:
        """Удалить отчет"""
        stmt = delete(ReportModel).where(ReportModel.id == report_id)
        result = await self.session.execute(stmt)
        await self.session.flush()

        return result.rowcount > 0

    async def count(
        self,
        status: Optional[ReportStatus] = None,
        report_type: Optional[ReportType] = None
    ) -> int:
        """Подсчитать количество отчетов"""
        stmt = select(func.count(ReportModel.id))

        # Применение фильтров
        if status:
            stmt = stmt.where(ReportModel.status == status)
        if report_type:
            stmt = stmt.where(ReportModel.report_type == report_type)

        result = await self.session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    def _map_to_entity(db_report: ReportModel) -> Report:
        """Конвертация модели БД в доменную сущность"""
        return Report(
            id=db_report.id,
            name=db_report.name,
            report_type=db_report.report_type,
            status=db_report.status,
            parameters=db_report.parameters,
            file_path=db_report.file_path,
            error_message=db_report.error_message,
            created_at=db_report.created_at,
            updated_at=db_report.updated_at,
            completed_at=db_report.completed_at
        )
