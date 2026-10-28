# -*- coding: utf-8 -*-
"""CAP13-PLANAR-REQUIRED-FORCE-01 - Planar Required Force, Slice 1 (directly owning tests).

The shared deterministic calculation / units owner after the bounded ninth
admission of calc/units Correction 09 (§13H); the ONE method
``cap13:planar_required_force`` 1.0 (``engine/cap13_planar_required_force_method.py``)
and its ONE consumer (``engine/cap13_planar_required_force.py`` + the
request-local page).

The numerical tests use INDEPENDENT exact-rational references: each binary64
input is decomposed with ``float.as_integer_ratio`` and the exact quotient is
formed from integers, and each decimal input is read with ``Fraction`` from its
own text, never from the method's own arithmetic. The remaining tests press on
the method contract (§§1-9A): the closed nine-method inventory on the existing
N·mm / mm / N bindings; binding isolation; owner artifact v9 with every
content-version-8 record unchanged; method-artifact integrity; the §7 order and
owner correspondence; exact zero versus nonzero underflow; the Mechanical-root
and integrated Mechanical-part gate; request integrity, isolation and no
persistence; the existing methods unchanged; and EN / AR fidelity. Synthetic
data only.
"""
import ast
import copy
import hashlib
import html
import json
import math
import random
import re
from fractions import Fraction
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import cap13_planar_required_force as force
from engine import cap13_planar_required_force_method as method
from engine import cap13_planar_moment as moment
from engine import cap13_planar_moment_method as moment_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _corrupt, _part_line, MECH, ELEC, PARTS)
from tests.test_cap13_planar_moment import _form as _moment_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "STAGE25_CAP13_PLANAR_REQUIRED_FORCE_METHOD_CONTRACT.md")
CALC_CONTRACT = (ROOT / "docs" / "governance"
                 / "SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md")
URL = "/session/%s/planar-required-force"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
BOUND = Fraction(1, 2 ** 52)
DECIMAL_BOUND = Fraction(1, 2 ** 51)
TINY = 5e-324                         # 2^-1074, the smallest positive subnormal
# SHA-256 of the content-version-8 records (every quantity kind and unit
# record, dcu:SU001 to dcu:SU015 and the eight earlier method records), taken
# from the owner artifact at base c4bf3a9: the ninth admission adds and changes
# nothing else.
V8_RECORDS_DIGEST = "12d964ec076270359ce467e9ead219f83ef3a8f225860fd6ee5dfa9a7bc7c789"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _exact(value):
    numerator, denominator = float(value).as_integer_ratio()
    return Fraction(numerator, denominator)


def _request(M_target=5000.0, d_perp=250.0, units=("N·mm", "mm"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"M_target": {"value": M_target, "unit": units[0]},
                      "d_perp": {"value": d_perp, "unit": units[1]}},
           "subject_ref": None}
    req.update(over)
    return req


def _run(M_target, d_perp):
    return dc.execute(BINDING, _request(M_target=M_target, d_perp=d_perp))


