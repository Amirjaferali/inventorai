"""G1-ROUTED-RECOVERY-CONTINUATION-01 — while routed recovery is the Compass primary action, the
integrated step the EXISTING guidance owner already derived is offered as ONE secondary link.

Synthetic data only. What is pinned:
  * the routed-recovery primary action is unchanged and stays the ONLY primary action;
  * the secondary link is the step `_integrated_journey_guidance` derives (part questions ->
    interaction -> components -> participation -> interaction preparation), with the same target
    and the same availability condition as that step's own primary branch;
  * rendering the page or following the link changes nothing: no gap, maturity, routing,
    substantive-attempt, accepted-risk, record or R2 effect;
  * no link while a governed question is served, on a single-domain project, or when the owner
    derives nothing usable (None, kind None, a declaration form that is not on the page);
  * the existing correction / accepted-risk recovery behaves exactly as before;
  * EN / AR copy states the boundary (the routed point stays open; nothing is resolved or shown
    ready), Arabic is RTL.
"""
import html as _html
import re

import pytest

import web.app as appmod
from engine import need_routing as nr
from engine import progression_loop as pl
from engine.idea_state import (ACCEPTED_RISK, BOUNDARY_AMBIGUITY as BA, MECHANISM_COMPLETENESS as MC,
                               PHYSICAL_FEASIBILITY as PF)
from tests.test_g1_integrated_engineering_continuation import (
    IDEA, PARTS, _answer, _participate, _primary, _raw, _to_participation, client)  # noqa: F401
from tests.test_28t5_nonfocused_required_part_questions import _ids, _part, _save as _save_part
from tests.test_safe_question_routing_pf_q2 import (
    BA_1, BA_2, MECH as MECH_ANSWER, PF_STRONG, _accept_pf_via_route, _facts, _start)
from tests.test_safe_question_routing_pf_q2_weak_recovery import WEAK, _correct
from tests.test_stage15_integrated_invention_entry import ELEC, MECH, _compose, _created, _live
from web import ui_text

LINK_RE = re.compile(r'<a data-rrc-link data-rrc-kind="([^"]+)" href="([^"]*)"')


def _integrated(c, lang=None):
    return _created(_compose(c, IDEA, focus=MECH, lang=lang, **PARTS))


def _to_routed_recovery(c, sid):
    """Mechanism and Boundary closed by the inventor's own answers; ONE non-substantive Physical
    Feasibility answer, so the routed point waits and accepting it as a risk is not available."""
    for value in (MECH_ANSWER, MECH_ANSWER, WEAK, BA_1, BA_2):
        _answer(c, sid, value)
    state = _live(sid)
    assert state.get_gap(PF).status == "OPEN"
    assert not pl.substantive_attempt_recorded(state, PF)
    assert nr.gap_has_outstanding_routing(state, PF)
    return state


def _links(page):
    return LINK_RE.findall(page)


def _snapshot(sid):
    state = _live(sid)
    return (_facts(state), pl.substantive_attempt_recorded(state, PF),
            tuple(r.record_id for r in state.assertions),
            len(appmod._get_store().load_contract(sid).assertions))


def _href(page):
    return _html.unescape(re.search(r'data-primary-action[^>]*href="([^"]*)"', page).group(1))


# ==========================================================================
# 1-2. the blocked case: routed recovery primary, ONE eligible secondary link
# ==========================================================================
def test_01_routed_recovery_stays_primary_and_one_part_step_is_secondary(client):
    sid = _integrated(client)
    _to_routed_recovery(client, sid)
    page = _raw(client, sid)
    _primary(page)                                            # exactly one primary action
    assert _href(page) == "#routed-recovery"
    assert 'id="routed-recovery"' in page and 'href="#correct-answer"' in page
    assert "routed-accept-risk" not in page
    expected = "/session/%s/part-questions?part=%s" % (sid, _part(sid, ELEC))
    assert [(k, _html.unescape(h)) for k, h in _links(page)] == [("part_questions", expected)]
    assert ui_text.text("UI_RRC_NOTE", "en") in _html.unescape(page)
    assert ui_text.text("UI_IJG_PART_CTA_ELEC", "en") in _html.unescape(page)
    assert "data-rrc-link data-primary-action" not in page and page.count("data-rrc-link") == 1


def test_02_following_the_link_reaches_the_existing_form_and_changes_nothing(client):
    sid = _integrated(client)
    _to_routed_recovery(client, sid)
    before = _snapshot(sid)
    [(kind, href)] = _links(_raw(client, sid))
    response = client.get(_html.unescape(href))
    assert response.status_code == 200
    assert 'name="part_answer__' in response.get_data(as_text=True)    # the existing editable form
    _raw(client, sid)
    assert _snapshot(sid) == before


