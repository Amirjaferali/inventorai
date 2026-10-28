# -*- coding: utf-8 -*-
"""Electrical / Electronics - DC Constant-Current Charge, Slice 1 (directly owning tests).

DC-CONSTANT-CURRENT-CHARGE-01. The shared deterministic calculation / units owner
after the bounded tenth admission of calc/units Correction 10 (§13I); the ONE
method ``electrical:dc_constant_current_charge`` 1.0
(``engine/dc_constant_current_charge_method.py``) and its ONE consumer
(``engine/dc_constant_current_charge.py`` + the request-local page).

Scientific reference: electric current is the flow of electric charge, one
ampere being one coulomb per second (DOE-HDBK-1011/1-92, recorded as
electronics_electrical:PR018), so for a current that stays constant throughout
the duration t the charge that flows is Q = I x t (InventorAI's own
restatement); the ampere hour is a unit of electric charge (NIST SP 811,
recorded as electronics_electrical:PR020). The numerical tests use an
INDEPENDENT decimal reference: every expected charge and every expected display
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
from engine import dc_constant_current_charge as dcq
from engine import dc_constant_current_charge_method as method
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

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "ELECTRICAL_DC_CONSTANT_CURRENT_CHARGE_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
URL = "/session/%s/dc-constant-current-charge"
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
    dc.bind_method(force_method.METHOD_ID, "1.0", force_method.evaluate))
# The reference vectors (A, h -> A·h).
REFERENCE = (("0.5", "4", "2"), ("2", "1.5", "3"), ("0.25", "0.5", "0.125"),
             ("1.2", "10", "12"))
DECIMAL_BOUND = Fraction(1, 2 ** 51)
PROVEN_WORST_CASE = Fraction(30000001, 10000000) * Fraction(1, 2 ** 53)
# The content-version-9 records (quantity kinds, unit records, source-use
# policies and the nine method records), pinned by digest: Correction 10 only
# appends after them.
V9_RECORDS_DIGEST = "a30890cecd1cfd2be48bc51ea690156b5d0a48a4110495eaaf8df447d3873743"
# Wording the Owner excluded from every surface of this method.
FORBIDDEN = ("battery capacity needed", "battery requirement", "required capacity",
             "runtime requirement", "battery size")


# --------------------------------------------------------------------------
# helpers: the independent decimal reference
# --------------------------------------------------------------------------
_EXACT = Context(prec=200, rounding=ROUND_HALF_EVEN)
_TWELVE = Context(prec=12, rounding=ROUND_HALF_EVEN)


def _reference(i, t):
    """The exact I x t as a Fraction, from Decimal alone."""
    return Fraction(Decimal(i)) * Fraction(Decimal(t))


def _reference_display(i, t):
    """The expected (text, exact) display, from Decimal alone: I x t correctly
    rounded to 12 significant digits (half to even), trailing zeros removed,
    plain for 1e-6 <= Q < 1e12 and 'm × 10^e' otherwise."""
    if Decimal(i) == 0 or Decimal(t) == 0:
        return "0", True
    product = _EXACT.multiply(Decimal(i), Decimal(t))          # exact: <= 36 digits
    rounded = _TWELVE.plus(product)
    exact = Fraction(rounded) == _reference(i, t)
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


def _request(i=0.5, t=4.0, units=("A", "h"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"i_load": {"value": i, "unit": units[0]},
                      "t_duration": {"value": t, "unit": units[1]}},
           "subject_ref": None}
    req.update(over)
    return req


def _q(result):
    return result["outputs"]["q_load"]["value"]


def _failure(result):
    return (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def _form(i="0.5", t="4", decl=None, screen=None):
    form = {dcq.DECLARATION_FIELD % d: dcq.ANSWER_APPLIES for d in dcq.DECLARATION_IDS}
    form.update({dcq.SCREEN_FIELD % s: dcq.SCREEN_NO for s in dcq.SCREEN_ITEMS})
    form[dcq.VALUE_FIELD % "i_load"] = i
    form[dcq.VALUE_FIELD % "t_duration"] = t
    for key, value in (decl or {}).items():
        form[dcq.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[dcq.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = dcq.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return dcq.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _method_artifact():
    return json.loads(dcq.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data):
    target = tmp_path / "a.json"
    target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return target


def _value(body):
    marker = 'data-dcq-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def _check_against_reference(i, t):
    """One typed pair through the whole consumer: success, the owner result
    within the decimal bound, the display equal to the independent reference."""
    evaluation = _evaluate(i=i, t=t)
    assert evaluation["outcome"] == dcq.OUTCOME_SUCCESS, (i, t)
    reference = _reference(i, t)
    produced = _q(evaluation["result"])
    assert math.copysign(1.0, produced) == 1.0, (i, t)         # never negative, no -0
    if reference == 0:
        assert produced == 0.0
    else:
        error = abs(Fraction(produced) - reference) / reference
        assert error <= PROVEN_WORST_CASE < DECIMAL_BOUND, (i, t)
        assert produced > 0
    assert (evaluation["display_value"], evaluation["display_exact"]) \
        == _reference_display(i, t), (i, t)
    assert evaluation["charge"] == reference
    return evaluation


@pytest.fixture
def elec():
    c, aid = _client_for("dcq-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def mech():
    c, aid = _client_for("dcq-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": MECH})


# ==========================================================================
# 1. the reference vectors and zero
# ==========================================================================
@pytest.mark.parametrize("i,t,expected", REFERENCE)
def test_reference_vectors_at_owner_adapter_and_consumer(i, t, expected):
    exact = _reference(i, t)
    produced = method.evaluate(float(i), float(t))["q_load"]
    assert abs(Fraction(produced) - exact) <= exact * Fraction(1, 2 ** 52)
    result = dc.execute(BINDING, _request(float(i), float(t)))
    assert result["state"] == dc.STATE_SUCCESS and _q(result) == produced
    evaluation = _check_against_reference(i, t)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (expected, True)


def test_charge_is_current_times_duration_and_nothing_is_converted():
    # Q = I x t exactly, in the declared A and h: no 3600 and no 1000 anywhere
    for i, t in (("0.5", "4"), ("2", "1.5"), ("0.001", "1000"), ("3", "0.25")):
        assert _evaluate(i=i, t=t)["charge"] == Fraction(Decimal(i)) * Fraction(Decimal(t))
    assert _evaluate(i="1", t="1")["display_value"] == "1"          # 1 A·h, not 3600 C
    assert _evaluate(i="0.001", t="1")["display_value"] == "0.001"  # not 1 mA·h
    # neither module holds a conversion constant: every numeric literal of the
    # executable code is inspected, and the only magnitudes are the grammar,
    # display and acceptance parameters
    import ast
    for module in (dcq, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        numbers = {node.value for node in ast.walk(tree)
                   if isinstance(node, ast.Constant) and isinstance(node.value, (int, float))
                   and not isinstance(node.value, bool)}
        assert not numbers & {3600, 3600.0, 3.6, 1000, 1000.0, 0.001, 60, 3.6e3}, numbers


@pytest.mark.parametrize("i,t", [("0", "4"), ("-0", "4"), ("0.000", "1"),
                                 ("-0.000000000", "999999999"), ("000000000", "5"),
                                 ("0.5", "0"), ("0.5", "-0"), ("2", "0.000000000"),
                                 ("999999999.999999999", "-0.000000000"), ("0", "0")])
def test_zero_current_or_duration_gives_exactly_positive_zero_charge(i, t):
    evaluation = _check_against_reference(i, t)
    assert evaluation["display_value"] == "0" and evaluation["display_exact"] is True
    produced = _q(evaluation["result"])
    assert produced == 0.0 and math.copysign(1.0, produced) == 1.0


def test_negative_zero_at_the_adapter_and_owner_is_positive_zero():
    for i, t in ((-0.0, 5.0), (0.0, 5.0), (5.0, -0.0), (-0.0, -0.0), (0.0, 0.0)):
        out = method.evaluate(i, t)["q_load"]
        assert out == 0.0 and math.copysign(1.0, out) == 1.0
        result = dc.execute(BINDING, _request(i, t))
        assert result["state"] == dc.STATE_SUCCESS
        assert math.copysign(1.0, _q(result)) == 1.0


# ==========================================================================
# 2. exact and rounded results; the display
# ==========================================================================
@pytest.mark.parametrize("i,t,display,exact", [
    ("2", "4", "8", True), ("1", "0.333333333", "0.333333333", True),
    ("0.1", "0.3", "0.03", True), ("1.234567891", "1.234567891", "1.52415787749", False),
    ("0.000000001", "0.000000001", "1 × 10^-18", True),
    ("999999999.999999999", "999999999.999999999", "1 × 10^18", False),
    ("123456789.123456789", "1", "123456789.123", False),
    ("1.5", "0.1", "0.15", True), ("0.7", "0.7", "0.49", True),
    ("999999999", "999999999", "9.99999998 × 10^17", False),
    ("0.000001", "1", "0.000001", True), ("0.0000001", "1", "1 × 10^-7", True),
    ("100000000", "1000", "100000000000", True), ("100000000", "10", "1000000000", True),
])
def test_exact_and_rounded_results(i, t, display, exact):
    evaluation = _check_against_reference(i, t)
    assert (evaluation["display_value"], evaluation["display_exact"]) == (display, exact)


def test_round_half_to_even_at_twelve_significant_digits():
    assert dcq.format_charge(Fraction("0.1234567890125")) == ("0.123456789012", False)
    assert dcq.format_charge(Fraction("0.1234567890135")) == ("0.123456789014", False)
    assert dcq.format_charge(Fraction("9.9999999999995")) == ("10", False)
    assert dcq.format_charge(Fraction("9.999999999994")) == ("9.99999999999", False)
    assert dcq.format_charge(Fraction(5, 2)) == ("2.5", True)
    assert dcq.format_charge(Fraction(0)) == ("0", True)
    with pytest.raises(TypeError):
        dcq.format_charge(2.5)


def test_tiny_and_large_charges_are_never_shown_as_zero_or_truncated():
    assert dcq.format_charge(Fraction(1, 10 ** 6)) == ("0.000001", True)
    assert dcq.format_charge(Fraction(1, 10 ** 7)) == ("1 × 10^-7", True)
    assert dcq.format_charge(Fraction(10 ** 11)) == ("100000000000", True)
    assert dcq.format_charge(Fraction(10 ** 12)) == ("1 × 10^12", True)
    for value in (Fraction(1, 10 ** 18), Fraction(7, 10 ** 15), Fraction(10 ** 18)):
        text, _exact = dcq.format_charge(value)
        assert text != "0" and "10^" in text


@pytest.mark.parametrize("i,t", [
    ("0.000000001", "0.000000001"),                      # smallest Q = 1e-18
    ("999999999.999999999", "999999999.999999999"),      # largest Q < 1e18
    ("0.000000001", "999999999.999999999"), ("999999999.999999999", "0.000000001"),
    ("1.000000001", "0.1"), ("0.1", "0.3"),
])
def test_representation_limits_are_calculated_and_representable(i, t):
    evaluation = _check_against_reference(i, t)
    produced = _q(evaluation["result"])
    assert math.isfinite(produced) and produced > 0.0
    assert Fraction(1, 10 ** 19) < Fraction(produced) < Fraction(10 ** 19)


def test_random_admitted_decimals_against_the_independent_reference():
    rng = random.Random(20261028)
    worst = Fraction(0)
    for _ in range(600):
        ii = rng.randint(0, 10 ** rng.randint(1, 9) - 1)
        fi = rng.randint(0, 10 ** 9 - 1)
        i = "%d.%09d" % (ii, fi) if rng.random() < 0.8 else str(ii)
        it = rng.randint(0, 10 ** rng.randint(1, 9) - 1)
        ft = rng.randint(0, 10 ** 9 - 1)
        t = "%d.%09d" % (it, ft) if rng.random() < 0.8 else str(it)
        evaluation = _check_against_reference(i, t)
        reference = _reference(i, t)
        if reference:
            worst = max(worst, abs(Fraction(_q(evaluation["result"])) - reference) / reference)
    assert worst <= PROVEN_WORST_CASE


def test_the_error_bound_proof():
    u = Fraction(1, 2 ** 53)
    # two correctly rounded inputs and one rounding of the product
    assert (1 + u) ** 3 - 1 < PROVEN_WORST_CASE < DECIMAL_BOUND
    assert 1 - (1 - u) ** 3 < PROVEN_WORST_CASE
    assert DECIMAL_BOUND == 4 * u and dcq.DECIMAL_REFERENCE_BOUND == DECIMAL_BOUND
    assert method.RELATIVE_ERROR_BOUND == 2 * u


def test_the_bound_holds_for_worst_case_binary_rounding_of_every_input():
    cases = ("0.1", "0.3", "0.7", "999999999.999999999", "0.000000001",
             "123456789.123456789", "1.000000001", "3.000000007")
    worst = Fraction(0)
    for i in cases:
        for t in cases:
            evaluation = _check_against_reference(i, t)
            reference = _reference(i, t)
            worst = max(worst, abs(Fraction(_q(evaluation["result"])) - reference) / reference)
    assert worst <= PROVEN_WORST_CASE


# ==========================================================================
# 3. negative current, negative duration; the adapter's acceptance
# ==========================================================================
@pytest.mark.parametrize("i", ["-1", "-0.000000001", "-0.5", "-999999999.999999999"])
def test_negative_current_is_refused_before_the_owner(i, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(i=i)
    assert evaluation["outcome"] == dcq.CURRENT_NEGATIVE
    assert evaluation["display_value"] is None and evaluation["result"] is None
    assert evaluation["charge"] is None and not calls


@pytest.mark.parametrize("t", ["-1", "-0.000000001", "-4", "-999999999.999999999"])
def test_negative_duration_is_refused_before_the_owner(t, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(t=t)
    assert evaluation["outcome"] == dcq.DURATION_NEGATIVE
    assert evaluation["display_value"] is None and evaluation["result"] is None
    assert evaluation["charge"] is None and not calls


def test_current_is_checked_before_the_duration():
    assert _evaluate(i="-1", t="-1")["outcome"] == dcq.CURRENT_NEGATIVE
    assert _evaluate(i="-0", t="-1")["outcome"] == dcq.DURATION_NEGATIVE


@pytest.mark.parametrize("t,display", [
    ("0", "0"), ("0.000000001", "5 × 10^-10"), ("999999999.999999999", "500000000"),
    ("999999999", "499999999.5"), ("1", "0.5")])
def test_duration_boundaries(t, display):
    assert _check_against_reference("0.5", t)["display_value"] == display


@pytest.mark.parametrize("i,display", [
    ("0", "0"), ("0.000000001", "4 × 10^-9"), ("999999999.999999999", "4000000000"),
    ("999999999", "3999999996"), ("1", "4")])
def test_current_boundaries(i, display):
    assert _check_against_reference(i, "4")["display_value"] == display


@pytest.mark.parametrize("i,t", [(-1.0, 4.0), (-5e-324, 4.0), (-1e308, 4.0),
                                 (0.5, -1.0), (0.5, -5e-324), (0.5, -1e308),
                                 (-1.0, -1.0)])
def test_negative_inputs_fail_closed_in_the_adapter_and_owner(i, t):
    with pytest.raises(ArithmeticError):
        method.evaluate(i, t)
    assert _failure(dc.execute(BINDING, _request(i, t)))


@pytest.mark.parametrize("i,t", [(1e200, 1e200), (1e300, 1e10), (1e-200, 1e-200),
                                 (5e-324, 0.5), (1e-170, 1e-170), (0.3, 5e-324)])
def test_overflow_and_underflow_fail_closed_in_the_adapter(i, t):
    with pytest.raises(ArithmeticError):
        method.evaluate(i, t)
    assert _failure(dc.execute(BINDING, _request(i, t)))


def test_an_exactly_representable_subnormal_result_is_not_rounded_away():
    assert method.evaluate(1.0, 5e-324)["q_load"] == 5e-324


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), "1", None, True])
@pytest.mark.parametrize("role", ["i", "t"])
def test_non_finite_and_non_numeric_inputs_are_refused(value, role):
    request = _request(i=value) if role == "i" else _request(t=value)
    result = dc.execute(BINDING, request)
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, None)


def test_adapter_refuses_non_float_or_out_of_domain_arguments():
    for args in ((1, 4.0), (0.5, 4), ("0.5", 4.0), (-1.0, 4.0), (0.5, -1.0),
                 (float("nan"), 1.0), (1.0, float("inf")), (float("inf"), 1.0),
                 (1.0, float("nan"))):
        with pytest.raises(ArithmeticError):
            method.evaluate(*args)
    with pytest.raises(TypeError):
        method.evaluate(0.5)


def test_adapter_results_are_correctly_rounded_and_nonnegative():
    rng = random.Random(10)
    for _ in range(500):
        i = rng.uniform(0, 1e9)
        t = rng.uniform(0, 1e9)
        exact = Fraction(i) * Fraction(t)
        produced = method.evaluate(i, t)["q_load"]
        assert produced == float(exact) and produced >= 0.0        # one correct rounding
        assert abs(Fraction(produced) - exact) <= exact * Fraction(1, 2 ** 53)


# ==========================================================================
# 4. the input grammar and strict capture
# ==========================================================================
@pytest.mark.parametrize("i,t", [
    ("+0.5", "4"), ("1e3", "4"), (" 0.5", "4"), ("1,5", "4"), ("٠٫٥", "4"), ("0.5.", "4"),
    (".5", "4"), ("--1", "4"), ("inf", "4"), ("nan", "4"), ("1.0000000001", "4"),
    ("1234567890", "4"), ("0.5A", "4"), ("500mA", "4"), ("", "4"), ("−0.5", "4"),
    ("1" * 65, "4"),
    ("0.5", ""), ("0.5", "+4"), ("0.5", "1e3"), ("0.5", "1000000000"),
    ("0.5", "0.0000000001"), ("0.5", "4h"), ("0.5", "240min"), ("0.5", "4:00"),
    ("0.5", "−4"), ("0.5", "1.5.0"), ("0.5", "inf"), ("0.5", "nan"), ("0.5", " 4"),
    ("0.5", "٤"), ("0.5", "--4"), ("0.5", "4."),
])
def test_malformed_values_are_invalid_and_never_reach_the_owner(i, t, monkeypatch):
    calls = _owner_spy(monkeypatch)
    evaluation = _evaluate(i=i, t=t)
    assert evaluation["outcome"] == dcq.INVALID_NUMERIC_INPUT, (i, t)
    assert evaluation["display_value"] is None and not calls


def test_parse_value_limits_and_roles():
    assert dcq.parse_value("9" * 9 + "." + "9" * 9, "i_load") == Fraction("999999999.999999999")
    assert dcq.parse_value("9" * 10, "i_load") is None
    assert dcq.parse_value("1." + "0" * 10, "t_duration") is None
    assert dcq.parse_value("-0", "t_duration") == 0
    with pytest.raises(KeyError):
        dcq.parse_value("1", "q_load")


def test_strict_capture_refuses_duplicates_unknown_fields_and_bad_answers():
    good = {k: [v] for k, v in _form().items()}
    assert dcq.capture_form(good) is not None
    for bad in (dict(good, **{dcq.VALUE_FIELD % "t_duration": ["1", "2"]}),
                dict(good, **{dcq.DECLARATION_FIELD % "constant_dc_current":
                              ["applies", "does_not_apply"]}),
                dict(good, unexpected=["1"]),
                dict(good, **{dcq.SCREEN_FIELD % "safety_function": ["maybe"]}),
                dict(good, **{dcq.DECLARATION_FIELD % "charge_through_load": ["yes"]}),
                dict(good, **{dcq.VALUE_FIELD % "q_load": ["2"]}),
                dict(good, **{dcq.VALUE_FIELD % "v_load": ["12"]}),
                dict(good, **{"decl_resistive_load": ["applies"]}), [], None):
        assert dcq.capture_form(bad) is None
    missing = {k: v for k, v in good.items()
               if k != dcq.DECLARATION_FIELD % "single_load_single_period"}
    captured = dcq.capture_form(missing)
    assert captured is not None
    assert dcq.evaluate(captured, BINDING)["outcome"] == dcq.NOT_DECLARED


# ==========================================================================
# 5. the owner: inventory, units, bindings and integrity (Correction 10)
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["outputs"] == {"q_load": {"value": 2.0, "unit": "A·h",
                                            "provenance": "CALCULATED"}}
    assert [u["record_id"] for u in result["unit_records"]] == [
        "dcu:U013", "dcu:U016", "dcu:U017"]
    assert [q["source_ref"] for q in result["source_qualification"]] == ["DOE-CHG-S1"]
    assert result["source_qualification"][0]["source_use_policy_ref"] == "dcu:SU018"
    assert result["validation_status"] == "UNVALIDATED"
    assert (result["artifact_version"], result["implementation_version"]) == ("11", "1.10.0")
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_adds_exactly_the_charge_kind_and_two_tokens():
    assert ("electrical:dc_constant_current_charge", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 11
    assert dc.ADMITTED_QUANTITY_KINDS >= {"electric_charge", "time", "electric_current"}
    assert len(dc.ADMITTED_QUANTITY_KINDS) == 15 and len(dc.ADMITTED_UNIT_TOKENS) == 17
    assert dc.ADMITTED_UNIT_TOKENS == {"N", "mm", "W", "K/W", "K", "N·mm", "N·m", "rad/s",
                                       "mV", "°C", "V", "Ω", "A", "J", "s", "h", "A·h"}
    # the second named exception (§13I): time holds exactly s and h, nothing else;
    # no other kind gains a token and no alias exists
    assert dc.KIND_TOKEN_EXCEPTIONS == {"voltage": frozenset({"mV", "V"}),
                                        "time": frozenset({"s", "h"})}
    assert dc._CONDITIONS == ("greater_than_zero", "less_than_zero",
                              "within_zero_and_role")
    data = dc.load_artifact()
    record = _record(data)
    assert record["applicability"] == [] and record["result_range"] == []
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"] + record["output_roles"]] == [
        ("i_load", "electric_current", "A"), ("t_duration", "time", "h"),
        ("q_load", "electric_charge", "A·h")]
    assert record["adapter_identity"] == "engine.dc_constant_current_charge_method.evaluate"
    units = {u["unit_token"]: u for u in data["unit_records"]}
    assert (units["h"]["record_id"], units["h"]["quantity_kind"]) == ("dcu:U016", "time")
    assert (units["A·h"]["record_id"], units["A·h"]["quantity_kind"]) \
        == ("dcu:U017", "electric_charge")
    for token in ("h", "A·h"):
        assert units[token]["source_use_policy_ref"] == "dcu:SU017"
        assert "electronics_electrical:PR020" in units[token]["inspection_reference"]
        assert "no conversion is admitted" in units[token]["inspected_content"]
        assert "never applied" in units[token]["inspected_content"]
    assert "not recorded here as an inspected location" in units["h"]["inspected_content"]
    assert units["s"]["source_use_policy_ref"] == "dcu:SU014"           # energy's s unchanged
    kinds = {k["quantity_kind"]: k["dimension"] for k in data["quantity_kinds"]}
    assert kinds["electric_charge"] == "T I"
    # only this method uses the charge kind and the h token
    users = {m["method_id"] for m in data["methods"]
             for role in m["input_roles"] + m["output_roles"]
             if role["quantity_kind"] == "electric_charge" or role["unit_token"] == "h"}
    assert users == {method.METHOD_ID}
    energy = _record(data, "electrical:dc_resistive_load_energy")
    assert energy["input_roles"][2] == {"role": "t_duration", "quantity_kind": "time",
                                        "unit_token": "s"}


@pytest.mark.parametrize("units,reason", [
    (("A", "s"), dc.UNIT_NOT_ADMITTED), (("mV", "h"), dc.UNIT_NOT_ADMITTED),
    (("V", "h"), dc.UNIT_NOT_ADMITTED), (("A", "J"), dc.UNIT_NOT_ADMITTED),
    (("A", "K"), dc.UNIT_NOT_ADMITTED), (("A·h", "h"), dc.UNIT_NOT_ADMITTED),
    (("A", "A·h"), dc.UNIT_NOT_ADMITTED), (("W", "h"), dc.UNIT_NOT_ADMITTED),
    (("a", "h"), dc.UNKNOWN_UNIT), (("mA", "h"), dc.UNKNOWN_UNIT),
    (("A", "H"), dc.UNKNOWN_UNIT), (("A", "min"), dc.UNKNOWN_UNIT),
    (("A", "hr"), dc.UNKNOWN_UNIT), (("A", "hour"), dc.UNKNOWN_UNIT),
    (("A", "ms"), dc.UNKNOWN_UNIT), (("A", "d"), dc.UNKNOWN_UNIT),
    (("A", "Ah"), dc.UNKNOWN_UNIT), (("A", "A.h"), dc.UNKNOWN_UNIT),
    (("A", "mAh"), dc.UNKNOWN_UNIT), (("A", "mA·h"), dc.UNKNOWN_UNIT),
    (("A", "C"), dc.UNKNOWN_UNIT), (("A", "Wh"), dc.UNKNOWN_UNIT),
    (("A", "W·h"), dc.UNKNOWN_UNIT),
])
def test_units_are_exact_with_no_alias_or_conversion(units, reason):
    result = dc.execute(BINDING, _request(units=units))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, reason, None)


def test_the_hour_is_no_alias_of_the_second_and_the_energy_duration_stays_s():
    # the same typed number means different durations to the two methods: the
    # owner neither converts nor equates them, and each role admits its own token
    energy = dc.bind_method(energy_method.METHOD_ID, "1.0", energy_method.evaluate)
    energy_request = {"method_id": energy_method.METHOD_ID, "method_version": "1.0",
                      "inputs": {"v_load": {"value": 12.0, "unit": "V"},
                                 "r_load": {"value": 24.0, "unit": "Ω"},
                                 "t_duration": {"value": 1.0, "unit": "h"}},
                      "subject_ref": None}
    assert dc.execute(energy, energy_request)["reason"] == dc.UNIT_NOT_ADMITTED
    energy_request["inputs"]["t_duration"]["unit"] = "s"
    assert dc.execute(energy, energy_request)["outputs"]["e_load"]["value"] == 6.0
    assert dc.execute(BINDING, _request(0.5, 1.0, units=("A", "s")))["reason"] \
        == dc.UNIT_NOT_ADMITTED
    assert _q(dc.execute(BINDING, _request(0.5, 1.0))) == 0.5


def test_each_binding_executes_only_its_own_method():
    for binding in OTHER_BINDINGS:
        assert dc.execute(binding, _request())["reason"] == dc.OPERATION_NOT_ADMITTED
    swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, current_method.evaluate)
    assert _failure(dc.execute(swapped, _request()))
    assert dc.execute(dc.bind_method(method.METHOD_ID, "2.0", method.evaluate),
                      _request())["reason"] == dc.VERSION_MISMATCH


def test_app_wires_one_immutable_binding_per_method():
    assert webapp._DC_CHARGE_BINDING.adapter_identity \
        == "engine.dc_constant_current_charge_method.evaluate"
    with pytest.raises(AttributeError):
        webapp._DC_CHARGE_BINDING.method_id = "x"
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 11
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("import dc_constant_current_charge", "engine.dc_", "engine/dc_",
                   "dc_constant_current_charge_method.", "dc_constant_current_charge import",
                   "electrical_content_config", "import fractions", "decimal", "sqlite",
                   "3600", "coulomb"):
        assert banned not in owner_source.lower(), banned


def _owner_tamper(data, name):
    record = _record(data)
    if name == "eleventh_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "electrical:dc_constant_current_energy"
        data["methods"].append(extra)
    elif name == "output_kind":
        record["output_roles"][0]["quantity_kind"] = "energy"
    elif name == "output_unit":
        record["output_roles"][0]["unit_token"] = "J"
    elif name == "duration_unit_s":
        record["input_roles"][1]["unit_token"] = "s"      # s is admitted, but not for this role
        data["unit_records"] = [u for u in data["unit_records"] if u["unit_token"] != "h"]
    elif name == "policy_unresolved":
        record["source_qualification"][0]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "coulomb_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "A·h"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "C"
        data["unit_records"].append(extra)
    elif name == "milliampere_hour_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "A·h"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "mA·h"
        data["unit_records"].append(extra)
    elif name == "third_time_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "h"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "min"
        data["unit_records"].append(extra)
    elif name == "hour_rebound_to_charge":
        [u for u in data["unit_records"] if u["unit_token"] == "h"][0]["quantity_kind"] \
            = "electric_charge"
    elif name == "extra_kind":
        data["quantity_kinds"].append({"quantity_kind": "electric_charge_density",
                                       "dimension": "T I L^-3"})
    elif name == "drop_charge_kind":
        data["quantity_kinds"] = [k for k in data["quantity_kinds"]
                                  if k["quantity_kind"] != "electric_charge"]
    elif name == "unknown_condition":
        record["applicability"].append(
            {"role": "i_load", "condition": "non_negative", "bound_role": None})
    elif name == "basis":
        data["source_use_policies"][-1]["inspection_basis"] = "EXECUTOR"
    return data


@pytest.mark.parametrize("name", ["eleventh_method", "output_kind", "output_unit",
                                  "duration_unit_s", "policy_unresolved", "coulomb_unit",
                                  "milliampere_hour_unit", "third_time_unit",
                                  "hour_rebound_to_charge", "extra_kind",
                                  "drop_charge_kind", "unknown_condition", "basis"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), name))
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    assert _failure(dc.execute(BINDING, _request(), artifact_path=path))


def test_owner_v9_records_are_unchanged_by_the_tenth_admission():
    data = dc.load_artifact()
    assert data["artifact_version"] == "11"
    v9 = {"quantity_kinds": data["quantity_kinds"][:14],
          "unit_records": data["unit_records"][:15],
          "source_use_policies": data["source_use_policies"][:16],
          "methods": data["methods"][:9]}
    canonical = json.dumps(v9, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(canonical.encode()).hexdigest() == V9_RECORDS_DIGEST
    assert [k["quantity_kind"] for k in data["quantity_kinds"][14:]] == ["electric_charge"]
    assert [u["record_id"] for u in data["unit_records"][15:]] == ["dcu:U016", "dcu:U017"]
    assert [p["record_id"] for p in data["source_use_policies"][16:18]] == [
        "dcu:SU017", "dcu:SU018"]
    assert [m["method_id"] for m in data["methods"][9:10]] == [method.METHOD_ID]
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "dcq:SU002" in policies["dcu:SU017"]["inspected_content"]
    assert "dcu:U016 (h) and dcu:U017 (A·h) only" in policies["dcu:SU017"]["inspected_content"]
    assert "DOE-CHG-S1 only" in policies["dcu:SU018"]["inspected_content"]
    assert "dcu:SU014, the DC resistive load energy snapshot for J and s, is not extended" \
        in policies["dcu:SU017"]["inspection_reference"]
    text = json.dumps(data, ensure_ascii=False).lower()
    for banned in ("electric_charge_reference_v1", "charge_current_time_reference",
                   "battery capacity", "battery runtime", "state of charge", "mA·h"):
        assert banned not in text, banned
    assert "Content version 11 admits exactly eleven methods" in data["governance_note"]


# ==========================================================================
# 6. the method artifact and the consumer
# ==========================================================================
def test_method_artifact_loads_with_provenance_and_ip_boundary():
    data = dcq.load_artifact()
    by_id = {r["record_id"]: r for r in data["sources"]}
    doe = by_id["DOE-CHG-S1"]
    for phrase in ("flow of electric charge", "one coulomb", "ES-01 page 10",
                   "ARCHIVE - Canceled", "electronics_electrical:PR018",
                   "NOT claimed that DOE wrote Q = I x t", "Not re-inspected by the executor",
                   "no varying-current, average-current, duty-cycle or integration treatment"):
        assert phrase in doe["inspected_content"], phrase
    assert doe["source_use_policy_ref"] == "dcq:SU001"
    assert doe["url"].startswith("https://www.energy.gov/")
    nist = by_id["NIST-AH-S1"]
    for phrase in ("Table 3", "s · A", "Appendix B.9", "1 A · h = 3.6 × 10³ C",
                   "electronics_electrical:PR020", "never applied",
                   "NOT recorded here as an inspected location",
                   "not attributed to the 2008 PDF edition"):
        assert phrase in nist["inspected_content"], phrase
    assert nist["source_use_policy_ref"] == "dcq:SU002"
    assert by_id["dcq:SU001"]["url"] == "https://www.energy.gov/web-policies"
    assert "electronics_electrical:PR019" in by_id["dcq:SU001"]["inspected_content"]
    assert "electronics_electrical:PR021" in by_id["dcq:SU002"]["inspected_content"]
    for record in data["sources"]:
        assert record["inspection_basis"] == "LEAD_SUPPLIED"
        assert "endorse" in record["no_endorsement_limitation"]
    method_block = data["method"]
    assert "not claimed that DOE prints Q = I × t" in method_block["derivation"]
    assert "never applied" in method_block["derivation"]
    assert data["method"]["method_id"] == method.METHOD_ID
    assert [d["declaration_id"] for d in data["declarations"]] == list(dcq.DECLARATION_IDS)
    assert [s["item_id"] for s in data["screen_items"]] == list(dcq.SCREEN_ITEMS)
    assert len(data["disclosure"]) == 7


def test_no_protected_material_or_pack_change():
    # the pack, its reference group and its provenance records are untouched by
    # this method: the owner's units are its own records (git diff is the proof
    # of file identity; here the recorded scope statements are checked)
    pack = json.loads((ROOT / "domains" / "electronics_electrical" / "domain.json")
                      .read_text(encoding="utf-8"))
    (group,) = [g for g in pack["reference_fundamentals"]
                if g["group_id"] == "electric_charge_reference_v1"]
    claims = {c["claim_id"]: c for c in group["claims"]}
    assert "NOT added as units" in claims["ampere_hour_charge_unit"]["limitation"]
    assert "project-specific calculation" in claims["charge_current_time_reference"]["limitation"]
    prov = json.loads((ROOT / "domains" / "domain_provenance.json").read_text(encoding="utf-8"))
    records = prov["records"] if isinstance(prov, dict) else prov
    ids = {r["record_id"] for r in records}
    assert {"electronics_electrical:PR018", "electronics_electrical:PR019",
            "electronics_electrical:PR020", "electronics_electrical:PR021"} <= ids
    assert not any("dc_constant_current_charge" in json.dumps(r) for r in records)
    # the method artifact copies no DOE / NIST prose: every text is InventorAI's
    # own, and no copied-looking long passage names a handbook paragraph
    text = json.dumps(dcq.load_artifact(), ensure_ascii=False)
    for banned in ("Figure", "worked example:", "Table 3 reads", "verbatim"):
        assert banned not in text, banned


@pytest.mark.parametrize("mutate", [
    lambda d: d.__setitem__("artifact_version", "2"),
    lambda d: d["declarations"].pop(),
    lambda d: d["declarations"][0].__setitem__("accepted_value", "the current may vary"),
    lambda d: d["disclosure"].__setitem__(2, "This is a battery capacity."),
    lambda d: d["numeric_domain"]["roles"][1].__setitem__("unit_token", "s"),
    lambda d: d["numeric_domain"]["roles"][2].__setitem__("unit_token", "C"),
    lambda d: d["sources"].pop(),
    lambda d: d["sources"][0].__setitem__("inspection_basis", "EXECUTOR"),
    lambda d: d["screen_items"].pop(),
    lambda d: d.__setitem__("extra", 1),
    lambda d: d["method"].__setitem__("method_version", "1.1"),
])
def test_method_artifact_tamper_is_knowledge_unavailable(mutate, monkeypatch):
    data = _method_artifact()
    mutate(data)
    with pytest.raises(dcq.DcChargeKnowledgeError):
        dcq.validate_artifact(data)
    calls = _owner_spy(monkeypatch)
    evaluation = dcq.evaluate(_captured(), BINDING, artifact=data)
    assert evaluation["outcome"] == dcq.KNOWLEDGE_UNAVAILABLE
    assert evaluation["display_value"] is None and not calls


def test_unreadable_artifacts_give_no_number(tmp_path, monkeypatch):
    monkeypatch.setattr(dcq, "ARTIFACT_PATH", tmp_path / "missing.json")
    assert _evaluate()["outcome"] == dcq.KNOWLEDGE_UNAVAILABLE
    broken = tmp_path / "broken.json"
    broken.write_text("{", encoding="utf-8")
    monkeypatch.setattr(dcq, "ARTIFACT_PATH", broken)
    assert _evaluate()["outcome"] == dcq.KNOWLEDGE_UNAVAILABLE
    monkeypatch.undo()
    evaluation = dcq.evaluate(_captured(), BINDING, owner_artifact_path=tmp_path / "no.json")
    assert evaluation["outcome"] == dcq.KNOWLEDGE_UNAVAILABLE
    assert (evaluation["owner_state"], evaluation["owner_reason"]) == (
        dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE)


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = _owner_spy(monkeypatch)
    # everything wrong at once: completeness wins
    bad = _form(i="-1", t="-1", decl={"constant_dc_current": ""},
                screen={"safety_function": "yes"})
    assert _evaluate(i="-1", t="-1", decl={"constant_dc_current": ""},
                     screen={"safety_function": "yes"})["outcome"] == dcq.NOT_DECLARED
    assert _evaluate(i="-1", t="-1", decl={"constant_dc_current": "does_not_apply"},
                     screen={"safety_function": "yes"})["outcome"] \
        == dcq.ENGINEERING_REVIEW_REQUIRED
    assert _evaluate(i="-1", t="-1", decl={"constant_dc_current": "does_not_apply"})["outcome"] \
        == dcq.MODEL_NOT_SUPPORTED
    assert _evaluate(i="x", t="-1")["outcome"] == dcq.INVALID_NUMERIC_INPUT
    assert _evaluate(i="-1", t="-1")["outcome"] == dcq.CURRENT_NEGATIVE
    assert _evaluate(i="1", t="-1")["outcome"] == dcq.DURATION_NEGATIVE
    assert not calls and bad


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, dcq.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, dcq.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, dcq.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, dcq.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, dcq.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, dcq.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, dcq.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, dcq.UNMAPPED_OWNER_OUTCOME),
    ("WEIRD", "x", dcq.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome, monkeypatch):
    monkeypatch.setattr(dc, "execute",
                        lambda *a, **k: {"state": state, "reason": reason, "outputs": None})
    evaluation = _evaluate()
    assert evaluation["outcome"] == outcome
    assert (evaluation["owner_state"], evaluation["owner_reason"]) == (state, reason)
    assert evaluation["display_value"] is None and evaluation["result"] is None


@pytest.mark.parametrize("produced", [2.0000001, -2.0, 0.0, -0.0, float("nan"),
                                      float("inf"), 2.0 * (1 + 2 ** -50), "2.0", None])
def test_decimal_reference_failure_fails_closed_with_no_number(produced, monkeypatch):
    real = dc.execute

    def fake(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["q_load"]["value"] = produced
        return result
    monkeypatch.setattr(dc, "execute", fake)
    evaluation = _evaluate()
    assert evaluation["outcome"] == dcq.KNOWLEDGE_UNAVAILABLE
    assert evaluation["display_value"] is None and evaluation["result"] is None


def test_zero_must_be_positive_zero_and_only_for_zero_current_or_duration(monkeypatch):
    assert dcq.agrees_with_reference(0.0, Fraction(0))
    assert not dcq.agrees_with_reference(-0.0, Fraction(0))
    assert not dcq.agrees_with_reference(0.0, Fraction(1, 10 ** 18))
    assert not dcq.agrees_with_reference(1e-18, Fraction(0))
    assert dcq.agrees_with_reference(2.0, Fraction(2))
    assert not dcq.agrees_with_reference(2.0, Fraction(-2))
    real = dc.execute

    def fake(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["q_load"]["value"] = -0.0
        return result
    monkeypatch.setattr(dc, "execute", fake)
    assert _evaluate(i="0")["outcome"] == dcq.KNOWLEDGE_UNAVAILABLE


def test_consumer_sends_the_correctly_rounded_values_and_fixed_units(monkeypatch):
    calls = _owner_spy(monkeypatch)
    _evaluate(i="0.1", t="0.3")
    (request, _result), = calls
    assert request["inputs"] == {"i_load": {"value": 0.1, "unit": "A"},
                                 "t_duration": {"value": 0.3, "unit": "h"}}
    assert request["inputs"]["i_load"]["value"] == float(Fraction("0.1"))
    assert (request["method_id"], request["method_version"], request["subject_ref"]) \
        == (method.METHOD_ID, "1.0", None)


def test_requests_are_isolated_and_inputs_not_mutated():
    captured = _captured(i="0.5", t="4")
    before = copy.deepcopy(captured)
    first = dcq.evaluate(captured, BINDING)
    second = dcq.evaluate(captured, BINDING)
    assert captured == before
    assert first["display_value"] == second["display_value"] == "2"
    assert first["result"]["result_identity"] == second["result"]["result_identity"]
    first["result"]["outputs"]["q_load"]["value"] = 99.0
    assert dcq.evaluate(captured, BINDING)["result"]["outputs"]["q_load"]["value"] == 2.0


def test_consumer_and_adapter_import_no_other_authority():
    import ast
    for module in (dcq, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        for banned in ("cap13", "therm01", "tmp36", "dc_resistive_load", "record_store",
                       "safety_signal", "requests", "urllib", "openai", "web", "flask",
                       "random", "time", "sqlite3", "domain_rules", "numpy", "scipy",
                       "subsystem_model", "idea_state"):
            assert not any(banned == n or n.startswith(banned + ".") or banned in n
                           for n in names if n), (module.__name__, banned)


# ==========================================================================
# 7. EN / AR fidelity, the forbidden wording and the contracts
# ==========================================================================
def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_english_wording_equals_the_artifact():
    content = dcq.load_artifact()
    assert ui_text.text("UI_DCQ_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"]
        assert ui_text.text("UI_DCQ_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."
    for entry in content["screen_items"]:
        value = entry["item"]
        assert ui_text.text("UI_DCQ_SCREEN_" + entry["item_id"].upper(), "en") \
            == value[0].upper() + value[1:]


def test_arabic_wording_equals_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    assert ui_text.text("UI_DCQ_DISCLOSURE", "ar").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$",
                           _contract_section("**A-2", "**A-3"), re.M))
    for decl, ref in dcq.DECLARATIONS:
        assert ui_text.text("UI_DCQ_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    screen = dict(re.findall(r"^\| (\w+) \| (.+?) \|$",
                             _contract_section("**A-3", "**A-4"), re.M))
    for item in dcq.SCREEN_ITEMS:
        assert ui_text.text("UI_DCQ_SCREEN_" + item.upper(), "ar") == screen[item], item
    s9 = _contract_section("## 9. Result", "## 9A.")
    assert [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)] \
        == dcq.load_artifact()["disclosure"]
    s5 = _contract_section("## 5. Applicability", "## 6.")
    english = dict(re.findall(r"^\| (D-\d) \| `\w+` \| (.+?) \|$", s5, re.M))
    for entry in dcq.load_artifact()["declarations"]:
        assert english[entry["contract_ref"]] == entry["accepted_value"]


def test_every_key_has_both_languages_and_the_owner_boundary_wording():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_DCQ_[A-Z0-9_]+)": \{', source)
    assert len(keys) >= 45
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in FORBIDDEN + (
            "the load is safe", "measured by inventorai", "guaranteed", "certified",
            "has been validated", "recommended", "battery will last", "battery capacity is",
            "is enough", "is rated", "runtime is", "enough charge", "you need a battery"):
        assert claim not in english, claim
    for phrase in ("charge that flows through the load during the declared constant-current "
                   "duration", "not a battery capacity", "not an energy", "state of charge",
                   "compared with no rating", "cannot determine how long a real battery lasts",
                   "does not establish that the current is constant", "duty-cycled",
                   "inrush", "ac behaviour", "next engineering need", "remain unverified",
                   "not physical limits", "labelled rounded", "never negative",
                   "no unit is converted", "unvalidated"):
        assert phrase in english, phrase
    # the Arabic keeps the same boundary
    arabic = " ".join(ui_text.text(k, "ar") for k in keys)
    for phrase in ("ليست سعة بطارية", "شحنة وليست طاقة", "لا تُقارن بأي قيمة اسمية",
                   "لا يثبت أن التيار ثابت", "UNVALIDATED", "A·h"):
        assert phrase in arabic, phrase


def test_forbidden_battery_wording_is_absent_from_every_surface():
    surfaces = [
        json.dumps(dcq.load_artifact(), ensure_ascii=False),
        json.dumps(_record(dc.load_artifact()), ensure_ascii=False),
        (ROOT / "web" / "templates" / "dc_constant_current_charge.html").read_text(encoding="utf-8"),
        Path(dcq.__file__).read_text(encoding="utf-8"),
        Path(method.__file__).read_text(encoding="utf-8"),
        " ".join(ui_text.text(k, "en") for k in re.findall(
            r'"(UI_DCQ_[A-Z0-9_]+)": \{', Path(ui_text.__file__).read_text(encoding="utf-8"))),
    ]
    for surface in surfaces:
        lowered = surface.lower()
        for phrase in FORBIDDEN:
            assert phrase not in lowered, phrase
    # the contract names them only as excluded wording
    contract = CONTRACT.read_text(encoding="utf-8")
    assert "never\nappear on any surface" in contract.replace('"battery size"', "x") \
        or "never appear on any surface" in _norm(contract)


def test_correction_10_is_recorded_and_earlier_sections_unchanged():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 10" in body and "## 13I." in body
    section = _norm(body[body.index("## 13I."):body.index("## 14.")])
    for phrase in ("exactly ten", "`electrical:dc_constant_current_charge`",
                   "one kind and two tokens added", "`dcu:U016`", "`dcu:U017`", "`dcu:SU017`",
                   "`dcu:SU018`", "content version `10`", "`1.9.0`",
                   "Second named token exception", "`KIND_TOKEN_EXCEPTIONS`",
                   "nothing maps `h` to `s`", "`electronics_electrical:PR020` keeps its own scope",
                   "NOT a generic owner policy", "No consumer imports another",
                   "within a relative `2^-51`", "never a negative zero",
                   "`A·h` is not related to `C`", "not recorded as an inspected location",
                   "declares NO owner condition"):
        assert phrase in section, phrase
    assert "**Methods — exactly nine:**" in body[body.index("## 13H."):body.index("## 13I.")]
    assert "- Correction 10 (§13I) is Owner-authorized" in body
    assert body.count("## 13I.") == 1


def test_method_contract_records_scope_provenance_and_exclusions():
    text = _norm(CONTRACT.read_text(encoding="utf-8"))
    for phrase in ("DOE-HDBK-1011/1-92", "ES-01 page 10", "electronics_electrical:PR018",
                   "electronics_electrical:PR019", "electronics_electrical:PR020",
                   "electronics_electrical:PR021", "1 A · h = 3.6 × 10³ C",
                   "NOT claimed that DOE prints the integrated formula",
                   "Constant-current assumption", "`0.5 A / 4 h = 2 A·h`", "3.0000001",
                   "Battery / BMS", "Representation limits are not physical limits",
                   "labelled exact when", "1 × 10^-18", "`CURRENT_NEGATIVE`",
                   "`DURATION_NEGATIVE`", "second named token exception",
                   "NOT recorded as an inspected location", "Not relied upon",
                   "no external modelling library or code is used",
                   "the SAME `_calc_gate` / `_calc_declared_part` rule",
                   "The Stage 15 exception in `engine/subsystem_model.py` names this method",
                   "an earlier rendered page grants nothing",
                   "Stage 15 part eligibility only as stated in §1",
                   "a charge and not an energy", "compared with any rating"):
        assert phrase in text, phrase
    model = Path(ROOT / "engine" / "subsystem_model.py").read_text(encoding="utf-8")
    assert "DC-CONSTANT-CURRENT-CHARGE-01" in model
    assert "``electrical:dc_constant_current_charge``" in model


# ==========================================================================
# 8. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_electronics_root_journey_and_reference_values(elec):
    c, _aid, sid = elec
    assert "data-dcq-link" in _page(c, sid)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-dcq-form" in body and "checked" not in body
    assert "data-dcq-value-note" in body and body.count('type="radio"') == 20
    for i, t, expected in REFERENCE:
        body = c.post(URL % sid, data=_form(i=i, t=t)).get_data(as_text=True)
        assert _value(body) == "%s A·h" % expected, (i, t)
        assert 'data-dcq-exactness="exact"' in body
    body = c.post(URL % sid, data=_form(i="0", t="4")).get_data(as_text=True)
    assert _value(body) == "0 A·h" and 'data-dcq-exactness="exact"' in body
    body = c.post(URL % sid, data=_form(i="1.234567891", t="1.234567891")).get_data(as_text=True)
    assert _value(body) == "1.52415787749 A·h"
    assert 'data-dcq-exactness="rounded"' in body
    assert "data-dcq-not-battery" in body and "data-dcq-charge-not-energy" in body
    assert "UNVALIDATED" in body and "NOT EVIDENCE" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_DCQ_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert "DOE-HDBK-1011/1-92" in body and "NIST" in body
    assert "electrical:dc_constant_current_charge" in body
    assert '<bdi dir="ltr" data-dcq-echo-value>1.234567891</bdi>' in body
    lowered = html.unescape(body).lower()
    for phrase in FORBIDDEN:
        assert phrase not in lowered, phrase


@pytest.mark.parametrize("over,outcome", [
    ({"i": "-0.5"}, "CURRENT_NEGATIVE"),
    ({"t": "-1"}, "DURATION_NEGATIVE"),
    ({"i": "-1", "t": "-1"}, "CURRENT_NEGATIVE"),
    ({"t": "1h"}, "INVALID_NUMERIC_INPUT"),
    ({"i": "500mA"}, "INVALID_NUMERIC_INPUT"),
    ({"t": ""}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"battery_or_storage_cell": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"constant_dc_current": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"charge_through_load": ""}}, "NOT_DECLARED"),
])
def test_non_success_shows_one_reason_and_no_number(elec, over, outcome):
    c, _aid, sid = elec
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert ui_text.text("UI_DCQ_OUTCOME_" + outcome, "en") in html.unescape(body)
    assert _value(body) is None
    assert body.count("data-dcq-outcome") == 1 and "data-dcq-result" not in body


def test_mechanical_root_is_not_eligible_but_a_declared_part_is(mech, monkeypatch):
    c, _aid, sid = mech
    assert "data-dcq-link" not in _page(c, sid)
    assert webapp._calc_gate(sid, dcq) == (False, None)
    called = []
    monkeypatch.setattr(webapp._dcq, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-dcq-scope-note" in body
        assert "data-dcq-form" not in body and _value(body) is None
    assert not called


@pytest.mark.parametrize("focus,extra", [(MECH, {}), (ELEC, {}), (MECH, CTRL), (ELEC, CTRL)],
                         ids=["mech-focus", "elec-focus", "mech-focus-3", "elec-focus-3"])
def test_the_declared_electronics_part_is_offered_with_attribution(focus, extra, monkeypatch):
    c, _ = _client_for("dcq-part-%s-%d@example.com" % (focus, len(extra)))
    sid = _integrated(c, focus, **extra)
    eligible, part = webapp._calc_gate(sid, dcq)
    assert eligible and part.domain == ELEC
    assert webapp._dcq_eligible(sid)
    assert "data-dcq-link" in _page(c, sid)
    get = c.get(URL % sid).get_data(as_text=True)
    assert "data-dcq-form" in get and "checked" not in get
    assert _part_line(get, "dcq") == PARTS["elec_part_name"]
    calls = _owner_spy(monkeypatch)
    post = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(post) == "2 A·h"
    assert _part_line(post, "dcq") == PARTS["elec_part_name"]
    assert len(calls) == 1 and calls[0][0]["method_id"] == method.METHOD_ID


def test_a_stale_page_grants_nothing_after_the_composition_changes(monkeypatch):
    c, _ = _client_for("dcq-stale@example.com")
    sid = _integrated(c, MECH)
    assert "data-dcq-form" in c.get(URL % sid).get_data(as_text=True)
    _corrupt("DELETE FROM project_subsystems WHERE subsystem_seq = 1")
    calls = _owner_spy(monkeypatch)
    assert webapp._calc_gate(sid, dcq) == (False, None)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-dcq-form" not in body and _value(body) is None
    assert "data-dcq-part" not in body and not calls


def test_the_part_name_is_escaped_and_bilingual():
    c, _ = _client_for("dcq-escape@example.com")
    sid = _integrated(c, MECH, elec_part_name=HOSTILE)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "<script>" not in body
    assert html.unescape(_part_line(body, "dcq")) == HOSTILE
    for lang in ("en", "ar"):
        if lang == "ar":
            assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
        page = c.get(URL % sid).get_data(as_text=True)
        text = html.unescape(re.sub(r"<[^>]+>", "", page))
        for key in ("UI_THERM01_PART_LABEL", "UI_THERM01_PART_NOTE", "UI_DCQ_SCOPE_NOTE"):
            assert re.sub(r"\s+", " ", ui_text.text(key, lang)) in re.sub(r"\s+", " ", text), \
                (key, lang)


def test_request_supplied_domain_or_part_never_grants_eligibility(mech, monkeypatch):
    c, _aid, sid = mech
    calls = _owner_spy(monkeypatch)
    for extra in ({"root_domain": ELEC}, {"domain": ELEC}, {"part_id": "x"},
                  {"declared_part": PARTS["elec_part_name"]}):
        r = c.post(URL % sid, data=dict(_form(), **extra))
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-dcq-form" not in body and _value(body) is None
        r = c.get((URL % sid) + "?domain=%s" % ELEC)
        assert "data-dcq-form" not in r.get_data(as_text=True)
    assert not calls


def test_unreadable_root_domain_grants_nothing(elec, monkeypatch):
    c, _aid, sid = elec

    def broken(_sid):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(webapp, "_cap12_root_domain", broken)
    assert not webapp._dcq_eligible(sid)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-dcq-form" not in body and _value(body) is None


def test_csrf_authorization_and_malformed_requests(elec):
    c, _aid, sid = elec
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("dcq-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302 and "data-dcq" not in r.get_data(as_text=True)
    for bad in (dict(_form(), unexpected="1"),
                dict(_form(), screen_safety_function="maybe"),
                dict(_form(), value_q_load="6")):
        r = c.post(URL % sid, data=bad)
        assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    from werkzeug.datastructures import MultiDict
    r = c.post(URL % sid, data=MultiDict(list(_form().items())
                                         + [(dcq.VALUE_FIELD % "t_duration", "13")]))
    assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    body = c.post(URL % sid, data=_form(t="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body
    assert c.get(URL % sid).headers["Cache-Control"] == "no-store"


@pytest.mark.parametrize("over", [{}, {"t": "-5"}, {"screen": {"safety_function": "yes"}}])
def test_nothing_is_persisted_and_no_request_leaks_into_the_next(elec, over):
    c, _aid, sid = elec
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(i="7.5", **over))
    body = c.get(URL % sid).get_data(as_text=True)
    assert _snapshot(c) == before
    assert "7.5" not in body and "checked" not in body and _value(body) is None


def test_no_report_export_api_or_safety_surface():
    src = Path(webapp.__file__).read_text(encoding="utf-8")
    start = src.index("# DC-CONSTANT-CURRENT-CHARGE-01 — DC Constant-Current Charge")
    section = src[start:src.index("# PWM-AVERAGE-VOLTAGE-01 —", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "_cap13", "_tmp36", "_dcl.", "_dcp.", "_dce.", "_dce_",
                   "load_project_subsystems", "request.args", "cap09",
                   "success_criteria", "redirect(", "3600", "openai", "provider"):
        assert banned not in section, banned
    assert section.count("_dcalc.bind_method(") == 1
    assert [r.rule for r in webapp.app.url_map.iter_rules()
            if "dc-constant-current-charge" in r.rule] \
        == ["/session/<sid>/dc-constant-current-charge"] * 2
    for template in ("deliverable.html", "report.html", "success_criteria.html",
                     "parts_components_interactions.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "dc-constant-current-charge" not in path.read_text(encoding="utf-8").lower()
    for module in ("engine/disclosure_export.py", "engine/deliverable_assembler.py",
                   "engine/safety_signal.py", "engine/readiness_snapshot.py"):
        assert "charge" not in (ROOT / module).read_text(encoding="utf-8").lower() \
            or "dc_constant_current" not in (ROOT / module).read_text(encoding="utf-8")


def test_existing_nine_calculations_are_unchanged(mech, elec):
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
    assert "data-cap13f-result-value" in body or "N</bdi>" in body
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


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_arabic_isolation_and_zero_input(elec, lang):
    c, _aid, sid = elec
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form(i="0.5", t="4")).get_data(as_text=True)
    assert _value(body) == "2 A·h"
    assert '<bdi dir="ltr" data-dcq-echo-value>0.5</bdi>' in body
    if lang == "ar":
        assert 'dir="rtl"' in body
        isolated = [html.unescape(run)
                    for run in re.findall(r'<bdi dir="ltr">([^<]*)</bdi>', body)]
        for token in ("UNVALIDATED", "NOT EVIDENCE", "DOE-HDBK-1011/1-92", "(A)", "(h)",
                      "(A·h)", "(t)", "(I)", "(Q)"):
            assert any(token in run for run in isolated), token
        assert any(run == "Q = I × t" for run in isolated)
        stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
        for item in ui_text.text("UI_DCQ_DISCLOSURE", "ar").split("\n\n"):
            assert _norm(item) in _norm(stripped), item[:30]
        refusal = c.post(URL % sid, data=_form(i="-1")).get_data(as_text=True)
        assert _norm(ui_text.text("UI_DCQ_OUTCOME_CURRENT_NEGATIVE", "ar")) \
            in _norm(html.unescape(re.sub(r"<[^>]+>", "", refusal)))
        assert _value(refusal) is None
