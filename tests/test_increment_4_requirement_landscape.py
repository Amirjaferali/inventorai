"""Increment 4 — Atomic Requirements & Criticality-Aware Risk Register — tests-first.

These are PLAIN pre-source failing tests (no xfail, no skip, no markers), authored
BEFORE any source, per the merged and binding governance:
  * docs/governance/INCREMENT_4_AUTHORITY_RULINGS.md   (C4-R1 .. C4-R13, merged)
  * docs/governance/INCREMENT_4_DESIGN.md              (D-1 .. D-7, merged)
  * docs/governance/INCREMENT_4_IMPLEMENTATION_CONTRACT.md
      (919 lines / SHA-256 7ee546673175f2222ca03adc3eb1d86846611b39e6e14e2f8da655dbd89851e8)

They assert ONLY behavior already frozen by those documents. Because the source is
not yet implemented (and is not authorized this turn), every test is EXPECTED to
fail/error by IMPLEMENTATION ABSENCE — the missing `engine.requirement_landscape`
module/function, or the missing additive deliverable section
`section_13_requirement_landscape`. No source or template is created or modified
here; this is the ONLY file created this turn.

Frozen minimum interface (the later source phase implements EXACTLY this; §4/§4.1):
  engine.requirement_landscape.derive_requirement_landscape(state) -> RequirementLandscape
    RequirementLandscape(requirements: tuple, risks: tuple)         # frozen, immutable
    DerivedRequirement(requirement_id, statement, primary_anchor,
        supporting_references: tuple, source_status, criticality,
        criticality_authority, criticality_rationale|None,
        resolving_action|None, linked_risk_ids: tuple)              # frozen
    ProvenanceAnchor(anchor_kind, anchor_reference, display_label)  # frozen
    SupportingReference(reference_kind, reference, display_label)   # frozen
    ResolvingAction(action_kind, statement, source_reference)       # frozen
    GroundedRisk(risk_id, linked_requirement_ids, consequence,
        grounding_references, authority, status, rationale)         # frozen
  engine.deliverable_assembler.assemble_deliverable(state) gains ONE additive key
    `section_13_requirement_landscape` (title "Requirement Landscape"); all other
    section_* keys and their values are unchanged.
"""
import os
import sys
import copy
import json
import importlib
import inspect

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import pytest

import engine.idea_state as idea_state
from engine.idea_state import (
    IdeaState, Gap,
    OPEN, PARTIAL, CLOSED, ACCEPTED_RISK,
    MECHANISM_COMPLETENESS, BOUNDARY_AMBIGUITY, PHYSICAL_FEASIBILITY,
    DISPOSITION_ANSWERED, DISPOSITION_EVIDENCE_REQUESTED,
    DISPOSITION_SPECIALIST_REQUESTED,
)
from engine.deliverable_assembler import assemble_deliverable

# --- Frozen contract vocabulary (assertions ABOUT the contract, not implementation) ---
ANCHOR_KINDS = {
    "assertion", "gap", "active_contradiction",
    "pending_evidence", "pending_specialist",
}
SOURCE_STATUS = {
    "assertion": "recorded",
    "active_contradiction": "active contradiction",
    "pending_evidence": "evidence pending",
    "pending_specialist": "specialist input pending",
    "gap_open": "open",
    "gap_partial": "partially addressed",
}
ACTION = {
    "assertion": ("validate_recorded_answer",
                  "Validate the recorded answer against the available evidence."),
    "active_contradiction": ("reconcile_recorded_contradiction",
                             "Reconcile the conflicting recorded answers "
                             "without assuming either is correct."),
    "pending_evidence": ("provide_requested_evidence",
                         "Provide the requested empirical evidence."),
    "pending_specialist": ("obtain_requested_specialist_input",
                           "Obtain the requested specialist input."),
    "gap": ("address_open_gap", None),   # statement = "Address the open gap: {label}."
}
CONTRADICTION_STATEMENT = "Resolve the active contradiction between the two recorded answers."
GAP_GLUE = "Address the open gap: "
CRITICALITY_UNDETERMINED = "UNDETERMINED"
CRITICALITY_AUTHORITY_SYSTEM = "system-derived"
SECTION_KEY = "section_13_requirement_landscape"
RAW_ENUM_TOKENS = (
    "MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "PHYSICAL_FEASIBILITY",
    "OWNER_STATED", "LEGACY_UNSPECIFIED", "evidence_requested",
    "specialist_requested",
)


