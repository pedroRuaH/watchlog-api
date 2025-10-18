"""Modelo para series disponibles en el catalogo."""

from __future__ import annotations

from datetime import datetime

from src.extensions import db


class Series(db.Model):
    """Representa una serie cargada por los usuarios."""

    __tablename__ = "series"

    # TODO: definir columnas (id, title, total_seasons, created_at, updated_at).
    # TODO: agregar columnas opcionales (synopsis, genres, image_url) si se desean.

    # TODO: configurar relacion con Season (one-to-many) y WatchEntry.
    # seasons = db.relationship("Season", back_populates="series", lazy="joined")

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        return f"<Series id={getattr(self, 'id', None)} title={getattr(self, 'title', None)}>"

    def to_dict(self, include_seasons: bool = False) -> dict:
        """Serializa la serie y opcionalmente sus temporadas."""
        # TODO: reemplazar por serializacion real usando marshmallow o similar.
        data = {
            "id": getattr(self, "id", None),
            "title": getattr(self, "title", None),
            "total_seasons": getattr(self, "total_seasons", None),
            "created_at": getattr(self, "created_at", datetime.utcnow()),
        }
        if include_seasons:
            # TODO: serializar temporadas reales en lugar de lista vacia.
            data["seasons"] = []
        return data
