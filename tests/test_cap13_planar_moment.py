# -*- coding: utf-8 -*-
"""Stage 25 / CAP-13 - Planar Single-Force Moment, Slice 1 (directly owning tests).

The shared deterministic calculation / units owner (``engine/deterministic_calculation.py``)
after the bounded third admission of calc/units Correction 03 (§13B); the ONE
method ``cap13:planar_single_force_moment`` 1.0 (``engine/cap13_planar_moment_method.py``)
and its ONE consumer (``engine/cap13_planar_moment.py`` + the request-local page).

The numerical tests use an INDEPENDENT exact-rational reference: each binary64
input is decomposed with ``float.as_integer_ratio`` and the exact product is
formed from integers, never from the adapter's own arithmetic. Acceptance is a
relative error of at most 2^-52 against that exact product; subnormal results
are accepted when they meet the bound and are never refused merely for being
subnormal. The remaining tests press on the method contract (§§1-9A): the
closed three-method inventory and the exact N / mm / N·mm bindings; binding
isolation; owner artifact v3 and moment-artifact integrity; the §7 pre-owner
order and owner correspondence; the Mechanical-root gate (no integrated-part
eligibility); request integrity, isolation and no persistence; the two-support
and THERM-01 methods unchanged; and EN / AR fidelity. Synthetic data only.
"""
import copy
import html
import json
import math
import random
import re
import sys
from fractions import Fraction
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import cap13_planar_moment as moment
from engine import cap13_planar_moment_method as method
from engine import cap13_static_reactions_method as cap13_method
from engine import therm01_conduction_method as therm_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import _integrated
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_therm01_temperature_difference import _form as _therm_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "STAGE25_CAP13_PLANAR_SINGLE_FORCE_MOMENT_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
URL = "/session/%s/planar-moment"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
CAP13_BINDING = dc.bind_method(cap13_method.METHOD_ID, cap13_method.METHOD_VERSION,
                               cap13_method.evaluate)
THERM_BINDING = dc.bind_method(therm_method.METHOD_ID, therm_method.METHOD_VERSION,
                               therm_method.evaluate)
BOUND = Fraction(1, 2 ** 52)
TINY = 5e-324                         # 2^-1074, the smallest positive subnormal
SMALLEST_NORMAL = sys.float_info.min  # 2^-1022


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _exact(value):
    """The exact rational value of a binary64 float, from its integer ratio."""
    numerator, denominator = float(value).as_integer_ratio()
    return Fraction(numerator, denominator)


def _exact_product(a, b):
    return _exact(a) * _exact(b)


def _within_bound(produced, a, b):
    exact = _exact_product(a, b)
    return abs(_exact(produced) - exact) <= exact * BOUND


def _request(F=12.5, d_perp=80.0, units=("N", "mm"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"F": {"value": F, "unit": units[0]},
                      "d_perp": {"value": d_perp, "unit": units[1]}},
           "subject_ref": None}
    req.update(over)
    return req


def _run(F, d_perp):
    return dc.execute(BINDING, _request(F=F, d_perp=d_perp))


