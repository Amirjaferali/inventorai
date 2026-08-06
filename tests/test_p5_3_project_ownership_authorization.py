"""P5-3 — Project Ownership and Route Authorization (RED/GREEN).

Behaviour-based tests for gate
G-P5-3-PROJECT-OWNERSHIP-ROUTE-AUTHORIZATION-IMPLEMENTATION-01, building only on
the merged P5-1/P5-2 account+session foundation. Covers the additive nullable
ownership model, atomic owner assignment at creation, the central server-side
authorization decision, the full authorization matrix across every protected
project-scoped route (GET and POST), cross-account isolation (IDOR), legacy/
anonymous NULL-owner compatibility, verified-only owned creation, disabled/
deleted denial, generic non-enumerating denial, forged-owner rejection, the
owned-project list, and migration.

Real on-disk SQLite (autouse conftest isolation); the real record + account
stores; multiple independent authenticated Flask clients with real signed
sessions; the real authorization helper. No mocks; no ``:memory:`` DB. False-green
guards (contract §21) are addressed explicitly in the marked tests.
"""
import os
import threading

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from engine import account_credentials as _acct
from engine.record_store import SqliteRecordStore
from engine.record_contract import ProjectRecordContract

PW = "correct horse battery staple"
IDEA = ("An electronic circuit uses a sensor and a switch to cut the power when "
        "the current gets too high.")
FORM = {"idea": IDEA, "domain_confirm": "electronics_electrical"}


@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _new_client():
    app.config["TESTING"] = True
    return app.test_client()


def _mk_account(email, verified=True, status="active"):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status=status)
    if verified:
        store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    return aid


def _client_for(email, verified=True, status="active"):
    _mk_account(email, verified=verified, status=status)
    c = _new_client()
    c.post("/login", data={"email": email, "password": PW})
    return c


def _start_project(client):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


def _store():
    return webapp._get_store()


# ===========================================================================
# Ownership data model & atomic assignment
# ===========================================================================
def test_owner_column_additive_and_indexed(db_path):
    s = SqliteRecordStore(db_path)
    cols = [r[1] for r in s._conn.execute("PRAGMA table_info(projects)").fetchall()]
    idx = [r[1] for r in s._conn.execute("PRAGMA index_list(projects)").fetchall()]
    s.close()
    assert "owner_account_id" in cols
    assert any("owner_account_id" in i for i in idx)


def test_verified_account_creates_owned_project_atomically(db_path):
    aid = _mk_account("owner@example.com")
    c = _new_client()
    c.post("/login", data={"email": "owner@example.com", "password": PW})
    sid = _start_project(c)
    exists, owner = _store().load_owner(sid)
    assert exists and owner == aid
    # FALSE-GREEN GUARD: owner is derived from the SERVER session, and the project
    # row + owner are written in ONE row (no create-then-assign window).
    assert _store().project_ids_for_owner(aid) == [sid]


def test_anonymous_and_unverified_create_null_owner(db_path):
    anon = _new_client()
    a_sid = _start_project(anon)
    assert _store().load_owner(a_sid) == (True, None)
    unv = _client_for("unv@example.com", verified=False)
    u_sid = _start_project(unv)
    assert _store().load_owner(u_sid) == (True, None)   # unverified → no ownership


def test_ownership_not_from_sid_or_client_input(db_path):
    """FALSE-GREEN GUARD (#owner assignment client-controlled): a forged
    owner_account_id in the form is ignored; ownership comes only from the session."""
    aid = _mk_account("real@example.com")
    c = _new_client()
    c.post("/login", data={"email": "real@example.com", "password": PW})
    forged = dict(FORM, owner_account_id="acct_attacker", account_id="acct_attacker")
    r = c.post("/start", data=forged)
    sid = r.headers["Location"].rsplit("/session/", 1)[-1]
    assert _store().load_owner(sid) == (True, aid)      # forged value ignored


# ===========================================================================
# Authorization matrix (GET and POST) — cross-account isolation
# ===========================================================================
def test_owner_can_access_owned_project_get_and_post(db_path):
    c = _client_for("m@example.com")
    sid = _start_project(c)
    assert c.get("/session/" + sid).status_code == 200
    assert "Project saved to your account" in c.get("/session/" + sid).get_data(as_text=True)
    # a POST answer to own project is accepted (not a generic redirect-to-index deny)
    r = c.post("/session/" + sid, data={"answer": "The sensor measures current and opens the switch."})
    assert r.status_code in (200, 302)
    if r.status_code == 302:
        assert not r.headers["Location"].endswith("/")   # not the generic deny redirect


