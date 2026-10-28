# -*- coding: utf-8 -*-
"""Electrical / Electronics - DC Resistive Load Power, Slice 1 (directly owning tests).

DC-RESISTIVE-LOAD-POWER-01. The shared deterministic calculation / units owner
after the bounded seventh admission of calc/units Correction 07 (§13F); the ONE
method ``electrical:dc_resistive_load_power`` 1.0
(``engine/dc_resistive_load_power_method.py``) and its ONE consumer
(``engine/dc_resistive_load_power.py`` + the request-local page).

Scientific reference: the power a resistive element absorbs, P = V x I with
I = V / R (DOE-HDBK-1011/1-92, recorded as electronics_electrical:PR004), so
P = V**2 / R. The numerical tests use an INDEPENDENT decimal reference: every
expected power and every expected display is formed with ``decimal.Decimal``
from the typed decimal strings, never from the consumer's or the adapter's own
arithmetic. Synthetic data.
"""
import copy
import hashlib
import html
import json
import math
import random
import re
from decimal import Decimal, Context, ROUND_HALF_EVEN
from fractions import Fraction
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import dc_resistive_load_power as dcp
from engine import dc_resistive_load_power_method as method
from engine import dc_resistive_load_current_method as current_method
from engine import cap13_static_reactions_method as cap13_method
from engine import cap13_planar_moment_method as moment_method
from engine import cap13_rotational_load_method as rotational_method
from engine import therm01_conduction_method as therm_method
from engine import tmp36_nominal_temperature_method as tmp36_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _owner_spy, MECH, ELEC)
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_therm01_temperature_difference import _form as _therm_form
from tests.test_cap13_planar_moment import _form as _moment_form
from tests.test_cap13_rotational_load import _form as _rotational_form
from tests.test_tmp36_nominal_temperature import _form as _tmp36_form
from tests.test_dc_resistive_load_current import _form as _current_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "ELECTRICAL_DC_RESISTIVE_LOAD_POWER_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
URL = "/session/%s/dc-load-power"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
OTHER_BINDINGS = (
    dc.bind_method(cap13_method.METHOD_ID, "1.0", cap13_method.evaluate),
    dc.bind_method(therm_method.METHOD_ID, "1.0", therm_method.evaluate),
    dc.bind_method(moment_method.METHOD_ID, "1.0", moment_method.evaluate),
    dc.bind_method(rotational_method.METHOD_ID, "1.0", rotational_method.evaluate),
    dc.bind_method(tmp36_method.METHOD_ID, "1.0", tmp36_method.evaluate),
    dc.bind_method(current_method.METHOD_ID, "1.0", current_method.evaluate))
# The reference vectors (V, Ω -> W).
REFERENCE = (("12", "24", "6"), ("5", "10", "2.5"), ("230", "52.9", "1000"))
DECIMAL_BOUND = Fraction(1, 2 ** 50)
PROVEN_WORST_CASE = Fraction(40000001, 10000000) * Fraction(1, 2 ** 53)
# The content-version-6 records (quantity kinds, unit records, source-use
# policies and the six method records), pinned by digest: Correction 07 only
# appends after them.
V6_RECORDS_DIGEST = "34f3408b3f929021bb06e75838fcca9e5828f04fd67b35a99849483781dcdc52"


# --------------------------------------------------------------------------
# helpers: the independent decimal reference
# --------------------------------------------------------------------------
_EXACT = Context(prec=200, rounding=ROUND_HALF_EVEN)
_TWELVE = Context(prec=12, rounding=ROUND_HALF_EVEN)


def _reference(v, r):
    """The exact V**2 / R as a Fraction, from Decimal alone."""
    voltage = Fraction(Decimal(v))
    return voltage * voltage / Fraction(Decimal(r))


