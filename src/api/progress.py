"""Endpoints para controlar el progreso de los usuarios."""

from __future__ import annotations

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

from src.extensions import db
from src.models import User, Movie, Serie, WatchEntry, Season

bp = Blueprint("progress", __name__, url_prefix="")


class ProgressService:
    """Coordina operaciones sobre la lista de seguimiento y progreso."""

    # TODO: inyectar modelos User, Series, Movie y WatchEntry con sus esquemas.
    def __init__(
        self,
        session=None,
        user_model=None,
        movie_model=None,
        series_model=None,
        entry_model=None,
        season_model=None,
    ) -> None:
        self.session = session or db.session
        self.user_model = user_model or User
        self.movie_model = movie_model or Movie
        self.series_model = series_model or Serie
        self.entry_model = entry_model or WatchEntry
        self.season_model = season_model or Season

    def list_watchlist(self, user_id: int) -> list[dict]:
        """Devuelve los contenidos asociados a un usuario."""
        # TODO: consultar entradas filtradas por user_id y calcular porcentajes.
        user = self.session.get(self.user_model, user_id)
        if not user:
            raise NotFound(f"Usuario con id {user_id} no encontrado")

        items = self.session.execute(
            db.select(self.entry_model).where(self.entry_model.user_id == user_id)
        ).scalars().all()
        return [e.to_dict() for e in items]

    def add_movie(self, user_id: int, movie_id: int) -> dict:
        """Agrega una pelicula a la lista del usuario."""
        # TODO: validar existencia del usuario y pelicula antes de crear el registro.
        user = self.session.get(self.user_model, user_id)
        if not user:
            raise NotFound(f"Usuario con id {user_id} no encontrado")

        movie = self.session.get(self.movie_model, movie_id)
        if not movie:
            raise NotFound(f"Pelicula con id {movie_id} no encontrada")

        existing = self.session.execute(
            db.select(self.entry_model).where(
                self.entry_model.user_id == user_id,
                self.entry_model.content_type == "movie",
                self.entry_model.movie_id == movie_id,
            )
        ).scalars().first()
        if existing:
            raise BadRequest("La pelicula ya existe en la watchlist del usuario")

        entry = self.entry_model(
            user_id=user_id,
            content_type="movie",
            content_id=movie_id,
            movie_id=movie_id,
            status="watching",
            current_season=None,
            current_episode=None,
            watched_episodes=0,
            total_episodes=None,
        )
        self.session.add(entry)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return entry.to_dict()

    def add_series(self, user_id: int, series_id: int) -> dict:
        """Agrega una serie a la lista del usuario."""
        # TODO: crear WatchEntry inicial con temporadas/episodios en cero.
        user = self.session.get(self.user_model, user_id)
        if not user:
            raise NotFound(f"Usuario con id {user_id} no encontrado")

        serie = self.session.get(self.series_model, series_id)
        if not serie:
            raise NotFound(f"Serie con id {series_id} no encontrada")

        existing = self.session.execute(
            db.select(self.entry_model).where(
                self.entry_model.user_id == user_id,
                self.entry_model.content_type == "series",
                self.entry_model.series_id == series_id,
            )
        ).scalars().first()
        if existing:
            raise BadRequest("La serie ya existe en la watchlist del usuario")

        # Calcular total de episodios si hay temporadas cargadas
        try:
            seasons = serie.seasons.all()  # lazy="dynamic"
        except Exception:
            seasons = list(serie.seasons) if hasattr(serie, "seasons") else []
        total_eps = sum((s.episodes_count or 0) for s in seasons) if seasons else 0

        entry = self.entry_model(
            user_id=user_id,
            content_type="series",
            content_id=series_id,
            series_id=series_id,
            status="watching",
            current_season=1 if (serie.total_seasons or 0) >= 1 else None,
            current_episode=0,
            watched_episodes=0,
            total_episodes=total_eps or None,
        )
        self.session.add(entry)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return entry.to_dict()

    def update_series_progress(self, user_id: int, series_id: int, payload: dict) -> dict:
        """Actualiza el progreso de una serie en la lista del usuario."""
        # TODO: validar limites de temporadas y episodios, recalcular porcentaje.
        if not isinstance(payload, dict):
            raise BadRequest("El cuerpo de la solicitud debe ser un objeto JSON.")

        entry = self.session.execute(
            db.select(self.entry_model).where(
                self.entry_model.user_id == user_id,
                self.entry_model.content_type == "series",
                self.entry_model.series_id == series_id,
            )
        ).scalars().first()
        if not entry:
            raise NotFound("No existe una entrada de progreso para esta serie y usuario")

        serie = entry.series or self.session.get(self.series_model, series_id)

        # Validaciones y asignaciones opcionales
        if "current_season" in payload:
            cs = payload.get("current_season")
            if cs is not None and (not isinstance(cs, int) or cs < 1):
                raise BadRequest("current_season debe ser un entero >= 1 o null")
            if cs and serie and serie.total_seasons and cs > serie.total_seasons:
                raise BadRequest("current_season excede el total de temporadas de la serie")
            entry.current_season = cs

        if "current_episode" in payload:
            ce = payload.get("current_episode")
            if ce is not None and (not isinstance(ce, int) or ce < 0):
                raise BadRequest("current_episode debe ser un entero >= 0 o null")
            # Si se conoce la temporada actual, validamos contra episodes_count
            if ce and entry.current_season:
                season = self.session.execute(
                    db.select(self.season_model).where(
                        self.season_model.series_id == series_id,
                        self.season_model.number == entry.current_season,
                    )
                ).scalars().first()
                if season and ce > (season.episodes_count or 0):
                    raise BadRequest("current_episode excede los episodios de la temporada actual")
            entry.current_episode = ce

        if "total_episodes" in payload:
            te = payload.get("total_episodes")
            if te is not None and (not isinstance(te, int) or te < 0):
                raise BadRequest("total_episodes debe ser un entero >= 0 o null")
            entry.total_episodes = te

        if "watched_episodes" in payload:
            we = payload.get("watched_episodes")
            if we is not None and (not isinstance(we, int) or we < 0):
                raise BadRequest("watched_episodes debe ser un entero >= 0 o null")
            if we is not None and entry.total_episodes is not None and we > entry.total_episodes:
                raise BadRequest("watched_episodes no puede superar total_episodes")
            entry.watched_episodes = we

        if "status" in payload:
            status = payload.get("status")
            allowed = {"watching", "completed", "paused"}
            if status not in allowed:
                raise BadRequest(f"status invalido, opciones: {', '.join(sorted(allowed))}")
            entry.status = status
            if status == "completed":
                # Marca como visto por completo si conocemos el total
                if entry.total_episodes:
                    entry.watched_episodes = entry.total_episodes

        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return entry.to_dict()


