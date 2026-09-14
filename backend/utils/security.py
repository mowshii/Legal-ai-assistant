"""
utils/security.py
------------------
Filename sanitization + unique storage naming so we never trust user input
for filesystem paths (Module 24 — Security).

Dependencies: Werkzeug
"""

import uuid
from werkzeug.utils import secure_filename


def make_secure_stored_filename(original_filename: str) -> str:
    """
    Returns a random, collision-free filename for disk storage.
    The original filename is kept only in the database for display purposes —
    never used to build a filesystem path (prevents path traversal).
    """
    safe_original = secure_filename(original_filename)
    ext = safe_original.rsplit(".", 1)[-1].lower() if "." in safe_original else "pdf"
    return f"{uuid.uuid4().hex}.{ext}"


def new_document_id() -> str:
    return str(uuid.uuid4())
