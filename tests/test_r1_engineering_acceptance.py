"""R1-ENGINEERING-ACCEPTANCE-PROOF-01 — first-release acceptance journeys for the
delivered, bounded R1 engineering scopes (roadmap §8D): Mechanical, Electrical /
Electronics and the Stage-15 integrated invention.

Each test drives ONE coherent journey for one area through the real web routes,
the real engine and the real durable store, reusing the helpers of the suites
that already prove each capability on its own. What is new here is only the
joined path: the gaps the report explains are the ones the inventor's own
answers left open (never injected), and every capability is reached on the
same project. Nothing here changes product behaviour; a failure is a product
finding, not a test to adjust.

Boundaries the journeys also check: calculations, advisories, reports and
exports write nothing; results stay UNVALIDATED; the routed Mechanical need
stays outstanding; interface observations stay out of the report.

Synthetic invention data only — never the T1-C′ study corpus.
"""
import html as _html
import json
import os
import pickle
import re
import sqlite3

import pytest

import engine.progression_loop as pl
from engine import need_routing as nr
import engine.therm01_temperature_difference as therm01
import web.app as appmod
from engine.idea_state import (
    ACCEPTED_RISK, BOUNDARY_AMBIGUITY, CLOSED, MECHANISM_COMPLETENESS, PARTIAL,
    PHYSICAL_FEASIBILITY,
)
from web import ui_text

from tests.test_cap12_form_mockup_advisory import ADV, OK_FORM, _client_for
from tests.test_cap13_static_reactions import URL as CAP13_URL, _form as _cap13_form
from tests.test_cap13_therm01_integrated_part_eligibility import (
    CTRL, PARTS, _integrated, _part_line,
)
from tests.test_cap01_mechanical_open_gap_context import FUND_PREFIX, _pdf_source
from tests.test_component_inventory_declare_list import (
    _declare as _declare_component, _form as _component_form,
)
from tests.test_safe_question_routing_pf_q2 import (
    BA_1, BA_2, MECH, PF_Q1, PF_Q2, PF_STRONG, SEED, _answer_form_target,
)
from tests.test_stage15_integration_closure import _dep_save
from tests.test_stage15_interface_observations import _observe, _record_form
from tests.test_stage15_interface_preparation import _save as _save_preparation
from tests.test_stage19_durable_success_criteria import ELEC_ANSWERS, ELEC_IDEA
from tests.test_stage28_control_loop_optional_part_slice1 import (
    _bindings, _declare as _declare_interface,
)
from tests.test_28t5_nonfocused_required_part_questions import (
    _form as _part_form, _ids as _part_question_ids, _save as _save_part_answers,
)
from tests.test_therm01_temperature_difference import (
    URL as THERM_URL, _form as _therm_form,
)

MECHANICAL = "mechanical"
ELECTRONICS = "electronics_electrical"
CONTROL_LOOP = "control_loop"
ELEC_PF = ("The physical principle is Ohm's law: the accelerometer output voltage "
           "is read by the ADC, and the transistor switches the LED current from "
           "the battery, which supplies enough power for the LED and the "
           "microcontroller.")
ELEC_BA = ("Existing bicycle brake lights are switched by hand; mine detects "
           "deceleration automatically with an accelerometer, unlike existing "
           "lights that do not sense braking.")
EXIT_PROMPT = "_EXHAUSTED_EXIT_PROMPT"

COMPONENT = ("Latch spring", "Pushes the latch pin into the rail.")
INTERFACE = "The motor board drives the hinge arm through a geared motor."
PREPARATION = {
    "operating_conditions": "Indoor use at room temperature, 30 open-close cycles.",
    "acceptance_criterion": "The arm reaches the open stop within 5 seconds.",
    "evidence_needed": "A timed video of each cycle.",
}
OBSERVATION = "In my bench check the arm reached the stop in 4 seconds."
PART_ANSWER = "The board switches the motor on when the button is pressed."


