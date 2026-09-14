"""
services/ollama_service.py
----------------------------
Thin wrapper around the local Ollama server running Qwen3 8B.

Prerequisite (run once on your machine, NOT in this repo):
  1. Install Ollama:      https://ollama.com/download
  2. Pull the model:      ollama pull qwen3:8b
  3. Confirm it runs:     ollama run qwen3:8b "hello"

Every agent (extraction, verification, risk, resolution, translation,
report) calls `generate_json()` so the LLM's output is always structured
JSON, per Project Rule 10.

Dependencies: ollama (python package)
"""

import json
import ollama
from config import config

_client = ollama.Client(host=config.OLLAMA_HOST)


class LLMOutputError(Exception):
    """Raised when the model does not return valid, parseable JSON."""


def generate_json(system_prompt: str, user_prompt: str, temperature: float = 0.1) -> dict:
    """
    Calls Qwen3 8B with a system + user prompt and enforces JSON-only output.
    Rule 11 says validate LLM output before it reaches the frontend — the
    caller (each agent) is responsible for schema-validating the returned dict.
    """
    response = _client.chat(
        model=config.OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        format="json",
        options={"temperature": temperature},
    )
    raw = response["message"]["content"]
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LLMOutputError(f"Model did not return valid JSON: {raw[:300]}") from exc


def generate_text(system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
    """Plain-text generation, used by the Translation Agent."""
    response = _client.chat(
        model=config.OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": temperature},
    )
    return response["message"]["content"]
