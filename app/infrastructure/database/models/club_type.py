"""
ClubType SQLAlchemy Model
ORM модель для типов клубов
"""
from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base, TimestampMixin


class ClubTypeModel(Base, TimestampMixin):
    """ORM модель для таблицы club_types"""

    __tablename__ = "club_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_kk: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_kk: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    value: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