# --- Import-indirection ONLY (lazy so each test fails individually by absence) ------
def _landscape(state):
    from engine.requirement_landscape import derive_requirement_landscape
    return derive_requirement_landscape(state)


def _types():
    import engine.requirement_landscape as rl
    return rl


# --- Repository-native fixtures (construction only; no product logic) ---------------
def _state():
    return IdeaState(idea_id="inc4-test")


def _answered(s, content, gap=MECHANISM_COMPLETENESS, it=1):
    return s.record_interaction(action=DISPOSITION_ANSWERED, content=content,
                                gap_context=gap, iteration=it)


def _evidence(s, content="bench measurement", gap=MECHANISM_COMPLETENESS, it=1):
    return s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content=content,
                                gap_context=gap, iteration=it)


def _specialist(s, content="ask EE", gap=MECHANISM_COMPLETENESS, it=1):
    return s.record_interaction(action=DISPOSITION_SPECIALIST_REQUESTED, content=content,
                                gap_context=gap, iteration=it)


def _add_gap(s, gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=1):
    s.gaps.append(Gap(gap_type=gap_type, status=status, opened_at=opened_at))
    return s


def _by_kind(lm, kind):
    return [r for r in lm.requirements if r.primary_anchor.anchor_kind == kind]


def _one(lm, kind):
    hits = _by_kind(lm, kind)
    assert len(hits) == 1, f"expected exactly one {kind} requirement, got {len(hits)}"
    return hits[0]


def _ids(lm):
    return [r.requirement_id for r in lm.requirements]


def _render_deliverable_html(state):
    """Render the real user-facing deliverable HTML. The lazy web import isolates
    any web dependency to the tests that call it and mirrors the Increment 3
    deliverable route; fails by implementation-absence when the additive
    "Requirement Landscape" section is not yet rendered."""
    from web.app import app as _flask_app, SESSION_STORE as _STORE
    sid = "inc4-deliv-" + str(id(state))
    _STORE[sid] = {"state": state}
    try:
        resp = _flask_app.test_client().get(f"/session/{sid}/deliverable")
        return resp.get_data(as_text=True)
    finally:
        _STORE.pop(sid, None)


# ==================================================================================
# A. Active-anchor derivation, one coarse requirement per anchor (§6.2, §6.4, §6.5)
# ==================================================================================
def test_single_answered_record_yields_one_assertion_requirement():
    s = _state(); r = _answered(s, "X is 5V")
    lm = _landscape(s)
    req = _one(lm, "assertion")
    assert req.requirement_id == f"req:assertion:{r.record_id}"
    assert req.primary_anchor.anchor_reference == r.record_id
    assert req.source_status == SOURCE_STATUS["assertion"]


def test_one_coarse_requirement_per_active_anchor_no_splitting():
    s = _state()
    _answered(s, "sentence one. sentence two. sentence three.")
    lm = _landscape(s)
    assert len(_by_kind(lm, "assertion")) == 1  # coarse; C4-R2 no fragment splitting


def test_evidence_request_maps_to_pending_evidence_anchor():
    s = _state(); r = _evidence(s)
    lm = _landscape(s)
    req = _one(lm, "pending_evidence")
    assert req.requirement_id == f"req:evidence:{r.record_id}"
    assert req.source_status == SOURCE_STATUS["pending_evidence"]


def test_specialist_request_maps_to_pending_specialist_anchor():
    s = _state(); r = _specialist(s)
    lm = _landscape(s)
    req = _one(lm, "pending_specialist")
    assert req.requirement_id == f"req:specialist:{r.record_id}"
    assert req.source_status == SOURCE_STATUS["pending_specialist"]


