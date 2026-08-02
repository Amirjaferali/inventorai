"""G-UX-SHELL — Shared Application Shell & Accessibility/Disclosure Baseline.

Behavioral RED->GREEN tests for the shared shell across the four user-facing
journey templates (index, session, deliverable, success_criteria). RED against the
authorized base (94b6b9d): those pages have no shared shell — no viewport meta, no
<main> landmark, no skip-to-content link, and no persistent "Temporary session"
header disclosure. GREEN only after the shell refactor. All assertions exercise
rendered HTML via Flask test_client (not source grep). No real server or port is
opened; no durable file is created. No existing test is modified.

The disclosure implemented here is an intentional BASELINE only: the persistent
"Temporary session" text. The accepted "Learn more" / S15 deep-disclosure remains
deferred to a later separately authorized increment and is NOT implemented here.
"""

import re

from web.app import app, SESSION_STORE
from engine.idea_state import (
    IdeaState, Evidence, REASONED, Gap, PARTIAL, CLOSED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)

_SID = "gux-shell-baseline-sid"


def _seed_session(sid):
    # Mirrors the boundary-state seeding used by tests/test_web_app.py so the
    # session/deliverable/success-criteria routes render without invoking the engine
    # loop. In-memory only; nothing durable.
    s = IdeaState(idea_id=sid)
    s.domain = "electronics_electrical"
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 1
    s.current_stage = 2
    s.known_problem = Evidence("existing systems miss micro-faults", REASONED, 1)
    s.known_mechanism = Evidence(
        "voltage drop across the shunt resistor triggers the comparator", REASONED, 2
    )
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=1, closed_at=2))
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=CLOSED, opened_at=3, closed_at=4))
    s.gaps.append(Gap(gap_type=BOUNDARY_AMBIGUITY, status=PARTIAL, opened_at=5))
    s.iteration = 5
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": [], "last_question": "Q"}


def _render_journey_pages():
    client = app.test_client()
    _seed_session(_SID)
    try:
        return {
            "entry": client.get("/").get_data(as_text=True),
            "session": client.get(f"/session/{_SID}").get_data(as_text=True),
            "deliverable": client.get(f"/session/{_SID}/deliverable").get_data(as_text=True),
            "success": client.get(f"/session/{_SID}/success-criteria").get_data(as_text=True),
        }
    finally:
        SESSION_STORE.pop(_SID, None)


def _header_block(html):
    m = re.search(r"<header\b.*?</header>", html, re.DOTALL)
    return m.group(0) if m else ""


# ------------------------------------------------------------------ RED -> GREEN

def test_viewport_meta_present_once_on_every_journey_page():
    for key, html in _render_journey_pages().items():
        assert html.count('name="viewport"') == 1, f"{key}: expected exactly one viewport meta"


def test_main_landmark_present_on_every_journey_page():
    for key, html in _render_journey_pages().items():
        assert '<main id="main-content">' in html, f"{key}: missing <main> landmark"


def test_skip_link_points_to_main_target_on_every_journey_page():
    for key, html in _render_journey_pages().items():
        assert 'href="#main-content"' in html, f"{key}: missing skip-to-content link"
        assert "Skip to content" in html, f"{key}: missing skip-link text"


def test_persistent_temporary_session_disclosure_in_header():
    for key, html in _render_journey_pages().items():
        header = _header_block(html)
        assert header, f"{key}: no <header> region"
        assert "Temporary session" in header, f"{key}: persistent disclosure missing from header"


# --------------------------------------------------------- preservation invariants
# (pass both before and after the refactor; NOT RED)

def test_exactly_one_h1_per_journey_page():
    for key, html in _render_journey_pages().items():
        assert html.count("<h1") == 1, f"{key}: expected exactly one <h1>"


def test_html_lang_marker_preserved():
    for key, html in _render_journey_pages().items():
        assert '<html lang="en">' in html, f"{key}: <html lang=\"en\"> marker not preserved"


def test_shell_header_adds_no_navigation_or_future_controls():
    # The shared header must contain only brand + temporary-session text — no
    # navigation and no future-capability controls (accounts, settings, logout,
    # projects, PDF, email, etc.). The skip link lives outside the header.
    for key, html in _render_journey_pages().items():
        header = _header_block(html)
        assert "<a" not in header, f"{key}: header must not contain links/navigation"
        assert "<nav" not in header, f"{key}: header must not contain a nav element"
        assert "<button" not in header, f"{key}: header must not contain controls"


def test_existing_journey_markers_preserved():
    pages = _render_journey_pages()
    assert 'name="idea"' in pages["entry"], "entry: idea input marker lost"
    assert "Describe your invention idea to begin." in pages["entry"], "entry: intro copy lost"
    assert "InventorAI" in pages["session"], "session: product name lost"
    assert "Back to session" in pages["deliverable"], "deliverable: back link lost"
    assert "Back to the assessment" in pages["success"], "success: back link lost"
