# -*- coding: utf-8 -*-
"""DC-RESISTIVE-LOAD-INTEGRATED-PART-01 — integrated-part eligibility for the
three admitted DC resistive load calculations (Owner-authorized).

Authority: the DC resistive load current, power and energy method contracts §1
as amended, and the narrow Stage 15 exception recorded in
``engine/subsystem_model.py``. Each calculation may be OFFERED for the declared
Electrical / Electronics part of a valid durable integrated composition,
whatever the initial analysis focus, through the existing ``_calc_gate``. Root
eligibility is unchanged; the decision is recomputed from the current durable
state on every request, so a missing, corrupt, replaced or unreadable
composition grants nothing, an earlier rendered page grants nothing once that
state no longer admits the project, and nothing is taken from the request. The
methods, declarations, screens, numbers and refusals are identical whatever the
path; the declared part is named, escaped, in EN and AR. Synthetic data only.
"""
import html
import re

import pytest

import web.app as webapp
from web import ui_text
from engine import deterministic_calculation as dc
from engine import dc_resistive_load_current as dcl
from engine import dc_resistive_load_power as dcp
from engine import dc_resistive_load_energy as dce
from tests.test_cap12_form_mockup_advisory import (
    _client_for, _new_client, _start, _page, _snapshot, SEED, ELEC_FORM)
from tests.test_cap13_therm01_integrated_part_eligibility import (
    _integrated, _corrupt, _owner_spy, _part_line, MECH, ELEC, PARTS, CTRL, HOSTILE)
from tests.test_dc_resistive_load_current import _form as _current_form
from tests.test_dc_resistive_load_power import _form as _power_form
from tests.test_dc_resistive_load_energy import _form as _energy_form

# (prefix, consumer, URL, eligibility function name, valid form, expected result)
CALCS = (
    ("dcl", dcl, "/session/%s/dc-load-current", "_dcl_eligible",
     lambda **k: _current_form(**dict({"v": "12", "r": "24"}, **k)), "0.5 A"),
    ("dcp", dcp, "/session/%s/dc-load-power", "_dcp_eligible",
     lambda **k: _power_form(**dict({"v": "12", "r": "24"}, **k)), "6 W"),
    ("dce", dce, "/session/%s/dc-load-energy", "_dce_eligible",
     lambda **k: _energy_form(**dict({"v": "12", "r": "24", "t": "3600"}, **k)), "21600 J"),
)
IDS = [c[0] for c in CALCS]


def _value(body, prefix):
    marker = 'data-%s-result-value><bdi dir="ltr">' % prefix
    return body.split(marker, 1)[1].split("</bdi>", 1)[0] if marker in body else None


def _client(tag):
    client, _aid = _client_for("dc-integrated-%s@example.com" % tag)
    return client


def _eligible(name, sid):
    return getattr(webapp, name)(sid)


# ==========================================================================
# 1. root behaviour is unchanged
# ==========================================================================
@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_single_domain_projects_keep_exactly_the_root_rule(prefix, consumer, url, gate,
                                                           form, expected):
    c = _client("root-" + prefix)
    elec = _start(c, ELEC_FORM)
    mech = _start(c, {"idea": SEED, "domain_confirm": MECH})
    assert webapp._calc_gate(elec, consumer) == (True, None)
    assert webapp._calc_gate(mech, consumer) == (False, None)
    assert "data-%s-link" % prefix in _page(c, elec)
    assert "data-%s-link" % prefix not in _page(c, mech)
    body = c.post(url % elec, data=form()).get_data(as_text=True)
    assert _value(body, prefix) == expected and "data-%s-part" % prefix not in body
    body = c.post(url % mech, data=form()).get_data(as_text=True)
    assert "data-%s-form" % prefix not in body and _value(body, prefix) is None


# ==========================================================================
# 2. the declared Electrical / Electronics part, both focus directions and three parts
# ==========================================================================
@pytest.mark.parametrize("focus,extra", [(MECH, {}), (ELEC, {}), (MECH, CTRL), (ELEC, CTRL)],
                         ids=["mech-focus", "elec-focus", "mech-focus-3", "elec-focus-3"])
