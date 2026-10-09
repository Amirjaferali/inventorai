# -*- coding: utf-8 -*-
"""Stage 27 / THERM-01 - Single-Path Temperature-Difference, Slice 1 (directly owning tests).

The shared deterministic calculation / units owner (``engine/deterministic_calculation.py``)
after the bounded second admission of calc/units Correction 02 (§13A); the ONE
THERM-01 method (``therm01:conduction_temperature_difference_single_path`` 1.0,
``engine/therm01_conduction_method.py``) and its ONE consumer
(``engine/therm01_temperature_difference.py`` + the request-local web page).

The tests press on the accepted THERM-01 contract (§§1-9A) and Correction 02:
the exact value ``ΔT = P × Rθ``; the closed two-method inventory and the exact
W / K/W / K bindings (no alias, no Celsius, no conversion); both bindings isolated
from each other; owner artifact v2 integrity; the §7 pre-owner order and owner
correspondence (owner FAILURE is never remapped to REFUSAL); overflow and
non-finite results; the Electrical / Electronics durable-root gate; request
integrity, isolation and no persistence; and EN / AR fidelity to the contract.
"""
import copy
import html
import json
import math
import re
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import therm01_temperature_difference as therm
from engine import therm01_conduction_method as method
from engine import cap13_static_reactions_method as cap13_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "STAGE27_THERM01_CONDUCTION_TEMPERATURE_DIFFERENCE_METHOD_CONTRACT.md")
URL = "/session/%s/temperature-difference"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)
CAP13_BINDING = dc.bind_method(cap13_method.METHOD_ID, cap13_method.METHOD_VERSION,
                               cap13_method.evaluate)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _request(P=10.0, R_theta=2.5, units=("W", "K/W"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"P": {"value": P, "unit": units[0]},
                      "R_theta": {"value": R_theta, "unit": units[1]}},
           "subject_ref": None}
    req.update(over)
    return req


def _cap13_request():
    return {"method_id": cap13_method.METHOD_ID,
            "method_version": cap13_method.METHOD_VERSION,
            "inputs": {"P": {"value": 1000.0, "unit": "N"},
                       "L": {"value": 2000.0, "unit": "mm"},
                       "x": {"value": 500.0, "unit": "mm"}},
            "subject_ref": None}


def _form(P="10", R_theta="2.5", decl=None, screen=None):
    form = {therm.DECLARATION_FIELD % d: therm.ANSWER_APPLIES
            for d in therm.DECLARATION_IDS}
    form.update({therm.SCREEN_FIELD % s: therm.SCREEN_NO for s in therm.SCREEN_ITEMS})
    form.update({therm.VALUE_FIELD % "P": P, therm.VALUE_FIELD % "R_theta": R_theta})
    for key, value in (decl or {}).items():
        form[therm.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[therm.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = therm.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return therm.evaluate(_captured(**kw), BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _therm_artifact():
    return json.loads(therm.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _record(data, method_id=method.METHOD_ID):
    (record,) = [m for m in data["methods"] if m["method_id"] == method_id]
    return record


def _write(tmp_path, data, name="a.json"):
    target = tmp_path / name
    target.write_text(json.dumps(data), encoding="utf-8")
    return target


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def _table(section):
    rows = {}
    for line in section.splitlines():
        m = re.match(r"^\| (.+?) \| (.+?) \|$", line)
        if m and not set(m.group(1)) <= set("-"):
            rows[m.group(1).strip("`")] = m.group(2)
    return rows


def _numbered_quote_items(section):
    items, current = [], None
    for line in section.splitlines():
        m = re.match(r"^> (\d)\. (.*)$", line)
        if m:
            if current is not None:
                items.append(_norm(current))
            current = m.group(2)
        elif line.startswith(">    ") and current is not None:
            current += " " + line[5:]
    if current is not None:
        items.append(_norm(current))
    return items


def _guillemet(section, after):
    start = section.index("«", section.index(after))
    depth, i = 0, start
    while True:
        if section[i] == "«":
            depth += 1
        elif section[i] == "»":
            depth -= 1
            if depth == 0:
                return _norm(section[start + 1:i])
        i += 1


@pytest.fixture
def elec():
    c, aid = _client_for("therm01-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def mech():
    c, aid = _client_for("therm01-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": "mechanical"})


# ==========================================================================
# 1. the method: the one executed form, overflow and non-finite results
# ==========================================================================
def test_interior_numerical_value():
    result = dc.execute(BINDING, _request())
    assert result["state"] == dc.STATE_SUCCESS and result["reason"] is None
    assert result["outputs"] == {"delta_T": {"value": 25.0, "unit": "K",
                                             "provenance": "CALCULATED"}}
    assert result["validation_status"] == "UNVALIDATED"
    assert result["inputs"]["R_theta"] == {"value": 2.5, "unit": "K/W",
                                           "provenance": "OWNER_STATED"}


@pytest.mark.parametrize("P,R,expected", [(1.0, 1.0, 1.0), (0.5, 4.0, 2.0),
                                          (1e-3, 2e3, 2.0), (3.0, 0.1, 3.0 * 0.1)])
def test_values_are_the_plain_product(P, R, expected):
    result = dc.execute(BINDING, _request(P=P, R_theta=R))
    assert result["outputs"]["delta_T"]["value"] == expected


def test_method_is_one_multiplication_with_no_ceiling_or_rounding():
    import inspect
    source = inspect.getsource(method.evaluate)
    assert "P * R_theta" in source
    for banned in ("round(", "min(", "max(", "isclose", "tolerance", " - ", "273"):
        assert banned not in source, banned
    imports = re.findall(r"^\s*(?:from|import)\s+([\w.]+)",
                         Path(method.__file__).read_text(encoding="utf-8"), re.M)
    assert imports == ["math"]
    # no physical magnitude ceiling: a very large admitted pair still succeeds
    result = dc.execute(BINDING, _request(P=1e150, R_theta=1e150))
    assert result["state"] == dc.STATE_SUCCESS
    assert result["outputs"]["delta_T"]["value"] == 1e150 * 1e150


@pytest.mark.parametrize("P,R", [(1e200, 1e200), (1.7e308, 2.0)])
def test_overflow_is_execution_integrity_failure_with_no_payload(P, R):
    result = dc.execute(BINDING, _request(P=P, R_theta=R))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)
    assert "result_identity" not in result
    with pytest.raises(ArithmeticError):
        method.evaluate(P, R)


def test_underflow_to_zero_fails_the_governed_result_range():
    result = dc.execute(BINDING, _request(P=1e-200, R_theta=1e-200))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


@pytest.mark.parametrize("produced", [{"delta_T": float("nan")},
                                      {"delta_T": float("inf")},
                                      {"delta_T": 1}, {"other": 1.0},
                                      ArithmeticError("x")])
def test_non_finite_or_tampered_adapter_output_fails_closed(produced):
    def evaluate(P, R_theta):
        if isinstance(produced, Exception):
            raise produced
        return produced
    evaluate.__module__ = method.evaluate.__module__
    evaluate.__qualname__ = method.evaluate.__qualname__
    fake = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, evaluate)
    result = dc.execute(fake, _request())
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


@pytest.mark.parametrize("bad", [True, "10", None, float("nan"), float("inf"),
                                 float("-inf")])
def test_owner_refuses_non_numeric_and_non_finite_inputs(bad):
    result = dc.execute(BINDING, _request(P=bad))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT, None)
    assert result["outputs"] is None


@pytest.mark.parametrize("over", [{"P": 0.0}, {"P": -1.0}, {"R_theta": 0.0},
                                  {"R_theta": -2.0}])
def test_owner_domain_is_defence_in_depth(over):
    result = dc.execute(BINDING, _request(**over))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, None)


