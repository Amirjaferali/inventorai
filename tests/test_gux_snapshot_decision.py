"""G-UX-SNAPSHOT-DECISION — post-output Keep/Refine decision experience (Option A).

Behavioral RED->GREEN tests via Flask test_client. An eligible deliverable gains a
truthful output-review decision section offering exactly two accepted actions:
  - "Refine this idea"  (primary) -> returns to the SAME guided session (same sid)
  - "Keep current snapshot" (secondary) -> a meaningful POST that sets a temporary,
    per-sid acknowledgement (no durable save, no IdeaState/transcript mutation).

RED against base 722cf1c: the decision section, both exact labels, the Keep POST
route, and the truthful temporary-session acknowledgement are all absent; the
existing generic "Back to session" link does not satisfy the accepted behavior.

In-memory sessions only; no real server/port; no durable file. No existing test is
modified.
"""

import re

from web.app import app, SESSION_STORE
from engine.idea_state import IdeaState, Evidence, REASONED

KEEP_LABEL = "Keep current snapshot"
REFINE_LABEL = "Refine this idea"
_SID = "gux-snapshot-decision-sid"


def _eligible_state(idea_id):
    s = IdeaState(idea_id=idea_id)
    s.domain = "electronics_electrical"
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 2
    s.known_problem = Evidence("Clear problem statement", REASONED, 0)
    s.known_mechanism = Evidence("ESP32 TMP117 mechanism", REASONED, 0)
    return s


def _seed(sid):
    SESSION_STORE[sid] = {"state": _eligible_state(sid), "last_result": None, "transcript": []}


def _snapshot(entry):
    s = entry["state"]
    return {
        "maturity": s.maturity_level,
        "iteration": getattr(s, "iteration", None),
        "gaps": len(s.gaps),
        "transcript": len(entry.get("transcript") or []),
        "interactions": len(getattr(s, "interactions", []) or []) if hasattr(s, "interactions") else None,
        "last_result": entry.get("last_result"),
        "problem": getattr(getattr(s, "known_problem", None), "content", None),
        "mechanism": getattr(getattr(s, "known_mechanism", None), "content", None),
    }


def _deliverable_body(sid):
    return app.test_client().get(f"/session/{sid}/deliverable").get_data(as_text=True)


# ------------------------------------------------------------------ RED -> GREEN

def test_eligible_deliverable_has_both_exact_labels():
    _seed(_SID)
    try:
        body = _deliverable_body(_SID)
        assert "FDC-001 Deliverable" in body, "precondition: deliverable must be eligible"
        assert KEEP_LABEL in body, "eligible deliverable must offer Keep current snapshot"
        assert REFINE_LABEL in body, "eligible deliverable must offer Refine this idea"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_keep_post_route_exists_and_is_meaningful():
    _seed(_SID)
    try:
        r = app.test_client().post(f"/session/{_SID}/keep-snapshot")
        assert r.status_code == 302, "Keep must be a meaningful POST (Post/Redirect/Get), not 404/405"
        assert r.headers.get("Location", "").endswith(f"/session/{_SID}/deliverable"), \
            "Keep must redirect back to the same deliverable (same sid)"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_keep_shows_truthful_temporary_acknowledgement():
    _seed(_SID)
    try:
        c = app.test_client()
        body = c.post(f"/session/{_SID}/keep-snapshot", follow_redirects=True).get_data(as_text=True)
        low = body.lower()
        assert "temporary session" in low, "acknowledgement must state the temporary-session boundary"
        assert "not" in low and ("permanently saved" in low or "not been permanently saved" in low), \
            "acknowledgement must truthfully say it has not been permanently saved"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_decision_section_states_working_snapshot_not_saved():
    _seed(_SID)
    try:
        low = _deliverable_body(_SID).lower()
        assert "working snapshot" in low, "decision framing must call the output a working snapshot"
        assert "not been permanently saved" in low or "not permanently saved" in low, \
            "decision framing must say it has not been permanently saved"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_refine_is_an_accepted_decision_to_same_session():
    _seed(_SID)
    try:
        body = _deliverable_body(_SID)
        # the Refine action links to the SAME guided session route with the same sid
        m = re.search(r'<a\b[^>]*href="/session/' + re.escape(_SID) + r'"[^>]*>(.*?)</a>', body, re.DOTALL)
        assert m and REFINE_LABEL in re.sub(r"<[^>]+>", "", m.group(1)), \
            "Refine this idea must be an explicit link to the same guided session (same sid)"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_back_to_session_link_alone_does_not_satisfy():
    # The existing generic Back to session link exists but is NOT the decision action.
    _seed(_SID)
    try:
        body = _deliverable_body(_SID)
        assert "Back to session" in body, "existing Back to session link preserved"
        # base has Back-to-session but neither decision label; GREEN adds the labels.
        assert KEEP_LABEL in body and REFINE_LABEL in body, \
            "the generic Back to session link does not satisfy the accepted decision behavior"
    finally:
        SESSION_STORE.pop(_SID, None)


# --------------------------------------------------------- focused GREEN checks

