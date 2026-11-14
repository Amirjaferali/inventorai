"""BOARD-ENCLOSURE-PLANAR-CLEARANCE-01 — the board-enclosure planar clearance journey.

Synthetic data only. What is pinned:
  * the method (``engine/mechanical_planar_clearance_method.py`` + consumer
    ``engine/mechanical_planar_clearance.py``): margin = (region - board)/2 - c per axis, met exactly when both
    margins are nonnegative (equality meets), decided on the EXACT entered decimals with an independent oracle
    (region >= board + 2c); the binary owner result is bridged within the derived absolute / mixed bound (the
    100.1 / 99.9 / 0.1 cancellation is exactly zero, MET); no rotation; strict grammar; missing never zero;
  * the declaration lifecycle (``engine/subsystem_model.py`` + ``engine/record_store.py``): append-only revisions,
    correction / withdrawal, resource limits with the reserved withdrawal, stale / forged / cross-project refusal
    inside the serialized write, exact retry as a no-op, component / participation staleness and the removal
    generation that stops a removed-then-re-added participant from reviving an old binding, fail-closed reads;
  * the output (``web/planar_clearance.py``, the page, the report and the PDF): ONE presentation model, the same
    snapshot identity and outcome everywhere, one store read per report render, escaped text, the English-only
    notice on the Arabic interface, no stored result;
  * protected behaviour: the session page, answer ledger and the Stage 35 export are unchanged by the journey.
"""
import html as _html
import os
import random
import re
import sqlite3
import threading
from decimal import Decimal
from fractions import Fraction

import pytest

import web.app as appmod
from engine import deterministic_calculation as dc
from engine import mechanical_planar_clearance as pcc
from engine import mechanical_planar_clearance_method as method
from engine import subsystem_model as sm
from engine.record_store import (
    PLANAR_CLEARANCE_EXACT_REPLAY, PLANAR_CLEARANCE_INSERTED, PlanarClearanceConflict,
    PlanarClearanceCorrupt, PlanarClearanceRejected, SqliteRecordStore)
from tests.csrf_client import csrf_client
from tests.test_component_interface_participation import (
    _cmp, _form as _icp_form, _ifc, _post as _icp_post, _project, _web_project)
from tests.test_component_inventory_correct_withdraw import _correct, _withdraw
from tests.test_stage15_integrated_invention_entry import _pdf_source
from web import planar_clearance as view_mod
from web import ui_text

BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
APPLIES = tuple(pcc.ANSWER_APPLIES for _ in pcc.DECLARATION_IDS)


# ==========================================================================
# 1. method and consumer
# ==========================================================================
def _ev(values, answers=APPLIES, region="Inner floor between the posts"):
    return pcc.evaluate({"values": dict(zip(pcc.VALUE_ROLES, values)),
                         "region_description": region,
                         "applicability": dict(zip(pcc.DECLARATION_IDS, answers))}, BINDING)


def _margins(result):
    return [(a["axis"], a["margin_text"], a["met"]) for a in result["axes"]]


def test_m01_the_declared_example_and_its_correction():
    r = _ev(("84", "50", "86", "56", "2"))
    assert r["outcome"] == pcc.OUTCOME_NOT_MET
    assert _margins(r) == [("x", "-1", False), ("y", "1", True)]
    assert r["axes"][0]["shortfall_text"] == "1" and r["axes"][1]["shortfall_text"] is None
    r = _ev(("84", "50", "90", "56", "2"))
    assert r["outcome"] == pcc.OUTCOME_MET
    assert _margins(r) == [("x", "1", True), ("y", "1", True)]


@pytest.mark.parametrize("values,outcome,margins", [
    (("10", "10", "14", "14", "1"), "MET", [("x", "1", True), ("y", "1", True)]),
    (("10", "10", "12", "12", "1"), "MET", [("x", "0", True), ("y", "0", True)]),   # equality meets
    (("10", "10", "11.9998", "12", "1"), "NOT_MET", [("x", "-0.0001", False), ("y", "0", True)]),
    (("10", "10", "12.0002", "12", "1"), "MET", [("x", "0.0001", True), ("y", "0", True)]),
    (("10", "10", "10", "10", "0"), "MET", [("x", "0", True), ("y", "0", True)]),     # c = 0, touching
    (("10", "10", "9", "20", "0"), "NOT_MET", [("x", "-0.5", False), ("y", "5", True)]),  # board larger
    (("30", "30", "20", "20", "1"), "NOT_MET", [("x", "-6", False), ("y", "-6", False)]),  # both axes
    (("99.9", "50", "100.1", "56", "0.1"), "MET", [("x", "0", True), ("y", "2.9", True)]),  # cancellation
    (("0.0001", "0.0001", "0.0003", "0.0003", "0.0001"), "MET", [("x", "0", True), ("y", "0", True)]),
    (("999999.9999", "1", "999999.9999", "3", "0"), "MET", [("x", "0", True), ("y", "1", True)]),
    (("999999.9998", "1", "999999.9999", "1", "0.0001"), "NOT_MET",
     [("x", "-0.00005", False), ("y", "-0.0001", False)]),
])
def test_m02_boundaries_against_the_independent_oracle(values, outcome, margins):
    r = _ev(values)
    assert r["outcome"] == outcome and _margins(r) == margins
    bx, by, rx, ry, c = (Decimal(v) for v in values)
    assert (rx >= bx + 2 * c and ry >= by + 2 * c) == (outcome == "MET")


def test_m03_the_binary_path_cancels_but_the_decision_is_exact():
    raw = method.evaluate(99.9, 50.0, 100.1, 56.0, 0.1)
    assert raw["margin_x"] != 0.0 and raw["margin_x"] < 0   # binary cancellation
    exact = (Fraction("100.1") - Fraction("99.9")) / 2 - Fraction("0.1")
    assert exact == 0
    assert pcc.agrees_with_reference(raw["margin_x"], exact, Fraction("100.1"),
                                     Fraction("99.9"), Fraction("0.1"))
    assert _ev(("99.9", "50", "100.1", "56", "0.1"))["outcome"] == "MET"
    assert method.evaluate(10.0, 10.0, 12.0, 12.0, 1.0) == {"margin_x": 0.0, "margin_y": 0.0}


