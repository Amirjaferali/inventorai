# -*- coding: utf-8 -*-
"""Electrical / Electronics - DC Resistive Load Current, Slice 1 (directly owning tests).

DC-RESISTIVE-LOAD-CURRENT-01. The shared deterministic calculation / units owner
after the bounded sixth admission of calc/units Correction 06 (§13E); the ONE
method ``electrical:dc_resistive_load_current`` 1.0
(``engine/dc_resistive_load_current_method.py``) and its ONE consumer
(``engine/dc_resistive_load_current.py`` + the request-local page).

Scientific reference: Ohm's law for a resistive element (DOE-HDBK-1011/1-92,
recorded as electronics_electrical:PR004), solved for the current: I = V / R.
The numerical tests use an INDEPENDENT decimal reference: every expected current
and every expected display is formed with ``decimal.Decimal`` from the typed
decimal strings, never from the consumer's or the adapter's own arithmetic.
Synthetic data.
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
from engine import dc_resistive_load_current as dcl
from engine import dc_resistive_load_current_method as method
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

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "ELECTRICAL_DC_RESISTIVE_LOAD_CURRENT_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
URL = "/session/%s/dc-load-current"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
OTHER_BINDINGS = (
    dc.bind_method(cap13_method.METHOD_ID, "1.0", cap13_method.evaluate),
    dc.bind_method(therm_method.METHOD_ID, "1.0", therm_method.evaluate),
    dc.bind_method(moment_method.METHOD_ID, "1.0", moment_method.evaluate),
    dc.bind_method(rotational_method.METHOD_ID, "1.0", rotational_method.evaluate),
    dc.bind_method(tmp36_method.METHOD_ID, "1.0", tmp36_method.evaluate))
# The Owner's reference vectors (V, Ω -> A).
REFERENCE = (("12", "24", "0.5"), ("5", "10", "0.5"))
DECIMAL_BOUND = Fraction(1, 2 ** 51)
PROVEN_WORST_CASE = Fraction(30000001, 10000000) * Fraction(1, 2 ** 53)
# The content-version-5 records (quantity kinds, unit records, source-use
# policies and the five method records), pinned by digest: Correction 06 only
# appends after them.
V5_RECORDS_DIGEST = "339ddd2139c622020d551989fab0875bd790f8a9a8f29584009b578a050cabaf"


# --------------------------------------------------------------------------
# helpers: the independent decimal reference
# --------------------------------------------------------------------------
_EXACT = Context(prec=200, rounding=ROUND_HALF_EVEN)
_TWELVE = Context(prec=12, rounding=ROUND_HALF_EVEN)


def _reference(v, r):
    """The exact quotient as a Fraction, from Decimal alone."""
    return Fraction(Decimal(v)) / Fraction(Decimal(r))


def _reference_display(v, r):
    """The expected (text, exact) display, from Decimal alone: the quotient
    correctly rounded to 12 significant digits (half to even), trailing zeros
    removed, plain for 1e-6 <= |I| < 1e12 and 'm × 10^e' otherwise."""
    if Decimal(v) == 0:
        return "0", True
    rounded = _TWELVE.divide(Decimal(v), Decimal(r))
    exact = Fraction(rounded) == _reference(v, r)
    sign = "-" if rounded < 0 else ""
    magnitude = abs(rounded).normalize(_EXACT)
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
    return sign + text, exact


def _request(v=12.0, r=24.0, units=("V", "Ω"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"v_load": {"value": v, "unit": units[0]},
                      "r_load": {"value": r, "unit": units[1]}},
           "subject_ref": None}
    req.update(over)
    return req


def _i(result):
    return result["outputs"]["i_load"]["value"]


def _failure(result):
    return (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def _form(v="12", r="24", decl=None, screen=None):
    form = {dcl.DECLARATION_FIELD % d: dcl.ANSWER_APPLIES for d in dcl.DECLARATION_IDS}
    form.update({dcl.SCREEN_FIELD % s: dcl.SCREEN_NO for s in dcl.SCREEN_ITEMS})
    form[dcl.VALUE_FIELD % "v_load"] = v
    form[dcl.VALUE_FIELD % "r_load"] = r
    for key, value in (decl or {}).items():
        form[dcl.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[dcl.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = dcl.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return dcl.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _method_artifact():
    return json.loads(dcl.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data):
    target = tmp_path / "a.json"
    target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return target


def _value(body):
    marker = 'data-dcl-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _magnitude(body):
    marker = 'data-dcl-magnitude><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def _check_against_reference(v, r):
    """One typed pair through the whole consumer: success, the owner result
    within the decimal bound, the display equal to the independent reference."""
    evaluation = _evaluate(v=v, r=r)
    assert evaluation["outcome"] == dcl.OUTCOME_SUCCESS, (v, r)
    reference = _reference(v, r)
    produced = _i(evaluation["result"])
    if reference == 0:
        assert produced == 0.0
    else:
        error = abs(Fraction(produced) - reference) / abs(reference)
        assert error <= PROVEN_WORST_CASE < DECIMAL_BOUND, (v, r)
        assert (produced < 0) == (reference < 0), (v, r)
    text, exact = _reference_display(v, r)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (text, exact), (v, r)
    assert evaluation["current"] == reference
    if reference < 0:
        assert evaluation["magnitude_value"] == _reference_display(v.lstrip("-"), r)[0]
    else:
        assert evaluation["magnitude_value"] is None
    return evaluation


@pytest.fixture
def elec():
    c, aid = _client_for("dcl-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def mech():
    c, aid = _client_for("dcl-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": MECH})


# ==========================================================================
# 1. the Owner's reference vectors and the sign convention
# ==========================================================================
@pytest.mark.parametrize("v,r,expected", REFERENCE)
def test_reference_vectors_at_owner_adapter_and_consumer(v, r, expected):
    assert method.evaluate(float(v), float(r)) == {"i_load": 0.5}
    result = dc.execute(BINDING, _request(float(v), float(r)))
    assert result["state"] == dc.STATE_SUCCESS and _i(result) == 0.5
    evaluation = _check_against_reference(v, r)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (expected, True)


@pytest.mark.parametrize("v,r,display,magnitude", [
    ("-12", "24", "-0.5", "0.5"), ("-5", "10", "-0.5", "0.5"),
    ("-1", "3", "-0.333333333333", "0.333333333333"),
    ("-0.000000001", "999999999999.999999999", "-1 × 10^-21", "1 × 10^-21"),
])
def test_negative_voltage_gives_a_signed_negative_current(v, r, display, magnitude):
    evaluation = _check_against_reference(v, r)
    assert evaluation["display_value"] == display
    assert evaluation["magnitude_value"] == magnitude       # separate, never a replacement
    assert _i(evaluation["result"]) < 0


@pytest.mark.parametrize("v", ["0", "-0", "0.000", "-0.000000000", "000000000"])
def test_zero_voltage_gives_exactly_zero_current(v):
    evaluation = _check_against_reference(v, "47")
    assert evaluation["display_value"] == "0" and evaluation["display_exact"] is True
    produced = _i(evaluation["result"])
    assert produced == 0.0 and math.copysign(1.0, produced) == 1.0
    assert evaluation["magnitude_value"] is None


# ==========================================================================
# 2. exact, nonterminating and rounded quotients; the display
# ==========================================================================
@pytest.mark.parametrize("v,r,display,exact", [
    ("1", "4", "0.25", True), ("3.3", "220", "0.015", True),
    ("9", "0.001", "9000", True), ("1", "8", "0.125", True),
    ("1", "3", "0.333333333333", False), ("2", "3", "0.666666666667", False),
    ("10", "7", "1.42857142857", False), ("1", "0.000000003", "333333333.333", False),
    ("999999999.999999999", "1", "1000000000", False),
    ("123456789012", "1", None, None),     # 12 integer digits: invalid for V
])
def test_exact_and_rounded_quotients(v, r, display, exact):
    if display is None:
        assert _evaluate(v=v, r=r)["outcome"] == dcl.INVALID_NUMERIC_INPUT
        return
    evaluation = _check_against_reference(v, r)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (display, exact)


def test_round_half_to_even_at_twelve_significant_digits():
    # exact quotients with a 13th significant digit of 5 and nothing after it
    assert dcl.format_current(Fraction("0.1234567890125")) == ("0.123456789012", False)
    assert dcl.format_current(Fraction("0.1234567890135")) == ("0.123456789014", False)
    assert dcl.format_current(Fraction("-2.5000000000005")) == ("-2.5", False)
    assert dcl.format_current(Fraction("9.9999999999995")) == ("10", False)
    assert dcl.format_current(Fraction("9.999999999994")) == ("9.99999999999", False)
    assert dcl.format_current(Fraction(1, 2)) == ("0.5", True)


def test_tiny_and_large_currents_are_never_shown_as_zero_or_truncated():
    assert dcl.format_current(Fraction(1, 10 ** 6)) == ("0.000001", True)
    assert dcl.format_current(Fraction(1, 10 ** 7)) == ("1 × 10^-7", True)
    assert dcl.format_current(Fraction(999999, 10 ** 12)) == ("9.99999 × 10^-7", True)
    assert dcl.format_current(Fraction(10 ** 11)) == ("100000000000", True)
    assert dcl.format_current(Fraction(10 ** 12)) == ("1 × 10^12", True)
    assert dcl.format_current(Fraction(1, 3 * 10 ** 20)) == ("3.33333333333 × 10^-21", False)
    for value in (Fraction(1, 10 ** 30), Fraction(-7, 10 ** 25)):
        text, _exact = dcl.format_current(value)
        assert text not in ("0", "-0") and "10^" in text
    with pytest.raises(TypeError):
        dcl.format_current(0.5)


@pytest.mark.parametrize("v,r", [
    ("0.000000001", "999999999999.999999999"),       # smallest |I|
    ("999999999.999999999", "0.000000001"),          # largest |I|
    ("-999999999.999999999", "0.000000001"),
    ("0.000000001", "0.000000001"), ("999999999", "999999999999"),
    ("1.000000001", "3"), ("0.1", "0.3"),
])
def test_representation_limits_are_calculated_and_representable(v, r):
    evaluation = _check_against_reference(v, r)
    produced = _i(evaluation["result"])
    assert math.isfinite(produced) and produced != 0.0


def test_random_admitted_decimals_against_the_independent_reference():
    rng = random.Random(20261025)
    for _ in range(600):
        iv = rng.randint(0, 10 ** rng.randint(1, 9) - 1)
        fv = rng.randint(0, 10 ** 9 - 1)
        v = "%s%d.%09d" % ("-" if rng.random() < 0.4 else "", iv, fv)
        ir = rng.randint(0, 10 ** rng.randint(1, 12) - 1)
        fr = rng.randint(1, 10 ** 9 - 1)
        r = "%d.%s" % (ir, ("%09d" % fr).rstrip("0") or "0")
        if Fraction(r) <= 0:
            continue
        _check_against_reference(v, r)


def test_the_error_bound_proof():
    u = Fraction(1, 2 ** 53)
    assert (1 + u) ** 2 / (1 - u) - 1 < PROVEN_WORST_CASE < DECIMAL_BOUND
    worst = Fraction(0)
    for v, r in (("0.1", "0.3"), ("0.7", "0.1"), ("0.000000003", "0.000000007"),
                 ("1.1", "3.3"), ("999999999.999999999", "0.000000003")):
        reference = _reference(v, r)
        produced = method.evaluate(float(Fraction(v)), float(Fraction(r)))["i_load"]
        worst = max(worst, abs(Fraction(produced) - reference) / abs(reference))
    assert worst <= PROVEN_WORST_CASE


# ==========================================================================
# 3. positive resistance; the adapter's binary acceptance
# ==========================================================================
@pytest.mark.parametrize("r", ["0", "-0", "0.000000000", "-1", "-0.000000001", "-24"])
def test_non_positive_resistance_is_refused_before_the_owner(r, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(r=r)
    assert evaluation["outcome"] == dcl.RESISTANCE_NOT_POSITIVE
    assert evaluation["display_value"] is None and evaluation["result"] is None
    assert not calls


@pytest.mark.parametrize("r", [0.0, -0.0, -1.0, -1e308])
def test_non_positive_resistance_is_declined_by_the_owner(r):
    result = dc.execute(BINDING, _request(12.0, r))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None)


@pytest.mark.parametrize("v,r", [(1e308, 1e-308), (-1e308, 1e-10), (1e-308, 1e308),
                                 (5e-324, 2.0), (-5e-324, 3.0)])
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


def test_adapter_results_are_correctly_rounded():
    rng = random.Random(7)
    for _ in range(500):
        v = rng.uniform(-1e9, 1e9)
        r = 10 ** rng.uniform(-9, 12)
        exact = Fraction(v) / Fraction(r)
        produced = method.evaluate(v, r)["i_load"]
        assert produced == float(exact)          # one correct rounding
        assert abs(Fraction(produced) - exact) <= abs(exact) * Fraction(1, 2 ** 53)


# ==========================================================================
# 4. the input grammar and strict capture
# ==========================================================================
@pytest.mark.parametrize("v,r", [
    ("+12", "24"), ("1e3", "24"), (" 12", "24"), ("12 ", "24"), ("1,5", "24"),
    ("١٢", "24"), ("12.", "24"), (".5", "24"), ("--1", "24"), ("inf", "24"),
    ("nan", "24"), ("1.0000000001", "24"), ("1234567890", "24"), ("12V", "24"),
    ("", "24"), ("12", ""), ("12", "24Ω"), ("12", "1e2"), ("12", "1234567890123"),
    ("12", "0.0000000001"), ("12", "+24"), ("−12", "24"), ("0x1", "24"),
    ("1" * 65, "24"), ("12", "24.5.0"),
])
def test_malformed_values_are_invalid_and_never_reach_the_owner(v, r, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(v=v, r=r)
    assert evaluation["outcome"] == dcl.INVALID_NUMERIC_INPUT, (v, r)
    assert evaluation["display_value"] is None and not calls


def test_accepted_grammar_is_exact():
    assert dcl.parse_value("-999999999.999999999", "v_load") == Fraction("-999999999.999999999")
    assert dcl.parse_value("999999999999.999999999", "r_load") == Fraction("999999999999.999999999")
    assert dcl.parse_value("0.000000001", "r_load") == Fraction(1, 10 ** 9)
    assert dcl.parse_value("-0", "v_load") == 0
    assert dcl.parse_value("1234567890", "v_load") is None
    assert dcl.parse_value("1.0000000001", "r_load") is None


def test_strict_capture_refuses_duplicates_unknown_fields_and_bad_answers():
    good = {k: [v] for k, v in _form().items()}
    assert dcl.capture_form(good) is not None
    duplicate = dict(good, **{dcl.VALUE_FIELD % "v_load": ["12", "13"]})
    contradictory = dict(good, **{dcl.DECLARATION_FIELD % "resistive_load":
                                  ["applies", "does_not_apply"]})
    for bad in (duplicate, contradictory, dict(good, unexpected=["1"]),
                dict(good, **{dcl.SCREEN_FIELD % "safety_function": ["maybe"]}),
                dict(good, **{dcl.DECLARATION_FIELD % "sign_convention": ["yes"]}),
                dict(good, **{dcl.VALUE_FIELD % "i_load": ["0.5"]}),
                dict(good, unit_v_load=["mV"]), [], None):
        assert dcl.capture_form(bad) is None
    missing = {k: v for k, v in good.items() if k != dcl.DECLARATION_FIELD % "sign_convention"}
    captured = dcl.capture_form(missing)
    assert captured is not None
    assert dcl.evaluate(captured, BINDING)["outcome"] == dcl.NOT_DECLARED


# ==========================================================================
# 5. the owner: inventory, units, bindings and integrity (Correction 06)
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["outputs"] == {"i_load": {"value": 0.5, "unit": "A",
                                            "provenance": "CALCULATED"}}
    assert result["inputs"]["v_load"] == {"value": 12.0, "unit": "V",
                                          "provenance": "OWNER_STATED"}
    assert [u["record_id"] for u in result["unit_records"]] == [
        "dcu:U011", "dcu:U012", "dcu:U013"]
    assert [q["source_ref"] for q in result["source_qualification"]] == ["DOE-OHM-S1"]
    assert result["source_qualification"][0]["source_use_policy_ref"] == "dcu:SU012"
    assert result["validation_status"] == "UNVALIDATED"
    assert (result["artifact_version"], result["implementation_version"]) == ("12", "1.11.0")
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_units_and_condition():
    assert ("electrical:dc_resistive_load_current", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 12
    assert {"electric_resistance", "electric_current"} <= dc.ADMITTED_QUANTITY_KINDS
    assert {"V", "Ω", "A"} <= dc.ADMITTED_UNIT_TOKENS
    assert dc.KIND_TOKEN_EXCEPTIONS == {"voltage": frozenset({"mV", "V"}),
                                        "time": frozenset({"s", "h"})}
    assert dc._CONDITIONS == ("greater_than_zero", "less_than_zero",
                              "within_zero_and_role")      # unchanged vocabulary
    record = _record(dc.load_artifact())
    assert record["applicability"] == [
        {"role": "r_load", "condition": "greater_than_zero", "bound_role": None}]
    assert record["result_range"] == []
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"] + record["output_roles"]] == [
        ("v_load", "voltage", "V"), ("r_load", "electric_resistance", "Ω"),
        ("i_load", "electric_current", "A")]
    assert "Ω" == "Ω"


@pytest.mark.parametrize("units,reason", [
    (("mV", "Ω"), dc.UNIT_NOT_ADMITTED), (("A", "Ω"), dc.UNIT_NOT_ADMITTED),
    (("V", "V"), dc.UNIT_NOT_ADMITTED), (("V", "A"), dc.UNIT_NOT_ADMITTED),
    (("v", "Ω"), dc.UNKNOWN_UNIT), (("volt", "Ω"), dc.UNKNOWN_UNIT),
    (("kV", "Ω"), dc.UNKNOWN_UNIT), (("V", "Ω"), dc.UNKNOWN_UNIT),
    (("V", "ohm"), dc.UNKNOWN_UNIT), (("V", "kΩ"), dc.UNKNOWN_UNIT),
    (("V", "mΩ"), dc.UNKNOWN_UNIT),
])
def test_units_are_exact_with_no_alias_or_conversion(units, reason):
    result = dc.execute(BINDING, _request(units=units))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, reason, None)


def test_mv_and_v_are_two_tokens_with_no_mapping():
    tmp36_binding = OTHER_BINDINGS[-1]
    in_volts = dc.execute(tmp36_binding, {
        "method_id": tmp36_method.METHOD_ID, "method_version": "1.0",
        "inputs": {"v_out": {"value": 0.75, "unit": "V"}}, "subject_ref": None})
    assert (in_volts["state"], in_volts["reason"]) == (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED)
    in_mv = dc.execute(BINDING, _request(12000.0, 24.0, units=("mV", "Ω")))
    assert (in_mv["state"], in_mv["reason"]) == (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED)
    data = dc.load_artifact()
    voltage = sorted(u["unit_token"] for u in data["unit_records"]
                     if u["quantity_kind"] == "voltage")
    assert voltage == ["V", "mV"]
    others = {}
    for unit in data["unit_records"]:
        others.setdefault(unit["quantity_kind"], []).append(unit["unit_token"])
    # Correction 10 (§13I): time is the second named two-token kind (s, h); every
    # other kind still holds exactly one token
    assert sorted(others["time"]) == ["h", "s"]
    assert all(len(tokens) == 1 for kind, tokens in others.items()
               if kind not in ("voltage", "time"))


def test_each_binding_executes_only_its_own_method():
    for binding in OTHER_BINDINGS:
        assert dc.execute(binding, _request())["reason"] == dc.OPERATION_NOT_ADMITTED
    swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, therm_method.evaluate)
    assert _failure(dc.execute(swapped, _request()))
    assert dc.execute(dc.bind_method(method.METHOD_ID, "2.0", method.evaluate),
                      _request())["reason"] == dc.VERSION_MISMATCH


def test_app_wires_one_immutable_binding_per_method():
    assert webapp._DC_LOAD_CURRENT_BINDING.adapter_identity \
        == "engine.dc_resistive_load_current_method.evaluate"
    with pytest.raises(AttributeError):
        webapp._DC_LOAD_CURRENT_BINDING.method_id = "x"
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 12
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("dc_resistive_load_current_method", "engine.dc_resistive",
                   "electrical_content_config",
                   "import fractions", "decimal", "sqlite", "1000", "1e-3", "0.001"):
        assert banned not in owner_source.lower(), banned


def _owner_tamper(data, name):
    record = _record(data)
    if name == "third_voltage_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "V"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "kV"
        data["unit_records"].append(extra)
    elif name == "second_resistance_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "Ω"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U098", "kΩ"
        data["unit_records"].append(extra)
    elif name == "ohm_sign_alias":
        [u for u in data["unit_records"] if u["unit_token"] == "Ω"][0]["unit_token"] = "Ω"
    elif name == "drop_volt":
        data["unit_records"] = [u for u in data["unit_records"] if u["unit_token"] != "V"]
    elif name == "drop_kind":
        data["quantity_kinds"] = [k for k in data["quantity_kinds"]
                                  if k["quantity_kind"] != "electric_current"]
    elif name == "seventh_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "electrical:dc_resistive_load_power"
        data["methods"].append(extra)
    elif name == "unknown_condition":
        record["applicability"][0]["condition"] = "between_1_and_1000"
    elif name == "policy_unresolved":
        record["source_qualification"][0]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "output_kind":
        record["output_roles"][0]["quantity_kind"] = "voltage"
    elif name == "input_in_mv":
        record["input_roles"][0]["unit_token"] = "mV"
        return data, False             # structurally valid; refused at execution
    elif name == "basis":
        data["source_use_policies"][-1]["inspection_basis"] = "EXECUTOR"
    return data, True


@pytest.mark.parametrize("name", ["third_voltage_unit", "second_resistance_unit",
                                  "ohm_sign_alias", "drop_volt", "drop_kind",
                                  "seventh_method", "unknown_condition",
                                  "policy_unresolved", "output_kind", "basis"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    data, invalid = _owner_tamper(_owner_artifact(), name)
    path = _write(tmp_path, data)
    assert invalid
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    assert _failure(dc.execute(BINDING, _request(), artifact_path=path))


def test_a_v_role_rebound_to_mv_refuses_the_v_request(tmp_path):
    data, _ = _owner_tamper(_owner_artifact(), "input_in_mv")
    path = _write(tmp_path, data)
    result = dc.execute(BINDING, _request(), artifact_path=path)
    assert (result["state"], result["reason"]) == (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED)


def test_owner_v5_records_are_unchanged_by_the_sixth_admission():
    data = dc.load_artifact()
    assert data["artifact_version"] == "12"
    v5 = {"quantity_kinds": data["quantity_kinds"][:10],
          "unit_records": data["unit_records"][:10],
          "source_use_policies": data["source_use_policies"][:10],
          "methods": data["methods"][:5]}
    canonical = json.dumps(v5, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(canonical.encode()).hexdigest() == V5_RECORDS_DIGEST
    assert [u["record_id"] for u in data["unit_records"][10:13]] == [
        "dcu:U011", "dcu:U012", "dcu:U013"]
    assert [p["record_id"] for p in data["source_use_policies"][10:12]] == [
        "dcu:SU011", "dcu:SU012"]
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "dcu:U011, dcu:U012 and dcu:U013 only" in policies["dcu:SU011"]["inspected_content"]
    assert "DOE-OHM-S1 only" in policies["dcu:SU012"]["inspected_content"]
    assert "dcu:SU004 (THERM-01) is not extended" in policies["dcu:SU012"]["inspection_reference"]


# ==========================================================================
# 6. the method artifact and the consumer
# ==========================================================================
def test_method_artifact_loads_with_provenance_and_ip_boundary():
    data = dcl.load_artifact()
    by_id = {r["record_id"]: r for r in data["sources"]}
    source = by_id["DOE-OHM-S1"]
    for phrase in ("E = I x R", "handbook page 14", "ARCHIVE - Canceled",
                   "electronics_electrical:PR004", "Not re-inspected by the executor",
                   "not claimed that DOE printed them"):
        assert phrase in source["inspected_content"], phrase
    assert "DOE-HDBK-1011/1-92" in source["source_title"]
    policy = by_id["dcload:SU001"]
    for phrase in ("not a legal opinion", "electronics_electrical:PR006", "public domain",
                   "EG&G Idaho", "no blanket claim", "not broadened"):
        assert phrase in policy["inspected_content"], phrase
    assert policy["acknowledgement"] == (
        "Reference source material: U.S. Department of Energy — Electrical Science, "
        "DOE-HDBK-1011/1-92")
    assert "endorse" in policy["no_endorsement_limitation"]
    assert "not claimed to print this solved form or the sign convention" \
        in data["method"]["derivation"]


def test_pack_provenance_records_and_claim_are_unchanged():
    provenance = json.loads((ROOT / "domains" / "domain_provenance.json")
                            .read_text(encoding="utf-8"))
    records = {r["record_id"]: r for r in provenance["records"]}
    assert records["electronics_electrical:PR004"]["notes"].endswith(
        "Bounded reference relationships only — no project-specific calculation and no "
        "applicability inference.")
    pack = (ROOT / "domains" / "electronics_electrical" / "domain.json").read_text(encoding="utf-8")
    assert "dc_resistive_load_current" not in pack and "dcload:" not in pack


@pytest.mark.parametrize("mutate", [
    lambda d: d["declarations"][1].__setitem__("accepted_value", "any load"),
    lambda d: d["declarations"][3].__setitem__("refusal", "NOT_DECLARED"),
    lambda d: d["numeric_domain"]["roles"][0].__setitem__("unit_token", "mV"),
    lambda d: d["numeric_domain"]["roles"][2].__setitem__("unit_token", "mA"),
    lambda d: d["method"].__setitem__("executed_form", "i_load = abs(v_load) / r_load"),
    lambda d: d["disclosure"].pop(),
    lambda d: d["disclosure"].__setitem__(5, "Your source can supply this current."),
    lambda d: d["screen_items"].pop(),
    lambda d: d["sources"][0].__setitem__("source_use_policy_ref", "tmp36:SU001"),
    lambda d: d["sources"][0].__setitem__("inspection_basis", "EXECUTOR"),
    lambda d: d.__setitem__("artifact_version", "2"),
])
def test_method_artifact_tamper_is_knowledge_unavailable(mutate, monkeypatch):
    data = _method_artifact()
    mutate(data)
    with pytest.raises(dcl.DcLoadKnowledgeError):
        dcl.validate_artifact(data)
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    result = dcl.evaluate(_captured(), BINDING, artifact=data)
    assert result["outcome"] == dcl.KNOWLEDGE_UNAVAILABLE and not calls
    assert result["display_value"] is None and result["current"] is None


def test_unreadable_method_artifact_is_knowledge_unavailable(tmp_path, monkeypatch):
    monkeypatch.setattr(dcl, "ARTIFACT_PATH", tmp_path / "missing.json")
    assert _evaluate()["outcome"] == dcl.KNOWLEDGE_UNAVAILABLE
    (tmp_path / "bad.json").write_text("{", encoding="utf-8")
    monkeypatch.setattr(dcl, "ARTIFACT_PATH", tmp_path / "bad.json")
    assert _evaluate()["outcome"] == dcl.KNOWLEDGE_UNAVAILABLE


def test_unreadable_owner_artifact_gives_no_number(tmp_path):
    result = dcl.evaluate(_captured(), BINDING, owner_artifact_path=tmp_path / "none.json")
    assert (result["outcome"], result["owner_state"], result["owner_reason"]) == (
        dcl.KNOWLEDGE_UNAVAILABLE, dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE)
    assert result["display_value"] is None


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(decl={"steady_state_dc": ""}, screen={"safety_function": "yes"},
                     v="x", r="0")["outcome"] == dcl.NOT_DECLARED
    assert _evaluate(screen={"safety_function": ""})["outcome"] == dcl.NOT_DECLARED
    assert _evaluate(screen={"battery_or_storage_cell": "yes"},
                     decl={"resistive_load": "does_not_apply"},
                     v="x")["outcome"] == dcl.ENGINEERING_REVIEW_REQUIRED
    for item in dcl.SCREEN_ITEMS:
        assert _evaluate(screen={item: "yes"})["outcome"] \
            == dcl.ENGINEERING_REVIEW_REQUIRED, item
    for decl in dcl.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"}, v="x")["outcome"] \
            == dcl.MODEL_NOT_SUPPORTED, decl
    assert _evaluate(v="x", r="0")["outcome"] == dcl.INVALID_NUMERIC_INPUT
    assert _evaluate(r="0")["outcome"] == dcl.RESISTANCE_NOT_POSITIVE
    assert not calls


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, dcl.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, dcl.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, dcl.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, dcl.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, dcl.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, dcl.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, dcl.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, dcl.UNMAPPED_OWNER_OUTCOME),
    (dc.STATE_REFUSAL, dc.OPERATION_NOT_ADMITTED, dcl.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome, monkeypatch):
    monkeypatch.setattr(dc, "execute", lambda *a, **k: {
        "state": state, "reason": reason, "outputs": None})
    result = _evaluate()
    assert (result["outcome"], result["owner_state"], result["owner_reason"]) \
        == (outcome, state, reason)
    assert result["result"] is None and result["display_value"] is None


@pytest.mark.parametrize("produced", [0.5000001, 0.49999, -0.5, 0.0, 0.5 + 2.0 ** -40,
                                      "0.5", None, float("nan")])
def test_decimal_reference_failure_fails_closed_with_no_number(produced, monkeypatch):
    real = dc.execute

    def tampered(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["i_load"]["value"] = produced
        return result
    monkeypatch.setattr(dc, "execute", tampered)
    result = _evaluate()
    assert result["outcome"] == dcl.KNOWLEDGE_UNAVAILABLE
    assert result["owner_state"] == dc.STATE_SUCCESS          # preserved, not rewritten
    assert result["result"] is None and result["display_value"] is None


def test_zero_must_be_exact_zero_and_only_for_zero_voltage(monkeypatch):
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: dict(
        real(b, r, artifact_path=artifact_path),
        outputs={"i_load": {"value": 2.0 ** -60, "unit": "A",
                            "provenance": "CALCULATED"}}))
    assert _evaluate(v="0")["outcome"] == dcl.KNOWLEDGE_UNAVAILABLE
    assert dcl.agrees_with_reference(0.0, Fraction(0))
    assert not dcl.agrees_with_reference(1e-300, Fraction(0))
    assert not dcl.agrees_with_reference(0.0, Fraction(1, 10 ** 21))


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
    a = dcl.evaluate(first, BINDING)
    b = dcl.evaluate(_captured(v="-1", r="3"), BINDING)
    assert first == before
    assert a == dcl.evaluate(_captured(v="12", r="24"), BINDING)
    assert (a["display_value"], b["display_value"]) == ("0.5", "-0.333333333333")


def test_consumer_and_adapter_import_no_other_authority():
    import ast
    for module in (dcl, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        for banned in ("cap13", "therm01", "tmp36", "record_store", "safety_signal",
                       "requests", "urllib", "openai", "web", "flask", "random", "time",
                       "sqlite3", "domain_rules"):
            assert not any(banned == n or n.startswith(banned + ".") or banned in n
                           for n in names if n), (module.__name__, banned)


# ==========================================================================
# 7. EN / AR fidelity and the contracts
# ==========================================================================
def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_english_wording_equals_the_artifact():
    content = dcl.load_artifact()
    assert ui_text.text("UI_DCL_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"]
        assert ui_text.text("UI_DCL_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."
    for entry in content["screen_items"]:
        value = entry["item"]
        assert ui_text.text("UI_DCL_SCREEN_" + entry["item_id"].upper(), "en") \
            == value[0].upper() + value[1:]


def test_arabic_wording_equals_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    assert ui_text.text("UI_DCL_DISCLOSURE", "ar").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$",
                           _contract_section("**A-2", "**A-3"), re.M))
    for decl, ref in dcl.DECLARATIONS:
        assert ui_text.text("UI_DCL_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    screen = dict(re.findall(r"^\| (\w+) \| (.+?) \|$",
                             _contract_section("**A-3", "**A-4"), re.M))
    for item in dcl.SCREEN_ITEMS:
        assert ui_text.text("UI_DCL_SCREEN_" + item.upper(), "ar") == screen[item], item
    s9 = _contract_section("## 9. Result", "## 9A.")
    assert [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)] \
        == dcl.load_artifact()["disclosure"]
    s5 = _contract_section("## 5. Applicability", "## 6.")
    english = dict(re.findall(r"^\| (D-\d) \| `\w+` \| (.+?) \|$", s5, re.M))
    for entry in dcl.load_artifact()["declarations"]:
        assert english[entry["contract_ref"]] == entry["accepted_value"]


def test_every_key_has_both_languages_and_no_rating_or_safety_claim():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_DCL_[A-Z0-9_]+)": \{', source)
    assert len(keys) >= 40
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("the load is safe", "circuit is safe", "measured by inventorai", "guaranteed", "certified",
                  "has been validated", "recommended", "can supply this current.",
                  "rated for", "fuse rating", "maximum current"):
        assert claim not in english, claim
    for phrase in ("next engineering need", "remain unverified", "did not measure",
                   "not physical limits", "labelled rounded", "flowing the opposite way"):
        assert phrase in english, phrase


def test_correction_06_is_recorded_and_earlier_sections_unchanged():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 06" in body and "## 13E." in body
    section = _norm(body[body.index("## 13E."):body.index("## 14.")])
    for phrase in ("exactly six", "`electric_resistance`", "`electric_current`", "`V`",
                   "`Ω` (U+03A9)", "`A`", "content version `6`", "`1.5.0`",
                   "NOT a generic owner policy", "{`mV`, `V`}", "KIND_TOKEN_EXCEPTIONS",
                   "nothing relates `mV` to `V`", "Condition vocabulary. Unchanged",
                   "No result range is declared"):
        assert phrase.lower() in section.lower(), phrase
    assert "**Methods — exactly five:**" in body[body.index("## 13D."):body.index("## 13E.")]
    assert "- Correction 06 (§13E) is Owner-authorized" in body


def test_method_contract_records_scope_provenance_and_exclusions():
    text = _norm(CONTRACT.read_text(encoding="utf-8"))
    for phrase in ("DOE-HDBK-1011/1-92", "handbook page 14", "ARCHIVE — Canceled",
                   "electronics_electrical:PR004", "electronics_electrical:PR006",
                   "no project-specific calculation", "passive reference direction",
                   "`12 V / 24 Ω = +0.5 A`", "3.0000001", "Root only",
                   "28-T3", "Representation limits are not physical limits",
                   "labelled exact when", "1 × 10^-21"):
        assert phrase in text, phrase


# ==========================================================================
# 8. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_electronics_root_journey_and_reference_values(elec):
    c, _aid, sid = elec
    assert "data-dcl-link" in _page(c, sid)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-dcl-form" in body and "checked" not in body
    assert 'value=""' in body and "data-dcl-value-note" in body
    for v, r, expected in REFERENCE:
        body = c.post(URL % sid, data=_form(v=v, r=r)).get_data(as_text=True)
        assert _value(body) == "%s A" % expected, (v, r)
        assert 'data-dcl-exactness="exact"' in body and _magnitude(body) is None
    body = c.post(URL % sid, data=_form(v="-12", r="24")).get_data(as_text=True)
    assert _value(body) == "-0.5 A" and _magnitude(body) == "0.5 A"
    body = c.post(URL % sid, data=_form(v="1", r="3")).get_data(as_text=True)
    assert _value(body) == "0.333333333333 A"
    assert 'data-dcl-exactness="rounded"' in body
    assert "UNVALIDATED" in body and "NOT EVIDENCE" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_DCL_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert "Next engineering need" in text
    assert "DOE-HDBK-1011/1-92" in body and "NIST" in body
    assert "electrical:dc_resistive_load_current" in body
    assert '<bdi dir="ltr" data-dcl-echo-value>1</bdi>' in body
    assert '<bdi dir="ltr" data-dcl-echo-value>3</bdi>' in body


@pytest.mark.parametrize("over,outcome", [
    ({"r": "0"}, "RESISTANCE_NOT_POSITIVE"),
    ({"r": "-24"}, "RESISTANCE_NOT_POSITIVE"),
    ({"v": "1e3"}, "INVALID_NUMERIC_INPUT"),
    ({"v": ""}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"mains_or_high_voltage": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"resistive_load": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"sign_convention": ""}}, "NOT_DECLARED"),
])
def test_non_success_shows_one_reason_and_no_number(elec, over, outcome):
    c, _aid, sid = elec
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert ui_text.text("UI_DCL_OUTCOME_" + outcome, "en") in html.unescape(body)
    assert _value(body) is None and _magnitude(body) is None
    assert body.count("data-dcl-outcome") == 1 and "data-dcl-result" not in body


def test_mechanical_root_is_not_eligible_but_a_declared_part_is(mech, monkeypatch):
    c, _aid, sid = mech
    assert "data-dcl-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._dcl, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-dcl-scope-note" in body
        assert "data-dcl-form" not in body and _value(body) is None
    # DC-RESISTIVE-LOAD-INTEGRATED-PART-01: on an integrated project with a
    # Mechanical focus the declared Electrical / Electronics part is offered the
    # calculation (tests/test_dc_resistive_load_integrated_part.py)
    c2, _ = _client_for("dcl-part-mech@example.com")
    sid2 = _integrated(c2, MECH)
    assert webapp._dcl_eligible(sid2)
    assert "data-dcl-link" in _page(c2, sid2)
    assert not called
    # an Electrical / Electronics focus is eligible by its root domain
    c3, _ = _client_for("dcl-part-elec@example.com")
    sid3 = _integrated(c3, ELEC)
    assert webapp._dcl_eligible(sid3)


def test_unreadable_root_domain_grants_nothing(elec, monkeypatch):
    c, _aid, sid = elec

    def broken(_sid):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(webapp, "_cap12_root_domain", broken)
    assert not webapp._dcl_eligible(sid)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-dcl-form" not in body and _value(body) is None


def test_csrf_authorization_and_malformed_requests(elec):
    c, _aid, sid = elec
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("dcl-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302 and "data-dcl" not in r.get_data(as_text=True)
    for bad in (dict(_form(), unexpected="1"),
                dict(_form(), screen_safety_function="maybe"),
                dict(_form(), decl_resistive_load="ohmic"),
                dict(_form(), value_i_load="0.5")):
        r = c.post(URL % sid, data=bad)
        assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    from werkzeug.datastructures import MultiDict
    for field, value in ((dcl.VALUE_FIELD % "v_load", "13"),
                         (dcl.DECLARATION_FIELD % "resistive_load", "does_not_apply")):
        r = c.post(URL % sid, data=MultiDict(list(_form().items()) + [(field, value)]))
        assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    body = c.post(URL % sid, data=_form(v="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body
    r = c.get(URL % sid)
    assert r.headers["Cache-Control"] == "no-store"


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
    start = src.index("# DC-RESISTIVE-LOAD-CURRENT-01 — DC Resistive Load Current")
    section = src[start:src.index("# DC-RESISTIVE-LOAD-POWER-01 —", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "_cap13", "_tmp36", "load_project_subsystems",
                   "request.args", "cap09", "success_criteria", "redirect("):
        assert banned not in section, banned
    assert section.count("_dcalc.bind_method(") == 1
    assert [r.rule for r in webapp.app.url_map.iter_rules() if "dc-load-current" in r.rule] \
        == ["/session/<sid>/dc-load-current"] * 2
    for template in ("deliverable.html", "report.html", "success_criteria.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "dc-load" not in path.read_text(encoding="utf-8").lower()
            assert "ui_dcl_" not in path.read_text(encoding="utf-8").lower()


def test_existing_five_calculations_are_unchanged(mech, elec):
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


def test_session_page_link_is_optional_and_carries_no_calculation(elec):
    c, _aid, sid = elec
    page = _page(c, sid)
    link = page.split("data-dcl-link", 1)[1].split("</p>", 1)[0]
    assert URL % sid in link and "A</bdi>" not in link
    assert "I = V / R" in html.unescape(link)


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_arabic_isolation_and_signed_values(elec, lang):
    c, _aid, sid = elec
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form(v="-12", r="24")).get_data(as_text=True)
    assert _value(body) == "-0.5 A" and _magnitude(body) == "0.5 A"
    assert '<bdi dir="ltr" data-dcl-echo-value>-12</bdi>' in body
    if lang == "ar":
        assert 'dir="rtl"' in body
        isolated = [html.unescape(run)
                    for run in re.findall(r'<bdi dir="ltr">([^<]*)</bdi>', body)]
        for token in ("UNVALIDATED", "NOT EVIDENCE", "Ohm's law", "DOE-HDBK-1011/1-92",
                      "(Ω)", "(A)"):
            assert any(token in run for run in isolated), token
        assert any(run == "I = V / R" for run in isolated)
        stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
        for item in ui_text.text("UI_DCL_DISCLOSURE", "ar").split("\n\n"):
            assert _norm(item) in _norm(stripped), item[:30]
        refusal = c.post(URL % sid, data=_form(r="0")).get_data(as_text=True)
        assert ui_text.text("UI_DCL_OUTCOME_RESISTANCE_NOT_POSITIVE", "ar") \
            in html.unescape(re.sub(r"<[^>]+>", "", refusal))
        assert _value(refusal) is None
