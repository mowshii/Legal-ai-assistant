"""
agents/document_agent.py
--------------------------
Module 3 — Document Processing Agent.
Reads the PDF, extracts text per page, triggers OCR only on pages that need
it, and returns a clean {document_id, pages, text, ocr_used} payload.
Deliberately does NOT interpret the document — preprocessing only.

Dependencies: services/pdf_service, services/ocr_service, services/chunking_service
"""

from services import pdf_service, ocr_service
from services.chunking_service import clean_text


def run_document_processing(document_id: str, file_path: str) -> dict:
    pages_raw = pdf_service.extract_pages(file_path)
    ocr_used = False
    processed_pages = []

    for page in pages_raw:
        text = page["text"]
        if page["needs_ocr"]:
            text = ocr_service.ocr_page(file_path, page["page_number"])
            ocr_used = True
        processed_pages.append({
            "page_number": page["page_number"],
            "text": clean_text(text),
            "was_ocr": page["needs_ocr"],
        })

    full_text = "\n\n".join(p["text"] for p in processed_pages)

    return {
        "document_id": document_id,
        "pages": len(processed_pages),
        "text": full_text,
        "ocr_used": ocr_used,
        "page_details": processed_pages,
    }
