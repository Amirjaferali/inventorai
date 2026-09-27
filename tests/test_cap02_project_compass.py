"""CAP-02 Slice 1 — the Project Compass (simplified one-step journey).

The existing top-of-session Project Orientation becomes ONE compact compass of
four plain rows — recorded so far / still unresolved / why it matters now /
what to do now — and the former standalone Next Development Step callout is
folded into it. Truth ownership is unchanged:

  * recorded so far   — the active answered ledger (disposition "answered",
                        not superseded), the same set as `active_answers`;
  * still unresolved  — canonical Requirement Landscape rows, counted per
                        category and never summed;
  * why it matters    — derive_next_development_step, reused unchanged;
  * what to do now    — the existing primary-action branches, unchanged: the
                        ONE primary action.

Session only; no report / PDF change; no question, form, POST, writer,
persistence or state change. Synthetic data only.
"""
import html
import re

import pytest

import web.app as appmod
from web.ui_text import text
from tests.test_deliverable_hygiene import PROHIBITED_TOKENS
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, PF_STRONG, BA_1, BA_2, _start, _answer, _body, _live,
    _accept_pf_via_route,
)
from tests.test_safe_question_routing_pf_q2_weak_recovery import (
    _to_stuck, _weak_pf_record, _correct, _token,
)


