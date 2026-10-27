# -*- coding: utf-8 -*-
"""Sensors C3 - TMP36 Nominal Voltage-to-Temperature, Slice 1 (directly owning tests).

TMP36-NOMINAL-VOLTAGE-TEMPERATURE-01. The shared deterministic calculation /
units owner after the bounded fifth admission of calc/units Correction 05
(§13D); the ONE method ``tmp36:nominal_voltage_to_temperature`` 1.0
(``engine/tmp36_nominal_temperature_method.py``) and its ONE consumer
(``engine/tmp36_nominal_temperature.py`` + the request-local page).

Scientific reference: the nominal TMP36 output characteristic of the Analog
Devices TMP35/TMP36/TMP37 data sheet, Rev. H (offset 500 mV, 10 mV/°C):
T = (V_OUT - 500) / 10. The numerical tests use an INDEPENDENT decimal
reference: every expected temperature is formed with ``decimal.Decimal`` from
the typed decimal string, never from the consumer's or the adapter's own
arithmetic. Synthetic data.
"""
import copy
import html
import json
import math
import random
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import tmp36_nominal_temperature as tmp36
from engine import tmp36_nominal_temperature_method as method
from engine import cap13_static_reactions_method as cap13_method
from engine import cap13_planar_moment_method as moment_method
from engine import cap13_rotational_load_method as rotational_method
from engine import therm01_conduction_method as therm_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _corrupt, _owner_spy, _part_line, MECH, ELEC, PARTS, HOSTILE)
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_therm01_temperature_difference import _form as _therm_form
from tests.test_cap13_planar_moment import _form as _moment_form
from tests.test_cap13_rotational_load import _form as _rotational_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "SENSORS_C3_TMP36_NOMINAL_VOLTAGE_TO_TEMPERATURE_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
DATASHEET = "https://www.analog.com/media/en/technical-documentation/data-sheets/TMP35_36_37.pdf"
DATASHEET_SHA256 = "6ce062fb73f0bebb61f82775aca0be56903c2b8484a7fc89a0cf71961189f8ee"
URL = "/session/%s/tmp36-temperature"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
OTHER_BINDINGS = (
    dc.bind_method(cap13_method.METHOD_ID, "1.0", cap13_method.evaluate),
    dc.bind_method(therm_method.METHOD_ID, "1.0", therm_method.evaluate),
    dc.bind_method(moment_method.METHOD_ID, "1.0", moment_method.evaluate),
    dc.bind_method(rotational_method.METHOD_ID, "1.0", rotational_method.evaluate))
# The Owner's reference vectors (mV -> nominal °C).
REFERENCE = (("100", -40), ("400", -10), ("500", 0), ("750", 25), ("1000", 50),
             ("1750", 125))
DECIMAL_BOUND = Fraction(1, 2 ** 45)
PROVEN_WORST_CASE = Fraction(13, 10) * Fraction(1, 2 ** 46)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _reference(text):
    """The independent decimal reference: (Decimal(V) - 500) / 10, exact."""
    return (Decimal(text) - Decimal(500)) / Decimal(10)


def _reference_display(text):
    """The expected display, from the decimal reference alone: at least one and
    at most four digits after the point, no rounding."""
    value = _reference(text)
    sign = "-" if value < 0 else ""
    whole, _, fraction = ("%.4f" % abs(value)).partition(".")
    assert Decimal("%s%s.%s" % (sign, whole, fraction)) == value     # exact, no rounding
    return "%s%s.%s" % (sign, whole, fraction.rstrip("0") or "0")


def _request(v_out=750.0, unit="mV", **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"v_out": {"value": v_out, "unit": unit}},
           "subject_ref": None}
    req.update(over)
    return req


def _run(v_out):
    return dc.execute(BINDING, _request(v_out))


def _t(result):
    return result["outputs"]["t_celsius"]["value"]


