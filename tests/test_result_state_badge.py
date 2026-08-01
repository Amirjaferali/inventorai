"""Result-State Badge — Increment 1: Accepted-vs-Rejected Result-State Clarity.

File: tests/test_result_state_badge.py
Purpose: pin the presentation-only badge distinction between an ACCEPTED first
REASONED answer (gap moved to PARTIAL) and an ASSERTED answer that was not
accepted, plus the removal of the raw "Direction: PROGRESSING" display.
Input contract: exercises only web.result_feedback.get_result_badge (pure
display helper) and the rendered /session page via the Flask test client.
Output contract: assertions only; no repository or fixture mutation.
Prohibited behaviors verified here: no engine transition/reason/gap/maturity/
direction/transcript change; no re-scoring; no mutation of last_result.

Proves the owner-authorized increment:
  * accepted first REASONED answer (WARN + "partially addressed") shows
    accepted/progressed wording — "Accepted — one more step";
  * ASSERTED answer (WARN + "asserted only") shows not-yet-sufficient wording —
    "More explanation needed";
  * closed/completed area (PASS) still shows "Good progress";
  * the two WARN outcomes no longer share the same badge (label AND css class);
  * raw "Direction: PROGRESSING" is absent from the normal display;
  * engine result, gap state, maturity, and transcript remain unchanged.
"""

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from web.result_feedback import get_result_badge  # noqa: E402
from engine.progression_loop import assess_response  # noqa: E402

# Pinned badge presentations (display-only; selected from the already-computed
# transition + the stable, replay-locked reason substrings).
_ACCEPTED = {"css_class": "badge-accepted", "label": "Accepted — one more step"}
_NOT_ACCEPTED = {"css_class": "badge-warn", "label": "More explanation needed"}
_WARN_OTHER = {"css_class": "badge-warn", "label": "More detail needed"}
_PASS = {"css_class": "badge-pass", "label": "Good progress"}
_BLOCK = {"css_class": "badge-block", "label": "Not enough to continue"}

# Fixed journey answers (engine classification asserted as a precondition in the
# journey test so any scoring change surfaces there, not silently here).
_REASONED_ANSWER = (
    "The voltage sensor detects an overload because the resistor divider "
    "raises its input, therefore the relay opens the circuit."
)
_ASSERTED_ANSWER = "It just works and people will like it."


