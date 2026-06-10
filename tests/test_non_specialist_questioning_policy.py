"""Characterization tests for NON_SPECIALIST_QUESTIONING_POLICY.

These tests are read-only/static. They inspect repository data only.
They do not require Flask, network, a live session, or runtime execution.
They do not modify files, prompts, domain question banks, routes, or engine logic.
They do not classify S-6, perform FORM T, or start R2.
"""

import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
DOMAIN_JSON = REPO_ROOT / "domains" / "electronics_electrical" / "domain.json"

ENGINEERING_GATED_TERMS = [
    "voltage",
    "current",
    "frequency",
    "circuit",
    "component",
    "signal transformation",
    "electrical constraints",
    "datasheet",
    "calculation",
    "manufacturing tolerance",
]

R1_QUESTION_FRAGMENTS = [
    "electronic circuit achieves its intended function",
    "electronic components are central to your mechanism",
    "signal or energy transformation",
    "energy or power for your design",
    "voltage, current",
    "known electrical constraints",
]


def load_domain_bank() -> dict:
    """Read-only load of the electronics_electrical domain pack."""
    assert DOMAIN_JSON.exists(), f"domain pack not found: {DOMAIN_JSON}"
    with open(DOMAIN_JSON, encoding="utf-8") as f:
        return json.load(f)


def extract_question_texts(bank: dict) -> list[str]:
    """Collect platform-askable question text from the domain JSON tree.

    Supports the observed domain schema:
    "questions": [
        {"question_id": "...", "text": "..."}
    ]

    Also tolerates direct string question fields.
    """
    questions: list[str] = []

    def walk(node):
        if isinstance(node, dict):
            if isinstance(node.get("text"), str) and (
                "question_id" in node or node.get("text", "").strip().endswith("?")
            ):
                questions.append(node["text"])

            for key, value in node.items():
                if key.lower() == "question" and isinstance(value, str):
                    questions.append(value)
                elif key.lower() == "questions":
                    walk(value)
                else:
                    walk(value)

        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(bank)

    return list(dict.fromkeys(questions))


def detect_gated_terms(platform_question_text: str) -> list[str]:
    """Evaluate platform question text only."""
    text = platform_question_text.lower()
    return [term for term in ENGINEERING_GATED_TERMS if term in text]


def test_question_inventory_loads():
    bank = load_domain_bank()
    questions = extract_question_texts(bank)
    assert len(questions) > 0, (
        "electronics_electrical domain pack yielded no enumerable questions"
    )


def test_r1_regression_source_visible():
    raw = DOMAIN_JSON.read_text(encoding="utf-8").lower()
    missing = [frag for frag in R1_QUESTION_FRAGMENTS if frag.lower() not in raw]
    assert not missing, (
        f"R1 source fragments no longer found in domain.json: {missing}"
    )


def test_gated_terms_detectable_in_platform_questions():
    bank = load_domain_bank()
    questions = extract_question_texts(bank)
    flagged = {q: hits for q in questions if (hits := detect_gated_terms(q))}
    assert flagged, (
        "Detector found no engineering-gated terms in the current bank"
    )


@pytest.mark.xfail(
    reason=(
        "Mode separation and non-specialist-safe question flow are not "
        "implemented yet; this test documents the intended future "
        "enforcement target."
    ),
    strict=True,
)
def test_early_non_specialist_questions_have_no_gated_terms():
    bank = load_domain_bank()
    questions = extract_question_texts(bank)
    violations = {q: hits for q in questions if (hits := detect_gated_terms(q))}
    assert not violations, f"engineering-gated terms in question bank: {violations}"


def test_user_responses_not_evaluated_by_policy():
    simulated_record = {
        "question": "What outcome do you want your invention to achieve?",
        "response": (
            "I think it needs some kind of circuit and maybe a 9 volt "
            "voltage supply, but I am not sure."
        ),
    }

    platform_side_hits = detect_gated_terms(simulated_record["question"])
    assert platform_side_hits == []

    hypothetical_violation_hits = detect_gated_terms(simulated_record["response"])
    assert hypothetical_violation_hits != []
