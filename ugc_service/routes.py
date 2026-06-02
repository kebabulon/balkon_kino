from dataclasses import asdict
from flask import Blueprint, jsonify, request

from .database import engine as db
from .clients import check_movie_exists
from .schemas import validate_create_review, validate_update_status
from .exceptions import APIError, MovieNotFoundError, ReviewNotFoundError, ServiceUnavailableError, ValidationError

reviews_bp = Blueprint("reviews", __name__)

@reviews_bp.app_errorhandler(APIError)
def handle_api_error(error):
    return jsonify({"errors": [{"code": error.code, "detail": error.detail}]}), error.status_code

@reviews_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@reviews_bp.route("/ugc", methods=["POST"])
def create_review():
    data = request.get_json(silent=True) or {}
    validated = validate_create_review(data)

    if not check_movie_exists(validated["movie_id"]):
        raise MovieNotFoundError()

    item = db.create(**validated)
    return jsonify({"data": _serialize_item(item)}), 201

@reviews_bp.route("/ugc", methods=["GET"])
def list_reviews():
    try:
        movie_id = int(request.args.get("movie_id", 0))
        if movie_id < 1:
            raise ValueError
    except (TypeError, ValueError):
        raise ValidationError({"movie_id": "Ожидается число >= 1"})

    items = db.list_for_movie(movie_id)
    return jsonify(
        {
            "data": [_serialize_item(item) for item in items],
            "meta": {"movie_id": movie_id, "count": len(items)},
        }
    )

@reviews_bp.route("/ugc/<int:item_id>", methods=["PATCH"])
def update_review_status(item_id):
    data = request.get_json(silent=True) or {}
    validated = validate_update_status(data)

    item = db.update_status(item_id, **validated)
    return jsonify({"data": _serialize_item(item)})

def _serialize_item(item):
    payload = asdict(item)
    payload["created_at"] = item.created_at.isoformat()
    payload["updated_at"] = item.updated_at.isoformat()
    return payload