def _reference_display(v, r):
    """The expected (text, exact) display, from Decimal alone: V**2 / R
    correctly rounded to 12 significant digits (half to even), trailing zeros
    removed, plain for 1e-6 <= P < 1e12 and 'm × 10^e' otherwise."""
    if Decimal(v) == 0:
        return "0", True
    square = _EXACT.multiply(Decimal(v), Decimal(v))          # exact: <= 36 digits
    rounded = _TWELVE.divide(square, Decimal(r))
    exact = Fraction(rounded) == _reference(v, r)
    magnitude = rounded.normalize(_EXACT)
    exponent = magnitude.adjusted()
    if -6 <= exponent <= 11:
        text = format(magnitude, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
    else:
        digits = magnitude.as_tuple().digits
        mantissa = str(digits[0]) + ("." + "".join(map(str, digits[1:]))
                                     if len(digits) > 1 else "")
        text = "%s × 10^%d" % (mantissa, exponent)
    return text, exact


def _request(v=12.0, r=24.0, units=("V", "Ω"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"v_load": {"value": v, "unit": units[0]},
                      "r_load": {"value": r, "unit": units[1]}},
           "subject_ref": None}
    req.update(over)
    return req


def _p(result):
    return result["outputs"]["p_load"]["value"]


def _failure(result):
    return (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def _form(v="12", r="24", decl=None, screen=None):
    form = {dcp.DECLARATION_FIELD % d: dcp.ANSWER_APPLIES for d in dcp.DECLARATION_IDS}
    form.update({dcp.SCREEN_FIELD % s: dcp.SCREEN_NO for s in dcp.SCREEN_ITEMS})
    form[dcp.VALUE_FIELD % "v_load"] = v
    form[dcp.VALUE_FIELD % "r_load"] = r
    for key, value in (decl or {}).items():
        form[dcp.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[dcp.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = dcp.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return dcp.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _method_artifact():
    return json.loads(dcp.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data):
    target = tmp_path / "a.json"
    target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return target


def _value(body):
    marker = 'data-dcp-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def _check_against_reference(v, r):
    """One typed pair through the whole consumer: success, the owner result
    within the decimal bound, the display equal to the independent reference."""
    evaluation = _evaluate(v=v, r=r)
    assert evaluation["outcome"] == dcp.OUTCOME_SUCCESS, (v, r)
    reference = _reference(v, r)
    produced = _p(evaluation["result"])
    assert math.copysign(1.0, produced) == 1.0, (v, r)          # never negative, no -0
    if reference == 0:
        assert produced == 0.0
    else:
        error = abs(Fraction(produced) - reference) / reference
        assert error <= PROVEN_WORST_CASE < DECIMAL_BOUND, (v, r)
        assert produced > 0
    assert (evaluation["display_value"], evaluation["display_exact"]) \
        == _reference_display(v, r), (v, r)
    assert evaluation["power"] == reference
    return evaluation


@pytest.fixture
def elec():
    c, aid = _client_for("dcp-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def mech():
    c, aid = _client_for("dcp-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": MECH})


# ==========================================================================
# 1. the reference vectors and the passive sign convention
# ==========================================================================
@pytest.mark.parametrize("v,r,expected", REFERENCE)
def test_reference_vectors_at_owner_adapter_and_consumer(v, r, expected):
    produced = method.evaluate(float(v), float(r))["p_load"]
    assert Fraction(produced) == _reference(v, r) or abs(
        Fraction(produced) - _reference(v, r)) <= _reference(v, r) * Fraction(1, 2 ** 52)
    result = dc.execute(BINDING, _request(float(v), float(r)))
    assert result["state"] == dc.STATE_SUCCESS and _p(result) == produced
    evaluation = _check_against_reference(v, r)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (expected, True)


@pytest.mark.parametrize("v,r", [("-12", "24"), ("-5", "10"), ("-1", "3"),
                                 ("-0.000000001", "999999999999.999999999"),
                                 ("-999999999.999999999", "0.000000001")])
def test_negative_voltage_gives_the_same_nonnegative_power(v, r):
    negative = _check_against_reference(v, r)
    positive = _check_against_reference(v.lstrip("-"), r)
    assert negative["display_value"] == positive["display_value"]
    assert _p(negative["result"]) == _p(positive["result"]) > 0
    assert method.evaluate(-float(Fraction(v.lstrip("-"))), float(Fraction(r))) \
        == method.evaluate(float(Fraction(v.lstrip("-"))), float(Fraction(r)))


@pytest.mark.parametrize("v", ["0", "-0", "0.000", "-0.000000000", "000000000"])
def test_zero_voltage_gives_exactly_positive_zero_power(v):
    evaluation = _check_against_reference(v, "47")
    assert evaluation["display_value"] == "0" and evaluation["display_exact"] is True
    produced = _p(evaluation["result"])
    assert produced == 0.0 and math.copysign(1.0, produced) == 1.0


def test_negative_zero_at_the_adapter_and_owner_is_positive_zero():
    for v in (-0.0, 0.0):
        out = method.evaluate(v, 3.0)["p_load"]
        assert out == 0.0 and math.copysign(1.0, out) == 1.0
        result = dc.execute(BINDING, _request(v, 3.0))
        assert math.copysign(1.0, _p(result)) == 1.0


# ==========================================================================
# 2. exact and rounded results; the display
# ==========================================================================
@pytest.mark.parametrize("v,r,display,exact", [
    ("2", "4", "1", True), ("3.3", "1100", "0.0099", True),
    ("9", "0.001", "81000", True), ("1", "8", "0.125", True),
    ("1", "3", "0.333333333333", False), ("2", "3", "1.33333333333", False),
    ("10", "7", "14.2857142857", False), ("1", "0.000000003", "333333333.333", False),
    ("999999999.999999999", "1", "1 × 10^18", False),
    ("0.1", "0.3", "0.0333333333333", False),
])
def test_exact_and_rounded_results(v, r, display, exact):
    evaluation = _check_against_reference(v, r)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (display, exact)


def test_round_half_to_even_at_twelve_significant_digits():
    assert dcp.format_power(Fraction("0.1234567890125")) == ("0.123456789012", False)
    assert dcp.format_power(Fraction("0.1234567890135")) == ("0.123456789014", False)
    assert dcp.format_power(Fraction("9.9999999999995")) == ("10", False)
    assert dcp.format_power(Fraction("9.999999999994")) == ("9.99999999999", False)
    assert dcp.format_power(Fraction(5, 2)) == ("2.5", True)
    assert dcp.format_power(Fraction(0)) == ("0", True)
    with pytest.raises(TypeError):
        dcp.format_power(2.5)


def test_tiny_and_large_powers_are_never_shown_as_zero_or_truncated():
    assert dcp.format_power(Fraction(1, 10 ** 6)) == ("0.000001", True)
    assert dcp.format_power(Fraction(1, 10 ** 7)) == ("1 × 10^-7", True)
    assert dcp.format_power(Fraction(10 ** 11)) == ("100000000000", True)
    assert dcp.format_power(Fraction(10 ** 12)) == ("1 × 10^12", True)
    for value in (Fraction(1, 10 ** 30), Fraction(7, 10 ** 25), Fraction(10 ** 27)):
        text, _exact = dcp.format_power(value)
        assert text != "0" and "10^" in text


@pytest.mark.parametrize("v,r", [
    ("0.000000001", "999999999999.999999999"),       # smallest P ~ 1e-30
    ("999999999.999999999", "0.000000001"),          # largest P ~ 1e27
    ("-999999999.999999999", "0.000000001"),
    ("0.000000001", "0.000000001"), ("999999999", "999999999999"),
    ("1.000000001", "3"), ("0.1", "0.3"),
])
def test_representation_limits_are_calculated_and_representable(v, r):
    evaluation = _check_against_reference(v, r)
    produced = _p(evaluation["result"])
    assert math.isfinite(produced) and produced > 0.0
    assert Fraction(1, 10 ** 31) < Fraction(produced) < Fraction(10 ** 28)


def test_random_admitted_decimals_against_the_independent_reference():
    rng = random.Random(20261026)
    worst = Fraction(0)
    for _ in range(600):
        iv = rng.randint(0, 10 ** rng.randint(1, 9) - 1)
        fv = rng.randint(0, 10 ** 9 - 1)
        v = "%s%d.%09d" % ("-" if rng.random() < 0.4 else "", iv, fv)
        ir = rng.randint(0, 10 ** rng.randint(1, 12) - 1)
        fr = rng.randint(1, 10 ** 9 - 1)
        r = "%d.%s" % (ir, ("%09d" % fr).rstrip("0") or "0")
        if Fraction(r) <= 0:
            continue
        evaluation = _check_against_reference(v, r)
        reference = _reference(v, r)
        if reference:
            worst = max(worst, abs(Fraction(_p(evaluation["result"])) - reference) / reference)
    assert worst <= PROVEN_WORST_CASE


def test_the_error_bound_proof():
    u = Fraction(1, 2 ** 53)
    assert (1 + u) ** 3 / (1 - u) - 1 < PROVEN_WORST_CASE < DECIMAL_BOUND
    assert 1 - (1 - u) ** 3 / (1 + u) < PROVEN_WORST_CASE
    assert DECIMAL_BOUND == 8 * u and dcp.DECIMAL_REFERENCE_BOUND == DECIMAL_BOUND
    assert method.RELATIVE_ERROR_BOUND == 2 * u


# ==========================================================================
# 3. positive resistance; the adapter's binary acceptance
# ==========================================================================
@pytest.mark.parametrize("r", ["0", "-0", "0.000000000", "-1", "-0.000000001", "-24"])
def test_non_positive_resistance_is_refused_before_the_owner(r, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(r=r)
    assert evaluation["outcome"] == dcp.RESISTANCE_NOT_POSITIVE
    assert evaluation["display_value"] is None and evaluation["result"] is None
    assert not calls


@pytest.mark.parametrize("r", [0.0, -0.0, -1.0, -1e308])
def test_non_positive_resistance_is_declined_by_the_owner(r):
    result = dc.execute(BINDING, _request(12.0, r))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None)


@pytest.mark.parametrize("v,r", [(1e200, 1e-200), (-1e300, 1.0), (1e-200, 1e200),
                                 (5e-324, 2.0), (-1e-170, 1e10)])
def test_overflow_and_underflow_fail_closed_in_the_adapter(v, r):
    with pytest.raises(ArithmeticError):
        method.evaluate(v, r)
    assert _failure(dc.execute(BINDING, _request(v, r)))


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), "1", None, True])
def test_non_finite_and_non_numeric_inputs_are_refused(value):
    result = dc.execute(BINDING, _request(value, 24.0))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, None)


