"""UNKNOWN-QUESTION-PAUSE-01 — Stage-2 unknown / deferred pause and safe
journey continuation (Owner-approved bounded amendment to Stage-2 cascade
eligibility).

`unknown` / `deferred` on a Stage-2 question pauses that gap: it stays
OPEN/PARTIAL, unresolved and visible, is never re-asked automatically
(UQTR-01), keeps its `iterations_open`, and the next independent Stage-2 gap is
questioned. An explicit answer to the paused question (voluntary revisit)
resumes it. Maturity / stage gates, routed needs and every other disposition
are unchanged, and live, cold-reconstructed and resumed states agree.
"""
import html as _html
import re

import pytest

import engine.progression_loop as pl
import web.app as appmod
from engine.idea_state import (
    IdeaState, Gap, Evidence, OPEN, PARTIAL, CLOSED, REASONED, OWNER_STATED,
    MECHANISM_COMPLETENESS,
    PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY, STALLED,
)
from engine.path_n_questions import get_served_question
from engine.session_reconstruction import reconstruct_readonly_state
from tests.csrf_client import csrf_client
from web import ui_text

ELEC = "electronics_electrical"
MECH = "mechanical"
MC, PF, BA = MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY
IDEA = "I want something that waters my plants when needed."
MC_ANSWER = ("A float in a small tank drops as water is used, which opens a valve "
             "so water flows by gravity through tubes to each pot, because the "
             "valve lever is pushed by the float.")
PF_ANSWER = ("It works because gravity pulls the water down the tubes, and the "
             "valve only opens when the float drops, so no pump is needed.")


