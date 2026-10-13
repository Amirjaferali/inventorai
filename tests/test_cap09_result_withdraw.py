"""CAP-09 RESULT WITHDRAW-01 — terminal withdrawal of ONE recorded execution.

The inventor may withdraw one recorded execution of a current OR a no-longer-
current experiment so it no longer counts as a current record. ONE append-only
terminal event (``wdr-`` identity, the owner's fixed internal marker, no
context) supersedes the chain's current head; the whole chain stays in the
history (withdrawal is not erasure) and nothing may follow it. No schema
change. Capacity: 200 ordinary events per project plus ONE reserved withdrawal
per root (at most 400). Outputs count CURRENT roots only.
"""
import html
import json
import re
import sqlite3
import threading

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from web.ui_text import text
from engine import disclosure_export as dx
from engine import experiment_result as er
from engine.record_store import (
    RecordStoreConnectionUnsafe, ResultEventConflict, ResultEventRejected,
    ResultEventsCorrupt, SqliteRecordStore, RESULT_EVENT_EXACT_REPLAY,
    RESULT_EVENT_INSERTED)
from tests.csrf_client import csrf_client
from tests.test_stage19_durable_success_criteria import (
    ELEC_DISPLACING_ANSWER, _journey, _restart, _live_ids, _answer, _db_path,
    _CommitThenRaise, _CommitAndRollbackFail, _client_for)
from tests.test_cap09_result_events import (
    OBS, OBS2, TABLE, _page, _forms, _record_form, _correct_form, _post, _events,
    _rows, _ctx)

MARKER = er.WITHDRAWAL_MARKER
WITHDRAW_URL = "/session/%s/experiment-result/withdraw"
EID_A = "exp_v1_alpha_" + "1" * 8
EID_B = "exp_v1_beta_" + "2" * 8


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _store():
    return webapp._get_store()


def _withdraw_forms(raw):
    forms = []
    for body in re.findall(
            r'<form method="POST" action="[^"]*experiment-result/withdraw"[^>]*>(.*?)</form>',
            raw, re.S):
        fields = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', body))
        forms.append({k: html.unescape(v) for k, v in fields.items()})
    return forms


def _withdraw_form(client, sid, head_id):
    [form] = [f for f in _withdraw_forms(_page(client, sid)) if f.get("supersedes") == head_id]
    return form


def _withdraw(client, sid, form, confirm=True):
    data = dict(form)
    if confirm:
        data["withdraw_confirm"] = "yes"
    return client.post(WITHDRAW_URL % sid, data=data)


def _body(r):
    return html.unescape(r.get_data(as_text=True))


def _project(client):
    sid = _journey(client)
    return sid, _live_ids(sid)


def _root_of(client, sid, eid, txt=OBS):
    _post(client, sid, _record_form(client, sid, eid), txt)
    return [e for e in _events(sid) if e.supersedes_result_event_id is None][-1]


def _report(c, sid, lang="en"):
    assert c.post("/ui-language", data={"lang": lang}).status_code in (200, 302)
    r = c.get("/session/%s/deliverable" % sid)
    assert r.status_code == 200
    return html.unescape(r.get_data(as_text=True))


def _pdf_source(c, sid, monkeypatch):
    seen = {}
    real = webapp._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        return real(source)
    monkeypatch.setattr(webapp, "_render_pdf_bytes", spy)
    r = c.post("/session/%s/deliverable.pdf" % sid, data={})
    assert r.status_code == 200 and r.data[:5] == b"%PDF-"
    return html.unescape(seen["source"])


def _key(n):
    return "k%040d" % n


# ==========================================================================
# E. the semantic owner (pure)
# ==========================================================================
def _root(eid=EID_A, txt="one"):
    return er.recorded_root(eid, txt, _ctx())


def test_e1_a_withdrawal_is_a_terminal_successor_with_the_marker_and_no_context():
    root = _root()
    w = er.recorded_withdrawal(EID_A, root.result_event_id)
    assert er.is_valid_withdrawal_event_id(w.result_event_id)
    assert not er.is_valid_result_event_id(w.result_event_id)
    assert len(w.result_event_id) == 36                          # the existing column CHECK
    assert w.result_text == MARKER and w.context is None
    assert w.supersedes_result_event_id == root.result_event_id
    assert er.event_kind(w) == er.EVENT_WITHDRAWAL and er.is_withdrawal(w)
    assert er.validate_result_history([root, w]) == (root, w)