def _failure(result):
    return (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def _form(v_out="750", decl=None, screen=None):
    form = {tmp36.DECLARATION_FIELD % d: tmp36.ANSWER_APPLIES
            for d in tmp36.DECLARATION_IDS}
    form.update({tmp36.SCREEN_FIELD % s: tmp36.SCREEN_NO for s in tmp36.SCREEN_ITEMS})
    form[tmp36.VALUE_FIELD % "v_out"] = v_out
    for key, value in (decl or {}).items():
        form[tmp36.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[tmp36.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = tmp36.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return tmp36.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _method_artifact():
    return json.loads(tmp36.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data):
    target = tmp_path / "a.json"
    target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return target


def _value(body):
    marker = 'data-tmp36-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def _check_against_reference(text):
    """One typed decimal through the whole consumer: success, the owner result
    within the decimal bound, the display equal to the reference."""
    evaluation = _evaluate(v_out=text)
    assert evaluation["outcome"] == tmp36.OUTCOME_SUCCESS, text
    reference = Fraction(_reference(text))
    produced = _t(evaluation["result"])
    error = abs(Fraction(produced) - reference)
    assert error <= PROVEN_WORST_CASE < DECIMAL_BOUND, text
    assert (produced == 0.0) == (reference == 0), text
    assert (produced < 0) == (reference < 0), text
    assert evaluation["display_value"] == _reference_display(text), text
    return error


@pytest.fixture
def elec():
    c, aid = _client_for("tmp36-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def mech():
    c, aid = _client_for("tmp36-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": MECH})


# ==========================================================================
# 1. the Owner's reference vectors
# ==========================================================================
@pytest.mark.parametrize("text,expected", REFERENCE)
def test_reference_vectors_at_owner_adapter_and_consumer(text, expected):
    result = _run(float(text))
    assert result["state"] == dc.STATE_SUCCESS
    assert _t(result) == float(expected)
    assert result["outputs"]["t_celsius"]["unit"] == "°C"
    assert result["inputs"]["v_out"] == {"value": float(text), "unit": "mV",
                                         "provenance": "OWNER_STATED"}
    assert result["validation_status"] == "UNVALIDATED"
    assert method.evaluate(float(text)) == {"t_celsius": float(expected)}
    evaluation = _evaluate(v_out=text)
    assert evaluation["outcome"] == tmp36.OUTCOME_SUCCESS
    assert evaluation["display_value"] == "%d.0" % expected
    assert _reference(text) == expected


def test_zero_at_500_mv_is_exact_positive_zero():
    for text in ("500", "500.0", "500.000", "0500"):
        evaluation = _evaluate(v_out=text)
        produced = _t(evaluation["result"])
        assert produced == 0.0 and math.copysign(1.0, produced) == 1.0
        assert evaluation["display_value"] == "0.0"
    assert method.evaluate(500.0) == {"t_celsius": 0.0}


# ==========================================================================
# 2. the nominal-model interval, decided from the exact decimal
# ==========================================================================
@pytest.mark.parametrize("text", ["100", "100.0", "100.001", "1749.999", "1750",
                                  "1750.000", "0100", "499.999", "500.001"])
def test_just_inside_the_interval_is_calculated(text):
    _check_against_reference(text)


@pytest.mark.parametrize("text", ["99.999", "99.9", "0", "0.001", "50",
                                  "1750.001", "1750.01", "1751", "2000", "9" * 64])
def test_just_outside_the_interval_is_refused_before_the_owner(text, monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    evaluation = _evaluate(v_out=text)
    assert evaluation["outcome"] == tmp36.OUTSIDE_NOMINAL_MODEL_RANGE, text
    assert evaluation["result"] is None and evaluation["display_value"] is None
    assert not calls


def test_the_interval_is_checked_before_binary_rounding():
    # a decimal just beyond an end can round to that end in binary64; the exact
    # decimal check refuses it all the same (here at the 64-character limit)
    beyond = "1750." + "0" * 57 + "1"
    assert len(beyond) <= 64 and float(beyond) == 1750.0
    assert tmp36.parse_millivolts(beyond) is None          # more than three digits
    assert not tmp36.within_nominal_interval(Fraction("1750.001"))
    assert not tmp36.within_nominal_interval(Fraction("99.999"))
    assert tmp36.within_nominal_interval(Fraction(100))
    assert tmp36.within_nominal_interval(Fraction(1750))
    # the ends are exact in binary64, so admitted decimals stay inside after rounding
    assert float(Fraction(100)) == 100.0 and float(Fraction(1750)) == 1750.0


@pytest.mark.parametrize("text,display", [
    ("750.1", "25.01"), ("750.5", "25.05"), ("750.123", "25.0123"), ("400.5", "-9.95"),
    ("123.456", "-37.6544"), ("1234.567", "73.4567"), ("100.01", "-39.999"),
    ("499.999", "-0.0001"), ("500.001", "0.0001"), ("500.01", "0.001"),
    ("499.9", "-0.01"), ("1749.999", "124.9999")])
def test_decimal_fractions_and_the_zero_crossing(text, display):
    _check_against_reference(text)
    assert _evaluate(v_out=text)["display_value"] == display


def test_exhaustive_reference_near_the_ends_and_the_zero_crossing():
    worst = Fraction(0)
    for centre in (100000, 500000, 1750000):            # in thousandths of a mV
        for n in range(centre - 3000, centre + 3001):
            if not 100000 <= n <= 1750000:
                continue
            text = "%d.%03d" % divmod(n, 1000)
            worst = max(worst, _check_against_reference(text))
    assert worst <= PROVEN_WORST_CASE


def test_random_admitted_decimals_against_the_independent_reference():
    rng = random.Random(20261024)
    worst = Fraction(0)
    for _ in range(20000):
        n = rng.randint(100000, 1750000)
        digits = rng.choice((0, 1, 2, 3))
        if digits == 0:
            n -= n % 1000
            text = "%d" % (n // 1000)
        else:
            n -= n % (10 ** (3 - digits))
            text = ("%d.%03d" % divmod(n, 1000))[:-(3 - digits) or None]
        worst = max(worst, _check_against_reference(text))
    assert 0 < worst <= PROVEN_WORST_CASE


def test_the_error_bound_proof_holds_at_the_largest_admitted_ulp():
    # |V - D| <= 2**-43 for D < 2048, /10, plus 2**-47 for the rounding of T
    assert Fraction(1, 2 ** 43) / 10 + Fraction(1, 2 ** 47) == PROVEN_WORST_CASE
    assert math.ulp(1750.0) == 2.0 ** -42 and math.ulp(125.0) == 2.0 ** -46
    # every nonzero admitted result is far from zero, so sign and zero survive
    assert Fraction(1, 10000) > 10 ** 9 * DECIMAL_BOUND


# ==========================================================================
# 3. the adapter's binary acceptance; overflow / underflow resistance
# ==========================================================================
@pytest.mark.parametrize("v_out", [99.99999999999999, 1750.0000000000002, 1e308,
                                   5e-324, 2.2250738585072014e-308, 0.1])
def test_values_outside_the_interval_fail_closed_in_the_adapter(v_out):
    with pytest.raises(ArithmeticError):
        method.evaluate(v_out)
    assert _failure(_run(v_out))          # positive, so the owner applicability passes


@pytest.mark.parametrize("v_out", [0.0, -0.0, -1.0, -1750.0, -1e308])
def test_non_positive_values_are_declined_by_the_owner(v_out):
    result = _run(v_out)
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"),
                                   True, "750", None])
def test_non_finite_and_non_numeric_inputs_are_refused(value):
    req = _request()
    req["inputs"]["v_out"]["value"] = value
    result = dc.execute(BINDING, req)
    assert result["outputs"] is None
    assert result["reason"] in (dc.INVALID_NUMERIC_INPUT, dc.INPUT_MISSING)


def test_adapter_refuses_non_float_arguments():
    for bad in (750, "750", None, Decimal("750"), Fraction(750)):
        with pytest.raises(ArithmeticError):
            method.evaluate(bad)


def test_adapter_results_are_correctly_rounded_within_the_bound():
    rng = random.Random(36)
    for _ in range(5000):
        v_out = rng.uniform(100.0, 1750.0)
        exact = (Fraction(v_out) - 500) / 10
        produced = method.evaluate(v_out)["t_celsius"]
        assert produced == float(exact)
        assert abs(Fraction(produced) - exact) <= abs(exact) * method.RELATIVE_ERROR_BOUND
        assert -40.0 <= produced <= 125.0


def test_overflow_and_underflow_cannot_occur_inside_the_interval():
    # the largest operand and result are bounded and every nonzero exact result
    # is at least 1e-17 in magnitude for binary inputs inside the interval
    nearest = math.nextafter(500.0, 1000.0)
    produced = method.evaluate(nearest)["t_celsius"]
    assert produced > 0 and produced == float((Fraction(nearest) - 500) / 10)
    assert method.evaluate(1750.0) == {"t_celsius": 125.0}
    assert method.evaluate(100.0) == {"t_celsius": -40.0}


# ==========================================================================
# 4. the input grammar
# ==========================================================================
@pytest.mark.parametrize("text", [
    "", " ", "750 ", " 750", "+750", "-750", "750.", ".5", "750.1234", "7,50",
    "7_50", "1e3", "1E3", "0x2EE", "inf", "nan", "Infinity", "٧٥٠", "７５０",
    "750mV", "750 mV", "0.75V", "750.0.0", "9" * 65])
def test_malformed_values_are_invalid_and_never_reach_the_owner(text, monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    evaluation = _evaluate(v_out=text)
    assert evaluation["outcome"] == tmp36.INVALID_NUMERIC_INPUT, text
    assert evaluation["display_value"] is None and not calls


def test_accepted_grammar_is_exact():
    assert tmp36.parse_millivolts("750") == Fraction(750)
    assert tmp36.parse_millivolts("750.125") == Fraction(6001, 8)
    assert tmp36.parse_millivolts("0750.1") == Fraction(7501, 10)
    assert tmp36.parse_millivolts("750.1234") is None
    assert tmp36.parse_millivolts(None) is None
    assert tmp36.MAX_FRACTION_DIGITS == 3


def test_omitted_value_is_invalid():
    captured = tmp36.capture_form({k: [v] for k, v in _form().items()
                                   if k != tmp36.VALUE_FIELD % "v_out"})
    assert tmp36.evaluate(captured, BINDING)["outcome"] == tmp36.INVALID_NUMERIC_INPUT


# ==========================================================================
# 5. the owner: inventory, units, bindings and integrity (Correction 05)
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["outputs"] == {"t_celsius": {"value": 25.0, "unit": "°C",
                                               "provenance": "CALCULATED"}}
    assert [u["record_id"] for u in result["unit_records"]] == ["dcu:U009", "dcu:U010"]
    assert [q["source_ref"] for q in result["source_qualification"]] == ["ADI-S1"]
    assert result["source_qualification"][0]["url"] == DATASHEET
    assert (result["artifact_version"], result["implementation_version"]) == ("9", "1.8.0")
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_units_and_condition():
    assert ("tmp36:nominal_voltage_to_temperature", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 9
    assert {"voltage", "celsius_temperature"} <= dc.ADMITTED_QUANTITY_KINDS
    assert {"mV", "°C"} <= dc.ADMITTED_UNIT_TOKENS
    assert dc._CONDITIONS == ("greater_than_zero", "less_than_zero",
                              "within_zero_and_role")      # unchanged vocabulary
    record = _record(dc.load_artifact())
    assert record["applicability"] == [
        {"role": "v_out", "condition": "greater_than_zero", "bound_role": None}]
    assert record["result_range"] == []
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"] + record["output_roles"]] == [
        ("v_out", "voltage", "mV"), ("t_celsius", "celsius_temperature", "°C")]


@pytest.mark.parametrize("unit,reason", [
    ("mv", dc.UNKNOWN_UNIT), ("MV", dc.UNKNOWN_UNIT), ("V", dc.UNIT_NOT_ADMITTED),
    ("millivolt", dc.UNKNOWN_UNIT), ("m V", dc.UNKNOWN_UNIT), ("µV", dc.UNKNOWN_UNIT),
    ("°C", dc.UNIT_NOT_ADMITTED), ("K", dc.UNIT_NOT_ADMITTED), ("W", dc.UNIT_NOT_ADMITTED),
])
def test_units_are_exact_with_no_alias_or_conversion(unit, reason):
    result = dc.execute(BINDING, _request(unit=unit))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, reason, None)


def test_celsius_tokens_have_no_alias_and_belong_to_tmp36_only():
    data = dc.load_artifact()
    tokens = {u["unit_token"] for u in data["unit_records"]}
    for alias in ("C", "degC", "℃", "deg C", "°c", "K"):
        assert alias == "K" or alias not in tokens
    for record in data["methods"]:
        kinds = {r["quantity_kind"] for r in record["input_roles"] + record["output_roles"]}
        if record["method_id"] in ("electrical:dc_resistive_load_current",
                                   "electrical:dc_resistive_load_power",
                                   "electrical:dc_resistive_load_energy"):
            # Correction 06 (§13E): the DC load voltage, in its own exact V token
            assert "celsius_temperature" not in kinds
        elif record["method_id"] != method.METHOD_ID:
            assert not kinds & {"voltage", "celsius_temperature"}, record["method_id"]


def test_each_binding_executes_only_its_own_method():
    for binding in OTHER_BINDINGS:
        assert dc.execute(binding, _request())["reason"] == dc.OPERATION_NOT_ADMITTED
    swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, therm_method.evaluate)
    assert _failure(dc.execute(swapped, _request()))
    assert dc.execute(dc.bind_method(method.METHOD_ID, "2.0", method.evaluate),
                      _request())["reason"] == dc.VERSION_MISMATCH


def test_app_wires_one_immutable_binding_per_method():
    assert webapp._TMP36_TEMPERATURE_BINDING.adapter_identity \
        == "engine.tmp36_nominal_temperature_method.evaluate"
    with pytest.raises(AttributeError):
        webapp._TMP36_TEMPERATURE_BINDING.method_id = "x"
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 9
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("tmp36_nominal_temperature", "tmp36_content_config", "import fractions",
                   "decimal", "sqlite", "273.15", "open(target, \"w"):
        assert banned not in owner_source.lower(), banned


def _owner_tamper(data, name):
    record = _record(data)
    if name == "second_voltage_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "mV"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U099", "kV"
        data["unit_records"].append(extra)
    elif name == "celsius_alias":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "°C"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U098", "degC"
        data["unit_records"].append(extra)
    elif name == "drop_celsius":
        data["unit_records"] = [u for u in data["unit_records"] if u["unit_token"] != "°C"]
    elif name == "drop_kind":
        data["quantity_kinds"] = [k for k in data["quantity_kinds"]
                                  if k["quantity_kind"] != "voltage"]
    elif name == "sixth_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "tmp37:nominal_voltage_to_temperature"
        data["methods"].append(extra)
    elif name == "unknown_condition":
        record["applicability"][0]["condition"] = "within_100_and_1750"
    elif name == "policy_unresolved":
        record["source_qualification"][0]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "output_kind":
        record["output_roles"][0]["quantity_kind"] = "temperature_difference"
    elif name == "basis":
        data["source_use_policies"][-1]["inspection_basis"] = "EXECUTOR"
    return data


@pytest.mark.parametrize("name", ["second_voltage_unit", "celsius_alias", "drop_celsius",
                                  "drop_kind", "sixth_method", "unknown_condition",
                                  "policy_unresolved", "output_kind", "basis"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(_owner_artifact(), name))
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    assert _failure(dc.execute(BINDING, _request(), artifact_path=path))


def test_owner_v4_records_are_unchanged_by_the_fifth_admission():
    data = dc.load_artifact()
    assert data["artifact_version"] == "9"
    units = {u["record_id"]: u["unit_token"] for u in data["unit_records"]}
    assert units == {"dcu:U001": "N", "dcu:U002": "mm", "dcu:U003": "W",
                     "dcu:U004": "K/W", "dcu:U005": "K", "dcu:U006": "N·mm",
                     "dcu:U007": "N·m", "dcu:U008": "rad/s",
                     "dcu:U009": "mV", "dcu:U010": "°C",
                     "dcu:U011": "V", "dcu:U012": "Ω", "dcu:U013": "A",
                     "dcu:U014": "J", "dcu:U015": "s"}
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "dcu:U006 only" in policies["dcu:SU006"]["inspected_content"]
    assert "dcu:U007, dcu:U008" in policies["dcu:SU007"]["inspected_content"]
    assert "dcu:U009 only" in policies["dcu:SU008"]["inspected_content"]
    assert "dcu:U010 only" in policies["dcu:SU009"]["inspected_content"]
    assert "ADI-S1 only" in policies["dcu:SU010"]["inspected_content"]
    assert [m["method_id"] for m in data["methods"]] == [
        "cap13:static_reactions_two_support",
        "therm01:conduction_temperature_difference_single_path",
        "cap13:planar_single_force_moment",
        "cap13:linear_speed_dependent_rotational_load",
        "tmp36:nominal_voltage_to_temperature",
        "electrical:dc_resistive_load_current",
        "electrical:dc_resistive_load_power",
        "electrical:dc_resistive_load_energy",
        "cap13:planar_required_force"]
    k_record = [u for u in data["unit_records"] if u["unit_token"] == "K"][0]
    assert "no Celsius scale" in k_record["inspected_content"]       # THERM-01 unchanged


# ==========================================================================
# 6. the method artifact and the consumer
# ==========================================================================
def test_method_artifact_loads_with_claim_level_provenance_and_ip_boundary():
    data = tmp36.load_artifact()
    by_id = {r["record_id"]: r for r in data["sources"]}
    source = by_id["ADI-S1"]
    assert source["url"] == DATASHEET and "Rev. H" in source["source_title"]
    content = source["inspected_content"]
    for phrase in ("Table 4", "printed page 8 of 19", "offset voltage 0.5 V",
                   "10 mV per degree Celsius", "750 mV", "Table 1",
                   "printed page 3 of 19", "-40 to +125 degrees Celsius",
                   "Output Voltage Range specification of 100 to 2000 mV",
                   "distinct from that Output Voltage Range specification",
                   "self-heating", "Rev. H", "(c)1996-2015 Analog Devices",
                   DATASHEET_SHA256, "No copy of the document enters the repository"):
        assert phrase in content, phrase
    assert "no data-sheet text" in source["paraphrase_only_limitation"]
    policy = by_id["tmp36:SU001"]
    for phrase in ("All rights reserved", "No reproduction right", "facts",
                   "were not inspected", "not a legal opinion"):
        assert phrase in policy["inspected_content"], phrase
    assert "endorse" in policy["no_endorsement_limitation"]
    assert "not claimed to print this solved form" in data["method"]["derivation"]


def test_no_copy_of_the_data_sheet_enters_the_repository():
    tracked = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts
               and p.suffix.lower() == ".pdf"]
    assert not [p for p in tracked if "tmp3" in p.name.lower()]


@pytest.mark.parametrize("mutate", [
    lambda d: d["declarations"][0].__setitem__("accepted_value", "any analog temperature sensor"),
    lambda d: d["declarations"][3].__setitem__("refusal", "NOT_DECLARED"),
    lambda d: d["numeric_domain"]["roles"][1].__setitem__("unit_token", "K"),
    lambda d: d["method"].__setitem__("executed_form", "t_celsius = (v_out - 500) / 10, accurate to 0.5 degrees"),
    lambda d: d["disclosure"].pop(),
    lambda d: d["screen_items"].pop(),
    lambda d: d["sources"][0].__setitem__("source_use_policy_ref", "cap13r:SU001"),
    lambda d: d["sources"][0].__setitem__("url", "https://example.com/copy.pdf"),
    lambda d: d.__setitem__("artifact_version", "2"),
])
def test_method_artifact_tamper_is_knowledge_unavailable(mutate, monkeypatch):
    data = _method_artifact()
    mutate(data)
    with pytest.raises(tmp36.Tmp36KnowledgeError):
        tmp36.validate_artifact(data)
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert tmp36.evaluate(_captured(), BINDING, artifact=data)["outcome"] \
        == tmp36.KNOWLEDGE_UNAVAILABLE and not calls


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(decl={"device_tmp36": ""}, screen={"food_safety": "yes"},
                     v_out="x")["outcome"] == tmp36.NOT_DECLARED
    assert _evaluate(screen={"food_safety": ""})["outcome"] == tmp36.NOT_DECLARED
    assert _evaluate(screen={"touch_skin_or_medical": "yes"},
                     decl={"nominal_only": "does_not_apply"},
                     v_out="x")["outcome"] == tmp36.ENGINEERING_REVIEW_REQUIRED
    for item in tmp36.SCREEN_ITEMS:
        assert _evaluate(screen={item: "yes"})["outcome"] \
            == tmp36.ENGINEERING_REVIEW_REQUIRED, item
    for decl in tmp36.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"}, v_out="x")["outcome"] \
            == tmp36.MODEL_NOT_SUPPORTED, decl
    assert _evaluate(v_out="x")["outcome"] == tmp36.INVALID_NUMERIC_INPUT
    assert _evaluate(v_out="2000")["outcome"] == tmp36.OUTSIDE_NOMINAL_MODEL_RANGE
    assert not calls


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, tmp36.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, tmp36.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, tmp36.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, tmp36.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, tmp36.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, tmp36.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, tmp36.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, tmp36.UNMAPPED_OWNER_OUTCOME),
    (dc.STATE_REFUSAL, dc.OPERATION_NOT_ADMITTED, tmp36.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome, monkeypatch):
    monkeypatch.setattr(dc, "execute", lambda *a, **k: {
        "state": state, "reason": reason, "outputs": None})
    result = _evaluate()
    assert (result["outcome"], result["owner_state"], result["owner_reason"]) \
        == (outcome, state, reason)
    assert result["result"] is None and result["display_value"] is None


@pytest.mark.parametrize("produced", [25.0000001, 24.99999, -25.0, 0.0, 25.0 + 2.0 ** -40,
                                      "25", None, float("nan")])
def test_decimal_reference_failure_fails_closed_with_no_number(produced, monkeypatch):
    real = dc.execute

    def tampered(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["t_celsius"]["value"] = produced
        return result
    monkeypatch.setattr(dc, "execute", tampered)
    result = _evaluate(v_out="750")
    assert result["outcome"] == tmp36.KNOWLEDGE_UNAVAILABLE
    assert result["owner_state"] == dc.STATE_SUCCESS          # preserved, not rewritten
    assert result["result"] is None and result["display_value"] is None


def test_zero_must_be_exact_zero_and_only_at_500(monkeypatch):
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: dict(
        real(b, r, artifact_path=artifact_path),
        outputs={"t_celsius": {"value": 2.0 ** -60, "unit": "°C",
                               "provenance": "CALCULATED"}}))
    assert _evaluate(v_out="500")["outcome"] == tmp36.KNOWLEDGE_UNAVAILABLE
    assert tmp36.agrees_with_reference(0.0, Fraction(0))
    assert not tmp36.agrees_with_reference(-0.0 + 1e-300, Fraction(0))
    assert not tmp36.agrees_with_reference(0.0, Fraction(1, 10000))


def test_consumer_sends_the_correctly_rounded_value_and_fixed_unit(monkeypatch):
    seen = []
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: (
        seen.append(copy.deepcopy(r)), real(b, r, artifact_path=artifact_path))[1])
    _evaluate(v_out="750.1")
    assert seen == [{"method_id": method.METHOD_ID, "method_version": "1.0",
                     "inputs": {"v_out": {"value": float("750.1"), "unit": "mV"}},
                     "subject_ref": None}]
    assert float(Fraction("750.1")) == float("750.1")


