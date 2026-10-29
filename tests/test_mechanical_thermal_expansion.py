# -*- coding: utf-8 -*-
"""MECHANICAL-FREE-LINEAR-THERMAL-EXPANSION-01 - Free Linear Thermal Expansion, Slice 1 (directly owning tests).

The shared deterministic calculation / units owner (``engine/deterministic_calculation.py``)
after the bounded thirteenth admission of calc/units Correction 13 (§13L); the ONE
method ``mechanical:free_linear_thermal_expansion`` 1.0
(``engine/mechanical_thermal_expansion_method.py``) and its ONE consumer
(``engine/mechanical_thermal_expansion.py`` + the request-local page).

The numerical tests use INDEPENDENT oracles that share nothing with the
implementation path: the reference product computed here with the ``decimal``
module at 120 significant digits from the exact binary input values (an exact
product, since every binary64 value is a terminating decimal); the identity
``ΔL / (L_ref × ΔT) = α_avg`` checked with rational arithmetic; and the sign
rule checked separately. Acceptance is a relative error of at most 2^-50 (the
contract bound) with one correct rounding observed. The remaining tests press on
the method contract (§§1-9A): the closed thirteen-method inventory and the exact
1/K / mm / K bindings (ONE new coefficient kind; the existing length and
temperature-difference records unchanged); binding isolation from THERM-01;
owner artifact v13 and method-artifact integrity; the §7 pre-owner order and
owner correspondence; the exact-decimal screening and the exact / rounded
display; the Mechanical-root and declared-Mechanical-part gate (malformed, stale
and corrupt compositions fail closed); request integrity, isolation and no
persistence; the twelve existing methods unchanged; no coefficient suggested;
and EN / AR fidelity. Synthetic data only.
"""
import copy
import hashlib
import html
import json
import math
import random
import re
import sqlite3
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import mechanical_thermal_expansion as te
from engine import mechanical_thermal_expansion_method as method
from engine import cap13_static_reactions_method as cap13_method
from engine import dc_resistive_load_energy_method as energy_method
from engine import mechanical_natural_frequency_method as nf_method
from engine import therm01_conduction_method as therm_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _corrupt, _owner_spy, _part_line, MECH, ELEC, PARTS, CTRL, HOSTILE)
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_mechanical_natural_frequency import _form as _nf_form
from tests.test_therm01_temperature_difference import _form as _therm_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "MECHANICAL_FREE_LINEAR_THERMAL_EXPANSION_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
URL = "/session/%s/thermal-expansion"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
CAP13_BINDING = dc.bind_method(cap13_method.METHOD_ID, cap13_method.METHOD_VERSION,
                               cap13_method.evaluate)
THERM_BINDING = dc.bind_method(therm_method.METHOD_ID, therm_method.METHOD_VERSION,
                               therm_method.evaluate)
BOUND = Fraction(1, 2 ** 50)
ONE_ROUNDING = Fraction(1, 2 ** 53)
# The canonical digest of every content-version-12 record (18 kinds, 20 units,
# 21 source-use records, 12 methods), which Correction 13 leaves unchanged.
V12_RECORDS_DIGEST = "51260bbacb969e8a8a4b668ed4ed8c973200befb634678135a8d440eff4f2911"
# 0.0000231 1/K x 1000 mm x 50 K = 1.155 mm, exactly.
EXAMPLE = "1.155"


# --------------------------------------------------------------------------
# independent oracles
# --------------------------------------------------------------------------
def _exact(value):
    numerator, denominator = float(value).as_integer_ratio()
    return Fraction(numerator, denominator)


def _oracle(alpha, length, delta_t):
    """The exact product of the binary inputs computed with the decimal module
    (every binary64 value is a terminating decimal of at most 1074 digits; the
    precision below holds every product used here exactly)."""
    with localcontext() as context:
        context.prec = 2400
        product = Decimal(alpha) * Decimal(length) * Decimal(delta_t)
        assert context.flags[__import__("decimal").Inexact] is False
    return Fraction(product)


def _within(produced, alpha, length, delta_t, bound=BOUND):
    reference = _oracle(alpha, length, delta_t)
    if reference == 0:
        return produced == 0.0 and math.copysign(1.0, produced) > 0
    if (produced > 0) != (reference > 0):
        return False
    return abs(_exact(produced) - reference) <= abs(reference) * bound


def _identity_holds(produced, alpha, length, delta_t):
    """ΔL / (L_ref × ΔT) = α_avg within the bound, with rational arithmetic."""
    if delta_t == 0:
        return produced == 0.0
    ratio = _exact(produced) / (_exact(length) * _exact(delta_t))
    return abs(ratio - _exact(alpha)) <= _exact(alpha) * BOUND


def _request(alpha=0.0000231, length=1000.0, delta_t=50.0, units=("1/K", "mm", "K"),
             **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"alpha_avg": {"value": alpha, "unit": units[0]},
                      "L_ref": {"value": length, "unit": units[1]},
                      "delta_T": {"value": delta_t, "unit": units[2]}},
           "subject_ref": None}
    req.update(over)
    return req


def _run(alpha, length, delta_t):
    return dc.execute(BINDING, _request(alpha=alpha, length=length, delta_t=delta_t))


