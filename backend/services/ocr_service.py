"""
services/ocr_service.py
------------------------
Runs Tesseract OCR on pages that pdf_service flagged as scanned/image-based.

Setup required on the host machine (NOT pip-installable):
  Ubuntu/Debian: sudo apt-get install tesseract-ocr
  macOS:         brew install tesseract
  Windows:       install the Tesseract binary and set TESSERACT_CMD in .env

Dependencies: pytesseract, Pillow, PyMuPDF (for rendering, via pdf_service)
"""

import io
import pytesseract
from PIL import Image
from config import config
from services.pdf_service import render_page_to_image

pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD


def ocr_page(file_path: str, page_number: int, lang: str = "eng") -> str:
    """
    OCRs a single page. `lang` uses Tesseract language codes:
      'eng' for English, 'tam' for Tamil (requires the tam.traineddata pack —
      see Future Extension: Tamil OCR in the project spec, Module 29).
    """
    pix = render_page_to_image(file_path, page_number)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    text = pytesseract.image_to_string(img, lang=lang)
    return text
