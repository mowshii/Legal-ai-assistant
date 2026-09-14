"""
agents/structuring_agent.py
------------------------------
Module 7 — Data Structuring Agent.
Pure deterministic normalization: guarantees every key in the Module 7
schema exists (filling any gaps left by the LLM with "Not Found") so the
frontend can always build its table without null-checking every field.

Dependencies: none (stdlib only) — intentionally deterministic, not LLM-based,
per Module 15 ("use deterministic validation wherever possible").
"""

SCHEMA = {
    "document_information": ["document_type", "document_number", "registration_number",
                              "registration_date", "execution_date"],
    "seller": ["name", "address", "identification"],
    "buyer": ["name", "address", "identification"],
    "property": ["address", "district", "taluk", "village", "survey_number",
                 "sub_division_number", "patta_number", "property_type", "extent",
                 "boundaries", "building_details"],
    "financial_information": ["sale_consideration", "payment_details", "stamp_duty", "registration_fee"],
}


def structure_data(raw_extracted: dict) -> dict:
    structured = {}
    for section, fields in SCHEMA.items():
        section_data = raw_extracted.get(section, {}) or {}
        structured[section] = {
            field: section_data.get(field) or "Not Found" for field in fields
        }
    structured["witnesses"] = raw_extracted.get("witnesses") or []
    structured["references"] = raw_extracted.get("references") or []
    return structured
