"""CAP-10 Slice 1 (Stage 21) — inventor-declared contradiction between two
recorded answers.

Proves, over the real engine, the real durable store and the real web routes:

* one `contradiction_declared` record on the EXISTING ledger (OWNER_STATED,
  OWNER_INPUT, UNVALIDATED, neutral fields, a canonical two-endpoint pair) is
  the ONLY durable authority; the symmetric `contradicts` edges are a derived
  projection that is never written into an endpoint payload;
* chronological validation over durable order: declaration-then-correction is
  valid (the pair becomes inactive, nothing transfers, nothing is "resolved"),
  correction-then-declaration is refused — at load AND inside the append
  transaction (a concurrent correction wins cleanly);
* idempotent retries (restart, later supersession) and fail-closed conflicts;
* the existing consumers light up truthfully (landscape, cross-gap readiness,
  next step, validation plan, deliverable) with Owner attribution; the
  MULTIPLE_ALTERNATIVES serving trigger and gap / maturity / progression are
  unchanged; EN / AR copy is truthful.

Neutral synthetic fixtures only; no study corpus.
"""
import copy
import html as _html
import json
import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

import engine.progression_loop as pl
import engine.session_reconstruction as SR
from engine.decision_composition import declare_decision_context, declare_alternative
from engine.derived_readiness import derive_readiness
from engine.idea_development_outputs import derive_next_development_step
from engine.idea_state import (
    IdeaState, Gap, OPEN, MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY,
    BOUNDARY_AMBIGUITY, DISPOSITION_CONTRADICTION_DECLARED, OWNER_STATED,
    OWNER_INPUT, UNVALIDATED, LEGACY_UNSPECIFIED, SPECIALIST_REVIEWED,
    active_declared_contradiction_pairs,
)
from engine.record_contract import (
    ContractError, InvalidProvenanceError, InvalidReferenceError,
    InvalidValidationStatusError, ProjectRecordContract, assertion_from_dict,
    assertion_to_dict,
)
from engine.record_store import ContradictionDeclarationRejected, StoreError
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan
from web import ui_text
import web.app as appmod
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, PF_STRONG, BA_1, BA_2, ELEC_SEED, _start, _answer, _live,
    _store, _body, _facts,
)

DECL = DISPOSITION_CONTRADICTION_DECLARED
NOTE = "The latch cannot be both spring-loaded and tool-free."
FORBIDDEN = ("verified", "validated.", "resolved", "is wrong", "wins", "detected")


# ---------------------------------------------------------------------------
# engine helpers
# ---------------------------------------------------------------------------

def _ledger():
    s = IdeaState(idea_id="cap10")
    s.record_interaction("answered", "A: steel latch", gap_context=PHYSICAL_FEASIBILITY)
    s.record_interaction("answered", "B: no tools", gap_context=BOUNDARY_AMBIGUITY)
    s.record_interaction("answered", "C: spring pin", gap_context=PHYSICAL_FEASIBILITY)
    s.record_interaction("unknown", "", gap_context=BOUNDARY_AMBIGUITY)      # rec_4
    return s


def _envelope(records):
    return {"contract_version": "p4-0-record-contract-v1", "idea_id": "cap10",
            "assertions": records}


def _payloads(state):
    return [assertion_to_dict(r) for r in state.assertions]


def _load(records):
    return ProjectRecordContract.from_dict(_envelope(records))


def _decl_payload(pair, record_id="rec_9", **over):
    d = {"record_id": record_id, "disposition": DECL, "content": "", "gap_context": None,
         "iteration": 0, "provenance": OWNER_STATED, "validation_status": UNVALIDATED,
         "quality": None, "pending": None, "responsibility": OWNER_INPUT,
         "resolves_gap": False, "contradicts": [], "supersedes": [],
         "superseded_by": None, "decision_context_root": None,
         "question_target": None, "contradiction_endpoints": list(pair)}
    d.update(over)
    return d


# ===========================================================================
# 1-11: carrier + load rules
# ===========================================================================

def test_01_02_valid_declaration_is_normalized_owner_stated_and_neutral():
    s = _ledger()
    d = s.record_contradiction_declaration("rec_3", "rec_1", content=NOTE)
    assert d.contradiction_endpoints == ["rec_1", "rec_3"]          # canonical
    assert (d.disposition, d.provenance, d.responsibility, d.validation_status) \
        == (DECL, OWNER_STATED, OWNER_INPUT, UNVALIDATED)
    assert (d.gap_context, d.question_target, d.decision_context_root, d.quality,
            d.pending, d.resolves_gap, d.contradicts, d.supersedes, d.superseded_by) \
        == (None, None, None, None, None, False, [], [], None)
    assert d.content == NOTE                                        # verbatim
    a, c = s.assertions[0], s.assertions[2]
    assert a.contradicts == ["rec_3"] and c.contradicts == ["rec_1"]
    # selection order never makes a different relationship; numeric, not lexical
    s2 = _ledger()
    for _ in range(7):
        s2.record_interaction("answered", "x", gap_context=PHYSICAL_FEASIBILITY)
    assert s2.record_contradiction_declaration("rec_10", "rec_9").contradiction_endpoints \
        == ["rec_9", "rec_10"]
    # record_interaction can never mint it
    with pytest.raises(ValueError):
        _ledger().record_interaction(DECL, "x")


