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
from test_p4_1b2a_durable_answer_append import answered_post  # P4-1b-2a
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

def test_asserted_wording_asks_for_explicit_structure():
    # Micro UX correction: the lead no longer repeats the recognizer
    # explanation (that lives once in the primary result feedback); it begins
    # directly with actionable guidance asking to make the structure explicit.
    for gap in ("MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "PHYSICAL_FEASIBILITY"):
        g = get_scaffolding_guidance(_warn(gap, "asserted only — reasoning required"), gap_type=gap)
        lead = g["lead"].lower()
        assert "explicit" in lead
        assert "why" in lead


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
# Feedback-truthfulness correction (owner-gated; scoring unchanged):
# ASSERTED-state feedback must be detector-honest. The engine knows only that
# its deterministic recognizer did not detect enough of the explicit structure
# it accepts — it must NEVER tell the inventor that reasoning, mechanism,
# limits, or rationale are absent from the answer.
# ---------------------------------------------------------------------------

# Superseded untruthful diagnosis phrases that must never reappear in
# ASSERTED-state feedback (each claims the answer lacks something the
# recognizer cannot establish is absent).
_FALSE_ABSENCE_PHRASES = (
    "but not how or why",
    "but not the reasoning",
    "not the reasoning behind",
    "no reasoning",
    "without reasoning",
    "says what happens",
    "states that it works",
    "only stated",
    "no rationale",
    "does not explain",
)
# Internal recognizer/scoring terminology that must never be exposed.
_INTERNAL_TOKENS = ("asserted", "reasoned", "lexical", "regex", "classifier")
# The detector-honest marker every ASSERTED-state feedback must carry.
_DETECTOR_HONEST_MARK = "did not recognize enough explicit"

# Answers that plainly contain reasoning language yet remain classified
# ASSERTED by the recognizer. These are the recognizer's remaining known
# false negatives after the Layer-2 connective+whole-word-substance gate
# (owner-authorized 2026-07-11): the new gate requires a whole-word domain
# substance signal inside the clause supporting the connective, so a
# substance-free rationale clause ("dust buildup can distort the thermal
# readings…", "internet connectivity may be unavailable…") and the implicit
# no-connective mechanism chain still classify ASSERTED. The classification
# is pinned; the displayed feedback must not contradict the answer.
_REASONING_BEARING_ASSERTED_EXAMPLES = (
    ("because", "The device should use a sealed sensor chamber because dust "
                "buildup can distort the thermal readings and cause false alarms."),
    ("since", "The controller should retain the previous threshold locally "
              "since internet connectivity may be unavailable during a fault."),
    ("no-connective-mechanism", "The thermistor resistance drops with heat. "
                                "The comparator output flips at 2.5 volts. "
                                "The relay coil energizes and disconnects the load."),
)

# Scoring-specific expected-REASONED set: previously pinned ASSERTED, now
# recognized by the Layer-2 connective gate because the rationale clause
# after "because" carries whole-word domain substance ("currents" plural-
# folds to the authorized signal "current"; "sensor's" tokenizes to the
# authorized signal "sensor"). Moved here from the ASSERTED truthfulness set
# per the owner-gated Layer-2 authorization; feedback truthfulness
# protections above are unchanged.
_CONNECTIVE_GATE_EXPECTED_REASONED_EXAMPLES = (
    ("scope-rationale", "The device covers only single-phase circuits because "
                        "three-phase fault currents exceed the sensor's saturation limit."),
)


def test_asserted_leads_never_claim_reasoning_is_absent():
    # Micro UX correction: the recognizer-limitation explanation is rendered
    # ONCE by the primary result feedback; the leads must NOT repeat it (the
    # previous requirement that the mark appear in both was the confirmed
    # duplication defect). Truthfulness is preserved: leads still never claim
    # reasoning is absent and never expose internal terminology.
    for gap in ("MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "PHYSICAL_FEASIBILITY"):
        g = get_scaffolding_guidance(_warn(gap, "asserted only — reasoning required"), gap_type=gap)
        lead = g["lead"].lower()
        assert _DETECTOR_HONEST_MARK not in lead, gap
        assert "move this area forward" not in lead, gap
        for phrase in _FALSE_ABSENCE_PHRASES:
            assert phrase not in lead, (gap, phrase)
        for token in _INTERNAL_TOKENS:
            assert token not in lead, (gap, token)


def test_asserted_leads_are_actionable_per_family():
    # Mechanism family: asks for the explicit physical/functional chain.
    mech = get_scaffolding_guidance(
        _warn("MECHANISM_COMPLETENESS", "asserted only — reasoning required"),
        gap_type="MECHANISM_COMPLETENESS")["lead"].lower()
    assert "condition" in mech and "respond" in mech and "why" in mech
    # Boundary family: asks for the explicit reason for the boundary.
    boundary = get_scaffolding_guidance(
        _warn("BOUNDARY_AMBIGUITY", "asserted only — reasoning required"),
        gap_type="BOUNDARY_AMBIGUITY")["lead"].lower()
    assert "boundary" in boundary and "limit" in boundary and "why" in boundary
    # Feasibility family: asks for explicit operating conditions/constraints/
    # dependencies (never says the answer merely states that it works).
    feas = get_scaffolding_guidance(
        _warn("PHYSICAL_FEASIBILITY", "asserted only — reasoning required"),
        gap_type="PHYSICAL_FEASIBILITY")["lead"].lower()
    assert "conditions" in feas and "constraints" in feas and "dependencies" in feas


def test_stage3_and_generic_asserted_lead_is_neutral_not_mechanism_specific():
    # Stage-3 / unknown gap types fall back to the generic lead, which must be
    # suitable for list-style and declarative answers (problem fit, assumption
    # inventories, expertise/specialist lists): it must not repeat the
    # recognizer explanation (that lives in the primary line), must not assume
    # a mechanism or a condition-response relationship, must not assume the
    # answer "addresses" something, and must not claim content is absent.
    for gap in ("PROBLEM_MECHANISM_FIT", "ASSUMPTION_INVENTORY",
                "EXPERTISE_GAP_AWARENESS", None):
        g = get_scaffolding_guidance(
            _warn(gap or "SOME_FUTURE_GAP", "asserted only — reasoning required"),
            gap_type=gap)
        lead = g["lead"].lower()
        assert _DETECTOR_HONEST_MARK not in lead, gap
        assert "mechanism" not in lead, gap
        assert "addresses" not in lead, gap
        assert "condition" not in lead, gap
        for phrase in _FALSE_ABSENCE_PHRASES:
            assert phrase not in lead, (gap, phrase)


def test_generic_lead_is_actionable_for_list_style_answers():
    # The generic lead must invite question-appropriate specificity that works
    # equally for problem-fit prose, assumption inventories, and expertise
    # lists: name the items, say why each matters, flag remaining uncertainty
    # or the need for specialist input.
    g = get_scaffolding_guidance(
        _warn("ASSUMPTION_INVENTORY", "asserted only — reasoning required"),
        gap_type="ASSUMPTION_INVENTORY")
    lead = g["lead"].lower()
    assert "name" in lead
    assert "why" in lead
    assert "uncertain" in lead or "specialist" in lead


def test_recognizer_explanation_appears_in_primary_but_never_in_leads():
    # Duplication acceptance rule: explanation once (primary result feedback),
    # actionable guidance next (scaffolding lead) — never the same sentence
    # twice in the normal ASSERTED flow.
    from web.result_feedback import get_result_feedback
    result = _warn("MECHANISM_COMPLETENESS", "asserted only — reasoning required")
    assert _DETECTOR_HONEST_MARK in get_result_feedback(result).lower()
    for gap in ("MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY",
                "PHYSICAL_FEASIBILITY", "PROBLEM_MECHANISM_FIT",
                "ASSUMPTION_INVENTORY", "EXPERTISE_GAP_AWARENESS", None):
        g = get_scaffolding_guidance(
            _warn(gap or "SOME_FUTURE_GAP", "asserted only — reasoning required"),
            gap_type=gap)
        assert _DETECTOR_HONEST_MARK not in g["lead"].lower(), gap


def test_rendered_asserted_page_shows_recognizer_explanation_once():
    # Integrated render: on a real ASSERTED WARN session page, the recognizer
    # explanation renders exactly once (primary line), the badge and raw
    # engine reason are unchanged, and the stored answer stays verbatim.
    sid = "ux-dup-once"
    state = IdeaState(idea_id="ux-dup-1")
    state.domain = "electronics_electrical"
    state.maturity_level = 1
    from engine.idea_state import Gap
    state.gaps.append(Gap(gap_type="MECHANISM_COMPLETENESS", status="OPEN", opened_at=1))
    last_result = _warn("MECHANISM_COMPLETENESS", "asserted only — reasoning required")
    transcript = [{"response": "It protects the wiring because overloads are dangerous.",
                   "iteration": 1}]
    _store(sid, state, last_result, transcript, "How does it work?")
    before_answer = copy.deepcopy(transcript)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert body.lower().count(_DETECTOR_HONEST_MARK) == 1
        assert "More detail needed" in body                    # badge unchanged
        assert "asserted only — reasoning required" in body     # raw reason preserved
        assert SESSION_STORE[sid]["transcript"] == before_answer
        assert SESSION_STORE[sid]["last_result"]["transition"] == "WARN"
    finally:
        SESSION_STORE.pop(sid, None)


def test_reasoning_bearing_answers_keep_classification_and_get_noncontradictory_feedback():
    from web.result_feedback import get_result_feedback
    result = _warn("MECHANISM_COMPLETENESS", "asserted only — reasoning required")
    lead = get_scaffolding_guidance(result, gap_type="MECHANISM_COMPLETENESS")["lead"].lower()
    primary = get_result_feedback(result).lower()
    for label, answer in _REASONING_BEARING_ASSERTED_EXAMPLES:
        # Remaining known false negatives: the recognizer (including the
        # Layer-2 connective gate) still classifies these ASSERTED.
        assert assess_response(answer, "electronics_electrical") == "ASSERTED", label
        # The visible feedback for the resulting state never claims the answer
        # lacks reasoning/mechanism/rationale. Detector-honesty lives ONCE in
        # the primary line; the lead is actionable-only (duplication removed).
        assert _DETECTOR_HONEST_MARK in primary, label
        assert _DETECTOR_HONEST_MARK not in lead, label
        for text in (lead, primary):
            for phrase in _FALSE_ABSENCE_PHRASES:
                assert phrase not in text, (label, phrase)


def test_connective_gate_recognizes_substance_bearing_rationale():
    # Layer-2 scoring correction (owner-authorized): a rationale clause that
    # carries whole-word domain substance after an authorized connective is
    # now REASONED. This does not weaken the ASSERTED-feedback truthfulness
    # protections above — it records the scoring-side reason the example was
    # moved out of the pinned-ASSERTED set.
    for label, answer in _CONNECTIVE_GATE_EXPECTED_REASONED_EXAMPLES:
        assert assess_response(answer, "electronics_electrical") == "REASONED", label


def test_primary_result_feedback_for_asserted_is_detector_honest():
    from web.result_feedback import get_result_feedback
    primary = get_result_feedback(
        {"transition": "WARN", "reason": "X asserted only — reasoning required"})
    low = primary.lower()
    assert _DETECTOR_HONEST_MARK in low
    for phrase in _FALSE_ABSENCE_PHRASES:
        assert phrase not in low, phrase
    for token in _INTERNAL_TOKENS:
        assert token not in low, token


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
        # No new persistence/schema keys introduced into the session record,
        # aside from the additive P4-1b-2a `answer_token` a render legitimately
        # stores (retained across renders; not epistemic/answer state).
        assert set(SESSION_STORE[sid].keys()) - {"answer_token"} == before_store_keys
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
