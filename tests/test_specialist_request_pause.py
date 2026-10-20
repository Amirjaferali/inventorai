"""SPECIALIST-REQUEST-PAUSE-01 — an explicit specialist request on the two
parts-and-roles questions of MECHANISM_COMPLETENESS continues the journey.

For exactly `PATHN:N-MC-2` and `PATHN:mechanical:MECHANISM_COMPLETENESS:Q3`, a
`specialist_requested` action pauses the gap through the existing
UNKNOWN-QUESTION-PAUSE-01 mechanism (PR #835): the gap stays OPEN/PARTIAL and
keeps blocking Level 2, the next independent Stage-2 gap may be questioned and
the paused question stays available for a voluntary explicit answer. The
pending specialist request stays its own record in the Requirement Landscape
and the Validation Plan. Every other question, gap and disposition keeps its
existing semantics; histories recorded before the amendment reconstruct to the
same gaps, evidence and maturity. Synthetic ideas only.
"""
import copy
import html as _html
import re

import pytest

import engine.progression_loop as pl
import web.app as appmod
from engine.idea_state import (
    IdeaState, Gap, OPEN, PARTIAL, MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY,
)
from engine.path_n_questions import get_served_question
from engine.requirement_landscape import derive_requirement_landscape
from engine.session_reconstruction import reconstruct_readonly_state
from engine.validation_plan import derive_validation_plan
from tests.csrf_client import csrf_client
from web import ui_text

ELEC = "electronics_electrical"
MECH = "mechanical"
MC, PF = MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY
TARGETS = {ELEC: "PATHN:N-MC-2", MECH: "PATHN:mechanical:MECHANISM_COMPLETENESS:Q3"}
IDEAS = {
    ELEC: {"en": "I want a small device that reminds an elderly person to drink water.",
           "ar": "أريد جهازا صغيرا يذكّر شخصا مسنا بشرب الماء."},
    MECH: {"en": "I want a gate that closes by itself after someone walks through it.",
           "ar": "أريد بوابة تُغلق من تلقاء نفسها بعد أن يمر شخص من خلالها."},
}
# Answers that reach the target question without closing the gap.
LEAD_IN = {
    ELEC: {"en": ["It would notice the person has not pressed the button for two "
                  "hours and respond by playing a sound."],
           "ar": ["سيلاحظ المشكلة عندما لا يُضغط الزر لمدة ساعتين ثم يستجيب بتشغيل صوت."]},
    MECH: {"en": ["It closes.", "The gate moves."],
           "ar": ["تُغلق.", "البوابة تتحرك."]},
}
PF_ANSWER = ("It works because gravity pulls the gate closed, so no motor or power "
             "supply is needed for the closing movement.")
PARTS_ANSWER = ("The main parts are a timer that counts the hours, a speaker that "
                "plays the reminder because the timer triggers it, and a button "
                "the person presses after drinking.")


