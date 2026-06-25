"""
FDC-001 Prototype & Test Plan (section_11).

A bounded, deterministic deliverable-layer capability that reorganizes
already-captured evidence into at most three traceable PROPOSED experiments.
It must never invent specifications, thresholds, measurements, results,
feasibility, validation, certification, safety, or expert conclusions, and must
surface success criteria as owner-defined unless an explicit owner criterion was
captured.
"""
import os, sys, uuid, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.idea_state import (
    IdeaState, Gap, Evidence, AcknowledgedUnknown,
    OPEN, PARTIAL, CLOSED, ASSERTED, REASONED, DEMONSTRATED,
    MECHANISM_COMPLETENESS, PROBLEM_MECHANISM_FIT,
    ASSUMPTION_INVENTORY, EXPERTISE_GAP_AWARENESS,
)
from engine.deliverable_assembler import (
    assemble_deliverable, _experiment_id, _canonical_source,
)
import dataclasses
from web.app import app, SESSION_STORE

OWNER_CRITERION_REQUIRED = "Owner-defined criterion required."
# Synthesized (platform-authored) item fields — must never carry invented specs
# or feasibility/validation/etc. claims. Excludes source_basis / traceability /
# required_expertise_or_tools, which quote the inventor's own captured wording.
_SYNTH_FIELDS = ("experiment_title", "objective", "minimum_prototype",
                 "what_to_observe", "failure_or_revision_condition",
                 "expected_evidence_upgrade")


def _state():
    s = IdeaState(idea_id="pp-" + uuid.uuid4().hex[:8])
    s.domain = "electronics_electrical"; s.domain_signal = "electronics_electrical"
    s.maturity_level = 2; s.current_stage = 3
    return s


def _gap(s, gap_type, *evidence, status=CLOSED):
    g = Gap(gap_type=gap_type, status=status, opened_at=0)
    for c in evidence:
        g.evidence.append(Evidence(c, REASONED, 1))
    s.gaps.append(g)
    return g


def _unknown(s, verbatim, iteration=5):
    s.acknowledged_unknowns.append(
        AcknowledgedUnknown(iteration=iteration, gap_context=ASSUMPTION_INVENTORY,
                            verbatim=verbatim, category_basis="explicit"))


def _plan(s):
    return assemble_deliverable(s)["section_11_prototype_test_plan"]


# --- 1-3: each priority source generates a traceable experiment ---------------

def test_acknowledged_unknown_creates_traceable_experiment():
    s = _state(); _unknown(s, "I do not know whether moisture reaches the joint")
    items = _plan(s)["items"]
    assert len(items) == 1
    assert items[0]["traceability"]["source_type"] == "acknowledged_unknown"
    assert items[0]["traceability"]["content"] == "I do not know whether moisture reaches the joint"


def test_essential_assumption_creates_traceable_experiment():
    s = _state(); _gap(s, ASSUMPTION_INVENTORY, "The mechanism assumes water bridges the electrodes")
    items = _plan(s)["items"]
    assert len(items) == 1
    assert items[0]["traceability"]["source_type"] == "assumption_inventory_evidence"


def test_reasoned_not_demonstrated_creates_upgrade_experiment():
    s = _state()
    s.known_problem = Evidence("Leaks cause hidden damage", REASONED, 0)
    s.known_mechanism = Evidence("A sensor changes reading and the controller alarms", REASONED, 0)
    items = _plan(s)["items"]
    assert len(items) == 1
    assert items[0]["traceability"]["source_type"] == "reasoned_leading_claim"
    assert items[0]["expected_evidence_upgrade"] == "Reasoned -> Demonstrated."


# --- 4: EGA supplies expertise only when supported ----------------------------

def test_expertise_supplied_only_when_ega_evidence_present():
    s = _state(); _unknown(s, "unknown alpha")
    _gap(s, EXPERTISE_GAP_AWARENESS, "I would need analog sensor calibration expertise")
    item = _plan(s)["items"][0]
    assert item["required_expertise_or_tools"]
    assert "analog sensor calibration" in item["required_expertise_or_tools"]
    # without EGA evidence -> None
    s2 = _state(); _unknown(s2, "unknown beta")
    assert _plan(s2)["items"][0]["required_expertise_or_tools"] is None


