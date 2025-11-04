"""
Application SQLAlchemy Model
ORM модель для заявок
"""
from datetime import datetime
from sqlalchemy import Integer, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class ApplicationModel(Base, TimestampMixin):
    """ORM модель для таблицы applications - реальная структура БД"""

    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    license_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("licences.id", ondelete="CASCADE"),  # licences с 'c'!
        nullable=False
    )
    club_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("clubs.id", ondelete="CASCADE"),
        nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("category_documents.id", ondelete="CASCADE"),
        nullable=False
    )
    is_ready: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)

    # Relationships
    club: Mapped["ClubModel"] = relationship("ClubModel", foreign_keys=[club_id])
    license: Mapped["LicenseModel"] = relationship("LicenseModel", foreign_keys=[license_id])
