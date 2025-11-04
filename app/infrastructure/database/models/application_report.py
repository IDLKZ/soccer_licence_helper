"""
ApplicationReport SQLAlchemy Model
ORM модель для отчетов по заявкам
"""
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class ApplicationReportModel(Base, TimestampMixin):
    """ORM модель для таблицы application_reports"""

    __tablename__ = "application_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )
    criteria_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("application_criteria.id", ondelete="CASCADE"),
        nullable=False
    )
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    # file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)  # Нет в БД

    # Relationships
    application: Mapped["ApplicationModel"] = relationship(
        "ApplicationModel",
        foreign_keys=[application_id]
    )
    criteria: Mapped["ApplicationCriteriaModel"] = relationship(
        "ApplicationCriteriaModel",
        foreign_keys=[criteria_id]
    )
