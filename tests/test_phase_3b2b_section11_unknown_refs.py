"""Phase 3B-2b — Section 11 Prototype & Test Plan acknowledged-unknown de-dup.

The user-facing "Based on:" line for a Priority-1 acknowledged-unknown experiment
now references the unknown by its stable registry id ("See UNK-00N — Acknowledged
unknown") instead of re-copying the full verbatim, mirroring the Section 10
(Phase 3B-2a) treatment. This is presentation-only: the full verbatim is still the
identity/digest/dedup source (`_experiment_id`, `_plan_sig`, dedup, success-
criterion resolution unchanged) and is still carried in `traceability.content`,
and it stays fully visible in Section 5 / the unknown registry. Priority-2
(assumption-inventory) and Priority-3 (reasoned-claim) source_basis are unchanged.
Sections 10/13/14 are unchanged.
"""
import json, os, sys, uuid
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.idea_state import (
    IdeaState, Gap, Evidence, AcknowledgedUnknown,
    CLOSED, REASONED,
    ASSUMPTION_INVENTORY,
    DISPOSITION_PROVISIONAL_ASSUMPTION, OWNER_INPUT,
)
from engine.deliverable_assembler import (
    assemble_deliverable, _experiment_id, _canonical_source, _plan_sig,
)
from web.app import app, SESSION_STORE

UK1 = ("I do not know how long the backup battery must last during a multi-hour rural "
       "power loss without losing the temperature log.")
UK2 = ("I am unsure which wireless protocol stays reliable across metal-walled "
       "refrigerated trailers with weak cellular coverage.")
PROBLEM = ("Delivered meat spoils when the refrigerated compartment drifts out of its safe "
           "temperature band during transit and the driver is not warned in time.")
MECHANISM = ("A microcontroller reads several digital temperature sensors, logs each reading, "
             "and raises a wireless alert to the cabin when the band is exceeded.")

_FORBIDDEN = ["validated", "feasible", "certified", "patentable",
              "market-ready", "build-ready", "guaranteed"]

CANONICAL_SECTIONS = {
    "section_1_disclaimer", "section_2_invention_summary", "section_3_assessment_overview",
    "section_4_requirements", "section_5_assumptions", "section_6_risks",
    "section_7_recommendations", "section_8_unresolved_items", "section_9_stage3_reasoning",
    "section_10_recommended_next_steps", "section_11_prototype_test_plan",
    "section_12_next_development_step", "section_13_requirement_landscape",
    "section_14_validation_plan",
}


def _base():
    s = IdeaState(idea_id="p3b2b-" + uuid.uuid4().hex[:8])
    s.domain = "electronics_electrical"; s.domain_signal = "electronics_electrical"
    s.maturity_level = 2; s.current_stage = 3
    return s


def _unknown(s, verbatim, iteration=5):
    s.acknowledged_unknowns.append(
        AcknowledgedUnknown(iteration=iteration, gap_context=ASSUMPTION_INVENTORY,
                            verbatim=verbatim, category_basis="explicit"))


def _gap(s, gap_type, *evidence, status=CLOSED):
    g = Gap(gap_type=gap_type, status=status, opened_at=0)
    for c in evidence:
        g.evidence.append(Evidence(c, REASONED, 1))
    s.gaps.append(g)
    return g


def _two_unknowns():
    s = _base()
    s.idea_summary = PROBLEM
    s.known_problem = Evidence(PROBLEM, REASONED, 1)
    _unknown(s, UK1, iteration=2)
    _unknown(s, UK2, iteration=3)
    return s


def _plan(s):
    return assemble_deliverable(s)["section_11_prototype_test_plan"]


def _render(state):
    sid = "p3b2b-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        resp = app.test_client().get(f"/session/{sid}/deliverable")
        return resp.status_code, resp.get_data(as_text=True)
    finally:
        SESSION_STORE.pop(sid, None)


def _section11(body):
    i = body.find("<h3>Prototype &amp; Test Plan</h3>")
    j = body.find("<h3>Validation Plan</h3>", i)
    return body[i:(j if j > i else len(body))]


# --- 1: source_basis uses UNK references ------------------------------------

def test_source_basis_uses_unk_references_in_order():
    items = _plan(_two_unknowns())["items"]
    unk_items = [it for it in items if it["traceability"]["source_type"] == "acknowledged_unknown"]
    assert len(unk_items) == 2
    assert unk_items[0]["source_basis"] == "See UNK-001 — Acknowledged unknown"
    assert unk_items[1]["source_basis"] == "See UNK-002 — Acknowledged unknown"