def _failure(result):
    return (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def _form(M_target="5000", d_perp="250", decl=None, screen=None):
    form = {force.DECLARATION_FIELD % d: force.ANSWER_APPLIES
            for d in force.DECLARATION_IDS}
    form.update({force.SCREEN_FIELD % s: force.SCREEN_NO for s in force.SCREEN_ITEMS})
    form.update({force.VALUE_FIELD % "M_target": M_target,
                 force.VALUE_FIELD % "d_perp": d_perp})
    for key, value in (decl or {}).items():
        form[force.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[force.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = force.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return force.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _force_artifact():
    return json.loads(force.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data, name="a.json"):
    target = tmp_path / name
    target.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return target


def _norm(text):
    return re.sub(r"\s+", " ", text).strip()


def _value(body):
    marker = 'data-cap13f-result-value><bdi dir="ltr">'
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _no_owner(monkeypatch):
    calls = []
    monkeypatch.setattr(dc, "execute", lambda *a, **k: calls.append(1))
    return calls


@pytest.fixture
def mech():
    c, aid = _client_for("cap13f-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": "mechanical"})


@pytest.fixture
def elec():
    c, aid = _client_for("cap13f-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


# ==========================================================================
# 1. adapter: exact-rational division, binary64 acceptance, zero vs underflow
# ==========================================================================
@pytest.mark.parametrize("M_target,d_perp", [
    (5000.0, 250.0), (1000.0, 3.0), (10.0, 7.0), (1.0, 1.0), (0.1, 0.3),
    (1e-9, 999999999.999999999), (999999999999.999999999, 1e-9), (2.0 ** -1022, 1.0),
    (1.0, 2.0 ** 1023), (1e300, 1e-5)])
def test_quotients_are_correctly_rounded_and_within_the_bound(M_target, d_perp):
    result = _run(M_target, d_perp)
    assert result["state"] == dc.STATE_SUCCESS, result
    produced = result["outputs"]["F"]["value"]
    exact = _exact(M_target) / _exact(d_perp)
    assert produced == float(exact)                   # rounded once, half to even
    assert abs(_exact(produced) - exact) <= exact * BOUND
    assert result["outputs"]["F"]["unit"] == "N"


def test_random_quotients_match_the_independent_oracle():
    rng = random.Random(20261025)
    for _ in range(2000):
        m = rng.uniform(0.0, 1e12) * 10.0 ** rng.randint(-20, 0)
        d = rng.uniform(1e-9, 1e9)
        produced = method.evaluate(m, d)["F"]
        numerator_m, denominator_m = m.as_integer_ratio()
        numerator_d, denominator_d = d.as_integer_ratio()
        exact = Fraction(numerator_m * denominator_d, denominator_m * numerator_d)
        assert produced == float(exact)
        if exact:
            assert abs(_exact(produced) - exact) <= exact * BOUND


def test_a_zero_target_moment_gives_exact_zero_not_an_underflow():
    for d_perp in (1.0, 1e-9, 1e300, 5e-324):
        result = _run(0.0, d_perp)
        assert result["state"] == dc.STATE_SUCCESS
        value = result["outputs"]["F"]["value"]
        assert value == 0.0 and math.copysign(1.0, value) == 1.0
    assert method.evaluate(-0.0, 2.0) == {"F": 0.0}


def test_a_nonzero_underflow_is_an_integrity_failure_not_a_zero():
    with pytest.raises(ArithmeticError, match="underflowed"):
        method.evaluate(TINY, 1e300)
    assert _failure(_run(TINY, 1e300))


def test_a_subnormal_beyond_the_bound_is_refused_and_an_exact_one_accepted():
    with pytest.raises(ArithmeticError, match="relative error"):
        method.evaluate(TINY, 1.5)                    # 2/3 of TINY rounds to TINY
    assert _failure(_run(TINY, 1.5))
    assert method.evaluate(4 * TINY, 2.0) == {"F": 2 * TINY}   # exact subnormal


def test_overflow_is_an_integrity_failure_with_no_payload():
    with pytest.raises(ArithmeticError, match="overflow"):
        method.evaluate(1e308, 1e-10)
    assert _failure(_run(1e308, 1e-10))


@pytest.mark.parametrize("args", [
    (-1.0, 2.0), (1.0, 0.0), (1.0, -2.0), (float("nan"), 1.0), (1.0, float("inf")),
    (1, 2.0), (1.0, True), ("1", 2.0)])
def test_adapter_refuses_inputs_outside_the_admitted_domain(args):
    with pytest.raises(ArithmeticError):
        method.evaluate(*args)


def test_owner_applicability_and_typed_input_refusals():
    zero = _run(5.0, 0.0)
    assert (zero["state"], zero["reason"], zero["outputs"]) == (
        dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None)
    assert _failure(_run(-5.0, 2.0))      # no owner condition on M: the adapter refuses
    for bad in (float("nan"), float("inf"), "5", True):
        result = dc.execute(BINDING, _request(M_target=bad))
        assert result["state"] == dc.STATE_REFUSAL and result["outputs"] is None


# ==========================================================================
# 2. the shared owner: closed inventory, versions, bindings, artifact v9
# ==========================================================================
def test_success_packaging_units_sources_and_identity():
    result = _run(5000.0, 250.0)
    assert result["outputs"]["F"] == {"value": 20.0, "unit": "N",
                                      "provenance": "CALCULATED"}
    assert (result["method_id"], result["method_version"]) == (
        "cap13:planar_required_force", "1.0")
    assert (result["artifact_version"], result["implementation_version"]) == ("10", "1.9.0")
    assert sorted(u["record_id"] for u in result["unit_records"]) == [
        "dcu:U001", "dcu:U002", "dcu:U006"]
    assert [q["source_ref"] for q in result["source_qualification"]] == [
        "NASA-S1", "NASA-T1"]
    assert {q["source_use_policy_ref"] for q in result["source_qualification"]} == {
        "dcu:SU016"}
    assert result["validation_status"] == "UNVALIDATED"
    assert result == _run(5000.0, 250.0)                 # deterministic
    assert dc.execute(BINDING, _request(subject_ref="opaque"))["subject_ref"] == "opaque"


def test_closed_inventory_and_versions():
    assert ("cap13:planar_required_force", "1.0") in dc.ADMITTED_METHODS
    assert len(dc.ADMITTED_METHODS) == 10
    assert len(dc.ADMITTED_QUANTITY_KINDS) == 15 and len(dc.ADMITTED_UNIT_TOKENS) == 17
    assert dc.IMPLEMENTATION_VERSION == "1.9.0"
    data = dc.load_artifact()
    assert data["artifact_version"] == "10"
    record = _record(data)
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"]] == [("M_target", "moment", "N·mm"),
                                                ("d_perp", "length", "mm")]
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["output_roles"]] == [("F", "force", "N")]
    assert record["applicability"] == [
        {"role": "d_perp", "condition": "greater_than_zero", "bound_role": None}]
    assert record["result_range"] == []
    assert record["adapter_identity"] == "engine.cap13_planar_required_force_method.evaluate"
    assert record["method_authority_artifact"] == {
        "artifact_id": "cap13_planar_required_force", "artifact_version": "1"}


def test_owner_v8_records_are_unchanged_by_the_ninth_admission():
    data = dc.load_artifact()
    # Correction 10 (§13I) appends the electric_charge kind, the h / A·h unit
    # records, dcu:SU017 / dcu:SU018 and the tenth method after these
    v8 = {"quantity_kinds": data["quantity_kinds"][:14],
          "unit_records": data["unit_records"][:15],
          "source_use_policies": data["source_use_policies"][:15],
          "methods": data["methods"][:8]}
    canonical = json.dumps(v8, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert hashlib.sha256(canonical.encode()).hexdigest() == V8_RECORDS_DIGEST
    assert [p["record_id"] for p in data["source_use_policies"][15:16]] == ["dcu:SU016"]
    assert [m["method_id"] for m in data["methods"][8:9]] == ["cap13:planar_required_force"]
    su16 = data["source_use_policies"][15]
    assert "planar required force method sources NASA-S1 and NASA-T1 only" \
        in su16["inspected_content"]
    assert "dcu:SU002 and dcu:SU005 keep their own scopes" in su16["inspection_reference"]


@pytest.mark.parametrize("units", [("N·m", "mm"), ("N·mm", "m"), ("Nmm", "mm"),
                                   ("N", "mm"), ("N·mm", "N·mm")])
def test_units_are_exact_with_no_alias_or_conversion(units):
    result = dc.execute(BINDING, _request(units=units))
    assert result["state"] == dc.STATE_REFUSAL
    assert result["reason"] in (dc.UNIT_NOT_ADMITTED, dc.UNKNOWN_UNIT)
    assert result["outputs"] is None


def test_method_version_and_adapter_integrity_fail_closed():
    assert dc.execute(BINDING, _request(method_version="1.1"))["reason"] \
        == dc.VERSION_MISMATCH
    other = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, lambda **k: {"F": 1.0})
    assert _failure(dc.execute(other, _request()))     # not this method's adapter
    moment_binding = dc.bind_method(moment_method.METHOD_ID, moment_method.METHOD_VERSION,
                                    moment_method.evaluate)
    refused = dc.execute(moment_binding, _request())   # a binding runs only its own method
    assert (refused["state"], refused["reason"], refused["outputs"]) == (
        dc.STATE_REFUSAL, dc.OPERATION_NOT_ADMITTED, None)


def test_app_wires_one_immutable_binding_per_method():
    assert webapp._CAP13_REQUIRED_FORCE_BINDING.method_id == method.METHOD_ID
    assert webapp._CAP13_REQUIRED_FORCE_BINDING.adapter_identity \
        == "engine.cap13_planar_required_force_method.evaluate"
    with pytest.raises(AttributeError):
        webapp._CAP13_REQUIRED_FORCE_BINDING.method_id = "x"
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 10
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("cap13_planar_required_force", "cap13_content_config",
                   "import fractions", "sqlite"):
        assert banned not in owner_source, banned


def test_owner_artifact_tamper_fails_closed(tmp_path):
    data = _owner_artifact()
    _record(data)["output_roles"][0]["unit_token"] = "N·mm"
    assert _failure(dc.execute(BINDING, _request(), artifact_path=_write(tmp_path, data)))
    data = _owner_artifact()
    data["methods"] = data["methods"][:8]                # not the admitted inventory
    assert _failure(dc.execute(BINDING, _request(),
                               artifact_path=_write(tmp_path, data, "b.json")))


# ==========================================================================
# 3. the consumer: grammar, positive distance, order, reference, display
# ==========================================================================
@pytest.mark.parametrize("m,d,shown,exact", [
    ("5000", "250", "20", True),
    ("1000", "3", "333.333333333", False),
    ("10", "7", "1.42857142857", False),
    ("12.5", "0.5", "25", True),
    ("1", "8", "0.125", True),
    ("0.000001", "1", "0.000001", True),
    ("0.0000001", "1", "1 × 10^-7", True),
    ("0.000000001", "999999999.999999999", "1 × 10^-18", False),
    ("999999999999.999999999", "0.000000001", "1 × 10^21", False),
    ("999999999999", "0.5", "2 × 10^12", False),
    ("0", "12.5", "0", True),
    ("0.000000000", "1", "0", True),
])
def test_reference_vectors_and_display(m, d, shown, exact):
    result = _evaluate(M_target=m, d_perp=d)
    assert result["outcome"] == force.OUTCOME_SUCCESS, result
    assert (result["display_value"], result["display_exact"]) == (shown, exact)
    assert result["force"] == Fraction(m) / Fraction(d)
    assert result["zero_moment"] is (Fraction(m) == 0)
    binary = result["result"]["outputs"]["F"]["value"]
    assert (binary == 0.0) is (Fraction(m) == 0)


def test_random_decimals_agree_with_the_exact_decimal_quotient():
    rng = random.Random(25)
    for _ in range(500):
        m = "%d.%09d" % (rng.randrange(10 ** 12), rng.randrange(10 ** 9))
        d = "%d.%09d" % (rng.randrange(10 ** 9), rng.randrange(1, 10 ** 9))
        result = _evaluate(M_target=m, d_perp=d)
        assert result["outcome"] == force.OUTCOME_SUCCESS
        reference = Fraction(m) / Fraction(d)
        binary = result["result"]["outputs"]["F"]["value"]
        if reference:
            assert abs(Fraction(binary) - reference) <= reference * DECIMAL_BOUND
        text, exact = force.format_force(reference)
        assert (result["display_value"], result["display_exact"]) == (text, exact)


@pytest.mark.parametrize("d", ["0", "0.0", "000", "0.000000000"])
def test_zero_distance_is_refused_before_the_owner(d, monkeypatch):
    calls = _no_owner(monkeypatch)
    result = _evaluate(d_perp=d)
    assert result["outcome"] == force.DISTANCE_NOT_POSITIVE
    assert result["result"] is None and result["display_value"] is None
    assert not calls


@pytest.mark.parametrize("text", [
    "", "-1", "+1", "1e3", "1E3", "1,5", "1_0", " 1", "1 ", ".5", "5.", "0x10",
    "inf", "nan", "١٢", "12N", "1.0000000001", "-0"])
def test_numeric_grammar_is_strict(text, monkeypatch):
    calls = _no_owner(monkeypatch)
    assert _evaluate(M_target=text)["outcome"] == force.INVALID_NUMERIC_INPUT, text
    assert _evaluate(d_perp=text)["outcome"] == force.INVALID_NUMERIC_INPUT, text
    assert not calls


def test_representation_limits_are_per_role():
    assert force.parse_value("9" * 12, "M_target") == Fraction("9" * 12)
    assert force.parse_value("9" * 13, "M_target") is None
    assert force.parse_value("9" * 9, "d_perp") == Fraction("9" * 9)
    assert force.parse_value("9" * 10, "d_perp") is None
    assert force.parse_value("1.123456789", "d_perp") == Fraction("1.123456789")
    assert force.parse_value("0", "M_target") == 0


def test_pre_owner_order_first_failing_stage_wins(monkeypatch):
    calls = _no_owner(monkeypatch)
    assert _evaluate(decl={"planar": ""}, screen={"pressure": "yes"},
                     M_target="abc", d_perp="0")["outcome"] == force.NOT_DECLARED
    assert _evaluate(screen={"pressure": ""})["outcome"] == force.NOT_DECLARED
    assert _evaluate(screen={"children": "yes"}, decl={"target_moment": "does_not_apply"},
                     d_perp="0")["outcome"] == force.ENGINEERING_REVIEW_REQUIRED
    for decl in force.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"}, M_target="x")["outcome"] \
            == force.MODEL_NOT_SUPPORTED, decl
    # a malformed number wins over a zero distance
    assert _evaluate(M_target="x", d_perp="0")["outcome"] == force.INVALID_NUMERIC_INPUT
    assert not calls


@pytest.mark.parametrize("form", [
    {"unexpected": ["1"]},
    {force.VALUE_FIELD % "M_target": ["1", "2"]},
    {force.DECLARATION_FIELD % "target_moment": ["yes"]},
    {force.SCREEN_FIELD % "children": ["maybe"]},
    {force.VALUE_FIELD % "F": ["1"]},
])
def test_malformed_capture_is_none(form):
    base = {k: [v] for k, v in _form().items()}
    base.update(form)
    assert force.capture_form(base) is None
    assert force.capture_form("not a mapping") is None


@pytest.mark.parametrize("state,reason,outcome", [
    (dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, force.INVALID_NUMERIC_INPUT),
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, force.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.UNKNOWN_UNIT, force.UNIT_NOT_SUPPORTED),
    (dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED, force.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.VERSION_MISMATCH, force.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, force.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, force.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, force.UNMAPPED_OWNER_OUTCOME),
])
def test_owner_correspondence_preserves_the_owner_state(state, reason, outcome,
                                                        monkeypatch):
    monkeypatch.setattr(dc, "execute", lambda *a, **k: {
        "state": state, "reason": reason, "outputs": None})
    result = _evaluate()
    assert result["outcome"] == outcome
    assert (result["owner_state"], result["owner_reason"]) == (state, reason)
    assert result["result"] is None and result["display_value"] is None


