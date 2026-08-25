"""W2-A / RVR-4 — carrier-level decision-action mint seam (frozen contract §2/§3/§8).

Covers RVR4-SEAM-1..3, RVR4-PROV-1..2, RVR4-SUP-1..5 and the falsy-neutral
gap-linkage rule. The carrier (`IdeaState.record_interaction`) itself must fail
closed on any invalid decision-action mint BEFORE anything is appended — there
is no privileged bypass path around `engine.decision_composition`.
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    IdeaState, INTERACTION_DISPOSITIONS, OWNER_STATED, LEGACY_UNSPECIFIED,
    OWNER_INPUT, DISPOSITION_ANSWERED, DISPOSITION_RISK_ACCEPTED,
    PHYSICAL_FEASIBILITY,
    DECISION_ACTION_DISPOSITIONS,
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN,
)

CTX = DISPOSITION_DECISION_CONTEXT_DECLARED
ALT = DISPOSITION_DECISION_ALTERNATIVE_DECLARED
WDR = DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN


def _s():
    return IdeaState(idea_id="pid-1")


def _ctx(s, content="Which latch mechanism should hold the ramp?"):
    return s.record_interaction(action=CTX, content=content)


def _alt(s, root, content="Toggle latch over the center"):
    return s.record_interaction(action=ALT, content=content,
                                decision_context_root=root)


# --- vocabulary (frozen §2) --------------------------------------------------

def test_vocabulary_exactly_three_decision_actions():
    assert DECISION_ACTION_DISPOSITIONS == frozenset({
        "decision_context_declared", "decision_alternative_declared",
        "decision_alternative_withdrawn"})
    assert DECISION_ACTION_DISPOSITIONS <= INTERACTION_DISPOSITIONS
    # seven legacy + exactly three decision actions, nothing else
    assert len(INTERACTION_DISPOSITIONS) == 10
    assert "decision_context_withdrawn" not in INTERACTION_DISPOSITIONS
    assert not any("refine" in d for d in INTERACTION_DISPOSITIONS)


# --- RVR4-SEAM-1: legacy behavior byte-/semantics-unchanged ------------------

def test_seam1_legacy_mint_unchanged():
    s = _s()
    r = s.record_interaction(action=DISPOSITION_ANSWERED, content="an answer",
                             gap_context=PHYSICAL_FEASIBILITY, iteration=2)
    assert r.provenance == OWNER_STATED and r.responsibility == OWNER_INPUT
    assert r.resolves_gap is False and r.decision_context_root is None
    assert r.gap_context == PHYSICAL_FEASIBILITY
    # explicit legacy provenance override still wins for legacy actions
    r2 = s.record_interaction(action=DISPOSITION_ANSWERED, content="x",
                              gap_context=PHYSICAL_FEASIBILITY,
                              provenance=LEGACY_UNSPECIFIED)
    assert r2.provenance == LEGACY_UNSPECIFIED
    with pytest.raises(ValueError):
        s.record_interaction(action="totally_unknown")


def test_seam1_legacy_multi_target_supersession_not_narrowed():
    # RVR4-SUP-5: the generic primitive keeps multi-target FORWARD supersession
    # for legacy records (one new record superseding two priors).
    s = _s()
    a = s.record_interaction(action=DISPOSITION_ANSWERED, content="a",
                             gap_context=PHYSICAL_FEASIBILITY)
    b = s.record_interaction(action=DISPOSITION_ANSWERED, content="b",
                             gap_context=PHYSICAL_FEASIBILITY)
    c = s.record_interaction(action=DISPOSITION_ANSWERED, content="c",
                             gap_context=PHYSICAL_FEASIBILITY,
                             supersedes=[a.record_id, b.record_id])
    assert a.superseded_by == c.record_id and b.superseded_by == c.record_id


# --- RVR4-SEAM-2: valid canonical mints --------------------------------------

def test_seam2_valid_context_alternative_refine_withdraw():
    s = _s()
    ctx = _ctx(s)
    assert ctx.disposition == CTX and ctx.decision_context_root is None
    alt = _alt(s, ctx.record_id)
    assert alt.decision_context_root == ctx.record_id
    # refinement: same class, same context, single target
    ref = s.record_interaction(action=ALT, content="Improved toggle latch",
                               decision_context_root=ctx.record_id,
                               supersedes=[alt.record_id])
    assert alt.superseded_by == ref.record_id
    # withdrawal: supersedes the active head, same context root
    w = s.record_interaction(action=WDR, content="not robust enough",
                             decision_context_root=ctx.record_id,
                             supersedes=[ref.record_id])
    assert ref.superseded_by == w.record_id
    # context refinement is carrier-legal (chain-preserving, no route needed)
    cref = s.record_interaction(action=CTX, content="Which latch, given cost?",
                                supersedes=[ctx.record_id])
    assert ctx.superseded_by == cref.record_id
    assert cref.decision_context_root is None


# --- RVR4-PROV-1/2: provenance -----------------------------------------------

def test_prov1_decision_actions_default_owner_stated():
    s = _s()
    ctx = _ctx(s)
    alt = _alt(s, ctx.record_id)
    w = s.record_interaction(action=WDR, decision_context_root=ctx.record_id,
                             supersedes=[alt.record_id])
    for r in (ctx, alt, w):
        assert r.provenance == OWNER_STATED
        assert r.responsibility == OWNER_INPUT


def test_prov2_conflicting_override_fails_closed_legacy_untouched():
    s = _s()
    before = len(s.assertions)
    with pytest.raises(ValueError):
        s.record_interaction(action=CTX, content="q",
                             provenance=LEGACY_UNSPECIFIED)
    assert len(s.assertions) == before
    # explicit OWNER_STATED (the one legal explicit value) still succeeds
    ctx = s.record_interaction(action=CTX, content="q", provenance=OWNER_STATED)
    assert ctx.provenance == OWNER_STATED


# --- RVR4-SEAM-3: direct bypass fails closed BEFORE append -------------------

def _refused(s, **kwargs):
    before = list(s.assertions)
    with pytest.raises(ValueError):
        s.record_interaction(**kwargs)
    assert s.assertions == before  # NOTHING appended, no edge written


def test_seam3_missing_and_invalid_roots_fail_closed():
    s = _s()
    ctx = _ctx(s)
    ans = s.record_interaction(action=DISPOSITION_ANSWERED, content="a",
                               gap_context=PHYSICAL_FEASIBILITY)
    _refused(s, action=ALT, content="no root at all")
    _refused(s, action=ALT, content="x", decision_context_root="rec_999")
    _refused(s, action=ALT, content="x", decision_context_root=ans.record_id)
    # a context REFINEMENT is not a founding root
    cref = s.record_interaction(action=CTX, content="refined q",
                                supersedes=[ctx.record_id])
    _refused(s, action=ALT, content="x", decision_context_root=cref.record_id)
    # context declaration may not carry a root
    _refused(s, action=CTX, content="q2", decision_context_root=ctx.record_id)
    # legacy record may not carry a root
    _refused(s, action=DISPOSITION_ANSWERED, content="a2",
             gap_context=PHYSICAL_FEASIBILITY,
             decision_context_root=ctx.record_id)


def test_seam3_forbidden_gap_context_on_decision_actions():
    s = _s()
    ctx = _ctx(s)
    _refused(s, action=CTX, content="q", gap_context=PHYSICAL_FEASIBILITY)
    _refused(s, action=ALT, content="x", decision_context_root=ctx.record_id,
             gap_context=PHYSICAL_FEASIBILITY)


def test_seam3_cross_class_and_cross_context_supersession():
    s = _s()
    ctx_a = _ctx(s, "context A?")
    ctx_b = _ctx(s, "context B?")
    alt_a = _alt(s, ctx_a.record_id)
    ans = s.record_interaction(action=DISPOSITION_ANSWERED, content="a",
                               gap_context=PHYSICAL_FEASIBILITY)
    # withdrawal targeting a context declaration (cross-class)
    _refused(s, action=WDR, decision_context_root=ctx_a.record_id,
             supersedes=[ctx_a.record_id])
    # alternative refinement targeting a legacy answer (cross-class)
    _refused(s, action=ALT, content="x", decision_context_root=ctx_a.record_id,
             supersedes=[ans.record_id])
    # legacy correction targeting a decision record (cross-class, reverse)
    _refused(s, action=DISPOSITION_ANSWERED, content="x",
             gap_context=PHYSICAL_FEASIBILITY, supersedes=[alt_a.record_id])
    # cross-context: refinement/withdrawal claiming context B over A's chain
    _refused(s, action=ALT, content="x", decision_context_root=ctx_b.record_id,
             supersedes=[alt_a.record_id])
    _refused(s, action=WDR, decision_context_root=ctx_b.record_id,
             supersedes=[alt_a.record_id])


def test_seam3_single_target_and_withdrawal_shape():
    s = _s()
    ctx = _ctx(s)
    a1 = _alt(s, ctx.record_id, "alt one")
    a2 = _alt(s, ctx.record_id, "alt two")
    # multi-target decision supersession refused (ID-11)
    _refused(s, action=ALT, content="x", decision_context_root=ctx.record_id,
             supersedes=[a1.record_id, a2.record_id])
    _refused(s, action=WDR, decision_context_root=ctx.record_id,
             supersedes=[a1.record_id, a2.record_id])
    # withdrawal must supersede exactly one target
    _refused(s, action=WDR, decision_context_root=ctx.record_id)
    # context refinement multi-target refused
    ctx2 = _ctx(s, "another context?")
    _refused(s, action=CTX, content="x",
             supersedes=[ctx.record_id, ctx2.record_id])


# --- falsy-neutral gap linkage (repository-native neutral) -------------------

def test_decision_actions_carry_falsy_neutral_gap_linkage():
    s = _s()
    ctx = _ctx(s)
    alt = _alt(s, ctx.record_id)
    for r in (ctx, alt):
        assert r.resolves_gap is False        # repository-native falsy neutral
        assert r.contradicts == []
        assert r.gap_context is None
        assert r.pending is None