def _form(F="12.5", d_perp="80", decl=None, screen=None):
    form = {moment.DECLARATION_FIELD % d: moment.ANSWER_APPLIES
            for d in moment.DECLARATION_IDS}
    form.update({moment.SCREEN_FIELD % s: moment.SCREEN_NO for s in moment.SCREEN_ITEMS})
    form.update({moment.VALUE_FIELD % "F": F, moment.VALUE_FIELD % "d_perp": d_perp})
    for key, value in (decl or {}).items():
        form[moment.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[moment.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = moment.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return moment.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _moment_artifact():
    return json.loads(moment.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data, name="a.json"):
    target = tmp_path / name
    target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return target


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def _failure(result):
    return (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


@pytest.fixture
def mech():
    c, aid = _client_for("cap13m-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": "mechanical"})


@pytest.fixture
def elec():
    c, aid = _client_for("cap13m-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


# ==========================================================================
# 1. numerical acceptance against an independent exact-rational reference
# ==========================================================================
@pytest.mark.parametrize("F,d_perp", [
    (12.5, 80.0), (1.0, 1.0), (0.1, 0.2), (3.0, 1.0 / 3.0), (1e-3, 1e3),
    (123456.789, 0.000321), (2.0 ** 52 + 1.0, 3.0), (math.pi, math.e),
    (1e150, 1e150), (1e-150, 1e-150), (sys.float_info.max, 1.0),
    (sys.float_info.max / 2.0, 2.0), (1.0, SMALLEST_NORMAL),
])
def test_normal_and_boundary_products_meet_the_bound(F, d_perp):
    result = _run(F, d_perp)
    assert result["state"] == dc.STATE_SUCCESS
    produced = result["outputs"]["M"]["value"]
    assert isinstance(produced, float) and math.isfinite(produced) and produced > 0
    assert _within_bound(produced, F, d_perp)
    # and it is exactly the correctly rounded product of the exact reference
    assert produced == float(_exact_product(F, d_perp))
    assert result["outputs"]["M"]["unit"] == "N·mm"
    assert result["validation_status"] == "UNVALIDATED"


def test_random_normal_products_are_correctly_rounded_and_within_bound():
    rng = random.Random(20261024)
    for _ in range(2000):
        F = rng.uniform(1e-6, 1e6) * 10.0 ** rng.randint(-100, 100)
        d_perp = rng.uniform(1e-6, 1e6) * 10.0 ** rng.randint(-100, 100)
        result = _run(F, d_perp)
        assert result["state"] == dc.STATE_SUCCESS, (F, d_perp)
        produced = result["outputs"]["M"]["value"]
        assert produced == float(_exact_product(F, d_perp))
        assert _within_bound(produced, F, d_perp)


def test_overflow_is_an_integrity_failure_with_no_payload():
    for F, d_perp in ((1e200, 1e200), (sys.float_info.max, 2.0),
                      (sys.float_info.max, 1.0 + 2.0 ** -52)):
        assert math.isinf(F * d_perp)
        assert _failure(_run(F, d_perp)), (F, d_perp)
    with pytest.raises(ArithmeticError):
        method.evaluate(1e200, 1e200)


def test_underflow_to_zero_is_an_integrity_failure_not_a_refusal():
    for F, d_perp in ((1e-200, 1e-200), (TINY, 0.25), (TINY, 0.5),
                      (SMALLEST_NORMAL, 2.0 ** -60)):
        assert F > 0 and d_perp > 0 and F * d_perp == 0.0
        result = _run(F, d_perp)
        assert _failure(result), (F, d_perp)
        assert result["state"] != dc.STATE_REFUSAL
    with pytest.raises(ArithmeticError):
        method.evaluate(1e-200, 1e-200)


@pytest.mark.parametrize("F,d_perp", [
    (TINY, 1.0), (TINY, 2.0), (TINY * 3, 7.0), (SMALLEST_NORMAL, 0.5),
    (SMALLEST_NORMAL, 0.25), (2.0 ** -1000, 2.0 ** -60), (SMALLEST_NORMAL * 0.75, 1.0),
])
def test_exact_subnormal_results_are_accepted(F, d_perp):
    exact = _exact_product(F, d_perp)
    assert exact < _exact(SMALLEST_NORMAL)                 # a subnormal result
    assert _exact(float(exact)) == exact                   # exactly representable
    result = _run(F, d_perp)
    assert result["state"] == dc.STATE_SUCCESS
    assert _exact(result["outputs"]["M"]["value"]) == exact


def test_inexact_subnormal_within_the_bound_is_accepted():
    # 0.75 * 2^-1022 * (1 + 2^-52): the exact product needs 0.75 units in the last
    # subnormal place more, so it rounds; the relative error is (1/3) * 2^-52.
    F, d_perp = SMALLEST_NORMAL * 0.75, 1.0 + 2.0 ** -52
    exact = _exact_product(F, d_perp)
    assert exact < _exact(SMALLEST_NORMAL)
    assert _exact(float(exact)) != exact                   # NOT exact
    result = _run(F, d_perp)
    assert result["state"] == dc.STATE_SUCCESS
    produced = result["outputs"]["M"]["value"]
    assert produced < SMALLEST_NORMAL                      # still subnormal
    assert _within_bound(produced, F, d_perp)
    # the rounding error is exactly a quarter of the smallest subnormal step
    assert abs(_exact(produced) - exact) == Fraction(1, 4) * _exact(TINY)


@pytest.mark.parametrize("F,d_perp", [
    (TINY, 1.5), (TINY * 3, 0.5), (TINY, 3.75), (2.0 ** -1070, 0.3),
])
def test_inexact_subnormal_beyond_the_bound_is_refused(F, d_perp):
    produced = F * d_perp
    assert 0.0 < produced < SMALLEST_NORMAL
    assert not _within_bound(produced, F, d_perp)
    assert _failure(_run(F, d_perp))
    with pytest.raises(ArithmeticError):
        method.evaluate(F, d_perp)


def test_zero_input_is_refused_before_execution_unlike_underflow(monkeypatch):
    calls = []
    real = method.evaluate
    # the owner's governed applicability (> 0) refuses a zero input before the
    # adapter runs; an underflow (above) is an integrity FAILURE instead
    for F, d_perp in ((0.0, 80.0), (12.5, 0.0), (0.0, 0.0), (-0.0, 5.0)):
        result = dc.execute(BINDING, _request(F=F, d_perp=d_perp))
        assert (result["state"], result["reason"], result["outputs"]) == (
            dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None), (F, d_perp)
    # the consumer refuses a typed zero as INVALID_NUMERIC_INPUT, owner never called
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    for over in ({"F": "0"}, {"d_perp": "0.0"}, {"F": "000"}):
        assert _evaluate(**over)["outcome"] == moment.INVALID_NUMERIC_INPUT
    assert not calls
    # the adapter itself never computes a zero input
    for bad in ((0.0, 1.0), (1.0, 0.0), (-1.0, 1.0)):
        with pytest.raises(ArithmeticError):
            real(*bad)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"),
                                   True, False, "12", None, [1.0]])
def test_non_finite_and_non_numeric_inputs_are_refused(value):
    result = dc.execute(BINDING, _request(F=value))
    assert result["state"] in (dc.STATE_REFUSAL, dc.STATE_UNABLE)
    assert result["outputs"] is None
    assert result["reason"] in (dc.INVALID_NUMERIC_INPUT, dc.INPUT_MISSING)


def test_adapter_refuses_non_float_or_non_finite_arguments():
    for bad in ((1, 2.0), (2.0, 1), (float("nan"), 1.0), (1.0, float("inf")),
                ("1", 1.0)):
        with pytest.raises(ArithmeticError):
            method.evaluate(*bad)


# ==========================================================================
# 2. the owner: inventory, bindings, units, identity (Correction 03)
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["state"] == dc.STATE_SUCCESS and result["reason"] is None
    assert result["outputs"] == {"M": {"value": 1000.0, "unit": "N·mm",
                                       "provenance": "CALCULATED"}}
    assert result["inputs"]["F"] == {"value": 12.5, "unit": "N",
                                     "provenance": "OWNER_STATED"}
    assert (result["method_id"], result["method_version"]) == (
        "cap13:planar_single_force_moment", "1.0")
    assert (result["artifact_version"], result["implementation_version"]) == ("6", "1.5.0")
    assert [u["record_id"] for u in result["unit_records"]] == [
        "dcu:U001", "dcu:U002", "dcu:U006"]
    assert [q["source_ref"] for q in result["source_qualification"]] == [
        "NASA-S1", "NASA-T1"]
    assert {q["source_use_policy_ref"] for q in result["source_qualification"]} \
        == {"dcu:SU005"}
    assert result["subject_ref"] == "opaque"
    assert re.fullmatch(r"[0-9a-f]{64}", result["result_identity"])
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_and_versions():
    assert ("cap13:planar_single_force_moment", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 6
    assert "moment" in dc.ADMITTED_QUANTITY_KINDS
    assert "N·mm" in dc.ADMITTED_UNIT_TOKENS
    assert dc.IMPLEMENTATION_VERSION == "1.5.0"
    data = dc.load_artifact()
    assert data["artifact_version"] == "6"
    record = _record(data)
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"]] == [("F", "force", "N"),
                                                ("d_perp", "length", "mm")]
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["output_roles"]] == [("M", "moment", "N·mm")]
    assert record["adapter_identity"] == "engine.cap13_planar_moment_method.evaluate"
    assert record["method_authority_artifact"] == {
        "artifact_id": moment.ARTIFACT_ID, "artifact_version": "1"}
    units = {u["unit_token"]: u for u in data["unit_records"]}
    assert units["N·mm"]["record_id"] == "dcu:U006"
    assert units["N·mm"]["source_use_policy_ref"] == "dcu:SU006"
    assert "no conversion" in units["N·mm"]["inspected_content"]


