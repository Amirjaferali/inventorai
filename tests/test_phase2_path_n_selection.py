"""Phase 2 Path N content selection tests."""

import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import pytest

from engine.idea_state import IdeaState
from engine.path_n_questions import get_path_n_question
from engine.progression_loop import QUESTIONS, get_question, run_iteration


REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_PATH = (
    REPO_ROOT / "docs" / "governance" / "path_n_content_config"
    / "electronics_electrical_path_n_questions.json"
)

DOMAIN = "electronics_electrical"
LEGACY_DEFAULT = "legacy_undesignated_current_behavior"

STAGE2_GAPS = [
    "MECHANISM_COMPLETENESS",
    "PHYSICAL_FEASIBILITY",
    "BOUNDARY_AMBIGUITY",
]

STAGE3_GAPS = [
    "PROBLEM_MECHANISM_FIT",
    "ASSUMPTION_INVENTORY",
    "EXPERTISE_GAP_AWARENESS",
]

DISALLOWED_TERM_PATTERNS = {
    "voltage": r"\bvoltage\b",
    "current": r"\bcurrent\b",
    "frequency": r"\bfrequency\b",
    "circuit architecture": r"\bcircuit architecture\b",
    "component-level selection": r"\bcomponent-level selection\b",
    "signal transformation": r"\bsignal transformation\b",
    "datasheet": r"\bdatasheet\b",
    "calculation": r"\bcalculation\b",
    "manufacturing tolerance": r"\bmanufacturing tolerance\b",
    "electrical constraints": r"\belectrical constraints\b",
}


def _artifact_gaps() -> dict:
    return json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))["gaps"]


def _artifact_texts() -> set[str]:
    return {
        entry["text"]
        for variants in _artifact_gaps().values()
        for entry in variants
    }


def _legacy_expected(domain: str, gap_type: str, iterations_open: int) -> str:
    from engine.domain_rules import get_domain_question

    domain_q = get_domain_question(domain, gap_type, iterations_open)
    if domain_q:
        return domain_q

    variants = QUESTIONS[gap_type]
    return variants[min(iterations_open, len(variants) - 1)]


def _make_state(path_value=None) -> IdeaState:
    state = IdeaState(idea_id="phase2-test")
    state.domain = DOMAIN
    state.domain_signal = DOMAIN
    if path_value is not None:
        state.path = path_value
    return state


@pytest.fixture(scope="module")
def artifact_sha_before():
    return hashlib.sha256(ARTIFACT_PATH.read_bytes()).hexdigest()


def test_artifact_gap_keys_align_with_engine_questions():
    for key in _artifact_gaps():
        assert key in QUESTIONS


def test_path_n_selection_matches_artifact_across_iterations():
    gaps = _artifact_gaps()

    for gap_type in STAGE2_GAPS:
        variants = gaps[gap_type]

        for n in range(len(variants) + 3):
            expected = variants[min(n, len(variants) - 1)]["text"]

            assert get_path_n_question(gap_type, n) == expected
            assert get_question(DOMAIN, gap_type, n, path="N") == expected


def test_legacy_behavior_preserved_for_default_and_legacy_path():
    for gap_type in STAGE2_GAPS + STAGE3_GAPS:
        for n in range(4):
            expected = _legacy_expected(DOMAIN, gap_type, n)

            assert get_question(DOMAIN, gap_type, n) == expected
            assert get_question(DOMAIN, gap_type, n, path=LEGACY_DEFAULT) == expected


def test_unknown_path_values_use_legacy_not_path_n():
    path_n_texts = _artifact_texts()

    for path_value in ["", "X", LEGACY_DEFAULT, None]:
        for gap_type in STAGE2_GAPS:
            q = get_question(DOMAIN, gap_type, 0, path=path_value)

            assert q == _legacy_expected(DOMAIN, gap_type, 0)
            assert q not in path_n_texts


def test_ai_cannot_displace_path_n_content(monkeypatch):
    import engine.ai_advisor as ai_advisor

    sentinel = "AI OVERRIDE SENTINEL QUESTION"
    monkeypatch.setattr(ai_advisor, "get_ai_question", lambda *a, **k: sentinel)

    for gap_type in STAGE2_GAPS:
        q = get_question(DOMAIN, gap_type, 0, path="N")
        assert q != sentinel
        assert q in _artifact_texts()


def test_stage3_path_n_falls_through_to_generic_questions():
    for gap_type in STAGE3_GAPS:
        assert get_path_n_question(gap_type, 0) is None

        for n in range(3):
            variants = QUESTIONS[gap_type]
            expected = variants[min(n, len(variants) - 1)]
            assert get_question(DOMAIN, gap_type, n, path="N") == expected


def test_no_disallowed_terms_in_path_n_questions():
    violations = {}

    for question in _artifact_texts():
        hits = [
            term
            for term, pattern in DISALLOWED_TERM_PATTERNS.items()
            if re.search(pattern, question, re.IGNORECASE)
        ]
        if hits:
            violations[question] = hits

    assert not violations


def test_path_n_selection_is_deterministic():
    first = [
        get_question(DOMAIN, gap_type, n, path="N")
        for gap_type in STAGE2_GAPS
        for n in range(4)
    ]

    second = [
        get_question(DOMAIN, gap_type, n, path="N")
        for gap_type in STAGE2_GAPS
        for n in range(4)
    ]

    assert first == second


def test_runtime_session_path_n_does_not_use_ai_question(monkeypatch):
    import engine.ai_advisor as ai_advisor

    sentinel = "AI OVERRIDE SENTINEL QUESTION"
    monkeypatch.setattr(ai_advisor, "get_ai_question", lambda *a, **k: sentinel)

    state = _make_state("N")
    result = run_iteration(
        state,
        "An electronic lock that opens when the right code is entered.",
    )

    question = result.get("question")
    if question is not None:
        assert question != sentinel


def test_artifact_unmodified_by_suite(artifact_sha_before):
    sha_after = hashlib.sha256(ARTIFACT_PATH.read_bytes()).hexdigest()
    assert sha_after == artifact_sha_before
