"""CONTROL-CYCLE-INTEGRATED-PART-01 — the existing 28-T4 READY / RUNNING
evaluation and the existing TMP36 -> threshold -> cycle composition may be
OFFERED for the inventor-declared Electrical / Electronics part of a valid
durable Stage 15 integrated composition, whatever the initial analysis focus.

Eligibility only changes: the 28-T4 page reads the SAME shared rule the admitted
calculations read (``_calc_gate``), and the composition is the INTERSECTION of
its two existing gates resolved to the SAME current part (the same durable
``subsystem_id``) — two separate True results never establish that. Root
behaviour is unchanged; a withdrawn, replaced, stale, malformed, corrupt or
unreadable composition grants nothing beyond the root rule; nothing from the
request grants eligibility; GET and POST read the same current authority; the
control-cycle definition, the composition semantics and the numbers are
identical on the part. Synthetic invention data only.
"""
import html
import re
from pathlib import Path

import pytest

import web.app as webapp
from web import ui_text
from engine import control_cycle as cc
from engine import temperature_control_condition as tcc
from engine import tmp36_nominal_temperature as tmp36
from engine.subsystem_model import Subsystem
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, SEED, ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    ELEC, MECH, PARTS, _corrupt, _integrated, _part_line)
from tests.test_control_cycle import _field as _cc_field, _form as _cc_form
from tests.test_temperature_control_condition import (
    _field as _tcc_field, _form as _tcc_form)

ROOT = Path(__file__).resolve().parents[1]
CC_URL = "/session/%s/control-cycle"
TCC_URL = "/session/%s/temperature-control-condition"
HOSTILE = "<script>alert(1)</script> & \"board\""

# (prefix, url, gate name, form, field reader, expected next state)
PAGES = (
    ("cc", CC_URL, "_control_cycle_eligible", _cc_form, _cc_field, "RUNNING"),
    ("tcc", TCC_URL, "_tcc_eligible", _tcc_form, _tcc_field, "RUNNING"),
)
IDS = [p[0] for p in PAGES]


def _client(tag):
    client, _aid = _client_for("cc-integrated-%s@example.com" % tag)
    return client


def _next(body, prefix):
    return (_cc_field if prefix == "cc" else _tcc_field)(body, "next")


def _elec_part(sid):
    parts = [s for s in webapp._get_store().load_project_subsystems(sid) if s.domain == ELEC]
    assert len(parts) == 1
    return parts[0]


# ==========================================================================
# 1. root behaviour is unchanged
# ==========================================================================
@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_single_domain_projects_keep_exactly_the_root_rule(prefix, url, gate, form, field,
                                                           expected, monkeypatch):
    c = _client("root-" + prefix)
    elec = _start(c, ELEC_FORM)
    mech = _start(c, {"idea": SEED, "domain_confirm": MECH})
    assert webapp._get_store().load_project_subsystems(elec) == ()
    assert webapp._control_cycle_gate(elec) == (True, None)
    assert webapp._tcc_gate(elec) == (True, None)
    assert webapp._control_cycle_gate(mech) == (False, None)
    assert webapp._tcc_gate(mech) == (False, None)
    assert getattr(webapp, gate)(elec) is True and getattr(webapp, gate)(mech) is False
    assert "data-%s-link" % prefix in _page(c, elec)
    assert "data-%s-link" % prefix not in _page(c, mech)
    body = c.get(url % elec).get_data(as_text=True)
    assert "data-%s-form" % prefix in body and "data-%s-part" % prefix not in body
    body = c.post(url % elec, data=form()).get_data(as_text=True)
    assert _next(body, prefix) == expected and "data-%s-part" % prefix not in body
    body = c.post(url % mech, data=form()).get_data(as_text=True)
    assert "data-%s-form" % prefix not in body and _next(body, prefix) is None
    # root eligibility never depends on the composition being readable
    store = webapp._get_store()

    def broken(_sid):
        raise OSError("disk I/O error")
    monkeypatch.setattr(store, "load_project_subsystems", broken)
    assert webapp._control_cycle_gate(elec) == (True, None)
    assert webapp._tcc_gate(elec) == (True, None)
    assert _next(c.post(url % elec, data=form()).get_data(as_text=True), prefix) == expected


