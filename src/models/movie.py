"""Modelo principal para las peliculas."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, String, Integer

from src.extensions import db

from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.models.watch_entry import WatchEntry


class Movie(db.Model):
    """Representa una pelicula dentro del catalogo."""

    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    genre: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    # Movie -> WatchEntry (one to many collection)
    watch_entries: Mapped[list[WatchEntry]] = relationship(
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