# --------------------------------------------------------------------------
# shared helpers (journey-level only; capability helpers are reused above)
# --------------------------------------------------------------------------
def _start(client, idea, domain):
    r = client.post("/start", data={"idea": idea, "domain_confirm": domain})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _state(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _token(client, sid):
    raw = client.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]*)"', raw)
    return m.group(1) if m else None


def _answer(client, sid, text):
    served = _answer_form_target(client, sid)["q"]
    r = client.post(f"/session/{sid}", data={
        "response": text, "answer_token": _token(client, sid), "action": "answered"})
    assert r.status_code == 302, r.status_code
    return served


def _accept_risk(client, sid, gap):
    r = client.post(f"/session/{sid}/accept-risk", data={
        "gap_type": gap, "risk_confirm": "yes", "answer_token": _token(client, sid)})
    assert r.status_code == 302, r.status_code
    assert _state(sid).get_gap(gap).status == ACCEPTED_RISK


def _gaps(sid):
    return [(g.gap_type, g.status) for g in _state(sid).gaps]


def _database():
    with sqlite3.connect(os.environ["INVENTORAI_DB_PATH"]) as connection:
        return list(connection.iterdump())


def _frozen(sid):
    """Durable rows + the live engine state: what a read-only surface must
    leave exactly as it found it."""
    return _database(), pickle.dumps(_state(sid))


def _report(client, sid):
    r = client.get(f"/session/{sid}/deliverable")
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _visible(raw):
    raw = re.sub(r"(?is)<(style|script)\b.*?</\1>", " ", raw)
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", raw))).strip()


def _guidance(raw):
    """The CAP-01 gap guidance a report or PDF source carries: gap contexts
    (gap, state), next-steps groups and reference-fundamentals groups, in
    rendered order."""
    return (re.findall(r'data-cap01-gap="([^"]+)" data-cap01-gap-state="([^"]+)"', raw),
            re.findall(r'data-cap01-next-steps="([^"]+)"', raw),
            re.findall(r'data-cap01-fundamentals="([^"]+)"', raw))


def _set_lang(client, lang):
    assert client.post("/ui-language", data={"lang": lang}).status_code in (200, 302)


# ==========================================================================
# A. Mechanical
# ==========================================================================
MECH_GUIDANCE = ([("physical-feasibility", "partial")],
                 ["cap01-mechanical-next-steps-v1"],
                 ["force-moment-pressure-v1"])


