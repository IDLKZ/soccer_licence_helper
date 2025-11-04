"""
League SQLAlchemy Model
ORM модель для лиг
"""
from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base, TimestampMixin


class LeagueModel(Base, TimestampMixin):
    """ORM модель для таблицы leagues"""

    __tablename__ = "leagues"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_kk: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_kk: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    value: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    # level_ru: Mapped[str] = mapped_column(String(100), nullable=False)  # Нет в БД
    # level_kk: Mapped[str] = mapped_column(String(100), nullable=False)  # Нет в БД
    # level_en: Mapped[str | None] = mapped_column(String(100), nullable=True)  # Нет в БД
    # level_value: Mapped[int] = mapped_column(Integer, nullable=False)  # В БД просто level
