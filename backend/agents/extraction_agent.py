"""
agents/extraction_agent.py
-----------------------------
Module 6 — Information Extraction Agent.
Retrieves relevant chunks via RAG (never the raw PDF) and asks Qwen3 8B
to extract only fields that are explicitly present, returning "Not Found"
otherwise (Rule 2/3 — never invent missing fields).

Dependencies: services/rag_service, services/ollama_service, prompts/extraction_prompt
"""

from services.rag_service import get_context_for_query, format_context_for_prompt
from services.ollama_service import generate_json
from prompts.extraction_prompt import EXTRACTION_SYSTEM_PROMPT, build_extraction_user_prompt

# One broad retrieval query per logical group keeps this simple; you can split
# into per-field retrieval calls later for higher precision.
RETRIEVAL_QUERIES = [
    "seller buyer names and addresses",
    "property description survey number boundaries extent district taluk village",
    "sale consideration payment stamp duty registration fee",
    "registration number document number execution date witnesses",
]


def run_extraction(document_id: str) -> dict:
    context_chunks = []
    for query in RETRIEVAL_QUERIES:
        context_chunks.extend(get_context_for_query(document_id, query, top_k=4))

    context_text = format_context_for_prompt(context_chunks)
    user_prompt = build_extraction_user_prompt(context_text)

    extracted = generate_json(EXTRACTION_SYSTEM_PROMPT, user_prompt)
    return extracted
