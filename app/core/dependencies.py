"""
Dependency Injection Container
Контейнер для внедрения зависимостей
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.domain.repositories.report_repository import IReportRepository
from app.domain.services.report_service import ReportDomainService
from app.infrastructure.database.repositories.report_repository_impl import (
    ReportRepositoryImpl
)
from app.application.use_cases.create_report import CreateReportUseCase
from app.application.use_cases.generate_report import GenerateReportUseCase
from app.application.use_cases.get_report import GetReportUseCase
from app.application.use_cases.list_reports import ListReportsUseCase
from app.application.use_cases.delete_report import DeleteReportUseCase


# Repository Dependencies
def get_report_repository(
    db: AsyncSession = Depends(get_db)
) -> IReportRepository:
    """Получить репозиторий отчетов"""
    return ReportRepositoryImpl(db)


# Service Dependencies
def get_report_service() -> ReportDomainService:
    """Получить доменный сервис отчетов"""
    return ReportDomainService()


# Use Case Dependencies
def get_create_report_use_case(
    repository: IReportRepository = Depends(get_report_repository),
    service: ReportDomainService = Depends(get_report_service)
) -> CreateReportUseCase:
    """Получить use case создания отчета"""
    return CreateReportUseCase(repository, service)


def get_generate_report_use_case(
    repository: IReportRepository = Depends(get_report_repository),
    service: ReportDomainService = Depends(get_report_service)
) -> GenerateReportUseCase:
    """Получить use case генерации отчета"""
    return GenerateReportUseCase(repository, service)


def get_get_report_use_case(
    repository: IReportRepository = Depends(get_report_repository)
) -> GetReportUseCase:
    """Получить use case получения отчета"""
    return GetReportUseCase(repository)


def get_list_reports_use_case(
    repository: IReportRepository = Depends(get_report_repository)
) -> ListReportsUseCase:
    """Получить use case списка отчетов"""
    return ListReportsUseCase(repository)


def get_delete_report_use_case(
    repository: IReportRepository = Depends(get_report_repository)
) -> DeleteReportUseCase:
    """Получить use case удаления отчета"""
    return DeleteReportUseCase(repository)
