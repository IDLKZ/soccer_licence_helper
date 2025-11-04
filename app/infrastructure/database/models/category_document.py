"""
CategoryDocument SQLAlchemy Model
ORM модель для категорий документов
"""
from sqlalchemy import Integer, String, Boolean, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base, TimestampMixin


class CategoryDocumentModel(Base, TimestampMixin):
    """ORM модель для таблицы category_documents"""

    __tablename__ = "category_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_kk: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    value: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    roles: Mapped[list | None] = mapped_column(JSON, nullable=True)
