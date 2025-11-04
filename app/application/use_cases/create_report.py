"""
Use Case: Create Report
Сценарий использования: Создание отчета
"""
from app.domain.entities.report import Report, ReportStatus
from app.domain.repositories.report_repository import IReportRepository
from app.domain.services.report_service import ReportDomainService
from app.application.dto.report_dto import CreateReportDTO, ReportDTO


class CreateReportUseCase:
    """
    Use Case для создания нового отчета
    Инкапсулирует бизнес-логику создания отчета
    """

    def __init__(
        self,
        report_repository: IReportRepository,
        report_service: ReportDomainService
    ):
        self.report_repository = report_repository
        self.report_service = report_service

    async def execute(self, dto: CreateReportDTO) -> ReportDTO:
        """
        Выполнить создание отчета

        Args:
            dto: DTO с данными для создания

        Returns:
            DTO созданного отчета

        Raises:
            ValueError: Если параметры невалидны
        """
        # Валидация параметров через доменный сервис
        is_valid, error_message = self.report_service.validate_report_parameters(
            dto.report_type,
            dto.parameters
        )

        if not is_valid:
            raise ValueError(f"Invalid report parameters: {error_message}")

        # Создание доменной сущности
        report = Report(
            name=dto.name,
            report_type=dto.report_type,
            parameters=dto.parameters,
            status=ReportStatus.PENDING
        )

        # Сохранение в репозиторий
        created_report = await self.report_repository.create(report)

        # Конвертация в DTO для возврата
        return self._map_to_dto(created_report)

    @staticmethod
    def _map_to_dto(report: Report) -> ReportDTO:
        """Конвертация доменной сущности в DTO"""
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