@pytest.mark.parametrize("a,b", [
    ("rec_1", "rec_1"),          # same endpoint
    ("rec_1", "rec_77"),         # unknown
    ("rec_1", "rec_4"),          # non-answer
    ("rec_1", "rec_01"), ("rec_1", "rec_0"), ("rec_1", "1"), ("rec_1", None),
])
def test_05_06_08_09_carrier_refuses_and_appends_nothing(a, b):
    s = _ledger()
    before = copy.deepcopy(s.assertions)
    with pytest.raises(ValueError):
        s.record_contradiction_declaration(a, b)
    assert s.assertions == before


def test_11_and_duplicate_carrier_refuses_superseded_or_repeated_pairs():
    s = _ledger()
    s.record_interaction("answered", "A2", gap_context=PHYSICAL_FEASIBILITY,
                         supersedes=["rec_1"])
    with pytest.raises(ValueError):
        s.record_contradiction_declaration("rec_1", "rec_2")      # already corrected
    s.record_contradiction_declaration("rec_2", "rec_3")
    with pytest.raises(ValueError):
        s.record_contradiction_declaration("rec_3", "rec_2")      # already active


def test_03_04_load_is_owner_stated_and_unvalidated_only():
    base = _payloads(_ledger())
    ok = _load(base + [_decl_payload(("rec_1", "rec_2"))])
    assert ok.assertions[-1].contradiction_endpoints == ["rec_1", "rec_2"]
    with pytest.raises(InvalidProvenanceError):
        _load(base + [_decl_payload(("rec_1", "rec_2"), provenance=LEGACY_UNSPECIFIED,
                                    responsibility=None)])
    with pytest.raises(InvalidValidationStatusError):
        _load(base + [_decl_payload(("rec_1", "rec_2"),
                                    validation_status=SPECIALIST_REVIEWED)])


@pytest.mark.parametrize("over", [
    {"gap_context": PHYSICAL_FEASIBILITY}, {"question_target": "PATHN:x"},
    {"contradicts": ["rec_1"]}, {"supersedes": ["rec_3"]}, {"quality": "REASONED"},
    {"resolves_gap": True}, {"pending": "specialist"},
    {"contradiction_endpoints": ["rec_1"]},
    {"contradiction_endpoints": ["rec_2", "rec_1"]},              # not canonical
    {"contradiction_endpoints": ["rec_1", "rec_x"]},              # malformed
    {"contradiction_endpoints": None},
])
def test_09_malformed_or_non_neutral_declarations_fail_closed(over):
    with pytest.raises(ContractError):
        _load(_payloads(_ledger()) + [_decl_payload(("rec_1", "rec_2"), **over)])


def test_06_07_08_10_reference_rules_fail_closed():
    base = _payloads(_ledger())
    for pair in (("rec_1", "rec_42"),      # unknown / foreign rec_N in this project
                 ("rec_1", "rec_4")):      # non-answer
        with pytest.raises(InvalidReferenceError):
            _load(base + [_decl_payload(pair)])
    # forward reference: the endpoint appears only AFTER the declaration
    with pytest.raises(InvalidReferenceError):
        _load(base[:1] + [_decl_payload(("rec_1", "rec_2"), record_id="rec_5")]
              + base[1:])
    # the endpoint pair is reserved for declarations
    with pytest.raises(InvalidReferenceError):
        _load([dict(base[0], contradiction_endpoints=None)] + base[1:])
    # nothing may supersede a declaration in Slice 1
    s = _ledger()
    s.record_contradiction_declaration("rec_1", "rec_2")
    bad = _payloads(s) + [dict(_payloads(s)[0], record_id="rec_6",
                               supersedes=["rec_5"])]
    with pytest.raises(InvalidReferenceError):
        _load(bad)


# ===========================================================================
# 12-19: chronology, supersession, projection, serialization
# ===========================================================================