@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _start(c, domain, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.post("/start", data={"idea": IDEA, "domain_choice": domain,
                               "domain_confirm": domain})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _page(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _state(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _token(body):
    return _html.unescape(re.search(r'name="answer_token" value="([^"]+)"', body).group(1))


def _question(body):
    m = re.search(r'<p class="question"[^>]*>(.*?)</p>', body, re.S)
    return " ".join(_html.unescape(m.group(1)).split()) if m else None


def _act(c, sid, action, text=""):
    r = c.post(f"/session/{sid}", data={"response": text, "action": action,
                                       "answer_token": _token(_page(c, sid))})
    assert r.status_code == 302
    return r


def _paused_block(body, gap):
    start = body.find(f'data-paused-gap="{gap}"')
    if start < 0:
        return None
    return body[start:body.find("</div>\n", start)]


def _revisit(c, sid, gap, text):
    body = _page(c, sid)
    block = _paused_block(body, gap)
    target = re.search(r'name="answer_target" value="([^"]+)"', block).group(1)
    return c.post(f"/session/{sid}", data={
        "response": text, "action": "answered", "answer_token": _token(body),
        "answer_target": _html.unescape(target)})


def _first(gap, domain):
    return " ".join(get_served_question(gap, 0, domain=domain).text.split())


def _structural(state):
    return ([(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
            sorted(pl.paused_gap_types(state)), state.maturity_level,
            state.current_stage, state.iteration, repr(state.known_mechanism),
            repr(state.known_problem), state.direction)


# ---------------------------------------------------------------------------
# 1-2. unknown / deferred on the first gap -> the next independent gap opens;
#      the paused gap stays open, unprogressed and visible
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("domain", [ELEC, MECH])
@pytest.mark.parametrize("action", ["unknown", "deferred"])
def test_pause_serves_the_next_independent_gap_and_keeps_the_gap_open(client, domain, action):
    sid = _start(client, domain)
    asked = _question(_page(client, sid))
    before_mc = [(g.gap_type, g.status, g.iterations_open) for g in _state(sid).gaps]
    _act(client, sid, action)
    body = _page(client, sid)
    state = _state(sid)
    # the paused gap is unchanged, open and visibly identified
    assert [(g.gap_type, g.status, g.iterations_open) for g in state.gaps] == before_mc
    assert pl.paused_gap_types(state) == {MC}
    block = _paused_block(body, MC)
    assert block is not None
    assert ui_text.text("UI_UQTR_SUPPRESSED_HEADING", "en") in block
    assert ui_text.text("UI_UQTR_MEANING_" + action.upper(), "en") in block
    assert asked in " ".join(_html.unescape(block).split())     # revisit = the paused ask
    # it is not re-asked automatically; the next gap's first question is served
    assert _question(body) == _first(PF, domain) != asked
    assert 'id="uqtr-suppressed"' not in body
    assert state.maturity_level == 0 and state.current_stage == 2


@pytest.mark.parametrize("action", ["specialist_requested", "evidence_requested",
                                    "provisional_assumption"])
def test_other_non_answers_keep_the_existing_uqtr_suppression(client, action):
    sid = _start(client, ELEC)
    _act(client, sid, action, "a note")
    body = _page(client, sid)
    assert pl.paused_gap_types(_state(sid)) == frozenset()
    assert 'id="uqtr-suppressed"' in body
    assert 'data-paused-gap=' not in body
    assert [g.gap_type for g in _state(sid).gaps] == [MC]


# ---------------------------------------------------------------------------
# 3. target binding: the next gap's answer is integrated into that gap only
# ---------------------------------------------------------------------------

def test_answer_to_the_next_gap_binds_to_it_and_never_moves_the_paused_gap(client):
    sid = _start(client, ELEC)
    _act(client, sid, "unknown")
    _act(client, sid, "answered", PF_ANSWER)
    state = _state(sid)
    record = state.assertions[-1]
    assert (record.disposition, record.gap_context) == ("answered", PF)
    assert record.question_target == "PATHN:" + get_served_question(PF, 0, domain=ELEC).question_id
    gaps = {g.gap_type: g for g in state.gaps}
    assert (gaps[MC].status, gaps[MC].iterations_open) == (OPEN, 0)
    assert gaps[PF].iterations_open == 1
    assert pl.paused_gap_types(state) == {MC}


# ---------------------------------------------------------------------------
# 4. live == cold reconstruction == writable resume
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("domain", [ELEC, MECH])
def test_live_cold_and_resumed_journeys_are_identical(client, domain):
    sid = _start(client, domain)
    _act(client, sid, "unknown")
    _act(client, sid, "answered", PF_ANSWER)
    _act(client, sid, "deferred")
    live = _structural(_state(sid))
    live_question = _question(_page(client, sid))
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    assert _structural(recon.state) == live
    appmod.SESSION_STORE.clear()
    assert client.post(f"/session/{sid}/resume").status_code == 302
    assert _structural(_state(sid)) == live
    assert _question(_page(client, sid)) == live_question


# ---------------------------------------------------------------------------
# 5-6. explicit revisit resumes the gap; counters and stall are unaffected
# ---------------------------------------------------------------------------

def test_revisit_answer_resumes_the_paused_gap_and_normal_serving(client):
    sid = _start(client, ELEC)
    paused_ask = _question(_page(client, sid))
    _act(client, sid, "unknown")
    _act(client, sid, "answered", PF_ANSWER)
    pf_before = _state(sid).get_gap(PF).iterations_open
    r = _revisit(client, sid, MC, MC_ANSWER)
    assert r.status_code == 302
    state = _state(sid)
    record = state.assertions[-1]
    assert (record.disposition, record.gap_context) == ("answered", MC)
    assert record.question_target == "PATHN:" + get_served_question(MC, 0, domain=ELEC).question_id
    assert pl.paused_gap_types(state) == frozenset()
    assert state.get_gap(MC).iterations_open == 1          # questioned once
    assert state.get_gap(PF).iterations_open == pf_before  # an open, unasked gap never moves
    body = _page(client, sid)
    assert pl.select_next_gap(state) == MC
    assert _question(body) != paused_ask and 'data-paused-gap=' not in body
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    assert _structural(recon.state) == _structural(state)


def test_paused_revisit_accepts_an_explicit_answer_only(client):
    sid = _start(client, ELEC)
    _act(client, sid, "unknown")
    body = _page(client, sid)
    target = _html.unescape(re.search(
        r'name="answer_target" value="([^"]+)"', _paused_block(body, MC)).group(1))
    before = len(_state(sid).assertions)
    client.post(f"/session/{sid}", data={"response": "", "action": "unknown",
                                         "answer_token": _token(body),
                                         "answer_target": target})
    assert len(_state(sid).assertions) == before
    assert appmod.ANSWER_FORM_STALE_MESSAGE in _page(client, sid)


def test_no_revisit_form_while_a_higher_priority_gap_is_active(client):
    sid = _start(client, ELEC)
    _act(client, sid, "unknown")                     # MC paused
    _act(client, sid, "answered", "I am not sure yet")
    _act(client, sid, "deferred")                    # PF paused -> BA served
    body = _page(client, sid)
    assert pl.paused_gap_types(_state(sid)) == {MC, PF}
    assert _question(body) == _first(BA, ELEC)
    _revisit(client, sid, MC, MC_ANSWER)             # MC resumed and active
    body = _page(client, sid)
    block = _paused_block(body, PF)
    assert block is not None and 'name="answer_target"' not in block
    assert not pl.paused_gap_answerable(_state(sid), PF)


def test_pause_never_counts_as_a_stall_or_moves_iterations():
    state = IdeaState(idea_id="pause-unit")
    state.domain = ELEC
    state.path = "N"
    state.maturity_level = 1
    state.gaps = [Gap(MC, PARTIAL, 0), Gap(PF, OPEN, 0)]
    state.get_gap(MC).iterations_open = pl.STALL_THRESHOLD + 2
    pl.apply_owner_disposition(state, "unknown", MC)
    pl.update_direction(state, state.maturity_level)
    assert state.direction != STALLED
    assert state.get_gap(MC).iterations_open == pl.STALL_THRESHOLD + 2
    assert pl.select_next_gap(state) == PF


# ---------------------------------------------------------------------------
# 7. gates unchanged: a paused gap still blocks Level 2; no closure, no stage
# ---------------------------------------------------------------------------

def test_maturity_and_stage_gates_are_unchanged_by_a_pause():
    state = IdeaState(idea_id="pause-gates")
    state.domain = ELEC
    state.path = "N"
    state.maturity_level = 1
    state.gaps = [Gap(MC, PARTIAL, 0), Gap(PF, CLOSED, 0), Gap(BA, CLOSED, 0)]
    state.known_mechanism = Evidence(content="x", quality=REASONED, iteration=1,
                                     provenance=OWNER_STATED)
    pl.apply_owner_disposition(state, "deferred", MC)
    can, reason = pl.evaluate_transition(state)
    assert not can and MC in reason
    assert pl.select_next_gap(state) is None and pl.deferred_open_gap(state) is None
    assert state.get_gap(MC).status == PARTIAL
    assert (state.maturity_level, state.current_stage) == (1, 2)
    # Stage-3 gaps never pause
    state.current_stage = 3
    pl.apply_owner_disposition(state, "unknown", "PROBLEM_MECHANISM_FIT")
    assert pl.paused_gap_types(state) == {MC}


# ---------------------------------------------------------------------------
# 8. every remaining gap paused -> honest review handoff, no loop
# ---------------------------------------------------------------------------

def test_all_gaps_paused_reaches_the_existing_review_handoff(client):
    sid = _start(client, ELEC)
    for action in ("unknown", "deferred", "unknown"):
        _act(client, sid, action)
    state = _state(sid)
    assert pl.paused_gap_types(state) == {MC, PF, BA}
    assert all(g.status == OPEN and g.iterations_open == 0 for g in state.gaps)
    _page(client, sid)                               # consumes the one-shot acknowledgement
    before = (_structural(state), len(state.assertions))
    bodies = {_page(client, sid).split('name="answer_token"')[0] for _ in range(3)}
    assert (_structural(state), len(state.assertions)) == before
    body = _page(client, sid)
    assert _question(body) is None and 'id="answer-form"' not in body
    assert len(bodies) == 1
    assert ui_text.text("UI_A1_REVIEW_HANDOFF", "en") in body
    assert ui_text.text("UI_NO_QUESTION_NOTE", "en") in body
    assert [g for g in ("data-paused-gap=\"%s\"" % x for x in (MC, PF, BA)) if g in body] \
        == ['data-paused-gap="%s"' % x for x in (MC, PF, BA)]
    assert state.maturity_level < 2 and state.get_open_gaps()


# ---------------------------------------------------------------------------
# 9. routed needs unchanged (Mechanical PF:Q2 routing)
# ---------------------------------------------------------------------------

def test_routed_need_behaviour_is_unchanged_beside_a_pause(client):
    sid = _start(client, MECH)
    _act(client, sid, "unknown")                     # MC paused, PF served
    _act(client, sid, "answered", PF_ANSWER)          # PF Q1 -> routed Q2 -> exhausted
    state = _state(sid)
    assert appmod._need_routing.owner_questioning_exhausted(state, state.get_gap(PF))
    body = _page(client, sid)
    assert 'class="routed-need' in body
    assert _question(body) == _first(BA, MECH)


# ---------------------------------------------------------------------------
# 10. pre-amendment histories replay unchanged
# ---------------------------------------------------------------------------

def test_unknown_then_answer_on_the_same_gap_matches_the_answer_alone(client):
    with_unknown = _start(client, ELEC)
    _act(client, with_unknown, "unknown")
    _revisit(client, with_unknown, MC, MC_ANSWER)
    plain = _start(client, ELEC)
    _act(client, plain, "answered", MC_ANSWER)
    a, b = _structural(_state(with_unknown)), _structural(_state(plain))
    assert a == b
    assert _structural(reconstruct_readonly_state(
        appmod._get_store(), with_unknown).state) == b


# ---------------------------------------------------------------------------
# 11. Arabic presentation
# ---------------------------------------------------------------------------

def test_arabic_page_serves_the_next_question_and_paused_notice_in_arabic(client):
    sid = _start(client, ELEC, lang="ar")
    _act(client, sid, "deferred")
    body = _page(client, sid)
    assert _question(body) == " ".join(get_served_question(PF, 0, domain=ELEC).text_ar.split())
    block = _paused_block(body, MC)
    assert ui_text.text("UI_UQTR_MEANING_DEFERRED", "ar") in block
    assert ui_text.text("UI_UQTR_REVISIT", "ar") in block
    assert 'class="paused-question-text" lang="ar" dir="rtl"' in block
    assert ui_text.text("UI_UQTR_MEANING_DEFERRED", "en") not in body
