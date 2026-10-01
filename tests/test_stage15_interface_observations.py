"""Stage 15 Slice 4 — Interface Verification Observation Event.

For each durable Owner-declared Stage-15 interface the inventor records, in
their own words, what actually happened when they tested or checked it.

  * semantic owner ``engine/interface_observation.py`` (NOT
    ``engine/subsystem_model.py``); ``interface_id`` stays the only interface
    identity; every event has a fresh opaque server-generated ``obs-`` id;
  * APPEND-ONLY: a separately reported check is an independent ROOT; a
    correction supersedes the current HEAD of one chain; nothing is rewritten
    or deleted; no fork;
  * a root freezes the interface's DURABLE preparation values at recording
    (exact text or explicit absence; all three absent is valid); a correction
    carries no context;
  * ONE additive append-only sidecar ``subsystem_interface_observations``;
    signed submission identity; exact retry / conflict / SAVED / NOT SAVED /
    UNKNOWN with the committed outcome of THIS submission reconciled first;
  * OWNER_STATED / UNVALIDATED: no verdict, criterion comparison,
    compatibility, readiness, IRL, progression, gap or evidence effect; the
    report, PDF and Structured Export are unchanged.
"""
import html as _html
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine import interface_observation as io
from engine import session_reconstruction as SR
from engine import subsystem_model as sm
from engine.readiness_snapshot import readiness_snapshot
from engine.record_store import (
    INTERFACE_OBSERVATION_EXACT_REPLAY, InterfaceObservationCapReached,
    InterfaceObservationConflict, InterfaceObservationRejected,
    InterfaceObservationsCorrupt, RecordStoreConnectionUnsafe, SqliteRecordStore,
    SubsystemInterfacesCorrupt)
from engine.requirement_landscape import derive_requirement_landscape
from engine.validation_plan import derive_validation_plan
from tests.csrf_client import csrf_client
from tests.test_stage15_integrated_invention_entry import (
    PARTS, _CommitAndRollbackFail, _pdf_source, _visible)
from tests.test_stage15_interface_preparation import (
    ACCEPT, COND, EVID, F_A, F_C, F_E, _field, _integrated_with_interface,
    _prep_rows, _save)
from tests.test_stage15_subsystem_interface_declaration import (
    _FailOn, _declare, _ifc, _new_project, _raw)
from tests.test_stage19_durable_success_criteria import (
    _CommitThenRaise, _progression_snapshot, _restart)
from web import ui_text

OBS = "The arm opened fully in about 2 seconds on 8 of 10 cycles."
OBS2 = "On a retest the arm opened fully every time."
TABLE = "subsystem_interface_observations"
ROUTE = "/session/%s/interface-observation"


@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _store():
    return appmod._get_store()


def _page_raw(c, sid):
    r = c.get("/session/%s/interface-preparation" % sid)
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _page(c, sid):
    return _html.unescape(_page_raw(c, sid))


def _forms(raw):
    """Every observation form on the page as a dict of its hidden fields."""
    forms = []
    for body in re.findall(
            r'<form method="POST" action="[^"]*interface-observation"[^>]*>(.*?)</form>',
            raw, re.S):
        fields = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', body))
        forms.append({k: _html.unescape(v) for k, v in fields.items()})
    return forms


def _record_form(c, sid, iid):
    [form] = [f for f in _forms(_page_raw(c, sid))
              if f.get("interface_id") == iid and "supersedes" not in f]
    return form


def _correct_form(c, sid, head_id):
    [form] = [f for f in _forms(_page_raw(c, sid)) if f.get("supersedes") == head_id]
    return form


def _observe(c, sid, form, observation_text, **extra):
    data = dict(form)
    data["observation_text"] = observation_text
    data.update(extra)
    return c.post(ROUTE % sid, data=data)


def _body(resp):
    return _html.unescape(resp.get_data(as_text=True))


def _events(sid):
    return _store().load_interface_observations(sid)


def _rows(sid):
    _store()
    return _raw("SELECT * FROM %s WHERE project_id = ? ORDER BY observation_seq" % TABLE,
                (sid,))


def _section(page):
    """The visible observation section of a preparation page."""
    start = page.index(ui_text.text("UI_S15_OBS_HEADING", "en")
                       if ui_text.text("UI_S15_OBS_HEADING", "en") in page
                       else ui_text.text("UI_S15_OBS_HEADING", "ar"))
    return _visible(re.sub(r"<style.*?</style>", " ", page[start:], flags=re.S))


def _two_interfaces(c):
    sid, first = _integrated_with_interface(c)
    assert _declare(c, sid, "Bolted mounting between the arm and the board.").status_code == 302
    [second] = [i for i in _store().load_subsystem_interfaces(sid)
                if i.interface_id != first.interface_id]
    return sid, first, second


def _store_project(store, n=1):
    pid, subs = _new_project(store)
    items = []
    for k in range(n):
        item = _ifc(subs, "Declared interaction %d." % k)
        store.append_subsystem_interface(pid, item, "ifc-key-%d" % k)
        items.append(item)
    return pid, items


def _root(iid, observation_text=OBS, context=None):
    return io.recorded_root(iid, observation_text, context or io.ObservationContext())


