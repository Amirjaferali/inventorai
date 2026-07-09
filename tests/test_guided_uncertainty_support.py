"""Guided Uncertainty Support — implementation tests.

Governed by
`docs/governance/GUIDED_UNCERTAINTY_SUPPORT_INCREMENT_CONTRACT.md` (PR #134) and
its scope decision
`docs/governance/INVENTOR_SUPPORTIVE_GUIDANCE_NON_EXAM_UX_SCOPE_DECISION.md`
(PR #132). Proves the new supportive, display-only surface:

  * English AND Arabic uncertainty inputs trigger supportive guidance; other
    text does not;
  * the guidance is optional/advisory/non-exam-like and makes no
    validation/safety/compliance/patent/engineering/readiness claim;
  * the helper is pure/deterministic and imports no engine/scoring/persistence/
    Safety-Signals modules;
  * the saved answer stays inventor-verbatim and guidance text never persists;
  * no forbidden Answer-Clarification field/flow, no save/approve/apply control,
    no hidden field, and no seventh session action are introduced;
  * scoring/readiness/maturity/criticality, Safety Signals, the Increment-6
    top-level contract, and the electronics/electrical MVP boundary are unchanged;
  * the Guided Answer Co-Authoring surface remains present and distinct.
"""
import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import app, SESSION_STORE, UNSUPPORTED_DOMAIN_MESSAGE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from web.uncertainty_guidance import get_uncertainty_guidance, is_uncertainty_text  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402
from engine.safety_signal import derive_inventor_stated_safety_signals  # noqa: E402

_EYEBROW = "Optional — no pressure"

_ENGLISH_UNCERTAIN = (
    "I don't know",
    "I'm not sure",
    "I don't understand the question",
    "I don't know the technical term",
    "I don't know how it works",
)
_ARABIC_UNCERTAIN = (
    "لا أعرف",
    "غير متأكد",
    "لا أفهم السؤال",
    "لا أعرف المصطلح التقني",
    "لا أعرف كيف تعمل",
)
_NOT_UNCERTAIN = (
    "The ESP32 reads the voltage sensor and opens a relay above 5V.",
    "It uses a Hall-effect sensor to detect current.",
    "",
    "   ",
)

_FORBIDDEN_CLAIM_WORDS = (
    "valid", "safe", "feasib", "compliance", "certif", "build-ready",
    "buildable", "patent", "ready to build", "verified", "proven",
    "correct", "complete", "engineering-ready", "patent-ready",
)
_FORBIDDEN_FIELDS = (
    "suggested_clarified_answer", "user_approved_answer",
    "original_user_answer", "clarification_status",
)


def _start(idea, confirm=True):
    data = {"idea": idea}
    if confirm:
        data["domain_confirm"] = DOMAIN_CONFIRM_VALUE
    return app.test_client().post("/start", data=data, follow_redirects=False)


def _start_electronics_session():
    resp = _start("ESP32 microcontroller circuit with a voltage sensor")
    assert resp.status_code == 302
    return resp.headers["Location"].rsplit("/", 1)[-1]


# ---------------------------------------------------------------------------
# Pure function — detection, determinism, safe structure
# ---------------------------------------------------------------------------

def test_english_uncertainty_triggers_guidance():
    for text in _ENGLISH_UNCERTAIN:
        g = get_uncertainty_guidance(text)
        assert g is not None, text
        assert is_uncertainty_text(text)


def test_arabic_uncertainty_triggers_guidance():
    for text in _ARABIC_UNCERTAIN:
        g = get_uncertainty_guidance(text)
        assert g is not None, text
        assert is_uncertainty_text(text)


def test_non_uncertainty_returns_none():
    for text in _NOT_UNCERTAIN:
        assert get_uncertainty_guidance(text) is None, text
    assert get_uncertainty_guidance(None) is None


def test_returns_only_safe_keys_and_list_of_str_prompts():
    g = get_uncertainty_guidance("I don't know")
    assert set(g.keys()) == {"heading", "prompts", "note"}
    assert isinstance(g["prompts"], list) and g["prompts"]
    assert all(isinstance(p, str) and p for p in g["prompts"])


def test_dict_has_no_forbidden_answer_clarification_fields():
    g = get_uncertainty_guidance("I'm not sure")
    for field in _FORBIDDEN_FIELDS:
        assert field not in g
        assert field not in " ".join(g["prompts"]).lower()
        assert field not in g["note"].lower()


