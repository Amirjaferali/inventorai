"""Guided Answer Co-Authoring Increment 1 — Advisory Prompt Support — tests.

Governed by
`docs/governance/GUIDED_ANSWER_COAUTHORING_INCREMENT_CONTRACT.md` (PR #127) and
its scope decision `docs/governance/GUIDED_ANSWER_COAUTHORING_SCOPE_DECISION.md`
(PR #125). Proves the new display-only, deterministic advisory prompt surface:

  * offers OPTIONAL, category-level, content-free prompts for the current
    electronics/electrical question, visibly labeled advisory;
  * preserves the inventor as the sole author of any saved answer — the saved
    answer is the inventor's verbatim response and guidance never enters the
    transcript or the durable interaction ledger;
  * introduces no Answer-Clarification field/flow, no approval/save control, no
    new session action / seventh radio option, and no hidden form field;
  * makes no validation/safety/compliance/patent/engineering/readiness claim;
  * performs no I/O / LLM / persistence and mutates no input/state/transcript;
  * leaves scoring, maturity, readiness, criticality, the Increment-6 deliverable
    top-level contract, and the Safety Signals surface unchanged; and
  * keeps the existing Increment 1B clarification and More Detail Needed
    scaffolding surfaces present and distinct.
"""
import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from web.app import app, SESSION_STORE, UNSUPPORTED_DOMAIN_MESSAGE, DOMAIN_CONFIRM_VALUE  # noqa: E402
from web.answer_coauthoring_prompts import get_answer_coauthoring_prompts  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402
from engine.safety_signal import derive_inventor_stated_safety_signals  # noqa: E402

_HEADING = "Optional: what you could include in your answer"
_EYEBROW = "Optional guidance"

# Every committed gap_type used by the existing display-only surfaces.
_GAP_TYPES = (
    "MECHANISM_COMPLETENESS", "BOUNDARY_AMBIGUITY", "ASSUMPTION_INVENTORY",
    "PROBLEM_MECHANISM_FIT", "PHYSICAL_FEASIBILITY", "EXPERTISE_GAP_AWARENESS",
)

# Forbidden claim words that must never appear in advisory text (contract §7/§10).
_FORBIDDEN_CLAIM_WORDS = (
    "valid", "safe", "feasib", "compliance", "certif", "build-ready",
    "buildable", "patent", "ready to build", "verified", "proven",
    "correct", "complete", "engineering-ready", "patent-ready",
)
# Forbidden Answer-Clarification / Improve-Wording field names (contract §7).
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
# Pure function — deterministic, content-free, safe structure
# ---------------------------------------------------------------------------

def test_returns_only_safe_keys_and_list_of_str_prompts():
    for gap_type in _GAP_TYPES + (None, "SOMETHING_UNKNOWN"):
        g = get_answer_coauthoring_prompts(gap_type)
        assert set(g.keys()) == {"heading", "prompts", "note"}
        assert isinstance(g["prompts"], list) and g["prompts"]
        assert all(isinstance(p, str) and p for p in g["prompts"])


def test_dict_has_no_forbidden_answer_clarification_fields():
    g = get_answer_coauthoring_prompts("MECHANISM_COMPLETENESS")
    for field in _FORBIDDEN_FIELDS:
        assert field not in g
        assert field not in " ".join(g["prompts"]).lower()
        assert field not in g["note"].lower()


def test_text_makes_no_validation_or_safety_or_readiness_claim():
    # The advisory CONTENT (heading + prompts) must assert no claim about the
    # answer. The note is guardrail text that is REQUIRED to NEGATE validation /
    # safety (contract §10), so it is checked separately (see the note test); the
    # naive claim-word scan must not run over its negations.
    for gap_type in _GAP_TYPES + (None,):
        g = get_answer_coauthoring_prompts(gap_type)
        text = (g["heading"] + " " + " ".join(g["prompts"])).lower()
        for forbidden in _FORBIDDEN_CLAIM_WORDS:
            assert forbidden not in text, f"forbidden claim word {forbidden!r} in {gap_type}"
        # The note only ever NEGATES these words ("not validation", "not safety");
        # it must never make a bare positive claim.
        note = g["note"].lower()
        assert "not validation" in note and "not safety" in note


def test_known_gap_types_yield_category_prompts():
    for gap_type in _GAP_TYPES:
        g = get_answer_coauthoring_prompts(gap_type)
        assert len(g["prompts"]) >= 2


def test_unknown_and_none_resolve_to_safe_fallback():
    fallback = get_answer_coauthoring_prompts(None)
    assert fallback == get_answer_coauthoring_prompts("NO_SUCH_GAP")
    assert fallback["prompts"]


def test_deterministic_and_returns_fresh_mutable_copy():
    a = get_answer_coauthoring_prompts("BOUNDARY_AMBIGUITY")
    b = get_answer_coauthoring_prompts("BOUNDARY_AMBIGUITY")
    assert a == b
    a["prompts"].append("leak")            # mutating the returned list ...
    assert "leak" not in get_answer_coauthoring_prompts("BOUNDARY_AMBIGUITY")["prompts"]


