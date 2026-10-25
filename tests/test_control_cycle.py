# -*- coding: utf-8 -*-
"""Stage 28 / 28-T4 - Single Vendor-Neutral Control-Cycle Evaluation, Slice 1 (directly owning tests).

28-T4 CONTROL-CYCLE-SLICE-01. ONE fixed READY / RUNNING definition, ONE bounded
module (``engine/control_cycle.py``) and its request-local page. The four
reference cases are checked at module, consumer and page level; the expected
results are written out here by hand from the Owner's table, never computed by
the module under test. Synthetic data.
"""
import copy
import html
import json
import re
from pathlib import Path

import pytest
from werkzeug.datastructures import MultiDict

import web.app as webapp
from web import ui_text
from engine import control_cycle as cc
from engine import deterministic_calculation as dc
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, _content_text, SEED,
    ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, MECH, ELEC)
from tests.test_therm01_temperature_difference import _form as _therm_form
from tests.test_tmp36_nominal_temperature import _form as _tmp36_form
from tests.test_cap13_static_reactions import _form as _cap13_form
from tests.test_cap13_planar_moment import _form as _moment_form
from tests.test_cap13_rotational_load import _form as _rotational_form

ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "docs" / "governance" / "STAGE28_T4_CONTROL_CYCLE_READY_RUNNING_CONTRACT.md"
URL = "/session/%s/control-cycle"
# The Owner's table: (previous, input) -> (next, output, transition status).
REFERENCE = (
    ("READY", True, "RUNNING", True, "APPLIED"),
    ("READY", False, "READY", False, "NOT_APPLIED_CONDITION_FALSE"),
    ("RUNNING", True, "RUNNING", True, "NOT_APPLICABLE_FROM_STATE"),
    ("RUNNING", False, "RUNNING", True, "NOT_APPLICABLE_FROM_STATE"),
)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _form(previous="READY", start_input="true", decl=None, screen=None):
    form = {cc.DECLARATION_FIELD % d: cc.ANSWER_APPLIES for d in cc.DECLARATION_IDS}
    form.update({cc.SCREEN_FIELD % s: cc.SCREEN_NO for s in cc.SCREEN_ITEMS})
    form[cc.PREVIOUS_STATE_FIELD] = previous
    form[cc.INPUT_FIELD] = start_input
    for key, value in (decl or {}).items():
        form[cc.DECLARATION_FIELD % key] = value
    for key, value in (screen or {}).items():
        form[cc.SCREEN_FIELD % key] = value
    return form


def _captured(**kw):
    captured = cc.capture_form({k: [v] for k, v in _form(**kw).items()})
    assert captured is not None
    return captured


def _evaluate(**kw):
    return cc.evaluate(_captured(**kw))


def _artifact():
    return json.loads(cc.ARTIFACT_PATH.read_text(encoding="utf-8"))


def _write(tmp_path, text):
    target = tmp_path / "a.json"
    target.write_text(text, encoding="utf-8")
    return target


def _field(body, name):
    marker = "data-cc-result-%s>" % name
    if marker not in body:
        return None
    cell = body.split(marker, 1)[1].split("</dd>", 1)[0]
    return html.unescape(re.sub(r"<[^>]+>", "", cell)).strip()


def _norm(text):
    return re.sub(r"\s+", " ", text.replace("**", "")).strip()


@pytest.fixture
def elec():
    c, aid = _client_for("cc-elec@example.com")
    return c, aid, _start(c, ELEC_FORM)


@pytest.fixture
def mech():
    c, aid = _client_for("cc-mech@example.com")
    return c, aid, _start(c, {"idea": SEED, "domain_confirm": MECH})