def test_format_reference_is_exact_and_never_rounds():
    assert tmp36.format_reference(Fraction(-40)) == "-40.0"
    assert tmp36.format_reference(Fraction(0)) == "0.0"
    assert tmp36.format_reference(Fraction(2501, 100)) == "25.01"
    assert tmp36.format_reference(Fraction(-1, 10000)) == "-0.0001"
    with pytest.raises(ValueError):
        tmp36.format_reference(Fraction(1, 100000))


def test_consumer_and_adapter_import_no_other_authority():
    import ast
    for module in (tmp36, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                names.add(node.module or "")
        for banned in ("cap13", "therm01", "record_store", "safety_signal", "requests",
                       "urllib", "openai", "web", "flask", "random", "time"):
            assert not any(banned == n or n.startswith(banned + ".") or banned in n
                           for n in names if n), (module.__name__, banned)


# ==========================================================================
# 7. EN / AR fidelity and the contracts
# ==========================================================================
def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_english_wording_equals_the_artifact():
    content = tmp36.load_artifact()
    assert ui_text.text("UI_TMP36_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"]
        assert ui_text.text("UI_TMP36_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."
    for entry in content["screen_items"]:
        value = entry["item"]
        assert ui_text.text("UI_TMP36_SCREEN_" + entry["item_id"].upper(), "en") \
            == value[0].upper() + value[1:]


def test_arabic_wording_equals_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    assert ui_text.text("UI_TMP36_DISCLOSURE", "ar").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$",
                           _contract_section("**A-2", "**A-3"), re.M))
    for decl, ref in tmp36.DECLARATIONS:
        assert ui_text.text("UI_TMP36_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    screen = dict(re.findall(r"^\| (\w+) \| (.+?) \|$",
                             _contract_section("**A-3", "**A-4"), re.M))
    for item in tmp36.SCREEN_ITEMS:
        assert ui_text.text("UI_TMP36_SCREEN_" + item.upper(), "ar") == screen[item], item
    s9 = _contract_section("## 9. Result", "## 9A.")
    assert [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)] \
        == tmp36.load_artifact()["disclosure"]


