"""Phase 3A — Evidence Registry pilot for problem/mechanism deduplication.

Full problem/mechanism text appears once (Section 2 / registry); Section 4
REQ-001/REQ-002 reference the registry entries (EV-001/EV-002) instead of
re-copying the long text. Additive and nested under _session_meta so the
top-level canonical-section contract is unchanged. No evidence is deleted and no
claim is added.
"""
import os, sys, uuid
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import IdeaState, Evidence, REASONED
from web.app import app, SESSION_STORE

PROBLEM = ("Delivered meat spoils when the refrigerated compartment drifts out of "
           "its safe temperature band during transit and the driver is not warned in time.")
MECHANISM = ("A microcontroller reads several digital temperature sensors, logs each "
             "reading, and raises a wireless alert to the cabin when the band is exceeded.")

TOP_LEVEL_ENVELOPE = {"package_version", "schema_id", "session_id", "generated_at"}
CANONICAL_SECTIONS = {
    "section_1_disclaimer", "section_2_invention_summary", "section_3_assessment_overview",
    "section_4_requirements", "section_5_assumptions", "section_6_risks",
    "section_7_recommendations", "section_8_unresolved_items", "section_9_stage3_reasoning",
    "section_10_recommended_next_steps", "section_11_prototype_test_plan",
    "section_12_next_development_step", "section_13_requirement_landscape",
    "section_14_validation_plan",
}


def _state(problem=PROBLEM, mechanism=MECHANISM):
    s = IdeaState(idea_id="ev-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 2
    s.current_stage = 3
    if problem is not None:
        s.idea_summary = problem          # _resolved_problem prefers idea_summary
        s.known_problem = Evidence(problem, REASONED, 1)
    if mechanism is not None:
        s.known_mechanism = Evidence(mechanism, REASONED, 2)
    return s


def _registry(pkg):
    return pkg["_session_meta"]["evidence_registry"]


# --- registry creation ------------------------------------------------------

def test_ev001_created_for_known_problem():
    reg = _registry(assemble_deliverable(_state()))
    ev = {e["evidence_id"]: e for e in reg}
    assert "EV-001" in ev
    assert ev["EV-001"]["label"] == "Known Problem"
    assert ev["EV-001"]["content"] == PROBLEM       # full text carried once
    assert "provenance" in ev["EV-001"]
    assert ev["EV-001"].get("quality_label")


def test_ev002_created_for_known_mechanism():
    reg = _registry(assemble_deliverable(_state()))
    ev = {e["evidence_id"]: e for e in reg}
    assert "EV-002" in ev
    assert ev["EV-002"]["label"] == "Known Mechanism"
    assert ev["EV-002"]["content"] == MECHANISM


def test_stable_fixed_slots_no_fake_entries_when_problem_absent():
    # Mechanism only: it keeps EV-002 (stable slot); no fake EV-001 is created.
    reg = _registry(assemble_deliverable(_state(problem=None)))
    ids = {e["evidence_id"] for e in reg}
    assert ids == {"EV-002"}


def test_stable_fixed_slots_no_fake_entries_when_mechanism_absent():
    reg = _registry(assemble_deliverable(_state(mechanism=None)))
    ids = {e["evidence_id"] for e in reg}
    assert ids == {"EV-001"}


# --- section 4 references (dedup) -------------------------------------------

def test_section4_references_evidence_ids_not_full_text():
    pkg = assemble_deliverable(_state())
    reqs = pkg["section_4_requirements"]["requirements"]
    by_ev = {r.get("evidence_id"): r for r in reqs if r.get("evidence_id")}
    assert by_ev["EV-001"]["statement"] == "See EV-001 — Known Problem"
    assert by_ev["EV-002"]["statement"] == "See EV-002 — Known Mechanism"
    # the full long text is NOT re-copied into section 4
    import json
    blob = json.dumps(pkg["section_4_requirements"])
    assert PROBLEM not in blob
    assert MECHANISM not in blob


def test_every_section4_reference_resolves_to_a_registry_entry():
    pkg = assemble_deliverable(_state())
    reg_ids = {e["evidence_id"] for e in _registry(pkg)}
    for r in pkg["section_4_requirements"]["requirements"]:
        if r.get("evidence_id"):
            assert r["evidence_id"] in reg_ids, f"dangling reference: {r['evidence_id']}"


def test_full_text_appears_once_in_targeted_path():
    pkg = assemble_deliverable(_state())
    import json
    # Section 2 carries the full text; the registry mirrors it; Section 4 does not.
    s2 = json.dumps(pkg["section_2_invention_summary"])
    s4 = json.dumps(pkg["section_4_requirements"])
    assert PROBLEM in s2 and PROBLEM not in s4
    assert MECHANISM in s2 and MECHANISM not in s4


# --- contract + rendering ---------------------------------------------------

def test_top_level_canonical_contract_unchanged():
    pkg = assemble_deliverable(_state())
    assert set(pkg) == TOP_LEVEL_ENVELOPE | CANONICAL_SECTIONS | {"_session_meta"}


def test_section2_renders_visible_ev_ids_and_full_text():
    sid = "ev-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": _state(), "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        assert resp.status_code == 200
        body = resp.get_data(as_text=True)
        assert "(EV-001)" in body and "(EV-002)" in body       # visible ids in Section 2
        assert PROBLEM in body and MECHANISM in body           # full text still visible
        assert "See EV-001 — Known Problem" in body            # Section 4 reference
        assert "See EV-002 — Known Mechanism" in body
        # honest warnings preserved
        assert "Derived readiness" in body
        assert "not technically verified" in body
    finally:
        SESSION_STORE.pop(sid, None)
