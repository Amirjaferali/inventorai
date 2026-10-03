# -*- coding: utf-8 -*-
"""STAGE 20 — ASSUMPTION REVISION & REPLACEMENT — CLOSURE (Owner-authorized).

What is pinned, over the real engine, the real durable store and the real web
routes:

* two explicit Owner actions on ONE of the inventor's own ACTIVE provisional
  assumptions — ``revise_assumption`` (a new `provisional_assumption`) and
  ``replace_with_answer`` (a new `answered` record) — each a canonical
  ``supersedes=[target]`` successor inheriting the target's gap and question
  target verbatim, OWNER_STATED / UNVALIDATED, the old assumption kept as
  history, dependencies deactivated without transfer;
* the deep-copy staging (no live inverse edge before the durable commit), the
  closed action vocabulary, authenticity before the committed-retry lookup, the
  exact committed retry after the target became superseded, action-separated
  identities without live iteration, and truthful recovery (saved-but-not-
  applied is never upgraded);
* reconstruction: ordinary ancestry replays exactly as before; a VALID
  assumption-origin answer runs the UNCHANGED ``run_iteration`` at its own
  durable position only when its gap exists, ``select_next_gap`` selects it and
  its exact question is not an outstanding routed need — otherwise it is skipped
  there (no progression), reported, and still counted under the replay bound;
  a MALFORMED assumption ancestry fails the whole reconstruction closed;
* routing: Replace is refused for a note on an outstanding routed question;
* risk: a skipped replacement does not itself revoke ACCEPTED_RISK.

A skipped replacement is NOT claimed to leave everything unchanged: ledger-
derived views legitimately recompute from the restored active ledger.
Neutral synthetic fixtures only; no study corpus.
"""
import copy
import html as _html
import inspect
import io
import os
import re

import pytest

import engine.progression_loop as pl
import engine.session_reconstruction as SR
from engine import need_routing as nr
from engine.idea_state import (
    ACCEPTED_RISK, ANCESTRY_ASSUMPTION_ORIGIN, ANCESTRY_MALFORMED,
    ANCESTRY_ORDINARY, BOUNDARY_AMBIGUITY, CLOSED, Gap, IdeaState,
    LEGACY_UNSPECIFIED, MECHANISM_COMPLETENESS, OPEN, OWNER_STATED, PARTIAL, PHYSICAL_FEASIBILITY,
    UNVALIDATED, AssertionRecord, classify_assumption_ancestry,
    project_assumption_dependencies,
)
from engine.record_contract import ContractError
from engine.record_store import AssumptionSuccessorRejected, StoreError
from engine.requirement_landscape import derive_requirement_landscape
from web import ui_text
import web.app as appmod
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, PF_STRONG, BA_1, BA_2, NOTE, PF_Q2, ID, NR1, _start, _answer,
    _live, _store, _routed_form, _web_to_ba, _accept_pf_via_route,
)
from tests.test_cap08_assumption_dependency import _assume, _raw, _declare
from tests.test_stage19_durable_success_criteria import _restart

ROUTE = "/session/%s/assumption-action"
REVISED = "Assume the spring latch holds at least the deck load."
ANSWER = MECH
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_DOCS = os.path.join(_ROOT, "docs", "governance")


# ==========================================================================
# harness
# ==========================================================================
def _item(c, sid, rid):
    """(answer_token, binding, replace_offered, block) of ONE assumption's forms
    exactly as one render issues them; None when no item renders for it."""
    raw = _raw(c, sid)
    m = re.search(r'<div class="assumption-action-item" data-assumption-action="%s".*?'
                  r'(?=<div class="assumption-action-item"|</section>)' % rid, raw, re.S)
    if not m:
        return None
    f = m.group(0)
    tok = _html.unescape(re.search(r'name="answer_token" value="([^"]*)"', f).group(1))
    b = _html.unescape(re.search(r'name="assumption_binding" value="([^"]*)"', f).group(1))
    return tok, b, 'value="replace_with_answer"' in f, f


def _act(c, sid, rid, action, content, form=None, **over):
    form = form or _item(c, sid, rid)
    data = {"answer_token": form[0], "assumption_binding": form[1],
            "assumption_action": action, "content": content}
    data.update(over)
    r = c.post(ROUTE % sid, data=data)
    assert r.status_code in (302, 400), r.status_code
    return r


def _notice(sid):
    e = appmod.SESSION_STORE[sid]
    return e.pop("_interaction_ack", None), e.pop("_answer_error", None)


def _rows(sid):
    return list(_store().load_contract(sid).assertions)


def _active_assumptions(state):
    return [r for r in state.assertions
            if r.disposition == "provisional_assumption" and r.superseded_by is None]


def _progress(state):
    return (state.maturity_level, state.current_stage, state.iteration,
            [(g.gap_type, g.status, g.iterations_open) for g in state.gaps])


def _project_with_assumption(c, text="Assume the hinge pin carries the full deck load."):
    """A mechanical NR1 project with one answer and ONE provisional assumption on
    the CURRENT question (Mechanism Completeness, still the selected gap)."""
    sid = _start(c)
    _answer(c, sid, MECH)
    _assume(c, sid, text)
    [a] = _active_assumptions(_live(sid))
    return sid, a


def _recon(sid):
    return SR.reconstruct_readonly_state(_store(), sid)


def _append_raw(sid, record):
    _store().append_record(sid, record, idempotency_key=None)


def _rec(rid, disposition, content, gap, qt, supersedes=(), iteration=0,
         provenance=OWNER_STATED):
    return AssertionRecord(record_id=rid, disposition=disposition, content=content,
                           gap_context=gap, iteration=iteration,
                           provenance=provenance, validation_status=UNVALIDATED,
                           responsibility="OWNER_INPUT" if provenance == OWNER_STATED else None, supersedes=list(supersedes),
                           question_target=qt)


def _next_id(sid):
    return "rec_%d" % (max(int(r.record_id[4:]) for r in _rows(sid)) + 1)


def _resume(c, sid):
    _restart()
    c.get("/session/%s" % sid)
    r = c.post("/session/%s/resume" % sid)
    assert r.status_code == 302
    return _live(sid)