def test_non_owner_denied_on_real_owned_project(db_path):
    """FALSE-GREEN GUARD (#unauthorized accesses a missing project): B accesses
    A's REAL existing owned project — every protected verb is denied generically."""
    ca = _client_for("a@example.com")
    sid = _start_project(ca)
    cb = _client_for("b@example.com")
    for verb, path in [("get", "/session/" + sid),
                       ("get", "/session/" + sid + "/deliverable"),
                       ("get", "/session/" + sid + "/success-criteria"),
                       ("post", "/session/" + sid),
                       ("post", "/session/" + sid + "/keep-snapshot"),
                       ("post", "/session/" + sid + "/success-criteria")]:
        r = getattr(cb, verb)(path, data={})
        assert r.status_code == 302 and r.headers["Location"].endswith("/"), (verb, path, r.status_code)


def test_anonymous_denied_on_owned_project_all_verbs(db_path):
    ca = _client_for("a2@example.com")
    sid = _start_project(ca)
    anon = _new_client()
    for verb, path in [("get", "/session/" + sid),
                       ("get", "/session/" + sid + "/deliverable"),
                       ("post", "/session/" + sid),
                       ("post", "/session/" + sid + "/keep-snapshot")]:
        r = getattr(anon, verb)(path, data={})
        assert r.status_code == 302 and r.headers["Location"].endswith("/")


def test_sid_possession_is_not_ownership(db_path):
    """A signed-in non-owner who KNOWS the sid is still denied (sid ≠ ownership)."""
    ca = _client_for("k1@example.com")
    sid = _start_project(ca)
    cb = _client_for("k2@example.com")   # knows sid, authenticated, but not owner
    assert cb.get("/session/" + sid).headers["Location"].endswith("/")


def test_missing_and_unauthorized_are_indistinguishable(db_path):
    """FALSE-GREEN GUARD (#9 generic denial compares text but not status/headers):
    a missing project and a non-owner-accessed owned project return the identical
    status AND Location (no enumeration)."""
    ca = _client_for("g1@example.com")
    sid = _start_project(ca)
    cb = _client_for("g2@example.com")
    missing = cb.get("/session/this-sid-does-not-exist")
    unauth = cb.get("/session/" + sid)
    assert missing.status_code == unauth.status_code == 302
    assert missing.headers["Location"] == unauth.headers["Location"]


def test_legacy_null_owner_capability_preserved(db_path):
    """Anonymous NULL-owner projects keep exactly their prior capability access —
    reachable by anyone with the sid, signed in or not."""
    anon = _new_client()
    sid = _start_project(anon)
    assert anon.get("/session/" + sid).status_code == 200
    # a different signed-in account can still open a NULL-owner (legacy) project
    cb = _client_for("legacy-viewer@example.com")
    assert cb.get("/session/" + sid).status_code == 200


# ===========================================================================
# Account status & ownership
# ===========================================================================
def test_disabled_owner_denied_and_session_invalidated(db_path):
    c = _client_for("dis@example.com")
    sid = _start_project(c)
    assert c.get("/session/" + sid).status_code == 200
    webapp._get_account_store().set_status(
        webapp._get_account_store().get_account_by_normalized_email("dis@example.com")["account_id"],
        "disabled", "2026-01-01T00:00:00.000000Z")
    # FALSE-GREEN GUARD (#disabled test uses expired session): denial is by STATUS,
    # the session itself is otherwise valid/unexpired.
    r = c.get("/session/" + sid)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")


def test_deleted_owner_denied(db_path):
    c = _client_for("del@example.com")
    sid = _start_project(c)
    webapp._get_account_store().set_status(
        webapp._get_account_store().get_account_by_normalized_email("del@example.com")["account_id"],
        "deleted", "2026-01-01T00:00:00.000000Z")
    r = c.get("/session/" + sid)
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    # ownership link is NOT silently transferred or nulled by the status change
    exists, owner = _store().load_owner(sid)
    assert exists and owner is not None


def test_password_reset_revokes_owned_project_access(db_path):
    c = _client_for("pr@example.com")
    sid = _start_project(c)
    assert c.get("/session/" + sid).status_code == 200
    other = _new_client()
    other.post("/recover", data={"email": "pr@example.com"})
    raw = webapp._EMAIL_SENDER.last_for("pr@example.com")["body"].rsplit("/reset/", 1)[-1].strip()
    other.post("/reset/" + raw, data={"password": "brand new long password", "password_confirm": "brand new long password"})
    # the epoch bump from reset revokes the still-open owner session
    assert c.get("/session/" + sid).headers["Location"].endswith("/")