@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_electrical_focus_integrated_project_stays_eligible(prefix, url, gate, form,
                                                            field, expected):
    c = _client("elec-focus-" + prefix)
    sid = _integrated(c, ELEC)
    part = _elec_part(sid)
    assert webapp._control_cycle_gate(sid) == (True, part)
    assert webapp._tcc_gate(sid) == (True, part)
    assert "data-%s-link" % prefix in _page(c, sid)
    body = c.post(url % sid, data=form()).get_data(as_text=True)
    assert _next(body, prefix) == expected
    assert html.unescape(_part_line(body, prefix)) == PARTS["elec_part_name"]


# ==========================================================================
# 2. the declared Electrical / Electronics part is offered, with attribution
# ==========================================================================
@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_mechanical_focus_with_an_electrical_part_becomes_eligible(prefix, url, gate, form,
                                                                   field, expected,
                                                                   monkeypatch):
    c = _client("mech-focus-" + prefix)
    sid = _integrated(c, MECH)
    part = _elec_part(sid)
    assert webapp._cap12_root_domain(sid) == MECH
    assert webapp._control_cycle_gate(sid) == (True, part)
    assert webapp._tcc_gate(sid) == (True, part)
    assert getattr(webapp, gate)(sid) is True
    assert "data-%s-link" % prefix in _page(c, sid)
    page = c.get(url % sid).get_data(as_text=True)
    assert "data-%s-form" % prefix in page
    assert html.unescape(_part_line(page, prefix)) == PARTS["elec_part_name"]
    # nothing is pre-selected on the part either
    form_html = page.split("data-%s-form" % prefix, 1)[1].split("</form>", 1)[0]
    assert not re.search(r"<input[^>]*\schecked", form_html)
    evaluated = []
    real = cc.evaluate
    monkeypatch.setattr(webapp._cc, "evaluate",
                        lambda *a, **k: evaluated.append(a) or real(*a, **k))
    body = c.post(url % sid, data=form()).get_data(as_text=True)
    assert _next(body, prefix) == expected
    assert html.unescape(_part_line(body, prefix)) == PARTS["elec_part_name"]
    assert len(evaluated) == 1
    # the same request the module receives on an Electronics root
    root = _client("mech-focus-root-" + prefix)
    rsid = _start(root, ELEC_FORM)
    root_evaluated = []
    monkeypatch.setattr(webapp._cc, "evaluate",
                        lambda *a, **k: root_evaluated.append(a) or real(*a, **k))
    root_body = root.post(url % rsid, data=form()).get_data(as_text=True)
    assert _next(root_body, prefix) == expected
    assert root_evaluated == evaluated


@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_results_and_refusals_are_identical_on_the_part(prefix, url, gate, form, field,
                                                        expected):
    c = _client("same-" + prefix)
    sid = _integrated(c, MECH)
    root = _start(c, ELEC_FORM)
    cases = ({}, {"previous": "RUNNING"}, {"screen": {"machinery_motion": "yes"}}) \
        if prefix == "cc" else ({}, {"threshold": "26"}, {"previous": "RUNNING"},
                                {"v_out": "9999"}, {"c_screen": {"machinery_motion": "yes"}})
    for over in cases:
        a = c.post(url % sid, data=form(**over)).get_data(as_text=True)
        b = c.post(url % root, data=form(**over)).get_data(as_text=True)
        for name in ("next", "output", "previous"):
            assert field(a, name) == field(b, name), (over, name)
        for marker in ("data-%s-outcome" % prefix, "data-%s-result=\"success\"" % prefix):
            assert (marker in a) == (marker in b), (over, marker)
    if prefix == "tcc":
        a = c.post(url % sid, data=form(threshold="26")).get_data(as_text=True)
        assert field(a, "next") == "READY" and field(a, "output") == "false"


# ==========================================================================
# 3. the composition requires the SAME current part on both sides
# ==========================================================================
def _other_part(part):
    return Subsystem(subsystem_id="ps-other", domain=part.domain,
                     display_name="Another board", function_text="x",
                     provenance=part.provenance, validation_state=part.validation_state)


