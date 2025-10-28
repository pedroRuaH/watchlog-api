"""Modelo que representa una temporada de una serie."""

from __future__ import annotations
from src.extensions import db
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.models.serie import Serie
from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint



class Season(db.Model):
    """Temporada asociada a una serie."""

    __tablename__ = "seasons"
    __table_args__ = (
        UniqueConstraint("series_id", "number", name="uq_season_series_number"),
    )


    id: Mapped[int] = mapped_column(primary_key=True)
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id", ondelete="CASCADE"), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    episodes_count: Mapped[int] = mapped_column(Integer,nullable=False, default=0)

    # Relacion con Series
    series: Mapped[Serie] = relationship(
        back_populates="seasons",
        lazy="selectin", 
        
    )
    def to_dict(self) -> dict:
        """Serializa la temporada en un diccionario."""
        return {
            "id": getattr(self, "id", None),
            "series_id": getattr(self, "series_id", None),
            "number": getattr(self, "number", None),
            "episodes_count": getattr(self, "episodes_count", None),
        }