# ==========================================================================
# 2. the shared owner after Correction 02: exact bindings, isolation, closed set
# ==========================================================================
@pytest.mark.parametrize("units,reason", [
    (("mW", "K/W"), dc.UNKNOWN_UNIT), (("kW", "K/W"), dc.UNKNOWN_UNIT),
    (("W", "°C/W"), dc.UNKNOWN_UNIT), (("W", "C/W"), dc.UNKNOWN_UNIT),
    (("W", "K/w"), dc.UNKNOWN_UNIT), (("w", "K/W"), dc.UNKNOWN_UNIT),
    (("W", "K / W"), dc.UNKNOWN_UNIT), (("W", "KW^-1"), dc.UNKNOWN_UNIT),
    (("W", "°C"), dc.UNKNOWN_UNIT), (("W", "degC"), dc.UNKNOWN_UNIT),
    (("K/W", "W"), dc.UNIT_NOT_ADMITTED), (("W", "K"), dc.UNIT_NOT_ADMITTED),
    (("N", "K/W"), dc.UNIT_NOT_ADMITTED), (("W", "mm"), dc.UNIT_NOT_ADMITTED),
])
def test_exact_tokens_and_alias_rejection(units, reason):
    result = dc.execute(BINDING, _request(units=units))
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_REFUSAL, reason, None)


def test_role_kind_unit_bindings_are_exactly_the_governed_set():
    data = dc.load_artifact()
    record = _record(data)
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"]] == [
        ("P", "power", "W"), ("R_theta", "thermal_resistance", "K/W")]
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["output_roles"]] == [
        ("delta_T", "temperature_difference", "K")]
    by_token = {u["unit_token"]: u["quantity_kind"] for u in data["unit_records"]}
    assert by_token == {"N": "force", "mm": "length", "W": "power",
                        "K/W": "thermal_resistance", "K": "temperature_difference"}
    kinds = {k["quantity_kind"] for k in data["quantity_kinds"]}
    assert "temperature" not in kinds and not any("celsius" in k for k in kinds)


def test_closed_inventory_is_exactly_the_two_admitted_methods():
    assert dc.ADMITTED_METHODS == frozenset({
        ("cap13:static_reactions_two_support", "1.0"),
        ("therm01:conduction_temperature_difference_single_path", "1.0")})
    assert dc.ADMITTED_QUANTITY_KINDS == frozenset({
        "force", "length", "power", "thermal_resistance", "temperature_difference"})
    assert dc.ADMITTED_UNIT_TOKENS == frozenset({"N", "mm", "W", "K/W", "K"})
    assert dc.IMPLEMENTATION_VERSION == "1.1.0"
    data = dc.load_artifact()
    assert data["artifact_version"] == "2"
    assert [m["method_id"] for m in data["methods"]] == [
        "cap13:static_reactions_two_support",
        "therm01:conduction_temperature_difference_single_path"]


def test_both_bindings_are_isolated_from_each_other():
    # each binding executes ONLY its own method's record
    assert dc.execute(BINDING, _cap13_request())["reason"] == dc.OPERATION_NOT_ADMITTED
    assert dc.execute(CAP13_BINDING, _request())["reason"] == dc.OPERATION_NOT_ADMITTED
    # a THERM-01 identity bound to the CAP-13 adapter (and vice versa) fails closed
    swapped = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION,
                             cap13_method.evaluate)
    assert dc.execute(swapped, _request())["reason"] == dc.EXECUTION_INTEGRITY_FAILURE
    swapped = dc.bind_method(cap13_method.METHOD_ID, cap13_method.METHOD_VERSION,
                             method.evaluate)
    assert dc.execute(swapped, _cap13_request())["reason"] \
        == dc.EXECUTION_INTEGRITY_FAILURE
    # one method's tokens never satisfy the other method's roles
    req = _cap13_request()
    req["inputs"]["P"]["unit"] = "W"
    assert dc.execute(CAP13_BINDING, req)["reason"] == dc.UNIT_NOT_ADMITTED
    req = _request(units=("N", "K/W"))
    assert dc.execute(BINDING, req)["reason"] == dc.UNIT_NOT_ADMITTED
    # and CAP-13 still succeeds exactly as before through its own binding
    cap13_result = dc.execute(CAP13_BINDING, _cap13_request())
    assert cap13_result["outputs"]["R_L"]["value"] == 750.0
    assert cap13_result["outputs"]["R_R"]["value"] == 250.0