def test_text_makes_no_validation_or_safety_or_readiness_claim():
    # Advisory CONTENT (heading + prompts) must assert no claim about the answer.
    # The note is guardrail text that REQUIRES negating validation/safety, so it
    # is checked separately.
    g = get_uncertainty_guidance("I don't know")
    content = (g["heading"] + " " + " ".join(g["prompts"])).lower()
    for forbidden in _FORBIDDEN_CLAIM_WORDS:
        assert forbidden not in content, forbidden
    note = g["note"].lower()
    assert "not validation" in note and "not safety" in note


def test_no_exam_like_wording():
    g = get_uncertainty_guidance("I don't know")
    blob = (g["heading"] + " " + " ".join(g["prompts"]) + " " + g["note"]).lower()
    for harsh in ("wrong", "failed", "insufficient", "incorrect", "you did not"):
        assert harsh not in blob, harsh


def test_deterministic_and_returns_fresh_mutable_copy():
    a = get_uncertainty_guidance("لا أعرف")
    b = get_uncertainty_guidance("لا أعرف")
    assert a == b
    a["prompts"].append("leak")
    assert "leak" not in get_uncertainty_guidance("لا أعرف")["prompts"]


def test_helper_is_pure_no_forbidden_imports():
    from web import uncertainty_guidance as mod
    src = open(mod.__file__, encoding="utf-8").read()
    for forbidden in ("import engine", "safety_signal", "assess_response",
                      "record_interaction", "session_store", "run_iteration",
                      "import requests", "open("):
        assert forbidden not in src, forbidden


# ---------------------------------------------------------------------------
# Rendered session page — supportive panel, distinct, additive
# ---------------------------------------------------------------------------

def test_panel_appears_for_uncertainty_via_unknown_action():
    # The "I do not know this yet" action never scores; the question is retained.
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": "I don't know", "action": "unknown"})
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _EYEBROW in body
        assert "one step at a time" in body.lower()
        assert "not validation" in body.lower() and "not safety" in body.lower()
    finally:
        SESSION_STORE.pop(sid, None)


def test_panel_appears_for_arabic_uncertainty():
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": "لا أعرف", "action": "unknown"})
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _EYEBROW in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_panel_absent_for_non_uncertainty_answer():
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}", data={
            "response": "It opens a relay when current exceeds a threshold.",
            "action": "unknown"})
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _EYEBROW not in body
    finally:
        SESSION_STORE.pop(sid, None)


def test_panel_has_no_hidden_field_or_save_approve_apply_control():
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": "I don't know", "action": "unknown"})
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        panel = body[body.index(_EYEBROW):]
        panel = panel[:panel.index("<form")] if "<form" in panel else panel
        low = panel.lower()
        for word in ("apply", "approve", "save clarified", "use this answer",
                     "input type=\"hidden\"", "rewrite"):
            assert word not in low, word
    finally:
        SESSION_STORE.pop(sid, None)


def test_no_seventh_session_action_radio_introduced():
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": "I don't know", "action": "unknown"})
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert body.count('name="action"') == 6
    finally:
        SESSION_STORE.pop(sid, None)


def test_saved_answer_is_verbatim_and_guidance_not_persisted():
    sid = _start_electronics_session()
    answer = "I don't know how the sensor triggers the relay yet."
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": answer, "action": "answered"})
        transcript = SESSION_STORE[sid]["transcript"]
        assert transcript, "an answered submission must be recorded"
        assert transcript[-1]["response"] == answer  # verbatim, byte-for-byte
        prompts = get_uncertainty_guidance("I don't know")["prompts"]
        stored = " ".join(r.get("response", "") for r in transcript)
        for p in prompts:
            assert p not in stored
        # Durable ledger holds only the verbatim answer, never guidance text.
        state = SESSION_STORE[sid]["state"]
        recorded = [getattr(a, "content", None) for a in getattr(state, "interactions", [])]
        if recorded:
            for p in prompts:
                assert p not in " ".join(c or "" for c in recorded)
    finally:
        SESSION_STORE.pop(sid, None)


