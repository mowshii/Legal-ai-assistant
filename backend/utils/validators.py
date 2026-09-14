
"""
utils/validators.py
--------------------
Implements the upload validation rules from Module 4:

  1. Only PDF files
  2. Max 10 MB
  3. Reject empty files
  4. Reject files that do not have a valid PDF signature
  5. Reject corrupted PDFs (must actually open with PyMuPDF)

Dependencies:
    PyMuPDF (fitz)
"""

import fitz  # PyMuPDF
from config import config


class ValidationError(Exception):
    """Raised with a user-facing message when upload validation fails."""


def validate_extension(filename: str) -> None:
    """Check that the uploaded filename has an allowed extension."""

    if "." not in filename:
        raise ValidationError("Only PDF files are supported.")

    ext = filename.rsplit(".", 1)[1].lower()

    if ext not in config.ALLOWED_EXTENSIONS:
        raise ValidationError("Only PDF files are supported.")


def validate_mime_type(file_bytes: bytes) -> None:
    """
    Validate that the file starts with the standard PDF signature.

    A PDF file normally begins with:
        %PDF-

    This replaces python-magic/libmagic because the project only accepts
    PDF documents and does not require native libmagic on Windows.
    """

    if not file_bytes.startswith(b"%PDF-"):
        raise ValidationError("Only PDF files are supported.")


def validate_size(file_bytes: bytes) -> None:
    """Reject empty files and files larger than the configured limit."""

    if len(file_bytes) == 0:
        raise ValidationError("The uploaded file is empty.")

    if len(file_bytes) > config.MAX_CONTENT_LENGTH:
        raise ValidationError("Maximum file size is 10 MB.")


def validate_pdf_readable(file_bytes: bytes) -> int:
    """
    Open the PDF using PyMuPDF to verify that it is not corrupted.

    Returns:
        int: Number of pages in the PDF.
    """

    doc = None

    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")

        page_count = doc.page_count

        if page_count == 0:
            raise ValidationError(
                "The uploaded PDF could not be processed."
            )

        return page_count

    except ValidationError:
        raise

    except Exception as exc:
        raise ValidationError(
            "The uploaded PDF could not be processed."
        ) from exc

    finally:
        if doc is not None:
            doc.close()


def validate_upload(filename: str, file_bytes: bytes) -> int:
    """
    Run all upload validations in order.

    Returns:
        int: Page count when validation succeeds.
    """

    validate_extension(filename)
    validate_size(file_bytes)
    validate_mime_type(file_bytes)

    return validate_pdf_readable(file_bytes)
