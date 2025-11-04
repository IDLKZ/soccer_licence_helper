"""
SQLAlchemy database models
Модели базы данных
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum, JSON
from sqlalchemy.sql import func
from app.core.database import Base
from app.domain.entities.report import ReportStatus, ReportType
import enum


class ReportModel(Base):
    """Модель отчета в БД"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    report_type = Column(
        SQLEnum(ReportType),
        nullable=False,
        index=True
    )
    status = Column(
        SQLEnum(ReportStatus),
        nullable=False,
        default=ReportStatus.PENDING,
        index=True
    )
    parameters = Column(JSON, nullable=False)
    file_path = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    completed_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<Report(id={self.id}, name={self.name}, status={self.status})>"
