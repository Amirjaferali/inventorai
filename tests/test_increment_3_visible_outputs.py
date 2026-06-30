"""Increment 3 — Visible Next Development Step — tests-first expected-failure package.

These tests are written BEFORE any source change (TESTS-FIRST-ONLY), per the merged
and binding governance documents:
  * docs/governance/INCREMENT_3_AUTHORITY_RULINGS.md  (R-1 through R-6, merged/binding)
  * docs/governance/INCREMENT_3_IMPLEMENTATION_CONTRACT.md
      (DRAFT — NOT AUTHORIZED FOR IMPLEMENTATION; the corrected SIX-PATH boundary
       is committed/merged/operative as a binding boundary).

Because the source is not yet implemented (and is not authorized this turn), the
behavioral tests below are EXPECTED to fail with implementation-absence errors
(a missing `engine.idea_development_outputs` module / function, a missing additive
deliverable section, or a missing session render context). They document the
required future behavior; they do NOT implement production logic.

Posited minimum public interface (the later source phase implements EXACTLY this
minimum; tests assert behavior, not internal class names beyond this minimum):

  engine.idea_development_outputs  (NEW pure module — six-path New #1):
    derive_next_development_step(state) -> payload | None
      * pure, deterministic, read-only; no persistence; no route/template knowledge.
      * returns ONE immutable payload for the single primary unresolved issue,
        OR None / a non-problem "ready" payload when nothing is actionable
        (verified-ready: do NOT invent a problem).
      * payload exposes at minimum these field-equivalents (attributes):
          issue_type, reference_id, title, why_it_matters, next_action,
          evidence_needed, suggested_provider, sufficiency_condition,
          unlock_condition, remaining_uncertainty
      * issue_type in ISSUE_TYPES (below).
      * suggested_provider in PROVIDER_VOCAB (below) or None (truthful absence).
      * the payload is immutable (frozen dataclass or equivalent).

  engine.deliverable_assembler.assemble_deliverable(state)  (six-path Modified #1):
    * gains ONE additive section key `section_12_next_development_step` consuming the
      SAME derivation; all existing section_* keys and their values are unchanged.

  web.app.show_session  (six-path Modified #2, bounded by R-5):
    * passes the SAME derived payload into the session render context so
      web/templates/session.html renders a compact callout; both surfaces resolve
      the SAME (issue_type, reference_id) (O-2). web/app.py routing/methods/state
      are otherwise unchanged.

This file is the ONLY path created this turn (six-path New #2). No source file is
created or modified; no template is modified; the frozen persistence worktree and
`web/responsibility_labels.py` are NOT imported or relied upon.
"""
import os
import sys
import copy
import inspect

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import pytest

import engine.idea_state as idea_state
from engine.idea_state import (
    IdeaState, Gap,
    OPEN, CLOSED,
    MECHANISM_COMPLETENESS, BOUNDARY_AMBIGUITY,
    OWNER_STATED, UNVALIDATED, INDEPENDENTLY_VERIFIED,
    OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED,
    DISPOSITION_ANSWERED, DISPOSITION_PROVISIONAL_ASSUMPTION,
    DISPOSITION_SPECIALIST_REQUESTED, DISPOSITION_EVIDENCE_REQUESTED,
)
from engine.deliverable_assembler import assemble_deliverable

# Real Flask app + in-memory session store (same surfaces used by Increment 2 tests).
from web.app import app as _flask_app, SESSION_STORE as _SESSION_STORE

# --- Posited contract vocabularies (the source phase must conform to these) -------
PROVIDER_VOCAB = {
    OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED,
}
ISSUE_TYPES = {
    "active_contradiction", "pending_evidence", "pending_specialist",
    "provisional_assumption", "owner_unvalidated", "open_gap", "maturity",
}
# Issue types that assert an unresolved *problem* (used to verify the verified-ready
# state never fabricates one).
PROBLEM_ISSUE_TYPES = ISSUE_TYPES
PAYLOAD_FIELDS = (
    "issue_type", "reference_id", "title", "why_it_matters", "next_action",
    "evidence_needed", "suggested_provider", "sufficiency_condition",
    "unlock_condition", "remaining_uncertainty",
)
ADDITIVE_SECTION_KEY = "section_12_next_development_step"