def test_adapter_refuses_non_float_or_non_positive_arguments():
    for args in ((12, 24.0), (12.0, 24), ("12", 24.0), (12.0, 0.0), (12.0, -1.0),
                 (float("nan"), 1.0), (1.0, float("inf"))):
        with pytest.raises(ArithmeticError):
            method.evaluate(*args)


def test_adapter_results_are_correctly_rounded_and_nonnegative():
    rng = random.Random(9)
    for _ in range(500):
        v = rng.uniform(-1e9, 1e9)
        r = 10 ** rng.uniform(-9, 12)
        exact = Fraction(v) * Fraction(v) / Fraction(r)
        produced = method.evaluate(v, r)["p_load"]
        assert produced == float(exact) and produced >= 0.0        # one correct rounding
        assert abs(Fraction(produced) - exact) <= exact * Fraction(1, 2 ** 53)


# ==========================================================================
# 4. the input grammar and strict capture
# ==========================================================================
@pytest.mark.parametrize("v,r", [
    ("+12", "24"), ("1e3", "24"), (" 12", "24"), ("1,5", "24"), ("١٢", "24"),
    ("12.", "24"), (".5", "24"), ("--1", "24"), ("inf", "24"), ("nan", "24"),
    ("1.0000000001", "24"), ("1234567890", "24"), ("12V", "24"), ("", "24"),
    ("12", ""), ("12", "24Ω"), ("12", "1e2"), ("12", "1234567890123"),
    ("12", "0.0000000001"), ("12", "+24"), ("−12", "24"), ("1" * 65, "24"),
])
def test_malformed_values_are_invalid_and_never_reach_the_owner(v, r, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(v=v, r=r)
    assert evaluation["outcome"] == dcp.INVALID_NUMERIC_INPUT, (v, r)
    assert evaluation["display_value"] is None and not calls


def test_strict_capture_refuses_duplicates_unknown_fields_and_bad_answers():
    good = {k: [v] for k, v in _form().items()}
    assert dcp.capture_form(good) is not None
    for bad in (dict(good, **{dcp.VALUE_FIELD % "v_load": ["12", "13"]}),
                dict(good, **{dcp.DECLARATION_FIELD % "resistive_load":
                              ["applies", "does_not_apply"]}),
                dict(good, unexpected=["1"]),
                dict(good, **{dcp.SCREEN_FIELD % "safety_function": ["maybe"]}),
                dict(good, **{dcp.DECLARATION_FIELD % "absorbed_power_convention": ["yes"]}),
                dict(good, **{dcp.VALUE_FIELD % "p_load": ["6"]}),
                dict(good, **{"decl_sign_convention": ["applies"]}), [], None):
        assert dcp.capture_form(bad) is None
    missing = {k: v for k, v in good.items()
               if k != dcp.DECLARATION_FIELD % "absorbed_power_convention"}
    captured = dcp.capture_form(missing)
    assert captured is not None
    assert dcp.evaluate(captured, BINDING)["outcome"] == dcp.NOT_DECLARED


# ==========================================================================
# 5. the owner: inventory, units, bindings and integrity (Correction 07)
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["outputs"] == {"p_load": {"value": 6.0, "unit": "W",
                                            "provenance": "CALCULATED"}}
    assert [u["record_id"] for u in result["unit_records"]] == [
        "dcu:U003", "dcu:U011", "dcu:U012"]
    assert [q["source_ref"] for q in result["source_qualification"]] == ["DOE-PWR-S1"]
    assert result["source_qualification"][0]["source_use_policy_ref"] == "dcu:SU013"
    assert result["validation_status"] == "UNVALIDATED"
    assert (result["artifact_version"], result["implementation_version"]) == ("10", "1.9.0")
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_units_and_condition_are_unchanged_but_one_method():
    assert ("electrical:dc_resistive_load_power", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 10
    assert len(dc.ADMITTED_QUANTITY_KINDS) == 15 and len(dc.ADMITTED_UNIT_TOKENS) == 17
    assert dc.KIND_TOKEN_EXCEPTIONS == {"voltage": frozenset({"mV", "V"}),
                                        "time": frozenset({"s", "h"})}
    assert dc._CONDITIONS == ("greater_than_zero", "less_than_zero",
                              "within_zero_and_role")
    record = _record(dc.load_artifact())
    assert record["applicability"] == [
        {"role": "r_load", "condition": "greater_than_zero", "bound_role": None}]
    assert record["result_range"] == []
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"] + record["output_roles"]] == [
        ("v_load", "voltage", "V"), ("r_load", "electric_resistance", "Ω"),
        ("p_load", "power", "W")]


@pytest.mark.parametrize("units,reason", [
    (("mV", "Ω"), dc.UNIT_NOT_ADMITTED), (("A", "Ω"), dc.UNIT_NOT_ADMITTED),
    (("V", "W"), dc.UNIT_NOT_ADMITTED), (("W", "Ω"), dc.UNIT_NOT_ADMITTED),
    (("v", "Ω"), dc.UNKNOWN_UNIT), (("kV", "Ω"), dc.UNKNOWN_UNIT),
    (("V", "Ω"), dc.UNKNOWN_UNIT), (("V", "kΩ"), dc.UNKNOWN_UNIT),
    (("mW", "Ω"), dc.UNKNOWN_UNIT), (("V", "kW"), dc.UNKNOWN_UNIT),
])
def test_units_are_exact_with_no_alias_or_conversion(units, reason):
    result = dc.execute(BINDING, _request(units=units))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, reason, None)