def test_03_the_secondary_step_follows_the_existing_owner_and_never_moves_the_routed_point(client):
    sid = _integrated(client)
    _to_routed_recovery(client, sid)
    pf_before = (_live(sid).get_gap(PF).status, _live(sid).maturity_level, tuple(_live(sid).need_routing))
    seen = []
    # each step is performed through its existing form; the link only points there
    assert _save_part(client, sid, _part(sid, ELEC),
                      {q: "My own words about it." for q in _ids(ELEC)}).status_code == 200
    seen.append(_links(_raw(client, sid))[0][0])
    _to_participation(client, sid)
    seen.append(_links(_raw(client, sid))[0][0])
    _participate(client, sid)
    seen.append(_links(_raw(client, sid))[0][0])
    assert seen == ["declare_interaction", "participation", "interface_preparation"]
    page = _raw(client, sid)
    assert _href(page) == "#routed-recovery"
    state = _live(sid)
    assert (state.get_gap(PF).status, state.maturity_level, tuple(state.need_routing)) == pf_before
    assert not pl.substantive_attempt_recorded(state, PF)
    assert state.get_gap(MC).status == "CLOSED" and state.get_gap(BA).status == "CLOSED"


def test_04_component_and_participation_steps_are_offered_with_their_own_targets(client):
    sid = _integrated(client)
    _to_routed_recovery(client, sid)
    _save_part(client, sid, _part(sid, ELEC), {q: "My own words about it." for q in _ids(ELEC)})
    from tests.test_stage15_subsystem_interface_declaration import _declare as _declare_interface
    from tests.test_component_inventory_declare_list import _declare as _declare_component
    assert _declare_interface(client, sid, "The board sits inside the case.").status_code == 302
    assert _links(_raw(client, sid)) == [("component_inventory", "#component_name")]
    _declare_component(client, sid, name="Control board", function="Carries the circuit")
    _declare_component(client, sid, name="Plastic enclosure", function="Surrounds the board")
    [(kind, href)] = _links(_raw(client, sid))
    assert kind == "participation"
    assert _html.unescape(href) == "/session/%s/interface-preparation#participation-heading" % sid
    assert client.get("/session/%s/interface-preparation" % sid).status_code == 200


# ==========================================================================
# 4-5. no new action where the owner offers nothing, or a question is served
# ==========================================================================
def test_05_no_link_while_a_governed_question_is_served(client):
    sid = _integrated(client)
    page = _raw(client, sid)
    assert 'id="answer-form"' in page and _href(page) == "#response"
    assert "data-rrc" not in page


def test_06_single_domain_routed_recovery_gets_no_link(client):
    sid = _start(client)
    for value in (MECH_ANSWER, MECH_ANSWER, WEAK, BA_1, BA_2):
        _answer(client, sid, value)
    page = _raw(client, sid)
    assert _href(page) == "#routed-recovery"
    assert "data-rrc" not in page


@pytest.mark.parametrize("derived", [None, {"kind": None, "clearance": []},
                                     {"kind": "declare_interaction", "clearance": []},
                                     {"kind": "unknown_kind", "clearance": []}])
def test_07_nothing_usable_from_the_owner_means_no_link(client, monkeypatch, derived):
    sid = _start(client)                                 # no interaction or component forms here
    for value in (MECH_ANSWER, MECH_ANSWER, WEAK, BA_1, BA_2):
        _answer(client, sid, value)
    monkeypatch.setattr(appmod, "_integrated_journey_guidance", lambda *_a, **_k: derived)
    page = _raw(client, sid)
    assert _href(page) == "#routed-recovery"
    assert "data-rrc" not in page


def test_08_an_unreadable_composition_keeps_the_routed_recovery_alone(client, monkeypatch):
    sid = _integrated(client)
    _to_routed_recovery(client, sid)

    def broken(*_a, **_k):
        raise RuntimeError("unreadable")
    monkeypatch.setattr(appmod._get_store(), "load_nonfocused_part_record", broken)
    page = _raw(client, sid)
    assert _href(page) == "#routed-recovery" and "data-rrc" not in page


def test_09_a_stranger_or_anonymous_client_cannot_follow_the_owners_link(client):
    from tests.test_p10_d3a_self_service_project_export import _client_for
    owner, _aid = _client_for("rrc-owner@example.com")
    sid = _integrated(owner)
    _to_routed_recovery(owner, sid)
    [(_kind, href)] = _links(_raw(owner, sid))
    href = _html.unescape(href)
    assert owner.get(href).status_code == 200
    stranger, _ = _client_for("rrc-stranger@example.com")
    for other in (stranger, client):
        response = other.get(href)
        assert response.status_code != 200 and b"part_answer__" not in response.data
        assert b"data-rrc" not in other.get("/session/%s" % sid).data


