"""
Template Renderer Service Interface
Интерфейс сервиса для рендеринга HTML шаблонов
"""
from abc import ABC, abstractmethod
from typing import Any, Dict


class ITemplateRenderer(ABC):
    """Интерфейс для рендеринга шаблонов"""

    @abstractmethod
    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Отрендерить шаблон с переданным контекстом

        Args:
            template_name: Имя файла шаблона (например, "report_template.html")
            context: Словарь с данными для шаблона

        Returns:
            HTML строка

        Raises:
            FileNotFoundError: Если шаблон не найден
            Exception: Другие ошибки рендеринга
        """
        pass
