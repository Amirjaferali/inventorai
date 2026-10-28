"""CURRENT-QUESTION-GAP-CONTEXT-01 — the served question's EXISTING gap identity
made visible (presentation only).

Beside the rendered question the session page states "This question is about:
<friendly gap name>", and the Design Understanding picture marks the ONE gap item
whose identity is that gap, both ONLY while the Compass presents answering the
current question as the one primary action. The identity is ``gap_type`` from
the same resolved question context that produced the question (``_qctx``); the
condition is the Compass's own answer branch (a template flag set inside it, no
second predicate). Nothing is selected, derived, ranked or written; the Compass,
question serving, progression and readiness are unchanged. Synthetic data only.
"""
import html as _html
import re

import pytest

import web.app as appmod
from web.ui_text import text
from web.gap_labels import GAP_DISPLAY_NAMES, GAP_DISPLAY_NAMES_AR
from tests.test_safe_question_routing_pf_q2 import (  # noqa: F401  (fixture)
    client, MECH, PF_STRONG, BA_1, BA_2, _start, _answer, _live,
)
from tests.test_safe_question_routing_pf_q2_weak_recovery import _to_stuck, _token, WEAK

LABEL_RE = re.compile(r'<p class="question-gap" data-question-gap[^>]*>.*?</p>', re.S)
MARKER_RE = re.compile(r'<span data-du-current-question[^>]*>.*?</span>', re.S)
GAP_ITEM_RE = re.compile(r'<li data-du-item="gap"[^>]*>.*?</li>', re.S)
QUESTION_RE = re.compile(r'<p class="question"[^>]*>(.*?)</p>', re.S)


def _raw(c, sid):
    r = c.get(f"/session/{sid}")
    assert r.status_code == 200, r.status_code
    return r.get_data(as_text=True)


def _visible(fragment):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def _primary(page):
    found = re.findall(r'<(?:a|button) class="journey-primary" data-primary-action[^>]*>', page)
    assert len(found) == 1, found
    return found[0]


def _label(page):
    found = LABEL_RE.findall(page)
    assert len(found) <= 1, found
    return found[0] if found else None


def _markers(page):
    return MARKER_RE.findall(page)


def _served_gap(sid):
    """The gap identity the page's own resolver produces for this session."""
    entry = appmod.SESSION_STORE[sid]
    return appmod._resolve_question_context(entry["state"], entry["last_result"]).gap_type


def _assert_absent(page):
    assert "data-question-gap" not in page
    assert "data-du-current-question" not in page
    assert text("UI_CQG_LABEL", "en") not in page and text("UI_CQG_MARKER", "en") not in page


# ---------------------------------------------------------------------------
# 1. identity: the label and the marker follow the resolved gap, not the text
# ---------------------------------------------------------------------------