@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_the_declared_electronics_part_is_offered_with_attribution(
        prefix, consumer, url, gate, form, expected, focus, extra, monkeypatch):
    c = _client("part-%s-%s-%d" % (prefix, focus, len(extra)))
    sid = _integrated(c, focus, **extra)
    eligible, part = webapp._calc_gate(sid, consumer)
    assert eligible and part.domain == ELEC
    assert part.display_name == PARTS["elec_part_name"]
    assert _eligible(gate, sid)
    assert "data-%s-link" % prefix in _page(c, sid)
    get = c.get(url % sid).get_data(as_text=True)
    assert "data-%s-form" % prefix in get and "checked" not in get
    assert _part_line(get, prefix) == PARTS["elec_part_name"]
    calls = _owner_spy(monkeypatch)
    post = c.post(url % sid, data=form()).get_data(as_text=True)
    assert _value(post, prefix) == expected
    assert _part_line(post, prefix) == PARTS["elec_part_name"]
    assert len(calls) == 1 and calls[0][0]["subject_ref"] is None
    assert calls[0][0]["method_id"] == consumer.METHOD_ID


@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_numbers_and_owner_requests_are_identical_whatever_the_path(
        prefix, consumer, url, gate, form, expected, monkeypatch):
    c = _client("same-" + prefix)
    root = _start(c, ELEC_FORM)
    part = _integrated(c, MECH)
    calls = _owner_spy(monkeypatch)
    root_body = c.post(url % root, data=form()).get_data(as_text=True)
    part_body = c.post(url % part, data=form()).get_data(as_text=True)
    assert _value(root_body, prefix) == _value(part_body, prefix) == expected
    (req_root, res_root), (req_part, res_part) = calls
    assert req_root == req_part
    assert res_root["result_identity"] == res_part["result_identity"]


@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_declarations_screen_and_refusals_are_unchanged_on_the_part(
        prefix, consumer, url, gate, form, expected, monkeypatch):
    c = _client("refuse-" + prefix)
    sid = _integrated(c, MECH)
    calls = _owner_spy(monkeypatch)
    cases = [
        (form(r="0"), "RESISTANCE_NOT_POSITIVE"),
        (form(screen={"battery_or_storage_cell": "yes"}), "ENGINEERING_REVIEW_REQUIRED"),
        (form(decl={consumer.DECLARATION_IDS[-1]: "does_not_apply"}), "MODEL_NOT_SUPPORTED"),
        (form(decl={consumer.DECLARATION_IDS[0]: ""}), "NOT_DECLARED"),
    ]
    if prefix == "dce":
        cases.append((form(t="-1"), "DURATION_NEGATIVE"))
    for data, outcome in cases:
        body = c.post(url % sid, data=data).get_data(as_text=True)
        assert ui_text.text("UI_%s_OUTCOME_%s" % (prefix.upper(), outcome), "en") \
            in html.unescape(body), outcome
        assert _value(body, prefix) is None
        assert body.count("data-%s-outcome" % prefix) == 1
    assert not calls
    # the part supplies no declaration or screen answer: nothing is pre-selected
    assert "checked" not in c.get(url % sid).get_data(as_text=True)


# ==========================================================================
# 3. stale, replaced, corrupt and unreadable compositions fail closed
# ==========================================================================
@pytest.mark.parametrize("sql", (
    "UPDATE project_subsystems SET domain = 'software' WHERE subsystem_seq = 1",
    "DELETE FROM project_subsystems WHERE subsystem_seq = 1",
    "DELETE FROM project_subsystems",
    "UPDATE project_subsystems SET display_name = ' padded' WHERE subsystem_seq = 1",
    "UPDATE project_subsystems SET subsystem_seq = 7 WHERE subsystem_seq = 1",
), ids=["replaced-domain", "withdrawn-part", "withdrawn-all", "corrupt-name", "corrupt-seq"])
@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_a_stale_page_grants_nothing_after_the_composition_changes(
        prefix, consumer, url, gate, form, expected, sql, monkeypatch):
    c = _client("stale-%s-%d" % (prefix, abs(hash(sql)) % 1000))
    sid = _integrated(c, MECH)
    page = c.get(url % sid).get_data(as_text=True)
    assert "data-%s-form" % prefix in page            # rendered while eligible
    _corrupt(sql)
    calls = _owner_spy(monkeypatch)
    evaluated = []
    monkeypatch.setattr(consumer, "evaluate", lambda *a, **k: evaluated.append(1))
    assert webapp._calc_gate(sid, consumer) == (False, None)
    assert not _eligible(gate, sid)
    session = c.get("/session/%s" % sid)          # a corrupt composition may not render
    assert session.status_code != 200 or \
        "data-%s-link" % prefix not in session.get_data(as_text=True)
    body = c.post(url % sid, data=form()).get_data(as_text=True)   # the stale form
    assert "data-%s-form" % prefix not in body and _value(body, prefix) is None
    assert "data-%s-part" % prefix not in body
    assert not calls and not evaluated