# --- 5: nothing invented from absent evidence ---------------------------------

def test_absent_evidence_produces_no_experiment():
    s = _state()  # no unknowns, no Stage 3 evidence, no REASONED leading claim
    plan = _plan(s)
    assert plan["items"] == []
    assert plan["count"] == 0
    assert plan["empty_statement"]


# --- 6: at most three experiments ---------------------------------------------

def test_no_more_than_three_experiments():
    s = _state()
    # genuinely distinct uncertainties (non-overlapping vocabulary)
    for i, text in enumerate((
        "uncertainty about battery longevity across cold winter seasons",
        "uncertainty about wireless signal range through thick concrete walls",
        "uncertainty about enclosure waterproofing under sustained humidity",
        "uncertainty about firmware timing latency during rapid input bursts",
        "uncertainty about acoustic loudness audibility from another room",
    )):
        _unknown(s, text, iteration=i)
    assert _plan(s)["count"] == 3


# --- 7: overlapping evidence deduplicated -------------------------------------

def test_overlapping_evidence_deduplicated():
    # Best-effort LEXICAL dedup (not semantic): text-identical / highly
    # overlapping sources collapse to one, preserving the first-priority source.
    s = _state()
    same = "the leak must produce detectable surface moisture at the sensor location"
    _unknown(s, same)
    _gap(s, ASSUMPTION_INVENTORY, same)          # lexically identical source
    items = _plan(s)["items"]
    assert len(items) == 1                        # collapsed to one
    assert items[0]["traceability"]["source_type"] == "acknowledged_unknown"  # priority kept


def test_highly_overlapping_sources_deduplicated():
    # Near-identical (not byte-identical) sources collapse to one (best-effort).
    s = _state()
    _unknown(s, "the moisture sensor must detect surface water at the pipe joint reliably")
    _gap(s, ASSUMPTION_INVENTORY,
         "the moisture sensor must detect surface water at the pipe joint consistently")
    assert _plan(s)["count"] == 1


def test_distinct_assumptions_sharing_some_vocab_stay_separate():
    # Two sources share incidental vocabulary but test genuinely different
    # assumptions -> kept as separate experiments.
    s = _state()
    _unknown(s, "the device must keep working when the battery runs low overnight")
    _gap(s, ASSUMPTION_INVENTORY,
         "the device must detect a leak before the water spreads widely")
    items = _plan(s)["items"]
    assert len(items) == 2
    assert {i["traceability"]["source_type"] for i in items} == {
        "acknowledged_unknown", "assumption_inventory_evidence"}


# --- 8: deterministic source priority -----------------------------------------

def test_source_priority_is_deterministic():
    s = _state()
    _unknown(s, "first an entirely separate timing question about latency")
    _gap(s, ASSUMPTION_INVENTORY, "second a wholly different enclosure sealing assumption")
    s.known_problem = Evidence("third problem framing here", REASONED, 0)
    s.known_mechanism = Evidence("third a completely unrelated radio modulation claim", REASONED, 0)
    types = [i["traceability"]["source_type"] for i in _plan(s)["items"]]
    assert types == ["acknowledged_unknown", "assumption_inventory_evidence",
                     "reasoned_leading_claim"]


# --- 9: every experiment carries traceability ---------------------------------

def test_every_experiment_has_traceability():
    s = _state()
    _unknown(s, "timing latency unknown")
    _gap(s, ASSUMPTION_INVENTORY, "sealing assumption distinct here")
    for item in _plan(s)["items"]:
        tr = item["traceability"]
        assert tr["source_type"] and tr["source_ref"] and tr["content"]


# --- 10/11: success criterion handling ----------------------------------------

def test_missing_success_criterion_renders_owner_required():
    s = _state(); _unknown(s, "a plain unknown with no criterion stated")
    assert _plan(s)["items"][0]["success_criterion"] == OWNER_CRITERION_REQUIRED


def test_owner_provided_success_criterion_preserved_verbatim():
    s = _state()
    _unknown(s, "We are unsure about detection. Success criterion: the alarm "
                "triggers before visible pooling. Other notes follow.")
    crit = _plan(s)["items"][0]["success_criterion"]
    assert crit == "the alarm triggers before visible pooling."


