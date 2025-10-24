"""Endpoints relacionados con series y temporadas."""

from __future__ import annotations

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, NotFound

from src.extensions import db
from src.models import Serie, Season

bp = Blueprint("series", __name__, url_prefix="/series")


class SeriesService:
    """Gestiona las operaciones CRUD sobre Series y Seasons."""

    # TODO: inyectar modelos Series y Season junto a la sesion de base de datos.
    def __init__(self, session=None, series_model=None, season_model=None) -> None:
        self.session = session or db.session
        self.series_model = series_model or Serie
        self.season_model = season_model or Season

    def list_series(self) -> list[dict]:
        """Retorna la lista de series disponibles."""
        # TODO: consultar las series existentes y devolverlas serializadas.
        items = self.session.execute(db.select(self.series_model)).scalars().all()
        return [s.to_dict() for s in items]

    def create_series(self, payload: dict) -> dict:
        """Crea una nueva serie."""
        # TODO: validar payload (titulo, temporadas, etc.) y persistir la serie.
        if not isinstance(payload, dict):
            raise BadRequest("El cuerpo de la solicitud debe ser un objeto JSON.")

        title = payload.get("title")
        if not title or not isinstance(title, str) or not title.strip():
            raise BadRequest("titulo invalido o faltante")

        total_seasons = payload.get("total_seasons", 1)
        if total_seasons is not None:
            if not isinstance(total_seasons, int) or total_seasons < 1:
                raise BadRequest("total_seasons debe ser un entero >= 1")

        serie = self.series_model(
            title=title.strip(),
            total_seasons=total_seasons,
        )
        self.session.add(serie)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return serie.to_dict()

    def get_series(self, series_id: int) -> dict:
        """Obtiene una serie y sus temporadas asociadas."""
        # TODO: recuperar el registro y manejar la ausencia del recurso.
        serie = self.session.get(self.series_model, series_id)
        if not serie:
            raise NotFound(f"Serie con id {series_id} no encontrada")
        return serie.to_dict(include_seasons=True)

    def update_series(self, series_id: int, payload: dict) -> dict:
        """Actualiza los campos permitidos de una serie."""
        # TODO: definir que campos son editables e implementar la actualizacion.
        if not isinstance(payload, dict):
            raise BadRequest("El cuerpo de la solicitud debe ser un objeto JSON.")

        serie = self.session.get(self.series_model, series_id)
        if not serie:
            raise NotFound(f"Serie con id {series_id} no encontrada")

        if "title" in payload:
            title = payload.get("title")
            if title is None or not isinstance(title, str) or not title.strip():
                raise BadRequest("titulo invalido o faltante")
            serie.title = title.strip()

        if "total_seasons" in payload:
            ts = payload.get("total_seasons")
            if ts is None or not isinstance(ts, int) or ts < 1:
                raise BadRequest("total_seasons debe ser un entero >= 1")
            # Evitar poner menos que la cantidad de seasons ya creadas
            existing_count = self.session.execute(
                db.select(db.func.count(self.season_model.id)).where(self.season_model.series_id == series_id)
            ).scalar_one()
            if ts < (existing_count or 0):
                raise BadRequest("total_seasons no puede ser menor a temporadas ya registradas")
            serie.total_seasons = ts

        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return serie.to_dict(include_seasons=True)

    def delete_series(self, series_id: int) -> None:
        """Elimina una serie del catalogo."""
        # TODO: decidir estrategia de borrado e implementarla.
        serie = self.session.get(self.series_model, series_id)
        if not serie:
            raise NotFound(f"Serie con id {series_id} no encontrada")
        self.session.delete(serie)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def add_season(self, series_id: int, payload: dict) -> dict:
        """Agrega una temporada a una serie existente."""
        # TODO: validar numero de temporada y cantidad de episodios.
        if not isinstance(payload, dict):
            raise BadRequest("El cuerpo de la solicitud debe ser un objeto JSON.")

        serie = self.session.get(self.series_model, series_id)
        if not serie:
            raise NotFound(f"Serie con id {series_id} no encontrada")

        number = payload.get("number")
        episodes_count = payload.get("episodes_count", 0)

        if number is None or not isinstance(number, int) or number < 1:
            raise BadRequest("number debe ser un entero >= 1")
        if not isinstance(episodes_count, int) or episodes_count < 0:
            raise BadRequest("episodes_count debe ser un entero >= 0")

        # Unicidad por (series_id, number)
        existing = self.session.execute(
            db.select(self.season_model).where(
                self.season_model.series_id == series_id,
                self.season_model.number == number,
            )
        ).scalars().first()
        if existing:
            raise BadRequest(f"La temporada {number} ya existe para la serie {series_id}")

        season = self.season_model(
            series_id=series_id,
            number=number,
            episodes_count=episodes_count,
        )
        self.session.add(season)

        # Mantener total_seasons como max(number, total_seasons)
        if number > (serie.total_seasons or 0):
            serie.total_seasons = number

        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return season.to_dict()


service = SeriesService()


@bp.get("/")
def list_series():
    """Devuelve todas las series registradas."""
    # TODO: invocar service.list_series y devolver respuesta paginada si aplica.
    try:
        return jsonify(service.list_series()), 200
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400


@bp.post("/")
def create_series():
    """Crea una nueva serie."""
    payload = request.get_json(silent=True) or {}
    # TODO: usar service.create_series y devolver 201 con la nueva serie.
    try:
        created = service.create_series(payload)
        return jsonify(created), 201
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400


@bp.get("/<int:series_id>")
def retrieve_series(series_id: int):
    """Devuelve los detalles de una serie."""
    # TODO: invocar service.get_series y construir respuesta con temporadas.
    try:
        return jsonify(service.get_series(series_id)), 200
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404


@bp.put("/<int:series_id>")
def update_series(series_id: int):
    """Actualiza la informacion de una serie."""
    payload = request.get_json(silent=True) or {}
    # TODO: invocar service.update_series y devolver la serie actualizada.
    try:
        return jsonify(service.update_series(series_id, payload)), 200
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400


@bp.delete("/<int:series_id>")
def delete_series(series_id: int):
    """Elimina una serie del catalogo."""
    # TODO: invocar service.delete_series y devolver 204.
    try:
        service.delete_series(series_id)
        return "", 204
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404


@bp.post("/<int:series_id>/seasons")
def add_season(series_id: int):
    """Agrega una temporada a una serie existente."""
    payload = request.get_json(silent=True) or {}
    # TODO: invocar service.add_season y devolver la temporada creada.
    try:
        created = service.add_season(series_id, payload)
        return jsonify(created), 201
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400
