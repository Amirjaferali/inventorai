# -*- coding: utf-8 -*-
"""Electrical / Electronics - PWM Average Voltage, Slice 1 (directly owning tests).

PWM-AVERAGE-VOLTAGE-01. The shared deterministic calculation / units owner after
the bounded eleventh admission of calc/units Correction 11 (§13J); the ONE
method ``electrical:pwm_average_voltage`` 1.0
(``engine/pwm_average_voltage_method.py``) and its ONE consumer
(``engine/pwm_average_voltage.py`` + the request-local page).

Scientific reference: a periodic voltage equal to E for an interval and zero
otherwise has an average proportional to the on-time fraction (NASA TN D-5643,
research record SRC-042), restated by InventorAI as V_avg = V_supply x t_on / T
for an ideal two-level waveform. The numerical tests use an INDEPENDENT decimal
reference: every expected average and every expected display is formed with
``decimal.Decimal`` from the typed decimal strings, never from the consumer's
or the adapter's own arithmetic. Synthetic data.
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
from engine import pwm_average_voltage as pwm
from engine import pwm_average_voltage_method as method
from engine import dc_constant_current_charge_method as charge_method
from engine import dc_resistive_load_energy_method as energy_method
from engine import dc_resistive_load_power_method as power_method
from engine import dc_resistive_load_current_method as current_method
from engine import cap13_static_reactions_method as cap13_method
from engine import cap13_planar_moment_method as moment_method
from engine import cap13_planar_required_force_method as force_method
from engine import cap13_rotational_load_method as rotational_method
from engine import therm01_conduction_method as therm_method
from engine import tmp36_nominal_temperature_method as tmp36_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _corrupt, _owner_spy, _part_line, MECH, ELEC, PARTS, CTRL, HOSTILE)
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_therm01_temperature_difference import _form as _therm_form
from tests.test_cap13_planar_moment import _form as _moment_form
from tests.test_cap13_planar_required_force import _form as _force_form
from tests.test_cap13_rotational_load import _form as _rotational_form
from tests.test_tmp36_nominal_temperature import _form as _tmp36_form
from tests.test_dc_resistive_load_current import _form as _current_form
from tests.test_dc_resistive_load_power import _form as _power_form
from tests.test_dc_resistive_load_energy import _form as _energy_form
from tests.test_dc_constant_current_charge import _form as _charge_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "docs" / "governance" / "ELECTRICAL_PWM_AVERAGE_VOLTAGE_METHOD_CONTRACT.md"
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
URL = "/session/%s/pwm-average-voltage"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
OTHER_BINDINGS = (
    dc.bind_method(cap13_method.METHOD_ID, "1.0", cap13_method.evaluate),
    dc.bind_method(therm_method.METHOD_ID, "1.0", therm_method.evaluate),
    dc.bind_method(moment_method.METHOD_ID, "1.0", moment_method.evaluate),
    dc.bind_method(rotational_method.METHOD_ID, "1.0", rotational_method.evaluate),
    dc.bind_method(tmp36_method.METHOD_ID, "1.0", tmp36_method.evaluate),
    dc.bind_method(current_method.METHOD_ID, "1.0", current_method.evaluate),
    dc.bind_method(power_method.METHOD_ID, "1.0", power_method.evaluate),
    dc.bind_method(energy_method.METHOD_ID, "1.0", energy_method.evaluate),
    dc.bind_method(force_method.METHOD_ID, "1.0", force_method.evaluate),
    dc.bind_method(charge_method.METHOD_ID, "1.0", charge_method.evaluate))
# The reference vectors (V, s, s -> V).
REFERENCE = (("12", "0.25", "1", "3"), ("5", "0.5", "2", "1.25"),
             ("3.3", "0.001", "0.004", "0.825"), ("24", "1", "1", "24"))
DECIMAL_BOUND = Fraction(1, 2 ** 50)
PROVEN_WORST_CASE = Fraction(40000001, 10000000) * Fraction(1, 2 ** 53)
# The content-version-10 records (quantity kinds, unit records, source-use
# policies and the ten method records), pinned by digest: Correction 11 only
# appends after them.
V10_RECORDS_DIGEST = "0f06614535cd83ef44cd436978855e1c3a4a9154b45474fe66e1c4a95c51a331"
# Wording the method must never use for its result.
FORBIDDEN = ("equivalent dc voltage is", "the load experiences", "motor speed is",
             "average power is", "rms voltage is", "duty cycle:", "battery capacity",
             "runtime")


# --------------------------------------------------------------------------
# helpers: the independent decimal reference
# --------------------------------------------------------------------------
_EXACT = Context(prec=200, rounding=ROUND_HALF_EVEN)
_TWELVE = Context(prec=12, rounding=ROUND_HALF_EVEN)


def _reference(v, on, period):
    """The exact V x t_on / T as a Fraction, from Decimal alone."""
    return Fraction(Decimal(v)) * Fraction(Decimal(on)) / Fraction(Decimal(period))


def _reference_display(v, on, period):
    """The expected (text, exact) display, from Decimal alone: V x t_on / T
    correctly rounded to 12 significant digits (half to even), trailing zeros
    removed, plain for 1e-6 <= V < 1e12 and 'm × 10^e' otherwise."""
    if Decimal(v) == 0 or Decimal(on) == 0:
        return "0", True
    product = _EXACT.multiply(Decimal(v), Decimal(on))          # exact: <= 36 digits
    rounded = _TWELVE.divide(product, Decimal(period))
    exact = Fraction(rounded) == _reference(v, on, period)
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


def _request(v=12.0, on=0.25, period=1.0, units=("V", "s", "s"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"v_supply": {"value": v, "unit": units[0]},
                      "t_on": {"value": on, "unit": units[1]},
                      "t_period": {"value": period, "unit": units[2]}},
           "subject_ref": None}
    req.update(over)
    return req


def _v(result):
    return result["outputs"]["v_avg"]["value"]


def _failure(result):
    return (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def _form(v="12", on="0.25", period="1", decl=None, screen=None):
    form = {pwm.DECLARATION_FIELD % d: pwm.ANSWER_APPLIES for d in pwm.DECLARATION_IDS}
    form.update({pwm.SCREEN_FIELD % s: pwm.SCREEN_NO for s in pwm.SCREEN_ITEMS})
    form[pwm.VALUE_FIELD % "v_supply"] = v
    form[pwm.VALUE_FIELD % "t_on"] = on
    form[pwm.VALUE_FIELD % "t_period"] = period
    for key, value in (decl or {}).items():
        form[pwm.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[pwm.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = pwm.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return pwm.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _method_artifact():
    return json.loads(pwm.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data):
    target = tmp_path / "a.json"
    target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return target


def _value(body):
    marker = 'data-pwm-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def _check_against_reference(v, on, period):
    """One typed triple through the whole consumer: success, the owner result
    within the decimal bound and never above the supply level, the display
    equal to the independent reference."""
    evaluation = _evaluate(v=v, on=on, period=period)
    assert evaluation["outcome"] == pwm.OUTCOME_SUCCESS, (v, on, period)
    reference = _reference(v, on, period)
    produced = _v(evaluation["result"])
    assert math.copysign(1.0, produced) == 1.0, (v, on, period)   # never negative, no -0
    assert produced <= float(Fraction(Decimal(v)))
    if reference == 0:
        assert produced == 0.0
    else:
        error = abs(Fraction(produced) - reference) / reference
        assert error <= PROVEN_WORST_CASE < DECIMAL_BOUND, (v, on, period)
        assert produced > 0
    assert (evaluation["display_value"], evaluation["display_exact"]) \
        == _reference_display(v, on, period), (v, on, period)
    assert evaluation["average"] == reference
    return evaluation


@pytest.fixture
def elec():
    c, aid = _client_for("pwm-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def mech():
    c, aid = _client_for("pwm-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": MECH})


# ==========================================================================
# 1. the reference vectors and the fixed boundary cases
# ==========================================================================
@pytest.mark.parametrize("v,on,period,expected", REFERENCE)
def test_reference_vectors_at_owner_adapter_and_consumer(v, on, period, expected):
    exact = _reference(v, on, period)
    produced = method.evaluate(float(v), float(on), float(period))["v_avg"]
    assert abs(Fraction(produced) - exact) <= exact * Fraction(1, 2 ** 52)
    result = dc.execute(BINDING, _request(float(v), float(on), float(period)))
    assert result["state"] == dc.STATE_SUCCESS and _v(result) == produced
    evaluation = _check_against_reference(v, on, period)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (expected, True)


@pytest.mark.parametrize("v,on", [("0", "0.25"), ("-0", "0.25"), ("0.000", "1"),
                                  ("-0.000000000", "0.999999999"), ("000000000", "0.5"),
                                  ("12", "0"), ("12", "-0"), ("12", "0.000000000"),
                                  ("999999999.999999999", "-0.000000000"), ("0", "0")])
def test_zero_supply_or_zero_on_time_gives_exactly_positive_zero(v, on):
    evaluation = _check_against_reference(v, on, "1")
    assert evaluation["display_value"] == "0" and evaluation["display_exact"] is True
    produced = _v(evaluation["result"])
    assert produced == 0.0 and math.copysign(1.0, produced) == 1.0


@pytest.mark.parametrize("v,period", [("12", "1"), ("5", "0.004"), ("0.7", "0.3"),
                                      ("999999999.999999999", "999999999.999999999"),
                                      ("0.000000001", "0.000000001"),
                                      ("123456789.123456789", "0.1")])
def test_on_time_equal_to_period_gives_exactly_the_supply_level(v, period):
    evaluation = _check_against_reference(v, period, period)
    assert evaluation["average"] == Fraction(Decimal(v))
    assert _v(evaluation["result"]) == float(Fraction(Decimal(v)))
    assert evaluation["display_exact"] is True or len(v.replace(".", "")) > 12
    produced = method.evaluate(float(Fraction(Decimal(v))), float(Fraction(Decimal(period))),
                               float(Fraction(Decimal(period))))["v_avg"]
    assert produced == float(Fraction(Decimal(v)))


def test_negative_zero_at_the_adapter_and_owner_is_positive_zero():
    for v, on in ((-0.0, 0.5), (0.0, 0.5), (5.0, -0.0), (-0.0, -0.0), (0.0, 0.0)):
        out = method.evaluate(v, on, 1.0)["v_avg"]
        assert out == 0.0 and math.copysign(1.0, out) == 1.0
        result = dc.execute(BINDING, _request(v, on, 1.0))
        assert result["state"] == dc.STATE_SUCCESS
        assert math.copysign(1.0, _v(result)) == 1.0


def test_the_ratio_exists_only_inside_the_product_and_nothing_is_converted():
    # no duty-cycle quantity, percentage, frequency or scale factor anywhere in
    # the executable code: every numeric literal is inspected
    import ast
    for module in (pwm, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        numbers = {node.value for node in ast.walk(tree)
                   if isinstance(node, ast.Constant) and isinstance(node.value, (int, float))
                   and not isinstance(node.value, bool)}
        assert not numbers & {100, 100.0, 1000, 1000.0, 0.001, 0.000001, 60, 3600}, numbers
    assert _evaluate(v="10", on="0.5", period="1")["display_value"] == "5"       # not "50 %"
    assert _evaluate(v="10", on="1", period="1000")["display_value"] == "0.01"


# ==========================================================================
# 2. exact and rounded results; the display
# ==========================================================================
@pytest.mark.parametrize("v,on,period,display,exact", [
    ("12", "1", "3", "4", True), ("5", "1", "3", "1.66666666667", False),
    ("10", "0.3", "0.7", "4.28571428571", False), ("1", "1", "7", "0.142857142857", False),
    ("0.000000001", "0.000000001", "999999999.999999999", "1 × 10^-27", False),
    ("999999999.999999999", "1", "1", "1000000000", False),
    ("999999999.999999999", "999999999.999999999", "999999999.999999999",
     "1000000000", False),
    ("123456789.123456789", "0.5", "1", "61728394.5617", False),
    ("1.5", "0.1", "1", "0.15", True), ("0.7", "0.7", "1", "0.49", True),
    ("3.3", "0.001", "1", "0.0033", True), ("1", "0.000001", "1", "0.000001", True),
    ("1", "0.0000001", "1", "1 × 10^-7", True), ("100000000", "1", "1", "100000000", True),
])
def test_exact_and_rounded_results(v, on, period, display, exact):
    evaluation = _check_against_reference(v, on, period)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (display, exact)


def test_round_half_to_even_at_twelve_significant_digits():
    assert pwm.format_average(Fraction("0.1234567890125")) == ("0.123456789012", False)
    assert pwm.format_average(Fraction("0.1234567890135")) == ("0.123456789014", False)
    assert pwm.format_average(Fraction("9.9999999999995")) == ("10", False)
    assert pwm.format_average(Fraction("9.999999999994")) == ("9.99999999999", False)
    assert pwm.format_average(Fraction(5, 2)) == ("2.5", True)
    assert pwm.format_average(Fraction(0)) == ("0", True)
    with pytest.raises(TypeError):
        pwm.format_average(2.5)


def test_tiny_and_large_averages_are_never_shown_as_zero_or_truncated():
    assert pwm.format_average(Fraction(1, 10 ** 6)) == ("0.000001", True)
    assert pwm.format_average(Fraction(1, 10 ** 7)) == ("1 × 10^-7", True)
    assert pwm.format_average(Fraction(10 ** 11)) == ("100000000000", True)
    assert pwm.format_average(Fraction(10 ** 12)) == ("1 × 10^12", True)
    for value in (Fraction(1, 10 ** 27), Fraction(7, 10 ** 20), Fraction(10 ** 9)):
        text, _exact = pwm.format_average(value)
        assert text != "0"


@pytest.mark.parametrize("v,on,period", [
    ("0.000000001", "0.000000001", "999999999.999999999"),      # smallest V_avg = 1e-27
    ("999999999.999999999", "999999999.999999999", "999999999.999999999"),   # largest
    ("999999999.999999999", "0.000000001", "0.000000001"),
    ("0.000000001", "0.000000001", "0.000000001"), ("1.000000001", "0.1", "0.3"),
])
def test_representation_limits_are_calculated_and_representable(v, on, period):
    evaluation = _check_against_reference(v, on, period)
    produced = _v(evaluation["result"])
    assert math.isfinite(produced) and produced > 0.0
    assert Fraction(1, 10 ** 28) < Fraction(produced) < Fraction(10 ** 10)


def test_random_admitted_decimals_against_the_independent_reference():
    rng = random.Random(20261029)
    worst = Fraction(0)
    for _ in range(600):
        iv = rng.randint(0, 10 ** rng.randint(1, 9) - 1)
        fv = rng.randint(0, 10 ** 9 - 1)
        v = "%d.%09d" % (iv, fv) if rng.random() < 0.8 else str(iv)
        ip = rng.randint(0, 10 ** rng.randint(1, 9) - 1)
        fp = rng.randint(1, 10 ** 9 - 1)
        period = "%d.%s" % (ip, ("%09d" % fp).rstrip("0") or "0")
        on_fraction = Fraction(rng.randint(0, 10 ** 9), 10 ** 9)
        on = Fraction(period) * on_fraction
        on = "%s" % (Decimal(on.numerator) / Decimal(on.denominator)).quantize(Decimal("1e-9"))
        if Fraction(on) > Fraction(period) or Fraction(on) < 0:
            continue
        evaluation = _check_against_reference(v, on, period)
        reference = _reference(v, on, period)
        if reference:
            worst = max(worst, abs(Fraction(_v(evaluation["result"])) - reference) / reference)
    assert worst <= PROVEN_WORST_CASE


def test_the_error_bound_proof():
    u = Fraction(1, 2 ** 53)
    # three correctly rounded inputs and one rounding of the result
    assert (1 + u) ** 3 / (1 - u) - 1 < PROVEN_WORST_CASE < DECIMAL_BOUND
    assert 1 - (1 - u) ** 3 / (1 + u) < PROVEN_WORST_CASE
    assert DECIMAL_BOUND == 8 * u and pwm.DECIMAL_REFERENCE_BOUND == DECIMAL_BOUND
    assert method.RELATIVE_ERROR_BOUND == 2 * u


def test_the_bound_holds_for_worst_case_binary_rounding_of_every_input():
    cases = ("0.1", "0.3", "0.7", "999999999.999999999", "0.000000001",
             "123456789.123456789", "1.000000001", "3.000000007")
    worst = Fraction(0)
    for v in cases:
        for on in cases:
            for period in cases:
                if Fraction(on) > Fraction(period):
                    continue
                evaluation = _check_against_reference(v, on, period)
                reference = _reference(v, on, period)
                worst = max(worst, abs(Fraction(_v(evaluation["result"])) - reference)
                            / reference)
    assert worst <= PROVEN_WORST_CASE


# ==========================================================================
# 3. the ordered exact-decimal screening; the adapter's acceptance
# ==========================================================================
@pytest.mark.parametrize("v", ["-1", "-0.000000001", "-12", "-999999999.999999999"])
def test_negative_supply_is_refused_before_the_owner(v, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(v=v)
    assert evaluation["outcome"] == pwm.VOLTAGE_NEGATIVE
    assert evaluation["display_value"] is None and evaluation["result"] is None
    assert evaluation["average"] is None and not calls


@pytest.mark.parametrize("period", ["0", "-0", "0.000000000", "-1", "-0.000000001"])
def test_non_positive_period_is_refused_before_the_owner(period, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(on="0", period=period)
    assert evaluation["outcome"] == pwm.PERIOD_NOT_POSITIVE
    assert evaluation["display_value"] is None and not calls


@pytest.mark.parametrize("on", ["-1", "-0.000000001", "-0.25"])
def test_negative_on_time_is_refused_before_the_owner(on, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(on=on)
    assert evaluation["outcome"] == pwm.ON_TIME_NEGATIVE
    assert evaluation["display_value"] is None and not calls


@pytest.mark.parametrize("on,period", [("1.000000001", "1"), ("2", "1"), ("0.5", "0.25"),
                                       ("999999999.999999999", "999999999.999999998")])
def test_on_time_above_the_period_is_refused_before_the_owner(on, period, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(on=on, period=period)
    assert evaluation["outcome"] == pwm.ON_TIME_EXCEEDS_PERIOD
    assert evaluation["display_value"] is None and not calls


def test_screening_order_is_supply_then_period_then_on_time_then_bound():
    assert _evaluate(v="-1", on="-1", period="-1")["outcome"] == pwm.VOLTAGE_NEGATIVE
    assert _evaluate(v="0", on="-1", period="-1")["outcome"] == pwm.PERIOD_NOT_POSITIVE
    assert _evaluate(v="0", on="-1", period="1")["outcome"] == pwm.ON_TIME_NEGATIVE
    assert _evaluate(v="0", on="2", period="1")["outcome"] == pwm.ON_TIME_EXCEEDS_PERIOD
    assert _evaluate(v="0", on="1", period="1")["outcome"] == pwm.OUTCOME_SUCCESS


@pytest.mark.parametrize("on,display", [
    ("0", "0"), ("0.000000001", "1.2 × 10^-8"), ("0.999999999", "11.999999988"),
    ("1", "12"), ("0.5", "6")])
def test_on_time_boundaries(on, display):
    assert _check_against_reference("12", on, "1")["display_value"] == display


@pytest.mark.parametrize("v,on,period", [(-1.0, 0.5, 1.0), (-5e-324, 0.5, 1.0),
                                         (12.0, -0.5, 1.0), (12.0, 1.5, 1.0),
                                         (12.0, 0.5, 0.0), (12.0, 0.5, -1.0),
                                         (12.0, 0.5, -0.0), (12.0, 1.0000000000000002, 1.0)])
def test_out_of_domain_inputs_fail_closed_in_the_adapter(v, on, period):
    with pytest.raises(ArithmeticError):
        method.evaluate(v, on, period)
    result = dc.execute(BINDING, _request(v, on, period))
    assert result["outputs"] is None
    assert result["state"] in (dc.STATE_FAILURE, dc.STATE_UNABLE)


@pytest.mark.parametrize("on,period", [(1.5, 1.0), (0.5, 0.0), (0.5, -1.0), (-0.5, 1.0)])
def test_owner_applicability_declines_before_the_adapter(on, period, monkeypatch):
    called = []
    monkeypatch.setattr(method, "evaluate", lambda *a, **k: called.append(1))
    result = dc.execute(BINDING, _request(12.0, on, period))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None)
    assert not called


@pytest.mark.parametrize("v,on,period", [(1e-200, 1e-200, 1e100), (5e-324, 0.5, 1.0),
                                         (1e-170, 1e-170, 1.0), (0.3, 5e-324, 1.0)])
def test_underflow_of_a_nonzero_result_fails_closed_in_the_adapter(v, on, period):
    with pytest.raises(ArithmeticError):
        method.evaluate(v, on, period)
    assert _failure(dc.execute(BINDING, _request(v, on, period)))


@pytest.mark.parametrize("v,on,period", [(1e300, 1e300, 1e-300), (1e308, 1.0, 1e-10),
                                         (1.7976931348623157e308, 1.0, 1.0)])
def test_overflow_is_unreachable_inside_the_admitted_domain(v, on, period):
    # v_avg = v_supply × t_on / T never exceeds v_supply while 0 ≤ t_on ≤ T, so a
    # binary64 supply level can never overflow; an on-time above the period is
    # outside the domain and is refused before the adapter runs (owner
    # applicability), while the largest finite supply level with t_on = T is
    # returned exactly.
    if on > period:
        with pytest.raises(ArithmeticError):
            method.evaluate(v, on, period)
        result = dc.execute(BINDING, _request(v, on, period))
        assert (result["state"], result["reason"], result["outputs"]) == (
            dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None)
    else:
        assert method.evaluate(v, on, period)["v_avg"] == v
        result = dc.execute(BINDING, _request(v, on, period))
        assert result["state"] == dc.STATE_SUCCESS and _v(result) == v


def test_an_exactly_representable_subnormal_result_is_not_rounded_away():
    assert method.evaluate(5e-324, 1.0, 1.0)["v_avg"] == 5e-324


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), "1", None, True])
@pytest.mark.parametrize("role", ["v", "on", "period"])
def test_non_finite_and_non_numeric_inputs_are_refused(value, role):
    request = _request(**{role: value})
    result = dc.execute(BINDING, request)
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, None)


def test_adapter_refuses_non_float_or_out_of_domain_arguments():
    for args in ((12, 0.5, 1.0), (12.0, 1, 1.0), (12.0, 0.5, 1), ("12", 0.5, 1.0),
                 (-1.0, 0.5, 1.0), (12.0, -1.0, 1.0), (12.0, 2.0, 1.0), (12.0, 0.5, 0.0),
                 (float("nan"), 0.5, 1.0), (1.0, float("inf"), 1.0), (1.0, 0.5, float("nan"))):
        with pytest.raises(ArithmeticError):
            method.evaluate(*args)
    with pytest.raises(TypeError):
        method.evaluate(12.0, 0.5)


def test_adapter_results_are_correctly_rounded_and_bounded():
    rng = random.Random(11)
    for _ in range(500):
        v = rng.uniform(0, 1e9)
        period = 10 ** rng.uniform(-9, 9)
        on = rng.uniform(0, period)
        exact = Fraction(v) * Fraction(on) / Fraction(period)
        produced = method.evaluate(v, on, period)["v_avg"]
        assert produced == float(exact) and 0.0 <= produced <= v     # one correct rounding
        assert abs(Fraction(produced) - exact) <= exact * Fraction(1, 2 ** 53)


# ==========================================================================
# 4. the input grammar and strict capture
# ==========================================================================
@pytest.mark.parametrize("v,on,period", [
    ("+12", "0.25", "1"), ("1e1", "0.25", "1"), (" 12", "0.25", "1"), ("1,5", "0.25", "1"),
    ("١٢", "0.25", "1"), ("12.", "0.25", "1"), (".5", "0.25", "1"), ("--1", "0.25", "1"),
    ("inf", "0.25", "1"), ("nan", "0.25", "1"), ("1.0000000001", "0.25", "1"),
    ("1234567890", "0.25", "1"), ("12V", "0.25", "1"), ("", "0.25", "1"), ("−12", "0.25", "1"),
    ("1" * 65, "0.25", "1"),
    ("12", "", "1"), ("12", "25%", "1"), ("12", "+0.25", "1"), ("12", "250ms", "1"),
    ("12", "0.0000000001", "1"), ("12", "1e-1", "1"), ("12", "٠٫٢٥", "1"), ("12", "−0.25", "1"),
    ("12", "0.25", ""), ("12", "0.25", "1s"), ("12", "0.25", "1kHz"), ("12", "0.25", "1000000000"),
    ("12", "0.25", "1.5.0"), ("12", "0.25", "inf"), ("12", "0.25", " 1"), ("12", "0.25", "1."),
])
def test_malformed_values_are_invalid_and_never_reach_the_owner(v, on, period, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(v=v, on=on, period=period)
    assert evaluation["outcome"] == pwm.INVALID_NUMERIC_INPUT, (v, on, period)
    assert evaluation["display_value"] is None and not calls


def test_parse_value_limits_and_roles():
    assert pwm.parse_value("9" * 9 + "." + "9" * 9, "v_supply") == Fraction("999999999.999999999")
    assert pwm.parse_value("9" * 10, "t_on") is None
    assert pwm.parse_value("1." + "0" * 10, "t_period") is None
    assert pwm.parse_value("-0", "t_on") == 0
    with pytest.raises(KeyError):
        pwm.parse_value("1", "v_avg")


def test_strict_capture_refuses_duplicates_unknown_fields_and_bad_answers():
    good = {k: [v] for k, v in _form().items()}
    assert pwm.capture_form(good) is not None
    for bad in (dict(good, **{pwm.VALUE_FIELD % "t_on": ["0.25", "0.5"]}),
                dict(good, **{pwm.DECLARATION_FIELD % "ideal_two_level_waveform":
                              ["applies", "does_not_apply"]}),
                dict(good, unexpected=["1"]),
                dict(good, **{pwm.SCREEN_FIELD % "safety_function": ["maybe"]}),
                dict(good, **{pwm.DECLARATION_FIELD % "waveform_average_wanted": ["yes"]}),
                dict(good, **{pwm.VALUE_FIELD % "v_avg": ["3"]}),
                dict(good, **{pwm.VALUE_FIELD % "duty": ["25"]}),
                dict(good, **{"decl_constant_dc_current": ["applies"]}), [], None):
        assert pwm.capture_form(bad) is None
    missing = {k: v for k, v in good.items()
               if k != pwm.DECLARATION_FIELD % "fixed_period_and_on_time"}
    captured = pwm.capture_form(missing)
    assert captured is not None
    assert pwm.evaluate(captured, BINDING)["outcome"] == pwm.NOT_DECLARED


# ==========================================================================
# 5. the owner: inventory, units, bindings and integrity (Correction 11)
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["outputs"] == {"v_avg": {"value": 3.0, "unit": "V",
                                           "provenance": "CALCULATED"}}
    assert [u["record_id"] for u in result["unit_records"]] == ["dcu:U011", "dcu:U015"]
    assert [q["source_ref"] for q in result["source_qualification"]] == [
        "NASA-PWM-S1", "NASA-PWM-S2"]
    assert {q["source_use_policy_ref"] for q in result["source_qualification"]} == {"dcu:SU019"}
    assert result["validation_status"] == "UNVALIDATED"
    assert (result["artifact_version"], result["implementation_version"]) == ("12", "1.11.0")
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_adds_exactly_one_method_and_no_kind_token_or_conversion():
    assert ("electrical:pwm_average_voltage", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 12
    # no new kind, token or exception from THIS admission: Correction 12 later added
    # exactly mass / kg, stiffness / N/m and frequency / Hz for its own method
    assert len(dc.ADMITTED_QUANTITY_KINDS) == 18 and len(dc.ADMITTED_UNIT_TOKENS) == 20
    assert dc.ADMITTED_UNIT_TOKENS == {"N", "mm", "W", "K/W", "K", "N·mm", "N·m", "rad/s",
                                       "mV", "°C", "V", "Ω", "A", "J", "s", "h", "A·h",
                                       "kg", "N/m", "Hz"}
    assert dc.KIND_TOKEN_EXCEPTIONS == {"voltage": frozenset({"mV", "V"}),
                                        "time": frozenset({"s", "h"})}
    assert dc._CONDITIONS == ("greater_than_zero", "less_than_zero",
                              "within_zero_and_role")
    assert not any(k in dc.ADMITTED_QUANTITY_KINDS
                   for k in ("duty_cycle", "ratio", "dimensionless", "switching_frequency"))
    assert not any(t in dc.ADMITTED_UNIT_TOKENS for t in ("%", "1", "kHz", "ms"))
    data = dc.load_artifact()
    assert len(data["unit_records"]) == 20 and len(data["quantity_kinds"]) == 18
    record = _record(data)
    assert record["applicability"] == [
        {"role": "t_period", "condition": "greater_than_zero", "bound_role": None},
        {"role": "t_on", "condition": "within_zero_and_role", "bound_role": "t_period"}]
    assert record["result_range"] == []
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"] + record["output_roles"]] == [
        ("v_supply", "voltage", "V"), ("t_on", "time", "s"), ("t_period", "time", "s"),
        ("v_avg", "voltage", "V")]
    assert record["adapter_identity"] == "engine.pwm_average_voltage_method.evaluate"
    assert [q["source_ref"] for q in record["source_qualification"]] == [
        "NASA-PWM-S1", "NASA-PWM-S2"]
    assert "inductive-load applicability context only" \
        in record["source_qualification"][1]["source_title"]


@pytest.mark.parametrize("units,reason", [
    (("mV", "s", "s"), dc.UNIT_NOT_ADMITTED), (("V", "h", "s"), dc.UNIT_NOT_ADMITTED),
    (("V", "s", "h"), dc.UNIT_NOT_ADMITTED), (("A", "s", "s"), dc.UNIT_NOT_ADMITTED),
    (("V", "J", "s"), dc.UNIT_NOT_ADMITTED), (("W", "s", "s"), dc.UNIT_NOT_ADMITTED),
    (("v", "s", "s"), dc.UNKNOWN_UNIT), (("kV", "s", "s"), dc.UNKNOWN_UNIT),
    (("V", "ms", "s"), dc.UNKNOWN_UNIT), (("V", "s", "ms"), dc.UNKNOWN_UNIT),
    (("V", "µs", "s"), dc.UNKNOWN_UNIT), (("V", "s", "Hz"), dc.UNIT_NOT_ADMITTED),
    (("V", "s", "kHz"), dc.UNKNOWN_UNIT), (("V", "%", "s"), dc.UNKNOWN_UNIT),
    (("V", "1", "s"), dc.UNKNOWN_UNIT), (("V", "S", "s"), dc.UNKNOWN_UNIT),
    (("V", "sec", "s"), dc.UNKNOWN_UNIT), (("V", "min", "s"), dc.UNKNOWN_UNIT),
])
def test_units_are_exact_with_no_alias_or_conversion(units, reason):
    result = dc.execute(BINDING, _request(units=units))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, reason, None)


def test_each_binding_executes_only_its_own_method():
    for binding in OTHER_BINDINGS:
        assert dc.execute(binding, _request())["reason"] == dc.OPERATION_NOT_ADMITTED
    swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, energy_method.evaluate)
    assert _failure(dc.execute(swapped, _request()))
    assert dc.execute(dc.bind_method(method.METHOD_ID, "2.0", method.evaluate),
                      _request())["reason"] == dc.VERSION_MISMATCH


def test_app_wires_one_immutable_binding_per_method():
    assert webapp._PWM_AVERAGE_VOLTAGE_BINDING.adapter_identity \
        == "engine.pwm_average_voltage_method.evaluate"
    with pytest.raises(AttributeError):
        webapp._PWM_AVERAGE_VOLTAGE_BINDING.method_id = "x"
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 12
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("import pwm_average_voltage", "engine.pwm", "engine/pwm",
                   "pwm_average_voltage_method.", "pwm_average_voltage import",
                   "electrical_content_config", "import fractions", "decimal", "sqlite",
                   "duty", "percent"):
        assert banned not in owner_source.lower(), banned


def _owner_tamper(data, name):
    record = _record(data)
    if name == "twelfth_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "electrical:pwm_rms_voltage"
        data["methods"].append(extra)
    elif name == "output_kind":
        record["output_roles"][0]["quantity_kind"] = "power"
    elif name == "output_unit":
        record["output_roles"][0]["unit_token"] = "mV"
    elif name == "on_time_in_hours":
        record["input_roles"][1]["unit_token"] = "h"      # admitted token, wrong for this role
    elif name == "policy_unresolved":
        record["source_qualification"][0]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "duty_cycle_kind":
        data["quantity_kinds"].append({"quantity_kind": "duty_cycle", "dimension": "1"})
    elif name == "percent_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "s"][0])
        extra["record_id"], extra["unit_token"], extra["quantity_kind"] = "dcu:U099", "%", "time"
        data["unit_records"].append(extra)
    elif name == "millisecond_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "s"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "ms"
        data["unit_records"].append(extra)
    elif name == "bound_dropped":
        record["applicability"] = record["applicability"][:1]
        record["applicability"].append(
            {"role": "t_on", "condition": "within_zero_and_role", "bound_role": None})
    elif name == "unknown_condition":
        record["applicability"].append(
            {"role": "v_supply", "condition": "non_negative", "bound_role": None})
    elif name == "basis":
        data["source_use_policies"][-1]["inspection_basis"] = "EXECUTOR"
    return data


@pytest.mark.parametrize("name", ["twelfth_method", "output_kind", "policy_unresolved",
                                  "duty_cycle_kind", "percent_unit", "millisecond_unit",
                                  "bound_dropped", "unknown_condition", "basis"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), name))
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    assert _failure(dc.execute(BINDING, _request(), artifact_path=path))


def test_owner_on_time_rebound_to_hours_refuses_the_request(tmp_path):
    # h is an admitted time token, so the owner artifact still loads; the
    # consumer's fixed V / s / s request is then refused by the owner
    # (UNIT_NOT_ADMITTED for that role) and the page shows no number.
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), "on_time_in_hours"))
    assert _record(dc.load_artifact(path))["input_roles"][1]["unit_token"] == "h"
    result = dc.execute(BINDING, _request(), artifact_path=path)
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, None)
    evaluation = pwm.evaluate(_captured(), BINDING, owner_artifact_path=path)
    assert evaluation["outcome"] == pwm.UNIT_NOT_SUPPORTED
    assert evaluation["display_value"] is None


def test_owner_output_rebound_to_millivolts_is_refused_by_the_consumer(tmp_path):
    # mV is an admitted voltage token, so the owner loads and even succeeds,
    # echoing mV; the consumer accepts only its own V output token (§4) and
    # shows no number rather than a mislabelled one.
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), "output_unit"))
    result = dc.execute(BINDING, _request(), artifact_path=path)
    assert result["state"] == dc.STATE_SUCCESS
    assert result["outputs"][pwm.OUTPUT_ROLE]["unit"] == "mV"
    evaluation = pwm.evaluate(_captured(), BINDING, owner_artifact_path=path)
    assert evaluation["outcome"] == pwm.KNOWLEDGE_UNAVAILABLE
    assert evaluation["display_value"] is None


def test_owner_v10_records_are_unchanged_by_the_eleventh_admission():
    data = dc.load_artifact()
    assert data["artifact_version"] == "12"
    v10 = {"quantity_kinds": data["quantity_kinds"][:15],
           "unit_records": data["unit_records"][:17],
           "source_use_policies": data["source_use_policies"][:18],
           "methods": data["methods"][:10]}
    canonical = json.dumps(v10, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(canonical.encode()).hexdigest() == V10_RECORDS_DIGEST
    assert [p["record_id"] for p in data["source_use_policies"][18:19]] == ["dcu:SU019"]
    assert [m["method_id"] for m in data["methods"][10:11]] == [method.METHOD_ID]
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "pwm:SU001" in policies["dcu:SU019"]["inspected_content"]
    assert "NASA-PWM-S1 and NASA-PWM-S2 only" in policies["dcu:SU019"]["inspected_content"]
    assert "dcu:SU002, dcu:SU005 and dcu:SU016" in policies["dcu:SU019"]["inspection_reference"]
    text = json.dumps(data, ensure_ascii=False).lower()
    for banned in ("duty_cycle", "percent", "equivalent dc", "motor speed", "rms voltage",
                   "root mean square", "root-mean-square"):
        assert banned not in text, banned
    assert "Content version 12 admits exactly twelve methods" in data["governance_note"]
    assert "28-T3" not in data["governance_note"] or "BLOCKED" in data["governance_note"]


# ==========================================================================
# 6. the method artifact and the consumer
# ==========================================================================
def test_method_artifact_loads_with_provenance_and_scope_distinction():
    data = pwm.load_artifact()
    by_id = {r["record_id"]: r for r in data["sources"]}
    s1 = by_id["NASA-PWM-S1"]
    for phrase in ("proportional to the duty cycle", "printed pages 3, 4 and 6",
                   "NOT claimed that NASA prints InventorAI's method wording",
                   "SRC-042", "GOV_PUBLIC_USE_PERMITTED", "NOT used",
                   "no filtering, ripple, converter, load or circuit behaviour is derived"):
        assert phrase in s1["inspected_content"], phrase
    s2 = by_id["NASA-PWM-S2"]
    for phrase in ("CONTEXT only", "much shorter than the winding's electrical time constant",
                   "free-wheeling path", "NOT the numerical basis", "NOT generalised",
                   "SRC-018", "no time-constant comparison"):
        assert phrase in s2["inspected_content"], phrase
    assert s1["url"] == "https://ntrs.nasa.gov/citations/19700009882"
    assert s2["url"] == "https://ntrs.nasa.gov/citations/19700009492"
    assert by_id["pwm:SU001"]["url"] == "https://sti.nasa.gov/disclaimers/"
    assert "17 U.S.C. 105" in by_id["pwm:SU001"]["inspected_content"]
    for record in data["sources"]:
        assert record["inspection_basis"] == "LEAD_SUPPLIED"
        assert "endorse" in record["no_endorsement_limitation"]
    derivation = data["method"]["derivation"]
    assert "not claimed that NASA prints InventorAI's method wording" in derivation
    assert "inductive-load applicability context" in derivation
    assert data["method"]["method_id"] == method.METHOD_ID
    assert [d["declaration_id"] for d in data["declarations"]] == list(pwm.DECLARATION_IDS)
    assert [s["item_id"] for s in data["screen_items"]] == list(pwm.SCREEN_ITEMS)
    assert len(data["disclosure"]) == 7
    assert "28-T3) stays BLOCKED" in data["governance_note"]


def test_no_protected_material_or_pack_change():
    pack = json.loads((ROOT / "domains" / "electronics_electrical" / "domain.json")
                      .read_text(encoding="utf-8"))
    assert not any("pwm" in g["group_id"] for g in pack["reference_fundamentals"])
    prov = json.loads((ROOT / "domains" / "domain_provenance.json").read_text(encoding="utf-8"))
    records = prov["records"] if isinstance(prov, dict) else prov
    assert not any("pwm_average_voltage" in json.dumps(r) for r in records)
    text = json.dumps(pwm.load_artifact(), ensure_ascii=False)
    for banned in ("Figure", "worked example:", "verbatim", "Equation ("):
        assert banned not in text, banned


@pytest.mark.parametrize("mutate", [
    lambda d: d.__setitem__("artifact_version", "2"),
    lambda d: d["declarations"].pop(),
    lambda d: d["declarations"][0].__setitem__("accepted_value", "the waveform may go negative"),
    lambda d: d["disclosure"].__setitem__(2, "The load responds to this average."),
    lambda d: d["numeric_domain"]["roles"][1].__setitem__("unit_token", "ms"),
    lambda d: d["numeric_domain"]["roles"][3].__setitem__("quantity_kind", "power"),
    lambda d: d["sources"].pop(),
    lambda d: d["sources"][0].__setitem__("inspection_basis", "EXECUTOR"),
    lambda d: d["screen_items"].pop(),
    lambda d: d.__setitem__("extra", 1),
    lambda d: d["method"].__setitem__("method_version", "1.1"),
])
def test_method_artifact_tamper_is_knowledge_unavailable(mutate, monkeypatch):
    data = _method_artifact()
    mutate(data)
    with pytest.raises(pwm.PwmKnowledgeError):
        pwm.validate_artifact(data)
    calls = _owner_spy(monkeypatch)
    evaluation = pwm.evaluate(_captured(), BINDING, artifact=data)
    assert evaluation["outcome"] == pwm.KNOWLEDGE_UNAVAILABLE
    assert evaluation["display_value"] is None and not calls


def test_unreadable_artifacts_give_no_number(tmp_path, monkeypatch):
    monkeypatch.setattr(pwm, "ARTIFACT_PATH", tmp_path / "missing.json")
    assert _evaluate()["outcome"] == pwm.KNOWLEDGE_UNAVAILABLE
    broken = tmp_path / "broken.json"
    broken.write_text("{", encoding="utf-8")
    monkeypatch.setattr(pwm, "ARTIFACT_PATH", broken)
    assert _evaluate()["outcome"] == pwm.KNOWLEDGE_UNAVAILABLE
    monkeypatch.undo()
    evaluation = pwm.evaluate(_captured(), BINDING, owner_artifact_path=tmp_path / "no.json")
    assert evaluation["outcome"] == pwm.KNOWLEDGE_UNAVAILABLE
    assert (evaluation["owner_state"], evaluation["owner_reason"]) == (
        dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE)


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = _owner_spy(monkeypatch)
    assert _evaluate(v="-1", on="2", period="-1", decl={"ideal_two_level_waveform": ""},
                     screen={"safety_function": "yes"})["outcome"] == pwm.NOT_DECLARED
    assert _evaluate(v="-1", on="2", period="-1",
                     decl={"ideal_two_level_waveform": "does_not_apply"},
                     screen={"safety_function": "yes"})["outcome"] \
        == pwm.ENGINEERING_REVIEW_REQUIRED
    assert _evaluate(v="-1", on="2", period="-1",
                     decl={"ideal_two_level_waveform": "does_not_apply"})["outcome"] \
        == pwm.MODEL_NOT_SUPPORTED
    assert _evaluate(v="x", on="2", period="-1")["outcome"] == pwm.INVALID_NUMERIC_INPUT
    assert _evaluate(v="-1", on="2", period="-1")["outcome"] == pwm.VOLTAGE_NEGATIVE
    assert not calls


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, pwm.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, pwm.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, pwm.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, pwm.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, pwm.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, pwm.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, pwm.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, pwm.UNMAPPED_OWNER_OUTCOME),
    ("WEIRD", "x", pwm.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome, monkeypatch):
    monkeypatch.setattr(dc, "execute",
                        lambda *a, **k: {"state": state, "reason": reason, "outputs": None})
    evaluation = _evaluate()
    assert evaluation["outcome"] == outcome
    assert (evaluation["owner_state"], evaluation["owner_reason"]) == (state, reason)
    assert evaluation["display_value"] is None and evaluation["result"] is None


@pytest.mark.parametrize("produced", [3.0000001, -3.0, 0.0, -0.0, float("nan"),
                                      float("inf"), 3.0 * (1 + 2 ** -49), 12.5, "3.0", None])
def test_decimal_reference_failure_fails_closed_with_no_number(produced, monkeypatch):
    real = dc.execute

    def fake(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["v_avg"]["value"] = produced
        return result
    monkeypatch.setattr(dc, "execute", fake)
    evaluation = _evaluate()
    assert evaluation["outcome"] == pwm.KNOWLEDGE_UNAVAILABLE
    assert evaluation["display_value"] is None and evaluation["result"] is None


def test_zero_must_be_positive_zero_and_the_average_never_exceeds_the_supply(monkeypatch):
    assert pwm.agrees_with_reference(0.0, Fraction(0), 12.0)
    assert not pwm.agrees_with_reference(-0.0, Fraction(0), 12.0)
    assert not pwm.agrees_with_reference(0.0, Fraction(1, 10 ** 27), 12.0)
    assert not pwm.agrees_with_reference(1e-27, Fraction(0), 12.0)
    assert pwm.agrees_with_reference(3.0, Fraction(3), 12.0)
    assert pwm.agrees_with_reference(12.0, Fraction(12), 12.0)
    assert not pwm.agrees_with_reference(12.0000001, Fraction("12.0000001"), 12.0)
    assert not pwm.agrees_with_reference(3.0, Fraction(-3), 12.0)
    real = dc.execute

    def fake(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["v_avg"]["value"] = -0.0
        return result
    monkeypatch.setattr(dc, "execute", fake)
    assert _evaluate(v="0")["outcome"] == pwm.KNOWLEDGE_UNAVAILABLE


def test_consumer_sends_the_correctly_rounded_values_and_fixed_units(monkeypatch):
    calls = _owner_spy(monkeypatch)
    _evaluate(v="0.1", on="0.3", period="0.7")
    (request, _result), = calls
    assert request["inputs"] == {"v_supply": {"value": 0.1, "unit": "V"},
                                 "t_on": {"value": 0.3, "unit": "s"},
                                 "t_period": {"value": 0.7, "unit": "s"}}
    assert (request["method_id"], request["method_version"], request["subject_ref"]) \
        == (method.METHOD_ID, "1.0", None)


def test_requests_are_isolated_and_inputs_not_mutated():
    captured = _captured(v="12", on="0.25", period="1")
    before = copy.deepcopy(captured)
    first = pwm.evaluate(captured, BINDING)
    second = pwm.evaluate(captured, BINDING)
    assert captured == before
    assert first["display_value"] == second["display_value"] == "3"
    assert first["result"]["result_identity"] == second["result"]["result_identity"]
    first["result"]["outputs"]["v_avg"]["value"] = 99.0
    assert pwm.evaluate(captured, BINDING)["result"]["outputs"]["v_avg"]["value"] == 3.0


def test_consumer_and_adapter_import_no_other_authority():
    import ast
    for module in (pwm, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        for banned in ("cap13", "therm01", "tmp36", "dc_resistive_load", "dc_constant_current",
                       "record_store", "safety_signal", "requests", "urllib", "openai", "web",
                       "flask", "random", "time", "sqlite3", "domain_rules", "numpy", "scipy",
                       "subsystem_model", "idea_state"):
            assert not any(banned == n or n.startswith(banned + ".") or banned in n
                           for n in names if n), (module.__name__, banned)


# ==========================================================================
# 7. EN / AR fidelity, the scientific boundary wording and the contracts
# ==========================================================================
def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_english_wording_equals_the_artifact():
    content = pwm.load_artifact()
    assert ui_text.text("UI_PWM_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"]
        assert ui_text.text("UI_PWM_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."
    for entry in content["screen_items"]:
        value = entry["item"]
        assert ui_text.text("UI_PWM_SCREEN_" + entry["item_id"].upper(), "en") \
            == value[0].upper() + value[1:]


def test_arabic_wording_equals_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    assert ui_text.text("UI_PWM_DISCLOSURE", "ar").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$",
                           _contract_section("**A-2", "**A-3"), re.M))
    for decl, ref in pwm.DECLARATIONS:
        assert ui_text.text("UI_PWM_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    screen = dict(re.findall(r"^\| (\w+) \| (.+?) \|$",
                             _contract_section("**A-3", "**A-4"), re.M))
    for item in pwm.SCREEN_ITEMS:
        assert ui_text.text("UI_PWM_SCREEN_" + item.upper(), "ar") == screen[item], item
    s9 = _contract_section("## 9. Result", "## 9A.")
    assert [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)] \
        == pwm.load_artifact()["disclosure"]
    s5 = _contract_section("## 5. Applicability", "## 6.")
    english = dict(re.findall(r"^\| (D-\d) \| `\w+` \| (.+?) \|$", s5, re.M))
    for entry in pwm.load_artifact()["declarations"]:
        assert english[entry["contract_ref"]] == entry["accepted_value"]


def test_every_key_has_both_languages_and_the_scientific_boundary_wording():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_PWM_[A-Z0-9_]+)": \{', source)
    assert len(keys) >= 48
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in FORBIDDEN + ("the load is safe", "measured by inventorai", "guaranteed",
                             "certified", "has been validated", "inventorai recommends", "we recommend",
                             "is equivalent to", "equals the dc voltage", "dimming"):
        assert claim not in english, claim
    for phrase in ("average of this pwm voltage waveform",
                   "for the ideal repeating voltage waveform you declared, inventorai "
                   "calculated its time-average over one cycle",
                   "not an equivalent steady dc voltage", "no physical load response is inferred",
                   "does not establish the average power as v_avg² / r",
                   "do not enter v_avg into the dc resistive load",
                   "no result is carried from one calculation into another",
                   "no current, ripple, average power, rms voltage, torque, speed, heating "
                   "or temperature is calculated", "context for inductive loads only",
                   "next engineering need", "remain unverified", "not physical limits",
                   "labelled rounded", "never negative", "unvalidated"):
        assert phrase in english, phrase
    arabic = " ".join(ui_text.text(k, "ar") for k in keys)
    for phrase in ("متوسط موجة جهد PWM هذه", "ليس جهدًا مستمرًا مكافئًا", "لا تُستنتج أي استجابة لحِمل",
                   "V_avg² / R", "سياق للأحمال الحثّية فقط", "UNVALIDATED"):
        assert phrase in arabic, phrase


def test_no_result_transfer_into_the_dc_load_calculations():
    # the page never links or posts to the DC load calculations and the DC load
    # pages never read this method; the only mention is the explicit warning
    template = (ROOT / "web" / "templates" / "pwm_average_voltage.html").read_text(encoding="utf-8")
    for other in ("dc-load-current", "dc-load-power", "dc-load-energy",
                  "dc-constant-current-charge", "dc_load_", "dc_constant"):
        assert other not in template, other
    for other in ("dc_load_energy.html", "dc_load_power.html", "dc_load_current.html",
                  "dc_constant_current_charge.html"):
        assert "pwm" not in (ROOT / "web" / "templates" / other).read_text(encoding="utf-8").lower()
    src = Path(webapp.__file__).read_text(encoding="utf-8")
    start = src.index("# PWM-AVERAGE-VOLTAGE-01 — PWM Average Voltage")
    section = src[start:src.index("# MECHANICAL-NATURAL-FREQUENCY-01 —", start)]
    for banned in ("_dcl", "_dcp", "_dce", "_dcq", "v_load", "r_load", "e_load", "p_load"):
        assert banned not in section, banned
    assert "data-pwm-no-transfer" in template and "data-pwm-not-dc-equivalent" in template


def test_correction_11_is_recorded_and_earlier_sections_unchanged():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 11" in body and "## 13J." in body
    section = _norm(body[body.index("## 13J."):body.index("## 14.")])
    for phrase in ("exactly eleven", "`electrical:pwm_average_voltage`",
                   "Quantity kinds and exact unit tokens: none added", "`dcu:U011`", "`dcu:U015`",
                   "`dcu:SU019`", "content version `11`", "`1.10.0`",
                   "Nonnegative-voltage convention", "No signed or bipolar waveform",
                   "no reuse of the DC load methods' passive sign convention",
                   "`within_zero_and_role` on `t_on` bound to `t_period` (inclusive at both ends",
                   "NOT a generic owner policy", "No consumer imports another",
                   "within a relative `2^-50`", "never a negative zero",
                   "exactly `v_supply` for an on-time equal to the period",
                   "no result is transferred", "no 28-T3 owner is created", "duty-cycle",
                   "`%` are unknown tokens"):
        assert phrase in section, phrase
    assert "General Power Electronics / Motion (28-T3) stays BLOCKED" in body
    assert "**Methods — exactly ten:**" in body[body.index("## 13I."):body.index("## 13J.")]
    assert "- Correction 11 (§13J) is Owner-authorized" in body
    assert body.count("## 13J.") == 1


def test_method_contract_records_scope_provenance_and_exclusions():
    text = _norm(CONTRACT.read_text(encoding="utf-8"))
    for phrase in ("NASA TN D-5643", "NTRS 19700009882", "printed pages 3, 4 and 6",
                   "NTRS 19700009492", "printed pages 14 to 17", "SRC-042", "SRC-018",
                   "numerical relation basis", "inductive-load applicability context only",
                   "NOT the numerical basis", "NOT generalised",
                   "not claimed that NASA prints InventorAI's exact method wording",
                   "Nonnegative-voltage convention", "No signed or bipolar PWM waveform",
                   "no reuse of another DC method's sign convention",
                   "Critical scientific boundary", "NOT established by this method",
                   "`VOLTAGE_NEGATIVE`", "`PERIOD_NOT_POSITIVE`", "`ON_TIME_NEGATIVE`",
                   "`ON_TIME_EXCEEDS_PERIOD`", "4.0000001", "Negative zero", "Non-finite",
                   "`12 V`, `0.25 s`, `1 s` shows `3`, exact", "`1 × 10^-27`, rounded",
                   "Electronics / Motion (28-T3) stays BLOCKED",
                   "creates no 28-T3 owner", "No general Power Electronics / Motion (28-T3) activation",
                   "no result handoff to the DC resistive load current, power or energy calculations",
                   "the SAME `_calc_gate` / `_calc_declared_part` rule",
                   "The Stage 15 exception in `engine/subsystem_model.py` names this method",
                   "an earlier rendered page grants nothing",
                   "Stage 15 part eligibility only as stated in §1",
                   "17 U.S.C. 105", "no external modelling library or code is used"):
        assert phrase in text, phrase
    model = (ROOT / "engine" / "subsystem_model.py").read_text(encoding="utf-8")
    assert "PWM-AVERAGE-VOLTAGE-01" in model
    assert "``electrical:pwm_average_voltage``" in model


# ==========================================================================
# 8. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_electronics_root_journey_and_reference_values(elec):
    c, _aid, sid = elec
    assert "data-pwm-link" in _page(c, sid)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-pwm-form" in body and "checked" not in body
    assert "data-pwm-value-note" in body and body.count('type="radio"') == 20
    for v, on, period, expected in REFERENCE:
        body = c.post(URL % sid, data=_form(v=v, on=on, period=period)).get_data(as_text=True)
        assert _value(body) == "%s V" % expected, (v, on, period)
        assert 'data-pwm-exactness="exact"' in body
    body = c.post(URL % sid, data=_form(v="0", on="0.25", period="1")).get_data(as_text=True)
    assert _value(body) == "0 V" and 'data-pwm-exactness="exact"' in body
    body = c.post(URL % sid, data=_form(v="12", on="0", period="1")).get_data(as_text=True)
    assert _value(body) == "0 V"
    body = c.post(URL % sid, data=_form(v="12", on="1", period="1")).get_data(as_text=True)
    assert _value(body) == "12 V"
    body = c.post(URL % sid, data=_form(v="5", on="1", period="3")).get_data(as_text=True)
    assert _value(body) == "1.66666666667 V"
    assert 'data-pwm-exactness="rounded"' in body
    assert "data-pwm-not-dc-equivalent" in body and "data-pwm-no-transfer" in body
    assert "UNVALIDATED" in body and "NOT EVIDENCE" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_PWM_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert "NASA TN D-5643" in body and "NIST" in body
    assert "electrical:pwm_average_voltage" in body
    assert '<bdi dir="ltr" data-pwm-echo-value>5</bdi>' in body
    lowered = html.unescape(body).lower()
    for phrase in FORBIDDEN:
        assert phrase not in lowered, phrase


@pytest.mark.parametrize("over,outcome", [
    ({"v": "-12"}, "VOLTAGE_NEGATIVE"),
    ({"period": "0"}, "PERIOD_NOT_POSITIVE"),
    ({"period": "-1"}, "PERIOD_NOT_POSITIVE"),
    ({"on": "-0.25"}, "ON_TIME_NEGATIVE"),
    ({"on": "1.5"}, "ON_TIME_EXCEEDS_PERIOD"),
    ({"on": "25%"}, "INVALID_NUMERIC_INPUT"),
    ({"period": "1kHz"}, "INVALID_NUMERIC_INPUT"),
    ({"v": ""}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"mains_or_high_voltage": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"ideal_two_level_waveform": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"waveform_average_wanted": ""}}, "NOT_DECLARED"),
])
def test_non_success_shows_one_reason_and_no_number(elec, over, outcome):
    c, _aid, sid = elec
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert ui_text.text("UI_PWM_OUTCOME_" + outcome, "en") in html.unescape(body)
    assert _value(body) is None
    assert body.count("data-pwm-outcome") == 1 and "data-pwm-result" not in body


def test_mechanical_root_is_not_eligible(mech, monkeypatch):
    c, _aid, sid = mech
    assert "data-pwm-link" not in _page(c, sid)
    assert webapp._calc_gate(sid, pwm) == (False, None)
    called = []
    monkeypatch.setattr(webapp._pwm, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-pwm-scope-note" in body
        assert "data-pwm-form" not in body and _value(body) is None
    assert not called


@pytest.mark.parametrize("focus,extra", [(MECH, {}), (ELEC, {}), (MECH, CTRL), (ELEC, CTRL)],
                         ids=["mech-focus", "elec-focus", "mech-focus-3", "elec-focus-3"])
def test_the_declared_electronics_part_is_offered_with_attribution(focus, extra, monkeypatch):
    c, _ = _client_for("pwm-part-%s-%d@example.com" % (focus, len(extra)))
    sid = _integrated(c, focus, **extra)
    eligible, part = webapp._calc_gate(sid, pwm)
    assert eligible and part.domain == ELEC
    assert webapp._pwm_eligible(sid)
    assert "data-pwm-link" in _page(c, sid)
    get = c.get(URL % sid).get_data(as_text=True)
    assert "data-pwm-form" in get and "checked" not in get
    assert _part_line(get, "pwm") == PARTS["elec_part_name"]
    calls = _owner_spy(monkeypatch)
    post = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(post) == "3 V"
    assert _part_line(post, "pwm") == PARTS["elec_part_name"]
    assert len(calls) == 1 and calls[0][0]["method_id"] == method.METHOD_ID


def test_a_stale_page_grants_nothing_after_the_composition_changes(monkeypatch):
    c, _ = _client_for("pwm-stale@example.com")
    sid = _integrated(c, MECH)
    assert "data-pwm-form" in c.get(URL % sid).get_data(as_text=True)
    _corrupt("DELETE FROM project_subsystems WHERE subsystem_seq = 1")
    calls = _owner_spy(monkeypatch)
    assert webapp._calc_gate(sid, pwm) == (False, None)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-pwm-form" not in body and _value(body) is None
    assert "data-pwm-part" not in body and not calls


def test_the_part_name_is_escaped_and_bilingual():
    c, _ = _client_for("pwm-escape@example.com")
    sid = _integrated(c, MECH, elec_part_name=HOSTILE)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "<script>" not in body
    assert html.unescape(_part_line(body, "pwm")) == HOSTILE
    for lang in ("en", "ar"):
        if lang == "ar":
            assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
        page = c.get(URL % sid).get_data(as_text=True)
        text = html.unescape(re.sub(r"<[^>]+>", "", page))
        for key in ("UI_THERM01_PART_LABEL", "UI_THERM01_PART_NOTE", "UI_PWM_SCOPE_NOTE"):
            assert re.sub(r"\s+", " ", ui_text.text(key, lang)) in re.sub(r"\s+", " ", text), \
                (key, lang)


def test_request_supplied_domain_part_or_switching_words_never_grant_eligibility(mech, monkeypatch):
    c, _aid, sid = mech
    calls = _owner_spy(monkeypatch)
    for extra in ({"root_domain": ELEC}, {"domain": ELEC}, {"part_id": "x"},
                  {"declared_part": PARTS["elec_part_name"]}, {"load": "motor"},
                  {"component": "transistor PWM dimmer"}):
        r = c.post(URL % sid, data=dict(_form(), **extra))
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-pwm-form" not in body and _value(body) is None
        r = c.get((URL % sid) + "?domain=%s&load=motor" % ELEC)
        assert "data-pwm-form" not in r.get_data(as_text=True)
    assert not calls


def test_unreadable_root_domain_grants_nothing(elec, monkeypatch):
    c, _aid, sid = elec

    def broken(_sid):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(webapp, "_cap12_root_domain", broken)
    assert not webapp._pwm_eligible(sid)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-pwm-form" not in body and _value(body) is None


def test_csrf_authorization_and_malformed_requests(elec):
    c, _aid, sid = elec
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("pwm-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302 and "data-pwm" not in r.get_data(as_text=True)
    for bad in (dict(_form(), unexpected="1"),
                dict(_form(), screen_safety_function="maybe"),
                dict(_form(), value_v_avg="6"), dict(_form(), value_duty="25")):
        r = c.post(URL % sid, data=bad)
        assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    from werkzeug.datastructures import MultiDict
    r = c.post(URL % sid, data=MultiDict(list(_form().items())
                                         + [(pwm.VALUE_FIELD % "t_on", "0.5")]))
    assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    body = c.post(URL % sid, data=_form(on="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body
    assert c.get(URL % sid).headers["Cache-Control"] == "no-store"


@pytest.mark.parametrize("over", [{}, {"on": "-5"}, {"screen": {"safety_function": "yes"}}])
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
    start = src.index("# PWM-AVERAGE-VOLTAGE-01 — PWM Average Voltage")
    section = src[start:src.index("# MECHANICAL-NATURAL-FREQUENCY-01 —", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "_cap13", "_tmp36", "load_project_subsystems", "request.args",
                   "cap09", "success_criteria", "redirect(", "openai", "provider", "motor",
                   "duty"):
        assert banned not in section, banned
    assert section.count("_dcalc.bind_method(") == 1
    assert [r.rule for r in webapp.app.url_map.iter_rules()
            if "pwm-average-voltage" in r.rule] == ["/session/<sid>/pwm-average-voltage"] * 2
    for template in ("deliverable.html", "report.html", "success_criteria.html",
                     "parts_components_interactions.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "pwm-average-voltage" not in path.read_text(encoding="utf-8").lower()
    for module in ("engine/disclosure_export.py", "engine/deliverable_assembler.py",
                   "engine/safety_signal.py", "engine/readiness_snapshot.py"):
        assert "pwm_average_voltage" not in (ROOT / module).read_text(encoding="utf-8")


def test_existing_ten_calculations_are_unchanged(mech, elec):
    c, _aid, sid = mech
    body = c.post("/session/%s/support-reactions" % sid, data=_cap13_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">750.0 N</bdi>' in body and '<bdi dir="ltr">250.0 N</bdi>' in body
    body = c.post("/session/%s/planar-moment" % sid, data=_moment_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">1000.0 N·mm</bdi>' in body
    body = c.post("/session/%s/rotational-load" % sid,
                  data=_rotational_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">-1.0 N·m</bdi>' in body
    body = c.post("/session/%s/planar-required-force" % sid,
                  data=_force_form()).get_data(as_text=True)
    assert "N</bdi>" in body
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
    body = c2.post("/session/%s/dc-load-energy" % sid2,
                   data=_energy_form(v="12", r="24", t="3600")).get_data(as_text=True)
    assert 'data-dce-result-value><bdi dir="ltr">21600 J</bdi>' in body
    body = c2.post("/session/%s/dc-constant-current-charge" % sid2,
                   data=_charge_form(i="0.5", t="4")).get_data(as_text=True)
    assert 'data-dcq-result-value><bdi dir="ltr">2 A·h</bdi>' in body


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_arabic_isolation_and_boundary_wording(elec, lang):
    c, _aid, sid = elec
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form(v="12", on="0.25", period="1")).get_data(as_text=True)
    assert _value(body) == "3 V"
    assert '<bdi dir="ltr" data-pwm-echo-value>0.25</bdi>' in body
    if lang == "ar":
        assert 'dir="rtl"' in body
        isolated = [html.unescape(run)
                    for run in re.findall(r'<bdi dir="ltr">([^<]*)</bdi>', body)]
        for token in ("UNVALIDATED", "NOT EVIDENCE", "NASA TN D-5643", "(V)", "(s)",
                      "(t_on)", "(T)", "(V_supply)", "(V_avg)"):
            assert any(token in run for run in isolated), token
        assert any(run == "V_avg = V_supply × t_on / T" for run in isolated)
        assert any("V_avg² / R" in run for run in isolated)
        stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
        for item in ui_text.text("UI_PWM_DISCLOSURE", "ar").split("\n\n"):
            assert _norm(item) in _norm(stripped), item[:30]
        refusal = c.post(URL % sid, data=_form(v="-1")).get_data(as_text=True)
        assert _norm(ui_text.text("UI_PWM_OUTCOME_VOLTAGE_NEGATIVE", "ar")) \
            in _norm(html.unescape(re.sub(r"<[^>]+>", "", refusal)))
        assert _value(refusal) is None