@pytest.mark.parametrize("m,produced", [("5000", 20.000001), ("5000", 0.0),
                                        ("0", 1e-300), ("5000", float("inf"))])
def test_a_success_that_disagrees_with_the_decimal_reference_shows_no_number(
        m, produced, monkeypatch):
    real = dc.execute

    def fake(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result = copy.deepcopy(result)
        result["outputs"]["F"]["value"] = produced
        return result
    monkeypatch.setattr(dc, "execute", fake)
    result = _evaluate(M_target=m)
    assert result["outcome"] == force.KNOWLEDGE_UNAVAILABLE
    assert result["result"] is None and result["display_value"] is None


def test_typed_values_and_fixed_units_reach_the_owner(monkeypatch):
    seen = []
    real = dc.execute
    monkeypatch.setattr(dc, "execute", lambda b, r, artifact_path=None: (
        seen.append(copy.deepcopy(r)), real(b, r, artifact_path=artifact_path))[1])
    _evaluate(M_target="2.5", d_perp="0.1")
    assert seen == [{"method_id": method.METHOD_ID, "method_version": "1.0",
                     "inputs": {"M_target": {"value": 2.5, "unit": "N·mm"},
                                "d_perp": {"value": 0.1, "unit": "mm"}},
                     "subject_ref": None}]


def test_format_force_rejects_non_fractions_and_negatives():
    with pytest.raises(TypeError):
        force.format_force(1.5)
    with pytest.raises(ValueError):
        force.format_force(Fraction(-1, 2))


def test_artifact_loads_and_binds_its_own_sources():
    content = force.load_artifact()
    assert content["method"]["method_id"] == method.METHOD_ID
    by_id = {r["record_id"]: r for r in content["sources"]}
    assert by_id["NASA-S1"]["source_use_policy_ref"] == "cap13f:SU001"
    assert by_id["NASA-T1"]["source_use_policy_ref"] == "cap13f:SU001"
    assert by_id["NIST-U"]["source_use_policy_ref"] == "cap13f:SU002"
    # the reused evidence is the planar-moment method's, at the same URLs and dates
    moment_sources = {r["record_id"]: r for r in moment.load_artifact()["sources"]}
    for rid in ("NASA-S1", "NASA-T1", "NIST-U"):
        assert (by_id[rid]["url"], by_id[rid]["inspection_date"]) == (
            moment_sources[rid]["url"], moment_sources[rid]["inspection_date"])
    assert content["screen_items"] == moment.load_artifact()["screen_items"]


@pytest.mark.parametrize("mutate", [
    lambda d: d["declarations"].pop(),
    lambda d: d["disclosure"].pop(),
    lambda d: d["numeric_domain"]["roles"][2].update(unit_token="N·mm"),
    lambda d: d["method"].update(executed_form="F = M_target * d_perp"),
    lambda d: d["sources"][0].update(source_use_policy_ref="cap13m:SU001"),
    lambda d: d["declarations"][4].update(accepted_value="the target moment is checked"),
    lambda d: d.update(artifact_version="2"),
])
def test_artifact_tamper_is_knowledge_unavailable(tmp_path, mutate, monkeypatch):
    data = _force_artifact()
    mutate(data)
    path = _write(tmp_path, data)
    with pytest.raises(force.RequiredForceKnowledgeError):
        force.load_artifact(path)
    calls = _no_owner(monkeypatch)
    monkeypatch.setattr(force, "ARTIFACT_PATH", path)
    assert _evaluate()["outcome"] == force.KNOWLEDGE_UNAVAILABLE
    assert not calls


def test_modules_import_no_other_method_authority():
    for module in (force, method):
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(a.name for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                imports.add(node.module or "")
        for banned in ("cap13_planar_moment", "cap13_static", "cap13_rotational",
                       "dc_resistive", "therm01", "tmp36", "record_store",
                       "safety_signal", "web", "requests", "sqlite3"):
            assert not any(banned in name for name in imports), (module, banned)
    source = Path(force.__file__).read_text(encoding="utf-8")
    assert "planar_single_force_moment_v1.json" not in source


# ==========================================================================
# 4. EN / AR fidelity and the governing contracts
# ==========================================================================
def test_english_wording_equals_the_artifact():
    content = force.load_artifact()
    assert ui_text.text("UI_CAP13F_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"].replace("d_perp", "d⊥")
        assert ui_text.text("UI_CAP13F_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."


def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_arabic_and_english_wording_equal_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    items = [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    assert ui_text.text("UI_CAP13F_DISCLOSURE", "ar").split("\n\n") == items
    a2 = _contract_section("**A-2", "**A-3")
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$", a2, re.M))
    for entry in force.load_artifact()["declarations"]:
        key = "%s %s" % (entry["contract_ref"], entry["declaration_id"])
        assert ui_text.text("UI_CAP13F_DECL_" + entry["declaration_id"].upper(), "ar") \
            == rows[key], key
    s9 = _contract_section("## 9. Result", "## 9A.")
    english = [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)]
    assert english == force.load_artifact()["disclosure"]
    s5 = _contract_section("## 5. Applicability", "## 6.")
    for entry in force.load_artifact()["declarations"]:
        assert "| %s | `%s` | %s |" % (entry["contract_ref"], entry["declaration_id"],
                                       entry["accepted_value"]) in s5


def test_every_key_has_both_languages_and_no_overclaim():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_CAP13F_")] \
        if hasattr(ui_text, "UI_STRINGS") else [
            "UI_CAP13F_" + s for s in (
                "LINK_TEXT", "LINK_NOTE", "TITLE", "INTRO", "SCOPE_NOTE", "RESULT_F",
                "EXACT", "ROUNDED", "ZERO_NOTE", "STATUS", "SOURCES_NOTE", "DISCLOSURE",
                "ERR_REQUEST")] + ["UI_CAP13F_OUTCOME_" + o for o in force.OUTCOMES[1:]]
    assert len(keys) >= 20
    for key in keys:
        en, ar = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert en and ar and en != ar, key
        lowered = en.lower()
        # positive claims only: the copy names these topics in order to deny them
        for claim in ("it is safe", "will work", "has been validated", "this force is enough",
                      "you can apply", "the motor can", "recommended", "you should use"):
            assert claim not in lowered, (key, claim)
    for outcome in force.OUTCOMES[1:]:
        assert ui_text.text("UI_CAP13F_OUTCOME_" + outcome, "en")


def test_correction_09_is_recorded_in_the_calc_contract():
    body = CALC_CONTRACT.read_text(encoding="utf-8")
    assert "CORRECTION 09" in body and "## 13H." in body
    section = body[body.index("## 13H."):body.index("## 14.")]
    for phrase in ("exactly nine", "`cap13:planar_required_force` 1.0", "none added",
                   "content version `9`", "`1.8.0`", "`dcu:SU016`", "2^-52", "2^-51",
                   "NOT a generic owner policy"):
        assert phrase in section, phrase
    assert "**Methods — exactly eight:**" in body[body.index("## 13G."):body.index("## 13H.")]


def test_the_stage15_exception_names_this_method():
    source = (ROOT / "engine" / "subsystem_model.py").read_text(encoding="utf-8")
    assert "(CAP13-PLANAR-REQUIRED-FORCE-01)" in source
    assert "``cap13:planar_required_force`` v1.0" in source


# ==========================================================================
# 5. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_session_link_and_page_on_a_mechanical_root_project(mech):
    c, _aid, sid = mech
    page = _page(c, sid)
    assert "data-cap13f-link" in page and URL % sid in page
    assert "data-cap13m-link" in page            # the planar moment link is unchanged
    r = c.get(URL % sid)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    body = r.get_data(as_text=True)
    assert "data-cap13f-form" in body and "checked" not in body
    for role in ("M_target", "d_perp"):
        assert re.search(r'name="value_%s"[^>]*maxlength="64"[^>]*value=""' % role, body)
    assert "data-cap13f-result" not in body and "data-cap13f-outcome" not in body
    radios = re.findall(r'type="radio"', body)
    assert len(radios) == 2 * (len(force.DECLARATION_IDS) + len(force.SCREEN_ITEMS))


def test_post_success_renders_in_the_same_request(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(M_target="1000", d_perp="3"))
    assert r.status_code == 200 and "Location" not in r.headers
    body = r.get_data(as_text=True)
    assert _value(body) == "333.333333333 N"
    assert 'data-cap13f-exactness="rounded"' in body
    assert "data-cap13f-zero-note" not in body
    assert "cap13:planar_required_force" in body and "UNVALIDATED" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_CAP13F_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert re.findall(r'data-cap13f-echo-value>([^<]*)<', body) == ["1000", "3"]
    assert "Torque (Moment)" in body and "Appendix B.9" in body


def test_zero_target_moment_renders_zero_with_its_note(mech):
    c, _aid, sid = mech
    body = c.post(URL % sid, data=_form(M_target="0")).get_data(as_text=True)
    assert _value(body) == "0 N"
    assert 'data-cap13f-exactness="exact"' in body and "data-cap13f-zero-note" in body


@pytest.mark.parametrize("over,outcome", [
    ({"d_perp": "0"}, "DISTANCE_NOT_POSITIVE"),
    ({"M_target": "-5"}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"supports_people": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"target_moment": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"decl": {"planar": ""}}, "NOT_DECLARED"),
])
def test_post_non_success_shows_one_reason_and_no_number(mech, over, outcome):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(**over))
    body = r.get_data(as_text=True)
    assert r.status_code == 200
    assert html.escape(ui_text.text("UI_CAP13F_OUTCOME_" + outcome, "en"),
                       quote=False) in body
    assert "data-cap13f-result" not in body and body.count("data-cap13f-outcome") == 1
    assert " N<" not in body.split("data-cap13f-outcome", 1)[1].split("</div>", 1)[0]