def test_each_binding_executes_only_its_own_method():
    for binding in OTHER_BINDINGS:
        assert dc.execute(binding, _request())["reason"] == dc.OPERATION_NOT_ADMITTED
    swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, current_method.evaluate)
    assert _failure(dc.execute(swapped, _request()))
    assert dc.execute(dc.bind_method(method.METHOD_ID, "2.0", method.evaluate),
                      _request())["reason"] == dc.VERSION_MISMATCH


def test_app_wires_one_immutable_binding_per_method():
    assert webapp._DC_LOAD_POWER_BINDING.adapter_identity \
        == "engine.dc_resistive_load_power_method.evaluate"
    with pytest.raises(AttributeError):
        webapp._DC_LOAD_POWER_BINDING.method_id = "x"
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 10
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("dc_resistive_load_power_method", "engine.dc_resistive",
                   "electrical_content_config", "import fractions", "decimal",
                   "sqlite", "**2", "** 2"):
        assert banned not in owner_source.lower(), banned


def _owner_tamper(data, name):
    record = _record(data)
    if name == "eighth_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "electrical:dc_resistive_load_energy"
        data["methods"].append(extra)
    elif name == "output_kind":
        record["output_roles"][0]["quantity_kind"] = "electric_current"
    elif name == "output_unit":
        record["output_roles"][0]["unit_token"] = "A"
    elif name == "policy_unresolved":
        record["source_qualification"][0]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "second_power_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "W"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "mW"
        data["unit_records"].append(extra)
    elif name == "unknown_condition":
        record["applicability"][0]["condition"] = "non_negative"
    elif name == "basis":
        data["source_use_policies"][-1]["inspection_basis"] = "EXECUTOR"
    return data


