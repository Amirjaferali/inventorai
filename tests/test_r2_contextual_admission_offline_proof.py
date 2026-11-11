# -*- coding: utf-8 -*-
"""R2 OFFLINE CONTEXTUAL ADMISSION PROOF — injected decisions only.

Owner-authorized offline proof of ONE corrected candidate rule. It is NOT a
method admission. There is no table, writer, provider call, network or
persisted decision, and no stamped or registered engine-contract version. The
proof covers the candidate rule only.

Decisions are injected in memory and composed, in this test only, at the
existing replay seam `_answer_replays_here` of `engine/session_reconstruction.py`.
Everything else is unchanged and runs for real: the real store and ledger, the
real `/correct` supersession, and the real canonical `run_iteration` /
`integrate_response`. A withheld or pending answer takes the existing XG1 path:
it stays saved, verbatim and in the ledger, is listed as unapplied and earns no
credit.

What is pinned (synthetic Mechanical ramp project, T2-G-4 contract):
  * unrelated-answer credit is withheld;
  * legitimate RELATED content keeps the incumbent's result exactly;
  * RELATED never overrides an incumbent rejection;
  * absent, UNCERTAIN, UNAVAILABLE and stale decisions give no credit;
  * corrupt decision evidence raises and is never read as absent;
  * context selection is acyclic (strictly earlier, active, admitted only);
  * a correction invalidates every dependent decision transitively;
  * production is unreachable, legacy replay is unchanged, and replay makes no
    provider call.
"""
import os
import socket
from types import SimpleNamespace

import pytest

import engine.session_reconstruction as sr
from engine import technical_orchestration_openai as toa
from engine.idea_state import MECHANISM_COMPLETENESS as MC
from tests.test_t2g_versioned_journey import (  # noqa: F401 — fixture reuse
    client, _login, _stamped_start, _answer, _correct, _active_answers, MECH_SEED)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T2G4 = sr.ENGINE_CONTRACT_VERSION_T2G4
METHOD = "r2-context-history-v1/offline-proof"

LEGIT = ("You pull it open, push the wheelchair up it, and a little hook at the "
         "top drops over the doorstep so it can't slide back down.")
LEGIT_2 = ("When you lift the far end, the hook comes free and the two halves "
           "fold together on the middle hinge so you can carry it by its handle.")
LEGIT_3 = ("The hinge pin runs through both halves, and the spring keeps the hook "
           "pressed down until you lift it with your thumb.")
OTHER = ("The bike light switches on by itself when it gets dark, and a light "
         "sensor tells a small board to make the lamp flash when I brake.")
UNDECIDED = ("I haven't decided whether the latch should be a spring catch or a "
             "magnet.")


# ─── no provider, no network: for every test in this module ───────────────────

@pytest.fixture(autouse=True)
def no_provider(monkeypatch):
    def refuse(*_a, **_k):
        raise AssertionError("the offline proof must not reach a provider or the network")
    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(toa, "_urllib_transport", refuse)


# ─── helpers ─────────────────────────────────────────────────────────────────

def _project(c, appmod, answers):
    sid = _stamped_start(c, appmod, T2G4, MECH_SEED, "mechanical")
    for text in answers:
        assert _answer(c, sid, text).status_code in (200, 302)
    return sid


def _sources(appmod, sid):
    store = appmod._get_store()
    seed = store.load_reconstruction_inputs(sid)["seed_idea_text"]
    return seed, list(store.load_contract(sid).assertions)


def _active(ledger):
    return [r for r in ledger
            if r.disposition == "answered" and r.superseded_by is None]


def _valid_decisions(seed, ledger, values, method=METHOD):
    """Decisions bound exactly as the candidate rule recomputes them: in ledger
    order, each against the latest earlier ADMITTED record. ``values`` maps a
    record id to a decision value; a missing id stays undecided."""
    out, context = {}, None
    for record in _active(ledger):
        value = values.get(record.record_id)
        if value is None:
            continue
        digest = sr.contextual_source_digest(method, seed, record, context)
        out[record.record_id] = sr.ContextualDecision(record.record_id, value, method, digest)
        if value == sr.CX_RELATED:
            context = record
    return out