# --- 12/13: truthfulness — no invented specs or claims ------------------------

def test_no_invented_numbers_in_synthesized_fields():
    s = _state()
    # source deliberately contains numbers; synthesized fields must not.
    _unknown(s, "battery at 3.3 volts and a 50 percent humidity threshold")
    for item in _plan(s)["items"]:
        for f in _SYNTH_FIELDS:
            assert not re.search(r"\d", item[f]), f"invented number in {f}: {item[f]!r}"


def test_no_feasibility_or_validation_claims_in_synthesized_fields():
    s = _state()
    _unknown(s, "an unknown about detection")
    _gap(s, ASSUMPTION_INVENTORY, "an assumption about sealing")
    s.known_problem = Evidence("problem", REASONED, 0)
    s.known_mechanism = Evidence("a mechanism claim", REASONED, 0)
    banned = ("validated", "proven", "feasible", "certified", "safe", "production-ready")
    for item in _plan(s)["items"]:
        for f in _SYNTH_FIELDS:
            low = item[f].lower()
            for w in banned:
                assert w not in low, f"banned claim {w!r} in {f}: {item[f]!r}"


# --- 14/15: backward compatibility --------------------------------------------

def test_stage2_only_state_backward_compatible():
    s = IdeaState(idea_id="s2-" + uuid.uuid4().hex[:8])
    s.domain_signal = "electronics_electrical"
    _gap(s, MECHANISM_COMPLETENESS, status=CLOSED)   # Stage 2 gap only, no evidence
    pkg = assemble_deliverable(s)
    assert "section_11_prototype_test_plan" in pkg
    assert pkg["section_11_prototype_test_plan"]["items"] == []


def test_stage3_and_next_steps_unchanged_by_plan():
    s = _state()
    _gap(s, PROBLEM_MECHANISM_FIT, "problem fit reasoning", status=CLOSED)
    _unknown(s, "a residual unknown")
    pkg = assemble_deliverable(s)
    # section 9 still surfaces the Stage 3 gap evidence
    s9 = pkg["section_9_stage3_reasoning"]
    assert s9["stage3_gap_count"] == 1
    assert s9["items"][0]["evidence"][0]["content"] == "problem fit reasoning"
    # section 10 still surfaces the acknowledged unknown as a next step
    s10 = pkg["section_10_recommended_next_steps"]
    assert any(i["basis"].startswith("acknowledged_unknown:") for i in s10["items"])


# --- 16/17: rendering ---------------------------------------------------------

def test_rendered_template_shows_prototype_plan():
    s = _state(); _unknown(s, "an unknown about early detection timing")
    _gap(s, EXPERTISE_GAP_AWARENESS, "would need waterproof enclosure design knowledge")
    sid = "pp-render-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": []}
    try:
        body = app.test_client().get(f"/session/{sid}/deliverable").get_data(as_text=True)
        assert "Prototype &amp; Test Plan" in body or "Prototype & Test Plan" in body
        assert "Proposed experiment" in body
        assert OWNER_CRITERION_REQUIRED in body
        # internal source enums must not leak into the rendered page
        assert "acknowledged_unknown" not in body
        assert "ASSUMPTION_INVENTORY" not in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_rendered_template_shows_empty_statement_when_appropriate():
    s = _state()   # no testable evidence
    sid = "pp-empty-" + uuid.uuid4().hex[:8]
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": []}
    try:
        body = app.test_client().get(f"/session/{sid}/deliverable").get_data(as_text=True)
        assert "No evidence-grounded prototype experiment can be proposed" in body
    finally:
        SESSION_STORE.pop(sid, None)


# ===========================================================================
# Stable, deterministic, source-derived experiment identifiers (section_11).
# id = exp_v1_<source_type>_<sha256(source_type + normalized source)[:16]>.
# Derived ONLY from source_type + normalized verbatim source content — never
# list position or synthesized display wording.
# ===========================================================================

from engine.idea_state import IdeaState as _IdeaState

