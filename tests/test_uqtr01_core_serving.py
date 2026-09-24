"""UQTR-01 CORE IMPLEMENTATION CANDIDATE 01 — gap-scoped non-answer serving
suppression, voluntary revisit, the 4 + 2 response group, and the exhausted-
prompt truth fix.

Authority: Owner authorization "UQTR-01 CORE IMPLEMENTATION CANDIDATE 01";
docs/governance/W2_B_RVR6A_CONTRACT_AMENDMENT_2_UQTR01_CANDIDATE.md.

Binding separation proved here: SERVING changes; STRUCTURAL PROGRESSION (gap
status, iterations, maturity, stage, completion) and VERIFICATION (validation,
derived readiness, eligibility) do not. Question suppression is not gap
resolution.

Fixtures are neutral synthetic ideas written for this file. The frozen T1-C′
study corpus and the S2 benchmark cases are deliberately NOT used.
"""
import copy
import html as _html
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

import engine.progression_loop as pl
from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    IdeaState, Gap, Evidence, OPEN, CLOSED, ACCEPTED_RISK, REASONED, OWNER_STATED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY,
)
from engine.session_reconstruction import reconstruct_readonly_state
from tests.csrf_client import csrf_client
from web import ui_text
import web.app as appmod

# Neutral synthetic seed (electronics, written for this file).
SEED = ("a small device that switches off a room heater when the room gets "
        "too warm, using a temperature sensor and a relay circuit")
NOTE = "I am not sure about this part yet."
ANSWER = ("The temperature sensor output is compared with a set threshold; when "
          "the room is too warm the comparator switches the relay and the relay "
          "cuts power to the heater until the room cools down again.")

NON_ANSWERS = ("unknown", "deferred", "provisional_assumption",
               "specialist_requested", "evidence_requested")