def _form(alpha="0.0000231", length="1000", delta_t="50", decl=None, screen=None):
    form = {te.DECLARATION_FIELD % d: te.ANSWER_APPLIES for d in te.DECLARATION_IDS}
    form.update({te.SCREEN_FIELD % s: te.SCREEN_NO for s in te.SCREEN_ITEMS})
    form.update({te.VALUE_FIELD % "alpha_avg": alpha, te.VALUE_FIELD % "L_ref": length,
                 te.VALUE_FIELD % "delta_T": delta_t})
    for key, value in (decl or {}).items():
        form[te.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[te.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = te.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return te.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _method_artifact():
    return json.loads(te.ARTIFACT_PATH.read_text(encoding="utf-8"))


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


def _value(body):
    marker = 'data-mte-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _en_decl(value):
    return (value[0].upper() + value[1:] if value[0].isascii() else value) + "."


@pytest.fixture
def mech():
    c, aid = _client_for("mte-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": "mechanical"})


@pytest.fixture
def elec():
    c, aid = _client_for("mte-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def elec_focus():
    c, _aid = _client_for("mte-part-elec-focus@example.com")
    return c, _integrated(c, ELEC)


# ==========================================================================
# 1. numerical acceptance against independent oracles
# ==========================================================================
@pytest.mark.parametrize("alpha,length,delta_t", [
    (0.0000231, 1000.0, 50.0), (0.0000231, 1000.0, -50.0), (1.2e-5, 3.0, 7.0),
    (1e-12, 1e-9, 1e-9), (1e-12, 1e-9, -1e-9), (999999999999.0, 999999999999.0, 999999999.0),
    (0.1, 0.1, 0.1), (1e-5, 1.0, 1.0 / 3.0), (17.0, 3.0, -0.125), (5e-7, 2500.0, -273.15)])
def test_normal_boundary_and_signed_values_meet_the_bound(alpha, length, delta_t):
    result = _run(alpha, length, delta_t)
    assert result["state"] == dc.STATE_SUCCESS
    produced = result["outputs"]["delta_L"]["value"]
    assert _within(produced, alpha, length, delta_t, ONE_ROUNDING)
    assert _identity_holds(produced, alpha, length, delta_t)
    assert (produced > 0) == (delta_t > 0)


def test_example_is_exact_and_the_sign_follows_the_temperature_change():
    assert _run(0.0000231, 1000.0, 50.0)["outputs"]["delta_L"]["value"] == 1.155
    assert _run(0.0000231, 1000.0, -50.0)["outputs"]["delta_L"]["value"] == -1.155
    assert _run(0.0000231, 1000.0, 50.0)["outputs"]["delta_L"]["value"] \
        == -_run(0.0000231, 1000.0, -50.0)["outputs"]["delta_L"]["value"]


def test_random_values_are_within_the_bound_and_the_identity():
    rng = random.Random(20261029)
    for _ in range(400):
        alpha = rng.uniform(1e-7, 1e-3) * 10 ** rng.randint(-5, 5)
        length = rng.uniform(1e-3, 1e4) * 10 ** rng.randint(-6, 6)
        delta_t = rng.uniform(-500.0, 500.0) * 10 ** rng.randint(-6, 6)
        produced = _run(alpha, length, delta_t)["outputs"]["delta_L"]["value"]
        assert _within(produced, alpha, length, delta_t, ONE_ROUNDING), (alpha, length, delta_t)
        assert _identity_holds(produced, alpha, length, delta_t)


@pytest.mark.parametrize("delta_t", [0.0, -0.0])
def test_zero_temperature_change_is_exactly_positive_zero(delta_t):
    produced = _run(0.0000231, 1000.0, delta_t)["outputs"]["delta_L"]["value"]
    assert produced == 0.0 and math.copysign(1.0, produced) == 1.0
    assert method.evaluate(0.0000231, 1000.0, delta_t) == {"delta_L": 0.0}
    assert math.copysign(1.0, method.evaluate(0.0000231, 1000.0, -0.0)["delta_L"]) == 1.0


def test_overflow_and_underflow_are_integrity_failures_with_no_payload():
    assert _failure(_run(1e200, 1e200, 1e10))
    assert _failure(_run(1e200, 1e200, -1e10))
    assert _failure(_run(1e-200, 1e-200, 1e-10))
    assert _failure(_run(1e-200, 1e-200, -1e-10))
    for args in ((1e200, 1e200, 1e10), (1e-200, 1e-200, 1e-10)):
        with pytest.raises(ArithmeticError):
            method.evaluate(*args)


def test_subnormal_results_are_accepted_only_within_the_bound():
    for alpha, length, delta_t in ((1e-160, 1e-150, 3.0), (3e-160, 7e-150, -1.0)):
        result = _run(alpha, length, delta_t)
        if result["state"] == dc.STATE_SUCCESS:
            produced = result["outputs"]["delta_L"]["value"]
            assert _within(produced, alpha, length, delta_t, Fraction(1, 2 ** 52))
        else:
            assert _failure(result)


@pytest.mark.parametrize("alpha,length", [(0.0, 1.0), (-1e-5, 1.0), (1e-5, 0.0), (1e-5, -1.0)])
def test_non_positive_coefficient_or_length_never_reaches_the_adapter(alpha, length):
    result = _run(alpha, length, 10.0)
    assert result["outputs"] is None
    assert (result["state"], result["reason"]) == (dc.STATE_UNABLE,
                                                   dc.INPUT_OUTSIDE_ADMITTED_RANGE)
    with pytest.raises(ArithmeticError):
        method.evaluate(alpha, length, 10.0)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"),
                                   "1", True, None])
def test_non_finite_and_non_numeric_inputs_are_refused(value):
    for args in ((value, 1000.0, 50.0), (1e-5, value, 50.0), (1e-5, 1000.0, value)):
        result = _run(*args)
        assert result["outputs"] is None and result["state"] != dc.STATE_SUCCESS


def test_adapter_refuses_non_float_or_non_finite_arguments():
    for args in ((1, 1.0, 1.0), (1e-5, 1, 1.0), (1e-5, 1.0, 1), (float("nan"), 1.0, 1.0),
                 (1e-5, float("inf"), 1.0), (1e-5, 1.0, -float("inf")), (True, 1.0, 1.0)):
        with pytest.raises(ArithmeticError):
            method.evaluate(*args)


def _float_stand_in(transform):
    """A stand-in for ``float`` inside the adapter module: real floats still
    pass its ``isinstance`` checks, and the ONE conversion of the exact product
    is replaced by ``transform`` of the correctly rounded value."""
    import builtins

    class _Meta(type):
        def __instancecheck__(cls, obj):
            return isinstance(obj, builtins.float)

    class _Float(metaclass=_Meta):
        def __new__(cls, value):
            return transform(builtins.float(value))
    return _Float


@pytest.mark.parametrize("transform", [
    lambda x: -x,                       # the sign is lost
    lambda x: x * (1 + 2 ** -40),       # outside the accepted relative error
    lambda x: 0.0,                      # a nonzero product underflowed to zero
    lambda x: float("inf"),             # a non-finite result
])
def test_adapter_rejects_a_lost_sign_or_an_out_of_bound_result(monkeypatch, transform):
    assert method.evaluate(2e-5, 3.0, -4.0)["delta_L"] < 0
    monkeypatch.setattr(method, "float", _float_stand_in(transform), raising=False)
    with pytest.raises(ArithmeticError):
        method.evaluate(2e-5, 3.0, 4.0)
    with pytest.raises(ArithmeticError):
        method.evaluate(2e-5, 3.0, -4.0)


def test_adapter_accepts_one_correct_rounding_through_the_stand_in(monkeypatch):
    monkeypatch.setattr(method, "float", _float_stand_in(lambda x: x), raising=False)
    assert method.evaluate(0.0000231, 1000.0, 50.0) == {"delta_L": 1.155}


