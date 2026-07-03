"""Increment 5 — Concrete Validation-Plan Generation — tests-first.

PLAIN pre-source failing tests (no xfail, no skip, no markers), authored BEFORE any
source and BEFORE the additive `section_14_validation_plan` / `Validation Plan`
template section exist, per the merged and binding governance:
  * docs/governance/INCREMENT_5_DESIGN.md
  * docs/governance/INCREMENT_5_IMPLEMENTATION_CONTRACT.md
      (882 lines / SHA-256
       e103eab13b8ddd07bef41895dc8eea2d48bab7c047bc0fbb46ba3df55f7d7a64)

They assert ONLY behavior already frozen by that contract. Because the Increment 5
source is not yet implemented (and is NOT authorized by this turn), every test is
EXPECTED to FAIL by IMPLEMENTATION ABSENCE — the missing `engine.validation_plan`
module/function, or the missing additive deliverable section
`section_14_validation_plan` / rendered `Validation Plan` section. No production
source or template is created or modified here; this is the ONLY file created.

Lazy-import discipline (Increment 3/4 precedent): module-level imports reference
only committed, existing modules. `engine.validation_plan` is imported INSIDE test
functions/helpers so collection succeeds and each test fails at call time for the
absent implementation rather than at collection.

Frozen minimum interface the later source phase implements EXACTLY (§4–§16):
  engine.validation_plan.derive_validation_plan(state) -> ValidationPlan
    ValidationPlan(outcome: str, steps: tuple, blocked_items: tuple)      # frozen
    ValidationStep(step_id, statement, responsibility, evidence_category,
        closure_condition, provenance, confidence)                       # frozen
    BlockedValidationItem(item_id, reason, missing, responsibility,
        provenance)                                                      # frozen
    ProvenanceRef(anchor_kind, reference, display_label)                 # frozen
  engine.deliverable_assembler.assemble_deliverable(state) gains ONE additive key
    `section_14_validation_plan` built by `_s14(state)`; all other section_* keys
    and their values are unchanged.
  web/templates/deliverable.html gains ONE additive `Validation Plan` section.
The Increment 5 module imports, among project modules, ONLY `engine.idea_state`
and `engine.requirement_landscape`, and monkeypatches its import-site symbol
`engine.validation_plan.derive_requirement_landscape` as the authorized §19 seam.
"""
import os
import sys
import ast
import copy
import json
import importlib
import inspect

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import pytest

import engine.idea_state as idea_state
from engine.idea_state import (
    IdeaState, Gap,
    OPEN,
    PHYSICAL_FEASIBILITY,
    OWNER_STATED, LEGACY_UNSPECIFIED,
    OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED,
    DISPOSITION_ANSWERED, DISPOSITION_UNKNOWN, DISPOSITION_DEFERRED,
    DISPOSITION_PROVISIONAL_ASSUMPTION,
    DISPOSITION_EVIDENCE_REQUESTED, DISPOSITION_SPECIALIST_REQUESTED,
)
from engine.requirement_landscape import (
    derive_requirement_landscape,
    RequirementLandscape, DerivedRequirement, ProvenanceAnchor, ResolvingAction,
)
from engine.deliverable_assembler import (
    assemble_deliverable, _s4, _s6, _s12, _s13,
)

# --- Frozen ValidationStep responsibility vocabulary (contract §7; five, exactly)
OWNER_EXECUTABLE            = "OWNER_EXECUTABLE"
SYSTEM_DERIVABLE           = "SYSTEM_DERIVABLE"
SPECIALIST_REQUIRED        = "SPECIALIST_REQUIRED"
EMPIRICAL_EVIDENCE_REQUIRED = "EMPIRICAL_EVIDENCE_REQUIRED"
FIVE_RESPONSIBILITY_CLASSES = frozenset({
    OWNER_EXECUTABLE, SYSTEM_DERIVABLE, SPECIALIST_REQUIRED,
    EMPIRICAL_EVIDENCE_REQUIRED, UNDETERMINED,
})
# Ledger-vocabulary tokens that MUST NEVER appear as a ValidationStep responsibility
LEDGER_TOKENS = {OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE}
OUTCOMES = {"PLAN", "EMPTY", "BLOCKED"}