SIX = ("answered", "unknown", "deferred", "provisional_assumption",
       "specialist_requested", "evidence_requested")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _start(c, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.post("/start", data={"idea": SEED,
                               "domain_confirm": "electronics_electrical"})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _page(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _token(c, sid):
    m = re.search(r'name="answer_token" value="([^"]+)"', _page(c, sid))
    return _html.unescape(m.group(1))


def _non_answer(c, sid, action, text=NOTE):
    r = c.post(f"/session/{sid}", data={"response": text, "action": action})
    assert r.status_code == 302
    return r


def _answer(c, sid, text=ANSWER):
    r = c.post(f"/session/{sid}", data={
        "response": text, "action": "answered", "answer_token": _token(c, sid)})
    assert r.status_code == 302
    return r


def _question(body):
    m = re.search(r'<p class="question"[^>]*>(.*?)</p>', body, re.S)
    return _html.unescape(m.group(1)).strip() if m else None


def _revisit_block(body):
    """The whole voluntary-revisit disclosure, nested <details> included."""
    start = body.find('<details class="uqtr-revisit"')
    if start < 0:
        return None
    depth, pos = 0, start
    for m in re.finditer(r"<details\b|</details>", body[start:]):
        depth += 1 if m.group(0) == "<details" else -1
        if depth == 0:
            return body[start:start + m.end()]
    raise AssertionError("unterminated revisit disclosure")


def _outside_revisit(body):
    block = _revisit_block(body)
    return body.replace(block, "") if block else body


def _structural(state):
    pkg = assemble_deliverable(state)["_session_meta"]
    return (
        [(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
        state.maturity_level, state.current_stage, state.iteration,
        repr(state.known_mechanism), repr(state.known_problem),
        pkg["deliverable_eligible"], pkg["derived_verified_ready"],
    )


def _state(sid):
    return appmod.SESSION_STORE[sid]["state"]


def _durable_dispositions(sid):
    return [r.disposition for r in
            appmod._get_store().load_contract(sid).assertions]


def _engine_state():
    s = IdeaState(idea_id="uqtr01-unit")
    s.domain = "electronics_electrical"
    s.domain_signal = s.domain
    s.path = "N"
    s.maturity_level = 1
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, OPEN, 0))
    return s


# ---------------------------------------------------------------------------
# A + B. Baseline trap removed: each non-answer action is recorded durably,
# the automatic re-ask is suppressed, and structure/verification are untouched
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("action", NON_ANSWERS)
def test_non_answer_suppresses_automatic_reask_without_structural_change(client, action):
    sid = _start(client)
    before_body = _page(client, sid)
    asked = _question(before_body)
    assert asked and 'id="uqtr-suppressed"' not in before_body
    before = _structural(_state(sid))

    _non_answer(client, sid, action)

    body = _page(client, sid)
    # durably recorded against the canonical gap
    assert _durable_dispositions(sid)[-1] == action
    assert _state(sid).assertions[-1].gap_context == MECHANISM_COMPLETENESS
    # the automatic re-ask is suppressed: notice shown, question only inside the
    # voluntary revisit disclosure
    assert 'id="uqtr-suppressed"' in body
    assert ui_text.text("UI_UQTR_MEANING_" + action.upper(), "en") in body
    block = _revisit_block(body)
    assert block is not None and _question(block) == asked
    assert body.count('<p class="question"') == 1
    assert body.find('<p class="question"') > body.find('<details class="uqtr-revisit"')
    # no structural or verification movement, no completion
    assert _structural(_state(sid)) == before
    assert 'class="complete"' not in body
    assert not any(g.status == ACCEPTED_RISK for g in _state(sid).gaps)


def test_the_primary_journey_action_no_longer_demands_the_suppressed_question(client):
    sid = _start(client)
    assert 'href="#response"' in _page(client, sid)
    _non_answer(client, sid, "specialist_requested")
    body = _page(client, sid)
    actions = re.findall(r'data-primary-action href="([^"]+)"', body)
    assert len(actions) == 1
    assert actions[0].endswith(f"/session/{sid}/deliverable")
    assert ui_text.text("UI_UQTR_JOURNEY_NOTE", "en") in body
    cta = re.search(r'data-primary-action href="[^"]+">([^<]+)</a>', body).group(1)
    assert _html.unescape(cta) == "Review what is still needed"
    assert ui_text.text("UI_A1_REVIEW_HANDOFF", "en") not in cta


# ---------------------------------------------------------------------------
# C. Latest-active rule (engine level)
# ---------------------------------------------------------------------------

def test_latest_active_non_answer_suppresses_and_later_answer_restores():
    s = _engine_state()
    assert pl.compute_non_answer_suppression(s) is None
    s.record_interaction(action="unknown", content=NOTE,
                         gap_context=MECHANISM_COMPLETENESS)
    sup = pl.compute_non_answer_suppression(s)
    assert sup.gap_type == MECHANISM_COMPLETENESS and sup.disposition == "unknown"
    s.record_interaction(action="answered", content=ANSWER,
                         gap_context=MECHANISM_COMPLETENESS)
    assert pl.compute_non_answer_suppression(s) is None
    s.record_interaction(action="deferred", content="",
                         gap_context=MECHANISM_COMPLETENESS)
    assert pl.compute_non_answer_suppression(s).disposition == "deferred"


def test_superseded_records_never_decide():
    s = _engine_state()
    s.record_interaction(action="unknown", content=NOTE,
                         gap_context=MECHANISM_COMPLETENESS)
    s.assertions[-1].superseded_by = "rec_x"
    assert pl.compute_non_answer_suppression(s) is None
    # a superseded answer cannot lift an ACTIVE earlier suppression either
    s.record_interaction(action="specialist_requested", content="",
                         gap_context=MECHANISM_COMPLETENESS)
    s.record_interaction(action="answered", content=ANSWER,
                         gap_context=MECHANISM_COMPLETENESS)
    s.assertions[-1].superseded_by = "rec_y"
    assert pl.compute_non_answer_suppression(s).disposition == "specialist_requested"


def test_only_the_canonical_gap_and_the_six_actions_count():
    s = _engine_state()
    s.record_interaction(action="unknown", content=NOTE,
                         gap_context=PHYSICAL_FEASIBILITY)
    s.record_interaction(action="decision_context_declared",
                         content="choose a sensor", gap_context=None)
    assert pl.select_next_gap(s) == MECHANISM_COMPLETENESS
    assert pl.compute_non_answer_suppression(s) is None


def test_rule_is_pure_deterministic_and_non_mutating():
    s = _engine_state()
    s.record_interaction(action="evidence_requested", content="",
                         gap_context=MECHANISM_COMPLETENESS)
    snapshot = copy.deepcopy(s)
    a = pl.compute_non_answer_suppression(s)
    b = pl.compute_non_answer_suppression(copy.deepcopy(s))
    assert a == b and repr(s) == repr(snapshot)


def test_canonical_engine_paths_never_consult_the_rule(monkeypatch):
    def _boom(*a, **kw):
        raise AssertionError("canonical path consulted UQTR-01 serving")
    monkeypatch.setattr(pl, "compute_non_answer_suppression", _boom)
    s = _engine_state()
    s.maturity_level = 0
    pl.run_iteration(s, ANSWER)
    pl.run_iteration(s, ANSWER)
    s.record_interaction(action="unknown", content=NOTE,
                         gap_context=pl.select_next_gap(s))
    pl.advance_after_disposition(s)
    src = open(os.path.join(os.path.dirname(__file__), "..", "engine",
                            "session_reconstruction.py"), encoding="utf-8").read()
    assert "compute_non_answer_suppression" not in src


def test_no_fifth_w2b_trigger_and_serving_decision_shape_unchanged():
    assert pl.W2B_TRIGGERS == frozenset({
        pl.TRIGGER_CRITICAL_UNRESOLVED, pl.TRIGGER_LAPSED_ACCEPTANCE,
        pl.TRIGGER_MULTIPLE_ALTERNATIVES, pl.TRIGGER_COMPLETED_INTENT_SKIP})
    assert list(pl.ServingDecision.__dataclass_fields__) == [
        "served_gap", "question_override", "question_override_source",
        "primary_action", "triggers", "lapsed_served_gap",
        "accepted_risk_gaps"]
    assert pl.UQTR_SUPPRESSING_DISPOSITIONS == frozenset(NON_ANSWERS)


# ---------------------------------------------------------------------------
# D. Voluntary revisit
# ---------------------------------------------------------------------------

def test_revisit_exposes_the_existing_question_and_answer_path(client):
    sid = _start(client)
    asked = _question(_page(client, sid))
    _non_answer(client, sid, "unknown")
    body = _page(client, sid)
    block = _revisit_block(body)
    assert ui_text.text("UI_UQTR_REVISIT", "en") in block
    assert "open" not in block[:block.find(">")]          # user-controlled
    assert _question(block) == asked
    assert 'id="answer-form"' in block and 'name="answer_token"' in block
    for value in SIX:
        assert f'value="{value}"' in block
    # no second route or state owner
    rules = {r.rule for r in appmod.app.url_map.iter_rules()}
    assert not any("revisit" in r for r in rules)
    # answering through the revisit uses the canonical answered path
    served = pl.select_next_gap(_state(sid))
    _answer(client, sid)
    record = _state(sid).assertions[-1]
    assert record.disposition == "answered" and record.gap_context == served
    assert _durable_dispositions(sid)[-1] == "answered"


def test_revisit_opens_itself_when_an_answer_error_must_be_seen(client):
    sid = _start(client)
    _non_answer(client, sid, "deferred")
    appmod.SESSION_STORE[sid]["_answer_error"] = appmod.INTERACTION_NOT_SAVED_MESSAGE
    block = _revisit_block(_page(client, sid))
    assert " open" in block[:block.find(">") + 1]


# ---------------------------------------------------------------------------
# E. Reconstruction / writable resume / idle re-render
# ---------------------------------------------------------------------------

def test_cold_reconstruction_and_resume_derive_the_same_suppression(client):
    sid = _start(client)
    _non_answer(client, sid, "specialist_requested")
    live = pl.compute_non_answer_suppression(_state(sid))
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    assert pl.compute_non_answer_suppression(recon.state) == live
    # writable resume from reconstructed truth only (no transient memory)
    appmod.SESSION_STORE.clear()
    r = client.post(f"/session/{sid}/resume")
    assert r.status_code == 302
    entry = appmod.SESSION_STORE[sid]
    assert not entry.get("interaction_actions")
    assert pl.compute_non_answer_suppression(entry["state"]) == live
    body = _page(client, sid)
    assert 'id="uqtr-suppressed"' in body
    assert ui_text.text("UI_UQTR_MEANING_SPECIALIST_REQUESTED", "en") in body


def test_repeated_get_changes_nothing(client):
    sid = _start(client)
    _non_answer(client, sid, "unknown")
    state = _state(sid)
    before = (_structural(state), repr(state.assertions),
              _durable_dispositions(sid))
    bodies = {_revisit_block(_page(client, sid)).split('name="answer_token"')[0]
              for _ in range(3)}
    assert len(bodies) == 1
    assert (_structural(state), repr(state.assertions),
            _durable_dispositions(sid)) == before


# ---------------------------------------------------------------------------
# F. Accept-risk semantics unchanged
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("action", ("unknown", "deferred",
                                    "specialist_requested", "evidence_requested"))
def test_non_answers_never_become_accepted_risk(client, action):
    sid = _start(client)
    _non_answer(client, sid, action)
    body = _page(client, sid)
    assert not any(g.status == ACCEPTED_RISK for g in _state(sid).gaps)
    assert 'class="accept-risk"' not in body            # MC: never offered


def test_mechanism_still_refuses_risk_and_the_w2d_gate_is_unaffected():
    s = _engine_state()
    with pytest.raises(ValueError):
        pl.accept_gap_risk(s, MECHANISM_COMPLETENESS)
    s.gaps[0].status = CLOSED
    s.gaps.append(Gap(PHYSICAL_FEASIBILITY, OPEN, 1))
    s.record_interaction(action="answered", content=(
        "It must keep working reliably when the room temperature and humidity "
        "change, and the relay must be rated for the heater's power."),
        gap_context=PHYSICAL_FEASIBILITY)
    gate = pl.substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY)
    s.record_interaction(action="specialist_requested", content="",
                         gap_context=PHYSICAL_FEASIBILITY)
    assert pl.compute_non_answer_suppression(s).gap_type == PHYSICAL_FEASIBILITY
    # suppression is serving-only: the governed availability input is unchanged
    assert pl.substantive_attempt_recorded(s, PHYSICAL_FEASIBILITY) == gate
    assert s.get_gap(PHYSICAL_FEASIBILITY).status == OPEN


# ---------------------------------------------------------------------------
# G. Exhausted-prompt truth fix
# ---------------------------------------------------------------------------

def test_exhausted_prompt_no_longer_promises_accept_risk():
    prompt = pl._EXHAUSTED_EXIT_PROMPT
    assert "accept it explicitly as a known risk" not in prompt
    assert "only where this page shows that option" in prompt
    ar = ui_text.RVR7_SUBSTANTIVE_AR[ui_text.RVR7_EXHAUSTED_EXIT_PROMPT]
    assert "Your available options now" in prompt and "honest options" not in prompt
    assert "اقبله صراحة" not in ar
    assert "إلا إذا ظهر هذا الخيار في الصفحة" in ar
    assert "الخيارات المتاحة لك الآن" in ar
    # it is what an exhausted MECHANISM_COMPLETENESS area actually serves
    assert pl.get_display_question("electronics_electrical",
                                   MECHANISM_COMPLETENESS, 12,
                                   path="N") == prompt


def test_exhausted_mechanism_page_shows_no_accept_risk_affordance(client):
    sid = _start(client)
    _state(sid).get_gap(MECHANISM_COMPLETENESS).iterations_open = 12
    body = _page(client, sid)
    assert "only where this page shows that option" in body
    assert 'class="accept-risk"' not in body


# ---------------------------------------------------------------------------
# H. 4 primary + 2 additional presentation of the SAME six actions
# ---------------------------------------------------------------------------

def test_four_primary_and_two_additional_choices_keep_the_six_values(client):
    sid = _start(client)
    body = _page(client, sid)
    form = body[body.find('id="answer-form"'):]
    form = form[:form.find("</form>")]
    assert form.count('name="action"') == 6
    assert 'value="answered" checked' in form
    more = form.find('<details class="response-more-choices"')
    assert more > 0
    order = [re.search(rf'value="{v}"', form).start() for v in
             ("answered", "unknown", "specialist_requested", "deferred")]
    assert order == sorted(order) and order[-1] < more
    for v in ("provisional_assumption", "evidence_requested"):
        assert form.find(f'value="{v}"') > more
    assert "<fieldset" in form and "<legend" in form
    assert ui_text.text("UI_UQTR_TEXT_HINT", "en") in form
    assert form.count('id="response"') == 1
    assert "required" not in re.search(r'<textarea[^>]*>', form).group(0)


def test_answer_text_required_and_non_answer_note_optional_unchanged(client):
    sid = _start(client)
    n = len(_durable_dispositions(sid))
    client.post(f"/session/{sid}", data={
        "response": "", "action": "answered", "answer_token": _token(client, sid)})
    assert len(_durable_dispositions(sid)) == n          # empty answer: no record
    _non_answer(client, sid, "deferred", text="")
    assert _durable_dispositions(sid)[-1] == "deferred"   # empty note allowed


def test_arabic_page_carries_the_same_semantics_rtl(client):
    sid = _start(client, lang="ar")
    _non_answer(client, sid, "unknown")
    body = _page(client, sid)
    assert '<html lang="ar" dir="rtl">' in body
    for key in ("UI_UQTR_SUPPRESSED_HEADING", "UI_UQTR_MEANING_UNKNOWN",
                "UI_UQTR_SUPPRESSED_NEXT", "UI_UQTR_REVISIT",
                "UI_UQTR_MORE_CHOICES", "UI_UQTR_TEXT_HINT"):
        assert ui_text.text(key, "ar") in body, key
    form = _revisit_block(body)
    for value in SIX:
        assert f'value="{value}"' in form


def test_every_uqtr_string_is_bilingual():
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_UQTR_")]
    assert len(keys) == 12
    for k in keys:
        en, ar = ui_text.text(k, "en"), ui_text.text(k, "ar")
        assert en and ar and en != ar, k
        assert re.search("[؀-ۿ]", ar) and not re.search("[A-Za-z]", ar), k


# ---------------------------------------------------------------------------
# I. No false completion
# ---------------------------------------------------------------------------

def test_suppression_is_never_read_as_completion_or_readiness(client):
    sid = _start(client)
    _non_answer(client, sid, "evidence_requested")
    body = _page(client, sid)
    assert 'class="complete"' not in body
    assert _question(body) is not None                   # never cleared
    state = _state(sid)
    meta = assemble_deliverable(state)["_session_meta"]
    assert meta["deliverable_eligible"] is False
    assert meta["derived_verified_ready"] is False
    deliverable = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert 'class="status-snapshot"' in deliverable


# ---------------------------------------------------------------------------
# J. Determinism / idempotency
# ---------------------------------------------------------------------------

def test_duplicate_non_answer_submission_stays_one_record(client):
    sid = _start(client)
    _non_answer(client, sid, "unknown")
    n = len(_state(sid).assertions)
    d = _durable_dispositions(sid)
    _non_answer(client, sid, "unknown")                  # identical resubmission
    assert len(_state(sid).assertions) == n
    assert _durable_dispositions(sid) == d
    assert pl.compute_non_answer_suppression(_state(sid)).disposition == "unknown"


# ---------------------------------------------------------------------------
# Candidate 02 — no answer pressure after suppression (five help panels)
# ---------------------------------------------------------------------------

_PANELS = {
    "scaffolding": ("get_scaffolding_guidance", {
        "heading": "UQTRPANEL-scaffolding", "lead": "l", "prompts": ["p"], "note": "n"},
        'class="scaffolding-guidance"'),
    "clarification": ("get_clarification", {
        "label": "UQTRPANEL-clarification", "plain_language": "p",
        "information_needed": "i", "answer_shape": "a", "support_hint": "s"},
        "UQTRPANEL-clarification"),
    "responsibility": ("get_responsibility", {
        "label": "UQTRPANEL-responsibility", "guidance": "g"},
        # the gap-label box also uses class="gap-guidance"; the unique label is
        # the responsibility panel's own marker
        "UQTRPANEL-responsibility"),
    "uncertainty": ("get_uncertainty_guidance", {
        "lang": "en", "dir": "ltr", "eyebrow": "e",
        "heading": "UQTRPANEL-uncertainty", "prompts": ["p"], "note": "n"},
        'class="uncertainty-guidance"'),
    "coauthoring": ("get_answer_coauthoring_prompts", {
        "heading": "UQTRPANEL-coauthoring", "prompts": ["p"], "note": "n"},
        'class="answer-coauthoring"'),
}


def _only_panel(monkeypatch, name):
    for other, (helper, value, _) in _PANELS.items():
        fake = value if other == name else None
        monkeypatch.setattr(appmod, helper, lambda *a, _v=fake, **k: _v)


@pytest.mark.parametrize("name", sorted(_PANELS))
def test_help_panel_is_never_automatic_pressure_while_suppressed(client, monkeypatch, name):
    _only_panel(monkeypatch, name)
    marker = _PANELS[name][2]
    sid = _start(client)
    unsuppressed = _page(client, sid)
    assert marker in unsuppressed                  # normal behaviour: rendered
    assert _revisit_block(unsuppressed) is None
    _non_answer(client, sid, "deferred")
    body = _page(client, sid)
    assert 'id="uqtr-suppressed"' in body
    assert marker not in _outside_revisit(body)    # no pressure outside revisit
    assert marker in _revisit_block(body)          # still available on revisit
    assert body.count(marker) == 1                 # defined once, not duplicated


def test_unsuppressed_help_panels_keep_their_original_positions(client, monkeypatch):
    _only_panel(monkeypatch, "clarification")
    sid = _start(client)
    body = _page(client, sid)
    assert body.find('id="answer-form"') < body.find("UQTRPANEL-clarification")
    _only_panel(monkeypatch, "scaffolding")
    body = _page(client, sid)
    assert body.find('class="scaffolding-guidance"') < body.find('<p class="question"')


def test_help_capabilities_are_not_deleted():
    from web import (scaffolding_guidance, clarification_labels,
                     responsibility_labels, uncertainty_guidance,
                     answer_coauthoring_prompts)
    assert callable(scaffolding_guidance.get_scaffolding_guidance)
    assert callable(clarification_labels.get_clarification)
    assert callable(responsibility_labels.get_responsibility)
    assert callable(uncertainty_guidance.get_uncertainty_guidance)
    assert callable(answer_coauthoring_prompts.get_answer_coauthoring_prompts)
    assert uncertainty_guidance.get_uncertainty_guidance("I don't know") is not None


# ---------------------------------------------------------------------------
# Candidate 02 — W2-B × UQTR composition
# ---------------------------------------------------------------------------

def _stalled_generic_state():
    """Neutral synthetic level-1 state (the W2-B policy suite's stalled-blocker
    pattern): PHYSICAL_FEASIBILITY blocks the transition and is stalled on the
    generic-verbatim surface, so CRITICAL_UNRESOLVED genuinely fires."""
    s = IdeaState(idea_id="uqtr01-w2b")
    s.domain = "software"               # generic-verbatim surface (no Path-N artifact)
    s.domain_signal = s.domain
    s.path = "N"
    s.maturity_level = 1
    s.known_mechanism = Evidence(
        content=("(1) the operator lifts the handle and the panel rotates on the "
                 "hinge until flat. (2) the latch snaps over the rib and holds the "
                 "panel rigid. (3) the release lever frees the latch."),
        quality=REASONED, iteration=1, provenance=OWNER_STATED)
    s.gaps.append(Gap(MECHANISM_COMPLETENESS, CLOSED, 0, closed_at=2))
    s.gaps.append(Gap(PHYSICAL_FEASIBILITY, OPEN, 3,
                      iterations_open=pl.STALL_THRESHOLD))
    return s


def test_deriving_suppression_never_changes_the_w2b_decision():
    s = _stalled_generic_state()
    s.record_interaction(action="unknown", content=NOTE,
                         gap_context=PHYSICAL_FEASIBILITY)
    for elevated in (False, True):
        before = pl.compute_serving_decision(s, register_elevated=elevated)
        assert pl.compute_non_answer_suppression(s) is not None
        after = pl.compute_serving_decision(s, register_elevated=elevated)
        assert before == after


def test_a_suppressing_non_answer_leaves_w2b_trigger_membership_unchanged():
    s = _stalled_generic_state()
    assert pl.select_next_gap(s) == PHYSICAL_FEASIBILITY
    base = pl.compute_serving_decision(s)
    assert pl.TRIGGER_CRITICAL_UNRESOLVED in base.triggers
    for action in NON_ANSWERS:
        t = copy.deepcopy(s)
        t.record_interaction(action=action, content=NOTE,
                             gap_context=PHYSICAL_FEASIBILITY)
        assert pl.compute_non_answer_suppression(t).disposition == action
        assert pl.compute_serving_decision(t).triggers == base.triggers
        assert pl.W2B_TRIGGERS == frozenset(pl.W2B_QUESTION_SLOT_PRECEDENCE) | {
            pl.TRIGGER_MULTIPLE_ALTERNATIVES}


def test_legitimate_w2b_primary_action_keeps_precedence_with_one_cta(client):
    sid = _start(client)
    _non_answer(client, sid, "unknown")
    r = client.post(f"/session/{sid}/decision/declare-context", data={
        "content": "Which switching part should cut the heater power?",
        "answer_token": _token(client, sid)})
    assert r.status_code == 302
    root = _state(sid).assertions[-1].record_id
    for alt in ("mechanical relay", "solid-state relay"):
        client.post(f"/session/{sid}/decision/declare-alternative", data={
            "content": alt, "context_root": root,
            "answer_token": _token(client, sid)})
    body = _page(client, sid)
    decision = pl.compute_serving_decision(_state(sid))
    assert decision.primary_action == "decision_refine"
    assert 'id="uqtr-suppressed"' in body          # both states coexist
    actions = re.findall(r'data-primary-action href="([^"]+)"', body)
    assert actions == ["#w2b-decision-capture"]    # W2-B action-slot precedence


def test_rule_owns_no_gap_selection_and_app_has_one_serving_owner():
    import inspect
    src = inspect.getsource(pl.compute_non_answer_suppression)
    assert "select_next_gap(state)" in src
    for forbidden in ("GAP_PRIORITY", "_active_gap_priority",
                      "_open_next_gap_if_needed", "gaps.append", ".status ="):
        assert forbidden not in src, forbidden
    app_src = open(os.path.join(os.path.dirname(__file__), "..", "web", "app.py"),
                   encoding="utf-8").read()
    assert app_src.count("compute_non_answer_suppression(") == 1
    assert "uqtr_suppression = _uqtr.disposition" in app_src


# ---------------------------------------------------------------------------
# Candidate 02 — language neutrality (language does not own serving truth)
# ---------------------------------------------------------------------------

def test_en_and_ar_presentations_derive_the_same_canonical_decision(client):
    sid = _start(client)
    _non_answer(client, sid, "provisional_assumption", text="لا أعرف بعد")
    decision_en = pl.compute_non_answer_suppression(_state(sid))
    en = _page(client, sid)
    client.post("/ui-language", data={"lang": "ar"})
    ar = _page(client, sid)
    decision_ar = pl.compute_non_answer_suppression(_state(sid))
    assert decision_en == decision_ar
    assert decision_en.disposition == "provisional_assumption"
    assert ui_text.text("UI_UQTR_MEANING_PROVISIONAL_ASSUMPTION", "en") in en
    assert ui_text.text("UI_UQTR_MEANING_PROVISIONAL_ASSUMPTION", "ar") in ar
    import inspect
    src = inspect.getsource(pl.compute_non_answer_suppression)
    for token in ("lang", "ui_text", "content", "question", "text("):
        assert token not in src, token


# ---------------------------------------------------------------------------
# Candidate 02 — route-level correction reactivation (existing route only)
# ---------------------------------------------------------------------------

WEAK = "It turns the heater off."


def test_existing_correction_route_reactivates_ordinary_serving(client):
    sid = _start(client)
    _answer(client, sid, WEAK)
    target = _state(sid).assertions[-1]
    assert target.disposition == "answered"
    gap = pl.select_next_gap(_state(sid))
    assert target.gap_context == gap
    _non_answer(client, sid, "unknown")
    assert 'id="uqtr-suppressed"' in _page(client, sid)
    r = client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": target.record_id,
        "response": "It switches the heater off.",
        "answer_token": _token(client, sid)})
    assert r.status_code == 302
    state = _state(sid)
    assert pl.select_next_gap(state) == gap
    latest = [r for r in state.assertions if r.gap_context == gap
              and r.superseded_by is None][-1]
    assert latest.disposition == "answered" and target.record_id in latest.supersedes
    assert pl.compute_non_answer_suppression(state) is None
    assert 'id="uqtr-suppressed"' not in _page(client, sid)