def _view(state):
    return ([(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
            state.maturity_level,
            None if state.known_mechanism is None else state.known_mechanism.content)


def _incumbent(appmod, sid):
    appmod.SESSION_STORE.clear()
    return sr.reconstruct_readonly_state(appmod._get_store(), sid).state


def _composed(appmod, sid, monkeypatch, decisions):
    """Reconstruct with the candidate rule composed at the existing seam."""
    seed, ledger = _sources(appmod, sid)
    plan = sr.contextual_admission_plan(seed, ledger, decisions, METHOD)
    original = sr._answer_replays_here

    def composed(state, record, version):
        return (original(state, record, version)
                and plan[record.record_id].outcome == sr.CX_ADMITTED)
    with monkeypatch.context() as m:
        m.setattr(sr, "_answer_replays_here", composed)
        state = _incumbent(appmod, sid)
    return state, plan


def _unapplied(state):
    return set(getattr(state, sr.UNAPPLIED_ANSWERS_ATTR, ()))


# ==========================================================================
# 1. the real decision boundary
# ==========================================================================
def test_unrelated_answer_credit_is_withheld_and_the_answer_kept(client, monkeypatch):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, [OTHER])
    seed_only = _view(_incumbent(appmod, _project(c, appmod, [])))
    incumbent = _incumbent(appmod, sid)
    assert _view(incumbent) != seed_only                       # today: false credit
    assert incumbent.known_mechanism.content == OTHER
    seed, ledger = _sources(appmod, sid)
    rec = _active(ledger)[0]
    state, plan = _composed(appmod, sid, monkeypatch,
                            _valid_decisions(seed, ledger, {rec.record_id: sr.CX_UNRELATED}))
    assert plan[rec.record_id].outcome == sr.CX_WITHHELD
    assert _view(state) == seed_only                           # no credit at all
    assert _unapplied(state) == {rec.record_id}
    kept = [r for r in state.assertions if r.record_id == rec.record_id]
    assert kept and kept[0].content == OTHER                   # recorded verbatim


def test_legitimate_related_content_keeps_the_incumbent_result(client, monkeypatch):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, [LEGIT])
    incumbent = _incumbent(appmod, sid)
    assert incumbent.get_gap(MC).status in ("PARTIAL", "CLOSED")
    seed, ledger = _sources(appmod, sid)
    rec = _active(ledger)[0]
    state, plan = _composed(appmod, sid, monkeypatch,
                            _valid_decisions(seed, ledger, {rec.record_id: sr.CX_RELATED}))
    assert plan[rec.record_id].outcome == sr.CX_ADMITTED
    assert _view(state) == _view(incumbent) and _unapplied(state) == set()


def test_related_never_overrides_an_incumbent_rejection(client, monkeypatch):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, [UNDECIDED])
    seed_only = _view(_incumbent(appmod, _project(c, appmod, [])))
    incumbent = _incumbent(appmod, sid)
    assert incumbent.known_mechanism is None                   # T2-G-4 rejects it
    seed, ledger = _sources(appmod, sid)
    rec = _active(ledger)[0]
    state, plan = _composed(appmod, sid, monkeypatch,
                            _valid_decisions(seed, ledger, {rec.record_id: sr.CX_RELATED}))
    assert plan[rec.record_id].outcome == sr.CX_ADMITTED
    assert _view(state) == _view(incumbent)                    # still the incumbent's no
    assert state.known_mechanism is None
    assert [s[1] for s in _view(state)[0]] == [s[1] for s in seed_only[0]]


@pytest.mark.parametrize("text", [OTHER, LEGIT])
@pytest.mark.parametrize("kind, reason", [
    ("absent", sr.CX_REASON_ABSENT), ("uncertain", sr.CX_REASON_UNCERTAIN),
    ("unavailable", sr.CX_REASON_UNAVAILABLE), ("stale_digest", sr.CX_REASON_STALE),
    ("stale_method", sr.CX_REASON_STALE)])
def test_no_valid_related_decision_gives_no_credit(client, monkeypatch, text, kind, reason):
    """Conservative for every non-admitting state: even a legitimate answer stays
    pending (no credit) until it holds a valid RELATED decision."""
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, [text])
    seed_only = _view(_incumbent(appmod, _project(c, appmod, [])))
    seed, ledger = _sources(appmod, sid)
    rec = _active(ledger)[0]
    if kind == "absent":
        decisions = {}
    elif kind in ("uncertain", "unavailable"):
        decisions = _valid_decisions(seed, ledger, {rec.record_id: kind.upper()})
    elif kind == "stale_digest":
        decisions = {rec.record_id: sr.ContextualDecision(
            rec.record_id, sr.CX_RELATED, METHOD, "0" * 64)}
    else:
        decisions = _valid_decisions(seed, ledger, {rec.record_id: sr.CX_RELATED},
                                     method="another-method")
    state, plan = _composed(appmod, sid, monkeypatch, decisions)
    assert (plan[rec.record_id].outcome, plan[rec.record_id].reason) == (sr.CX_PENDING, reason)
    assert _view(state) == seed_only and _unapplied(state) == {rec.record_id}