def test_e2_classification_is_by_identity_and_structure_never_by_text():
    root = er.recorded_root(EID_A, MARKER, _ctx())                # ordinary text == marker
    fix = er.recorded_correction(EID_A, MARKER, root.result_event_id)
    assert er.event_kind(root) == er.EVENT_ROOT and not er.is_withdrawal(root)
    assert er.event_kind(fix) == er.EVENT_CORRECTION and not er.is_withdrawal(fix)
    w = er.recorded_withdrawal(EID_A, root.result_event_id)
    for bad in (
            er.ResultEvent(w.result_event_id, EID_A, "not the marker", root.result_event_id,
                           w.recorded_at),
            er.ResultEvent(w.result_event_id, EID_A, MARKER, None, w.recorded_at, _ctx()),
            er.ResultEvent(w.result_event_id, EID_A, MARKER, root.result_event_id,
                           w.recorded_at, _ctx()),
            er.ResultEvent("wdr-" + "A" * 32, EID_A, MARKER, root.result_event_id, w.recorded_at),
            er.ResultEvent("xyz-" + "a" * 32, EID_A, MARKER, root.result_event_id, w.recorded_at)):
        with pytest.raises(er.ResultEventError):
            er.event_kind(bad)
        assert not er.is_withdrawal(bad)
    # a marker-text root and correction validate as ordinary history and count
    assert er.execution_states((root, fix), [EID_A])[EID_A] == {"state": "recorded", "count": 1}


def test_e3_a_withdrawn_execution_is_terminal_and_never_forked_or_crossed():
    root = _root()
    w = er.recorded_withdrawal(EID_A, root.result_event_id)
    after_fix = er.recorded_correction(EID_A, "later", w.result_event_id)
    after_w = er.recorded_withdrawal(EID_A, w.result_event_id)
    fix = er.recorded_correction(EID_A, "fix", root.result_event_id)
    for bad, why in (([root, w, after_fix], "terminal"), ([root, w, after_w], "terminal"),
                     ([root, fix, er.recorded_withdrawal(EID_A, root.result_event_id)],
                      "two successors"),
                     ([root, er.recorded_withdrawal(EID_B, root.result_event_id)],
                      "crosses experiments"),
                     ([er.recorded_withdrawal(EID_A, root.result_event_id), root],
                      "no earlier event")):
        with pytest.raises(er.ResultEventError, match=why):
            er.validate_result_history(bad)


def test_e4_capacity_is_200_ordinary_plus_one_withdrawal_per_root():
    roots = [_root(txt="r%d" % i) for i in range(er.MAX_RESULT_EVENTS_PER_PROJECT)]
    withdrawals = [er.recorded_withdrawal(EID_A, r.result_event_id) for r in roots]
    full = roots + withdrawals
    assert len(full) == er.MAX_TOTAL_RESULT_EVENTS == 400
    assert er.validate_result_history(full) == tuple(full)
    with pytest.raises(er.ResultEventError, match="ordinary"):
        er.validate_result_history(roots + [_root(txt="r200")])
    # a withdrawal never frees ordinary capacity
    with pytest.raises(er.ResultEventError):
        er.validate_result_history(full + [_root(txt="one more")])
    with pytest.raises(er.ResultEventError, match="too many"):
        er.validate_result_history(full + [er.recorded_withdrawal(EID_A, roots[0].result_event_id)])


