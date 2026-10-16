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


# ---------------------------------------------------------------------------
# 12. Review finding 1 — a routed-need note never rebinds a paused revisit
# ---------------------------------------------------------------------------

def _routed_note(c, sid, text="A specialist will check this."):
    body = _page(c, sid)
    form = body[body.find('class="routed-need-form"'):]
    target = _html.unescape(re.search(r'name="answer_target" value="([^"]+)"', form).group(1))
    return c.post(f"/session/{sid}", data={
        "response": text, "action": "provisional_assumption",
        "answer_token": _token(body), "answer_target": target})


def _paused_text(body, gap):
    block = _paused_block(body, gap)
    m = re.search(r'class="paused-question-text"[^>]*>(.*?)</p>', block, re.S)
    return " ".join(_html.unescape(m.group(1)).split()) if m else None


def test_routed_note_cannot_rebind_the_paused_question(client):
    # Astra's sequence: pause mechanism, then pause the Mechanical feasibility
    # question, then record a note on its specialist-routed question.
    sid = _start(client, MECH)
    _act(client, sid, "unknown")
    paused_ask = _question(_page(client, sid))
    _act(client, sid, "unknown")
    assert pl.paused_gap_types(_state(sid)) == {MC, PF}
    assert _paused_text(_page(client, sid), PF) == paused_ask
    assert _routed_note(client, sid).status_code == 302
    note = _state(sid).assertions[-1]
    routed = appmod._need_routing.outstanding_routed_question_ids(_state(sid), PF)
    assert note.disposition == "provisional_assumption"
    assert note.question_target[len("PATHN:"):] in routed
    body = _page(client, sid)
    # the revisit stays bound to the question the owner actually paused
    assert _paused_text(body, PF) == paused_ask
    target = _html.unescape(re.search(
        r'name="answer_target" value="([^"]+)"', _paused_block(body, PF)).group(1))
    assert appmod._verified_answer_target(sid, _token(body), target).identity \
        == "PATHN:" + get_served_question(PF, 0, domain=MECH).question_id
    # and a forged revisit for the routed question is refused at POST
    forged = appmod._issue_answer_target(sid, _token(body), appmod._AnswerTarget(
        appmod.UQTR_TARGET_PAUSED_QUESTION, note.question_target, PF,
        getattr(_state(sid), "engine_contract_version", None)))
    before = len(_state(sid).assertions)
    client.post(f"/session/{sid}", data={"response": PF_ANSWER,
                                         "answer_token": _token(body),
                                         "answer_target": forged})
    assert len(_state(sid).assertions) == before
    assert pl.paused_gap_types(_state(sid)) == {MC, PF}


def test_a_paused_question_that_is_a_routed_need_offers_no_answer_form(client):
    sid = _start(client, MECH)
    _act(client, sid, "unknown")
    _act(client, sid, "unknown")                      # PF Q1 paused
    state = _state(sid)
    record = [r for r in state.assertions if r.gap_context == PF][-1]
    routed = sorted(appmod._need_routing.outstanding_routed_question_ids(state, PF))
    record.question_target = "PATHN:" + routed[0]     # a routed identity
    assert appmod._paused_question(state, PF) is None
    assert appmod._paused_question_target(state, PF, record.question_target) is None
    block = _paused_block(_page(client, sid), PF)
    assert block is not None and 'name="answer_target"' not in block


# ---------------------------------------------------------------------------
# 13. Review finding 2 — a correction is never integrated into another gap
# ---------------------------------------------------------------------------

def _astra_finding_2(c, domain=ELEC):
    sid = _start(c, domain)
    _act(c, sid, "unknown")                           # pause mechanism
    _act(c, sid, "answered", PF_ANSWER)               # answer feasibility
    assert _revisit(c, sid, MC, MC_ANSWER).status_code == 302   # revisit mechanism
    pf_answer = [r for r in _state(sid).assertions
                 if r.gap_context == PF and r.disposition == "answered"][-1]
    return sid, pf_answer


CORRECTED_PF = "It works because gravity moves the water; no electric pump at all."


def test_feasibility_correction_while_mechanism_is_active_fails_closed(client):
    sid, pf_answer = _astra_finding_2(client)
    before = _structural(_state(sid))
    durable_before = len(appmod._get_store().load_contract(sid).assertions)
    r = client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": pf_answer.record_id, "response": CORRECTED_PF,
        "answer_token": _token(_page(client, sid))})
    assert r.status_code == 302
    assert _structural(_state(sid)) == before          # mechanism untouched
    assert len(appmod._get_store().load_contract(sid).assertions) == durable_before
    assert appmod.CORRECTION_NOT_APPLIED_MESSAGE in _page(client, sid)
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    assert _structural(recon.state) == before
    appmod.SESSION_STORE.clear()
    assert client.post(f"/session/{sid}/resume").status_code == 302
    assert _structural(_state(sid)) == before


def test_a_stored_incompatible_correction_replays_explicitly_unapplied(client, monkeypatch):
    # Defence in depth: even if such a correction is durably recorded, replay
    # never integrates it into the mechanism gap.
    sid, pf_answer = _astra_finding_2(client)
    def _mechanism(state):
        gap, known = state.get_gap(MC), state.known_mechanism
        # the replay iteration stamp shifts because the superseded answer is
        # withdrawn (existing full-replay behaviour); the substance must not.
        return (gap.status, gap.iterations_open, known.content, known.quality)
    mc_before = _mechanism(_state(sid))
    monkeypatch.setattr(appmod, "answer_applicable", lambda *a, **k: True)
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": pf_answer.record_id, "response": CORRECTED_PF,
        "answer_token": _token(_page(client, sid))})
    monkeypatch.undo()
    correction = appmod._get_store().load_contract(sid).assertions[-1]
    assert (correction.disposition, correction.gap_context) == ("answered", PF)
    assert pf_answer.record_id in correction.supersedes
    for state in (_state(sid),
                  reconstruct_readonly_state(appmod._get_store(), sid).state):
        assert _mechanism(state) == mc_before
    review = reconstruct_readonly_state(appmod._get_store(), sid).review
    assert review.unapplied_answer_record_ids == (correction.record_id,)


def test_correction_of_the_selected_gap_still_applies_normally(client):
    sid = _start(client, ELEC)
    _act(client, sid, "unknown")
    _act(client, sid, "answered", "It just works somehow.")
    target = _state(sid).assertions[-1]
    assert target.gap_context == PF and pl.select_next_gap(_state(sid)) == PF
    r = client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": target.record_id, "response": PF_ANSWER,
        "answer_token": _token(_page(client, sid))})
    assert r.status_code == 302
    latest = _state(sid).assertions[-1]
    assert latest.gap_context == PF and target.record_id in latest.supersedes
    assert pl.paused_gap_types(_state(sid)) == {MC}
    assert _state(sid).get_gap(MC).iterations_open == 0
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    assert _structural(recon.state) == _structural(_state(sid))
    assert recon.review.unapplied_answer_record_ids == ()