def test_m04_no_rotation_is_tried_and_axes_stay_paired():
    assert _ev(("84", "50", "86", "56", "1"))["outcome"] == "MET"
    swapped = _ev(("50", "84", "86", "56", "1"))
    assert swapped["outcome"] == "NOT_MET"
    assert _margins(swapped) == [("x", "17", True), ("y", "-15", False)]


def test_m05_random_decimals_agree_with_the_oracle_and_the_bridge():
    rng = random.Random(20261101)
    for _ in range(400):
        def dec(lo):
            whole = rng.randint(lo, 2000)
            frac = rng.randint(0, 9999)
            return "%d.%04d" % (whole, frac) if rng.random() < 0.7 else str(max(whole, lo))
        bx, by = dec(1), dec(1)
        rx = str(Decimal(bx) + Decimal(rng.choice(["-2", "0", "0.0002", "1", "3.5"])) + 2)
        ry = str(Decimal(by) + Decimal(rng.choice(["-1", "0", "2", "0.0001"])) + 2)
        c = rng.choice(["0", "1", "0.0001", "1.25"])
        values = (bx, by, rx, ry, c)
        if not all(pcc.is_admitted_value(r, v) for r, v in zip(pcc.VALUE_ROLES, values)):
            continue
        r = _ev(values)
        oracle = Decimal(rx) >= Decimal(bx) + 2 * Decimal(c) and \
            Decimal(ry) >= Decimal(by) + 2 * Decimal(c)
        assert r["outcome"] == ("MET" if oracle else "NOT_MET"), values
        for axis, b, reg in (("x", bx, rx), ("y", by, ry)):
            m = (Decimal(reg) - Decimal(b)) / 2 - Decimal(c)
            got = [a for a in r["axes"] if a["axis"] == axis][0]
            assert Decimal(got["margin_text"]) == m


@pytest.mark.parametrize("text", ["-1", "+1", "1e3", "inf", "nan", "1,5", "١٢", "1234567", "1.23456",
                                  " 1", "1 ", ".5", "5.", "", "0x10", "1/2", "12mm"])
def test_m06_the_grammar_refuses_everything_else(text):
    assert pcc.parse_value(text) is None
    assert not pcc.is_admitted_value("board_x", text)


def test_m07_domain_and_representation_policy():
    assert not pcc.is_admitted_value("board_x", "0") and not pcc.is_admitted_value("region_y", "0.0000")
    assert pcc.is_admitted_value("c", "0") and pcc.is_admitted_value("c", "0.0")
    assert pcc.is_admitted_value("board_x", "999999.9999")
    for bad in ((-1.0, 1.0, 1.0, 1.0, 0.0), (1.0, 1.0, 1.0, 1.0, -0.5),
                (float("inf"), 1.0, 1.0, 1.0, 0.0), (1, 1.0, 1.0, 1.0, 0.0)):
        with pytest.raises(ArithmeticError):
            method.evaluate(*bad)


def test_m08_missing_unknown_unanswered_and_inapplicable():
    r = _ev(("84", None, "86", "56", "unknown"))
    assert r["outcome"] == "MISSING_INFORMATION" and r["missing"] == ["board_y", "c"]
    assert r["axes"] is None and r["margins"] is None
    answers = list(APPLIES)
    answers[2] = None
    r = _ev(("84", "50", "86", "56", "2"), tuple(answers))
    assert r["outcome"] == "MISSING_INFORMATION" and r["missing"] == ["region_unobstructed"]
    assert _ev(("84", "50", "86", "56", "2"), region=None)["missing"] == ["region_description"]
    answers[2] = pcc.ANSWER_DOES_NOT_APPLY
    r = _ev(("84", "50", "86", "56", "2"), tuple(answers))
    assert r["outcome"] == "INAPPLICABLE" and r["inapplicable"] == ["region_unobstructed"]
    assert r["axes"] is None


def test_m09_owner_and_bridge_failures_yield_no_verdict(tmp_path, monkeypatch):
    def liar(board_x, board_y, region_x, region_y, c):
        return {"margin_x": 5.0, "margin_y": 5.0}
    liar.__module__, liar.__qualname__ = method.evaluate.__module__, method.evaluate.__qualname__
    bad = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, liar)
    r = pcc.evaluate({"values": dict(zip(pcc.VALUE_ROLES, ("84", "50", "86", "56", "2"))),
                      "region_description": "x", "applicability":
                      dict(zip(pcc.DECLARATION_IDS, APPLIES))}, bad)
    assert r["outcome"] == "COULD_NOT_BE_COMPUTED" and r["axes"] is None
    assert r["owner_reason"] == dc.EXECUTION_INTEGRITY_FAILURE
    wrong = dc.bind_method(method.METHOD_ID, "0.9", method.evaluate)
    r = pcc.evaluate({"values": dict(zip(pcc.VALUE_ROLES, ("84", "50", "86", "56", "2"))),
                      "region_description": "x", "applicability":
                      dict(zip(pcc.DECLARATION_IDS, APPLIES))}, wrong)
    assert (r["outcome"], r["owner_state"], r["owner_reason"]) == (
        "COULD_NOT_BE_COMPUTED", dc.STATE_REFUSAL, dc.VERSION_MISMATCH)
    artifact = pcc.load_artifact()
    artifact["disclosure"][0] = "These values are verified."
    with pytest.raises(pcc.PlanarClearanceKnowledgeError):
        pcc.validate_artifact(artifact)
    monkeypatch.setattr(pcc, "ARTIFACT_PATH", tmp_path / "missing.json")
    assert _ev(("84", "50", "86", "56", "2"))["outcome"] == "COULD_NOT_BE_COMPUTED"