def test_unk_reference_visible_in_rendered_section11():
    _, body = _render(_two_unknowns())
    sec = _section11(body)
    assert "See UNK-001 — Acknowledged unknown" in sec
    assert "See UNK-002 — Acknowledged unknown" in sec


# --- 2: full verbatim absent from the user-facing display -------------------

def test_full_verbatim_absent_from_source_basis_display():
    items = _plan(_two_unknowns())["items"]
    for it in items:
        if it["traceability"]["source_type"] == "acknowledged_unknown":
            assert UK1 not in it["source_basis"]
            assert UK2 not in it["source_basis"]
    # and absent from the rendered "Based on:" display region
    _, body = _render(_two_unknowns())
    sec = _section11(body)
    assert UK1 not in sec
    assert UK2 not in sec


# --- 3: full verbatim preserved in traceability.content ---------------------

def test_full_verbatim_retained_in_traceability_content():
    items = _plan(_two_unknowns())["items"]
    contents = {it["traceability"]["content"] for it in items
                if it["traceability"]["source_type"] == "acknowledged_unknown"}
    assert UK1 in contents
    assert UK2 in contents


# --- 4: full verbatim still available in the package (Section 5 / registry) --

def test_full_verbatim_available_in_section5_and_registry():
    pkg = assemble_deliverable(_two_unknowns())
    # unknown registry carries the full verbatim once
    reg_contents = {e["content"] for e in pkg["_session_meta"]["unknown_registry"]}
    assert UK1 in reg_contents and UK2 in reg_contents
    # Section 5 remains the primary visible full-text location
    s5 = json.dumps(pkg["section_5_assumptions"])
    assert UK1 in s5 and UK2 in s5


# --- 5: experiment_id derives from verbatim, not the display string ---------

def test_experiment_id_derived_from_verbatim_not_display():
    items = _plan(_two_unknowns())["items"]
    by_content = {it["traceability"]["content"]: it for it in items
                  if it["traceability"]["source_type"] == "acknowledged_unknown"}
    # id is exactly the source-derived digest of (source_type + normalized verbatim)
    assert by_content[UK1]["experiment_id"] == _experiment_id("acknowledged_unknown", UK1)
    assert by_content[UK2]["experiment_id"] == _experiment_id("acknowledged_unknown", UK2)
    # id does NOT encode the display wording / UNK label
    for it in by_content.values():
        assert "UNK-" not in it["experiment_id"]
        assert "Acknowledged unknown" not in it["experiment_id"]


def test_experiment_id_unchanged_by_this_phase():
    # The id must be stable against the presentation change: recomputing it from
    # the canonical verbatim source (the pre-3B-2b identity input) still matches.
    items = _plan(_two_unknowns())["items"]
    for it in items:
        if it["traceability"]["source_type"] == "acknowledged_unknown":
            src = it["traceability"]["content"]
            assert it["experiment_id"] == _experiment_id("acknowledged_unknown", src)
            # canonicalization of the verbatim (not the display) drives the digest
            assert _canonical_source(src) == _canonical_source(it["traceability"]["content"])


# --- 6: dedup still keyed on the verbatim source, not the display -----------

def test_distinct_unknowns_stay_separate():
    # two lexically distinct unknowns -> two experiments (dedup unaffected)
    assert _plan(_two_unknowns())["count"] == 2


def test_overlapping_unknowns_still_dedup_on_verbatim():
    # Near-identical verbatim sources still collapse to one even though their
    # display strings ("See UNK-001" vs "See UNK-002") differ — proving dedup
    # keys on the verbatim source_text, not source_basis.
    s = _base()
    _unknown(s, "the moisture sensor must detect surface water at the pipe joint reliably")
    _unknown(s, "the moisture sensor must detect surface water at the pipe joint consistently")
    assert _plan(s)["count"] == 1


def test_plan_sig_keys_on_verbatim():
    # sanity: the dedup signature is a function of the verbatim, independent of
    # the new display string.
    assert _plan_sig(UK1) == _plan_sig(UK1)
    assert _plan_sig(UK1) != _plan_sig(UK2)


# --- 7: cap behavior unchanged ----------------------------------------------