@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_an_unreadable_composition_or_root_grants_nothing(
        prefix, consumer, url, gate, form, expected, monkeypatch):
    c = _client("unreadable-" + prefix)
    sid = _integrated(c, MECH)
    store = webapp._get_store()

    def broken(_sid):
        raise OSError("disk I/O error")
    monkeypatch.setattr(store, "load_project_subsystems", broken)
    assert webapp._calc_gate(sid, consumer) == (False, None)
    body = c.post(url % sid, data=form()).get_data(as_text=True)
    assert "data-%s-form" % prefix not in body and _value(body, prefix) is None
    monkeypatch.undo()
    monkeypatch.setattr(webapp, "_cap12_root_domain", broken)
    # the root read fails, but the validated composition still holds the part
    assert webapp._calc_gate(sid, consumer)[0] is True
    single = _start(c, ELEC_FORM)
    assert webapp._calc_gate(single, consumer) == (False, None)


@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_eligibility_follows_the_current_state_on_every_request(
        prefix, consumer, url, gate, form, expected, monkeypatch):
    c = _client("current-" + prefix)
    sid = _integrated(c, MECH)
    store = webapp._get_store()
    real = store.load_project_subsystems
    assert _value(c.post(url % sid, data=form()).get_data(as_text=True), prefix) == expected
    # the composition now reads without the Electronics part: the next request refuses
    monkeypatch.setattr(store, "load_project_subsystems", lambda s: tuple(
        sub for sub in real(s) if sub.domain != ELEC))
    assert _value(c.post(url % sid, data=form()).get_data(as_text=True), prefix) is None
    assert "data-%s-link" % prefix not in _page(c, sid)
    # restored: eligible again, with no state carried over from either request
    monkeypatch.setattr(store, "load_project_subsystems", real)
    body = c.post(url % sid, data=form()).get_data(as_text=True)
    assert _value(body, prefix) == expected


# ==========================================================================
# 4. nothing from the request grants eligibility; authorization and CSRF
# ==========================================================================
@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_request_supplied_domain_or_part_never_grants_eligibility(
        prefix, consumer, url, gate, form, expected, monkeypatch):
    c = _client("request-" + prefix)
    mech = _start(c, {"idea": SEED, "domain_confirm": MECH})
    part_sid = _integrated(c, MECH)
    part_id = webapp._calc_gate(part_sid, consumer)[1].subsystem_id
    calls = _owner_spy(monkeypatch)
    for extra in ({"root_domain": ELEC}, {"domain": ELEC}, {"part_id": part_id},
                  {"subsystem_id": part_id}, {"declared_part": PARTS["elec_part_name"]}):
        r = c.post(url % mech, data=dict(form(), **extra))
        body = r.get_data(as_text=True)
        assert r.status_code == 200 and "data-%s-form" % prefix not in body
        assert _value(body, prefix) is None
        r = c.get((url % mech) + "?domain=%s&part_id=%s" % (ELEC, part_id))
        assert "data-%s-form" % prefix not in r.get_data(as_text=True)
        # on an eligible project an extra field is a malformed request, not a grant
        r = c.post(url % part_sid, data=dict(form(), **extra))
        assert r.status_code == 400 and _value(r.get_data(as_text=True), prefix) is None
    assert not calls