def test_open_gap_yields_one_gap_requirement():
    s = _state(); _add_gap(s, MECHANISM_COMPLETENESS, OPEN, 1)
    lm = _landscape(s)
    req = _one(lm, "gap")
    assert req.requirement_id == "req:gap:MECHANISM_COMPLETENESS"
    assert req.source_status == SOURCE_STATUS["gap_open"]


def test_partial_gap_source_status_partially_addressed():
    s = _state(); _add_gap(s, BOUNDARY_AMBIGUITY, PARTIAL, 1)
    lm = _landscape(s)
    req = _one(lm, "gap")
    assert req.source_status == SOURCE_STATUS["gap_partial"]


def test_closed_and_accepted_risk_gaps_are_not_emitted():
    s = _state()
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=1))
    s.gaps.append(Gap(gap_type=BOUNDARY_AMBIGUITY, status=ACCEPTED_RISK, opened_at=2))
    lm = _landscape(s)
    assert _by_kind(lm, "gap") == []


def test_maturity_is_not_a_primary_anchor_and_empty_state_is_empty():
    s = _state()  # fresh: maturity 0, no anchors
    lm = _landscape(s)
    assert lm.requirements == ()          # empty ONLY when no valid active anchor
    assert lm.risks == ()


def test_superseded_record_is_excluded_before_derivation():
    s = _state()
    a = _answered(s, "old answer")
    b = _answered(s, "new answer", it=2)
    s.mark_supersession(a.record_id, b.record_id)
    lm = _landscape(s)
    ids = _ids(lm)
    assert f"req:assertion:{b.record_id}" in ids
    assert f"req:assertion:{a.record_id}" not in ids


# ==================================================================================
# B. Deterministic order-independent identifiers (§6.7, §8.1, §8.6)
# ==================================================================================
def test_identifiers_are_input_order_independent():
    s = _state()
    _answered(s, "a", it=1); _evidence(s, "e", it=2); _add_gap(s, MECHANISM_COMPLETENESS, OPEN, 1)
    s2 = copy.deepcopy(s)
    s2.assertions.reverse()      # same records/record_ids, different list order
    s2.gaps.reverse()
    assert _landscape(s) == _landscape(s2)   # structural equality; no positional dependence


def test_repeated_derivation_is_stable():
    s = _state(); _answered(s, "a"); _evidence(s, "e", it=2)
    assert _landscape(s) == _landscape(s)


def test_no_identifier_depends_on_list_position():
    s = _state()
    r1 = _answered(s, "first", it=1)
    r2 = _answered(s, "second", it=2)
    lm = _landscape(s)
    ids = _ids(lm)
    assert f"req:assertion:{r1.record_id}" in ids
    assert f"req:assertion:{r2.record_id}" in ids


# ==================================================================================
# C. Contradiction pair unit (§6.5, §6.6, §6.7 — F-2 / D-3)
# ==================================================================================
def test_contradiction_pair_yields_one_requirement_with_fixed_statement():
    s = _state()
    a = _answered(s, "X is 5V", it=1)
    b = _answered(s, "X is 12V", it=2)
    s.mark_contradiction(a.record_id, b.record_id)
    lm = _landscape(s)
    req = _one(lm, "active_contradiction")
    assert req.requirement_id == "req:contradiction:rec_1|rec_2"
    assert req.statement == CONTRADICTION_STATEMENT
    assert req.source_status == SOURCE_STATUS["active_contradiction"]
    # the two contradicting records do NOT also produce assertion requirements
    assert _by_kind(lm, "assertion") == []


def test_contradiction_pair_identifier_is_order_normalized_and_symmetric():
    s1 = _state()
    a = _answered(s1, "5V", it=1); b = _answered(s1, "12V", it=2)
    s1.mark_contradiction(a.record_id, b.record_id)
    s2 = _state()
    c = _answered(s2, "5V", it=1); d = _answered(s2, "12V", it=2)
    s2.mark_contradiction(d.record_id, c.record_id)   # reversed edge direction
    assert _one(_landscape(s1), "active_contradiction").requirement_id == \
           _one(_landscape(s2), "active_contradiction").requirement_id == \
           "req:contradiction:rec_1|rec_2"