# ==========================================================================
# 1. Roots: first check, retest, identical-text retest, server identity
# ==========================================================================
def test_a_first_check_is_one_root_with_a_server_generated_opaque_id(client):
    sid, ifc = _integrated_with_interface(client)
    form = _record_form(client, sid, ifc.interface_id)
    chosen = "obs-" + "a" * 32
    r = _observe(client, sid, form, "  " + OBS + "  ", observation_id=chosen)
    assert r.status_code == 200
    assert appmod.S15_OBS_SAVED_MESSAGE in _body(r)
    [ev] = _events(sid)
    assert ev.interface_id == ifc.interface_id and ev.observation_text == OBS  # trimmed
    assert ev.supersedes_observation_id is None and ev.context is not None
    assert io.is_valid_observation_id(ev.observation_id)
    assert ev.observation_id != chosen                            # client never chooses it
    assert OBS not in ev.observation_id and ifc.interface_id[4:] not in ev.observation_id


def test_a_retest_is_a_second_independent_root(client):
    sid, ifc = _integrated_with_interface(client)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS2)
    first, second = _events(sid)
    assert first.supersedes_observation_id is None
    assert second.supersedes_observation_id is None               # never supersedes
    assert [c["root"] for c in io.observation_chains(_events(sid), ifc.interface_id)] \
        == [first, second]


def test_identical_text_from_a_new_form_is_a_real_retest(client):
    sid, ifc = _integrated_with_interface(client)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    first, second = _events(sid)
    assert first.observation_text == second.observation_text == OBS
    assert first.observation_id != second.observation_id
    assert second.supersedes_observation_id is None


# ==========================================================================
# 2. Corrections: successor, immutability, fork / non-head / cross refusals
# ==========================================================================
def test_a_correction_appends_a_successor_and_never_rewrites_the_earlier_entry(client):
    sid, ifc = _integrated_with_interface(client)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    [root] = _events(sid)
    raw_before = _rows(sid)
    r = _observe(client, sid, _correct_form(client, sid, root.observation_id), OBS2)
    assert r.status_code == 200
    root2, fix = _events(sid)
    assert root2 == root and _rows(sid)[:1] == raw_before          # byte-for-byte kept
    assert fix.supersedes_observation_id == root.observation_id
    assert fix.context is None and fix.interface_id == ifc.interface_id
    [chain] = io.observation_chains(_events(sid), ifc.interface_id)
    assert chain["head"] == fix and chain["history"] == [root, fix]
    page = _page(client, sid)
    assert OBS2 in page and OBS in page                           # head and history shown
    assert ui_text.text("UI_S15_OBS_EARLIER", "en") in page
    assert _forms(_page_raw(client, sid))[0]["supersedes"] == fix.observation_id


def test_a_fork_and_a_non_head_correction_are_refused(client):
    sid, ifc = _integrated_with_interface(client)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    [root] = _events(sid)
    stale_form = _correct_form(client, sid, root.observation_id)
    _observe(client, sid, _correct_form(client, sid, root.observation_id), OBS2)
    r = _observe(client, sid, stale_form, "Another correction")    # root is no head now
    assert r.status_code == 400
    assert appmod.S15_OBS_STALE_MESSAGE in _body(r)
    assert len(_events(sid)) == 2
    with pytest.raises(InterfaceObservationRejected):
        _store().append_interface_observation(
            sid, io.recorded_correction(ifc.interface_id, "x", root.observation_id), "k-fork")
    row = list(_rows(sid)[1])                                      # database backstop
    row[1], row[2], row[6] = 5, io.new_observation_id(), "raw-key"
    with pytest.raises(sqlite3.IntegrityError):
        _raw("INSERT INTO %s VALUES (%s)" % (TABLE, ",".join("?" * len(row))), row)
    assert len(_rows(sid)) == 2


def test_cross_project_and_cross_interface_targets_are_refused(client):
    sid, first, second = _two_interfaces(client)
    other, theirs_ifc = _integrated_with_interface(client)
    _observe(client, sid, _record_form(client, sid, first.interface_id), OBS)
    _observe(client, other, _record_form(client, other, theirs_ifc.interface_id), OBS)
    [mine] = _events(sid)
    [theirs] = _events(other)
    store = _store()
    with pytest.raises(InterfaceObservationRejected):             # another project's event
        store.append_interface_observation(sid, io.recorded_correction(
            first.interface_id, "x", theirs.observation_id), "k1")
    with pytest.raises(InterfaceObservationRejected):             # another interface
        store.append_interface_observation(sid, io.recorded_correction(
            second.interface_id, "x", mine.observation_id), "k2")
    form = _correct_form(client, sid, mine.observation_id)
    assert _observe(client, sid, dict(form, interface_id=second.interface_id),
                    "x").status_code == 400
    assert _observe(client, sid, dict(form, supersedes=theirs.observation_id),
                    "x").status_code == 400
    assert len(_events(sid)) == 1 and len(_events(other)) == 1


# ==========================================================================
# 3. Retry identity: exact retry, restart, later changes, conflicts, forgery
# ==========================================================================
def test_an_exact_retry_creates_no_duplicate_even_after_a_restart(client):
    sid, ifc = _integrated_with_interface(client)
    form = _record_form(client, sid, ifc.interface_id)
    for _ in range(3):
        r = _observe(client, sid, form, OBS)
        assert r.status_code == 200
        assert appmod.S15_OBS_SAVED_MESSAGE in _body(r)
    assert len(_events(sid)) == 1
    _restart()
    assert _observe(client, sid, form, OBS).status_code == 200    # after a restart too
    assert len(_events(sid)) == 1