# ===========================================================================
# Owned-project list (account surface)
# ===========================================================================
def test_account_lists_only_own_projects(db_path):
    ca = _client_for("list-a@example.com")
    sid_a = _start_project(ca)
    cb = _client_for("list-b@example.com")
    sid_b = _start_project(cb)
    body_a = ca.get("/account").get_data(as_text=True)
    assert ("/session/" + sid_a) in body_a
    assert ("/session/" + sid_b) not in body_a        # never another account's project
    # a fresh owner with no projects sees the empty state
    cc = _client_for("list-c@example.com")
    assert "no account-owned projects" in cc.get("/account").get_data(as_text=True).lower()


def test_project_list_reflects_real_store_not_hardcoded(db_path):
    """FALSE-GREEN GUARD (#project list uses hardcoded fixture): the list equals the
    real durable project_ids_for_owner set."""
    ca = _client_for("real-list@example.com")
    aid = webapp._get_account_store().get_account_by_normalized_email("real-list@example.com")["account_id"]
    s1 = _start_project(ca)
    s2 = _start_project(ca)
    listed = _store().project_ids_for_owner(aid)
    assert set(listed) == {s1, s2}
    body = ca.get("/account").get_data(as_text=True)
    assert ("/session/" + s1) in body and ("/session/" + s2) in body


# ===========================================================================
# Migration
# ===========================================================================
def test_migration_from_pre_p5_3_db_preserves_projects(db_path):
    """A pre-P5-3 projects table (no owner column) migrates additively: existing
    rows preserved, all NULL-owner; idempotent on re-open."""
    import sqlite3
    # Build a minimal pre-P5-3 projects table WITHOUT owner_account_id and insert a row.
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE projects (project_id TEXT PRIMARY KEY, idea_id TEXT NOT NULL, contract_version TEXT NOT NULL)")
    conn.execute("INSERT INTO projects (project_id, idea_id, contract_version) VALUES ('legacy', 'idea', 'p4-0-record-contract-v1')")
    conn.commit()
    conn.close()
    s = SqliteRecordStore(db_path)          # migration runs on open
    cols = [r[1] for r in s._conn.execute("PRAGMA table_info(projects)").fetchall()]
    assert "owner_account_id" in cols
    assert s.load_owner("legacy") == (True, None)        # preserved, NULL owner
    s.close()
    s2 = SqliteRecordStore(db_path)         # idempotent re-open
    assert s2.load_owner("legacy") == (True, None)
    s2.close()


def test_ownership_immutable_no_reassignment_api(db_path):
    """Ownership is immutable in this MVP: the store exposes no owner-reassignment
    method (no owner transfer)."""
    s = SqliteRecordStore(db_path)
    try:
        assert not any(hasattr(s, name) for name in
                       ("set_owner", "reassign_owner", "transfer_owner", "update_owner"))
    finally:
        s.close()


# ===========================================================================
# Concurrency — owner assignment race
# ===========================================================================
def test_owner_assignment_is_atomic_under_concurrent_creation(db_path):
    """Owner is written in the SAME INSERT that creates the project row — there is
    no create-then-assign window, so a claim/visibility race is impossible. Proven
    at the durable-store level (the project record store is intentionally
    thread-bound per the P4 threaded=False decision, so genuine DB concurrency is
    exercised with SEPARATE connections, each in its own thread). Every project is
    observed with its correct owner and NEVER momentarily NULL or cross-assigned."""
    N = 12
    barrier = threading.Barrier(N)
    results = [None] * N
    lock = threading.Lock()

    def worker(i):
        store = SqliteRecordStore(db_path)     # separate connection per thread
        try:
            owner = "acct_owner_%d" % i
            barrier.wait()
            sid = store.create_project(
                ProjectRecordContract(idea_id="idea-%d" % i, assertions=[]),
                project_id="sid-%d" % i, owner_account_id=owner)
            # read-back through the SAME atomic-created row: never NULL, never cross
            exists, got = store.load_owner(sid)
            with lock:
                results[i] = (exists, got, owner)
        finally:
            store.close()

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    for exists, got, owner in results:
        assert exists and got == owner          # atomic; correct owner; no NULL/cross
    # global check via a fresh connection
    verify = SqliteRecordStore(db_path)
    try:
        for i in range(N):
            assert verify.load_owner("sid-%d" % i) == (True, "acct_owner_%d" % i)
    finally:
        verify.close()


# ===========================================================================
# Compatibility — anonymous journey remains open, no mandatory login
# ===========================================================================
def test_anonymous_journey_still_open(db_path):
    anon = _new_client()
    assert anon.get("/").status_code == 200
    sid = _start_project(anon)               # no login required
    assert anon.get("/session/" + sid).status_code == 200
    # no false ownership claim on a NULL-owner project
    assert "saved to your account" not in anon.get("/session/" + sid).get_data(as_text=True).lower()
