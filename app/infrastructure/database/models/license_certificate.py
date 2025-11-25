"""
LicenseCertificate SQLAlchemy Model
ORM модель для сертификатов лицензий
"""
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class LicenseCertificateModel(Base, TimestampMixin):
    """ORM модель для таблицы license_certificates"""

    __tablename__ = "license_certificates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    application_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("applications.id", ondelete="CASCADE"),
        nullable=False
    )
    license_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("licences.id", ondelete="CASCADE"),
        nullable=False
    )
    club_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("clubs.id", ondelete="CASCADE"),
        nullable=False
    )
    type_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)
    type_kk: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    application: Mapped["ApplicationModel"] = relationship(
        "ApplicationModel",
        foreign_keys=[application_id]
    )
    license: Mapped["LicenseModel"] = relationship(
        "LicenseModel",
        foreign_keys=[license_id]
    )
    club: Mapped["ClubModel"] = relationship(
        "ClubModel",
        foreign_keys=[club_id]
    )
