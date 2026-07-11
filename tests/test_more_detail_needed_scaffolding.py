"""More Detail Needed / Guided Answer Scaffolding — implementation tests.

Governed by
`docs/governance/MORE_DETAIL_NEEDED_GUIDED_SCAFFOLDING_INCREMENT_CONTRACT.md`
(true-merged via PR #106). Proves the display-only, deterministic guidance
appears for WARN-class insufficiency, tells the inventor what KIND of missing
detail to add, and never rewrites/stores the answer, closes a gap, advances
maturity, alters the PASS/WARN/BLOCK outcome, introduces forbidden Answer
Clarification fields, or changes Domain Gate / Increment 1B behavior.
"""
import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import app, SESSION_STORE, UNSUPPORTED_DOMAIN_MESSAGE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from web.scaffolding_guidance import get_scaffolding_guidance  # noqa: E402
from engine.idea_state import IdeaState  # noqa: E402

_HEADING = "What kind of detail to add"

# Forbidden claim words that must never appear in guidance text (contract §8).
_FORBIDDEN_CLAIM_WORDS = (
    "valid", "safe", "feasib", "compliance", "certif", "build-ready",
    "buildable", "patent", "ready to build", "verified", "proven",
)
# Forbidden Answer-Clarification / Improve-Wording field names (contract §8).
_FORBIDDEN_FIELDS = (
    "suggested_clarified_answer", "user_approved_answer",
    "original_user_answer", "clarification_status",
)


def _warn(reason):
    return {"transition": "WARN", "reason": reason, "direction": "STALLED"}


# ---------------------------------------------------------------------------
# Pure guidance function
# ---------------------------------------------------------------------------

def test_guidance_none_without_warn_result():
    assert get_scaffolding_guidance(None) is None
    assert get_scaffolding_guidance({}) is None
    assert get_scaffolding_guidance("not a dict") is None


def test_guidance_none_for_pass_and_block():
    assert get_scaffolding_guidance({"transition": "PASS", "reason": "ok"}) is None
    assert get_scaffolding_guidance({"transition": "BLOCK", "reason": "no"}) is None


def test_guidance_asserted_reason_names_missing_reasoning():
    # Micro UX correction: the lead no longer repeats the recognizer
    # explanation (that lives once in the primary result feedback); it names
    # the KIND of detail to make explicit for the mechanism family directly.
    g = get_scaffolding_guidance(_warn("MECHANISM_COMPLETENESS asserted only — reasoning required"))
    assert g is not None
    assert g["heading"] == _HEADING
    lead = g["lead"].lower()
    assert "explicit" in lead
    assert "chain" in lead or "condition" in lead


def test_guidance_partial_reason_asks_for_more_depth():
    g = get_scaffolding_guidance(_warn("MECHANISM_COMPLETENESS partially addressed — needs more depth"))
    assert g is not None
    assert "more" in g["lead"].lower() and "detail" in g["lead"].lower()


def test_guidance_intake_reason_asks_problem_and_how():
    g = get_scaffolding_guidance(_warn("mechanism not yet established"))
    assert g is not None
    assert "problem" in g["lead"].lower()


def test_guidance_generic_fallback_for_other_warn():
    g = get_scaffolding_guidance(_warn("some other warn reason"))
    assert g is not None
    assert g["heading"] == _HEADING


def test_guidance_tells_what_kind_of_detail():
    # Category-level prompts naming KINDS of missing detail (contract §9).
    g = get_scaffolding_guidance(_warn("x asserted only — reasoning required"))
    blob = " ".join(g["prompts"]).lower()
    for kind in ("mechanism", "condition", "detect", "output", "evidence"):
        assert kind in blob


def test_guidance_dict_has_only_safe_keys_and_no_forbidden_fields():
    g = get_scaffolding_guidance(_warn("x asserted only — reasoning required"))
    assert set(g.keys()) == {"heading", "lead", "prompts", "note"}
    for field in _FORBIDDEN_FIELDS:
        assert field not in g


def test_guidance_text_makes_no_validation_or_safety_claim():
    g = get_scaffolding_guidance(_warn("x asserted only — reasoning required"))
    text = (g["heading"] + " " + g["lead"] + " " + g["note"] + " " + " ".join(g["prompts"])).lower()
    for forbidden in _FORBIDDEN_CLAIM_WORDS:
        assert forbidden not in text