def test_multiple_pairs_do_not_collapse_into_a_component():
    s = _state()
    a = _answered(s, "A", it=1); b = _answered(s, "B", it=2); c = _answered(s, "C", it=3)
    s.mark_contradiction(a.record_id, b.record_id)   # (rec_1, rec_2)
    s.mark_contradiction(b.record_id, c.record_id)   # (rec_2, rec_3)
    lm = _landscape(s)
    ids = set(r.requirement_id for r in _by_kind(lm, "active_contradiction"))
    assert ids == {"req:contradiction:rec_1|rec_2", "req:contradiction:rec_2|rec_3"}


def test_contradiction_with_inactive_partner_produces_no_pair_valid_anchors_render():
    s = _state()
    a = _answered(s, "5V", it=1)
    b = _answered(s, "12V", it=2)
    s.mark_contradiction(a.record_id, b.record_id)
    c = _answered(s, "replacement", it=3)
    s.mark_supersession(b.record_id, c.record_id)     # partner b now inactive
    lm = _landscape(s)
    assert _by_kind(lm, "active_contradiction") == []          # no pair for malformed edge
    ids = _ids(lm)
    assert f"req:assertion:{a.record_id}" in ids               # valid anchors continue
    assert f"req:assertion:{c.record_id}" in ids
    assert f"req:assertion:{b.record_id}" not in ids           # inactive excluded


# ==================================================================================
# D. Duplicate-gap reconciliation (§6.7 — F-1 / R-3)
# ==================================================================================
def test_duplicate_same_type_gaps_collapse_to_one_anchor_open_over_partial():
    s = _state()
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=PARTIAL, opened_at=5))
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=2))
    lm = _landscape(s)
    req = _one(lm, "gap")                                  # exactly one anchor per gap_type
    assert req.requirement_id == "req:gap:MECHANISM_COMPLETENESS"
    assert req.source_status == SOURCE_STATUS["gap_open"]  # any OPEN -> "open"


def test_duplicate_gap_reconciliation_has_no_list_position_dependence():
    s = _state()
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=PARTIAL, opened_at=5))
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=2))
    s2 = copy.deepcopy(s); s2.gaps.reverse()
    assert _landscape(s) == _landscape(s2)


# ==================================================================================
# E. Provenance and supporting references (§7.1, §7.2, §8.4)
# ==================================================================================
def test_every_requirement_has_exactly_one_provenance_anchor_in_vocabulary():
    s = _state(); _answered(s, "a"); _evidence(s, "e", it=2); _add_gap(s)
    lm = _landscape(s)
    assert lm.requirements  # non-empty
    for r in lm.requirements:
        assert r.primary_anchor is not None
        assert r.primary_anchor.anchor_kind in ANCHOR_KINDS


def test_supporting_references_are_deduped_and_lexically_sorted_tuples():
    s = _state(); _answered(s, "a"); _add_gap(s)
    for r in _landscape(s).requirements:
        refs = r.supporting_references
        assert isinstance(refs, tuple)
        keys = [(x.reference_kind, x.reference) for x in refs]
        assert keys == sorted(keys)                 # lexical order (§8.4)
        assert len(keys) == len(set(keys))          # deduplicated (§7.2)


# ==================================================================================
# F. Deterministic ordering across anchor kinds (§8.2, §8.3)
# ==================================================================================
def test_anchor_kind_display_precedence_order():
    s = _state()
    _add_gap(s, MECHANISM_COMPLETENESS, OPEN, 1)                   # gap (4)
    _answered(s, "plain", it=5)                                   # assertion (3)
    _specialist(s, gap=BOUNDARY_AMBIGUITY, it=4)                  # pending_specialist (2)
    _evidence(s, gap=PHYSICAL_FEASIBILITY, it=3)                  # pending_evidence (1)
    x = _answered(s, "5V", it=1); y = _answered(s, "12V", it=2)
    s.mark_contradiction(x.record_id, y.record_id)               # active_contradiction (0)
    kinds = [r.primary_anchor.anchor_kind for r in _landscape(s).requirements]
    order = ["active_contradiction", "pending_evidence", "pending_specialist",
             "assertion", "gap"]
    positions = [order.index(k) for k in kinds]
    assert positions == sorted(positions)     # non-decreasing precedence; no interleave


