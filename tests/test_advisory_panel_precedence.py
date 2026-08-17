"""Advisory Panel Precedence — Supportive Surface Consolidation — implementation tests.

Governed by
`docs/governance/ADVISORY_PANEL_PRECEDENCE_SUPPORTIVE_SURFACE_CONSOLIDATION_INCREMENT_CONTRACT.md`
(true-merged via PR #141) and its scope decision (PR #139). Proves the
display-only, render-time, state-specific, reversible-by-state precedence among
the three competing OPEN advisory panels — Guided Uncertainty Support, More
Detail Needed scaffolding, and Guided Answer Co-Authoring — so that at most one
renders as primary per state (uncertainty > scaffolding[WARN] > co-authoring),
without hiding any truthful state and without removing, degrading, duplicating,
or persistently disabling any surface.

Tests assert rendered-output behavior (panel presence/absence), not internals.
They are written to FAIL on the prior stacked-panel behavior and PASS only after
the template precedence guards are applied.
"""
import copy
from test_p4_1b2a_durable_answer_append import answered_post  # P4-1b-2a
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import app, SESSION_STORE, UNSUPPORTED_DOMAIN_MESSAGE, DOMAIN_CONFIRM_VALUE, select_next_gap  # noqa: E402
from web.responsibility_labels import get_responsibility  # noqa: E402
from web.answer_coauthoring_prompts import get_answer_coauthoring_prompts  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402
from engine.safety_signal import derive_inventor_stated_safety_signals  # noqa: E402

# Stable class markers for the three competing OPEN advisory panels.
_SCAFFOLDING = 'class="scaffolding-guidance"'
_UNCERTAINTY = 'class="uncertainty-guidance"'
_COAUTHORING = 'class="answer-coauthoring"'
# On-demand / truthful surface markers.
_CLARIFICATION = "Help me understand this question"
_WARN_BADGE = "More detail needed"

_FORBIDDEN_FIELDS = (
    "suggested_clarified_answer", "user_approved_answer",
    "original_user_answer", "clarification_status",
)


def _warn(reason="MECHANISM_COMPLETENESS asserted only — reasoning required"):
    return {"transition": "WARN", "reason": reason, "direction": "STALLED"}


def _start(idea, confirm=True):
    data = {"idea": idea}
    if confirm:
        data["domain_confirm"] = DOMAIN_CONFIRM_VALUE
    return app.test_client().post("/start", data=data, follow_redirects=False)


def _start_electronics_session():
    resp = _start("ESP32 microcontroller circuit with a voltage sensor")
    assert resp.status_code == 302
    return resp.headers["Location"].rsplit("/", 1)[-1]


def _primary_panels(body):
    """Return which competing OPEN advisory panels are present in the render."""
    out = []
    if _UNCERTAINTY in body:
        out.append("uncertainty")
    if _SCAFFOLDING in body:
        out.append("scaffolding")
    if _COAUTHORING in body:
        out.append("coauthoring")
    return out


def _force(sid, last_result=None, last_response=None):
    """Test-only in-memory override of the render signals (no production change).

    Sets the already-existing `last_result` and last transcript response on the
    in-memory session entry so a specific render state can be exercised. This
    mutates only the ephemeral test session store, exactly as existing render
    tests do; it changes no production code, scoring, schema, or persistence.
    """
    entry = SESSION_STORE[sid]
    if last_result is not None:
        entry["last_result"] = last_result
    if last_response is not None:
        entry["transcript"] = [{"response": last_response, "iteration": 1}]


# ---------------------------------------------------------------------------
# Precedence — exactly one primary panel per state
# ---------------------------------------------------------------------------

def test_uncertainty_state_uncertainty_is_sole_primary():
    # Uncertainty via the non-scoring "I do not know this yet" action (no WARN).
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": "I don't know", "action": "unknown"})
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _primary_panels(body) == ["uncertainty"]  # co-authoring suppressed
    finally:
        SESSION_STORE.pop(sid, None)


def test_arabic_uncertainty_state_uncertainty_is_sole_primary():
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": "لا أعرف", "action": "unknown"})
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _primary_panels(body) == ["uncertainty"]
    finally:
        SESSION_STORE.pop(sid, None)


