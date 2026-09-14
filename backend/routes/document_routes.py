"""
routes/document_routes.py
----------------------------
Module 2 — PDF Upload and Validation.
POST /api/documents/upload, GET /api/documents, GET /api/documents/{id}, DELETE /api/documents/{id}

Never exposes the internal storage path to the frontend (Module 24).

Dependencies: Flask, Flask-JWT-Extended, utils/validators, utils/security
"""

import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models.user import User
from models.document import Document
from utils.validators import validate_upload, ValidationError
from utils.security import make_secure_stored_filename, new_document_id
from utils.logger import get_logger

document_bp = Blueprint("documents", __name__, url_prefix="/api/documents")
logger = get_logger("routes.documents")


@document_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_document():
    user_id = get_jwt_identity()

    if "file" not in request.files:
        return jsonify({"error": "No file was uploaded."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file was uploaded."}), 400

    file_bytes = file.read()

    try:
        page_count = validate_upload(file.filename, file_bytes)
    except ValidationError as exc:
        return jsonify({"error": str(exc)}), 400

    stored_filename = make_secure_stored_filename(file.filename)
    stored_path = os.path.join(current_app.config["UPLOAD_FOLDER"], stored_filename)
    with open(stored_path, "wb") as f:
        f.write(file_bytes)

    document = Document(
        id=new_document_id(),
        user_id=user_id,
        original_filename=file.filename,
        stored_filename=stored_filename,
        file_size_bytes=len(file_bytes),
        page_count=page_count,
        status="uploaded",
    )
    db.session.add(document)
    db.session.commit()

    return jsonify(document.to_dict()), 201


@document_bp.route("", methods=["GET"])
@jwt_required()
def list_documents():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    query = Document.query if user and user.role == "admin" else Document.query.filter_by(user_id=user_id)
    documents = query.order_by(Document.created_at.desc()).all()
    return jsonify([d.to_dict() for d in documents]), 200


@document_bp.route("/<document_id>", methods=["GET"])
@jwt_required()
def get_document(document_id):
    document = _get_owned_document_or_none(document_id)
    if not document:
        return jsonify({"error": "Document not found."}), 404
    return jsonify(document.to_dict()), 200


@document_bp.route("/<document_id>", methods=["DELETE"])
@jwt_required()
def delete_document(document_id):
    document = _get_owned_document_or_none(document_id)
    if not document:
        return jsonify({"error": "Document not found."}), 404

    stored_path = os.path.join(current_app.config["UPLOAD_FOLDER"], document.stored_filename)
    if os.path.exists(stored_path):
        os.remove(stored_path)

    db.session.delete(document)
    db.session.commit()
    return jsonify({"message": "Document deleted."}), 200


def _get_owned_document_or_none(document_id: str):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    document = Document.query.get(document_id)
    if not document:
        return None
    if user and user.role == "admin":
        return document
    return document if document.user_id == user_id else None