# ==========================================================================
# 6. EN / AR
# ==========================================================================
def test_10_copy_is_bilingual_and_states_the_boundary():
    en = ui_text.text("UI_RRC_NOTE", "en")
    ar = ui_text.text("UI_RRC_NOTE", "ar")
    assert en and ar and en != ar
    assert "does not answer or resolve" in en and "Optional" in en
    assert "none of it shows that the idea is ready" in en
    assert "لا يجيب" in ar and "ولا يحلّها" in ar and "اختياري" in ar and "جاهزة" in ar
    for word in ("validat", "verified", "compatib", "safe", "recommend"):
        assert word not in en.lower()


def test_11_arabic_page_is_rtl_with_the_arabic_link(client):
    sid = _integrated(client, lang="ar")
    _to_routed_recovery(client, sid)
    page = _html.unescape(_raw(client, sid))
    assert 'dir="rtl"' in page
    assert ui_text.text("UI_RRC_NOTE", "ar") in page
    assert ui_text.text("UI_IJG_PART_CTA_ELEC", "ar") in page
    client.post("/ui-language", data={"lang": "en"})


# ==========================================================================
# 7. the existing recovery is unchanged
# ==========================================================================
def test_12_correction_and_explicit_risk_acceptance_behave_as_before(client):
    sid = _integrated(client)
    state = _to_routed_recovery(client, sid)
    weak = [r for r in state.assertions if r.gap_context == PF and r.disposition == "answered"
            and r.superseded_by is None][-1]
    assert _correct(client, sid, weak.record_id, PF_STRONG).status_code == 302
    assert pl.substantive_attempt_recorded(_live(sid), PF)
    page = _raw(client, sid)
    assert 'id="routed-recovery"' not in page and "data-rrc" not in page
    assert "routed-accept-risk" in page
    assert _accept_pf_via_route(client, sid).status_code == 302
    assert _live(sid).get_gap(PF).status == ACCEPTED_RISK


# ==========================================================================
# the reported inventor case: ordinary-language answers, frozen before the trace
# ==========================================================================
BOARD_PARTS = dict(mech_part_name="Plastic case", mech_part_function="Holds the board",
                   elec_part_name="Small circuit board",
                   elec_part_function="Reads the temperature and lights the LED")
ORDINARY = {
    "MECHANISM_COMPLETENESS:Q1": "You switch it on, the board checks how warm it is, and if it gets warm the "
                                 "little light comes on. The case just holds the board so it doesn't rattle around.",
    "MECHANISM_COMPLETENESS:Q2": "Nothing really moves. The board sits on little posts inside the box and the "
                                 "lid closes over it.",
    "MECHANISM_COMPLETENESS:Q3": "A plastic box to hold everything, the board inside it, a small heat sensor and "
                                 "a light you can see from outside.",
    "MECHANISM_COMPLETENESS:Q4": "I know what it should do, but I don't know how big the box needs to be or "
                                 "exactly how the board is held in place.",
    "PHYSICAL_FEASIBILITY:Q1": "Nothing pushes or turns. It just sits there; the screws and its own weight keep "
                               "the board in place in the case.",
    "BOUNDARY_AMBIGUITY:Q1": "It should show when something gets warm. It is not meant to cool anything down "
                             "or to be waterproof.",
    "BOUNDARY_AMBIGUITY:Q2": "It's only for indoors on a desk; it is not meant to be dropped or used outside "
                             "in the rain.",
    "BOUNDARY_AMBIGUITY:Q3": "Maybe one of those little stick-on thermometers, but I'm not sure.",
    "BOUNDARY_AMBIGUITY:Q4": "Unlike a normal thermometer it doesn't show a number, it only lights up when it "
                             "gets warm.",
}


def test_13_the_ordinary_language_inventor_case_now_has_a_way_forward(client):
    from tests.test_g1_integrated_journey_recovery import BOARD_IDEA
    from tests.test_safe_question_routing_pf_q2 import _answer_form_target
    sid = _created(_compose(client, BOARD_IDEA, focus=MECH, **BOARD_PARTS))
    for _step in range(20):
        page = _raw(client, sid)
        if 'id="answer-form"' not in page:
            break
        question = _answer_form_target(client, sid)["q"].replace("PATHN:mechanical:", "")
        token = _html.unescape(re.search(r'name="answer_token" value="([^"]+)"', page).group(1))
        target = _html.unescape(re.search(r'<form id="answer-form".*?name="answer_target" value="([^"]*)"',
                                          page, re.S).group(1))
        text = ORDINARY.get(question)
        data = {"response": text or "", "answer_token": token, "answer_target": target,
                "action": "answered" if text else "unknown"}
        assert client.post(f"/session/{sid}", data=data).status_code == 302
    state = _live(sid)
    assert state.get_gap(PF).status == "OPEN" and not pl.substantive_attempt_recorded(state, PF)
    page = _raw(client, sid)
    assert _href(page) == "#routed-recovery" and "routed-accept-risk" not in page
    assert [k for k, _h in _links(page)] == ["part_questions"]