def test_units_are_exact_with_no_alias_or_conversion():
    for unit in ("N*mm", "Nmm", "n·mm", "N mm", "kN", "N.mm"):
        result = dc.execute(BINDING, _request(units=(unit, "mm")))
        assert result["reason"] == dc.UNKNOWN_UNIT, unit
    assert dc.execute(BINDING, _request(units=("N", "N")))["reason"] \
        == dc.UNIT_NOT_ADMITTED
    assert dc.execute(BINDING, _request(units=("N·mm", "mm")))["reason"] \
        == dc.UNIT_NOT_ADMITTED
    assert dc.execute(BINDING, _request(units=("W", "mm")))["reason"] \
        == dc.UNIT_NOT_ADMITTED
    # N·m is admitted for the rotational load's torque (Correction 04) and is
    # still never accepted, converted or aliased for this method's roles
    for units in (("N·m", "mm"), ("N", "rad/s")):
        assert dc.execute(BINDING, _request(units=units))["reason"] \
            == dc.UNIT_NOT_ADMITTED


def test_method_version_and_adapter_integrity_fail_closed():
    assert dc.execute(BINDING, _request(method_version="1.1"))["reason"] \
        == dc.VERSION_MISMATCH
    stale = dc.bind_method(method.METHOD_ID, "0.9", method.evaluate)
    assert dc.execute(stale, _request())["reason"] == dc.VERSION_MISMATCH
    for adapter in (cap13_method.evaluate, therm_method.evaluate,
                    lambda F, d_perp: {"M": F * d_perp}):
        swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, adapter)
        assert _failure(dc.execute(swapped, _request()))
    req = _request()
    del req["inputs"]["d_perp"]
    assert dc.execute(BINDING, req)["reason"] == dc.INPUT_MISSING
    req = _request()
    req["inputs"]["x"] = {"value": 1.0, "unit": "mm"}
    assert dc.execute(BINDING, req)["reason"] == dc.OPERATION_NOT_ADMITTED
    unknown = dc.bind_method("cap13:planar_two_force_moment", "1.0", method.evaluate)
    assert dc.execute(unknown, _request(method_id="cap13:planar_two_force_moment")
                      )["reason"] == dc.METHOD_NOT_REGISTERED


