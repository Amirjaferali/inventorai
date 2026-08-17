"""Plain-Language Result Feedback — Increment Contract PR #155.

Proves the display-only increment:
  * friendly plain-language feedback is the PRIMARY visible feedback line;
  * the raw engine/scoring `last_result.reason` is preserved byte-for-byte and
    shown only as non-primary provenance (collapsed <details>);
  * the truthful WARN/PASS/BLOCK badge and failed criteria are preserved;
  * scaffolding guidance and the existing WARN-detection substrings still work;
  * scoring / transitions / gaps / maturity / transcript / deliverable / report /
    domain gate are unchanged; saved answers stay verbatim; Answer Clarification
    inactive; Safety Signals closed; six honest actions; no forbidden claims.
"""

import copy
from test_p4_1b2a_durable_answer_append import answered_post  # P4-1b-2a
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.app import app, SESSION_STORE, UNSUPPORTED_DOMAIN_MESSAGE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from web.result_feedback import get_result_feedback  # noqa: E402
from web.scaffolding_guidance import get_scaffolding_guidance  # noqa: E402
import engine.progression_loop as _progression_loop  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402
from engine.safety_signal import derive_inventor_stated_safety_signals  # noqa: E402

# The exact pinned friendly strings (contract section 10; the asserted-only
# string was corrected by the owner-gated feedback-truthfulness correction —
# the superseded string implied a reasoning deficiency the recognizer cannot
# actually establish).
_WARN_ASSERTED = (
    "The current demo did not recognize enough explicit reasoning structure in "
    "your answer to move this area forward yet. Making the cause-and-effect "
    "relationship more explicit may help."
)
_WARN_PARTIAL = "You addressed part of this, but more detail is still needed."
_PASS_DEMO = "This point is supported well enough to move forward in the current demo flow."
_PASS_REASONED = "Your follow-up added enough reasoning to continue in the current demo flow."
_NOT_ESTABLISHED = "This point is not established yet, so the idea cannot move forward on this item."
# Semantic WARN corrections (independent-review defect fix).
_MVP_CAP = "This point has reached the highest maturity level supported by the current MVP demo."
_SEQUENCING = "An earlier required step needs to be addressed first before this can move forward."
_REASONED_MINIMUM = "This needs more reasoning or supporting detail before it can move forward."
_GENERIC_WARN = "This point cannot move forward yet. Review the result details for the specific reason."

_FORBIDDEN_CLAIM_WORDS = (
    "production-ready", "production ready", "validated", "safe to build",
    "compliant", "compliance", "feasible", "feasibility", "patent",
    "certified", "approved", "guaranteed", "verified",
)
_FORBIDDEN_FIELDS = (
    "suggested_clarified_answer", "user_approved_answer",
    "original_user_answer", "clarification_status",
)


def _start(idea="ESP32 microcontroller circuit with a voltage sensor and relay"):
    return app.test_client().post(
        "/start", data={"idea": idea, "domain_confirm": DOMAIN_CONFIRM_VALUE})


def _session():
    r = _start()
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _force(sid, transition, reason, direction=None):
    e = SESSION_STORE[sid]
    e["last_result"] = {"transition": transition, "reason": reason, "direction": direction}


def _body(sid):
    return app.test_client().get(f"/session/{sid}").get_data(as_text=True)


def _primary_reason(body):
    m = re.search(r'class="reason-text"[^>]*>(.*?)</div>', body, re.S)
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------------------
# Pure helper — category coverage, safe defaults, purity
# ---------------------------------------------------------------------------

def test_helper_covers_all_pinned_categories():
    assert get_result_feedback({"transition": "WARN", "reason": "X asserted only — reasoning required"}) == _WARN_ASSERTED
    assert get_result_feedback({"transition": "WARN", "reason": "X partially addressed — needs more depth"}) == _WARN_PARTIAL
    assert get_result_feedback({"transition": "PASS", "reason": "X closed with DEMONSTRATED evidence"}) == _PASS_DEMO
    assert get_result_feedback({"transition": "PASS", "reason": "X closed after REASONED follow-up"}) == _PASS_REASONED
    assert get_result_feedback({"transition": "BLOCK", "reason": "BLOCK: X not yet closed"}) == _NOT_ESTABLISHED


def test_helper_initial_or_no_result_renders_nothing():
    assert get_result_feedback(None) is None
    assert get_result_feedback({}) is None
    assert get_result_feedback("not a dict") is None
    assert get_result_feedback({"transition": None, "reason": ""}) is None


def test_helper_degrades_safely_for_unknown_reason_without_false_success():
    # Unknown / future WARN reason -> conservative generic fallback that does NOT
    # invent the cause, does NOT claim "not established", and never a success.
    out = get_result_feedback({"transition": "WARN", "reason": "some unexpected reason"})
    assert out == _GENERIC_WARN
    assert out != _NOT_ESTABLISHED
    assert out not in (_PASS_DEMO, _PASS_REASONED)
    # Generic maturity-advance PASS -> truthful supportive PASS, never over-claim.
    out2 = get_result_feedback({"transition": "PASS", "reason": "Problem established — ready for LEVEL 1"})
    assert out2 == _PASS_DEMO


