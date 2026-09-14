"""
services/pdf_service.py
------------------------
Reads a PDF, extracts text page-by-page, and flags pages that look
scanned/image-only (little or no extractable text) so ocr_service can
be triggered on just those pages.

Dependencies: PyMuPDF (fitz), pdfplumber
"""

import fitz  # PyMuPDF

MIN_CHARS_TO_SKIP_OCR = 20  # below this, a page is treated as "scanned"


def extract_pages(file_path: str) -> list[dict]:
    """
    Returns a list of:
      {"page_number": int, "text": str, "needs_ocr": bool}
    """
    pages = []
    doc = fitz.open(file_path)
    for i, page in enumerate(doc):
        text = page.get_text("text") or ""
        needs_ocr = len(text.strip()) < MIN_CHARS_TO_SKIP_OCR
        pages.append({
            "page_number": i + 1,
            "text": text,
            "needs_ocr": needs_ocr,
        })
    doc.close()
    return pages


def get_page_count(file_path: str) -> int:
    doc = fitz.open(file_path)
    count = doc.page_count
    doc.close()
    return count


def render_page_to_image(file_path: str, page_number: int, zoom: float = 2.0):
    """Rasterizes a single page (1-indexed) to a PIL-compatible pixmap, for OCR."""
    doc = fitz.open(file_path)
    page = doc[page_number - 1]
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    doc.close()
    return pix