def test_m10_display_is_exact_and_never_rounds():
    assert pcc.format_exact(Fraction("-0.00005")) == "-0.00005"
    assert pcc.format_exact(Fraction(0)) == "0"
    assert pcc.format_exact(Fraction("123456.78905")) == "123456.78905"
    with pytest.raises(ValueError):
        pcc.format_exact(Fraction(1, 3))


def test_m11_owner_registration_is_one_bounded_admission():
    assert (method.METHOD_ID, "1.0") in dc.ADMITTED_METHODS and len(dc.ADMITTED_METHODS) == 14
    data = dc.load_artifact()
    assert data["artifact_version"] == "14" and dc.IMPLEMENTATION_VERSION == "1.13.0"
    record = [m for m in data["methods"] if m["method_id"] == method.METHOD_ID][0]
    assert {r["unit_token"] for r in record["input_roles"] + record["output_roles"]} == {"mm"}
    assert record["result_range"] == [] and len(record["applicability"]) == 4
    assert record["source_qualification"][0]["source_use_policy_ref"] == "dcu:SU001"
    owner_source = open(dc.__file__, encoding="utf-8").read()
    assert "mechanical_planar_clearance" not in owner_source
    app_source = open(appmod.__file__, encoding="utf-8").read()
    assert app_source.count("_dcalc.bind_method(") == 14


# ==========================================================================
# 2. declaration lifecycle (store)
# ==========================================================================
@pytest.fixture
def store(tmp_path):
    return SqliteRecordStore(str(tmp_path / "pcc.db"))


def _setup(store, idea="i-pcc"):
    pid, subs = _project(store, idea)
    ifc = _ifc(store, pid, subs, key="i-" + idea)
    b = _cmp(store, pid, subs, "Board", key="kb-" + idea)
    e = _cmp(store, pid, subs, "Case", key="ke-" + idea)
    x = _cmp(store, pid, subs, "Spare", key="kx-" + idea)
    store.set_interface_participation(pid, ifc, [b, e, x], [])
    return pid, subs, ifc, b, e, x


def _material(store, pid, ifc, b, e, values=("84", "50", "86", "56", "2"), **over):
    snap = store.load_planar_clearance(pid)
    inv, ep = snap["inventory"], snap["epochs"]
    def head(component_id):
        record = inv.record_for(component_id)
        return record.head_revision_no if record is not None else 0
    args = dict(brev=head(b), erev=head(e),
                bep=ep.get((ifc, b), 0), eep=ep.get((ifc, e), 0), region="Inner floor",
                basis=(None, None, None), answers=APPLIES)
    args.update(over)
    return snap, sm.planar_clearance_material(
        inv, snap["interfaces"], snap["participations"], ep, ifc, b, e, args["brev"],
        args["erev"], args["bep"], args["eep"], args["region"], tuple(values),
        args["basis"], args["answers"])


def _declare(store, pid, ifc, b, e, key="k-decl", **kw):
    snap, m = _material(store, pid, ifc, b, e, **kw)
    rev = sm.declared_planar_clearance(snap["ledger"], m)
    return store.append_planar_clearance_revision(pid, rev, key)


def _active(store, pid, ifc):
    return store.load_planar_clearance(pid)["ledger"].active_for(ifc)


def _correct_decl(store, pid, ifc, b, e, key, values, head=None):
    snap, m = _material(store, pid, ifc, b, e, values=values)
    rec = snap["ledger"].active_for(ifc)
    rev = sm.corrected_planar_clearance(
        snap["ledger"], rec.declaration_id, rec.head_revision_no if head is None else head, m)
    return store.append_planar_clearance_revision(pid, rev, key)


def _issues(store, pid, ifc):
    snap = store.load_planar_clearance(pid)
    rec = snap["ledger"].active_for(ifc)
    return sm.planar_clearance_binding_issues(rec.current, snap["inventory"],
                                              snap["participations"], snap["epochs"])


def _rows(store, pid):
    return store._conn.execute(
        "SELECT * FROM planar_clearance_revisions WHERE project_id = ? ORDER BY event_seq",
        (pid,)).fetchall()


def test_s01_create_reload_correct_withdraw_and_history_is_immutable(tmp_path):
    path = str(tmp_path / "s01.db")
    store = SqliteRecordStore(path)
    pid, subs, ifc, b, e, _x = _setup(store)
    outcome, rev = _declare(store, pid, ifc, b, e)
    assert outcome == PLANAR_CLEARANCE_INSERTED and rev.revision_no == 0
    first = _rows(store, pid)
    rec = _active(SqliteRecordStore(path), pid, ifc)              # a fresh process view
    assert rec.current.values == ("84", "50", "86", "56", "2")
    assert rec.current.board_component_id == b and rec.current.enclosure_component_id == e
    _correct_decl(store, pid, ifc, b, e, "k2", ("84", "50", "90", "56", "2"))
    assert _rows(store, pid)[0] == first[0]                      # earlier row untouched
    rec = _active(store, pid, ifc)
    assert rec.head_revision_no == 1 and rec.current.values[2] == "90"
    w = sm.withdrawn_planar_clearance(store.load_planar_clearance(pid)["ledger"],
                                      rec.declaration_id, 1)
    store.append_planar_clearance_revision(pid, w, "k3")
    ledger = store.load_planar_clearance(pid)["ledger"]
    assert ledger.active_for(ifc) is None
    assert [r.kind for r in ledger.records[0].revisions] == ["DECLARED", "CORRECTED", "WITHDRAWN"]
    assert len(_rows(store, pid)) == 3                           # withdrawal is not erasure