@pytest.mark.parametrize("corrupt", [
    lambda rid: {rid: sr.ContextualDecision(rid, "MAYBE", METHOD, "0" * 64)},
    lambda rid: {rid: sr.ContextualDecision(rid, sr.CX_RELATED, "", "0" * 64)},
    lambda rid: {rid: sr.ContextualDecision("rec_999", sr.CX_RELATED, METHOD, "0" * 64)},
    lambda rid: {"rec_999": sr.ContextualDecision("rec_999", sr.CX_RELATED, METHOD, "0" * 64)},
    lambda rid: {rid: {"decision": sr.CX_RELATED}},
])
def test_corrupt_decision_evidence_raises_and_is_never_read_as_absent(client, corrupt):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, [LEGIT])
    seed, ledger = _sources(appmod, sid)
    with pytest.raises(sr.ContextualDecisionError):
        sr.contextual_admission_plan(seed, ledger, corrupt(_active(ledger)[0].record_id), METHOD)


# ==========================================================================
# 2. acyclic context selection and transitive invalidation
# ==========================================================================
def test_withheld_answers_never_become_context_and_substitution_is_stale(client, monkeypatch):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, [LEGIT, OTHER, LEGIT_2])
    seed, ledger = _sources(appmod, sid)
    a1, a2, a3 = _active(ledger)
    values = {a1.record_id: sr.CX_RELATED, a2.record_id: sr.CX_UNRELATED,
              a3.record_id: sr.CX_RELATED}
    plan = sr.contextual_admission_plan(seed, ledger, _valid_decisions(seed, ledger, values),
                                        METHOD)
    assert [plan[r.record_id].context_record_id for r in (a1, a2, a3)] == \
        [None, a1.record_id, a1.record_id]                    # the withheld a2 is skipped
    assert [plan[r.record_id].outcome for r in (a1, a2, a3)] == \
        [sr.CX_ADMITTED, sr.CX_WITHHELD, sr.CX_ADMITTED]
    # a decision bound to the withheld answer as context is an unverified substitution
    forged = dict(_valid_decisions(seed, ledger, values))
    forged[a3.record_id] = sr.ContextualDecision(
        a3.record_id, sr.CX_RELATED, METHOD, sr.contextual_source_digest(METHOD, seed, a3, a2))
    plan = sr.contextual_admission_plan(seed, ledger, forged, METHOD)
    assert (plan[a3.record_id].outcome, plan[a3.record_id].reason) == \
        (sr.CX_PENDING, sr.CX_REASON_STALE)
    state, _ = _composed(appmod, sid, monkeypatch, forged)
    assert {a2.record_id, a3.record_id} <= _unapplied(state)


def test_a_correction_invalidates_every_dependent_decision_transitively(client, monkeypatch):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, [LEGIT, LEGIT_2, LEGIT_3])
    seed, ledger = _sources(appmod, sid)
    a1, a2, a3 = _active(ledger)
    old = _valid_decisions(seed, ledger, {r.record_id: sr.CX_RELATED for r in (a1, a2, a3)})
    plan = sr.contextual_admission_plan(seed, ledger, old, METHOD)
    assert [plan[r.record_id].context_record_id for r in (a1, a2, a3)] == \
        [None, a1.record_id, a2.record_id]                    # a chain a1 <- a2 <- a3
    # the inventor corrects the FIRST answer through the existing /correct path
    assert _correct(c, sid, a1.record_id, LEGIT.replace("doorstep", "kerb")).status_code == 302
    seed, ledger = _sources(appmod, sid)
    successor = [r for r in _active(ledger) if a1.record_id in r.supersedes][0]
    plan = sr.contextual_admission_plan(seed, ledger, old, METHOD)
    assert a1.record_id not in plan                            # superseded: inert
    assert {rid: (p.outcome, p.reason) for rid, p in plan.items()} == {
        a2.record_id: (sr.CX_PENDING, sr.CX_REASON_STALE),     # its source changed
        a3.record_id: (sr.CX_PENDING, sr.CX_REASON_STALE),     # transitively
        successor.record_id: (sr.CX_PENDING, sr.CX_REASON_ABSENT)}
    state, _ = _composed(appmod, sid, monkeypatch, old)
    assert {a2.record_id, a3.record_id, successor.record_id} <= _unapplied(state)
    assert state.known_mechanism is None                       # nothing is credited
    # reassessed in dependency order, every answer is admitted again
    fresh = _valid_decisions(seed, ledger, {r.record_id: sr.CX_RELATED for r in _active(ledger)})
    plan = sr.contextual_admission_plan(seed, ledger, fresh, METHOD)
    assert {p.outcome for p in plan.values()} == {sr.CX_ADMITTED}
    assert plan[a2.record_id].context_record_id is None        # a1 is gone, nothing earlier
    assert plan[successor.record_id].context_record_id == a3.record_id


