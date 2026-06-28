"""
Increment 1B — clarification display (deterministic, owner-invoked, display-only).

Proves the clarification disclosure is DETERMINISTIC EPHEMERAL SYSTEM GUIDANCE that
explains ONLY the current question: it is derived, per-gap-type, render-time,
web-display-only; it adds no owner action and no POST handling; it does not mutate
IdeaState, transcript, gaps, maturity, stage, gates, or selection; it never
introduces another question; and it does not depend on the frozen persistence
`tests/conftest.py` (these tests are hermetic).

Tests inspect observable behavior (the accessor's returned values and the rendered
session page), not private implementation details.
"""
import importlib
import inspect
import uuid

import pytest

from web.app import app, SESSION_STORE
from web.clarification_labels import get_clarification
from web.responsibility_labels import (
    get_responsibility,
    OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED,
)
from engine.idea_state import IdeaState, Gap, OPEN
from engine.progression_loop import select_next_gap, get_question

# Owner-approved canonical gap types and their stage (matches the 1B fixture).
GAPS = {
    "MECHANISM_COMPLETENESS": 2,
    "BOUNDARY_AMBIGUITY": 2,
    "PHYSICAL_FEASIBILITY": 2,
    "PROBLEM_MECHANISM_FIT": 3,
    "ASSUMPTION_INVENTORY": 3,
    "EXPERTISE_GAP_AWARENESS": 3,
}

CLAR_FIELDS = {"label", "plain_language", "information_needed", "answer_shape", "support_hint"}
SUMMARY = "Help me understand this question"
SYSTEM_TAG = "System guidance"

# Internal identifiers that must never appear in visible clarification text.
_FORBIDDEN_TOKENS = set(GAPS) | {
    OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED,
}


def _session_with_gap(gap_type, stage):
    """Deterministic in-memory session whose single open gap is gap_type."""
    st = IdeaState(idea_id="clar-" + uuid.uuid4().hex[:8])
    st.domain = "electronics_electrical"
    st.current_stage = stage
    st.gaps.append(Gap(gap_type=gap_type, status=OPEN, opened_at=0))
    sid = "clar-" + uuid.uuid4().hex
    SESSION_STORE[sid] = {"state": st, "last_result": None, "transcript": []}
    return sid, st


def _intake_session():
    """A no-gap intake session: select_next_gap()==None but a question shows."""
    st = IdeaState(idea_id="clar-intake-" + uuid.uuid4().hex[:6])
    st.domain = "electronics_electrical"
    st.maturity_level = 0
    sid = "clar-" + uuid.uuid4().hex
    SESSION_STORE[sid] = {
        "state": st, "transcript": [],
        "last_result": {"transition": "WARN", "reason": "core problem not yet established"},
    }
    return sid, st


def _snap(st):
    return {
        "iteration": st.iteration, "maturity": st.maturity_level,
        "stage": getattr(st, "current_stage", None), "path": getattr(st, "path", None),
        "gaps": [(g.gap_type, g.status, g.iterations_open) for g in st.gaps],
        "ack": len(getattr(st, "acknowledged_unknowns", [])),
        "kp": None if st.known_problem is None else st.known_problem.quality,
        "km": repr(st.known_mechanism),
        "direction": getattr(st, "direction", None),
    }


def _clar_visible_text(clar):
    return " ".join(clar[k] for k in CLAR_FIELDS)


# 1. All six canonical gap types return deterministic clarification.
@pytest.mark.parametrize("gap_type", list(GAPS))
def test_each_gap_returns_deterministic_clarification(gap_type):
    a = get_clarification(gap_type)
    b = get_clarification(gap_type)
    assert set(a.keys()) == CLAR_FIELDS
    assert a == b  # deterministic