def test_s02_exact_retry_is_a_no_op_and_a_restatement_is_unchanged(store):
    pid, subs, ifc, b, e, _x = _setup(store)
    snap, m = _material(store, pid, ifc, b, e)
    rev = sm.declared_planar_clearance(snap["ledger"], m)
    assert store.append_planar_clearance_revision(pid, rev, "k1")[0] == PLANAR_CLEARANCE_INSERTED
    again = sm.PlanarClearanceRevision(revision_id=sm.new_planar_clearance_revision_id(),
                                       declaration_id=sm.new_planar_clearance_id(),
                                       revision_no=0, kind="DECLARED", interface_id=ifc, material=m)
    outcome, stored = store.append_planar_clearance_revision(pid, again, "k1")
    assert outcome == PLANAR_CLEARANCE_EXACT_REPLAY and stored.revision_id == rev.revision_id
    assert len(_rows(store, pid)) == 1
    with pytest.raises(sm.PlanarClearanceUnchanged):
        _correct_decl(store, pid, ifc, b, e, "k2", ("84", "50", "86", "56", "2"))
    other = sm.withdrawn_planar_clearance(store.load_planar_clearance(pid)["ledger"],
                                          rev.declaration_id, 0)
    with pytest.raises(PlanarClearanceConflict):
        store.append_planar_clearance_revision(pid, other, "k1")
    assert len(_rows(store, pid)) == 1


def test_s03_one_active_per_interaction_and_the_resource_limits(store):
    pid, subs, ifc, b, e, _x = _setup(store)
    _declare(store, pid, ifc, b, e)
    with pytest.raises(sm.PlanarClearanceActiveExists):
        _declare(store, pid, ifc, b, e, key="k-dup")
    for i in range(sm.MAX_PLANAR_CLEARANCE_CORRECTIONS):
        _correct_decl(store, pid, ifc, b, e, "kc%d" % i, ("84", "50", str(86 + i + 1), "56", "2"))
    with pytest.raises(sm.PlanarClearanceCorrectionLimit):
        _correct_decl(store, pid, ifc, b, e, "kc-over", ("84", "50", "200", "56", "2"))
    rec = _active(store, pid, ifc)
    w = sm.withdrawn_planar_clearance(store.load_planar_clearance(pid)["ledger"],
                                      rec.declaration_id, rec.head_revision_no)
    store.append_planar_clearance_revision(pid, w, "kw")        # the reserved withdrawal
    assert _active(store, pid, ifc) is None


def test_s04_the_lifetime_identity_limit(store):
    pid, subs, ifc, b, e, _x = _setup(store)
    for i in range(sm.MAX_PLANAR_CLEARANCE_IDENTITIES_PER_PROJECT):
        _declare(store, pid, ifc, b, e, key="kd%d" % i)
        rec = _active(store, pid, ifc)
        w = sm.withdrawn_planar_clearance(store.load_planar_clearance(pid)["ledger"],
                                          rec.declaration_id, 0)
        store.append_planar_clearance_revision(pid, w, "kw%d" % i)
    with pytest.raises(sm.PlanarClearanceIdentityLimit):
        _declare(store, pid, ifc, b, e, key="k-over")


def test_s05_stale_heads_forged_bindings_and_cross_project_identities(store):
    pid, subs, ifc, b, e, x = _setup(store)
    _declare(store, pid, ifc, b, e)
    _correct_decl(store, pid, ifc, b, e, "k2", ("84", "50", "90", "56", "2"))
    with pytest.raises(sm.PlanarClearanceStale):                 # an older head
        _correct_decl(store, pid, ifc, b, e, "k3", ("84", "50", "91", "56", "2"), head=0)
    with pytest.raises(sm.PlanarClearanceStale):                 # a forged component revision
        _material(store, pid, ifc, b, e, brev=5)
    with pytest.raises(sm.PlanarClearanceStale):                 # a forged generation
        _material(store, pid, ifc, b, e, eep=3)
    with pytest.raises(sm.PlanarClearanceNotEligible):           # same component twice
        _material(store, pid, ifc, b, b)
    other_pid, _s, other_ifc, ob, oe, _ox = _setup(store, idea="i-other")
    with pytest.raises(sm.PlanarClearanceNotEligible):           # another project's component
        _material(store, pid, ifc, b, ob)
    snap, m = _material(store, pid, ifc, b, e, values=("84", "50", "95", "56", "2"))
    forged = sm.PlanarClearanceRevision(
        revision_id=sm.new_planar_clearance_revision_id(),
        declaration_id=snap["ledger"].active_for(ifc).declaration_id, revision_no=2,
        kind="CORRECTED", interface_id=ifc,
        material=sm.PlanarClearanceMaterial(**{**m.__dict__, "board_participation_epoch": 7}))
    with pytest.raises(PlanarClearanceRejected) as exc:
        store.append_planar_clearance_revision(pid, forged, "k-forged")
    assert isinstance(exc.value.cause, sm.PlanarClearanceStale)
    with pytest.raises(Exception):                               # another project's write path
        store.append_planar_clearance_revision(other_pid, forged, "k-cross")
    assert len(_rows(store, pid)) == 2 and len(_rows(store, other_pid)) == 0