def test_e5_full_history_keeps_withdrawn_chains_and_the_current_projection_drops_them():
    a, b = _root(txt="first"), _root(txt="second")
    fix = er.recorded_correction(EID_A, "first, corrected", a.result_event_id)
    w = er.recorded_withdrawal(EID_A, fix.result_event_id)
    events = er.validate_result_history([a, b, fix, w])
    full = er.result_chains(events, EID_A)
    assert [c["root"] for c in full] == [a, b]
    assert full[0]["withdrawal"] == w and full[0]["head"] == fix
    assert full[0]["history"] == [a, fix]                         # the marker is never history
    assert full[1]["withdrawal"] is None
    assert [c["root"] for c in er.current_result_chains(events, EID_A)] == [b]
    assert er.execution_states(events, [EID_A])[EID_A] == {"state": "recorded", "count": 1}
    w2 = er.recorded_withdrawal(EID_A, b.result_event_id)
    gone = er.validate_result_history([a, b, fix, w, w2])
    assert er.current_result_chains(gone) == []
    assert len(er.result_chains(gone)) == 2                       # nothing erased
    assert er.execution_states(gone, [EID_A])[EID_A] == {"state": "none", "count": 0}
    assert er.head_ids(gone) == {w.result_event_id, w2.result_event_id}


def test_e6_material_comparison_includes_the_action_kind():
    root = _root()
    w = er.recorded_withdrawal(EID_A, root.result_event_id)
    fix_as_marker = er.recorded_correction(EID_A, MARKER, root.result_event_id)
    assert er.same_result_material(w, er.recorded_withdrawal(EID_A, root.result_event_id))
    assert not er.same_result_material(w, fix_as_marker)
    assert not er.same_result_material(fix_as_marker, w)


# ==========================================================================
# S. the store: append, terminality, replay, capacity, races
# ==========================================================================
def test_s1_store_appends_one_withdrawal_at_a_head_and_refuses_every_other_target(client):
    sid, ids = _project(client)
    other, other_ids = _project(client)
    store = _store()
    root = _root_of(client, sid, ids[0])
    _post(client, sid, _correct_form(client, sid, root.result_event_id), OBS2)
    [_, fix] = _events(sid)
    theirs = _root_of(client, other, other_ids[0])
    for target, eid in ((root.result_event_id, ids[0]),            # not the head
                        (fix.result_event_id, ids[1]),             # another experiment
                        (theirs.result_event_id, ids[0]),          # another project
                        ("res-" + "f" * 32, ids[0])):              # unknown
        with pytest.raises(ResultEventRejected):
            store.append_result_event(sid, er.recorded_withdrawal(eid, target), _key(1))
    assert len(_events(sid)) == 2 and len(_events(other)) == 1
    outcome, stored = store.append_result_event(
        sid, er.recorded_withdrawal(ids[0], fix.result_event_id), _key(2))
    assert outcome == RESULT_EVENT_INSERTED and er.is_withdrawal(stored)
    events = _events(sid)
    assert events[-1] == stored and events[:2] == (root, fix)     # the chain is preserved
    # terminal: neither a correction nor a second withdrawal may follow
    for event in (er.recorded_correction(ids[0], OBS, stored.result_event_id),
                  er.recorded_withdrawal(ids[0], stored.result_event_id),
                  er.recorded_withdrawal(ids[0], fix.result_event_id)):
        with pytest.raises(ResultEventRejected):
            store.append_result_event(sid, event, _key(3))
    assert _events(sid) == events


def test_s2_exact_replay_writes_nothing_and_a_cross_action_replay_is_a_conflict(client):
    sid, ids = _project(client)
    store = _store()
    root = _root_of(client, sid, ids[0])
    w = er.recorded_withdrawal(ids[0], root.result_event_id)
    assert store.append_result_event(sid, w, _key(1))[0] == RESULT_EVENT_INSERTED
    again = er.recorded_withdrawal(ids[0], root.result_event_id)  # a new id, same action
    outcome, stored = store.append_result_event(sid, again, _key(1))
    assert outcome == RESULT_EVENT_EXACT_REPLAY and stored == w
    # the same key with a correction whose text equals the marker is another action
    with pytest.raises(ResultEventConflict):
        store.append_result_event(
            sid, er.recorded_correction(ids[0], MARKER, root.result_event_id), _key(1))
    # an ordinary submission key reused for a withdrawal is a conflict too
    other = _root_of(client, sid, ids[1])
    [ordinary_key] = [r[6] for r in _rows(sid) if r[2] == other.result_event_id]
    with pytest.raises(ResultEventConflict):
        store.append_result_event(
            sid, er.recorded_withdrawal(ids[1], other.result_event_id), ordinary_key)
    assert len(_events(sid)) == 3


