# -*- coding: utf-8 -*-
"""TEMPERATURE-TO-CONTROL-CONDITION-01 - Slice 1 (directly owning tests).

The thin composition (``engine/temperature_control_condition.py``) of the
EXISTING TMP36 consumer and the EXISTING 28-T4 evaluator. Expected values come
from an INDEPENDENT exact-decimal oracle written here with ``decimal.Decimal``
from the typed strings - never from either module's arithmetic - and the state
results from the Owner's 28-T4 table. Synthetic data.
"""
import html
import random
import re
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest
from werkzeug.datastructures import MultiDict

import web.app as webapp
from web import ui_text
from engine import control_cycle as cc
from engine import deterministic_calculation as dc
from engine import temperature_control_condition as tcc
from engine import tmp36_nominal_temperature as tmp36
from engine import tmp36_nominal_temperature_method as tmp36_method
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import _integrated, MECH, ELEC
from tests.test_tmp36_nominal_temperature import _form as _tmp36_form
from tests.test_control_cycle import _form as _cc_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "docs" / "governance" / "TEMPERATURE_TO_CONTROL_CONDITION_COMPOSITION_CONTRACT.md"
TMP36_CONTRACT = (ROOT / "docs" / "governance"
                  / "SENSORS_C3_TMP36_NOMINAL_VOLTAGE_TO_TEMPERATURE_METHOD_CONTRACT.md")
CC_CONTRACT = ROOT / "docs" / "governance" / "STAGE28_T4_CONTROL_CYCLE_READY_RUNNING_CONTRACT.md"
URL = "/session/%s/temperature-control-condition"
BINDING = dc.bind_method(tmp36_method.METHOD_ID, tmp36_method.METHOD_VERSION,
                         tmp36_method.evaluate)
# The Owner's 28-T4 table: (previous, start_input) -> (next, output).
CYCLE = {("READY", True): ("RUNNING", True), ("READY", False): ("READY", False),
         ("RUNNING", True): ("RUNNING", True), ("RUNNING", False): ("RUNNING", True)}


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _oracle(v_out, threshold):
    """Independent exact-decimal oracle: (Decimal(V) - 500) / 10 >= Decimal(theta)."""
    return (Decimal(v_out) - Decimal(500)) / Decimal(10) >= Decimal(threshold)


def _form(v_out="750", threshold="25", previous="READY", meaning="applies",
          t_decl=None, t_screen=None, c_decl=None, c_screen=None):
    form = {"decl_condition_meaning": meaning, "threshold_c": threshold}
    for key, value in _tmp36_form(v_out=v_out, decl=t_decl, screen=t_screen).items():
        form["t_" + key] = value
    for key, value in _cc_form(previous=previous, decl=c_decl, screen=c_screen).items():
        if key != cc.INPUT_FIELD:
            form["c_" + key] = value
    return form


def _captured(**kw):
    captured = tcc.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return tcc.evaluate(_captured(**kw), BINDING)


def _field(body, name):
    marker = "data-tcc-result-%s" % name
    if marker not in body:
        return None
    cell = body.split(marker, 1)[1].split(">", 1)[1].split("</dd>", 1)[0]
    return html.unescape(re.sub(r"<[^>]+>", "", cell)).strip()


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


def _assert_refused(result, outcome, part=None):
    assert result == {"outcome": outcome, "part_outcome": part}, result


@pytest.fixture
def elec():
    c, aid = _client_for("tcc-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def mech():
    c, aid = _client_for("tcc-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": MECH})


# ==========================================================================
# 1. the fixed condition against the exact-decimal oracle
# ==========================================================================
@pytest.mark.parametrize("v_out,threshold", [
    ("750", "24.9999"), ("750", "25"), ("750", "25.0001"),       # above, equal, below
    ("100", "-40"), ("100", "-39.9999"), ("101", "-40"),         # threshold -40
    ("1750", "125"), ("1749.999", "125"), ("1750", "124.9999"),  # threshold +125
    ("500", "0"), ("500", "-0"), ("500", "0.0001"), ("499.999", "0"), ("500.001", "0"),
    ("100", "125"), ("1750", "-40"),
])
def test_condition_matches_the_exact_decimal_oracle(v_out, threshold):
    result = _evaluate(v_out=v_out, threshold=threshold)
    assert result["outcome"] == tcc.OUTCOME_SUCCESS
    assert result["condition"] is _oracle(v_out, threshold)
    assert result["start_input"] is result["condition"]
    assert result["nominal_temperature"] == Fraction(
        (Decimal(v_out) - Decimal(500)) / Decimal(10))
    assert result["threshold"] == Fraction(Decimal(threshold))


