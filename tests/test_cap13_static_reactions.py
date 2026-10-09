# -*- coding: utf-8 -*-
"""Stage 25 / CAP-13 - Two-Support Static Reactions, Slice 1 (directly owning tests).

ONE shared deterministic calculation / units owner (``engine/deterministic_calculation.py``),
ONE method (``cap13:static_reactions_two_support`` 1.0, ``engine/cap13_static_reactions_method.py``)
and ONE CAP-13 consumer (``engine/cap13_static_reactions.py`` + the request-local web page).

The tests press on the locked boundaries of the A-5 authorization and the method
contract (§§5-12B): exact numerical values and endpoints, the strict ASCII
grammar, the pre-owner precedence of §12A, the §8 owner-state correspondence
(owner FAILURE is never remapped to REFUSAL), artifact fail-closed behaviour,
ownership separation (the owner never imports CAP-13 and reads no project
state), no persistence, and EN / AR fidelity to the contract text.
"""
import copy
import html
import inspect
import json
import math
import re
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import cap13_static_reactions as cap13
from engine import cap13_static_reactions_method as method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = (ROOT / "docs" / "governance"
            / "STAGE25_CAP13_TWO_SUPPORT_STATIC_REACTIONS_METHOD_CONTRACT.md")
URL = "/session/%s/support-reactions"
BINDING = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, method.evaluate)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _request(P=1000.0, L=2000.0, x=500.0, units=("N", "mm", "mm"), **over):
    req = {"method_id": method.METHOD_ID, "method_version": method.METHOD_VERSION,
           "inputs": {"P": {"value": P, "unit": units[0]},
                      "L": {"value": L, "unit": units[1]},
                      "x": {"value": x, "unit": units[2]}},
           "subject_ref": None}
    req.update(over)
    return req