def test_s06_concurrent_corrections_from_one_head_never_both_win(tmp_path):
    path = str(tmp_path / "c.db")
    store = SqliteRecordStore(path)
    pid, subs, ifc, b, e, _x = _setup(store)
    _declare(store, pid, ifc, b, e)
    staged = []
    for i in range(2):
        snap, m = _material(store, pid, ifc, b, e, values=("84", "50", str(90 + i), "56", "2"))
        rec = snap["ledger"].active_for(ifc)
        staged.append(sm.corrected_planar_clearance(snap["ledger"], rec.declaration_id, 0, m))
    results = []

    def run(i):
        own = SqliteRecordStore(path)
        try:
            results.append(own.append_planar_clearance_revision(pid, staged[i], "kc%d" % i)[0])
        except PlanarClearanceRejected as exc:
            results.append(type(exc.cause).__name__)
    threads = [threading.Thread(target=run, args=(i,)) for i in range(2)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    assert sorted(results) == sorted([PLANAR_CLEARANCE_INSERTED, "PlanarClearanceStale"])


def test_s07_component_and_participation_changes_need_reconfirmation(store):
    pid, subs, ifc, b, e, x = _setup(store)
    _declare(store, pid, ifc, b, e)
    assert _issues(store, pid, ifc) == ()
    _correct(store, pid, b, 0, "Board v2", "Holds the parts")
    assert _issues(store, pid, ifc) == (("COMPONENT_CHANGED", "board"),)
    snap = store.load_planar_clearance(pid)
    view = view_mod.clearance_view(snap, ifc, BINDING)
    assert view["state"] == view_mod.STATE_RECONFIRM and view["evaluation"] is None
    _correct_decl(store, pid, ifc, b, e, "k-rebind", ("84", "50", "86", "56", "2"))  # explicit rebind
    assert _issues(store, pid, ifc) == ()
    store.set_interface_participation(pid, ifc, [b, x], [b, e, x])
    assert _issues(store, pid, ifc) == (("NOT_PARTICIPATING", "enclosure"),)
    _withdraw(store, pid, b, 1)
    assert ("COMPONENT_WITHDRAWN", "board") in _issues(store, pid, ifc)


def test_s08_removal_then_readdition_does_not_revive_the_old_binding(store):
    pid, subs, ifc, b, e, x = _setup(store)
    _declare(store, pid, ifc, b, e)
    store.set_interface_participation(pid, ifc, [b, x], [b, e, x])
    store.set_interface_participation(pid, ifc, [b, e, x], [b, x])
    assert _issues(store, pid, ifc) == (("PARTICIPATION_CHANGED", "enclosure"),)
    assert store.load_planar_clearance(pid)["epochs"][(ifc, e)] == 1
    store.set_interface_participation(pid, ifc, [b, x], [b, e, x])
    store.set_interface_participation(pid, ifc, [b, e, x], [b, x])
    assert store.load_planar_clearance(pid)["epochs"][(ifc, e)] == 2
    _correct_decl(store, pid, ifc, b, e, "k-rebind", ("84", "50", "86", "56", "2"))
    assert _issues(store, pid, ifc) == ()
    rec = _active(store, pid, ifc)
    assert rec.revisions[0].material.enclosure_participation_epoch == 0   # history kept
    assert rec.current.enclosure_participation_epoch == 2


def test_s08b_the_generation_moves_on_for_any_delete_and_the_guard_fails_closed(tmp_path):
    """Review F1: the removal generation is maintained by a database trigger, so a
    deletion issued by ANY code (here a raw statement, as a pre-increment build
    would issue it) moves it on; without the trigger nothing is trusted."""
    path = str(tmp_path / "trigger.db")
    store = SqliteRecordStore(path)
    pid, subs, ifc, b, e, x = _setup(store)
    _declare(store, pid, ifc, b, e)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("DELETE FROM subsystem_interface_components WHERE project_id = ? AND "
                 "interface_id = ? AND component_id = ?", (pid, ifc, e))
    conn.execute("INSERT INTO subsystem_interface_components (project_id, interface_id, "
                 "component_id) VALUES (?, ?, ?)", (pid, ifc, e))
    conn.commit()
    assert _issues(store, pid, ifc) == (("PARTICIPATION_CHANGED", "enclosure"),)
    store.set_interface_participation(pid, ifc, [b, x], [b, e, x])   # the new writer: once, not twice
    assert store.load_planar_clearance(pid)["epochs"][(ifc, e)] == 2
    conn.execute("DROP TRIGGER subsystem_interface_components_removal_generation")
    conn.commit()
    with pytest.raises(PlanarClearanceCorrupt):
        store.load_planar_clearance(pid)
    conn.execute("CREATE TRIGGER subsystem_interface_components_removal_generation AFTER "
                  "DELETE ON subsystem_interface_components BEGIN SELECT 1; END")
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(path)                                       # an unknown trigger shape


def test_s09_method_version_mismatch_is_never_substituted(store):
    pid, subs, ifc, b, e, _x = _setup(store)
    _declare(store, pid, ifc, b, e)
    store._conn.execute("UPDATE planar_clearance_revisions SET method_version = '0.9'")
    assert _issues(store, pid, ifc) == (("METHOD_CHANGED", None),)
    view = view_mod.clearance_view(store.load_planar_clearance(pid), ifc, BINDING)
    assert view["state"] == view_mod.STATE_RECONFIRM and view["evaluation"] is None


@pytest.mark.parametrize("sql", [
    "UPDATE planar_clearance_revisions SET event_seq = 5",
    "UPDATE planar_clearance_revisions SET value_board_x = '84.12345'",
    "UPDATE planar_clearance_revisions SET axis_pairing = 'rotated'",
    "INSERT INTO subsystem_interface_participation_epochs SELECT project_id, interface_id, "
    "'cmp-00000000000000000000000000000000', 1 FROM planar_clearance_revisions",
])
def test_s10_corrupt_history_reads_unavailable_never_not_recorded(store, sql):
    pid, subs, ifc, b, e, _x = _setup(store)
    _declare(store, pid, ifc, b, e)
    store._conn.execute("PRAGMA foreign_keys = OFF")
    try:
        store._conn.execute(sql)
    except sqlite3.IntegrityError:
        pytest.skip("the database backstop already refuses this row")
    store._conn.execute("PRAGMA foreign_keys = ON")
    with pytest.raises(PlanarClearanceCorrupt):
        store.load_planar_clearance(pid)


def test_s11_migration_is_additive_idempotent_and_refuses_an_unknown_shape(tmp_path):
    path = str(tmp_path / "m.db")
    SqliteRecordStore(path)
    SqliteRecordStore(path)                                       # idempotent
    conn = sqlite3.connect(path)
    conn.execute("DROP TABLE planar_clearance_revisions")
    conn.execute("CREATE TABLE planar_clearance_revisions (project_id TEXT)")
    conn.commit()
    conn.close()
    with pytest.raises(sqlite3.DatabaseError):
        SqliteRecordStore(path)


def test_s12_no_result_is_stored_and_the_answer_stream_is_untouched(store):
    pid, subs, ifc, b, e, _x = _setup(store)
    records_before = store._conn.execute(
        "SELECT COUNT(*) FROM records WHERE project_id = ?", (pid,)).fetchone()
    _declare(store, pid, ifc, b, e)
    cols = [r[1] for r in store._conn.execute("PRAGMA table_info(planar_clearance_revisions)")]
    assert not any(col.startswith(word) for col in cols
                   for word in ("margin", "result", "outcome", "verdict", "met_", "is_met"))
    assert store._conn.execute("SELECT COUNT(*) FROM records WHERE project_id = ?",
                               (pid,)).fetchone() == records_before


# ==========================================================================
# 3. web journey, report and PDF
# ==========================================================================
@pytest.fixture
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _web(c):
    sid = _web_project(c, names=("Driver board", "Plastic case", "Battery"))
    form = _icp_form(c, sid)
    ids = [o[0] for o in form["options"]]
    assert _icp_post(c, sid, form, ids).status_code in (200, 302)
    store = appmod._get_store()
    ifc = store.load_planar_clearance(sid)["interfaces"][0].interface_id
    return sid, ifc, ids


def _page(c, sid, ifc, lang=None):
    url = "/session/%s/interface-clearance/%s" % (sid, ifc)
    if lang:
        assert c.post("/ui-language", data={"lang": lang, "next": url}).status_code in (200, 302)
    return c.get(url)


def _fields(body, prefix="pcc_submission", form="data-pcc-form"):
    chunk = re.search(r"<form[^>]*%s>.*?</form>" % form, body, re.S).group(0)
    hidden = dict(re.findall(r'<input type="hidden" name="([^"]+)" value="([^"]*)"', chunk))
    hidden.pop("csrf_token", None)
    return {k: _html.unescape(v) for k, v in hidden.items()}


def _save(c, sid, ifc, ids, values=("84", "50", "86", "56", "2"), unknown=(), extra=None,
          answers=None, page=None):
    body = (page or _page(c, sid, ifc)).get_data(as_text=True)
    data = _fields(body)
    data.update({"board_component_id": ids[0], "enclosure_component_id": ids[1],
                 "region_description": "Inner floor between the four posts",
                 "basis_board": "Measured with calipers"})
    for role, value in zip(pcc.VALUE_ROLES, values):
        data["value_" + role] = value or ""
    for role in unknown:
        data["unknown_" + role] = "1"
    for d, a in zip(pcc.DECLARATION_IDS, answers or APPLIES):
        if a:
            data["decl_" + d] = a
    data.update(extra or {})
    return c.post("/session/%s/interface-clearance/%s" % (sid, ifc), data=data)


def _text(resp):
    return _html.unescape(re.sub(r"<[^>]+>", " ", resp.get_data(as_text=True)))


def _outcome(body):
    return re.findall(r'data-pcc-outcome="(\w+)"', body)


def _margin_cells(body):
    return re.findall(r"data-pcc-margin>([^<]*)<", body)


def _digests(body):
    return re.findall(r"data-pcc-digest>([0-9a-f]{16})<", body)


def _revisions(body):
    return re.findall(r"data-pcc-revision>(\d+)<", body)


def test_w01_the_end_to_end_journey_page_report_and_pdf_agree(client, monkeypatch):
    sid, ifc, ids = _web(client)
    prep = client.get("/session/%s/interface-preparation" % sid).get_data(as_text=True)
    assert "/interface-clearance/%s" % ifc in prep and "data-pcc-link" in prep
    first = _page(client, sid, ifc).get_data(as_text=True)
    assert "data-pcc-none" in first and 'checked' not in re.search(
        r"<form[^>]*data-pcc-form>.*?</form>", first, re.S).group(0)  # nothing pre-selected
    r = _save(client, sid, ifc, ids)
    body = r.get_data(as_text=True)
    assert r.status_code == 200 and "Saved." in body
    assert _outcome(body) == ["NOT_MET"] and _margin_cells(body) == ["-1 mm", "1 mm"]
    assert "not met: short by 1 mm" in " ".join(_text(r).split()) and "data-pcc-diagram" in body
    old_digest = _digests(body)[0]
    report_old = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert _outcome(report_old) == ["NOT_MET"] and _digests(report_old) == [old_digest]
    pdf_old = _pdf_source(client, sid, monkeypatch)
    assert _outcome(pdf_old) == ["NOT_MET"] and _digests(pdf_old) == [old_digest]
    r = _save(client, sid, ifc, ids, values=("84", "50", "90", "56", "2"))
    body = r.get_data(as_text=True)
    assert _outcome(body) == ["MET"] and _margin_cells(body) == ["1 mm", "1 mm"]
    new_digest = _digests(body)[0]
    assert new_digest != old_digest
    report_new = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert _outcome(report_new) == ["MET"] and _digests(report_new) == [new_digest]
    # the earlier render is a fixed, self-describing snapshot naming its own revision
    assert _revisions(report_old) == ["0"] and _revisions(report_new) == ["1"]
    assert "does not update" in _html.unescape(report_old)


def test_w02_unknown_input_saves_without_a_comparison(client):
    sid, ifc, ids = _web(client)
    r = _save(client, sid, ifc, ids, values=("84", "50", "86", "56", ""), unknown=("c",))
    body = r.get_data(as_text=True)
    assert _outcome(body) == ["MISSING_INFORMATION"] and _margin_cells(body) == []
    assert 'data-pcc-missing-item="c"' in body and "data-pcc-diagram" not in body
    store = appmod._get_store()
    assert store.load_planar_clearance(sid)["ledger"].active_for(ifc).current.values[4] == "unknown"
    r = _save(client, sid, ifc, ids, values=("84", "50", "86", "56", "3"), unknown=("c",))
    assert r.status_code == 400                                   # number AND unknown: refused


@pytest.mark.parametrize("bad", ["-1", "1e2", "0", "84.12345", "abc", "١2"])
def test_w03_inadmissible_values_are_refused_and_write_nothing(client, bad):
    sid, ifc, ids = _web(client)
    r = _save(client, sid, ifc, ids, values=(bad, "50", "86", "56", "2"))
    assert r.status_code == 400
    assert appmod._get_store().load_planar_clearance(sid)["ledger"].records == ()


def test_w04_retry_stale_and_withdraw(client):
    sid, ifc, ids = _web(client)
    page = _page(client, sid, ifc)
    r1 = _save(client, sid, ifc, ids, page=page)
    r2 = _save(client, sid, ifc, ids, page=page)                  # same signed submission
    assert "Saved." in r1.get_data(as_text=True) and "Saved." in r2.get_data(as_text=True)
    store = appmod._get_store()
    assert len(store.load_planar_clearance(sid)["ledger"].records[0].revisions) == 1
    stale_page = _page(client, sid, ifc)
    _save(client, sid, ifc, ids, values=("84", "50", "90", "56", "2"))
    r = _save(client, sid, ifc, ids, values=("84", "50", "91", "56", "2"), page=stale_page)
    assert r.status_code == 409 and "changed since this page was shown" in _html.unescape(
        r.get_data(as_text=True))
    body = _page(client, sid, ifc).get_data(as_text=True)
    data = _fields(body, form="data-pcc-withdraw-form")
    r = client.post("/session/%s/interface-clearance/%s/withdraw" % (sid, ifc), data=data)
    assert r.status_code == 400                                   # no confirmation
    data["withdraw_confirm"] = "yes"
    r = client.post("/session/%s/interface-clearance/%s/withdraw" % (sid, ifc), data=data)
    assert "Withdrawn." in r.get_data(as_text=True)
    r = client.post("/session/%s/interface-clearance/%s/withdraw" % (sid, ifc), data=data)
    assert "Withdrawn." in r.get_data(as_text=True)               # exact retry: no revival
    r = _save(client, sid, ifc, ids, page=page)                   # the first save, retried again
    assert "already recorded earlier" in r.get_data(as_text=True)
    ledger = store.load_planar_clearance(sid)["ledger"]
    assert ledger.active_for(ifc) is None and len(ledger.records[0].revisions) == 3
    assert "data-pcc-withdrawn-only" in _page(client, sid, ifc).get_data(as_text=True)


@pytest.mark.parametrize("recovers", [False, True])
@pytest.mark.parametrize("supersede", ["correction", "withdrawal"])
def test_w04b_an_old_retry_with_unreadable_currency_is_never_a_current_save(
        client, monkeypatch, supersede, recovers):
    """Acknowledgement currency: the committed lookup of an earlier submission
    succeeds, the current-state read then fails (persistently, or once and then
    recovers for the page render). The response says the submission was
    recorded and that its currency is unconfirmed - never a fresh / current save
    ("Saved."), never "not saved"."""
    sid, ifc, ids = _web(client)
    page = _page(client, sid, ifc)
    assert "Saved." in _save(client, sid, ifc, ids, page=page).get_data(as_text=True)
    if supersede == "correction":
        _save(client, sid, ifc, ids, values=("84", "50", "90", "56", "2"))
    else:
        data = _fields(_page(client, sid, ifc).get_data(as_text=True),
                       form="data-pcc-withdraw-form")
        data["withdraw_confirm"] = "yes"
        client.post("/session/%s/interface-clearance/%s/withdraw" % (sid, ifc), data=data)
    store_type = type(appmod._get_store())
    real = store_type.load_planar_clearance
    calls = []

    def failing(self, project_id):
        calls.append(project_id)
        if not recovers or len(calls) == 1:
            raise sqlite3.OperationalError("database is locked")
        return real(self, project_id)
    monkeypatch.setattr(store_type, "load_planar_clearance", failing)
    r = _save(client, sid, ifc, ids, page=page)              # the FIRST submission, retried
    body = _html.unescape(r.get_data(as_text=True))
    assert calls, "the currency read was attempted"
    assert "This submission was recorded." in body
    assert "cannot be confirmed right now" in body
    assert "Saved." not in body and "Not saved." not in body
    assert "already recorded earlier" not in body             # no currency was established
    if recovers:
        assert r.status_code == 200 and "data-pcc-unavailable" not in body   # current state renders
        assert ("data-pcc-identity" in body) == (supersede == "correction")
    else:
        assert r.status_code == 503 and "data-pcc-unavailable" in body
    monkeypatch.setattr(store_type, "load_planar_clearance", real)
    ledger = appmod._get_store().load_planar_clearance(sid)["ledger"]
    assert len(ledger.records) == 1 and len(ledger.records[0].revisions) == 2   # nothing written


def test_w05b_withdrawal_is_bound_to_the_pages_interaction(client):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids)
    store = appmod._get_store()
    subs = store.load_planar_clearance(sid)["subsystems"]
    other = sm.declared_interface(subs, subs[0].subsystem_id, subs[1].subsystem_id, "Second link")
    store.append_subsystem_interface(sid, other, "k-second")
    data = _fields(_page(client, sid, ifc).get_data(as_text=True), form="data-pcc-withdraw-form")
    data["withdraw_confirm"] = "yes"
    r = client.post("/session/%s/interface-clearance/%s/withdraw" % (sid, other.interface_id),
                    data=data)
    assert r.status_code == 409
    assert store.load_planar_clearance(sid)["ledger"].active_for(ifc) is not None