def test_exactly_one_primary_action():
    _seed(_SID)
    try:
        body = _deliverable_body(_SID)
        m = re.search(r'<section\b[^>]*class="[^"]*decision[^"]*".*?</section>', body, re.DOTALL)
        assert m, "a decision section must exist"
        sec = m.group(0)
        primaries = re.findall(r'class="[^"]*\bdecision-primary\b[^"]*"', sec)
        assert len(primaries) == 1, "exactly one action is visually primary"
        # the primary is Refine (recommended hierarchy)
        prim = re.search(r'<[^>]*class="[^"]*decision-primary[^"]*"[^>]*>(.*?)</a>', sec, re.DOTALL)
        assert prim and REFINE_LABEL in re.sub(r"<[^>]+>", "", prim.group(1)), "Refine is the primary action"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_controls_are_semantic_and_keyboard_operable():
    _seed(_SID)
    try:
        body = _deliverable_body(_SID)
        # Refine = semantic <a href>; Keep = semantic <button type=submit> inside a POST form
        assert re.search(r'<a\b[^>]*href="/session/' + re.escape(_SID) + r'"', body), "Refine is a semantic link"
        assert re.search(r'<form\b[^>]*method="POST"[^>]*action="/session/' + re.escape(_SID) + r'/keep-snapshot"', body) \
            or re.search(r'<form\b[^>]*action="/session/' + re.escape(_SID) + r'/keep-snapshot"[^>]*method="POST"', body), \
            "Keep is a POST form"
        assert re.search(r'<button\b[^>]*type="submit"[^>]*>\s*Keep current snapshot\s*</button>', body), \
            "Keep is a semantic submit button"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_one_h1_preserved_and_unique_ids():
    _seed(_SID)
    try:
        body = _deliverable_body(_SID)
        assert body.count("<h1") == 1, "exactly one h1 preserved"
        ids = re.findall(r'\bid="([^"]+)"', body)
        assert len(ids) == len(set(ids)), f"all ids unique; dupes: {[i for i in ids if ids.count(i)>1]}"
    finally:
        SESSION_STORE.pop(_SID, None)


# --------------------------------------------------------- determinism & safety

def test_keep_does_not_mutate_deterministic_state_or_transcript():
    _seed(_SID)
    try:
        before = _snapshot(SESSION_STORE[_SID])
        app.test_client().post(f"/session/{_SID}/keep-snapshot")
        after = _snapshot(SESSION_STORE[_SID])
        assert after == before, f"Keep must not mutate IdeaState/iteration/maturity/gaps/evidence/transcript/last_result: {before} -> {after}"
        assert (SESSION_STORE[_SID].get("transcript") or []) == [], "Keep writes no transcript"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_keep_ack_is_single_use_transient():
    _seed(_SID)
    try:
        c = app.test_client()
        c.post(f"/session/{_SID}/keep-snapshot", follow_redirects=True)  # ack shown, consumed
        again = c.get(f"/session/{_SID}/deliverable").get_data(as_text=True).lower()
        assert "current working snapshot selected" not in again, \
            "the Keep acknowledgement must be a single-use transient, not persisted across later GETs"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_keep_marker_does_not_leak_across_sids():
    _seed(_SID)
    other = "gux-snapshot-other-sid"
    _seed(other)
    try:
        app.test_client().post(f"/session/{_SID}/keep-snapshot")  # sets marker on _SID only
        other_body = app.test_client().get(f"/session/{other}/deliverable").get_data(as_text=True).lower()
        assert "current working snapshot selected" not in other_body, "Keep marker must be namespaced to its own sid"
        assert "_snapshot_kept_ack" not in SESSION_STORE.get(other, {}), "no cross-session marker leak"
    finally:
        SESSION_STORE.pop(_SID, None)
        SESSION_STORE.pop(other, None)


def test_keep_missing_session_is_generic():
    SESSION_STORE.pop("no-such-sid", None)
    r = app.test_client().post("/session/no-such-sid/keep-snapshot")
    assert r.status_code == 302 and r.headers.get("Location", "").endswith("/"), \
        "Keep on a missing session must use the generic redirect to / (no existence disclosure)"


def test_no_overclaim_or_durable_language():
    _seed(_SID)
    try:
        low = (_deliverable_body(_SID)
               + app.test_client().post(f"/session/{_SID}/keep-snapshot", follow_redirects=True).get_data(as_text=True)).lower()
        for forbidden in ("permanently saved.", "version history", "account", "sign in", "approved and",
                          "restore", "download pdf", "email delivery"):
            # allow the truthful negations ("not been permanently saved", "not ... approved")
            pass
        for banned in ("version history", "saved projects", "your account", "restored", "download pdf", "email delivery"):
            assert banned not in low, f"decision experience must not introduce {banned!r}"
    finally:
        SESSION_STORE.pop(_SID, None)


# --------------------------------------------------------- preservation invariants

def test_existing_deliverable_content_preserved():
    _seed(_SID)
    try:
        body = _deliverable_body(_SID)
        assert "FDC-001 Deliverable" in body
        assert "Back to session" in body
        assert "Define or edit success criteria" in body
    finally:
        SESSION_STORE.pop(_SID, None)


def test_missing_session_deliverable_generic_redirect():
    SESSION_STORE.pop("gone", None)
    r = app.test_client().get("/session/gone/deliverable")
    assert r.status_code == 302 and r.headers.get("Location", "").endswith("/")
