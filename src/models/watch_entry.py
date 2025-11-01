"""Modelo puente que guarda el progreso del usuario."""

from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from src.extensions import db
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from src.models.movie import Movie
    from src.models.serie import Serie
    from src.models.user import User


class WatchEntry(db.Model):
    """Relacion entre un usuario y un contenido (pelicula o serie)."""

    __tablename__ = "watch_entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=True)
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="watching")
    current_season: Mapped[int] = mapped_column(Integer, nullable=True)
    current_episode: Mapped[int] = mapped_column(Integer, nullable=True)
    watched_episodes: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    total_episodes: Mapped[int] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    user: Mapped["User"] = relationship(
        back_populates="watch_entries",
    )
    
    movie: Mapped["Movie"] = relationship(
        back_populates="watch_entries",
    )
    
    series: Mapped["Serie"] = relationship(
        back_populates="watch_entries",
    )

    def percentage_watched(self) -> float:
        """Calcula el porcentaje completado para el contenido asociado."""
        total = self.total_episodes or 0
        watched = self.watched_episodes or 0
        if total <= 0:
            return 100.0 if self.status == "completed" else 0.0
        pct = (watched / float(total)) * 100.0
        return max(0.0, min(100.0, round(pct, 2)))

    def mark_as_watched(self) -> None:
        """Marca el contenido como completado."""
        if self.total_episodes and (self.watched_episodes or 0) < self.total_episodes:
            self.watched_episodes = self.total_episodes
        self.status = "completed"
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Serializa la entrada para respuestas JSON."""
        updated = getattr(self, "updated_at", datetime.now(timezone.utc))
        return {
            "id": getattr(self, "id", None),
            "user_id": getattr(self, "user_id", None),
            "content_type": getattr(self, "content_type", None),
            "movie_id": getattr(self, "movie_id", None),
            "series_id": getattr(self, "series_id", None),
            "content_id": getattr(self, "content_id", None),
            "status": getattr(self, "status", None),
            "current_season": getattr(self, "current_season", None),
            "current_episode": getattr(self, "current_episode", None),
            "watched_episodes": getattr(self, "watched_episodes", None),
            "total_episodes": getattr(self, "total_episodes", None),
            "percentage": self.percentage_watched(),
            "updated_at": updated.isoformat(),
        }