def test_cap_still_three_experiments():
    s = _base()
    for i, text in enumerate((
        "uncertainty about battery longevity across cold winter seasons",
        "uncertainty about wireless signal range through thick concrete walls",
        "uncertainty about enclosure waterproofing under sustained humidity",
        "uncertainty about firmware timing latency during rapid input bursts",
        "uncertainty about acoustic loudness audibility from another room",
    )):
        _unknown(s, text, iteration=i)
    assert _plan(s)["count"] == 3
    # every surviving unknown item uses a UNK reference
    for it in _plan(s)["items"]:
        if it["traceability"]["source_type"] == "acknowledged_unknown":
            assert it["source_basis"].startswith("See UNK-")


# --- 8: Priority 2 / Priority 3 source_basis unchanged ----------------------

def test_priority2_assumption_source_basis_unchanged():
    s = _base()
    _gap(s, ASSUMPTION_INVENTORY, "The mechanism assumes water bridges the electrodes")
    items = _plan(s)["items"]
    ai = [it for it in items if it["traceability"]["source_type"] == "assumption_inventory_evidence"]
    assert len(ai) == 1
    assert ai[0]["source_basis"] == 'Assumption Inventory evidence: "The mechanism assumes water bridges the electrodes"'


def test_priority3_reasoned_claim_source_basis_unchanged():
    s = _base()
    s.known_problem = Evidence("Leaks cause hidden damage", REASONED, 0)
    s.known_mechanism = Evidence("A sensor changes reading and the controller alarms", REASONED, 0)
    items = _plan(s)["items"]
    rc = [it for it in items if it["traceability"]["source_type"] == "reasoned_leading_claim"]
    assert len(rc) == 1
    assert rc[0]["source_basis"] == 'Leading claim at Reasoned quality: "A sensor changes reading and the controller alarms"'


# --- 9: Section 10 unchanged (still concise UNK references) ------------------

def test_section10_still_uses_unk_references():
    pkg = assemble_deliverable(_two_unknowns())
    s10 = json.dumps(pkg["section_10_recommended_next_steps"], ensure_ascii=False)
    assert "See UNK-001 — Acknowledged unknown" in s10
    assert "See UNK-002 — Acknowledged unknown" in s10
    assert UK1 not in s10 and UK2 not in s10


# --- 10/11: Section 13 and Section 14 collapse intact ------------------------

def _recorded_answers_state(n=5):
    s = _base()
    for k in range(n):
        s.record_interaction(DISPOSITION_PROVISIONAL_ASSUMPTION, iteration=0,
                             content=f"distinct recorded answer number {k}",
                             responsibility=OWNER_INPUT)
    return s


def test_section13_collapse_still_intact():
    _, body = _render(_recorded_answers_state(5))
    i = body.find("<h3>Requirement Landscape</h3>")
    j = body.find("What is assumed", i)
    sec13 = body[i:(j if j > i else len(body))]
    assert sec13.count("<strong>Provenance:</strong>") == 1
    assert "(shared by 5 entries)" in sec13
    assert "Criticality:</strong> Not yet determined (assigned automatically by the system; not yet reviewed)" in sec13


def test_section14_collapse_still_intact():
    _, body = _render(_recorded_answers_state(5))
    i = body.find("<h3>Validation Plan</h3>")
    sec14 = body[i:]
    assert "(applies to 5 recorded answers)" in sec14


# --- 12: no forbidden wording introduced ------------------------------------

def test_no_forbidden_wording_in_section11():
    # Scan only the experiment/display region this change could affect, not the
    # pre-existing advisory note ("nothing here has been built, tested,
    # demonstrated, validated, certified, or shown feasible.") which legitimately
    # negates those words and is unchanged by this phase.
    _, body = _render(_two_unknowns())
    sec = _section11(body)
    cut = sec.find("Proposed experiments synthesized")   # start of the advisory note
    scanned = (sec[:cut] if cut >= 0 else sec).lower()
    for w in _FORBIDDEN:
        assert w not in scanned, f"forbidden wording in Section 11 body: {w!r}"


# --- 13: 14-section contract intact -----------------------------------------

def test_fourteen_section_contract_intact():
    pkg = assemble_deliverable(_two_unknowns())
    assert {k for k in pkg if k.startswith("section_")} == CANONICAL_SECTIONS
    assert len([k for k in pkg if k.startswith("section_")]) == 14
