"""
Domain service for Report business logic
Доменный сервис - содержит бизнес-логику, которая не относится к конкретной сущности
"""
from typing import Dict, Any
from app.domain.entities.report import Report, ReportType


class ReportDomainService:
    """
    Доменный сервис для бизнес-логики отчетов
    Содержит правила и валидации, которые затрагивают несколько сущностей
    """

    @staticmethod
    def validate_report_parameters(
        report_type: ReportType,
        parameters: Dict[str, Any]
    ) -> tuple[bool, str]:
        """
        Валидация параметров отчета в зависимости от типа

        Args:
            report_type: Тип отчета
            parameters: Параметры отчета

        Returns:
            Tuple (валидность, сообщение об ошибке)
        """
        if not parameters:
            return False, "Parameters cannot be empty"

        if report_type == ReportType.LICENSE_SUMMARY:
            return ReportDomainService._validate_license_summary_params(parameters)

        elif report_type == ReportType.LICENSE_DETAILS:
            return ReportDomainService._validate_license_details_params(parameters)

        elif report_type == ReportType.EXPIRATION_REPORT:
            return ReportDomainService._validate_expiration_report_params(parameters)

        elif report_type == ReportType.CUSTOM:
            return ReportDomainService._validate_custom_report_params(parameters)

        return False, f"Unknown report type: {report_type}"

    @staticmethod
    def _validate_license_summary_params(parameters: Dict[str, Any]) -> tuple[bool, str]:
        """Валидация параметров для сводного отчета по лицензиям"""
        required_fields = ["date_from", "date_to"]

        for field in required_fields:
            if field not in parameters:
                return False, f"Missing required field: {field}"

        return True, ""

    @staticmethod
    def _validate_license_details_params(parameters: Dict[str, Any]) -> tuple[bool, str]:
        """Валидация параметров для детального отчета по лицензиям"""
        if "license_ids" not in parameters and "product_ids" not in parameters:
            return False, "Either license_ids or product_ids must be provided"

        return True, ""

    @staticmethod
    def _validate_expiration_report_params(parameters: Dict[str, Any]) -> tuple[bool, str]:
        """Валидация параметров для отчета по истекающим лицензиям"""
        if "days_threshold" not in parameters:
            return False, "days_threshold parameter is required"

        try:
            days = int(parameters["days_threshold"])
            if days <= 0:
                return False, "days_threshold must be positive"
        except (ValueError, TypeError):
            return False, "days_threshold must be a valid number"

        return True, ""

    @staticmethod
    def _validate_custom_report_params(parameters: Dict[str, Any]) -> tuple[bool, str]:
        """Валидация параметров для кастомного отчета"""
        if "query" not in parameters:
            return False, "Custom report requires 'query' parameter"

        return True, ""

    @staticmethod
    def calculate_report_priority(report: Report) -> int:
        """
        Рассчитать приоритет отчета для очереди обработки

        Args:
            report: Отчет

        Returns:
            Приоритет (чем выше число, тем выше приоритет)
        """
        priority = 0

        # Приоритет по типу отчета
        priority_by_type = {
            ReportType.EXPIRATION_REPORT: 3,
            ReportType.LICENSE_DETAILS: 2,
            ReportType.LICENSE_SUMMARY: 1,
            ReportType.CUSTOM: 0
        }
        priority += priority_by_type.get(report.report_type, 0)

        # Можно добавить другие факторы (например, время ожидания)

        return priority

    @staticmethod
    def generate_report_filename(report: Report) -> str:
        """
        Сгенерировать имя файла для отчета

        Args:
            report: Отчет

        Returns:
            Имя файла
        """
        from datetime import datetime
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        report_name = report.name.replace(" ", "_").lower()
        return f"report_{report.report_type.value}_{report_name}_{timestamp}.pdf"
