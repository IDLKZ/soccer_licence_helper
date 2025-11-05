"""
FastAPI Dependencies
Зависимости для инжекции в эндпоинты
"""
import os
import base64
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.application.use_cases.generate_report_use_case_v2 import GenerateReportUseCaseV2
from app.application.use_cases.generate_initial_report_use_case import GenerateInitialReportUseCase
from app.application.use_cases.generate_solution_use_case import GenerateSolutionUseCase
from app.application.use_cases.generate_department_report_use_case import GenerateDepartmentReportUseCase
from app.application.use_cases.generate_certificate_use_case import GenerateCertificateUseCase
from app.domain.services.template_renderer import ITemplateRenderer
from app.domain.services.pdf_generator import IPDFGenerator
from app.infrastructure.services.jinja2_template_renderer import Jinja2TemplateRenderer
from app.infrastructure.services.pdfkit_generator import PdfKitGenerator


# Database dependency
DatabaseSession = Annotated[AsyncSession, Depends(get_db)]


# Template renderer dependency
def get_template_renderer() -> ITemplateRenderer:
    """Получить сервис рендеринга шаблонов"""
    # Путь к директории templates
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    templates_dir = os.path.join(base_dir, "templates")
    return Jinja2TemplateRenderer(templates_dir)


TemplateRenderer = Annotated[ITemplateRenderer, Depends(get_template_renderer)]


# PDF generator dependency
def get_pdf_generator() -> IPDFGenerator:
    """Получить сервис генерации PDF"""
    return PdfKitGenerator()


PDFGenerator = Annotated[IPDFGenerator, Depends(get_pdf_generator)]


# Use Case dependency
def get_generate_report_use_case(
    db: DatabaseSession
) -> GenerateReportUseCaseV2:
    """Получить Use Case для генерации отчета"""
    return GenerateReportUseCaseV2(db)


GenerateReportUseCaseDep = Annotated[GenerateReportUseCaseV2, Depends(get_generate_report_use_case)]


# Initial Report Use Case dependency
def get_generate_initial_report_use_case(
    db: DatabaseSession
) -> GenerateInitialReportUseCase:
    """Получить Use Case для генерации начального отчета"""
    return GenerateInitialReportUseCase(db)


GenerateInitialReportUseCaseDep = Annotated[GenerateInitialReportUseCase, Depends(get_generate_initial_report_use_case)]


# Solution Use Case dependency
def get_generate_solution_use_case(
    db: DatabaseSession
) -> GenerateSolutionUseCase:
    """Получить Use Case для генерации решения"""
    return GenerateSolutionUseCase(db)


GenerateSolutionUseCaseDep = Annotated[GenerateSolutionUseCase, Depends(get_generate_solution_use_case)]


# Department Report Use Case dependency
def get_generate_department_report_use_case(
    db: DatabaseSession
) -> GenerateDepartmentReportUseCase:
    """Получить Use Case для генерации отчета департамента"""
    return GenerateDepartmentReportUseCase(db)


GenerateDepartmentReportUseCaseDep = Annotated[GenerateDepartmentReportUseCase, Depends(get_generate_department_report_use_case)]


# Logo loader helper
def load_logo_base64() -> str:
    """Загрузить логотип в формате base64"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    logo_path = os.path.join(base_dir, "templates", "logo_white.png")

    if not os.path.exists(logo_path):
        # Возвращаем пустую строку если логотип не найден
        return ""

    with open(logo_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# Certificate Use Case dependency
def get_generate_certificate_use_case(
    db: DatabaseSession
) -> GenerateCertificateUseCase:
    """Получить Use Case для генерации сертификата"""
    return GenerateCertificateUseCase(db)


GenerateCertificateUseCaseDep = Annotated[GenerateCertificateUseCase, Depends(get_generate_certificate_use_case)]


# Sign image loader helper
def load_sign_img_base64() -> str:
    """Загрузить изображение подписи в формате base64"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    sign_path = os.path.join(base_dir, "templates", "sign_img.png")

    if not os.path.exists(sign_path):
        # Возвращаем пустую строку если изображение не найдено
        return ""

    with open(sign_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


# Background certificate images loaders
def load_bg_certificate_en() -> str:
    """Загрузить фон для английского сертификата в формате base64"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    bg_path = os.path.join(base_dir, "templates", "bg_certificate_en.png")

    if not os.path.exists(bg_path):
        return ""

    with open(bg_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def load_bg_certificate_kk() -> str:
    """Загрузить фон для казахского сертификата в формате base64"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    bg_path = os.path.join(base_dir, "templates", "bg_certificate_kk.png")

    if not os.path.exists(bg_path):
        return ""

    with open(bg_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
