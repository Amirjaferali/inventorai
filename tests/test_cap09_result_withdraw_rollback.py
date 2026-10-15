"""CAP-09 RESULT WITHDRAW-01 — supported rollback evidence against the EXACT
pre-increment baseline ``dedf051e75dc096a0e1d7630e5eee793ca635636``.

The baseline tree is extracted from Git (``git archive``) and run in a separate
interpreter against the SAME database this candidate wrote. It is driven
through its real Result store reads and writes and its real planning page,
report and disclosure-export routes. Proven here:

* the record-store schema a fresh baseline database receives is identical to the
  candidate's (no table, column, index, trigger or foreign-key change);
* on a project holding a withdrawal the baseline fails CLOSED everywhere it reads
  Result history — the store read and the committed-submission read refuse, a
  write is refused and adds no row, the planning page shows its Result block as
  unavailable, the report states the experiments' execution state is unavailable
  (never "no result" or zero) and the export is refused;
* an ordinary legacy history stays readable unchanged by the baseline, and rows
  the baseline writes are read back unchanged by the candidate.

No transparent downgrade is promised, no claim is made about any other historical
build, and nothing here deletes or reverses a withdrawal row.
"""
import html
import io
import json
import os
import sqlite3
import subprocess
import sys
import tarfile

import pytest

import web.app as webapp
from web.app import app
from engine import experiment_result as er
from engine.record_store import SqliteRecordStore
from tests.test_stage19_durable_success_criteria import (
    PW, _journey, _restart, _live_ids, _client_for)
from tests.test_cap09_result_events import OBS, OBS2, _record_form, _correct_form, _post
from tests.test_cap09_result_withdraw import _withdraw, _withdraw_form

BASELINE = "dedf051e75dc096a0e1d7630e5eee793ca635636"
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TREE = ("engine", "web", "domains", "docs", "schemas", "prompts", "database",
         "tests/csrf_client.py")

# The baseline driver: run with ``-I`` from the extracted baseline root, so only
# baseline modules are importable. It never edits the database except through
# the baseline store's own append path.
_PROBE = r'''
import html, json, os, sqlite3, sys
base, mode, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, base)
from engine.record_store import SqliteRecordStore
if mode == "schema":
    SqliteRecordStore(out_path).close()
    sys.exit(0)
email, pw, sid_w, eid_w, sid_o, sid_l, eid_l = sys.argv[4:11]
db = os.environ["INVENTORAI_DB_PATH"]
from engine import experiment_result as er
out = {}

def outcome(fn):
    try:
        return ["ok", fn()]
    except Exception as exc:
        return ["error", type(exc).__name__]

def rows(sid):
    con = sqlite3.connect(db)
    try:
        return con.execute("SELECT COUNT(*) FROM prototype_test_results WHERE project_id = ?",
                           (sid,)).fetchone()[0]
    finally:
        con.close()

def ser(events):
    return [[e.result_event_id, e.experiment_id, e.result_text, e.supersedes_result_event_id,
             e.recorded_at, None if e.context is None else
             [getattr(e.context, f) for f in er.CONTEXT_FIELDS]] for e in events]

store = SqliteRecordStore(db)
out["w_load"] = outcome(lambda: ser(store.load_result_events(sid_w)))
out["w_committed"] = outcome(lambda: store.committed_result_event_for_submission(sid_w, "x" * 40))
before = rows(sid_w)
out["w_append"] = outcome(lambda: store.append_result_event(
    sid_w, er.recorded_root(eid_w, "baseline write", er.ResultContext("t")), "b" * 40)[0])
out["w_rows"] = [before, rows(sid_w)]
out["o_load"] = outcome(lambda: ser(store.load_result_events(sid_o)))
root = er.recorded_root(eid_l, "legacy root", er.ResultContext("Legacy title"))
store.append_result_event(sid_l, root, "l" * 40)
store.append_result_event(sid_l, er.recorded_correction(eid_l, "legacy fix", root.result_event_id),
                          "m" * 40)
out["l_load"] = ser(store.load_result_events(sid_l))
store.close()

import web.app as w
from tests.csrf_client import csrf_client
w.app.config["TESTING"] = True
c = csrf_client(w.app)
out["login"] = c.post("/login", data={"email": email, "password": pw}).status_code
pages = {}
for name, sid in (("w", sid_w), ("o", sid_o)):
    p = c.get("/session/%s/success-criteria" % sid)
    r = c.get("/session/%s/deliverable" % sid)
    j = c.get("/account/projects/%s/disclosure-export/json" % sid)
    pages[name] = {"planning": [p.status_code, html.unescape(p.get_data(as_text=True))],
                   "report": [r.status_code, html.unescape(r.get_data(as_text=True))],
                   "export": [j.status_code, j.data.decode("utf-8")]}
out["pages"] = pages
out["files"] = [w.__file__, er.__file__]
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(out, fh)
'''


def _ser(events):
    return [[e.result_event_id, e.experiment_id, e.result_text, e.supersedes_result_event_id,
             e.recorded_at, None if e.context is None else
             [getattr(e.context, f) for f in er.CONTEXT_FIELDS]] for e in events]


@pytest.fixture(scope="module")
def baseline(tmp_path_factory):
    """The exact baseline tree, extracted from Git. CI checks out full history
    (``fetch-depth: 0``); a checkout without the baseline commit fails here
    rather than silently skipping the rollback guarantee."""
    have = subprocess.run(["git", "cat-file", "-e", BASELINE + "^{commit}"], cwd=_REPO,
                          capture_output=True)
    if have.returncode != 0:
        pytest.fail("the rollback baseline %s is not available in this checkout" % BASELINE)
    archive = subprocess.run(["git", "archive", "--format=tar", BASELINE, *_TREE], cwd=_REPO,
                             capture_output=True, check=True).stdout
    root = tmp_path_factory.mktemp("baseline")
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(root, filter="data")
    probe = tmp_path_factory.mktemp("probe") / "probe.py"
    probe.write_text(_PROBE, encoding="utf-8")
    return str(root), str(probe)