def test_12_14_15_16_declaration_then_correction_is_valid_and_goes_inactive():
    s = _ledger()
    s.record_contradiction_declaration("rec_1", "rec_2", content=NOTE)
    s.record_interaction("answered", "A2", gap_context=PHYSICAL_FEASIBILITY,
                         supersedes=["rec_1"])                          # rec_6
    c = _load(_payloads(s))
    by = {r.record_id: r for r in c.assertions}
    assert by["rec_5"].disposition == DECL and by["rec_5"].content == NOTE  # historical
    assert by["rec_1"].superseded_by == "rec_6"
    assert active_declared_contradiction_pairs(c.assertions) == frozenset()
    assert by["rec_6"].contradicts == []                                  # no transfer
    assert by["rec_2"].contradicts == ["rec_1"]                           # history kept
    ids = [q.requirement_id for q in derive_requirement_landscape(c.to_state()).requirements]
    assert not any(i.startswith("req:contradiction:") for i in ids)


def test_13_correction_then_declaration_is_rejected_on_load():
    s = _ledger()
    s.record_interaction("answered", "A2", gap_context=PHYSICAL_FEASIBILITY,
                         supersedes=["rec_1"])                          # rec_5
    forged = _payloads(s) + [_decl_payload(("rec_1", "rec_2"), record_id="rec_6")]
    with pytest.raises(InvalidReferenceError):
        _load(forged)


def test_18_19_projection_never_becomes_durable_and_legacy_edges_still_load():
    s = _ledger()
    s.record_contradiction_declaration("rec_1", "rec_2")
    payloads = _payloads(s)
    assert payloads[0]["contradicts"] == [] and payloads[1]["contradicts"] == []
    assert all("contradiction_endpoints" not in p for p in payloads[:4])
    assert payloads[4]["contradiction_endpoints"] == ["rec_1", "rec_2"]
    # a stored copy of the projected edge would be a second truth source
    forged = copy.deepcopy(payloads)
    forged[0]["contradicts"] = ["rec_2"]
    forged[1]["contradicts"] = ["rec_1"]
    with pytest.raises(InvalidReferenceError):
        _load(forged)
    # a legitimate legacy edge between OTHER records keeps loading verbatim,
    # is not relabelled and fabricates no declaration
    legacy = _ledger()
    legacy.mark_contradiction("rec_1", "rec_3")
    loaded = _load(_payloads(legacy))
    assert loaded.assertions[0].contradicts == ["rec_3"]
    assert not any(r.disposition == DECL for r in loaded.assertions)
    row = [q for q in derive_requirement_landscape(loaded.to_state()).requirements
           if q.requirement_id == "req:contradiction:rec_1|rec_3"][0]
    assert row.primary_anchor.display_label == "Recorded contradiction"
    # re-serializing a loaded declared project round-trips byte-identically
    again = _load(payloads)
    assert ProjectRecordContract(idea_id="cap10", assertions=again.assertions) \
        .to_dict()["assertions"] == payloads
    # an older reader's payload shape (no endpoint key anywhere) is unchanged
    old = _payloads(_ledger())
    assert _payloads(_load(old).to_state()) == old


# ===========================================================================
# 26-35: consumers
# ===========================================================================

def _consumer_state(cross_gap=True):
    s = _ledger()
    s.record_contradiction_declaration("rec_1", "rec_2" if cross_gap else "rec_3",
                                       content=NOTE)
    return s


def test_26_27_landscape_row_once_attributed_and_declaration_not_an_answer():
    s = _consumer_state()
    reqs = derive_requirement_landscape(s).requirements
    ids = [r.requirement_id for r in reqs]
    assert ids.count("req:contradiction:rec_1|rec_2") == 1
    assert "req:assertion:rec_5" not in ids                  # declaration is not an answer
    assert "req:assertion:rec_1" not in ids and "req:assertion:rec_2" not in ids
    row = [r for r in reqs if r.requirement_id == "req:contradiction:rec_1|rec_2"][0]
    assert row.primary_anchor.display_label == "Contradiction you declared"
    assert "“A: steel latch”" in row.statement and "“B: no tools”" in row.statement
    assert "not been validated" in row.statement
    for bad in ("resolved", "wins", "is wrong", "must"):
        assert bad not in (row.statement + row.resolving_action.statement).lower()


def test_28_29_30_readiness_sees_active_conflicts_across_and_within_gaps():
    for cross in (True, False):
        s = _consumer_state(cross_gap=cross)
        r = derive_readiness(s)
        assert r._has_active_unresolved_contradiction(PHYSICAL_FEASIBILITY) is True
        if cross:
            assert r._has_active_unresolved_contradiction(BOUNDARY_AMBIGUITY) is True
    # historical (an endpoint corrected) no longer counts, in either gap
    s = _consumer_state()
    s.record_interaction("answered", "A2", gap_context=PHYSICAL_FEASIBILITY,
                         supersedes=["rec_1"])
    r = derive_readiness(s)
    assert r._has_active_unresolved_contradiction(PHYSICAL_FEASIBILITY) is False
    assert r._has_active_unresolved_contradiction(BOUNDARY_AMBIGUITY) is False
    assert r.overall_verified() is False                     # never awarded