def test_every_key_has_both_languages_and_no_measurement_or_safety_claim():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_TMP36_[A-Z0-9_]+)": \{', source)
    assert len(keys) >= 35
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("the sensor is safe", "measured by inventorai", "accurate to", "guaranteed",
                  "certified", "has been validated", "recommended sensor",
                  "calibrated value", "inventorai measured", "inventorai read your"):
        assert claim not in english, claim
    for phrase in ("did not read, sample or measure", "nominal relation only",
                   "not the data sheet's output-voltage specification",
                   "not the precision of the sensor"):
        assert phrase in english, phrase


def test_correction_05_is_recorded_and_earlier_sections_unchanged():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 05" in body and "## 13D." in body
    section = _norm(body[body.index("## 13D."):body.index("## 14.")])
    for phrase in ("exactly five", "`voltage`", "`celsius_temperature`", "`mV`", "`°C`",
                   "content version `5`", "`1.4.0`", "NOT a generic owner policy",
                   "never converts it to or from `K`", "THERM-01 keeps its own",
                   "Condition vocabulary. Unchanged"):
        assert phrase in section, phrase
    assert "**Methods — exactly four:**" in body[body.index("## 13C."):body.index("## 13D.")]
    assert "No absolute `temperature` kind is admitted." in body      # §13A text kept


