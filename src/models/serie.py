"""Modelo para series disponibles en el catalogo."""

from __future__ import annotations

from datetime import datetime, timezone

from src.extensions import db

from sqlalchemy import String, Integer, DateTime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.season import Season
from src.models.watch_entry import WatchEntry


class Serie(db.Model):
    """Representa una serie cargada por los usuarios."""

    __tablename__ = "series"

    # TODO: definir columnas (id, title, total_seasons, created_at, updated_at).
    # TODO: agregar columnas opcionales (synopsis, genres, image_url) si se desean.

    # TODO: configurar relacion con Season (one-to-many) y WatchEntry.
    # seasons = db.relationship("Season", back_populates="series", lazy="joined")

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    total_seasons: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Serie -> Season (one to many collection)
    seasons: Mapped[list[Season]] = relationship(
        back_populates="series",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    # Serie -> WatchEntry (one to many collection)
    watch_entries: Mapped[list[WatchEntry]] = relationship(
        back_populates="series",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Series id={self.id} title={self.title}>"

    def to_dict(self, include_seasons: bool = False) -> dict:
        """Serializa la serie y opcionalmente sus temporadas."""
        # TODO: reemplazar por serializacion real usando marshmallow o similar.
        created = getattr(self, "created_at", datetime.now(timezone.utc))
        data = {
            "id": getattr(self, "id", None),
            "title": getattr(self, "title", None),
            "total_seasons": getattr(self, "total_seasons", None),
            "created_at": created.isoformat(),
        }
        if include_seasons:
            # TODO: serializar temporadas reales en lugar de lista vacia.
            data["seasons"] = [s.to_dict() for s in getattr(self, "seasons", [])]
        return data