# ==========================================================================
# 2. the owner: packaging, closed inventory, units, versions, isolation
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["state"] == dc.STATE_SUCCESS and result["reason"] is None
    assert result["outputs"] == {"delta_L": {"value": 1.155, "unit": "mm",
                                             "provenance": "CALCULATED"}}
    assert result["inputs"]["alpha_avg"] == {"value": 0.0000231, "unit": "1/K",
                                             "provenance": "OWNER_STATED"}
    assert result["inputs"]["L_ref"] == {"value": 1000.0, "unit": "mm",
                                         "provenance": "OWNER_STATED"}
    assert result["inputs"]["delta_T"] == {"value": 50.0, "unit": "K",
                                           "provenance": "OWNER_STATED"}
    assert (result["method_id"], result["method_version"]) == (
        "mechanical:free_linear_thermal_expansion", "1.0")
    assert (result["artifact_version"], result["implementation_version"]) == ("13", "1.12.0")
    assert [u["record_id"] for u in result["unit_records"]] == [
        "dcu:U002", "dcu:U005", "dcu:U021"]
    assert [q["source_ref"] for q in result["source_qualification"]] == [
        "NBS-TE-S1", "NIST-TE-U"]
    assert [q["source_use_policy_ref"] for q in result["source_qualification"]] \
        == ["dcu:SU022", "dcu:SU023"]
    assert result["subject_ref"] == "opaque"
    assert re.fullmatch(r"[0-9a-f]{64}", result["result_identity"])
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_and_versions():
    assert ("mechanical:free_linear_thermal_expansion", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 13
    assert "linear_thermal_expansion_coefficient" in dc.ADMITTED_QUANTITY_KINDS
    assert len(dc.ADMITTED_QUANTITY_KINDS) == 19
    assert "1/K" in dc.ADMITTED_UNIT_TOKENS and len(dc.ADMITTED_UNIT_TOKENS) == 21
    # no alias, no conversion token, no property scale
    assert not any(t in dc.ADMITTED_UNIT_TOKENS
                   for t in ("1/°C", "°C⁻¹", "K⁻¹", "/K", "ppm/K", "µm/(m·K)", "10⁻⁶/K",
                             "m", "cm", "µm", "in", "°F", "1/s"))
    assert dc.KIND_TOKEN_EXCEPTIONS == {"voltage": frozenset({"mV", "V"}),
                                        "time": frozenset({"s", "h"})}
    assert dc.IMPLEMENTATION_VERSION == "1.12.0"
    data = dc.load_artifact()
    assert data["artifact_version"] == "13"
    kinds = {k["quantity_kind"]: k["dimension"] for k in data["quantity_kinds"]}
    assert kinds["linear_thermal_expansion_coefficient"] == "Theta^-1"
    assert (kinds["length"], kinds["temperature_difference"]) == ("L", "Theta")
    record = _record(data)
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"]] == [
        ("alpha_avg", "linear_thermal_expansion_coefficient", "1/K"),
        ("L_ref", "length", "mm"), ("delta_T", "temperature_difference", "K")]
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["output_roles"]] == [("delta_L", "length", "mm")]
    assert record["applicability"] == [
        {"role": "alpha_avg", "condition": "greater_than_zero", "bound_role": None},
        {"role": "L_ref", "condition": "greater_than_zero", "bound_role": None}]
    assert record["result_range"] == []
    assert record["adapter_identity"] == "engine.mechanical_thermal_expansion_method.evaluate"
    assert record["method_authority_artifact"] == {
        "artifact_id": te.ARTIFACT_ID, "artifact_version": "1"}
    units = {u["unit_token"]: u for u in data["unit_records"]}
    assert units["1/K"]["record_id"] == "dcu:U021"
    assert units["1/K"]["quantity_kind"] == "linear_thermal_expansion_coefficient"
    assert units["1/K"]["source_use_policy_ref"] == "dcu:SU023"
    assert "Special Publication 330" in units["1/K"]["source_title"]
    assert "bounded quantity usage" in units["1/K"]["inspected_content"]
    assert "no conversion is admitted" in units["1/K"]["inspected_content"]
    # the reused records keep their own scope and record ids
    assert (units["mm"]["record_id"], units["mm"]["source_use_policy_ref"]) == (
        "dcu:U002", "dcu:SU001")
    assert (units["K"]["record_id"], units["K"]["source_use_policy_ref"]) == (
        "dcu:U005", "dcu:SU003")


def test_units_are_exact_with_no_alias_or_conversion():
    for unit in ("1/°C", "°C⁻¹", "K⁻¹", "/K", "ppm/K", "1/k", "µm/(m·K)", "10⁻⁶/K"):
        result = dc.execute(BINDING, _request(units=(unit, "mm", "K")))
        assert result["reason"] in (dc.UNKNOWN_UNIT, dc.UNIT_NOT_ADMITTED), unit
    for unit in ("m", "cm", "µm", "in", "MM"):
        result = dc.execute(BINDING, _request(units=("1/K", unit, "K")))
        assert result["reason"] == dc.UNKNOWN_UNIT, unit
    for unit in ("°F", "k", "degC"):
        result = dc.execute(BINDING, _request(units=("1/K", "mm", unit)))
        assert result["reason"] == dc.UNKNOWN_UNIT, unit
    # admitted tokens of other kinds are still never accepted for these roles
    for units in (("K", "mm", "K"), ("1/K", "N", "K"), ("1/K", "mm", "°C"),
                  ("1/K", "mm", "1/K"), ("1/K", "K", "mm"), ("Hz", "mm", "K")):
        assert dc.execute(BINDING, _request(units=units))["reason"] \
            == dc.UNIT_NOT_ADMITTED, units


def test_method_version_and_adapter_integrity_fail_closed():
    assert dc.execute(BINDING, _request(method_version="1.1"))["reason"] \
        == dc.VERSION_MISMATCH
    stale = dc.bind_method(method.METHOD_ID, "0.9", method.evaluate)
    assert dc.execute(stale, _request())["reason"] == dc.VERSION_MISMATCH
    for adapter in (energy_method.evaluate, nf_method.evaluate,
                    lambda alpha_avg, L_ref, delta_T: {"delta_L": alpha_avg * L_ref * delta_T}):
        swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, adapter)
        assert _failure(dc.execute(swapped, _request()))
    req = _request()
    del req["inputs"]["L_ref"]
    assert dc.execute(BINDING, req)["reason"] == dc.INPUT_MISSING
    req = _request()
    req["inputs"]["alpha_second"] = {"value": 1e-5, "unit": "1/K"}
    assert dc.execute(BINDING, req)["reason"] == dc.OPERATION_NOT_ADMITTED
    unknown = dc.bind_method("mechanical:thermal_stress", "1.0", method.evaluate)
    assert dc.execute(unknown, _request(method_id="mechanical:thermal_stress")
                      )["reason"] == dc.METHOD_NOT_REGISTERED


def test_bindings_are_isolated_and_therm01_is_never_fed():
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
    cap13 = dc.execute(CAP13_BINDING, cap13_req)
    assert (cap13["outputs"]["R_L"]["value"], cap13["outputs"]["R_R"]["value"]) \
        == (750.0, 250.0)
    assert dc.execute(THERM_BINDING, therm_req)["outputs"]["delta_T"]["value"] == 25.0
    # the THERM-01 result names a different role meaning; nothing maps one to the other
    therm_record = _record(dc.load_artifact(), therm_method.METHOD_ID)
    assert therm_record["output_roles"] == [
        {"role": "delta_T", "quantity_kind": "temperature_difference", "unit_token": "K"}]


def test_app_wires_one_immutable_binding():
    assert webapp._MTE_BINDING.adapter_identity \
        == "engine.mechanical_thermal_expansion_method.evaluate"
    assert webapp._MTE_BINDING.method_id == method.METHOD_ID
    with pytest.raises(AttributeError):
        webapp._MTE_BINDING.method_id = "x"
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    assert app_source.count("_dcalc.bind_method(") == 13
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("mechanical_thermal_expansion", "mechanical_content_config",
                   "alpha_avg", "L_ref"):
        assert banned not in owner_source, banned


# ==========================================================================
# 3. owner artifact v13 and the method artifact: integrity and tamper
# ==========================================================================
def _owner_tamper(data, name):
    record = _record(data)
    if name == "second_coefficient_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "1/K"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U022", "1/°C"
        data["unit_records"].append(extra)
    elif name == "k_rebound_to_coefficient":
        [u for u in data["unit_records"] if u["unit_token"] == "K"][0]["quantity_kind"] = \
            "linear_thermal_expansion_coefficient"
    elif name == "drop_coefficient_unit":
        data["unit_records"] = [u for u in data["unit_records"] if u["unit_token"] != "1/K"]
    elif name == "drop_coefficient_kind":
        data["quantity_kinds"] = [k for k in data["quantity_kinds"]
                                  if k["quantity_kind"] != "linear_thermal_expansion_coefficient"]
    elif name == "extra_kind":
        data["quantity_kinds"].append({"quantity_kind": "volumetric_thermal_expansion_coefficient",
                                       "dimension": "Theta^-1"})
    elif name == "drop_method":
        data["methods"].remove(record)
    elif name == "extra_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "mechanical:thermal_stress"
        data["methods"].append(extra)
    elif name == "output_unit":
        record["output_roles"][0]["unit_token"] = "K"
    elif name == "input_kind":
        record["input_roles"][0]["quantity_kind"] = "temperature_difference"
    elif name == "policy_unresolved":
        record["source_qualification"][0]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "basis":
        record["source_qualification"][1]["inspection_basis"] = "EXECUTOR"
    elif name == "adapter":
        record["adapter_identity"] = "engine.dc_resistive_load_energy_method.evaluate"
    return data


