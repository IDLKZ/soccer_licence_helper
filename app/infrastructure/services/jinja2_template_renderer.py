"""
Jinja2 Template Renderer Implementation
Реализация рендеринга шаблонов через Jinja2
"""
import os
from typing import Any, Dict
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from app.domain.services.template_renderer import ITemplateRenderer


class Jinja2TemplateRenderer(ITemplateRenderer):
    """Рендеринг шаблонов через Jinja2"""

    def __init__(self, templates_dir: str):
        """
        Инициализация рендерера

        Args:
            templates_dir: Директория с шаблонами
        """
        if not os.path.exists(templates_dir):
            raise FileNotFoundError(f"Templates directory not found: {templates_dir}")

        self.env = Environment(loader=FileSystemLoader(templates_dir))

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Отрендерить шаблон

        Args:
            template_name: Имя файла шаблона
            context: Данные для шаблона

        Returns:
            HTML строка

        Raises:
            FileNotFoundError: Если шаблон не найден
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except TemplateNotFound as e:
            raise FileNotFoundError(f"Template not found: {template_name}") from e
