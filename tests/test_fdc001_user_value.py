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
    # Phase 3A: the functional requirement references the evidence registry
    # (EV-001) instead of re-copying the full problem text; the problem provenance
    # is proven by the EV-001 registry entry carrying that exact problem evidence.
    s = _polluted_state()
    pkg = assemble_deliverable(s)
    reqs = pkg["section_4_requirements"]["requirements"]
    func = [r for r in reqs if r["type"] == "functional"]
    assert func and func[0].get("evidence_id") == "EV-001"
    assert func[0]["statement"] == "See EV-001 — Known Problem"
    ev001 = next(e for e in pkg["_session_meta"]["evidence_registry"]
                 if e["evidence_id"] == "EV-001")
    assert ev001["content"] == PMF_PROBLEM      # grounded in real problem evidence


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


def test_completeness_string_is_truthful_and_has_no_phase5():
    s = _polluted_state()
    comp = assemble_deliverable(s)["section_2_invention_summary"]["assessment_completeness"]
    assert "Phase 5" not in comp
    # truthful contract: states inquiry completion AND outstanding validation
    assert comp.startswith("INQUIRY COMPLETE")
    low = comp.lower()
    assert "remain outstanding" in low
    assert "validation" in low and "demonstration" in low
    # must NOT imply the invention / development / validation itself is complete
    assert "demonstrated" not in low.replace("demonstration", "")
    for w in ("feasible", "validated", "proven", "ready", "certified"):
        assert w not in low


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
    assert any(i["basis"] == "evidence_quality:Reasoned" for i in items)
    assert any(i["basis"].startswith("acknowledged_unknown:") for i in items)
    # Phase 3B-2a: the unknown next step references the registry (See UNK-00N)
    # instead of repeating the full verbatim; the verbatim is no longer in Section 10.
    assert "See UNK-" in actions
    assert "the exact moisture threshold is unknown" not in actions
    for i in items:                       # every step names its state source
        assert i.get("basis")


