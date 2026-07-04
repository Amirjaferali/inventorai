"""Phase 8A — display-only Section 4 clarification note.

Adds a short advisory note under the Section 4 "Captured Inputs and Assessment
Status" heading, reinforcing that the listed items are inputs captured from the
inventor's answers (not tested conclusions) and pointing to the Section 14
suggested checks. Display-only: no requirement/candidate/spec/acceptance-criteria
generation, no data-model change, no Section 13/14 change, no reintroduction of
the old "Requirements" heading, and no ranking/criticality/validation wording.
"""
import os, sys, uuid
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import IdeaState, Evidence, REASONED
from web.app import app, SESSION_STORE

PROBLEM = "Meat spoils when the refrigerated compartment drifts out of its safe band."
MECHANISM = "A microcontroller reads several digital temperature sensors and alerts the cabin."

NOTE = ("These are inputs captured from your answers, not tested conclusions. "
        "The suggested checks further down show what could help firm them up.")

# wording the clarification note must NOT introduce
_FORBIDDEN = ["requirements", "specification", "acceptance criteria", "validated",
              "verified", "feasible", "certified", "patentable", "market-ready",
              "build-ready", "guaranteed", "criticality", "testable requirement",
              "candidate requirement"]


def _state():
    s = IdeaState(idea_id="p8a-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 2
    s.current_stage = 3
    s.idea_summary = PROBLEM
    s.known_problem = Evidence(PROBLEM, REASONED, 1)
    s.known_mechanism = Evidence(MECHANISM, REASONED, 2)
    return s


def _render(state):
    sid = "p8a-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        return resp.status_code, resp.get_data(as_text=True)
    finally:
        SESSION_STORE.pop(sid, None)


# --- the clarification note -------------------------------------------------

def test_clarification_note_renders():
    status, body = _render(_state())
    assert status == 200
    assert NOTE in body


def test_section4_heading_preserved():
    _, body = _render(_state())
    assert "<h3>Captured Inputs and Assessment Status</h3>" in body


def test_old_requirements_heading_not_reintroduced():
    _, body = _render(_state())
    assert "<h3>Requirements</h3>" not in body


def test_note_uses_no_forbidden_wording():
    note = NOTE.lower()
    for w in _FORBIDDEN:
        assert w not in note, f"forbidden wording in clarification note: {w!r}"


# --- nothing generated / IDs unchanged --------------------------------------

def test_no_requirement_or_spec_generated_in_section4_data():
    # The note is display-only: section_4 data is unchanged; REQ items still
    # reference the evidence registry (captured inputs), not generated requirements.
    pkg = assemble_deliverable(_state())
    reqs = pkg["section_4_requirements"]["requirements"]
    assert [r["id"] for r in reqs] == ["REQ-001", "REQ-002"]
    assert reqs[0]["statement"] == "See EV-001 — Known Problem"
    assert reqs[1]["statement"] == "See EV-002 — Known Mechanism"


# --- sections 13 / 14 untouched ---------------------------------------------

def test_section_13_and_14_unchanged():
    pkg = assemble_deliverable(_state())
    # Section 13 present and its labels unchanged
    assert pkg["section_13_requirement_landscape"]["title"] == "Requirement Landscape"
    # Section 14 present, confidence stays UNDETERMINED for any steps
    vp = pkg["section_14_validation_plan"]
    assert vp["title"] == "Validation Plan"
    assert all(st["confidence"] == "UNDETERMINED" for st in vp["steps"])
    _, body = _render(_state())
    assert "Requirement Landscape" in body
    assert "<h3>Validation Plan</h3>" in body


def test_contract_and_advisory_framing_intact():
    pkg = assemble_deliverable(_state())
    assert len([k for k in pkg if k.startswith("section_")]) == 14
    _, body = _render(_state())
    assert "Derived readiness" in body
    assert "not technically verified" in body
