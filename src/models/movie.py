"""Modelo principal para las peliculas."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON

from src.extensions import db


class Movie(db.Model):
    """Representa una pelicula dentro del catalogo."""

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    genre = db.Column(JSON, nullable=False, default=list)
    release_year = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # TODO: crear relacion con WatchEntry (one-to-many) si aplica.
    watch_entries = db.relationship(
        "WatchEntry",
        back_populates="movie",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        # TODO: ajustar los campos utilizados en la representacion.
        return f"<Movie id={getattr(self, 'id', None)} title={getattr(self, 'title', None)} year={getattr(self, 'release_year', None)}>"

    def to_dict(self) -> dict:
        """Serializa la instancia para respuestas JSON."""
        # TODO: reemplazar esta implementacion temporal por serializacion real.
        created = getattr(self, "created_at", datetime.now(timezone.utc))
        return {
            "id": getattr(self, "id", None),
            "title": getattr(self, "title", None),
            "genre": getattr(self, "genre", None),
            "release_year": getattr(self, "release_year", None),
            "created_at": created.isoformat(),
        }
