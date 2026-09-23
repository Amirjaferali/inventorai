"""Stage 19 / CAP-09 — durable SuccessCriterion remediation (IMPLEMENTATION-01).

File-creation contract:
  Path: tests/test_stage19_durable_success_criteria.py
  Purpose: prove that the EXISTING user-authored ``SuccessCriterion`` planning
    metadata — keyed to the canonical Section-11 stable ``experiment_id`` — is
    durable through the saved-project architecture: it survives process/session
    memory loss and a same-database reopen, it is attached to every state that
    Section 11 actually consumes, edits are validated against CURRENT durable
    project truth (never a stale cached session), the submitted delta commits
    atomically, and absence / stale / unavailable / corruption stay distinct.
  Input contract: the live web app, the conftest per-test on-disk SQLite
    database, and REAL /start -> answer journeys (Electronics and Mechanical).
    A "restart" clears SESSION_STORE, closes the application store and drops the
    handle, so the next request reopens the SAME database file with a fresh
    store — the governed P4-2/PC1/PC2 convention.
  Output contract: pass/fail evidence only.
  Prohibited behaviors: no activation doubles; no fabricated results; the only
    doubles are named, bounded failure injections (documented inline).
"""
import html
import re
import sqlite3

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from engine.record_store import SqliteRecordStore
from tests.csrf_client import csrf_client

PREFIX = "criterion__"
ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"
ELEC_ANSWERS = (
    "The problem is that cyclists have no reliable brake light. My circuit senses "
    "deceleration with an accelerometer because sudden voltage change on the "
    "sensor indicates braking, so the microcontroller switches the LED because "
    "riders behind need warning.",
    "The mechanism works because the accelerometer outputs a voltage proportional "
    "to deceleration; the microcontroller reads it through the ADC and drives the "
    "LED through a transistor because the LED current exceeds the GPIO limit.",
    "I do not know how much deceleration should count as braking. I assume the "
    "battery will last a full ride.",
    "I am not sure whether rain affects the sensor. The design assumes the LED is "
    "bright enough in daylight.",
)
# A fifth answer that adds a THIRD acknowledged unknown, which displaces the
# reasoned-leading-claim experiment from the three-item plan.
ELEC_DISPLACING_ANSWER = "I don't know yet what the right threshold is."
MECH_IDEA = ("A door hinge with a torsion spring and a rotary damper that closes "
             "the door slowly")
MECH_ANSWERS = (
    "The problem is that doors slam shut in the wind. My hinge uses a spring and a "
    "friction damper because the damper resists fast rotation, so the door closes "
    "slowly.",
    "The mechanism works because the viscous damper produces torque proportional "
    "to angular speed, and the torsion spring returns the door to closed.",
    "I do not know how stiff the spring should be. I assume the damper oil stays "
    "viscous in winter.",
    "I am not sure whether the hinge pin will wear out. The design assumes the door "
    "weighs under 30 kilograms.",
)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _answer_token(client, sid):
    body = client.get("/session/" + sid).get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', body)
    return m.group(1) if m else None


def _answer(client, sid, response):
    r = client.post("/session/" + sid, data={
        "response": response, "action": "answered",
        "answer_token": _answer_token(client, sid)})
    assert r.status_code == 302, r.status_code
    return r


def _journey(client, idea=ELEC_IDEA, domain="electronics_electrical",
             answers=ELEC_ANSWERS):
    r = client.post("/start", data={"idea": idea, "domain_confirm": domain})
    assert r.status_code == 302, r.status_code
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    for a in answers:
        _answer(client, sid, a)
    return sid


def _restart():
    """Process/session memory loss + a SAME-database reopen: drop every live
    session, close the application store and drop its handle, so the next
    request constructs a fresh SqliteRecordStore on the same file."""
    SESSION_STORE.clear()
    store = webapp._STORE
    if store is not None:
        store.close()
    webapp._STORE = None


def _plan_items(state):
    from engine.deliverable_assembler import assemble_deliverable
    return assemble_deliverable(state)["section_11_prototype_test_plan"]["items"]


def _live_ids(sid):
    return [it["experiment_id"] for it in _plan_items(SESSION_STORE[sid]["state"])]


def _post_criteria(client, sid, mapping):
    return client.post("/session/%s/success-criteria" % sid,
                       data={PREFIX + k: v for k, v in mapping.items()})


def _report(client, sid):
    return html.unescape(client.get("/session/%s/deliverable" % sid)
                         .get_data(as_text=True))


def _db_path():
    import os
    return os.environ["INVENTORAI_DB_PATH"]


# ==========================================================================
# BASE RED — the defect, reproduced through the real application
# ==========================================================================
def test_red_saved_criterion_survives_memory_loss_and_same_db_reopen(client):
    """A criterion saved through the real route must still be attached to the
    SAME stable experiment_id after memory loss and a same-database reopen."""
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    r = _post_criteria(client, sid, {eid: "Brake light visible at 50 m in daylight"})
    assert r.status_code == 302
    _restart()
    fresh = csrf_client(app)
    with app.test_request_context():
        context = webapp._deliverable_context(sid)
    assert context is not None
    items = context[1]["section_11_prototype_test_plan"]["items"]
    by_id = {it["experiment_id"]: it for it in items}
    assert eid in by_id
    assert by_id[eid]["success_criterion"] == "Brake light visible at 50 m in daylight"
    assert by_id[eid]["success_criterion_provenance"] == "user_defined"
    assert "Brake light visible at 50 m in daylight" in _report(fresh, sid)