# ==========================================================================
# 1. the four reference cases and the next-state output rule
# ==========================================================================
@pytest.mark.parametrize("previous,start_input,next_state,output,status", REFERENCE)
def test_reference_cases_at_module_and_consumer(previous, start_input, next_state,
                                                output, status):
    result = cc.evaluate_cycle(previous, start_input)
    assert result == {
        "outcome": "SUCCESS", "previous_state": previous, "frozen_input": start_input,
        "transition_status": status, "transition_applied": status == "APPLIED",
        "next_state": next_state, "output": output,
        "method_id": "control_cycle:ready_running_single_transition",
        "method_version": "1.0", "validation_status": "UNVALIDATED"}
    consumer = _evaluate(previous=previous, start_input="true" if start_input else "false")
    assert consumer == result


def test_output_is_read_from_the_next_state_not_the_previous_state():
    applied = cc.evaluate_cycle("READY", True)
    # the previous state READY maps to false; the next state RUNNING maps to true
    assert cc.DEFINITION["output_map"]["READY"] is False
    assert applied["output"] is True
    assert applied["output"] == cc.DEFINITION["output_map"][applied["next_state"]]
    assert applied["output"] != cc.DEFINITION["output_map"][applied["previous_state"]]


def test_no_transition_results_are_successes_not_refusals():
    for previous, start_input in (("READY", False), ("RUNNING", True), ("RUNNING", False)):
        result = cc.evaluate_cycle(previous, start_input)
        assert result["outcome"] == cc.OUTCOME_SUCCESS
        assert result["transition_applied"] is False
        assert result["next_state"] == previous
    assert cc.evaluate_cycle("RUNNING", True)["transition_status"] \
        == cc.TRANSITION_NOT_APPLICABLE        # the source is READY: never fired


def test_the_input_is_frozen_and_nothing_is_kept_between_calls():
    sequence = [cc.evaluate_cycle(p, i) for p, i in
                (("READY", True), ("READY", False), ("RUNNING", False), ("READY", False))]
    assert [r["next_state"] for r in sequence] == ["RUNNING", "READY", "RUNNING", "READY"]
    assert cc.evaluate_cycle("READY", False)["next_state"] == "READY"   # no carried state
    source = Path(cc.__file__).read_text(encoding="utf-8")
    for banned in ("global ", "session[", "SESSION_STORE", "cache", "lru_cache",
                   "_get_store", "record_store", "import time", "import random"):
        assert banned not in source, banned


# ==========================================================================
# 2. refusals at the module level
# ==========================================================================
@pytest.mark.parametrize("state", ["STOPPED", "ready", "Ready", " READY", "", None, 1,
                                   "IDLE", "RUNNING\n"])
def test_unknown_previous_state_is_refused(state):
    assert cc.evaluate_cycle(state, True) == {"outcome": cc.UNKNOWN_STATE}


@pytest.mark.parametrize("value", [1, 0, "true", "false", None, 1.0, [], "yes"])
def test_non_boolean_input_snapshot_is_refused(value):
    assert cc.evaluate_cycle("READY", value) == {"outcome": cc.INVALID_INPUT_SNAPSHOT}


def _definition_mutations():
    def m(fn):
        d = copy.deepcopy(cc.DEFINITION)
        fn(d)
        return d
    return [
        ("extra_state", m(lambda d: d["states"].append("STOPPED"))),
        ("duplicate_state", m(lambda d: d["states"].__setitem__(1, "READY"))),
        ("renamed_state", m(lambda d: d["states"].__setitem__(1, "ON"))),
        ("second_transition", m(lambda d: d["transitions"].append(
            {"source": "RUNNING", "condition": {"input": "start_input", "equals": False},
             "target": "READY"}))),
        ("no_transition", m(lambda d: d["transitions"].clear())),
        ("unknown_source", m(lambda d: d["transitions"][0].__setitem__("source", "IDLE"))),
        ("source_equals_target", m(lambda d: d["transitions"][0].__setitem__("source", "RUNNING"))),
        ("reversed", m(lambda d: d["transitions"][0].update(source="RUNNING", target="READY"))),
        ("condition_input", m(lambda d: d["transitions"][0]["condition"].__setitem__("input", "stop"))),
        ("condition_not_bool", m(lambda d: d["transitions"][0]["condition"].__setitem__("equals", 1))),
        ("condition_inverted", m(lambda d: d["transitions"][0]["condition"].__setitem__("equals", False))),
        ("condition_expression", m(lambda d: d["transitions"][0]["condition"].__setitem__("expr", "x"))),
        ("missing_output_entry", m(lambda d: d["output_map"].pop("RUNNING"))),
        ("extra_output_entry", m(lambda d: d["output_map"].__setitem__("STOPPED", False))),
        ("output_not_bool", m(lambda d: d["output_map"].__setitem__("RUNNING", 1))),
        ("contradictory_output", m(lambda d: d["output_map"].update(READY=True, RUNNING=False))),
        ("input_not_boolean", m(lambda d: d["input"].__setitem__("type", "number"))),
        ("unknown_key", m(lambda d: d.__setitem__("callback", "lambda s: s"))),
    ]