@pytest.mark.parametrize("name", ["eighth_method", "output_kind", "output_unit",
                                  "policy_unresolved", "second_power_unit",
                                  "unknown_condition", "basis"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), name))
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    assert _failure(dc.execute(BINDING, _request(), artifact_path=path))


def test_owner_v6_records_are_unchanged_by_the_seventh_admission():
    data = dc.load_artifact()
    assert data["artifact_version"] == "10"
    v6 = {"quantity_kinds": data["quantity_kinds"][:12],
          "unit_records": data["unit_records"][:13],
          "source_use_policies": data["source_use_policies"][:12],
          "methods": data["methods"][:6]}
    canonical = json.dumps(v6, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(canonical.encode()).hexdigest() == V6_RECORDS_DIGEST
    assert [p["record_id"] for p in data["source_use_policies"][12:13]] == ["dcu:SU013"]
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "DOE-PWR-S1 only" in policies["dcu:SU013"]["inspected_content"]
    assert "dcu:SU012 (DC resistive load current) is not extended" \
        in policies["dcu:SU013"]["inspection_reference"]
    assert "for the THERM-01 method" in policies["dcu:SU003"]["inspected_content"]


# ==========================================================================
# 6. the method artifact and the consumer
# ==========================================================================
def test_method_artifact_loads_with_provenance_and_ip_boundary():
    data = dcp.load_artifact()
    by_id = {r["record_id"]: r for r in data["sources"]}
    source = by_id["DOE-PWR-S1"]
    for phrase in ("E = I x R", "handbook page 14", "P = I x E", "handbook page 16",
                   "ARCHIVE - Canceled", "electronics_electrical:PR004",
                   "Not re-inspected by the executor",
                   "not claimed that DOE printed them"):
        assert phrase in source["inspected_content"], phrase
    assert "no textbook material is reproduced" in source["paraphrase_only_limitation"]
    policy = by_id["dcpower:SU001"]
    for phrase in ("not a legal opinion", "electronics_electrical:PR006", "public domain",
                   "EG&G Idaho", "no blanket claim", "not broadened"):
        assert phrase in policy["inspected_content"], phrase
    watt = by_id["NIST-W-S1"]
    assert "electronics_electrical:PR005" in watt["inspected_content"]
    assert "dcu:SU003 is not extended" in watt["inspected_content"]
    assert by_id["dcpower:SU002"]["source_use_policy_ref"] == "dcpower:SU002"
    assert "not claimed to print this combined form or the passive sign convention" \
        in data["method"]["derivation"]


def test_no_openstax_material_or_pack_change():
    for path in (dcp.ARTIFACT_PATH, CONTRACT):
        text = path.read_text(encoding="utf-8")
        assert "openstax.org" not in text.lower()
    pack = (ROOT / "domains" / "electronics_electrical" / "domain.json").read_text(encoding="utf-8")
    assert "dc_resistive_load_power" not in pack and "dcpower:" not in pack
    provenance = json.loads((ROOT / "domains" / "domain_provenance.json")
                            .read_text(encoding="utf-8"))
    records = {r["record_id"]: r for r in provenance["records"]}
    assert records["electronics_electrical:PR004"]["notes"].endswith(
        "Bounded reference relationships only — no project-specific calculation and no "
        "applicability inference.")


@pytest.mark.parametrize("mutate", [
    lambda d: d["declarations"][3].__setitem__("accepted_value", "any power"),
    lambda d: d["declarations"][0].__setitem__("refusal", "NOT_DECLARED"),
    lambda d: d["numeric_domain"]["roles"][2].__setitem__("unit_token", "mW"),
    lambda d: d["numeric_domain"]["roles"][2].__setitem__("quantity_kind", "temperature_difference"),
    lambda d: d["method"].__setitem__("executed_form", "p_load = v_load * abs(v_load) / r_load"),
    lambda d: d["disclosure"].pop(),
    lambda d: d["disclosure"].__setitem__(5, "The load will not overheat."),
    lambda d: d["sources"][2].__setitem__("source_use_policy_ref", "dcload:SU001"),
    lambda d: d["sources"].pop(),
    lambda d: d.__setitem__("artifact_version", "2"),
])
def test_method_artifact_tamper_is_knowledge_unavailable(mutate, monkeypatch):
    data = _method_artifact()
    mutate(data)
    with pytest.raises(dcp.DcPowerKnowledgeError):
        dcp.validate_artifact(data)
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    result = dcp.evaluate(_captured(), BINDING, artifact=data)
    assert result["outcome"] == dcp.KNOWLEDGE_UNAVAILABLE and not calls
    assert result["display_value"] is None and result["power"] is None


def test_unreadable_artifacts_give_no_number(tmp_path, monkeypatch):
    result = dcp.evaluate(_captured(), BINDING, owner_artifact_path=tmp_path / "none.json")
    assert (result["outcome"], result["owner_state"], result["owner_reason"]) == (
        dcp.KNOWLEDGE_UNAVAILABLE, dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE)
    assert result["display_value"] is None
    monkeypatch.setattr(dcp, "ARTIFACT_PATH", tmp_path / "missing.json")
    assert _evaluate()["outcome"] == dcp.KNOWLEDGE_UNAVAILABLE


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(decl={"steady_state_dc": ""}, screen={"safety_function": "yes"},
                     v="x", r="0")["outcome"] == dcp.NOT_DECLARED
    assert _evaluate(screen={"fire_or_overheating": "yes"},
                     decl={"resistive_load": "does_not_apply"},
                     v="x")["outcome"] == dcp.ENGINEERING_REVIEW_REQUIRED
    for item in dcp.SCREEN_ITEMS:
        assert _evaluate(screen={item: "yes"})["outcome"] \
            == dcp.ENGINEERING_REVIEW_REQUIRED, item
    for decl in dcp.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"}, v="x")["outcome"] \
            == dcp.MODEL_NOT_SUPPORTED, decl
    assert _evaluate(v="x", r="0")["outcome"] == dcp.INVALID_NUMERIC_INPUT
    assert _evaluate(r="0")["outcome"] == dcp.RESISTANCE_NOT_POSITIVE
    assert not calls


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, dcp.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, dcp.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, dcp.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, dcp.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, dcp.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, dcp.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, dcp.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, dcp.UNMAPPED_OWNER_OUTCOME),
    (dc.STATE_REFUSAL, dc.OPERATION_NOT_ADMITTED, dcp.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome, monkeypatch):
    monkeypatch.setattr(dc, "execute", lambda *a, **k: {
        "state": state, "reason": reason, "outputs": None})
    result = _evaluate()
    assert (result["outcome"], result["owner_state"], result["owner_reason"]) \
        == (outcome, state, reason)
    assert result["result"] is None and result["display_value"] is None