# Journey-equivalent source contents (distinct vocabulary per idea).
_WL_UNKNOWN = "I do not know the exact moisture threshold that distinguishes a leak from ambient humidity"
_WL_ASSUMPTION = "surface moisture must reach the sensor electrodes for the mechanism to work"
_WL_MECH = "a moisture sensor changes capacitance and the controller then sounds an alarm"
_LK_UNKNOWN = "I do not know how many wrong attempts should trigger the lockout or how long it should last"
_LK_ASSUMPTION = "the stored code must stay secret and the solenoid bolt must hold against a push"
_LK_MECH = "a keypad enters a code and on a match the controller drives a solenoid bolt"


def _three_experiment_state(unknown, assumption, mech):
    s = _state()
    _unknown(s, unknown)
    _gap(s, ASSUMPTION_INVENTORY, assumption)
    s.known_problem = _ev_problem("a clear problem statement for this idea")
    s.known_mechanism = Evidence(mech, REASONED, 0)
    return s


def _ev_problem(text):
    # PMF evidence is the resolved-problem source; use a Stage-3 PMF gap so the
    # leading claim resolves and _overall_quality(state) == REASONED.
    return Evidence(text, REASONED, 0)


# 1 / 2 — every experiment has a versioned, namespaced, non-empty id ----------

def test_every_experiment_has_versioned_namespaced_id():
    s = _three_experiment_state(_WL_UNKNOWN, _WL_ASSUMPTION, _WL_MECH)
    items = _plan(s)["items"]
    assert items
    for it in items:
        eid = it["experiment_id"]
        assert eid and isinstance(eid, str)
        st = it["traceability"]["source_type"]
        assert eid.startswith(f"exp_v1_{st}_")
        # exact format: exp_v1_<source_type>_<32 lowercase hex chars> (128-bit)
        assert re.fullmatch(r"exp_v1_" + re.escape(st) + r"_[0-9a-f]{32}", eid)


def test_digest_is_32_lowercase_hex():
    eid = _experiment_id("acknowledged_unknown", "some normalized source content")
    digest = eid.rsplit("_", 1)[-1]
    assert len(digest) == 32
    assert re.fullmatch(r"[0-9a-f]{32}", digest)


# 3 — repeated assembly is stable ---------------------------------------------

def test_repeated_assembly_produces_identical_ids():
    s = _three_experiment_state(_WL_UNKNOWN, _WL_ASSUMPTION, _WL_MECH)
    a = [i["experiment_id"] for i in _plan(s)["items"]]
    b = [i["experiment_id"] for i in _plan(s)["items"]]
    assert a == b and len(a) == 3


# 4 / 5 — canonicalization (whitespace + documented casefold) -----------------

def test_whitespace_normalization_stability():
    base = "the   stored  code\tmust stay secret"
    spaced = "  the stored   code must stay  secret  "
    assert _experiment_id("acknowledged_unknown", base) == \
           _experiment_id("acknowledged_unknown", spaced)


def test_case_normalization_is_casefold():
    assert _canonical_source("ABC Def") == "abc def"
    assert _experiment_id("acknowledged_unknown", "Surface Moisture Reaches") == \
           _experiment_id("acknowledged_unknown", "surface moisture reaches")


# 6 / 7 — source_type and content both affect identity ------------------------

def test_same_content_different_source_type_differ():
    c = "identical source content across both"
    assert _experiment_id("acknowledged_unknown", c) != \
           _experiment_id("assumption_inventory_evidence", c)


def test_same_source_type_different_content_differ():
    assert _experiment_id("acknowledged_unknown", "content one here") != \
           _experiment_id("acknowledged_unknown", "content two here")


# 8 — id is independent of synthesized display wording ------------------------

def test_id_derived_only_from_source_not_display_wording():
    # The rendered id must equal the id recomputed from ONLY source_type+content,
    # proving the synthesized title/objective/observe/failure/upgrade are not
    # inputs to identity.
    s = _three_experiment_state(_WL_UNKNOWN, _WL_ASSUMPTION, _WL_MECH)
    for it in _plan(s)["items"]:
        recomputed = _experiment_id(it["traceability"]["source_type"],
                                    it["traceability"]["content"])
        assert it["experiment_id"] == recomputed


# 9 — ordering does not define identity ---------------------------------------