def test_an_exact_retry_reconciles_after_a_preparation_edit_and_a_chain_advance(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_C, iid): COND})
    form = _record_form(client, sid, iid)
    _observe(client, sid, form, OBS)
    [root] = _events(sid)
    _save(client, sid, {(F_C, iid): "Outdoors.", (F_A, iid): ACCEPT})  # preparation changed
    _observe(client, sid, _correct_form(client, sid, root.observation_id), OBS2)  # chain advanced
    r = _observe(client, sid, form, OBS)
    assert r.status_code == 200 and appmod.S15_OBS_SAVED_MESSAGE in _body(r)
    events = _events(sid)
    assert len(events) == 2 and events[0] == root
    assert root.context.operating_conditions == COND                # still the frozen value
    outcome, stored = _store().append_interface_observation(
        sid, _root(iid, OBS, io.ObservationContext(operating_conditions="Anything")),
        appmod._s15_observation_action_key(sid, form["observation_submission"][:32]))
    assert outcome == INTERFACE_OBSERVATION_EXACT_REPLAY and stored == root


def test_the_same_identity_with_changed_material_fails_closed(client):
    sid, first, second = _two_interfaces(client)
    form = _record_form(client, sid, first.interface_id)
    _observe(client, sid, form, OBS)
    [root] = _events(sid)
    for data, text_value in ((form, OBS2),                                   # text
                             (dict(form, interface_id=second.interface_id), OBS),  # interface
                             (dict(form, supersedes=root.observation_id), OBS)):   # target
        r = _observe(client, sid, data, text_value)
        assert r.status_code == 400
        assert appmod.S15_OBS_NOT_SAVED_MESSAGE in _body(r)
    assert _events(sid) == (root,)
    with pytest.raises(InterfaceObservationConflict):
        _store().append_interface_observation(
            sid, _root(first.interface_id, OBS2),
            appmod._s15_observation_action_key(sid, form["observation_submission"][:32]))


def test_a_forged_missing_or_foreign_submission_identity_saves_nothing(client):
    sid, ifc = _integrated_with_interface(client)
    form = _record_form(client, sid, ifc.interface_id)
    nonce = form["observation_submission"][:32]
    foreign = nonce + "." + appmod._submission_sig(appmod._RESULT_SUBMISSION_DOMAIN, sid, nonce)
    for bad in ("", "0" * 32 + ".forged", form["observation_submission"][:-2] + "zz", foreign):
        r = _observe(client, sid, dict(form, observation_submission=bad), OBS)
        assert r.status_code == 400
        assert appmod.S15_OBS_NOT_SAVED_MESSAGE in _body(r)
    other, other_ifc = _integrated_with_interface(client)          # another project's form
    assert _observe(client, sid, _record_form(client, other, other_ifc.interface_id),
                    OBS).status_code == 400
    assert _events(sid) == () and _events(other) == ()
    submissions = [f["observation_submission"] for f in _forms(_page_raw(client, sid))]
    assert len(set(submissions)) == len(submissions)               # one per form


def test_csrf_and_project_authorization_are_enforced(client):
    sid, ifc = _integrated_with_interface(client)
    form = _record_form(client, sid, ifc.interface_id)
    raw = appmod.app.test_client()                                  # no CSRF token injection
    r = raw.post(ROUTE % sid, data=dict(form, observation_text=OBS))
    assert r.status_code in (400, 403)
    assert client.post(ROUTE % "does-not-exist",
                       data=dict(form, observation_text=OBS)).status_code in (302, 403, 404)
    from tests.test_commercial_evidence_capture import _client_for
    owner, _aid = _client_for("obs-owner@example.com")
    owned, owned_ifc = _integrated_with_interface(owner)
    owned_form = _record_form(owner, owned, owned_ifc.interface_id)
    intruder, _bid = _client_for("obs-intruder@example.com")
    r = intruder.post(ROUTE % owned, data=dict(owned_form, observation_text=OBS))
    assert r.status_code in (302, 403, 404)
    assert _events(sid) == () and _events(owned) == ()


# ==========================================================================
# 4. SAVED / NOT SAVED / UNKNOWN (IR-01)
# ==========================================================================
def test_a_committed_but_unconfirmed_write_resolves_saved(client):
    sid, ifc = _integrated_with_interface(client)
    form = _record_form(client, sid, ifc.interface_id)
    store = _store()
    real = store._conn
    store._conn = _CommitThenRaise(real)
    try:
        r = _observe(client, sid, form, OBS)
    finally:
        store._conn = real
    assert r.status_code == 200 and appmod.S15_OBS_SAVED_MESSAGE in _body(r)
    assert len(_events(sid)) == 1


def test_a_failed_insert_with_a_clean_rollback_is_not_saved(client):
    sid, ifc = _integrated_with_interface(client)
    form = _record_form(client, sid, ifc.interface_id)
    store = _store()
    real = store._conn
    store._conn = _FailOn(real, prefix="INSERT INTO " + TABLE)
    try:
        r = _observe(client, sid, form, OBS)
    finally:
        store._conn = real
    assert r.status_code == 503
    body = _body(r)
    assert appmod.S15_OBS_NOT_SAVED_MESSAGE in body and appmod.S15_OBS_SAVED_MESSAGE not in body
    assert OBS in body                                              # the draft is kept
    assert _events(sid) == ()
    assert _observe(client, sid, form, OBS).status_code == 200      # same retry now saves
    assert len(_events(sid)) == 1