def test_w05_authorization_csrf_and_foreign_identities(client):
    sid, ifc, ids = _web(client)
    other_sid, other_ifc, other_ids = _web(client)
    r = _save(client, sid, ifc, [ids[0], other_ids[1]])
    assert r.status_code in (400, 409) and appmod._get_store().load_planar_clearance(
        sid)["ledger"].records == ()
    assert client.get("/session/%s/interface-clearance/%s" % (sid, other_ifc)).status_code == 302
    page = _page(client, sid, ifc).get_data(as_text=True)
    data = _fields(page)
    data.update({"board_component_id": ids[0], "enclosure_component_id": ids[1]})
    with appmod.app.test_client() as anonymous:                    # no project access, no token
        r = anonymous.post("/session/%s/interface-clearance/%s" % (sid, ifc), data=data)
        assert r.status_code in (302, 400, 403)
    assert appmod._get_store().load_planar_clearance(sid)["ledger"].records == ()


def test_w06_escaping_and_basis_disclosure(client, monkeypatch):
    sid, ifc, ids = _web(client)
    nasty = '<script>alert(1)</script> https://example.com/x'
    r = _save(client, sid, ifc, ids, extra={"region_description": nasty, "basis_region": nasty})
    for body in (r.get_data(as_text=True),
                 client.get("/session/%s/deliverable" % sid).get_data(as_text=True),
                 _pdf_source(client, sid, monkeypatch)):
        assert "<script>alert(1)</script>" not in body and "&lt;script&gt;" in body
        assert 'href="https://example.com' not in body               # a note is never a link
        assert "basis not recorded" in body                           # the clearance basis is absent