def test_experiment_order_does_not_change_ids():
    s1 = _state(); _unknown(s1, "alpha distinct uncertainty about timing")
    _gap(s1, ASSUMPTION_INVENTORY, "beta distinct assumption about sealing")
    # reversed declaration order of the same two sources in a fresh state
    s2 = _state()
    _gap(s2, ASSUMPTION_INVENTORY, "beta distinct assumption about sealing")
    _unknown(s2, "alpha distinct uncertainty about timing")
    id_map1 = {i["traceability"]["content"]: i["experiment_id"] for i in _plan(s1)["items"]}
    id_map2 = {i["traceability"]["content"]: i["experiment_id"] for i in _plan(s2)["items"]}
    assert id_map1 == id_map2  # same source -> same id regardless of position


# 10 — multiple ASSUMPTION_INVENTORY evidence items get distinct ids -----------

def test_multiple_assumption_evidence_get_distinct_ids():
    s = _state()
    _gap(s, ASSUMPTION_INVENTORY,
         "first assumption about battery longevity in cold weather",
         "second assumption about radio range through concrete walls")
    items = _plan(s)["items"]
    assert len(items) == 2
    ids = [i["experiment_id"] for i in items]
    assert len(set(ids)) == 2
    assert all(i.startswith("exp_v1_assumption_inventory_evidence_") for i in ids)


# 11 / 12 / 13 — both journeys: 3 unique ids each, disjoint across journeys ----

def test_water_leak_three_unique_ids():
    s = _three_experiment_state(_WL_UNKNOWN, _WL_ASSUMPTION, _WL_MECH)
    ids = [i["experiment_id"] for i in _plan(s)["items"]]
    assert len(ids) == 3 and len(set(ids)) == 3


def test_combination_lock_three_unique_ids():
    s = _three_experiment_state(_LK_UNKNOWN, _LK_ASSUMPTION, _LK_MECH)
    ids = [i["experiment_id"] for i in _plan(s)["items"]]
    assert len(ids) == 3 and len(set(ids)) == 3


def test_journey_ids_do_not_overlap_when_content_differs():
    a = {i["experiment_id"] for i in
         _plan(_three_experiment_state(_WL_UNKNOWN, _WL_ASSUMPTION, _WL_MECH))["items"]}
    b = {i["experiment_id"] for i in
         _plan(_three_experiment_state(_LK_UNKNOWN, _LK_ASSUMPTION, _LK_MECH))["items"]}
    assert a.isdisjoint(b)


# 14 / 15 — dedup, count, and plan content unchanged except additive id -------

def test_lexical_dedup_unchanged_with_ids():
    s = _state()
    same = "the leak must produce detectable surface moisture at the sensor location"
    _unknown(s, same)
    _gap(s, ASSUMPTION_INVENTORY, same)   # lexically identical -> collapses to one
    items = _plan(s)["items"]
    assert len(items) == 1
    assert items[0]["traceability"]["source_type"] == "acknowledged_unknown"


def test_plan_content_unchanged_except_additive_id():
    s = _three_experiment_state(_WL_UNKNOWN, _WL_ASSUMPTION, _WL_MECH)
    items = _plan(s)["items"]
    # every previously-specified field is still present and the only new key is id
    expected = {"experiment_title", "objective", "source_basis", "minimum_prototype",
                "what_to_observe", "success_criterion", "failure_or_revision_condition",
                "required_expertise_or_tools", "expected_evidence_upgrade",
                "traceability", "experiment_id",
                # added by the per-experiment success-criteria increment:
                "success_criterion_provenance", "success_criterion_status"}
    for it in items:
        assert set(it.keys()) == expected


# 16 — no state field / serialization behavior introduced ---------------------

def test_no_state_field_added_for_ids():
    # The stable-ID mechanism itself adds no state field: the id lives only on
    # the assembled plan item. (success_criteria is added separately by the
    # per-experiment success-criteria increment and is verified there.)
    field_names = {f.name for f in dataclasses.fields(_IdeaState)}
    assert "experiment_id" not in field_names
    s = _three_experiment_state(_WL_UNKNOWN, _WL_ASSUMPTION, _WL_MECH)
    assert not hasattr(s, "experiment_id")