def test_an_unresolved_transaction_stays_unknown_until_durable_truth_is_readable(client):
    sid, ifc = _integrated_with_interface(client)
    form = _record_form(client, sid, ifc.interface_id)
    store = _store()
    real = store._conn
    store._conn = _CommitAndRollbackFail(real)
    try:
        r = _observe(client, sid, form, OBS)
    finally:
        store._conn = real
    try:
        assert r.status_code == 503
        body = _body(r)
        assert appmod.S15_OBS_UNKNOWN_MESSAGE in body
        assert appmod.S15_OBS_SAVED_MESSAGE not in body and "Nothing was changed" not in body
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.load_interface_observations(sid)
        # The SAME retry on the still-unresolved connection stays UNKNOWN: it
        # is never reinterpreted as NOT SAVED and never duplicates.
        assert appmod._STORE is store and store._conn is real
        retry = _observe(client, sid, form, OBS)
        assert retry.status_code == 503
        body = _body(retry)
        assert appmod.S15_OBS_UNKNOWN_MESSAGE in body and "Nothing was changed" not in body
        with pytest.raises(RecordStoreConnectionUnsafe):
            store.committed_interface_observation_for_submission(sid, "anything")
    finally:
        real.close()
        appmod._STORE = None
    assert _events(sid) == ()                                       # nothing half-written
    r = _observe(client, sid, form, OBS)                            # readable again: resolves
    assert r.status_code == 200 and len(_events(sid)) == 1
    assert _observe(client, sid, form, OBS).status_code == 200      # and never duplicates
    assert len(_events(sid)) == 1


# ==========================================================================
# 5. Frozen context at recording
# ==========================================================================
def test_a_root_freezes_the_exact_durable_preparation(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_C, iid): COND, (F_A, iid): ACCEPT, (F_E, iid): EVID})
    _observe(client, sid, _record_form(client, sid, iid), OBS)
    [root] = _events(sid)
    assert root.context == io.ObservationContext(COND, ACCEPT, EVID)


def test_a_partial_preparation_freezes_exact_present_and_absent_values(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_A, iid): ACCEPT})
    _observe(client, sid, _record_form(client, sid, iid), OBS)
    [root] = _events(sid)
    assert root.context == io.ObservationContext(None, ACCEPT, None)
    ctx_cols = _rows(sid)[0][8:]
    assert ctx_cols == (None, ACCEPT, None)                        # explicit NULL absence


def test_a_root_with_all_three_preparation_inputs_absent_is_valid(client):
    sid, ifc = _integrated_with_interface(client)
    assert _prep_rows(sid) == []                                    # no preparation row
    r = _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    assert r.status_code == 200
    [root] = _events(sid)
    assert root.supersedes_observation_id is None
    assert root.context == io.ObservationContext(None, None, None)  # no placeholder
    assert _rows(sid)[0][5] is None and _rows(sid)[0][8:] == (None, None, None)
    assert io.validate_observation_history([root]) == (root,)
    page = _page(client, sid)
    assert page.count(ui_text.text("UI_S15_OBS_CONTEXT_ABSENT", "en")) == 3


def test_unsaved_preparation_text_is_never_frozen_or_saved(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_C, iid): COND})
    base = appmod._S15_PREP_BASE_PREFIXES
    typed = {_field(F_C, iid): "Typed in the browser but never saved.",
             base[F_C] + iid: COND,
             _field(F_E, iid): "Also unsaved.", base[F_E] + iid: ""}
    r = _observe(client, sid, _record_form(client, sid, iid), OBS, **typed)
    assert r.status_code == 200
    [root] = _events(sid)
    assert root.context == io.ObservationContext(COND, None, None)  # durable truth only
    assert _prep_rows(sid) == [(iid, COND, None, None)]             # preparation untouched


def test_later_preparation_edits_never_rewrite_frozen_context_and_corrections_add_none(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_C, iid): COND, (F_E, iid): EVID})
    _observe(client, sid, _record_form(client, sid, iid), OBS)
    [root] = _events(sid)
    _save(client, sid, {(F_C, iid): "Outdoors.", (F_E, iid): ""})    # edit + clear
    _save(client, sid, {(F_C, iid): ""})                             # clear all
    assert _prep_rows(sid) == []
    _observe(client, sid, _correct_form(client, sid, root.observation_id), OBS2)
    root2, fix = _events(sid)
    assert root2.context == io.ObservationContext(COND, None, EVID)   # history untouched
    assert fix.context is None and _rows(sid)[1][8:] == (None, None, None)
    page = _page(client, sid)
    assert COND in page and EVID in page
    assert ui_text.text("UI_S15_OBS_CONTEXT_NOTE", "en") in page
    _observe(client, sid, _record_form(client, sid, iid), "A later check.")
    assert _events(sid)[2].context == io.ObservationContext()        # the current (empty) truth


def test_the_store_refuses_a_root_whose_context_is_not_the_durable_preparation():
    store = _store()
    pid, [item] = _store_project(store)
    store.apply_interface_preparation_delta(pid, {item.interface_id: {F_C: COND}})
    stale = _root(item.interface_id, OBS, io.ObservationContext(operating_conditions="Old"))
    with pytest.raises(InterfaceObservationRejected):
        store.append_interface_observation(pid, stale, "k-stale")
    with pytest.raises(InterfaceObservationRejected):               # absence is not a match
        store.append_interface_observation(pid, _root(item.interface_id), "k-empty")
    assert store.load_interface_observations(pid) == ()
    good = _root(item.interface_id, OBS, io.ObservationContext(operating_conditions=COND))
    store.append_interface_observation(pid, good, "k-good")
    assert store.load_interface_observations(pid) == (good,)


def test_recorded_at_is_recording_metadata_only(client):
    sid, ifc = _integrated_with_interface(client)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    [root] = _events(sid)
    assert re.match(r"\A\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\+00:00\Z", root.recorded_at)
    assert root.recorded_at not in _page(client, sid)               # never shown as a test time
    cols = [r[1] for r in _raw("PRAGMA table_info(%s)" % TABLE)]
    assert "recorded_at" in cols
    for banned in ("tested_at", "executed_at", "performed_at", "check_time"):
        assert banned not in cols