def test_method_contract_records_scope_provenance_and_exclusions():
    text = _norm(CONTRACT.read_text(encoding="utf-8"))
    for phrase in ("Rev. H", "Table 4", "printed page 8 of 19", "Table 1",
                   "printed page 3 of 19", "100 mV to 2000 mV", "NOT the data sheet's",
                   DATASHEET_SHA256, "©1996–2015 Analog Devices", "SOURCE-BLOCKED",
                   "D13 research stays paused", "`100 → −40`", "`1750 → 125`",
                   "1.3 × 2^-46", "smallest sound bridge"):
        assert phrase in text, phrase


# ==========================================================================
# 8. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_electronics_root_journey_and_reference_values(elec):
    c, _aid, sid = elec
    assert "data-tmp36-link" in _page(c, sid)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-tmp36-form" in body and "checked" not in body
    assert "data-tmp36-voltage-note" in body
    for text, expected in REFERENCE:
        body = c.post(URL % sid, data=_form(v_out=text)).get_data(as_text=True)
        assert _value(body) == "%d.0 °C" % expected, text
    body = c.post(URL % sid, data=_form(v_out="750.1")).get_data(as_text=True)
    assert _value(body) == "25.01 °C"
    assert "data-tmp36-nominal-note" in body and "UNVALIDATED" in body
    assert "NOT EVIDENCE" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_TMP36_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert "TMP35/TMP36/TMP37" in body and "Modelica.Units" in body and "NIST" in body
    assert '<bdi dir="ltr" data-tmp36-echo-value>750.1</bdi>' in body