# ================================================================================
# Lazy seam to the not-yet-existing Increment 5 module (fails by absence pre-source)
# ================================================================================
def _derive(state):
    """Import-site call into the Increment 5 engine. Lazy so collection succeeds
    and the test fails at call time for the absent module."""
    from engine.validation_plan import derive_validation_plan
    return derive_validation_plan(state)


def _render_deliverable_html(state):
    """Render the real user-facing deliverable HTML through the committed web route
    (Increment 4 precedent). Fails by implementation-absence while the additive
    `Validation Plan` section is not yet rendered. Lazy web import isolates the
    dependency to the render tests only."""
    from web.app import app as _flask_app, SESSION_STORE as _STORE
    sid = "inc5-deliv-" + str(id(state))
    _STORE[sid] = {"state": state}
    try:
        resp = _flask_app.test_client().get(f"/session/{sid}/deliverable")
        return resp.get_data(as_text=True)
    finally:
        _STORE.pop(sid, None)


# --- State builders (committed API only) ----------------------------------------
def _state():
    return IdeaState(idea_id="inc5-test")


def _record(s, action, **kw):
    return s.record_interaction(action, iteration=0, **kw)


def _step_by_reqid(plan, requirement_id):
    want = "vstep:" + requirement_id
    for st in plan.steps:
        if st.step_id == want:
            return st
    raise AssertionError(f"no step for {requirement_id!r}; got {[s.step_id for s in plan.steps]}")


def _open_gaps(state):
    return [g for g in state.gaps if g.status == OPEN]


# ================================================================================
# Responsibility classification — one PARAMETERIZED function, 15 collected cases
# (contract §7 precedence, §7-T translation, §7-P provisional-assumption rule)
# ================================================================================
def _b_provisional_auto():
    s = _state(); r = _record(s, DISPOSITION_PROVISIONAL_ASSUMPTION, content="assume 5V rail")
    return s, f"req:assertion:{r.record_id}"

def _b_provisional_explicit_owner():
    s = _state(); r = _record(s, DISPOSITION_PROVISIONAL_ASSUMPTION, content="assume 5V rail",
                              responsibility=OWNER_INPUT)
    return s, f"req:assertion:{r.record_id}"

def _b_provisional_system():
    s = _state(); r = _record(s, DISPOSITION_PROVISIONAL_ASSUMPTION, content="derivable",
                              responsibility=SYSTEM_ANALYSIS)
    return s, f"req:assertion:{r.record_id}"

def _b_provisional_specialist():
    s = _state(); r = _record(s, DISPOSITION_PROVISIONAL_ASSUMPTION, content="needs specialist",
                              responsibility=SPECIALIST_INPUT)
    return s, f"req:assertion:{r.record_id}"

def _b_provisional_empirical():
    s = _state(); r = _record(s, DISPOSITION_PROVISIONAL_ASSUMPTION, content="needs measurement",
                              responsibility=EMPIRICAL_EVIDENCE)
    return s, f"req:assertion:{r.record_id}"

def _b_provisional_undetermined():
    s = _state(); r = _record(s, DISPOSITION_PROVISIONAL_ASSUMPTION, content="unclear",
                              responsibility=UNDETERMINED)
    return s, f"req:assertion:{r.record_id}"

def _b_answered_owner_stated():
    s = _state(); r = _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    return s, f"req:assertion:{r.record_id}"

def _b_unknown():
    s = _state(); r = _record(s, DISPOSITION_UNKNOWN, content="do not know")
    return s, f"req:assertion:{r.record_id}"

def _b_deferred():
    s = _state(); r = _record(s, DISPOSITION_DEFERRED, content="later")
    return s, f"req:assertion:{r.record_id}"