@pytest.mark.parametrize("name", [
    "second_coefficient_unit", "k_rebound_to_coefficient", "drop_coefficient_unit",
    "drop_coefficient_kind", "extra_kind", "drop_method", "extra_method", "output_unit",
    "input_kind", "policy_unresolved", "basis", "adapter"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), name))
    result = dc.execute(BINDING, _request(), artifact_path=path)
    assert result["outputs"] is None
    assert result["state"] in (dc.STATE_FAILURE, dc.STATE_REFUSAL)
    if name not in ("drop_method", "adapter"):
        with pytest.raises(dc.CalculationArtifactError):
            dc.load_artifact(path)


def test_owner_artifact_unreadable_is_source_unavailable(tmp_path):
    result = dc.execute(BINDING, _request(), artifact_path=tmp_path / "missing.json")
    assert (result["state"], result["reason"]) == (dc.STATE_UNABLE,
                                                   dc.SOURCE_UNAVAILABLE)


def test_owner_v12_records_are_unchanged_by_the_thirteenth_admission():
    data = dc.load_artifact()
    assert data["artifact_version"] == "13"
    v12 = {"quantity_kinds": data["quantity_kinds"][:18],
           "unit_records": data["unit_records"][:20],
           "source_use_policies": data["source_use_policies"][:21],
           "methods": data["methods"][:12]}
    canonical = json.dumps(v12, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(canonical.encode()).hexdigest() == V12_RECORDS_DIGEST
    assert [k["quantity_kind"] for k in data["quantity_kinds"][18:]] == [
        "linear_thermal_expansion_coefficient"]
    assert [u["record_id"] for u in data["unit_records"][20:]] == ["dcu:U021"]
    assert [p["record_id"] for p in data["source_use_policies"][21:]] == [
        "dcu:SU022", "dcu:SU023"]
    assert [m["method_id"] for m in data["methods"][12:]] == [method.METHOD_ID]
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "mte:SU001" in policies["dcu:SU022"]["inspected_content"]
    assert "NBS-TE-S1" in policies["dcu:SU022"]["inspected_content"]
    assert "Circular 486" in policies["dcu:SU022"]["inspected_content"]
    assert "SRC-029 is relied upon by nothing" in policies["dcu:SU022"]["inspected_content"]
    assert "dcu:U021 (1/K)" in policies["dcu:SU023"]["inspected_content"]
    assert all(p["inspection_basis"] == "LEAD_SUPPLIED" for p in data["source_use_policies"])
    assert "Content version 13 admits exactly thirteen methods" in data["governance_note"]
    text = json.dumps(data, ensure_ascii=False)
    for banned in ("thermal stress calculation", "clearance adequacy is", "DOE-HDBK-1017"):
        assert banned not in text, banned


def test_method_artifact_loads_and_binds_its_sources():
    data = te.load_artifact()
    assert data["method"]["method_id"] == method.METHOD_ID
    assert "2^-52" in data["method"]["executed_form"]
    assert "+0.0" in data["method"]["executed_form"]
    assert "states no convention" in data["method"]["derivation"] \
        or "no convention is stated" in data["method"]["derivation"]
    assert [d["declaration_id"] for d in data["declarations"]] == list(te.DECLARATION_IDS)
    assert len(data["declarations"]) == 8
    assert [i["item_id"] for i in data["screen_items"]] == list(te.SCREEN_ITEMS)
    by_id = {r["record_id"]: r for r in data["sources"]}
    assert by_id["NBS-TE-S1"]["source_use_policy_ref"] == "mte:SU001"
    assert by_id["NASA-TE-S2"]["source_use_policy_ref"] == "mte:SU002"
    assert by_id["NIST-TE-U"]["source_use_policy_ref"] == "mte:SU003"
    assert "Hidnert and W. Souder" in by_id["NBS-TE-S1"]["source_title"]
    assert "average and an instantaneous coefficient" in by_id["NBS-TE-S1"]["inspected_content"]
    assert "NOT quoted" in by_id["NBS-TE-S1"]["inspected_content"]
    assert "64b4f0b841093e50b8edb88dcf15599b9fee28708af976b672f6d721b76ac883" \
        in by_id["NBS-TE-S1"]["inspected_content"]
    assert "NOT adopted" in by_id["NASA-TE-S2"]["inspected_content"]
    assert "GOV_PUBLIC_USE_PERMITTED" in by_id["mte:SU002"]["inspected_content"]
    assert all(r["inspection_basis"] == "LEAD_SUPPLIED" for r in data["sources"])
    assert len(data["disclosure"]) == 7
    from engine import cap13_planar_moment as moment
    assert te.SCREEN_ITEMS == moment.SCREEN_ITEMS
    text = json.dumps(data, ensure_ascii=False)
    # no coefficient value, material value or data table is supplied
    assert "SRC-029" in text and "relied upon by nothing" in text
    for banned in ("aluminium", "aluminum", "steel", "brass", "copper", "typical value",
                   "DOE-HDBK-1017"):
        assert banned not in text.lower(), banned


@pytest.mark.parametrize("mutate", [
    lambda d: d["declarations"][4].__setitem__(
        "accepted_value", "α_avg may be a value at one temperature"),
    lambda d: d["declarations"][0].__setitem__("refusal", "NOT_DECLARED"),
    lambda d: d["numeric_domain"]["roles"][0].__setitem__("unit_token", "1/°C"),
    lambda d: d["numeric_domain"]["roles"][2].__setitem__("quantity_kind", "celsius_temperature"),
    lambda d: d["disclosure"].pop(),
    lambda d: d["limitations"].__setitem__(0, "The required gap is calculated."),
    lambda d: d["sources"][0].__setitem__("source_use_policy_ref", "mnf:SU001"),
    lambda d: d["method"].__setitem__("executed_form", "delta_L = alpha * L"),
    lambda d: d.__setitem__("artifact_version", "2"),
    lambda d: d["screen_items"].pop(),
    lambda d: d["declarations"].pop(),
    lambda d: d["sources"].pop(1),
])
def test_method_artifact_tamper_is_knowledge_unavailable(tmp_path, mutate, monkeypatch):
    data = _method_artifact()
    mutate(data)
    with pytest.raises(te.ThermalExpansionKnowledgeError):
        te.validate_artifact(data)
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    result = te.evaluate(_captured(), BINDING, artifact=data)
    assert result["outcome"] == te.KNOWLEDGE_UNAVAILABLE and not calls
    assert result["display_value"] is None


def test_method_artifact_unreadable_is_knowledge_unavailable(tmp_path):
    with pytest.raises(te.ThermalExpansionKnowledgeError):
        te.load_artifact(tmp_path / "missing.json")
    (tmp_path / "bad.json").write_text("{", encoding="utf-8")
    with pytest.raises(te.ThermalExpansionKnowledgeError):
        te.load_artifact(tmp_path / "bad.json")


# ==========================================================================
# 4. the consumer: capture, the §7 order, the exact reference, the display
# ==========================================================================
def test_consumer_success_carries_the_owner_result_and_an_exact_display():
    result = _evaluate()
    assert result["outcome"] == te.OUTCOME_SUCCESS
    assert result["owner_state"] == dc.STATE_SUCCESS
    assert result["result"]["outputs"]["delta_L"]["value"] == 1.155
    assert (result["display_value"], result["display_exact"]) == (EXAMPLE, True)
    assert result["change"] == Fraction("1.155")
    negative = _evaluate(delta_t="-50")
    assert (negative["display_value"], negative["display_exact"]) == ("-1.155", True)


@pytest.mark.parametrize("alpha,length,delta_t", [
    ("0.0000231", "1000", "50"), ("0.000012", "3", "-7"), ("0.00001", "1", "0.333333333"),
    ("0.000000000001", "0.000000001", "-0.000000001"),
    ("999999999999.999999999999", "999999999999.999999999", "-999999999.999999999"),
    ("0.000017", "2500.5", "-273.15")])
def test_exact_reference_matches_the_independent_decimal_oracle(alpha, length, delta_t):
    reference = te.exact_change(Fraction(alpha), Fraction(length), Fraction(delta_t))
    with localcontext() as context:
        context.prec = 200
        oracle = Fraction(Decimal(alpha) * Decimal(length) * Decimal(delta_t))
    assert reference == oracle
    result = _evaluate(alpha=alpha, length=length, delta_t=delta_t)
    assert result["outcome"] == te.OUTCOME_SUCCESS
    produced = result["result"]["outputs"]["delta_L"]["value"]
    assert abs(_exact(produced) - oracle) <= abs(oracle) * BOUND
    assert (produced > 0) == (oracle > 0)


@pytest.mark.parametrize("value,text,exact", [
    (Fraction(0), "0", True),
    (Fraction("1.155"), "1.155", True),
    (Fraction("-1.155"), "-1.155", True),
    (Fraction(1, 3), "0.333333333333", False),
    (Fraction(-2, 3), "-0.666666666667", False),
    (Fraction(10) ** -30, "1 × 10^-30", True),
    (-Fraction(10) ** -7, "-1 × 10^-7", True),
    (Fraction(10) ** -6, "0.000001", True),
    (Fraction(10) ** 12, "1 × 10^12", True),
    (Fraction("999999999999.5"), "1 × 10^12", False),
    (Fraction("123456789012.5"), "123456789012", False),
    (Fraction("0.0000123456789012345"), "0.0000123456789012", False),
])
def test_display_rounds_once_to_twelve_significant_digits(value, text, exact):
    assert te.format_change(value) == (text, exact)


def test_agrees_with_reference_is_strict():
    assert te.agrees_with_reference(1.155, Fraction("1.155"))
    assert not te.agrees_with_reference(-1.155, Fraction("1.155"))
    assert not te.agrees_with_reference(1.155 * (1 + 2 ** -48), Fraction("1.155"))
    assert te.agrees_with_reference(0.0, Fraction(0))
    assert not te.agrees_with_reference(-0.0, Fraction(0))
    assert not te.agrees_with_reference(0.0, Fraction("1e-30"))
    assert not te.agrees_with_reference(1e-30, Fraction(0))
    for bad in (float("nan"), float("inf"), "1.155", None, 1):
        assert not te.agrees_with_reference(bad, Fraction("1.155"))
    assert not te.agrees_with_reference(1.155, 1.155)


def test_owner_result_in_another_unit_or_off_reference_is_knowledge_unavailable(monkeypatch):
    real = dc.execute

    def wrong_unit(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["delta_L"]["unit"] = "K"
        return result
    monkeypatch.setattr(dc, "execute", wrong_unit)
    assert _evaluate()["outcome"] == te.KNOWLEDGE_UNAVAILABLE

    def off_reference(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["delta_L"]["value"] = -result["outputs"]["delta_L"]["value"]
        return result
    monkeypatch.setattr(dc, "execute", off_reference)
    result = _evaluate()
    assert result["outcome"] == te.KNOWLEDGE_UNAVAILABLE and result["result"] is None
    assert result["display_value"] is None


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(decl={"free_unrestrained": ""}, screen={"pressure": "yes"},
                     alpha="abc")["outcome"] == te.NOT_DECLARED
    assert _evaluate(screen={"pressure": ""})["outcome"] == te.NOT_DECLARED
    assert _evaluate(screen={"high_temperature": "yes"},
                     decl={"reference_length": "does_not_apply"},
                     alpha="0")["outcome"] == te.ENGINEERING_REVIEW_REQUIRED
    for decl in te.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"}, alpha="x")["outcome"] \
            == te.MODEL_NOT_SUPPORTED, decl
    assert not calls


@pytest.mark.parametrize("text", [
    "", "-1", "+1", "1e3", "1E3", "1,5", "1_0", " 1", "1 ", ".5", "5.", "0x10",
    "inf", "nan", "١٢", "12mm", "0", "0.0", "-0", "0.000000000", "1234567890123",
    "1.0000000001", "9" * 13])
def test_length_grammar_representation_limits_and_zero_are_invalid(text, monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(length=text)["outcome"] == te.INVALID_NUMERIC_INPUT, text
    assert not calls


@pytest.mark.parametrize("text", [
    "", "-0.00001", "+0.00001", "2.3e-5", "23E-6", "0,000023", " 0.1", ".00002",
    "0.", "inf", "nan", "٠٫١", "0.000023/K", "0", "0.000000000000", "-0",
    "1234567890123", "0.0000000000001", "23 × 10⁻⁶"])
def test_coefficient_grammar_representation_limits_and_zero_are_invalid(text, monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(alpha=text)["outcome"] == te.INVALID_NUMERIC_INPUT, text
    assert not calls


@pytest.mark.parametrize("text", [
    "", "+50", "--50", "5e1", "50 ", "50K", "50°C", "1234567890", "1.0000000001", ".5",
    "-", "inf", "-nan", "٥٠"])
def test_temperature_change_grammar_is_strict(text, monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(delta_t=text)["outcome"] == te.INVALID_NUMERIC_INPUT, text
    assert not calls


def test_numeric_grammar_accepts_exact_decimals_within_the_limits():
    assert te.parse_value("0.0000231", "alpha_avg") == Fraction(231, 10 ** 7)
    assert te.parse_value("0.000000000001", "alpha_avg") == Fraction(1, 10 ** 12)
    assert te.parse_value("0.0000000000001", "alpha_avg") is None
    assert te.parse_value("123456789012.123456789", "L_ref") == Fraction("123456789012.123456789")
    assert te.parse_value("-273.15", "delta_T") == Fraction("-273.15")
    assert te.parse_value("-0", "delta_T") == 0
    assert te.parse_value("-1", "L_ref") is None and te.parse_value("-1", "alpha_avg") is None
    assert te.parse_value("1234567890", "delta_T") is None
    assert te.parse_value(2.5, "L_ref") is None
    for zero in ("0", "-0", "0.000000000"):
        result = _evaluate(delta_t=zero)
        assert (result["outcome"], result["display_value"], result["display_exact"]) == (
            te.OUTCOME_SUCCESS, "0", True)
        assert math.copysign(1.0, result["result"]["outputs"]["delta_L"]["value"]) == 1.0
    assert _evaluate(alpha="999999999999.999999999999", length="999999999999.999999999",
                     delta_t="-999999999.999999999")["outcome"] == te.OUTCOME_SUCCESS


@pytest.mark.parametrize("form", [
    {"unexpected": ["1"]},
    {te.VALUE_FIELD % "alpha_avg": ["1", "2"]},
    {te.DECLARATION_FIELD % "free_unrestrained": ["yes"]},
    {te.SCREEN_FIELD % "children": ["maybe"]},
    {te.VALUE_FIELD % "L_ref": [2.5]},
    {"value_delta_L": ["3"]},
    {"value_alpha_second": ["0.00001"]},
    {"material": ["steel"]},
])
def test_malformed_capture_is_none(form):
    base = {k: [v] for k, v in _form().items()}
    base.update(form)
    assert te.capture_form(base) is None
    assert te.capture_form("not a mapping") is None


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, te.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, te.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, te.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, te.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, te.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, te.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, te.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, te.UNMAPPED_OWNER_OUTCOME),
    (dc.STATE_REFUSAL, dc.OPERATION_NOT_ADMITTED, te.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome,
                                                        monkeypatch):
    monkeypatch.setattr(dc, "execute", lambda *a, **k: {
        "state": state, "reason": reason, "outputs": None})
    result = _evaluate()
    assert result["outcome"] == outcome
    assert (result["owner_state"], result["owner_reason"]) == (state, reason)
    assert result["result"] is None and result["display_value"] is None


def test_owner_failure_from_a_tampered_owner_artifact_is_never_a_refusal(tmp_path):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), "output_unit"))
    result = te.evaluate(_captured(), BINDING, owner_artifact_path=path)
    assert result["outcome"] == te.KNOWLEDGE_UNAVAILABLE
    assert result["owner_state"] == dc.STATE_FAILURE


def test_consumer_typed_values_and_fixed_units_reach_the_owner(monkeypatch):
    seen = []
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: (
        seen.append(copy.deepcopy(r)), real(b, r, artifact_path=artifact_path))[1])
    _evaluate(alpha="0.000012", length="250.5", delta_t="-0")
    assert seen == [{"method_id": method.METHOD_ID, "method_version": "1.0",
                     "inputs": {"alpha_avg": {"value": 0.000012, "unit": "1/K"},
                                "L_ref": {"value": 250.5, "unit": "mm"},
                                "delta_T": {"value": 0.0, "unit": "K"}},
                     "subject_ref": None}]
    assert math.copysign(1.0, seen[0]["inputs"]["delta_T"]["value"]) == 1.0


def test_consumer_and_adapter_import_no_other_method_authority():
    import ast
    for module in (te, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module or "")
                imports.update("%s.%s" % (node.module, a.name) for a in node.names)
        for banned in ("cap13", "therm01", "tmp36", "dc_resistive", "pwm", "control_cycle",
                       "natural_frequency", "record_store", "safety_signal", "idea_state",
                       "requests", "urllib", "openai", "numpy", "scipy", "mpmath"):
            assert not any(banned in name for name in imports), (module, banned)
    adapter_source = Path(method.__file__).read_text(encoding="utf-8")
    assert "deterministic_calculation" not in adapter_source


# ==========================================================================
# 5. EN / AR fidelity and the governing documents
# ==========================================================================
def test_english_wording_equals_the_artifact():
    content = te.load_artifact()
    assert ui_text.text("UI_MTE_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        assert ui_text.text("UI_MTE_DECL_" + entry["declaration_id"].upper(), "en") \
            == _en_decl(entry["accepted_value"])
    for entry in content["screen_items"]:
        assert ui_text.text("UI_CAP13_SCREEN_" + entry["item_id"].upper(), "en") \
            == entry["item"][0].upper() + entry["item"][1:]


def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_arabic_and_english_wording_equal_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    items = [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    assert ui_text.text("UI_MTE_DISCLOSURE", "ar").split("\n\n") == items
    a2 = _contract_section("**A-2", "**A-3")
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$", a2, re.M))
    refs = ("D-1", "D-2", "D-3", "D-4", "D-5", "D-6", "D-7", "D-8")
    for decl, ref in zip(te.DECLARATION_IDS, refs):
        assert ui_text.text("UI_MTE_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    s9 = _contract_section("## 9. Result", "## 9A.")
    english = [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)]
    assert english == te.load_artifact()["disclosure"]
    s5 = _contract_section("## 5. Applicability", "## 6.")
    for entry in te.load_artifact()["declarations"]:
        assert "| %s | `%s` | %s |" % (entry["contract_ref"], entry["declaration_id"],
                                       entry["accepted_value"]) in s5


def test_every_key_has_both_languages_and_no_overclaim():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_MTE_[A-Z0-9_]+)": \{', source)
    assert len(keys) == 43
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("you need a gap", "requires a gap of", "the gap must be", "is sufficient",
                  "is adequate", "will not fail", "is safe", "approved", "certified",
                  "has been validated", "verified design", "recommended coefficient",
                  "typical value", "typical coefficient", "for steel", "for aluminium",
                  "for aluminum", "thermal stress is", "the stress is"):
        assert claim not in english, claim
    next_step = ui_text.text("UI_MTE_NEXT_STEP", "en")
    assert "measurement or qualified engineering review" in next_step
    assert "how much movement may need to be accommodated" in next_step
    assert "does not say that any gap, slot, clearance, fit or flexible mounting is needed or enough" \
        in next_step
    arabic = " ".join(ui_text.text(k, "ar") for k in keys)
    for term in ("UNVALIDATED", "NOT EVIDENCE", "α_avg", "L_ref", "ΔT", "ΔL", "1/K", "mm"):
        assert term in arabic, term


def test_no_coefficient_value_is_suggested_anywhere():
    """The one numeric example in the help text is a notation example of the
    unit scale (1 × 10⁻⁶ /K), never a material value."""
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_MTE_[A-Z0-9_]+)": \{', source)
    for key in keys:
        for lang in ("en", "ar"):
            text = ui_text.text(key, lang)
            for number in re.findall(r"0\.0000\d+", text):
                assert number == "0.000001", (key, number)
    help_en = ui_text.text("UI_MTE_HELP_ALPHA_AVG", "en")
    assert "does not suggest, look up or check a value" in help_en


def test_correction_13_is_recorded_in_the_calc_contract():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 13" in body and "## 13L." in body
    section = body[body.index("## 13L."):body.index("## 14.")]
    for phrase in ("exactly thirteen", "`linear_thermal_expansion_coefficient`", "`1/K`",
                   "`dcu:U021`", "`dcu:U002`", "`dcu:U005`", "content version `13`",
                   "`1.12.0`", "2^-50", "2^-52", "`dcu:SU022`", "`dcu:SU023`",
                   "NOT a generic owner policy", "IP-UNRESOLVED", "THERM-01",
                   "No Materials domain exists"):
        assert phrase in section, phrase
    assert "- Correction 13 (§13L) is Owner-authorized" in body
    # §13K is unchanged
    assert "**Methods — exactly twelve:**" in body[body.index("## 13K."):body.index("## 13L.")]


def test_contract_and_stage15_exception_name_this_method():
    contract = CONTRACT.read_text(encoding="utf-8")
    assert "MECHANICAL-FREE-LINEAR-THERMAL-EXPANSION-01" in contract
    s1 = contract[contract.index("## 1. Purpose"):contract.index("## 2.")]
    assert "the ONE inventor-declared Mechanical part" in s1 and "_calc_gate" in s1
    s3 = contract[contract.index("## 3. Method"):contract.index("## 4.")]
    assert "states NO convention of its own" in s3
    assert "An arbitrary length is never substituted for\n   `L_ref`." in s3
    assert "SRC-029" in contract and "IP-UNRESOLVED" in contract
    assert "BLOCKED — RELATIONSHIP AUTHORITY" in contract
    source = (ROOT / "engine" / "subsystem_model.py").read_text(encoding="utf-8")
    assert "MECHANICAL-FREE-LINEAR-THERMAL-EXPANSION-01" in source
    assert "``mechanical:free_linear_thermal_expansion`` v1.0" in source
    assert "No other specialist\nbehaviour is granted by these exceptions." in source


# ==========================================================================
# 6. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_session_link_and_page_on_a_mechanical_root_project(mech):
    c, _aid, sid = mech
    page = _page(c, sid)
    assert "data-mte-link" in page and URL % sid in page
    r = c.get(URL % sid)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    body = r.get_data(as_text=True)
    assert "data-mte-form" in body and not re.search(r"<input[^>]*\schecked", body)
    for role in ("alpha_avg", "L_ref", "delta_T"):
        assert re.search(r'name="value_%s"[^>]*maxlength="64"[^>]*value=""' % role, body)
        assert 'data-mte-field-help="%s"' % role in body
    assert "data-mte-result" not in body and "data-mte-outcome" not in body
    assert body.count("data-mte-declaration=") == 8 and body.count("data-mte-screen=") == 9


def test_post_success_renders_in_the_same_request(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form())
    assert r.status_code == 200 and "Location" not in r.headers
    body = r.get_data(as_text=True)
    assert re.findall(r'data-mte-result-value><bdi dir="ltr">([^<]+)</bdi>',
                      body) == [EXAMPLE + " mm"]
    assert "mechanical:free_linear_thermal_expansion" in body and "UNVALIDATED" in body
    assert "data-mte-exact" in body and "data-mte-rounded" not in body
    assert "data-mte-sign" in body and "data-mte-next-step" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_MTE_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert _norm(ui_text.text("UI_MTE_NEXT_STEP", "en")) in text
    assert _norm(ui_text.text("UI_MTE_EXACT", "en")) in text
    assert re.findall(r'data-mte-echo-value>([^<]*)<', body) == ["0.0000231", "1000", "50"]
    assert "Circular 486" in body and "Special Publication 330" in body
    assert "nbscircular486" in body
    rounded = c.post(URL % sid, data=_form(alpha="0.00001", length="1",
                                           delta_t="0.333333333")).get_data(as_text=True)
    assert "data-mte-exact" in rounded
    rounded = c.post(URL % sid, data=_form(alpha="0.123456789012", length="123456789.123456789",
                                           delta_t="7")).get_data(as_text=True)
    expected = te.format_change(te.exact_change(
        Fraction("0.123456789012"), Fraction("123456789.123456789"), Fraction(7)))
    assert expected[1] is False
    assert _value(rounded) == expected[0] + " mm"
    assert "data-mte-rounded" in rounded and "data-mte-exact" not in rounded


def test_post_cooling_shows_a_negative_change(mech):
    c, _aid, sid = mech
    body = c.post(URL % sid, data=_form(delta_t="-50")).get_data(as_text=True)
    assert _value(body) == "-1.155 mm"
    assert _norm(ui_text.text("UI_MTE_SIGN_NOTE", "en")) in _norm(html.unescape(_content_text(body)))


@pytest.mark.parametrize("over,outcome", [
    ({"alpha": "0"}, "INVALID_NUMERIC_INPUT"),
    ({"length": "1234567890123"}, "INVALID_NUMERIC_INPUT"),
    ({"alpha": "2.3e-5"}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"supports_people": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"free_unrestrained": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"reference_length": ""}}, "NOT_DECLARED"),
])
def test_post_non_success_shows_one_reason_and_no_number(mech, over, outcome):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(**over))
    body = r.get_data(as_text=True)
    assert r.status_code == 200
    assert html.escape(ui_text.text("UI_MTE_OUTCOME_" + outcome, "en"),
                       quote=False) in body
    assert "data-mte-result" not in body and body.count("data-mte-outcome") == 1


