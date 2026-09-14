"""
graph/state.py
-----------------
Module 14 — Agent State.
The single shared state object that every LangGraph node reads from and
writes to. No agent re-processes the PDF independently — everything they
need is already in this dict by the time they run.

Dependencies: typing (stdlib), langgraph
"""

from typing import TypedDict, Any


class DeedAnalysisState(TypedDict, total=False):
    document_id: str
    file_path: str
    language: str

    # populated by document_agent
    raw_text: str
    page_count: int
    ocr_used: bool
    page_details: list[dict]

    # populated by chunking step
    chunks: list[dict]

    # populated by extraction_agent + structuring_agent
    extracted_data: dict

    # populated by verification_agent
    verification_results: list[dict]

    # populated by risk_agent + resolution_agent
    risks: list[dict]

    # populated by translation_agent (only if language == 'ta')
    translated: dict

    # populated by report_agent
    final_report: dict

    errors: list[str]
