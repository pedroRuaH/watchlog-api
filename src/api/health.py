"""Endpoints de verificacion rapida de la API."""

from __future__ import annotations
from flask import Blueprint, jsonify, Response
from datetime import datetime, timezone
from time import perf_counter
from sqlalchemy import text
from src.extensions import db


bp = Blueprint("health", __name__, url_prefix="/health")


@bp.get("/")
def healthcheck() -> tuple[Response, int]:
    """Devuelve el estado actual de la aplicacion."""
    # TODO: agregar comprobaciones reales (db, cache, servicios externos).
    overall_ok = True

    # Comprobacion de base de datos
    database_status = "ok"
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        try:
            db.session.rollback()
        except Exception:
            pass
        database_status = "error"
        overall_ok = False

    payload: dict[str, str] = {
        "status": "ok" if overall_ok else "error",
        "database": database_status,
        "time": datetime.now(timezone.utc).isoformat(),
    }
    return jsonify(payload), 200 if overall_ok else 500