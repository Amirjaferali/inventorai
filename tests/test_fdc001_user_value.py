"""
FDC-001 user-value correction.

Three user-facing defects, fixed at the deliverable layer only (no progression,
maturity, domain, or governance change):

  1. "Known Problem" must show the inventor's actual problem evidence, never a
     repeat of the mechanism text (RISK-002 can populate state.known_problem
     from a mechanism answer).
  2. The internal phrase "Phase 5" must not appear in user-visible FDC-001
     content (the "ODS-001" reference is preserved).
  3. A "Recommended Next Steps" section is present, synthesized only from
     already-computed state and captured evidence.
"""
import os, sys, uuid, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.idea_state import (
    IdeaState, Gap, Evidence, AcknowledgedUnknown,
    OPEN, PARTIAL, CLOSED, REASONED, DEMONSTRATED,
    MECHANISM_COMPLETENESS, PROBLEM_MECHANISM_FIT,
    ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
)
from engine.deliverable_assembler import assemble_deliverable
from web.app import app, SESSION_STORE

MECH_AS_PROBLEM = (
    "The device uses a capacitive moisture sensor clamped at the pipe joint, and "
    "when water escapes it changes the sensor capacitance, which the ESP32 reads.")
MECH_PROPER = (
    "Inside the mechanism there is a moisture sensor, an ESP32, a buzzer and a "
    "WiFi radio; the microcontroller samples the sensor and triggers the alarm.")
PMF_PROBLEM = (
    "The problem is early detection of a slow household leak before it causes "
    "hidden damage, and the moisture sensor fits because a leak first appears as "
    "surface water at the joint.")


def _polluted_state():
    """Mirrors the real water-leak journey: known_problem holds mechanism text,
    the genuine problem lives in PROBLEM_MECHANISM_FIT evidence."""
    s = IdeaState(idea_id="uv-" + uuid.uuid4().hex[:8])
    s.domain = "electronics_electrical"; s.domain_signal = "electronics_electrical"
    s.maturity_level = 2; s.current_stage = 3
    s.known_problem = Evidence(MECH_AS_PROBLEM, REASONED, 1)     # RISK-002 pollution
    s.known_mechanism = Evidence(MECH_PROPER, REASONED, 2)
    pmf = Gap(gap_type=PROBLEM_MECHANISM_FIT, status=CLOSED, opened_at=3)
    pmf.evidence.append(Evidence(PMF_PROBLEM, REASONED, 3))
    s.gaps.append(pmf)
    return s


# --- Defect 1: Known Problem shows actual problem evidence -------------------

def test_known_problem_uses_problem_evidence_not_mechanism():
    s = _polluted_state()
    s2 = assemble_deliverable(s)["section_2_invention_summary"]
    assert s2["known_problem"]["content"] == PMF_PROBLEM
    assert s2["known_problem"]["content"] != MECH_AS_PROBLEM
    assert s2["known_problem"]["content"] != s2["known_mechanism"]["content"]


def test_requirement_functional_uses_problem_evidence():
    s = _polluted_state()
    reqs = assemble_deliverable(s)["section_4_requirements"]["requirements"]
    func = [r for r in reqs if r["type"] == "functional"]
    assert func and func[0]["statement"] == PMF_PROBLEM


