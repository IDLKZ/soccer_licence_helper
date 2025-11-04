"""
Club SQLAlchemy Model
ORM модель для клубов
"""
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class ClubModel(Base, TimestampMixin):
    """ORM модель для таблицы clubs"""

    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("clubs.id", ondelete="SET NULL"),
        nullable=True
    )
    type_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("club_types.id", ondelete="SET NULL"),
        nullable=True
    )
    full_name_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name_kk: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    short_name_ru: Mapped[str] = mapped_column(String(100), nullable=False)
    short_name_kk: Mapped[str] = mapped_column(String(100), nullable=False)
    short_name_en: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_kk: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    bin: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)
    foundation_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    legal_address: Mapped[str] = mapped_column(Text, nullable=False)
    actual_address: Mapped[str] = mapped_column(Text, nullable=False)
    website: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(Text, nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    # is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)  # Нет в БД

    # Relationships
    parent: Mapped["ClubModel"] = relationship(
        "ClubModel",
        remote_side=[id],
        foreign_keys=[parent_id],
        back_populates="children"
    )
    children: Mapped[list["ClubModel"]] = relationship(
        "ClubModel",
        back_populates="parent",
        foreign_keys=[parent_id]
    )
