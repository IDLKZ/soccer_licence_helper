"""
Solutions Router
Эндпоинты для работы с решениями
"""
import tempfile
import traceback
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.presentation.api.v1.schemas.solution_schemas import GenerateSolutionRequest
from app.presentation.api.dependencies import (
    GenerateSolutionUseCaseDep,
    TemplateRenderer,
    PDFGenerator,
    load_logo_base64
)

router = APIRouter(prefix="/solutions", tags=["solutions"])


@router.post("/generate", response_class=FileResponse)
async def generate_solution(
    request: GenerateSolutionRequest,
    use_case: GenerateSolutionUseCaseDep,
    template_renderer: TemplateRenderer,
    pdf_generator: PDFGenerator
):
    """
    Генерировать решение по заявке

    Генерирует PDF решение на основе данных заявки и критериев.

    Args:
        request: Запрос с solution_id
        use_case: Use Case для генерации данных решения
        template_renderer: Сервис рендеринга шаблонов
        pdf_generator: Сервис генерации PDF

    Returns:
        FileResponse с PDF файлом

    Raises:
        HTTPException: 404 если решение не найдено, 500 при ошибках генерации
    """
    try:
        # Загружаем логотип
        logo_base64 = load_logo_base64()

        # Выполняем Use Case для получения данных решения
        solution_data = await use_case.execute(
            solution_id=request.solution_id,
            logo_base64=logo_base64
        )

        # Преобразуем SolutionDataDTO в словарь для шаблона
        context = {
            "meeting_date": solution_data.meeting_date,
            "meeting_place": solution_data.meeting_place,
            "department_name": solution_data.department_name,
            "director_name": solution_data.director_name,
            "director_position": solution_data.director_position,
            "secretary_position": solution_data.secretary_position,
            "control_position": solution_data.control_position,
            "control_name": solution_data.control_name,
            "experts": solution_data.experts,
            "club_fullname": solution_data.club_fullname,
            "club_shortname": solution_data.club_shortname,
            "license": solution_data.license,
            "season": solution_data.season,
            "criteria": [
                {
                    "title": criterion.title,
                    "description": criterion.description,
                    "status": criterion.status
                }
                for criterion in solution_data.criteria
            ],
            "documents": [
                {
                    "title": article.title,
                    "docs": [
                        {
                            "title": doc.title,
                            "comment": doc.comment,
                            "deadline": doc.deadline
                        }
                        for doc in article.docs
                    ]
                }
                for article in solution_data.documents
            ],
            "secretary_name": solution_data.secretary_name,
            "summary": solution_data.summary,
            "conclusion": solution_data.conclusion,
            "logo_base64": solution_data.logo_base64
        }

        # Рендерим HTML шаблон
        html_content = template_renderer.render("solution_template.html", context)

        # Создаем временный файл для PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file.close()

        # Генерируем PDF
        pdf_generator.generate_from_html(html_content, temp_file.name)

        # Возвращаем PDF файл
        return FileResponse(
            path=temp_file.name,
            media_type="application/pdf",
            filename=f"solution_{request.solution_id}.pdf",
            background=None  # Файл будет удален автоматически после отправки
        )

    except ValueError as e:
        # Ошибка валидации (решение не найдено и т.д.)
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
        traceback.print_exc()
        # Другие ошибки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate solution: {str(e)}"
        )
