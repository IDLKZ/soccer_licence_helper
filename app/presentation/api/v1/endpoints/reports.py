"""
Report endpoints
API endpoints для работы с отчетами
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from typing import Optional

from app.domain.entities.report import ReportStatus, ReportType
from app.presentation.api.v1.schemas.report_schema import (
    ReportCreateRequest,
    ReportResponse,
    ReportListResponse,
    GenerateReportResponse,
    MessageResponse
)
from app.application.use_cases.create_report import CreateReportUseCase
from app.application.use_cases.generate_report import GenerateReportUseCase
from app.application.use_cases.get_report import GetReportUseCase
from app.application.use_cases.list_reports import ListReportsUseCase
from app.application.use_cases.delete_report import DeleteReportUseCase
from app.application.dto.report_dto import CreateReportDTO
from app.core.dependencies import (
    get_create_report_use_case,
    get_generate_report_use_case,
    get_get_report_use_case,
    get_list_reports_use_case,
    get_delete_report_use_case
)

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post(
    "/",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый отчет",
    description="Создает новый отчет с указанными параметрами"
)
async def create_report(
    request: ReportCreateRequest,
    use_case: CreateReportUseCase = Depends(get_create_report_use_case)
):
    """Создать новый отчет"""
    try:
        dto = CreateReportDTO(
            name=request.name,
            report_type=request.report_type,
            parameters=request.parameters
        )
        result = await use_case.execute(dto)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create report: {str(e)}"
        )


@router.get(
    "/",
    response_model=ReportListResponse,
    summary="Получить список отчетов",
    description="Получить список отчетов с фильтрацией и пагинацией"
)
async def list_reports(
    page: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    status: Optional[ReportStatus] = Query(None, description="Фильтр по статусу"),
    report_type: Optional[ReportType] = Query(None, description="Фильтр по типу отчета"),
    use_case: ListReportsUseCase = Depends(get_list_reports_use_case)
):
    """Получить список отчетов"""
    try:
        result = await use_case.execute(
            page=page,
            page_size=page_size,
            status=status,
            report_type=report_type
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch reports: {str(e)}"
        )


@router.get(
    "/{report_id}",
    response_model=ReportResponse,
    summary="Получить отчет по ID",
    description="Получить подробную информацию об отчете"
)
async def get_report(
    report_id: int,
    use_case: GetReportUseCase = Depends(get_get_report_use_case)
):
    """Получить отчет по ID"""
    try:
        result = await use_case.execute(report_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report with id {report_id} not found"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch report: {str(e)}"
        )


@router.post(
    "/{report_id}/generate",
    response_model=GenerateReportResponse,
    summary="Сгенерировать отчет",
    description="Запустить процесс генерации отчета"
)
async def generate_report(
    report_id: int,
    background_tasks: BackgroundTasks,
    use_case: GenerateReportUseCase = Depends(get_generate_report_use_case)
):
    """Сгенерировать отчет"""
    try:
        # Запуск генерации в фоне
        result = await use_case.execute(report_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate report: {str(e)}"
        )


@router.delete(
    "/{report_id}",
    response_model=MessageResponse,
    summary="Удалить отчет",
    description="Удалить отчет и связанные файлы"
)
async def delete_report(
    report_id: int,
    use_case: DeleteReportUseCase = Depends(get_delete_report_use_case)
):
    """Удалить отчет"""
    try:
        await use_case.execute(report_id)
        return MessageResponse(
            message="Report deleted successfully",
            detail=f"Report with id {report_id} has been deleted"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete report: {str(e)}"
        )


@router.get(
    "/{report_id}/download",
    summary="Скачать сгенерированный отчет",
    description="Скачать файл сгенерированного отчета"
)
async def download_report(
    report_id: int,
    use_case: GetReportUseCase = Depends(get_get_report_use_case)
):
    """Скачать файл отчета"""
    try:
        report = await use_case.execute(report_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report with id {report_id} not found"
            )

        if report.status != ReportStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Report is not ready yet"
            )

        if not report.file_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report file not found"
            )

        # TODO: Реализовать возврат файла
        # from fastapi.responses import FileResponse
        # return FileResponse(report.file_path, filename=...)

        return MessageResponse(
            message="Download endpoint",
            detail=f"File path: {report.file_path}"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download report: {str(e)}"
        )