@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _page(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _state(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _token(body):
    return _html.unescape(re.search(r'name="answer_token" value="([^"]+)"', body).group(1))


def _question(body):
    m = re.search(r'<p class="question"[^>]*>(.*?)</p>', body, re.S)
    return " ".join(_html.unescape(m.group(1)).split()) if m else None


def _act(c, sid, action, text="", body=None):
    body = _page(c, sid) if body is None else body
    r = c.post(f"/session/{sid}", data={"response": text, "action": action,
                                       "answer_token": _token(body)})
    assert r.status_code == 302
    return r


def _paused_block(body, gap):
    start = body.find(f'data-paused-gap="{gap}"')
    if start < 0:
        return None
    return body[start:body.find("</div>\n", start)]


def _revisit(c, sid, gap, text, action="answered"):
    body = _page(c, sid)
    target = re.search(r'name="answer_target" value="([^"]+)"',
                       _paused_block(body, gap)).group(1)
    return c.post(f"/session/{sid}", data={
        "response": text, "action": action, "answer_token": _token(body),
        "answer_target": _html.unescape(target)})


def _start(c, domain, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.post("/start", data={"idea": IDEAS[domain][lang], "domain_choice": domain,
                               "domain_confirm": domain})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _at_target(c, domain, lang="en"):
    """A journey whose next ask is the domain's parts-and-roles question."""
    sid = _start(c, domain, lang)
    for text in LEAD_IN[domain][lang]:
        _act(c, sid, "answered", text)
    state = _state(sid)
    assert state.get_gap(MC).status in (OPEN, PARTIAL)
    target = appmod._answer_target_from(
        appmod._resolve_question_context(
            state, appmod.SESSION_STORE[sid].get("last_result")), state, False)
    assert target.identity == TARGETS[domain], target
    return sid


def _first(gap, domain):
    return " ".join(get_served_question(gap, 0, domain=domain).text.split())


def _full(state):
    return ([(g.gap_type, g.status, g.iterations_open, g.closed_at) for g in state.gaps],
            repr(state.known_mechanism), repr(state.known_problem),
            state.maturity_level, state.current_stage, state.iteration,
            sorted(pl.paused_gap_types(state)))


def _durable(sid):
    return [(r.disposition, r.gap_context, r.question_target)
            for r in appmod._get_store().load_contract(sid).assertions]


def _assert_parity(c, sid):
    live = _full(_state(sid))
    live_question = _question(_page(c, sid))
    assert _full(reconstruct_readonly_state(appmod._get_store(), sid).state) == live
    appmod.SESSION_STORE.clear()
    assert c.post(f"/session/{sid}/resume").status_code == 302
    assert _full(_state(sid)) == live
    assert _question(_page(c, sid)) == live_question


# ---------------------------------------------------------------------------
# 1. both targets, EN / AR: the request pauses the gap and the journey continues
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang", ["en", "ar"])
@pytest.mark.parametrize("domain", [ELEC, MECH])
def test_specialist_request_on_a_target_pauses_and_serves_the_next_gap(client, domain, lang):
    sid = _at_target(client, domain, lang)
    before = [(g.gap_type, g.status, g.iterations_open) for g in _state(sid).gaps]
    _act(client, sid, "specialist_requested", "")
    state = _state(sid)
    record = state.assertions[-1]
    assert (record.disposition, record.gap_context, record.question_target) == (
        "specialist_requested", MC, TARGETS[domain])
    assert record.pending == "specialist" and not record.resolves_gap
    assert [(g.gap_type, g.status, g.iterations_open) for g in state.gaps] == before
    assert pl.paused_gap_types(state) == {MC}
    assert state.get_gap(MC).status in (OPEN, PARTIAL)   # unresolved, still blocks Level 2
    assert state.maturity_level < 2 and state.current_stage == 2
    body = _page(client, sid)
    block = _paused_block(body, MC)
    assert block is not None
    assert _html.unescape(ui_text.text("UI_UQTR_MEANING_SPECIALIST_REQUESTED", lang)) \
        in _html.unescape(block)
    pf_first = get_served_question(PF, 0, domain=domain)
    expected = " ".join((pf_first.text_ar if lang == "ar" and pf_first.text_ar
                         else pf_first.text).split())
    assert _question(body) == expected
    assert 'id="uqtr-suppressed"' not in body


def test_pending_specialist_requirement_is_kept_beside_the_pause(client):
    sid = _at_target(client, ELEC)
    _act(client, sid, "specialist_requested", "Please ask an electronics specialist.")
    state = _state(sid)
    rec_id = state.assertions[-1].record_id
    req_id = "req:specialist:" + rec_id
    landscape = derive_requirement_landscape(state)
    assert req_id in [r.requirement_id for r in landscape.requirements]
    plan = derive_validation_plan(state)
    plan_ids = [s.step_id for s in plan.steps] + [repr(b) for b in plan.blocked_items]
    assert any(rec_id in i for i in plan_ids)
    # the pause is runtime serving only: both projections are what they are
    # without it, and nothing claims a specialist was assigned
    unpaused = copy.deepcopy(state)
    setattr(unpaused, "stage2_paused_gaps", frozenset())
    assert derive_requirement_landscape(unpaused) == landscape
    assert derive_validation_plan(unpaused) == plan
    # still pending after the inventor later answers the paused question
    _act(client, sid, "answered", PF_ANSWER)
    assert _revisit(client, sid, MC, PARTS_ANSWER).status_code == 302
    after = _state(sid)
    assert pl.paused_gap_types(after) == frozenset()
    assert req_id in [r.requirement_id for r in
                      derive_requirement_landscape(after).requirements]


# ---------------------------------------------------------------------------
# 2. exclusions: other questions, gaps and dispositions are unchanged
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("domain", [ELEC, MECH])
def test_specialist_request_on_the_first_mechanism_question_keeps_uqtr(client, domain):
    sid = _start(client, domain)
    _act(client, sid, "specialist_requested", "a note")
    assert _state(sid).assertions[-1].question_target != TARGETS[domain]
    assert pl.paused_gap_types(_state(sid)) == frozenset()
    body = _page(client, sid)
    assert 'id="uqtr-suppressed"' in body and 'data-paused-gap=' not in body


def test_specialist_request_on_mechanical_q2_keeps_uqtr(client):
    sid = _start(client, MECH)
    _act(client, sid, "answered", LEAD_IN[MECH]["en"][0])
    _act(client, sid, "specialist_requested")
    assert _state(sid).assertions[-1].question_target == \
        "PATHN:mechanical:MECHANISM_COMPLETENESS:Q2"
    assert pl.paused_gap_types(_state(sid)) == frozenset()


@pytest.mark.parametrize("action", ["evidence_requested", "provisional_assumption"])
def test_other_non_answers_on_a_target_keep_uqtr(client, action):
    sid = _at_target(client, ELEC)
    _act(client, sid, action, "a note")
    assert pl.paused_gap_types(_state(sid)) == frozenset()
    assert 'id="uqtr-suppressed"' in _page(client, sid)


def test_specialist_request_on_a_later_gap_does_not_pause_it(client):
    sid = _at_target(client, ELEC)
    _act(client, sid, "specialist_requested")          # MC paused -> PF served
    _act(client, sid, "specialist_requested")          # on PF's first question
    state = _state(sid)
    assert state.assertions[-1].gap_context == PF
    assert pl.paused_gap_types(state) == {MC}
    assert 'id="uqtr-suppressed"' in _page(client, sid)


def test_pausing_predicate_is_bound_to_the_exact_targets():
    assert pl.is_pausing_disposition("unknown", PF)
    assert pl.is_pausing_disposition("deferred", MC, None)
    for target in TARGETS.values():
        assert pl.is_pausing_disposition("specialist_requested", MC, target)
        assert not pl.is_pausing_disposition("specialist_requested", PF, target)
        assert not pl.is_pausing_disposition("evidence_requested", MC, target)
        assert not pl.is_pausing_disposition("specialist_requested", MC,
                                             target[len("PATHN:"):])
    for other in (None, "", "PATHN:N-MC-1", "PATHN:N-MC-3",
                  "PATHN:mechanical:MECHANISM_COMPLETENESS:Q1",
                  "PATHN:mechanical:MECHANISM_COMPLETENESS:Q4",
                  "PATHN:mechanical:PHYSICAL_FEASIBILITY:Q2"):
        assert not pl.is_pausing_disposition("specialist_requested", MC, other)
    assert pl.SPECIALIST_PAUSE_QUESTION_TARGETS == frozenset(TARGETS.values())


def test_applier_without_question_target_keeps_the_old_semantics():
    state = IdeaState(idea_id="x")
    state.gaps.append(Gap(gap_type=MC, status=OPEN, opened_at=0))
    pl.apply_owner_disposition(state, "specialist_requested", MC)
    assert pl.paused_gap_types(state) == frozenset()
    pl.apply_owner_disposition(state, "specialist_requested", MC, TARGETS[ELEC])
    assert pl.paused_gap_types(state) == {MC}


# ---------------------------------------------------------------------------
# 3. signed-target safety, failed writes, idempotency
# ---------------------------------------------------------------------------

def test_a_stale_form_cannot_record_a_pausing_request(client):
    sid = _start(client, ELEC)
    stale = _page(client, sid)                          # form for N-MC-1
    _act(client, sid, "answered", LEAD_IN[ELEC]["en"][0])
    durable = _durable(sid)
    client.post(f"/session/{sid}", data={"response": "", "action": "specialist_requested",
                                         "answer_token": _token(stale)})
    assert _durable(sid) == durable
    assert pl.paused_gap_types(_state(sid)) == frozenset()
    assert appmod.ANSWER_FORM_STALE_MESSAGE in _page(client, sid)


def test_paused_revisit_accepts_an_explicit_answer_only(client):
    sid = _at_target(client, ELEC)
    _act(client, sid, "specialist_requested")
    durable = _durable(sid)
    for action in ("specialist_requested", "unknown"):
        _revisit(client, sid, MC, "", action=action)
        assert _durable(sid) == durable
    assert pl.paused_gap_types(_state(sid)) == {MC}
    # the revisit is the exact question the request was made on
    paused = appmod._paused_question(_state(sid), MC)
    assert paused[0] == TARGETS[ELEC]


def test_failed_durable_write_pauses_nothing(client, monkeypatch):
    from engine.record_store import StoreError
    sid = _at_target(client, MECH)
    before = _full(_state(sid))
    records = list(_state(sid).assertions)
    store = appmod._get_store()
    monkeypatch.setattr(
        store, "append_record",
        lambda *a, **k: (_ for _ in ()).throw(StoreError("durable unavailable")))
    _act(client, sid, "specialist_requested")
    assert _state(sid).assertions == records
    assert _full(_state(sid)) == before
    assert appmod.INTERACTION_NOT_SAVED_MESSAGE in _page(client, sid)


def test_duplicate_request_stays_one_record_and_one_pause(client):
    sid = _at_target(client, ELEC)
    body = _page(client, sid)
    _act(client, sid, "specialist_requested", "same", body=body)
    durable = _durable(sid)
    full = _full(_state(sid))
    _act(client, sid, "specialist_requested", "same", body=body)   # resubmission
    assert _durable(sid) == durable
    assert _full(_state(sid)) == full


# ---------------------------------------------------------------------------
# 4. live == cold reconstruction == writable resume; revisit and corrections
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("domain", [ELEC, MECH])
def test_live_cold_and_resumed_states_agree(client, domain):
    sid = _at_target(client, domain)
    _act(client, sid, "specialist_requested")
    _assert_parity(client, sid)
    _act(client, sid, "answered", PF_ANSWER)
    _assert_parity(client, sid)


def test_revisit_resumes_the_gap_with_unchanged_grading(client):
    sid = _at_target(client, ELEC)
    _act(client, sid, "specialist_requested")
    _act(client, sid, "answered", PF_ANSWER)
    assert _revisit(client, sid, MC, PARTS_ANSWER).status_code == 302
    state = _state(sid)
    record = state.assertions[-1]
    assert (record.disposition, record.gap_context, record.question_target) == (
        "answered", MC, TARGETS[ELEC])
    assert pl.paused_gap_types(state) == frozenset()
    # the same answer integrated through the ordinary path grades identically
    probe = IdeaState(idea_id="p")
    probe.domain = ELEC
    probe.gaps.append(Gap(gap_type=MC, status=PARTIAL, opened_at=0))
    assert pl.integrate_response(probe, MC, "q", PARTS_ANSWER)[0] == "PASS"
    assert state.get_gap(MC).status == probe.get_gap(MC).status
    _assert_parity(client, sid)


def test_feasibility_correction_while_mechanism_is_active_still_fails_closed(client):
    sid = _at_target(client, ELEC)
    _act(client, sid, "specialist_requested")
    _act(client, sid, "answered", PF_ANSWER)
    pf_answer = [r for r in _state(sid).assertions
                 if r.gap_context == PF and r.disposition == "answered"][-1]
    _revisit(client, sid, MC, "I am still not sure which parts it needs.")
    before = _full(_state(sid))
    durable = _durable(sid)
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": pf_answer.record_id,
        "response": "Gravity closes it; nothing powered is needed.",
        "answer_token": _token(_page(client, sid))})
    assert _durable(sid) == durable
    assert _full(_state(sid)) == before
    assert appmod.CORRECTION_NOT_APPLIED_MESSAGE in _page(client, sid)
    _assert_parity(client, sid)


def test_correction_of_an_earlier_mechanism_answer_replays_consistently(client):
    sid = _at_target(client, ELEC)
    lead_in = _state(sid).assertions[-1]
    _act(client, sid, "specialist_requested")
    r = client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": lead_in.record_id,
        "response": ("It would notice that two hours have passed without the "
                     "button being pressed and respond by sounding a reminder."),
        "answer_token": _token(_page(client, sid))})
    assert r.status_code == 302
    assert _durable(sid)[-1][0] == "answered"
    _assert_parity(client, sid)