@pytest.mark.parametrize("v_out,threshold,expected", [
    ("750.1", "25.01", True),
    ("100.001", "-39.9999", True),  # naive float arithmetic gives -39.999900000000004
    ("100.001", "-39.9998", False),
    ("750.1", "25.0101", False),
    ("750.099", "25.0099", True),
    ("750.099", "25.01", False),
    ("123.456", "-37.6544", True),
    ("123.456", "-37.6543", False),
    ("1234.567", "73.4567", True),
])
def test_decimal_adjacent_comparisons_are_exact(v_out, threshold, expected):
    assert _oracle(v_out, threshold) is expected
    result = _evaluate(v_out=v_out, threshold=threshold)
    assert result["condition"] is expected


def test_a_naive_binary_comparison_would_be_wrong_at_equality():
    naive = (float("100.001") - 500.0) / 10.0     # ordinary float arithmetic
    assert naive < float("-39.9999")              # says "below"
    assert _oracle("100.001", "-39.9999") is True  # the exact decimals are equal
    assert _evaluate(v_out="100.001", threshold="-39.9999")["condition"] is True


def test_random_comparisons_against_the_oracle():
    rng = random.Random(20261025)
    for _ in range(3000):
        v = "%d.%03d" % divmod(rng.randint(100000, 1750000), 1000)
        nominal = (Decimal(v) - 500) / 10
        offset = Decimal(rng.choice((-2, -1, 0, 0, 1, 2))) / Decimal(10000)
        theta = max(Decimal(-40), min(Decimal(125), nominal + offset))
        text = "%s" % theta.quantize(Decimal("0.0001"))
        result = _evaluate(v_out=v, threshold=text)
        assert result["outcome"] == tcc.OUTCOME_SUCCESS, (v, text)
        assert result["condition"] is _oracle(v, text), (v, text)


def test_condition_refuses_non_exact_values():
    with pytest.raises(TypeError):
        tcc.condition_holds(25.0, Fraction(25))
    with pytest.raises(TypeError):
        tcc.condition_holds(Fraction(25), "25")
    assert tcc.condition_holds(Fraction(25), Fraction(25)) is True


# ==========================================================================
# 2. the cycle: READY / RUNNING with true and false
# ==========================================================================
@pytest.mark.parametrize("previous", ["READY", "RUNNING"])
@pytest.mark.parametrize("threshold,condition", [("20", True), ("30", False)])
def test_cycle_results_follow_the_owner_table(previous, threshold, condition):
    result = _evaluate(v_out="750", threshold=threshold, previous=previous)
    assert result["condition"] is condition and result["start_input"] is condition
    assert (result["next_state"], result["output"]) == CYCLE[(previous, condition)]
    assert result["previous_state"] == previous


def test_running_with_false_is_not_reset():
    result = _evaluate(v_out="400", threshold="0", previous="RUNNING")
    assert result["condition"] is False
    assert result["next_state"] == "RUNNING" and result["output"] is True
    assert result["transition_status"] == cc.TRANSITION_NOT_APPLICABLE
    assert result["transition_applied"] is False


def test_success_carries_provenance_identity_and_unvalidated():
    result = _evaluate(v_out="750.1", threshold="25.01")
    assert result["declared_voltage_text"] == "750.1"
    assert result["threshold_text"] == "25.01"
    assert result["nominal_temperature_display"] == "25.01"
    assert result["nominal_temperature_unit"] == "°C"
    assert result["temperature_method"] == ("tmp36:nominal_voltage_to_temperature", "1.0")
    assert result["cycle_method"] == ("control_cycle:ready_running_single_transition", "1.0")
    assert result["composition"] == ("temperature_control_condition:tmp36_threshold_ready_running", "1.0")
    assert result["validation_status"] == "UNVALIDATED"


