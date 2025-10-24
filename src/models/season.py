"""Modelo que representa una temporada de una serie."""

from __future__ import annotations

from src.extensions import db


class Season(db.Model):
    """Temporada asociada a una serie."""

    __tablename__ = "seasons"

    # TODO: definir columnas (id, series_id, number, episodes_count).
    # TODO: establecer restriccion unica por (series_id, number).

    # TODO: configurar relacion back_populates con Series.
    # series = db.relationship("Series", back_populates="seasons")
    id = db.Column(db.Integer, primary_key=True)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    episodes_count = db.Column(db.Integer, nullable=False, default=0)
    
    # Relacion con Series
    series = db.relationship(
        "Serie",
        back_populates="seasons",
    )

    def to_dict(self) -> dict:
        """Serializa la temporada en un diccionario."""
        # TODO: reemplazar esta implementacion por la serializacion real.
        return {
            "id": getattr(self, "id", None),
            "series_id": getattr(self, "series_id", None),
            "number": getattr(self, "number", None),
            "episodes_count": getattr(self, "episodes_count", None),
        }