def test_all_three_bindings_are_isolated_from_each_other():
    cap13_req = {"method_id": cap13_method.METHOD_ID, "method_version": "1.0",
                 "inputs": {"P": {"value": 1000.0, "unit": "N"},
                            "L": {"value": 2000.0, "unit": "mm"},
                            "x": {"value": 500.0, "unit": "mm"}},
                 "subject_ref": None}
    therm_req = {"method_id": therm_method.METHOD_ID, "method_version": "1.0",
                 "inputs": {"P": {"value": 10.0, "unit": "W"},
                            "R_theta": {"value": 2.5, "unit": "K/W"}},
                 "subject_ref": None}
    for binding, req in ((BINDING, cap13_req), (BINDING, therm_req),
                         (CAP13_BINDING, _request()), (THERM_BINDING, _request())):
        assert dc.execute(binding, req)["reason"] == dc.OPERATION_NOT_ADMITTED
    # and the existing methods still produce exactly their established values
    cap13 = dc.execute(CAP13_BINDING, cap13_req)
    assert (cap13["outputs"]["R_L"]["value"], cap13["outputs"]["R_R"]["value"]) \
        == (750.0, 250.0)
    assert dc.execute(THERM_BINDING, therm_req)["outputs"]["delta_T"]["value"] == 25.0


def test_app_wires_one_immutable_moment_binding():
    assert webapp._CAP13_MOMENT_BINDING.adapter_identity \
        == "engine.cap13_planar_moment_method.evaluate"
    assert webapp._CAP13_MOMENT_BINDING.method_id == method.METHOD_ID
    with pytest.raises(AttributeError):
        webapp._CAP13_MOMENT_BINDING.method_id = "x"
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    assert app_source.count("_dcalc.bind_method(") == 6
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    assert "cap13_planar_moment" not in owner_source
    assert "cap13_content_config" not in owner_source