# 2. All five responsibility categories are represented (four via canonical gaps,
#    UNDETERMINED via the unlisted/None fallback), each with clarification content.
def test_all_responsibility_categories_have_clarification():
    seen = {get_responsibility(g)["responsibility"] for g in GAPS}
    assert seen == {OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE}
    assert get_responsibility("NOT_A_GAP")["responsibility"] == UNDETERMINED
    # Every category's representative gap (and the fallback) yields clarification.
    for g in list(GAPS) + ["NOT_A_GAP"]:
        assert set(get_clarification(g).keys()) == CLAR_FIELDS


# 3. Clarification fields are non-empty plain-language strings.
@pytest.mark.parametrize("gap_type", list(GAPS) + ["NOT_A_GAP", None])
def test_fields_nonempty_plain_language(gap_type):
    c = get_clarification(gap_type)
    for k in CLAR_FIELDS:
        assert isinstance(c[k], str) and c[k].strip()
    # No "?" in ANY visible field: the clarification explains the existing
    # question; it never poses a new one (all five visible fields covered).
    for k in CLAR_FIELDS:
        assert "?" not in c[k]


# 4. Unknown / unlisted input returns a safe fallback (no raise).
def test_unknown_input_returns_safe_fallback():
    c = get_clarification("TOTALLY_MADE_UP_GAP")
    assert set(c.keys()) == CLAR_FIELDS and all(c[k].strip() for k in CLAR_FIELDS)


# 5. Missing / None input returns a safe fallback (no raise).
def test_none_and_empty_input_return_safe_fallback():
    for gt in (None, ""):
        c = get_clarification(gt)
        assert set(c.keys()) == CLAR_FIELDS and all(c[k].strip() for k in CLAR_FIELDS)


# 6. Accessor returns a fresh object; mutation cannot leak between calls.
def test_accessor_returns_fresh_object_no_mutation_leak():
    a = get_clarification("MECHANISM_COMPLETENESS")
    a["plain_language"] = "MUTATED"
    b = get_clarification("MECHANISM_COMPLETENESS")
    assert b["plain_language"] != "MUTATED"


# 7. Each canonical session page shows the exact disclosure label.
@pytest.mark.parametrize("gap_type,stage", list(GAPS.items()))
def test_page_shows_exact_disclosure_label(gap_type, stage):
    sid, st = _session_with_gap(gap_type, stage)
    try:
        assert select_next_gap(st) == gap_type
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert SUMMARY in body
    finally:
        SESSION_STORE.pop(sid, None)


# 8. Disclosure renders after the original question and before responsibility guidance.
def test_disclosure_after_question_before_responsibility():
    sid, st = _session_with_gap("MECHANISM_COMPLETENESS", 2)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        r = get_responsibility("MECHANISM_COMPLETENESS")
        qi = body.index('<p class="question">')
        di = body.index(SUMMARY)
        ri = body.index(r["label"])
        assert qi < di < ri
    finally:
        SESSION_STORE.pop(sid, None)


# 9. The original question remains present on the page.
def test_original_question_remains_visible():
    sid, st = _session_with_gap("PHYSICAL_FEASIBILITY", 2)
    try:
        q = get_question(st.domain, "PHYSICAL_FEASIBILITY", 0, path=getattr(st, "path", None))
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert '<p class="question">' in body and q in body
    finally:
        SESSION_STORE.pop(sid, None)


# 10. Visible "System guidance" classification is present in the disclosure.
def test_system_guidance_classification_present():
    sid, st = _session_with_gap("BOUNDARY_AMBIGUITY", 2)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert SYSTEM_TAG in body
    finally:
        SESSION_STORE.pop(sid, None)


# 11. No-gap intake page shows no clarification disclosure.
def test_no_gap_intake_has_no_clarification():
    sid, st = _intake_session()
    try:
        assert select_next_gap(st) is None
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert "Describe your invention in more detail" in body  # intake question shown
        assert SUMMARY not in body
        assert SYSTEM_TAG not in body
    finally:
        SESSION_STORE.pop(sid, None)