def test_red_fresh_store_creates_the_additive_sidecar_table(tmp_path):
    path = str(tmp_path / "fresh.sqlite")
    SqliteRecordStore(path).close()
    with sqlite3.connect(path) as conn:
        names = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert "prototype_plan_metadata" in names


def test_red_stale_cached_ids_are_refused_after_a_committed_correction(client, monkeypatch):
    """Freshness: a durable correction commits but the live replacement fails,
    so SESSION_STORE still holds the OLD plan. An edit keyed to an experiment
    that only the stale cache still generates must be refused."""
    sid = _journey(client, answers=ELEC_ANSWERS + (ELEC_DISPLACING_ANSWER,))
    state = SESSION_STORE[sid]["state"]
    cached_ids = _live_ids(sid)
    displacing = [r for r in state.assertions
                  if r.disposition == "answered" and r.content == ELEC_DISPLACING_ANSWER][0]
    token = _answer_token(client, sid)
    real = webapp.reconstruct_readonly_state
    calls = {"n": 0}

    def fail_once(store, project_id):
        # Bounded injection: ONLY the correction route's post-append replay fails,
        # so the durable correction commits while the live replacement does not.
        calls["n"] += 1
        raise RuntimeError("injected replay failure")

    monkeypatch.setattr(webapp, "reconstruct_readonly_state", fail_once)
    r = client.post("/session/%s/correct" % sid, data={
        "supersedes_record_id": displacing.record_id,
        "response": "The threshold will be chosen by measuring real stops.",
        "answer_token": token})
    assert r.status_code == 302 and calls["n"] == 1
    monkeypatch.setattr(webapp, "reconstruct_readonly_state", real)
    # The stale cache still generates the displaced third-unknown experiment.
    assert _live_ids(sid) == cached_ids
    current = real(webapp._get_store(), sid)
    current_ids = [it["experiment_id"] for it in _plan_items(current.state)]
    obsolete = [eid for eid in cached_ids if eid not in current_ids]
    assert obsolete, "the correction must change the durable plan"
    r = _post_criteria(client, sid, {obsolete[0]: "must not be accepted"})
    assert r.status_code == 400
    with app.test_request_context():
        assert webapp._get_store().load_success_criteria(sid) == ()


# ==========================================================================
# Shared GREEN helpers
# ==========================================================================
import copy
import hashlib

from engine import account_credentials as _acct
from engine.deliverable_assembler import _experiment_id
from engine.record_contract import assertion_to_dict
from engine.record_store import (
    ProjectNotFound, SuccessCriterionCorrupt, SuccessCriterionInvalid,
)
from engine.session_reconstruction import RECONSTRUCTION_VERSION

PW = "correct horse battery staple"
VIEW_ONLY = webapp.SC_VIEW_ONLY_MESSAGE
NOT_SAVED = webapp.SC_NOT_SAVED_MESSAGE
SAVED_NOT_SHOWN = webapp.SC_SAVED_NOT_SHOWN_MESSAGE
NOT_A_PROJECT = webapp.SC_NOT_SAVED_PROJECT_MESSAGE
CRITERIA_UNAVAILABLE = webapp.SC_CRITERIA_UNAVAILABLE_MESSAGE
PLAN_UNAVAILABLE = webapp.SC_PLAN_UNAVAILABLE_MESSAGE


def _durable(sid):
    """The DURABLE collection, read through the application store."""
    return dict(webapp._get_store().load_success_criteria(sid))


def _raw_rows(sid):
    con = sqlite3.connect(_db_path())
    try:
        return con.execute(
            "SELECT experiment_id, success_criterion FROM prototype_plan_metadata "
            "WHERE project_id = ? ORDER BY experiment_id", (sid,)).fetchall()
    finally:
        con.close()


def _insert_raw(sid, experiment_id, criterion):
    """Test-only corruption injection: bypass the store (and its CHECKs)."""
    con = sqlite3.connect(_db_path())
    try:
        con.execute("PRAGMA ignore_check_constraints = ON")
        con.execute("INSERT INTO prototype_plan_metadata VALUES (?, ?, ?)",
                    (sid, experiment_id, criterion))
        con.commit()
    finally:
        con.close()


def _reopened_items(sid):
    """Section-11 items of the SAME project after a restart, through the real
    saved-project deliverable seam (a fresh store on the same database)."""
    with app.test_request_context():
        context = webapp._deliverable_context(sid)
    assert context is not None
    return {it["experiment_id"]: it
            for it in context[1]["section_11_prototype_test_plan"]["items"]}


def _criteria_page(client, sid):
    r = client.get("/session/%s/success-criteria" % sid)
    return r, html.unescape(r.get_data(as_text=True))


def _mk_account(email, status="active"):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status=status)
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    return aid


def _client_for(email):
    aid = _mk_account(email)
    c = csrf_client(app)
    assert c.post("/login", data={"email": email, "password": PW}).status_code == 302
    return c, aid


def _legacy_journey(client, idea=MECH_IDEA, domain="mechanical", answers=MECH_ANSWERS):
    """A project genuinely CREATED under the pre-T2-G stamp (only the creation
    constant changes), so it is eligible for engine-version adoption."""
    original = webapp.CURRENT_ENGINE_CONTRACT_VERSION
    webapp.CURRENT_ENGINE_CONTRACT_VERSION = RECONSTRUCTION_VERSION
    try:
        r = client.post("/start", data={"idea": idea, "domain_confirm": domain})
    finally:
        webapp.CURRENT_ENGINE_CONTRACT_VERSION = original
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    for a in answers:
        _answer(client, sid, a)
    return sid


