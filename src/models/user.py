"""Modelo para usuarios que usan la plataforma."""

from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime, timezone
from src.extensions import db
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from src.models.watch_entry import WatchEntry

class User(db.Model):
    """Representa a un usuario (simulado mediante el header X-User-Id)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    watch_entries: Mapped[list["WatchEntry"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def __repr__(self) -> str:
        """Devuelve una representacion legible del usuario."""
        return f"<User id={getattr(self, 'id', None)} name={getattr(self, 'name', None)}>"

    def to_dict(self) -> dict:
        """Serializa al usuario para respuestas JSON."""
        created = getattr(self, "created_at", datetime.now(timezone.utc))
        return {
            "id": getattr(self, "id", None),
            "name": getattr(self, "name", None),
            "email": getattr(self, "email", None),
            "created_at": created.isoformat(),
        }