def test_a_mechanical_r1_journey(monkeypatch):
    client, _aid = _client_for("r1-mechanical@example.com")
    sid = _start(client, SEED, MECHANICAL)

    # A1 — the governed Mechanical question journey, with PF:Q2 routed away.
    served = [_answer(client, sid, text) for text in (MECH, MECH, PF_STRONG, BA_1, BA_2)]
    assert all(q.startswith("PATHN:mechanical:") for q in served), served
    assert "PATHN:" + PF_Q1 in served and "PATHN:" + PF_Q2 not in served
    state = _state(sid)
    assert pl.select_next_gap(state) is None                 # no further question
    assert _gaps(sid) == [(MECHANISM_COMPLETENESS, CLOSED),
                          (PHYSICAL_FEASIBILITY, PARTIAL),
                          (BOUNDARY_AMBIGUITY, CLOSED)]
    assert PHYSICAL_FEASIBILITY in pl.routed_maturity_veto_gaps(state)
    page = client.get(f"/session/{sid}").get_data(as_text=True)
    assert 'id="answer-form"' not in page
    assert ui_text.text("UI_NR_HEADING_SPECIALIST", "en") in _html.unescape(page)

    before = _frozen(sid)

    # A2 — the gap the journey left open is explained in the report and the PDF.
    report = _report(client, sid)
    assert _guidance(report) == MECH_GUIDANCE
    for equation in ("T = F × L⊥", "F₁L₁ = F₂L₂", "F = pA"):
        assert equation in report
    assert _guidance(_pdf_source(client, sid, monkeypatch)) == MECH_GUIDANCE
    _set_lang(client, "ar")
    ar_report = _report(client, sid)
    assert '<html lang="ar" dir="rtl">' in ar_report
    assert _guidance(ar_report) == MECH_GUIDANCE
    assert ui_text.text(FUND_PREFIX + "TITLE", "ar") in _html.unescape(ar_report)
    assert _guidance(_pdf_source(client, sid, monkeypatch)) == MECH_GUIDANCE
    _set_lang(client, "en")

    # A3 — the CAP-12 form mock-up advisory, reached from the session page.
    page = client.get(f"/session/{sid}").get_data(as_text=True)
    assert "data-cap12-link" in page and (ADV % sid) in page
    advisory = client.post(ADV % sid, data=OK_FORM)
    assert advisory.status_code == 200
    body = advisory.get_data(as_text=True)
    assert 'data-cap12-result="available"' in body
    assert body.count("data-cap12-alternative") >= 2

    # A4 — the CAP-13 two-support calculation on the same project.
    assert (CAP13_URL % sid) in page
    result = client.post(CAP13_URL % sid, data=_cap13_form(P="1000", L="2000", x="500"))
    body = result.get_data(as_text=True)
    assert re.findall(r'data-cap13-reaction><bdi dir="ltr">([^<]+)</bdi>', body) == [
        "750.0 N", "250.0 N"]
    assert "UNVALIDATED" in body
    assert " ".join(ui_text.text("UI_CAP13_DISCLOSURE", "en").split()) in _visible(body)
    refused = client.post(CAP13_URL % sid, data=_cap13_form(x="2500")).get_data(as_text=True)
    assert "data-cap13-reaction" not in refused

    # A5 — reading the report, the PDF, the advisory and the calculation wrote nothing.
    assert _frozen(sid) == before

    # A6 — the existing explicit continuation: accepting the routed risk lifts the
    # Mechanical journey to Level 2 while the specialist need stays outstanding.
    _accept_risk(client, sid, PHYSICAL_FEASIBILITY)
    state = _state(sid)
    assert state.maturity_level == 2
    assert [r.operation for r in appmod._get_store().load_need_routing(sid)] == ["ROUTE"]
    assert nr.gap_has_outstanding_routing(state, PHYSICAL_FEASIBILITY)
    assert state.get_gap(PHYSICAL_FEASIBILITY).closed_at is None
    assert pl.select_next_gap(state) not in (
        MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY)


# ==========================================================================
# B. Electrical / Electronics
# ==========================================================================
ELEC_MC_GUIDANCE = ([("mechanism-completeness", "open")],
                    ["cap01-electronics-next-steps-v1"],
                    ["sensing-value-threshold-reference-v1",
                     "measurement-accuracy-resolution-reference-v1",
                     "controller-input-logic-output-reference-v1",
                     # 28-T3-LOAD-SWITCHING-PRINCIPLE-REFERENCE-01: the same exact gap binding.
                     "transistor-load-switching-reference-v1"])
ELEC_PF_GUIDANCE = ([("physical-feasibility", "partial")],
                    ["cap01-electronics-next-steps-v1"],
                    ["basic-electrical-reference-v1",
                     "electrical-energy-time-reference-v1",
                     "electric-charge-reference-v1"])


def _answer_until_exit(client, sid, gap, text):
    """Answer the served questions of ``gap`` until the governed exhausted-exit
    prompt is served; return the governed question ids served on the way."""
    served = []
    for _ in range(8):
        assert pl.select_next_gap(_state(sid)) == gap
        q = _answer_form_target(client, sid)["q"]
        if q.endswith(EXIT_PROMPT):
            return served
        served.append(_answer(client, sid, text))
    pytest.fail("the governed exit prompt was never served for %s" % gap)