# ==========================================================================
# 6. Interface membership and fail-closed durable truth
# ==========================================================================
def test_exact_interface_membership_is_required(client):
    sid, ifc = _integrated_with_interface(client)
    other, theirs = _integrated_with_interface(client)
    form = _record_form(client, sid, ifc.interface_id)
    for bogus in (theirs.interface_id, sm.new_interface_id(), "ifc-not-an-id", ""):
        r = _observe(client, sid, dict(form, interface_id=bogus), OBS)
        assert r.status_code == 400
        assert appmod.S15_OBS_NOT_CURRENT_MESSAGE in _body(r)
    with pytest.raises(InterfaceObservationRejected):
        _store().append_interface_observation(sid, _root(theirs.interface_id), "k-x")
    assert _events(sid) == () and _events(other) == ()


def test_corrupt_or_missing_interface_truth_fails_closed(client):
    sid, ifc = _integrated_with_interface(client)
    saved_form = _record_form(client, sid, ifc.interface_id)
    _observe(client, sid, saved_form, OBS)
    form = _record_form(client, sid, ifc.interface_id)
    _raw("UPDATE subsystem_interfaces SET description = '  padded  ' WHERE project_id = ?",
         (sid,), ignore_checks=True)
    # THIS submission's committed outcome is reconciled before any current read:
    # an exact retry still resolves SAVED although the page itself is unavailable.
    r = _observe(client, sid, saved_form, OBS)
    assert r.status_code == 200 and appmod.S15_OBS_SAVED_MESSAGE in _body(r)
    r = _observe(client, sid, form, OBS2)
    assert r.status_code == 503
    assert appmod.S15_PREP_UNAVAILABLE_MESSAGE in _body(r)
    with pytest.raises(SubsystemInterfacesCorrupt):
        _store().append_interface_observation(sid, _root(ifc.interface_id, OBS2), "k-c")
    with pytest.raises(SubsystemInterfacesCorrupt):
        _store().load_interface_observations(sid)
    assert len(_rows(sid)) == 1                                     # nothing written