def test_arabic_uncertainty_suppresses_scaffolding_and_coauthoring_and_is_rtl():
    # Arabic / RTL Supportive Response (contract PR #148): even in a WARN state,
    # Arabic uncertainty is the SOLE primary panel (scaffolding and co-authoring
    # suppressed as competing open primaries) and the panel is RTL — while the
    # page shell stays LTR/en. The one-primary-panel precedence is unchanged.
    sid = _start_electronics_session()
    try:
        _force(sid, last_result=_warn(), last_response="لا أعرف")
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _primary_panels(body) == ["uncertainty"]
        assert 'dir="rtl"' in body and body.count('dir="rtl"') == 1
        assert '<html lang="en">' in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_uncertainty_wins_over_warn_scaffolding():
    # Both drivers present (WARN + uncertainty text): uncertainty is sole primary,
    # scaffolding advisory panel is suppressed — but the truthful WARN badge stays.
    sid = _start_electronics_session()
    try:
        _force(sid, last_result=_warn(), last_response="I don't know")
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _primary_panels(body) == ["uncertainty"]
        assert _WARN_BADGE in body  # truthful WARN state NOT hidden
    finally:
        SESSION_STORE.pop(sid, None)


def test_warn_not_uncertain_scaffolding_is_sole_primary():
    sid = _start_electronics_session()
    try:
        _force(sid, last_result=_warn(),
               last_response="the plug senses current and cuts power")
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _primary_panels(body) == ["scaffolding"]  # co-authoring suppressed
        assert _WARN_BADGE in body
    finally:
        SESSION_STORE.pop(sid, None)


def _pass():
    return {"transition": "PASS", "reason": "ok", "direction": "PROGRESSING"}


def test_non_warn_non_uncertainty_state_coauthoring_is_sole_primary():
    # Reversibility: in a non-WARN (PASS), non-uncertainty state with an open
    # question, co-authoring is the sole primary advisory panel. (A freshly
    # started session is legitimately already in a WARN state, so scaffolding is
    # primary there; this exercises the reversible non-WARN case.)
    sid = _start_electronics_session()
    try:
        _force(sid, last_result=_pass(),
               last_response="it opens a relay when current exceeds a threshold")
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _primary_panels(body) == ["coauthoring"]
    finally:
        SESSION_STORE.pop(sid, None)


def test_exactly_one_primary_panel_in_every_exercised_state():
    sid = _start_electronics_session()
    try:
        # fresh
        b = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert len(_primary_panels(b)) == 1
        # uncertainty
        _force(sid, last_result=_warn(), last_response="I don't know")
        b = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert len(_primary_panels(b)) == 1
        # WARN not-uncertain
        _force(sid, last_result=_warn(), last_response="it opens a relay at 5V")
        b = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert len(_primary_panels(b)) == 1
    finally:
        SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# On-demand / truthful surfaces preserved
# ---------------------------------------------------------------------------

def test_clarification_remains_collapsed_on_demand():
    sid = _start_electronics_session()
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _CLARIFICATION in body           # available
        assert "<details" in body               # collapsed/on-demand, not an open panel
    finally:
        SESSION_STORE.pop(sid, None)


def test_responsibility_truthful_content_preserved():
    sid = _start_electronics_session()
    try:
        gap_type = select_next_gap(SESSION_STORE[sid]["state"])
        resp = get_responsibility(gap_type) if gap_type else None
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert resp is not None
        assert resp["label"] in body            # responsibility not removed
        assert resp["guidance"] in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_coauthoring_not_removed_renders_primary_in_non_uncertainty_non_warn_state():
    sid = _start_electronics_session()
    try:
        _force(sid, last_result=_pass(),
               last_response="it opens a relay when current exceeds a threshold")
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        # Capability preserved: the co-authoring panel and its unchanged helper
        # heading both render as primary in a non-uncertainty / non-WARN state.
        assert _COAUTHORING in body
        assert get_answer_coauthoring_prompts(select_next_gap(SESSION_STORE[sid]["state"]))["heading"] in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_truthful_warn_badge_visible_when_scaffolding_panel_suppressed():
    sid = _start_electronics_session()
    try:
        _force(sid, last_result=_warn(), last_response="I don't know")
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _SCAFFOLDING not in body   # advisory scaffolding panel suppressed
        assert _WARN_BADGE in body        # truthful WARN indicator preserved
    finally:
        SESSION_STORE.pop(sid, None)


