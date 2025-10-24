"""Endpoints relacionados con peliculas."""

from __future__ import annotations
from flask import Blueprint, jsonify, request
from src.extensions import db
from src.models.movie import Movie
from werkzeug.exceptions import NotFound, BadRequest


bp = Blueprint("movies", __name__, url_prefix="/movies")


class MovieService:
    """Orquesta la logica de negocio para el recurso Movie."""

    # TODO: inyectar dependencias necesarias (db.session, modelos, esquemas, etc.).
    def __init__(self, session=None, model=None, schema=None) -> None:
        """Permite inyectar dependencias para facilitar pruebas."""
        self.session = session or db.session
        self.model = model or Movie
        self.schema = schema

    def list_movies(self) -> list[dict]:
        """Retorna todas las peliculas registradas."""
        # TODO: consultar la base de datos y serializar a una lista de dicts.
        items = self.session.execute(db.select(self.model)).scalars().all()
        return [item.to_dict() for item in items]

    def create_movie(self, payload: dict) -> dict:
        """Crea una nueva pelicula."""
        # TODO: validar el payload y persistir un nuevo registro Movie.
        if not isinstance(payload, dict):
            raise BadRequest("el cuerpo de la solicitud debe ser un diccionario")
        
        title = payload.get("title")
        if not title or not isinstance(title, str) or not title.strip():
            raise BadRequest("titulo invalido o faltante")
        
        movie = self.model(
            title=title.strip(),
            genre=payload.get("genre", []) or [],
            release_year=payload.get("release_year"),
        )
        self.session.add(movie)
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return movie.to_dict()

    def get_movie(self, movie_id: int) -> dict:
        """Obtiene una pelicula por su identificador."""
        # TODO: buscar la pelicula y manejar el caso de no encontrada.
        movie = self.session.get(self.model, movie_id)
        if not movie:
            raise NotFound(f"Pelicula con id {movie_id} no encontrada")
        return movie.to_dict()

    def update_movie(self, movie_id: int, payload: dict) -> dict:
        """Actualiza los datos de una pelicula."""
        # TODO: aplicar cambios permitidos y guardar en la base de datos.
        movie = self.session.get(self.model, movie_id)
        if not movie:
            raise NotFound(f"Pelicula con id {movie_id} no encontrada")
        
        if not isinstance(payload, dict):
            raise BadRequest("El cuerpo debe ser un objeto JSON.")
        
        if "title" in payload:
            title = payload.get("title")
            if title is None or not isinstance(title, str) or not title.strip():
                raise BadRequest("titulo invalido o faltante")
            movie.title = title.strip()
        
        if "genre" in payload:
            movie.genre = payload.get("genre", []) or []

        if "release_year" in payload:
            movie.release_year = payload.get("release_year")

        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        return movie.to_dict()

    def delete_movie(self, movie_id: int) -> None:
        """Elimina una pelicula existente."""
        # TODO: definir si el borrado debe ser logico o fisico.
        movie = self.session.get(self.model, movie_id)
        if not movie:
            raise NotFound(f"Pelicula con id {movie_id} no encontrada")
        
        self.session.delete(movie)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        


service = MovieService()


@bp.get("/")
def list_movies():
    """Lista todas las peliculas disponibles."""
    # TODO: invocar service.list_movies y devolver la respuesta serializada.
    try:
        return jsonify(service.list_movies()), 200
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400


@bp.post("/")
def create_movie():
    """Crea una pelicula a partir de los datos enviados."""
    payload = request.get_json(silent=True) or {}
    # TODO: validar payload, manejar errores y devolver el recurso creado.
    try:
        created_movie = service.create_movie(payload)
        return jsonify(created_movie), 201
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400

@bp.get("/<int:movie_id>")
def retrieve_movie(movie_id: int):
    """Devuelve el detalle de una pelicula concreta."""
    # TODO: invocar service.get_movie y manejar 404 cuando corresponda.
    try:
        return jsonify(service.get_movie(movie_id)), 200
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404


@bp.put("/<int:movie_id>")
def update_movie(movie_id: int):
    """Actualiza la informacion de una pelicula."""
    payload = request.get_json(silent=True) or {}
    # TODO: invocar service.update_movie y devolver el recurso actualizado.
    try:
        return jsonify(service.update_movie(movie_id, payload)), 200
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400


@bp.delete("/<int:movie_id>")
def delete_movie(movie_id: int):
    """Elimina una pelicula del catalogo."""
    # TODO: invocar service.delete_movie y devolver 204 al completar.
    try:
        service.delete_movie(movie_id)
        return "", 204
    except NotFound as nf:
        return jsonify({"detail": str(nf)}), 404
    except BadRequest as br:
        return jsonify({"detail": str(br)}), 400