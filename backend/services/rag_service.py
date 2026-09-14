"""
services/rag_service.py
-------------------------
Glue between embedding_service (retrieval) and the agents (generation).
Ensures every agent gets *retrieved evidence*, never the raw whole PDF —
per Project Rule 9 ("Use RAG before asking Qwen3 8B to interpret
document-specific information") and Module 2 ("Do not send the entire
PDF directly to the LLM").

Dependencies: services/embedding_service
"""

from services.embedding_service import retrieve_relevant_chunks


def get_context_for_query(document_id: str, query: str, top_k: int = 5) -> list[dict]:
    chunks = retrieve_relevant_chunks(document_id, query, top_k=top_k)
    return [
        {
            "page_number": c.page_number,
            "section": c.section,
            "text": c.text,
        }
        for c in chunks
    ]


def format_context_for_prompt(context_chunks: list[dict]) -> str:
    """Turns retrieved chunks into a numbered, page-cited block for the LLM prompt."""
    lines = []
    for i, chunk in enumerate(context_chunks, start=1):
        lines.append(f"[{i}] (Page {chunk['page_number']}, Section: {chunk['section']})\n{chunk['text']}")
    return "\n\n".join(lines)