def test_app_wires_exactly_two_immutable_bindings_and_no_registry():
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    assert app_source.count("_dcalc.bind_method(") == 2
    assert webapp._THERM01_TEMPERATURE_BINDING.adapter_identity \
        == "engine.therm01_conduction_method.evaluate"
    assert webapp._CAP13_REACTIONS_BINDING.adapter_identity \
        == "engine.cap13_static_reactions_method.evaluate"
    with pytest.raises(AttributeError):
        webapp._THERM01_TEMPERATURE_BINDING.method_id = "x"
    source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("importlib", "__import__", "getattr(", "eval(", "exec(",
                   "entry_points", "pkgutil", "globals()", "convert",
                   "celsius", "273.15"):
        assert banned.lower() not in source.lower(), banned
    # the docstring may say "not a registry"; no registry object is defined
    assert not re.search(r"^\s*_?\w*registry\w*\s*=", source, re.I | re.M)


def test_missing_and_extra_roles_and_identity():
    req = _request()
    del req["inputs"]["R_theta"]
    assert dc.execute(BINDING, req)["reason"] == dc.INPUT_MISSING
    req = _request()
    req["inputs"]["A"] = {"value": 1.0, "unit": "W"}
    assert dc.execute(BINDING, req)["reason"] == dc.OPERATION_NOT_ADMITTED
    assert dc.execute(BINDING, _request(method_version="1.1"))["reason"] \
        == dc.VERSION_MISMATCH
    stale = dc.bind_method(method.METHOD_ID, "0.9", method.evaluate)
    assert dc.execute(stale, _request())["reason"] == dc.VERSION_MISMATCH


def test_deterministic_identity_and_no_input_mutation():
    req = _request(P=12.5, R_theta=0.75, subject_ref="opaque")
    before = copy.deepcopy(req)
    first = dc.execute(BINDING, req)
    assert req == before and first == dc.execute(BINDING, req)
    assert re.fullmatch(r"[0-9a-f]{64}", first["result_identity"])
    assert (first["artifact_version"], first["implementation_version"]) == ("2", "1.1.0")
    assert first["subject_ref"] == "opaque"
    assert [q["source_ref"] for q in first["source_qualification"]] == ["THERM-S1"]
    assert sorted(u["unit_token"] for u in first["unit_records"]) == ["K", "K/W", "W"]


# ==========================================================================
# 3. owner artifact v2 and the THERM-01 artifact: integrity, tamper, sources
# ==========================================================================
def _owner_tamper(name):
    data = _owner_artifact()
    record = _record(data)
    units = {u["unit_token"]: u for u in data["unit_records"]}
    if name == "unit_token":
        units["K/W"]["unit_token"] = "°C/W"
    elif name == "alias_unit":
        data["unit_records"].append(dict(units["K"], record_id="dcu:U999",
                                         unit_token="degC"))
    elif name == "role_unit":
        record["input_roles"][1]["unit_token"] = "K"
    elif name == "absolute_temperature_kind":
        data["quantity_kinds"].append({"quantity_kind": "temperature",
                                       "dimension": "Theta"})
    elif name == "third_method":
        extra = copy.deepcopy(record)
        extra["method_id"] = "therm01:convection"
        data["methods"].append(extra)
    elif name == "therm_method_removed":
        data["methods"] = [m for m in data["methods"]
                           if m["method_id"] != method.METHOD_ID]
    elif name == "source_policy_removed":
        data["source_use_policies"] = [p for p in data["source_use_policies"]
                                       if p["record_id"] != "dcu:SU004"]
    elif name == "unit_policy_removed":
        data["source_use_policies"] = [p for p in data["source_use_policies"]
                                       if p["record_id"] != "dcu:SU003"]
    elif name == "source_ref_foreign":
        record["source_qualification"][0]["source_use_policy_ref"] = "THERM-SU-DOE"
    elif name == "inspection_basis":
        units["K"]["inspection_basis"] = "SELF_ASSERTED"
    elif name == "inspection_date":
        record["source_qualification"][0]["inspection_date"] = "recently"
    elif name == "condition":
        record["result_range"][0]["condition"] = "anything"
    return data


OWNER_TAMPERS = ["unit_token", "alias_unit", "role_unit", "absolute_temperature_kind",
                 "third_method", "therm_method_removed", "source_policy_removed",
                 "unit_policy_removed", "source_ref_foreign", "inspection_basis",
                 "inspection_date", "condition"]


