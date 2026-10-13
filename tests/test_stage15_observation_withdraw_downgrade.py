"""STAGE15-OBSERVATION-WITHDRAW-01 — supported downgrade evidence against the
EXACT pre-increment baseline ``6e5a20c6d4cda7dd530f3fcf7ee3fe7027cfffd0``.

The baseline tree is extracted from Git (``git archive``) and run in a separate
interpreter against the SAME database this candidate wrote, through its real
observation store reads and writes and its real interface, report and
disclosure-export routes. Proven here:

* the observation table a fresh baseline database receives is EXACTLY the
  legacy shape this candidate recognises and upgrades;
* rows the baseline wrote in the legacy shape are upgraded with every value
  kept and read back unchanged;
* on the upgraded database the baseline's observation reads and writes fail
  CLOSED for EVERY project — with or without a withdrawal — and write nothing;
  its interface page shows the observation section and the checks count as
  unavailable while the preparation path, the report and the export stay
  usable;
* reopening with this build re-validates and reads the retained data.

No reverse migration, compatibility alias, history deletion or restoration of
an older database over newer records is offered or implied.
"""
import io as _io
import json
import os
import sqlite3
import subprocess
import sys
import tarfile

import pytest

import web.app as appmod
from engine import interface_observation as io
from engine import record_store as rs
from tests.test_stage15_interface_observations import TABLE, _events
from tests.test_stage15_interface_preparation import _integrated_with_interface
from tests.test_stage15_observation_withdraw import _withdraw, _withdraw_form
from tests.test_stage19_durable_success_criteria import PW, _client_for, _db_path, _restart

BASELINE = "6e5a20c6d4cda7dd530f3fcf7ee3fe7027cfffd0"
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TREE = ("engine", "web", "domains", "docs", "schemas", "prompts", "database",
         "tests/csrf_client.py")

_PROBE = r'''
import html, json, os, sqlite3, sys
base, mode, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, base)
from engine.record_store import SqliteRecordStore
if mode == "schema":
    SqliteRecordStore(out_path).close()
    sys.exit(0)
db = os.environ["INVENTORAI_DB_PATH"]
from engine import interface_observation as io
out = {}

def outcome(fn):
    try:
        return ["ok", fn()]
    except Exception as exc:
        return ["error", type(exc).__name__]

def ser(events):
    return [[e.observation_id, e.interface_id, e.observation_text, e.supersedes_observation_id,
             e.recorded_at, None if e.context is None else
             [getattr(e.context, f) for f in io.CONTEXT_FIELDS]] for e in events]

def rows():
    con = sqlite3.connect(db)
    try:
        return con.execute("SELECT COUNT(*) FROM subsystem_interface_observations").fetchone()[0]
    finally:
        con.close()

store = SqliteRecordStore(db)
if mode == "seed":
    pid_a, iid_a, pid_b, iid_b = sys.argv[4:8]
    root = io.recorded_root(iid_a, "baseline check", io.ObservationContext())
    store.append_interface_observation(pid_a, root, "seed-a1")
    store.append_interface_observation(
        pid_a, io.recorded_correction(iid_a, "baseline check, corrected", root.observation_id),
        "seed-a2")
    store.append_interface_observation(
        pid_b, io.recorded_root(iid_b, "baseline check b", io.ObservationContext()), "seed-b1")
    out["a"] = ser(store.load_interface_observations(pid_a))
    out["b"] = ser(store.load_interface_observations(pid_b))
    store.close()
else:
    email, pid_a, iid_a, pid_b, iid_b, field, prep_text = sys.argv[4:11]
    for name, pid, iid in (("a", pid_a, iid_a), ("b", pid_b, iid_b)):
        before = rows()
        out[name] = {
            "load": outcome(lambda: ser(store.load_interface_observations(pid))),
            "committed": outcome(lambda: store.committed_interface_observation_for_submission(
                pid, "seed-a1")),
            "append": outcome(lambda: store.append_interface_observation(
                pid, io.recorded_root(iid, "baseline write", io.ObservationContext()),
                "down-" + name)[0]),
            "rows": [before, rows()],
        }
    out["prep_write"] = outcome(lambda: store.apply_interface_preparation_delta(
        pid_b, {iid_b: {field: prep_text}}) or "saved")
    out["prep_read"] = outcome(lambda: [getattr(p, field) for p in
                                        store.load_interface_preparations(pid_b)])
    store.close()
    import web.app as w
    from tests.csrf_client import csrf_client
    w.app.config["TESTING"] = True
    c = csrf_client(w.app)
    out["login"] = c.post("/login", data={"email": email, "password": sys.argv[11]}).status_code
    pages = {}
    for name, pid in (("a", pid_a), ("b", pid_b)):
        p = c.get("/session/%s/interface-preparation" % pid)
        r = c.get("/session/%s/deliverable" % pid)
        j = c.get("/account/projects/%s/disclosure-export/json" % pid)
        pages[name] = {"page": [p.status_code, html.unescape(p.get_data(as_text=True))],
                       "report": r.status_code, "export": j.status_code}
    out["pages"] = pages
    out["files"] = [w.__file__, io.__file__]
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(out, fh)
'''


def _ser(events):
    return [[e.observation_id, e.interface_id, e.observation_text, e.supersedes_observation_id,
             e.recorded_at, None if e.context is None else
             [getattr(e.context, f) for f in io.CONTEXT_FIELDS]] for e in events]