def _raw(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _compass(page):
    m = re.search(r'<section class="project-orientation project-compass" id="project-compass".*?</section>',
                  page, re.S)
    assert m, "the Project Compass must render"
    return m.group(0)


def _row(compass, name):
    m = re.search(r'<div class="pc-row [^"]*" data-pc-row="%s">(.*?)(?=<div class="pc-row |</section>)'
                  % name, compass, re.S)
    assert m, name
    return m.group(1)


def _visible(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def _categories(compass):
    return dict((k, int(v)) for k, v in re.findall(
        r'<li data-pc-category="([a-z_]+)">[^<]*<span class="pc-count">(\d+)</span>', compass))


def _primary(page):
    found = re.findall(r'<(?:a|button) class="journey-primary" data-primary-action[^>]*>', page)
    assert len(found) == 1, found
    return found[0]


FORBIDDEN = ("complete", "validated", "verified", "ready", "feasible", "safe ",
             "severity", "priority", "ranked", "score", "recommend")


def _no_overclaim(compass, lang="en"):
    """The Compass's OWN copy (recorded / unresolved rows and chrome) claims
    nothing; the next-step text and the primary-action notes are existing owners'
    wording, reused verbatim, and are checked by their own suites."""
    own = _row(compass, "recorded") + _row(compass, "unresolved")
    visible = _visible(own).lower()
    for word in FORBIDDEN:
        assert word not in visible, word
    for token in PROHIBITED_TOKENS:
        assert token not in compass, token
    assert not re.search(r"\brec_\d+\b", compass)


# ---------------------------------------------------------------------------
# A / C / E / H / J / P / Q / U — a fresh Mechanical project
# ---------------------------------------------------------------------------

def test_a_fresh_project_compass_is_truthful_and_has_one_primary_action(client):
    sid = _start(client)
    page = _raw(client, sid)
    compass = _compass(page)
    # four rows in order, then nothing else competing
    assert re.findall(r'data-pc-row="([a-z]+)"', compass) == [
        "recorded", "unresolved", "why", "do"]
    recorded = _row(compass, "recorded")
    assert 'data-pc-answers="0"' in recorded
    assert html.escape(text("UI_PC_ANSWERS_NONE", "en")) in recorded
    # C / E: the open gap and the pending specialist route, per category
    assert _categories(compass) == {"gaps": 1, "specialist": 1}
    assert html.escape(text("UI_PC_NOT_SUMMED", "en")) in compass
    # H: the existing next development step, as context
    step = appmod.derive_next_development_step(_live(sid))
    why = _row(compass, "why")
    assert 'id="next-development-step"' in why
    assert html.escape(step.title) in why and html.escape(step.why_it_matters) in why
    assert html.escape(step.next_action) in why
    assert "<a " not in why and "<button" not in why and "<form" not in why
    # J / U: the existing question action is the ONE primary action, in "do"
    assert 'href="#response"' in _primary(page)
    assert "data-primary-action" in _row(compass, "do")
    assert page.count("data-primary-action") == 1
    # U: no second "do next" label anywhere on the page
    assert html.escape(text("UI_B_SESSION_002", "en")) not in page
    assert html.escape(text("UI_A1_NEXT_ACTION", "en")) not in page
    assert page.count('id="next-development-step"') == 1
    assert 'class="next-step-callout" id="next-development-step" style=' not in page
    # P: the gap-pack link resolves on the same page
    assert 'href="#gap-action-packs"' in compass and 'id="gap-action-packs"' in page
    # Q: works before any decision; nothing of the Decision Room inside
    for marker in ("w2b-decision-capture", "decision-action-summary",
                   "decision-project-context", "dt-history"):
        assert marker not in compass, marker
    _no_overclaim(compass)


# ---------------------------------------------------------------------------
# B — only CURRENT active answered records count
# ---------------------------------------------------------------------------

def test_b_recorded_so_far_counts_only_current_answers(client):
    sid = _start(client)
    _to_stuck(client, sid)
    state = _live(sid)
    expected = sum(1 for r in state.assertions
                   if r.disposition == "answered" and r.superseded_by is None)
    assert f'data-pc-answers="{expected}"' in _compass(_raw(client, sid))
    weak = _weak_pf_record(state)
    assert _correct(client, sid, weak.record_id, PF_STRONG).status_code == 302
    state = _live(sid)
    assert any(r.superseded_by for r in state.assertions)       # a superseded one
    after = sum(1 for r in state.assertions
                if r.disposition == "answered" and r.superseded_by is None)
    assert after == expected                  # replaced, not added
    assert f'data-pc-answers="{after}"' in _compass(_raw(client, sid))


# ---------------------------------------------------------------------------
# D / F — a recorded unknown and several categories, never summed
# ---------------------------------------------------------------------------

def test_d_f_recorded_unknown_is_its_own_category_and_nothing_is_summed(client):
    sid = _start(client)
    raw = _raw(client, sid)
    token = re.search(r'name="answer_token" value="([^"]*)"', raw).group(1)
    data = {"response": "I do not know the latch force yet.", "action": "unknown",
            "answer_token": token}
    target = re.search(r'name="answer_target" value="([^"]*)"', raw)
    if target:
        data["answer_target"] = html.unescape(target.group(1))
    assert client.post(f"/session/{sid}", data=data).status_code == 302
    state = _live(sid)
    assert any(r.disposition == "unknown" and r.superseded_by is None
               for r in state.assertions)
    compass = _compass(_raw(client, sid))
    cats = _categories(compass)
    assert cats.get("unknowns") == 1, cats
    assert len(cats) >= 2
    assert html.escape(text("UI_PC_NOT_SUMMED", "en")) in compass
    # an unknown is not a recorded answer
    assert 'data-pc-answers="0"' in compass
    # no composite total anywhere in the unresolved row
    unresolved = _row(compass, "unresolved")
    assert unresolved.count('class="pc-count"') == len(cats)   # one per category
    assert "total" not in _visible(unresolved).lower()
    _no_overclaim(compass)


def test_d_unknowns_noted_inside_an_answer_are_their_own_category(client):
    sid = _start(client)
    _answer(client, sid, "The hinge pivots on a steel pin; I don't know the "
                         "spring rate yet.")
    state = _live(sid)
    assert len(state.acknowledged_unknowns) == 1
    assert not any(r.disposition == "unknown" for r in state.assertions)
    cats = _categories(_compass(_raw(client, sid)))
    assert cats.get("noted_unknowns") == 1 and "unknowns" not in cats, cats
    assert 'id="gap-action-packs"' in _raw(client, sid)


def test_e_pending_evidence_and_specialist_come_from_the_landscape(client):
    sid = _start(client)
    raw = _raw(client, sid)
    token = re.search(r'name="answer_token" value="([^"]*)"', raw).group(1)
    data = {"response": "A bench load test is needed.", "action": "evidence_requested",
            "answer_token": token}
    target = re.search(r'name="answer_target" value="([^"]*)"', raw)
    if target:
        data["answer_target"] = html.unescape(target.group(1))
    assert client.post(f"/session/{sid}", data=data).status_code == 302
    state = _live(sid)
    from engine.requirement_landscape import derive_requirement_landscape
    kinds = [q.primary_anchor.anchor_kind
             for q in derive_requirement_landscape(state).requirements]
    cats = _categories(_compass(_raw(client, sid)))
    assert cats.get("evidence", 0) == kinds.count("pending_evidence") >= 1
    assert cats.get("specialist", 0) == kinds.count("pending_specialist")
    assert cats.get("gaps", 0) == kinds.count("gap")


# ---------------------------------------------------------------------------
# G / I / T — empty, absent and unavailable stay distinct
# ---------------------------------------------------------------------------

def test_g_no_unresolved_category_is_neutral_not_completion():
    from engine.idea_state import IdeaState
    state = IdeaState(idea_id="cap02-empty")
    state.domain = "mechanical"
    ctx = appmod._project_compass_context(state)
    assert ctx == {"status": "available", "answers": 0, "unresolved": []}
    for lang in ("en", "ar"):
        none = text("UI_PC_UNRESOLVED_NONE", lang)
        assert none and (lang == "ar" or "does not mean" in none)
    for word in ("complete ", "validated", "ready"):
        assert word not in text("UI_PC_UNRESOLVED_NONE", "en").lower()


def test_i_no_next_development_step_shows_no_invented_reason(client, monkeypatch):
    sid = _start(client)
    monkeypatch.setattr(appmod, "derive_next_development_step", lambda state: None)
    page = _raw(client, sid)
    why = _row(_compass(page), "why")
    assert html.escape(text("UI_PC_WHY_NONE", "en")) in why
    assert 'id="next-development-step"' not in page
    assert page.count("data-primary-action") == 1


def test_t_derivation_failure_reads_unavailable_never_zero(client, monkeypatch):
    sid = _start(client)

    def boom(state):
        raise RuntimeError("landscape exploded")
    monkeypatch.setattr(appmod, "derive_requirement_landscape", boom)
    page = _raw(client, sid)
    compass = _compass(page)
    assert "data-pc-answers" not in compass and "data-pc-none" not in compass
    assert compass.count("data-pc-unavailable") == 2          # recorded + unresolved
    assert "exploded" not in page
    assert page.count("data-primary-action") == 1


def test_t_cold_read_only_view_is_unavailable(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    appmod.SESSION_STORE.pop(sid)
    page = _raw(client, sid)
    compass = _compass(page)
    assert "data-pc-answers" not in compass and "data-pc-none" not in compass
    assert "data-pc-unavailable" in compass
    assert page.count("data-primary-action") == 1


# ---------------------------------------------------------------------------
# K / L / M / N / O — the primary action keeps every existing branch
# ---------------------------------------------------------------------------

# The primary-action branches, in their exact existing order, with their
# primary targets. The Compass moved this block verbatim; the order and the
# conditions are the behaviour.
_BRANCHES = (
    ("{% if reconstructed_review and reconstructed_review.resume_eligible %}",
     'id="resume-project"'),
    ("{% elif not state.domain %}", "UI_A1_REVIEW_HANDOFF"),
    ("{% elif w2b_primary_action == 'decision_refine' and "
     "(state.maturity_level < 2 or open_gaps) %}", 'href="#w2b-decision-capture"'),
    ("{% elif uqtr_suppression and (state.maturity_level < 2 or open_gaps) and "
     "question %}", "UI_UQTR_CTA"),
    ("{% elif (state.maturity_level < 2 or open_gaps) and question %}",
     'href="#response"'),
    ("{% elif routed_recovery %}", 'href="#routed-recovery"'),
    ("{% elif criticality_step %}", 'href="#criticality-review"'),
    ("{% else %}", "UI_A1_REVIEW_HANDOFF"),
)


def test_m_primary_action_branches_are_unchanged_and_live_in_the_compass():
    with open("web/templates/session.html", encoding="utf-8") as fh:
        tpl = fh.read()
    do = tpl[tpl.index('data-pc-row="do"'):tpl.index("</section>", tpl.index('data-pc-row="do"'))]
    pos = 0
    for condition, target in _BRANCHES:
        i = do.index(condition, pos)
        j = do.index(target, i)
        nxt = min([do.index(c, i + 1) for c, _ in _BRANCHES if c in do[i + 1:]] or [len(do)])
        assert j < nxt, condition
        pos = i + 1
    assert do.count("data-primary-action") == len(_BRANCHES)
    assert tpl.count("data-primary-action") == len(_BRANCHES)


def test_k_decision_refine_stays_the_primary_action(client):
    sid = _start(client)
    client.post(f"/session/{sid}/decision/declare-context", data={
        "content": "Which latch design should hold the ramp?",
        "answer_token": _token(client, sid)})
    ctx_root = _live(sid).assertions[-1].record_id
    for alt in ("toggle latch", "spring pin"):
        client.post(f"/session/{sid}/decision/declare-alternative", data={
            "content": alt, "context_root": ctx_root,
            "answer_token": _token(client, sid)})
    page = _raw(client, sid)
    assert 'href="#w2b-decision-capture"' in _primary(page)
    compass = _compass(page)
    # R: decision records are never counted as answers, nor duplicated here
    assert 'data-pc-answers="0"' in compass
    for marker in ("dt-history", "decision-action-summary", "decision-project-context"):
        assert marker not in compass
    assert 'id="decision-action-summary"' in page         # the room is still there


def test_l_routed_recovery_stays_the_primary_action(client):
    sid = _start(client)
    _to_stuck(client, sid)
    page = _raw(client, sid)
    assert 'href="#routed-recovery"' in _primary(page)
    assert "data-primary-action" in _row(_compass(page), "do")


def test_n_handoff_stays_the_primary_action(client):
    sid = _start(client)
    for value in (MECH, MECH, PF_STRONG, BA_1, BA_2):
        _answer(client, sid, value)
    page = _raw(client, sid)
    assert f'href="/session/{sid}/deliverable"' in _primary(page)
    _no_overclaim(_compass(page))


def test_o_cold_resume_stays_the_primary_action(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    appmod.SESSION_STORE.pop(sid)
    page = _raw(client, sid)
    primary = _primary(page)
    assert 'id="resume-project"' in primary or "deliverable" in primary


# ---------------------------------------------------------------------------
# S — a GET render mutates nothing
# ---------------------------------------------------------------------------

def test_s_get_render_changes_no_state(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    state = _live(sid)
    before = (len(state.assertions), [(g.gap_type, g.status) for g in state.gaps],
              state.maturity_level, list(getattr(state, "need_routing", []) or []))
    for _ in range(2):
        _raw(client, sid)
    state = _live(sid)
    after = (len(state.assertions), [(g.gap_type, g.status) for g in state.gaps],
             state.maturity_level, list(getattr(state, "need_routing", []) or []))
    assert before == after


# ---------------------------------------------------------------------------
# V / W — EN and AR
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("lang", ["en", "ar"])
def test_v_w_compass_chrome_follows_the_ui_language(client, lang):
    sid = _start(client, lang=lang)
    _answer(client, sid, MECH)
    page = _raw(client, sid)
    compass = _compass(page)
    for key in ("UI_PC_HEADING", "UI_PC_RECORDED", "UI_PC_UNRESOLVED", "UI_PC_WHY",
                "UI_PC_DO_NOW", "UI_PC_ANSWERS_N", "UI_PC_CAT_GAPS"):
        assert html.escape(text(key, lang)) in compass, key
    other = "ar" if lang == "en" else "en"
    for key in ("UI_PC_HEADING", "UI_PC_RECORDED", "UI_PC_DO_NOW"):
        assert html.escape(text(key, other)) not in compass, key
    assert 'data-pc-answers="1"' in compass
    _no_overclaim(compass, lang)


def test_report_and_pdf_gain_no_compass(client):
    sid = _start(client)
    report = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert "project-compass" not in report and "data-pc-row" not in report
    assert "UI_PC_" not in report


def test_new_strings_have_both_languages():
    from web.ui_text import UI_STRINGS
    keys = [k for k in UI_STRINGS if k.startswith("UI_PC_")]
    assert len(keys) == 21
    for k in keys:
        assert UI_STRINGS[k]["en"].strip() and UI_STRINGS[k]["ar"].strip(), k