# ---------------------------------------------------------------------------
# Candidate 02 — no runtime model / network use anywhere on the UQTR path
# ---------------------------------------------------------------------------

def test_no_model_or_network_call_on_the_uqtr_path(client, monkeypatch):
    import socket
    import engine.ai_advisor as ai
    def _no(*a, **k):
        raise AssertionError("network or model call attempted")
    monkeypatch.setattr(socket.socket, "connect", _no)
    monkeypatch.setattr(socket, "create_connection", _no)
    for name in dir(ai):
        if name.startswith("get_") and callable(getattr(ai, name)):
            monkeypatch.setattr(ai, name, _no)
    sid = _start(client)
    _non_answer(client, sid, "specialist_requested")
    assert 'id="uqtr-suppressed"' in _page(client, sid)
    reconstruct_readonly_state(appmod._get_store(), sid)
    appmod.SESSION_STORE.clear()
    assert client.post(f"/session/{sid}/resume").status_code == 302
    assert 'id="uqtr-suppressed"' in _page(client, sid)


# ---------------------------------------------------------------------------
# Browser (real Chromium): collapsed revisit, native disclosure, RTL
# ---------------------------------------------------------------------------

from tests.test_draft_l2_local_continuity import server, _browser, _start as _browser_start  # noqa: E402,F401


