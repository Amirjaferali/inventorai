"""Validation tests for the Path N content config artifact.

Governance chain:
  8ceb5d4  Path N content config artifact          (artifact under test)
  932b7a8  PATH_N_OPTION_A_CONTENT_CONFIG_ARTIFACT_PLAN.md
  fa26744  PATH_N_INTEGRATION_PLAN.md (Option A)
  effd040  PATH_N_CONTENT_APPROVAL_RECORD.md
  221d848  spec tests (detector patterns reused here)
  e2e6234  PATH_N_QUESTION_CONTENT_SPECIFICATION.md

These tests inspect ONLY the Path N artifact JSON under
docs/governance/path_n_content_config/. They have no web-framework
imports, no domain-pack reads, no session execution, and they do
NOT modify any file.
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_PATH = (
    REPO_ROOT
    / "docs"
    / "governance"
    / "path_n_content_config"
    / "electronics_electrical_path_n_questions.json"
)

EXPECTED_METADATA = {
    "path": "Path N",
    "domain": "electronics_electrical",
    "status": "approved_governance_content_runtime_integrated",
    "source_spec": "e2e6234",
    "approval_record": "effd040",
    "integration_plan": "fa26744",
    "artifact_plan": "932b7a8",
}

EXPECTED_GAP_GROUPS = [
    "MECHANISM_COMPLETENESS",
    "PHYSICAL_FEASIBILITY",
    "BOUNDARY_AMBIGUITY",
]

EXPECTED_IDS_IN_ORDER = [
    "N-MC-1", "N-MC-2", "N-MC-3", "N-MC-4",
    "N-PF-1", "N-PF-2", "N-PF-3", "N-PF-4",
    "N-BA-1", "N-BA-2", "N-BA-3",
]

# Disallowed early-gate terms (policy a31010a §5 / plan 932b7a8 §5).
# Word boundaries prevent false positives such as 'currently'.
DISALLOWED_TERM_PATTERNS = {
    "voltage": r"\bvoltage\b",
    "current": r"\bcurrent\b",
    "frequency": r"\bfrequency\b",
    "circuit architecture": r"\bcircuit architecture\b",
    "component-level selection": r"\bcomponent-level selection\b",
    "signal transformation": r"\bsignal transformation\b",
    "datasheet": r"\bdatasheet\b",
    "calculation": r"\bcalculation\b",
    "manufacturing tolerance": r"\bmanufacturing tolerance",
    "electrical constraints": r"\belectrical constraints\b",
}

# R1 regression markers (drift record 10d6876) — must be ABSENT here.
R1_REGRESSION_PATTERNS = {
    "electronic circuit achieves": r"\belectronic circuit achieves\b",
    "electronic components": r"\belectronic components\b",
    "signal or energy transformation": r"\bsignal or energy transformation\b",
    "voltage/current/frequency": r"\bvoltage/current/frequency\b",
    "electrical constraints": r"\belectrical constraints\b",
}


def load_artifact() -> dict:
    assert ARTIFACT_PATH.exists(), f"artifact not found: {ARTIFACT_PATH}"
    with open(ARTIFACT_PATH, encoding="utf-8") as f:
        return json.load(f)


def all_questions(artifact: dict) -> list[dict]:
    """Flatten gap groups into ordered [{question_id, text}, ...]."""
    out: list[dict] = []
    for group in EXPECTED_GAP_GROUPS:
        out.extend(artifact.get("gaps", {}).get(group, []))
    return out


# ---------------------------------------------------------------------------
# Test 1 — Artifact exists and parses as JSON
# ---------------------------------------------------------------------------

def test_artifact_exists_and_parses():
    artifact = load_artifact()
    assert isinstance(artifact, dict) and artifact, "artifact empty or not an object"


# ---------------------------------------------------------------------------
# Test 2 — Metadata is correct
# ---------------------------------------------------------------------------

def test_metadata_correct():
    meta = load_artifact().get("metadata", {})
    mismatches = {
        key: meta.get(key)
        for key, expected in EXPECTED_METADATA.items()
        if meta.get(key) != expected
    }
    assert not mismatches, f"metadata mismatches: {mismatches}"
    assert meta.get("runtime_integrated") is True, (
        f"runtime_integrated must be true, got: {meta.get('runtime_integrated')!r}"
    )


# ---------------------------------------------------------------------------
# Test 3 — All eleven IDs exist in order
# ---------------------------------------------------------------------------

def test_all_ids_present_in_order():
    ids = [q.get("question_id") for q in all_questions(load_artifact())]
    assert ids == EXPECTED_IDS_IN_ORDER, (
        f"ID set/order mismatch:\n  got      {ids}\n  expected {EXPECTED_IDS_IN_ORDER}"
    )


# ---------------------------------------------------------------------------
# Test 4 — Gap groups exist
# ---------------------------------------------------------------------------

def test_gap_groups_exist():
    gaps = load_artifact().get("gaps", {})
    missing = [g for g in EXPECTED_GAP_GROUPS if g not in gaps]
    assert not missing, f"missing gap groups: {missing}"


# ---------------------------------------------------------------------------
# Test 5 — Question text is non-empty
# ---------------------------------------------------------------------------

def test_question_text_non_empty():
    empty = [
        q.get("question_id")
        for q in all_questions(load_artifact())
        if not (isinstance(q.get("text"), str) and q["text"].strip())
    ]
    assert not empty, f"questions with empty text: {empty}"


# ---------------------------------------------------------------------------
# Test 6 — No disallowed early-gate terms in question text
# ---------------------------------------------------------------------------

def test_no_disallowed_terms():
    violations = {}
    for q in all_questions(load_artifact()):
        hits = [
            term
            for term, pattern in DISALLOWED_TERM_PATTERNS.items()
            if re.search(pattern, q.get("text", ""), re.IGNORECASE)
        ]
        if hits:
            violations[q.get("question_id")] = hits
    assert not violations, f"disallowed early-gate terms found: {violations}"


def test_word_boundary_guard():
    """'current' must not match inside 'currently'."""
    assert not re.search(
        DISALLOWED_TERM_PATTERNS["current"], "currently working", re.IGNORECASE
    )
    assert re.search(
        DISALLOWED_TERM_PATTERNS["current"], "the current it draws", re.IGNORECASE
    )


# ---------------------------------------------------------------------------
# Test 7 — R1 regression markers absent
# ---------------------------------------------------------------------------

def test_r1_regression_markers_absent():
    violations = {}
    for q in all_questions(load_artifact()):
        hits = [
            marker
            for marker, pattern in R1_REGRESSION_PATTERNS.items()
            if re.search(pattern, q.get("text", ""), re.IGNORECASE)
        ]
        if hits:
            violations[q.get("question_id")] = hits
    assert not violations, f"R1 regression markers found: {violations}"


# ---------------------------------------------------------------------------
# Test 8 — No runtime/domain dependency (static self-inspection)
# ---------------------------------------------------------------------------

def test_no_runtime_or_domain_dependency():
    """Static assertion on THIS module's own source.

    Needles are built by concatenation below so that this check
    function does not trip on its own literals; any REAL dependency
    elsewhere in the module would use the plain literal and be caught.
    """
    source = Path(__file__).read_text(encoding="utf-8")
    body = source.split("def test_no_runtime_or_domain_dependency", 1)[0]

    needle_flask = "import " + "flask"
    needle_domain = "domains/electronics_electrical/" + "domain.json"
    needle_route = "start_" + "ilt002"
    needle_run = "app." + "run"

    assert needle_flask not in body.lower(), "module imports the web framework"
    assert needle_domain not in body, "module reads the domain pack file"
    assert needle_route not in body, "module references session routes"
    assert needle_run not in body, "module starts the app"


# ---------------------------------------------------------------------------
# Test 9 — runtime_integrated remains false (integration tripwire)
# ---------------------------------------------------------------------------

def test_runtime_integrated_remains_true_post_phase4():
    """Post-Phase-4 invariant (Phase 4 authority
    PHASE_4_PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION.md): the flag must
    remain true after authorized runtime integration. Any future
    regression of this flag to false outside a separately authorized
    rollback action fails the suite loudly."""
    meta = load_artifact().get("metadata", {})
    assert meta.get("runtime_integrated") is True, (
        "runtime_integrated reverted to false unexpectedly — any "
        "reversal requires its own recorded rollback authorization"
    )