def test_b_electronics_r1_journey(monkeypatch):
    client, _aid = _client_for("r1-electronics@example.com")
    sid = _start(client, ELEC_IDEA, ELECTRONICS)

    # B2 (start) — the open mechanism gap is explained with its reference groups.
    before = _frozen(sid)
    assert _guidance(_report(client, sid)) == ELEC_MC_GUIDANCE
    assert _guidance(_pdf_source(client, sid, monkeypatch)) == ELEC_MC_GUIDANCE
    assert _frozen(sid) == before

    # B1 — the governed Electrical / Electronics question journey.
    served = [_answer(client, sid, text) for text in ELEC_ANSWERS[:2]]
    assert _state(sid).get_gap(MECHANISM_COMPLETENESS).status == CLOSED
    served += _answer_until_exit(client, sid, PHYSICAL_FEASIBILITY, ELEC_PF)
    assert _state(sid).get_gap(PHYSICAL_FEASIBILITY).status == PARTIAL

    # B2 (feasibility) — the partial feasibility gap and its fundamentals.
    before = _frozen(sid)
    report = _report(client, sid)
    assert _guidance(report) == ELEC_PF_GUIDANCE
    for equation in ("V = I × R", "P = V × I", "E = P × t"):
        assert equation in report
    assert _guidance(_pdf_source(client, sid, monkeypatch)) == ELEC_PF_GUIDANCE
    _set_lang(client, "ar")
    ar_report = _report(client, sid)
    assert '<html lang="ar" dir="rtl">' in ar_report
    assert _guidance(ar_report) == ELEC_PF_GUIDANCE
    _set_lang(client, "en")

    # B3 — the THERM-01 single-path calculation on the same project.
    page = client.get(f"/session/{sid}").get_data(as_text=True)
    assert (THERM_URL % sid) in page
    body = client.post(THERM_URL % sid, data=_therm_form(P="10", R_theta="2.5")).get_data(
        as_text=True)
    assert "25.0 K" in body and "UNVALIDATED" in body
    assert " ".join(ui_text.text("UI_THERM01_DISCLOSURE", "en").split()) in _visible(body)
    abstained = client.post(THERM_URL % sid, data=_therm_form(
        screen={therm01.SCREEN_ITEMS[0]: therm01.SCREEN_YES})).get_data(as_text=True)
    assert "25.0 K" not in abstained
    assert _frozen(sid) == before

    # B1 (end) — the existing explicit exits close the Electronics journey.
    _accept_risk(client, sid, PHYSICAL_FEASIBILITY)
    served += _answer_until_exit(client, sid, BOUNDARY_AMBIGUITY, ELEC_BA)
    _accept_risk(client, sid, BOUNDARY_AMBIGUITY)
    governed = [q for q in served if q.startswith("PATHN:")]
    assert set(served) - set(governed) <= {"_STALL_REFRAME"}, served   # engine reframe prompt
    assert all(q.startswith("PATHN:N-") for q in governed), governed
    assert {q.split(":")[1].rsplit("-", 1)[0] for q in governed} == {"N-MC", "N-PF", "N-BA"}
    assert _state(sid).maturity_level == 2
    assert pl.select_next_gap(_state(sid)) not in (
        MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY)


