# -*- coding: utf-8 -*-
"""Stage 25 / CAP-13 - Linear Speed-Dependent Rotational Load, Slice 1 (directly owning tests).

ROTATIONAL-LOAD-SLICE-01. The shared deterministic calculation / units owner after
the bounded fourth admission of calc/units Correction 04 (§13C); the ONE method
``cap13:linear_speed_dependent_rotational_load`` 1.0
(``engine/cap13_rotational_load_method.py``) and its ONE consumer
(``engine/cap13_rotational_load.py`` + the request-local page).

Scientific reference: Modelica Standard Library v4.1.0,
LinearSpeedDependentTorque with TorqueDirection=false:
tau = tau_nominal * (w / w_nominal), tau = -flange.tau (accelerating torque).
The numerical tests use an INDEPENDENT exact-rational reference: each binary64
input is decomposed with ``float.as_integer_ratio`` and the exact result is
formed from integers, never from the adapter's own arithmetic. Synthetic data.
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
from engine import cap13_rotational_load as rload
from engine import cap13_rotational_load_method as method
from engine import cap13_static_reactions_method as cap13_method
from engine import cap13_planar_moment_method as moment_method
from engine import therm01_conduction_method as therm_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _corrupt, _owner_spy, _part_line, MECH, ELEC, PARTS, HOSTILE)
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_therm01_temperature_difference import _form as _therm_form
from tests.test_cap13_planar_moment import _form as _moment_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "STAGE25_CAP13_LINEAR_SPEED_DEPENDENT_ROTATIONAL_LOAD_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
UPSTREAM = ("https://github.com/modelica/ModelicaStandardLibrary/blob/v4.1.0/"
            "Modelica/Mechanics/Rotational/Sources/LinearSpeedDependentTorque.mo")
URL = "/session/%s/rotational-load"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
OTHER_BINDINGS = (
    dc.bind_method(cap13_method.METHOD_ID, "1.0", cap13_method.evaluate),
    dc.bind_method(therm_method.METHOD_ID, "1.0", therm_method.evaluate),
    dc.bind_method(moment_method.METHOD_ID, "1.0", moment_method.evaluate))
BOUND = Fraction(1, 2 ** 52)
TINY = 5e-324
SMALLEST_NORMAL = sys.float_info.min
REFERENCE_PAIRS = ((-10.0, 2.0), (-5.0, 1.0), (0.0, 0.0), (5.0, -1.0), (10.0, -2.0))


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _exact(value):
    numerator, denominator = float(value).as_integer_ratio()
    return Fraction(numerator, denominator)


def _exact_tau(tau_nominal, w_nominal, w):
    return _exact(tau_nominal) * _exact(w) / _exact(w_nominal)


def _request(tau_nominal=-2.0, w_nominal=10.0, w=5.0,
             units=("N·m", "rad/s", "rad/s"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"tau_nominal": {"value": tau_nominal, "unit": units[0]},
                      "w_nominal": {"value": w_nominal, "unit": units[1]},
                      "w": {"value": w, "unit": units[2]}},
           "subject_ref": None}
    req.update(over)
    return req


def _run(tau_nominal, w_nominal, w):
    return dc.execute(BINDING, _request(tau_nominal, w_nominal, w))


def _tau(result):
    return result["outputs"]["tau"]["value"]


def _failure(result):
    return (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def _form(tau_nominal="-2", w_nominal="10", w="5", decl=None, screen=None):
    form = {rload.DECLARATION_FIELD % d: rload.ANSWER_APPLIES
            for d in rload.DECLARATION_IDS}
    form.update({rload.SCREEN_FIELD % s: rload.SCREEN_NO for s in rload.SCREEN_ITEMS})
    form.update({rload.VALUE_FIELD % "tau_nominal": tau_nominal,
                 rload.VALUE_FIELD % "w_nominal": w_nominal,
                 rload.VALUE_FIELD % "w": w})
    for key, value in (decl or {}).items():
        form[rload.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[rload.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = rload.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return rload.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _method_artifact():
    return json.loads(rload.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data):
    target = tmp_path / "a.json"
    target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return target


def _value(body):
    marker = 'data-cap13r-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


@pytest.fixture
def mech():
    c, aid = _client_for("cap13r-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": MECH})


@pytest.fixture
def elec():
    c, aid = _client_for("cap13r-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


# ==========================================================================
# 1. the Owner's reference pairs and the sign convention
# ==========================================================================
@pytest.mark.parametrize("w,expected", REFERENCE_PAIRS)
def test_reference_pairs_at_owner_adapter_and_consumer(w, expected):
    result = _run(-2.0, 10.0, w)
    assert result["state"] == dc.STATE_SUCCESS
    assert _tau(result) == expected
    assert result["outputs"]["tau"]["unit"] == "N·m"
    assert result["validation_status"] == "UNVALIDATED"
    assert method.evaluate(-2.0, 10.0, w) == {"tau": expected}
    consumer = _evaluate(w=repr(w).replace(".0", "") if w else "0")
    assert consumer["outcome"] == rload.OUTCOME_SUCCESS
    assert _tau(consumer["result"]) == expected


def test_the_load_opposes_rotation_in_both_directions_and_is_never_abs():
    for w in (0.001, 1.0, 37.5, 1e6):
        assert _tau(_run(-3.0, 7.0, w)) < 0 < _tau(_run(-3.0, 7.0, -w))
        assert _tau(_run(-3.0, 7.0, w)) == -_tau(_run(-3.0, 7.0, -w))
    src = Path(method.__file__).read_text(encoding="utf-8")
    assert "abs(w" not in src and "abs(exact" in src     # abs() only in the error check


def test_zero_speed_is_exact_zero_not_an_underflow():
    for w in (0.0, -0.0):
        for tau_nominal, w_nominal in ((-2.0, 10.0), (-1e-300, 1e300), (-1e300, 1e-300)):
            result = _run(tau_nominal, w_nominal, w)
            assert result["state"] == dc.STATE_SUCCESS
            assert _tau(result) == 0.0 and math.copysign(1.0, _tau(result)) == 1.0
    # a nonzero exact result that would round to zero is a FAILURE, never 0.0
    assert _failure(_run(-1e-300, 1.0, 1e-300))


# ==========================================================================
# 2. numerical acceptance against an independent exact-rational reference
# ==========================================================================
@pytest.mark.parametrize("args", [
    (-2.0, 10.0, 5.0), (-0.1, 0.3, 0.7), (-1.0, 3.0, 1.0), (-math.pi, math.e, -1.5),
    (-1e300, 1e300, 1e300),          # naive tau*w would overflow
    (-1e300, 1e300, 1e-300),         # naive w/w_nominal would underflow
    (-sys.float_info.max, 1.0, 1.0), (-sys.float_info.max, 2.0, 2.0),
    (-SMALLEST_NORMAL, 1.0, 1.0), (-1.0, 1e-300, 1e-300),
])
def test_results_are_correctly_rounded_and_within_bound(args):
    result = _run(*args)
    assert result["state"] == dc.STATE_SUCCESS, args
    exact = _exact_tau(*args)
    assert _tau(result) == float(exact)
    assert abs(_exact(_tau(result)) - exact) <= abs(exact) * BOUND


def test_random_signed_results_are_correctly_rounded():
    rng = random.Random(20261024)
    for _ in range(2000):
        tau_nominal = -rng.uniform(1e-6, 1e6) * 10.0 ** rng.randint(-90, 90)
        w_nominal = rng.uniform(1e-6, 1e6) * 10.0 ** rng.randint(-90, 90)
        w = rng.choice((-1, 1)) * rng.uniform(1e-6, 1e6) * 10.0 ** rng.randint(-90, 90)
        result = _run(tau_nominal, w_nominal, w)
        assert result["state"] == dc.STATE_SUCCESS
        exact = _exact_tau(tau_nominal, w_nominal, w)
        assert _tau(result) == float(exact)
        assert (_tau(result) < 0) == (w > 0)


def test_overflow_is_an_integrity_failure_with_no_payload():
    for args in ((-1e300, 1e-300, 1e300), (-sys.float_info.max, 1.0, 2.0),
                 (-sys.float_info.max, 0.5, -1.0)):
        assert _failure(_run(*args)), args
    with pytest.raises(ArithmeticError):
        method.evaluate(-1e300, 1e-300, 1e300)


def test_underflow_to_zero_of_a_nonzero_result_fails_closed():
    for args in ((-1e-300, 1.0, 1e-300), (-TINY, 4.0, 1.0), (-1e-200, 1e200, -1.0)):
        assert _exact_tau(*args) != 0 and float(_exact_tau(*args)) == 0.0
        result = _run(*args)
        assert _failure(result) and result["state"] != dc.STATE_REFUSAL


@pytest.mark.parametrize("args", [
    (-TINY, 1.0, 1.0), (-TINY, 1.0, -3.0), (-SMALLEST_NORMAL, 2.0, 1.0),
    (-SMALLEST_NORMAL * 0.75, 1.0, 1.0), (-2.0 ** -1000, 1.0, 2.0 ** -60),
])
def test_exact_subnormal_results_are_accepted(args):
    exact = _exact_tau(*args)
    assert abs(exact) < _exact(SMALLEST_NORMAL) and _exact(float(exact)) == exact
    result = _run(*args)
    assert result["state"] == dc.STATE_SUCCESS
    assert _exact(_tau(result)) == exact


def test_inexact_subnormal_within_the_bound_is_accepted():
    args = (-SMALLEST_NORMAL * 0.75, 1.0, 1.0 + 2.0 ** -52)
    exact = _exact_tau(*args)
    assert _exact(float(exact)) != exact and abs(exact) < _exact(SMALLEST_NORMAL)
    produced = _tau(_run(*args))
    assert abs(produced) < SMALLEST_NORMAL
    assert abs(_exact(produced) - exact) <= abs(exact) * BOUND


@pytest.mark.parametrize("args", [(-TINY, 1.0, 1.5), (-TINY, 2.0, -3.0),
                                  (-TINY * 3, 2.0, 1.0)])
def test_inexact_subnormal_beyond_the_bound_fails_closed(args):
    exact = _exact_tau(*args)
    produced = float(exact)
    assert produced != 0.0 and abs(_exact(produced) - exact) > abs(exact) * BOUND
    assert _failure(_run(*args))
    with pytest.raises(ArithmeticError):
        method.evaluate(*args)


# ==========================================================================
# 3. signs, domain and inputs
# ==========================================================================
@pytest.mark.parametrize("tau_nominal,w_nominal", [
    (2.0, 10.0), (0.0, 10.0), (-0.0, 10.0), (-2.0, 0.0), (-2.0, -0.0), (-2.0, -10.0)])
def test_sign_violations_are_refused_before_the_adapter(tau_nominal, w_nominal):
    result = _run(tau_nominal, w_nominal, 5.0)
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None)
    with pytest.raises(ArithmeticError):
        method.evaluate(tau_nominal, w_nominal, 5.0)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"),
                                   True, "5", None])
def test_non_finite_and_non_numeric_inputs_are_refused(value):
    for role in ("tau_nominal", "w_nominal", "w"):
        req = _request()
        req["inputs"][role]["value"] = value
        result = dc.execute(BINDING, req)
        assert result["outputs"] is None
        assert result["reason"] in (dc.INVALID_NUMERIC_INPUT, dc.INPUT_MISSING)


def test_adapter_refuses_non_float_arguments():
    for bad in ((-2, 10.0, 5.0), (-2.0, 10, 5.0), (-2.0, 10.0, 5), (-2.0, 10.0, "5")):
        with pytest.raises(ArithmeticError):
            method.evaluate(*bad)


@pytest.mark.parametrize("over", [
    {"tau_nominal": "2"}, {"tau_nominal": "0"}, {"tau_nominal": "-0"},
    {"tau_nominal": "-0.0"}, {"w_nominal": "0"}, {"w_nominal": "-10"},
    {"w": "+5"}, {"w": "--5"}, {"w": "1e3"}, {"w": "5."}, {"w": ".5"}, {"w": "١"},
    {"w": " 5"}, {"w": "5 "}, {"w": "inf"}, {"w": "nan"}, {"w": ""},
    {"tau_nominal": "-2N"}, {"w": "1,5"}, {"w": "-" + "9" * 64},
])
def test_numeric_grammar_and_signs_are_invalid(over, monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(**over)["outcome"] == rload.INVALID_NUMERIC_INPUT, over
    assert not calls


def test_accepted_grammar_and_signed_zero_speed():
    assert rload.parse_number("-2", signed=True) == -2.0
    assert rload.parse_number("-0", signed=True) == 0.0
    assert rload.parse_number("-2") is None
    assert rload.parse_number("9" * 64) == float("9" * 64)
    assert _tau(_evaluate(w="-0")["result"]) == 0.0
    assert _tau(_evaluate(tau_nominal="-0.5", w_nominal="0.25", w="-3")["result"]) == 6.0


# ==========================================================================
# 4. the owner: inventory, units, bindings and integrity (Correction 04)
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["outputs"] == {"tau": {"value": -1.0, "unit": "N·m",
                                         "provenance": "CALCULATED"}}
    assert [u["record_id"] for u in result["unit_records"]] == ["dcu:U007", "dcu:U008"]
    assert [q["source_ref"] for q in result["source_qualification"]] == ["MODELICA-S1"]
    assert result["source_qualification"][0]["url"] == UPSTREAM
    assert (result["artifact_version"], result["implementation_version"]) == ("13", "1.12.0")
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_units_and_condition():
    assert ("cap13:linear_speed_dependent_rotational_load", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 13
    assert {"torque", "angular_velocity"} <= dc.ADMITTED_QUANTITY_KINDS
    assert {"N·m", "rad/s"} <= dc.ADMITTED_UNIT_TOKENS
    assert "less_than_zero" in dc._CONDITIONS
    record = _record(dc.load_artifact())
    assert [(r["role"], r["quantity_kind"], r["unit_token"]) for r in record["input_roles"]] \
        == [("tau_nominal", "torque", "N·m"), ("w_nominal", "angular_velocity", "rad/s"),
            ("w", "angular_velocity", "rad/s")]
    assert record["output_roles"] == [{"role": "tau", "quantity_kind": "torque",
                                       "unit_token": "N·m"}]
    assert record["result_range"] == []
    assert record["adapter_identity"] == "engine.cap13_rotational_load_method.evaluate"


def test_units_are_exact_with_no_alias_or_conversion():
    for unit in ("Nm", "N.m", "N*m", "rpm", "rev/s", "deg/s", "rad/sec"):
        for units in ((unit, "rad/s", "rad/s"), ("N·m", unit, "rad/s")):
            assert dc.execute(BINDING, _request(units=units))["reason"] == dc.UNKNOWN_UNIT
    for units in (("N·mm", "rad/s", "rad/s"), ("N·m", "N·m", "rad/s"),
                  ("N·m", "rad/s", "mm")):
        assert dc.execute(BINDING, _request(units=units))["reason"] == dc.UNIT_NOT_ADMITTED


def test_method_version_and_adapter_integrity_fail_closed():
    assert dc.execute(BINDING, _request(method_version="1.1"))["reason"] \
        == dc.VERSION_MISMATCH
    for adapter in (cap13_method.evaluate, moment_method.evaluate,
                    lambda tau_nominal, w_nominal, w: {"tau": tau_nominal * w / w_nominal}):
        swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, adapter)
        assert _failure(dc.execute(swapped, _request()))
    for binding in OTHER_BINDINGS:
        assert dc.execute(binding, _request())["reason"] == dc.OPERATION_NOT_ADMITTED


def test_app_wires_one_immutable_binding_per_method():
    assert webapp._CAP13_ROTATIONAL_LOAD_BINDING.adapter_identity \
        == "engine.cap13_rotational_load_method.evaluate"
    with pytest.raises(AttributeError):
        webapp._CAP13_ROTATIONAL_LOAD_BINDING.method_id = "x"
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 13
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("cap13_rotational_load", "cap13_content_config", "modelica",
                   "import fractions", "sqlite", "open(target, \"w"):
        assert banned not in owner_source.lower(), banned


def _owner_tamper(data, name):
    record = _record(data)
    if name == "second_torque_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "N·m"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "N.m"
        data["unit_records"].append(extra)
    elif name == "drop_rad_s":
        data["unit_records"] = [u for u in data["unit_records"] if u["unit_token"] != "rad/s"]
    elif name == "drop_kind":
        data["quantity_kinds"] = [k for k in data["quantity_kinds"]
                                  if k["quantity_kind"] != "angular_velocity"]
    elif name == "fifth_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "cap13:quadratic_speed_dependent_rotational_load"
        data["methods"].append(extra)
    elif name == "unknown_condition":
        record["applicability"][0]["condition"] = "not_positive"
    elif name == "policy_unresolved":
        record["source_qualification"][0]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "output_kind":
        record["output_roles"][0]["quantity_kind"] = "moment"
    elif name == "basis":
        data["source_use_policies"][-1]["inspection_basis"] = "EXECUTOR"
    return data


@pytest.mark.parametrize("name", ["second_torque_unit", "drop_rad_s", "drop_kind",
                                  "fifth_method", "unknown_condition",
                                  "policy_unresolved", "output_kind", "basis"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), name))
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    assert _failure(dc.execute(BINDING, _request(), artifact_path=path))


def test_owner_v3_records_are_unchanged_by_the_fourth_admission():
    data = dc.load_artifact()
    assert data["artifact_version"] == "13"
    units = {u["record_id"]: u["unit_token"] for u in data["unit_records"]}
    assert units == {"dcu:U001": "N", "dcu:U002": "mm", "dcu:U003": "W",
                     "dcu:U004": "K/W", "dcu:U005": "K", "dcu:U006": "N·mm",
                     "dcu:U007": "N·m", "dcu:U008": "rad/s",
                     "dcu:U009": "mV", "dcu:U010": "°C",
                     "dcu:U011": "V", "dcu:U012": "Ω", "dcu:U013": "A",
                     "dcu:U014": "J", "dcu:U015": "s",
                     "dcu:U016": "h", "dcu:U017": "A·h",
                     "dcu:U018": "kg", "dcu:U019": "N/m", "dcu:U020": "Hz",
                     "dcu:U021": "1/K"}
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "dcu:U006 only" in policies["dcu:SU006"]["inspected_content"]
    assert "BSD 3-Clause" in policies["dcu:SU007"]["inspected_content"]
    assert [m["method_id"] for m in data["methods"]][:3] == [
        "cap13:static_reactions_two_support",
        "therm01:conduction_temperature_difference_single_path",
        "cap13:planar_single_force_moment"]


# ==========================================================================
# 5. the method artifact and the consumer
# ==========================================================================
def test_method_artifact_loads_with_provenance_and_ip_boundary():
    data = rload.load_artifact()
    by_id = {r["record_id"]: r for r in data["sources"]}
    source = by_id["MODELICA-S1"]
    assert source["url"] == UPSTREAM
    assert "8ae3d35c24e519cb2996cab20f3b13daf2b0c50a" in source["inspected_content"]
    assert "TorqueDirection=false" in source["inspected_content"]
    assert "-flange.tau" in source["inspected_content"]
    assert "no Modelica source code" in source["paraphrase_only_limitation"]
    policy = by_id["cap13r:SU001"]
    for phrase in ("BSD 3-Clause", "1998-2025, Modelica Association and contributors",
                   "endorse", "registered trademark"):
        assert phrase in policy["inspected_content"], phrase
    assert "TorqueDirection=true" not in data["method"]["executed_form"]
    assert "abs(w)" in data["method"]["executed_form"]       # stated as excluded
    from engine import cap13_static_reactions as reactions
    assert rload.SCREEN_ITEMS == reactions.SCREEN_ITEMS


@pytest.mark.parametrize("mutate", [
    lambda d: d["declarations"][0].__setitem__("accepted_value", "the load torque is constant"),
    lambda d: d["declarations"][4].__setitem__("refusal", "NOT_DECLARED"),
    lambda d: d["numeric_domain"]["roles"][3].__setitem__("unit_token", "N·mm"),
    lambda d: d["method"].__setitem__("executed_form", "tau = tau_nominal * abs(w / w_nominal)"),
    lambda d: d["disclosure"].pop(),
    lambda d: d["sources"][0].__setitem__("source_use_policy_ref", "cap13:SU001"),
    lambda d: d["sources"][0].__setitem__("url", "https://example.com/copy.mo"),
    lambda d: d.__setitem__("artifact_version", "2"),
])
def test_method_artifact_tamper_is_knowledge_unavailable(mutate, monkeypatch):
    data = _method_artifact()
    mutate(data)
    with pytest.raises(rload.RotationalLoadKnowledgeError):
        rload.validate_artifact(data)
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert rload.evaluate(_captured(), BINDING, artifact=data)["outcome"] \
        == rload.KNOWLEDGE_UNAVAILABLE and not calls


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(decl={"nominal_point": ""}, screen={"children": "yes"},
                     tau_nominal="2")["outcome"] == rload.NOT_DECLARED
    assert _evaluate(screen={"pressure": "yes"}, decl={"load_only": "does_not_apply"},
                     tau_nominal="2")["outcome"] == rload.ENGINEERING_REVIEW_REQUIRED
    for decl in rload.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"}, w="x")["outcome"] \
            == rload.MODEL_NOT_SUPPORTED, decl
    assert not calls


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, rload.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, rload.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, rload.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, rload.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, rload.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome, monkeypatch):
    monkeypatch.setattr(dc, "execute", lambda *a, **k: {
        "state": state, "reason": reason, "outputs": None})
    result = _evaluate()
    assert (result["outcome"], result["owner_state"], result["owner_reason"]) \
        == (outcome, state, reason) and result["result"] is None


def test_consumer_sends_typed_signed_values_and_fixed_units(monkeypatch):
    seen = []
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: (
        seen.append(copy.deepcopy(r)), real(b, r, artifact_path=artifact_path))[1])
    _evaluate(tau_nominal="-2.5", w_nominal="4", w="-8")
    assert seen == [{"method_id": method.METHOD_ID, "method_version": "1.0",
                     "inputs": {"tau_nominal": {"value": -2.5, "unit": "N·m"},
                                "w_nominal": {"value": 4.0, "unit": "rad/s"},
                                "w": {"value": -8.0, "unit": "rad/s"}},
                     "subject_ref": None}]


def test_consumer_and_adapter_import_no_other_authority():
    import ast
    for module in (rload, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        for banned in ("cap13_static", "cap13_planar", "therm01", "record_store",
                       "safety_signal", "requests", "urllib", "openai", "modelica"):
            assert not any(banned in n for n in names), (module, banned)


# ==========================================================================
# 6. EN / AR fidelity and the contracts
# ==========================================================================
def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_english_wording_equals_the_artifact():
    content = rload.load_artifact()
    assert ui_text.text("UI_CAP13R_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"].replace("tau_nominal", "τ_nominal") \
            .replace("w_nominal", "ω_nominal")
        assert ui_text.text("UI_CAP13R_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."


def test_arabic_wording_equals_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    assert ui_text.text("UI_CAP13R_DISCLOSURE", "ar").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$",
                           _contract_section("**A-2", "**A-3"), re.M))
    for decl, ref in rload.DECLARATIONS:
        assert ui_text.text("UI_CAP13R_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    s9 = _contract_section("## 9. Result", "## 9A.")
    assert [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)] \
        == rload.load_artifact()["disclosure"]


def test_every_key_has_both_languages_and_the_sign_convention_is_explicit():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_CAP13R_[A-Z_]+)": \{', source)
    assert len(keys) >= 30
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    assert ui_text.text("UI_CAP13R_DECL_NOMINAL_POINT", "en").startswith("The value τ_nominal")
    assert "Τ" not in ui_text.text("UI_CAP13R_DECL_NOMINAL_POINT", "en")    # never capital Tau
    note = ui_text.text("UI_CAP13R_SIGN_NOTE", "en")
    for phrase in ("positive direction of rotation", "−flange.tau", "negative for positive ω",
                   "positive for negative ω", "zero at ω = 0"):
        assert phrase in note, phrase
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("is safe.", "will drive", "motor is suitable", "verified design",
                  "certified", "has been validated", "recommended motor"):
        assert claim not in english, claim


def test_correction_04_is_recorded_and_earlier_sections_unchanged():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 04" in body and "## 13C." in body
    section = body[body.index("## 13C."):body.index("## 14.")]
    for phrase in ("exactly four", "`torque`", "`angular_velocity`", "`N·m`", "`rad/s`",
                   "`less_than_zero`", "content version `4`", "`1.3.0`",
                   "NOT a generic owner policy"):
        assert phrase in section, phrase
    assert "**Methods — exactly three:**" in body[body.index("## 13B."):body.index("## 13C.")]


def test_method_contract_records_scope_and_exclusions():
    text = CONTRACT.read_text(encoding="utf-8")
    for phrase in ("TorqueDirection=false", "-flange.tau", "abs(ω)", "BSD", "8ae3d35",
                   "preliminary-motion blocker", "NOT discharged", "(-10, +2)", "(+10, -2)"):
        assert phrase in text, phrase


# ==========================================================================
# 7. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_mechanical_root_journey_and_reference_values(mech):
    c, _aid, sid = mech
    assert "data-cap13r-link" in _page(c, sid)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-cap13r-form" in body and "checked" not in body
    for w, expected in REFERENCE_PAIRS:
        typed = ("%g" % w) if w else "0"
        body = c.post(URL % sid, data=_form(w=typed)).get_data(as_text=True)
        assert _value(body) == "%r N·m" % expected, w
    assert "data-cap13r-sign-note" in body and "UNVALIDATED" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_CAP13R_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert "LinearSpeedDependentTorque" in body and "Modelica.Units.SI" in body


@pytest.mark.parametrize("over,outcome", [
    ({"tau_nominal": "2"}, "INVALID_NUMERIC_INPUT"),
    ({"w_nominal": "0"}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"children": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"linear_through_zero": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"sign_convention": ""}}, "NOT_DECLARED"),
])
def test_non_success_shows_one_reason_and_no_number(mech, over, outcome):
    c, _aid, sid = mech
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert html.escape(ui_text.text("UI_CAP13R_OUTCOME_" + outcome, "en"), quote=False) in body
    assert _value(body) is None and body.count("data-cap13r-outcome") == 1


def test_electronics_root_is_unsupported(elec, monkeypatch):
    c, _aid, sid = elec
    assert "data-cap13r-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._cap13r, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-cap13r-scope-note" in body
        assert "data-cap13r-form" not in body and _value(body) is None
    assert not called


@pytest.mark.parametrize("focus", (ELEC, MECH))
def test_integrated_mechanical_part_is_offered_with_attribution(focus):
    c, _ = _client_for("cap13r-part-%s@example.com" % focus)
    sid = _integrated(c, focus)
    eligible, part = webapp._calc_gate(sid, rload)
    assert eligible and part.domain == MECH
    assert "data-cap13r-link" in _page(c, sid)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) == "-1.0 N·m"
    assert _part_line(body, "cap13r") == PARTS["mech_part_name"]


def test_corrupt_or_unreadable_composition_grants_nothing(monkeypatch):
    c, _ = _client_for("cap13r-corrupt@example.com")
    sid = _integrated(c, ELEC)
    _corrupt("UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0")
    calls = _owner_spy(monkeypatch)
    assert webapp._calc_gate(sid, rload) == (False, None)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) is None and "data-cap13r-form" not in body and not calls
    sid2 = _integrated(c, ELEC)

    def broken(_sid):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", broken)
    assert webapp._calc_gate(sid2, rload) == (False, None)


def test_csrf_authorization_and_malformed_requests(mech):
    c, _aid, sid = mech
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("cap13r-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302 and "data-cap13r" not in r.get_data(as_text=True)
    r = c.post(URL % sid, data=dict(_form(), unexpected="1"))
    assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    body = c.post(URL % sid, data=_form(w="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body


@pytest.mark.parametrize("over", [{}, {"tau_nominal": "3"}, {"screen": {"children": "yes"}}])
def test_nothing_is_persisted(mech, over):
    c, _aid, sid = mech
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_no_report_export_api_or_safety_surface():
    src = Path(webapp.__file__).read_text(encoding="utf-8")
    start = src.index("# Stage 25 / CAP-13 — Linear Speed-Dependent Rotational Load")
    section = src[start:src.index("# Stage 27 / THERM-01 — Single-Path", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "_cap13m", "load_project_subsystems", "request.args"):
        assert banned not in section, banned
    assert section.count("_calc_gate(sid, _cap13r)") == 3
    assert [r.rule for r in webapp.app.url_map.iter_rules() if "rotational-load" in r.rule] \
        == ["/session/<sid>/rotational-load"] * 2
    for template in ("deliverable.html", "report.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "cap13r" not in path.read_text(encoding="utf-8")


def test_existing_three_calculations_are_unchanged(mech, elec):
    c, _aid, sid = mech
    body = c.post("/session/%s/support-reactions" % sid, data=_cap13_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">750.0 N</bdi>' in body and '<bdi dir="ltr">250.0 N</bdi>' in body
    body = c.post("/session/%s/planar-moment" % sid, data=_moment_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">1000.0 N·mm</bdi>' in body
    c2, _aid2, sid2 = elec
    body = c2.post("/session/%s/temperature-difference" % sid2,
                   data=_therm_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">25.0 K</bdi>' in body


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_attribution_escaping_and_arabic_isolation(lang):
    c, _ = _client_for("cap13r-hostile-%s@example.com" % lang)
    sid = _integrated(c, ELEC, mech_part_name=HOSTILE)
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form(w="-5")).get_data(as_text=True)
    assert "<script>alert" not in body
    assert html.unescape(_part_line(body, "cap13r")) == HOSTILE
    assert '<bdi dir="ltr">1.0 N·m</bdi>' in body
    if lang == "ar":
        assert 'dir="rtl"' in body
        for token in ("τ_nominal", "ω_nominal", "N·m", "rad/s", "UNVALIDATED", "NOT EVIDENCE"):
            assert '<bdi dir="ltr">%s</bdi>' % html.escape(token) in body, token
        assert '<bdi dir="ltr">−flange.tau</bdi>' in body      # minus kept with its token
        stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
        for item in ui_text.text("UI_CAP13R_DISCLOSURE", "ar").split("\n\n"):
            assert _norm(item) in _norm(stripped), item[:30]