def test_two_true_results_on_different_parts_grant_nothing(monkeypatch):
    c = _client("identity-diff")
    sid = _integrated(c, MECH)
    part = _elec_part(sid)
    other = _other_part(part)
    assert part.subsystem_id != other.subsystem_id

    def gate(_sid, consumer):
        return (True, part) if consumer is webapp._tmp36 else (True, other)
    monkeypatch.setattr(webapp, "_calc_gate", gate)
    assert webapp._calc_gate(sid, webapp._tmp36)[0] is True
    assert webapp._calc_gate(sid, webapp._cc)[0] is True
    assert webapp._tcc_gate(sid) == (False, None)
    assert webapp._tcc_eligible(sid) is False
    assert "data-tcc-link" not in _page(c, sid)
    body = c.post(TCC_URL % sid, data=_tcc_form()).get_data(as_text=True)
    assert "data-tcc-form" not in body and _tcc_field(body, "next") is None


@pytest.mark.parametrize("tmp36_part,cycle_part", [(True, False), (False, True)],
                         ids=["part-on-tmp36-side-only", "part-on-cycle-side-only"])
def test_a_part_on_one_side_only_grants_nothing(tmp36_part, cycle_part, monkeypatch):
    c = _client("identity-one-%d%d" % (tmp36_part, cycle_part))
    sid = _integrated(c, MECH)
    part = _elec_part(sid)

    def gate(_sid, consumer):
        has = tmp36_part if consumer is webapp._tmp36 else cycle_part
        return (True, part if has else None)
    monkeypatch.setattr(webapp, "_calc_gate", gate)
    assert webapp._tcc_gate(sid) == (False, None)
    body = c.post(TCC_URL % sid, data=_tcc_form()).get_data(as_text=True)
    assert "data-tcc-form" not in body and _tcc_field(body, "next") is None


@pytest.mark.parametrize("tmp36_ok,cycle_ok", [(True, False), (False, True), (False, False)],
                         ids=["tmp36-only", "cycle-only", "neither"])
def test_one_gate_alone_is_insufficient(tmp36_ok, cycle_ok, monkeypatch):
    c = _client("identity-alone-%d%d" % (tmp36_ok, cycle_ok))
    sid = _integrated(c, MECH)
    part = _elec_part(sid)

    def gate(_sid, consumer):
        ok = tmp36_ok if consumer is webapp._tmp36 else cycle_ok
        return (ok, part if ok else None)
    monkeypatch.setattr(webapp, "_calc_gate", gate)
    assert webapp._tcc_gate(sid) == (False, None)
    assert "data-tcc-link" not in _page(c, sid)
    evaluated = []
    monkeypatch.setattr(webapp._tcc, "evaluate", lambda *a, **k: evaluated.append(1))
    body = c.post(TCC_URL % sid, data=_tcc_form()).get_data(as_text=True)
    assert "data-tcc-form" not in body and not evaluated


def test_a_part_of_another_domain_on_both_sides_grants_nothing(monkeypatch):
    c = _client("identity-domain")
    sid = _integrated(c, MECH)
    mech_part = [s for s in webapp._get_store().load_project_subsystems(sid)
                 if s.domain == MECH][0]
    monkeypatch.setattr(webapp, "_calc_gate", lambda _sid, _consumer: (True, mech_part))
    assert webapp._tcc_gate(sid) == (False, None)


def test_the_composition_gate_is_the_one_selection_rule():
    source = Path(webapp.__file__).read_text(encoding="utf-8")
    body = source[source.index("def _tcc_gate(sid):"):]
    body = body[:body.index("\n\n\n")]
    assert body.count("_calc_gate(sid, _tmp36)") == 1
    assert body.count("_calc_gate(sid, _cc)") == 1
    assert "tmp36_part.subsystem_id == cycle_part.subsystem_id" in body
    for gate in ("_tcc_eligible", "_control_cycle_eligible"):
        fn = source[source.index("def %s(sid):" % gate):]
        fn = fn[:fn.index("\n\n\n")]
        assert "return %s_gate(sid)[0]" % gate.replace("_eligible", "") in fn
    cc_gate = source[source.index("def _control_cycle_gate(sid):"):]
    cc_gate = cc_gate[:cc_gate.index("\n\n\n")]
    assert "return _calc_gate(sid, _cc)" in cc_gate
    # GET, POST and the session link read the gates, never the request
    for route in ("def control_cycle(sid):", "def control_cycle_post(sid):"):
        fn = source[source.index(route):]
        fn = fn[:fn.index("\n\n\n")]
        assert "_control_cycle_gate(sid)" in fn and "request.args" not in fn
    for route in ("def temperature_control_condition(sid):",
                  "def temperature_control_condition_post(sid):"):
        fn = source[source.index(route):]
        fn = fn[:fn.index("\n\n\n")]
        assert "_tcc_gate(sid)" in fn and "request.args" not in fn
    assert "control_cycle_link=_control_cycle_eligible(sid)" in source
    assert "temperature_control_condition_link=_tcc_eligible(sid)" in source


