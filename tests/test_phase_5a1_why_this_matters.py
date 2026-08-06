"""Phase 5A-1 — display-only "Why this matters" for Section 5 assumptions.

Surfaces the already-recorded, non-rendered `risk_if_invalid` field for each
Section 5 assumption as an advisory line ("Why this matters: <risk_if_invalid>").
Display-only: no capture, no data-model change, no ranking, no criticality/
priority labels, no new claim. When `risk_if_invalid` is absent/empty nothing is
fabricated. Sections 10/11/13 and the EV/UNK registries are untouched.
"""
import os, sys, uuid
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import IdeaState, Evidence, REASONED
from web.app import app, SESSION_STORE

PROBLEM = "Meat spoils when the refrigerated compartment drifts out of its safe band."
MECHANISM = "A microcontroller reads several digital temperature sensors and alerts the cabin."

# forbidden wording that this display-only change must NOT introduce
_FORBIDDEN = ["criticality", "critical", "severity", "priority",
              "certified", "patentable", "market-ready", "build-ready",
              "High priority", "Medium priority", "Low priority"]


def _state(mechanism=MECHANISM):
    s = IdeaState(idea_id="p5a1-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 2
    s.current_stage = 3
    s.idea_summary = PROBLEM
    s.known_problem = Evidence(PROBLEM, REASONED, 1)
    if mechanism is not None:
        s.known_mechanism = Evidence(mechanism, REASONED, 2)
    return s


def _render(state):
    sid = "p5a1-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        return resp.status_code, resp.get_data(as_text=True)
    finally:
        SESSION_STORE.pop(sid, None)


def _section5(body):
    """The rendered Section 5 slice (assumptions/unknowns group)."""
    i = body.find("What is assumed")
    j = body.find("What could go wrong")
    assert i >= 0 and j > i
    return body[i:j]


# --- present case -----------------------------------------------------------

def test_risk_if_invalid_renders_as_why_this_matters():
    state = _state()
    asmp = assemble_deliverable(state)["section_5_assumptions"]["assumptions"]
    assert asmp and asmp[0].get("risk_if_invalid"), "fixture expected an assumption with risk_if_invalid"
    status, body = _render(state)
    assert status == 200
    sect5 = _section5(body)
    assert "Why this matters:" in sect5
    # the exact recorded field text is surfaced verbatim (no summary, no fabrication)
    assert asmp[0]["risk_if_invalid"] in sect5


def test_assumption_and_validation_approach_still_shown():
    state = _state()
    _, body = _render(state)
    asmp = assemble_deliverable(state)["section_5_assumptions"]["assumptions"]
    sect5 = _section5(body)
    assert asmp[0]["assumption"] in sect5
    assert asmp[0]["validation_approach"] in sect5


# --- absent case ------------------------------------------------------------

def test_no_why_this_matters_when_no_assumptions():
    # A low-maturity state with no mechanism produces no assumptions -> no line,
    # and no fabricated default text.
    state = IdeaState(idea_id="empty", domain_signal="electronics_electrical")
    assert assemble_deliverable(state)["section_5_assumptions"]["assumptions"] == []
    _, body = _render(state)
    assert "Why this matters:" not in _section5(body)


# --- no criticality/priority wording introduced -----------------------------

def test_no_criticality_or_priority_wording_introduced_in_assumptions_line():
    # Scan only the assumptions list region: the surfaced field must not carry
    # ranking/criticality vocabulary, and this change introduces none.
    state = _state()
    _, body = _render(state)
    sect5 = _section5(body)
    # locate just the "Why this matters:" advisory text we added
    idx = sect5.find("Why this matters:")
    advisory = sect5[idx: idx + 160].lower()
    for w in _FORBIDDEN:
        assert w.lower() not in advisory, f"forbidden wording surfaced: {w!r}"


# --- non-regression: sections 10/11/13 and registries untouched -------------

def test_sections_10_11_13_and_registries_unchanged():
    pkg = assemble_deliverable(_state())
    # Section 13 criticality still frozen UNDETERMINED / system-derived is
    # governed elsewhere; here we only assert this display change did not add or
    # remove requirement-landscape entries or registries.
    assert "section_13_requirement_landscape" in pkg
    assert "section_10_recommended_next_steps" in pkg
    assert "section_11_prototype_test_plan" in pkg
    ev_ids = {e["evidence_id"] for e in pkg["_session_meta"]["evidence_registry"]}
    assert ev_ids == {"EV-001", "EV-002"}
    assert "unknown_registry" in pkg["_session_meta"]
    # canonical contract intact
    assert len([k for k in pkg if k.startswith("section_")]) == 14


def test_advisory_framing_preserved():
    _, body = _render(_state())
    assert "Derived readiness" in body
    assert "not technically verified" in body
