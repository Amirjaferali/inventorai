"""G1-PLANAR-MOMENT-SAVED-DECLARATION-01 - what the PRE-increment build ACTUALLY does with an upgraded database.

Rollback is disable-and-preserve. The pre-increment build (this PR's base, 7d02d80) is extracted from Git and run
with ``-I`` so only its own modules import, against a database the current build migrated and wrote saved
planar-moment configurations to. Observed and pinned:

* it opens the upgraded database (the additive ``planar_moment_revisions`` table is ignored);
* it reads the UNCHANGED component inventory exactly as before and still declares components;
* it never reads or writes a saved configuration: re-opening with the current build (re-upgrade, an idempotent
  migration) finds every revision intact beside the component the old build added.
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
from tests.test_component_inventory_correct_withdraw import _declare_store
from tests.test_g1_planar_moment_saved_declaration import _declare_pm, POINT
from tests.test_stage15_integrated_invention_entry import MECH, _contract, _ri

BASELINE = "7d02d8072bffffca331031df7aa65439d50e0500"    # the PR's base: the pre-increment build
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TREE = ("engine", "domains", "docs", "schemas", "prompts", "database")

_PROBE = r'''
import json, sys
base, db, out_path, pid = sys.argv[1:5]
sys.path.insert(0, base)
from engine.record_store import SqliteRecordStore
from engine import subsystem_model as sm
store = SqliteRecordStore(db, create=False)
out = {"tables": sorted(r[0] for r in store._conn.execute(
    "SELECT name FROM sqlite_master WHERE type = 'table'")),
       "has_reader": hasattr(store, "load_planar_moments")}
subs = store.load_project_subsystems(pid)
out["before"] = [c.display_name for c in store.load_component_inventory(pid)[1]]
item = sm.declared_component(subs, "Added by the old build", "Old build", ())
store.append_project_component(pid, item, "old-build-key")
out["after"] = [c.display_name for c in store.load_component_inventory(pid)[1]]
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
    root = tmp_path_factory.mktemp("pm_baseline")
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(root, filter="data")
    probe = tmp_path_factory.mktemp("pm_probe") / "probe.py"
    probe.write_text(_PROBE, encoding="utf-8")
    return str(root), str(probe)


def test_rb_the_pre_increment_build_ignores_saved_configurations_and_keeps_working(baseline, tmp_path):
    db = str(tmp_path / "upgraded.db")
    store = SqliteRecordStore(db)
    pid = store.create_project(_contract(), reconstruction_inputs=_ri(MECH))
    comp = _declare_store(store, pid, (), "Folding flap")
    _outcome, stored = _declare_pm(store, pid, comp.component_id)
    ledger = store.load_planar_moments(pid)["ledger"]
    store.append_planar_moment_revision(
        pid, sm.withdrawn_planar_moment(ledger, stored.declaration_id, 0), "k-w")
    rows = store._conn.execute("SELECT * FROM planar_moment_revisions ORDER BY event_seq").fetchall()
    store.close()

    root, probe = baseline
    out_path = tmp_path / "out.json"
    done = subprocess.run([sys.executable, "-I", probe, root, db, str(out_path), pid],
                          cwd=root, env=dict(os.environ), capture_output=True, text=True, timeout=600)
    assert done.returncode == 0, done.stderr[-4000:]
    out = json.loads(out_path.read_text(encoding="utf-8"))
    assert "planar_moment_revisions" in out["tables"] and out["has_reader"] is False
    assert out["before"] == ["Folding flap"]
    assert out["after"] == ["Folding flap", "Added by the old build"]

    reopened = SqliteRecordStore(db, create=False)          # re-upgrade: idempotent migration
    try:
        assert reopened._conn.execute(
            "SELECT * FROM planar_moment_revisions ORDER BY event_seq").fetchall() == rows
        record = reopened.load_planar_moments(pid)["ledger"].record_for(stored.declaration_id)
        assert record.withdrawn and record.current.point_description == POINT
        names = [c.display_name for c in reopened.load_component_inventory(pid)[1]]
        assert names == ["Folding flap", "Added by the old build"]
    finally:
        reopened.close()