# ==========================================================================
# 3. owner artifact v3 and the moment artifact: integrity and tamper
# ==========================================================================
def _owner_tamper(data, name):
    record = _record(data)
    if name == "second_moment_unit":
        extra = copy.deepcopy([u for u in data["unit_records"]
                               if u["unit_token"] == "N·mm"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U007", "N·m"
        data["unit_records"].append(extra)
    elif name == "drop_moment_unit":
        data["unit_records"] = [u for u in data["unit_records"]
                                if u["unit_token"] != "N·mm"]
    elif name == "drop_moment_kind":
        data["quantity_kinds"] = [k for k in data["quantity_kinds"]
                                  if k["quantity_kind"] != "moment"]
    elif name == "drop_method":
        data["methods"].remove(record)
    elif name == "extra_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "cap13:planar_two_force_moment"
        data["methods"].append(extra)
    elif name == "output_unit":
        record["output_roles"][0]["unit_token"] = "mm"
    elif name == "policy_unresolved":
        record["source_qualification"][0]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "basis":
        record["source_qualification"][1]["inspection_basis"] = "EXECUTOR"
    elif name == "adapter":
        record["adapter_identity"] = "engine.cap13_static_reactions_method.evaluate"
    return data


@pytest.mark.parametrize("name", [
    "second_moment_unit", "drop_moment_unit", "drop_moment_kind", "drop_method",
    "extra_method", "output_unit", "policy_unresolved", "basis", "adapter"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), name))
    result = dc.execute(BINDING, _request(), artifact_path=path)
    assert result["outputs"] is None
    assert result["state"] in (dc.STATE_FAILURE, dc.STATE_REFUSAL)
    if name != "drop_method" and name != "adapter":
        with pytest.raises(dc.CalculationArtifactError):
            dc.load_artifact(path)


def test_owner_artifact_unreadable_is_source_unavailable(tmp_path):
    result = dc.execute(BINDING, _request(), artifact_path=tmp_path / "missing.json")
    assert (result["state"], result["reason"]) == (dc.STATE_UNABLE,
                                                   dc.SOURCE_UNAVAILABLE)


def test_owner_v2_records_are_unchanged_by_the_third_admission():
    data = dc.load_artifact()
    units = {u["record_id"]: u for u in data["unit_records"]}
    assert [units[r]["unit_token"] for r in ("dcu:U001", "dcu:U002", "dcu:U003",
                                             "dcu:U004", "dcu:U005")] \
        == ["N", "mm", "W", "K/W", "K"]
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "dcu:U001 and dcu:U002 only" in policies["dcu:SU001"]["inspection_reference"]
    assert "NASA-S1 and NASA-S2 only" in policies["dcu:SU002"]["inspected_content"]
    assert "NASA-S1 and NASA-T1 only" in policies["dcu:SU005"]["inspected_content"]
    assert "dcu:U006 only" in policies["dcu:SU006"]["inspected_content"]
    reactions = _record(data, cap13_method.METHOD_ID)
    assert [q["source_use_policy_ref"] for q in reactions["source_qualification"]] \
        == ["dcu:SU002", "dcu:SU002"]
    assert reactions["method_authority_artifact"]["artifact_version"] == "1"


def test_moment_artifact_loads_and_binds_its_sources():
    data = moment.load_artifact()
    assert data["method"]["method_id"] == method.METHOD_ID
    assert [d["declaration_id"] for d in data["declarations"]] == list(
        moment.DECLARATION_IDS)
    assert [i["item_id"] for i in data["screen_items"]] == list(moment.SCREEN_ITEMS)
    by_id = {r["record_id"]: r for r in data["sources"]}
    assert by_id["NASA-S1"]["source_use_policy_ref"] == "cap13m:SU001"
    assert by_id["NASA-T1"]["source_use_policy_ref"] == "cap13m:SU001"
    assert by_id["NIST-U"]["source_use_policy_ref"] == "cap13m:SU002"
    assert all(r["inspection_basis"] == "LEAD_SUPPLIED" for r in data["sources"])
    assert len(data["disclosure"]) == 7
    # the same nine screen items as the two-support artifact
    from engine import cap13_static_reactions as reactions
    assert moment.SCREEN_ITEMS == reactions.SCREEN_ITEMS


@pytest.mark.parametrize("mutate", [
    lambda d: d["declarations"][2].__setitem__(
        "accepted_value", "the distance d_perp may be measured along the lever"),
    lambda d: d["declarations"][0].__setitem__("refusal", "NOT_DECLARED"),
    lambda d: d["numeric_domain"]["roles"][2].__setitem__("unit_token", "N·m"),
    lambda d: d["disclosure"].pop(),
    lambda d: d["limitations"].__setitem__(0, "Static equilibrium is checked."),
    lambda d: d["sources"][0].__setitem__("source_use_policy_ref", "cap13:SU001"),
    lambda d: d["method"].__setitem__("executed_form", "M = F * d_perp * 1000"),
    lambda d: d.__setitem__("artifact_version", "2"),
    lambda d: d["screen_items"].pop(),
])
def test_moment_artifact_tamper_is_knowledge_unavailable(tmp_path, mutate, monkeypatch):
    data = _moment_artifact()
    mutate(data)
    with pytest.raises(moment.MomentKnowledgeError):
        moment.validate_artifact(data)
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    result = moment.evaluate(_captured(), BINDING, artifact=data)
    assert result["outcome"] == moment.KNOWLEDGE_UNAVAILABLE and not calls


# ==========================================================================
# 4. the consumer: capture, the §7 order and owner correspondence
# ==========================================================================
def test_consumer_success_carries_the_owner_result():
    result = _evaluate()
    assert result["outcome"] == moment.OUTCOME_SUCCESS
    assert result["owner_state"] == dc.STATE_SUCCESS
    assert result["result"]["outputs"]["M"]["value"] == 1000.0
    assert moment.format_value(result["result"]["outputs"]["M"]["value"]) == "1000.0"


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    # an unanswered item wins over a YES, a non-applying declaration and a bad number
    assert _evaluate(decl={"planar": ""}, screen={"pressure": "yes"},
                     F="abc")["outcome"] == moment.NOT_DECLARED
    assert _evaluate(screen={"pressure": ""})["outcome"] == moment.NOT_DECLARED
    # a screen YES wins over a non-applying declaration and a bad number
    assert _evaluate(screen={"children": "yes"}, decl={"single_force": "does_not_apply"},
                     F="-1")["outcome"] == moment.ENGINEERING_REVIEW_REQUIRED
    # a non-applying declaration wins over a bad number
    for decl in moment.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"}, F="x")["outcome"] \
            == moment.MODEL_NOT_SUPPORTED, decl
    assert not calls


@pytest.mark.parametrize("text", [
    "", "-1", "+1", "1e3", "1E3", "1,5", "1_0", " 1", "1 ", ".5", "5.", "0x10",
    "inf", "nan", "١٢", "12N", "1." + "0" * 64, "0", "0.0"])
def test_numeric_grammar_and_zero_are_invalid(text, monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(F=text)["outcome"] == moment.INVALID_NUMERIC_INPUT, text
    assert _evaluate(d_perp=text)["outcome"] == moment.INVALID_NUMERIC_INPUT, text
    assert not calls


def test_numeric_grammar_accepts_plain_decimals():
    assert moment.parse_number("80") == 80.0
    assert moment.parse_number("0.000001") == 1e-6
    assert moment.parse_number("9" * 64) == float("9" * 64)
    assert moment.parse_number("9" * 65) is None


@pytest.mark.parametrize("form", [
    {"unexpected": ["1"]},
    {moment.VALUE_FIELD % "F": ["1", "2"]},
    {moment.DECLARATION_FIELD % "planar": ["yes"]},
    {moment.SCREEN_FIELD % "children": ["maybe"]},
    {moment.VALUE_FIELD % "F": [1.0]},
])
def test_malformed_capture_is_none(form):
    base = {k: [v] for k, v in _form().items()}
    base.update(form)
    assert moment.capture_form(base) is None
    assert moment.capture_form("not a mapping") is None


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, moment.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, moment.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, moment.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, moment.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, moment.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, moment.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, moment.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, moment.UNMAPPED_OWNER_OUTCOME),
    (dc.STATE_REFUSAL, dc.OPERATION_NOT_ADMITTED, moment.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome,
                                                        monkeypatch):
    monkeypatch.setattr(dc, "execute", lambda *a, **k: {
        "state": state, "reason": reason, "outputs": None})
    result = _evaluate()
    assert result["outcome"] == outcome
    assert (result["owner_state"], result["owner_reason"]) == (state, reason)
    assert result["result"] is None


def test_owner_failure_from_a_tampered_owner_artifact_is_never_a_refusal(tmp_path):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), "output_unit"))
    result = moment.evaluate(_captured(), BINDING, owner_artifact_path=path)
    assert result["outcome"] == moment.KNOWLEDGE_UNAVAILABLE
    assert result["owner_state"] == dc.STATE_FAILURE