# ==========================================================================
# A. supersession: revise / replace
# ==========================================================================
def test_a01_revise_supersedes_append_only_and_changes_no_progression(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    before = _progress(_live(sid))
    calls = {"recon": 0, "qty": 0, "msnl": 0}
    real_recon, real_qty = appmod.reconstruct_readonly_state, appmod._attach_quantity_history
    monkeypatch.setattr(appmod, "reconstruct_readonly_state",
                        lambda *a_, **k: calls.__setitem__("recon", calls["recon"] + 1) or real_recon(*a_, **k))
    monkeypatch.setattr(appmod, "_attach_quantity_history",
                        lambda *a_, **k: calls.__setitem__("qty", calls["qty"] + 1) or real_qty(*a_, **k))
    monkeypatch.setattr(appmod, "_msnl_capture",
                        lambda **k: calls.__setitem__("msnl", calls["msnl"] + 1))
    form = _item(client, sid, a.record_id)
    calls.update(recon=0, qty=0, msnl=0)                 # the render itself is not the action
    _act(client, sid, a.record_id, "revise_assumption", REVISED, form=form)
    assert _notice(sid) == (appmod.ASSUMPTION_REVISED_ACK, None)
    assert calls == {"recon": 0, "qty": 0, "msnl": 0}
    state = _live(sid)
    old = next(r for r in state.assertions if r.record_id == a.record_id)
    [new] = _active_assumptions(state)
    assert (new.disposition, new.content, new.supersedes, new.gap_context,
            new.question_target, new.provenance, new.validation_status) == (
        "provisional_assumption", REVISED, [a.record_id], a.gap_context,
        a.question_target, OWNER_STATED, UNVALIDATED)
    assert old.superseded_by == new.record_id and old.content == a.content
    assert _progress(state) == before
    # durable truth: the old row is untouched history, the new row carries the edge
    durable = {r.record_id: r for r in _rows(sid)}
    assert durable[a.record_id].content == a.content
    assert durable[a.record_id].superseded_by == new.record_id
    assert durable[new.record_id].supersedes == [a.record_id]


def test_a02_replace_is_an_owner_stated_unvalidated_answer_at_its_new_position(client):
    sid, a = _project_with_assumption(client)
    _act(client, sid, a.record_id, "replace_with_answer", ANSWER)
    ack, err = _notice(sid)
    assert err is None and ack == appmod.ASSUMPTION_REPLACED_ACK
    rows = _rows(sid)
    new = rows[-1]                                      # its own NEW durable position
    assert (new.disposition, new.content, new.supersedes, new.gap_context,
            new.question_target, new.provenance, new.validation_status) == (
        "answered", ANSWER, [a.record_id], a.gap_context, a.question_target,
        OWNER_STATED, UNVALIDATED)
    state = _live(sid)
    assert not _active_assumptions(state)
    assert next(r for r in state.assertions if r.record_id == a.record_id).superseded_by \
        == new.record_id
    [outcome] = _recon(sid).review.assumption_origin_outcomes
    assert outcome.record_id == new.record_id and outcome.applied is True
    # live state IS the full deterministic reconstruction
    assert _progress(state) == _progress(_recon(sid).state)


def test_a03_deep_copy_staging_keeps_live_untouched_until_commit(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    live_target = next(r for r in _live(sid).assertions if r.record_id == a.record_id)
    seen = {}
    real = type(_store()).append_assumption_successor

    def spy(self, project_id, record, idempotency_key):
        seen["live_superseded_by"] = live_target.superseded_by
        raise StoreError("store unavailable")
    monkeypatch.setattr(type(_store()), "append_assumption_successor", spy)
    n = len(_rows(sid))
    for action, text in (("revise_assumption", REVISED), ("replace_with_answer", ANSWER)):
        _act(client, sid, a.record_id, action, text)
        assert _notice(sid) == (None, appmod.ASSUMPTION_ACTION_NOT_SAVED_MESSAGE)
        assert seen.pop("live_superseded_by") is None   # never mutated before commit
        assert live_target.superseded_by is None
        assert len(_rows(sid)) == n
    monkeypatch.setattr(type(_store()), "append_assumption_successor", real)
    src = inspect.getsource(appmod.assumption_action)
    assert "copy.deepcopy(r) for r in state.assertions" in src
    assert "list(state.assertions)" not in src


def test_a04_dependencies_deactivate_without_transfer(client):
    sid, a = _project_with_assumption(client)
    answered = [r.record_id for r in _live(sid).assertions if r.disposition == "answered"]
    _declare(client, sid, a.record_id, answered)
    proj = project_assumption_dependencies(_live(sid).assertions)
    assert proj.active_edges == ((a.record_id, answered[0]),)
    _act(client, sid, a.record_id, "revise_assumption", REVISED)
    state = _live(sid)
    [new] = _active_assumptions(state)
    proj = project_assumption_dependencies(state.assertions)
    assert proj.active_edges == ()                     # the old edge is inactive
    assert len(proj.declarations) == 1 and not proj.declarations[0].active
    assert all(new.record_id not in (d.assumption_record_id, d.dependent_answer_record_id)
               for d in proj.declarations)             # nothing transferred or inferred
    assert [r.record_id for r in state.assertions if r.disposition == "answered"
            and r.superseded_by is None] == answered   # dependent answers unchanged


def test_a05_target_must_be_an_active_provisional_assumption_with_a_gap(client):
    sid, a = _project_with_assumption(client)
    form = _item(client, sid, a.record_id)
    answered = next(r for r in _live(sid).assertions if r.disposition == "answered")
    n = len(_rows(sid))
    # a binding for another record is not issued by any render: forge-proof
    forged = appmod._issue_assumption_binding(
        sid, "x" + form[0], _live(sid), answered.record_id, ["revise_assumption"])
    _act(client, sid, a.record_id, "revise_assumption", REVISED,
         form=(form[0], forged, True, ""))
    assert _notice(sid)[1] == appmod.ASSUMPTION_ACTION_NOT_SAVED_MESSAGE
    # a correctly signed binding naming an answered record is refused (wrong disposition)
    signed = appmod._issue_assumption_binding(
        sid, form[0], _live(sid), answered.record_id, ["revise_assumption"])
    _act(client, sid, a.record_id, "revise_assumption", REVISED, form=(form[0], signed, True, ""))
    assert _notice(sid)[1] == appmod.ASSUMPTION_ACTION_NOT_SAVED_MESSAGE
    # unknown action and an action outside the binding fail closed
    _act(client, sid, a.record_id, "withdraw_assumption", REVISED)
    assert _notice(sid)[1] == appmod.ASSUMPTION_ACTION_NOT_SAVED_MESSAGE
    revise_only = appmod._issue_assumption_binding(
        sid, form[0], _live(sid), a.record_id, ["revise_assumption"])
    _act(client, sid, a.record_id, "replace_with_answer", ANSWER,
         form=(form[0], revise_only, False, ""))
    assert _notice(sid)[1] == appmod.ASSUMPTION_ACTION_NOT_SAVED_MESSAGE
    # empty content
    _act(client, sid, a.record_id, "revise_assumption", "   ")
    assert _notice(sid)[1] == appmod.ASSUMPTION_ACTION_INVALID_MESSAGE
    assert len(_rows(sid)) == n
    # ordinary /correct still refuses a provisional target (unchanged)
    r = client.post("/session/%s/correct" % sid, data={
        "answer_token": form[0], "supersedes_record_id": a.record_id, "response": ANSWER})
    assert r.status_code == 302 and len(_rows(sid)) == n


# ==========================================================================
# B. ancestry classification
# ==========================================================================
def _chain_state(*specs):
    """IdeaState whose ledger is minted through the canonical seam: each spec is
    (disposition, supersedes_index_or_None, gap, qt)."""
    s = IdeaState(idea_id="p")
    recs = []
    for disp, sup, gap, qt in specs:
        recs.append(s.record_interaction(
            disp, content=disp, gap_context=gap, question_target=qt,
            supersedes=[recs[sup].record_id] if sup is not None else None))
    return s, {r.record_id: r for r in s.assertions}, recs


def test_b01_valid_shapes_and_ordinary_corrections():
    g, q = PHYSICAL_FEASIBILITY, "PATHN:x"
    # assumption -> answer -> correction -> correction
    _s, by, r = _chain_state(("provisional_assumption", None, g, q), ("answered", 0, g, q),
                             ("answered", 1, g, q), ("answered", 2, g, q))
    assert [classify_assumption_ancestry(x, by) for x in r] == [ANCESTRY_ASSUMPTION_ORIGIN] * 4
    # assumption -> revision -> revision -> answer -> correction
    _s, by, r = _chain_state(("provisional_assumption", None, g, q),
                             ("provisional_assumption", 0, g, q),
                             ("provisional_assumption", 1, g, q),
                             ("answered", 2, g, q), ("answered", 3, g, q))
    assert classify_assumption_ancestry(r[-1], by) == ANCESTRY_ASSUMPTION_ORIGIN
    # legacy None question target throughout is valid
    _s, by, r = _chain_state(("provisional_assumption", None, g, None), ("answered", 0, g, None))
    assert classify_assumption_ancestry(r[-1], by) == ANCESTRY_ASSUMPTION_ORIGIN
    # ordinary answer and ordinary corrections: no assumption anywhere
    _s, by, r = _chain_state(("answered", None, g, q), ("answered", 0, g, q),
                             ("answered", 1, BOUNDARY_AMBIGUITY, q))
    assert [classify_assumption_ancestry(x, by) for x in r] == [ANCESTRY_ORDINARY] * 3


def test_b02_malformed_shapes():
    g, q = PHYSICAL_FEASIBILITY, "PATHN:x"
    _s, by, r = _chain_state(("provisional_assumption", None, g, q), ("answered", 0, g, q))
    r[1].gap_context = BOUNDARY_AMBIGUITY                    # gap mismatch
    assert classify_assumption_ancestry(r[1], by) == ANCESTRY_MALFORMED
    _s, by, r = _chain_state(("answered", None, g, q), ("provisional_assumption", 0, g, q),
                             ("answered", 1, g, q))           # answer before assumption
    assert classify_assumption_ancestry(r[2], by) == ANCESTRY_MALFORMED
    _s, by, r = _chain_state(("provisional_assumption", None, g, q), ("unknown", 0, g, q),
                             ("answered", 1, g, q))           # unsupported disposition
    assert classify_assumption_ancestry(r[2], by) == ANCESTRY_MALFORMED
    _s, by, r = _chain_state(("provisional_assumption", None, g, q), ("answered", 0, g, q))
    r[1].supersedes.append("rec_99")                          # ambiguous / dangling
    assert classify_assumption_ancestry(r[1], by) == ANCESTRY_MALFORMED
    _s, by, r = _chain_state(("provisional_assumption", None, None, q), ("answered", 0, None, q))
    assert classify_assumption_ancestry(r[1], by) == ANCESTRY_MALFORMED   # no gap


def test_b03_web_chains_reconstruct_and_only_the_active_member_replays(client):
    # assumption -> revision -> revision -> answer -> correction -> correction
    sid, a = _project_with_assumption(client)
    for text in (REVISED, REVISED + " (twice)"):
        [cur] = _active_assumptions(_live(sid))
        _act(client, sid, cur.record_id, "revise_assumption", text)
    [cur] = _active_assumptions(_live(sid))
    _act(client, sid, cur.record_id, "replace_with_answer", ANSWER)
    _notice(sid)
    for text in (ANSWER + " Corrected once.", ANSWER + " Corrected twice."):
        head = next(r for r in _live(sid).assertions
                    if r.disposition == "answered" and r.superseded_by is None
                    and r.gap_context == a.gap_context and r.supersedes)
        raw = _raw(client, sid)
        token = _html.unescape(re.search(r'name="answer_token" value="([^"]*)"', raw).group(1))
        client.post("/session/%s/correct" % sid, data={
            "answer_token": token, "supersedes_record_id": head.record_id, "response": text})
    recon = _recon(sid)
    state = recon.state
    chain = [r for r in state.assertions if r.gap_context == a.gap_context
             and (r.disposition == "provisional_assumption" or r.supersedes)]
    active = [r for r in chain if r.superseded_by is None]
    assert len(active) == 1 and active[0].content.endswith("Corrected twice.")
    by = {r.record_id: r for r in state.assertions}
    assert classify_assumption_ancestry(active[0], by) == ANCESTRY_ASSUMPTION_ORIGIN
    assert [o.record_id for o in recon.review.assumption_origin_outcomes] == [active[0].record_id]


def test_b04_ordinary_projects_reconstruct_exactly_as_before(client, monkeypatch):
    sid = _start(client)
    _answer(client, sid, MECH)
    _answer(client, sid, MECH)
    raw = _raw(client, sid)
    token = _html.unescape(re.search(r'name="answer_token" value="([^"]*)"', raw).group(1))
    first = next(r for r in _live(sid).assertions if r.disposition == "answered")
    client.post("/session/%s/correct" % sid, data={
        "answer_token": token, "supersedes_record_id": first.record_id, "response": MECH})
    seen = []
    real = pl.run_iteration
    monkeypatch.setattr(SR.progression_loop, "run_iteration",
                        lambda st, text: seen.append(text) or real(st, text))
    recon = _recon(sid)
    active = [r.content for r in recon.state.assertions
              if r.disposition == "answered" and r.superseded_by is None]
    assert recon.review.assumption_origin_outcomes == ()
    assert seen[1:] == active                            # every active answer, in seq order


# ==========================================================================
# C. malformed ancestry fails reconstruction closed
# ==========================================================================
def _malformed_project(client, mutate):
    sid, a = _project_with_assumption(client)
    rid = _next_id(sid)
    gap, qt = mutate(a)
    _append_raw(sid, _rec(rid, "answered", MECH, gap, qt, supersedes=[a.record_id]))
    return sid, a, rid


def test_c01_gap_mismatch_fails_the_reconstruction(client, monkeypatch):
    sid, a, rid = _malformed_project(client, lambda a: (BOUNDARY_AMBIGUITY, a.question_target))
    seen = []
    real = pl.run_iteration
    monkeypatch.setattr(SR.progression_loop, "run_iteration",
                        lambda st, text: seen.append(text) or real(st, text))
    with pytest.raises(SR.MalformedAssumptionAncestryError):
        _recon(sid)
    assert issubclass(SR.MalformedAssumptionAncestryError, ContractError)
    assert MECH not in seen[1:]                           # no positional fallback replay
    # durable rows untouched
    assert _rows(sid)[-1].record_id == rid and _rows(sid)[-1].gap_context == BOUNDARY_AMBIGUITY


def test_c02_unsupported_shape_fails_and_never_yields_a_writable_state(client):
    sid, a = _project_with_assumption(client)
    unknown_id = _next_id(sid)
    _append_raw(sid, _rec(unknown_id, "unknown", "", a.gap_context, a.question_target,
                          supersedes=[a.record_id], provenance=LEGACY_UNSPECIFIED))
    _append_raw(sid, _rec(_next_id(sid), "answered", MECH, a.gap_context, a.question_target,
                          supersedes=[unknown_id]))
    with pytest.raises(ContractError):
        _recon(sid)
    _restart()
    client.get("/session/%s" % sid)
    client.post("/session/%s/resume" % sid)
    assert getattr(_live(sid), "domain", None) is None   # never established as writable
    assert client.get("/session/%s/deliverable" % sid).status_code == 200


# ==========================================================================
# D. the applicability law (exact helper used by reconstruction)
# ==========================================================================
def _law_state(gaps, routed=()):
    s = IdeaState(idea_id="law")
    s.domain = "mechanical"
    s.current_stage = 2
    s.gaps = [Gap(gap_type=g, status=st, opened_at=0) for g, st in gaps]
    s.need_routing = [nr.NeedRoutingRevision(
        project_id="law", routing_seq=i, gap_type=g, question_id=q,
        after_assertion_seq=-1, operation=nr.OPERATION_ROUTE,
        required_input=nr.REQUIRED_INPUT_SPECIALIST, policy_ref="p",
        supersedes_seq=None, provenance=nr.ROUTING_PROVENANCE, event_key="k%d" % i)
        for i, (g, q) in enumerate(routed)]
    return s


def test_d01_applicability_law_reasons():
    law = SR.assumption_answer_skip_reason
    s = _law_state([(PHYSICAL_FEASIBILITY, OPEN)])
    assert pl.select_next_gap(s) == PHYSICAL_FEASIBILITY
    assert law(s, PHYSICAL_FEASIBILITY, ID("mechanical:PHYSICAL_FEASIBILITY:Q1")) is None
    assert law(s, BOUNDARY_AMBIGUITY, None) == SR.ASSUMPTION_SKIP_GAP_NOT_PRESENT
    for status in (CLOSED, ACCEPTED_RISK):
        s2 = _law_state([(PHYSICAL_FEASIBILITY, status), (BOUNDARY_AMBIGUITY, OPEN)])
        assert law(s2, PHYSICAL_FEASIBILITY, None) == "gap_status_" + status
    s3 = _law_state([(PHYSICAL_FEASIBILITY, OPEN), (BOUNDARY_AMBIGUITY, OPEN)])
    assert pl.select_next_gap(s3) == PHYSICAL_FEASIBILITY
    assert law(s3, BOUNDARY_AMBIGUITY, None) == SR.ASSUMPTION_SKIP_GAP_NOT_SELECTED
    # QUESTION-level routing inside an otherwise selected gap
    s4 = _law_state([(PHYSICAL_FEASIBILITY, OPEN)], routed=[(PHYSICAL_FEASIBILITY, PF_Q2)])
    assert pl.select_next_gap(s4) == PHYSICAL_FEASIBILITY     # Q1 still serves the gap
    assert law(s4, PHYSICAL_FEASIBILITY, ID(PF_Q2)) == SR.ASSUMPTION_SKIP_QUESTION_ROUTED
    assert law(s4, PHYSICAL_FEASIBILITY, ID("mechanical:PHYSICAL_FEASIBILITY:Q1")) is None
    assert law(s4, PHYSICAL_FEASIBILITY, None) == SR.ASSUMPTION_SKIP_QUESTION_ROUTED  # fail safe
    # the law never mutates (no gap is created, injected or retargeted)
    snap = copy.deepcopy([(g.gap_type, g.status) for g in s.gaps])
    law(s, BOUNDARY_AMBIGUITY, None)
    assert [(g.gap_type, g.status) for g in s.gaps] == snap


def test_d02_missing_historical_gap_is_skipped_never_created(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    target = _next_id(sid)
    _append_raw(sid, _rec(target, "provisional_assumption", "Assume the ramp fits a car boot.",
                          BOUNDARY_AMBIGUITY, ID("mechanical:BOUNDARY_AMBIGUITY:Q1")))
    state = _resume(client, sid)
    assert state.get_gap(BOUNDARY_AMBIGUITY) is None
    before = _progress(state)
    seen = []
    real = pl.run_iteration
    monkeypatch.setattr(SR.progression_loop, "run_iteration",
                        lambda st, text: seen.append(text) or real(st, text))
    _act(client, sid, target, "replace_with_answer", BA_1)
    assert _notice(sid) == (appmod.ASSUMPTION_REPLACED_SKIPPED_ACK, None)
    state = _live(sid)
    assert BA_1 not in seen                               # no progression iteration for it
    assert state.get_gap(BOUNDARY_AMBIGUITY) is None      # never created
    assert _progress(state) == before                     # incl. state.iteration
    [o] = _recon(sid).review.assumption_origin_outcomes
    assert (o.applied, o.reason) == (False, SR.ASSUMPTION_SKIP_GAP_NOT_PRESENT)
    new = _rows(sid)[-1]
    assert new.disposition == "answered" and new.superseded_by is None   # still active truth
    assert new.iteration == before[2]                     # historical metadata kept


def test_d03_closed_historical_gap_is_skipped_and_stays_closed(client):
    sid, a = _project_with_assumption(client)              # assumption on MECHANISM
    _answer(client, sid, MECH)
    state = _live(sid)
    assert state.get_gap(MECHANISM_COMPLETENESS).status == CLOSED
    before = _progress(state)
    _act(client, sid, a.record_id, "replace_with_answer", MECH + " (my answer)")
    assert _notice(sid)[0] == appmod.ASSUMPTION_REPLACED_SKIPPED_ACK
    state = _live(sid)
    assert state.get_gap(MECHANISM_COMPLETENESS).status == CLOSED
    assert _progress(state) == before
    [o] = _recon(sid).review.assumption_origin_outcomes
    assert o.reason == "gap_status_CLOSED"


# ==========================================================================
# E. chronology, replay bound, iteration, ledger-derived consequences
# ==========================================================================
def test_e01_skipped_answer_counts_under_the_replay_bound(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    _answer(client, sid, MECH)
    _act(client, sid, a.record_id, "replace_with_answer", MECH + " (skip me)")
    answered = [r for r in _rows(sid) if r.disposition == "answered"]
    assert _recon(sid).review.assumption_origin_outcomes[0].applied is False
    monkeypatch.setattr(SR, "MAX_ACCEPTED_ANSWER_REPLAY", len(answered) - 1)
    with pytest.raises(SR.ReconstructionReplayLimitError):
        _recon(sid)


def test_e02_routing_revisions_at_a_skipped_position_still_apply(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    _assume(client, sid, "Assume the hinge pin carries the full deck load.")
    [a] = _active_assumptions(_live(sid))
    _answer(client, sid, MECH)                            # MECHANISM closes
    _act(client, sid, a.record_id, "replace_with_answer", MECH + " (skip me)")
    _notice(sid)
    skipped_seq = len(_rows(sid)) - 1
    # a later committed RETRACT revision lands right after the skipped record
    head = _store().load_need_routing(sid)[-1]
    rev = nr.NeedRoutingRevision(
        project_id=sid, routing_seq=0, gap_type=head.gap_type, question_id=head.question_id,
        after_assertion_seq=0, operation=nr.OPERATION_RETRACT, required_input=None,
        policy_ref=head.policy_ref, supersedes_seq=head.routing_seq,
        provenance=nr.ROUTING_PROVENANCE, event_key="nr:test:retract")
    _store().append_need_routing(sid, rev)
    stored = _store().load_need_routing(sid)
    assert stored[-1].after_assertion_seq == skipped_seq
    recon = _recon(sid)
    assert recon.review.assumption_origin_outcomes[0].applied is False
    assert list(recon.state.need_routing) == list(stored)   # applied in durable order
    assert not nr.active_routes(recon.state)


def test_e03_skip_is_no_progression_but_ledger_views_may_recompute(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    _answer(client, sid, MECH)
    before_state = _live(sid)
    before = _progress(before_state)
    landscape_before = [r.requirement_id for r in
                        derive_requirement_landscape(before_state).requirements]
    seen = []
    real = pl.run_iteration
    monkeypatch.setattr(SR.progression_loop, "run_iteration",
                        lambda st, text: seen.append(text) or real(st, text))
    text = MECH + " (replacement)"
    _act(client, sid, a.record_id, "replace_with_answer", text)
    state = _live(sid)
    assert text not in seen and _progress(state) == before        # no progression ran
    landscape_after = [r.requirement_id for r in
                       derive_requirement_landscape(state).requirements]
    # a truthful ledger-derived recomputation: the assumption row is replaced by
    # the inventor's answer row (NOT asserted neutral)
    assert "req:assertion:%s" % a.record_id in landscape_before
    assert "req:assertion:%s" % a.record_id not in landscape_after
    assert landscape_after != landscape_before


# ==========================================================================
# F. routing boundary
# ==========================================================================
def test_f01_replace_of_a_routed_need_note_is_refused_revision_allowed(client):
    sid = _start(client)
    _web_to_ba(client, sid)
    form = _routed_form(client, sid)
    client.post(f"/session/{sid}", data=dict(form, action="provisional_assumption",
                                              response=NOTE), answer_binding=False)
    [note] = _active_assumptions(_live(sid))
    assert note.question_target == ID(PF_Q2)
    item = _item(client, sid, note.record_id)
    assert item[2] is False and 'data-assumption-replace-unavailable="routed"' in item[3]
    n = len(_rows(sid))
    forged = appmod._issue_assumption_binding(
        sid, item[0], _live(sid), note.record_id,
        ["replace_with_answer", "revise_assumption"])
    _act(client, sid, note.record_id, "replace_with_answer", PF_STRONG,
         form=(item[0], forged, True, ""))
    assert _notice(sid) == (None, appmod.ASSUMPTION_REPLACE_ROUTED_MESSAGE)
    assert len(_rows(sid)) == n                           # zero writes
    before = _progress(_live(sid))
    _act(client, sid, note.record_id, "revise_assumption", NOTE + " Revised.")
    assert _notice(sid)[0] == appmod.ASSUMPTION_REVISED_ACK
    [rev] = _active_assumptions(_live(sid))
    assert rev.question_target == ID(PF_Q2) and _progress(_live(sid)) == before
    assert nr.gap_has_outstanding_routing(_live(sid), PHYSICAL_FEASIBILITY)


def test_f02_unreadable_committed_routing_fails_closed(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    monkeypatch.setattr(type(_store()), "committed_state_readable", lambda self: False)
    item = _item(client, sid, a.record_id)
    assert item[2] is False and 'data-assumption-replace-unavailable="unreadable"' in item[3]
    forged = appmod._issue_assumption_binding(
        sid, item[0], _live(sid), a.record_id, ["replace_with_answer", "revise_assumption"])
    n = len(_rows(sid))
    _act(client, sid, a.record_id, "replace_with_answer", ANSWER, form=(item[0], forged, True, ""))
    assert _notice(sid)[1] in (appmod.ASSUMPTION_ACTION_NOT_SAVED_MESSAGE,)
    assert len(_rows(sid)) == n


# ==========================================================================
# G. risk
# ==========================================================================
def test_g01_skipped_replacement_does_not_revoke_accepted_risk(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    _answer(client, sid, MECH)                            # PF served (Q1)
    assert pl.select_next_gap(_live(sid)) == PHYSICAL_FEASIBILITY
    _assume(client, sid, "Assume the steel rail is strong enough.")
    [a] = _active_assumptions(_live(sid))
    assert a.gap_context == PHYSICAL_FEASIBILITY and a.question_target != ID(PF_Q2)
    _answer(client, sid, PF_STRONG)
    assert pl.select_next_gap(_live(sid)) == BOUNDARY_AMBIGUITY
    _accept_pf_via_route(client, sid)
    assert _live(sid).get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    _act(client, sid, a.record_id, "replace_with_answer", PF_STRONG + " (mine)")
    ack, err = _notice(sid)
    assert err is None and ack == appmod.ASSUMPTION_REPLACED_SKIPPED_ACK
    state = _live(sid)
    assert state.get_gap(PHYSICAL_FEASIBILITY).status == ACCEPTED_RISK
    recon = _recon(sid)
    [o] = recon.review.assumption_origin_outcomes
    assert o.reason == "gap_status_ACCEPTED_RISK"
    assert all(oc.applied for oc in recon.review.risk_acceptance_outcomes)


# ==========================================================================
# H. idempotency and committed retry
# ==========================================================================
def test_h01_identity_is_action_separated_and_iteration_free():
    params = list(inspect.signature(appmod._assumption_action_key).parameters)
    assert params == ["sid", "action", "target_id", "gap_context", "question_target", "content"]
    k = appmod._assumption_action_key
    base = ("p", "revise_assumption", "rec_1", PHYSICAL_FEASIBILITY, None, "x")
    assert k(*base) != k("p", "replace_with_answer", *base[2:])        # same text, other action
    assert k(*base) != k(*base[:4], "", "x")                           # None != ""
    assert k(*base) != k(*base[:5], "y")
    src = inspect.getsource(appmod.assumption_action)
    assert "_assumption_action_key(sid, action, target_id, target.gap_context" in src


def test_h02_exact_committed_retry_after_the_target_is_superseded(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    form = _item(client, sid, a.record_id)
    _act(client, sid, a.record_id, "revise_assumption", REVISED, form=form)
    _notice(sid)
    n = len(_rows(sid))
    _act(client, sid, a.record_id, "revise_assumption", REVISED, form=form)
    assert _notice(sid) == (appmod.ASSUMPTION_REVISED_ACK, None)       # recognised, not stale
    assert len(_rows(sid)) == n
    # changed material under the same (now stale) form never writes
    _act(client, sid, a.record_id, "revise_assumption", REVISED + " Different.", form=form)
    assert _notice(sid)[1] == appmod.ASSUMPTION_ACTION_STALE_MESSAGE
    assert len(_rows(sid)) == n


def test_h03_committed_lookup_only_after_authenticity(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    calls = []
    real = type(_store()).committed_record_payload_for_idempotency_key
    monkeypatch.setattr(type(_store()), "committed_record_payload_for_idempotency_key",
                        lambda self, *x: calls.append(x) or real(self, *x))
    form = _item(client, sid, a.record_id)
    for bad in ({"answer_token": "nope"}, {"assumption_binding": form[1][:-2] + "00"},
                {"assumption_action": "withdraw"}):
        _act(client, sid, a.record_id, "revise_assumption", REVISED, form=form, **bad)
        assert _notice(sid)[1] == appmod.ASSUMPTION_ACTION_NOT_SAVED_MESSAGE
    assert calls == []
    _act(client, sid, a.record_id, "revise_assumption", REVISED, form=form)
    assert len(calls) == 1


def test_h04_replacement_retry_never_recaptures_or_upgrades(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    captured = []
    monkeypatch.setattr(appmod, "_msnl_capture", lambda **k: captured.append(k))
    form = _item(client, sid, a.record_id)
    _act(client, sid, a.record_id, "replace_with_answer", ANSWER, form=form)
    _notice(sid)
    assert len(captured) == 1 and captured[0]["correction_status"] == \
        appmod._msnl_shadow.CORRECTION_APPLIED
    live = appmod.SESSION_STORE[sid]["state"]
    _act(client, sid, a.record_id, "replace_with_answer", ANSWER, form=form)
    assert _notice(sid) == (appmod.ASSUMPTION_REPLACEMENT_RECORDED_ACK, None)
    assert len(captured) == 1                             # no second capture
    assert appmod.SESSION_STORE[sid]["state"] is live    # no republication


def test_h05_saved_not_applied_is_never_upgraded_by_a_retry(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    form = _item(client, sid, a.record_id)
    live = _live(sid)
    real = appmod.reconstruct_readonly_state

    def boom(*x, **k):
        raise SR.MalformedAssumptionAncestryError("x")
    monkeypatch.setattr(appmod, "reconstruct_readonly_state", boom)
    _act(client, sid, a.record_id, "replace_with_answer", ANSWER, form=form)
    assert _notice(sid) == (None, appmod.ASSUMPTION_REPLACEMENT_SAVED_NOT_APPLIED_MESSAGE)
    assert _live(sid) is live and _active_assumptions(live)    # live unchanged
    assert _rows(sid)[-1].disposition == "answered"            # the append stands
    monkeypatch.setattr(appmod, "reconstruct_readonly_state", real)   # now it would work
    _act(client, sid, a.record_id, "replace_with_answer", ANSWER, form=form)
    assert _notice(sid) == (None, appmod.ASSUMPTION_REPLACEMENT_SAVED_NOT_APPLIED_MESSAGE)
    assert _live(sid) is live


def test_h06_a_racing_identical_submission_is_answered_as_its_committed_retry(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    real = type(_store()).append_assumption_successor

    def sibling_first(self, project_id, record, idempotency_key):
        twin = copy.deepcopy(record)
        twin.record_id = record.record_id + "_twin"
        real(self, project_id, twin, idempotency_key)        # the sibling commits first
        return real(self, project_id, record, idempotency_key)
    monkeypatch.setattr(type(_store()), "append_assumption_successor", sibling_first)
    _act(client, sid, a.record_id, "revise_assumption", REVISED)
    # this request wrote nothing, but the identical event IS durably recorded
    assert _notice(sid) == (None, appmod.ASSUMPTION_REVISION_SAVED_NOT_SHOWN_MESSAGE)
    successors = [r for r in _rows(sid) if r.supersedes == [a.record_id]]
    assert [r.content for r in successors] == [REVISED]


# ==========================================================================
# I. recovery
# ==========================================================================
def test_i01_replay_bound_and_quantity_failures_after_commit(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    live = _live(sid)
    monkeypatch.setattr(SR, "MAX_ACCEPTED_ANSWER_REPLAY", 0)
    _act(client, sid, a.record_id, "replace_with_answer", ANSWER)
    assert _notice(sid) == (None, appmod.ASSUMPTION_REPLACEMENT_SAVED_NOT_APPLIED_MESSAGE)
    assert _live(sid) is live

    sid2, b = _project_with_assumption(client)
    live2 = _live(sid2)
    monkeypatch.setattr(SR, "MAX_ACCEPTED_ANSWER_REPLAY", 500)
    form = _item(client, sid2, b.record_id)
    monkeypatch.setattr(appmod, "_attach_quantity_history", lambda *x, **k: False)
    _act(client, sid2, b.record_id, "replace_with_answer", ANSWER, form=form)
    assert _notice(sid2) == (None, appmod.ASSUMPTION_REPLACEMENT_SAVED_NOT_APPLIED_MESSAGE)
    assert _live(sid2) is live2


def test_i02_quantity_prevalidation_failure_writes_nothing(client, monkeypatch):
    sid, a = _project_with_assumption(client)
    n = len(_rows(sid))

    def boom(self, *x):
        raise StoreError("unavailable")
    form = _item(client, sid, a.record_id)
    monkeypatch.setattr(type(_store()), "load_requirement_quantities", boom)
    _act(client, sid, a.record_id, "replace_with_answer", ANSWER, form=form)
    assert _notice(sid) == (None, appmod.ASSUMPTION_ACTION_NOT_SAVED_MESSAGE)
    assert len(_rows(sid)) == n and _active_assumptions(_live(sid))


def test_i03_in_transaction_revalidation_refuses_a_superseded_target(client):
    sid, a = _project_with_assumption(client)
    state = _live(sid)
    first = copy.deepcopy(state)
    rec1 = first.record_interaction("provisional_assumption", content="one",
                                    gap_context=a.gap_context, supersedes=[a.record_id],
                                    question_target=a.question_target)
    _store().append_assumption_successor(sid, rec1, idempotency_key="k" * 32)
    second = copy.deepcopy(state)
    rec2 = second.record_interaction("answered", content="two",
                                     gap_context=a.gap_context, supersedes=[a.record_id],
                                     question_target=a.question_target)
    rec2.record_id = _next_id(sid)
    with pytest.raises(AssumptionSuccessorRejected):
        _store().append_assumption_successor(sid, rec2, idempotency_key="j" * 32)
    bad = copy.deepcopy(state).record_interaction(
        "answered", content="x", gap_context=BOUNDARY_AMBIGUITY, question_target=a.question_target)
    bad.supersedes = [a.record_id]
    with pytest.raises(AssumptionSuccessorRejected):
        _store().append_assumption_successor(sid, bad, idempotency_key="h" * 32)


# ==========================================================================
# J. resume parity
# ==========================================================================
def test_j01_cold_and_writable_resume_preserve_classifications_and_ledger(client):
    sid, a = _project_with_assumption(client)
    _act(client, sid, a.record_id, "revise_assumption", REVISED)
    [rev] = _active_assumptions(_live(sid))
    _answer(client, sid, MECH)                           # MECHANISM closes
    _act(client, sid, rev.record_id, "replace_with_answer", MECH + " (skip me)")
    _notice(sid)
    live = _live(sid)
    live_ledger = [(r.record_id, r.disposition, r.superseded_by, r.supersedes)
                   for r in live.assertions]
    live_progress = _progress(live)
    cold = _recon(sid)
    resumed = _resume(client, sid)
    for st in (cold.state, resumed):
        assert [(r.record_id, r.disposition, r.superseded_by, r.supersedes)
                for r in st.assertions] == live_ledger
        assert _progress(st) == live_progress
    again = _recon(sid).review.assumption_origin_outcomes
    assert again == cold.review.assumption_origin_outcomes and again[0].applied is False


# ==========================================================================
# K. UX: EN / AR chrome, verbatim inventor text
# ==========================================================================
@pytest.mark.parametrize("lang", ("en", "ar"))
def test_k01_section_renders_localized_chrome_and_verbatim_text(client, lang):
    text = "Assume the hinge <pin> & latch hold."
    sid, a = _project_with_assumption(client, text=text)
    client.post("/ui-language", data={"lang": lang})
    raw = _html.unescape(_raw(client, sid))
    block = raw[raw.index('id="assumption-actions"'):]
    block = block[:block.index("</section>")]
    for key in ("UI_S20_HEADING", "UI_S20_EXPLAIN", "UI_S20_REVISE_SUMMARY",
                "UI_S20_REPLACE_SUMMARY", "UI_S20_REVISE_BUTTON", "UI_S20_REPLACE_BUTTON"):
        assert ui_text.UI_STRINGS[key][lang] in block, key
    assert text in block
    _act(client, sid, a.record_id, "revise_assumption", REVISED)
    raw = _html.unescape(_raw(client, sid))
    assert ui_text.localize_deep(appmod.ASSUMPTION_REVISED_ACK, lang) in raw
    for key in [k for k in ui_text.UI_STRINGS if k.startswith("UI_S20_")]:
        assert ui_text.UI_STRINGS[key]["en"] and re.search(
            r"[؀-ۿ]", ui_text.UI_STRINGS[key]["ar"]), key
    for msg in (appmod.ASSUMPTION_ACTION_NOT_SAVED_MESSAGE, appmod.ASSUMPTION_ACTION_STALE_MESSAGE,
                appmod.ASSUMPTION_REPLACE_ROUTED_MESSAGE, appmod.ASSUMPTION_ACTION_UNKNOWN_MESSAGE,
                appmod.ASSUMPTION_ACTION_INVALID_MESSAGE,
                appmod.ASSUMPTION_REVISION_SAVED_NOT_SHOWN_MESSAGE,
                appmod.ASSUMPTION_REPLACEMENT_SAVED_NOT_APPLIED_MESSAGE):
        assert ui_text.localize_message(msg, "ar") != msg, msg
    for ack in (appmod.ASSUMPTION_REVISED_ACK, appmod.ASSUMPTION_REPLACED_ACK,
                appmod.ASSUMPTION_REPLACED_SKIPPED_ACK, appmod.ASSUMPTION_REPLACEMENT_RECORDED_ACK):
        assert ui_text.localize_deep(ack, "ar") != ack, ack


def test_k02_truthful_copy_claims_no_validation_or_resolution():
    for text in (appmod.ASSUMPTION_REVISED_ACK, appmod.ASSUMPTION_REPLACED_ACK,
                 appmod.ASSUMPTION_REPLACED_SKIPPED_ACK, appmod.ASSUMPTION_REPLACEMENT_RECORDED_ACK):
        low = text.lower()
        for bad in ("validated.", "is resolved", "was resolved", "confirmed", "rejected",
                    "applied to progression"):
            assert bad not in low.replace("not been validated.", "").replace(
                "remains unvalidated.", ""), (bad, text)
    skipped = appmod.ASSUMPTION_REPLACED_SKIPPED_ACK
    assert "not replayed for progression" in skipped and "remains unvalidated" in skipped
    assert "unchanged" not in skipped.lower()


# ==========================================================================
# L. Stage-20 closure truth
# ==========================================================================
_COMPLETE = "STAGE 20: COMPLETE — CURRENT OWNER-DECLARED ASSUMPTION SCOPE"
_DELIVERED = "STAGE 20 CLOSURE: DELIVERED"
# The later Owner-authorized Stage 21 and Stage 22 closures moved the marker on to Stage 23 (navigation only); the
# Stage-20 completion and the "no Stage-21 implementation by the Stage-20 closure" fact stay true history.
# The later Owner-authorized Stage 23 closure (no product change) moved the marker on to Stage 24 (navigation only);
# the later delivered CAP-12 Form Mock-up Advisory Slice 1 entered Stage 24 as ENTERED / PARTIAL (marker unchanged).
_MARKER = "MASTER ROADMAP SEQUENTIAL MARKER: STAGE 24 — ENTERED / PARTIAL — NAVIGATION ONLY"
_NO_S21 = "NO STAGE-21 IMPLEMENTATION AUTHORIZED BY STAGE-20 CLOSURE"


def _doc(name):
    with io.open(os.path.join(_DOCS, name), encoding="utf-8") as fh:
        return re.sub(r"\s+", " ", fh.read())


def test_l01_closure_truth_on_every_current_surface():
    surfaces = {"CLAUDE.md": re.sub(r"\s+", " ", io.open(os.path.join(_ROOT, "CLAUDE.md"),
                                                          encoding="utf-8").read())}
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "CURRENT_PROJECT_STATE.md",
                 "INVENTORAI_MASTER_EXECUTION_ROADMAP.md",
                 "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md",
                 "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"):
        surfaces[name] = _doc(name)
    for name, text in surfaces.items():
        for token in (_COMPLETE, _MARKER, "FULL CAP-08: NOT AUTHORIZED"):
            assert token in text, (name, token)
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "INVENTORAI_MASTER_EXECUTION_ROADMAP.md",
                 "INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md", "INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md"):
        assert _NO_S21 in surfaces[name], name
    for name in ("ACTIVE_INCREMENT_CONTRACT.md", "CURRENT_PROJECT_STATE.md"):
        assert _DELIVERED in surfaces[name], name
    # the later Stage 21 closure took over the CLAUDE.md head; the Stage-20 delivery stays recorded there as history
    assert ("Stage 20 closure (delivered; completes Stage 20 for the current Owner-declared assumption scope"
            in surfaces["CLAUDE.md"])
    assert "**ACTIVE CONTRACT: NONE.**" in surfaces["CLAUDE.md"]
    assert "Assumption Revision & Replacement" not in _doc("OWNER_DECISION_REGISTER.md")


def test_l02_only_stage_20_is_newly_ticked():
    roadmap = io.open(os.path.join(_DOCS, "INVENTORAI_MASTER_EXECUTION_ROADMAP.md"),
                      encoding="utf-8").read()
    # Stages 21 and 22 were ticked later by their own Owner-authorized closures, not by this one
    for stage in (15, 18, 19, 20, 21, 22):
        assert re.search(r"^- \[x\] \*\*%d — " % stage, roadmap, re.M), stage
    # Stage 23 was ticked later by its own Owner-authorized closure (bounded four-axis scope, no product change)
    assert re.search(r"^- \[x\] \*\*23 — ", roadmap, re.M)
    for stage in (11, 13, 14, 16, 17, 24):
        assert re.search(r"^- \[ \] \*\*%d — " % stage, roadmap, re.M), stage
    flat = re.sub(r"\s+", " ", roadmap)
    for limit in ("FULL CAP-08: NOT AUTHORIZED", "FULL CAP-10: NOT AUTHORIZED"):
        assert limit in flat, limit