def _b_legacy_unspecified():
    # Deterministically isolate the §7 "LEGACY_UNSPECIFIED provenance (no other
    # affirmative signal)" fall-through. An `answered` record WOULD map to
    # OWNER_EXECUTABLE ONLY via owner-stated provenance; here provenance is forced
    # to LEGACY_UNSPECIFIED and no explicit responsibility is supplied, so the SOLE
    # operative signal is the legacy provenance → UNDETERMINED. The preconditions
    # below pin the isolation to current committed fields, so the case cannot pass
    # for an unrelated disposition-mapping reason if the mapping changes.
    s = _state()
    r = _record(s, DISPOSITION_ANSWERED, content="legacy answer",
                provenance=LEGACY_UNSPECIFIED)
    assert r.provenance == LEGACY_UNSPECIFIED      # not owner-stated
    assert r.provenance != OWNER_STATED            # so the answered→OWNER_EXECUTABLE row cannot apply
    assert r.responsibility is None                # no affirmative responsibility signal
    return s, f"req:assertion:{r.record_id}"

def _b_active_contradiction():
    s = _state()
    r1 = _record(s, DISPOSITION_ANSWERED, content="rail is 5V")
    r2 = _record(s, DISPOSITION_ANSWERED, content="rail is 12V")
    r2.contradicts = [r1.record_id]
    r1.contradicts = [r2.record_id]
    # Derive the expected requirement id from the committed Increment 4
    # normalization itself (NOT an ad-hoc re-sort): the landscape emits exactly one
    # active_contradiction requirement whose requirement_id carries the
    # order-normalized rec pair. Increment 5 reuses that same stable key.
    landscape = derive_requirement_landscape(s)
    contradiction_ids = [req.requirement_id for req in landscape.requirements
                         if req.primary_anchor.anchor_kind == "active_contradiction"]
    assert len(contradiction_ids) == 1
    return s, contradiction_ids[0]

def _b_pending_evidence():
    s = _state(); r = _record(s, DISPOSITION_EVIDENCE_REQUESTED, content="measure current")
    return s, f"req:evidence:{r.record_id}"

def _b_pending_specialist():
    s = _state(); r = _record(s, DISPOSITION_SPECIALIST_REQUESTED, content="ask EE")
    return s, f"req:specialist:{r.record_id}"

def _b_gap():
    s = _state(); s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=OPEN, opened_at=0))
    return s, f"req:gap:{PHYSICAL_FEASIBILITY}"

def _b_unrecognized_ledger_token():
    # a neutral (deferred) record carrying an unrecognized responsibility token:
    # precedence-1 does not resolve; the record falls through to UNDETERMINED.
    s = _state(); r = _record(s, DISPOSITION_DEFERRED, content="token test",
                              responsibility="NOT_A_REAL_TOKEN")
    return s, f"req:assertion:{r.record_id}"

RESPONSIBILITY_CASES = [
    ("provisional_auto_owner_input",       _b_provisional_auto,            UNDETERMINED),
    ("provisional_explicit_owner_input",   _b_provisional_explicit_owner,  UNDETERMINED),
    ("provisional_system_analysis",        _b_provisional_system,          SYSTEM_DERIVABLE),
    ("provisional_specialist_input",       _b_provisional_specialist,      SPECIALIST_REQUIRED),
    ("provisional_empirical_evidence",     _b_provisional_empirical,       EMPIRICAL_EVIDENCE_REQUIRED),
    ("provisional_undetermined",           _b_provisional_undetermined,    UNDETERMINED),
    ("answered_owner_stated",              _b_answered_owner_stated,       OWNER_EXECUTABLE),
    ("unknown",                            _b_unknown,                     UNDETERMINED),
    ("deferred",                           _b_deferred,                    UNDETERMINED),
    ("legacy_unspecified",                 _b_legacy_unspecified,          UNDETERMINED),
    ("active_contradiction",               _b_active_contradiction,        OWNER_EXECUTABLE),
    ("pending_evidence",                   _b_pending_evidence,            EMPIRICAL_EVIDENCE_REQUIRED),
    ("pending_specialist",                 _b_pending_specialist,          SPECIALIST_REQUIRED),
    ("gap",                                _b_gap,                         UNDETERMINED),
    ("unrecognized_ledger_token",          _b_unrecognized_ledger_token,   UNDETERMINED),
]

