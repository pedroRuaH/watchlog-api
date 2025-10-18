"""Modelo principal para las peliculas."""

from __future__ import annotations

from datetime import datetime

from src.extensions import db


class Movie(db.Model):
    """Representa una pelicula dentro del catalogo."""

    __tablename__ = "movies"

    # TODO: definir columnas (id, title, genre, release_year, created_at, updated_at).
    # Ejemplo:
    # id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(120), nullable=False)
    # ...

    # TODO: crear relacion con WatchEntry (one-to-many) si aplica.

    def __repr__(self) -> str:
        """Devuelve una representacion legible del modelo."""
        # TODO: ajustar los campos utilizados en la representacion.
        return f"<Movie id={getattr(self, 'id', None)} title={getattr(self, 'title', None)}>"

    def to_dict(self) -> dict:
        """Serializa la instancia para respuestas JSON."""
        # TODO: reemplazar esta implementacion temporal por serializacion real.
        return {
            "id": getattr(self, "id", None),
            "title": getattr(self, "title", None),
            "genre": getattr(self, "genre", None),
            "release_year": getattr(self, "release_year", None),
            "created_at": getattr(self, "created_at", datetime.utcnow()),
        }