def test_31_32_next_step_and_validation_plan_are_truthful():
    s = _consumer_state()
    step = derive_next_development_step(s)
    assert step.issue_type == "active_contradiction"
    text = " ".join(str(v) for v in (step.title, step.why_it_matters, step.next_action,
                                     step.sufficiency_condition, step.unlock_condition,
                                     step.remaining_uncertainty))
    assert "You declared" in text and "not been validated" in text
    assert "before the idea can advance" not in text
    assert "into one consistent" not in text
    plan = derive_validation_plan(s)
    st = [x for x in plan.steps if x.step_id == "vstep:req:contradiction:rec_1|rec_2"][0]
    assert st.evidence_category == "a correction of either conflicting answer"
    assert "reconciliation" not in st.closure_condition


def test_34_multiple_alternatives_trigger_ignores_the_declaration():
    s = IdeaState(idea_id="w2b")
    s.domain, s.domain_signal, s.path = "software", "software", "N"
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))
    s.record_interaction("answered", "a", gap_context=MECHANISM_COMPLETENESS)
    s.record_interaction("answered", "b", gap_context=MECHANISM_COMPLETENESS)
    ctx = declare_decision_context(s, "Which latch design should hold?")
    declare_alternative(s, "toggle latch", ctx.record_id)
    declare_alternative(s, "spring pin", ctx.record_id)
    fired = pl._alternatives_crossing_context(s)
    before = pl.compute_serving_decision(s, register_elevated=False)
    assert fired is not None and pl.TRIGGER_MULTIPLE_ALTERNATIVES in before.triggers
    s.record_contradiction_declaration("rec_1", "rec_2")
    assert pl._alternatives_crossing_context(s) == fired
    assert pl.compute_serving_decision(s, register_elevated=False) == before


# ===========================================================================
# web: 17, 20-25, 33, 35-44
# ===========================================================================