def _run(baseline, mode, out_path, *args):
    root, probe = baseline
    env = dict(os.environ)
    done = subprocess.run([sys.executable, "-I", probe, root, mode, str(out_path), *args],
                          cwd=root, env=env, capture_output=True, text=True, timeout=600)
    assert done.returncode == 0, done.stderr[-4000:]


# AMENDED at STAGE15-OBSERVATION-WITHDRAW-01: that later increment changes the
# observation table on purpose (its own downgrade test pins the change), so the
# CAP-09 "no schema change" proof compares every OTHER schema object.
# AMENDED at COMPONENT-PROTOTYPE-NEED-NOTE-01: that later increment adds ONE
# additive current-value table on purpose (its own tests pin it); it is not a
# CAP-09 schema change.
# AMENDED at COMPONENT-INTERFACE-PARTICIPATION-01: one more additive current-value table on
# purpose (its own tests pin it); it is not a CAP-09 schema change.
_LATER_CHANGED_TABLES = ("subsystem_interface_observations", "component_prototype_needs",
                         "subsystem_interface_components")


def _schema(path):
    con = sqlite3.connect(path)
    try:
        master = [row for row in con.execute(
            "SELECT type, name, tbl_name, sql FROM sqlite_master ORDER BY type, name")
            if row[2] not in _LATER_CHANGED_TABLES]
        fks = {t: con.execute("PRAGMA foreign_key_list(%s)" % t).fetchall()
               for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
               if t not in _LATER_CHANGED_TABLES}
    finally:
        con.close()
    return master, fks


def test_rb1_the_record_store_schema_is_identical_to_the_baseline(baseline, tmp_path):
    _run(baseline, "schema", tmp_path / "baseline.db")
    SqliteRecordStore(str(tmp_path / "candidate.db")).close()
    base_master, base_fks = _schema(str(tmp_path / "baseline.db"))
    cand_master, cand_fks = _schema(str(tmp_path / "candidate.db"))
    assert [r for r in base_master if r[2] == "prototype_test_results"]   # the table exists
    assert cand_master == base_master
    assert cand_fks == base_fks


def test_rb2_the_baseline_fails_closed_on_withdrawals_and_keeps_legacy_history(baseline, tmp_path):
    app.config["TESTING"] = True
    email = "withdraw-rollback@example.com"
    c, _aid = _client_for(email)
    sid_w = _journey(c)
    ids = _live_ids(sid_w)
    _post(c, sid_w, _record_form(c, sid_w, ids[0]), OBS)
    _post(c, sid_w, _record_form(c, sid_w, ids[0]), OBS2)
    first = webapp._get_store().load_result_events(sid_w)[0]
    assert _withdraw(c, sid_w, _withdraw_form(c, sid_w, first.result_event_id)).status_code == 200
    sid_o = _journey(c)
    o_ids = _live_ids(sid_o)
    _post(c, sid_o, _record_form(c, sid_o, o_ids[0]), OBS)
    root = webapp._get_store().load_result_events(sid_o)[0]
    _post(c, sid_o, _correct_form(c, sid_o, root.result_event_id), OBS2)
    sid_l = _journey(c)
    eid_l = _live_ids(sid_l)[0]
    before_w = webapp._get_store().load_result_events(sid_w)
    before_o = webapp._get_store().load_result_events(sid_o)
    _restart()

    out_path = tmp_path / "probe.json"
    _run(baseline, "drive", out_path, email, PW, sid_w, ids[1], sid_o, sid_l, eid_l)
    out = json.loads(out_path.read_text(encoding="utf-8"))
    root_dir = baseline[0]
    assert all(f.startswith(root_dir) for f in out["files"])          # the baseline ran

    # fail CLOSED on the withdrawal-containing project
    assert out["w_load"] == ["error", "ResultEventsCorrupt"]
    assert out["w_committed"] == ["error", "ResultEventsCorrupt"]
    assert out["w_append"] == ["error", "ResultEventsCorrupt"]
    assert out["w_rows"][0] == out["w_rows"][1] == len(before_w) == 3
    assert out["login"] == 302
    planning = out["pages"]["w"]["planning"]
    assert planning[0] == 200
    assert "Your recorded results could not be read" in planning[1]
    assert OBS not in planning[1] and er.WITHDRAWAL_MARKER not in planning[1]
    report = out["pages"]["w"]["report"]
    assert report[0] == 200
    assert "Your recorded results could not be read, so whether this experiment has" in report[1]
    assert "No result recorded." not in report[1] and "You recorded" not in report[1]
    assert out["pages"]["w"]["export"] == [503, ""]

    # ordinary legacy history stays readable unchanged by the baseline
    assert out["o_load"] == ["ok", _ser(before_o)]
    assert out["pages"]["o"]["planning"][0] == 200 and OBS2 in out["pages"]["o"]["planning"][1]
    assert "You recorded 1 execution(s)." in out["pages"]["o"]["report"][1]
    assert out["pages"]["o"]["export"][0] == 200
    assert json.loads(out["pages"]["o"]["export"][1])["export_format_version"] \
        == "inventorai-disclosure-json/2"

    # the candidate reads every row unchanged afterwards (baseline-written rows included)
    store = webapp._get_store()
    assert store.load_result_events(sid_w) == before_w
    assert store.load_result_events(sid_o) == before_o
    assert _ser(store.load_result_events(sid_l)) == out["l_load"]
    assert [e.result_text for e in store.load_result_events(sid_l)] == ["legacy root", "legacy fix"]