# ==================================================================================
# G. Criticality (§9.7 — all UNDETERMINED / system-derived in MVP-1)
# ==================================================================================
def test_all_criticality_is_undetermined_system_derived_with_no_rationale():
    s = _state(); _answered(s, "a"); _evidence(s, "e", it=2); _add_gap(s)
    for r in _landscape(s).requirements:
        assert r.criticality == CRITICALITY_UNDETERMINED
        assert r.criticality_authority == CRITICALITY_AUTHORITY_SYSTEM
        assert r.criticality_rationale is None       # None for UNDETERMINED (§9.7.7)


def test_no_numeric_criticality_score_field_leaks():
    s = _state(); _answered(s, "a")
    r = _one(_landscape(s), "assertion")
    assert not isinstance(r.criticality, (int, float))   # category string, never a score


# ==================================================================================
# H. Risk and zero-risk truthfulness (§9.8)
# ==================================================================================
def test_zero_grounded_risks_in_mvp_and_empty_linked_risk_ids():
    s = _state(); _answered(s, "a"); _add_gap(s); _evidence(s, "e", it=2)
    lm = _landscape(s)
    assert lm.risks == ()                                 # zero grounded risks (§9.8.2)
    for r in lm.requirements:
        assert r.linked_risk_ids == ()                    # no auto-risk (§9.8.1)


def test_unmet_or_undetermined_requirement_creates_no_generic_risk():
    s = _state(); _add_gap(s, MECHANISM_COMPLETENESS, OPEN, 1)   # open/unmet gap
    assert _landscape(s).risks == ()                            # no restatement-risk


# ==================================================================================
# I. Resolving-action vocabulary and exact statements (§9.9.2 — R-5 / FF-2)
# ==================================================================================
def test_assertion_resolving_action_exact():
    s = _state(); _answered(s, "a")
    act = _one(_landscape(s), "assertion").resolving_action
    assert (act.action_kind, act.statement) == ACTION["assertion"]


def test_pending_evidence_and_specialist_resolving_actions_exact():
    s = _state(); _evidence(s)
    assert (lambda a: (a.action_kind, a.statement))(
        _one(_landscape(s), "pending_evidence").resolving_action) == ACTION["pending_evidence"]
    s2 = _state(); _specialist(s2)
    a2 = _one(_landscape(s2), "pending_specialist").resolving_action
    assert (a2.action_kind, a2.statement) == ACTION["pending_specialist"]


def test_contradiction_resolving_action_exact():
    s = _state()
    a = _answered(s, "5V", it=1); b = _answered(s, "12V", it=2)
    s.mark_contradiction(a.record_id, b.record_id)
    act = _one(_landscape(s), "active_contradiction").resolving_action
    assert (act.action_kind, act.statement) == ACTION["active_contradiction"]


def test_gap_resolving_action_uses_exact_frozen_template():
    s = _state(); _add_gap(s, MECHANISM_COMPLETENESS, OPEN, 1)
    act = _one(_landscape(s), "gap").resolving_action
    assert act.action_kind == "address_open_gap"
    assert act.statement == "Address the open gap: Mechanism Completeness."
    assert act.statement.startswith(GAP_GLUE)             # exact glue text
    assert act.statement.endswith(".") and act.statement.count(".") == 1  # one period
    assert "MECHANISM_COMPLETENESS" not in act.statement  # no raw gap_type token


# ==================================================================================
# J. Immutable / JSON-safe payloads (§4.1, §4.3, §9.12.3)
# ==================================================================================
def test_result_and_requirements_are_frozen_with_tuple_collections():
    s = _state(); _answered(s, "a")
    lm = _landscape(s)
    assert isinstance(lm.requirements, tuple)
    assert isinstance(lm.risks, tuple)
    with pytest.raises(AttributeError):
        lm.requirements = ()                      # frozen dataclass
    req = lm.requirements[0]
    assert isinstance(req.supporting_references, tuple)
    assert isinstance(req.linked_risk_ids, tuple)
    with pytest.raises(AttributeError):
        req.statement = "mutated"                 # frozen dataclass