@pytest.mark.parametrize(
    "builder,expected",
    [(b, e) for _id, b, e in RESPONSIBILITY_CASES],
    ids=[_id for _id, _b, _e in RESPONSIBILITY_CASES],
)
def test_responsibility_classification(builder, expected):
    state, requirement_id = builder()
    plan = _derive(state)
    step = _step_by_reqid(plan, requirement_id)
    assert step.responsibility == expected
    # No ledger-vocabulary token ever leaks into the ValidationStep responsibility.
    assert step.responsibility not in LEDGER_TOKENS
    assert step.responsibility in FIVE_RESPONSIBILITY_CLASSES


# ================================================================================
# Evidence category — one PARAMETERIZED function, 5 collected cases (contract §7)
# ================================================================================
EVIDENCE_CATEGORY_CASES = [
    ("contradiction",     _b_active_contradiction, "reconciliation of conflicting records"),
    ("pending_evidence",  _b_pending_evidence,     "empirical evidence"),
    ("pending_specialist", _b_pending_specialist,  "specialist input"),
    ("answered",          _b_answered_owner_stated, "owner confirmation"),
    ("undetermined_gap",  _b_gap,                  "clarifying information"),
]

@pytest.mark.parametrize(
    "builder,expected",
    [(b, e) for _id, b, e in EVIDENCE_CATEGORY_CASES],
    ids=[_id for _id, _b, _e in EVIDENCE_CATEGORY_CASES],
)
def test_evidence_category(builder, expected):
    state, requirement_id = builder()
    plan = _derive(state)
    step = _step_by_reqid(plan, requirement_id)
    assert step.evidence_category == expected


# ================================================================================
# 35 single-case functions
# ================================================================================
def test_derive_is_pure_no_state_mutation():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    before = copy.deepcopy(s)
    _derive(s)
    assert s.assertions == before.assertions
    assert s.gaps == before.gaps
    assert s == before


def test_output_frozen_and_collections_are_tuples():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    plan = _derive(s)
    assert isinstance(plan.steps, tuple)
    assert isinstance(plan.blocked_items, tuple)
    with pytest.raises(Exception):
        plan.outcome = "MUTATED"          # frozen dataclass: setattr must raise
    with pytest.raises(Exception):
        plan.steps[0].responsibility = "X"


def test_step_id_prefix_and_non_positional():
    # Semantic position-independence proof: the SAME underlying requirement yields
    # the SAME step_id even when it is emitted at a DIFFERENT index. State A emits
    # the answered requirement first; state B pushes the SAME requirement (rec_1)
    # to a later index by adding evidence/specialist requests, which the Increment 4
    # landscape order sorts ahead of an assertion.
    a = _state(); ra = _record(a, DISPOSITION_ANSWERED, content="X is 5V")
    b = _state(); rb = _record(b, DISPOSITION_ANSWERED, content="X is 5V")
    _record(b, DISPOSITION_EVIDENCE_REQUESTED, content="measure")
    _record(b, DISPOSITION_SPECIALIST_REQUESTED, content="ask EE")
    assert ra.record_id == rb.record_id == "rec_1"        # same underlying record identity
    req_id = "req:assertion:rec_1"
    pa, pb = _derive(a), _derive(b)
    sa, sb = _step_by_reqid(pa, req_id), _step_by_reqid(pb, req_id)
    assert sa.step_id == "vstep:" + req_id                # stable Increment 4 key
    assert sa.step_id.startswith("vstep:")
    assert sb.step_id == sa.step_id                       # identical id across states
    assert pa.steps.index(sa) != pb.steps.index(sb)       # emitted at different indices