def _session():
    r = app.test_client().post(
        "/start",
        data={"idea": "ESP32 microcontroller circuit with a voltage sensor and relay",
              "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _force(sid, transition, reason, direction=None):
    SESSION_STORE[sid]["last_result"] = {
        "transition": transition, "reason": reason, "direction": direction}


def _body(sid):
    return app.test_client().get(f"/session/{sid}").get_data(as_text=True)


# ---------------------------------------------------------------------------
# Pure helper — pinned mapping, distinctness, purity
# ---------------------------------------------------------------------------

def test_helper_pinned_mapping():
    assert get_result_badge({"transition": "WARN",
                             "reason": "X partially addressed — needs more depth"}) == _ACCEPTED
    assert get_result_badge({"transition": "WARN",
                             "reason": "X asserted only — reasoning required"}) == _NOT_ACCEPTED
    assert get_result_badge({"transition": "PASS",
                             "reason": "X closed after REASONED follow-up"}) == _PASS
    assert get_result_badge({"transition": "PASS",
                             "reason": "X closed with DEMONSTRATED evidence"}) == _PASS
    assert get_result_badge({"transition": "PASS",
                             "reason": "Problem established — ready for LEVEL 1"}) == _PASS
    assert get_result_badge({"transition": "BLOCK",
                             "reason": "BLOCK: X not yet closed"}) == _BLOCK


def test_helper_other_warn_reasons_keep_prior_generic_badge():
    for reason in ("Problem not yet established",
                   "LEVEL 2 is max for MVP",
                   "MECHANISM_COMPLETENESS must be attempted first",
                   "Mechanism quality must be REASONED minimum",
                   "some unexpected future reason"):
        assert get_result_badge({"transition": "WARN", "reason": reason}) == _WARN_OTHER, reason


def test_helper_none_for_missing_or_unrecognized_result():
    assert get_result_badge(None) is None
    assert get_result_badge({}) is None
    assert get_result_badge("not a dict") is None
    assert get_result_badge({"transition": "SOMETHING_ELSE", "reason": "x"}) is None


def test_accepted_and_not_accepted_badges_are_visually_distinct():
    a = get_result_badge({"transition": "WARN",
                          "reason": "X partially addressed — needs more depth"})
    b = get_result_badge({"transition": "WARN",
                          "reason": "X asserted only — reasoning required"})
    assert a["label"] != b["label"]
    assert a["css_class"] != b["css_class"]


def test_helper_is_pure_and_does_not_mutate_result():
    result = {"transition": "WARN",
              "reason": "X partially addressed — needs more depth",
              "direction": "PROGRESSING"}
    before = copy.deepcopy(result)
    out1 = get_result_badge(result)
    out2 = get_result_badge(result)
    assert result == before          # input untouched
    assert out1 == out2              # deterministic
    assert out1 is not out2          # fresh dict per call — constants shielded
    out1["label"] = "mutated"
    assert get_result_badge(result)["label"] == _ACCEPTED["label"]


def test_accepted_badge_wording_never_implies_rejection():
    low = _ACCEPTED["label"].lower()
    for w in ("reject", "not accepted", "insufficient", "failed", "wrong",
              "more detail needed", "more explanation needed"):
        assert w not in low, w


# ---------------------------------------------------------------------------
# Rendered session page — the three states are immediately distinguishable
# ---------------------------------------------------------------------------

def test_rendered_accepted_partial_page_shows_accepted_badge():
    sid = _session()
    try:
        _force(sid, "WARN",
               "PHYSICAL_FEASIBILITY partially addressed — needs more depth",
               direction="PROGRESSING")
        b = _body(sid)
        assert "Accepted — one more step" in b
        assert 'class="badge-accepted"' in b
        # the not-accepted and generic-WARN badge wordings do not appear
        assert "More explanation needed" not in b
        assert "More detail needed" not in b
    finally:
        SESSION_STORE.pop(sid, None)


def test_rendered_asserted_page_shows_not_accepted_badge():
    sid = _session()
    try:
        _force(sid, "WARN",
               "PHYSICAL_FEASIBILITY asserted only — reasoning required",
               direction="PROGRESSING")
        b = _body(sid)
        assert "More explanation needed" in b
        assert "Accepted — one more step" not in b
        assert 'class="badge-accepted"' not in b
    finally:
        SESSION_STORE.pop(sid, None)


def test_rendered_completed_page_keeps_good_progress_badge():
    sid = _session()
    try:
        _force(sid, "PASS",
               "PHYSICAL_FEASIBILITY closed after REASONED follow-up",
               direction="PROGRESSING")
        b = _body(sid)
        assert "Good progress" in b
        assert 'class="badge-pass"' in b
    finally:
        SESSION_STORE.pop(sid, None)


def test_raw_direction_absent_from_normal_display():
    sid = _session()
    try:
        for transition, reason in (
                ("WARN", "X partially addressed — needs more depth"),
                ("WARN", "X asserted only — reasoning required"),
                ("PASS", "X closed after REASONED follow-up")):
            _force(sid, transition, reason, direction="PROGRESSING")
            b = _body(sid)
            assert "Direction: PROGRESSING" not in b, (transition, reason)
            assert 'class="direction-text"' not in b, (transition, reason)
            # internal direction enum untouched by rendering
            assert SESSION_STORE[sid]["last_result"]["direction"] == "PROGRESSING"
    finally:
        SESSION_STORE.pop(sid, None)


def test_no_result_still_renders_neutral_badge():
    sid = _session()
    try:
        SESSION_STORE[sid]["last_result"] = {"transition": "UNRECOGNIZED", "reason": "x"}
        assert "Response recorded" in _body(sid)
    finally:
        SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# Real engine journey — badges track the genuine computed states, and the
# engine result, gap state, maturity, and transcript remain unchanged
# ---------------------------------------------------------------------------

def test_real_journey_badges_and_engine_state_unchanged():
    # Preconditions: the fixed answers still classify as before (any scoring
    # change surfaces here explicitly instead of silently altering the journey).
    assert assess_response(_REASONED_ANSWER, "electronics_electrical") == "REASONED"
    assert assess_response(_ASSERTED_ANSWER, "electronics_electrical") == "ASSERTED"

    sid = _session()
    c = app.test_client()
    try:
        # Iterations 2-3: intake PASS then close MECHANISM_COMPLETENESS; reach
        # the first-accepted-REASONED state on PHYSICAL_FEASIBILITY (iteration 4).
        for _ in range(3):
            c.post(f"/session/{sid}", data={"response": _REASONED_ANSWER,
                                            "action": "answered"})
        lr = SESSION_STORE[sid]["last_result"]
        assert lr["transition"] == "WARN"
        assert "partially addressed — needs more depth" in lr["reason"]
        state = SESSION_STORE[sid]["state"]
        assert [(g.gap_type, g.status) for g in state.gaps] == [
            ("MECHANISM_COMPLETENESS", "CLOSED"),
            ("PHYSICAL_FEASIBILITY", "PARTIAL")]

        before_result = copy.deepcopy(lr)
        before_maturity = state.maturity_level
        before_gaps = [(g.gap_type, g.status) for g in state.gaps]
        before_transcript = copy.deepcopy(SESSION_STORE[sid]["transcript"])

        # State A rendered: accepted — one more step.
        b = _body(sid)
        assert "Accepted — one more step" in b
        assert "More explanation needed" not in b
        assert "Direction: PROGRESSING" not in b

        # Rendering changed nothing.
        assert SESSION_STORE[sid]["last_result"] == before_result
        assert state.maturity_level == before_maturity
        assert [(g.gap_type, g.status) for g in state.gaps] == before_gaps
        assert SESSION_STORE[sid]["transcript"] == before_transcript

        # State B: an ASSERTED answer is not accepted.
        c.post(f"/session/{sid}", data={"response": _ASSERTED_ANSWER,
                                        "action": "answered"})
        lr = SESSION_STORE[sid]["last_result"]
        assert lr["transition"] == "WARN"
        assert "asserted only — reasoning required" in lr["reason"]
        b = _body(sid)
        assert "More explanation needed" in b
        assert "Accepted — one more step" not in b

        # State C: closing REASONED follow-up completes the area.
        c.post(f"/session/{sid}", data={"response": _REASONED_ANSWER,
                                        "action": "answered"})
        lr = SESSION_STORE[sid]["last_result"]
        assert lr["transition"] == "PASS"
        assert "closed after REASONED follow-up" in lr["reason"]
        b = _body(sid)
        assert "Good progress" in b

        # Answers were stored verbatim throughout; no badge text leaked into
        # the transcript.
        stored = " ".join(r.get("response", "")
                          for r in SESSION_STORE[sid]["transcript"])
        for badge_text in ("Accepted — one more step", "More explanation needed",
                           "Good progress"):
            assert badge_text not in stored
    finally:
        SESSION_STORE.pop(sid, None)