# --- Import-indirection only (NOT the selection algorithm) ------------------------
def _derive(state):
    """Lazily import and call the not-yet-implemented derivation so each test fails
    individually with a clear implementation-absence error (rather than a single
    collection error). Contains no selection logic."""
    from engine.idea_development_outputs import derive_next_development_step
    return derive_next_development_step(state)


# --- Repository-native, self-contained fixtures (construction only) ---------------
def _fresh_state():
    return IdeaState(idea_id="inc3-test")


def _state_with_open_gap(gap_type=MECHANISM_COMPLETENESS):
    s = _fresh_state()
    s.gaps.append(Gap(gap_type=gap_type, status=OPEN, opened_at=1))
    return s


def _snapshot(state):
    """Deep copy for mutation-safety comparison (IdeaState/AssertionRecord/Gap are
    dataclasses with structural equality)."""
    return copy.deepcopy(state)


def _render_html(path):
    return _flask_app.test_client().get(path)


def _render_session(state):
    sid = "inc3-sess-" + str(id(state))
    _SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        return _render_html(f"/session/{sid}")
    finally:
        _SESSION_STORE.pop(sid, None)


def _render_deliverable(state):
    sid = "inc3-deliv-" + str(id(state))
    _SESSION_STORE[sid] = {"state": state}
    try:
        return _render_html(f"/session/{sid}/deliverable")
    finally:
        _SESSION_STORE.pop(sid, None)


# =================================================================================
# A. Seven-level priority — each higher issue beats every lower one.
# =================================================================================
def test_priority_active_contradiction_beats_everything():
    s = _state_with_open_gap()
    a = s.record_interaction(action=DISPOSITION_ANSWERED, content="X is 5V",
                             gap_context=MECHANISM_COMPLETENESS, iteration=1)
    b = s.record_interaction(action=DISPOSITION_ANSWERED, content="X is 12V",
                             gap_context=MECHANISM_COMPLETENESS, iteration=2)
    s.mark_contradiction(a.record_id, b.record_id)
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="bench test",
                         gap_context=MECHANISM_COMPLETENESS, iteration=3)
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "active_contradiction"


def test_priority_pending_evidence_beats_specialist_provisional_gap_maturity():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_SPECIALIST_REQUESTED, content="ask EE",
                         gap_context=MECHANISM_COMPLETENESS, iteration=2)
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="measure",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "pending_evidence"


def test_priority_pending_specialist_beats_provisional_gap_maturity():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_PROVISIONAL_ASSUMPTION, content="assume Y",
                         gap_context=MECHANISM_COMPLETENESS, iteration=2)
    s.record_interaction(action=DISPOSITION_SPECIALIST_REQUESTED, content="ask EE",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "pending_specialist"


def test_priority_provisional_beats_owner_unvalidated_gap_maturity():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_ANSWERED, content="owner says Z",
                         gap_context=MECHANISM_COMPLETENESS, iteration=2)
    s.record_interaction(action=DISPOSITION_PROVISIONAL_ASSUMPTION, content="assume Y",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "provisional_assumption"


def test_priority_owner_unvalidated_beats_open_gap_and_maturity():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_ANSWERED, content="owner says Z",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "owner_unvalidated"


def test_priority_open_gap_beats_maturity():
    s = _state_with_open_gap()   # open gap, maturity 0, no assertions
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "open_gap"


def test_priority_maturity_is_final_fallback():
    s = _fresh_state()           # maturity 0 (<2), no gaps, no assertions
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "maturity"


# =================================================================================
# B. Inactive / superseded records are excluded before selection.
# =================================================================================
def test_superseded_record_is_excluded_from_selection():
    s = _state_with_open_gap()
    old = s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="old",
                               gap_context=MECHANISM_COMPLETENESS, iteration=1)
    new = s.record_interaction(action=DISPOSITION_ANSWERED, content="owner now answers",
                               gap_context=MECHANISM_COMPLETENESS, iteration=2)
    s.mark_supersession(old.record_id, new.record_id)
    payload = _derive(s)
    assert payload is not None
    # The superseded pending-evidence record is deactivated; the active set leaves
    # only the owner-unvalidated answer (and the open gap below it).
    assert payload.issue_type == "owner_unvalidated"
    assert payload.reference_id != old.record_id