# ==========================================================================
# 3. reuse: the parts run unchanged, nothing is duplicated
# ==========================================================================
def test_both_parts_are_called_once_and_start_input_is_derived(monkeypatch):
    seen = {"tmp36": [], "cc": []}
    real_t, real_c = tmp36.evaluate, cc.evaluate
    monkeypatch.setattr(tmp36, "evaluate", lambda c, b, **k: (
        seen["tmp36"].append((c, b)), real_t(c, b, **k))[1])
    monkeypatch.setattr(cc, "evaluate", lambda c, **k: (
        seen["cc"].append(dict(c)), real_c(c, **k))[1])
    _evaluate(v_out="760", threshold="26")
    assert len(seen["tmp36"]) == 1 and seen["tmp36"][0][1] is BINDING
    assert seen["tmp36"][0][0]["values"] == {"v_out": "760"}
    assert len(seen["cc"]) == 1 and seen["cc"][0]["start_input"] == "true"
    assert seen["cc"][0]["previous_state"] == "READY"


def test_the_accepted_exact_value_is_compared_never_display_text(monkeypatch):
    real = tmp36.evaluate

    def tampered(captured, binding, **kw):
        result = dict(real(captured, binding, **kw))
        result["display_value"] = "999.0"          # display text is never parsed
        return result
    monkeypatch.setattr(tmp36, "evaluate", tampered)
    assert _evaluate(v_out="750", threshold="25")["condition"] is True

    def float_value(captured, binding, **kw):
        result = dict(real(captured, binding, **kw))
        result["nominal_temperature"] = 25.0       # a float is never compared
        return result
    monkeypatch.setattr(tmp36, "evaluate", float_value)
    _assert_refused(_evaluate(), tcc.TMP36_REFUSED, tmp36.KNOWLEDGE_UNAVAILABLE)


def test_no_equation_state_table_or_refusal_rule_is_duplicated():
    source = Path(tcc.__file__).read_text(encoding="utf-8")
    code = "\n".join(line for line in source.splitlines()
                     if not line.strip().startswith("#"))
    code = re.sub(r'"""[\s\S]*?"""', "", code)
    for banned in ("500", "/ 10", "output_map", '"READY"', '"RUNNING"', "transitions",
                   "agrees_with_reference", "_dc.", "deterministic_calculation",
                   "float(", "eval(", "lambda"):
        assert banned not in code, banned
    import ast
    names = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom):
            names.add(node.module or "")
        elif isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
    assert names == {"re", "fractions", "engine"}, names


def test_tmp36_extraction_is_success_only_and_exact():
    ok = tmp36.evaluate(tmp36.capture_form({k: [v] for k, v in _tmp36_form(v_out="750.1").items()}),
                        BINDING)
    assert ok["nominal_temperature"] == Fraction(2501, 100)
    assert isinstance(ok["nominal_temperature"], Fraction)
    refused = tmp36.evaluate(tmp36.capture_form({k: [v] for k, v in _tmp36_form(v_out="2000").items()}),
                             BINDING)
    assert refused["nominal_temperature"] is None


# ==========================================================================
# 4. composition-level refusals
# ==========================================================================
@pytest.mark.parametrize("over,outcome", [
    ({"threshold": ""}, tcc.NOT_DECLARED),
    ({"meaning": ""}, tcc.NOT_DECLARED),
    ({"meaning": "does_not_apply"}, tcc.MODEL_NOT_SUPPORTED),
    ({"threshold": "abc"}, tcc.INVALID_THRESHOLD),
    ({"threshold": "25.00001"}, tcc.INVALID_THRESHOLD),
    ({"threshold": "+25"}, tcc.INVALID_THRESHOLD),
    ({"threshold": "1e1"}, tcc.INVALID_THRESHOLD),
    ({"threshold": "--5"}, tcc.INVALID_THRESHOLD),
    ({"threshold": " 25"}, tcc.INVALID_THRESHOLD),
    ({"threshold": "25,5"}, tcc.INVALID_THRESHOLD),
    ({"threshold": "inf"}, tcc.INVALID_THRESHOLD),
    ({"threshold": "-40.0001"}, tcc.THRESHOLD_OUTSIDE_RANGE),
    ({"threshold": "125.0001"}, tcc.THRESHOLD_OUTSIDE_RANGE),
    ({"threshold": "-273.15"}, tcc.THRESHOLD_OUTSIDE_RANGE),
    ({"threshold": "1000"}, tcc.THRESHOLD_OUTSIDE_RANGE),
])
def test_composition_refusals_carry_nothing(over, outcome, monkeypatch):
    calls = []
    monkeypatch.setattr(tmp36, "evaluate", lambda *a, **k: calls.append("t"))
    monkeypatch.setattr(cc, "evaluate", lambda *a, **k: calls.append("c"))
    _assert_refused(_evaluate(**over), outcome)
    assert not calls