def test_browser_suppression_and_voluntary_revisit(server, _browser):
    ctx = _browser.new_context()
    page = ctx.new_page()
    try:
        sid = _browser_start(page, server)
        question = page.locator("p.question").inner_text()
        assert page.locator("p.question").is_visible()
        page.locator('input[name="action"][value="unknown"]').check()
        page.locator('#answer-form button[type="submit"]').click()
        page.wait_for_load_state()
        assert page.locator("#uqtr-suppressed").is_visible()
        assert not page.locator("p.question").is_visible()       # collapsed
        page.locator("#uqtr-revisit > summary").click()
        assert page.locator("p.question").is_visible()
        assert page.locator("p.question").inner_text() == question
        more = page.locator("details.response-more-choices")
        assert not more.locator('input[value="evidence_requested"]').is_visible()
        more.locator("summary").click()
        assert more.locator('input[value="evidence_requested"]').is_visible()
        assert page.locator("[data-primary-action]").count() == 1
    finally:
        ctx.close()


_HELP = (".scaffolding-guidance, .gap-guidance, .uncertainty-guidance, "
         ".answer-coauthoring")

# Visible answer-help panels OUTSIDE the voluntary revisit. The canonical
# gap-label box (also class "gap-guidance") precedes the suppression notice and
# is gap context, not answer help, so only elements after the notice count.
_VISIBLE_HELP_OUTSIDE_REVISIT = """sel => {
  const notice = document.getElementById('uqtr-suppressed');
  const revisit = document.getElementById('uqtr-revisit');
  return [...document.querySelectorAll(sel)].filter(e =>
    (notice.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING)
    && !revisit.contains(e) && e.checkVisibility()).map(e => e.outerHTML);
}"""