def test_01_label_names_the_served_gap_by_its_friendly_name(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    page = _raw(client, sid)
    assert 'href="#response"' in _primary(page)
    gap = _served_gap(sid)
    assert gap == "MECHANISM_COMPLETENESS"
    label = _label(page)
    assert label is not None
    assert _visible(label) == f"{text('UI_CQG_LABEL', 'en')} {GAP_DISPLAY_NAMES[gap]}"
    # placed beside the rendered question: after the question element, before the form
    q = QUESTION_RE.search(page)
    assert q and page.index(label) > q.end()
    assert page.index(label) < page.index('id="answer-form"')
    # the same identity is what the page already signs into the answer form
    assert re.search(r'name="answer_target" value="[^"]+"', page)


def test_02_label_follows_the_resolved_identity_not_the_question_text(client, monkeypatch):
    sid = _start(client)
    _answer(client, sid, MECH)
    original = appmod._resolve_question_context

    def redirected(state, last_result):
        ctx = original(state, last_result)
        assert ctx.gap_type == "MECHANISM_COMPLETENESS" and ctx.question
        return appmod._QuestionContext(
            "BOUNDARY_AMBIGUITY", ctx.iterations_open, ctx.question, ctx.identity,
            ctx.served, ctx.w2b_cues, ctx.w2b_risk_note, ctx.w2b_primary_action,
            ctx.serving_basis)

    monkeypatch.setattr(appmod, "_resolve_question_context", redirected)
    page = _raw(client, sid)
    # same question text, different resolved identity -> the label changes with the identity
    assert _visible(_label(page)) == f"{text('UI_CQG_LABEL', 'en')} {GAP_DISPLAY_NAMES['BOUNDARY_AMBIGUITY']}"
    # and the marker appears on NO item, because no picture gap item carries that identity
    assert _markers(page) == []
    assert len(GAP_ITEM_RE.findall(page)) == 1


def test_03_marker_sits_on_the_exact_matching_item_and_other_gaps_stay_unmarked(client):
    sid = _start(client)
    for value in (MECH, MECH, WEAK):
        _answer(client, sid, value)
    state = _live(sid)
    unresolved = [g.gap_type for g in state.gaps if g.status in ("OPEN", "PARTIAL")]
    assert len(unresolved) >= 2, unresolved
    page = _raw(client, sid)
    assert 'href="#response"' in _primary(page)
    gap = _served_gap(sid)
    assert gap in unresolved
    items = GAP_ITEM_RE.findall(page)
    assert len(items) == len(unresolved)
    marked = [i for i in items if "data-du-current-question" in i]
    assert len(marked) == 1 and len(_markers(page)) == 1
    assert _visible(marked[0]).startswith(GAP_DISPLAY_NAMES[gap])
    assert text("UI_CQG_MARKER", "en") in _visible(marked[0])
    for other in items:
        if other is not marked[0]:
            assert "data-du-current-question" not in other
            assert not _visible(other).startswith(GAP_DISPLAY_NAMES[gap])
    assert _visible(_label(page)).endswith(GAP_DISPLAY_NAMES[gap])


def test_03b_served_gap_without_a_picture_item_gets_the_label_and_no_marker(client):
    """After the inventor records the current question as not known yet, the
    paused gap stays in the picture and the next question is served for a gap
    that has no record yet: the label names that served gap, the marker marks
    nothing (no picture item carries that identity) and no item is invented."""
    sid = _start(client)
    _answer(client, sid, MECH)
    client.post(f"/session/{sid}", data={
        "action": "unknown", "answer_token": _token(client, sid),
        "response": "I do not know the latch load yet."})
    page = _raw(client, sid)
    assert 'href="#response"' in _primary(page) and "paused-question-item" in page
    gap = _served_gap(sid)
    assert gap not in [g.gap_type for g in _live(sid).gaps]
    assert _visible(_label(page)) == f"{text('UI_CQG_LABEL', 'en')} {GAP_DISPLAY_NAMES[gap]}"
    assert _markers(page) == []
    items = GAP_ITEM_RE.findall(page)
    assert len(items) == 1 and not _visible(items[0]).startswith(GAP_DISPLAY_NAMES[gap])


# ---------------------------------------------------------------------------
# 2. what the label and the marker are NOT
# ---------------------------------------------------------------------------

def test_04_no_control_no_raw_id_and_one_primary_action(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    page = _raw(client, sid)
    for fragment in [_label(page)] + _markers(page):
        for forbidden in ("<a ", "<button", "<form", "<input", "href="):
            assert forbidden not in fragment, fragment
        for raw in GAP_DISPLAY_NAMES:
            assert raw not in fragment
        assert not re.search(r"\brec_\d|\bq[0-9]+\b|[A-Z]{3,}_[A-Z_]{3,}", _visible(fragment)), fragment
    assert page.count("data-primary-action") == 1
    # the Compass "What to do now" row carries neither the label nor the marker
    do = page[page.index('data-pc-row="do"'):page.index("</section>", page.index('data-pc-row="do"'))]
    assert "data-question-gap" not in do and "data-du-current-question" not in do


def test_05_get_render_changes_no_state(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    state = _live(sid)
    before = (len(state.assertions), [(g.gap_type, g.status) for g in state.gaps],
              state.maturity_level, list(getattr(state, "need_routing", []) or []))
    for _ in range(2):
        assert _label(_raw(client, sid)) is not None
    state = _live(sid)
    after = (len(state.assertions), [(g.gap_type, g.status) for g in state.gaps],
             state.maturity_level, list(getattr(state, "need_routing", []) or []))
    assert before == after


# ---------------------------------------------------------------------------
# 3. every displacing primary action shows neither label nor marker
# ---------------------------------------------------------------------------

def test_06_uqtr_suppression_shows_nothing_although_the_question_still_renders(client):
    from tests.test_uqtr01_core_serving import _start as _uqtr_start, _non_answer
    sid = _uqtr_start(client)
    before = _raw(client, sid)
    assert 'href="#response"' in _primary(before) and _label(before) is not None
    _non_answer(client, sid, "provisional_assumption")
    page = _raw(client, sid)
    assert 'id="uqtr-suppressed"' in page and QUESTION_RE.search(page)
    primary = _primary(page)
    assert f"/session/{sid}/deliverable" in primary
    assert _html.escape(text("UI_UQTR_JOURNEY_NOTE", "en")) in page
    _assert_absent(page)


def test_07_decision_refine_primary_shows_nothing(client):
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
    assert QUESTION_RE.search(page)
    _assert_absent(page)


def test_08_routed_recovery_primary_shows_nothing(client):
    sid = _start(client)
    _to_stuck(client, sid)
    page = _raw(client, sid)
    assert 'href="#routed-recovery"' in _primary(page)
    _assert_absent(page)


def test_09_criticality_review_primary_shows_nothing():
    from tests.test_structured_criticality import _fresh_completed_journey
    client, sid, _state = _fresh_completed_journey()
    try:
        page = _raw(client, sid)
        assert 'href="#criticality-review"' in _primary(page)
        _assert_absent(page)
    finally:
        appmod.SESSION_STORE.pop(sid, None)


def test_10_integrated_guidance_primary_shows_nothing(client):
    from tests.test_integrated_journey_guidance import _finished_focus
    sid = _finished_focus(client)
    page = _raw(client, sid)
    assert 'data-ijg-action="part_questions"' in _primary(page)
    _assert_absent(page)


def test_11_experiment_planning_primary_shows_nothing(client):
    sid = _start(client)
    for value in (MECH, MECH, PF_STRONG, BA_1, BA_2):
        _answer(client, sid, value)
    page = _raw(client, sid)
    assert "data-epg-action" in _primary(page)
    _assert_absent(page)


def test_12_cold_resume_shows_nothing(client):
    sid = _start(client)
    _answer(client, sid, MECH)
    appmod.SESSION_STORE.pop(sid)
    page = _raw(client, sid)
    primary = _primary(page)
    assert 'id="resume-project"' in primary or "deliverable" in primary
    _assert_absent(page)


# ---------------------------------------------------------------------------
# 4. binding: one flag, set only inside the existing answer branch
# ---------------------------------------------------------------------------

def test_13_label_and_marker_are_bound_to_the_compass_answer_branch_only():
    with open("web/templates/session.html", encoding="utf-8") as fh:
        tpl = fh.read()
    do = tpl[tpl.index('data-pc-row="do"'):tpl.index("</section>", tpl.index('data-pc-row="do"'))]
    assert tpl.count("{% set current_question_primary = true %}") == 1
    assert do.count("{% set current_question_primary = false %}") == 1
    answer = do.index("{% elif (state.maturity_level < 2 or open_gaps) and question %}")
    nxt = do.index("{% elif routed_recovery %}", answer)
    assert answer < do.index("{% set current_question_primary = true %}") < nxt
    assert do.index("{% set current_question_primary = false %}") < do.index("{% if reconstructed_review")
    assert "{% if question and current_question_primary and gap_type %}" in tpl
    assert "{%- if current_question_primary and question and i.reference == gap_type %}" in tpl
    # the identity the label shows is the page's existing gap_type kwarg (from _qctx)
    assert "{{ gap_type|gap_display }}" in tpl
    with open("web/app.py", encoding="utf-8") as fh:
        app_src = fh.read()
    assert "gap_type = _qctx.gap_type" in app_src and "gap_type=gap_type," in app_src


# ---------------------------------------------------------------------------
# 5. EN / AR
# ---------------------------------------------------------------------------

def test_14_copy_has_both_languages_and_no_overclaim():
    for key in ("UI_CQG_LABEL", "UI_CQG_MARKER"):
        for lang in ("en", "ar"):
            assert text(key, lang).strip()
        assert text(key, "en") != text(key, "ar")
    for word in ("eliminated", "approved", "validated", "certified", "verified", "complete"):
        assert word not in (text("UI_CQG_LABEL", "en") + text("UI_CQG_MARKER", "en")).lower()


def test_15_arabic_label_and_marker_follow_the_ui_language(client):
    sid = _start(client, lang="ar")
    _answer(client, sid, MECH)
    page = _raw(client, sid)
    gap = _served_gap(sid)
    assert _visible(_label(page)) == f"{text('UI_CQG_LABEL', 'ar')} {GAP_DISPLAY_NAMES_AR[gap]}"
    markers = _markers(page)
    assert len(markers) == 1 and text("UI_CQG_MARKER", "ar") in _visible(markers[0])
    assert text("UI_CQG_LABEL", "en") not in page and text("UI_CQG_MARKER", "en") not in page
    assert 'dir="rtl"' in page[:400]