def test_s3_capacity_extremes_reserve_one_withdrawal_per_root_and_never_reclaim(client):
    sid, ids = _project(client)
    store = _store()
    roots = []
    for i in range(er.MAX_RESULT_EVENTS_PER_PROJECT):
        roots.append(store.append_result_event(
            sid, er.recorded_root(ids[0], "run %d" % i, _ctx()), _key(i))[1])
    with pytest.raises(ResultEventRejected, match="cap"):
        store.append_result_event(sid, er.recorded_root(ids[0], "over", _ctx()), _key(900))
    with pytest.raises(ResultEventRejected, match="cap"):
        store.append_result_event(
            sid, er.recorded_correction(ids[0], "over", roots[0].result_event_id), _key(901))
    # an exact retry at capacity resolves before the capacity check and writes nothing
    outcome, stored = store.append_result_event(
        sid, er.recorded_root(ids[0], "run 7", _ctx()), _key(7))
    assert outcome == RESULT_EVENT_EXACT_REPLAY and stored == roots[7]
    # every root still has its ONE reserved withdrawal
    for i, root in enumerate(roots):
        store.append_result_event(sid, er.recorded_withdrawal(ids[0], root.result_event_id),
                                  _key(1000 + i))
    assert len(_events(sid)) == er.MAX_TOTAL_RESULT_EVENTS
    # withdrawals freed nothing, and a retry of a withdrawal at the total bound is a replay
    with pytest.raises(ResultEventRejected, match="cap"):
        store.append_result_event(sid, er.recorded_root(ids[0], "after", _ctx()), _key(902))
    assert store.append_result_event(
        sid, er.recorded_withdrawal(ids[0], roots[3].result_event_id),
        _key(1003))[0] == RESULT_EVENT_EXACT_REPLAY
    assert len(_rows(sid)) == er.MAX_TOTAL_RESULT_EVENTS
    assert er.execution_states(_events(sid), [ids[0]])[ids[0]] == {"state": "none", "count": 0}