def test_consumer_typed_values_and_fixed_units_reach_the_owner(monkeypatch):
    seen = []
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: (
        seen.append(copy.deepcopy(r)), real(b, r, artifact_path=artifact_path))[1])
    _evaluate(F="2.5", d_perp="4")
    assert seen == [{"method_id": method.METHOD_ID, "method_version": "1.0",
                     "inputs": {"F": {"value": 2.5, "unit": "N"},
                                "d_perp": {"value": 4.0, "unit": "mm"}},
                     "subject_ref": None}]


def test_consumer_imports_no_other_method_authority():
    import ast
    for module in (moment, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module or "")
                imports.update("%s.%s" % (node.module, a.name) for a in node.names)
        for banned in ("cap13_static_reactions", "therm01", "record_store",
                       "safety_signal", "idea_state", "requests", "urllib", "openai"):
            assert not any(banned in name for name in imports), (module, banned)


# ==========================================================================
# 5. EN / AR fidelity
# ==========================================================================
def test_english_wording_equals_the_artifact():
    content = moment.load_artifact()
    assert ui_text.text("UI_CAP13M_DISCLOSURE", "en").split("\n\n") \
        == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"].replace("d_perp", "d⊥")
        assert ui_text.text("UI_CAP13M_DECL_" + entry["declaration_id"].upper(),
                            "en") == value[0].upper() + value[1:] + "."
    for entry in content["screen_items"]:
        assert ui_text.text("UI_CAP13_SCREEN_" + entry["item_id"].upper(), "en") \
            == entry["item"][0].upper() + entry["item"][1:]