@pytest.mark.parametrize("produced", [6.000001, 5.9999, -6.0, 0.0, -0.0, 6.0 + 2.0 ** -40,
                                      "6", None, float("nan"), float("inf")])
def test_decimal_reference_failure_fails_closed_with_no_number(produced, monkeypatch):
    real = dc.execute

    def tampered(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["p_load"]["value"] = produced
        return result
    monkeypatch.setattr(dc, "execute", tampered)
    result = _evaluate()
    assert result["outcome"] == dcp.KNOWLEDGE_UNAVAILABLE
    assert result["owner_state"] == dc.STATE_SUCCESS          # preserved, not rewritten
    assert result["result"] is None and result["display_value"] is None


def test_zero_must_be_positive_zero_and_only_for_zero_voltage(monkeypatch):
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: dict(
        real(b, r, artifact_path=artifact_path),
        outputs={"p_load": {"value": -0.0, "unit": "W", "provenance": "CALCULATED"}}))
    assert _evaluate(v="0")["outcome"] == dcp.KNOWLEDGE_UNAVAILABLE
    assert dcp.agrees_with_reference(0.0, Fraction(0))
    assert not dcp.agrees_with_reference(-0.0, Fraction(0))
    assert not dcp.agrees_with_reference(1e-300, Fraction(0))
    assert not dcp.agrees_with_reference(0.0, Fraction(1, 10 ** 30))


def test_consumer_sends_the_correctly_rounded_values_and_fixed_units(monkeypatch):
    seen = []
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: (
        seen.append(copy.deepcopy(r)), real(b, r, artifact_path=artifact_path))[1])
    _evaluate(v="-3.3", r="0.1")
    assert seen == [{"method_id": method.METHOD_ID, "method_version": "1.0",
                     "inputs": {"v_load": {"value": float("-3.3"), "unit": "V"},
                                "r_load": {"value": float("0.1"), "unit": "Ω"}},
                     "subject_ref": None}]


def test_requests_are_isolated_and_inputs_not_mutated():
    first = _captured(v="12", r="24")
    before = copy.deepcopy(first)
    a = dcp.evaluate(first, BINDING)
    b = dcp.evaluate(_captured(v="-1", r="3"), BINDING)
    assert first == before
    assert a == dcp.evaluate(_captured(v="12", r="24"), BINDING)
    assert (a["display_value"], b["display_value"]) == ("6", "0.333333333333")