def test_superseded_contradiction_endpoint_no_longer_blocks():
    s = _state_with_open_gap()
    a = s.record_interaction(action=DISPOSITION_ANSWERED, content="A",
                             gap_context=MECHANISM_COMPLETENESS, iteration=1)
    b = s.record_interaction(action=DISPOSITION_ANSWERED, content="B",
                             gap_context=MECHANISM_COMPLETENESS, iteration=2)
    s.mark_contradiction(a.record_id, b.record_id)
    c = s.record_interaction(action=DISPOSITION_ANSWERED, content="C resolves",
                             gap_context=MECHANISM_COMPLETENESS, iteration=3)
    s.mark_supersession(a.record_id, c.record_id)   # deactivate one endpoint
    payload = _derive(s)
    assert payload is not None
    # Contradiction no longer active (one endpoint superseded) -> not the primary.
    assert payload.issue_type != "active_contradiction"


# =================================================================================
# C. R-6 deterministic within-level tie-break.
# =================================================================================
def test_tiebreak_lowest_record_id_at_selected_level():
    s = _state_with_open_gap()
    first = s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="e1",
                                 gap_context=MECHANISM_COMPLETENESS, iteration=5)
    second = s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="e2",
                                  gap_context=BOUNDARY_AMBIGUITY, iteration=1)
    assert first.record_id == "rec_1" and second.record_id == "rec_2"
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "pending_evidence"
    # Lowest numeric rec_N wins regardless of iteration / gap_context order.
    assert payload.reference_id == "rec_1"


def test_tiebreak_is_deterministic_and_repeatable():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="e1",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="e2",
                         gap_context=BOUNDARY_AMBIGUITY, iteration=2)
    p1 = _derive(s)
    p2 = _derive(s)
    assert p1 == p2
    assert (p1.issue_type, p1.reference_id) == (p2.issue_type, p2.reference_id)


def test_identical_state_yields_identical_selection():
    s1 = _state_with_open_gap()
    s1.record_interaction(action=DISPOSITION_ANSWERED, content="owner Z",
                          gap_context=MECHANISM_COMPLETENESS, iteration=1)
    s2 = _snapshot(s1)
    assert _derive(s1) == _derive(s2)


# =================================================================================
# D. Exactly one primary issue, or a truthful no-eligible fallback.
# =================================================================================
def test_exactly_one_primary_issue_or_truthful_fallback():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="e",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type in ISSUE_TYPES
    # exactly one primary issue is exposed (a single payload, not a ranked list)
    assert not isinstance(payload, (list, tuple, set))


def test_verified_ready_state_does_not_invent_a_problem():
    s = _fresh_state()
    s.maturity_level = 2
    # one CLOSED gap + an independently-verified owner answer => verified readiness
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=1,
                      closed_at=2))
    s.record_interaction(action=DISPOSITION_ANSWERED, content="verified value",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1,
                         validation_status=INDEPENDENTLY_VERIFIED)
    payload = _derive(s)
    # No invented problem: either no payload, or a non-problem "ready" statement.
    assert payload is None or payload.issue_type not in PROBLEM_ISSUE_TYPES


