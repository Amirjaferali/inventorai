"""G1-2 CONSTRAINT-ENGINEERING-LINK-01 - what the PRE-increment build ACTUALLY does with an upgraded database.

Rollback is disable-and-preserve. The pre-increment build (this PR's base, 170c1f8) is extracted from Git and run
with ``-I`` so only its own modules import, against a database the current build migrated and wrote a link and
acceptance notes to. Observed and pinned:

* it opens the upgraded database (the additive ``constraint_engineering_links`` table and its triggers are ignored);
* it reads the UNCHANGED ``constraint_acceptance_preparations`` table exactly as before and still writes notes;
* it never reads or writes a link row: re-opening with the current build (re-upgrade, an idempotent migration)
  finds the link intact, with its generation, beside the notes the old build wrote.
"""
import io
import json
import os
import sqlite3
import subprocess
import sys
import tarfile

import pytest

from engine.record_store import SqliteRecordStore
from tests.test_g1_constraint_engineering_link import _db, _heads, _link, _row, _setup, client  # noqa: F401
from tests.test_mandatory_constraint_acceptance_preparation import _form_for, _post as _pca_post

BASELINE = "170c1f8f99ce5fa4e8d5da61f30e2243a573d2ae"    # the PR's base: the pre-increment build
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TREE = ("engine", "domains", "docs", "schemas", "prompts", "database")

_PROBE = r'''
import json, sys
base, db, out_path, pid, cid, record = sys.argv[1:7]
sys.path.insert(0, base)
from engine.record_store import SqliteRecordStore
from engine.idea_state import current_constraint_acceptance
store = SqliteRecordStore(db, create=False)
before = store.load_constraint_acceptance(pid)
shown = current_constraint_acceptance(before["preparations"], before["history"])
prep, earlier = shown[cid]
out = {"read": [prep.acceptance_criterion, prep.evidence_needed, earlier],
       "tables": sorted(r[0] for r in store._conn.execute(
           "SELECT name FROM sqlite_master WHERE type = 'table'"))}
outcome = store.set_constraint_acceptance(
    pid, cid, record, {"acceptance_criterion": "Gap of 3 mm, written by the old build",
                       "evidence_needed": None},
    {"acceptance_criterion": prep.acceptance_criterion, "evidence_needed": prep.evidence_needed,
     "earlier": earlier})
out["write"] = outcome
after = store.load_constraint_acceptance(pid)
out["after"] = [p.acceptance_criterion for p in after["preparations"]]
store.close()
with open(out_path, "w", encoding="utf-8") as fh:
    json.dump(out, fh)
'''


@pytest.fixture(scope="module")
def baseline(tmp_path_factory):
    have = subprocess.run(["git", "cat-file", "-e", BASELINE + "^{commit}"], cwd=_REPO,
                          capture_output=True)
    if have.returncode != 0:
        pytest.fail("the rollback baseline %s is not available in this checkout" % BASELINE)
    archive = subprocess.run(["git", "archive", "--format=tar", BASELINE, *_TREE], cwd=_REPO,
                             capture_output=True, check=True).stdout
    root = tmp_path_factory.mktemp("cel_baseline")
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(root, filter="data")
    probe = tmp_path_factory.mktemp("cel_probe") / "probe.py"
    probe.write_text(_PROBE, encoding="utf-8")
    return str(root), str(probe)


def test_rb_the_pre_increment_build_keeps_using_the_notes_and_never_touches_links(
        client, baseline, tmp_path):
    sid, _ifc, _ids, cid = _setup(client)
    _pca_post(client, sid, _form_for(client, sid, cid), crit="Gap of 2 mm on every side")
    _link(client, sid, cid)
    link = _row(sid, cid)
    record = _heads(sid)[cid].record_id

    root, probe = baseline
    out_path = tmp_path / "out.json"
    done = subprocess.run([sys.executable, "-I", probe, root, _db(), str(out_path), sid, cid, record],
                          cwd=root, env=dict(os.environ), capture_output=True, text=True, timeout=600)
    assert done.returncode == 0, done.stderr[-4000:]
    out = json.loads(out_path.read_text(encoding="utf-8"))
    assert out["read"] == ["Gap of 2 mm on every side", None, False]   # the notes table, unchanged
    assert "constraint_engineering_links" in out["tables"]            # present, ignored
    assert out["write"] == "SAVED"
    assert out["after"] == ["Gap of 3 mm, written by the old build"]

    assert _row(sid, cid) == link                                     # the old build never touched it
    reopened = SqliteRecordStore(_db(), create=False)                 # re-upgrade: idempotent migration
    try:
        state = reopened.load_constraint_engineering_links(sid)
        stored = next(item for item in state["links"] if item.constraint_id == cid)
        assert (stored.constraint_record, stored.revision_id, stored.generation) == link
        notes = reopened.load_constraint_acceptance(sid)["preparations"]
        assert [p.acceptance_criterion for p in notes] == ["Gap of 3 mm, written by the old build"]
    finally:
        reopened.close()
    con = sqlite3.connect(_db())
    try:
        triggers = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type = 'trigger' AND name LIKE 'constraint_engineering%'")]
    finally:
        con.close()
    assert sorted(triggers) == ["constraint_engineering_links_generation_grows",
                                "constraint_engineering_links_insert_generation_grows",
                                "constraint_engineering_links_no_delete"]
