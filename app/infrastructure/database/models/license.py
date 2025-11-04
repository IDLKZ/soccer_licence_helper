"""
License SQLAlchemy Model
ORM модель для лицензий
"""
from datetime import datetime
from sqlalchemy import Integer, String, Boolean, Date, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.models.base import Base, TimestampMixin


class LicenseModel(Base, TimestampMixin):
    """ORM модель для таблицы licences"""

    __tablename__ = "licences"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    season_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("seasons.id", ondelete="CASCADE"),
        nullable=True
    )
    league_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("leagues.id", ondelete="CASCADE"),
        nullable=True
    )
    title_ru: Mapped[str] = mapped_column(String(255), nullable=False)
    title_kk: Mapped[str] = mapped_column(String(255), nullable=False)
    title_en: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_kk: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_at: Mapped[datetime] = mapped_column(Date, nullable=False)
    end_at: Mapped[datetime] = mapped_column(Date, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    season: Mapped["SeasonModel"] = relationship("SeasonModel", foreign_keys=[season_id])
    league: Mapped["LeagueModel"] = relationship("LeagueModel", foreign_keys=[league_id])