# ==========================================================================
# 4. the current state is re-read on every request; stale pages grant nothing
# ==========================================================================
@pytest.mark.parametrize("sql", (
    "UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 1",
    "DELETE FROM project_subsystems WHERE subsystem_seq = 1",
    "DELETE FROM project_subsystems",
    "UPDATE project_subsystems SET display_name = ' padded' WHERE subsystem_seq = 1",
    "UPDATE project_subsystems SET subsystem_seq = 7 WHERE subsystem_seq = 1",
    "UPDATE project_subsystems SET subsystem_id = 'sub-%s' WHERE subsystem_seq = 1" % ("f" * 32),
), ids=["replaced-domain", "withdrawn-part", "withdrawn-all", "corrupt-name",
        "corrupt-seq", "replaced-identity"])
@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_a_stale_page_grants_nothing_after_the_composition_changes(
        prefix, url, gate, form, field, expected, sql, monkeypatch):
    c = _client("stale-%s-%d" % (prefix, abs(hash(sql)) % 1000))
    sid = _integrated(c, MECH)
    page = c.get(url % sid).get_data(as_text=True)
    assert "data-%s-form" % prefix in page            # rendered while eligible
    before = _elec_part(sid).subsystem_id
    _corrupt(sql)
    evaluated = []
    monkeypatch.setattr(webapp._cc, "evaluate", lambda *a, **k: evaluated.append(1))
    monkeypatch.setattr(webapp._tcc, "evaluate", lambda *a, **k: evaluated.append(1))
    if "subsystem_id = 'sub-" in sql:
        # a replaced identity may still validate as a composition: eligibility
        # then follows the NEW current part, never the one the page was built on
        current = webapp._control_cycle_gate(sid)
        if current[0]:
            assert current[1].subsystem_id == "sub-" + "f" * 32 != before
            assert webapp._tcc_gate(sid)[1].subsystem_id == "sub-" + "f" * 32
            body = c.post(url % sid, data=form()).get_data(as_text=True)
            assert html.unescape(_part_line(body, prefix)) == PARTS["elec_part_name"]
            return
    assert webapp._control_cycle_gate(sid) == (False, None)
    assert webapp._tcc_gate(sid) == (False, None)
    assert getattr(webapp, gate)(sid) is False
    session = c.get("/session/%s" % sid)          # a corrupt composition may not render
    assert session.status_code != 200 or \
        "data-%s-link" % prefix not in session.get_data(as_text=True)
    body = c.post(url % sid, data=form()).get_data(as_text=True)   # the stale form
    assert "data-%s-form" % prefix not in body and _next(body, prefix) is None
    assert "data-%s-part" % prefix not in body
    assert not evaluated


@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_an_unreadable_composition_grants_nothing_beyond_the_root(
        prefix, url, gate, form, field, expected, monkeypatch):
    c = _client("unreadable-" + prefix)
    sid = _integrated(c, MECH)
    store = webapp._get_store()

    def broken(_sid):
        raise OSError("disk I/O error")
    monkeypatch.setattr(store, "load_project_subsystems", broken)
    assert webapp._control_cycle_gate(sid) == (False, None)
    assert webapp._tcc_gate(sid) == (False, None)
    body = c.post(url % sid, data=form()).get_data(as_text=True)
    assert "data-%s-form" % prefix not in body and _next(body, prefix) is None
    monkeypatch.undo()
    monkeypatch.setattr(webapp, "_cap12_root_domain", broken)
    # the root read fails, but the validated composition still holds the part
    assert webapp._control_cycle_gate(sid)[0] is True
    assert webapp._tcc_gate(sid)[0] is True
    single = _start(c, ELEC_FORM)
    assert webapp._control_cycle_gate(single) == (False, None)
    assert webapp._tcc_gate(single) == (False, None)


