"""
agents/report_agent.py
-------------------------
Module 16 — Report Generation Agent.
Thin wrapper around services/report_service so the LangGraph node interface
is consistent with the other agents (agents/*.py = graph-callable units).

Dependencies: services/report_service
"""

from services.report_service import build_report


def run_report_generation(document_id: str) -> dict:
    return build_report(document_id)
