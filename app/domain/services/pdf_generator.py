"""
PDF Generator Service Interface
Интерфейс сервиса для генерации PDF из HTML
"""
from abc import ABC, abstractmethod


class IPDFGenerator(ABC):
    """Интерфейс для генерации PDF"""

    @abstractmethod
    def generate_from_html(self, html_content: str, output_path: str) -> None:
        """
        Сгенерировать PDF файл из HTML строки

        Args:
            html_content: HTML контент для конвертации
            output_path: Путь для сохранения PDF файла

        Raises:
            Exception: Ошибки при генерации PDF
        """
        pass
