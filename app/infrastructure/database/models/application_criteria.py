"""
ApplicationCriteria SQLAlchemy Model
ORM модель для критериев заявки - реальная структура БД
"""
from sqlalchemy import Integer, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class ApplicationCriteriaModel(Base, TimestampMixin):
    """ORM модель для таблицы application_criteria"""

    __tablename__ = "application_criteria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("category_documents.id", ondelete="CASCADE"),
        nullable=False
    )
    status_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Uploaded by
    uploaded_by_id: Mapped[int] = mapped_column(Integer, nullable=False)
    uploaded_by: Mapped[str | None] = mapped_column(Text, nullable=True)

    # First check
    first_checked_by_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_checked_by: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Regular check
    checked_by_id: Mapped[int] = mapped_column(Integer, nullable=False)
    checked_by: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Control check
    control_checked_by_id: Mapped[int] = mapped_column(Integer, nullable=False)
    control_checked_by: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Status flags
    is_ready: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_first_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_industry_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_final_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_reupload_after_ending: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_reupload_after_endings_doc_ids: Mapped[list | None] = mapped_column(JSON, nullable=True)

    # Relationships
    application: Mapped["ApplicationModel"] = relationship(
        "ApplicationModel",
        foreign_keys=[application_id]
    )
    category: Mapped["CategoryDocumentModel"] = relationship(
        "CategoryDocumentModel",
        foreign_keys=[category_id]
    )
