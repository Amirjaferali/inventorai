"""G-UX-TRUST — Temporary-Session "Learn more" / Data & Session Trust Surface (S15).

Behavioral RED->GREEN tests via Flask test_client. RED against base 43453ce:
GET /data-and-session is 404; the four journey headers have no Learn more link; the
S15 copy does not render. GREEN after the increment. No real server/port; no durable
file; no session mutation.

Exact canonical copy is asserted verbatim (HTML entities unescaped for the title).
"""

import html
import re

from web.app import app, SESSION_STORE
from engine.idea_state import (
    IdeaState, Evidence, REASONED, Gap, PARTIAL, CLOSED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)

_SID = "gux-trust-baseline-sid"

# ---- exact canonical copy (owner-authorized) -------------------------------
PAGE_TITLE = "Data & Session information"
LEARN_MORE = "Learn more"
# D-P6-18: truth-corrected, owner-approved product-truth copy. Phase-4/5 added
# accounts and durable/reopenable projects, so the stale "held temporarily / no
# durable saved-projects / no account or sign-in / no durable transcript"
# sentences were replaced with the corrected canonical English (DATA-01..07).
S15_LINES = [
    "Your idea and accepted answers are saved as part of your project so the tool can prepare and reload your assessment. Some in-progress working state remains temporary to the current session.",
    "Signed-in accounts can keep and reopen saved projects. Version history and branching are not currently provided.",
    "To help you recover unfinished text if you leave and return, text you are typing may be kept temporarily in this browser on this device only (local browser storage). It is not saved to an account or to any server, and is not available on another device or browser. It expires after 7 days, is removed once the matching answer is submitted, and can be discarded at any time. Because it is kept in this browser profile, anyone who can use this browser (including browser-profile sync) may be able to see it — please avoid this feature on a shared or public device, or discard your draft when you finish.",
    "You can use InventorAI anonymously, or create an account and sign in. Having an account or a saved project does not create or prove legal ownership of your idea.",
    "Your accepted answers are saved as part of your project so the tool can prepare and reload your assessment. This does not provide a complete resumable record of every interaction in your session.",
    "Confidentiality and staff-access details are not finalized on this screen. Do not rely on this screen as a promise that information can never be accessed or reviewed.",
    "Privacy Policy and Terms content is not provided on this information screen.",
]
RETURN_LABEL = "Back to InventorAI"

PROHIBITED = [
    # NB: the blanket "reload" token was dropped — the truth-corrected DATA-01/05
    # copy legitimately says the tool can "reload your assessment" (durable
    # projects now exist). The over-access / storage-mechanism claims below stay
    # forbidden.
    "browser session", "closing", "tab", "/tmp",
    "staff can never", "never access", "never review", "retention",
    "deleted after", "encrypted", "Privacy Policy and Terms are not yet available",
]

_JOURNEY = ("/", None, None, None)  # entry + three seeded routes (built below)


def _seed_session(sid):
    s = IdeaState(idea_id=sid)
    s.domain = "electronics_electrical"
    s.domain_signal = "electronics_electrical"
    s.maturity_level = 1
    s.current_stage = 2
    s.known_problem = Evidence("existing systems miss micro-faults", REASONED, 1)
    s.known_mechanism = Evidence("voltage drop across the shunt resistor triggers the comparator", REASONED, 2)
    s.gaps.append(Gap(gap_type=MECHANISM_COMPLETENESS, status=CLOSED, opened_at=1, closed_at=2))
    s.gaps.append(Gap(gap_type=PHYSICAL_FEASIBILITY, status=CLOSED, opened_at=3, closed_at=4))
    s.gaps.append(Gap(gap_type=BOUNDARY_AMBIGUITY, status=PARTIAL, opened_at=5))
    s.iteration = 5
    SESSION_STORE[sid] = {"state": s, "last_result": None, "transcript": [], "last_question": "Q"}


def _journey_routes():
    return ["/", f"/session/{_SID}", f"/session/{_SID}/deliverable", f"/session/{_SID}/success-criteria"]


def _header_block(body):
    m = re.search(r"<header\b.*?</header>", body, re.DOTALL)
    return m.group(0) if m else ""


def test_s15_route_renders_and_extends_shell():
    c = app.test_client()
    r = c.get("/data-and-session")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    # shell inheritance
    assert 'name="viewport"' in body
    assert '<main id="main-content">' in body
    assert 'href="#main-content"' in body


def test_s15_exact_canonical_copy_renders():
    body = html.unescape(app.test_client().get("/data-and-session").get_data(as_text=True))
    assert body.count("<h1") == 1
    assert PAGE_TITLE in body
    for line in S15_LINES:
        assert line in body, f"missing exact S15 line: {line!r}"
    assert RETURN_LABEL in body


def test_s15_return_link_points_to_root():
    body = app.test_client().get("/data-and-session").get_data(as_text=True)
    assert re.search(r'<a href="/">\s*Back to InventorAI\s*</a>', body), "Back to InventorAI must link to /"


def test_s15_no_prohibited_claims():
    r = app.test_client().get("/data-and-session")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    for token in PROHIBITED:
        assert token not in body, f"prohibited phrase rendered on S15: {token!r}"


def test_s15_no_terms_privacy_body_or_future_controls():
    r = app.test_client().get("/data-and-session")
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    # only structural controls: the header has no self-link; the sole in-body link is Back to /
    hdr = _header_block(body)
    assert "Learn more" not in hdr, "S15 header must suppress the Learn more self-link"
    # NB: the D-P6-18 UI-language selector is text links (no <form>/<button>), so
    # the original no-product-controls guard still holds unchanged.
    for forbidden in ("Sign in", "Log in", "Logout", "Account", "Settings",
                      "Saved Projects", "Download PDF", "Email", "<form", "<button"):
        assert forbidden not in body, f"S15 must not contain: {forbidden!r}"


def test_learn_more_link_present_on_journey_headers():
    _seed_session(_SID)
    c = app.test_client()
    try:
        for route in _journey_routes():
            hdr = _header_block(c.get(route).get_data(as_text=True))
            assert 'href="/data-and-session"' in hdr, f"{route}: header missing Learn more link"
            assert "Learn more" in hdr, f"{route}: header missing Learn more text"
    finally:
        SESSION_STORE.pop(_SID, None)


def test_learn_more_self_link_suppressed_on_s15():
    hdr = _header_block(app.test_client().get("/data-and-session").get_data(as_text=True))
    assert "Temporary session" in hdr, "S15 header must still show the Temporary session text"
    assert 'href="/data-and-session"' not in hdr, "S15 header must not self-link"
    assert "<a" not in hdr, "S15 header must contain no anchor"


def test_s15_route_reads_no_session_state():
    # The route must render with no session in the store (takes no sid, reads no state).
    SESSION_STORE.clear()
    r = app.test_client().get("/data-and-session")
    assert r.status_code == 200
    assert SESSION_STORE == {}, "S15 route must not create or mutate session state"
