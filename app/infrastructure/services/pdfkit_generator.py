"""
PDFKit Generator Implementation
Реализация генерации PDF через pdfkit/wkhtmltopdf
"""
import os
from sys import platform
import pdfkit
from app.domain.services.pdf_generator import IPDFGenerator


class PdfKitGenerator(IPDFGenerator):
    """Генерация PDF через pdfkit"""

    def __init__(self):
        """Инициализация генератора с конфигурацией для платформы"""
        # Конфигурация для Windows
        if platform == "win32":
            path_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
            self.config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
        else:
            # На Linux wkhtmltopdf будет найден автоматически
            self.config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")

        # Опции для генерации PDF
        self.options = {
            "enable-local-file-access": None,  # Разрешает локальные файлы
            "encoding": "UTF-8",  # Рекомендуется для кириллицы
            "quiet": "",  # Убирает лишний вывод
        }

    def generate_from_html(self, html_content: str, output_path: str) -> None:
        """
        Сгенерировать PDF из HTML

        Args:
            html_content: HTML контент
            output_path: Путь для сохранения PDF

        Raises:
            Exception: Ошибки при генерации
        """
        try:
            pdfkit.from_string(
                html_content,
                output_path,
                configuration=self.config,
                options=self.options
            )
        except Exception as e:
            raise Exception(f"Failed to generate PDF: {str(e)}") from e
