"""Phase 4A — rename the misleading Section 4 heading.

Section 4 contains captured inputs, evidence references (See EV-00N), assessment
status, and verification-needed notes — NOT true testable engineering
requirements. The user-visible heading is renamed from "Requirements" to
"Captured Inputs and Assessment Status" (and the group lede aligned) so the
report no longer implies engineering readiness. Presentation-only: the
section_4_requirements data key, the REQ-00N item ids, and the EV references are
all unchanged.
"""
import os, sys, uuid
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import IdeaState, Evidence, REASONED
from web.app import app, SESSION_STORE

PROBLEM = ("Meat spoils when the refrigerated compartment drifts out of its safe "
           "temperature band during transit and the driver is not warned in time.")
MECHANISM = ("A microcontroller reads several digital temperature sensors, logs each "
             "reading, and raises a wireless alert to the cabin when the band is exceeded.")


def _state():
    s = IdeaState(idea_id="p4a-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 2
    s.current_stage = 3
    s.idea_summary = PROBLEM
    s.known_problem = Evidence(PROBLEM, REASONED, 1)
    s.known_mechanism = Evidence(MECHANISM, REASONED, 2)
    return s


def _render(state):
    sid = "p4a-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        return resp.status_code, resp.get_data(as_text=True)
    finally:
        SESSION_STORE.pop(sid, None)


# --- renamed visible heading ------------------------------------------------

def test_new_heading_is_shown():
    status, body = _render(_state())
    assert status == 200
    assert "<h3>Captured Inputs and Assessment Status</h3>" in body


def test_old_requirements_h3_is_gone():
    _, body = _render(_state())
    assert "<h3>Requirements</h3>" not in body
    # the misleading plural word no longer appears anywhere in the report
    assert "Requirements" not in body


def test_group_lede_no_longer_leads_with_requirements():
    _, body = _render(_state())
    assert "Requirements and open areas that still have to be worked out." not in body
    assert "The inputs we captured and the open areas that still have to be worked out." in body


def test_friendly_group_heading_unchanged():
    _, body = _render(_state())
    assert "<h2>What it needs</h2>" in body


# --- data / IDs / references unchanged (presentation-only) -------------------

def test_section4_data_key_and_req_ids_unchanged():
    pkg = assemble_deliverable(_state())
    assert "section_4_requirements" in pkg                     # canonical key intact
    reqs = pkg["section_4_requirements"]["requirements"]
    assert [r["id"] for r in reqs] == ["REQ-001", "REQ-002"]   # ids not renamed
    assert reqs[0]["statement"] == "See EV-001 — Known Problem"
    assert reqs[1]["statement"] == "See EV-002 — Known Mechanism"


def test_rendered_req_lines_and_ev_references_unchanged():
    _, body = _render(_state())
    assert "REQ-001 — See EV-001 — Known Problem" in body
    assert "REQ-002 — See EV-002 — Known Mechanism" in body


def test_registries_and_landscape_untouched():
    pkg = assemble_deliverable(_state())
    ev_ids = {e["evidence_id"] for e in pkg["_session_meta"]["evidence_registry"]}
    assert ev_ids == {"EV-001", "EV-002"}                      # Phase 3A intact
    assert "unknown_registry" in pkg["_session_meta"]          # Phase 3B-1 intact
    _, body = _render(_state())
    assert "Requirement Landscape" in body                     # Section 13 heading unchanged


# --- honest framing preserved -----------------------------------------------

def test_advisory_framing_preserved():
    _, body = _render(_state())
    assert "Derived readiness" in body
    assert "not technically verified" in body
