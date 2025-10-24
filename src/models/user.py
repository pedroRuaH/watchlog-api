"""Modelo para usuarios que usan la plataforma."""

from __future__ import annotations

from datetime import datetime, timezone

from src.extensions import db



class User(db.Model):
    """Representa a un usuario (simulado mediante el header X-User-Id)."""

    __tablename__ = "users"

    # TODO: definir columnas (id, name, email opcional, created_at).
    # TODO: agregar relacion con WatchEntry (one-to-many).

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relacion con WatchEntry
    watch_entries = db.relationship(
        "WatchEntry",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def __repr__(self) -> str:
        """Devuelve una representacion legible del usuario."""
        return f"<User id={getattr(self, 'id', None)} name={getattr(self, 'name', None)}>"

    def to_dict(self) -> dict:
        """Serializa al usuario para respuestas JSON."""
        # TODO: reemplazar esta implementacion por serializacion real.
        created = getattr(self, "created_at", datetime.now(timezone.utc))
        return {
            "id": getattr(self, "id", None),
            "name": getattr(self, "name", None),
            "email": getattr(self, "email", None),
            "created_at": created.isoformat(),
        }