def test_render_does_not_change_maturity_gaps_or_outcome():
    sid = _start_electronics_session()
    # Prime an uncertainty signal via the non-scoring unknown action.
    app.test_client().post(f"/session/{sid}",
                           data={"response": "I don't know", "action": "unknown"})
    state = SESSION_STORE[sid]["state"]
    before_maturity = state.maturity_level
    before_gaps = [(g.gap_type, g.status) for g in state.gaps]
    before_result = copy.deepcopy(SESSION_STORE[sid].get("last_result"))
    try:
        r1 = app.test_client().get(f"/session/{sid}")
        r2 = app.test_client().get(f"/session/{sid}")
        assert r1.status_code == 200 and r2.status_code == 200
        assert _EYEBROW in r1.get_data(as_text=True)
        assert state.maturity_level == before_maturity
        assert [(g.gap_type, g.status) for g in state.gaps] == before_gaps
        assert SESSION_STORE[sid].get("last_result") == before_result
    finally:
        SESSION_STORE.pop(sid, None)


def test_no_forbidden_fields_introduced_on_state_or_store():
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": "I don't know", "action": "unknown"})
        app.test_client().get(f"/session/{sid}")
        state = SESSION_STORE[sid]["state"]
        for field in _FORBIDDEN_FIELDS:
            assert not hasattr(state, field)
            assert field not in SESSION_STORE[sid]
    finally:
        SESSION_STORE.pop(sid, None)


def test_guided_answer_coauthoring_suppressed_in_uncertainty_but_not_removed():
    # Advisory Panel Precedence (Increment Contract PR #141) reconciliation: in the
    # uncertainty state, Guided Uncertainty Support is the primary advisory panel
    # and Guided Answer Co-Authoring is SUPPRESSED as a competing open primary
    # panel — it is NOT removed as a capability. The uncertainty panel and the
    # Increment 1B clarification expander remain present and distinct.
    _COAUTHORING_HEADING = "Optional: what you could include in your answer"
    sid = _start_electronics_session()
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": "I don't know", "action": "unknown"})
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _EYEBROW in body                              # uncertainty is primary
        assert _COAUTHORING_HEADING not in body             # co-authoring suppressed here
        assert "Help me understand this question" in body   # Increment 1B intact
    finally:
        SESSION_STORE.pop(sid, None)
    # Co-Authoring is NOT deleted or persistently disabled: it renders as primary
    # in a separate non-uncertainty / non-WARN (PASS) state.
    sid = _start_electronics_session()
    try:
        entry = SESSION_STORE[sid]
        entry["last_result"] = {"transition": "PASS", "reason": "ok",
                                "direction": "PROGRESSING"}
        entry["transcript"] = [{"response": "it opens a relay when current exceeds a threshold",
                                "iteration": 1}]
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _COAUTHORING_HEADING in body                 # co-authoring available/primary
        assert _EYEBROW not in body                          # uncertainty absent here
    finally:
        SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# Boundary regressions — MVP domain, Increment-6 contract, Safety Signals
# ---------------------------------------------------------------------------

def test_domain_gate_holds_electronics_only():
    before = set(SESSION_STORE)
    resp = _start("a gearbox with a rotating shaft and bearing torque")
    assert resp.status_code == 200
    assert UNSUPPORTED_DOMAIN_MESSAGE in resp.get_data(as_text=True)
    assert set(SESSION_STORE) == before

    resp2 = _start("ESP32 microcontroller circuit with a voltage sensor")
    assert resp2.status_code == 302
    SESSION_STORE.pop(resp2.headers["Location"].rsplit("/", 1)[-1], None)


def test_increment_6_toplevel_contract_intact():
    sid = _start_electronics_session()
    try:
        pkg = assemble_deliverable(SESSION_STORE[sid]["state"])
        section_keys = [k for k in pkg if k.startswith("section_")]
        assert len(section_keys) == 14
        assert "_session_meta" in pkg
        assert not any("uncertain" in k.lower() for k in pkg)
    finally:
        SESSION_STORE.pop(sid, None)


def test_safety_signals_surface_unchanged():
    sid = _start_electronics_session()
    try:
        state = SESSION_STORE[sid]["state"]
        assert isinstance(derive_inventor_stated_safety_signals(state), tuple)
        pkg = assemble_deliverable(state)
        assert "inventor_stated_safety_signals" in pkg["_session_meta"]
    finally:
        SESSION_STORE.pop(sid, None)