def test_note_states_optional_authorship_and_not_validation_or_safety():
    note = get_answer_coauthoring_prompts("MECHANISM_COMPLETENESS")["note"].lower()
    assert "optional" in note
    assert "your own" in note
    assert "not validation" in note
    assert "not safety" in note


def test_pure_call_does_not_perform_io_or_read_source_of_engine():
    # The module must not couple to the engine/safety surfaces. Assert its source
    # imports nothing from engine and never references safety/scoring modules.
    from web import answer_coauthoring_prompts as mod
    src = open(mod.__file__, encoding="utf-8").read()
    assert "import engine" not in src
    assert "safety_signal" not in src
    assert "assess_response" not in src
    assert "record_interaction" not in src


# ---------------------------------------------------------------------------
# Rendered session page — advisory panel, labeled, distinct, additive
# ---------------------------------------------------------------------------

def test_panel_appears_and_is_labeled_advisory_for_electronics_question():
    sid = _start_electronics_session()
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert _HEADING in body
        assert _EYEBROW in body
        assert "not validation" in body.lower()
        assert "not safety" in body.lower()
    finally:
        SESSION_STORE.pop(sid, None)


def test_panel_has_no_save_approve_apply_control_or_hidden_field():
    sid = _start_electronics_session()
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        panel = body[body.index(_HEADING):]
        panel = panel[:panel.index("<form")] if "<form" in panel else panel
        low = panel.lower()
        for word in ("apply", "approve", "save clarified", "use this answer",
                     "input type=\"hidden\""):
            assert word not in low
    finally:
        SESSION_STORE.pop(sid, None)


def test_no_seventh_session_action_radio_introduced():
    sid = _start_electronics_session()
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert body.count('name="action"') == 6
    finally:
        SESSION_STORE.pop(sid, None)


def test_saved_answer_is_verbatim_and_guidance_not_persisted():
    sid = _start_electronics_session()
    answer = "The ESP32 reads the voltage sensor and opens a relay above 5V."
    try:
        app.test_client().post(f"/session/{sid}",
                               data={"response": answer, "action": "answered"})
        transcript = SESSION_STORE[sid]["transcript"]
        assert transcript, "an answered submission must be recorded"
        assert transcript[-1]["response"] == answer  # verbatim, byte-for-byte
        # No advisory prompt text leaked into the durable record.
        prompts = get_answer_coauthoring_prompts("MECHANISM_COMPLETENESS")["prompts"]
        stored_blob = " ".join(r.get("response", "") for r in transcript)
        for p in prompts:
            assert p not in stored_blob
        # Durable IdeaState interaction ledger holds the verbatim answer only.
        state = SESSION_STORE[sid]["state"]
        recorded = [getattr(a, "content", None) for a in getattr(state, "interactions", [])]
        if recorded:
            assert answer in recorded
            for p in prompts:
                assert p not in " ".join(c or "" for c in recorded)
    finally:
        SESSION_STORE.pop(sid, None)


def test_render_does_not_change_maturity_gaps_or_outcome():
    sid = _start_electronics_session()
    state = SESSION_STORE[sid]["state"]
    before_maturity = state.maturity_level
    before_gaps = [(g.gap_type, g.status) for g in state.gaps]
    before_result = copy.deepcopy(SESSION_STORE[sid].get("last_result"))
    try:
        r1 = app.test_client().get(f"/session/{sid}")
        r2 = app.test_client().get(f"/session/{sid}")
        assert r1.status_code == 200 and r2.status_code == 200
        assert _HEADING in r1.get_data(as_text=True)
        assert state.maturity_level == before_maturity
        assert [(g.gap_type, g.status) for g in state.gaps] == before_gaps
        assert SESSION_STORE[sid].get("last_result") == before_result
    finally:
        SESSION_STORE.pop(sid, None)


def test_no_forbidden_fields_introduced_on_state_or_store():
    sid = _start_electronics_session()
    try:
        app.test_client().get(f"/session/{sid}")
        state = SESSION_STORE[sid]["state"]
        for field in _FORBIDDEN_FIELDS:
            assert not hasattr(state, field)
            assert field not in SESSION_STORE[sid]
    finally:
        SESSION_STORE.pop(sid, None)


def test_existing_surfaces_present_and_distinct():
    # Increment 1B "Help me understand this question" expander remains; the new
    # advisory co-authoring panel is a separate, distinctly-labeled surface.
    sid = _start_electronics_session()
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert "Help me understand this question" in body   # Increment 1B intact
        assert _HEADING in body                             # new surface present
        assert _EYEBROW in body                             # distinctly labeled
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
    assert set(SESSION_STORE) == before  # no session for unsupported domain

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
        # No top-level co-authoring section leaked into the deliverable.
        assert not any("coauthor" in k.lower() for k in pkg)
    finally:
        SESSION_STORE.pop(sid, None)


def test_safety_signals_surface_unchanged():
    sid = _start_electronics_session()
    try:
        state = SESSION_STORE[sid]["state"]
        # Safety Signals derivation still callable and returns a tuple (read-only).
        assert isinstance(derive_inventor_stated_safety_signals(state), tuple)
        # Deliverable still carries the safety block under _session_meta only.
        pkg = assemble_deliverable(state)
        assert "inventor_stated_safety_signals" in pkg["_session_meta"]
    finally:
        SESSION_STORE.pop(sid, None)