def test_guidance_does_not_mutate_inputs():
    result = _warn("x asserted only — reasoning required")
    before = copy.deepcopy(result)
    get_scaffolding_guidance(result, gap_type="MECHANISM_COMPLETENESS")
    assert result == before


# ---------------------------------------------------------------------------
# Rendered session page
# ---------------------------------------------------------------------------

def _store(sid, state, last_result):
    SESSION_STORE[sid] = {"state": state, "last_result": last_result, "transcript": []}


def test_session_page_shows_guidance_on_warn():
    sid = "mdn-warn-shows-guidance"
    state = IdeaState(idea_id="mdn-1")
    state.domain = "electronics_electrical"
    _store(sid, state, _warn("MECHANISM_COMPLETENESS asserted only — reasoning required"))
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _HEADING in body
        assert "What condition triggers the action?" in body
        assert "do not change or grade your answer" in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_session_page_no_guidance_on_pass():
    sid = "mdn-pass-no-guidance"
    state = IdeaState(idea_id="mdn-2")
    state.domain = "electronics_electrical"
    _store(sid, state, {"transition": "PASS", "reason": "good", "direction": "PROGRESSING"})
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _HEADING not in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_render_does_not_change_stored_answer_state_or_outcome():
    sid = "mdn-no-mutation"
    state = IdeaState(idea_id="mdn-3")
    state.domain = "electronics_electrical"
    state.maturity_level = 1
    last_result = _warn("MECHANISM_COMPLETENESS partially addressed — needs more depth")
    transcript = [{"response": "the plug senses current and cuts power", "iteration": 1}]
    SESSION_STORE[sid] = {"state": state, "last_result": last_result,
                          "transcript": transcript,
                          "last_question": "How does it work?"}
    before_answer = copy.deepcopy(transcript)
    before_maturity = state.maturity_level
    before_gap_count = len(state.gaps)
    before_gap_status = [(g.gap_type, g.status) for g in state.gaps]
    before_transition = last_result["transition"]
    try:
        resp = app.test_client().get(f"/session/{sid}")
        assert resp.status_code == 200
        assert _HEADING in resp.get_data(as_text=True)  # guidance shown (WARN)
        # Stored answer byte-for-byte unchanged; no maturity/gap advance; outcome intact.
        assert SESSION_STORE[sid]["transcript"] == before_answer
        assert state.maturity_level == before_maturity
        assert len(state.gaps) == before_gap_count
        assert [(g.gap_type, g.status) for g in state.gaps] == before_gap_status
        assert SESSION_STORE[sid]["last_result"]["transition"] == before_transition
    finally:
        SESSION_STORE.pop(sid, None)


def test_no_forbidden_answer_clarification_fields_introduced():
    sid = "mdn-no-forbidden-fields"
    state = IdeaState(idea_id="mdn-4")
    state.domain = "electronics_electrical"
    _store(sid, state, _warn("MECHANISM_COMPLETENESS asserted only — reasoning required"))
    try:
        app.test_client().get(f"/session/{sid}")
        for field in _FORBIDDEN_FIELDS:
            assert not hasattr(state, field)
            assert field not in SESSION_STORE[sid]
    finally:
        SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# Regressions: Domain Gate (PR #101) and Increment 1B are unaffected
# ---------------------------------------------------------------------------

def _start(idea, confirm=True):
    data = {"idea": idea}
    if confirm:
        data["domain_confirm"] = DOMAIN_CONFIRM_VALUE
    return app.test_client().post("/start", data=data, follow_redirects=False)


def test_domain_gate_still_rejects_unsupported_and_admits_electronics():
    # Regression: importing/adding the scaffolding surface changes no gate behavior.
    before = set(SESSION_STORE)
    resp = _start("a gearbox with a rotating shaft and bearing torque")
    assert resp.status_code == 200
    assert UNSUPPORTED_DOMAIN_MESSAGE in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before  # no session created for unsupported idea

    resp2 = _start("ESP32 microcontroller circuit with a voltage sensor")
    assert resp2.status_code == 302
    assert "/session/" in resp2.headers["Location"]


def test_increment_1b_help_expander_preserved_and_distinct_from_guidance():
    # A live electronics session renders the Increment 1B "Help me understand this
    # question" expander; the new scaffolding guidance is a separate surface.
    resp = _start("ESP32 microcontroller circuit with a voltage sensor")
    assert resp.status_code == 302
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert "Help me understand this question" in body  # Increment 1B intact
    finally:
        SESSION_STORE.pop(sid, None)
