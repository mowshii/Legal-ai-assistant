"""
utils/logger.py
----------------
Central logger + a helper to record per-agent execution rows into the
AgentRun table (Module 18 — Agent Monitoring, Rule 13 — log every agent run).

Dependencies: SQLAlchemy (via extensions.db)
"""

import logging
from datetime import datetime, timezone
from extensions import db
from models.analysis import AgentRun

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def start_agent_run(document_id: str, agent_name: str) -> AgentRun:
    run = AgentRun(document_id=document_id, agent_name=agent_name, status="running")
    db.session.add(run)
    db.session.commit()
    return run


def finish_agent_run(run: AgentRun, status: str, message: str = "") -> None:
    """status: 'success' | 'warning' | 'failed'"""
    run.status = status
    run.message = message
    run.finished_at = datetime.now(timezone.utc)
    db.session.commit()
