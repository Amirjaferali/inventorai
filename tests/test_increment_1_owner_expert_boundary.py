"""Increment 1 — Owner-Expert Question Boundary (bounded question-layer fix).

These tests verify the bounded, question-layer correction only:
  * the general /start non-specialist flow uses the committed Path N provider;
  * the existing named ILT routes keep their current default behavior;
  * the early non-specialist runtime questions contain no engineering-gated terms;
  * a deterministic plain-language stall reframe replaces verbatim repetition of
    the final Path N variant, without resolving the gap, changing maturity, or
    starting a conversational / multi-question loop;
  * the six Increment 1A owner actions are unchanged.

No engine state model, provenance, transcript, deliverable, domain pack, or
governance artifact is touched (those remain reserved for Increment 2).
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from engine.progression_loop import get_display_question, _STALL_REFRAME
from engine.path_n_questions import get_path_n_question
from engine.idea_state import (
    IdeaState, Gap, OPEN,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)
from web.app import (
    app, SESSION_STORE, INTERACTION_ACTIONS, ACTION_ANSWERED, _NON_ANSWER_ACK,
)
from tests.test_non_specialist_questioning_policy import detect_gated_terms

_STAGE2_GAPS = (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY)


def _path_n_variant_count(gap_type):
    """Number of distinct Path N variants for a gap (clamp begins at this index)."""
    prev = get_path_n_question(gap_type, 0)
    n = 1
    while n < 50:
        cur = get_path_n_question(gap_type, n)
        if cur == prev:
            return n
        prev = cur
        n += 1
    raise AssertionError("Path N variant count did not converge")


def _runtime_non_specialist_early_questions():
    """Platform-asked early (Stage 2) questions for the non-specialist /start flow.

    /start sets state.path == 'N', so the runtime source is the Path N provider via
    get_display_question(..., path='N'). Enumerate each Stage 2 gap across its variants and
    one past exhaustion (which yields the deterministic stall reframe)."""
    questions = []
    for gap in _STAGE2_GAPS:
        for it in range(0, 8):
            questions.append(get_display_question("electronics_electrical", gap, it, path="N"))
    return list(dict.fromkeys(questions))


# --------------------------------------------------------------------------
# 1. /start uses Path N; named routes unchanged
# --------------------------------------------------------------------------

def test_start_initializes_path_n():
    # This idea classifies as NONE; with 2 activated domains (Mechanical
    # Activation Execution Gate) the D2 branch additionally requires an
    # explicit domain_choice.
    client = app.test_client()
    resp = client.post(
        "/start",
        data={"idea": "A small electronic reminder gadget for medicine times",
              "domain_confirm": "electronics_electrical",
              "domain_choice": "electronics_electrical"},
        follow_redirects=False,
    )
    assert resp.status_code == 302
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    try:
        entry = SESSION_STORE.get(sid)
        assert entry is not None, "session not stored"
        assert entry["state"].path == "N"
    finally:
        SESSION_STORE.pop(sid, None)


def test_named_ilt_routes_remain_on_existing_behavior():
    client = app.test_client()
    for route in ("/start_ilt002_water_leak", "/start_ilt002_combination_lock"):
        resp = client.post(route, data={"idea": "leak detector idea"},
                           follow_redirects=False)
        assert resp.status_code == 302
        sid = resp.headers["Location"].rsplit("/", 1)[-1]
        try:
            entry = SESSION_STORE.get(sid)
            assert entry is not None
            # These named routes never set Path N — they keep the default path.
            assert entry["state"].path == "legacy_undesignated_current_behavior", route
        finally:
            SESSION_STORE.pop(sid, None)


def test_path_n_governed_route_remains_path_n():
    client = app.test_client()
    resp = client.post("/start_ilt002_combination_lock_path_n",
                       data={"idea": "combination lock idea"},
                       follow_redirects=False)
    assert resp.status_code == 302
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    try:
        entry = SESSION_STORE.get(sid)
        assert entry is not None
        assert entry["state"].path == "N"
    finally:
        SESSION_STORE.pop(sid, None)


# --------------------------------------------------------------------------
# 2. Early non-specialist questions are safe
# --------------------------------------------------------------------------

def test_start_early_questions_are_non_specialist_safe():
    questions = _runtime_non_specialist_early_questions()
    violations = {q: hits for q in questions if (hits := detect_gated_terms(q))}
    assert not violations, (
        f"engineering-gated terms in non-specialist runtime questions: {violations}"
    )


# --------------------------------------------------------------------------
# 3. Stall reframe behavior (question-layer, deterministic)
# --------------------------------------------------------------------------

def test_stall_does_not_repeat_last_variant_verbatim():
    for gap in _STAGE2_GAPS:
        n = _path_n_variant_count(gap)
        last_variant = get_display_question("electronics_electrical", gap, n - 1, path="N")
        at_stall = get_display_question("electronics_electrical", gap, n, path="N")
        beyond = get_display_question("electronics_electrical", gap, n + 3, path="N")
        assert at_stall != last_variant, f"{gap}: stall repeats final variant verbatim"
        assert beyond != last_variant, f"{gap}: beyond-stall repeats final variant"
        assert at_stall == _STALL_REFRAME


def test_stall_reframe_asks_what_owner_knows_or_information_needed():
    text = _STALL_REFRAME.lower()
    assert "what do you" in text and "already know" in text
    assert "information" in text and "would need" in text


def test_stall_reframe_is_non_specialist_safe():
    assert detect_gated_terms(_STALL_REFRAME) == []


def test_stall_reframe_keeps_gap_open():
    n = _path_n_variant_count(MECHANISM_COMPLETENESS)
    state = IdeaState(idea_id="t-open")
    state.domain = "electronics_electrical"
    state.path = "N"
    gap = Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0,
              iterations_open=n)
    state.gaps = [gap]
    q = get_display_question(state.domain, MECHANISM_COMPLETENESS, gap.iterations_open,
                     path=state.path)
    assert q == _STALL_REFRAME
    assert state.get_gap(MECHANISM_COMPLETENESS).status == OPEN


def test_stall_reframe_does_not_change_maturity():
    n = _path_n_variant_count(MECHANISM_COMPLETENESS)
    state = IdeaState(idea_id="t-mat")
    state.domain = "electronics_electrical"
    state.path = "N"
    state.maturity_level = 1
    gap = Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0,
              iterations_open=n)
    state.gaps = [gap]
    before = state.maturity_level
    _ = get_display_question(state.domain, MECHANISM_COMPLETENESS, gap.iterations_open,
                     path=state.path)
    assert state.maturity_level == before


def test_one_question_per_iteration_is_preserved():
    # get_question always returns exactly one question string — never a list,
    # batch, or multi-question turn — both before and at stall.
    first = get_display_question("electronics_electrical", MECHANISM_COMPLETENESS, 0, path="N")
    assert isinstance(first, str) and first.strip()
    n = _path_n_variant_count(MECHANISM_COMPLETENESS)
    stalled = get_display_question("electronics_electrical", MECHANISM_COMPLETENESS, n + 1,
                           path="N")
    assert isinstance(stalled, str) and stalled.strip()


# --------------------------------------------------------------------------
# 4. Six owner actions unchanged
# --------------------------------------------------------------------------

def test_existing_six_owner_actions_remain_exact():
    assert INTERACTION_ACTIONS == {
        "answered", "unknown", "deferred", "provisional_assumption",
        "specialist_requested", "evidence_requested",
    }
    assert ACTION_ANSWERED == "answered"
    assert set(_NON_ANSWER_ACK.keys()) == {
        "unknown", "deferred", "provisional_assumption",
        "specialist_requested", "evidence_requested",
    }


# --------------------------------------------------------------------------
# 5. End-to-end integration: real /start route + real session-render route
# --------------------------------------------------------------------------

def _rendered_question(html):
    """Extract the single platform question rendered by session.html."""
    matches = re.findall(r'<p class="question"[^>]*>(.*?)</p>', html, re.S)
    return matches


# A distinctive, special-character-free fragment of the engineering-gated default
# (legacy/domain) MECHANISM question — must NOT appear in the non-specialist render.
_GATED_DEFAULT_FRAGMENT = "electronic circuit achieves its intended function"
# A distinctive, special-character-free fragment of the deterministic stall reframe
# (avoids Jinja-escaped apostrophes / em dashes) — appears only via get_display_question.
_REFRAME_FRAGMENT = "information do you think you would need"


def test_start_renders_path_n_question_end_to_end():
    """Real-flow integration: POST the general /start route (with the required
    domain confirmation), follow to the real session-render route, and verify the
    displayed platform question is the Path N runtime question — not the
    engineering-gated default — and that the render path uses get_display_question
    (proven via a stalled session rendering the deterministic reframe).

    Fails if /start stops setting Path N (the gated default question would render)
    OR if show_session stops using get_display_question (a stalled gap would render
    the final variant verbatim instead of the reframe). Does not call
    get_display_question directly and does not mock /start or the render route."""
    client = app.test_client()

    # --- Phase A: fresh /start through the real route + real render ---
    # This idea classifies as NONE; with 2 activated domains the D2 branch
    # additionally requires an explicit domain_choice.
    resp = client.post(
        "/start",
        data={"idea": "A small electronic reminder gadget for medicine times",
              "domain_confirm": "electronics_electrical",
              "domain_choice": "electronics_electrical"},
        follow_redirects=False,
    )
    assert resp.status_code == 302
    assert "/session/" in resp.headers["Location"]
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    try:
        entry = SESSION_STORE.get(sid)
        assert entry is not None, "session not created by /start"
        assert entry["state"].path == "N"

        page = client.get(f"/session/{sid}")
        assert page.status_code == 200
        body = page.get_data(as_text=True)

        rendered = _rendered_question(body)
        assert len(rendered) == 1, (
            f"expected exactly one platform question, found {len(rendered)} "
            "(no extra question / questionnaire may be injected)"
        )
        question = rendered[0].strip()

        # The displayed question is the Path N MECHANISM first question ...
        expected_path_n = get_path_n_question(MECHANISM_COMPLETENESS, 0)
        assert question == expected_path_n
        # ... and NOT the engineering-gated default/domain question.
        assert _GATED_DEFAULT_FRAGMENT not in body
        # The rendered platform question carries no engineering-gated terms.
        assert detect_gated_terms(question) == []
        # The reframe is not shown for a fresh (non-stalled) session.
        assert _REFRAME_FRAGMENT not in body
    finally:
        SESSION_STORE.pop(sid, None)

    # --- Phase B: a stalled Path N session renders the reframe via the real route ---
    # Seed a session whose current Stage-2 gap is at variant exhaustion, then drive
    # the REAL session-render route. Only get_display_question yields the reframe;
    # the pure get_question selector would render the final variant verbatim, so
    # this asserts show_session uses get_display_question.
    exhausted = _path_n_variant_count(MECHANISM_COMPLETENESS)
    stalled_sid = "incr1-e2e-stall-sid"
    state = IdeaState(idea_id="incr1-e2e-stall")
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    state.path = "N"
    state.gaps = [Gap(gap_type=MECHANISM_COMPLETENESS, status=OPEN, opened_at=0,
                      iterations_open=exhausted)]
    SESSION_STORE[stalled_sid] = {"state": state, "last_result": None, "transcript": []}
    try:
        page = client.get(f"/session/{stalled_sid}")
        assert page.status_code == 200
        body = page.get_data(as_text=True)
        rendered = _rendered_question(body)
        assert len(rendered) == 1
        # The reframe (not a verbatim repeat of the final Path N variant) is shown.
        assert _REFRAME_FRAGMENT in rendered[0]
        # Still non-specialist safe and still a single question.
        assert detect_gated_terms(rendered[0]) == []
    finally:
        SESSION_STORE.pop(stalled_sid, None)
