"""
Season SQLAlchemy Model
ORM модель для сезонов
"""
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base, TimestampMixin


class SeasonModel(Base, TimestampMixin):
    """ORM модель для таблицы seasons"""

    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_kk: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    value: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    start: Mapped[datetime] = mapped_column(Date, nullable=False)
    end: Mapped[datetime] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