def _rec(i, content, superseded_by=None, disposition="answered"):
    return SimpleNamespace(record_id="rec_%d" % i, disposition=disposition,
                           gap_context=MC, question_target=None, content=content,
                           superseded_by=superseded_by, supersedes=[])


def test_bounded_histories_are_acyclic_and_ordered():
    """A bounded synthetic history mixing answers, non-answers, superseded
    records and every decision value: each context is strictly earlier, active
    and admitted, never the record itself, and the plan is deterministic."""
    values = [sr.CX_RELATED, sr.CX_UNRELATED, None, sr.CX_UNCERTAIN, sr.CX_RELATED,
              sr.CX_UNAVAILABLE, sr.CX_RELATED, sr.CX_RELATED, None, sr.CX_RELATED]
    ledger = []
    for i in range(12):
        if i == 3:
            ledger.append(_rec(i, "unknown", disposition="unknown"))
        elif i == 5:
            ledger.append(_rec(i, "replaced", superseded_by="rec_11"))
        else:
            ledger.append(_rec(i, "answer %d" % i))
    active = _active(ledger)
    decided = {r.record_id: v for r, v in zip(active, values) if v is not None}
    decisions = _valid_decisions("seed", ledger, decided)
    plan = sr.contextual_admission_plan("seed", ledger, decisions, METHOD)
    assert plan == sr.contextual_admission_plan("seed", ledger, decisions, METHOD)
    position = {r.record_id: i for i, r in enumerate(ledger)}
    assert set(plan) == {r.record_id for r in active}
    for rid, entry in plan.items():
        ctx = entry.context_record_id
        if ctx is not None:
            assert ctx != rid and position[ctx] < position[rid]
            assert plan[ctx].outcome == sr.CX_ADMITTED
    # changing an earlier admitted source makes every later decision stale
    ledger[0] = _rec(0, "answer 0, changed")
    plan = sr.contextual_admission_plan("seed", ledger, decisions, METHOD)
    assert all(e.outcome == sr.CX_PENDING and e.reason in (sr.CX_REASON_STALE,
                                                           sr.CX_REASON_ABSENT)
               for e in plan.values())


# ==========================================================================
# 3. production unreachable, legacy unchanged
# ==========================================================================
def test_ordinary_replay_never_consults_the_candidate(client, monkeypatch):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _project(c, appmod, [OTHER, LEGIT])

    def boom(*_a, **_k):
        raise AssertionError("the candidate rule must not run in ordinary replay")
    for name in ("contextual_admission_plan", "contextual_source_digest"):
        monkeypatch.setattr(sr, name, boom)
    state = _incumbent(appmod, sid)
    assert state.known_mechanism is not None                   # the incumbent result


def test_no_runtime_module_references_the_candidate_and_no_contract_is_registered():
    names = ("contextual_admission_plan", "contextual_source_digest", "ContextualDecision",
             "CX_ADMITTED", "CX_CONTEXT_POLICY")
    for top in ("engine", "web", "scripts"):
        for base, _dirs, files in os.walk(os.path.join(ROOT, top)):
            for name in files:
                path = os.path.join(base, name)
                if not name.endswith(".py") or path.endswith(
                        os.path.join("engine", "session_reconstruction.py")):
                    continue
                with open(path, encoding="utf-8") as fh:
                    text = fh.read()
                assert not any(n in text for n in names), path
    assert sr.CURRENT_ENGINE_CONTRACT_VERSION == T2G4
    assert sr.GAP_BOUND_REPLAY_VERSIONS == (sr.ENGINE_CONTRACT_VERSION_XG1, T2G4)
    assert not any("context" in v or "cx" in v.split("-")
                   for v in sr.SUPPORTED_ENGINE_CONTRACT_VERSIONS)