# 12. All six Increment 1A action controls remain present.
def test_six_owner_actions_remain_present():
    sid, st = _session_with_gap("MECHANISM_COMPLETENESS", 2)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert body.count('name="action"') == 6
        for val in ("answered", "unknown", "deferred", "provisional_assumption",
                    "specialist_requested", "evidence_requested"):
            assert f'value="{val}"' in body
    finally:
        SESSION_STORE.pop(sid, None)


# 13. ANSWERED remains the checked default.
def test_answered_remains_default_checked():
    sid, st = _session_with_gap("EXPERTISE_GAP_AWARENESS", 3)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert 'value="answered" checked' in body
    finally:
        SESSION_STORE.pop(sid, None)


# 14. Clarification introduces no seventh action and no form control.
def test_clarification_introduces_no_seventh_action():
    sid, st = _session_with_gap("PROBLEM_MECHANISM_FIT", 3)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert body.count('name="action"') == 6
        # The disclosure block (summary..</details>) carries no form controls.
        start = body.index(SUMMARY)
        end = body.index("</details>", start)
        block = body[start:end]
        assert "<input" not in block and "<textarea" not in block and "<button" not in block
        assert 'name="action"' not in block
    finally:
        SESSION_STORE.pop(sid, None)


# 15. Repeated GETs are stable (same clarification, no drift).
def test_repeated_gets_stable():
    sid, st = _session_with_gap("ASSUMPTION_INVENTORY", 3)
    try:
        c = app.test_client()
        b1 = c.get(f"/session/{sid}").get_data(as_text=True)
        b2 = c.get(f"/session/{sid}").get_data(as_text=True)
        clar = get_clarification("ASSUMPTION_INVENTORY")
        for k in CLAR_FIELDS:
            assert clar[k] in b1 and clar[k] in b2
    finally:
        SESSION_STORE.pop(sid, None)


# 16-20. Rendering clarification does not mutate IdeaState / transcript / selection.
def test_render_does_not_mutate_state_transcript_or_selection():
    sid, st = _session_with_gap("MECHANISM_COMPLETENESS", 2)
    try:
        before = _snap(st)
        sel_before = select_next_gap(st)
        q_before = get_question(st.domain, sel_before, 0, path=getattr(st, "path", None))
        entry = SESSION_STORE[sid]
        app.test_client().get(f"/session/{sid}")
        app.test_client().get(f"/session/{sid}")  # repeated GET also inert
        assert _snap(st) == before                       # iteration/maturity/stage/path/gaps...
        assert entry["transcript"] == []                 # no transcript append
        assert "interaction_actions" not in entry        # no interaction metadata
        assert not hasattr(st, "clarification")          # no IdeaState field added
        assert select_next_gap(st) == sel_before         # selection unchanged
        assert get_question(st.domain, sel_before, 0, path=getattr(st, "path", None)) == q_before
    finally:
        SESSION_STORE.pop(sid, None)


# 21. One-shot acknowledgement still appears once and clears, with clarification present both GETs.
def test_one_shot_ack_still_correct_with_clarification():
    sid, st = _session_with_gap("MECHANISM_COMPLETENESS", 2)
    try:
        SESSION_STORE[sid]["_interaction_ack"] = "Recorded as deferred. The question remains open and unresolved."
        c = app.test_client()
        b1 = c.get(f"/session/{sid}").get_data(as_text=True)
        b2 = c.get(f"/session/{sid}").get_data(as_text=True)
        assert "Recorded as deferred" in b1            # ack shown once
        assert "Recorded as deferred" not in b2        # one-shot cleared
        assert SUMMARY in b1 and SUMMARY in b2          # clarification remains available
    finally:
        SESSION_STORE.pop(sid, None)