def _adopt(client, sid, action):
    return client.post("/session/%s/engine-version" % sid, data={
        "answer_token": _answer_token(client, sid), "version_action": action,
        "confirm_adoption": "yes"})


def _correct(client, sid, record_id, response):
    return client.post("/session/%s/correct" % sid, data={
        "supersedes_record_id": record_id, "response": response,
        "answer_token": _answer_token(client, sid)})


def _answered_record(sid, content):
    return [r for r in SESSION_STORE[sid]["state"].assertions
            if r.disposition == "answered" and r.content == content
            and r.superseded_by is None][0]


# ==========================================================================
# 1-3 — additive schema: fresh, migrated populated, idempotent
# ==========================================================================
def test_01_fresh_table_has_exactly_the_bounded_shape(tmp_path):
    path = str(tmp_path / "shape.sqlite")
    SqliteRecordStore(path).close()
    con = sqlite3.connect(path)
    try:
        cols = [(r[1], r[2], r[3], r[5]) for r in
                con.execute("PRAGMA table_info(prototype_plan_metadata)")]
        fks = [(r[2], r[3], r[4]) for r in
               con.execute("PRAGMA foreign_key_list(prototype_plan_metadata)")]
    finally:
        con.close()
    # ONLY the existing SuccessCriterion: no experiment definition, source,
    # provenance, result, validation, readiness or PASS/FAIL column.
    assert cols == [("project_id", "TEXT", 1, 1), ("experiment_id", "TEXT", 1, 2),
                    ("success_criterion", "TEXT", 1, 0)]
    assert fks == [("projects", "project_id", "project_id")]


def test_02_existing_populated_database_migrates_additively_without_loss(tmp_path, client):
    sid = _journey(client)
    before_contract = [assertion_to_dict(r)
                       for r in webapp._get_store().load_contract(sid).assertions]
    _restart()
    # Emulate a database written BEFORE this migration existed.
    con = sqlite3.connect(_db_path())
    con.execute("DROP TABLE prototype_plan_metadata")
    con.commit()
    counts = {t: con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
              for t in ("projects", "records")}
    con.close()
    store = SqliteRecordStore(_db_path())
    try:
        assert [assertion_to_dict(r) for r in store.load_contract(sid).assertions] \
            == before_contract
        assert store.load_success_criteria(sid) == ()
    finally:
        store.close()
    con = sqlite3.connect(_db_path())
    try:
        assert {t: con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
                for t in ("projects", "records")} == counts
    finally:
        con.close()


