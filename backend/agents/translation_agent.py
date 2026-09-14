"""
agents/translation_agent.py
------------------------------
Module 12 — Bilingual Translation Agent (English <-> Tamil).
Identifiers, names, and numbers are never sent for translation — only
label/explanation strings are — enforced by a deterministic key allowlist
rather than trusting the LLM alone (defense in depth for Rule 12).

Dependencies: services/ollama_service, prompts/translation_prompt
"""

import json
from services.ollama_service import generate_text
from prompts.translation_prompt import TRANSLATION_SYSTEM_PROMPT, build_translation_user_prompt

# Keys whose VALUES must never be translated/altered, even if nested.
PROTECTED_KEYS = {
    "name", "identification", "survey_number", "sub_division_number", "patta_number",
    "document_number", "registration_number", "sale_consideration", "extracted_value",
    "registration_date", "execution_date",
}


def _extract_translatable(data: dict) -> dict:
    """Returns only the subset of keys that are safe to send for translation."""
    if isinstance(data, dict):
        return {k: _extract_translatable(v) for k, v in data.items() if k not in PROTECTED_KEYS}
    if isinstance(data, list):
        return [_extract_translatable(v) for v in data]
    return data


def _merge_translated(original: dict, translated: dict) -> dict:
    """Merges translated label/explanation strings back over the original,
    leaving protected keys exactly as they were."""
    if isinstance(original, dict):
        merged = dict(original)
        for k, v in original.items():
            if k in PROTECTED_KEYS:
                continue
            if isinstance(translated, dict) and k in translated:
                merged[k] = _merge_translated(v, translated[k])
        return merged
    return translated if translated is not None else original


def translate_payload(data: dict, target_language: str) -> dict:
    if target_language not in ("en", "ta"):
        raise ValueError("target_language must be 'en' or 'ta'")

    translatable_subset = _extract_translatable(data)
    user_prompt = build_translation_user_prompt(json.dumps(translatable_subset), target_language)
    raw_response = generate_text(TRANSLATION_SYSTEM_PROMPT, user_prompt)

    try:
        translated_subset = json.loads(raw_response)
    except json.JSONDecodeError:
        # Fail safe: if translation output is malformed, keep the original language
        # rather than showing broken/garbled text to the user.
        return data

    return _merge_translated(data, translated_subset)