def test_malformed_history_fails_only_the_observation_surface_closed(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _observe(client, sid, _record_form(client, sid, iid), OBS)
    form = _record_form(client, sid, iid)
    _raw("UPDATE %s SET observation_text = '  padded  ' WHERE project_id = ?" % TABLE,
         (sid,), ignore_checks=True)
    with pytest.raises(InterfaceObservationsCorrupt):
        _store().load_interface_observations(sid)
    page = _page(client, sid)
    assert ui_text.text("UI_S15_OBS_UNAVAILABLE", "en") in page      # closed, not partial
    assert "padded" not in page and "data-obs-chain" not in page
    assert _forms(_page_raw(client, sid)) == []                      # nothing offered
    assert 'name="%s' % _field(F_C, iid) in _page_raw(client, sid)   # preparation still works
    assert _save(client, sid, {(F_C, iid): COND}).status_code == 200
    assert _prep_rows(sid) == [(iid, COND, None, None)]
    r = _observe(client, sid, form, OBS2)                            # never appended on top
    assert r.status_code in (400, 503)
    assert len(_rows(sid)) == 1
    assert client.get("/session/%s" % sid).status_code == 200       # progression unaffected


@pytest.mark.parametrize("mutation", [
    "UPDATE {t} SET observation_seq = observation_seq + 5 WHERE project_id = ?",
    "UPDATE {t} SET ctx_operating_conditions = 'x' WHERE project_id = ? AND supersedes_observation_id IS NOT NULL",
    "UPDATE {t} SET supersedes_observation_id = observation_id WHERE project_id = ? AND observation_seq = 1",
    "UPDATE {t} SET observation_id = 'obs-zz' WHERE project_id = ? AND observation_seq = 1",
])
def test_every_malformed_durable_row_fails_the_whole_history_closed(client, mutation):
    sid, ifc = _integrated_with_interface(client)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    [root] = _events(sid)
    _observe(client, sid, _correct_form(client, sid, root.observation_id), OBS2)
    _raw(mutation.format(t=TABLE), (sid,), fk=False, ignore_checks=True)
    with pytest.raises(InterfaceObservationsCorrupt):
        _store().load_interface_observations(sid)
    with pytest.raises(InterfaceObservationsCorrupt):
        _store().committed_interface_observation_for_submission(sid, "any")


def test_an_observation_orphaned_from_this_projects_interfaces_fails_closed(client):
    sid, ifc = _integrated_with_interface(client)
    other, theirs = _integrated_with_interface(client)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    _raw("UPDATE %s SET interface_id = ? WHERE project_id = ?" % TABLE,
         (theirs.interface_id, sid), fk=False)                     # never remapped back
    with pytest.raises(InterfaceObservationsCorrupt):
        _store().load_interface_observations(sid)
    with pytest.raises(InterfaceObservationsCorrupt):
        _store().append_interface_observation(sid, _root(ifc.interface_id, OBS2), "k-orphan")
    assert ui_text.text("UI_S15_OBS_UNAVAILABLE", "en") in _page(client, sid)
    assert _events(other) == ()


# ==========================================================================
# 7. Text bounds and the project cap
# ==========================================================================
def test_observation_text_is_trimmed_bounded_and_never_truncated(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    for bad, message in (("", appmod.S15_OBS_INVALID_MESSAGE),
                         ("   \n  ", appmod.S15_OBS_INVALID_MESSAGE),
                         ("x" * 1001, appmod.S15_OBS_TOO_LONG_MESSAGE),
                         ("a\x00b", None)):
        r = _observe(client, sid, _record_form(client, sid, iid), bad)
        assert r.status_code == 400
        if message:
            assert message in _body(r)
    assert _events(sid) == ()
    multi = "Line one.\nLine two."
    _observe(client, sid, _record_form(client, sid, iid), "  " + multi + "  ")
    _observe(client, sid, _record_form(client, sid, iid), "y" * 1000)
    assert [e.observation_text for e in _events(sid)] == [multi, "y" * 1000]
    for bad in ("", " x", "a\x00b", "x" * 1001, 7):
        with pytest.raises(io.ObservationError):
            _root(iid, bad)


def test_the_project_cap_refuses_event_201_without_pruning(client):
    sid, ifc = _integrated_with_interface(client)
    store = _store()
    for k in range(io.MAX_OBSERVATIONS_PER_PROJECT):
        store.append_interface_observation(sid, _root(ifc.interface_id, "check %d" % k),
                                           "cap-%d" % k)
    before = _rows(sid)
    assert len(before) == 200
    with pytest.raises(InterfaceObservationCapReached):
        store.append_interface_observation(sid, _root(ifc.interface_id, "one more"), "cap-x")
    head = _events(sid)[-1]
    with pytest.raises(InterfaceObservationCapReached):             # corrections count too
        store.append_interface_observation(sid, io.recorded_correction(
            ifc.interface_id, "fix", head.observation_id), "cap-y")
    r = _observe(client, sid, _record_form(client, sid, ifc.interface_id), "one more")
    assert r.status_code == 400 and appmod.S15_OBS_CAP_MESSAGE in _body(r)
    assert _rows(sid) == before                                     # nothing pruned or rewritten


# ==========================================================================
# 8. Migration and writer surface
# ==========================================================================
def test_migration_is_additive_idempotent_and_never_backfills(tmp_path):
    path = str(tmp_path / "obs.db")
    store = SqliteRecordStore(path)
    pid, [item] = _store_project(store)
    store.apply_interface_preparation_delta(pid, {item.interface_id: {F_C: COND}})
    store.close()
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE %s" % TABLE)                           # a pre-slice database
    conn.commit()
    before = conn.execute("SELECT * FROM subsystem_interface_preparations").fetchall()
    conn.close()
    SqliteRecordStore(path).close()
    again = SqliteRecordStore(path)
    assert again.load_interface_observations(pid) == ()            # nothing backfilled
    assert again.load_interface_preparations(pid)[0].operating_conditions == COND
    again.close()
    conn = sqlite3.connect(path)
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(%s)" % TABLE)]
        indexes = {r[1] for r in conn.execute("PRAGMA index_list(%s)" % TABLE)}
        assert conn.execute("SELECT * FROM subsystem_interface_preparations").fetchall() == before
    finally:
        conn.close()
    assert cols == ["project_id", "observation_seq", "observation_id", "interface_id",
                    "observation_text", "supersedes_observation_id", "submission_key",
                    "recorded_at", "ctx_operating_conditions", "ctx_acceptance_criterion",
                    "ctx_evidence_needed"]
    assert {"subsystem_interface_observations_id_uq",
            "subsystem_interface_observations_successor_uq"} <= indexes
    for banned in ("outcome", "status", "verdict", "pass", "fail", "valid", "quality",
                   "readiness", "compatib", "confidence", "score", "irl"):
        assert not any(banned in c for c in cols), banned


def test_no_update_delete_or_withdraw_writer_exists():
    source = open(os.path.join("engine", "record_store.py"), encoding="utf-8").read()
    assert not re.search(r"UPDATE\s+%s" % TABLE, source)
    assert not re.search(r"DELETE\s+FROM\s+%s" % TABLE, source)
    assert source.count("INSERT INTO %s" % TABLE) == 1
    writers = [n for n in dir(SqliteRecordStore) if "observation" in n.lower()]
    assert sorted(writers) == ["_OBSERVATION_COLUMNS", "_migrate_interface_observations",
                               "_validated_observations",
                               "append_interface_observation",
                               "committed_interface_observation_for_submission",
                               "load_interface_observations"]
    owner = open(os.path.join("engine", "interface_observation.py"), encoding="utf-8").read()
    assert "experiment_result" not in owner                          # no CAP-09 coupling
    model = open(os.path.join("engine", "subsystem_model.py"), encoding="utf-8").read()
    assert "interface_observation" not in model                      # no reverse dependency


def test_the_database_refuses_a_malformed_id_and_a_correction_with_context(client):
    sid, ifc = _integrated_with_interface(client)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    root = list(_rows(sid)[0])
    for patch in ({2: "obs-" + "Z" * 32}, {2: "res-" + "a" * 32},
                  {2: io.new_observation_id(), 5: root[2], 8: "ctx"},
                  {2: io.new_observation_id(), 4: "x" * 1001}):
        row = list(root)
        row[1], row[6] = 9, "raw-%d" % len(patch)
        for i, v in patch.items():
            row[i] = v
        with pytest.raises(sqlite3.IntegrityError):
            _raw("INSERT INTO %s VALUES (%s)" % (TABLE, ",".join("?" * len(row))), row)


# ==========================================================================
# 9. Reload / restart / cold load and the page surface
# ==========================================================================
def test_history_survives_reload_restart_and_cold_load(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_A, iid): ACCEPT})
    _observe(client, sid, _record_form(client, sid, iid), OBS)
    [root] = _events(sid)
    _observe(client, sid, _correct_form(client, sid, root.observation_id), OBS2)
    _observe(client, sid, _record_form(client, sid, iid), "A retest.")
    before = _events(sid)
    for _ in range(2):                                                # plain reloads
        assert OBS2 in _page(client, sid)
    _restart()                                                        # no live session
    assert sid not in appmod.SESSION_STORE
    assert _events(sid) == before
    page = _page(client, sid)                                        # cold durable load
    assert OBS in page and OBS2 in page and "A retest." in page and ACCEPT in page
    assert PARTS["mech_part_name"] in page                           # the interaction named
    assert sid not in appmod.SESSION_STORE or not getattr(
        appmod.SESSION_STORE[sid]["state"], "interface_observations", None)
    visible = _visible(re.sub(r"<style.*?</style>", " ", _page_raw(client, sid), flags=re.S))
    for leaked in (root.observation_id, "obs-", "ifc-", "sub-", "interface_id",
                   "observation_id", TABLE):
        assert leaked not in visible