def test_03_repeated_initialization_is_idempotent_and_keeps_rows(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    assert _post_criteria(client, sid, {eid: "kept across inits"}).status_code == 302
    _restart()
    for _ in range(3):
        SqliteRecordStore(_db_path()).close()
    assert _raw_rows(sid) == [(eid, "kept across inits")]


# ==========================================================================
# 4-7, 35 — real save -> memory loss -> same-DB reopen, both domains
# ==========================================================================
@pytest.mark.parametrize("idea,domain,answers", [
    (ELEC_IDEA, "electronics_electrical", ELEC_ANSWERS),
    (MECH_IDEA, "mechanical", MECH_ANSWERS),
])
def test_04_07_35_criterion_survives_restart_on_the_same_id_in_both_domains(
        client, idea, domain, answers):
    sid = _journey(client, idea, domain, answers)
    ids = _live_ids(sid)
    assert len(ids) >= 2
    assert _post_criteria(client, sid, {ids[0]: "target survives a restart"}).status_code == 302
    _restart()
    items = _reopened_items(sid)
    assert set(items) == set(ids)                   # same stable identities
    assert items[ids[0]]["success_criterion"] == "target survives a restart"
    assert items[ids[0]]["success_criterion_provenance"] == "user_defined"
    for other in ids[1:]:                           # attached to THAT id only
        assert items[other]["success_criterion_status"] == "required"


def test_05_direct_saved_project_html_report_after_restart(client):
    sid = _journey(client)
    eid = _live_ids(sid)[1]
    _post_criteria(client, sid, {eid: "<b>visible</b> within 2 seconds"})
    _restart()
    fresh = csrf_client(app)                        # a new browser, no live session
    r = fresh.get("/session/%s/deliverable" % sid)
    assert r.status_code == 200
    raw = r.get_data(as_text=True)
    assert "&lt;b&gt;visible&lt;/b&gt; within 2 seconds" in raw   # escaped, verbatim
    assert "<b>visible</b>" not in raw


def test_06_pdf_source_carries_the_durable_criterion_after_restart(client, monkeypatch):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post_criteria(client, sid, {eid: "PDF carries this durable target"})
    _restart()
    seen = {}

    def capture(source):
        # Bounded double: capture the exact trusted source handed to the
        # renderer; the PDF engine itself is not under test here.
        seen["source"] = source
        return b"%PDF-1.7 captured"

    monkeypatch.setattr(webapp, "_render_pdf_bytes", capture)
    r = csrf_client(app).post("/session/%s/deliverable.pdf" % sid, data={})
    assert r.status_code == 200
    assert "PDF carries this durable target" in seen["source"]


# ==========================================================================
# 8-12 — edit, delete, omitted, multiple, mixed: all durable across restart
# ==========================================================================
def test_08_09_10_edit_delete_and_omitted_persist_across_restart(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_criteria(client, sid, {ids[0]: "first", ids[1]: "second", ids[2]: "third"})
    _post_criteria(client, sid, {ids[0]: "first edited"})          # ids[1], ids[2] omitted
    _post_criteria(client, sid, {ids[1]: "  \t "})                  # whitespace deletes
    _restart()
    items = _reopened_items(sid)
    assert items[ids[0]]["success_criterion"] == "first edited"
    assert items[ids[1]]["success_criterion_status"] == "required"
    assert items[ids[2]]["success_criterion"] == "third"             # untouched
    assert _raw_rows(sid) == sorted([(ids[0], "first edited"), (ids[2], "third")])


def test_11_12_multiple_and_mixed_deltas_commit_as_one(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    assert _post_criteria(client, sid, {ids[0]: "a", ids[1]: "b"}).status_code == 302
    assert _durable(sid) == {ids[0]: "a", ids[1]: "b"}
    r = _post_criteria(client, sid, {ids[0]: "", ids[1]: "b2", ids[2]: "c"})
    assert r.status_code == 302
    assert _durable(sid) == {ids[1]: "b2", ids[2]: "c"}
    assert {k: v.criterion for k, v in
            SESSION_STORE[sid]["state"].success_criteria.items()} == _durable(sid)


class _FailOnSecondMutation:
    """Bounded failure injection: a proxy for the store connection that lets
    the FIRST criteria mutation run and fails the SECOND, inside the one
    transaction."""

    def __init__(self, conn):
        self._conn = conn
        self.mutations = 0

    def execute(self, sql, *args):
        if sql.lstrip().upper().startswith(("INSERT INTO PROTOTYPE_PLAN_METADATA",
                                            "DELETE FROM PROTOTYPE_PLAN_METADATA")):
            self.mutations += 1
            if self.mutations == 2:
                raise sqlite3.OperationalError("injected failure between mutations")
        return self._conn.execute(sql, *args)

    def __getattr__(self, name):
        return getattr(self._conn, name)


def test_13_failure_between_mutations_rolls_back_everything(client, monkeypatch):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_criteria(client, sid, {ids[2]: "keep me"})
    live = SESSION_STORE[sid]["state"]
    memory_before = copy.deepcopy(live.success_criteria)
    store = webapp._get_store()
    proxy = _FailOnSecondMutation(store._conn)
    monkeypatch.setattr(store, "_conn", proxy)
    r = _post_criteria(client, sid, {ids[0]: "would be first", ids[2]: "   "})
    monkeypatch.setattr(store, "_conn", proxy._conn)
    assert proxy.mutations == 2                       # one mutation DID run first
    assert r.status_code == 503
    body = html.unescape(r.get_data(as_text=True))
    assert NOT_SAVED in body and SAVED_NOT_SHOWN not in body
    assert _durable(sid) == {ids[2]: "keep me"}        # durable unchanged
    assert live.success_criteria == memory_before     # memory unchanged


@pytest.mark.parametrize("failure", ["publication", "redirect"])
def test_14_post_commit_failure_is_never_reported_as_not_saved(client, monkeypatch, failure):
    sid = _journey(client)
    ids = _live_ids(sid)
    originals = (webapp._attach_success_criteria, webapp.redirect)
    if failure == "publication":
        real = webapp._attach_success_criteria
        calls = {"n": 0}

        def attach(sid_, state):
            # Call 1 establishes the current plan BEFORE the commit; call 2 is
            # the post-commit publication, which is made to fail.
            calls["n"] += 1
            return False if calls["n"] == 2 else real(sid_, state)

        monkeypatch.setattr(webapp, "_attach_success_criteria", attach)
    else:
        def broken_redirect(*a, **k):
            raise RuntimeError("injected redirect failure")

        monkeypatch.setattr(webapp, "redirect", broken_redirect)
    r = _post_criteria(client, sid, {ids[0]: "committed one", ids[1]: "committed two"})
    body = html.unescape(r.get_data(as_text=True))
    assert r.status_code == 200
    assert SAVED_NOT_SHOWN in body and NOT_SAVED not in body
    # Restore ONLY what this test replaced (monkeypatch.undo() would also
    # revert the conftest per-test database path).
    monkeypatch.setattr(webapp, "_attach_success_criteria", originals[0])
    monkeypatch.setattr(webapp, "redirect", originals[1])
    _restart()
    items = _reopened_items(sid)
    assert items[ids[0]]["success_criterion"] == "committed one"
    assert items[ids[1]]["success_criterion"] == "committed two"


# ==========================================================================
# 15-17, 23 — stale preserved, never remapped, exact-identity reattachment
# ==========================================================================
def test_15_16_17_23_stale_is_preserved_never_remapped_and_reattaches_by_identity(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    claim_id = [i for i in ids if "_reasoned_leading_claim_" in i][0]
    unknown_id = ids[0]
    _post_criteria(client, sid, {claim_id: "claim demonstrated at 20 km/h",
                                 unknown_id: "threshold measured on 10 stops"})
    # A further answer adds a third unknown that displaces the claim experiment.
    _answer(client, sid, ELEC_DISPLACING_ANSWER)
    current = _live_ids(sid)
    assert claim_id not in current and unknown_id in current
    report = _report(client, sid)
    assert "no longer matches a current proposed experiment" in report
    with app.test_request_context():
        package = webapp._deliverable_context(sid)[1]
    plan = package["section_11_prototype_test_plan"]
    assert [s["experiment_id"] for s in plan["stale_criteria"]] == [claim_id]
    # never remapped onto any current experiment (not by position, not by text)
    assert all(it["success_criterion"] != "claim demonstrated at 20 km/h"
               for it in plan["items"])
    assert _durable(sid)[claim_id] == "claim demonstrated at 20 km/h"   # preserved
    # A correction withdraws the displacing answer: the SAME canonical source
    # returns, so the SAME id is generated and the criterion reattaches.
    old_state = SESSION_STORE[sid]["state"]
    record = _answered_record(sid, ELEC_DISPLACING_ANSWER)
    assert _correct(client, sid, record.record_id,
                    "The threshold will be chosen by measuring real stops.").status_code == 302
    new_state = SESSION_STORE[sid]["state"]
    assert new_state is not old_state                                   # replaced (23)
    assert new_state.success_criteria[claim_id].criterion == "claim demonstrated at 20 km/h"
    assert new_state.success_criteria[unknown_id].criterion == "threshold measured on 10 stops"
    _restart()
    items = _reopened_items(sid)
    assert items[claim_id]["success_criterion"] == "claim demonstrated at 20 km/h"
    assert items[unknown_id]["success_criterion"] == "threshold measured on 10 stops"


# ==========================================================================
# 18-19 — whole-request rejection
# ==========================================================================
@pytest.mark.parametrize("bad", ["unknown", "over_limit"])
def test_18_19_invalid_submission_rejects_the_whole_request(client, bad):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_criteria(client, sid, {ids[2]: "pre-existing"})
    memory_before = copy.deepcopy(SESSION_STORE[sid]["state"].success_criteria)
    mapping = {ids[0]: "valid and would be saved", ids[2]: ""}
    if bad == "unknown":
        mapping["exp_v1_acknowledged_unknown_" + "9" * 32] = "rogue"
    else:
        mapping[ids[1]] = "x" * (webapp.MAX_CRITERION_LENGTH + 1)
    r = _post_criteria(client, sid, mapping)
    assert r.status_code == 400
    assert _durable(sid) == {ids[2]: "pre-existing"}
    assert SESSION_STORE[sid]["state"].success_criteria == memory_before


# ==========================================================================
# 20 — freshness: engine-version adoption committed, live replacement failed
# ==========================================================================
def test_20_adoption_freshness_uses_the_durable_effective_version(client, monkeypatch):
    sid = _legacy_journey(client)
    stale_live = SESSION_STORE[sid]["state"]
    assert stale_live.engine_contract_version == RECONSTRUCTION_VERSION
    real = webapp.reconstruct_readonly_state
    phase = {"eva": True}
    seen = []

    def recon(store, project_id):
        # Bounded injection: fail ONLY the adoption route's post-commit replay.
        if phase["eva"]:
            raise RuntimeError("injected replay failure")
        result = real(store, project_id)
        seen.append(result.state.engine_contract_version)
        return result

    monkeypatch.setattr(webapp, "reconstruct_readonly_state", recon)
    assert _adopt(client, sid, "adopt").status_code == 302
    assert SESSION_STORE[sid]["state"] is stale_live            # live NOT replaced
    phase["eva"] = False
    ids = [it["experiment_id"] for it in _plan_items(stale_live)]
    r = _post_criteria(client, sid, {ids[0]: "validated against durable truth"})
    assert r.status_code == 302
    # The edit was validated against the plan of the DURABLE effective version,
    # not against the stale cached legacy reading.
    assert seen and seen[0] == webapp.CURRENT_ENGINE_CONTRACT_VERSION
    assert _durable(sid) == {ids[0]: "validated against durable truth"}


# ==========================================================================
# 21-22 — cold view is view-only; explicit resume attaches before publishing
# ==========================================================================
def test_21_cold_view_uses_durable_truth_without_writable_resume(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post_criteria(client, sid, {eid: "cold readable target"})
    _restart()
    fresh = csrf_client(app)
    r, body = _criteria_page(fresh, sid)
    assert r.status_code == 200
    assert "cold readable target</textarea>" in body
    assert VIEW_ONLY in body
    from web.ui_text import text
    assert "readonly" in body
    assert ">%s</button>" % text("UI_B_SC_004", "en") not in body   # no save control
    assert text("UI_SC_SAVE_CLEAR", "en") not in body                 # no save guidance
    entry = SESSION_STORE.get(sid)
    assert entry is None or getattr(entry["state"], "domain", None) is None
    r = _post_criteria(fresh, sid, {eid: "must not be written from a cold view"})
    assert r.status_code == 409
    assert _durable(sid) == {eid: "cold readable target"}
    entry = SESSION_STORE.get(sid)
    assert entry is None or getattr(entry["state"], "domain", None) is None


def test_22_explicit_resume_attaches_criteria_before_publishing(client):
    sid = _journey(client)
    eid = _live_ids(sid)[1]
    _post_criteria(client, sid, {eid: "resumed target"})
    _restart()
    fresh = csrf_client(app)
    assert fresh.post("/session/%s/resume" % sid, data={}).status_code == 302
    state = SESSION_STORE[sid]["state"]
    assert getattr(state, "domain", None) is not None               # writable
    assert state.success_criteria[eid].criterion == "resumed target"
    assert state.success_criteria[eid].provenance == "user_defined"
    assert _post_criteria(fresh, sid, {eid: "edited after resume"}).status_code == 302
    assert _durable(sid) == {eid: "edited after resume"}


def _live_ids_after_restart(sid):
    recon = webapp.reconstruct_readonly_state(webapp._get_store(), sid)
    return [it["experiment_id"] for it in _plan_items(recon.state)]


def test_22b_resume_refuses_establishment_on_corrupt_metadata(client):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post_criteria(client, sid, {eid: "good"})
    _restart()
    _insert_raw(sid, _live_ids_after_restart(sid)[1], "  untrimmed  ")
    fresh = csrf_client(app)
    fresh.post("/session/%s/resume" % sid, data={})
    entry = SESSION_STORE.get(sid)
    assert entry is None or getattr(entry["state"], "domain", None) is None


# ==========================================================================
# 24 — engine-version adoption AND reversal replace state; criteria survive
# ==========================================================================
def test_24_adoption_and_reversal_carry_the_durable_criteria(client):
    sid = _legacy_journey(client)
    ids = _live_ids(sid)
    _post_criteria(client, sid, {ids[0]: "held across adoption", ids[1]: "and reversal"})
    for action in ("adopt", "revert"):
        before = SESSION_STORE[sid]["state"]
        assert _adopt(client, sid, action).status_code == 302
        after = SESSION_STORE[sid]["state"]
        assert after is not before                                   # replaced
        assert {k: v.criterion for k, v in after.success_criteria.items()} == {
            ids[0]: "held across adoption", ids[1]: "and reversal"}
        from engine.deliverable_assembler import assemble_deliverable
        plan = assemble_deliverable(after)["section_11_prototype_test_plan"]
        plan_ids = [it["experiment_id"] for it in plan["items"]]
        # Present on the current plan, or truthfully stale — never dropped.
        stale = {s["experiment_id"] for s in plan["stale_criteria"]}
        for eid in (ids[0], ids[1]):
            assert (eid in plan_ids) != (eid in stale)


# ==========================================================================
# 25-28 — isolation, authorization, NULL-owner, no session-only fallback
# ==========================================================================
def test_25_identical_experiment_ids_in_two_projects_stay_isolated(client):
    a = _journey(client)
    b = _journey(csrf_client(app))
    assert _live_ids(a) == _live_ids(b)                 # the SAME canonical ids
    eid = _live_ids(a)[0]
    _post_criteria(client, a, {eid: "project A only"})
    _post_criteria(client, b, {eid: "project B only"})
    _post_criteria(client, a, {eid: " "})               # delete in A
    assert _durable(a) == {}
    assert _durable(b) == {eid: "project B only"}
    assert "project A only" not in _report(client, b)
    assert "project B only" not in _report(client, a)


def test_26_owner_non_owner_anonymous_and_disabled_owner(client):
    owner, aid = _client_for("owner19@example.com")
    sid = _journey(owner)
    eid = _live_ids(sid)[0]
    assert _post_criteria(owner, sid, {eid: "owner target"}).status_code == 302
    other, _ = _client_for("other19@example.com")
    anon = csrf_client(app)
    for c in (other, anon):
        r = c.get("/session/%s/success-criteria" % sid)
        assert r.status_code == 302 and r.headers["Location"].endswith("/")
        r = _post_criteria(c, sid, {eid: "intruder"})
        assert r.status_code == 302 and r.headers["Location"].endswith("/")
    webapp._get_account_store().set_status(aid, "disabled", "2026-01-02T00:00:00.000000Z")
    r = _post_criteria(owner, sid, {eid: "disabled owner"})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert _durable(sid) == {eid: "owner target"}


def test_27_null_owner_durable_project_keeps_capability_access(client):
    sid = _journey(client)                              # anonymous -> NULL owner
    assert webapp._get_store().load_owner(sid) == (True, None)
    eid = _live_ids(sid)[0]
    holder = csrf_client(app)                           # another browser with the sid
    assert _post_criteria(holder, sid, {eid: "capability holder target"}).status_code == 302
    assert _durable(sid) == {eid: "capability holder target"}


def test_28_memory_only_context_never_falls_back_to_session_saving(client):
    from engine.idea_state import IdeaState, AcknowledgedUnknown, ASSUMPTION_INVENTORY
    sid = "mem-only-" + "0" * 8
    state = IdeaState(idea_id=sid)
    state.domain = "electronics_electrical"
    state.acknowledged_unknowns.append(AcknowledgedUnknown(
        iteration=1, gap_context=ASSUMPTION_INVENTORY,
        verbatim="I do not know the lockout count", category_basis="explicit"))
    SESSION_STORE[sid] = {"state": state, "last_result": None, "transcript": []}
    eid = [it["experiment_id"] for it in _plan_items(state)][0]
    r, body = _criteria_page(client, sid)
    assert r.status_code == 409 and NOT_A_PROJECT in body
    r = _post_criteria(client, sid, {eid: "would only live in memory"})
    assert r.status_code == 409
    assert NOT_A_PROJECT in html.unescape(r.get_data(as_text=True))
    assert state.success_criteria == {}
    assert webapp._get_store().load_owner(sid) == (False, None)


# ==========================================================================
# 29-31 — corruption and store failure fail closed; never a partial set
# ==========================================================================
@pytest.mark.parametrize("corruption", [
    ("valid_id", "  untrimmed  "),
    ("valid_id", b"blob-value"),
    ("not-an-experiment-id", "fine text"),
])
def test_29_corrupt_metadata_fails_closed_and_never_reads_as_empty(client, corruption):
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_criteria(client, sid, {ids[0]: "good one"})
    bad_id, bad_value = corruption
    _insert_raw(sid, ids[1] if bad_id == "valid_id" else bad_id, bad_value)
    with pytest.raises(SuccessCriterionCorrupt):
        webapp._get_store().load_success_criteria(sid)
    r, body = _criteria_page(client, sid)
    assert r.status_code == 503 and CRITERIA_UNAVAILABLE in body
    assert 'name="criterion__' not in body
    r = client.get("/session/%s/deliverable" % sid)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    r = _post_criteria(client, sid, {ids[2]: "blocked while corrupt"})
    assert r.status_code == 503
    _restart()
    r = csrf_client(app).get("/session/%s" % sid)          # cold load fails closed
    assert r.status_code == 302 and r.headers["Location"].endswith("/")


def test_30_store_unavailable_fails_closed(client, monkeypatch):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post_criteria(client, sid, {eid: "exists"})

    def unavailable(self, project_id):
        raise sqlite3.OperationalError("injected: database is locked")

    monkeypatch.setattr(SqliteRecordStore, "load_success_criteria", unavailable)
    r, body = _criteria_page(client, sid)
    assert r.status_code == 503 and CRITERIA_UNAVAILABLE in body
    r = client.get("/session/%s/deliverable" % sid)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    r = csrf_client(app).post("/session/%s/deliverable.pdf" % sid, data={})
    assert r.status_code == 302


def test_31_a_bad_row_never_yields_a_partial_attachment(client):
    from engine.idea_state import SuccessCriterion
    sid = _journey(client)
    ids = _live_ids(sid)
    _post_criteria(client, sid, {ids[0]: "good a", ids[2]: "good c"})
    _insert_raw(sid, ids[1], "\tbad\t")
    carrier = {"prior": SuccessCriterion("carrier before")}
    state = SESSION_STORE[sid]["state"]
    state.success_criteria = dict(carrier)
    assert webapp._attach_success_criteria(sid, state) is False
    assert state.success_criteria == carrier             # untouched, not the good subset


def test_plan_unavailable_is_not_reported_as_stale_or_empty(client, monkeypatch):
    sid = _journey(client)
    eid = _live_ids(sid)[0]
    _post_criteria(client, sid, {eid: "kept while plan unavailable"})

    def no_plan(store, project_id):
        raise RuntimeError("injected reconstruction unavailability")

    monkeypatch.setattr(webapp, "reconstruct_readonly_state", no_plan)
    r, body = _criteria_page(client, sid)
    assert r.status_code == 503 and PLAN_UNAVAILABLE in body
    from web.ui_text import text
    assert text("UI_B_SC_005", "en") not in body          # never "no experiments"
    assert "no longer matches" not in body                 # never "all stale"
    r = _post_criteria(client, sid, {eid: "cannot be validated now"})
    assert r.status_code == 503
    assert _durable(sid) == {eid: "kept while plan unavailable"}


# ==========================================================================
# 32-34 — never progression, contract, transcript, Evidence, results, readiness
# ==========================================================================
def test_32_33_34_criteria_stay_planning_metadata_only(client):
    sid = _journey(client)
    ids = _live_ids(sid)
    store = webapp._get_store()
    contract_before = [assertion_to_dict(r) for r in store.load_contract(sid).assertions]
    review_before = webapp.reconstruct_readonly_state(store, sid).review
    live = SESSION_STORE[sid]["state"]
    progression_before = (live.maturity_level, live.current_stage,
                          [(g.gap_type, g.status, len(g.evidence)) for g in live.gaps],
                          live.iteration, len(live.acknowledged_unknowns))
    transcript_before = copy.deepcopy(SESSION_STORE[sid]["transcript"])
    con = sqlite3.connect(_db_path())
    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name <> 'prototype_plan_metadata'")]
    counts_before = {t: con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
                     for t in tables}
    con.close()
    from engine.deliverable_assembler import assemble_deliverable
    package_before = assemble_deliverable(live)
    _post_criteria(client, sid, {ids[0]: "PASS if it works", ids[1]: "FAIL otherwise"})
    # (32) no ledger/contract assertion, no transcript entry, no progression
    assert [assertion_to_dict(r) for r in store.load_contract(sid).assertions] \
        == contract_before
    review_after = webapp.reconstruct_readonly_state(store, sid).review
    assert (review_after.maturity_level, review_after.current_stage,
            review_after.open_gaps) == (review_before.maturity_level,
                                        review_before.current_stage,
                                        review_before.open_gaps)
    assert (live.maturity_level, live.current_stage,
            [(g.gap_type, g.status, len(g.evidence)) for g in live.gaps],
            live.iteration, len(live.acknowledged_unknowns)) == progression_before
    assert SESSION_STORE[sid]["transcript"] == transcript_before
    # (33) no other durable row anywhere — no Evidence, result or readiness row
    con = sqlite3.connect(_db_path())
    try:
        assert {t: con.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
                for t in tables} == counts_before
    finally:
        con.close()
    # every other section, Validation Plan and readiness included, is unchanged
    package_after = assemble_deliverable(live)
    for key in package_before:
        if key.startswith("section_") and key != "section_11_prototype_test_plan":
            assert package_after[key] == package_before[key], key
    # (34) the criterion text is kept verbatim as a TARGET; no status beyond
    # captured/required is ever produced, however the user phrased it
    items = {it["experiment_id"]: it
             for it in package_after["section_11_prototype_test_plan"]["items"]}
    assert items[ids[0]]["success_criterion"] == "PASS if it works"
    assert {it["success_criterion_status"] for it in items.values()} <= {"captured", "required"}


# ==========================================================================
# 36 — the experiment-id contract and plan behaviour are unchanged
# ==========================================================================
def test_36_v1_identity_contract_and_live_reconstructed_plan_parity(client):
    source = "  I do NOT know\n  the   threshold  "
    canonical = re.sub(r"\s+", " ", source.strip()).casefold()
    digest = hashlib.sha256(("acknowledged_unknown\x1f" + canonical)
                            .encode("utf-8")).hexdigest()[:32]
    assert _experiment_id("acknowledged_unknown", source) \
        == "exp_v1_acknowledged_unknown_" + digest
    sid = _journey(client, answers=ELEC_ANSWERS + (ELEC_DISPLACING_ANSWER,))
    live_items = _plan_items(SESSION_STORE[sid]["state"])
    recon = webapp.reconstruct_readonly_state(webapp._get_store(), sid)
    recon_items = _plan_items(recon.state)
    assert len(live_items) == 3                                    # three-item cap
    assert [(i["experiment_id"], i["experiment_title"], i["source_basis"])
            for i in recon_items] == [(i["experiment_id"], i["experiment_title"],
                                       i["source_basis"]) for i in live_items]


# ==========================================================================
# Store contract — validation, project scope, foreign key
# ==========================================================================
def test_store_delta_is_validated_before_any_write_and_project_scoped(tmp_path):
    from engine.record_contract import ProjectRecordContract
    from engine.idea_state import IdeaState
    path = str(tmp_path / "unit.sqlite")
    store = SqliteRecordStore(path)
    try:
        a = store.create_project(ProjectRecordContract.from_state(IdeaState(idea_id="a")),
                                 project_id="proj-a")
        b = store.create_project(ProjectRecordContract.from_state(IdeaState(idea_id="b")),
                                 project_id="proj-b")
        good = "exp_v1_acknowledged_unknown_" + "a" * 32
        other = "exp_v1_reasoned_leading_claim_" + "b" * 32
        store.apply_success_criteria_delta(a, {good: "A1", other: "A2"})
        store.apply_success_criteria_delta(b, {good: "B1"})
        for bad in ({good: "  untrimmed "}, {good: ""}, {good: "x" * 1001},
                    {"bad id": "x"}, {good: 5}, [(good, "x")]):
            with pytest.raises(SuccessCriterionInvalid):
                store.apply_success_criteria_delta(a, bad)
        assert store.load_success_criteria(a) == ((good, "A1"), (other, "A2"))
        with pytest.raises(ProjectNotFound):
            store.apply_success_criteria_delta("missing", {good: "x"})
        with pytest.raises(ProjectNotFound):
            store.load_success_criteria("missing")
        store.apply_success_criteria_delta(a, {good: None})           # delete in A only
        assert store.load_success_criteria(a) == ((other, "A2"),)
        assert store.load_success_criteria(b) == ((good, "B1"),)
        with pytest.raises(sqlite3.IntegrityError):                   # FK enforced
            store._conn.execute("INSERT INTO prototype_plan_metadata VALUES (?, ?, ?)",
                                ("no-such-project", good, "x"))
    finally:
        store.close()


@pytest.mark.parametrize("with_criteria", [True, False])
def test_cold_report_without_a_current_plan_never_shows_saved_criteria_as_stale(
        client, monkeypatch, with_criteria):
    """A cold report whose plan cannot be rebuilt has no CURRENT plan, so saved
    criteria can be placed against nothing: the report fails closed instead of
    listing them all as stale or silently dropping them. Negative control: the
    same cold report with no saved criteria keeps its existing behaviour."""
    sid = _journey(client)
    if with_criteria:
        _post_criteria(client, sid, {_live_ids(sid)[0]: "must not read as stale"})
    _restart()

    def no_plan(store, project_id):
        raise RuntimeError("injected reconstruction unavailability")

    monkeypatch.setattr(webapp, "reconstruct_readonly_state", no_plan)
    r = csrf_client(app).get("/session/%s/deliverable" % sid)
    if with_criteria:
        assert r.status_code == 302 and r.headers["Location"].endswith("/")
    else:
        assert r.status_code == 200
        assert "no longer matches a current proposed experiment" not in \
            html.unescape(r.get_data(as_text=True))


def test_correction_refuses_before_its_append_when_saved_criteria_are_corrupt(client):
    """A correction must never COMMIT against a criteria collection that could
    not be reattached to the replayed state afterwards: with a corrupt row it
    is refused BEFORE the durable append — no new ledger record, nothing
    replaced, and the truthful not-applied message (never "saved")."""
    sid = _journey(client)
    ids = _live_ids(sid)
    _insert_raw(sid, ids[0], "  untrimmed  ")
    store = webapp._get_store()
    ledger_before = [assertion_to_dict(r) for r in store.load_contract(sid).assertions]
    live_before = SESSION_STORE[sid]["state"]
    record = _answered_record(sid, ELEC_ANSWERS[3])
    assert _correct(client, sid, record.record_id,
                    "The rain question is answered by a sealed enclosure.").status_code == 302
    assert [assertion_to_dict(r) for r in store.load_contract(sid).assertions] == ledger_before
    assert SESSION_STORE[sid]["state"] is live_before
    assert SESSION_STORE[sid].get("_answer_error") == webapp.CORRECTION_NOT_APPLIED_MESSAGE