def test_malformed_request_is_400_and_echo_is_escaped(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=dict(_form(), unexpected="1"))
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert ui_text.text("UI_CAP13F_ERR_REQUEST", "en") in body
    assert "data-cap13f-outcome" not in body and "data-cap13f-result" not in body
    body = c.post(URL % sid, data=_form(M_target="<b>1</b>")).get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body


def test_electronics_root_project_is_never_offered_or_evaluated(elec, monkeypatch):
    c, _aid, sid = elec
    assert "data-cap13f-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._cap13f, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-cap13f-scope-note" in body
        assert "data-cap13f-form" not in body and "data-cap13f-outcome" not in body
    assert not called
    assert webapp._calc_gate(sid, force) == (False, None)


@pytest.mark.parametrize("focus", (ELEC, MECH))
def test_integrated_mechanical_part_is_offered_in_either_focus(focus):
    c, _aid = _client_for("cap13f-focus-%s@example.com" % focus)
    sid = _integrated(c, focus)
    eligible, part = webapp._calc_gate(sid, force)
    assert eligible and part.domain == MECH
    assert webapp._cap13f_link_offered(sid) is True
    assert "data-cap13f-link" in _page(c, sid)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert _value(body) == "20 N"
    assert _part_line(body, "cap13f") == PARTS["mech_part_name"]
    assert PARTS["elec_part_name"] not in body