def test_observation_forms_are_separate_from_the_preparation_form(client):
    sid, ifc = _integrated_with_interface(client)
    raw = _page_raw(client, sid)
    forms = re.findall(r"<form\b.*?</form>", raw, re.S)
    [prep] = [f for f in forms if "interface-preparation" in f.split(">", 1)[0]]
    assert "observation_text" not in prep and "observation_submission" not in prep
    for form in forms:
        if "interface-observation" in form.split(">", 1)[0]:
            assert "prep_" not in form
    assert raw.count("<form") == len(forms)                          # never nested
    assert all(f.count("<form") == 1 for f in forms)
    assert len([f for f in forms if "interface-observation" in f.split(">", 1)[0]]) == 1


def test_an_integrated_project_without_interfaces_offers_no_observation(client):
    from tests.test_stage15_integrated_invention_entry import TIE_IDEA, _compose, _created
    sid = _created(_compose(client, TIE_IDEA))
    page = _page(client, sid)
    assert ui_text.text("UI_S15_PREP_NO_INTERFACES", "en") in page
    assert ui_text.text("UI_S15_OBS_HEADING", "en") not in page
    assert _forms(_page_raw(client, sid)) == []


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_local_disclosure_sits_at_every_history_and_form(client, lang):
    sid, ifc = _integrated_with_interface(client)
    if lang == "ar":
        assert client.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS)
    _observe(client, sid, _record_form(client, sid, ifc.interface_id), OBS2)
    raw = _html.unescape(_page_raw(client, sid))
    chains = re.findall(r'<div class="obs-chain" data-obs-chain>(.*?)<details><summary>'
                        + re.escape(ui_text.text("UI_S15_OBS_CORRECT", lang)), raw, re.S)
    assert len(chains) == 2
    for chain in chains:                                            # at each history entry
        assert ui_text.text("UI_S15_OBS_LABEL", lang) in chain
        assert ui_text.text("UI_S15_OBS_CONTEXT_NOTE", lang) in chain
    [note] = re.findall(r"data-obs-record-note>(.*?)</p>", raw, re.S)  # at the form
    assert note == ui_text.text("UI_S15_OBS_RECORD_NOTE", lang).format(limit=1000)
    for key in ("UI_S15_OBS_LABEL", "UI_S15_OBS_RECORD_NOTE"):
        copy = ui_text.text(key, "en")
        assert "not checked or validated by InventorAI" in copy
        assert "does not decide whether the acceptance criterion was met" in copy
    assert "not a claim about the conditions actually used" in ui_text.text(
        "UI_S15_OBS_CONTEXT_NOTE", "en")
    assert OBS in raw and OBS2 in raw                                # verbatim in both languages
    if lang == "ar":
        assert 'dir="rtl"' in raw or "dir='rtl'" in raw


def test_no_verdict_or_approval_wording_is_rendered(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_C, iid): COND, (F_A, iid): ACCEPT, (F_E, iid): EVID})
    r = _observe(client, sid, _record_form(client, sid, iid), OBS)
    for surface in (_section(_body(r)), _section(_page(client, sid))):
        for word in ("PASS", "FAIL", "Pass", "Fail", "PARTIAL", "INCONCLUSIVE", "Verified",
                     "verified", "Criterion met", "criterion is met", "Compatible",
                     "compatibility established", "Approved", "approved", "Ready",
                     "✓", "✔", "✗"):
            assert word not in surface, word
    obs_keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_S15_OBS_")]
    for key in obs_keys:
        for word in ("نجح", "فشل", "ناجح", "فاشل", "مُعتمد", "متوافق"):
            assert word not in ui_text.UI_STRINGS[key]["ar"], (key, word)


def test_every_new_catalogue_key_and_message_is_bilingual():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_S15_OBS_")]
    assert len(keys) >= 20
    for key in keys:
        assert ui_text.UI_STRINGS[key].get("en") and ui_text.UI_STRINGS[key].get("ar")
        assert ui_text.text(key, "en") != ui_text.text(key, "ar")
    for message in (appmod.S15_OBS_NOT_SAVED_MESSAGE, appmod.S15_OBS_SAVED_MESSAGE,
                    appmod.S15_OBS_INVALID_MESSAGE, appmod.S15_OBS_TOO_LONG_MESSAGE,
                    appmod.S15_OBS_NOT_CURRENT_MESSAGE, appmod.S15_OBS_STALE_MESSAGE,
                    appmod.S15_OBS_CAP_MESSAGE, appmod.S15_OBS_UNKNOWN_MESSAGE):
        assert ui_text.localize_message(message, "en") == message
        assert ui_text.localize_message(message, "ar") != message


# ==========================================================================
# 10. No effect on any other project truth; page-only
# ==========================================================================
def _landscape_and_plan(sid):
    state = SR.reconstruct_readonly_state(_store(), sid).state
    return derive_requirement_landscape(state), derive_validation_plan(state)