@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_get_and_post_follow_the_current_state_on_every_request(
        prefix, url, gate, form, field, expected, monkeypatch):
    c = _client("current-" + prefix)
    sid = _integrated(c, MECH)
    store = webapp._get_store()
    real = store.load_project_subsystems
    assert _next(c.post(url % sid, data=form()).get_data(as_text=True), prefix) == expected
    # the composition now reads without the Electronics part: GET and POST refuse
    monkeypatch.setattr(store, "load_project_subsystems", lambda s: tuple(
        sub for sub in real(s) if sub.domain != ELEC))
    assert "data-%s-form" % prefix not in c.get(url % sid).get_data(as_text=True)
    assert _next(c.post(url % sid, data=form()).get_data(as_text=True), prefix) is None
    assert "data-%s-link" % prefix not in _page(c, sid)
    # restored: eligible again, with no state carried over from either request
    monkeypatch.setattr(store, "load_project_subsystems", real)
    assert "data-%s-form" % prefix in c.get(url % sid).get_data(as_text=True)
    assert _next(c.post(url % sid, data=form()).get_data(as_text=True), prefix) == expected


# ==========================================================================
# 5. nothing from the request grants eligibility; authorization; no persistence
# ==========================================================================
@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_request_supplied_domain_or_part_never_grants_eligibility(
        prefix, url, gate, form, field, expected, monkeypatch):
    c = _client("request-" + prefix)
    mech = _start(c, {"idea": SEED, "domain_confirm": MECH})
    part_sid = _integrated(c, MECH)
    part_id = _elec_part(part_sid).subsystem_id
    evaluated = []
    monkeypatch.setattr(webapp._cc, "evaluate", lambda *a, **k: evaluated.append(1))
    monkeypatch.setattr(webapp._tcc, "evaluate", lambda *a, **k: evaluated.append(1))
    for extra in ({"root_domain": ELEC}, {"domain": ELEC}, {"part_id": part_id},
                  {"subsystem_id": part_id}, {"declared_part": PARTS["elec_part_name"]},
                  {"initial_focus": ELEC}):
        r = c.post(url % mech, data=dict(form(), **extra))
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-%s-form" % prefix not in body
        assert _next(body, prefix) is None
        r = c.get((url % mech) + "?domain=%s&part_id=%s&subsystem_id=%s" % (ELEC, part_id, part_id))
        assert "data-%s-form" % prefix not in r.get_data(as_text=True)
        # on an eligible project an extra field is a malformed request, not a grant
        r = c.post(url % part_sid, data=dict(form(), **extra))
        assert r.status_code == 400 and _next(r.get_data(as_text=True), prefix) is None
    assert not evaluated


@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_authorization_csrf_and_no_persistence_on_the_part(prefix, url, gate, form, field,
                                                           expected):
    c = _client("auth-" + prefix)
    sid = _integrated(c, MECH)
    assert webapp.app.test_client().post(url % sid, data=form()).status_code == 403
    other, _ = _client_for("cc-integrated-other-%s@example.com" % prefix)
    for client in (other, _new_client()):
        for r in (client.get(url % sid), client.post(url % sid, data=form())):
            assert r.status_code == 302 and ("data-%s" % prefix) not in r.get_data(as_text=True)
    _page(c, sid)
    before = _snapshot(c)
    c.post(url % sid, data=form())
    c.get(url % sid)
    assert _snapshot(c) == before


# ==========================================================================
# 6. EN / AR attribution, escaping; the unchanged definitions and records
# ==========================================================================
@pytest.mark.parametrize("prefix,url,gate,form,field,expected", PAGES, ids=IDS)
def test_the_part_name_is_escaped_and_bilingual(prefix, url, gate, form, field, expected):
    c = _client("escape-" + prefix)
    sid = _integrated(c, MECH, elec_part_name=HOSTILE)
    body = c.get(url % sid).get_data(as_text=True)
    assert "<script>" not in body
    assert html.unescape(_part_line(body, prefix)) == HOSTILE
    note = "UI_%s_PART_NOTE" % prefix.upper()
    for lang in ("en", "ar"):
        if lang == "ar":
            assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
        page = c.get(url % sid).get_data(as_text=True)
        text = html.unescape(re.sub(r"<[^>]+>", "", page))
        for key in ("UI_THERM01_PART_LABEL", note, "UI_%s_SCOPE_NOTE" % prefix.upper()):
            assert re.sub(r"\s+", " ", ui_text.text(key, lang)) in re.sub(r"\s+", " ", text), \
                (key, lang)
        if lang == "ar":
            assert 'dir="rtl"' in page


