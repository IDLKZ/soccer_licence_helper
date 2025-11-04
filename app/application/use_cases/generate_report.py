"""
Use Case: Generate Report
Сценарий использования: Генерация отчета
"""
from typing import Optional
from app.domain.entities.report import Report, ReportStatus
from app.domain.repositories.report_repository import IReportRepository
from app.domain.services.report_service import ReportDomainService
from app.application.dto.report_dto import GenerateReportResultDTO


class GenerateReportUseCase:
    """
    Use Case для генерации отчета
    Координирует процесс генерации отчета
    """

    def __init__(
        self,
        report_repository: IReportRepository,
        report_service: ReportDomainService
    ):
        self.report_repository = report_repository
        self.report_service = report_service

    async def execute(self, report_id: int) -> GenerateReportResultDTO:
        """
        Выполнить генерацию отчета

        Args:
            report_id: ID отчета для генерации

        Returns:
            Результат генерации

        Raises:
            ValueError: Если отчет не найден или недоступен для генерации
        """
        # Получение отчета
        report = await self.report_repository.get_by_id(report_id)
        if not report:
            raise ValueError(f"Report with id {report_id} not found")

        # Проверка, можно ли генерировать отчет
        if report.is_processing():
            raise ValueError(f"Report {report_id} is already being processed")

        try:
            # Отметить как обрабатывающийся
            report.mark_as_processing()
            await self.report_repository.update(report)

            # Генерация отчета (здесь будет вызов реального генератора)
            file_path = await self._generate_report_file(report)

            # Отметить как завершенный
            report.mark_as_completed(file_path)
            await self.report_repository.update(report)

            return GenerateReportResultDTO(
                report_id=report.id,
                status=ReportStatus.COMPLETED,
                message="Report generated successfully",
                file_path=file_path
            )

        except Exception as e:
            # Отметить как неудачный
            error_msg = str(e)
            report.mark_as_failed(error_msg)
            await self.report_repository.update(report)

            return GenerateReportResultDTO(
                report_id=report.id,
                status=ReportStatus.FAILED,
                message=f"Report generation failed: {error_msg}"
            )

    async def _generate_report_file(self, report: Report) -> str:
        """
        Сгенерировать файл отчета
        TODO: Реализовать реальную генерацию отчета

        Args:
            report: Отчет для генерации

        Returns:
            Путь к сгенерированному файлу
        """
        # Генерация имени файла
        filename = self.report_service.generate_report_filename(report)

        # TODO: Здесь будет реальная логика генерации отчета
        # Например, генерация PDF, Excel и т.д.
        # В зависимости от типа отчета вызывать соответствующий генератор

        # Временная заглушка
        file_path = f"reports/{filename}"

        return file_path
