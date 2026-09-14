"""
graph/nodes.py
-----------------
Wraps each agent as a LangGraph node: (state) -> partial state update.
Every node logs a start/finish AgentRun row (Module 18 monitoring, Rule 13)
and appends to state["errors"] instead of crashing the whole graph on
failure (Rule 14 — recover from an agent failure) where it's safe to
continue with degraded results.

Dependencies: extensions.db, models, agents/*, services/*, utils/logger
"""

from extensions import db
from utils.logger import start_agent_run, finish_agent_run, get_logger
from models.document import Document, DocumentChunk
from models.analysis import ExtractedInformation, VerificationResult, RiskAnalysis, AnalysisReport

from agents.document_agent import run_document_processing
from agents.extraction_agent import run_extraction
from agents.structuring_agent import structure_data
from agents.verification_agent import run_verification
from agents.risk_agent import run_risk_analysis
from agents.resolution_agent import run_risk_resolution
from agents.translation_agent import translate_payload
from agents.report_agent import run_report_generation
from services.chunking_service import chunk_document
from services.embedding_service import store_chunks
from services.report_service import compute_overall_risk

logger = get_logger("graph.nodes")


def _wrap(document_id: str, agent_name: str, fn, *args, **kwargs):
    run = start_agent_run(document_id, agent_name)
    try:
        result = fn(*args, **kwargs)
        finish_agent_run(run, "success")
        return result, None
    except Exception as exc:  # noqa: BLE001 — intentionally broad: log & degrade, don't crash the graph
        logger.exception("%s failed for document %s", agent_name, document_id)
        finish_agent_run(run, "failed", str(exc))
        return None, str(exc)


def document_processing_node(state: dict) -> dict:
    result, err = _wrap(state["document_id"], "Document Processing", run_document_processing,
                         state["document_id"], state["file_path"])
    if err:
        state.setdefault("errors", []).append(f"document_processing: {err}")
        return state
    state["raw_text"] = result["text"]
    state["page_count"] = result["pages"]
    state["ocr_used"] = result["ocr_used"]
    state["page_details"] = result["page_details"]

    doc = Document.query.get(state["document_id"])
    if doc:
        doc.page_count = result["pages"]
        doc.ocr_used = result["ocr_used"]
        doc.status = "extracted"
        db.session.commit()
    return state


def chunking_and_indexing_node(state: dict) -> dict:
    result, err = _wrap(state["document_id"], "Chunking & Indexing",
                         lambda: chunk_document(state["page_details"]))
    if err:
        state.setdefault("errors", []).append(f"chunking: {err}")
        return state
    state["chunks"] = result

    _, index_err = _wrap(state["document_id"], "Embedding Indexing",
                          store_chunks, state["document_id"], result)
    if index_err:
        state.setdefault("errors", []).append(f"embedding: {index_err}")
    return state


def extraction_node(state: dict) -> dict:
    result, err = _wrap(state["document_id"], "Information Extraction", run_extraction, state["document_id"])
    if err:
        state.setdefault("errors", []).append(f"extraction: {err}")
        state["extracted_data"] = {}
        return state
    state["extracted_data"] = result
    return state


def structuring_node(state: dict) -> dict:
    structured = structure_data(state.get("extracted_data", {}))
    state["extracted_data"] = structured

    db.session.add(ExtractedInformation(document_id=state["document_id"], data=structured))
    db.session.commit()
    return state


def verification_node(state: dict) -> dict:
    result, err = _wrap(state["document_id"], "Verification", run_verification,
                         state["document_id"], state["extracted_data"])
    if err:
        state.setdefault("errors", []).append(f"verification: {err}")
        state["verification_results"] = []
        return state
    state["verification_results"] = result

    for v in result:
        db.session.add(VerificationResult(
            document_id=state["document_id"], field_name=v["field_name"],
            extracted_value=v["extracted_value"], confidence=v["confidence"],
            evidence_page=v.get("evidence_page"),
        ))
    db.session.commit()
    return state


def risk_analysis_node(state: dict) -> dict:
    result, err = _wrap(state["document_id"], "Risk Analysis", run_risk_analysis,
                         state["document_id"], state["extracted_data"])
    state["risks"] = result or []
    if err:
        state.setdefault("errors", []).append(f"risk_analysis: {err}")
    return state


def risk_resolution_node(state: dict) -> dict:
    if not state.get("risks"):
        return state
    result, err = _wrap(state["document_id"], "Risk Resolution", run_risk_resolution, state["risks"])
    if err:
        state.setdefault("errors", []).append(f"risk_resolution: {err}")
        return state
    state["risks"] = result

    for r in result:
        db.session.add(RiskAnalysis(
            document_id=state["document_id"], risk_title=r.get("risk_title", ""),
            risk_level=r.get("risk_level", "MEDIUM"), explanation=r.get("explanation", ""),
            evidence=r.get("evidence", ""),
            recommended_action=r.get("recommended_verification", ""),
            possible_resolution=r.get("possible_resolution", ""),
        ))
    db.session.commit()
    return state


def translation_node(state: dict) -> dict:
    if state.get("language", "en") != "ta":
        return state
    result, err = _wrap(state["document_id"], "Translation", translate_payload,
                         state.get("extracted_data", {}), "ta")
    if err:
        state.setdefault("errors", []).append(f"translation: {err}")
        return state
    state["translated"] = result
    return state


def report_generation_node(state: dict) -> dict:
    result, err = _wrap(state["document_id"], "Report Generation", run_report_generation, state["document_id"])
    if err:
        state.setdefault("errors", []).append(f"report: {err}")
        return state
    state["final_report"] = result

    overall, counts = compute_overall_risk_from_dicts(state.get("risks", []))
    db.session.add(AnalysisReport(
        document_id=state["document_id"], overall_risk=overall,
        high_count=counts["HIGH"], medium_count=counts["MEDIUM"], low_count=counts["LOW"],
        report_json=result,
    ))

    doc = Document.query.get(state["document_id"])
    if doc:
        doc.status = "completed"
    db.session.commit()
    return state


def compute_overall_risk_from_dicts(risks: list[dict]):
    counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0}
    for r in risks:
        level = r.get("risk_level", "MEDIUM")
        counts[level] = counts.get(level, 0) + 1
    overall = "HIGH" if counts["HIGH"] else "MEDIUM" if counts["MEDIUM"] else "LOW"
    return overall, counts


def final_validation_node(state: dict) -> dict:
    """Module 15 — deterministic pass/fail check before returning to the frontend."""
    required = ["extracted_data", "verification_results", "risks", "final_report"]
    missing = [k for k in required if not state.get(k) and k != "risks"]  # risks may legitimately be empty
    if missing:
        state.setdefault("errors", []).append(f"final_validation: missing {missing}")
    return state