@pytest.mark.parametrize("name,definition", _definition_mutations())
def test_conflicting_or_unsupported_definitions_fail_closed(name, definition):
    with pytest.raises(cc.ControlCycleDefinitionError):
        cc.validate_definition(definition)
    assert cc.evaluate_cycle("READY", True, definition=definition) \
        == {"outcome": cc.DEFINITION_UNAVAILABLE}, name


def test_duplicate_key_rule_representations_fail_closed(tmp_path):
    raw = cc.ARTIFACT_PATH.read_text(encoding="utf-8")
    duplicated = raw.replace('"output_map": {"READY": false, "RUNNING": true}',
                             '"output_map": {"READY": false, "RUNNING": true, "RUNNING": false}')
    assert duplicated != raw
    with pytest.raises(cc.ControlCycleDefinitionError):
        cc.load_artifact(_write(tmp_path, duplicated))
    twice = raw.replace('"transitions": [', '"transitions": [], "transitions": [', 1)
    with pytest.raises(cc.ControlCycleDefinitionError):
        cc.load_artifact(_write(tmp_path, twice))


@pytest.mark.parametrize("mutate", [
    lambda d: d["definition"]["output_map"].__setitem__("READY", True),
    lambda d: d["definition"]["states"].append("STOPPED"),
    lambda d: d["method"].__setitem__("output_rule", "The output is read from the previous state."),
    lambda d: d["declarations"][2].__setitem__("accepted_value", "the output follows the input"),
    lambda d: d["declarations"][0].__setitem__("refusal", "NOT_DECLARED"),
    lambda d: d["screen_items"].pop(0),
    lambda d: d["disclosure"].pop(),
    lambda d: d["sources"][0].__setitem__("inspected_content", "IEC 61131-3 conformant scan."),
    lambda d: d["sources"][0].__setitem__("source_use_policy_ref", "cap13r:SU001"),
    lambda d: d["method"].__setitem__("method_version", "2.0"),
    lambda d: d.__setitem__("artifact_version", "2"),
    lambda d: d.__setitem__("transition_table", []),
])
def test_artifact_tamper_is_definition_unavailable(mutate):
    data = _artifact()
    mutate(data)
    with pytest.raises(cc.ControlCycleDefinitionError):
        cc.validate_artifact(data)
    assert cc.evaluate(_captured(), artifact=data) == {"outcome": cc.DEFINITION_UNAVAILABLE}


def test_missing_or_unreadable_artifact_is_definition_unavailable(tmp_path, monkeypatch):
    monkeypatch.setattr(cc, "ARTIFACT_PATH", tmp_path / "absent.json")
    assert cc.evaluate(_captured()) == {"outcome": cc.DEFINITION_UNAVAILABLE}
    target = _write(tmp_path, "{not json")
    monkeypatch.setattr(cc, "ARTIFACT_PATH", target)
    assert cc.evaluate(_captured()) == {"outcome": cc.DEFINITION_UNAVAILABLE}