@pytest.mark.parametrize("over,outcome", [
    ({"v_out": "2000"}, "OUTSIDE_NOMINAL_MODEL_RANGE"),
    ({"v_out": "99.999"}, "OUTSIDE_NOMINAL_MODEL_RANGE"),
    ({"v_out": "-5"}, "INVALID_NUMERIC_INPUT"),
    ({"v_out": ""}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"battery_or_storage_cell": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"device_tmp36": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"nominal_only": ""}}, "NOT_DECLARED"),
])
def test_non_success_shows_one_reason_and_no_number(elec, over, outcome):
    c, _aid, sid = elec
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert ui_text.text("UI_TMP36_OUTCOME_" + outcome, "en") in html.unescape(body)
    assert _value(body) is None and body.count("data-tmp36-outcome") == 1


def test_mechanical_root_is_unsupported(mech, monkeypatch):
    c, _aid, sid = mech
    assert "data-tmp36-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._tmp36, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-tmp36-scope-note" in body
        assert "data-tmp36-form" not in body and _value(body) is None
    assert not called


@pytest.mark.parametrize("focus", (MECH, ELEC))
def test_integrated_electronics_part_is_offered_with_attribution(focus):
    c, _ = _client_for("tmp36-part-%s@example.com" % focus)
    sid = _integrated(c, focus)
    eligible, part = webapp._calc_gate(sid, tmp36)
    assert eligible and part.domain == ELEC
    assert "data-tmp36-link" in _page(c, sid)
    body = c.post(URL % sid, data=_form(v_out="400")).get_data(as_text=True)
    assert _value(body) == "-10.0 °C"
    assert _part_line(body, "tmp36") == PARTS["elec_part_name"]