def _negations():
    """Every sentence of this journey that mentions fit, verification, safety or
    compatibility only to deny it (the governed disclosure and limitations and the
    fixed boundary copy)."""
    artifact = pcc.load_artifact()
    keys = ("UI_PCC_OWNER_STATED", "UI_PCC_BASIS_NOTE", "UI_PCC_NOT_MET_NOTE",
            "UI_PCC_DIAGRAM_NOTE", "UI_PCC_OUTCOME_INAPPLICABLE", "UI_PCC_INTRO")
    # BOARD-ENCLOSURE-CONDITIONAL-REGION-BOUND-01: the derived consequence's
    # governed meaning lines deny fit and verification in the same way.
    return (artifact["disclosure"] + artifact["limitations"]
            + artifact["region_bound"]["statements"]
            + [ui_text.text(k, "en") for k in keys])


def test_w07_prohibited_affirmative_claims_never_appear(client, monkeypatch):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids, values=("84", "50", "90", "56", "2"))
    page = _page(client, sid, ifc).get_data(as_text=True)
    report = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    chunks = [re.search(r"<div lang=\"en\" dir=\"ltr\" data-pcc-page>.*</div>", page, re.S).group(0),
              re.search(r"<section class=\"group\" data-pcc-report.*?</section>", report, re.S).group(0)]
    for raw in chunks:
        text = " ".join(_html.unescape(re.sub(r"<[^>]+>", " ", raw)).split())
        assert "This does not show that the parts fit" in text      # present, as a denial
        for sentence in _negations():
            text = text.replace(" ".join(sentence.split()), " ")
        found = re.findall(r"\b(fits?|compatible|compatibility|verified|verify|certified|safe|safety"
                           r"|manufacturable|ready)\b", text, re.I)
        assert found == [], found