# 22. No cross-session leakage: each session renders its own gap's clarification.
def test_no_cross_session_leakage():
    sid1, _ = _session_with_gap("PHYSICAL_FEASIBILITY", 2)
    sid2, _ = _session_with_gap("EXPERTISE_GAP_AWARENESS", 3)
    try:
        c = app.test_client()
        b1 = c.get(f"/session/{sid1}").get_data(as_text=True)
        b2 = c.get(f"/session/{sid2}").get_data(as_text=True)
        assert get_clarification("PHYSICAL_FEASIBILITY")["plain_language"] in b1
        assert get_clarification("EXPERTISE_GAP_AWARENESS")["plain_language"] in b2
        assert get_clarification("EXPERTISE_GAP_AWARENESS")["plain_language"] not in b1
    finally:
        SESSION_STORE.pop(sid1, None)
        SESSION_STORE.pop(sid2, None)


# 23-25. No persistence / filesystem / LLM / external-service dependency in the module.
def test_no_persistence_io_or_llm_dependency():
    mod = importlib.import_module("web.clarification_labels")
    src = inspect.getsource(mod)
    # The module is pure data + one accessor: it imports nothing and makes no I/O,
    # persistence, or external/LLM call. Check executable patterns (not docstring
    # prose, which describes what the module deliberately does NOT do).
    code_lines = [
        ln for ln in src.splitlines()
        if ln.strip() and not ln.lstrip().startswith("#")
    ]
    code = "\n".join(code_lines)
    assert "\nimport " not in ("\n" + code) and "\nfrom " not in ("\n" + code)
    for forbidden in ("session_store", "open(", "json.dump", "json.load",
                      "os.replace", "requests.", "urllib", "subprocess", "socket("):
        assert forbidden not in code
    # The accessor truly defines no module-level imports and no callables beyond
    # get_clarification.
    assert [n for n in dir(mod) if callable(getattr(mod, n)) and not n.startswith("_")] == ["get_clarification"]
    import web.app as webapp
    assert not hasattr(webapp, "session_store")


# 26. No JavaScript is required by the disclosure (native <details>).
def test_no_javascript_required():
    sid, st = _session_with_gap("MECHANISM_COMPLETENESS", 2)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        start = body.index(SUMMARY)
        block = body[start - 200:start + 1400]
        assert "<details" in block and "<summary" in block
        assert "<script" not in body
        assert "onclick" not in block
    finally:
        SESSION_STORE.pop(sid, None)


# 27. Visible clarification text contains no internal enum names.
@pytest.mark.parametrize("gap_type", list(GAPS) + ["NOT_A_GAP", None])
def test_visible_text_contains_no_internal_enum_names(gap_type):
    text = _clar_visible_text(get_clarification(gap_type))
    for token in _FORBIDDEN_TOKENS:
        assert token not in text


# 28. Existing Increment 1B responsibility block and Increment 1A actions still render.
def test_responsibility_and_actions_unchanged_on_page():
    sid, st = _session_with_gap("EXPERTISE_GAP_AWARENESS", 3)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        r = get_responsibility("EXPERTISE_GAP_AWARENESS")
        assert r["label"] in body and r["guidance"] in body   # 1B responsibility intact
        assert body.count('name="action"') == 6               # 1A actions intact
    finally:
        SESSION_STORE.pop(sid, None)


# 29. Fallback visible text lists no internal owner-action value and does not
#     enumerate a partial action menu (all six actions stay available, neutrally).
def test_fallback_lists_no_internal_action_value_or_partial_menu():
    action_values = ("answered", "unknown", "deferred", "provisional_assumption",
                     "specialist_requested", "evidence_requested")
    for gt in ("TOTALLY_MADE_UP_GAP", None, ""):
        text = _clar_visible_text(get_clarification(gt)).lower()
        for v in action_values:
            assert v not in text                       # no internal action value
        assert "available actions" in text             # neutral, not a partial list


# 30. PROBLEM_MECHANISM_FIT clarification promises no system analysis/examination
#     (this increment is display-only; no analysis capability is implemented).
def test_problem_fit_makes_no_system_analysis_claim():
    text = _clar_visible_text(get_clarification("PROBLEM_MECHANISM_FIT")).lower()
    for forbidden in ("the system can", "system will", "system can help",
                      "examine the relationship", "analyze", "analyse"):
        assert forbidden not in text
