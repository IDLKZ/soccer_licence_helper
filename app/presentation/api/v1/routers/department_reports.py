"""
Department Reports Router
Эндпоинты для работы с отчетами департамента
"""
import tempfile
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.presentation.api.v1.schemas.department_report_schemas import GenerateDepartmentReportRequest
from app.presentation.api.dependencies import (
    GenerateDepartmentReportUseCaseDep,
    TemplateRenderer,
    PDFGenerator,
    load_logo_base64,
    load_sign_img_base64
)

router = APIRouter(prefix="/department-reports", tags=["department-reports"])


@router.post("/generate", response_class=FileResponse)
async def generate_department_report(
    request: GenerateDepartmentReportRequest,
    use_case: GenerateDepartmentReportUseCaseDep,
    template_renderer: TemplateRenderer,
    pdf_generator: PDFGenerator
):
    """
    Генерировать отчет департамента

    Генерирует PDF отчет на основе данных application_reports.

    Args:
        request: Запрос с report_id
        use_case: Use Case для генерации отчета департамента
        template_renderer: Сервис рендеринга шаблонов
        pdf_generator: Сервис генерации PDF

    Returns:
        FileResponse с PDF файлом

    Raises:
        HTTPException: 404 если отчет не найден, 500 при ошибках генерации
    """
    try:
        # Загружаем изображения
        logo_base64 = load_logo_base64()
        sign_img = load_sign_img_base64()

        # Выполняем Use Case для получения данных отчета
        report_data = await use_case.execute(
            report_id=request.report_id,
            logo_base64=logo_base64,
            sign_img=sign_img
        )

        # Преобразуем DepartmentReportDataDTO в словарь для шаблона
        context = {
            "department": report_data.department,
            "position": report_data.position,
            "date": report_data.date,
            "club": report_data.club,
            "reports": [
                {
                    "date": report.date,
                    "expert": report.expert,
                    "documents": report.documents
                }
                for report in report_data.reports
            ],
            "logo_base64": report_data.logo_base64,
            "sign_img": report_data.sign_img
        }

        # Рендерим HTML шаблон
        html_content = template_renderer.render("department_report_template.html", context)

        # Создаем временный файл для PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.close()

        # Генерируем PDF
        pdf_generator.generate_from_html(html_content, temp_file.name)

        # Возвращаем PDF файл
        return FileResponse(
            path=temp_file.name,
            media_type="application/pdf",
            filename=f"department_report_{request.report_id}.pdf",
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
        # traceback.print_exc()
        # Другие ошибки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate department report: {str(e)}"
        )