# ==========================================================================
# C. Stage-15 integrated invention (three parts, Mechanical focus)
# ==========================================================================
def test_c_integrated_r1_journey(monkeypatch):
    client, _aid = _client_for("r1-integrated@example.com")

    # C1 — Mechanical + Electrical / Electronics with the optional control-loop part.
    sid = _integrated(client, MECHANICAL, **CTRL)
    parts = {s.domain: s for s in appmod._get_store().load_project_subsystems(sid)}
    assert list(parts) == [MECHANICAL, ELECTRONICS, CONTROL_LOOP]
    mech_id, elec_id = parts[MECHANICAL].subsystem_id, parts[ELECTRONICS].subsystem_id

    # C2 — one component linked to both required parts, and one interface.
    offered = _component_form(client.get(f"/session/{sid}").get_data(as_text=True))["parts"]
    assert mech_id in offered and elec_id in offered
    assert _declare_component(client, sid, *COMPONENT,
                              parts=(mech_id, elec_id)).status_code == 302
    binding = _bindings(client.get(f"/session/{sid}").get_data(as_text=True))[0]
    assert _declare_interface(client, sid, binding, INTERFACE).status_code == 302
    [interface] = appmod._get_store().load_subsystem_interfaces(sid)
    assert {interface.subsystem_a_id, interface.subsystem_b_id} == {mech_id, elec_id}
    iid = interface.interface_id

    # C3 — verification preparation, a declared dependency and one observation;
    # each save is confirmed from the durable store, not from its response.
    store = appmod._get_store()
    assert _save_preparation(client, sid, {
        (field, iid): text for field, text in PREPARATION.items()}).status_code == 200
    assert len(store.load_interface_preparations(sid)) == 1
    assert _dep_save(client, sid, iid, "one_way:%s:%s" % (mech_id, elec_id)).status_code == 200
    [dependency] = store.load_interface_dependencies(sid)
    assert (dependency.kind, dependency.dependent_subsystem_id) == ("one_way", mech_id)
    _observe(client, sid, _record_form(client, sid, iid), OBSERVATION)
    assert len(store.load_interface_observations(sid)) == 1

    # The non-focused required part's own governed questions.
    first = _part_question_ids(ELECTRONICS)[0]
    assert _save_part_answers(client, sid, elec_id, {first: PART_ANSWER},
                              form=_part_form(client, sid, elec_id)).status_code == 200
    assert len(store.load_part_answers(sid, elec_id)) == 1

    before = _database()

    # C4 — each admitted calculation, for its own declared part.
    body = client.post(CAP13_URL % sid, data=_cap13_form()).get_data(as_text=True)
    assert _part_line(body, "cap13") == PARTS["mech_part_name"]
    assert "750.0 N" in body and "UNVALIDATED" in body
    body = client.post(THERM_URL % sid, data=_therm_form()).get_data(as_text=True)
    assert _part_line(body, "therm01") == PARTS["elec_part_name"]
    assert "25.0 K" in body and "UNVALIDATED" in body

    # C2 / C3 (inspection) — the read-only Parts, Components & Interactions view.
    view = _visible(client.get(
        f"/session/{sid}/parts-components-interactions").get_data(as_text=True))
    for text in (PARTS["mech_part_name"], PARTS["elec_part_name"],
                 CTRL["ctrl_part_name"], COMPONENT[0], INTERFACE,
                 *PREPARATION.values()):
        assert text in view, text

    # C5 — the integrated report and PDF.
    for source in (_report(client, sid), _pdf_source(client, sid, monkeypatch)):
        text = _visible(source)
        assert ui_text.text("UI_S15_SCOPE_STATEMENT_3", "en") in text   # three-part copy
        assert CTRL["ctrl_part_name"] in text
        for expected in (COMPONENT[0], COMPONENT[1], INTERFACE, PART_ANSWER,
                         PREPARATION["acceptance_criterion"]):
            assert expected in text, expected
        assert OBSERVATION not in text                       # observations stay out

    # C5 — the Stage 35 Disclosure Export of the same project.
    r = client.get("/account/projects/%s/disclosure-export/json" % sid)
    assert r.status_code == 200
    fields = {f["field"]: f for f in json.loads(r.data.decode("utf-8"))["content"]["fields"]}
    names = [item["slots"]["name"]["value"] for item in fields["parts"]["items"]]
    assert names == [PARTS["mech_part_name"], PARTS["elec_part_name"],
                     CTRL["ctrl_part_name"]]
    [relationship] = fields["relationships"]["items"]
    assert relationship["slots"]["description"]["value"] == INTERFACE
    assert relationship["slots"]["dependency"]["tokens"]["dependency_kind"] == "one_way"
    part_keys = [item["item_key"] for item in fields["parts"]["items"]]
    assert sorted(relationship["refs"]) == sorted(part_keys[:2])
    [component] = fields["component_descriptions_beyond_parts"]["items"]
    assert component["slots"]["name"]["value"] == COMPONENT[0]
    assert component["refs"] == part_keys[:2]

    # Calculations, the view, the report, the PDF and the export wrote nothing.
    assert _database() == before