def _visible_help_outside_revisit(page):
    return page.evaluate(_VISIBLE_HELP_OUTSIDE_REVISIT, _HELP)


def test_browser_help_absent_outside_revisit_and_keyboard_disclosure(server, _browser):
    ctx = _browser.new_context()
    page = ctx.new_page()
    try:
        _browser_start(page, server)
        page.locator("#response").fill("I don't know how this part works yet.")
        page.locator('input[name="action"][value="unknown"]').check()
        page.locator('#answer-form button[type="submit"]').click()
        page.wait_for_load_state()
        assert page.locator("#uqtr-suppressed").is_visible()
        assert _visible_help_outside_revisit(page) == []
        # four primary choices live inside the revisit; the two extra ones stay
        # collapsed until asked for
        summary = page.locator("#uqtr-revisit > summary")
        summary.focus()
        page.keyboard.press("Enter")
        assert page.locator("#uqtr-revisit").get_attribute("open") is not None
        # the help is not deleted: it is available inside the voluntary revisit
        assert page.locator("#uqtr-revisit .uncertainty-guidance").is_visible()
        for v in ("answered", "unknown", "specialist_requested", "deferred"):
            assert page.locator(f'input[name="action"][value="{v}"]').is_visible()
        for v in ("provisional_assumption", "evidence_requested"):
            assert not page.locator(f'input[name="action"][value="{v}"]').is_visible()
        assert page.locator("[data-primary-action]").count() == 1
        assert page.locator("[data-primary-action]").inner_text().strip() == \
            "Review what is still needed"
    finally:
        ctx.close()


