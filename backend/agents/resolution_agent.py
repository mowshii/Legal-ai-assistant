"""
agents/resolution_agent.py
-----------------------------
Module 11 — Risk Resolution Agent.
For every risk found by risk_agent, adds a recommended verification step
and a possible resolution path. Kept as a separate agent (not merged into
risk_agent) so each has one clear responsibility, matching the spec.

Dependencies: services/ollama_service, prompts/risk_prompt
"""

from services.ollama_service import generate_json
from prompts.risk_prompt import RISK_RESOLUTION_SYSTEM_PROMPT, build_risk_resolution_user_prompt


def run_risk_resolution(risks: list[dict]) -> list[dict]:
    resolved = []
    for risk in risks:
        user_prompt = build_risk_resolution_user_prompt(
            risk.get("risk_title", ""), risk.get("explanation", "")
        )
        resolution = generate_json(RISK_RESOLUTION_SYSTEM_PROMPT, user_prompt)
        resolved.append({
            **risk,
            "recommended_verification": resolution.get("recommended_verification", ""),
            "possible_resolution": resolution.get("possible_resolution", ""),
        })
    return resolved