def test_recording_changes_no_progression_gap_readiness_evidence_or_plan_truth(client):
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_C, iid): COND, (F_A, iid): ACCEPT, (F_E, iid): EVID})

    def snapshot():
        st = appmod.SESSION_STORE[sid]["state"]
        return (len(st.assertions),
                [(r.record_id, getattr(r, "validation_status", None),
                  getattr(r, "quality", None), getattr(r, "provenance", None))
                 for r in st.assertions],
                _progression_snapshot(sid), st.domain,
                [s.subsystem_id for s in st.subsystems],
                [i.interface_id for i in st.subsystem_interfaces],
                _prep_rows(sid), _store().load_evidence_references(sid),
                _store().load_readiness_evidence(sid))
    before = snapshot()
    landscape, plan = _landscape_and_plan(sid)
    _observe(client, sid, _record_form(client, sid, iid), OBS)
    [root] = _events(sid)
    _observe(client, sid, _correct_form(client, sid, root.observation_id), OBS2)
    _observe(client, sid, _record_form(client, sid, iid), OBS)
    assert snapshot() == before
    assert _landscape_and_plan(sid) == (landscape, plan)             # rows / steps unchanged
    assert [s for s in plan.steps if s.provenance.anchor_kind == "subsystem_interface"]
    assert readiness_snapshot(appmod.SESSION_STORE[sid]["state"], ())["rows"][0][
        "verified_contexts"] == 0


def test_report_pdf_and_structured_export_are_unchanged(client, monkeypatch):
    from engine import read_export_service as rx
    sid, ifc = _integrated_with_interface(client)
    iid = ifc.interface_id
    _save(client, sid, {(F_C, iid): COND})

    def export():
        store = _store()
        return rx._compose_export(store.load_contract(sid), rx._domain_support_state(store, sid))

    def stable(source):
        # Only the render time and the CSRF token differ between renders.
        source = re.sub(r'name="csrf_token" value="[^"]*"', "", source)
        return re.sub(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|\+00:00)", "T", source)

    def report():
        return stable(client.get("/session/%s/deliverable" % sid).get_data(as_text=True))
    report_before, export_before = report(), export()
    pdf_before = stable(_pdf_source(client, sid, monkeypatch))
    _observe(client, sid, _record_form(client, sid, iid), OBS)
    [root] = _events(sid)
    _observe(client, sid, _correct_form(client, sid, root.observation_id), OBS2)
    assert report() == report_before
    assert export() == export_before
    pdf_after = stable(_pdf_source(client, sid, monkeypatch))
    assert pdf_after == pdf_before
    for surface in (report_before, pdf_after, repr(export_before)):
        assert OBS not in surface and OBS2 not in surface
    for path in (os.path.join("web", "templates", "deliverable.html"),
                 os.path.join("engine", "read_export_service.py"),
                 os.path.join("engine", "export_adapter.py"),
                 os.path.join("engine", "deliverable_assembler.py"),
                 os.path.join("engine", "validation_plan.py"),
                 os.path.join("engine", "requirement_landscape.py"),
                 os.path.join("engine", "readiness_snapshot.py")):
        source = open(path, encoding="utf-8").read()
        assert not any(p in source for p in _CONSUMER_PATTERNS), path


_CONSUMER_PATTERNS = ("engine import interface_observation", "engine.interface_observation",
                      "load_interface_observations", "append_interface_observation",
                      "committed_interface_observation_for_submission")


def test_the_observation_owner_has_no_consumer_outside_its_page():
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    consumers = []
    for folder in ("engine", "web"):
        for dirpath, _dirs, files in os.walk(os.path.join(root, folder)):
            for name in files:
                if not name.endswith(".py"):
                    continue
                path = os.path.join(dirpath, name)
                source = open(path, encoding="utf-8").read()
                if any(p in source for p in _CONSUMER_PATTERNS):
                    consumers.append(os.path.relpath(path, root).replace(os.sep, "/"))
    assert sorted(consumers) == ["engine/record_store.py", "web/app.py"]
    app_source = open(os.path.join(root, "web", "app.py"), encoding="utf-8").read()
    assert app_source.count("load_interface_observations(") == 1     # the page view only


def test_history_validation_refuses_malformed_chains():
    iid, other = sm.new_interface_id(), sm.new_interface_id()
    root = _root(iid, "one")
    fix = io.recorded_correction(iid, "two", root.observation_id)
    retest = _root(iid, "one")                                      # identical text, new root
    assert io.validate_observation_history([root, fix, retest]) == (root, fix, retest)
    assert io.head_ids([root, fix, retest]) == {fix.observation_id, retest.observation_id}
    for bad in ([fix],                                               # orphan correction
                [fix, root],                                         # target not EARLIER
                [root, fix, io.recorded_correction(iid, "3", root.observation_id)],  # fork
                [root, io.recorded_correction(other, "x", root.observation_id)],     # crosses
                [root, root],                                        # duplicate identity
                [root.__class__(root.observation_id, iid, "x", None, "t", None)],    # no context
                [root, fix.__class__(io.new_observation_id(), iid, "x", root.observation_id,
                                     "t", io.ObservationContext())],                 # ctx on fix
                [_root(iid, "c%d" % k) for k in range(io.MAX_OBSERVATIONS_PER_PROJECT + 1)]):
        with pytest.raises(io.ObservationError):
            io.validate_observation_history(bad)
    with pytest.raises(io.ObservationError):
        io.recorded_root("ifc-bad", "x", io.ObservationContext())
    with pytest.raises(io.ObservationError):                         # context bound = prep bound
        io.recorded_root(iid, "x", io.ObservationContext(evidence_needed="e" * 1001))
    assert io.context_from_preparation(None) == io.ObservationContext(None, None, None)
    assert io.context_from_preparation(sm.InterfacePreparation(iid, acceptance_criterion=ACCEPT)) \
        == io.ObservationContext(None, ACCEPT, None)