def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_arabic_and_english_wording_equal_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    items = [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    assert ui_text.text("UI_CAP13M_DISCLOSURE", "ar").split("\n\n") == items
    a2 = _contract_section("**A-2", "**A-3")
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$", a2, re.M))
    for decl, ref in zip(moment.DECLARATION_IDS, ("D-1", "D-2", "D-3", "D-4", "D-5")):
        assert ui_text.text("UI_CAP13M_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    s9 = _contract_section("## 9. Result", "## 9A.")
    english = [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)]
    assert english == moment.load_artifact()["disclosure"]
    s5 = _contract_section("## 5. Applicability", "## 6.")
    for entry in moment.load_artifact()["declarations"]:
        assert "| %s | `%s` | %s |" % (entry["contract_ref"], entry["declaration_id"],
                                       entry["accepted_value"]) in s5


def test_every_moment_key_has_both_languages_and_no_overclaim():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_CAP13M_")] \
        if hasattr(ui_text, "UI_STRINGS") else None
    if keys is None:
        source = Path(ui_text.__file__).read_text(encoding="utf-8")
        keys = re.findall(r'"(UI_CAP13M_[A-Z_]+)": \{', source)
    assert len(keys) >= 30
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("is safe.", "is adequate.", "has been validated", "verified design",
                  "certified", "will not fail"):
        assert claim not in english, claim


def test_correction_03_is_recorded_in_the_calc_contract():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 03" in body and "## 13B." in body
    section = body[body.index("## 13B."):body.index("## 14.")]
    for phrase in ("exactly three", "`moment`", "`N·mm`", "content version `3`",
                   "`1.2.0`", "2^-52", "NOT a generic owner numerical policy"):
        assert phrase in section, phrase
    # §13A is unchanged
    assert "**Methods — exactly two:**" in body[body.index("## 13A."):body.index("## 13B.")]


# ==========================================================================
# 6. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_session_link_and_page_on_a_mechanical_root_project(mech):
    c, _aid, sid = mech
    page = _page(c, sid)
    assert "data-cap13m-link" in page and URL % sid in page
    r = c.get(URL % sid)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    body = r.get_data(as_text=True)
    assert "data-cap13m-form" in body and "checked" not in body
    for role in ("F", "d_perp"):
        assert re.search(r'name="value_%s"[^>]*maxlength="64"[^>]*value=""' % role, body)
    assert "data-cap13m-result" not in body and "data-cap13m-outcome" not in body


def test_post_success_renders_in_the_same_request(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(F="12.5", d_perp="80"))
    assert r.status_code == 200 and "Location" not in r.headers
    body = r.get_data(as_text=True)
    assert re.findall(r'data-cap13m-result-value><bdi dir="ltr">([^<]+)</bdi>',
                      body) == ["1000.0 N·mm"]
    assert "cap13:planar_single_force_moment" in body and "UNVALIDATED" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_CAP13M_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert re.findall(r'data-cap13m-echo-value>([^<]*)<', body) == ["12.5", "80"]
    assert "Torque (Moment)" in body and "Appendix B.9" in body


@pytest.mark.parametrize("over,outcome", [
    ({"d_perp": "0"}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"supports_people": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"perpendicular_distance": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"planar": ""}}, "NOT_DECLARED"),
])
def test_post_non_success_shows_one_reason_and_no_number(mech, over, outcome):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(**over))
    body = r.get_data(as_text=True)
    assert r.status_code == 200
    assert html.escape(ui_text.text("UI_CAP13M_OUTCOME_" + outcome, "en"),
                       quote=False) in body
    assert "data-cap13m-result" not in body and body.count("data-cap13m-outcome") == 1


