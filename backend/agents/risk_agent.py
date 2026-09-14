"""
agents/risk_agent.py
-----------------------
Module 9 & 10 — Risk Analysis Agent + Risk Classification.
Never declares legal validity; only flags "Potential Risk Identified",
"Requires Verification" or "Insufficient Evidence", each with a LOW/
MEDIUM/HIGH severity and evidence citation.

Dependencies: services/rag_service, services/ollama_service, prompts/risk_prompt
"""

import json
from services.rag_service import get_context_for_query, format_context_for_prompt
from services.ollama_service import generate_json
from prompts.risk_prompt import RISK_ANALYSIS_SYSTEM_PROMPT, build_risk_analysis_user_prompt

RISK_QUERIES = [
    "survey number property boundaries extent",
    "registration number document number encumbrance",
    "previous deed parent document references",
]


def run_risk_analysis(document_id: str, structured_data: dict) -> list[dict]:
    context_chunks = []
    for query in RISK_QUERIES:
        context_chunks.extend(get_context_for_query(document_id, query, top_k=3))
    context_text = format_context_for_prompt(context_chunks)

    user_prompt = build_risk_analysis_user_prompt(json.dumps(structured_data), context_text)
    result = generate_json(RISK_ANALYSIS_SYSTEM_PROMPT, user_prompt)

    risks = result.get("risks", [])
    valid_levels = {"LOW", "MEDIUM", "HIGH"}
    for risk in risks:
        if risk.get("risk_level") not in valid_levels:
            risk["risk_level"] = "MEDIUM"  # deterministic fallback, never leave it unclassified
    return risks