def test_blocked_item_id_prefix(monkeypatch):
    ineligible = _crafted_requirement("req:assertion:rec_9", resolving_action=None)
    _install_seam(monkeypatch, RequirementLandscape(requirements=(ineligible,), risks=()))
    plan = _derive(_state())
    assert len(plan.blocked_items) >= 1
    assert plan.blocked_items[0].item_id == "vblock:req:assertion:rec_9"
    assert plan.blocked_items[0].item_id.startswith("vblock:")


def test_plan_no_plan_id_structural_equality():
    s1 = _state(); _record(s1, DISPOSITION_ANSWERED, content="X is 5V")
    s2 = _state(); _record(s2, DISPOSITION_ANSWERED, content="X is 5V")
    p1, p2 = _derive(s1), _derive(s2)
    assert not hasattr(p1, "plan_id")
    assert p1 == p2                      # structural equality identifies the plan


def test_deduplication_unique_step_id():
    s = _state()
    _record(s, DISPOSITION_ANSWERED, content="a")
    _record(s, DISPOSITION_EVIDENCE_REQUESTED, content="b")
    _record(s, DISPOSITION_SPECIALIST_REQUESTED, content="c")
    plan = _derive(s)
    ids = [st.step_id for st in plan.steps]
    assert len(ids) == len(set(ids))


def test_ordering_follows_landscape_order():
    s = _state()
    r1 = _record(s, DISPOSITION_ANSWERED, content="rail is 5V")
    r2 = _record(s, DISPOSITION_ANSWERED, content="rail is 12V")
    r2.contradicts = [r1.record_id]; r1.contradicts = [r2.record_id]
    _record(s, DISPOSITION_EVIDENCE_REQUESTED, content="measure")
    _record(s, DISPOSITION_SPECIALIST_REQUESTED, content="ask EE")
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=OPEN, opened_at=0))
    landscape = derive_requirement_landscape(s)
    expected = ["vstep:" + req.requirement_id for req in landscape.requirements]
    plan = _derive(s)
    assert [st.step_id for st in plan.steps] == expected


def test_equivalent_state_order_independent():
    s1 = _state()
    _record(s1, DISPOSITION_ANSWERED, content="a")
    _record(s1, DISPOSITION_EVIDENCE_REQUESTED, content="b")
    _record(s1, DISPOSITION_SPECIALIST_REQUESTED, content="c")
    s2 = copy.deepcopy(s1)
    s2.assertions.reverse()              # same records, shuffled list position
    assert _derive(s1) == _derive(s2)


def test_repeated_run_stability():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    assert _derive(s) == _derive(s)


def test_ordering_is_severity_neutral():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    plan = _derive(s)
    for st in plan.steps:
        for banned in ("severity", "priority", "rank", "urgency", "criticality"):
            assert not hasattr(st, banned)


def test_supersession_and_active_set_excluded():
    s = _state()
    r1 = _record(s, DISPOSITION_ANSWERED, content="old")
    r2 = _record(s, DISPOSITION_ANSWERED, content="new")
    r1.superseded_by = r2.record_id
    plan = _derive(s)
    ids = [st.step_id for st in plan.steps]
    assert f"vstep:req:assertion:{r2.record_id}" in ids
    assert f"vstep:req:assertion:{r1.record_id}" not in ids


def test_confidence_undetermined_everywhere():
    s = _state()
    _record(s, DISPOSITION_ANSWERED, content="a")
    _record(s, DISPOSITION_EVIDENCE_REQUESTED, content="b")
    plan = _derive(s)
    assert plan.steps
    for st in plan.steps:
        assert st.confidence == UNDETERMINED


def test_no_result_supplied_passed_verified_fields():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    plan = _derive(s)
    st = plan.steps[0]
    for banned in ("result", "verdict", "validated", "supplied", "passed", "verified"):
        assert not hasattr(st, banned)
    blob = " ".join([st.statement, st.evidence_category, st.closure_condition]).lower()
    assert "supplied" not in blob
    assert "passed" not in blob
    assert "verified" not in blob


