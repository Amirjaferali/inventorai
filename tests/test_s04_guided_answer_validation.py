"""G-UX-ANSWER-VALIDATION — Guided-question empty-answer validation experience.

Behavioral RED->GREEN tests via Flask test_client on a seeded in-memory session.

Defect (base 6b37512): POST action="answered" with a whitespace-normalized empty
response silently redirects to the same session page with no visible error, no
programmatic association, and no focus. GREEN adds a single-use transient error,
associated with #response and conditionally focused, with no engine/state change.

No real server/port; no durable file; session seeded in-memory using the same
pattern as tests/test_web_app.py; no application code is modified by the tests.
"""

import re

from web.app import app, SESSION_STORE
from engine.idea_state import (
    IdeaState, Evidence, REASONED, Gap, PARTIAL, CLOSED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)

_SID = "gux-answer-validation-sid"
ERROR_MSG = "Enter an answer, or choose one of the response options below."


def _seed_session(sid):
    s = IdeaState(idea_id=sid)
    s.domain = "electronics_electrical"
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 1
    s.current_stage = 2
    s.known_problem = Evidence("existing systems miss micro-faults", REASONED, 1)
    s.known_mechanism = Evidence(
        "voltage drop across the shunt resistor triggers the comparator", REASONED, 2)
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=1, closed_at=2))
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=CLOSED, opened_at=3, closed_at=4))
    s.gaps.append(Gap(gap_type=BOUNDARY_AMBIGUITY, status=PARTIAL, opened_at=5))
    s.iteration = 5
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": [], "last_question": "Q"}


def _snapshot(entry):
    s = entry["state"]
    return (s.iteration, s.maturity_level, len(s.gaps),
            len(entry.get("transcript") or []),
            len(getattr(s, "interactions", []) or []) if hasattr(s, "interactions") else None)


# ------------------------------------------------------------------ RED -> GREEN

def test_empty_answered_shows_error_once():
    _seed_session(_SID)
    try:
        c = app.test_client()
        r = c.post(f"/session/{_SID}", data={"response": "", "action": "answered"},
                   follow_redirects=True)
        assert r.status_code == 200
        body = r.get_data(as_text=True)
        assert body.count(ERROR_MSG) == 1, "exact error must render exactly once after empty answered submit"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_whitespace_only_answered_shows_error():
    _seed_session(_SID)
    try:
        c = app.test_client()
        r = c.post(f"/session/{_SID}", data={"response": "   \t  ", "action": "answered"},
                   follow_redirects=True)
        assert ERROR_MSG in r.get_data(as_text=True), "whitespace-only answer must be treated as empty"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_error_element_id_and_aria_association():
    _seed_session(_SID)
    try:
        c = app.test_client()
        body = c.post(f"/session/{_SID}", data={"response": "", "action": "answered"},
                      follow_redirects=True).get_data(as_text=True)
        # exactly one error element with a stable id and role=alert
        errs = re.findall(r'<[a-z0-9]+\b[^>]*\bid="answer-error"[^>]*>', body)
        assert len(errs) == 1, "exactly one error element with id=answer-error"
        assert 'role="alert"' in errs[0], "error element must have role=alert"
        # the answer textarea references it via aria-describedby
        ta = [t for t in re.findall(r"<textarea\b[^>]*>", body) if 'id="response"' in t]
        assert len(ta) == 1, "exactly one id=response textarea"
        assert 'aria-describedby="answer-error"' in ta[0], "textarea must associate the error"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_conditional_autofocus_on_error():
    _seed_session(_SID)
    try:
        c = app.test_client()
        body = c.post(f"/session/{_SID}", data={"response": "", "action": "answered"},
                      follow_redirects=True).get_data(as_text=True)
        ta = [t for t in re.findall(r"<textarea\b[^>]*>", body) if 'id="response"' in t][0]
        assert "autofocus" in ta, "textarea must autofocus on the validation-error render"
    finally:
        SESSION_STORE.pop(_SID, None)


# --------------------------------------------------------- transient lifecycle