@pytest.mark.parametrize("extra", [
    {"start_input": "true"}, {"c_start_input": "true"}, {"t_start_input": "false"},
    {"condition": ">="}, {"operator": "<"}, {"c_transition": "READY->RUNNING"},
    {"c_output": "true"}, {"value_v_out": "750"}, {"previous_state": "READY"},
    {"t_value_t_celsius": "25"},
])
def test_submitted_start_input_and_overrides_are_malformed(extra):
    form = {k: [v] for k, v in _form().items()}
    form.update({k: [v] for k, v in extra.items()})
    assert tcc.capture_form(form) is None


@pytest.mark.parametrize("field,value", [
    ("c_previous_state", "STOPPED"), ("t_decl_device_tmp36", "maybe"),
    ("c_screen_safety_function", "unsure"), ("decl_condition_meaning", "yes"),
])
def test_values_outside_closed_choices_are_malformed(field, value):
    form = {k: [v] for k, v in _form().items()}
    form[field] = [value]
    assert tcc.capture_form(form) is None


def test_duplicated_fields_are_malformed():
    for key in ("threshold_c", "t_value_v_out", "c_previous_state", "decl_condition_meaning"):
        form = {k: [v] for k, v in _form().items()}
        form[key] = [form[key][0], form[key][0]]
        assert tcc.capture_form(form) is None, key


# ==========================================================================
# 5. every TMP36 refusal path: no Boolean, no cycle
# ==========================================================================
@pytest.mark.parametrize("over,part", [
    ({"t_decl": {"device_tmp36": ""}}, tmp36.NOT_DECLARED),
    ({"t_screen": {"food_safety": ""}}, tmp36.NOT_DECLARED),
    ({"t_screen": {"battery_or_storage_cell": "yes"}}, tmp36.ENGINEERING_REVIEW_REQUIRED),
    ({"t_decl": {"nominal_only": "does_not_apply"}}, tmp36.MODEL_NOT_SUPPORTED),
    ({"v_out": ""}, tmp36.INVALID_NUMERIC_INPUT),
    ({"v_out": "750.1234"}, tmp36.INVALID_NUMERIC_INPUT),
    ({"v_out": "-5"}, tmp36.INVALID_NUMERIC_INPUT),
    ({"v_out": "99.999"}, tmp36.OUTSIDE_NOMINAL_MODEL_RANGE),
    ({"v_out": "1750.001"}, tmp36.OUTSIDE_NOMINAL_MODEL_RANGE),
])
def test_tmp36_refusals_propagate_with_no_partial_result(over, part, monkeypatch):
    calls = []
    monkeypatch.setattr(cc, "evaluate", lambda *a, **k: calls.append(1))
    _assert_refused(_evaluate(**over), tcc.TMP36_REFUSED, part)
    assert not calls


@pytest.mark.parametrize("state,reason,part", [
    (dc.STATE_FAILURE, dc.EXECUTION_INTEGRITY_FAILURE, tmp36.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_UNABLE, dc.SOURCE_UNAVAILABLE, tmp36.KNOWLEDGE_UNAVAILABLE),
    (dc.STATE_REFUSAL, dc.UNIT_NOT_ADMITTED, tmp36.UNIT_NOT_SUPPORTED),
    (dc.STATE_UNABLE, dc.INPUT_OUTSIDE_ADMITTED_RANGE, tmp36.UNMAPPED_OWNER_OUTCOME),
])
def test_tmp36_owner_failures_propagate(state, reason, part, monkeypatch):
    monkeypatch.setattr(dc, "execute", lambda *a, **k: {
        "state": state, "reason": reason, "outputs": None})
    calls = []
    monkeypatch.setattr(cc, "evaluate", lambda *a, **k: calls.append(1))
    _assert_refused(_evaluate(), tcc.TMP36_REFUSED, part)
    assert not calls