def test_closure_condition_required_not_supplied_wording():
    s = _state(); r = _record(s, DISPOSITION_EVIDENCE_REQUESTED, content="measure")
    plan = _derive(s)
    st = _step_by_reqid(plan, f"req:evidence:{r.record_id}")
    assert st.closure_condition == (
        f"Closed when {st.evidence_category} is provided and recorded; "
        "no such evidence is recorded yet."
    )


def test_provenance_present_on_every_step_and_blocked_item():
    s = _state()
    _record(s, DISPOSITION_ANSWERED, content="a")
    _record(s, DISPOSITION_EVIDENCE_REQUESTED, content="b")
    plan = _derive(s)
    assert plan.steps
    for st in plan.steps:
        assert st.provenance is not None
        assert st.provenance.anchor_kind
        assert st.provenance.reference
        assert st.provenance.display_label


def test_outcome_empty():
    plan = _derive(_state())
    assert plan.outcome == "EMPTY"
    assert plan.steps == ()
    assert plan.blocked_items == ()


def test_outcome_plan():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    plan = _derive(s)
    assert plan.outcome == "PLAN"
    assert len(plan.steps) >= 1


def test_outcome_blocked_via_seam(monkeypatch):
    ineligible = _crafted_requirement("req:assertion:rec_1", resolving_action=None)
    _install_seam(monkeypatch, RequirementLandscape(requirements=(ineligible,), risks=()))
    plan = _derive(_state())
    assert plan.outcome == "BLOCKED"
    assert plan.steps == ()
    assert len(plan.blocked_items) >= 1


def test_malformed_per_record_degrades_without_raising(monkeypatch):
    good = _crafted_requirement("req:assertion:rec_1")
    malformed = _crafted_requirement("req:assertion:rec_2", primary_anchor=None)
    _install_seam(monkeypatch, RequirementLandscape(requirements=(good, malformed), risks=()))
    plan = _derive(_state())                      # must not raise
    step_ids = [st.step_id for st in plan.steps]
    assert "vstep:req:assertion:rec_1" in step_ids
    assert plan.outcome == "PLAN"


def test_mixed_state_plan_with_blocked_items(monkeypatch):
    good = _crafted_requirement("req:assertion:rec_1")
    ineligible = _crafted_requirement("req:assertion:rec_2", resolving_action=None)
    _install_seam(monkeypatch, RequirementLandscape(requirements=(good, ineligible), risks=()))
    plan = _derive(_state())
    assert plan.outcome == "PLAN"
    assert len(plan.steps) >= 1
    assert len(plan.blocked_items) >= 1
    assert plan.outcome != "PARTIAL"


def test_section_14_key_present_and_additive():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    pkg = assemble_deliverable(s)
    assert "section_14_validation_plan" in pkg
    for prior in ("section_4_requirements", "section_6_risks",
                  "section_12_next_development_step", "section_13_requirement_landscape"):
        assert prior in pkg


def test_section_14_json_safe():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    pkg = assemble_deliverable(s)
    section = pkg["section_14_validation_plan"]
    assert json.loads(json.dumps(section)) == section


def test_section_14_both_arrays_preserved():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    section = assemble_deliverable(s)["section_14_validation_plan"]
    assert isinstance(section["steps"], list)
    assert isinstance(section["blocked_items"], list)


def test_section_14_empty_collections_are_lists_not_null():
    section = assemble_deliverable(_state())["section_14_validation_plan"]
    assert section["steps"] == []
    assert section["blocked_items"] == []
    assert section["steps"] is not None
    assert section["blocked_items"] is not None


def test_section_14_outcome_token_present():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    section = assemble_deliverable(s)["section_14_validation_plan"]
    assert section["outcome"] in OUTCOMES


def test_section_14_deterministic_ordering():
    s = _state()
    _record(s, DISPOSITION_ANSWERED, content="a")
    _record(s, DISPOSITION_EVIDENCE_REQUESTED, content="b")
    a = assemble_deliverable(s)["section_14_validation_plan"]["steps"]
    b = assemble_deliverable(s)["section_14_validation_plan"]["steps"]
    assert a == b


