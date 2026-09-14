"""
graph/workflow.py
--------------------
Module 13 — LangGraph Agent Orchestration.
Builds the single StateGraph that runs the whole pipeline:

  START -> Document Processing -> Chunking/Indexing -> Extraction
        -> Structuring -> Verification -> Risk Analysis
        -> (conditional) Risk Resolution -> Translation
        -> Report Generation -> Final Validation -> END

The OCR decision (Module 13's "Is OCR required?" branch) is handled per-page
inside document_agent.run_document_processing rather than as a graph-level
branch, since OCR need can differ page-by-page within the same document.
The "Are risks detected?" branch below IS graph-level, since it applies
to the whole document.

Dependencies: langgraph
"""

from langgraph.graph import StateGraph, END
from graph.state import DeedAnalysisState
from graph.nodes import (
    document_processing_node,
    chunking_and_indexing_node,
    extraction_node,
    structuring_node,
    verification_node,
    risk_analysis_node,
    risk_resolution_node,
    translation_node,
    report_generation_node,
    final_validation_node,
)


def risks_detected(state: dict) -> str:
    return "resolve" if state.get("risks") else "skip"


def build_workflow():
    graph = StateGraph(DeedAnalysisState)

    graph.add_node("document_processing", document_processing_node)
    graph.add_node("chunking_indexing", chunking_and_indexing_node)
    graph.add_node("extraction", extraction_node)
    graph.add_node("structuring", structuring_node)
    graph.add_node("verification", verification_node)
    graph.add_node("risk_analysis", risk_analysis_node)
    graph.add_node("risk_resolution", risk_resolution_node)
    graph.add_node("translation", translation_node)
    graph.add_node("report_generation", report_generation_node)
    graph.add_node("final_validation", final_validation_node)

    graph.set_entry_point("document_processing")
    graph.add_edge("document_processing", "chunking_indexing")
    graph.add_edge("chunking_indexing", "extraction")
    graph.add_edge("extraction", "structuring")
    graph.add_edge("structuring", "verification")
    graph.add_edge("verification", "risk_analysis")

    graph.add_conditional_edges(
        "risk_analysis", risks_detected,
        {"resolve": "risk_resolution", "skip": "translation"},
    )
    graph.add_edge("risk_resolution", "translation")
    graph.add_edge("translation", "report_generation")
    graph.add_edge("report_generation", "final_validation")
    graph.add_edge("final_validation", END)

    return graph.compile()


# Compiled once at import time and reused across requests.
workflow = build_workflow()


def run_full_analysis(document_id: str, file_path: str, language: str = "en") -> dict:
    initial_state: DeedAnalysisState = {
        "document_id": document_id,
        "file_path": file_path,
        "language": language,
        "errors": [],
    }
    final_state = workflow.invoke(initial_state)
    return final_state