def test_consumer_and_adapter_import_no_other_authority():
    import ast
    for module in (dcp, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        for banned in ("cap13", "therm01", "tmp36", "dc_resistive_load_current",
                       "record_store", "safety_signal", "requests", "urllib", "openai",
                       "web", "flask", "random", "time", "sqlite3", "domain_rules"):
            assert not any(banned == n or n.startswith(banned + ".") or banned in n
                           for n in names if n), (module.__name__, banned)


# ==========================================================================
# 7. EN / AR fidelity and the contracts
# ==========================================================================
def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_english_wording_equals_the_artifact():
    content = dcp.load_artifact()
    assert ui_text.text("UI_DCP_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"]
        assert ui_text.text("UI_DCP_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."
    for entry in content["screen_items"]:
        value = entry["item"]
        assert ui_text.text("UI_DCP_SCREEN_" + entry["item_id"].upper(), "en") \
            == value[0].upper() + value[1:]


def test_arabic_wording_equals_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    assert ui_text.text("UI_DCP_DISCLOSURE", "ar").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$",
                           _contract_section("**A-2", "**A-3"), re.M))
    for decl, ref in dcp.DECLARATIONS:
        assert ui_text.text("UI_DCP_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    screen = dict(re.findall(r"^\| (\w+) \| (.+?) \|$",
                             _contract_section("**A-3", "**A-4"), re.M))
    for item in dcp.SCREEN_ITEMS:
        assert ui_text.text("UI_DCP_SCREEN_" + item.upper(), "ar") == screen[item], item
    s9 = _contract_section("## 9. Result", "## 9A.")
    assert [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)] \
        == dcp.load_artifact()["disclosure"]
    s5 = _contract_section("## 5. Applicability", "## 6.")
    english = dict(re.findall(r"^\| (D-\d) \| `\w+` \| (.+?) \|$", s5, re.M))
    for entry in dcp.load_artifact()["declarations"]:
        assert english[entry["contract_ref"]] == entry["accepted_value"]


def test_every_key_has_both_languages_and_no_thermal_rating_or_safety_claim():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_DCP_[A-Z0-9_]+)": \{', source)
    assert len(keys) >= 40
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("the load is safe", "will not overheat", "temperature will be",
                  "measured by inventorai", "guaranteed", "certified", "has been validated",
                  "recommended", "rated for this power.", "is rated"):
        assert claim not in english, claim
    for phrase in ("not a temperature", "next engineering need", "remain unverified",
                   "did not measure", "not physical limits", "labelled rounded",
                   "never negative"):
        assert phrase in english, phrase


def test_correction_07_is_recorded_and_earlier_sections_unchanged():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 07" in body and "## 13F." in body
    section = _norm(body[body.index("## 13F."):body.index("## 14.")])
    for phrase in ("exactly seven", "`electrical:dc_resistive_load_power`",
                   "Quantity kinds and exact unit tokens: unchanged", "`dcu:U003`",
                   "is not extended", "content version `7`", "`1.6.0`", "`dcu:SU013`",
                   "NOT a generic owner policy", "No consumer imports another",
                   "within a relative `2^-50`", "never a negative zero"):
        assert phrase in section, phrase
    assert "**Methods — exactly six:**" in body[body.index("## 13E."):body.index("## 13F.")]
    assert "- Correction 07 (§13F) is Owner-authorized" in body


def test_method_contract_records_scope_provenance_and_exclusions():
    text = _norm(CONTRACT.read_text(encoding="utf-8"))
    for phrase in ("DOE-HDBK-1011/1-92", "handbook page 14", "handbook page 16",
                   "electronics_electrical:PR004", "electronics_electrical:PR006",
                   "no project-specific calculation", "passive sign convention",
                   "`12 V / 24 Ω = 6 W`", "4.0000001", "Root only", "28-T3",
                   "Representation limits are not physical limits", "labelled exact when",
                   "1 × 10^-30", "never a temperature", "`10^27` W"):
        assert phrase in text, phrase


# ==========================================================================
# 8. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_electronics_root_journey_and_reference_values(elec):
    c, _aid, sid = elec
    assert "data-dcp-link" in _page(c, sid)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-dcp-form" in body and "checked" not in body
    assert "data-dcp-value-note" in body
    for v, r, expected in REFERENCE:
        body = c.post(URL % sid, data=_form(v=v, r=r)).get_data(as_text=True)
        assert _value(body) == "%s W" % expected, (v, r)
        assert 'data-dcp-exactness="exact"' in body
    body = c.post(URL % sid, data=_form(v="-12", r="24")).get_data(as_text=True)
    assert _value(body) == "6 W" and "data-dcp-magnitude" not in body
    body = c.post(URL % sid, data=_form(v="1", r="3")).get_data(as_text=True)
    assert _value(body) == "0.333333333333 W"
    assert 'data-dcp-exactness="rounded"' in body
    assert "data-dcp-not-temperature" in body
    assert "UNVALIDATED" in body and "NOT EVIDENCE" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_DCP_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert "DOE-HDBK-1011/1-92" in body and "NIST" in body
    assert "electrical:dc_resistive_load_power" in body
    assert '<bdi dir="ltr" data-dcp-echo-value>1</bdi>' in body


@pytest.mark.parametrize("over,outcome", [
    ({"r": "0"}, "RESISTANCE_NOT_POSITIVE"),
    ({"r": "-24"}, "RESISTANCE_NOT_POSITIVE"),
    ({"v": "1e3"}, "INVALID_NUMERIC_INPUT"),
    ({"v": ""}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"fire_or_overheating": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"absorbed_power_convention": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"resistive_load": ""}}, "NOT_DECLARED"),
])
def test_non_success_shows_one_reason_and_no_number(elec, over, outcome):
    c, _aid, sid = elec
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert ui_text.text("UI_DCP_OUTCOME_" + outcome, "en") in html.unescape(body)
    assert _value(body) is None
    assert body.count("data-dcp-outcome") == 1 and "data-dcp-result" not in body


