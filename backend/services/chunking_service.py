"""
services/chunking_service.py
------------------------------
Module 4 — Text Cleaning and Chunking.

clean_text(): strips repeated headers/footers, collapses whitespace,
              fixes broken line-wraps and common OCR artifacts.

chunk_document(): splits cleaned text into document-aware sections
              (Parties, Property Description, Consideration, Boundaries,
              Survey Information, Registration, Encumbrance, Witnesses,
              Clauses) using heading-keyword matching, rather than a
              blind fixed-length split.

Dependencies: re (stdlib) only
"""

import re

SECTION_KEYWORDS = {
    "Parties": [r"between", r"seller", r"vendor", r"purchaser", r"buyer"],
    "Property Description": [r"property described", r"schedule of property", r"description of property"],
    "Consideration": [r"sale consideration", r"consideration of rs", r"total consideration"],
    "Boundaries": [r"boundaries", r"bounded on", r"bounded by"],
    "Survey Information": [r"survey no", r"survey number", r"sub[- ]?division"],
    "Registration": [r"registered as document", r"registration no", r"book no", r"sro"],
    "Encumbrance": [r"encumbrance", r"mortgage", r"charge on the property"],
    "Witnesses": [r"witness", r"witnesses"],
    "Clauses": [r"whereas", r"now this deed witnesseth", r"covenant"],
}


def clean_text(raw_text: str) -> str:
    text = raw_text

    # Collapse excessive whitespace/newlines
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Fix hyphenated line-wrap artifacts: "regis-\ntration" -> "registration"
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)

    # Drop common repeated OCR/footer noise (page numbers, "Page X of Y")
    text = re.sub(r"\bPage\s+\d+\s+of\s+\d+\b", "", text, flags=re.IGNORECASE)

    return text.strip()


def _detect_section(paragraph: str) -> str:
    lower = paragraph.lower()
    for section, patterns in SECTION_KEYWORDS.items():
        for pattern in patterns:
            if re.search(pattern, lower):
                return section
    return "General"


def chunk_document(pages: list[dict]) -> list[dict]:
    """
    pages: [{"page_number": int, "text": str}, ...]  (already cleaned)
    Returns: [{"page_number", "section", "text"}, ...]
    """
    chunks = []
    for page in pages:
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", page["text"]) if p.strip()]
        for paragraph in paragraphs:
            if len(paragraph) < 15:
                continue  # skip near-empty fragments
            section = _detect_section(paragraph)
            chunks.append({
                "page_number": page["page_number"],
                "section": section,
                "text": paragraph,
            })
    return chunks