service = ProgressService()


@bp.get("/me/watchlist")
def get_my_watchlist():
    """Devuelve la lista de seguimiento del usuario actual."""
    user_id = request.headers.get("X-User-Id", type=int)
    # TODO: validar el header y manejar autenticacion simulada.
    if not user_id:
        return jsonify({"detail": "Header X-User-Id requerido"}), 400
    try:
        return jsonify(service.list_watchlist(user_id)), 200
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400


@bp.post("/watchlist/movies/<int:movie_id>")
def add_movie_to_watchlist(movie_id: int):
    """Agrega una pelicula a la lista del usuario."""
    user_id = request.headers.get("X-User-Id", type=int)
    # TODO: invocar service.add_movie y devolver 201 con la entrada creada.
    if not user_id:
        return jsonify({"detail": "Header X-User-Id requerido"}), 400
    try:
        created = service.add_movie(user_id, movie_id)
        return jsonify(created), 201
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400


@bp.post("/watchlist/series/<int:series_id>")
def add_series_to_watchlist(series_id: int):
    """Agrega una serie a la lista del usuario."""
    user_id = request.headers.get("X-User-Id", type=int)
    # TODO: invocar service.add_series y devolver 201 con la entrada creada.
    if not user_id:
        return jsonify({"detail": "Header X-User-Id requerido"}), 400
    try:
        created = service.add_series(user_id, series_id)
        return jsonify(created), 201
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400


@bp.patch("/progress/series/<int:series_id>")
def update_series_progress(series_id: int):
    """Actualiza los datos de progreso de una serie."""
    user_id = request.headers.get("X-User-Id", type=int)
    payload = request.get_json(silent=True) or {}
    # TODO: invocar service.update_series_progress y devolver el recurso actualizado.
    if not user_id:
        return jsonify({"detail": "Header X-User-Id requerido"}), 400
    try:
        updated = service.update_series_progress(user_id, series_id, payload)
        return jsonify(updated), 200
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400
