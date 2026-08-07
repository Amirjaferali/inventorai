"""
Increment 1B — responsibility guidance (Option E: label + one guidance sentence).

Proves the ADVISORY responsibility guidance WITHOUT changing any epistemic
semantics: it is derived, per-gap-type, web-display-only; it does not mutate
IdeaState or transcript, does not auto-select/constrain an Increment 1A action,
and never implies a specialist has already answered or that evidence exists.

Tests inspect observable behavior (the accessor's returned values and the
rendered session page), not private implementation details.
"""
import importlib
import uuid

import pytest

from web.app import app, SESSION_STORE
from web.responsibility_labels import (
    get_responsibility,
    OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT, EMPIRICAL_EVIDENCE, UNDETERMINED,
)
from engine.idea_state import IdeaState, Gap, OPEN
from engine.progression_loop import select_next_gap

# Owner-approved initial mapping (committed gap-type identifiers).
MAPPING = {
    "MECHANISM_COMPLETENESS": (OWNER_INPUT, 2),
    "BOUNDARY_AMBIGUITY": (OWNER_INPUT, 2),
    "PHYSICAL_FEASIBILITY": (EMPIRICAL_EVIDENCE, 2),
    "PROBLEM_MECHANISM_FIT": (SYSTEM_ANALYSIS, 3),
    "ASSUMPTION_INVENTORY": (OWNER_INPUT, 3),
    "EXPERTISE_GAP_AWARENESS": (SPECIALIST_INPUT, 3),
}


def _session_with_gap(gap_type, stage):
    """Deterministic in-memory session whose single open gap is gap_type."""
    st = IdeaState(idea_id="1b-" + uuid.uuid4().hex[:8])
    st.domain = "electronics_electrical"
    st.current_stage = stage
    st.gaps.append(Gap(gap_type=gap_type, status=OPEN, opened_at=0))
    sid = "1b-" + uuid.uuid4().hex
    SESSION_STORE[sid] = {"state": st, "last_result": None, "transcript": []}
    return sid, st


def _snap(st):
    return {
        "iteration": st.iteration, "maturity": st.maturity_level,
        "gaps": [(g.gap_type, g.status) for g in st.gaps],
        "ack": len(getattr(st, "acknowledged_unknowns", [])),
        "kp": None if st.known_problem is None else st.known_problem.quality,
        "km": None if st.known_mechanism is None else st.known_mechanism.quality,
        "direction": getattr(st, "direction", None),
    }


# 1. Every active mapped gap type resolves to the expected approved value.
@pytest.mark.parametrize("gap_type,expected", {k: v[0] for k, v in MAPPING.items()}.items())
def test_mapping_resolves_to_approved_value(gap_type, expected):
    r = get_responsibility(gap_type)
    assert r["responsibility"] == expected
    assert r["responsibility"] in {OWNER_INPUT, SYSTEM_ANALYSIS, SPECIALIST_INPUT,
                                   EMPIRICAL_EVIDENCE, UNDETERMINED}
    assert r["label"] and r["guidance"]


# 2. Unknown / missing gap type resolves safely to UNDETERMINED (no raise).
def test_unknown_and_none_gap_type_is_undetermined():
    assert get_responsibility("NOT_A_GAP_TYPE")["responsibility"] == UNDETERMINED
    assert get_responsibility(None)["responsibility"] == UNDETERMINED
    assert get_responsibility("")["responsibility"] == UNDETERMINED


# 3+4. The responsibility label and guidance sentence render near the question.
def test_label_and_guidance_render_near_question():
    sid, st = _session_with_gap("MECHANISM_COMPLETENESS", 2)
    try:
        assert select_next_gap(st) == "MECHANISM_COMPLETENESS"  # precondition
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        r = get_responsibility("MECHANISM_COMPLETENESS")
        assert r["label"] in body
        assert r["guidance"] in body
        # rendered AFTER the question (near it), not at the top of the page.
        assert body.index('<p class="question"') < body.index(r["label"])
    finally:
        SESSION_STORE.pop(sid, None)


