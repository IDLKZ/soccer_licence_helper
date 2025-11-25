"""
Certificates Router
Эндпоинты для работы с сертификатами лицензий
"""
import os
import tempfile
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from PyPDF2 import PdfMerger

from app.presentation.api.v1.schemas.certificate_schemas import GenerateCertificateRequest
from app.presentation.api.dependencies import (
    GenerateCertificateUseCaseDep,
    TemplateRenderer,
    PDFGenerator,
    load_logo_base64,
    load_sign_img_base64,
    load_bg_certificate_en,
    load_bg_certificate_kk
)

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.post("/generate", response_class=FileResponse)
async def generate_certificate(
    request: GenerateCertificateRequest,
    use_case: GenerateCertificateUseCaseDep,
    template_renderer: TemplateRenderer,
    pdf_generator: PDFGenerator
):
    """
    Генерировать сертификат лицензии

    Генерирует PDF сертификат на двух языках (EN и KK) и объединяет их в один файл.

    Args:
        request: Запрос с certificate_id
        use_case: Use Case для генерации сертификата
        template_renderer: Сервис рендеринга шаблонов
        pdf_generator: Сервис генерации PDF

    Returns:
        FileResponse с PDF файлом (две страницы: EN и KK)

    Raises:
        HTTPException: 404 если сертификат не найден, 500 при ошибках генерации
    """
    try:
        # Загружаем изображения
        logo_base64 = load_logo_base64()
        sign_img = load_sign_img_base64()
        bg_image_en = load_bg_certificate_en()
        bg_image_kk = load_bg_certificate_kk()

        # Выполняем Use Case для получения данных сертификата
        certificate_data = await use_case.execute(
            certificate_id=request.certificate_id,
            logo_base64=logo_base64,
            bg_image_en=bg_image_en,
            bg_image_kk=bg_image_kk,
            sign_img=sign_img
        )

        # Преобразуем CertificateDataDTO в словарь для шаблона
        context = {
            "type_kk": certificate_data.type_kk,
            "type_en": certificate_data.type_en,
            "club_full_name_kk": certificate_data.club_full_name_kk,
            "club_full_name_en": certificate_data.club_full_name_en,
            "club_bin": certificate_data.club_bin,
            "license_end_at": certificate_data.license_end_at,
            "certificate_id": certificate_data.certificate_id,
            "solution_day": certificate_data.solution_day,
            "solution_month": certificate_data.solution_month,
            "solution_year": certificate_data.solution_year,
            "logo_base64": certificate_data.logo_base64,
            "bg_image_en": certificate_data.bg_image_en,
            "bg_image_kk": certificate_data.bg_image_kk,
            "sign_img": certificate_data.sign_img
        }

        # Рендерим HTML шаблоны (EN и KK версии)
        html_content_en = template_renderer.render("certificate_template_en.html", context)
        html_content_kk = template_renderer.render("certificate_template_kk.html", context)

        # Создаем временные файлы для каждой страницы
        temp_file_en = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file_kk = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_file_combined = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

        temp_file_en.close()
        temp_file_kk.close()
        temp_file_combined.close()

        try:
            # Генерируем PDF для английской версии
            pdf_generator.generate_from_html(html_content_en, temp_file_en.name)

            # Генерируем PDF для казахской версии
            pdf_generator.generate_from_html(html_content_kk, temp_file_kk.name)

            # Объединяем PDF файлы
            merger = PdfMerger()
            merger.append(temp_file_en.name)
            merger.append(temp_file_kk.name)
            merger.write(temp_file_combined.name)
            merger.close()

            # Возвращаем объединенный файл
            return FileResponse(
                path=temp_file_combined.name,
                media_type="application/pdf",
                filename=f"license_certificate_{request.certificate_id}.pdf",
                background=None  # Файл будет удален автоматически после отправки
            )

        finally:
            # Удаляем временные файлы (EN и KK версии)
            try:
                os.unlink(temp_file_en.name)
                os.unlink(temp_file_kk.name)
                # temp_file_combined.name не удаляем, так как его использует FileResponse
            except Exception:
                pass

    except ValueError as e:
        # Ошибка валидации (сертификат не найден и т.д.)
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
            detail=f"Failed to generate certificate: {str(e)}"
        )
