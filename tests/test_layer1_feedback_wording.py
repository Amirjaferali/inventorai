"""Layer-1 Feedback Wording / Gap-Type-Aware Guidance — implementation tests.

Governed by
`docs/governance/LAYER1_FEEDBACK_WORDING_GAP_TYPE_GUIDANCE_INCREMENT_CONTRACT.md`
(true-merged via PR #115). Proves the display-only, deterministic guidance:
- distinguishes honest wording for (a) a first accepted/REASONED answer whose gap
  is PARTIAL, (b) an asserted-only answer, and (c) boundary/feasibility answers;
- keeps the truthful WARN state visible (never implies the gap is closed);
- is gap-type-aware (boundary/feasibility prompts differ from mechanism prompts);
- renders no guidance on PASS;
- introduces no forbidden Answer-Clarification fields and mutates nothing;
- leaves scoring, transition outcome, gap status, maturity, stored answers,
  persistence behavior, and Domain-Gate rejection unchanged.
"""
import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import app, SESSION_STORE, UNSUPPORTED_DOMAIN_MESSAGE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from web.scaffolding_guidance import get_scaffolding_guidance  # noqa: E402
from engine.idea_state import IdeaState  # noqa: E402
from engine.progression_loop import assess_response  # noqa: E402

_HEADING = "What kind of detail to add"

# Words that would falsely imply the accepted first answer was poor quality.
_QUALITY_SLUR_WORDS = (
    "weak", "poor", "insufficient", "inadequate", "deficient", "low quality",
    "not good", "bad answer", "wrong",
)
# Forbidden validation/readiness claim words (Layer-1 contract §5).
_FORBIDDEN_CLAIM_WORDS = (
    "valid", "safe", "feasib", "compliance", "certif", "build-ready",
    "buildable", "patent", "ready to build", "verified", "proven",
)
_FORBIDDEN_FIELDS = (
    "suggested_clarified_answer", "user_approved_answer",
    "original_user_answer", "clarification_status",
)


def _warn(gap_type, tail):
    return {"transition": "WARN", "reason": f"{gap_type} {tail}", "direction": "STALLED"}


def _text_blob(g):
    return (g["heading"] + " " + g["lead"] + " " + g["note"] + " " + " ".join(g["prompts"]))


# ---------------------------------------------------------------------------
# (7)(8) First REASONED / PARTIAL wording
# ---------------------------------------------------------------------------