def test_rendered_no_raw_token_leak():
    s = _state()
    _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    _record(s, DISPOSITION_EVIDENCE_REQUESTED, content="measure current")
    html = _render_deliverable_html(s)
    assert "Validation Plan" in html                 # additive section rendered (fails by absence)
    for raw in ("vstep:", "vblock:", "req:assertion:", "req:evidence:",
                "active_contradiction", "pending_evidence", "OWNER_EXECUTABLE",
                "EMPIRICAL_EVIDENCE_REQUIRED"):
        assert raw not in html


def test_rendered_jinja_autoescape_preserved(monkeypatch):
    # Inject a UNIQUE unsafe marker ONLY through the Validation Plan payload via the
    # authorized §19 seam. The seam replaces derive_requirement_landscape at the
    # Increment 5 import site ONLY, so the marker reaches section_14 (Validation
    # Plan) alone; every legacy section uses the real (empty) landscape and cannot
    # contain it. Autoescape must render the marker escaped INSIDE the Validation
    # Plan section and never raw — an escaped value elsewhere cannot satisfy this.
    marker_raw = "<vp-xss-42>alert&\"'</vp-xss-42>"
    good = _crafted_requirement("req:assertion:rec_1", statement=marker_raw)
    _install_seam(monkeypatch, RequirementLandscape(requirements=(good,), risks=()))
    html = _render_deliverable_html(_state())
    assert "Validation Plan" in html                  # additive section rendered (fails by absence)
    section = html[html.find("Validation Plan"):]     # isolate the Validation Plan region
    assert "<vp-xss-42>" not in html                  # raw unsafe marker never leaks anywhere
    assert "<vp-xss-42>" not in section               # ... and specifically not in this section
    assert "&lt;vp-xss-42&gt;" in section             # escaped representation IS inside the section


def test_rendered_mixed_state_shows_both(monkeypatch):
    good = _crafted_requirement("req:assertion:rec_1", statement="Validate the recorded answer.")
    ineligible = _crafted_requirement("req:assertion:rec_2", resolving_action=None)
    _install_seam(monkeypatch, RequirementLandscape(requirements=(good, ineligible), risks=()))
    # Contract-anchored mixed state (§12/§16): the machine package losslessly carries
    # BOTH a non-empty `steps` array AND a non-empty `blocked_items` array under a
    # single `PLAN` outcome — a stable structural signal, not generic English words.
    section = assemble_deliverable(_state())["section_14_validation_plan"]
    assert section["outcome"] == "PLAN"
    assert len(section["steps"]) >= 1
    assert len(section["blocked_items"]) >= 1
    # The rendered mixed output shows the actionable step and leaks no raw identifier.
    html = _render_deliverable_html(_state())
    assert "Validation Plan" in html
    assert "Validate the recorded answer." in html   # the actionable step is rendered
    for raw in ("vstep:", "vblock:", "req:assertion:"):
        assert raw not in html


def test_rendered_non_claim_wording():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    html = _render_deliverable_html(s)
    assert "Validation Plan" in html                 # additive section rendered (fails by absence)
    low = html.lower()
    for banned in ("has been verified", "evidence supplied", "step passed",
                   "validation complete", "risk-free", "market-ready"):
        assert banned not in low


