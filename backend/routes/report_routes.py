"""
routes/report_routes.py
--------------------------
GET /api/documents/{id}/report — returns the final structured report
(Module 16). A PDF-export version can be added later using the pdf skill /
fpdf2 without changing this endpoint's contract.

Dependencies: Flask, Flask-JWT-Extended, services/report_service
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from services.report_service import build_report
from models.document import Document

report_bp = Blueprint("report", __name__, url_prefix="/api/documents")


@report_bp.route("/<document_id>/report", methods=["GET"])
@jwt_required()
def get_report(document_id):
    document = Document.query.get(document_id)
    if not document:
        return jsonify({"error": "Document not found."}), 404
    return jsonify(build_report(document_id)), 200
