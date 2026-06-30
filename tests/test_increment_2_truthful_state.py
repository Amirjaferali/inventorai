"""Increment 2 — Truthful Gap and Evidence State — tests-first expected-failure package.

These tests are written BEFORE any production-source change (tests-first), per the
committed `docs/governance/INCREMENT_2_IMPLEMENTATION_CONTRACT.md` and
`docs/governance/INCREMENT_2_AUTHORITY_RULINGS.md`, and the binding corrections
C-1..C-4 of the implementation-authorization readiness decision.

This package was authored tests-first: each Increment 2 behavior was first added
as `pytest.mark.xfail(strict=True)` (failing because the interface/semantics were
absent), verified to fail for the genuine absent-behavior reason, and only then
implemented. Per the bounded source-implementation sequence, each strict-xfail
marker was removed once — and only once — the asserted behavior genuinely passed.
They are now plain passing conformance tests for the implemented behavior.

The six-action set and engine persistence-independence are protected invariants
(plain passing anchors that held both before and after Increment 2).

Posited minimum public interface (the source phase will implement exactly this; the
tests assert behavior, not internal class names beyond this minimum):

  engine.idea_state:
    - provenance constants:  LEGACY_UNSPECIFIED (the default), OWNER_STATED,
      SYSTEM_INFERRED, EXPERT_SUPPLIED, EXTERNAL_EVIDENCE
    - validation constants:  UNVALIDATED (the default), SPECIALIST_REVIEWED,
      EMPIRICALLY_DEMONSTRATED, INDEPENDENTLY_VERIFIED
    - responsibility constants: OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT,
      EMPIRICAL_EVIDENCE, UNDETERMINED
    - Evidence gains additive, defaulted `provenance` (= LEGACY_UNSPECIFIED) and
      `validation_status` (= UNVALIDATED) fields
    - Gap gains additive, defaulted `resolution_rationale` and `resolution_source`
    - IdeaState gains an append-only assertion/interaction ledger `assertions`
      (list) plus:
        record_interaction(action, content, gap_context, iteration,
                           provenance=LEGACY_UNSPECIFIED,
                           validation_status=UNVALIDATED, quality=None) -> record
        get_assertions(gap_context=None) -> list[record]
        mark_contradiction(record_id_a, record_id_b) -> None
        mark_supersession(superseded_id, by_id) -> None
        has_unresolved_contradiction(gap_context) -> bool
      each record exposes at minimum: record_id, content, gap_context, iteration,
      disposition, provenance, validation_status, quality, pending,
      contradicts, supersedes

  engine.derived_readiness (new pure module):
    - derive_readiness(state) -> readiness object exposing at minimum
      is_verified(gap_type) -> bool; pure (no mutation of state)

  engine.deliverable_assembler.assemble_deliverable(state):
    - evidence views carry `validation_status`; `_session_meta` carries a derived
      `derived_verified_ready` boolean; a `section` reflects derived readiness.

No change to assess_response(), integrate_response(), evaluate_transition(), or
score_case() is asserted or required. Existing known_problem / known_mechanism /
gap status / maturity / lifecycle remain the legacy fields and are NOT the
append-only ledger.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import pytest

import engine.idea_state as idea_state
from engine.idea_state import (
    IdeaState, Evidence, Gap,
    OPEN, PARTIAL, CLOSED,
    ASSERTED, REASONED,
    MECHANISM_COMPLETENESS,
)
from engine.deliverable_assembler import assemble_deliverable
from web.app import INTERACTION_ACTIONS, ACTION_ANSWERED

SIX_ACTIONS = {
    "answered", "unknown", "deferred",
    "provisional_assumption", "specialist_requested", "evidence_requested",
}


def _state():
    s = IdeaState(idea_id="incr2")
    s.domain = "electronics_electrical"
    s.domain_signal = "electronics_electrical"
    return s


def _record(state, action, content="owner content",
            gap_context=MECHANISM_COMPLETENESS, iteration=1, **kw):
    """Probe the (currently absent) append-only interaction ledger."""
    return state.record_interaction(
        action=action, content=content,
        gap_context=gap_context, iteration=iteration, **kw,
    )


# ===========================================================================
# Plain passing regression anchors (MUST hold now and after Increment 2).
# Not xfail: these are protected invariants, not absent behavior.
# ===========================================================================

def test_six_owner_action_identifiers_remain_exact():
    """C-1 / contract §5: exactly the six owner actions, unchanged."""
    assert INTERACTION_ACTIONS == SIX_ACTIONS
    assert ACTION_ANSWERED == "answered"


def test_engine_state_is_persistence_independent():
    """Contract: Increment 2 is persistence-independent. The engine state model
    operates fully in memory and does NOT depend on the frozen session-store
    overlay (`engine/session_store.py`), which is absent here by design."""
    s = _state()
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0)]
    assert s.get_open_gaps()  # works purely in memory
    assert "engine.session_store" not in sys.modules


def test_full_in_memory_cycle_is_persistence_independent():
    """Increment 2 strengthened persistence-independence: the COMPLETE cycle runs
    entirely in memory — create state; record interactions; preserve multiple
    coexisting records; establish a (non-destructive) relationship; derive
    readiness (pure); assemble a deliverable — with NO durable persistence. The
    frozen `engine.session_store` overlay is never imported, and no filesystem or
    database persistence is touched."""
    from engine import derived_readiness as dr
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    # record + preserve multiple coexisting records for one context
    r1 = _record(s, ACTION_ANSWERED, content="Output is 5V.")
    r2 = _record(s, ACTION_ANSWERED, content="Output is 9V.")
    assert len(s.get_assertions(MECHANISM_COMPLETENESS)) == 2
    # establish a relationship (non-destructive; both records retained)
    s.mark_contradiction(r1.record_id, r2.record_id)
    assert {r.record_id for r in s.get_assertions(MECHANISM_COMPLETENESS)} == \
        {r1.record_id, r2.record_id}
    assert s.has_unresolved_contradiction(MECHANISM_COMPLETENESS) is True
    # derive readiness (pure) — constrained below stored CLOSED by the conflict
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is False
    # assemble the deliverable — truthful; does not overstate certainty
    d = assemble_deliverable(s)
    assert d["_session_meta"]["derived_verified_ready"] is False
    # the entire cycle used no durable-persistence overlay
    assert "engine.session_store" not in sys.modules


# ===========================================================================
# Conformance tests for the implemented Increment 2 behaviors. Each was authored
# tests-first as a strict xfail; the marker was removed once the behavior passed.
# ===========================================================================

def test_legacy_evidence_provenance_defaults_to_unspecified():
    legacy = getattr(idea_state, "LEGACY_UNSPECIFIED")
    owner = getattr(idea_state, "OWNER_STATED")
    ev = Evidence(content="x", quality=ASSERTED, iteration=0)
    assert getattr(ev, "provenance") == legacy
    assert getattr(ev, "provenance") != owner


def test_validation_status_independent_of_quality():
    unval = getattr(idea_state, "UNVALIDATED")
    ev = Evidence(content="The Hall sensor detects rotation by measuring flux.",
                  quality=REASONED, iteration=0)
    assert getattr(ev, "validation_status") == unval


def test_owner_answered_assertion_is_not_verified():
    s = _state()
    rec = _record(s, ACTION_ANSWERED, content="It uses a 9V battery.")
    assert rec.provenance == getattr(idea_state, "OWNER_STATED")
    assert rec.validation_status == getattr(idea_state, "UNVALIDATED")


def test_all_six_actions_recordable_in_durable_history():
    s = _state()
    for action in sorted(SIX_ACTIONS):
        _record(s, action)
    recs = s.assertions
    assert len(recs) == 6
    assert {r.disposition for r in recs} == SIX_ACTIONS


def test_unknown_disposition_durable_and_unresolved():
    s = _state()
    rec = _record(s, "unknown")
    assert rec.disposition == "unknown"
    assert getattr(rec, "resolves_gap", False) is False


def test_deferred_distinct_from_unknown():
    s = _state()
    u = _record(s, "unknown")
    d = _record(s, "deferred")
    assert u.disposition == "unknown"
    assert d.disposition == "deferred"
    assert u.disposition != d.disposition


def test_provisional_assumption_durable_and_provisional():
    s = _state()
    rec = _record(s, "provisional_assumption", content="Assume the coating holds.")
    assert rec.disposition == "provisional_assumption"
    assert rec.validation_status == getattr(idea_state, "UNVALIDATED")


def test_specialist_requested_durable_pending():
    s = _state()
    rec = _record(s, "specialist_requested")
    assert rec.disposition == "specialist_requested"
    assert rec.pending == "specialist"


def test_evidence_requested_durable_pending():
    s = _state()
    rec = _record(s, "evidence_requested")
    assert rec.disposition == "evidence_requested"
    assert rec.pending == "evidence"


def test_append_only_history_preserves_multiple_records_for_same_gap():
    s = _state()
    _record(s, ACTION_ANSWERED, content="Output is 5V.")
    _record(s, ACTION_ANSWERED, content="Output is 9V.")
    recs = s.get_assertions(MECHANISM_COMPLETENESS)
    assert len(recs) == 2
    assert {r.content for r in recs} == {"Output is 5V.", "Output is 9V."}


def test_contradiction_preserves_both_records_unresolved():
    s = _state()
    r1 = _record(s, ACTION_ANSWERED, content="Output is 5V.")
    r2 = _record(s, ACTION_ANSWERED, content="Output is 9V.")
    s.mark_contradiction(r1.record_id, r2.record_id)
    recs = s.get_assertions(MECHANISM_COMPLETENESS)
    assert {r.record_id for r in recs} == {r1.record_id, r2.record_id}  # both kept
    assert s.has_unresolved_contradiction(MECHANISM_COMPLETENESS) is True


def test_supersession_preserves_historical_records():
    s = _state()
    r1 = _record(s, ACTION_ANSWERED, content="First estimate.")
    r2 = _record(s, ACTION_ANSWERED, content="Revised estimate.")
    s.mark_supersession(r1.record_id, r2.record_id)
    ids = {r.record_id for r in s.get_assertions(MECHANISM_COMPLETENESS)}
    assert r1.record_id in ids  # history retained
    assert r2.record_id in ids


def test_gap_resolution_records_source_and_rationale():
    g = Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)
    assert hasattr(g, "resolution_rationale")
    assert hasattr(g, "resolution_source")
    # default for an unresolved/legacy gap is empty, never fabricated
    assert getattr(g, "resolution_rationale") in (None, "")


def test_derived_readiness_can_present_below_stored_closed():
    from engine import derived_readiness as dr
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    _record(s, ACTION_ANSWERED, content="owner-only claim, no validation")
    readiness = dr.derive_readiness(s)
    assert readiness.is_verified(MECHANISM_COMPLETENESS) is False


def test_derived_readiness_does_not_mutate_state():
    from engine import derived_readiness as dr
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    before_maturity = s.maturity_level
    before_statuses = [g.status for g in s.gaps]
    dr.derive_readiness(s)
    assert s.maturity_level == before_maturity
    assert [g.status for g in s.gaps] == before_statuses


# ---------------------------------------------------------------------------
# Granular per-constraint derived-readiness tests (closes review observation
# O-1). Each isolates ONE constraint: every other record is forced to an
# independently-verified validation status, so the asserted drop from verified
# to not-verified is attributable ONLY to the named constraint — not to generic
# unvalidated-ness. Each also proves the stored forward-only lifecycle and
# maturity are NOT reversed by the (purely derived) recomputation.
# ---------------------------------------------------------------------------

def test_unresolved_contradiction_constrains_derived_readiness():
    from engine import derived_readiness as dr
    verified = getattr(idea_state, "INDEPENDENTLY_VERIFIED")
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    r1 = _record(s, ACTION_ANSWERED, content="Output is 5V.", validation_status=verified)
    r2 = _record(s, ACTION_ANSWERED, content="Output is 9V.", validation_status=verified)
    # Baseline: two independently-verified records, no conflict -> verified.
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is True
    # The unresolved contradiction alone must drop verified readiness.
    s.mark_contradiction(r1.record_id, r2.record_id)
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is False
    # Stored lifecycle/maturity are NOT reversed by the derivation.
    assert s.maturity_level == 2
    assert s.get_gap(MECHANISM_COMPLETENESS).status == CLOSED


def test_provisional_assumption_constrains_derived_readiness():
    from engine import derived_readiness as dr
    verified = getattr(idea_state, "INDEPENDENTLY_VERIFIED")
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    _record(s, ACTION_ANSWERED, content="Verified mechanism.", validation_status=verified)
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is True
    # Disposition is provisional regardless of validation_status -> constrains.
    _record(s, "provisional_assumption", content="Assume the coating holds.",
            validation_status=verified)
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is False
    assert s.maturity_level == 2
    assert s.get_gap(MECHANISM_COMPLETENESS).status == CLOSED


def test_pending_specialist_request_constrains_derived_readiness():
    from engine import derived_readiness as dr
    verified = getattr(idea_state, "INDEPENDENTLY_VERIFIED")
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    _record(s, ACTION_ANSWERED, content="Verified mechanism.", validation_status=verified)
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is True
    # A still-pending specialist request constrains derived readiness.
    _record(s, "specialist_requested", validation_status=verified)
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is False
    assert s.maturity_level == 2
    assert s.get_gap(MECHANISM_COMPLETENESS).status == CLOSED


def test_pending_evidence_request_constrains_derived_readiness():
    from engine import derived_readiness as dr
    verified = getattr(idea_state, "INDEPENDENTLY_VERIFIED")
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    _record(s, ACTION_ANSWERED, content="Verified mechanism.", validation_status=verified)
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is True
    # A still-pending evidence request constrains derived readiness.
    _record(s, "evidence_requested", validation_status=verified)
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is False
    assert s.maturity_level == 2
    assert s.get_gap(MECHANISM_COMPLETENESS).status == CLOSED


def test_reasoned_evidence_not_presented_as_verified():
    s = _state()
    s.known_mechanism = Evidence(
        content="The comparator switches at 1.2V, latching until reset.",
        quality=REASONED, iteration=1)
    d = assemble_deliverable(s)
    mech = d["section_2_invention_summary"]["known_mechanism"]
    assert mech.get("validation_status") == getattr(idea_state, "UNVALIDATED")


def test_deliverable_does_not_overstate_certainty():
    s = _state()
    s.maturity_level = 2
    s.known_mechanism = Evidence(content="owner-only mechanism claim",
                                 quality=REASONED, iteration=1)
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    _record(s, ACTION_ANSWERED, content="owner-only mechanism claim")
    d = assemble_deliverable(s)
    assert d["_session_meta"].get("derived_verified_ready") is False


def test_system_suggestion_is_not_evidence():
    s = _state()
    rec = _record(s, ACTION_ANSWERED, content="system-suggested value",
                  provenance=getattr(idea_state, "SYSTEM_INFERRED"))
    assert rec.provenance == getattr(idea_state, "SYSTEM_INFERRED")
    assert rec.validation_status == getattr(idea_state, "UNVALIDATED")


def test_specialist_provided_differs_from_specialist_confirmed():
    s = _state()
    provided = _record(s, ACTION_ANSWERED, content="spec value",
                       provenance=getattr(idea_state, "EXPERT_SUPPLIED"),
                       validation_status=getattr(idea_state, "UNVALIDATED"))
    confirmed = _record(s, ACTION_ANSWERED, content="spec value confirmed",
                        provenance=getattr(idea_state, "EXPERT_SUPPLIED"),
                        validation_status=getattr(idea_state, "SPECIALIST_REVIEWED"))
    assert provided.validation_status != confirmed.validation_status


def test_documentary_evidence_differs_from_verbal_assertion():
    s = _state()
    doc = _record(s, ACTION_ANSWERED, content="datasheet value",
                  provenance=getattr(idea_state, "EXTERNAL_EVIDENCE"))
    verbal = _record(s, ACTION_ANSWERED, content="I think it is 5V",
                     provenance=getattr(idea_state, "OWNER_STATED"))
    assert doc.provenance != verbal.provenance


# ===========================================================================
# F-2 — relationship-seam safety and stable identity (review correction pass).
# ===========================================================================

def test_record_ids_unique_and_stable():
    """Record IDs are unique across multiple records and stable: they do not
    change as more records are appended or relationships are established."""
    s = _state()
    recs = [_record(s, ACTION_ANSWERED, content=f"c{i}") for i in range(5)]
    ids = [r.record_id for r in recs]
    assert len(set(ids)) == 5                      # unique
    snapshot = list(ids)
    _record(s, "unknown")                          # append more
    s.mark_contradiction(recs[0].record_id, recs[1].record_id)
    assert [r.record_id for r in recs] == snapshot  # unchanged (stable)


def test_mark_contradiction_rejects_unknown_record_id():
    s = _state()
    r = _record(s, ACTION_ANSWERED)
    with pytest.raises(ValueError):
        s.mark_contradiction(r.record_id, "rec_does_not_exist")
    with pytest.raises(ValueError):
        s.mark_contradiction("rec_does_not_exist", r.record_id)
    assert r.contradicts == []                     # no invalid edge created


def test_mark_supersession_rejects_unknown_record_id():
    s = _state()
    r = _record(s, ACTION_ANSWERED)
    with pytest.raises(ValueError):
        s.mark_supersession(r.record_id, "rec_does_not_exist")
    with pytest.raises(ValueError):
        s.mark_supersession("rec_does_not_exist", r.record_id)
    assert r.superseded_by is None                 # no invalid edge created


def test_self_contradiction_and_self_supersession_rejected():
    """F-5: a record cannot contradict or supersede itself; no self-edge forms."""
    s = _state()
    r = _record(s, ACTION_ANSWERED)
    with pytest.raises(ValueError):
        s.mark_contradiction(r.record_id, r.record_id)
    with pytest.raises(ValueError):
        s.mark_supersession(r.record_id, r.record_id)
    assert r.contradicts == []
    assert r.superseded_by is None
    assert r.supersedes == []


def test_relationship_operations_are_idempotent():
    """Repeated valid contradiction/supersession operations do not duplicate
    edges and do not delete records."""
    s = _state()
    a = _record(s, ACTION_ANSWERED, content="a")
    b = _record(s, ACTION_ANSWERED, content="b")
    s.mark_contradiction(a.record_id, b.record_id)
    s.mark_contradiction(a.record_id, b.record_id)
    assert a.contradicts == [b.record_id]
    assert b.contradicts == [a.record_id]
    c = _record(s, ACTION_ANSWERED, content="c")
    s.mark_supersession(a.record_id, c.record_id)
    s.mark_supersession(a.record_id, c.record_id)
    assert c.supersedes == [a.record_id]
    assert a.superseded_by == c.record_id
    assert len(s.assertions) == 3                  # nothing deleted


# ===========================================================================
# F-3 — explicit supersession deactivates the superseded record for CURRENT
# derived-readiness evaluation only, preserving it immutably in history.
# ===========================================================================

def test_verified_readiness_after_unvalidated_superseded_by_verified():
    """Owner ruling: an unvalidated record explicitly superseded by an
    independently verified record permits verified readiness when no other active
    blocker remains; the superseded record stays immutably in history."""
    from engine import derived_readiness as dr
    verified = getattr(idea_state, "INDEPENDENTLY_VERIFIED")
    unval = getattr(idea_state, "UNVALIDATED")
    s = _state()
    old = _record(s, ACTION_ANSWERED, content="old guess", validation_status=unval)
    new = _record(s, ACTION_ANSWERED, content="verified value", validation_status=verified)
    # Before supersession the active unvalidated record blocks readiness.
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is False
    s.mark_supersession(old.record_id, new.record_id)
    # The superseding verified record now drives readiness.
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is True
    # History retained and immutable.
    ids = {r.record_id for r in s.get_assertions(MECHANISM_COMPLETENESS)}
    assert old.record_id in ids and new.record_id in ids
    assert old.content == "old guess"
    assert old.validation_status == unval
    assert old.superseded_by == new.record_id


def test_verified_readiness_false_when_verified_superseded_by_unvalidated():
    """Owner ruling point 5: a superseding UNVALIDATED record still prevents
    verified readiness, even though the record it supersedes was verified."""
    from engine import derived_readiness as dr
    verified = getattr(idea_state, "INDEPENDENTLY_VERIFIED")
    unval = getattr(idea_state, "UNVALIDATED")
    s = _state()
    old = _record(s, ACTION_ANSWERED, content="verified", validation_status=verified)
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is True
    new = _record(s, ACTION_ANSWERED, content="new guess", validation_status=unval)
    s.mark_supersession(old.record_id, new.record_id)
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is False
    # The verified record remains in history, unchanged.
    assert old.validation_status == verified
    assert old.superseded_by == new.record_id


# ===========================================================================
# F-1 — user-VISIBLE deliverable truthfulness. These assert fields that
# `web/templates/deliverable.html` actually renders (the Recommendations verdict
# and rationale, and the Open Items / category_d action bullets) — not only the
# buried `_session_meta` flag.
# ===========================================================================

def _level2_unvalidated_web_state():
    """A maturity-2 state whose CLOSED gap rests only on an unvalidated owner
    answer (the real web flow): stored state is positive, derived readiness is
    not met."""
    s = _state()
    s.maturity_level = 2
    s.known_mechanism = Evidence(content="owner-only mechanism claim",
                                 quality=REASONED, iteration=1)
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    _record(s, ACTION_ANSWERED, content="owner-only mechanism claim")
    return s


def test_rendered_verdict_does_not_overstate_when_unvalidated():
    s = _level2_unvalidated_web_state()
    d = assemble_deliverable(s)
    assert d["_session_meta"]["derived_verified_ready"] is False
    # Stored eligibility remains visible as stored state (not erased).
    assert d["_session_meta"]["deliverable_eligible"] is True
    cat_a = d["section_7_recommendations"]["category_a_proceed_revise_block"]
    # The user-visible verdict must NOT be an unqualified PROCEED, and must stay
    # within the FDC-001 valid verdict set.
    assert cat_a["verdict"] != "PROCEED"
    assert cat_a["verdict"] in ("PROCEED WITH CAUTION", "REVISE", "BLOCK")
    # The user-visible rationale states verification is incomplete and does not
    # claim all gaps resolved.
    rationale = cat_a["rationale"].lower()
    assert "not" in rationale and "verif" in rationale
    assert "all identified gaps resolved" not in rationale


def test_unresolved_validation_is_visible_in_rendered_open_items():
    """The 'No unresolved items'/'all resolved' overstatement is countered in a
    field the template renders: the Open Items (category_d) action bullets."""
    s = _level2_unvalidated_web_state()
    d = assemble_deliverable(s)
    actions = [it["action"].lower() for it in
               d["section_7_recommendations"]["category_d_open_items"]]
    assert any("verification remains incomplete" in a for a in actions)


def test_verified_web_state_may_present_verified_after_supersession():
    """Symmetric positive: once the unvalidated basis is superseded by an
    independently verified record, the rendered verdict is no longer forced to
    the caution form and derived readiness is met."""
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    old = _record(s, ACTION_ANSWERED, content="owner-only claim",
                  validation_status=getattr(idea_state, "UNVALIDATED"))
    new = _record(s, ACTION_ANSWERED, content="independently verified value",
                  validation_status=getattr(idea_state, "INDEPENDENTLY_VERIFIED"))
    s.mark_supersession(old.record_id, new.record_id)
    d = assemble_deliverable(s)
    assert d["_session_meta"]["derived_verified_ready"] is True
    actions = [it["action"].lower() for it in
               d["section_7_recommendations"]["category_d_open_items"]]
    assert not any("verification remains incomplete" in a for a in actions)


# ===========================================================================
# F-1 final visible-product correction — the Unresolved Items section must not
# render the unqualified "No unresolved items." while derived readiness is false.
# These render the ACTUAL deliverable template via the Flask route (the real
# rendering path), then inspect the returned HTML.
# ===========================================================================

from web.app import app as _flask_app, SESSION_STORE as _SESSION_STORE

_NO_UNRESOLVED = "No unresolved items."


def _render_deliverable_html(state):
    """Render the real `deliverable.html` template through the Flask deliverable
    route and return the decoded HTML (not the assembler dict)."""
    sid = "incr2-render-" + str(id(state))
    _SESSION_STORE[sid] = {"state": state}
    try:
        resp = _flask_app.test_client().get(f"/session/{sid}/deliverable")
        assert resp.status_code == 200
        return resp.data.decode("utf-8")
    finally:
        _SESSION_STORE.pop(sid, None)


def test_rendered_html_no_false_no_unresolved_items_when_readiness_false():
    # derived_verified_ready == False, no stored open gaps (CLOSED gap only).
    s = _level2_unvalidated_web_state()
    html = _render_deliverable_html(s)
    # The absolute fallback must NOT appear.
    assert _NO_UNRESOLVED not in html
    # A truthful caveat distinguishing stored gap closure from unresolved
    # validation and from technical verification must appear.
    assert "No stored gaps remain open" in html          # stored gap closure
    assert "evidence validation" in html                 # unresolved validation
    assert "not technically verified" in html            # lack of verification


def test_rendered_html_clean_fallback_allowed_when_readiness_true():
    # derived_verified_ready == True (independently verified), no open gaps.
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    _record(s, ACTION_ANSWERED, content="bench-verified value",
            validation_status=getattr(idea_state, "INDEPENDENTLY_VERIFIED"))
    html = _render_deliverable_html(s)
    assert _NO_UNRESOLVED in html                         # clean fallback allowed
    assert "No stored gaps remain open" not in html       # caveat NOT shown


def test_rendered_html_open_gap_rendering_unchanged():
    # An OPEN gap must still render via the existing open-gap branch, and neither
    # fallback message appears (the section has items).
    s = _state()
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0)]
    html = _render_deliverable_html(s)
    assert "Mechanism Completeness" in html               # gap_label rendered
    assert _NO_UNRESOLVED not in html
    assert "No stored gaps remain open" not in html


def test_rendered_html_acknowledged_unknown_not_used_for_validation_blockers():
    # An acknowledged unknown renders via its own branch; the validation caveat is
    # NOT rendered (items present) and validation blockers are never labelled as
    # inventor-acknowledged unknowns.
    from engine.idea_state import AcknowledgedUnknown
    s = _state()
    s.maturity_level = 2
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    s.acknowledged_unknowns = [AcknowledgedUnknown(
        iteration=1, gap_context=MECHANISM_COMPLETENESS,
        verbatim="I do not know the exact trip voltage.",
        category_basis="owner_stated")]
    _record(s, ACTION_ANSWERED, content="owner-only claim")  # readiness false
    html = _render_deliverable_html(s)
    assert "Acknowledged unknown:" in html
    assert "I do not know the exact trip voltage." in html
    # The empty-section validation caveat must not appear (the section has items),
    # so a validation blocker is never shown as an "Acknowledged unknown".
    assert "No stored gaps remain open" not in html
    assert _NO_UNRESOLVED not in html


# ===========================================================================
# O-2 — supersession cycles (direct and indirect) are rejected atomically; the
# supersession graph stays acyclic; valid acyclic chains of any length work.
# ===========================================================================

def _rel_snapshot(state):
    return {r.record_id: (r.superseded_by, tuple(r.supersedes), tuple(r.contradicts))
            for r in state.assertions}


def test_self_supersession_rejected_atomic():
    s = _state()
    a = _record(s, ACTION_ANSWERED, content="a")
    before = _rel_snapshot(s)
    with pytest.raises(ValueError):
        s.mark_supersession(a.record_id, a.record_id)
    assert _rel_snapshot(s) == before


def test_two_record_supersession_cycle_rejected():
    s = _state()
    a = _record(s, ACTION_ANSWERED, content="a")
    b = _record(s, ACTION_ANSWERED, content="b")
    s.mark_supersession(a.record_id, b.record_id)          # A -> B
    with pytest.raises(ValueError):
        s.mark_supersession(b.record_id, a.record_id)      # would close A<->B
    assert a.superseded_by == b.record_id
    assert b.superseded_by is None
    assert b.supersedes == [a.record_id]
    assert a.supersedes == []


def test_three_record_indirect_cycle_rejected():
    s = _state()
    a = _record(s, ACTION_ANSWERED, content="a")
    b = _record(s, ACTION_ANSWERED, content="b")
    c = _record(s, ACTION_ANSWERED, content="c")
    s.mark_supersession(a.record_id, b.record_id)          # A -> B
    s.mark_supersession(b.record_id, c.record_id)          # B -> C
    with pytest.raises(ValueError):
        s.mark_supersession(c.record_id, a.record_id)      # would close A->B->C->A
    assert a.superseded_by == b.record_id
    assert b.superseded_by == c.record_id
    assert c.superseded_by is None
    assert c.supersedes == [b.record_id]


def test_failed_cycle_attempt_leaves_all_relationships_unchanged():
    s = _state()
    a = _record(s, ACTION_ANSWERED, content="a")
    b = _record(s, ACTION_ANSWERED, content="b")
    s.mark_supersession(a.record_id, b.record_id)
    before = _rel_snapshot(s)
    with pytest.raises(ValueError):
        s.mark_supersession(b.record_id, a.record_id)
    assert _rel_snapshot(s) == before                      # no partial mutation
    assert len(s.assertions) == 2                          # nothing deleted


def test_valid_acyclic_chain_accepted_idempotent_and_readiness_on_tip():
    from engine import derived_readiness as dr
    verified = getattr(idea_state, "INDEPENDENTLY_VERIFIED")
    unval = getattr(idea_state, "UNVALIDATED")
    s = _state()
    s.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=0)]
    a = _record(s, ACTION_ANSWERED, content="a", validation_status=unval)
    b = _record(s, ACTION_ANSWERED, content="b", validation_status=unval)
    c = _record(s, ACTION_ANSWERED, content="c", validation_status=verified)
    s.mark_supersession(a.record_id, b.record_id)          # A -> B
    s.mark_supersession(b.record_id, c.record_id)          # B -> C (arbitrary chain)
    s.mark_supersession(b.record_id, c.record_id)          # duplicate -> idempotent
    assert b.superseded_by == c.record_id
    assert c.supersedes == [b.record_id]                   # not duplicated
    # readiness evaluates only the active chain tip C (verified) -> True
    assert dr.derive_readiness(s).is_verified(MECHANISM_COMPLETENESS) is True
    # historical records remain available after valid supersession
    assert {r.record_id for r in s.get_assertions(MECHANISM_COMPLETENESS)} == \
        {a.record_id, b.record_id, c.record_id}


# ===========================================================================
# O-1 — legacy-safe template access: a package whose `_session_meta` lacks the
# `derived_verified_ready` key must render the conservative cautionary fallback
# (never "No unresolved items.", never a template exception).
# ===========================================================================

def test_legacy_package_missing_readiness_key_renders_caveat():
    # Build a real assembled package, then remove the readiness key to simulate a
    # legacy package, and render the ACTUAL template.
    s = _level2_unvalidated_web_state()
    pkg = assemble_deliverable(s)
    del pkg["_session_meta"]["derived_verified_ready"]
    with _flask_app.test_request_context("/"):
        html = _flask_app.jinja_env.get_template("deliverable.html").render(
            package=pkg, sid="legacy",
            eligible=pkg["_session_meta"]["deliverable_eligible"])
    assert _NO_UNRESOLVED not in html                      # conservative
    assert "No stored gaps remain open" in html            # cautionary fallback
