"""
ApplicationDocument SQLAlchemy Model
ORM модель для документов заявки - реальная структура БД
"""
from datetime import datetime
from sqlalchemy import Integer, Boolean, ForeignKey, Date, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class ApplicationDocumentModel(Base, TimestampMixin):
    """ORM модель для таблицы application_documents"""

    __tablename__ = "application_documents"

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
    document_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False
    )
    file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Uploaded by
    uploaded_by_id: Mapped[int] = mapped_column(Integer, nullable=False)
    uploaded_by: Mapped[str | None] = mapped_column(Text, nullable=True)

    # First check (первичная проверка)
    first_checked_by_id: Mapped[int] = mapped_column(Integer, nullable=False)
    first_checked_by: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_first_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    first_comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Regular/Industry check (отраслевая проверка)
    checked_by_id: Mapped[int] = mapped_column(Integer, nullable=False)
    checked_by: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_industry_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    industry_comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Control check (контрольная проверка)
    control_checked_by_id: Mapped[int] = mapped_column(Integer, nullable=False)
    control_checked_by: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_final_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    control_comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Document info
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    info: Mapped[str | None] = mapped_column(Text, nullable=True)
    deadline: Mapped[datetime | None] = mapped_column(Date, nullable=True)

    # Relationships
    application: Mapped["ApplicationModel"] = relationship(
        "ApplicationModel",
        foreign_keys=[application_id]
    )
    category: Mapped["CategoryDocumentModel"] = relationship(
        "CategoryDocumentModel",
        foreign_keys=[category_id]
    )
    document: Mapped["DocumentModel"] = relationship(
        "DocumentModel",
        foreign_keys=[document_id]
    )