def test_tmp36_decimal_reference_failure_and_tampered_artifact_propagate(monkeypatch):
    real = dc.execute

    def wrong(binding, request, artifact_path=None):
        result = real(binding, request, artifact_path=artifact_path)
        result["outputs"]["t_celsius"]["value"] = 25.5
        return result
    monkeypatch.setattr(dc, "execute", wrong)
    _assert_refused(_evaluate(), tcc.TMP36_REFUSED, tmp36.KNOWLEDGE_UNAVAILABLE)
    monkeypatch.setattr(dc, "execute", real)

    def broken(*a, **k):
        raise tmp36.Tmp36KnowledgeError("artifact: unreadable")
    monkeypatch.setattr(tmp36, "load_artifact", broken)
    _assert_refused(_evaluate(), tcc.TMP36_REFUSED, tmp36.KNOWLEDGE_UNAVAILABLE)


# ==========================================================================
# 6. every 28-T4 refusal path: no partial success
# ==========================================================================
@pytest.mark.parametrize("over,part", [
    ({"previous": ""}, cc.NOT_DECLARED),
    ({"c_decl": {"two_states": ""}}, cc.NOT_DECLARED),
    ({"c_screen": {"machinery_motion": ""}}, cc.NOT_DECLARED),
    ({"c_screen": {"safety_function": "yes"}}, cc.ENGINEERING_REVIEW_REQUIRED),
    ({"c_decl": {"one_frozen_input": "does_not_apply"}}, cc.MODEL_NOT_SUPPORTED),
])
def test_control_cycle_refusals_propagate_with_no_partial_result(over, part):
    _assert_refused(_evaluate(**over), tcc.CONTROL_CYCLE_REFUSED, part)


def test_control_cycle_definition_failure_propagates(monkeypatch):
    def broken(*a, **k):
        raise cc.ControlCycleDefinitionError("artifact: unreadable")
    monkeypatch.setattr(cc, "load_artifact", broken)
    _assert_refused(_evaluate(), tcc.CONTROL_CYCLE_REFUSED, cc.DEFINITION_UNAVAILABLE)


def test_a_cycle_that_did_not_use_the_condition_is_refused(monkeypatch):
    monkeypatch.setattr(cc, "evaluate", lambda c, **k: dict(
        cc.evaluate_cycle("READY", False)))      # ignores the derived start_input
    _assert_refused(_evaluate(threshold="20"), tcc.CONTROL_CYCLE_REFUSED,
                    cc.DEFINITION_UNAVAILABLE)


# ==========================================================================
# 7. contracts and EN / AR fidelity
# ==========================================================================
def _section(path, start, end):
    body = path.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_named_consumer_exceptions_are_recorded_and_bounded():
    tmp = _norm(_section(TMP36_CONTRACT, "## 1A.", "## 2."))
    for phrase in ("ONE named request-local consumer", "engine/temperature_control_condition.py",
                   "`nominal_temperature`", "A refusal gives that consumer nothing",
                   "adds no consumer or binding to the shared deterministic calculation owner",
                   "authorizes no other consumer"):
        assert phrase in tmp, phrase
    cyc = _norm(_section(CC_CONTRACT, "## 6A.", "## 7."))
    for phrase in ("ONE named request-local consumer", "the client can never submit it there",
                   "not a reading or inference of any real signal",
                   "the §1 eligibility rule (root-only at delivery; as amended by "
                   "CONTROL-CYCLE-INTEGRATED-PART-01",
                   "for the SAME current part on both of its sides) are unchanged"):
        assert phrase in cyc, phrase


def test_composition_contract_records_semantics_and_exclusions():
    text = _norm(CONTRACT.read_text(encoding="utf-8"))
    for phrase in ("`nominal_temperature_C >= threshold_C`", "EXACT decimal values",
                   "never a binary float and never parsed from display text",
                   "INTERSECTION of the two existing gates", "there is no partial success",
                   "`RUNNING` stays `RUNNING` whatever `start_input` is",
                   "five methods, five bindings", "No new source"):
        assert phrase in text, phrase