def test_structural_equality_of_equal_states():
    s1 = _state(); _answered(s1, "a", it=1)
    s2 = _state(); _answered(s2, "a", it=1)
    assert _landscape(s1) == _landscape(s2)


# ==================================================================================
# K. Deliverable integration — additive section only (§9.10, §4.3)
# ==================================================================================
def test_deliverable_gains_section_13_and_preserves_prior_sections():
    s = _state(); _answered(s, "a")
    pkg = assemble_deliverable(s)
    assert SECTION_KEY in pkg                                   # additive (fails by absence)
    assert "section_12_next_development_step" in pkg            # Increment 3 preserved
    assert "section_4_requirements" in pkg or any(              # _s4 preserved
        k.startswith("section_4") for k in pkg)


def test_section_13_is_json_safe_plain_data():
    s = _state(); _answered(s, "a"); _add_gap(s)
    pkg = assemble_deliverable(s)
    assert SECTION_KEY in pkg
    json.dumps(pkg[SECTION_KEY])                                # plain dict/list/str only


def test_section_13_leaks_no_raw_enum_tokens():
    # §7.3 governs USER-FACING (rendered) output; the machine package / `_s12`
    # mirror may carry canonical identifiers (e.g. reference_id). Scan the rendered
    # deliverable HTML, not the package.
    s = _state(); _add_gap(s, MECHANISM_COMPLETENESS, OPEN, 1); _answered(s, "a")
    html = _render_deliverable_html(s)
    assert "Requirement Landscape" in html                     # additive section rendered (fails by absence)
    for tok in RAW_ENUM_TOKENS:
        assert tok not in html                                 # no raw enum in user-facing output (§7.3)


def test_section_13_zero_risk_wording_is_truthful():
    s = _state(); _answered(s, "a")
    pkg = assemble_deliverable(s)
    assert SECTION_KEY in pkg
    blob = json.dumps(pkg[SECTION_KEY])
    # §9.8.3: the truthful zero-risk disclaimer is REQUIRED and itself NEGATES the
    # words "risk-free"/"safe"/"verified"; a correct section presents it and never
    # AFFIRMS safety. An affirmative-only claim omits the negation phrase and so
    # fails the second assertion below.
    assert "No structurally grounded risks are recorded" in blob
    assert "not a statement that the idea is risk-free, safe, or verified" in blob


def test_section_13_defined_empty_state_when_no_active_anchor():
    s = _state()                                               # nothing actionable
    pkg = assemble_deliverable(s)
    assert SECTION_KEY in pkg                                  # section still present, empty-framed


# ==================================================================================
# L. Import guardrails (§5 — F-5)
# ==================================================================================
def test_module_imports_only_idea_state_among_project_modules():
    mod = importlib.import_module("engine.requirement_landscape")   # fails by absence
    src = inspect.getsource(mod)
    forbidden = (
        "idea_development_outputs", "deliverable_assembler", "scoring",
        "progression", "persistence", "session_store", "domain_rules",
        "domain_registry", "web.app", "flask", "ai_advisor",
    )
    for f in forbidden:
        assert f not in src, f"forbidden import reference: {f}"
    assert "engine.idea_state" in src or "from engine.idea_state" in src


# ==================================================================================
# M. Increment 3 / _s4 / _s6 / statelessness non-regression (§9.9.1, §6.1, §12)
# ==================================================================================
def test_derivation_does_not_mutate_state():
    s = _state(); _answered(s, "a"); _add_gap(s)
    before = copy.deepcopy(s)
    _landscape(s)
    assert s == before                                         # pure / read-only (§6.1)


def test_increment_3_selector_still_present_and_landscape_is_distinct():
    # Increment 3 selector remains callable and unchanged in identity...
    from engine.idea_development_outputs import derive_next_development_step
    s = _state(); _add_gap(s, MECHANISM_COMPLETENESS, OPEN, 1)
    step = derive_next_development_step(s)
    assert step is not None
    # ...and the Increment 4 landscape is a DISTINCT additional selector (fails by absence)
    types = _types()
    assert hasattr(types, "derive_requirement_landscape")
    assert types.derive_requirement_landscape is not derive_next_development_step
