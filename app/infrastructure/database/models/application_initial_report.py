"""
ApplicationInitialReport SQLAlchemy Model
ORM модель для начальных отчетов по заявкам
"""
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class ApplicationInitialReportModel(Base, TimestampMixin):
    """ORM модель для таблицы application_initial_reports"""

    __tablename__ = "application_initial_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("applications.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True
    )
    criteria_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("application_criteria.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True
    )
    status: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    application: Mapped["ApplicationModel"] = relationship(
        "ApplicationModel",
        foreign_keys=[application_id]
    )
    criteria: Mapped["ApplicationCriteriaModel"] = relationship(
        "ApplicationCriteriaModel",
        foreign_keys=[criteria_id]
    )