def _race(sid, events):
    """Append ``events`` concurrently from separate connections to the same
    database; return each outcome (``"ok"`` or the exception class name)."""
    path = _db_path()
    barrier = threading.Barrier(len(events))
    outcomes = [None] * len(events)

    def run(i, event):
        store = SqliteRecordStore(path)
        try:
            barrier.wait()
            store.append_result_event(sid, event, _key(500 + i))
            outcomes[i] = "ok"
        except Exception as exc:                                   # noqa: BLE001
            outcomes[i] = type(exc).__name__
        finally:
            store.close()
    threads = [threading.Thread(target=run, args=(i, e)) for i, e in enumerate(events)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(30)
    return outcomes


@pytest.mark.parametrize("rival", ["correction", "withdrawal"])
def test_s4_a_concurrent_correction_or_second_withdrawal_of_the_same_head_loses(client, rival):
    sid, ids = _project(client)
    root = _root_of(client, sid, ids[0])
    _restart()
    head = root.result_event_id
    other = (er.recorded_correction(ids[0], OBS2, head) if rival == "correction"
             else er.recorded_withdrawal(ids[0], head))
    outcomes = _race(sid, [er.recorded_withdrawal(ids[0], head), other])
    assert sorted(outcomes) == sorted(["ok", "ResultEventRejected"]), outcomes
    events = _events(sid)
    assert len(events) == 2 and events[1].supersedes_result_event_id == head
    assert er.validate_result_history(events) == events


# ==========================================================================
# R. the route: confirmation, signed binding, retry, staleness, ambiguity
# ==========================================================================
def test_r1_withdrawing_keeps_the_chain_as_labelled_history_without_controls(client):
    sid, ids = _project(client)
    root = _root_of(client, sid, ids[0])
    _post(client, sid, _correct_form(client, sid, root.result_event_id), OBS2)
    [_, fix] = _events(sid)
    r = _withdraw(client, sid, _withdraw_form(client, sid, fix.result_event_id))
    assert r.status_code == 200
    assert webapp._RESULT_WITHDRAW_SAVED_MESSAGE in _body(r)
    events = _events(sid)
    assert len(events) == 3 and er.is_withdrawal(events[2])
    assert events[2].supersedes_result_event_id == fix.result_event_id
    page = html.unescape(_page(client, sid))
    assert OBS in page and OBS2 in page                            # nothing erased
    assert text("UI_R_WITHDRAWN", "en") in page
    assert page.count("data-result-chain-withdrawn") == 1
    assert MARKER not in page and events[2].result_event_id not in page
    assert not any(f.get("supersedes") in (root.result_event_id, fix.result_event_id)
                   for f in _forms(page) + _withdraw_forms(page))   # no further control


def test_r2_a_withdrawal_needs_explicit_confirmation(client):
    sid, ids = _project(client)
    root = _root_of(client, sid, ids[0])
    form = _withdraw_form(client, sid, root.result_event_id)
    for data in ({}, {"withdraw_confirm": "no"}, {"withdraw_confirm": ""}):
        r = client.post(WITHDRAW_URL % sid, data=dict(form, **data))
        assert r.status_code == 400
        assert webapp._RESULT_WITHDRAW_CONFIRM_MESSAGE in _body(r)
    assert _events(sid) == (root,)


def test_r3_the_signed_binding_covers_project_experiment_head_and_action(client):
    sid, ids = _project(client)
    other, other_ids = _project(client)
    a = _root_of(client, sid, ids[0])
    b = _root_of(client, sid, ids[0], OBS2)
    form = _withdraw_form(client, sid, a.result_event_id)
    theirs_root = _root_of(client, other, other_ids[0])
    theirs = _withdraw_form(client, other, theirs_root.result_event_id)
    record = _record_form(client, sid, ids[0])
    for data in (dict(form, supersedes=b.result_event_id),          # re-targeted head
                 dict(form, experiment_id=ids[1]),                  # re-targeted experiment
                 dict(form, result_withdrawal_submission=""),
                 dict(form, result_withdrawal_submission=theirs["result_withdrawal_submission"]),
                 dict(form, result_withdrawal_submission=record["result_submission"]),
                 dict(form, result_withdrawal_submission=form["result_withdrawal_submission"][:-2]
                      + "zz")):
        r = _withdraw(client, sid, data)
        assert r.status_code == 400
        assert webapp._RESULT_WITHDRAW_NOT_SAVED_MESSAGE in _body(r)
    # another project's form posted at this project verifies as nothing
    assert _withdraw(client, sid, theirs).status_code == 400
    assert _events(sid) == (a, b) and _events(other) == (theirs_root,)


def test_r4_an_exact_retry_writes_nothing_also_after_a_restart(client):
    sid, ids = _project(client)
    root = _root_of(client, sid, ids[0])
    form = _withdraw_form(client, sid, root.result_event_id)
    assert _withdraw(client, sid, form).status_code == 200
    _restart()
    r = _withdraw(client, sid, form)
    assert r.status_code == 200 and webapp._RESULT_WITHDRAW_SAVED_MESSAGE in _body(r)
    assert len(_rows(sid)) == 2


def test_r5_a_stale_form_never_withdraws_a_changed_or_withdrawn_execution(client):
    sid, ids = _project(client)
    root = _root_of(client, sid, ids[0])
    early = _withdraw_form(client, sid, root.result_event_id)
    twin = _withdraw_form(client, sid, root.result_event_id)       # a second rendering
    _post(client, sid, _correct_form(client, sid, root.result_event_id), OBS2)
    r = _withdraw(client, sid, early)
    assert r.status_code == 400 and webapp._RESULT_WITHDRAW_STALE_MESSAGE in _body(r)
    [_, fix] = _events(sid)
    assert _withdraw(client, sid, _withdraw_form(client, sid, fix.result_event_id)).status_code == 200
    late = twin
    assert _withdraw(client, sid, late).status_code == 400
    assert len(_events(sid)) == 3


def test_r5b_a_correction_form_rendered_before_the_withdrawal_saves_nothing(client):
    sid, ids = _project(client)
    root = _root_of(client, sid, ids[0])
    fix_form = _correct_form(client, sid, root.result_event_id)
    assert _withdraw(client, sid, _withdraw_form(client, sid, root.result_event_id)).status_code == 200
    r = _post(client, sid, fix_form, OBS2)
    assert r.status_code == 400
    assert webapp._RESULT_STALE_TARGET_MESSAGE in _body(r) and "withdrawn" in webapp._RESULT_STALE_TARGET_MESSAGE
    assert len(_events(sid)) == 2 and er.is_withdrawal(_events(sid)[1])


def test_r6_a_cross_action_replay_under_the_withdrawal_key_is_never_confirmed(client):
    sid, ids = _project(client)
    root = _root_of(client, sid, ids[0])
    form = _withdraw_form(client, sid, root.result_event_id)
    nonce = form["result_withdrawal_submission"].split(".")[0]
    key = webapp._result_withdrawal_key(sid, nonce)
    _store().append_result_event(
        sid, er.recorded_correction(ids[0], MARKER, root.result_event_id), key)
    r = _withdraw(client, sid, form)
    assert r.status_code == 400
    body = _body(r)
    assert webapp._RESULT_WITHDRAW_NOT_SAVED_MESSAGE in body
    assert webapp._RESULT_WITHDRAW_SAVED_MESSAGE not in body
    assert not any(er.is_withdrawal(e) for e in _events(sid))
    # and the marker-text correction is shown as the ordinary observation it is
    assert er.execution_states(_events(sid), [ids[0]])[ids[0]]["count"] == 1


def test_r7_a_historical_experiment_execution_can_be_withdrawn_but_not_extended(client):
    sid, ids = _project(client)
    claim = [i for i in ids if "_reasoned_leading_claim_" in i][0]
    root = _root_of(client, sid, claim)
    _answer(client, sid, ELEC_DISPLACING_ANSWER)
    assert claim not in _live_ids(sid)
    page = html.unescape(_page(client, sid))
    assert text("UI_R_STALE", "en") in page
    assert all(f.get("experiment_id") != claim for f in _forms(page))   # no record / correct
    form = _withdraw_form(client, sid, root.result_event_id)
    assert form["experiment_id"] == claim
    assert _withdraw(client, sid, form).status_code == 200
    events = _events(sid)
    assert len(events) == 2 and er.is_withdrawal(events[1])
    page = html.unescape(_page(client, sid))
    assert text("UI_R_WITHDRAWN", "en") in page and OBS in page and MARKER not in page
    assert not _withdraw_forms(page)


def test_r8_commit_ambiguity_resolves_from_committed_truth_or_stays_unknown(client):
    sid, ids = _project(client)
    a = _root_of(client, sid, ids[0])
    b = _root_of(client, sid, ids[1])
    store = _store()
    real = store._conn
    store._conn = _CommitThenRaise(real)
    try:
        r = _withdraw(client, sid, _withdraw_form(client, sid, a.result_event_id))
    finally:
        store._conn = real
    assert r.status_code == 200 and webapp._RESULT_WITHDRAW_SAVED_MESSAGE in _body(r)
    assert len(_events(sid)) == 3
    form = _withdraw_form(client, sid, b.result_event_id)
    store._conn = _CommitAndRollbackFail(real)
    try:
        r = _withdraw(client, sid, form)
    finally:
        store._conn = real
    try:
        assert r.status_code == 503
        body = _body(r)
        assert webapp._RESULT_WITHDRAW_UNKNOWN_MESSAGE in body
        assert webapp._RESULT_WITHDRAW_SAVED_MESSAGE not in body
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_result_events(sid)
        retry = _withdraw(client, sid, form)                       # still unresolved
        assert retry.status_code == 503
        assert webapp._RESULT_WITHDRAW_UNKNOWN_MESSAGE in _body(retry)
    finally:
        real.close()
        webapp._STORE = None
    assert len(_events(sid)) == 3                                  # nothing half-written
    assert _withdraw(client, sid, form).status_code == 200
    assert len(_events(sid)) == 4


def test_r9_only_the_project_owner_can_withdraw(client):
    owner, _aid = _client_for("withdraw-owner@example.com")
    stranger, _sid2 = _client_for("withdraw-stranger@example.com")
    sid = _journey(owner)
    eid = _live_ids(sid)[0]
    _post(owner, sid, _record_form(owner, sid, eid), OBS)
    [root] = _events(sid)
    form = _withdraw_form(owner, sid, root.result_event_id)
    form.pop("csrf_token")                    # the stranger's own browser token
    r = _withdraw(stranger, sid, form)
    assert r.status_code == 302 and "experiment-result" not in r.headers.get("Location", "")
    assert _events(sid) == (root,)


# ==========================================================================
# O. outputs: report / PDF and the disclosure export count CURRENT roots
# ==========================================================================
def _export(c, sid):
    doc = json.loads(c.get("/account/projects/%s/disclosure-export/json" % sid).data.decode("utf-8"))
    [field] = [f for f in doc["content"]["fields"] if f["field"] == "experiments"]
    return doc, [i["slots"]["execution_state"]["tokens"] for i in field["items"]]


def test_o1_report_pdf_and_export_count_current_roots_mixed_and_all_withdrawn(monkeypatch):
    app.config["TESTING"] = True
    c, _aid = _client_for("withdraw-outputs@example.com")
    sid = _journey(c)
    ids = _live_ids(sid)
    a = _root_of(c, sid, ids[0])
    b = _root_of(c, sid, ids[0], OBS2)
    _withdraw(c, sid, _withdraw_form(c, sid, a.result_event_id))
    mixed = webapp.S11_EXECUTION_TEXT["recorded"].format(n=1)
    report = _report(c, sid)
    assert mixed in report and MARKER not in report
    assert mixed in _pdf_source(c, sid, monkeypatch)
    _doc, states = _export(c, sid)
    assert states.count({"state": "recorded", "count": 1}) == 1
    assert states.count({"state": "none", "count": 0}) == len(states) - 1
    _withdraw(c, sid, _withdraw_form(c, sid, b.result_event_id))
    none = webapp.S11_EXECUTION_TEXT["none"]
    assert "current" in none.lower()                               # zero CURRENT, not "never"
    report = _report(c, sid)
    assert webapp.S11_EXECUTION_TEXT["recorded"].format(n=1) not in report
    assert report.count(none) == len(ids)
    doc, states = _export(c, sid)
    assert states and all(t == {"state": "none", "count": 0} for t in states)
    dx.check_projection(doc["content"])
    for lang in ("en", "ar"):
        c.post("/ui-language", data={"lang": lang})
        for raw in (json.dumps(doc), c.get("/account/projects/%s/disclosure-export/html" % sid)
                    .data.decode("utf-8"), _report(c, sid, lang)):
            assert MARKER not in raw and "wdr-" not in raw
            assert OBS not in raw and OBS2 not in raw              # result text never carried


def test_o2_a_corrupt_withdrawal_reads_unavailable_never_zero(client, monkeypatch):
    sid, ids = _project(client)
    root = _root_of(client, sid, ids[0])
    _withdraw(client, sid, _withdraw_form(client, sid, root.result_event_id))
    con = sqlite3.connect(_db_path())
    try:
        con.execute("UPDATE %s SET result_text = 'not the marker' "
                    "WHERE project_id = ? AND result_event_id LIKE 'wdr-%%'" % TABLE, (sid,))
        con.commit()
    finally:
        con.close()
    with pytest.raises(ResultEventsCorrupt):
        _store().load_result_events(sid)
    report = _report(client, sid)
    assert webapp.S11_EXECUTION_TEXT["unavailable"] in report
    assert webapp.S11_EXECUTION_TEXT["none"] not in report
    page = html.unescape(_page(client, sid))
    assert text("UI_R_UNAVAILABLE", "en") in page and not _withdraw_forms(page)


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_o3_the_withdrawal_copy_is_localized_on_the_planning_page(client, lang):
    sid, ids = _project(client)
    root = _root_of(client, sid, ids[0])
    client.post("/ui-language", data={"lang": lang})
    page = html.unescape(_page(client, sid))
    for key in ("UI_R_WITHDRAW", "UI_R_WITHDRAW_NOTE", "UI_R_WITHDRAW_CONFIRM",
                "UI_R_WITHDRAW_BUTTON"):
        assert text(key, lang) in page, key
    r = _withdraw(client, sid, _withdraw_form(client, sid, root.result_event_id))
    assert text("UI_R_MSG_WITHDRAW_SAVED", lang) in _body(r)
    assert text("UI_R_WITHDRAWN", lang) in html.unescape(_page(client, sid))