def test_the_scope_and_part_notes_make_no_control_or_safety_claim():
    for prefix in ("CC", "TCC"):
        en = ui_text.text("UI_%s_SCOPE_NOTE" % prefix, "en")
        ar = ui_text.text("UI_%s_SCOPE_NOTE" % prefix, "ar")
        assert "declared Electrical / Electronics part" in en
        assert "Neither the focus nor a recorded part establishes" in en
        assert "الكهربائي/الإلكتروني المصرّح به" in ar
        note = ui_text.text("UI_%s_PART_NOTE" % prefix, "en").lower()
        for phrase in ("control requirement", "actuation", "timing", "compatibility",
                       "suitability", "validation", "safety"):
            assert phrase in note, (prefix, phrase)
        assert ui_text.text("UI_%s_PART_NOTE" % prefix, "ar").strip()
    assert "the same declared Electrical / Electronics part" in ui_text.text("UI_TCC_SCOPE_NOTE", "en")


def test_definitions_identities_and_artifacts_are_unchanged():
    assert cc.METHOD_ID == "control_cycle:ready_running_single_transition"
    assert cc.METHOD_VERSION == "1.0"
    assert cc.ELIGIBLE_ROOT_DOMAIN == ELEC == tmp36.ELIGIBLE_ROOT_DOMAIN
    assert cc.load_artifact()["artifact_version"] == "1"
    assert tcc.COMPOSITION_ID == "temperature_control_condition:tmp36_threshold_ready_running"
    assert tcc.COMPOSITION_VERSION == "1.0"
    assert cc.STATES == ("READY", "RUNNING")
    assert cc.evaluate(cc.capture_form({k: [v] for k, v in _cc_form().items()}))["next_state"] \
        == "RUNNING"
    source = Path(webapp.__file__).read_text(encoding="utf-8")
    section = source[source.index("# 28-T4 — Single Vendor-Neutral"):
                     source.index("# DC-RESISTIVE-LOAD-CURRENT-01")]
    code = "\n".join(line for line in section.splitlines()
                     if not line.strip().startswith("#"))
    for banned in ("control_loop", "load_project_subsystem_part_answers", "SafetySignal(",
                   "_get_store()", "request.args", "session["):
        assert banned not in code, banned


def test_the_stage15_exception_and_contracts_record_the_amendment():
    model = (ROOT / "engine" / "subsystem_model.py").read_text(encoding="utf-8")
    assert "CONTROL-CYCLE-INTEGRATED-PART-01" in model
    assert "``control_cycle:ready_running_single_transition``" in model
    assert "``temperature_control_condition:tmp36_threshold_ready_running``" in model
    assert "resolve to that SAME current part" in re.sub(r"\s+", " ", model)
    cycle = re.sub(r"\s+", " ", (ROOT / "docs" / "governance" /
                                 "STAGE28_T4_CONTROL_CYCLE_READY_RUNNING_CONTRACT.md")
                   .read_text(encoding="utf-8"))
    for phrase in ("Amended by CONTROL-CYCLE-INTEGRATED-PART-01",
                   "the ONE shared rule the admitted calculations use (`_calc_gate`",
                   "never dependent on any composition",
                   "no request-supplied part id or domain can establish eligibility",
                   "establishes no control requirement, actuation, PLC runtime semantics, timing",
                   "no D4, PLC, Mechatronics or domain activation follows"):
        assert phrase in cycle, phrase
    comp = re.sub(r"\s+", " ", (ROOT / "docs" / "governance" /
                                "TEMPERATURE_TO_CONTROL_CONDITION_COMPOSITION_CONTRACT.md")
                  .read_text(encoding="utf-8"))
    for phrase in ("Amended by CONTROL-CYCLE-INTEGRATED-PART-01",
                   "the SAME current validated Electrical / Electronics part",
                   "Two separate `True` results never establish that",
                   "No second composition-selection engine exists",
                   "INTERSECTION of the two existing gates"):
        assert phrase in comp, phrase