def test_next_steps_reference_open_gaps():
    s = IdeaState(idea_id="uv-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"; s.maturity_level = 2
    s.gaps.append(Gap(gap_type=EXPERTISE_GAP_AWARENESS, status=OPEN, opened_at=1))
    items = assemble_deliverable(s)["section_10_recommended_next_steps"]["items"]
    assert any(i["basis"] == "open_gap:Expertise-Gap Awareness" for i in items)


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
    # Phase 3B-2a: the duplicate unknown still collapses to a single action; the
    # action now references the registry (See UNK-00N) rather than the verbatim.
    assert same not in " ".join(actions)                # verbatim no longer repeated
    unknown_actions = [i for i in items if i["basis"].startswith("acknowledged_unknown:")]
    assert len(unknown_actions) == 1                     # collapsed to one


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


# ===========================================================================
# Known Problem provenance (idea_summary first) + truthful completeness.
# Selection is by capture provenance, never keywords/string analysis.
# ===========================================================================

CYCLIST_PROBLEM = ("Cyclists often slow suddenly but drivers behind may not notice in time, "
                   "especially at night, leaving little warning before a rear collision")
PMF_FIT_FIRST = ("This mechanism is a good fit because the accelerometer measures the same "
                 "deceleration a driver would want warning of, and the light brightens on braking")
BIKE_MECH = ("Inside the mechanism there is a three-axis accelerometer, a microcontroller, a "
             "MOSFET driver and an LED array that brightens when deceleration exceeds a threshold")


def _bike_state(idea_summary=CYCLIST_PROBLEM):
    s = IdeaState(idea_id="tl-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"; s.maturity_level = 2; s.current_stage = 3
    if idea_summary is not None:
        s.idea_summary = idea_summary
    s.known_mechanism = Evidence(BIKE_MECH, REASONED, 2)
    pmf = Gap(gap_type=PROBLEM_MECHANISM_FIT, status=CLOSED, opened_at=3)
    pmf.evidence.append(Evidence(PMF_FIT_FIRST, REASONED, 4))   # mechanism-fit FIRST
    s.gaps.append(pmf)
    return s


def test_idea_summary_takes_priority_over_pmf_for_known_problem():
    s = _bike_state()
    s2 = assemble_deliverable(s)["section_2_invention_summary"]
    assert s2["known_problem"]["content"] == CYCLIST_PROBLEM          # provenance wins


def test_mechanism_fit_first_pmf_cannot_replace_present_idea_summary():
    s = _bike_state()
    kp = assemble_deliverable(s)["section_2_invention_summary"]["known_problem"]["content"]
    assert kp != PMF_FIT_FIRST
    assert not kp.startswith("This mechanism is a good fit because")


def test_known_mechanism_unchanged_by_problem_fix():
    s = _bike_state()
    assert assemble_deliverable(s)["section_2_invention_summary"]["known_mechanism"]["content"] == BIKE_MECH


def test_pmf_fallback_when_idea_summary_absent():
    s = _bike_state(idea_summary=None)   # no problem-establishment capture
    kp = assemble_deliverable(s)["section_2_invention_summary"]["known_problem"]["content"]
    assert kp == PMF_FIT_FIRST           # falls back to accepted PMF evidence


def test_honest_absence_when_both_absent():
    s = IdeaState(idea_id="tl-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"; s.maturity_level = 2
    s.known_mechanism = Evidence(BIKE_MECH, REASONED, 2)   # mechanism present, no problem source
    s2 = assemble_deliverable(s)["section_2_invention_summary"]
    assert s2["known_problem"] is None
    assert s2["known_problem_note"] == "Problem evidence has not yet been captured clearly."


def test_selection_is_provenance_not_keywords():
    # idea_summary has NONE of the words problem/because/mechanism/fit/need; the
    # PMF evidence has them. Provenance (idea_summary) must still win — proving
    # selection is not keyword-based.
    s = _bike_state(idea_summary="riders are struck from behind when they slow at night")
    pmf = s.get_gap(PROBLEM_MECHANISM_FIT)
    pmf.evidence[0] = Evidence("the problem is rear collisions because the mechanism fits the need", REASONED, 4)
    kp = assemble_deliverable(s)["section_2_invention_summary"]["known_problem"]["content"]
    assert kp == "riders are struck from behind when they slow at night"


def test_water_leak_backward_compatible():
    # _polluted_state has no idea_summary -> PMF problem evidence still used.
    s = _polluted_state()
    assert assemble_deliverable(s)["section_2_invention_summary"]["known_problem"]["content"] == PMF_PROBLEM


def test_problem_fix_does_not_change_experiment_ids_or_criteria():
    # idea_summary presence must not affect Prototype & Test Plan experiment IDs
    # (section_11 reads unknowns / AI evidence / known_mechanism, not the problem),
    # and a stored success criterion stays attached to its experiment_id.
    from engine.idea_state import SuccessCriterion, ASSUMPTION_INVENTORY
    def build(with_summary):
        s = IdeaState(idea_id="tl-fixed")
        s.domain_signal = "electronics_electrical"; s.maturity_level = 2; s.current_stage = 3
        if with_summary:
            s.idea_summary = CYCLIST_PROBLEM
        s.acknowledged_unknowns.append(AcknowledgedUnknown(
            iteration=5, gap_context=ASSUMPTION_INVENTORY,
            verbatim="the exact deceleration threshold for braking", category_basis="explicit"))
        g = Gap(gap_type=ASSUMPTION_INVENTORY, status=CLOSED, opened_at=0)
        g.evidence.append(Evidence("the accelerometer must distinguish braking from bumps", REASONED, 1))
        s.gaps.append(g)
        s.known_problem = Evidence(CYCLIST_PROBLEM, REASONED, 0)
        s.known_mechanism = Evidence(BIKE_MECH, REASONED, 0)
        return s
    ids_no = [it["experiment_id"] for it in assemble_deliverable(build(False))["section_11_prototype_test_plan"]["items"]]
    s_yes = build(True)
    items_yes = assemble_deliverable(s_yes)["section_11_prototype_test_plan"]["items"]
    ids_yes = [it["experiment_id"] for it in items_yes]
    assert ids_no == ids_yes                                  # ids unaffected by the problem fix
    # a stored criterion stays attached to the same id
    s_yes.success_criteria[ids_yes[0]] = SuccessCriterion("my target")
    after = assemble_deliverable(s_yes)["section_11_prototype_test_plan"]["items"]
    assert next(it for it in after if it["experiment_id"] == ids_yes[0])["success_criterion"] == "my target"


def test_unrelated_sections_unchanged_by_problem_fix():
    # Only section 2 (known_problem) and section 4 (functional REQ) derive from
    # the resolved problem; other sections must be identical with/without idea_summary.
    base = IdeaState(idea_id="tl-u")
    base.domain_signal = "electronics_electrical"; base.maturity_level = 2; base.current_stage = 3
    base.known_mechanism = Evidence(BIKE_MECH, REASONED, 0)
    pmf = Gap(gap_type=PROBLEM_MECHANISM_FIT, status=CLOSED, opened_at=3)
    pmf.evidence.append(Evidence(PMF_FIT_FIRST, REASONED, 4)); base.gaps.append(pmf)
    a = assemble_deliverable(base)
    base.idea_summary = CYCLIST_PROBLEM
    b = assemble_deliverable(base)
    for k in ("section_3_assessment_overview", "section_5_assumptions", "section_6_risks",
              "section_7_recommendations", "section_8_unresolved_items",
              "section_9_stage3_reasoning", "section_11_prototype_test_plan"):
        assert a[k] == b[k]