# =================================================================================
# E. Presentation-only semantics (no winner / no scoring / no mutation).
# =================================================================================
def test_contradiction_payload_selects_no_winner_and_does_not_mutate():
    s = _state_with_open_gap()
    a = s.record_interaction(action=DISPOSITION_ANSWERED, content="A",
                             gap_context=MECHANISM_COMPLETENESS, iteration=1)
    b = s.record_interaction(action=DISPOSITION_ANSWERED, content="B",
                             gap_context=MECHANISM_COMPLETENESS, iteration=2)
    s.mark_contradiction(a.record_id, b.record_id)
    before = _snapshot(s)
    payload = _derive(s)
    assert payload is not None and payload.issue_type == "active_contradiction"
    # No winner chosen: neither contradicting record becomes superseded by derivation.
    rec_a = next(r for r in s.assertions if r.record_id == a.record_id)
    rec_b = next(r for r in s.assertions if r.record_id == b.record_id)
    assert rec_a.superseded_by is None and rec_b.superseded_by is None
    # Pure: state is structurally unchanged.
    assert s == before


# =================================================================================
# F. O-1 provider grounding (engine-resident only; no invention).
# =================================================================================
def test_provider_is_always_in_vocabulary_or_absent():
    for s in (
        _fresh_state(),
        _state_with_open_gap(),
    ):
        payload = _derive(s)
        if payload is not None:
            assert payload.suggested_provider is None \
                or payload.suggested_provider in PROVIDER_VOCAB


def test_evidence_request_grounds_to_empirical_evidence():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="measure",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None and payload.issue_type == "pending_evidence"
    assert payload.suggested_provider == EMPIRICAL_EVIDENCE


def test_specialist_request_grounds_to_specialist_input():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_SPECIALIST_REQUESTED, content="ask EE",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None and payload.issue_type == "pending_specialist"
    assert payload.suggested_provider == SPECIALIST_INPUT


def test_owner_unvalidated_answer_grounds_to_owner_input():
    s = _state_with_open_gap()
    rec = s.record_interaction(action=DISPOSITION_ANSWERED, content="owner Z",
                               gap_context=MECHANISM_COMPLETENESS, iteration=1)
    assert rec.provenance == OWNER_STATED and rec.responsibility == OWNER_INPUT
    payload = _derive(s)
    assert payload is not None and payload.issue_type == "owner_unvalidated"
    assert payload.suggested_provider == OWNER_INPUT


def test_bare_open_gap_provider_is_undetermined_or_absent_no_invention():
    s = _state_with_open_gap()   # no records: no engine-resident responsibility
    payload = _derive(s)
    assert payload is not None and payload.issue_type == "open_gap"
    assert payload.suggested_provider in (UNDETERMINED, None)


# =================================================================================
# G. Payload field-equivalent contract (truthful absence permitted).
# =================================================================================
def test_payload_exposes_all_field_equivalents():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="measure",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None
    for field in PAYLOAD_FIELDS:
        assert hasattr(payload, field), f"payload missing field-equivalent: {field}"
    # issue_type / reference_id are required, non-empty
    assert isinstance(payload.issue_type, str) and payload.issue_type
    assert isinstance(payload.reference_id, str) and payload.reference_id
    # optional fields are str or truthful absence (None / empty) — never fabricated
    for field in ("evidence_needed", "suggested_provider", "sufficiency_condition",
                  "unlock_condition", "remaining_uncertainty"):
        val = getattr(payload, field)
        assert val is None or isinstance(val, str)


# =================================================================================
# H. Immutability and purity.
# =================================================================================
def test_payload_is_immutable():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="m",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None
    with pytest.raises((AttributeError, TypeError)):
        payload.issue_type = "mutated"


def test_derivation_does_not_mutate_idea_state():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_ANSWERED, content="owner Z",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    before = _snapshot(s)
    _derive(s)
    # No assertion/gap/disposition/history/score/maturity/stage field changed.
    assert s == before
    assert s.maturity_level == before.maturity_level
    assert len(s.assertions) == len(before.assertions)
    assert [g.status for g in s.gaps] == [g.status for g in before.gaps]