def test_semantic_warn_categories_are_faithful():
    # Independent-review defect fix: distinct live WARN reasons must NOT all
    # collapse to "not established".
    # 1. MVP maturity cap must NOT say the point is unestablished.
    mvp = get_result_feedback({"transition": "WARN", "reason": "LEVEL 2 is max for MVP"})
    assert mvp == _MVP_CAP
    assert mvp != _NOT_ESTABLISHED
    assert "not established" not in mvp.lower()
    # 2. Sequencing / prerequisite not attempted.
    seq = get_result_feedback({"transition": "WARN", "reason": "MECHANISM_COMPLETENESS must be attempted first"})
    assert seq == _SEQUENCING
    assert seq != _NOT_ESTABLISHED
    # 3. Reasoned-evidence minimum not met.
    rmin = get_result_feedback({"transition": "WARN", "reason": "Mechanism quality must be REASONED minimum"})
    assert rmin == _REASONED_MINIMUM
    assert rmin != _NOT_ESTABLISHED
    # 4. Genuine not-established reasons still map to the approved not-established string.
    for r in ("Problem not yet established", "Mechanism not established",
              "BLOCK: MECHANISM_COMPLETENESS not yet closed",
              "BLOCK: PHYSICAL_FEASIBILITY not yet opened",
              "BLOCK: PHYSICAL_FEASIBILITY not yet closed (status: OPEN)"):
        assert get_result_feedback({"transition": "WARN", "reason": r}) == _NOT_ESTABLISHED


def test_semantic_warn_strings_have_no_forbidden_claims():
    for s in (_MVP_CAP, _SEQUENCING, _REASONED_MINIMUM, _GENERIC_WARN):
        low = s.lower()
        for w in _FORBIDDEN_CLAIM_WORDS:
            assert w not in low, (w, s)


def test_mvp_cap_renders_dedicated_message_in_session_ui():
    sid = _session()
    try:
        _force(sid, "WARN", "LEVEL 2 is max for MVP")
        b = _body(sid)
        assert _primary_reason(b) == _MVP_CAP
        assert "not established" not in (_primary_reason(b) or "").lower()
        assert "More detail needed" in b                      # WARN badge preserved
        assert "LEVEL 2 is max for MVP" in b                  # raw reason still in provenance
        assert 'class="reason-raw"' in b
    finally:
        SESSION_STORE.pop(sid, None)


def test_helper_is_pure_no_forbidden_imports():
    from web import result_feedback as mod
    src = open(mod.__file__, encoding="utf-8").read()
    for forbidden in ("import engine", "safety_signal", "score_case",
                      "session_store", "run_iteration", "integrate_response",
                      "import requests", "open("):
        assert forbidden not in src, forbidden


def test_friendly_strings_contain_no_forbidden_claim_words():
    for s in (_WARN_ASSERTED, _WARN_PARTIAL, _PASS_DEMO, _PASS_REASONED, _NOT_ESTABLISHED):
        low = s.lower()
        for w in _FORBIDDEN_CLAIM_WORDS:
            assert w not in low, (w, s)


# ---------------------------------------------------------------------------
# Rendered session page — friendly primary, raw provenance, truthful badge
# ---------------------------------------------------------------------------

def test_friendly_feedback_is_primary_and_raw_token_not_primary():
    sid = _session()
    try:
        _force(sid, "WARN", "MECHANISM_COMPLETENESS asserted only — reasoning required")
        body = _body(sid)
        assert _primary_reason(body) == _WARN_ASSERTED
        assert "MECHANISM_COMPLETENESS" not in (_primary_reason(body) or "")
    finally:
        SESSION_STORE.pop(sid, None)


def test_raw_reason_preserved_byte_for_byte_and_shown_as_provenance():
    sid = _session()
    raw = "MECHANISM_COMPLETENESS asserted only — reasoning required"
    try:
        _force(sid, "WARN", raw)
        before = SESSION_STORE[sid]["last_result"]["reason"]
        body = _body(sid)
        # raw reason unchanged in state after render
        assert SESSION_STORE[sid]["last_result"]["reason"] == before == raw
        # raw reason available as non-primary provenance (collapsed <details>)
        assert "<details" in body and 'class="reason-raw"' in body
        assert raw in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_warn_badge_visible():
    sid = _session()
    try:
        _force(sid, "WARN", "X asserted only — reasoning required")
        assert "More detail needed" in _body(sid)
    finally:
        SESSION_STORE.pop(sid, None)


def test_pass_badge_visible():
    sid = _session()
    try:
        _force(sid, "PASS", "X closed with DEMONSTRATED evidence")
        b = _body(sid)
        assert "Good progress" in b
        assert _primary_reason(b) == _PASS_DEMO
    finally:
        SESSION_STORE.pop(sid, None)


def test_block_badge_visible():
    sid = _session()
    try:
        _force(sid, "BLOCK", "BLOCK: X not yet closed")
        b = _body(sid)
        assert "Not enough to continue" in b
        assert _primary_reason(b) == _NOT_ESTABLISHED
    finally:
        SESSION_STORE.pop(sid, None)