def test_legacy_known_problem_not_surfaced_without_pmf_even_if_distinct():
    # Provenance rule: without accepted PMF evidence, state.known_problem is
    # NEVER surfaced — even when it differs textually from known_mechanism. A
    # textual difference is not proof it is genuine problem evidence (it can be
    # a mechanism answer captured by RISK-002). The honest note is shown instead.
    s = IdeaState(idea_id="uv-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"; s.maturity_level = 2
    s.known_problem = Evidence(MECH_AS_PROBLEM, REASONED, 1)   # mechanism answer
    s.known_mechanism = Evidence(MECH_PROPER, REASONED, 2)     # textually distinct
    s2 = assemble_deliverable(s)["section_2_invention_summary"]
    assert s2["known_problem"] is None
    assert s2["known_problem_note"] == "Problem evidence has not yet been captured clearly."
    # and the mechanism text never leaks into the functional requirement either
    reqs = assemble_deliverable(s)["section_4_requirements"]["requirements"]
    assert not [r for r in reqs if r["type"] == "functional"]


def test_known_problem_hidden_when_duplicate_of_mechanism_and_no_pmf():
    # Pollution with NO problem evidence anywhere: do not surface mechanism text.
    s = IdeaState(idea_id="uv-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"; s.maturity_level = 2
    s.known_problem = Evidence(MECH_PROPER, REASONED, 1)
    s.known_mechanism = Evidence(MECH_PROPER, REASONED, 2)
    s2 = assemble_deliverable(s)["section_2_invention_summary"]
    assert s2["known_problem"] is None
    assert s2["known_problem_note"]


def test_no_problem_evidence_yields_none_with_honest_note():
    s = IdeaState(idea_id="uv-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    s2 = assemble_deliverable(s)["section_2_invention_summary"]
    assert s2["known_problem"] is None
    assert s2["known_problem_note"] == "Problem evidence has not yet been captured clearly."


# --- Defect 2: no user-visible "Phase 5" ------------------------------------

def _all_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values(): yield from _all_strings(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj: yield from _all_strings(v)


def test_no_phase5_anywhere_in_package():
    s = _polluted_state()
    for text in _all_strings(assemble_deliverable(s)):
        assert "Phase 5" not in text, f"'Phase 5' leaked: {text!r}"


def test_completeness_string_has_no_phase5():
    s = _polluted_state()
    comp = assemble_deliverable(s)["section_2_invention_summary"]["assessment_completeness"]
    assert "Phase 5" not in comp and comp.startswith("COMPLETE")


def test_ods001_reference_preserved():
    s = _polluted_state()
    note = assemble_deliverable(s)["section_7_recommendations"]["category_b_material_selection"]["note"]
    assert "ODS-001" in note and "Phase 5" not in note


# --- Defect 3: Recommended Next Steps section -------------------------------

def test_next_steps_section_present():
    pkg = assemble_deliverable(_polluted_state())
    assert "section_10_recommended_next_steps" in pkg
    assert "items" in pkg["section_10_recommended_next_steps"]


def test_next_steps_synthesized_from_state_only():
    # maturity 2, all gaps closed, REASONED evidence, one acknowledged unknown.
    s = _polluted_state()
    s.acknowledged_unknowns.append(
        AcknowledgedUnknown(iteration=5, gap_context=ASSUMPTION_INVENTORY,
                            verbatim="the exact moisture threshold is unknown",
                            category_basis="explicit"))
    items = assemble_deliverable(s)["section_10_recommended_next_steps"]["items"]
    actions = " ".join(i["action"] for i in items)
    # validation step (REASONED -> Demonstrated) and the stated unknown, both
    # traceable to existing state via the basis field.
    assert any(i["basis"] == "evidence_quality:REASONED" for i in items)
    assert any(i["basis"].startswith("acknowledged_unknown:") for i in items)
    assert "the exact moisture threshold is unknown" in actions
    for i in items:                       # every step names its state source
        assert i.get("basis")


def test_next_steps_reference_open_gaps():
    s = IdeaState(idea_id="uv-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"; s.maturity_level = 2
    s.gaps.append(Gap(gap_type=EXPERTISE_GAP_AWARENESS, status=OPEN, opened_at=1))
    items = assemble_deliverable(s)["section_10_recommended_next_steps"]["items"]
    assert any(i["basis"] == f"open_gap:{EXPERTISE_GAP_AWARENESS}" for i in items)


def test_next_steps_no_duplicate_actions_from_duplicate_evidence():
    s = IdeaState(idea_id="uv-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"; s.maturity_level = 2
    same = "the exact moisture threshold is unknown"
    for it in (3, 4):  # same unknown stated twice
        s.acknowledged_unknowns.append(
            AcknowledgedUnknown(iteration=it, gap_context=ASSUMPTION_INVENTORY,
                                verbatim=same, category_basis="explicit"))
    items = assemble_deliverable(s)["section_10_recommended_next_steps"]["items"]
    actions = [i["action"] for i in items]
    assert len(actions) == len(set(actions))            # no duplicate actions
    assert sum(1 for a in actions if same in a) == 1    # collapsed to one


def test_next_steps_absent_evidence_invents_nothing():
    # Level 0, no gaps, no unknowns, no REASONED/DEMONSTRATED leading evidence.
    s = IdeaState(idea_id="uv-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    sec = assemble_deliverable(s)["section_10_recommended_next_steps"]
    # only the honest maturity step may appear (traceable); nothing invented
    for i in sec["items"]:
        assert i["basis"].startswith(("open_gap:", "maturity_level:",
                                      "acknowledged_unknown:", "evidence_quality:"))


def test_next_steps_empty_state_is_honest():
    # maturity 2, no gaps, no unknowns, no REASONED leading evidence.
    s = IdeaState(idea_id="uv-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"; s.maturity_level = 2
    sec = assemble_deliverable(s)["section_10_recommended_next_steps"]
    assert sec["items"] == []
    assert sec["empty_statement"]


def test_package_still_json_serialisable():
    json.dumps(assemble_deliverable(_polluted_state()), default=str)


# --- Rendering integration --------------------------------------------------

def test_rendered_deliverable_shows_next_steps_and_problem():
    s = _polluted_state()
    s.acknowledged_unknowns.append(
        AcknowledgedUnknown(iteration=5, gap_context=ASSUMPTION_INVENTORY,
                            verbatim="the exact moisture threshold is unknown",
                            category_basis="explicit"))
    sid = "uv-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": []}
    try:
        body = app.test_client().get(f"/session/{sid}/deliverable").get_data(as_text=True)
        assert "Recommended Next Steps" in body
        assert PMF_PROBLEM[:30] in body          # actual problem rendered
        assert MECH_AS_PROBLEM[:30] not in body  # mechanism text not shown as problem
        assert "Phase 5" not in body
    finally:
        SESSION_STORE.pop(sid, None)