@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_authorization_csrf_and_no_persistence_on_the_part(
        prefix, consumer, url, gate, form, expected):
    c = _client("auth-" + prefix)
    sid = _integrated(c, MECH)
    assert webapp.app.test_client().post(url % sid, data=form()).status_code == 403
    other = _client("auth-other-" + prefix)
    for client in (other, _new_client()):
        for r in (client.get(url % sid), client.post(url % sid, data=form())):
            assert r.status_code == 302
            assert "data-%s" % prefix not in r.get_data(as_text=True)
    before = _snapshot(c)
    c.post(url % sid, data=form())
    body = c.get(url % sid).get_data(as_text=True)
    assert _snapshot(c) == before and "checked" not in body
    assert c.get(url % sid).headers["Cache-Control"] == "no-store"


# ==========================================================================
# 5. EN / AR attribution, escaping, and the unchanged method boundaries
# ==========================================================================
@pytest.mark.parametrize("prefix,consumer,url,gate,form,expected", CALCS, ids=IDS)
def test_the_part_name_is_escaped_and_bilingual(prefix, consumer, url, gate, form,
                                                expected):
    c = _client("escape-" + prefix)
    sid = _integrated(c, MECH, elec_part_name=HOSTILE)
    body = c.get(url % sid).get_data(as_text=True)
    assert "<script>" not in body
    assert html.unescape(_part_line(body, prefix)) == HOSTILE
    for lang in ("en", "ar"):
        if lang == "ar":
            assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
        page = c.get(url % sid).get_data(as_text=True)
        text = html.unescape(re.sub(r"<[^>]+>", "", page))
        for key in ("UI_THERM01_PART_LABEL", "UI_THERM01_PART_NOTE",
                    "UI_%s_SCOPE_NOTE" % prefix.upper()):
            assert re.sub(r"\s+", " ", ui_text.text(key, lang)) in re.sub(r"\s+", " ", text), \
                (key, lang)
        if lang == "ar":
            assert 'dir="rtl"' in page


def test_the_scope_notes_name_the_declared_part_in_both_languages():
    for prefix in IDS:
        en = ui_text.text("UI_%s_SCOPE_NOTE" % prefix.upper(), "en")
        ar = ui_text.text("UI_%s_SCOPE_NOTE" % prefix.upper(), "ar")
        assert "declared Electrical / Electronics part" in en
        assert "Neither the focus nor a recorded part establishes" in en
        assert "لجزئه الكهربائي/الإلكتروني المصرّح به" in ar


def test_methods_owner_and_artifacts_are_unchanged():
    # the shared owner as it stands on the base this increment starts from
    assert dc.IMPLEMENTATION_VERSION == "1.11.0"
    assert dc.load_artifact()["artifact_version"] == "12"
    for consumer in (dcl, dcp, dce):
        assert consumer.METHOD_VERSION == "1.0"
        assert consumer.load_artifact()["artifact_version"] == "1"
        assert consumer.ELIGIBLE_ROOT_DOMAIN == ELEC
    source = open(webapp.__file__, encoding="utf-8").read()
    assert source.count("_dcalc.bind_method(") == 12
    for gate, consumer in (("_dcl_eligible", "_dcl"), ("_dcp_eligible", "_dcp"),
                           ("_dce_eligible", "_dce")):
        body = source[source.index("def %s(sid):" % gate):]
        body = body[:body.index("\n\n\n")]
        assert "return _calc_gate(sid, %s)[0]" % consumer in body


def test_the_stage15_exception_and_contracts_record_the_amendment():
    model = open("engine/subsystem_model.py", encoding="utf-8").read()
    assert "DC-RESISTIVE-LOAD-INTEGRATED-PART-01" in model
    for name in ("current", "power", "energy"):
        assert "``electrical:dc_resistive_load_%s``" % name in model
        path = ("docs/governance/ELECTRICAL_DC_RESISTIVE_LOAD_%s_METHOD_CONTRACT.md"
                % name.upper())
        text = re.sub(r"\s+", " ", open(path, encoding="utf-8").read())
        for phrase in ("the SAME `_calc_gate` / `_calc_declared_part` rule",
                       "The Stage 15 exception in `engine/subsystem_model.py` names this method",
                       "an earlier rendered page grants nothing",
                       "Amendment (DC-RESISTIVE-LOAD-INTEGRATED-PART-01",
                       "Only eligibility changes",
                       "Stage 15 part eligibility only as stated in §1"):
            assert phrase in text, (name, phrase)
