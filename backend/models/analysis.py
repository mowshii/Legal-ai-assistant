"""
models/analysis.py
-------------------
Tables for extracted structured information, verification results,
generated reports, and per-agent execution logs (for Module 18 monitoring).

Dependencies: SQLAlchemy
"""

import uuid
from datetime import datetime, timezone
from extensions import db


class ExtractedInformation(db.Model):
    __tablename__ = "extracted_information"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey("documents.id"), nullable=False)
    # Full structured JSON per MODULE 7 schema (document_information, seller, buyer,
    # property, financial_information, registration, witnesses, references)
    data = db.Column(db.JSON, nullable=False, default=dict)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class VerificationResult(db.Model):
    __tablename__ = "verification_results"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey("documents.id"), nullable=False)
    field_name = db.Column(db.String(120), nullable=False)
    extracted_value = db.Column(db.Text, nullable=True)
    confidence = db.Column(db.String(10), nullable=False)  # High | Medium | Low
    evidence_page = db.Column(db.Integer, nullable=True)
    evidence_snippet = db.Column(db.Text, nullable=True)


class RiskAnalysis(db.Model):
    __tablename__ = "risk_analysis"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey("documents.id"), nullable=False)
    risk_title = db.Column(db.String(200), nullable=False)
    risk_level = db.Column(db.String(10), nullable=False)  # LOW | MEDIUM | HIGH
    explanation = db.Column(db.Text, nullable=False)
    evidence = db.Column(db.Text, nullable=True)
    recommended_action = db.Column(db.Text, nullable=True)
    possible_resolution = db.Column(db.Text, nullable=True)


class AnalysisReport(db.Model):
    __tablename__ = "analysis_reports"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey("documents.id"), nullable=False)
    overall_risk = db.Column(db.String(10), nullable=True)  # LOW | MEDIUM | HIGH
    high_count = db.Column(db.Integer, default=0)
    medium_count = db.Column(db.Integer, default=0)
    low_count = db.Column(db.Integer, default=0)
    report_json = db.Column(db.JSON, nullable=False, default=dict)
    pdf_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class AgentRun(db.Model):
    """Module 18 — Agent Monitoring: one row per agent execution per document."""
    __tablename__ = "agent_runs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = db.Column(db.String(36), db.ForeignKey("documents.id"), nullable=False)
    agent_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="pending")
    # pending | running | success | warning | failed
    message = db.Column(db.Text, nullable=True)
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    finished_at = db.Column(db.DateTime, nullable=True)


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), nullable=True)
    action = db.Column(db.String(120), nullable=False)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