# ---------------------------------------------------------------------------
# 5. historical replay compatibility
# ---------------------------------------------------------------------------

def _structure_without_pause(state):
    return _full(state)[:-1]


@pytest.mark.parametrize("domain", [ELEC, MECH])
@pytest.mark.parametrize("after", ["nothing", "answer", "unknown"])
def test_histories_recorded_before_the_amendment_reconstruct_unchanged(
        client, monkeypatch, domain, after):
    """A history recorded under the pre-amendment semantics (the target set
    empty, so the request only suppressed the re-ask) reconstructs under the
    amendment to the same gaps, evidence, maturity, stage and iteration; only
    the runtime pause — and therefore what is served next — differs."""
    monkeypatch.setattr(pl, "SPECIALIST_PAUSE_QUESTION_TARGETS", frozenset())
    sid = _at_target(client, domain)
    _act(client, sid, "specialist_requested")
    if after == "answer":
        _act(client, sid, "answered", PARTS_ANSWER)     # the UQTR voluntary revisit
    elif after == "unknown":
        _act(client, sid, "unknown")
    old = _state(sid)
    old_structure = _structure_without_pause(old)
    old_records = _durable(sid)
    monkeypatch.undo()
    new = reconstruct_readonly_state(appmod._get_store(), sid)
    assert _structure_without_pause(new.state) == old_structure
    assert new.review.unapplied_answer_record_ids == ()
    assert _durable(sid) == old_records
    if after == "answer":
        assert pl.paused_gap_types(new.state) == frozenset()
    else:
        assert pl.paused_gap_types(new.state) == {MC}
    appmod.SESSION_STORE.clear()
    assert client.post(f"/session/{sid}/resume").status_code == 302
    assert _full(_state(sid)) == _full(new.state)