def test_partial_wording_does_not_imply_poor_quality():
    for gap in ("MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "PHYSICAL_FEASIBILITY"):
        g = get_scaffolding_guidance(_warn(gap, "partially addressed — needs more depth"), gap_type=gap)
        lead = g["lead"].lower()
        assert "accepted" in lead  # positively acknowledges the answer
        for slur in _QUALITY_SLUR_WORDS:
            assert slur not in lead, (gap, slur)


def test_partial_wording_says_gap_not_closed_yet():
    for gap in ("MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "PHYSICAL_FEASIBILITY"):
        g = get_scaffolding_guidance(_warn(gap, "partially addressed — needs more depth"), gap_type=gap)
        lead = g["lead"].lower()
        # Truthful WARN remains visible: it must say one more answer is needed
        # before the gap can close.
        assert "close" in lead
        assert "one more" in lead


# ---------------------------------------------------------------------------
# (9) ASSERTED-only wording still asks for reasoning/detail
# ---------------------------------------------------------------------------

def test_asserted_wording_asks_for_reasoning():
    for gap in ("MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "PHYSICAL_FEASIBILITY"):
        g = get_scaffolding_guidance(_warn(gap, "asserted only — reasoning required"), gap_type=gap)
        assert "reasoning" in g["lead"].lower()


# ---------------------------------------------------------------------------
# (10) Boundary/feasibility guidance differs from mechanism guidance
# ---------------------------------------------------------------------------

def test_gap_type_aware_prompts_differ():
    mech = get_scaffolding_guidance(_warn("MECHANISM_COMPLETENESS", "asserted only — reasoning required"),
                                    gap_type="MECHANISM_COMPLETENESS")["prompts"]
    boundary = get_scaffolding_guidance(_warn("BOUNDARY_AMBIGUITY", "asserted only — reasoning required"),
                                        gap_type="BOUNDARY_AMBIGUITY")["prompts"]
    feasibility = get_scaffolding_guidance(_warn("PHYSICAL_FEASIBILITY", "asserted only — reasoning required"),
                                           gap_type="PHYSICAL_FEASIBILITY")["prompts"]
    assert mech != boundary
    assert mech != feasibility
    assert boundary != feasibility
    # Boundary prompts ask about scope/limits; mechanism prompts do not.
    assert any("scope" in p.lower() or "limit" in p.lower() for p in boundary)
    assert not any("scope" in p.lower() for p in mech)
    # Feasibility prompts ask about physical limits/constraints.
    assert any("constraint" in p.lower() or "operating range" in p.lower() for p in feasibility)


def test_gap_family_recovered_from_reason_when_gap_type_absent():
    # gap_type not passed; family recovered from the reason's leading token.
    g = get_scaffolding_guidance(_warn("BOUNDARY_AMBIGUITY", "asserted only — reasoning required"))
    assert any("scope" in p.lower() or "does not do" in p.lower().replace("not do", "does not do")
               for p in g["prompts"])


# ---------------------------------------------------------------------------
# No validation/readiness/answer-content claims; safe keys only
# ---------------------------------------------------------------------------

def test_no_forbidden_claim_words_across_all_families_and_cases():
    cases = ("partially addressed — needs more depth", "asserted only — reasoning required")
    gaps = ("MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "PHYSICAL_FEASIBILITY")
    for gap in gaps:
        for tail in cases:
            g = get_scaffolding_guidance(_warn(gap, tail), gap_type=gap)
            blob = _text_blob(g).lower()
            for forbidden in _FORBIDDEN_CLAIM_WORDS:
                assert forbidden not in blob, (gap, tail, forbidden)


def test_only_safe_keys_and_no_forbidden_fields():
    g = get_scaffolding_guidance(_warn("MECHANISM_COMPLETENESS", "asserted only — reasoning required"),
                                 gap_type="MECHANISM_COMPLETENESS")
    assert set(g.keys()) == {"heading", "lead", "prompts", "note"}
    for field in _FORBIDDEN_FIELDS:
        assert field not in g


# ---------------------------------------------------------------------------
# (11) PASS renders no guidance; (2) other outcomes → None
# ---------------------------------------------------------------------------

def test_no_guidance_for_pass_block_or_missing():
    assert get_scaffolding_guidance({"transition": "PASS", "reason": "ok"}) is None
    assert get_scaffolding_guidance({"transition": "BLOCK", "reason": "no"}) is None
    assert get_scaffolding_guidance(None) is None
    assert get_scaffolding_guidance({}) is None


# ---------------------------------------------------------------------------
# (1) Scoring output unchanged — assess_response classification is untouched
# ---------------------------------------------------------------------------

def test_assess_response_scoring_untouched_and_deterministic():
    # The display layer does not import into, wrap, or alter assess_response.
    # Scoring stays deterministic and returns a valid tier; a plain claim with no
    # causal structure stays ASSERTED. (The authoritative proof that the locked
    # scoring behavior is unchanged is that tests/test_assess_response_replay.py
    # and tests/test_assess_response_adversarial.py still pass — run in the
    # broader subset — since this change touches only web/scaffolding_guidance.py.)
    valid_tiers = {"ASSERTED", "REASONED", "DEMONSTRATED"}
    r1 = assess_response("It alerts people.", "electronics_electrical")
    r2 = assess_response("It alerts people.", "electronics_electrical")
    assert r1 == r2 == "ASSERTED"  # deterministic; plain claim stays ASSERTED
    assert assess_response(
        "The sensor detects rising current and the microcontroller opens the relay.",
        "electronics_electrical",
    ) in valid_tiers


# ---------------------------------------------------------------------------
# (3)(4)(5)(11)(13) Rendered page: no mutation of answer/state/outcome; PASS blank
# ---------------------------------------------------------------------------

def _store(sid, state, last_result, transcript=None, last_question=None):
    SESSION_STORE[sid] = {"state": state, "last_result": last_result,
                          "transcript": transcript or [], "last_question": last_question}


def test_render_preserves_answer_state_and_outcome():
    sid = "l1-no-mutation"
    state = IdeaState(idea_id="l1-1")
    state.domain = "electronics_electrical"
    state.maturity_level = 1
    last_result = _warn("MECHANISM_COMPLETENESS", "partially addressed — needs more depth")
    transcript = [{"response": "the plug senses current and cuts power", "iteration": 1}]
    _store(sid, state, last_result, transcript, "How does it work?")
    before_answer = copy.deepcopy(transcript)
    before_maturity = state.maturity_level
    before_gap_status = [(g.gap_type, g.status) for g in state.gaps]
    before_transition = last_result["transition"]
    before_store_keys = set(SESSION_STORE[sid].keys())
    try:
        resp = app.test_client().get(f"/session/{sid}")
        assert resp.status_code == 200
        assert _HEADING in resp.get_data(as_text=True)  # WARN guidance shown
        assert SESSION_STORE[sid]["transcript"] == before_answer  # answer byte-for-byte
        assert state.maturity_level == before_maturity
        assert [(g.gap_type, g.status) for g in state.gaps] == before_gap_status
        assert SESSION_STORE[sid]["last_result"]["transition"] == before_transition
        # No new persistence/schema keys introduced into the session record.
        assert set(SESSION_STORE[sid].keys()) == before_store_keys
        for field in _FORBIDDEN_FIELDS:
            assert not hasattr(state, field)
            assert field not in SESSION_STORE[sid]
    finally:
        SESSION_STORE.pop(sid, None)


def test_render_pass_shows_no_guidance():
    sid = "l1-pass"
    state = IdeaState(idea_id="l1-2")
    state.domain = "electronics_electrical"
    _store(sid, state, {"transition": "PASS", "reason": "good", "direction": "PROGRESSING"})
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _HEADING not in body
    finally:
        SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# (12) Unsupported-domain rejection unchanged
# ---------------------------------------------------------------------------

def _start(idea, confirm=True):
    data = {"idea": idea}
    if confirm:
        data["domain_confirm"] = DOMAIN_CONFIRM_VALUE
    return app.test_client().post("/start", data=data, follow_redirects=False)


def test_unsupported_domain_rejection_unchanged():
    before = set(SESSION_STORE)
    resp = _start("a gearbox with a rotating shaft and bearing torque")
    assert resp.status_code == 200
    assert UNSUPPORTED_DOMAIN_MESSAGE in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before  # no session created for unsupported idea

    resp2 = _start("ESP32 microcontroller circuit with a voltage sensor")
    assert resp2.status_code == 302
    assert "/session/" in resp2.headers["Location"]
    SESSION_STORE.pop(resp2.headers["Location"].rsplit("/", 1)[-1], None)
