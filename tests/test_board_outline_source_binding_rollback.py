"""BOARD-OUTLINE-SOURCE-BINDING-01 - what the PRE-increment build ACTUALLY does with a v2 database.

The supported rollback target is THIS build with v2 writes off (tested in
``test_board_outline_source_binding.py``). The pre-increment build (the PR's base,
560cfa7) cannot be made to honour the source binding: this test records its real
behaviour on a database the current build migrated and wrote a file-linked (v2)
declaration to. The old build is extracted from Git and run with ``-I`` so only its
own modules import. Observed and pinned:

* it opens the upgraded database (the additive table and its triggers are ignored);
* it reads the v2 revision as NEEDS RECONFIRMATION (``METHOD_CHANGED``: it knows only
  ``planar-clearance-declaration/1``), so it shows no evaluation and offers no CAD file;
* a correction it writes is source-free (v1), so the file link silently ends there; the
  current build then reads the whole history - the v2 revision keeps its binding.
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
from tests.test_board_enclosure_planar_clearance import _material, _setup

BASELINE = "560cfa7c88d3fa6d413fb6c82599289c65ad0e34"    # the PR's base: the pre-increment build
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TREE = ("engine", "domains", "docs", "schemas", "prompts", "database", "web/planar_clearance.py")

_PROBE = r'''
import json, sys
base, db, out_path, pid, ifc = sys.argv[1:6]
sys.path.insert(0, base)
from engine.record_store import SqliteRecordStore
from engine import subsystem_model as sm
from engine import mechanical_planar_clearance_method as mm
from engine import deterministic_calculation as dc
from web import planar_clearance as view_model
store = SqliteRecordStore(db, create=False)
snap = store.load_planar_clearance(pid)
record = snap["ledger"].active_for(ifc)
binding = dc.bind_method(mm.METHOD_ID, mm.METHOD_VERSION, mm.evaluate)
view = view_model.clearance_view(snap, ifc, binding)
out = {"declaration_version": record.current.declaration_version,
       "issues": [list(i) for i in sm.planar_clearance_binding_issues(
           record.current, snap["inventory"], snap["participations"], snap["epochs"])],
       "state": view["state"], "cad_eligible": view_model.cad_eligible(view),
       "evaluated": view["evaluation"] is not None}
m = record.current
material = sm.planar_clearance_material(
    snap["inventory"], snap["interfaces"], snap["participations"], snap["epochs"], ifc,
    m.board_component_id, m.enclosure_component_id, m.board_component_revision,
    m.enclosure_component_revision, m.board_participation_epoch,
    m.enclosure_participation_epoch, m.region_description, ("84", "50", "90", "56", "2"),
    m.basis, m.applicability)
rev = sm.corrected_planar_clearance(snap["ledger"], record.declaration_id,
                                    record.head_revision_no, material)
outcome, stored = store.append_planar_clearance_revision(pid, rev, "old-build-correction")
out["old_correction"] = [outcome, stored.material.declaration_version]
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
    root = tmp_path_factory.mktemp("bosb_baseline")
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        tar.extractall(root, filter="data")
    with open(os.path.join(root, "web", "__init__.py"), "w", encoding="utf-8"):
        pass
    probe = tmp_path_factory.mktemp("bosb_probe") / "probe.py"
    probe.write_text(_PROBE, encoding="utf-8")
    return str(root), str(probe)


def test_rb_the_pre_increment_build_reads_v2_as_needs_reconfirmation_and_writes_v1(
        baseline, tmp_path):
    db = str(tmp_path / "rollback.db")
    store = SqliteRecordStore(db)
    pid, _subs, ifc, b, e, _x = _setup(store)
    snap, m = _material(store, pid, ifc, b, e)
    source = sm.PlanarClearanceSource(
        kind="kicad_pcb", source_sha256="a" * 64, source_size=2214,
        format_id="kicad-board/20260206", reader_id="kicad-board-outline-reader/1",
        rule_id="edge-cuts-one-rectangle/1", file_x="84", file_y="50",
        axis_assignment="file_x_is_board_x", inspected_at="2026-11-06T00:00:00+00:00",
        nonce_hash="b" * 64, carry_forward_from=None)
    m2 = sm.planar_clearance_material(
        snap["inventory"], snap["interfaces"], snap["participations"], snap["epochs"], ifc,
        b, e, m.board_component_revision, m.enclosure_component_revision,
        m.board_participation_epoch, m.enclosure_participation_epoch, m.region_description,
        m.values, m.basis, m.applicability, source=source)
    store.append_planar_clearance_revision(
        pid, sm.declared_planar_clearance(snap["ledger"], m2), "k-v2", allow_source=True)
    store.close()

    root, probe = baseline
    out_path = tmp_path / "out.json"
    done = subprocess.run([sys.executable, "-I", probe, root, db, str(out_path), pid, ifc],
                          cwd=root, env=dict(os.environ), capture_output=True, text=True,
                          timeout=600)
    assert done.returncode == 0, done.stderr[-4000:]
    out = json.loads(out_path.read_text(encoding="utf-8"))
    assert out["declaration_version"] == sm.PLANAR_CLEARANCE_DECLARATION_V2
    assert out["issues"] == [[sm.PCC_ISSUE_METHOD_CHANGED, None]]
    assert (out["state"], out["cad_eligible"], out["evaluated"]) == (
        "NEEDS_RECONFIRMATION", False, False)
    assert out["old_correction"] == ["INSERTED", "planar-clearance-declaration/1"]

    reopened = SqliteRecordStore(db)
    record = reopened.load_planar_clearance(pid)["ledger"].active_for(ifc)
    assert [r.material.declaration_version for r in record.revisions] == [
        sm.PLANAR_CLEARANCE_DECLARATION_V2, "planar-clearance-declaration/1"]
    assert record.revisions[0].material.source == source          # the binding is intact
    assert record.current.source is None                          # the link ended at the old build
    reopened.close()