def test_corrupt_or_unreadable_composition_grants_nothing(monkeypatch):
    c, _ = _client_for("tmp36-corrupt@example.com")
    sid = _integrated(c, MECH)
    _corrupt("UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 1")
    calls = _owner_spy(monkeypatch)
    assert webapp._calc_gate(sid, tmp36) == (False, None)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) is None and "data-tmp36-form" not in body and not calls
    sid2 = _integrated(c, MECH)

    def broken(_sid):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", broken)
    assert webapp._calc_gate(sid2, tmp36) == (False, None)


def test_csrf_authorization_and_malformed_requests(elec):
    c, _aid, sid = elec
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("tmp36-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302 and "data-tmp36" not in r.get_data(as_text=True)
    for bad in (dict(_form(), unexpected="1"), dict(_form(), screen_food_safety="maybe"),
                dict(_form(), decl_device_tmp36="tmp37")):
        r = c.post(URL % sid, data=bad)
        assert r.status_code == 400 and _value(r.get_data(as_text=True)) is None
    from werkzeug.datastructures import MultiDict
    r = c.post(URL % sid, data=MultiDict(list(_form().items())
                                         + [(tmp36.VALUE_FIELD % "v_out", "750")]))
    assert r.status_code == 400
    body = c.post(URL % sid, data=_form(v_out="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body


@pytest.mark.parametrize("over", [{}, {"v_out": "2000"}, {"screen": {"food_safety": "yes"}}])
def test_nothing_is_persisted(elec, over):
    c, _aid, sid = elec
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_no_report_export_api_or_safety_surface():
    src = Path(webapp.__file__).read_text(encoding="utf-8")
    start = src.index("# Sensors C3 — TMP36 Nominal Voltage-to-Temperature")
    section = src[start:src.index("# 28-T4 — Single Vendor-Neutral Control-Cycle", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "_cap13", "load_project_subsystems", "request.args",
                   "cap09", "success_criteria"):
        assert banned not in section, banned
    assert section.count("_calc_gate(sid, _tmp36)") == 3
    assert [r.rule for r in webapp.app.url_map.iter_rules() if "tmp36" in r.rule] \
        == ["/session/<sid>/tmp36-temperature"] * 2
    for template in ("deliverable.html", "report.html", "success_criteria.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "tmp36" not in path.read_text(encoding="utf-8").lower()


def test_existing_four_calculations_are_unchanged(mech, elec):
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


def test_measurement_planning_page_is_unchanged(elec):
    c, _aid, sid = elec
    body = c.get("/session/%s/success-criteria" % sid).get_data(as_text=True)
    assert "tmp36" not in body.lower()


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_attribution_escaping_and_arabic_isolation(lang):
    c, _ = _client_for("tmp36-hostile-%s@example.com" % lang)
    sid = _integrated(c, MECH, elec_part_name=HOSTILE)
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form(v_out="499.999")).get_data(as_text=True)
    assert "<script>alert" not in body
    assert html.unescape(_part_line(body, "tmp36")) == HOSTILE
    assert '<bdi dir="ltr">-0.0001 °C</bdi>' in body
    if lang == "ar":
        assert 'dir="rtl"' in body
        isolated = re.findall(r'<bdi dir="ltr">([^<]*)</bdi>', body)
        for token in ("V_OUT", "mV", "°C", "TMP36", "UNVALIDATED", "NOT EVIDENCE", "ADC"):
            assert any(token in run for run in isolated), token
        assert any("T = (V_OUT − 500 mV) / (10 mV/°C)" == run for run in isolated)
        assert any(run.startswith("−40 °C") for run in isolated)
        stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
        for item in ui_text.text("UI_TMP36_DISCLOSURE", "ar").split("\n\n"):
            assert _norm(item) in _norm(stripped), item[:30]
