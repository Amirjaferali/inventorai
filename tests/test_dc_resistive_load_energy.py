# -*- coding: utf-8 -*-
"""Electrical / Electronics - DC Resistive Load Energy, Slice 1 (directly owning tests).

DC-RESISTIVE-LOAD-ENERGY-01. The shared deterministic calculation / units owner
after the bounded eighth admission of calc/units Correction 08 (§13G); the ONE
method ``electrical:dc_resistive_load_energy`` 1.0
(``engine/dc_resistive_load_energy_method.py``) and its ONE consumer
(``engine/dc_resistive_load_energy.py`` + the request-local page).

Scientific reference: the power a resistive element absorbs, P = V x I with
I = V / R (DOE-HDBK-1011/1-92, recorded as electronics_electrical:PR004), and
power as the rate at which energy is transferred (DOE-HDBK-1010-92, recorded as
electronics_electrical:PR008), so for a power that stays constant throughout
the duration t, E = P x t = V**2 x t / R. The numerical tests use an
INDEPENDENT decimal reference: every expected energy and every expected display
is formed with ``decimal.Decimal`` from the typed decimal strings, never from
the consumer's or the adapter's own arithmetic. Synthetic data.
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
from engine import dc_resistive_load_energy as dce
from engine import dc_resistive_load_energy_method as method
from engine import dc_resistive_load_power_method as power_method
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
from tests.test_dc_resistive_load_power import _form as _power_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "ELECTRICAL_DC_RESISTIVE_LOAD_ENERGY_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
URL = "/session/%s/dc-load-energy"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
OTHER_BINDINGS = (
    dc.bind_method(cap13_method.METHOD_ID, "1.0", cap13_method.evaluate),
    dc.bind_method(therm_method.METHOD_ID, "1.0", therm_method.evaluate),
    dc.bind_method(moment_method.METHOD_ID, "1.0", moment_method.evaluate),
    dc.bind_method(rotational_method.METHOD_ID, "1.0", rotational_method.evaluate),
    dc.bind_method(tmp36_method.METHOD_ID, "1.0", tmp36_method.evaluate),
    dc.bind_method(current_method.METHOD_ID, "1.0", current_method.evaluate),
    dc.bind_method(power_method.METHOD_ID, "1.0", power_method.evaluate))
# The reference vectors (V, Ω, s -> J).
REFERENCE = (("12", "24", "3600", "21600"), ("5", "10", "60", "150"),
             ("230", "52.9", "1", "1000"), ("3", "1", "2", "18"))
DECIMAL_BOUND = Fraction(1, 2 ** 50)
PROVEN_WORST_CASE = Fraction(50000001, 10000000) * Fraction(1, 2 ** 53)
# The content-version-7 records (quantity kinds, unit records, source-use
# policies and the seven method records), pinned by digest: Correction 08 only
# appends after them.
V7_RECORDS_DIGEST = "784d0b4e85081fdf1d6d9330eb9c49c610ec2b5089c6fe5ce55694229d271b4e"


# --------------------------------------------------------------------------
# helpers: the independent decimal reference
# --------------------------------------------------------------------------
_EXACT = Context(prec=200, rounding=ROUND_HALF_EVEN)
_TWELVE = Context(prec=12, rounding=ROUND_HALF_EVEN)


def _reference(v, r, t):
    """The exact V**2 x t / R as a Fraction, from Decimal alone."""
    voltage = Fraction(Decimal(v))
    return voltage * voltage * Fraction(Decimal(t)) / Fraction(Decimal(r))


def _reference_display(v, r, t):
    """The expected (text, exact) display, from Decimal alone: V**2 x t / R
    correctly rounded to 12 significant digits (half to even), trailing zeros
    removed, plain for 1e-6 <= E < 1e12 and 'm × 10^e' otherwise."""
    if Decimal(v) == 0 or Decimal(t) == 0:
        return "0", True
    product = _EXACT.multiply(_EXACT.multiply(Decimal(v), Decimal(v)),
                              Decimal(t))                    # exact: <= 54 digits
    rounded = _TWELVE.divide(product, Decimal(r))
    exact = Fraction(rounded) == _reference(v, r, t)
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


def _request(v=12.0, r=24.0, t=3600.0, units=("V", "Ω", "s"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"v_load": {"value": v, "unit": units[0]},
                      "r_load": {"value": r, "unit": units[1]},
                      "t_duration": {"value": t, "unit": units[2]}},
           "subject_ref": None}
    req.update(over)
    return req


def _e(result):
    return result["outputs"]["e_load"]["value"]


def _failure(result):
    return (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def _form(v="12", r="24", t="3600", decl=None, screen=None):
    form = {dce.DECLARATION_FIELD % d: dce.ANSWER_APPLIES for d in dce.DECLARATION_IDS}
    form.update({dce.SCREEN_FIELD % s: dce.SCREEN_NO for s in dce.SCREEN_ITEMS})
    form[dce.VALUE_FIELD % "v_load"] = v
    form[dce.VALUE_FIELD % "r_load"] = r
    form[dce.VALUE_FIELD % "t_duration"] = t
    for key, value in (decl or {}).items():
        form[dce.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[dce.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = dce.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return dce.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _method_artifact():
    return json.loads(dce.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data):
    target = tmp_path / "a.json"
    target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return target


def _value(body):
    marker = 'data-dce-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def _check_against_reference(v, r, t):
    """One typed triple through the whole consumer: success, the owner result
    within the decimal bound, the display equal to the independent reference."""
    evaluation = _evaluate(v=v, r=r, t=t)
    assert evaluation["outcome"] == dce.OUTCOME_SUCCESS, (v, r, t)
    reference = _reference(v, r, t)
    produced = _e(evaluation["result"])
    assert math.copysign(1.0, produced) == 1.0, (v, r, t)       # never negative, no -0
    if reference == 0:
        assert produced == 0.0
    else:
        error = abs(Fraction(produced) - reference) / reference
        assert error <= PROVEN_WORST_CASE < DECIMAL_BOUND, (v, r, t)
        assert produced > 0
    assert (evaluation["display_value"], evaluation["display_exact"]) \
        == _reference_display(v, r, t), (v, r, t)
    assert evaluation["energy"] == reference
    return evaluation


@pytest.fixture
def elec():
    c, aid = _client_for("dce-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def mech():
    c, aid = _client_for("dce-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": MECH})


# ==========================================================================
# 1. the reference vectors, the passive sign convention and zero
# ==========================================================================
@pytest.mark.parametrize("v,r,t,expected", REFERENCE)
def test_reference_vectors_at_owner_adapter_and_consumer(v, r, t, expected):
    exact = _reference(v, r, t)
    produced = method.evaluate(float(v), float(r), float(t))["e_load"]
    assert abs(Fraction(produced) - exact) <= exact * Fraction(1, 2 ** 52)
    result = dc.execute(BINDING, _request(float(v), float(r), float(t)))
    assert result["state"] == dc.STATE_SUCCESS and _e(result) == produced
    evaluation = _check_against_reference(v, r, t)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (expected, True)


def test_energy_is_the_power_relation_times_the_duration():
    # E = P x t: the same value as the merged DC load power method times t
    for v, r, t in (("12", "24", "3600"), ("5", "10", "60"), ("9", "0.5", "0.25")):
        power = Fraction(Decimal(v)) ** 2 / Fraction(Decimal(r))
        assert _evaluate(v=v, r=r, t=t)["energy"] == power * Fraction(Decimal(t))


@pytest.mark.parametrize("v,r,t", [("-12", "24", "3600"), ("-5", "10", "60"),
                                   ("-1", "3", "1"),
                                   ("-0.000000001", "999999999999.999999999", "0.000000001"),
                                   ("-999999999.999999999", "0.000000001", "999999999.999999999")])
def test_negative_voltage_gives_the_same_nonnegative_energy(v, r, t):
    negative = _check_against_reference(v, r, t)
    positive = _check_against_reference(v.lstrip("-"), r, t)
    assert negative["display_value"] == positive["display_value"]
    assert _e(negative["result"]) == _e(positive["result"]) > 0
    args = (float(Fraction(r)), float(Fraction(t)))
    assert method.evaluate(-float(Fraction(v.lstrip("-"))), *args) \
        == method.evaluate(float(Fraction(v.lstrip("-"))), *args)


@pytest.mark.parametrize("v,t", [("0", "3600"), ("-0", "3600"), ("0.000", "1"),
                                 ("-0.000000000", "999999999"), ("000000000", "5"),
                                 ("12", "0"), ("12", "-0"), ("-12", "0.000000000"),
                                 ("999999999.999999999", "-0.000000000"), ("0", "0")])
def test_zero_voltage_or_duration_gives_exactly_positive_zero_energy(v, t):
    evaluation = _check_against_reference(v, "47", t)
    assert evaluation["display_value"] == "0" and evaluation["display_exact"] is True
    produced = _e(evaluation["result"])
    assert produced == 0.0 and math.copysign(1.0, produced) == 1.0


def test_negative_zero_at_the_adapter_and_owner_is_positive_zero():
    for v, t in ((-0.0, 5.0), (0.0, 5.0), (5.0, -0.0), (-5.0, 0.0), (-0.0, -0.0)):
        out = method.evaluate(v, 3.0, t)["e_load"]
        assert out == 0.0 and math.copysign(1.0, out) == 1.0
        result = dc.execute(BINDING, _request(v, 3.0, t))
        assert result["state"] == dc.STATE_SUCCESS
        assert math.copysign(1.0, _e(result)) == 1.0


# ==========================================================================
# 2. exact and rounded results; the display
# ==========================================================================
@pytest.mark.parametrize("v,r,t,display,exact", [
    ("2", "4", "1", "1", True), ("3.3", "1100", "100", "0.99", True),
    ("9", "0.001", "2", "162000", True), ("1", "8", "3", "0.375", True),
    ("1", "3", "1", "0.333333333333", False), ("2", "3", "1", "1.33333333333", False),
    ("10", "7", "60", "857.142857143", False),
    ("1", "0.000000003", "1", "333333333.333", False),
    ("999999999.999999999", "1", "1", "1 × 10^18", False),
    ("0.1", "0.3", "0.1", "0.00333333333333", False),
    ("12", "24", "0.000000001", "6 × 10^-9", True),
    ("1", "1", "999999999.999999999", "1000000000", False),
])
def test_exact_and_rounded_results(v, r, t, display, exact):
    evaluation = _check_against_reference(v, r, t)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (display, exact)


def test_round_half_to_even_at_twelve_significant_digits():
    assert dce.format_energy(Fraction("0.1234567890125")) == ("0.123456789012", False)
    assert dce.format_energy(Fraction("0.1234567890135")) == ("0.123456789014", False)
    assert dce.format_energy(Fraction("9.9999999999995")) == ("10", False)
    assert dce.format_energy(Fraction("9.999999999994")) == ("9.99999999999", False)
    assert dce.format_energy(Fraction(5, 2)) == ("2.5", True)
    assert dce.format_energy(Fraction(0)) == ("0", True)
    with pytest.raises(TypeError):
        dce.format_energy(2.5)


def test_tiny_and_large_energies_are_never_shown_as_zero_or_truncated():
    assert dce.format_energy(Fraction(1, 10 ** 6)) == ("0.000001", True)
    assert dce.format_energy(Fraction(1, 10 ** 7)) == ("1 × 10^-7", True)
    assert dce.format_energy(Fraction(10 ** 11)) == ("100000000000", True)
    assert dce.format_energy(Fraction(10 ** 12)) == ("1 × 10^12", True)
    for value in (Fraction(1, 10 ** 39), Fraction(7, 10 ** 25), Fraction(10 ** 36)):
        text, _exact = dce.format_energy(value)
        assert text != "0" and "10^" in text


@pytest.mark.parametrize("v,r,t", [
    ("0.000000001", "999999999999.999999999", "0.000000001"),   # smallest E ~ 1e-39
    ("999999999.999999999", "0.000000001", "999999999.999999999"),  # largest E ~ 1e36
    ("-999999999.999999999", "0.000000001", "999999999.999999999"),
    ("0.000000001", "0.000000001", "0.000000001"), ("999999999", "999999999999", "999999999"),
    ("1.000000001", "3", "0.1"), ("0.1", "0.3", "0.3"),
])
def test_representation_limits_are_calculated_and_representable(v, r, t):
    evaluation = _check_against_reference(v, r, t)
    produced = _e(evaluation["result"])
    assert math.isfinite(produced) and produced > 0.0
    assert Fraction(1, 10 ** 40) < Fraction(produced) < Fraction(10 ** 37)


def test_extremes_display_from_the_exact_decimal_value():
    small = _check_against_reference("0.000000001", "999999999999.999999999", "0.000000001")
    assert (small["display_value"], small["display_exact"]) == ("1 × 10^-39", False)
    large = _check_against_reference("999999999.999999999", "0.000000001",
                                     "999999999.999999999")
    assert (large["display_value"], large["display_exact"]) == ("1 × 10^36", False)


def test_random_admitted_decimals_against_the_independent_reference():
    rng = random.Random(20261025)
    worst = Fraction(0)
    for _ in range(600):
        iv = rng.randint(0, 10 ** rng.randint(1, 9) - 1)
        fv = rng.randint(0, 10 ** 9 - 1)
        v = "%s%d.%09d" % ("-" if rng.random() < 0.4 else "", iv, fv)
        ir = rng.randint(0, 10 ** rng.randint(1, 12) - 1)
        fr = rng.randint(1, 10 ** 9 - 1)
        r = "%d.%s" % (ir, ("%09d" % fr).rstrip("0") or "0")
        it = rng.randint(0, 10 ** rng.randint(1, 9) - 1)
        ft = rng.randint(0, 10 ** 9 - 1)
        t = "%d.%09d" % (it, ft) if rng.random() < 0.8 else str(it)
        if Fraction(r) <= 0:
            continue
        evaluation = _check_against_reference(v, r, t)
        reference = _reference(v, r, t)
        if reference:
            worst = max(worst, abs(Fraction(_e(evaluation["result"])) - reference) / reference)
    assert worst <= PROVEN_WORST_CASE


def test_the_error_bound_proof():
    u = Fraction(1, 2 ** 53)
    # three correctly rounded inputs (V twice) and one rounding of the result
    assert (1 + u) ** 4 / (1 - u) - 1 < PROVEN_WORST_CASE < DECIMAL_BOUND
    assert 1 - (1 - u) ** 4 / (1 + u) < PROVEN_WORST_CASE
    assert DECIMAL_BOUND == 8 * u and dce.DECIMAL_REFERENCE_BOUND == DECIMAL_BOUND
    assert method.RELATIVE_ERROR_BOUND == 2 * u


def test_the_bound_holds_for_worst_case_binary_rounding_of_every_input():
    # inputs whose binary64 rounding error is near its maximum, combined in the
    # directions that push the result furthest from the exact decimal value
    cases = ("0.1", "0.3", "0.7", "999999999.999999999", "0.000000001",
             "123456789.123456789", "1.000000001", "3.000000007")
    worst = Fraction(0)
    for v in cases:
        for r in cases:
            for t in cases:
                evaluation = _check_against_reference(v, r, t)
                reference = _reference(v, r, t)
                worst = max(worst, abs(Fraction(_e(evaluation["result"])) - reference)
                            / reference)
    assert worst <= PROVEN_WORST_CASE


# ==========================================================================
# 3. positive resistance, duration not negative; the adapter's acceptance
# ==========================================================================
@pytest.mark.parametrize("r", ["0", "-0", "0.000000000", "-1", "-0.000000001", "-24"])
def test_non_positive_resistance_is_refused_before_the_owner(r, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(r=r)
    assert evaluation["outcome"] == dce.RESISTANCE_NOT_POSITIVE
    assert evaluation["display_value"] is None and evaluation["result"] is None
    assert not calls


@pytest.mark.parametrize("t", ["-1", "-0.000000001", "-3600", "-999999999.999999999"])
def test_negative_duration_is_refused_before_the_owner(t, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(t=t)
    assert evaluation["outcome"] == dce.DURATION_NEGATIVE
    assert evaluation["display_value"] is None and evaluation["result"] is None
    assert evaluation["energy"] is None and not calls


def test_resistance_is_checked_before_the_duration():
    assert _evaluate(r="0", t="-1")["outcome"] == dce.RESISTANCE_NOT_POSITIVE
    assert _evaluate(r="-1", t="-1")["outcome"] == dce.RESISTANCE_NOT_POSITIVE


@pytest.mark.parametrize("t,display", [
    ("0", "0"), ("0.000000001", "6 × 10^-9"), ("999999999.999999999", "6000000000"),
    ("999999999", "5999999994"), ("1", "6")])
def test_duration_boundaries(t, display):
    evaluation = _check_against_reference("12", "24", t)
    assert evaluation["display_value"] == display


@pytest.mark.parametrize("r", ["0.000000001", "999999999999.999999999", "999999999999",
                               "0.1", "1"])
def test_resistance_boundaries(r):
    _check_against_reference("12", r, "3600")


@pytest.mark.parametrize("r", [0.0, -0.0, -1.0, -1e308])
def test_non_positive_resistance_is_declined_by_the_owner(r):
    result = dc.execute(BINDING, _request(12.0, r, 1.0))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None)


@pytest.mark.parametrize("t", [-1.0, -5e-324, -1e308])
def test_negative_duration_fails_closed_in_the_adapter(t):
    with pytest.raises(ArithmeticError):
        method.evaluate(12.0, 24.0, t)
    assert _failure(dc.execute(BINDING, _request(12.0, 24.0, t)))


@pytest.mark.parametrize("v,r,t", [(1e200, 1e-200, 1.0), (-1e300, 1.0, 1.0),
                                   (1e10, 1e-10, 1e300), (1e-200, 1e200, 1.0),
                                   (5e-324, 2.0, 1.0), (1.0, 3.0, 1e-320),
                                   (-1e-170, 1e10, 1.0), (1e-100, 1.0, 1e-200)])
def test_overflow_and_underflow_fail_closed_in_the_adapter(v, r, t):
    with pytest.raises(ArithmeticError):
        method.evaluate(v, r, t)
    assert _failure(dc.execute(BINDING, _request(v, r, t)))


def test_an_exactly_representable_subnormal_result_is_not_rounded_away():
    # acceptance is the relative bound, not a magnitude floor: an exact result
    # passes, a subnormal that loses precision does not (above)
    assert method.evaluate(1.0, 1.0, 5e-324)["e_load"] == 5e-324


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), "1", None, True])
@pytest.mark.parametrize("role", ["v", "t"])
def test_non_finite_and_non_numeric_inputs_are_refused(value, role):
    request = _request(v=value) if role == "v" else _request(t=value)
    result = dc.execute(BINDING, request)
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, None)


def test_adapter_refuses_non_float_or_out_of_domain_arguments():
    for args in ((12, 24.0, 1.0), (12.0, 24, 1.0), (12.0, 24.0, 1), ("12", 24.0, 1.0),
                 (12.0, 0.0, 1.0), (12.0, -1.0, 1.0), (12.0, 24.0, -1.0),
                 (float("nan"), 1.0, 1.0), (1.0, float("inf"), 1.0),
                 (1.0, 1.0, float("inf")), (1.0, 1.0, float("nan"))):
        with pytest.raises(ArithmeticError):
            method.evaluate(*args)
    with pytest.raises(TypeError):
        method.evaluate(12.0, 24.0)


def test_adapter_results_are_correctly_rounded_and_nonnegative():
    rng = random.Random(10)
    for _ in range(500):
        v = rng.uniform(-1e9, 1e9)
        r = 10 ** rng.uniform(-9, 12)
        t = rng.uniform(0, 1e9)
        exact = Fraction(v) * Fraction(v) * Fraction(t) / Fraction(r)
        produced = method.evaluate(v, r, t)["e_load"]
        assert produced == float(exact) and produced >= 0.0        # one correct rounding
        assert abs(Fraction(produced) - exact) <= exact * Fraction(1, 2 ** 53)


# ==========================================================================
# 4. the input grammar and strict capture
# ==========================================================================
@pytest.mark.parametrize("v,r,t", [
    ("+12", "24", "1"), ("1e3", "24", "1"), (" 12", "24", "1"), ("1,5", "24", "1"),
    ("١٢", "24", "1"), ("12.", "24", "1"), (".5", "24", "1"), ("--1", "24", "1"),
    ("inf", "24", "1"), ("nan", "24", "1"), ("1.0000000001", "24", "1"),
    ("1234567890", "24", "1"), ("12V", "24", "1"), ("", "24", "1"), ("12", "", "1"),
    ("12", "24Ω", "1"), ("12", "1e2", "1"), ("12", "1234567890123", "1"),
    ("12", "0.0000000001", "1"), ("12", "+24", "1"), ("−12", "24", "1"),
    ("1" * 65, "24", "1"),
    ("12", "24", ""), ("12", "24", "+1"), ("12", "24", "1e3"), ("12", "24", "1000000000"),
    ("12", "24", "0.0000000001"), ("12", "24", "1h"), ("12", "24", "60s"),
    ("12", "24", "1:00"), ("12", "24", "−1"), ("12", "24", "1.5.0"), ("12", "24", "inf"),
    ("12", "24", "nan"), ("12", "24", " 1"), ("12", "24", "٣٦٠٠"), ("12", "24", "--1"),
])
def test_malformed_values_are_invalid_and_never_reach_the_owner(v, r, t, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(v=v, r=r, t=t)
    assert evaluation["outcome"] == dce.INVALID_NUMERIC_INPUT, (v, r, t)
    assert evaluation["display_value"] is None and not calls


def test_strict_capture_refuses_duplicates_unknown_fields_and_bad_answers():
    good = {k: [v] for k, v in _form().items()}
    assert dce.capture_form(good) is not None
    for bad in (dict(good, **{dce.VALUE_FIELD % "t_duration": ["1", "2"]}),
                dict(good, **{dce.DECLARATION_FIELD % "resistive_load":
                              ["applies", "does_not_apply"]}),
                dict(good, unexpected=["1"]),
                dict(good, **{dce.SCREEN_FIELD % "safety_function": ["maybe"]}),
                dict(good, **{dce.DECLARATION_FIELD % "constant_power_duration": ["yes"]}),
                dict(good, **{dce.VALUE_FIELD % "e_load": ["6"]}),
                dict(good, **{dce.VALUE_FIELD % "p_load": ["6"]}),
                dict(good, **{"decl_absorbed_power_convention": ["applies"]}), [], None):
        assert dce.capture_form(bad) is None
    missing = {k: v for k, v in good.items()
               if k != dce.DECLARATION_FIELD % "constant_power_duration"}
    captured = dce.capture_form(missing)
    assert captured is not None
    assert dce.evaluate(captured, BINDING)["outcome"] == dce.NOT_DECLARED


# ==========================================================================
# 5. the owner: inventory, units, bindings and integrity (Correction 08)
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["outputs"] == {"e_load": {"value": 21600.0, "unit": "J",
                                            "provenance": "CALCULATED"}}
    assert [u["record_id"] for u in result["unit_records"]] == [
        "dcu:U011", "dcu:U012", "dcu:U014", "dcu:U015"]
    assert [q["source_ref"] for q in result["source_qualification"]] == [
        "DOE-ENG-S1", "DOE-ENG-S2"]
    assert {q["source_use_policy_ref"] for q in result["source_qualification"]} == {"dcu:SU015"}
    assert result["validation_status"] == "UNVALIDATED"
    assert (result["artifact_version"], result["implementation_version"]) == ("12", "1.11.0")
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_adds_exactly_energy_and_time():
    assert ("electrical:dc_resistive_load_energy", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 12
    assert dc.ADMITTED_QUANTITY_KINDS >= {"energy", "time"}
    assert len(dc.ADMITTED_QUANTITY_KINDS) == 18 and len(dc.ADMITTED_UNIT_TOKENS) == 20
    assert dc.ADMITTED_UNIT_TOKENS == {"N", "mm", "W", "K/W", "K", "N·mm", "N·m", "rad/s",
                                       "mV", "°C", "V", "Ω", "A", "J", "s", "h", "A·h",
                                       "kg", "N/m", "Hz"}
    # Correction 10 (§13I): the time kind gains h for the DC constant-current charge
    # duration only; this method's duration stays s and nothing maps one to the other
    assert dc.KIND_TOKEN_EXCEPTIONS == {"voltage": frozenset({"mV", "V"}),
                                        "time": frozenset({"s", "h"})}
    assert dc._CONDITIONS == ("greater_than_zero", "less_than_zero",
                              "within_zero_and_role")
    data = dc.load_artifact()
    record = _record(data)
    assert record["applicability"] == [
        {"role": "r_load", "condition": "greater_than_zero", "bound_role": None}]
    assert record["result_range"] == []
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"] + record["output_roles"]] == [
        ("v_load", "voltage", "V"), ("r_load", "electric_resistance", "Ω"),
        ("t_duration", "time", "s"), ("e_load", "energy", "J")]
    units = {u["unit_token"]: u for u in data["unit_records"]}
    assert (units["J"]["record_id"], units["J"]["quantity_kind"]) == ("dcu:U014", "energy")
    assert (units["s"]["record_id"], units["s"]["quantity_kind"]) == ("dcu:U015", "time")
    for token in ("J", "s"):
        assert units[token]["source_use_policy_ref"] == "dcu:SU014"
        assert "electronics_electrical:PR009" in units[token]["inspection_reference"]
        assert "no conversion is admitted" in units[token]["inspected_content"]
    # only this method uses the energy kind; the s token is shared with the
    # PWM average voltage method (on-time and period), and the time kind with
    # the DC constant-current charge method through its own h token
    energy_users = {m["method_id"] for m in data["methods"]
                    for role in m["input_roles"] + m["output_roles"]
                    if role["quantity_kind"] == "energy"}
    assert energy_users == {method.METHOD_ID}
    second_users = {m["method_id"] for m in data["methods"]
                    for role in m["input_roles"] + m["output_roles"]
                    if role["unit_token"] == "s"}
    assert second_users == {method.METHOD_ID, "electrical:pwm_average_voltage"}


@pytest.mark.parametrize("units,reason", [
    (("mV", "Ω", "s"), dc.UNIT_NOT_ADMITTED), (("A", "Ω", "s"), dc.UNIT_NOT_ADMITTED),
    (("V", "W", "s"), dc.UNIT_NOT_ADMITTED), (("V", "Ω", "J"), dc.UNIT_NOT_ADMITTED),
    (("V", "Ω", "K"), dc.UNIT_NOT_ADMITTED), (("V", "Ω", "rad/s"), dc.UNIT_NOT_ADMITTED),
    (("v", "Ω", "s"), dc.UNKNOWN_UNIT), (("V", "kΩ", "s"), dc.UNKNOWN_UNIT),
    (("V", "Ω", "S"), dc.UNKNOWN_UNIT), (("V", "Ω", "min"), dc.UNKNOWN_UNIT),
    (("V", "Ω", "h"), dc.UNIT_NOT_ADMITTED), (("V", "Ω", "ms"), dc.UNKNOWN_UNIT),
    (("V", "Ω", "A·h"), dc.UNIT_NOT_ADMITTED),
    (("V", "Ω", "sec"), dc.UNKNOWN_UNIT), (("V", "Ω", "Wh"), dc.UNKNOWN_UNIT),
])
def test_units_are_exact_with_no_alias_or_conversion(units, reason):
    result = dc.execute(BINDING, _request(units=units))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, reason, None)


def test_each_binding_executes_only_its_own_method():
    for binding in OTHER_BINDINGS:
        assert dc.execute(binding, _request())["reason"] == dc.OPERATION_NOT_ADMITTED
    swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, power_method.evaluate)
    assert _failure(dc.execute(swapped, _request()))
    assert dc.execute(dc.bind_method(method.METHOD_ID, "2.0", method.evaluate),
                      _request())["reason"] == dc.VERSION_MISMATCH


def test_app_wires_one_immutable_binding_per_method():
    assert webapp._DC_LOAD_ENERGY_BINDING.adapter_identity \
        == "engine.dc_resistive_load_energy_method.evaluate"
    with pytest.raises(AttributeError):
        webapp._DC_LOAD_ENERGY_BINDING.method_id = "x"
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 12
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("dc_resistive_load_energy_method", "engine.dc_resistive",
                   "electrical_content_config", "import fractions", "decimal",
                   "sqlite", "**2", "** 2"):
        assert banned not in owner_source.lower(), banned


def _owner_tamper(data, name):
    record = _record(data)
    if name == "ninth_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "electrical:dc_resistive_load_charge"
        data["methods"].append(extra)
    elif name == "output_kind":
        record["output_roles"][0]["quantity_kind"] = "power"
    elif name == "output_unit":
        record["output_roles"][0]["unit_token"] = "W"
    elif name == "duration_unit":
        record["input_roles"][2]["unit_token"] = "K"
    elif name == "policy_unresolved":
        record["source_qualification"][1]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "second_energy_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "J"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "Wh"
        data["unit_records"].append(extra)
    elif name == "second_time_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "s"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "min"
        data["unit_records"].append(extra)
    elif name == "extra_kind":
        data["quantity_kinds"].append({"quantity_kind": "electric_charge_density",
                                       "dimension": "T I L^-3"})
    elif name == "drop_time_kind":
        data["quantity_kinds"] = [k for k in data["quantity_kinds"]
                                  if k["quantity_kind"] != "time"]
    elif name == "unknown_condition":
        record["applicability"].append(
            {"role": "t_duration", "condition": "non_negative", "bound_role": None})
    elif name == "basis":
        data["source_use_policies"][-1]["inspection_basis"] = "EXECUTOR"
    return data


@pytest.mark.parametrize("name", ["ninth_method", "output_kind", "output_unit",
                                  "duration_unit", "policy_unresolved",
                                  "second_energy_unit", "second_time_unit", "extra_kind",
                                  "drop_time_kind", "unknown_condition", "basis"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), name))
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    assert _failure(dc.execute(BINDING, _request(), artifact_path=path))


def test_owner_v7_records_are_unchanged_by_the_eighth_admission():
    data = dc.load_artifact()
    assert data["artifact_version"] == "12"
    v7 = {"quantity_kinds": data["quantity_kinds"][:12],
          "unit_records": data["unit_records"][:13],
          "source_use_policies": data["source_use_policies"][:13],
          "methods": data["methods"][:7]}
    canonical = json.dumps(v7, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(canonical.encode()).hexdigest() == V7_RECORDS_DIGEST
    assert [k["quantity_kind"] for k in data["quantity_kinds"][12:14]] == ["energy", "time"]
    assert [u["record_id"] for u in data["unit_records"][13:15]] == ["dcu:U014", "dcu:U015"]
    assert [p["record_id"] for p in data["source_use_policies"][13:15]] == [
        "dcu:SU014", "dcu:SU015"]
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "dcenergy:SU002" in policies["dcu:SU014"]["inspected_content"]
    assert "DOE-ENG-S1 and DOE-ENG-S2 only" in policies["dcu:SU015"]["inspected_content"]
    assert "dcu:SU012 and dcu:SU013 (DC resistive load current and power) are not extended" \
        in policies["dcu:SU015"]["inspection_reference"]
    for text in ("constant_power_energy", "electrical_energy_time_reference_v1",
                 "electric_charge_reference_v1"):
        assert text not in json.dumps(data, ensure_ascii=False).lower()


# ==========================================================================
# 6. the method artifact and the consumer
# ==========================================================================
def test_method_artifact_loads_with_provenance_and_ip_boundary():
    data = dce.load_artifact()
    by_id = {r["record_id"]: r for r in data["sources"]}
    ohm = by_id["DOE-ENG-S1"]
    for phrase in ("E = I x R", "handbook page 14", "P = I x E", "handbook page 16",
                   "ARCHIVE - Canceled", "electronics_electrical:PR004",
                   "Not re-inspected by the executor", "not claimed that DOE printed them"):
        assert phrase in ohm["inspected_content"], phrase
    rate = by_id["DOE-ENG-S2"]
    for phrase in ("rate at which energy is transferred or used", "Module CP-05",
                   "printed page 8", "electronics_electrical:PR008",
                   "NOT claimed that DOE wrote E = P x t verbatim",
                   "power stays constant throughout the declared duration",
                   "no varying-power, average-power or integration treatment", "Archive"):
        assert phrase in rate["inspected_content"], phrase
    policy = by_id["dcenergy:SU001"]
    for phrase in ("not a legal opinion", "electronics_electrical:PR006",
                   "electronics_electrical:PR010", "public domain", "no blanket claim",
                   "is broadened beyond this method"):
        assert phrase in policy["inspected_content"], phrase
    units = by_id["NIST-JS-S1"]
    for phrase in ("Table 1", "second, symbol s", "Table 3", "joule, symbol J", "J = W x s",
                   "electronics_electrical:PR009", "Correction 08", "is unchanged"):
        assert phrase in units["inspected_content"], phrase
    assert "electronics_electrical:PR011" in by_id["dcenergy:SU002"]["inspected_content"]
    for phrase in ("ONLY for a power that stays constant throughout the declared duration t",
                   "no varying-power, average-power or integration treatment is derived",
                   "InventorAI's own statement"):
        assert phrase in data["method"]["derivation"], phrase


def test_no_protected_material_or_pack_change():
    for path in (dce.ARTIFACT_PATH, CONTRACT):
        text = path.read_text(encoding="utf-8").lower()
        assert "openstax.org" not in text and "modelica.org" not in text
    pack = (ROOT / "domains" / "electronics_electrical" / "domain.json").read_text(encoding="utf-8")
    assert "dc_resistive_load_energy" not in pack and "dcenergy:" not in pack
    provenance = json.loads((ROOT / "domains" / "domain_provenance.json")
                            .read_text(encoding="utf-8"))
    records = {r["record_id"]: r for r in provenance["records"]}
    assert "NOT added as units, quantities, bindings or methods of the shared deterministic " \
        "calculation / units owner" in records["electronics_electrical:PR009"]["notes"]
    assert records["electronics_electrical:PR008"]["notes"].endswith(
        "Bounded reference relationship only — no project-specific calculation and no "
        "applicability inference.")


@pytest.mark.parametrize("mutate", [
    lambda d: d["declarations"][4].__setitem__("accepted_value", "any power profile"),
    lambda d: d["declarations"][0].__setitem__("refusal", "NOT_DECLARED"),
    lambda d: d["declarations"].pop(),
    lambda d: d["numeric_domain"]["roles"][3].__setitem__("unit_token", "Wh"),
    lambda d: d["numeric_domain"]["roles"][2].__setitem__("unit_token", "h"),
    lambda d: d["numeric_domain"]["roles"][3].__setitem__("quantity_kind", "power"),
    lambda d: d["method"].__setitem__("executed_form", "e_load = v_load * t_duration / r_load"),
    lambda d: d["disclosure"].pop(),
    lambda d: d["disclosure"].__setitem__(5, "A battery of this capacity is enough."),
    lambda d: d["sources"][1].__setitem__("source_use_policy_ref", "dcpower:SU001"),
    lambda d: d["sources"].pop(),
    lambda d: d.__setitem__("artifact_version", "2"),
])
def test_method_artifact_tamper_is_knowledge_unavailable(mutate, monkeypatch):
    data = _method_artifact()
    mutate(data)
    with pytest.raises(dce.DcEnergyKnowledgeError):
        dce.validate_artifact(data)
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    result = dce.evaluate(_captured(), BINDING, artifact=data)
    assert result["outcome"] == dce.KNOWLEDGE_UNAVAILABLE and not calls
    assert result["display_value"] is None and result["energy"] is None


def test_unreadable_artifacts_give_no_number(tmp_path, monkeypatch):
    result = dce.evaluate(_captured(), BINDING, owner_artifact_path=tmp_path / "none.json")
    assert (result["outcome"], result["owner_state"], result["owner_reason"]) == (
        dce.KNOWLEDGE_UNAVAILABLE, dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE)
    assert result["display_value"] is None
    monkeypatch.setattr(dce, "ARTIFACT_PATH", tmp_path / "missing.json")
    assert _evaluate()["outcome"] == dce.KNOWLEDGE_UNAVAILABLE


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(decl={"steady_state_dc": ""}, screen={"safety_function": "yes"},
                     v="x", r="0", t="-1")["outcome"] == dce.NOT_DECLARED
    assert _evaluate(screen={"fire_or_overheating": "yes"},
                     decl={"constant_power_duration": "does_not_apply"},
                     v="x")["outcome"] == dce.ENGINEERING_REVIEW_REQUIRED
    for item in dce.SCREEN_ITEMS:
        assert _evaluate(screen={item: "yes"})["outcome"] \
            == dce.ENGINEERING_REVIEW_REQUIRED, item
    for decl in dce.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"}, v="x")["outcome"] \
            == dce.MODEL_NOT_SUPPORTED, decl
    assert _evaluate(v="x", r="0", t="-1")["outcome"] == dce.INVALID_NUMERIC_INPUT
    assert _evaluate(r="0", t="-1")["outcome"] == dce.RESISTANCE_NOT_POSITIVE
    assert _evaluate(t="-1")["outcome"] == dce.DURATION_NEGATIVE
    assert not calls


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, dce.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, dce.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, dce.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, dce.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, dce.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, dce.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, dce.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, dce.UNMAPPED_OWNER_OUTCOME),
    (dc.STATE_REFUSAL, dc.OPERATION_NOT_ADMITTED, dce.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome, monkeypatch):
    monkeypatch.setattr(dc, "execute", lambda *a, **k: {
        "state": state, "reason": reason, "outputs": None})
    result = _evaluate()
    assert (result["outcome"], result["owner_state"], result["owner_reason"]) \
        == (outcome, state, reason)
    assert result["result"] is None and result["display_value"] is None


@pytest.mark.parametrize("produced", [21600.001, 21599.99, -21600.0, 0.0, -0.0,
                                      21600.0 + 2.0 ** -30, "21600", None,
                                      float("nan"), float("inf")])
def test_decimal_reference_failure_fails_closed_with_no_number(produced, monkeypatch):
    real = dc.execute

    def tampered(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["e_load"]["value"] = produced
        return result
    monkeypatch.setattr(dc, "execute", tampered)
    result = _evaluate()
    assert result["outcome"] == dce.KNOWLEDGE_UNAVAILABLE
    assert result["owner_state"] == dc.STATE_SUCCESS          # preserved, not rewritten
    assert result["result"] is None and result["display_value"] is None


def test_zero_must_be_positive_zero_and_only_for_zero_voltage_or_duration(monkeypatch):
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: dict(
        real(b, r, artifact_path=artifact_path),
        outputs={"e_load": {"value": -0.0, "unit": "J", "provenance": "CALCULATED"}}))
    assert _evaluate(v="0")["outcome"] == dce.KNOWLEDGE_UNAVAILABLE
    assert _evaluate(t="0")["outcome"] == dce.KNOWLEDGE_UNAVAILABLE
    assert dce.agrees_with_reference(0.0, Fraction(0))
    assert not dce.agrees_with_reference(-0.0, Fraction(0))
    assert not dce.agrees_with_reference(1e-300, Fraction(0))
    assert not dce.agrees_with_reference(0.0, Fraction(1, 10 ** 39))
    assert not dce.agrees_with_reference(float("nan"), Fraction(1))


def test_consumer_sends_the_correctly_rounded_values_and_fixed_units(monkeypatch):
    seen = []
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: (
        seen.append(copy.deepcopy(r)), real(b, r, artifact_path=artifact_path))[1])
    _evaluate(v="-3.3", r="0.1", t="0.7")
    _evaluate(v="5", r="1", t="-0")
    assert seen[0] == {"method_id": method.METHOD_ID, "method_version": "1.0",
                       "inputs": {"v_load": {"value": float("-3.3"), "unit": "V"},
                                  "r_load": {"value": float("0.1"), "unit": "Ω"},
                                  "t_duration": {"value": float("0.7"), "unit": "s"}},
                       "subject_ref": None}
    # an exact-zero duration typed as -0 reaches the owner as +0.0
    zero = seen[1]["inputs"]["t_duration"]["value"]
    assert zero == 0.0 and math.copysign(1.0, zero) == 1.0


def test_requests_are_isolated_and_inputs_not_mutated():
    first = _captured(v="12", r="24", t="3600")
    before = copy.deepcopy(first)
    a = dce.evaluate(first, BINDING)
    b = dce.evaluate(_captured(v="-1", r="3", t="1"), BINDING)
    assert first == before
    assert a == dce.evaluate(_captured(v="12", r="24", t="3600"), BINDING)
    assert (a["display_value"], b["display_value"]) == ("21600", "0.333333333333")


def test_consumer_and_adapter_import_no_other_authority():
    import ast
    for module in (dce, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        for banned in ("cap13", "therm01", "tmp36", "dc_resistive_load_current",
                       "dc_resistive_load_power", "record_store", "safety_signal",
                       "requests", "urllib", "openai", "web", "flask", "random", "time",
                       "sqlite3", "domain_rules", "numpy", "scipy"):
            assert not any(banned == n or n.startswith(banned + ".") or banned in n
                           for n in names if n), (module.__name__, banned)


# ==========================================================================
# 7. EN / AR fidelity and the contracts
# ==========================================================================
def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_english_wording_equals_the_artifact():
    content = dce.load_artifact()
    assert ui_text.text("UI_DCE_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"]
        assert ui_text.text("UI_DCE_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."
    for entry in content["screen_items"]:
        value = entry["item"]
        assert ui_text.text("UI_DCE_SCREEN_" + entry["item_id"].upper(), "en") \
            == value[0].upper() + value[1:]


def test_arabic_wording_equals_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    assert ui_text.text("UI_DCE_DISCLOSURE", "ar").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$",
                           _contract_section("**A-2", "**A-3"), re.M))
    for decl, ref in dce.DECLARATIONS:
        assert ui_text.text("UI_DCE_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    screen = dict(re.findall(r"^\| (\w+) \| (.+?) \|$",
                             _contract_section("**A-3", "**A-4"), re.M))
    for item in dce.SCREEN_ITEMS:
        assert ui_text.text("UI_DCE_SCREEN_" + item.upper(), "ar") == screen[item], item
    s9 = _contract_section("## 9. Result", "## 9A.")
    assert [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)] \
        == dce.load_artifact()["disclosure"]
    s5 = _contract_section("## 5. Applicability", "## 6.")
    english = dict(re.findall(r"^\| (D-\d) \| `\w+` \| (.+?) \|$", s5, re.M))
    for entry in dce.load_artifact()["declarations"]:
        assert english[entry["contract_ref"]] == entry["accepted_value"]


def test_every_key_has_both_languages_and_no_battery_thermal_or_safety_claim():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_DCE_[A-Z0-9_]+)": \{', source)
    assert len(keys) >= 45
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("the load is safe", "will not overheat", "temperature will be",
                  "measured by inventorai", "guaranteed", "certified", "has been validated",
                  "recommended", "battery will last", "battery capacity is", "is enough",
                  "is rated", "runtime is"):
        assert claim not in english, claim
    for phrase in ("not a battery capacity", "runtime", "or a temperature",
                   "next engineering need", "remain unverified", "did not measure",
                   "not physical limits", "labelled rounded", "never negative",
                   "constant power", "converts no minutes or hours"):
        assert phrase in english, phrase


def test_correction_08_is_recorded_and_earlier_sections_unchanged():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 08" in body and "## 13G." in body
    section = _norm(body[body.index("## 13G."):body.index("## 14.")])
    for phrase in ("exactly eight", "`electrical:dc_resistive_load_energy`",
                   "Quantity kinds and exact unit tokens: exactly two added", "`dcu:U014`",
                   "`dcu:U015`", "`dcu:SU014`", "`dcu:SU015`", "content version `8`",
                   "`1.7.0`", "`electronics_electrical:PR009` keeps its own scope",
                   "NOT a generic owner policy", "No consumer imports another",
                   "within a relative `2^-50`", "never a negative zero",
                   "`J` is not related to `W`"):
        assert phrase in section, phrase
    assert "**Methods — exactly seven:**" in body[body.index("## 13F."):body.index("## 13G.")]
    assert "- Correction 08 (§13G) is Owner-authorized" in body


def test_method_contract_records_scope_provenance_and_exclusions():
    text = _norm(CONTRACT.read_text(encoding="utf-8"))
    for phrase in ("DOE-HDBK-1011/1-92", "DOE-HDBK-1010-92", "handbook page 14",
                   "handbook page 16", "printed page 8", "electronics_electrical:PR004",
                   "electronics_electrical:PR008", "electronics_electrical:PR009",
                   "electronics_electrical:PR006", "`PR010`",
                   "no project-specific calculation", "passive sign convention",
                   "Constant-power assumption", "`12 V / 24 Ω / 3600 s = 21600 J`",
                   "5.0000001", "Root only", "28-T3", "Battery / BMS",
                   "Representation limits are not physical limits", "labelled exact when",
                   "1 × 10^-39", "never a battery capacity", "`10^36` J",
                   "`DURATION_NEGATIVE`", "no external modelling library or code is used"):
        assert phrase in text, phrase


# ==========================================================================
# 8. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_electronics_root_journey_and_reference_values(elec):
    c, _aid, sid = elec
    assert "data-dce-link" in _page(c, sid)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-dce-form" in body and "checked" not in body
    assert "data-dce-value-note" in body and body.count('type="radio"') == 22
    for v, r, t, expected in REFERENCE:
        body = c.post(URL % sid, data=_form(v=v, r=r, t=t)).get_data(as_text=True)
        assert _value(body) == "%s J" % expected, (v, r, t)
        assert 'data-dce-exactness="exact"' in body
    body = c.post(URL % sid, data=_form(v="-12", r="24", t="3600")).get_data(as_text=True)
    assert _value(body) == "21600 J"
    body = c.post(URL % sid, data=_form(v="12", r="24", t="0")).get_data(as_text=True)
    assert _value(body) == "0 J" and 'data-dce-exactness="exact"' in body
    body = c.post(URL % sid, data=_form(v="1", r="3", t="1")).get_data(as_text=True)
    assert _value(body) == "0.333333333333 J"
    assert 'data-dce-exactness="rounded"' in body
    assert "data-dce-not-battery" in body
    assert "UNVALIDATED" in body and "NOT EVIDENCE" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_DCE_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert "DOE-HDBK-1011/1-92" in body and "DOE-HDBK-1010-92" in body and "NIST" in body
    assert "electrical:dc_resistive_load_energy" in body
    assert '<bdi dir="ltr" data-dce-echo-value>1</bdi>' in body


@pytest.mark.parametrize("over,outcome", [
    ({"r": "0"}, "RESISTANCE_NOT_POSITIVE"),
    ({"r": "-24"}, "RESISTANCE_NOT_POSITIVE"),
    ({"t": "-1"}, "DURATION_NEGATIVE"),
    ({"t": "1h"}, "INVALID_NUMERIC_INPUT"),
    ({"v": "1e3"}, "INVALID_NUMERIC_INPUT"),
    ({"t": ""}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"battery_or_storage_cell": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"constant_power_duration": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"absorbed_energy_convention": ""}}, "NOT_DECLARED"),
])
def test_non_success_shows_one_reason_and_no_number(elec, over, outcome):
    c, _aid, sid = elec
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert ui_text.text("UI_DCE_OUTCOME_" + outcome, "en") in html.unescape(body)
    assert _value(body) is None
    assert body.count("data-dce-outcome") == 1 and "data-dce-result" not in body


def test_mechanical_root_is_not_eligible_but_a_declared_part_is(mech, monkeypatch):
    c, _aid, sid = mech
    assert "data-dce-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._dce, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-dce-scope-note" in body
        assert "data-dce-form" not in body and _value(body) is None
    # DC-RESISTIVE-LOAD-INTEGRATED-PART-01: on an integrated project with a
    # Mechanical focus the declared Electrical / Electronics part is offered the
    # calculation (tests/test_dc_resistive_load_integrated_part.py)
    c2, _ = _client_for("dce-part-mech@example.com")
    sid2 = _integrated(c2, MECH)
    assert webapp._dce_eligible(sid2)
    assert "data-dce-link" in _page(c2, sid2)
    assert not called
    c3, _ = _client_for("dce-part-elec@example.com")
    assert webapp._dce_eligible(_integrated(c3, ELEC))


def test_unreadable_root_domain_grants_nothing(elec, monkeypatch):
    c, _aid, sid = elec

    def broken(_sid):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(webapp, "_cap12_root_domain", broken)
    assert not webapp._dce_eligible(sid)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-dce-form" not in body and _value(body) is None


def test_csrf_authorization_and_malformed_requests(elec):
    c, _aid, sid = elec
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("dce-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302 and "data-dce" not in r.get_data(as_text=True)
    for bad in (dict(_form(), unexpected="1"),
                dict(_form(), screen_safety_function="maybe"),
                dict(_form(), value_e_load="6")):
        r = c.post(URL % sid, data=bad)
        assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    from werkzeug.datastructures import MultiDict
    r = c.post(URL % sid, data=MultiDict(list(_form().items())
                                         + [(dce.VALUE_FIELD % "t_duration", "13")]))
    assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    body = c.post(URL % sid, data=_form(t="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body
    assert c.get(URL % sid).headers["Cache-Control"] == "no-store"


@pytest.mark.parametrize("over", [{}, {"t": "-5"}, {"screen": {"safety_function": "yes"}}])
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
    start = src.index("# DC-RESISTIVE-LOAD-ENERGY-01 — DC Resistive Load Energy")
    section = src[start:src.index("# DC-CONSTANT-CURRENT-CHARGE-01 —", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "_cap13", "_tmp36", "_dcl.", "_dcp.", "_dcp_",
                   "load_project_subsystems", "request.args", "cap09",
                   "success_criteria", "redirect("):
        assert banned not in section, banned
    assert section.count("_dcalc.bind_method(") == 1
    assert [r.rule for r in webapp.app.url_map.iter_rules() if "dc-load-energy" in r.rule] \
        == ["/session/<sid>/dc-load-energy"] * 2
    for template in ("deliverable.html", "report.html", "success_criteria.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "dc-load-energy" not in path.read_text(encoding="utf-8").lower()


def test_existing_seven_calculations_are_unchanged(mech, elec):
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
    body = c2.post("/session/%s/dc-load-power" % sid2,
                   data=_power_form(v="12", r="24")).get_data(as_text=True)
    assert 'data-dcp-result-value><bdi dir="ltr">6 W</bdi>' in body


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_arabic_isolation_and_signed_input(elec, lang):
    c, _aid, sid = elec
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form(v="-12", r="24", t="3600")).get_data(as_text=True)
    assert _value(body) == "21600 J"
    assert '<bdi dir="ltr" data-dce-echo-value>-12</bdi>' in body
    if lang == "ar":
        assert 'dir="rtl"' in body
        isolated = [html.unescape(run)
                    for run in re.findall(r'<bdi dir="ltr">([^<]*)</bdi>', body)]
        for token in ("UNVALIDATED", "NOT EVIDENCE", "DOE-HDBK-1010-92", "(Ω)", "(J)", "(s)",
                      "(t)"):
            assert any(token in run for run in isolated), token
        assert any(run == "E = V² × t / R = P × t" for run in isolated)
        stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
        for item in ui_text.text("UI_DCE_DISCLOSURE", "ar").split("\n\n"):
            assert _norm(item) in _norm(stripped), item[:30]
        refusal = c.post(URL % sid, data=_form(t="-1")).get_data(as_text=True)
        assert ui_text.text("UI_DCE_OUTCOME_DURATION_NEGATIVE", "ar") \
            in html.unescape(re.sub(r"<[^>]+>", "", refusal))
        assert _value(refusal) is None