def test_pinned_definition_and_artifact_agree():
    data = cc.load_artifact()
    assert data["definition"] == cc.DEFINITION
    assert cc.validate_definition(cc.DEFINITION) is cc.DEFINITION
    assert cc.STATES == ("READY", "RUNNING")


# ==========================================================================
# 3. capture and the pre-evaluation order
# ==========================================================================
@pytest.mark.parametrize("extra", [
    {"transition": "READY->RUNNING"}, {"target_state": "RUNNING"},
    {"next_state": "RUNNING"}, {"output": "true"}, {"output_map": "{}"},
    {"condition": "start_input == false"}, {"states": "READY,RUNNING,STOPPED"},
    {"callback": "lambda s: s"}, {"source_state": "RUNNING"},
])
def test_override_attempts_are_malformed_and_never_evaluated(extra):
    form = {k: [v] for k, v in _form().items()}
    form.update({k: [v] for k, v in extra.items()})
    assert cc.capture_form(form) is None


@pytest.mark.parametrize("field,value", [
    (cc.PREVIOUS_STATE_FIELD, "STOPPED"), (cc.PREVIOUS_STATE_FIELD, "ready"),
    (cc.INPUT_FIELD, "1"), (cc.INPUT_FIELD, "True"), (cc.INPUT_FIELD, "on"),
    (cc.INPUT_FIELD, "yes"), (cc.DECLARATION_FIELD % "two_states", "maybe"),
    (cc.SCREEN_FIELD % "safety_function", "unsure"),
])
def test_values_outside_the_closed_choices_are_malformed(field, value):
    form = {k: [v] for k, v in _form().items()}
    form[field] = [value]
    assert cc.capture_form(form) is None


def test_duplicated_fields_are_malformed():
    form = {k: [v] for k, v in _form().items()}
    form[cc.INPUT_FIELD] = ["true", "false"]
    assert cc.capture_form(form) is None
    form = {k: [v] for k, v in _form().items()}
    form[cc.PREVIOUS_STATE_FIELD] = ["READY", "READY"]
    assert cc.capture_form(form) is None
    assert cc.capture_form([("previous_state", "READY")]) is None


def test_pre_evaluation_order_first_failing_stage_wins():
    assert _evaluate(previous="", screen={"safety_function": "yes"})["outcome"] \
        == cc.NOT_DECLARED
    assert _evaluate(start_input="")["outcome"] == cc.NOT_DECLARED
    assert _evaluate(decl={"two_states": ""})["outcome"] == cc.NOT_DECLARED
    assert _evaluate(screen={"heating_or_fire": "yes"},
                     decl={"one_transition": "does_not_apply"})["outcome"] \
        == cc.ENGINEERING_REVIEW_REQUIRED
    for item in cc.SCREEN_ITEMS:
        assert _evaluate(screen={item: "yes"})["outcome"] \
            == cc.ENGINEERING_REVIEW_REQUIRED, item
    for decl in cc.DECLARATION_IDS:
        assert _evaluate(decl={decl: "does_not_apply"})["outcome"] \
            == cc.MODEL_NOT_SUPPORTED, decl
    for outcome in (cc.NOT_DECLARED, cc.ENGINEERING_REVIEW_REQUIRED, cc.MODEL_NOT_SUPPORTED):
        assert set(_evaluate(**{"NOT_DECLARED": {"previous": ""},
                                "ENGINEERING_REVIEW_REQUIRED": {"screen": {"safety_function": "yes"}},
                                "MODEL_NOT_SUPPORTED": {"decl": {"logical_only": "does_not_apply"}}}
                              [outcome])) == {"outcome"}