@pytest.fixture(scope="module")
def baseline(tmp_path_factory):
    """The exact baseline tree from Git. CI checks out full history
    (``fetch-depth: 0``); a checkout without the commit fails here rather than
    silently skipping the downgrade guarantee."""
    have = subprocess.run(["git", "cat-file", "-e", BASELINE + "^{commit}"], cwd=_REPO,
                          capture_output=True)
    if have.returncode != 0:
        pytest.fail("the downgrade baseline %s is not available in this checkout" % BASELINE)
    archive = subprocess.run(["git", "archive", "--format=tar", BASELINE, *_TREE], cwd=_REPO,
                             capture_output=True, check=True).stdout
    root = tmp_path_factory.mktemp("obs-baseline")
    with tarfile.open(fileobj=_io.BytesIO(archive)) as tar:
        tar.extractall(root, filter="data")
    probe = tmp_path_factory.mktemp("obs-probe") / "probe.py"
    probe.write_text(_PROBE, encoding="utf-8")
    return str(root), str(probe)


def _run(baseline, mode, out_path, *args):
    root, probe = baseline
    done = subprocess.run([sys.executable, "-I", probe, root, mode, str(out_path), *args],
                          cwd=root, env=dict(os.environ), capture_output=True, text=True,
                          timeout=600)
    assert done.returncode == 0, done.stderr[-4000:]
    if mode != "schema":
        return json.loads(open(out_path, encoding="utf-8").read())


def _shape(path):
    conn = sqlite3.connect(path)
    try:
        return rs._observation_schema_shape(conn)
    finally:
        conn.close()


def _raw_rows():
    conn = sqlite3.connect(_db_path())
    try:
        return conn.execute("SELECT * FROM %s ORDER BY project_id, 2" % TABLE).fetchall()
    finally:
        conn.close()


def test_d1_the_baseline_creates_exactly_the_recognised_legacy_shape(baseline, tmp_path):
    _run(baseline, "schema", tmp_path / "baseline.db")
    legacy, current = rs._observation_reference_shapes()
    assert _shape(str(tmp_path / "baseline.db")) == legacy != current


def test_d2_upgrade_then_baseline_fails_closed_for_every_project_and_forward_reopen(
        baseline, tmp_path):
    appmod.app.config["TESTING"] = True
    email = "obs-downgrade@example.com"
    c, _aid = _client_for(email)
    sid_a, ifc_a = _integrated_with_interface(c)
    sid_b, ifc_b = _integrated_with_interface(c)
    _restart()
    # The database as the baseline would hold it: the observation table in the
    # legacy shape (empty here; the baseline itself writes the rows below).
    conn = sqlite3.connect(_db_path())
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("DROP TABLE %s" % TABLE)
    for stmt in rs._INTERFACE_OBSERVATIONS_SCHEMA:
        conn.execute(stmt)
    conn.commit()
    conn.close()
    assert _shape(_db_path()) == rs._observation_reference_shapes()[0]
    seeded = _run(baseline, "seed", tmp_path / "seed.json",
                  sid_a, ifc_a.interface_id, sid_b, ifc_b.interface_id)
    legacy_rows = _raw_rows()
    assert len(legacy_rows) == 3 and len(legacy_rows[0]) == 11

    # forward: this build upgrades in place, keeping every value
    assert _ser(_events(sid_a)) == seeded["a"] and _ser(_events(sid_b)) == seeded["b"]
    upgraded = _raw_rows()
    assert [r[:11] for r in upgraded] == legacy_rows
    assert {r[11] for r in upgraded} == {io.EVENT_OBSERVATION}
    assert _shape(_db_path()) == rs._observation_reference_shapes()[1]
    head = _events(sid_a)[-1]
    assert _withdraw(c, sid_a, _withdraw_form(c, sid_a, head.observation_id)).status_code == 200
    before = _raw_rows()
    _restart()

    field = io.CONTEXT_FIELDS[0]
    prep_text = "Indoors, written by the older build."
    out = _run(baseline, "downgrade", tmp_path / "down.json", email, sid_a, ifc_a.interface_id,
               sid_b, ifc_b.interface_id, field, prep_text, PW)
    assert all(f.startswith(baseline[0]) for f in out["files"])        # the baseline ran
    for name in ("a", "b"):                                            # with AND without
        assert out[name]["load"] == ["error", "OperationalError"], name
        assert out[name]["committed"] == ["error", "OperationalError"], name
        assert out[name]["append"] == ["error", "OperationalError"], name
        assert out[name]["rows"][0] == out[name]["rows"][1] == len(before), name
    assert out["prep_write"] == ["ok", "saved"]                        # preparation usable
    assert out["prep_read"] == ["ok", [prep_text]]
    assert out["login"] == 302
    unavailable = ("Your recorded observations could not be read, so they cannot be shown "
                   "or added to from this page.")
    for name in ("a", "b"):
        code, page = out["pages"][name]["page"]
        assert code == 200 and unavailable in page, name
        assert "baseline check" not in page and io.WITHDRAWAL_MARKER not in page
        assert out["pages"][name]["report"] == 200
        assert out["pages"][name]["export"] == 200

    # reopening with this build re-validates and reads the retained data
    after = _raw_rows()
    assert after == before                                             # the baseline wrote none
    assert _shape(_db_path()) == rs._observation_reference_shapes()[1]
    events = _events(sid_a)
    assert len(events) == 3 and io.is_withdrawal(events[-1])
    assert io.current_observation_chains(events) == []
    assert len(io.current_observation_chains(_events(sid_b))) == 1
    preparations = appmod._get_store().load_interface_preparations(sid_b)
    assert [getattr(p, field) for p in preparations] == [prep_text]
