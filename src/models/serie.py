"""Modelo para series disponibles en el catalogo."""

from __future__ import annotations

from datetime import datetime, timezone

from src.extensions import db


class Serie(db.Model):
    """Representa una serie cargada por los usuarios."""

    __tablename__ = "series"

    # TODO: definir columnas (id, title, total_seasons, created_at, updated_at).
    # TODO: agregar columnas opcionales (synopsis, genres, image_url) si se desean.

    # TODO: configurar relacion con Season (one-to-many) y WatchEntry.
    # seasons = db.relationship("Season", back_populates="series", lazy="joined")

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    total_seasons = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    #Relacion con Season
    seasons = db.relationship(
        "Season",
        back_populates="series",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    #Relacion con WatchEntry
    watch_entries = db.relationship(
        "WatchEntry",
        back_populates="series",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Series id={getattr(self, 'id', None)} title={getattr(self, 'title', None)}>"

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