# 5. Specialist wording does not imply a specialist has already answered.
def test_specialist_wording_does_not_imply_already_answered():
    g = get_responsibility("EXPERTISE_GAP_AWARENESS")
    assert g["responsibility"] == SPECIALIST_INPUT
    low = g["guidance"].lower()
    for forbidden in ["has answered", "already answered", "specialist confirmed",
                      "reviewed by", "has been answered", "already reviewed"]:
        assert forbidden not in low
    assert "usually needs" in low and "request specialist input and continue" in low
    # And it renders that way on the page (Stage 3 EGA gap).
    sid, st = _session_with_gap("EXPERTISE_GAP_AWARENESS", 3)
    try:
        assert select_next_gap(st) == "EXPERTISE_GAP_AWARENESS"
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert "Specialist input may help" in body
    finally:
        SESSION_STORE.pop(sid, None)


# 6. Empirical-evidence wording does not imply evidence already exists.
def test_empirical_wording_does_not_imply_evidence_exists():
    g = get_responsibility("PHYSICAL_FEASIBILITY")
    assert g["responsibility"] == EMPIRICAL_EVIDENCE
    low = g["guidance"].lower()
    for forbidden in ["evidence shows", "evidence confirms", "has been tested",
                      "already tested", "test results show", "evidence exists",
                      "already have evidence"]:
        assert forbidden not in low
    assert "usually needs" in low and "request evidence and continue" in low
    sid, st = _session_with_gap("PHYSICAL_FEASIBILITY", 2)
    try:
        assert select_next_gap(st) == "PHYSICAL_FEASIBILITY"
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert "Evidence or a test may be needed" in body
    finally:
        SESSION_STORE.pop(sid, None)


# 7. Rendering the session page does not mutate IdeaState or transcript.
def test_render_does_not_mutate_state_or_transcript():
    sid, st = _session_with_gap("MECHANISM_COMPLETENESS", 2)
    try:
        before = _snap(st)
        entry = SESSION_STORE[sid]
        app.test_client().get(f"/session/{sid}")
        app.test_client().get(f"/session/{sid}")  # repeated GET also inert
        assert _snap(st) == before
        assert entry["transcript"] == []
        assert "interaction_actions" not in entry
        # IdeaState carries no Increment 1B responsibility attribute.
        assert not hasattr(st, "responsibility")
        assert not hasattr(st, "answer_responsibility")
    finally:
        SESSION_STORE.pop(sid, None)


# 8. All six Increment 1A action controls remain present.
def test_all_six_1a_actions_remain_present():
    sid, st = _session_with_gap("MECHANISM_COMPLETENESS", 2)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert body.count('name="action"') == 6
        for val in ("answered", "unknown", "deferred", "provisional_assumption",
                    "specialist_requested", "evidence_requested"):
            assert f'value="{val}"' in body
    finally:
        SESSION_STORE.pop(sid, None)


# 9. Guidance does not auto-select or constrain an action; ANSWERED stays default.
def test_guidance_does_not_autoselect_or_constrain_action():
    # Even for a SPECIALIST_INPUT gap, ANSWERED remains the default and all
    # actions remain available; the guidance block contains no input control.
    sid, st = _session_with_gap("EXPERTISE_GAP_AWARENESS", 3)
    try:
        body = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert 'value="answered" checked' in body
        assert body.count('name="action"') == 6
        # The responsibility guidance div is display-only (no form controls).
        start = body.index("Specialist input may help")
        block = body[start:start + 400]
        assert "<input" not in block and "checked" not in block
    finally:
        SESSION_STORE.pop(sid, None)


# 11. No engine.session_store import / no persistence behavior introduced.
def test_no_session_store_or_persistence_dependency():
    rl = importlib.import_module("web.responsibility_labels")
    import inspect
    src = inspect.getsource(rl)
    assert "session_store" not in src
    assert "open(" not in src and "json.dump" not in src and "os.replace" not in src
    import web.app as webapp
    assert not hasattr(webapp, "session_store")


# 12 (sanity). The accessor is pure: repeated calls are equal and create nothing.
def test_accessor_is_pure_and_total():
    for gt in list(MAPPING) + ["NOT_A_GAP_TYPE", None]:
        a = get_responsibility(gt)
        b = get_responsibility(gt)
        assert a == b
        assert set(a.keys()) == {"responsibility", "label", "guidance"}
