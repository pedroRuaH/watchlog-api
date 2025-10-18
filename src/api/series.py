"""Endpoints relacionados con series y temporadas."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

bp = Blueprint("series", __name__, url_prefix="/series")


class SeriesService:
    """Gestiona las operaciones CRUD sobre Series y Seasons."""

    # TODO: inyectar modelos Series y Season junto a la sesion de base de datos.

    def list_series(self) -> list[dict]:
        """Retorna la lista de series disponibles."""
        # TODO: consultar las series existentes y devolverlas serializadas.
        pass

    def create_series(self, payload: dict) -> dict:
        """Crea una nueva serie."""
        # TODO: validar payload (titulo, temporadas, etc.) y persistir la serie.
        pass

    def get_series(self, series_id: int) -> dict:
        """Obtiene una serie y sus temporadas asociadas."""
        # TODO: recuperar el registro y manejar la ausencia del recurso.
        pass

    def update_series(self, series_id: int, payload: dict) -> dict:
        """Actualiza los campos permitidos de una serie."""
        # TODO: definir que campos son editables e implementar la actualizacion.
        pass

    def delete_series(self, series_id: int) -> None:
        """Elimina una serie del catalogo."""
        # TODO: decidir estrategia de borrado e implementarla.
        pass

    def add_season(self, series_id: int, payload: dict) -> dict:
        """Agrega una temporada a una serie existente."""
        # TODO: validar numero de temporada y cantidad de episodios.
        pass


service = SeriesService()


@bp.get("/")
def list_series():
    """Devuelve todas las series registradas."""
    # TODO: invocar service.list_series y devolver respuesta paginada si aplica.
    return jsonify({"detail": "TODO: implementar listado de series"}), 501


@bp.post("/")
def create_series():
    """Crea una nueva serie."""
    payload = request.get_json(silent=True) or {}
    # TODO: usar service.create_series y devolver 201 con la nueva serie.
    return (
        jsonify(
            {
                "detail": "TODO: implementar creacion de serie",
                "payload_example": payload,
            }
        ),
        501,
    )


@bp.get("/<int:series_id>")
def retrieve_series(series_id: int):
    """Devuelve los detalles de una serie."""
    # TODO: invocar service.get_series y construir respuesta con temporadas.
    return (
        jsonify(
            {
                "detail": "TODO: implementar recuperacion de serie",
                "series_id": series_id,
            }
        ),
        501,
    )


@bp.put("/<int:series_id>")
def update_series(series_id: int):
    """Actualiza la informacion de una serie."""
    payload = request.get_json(silent=True) or {}
    # TODO: invocar service.update_series y devolver la serie actualizada.
    return (
        jsonify(
            {
                "detail": "TODO: implementar actualizacion de serie",
                "series_id": series_id,
                "payload_example": payload,
            }
        ),
        501,
    )


@bp.delete("/<int:series_id>")
def delete_series(series_id: int):
    """Elimina una serie del catalogo."""
    # TODO: invocar service.delete_series y devolver 204.
    return (
        jsonify(
            {
                "detail": "TODO: implementar borrado de serie",
                "series_id": series_id,
            }
        ),
        501,
    )


@bp.post("/<int:series_id>/seasons")
def add_season(series_id: int):
    """Agrega una temporada a una serie existente."""
    payload = request.get_json(silent=True) or {}
    # TODO: invocar service.add_season y devolver la temporada creada.
    return (
        jsonify(
            {
                "detail": "TODO: implementar creacion de temporada",
                "series_id": series_id,
                "payload_example": payload,
            }
        ),
        501,
    )
