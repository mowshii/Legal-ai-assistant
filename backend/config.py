"""
config.py
---------
Central configuration for the Flask app. Reads everything from environment
variables (via .env) so no secrets or machine-specific paths are hard-coded.

Dependencies: python-dotenv
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # ---- Flask ----
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

    # ---- JWT ----
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    # ---- Database ----
    # Example: postgresql://saledeed_user:password@localhost:5432/saledeed_db
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://saledeed_user:password@localhost:5432/saledeed_db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---- Uploads ----
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB, per project spec
    ALLOWED_EXTENSIONS = {"pdf"}
    ALLOWED_MIME_TYPES = {"application/pdf"}

    # ---- Ollama / LLM ----
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:8b")

    # ---- OCR ----
    TESSERACT_CMD = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")

    # ---- CORS ----
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")


config = Config()