def _form(P="1000", L="2000", x="500", decl=None, screen=None):
    form = {cap13.DECLARATION_FIELD % d: cap13.ANSWER_MATCHES
            for d in cap13.DECLARATION_IDS}
    form.update({cap13.SCREEN_FIELD % s: cap13.SCREEN_NO for s in cap13.SCREEN_ITEMS})
    form.update({cap13.VALUE_FIELD % "P": P, cap13.VALUE_FIELD % "L": L,
                 cap13.VALUE_FIELD % "x": x})
    for key, value in (decl or {}).items():
        form[cap13.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[cap13.SCREEN_FIELD % key] = value
    return form


def _evaluate(**kw):
    captured = cap13.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return cap13.evaluate(captured, BINDING)


def _owner_artifact():
    return json.loads(dc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _cap13_artifact():
    return json.loads(cap13.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _write(tmp_path, data, name="a.json"):
    target = tmp_path / name
    target.write_text(json.dumps(data), encoding="utf-8")
    return target


def _fake_adapter(result):
    def evaluate(P, L, x):
        if isinstance(result, Exception):
            raise result
        return result
    evaluate.__module__ = method.evaluate.__module__
    evaluate.__qualname__ = method.evaluate.__qualname__
    return evaluate


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


def _blockquote_paragraphs(section):
    paragraphs, current = [], []
    for line in section.splitlines():
        if not line.startswith(">"):
            continue
        content = line[1:].strip()
        if content:
            current.append(content)
        elif current:
            paragraphs.append(_norm(" ".join(current)))
            current = []
    if current:
        paragraphs.append(_norm(" ".join(current)))
    return paragraphs


@pytest.fixture
def mech():
    c, aid = _client_for("cap13-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": "mechanical"})


@pytest.fixture
def elec():
    c, aid = _client_for("cap13-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


# ==========================================================================
# 1. the method: numerical values, endpoints, no subtraction
# ==========================================================================
def test_interior_numerical_value():
    result = dc.execute(BINDING, _request())
    assert result["state"] == dc.STATE_SUCCESS and result["reason"] is None
    assert result["outputs"]["R_L"] == {"value": 750.0, "unit": "N",
                                        "provenance": "CALCULATED"}
    assert result["outputs"]["R_R"] == {"value": 250.0, "unit": "N",
                                        "provenance": "CALCULATED"}
    assert result["validation_status"] == "UNVALIDATED"


@pytest.mark.parametrize("x,left,right", [(0.0, 1000.0, 0.0), (2000.0, 0.0, 1000.0)])
def test_endpoints_are_exact_and_valid(x, left, right):
    result = dc.execute(BINDING, _request(x=x))
    assert result["state"] == dc.STATE_SUCCESS
    assert result["outputs"]["R_L"]["value"] == left
    assert result["outputs"]["R_R"]["value"] == right
    assert math.copysign(1.0, result["outputs"]["R_L"]["value"]) == 1.0
    assert math.copysign(1.0, result["outputs"]["R_R"]["value"]) == 1.0


def test_each_reaction_is_computed_independently_never_by_subtraction():
    source = inspect.getsource(method.evaluate)
    assert "P - " not in source and "P-" not in source
    assert "- reaction" not in source and "-reaction" not in source
    assert "isclose" not in source and "tolerance" not in source.lower()
    assert "ratio_right = x / L" in source and "ratio_left = (L - x) / L" in source
    # a value whose subtraction form would differ from the ratio form
    P, L, x = 0.3, 0.7, 0.1
    out = method.evaluate(P, L, x)
    assert out["R_R"] == P * (x / L) and out["R_L"] == P * ((L - x) / L)


def test_interior_collapse_and_non_finite_fail_as_owner_failure():
    # subnormal weight: an interior reaction rounds to zero -> integrity failure
    result = dc.execute(BINDING, _request(P=5e-324, L=1.0, x=0.5))
    assert (result["state"], result["reason"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE)
    assert result["outputs"] is None
    with pytest.raises(ArithmeticError):
        method.evaluate(1e308, 1e-308, 1e300)          # non-finite intermediate
    with pytest.raises(ArithmeticError):
        method.evaluate(float("inf"), 1.0, 0.5)       # non-finite reaction


@pytest.mark.parametrize("produced", [
    {"R_L": float("inf"), "R_R": 0.0},                  # overflow / non-finite
    {"R_L": float("nan"), "R_R": 0.0},
    {"R_L": 2000.0, "R_R": 0.0},                        # out of the [0, P] range
    {"R_L": -1.0, "R_R": 1001.0},
    {"R_L": 750, "R_R": 250.0},                         # not a float
    {"R_L": 750.0},                                     # missing output role
    {"R_L": 750.0, "R_R": 250.0, "M": 0.0},             # extra output role
    "not a mapping",
    OverflowError("tamper"),
    ZeroDivisionError("tamper"),
])
def test_bad_or_tampered_adapter_output_is_owner_failure(produced):
    binding = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION,
                             _fake_adapter(produced))
    result = dc.execute(binding, _request())
    assert (result["state"], result["reason"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE)
    assert result["outputs"] is None and "inputs" not in result


# ==========================================================================
# 2. the owner: numeric admission, exact units, roles, identity
# ==========================================================================
@pytest.mark.parametrize("value", [True, False, float("nan"), float("inf"),
                                   float("-inf"), "1000", None, [1.0], 10 ** 400])
@pytest.mark.parametrize("role", ["P", "L", "x"])
def test_bool_nan_infinity_and_non_numbers_refused_at_the_owner(role, value):
    req = _request()
    req["inputs"][role]["value"] = value
    result = dc.execute(BINDING, req)
    assert (result["state"], result["reason"]) == (
        dc.STATE_REFUSAL, dc.INVALID_NUMERIC_INPUT)
    assert result["outputs"] is None


@pytest.mark.parametrize("units,reason", [
    (("mm", "mm", "mm"), dc.UNIT_NOT_ADMITTED),
    (("N", "N", "mm"), dc.UNIT_NOT_ADMITTED),
    (("N", "mm", "N"), dc.UNIT_NOT_ADMITTED),
    (("kN", "mm", "mm"), dc.UNKNOWN_UNIT),
    (("N", "m", "mm"), dc.UNKNOWN_UNIT),
    (("newton", "mm", "mm"), dc.UNKNOWN_UNIT),
    (("n", "mm", "mm"), dc.UNKNOWN_UNIT),
    (("N ", "mm", "mm"), dc.UNKNOWN_UNIT),
    (("N", "MM", "mm"), dc.UNKNOWN_UNIT),
    (("N", "millimetre", "mm"), dc.UNKNOWN_UNIT),
    ((1, "mm", "mm"), dc.UNKNOWN_UNIT),
])
def test_exact_unit_tokens_only_no_alias_no_conversion(units, reason):
    result = dc.execute(BINDING, _request(units=units))
    assert (result["state"], result["reason"]) == (dc.STATE_REFUSAL, reason)
    assert result["outputs"] is None


def _cap13_record(data):
    # Correction 02 (calc / units contract §13A): the shared owner artifact now carries
    # exactly two method records; CAP-13 selects its own record by identity
    (record,) = [r for r in data["methods"] if r["method_id"] == method.METHOD_ID]
    return record


def test_role_kind_unit_bindings_are_exactly_the_governed_set():
    data = dc.load_artifact()
    record = _cap13_record(data)
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["input_roles"]] == [
        ("P", "force", "N"), ("L", "length", "mm"), ("x", "length", "mm")]
    assert [(r["role"], r["quantity_kind"], r["unit_token"])
            for r in record["output_roles"]] == [
        ("R_L", "force", "N"), ("R_R", "force", "N")]
    assert sorted(u["unit_token"] for u in data["unit_records"]) == [
        "K", "K/W", "N", "W", "mm"]
    assert sorted(k["quantity_kind"] for k in data["quantity_kinds"]) == [
        "force", "length", "power", "temperature_difference", "thermal_resistance"]


def test_missing_and_extra_roles():
    req = _request()
    del req["inputs"]["x"]
    assert dc.execute(BINDING, req)["reason"] == dc.INPUT_MISSING
    req = _request()
    req["inputs"]["Q"] = {"value": 1.0, "unit": "N"}
    assert dc.execute(BINDING, req)["reason"] == dc.OPERATION_NOT_ADMITTED


def test_owner_domain_is_defence_in_depth():
    for kw in ({"x": -1.0}, {"x": 2000.5}, {"P": 0.0}, {"L": -1.0}):
        result = dc.execute(BINDING, _request(**kw))
        assert (result["state"], result["reason"]) == (
            dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE)
        assert result["outputs"] is None


def test_identity_version_and_binding_integrity():
    assert dc.execute(BINDING, _request(method_id="cap13:other"))["reason"] \
        == dc.OPERATION_NOT_ADMITTED
    assert dc.execute(BINDING, _request(method_version="1.1"))["reason"] \
        == dc.VERSION_MISMATCH
    stale = dc.bind_method(method.METHOD_ID, "0.9", method.evaluate)
    assert dc.execute(stale, _request())["reason"] == dc.VERSION_MISMATCH
    unknown = dc.bind_method("cap13:unknown", "1.0", method.evaluate)
    result = dc.execute(unknown, _request(method_id="cap13:unknown"))
    assert (result["state"], result["reason"]) == (
        dc.STATE_REFUSAL, dc.METHOD_NOT_REGISTERED)

    def evaluate(P, L, x):  # a different callable under the right method id
        return {"R_L": 0.0, "R_R": P}
    wrong = dc.bind_method(method.METHOD_ID, method.METHOD_VERSION, evaluate)
    result = dc.execute(wrong, _request())
    assert (result["state"], result["reason"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE)
    assert dc.execute(object(), _request())["reason"] == dc.OPERATION_NOT_ADMITTED
    assert dc.execute(BINDING, {"method_id": method.METHOD_ID})["reason"] \
        == dc.OPERATION_NOT_ADMITTED


def test_binding_is_immutable_and_not_a_registry():
    with pytest.raises(AttributeError):
        BINDING.method_id = "x"
    with pytest.raises(AttributeError):
        BINDING._adapter = None
    with pytest.raises(AttributeError):
        del BINDING._method_id
    assert BINDING.adapter_identity == "engine.cap13_static_reactions_method.evaluate"
    source = Path(dc.__file__).read_text(encoding="utf-8")
    for banned in ("importlib", "__import__", "getattr(", "eval(", "exec(",
                   "entry_points", "pkgutil", "globals()", "REGISTRY"):
        assert banned not in source, banned
    # the app wires exactly ONE CAP-13 binding, to the method's own function; the
    # only other binding is THERM-01's (Correction 02: one immutable binding per method)
    assert webapp._CAP13_REACTIONS_BINDING.adapter_identity == BINDING.adapter_identity
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    assert app_source.count("_dcalc.bind_method(") == 2


def test_deterministic_identity_and_no_input_mutation():
    req = _request(P=123.456, L=789.0, x=12.5, subject_ref="opaque")
    before = copy.deepcopy(req)
    first = dc.execute(BINDING, req)
    second = dc.execute(BINDING, req)
    assert req == before
    assert first == second
    assert re.fullmatch(r"[0-9a-f]{64}", first["result_identity"])
    assert first["subject_ref"] == "opaque"
    assert first["inputs"]["P"] == {"value": 123.456, "unit": "N",
                                    "provenance": "OWNER_STATED"}
    other = dc.execute(BINDING, _request(P=123.457, L=789.0, x=12.5,
                                         subject_ref="opaque"))
    assert other["result_identity"] != first["result_identity"]
    for key in ("method_id", "method_version", "artifact_id", "artifact_version",
                "implementation_version"):
        assert first[key]


def test_owner_is_separate_from_cap13_and_from_project_state():
    source = Path(dc.__file__).read_text(encoding="utf-8")
    imports = re.findall(r"^\s*(?:from|import)\s+([\w.]+)", source, re.M)
    assert all("cap13" not in name for name in imports)
    for banned in ("record_store", "SESSION_STORE", "flask", "web.", "idea_state",
                   "safety_signal", "requirement_quantity", "socket", "urllib",
                   "requests", "random", "secrets", "time", "datetime", "uuid"):
        assert all(banned != name and not name.startswith(banned + ".")
                   for name in imports), banned
    for module in (method, cap13):
        mod_imports = re.findall(r"^\s*(?:from|import)\s+([\w.]+)",
                                 Path(module.__file__).read_text(encoding="utf-8"),
                                 re.M)
        for banned in ("record_store", "flask", "web", "safety_signal",
                       "requirement_quantity", "socket", "urllib", "requests",
                       "random", "secrets", "time", "datetime", "uuid"):
            assert all(banned != n and not n.startswith(banned + ".")
                       for n in mod_imports), (module.__name__, banned)
    method_imports = re.findall(r"^\s*(?:from|import)\s+([\w.]+)",
                                Path(method.__file__).read_text(encoding="utf-8"), re.M)
    assert method_imports == ["math"]


# ==========================================================================
# 3. the two governed artifacts: presence, tamper, version, source-use
# ==========================================================================
def test_both_artifacts_load_and_cross_reference_without_circular_loading(
        monkeypatch, tmp_path):
    owner = dc.load_artifact()
    content = cap13.load_artifact()
    record = _cap13_record(owner)
    assert record["method_id"] == content["method"]["method_id"] == method.METHOD_ID
    assert record["method_version"] == content["method"]["method_version"] == "1.0"
    assert record["method_authority_artifact"] == {
        "artifact_id": content["artifact_id"],
        "artifact_version": content["artifact_version"]}
    # the owner executes without the CAP-13 artifact existing at all
    monkeypatch.setattr(cap13, "ARTIFACT_PATH", tmp_path / "absent.json")
    assert dc.execute(BINDING, _request())["state"] == dc.STATE_SUCCESS
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    assert "cap13_content_config" not in owner_source


def test_source_use_records_are_present_and_bound():
    content = cap13.load_artifact()
    by_id = {r["record_id"]: r for r in content["sources"]}
    policy = by_id["cap13:SU001"]
    assert policy["record_type"] == "source_use_policy"
    assert policy["url"] == "https://sti.nasa.gov/disclaimers/"
    for ref in ("NASA-S1", "NASA-S2"):
        assert by_id[ref]["source_use_policy_ref"] == "cap13:SU001"
        assert by_id[ref]["url"].startswith("https://www1.grc.nasa.gov/")
    owner = dc.load_artifact()
    policies = {p["record_id"] for p in owner["source_use_policies"]}
    # dcu:SU001 binds the NIST unit records N / mm; dcu:SU002 is the owner-local,
    # version-bound snapshot that the CAP-13 source qualification resolves to;
    # dcu:SU003 / dcu:SU004 are THERM-01's own (Correction 02) and bind nothing of CAP-13
    assert policies == {"dcu:SU001", "dcu:SU002", "dcu:SU003", "dcu:SU004"}
    cap13_units = [u for u in owner["unit_records"] if u["unit_token"] in ("N", "mm")]
    assert len(cap13_units) == 2
    for unit in cap13_units:
        assert unit["source_use_policy_ref"] == "dcu:SU001"
        assert unit["doi"] == "10.6028/NIST.SP.811e2008"
    record = _cap13_record(owner)
    assert [q["source_ref"] for q in record["source_qualification"]] == [
        "NASA-S1", "NASA-S2"]


def _owner_tamper(name):
    data = _owner_artifact()
    record = _cap13_record(data)
    if name == "extra_field":
        data["grade"] = "A"
    elif name == "unit_token":
        data["unit_records"][0]["unit_token"] = "kN"
    elif name == "alias_unit":
        extra = dict(data["unit_records"][1], record_id="dcu:U999", unit_token="MM")
        data["unit_records"].append(extra)
    elif name == "missing_policy":
        data["source_use_policies"] = []
    elif name == "role_unit":
        record["input_roles"][0]["unit_token"] = "mm"
    elif name == "schema":
        data["schema_version"] = "2.0"
    elif name == "adapter_path":
        record["adapter_identity"] = 7
    elif name == "condition":
        record["applicability"][0]["condition"] = "anything"
    elif name == "no_methods":
        data["methods"] = []
    return data


@pytest.mark.parametrize("name", ["extra_field", "unit_token", "alias_unit",
                                  "missing_policy", "role_unit", "schema",
                                  "adapter_path", "condition", "no_methods"])
def test_owner_artifact_tamper_fails_closed(tmp_path, name):
    path = _write(tmp_path, _owner_tamper(name))
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    result = dc.execute(BINDING, _request(), artifact_path=path)
    assert (result["state"], result["reason"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE)
    assert result["outputs"] is None


def test_owner_artifact_missing_or_unreadable(tmp_path):
    result = dc.execute(BINDING, _request(), artifact_path=tmp_path / "absent.json")
    assert (result["state"], result["reason"]) == (
        dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE)
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    result = dc.execute(BINDING, _request(), artifact_path=bad)
    assert result["reason"] == dc.EXECUTION_INTEGRITY_FAILURE


def test_owner_artifact_version_edit_fails_closed_and_binding_mismatch_refuses(tmp_path):
    # the admitted inventory pins (method id, version): an artifact carrying another
    # version is not the admitted artifact; a binding / request version mismatch
    # against the admitted record stays a REFUSAL / VERSION_MISMATCH
    data = _owner_artifact()
    _cap13_record(data)["method_version"] = "1.1"
    path = _write(tmp_path, data)
    with pytest.raises(dc.CalculationArtifactError, match="not the admitted inventory"):
        dc.load_artifact(path)
    result = dc.execute(BINDING, _request(), artifact_path=path)
    assert (result["state"], result["reason"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE)
    stale = dc.bind_method(method.METHOD_ID, "1.1", method.evaluate)
    result = dc.execute(stale, _request(method_version="1.1"))
    assert (result["state"], result["reason"]) == (dc.STATE_REFUSAL, dc.VERSION_MISMATCH)


def _extra_kind(data, kind="mass"):
    data["quantity_kinds"].append({"quantity_kind": kind, "dimension": "M"})


def _extra_unit(data):
    data["unit_records"].append(dict(data["unit_records"][0], record_id="dcu:U999",
                                     unit_token="kg", unit_name="kilogram",
                                     quantity_kind="mass"))


@pytest.mark.parametrize("name,message", [
    ("extra_method", "methods: not the admitted inventory"),
    ("extra_kind", "quantity_kinds: not the admitted inventory"),
    ("extra_unit", "unit_records: not the admitted inventory"),
])
def test_owner_closed_inventory_rejects_structurally_valid_extras(tmp_path, monkeypatch,
                                                                  name, message):
    data = _owner_artifact()
    if name == "extra_method":
        extra = copy.deepcopy(_cap13_record(data))
        extra["method_id"] = "cap13:static_reactions_three_support"
        data["methods"].append(extra)
    elif name == "extra_kind":
        _extra_kind(data)
    else:
        # admit the extra kind for this test only, so the UNIT inventory alone decides
        monkeypatch.setattr(dc, "ADMITTED_QUANTITY_KINDS",
                            dc.ADMITTED_QUANTITY_KINDS | {"mass"})
        _extra_kind(data)
        _extra_unit(data)
    path = _write(tmp_path, data)
    with pytest.raises(dc.CalculationArtifactError, match=message):
        dc.load_artifact(path)
    result = dc.execute(BINDING, _request(), artifact_path=path)
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def test_owner_closed_inventory_constants():
    # Correction 02 (calc / units contract §13A): exactly two methods, closed
    assert dc.ADMITTED_METHODS == frozenset({
        ("cap13:static_reactions_two_support", "1.0"),
        ("therm01:conduction_temperature_difference_single_path", "1.0")})
    assert dc.ADMITTED_QUANTITY_KINDS == frozenset({
        "force", "length", "power", "thermal_resistance", "temperature_difference"})
    assert dc.ADMITTED_UNIT_TOKENS == frozenset({"N", "mm", "W", "K/W", "K"})


def test_owner_method_source_qualification_is_self_contained():
    data = dc.load_artifact()
    policies = {p["record_id"]: p for p in data["source_use_policies"]}
    record = _cap13_record(data)
    for entry in record["source_qualification"]:
        assert entry["source_use_policy_ref"] in policies
        assert entry["source_use_policy_ref"] == "dcu:SU002"
    snapshot = policies["dcu:SU002"]
    assert snapshot["url"] == "https://sti.nasa.gov/disclaimers/"
    assert "cap13:SU001" in snapshot["inspection_reference"]
    assert "version 1" in snapshot["inspection_reference"]
    owner_source = Path(dc.__file__).read_text(encoding="utf-8")
    assert "cap13_content_config" not in owner_source


@pytest.mark.parametrize("name", ["foreign_ref", "unknown_ref", "snapshot_removed",
                                  "basis_altered", "ref_missing", "date_altered"])
def test_owner_method_source_use_tamper_fails_closed(tmp_path, name):
    data = _owner_artifact()
    entry = _cap13_record(data)["source_qualification"][0]
    if name == "foreign_ref":
        entry["source_use_policy_ref"] = "cap13:SU001"      # not resolvable locally
    elif name == "unknown_ref":
        entry["source_use_policy_ref"] = "dcu:SU999"
    elif name == "snapshot_removed":
        data["source_use_policies"] = [p for p in data["source_use_policies"]
                                       if p["record_id"] != "dcu:SU002"]
    elif name == "basis_altered":
        entry["inspection_basis"] = "SELF_ASSERTED"
    elif name == "ref_missing":
        del entry["source_use_policy_ref"]
    elif name == "date_altered":
        entry["inspection_date"] = "recently"
    path = _write(tmp_path, data)
    with pytest.raises(dc.CalculationArtifactError):
        dc.load_artifact(path)
    result = dc.execute(BINDING, _request(), artifact_path=path)
    assert (result["state"], result["reason"], result["outputs"]) == (
        dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, None)


def _cap13_tamper(name):
    data = _cap13_artifact()
    if name == "extra_field":
        data["rating"] = "safe"
    elif name == "version":
        data["method"]["method_version"] = "1.1"
    elif name == "declaration_removed":
        data["declarations"].pop()
    elif name == "refusal_changed":
        data["declarations"][0]["refusal"] = "SUPPORT_NOT_SUPPORTED"
    elif name == "screen_removed":
        data["screen_items"].pop()
    elif name == "policy_removed":
        data["sources"] = [s for s in data["sources"]
                           if s["record_id"] != "cap13:SU001"]
    elif name == "source_unbound":
        data["sources"][0]["source_use_policy_ref"] = "cap12:SU001"
    elif name == "role_changed":
        data["numeric_domain"]["roles"][0]["unit_token"] = "kN"
    elif name == "schema":
        data["schema_version"] = "9"
    return data


@pytest.mark.parametrize("name", ["extra_field", "version", "declaration_removed",
                                  "refusal_changed", "screen_removed",
                                  "policy_removed", "source_unbound",
                                  "role_changed", "schema"])
def test_cap13_artifact_tamper_fails_closed_before_any_calculation(name, monkeypatch):
    data = _cap13_tamper(name)
    with pytest.raises(cap13.Cap13KnowledgeError):
        cap13.validate_artifact(data)
    called = []
    monkeypatch.setattr(cap13._dc, "execute",
                        lambda *a, **k: called.append(1) or {})
    captured = cap13.capture_form({k: [v] for k, v in _form().items()})
    result = cap13.evaluate(captured, BINDING, artifact=data)
    assert result == {"outcome": cap13.KNOWLEDGE_UNAVAILABLE, "owner_state": None,
                      "owner_reason": None, "result": None}
    assert not called


def _semantic_tamper(name):
    data = _cap13_artifact()
    if name == "declaration_meaning":
        data["declarations"][0]["accepted_value"] = "static or slowly varying"
    elif name == "centre_of_gravity_meaning":
        data["declarations"][-1]["accepted_value"] = "defaulted to midspan when not declared"
    elif name == "screen_meaning":
        data["screen_items"][0]["item"] = "supports light objects"
    elif name == "numeric_rule":
        data["numeric_domain"]["rules"][0] = data["numeric_domain"]["rules"][0] + " (tolerance 1%)"
    elif name == "role_meaning":
        data["numeric_domain"]["roles"][0]["meaning"] = "any force"
    elif name == "limitation":
        data["limitations"][0] = "Support capacity is checked."
    elif name == "disclosure":
        data["disclosure"] = data["disclosure"].replace("are not evidence", "are evidence")
    elif name == "executed_form":
        data["method"]["executed_form"] = "R_R = P * x / L; R_L = P - R_R"
    elif name == "method_model":
        data["method"]["model"] = data["method"]["model"] + " with a third support"
    elif name == "source_url":
        data["sources"][0]["url"] = "https://example.com/equilibrium"
    elif name == "source_use_content":
        policy = [s for s in data["sources"] if s["record_id"] == "cap13:SU001"][0]
        policy["inspected_content"] = "Freely reusable."
    elif name == "artifact_version":
        data["artifact_version"] = "2"
    return data


@pytest.mark.parametrize("name", ["declaration_meaning", "centre_of_gravity_meaning",
                                  "screen_meaning", "numeric_rule", "role_meaning",
                                  "limitation", "disclosure", "executed_form",
                                  "method_model", "source_url", "source_use_content",
                                  "artifact_version"])
def test_cap13_semantic_tamper_fails_closed(name, monkeypatch):
    data = _semantic_tamper(name)
    assert data != _cap13_artifact()
    with pytest.raises(cap13.Cap13KnowledgeError):
        cap13.validate_artifact(data)
    called = []
    monkeypatch.setattr(cap13._dc, "execute", lambda *a, **k: called.append(1) or {})
    captured = cap13.capture_form({k: [v] for k, v in _form().items()})
    assert cap13.evaluate(captured, BINDING, artifact=data)["outcome"] \
        == cap13.KNOWLEDGE_UNAVAILABLE
    assert not called


def test_cap13_semantic_pins_cover_the_governed_sections():
    assert set(cap13._SEMANTIC_DIGESTS) == {"method", "numeric_domain", "declarations",
                                           "screen_items", "limitations", "disclosure",
                                           "sources"}
    data = cap13.load_artifact()
    for section, digest in cap13._SEMANTIC_DIGESTS.items():
        assert cap13._section_digest(data[section]) == digest, section
    assert data["method"]["method_id"] == method.METHOD_ID
    assert data["method"]["method_version"] == method.METHOD_VERSION


def test_cap13_artifact_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(cap13, "ARTIFACT_PATH", tmp_path / "absent.json")
    assert _evaluate()["outcome"] == cap13.KNOWLEDGE_UNAVAILABLE


# ==========================================================================
# 4. the consumer: strict capture, grammar, §12A precedence, §8 mapping
# ==========================================================================
def test_success_through_the_consumer():
    result = _evaluate()
    assert result["outcome"] == cap13.OUTCOME_SUCCESS
    assert result["owner_state"] == dc.STATE_SUCCESS
    outputs = result["result"]["outputs"]
    assert (outputs["R_L"]["value"], outputs["R_R"]["value"]) == (750.0, 250.0)


@pytest.mark.parametrize("x,left,right", [("0", 1000.0, 0.0), ("-0", 1000.0, 0.0),
                                          ("0.0", 1000.0, 0.0),
                                          ("2000", 0.0, 1000.0),
                                          ("2000.000", 0.0, 1000.0)])
def test_endpoints_through_the_consumer(x, left, right):
    result = _evaluate(x=x)
    assert result["outcome"] == cap13.OUTCOME_SUCCESS
    outputs = result["result"]["outputs"]
    assert repr(outputs["R_L"]["value"]) == repr(left)
    assert repr(outputs["R_R"]["value"]) == repr(right)


@pytest.mark.parametrize("x", ["-1", "-0.0001", "2000.0001", "3000"])
def test_out_of_span_both_directions(x):
    result = _evaluate(x=x)
    assert result == {"outcome": cap13.CG_OUTSIDE_SUPPORT_SPAN, "owner_state": None,
                      "owner_reason": None, "result": None}


GRAMMAR_REJECTED = [
    "1,000", "1_000", "1e3", "1E3", "0x10", "10N", "10 N", "10mm", "inf", "Inf",
    "nan", "NaN", "Infinity", "+5", " 5", "5 ", "\t5", "5\n", ".5", "5.", "1.2.3",
    "--5", "٥", "۵", "５", "5٠", "½", "1 000",
    "−5", "9" * 400, "0b101", "5.0e0", "١٠٠٠",
]


@pytest.mark.parametrize("text", GRAMMAR_REJECTED)
@pytest.mark.parametrize("role", ["P", "L", "x"])
def test_strict_grammar_rejection_matrix(role, text):
    result = _evaluate(**{role: text})
    assert result == {"outcome": cap13.INVALID_NUMERIC_INPUT, "owner_state": None,
                      "owner_reason": None, "result": None}


@pytest.mark.parametrize("role", ["P", "L"])
@pytest.mark.parametrize("text", ["-5", "-0", "0", "0.0", "-1000"])
def test_sign_only_on_x_and_positivity(role, text):
    assert _evaluate(**{role: text})["outcome"] == cap13.INVALID_NUMERIC_INPUT


def test_parse_number_is_the_only_string_step():
    assert cap13.parse_number("12.5", signed=False) == 12.5
    assert cap13.parse_number("-12.5", signed=True) == -12.5
    assert cap13.parse_number("-12.5", signed=False) is None
    assert cap13.parse_number(12.5, signed=False) is None
    assert cap13.parse_number("1" + "0" * 400, signed=False) is None
    source = Path(dc.__file__).read_text(encoding="utf-8")
    assert "float(value)" in source and "re.compile" not in source.split(
        "def execute", 1)[1]


@pytest.mark.parametrize("field", ["P", "L", "x"])
def test_missing_or_empty_values_are_not_declared(field):
    assert _evaluate(**{field: ""})["outcome"] == cap13.NOT_DECLARED
    form = {k: [v] for k, v in _form().items()}
    del form[cap13.VALUE_FIELD % field]
    assert cap13.evaluate(cap13.capture_form(form), BINDING)["outcome"] \
        == cap13.NOT_DECLARED


@pytest.mark.parametrize("decl", cap13.DECLARATION_IDS)
def test_unanswered_declaration_is_not_declared(decl):
    assert _evaluate(decl={decl: ""})["outcome"] == cap13.NOT_DECLARED


@pytest.mark.parametrize("item", cap13.SCREEN_ITEMS)
def test_unanswered_screen_item_is_not_declared(item):
    assert _evaluate(screen={item: ""})["outcome"] == cap13.NOT_DECLARED


@pytest.mark.parametrize("item", cap13.SCREEN_ITEMS)
def test_any_screen_yes_abstains_without_calling_the_owner(item, monkeypatch):
    called = []
    monkeypatch.setattr(cap13._dc, "execute", lambda *a, **k: called.append(1))
    result = _evaluate(screen={item: cap13.SCREEN_YES})
    assert result["outcome"] == cap13.ENGINEERING_REVIEW_REQUIRED
    assert result["result"] is None and not called


@pytest.mark.parametrize("decl", cap13.DECLARATION_IDS)
def test_each_declaration_refuses_with_its_own_group(decl):
    expected = {"load": cap13.LOAD_NOT_SUPPORTED,
                "support": cap13.SUPPORT_NOT_SUPPORTED,
                "centre_of_gravity": cap13.NOT_DECLARED}[dict(cap13.DECLARATIONS)[decl]]
    result = _evaluate(decl={decl: cap13.ANSWER_DIFFERS})
    assert result["outcome"] == expected and result["result"] is None


def test_section_12a_precedence_first_failing_stage_wins():
    everything_wrong = dict(
        decl={"condition": cap13.ANSWER_DIFFERS, "support_count": cap13.ANSWER_DIFFERS},
        screen={"pressure": cap13.SCREEN_YES}, P="abc", x="-5")
    # 2. completeness before everything
    kw = copy.deepcopy(everything_wrong)
    kw["decl"]["weight"] = ""
    assert _evaluate(**kw)["outcome"] == cap13.NOT_DECLARED
    # 3. screen before load / support / numeric / span
    assert _evaluate(**everything_wrong)["outcome"] == cap13.ENGINEERING_REVIEW_REQUIRED
    # 4. load before support / numeric / span
    kw = copy.deepcopy(everything_wrong)
    kw["screen"] = {}
    assert _evaluate(**kw)["outcome"] == cap13.LOAD_NOT_SUPPORTED
    # 5. support before numeric / span
    kw["decl"].pop("condition")
    assert _evaluate(**kw)["outcome"] == cap13.SUPPORT_NOT_SUPPORTED
    # 6. numeric before span
    kw["decl"] = {}
    assert _evaluate(**kw)["outcome"] == cap13.INVALID_NUMERIC_INPUT
    # 7. span
    kw["P"] = "10"
    assert _evaluate(**kw)["outcome"] == cap13.CG_OUTSIDE_SUPPORT_SPAN
    # declaration precedence inside the completeness stage: an unanswered
    # declaration beats a differing centre-of-gravity declaration
    assert _evaluate(decl={"centre_of_gravity": cap13.ANSWER_DIFFERS,
                           "condition": ""})["outcome"] == cap13.NOT_DECLARED


def test_owner_is_called_only_after_every_pre_owner_stage(monkeypatch):
    seen = []
    real_execute = dc.execute

    def spy(binding, request, artifact_path=None):
        seen.append(copy.deepcopy(request))
        return real_execute(binding, request, artifact_path)
    monkeypatch.setattr(cap13._dc, "execute", spy)
    _evaluate(x="5000")
    _evaluate(P="0")
    assert seen == []
    _evaluate(P="10.5", L="3", x="1")
    assert seen == [{"method_id": method.METHOD_ID, "method_version": "1.0",
                     "inputs": {"P": {"value": 10.5, "unit": "N"},
                                "L": {"value": 3.0, "unit": "mm"},
                                "x": {"value": 1.0, "unit": "mm"}},
                     "subject_ref": None}]


ALL_OWNER_PAIRS = [(dc.REASON_STATE[r], r) for r in sorted(dc.REASON_STATE)]


@pytest.mark.parametrize("state,reason", ALL_OWNER_PAIRS)
def test_every_owner_state_maps_per_section_8_and_is_preserved(state, reason, monkeypatch):
    monkeypatch.setattr(cap13._dc, "execute",
                        lambda *a, **k: {"state": state, "reason": reason,
                                         "outputs": None})
    result = _evaluate()
    expected = cap13.OWNER_CORRESPONDENCE.get((state, reason),
                                              cap13.UNMAPPED_OWNER_OUTCOME)
    assert result == {"outcome": expected, "owner_state": state,
                      "owner_reason": reason, "result": None}


def test_section_8_correspondence_table_is_exact():
    assert cap13.OWNER_CORRESPONDENCE == {
        ("REFUSAL", "INVALID_NUMERIC_INPUT"): "INVALID_NUMERIC_INPUT",
        ("REFUSAL", "UNIT_NOT_ADMITTED"): "UNIT_NOT_SUPPORTED",
        ("REFUSAL", "UNKNOWN_UNIT"): "UNIT_NOT_SUPPORTED",
        ("REFUSAL", "METHOD_NOT_REGISTERED"): "KNOWLEDGE_UNAVAILABLE",
        ("REFUSAL", "VERSION_MISMATCH"): "KNOWLEDGE_UNAVAILABLE",
        ("UNABLE_TO_DETERMINE", "SOURCE_UNAVAILABLE"): "KNOWLEDGE_UNAVAILABLE",
        ("FAILURE", "EXECUTION_INTEGRITY_FAILURE"): "KNOWLEDGE_UNAVAILABLE",
    }


def test_reachable_real_owner_states_through_the_consumer(tmp_path):
    captured = cap13.capture_form({k: [v] for k, v in _form().items()})
    # owner artifact missing -> UNABLE / SOURCE_UNAVAILABLE -> KNOWLEDGE_UNAVAILABLE
    r = cap13.evaluate(captured, BINDING, owner_artifact_path=tmp_path / "x.json")
    assert (r["outcome"], r["owner_state"], r["owner_reason"]) == (
        cap13.KNOWLEDGE_UNAVAILABLE, dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE)
    # owner artifact tampered -> FAILURE preserved (never remapped to REFUSAL)
    path = _write(tmp_path, _owner_tamper("unit_token"), "t.json")
    r = cap13.evaluate(captured, BINDING, owner_artifact_path=path)
    assert (r["outcome"], r["owner_state"], r["owner_reason"]) == (
        cap13.KNOWLEDGE_UNAVAILABLE, dc.STATE_FAILURE,
        dc.EXECUTION_INTEGRITY_FAILURE)
    # version mismatch -> REFUSAL / VERSION_MISMATCH
    stale = dc.bind_method(method.METHOD_ID, "0.9", method.evaluate)
    r = cap13.evaluate(captured, stale)
    assert (r["outcome"], r["owner_state"], r["owner_reason"]) == (
        cap13.KNOWLEDGE_UNAVAILABLE, dc.STATE_REFUSAL, dc.VERSION_MISMATCH)
    # interior collapse -> FAILURE, no payload
    captured_tiny = cap13.capture_form({k: [v] for k, v in _form(
        P="0." + "0" * 323 + "5", L="1", x="0.5").items()})
    r = cap13.evaluate(captured_tiny, BINDING)
    assert (r["outcome"], r["owner_state"], r["result"]) == (
        cap13.KNOWLEDGE_UNAVAILABLE, dc.STATE_FAILURE, None)


@pytest.mark.parametrize("form", [
    {"value_P": ["1"], "extra": ["x"]},
    {"value_P": ["1", "2"]},
    {"decl_condition": ["yes"]},
    {"decl_condition": ["MATCHES"]},
    {"screen_pressure": ["matches"]},
    {"screen_pressure": ["No"]},
    {"value_P": [1]},
    {"value_P": "1"},
    [],
])
def test_malformed_capture(form):
    assert cap13.capture_form(form) is None


def test_eligibility_is_mechanical_root_only():
    assert cap13.is_eligible("mechanical")
    for value in (None, "", "Mechanical", "electronics_electrical", "control_loop",
                  " mechanical", ["mechanical"]):
        assert not cap13.is_eligible(value)


def test_format_value_applies_no_rounding():
    for value in (750.0, 0.1 + 0.2, 1e-300, 123456789.123456789, 2.0 / 3.0):
        assert float(cap13.format_value(value)) == value
    assert cap13.format_value(0.1 + 0.2) == "0.30000000000000004"


# ==========================================================================
# 5. EN / AR fidelity to the contract
# ==========================================================================
def test_english_wording_equals_the_contract_and_artifact():
    content = cap13.load_artifact()
    disclosure = _contract_section("**Fixed disclosure (English", "## 11.")
    assert _blockquote_paragraphs(disclosure) == [_norm(content["disclosure"])]
    assert ui_text.text("UI_CAP13_DISCLOSURE", "en") == content["disclosure"]
    for entry in content["declarations"]:
        expected = entry["accepted_value"][0].upper() + entry["accepted_value"][1:] + "."
        assert ui_text.text("UI_CAP13_DECL_" + entry["declaration_id"].upper(),
                            "en") == expected
    for entry in content["screen_items"]:
        expected = entry["item"][0].upper() + entry["item"][1:]
        assert ui_text.text("UI_CAP13_SCREEN_" + entry["item_id"].upper(),
                            "en") == expected


def test_arabic_wording_is_contract_12b_verbatim():
    b1 = _contract_section("**B-1", "Parity with §10")
    paragraphs = [p.replace("**", "") for p in _blockquote_paragraphs(b1)]
    assert ui_text.text("UI_CAP13_DISCLOSURE", "ar").split("\n\n") == paragraphs
    b2 = _table(_contract_section("**B-2", "**B-3"))
    for decl in cap13.DECLARATION_IDS:
        label = decl.replace("_", " ").replace("centre of gravity", "centre of gravity")
        assert ui_text.text("UI_CAP13_DECL_" + decl.upper(), "ar") == b2[label], decl
    b3_section = _contract_section("**B-3", "**B-4")
    b3 = _table(b3_section)
    screen_labels = {"supports_people": "supports people",
                     "overhead_or_falling_hazard": "overhead or falling hazard",
                     "children": "use by or for children",
                     "safety_critical_load_path": "safety-critical load path",
                     "pressure": "pressure", "high_temperature": "high temperature",
                     "battery_containment": "battery containment",
                     "medical_use": "medical use", "food_contact": "food contact"}
    for item, label in screen_labels.items():
        assert ui_text.text("UI_CAP13_SCREEN_" + item.upper(), "ar") == b3[label]
    assert "«" + ui_text.text("UI_CAP13_SCREEN_NOTE", "ar") + "»" in _norm(b3_section)
    assert "«" + ui_text.text("UI_CAP13_SCREEN_STEM", "ar") + "»" in _norm(b3_section)
    b4 = _table(_contract_section("**B-4", "The unmapped-outcome line"))
    for outcome in ("NOT_DECLARED", "LOAD_NOT_SUPPORTED", "SUPPORT_NOT_SUPPORTED",
                    "INVALID_NUMERIC_INPUT", "CG_OUTSIDE_SUPPORT_SPAN",
                    "UNIT_NOT_SUPPORTED", "KNOWLEDGE_UNAVAILABLE"):
        assert ui_text.text("UI_CAP13_OUTCOME_" + outcome, "ar") == b4[outcome]
    assert ui_text.text("UI_CAP13_OUTCOME_ENGINEERING_REVIEW_REQUIRED", "ar") \
        == b4["ENGINEERING REVIEW REQUIRED"]
    assert ui_text.text("UI_CAP13_OUTCOME_UNMAPPED_OWNER_OUTCOME", "ar") \
        == b4["Owner outcome not mapped by §8 (no reason token)"]
    assert ui_text.text("UI_CAP13_ERR_REQUEST", "ar") \
        == b4["Malformed request (§12A; no reason token)"]
    b5 = _table(_contract_section("**B-5", "**B-6"))
    pairs = {"LINK_TEXT": "Session-page link", "LINK_NOTE": "Link note",
             "TITLE": "Page title", "INTRO": "Page intro",
             "FIELD_P": "Total weight input", "FIELD_L": "Separation input",
             "FIELD_X": "Centre-of-gravity input", "SUBMIT": "Submit",
             "RESULT_R_L": "Left reaction", "RESULT_R_R": "Right reaction",
             "STATUS": "Status", "ECHO_HEADING": "Echoed inputs heading",
             "METHOD_LINE": "Method line", "SOURCES_HEADING": "Sources heading",
             "SOURCES_NOTE": "Sources note", "BACK": "Back link",
             "SCOPE_NOTE": "Scope note (Mechanical-only first slice)"}
    for key, row in pairs.items():
        assert ui_text.text("UI_CAP13_" + key, "ar") == b5[row], key
    matches, differs = b5["Declaration answers"].split(" / ")
    assert ui_text.text("UI_CAP13_ANSWER_MATCHES", "ar") == matches
    assert ui_text.text("UI_CAP13_ANSWER_DIFFERS", "ar") == differs
    yes, no = b5["Screen answers"].split(" / ")
    assert (ui_text.text("UI_CAP13_SCREEN_YES", "ar"),
            ui_text.text("UI_CAP13_SCREEN_NO", "ar")) == (yes, no)


def test_every_cap13_string_is_bilingual_and_carries_no_verdict_wording():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_CAP13_")]
    assert len(keys) == 53
    for key in keys:
        entry = ui_text.UI_STRINGS[key]
        assert entry.get("en") and entry.get("ar"), key
        assert re.search(r"[؀-ۿ]", entry["ar"]), key
        for word in ("is adequate", "approved", "certified", "passes",
                     "recommended", "you can rely"):
            assert word not in entry["en"].lower(), (key, word)


# ==========================================================================
# 6. the web slice: eligibility, request integrity, isolation, no persistence
# ==========================================================================
def test_route_in_r05_inventory():
    from tests.test_r05_request_integrity import MUTATIONS
    assert "/session/<sid>/support-reactions" in MUTATIONS


def test_link_offered_on_mechanical_only(mech, elec):
    c, _aid, sid = mech
    assert "data-cap13-link" in _page(c, sid)
    c2, _aid2, sid2 = elec
    assert "data-cap13-link" not in _page(c2, sid2)


def test_get_shows_an_unanswered_form(mech):
    c, _aid, sid = mech
    r = c.get(URL % sid)
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    body = r.get_data(as_text=True)
    assert "data-cap13-form" in body and " checked" not in body
    assert body.count('type="radio"') == 2 * (10 + 9)
    for role in ("P", "L", "x"):
        assert re.search(r'name="value_%s"[^>]*value=""' % role, body)
    assert "data-cap13-result" not in body and "data-cap13-outcome" not in body


def test_post_success_renders_in_the_same_request(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(P="1000", L="2000", x="500"))
    assert r.status_code == 200 and r.headers["Cache-Control"] == "no-store"
    assert "Location" not in r.headers
    body = r.get_data(as_text=True)
    reactions = re.findall(r'data-cap13-reaction><bdi dir="ltr">([^<]+)</bdi>', body)
    assert reactions == ["750.0 N", "250.0 N"]
    assert "cap13:static_reactions_two_support" in body
    assert "UNVALIDATED" in body
    text = html.unescape(_content_text(body))
    assert _norm(ui_text.text("UI_CAP13_DISCLOSURE", "en")) in _norm(text)
    echoed = re.findall(r'data-cap13-echo-value>([^<]*)<', body)
    assert echoed == ["1000", "2000", "500"]
    assert "Beginners Guide to Aeronautics - Equilibrium" in body
    assert "NIST Special Publication 811" in body


def test_post_refusal_shows_one_reason_and_no_number(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(x="2500"))
    body = r.get_data(as_text=True)
    assert r.status_code == 200
    assert ui_text.text("UI_CAP13_OUTCOME_CG_OUTSIDE_SUPPORT_SPAN", "en") in body
    assert "data-cap13-reaction" not in body and "data-cap13-result" not in body
    assert body.count("data-cap13-outcome") == 1


def test_raw_echo_is_escaped_and_same_request_only(mech):
    c, _aid, sid = mech
    r = c.post(URL % sid, data=_form(P="<b>1</b>"))
    body = r.get_data(as_text=True)
    assert "<b>1</b>" not in body and "&lt;b&gt;1&lt;/b&gt;" in body
    assert "&lt;b&gt;" not in c.get(URL % sid).get_data(as_text=True)


def test_malformed_request_is_400_without_a_reason_token(mech):
    c, _aid, sid = mech
    data = _form()
    data["unexpected"] = "1"
    r = c.post(URL % sid, data=data)
    assert r.status_code == 400
    body = r.get_data(as_text=True)
    assert ui_text.text("UI_CAP13_ERR_REQUEST", "en") in body
    assert "data-cap13-outcome" not in body and "data-cap13-result" not in body
    r = c.post(URL % sid, data=dict(_form(), decl_condition="yes"))
    assert r.status_code == 400


def test_ineligible_project_is_never_evaluated(elec, monkeypatch):
    c, _aid, sid = elec
    called = []
    monkeypatch.setattr(webapp._cap13, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert "data-cap13-scope-note" in body
        assert "data-cap13-form" not in body and "data-cap13-outcome" not in body
    assert not called


def test_csrf_is_enforced():
    c = webapp.app.test_client()
    assert c.post(URL % "not-a-project", data=_form()).status_code == 403


def test_another_account_and_anonymous_callers_are_denied(mech):
    _c, _aid, sid = mech
    other, _ = _client_for("cap13-other@example.com")
    anon = _new_client()
    for client in (other, anon):
        for response in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert response.status_code == 302
            assert "data-cap13" not in response.get_data(as_text=True)


@pytest.mark.parametrize("over", [{}, {"x": "-3"}, {"P": "abc"},
                                  {"screen": {"pressure": "yes"}}])
def test_nothing_is_persisted_and_no_project_state_moves(mech, over):
    c, _aid, sid = mech
    _page(c, sid)                       # consume any one-shot start notice
    before = _snapshot(c)               # the whole database and SESSION_STORE
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_no_safety_signal_report_export_or_api_surface():
    app_source = Path(webapp.__file__).read_text(encoding="utf-8")
    start = app_source.index("# Stage 25 / CAP-13 — Two-Support Static Reactions")
    section = app_source[start:app_source.index("# Manufacturing Evidence Capture", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store().save", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/"):
        assert banned not in section, banned
    routes = [r.rule for r in webapp.app.url_map.iter_rules()
              if "support-reactions" in r.rule]
    assert routes == ["/session/<sid>/support-reactions"] * 2
    for template in ("deliverable.html", "report.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "cap13" not in path.read_text(encoding="utf-8")


def test_arabic_page_is_rtl_and_isolates_tokens(mech):
    c, _aid, sid = mech
    c.post("/ui-language", data={"lang": "ar"})
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert 'dir="rtl"' in body
    assert '(<bdi dir="ltr">R_L</bdi>)' in body and '(<bdi dir="ltr">R_R</bdi>)' in body
    assert '(<bdi dir="ltr">N</bdi>)' in body and '(<bdi dir="ltr">mm</bdi>)' in body
    assert '<bdi dir="ltr">cap13:static_reactions_two_support</bdi>' in body
    assert '<bdi dir="ltr">750.0 N</bdi>' in body
    assert '(<bdi dir="ltr">UNVALIDATED</bdi>)' in body
    assert 'بـ<bdi dir="ltr">InventorAI</bdi>' in body
    assert ui_text.text("UI_CAP13_ANSWER_MATCHES", "ar") in body
    for para in ui_text.text("UI_CAP13_DISCLOSURE", "ar").split("\n\n"):
        stripped = re.sub(r"<[^>]+>", "", body)
        assert para in stripped
    for role in ("P", "L", "x"):
        assert re.search(r'name="value_%s" dir="ltr"' % role, body)