def test_error_consumed_once_not_repeated_on_refresh():
    _seed_session(_SID)
    try:
        c = app.test_client()
        c.post(f"/session/{_SID}", data={"response": "", "action": "answered"},
               follow_redirects=True)  # error rendered here (transient consumed)
        refreshed = c.get(f"/session/{_SID}").get_data(as_text=True)
        assert ERROR_MSG not in refreshed, "consumed error must not reappear on a later plain GET"
        assert 'id="answer-error"' not in refreshed, "no error element on a normal load"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_no_aria_or_autofocus_on_normal_load():
    _seed_session(_SID)
    try:
        body = app.test_client().get(f"/session/{_SID}").get_data(as_text=True)
        ta = [t for t in re.findall(r"<textarea\b[^>]*>", body) if 'id="response"' in t][0]
        assert "aria-describedby" not in ta, "no dangling aria-describedby on normal load"
        assert "autofocus" not in ta, "no autofocus on normal load"
        assert 'id="answer-error"' not in body, "no error element on normal load"
    finally:
        SESSION_STORE.pop(_SID, None)


# --------------------------------------------------------- non-triggering paths

def test_non_answer_action_does_not_trigger_error():
    _seed_session(_SID)
    try:
        c = app.test_client()
        body = c.post(f"/session/{_SID}", data={"response": "", "action": "deferred"},
                      follow_redirects=True).get_data(as_text=True)
        assert ERROR_MSG not in body, "a valid non-answer option must not show the answer-required error"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_valid_answer_shows_no_error():
    _seed_session(_SID)
    try:
        c = app.test_client()
        body = c.post(f"/session/{_SID}",
                      data={"response": "It uses a shunt resistor and comparator to detect the fault current.",
                            "action": "answered"}, follow_redirects=True).get_data(as_text=True)
        assert ERROR_MSG not in body, "a valid non-empty answer must not show the error"
    finally:
        SESSION_STORE.pop(_SID, None)


# --------------------------------------------------------- state preservation

def test_empty_answered_changes_no_state_and_no_transcript():
    _seed_session(_SID)
    try:
        before = _snapshot(SESSION_STORE[_SID])
        app.test_client().post(f"/session/{_SID}", data={"response": "", "action": "answered"})
        after = _snapshot(SESSION_STORE[_SID])
        assert after == before, "empty answered submit must not change iteration/maturity/gaps/transcript/interactions"
        assert (SESSION_STORE[_SID].get("transcript") or []) == [], "no transcript entry for an empty answer"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_empty_answered_redirects_302():
    _seed_session(_SID)
    try:
        r = app.test_client().post(f"/session/{_SID}", data={"response": "", "action": "answered"})
        assert r.status_code == 302 and r.headers.get("Location", "").endswith(f"/session/{_SID}"), \
            "empty answered must still Post/Redirect/Get to the same session page"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_error_does_not_echo_submitted_content():
    _seed_session(_SID)
    try:
        # even a non-empty-but-whitespace payload must not be echoed; the message is a constant
        body = app.test_client().post(f"/session/{_SID}", data={"response": "  \n ", "action": "answered"},
                                      follow_redirects=True).get_data(as_text=True)
        # the rendered error region contains only the constant message
        m = re.search(r'<[a-z0-9]+\b[^>]*\bid="answer-error"[^>]*>(.*?)</[a-z0-9]+>', body, re.DOTALL)
        assert m and m.group(1).strip() == ERROR_MSG, "error must render only the constant message, not user content"
    finally:
        SESSION_STORE.pop(_SID, None)


# --------------------------------------------------------- preservation invariants

def test_preserved_answer_controls_intact():
    _seed_session(_SID)
    try:
        body = app.test_client().get(f"/session/{_SID}").get_data(as_text=True)
        assert '<label for="response"' in body and "Your answer" in body, "answer label preserved"
        assert '<p class="question">' in body, "question paragraph preserved"
        assert "<fieldset" in body and "How do you want to respond?" in body, "response fieldset/legend preserved"
        for v in ("answered", "unknown", "deferred", "provisional_assumption",
                  "specialist_requested", "evidence_requested"):
            assert f'value="{v}"' in body, f"radio value {v} preserved"
        assert re.search(r'<button[^>]*>\s*Submit\s*</button>', body), "Submit CTA preserved"
        assert body.count("<h1") == 1, "one h1 preserved"
        assert body.count('id="response"') == 1, "exactly one id=response"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_missing_session_generic_redirect_unchanged():
    SESSION_STORE.pop("no-such", None)
    r = app.test_client().post("/session/no-such", data={"response": "", "action": "answered"})
    assert r.status_code == 302 and r.headers.get("Location", "").endswith("/"), \
        "unavailable session retains the generic redirect to /"