def test_import_boundary_only_two_project_modules():
    # AST-based (not spelling-based): accept ANY syntactically valid form that
    # imports only engine.idea_state and engine.requirement_landscape — including
    # `from engine import idea_state, requirement_landscape`, aliased imports,
    # parenthesized multi-line imports, `from engine.idea_state import X`, and
    # relative `from . import requirement_landscape`. Reject any other engine
    # submodule and any `web` import. Robust to comments/strings/whitespace.
    _ALLOWED = {"idea_state", "requirement_landscape"}
    mod = importlib.import_module("engine.validation_plan")
    tree = ast.parse(inspect.getsource(mod))
    offending = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                parts = alias.name.split(".")
                if parts[0] == "web":
                    offending.append(alias.name)
                elif parts[0] == "engine":
                    # bare `import engine` is too broad; a submodule must be allowed
                    if len(parts) < 2 or parts[1] not in _ALLOWED:
                        offending.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod_name = node.module or ""
            top = mod_name.split(".")[0] if mod_name else ""
            if top == "web":
                offending.append(mod_name)
            elif top == "engine":
                parts = mod_name.split(".")
                if len(parts) == 1:                       # from engine import X, Y
                    for alias in node.names:
                        if alias.name not in _ALLOWED:
                            offending.append(f"engine.{alias.name}")
                elif parts[1] not in _ALLOWED:            # from engine.<sub> import ...
                    offending.append(mod_name)
            elif node.level and node.level > 0:           # relative, i.e. within engine/
                if mod_name:                              # from .idea_state import X
                    if mod_name.split(".")[0] not in _ALLOWED:
                        offending.append("." + mod_name)
                else:                                     # from . import idea_state, ...
                    for alias in node.names:
                        if alias.name not in _ALLOWED:
                            offending.append("." + alias.name)
    assert offending == []


def test_increment_3_non_dependency():
    mod = importlib.import_module("engine.validation_plan")
    src = inspect.getsource(mod)
    assert "idea_development_outputs" not in src
    assert "derive_next_development_step" not in src


def test_no_domain_registry_dependency():
    mod = importlib.import_module("engine.validation_plan")
    src = inspect.getsource(mod)
    for banned in ("domain_registry", "domain_rules", "load_registry", "domains/"):
        assert banned not in src


def test_prior_sections_s4_s6_s12_s13_unchanged():
    s = _state(); _record(s, DISPOSITION_ANSWERED, content="X is 5V")
    pkg = assemble_deliverable(s)
    assert pkg["section_4_requirements"] == _s4(s)
    assert pkg["section_6_risks"] == _s6(s, _open_gaps(s))
    assert pkg["section_12_next_development_step"] == _s12(s)
    assert pkg["section_13_requirement_landscape"] == _s13(s)
    assert "section_14_validation_plan" in pkg       # additive-only (fails by absence)


def test_frozen_responsibility_vocabulary_exactly_five():
    observed = set()
    for _id, builder, _expected in RESPONSIBILITY_CASES:
        state, requirement_id = builder()
        step = _step_by_reqid(_derive(state), requirement_id)
        observed.add(step.responsibility)
        assert step.responsibility not in LEDGER_TOKENS
    assert observed == FIVE_RESPONSIBILITY_CLASSES    # all five, and only the five


# --- Seam helpers (authorized §19 import-site monkeypatch) -----------------------
def _crafted_requirement(requirement_id, resolving_action="__default__",
                         primary_anchor="__default__", statement="Validate the recorded answer."):
    """Build a committed Increment 4 DerivedRequirement for the test seam. Default
    is an ELIGIBLE assertion requirement; pass resolving_action=None for an
    ineligible (blocked) requirement, or primary_anchor=None for a malformed one."""
    if primary_anchor == "__default__":
        primary_anchor = ProvenanceAnchor(
            anchor_kind="assertion", anchor_reference=requirement_id.split(":")[-1],
            display_label="Recorded answer")
    if resolving_action == "__default__":
        resolving_action = ResolvingAction(
            action_kind="validate_recorded_answer", statement=statement,
            source_reference=requirement_id.split(":")[-1])
    return DerivedRequirement(
        requirement_id=requirement_id, statement=statement,
        primary_anchor=primary_anchor, supporting_references=(),
        source_status="recorded", criticality="UNDETERMINED",
        criticality_authority="system-derived", criticality_rationale=None,
        resolving_action=resolving_action, linked_risk_ids=())


def _install_seam(monkeypatch, landscape):
    """Monkeypatch the Increment 5 import-site symbol ONLY (fails by absence
    pre-source). Production behavior remains driven by the real derivation."""
    import engine.validation_plan as vp
    monkeypatch.setattr(vp, "derive_requirement_landscape", lambda state: landscape)
