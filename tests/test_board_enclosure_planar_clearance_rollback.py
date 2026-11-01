"""BOARD-ENCLOSURE-PLANAR-CLEARANCE-01 — the removal-generation guard holds across a rollback interval.

Independent review F1: with the guard maintained only by the new participation writer, the PRE-increment build
(run during a disable-and-preserve rollback) could remove and re-add a participant without moving the removal
generation, so the old binding came back as CURRENT after rolling forward. The generation is now maintained by a
database trigger on ``subsystem_interface_components``, so ANY build's DELETE moves it on. This test runs the
exact pre-increment build (extracted from Git, run with ``-I`` so only its own modules import) against a database
the current build migrated and declared on, then reopens it with the current build.
"""
import io
import json
import os
import subprocess
import sys
import tarfile

import pytest

from engine import subsystem_model as sm
from engine.record_store import SqliteRecordStore
from tests.test_board_enclosure_planar_clearance import _declare, _issues, _setup

BASELINE = "798d7750b0fa91e79cba9f37949608abd4386c2c"     # the PR's base: the pre-increment build
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TREE = ("engine", "domains", "docs", "schemas", "prompts", "database")

_PROBE = r'''
import json, sys
base, db, out_path, pid, ifc, keep, churn, other = sys.argv[1:9]
sys.path.insert(0, base)
from engine.record_store import SqliteRecordStore
store = SqliteRecordStore(db, create=False)
out = {"removed": store.set_interface_participation(pid, ifc, [keep, other],
                                                   [keep, churn, other]),
       "readded": store.set_interface_participation(pid, ifc, [keep, churn, other],
                                                   [keep, other])}
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
    root = tmp_path_factory.mktemp("pcc_baseline")
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(root, filter="data")
    probe = tmp_path_factory.mktemp("pcc_probe") / "probe.py"
    probe.write_text(_PROBE, encoding="utf-8")
    return str(root), str(probe)


def test_rb_a_participant_churned_by_the_pre_increment_build_does_not_revive_the_binding(
        baseline, tmp_path):
    db = str(tmp_path / "rollback.db")
    store = SqliteRecordStore(db)
    pid, _subs, ifc, b, e, x = _setup(store)
    _declare(store, pid, ifc, b, e)
    assert _issues(store, pid, ifc) == ()
    store.close()

    root, probe = baseline
    out_path = tmp_path / "out.json"
    done = subprocess.run([sys.executable, "-I", probe, root, db, str(out_path), pid, ifc, b, e, x],
                          cwd=root, env=dict(os.environ), capture_output=True, text=True,
                          timeout=600)
    assert done.returncode == 0, done.stderr[-4000:]
    out = json.loads(out_path.read_text(encoding="utf-8"))
    assert out == {"removed": "SAVED", "readded": "SAVED"}    # the old build's own writer did it

    reopened = SqliteRecordStore(db)
    snap = reopened.load_planar_clearance(pid)
    assert snap["epochs"][(ifc, e)] == 1                       # the trigger fired for the old build
    assert _issues(reopened, pid, ifc) == ((sm.PCC_ISSUE_PARTICIPATION_CHANGED, sm.PCC_ROLE_ENCLOSURE),)
    rows = reopened._conn.execute("SELECT COUNT(*) FROM planar_clearance_revisions").fetchone()
    assert rows == (1,)                                         # preserved; nothing rewritten