def test_malformed_request_is_400_and_echo_is_escaped(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=dict(_form(), unexpected="1"))
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert ui_text.text("UI_CAP13M_ERR_REQUEST", "en") in body
    assert "data-cap13m-outcome" not in body and "data-cap13m-result" not in body
    body = c.post(URL % sid, data=_form(F="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body


def test_electronics_root_project_is_never_offered_or_evaluated(elec, monkeypatch):
    c, _aid, sid = elec
    assert "data-cap13m-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._cap13m, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-cap13m-scope-note" in body
        assert "data-cap13m-form" not in body and "data-cap13m-outcome" not in body
    assert not called


def test_integrated_part_is_offered_the_moment_with_attribution():
    # CAP13-PLANAR-MOMENT-INTEGRATED-PART-01: an Electrical / Electronics-focus
    # integrated project is offered the moment for its declared Mechanical part,
    # as it is the two-support reactions (the full gate matrix is in
    # tests/test_cap13_planar_moment_integrated_part.py)
    client, _aid = _client_for("cap13m-integrated@example.com")
    sid = _integrated(client, "electronics_electrical")
    page = _page(client, sid)
    assert "data-cap13-link" in page and "data-cap13m-link" in page
    body = client.post(URL % sid, data=_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">1000.0 N·mm</bdi>' in body
    assert "data-cap13m-part-name>Hinge arm<" in body


def test_csrf_and_authorization_are_enforced(mech):
    _c, _aid, sid = mech
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("cap13m-other@example.com")
    for client in (other, _new_client()):
        for response in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert response.status_code == 302
            assert "data-cap13m" not in response.get_data(as_text=True)


@pytest.mark.parametrize("over", [{}, {"F": "-3"}, {"d_perp": "abc"},
                                  {"screen": {"children": "yes"}}])
def test_nothing_is_persisted_and_no_project_state_moves(mech, over):
    c, _aid, sid = mech
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_no_safety_signal_report_export_or_api_surface():
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    start = app_source.index("# Stage 25 / CAP-13 — Planar Single-Force Moment")
    section = app_source[start:app_source.index("# Stage 27 / THERM-01", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "load_project_subsystems"):
        assert banned not in section, banned
    routes = [r.rule for r in webapp.app.url_map.iter_rules() if "planar-moment" in r.rule]
    assert routes == ["/session/<sid>/planar-moment"] * 2
    for template in ("deliverable.html", "report.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "cap13m" not in path.read_text(encoding="utf-8")


def test_existing_calculations_still_render_their_values(mech, elec):
    c, _aid, sid = mech
    body = c.post("/session/%s/support-reactions" % sid,
                  data=_cap13_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">750.0 N</bdi>' in body and '<bdi dir="ltr">250.0 N</bdi>' in body
    c2, _aid2, sid2 = elec
    body = c2.post("/session/%s/temperature-difference" % sid2,
                   data=_therm_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">25.0 K</bdi>' in body


def test_arabic_page_is_rtl_and_isolates_tokens(mech):
    c, _aid, sid = mech
    c.post("/ui-language", data={"lang": "ar"})
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert 'dir="rtl"' in body
    for token in ("F", "d⊥", "M", "N", "mm", "N·mm", "UNVALIDATED", "NOT EVIDENCE"):
        assert '(<bdi dir="ltr">%s</bdi>)' % html.escape(token) in body, token
    assert '<bdi dir="ltr">cap13:planar_single_force_moment</bdi>' in body
    assert '<bdi dir="ltr">1000.0 N·mm</bdi>' in body
    stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
    for item in ui_text.text("UI_CAP13M_DISCLOSURE", "ar").split("\n\n"):
        assert _norm(item) in _norm(stripped), item[:40]
