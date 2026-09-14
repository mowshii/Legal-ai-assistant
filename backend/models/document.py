"""
models/document.py
-------------------
Document + DocumentPage + DocumentChunk models.
A Document is one uploaded Sales Deed PDF.
DocumentChunk stores the semantic chunks + their pgvector embedding.

Dependencies: SQLAlchemy, pgvector
"""

import uuid
from datetime import datetime, timezone
from extensions import db
from pgvector.sqlalchemy import Vector

EMBEDDING_DIM = 384  # matches sentence-transformers/all-MiniLM-L6-v2


class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)  # random/secure name on disk
    file_size_bytes = db.Column(db.Integer, nullable=False)
    page_count = db.Column(db.Integer, nullable=True)
    ocr_used = db.Column(db.Boolean, default=False)

    status = db.Column(db.String(30), default="uploaded")
    # uploaded -> processing -> extracted -> verified -> analyzed -> completed -> failed

    language = db.Column(db.String(5), default="en")  # 'en' | 'ta'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    pages = db.relationship("DocumentPage", backref="document", lazy=True, cascade="all, delete-orphan")
    chunks = db.relationship("DocumentChunk", backref="document", lazy=True, cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "document_id": self.id,
            "original_filename": self.original_filename,
            "file_size_bytes": self.file_size_bytes,
            "page_count": self.page_count,
            "ocr_used": self.ocr_used,
            "status": self.status,
            "language": self.language,
            "created_at": self.created_at.isoformat(),
        }


class DocumentPage(db.Model):
    __tablename__ = "document_pages"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey("documents.id"), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    raw_text = db.Column(db.Text, nullable=True)
    was_ocr = db.Column(db.Boolean, default=False)


class DocumentChunk(db.Model):
    __tablename__ = "document_chunks"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey("documents.id"), nullable=False)
    chunk_id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()))
    page_number = db.Column(db.Integer, nullable=True)
    section = db.Column(db.String(80), nullable=True)
    # e.g. Parties, Property Description, Consideration, Boundaries, Registration...
    text = db.Column(db.Text, nullable=False)

    # pgvector column — requires `CREATE EXTENSION vector;` in Postgres
    embedding = db.Column(Vector(EMBEDDING_DIM), nullable=True)