def test_repeated_derivation_is_equal():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_SPECIALIST_REQUESTED, content="ask",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    assert _derive(s) == _derive(s)


# =================================================================================
# I. O-2 same primary issue on both surfaces (required test name).
# =================================================================================
def test_session_and_deliverable_same_primary_issue():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="measure",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    payload = _derive(s)
    assert payload is not None

    # Deliverable surface: assembler consumes the SAME derivation via an additive
    # section exposing (issue_type, reference_id).
    package = assemble_deliverable(s)
    assert ADDITIVE_SECTION_KEY in package, \
        "assembler has not integrated the shared next-development-step derivation"
    section = package[ADDITIVE_SECTION_KEY]
    assert (section["issue_type"], section["reference_id"]) \
        == (payload.issue_type, payload.reference_id)

    # Session surface: show_session passes the SAME payload; the rendered callout
    # exposes the same stable reference identifier (templates do not compute it).
    resp = _render_session(s)
    assert resp.status_code == 200
    assert payload.reference_id.encode() in resp.data, \
        "session callout does not render the engine-selected primary issue"


# =================================================================================
# J. Additive assembler behavior (existing sections unchanged).
# =================================================================================
def test_assembler_is_additive_existing_sections_preserved():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="m",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    package = assemble_deliverable(s)
    # Existing Increment 1/2 sections and meta must all remain present.
    for key in ("section_1_disclaimer", "section_2_invention_summary",
                "section_7_recommendations", "section_8_unresolved_items",
                "section_10_recommended_next_steps", "_session_meta"):
        assert key in package, f"existing deliverable key missing: {key}"
    # The new visible-output section is additive (this assertion fails pre-impl).
    assert ADDITIVE_SECTION_KEY in package


def test_assembler_does_not_replace_existing_verdict_or_readiness():
    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_ANSWERED, content="owner Z",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)
    package = assemble_deliverable(s)
    # Existing verdict + derived readiness meaning is preserved (unchanged keys).
    assert "category_a_proceed_revise_block" in package["section_7_recommendations"]
    assert "derived_verified_ready" in package["_session_meta"]


def test_assembler_does_not_crash_on_legacy_incomplete_state():
    # A bare legacy state with no ledger and no gaps must assemble without error.
    s = _fresh_state()
    package = assemble_deliverable(s)
    assert isinstance(package, dict) and "section_1_disclaimer" in package
    # The additive section is present even for legacy state (conservative fallback).
    assert ADDITIVE_SECTION_KEY in package


# =================================================================================
# K. Template fallback behavior (presentation-only; safe with absent payload).
# =================================================================================
def test_deliverable_renders_without_crashing_on_legacy_state():
    s = _fresh_state()
    resp = _render_deliverable(s)
    assert resp.status_code == 200
    # Existing fallback content remains visible (Increment 1/2 behavior preserved).
    assert b"InventorAI" in resp.data


def test_session_renders_without_crashing_on_legacy_state():
    s = _fresh_state()
    resp = _render_session(s)
    assert resp.status_code == 200
    assert b"InventorAI" in resp.data


# =================================================================================
# L. R-5 route boundary — show_session only; no new/changed route or method.
# =================================================================================
def _route_signature():
    return sorted(
        (rule.rule, tuple(sorted(m for m in rule.methods if m in
                                 {"GET", "POST", "PUT", "PATCH", "DELETE"})))
        for rule in _flask_app.url_map.iter_rules()
    )


def test_no_new_or_changed_route_for_increment_3():
    sig = _route_signature()
    paths = {rule for rule, _ in sig}
    # The session and deliverable routes already exist and are unchanged.
    assert "/session/<sid>" in paths
    assert "/session/<sid>/deliverable" in paths
    # No Increment-3-specific route may be introduced (R-5: show_session only).
    for rule, _ in sig:
        low = rule.lower()
        assert "next-development" not in low
        assert "idea-development" not in low
        assert "development-step" not in low


