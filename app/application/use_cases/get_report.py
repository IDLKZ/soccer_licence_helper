"""
Use Case: Get Report
Сценарий использования: Получение отчета
"""
from typing import Optional
from app.domain.repositories.report_repository import IReportRepository
from app.application.dto.report_dto import ReportDTO


class GetReportUseCase:
    """Use Case для получения отчета по ID"""

    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository

    async def execute(self, report_id: int) -> Optional[ReportDTO]:
        """
        Получить отчет по ID

        Args:
            report_id: ID отчета

        Returns:
            DTO отчета или None
        """
        report = await self.report_repository.get_by_id(report_id)

        if not report:
            return None

        return ReportDTO(
            id=report.id,
            name=report.name,
            report_type=report.report_type,
            status=report.status,
            parameters=report.parameters,
            file_path=report.file_path,
            created_at=report.created_at,
            updated_at=report.updated_at,
            completed_at=report.completed_at,
            error_message=report.error_message
        )
