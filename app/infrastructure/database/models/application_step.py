"""
ApplicationStep SQLAlchemy Model
ORM модель для шагов заявки
"""
from datetime import datetime
from sqlalchemy import Integer, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class ApplicationStepModel(Base, TimestampMixin):
    """ORM модель для таблицы application_steps"""

    __tablename__ = "application_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )
    application_criteria_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("application_criteria.id", ondelete="CASCADE"),
        nullable=False
    )
    status_id: Mapped[int] = mapped_column(Integer, nullable=False)
    responsible_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False
    )
    file_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsible_by: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    result: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    application: Mapped["ApplicationModel"] = relationship(
        "ApplicationModel",
        foreign_keys=[application_id]
    )
    responsible: Mapped["UserModel"] = relationship(
        "UserModel",
        foreign_keys=[responsible_id]
    )
