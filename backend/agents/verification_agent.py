"""
agents/verification_agent.py
-------------------------------
Module 8 — Verification Agent.
For every important extracted field, retrieves supporting evidence via RAG
and asks the LLM to compare the extracted value against that evidence,
assigning a confidence level. This is what stops the system from blindly
trusting the extraction agent's output.

Dependencies: services/rag_service, services/ollama_service, prompts/verification_prompt
"""

from services.rag_service import get_context_for_query, format_context_for_prompt
from services.ollama_service import generate_json
from prompts.verification_prompt import VERIFICATION_SYSTEM_PROMPT, build_verification_user_prompt

IMPORTANT_FIELDS = [
    ("seller", "name"), ("buyer", "name"),
    ("property", "survey_number"), ("property", "extent"), ("property", "boundaries"),
    ("financial_information", "sale_consideration"),
    ("document_information", "registration_number"),
]


def run_verification(document_id: str, structured_data: dict) -> list[dict]:
    results = []
    for section, field in IMPORTANT_FIELDS:
        value = structured_data.get(section, {}).get(field, "Not Found")
        field_label = f"{section}.{field}"

        if value == "Not Found":
            results.append({
                "field_name": field_label, "extracted_value": value,
                "confidence": "Low", "evidence_page": None,
            })
            continue

        context_chunks = get_context_for_query(document_id, str(value), top_k=3)
        context_text = format_context_for_prompt(context_chunks)
        user_prompt = build_verification_user_prompt(field_label, str(value), context_text)

        verdict = generate_json(VERIFICATION_SYSTEM_PROMPT, user_prompt)
        results.append({
            "field_name": field_label,
            "extracted_value": value,
            "confidence": verdict.get("confidence", "Low"),
            "evidence_page": verdict.get("evidence_page"),
        })
    return results
