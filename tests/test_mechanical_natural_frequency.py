# -*- coding: utf-8 -*-
"""MECHANICAL-NATURAL-FREQUENCY-01 - Spring-Mass Natural Frequency, Slice 1 (directly owning tests).

The shared deterministic calculation / units owner (``engine/deterministic_calculation.py``)
after the bounded twelfth admission of calc/units Correction 12 (§13K); the ONE
method ``mechanical:spring_mass_natural_frequency`` 1.0
(``engine/mechanical_natural_frequency_method.py``) and its ONE consumer
(``engine/mechanical_natural_frequency.py`` + the request-local page).

The numerical tests use INDEPENDENT oracles that share nothing with the
implementation path: π computed here with Machin's formula in integer
arithmetic; the reference frequency computed here with the ``decimal`` module
at 80 significant digits from the exact binary input values; and the exact
identity ``(2 π f₀)² m = k`` checked with rational arithmetic. Acceptance is a
relative error of at most 2^-50 (the contract bound), with the observed
execution error well inside 4 × 2^-53. The remaining tests press on the method
contract (§§1-9A): the closed twelve-method inventory and the exact
N/m / kg / Hz bindings (a NEW ``frequency`` kind, never the ``angular_velocity``
kind); binding isolation; owner artifact v12 and method-artifact integrity; the
§7 pre-owner order and owner correspondence; the exact-decimal screening and the
12-digit rounded display; the Mechanical-root and declared-Mechanical-part gate
(malformed, stale and corrupt compositions fail closed); request integrity,
isolation and no persistence; the eleven existing methods unchanged; and EN / AR
fidelity. Synthetic data only.
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
from engine import mechanical_natural_frequency as nf
from engine import mechanical_natural_frequency_method as method
from engine import cap13_static_reactions_method as cap13_method
from engine import cap13_rotational_load_method as rotational_method
from engine import therm01_conduction_method as therm_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _corrupt, _owner_spy, _part_line, MECH, ELEC, PARTS, CTRL, HOSTILE)
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_cap13_planar_moment import _form as _moment_form
from tests.test_therm01_temperature_difference import _form as _therm_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "MECHANICAL_SPRING_MASS_NATURAL_FREQUENCY_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
URL = "/session/%s/natural-frequency"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
CAP13_BINDING = dc.bind_method(cap13_method.METHOD_ID, cap13_method.METHOD_VERSION,
                               cap13_method.evaluate)
THERM_BINDING = dc.bind_method(therm_method.METHOD_ID, therm_method.METHOD_VERSION,
                               therm_method.evaluate)
BOUND = Fraction(1, 2 ** 50)
OBSERVED_BOUND = Fraction(4, 2 ** 53)
TINY = 5e-324                         # 2^-1074, the smallest positive subnormal
SMALLEST_NORMAL = sys.float_info.min  # 2^-1022
# The canonical digest of every content-version-11 record (15 kinds, 17 units,
# 19 source-use records, 11 methods), which Correction 12 leaves unchanged.
V11_RECORDS_DIGEST = "15a2b2ce7d5e356c8369907bea7d3ea475f99150dc1dd1033a483f7f0b2d1123"
# The 1000 N/m on 2.5 kg example: sqrt(400) / (2π) = 20 / (2π) = 10 / π Hz.
EXAMPLE = "3.18309886184"


# --------------------------------------------------------------------------
# independent oracles
# --------------------------------------------------------------------------
def _machin_pi(digits):
    """π to ``digits`` decimals by Machin's formula, integer arithmetic only:
    π = 16 arctan(1/5) - 4 arctan(1/239)."""
    scale = 10 ** (digits + 10)

    def arctan_inverse(x):
        total, term, n, sign = 0, scale // x, 1, 1
        while term:
            total += sign * (term // n)
            term //= x * x
            n += 2
            sign = -sign
        return total
    return (16 * arctan_inverse(5) - 4 * arctan_inverse(239)) // 10 ** 10


PI_80 = _machin_pi(80)   # integer: π × 10^80, truncated


def _exact(value):
    numerator, denominator = float(value).as_integer_ratio()
    return Fraction(numerator, denominator)


def _oracle(k, m):
    """The reference frequency as a ``Fraction`` from the exact binary inputs,
    with the decimal module at 80 digits and the Machin π (an algorithm and a
    constant that share nothing with the adapter or the consumer)."""
    with localcontext() as context:
        context.prec = 80
        pi = Decimal(PI_80) / Decimal(10 ** 80)
        kk = Decimal(_exact(k).numerator) / Decimal(_exact(k).denominator)
        mm = Decimal(_exact(m).numerator) / Decimal(_exact(m).denominator)
        return Fraction((kk / mm).sqrt() / (2 * pi))


def _within(produced, k, m, bound=BOUND):
    reference = _oracle(k, m)
    return abs(_exact(produced) - reference) <= reference * bound


def _identity_holds(produced, k, m):
    """(2 π f₀)² m = k within the bound, with π bracketed rationally."""
    pi_low = Fraction(PI_80, 10 ** 80)
    pi_high = pi_low + Fraction(1, 10 ** 80)
    f = _exact(produced)
    low = (2 * pi_low * f) ** 2 * _exact(m)
    high = (2 * pi_high * f) ** 2 * _exact(m)
    return low * (1 - 3 * BOUND) <= _exact(k) <= high * (1 + 3 * BOUND)


def _request(k=1000.0, m=2.5, units=("N/m", "kg"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"k": {"value": k, "unit": units[0]},
                      "m": {"value": m, "unit": units[1]}},
           "subject_ref": None}
    req.update(over)
    return req


def _run(k, m):
    return dc.execute(BINDING, _request(k=k, m=m))


def _form(k="1000", m="2.5", decl=None, screen=None):
    form = {nf.DECLARATION_FIELD % d: nf.ANSWER_APPLIES for d in nf.DECLARATION_IDS}
    form.update({nf.SCREEN_FIELD % s: nf.SCREEN_NO for s in nf.SCREEN_ITEMS})
    form.update({nf.VALUE_FIELD % "k": k, nf.VALUE_FIELD % "m": m})
    for key, value in (decl or {}).items():
        form[nf.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[nf.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = nf.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return nf.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _method_artifact():
    return json.loads(nf.ARTIFACT_PATH.read_text(encoding="utf-8"))


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
    marker = 'data-mnf-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


@pytest.fixture
def mech():
    c, aid = _client_for("mnf-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": "mechanical"})


@pytest.fixture
def elec():
    c, aid = _client_for("mnf-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def elec_focus():
    c, _aid = _client_for("mnf-part-elec-focus@example.com")
    return c, _integrated(c, ELEC)


# ==========================================================================
# 1. numerical acceptance against independent oracles
# ==========================================================================
def test_pi_constants_are_verified_independently_of_the_implementation():
    digits = str(PI_80)
    assert digits[:51] == method.PI_50_DECIMALS.replace(".", "")
    assert digits[:61] == nf.PI_60_DECIMALS.replace(".", "")
    assert digits[51:53] == "58" and digits[61:63] == "59"   # both are truncations
    assert method.PI_LOW < Fraction(PI_80, 10 ** 80) < method.PI_HIGH
    assert float(method.PI_LOW) == math.pi
    assert method.TWO_PI == 2.0 * math.pi and _exact(method.TWO_PI) == 2 * _exact(math.pi)
    assert Fraction(1, 2 ** 53) > abs(_exact(math.pi) - Fraction(PI_80, 10 ** 80)) / Fraction(PI_80, 10 ** 80)


@pytest.mark.parametrize("k,m", [
    (1000.0, 2.5), (4.0, 1.0), (1.0, 1.0), (0.1, 0.2), (3.0, 1.0 / 3.0),
    (1e-3, 1e3), (1e12, 1e-9), (123456789012.123456789, 0.000000001),
    (2.0, 7.0), (9.81, 0.5), (1e21, 1.0), (1.0, 1e21),
])
def test_normal_and_boundary_values_meet_the_bound(k, m):
    result = _run(k, m)
    assert result["state"] == dc.STATE_SUCCESS, result
    produced = result["outputs"]["f0"]["value"]
    assert isinstance(produced, float) and produced > 0.0
    assert _within(produced, k, m, OBSERVED_BOUND)
    assert _identity_holds(produced, k, m)
    assert produced == method.evaluate(k, m)["f0"]
    assert produced == math.sqrt(k / m) / (2.0 * math.pi)


def test_example_values_and_the_rational_check():
    assert method.evaluate(1000.0, 2.5)["f0"] == 10.0 / math.pi
    assert method.evaluate(4.0, 1.0)["f0"] == 1.0 / math.pi
    low, high = method.frequency_bounds(Fraction(1000), Fraction(5, 2))
    assert low < Fraction(10) / Fraction(PI_80, 10 ** 80) < high
    assert (high - low) / low < Fraction(1, 10 ** 40)
    s_low, s_high = method.sqrt_bounds(Fraction(2))
    assert s_low ** 2 <= 2 <= s_high ** 2 and (s_high - s_low) < Fraction(1, 10 ** 39)


def test_random_values_are_within_the_bound_and_the_identity():
    rng = random.Random(20261029)
    for _ in range(300):
        k = rng.uniform(1e-9, 1e12) * 10.0 ** rng.randint(-9, 9)
        m = rng.uniform(1e-9, 1e12) * 10.0 ** rng.randint(-9, 9)
        produced = method.evaluate(k, m)["f0"]
        assert _within(produced, k, m, OBSERVED_BOUND), (k, m)
        assert _identity_holds(produced, k, m), (k, m)


def test_overflow_of_the_ratio_is_an_integrity_failure_with_no_payload():
    with pytest.raises(ArithmeticError):
        method.evaluate(1.0, TINY)
    with pytest.raises(ArithmeticError):
        method.evaluate(sys.float_info.max, 1e-10)
    assert _failure(_run(1.0, TINY))
    assert _failure(_run(sys.float_info.max, 1e-10))


def test_underflow_of_the_ratio_to_zero_is_an_integrity_failure_not_a_refusal():
    with pytest.raises(ArithmeticError):
        method.evaluate(TINY, 1e10)
    result = _run(TINY, 1e10)
    assert _failure(result)


def test_subnormal_ratio_is_accepted_only_within_the_bound():
    # an exactly representable subnormal ratio: TINY / 1.0 = TINY exactly
    produced = method.evaluate(TINY, 1.0)["f0"]
    assert _within(produced, TINY, 1.0)
    # a subnormal ratio whose rounding error is large fails closed
    with pytest.raises(ArithmeticError):
        method.evaluate(3.0 * TINY, 7.0)


def test_zero_input_is_refused_before_execution_unlike_underflow():
    # the owner's applicability conditions refuse a zero or negative input
    # before the adapter runs; the adapter itself would raise for them, so a
    # refusal (never an integrity failure) proves it was not invoked
    for k, m in ((0.0, 2.5), (1000.0, 0.0), (-1000.0, 2.5), (1000.0, -2.5)):
        result = dc.execute(BINDING, _request(k=k, m=m))
        assert (result["state"], result["reason"], result["outputs"]) == (
            dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None), (k, m)
        with pytest.raises(ArithmeticError):
            method.evaluate(k, m)


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"),
                                   "1000", True, None, [1000.0]])
def test_non_finite_and_non_numeric_inputs_are_refused(value):
    assert _run(value, 2.5)["reason"] == dc.INVALID_NUMERIC_INPUT
    assert _run(1000.0, value)["reason"] == dc.INVALID_NUMERIC_INPUT


def test_adapter_refuses_non_float_or_non_finite_arguments():
    for k, m in ((1000, 2.5), (1000.0, "2.5"), (float("nan"), 2.5),
                 (1000.0, float("inf")), (0.0, 2.5), (1000.0, -2.5)):
        with pytest.raises(ArithmeticError):
            method.evaluate(k, m)
    with pytest.raises(ArithmeticError):
        method.sqrt_bounds(Fraction(0))
    with pytest.raises(ArithmeticError):
        method.frequency_bounds(Fraction(1), Fraction(-1))


# ==========================================================================
# 2. the shared owner after Correction 12: packaging, inventory, isolation
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = dc.execute(BINDING, _request(subject_ref="opaque"))
    assert result["state"] == dc.STATE_SUCCESS and result["reason"] is None
    assert result["outputs"] == {"f0": {"value": 10.0 / math.pi, "unit": "Hz",
                                        "provenance": "CALCULATED"}}
    assert result["inputs"]["k"] == {"value": 1000.0, "unit": "N/m",
                                     "provenance": "OWNER_STATED"}
    assert result["inputs"]["m"] == {"value": 2.5, "unit": "kg",
                                     "provenance": "OWNER_STATED"}
    assert (result["method_id"], result["method_version"]) == (
        "mechanical:spring_mass_natural_frequency", "1.0")
    assert (result["artifact_version"], result["implementation_version"]) == ("13", "1.12.0")
    assert [u["record_id"] for u in result["unit_records"]] == [
        "dcu:U018", "dcu:U019", "dcu:U020"]
    assert [q["source_ref"] for q in result["source_qualification"]] == [
        "NBS-NF-S1", "NIST-NF-U"]
    assert [q["source_use_policy_ref"] for q in result["source_qualification"]] \
        == ["dcu:SU020", "dcu:SU021"]
    assert result["subject_ref"] == "opaque"
    assert re.fullmatch(r"[0-9a-f]{64}", result["result_identity"])
    assert result == dc.execute(BINDING, _request(subject_ref="opaque"))


def test_closed_inventory_and_versions():
    assert ("mechanical:spring_mass_natural_frequency", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 13
    assert {"mass", "stiffness", "frequency"} <= dc.ADMITTED_QUANTITY_KINDS
    assert len(dc.ADMITTED_QUANTITY_KINDS) == 19   # Correction 13 later added one kind
    assert {"kg", "N/m", "Hz", "1/K"} <= dc.ADMITTED_UNIT_TOKENS
    assert len(dc.ADMITTED_UNIT_TOKENS) == 21      # and its one token 1/K
    # no alias, no conversion token and no second rad/s meaning
    assert not any(t in dc.ADMITTED_UNIT_TOKENS
                   for t in ("g", "t", "lb", "N/mm", "kN/m", "lbf/in", "rpm", "kHz", "1/s"))
    assert dc.KIND_TOKEN_EXCEPTIONS == {"voltage": frozenset({"mV", "V"}),
                                        "time": frozenset({"s", "h"})}
    assert dc.IMPLEMENTATION_VERSION == "1.12.0"
    data = dc.load_artifact()
    assert data["artifact_version"] == "13"
    kinds = {k["quantity_kind"]: k["dimension"] for k in data["quantity_kinds"]}
    assert (kinds["mass"], kinds["stiffness"], kinds["frequency"]) == ("M", "M T^-2", "T^-1")
    record = _record(data)
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"]] == [("k", "stiffness", "N/m"),
                                                ("m", "mass", "kg")]
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["output_roles"]] == [("f0", "frequency", "Hz")]
    assert record["applicability"] == [
        {"role": "k", "condition": "greater_than_zero", "bound_role": None},
        {"role": "m", "condition": "greater_than_zero", "bound_role": None}]
    assert record["result_range"] == [
        {"role": "f0", "condition": "greater_than_zero", "bound_role": None}]
    assert record["adapter_identity"] == "engine.mechanical_natural_frequency_method.evaluate"
    assert record["method_authority_artifact"] == {
        "artifact_id": nf.ARTIFACT_ID, "artifact_version": "1"}
    units = {u["unit_token"]: u for u in data["unit_records"]}
    assert [units[t]["record_id"] for t in ("kg", "N/m", "Hz")] == [
        "dcu:U018", "dcu:U019", "dcu:U020"]
    assert all(units[t]["source_use_policy_ref"] == "dcu:SU021" for t in ("kg", "N/m", "Hz"))
    assert all("Special Publication 330" in units[t]["source_title"] for t in ("kg", "N/m", "Hz"))
    assert "bounded quantity usage" in units["N/m"]["inspected_content"]
    assert "distinct from the angular_velocity kind" in units["Hz"]["inspected_content"]
    assert "no conversion" in units["Hz"]["inspected_content"]
    # the rotational load keeps its own rad/s record: angular velocity is not frequency
    assert units["rad/s"]["quantity_kind"] == "angular_velocity"
    assert units["rad/s"]["record_id"] == "dcu:U008"
    assert units["Hz"]["quantity_kind"] == "frequency"


def test_units_are_exact_with_no_alias_or_conversion():
    for unit in ("N/mm", "kN/m", "n/m", "N m^-1", "N/M", "lbf/in", "N·m"):
        result = dc.execute(BINDING, _request(units=(unit, "kg")))
        assert result["reason"] in (dc.UNKNOWN_UNIT, dc.UNIT_NOT_ADMITTED), unit
    for unit in ("g", "t", "lb", "KG", "kilogram"):
        result = dc.execute(BINDING, _request(units=("N/m", unit)))
        assert result["reason"] == dc.UNKNOWN_UNIT, unit
    # admitted tokens of other kinds are still never accepted for these roles
    for units in (("N", "kg"), ("N/m", "N"), ("Hz", "kg"), ("N/m", "rad/s"), ("kg", "N/m")):
        assert dc.execute(BINDING, _request(units=units))["reason"] \
            == dc.UNIT_NOT_ADMITTED, units


def test_method_version_and_adapter_integrity_fail_closed():
    assert dc.execute(BINDING, _request(method_version="1.1"))["reason"] \
        == dc.VERSION_MISMATCH
    stale = dc.bind_method(method.METHOD_ID, "0.9", method.evaluate)
    assert dc.execute(stale, _request())["reason"] == dc.VERSION_MISMATCH
    for adapter in (cap13_method.evaluate, rotational_method.evaluate,
                    lambda k, m: {"f0": math.sqrt(k / m) / (2 * math.pi)}):
        swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, adapter)
        assert _failure(dc.execute(swapped, _request()))
    req = _request()
    del req["inputs"]["m"]
    assert dc.execute(BINDING, req)["reason"] == dc.INPUT_MISSING
    req = _request()
    req["inputs"]["c"] = {"value": 1.0, "unit": "kg"}
    assert dc.execute(BINDING, req)["reason"] == dc.OPERATION_NOT_ADMITTED
    unknown = dc.bind_method("mechanical:damped_natural_frequency", "1.0", method.evaluate)
    assert dc.execute(unknown, _request(method_id="mechanical:damped_natural_frequency")
                      )["reason"] == dc.METHOD_NOT_REGISTERED


def test_bindings_are_isolated_and_existing_methods_unchanged():
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
    rot = dc.bind_method(rotational_method.METHOD_ID, rotational_method.METHOD_VERSION,
                         rotational_method.evaluate)
    rot_req = {"method_id": rotational_method.METHOD_ID, "method_version": "1.0",
               "inputs": {"tau_nominal": {"value": -2.0, "unit": "N·m"},
                          "w_nominal": {"value": 100.0, "unit": "rad/s"},
                          "w": {"value": 50.0, "unit": "rad/s"}},
               "subject_ref": None}
    assert dc.execute(rot, rot_req)["outputs"]["tau"]["value"] == -1.0


def test_app_wires_one_immutable_binding():
    assert webapp._MNF_BINDING.adapter_identity \
        == "engine.mechanical_natural_frequency_method.evaluate"
    assert webapp._MNF_BINDING.method_id == method.METHOD_ID
    with pytest.raises(AttributeError):
        webapp._MNF_BINDING.method_id = "x"
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    assert app_source.count("_dcalc.bind_method(") == 13
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("mechanical_natural_frequency", "mechanical_content_config",
                   "math.sqrt", "math.pi", "isqrt"):
        assert banned not in owner_source, banned


# ==========================================================================
# 3. owner artifact v12 and the method artifact: integrity and tamper
# ==========================================================================
def _owner_tamper(data, name):
    record = _record(data)
    if name == "second_frequency_unit":
        extra = copy.deepcopy([u for u in data["unit_records"] if u["unit_token"] == "Hz"][0])
        extra["record_id"], extra["unit_token"] = "dcu:U021", "rad/s"
        data["unit_records"].append(extra)
    elif name == "rad_s_rebound_to_frequency":
        [u for u in data["unit_records"] if u["unit_token"] == "rad/s"][0]["quantity_kind"] = "frequency"
    elif name == "drop_frequency_unit":
        data["unit_records"] = [u for u in data["unit_records"] if u["unit_token"] != "Hz"]
    elif name == "drop_stiffness_kind":
        data["quantity_kinds"] = [k for k in data["quantity_kinds"]
                                  if k["quantity_kind"] != "stiffness"]
    elif name == "extra_kind":
        data["quantity_kinds"].append({"quantity_kind": "angular_frequency", "dimension": "T^-1"})
    elif name == "drop_method":
        data["methods"].remove(record)
    elif name == "extra_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "mechanical:damped_natural_frequency"
        data["methods"].append(extra)
    elif name == "output_unit":
        record["output_roles"][0]["unit_token"] = "rad/s"
    elif name == "output_kind":
        record["output_roles"][0]["quantity_kind"] = "angular_velocity"
    elif name == "policy_unresolved":
        record["source_qualification"][0]["source_use_policy_ref"] = "dcu:SU999"
    elif name == "basis":
        record["source_qualification"][1]["inspection_basis"] = "EXECUTOR"
    elif name == "adapter":
        record["adapter_identity"] = "engine.cap13_planar_moment_method.evaluate"
    return data


@pytest.mark.parametrize("name", [
    "second_frequency_unit", "rad_s_rebound_to_frequency", "drop_frequency_unit",
    "drop_stiffness_kind", "extra_kind", "drop_method", "extra_method", "output_unit",
    "output_kind", "policy_unresolved", "basis", "adapter"])
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


def test_owner_v11_records_are_unchanged_by_the_twelfth_admission():
    data = dc.load_artifact()
    assert data["artifact_version"] == "13"
    v11 = {"quantity_kinds": data["quantity_kinds"][:15],
           "unit_records": data["unit_records"][:17],
           "source_use_policies": data["source_use_policies"][:19],
           "methods": data["methods"][:11]}
    canonical = json.dumps(v11, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(canonical.encode()).hexdigest() == V11_RECORDS_DIGEST
    assert [k["quantity_kind"] for k in data["quantity_kinds"][15:18]] == [
        "mass", "stiffness", "frequency"]
    assert [u["record_id"] for u in data["unit_records"][17:20]] == [
        "dcu:U018", "dcu:U019", "dcu:U020"]
    assert [p["record_id"] for p in data["source_use_policies"][19:21]] == [
        "dcu:SU020", "dcu:SU021"]
    assert [m["method_id"] for m in data["methods"][11:12]] == [method.METHOD_ID]
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert "mnf:SU001" in policies["dcu:SU020"]["inspected_content"]
    assert "NBS-NF-S1" in policies["dcu:SU020"]["inspected_content"]
    assert "Technical Note 487" in policies["dcu:SU020"]["inspected_content"]
    assert "IP-UNRESOLVED" in policies["dcu:SU020"]["inspected_content"]
    assert "dcu:U018 (kg), dcu:U019 (N/m) and dcu:U020 (Hz) only" \
        in policies["dcu:SU021"]["inspected_content"]
    assert all(p["inspection_basis"] == "LEAD_SUPPLIED" for p in data["source_use_policies"])
    assert "Content version 13 admits exactly thirteen methods" in data["governance_note"]
    text = json.dumps(data, ensure_ascii=False)
    for banned in ("damping ratio", "transmissibility", "resonant amplitude"):
        assert banned not in text, banned
    # the IP-unresolved basis is named only to say it is NOT relied upon
    assert text.count("SP 615") == 1 and text.count("SRC-045") == 1
    assert "SRC-045 / NBS SP 615 basis is IP-UNRESOLVED and is NOT relied upon" \
        in policies["dcu:SU020"]["inspected_content"]


def test_method_artifact_loads_and_binds_its_sources():
    data = nf.load_artifact()
    assert data["method"]["method_id"] == method.METHOD_ID
    assert "2.0 * math.pi" in data["method"]["executed_form"]
    assert "2^-50" in data["method"]["executed_form"]
    assert [d["declaration_id"] for d in data["declarations"]] == list(nf.DECLARATION_IDS)
    assert len(data["declarations"]) == 7
    assert [i["item_id"] for i in data["screen_items"]] == list(nf.SCREEN_ITEMS)
    by_id = {r["record_id"]: r for r in data["sources"]}
    assert by_id["NBS-NF-S1"]["source_use_policy_ref"] == "mnf:SU001"
    assert by_id["NIST-NF-U"]["source_use_policy_ref"] == "mnf:SU002"
    assert "Newman" in by_id["NBS-NF-S1"]["source_title"]
    assert "July 1969" in by_id["NBS-NF-S1"]["source_title"]
    assert "relatively very large mass" in by_id["NBS-NF-S1"]["inspected_content"]
    assert "IP-UNRESOLVED" in by_id["mnf:SU001"]["inspected_content"]
    assert all(r["inspection_basis"] == "LEAD_SUPPLIED" for r in data["sources"])
    assert len(data["disclosure"]) == 7
    from engine import cap13_planar_moment as moment
    assert nf.SCREEN_ITEMS == moment.SCREEN_ITEMS
    text = json.dumps(data, ensure_ascii=False)
    for banned in ("90°", "maximum amplitude", "percent of", "per cent"):
        assert banned not in text, banned
    assert text.count("SP 615") == 1 and text.count("SRC-045") == 1
    assert "IP-UNRESOLVED and is NOT relied upon" in by_id["mnf:SU001"]["inspected_content"]


@pytest.mark.parametrize("mutate", [
    lambda d: d["declarations"][5].__setitem__(
        "accepted_value", "damping is modelled as a viscous damper"),
    lambda d: d["declarations"][0].__setitem__("refusal", "NOT_DECLARED"),
    lambda d: d["numeric_domain"]["roles"][2].__setitem__("unit_token", "rad/s"),
    lambda d: d["numeric_domain"]["roles"][2].__setitem__("quantity_kind", "angular_velocity"),
    lambda d: d["disclosure"].pop(),
    lambda d: d["limitations"].__setitem__(0, "Resonance is checked."),
    lambda d: d["sources"][0].__setitem__("source_use_policy_ref", "cap13m:SU001"),
    lambda d: d["method"].__setitem__("executed_form", "f0 = sqrt(k / m)"),
    lambda d: d.__setitem__("artifact_version", "2"),
    lambda d: d["screen_items"].pop(),
    lambda d: d["declarations"].pop(),
])
def test_method_artifact_tamper_is_knowledge_unavailable(tmp_path, mutate, monkeypatch):
    data = _method_artifact()
    mutate(data)
    with pytest.raises(nf.NaturalFrequencyKnowledgeError):
        nf.validate_artifact(data)
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    result = nf.evaluate(_captured(), BINDING, artifact=data)
    assert result["outcome"] == nf.KNOWLEDGE_UNAVAILABLE and not calls
    assert result["display_value"] is None


# ==========================================================================
# 4. the consumer: capture, the §7 order, the decimal reference, the display
# ==========================================================================
def test_consumer_success_carries_the_owner_result_and_a_rounded_display():
    result = _evaluate()
    assert result["outcome"] == nf.OUTCOME_SUCCESS
    assert result["owner_state"] == dc.STATE_SUCCESS
    assert result["result"]["outputs"]["f0"]["value"] == 10.0 / math.pi
    assert result["display_value"] == EXAMPLE
    assert isinstance(result["frequency"], Fraction)
    assert "exact" not in result


def test_reference_frequency_matches_the_independent_oracle():
    for k, m in ((Fraction(1000), Fraction(5, 2)), (Fraction(1), Fraction(1)),
                 (Fraction("0.000000001"), Fraction("123456789012.123456789")),
                 (Fraction("123456789012"), Fraction("0.000000001"))):
        reference = nf.reference_frequency(k, m)
        oracle = _oracle(float(k), float(m)) if (float(k) == k and float(m) == m) else None
        if oracle is not None:
            assert abs(reference - oracle) <= oracle * Fraction(1, 10 ** 55)
        # the identity (2π f)² m = k holds to the reference precision
        pi = Fraction(PI_80, 10 ** 80)
        assert abs((2 * pi * reference) ** 2 * m - k) <= k * Fraction(1, 10 ** 55)
    with pytest.raises(ValueError):
        nf.reference_frequency(Fraction(0), Fraction(1))


@pytest.mark.parametrize("value,text", [
    (Fraction(10) / Fraction(PI_80, 10 ** 80), EXAMPLE),
    (Fraction(1), "1"),
    (Fraction(123456789012345), "1.23456789012 × 10^14"),
    (Fraction(999999999999999), "1 × 10^15"),
    (Fraction(1, 10 ** 7), "1 × 10^-7"),
    (Fraction("0.000001"), "0.000001"),
    (Fraction("123456789012.4"), "123456789012"),
    (Fraction("123456789013.6"), "123456789014"),
    (Fraction("1234567890125") + Fraction(1, 10 ** 30), "1.23456789013 × 10^12"),
    (Fraction("2.5"), "2.5"),
])
def test_display_rounds_once_to_twelve_significant_digits(value, text):
    assert nf.format_frequency(value) == text


def test_display_fails_closed_at_a_rounding_boundary():
    # exactly halfway between two 12-digit values: the guard widening changes the digits
    assert nf.format_frequency(Fraction("1.000000000005")) is None
    assert nf.format_frequency(Fraction("1.000000000005") + Fraction(1, 10 ** 40)) \
        == "1.00000000001"
    with pytest.raises(TypeError):
        nf.format_frequency(1.5)
    with pytest.raises(TypeError):
        nf.format_frequency(Fraction(0))


def test_agrees_with_reference_is_strict():
    reference = nf.reference_frequency(Fraction(1000), Fraction(5, 2))
    assert nf.agrees_with_reference(10.0 / math.pi, reference)
    assert not nf.agrees_with_reference(10.0 / math.pi * (1 + 2 ** -40), reference)
    assert not nf.agrees_with_reference(-10.0 / math.pi, reference)
    assert not nf.agrees_with_reference(float("nan"), reference)
    assert not nf.agrees_with_reference(10.0 / math.pi, Fraction(0))
    assert not nf.agrees_with_reference("3.18", reference)


def test_owner_result_in_another_unit_or_off_reference_is_knowledge_unavailable(monkeypatch):
    real = dc.execute

    def tampered(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["f0"]["unit"] = "rad/s"
        return result
    monkeypatch.setattr(dc, "execute", tampered)
    assert _evaluate()["outcome"] == nf.KNOWLEDGE_UNAVAILABLE

    def shifted(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["f0"]["value"] *= 1 + 2 ** -45
        return result
    monkeypatch.setattr(dc, "execute", shifted)
    result = _evaluate()
    assert result["outcome"] == nf.KNOWLEDGE_UNAVAILABLE
    assert result["owner_state"] == dc.STATE_SUCCESS and result["display_value"] is None


def test_guarded_display_failure_is_knowledge_unavailable(monkeypatch):
    monkeypatch.setattr(nf, "format_frequency", lambda reference: None)
    result = _evaluate()
    assert result["outcome"] == nf.KNOWLEDGE_UNAVAILABLE and result["result"] is None


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(decl={"single_mass": ""}, screen={"pressure": "yes"},
                     k="abc")["outcome"] == nf.NOT_DECLARED
    assert _evaluate(screen={"pressure": ""})["outcome"] == nf.NOT_DECLARED
    assert _evaluate(screen={"children": "yes"}, decl={"rigid_support": "does_not_apply"},
                     k="0")["outcome"] == nf.ENGINEERING_REVIEW_REQUIRED
    for decl in nf.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"}, k="x")["outcome"] \
            == nf.MODEL_NOT_SUPPORTED, decl
    assert not calls


@pytest.mark.parametrize("text", [
    "", "-1", "+1", "1e3", "1E3", "1,5", "1_0", " 1", "1 ", ".5", "5.", "0x10",
    "inf", "nan", "١٢", "12N", "0", "0.0", "0.000000000", "1234567890123",
    "1.0000000001", "1." + "0" * 9 + "1", "9" * 13])
def test_numeric_grammar_representation_limits_and_zero_are_invalid(text, monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    assert _evaluate(k=text)["outcome"] == nf.INVALID_NUMERIC_INPUT, text
    assert _evaluate(m=text)["outcome"] == nf.INVALID_NUMERIC_INPUT, text
    assert not calls


def test_numeric_grammar_accepts_exact_decimals_within_the_limits():
    assert nf.parse_value("2.5") == Fraction(5, 2)
    assert nf.parse_value("0.000000001") == Fraction(1, 10 ** 9)
    assert nf.parse_value("123456789012.123456789") == Fraction("123456789012.123456789")
    assert nf.parse_value("0") == 0
    assert nf.parse_value("1234567890123") is None
    assert nf.parse_value("1.0000000001") is None
    assert nf.parse_value(2.5) is None
    assert _evaluate(k="123456789012.123456789", m="0.000000001")["outcome"] \
        == nf.OUTCOME_SUCCESS
    assert _evaluate(k="0.000000001", m="123456789012.123456789")["outcome"] \
        == nf.OUTCOME_SUCCESS


@pytest.mark.parametrize("form", [
    {"unexpected": ["1"]},
    {nf.VALUE_FIELD % "k": ["1", "2"]},
    {nf.DECLARATION_FIELD % "single_mass": ["yes"]},
    {nf.SCREEN_FIELD % "children": ["maybe"]},
    {nf.VALUE_FIELD % "m": [2.5]},
    {"value_f0": ["3"]},
])
def test_malformed_capture_is_none(form):
    base = {k: [v] for k, v in _form().items()}
    base.update(form)
    assert nf.capture_form(base) is None
    assert nf.capture_form("not a mapping") is None


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, nf.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, nf.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, nf.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, nf.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, nf.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, nf.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, nf.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, nf.UNMAPPED_OWNER_OUTCOME),
    (dc.STATE_REFUSAL, dc.OPERATION_NOT_ADMITTED, nf.UNMAPPED_OWNER_OUTCOME),
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
    result = nf.evaluate(_captured(), BINDING, owner_artifact_path=path)
    assert result["outcome"] == nf.KNOWLEDGE_UNAVAILABLE
    assert result["owner_state"] == dc.STATE_FAILURE


def test_consumer_typed_values_and_fixed_units_reach_the_owner(monkeypatch):
    seen = []
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: (
        seen.append(copy.deepcopy(r)), real(b, r, artifact_path=artifact_path))[1])
    _evaluate(k="2.5", m="4")
    assert seen == [{"method_id": method.METHOD_ID, "method_version": "1.0",
                     "inputs": {"k": {"value": 2.5, "unit": "N/m"},
                                "m": {"value": 4.0, "unit": "kg"}},
                     "subject_ref": None}]


def test_consumer_and_adapter_import_no_other_method_authority():
    import ast
    for module in (nf, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module or "")
                imports.update("%s.%s" % (node.module, a.name) for a in node.names)
        for banned in ("cap13", "therm01", "tmp36", "dc_resistive", "pwm", "control_cycle",
                       "record_store", "safety_signal", "idea_state", "requests",
                       "urllib", "openai", "numpy", "scipy", "mpmath"):
            assert not any(banned in name for name in imports), (module, banned)
    adapter_source = Path(method.__file__).read_text(encoding="utf-8")
    assert "deterministic_calculation" not in adapter_source


# ==========================================================================
# 5. EN / AR fidelity and the governing documents
# ==========================================================================
def test_english_wording_equals_the_artifact():
    content = nf.load_artifact()
    assert ui_text.text("UI_MNF_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"]
        assert ui_text.text("UI_MNF_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."
    for entry in content["screen_items"]:
        assert ui_text.text("UI_CAP13_SCREEN_" + entry["item_id"].upper(), "en") \
            == entry["item"][0].upper() + entry["item"][1:]


def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_arabic_and_english_wording_equal_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    items = [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    assert ui_text.text("UI_MNF_DISCLOSURE", "ar").split("\n\n") == items
    a2 = _contract_section("**A-2", "**A-3")
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$", a2, re.M))
    for decl, ref in zip(nf.DECLARATION_IDS, ("D-1", "D-2", "D-3", "D-4", "D-5", "D-6", "D-7")):
        assert ui_text.text("UI_MNF_DECL_" + decl.upper(), "ar") \
            == rows["%s %s" % (ref, decl)], decl
    s9 = _contract_section("## 9. Result", "## 9A.")
    english = [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)]
    assert english == nf.load_artifact()["disclosure"]
    s5 = _contract_section("## 5. Applicability", "## 6.")
    for entry in nf.load_artifact()["declarations"]:
        assert "| %s | `%s` | %s |" % (entry["contract_ref"], entry["declaration_id"],
                                       entry["accepted_value"]) in s5


def test_every_key_has_both_languages_and_no_overclaim():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_MNF_[A-Z0-9_]+)": \{', source)
    assert len(keys) >= 34
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("is a safe frequency", "this frequency is safe", "you should avoid", "is adequate", "approved",
                  "acceptable margin", "will resonate", "resonance occurs at",
                  "has been validated", "verified design", "certified", "will not fail",
                  " damped natural frequency", "damping ratio"):
        assert claim not in english, claim
    next_step = ui_text.text("UI_MNF_NEXT_STEP", "en")
    assert "measurement or qualified engineering review" in next_step
    assert "Compare the excitation" in next_step
    arabic = " ".join(ui_text.text(k, "ar") for k in keys)
    for term in ("UNVALIDATED", "NOT EVIDENCE", "f₀", "N/m", "kg", "Hz", "2π"):
        assert term in arabic, term


def test_correction_12_is_recorded_in_the_calc_contract():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 12" in body and "## 13K." in body
    section = body[body.index("## 13K."):body.index("## 14.")]
    for phrase in ("exactly twelve", "`frequency`", "`Hz`", "`stiffness`", "`N/m`", "`mass`",
                   "`kg`", "content version `12`", "`1.11.0`", "2^-50", "`dcu:SU020`",
                   "`dcu:SU021`", "NOT a generic owner policy", "IP-UNRESOLVED",
                   "first admitted square-root", "angular_velocity"):
        assert phrase in section, phrase
    assert "- Correction 12 (§13K) is Owner-authorized" in body
    # §13J is unchanged
    assert "**Methods — exactly eleven:**" in body[body.index("## 13J."):body.index("## 13K.")]


def test_contract_and_stage15_exception_name_this_method():
    contract = CONTRACT.read_text(encoding="utf-8")
    assert "MECHANICAL-NATURAL-FREQUENCY-01" in contract
    s1 = contract[contract.index("## 1. Purpose"):contract.index("## 2.")]
    assert "the ONE inventor-declared Mechanical part" in s1 and "_calc_gate" in s1
    assert "SRC-045" in contract and "IP-UNRESOLVED" in contract
    source = (ROOT / "engine" / "subsystem_model.py").read_text(encoding="utf-8")
    assert "MECHANICAL-NATURAL-FREQUENCY-01" in source
    assert "``mechanical:spring_mass_natural_frequency`` v1.0" in source
    assert "No other specialist\nbehaviour is granted by these exceptions." in source


# ==========================================================================
# 6. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_session_link_and_page_on_a_mechanical_root_project(mech):
    c, _aid, sid = mech
    page = _page(c, sid)
    assert "data-mnf-link" in page and URL % sid in page
    r = c.get(URL % sid)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    body = r.get_data(as_text=True)
    assert "data-mnf-form" in body and not re.search(r"<input[^>]*\schecked", body)
    for role in ("k", "m"):
        assert re.search(r'name="value_%s"[^>]*maxlength="64"[^>]*value=""' % role, body)
    assert "data-mnf-result" not in body and "data-mnf-outcome" not in body
    assert body.count("data-mnf-declaration=") == 7 and body.count("data-mnf-screen=") == 9


def test_post_success_renders_in_the_same_request(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(k="1000", m="2.5"))
    assert r.status_code == 200 and "Location" not in r.headers
    body = r.get_data(as_text=True)
    assert re.findall(r'data-mnf-result-value><bdi dir="ltr">([^<]+)</bdi>',
                      body) == [EXAMPLE + " Hz"]
    assert "mechanical:spring_mass_natural_frequency" in body and "UNVALIDATED" in body
    assert "data-mnf-rounded" in body and "data-mnf-next-step" in body
    assert "data-mnf-verification" in body
    for key in ("UI_MNF_VERIFY_TITLE", "UI_MNF_VERIFY_INTRO",
                "UI_MNF_VERIFY_ITEM_1", "UI_MNF_VERIFY_ITEM_2",
                "UI_MNF_VERIFY_ITEM_3", "UI_MNF_VERIFY_ITEM_4",
                "UI_MNF_VERIFY_ITEM_5", "UI_MNF_VERIFY_BOUNDARY",
                "UI_MNF_VERIFY_AUTHORITY"):
        assert _norm(ui_text.text(key, "en")) in _norm(html.unescape(_content_text(body)))
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_MNF_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert _norm(ui_text.text("UI_MNF_NEXT_STEP", "en")) in text
    assert _norm(ui_text.text("UI_MNF_ROUNDED", "en")) in text
    assert re.findall(r'data-mnf-echo-value>([^<]*)<', body) == ["1000", "2.5"]
    assert "Technical Note 487" in body and "Special Publication 330" in body
    assert "nbstechnicalnote487" in body


@pytest.mark.parametrize("over,outcome", [
    ({"m": "0"}, "INVALID_NUMERIC_INPUT"),
    ({"k": "1234567890123"}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"supports_people": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"damping_not_modelled": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"single_mass": ""}}, "NOT_DECLARED"),
])
def test_post_non_success_shows_one_reason_and_no_number(mech, over, outcome):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(**over))
    body = r.get_data(as_text=True)
    assert r.status_code == 200
    assert html.escape(ui_text.text("UI_MNF_OUTCOME_" + outcome, "en"),
                       quote=False) in body
    assert "data-mnf-result" not in body and body.count("data-mnf-outcome") == 1
    assert "data-mnf-verification" not in body


def test_malformed_request_is_400_and_echo_is_escaped(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=dict(_form(), unexpected="1"))
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert ui_text.text("UI_MNF_ERR_REQUEST", "en") in body
    assert "data-mnf-outcome" not in body and "data-mnf-result" not in body
    body = c.post(URL % sid, data=_form(k="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body


def test_electronics_root_project_is_never_offered_or_evaluated(elec, monkeypatch):
    c, _aid, sid = elec
    assert "data-mnf-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._mnf, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-mnf-scope-note" in body
        assert "data-mnf-form" not in body and "data-mnf-outcome" not in body
    assert not called


def test_csrf_and_authorization_are_enforced(mech):
    _c, _aid, sid = mech
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("mnf-other@example.com")
    for client in (other, _new_client()):
        for response in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert response.status_code == 302
            assert "data-mnf" not in response.get_data(as_text=True)


@pytest.mark.parametrize("over", [{}, {"k": "0"}, {"m": "abc"},
                                  {"screen": {"children": "yes"}}])
def test_nothing_is_persisted_and_no_project_state_moves(mech, over):
    c, _aid, sid = mech
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_no_safety_signal_report_export_api_or_transfer_surface():
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    start = app_source.index("# MECHANICAL-NATURAL-FREQUENCY-01 — Spring-Mass Natural Frequency")
    section = app_source[start:app_source.index("# Manufacturing Evidence Capture", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_therm01", "_cap13r", "_cap13m", "_pwm", "load_project_subsystems",
                   "request.args", "request.values", "request.json"):
        assert banned not in section, banned
    assert section.count("_calc_gate(sid, _mnf)") == 3      # eligible / GET / POST
    routes = [r.rule for r in webapp.app.url_map.iter_rules() if "natural-frequency" in r.rule]
    assert routes == ["/session/<sid>/natural-frequency"] * 2
    for template in ("deliverable.html", "report.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "mnf" not in path.read_text(encoding="utf-8")


def test_existing_calculations_still_render_their_values(mech, elec):
    c, _aid, sid = mech
    body = c.post("/session/%s/support-reactions" % sid,
                  data=_cap13_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">750.0 N</bdi>' in body and '<bdi dir="ltr">250.0 N</bdi>' in body
    body = c.post("/session/%s/planar-moment" % sid,
                  data=_moment_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">1000.0 N·mm</bdi>' in body
    c2, _aid2, sid2 = elec
    body = c2.post("/session/%s/temperature-difference" % sid2,
                   data=_therm_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">25.0 K</bdi>' in body


def test_arabic_page_is_rtl_and_isolates_tokens(mech):
    c, _aid, sid = mech
    c.post("/ui-language", data={"lang": "ar"})
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert 'dir="rtl"' in body
    for token in ("k", "m", "f₀", "N/m", "kg", "Hz", "UNVALIDATED", "NOT EVIDENCE"):
        assert '(<bdi dir="ltr">%s</bdi>)' % html.escape(token) in body, token
    assert '<bdi dir="ltr">mechanical:spring_mass_natural_frequency</bdi>' in body
    assert '<bdi dir="ltr">%s Hz</bdi>' % EXAMPLE in body
    stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
    for item in ui_text.text("UI_MNF_DISCLOSURE", "ar").split("\n\n"):
        assert _norm(item) in _norm(stripped), item[:40]
    assert _norm(ui_text.text("UI_MNF_NEXT_STEP", "ar")) in _norm(stripped)
    for key in ("UI_MNF_VERIFY_TITLE", "UI_MNF_VERIFY_INTRO",
                "UI_MNF_VERIFY_ITEM_1", "UI_MNF_VERIFY_ITEM_2",
                "UI_MNF_VERIFY_ITEM_3", "UI_MNF_VERIFY_ITEM_4",
                "UI_MNF_VERIFY_ITEM_5", "UI_MNF_VERIFY_BOUNDARY",
                "UI_MNF_VERIFY_AUTHORITY"):
        assert _norm(ui_text.text(key, "ar")) in _norm(stripped)


def test_verification_preparation_is_bounded_and_artifact_sources_stay_pinned(mech):
    c, _aid, sid = mech
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-mnf-verification" in body
    combined = " ".join(ui_text.text(key, "en") for key in (
        "UI_MNF_VERIFY_INTRO", "UI_MNF_VERIFY_ITEM_1", "UI_MNF_VERIFY_ITEM_2",
        "UI_MNF_VERIFY_ITEM_3", "UI_MNF_VERIFY_ITEM_4", "UI_MNF_VERIFY_ITEM_5",
        "UI_MNF_VERIFY_BOUNDARY", "UI_MNF_VERIFY_AUTHORITY"))
    lowered = combined.lower()
    for banned in ("perform a frequency sweep to", "excite the system at resonance",
                   "resonance occurs at", "response peak is the natural frequency",
                   "safe frequency", "acceptable margin", "damping ratio",
                   "transmissibility ="):
        assert banned not in lowered, banned
    assert "not automatically the calculated f₀" in combined
    assert "does not instruct you to excite the system at or near resonance" in combined
    assert "UNVALIDATED" in combined and "NOT EVIDENCE" in combined

    # Reviewer correction: this increment must not mutate the pinned method
    # artifact or silently extend its source-use records.
    data = _method_artifact()
    assert data["artifact_version"] == "1"
    by_id = {r["record_id"]: r for r in data["sources"]}
    assert set(by_id) == {"NBS-NF-S1", "NIST-NF-U", "mnf:SU001", "mnf:SU002"}
    assert "maximum" not in by_id["NBS-NF-S1"]["inspected_content"].lower()
    assert "resonance sought" not in by_id["NBS-NF-S1"]["inspected_content"].lower()
    artifact_text = nf.ARTIFACT_PATH.read_text(encoding="utf-8")
    assert "MNF-VERIFICATION-MEASUREMENT-STEP-01" not in artifact_text
    assert "SRC-045" not in artifact_text


def test_verification_preparation_is_success_only_and_request_local(mech):
    c, _aid, sid = mech
    assert "data-mnf-verification" not in c.get(URL % sid).get_data(as_text=True)
    for over in ({"m": "0"},
                 {"screen": {"supports_people": "yes"}},
                 {"decl": {"single_mass": "does_not_apply"}}):
        body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
        assert "data-mnf-verification" not in body
    before = _snapshot(c)
    c.post(URL % sid, data=_form())
    assert _snapshot(c) == before


# ==========================================================================
# 7. the declared Mechanical part of an integrated composition
# ==========================================================================
def test_single_domain_projects_keep_exactly_the_root_rule():
    c, _aid = _client_for("mnf-part-single@example.com")
    mech_sid = _start(c, {"idea": SEED, "domain_confirm": MECH})
    elec_sid = _start(c, ELEC_FORM)
    assert webapp._calc_gate(mech_sid, nf) == (True, None)
    assert webapp._calc_gate(elec_sid, nf) == (False, None)
    assert "data-mnf-link" in _page(c, mech_sid)
    assert "data-mnf-link" not in _page(c, elec_sid)
    body = c.post(URL % mech_sid, data=_form()).get_data(as_text=True)
    assert _value(body) == EXAMPLE + " Hz" and "data-mnf-part" not in body
    body = c.post(URL % elec_sid, data=_form()).get_data(as_text=True)
    assert "data-mnf-form" not in body and _value(body) is None


@pytest.mark.parametrize("focus", (ELEC, MECH))
def test_integrated_mechanical_part_is_offered_in_either_focus(focus):
    c, _aid = _client_for("mnf-part-focus-%s@example.com" % focus)
    sid = _integrated(c, focus)
    eligible, part = webapp._calc_gate(sid, nf)
    assert eligible and part.domain == MECH
    assert part.display_name == PARTS["mech_part_name"]
    assert webapp._mnf_link_offered(sid) is True
    assert "data-mnf-link" in _page(c, sid)
    get_body = c.get(URL % sid).get_data(as_text=True)
    assert "data-mnf-form" in get_body
    assert _part_line(get_body, "mnf") == PARTS["mech_part_name"]
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) == EXAMPLE + " Hz"
    assert _part_line(body, "mnf") == PARTS["mech_part_name"]
    assert PARTS["elec_part_name"] not in body
    assert "UNVALIDATED" in body


def test_three_part_composition_names_only_the_mechanical_part():
    c, _aid = _client_for("mnf-part-three@example.com")
    sid = _integrated(c, ELEC, **CTRL)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _part_line(body, "mnf") == PARTS["mech_part_name"]
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
    monkeypatch.setattr(webapp._mnf, "evaluate", lambda *a, **k: evaluated.append(1))
    assert webapp._calc_gate(sid, nf) == (False, None)
    assert webapp._mnf_link_offered(sid) is False
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-mnf-scope-note" in body
        assert "data-mnf-form" not in body and "data-mnf-part" not in body
        assert _value(body) is None and "data-mnf-outcome" not in body
    assert not evaluated and not calls


def test_unreadable_composition_grants_nothing(elec_focus, monkeypatch):
    c, sid = elec_focus

    def broken(_sid):
        raise sqlite3.OperationalError("disk I/O error")
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", broken)
    calls = _owner_spy(monkeypatch)
    assert webapp._calc_gate(sid, nf) == (False, None)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) is None and "data-mnf-form" not in body
    assert not calls


def test_missing_or_invalid_composition_keeps_only_the_root_rule(monkeypatch):
    c, _aid = _client_for("mnf-part-missing@example.com")
    elec_sid = _integrated(c, ELEC)
    mech_sid = _integrated(c, MECH)
    monkeypatch.setattr(webapp._get_store(), "load_project_subsystems", lambda _sid: ())
    assert webapp._calc_gate(elec_sid, nf) == (False, None)
    assert webapp._calc_gate(mech_sid, nf) == (True, None)      # root rule only
    body = c.post(URL % mech_sid, data=_form()).get_data(as_text=True)
    assert _value(body) == EXAMPLE + " Hz" and "data-mnf-part" not in body


def test_the_request_can_never_supply_a_part_or_domain():
    c, _aid = _client_for("mnf-part-request@example.com")
    elec_sid = _start(c, ELEC_FORM)
    for extra in ({"part_domain": MECH}, {"subsystem_id": "sub-" + "0" * 32},
                  {"confirmed_domain": MECH}, {"part": "mechanical"}):
        body = c.post(URL % elec_sid, data=dict(_form(), **extra)).get_data(as_text=True)
        assert "data-mnf-form" not in body and _value(body) is None


def test_numbers_and_owner_requests_are_identical_irrespective_of_path(monkeypatch):
    c, _aid = _client_for("mnf-part-identical@example.com")
    root = _start(c, {"idea": SEED, "domain_confirm": MECH})
    part = _integrated(c, ELEC)
    calls = _owner_spy(monkeypatch)
    bodies = [c.post(URL % sid, data=_form(k="7.25", m="13"))
              .get_data(as_text=True) for sid in (root, part)]
    assert [_value(b) for b in bodies] == [nf.format_frequency(
        nf.reference_frequency(Fraction("7.25"), Fraction(13))) + " Hz"] * 2
    (req_root, res_root), (req_part, res_part) = calls
    assert req_root == req_part == {
        "method_id": method.METHOD_ID, "method_version": "1.0",
        "inputs": {"k": {"value": 7.25, "unit": "N/m"},
                   "m": {"value": 13.0, "unit": "kg"}},
        "subject_ref": None}
    assert res_root["result_identity"] == res_part["result_identity"]
    assert res_part["outputs"]["f0"]["unit"] == "Hz"


@pytest.mark.parametrize("lang", ("en", "ar"))
def test_attribution_is_escaped_isolated_and_bilingual(lang):
    c, _aid = _client_for("mnf-part-hostile-%s@example.com" % lang)
    sid = _integrated(c, ELEC, mech_part_name=HOSTILE)
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "<script>alert" not in body
    raw_name = _part_line(body, "mnf")
    assert raw_name is not None and "&lt;script&gt;" in raw_name
    assert html.unescape(raw_name) == HOSTILE
    assert '<bdi dir="auto" data-mnf-part-name>' in body
    stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
    for key in ("UI_CAP13_PART_LABEL", "UI_CAP13_PART_NOTE", "UI_MNF_SCOPE_NOTE"):
        assert ui_text.text(key, lang) in stripped, key
    if lang == "ar":
        assert 'dir="rtl"' in body
        assert '(<bdi dir="ltr">UNVALIDATED</bdi>)' in body
    assert '<bdi dir="ltr">%s Hz</bdi>' % EXAMPLE in body


def test_scope_wording_names_the_part_and_carries_no_applicability_claim():
    en = ui_text.text("UI_MNF_SCOPE_NOTE", "en")
    assert "declared Mechanical part" in en
    assert "contains a spring–mass system" in en
    assert "single-degree-of-freedom model applies" in en
    assert en.startswith("This optional calculation") and "Neither" in en
    for word in ("is suitable", "is safe", "is adequate", "approved", "compatible"):
        assert word not in en.lower(), word
    assert "الميكانيكي المصرّح به" in ui_text.text("UI_MNF_SCOPE_NOTE", "ar")
