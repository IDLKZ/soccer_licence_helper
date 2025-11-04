"""
Use Case: Delete Report
Сценарий использования: Удаление отчета
"""
from app.domain.repositories.report_repository import IReportRepository


class DeleteReportUseCase:
    """Use Case для удаления отчета"""

    def __init__(self, report_repository: IReportRepository):
        self.report_repository = report_repository

    async def execute(self, report_id: int) -> bool:
        """
        Удалить отчет

        Args:
            report_id: ID отчета

        Returns:
            True если удален успешно

        Raises:
            ValueError: Если отчет не найден
        """
        # Проверка существования отчета
        report = await self.report_repository.get_by_id(report_id)
        if not report:
            raise ValueError(f"Report with id {report_id} not found")

        # Удаление отчета
        result = await self.report_repository.delete(report_id)

        # TODO: Добавить удаление файла отчета, если он существует
        # if report.file_path:
        #     await delete_file(report.file_path)

        return result