def test_browser_arabic_suppressed_page_is_rtl(server, _browser):
    ctx = _browser.new_context()
    page = ctx.new_page()
    try:
        sid = _browser_start(page, server)
        page.locator("form button[lang=ar]").first.click()
        page.wait_for_load_state()
        page.locator('input[name="action"][value="specialist_requested"]').check()
        page.locator('#answer-form button[type="submit"]').click()
        page.wait_for_load_state()
        assert page.locator("html").get_attribute("dir") == "rtl"
        notice = page.locator("#uqtr-suppressed")
        assert notice.is_visible()
        assert notice.evaluate("e => getComputedStyle(e).direction") == "rtl"
        assert ui_text.text("UI_UQTR_MEANING_SPECIALIST_REQUESTED", "ar") in notice.inner_text()
        assert _visible_help_outside_revisit(page) == []
        summary = page.locator("#uqtr-revisit > summary")
        assert summary.inner_text().strip() == ui_text.text("UI_UQTR_REVISIT", "ar")
        summary.click()
        page.locator("details.response-more-choices > summary").click()
        assert page.locator('input[value="evidence_requested"]').is_visible()
        cta = page.locator("[data-primary-action]")
        assert cta.count() == 1
        assert cta.inner_text().strip() == ui_text.text("UI_UQTR_CTA", "ar")
        assert pl.compute_non_answer_suppression(
            appmod.SESSION_STORE[sid]["state"]).disposition == "specialist_requested"
    finally:
        ctx.close()
