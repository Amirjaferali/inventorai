"""P4-1b-1 — Runtime Store Construction and Durable Project Create/Load (RED/GREEN).

Behaviour-based tests for wiring the merged P4-1a durable store
(`engine.record_store.SqliteRecordStore`) into the Flask runtime so that a NEW
project is durably created at `/start`, survives a real process/store restart,
and is cold-loaded back through the session route. Governed by the merged
P4-1b-1 Increment Contract (`docs/governance/ACTIVE_INCREMENT_CONTRACT.md`,
G-P4-1B-1-DOC-01 / PR #358).

Correct model (BF-1 correction): `sid` and the durable `project_id` are the
SAME `uuid4` value — one pre-account lookup capability. Durable creation is
`create_project(contract, project_id=sid)`; cold-load is `load_contract(sid)`.
No `sid`->`project_id` mapping table, no `project_ids()` scan, no reversible
mapping layer.

Durability is proved through ACTUAL on-disk SQLite and a real
restart: only the route `sid` string is carried across; the live
`SESSION_STORE`, the app-scoped store handle, and the original `IdeaState` are
discarded; a fresh store is opened against the SAME database file; the route is
driven through Flask `test_client`. No module dicts, reused connections, mocks,
`:memory:` databases, or file-existence-only assertions. SQLite files live only
in pytest `tmp_path`. Scope: durable NEW-project create/load only — no
accepted-input append, no Keep/Refine durability, no transcript/last_result
persistence, no replay (all P4-1b-2 or later).
"""
import os

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from engine.record_store import SqliteRecordStore, ProjectNotFound
from engine.record_contract import ProjectRecordContract, UnknownVersionError
from engine.derived_readiness import derive_readiness

# A genuine electronics/electrical idea that passes the /start domain gate:
# lay electrical mechanism words (electronic, circuit, sensor, switch, power,
# current) and no strong unsupported-domain evidence.
IDEA_A = ("An electronic circuit uses a sensor and a switch to cut the power "
          "when the current gets too high.")
IDEA_B = ("A small battery charger uses a sensor and a relay to switch off the "
          "circuit when the voltage is full.")
FORM = {"domain_confirm": "electronics_electrical"}


@pytest.fixture
def db_path():
    """The isolated, pytest-managed on-disk SQLite path for this test. The
    autouse `isolated_inventorai_db` fixture in tests/conftest.py already set
    `INVENTORAI_DB_PATH` to a unique tmp file and reset the app-scoped store and
    SESSION_STORE (B2 / G-P4-1B-1-AMEND-01); read that single source of truth
    here so there is exactly one governed DB path per test."""
    return os.environ["INVENTORAI_DB_PATH"]


def _reset_runtime():
    """Discard live sessions and the app-scoped store handle. Safe before the
    implementation exists (setting `_STORE` merely creates a module attribute
    the unmodified app ignores)."""
    SESSION_STORE.clear()
    setattr(webapp, "_STORE", None)


def _start(idea=IDEA_A):
    return app.test_client().post("/start", data={"idea": idea, **FORM},
                                  follow_redirects=False)


def _sid_of(resp):
    loc = resp.headers.get("Location", "")
    assert "/session/" in loc, f"expected a /session/<sid> redirect, got {loc!r}"
    return loc.rstrip("/").rsplit("/session/", 1)[1].split("?")[0]


# --- RED-1: /start durably creates a project envelope (project_id == sid) -----
def test_red1_start_durably_creates_project(db_path):
    sid = _sid_of(_start(IDEA_A))
    # Inspect through a NEWLY opened store on the same file (not the app's handle).
    store = SqliteRecordStore(db_path)
    loaded = store.load_contract(sid)           # RED: raises ProjectNotFound today
    assert loaded.contract_version == "p4-0-record-contract-v1"
    assert isinstance(loaded.idea_id, str) and loaded.idea_id
    store.close()


# --- RED-2 / RED-3: real restart survival + cold route load -------------------
def test_red2_project_survives_real_restart_and_cold_loads(db_path):
    sid = _sid_of(_start(IDEA_A))
    # Simulate a process restart: carry ONLY the sid string across.
    _reset_runtime()                             # discard SESSION_STORE + store handle
    assert sid not in SESSION_STORE
    resp = app.test_client().get(f"/session/{sid}", follow_redirects=False)
    # RED: today a missing SESSION_STORE entry redirects (302) with no durable load.
    assert resp.status_code == 200, (
        "cold request with only the sid must reconstruct the durable project")
    assert sid in SESSION_STORE, "cold-load must rebuild the minimum runtime entry"