def test_english_and_arabic_wording_equal_the_contract():
    s9 = _section(CONTRACT, "## 9. Fixed disclosure", "## 9A.")
    assert ui_text.text("UI_TCC_DISCLOSURE", "en").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)]
    a1 = _section(CONTRACT, "**A-1", "**A-2")
    assert ui_text.text("UI_TCC_DISCLOSURE", "ar").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    s5 = _section(CONTRACT, "## 5. Confirmation", "## 6.")
    en = re.search(r"^\| D-1 \| `condition_meaning` \| (.+?) \|$", s5, re.M).group(1)
    assert ui_text.text("UI_TCC_DECL_CONDITION_MEANING", "en") == en + "."
    a2 = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$", _section(CONTRACT, "**A-2", "**A-3"), re.M))
    assert ui_text.text("UI_TCC_DECL_CONDITION_MEANING", "ar") == a2["D-1 condition_meaning"]


def test_every_key_is_bilingual_and_makes_no_control_or_accuracy_claim():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_TCC_[A-Z0-9_]+)": \{', source)
    assert len(keys) >= 30
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("will switch", "turns on the", "accurate temperature reading",
                  "measured temperature is", "certified", "has been validated",
                  "the threshold is safe"):
        assert claim not in english, claim
    for phrase in ("not a measurement", "controls nothing", "no partial result",
                   "you do not choose start_input"):
        assert phrase in english, phrase


# ==========================================================================
# 8. the web surface
# ==========================================================================
def test_electronics_root_journey(elec):
    c, _aid, sid = elec
    assert "data-tcc-link" in _page(c, sid)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-tcc-form" in body and " checked>" not in body
    assert 'name="start_input"' not in body and 'name="c_start_input"' not in body
    body = c.post(URL % sid, data=_form(v_out="750.1", threshold="25.01")).get_data(as_text=True)
    assert _field(body, "voltage") == "750.1 mV"
    assert _field(body, "temperature") == "25.01 °C"
    assert _field(body, "threshold") == "25.01 °C"
    assert 'data-tcc-condition="true"' in body
    assert _field(body, "start-input") == "true"
    assert _field(body, "next") == "RUNNING" and _field(body, "output") == "true"
    assert "UNVALIDATED" in body and "NOT EVIDENCE" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_TCC_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    for marker in ("data-tcc-tmp36-disclosure", "data-tcc-cc-disclosure",
                   "tmp36:nominal_voltage_to_temperature",
                   "control_cycle:ready_running_single_transition",
                   "temperature_control_condition:tmp36_threshold_ready_running"):
        assert marker in body, marker


@pytest.mark.parametrize("previous,threshold,next_state,output", [
    ("READY", "30", "READY", "false"), ("RUNNING", "30", "RUNNING", "true"),
    ("RUNNING", "20", "RUNNING", "true"), ("READY", "20", "RUNNING", "true")])
def test_page_cycle_results(elec, previous, threshold, next_state, output):
    c, _aid, sid = elec
    body = c.post(URL % sid, data=_form(threshold=threshold, previous=previous)).get_data(as_text=True)
    assert (_field(body, "next"), _field(body, "output")) == (next_state, output)


@pytest.mark.parametrize("over,key", [
    ({"v_out": "2000"}, "UI_TMP36_OUTCOME_OUTSIDE_NOMINAL_MODEL_RANGE"),
    ({"c_screen": {"safety_function": "yes"}}, "UI_CC_OUTCOME_ENGINEERING_REVIEW_REQUIRED"),
    ({"threshold": "126"}, "UI_TCC_OUTCOME_THRESHOLD_OUTSIDE_RANGE"),
    ({"meaning": "does_not_apply"}, "UI_TCC_OUTCOME_MODEL_NOT_SUPPORTED"),
])
def test_page_refusals_show_one_reason_and_nothing_else(elec, over, key):
    c, _aid, sid = elec
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert ui_text.text(key, "en") in html.unescape(body)
    assert body.count("data-tcc-outcome") == 1
    for name in ("temperature", "condition", "start-input", "next", "output"):
        assert _field(body, name) is None, name


@pytest.mark.parametrize("bad", [
    {"c_start_input": "true"}, {"start_input": "false"}, {"c_output": "true"},
    {"c_previous_state": "STOPPED"}])
def test_malformed_and_injected_start_input_are_400(elec, bad):
    c, _aid, sid = elec
    r = c.post(URL % sid, data=dict(_form(), **bad))
    assert r.status_code == 400 and _field(r.get_data(as_text=True), "next") is None
    r = c.post(URL % sid, data=MultiDict(list(_form().items()) + [("threshold_c", "25")]))
    assert r.status_code == 400


