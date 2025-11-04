"""
Use Case: List Reports
Сценарий использования: Получение списка отчетов
"""
from typing import Optional
from app.domain.entities.report import ReportStatus, ReportType
from app.domain.repositories.report_repository import IReportRepository
from app.application.dto.report_dto import ReportListDTO, ReportDTO
from math import ceil


class ListReportsUseCase:
    """Use Case для получения списка отчетов с фильтрацией и пагинацией"""

    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository

    async def execute(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[ReportStatus] = None,
        report_type: Optional[ReportType] = None
    ) -> ReportListDTO:
        """
        Получить список отчетов

        Args:
            page: Номер страницы (начинается с 1)
            page_size: Размер страницы
            status: Фильтр по статусу
            report_type: Фильтр по типу отчета

        Returns:
            DTO со списком отчетов и мета-информацией
        """
        # Валидация параметров пагинации
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        if page_size > 100:
            page_size = 100

        # Расчет offset
        skip = (page - 1) * page_size

        # Получение отчетов
        reports = await self.report_repository.get_all(
            skip=skip,
            limit=page_size,
            status=status,
            report_type=report_type
        )

        # Получение общего количества
        total = await self.report_repository.count(
            status=status,
            report_type=report_type
        )

        # Конвертация в DTO
        report_dtos = [
            ReportDTO(
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
            for report in reports
        ]

        # Расчет общего количества страниц
        total_pages = ceil(total / page_size) if total > 0 else 0

        return ReportListDTO(
            reports=report_dtos,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
