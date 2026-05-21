"""
AI Advisory Layer — Phase G-A
Scope: generate contextual questions only.
AI may NOT return: maturity, status, gate decision, score, gap closure.
All AI logic lives here. Engine calls this; never the reverse.
"""

import json
import urllib.request

AI_ADVISORY_ENABLED = False  # Default: off. Enable explicitly for testing only.


def get_ai_question(domain: str, gap_type: str, context: dict) -> str | None:
    """
    Returns one AI-generated question string, or None (triggers fallback).
    
    context keys available (from progression_loop.py — no new state methods):
        - idea_summary: str | None
        - gap_type: str
        - domain: str
        - last_response: str | None
        - iteration: int

    Never returns: maturity, status, gate decision, score, gap closure.
    Returns None on any failure — fallback chain handles the rest.
    """
    if not AI_ADVISORY_ENABLED:
        return None

    try:
        idea_summary = context.get("idea_summary") or "unknown idea"
        last_response = context.get("last_response") or "no previous response"
        iteration = context.get("iteration", 1)

        prompt = (
            f"You are helping an inventor clarify their idea.\n"
            f"Domain: {domain}\n"
            f"Current gap to address: {gap_type}\n"
            f"Idea so far: {idea_summary}\n"
            f"Last inventor response: {last_response}\n"
            f"Iteration: {iteration}\n\n"
            f"Generate one specific, concise question to help the inventor "
            f"better describe their {gap_type.lower().replace('_', ' ')}. "
            f"Return the question only. No explanation. No preamble."
        )

        payload = json.dumps({
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 150,
            "messages": [{"role": "user", "content": prompt}]
        }).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=payload,
            headers={
                "content-type": "application/json",
                "anthropic-version": "2023-06-01",
            }
        )

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            question = data["content"][0]["text"].strip()
            return question if question else None

    except Exception:
        return None  # Always falls back — never raises
