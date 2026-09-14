"""
services/embedding_service.py
-------------------------------
Generates embeddings locally (no external API calls — everything runs on
your machine, consistent with the "local LLM via Ollama" requirement) using
sentence-transformers, and stores/retrieves them via pgvector.

Model: all-MiniLM-L6-v2 (384-dim, small & fast, good enough for RAG on
short legal-deed chunks). Swap EMBEDDING_MODEL_NAME if you want higher
quality at the cost of speed.

First run will download the model (~90MB) from HuggingFace — after that
it's fully offline.

Dependencies: sentence-transformers, pgvector, SQLAlchemy
"""

from sentence_transformers import SentenceTransformer
from extensions import db
from models.document import DocumentChunk

EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

_model = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _model


def embed_text(text: str) -> list[float]:
    model = _get_model()
    vector = model.encode(text, normalize_embeddings=True)
    return vector.tolist()


def store_chunks(document_id: str, chunks: list[dict]) -> None:
    """chunks: [{"page_number", "section", "text"}, ...] -> writes DocumentChunk rows with embeddings."""
    for chunk in chunks:
        embedding = embed_text(chunk["text"])
        row = DocumentChunk(
            document_id=document_id,
            page_number=chunk["page_number"],
            section=chunk["section"],
            text=chunk["text"],
            embedding=embedding,
        )
        db.session.add(row)
    db.session.commit()


def retrieve_relevant_chunks(document_id: str, query: str, top_k: int = 5) -> list[DocumentChunk]:
    """
    Retrieves the top_k most similar chunks for this document using pgvector's
    cosine-distance operator (`<=>`), scoped to a single document so RAG never
    leaks context between different Sales Deeds.
    """
    query_embedding = embed_text(query)
    results = (
        db.session.query(DocumentChunk)
        .filter(DocumentChunk.document_id == document_id)
        .order_by(DocumentChunk.embedding.cosine_distance(query_embedding))
        .limit(top_k)
        .all()
    )
    return results
