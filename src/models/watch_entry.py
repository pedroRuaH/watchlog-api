"""Modelo puente que guarda el progreso del usuario."""

from __future__ import annotations

from datetime import datetime, timezone

from src.extensions import db



class WatchEntry(db.Model):
    """Relacion entre un usuario y un contenido (pelicula o serie)."""

    __tablename__ = "watch_entries"

    # TODO: definir columnas basicas (id, user_id, content_type, content_id, status).
    # TODO: agregar columnas de progreso (current_season, current_episode, watched_episodes, total_episodes).
    # TODO: establecer claves foraneas hacia User, Movie y Series segun el tipo.

    # TODO: modelar las relaciones back_populates con User, Movie y Series.

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    content_id = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=True)
    status = db.Column(db.String(50), nullable=False, default="watching")
    current_season = db.Column(db.Integer, nullable=True)
    current_episode = db.Column(db.Integer, nullable=True)
    watched_episodes = db.Column(db.Integer, nullable=True, default=0)
    total_episodes = db.Column(db.Integer, nullable=True)
    
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relacion con User
    user = db.relationship(
        "User",
        back_populates="watch_entries",
    )
    # Relacion con Movie
    movie = db.relationship(
        "Movie",
        back_populates="watch_entries",
    )
    # Relacion con Series
    series = db.relationship(
        "Serie",
        back_populates="watch_entries",
    )

    def percentage_watched(self) -> float:
        """Calcula el porcentaje completado para el contenido asociado."""
        # TODO: implementar calculo utilizando watched_episodes y total_episodes.
        total = self.total_episodes or 0
        watched = self.watched_episodes or 0
        if total <= 0:
            return 100.0 if self.status == "completed" else 0.0
        pct = (watched / float(total)) * 100.0
        return max(0.0, min(100.0, round(pct, 2)))

    def mark_as_watched(self) -> None:
        """Marca el contenido como completado."""
        # TODO: actualizar atributos y timestamps para reflejar el estado final.
        if self.total_episodes and (self.watched_episodes or 0) < self.total_episodes:
            self.watched_episodes = self.total_episodes
        self.status = "completed"
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """Serializa la entrada para respuestas JSON."""
        # TODO: reemplazar con serializacion acorde al modelo final.
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
