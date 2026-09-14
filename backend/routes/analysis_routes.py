"""
routes/analysis_routes.py
----------------------------
POST /api/documents/{id}/analyze, GET /api/documents/{id}/analysis,
GET /api/documents/{id}/risks, GET /api/documents/{id}/evidence,
GET /api/documents/{id}/translation

Triggers the LangGraph workflow (graph/workflow.py) and reads back the
results that each node already persisted to Postgres.

Dependencies: Flask, Flask-JWT-Extended, graph/workflow, models
"""

import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from models.document import Document
from models.analysis import ExtractedInformation, VerificationResult, RiskAnalysis
from graph.workflow import run_full_analysis
from agents.translation_agent import translate_payload
from utils.logger import get_logger

analysis_bp = Blueprint("analysis", __name__, url_prefix="/api/documents")
logger = get_logger("routes.analysis")


@analysis_bp.route("/<document_id>/analyze", methods=["POST"])
@jwt_required()
def analyze_document(document_id):
    document = Document.query.get(document_id)
    if not document:
        return jsonify({"error": "Document not found."}), 404

    language = (request.get_json(silent=True) or {}).get("language", "en")
    file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], document.stored_filename)

    try:
        final_state = run_full_analysis(document_id, file_path, language)
    except Exception as exc:  # noqa: BLE001
        logger.exception("Analysis pipeline crashed for %s", document_id)
        document.status = "failed"
        from extensions import db
        db.session.commit()
        return jsonify({"error": "Analysis failed.", "details": str(exc)}), 500

    return jsonify({
        "document_id": document_id,
        "status": document.status,
        "errors": final_state.get("errors", []),
        "final_report": final_state.get("final_report", {}),
    }), 200


@analysis_bp.route("/<document_id>/analysis", methods=["GET"])
@jwt_required()
def get_analysis(document_id):
    extracted = ExtractedInformation.query.filter_by(document_id=document_id).first()
    if not extracted:
        return jsonify({"error": "No analysis found for this document yet."}), 404
    return jsonify(extracted.data), 200


@analysis_bp.route("/<document_id>/risks", methods=["GET"])
@jwt_required()
def get_risks(document_id):
    risks = RiskAnalysis.query.filter_by(document_id=document_id).all()
    return jsonify([{
        "risk": r.risk_title, "risk_level": r.risk_level, "explanation": r.explanation,
        "evidence": r.evidence, "recommended_action": r.recommended_action,
        "possible_resolution": r.possible_resolution,
    } for r in risks]), 200


@analysis_bp.route("/<document_id>/evidence", methods=["GET"])
@jwt_required()
def get_evidence(document_id):
    results = VerificationResult.query.filter_by(document_id=document_id).all()
    return jsonify([{
        "field": v.field_name, "extracted_value": v.extracted_value,
        "confidence": v.confidence, "evidence_page": v.evidence_page,
    } for v in results]), 200


@analysis_bp.route("/<document_id>/translation", methods=["GET"])
@jwt_required()
def get_translation(document_id):
    target_language = request.args.get("language", "ta")
    extracted = ExtractedInformation.query.filter_by(document_id=document_id).first()
    if not extracted:
        return jsonify({"error": "No analysis found for this document yet."}), 404

    translated = translate_payload(extracted.data, target_language)
    return jsonify(translated), 200