def test_session_route_methods_unchanged():
    methods = {}
    for rule in _flask_app.url_map.iter_rules():
        methods.setdefault(rule.rule, set()).update(rule.methods)
    # /session/<sid> supports GET (render) and POST (submit_answer) — unchanged by R-5.
    assert "GET" in methods["/session/<sid>"]
    assert "POST" in methods["/session/<sid>"]


# =================================================================================
# N. Frozen-persistence / web-layer non-reuse (static source assertion).
# =================================================================================
def test_engine_derivation_imports_no_forbidden_modules():
    import engine.idea_development_outputs as mod
    src = inspect.getsource(mod)
    for forbidden in ("web.responsibility_labels", "web/responsibility_labels",
                      "engine.session_store", "session_store",
                      "tests.conftest", "conftest"):
        assert forbidden not in src, \
            f"Increment 3 engine derivation must not reference {forbidden!r}"
    # Engine must not depend on the web layer at all.
    assert "import web" not in src and "from web" not in src


# =================================================================================
# O. Hardening A — R-6 tie-break is NUMERIC, not lexicographic (rec_2 < rec_10).
# =================================================================================
def test_tiebreak_numeric_record_id_beats_lexicographic_order():
    """At least ten same-priority eligible records exist; the pending-evidence
    candidates include rec_2 and rec_10. R-6 clause 1 selects the lowest NUMERIC
    rec_N (rec_2, because 2 < 10). A lexicographic implementation would instead
    select rec_10 (since the string "rec_10" sorts before "rec_2") and must fail."""
    s = _state_with_open_gap()
    # rec_1 is a LOWER-priority specialist request (level 3); it is excluded from the
    # selected pending-evidence (level 2) set, so the lowest ELIGIBLE id is rec_2.
    first = s.record_interaction(action=DISPOSITION_SPECIALIST_REQUESTED, content="ask",
                                 gap_context=MECHANISM_COMPLETENESS, iteration=1)
    assert first.record_id == "rec_1"
    # rec_2 .. rec_10 are nine same-level pending-evidence candidates (native append).
    for i in range(2, 11):
        s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED,
                             content=f"measure-{i}",
                             gap_context=MECHANISM_COMPLETENESS, iteration=i)
    evidence_ids = [r.record_id for r in s.assertions
                    if r.disposition == DISPOSITION_EVIDENCE_REQUESTED]
    # The governed identifiers exist, and lexicographic vs numeric MIN disagree:
    assert "rec_2" in evidence_ids and "rec_10" in evidence_ids
    assert min(evidence_ids) == "rec_10"                                  # lexicographic
    assert min(evidence_ids, key=lambda x: int(x.split("_")[1])) == "rec_2"  # numeric
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "pending_evidence"
    # Numeric parse of the rec_N suffix wins: rec_2, NOT the lexicographic rec_10.
    assert payload.reference_id == "rec_2"
    assert payload.reference_id != "rec_10"


# =================================================================================
# P. Hardening B — all-seven-level peeling: each excluded higher level reveals the
#    next governed level (independent mixed states; no production selector in test).
# =================================================================================
_EXPECTED_BY_TOP_LEVEL = {
    1: "active_contradiction",
    2: "pending_evidence",
    3: "pending_specialist",
    4: "provisional_assumption",
    5: "owner_unvalidated",
    6: "open_gap",
    7: "maturity",
}