# --- RED-4: durable-creation failure leaves no live session (fail closed) ------
def test_red4_durable_creation_failure_no_live_session(tmp_path, monkeypatch):
    # Make the DB path unusable: parent is a FILE, so the store cannot be built.
    blocker = tmp_path / "blocker"
    blocker.write_text("x")
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(blocker / "db.sqlite"))
    _reset_runtime()
    resp = _start(IDEA_A)
    # RED: today /start ignores the store and always advertises a live session.
    assert resp.status_code != 302 or "/session/" not in resp.headers.get("Location", ""), (
        "a failed durable creation must not advertise a live session")
    assert not any(k for k in SESSION_STORE), "no SESSION_STORE entry may remain"
    _reset_runtime()


# --- RED-5: unknown capability is generic and non-disclosing -------------------
def test_red5_unknown_capability_generic(db_path):
    resp = app.test_client().get("/session/00000000-0000-4000-8000-000000000000",
                                 follow_redirects=False)
    # Generic redirect to index; discloses nothing about existence.
    assert resp.status_code == 302
    assert "/session/" not in resp.headers.get("Location", "")


# --- RED-6: malformed / unsupported stored contract fails closed --------------
def test_red6_malformed_stored_contract_fails_closed(db_path):
    sid = _sid_of(_start(IDEA_A))
    _reset_runtime()
    # Corrupt the persisted contract_version directly in the SQLite file.
    import sqlite3
    conn = sqlite3.connect(db_path)
    with conn:
        conn.execute("UPDATE projects SET contract_version = ? WHERE project_id = ?",
                     ("p4-0-record-contract-v999", sid))
    conn.close()
    resp = app.test_client().get(f"/session/{sid}", follow_redirects=False)
    # Must fail closed to the generic behaviour (redirect), never 500/traceback.
    assert resp.status_code == 302
    assert "/session/" not in resp.headers.get("Location", "")


# --- RED-7: database unavailable → generic behaviour, no leak ------------------
def test_red7_database_unavailable_generic(db_path, tmp_path, monkeypatch):
    sid = _sid_of(_start(IDEA_A))
    _reset_runtime()
    # Repoint at an unusable DB path (parent is a file) for the cold request.
    blocker = tmp_path / "blk"
    blocker.write_text("x")
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(blocker / "db.sqlite"))
    setattr(webapp, "_STORE", None)
    resp = app.test_client().get(f"/session/{sid}", follow_redirects=False)
    assert resp.status_code == 302
    assert "/session/" not in resp.headers.get("Location", "")


# --- RED-8: cross-project capability isolation --------------------------------
def test_red8_cross_project_isolation(db_path):
    sid_a = _sid_of(_start(IDEA_A))
    sid_b = _sid_of(_start(IDEA_B))
    assert sid_a != sid_b
    store = SqliteRecordStore(db_path)
    a = store.load_contract(sid_a)               # RED: not persisted today
    b = store.load_contract(sid_b)
    assert a.idea_id != b.idea_id
    with pytest.raises(ProjectNotFound):
        store.load_contract("11111111-1111-4111-8111-111111111111")
    store.close()


# --- RED-9: readiness is freshly derived after cold load ----------------------
def test_red9_readiness_derived_after_cold_load(db_path):
    sid = _sid_of(_start(IDEA_A))
    _reset_runtime()
    resp = app.test_client().get(f"/session/{sid}", follow_redirects=False)
    assert resp.status_code == 200
    entry = SESSION_STORE.get(sid)
    assert entry is not None
    state = entry["state"]
    # Readiness is recomputed from the reconstructed ledger, never restored.
    r = derive_readiness(state)
    # A freshly created project has an empty accepted-input ledger -> not verified.
    assert r.overall_verified() is False
    assert list(state.assertions) == []


# --- RED-10: transcript / last_result are not restored as authoritative --------
def test_red10_no_transcript_or_last_result_restored(db_path):
    sid = _sid_of(_start(IDEA_A))
    _reset_runtime()
    resp = app.test_client().get(f"/session/{sid}", follow_redirects=False)
    assert resp.status_code == 200
    entry = SESSION_STORE.get(sid)
    assert entry.get("transcript") == []          # not reconstructed
    assert entry.get("last_result") is None       # cached result not authoritative