def test_malformed_request_is_400_and_echo_is_escaped(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=dict(_form(), unexpected="1"))
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert ui_text.text("UI_MTE_ERR_REQUEST", "en") in body
    assert "data-mte-outcome" not in body and "data-mte-result" not in body
    body = c.post(URL % sid, data=_form(length="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body


def test_electronics_root_project_is_never_offered_or_evaluated(elec, monkeypatch):
    c, _aid, sid = elec
    assert "data-mte-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._mte, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-mte-scope-note" in body
        assert "data-mte-form" not in body and "data-mte-outcome" not in body
    assert not called


def test_csrf_and_authorization_are_enforced(mech):
    _c, _aid, sid = mech
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("mte-other@example.com")
    for client in (other, _new_client()):
        for response in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert response.status_code == 302
            assert "data-mte" not in response.get_data(as_text=True)


@pytest.mark.parametrize("over", [{}, {"alpha": "0"}, {"length": "abc"},
                                  {"delta_t": "-50"}, {"screen": {"children": "yes"}}])
def test_nothing_is_persisted_and_no_project_state_moves(mech, over):
    c, _aid, sid = mech
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_no_safety_signal_report_export_api_or_transfer_surface():
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    start = app_source.index("# MECHANICAL-FREE-LINEAR-THERMAL-EXPANSION-01 — Free Linear Thermal")
    section = app_source[start:app_source.index("# Manufacturing Evidence Capture", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "_THERM01", "_mnf.", "_cap13", "_dcp", "load_project_subsystems",
                   "request.args", "request.values", "request.json"):
        assert banned not in section, banned
    assert section.count("_calc_gate(sid, _mte)") == 3      # eligible / GET / POST
    routes = [r.rule for r in webapp.app.url_map.iter_rules() if "thermal-expansion" in r.rule]
    assert routes == ["/session/<sid>/thermal-expansion"] * 2
    for template in ("deliverable.html", "report.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "mte" not in path.read_text(encoding="utf-8")


def test_existing_calculations_still_render_their_values(mech, elec):
    c, _aid, sid = mech
    body = c.post("/session/%s/support-reactions" % sid,
                  data=_cap13_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">750.0 N</bdi>' in body and '<bdi dir="ltr">250.0 N</bdi>' in body
    body = c.post("/session/%s/natural-frequency" % sid,
                  data=_nf_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">3.18309886184 Hz</bdi>' in body
    c2, _aid2, sid2 = elec
    body = c2.post("/session/%s/temperature-difference" % sid2,
                   data=_therm_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">25.0 K</bdi>' in body


def test_arabic_page_is_rtl_and_isolates_tokens(mech):
    c, _aid, sid = mech
    c.post("/ui-language", data={"lang": "ar"})
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert 'dir="rtl"' in body
    for token in ("α_avg", "L_ref", "ΔT", "ΔL", "1/K", "mm", "K", "UNVALIDATED", "NOT EVIDENCE"):
        assert '(<bdi dir="ltr">%s</bdi>)' % html.escape(token) in body, token
    assert '<bdi dir="ltr">mechanical:free_linear_thermal_expansion</bdi>' in body
    assert '<bdi dir="ltr">%s mm</bdi>' % EXAMPLE in body
    stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
    for item in ui_text.text("UI_MTE_DISCLOSURE", "ar").split("\n\n"):
        assert _norm(item) in _norm(stripped), item[:40]
    assert _norm(ui_text.text("UI_MTE_NEXT_STEP", "ar")) in _norm(stripped)


# ==========================================================================
# 7. the declared Mechanical part of an integrated composition
# ==========================================================================
def test_single_domain_projects_keep_exactly_the_root_rule():
    c, _aid = _client_for("mte-part-single@example.com")
    mech_sid = _start(c, {"idea": SEED, "domain_confirm": MECH})
    elec_sid = _start(c, ELEC_FORM)
    assert webapp._calc_gate(mech_sid, te) == (True, None)
    assert webapp._calc_gate(elec_sid, te) == (False, None)
    assert "data-mte-link" in _page(c, mech_sid)
    assert "data-mte-link" not in _page(c, elec_sid)
    body = c.post(URL % mech_sid, data=_form()).get_data(as_text=True)
    assert _value(body) == EXAMPLE + " mm" and "data-mte-part" not in body
    body = c.post(URL % elec_sid, data=_form()).get_data(as_text=True)
    assert "data-mte-form" not in body and _value(body) is None


@pytest.mark.parametrize("focus", (ELEC, MECH))
def test_integrated_mechanical_part_is_offered_in_either_focus(focus):
    c, _aid = _client_for("mte-part-focus-%s@example.com" % focus)
    sid = _integrated(c, focus)
    eligible, part = webapp._calc_gate(sid, te)
    assert eligible and part.domain == MECH
    assert part.display_name == PARTS["mech_part_name"]
    assert webapp._mte_link_offered(sid) is True
    assert "data-mte-link" in _page(c, sid)
    get_body = c.get(URL % sid).get_data(as_text=True)
    assert "data-mte-form" in get_body
    assert _part_line(get_body, "mte") == PARTS["mech_part_name"]
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) == EXAMPLE + " mm"
    assert _part_line(body, "mte") == PARTS["mech_part_name"]
    assert PARTS["elec_part_name"] not in body
    assert "UNVALIDATED" in body


def test_three_part_composition_names_only_the_mechanical_part():
    c, _aid = _client_for("mte-part-three@example.com")
    sid = _integrated(c, ELEC, **CTRL)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _part_line(body, "mte") == PARTS["mech_part_name"]
    assert CTRL["ctrl_part_name"] not in body and PARTS["elec_part_name"] not in body


@pytest.mark.parametrize("sql", (
    "UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0",
    "DELETE FROM project_subsystems WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET display_name = ' padded' WHERE subsystem_seq = 0",
    "UPDATE project_subsystems SET subsystem_seq = 7 WHERE subsystem_seq = 0",
))
def test_corrupt_composition_grants_nothing(elec_focus, monkeypatch, sql):
    c, sid = elec_focus
    _corrupt(sql)
    calls = _owner_spy(monkeypatch)
    evaluated = []
    monkeypatch.setattr(webapp._mte, "evaluate", lambda *a, **k: evaluated.append(1))
    assert webapp._calc_gate(sid, te) == (False, None)
    assert webapp._mte_link_offered(sid) is False
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-mte-scope-note" in body
        assert "data-mte-form" not in body and "data-mte-part" not in body
        assert _value(body) is None and "data-mte-outcome" not in body
    assert not evaluated and not calls


def test_unreadable_composition_grants_nothing(elec_focus, monkeypatch):
    c, sid = elec_focus

    def broken(_sid):
        raise sqlite3.OperationalError("disk I/O error")
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", broken)
    calls = _owner_spy(monkeypatch)
    assert webapp._calc_gate(sid, te) == (False, None)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) is None and "data-mte-form" not in body
    assert not calls


def test_missing_or_invalid_composition_keeps_only_the_root_rule(monkeypatch):
    c, _aid = _client_for("mte-part-missing@example.com")
    elec_sid = _integrated(c, ELEC)
    mech_sid = _integrated(c, MECH)
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", lambda _sid: ())
    assert webapp._calc_gate(elec_sid, te) == (False, None)
    assert webapp._calc_gate(mech_sid, te) == (True, None)      # root rule only
    body = c.post(URL % mech_sid, data=_form()).get_data(as_text=True)
    assert _value(body) == EXAMPLE + " mm" and "data-mte-part" not in body


def test_the_request_can_never_supply_a_part_or_domain():
    c, _aid = _client_for("mte-part-request@example.com")
    elec_sid = _start(c, ELEC_FORM)
    for extra in ({"part_domain": MECH}, {"subsystem_id": "sub-" + "0" * 32},
                  {"confirmed_domain": MECH}, {"part": "mechanical"}):
        body = c.post(URL % elec_sid, data=dict(_form(), **extra)).get_data(as_text=True)
        assert "data-mte-form" not in body and _value(body) is None


def test_numbers_and_owner_requests_are_identical_irrespective_of_path(monkeypatch):
    c, _aid = _client_for("mte-part-identical@example.com")
    root = _start(c, {"idea": SEED, "domain_confirm": MECH})
    part = _integrated(c, ELEC)
    calls = _owner_spy(monkeypatch)
    bodies = [c.post(URL % sid, data=_form(alpha="0.0000172", length="640.25",
                                           delta_t="-35.5")).get_data(as_text=True)
              for sid in (root, part)]
    expected = te.format_change(te.exact_change(
        Fraction("0.0000172"), Fraction("640.25"), Fraction("-35.5")))[0] + " mm"
    assert [_value(b) for b in bodies] == [expected] * 2
    (req_root, res_root), (req_part, res_part) = calls
    assert req_root == req_part == {
        "method_id": method.METHOD_ID, "method_version": "1.0",
        "inputs": {"alpha_avg": {"value": 0.0000172, "unit": "1/K"},
                   "L_ref": {"value": 640.25, "unit": "mm"},
                   "delta_T": {"value": -35.5, "unit": "K"}},
        "subject_ref": None}
    assert res_root["result_identity"] == res_part["result_identity"]
    assert res_part["outputs"]["delta_L"]["unit"] == "mm"


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_attribution_is_escaped_isolated_and_bilingual(lang):
    c, _aid = _client_for("mte-part-hostile-%s@example.com" % lang)
    sid = _integrated(c, ELEC, mech_part_name=HOSTILE)
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "<script>alert" not in body
    raw_name = _part_line(body, "mte")
    assert raw_name is not None and "&lt;script&gt;" in raw_name
    assert html.unescape(raw_name) == HOSTILE
    assert '<bdi dir="auto" data-mte-part-name>' in body
    stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
    for key in ("UI_CAP13_PART_LABEL", "UI_CAP13_PART_NOTE", "UI_MTE_SCOPE_NOTE"):
        assert ui_text.text(key, lang) in stripped, key
    if lang == "ar":
        assert 'dir="rtl"' in body
        assert '(<bdi dir="ltr">UNVALIDATED</bdi>)' in body
    assert '<bdi dir="ltr">%s mm</bdi>' % EXAMPLE in body


def test_scope_wording_names_the_part_and_carries_no_applicability_claim():
    en = ui_text.text("UI_MTE_SCOPE_NOTE", "en")
    assert "declared Mechanical part" in en
    assert "changes length with temperature" in en
    assert "free-expansion model applies" in en
    assert en.startswith("This optional calculation") and "Neither" in en
    for word in ("is suitable", "is safe", "is adequate", "approved", "compatible"):
        assert word not in en.lower(), word
    assert "الميكانيكي المصرّح به" in ui_text.text("UI_MTE_SCOPE_NOTE", "ar")