@pytest.mark.parametrize("name", OWNER_TAMPERS)
def test_owner_artifact_v2_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(name))
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    for binding, request in ((BINDING, _request()), (CAP13_BINDING, _cap13_request())):
        result = dc.execute(binding, request, artifact_path=path)
        assert (result["state"], result["reason"], result["outputs"]) == (
            dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def test_owner_artifact_missing_is_source_unavailable(tmp_path):
    result = dc.execute(BINDING, _request(), artifact_path=tmp_path / "absent.json")
    assert (result["state"], result["reason"]) == (dc.STATE_UNABLE,
                                                   dc.SOURCE_UNAVAILABLE)


def test_owner_v2_keeps_the_cap13_records_unchanged():
    data = dc.load_artifact()
    units = {u["record_id"]: u for u in data["unit_records"]}
    for rid, token in (("dcu:U001", "N"), ("dcu:U002", "mm")):
        assert units[rid]["unit_token"] == token
        assert units[rid]["source_use_policy_ref"] == "dcu:SU001"
        assert units[rid]["doi"] == "10.6028/NIST.SP.811e2008"
    for rid, token in (("dcu:U003", "W"), ("dcu:U004", "K/W"), ("dcu:U005", "K")):
        assert units[rid]["unit_token"] == token
        assert units[rid]["source_use_policy_ref"] == "dcu:SU003"
        assert "Special Publication 330" in units[rid]["source_title"]
        assert units[rid]["edition"] == "2019 Edition"
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    assert set(policies) == {"dcu:SU001", "dcu:SU002", "dcu:SU003", "dcu:SU004"}
    assert "dcu:U001 and dcu:U002 only" in policies["dcu:SU001"]["inspection_reference"]
    assert policies["dcu:SU004"]["url"] == "https://www.energy.gov/web-policies"
    record = _record(data)
    assert [q["source_use_policy_ref"] for q in record["source_qualification"]] == [
        "dcu:SU004"]
    assert record["method_authority_artifact"] == {
        "artifact_id": therm.ARTIFACT_ID, "artifact_version": "1"}
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    assert "therm01_content_config" not in owner_source
    assert "cap13_content_config" not in owner_source


def test_no_runtime_cross_loading_between_authority_artifacts(monkeypatch, tmp_path):
    for module in (therm, method):
        text = Path(module.__file__).read_text(encoding="utf-8")
        assert "cap13" not in text.lower()
    from engine import cap13_static_reactions as cap13
    assert "therm01" not in Path(cap13.__file__).read_text(encoding="utf-8").lower()
    # THERM-01 still runs with the CAP-13 artifact absent, and vice versa
    monkeypatch.setattr(cap13, "ARTIFACT_PATH", tmp_path / "absent.json")
    assert _evaluate()["outcome"] == therm.OUTCOME_SUCCESS
    monkeypatch.undo()
    monkeypatch.setattr(therm, "ARTIFACT_PATH", tmp_path / "absent.json")
    assert dc.execute(CAP13_BINDING, _cap13_request())["state"] == dc.STATE_SUCCESS


def _therm_tamper(name):
    data = _therm_artifact()
    if name == "extra_field":
        data["rating"] = "safe"
    elif name == "version":
        data["method"]["method_version"] = "1.1"
    elif name == "declaration_removed":
        data["declarations"].pop()
    elif name == "declarations_merged":
        data["declarations"][2]["accepted_value"] += " through one constant area"
        del data["declarations"][3]
    elif name == "refusal_changed":
        data["declarations"][0]["refusal"] = "NOT_DECLARED"
    elif name == "screen_removed":
        data["screen_items"].pop()
    elif name == "disclosure_item_removed":
        data["disclosure"].pop()
    elif name == "policy_removed":
        data["sources"] = [s for s in data["sources"]
                           if s["record_id"] != "THERM-SU-DOE"]
    elif name == "source_unbound":
        data["sources"][0]["source_use_policy_ref"] = "THERM-SU-NIST"
    elif name == "role_changed":
        data["numeric_domain"]["roles"][2]["unit_token"] = "°C"
    elif name == "declaration_meaning":
        data["declarations"][4]["accepted_value"] = "R_theta may be a datasheet value"
    elif name == "screen_meaning":
        data["screen_items"][0]["item"] = "a small battery"
    elif name == "disclosure_meaning":
        data["disclosure"][1] = "It is the component temperature."
    elif name == "derivation":
        data["method"]["derivation"] = "DOE states delta_T = P * R_theta."
    elif name == "numeric_rule":
        data["numeric_domain"]["rules"][1] = "P must not exceed 1000 W."
    elif name == "source_url":
        data["sources"][0]["url"] = "https://example.com/handbook"
    elif name == "artifact_version":
        data["artifact_version"] = "2"
    elif name == "schema":
        data["schema_version"] = "9"
    return data


THERM_TAMPERS = ["extra_field", "version", "declaration_removed", "declarations_merged",
                 "refusal_changed", "screen_removed", "disclosure_item_removed",
                 "policy_removed", "source_unbound", "role_changed",
                 "declaration_meaning", "screen_meaning", "disclosure_meaning",
                 "derivation", "numeric_rule", "source_url", "artifact_version",
                 "schema"]


@pytest.mark.parametrize("name", THERM_TAMPERS)
def test_therm01_artifact_tamper_fails_closed_before_any_calculation(name, monkeypatch):
    data = _therm_tamper(name)
    assert data != _therm_artifact()
    with pytest.raises(therm.Therm01KnowledgeError):
        therm.validate_artifact(data)
    called = []
    monkeypatch.setattr(therm._dc, "execute", lambda *a, **k: called.append(1) or {})
    result = therm.evaluate(_captured(), BINDING, artifact=data)
    assert result == {"outcome": therm.KNOWLEDGE_UNAVAILABLE, "owner_state": None,
                      "owner_reason": None, "result": None}
    assert not called


def test_therm01_semantic_pins_cover_every_governed_section():
    data = therm.load_artifact()
    assert set(therm._SEMANTIC_DIGESTS) == {
        "method", "numeric_domain", "declarations", "screen_items", "limitations",
        "disclosure", "sources"}
    for section, digest in therm._SEMANTIC_DIGESTS.items():
        assert therm._section_digest(data[section]) == digest


def test_therm01_artifact_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(therm, "ARTIFACT_PATH", tmp_path / "absent.json")
    assert _evaluate()["outcome"] == therm.KNOWLEDGE_UNAVAILABLE


def test_source_records_match_the_closed_section_11_qualification():
    data = therm.load_artifact()
    by_id = {r["record_id"]: r for r in data["sources"]}
    assert set(by_id) == {"THERM-S1", "THERM-U", "THERM-SU-DOE", "THERM-SU-NIST"}
    s1 = by_id["THERM-S1"]
    assert s1["url"] == "https://www.energy.gov/documents/doe-hdbk-1012-92vol2"
    assert "HT-02 page 9, equation (2-6)" in s1["source_title"]
    assert "status Archive; approved 1996-01-22; last updated 2014-12-29" \
        in s1["inspected_content"]
    assert "not established" in s1["inspected_content"]
    assert "InventorAI's own derivation" in s1["paraphrase_only_limitation"]
    assert by_id["THERM-SU-DOE"]["url"] == "https://www.energy.gov/web-policies"
    assert by_id["THERM-SU-DOE"]["inspection_date"] == "2026-10-09"
    assert by_id["THERM-U"]["url"] \
        == "https://www.nist.gov/pml/special-publication-330/sp-330-section-2"
    assert "PR006" in by_id["THERM-SU-DOE"]["inspected_content"]
    assert "not extended" in by_id["THERM-SU-NIST"]["inspected_content"]


# ==========================================================================
# 4. the consumer: grammar, §7 precedence, owner correspondence
# ==========================================================================
def test_success_through_the_consumer():
    result = _evaluate()
    assert result["outcome"] == therm.OUTCOME_SUCCESS
    assert result["result"]["outputs"]["delta_T"]["value"] == 25.0
    assert (result["owner_state"], result["owner_reason"]) == (dc.STATE_SUCCESS, None)


GRAMMAR_REJECTED = [
    "", "1,000", "1_000", "1e3", "1E3", "0x10", "10W", "10 W", "2.5K/W", "inf", "Inf",
    "nan", "NaN", "Infinity", "+5", "-5", "-0", " 5", "5 ", "\t5", "5\n", ".5", "5.",
    "1.2.3", "--5", "٥", "۵", "５", "5٠", "½", "1 000", "−5", "0b101", "5.0e0", "١٠٠٠",
    "9" * 65, "1." + "0" * 63,
]


@pytest.mark.parametrize("text", GRAMMAR_REJECTED)
@pytest.mark.parametrize("role", ["P", "R_theta"])
def test_strict_grammar_and_non_physical_length_cap(role, text):
    result = _evaluate(**{role: text})
    assert result == {"outcome": therm.INVALID_NUMERIC_INPUT, "owner_state": None,
                      "owner_reason": None, "result": None}


@pytest.mark.parametrize("role", ["P", "R_theta"])
@pytest.mark.parametrize("text", ["0", "0.0", "0.000"])
def test_zero_is_invalid_numeric_input(role, text):
    assert _evaluate(**{role: text})["outcome"] == therm.INVALID_NUMERIC_INPUT


def test_length_cap_is_inclusive_and_non_physical():
    sixty_four = "9" * 64
    assert therm.parse_number(sixty_four) == float(sixty_four)
    assert therm.parse_number("9" * 65) is None
    assert therm.MAX_VALUE_CHARS == 64
    # the largest admissible text pair stays finite: the cap is not a physical bound
    result = _evaluate(P="9" * 64, R_theta="9" * 64)
    assert result["outcome"] == therm.OUTCOME_SUCCESS


@pytest.mark.parametrize("decl", therm.DECLARATION_IDS)
def test_unanswered_declaration_is_not_declared(decl):
    assert _evaluate(decl={decl: ""})["outcome"] == therm.NOT_DECLARED


@pytest.mark.parametrize("item", therm.SCREEN_ITEMS)
def test_unanswered_screen_item_is_not_declared(item):
    assert _evaluate(screen={item: ""})["outcome"] == therm.NOT_DECLARED


@pytest.mark.parametrize("item", therm.SCREEN_ITEMS)
def test_any_screen_yes_abstains_without_calling_the_owner(item, monkeypatch):
    called = []
    monkeypatch.setattr(therm._dc, "execute", lambda *a, **k: called.append(1) or {})
    result = _evaluate(screen={item: therm.SCREEN_YES})
    assert result == {"outcome": therm.THERMAL_SPECIALIST_REVIEW_REQUIRED,
                      "owner_state": None, "owner_reason": None, "result": None}
    assert not called


@pytest.mark.parametrize("decl", therm.DECLARATION_IDS)
def test_each_declaration_refuses_path_not_supported(decl):
    result = _evaluate(decl={decl: therm.ANSWER_DOES_NOT_APPLY})
    assert result == {"outcome": therm.PATH_NOT_SUPPORTED, "owner_state": None,
                      "owner_reason": None, "result": None}


def test_section_7_precedence_first_failing_stage_wins():
    # completeness beats the screen, the screen beats declarations, declarations
    # beat numeric problems
    assert _evaluate(decl={"steady_state": ""}, screen={"cryogenic": "yes"},
                     P="abc")["outcome"] == therm.NOT_DECLARED
    assert _evaluate(screen={"cryogenic": "yes"},
                     decl={"constant_area": therm.ANSWER_DOES_NOT_APPLY},
                     P="abc")["outcome"] == therm.THERMAL_SPECIALIST_REVIEW_REQUIRED
    assert _evaluate(decl={"constant_area": therm.ANSWER_DOES_NOT_APPLY},
                     P="abc")["outcome"] == therm.PATH_NOT_SUPPORTED
    assert _evaluate(P="abc")["outcome"] == therm.INVALID_NUMERIC_INPUT


def test_owner_is_called_only_after_every_pre_owner_stage(monkeypatch):
    seen = []

    def fake(binding, request, artifact_path=None):
        seen.append(request)
        return {"state": dc.STATE_SUCCESS, "reason": None, "outputs": {}}
    monkeypatch.setattr(therm._dc, "execute", fake)
    _evaluate()
    assert seen == [{"method_id": method.METHOD_ID,
                     "method_version": method.METHOD_VERSION,
                     "inputs": {"P": {"value": 10.0, "unit": "W"},
                                "R_theta": {"value": 2.5, "unit": "K/W"}},
                     "subject_ref": None}]


ALL_OWNER_PAIRS = [(dc.REASON_STATE[r], r) for r in sorted(dc.REASON_STATE)]


@pytest.mark.parametrize("state,reason", ALL_OWNER_PAIRS)
def test_every_owner_state_maps_per_section_7_and_is_preserved(state, reason,
                                                               monkeypatch):
    monkeypatch.setattr(therm._dc, "execute",
                        lambda *a, **k: {"state": state, "reason": reason,
                                         "outputs": None})
    expected = therm.OWNER_CORRESPONDENCE.get((state, reason),
                                              therm.UNMAPPED_OWNER_OUTCOME)
    assert _evaluate() == {"outcome": expected, "owner_state": state,
                           "owner_reason": reason, "result": None}


def test_section_7_correspondence_table_is_exact():
    assert therm.OWNER_CORRESPONDENCE == {
        ("REFUSAL", "INVALID_NUMERIC_INPUT"): "INVALID_NUMERIC_INPUT",
        ("REFUSAL", "UNIT_NOT_ADMITTED"): "UNIT_NOT_SUPPORTED",
        ("REFUSAL", "UNKNOWN_UNIT"): "UNIT_NOT_SUPPORTED",
        ("REFUSAL", "METHOD_NOT_REGISTERED"): "KNOWLEDGE_UNAVAILABLE",
        ("REFUSAL", "VERSION_MISMATCH"): "KNOWLEDGE_UNAVAILABLE",
        ("UNABLE_TO_DETERMINE", "SOURCE_UNAVAILABLE"): "KNOWLEDGE_UNAVAILABLE",
        ("FAILURE", "EXECUTION_INTEGRITY_FAILURE"): "KNOWLEDGE_UNAVAILABLE",
    }


def test_reachable_real_owner_states_through_the_consumer(tmp_path):
    captured = _captured()
    r = therm.evaluate(captured, BINDING, owner_artifact_path=tmp_path / "x.json")
    assert (r["outcome"], r["owner_state"], r["owner_reason"]) == (
        therm.KNOWLEDGE_UNAVAILABLE, dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE)
    path = _write(tmp_path, _owner_tamper("unit_token"), "t.json")
    r = therm.evaluate(captured, BINDING, owner_artifact_path=path)
    assert (r["outcome"], r["owner_state"], r["owner_reason"], r["result"]) == (
        therm.KNOWLEDGE_UNAVAILABLE, dc.STATE_FAILURE,
        dc.EXECUTION_INTEGRITY_FAILURE, None)
    stale = dc.bind_method(method.METHOD_ID, "0.9", method.evaluate)
    r = therm.evaluate(captured, stale)
    assert (r["outcome"], r["owner_state"], r["owner_reason"]) == (
        therm.KNOWLEDGE_UNAVAILABLE, dc.STATE_REFUSAL, dc.VERSION_MISMATCH)


@pytest.mark.parametrize("form", [
    {"value_P": ["1"], "extra": ["x"]},
    {"value_P": ["1", "2"]},
    {"decl_steady_state": ["yes"]},
    {"decl_steady_state": ["APPLIES"]},
    {"screen_cryogenic": ["applies"]},
    {"screen_cryogenic": ["No"]},
    {"value_P": [1]},
    {"value_P": "1"},
    {"value_L": ["1"]},
    [],
])
def test_malformed_capture(form):
    assert therm.capture_form(form) is None


def test_eligibility_is_electrical_electronics_root_only():
    assert therm.is_eligible("electronics_electrical")
    for value in (None, "", "mechanical", "Electronics_Electrical", "control_loop",
                  " electronics_electrical", ["electronics_electrical"], "electrical"):
        assert not therm.is_eligible(value)


def test_format_value_applies_no_rounding():
    for value in (25.0, 0.1 * 3.0, 1e-300, 2.0 / 3.0):
        assert float(therm.format_value(value)) == value
    assert therm.format_value(0.1 * 3.0) == "0.30000000000000004"


def test_consumer_is_separate_and_reads_no_project_state():
    for module in (therm, method):
        imports = re.findall(r"^\s*(?:from|import)\s+([\w.]+)",
                             Path(module.__file__).read_text(encoding="utf-8"), re.M)
        for banned in ("record_store", "flask", "web", "safety_signal",
                       "requirement_quantity", "socket", "urllib", "requests",
                       "random", "secrets", "time", "datetime", "uuid", "cap13"):
            assert all(banned != n and not n.startswith(banned + ".")
                       and "cap13" not in n for n in imports), (module.__name__, banned)


# ==========================================================================
# 5. EN / AR fidelity to the contract (§9 / §9A)
# ==========================================================================
def test_english_wording_equals_the_artifact():
    content = therm.load_artifact()
    assert ui_text.text("UI_THERM01_DISCLOSURE", "en").split("\n\n") \
        == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"].replace("R_theta", "Rθ")
        expected = value[0].upper() + value[1:] + "."
        assert ui_text.text("UI_THERM01_DECL_" + entry["declaration_id"].upper(),
                            "en") == expected
    for entry in content["screen_items"]:
        expected = entry["item"][0].upper() + entry["item"][1:]
        assert ui_text.text("UI_THERM01_SCREEN_" + entry["item_id"].upper(),
                            "en") == expected


def test_english_disclosure_carries_every_section_9_requirement():
    text = " ".join(therm.load_artifact()["disclosure"])
    for phrase in ("steady-state, single-path, uniform one-dimensional and constant-area",
                   "your own P and Rθ", "not a component, junction, case, surface or "
                   "ambient temperature", "not compared with any rating, limit or margin",
                   "safe, acceptable, suitable, compliant or reliable",
                   "UNVALIDATED and not evidence", "measurement or a thermal specialist",
                   "does not check Rθ", "datasheet figure applies only",
                   "Convection, radiation, spreading, transient behaviour",
                   "archived; historical fundamentals reference only",
                   "InventorAI's own derivation"):
        assert phrase in text, phrase


def test_arabic_wording_is_contract_9a_verbatim():
    a1 = _contract_section("**A-1", "Parity with §9")
    assert ui_text.text("UI_THERM01_DISCLOSURE", "ar").split("\n\n") \
        == _numbered_quote_items(a1)
    a2_section = _contract_section("**A-2", "**A-3")
    a2 = _table(a2_section)
    labels = dict(zip(therm.DECLARATION_IDS, (
        "D-1 condition", "D-2 heat path", "D-3 heat-flow geometry", "D-4 area",
        "D-5 resistance meaning", "D-6 resistance constancy")))
    for decl, label in labels.items():
        assert ui_text.text("UI_THERM01_DECL_" + decl.upper(), "ar") == a2[label], decl
    assert ui_text.text("UI_THERM01_DATASHEET_NOTE", "ar") \
        == _guillemet(a2_section, "Datasheet note")
    a3_section = _contract_section("**A-3", "**A-4")
    a3 = _table(a3_section)
    for index, item in enumerate(therm.SCREEN_ITEMS, start=1):
        assert ui_text.text("UI_THERM01_SCREEN_" + item.upper(), "ar") \
            == a3[str(index)], item
    assert ui_text.text("UI_THERM01_SCREEN_STEM", "ar") == _guillemet(a3_section, "Stem:")
    assert ui_text.text("UI_THERM01_SCREEN_NOTE", "ar") \
        == _guillemet(a3_section, "Screen note")
    a4_section = _contract_section("**A-4", "The unmapped-outcome line")
    a4 = _table(a4_section)
    for outcome in ("NOT_DECLARED", "PATH_NOT_SUPPORTED", "INVALID_NUMERIC_INPUT",
                    "UNIT_NOT_SUPPORTED", "KNOWLEDGE_UNAVAILABLE"):
        assert ui_text.text("UI_THERM01_OUTCOME_" + outcome, "ar") == a4[outcome]
    assert ui_text.text("UI_THERM01_OUTCOME_THERMAL_SPECIALIST_REVIEW_REQUIRED", "ar") \
        == a4["THERMAL SPECIALIST REVIEW REQUIRED"]
    assert ui_text.text("UI_THERM01_OUTCOME_UNMAPPED_OWNER_OUTCOME", "ar") \
        == a4["Owner outcome not mapped by §7 (no reason token)"]
    assert ui_text.text("UI_THERM01_UNABLE_HEADING", "ar") \
        == _guillemet(a4_section, "The refusal display heading")
    a5 = _table(_contract_section("**A-5", "**A-6"))
    pairs = {"LINK_TEXT": "Session-page link", "LINK_NOTE": "Link note",
             "TITLE": "Page title", "INTRO": "Page intro", "FIELD_P": "P input",
             "FIELD_R_THETA": "Rθ input", "SUBMIT": "Submit",
             "RESULT_DELTA_T": "ΔT result", "STATUS": "Status",
             "ECHO_HEADING": "Echoed inputs heading", "METHOD_LINE": "Method line",
             "SOURCES_HEADING": "Sources heading", "SOURCES_NOTE": "Sources note",
             "BACK": "Back link",
             "SCOPE_NOTE": "Eligibility note (Electrical / Electronics first slice)"}
    a5 = {k.replace("` input", " input").replace("` result", " result"): v
          for k, v in a5.items()}
    for key, row in pairs.items():
        assert ui_text.text("UI_THERM01_" + key, "ar") == a5[row], key
    applies, does_not = a5["Declaration answers"].split(" / ")
    assert (ui_text.text("UI_THERM01_ANSWER_APPLIES", "ar"),
            ui_text.text("UI_THERM01_ANSWER_DOES_NOT_APPLY", "ar")) == (applies, does_not)
    yes, no = a5["Screen answers"].split(" / ")
    assert (ui_text.text("UI_THERM01_SCREEN_YES", "ar"),
            ui_text.text("UI_THERM01_SCREEN_NO", "ar")) == (yes, no)


def test_every_therm01_string_is_bilingual_and_carries_no_verdict_wording():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_THERM01_")]
    assert len(keys) == 48
    for key in keys:
        entry = ui_text.UI_STRINGS[key]
        assert entry.get("en") and entry.get("ar"), key
        assert re.search(r"[؀-ۿ]", entry["ar"]), key
        # the accepted screen note negates safety explicitly; that negation is allowed
        low = entry["en"].lower()
        for negation in ("never means that anything is safe",
                         "says nothing about whether anything is safe"):
            low = low.replace(negation, "")
        for word in ("is safe", "is adequate", "approved", "certified", "passes",
                     "recommended", "you can rely", "°c", "celsius", "junction temperature is"):
            assert word not in low, (key, word)


# ==========================================================================
# 6. the web slice: eligibility, request integrity, isolation, no persistence
# ==========================================================================
def test_route_in_r05_inventory():
    from tests.test_r05_request_integrity import MUTATIONS
    assert "/session/<sid>/temperature-difference" in MUTATIONS


def test_link_offered_on_electrical_electronics_only(elec, mech):
    c, _aid, sid = elec
    assert "data-therm01-link" in _page(c, sid)
    c2, _aid2, sid2 = mech
    assert "data-therm01-link" not in _page(c2, sid2)


def test_get_shows_an_unanswered_form(elec):
    c, _aid, sid = elec
    r = c.get(URL % sid)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    body = r.get_data(as_text=True)
    assert "data-therm01-form" in body and " checked" not in body
    assert body.count('type="radio"') == 2 * (6 + 10)
    for role in ("P", "R_theta"):
        assert re.search(r'name="value_%s"[^>]*maxlength="64"[^>]*value=""' % role, body)
    assert "data-therm01-result" not in body and "data-therm01-outcome" not in body
    assert "data-therm01-datasheet-note" in body


def test_post_success_renders_in_the_same_request(elec):
    c, _aid, sid = elec
    r = c.post(URL % sid, data=_form(P="10", R_theta="2.5"))
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    assert "Location" not in r.headers
    body = r.get_data(as_text=True)
    assert re.findall(r'data-therm01-result-value><bdi dir="ltr">([^<]+)</bdi>',
                      body) == ["25.0 K"]
    assert "therm01:conduction_temperature_difference_single_path" in body
    assert "UNVALIDATED" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_THERM01_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert re.findall(r'data-therm01-echo-value>([^<]*)<', body) == ["10", "2.5"]
    assert "DOE-HDBK-1012/2-92" in body and "NIST Special Publication 330" in body


@pytest.mark.parametrize("over,outcome", [
    ({"R_theta": "0"}, "INVALID_NUMERIC_INPUT"),
    ({"screen": {"mains_or_high_voltage": "yes"}}, "THERMAL_SPECIALIST_REVIEW_REQUIRED"),
    ({"decl": {"constant_area": "does_not_apply"}}, "PATH_NOT_SUPPORTED"),
    ({"decl": {"steady_state": ""}}, "NOT_DECLARED"),
])
def test_post_non_success_shows_one_reason_and_no_number(elec, over, outcome):
    c, _aid, sid = elec
    r = c.post(URL % sid, data=_form(**over))
    body = r.get_data(as_text=True)
    assert r.status_code == 200
    assert html.escape(ui_text.text("UI_THERM01_OUTCOME_" + outcome, "en"),
                       quote=False) in body
    assert ui_text.text("UI_THERM01_UNABLE_HEADING", "en") in body
    assert "data-therm01-result" not in body and body.count("data-therm01-outcome") == 1


def test_raw_echo_is_escaped_and_same_request_only(elec):
    c, _aid, sid = elec
    r = c.post(URL % sid, data=_form(P="<b>1</b>"))
    body = r.get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body
    assert "&lt;b&gt;" not in c.get(URL % sid).get_data(as_text=True)


def test_malformed_request_is_400_without_a_reason_token(elec):
    c, _aid, sid = elec
    r = c.post(URL % sid, data=dict(_form(), unexpected="1"))
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert ui_text.text("UI_THERM01_ERR_REQUEST", "en") in body
    assert "data-therm01-outcome" not in body and "data-therm01-result" not in body
    assert c.post(URL % sid, data=dict(_form(), decl_steady_state="yes")).status_code \
        == 400


def test_ineligible_project_is_never_evaluated(mech, monkeypatch):
    c, _aid, sid = mech
    called = []
    monkeypatch.setattr(webapp._therm01, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-therm01-scope-note" in body
        assert "data-therm01-form" not in body and "data-therm01-outcome" not in body
    assert not called


def test_csrf_is_enforced():
    c = webapp.app.test_client()
    assert c.post(URL % "not-a-project", data=_form()).status_code == 403


def test_another_account_and_anonymous_callers_are_denied(elec):
    _c, _aid, sid = elec
    other, _ = _client_for("therm01-other@example.com")
    anon = _new_client()
    for client in (other, anon):
        for response in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert response.status_code == 302
            assert "data-therm01" not in response.get_data(as_text=True)


@pytest.mark.parametrize("over", [{}, {"R_theta": "-3"}, {"P": "abc"},
                                  {"screen": {"cryogenic": "yes"}}])
def test_nothing_is_persisted_and_no_project_state_moves(elec, over):
    c, _aid, sid = elec
    _page(c, sid)                       # consume any one-shot start notice
    before = _snapshot(c)               # the whole database and SESSION_STORE
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_no_safety_signal_report_export_or_api_surface():
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    start = app_source.index("# Stage 27 / THERM-01 — Single-Path Temperature-Difference")
    section = app_source[start:app_source.index("# Manufacturing Evidence Capture", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store().save", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/", "_cap13"):
        assert banned not in section, banned
    routes = [r.rule for r in webapp.app.url_map.iter_rules()
              if "temperature-difference" in r.rule]
    assert routes == ["/session/<sid>/temperature-difference"] * 2
    for template in ("deliverable.html", "report.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "therm01" not in path.read_text(encoding="utf-8")


def test_arabic_page_is_rtl_and_isolates_tokens(elec):
    c, _aid, sid = elec
    c.post("/ui-language", data={"lang": "ar"})
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert 'dir="rtl"' in body
    for token in ("P", "Rθ", "ΔT", "W", "K/W", "K", "UNVALIDATED", "NOT EVIDENCE"):
        assert '(<bdi dir="ltr">%s</bdi>)' % html.escape(token) in body, token
    assert '<bdi dir="ltr">therm01:conduction_temperature_difference_single_path</bdi>' \
        in body
    assert '<bdi dir="ltr">25.0 K</bdi>' in body
    assert 'بـ<bdi dir="ltr">InventorAI</bdi>' in body
    assert '(<bdi dir="ltr">U.S. DOE Fundamentals Handbook</bdi>)' in body
    stripped = re.sub(r"<[^>]+>", "", body)
    for item in ui_text.text("UI_THERM01_DISCLOSURE", "ar").split("\n\n"):
        assert item in stripped
    for role in ("P", "R_theta"):
        assert re.search(r'name="value_%s" dir="ltr"' % role, body)