def test_direction_and_gaps_still_visible():
    sid = _session()
    try:
        _force(sid, "WARN", "X partially addressed — needs more depth", direction="Add the mechanism")
        b = _body(sid)
        assert "Direction: Add the mechanism" in b
        # gap board / open gap surfaces preserved
        assert "gap" in b.lower()
    finally:
        SESSION_STORE.pop(sid, None)


def test_scaffolding_guidance_still_triggers_on_warn():
    sid = _session()
    try:
        _force(sid, "WARN", "MECHANISM_COMPLETENESS asserted only — reasoning required")
        b = _body(sid)
        assert 'class="scaffolding-guidance"' in b            # panel still renders
        # and the pure scaffolding helper still maps the same raw reason
        g = get_scaffolding_guidance(
            {"transition": "WARN", "reason": "MECHANISM_COMPLETENESS asserted only — reasoning required"},
            gap_type="MECHANISM_COMPLETENESS")
        assert g is not None
    finally:
        SESSION_STORE.pop(sid, None)


def test_six_honest_actions_unchanged():
    sid = _session()
    try:
        _force(sid, "WARN", "X asserted only — reasoning required")
        assert _body(sid).count('name="action"') == 6
    finally:
        SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# Verbatim answers, no persistence of feedback, no forbidden fields/claims
# ---------------------------------------------------------------------------

def test_saved_answer_verbatim_and_feedback_not_persisted():
    sid = _session()
    answer = "The ESP32 reads the voltage sensor and opens a relay above 5V."
    try:
        answered_post(app.test_client(), sid, {"response": answer, "action": "answered"})
        tx = SESSION_STORE[sid]["transcript"]
        assert tx and tx[-1]["response"] == answer            # verbatim
        stored = " ".join(r.get("response", "") for r in tx)
        for s in (_WARN_ASSERTED, _WARN_PARTIAL, _PASS_DEMO, _PASS_REASONED, _NOT_ESTABLISHED):
            assert s not in stored                            # feedback never persisted
    finally:
        SESSION_STORE.pop(sid, None)


def test_no_forbidden_fields_and_no_forbidden_claims_in_page():
    sid = _session()
    try:
        _force(sid, "PASS", "X closed with DEMONSTRATED evidence")
        b = _body(sid)
        state = SESSION_STORE[sid]["state"]
        for f in _FORBIDDEN_FIELDS:
            assert not hasattr(state, f)
            assert f not in b
        # friendly primary line makes no readiness/validation/safety/patent claim
        primary = (_primary_reason(b) or "").lower()
        for w in _FORBIDDEN_CLAIM_WORDS:
            assert w not in primary, w
    finally:
        SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# Engine / scoring / persistence / deliverable / domain-gate untouched
# ---------------------------------------------------------------------------

def test_render_does_not_change_scoring_transition_gaps_or_maturity():
    sid = _session()
    try:
        app.test_client().post(f"/session/{sid}", data={"response": "I don't know", "action": "unknown"})
        state = SESSION_STORE[sid]["state"]
        before_mat = state.maturity_level
        before_gaps = [(g.gap_type, g.status) for g in state.gaps]
        before_result = copy.deepcopy(SESSION_STORE[sid].get("last_result"))
        _body(sid); _body(sid)
        assert state.maturity_level == before_mat
        assert [(g.gap_type, g.status) for g in state.gaps] == before_gaps
        assert SESSION_STORE[sid].get("last_result") == before_result
    finally:
        SESSION_STORE.pop(sid, None)


def test_engine_raw_reason_strings_unchanged_upstream():
    # The engine still PRODUCES the raw reason strings the display layer maps
    # FROM (source-level, so the friendly layer changed nothing upstream).
    src = open(_progression_loop.__file__, encoding="utf-8").read()
    for token in ('{gap_type} asserted only — reasoning required',
                  '{gap_type} partially addressed — needs more depth',
                  '{gap_type} closed with DEMONSTRATED evidence',
                  '{gap_type} closed after REASONED follow-up'):
        assert token in src, token


def test_deliverable_and_safety_and_domain_gate_unchanged(monkeypatch):
    # Pinned to the electronics-only activation state for the domain-gate
    # check below; mechanical is now really activated in production
    # (Mechanical Activation Execution Gate) and would legitimately admit a
    # gearbox idea via its own confirmation.
    from engine import domain_activation
    monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS",
                         frozenset({"electronics_electrical"}))
    sid = _session()
    try:
        state = SESSION_STORE[sid]["state"]
        pkg = assemble_deliverable(state)
        assert len([k for k in pkg if k.startswith("section_")]) == 14
        assert "_session_meta" in pkg
        assert isinstance(derive_inventor_stated_safety_signals(state), tuple)
    finally:
        SESSION_STORE.pop(sid, None)
    # domain gate still rejects unsupported ideas
    before = set(SESSION_STORE)
    r = _start("a gearbox with a rotating shaft and meshing gears")
    assert r.status_code == 200 and UNSUPPORTED_DOMAIN_MESSAGE in r.get_data(as_text=True)
    assert set(SESSION_STORE) == before