def test_eligibility_is_the_intersection_of_both_gates(mech, monkeypatch):
    c, _aid, sid = mech
    assert "data-tcc-link" not in _page(c, sid)
    assert webapp._tcc_eligible(sid) is False
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-tcc-form" not in body and _field(body, "next") is None
    c2, _ = _client_for("tcc-part@example.com")
    part_sid = _integrated(c2, MECH)            # both gates resolve to the SAME declared part
    assert webapp._calc_gate(part_sid, tmp36)[0] is True
    assert webapp._control_cycle_eligible(part_sid) is True   # CONTROL-CYCLE-INTEGRATED-PART-01
    assert webapp._tcc_eligible(part_sid) is True
    assert webapp._tcc_gate(part_sid)[1].domain == ELEC
    assert "data-tcc-link" in _page(c2, part_sid)
    root_sid = _integrated(c2, ELEC)            # Electronics focus: both gates admit
    assert webapp._tcc_eligible(root_sid) is True
    monkeypatch.setattr(webapp, "_calc_gate", lambda *a: (False, None))
    assert webapp._tcc_eligible(root_sid) is False


def test_csrf_and_project_authorization(elec):
    c, _aid, sid = elec
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("tcc-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302 and "data-tcc" not in r.get_data(as_text=True)


def test_requests_are_isolated(elec):
    c, _aid, sid = elec
    c.post(URL % sid, data=_form(threshold="20", previous="READY"))      # -> RUNNING
    body = c.post(URL % sid, data=_form(threshold="30", previous="READY")).get_data(as_text=True)
    assert _field(body, "next") == "READY"          # nothing carried from the last request


@pytest.mark.parametrize("over", [{}, {"v_out": "2000"}, {"c_screen": {"safety_function": "yes"}}])
def test_nothing_is_persisted(elec, over):
    c, _aid, sid = elec
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_no_report_export_api_or_safety_surface():
    src = Path(webapp.__file__).read_text(encoding="utf-8")
    start = src.index("# TEMPERATURE-TO-CONTROL-CONDITION-01 — TMP36 nominal temperature")
    section = src[start:src.index("# DC-RESISTIVE-LOAD-CURRENT-01 —", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_dcalc.bind_method", "request.args", "session[", "control_loop"):
        assert banned not in section, banned
    assert section.count("_TMP36_TEMPERATURE_BINDING") == 1
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 12
    assert [r.rule for r in webapp.app.url_map.iter_rules()
            if "temperature-control-condition" in r.rule] \
        == ["/session/<sid>/temperature-control-condition"] * 2


def test_standalone_tmp36_and_control_cycle_are_unchanged(elec):
    c, _aid, sid = elec
    body = c.post("/session/%s/tmp36-temperature" % sid, data=_tmp36_form(v_out="750.1")
                  ).get_data(as_text=True)
    assert '<bdi dir="ltr">25.01 °C</bdi>' in body and "data-tcc" not in body
    body = c.post("/session/%s/control-cycle" % sid,
                  data=_cc_form(previous="RUNNING", start_input="false")).get_data(as_text=True)
    assert "data-cc-result-next><bdi dir=\"ltr\">RUNNING</bdi>" in body
    r = c.post("/session/%s/control-cycle" % sid, data=dict(_cc_form(), threshold_c="25"))
    assert r.status_code == 400                     # the 28-T4 input contract is unchanged
    r = c.post("/session/%s/tmp36-temperature" % sid, data=dict(_tmp36_form(), threshold_c="25"))
    assert r.status_code == 400


def test_arabic_page_is_rtl_with_isolated_tokens():
    c, _ = _client_for("tcc-ar@example.com")
    sid = _start(c, ELEC_FORM)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form(v_out="499.999", threshold="-0.0001")).get_data(as_text=True)
    assert 'dir="rtl"' in body
    assert _field(body, "temperature") == "-0.0001 °C"
    assert 'data-tcc-condition="true"' in body
    isolated = re.findall(r'<bdi dir="ltr">([^<]*)</bdi>', body)
    for token in ("TMP36", "start_input", "READY", "RUNNING", "UNVALIDATED", "NOT EVIDENCE"):
        assert any(token in run for run in isolated), token
    stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
    for item in ui_text.text("UI_TCC_DISCLOSURE", "ar").split("\n\n"):
        assert _norm(item) in _norm(stripped), item[:30]