# --- RED-11: no repository-tracked database artifact --------------------------
def test_red11_no_repo_tracked_db(db_path):
    _sid_of(_start(IDEA_A))
    # The configured DB lives under pytest tmp_path, never in the repo tree.
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(webapp.__file__)))
    assert os.path.commonpath([os.path.abspath(db_path), repo_root]) != repo_root, (
        "the SQLite database must not live inside the repository tree")
    assert not os.path.exists(os.path.join(repo_root, "inventorai.sqlite"))


# ===========================================================================
# P4-1b-1 correction (G-P4-1B-1-AMEND-01) — B1 threading + B2 pytest DB isolation
# ===========================================================================
import runpy
import sqlite3
import tempfile
import threading
from unittest import mock

_SHARED_DEV_DB = os.path.join(tempfile.gettempdir(), "inventorai_dev",
                              "inventorai_p4_1b1.sqlite")


def _captured_run_kwargs():
    """Execute the module run-entry with Flask.run patched to capture kwargs —
    a bounded, behaviour-oriented seam onto the ACTUAL run configuration (no
    server is started)."""
    captured = {}
    with mock.patch("flask.Flask.run",
                    lambda self, *a, **k: captured.update(k)):
        runpy.run_module("web.app", run_name="__main__")
    return captured


def _shared_dev_db_project_count():
    if not os.path.exists(_SHARED_DEV_DB):
        return 0
    conn = sqlite3.connect(_SHARED_DEV_DB)
    try:
        return conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0]
    except sqlite3.Error:
        return 0
    finally:
        conn.close()


# --- RED-B1: run entry explicitly selects threaded=False --------------------
def test_redb1_run_entry_selects_threaded_false():
    kw = _captured_run_kwargs()
    # RED: the superseded candidate relied on Flask's default (threaded absent).
    assert kw.get("threaded") is False, (
        "the run entry must explicitly configure threaded=False (B1)")


# --- RED-B1B: reviewer scenario — shared connection is thread-bound ----------
def test_redb1b_shared_connection_thread_bound_and_serving_serial(db_path):
    # Build the ONE app-scoped store in this thread via a real /start.
    sid = _sid_of(_start(IDEA_A))
    store = webapp._get_store()
    errors = []

    def _use_off_thread():
        try:
            store.load_contract(sid)   # shared sqlite3 conn used off its thread
        except Exception as exc:       # noqa: BLE001 - capturing the class name
            errors.append(type(exc).__name__)

    t = threading.Thread(target=_use_off_thread)
    t.start()
    t.join()
    # The single shared connection is thread-bound: cross-thread use raises. This
    # is WHY the MVP must serve serially — proven WITHOUT check_same_thread
    # changes, WITHOUT mocking sqlite, and WITHOUT relying on same-thread
    # test_client as the proof.
    assert errors, (
        "the app-scoped SQLite connection must be thread-bound, demonstrating "
        "why threaded serving through it is unsafe")
    # The selected serving boundary is serial (matches the single connection).
    assert _captured_run_kwargs().get("threaded") is False


# --- RED-B2: governed pytest uses an isolated DB path, not the shared dev DB -
def test_redb2_governed_db_path_is_pytest_isolated():
    path = webapp._resolve_db_path()
    assert "inventorai_dev" not in path, (
        "governed pytest must not use the shared local-development database (B2)")
    assert ("pytest" in path or "tmp" in path.lower()), (
        "governed pytest must use a pytest-managed temporary database path")


# --- RED-B2C: a governed /start writes nothing to the shared dev DB ----------
def test_redb2c_no_shared_dev_db_write_during_pytest():
    before = _shared_dev_db_project_count()
    _sid_of(_start(IDEA_A))
    after = _shared_dev_db_project_count()
    assert after == before, (
        "a governed /start must not write to the shared local-development "
        "database (B2)")


# --- RED-B2B: store/SESSION_STORE reset between tests (order-independent) ----
def test_redb2b_a_dirty_state_no_local_cleanup():
    # Deliberately does NOT use the db_path fixture (which would self-clean at
    # teardown): it leaves the app-scoped store and SESSION_STORE dirty so the
    # NEXT test can prove the global isolation fixture cleans up between tests.
    _sid_of(_start(IDEA_A))
    assert len(SESSION_STORE) >= 1
    assert webapp._STORE is not None


def test_redb2b_b_isolated_clean_start():
    # The isolation fixture must reset the app-scoped store and SESSION_STORE
    # before this test, regardless of the preceding test — no order dependency.
    assert len(SESSION_STORE) == 0, "SESSION_STORE must be clean between tests"
    assert getattr(webapp, "_STORE", "missing") is None, (
        "the app-scoped store must be reset between tests")
