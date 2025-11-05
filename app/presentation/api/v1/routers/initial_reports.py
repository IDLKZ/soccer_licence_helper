"""
Initial Reports Router
Эндпоинты для работы с начальными отчетами
"""
import tempfile
import os
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.presentation.api.v1.schemas.initial_report_schemas import GenerateInitialReportRequest
from app.presentation.api.dependencies import (
    GenerateInitialReportUseCaseDep,
    TemplateRenderer,
    PDFGenerator,
    load_logo_base64
)

router = APIRouter(prefix="/initial-reports", tags=["initial-reports"])


@router.post("/generate", response_class=FileResponse)
async def generate_initial_report(
    request: GenerateInitialReportRequest,
    use_case: GenerateInitialReportUseCaseDep,
    template_renderer: TemplateRenderer,
    pdf_generator: PDFGenerator
):
    """
    Генерировать начальный отчет по заявке

    Генерирует PDF отчет на основе данных заявки и критериев.

    Args:
        request: Запрос с report_id
        use_case: Use Case для генерации данных отчета
        template_renderer: Сервис рендеринга шаблонов
        pdf_generator: Сервис генерации PDF

    Returns:
        FileResponse с PDF файлом

    Raises:
        HTTPException: 404 если отчет не найден, 500 при ошибках генерации
    """
    try:
        # Загружаем логотип
        logo_base64 = load_logo_base64()

        # Выполняем Use Case для получения данных отчета
        report_data = await use_case.execute(
            report_id=request.report_id,
            logo_base64=logo_base64
        )

        # Преобразуем InitialReportDataDTO в словарь для шаблона
        context = {
            "expert": report_data.expert,
            "director": report_data.director,
            "date": report_data.date,
            "club": report_data.club,
            "documents": [
                {
                    "number": doc.number,
                    "name": doc.name,
                    "submission_date": doc.submission_date,
                    "notes": doc.notes
                }
                for doc in report_data.documents
            ],
            "logo_base64": logo_base64
        }

        # Рендерим HTML шаблон
        html_content = template_renderer.render("initial_report_template.html", context)

        # Создаем временный файл для PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.close()

        # Генерируем PDF
        pdf_generator.generate_from_html(html_content, temp_file.name)

        # Возвращаем PDF файл
        return FileResponse(
            path=temp_file.name,
            media_type="application/pdf",
            filename=f"initial_report_{request.report_id}.pdf",
            background=None  # Файл будет удален автоматически после отправки
        )

    except ValueError as e:
        # Ошибка валидации (отчет не найден и т.д.)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except FileNotFoundError as e:
        # Шаблон не найден
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Template not found: {str(e)}"
        )
    except Exception as e:
        # Другие ошибки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate initial report: {str(e)}"
        )