def _raw(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _token(c, sid):
    return _html.unescape(re.search(r'name="answer_token" value="([^"]*)"',
                                    _raw(c, sid)).group(1))


def _form(c, sid):
    """(answer_token, conflict_binding) exactly as ONE render of the page
    issues them; the binding is "" when no CAP-10 form is offered."""
    raw = _raw(c, sid)
    token = _html.unescape(re.search(r'name="answer_token" value="([^"]*)"', raw).group(1))
    m = re.search(r'name="conflict_binding" value="([^"]*)"', raw)
    return token, (_html.unescape(m.group(1)) if m else "")


def _declare(c, sid, endpoints, note=NOTE, confirm="yes", token=None, form=None,
             binding=None):
    if form is None:
        form = _form(c, sid)
    data = {"answer_token": token if token is not None else form[0],
            "conflict_binding": binding if binding is not None else form[1],
            "note": note, "endpoint": list(endpoints)}
    if confirm:
        data["conflict_confirm"] = confirm
    return c.post(f"/session/{sid}/declare-conflict", data=data)


def _rows(sid):
    return [json.loads(p) for (p,) in _store()._conn.execute(
        "SELECT payload FROM records WHERE project_id = ? ORDER BY seq", (sid,))]


def _declarations(sid):
    return [p for p in _rows(sid) if p["disposition"] == DECL]


def _web_project(c):
    sid = _start(c)
    for text in (MECH, MECH, PF_STRONG, BA_1):
        _answer(c, sid, text)
    answered = [r.record_id for r in _live(sid).assertions
                if r.disposition == "answered" and r.superseded_by is None]
    return sid, answered


def _progress(state):
    return (state.maturity_level, state.current_stage, state.iteration,
            [(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
            pl.select_next_gap(state), tuple(state.need_routing))


def test_17_33_35_36_38_web_declaration_end_to_end(client):
    sid, answered = _web_project(client)
    raw = _raw(client, sid)
    form = re.search(r'<details class="declare-conflict".*?</details>', raw, re.S).group(0)
    assert sorted(re.findall(r'name="endpoint" value="([^"]+)"', form)) == sorted(answered)
    lo, hi = answered[0], answered[-1]            # an MC answer and the PF answer
    before = _progress(_live(sid))
    assert _declare(client, sid, [hi, lo]).status_code == 302
    body = _body(client, sid)
    assert ui_text.text("UI_CAP10_ERR_NOT_SAVED", "en") not in body
    assert appmod.CONTRADICTION_DECLARED_ACK in body
    decl = _declarations(sid)
    assert len(decl) == 1 and decl[0]["contradiction_endpoints"] == [lo, hi]
    assert decl[0]["content"] == NOTE and decl[0]["provenance"] == OWNER_STATED
    # no endpoint row was rewritten
    assert all(p["contradicts"] == [] for p in _rows(sid))
    state = _live(sid)
    assert _progress(state) == before                  # 35: nothing progresses
    # 17: live == cold reconstruction == writable resume
    live = _facts(state)
    assert _facts(SR.reconstruct_readonly_state(_store(), sid).state) == live
    appmod.SESSION_STORE.pop(sid)
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _facts(_live(sid)) == live
    assert (lo, hi) in active_declared_contradiction_pairs(_live(sid).assertions)
    # 33: the deliverable carries the attributed row and never claims resolution
    deliv = _html.unescape(client.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    assert "Contradiction you declared" in deliv
    assert "You marked these two recorded answers as conflicting" in deliv
    assert "Two recorded answers you marked as conflicting" in _body(client, sid)
    # project record lists the declaration and the two steps it marks
    assert "Conflict you declared between two answers" in _body(client, sid)


def test_37_39_40_41_refusals_append_nothing(client):
    sid, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    rows = len(_rows(sid))
    cases = [
        dict(endpoints=[a, b], confirm=None),                  # no confirmation
        dict(endpoints=[a]), dict(endpoints=answered[:3]),    # not exactly two
        dict(endpoints=[a, a]), dict(endpoints=[a, "rec_x"]),  # same / malformed
        dict(endpoints=[a, "rec_999"]),                        # not in THIS project
        dict(endpoints=[a, b], token="forged.token"),          # forged token
        dict(endpoints=[a, b], binding=""),                    # no CAP-10 binding
    ]
    for case in cases:
        _declare(client, sid, **case)
        assert len(_rows(sid)) == rows, case
    # a token signed for ANOTHER project never verifies here
    other, _ = _web_project(client)
    _declare(client, sid, [a, b], form=_form(client, other))   # both from B
    _declare(client, sid, [a, b], binding=_form(client, other)[1])
    assert len(_rows(sid)) == rows
    # a non-answer endpoint (an explicit "not known yet") is refused
    client.post(f"/session/{sid}", data={
        "response": "", "action": "unknown", "answer_token": _token(client, sid)})
    unknown = [r.record_id for r in _live(sid).assertions if r.disposition == "unknown"]
    assert len(unknown) == 1
    rows = len(_rows(sid))
    _declare(client, sid, [a, unknown[0]])
    assert len(_rows(sid)) == rows
    # a stale endpoint (corrected after the form was rendered) is refused
    old_form = _form(client, sid)
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": a, "response": MECH, "answer_token": _token(client, sid)})
    rows = len(_rows(sid))
    _declare(client, sid, [a, b], form=old_form)
    assert len(_rows(sid)) == rows
    assert ui_text.text("UI_CAP10_ERR_STALE", "en") in _body(client, sid)
    # a current form no longer offers the corrected answer at all
    _declare(client, sid, [a, b])
    assert len(_rows(sid)) == rows


def test_20_21_22_23_42_idempotency(client):
    sid, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    form = _form(client, sid)
    _declare(client, sid, [a, b], form=form)
    _declare(client, sid, [b, a], form=form)                     # exact retry
    assert len(_declarations(sid)) == 1
    # same key, different material -> fail closed, nothing written
    _declare(client, sid, [a, b], note="another note", form=form)
    assert len(_declarations(sid)) == 1
    assert ui_text.text("UI_CAP10_ERR_NOT_SAVED", "en") in _body(client, sid)
    # retry after a restart
    appmod.SESSION_STORE.pop(sid)
    client.post(f"/session/{sid}/resume", data={})
    _declare(client, sid, [a, b], form=form)
    assert len(_declarations(sid)) == 1
    # retry after an endpoint was superseded: recognised, reactivates nothing
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": a, "response": MECH, "answer_token": _token(client, sid)})
    rows = len(_rows(sid))
    _declare(client, sid, [a, b], form=form)
    assert len(_rows(sid)) == rows
    assert active_declared_contradiction_pairs(_live(sid).assertions) == frozenset()
    assert appmod.CONTRADICTION_DECLARED_ACK in _body(client, sid)


def test_24_uncertain_or_failed_commits_never_claim_a_save(client, monkeypatch):
    sid, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    store = _store()
    real = type(store).append_contradiction_declaration

    def fail_before(self, *args, **kw):
        raise StoreError("unavailable")
    monkeypatch.setattr(type(store), "append_contradiction_declaration", fail_before)
    live_before = copy.deepcopy(_live(sid).assertions)
    _declare(client, sid, [a, b])
    assert _declarations(sid) == [] and _live(sid).assertions == live_before
    assert ui_text.text("UI_CAP10_ERR_NOT_SAVED", "en") in _body(client, sid)

    def commit_then_fail(self, *args, **kw):          # committed, outcome lost
        real(self, *args, **kw)
        raise StoreError("commit outcome unknown")
    monkeypatch.setattr(type(store), "append_contradiction_declaration", commit_then_fail)
    _declare(client, sid, [a, b])
    assert len(_declarations(sid)) == 1
    assert (a, b) in active_declared_contradiction_pairs(_live(sid).assertions)

    monkeypatch.setattr(type(store), "append_contradiction_declaration", fail_before)
    monkeypatch.setattr(type(store), "committed_record_payload_for_idempotency_key",
                        lambda self, *a, **k: (_ for _ in ()).throw(StoreError("x")))
    rows = len(_rows(sid))
    _declare(client, sid, [answered[1], b])
    assert len(_rows(sid)) == rows


def test_25_concurrent_correction_wins_inside_the_transaction(client):
    sid, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    state = _live(sid)
    minter = IdeaState(idea_id=state.idea_id)
    minter.assertions = copy.deepcopy(state.assertions)
    staged = minter.record_contradiction_declaration(a, b)        # checked pre-txn
    # a correction commits between the check and the append
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": a, "response": MECH, "answer_token": _token(client, sid)})
    staged.record_id = "rec_%d" % (len(_rows(sid)) + 1)
    rows = len(_rows(sid))
    with pytest.raises(ContradictionDeclarationRejected):
        _store().append_contradiction_declaration(sid, staged, idempotency_key="k" * 32)
    assert len(_rows(sid)) == rows
    with pytest.raises(sqlite3.IntegrityError):                   # key uniqueness
        ok = minter.record_contradiction_declaration(answered[1], b)
        ok.record_id = "rec_%d" % (len(_rows(sid)) + 1)
        _store().append_contradiction_declaration(sid, ok, idempotency_key="j" * 32)
        ok2 = copy.deepcopy(ok)
        ok2.record_id = "rec_%d" % (len(_rows(sid)) + 1)
        ok2.contradiction_endpoints = [answered[1], answered[2]]
        _store().append_contradiction_declaration(sid, ok2, idempotency_key="j" * 32)


def test_43_44_copy_is_truthful_in_english_and_arabic(client):
    keys = ("UI_CAP10_HEADING", "UI_CAP10_EXPLAIN", "UI_CAP10_SELECT", "UI_CAP10_NOTE",
            "UI_CAP10_CONFIRM", "UI_CAP10_BUTTON", "UI_CAP10_ERR_NOT_SAVED",
            "UI_CAP10_ERR_INVALID", "UI_CAP10_ERR_STALE", "UI_CAP10_ERR_UNKNOWN",
            "UI_T3A_EVENT_CONTRADICTION_DECLARED", "UI_T3A_DECLARES_CONFLICT")
    for key in keys:
        en, ar = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert en and ar and en != ar and re.search("[؀-ۿ]", ar)
        for bad in ("AI ", "detected", "verified", "is wrong", "wins"):
            assert bad not in en, (key, bad)
        for bad in ("تم التحقق", "معتمد", "الذكاء الاصطناعي"):
            assert bad not in ar, (key, bad)
    ack_ar = ui_text.localize_deep(appmod.CONTRADICTION_DECLARED_ACK, "ar")
    assert ack_ar != appmod.CONTRADICTION_DECLARED_ACK and "غير مُتحقَّق" in ack_ar
    sid = _start(client, lang="ar")
    for text in (MECH, MECH, PF_STRONG):
        _answer(client, sid, text)
    answered = [r.record_id for r in _live(sid).assertions if r.disposition == "answered"]
    body = _body(client, sid)
    assert ui_text.text("UI_CAP10_HEADING", "ar") in body
    _declare(client, sid, answered[:2])
    assert ack_ar in _body(client, sid)
    assert len(_declarations(sid)) == 1


def test_electronics_journey_is_unaffected_until_a_declaration(client):
    sid = _start(client, seed=ELEC_SEED, domain="electronics_electrical")
    assert _live(sid).need_routing == []
    assert 'class="declare-conflict"' not in _raw(client, sid)   # < two answers


# ===========================================================================
# Astra correction F1 — dedicated CAP-10 action binding and freshness
# ===========================================================================

def test_f1_a_generic_or_pre_context_answer_token_never_authorizes(client):
    sid = _start(client)
    early_token, early_binding = _form(client, sid)       # before any CAP-10 form
    assert early_binding == ""
    for text in (MECH, MECH, PF_STRONG, BA_1):
        _answer(client, sid, text)
    answered = [r.record_id for r in _live(sid).assertions if r.disposition == "answered"]
    rows = len(_rows(sid))
    # a generic answer token alone (current or obsolete) is refused
    current_token, current_binding = _form(client, sid)
    _declare(client, sid, answered[:2], token=current_token, binding="")
    _declare(client, sid, answered[:2], token=early_token, binding="")
    # the current binding never transfers to the obsolete token
    _declare(client, sid, answered[:2], token=early_token, binding=current_binding)
    assert len(_rows(sid)) == rows and _declarations(sid) == []
    # the correctly bound current form works
    _declare(client, sid, answered[:2])
    assert len(_declarations(sid)) == 1


def test_f1_b_binding_is_action_specific_and_commits_to_the_endpoint_set(client):
    sid, answered = _web_project(client)
    token, binding = _form(client, sid)
    raw = _raw(client, sid)
    answer_target = _html.unescape(
        re.search(r'name="answer_target" value="([^"]*)"', raw).group(1))
    rows = len(_rows(sid))
    # another signed action's material is not a CAP-10 binding ...
    _declare(client, sid, answered[:2], binding=answer_target)
    # ... and the CAP-10 binding is not an answer target
    client.post(f"/session/{sid}", data={
        "response": "x", "answer_token": token, "answer_target": binding},
        answer_binding=False)
    assert len(_rows(sid)) == rows
    # an endpoint outside the bound set, or a tampered bound set, fails closed
    _declare(client, sid, [answered[0], "rec_999"])
    body, _, sig = binding.rpartition(".")
    import base64
    data = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    data["e"] = data["e"] + ["rec_999"]
    forged = base64.urlsafe_b64encode(json.dumps(
        data, sort_keys=True, separators=(",", ":")).encode()).decode().rstrip("=")
    _declare(client, sid, [answered[0], "rec_999"], binding=forged + "." + sig)
    assert len(_rows(sid)) == rows and _declarations(sid) == []


def test_f1_c_a_stale_binding_cannot_create_a_new_declaration(client):
    sid, answered = _web_project(client)
    old = _form(client, sid)
    # the eligible set changes (a correction) after the form was rendered
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": answered[0], "response": MECH,
        "answer_token": _token(client, sid)})
    rows = len(_rows(sid))
    _declare(client, sid, [answered[1], answered[2]], form=old)
    assert len(_rows(sid)) == rows
    assert ui_text.text("UI_CAP10_ERR_STALE", "en") in _body(client, sid)
    # a new accepted answer (token rotation + a new eligible answer) also stales it
    old = _form(client, sid)
    _answer(client, sid, BA_2)
    rows = len(_rows(sid))
    _declare(client, sid, [answered[1], answered[2]], form=old)
    assert len(_rows(sid)) == rows
    # a fresh render authorizes again
    _declare(client, sid, [answered[1], answered[2]])
    assert len(_declarations(sid)) == 1


@pytest.mark.failure_pattern(
    "FP-02",
    invariant=("a stable action identity never changes with the submitted material; only an exact committed retry is a no-op and the same identity with different material fails closed"),
    constructs=("flask-route", "hmac-signature", "persistence-writer"))
def test_f1_d_exact_committed_retry_survives_staleness_only_for_that_event(client):
    sid, answered = _web_project(client)
    a, b, c = answered[0], answered[-1], answered[1]
    form = _form(client, sid)
    _declare(client, sid, [a, b], form=form)
    assert len(_declarations(sid)) == 1
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": a, "response": MECH, "answer_token": _token(client, sid)})
    rows = len(_rows(sid))
    _declare(client, sid, [a, b], form=form)            # the exact historical event
    assert len(_rows(sid)) == rows
    assert appmod.CONTRADICTION_DECLARED_ACK in _body(client, sid)
    assert active_declared_contradiction_pairs(_live(sid).assertions) == frozenset()
    _declare(client, sid, [c, b], form=form)            # a NEW pair on the stale form
    assert len(_rows(sid)) == rows
    _declare(client, sid, [a, b], note="different", form=form)   # same key, new material
    assert len(_rows(sid)) == rows


# ===========================================================================
# Astra correction F2 — never confirm through an unresolved connection
# ===========================================================================

class _CommitAndRollbackFail:
    def __init__(self, conn):
        self._conn = conn
        self.armed = True

    def execute(self, sql, *args):
        if self.armed and sql in ("COMMIT", "ROLLBACK"):
            if sql == "ROLLBACK":
                self.armed = False
            raise sqlite3.OperationalError("injected: %s failed" % sql)
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


def _independent_declarations(sid):
    path = os.environ["INVENTORAI_DB_PATH"]
    conn = sqlite3.connect(path)
    try:
        return [json.loads(p) for (p,) in conn.execute(
            "SELECT payload FROM records WHERE project_id = ?", (sid,))
            if json.loads(p)["disposition"] == DECL]
    finally:
        conn.close()


def test_f2_failed_commit_and_rollback_never_publishes_uncommitted_data(client):
    sid, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    store = _store()
    real = store._conn
    live_before = copy.deepcopy(_live(sid).assertions)
    try:
        store._conn = _CommitAndRollbackFail(real)
        _declare(client, sid, [a, b])
        # the SAME connection can still see its own uncommitted row ...
        assert real.in_transaction
        assert any(json.loads(p)["disposition"] == DECL for (p,) in real.execute(
            "SELECT payload FROM records WHERE project_id = ?", (sid,)))
        # ... but nothing committed exists, and nothing was acknowledged/published
        assert _independent_declarations(sid) == []
        assert store.committed_state_readable() is False
        assert _live(sid).assertions == live_before
        state = _live(sid)
        assert active_declared_contradiction_pairs(state.assertions) == frozenset()
        assert not any(r.requirement_id.startswith("req:contradiction:")
                       for r in derive_requirement_landscape(state).requirements)
        entry = appmod.SESSION_STORE[sid]
        assert entry.get("_interaction_ack") != appmod.CONTRADICTION_DECLARED_ACK
        assert entry.get("_answer_error") == appmod.CONTRADICTION_UNKNOWN_MESSAGE
        # a further attempt on the unresolved connection writes nothing
        entry.pop("_answer_error", None)
        _declare(client, sid, [answered[1], b])
        assert _independent_declarations(sid) == []
        assert appmod.SESSION_STORE[sid].get("_interaction_ack") \
            != appmod.CONTRADICTION_DECLARED_ACK
    finally:
        store._conn = real
        if real.in_transaction:
            real.execute("ROLLBACK")
    # existing store semantics: the unsafe flag is never cleared on this
    # connection; recovery is a FRESH store connection (as after a restart).
    assert store.committed_state_readable() is False
    store.close()
    appmod._STORE = None
    # the row never committed, and a fresh, correctly bound declaration is
    # accepted exactly once
    assert _independent_declarations(sid) == []
    _declare(client, sid, [a, b])
    assert len(_independent_declarations(sid)) == 1


def test_f2_uncertain_commit_confirmed_from_committed_state_is_acknowledged(client):
    sid, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    store = _store()
    real = store._conn

    class _CommitThenRaise:
        def __init__(self, conn):
            self._conn, self.armed = conn, True

        def execute(self, sql, *args):
            if sql == "COMMIT" and self.armed:
                self.armed = False
                self._conn.execute("COMMIT")
                raise sqlite3.OperationalError("injected: error after commit")
            return self._conn.execute(sql, *args)

        def __getattr__(self, name):
            return getattr(self._conn, name)
    try:
        store._conn = _CommitThenRaise(real)
        _declare(client, sid, [a, b])
    finally:
        store._conn = real
    assert store.committed_state_readable() is True
    assert len(_independent_declarations(sid)) == 1
    assert (a, b) in active_declared_contradiction_pairs(_live(sid).assertions)
    assert appmod.CONTRADICTION_DECLARED_ACK in _body(client, sid)


# ===========================================================================
# Astra correction F3 — the note is stored and compared VERBATIM
# ===========================================================================

def test_f3_note_is_verbatim_and_exact_material(client):
    sid, answered = _web_project(client)
    a, b = answered[0], answered[-1]
    raw_note = "\n Owner note \n"
    form = _form(client, sid)
    _declare(client, sid, [a, b], note=raw_note, form=form)
    decl = _declarations(sid)
    assert len(decl) == 1 and decl[0]["content"] == raw_note
    live = [r for r in _live(sid).assertions if r.disposition == DECL][0]
    assert live.content == raw_note
    # the trimmed variant is DIFFERENT material under the same key -> fail closed
    _declare(client, sid, [a, b], note="Owner note", form=form)
    assert len(_declarations(sid)) == 1
    assert ui_text.text("UI_CAP10_ERR_NOT_SAVED", "en") in _body(client, sid)
    # the exact verbatim retry is still the same event
    _declare(client, sid, [a, b], note=raw_note, form=form)
    assert len(_declarations(sid)) == 1
    assert appmod.CONTRADICTION_DECLARED_ACK in _body(client, sid)
    # replay keeps it byte-identical; display escapes but never rewrites it
    cold = SR.reconstruct_readonly_state(_store(), sid).state
    assert [r.content for r in cold.assertions if r.disposition == DECL] == [raw_note]
    assert "Owner note" in _body(client, sid)
    assert _declarations(sid)[0]["content"] == raw_note