def test_w08_the_report_reads_one_snapshot_per_render(client, monkeypatch):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids)
    calls = []
    real = type(appmod._get_store()).load_planar_clearance

    def counting(self, project_id):
        calls.append(project_id)
        return real(self, project_id)
    monkeypatch.setattr(type(appmod._get_store()), "load_planar_clearance", counting)
    client.get("/session/%s/deliverable" % sid)
    assert calls == [sid]


def test_w09_unreadable_reads_unavailable(client, monkeypatch):
    sid, ifc, ids = _web(client)
    _save(client, sid, ifc, ids)

    def broken(self, project_id):
        raise PlanarClearanceCorrupt("broken")
    monkeypatch.setattr(type(appmod._get_store()), "load_planar_clearance", broken)
    r = _page(client, sid, ifc)
    assert r.status_code == 503 and "data-pcc-unavailable" in r.get_data(as_text=True)
    report = client.get("/session/%s/deliverable" % sid).get_data(as_text=True)
    assert "data-pcc-report-unavailable" in report and "data-pcc-outcome" not in report


def test_w10_arabic_interface_renders_the_journey_in_arabic(client):
    """BOARD-ENCLOSURE-ARABIC-QUALIFICATION-01 replaces the former English-only
    notice: on the Arabic interface the journey itself is Arabic and RTL (its
    full qualification is pinned in test_board_enclosure_arabic_qualification)."""
    sid, ifc, ids = _web(client)
    body = _page(client, sid, ifc, lang="ar").get_data(as_text=True)
    assert 'lang="ar" dir="rtl" data-pcc-page' in body
    assert ui_text.text("UI_PCC_TITLE", "ar") in body
    assert "UI_PCC_ENGLISH_ONLY" not in body and not ui_text.has_string("UI_PCC_ENGLISH_ONLY")
    prep = client.get("/session/%s/interface-preparation" % sid)
    assert prep.status_code == 200 and ui_text.text("UI_PCC_LINK", "ar") in prep.get_data(as_text=True)


def _stable(body):
    body = re.sub(r'value="[^"]*"', "", body)
    return re.sub(r"\d{4}-\d\d-\d\d[T ]\d\d:\d\d:\d\d(?:\.\d+)?(?:Z|[+-]\d\d:\d\d)?", "", body)


def test_w11_protected_behaviour_session_ledger_and_export_unchanged(client):
    sid, ifc, ids = _web(client)
    client.get("/session/%s" % sid)                     # consumes the earlier one-shot notices
    session_before = _stable(client.get("/session/%s" % sid).get_data(as_text=True))
    store = appmod._get_store()
    ledger_before = store.load_records(sid) if hasattr(store, "load_records") else None
    export_before = client.get("/session/%s/disclosure-export.json" % sid)
    _save(client, sid, ifc, ids)
    _save(client, sid, ifc, ids, values=("84", "50", "90", "56", "2"))
    assert _stable(client.get("/session/%s" % sid).get_data(as_text=True)) == session_before
    if ledger_before is not None:
        assert store.load_records(sid) == ledger_before
    export_after = client.get("/session/%s/disclosure-export.json" % sid)
    assert export_after.status_code == export_before.status_code
    if export_before.status_code == 200:
        strip = lambda raw: re.sub(r'"generated_at":\s*"[^"]*"', "", raw)
        assert strip(export_after.get_data(as_text=True)) == strip(
            export_before.get_data(as_text=True))
