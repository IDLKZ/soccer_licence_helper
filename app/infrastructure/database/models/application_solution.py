"""
ApplicationSolution SQLAlchemy Model
ORM модель для решений по заявкам
"""
from datetime import datetime, date
from sqlalchemy import Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class ApplicationSolutionModel(Base, TimestampMixin):
    """ORM модель для таблицы application_solutions"""

    __tablename__ = "application_solutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )
    secretary_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )
    secretary_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    meeting_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    meeting_place: Mapped[str | None] = mapped_column(Text, nullable=True)
    department_name: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    application: Mapped["ApplicationModel"] = relationship(
        "ApplicationModel",
        foreign_keys=[application_id]
    )
