"""
models/__init__.py
-------------------
Import every model here so `db.create_all()` in app.py can see them all,
and so other modules can do `from models import User, Document, ...`.
"""

from models.user import User
from models.document import Document, DocumentPage, DocumentChunk
from models.analysis import (
    ExtractedInformation,
    VerificationResult,
    RiskAnalysis,
    AnalysisReport,
    AgentRun,
    AuditLog,
)