def test_a_corrupt_composition_grants_nothing(monkeypatch):
    c, _aid = _client_for("cap13f-corrupt@example.com")
    sid = _integrated(c, ELEC)
    _corrupt("UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 0")
    called = []
    monkeypatch.setattr(webapp._cap13f, "evaluate", lambda *a, **k: called.append(1))
    assert webapp._calc_gate(sid, force) == (False, None)
    assert webapp._cap13f_link_offered(sid) is False
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-cap13f-form" not in body
    assert not called


def test_the_gate_is_the_shared_calc_gate_and_reads_nothing_from_the_request():
    src = Path(webapp.__file__).read_text(encoding="utf-8")
    start = src.index("# CAP13-PLANAR-REQUIRED-FORCE-01 — Planar Required Force")
    section = src[start:src.index("# Stage 25 / CAP-13 — Linear Speed-Dependent", start)]
    assert section.count("_calc_gate(sid, _cap13f)") == 3      # eligible / GET / POST
    for banned in ("request.args", "request.values", "request.json",
                   "load_project_subsystems", "_get_store()", "safety_signal",
                   "SafetySignal(", "append_", "SESSION_STORE[", "deliverable", "pdf",
                   "export", "/api/", "_cap13m.", "_CAP13_MOMENT_BINDING"):
        assert banned not in section, banned
    routes = [r.rule for r in webapp.app.url_map.iter_rules()
              if "planar-required-force" in r.rule]
    assert routes == ["/session/<sid>/planar-required-force"] * 2
    for template in ("deliverable.html", "report.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "cap13f" not in path.read_text(encoding="utf-8")


def test_csrf_and_authorization_are_enforced(mech):
    _c, _aid, sid = mech
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("cap13f-other@example.com")
    for client in (other, _new_client()):
        for response in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert response.status_code == 302
            assert "data-cap13f" not in response.get_data(as_text=True)


@pytest.mark.parametrize("over", [{}, {"M_target": "0"}, {"d_perp": "0"},
                                  {"M_target": "abc"}, {"screen": {"children": "yes"}}])
def test_nothing_is_persisted_and_no_request_leaks_into_the_next(mech, over):
    c, _aid, sid = mech
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(**over))
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-cap13f-result" not in body and "checked" not in body
    assert re.search(r'name="value_M_target"[^>]*value=""', body)
    assert _snapshot(c) == before