def test_module_is_bounded_and_imports_no_other_authority():
    import ast
    tree = ast.parse(Path(cc.__file__).read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.add(node.module or "")
    assert names <= {"hashlib", "json", "re", "pathlib"}, names
    source = Path(cc.__file__).read_text(encoding="utf-8")
    for banned in ("eval(", "exec(", "getattr(", "importlib", "lambda", "__import__"):
        assert banned not in source, banned
    assert not re.search(r"(?<!re\.)compile\(", source)


def test_not_a_method_of_the_shared_calculation_owner():
    assert all(not m.startswith("control_cycle") for m, _ in dc.ADMITTED_METHODS)
    assert len(dc.ADMITTED_METHODS) == 5 and dc.IMPLEMENTATION_VERSION == "1.4.0"
    assert dc.load_artifact()["artifact_version"] == "5"
    assert Path(webapp.__file__).read_text(encoding="utf-8").count("_dcalc.bind_method(") == 5


# ==========================================================================
# 4. provenance, IP and the contract
# ==========================================================================
def test_source_record_states_reference_only_and_licence():
    data = cc.load_artifact()
    by_id = {r["record_id"]: r for r in data["sources"]}
    source = by_id["OPENPLC-S1"]
    assert "8d69d935a7915bef9b67bbea46cf87c68d112246" in source["source_title"]
    upstream = ("https://github.com/Autonomy-Logic/openplc-runtime/tree/"
                "8d69d935a7915bef9b67bbea46cf87c68d112246")
    assert source["url"] == by_id["oplc:SU001"]["url"] == upstream
    assert upstream in CONTRACT.read_text(encoding="utf-8")
    assert "not recorded" not in json.dumps(data["sources"])
    for phrase in ("factual reference", "does NOT support",
                   "InventorAI's own design", "not re-inspected by the executor"):
        assert phrase in source["inspected_content"], phrase
    policy = by_id["oplc:SU001"]
    for phrase in ("MIT", "(c) 2026 Autonomy", "not a legal opinion", "no notice-retention"):
        assert phrase in policy["inspected_content"] + policy["acknowledgement"], phrase
    assert "endorse" in policy["no_endorsement_limitation"]
    assert "InventorAI's own design decision" in data["method"]["output_rule"]


def test_no_external_source_or_dependency_enters_the_repository():
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        assert "openplc" not in path.name.lower(), path
    for manifest in ("requirements.txt", "pyproject.toml", "setup.cfg"):
        target = ROOT / manifest
        if target.exists():
            assert "openplc" not in target.read_text(encoding="utf-8").lower()


def _contract_section(start, end):
    body = CONTRACT.read_text(encoding="utf-8")
    return body[body.index(start):body.index(end)]


def test_contract_records_semantics_reference_cases_and_exclusions():
    text = _norm(CONTRACT.read_text(encoding="utf-8"))
    for phrase in ("8d69d935a7915bef9b67bbea46cf87c68d112246", "MIT", "2026 Autonomy",
                   "NOT a claimed OpenPLC, PLC or IEC 61131-3 execution semantic",
                   "A declared Stage 15 part grants NOTHING here",
                   "stays exactly as it is (PART-ONLY, one optional part, NOT root-activated)",
                   "NOT a method of the shared deterministic calculation owner",
                   "the Stage 30 new-domain-activation trigger recorded for 28-T4 does not fire",
                   "| RUNNING | false | NOT_APPLICABLE_FROM_STATE | RUNNING | true |",
                   "| READY | true | APPLIED | RUNNING | true |"):
        assert phrase in text, phrase


def test_english_wording_equals_the_artifact():
    content = cc.load_artifact()
    assert ui_text.text("UI_CC_DISCLOSURE", "en").split("\n\n") == content["disclosure"]
    for entry in content["declarations"]:
        value = entry["accepted_value"]
        assert ui_text.text("UI_CC_DECL_" + entry["declaration_id"].upper(), "en") \
            == value[0].upper() + value[1:] + "."
    for entry in content["screen_items"]:
        value = entry["item"]
        assert ui_text.text("UI_CC_SCREEN_" + entry["item_id"].upper(), "en") \
            == value[0].upper() + value[1:]
    s9 = _contract_section("## 9. Fixed disclosure", "## 9A.")
    assert [m.group(1) for m in re.finditer(r"^\d\. (.*)$", s9, re.M)] == content["disclosure"]


def test_arabic_wording_equals_the_contract():
    a1 = _contract_section("**A-1", "**A-2")
    assert ui_text.text("UI_CC_DISCLOSURE", "ar").split("\n\n") \
        == [m.group(1) for m in re.finditer(r"^> \d\. (.*)$", a1, re.M)]
    rows = dict(re.findall(r"^\| (D-\d \w+) \| (.+?) \|$",
                           _contract_section("**A-2", "**A-3"), re.M))
    for decl, ref in cc.DECLARATIONS:
        assert ui_text.text("UI_CC_DECL_" + decl.upper(), "ar") == rows["%s %s" % (ref, decl)]
    screen = dict(re.findall(r"^\| (\w+) \| (.+?) \|$",
                             _contract_section("**A-3", "**A-4"), re.M))
    for item in cc.SCREEN_ITEMS:
        assert ui_text.text("UI_CC_SCREEN_" + item.upper(), "ar") == screen[item]


def test_every_key_has_both_languages_and_no_device_or_safety_claim():
    source = Path(ui_text.__file__).read_text(encoding="utf-8")
    keys = re.findall(r'"(UI_CC_[A-Z0-9_]+)": \{', source)
    assert len(keys) >= 40
    for key in keys:
        for lang in ("en", "ar"):
            assert ui_text.text(key, lang).strip(), (key, lang)
    english = " ".join(ui_text.text(k, "en") for k in keys).lower()
    for claim in ("will start the", "starts the motor", "energizes the", "the logic is safe",
                  "iec 61131-3 compliant", "conforms to iec", "plc-equivalent",
                  "guaranteed timing", "certified", "has been validated"):
        assert claim not in english, claim
    for phrase in ("controls nothing", "logical value only", "normal result",
                   "inventorai's own design", "no iec 61131-3 conformity is claimed"):
        assert phrase in english, phrase


# ==========================================================================
# 5. the web surface: gate, journey, integrity, isolation, no persistence
# ==========================================================================
def test_electronics_root_journey_and_reference_cases(elec):
    c, _aid, sid = elec
    assert "data-cc-link" in _page(c, sid)
    body = c.get(URL % sid).get_data(as_text=True)
    assert "data-cc-form" in body and " checked>" not in body
    assert "data-cc-definition" in body
    for previous, start_input, next_state, output, status in REFERENCE:
        body = c.post(URL % sid, data=_form(previous, "true" if start_input else "false")
                      ).get_data(as_text=True)
        assert _field(body, "previous") == previous
        assert _field(body, "input") == ("true" if start_input else "false")
        assert _field(body, "next") == next_state
        assert _field(body, "output") == ("true" if output else "false")
        assert 'data-cc-transition-status="%s"' % status in body
        assert _norm(ui_text.text("UI_CC_TRANSITION_" + status, "en")) \
            in _norm(html.unescape(_content_text(body)))
        assert "data-cc-outcome" not in body       # a no-transition result is no refusal
    assert "UNVALIDATED" in body and "NOT EVIDENCE" in body
    text = _norm(html.unescape(_content_text(body)))
    for item in ui_text.text("UI_CC_DISCLOSURE", "en").split("\n\n"):
        assert _norm(item) in text
    assert "control_cycle:ready_running_single_transition" in body


def test_requests_are_isolated_and_nothing_is_carried(elec):
    c, _aid, sid = elec
    c.post(URL % sid, data=_form("READY", "true"))
    body = c.post(URL % sid, data=_form("READY", "false")).get_data(as_text=True)
    assert _field(body, "next") == "READY" and _field(body, "output") == "false"
    other, _ = _client_for("cc-isolation@example.com")
    sid2 = _start(other, ELEC_FORM)
    other.post(URL % sid2, data=_form("RUNNING", "false"))
    body = c.post(URL % sid, data=_form("READY", "false")).get_data(as_text=True)
    assert _field(body, "next") == "READY"


@pytest.mark.parametrize("over,outcome", [
    ({"screen": {"safety_function": "yes"}}, "ENGINEERING_REVIEW_REQUIRED"),
    ({"decl": {"logical_only": "does_not_apply"}}, "MODEL_NOT_SUPPORTED"),
    ({"previous": ""}, "NOT_DECLARED"),
    ({"start_input": ""}, "NOT_DECLARED"),
])
def test_refusals_show_one_reason_and_no_state_or_output(elec, over, outcome):
    c, _aid, sid = elec
    body = c.post(URL % sid, data=_form(**over)).get_data(as_text=True)
    assert ui_text.text("UI_CC_OUTCOME_" + outcome, "en") in html.unescape(body)
    assert body.count("data-cc-outcome") == 1
    assert _field(body, "next") is None and _field(body, "output") is None


@pytest.mark.parametrize("bad", [
    {"transition": "READY->RUNNING"}, {"output": "false"}, {"next_state": "READY"},
    {cc.PREVIOUS_STATE_FIELD: "STOPPED"}, {cc.INPUT_FIELD: "1"},
])
def test_malformed_and_override_requests_are_400(elec, bad):
    c, _aid, sid = elec
    r = c.post(URL % sid, data=dict(_form(), **bad))
    body = r.get_data(as_text=True)
    assert r.status_code == 400 and _field(body, "next") is None
    assert ui_text.text("UI_CC_ERR_REQUEST", "en") in html.unescape(body)


def test_duplicated_field_request_is_400(elec):
    c, _aid, sid = elec
    r = c.post(URL % sid, data=MultiDict(list(_form().items())
                                         + [(cc.INPUT_FIELD, "false")]))
    assert r.status_code == 400 and _field(r.get_data(as_text=True), "next") is None


def test_mechanical_root_is_unsupported(mech, monkeypatch):
    c, _aid, sid = mech
    assert "data-cc-link" not in _page(c, sid)
    called = []
    monkeypatch.setattr(webapp._cc, "evaluate", lambda *a, **k: called.append(1))
    for r in (c.get(URL % sid), c.post(URL % sid, data=_form())):
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-cc-scope-note" in body
        assert "data-cc-form" not in body and _field(body, "next") is None
    assert not called


def test_a_declared_electronics_part_grants_nothing(monkeypatch):
    c, _ = _client_for("cc-part@example.com")
    sid = _integrated(c, MECH)          # Mechanical focus with a declared Electronics part
    assert any(s.domain == ELEC for s in webapp._get_store().load_project_subsystems(sid))
    assert webapp._control_cycle_eligible(sid) is False
    assert "data-cc-link" not in _page(c, sid)
    body = c.post(URL % sid, data=_form()).get_data(as_text=True)
    assert "data-cc-form" not in body and _field(body, "next") is None
    sid2 = _integrated(c, ELEC)         # Electronics focus: eligible through the root only
    assert webapp._control_cycle_eligible(sid2) is True
    monkeypatch.setattr(webapp, "_cap12_root_domain", lambda _sid: None)
    assert webapp._control_cycle_eligible(sid2) is False


def test_csrf_and_project_authorization(elec):
    c, _aid, sid = elec
    assert webapp.app.test_client().post(URL % sid, data=_form()).status_code == 403
    other, _ = _client_for("cc-other@example.com")
    for client in (other, _new_client()):
        for r in (client.get(URL % sid), client.post(URL % sid, data=_form())):
            assert r.status_code == 302 and "data-cc" not in r.get_data(as_text=True)


@pytest.mark.parametrize("over", [{}, {"previous": "RUNNING", "start_input": "false"},
                                  {"screen": {"machinery_motion": "yes"}}])
def test_nothing_is_persisted(elec, over):
    c, _aid, sid = elec
    _page(c, sid)
    before = _snapshot(c)
    c.post(URL % sid, data=_form(**over))
    c.get(URL % sid)
    assert _snapshot(c) == before


def test_no_report_export_api_control_loop_or_safety_surface():
    src = Path(webapp.__file__).read_text(encoding="utf-8")
    start = src.index("# 28-T4 — Single Vendor-Neutral Control-Cycle Evaluation")
    section = src[start:src.index("# TEMPERATURE-TO-CONTROL-CONDITION-01 —", start)]
    for banned in ("safety_signal", "SafetySignal(", "_get_store()", "append_",
                   "SESSION_STORE[", "deliverable", "pdf", "export", "/api/",
                   "_calc_gate", "_calc_declared_part", "load_project_subsystems",
                   "_dcalc", "request.args", "session["):
        assert banned not in section, banned
    code = "\n".join(line for line in section.splitlines()
                     if not line.strip().startswith("#"))
    assert "control_loop" not in code and "subsystem" not in code
    assert [r.rule for r in webapp.app.url_map.iter_rules() if "control-cycle" in r.rule] \
        == ["/session/<sid>/control-cycle"] * 2
    for template in ("deliverable.html", "report.html", "success_criteria.html",
                     "parts_components_interactions.html"):
        path = ROOT / "web" / "templates" / template
        if path.exists():
            assert "control-cycle" not in path.read_text(encoding="utf-8")


def test_control_loop_activation_and_stage15_boundaries_are_unchanged():
    from engine import domain_activation, subsystem_model
    assert domain_activation._PART_ONLY_DOMAINS == frozenset({"control_loop"}) \
        or tuple(domain_activation._PART_ONLY_DOMAINS) == ("control_loop",)
    assert "control_loop" not in domain_activation.activated_domains()
    assert "control_cycle" not in Path(subsystem_model.__file__).read_text(encoding="utf-8")
    assert "control_cycle" not in Path(domain_activation.__file__).read_text(encoding="utf-8")


def test_existing_calculations_are_unchanged(mech, elec):
    c, _aid, sid = mech
    body = c.post("/session/%s/support-reactions" % sid, data=_cap13_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">750.0 N</bdi>' in body
    body = c.post("/session/%s/planar-moment" % sid, data=_moment_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">1000.0 N·mm</bdi>' in body
    body = c.post("/session/%s/rotational-load" % sid, data=_rotational_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">-1.0 N·m</bdi>' in body
    c2, _aid2, sid2 = elec
    body = c2.post("/session/%s/temperature-difference" % sid2, data=_therm_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">25.0 K</bdi>' in body
    body = c2.post("/session/%s/tmp36-temperature" % sid2, data=_tmp36_form()).get_data(as_text=True)
    assert '<bdi dir="ltr">25.0 °C</bdi>' in body


def test_arabic_page_is_rtl_with_isolated_tokens():
    c, _ = _client_for("cc-ar@example.com")
    sid = _start(c, ELEC_FORM)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    body = c.post(URL % sid, data=_form("READY", "true")).get_data(as_text=True)
    assert 'dir="rtl"' in body
    assert _field(body, "next") == "RUNNING" and _field(body, "output") == "true"
    isolated = re.findall(r'<bdi dir="ltr">([^<]*)</bdi>', body)
    for token in ("READY", "RUNNING", "start_input", "true", "false", "UNVALIDATED",
                  "NOT EVIDENCE", "OpenPLC", "IEC 61131-3", "interlock"):
        assert any(token in run for run in isolated), token
    stripped = html.unescape(re.sub(r"<[^>]+>", "", body))
    for item in ui_text.text("UI_CC_DISCLOSURE", "ar").split("\n\n"):
        assert _norm(item) in _norm(stripped), item[:30]