def _add_level_candidate(s, level):
    """Append ONE repository-native eligible candidate for the given R-2 level.

    Fixture CONSTRUCTION ONLY (mirrors _state_with_open_gap) — it contains no
    priority/selection logic; it merely records native dispositions / gaps. The
    level-1 contradiction pair is placed on a DISTINCT gap_context so it is not
    conflated with the level-5 owner-unvalidated answer."""
    if level == 1:
        a = s.record_interaction(action=DISPOSITION_ANSWERED, content="contra-A",
                                 gap_context=BOUNDARY_AMBIGUITY, iteration=11)
        b = s.record_interaction(action=DISPOSITION_ANSWERED, content="contra-B",
                                 gap_context=BOUNDARY_AMBIGUITY, iteration=12)
        s.mark_contradiction(a.record_id, b.record_id)
    elif level == 2:
        s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="measure",
                             gap_context=MECHANISM_COMPLETENESS, iteration=2)
    elif level == 3:
        s.record_interaction(action=DISPOSITION_SPECIALIST_REQUESTED, content="ask EE",
                             gap_context=MECHANISM_COMPLETENESS, iteration=3)
    elif level == 4:
        s.record_interaction(action=DISPOSITION_PROVISIONAL_ASSUMPTION, content="assume Y",
                             gap_context=MECHANISM_COMPLETENESS, iteration=4)
    elif level == 5:
        s.record_interaction(action=DISPOSITION_ANSWERED, content="owner Z",
                             gap_context=MECHANISM_COMPLETENESS, iteration=5)
    elif level == 6:
        s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=1))
    elif level == 7:
        s.maturity_level = 0   # below 2 — the standing final-fallback condition
    else:                                                   # pragma: no cover
        raise AssertionError(f"unknown level {level}")


def _state_with_levels(top):
    """Build a fresh state containing representative eligible issues for EVERY level
    from `top` through 7 (higher levels than `top` are truthfully absent)."""
    s = _fresh_state()
    for level in range(top, 8):
        _add_level_candidate(s, level)
    return s


def test_full_mixed_state_selects_highest_governed_level():
    # The complete mixed state (all seven levels present) selects level 1.
    s = _state_with_levels(top=1)
    payload = _derive(s)
    assert payload is not None
    assert payload.issue_type == "active_contradiction"


def test_peeling_each_excluded_higher_level_reveals_next_governed_level():
    # For each top level k, a state holding exactly levels k..7 selects level k —
    # i.e. excluding the higher levels reveals the next governed level in order.
    for top, expected in _EXPECTED_BY_TOP_LEVEL.items():
        s = _state_with_levels(top=top)
        payload = _derive(s)
        assert payload is not None, f"no payload for top level {top}"
        assert payload.issue_type == expected, (
            f"top level {top}: expected {expected!r}, got {payload.issue_type!r}")


def test_superseding_top_contradiction_reveals_level_two():
    # Truthful in-place demonstration: a full mixed state whose level-1 contradiction
    # is made INACTIVE by superseding one endpoint reveals level 2 (pending_evidence).
    s = _state_with_levels(top=1)
    # The contradiction endpoints are the two BOUNDARY_AMBIGUITY answers (rec_1/rec_2).
    endpoints = [r for r in s.assertions
                 if r.gap_context == BOUNDARY_AMBIGUITY
                 and r.disposition == DISPOSITION_ANSWERED]
    assert len(endpoints) == 2
    resolver = s.record_interaction(action=DISPOSITION_ANSWERED, content="resolves",
                                    gap_context=BOUNDARY_AMBIGUITY, iteration=13)
    s.mark_supersession(endpoints[0].record_id, resolver.record_id)
    payload = _derive(s)
    assert payload is not None
    # Contradiction no longer active -> next governed level (pending_evidence) wins.
    assert payload.issue_type == "pending_evidence"


# =================================================================================
# Q. Hardening C — O-2 shared derivation across multiple states + shared-entry-point
#    call proof (both surfaces invoke the SAME public derivation, not coincidence).
# =================================================================================
def _predetermined_payload(issue_type, reference_id):
    """An explicit, predetermined IMMUTABLE stand-in payload (a namedtuple) used only
    to prove call-routing through the shared public entry point. It contains NO
    selection logic and is NOT a second derivation implementation."""
    from collections import namedtuple
    P = namedtuple("_PredeterminedPayload", PAYLOAD_FIELDS)
    return P(issue_type=issue_type, reference_id=reference_id, title="t",
             why_it_matters="w", next_action="n", evidence_needed=None,
             suggested_provider=None, sufficiency_condition=None,
             unlock_condition=None, remaining_uncertainty=None)