def test_the_planar_moment_page_is_unchanged_and_shares_no_result(mech):
    c, _aid, sid = mech
    c.post(URL % sid, data=_form(M_target="5000", d_perp="250"))
    body = c.post("/session/%s/planar-moment" % sid,
                  data=_moment_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">1000.0 N·mm</bdi>' in body
    assert "cap13f" not in body and "planar_required_force" not in body
    body = c.get(URL % sid).get_data(as_text=True)
    assert "1000.0" not in body and "data-cap13f-result" not in body


def test_arabic_page_is_rtl_and_isolates_tokens(mech):
    c, _aid, sid = mech
    c.post("/ui-language", data={"lang": "ar"})
    body = c.post(URL % sid, data=_form(M_target="1000", d_perp="3")).get_data(as_text=True)
    assert 'dir="rtl"' in body
    for token in ("M_target", "d⊥", "F", "N", "mm", "N·mm", "UNVALIDATED", "NOT EVIDENCE"):
        assert '(<bdi dir="ltr">%s</bdi>)' % html.escape(token) in body, token
    assert '<bdi dir="ltr">cap13:planar_required_force</bdi>' in body
    assert _value(body) == "333.333333333 N"
    assert '<bdi dir="ltr">F = M_target / d⊥</bdi>' in body
    stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
    for item in ui_text.text("UI_CAP13F_DISCLOSURE", "ar").split("\n\n"):
        assert _norm(item) in _norm(stripped), item[:40]