def test_mechanical_root_is_not_eligible_but_a_declared_part_is(mech, monkeypatch):
    c, _aid, sid = mech
    assert "data-dcp-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._dcp, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-dcp-scope-note" in body
        assert "data-dcp-form" not in body and _value(body) is None
    # DC-RESISTIVE-LOAD-INTEGRATED-PART-01: on an integrated project with a
    # Mechanical focus the declared Electrical / Electronics part is offered the
    # calculation (tests/test_dc_resistive_load_integrated_part.py)
    c2, _ = _client_for("dcp-part-mech@example.com")
    sid2 = _integrated(c2, MECH)
    assert webapp._dcp_eligible(sid2)
    assert "data-dcp-link" in _page(c2, sid2)
    assert not called
    c3, _ = _client_for("dcp-part-elec@example.com")
    assert webapp._dcp_eligible(_integrated(c3, ELEC))


def test_unreadable_root_domain_grants_nothing(elec, monkeypatch):
    c, _aid, sid = elec

    def broken(_sid):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(webapp, "_cap12_root_domain", broken)
    assert not webapp._dcp_eligible(sid)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-dcp-form" not in body and _value(body) is None


def test_csrf_authorization_and_malformed_requests(elec):
    c, _aid, sid = elec
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("dcp-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302 and "data-dcp" not in r.get_data(as_text=True)
    for bad in (dict(_form(), unexpected="1"),
                dict(_form(), screen_safety_function="maybe"),
                dict(_form(), value_p_load="6")):
        r = c.post(URL % sid, data=bad)
        assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    from werkzeug.datastructures import MultiDict
    r = c.post(URL % sid, data=MultiDict(list(_form().items())
                                         + [(dcp.VALUE_FIELD % "v_load", "13")]))
    assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    body = c.post(URL % sid, data=_form(v="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body
    assert c.get(URL % sid).headers["Cache-Control"] == "no-store"


@pytest.mark.parametrize("over", [{}, {"r": "0"}, {"screen": {"safety_function": "yes"}}])
def test_nothing_is_persisted_and_no_request_leaks_into_the_next(elec, over):
    c, _aid, sid = elec
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(v="7.5", **over))
    body = c.get(URL % sid).get_data(as_text=True)
    assert _snapshot(c) == before
    assert "7.5" not in body and "checked" not in body and _value(body) is None


def test_no_report_export_api_or_safety_surface():
    src = Path(webapp.__file__).read_text(encoding="utf-8")
    start = src.index("# DC-RESISTIVE-LOAD-POWER-01 — DC Resistive Load Power")
    section = src[start:src.index("# DC-RESISTIVE-LOAD-ENERGY-01 —", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "_cap13", "_tmp36", "_dcl.",
                   "load_project_subsystems", "request.args", "cap09",
                   "success_criteria", "redirect("):
        assert banned not in section, banned
    assert section.count("_dcalc.bind_method(") == 1
    assert [r.rule for r in webapp.app.url_map.iter_rules() if "dc-load-power" in r.rule] \
        == ["/session/<sid>/dc-load-power"] * 2
    for template in ("deliverable.html", "report.html", "success_criteria.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "dc-load-power" not in path.read_text(encoding="utf-8").lower()


def test_existing_six_calculations_are_unchanged(mech, elec):
    c, _aid, sid = mech
    body = c.post("/session/%s/support-reactions" % sid, data=_cap13_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">750.0 N</bdi>' in body and '<bdi dir="ltr">250.0 N</bdi>' in body
    body = c.post("/session/%s/planar-moment" % sid, data=_moment_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">1000.0 N·mm</bdi>' in body
    body = c.post("/session/%s/rotational-load" % sid,
                  data=_rotational_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">-1.0 N·m</bdi>' in body
    c2, _aid2, sid2 = elec
    body = c2.post("/session/%s/temperature-difference" % sid2,
                   data=_therm_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">25.0 K</bdi>' in body
    body = c2.post("/session/%s/tmp36-temperature" % sid2,
                   data=_tmp36_form(v_out="750")).get_data(as_text=True)
    assert '<bdi dir="ltr">25.0 °C</bdi>' in body
    body = c2.post("/session/%s/dc-load-current" % sid2,
                   data=_current_form(v="12", r="24")).get_data(as_text=True)
    assert 'data-dcl-result-value><bdi dir="ltr">0.5 A</bdi>' in body


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_arabic_isolation_and_signed_input(elec, lang):
    c, _aid, sid = elec
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form(v="-12", r="24")).get_data(as_text=True)
    assert _value(body) == "6 W"
    assert '<bdi dir="ltr" data-dcp-echo-value>-12</bdi>' in body
    if lang == "ar":
        assert 'dir="rtl"' in body
        isolated = [html.unescape(run)
                    for run in re.findall(r'<bdi dir="ltr">([^<]*)</bdi>', body)]
        for token in ("UNVALIDATED", "NOT EVIDENCE", "DOE-HDBK-1011/1-92", "(Ω)", "(W)"):
            assert any(token in run for run in isolated), token
        assert any(run == "P = V² / R = V × I" for run in isolated)
        stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
        for item in ui_text.text("UI_DCP_DISCLOSURE", "ar").split("\n\n"):
            assert _norm(item) in _norm(stripped), item[:30]
        refusal = c.post(URL % sid, data=_form(r="0")).get_data(as_text=True)
        assert ui_text.text("UI_DCP_OUTCOME_RESISTANCE_NOT_POSITIVE", "ar") \
            in html.unescape(re.sub(r"<[^>]+>", "", refusal))
        assert _value(refusal) is None