def test_truthful_gap_progress_and_interaction_ack_visible():
    sid = _start_electronics_session()
    try:
        # gap-progress list renders from the truthful state.
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert "gap-row" in body
        # interaction acknowledgement renders after a non-answer action.
        app.test_client().post(f"/session/{sid}",
                               data={"response": "", "action": "deferred"})
        body2 = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert "badge-warn" in body2
    finally:
        SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# Boundaries — actions, provenance, schema, safety, domain
# ---------------------------------------------------------------------------

def test_six_honest_actions_unchanged_no_seventh():
    sid = _start_electronics_session()
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert body.count('name="action"') == 6
        for v in ("answered", "unknown", "deferred", "provisional_assumption",
                  "specialist_requested", "evidence_requested"):
            assert f'value="{v}"' in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_saved_answer_verbatim_and_guidance_not_persisted():
    sid = _start_electronics_session()
    answer = "The ESP32 reads the voltage sensor and opens a relay above 5V."
    try:
        answered_post(app.test_client(), sid, {"response": answer, "action": "answered"})
        tx = SESSION_STORE[sid]["transcript"]
        assert tx[-1]["response"] == answer
    finally:
        SESSION_STORE.pop(sid, None)


def test_render_does_not_change_maturity_gaps_or_outcome():
    sid = _start_electronics_session()
    _force(sid, last_result=_warn(), last_response="I don't know")
    state = SESSION_STORE[sid]["state"]
    before_maturity = state.maturity_level
    before_gaps = [(g.gap_type, g.status) for g in state.gaps]
    before_result = copy.deepcopy(SESSION_STORE[sid].get("last_result"))
    try:
        app.test_client().get(f"/session/{sid}")
        app.test_client().get(f"/session/{sid}")
        assert state.maturity_level == before_maturity
        assert [(g.gap_type, g.status) for g in state.gaps] == before_gaps
        assert SESSION_STORE[sid].get("last_result") == before_result
    finally:
        SESSION_STORE.pop(sid, None)


def test_no_forbidden_answer_clarification_fields():
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": "I don't know", "action": "unknown"})
        app.test_client().get(f"/session/{sid}")
        state = SESSION_STORE[sid]["state"]
        for f in _FORBIDDEN_FIELDS:
            assert not hasattr(state, f)
            assert f not in SESSION_STORE[sid]
    finally:
        SESSION_STORE.pop(sid, None)


def test_safety_signals_surface_unchanged():
    sid = _start_electronics_session()
    try:
        state = SESSION_STORE[sid]["state"]
        assert isinstance(derive_inventor_stated_safety_signals(state), tuple)
        pkg = assemble_deliverable(state)
        assert "inventor_stated_safety_signals" in pkg["_session_meta"]
        assert len([k for k in pkg if k.startswith("section_")]) == 14
    finally:
        SESSION_STORE.pop(sid, None)


def test_domain_gate_holds_electronics_only(monkeypatch):
    # Pinned to the electronics-only activation state this file's scope is
    # about; mechanical is now really activated in production (Mechanical
    # Activation Execution Gate) and would legitimately admit the gearbox
    # idea via its own confirmation — out of scope for this test file.
    from engine import domain_activation
    monkeypatch.setattr(domain_activation, "_ACTIVATED_DOMAINS",
                         frozenset({"electronics_electrical"}))
    before = set(SESSION_STORE)
    resp = _start("a gearbox with a rotating shaft and bearing torque")
    assert resp.status_code == 200
    assert UNSUPPORTED_DOMAIN_MESSAGE in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before
    resp2 = _start("ESP32 microcontroller circuit with a voltage sensor")
    assert resp2.status_code == 302
    SESSION_STORE.pop(resp2.headers["Location"].rsplit("/", 1)[-1], None)