def test_session_and_deliverable_same_primary_issue_multi_state():
    # Two MATERIALLY DIFFERENT priority states (distinct levels and references). Both
    # the deliverable section and the session callout must resolve the SAME
    # (issue_type, reference_id) as the shared public derivation for EACH state —
    # agreement across distinct states rules out coincidental equal output.
    s_evidence = _state_with_open_gap()
    s_evidence.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="measure",
                                  gap_context=MECHANISM_COMPLETENESS, iteration=1)

    s_contra = _state_with_open_gap()
    a = s_contra.record_interaction(action=DISPOSITION_ANSWERED, content="A",
                                    gap_context=MECHANISM_COMPLETENESS, iteration=1)
    b = s_contra.record_interaction(action=DISPOSITION_ANSWERED, content="B",
                                    gap_context=MECHANISM_COMPLETENESS, iteration=2)
    s_contra.mark_contradiction(a.record_id, b.record_id)

    for expected_type, s in (("pending_evidence", s_evidence),
                             ("active_contradiction", s_contra)):
        payload = _derive(s)
        assert payload is not None and payload.issue_type == expected_type

        package = assemble_deliverable(s)
        assert ADDITIVE_SECTION_KEY in package, \
            "assembler has not integrated the shared next-development-step derivation"
        section = package[ADDITIVE_SECTION_KEY]
        assert (section["issue_type"], section["reference_id"]) \
            == (payload.issue_type, payload.reference_id)

        resp = _render_session(s)
        assert resp.status_code == 200
        assert payload.reference_id.encode() in resp.data, \
            "session callout does not render the engine-selected primary issue"


def test_both_surfaces_call_shared_derivation_entry_point(monkeypatch):
    # Prove BOTH integration surfaces invoke the SAME public entry point
    # engine.idea_development_outputs.derive_next_development_step (not two separate
    # equivalent algorithms). Pre-implementation the module import fails here, which
    # is an EXPECTED MISSING SHARED DERIVATION failure (the entry point is absent).
    import engine.idea_development_outputs as mod   # ModuleNotFoundError pre-impl
    import engine.deliverable_assembler as _asm
    import web.app as _webapp

    calls = []
    predetermined = _predetermined_payload("pending_evidence", "rec_1")

    def _spy(state):
        calls.append(state)            # record the call only — NO selection logic
        return predetermined

    # Patch the governed public entry point at its canonical home and at any consumer
    # lookup site that already binds it (standard "patch where it is looked up" idiom;
    # guarded so no private detail is assumed and no second selector is introduced).
    monkeypatch.setattr(mod, "derive_next_development_step", _spy)
    if hasattr(_asm, "derive_next_development_step"):
        monkeypatch.setattr(_asm, "derive_next_development_step", _spy)
    if hasattr(_webapp, "derive_next_development_step"):
        monkeypatch.setattr(_webapp, "derive_next_development_step", _spy)

    s = _state_with_open_gap()
    s.record_interaction(action=DISPOSITION_EVIDENCE_REQUESTED, content="m",
                         gap_context=MECHANISM_COMPLETENESS, iteration=1)

    # Deliverable surface calls the shared entry point and renders its output.
    calls.clear()
    package = assemble_deliverable(s)
    assert len(calls) >= 1, "assembler did not call the shared derivation entry point"
    assert package[ADDITIVE_SECTION_KEY]["reference_id"] == "rec_1"

    # Session surface calls the SAME entry point with the ALREADY-LOADED in-memory
    # IdeaState (object identity), proving one selection feeds both surfaces.
    calls.clear()
    resp = _render_session(s)
    assert resp.status_code == 200
    assert any(c is s for c in calls), \
        "session did not call the shared derivation with the in-memory IdeaState"
    assert b"rec_1" in resp.data
