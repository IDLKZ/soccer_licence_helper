"""
Document SQLAlchemy Model
ORM модель для документов (справочник)
"""
from sqlalchemy import Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class DocumentModel(Base, TimestampMixin):
    """ORM модель для таблицы documents - справочник документов"""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("category_documents.id", ondelete="CASCADE"),
        nullable=False
    )
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_kk: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    category: Mapped["CategoryDocumentModel"] = relationship(
        "CategoryDocumentModel",
        foreign_keys=[category_id]
    )
