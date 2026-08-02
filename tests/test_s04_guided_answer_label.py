"""G-UX-GUIDED-LABEL — Guided Question Accessibility Alignment (S04).

Behavioral RED->GREEN tests via Flask test_client for the guided-session answer
control on `/session/<sid>`.

RED against base 41e51ba: the free-text answer textarea has no `id="response"` and
no visible `<label for="response">Your answer</label>`; the label-to-textarea
association is absent. GREEN after the bounded session.html additions.

All assertions exercise rendered HTML (not source grep) on a seeded in-memory
session and verify the actual label-to-textarea association. No real server/port is
opened; no durable file is created; the session is seeded in-memory using the same
pattern as tests/test_web_app.py and mutated by no application code.
"""

import re

from web.app import app, SESSION_STORE
from engine.idea_state import (
    IdeaState, Evidence, REASONED, Gap, PARTIAL, CLOSED,
    MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY,
)

_SID = "gux-guided-label-sid"

# ---- owner-approved exact copy ---------------------------------------------
LABEL_TEXT = "Your answer"
LEGEND = "How do you want to respond?"
PLACEHOLDER = "Describe your thinking here, or pick an option below..."

# ---- radio values pinned by the current product (preservation) -------------
RADIO_VALUES = ["answered", "unknown", "deferred",
                "provisional_assumption", "specialist_requested", "evidence_requested"]


def _seed_session(sid):
    # Boundary state that leaves an open gap so select_next_gap() yields a gap and
    # the guided-question answer form renders. In-memory only; nothing durable.
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


def _session_body():
    _seed_session(_SID)
    try:
        r = app.test_client().get(f"/session/{_SID}")
        return r
    finally:
        SESSION_STORE.pop(_SID, None)


def _header_block(body):
    m = re.search(r"<header\b.*?</header>", body, re.DOTALL)
    return m.group(0) if m else ""


# ------------------------------------------------------------------ RED -> GREEN

def test_session_returns_200_for_seeded_session():
    assert _session_body().status_code == 200


def test_exactly_one_label_for_response_with_exact_text():
    body = _session_body().get_data(as_text=True)
    labels = re.findall(r'<label\b[^>]*\bfor="response"[^>]*>(.*?)</label>', body, re.DOTALL)
    assert len(labels) == 1, f"expected exactly one <label for=\"response\">, found {len(labels)}"
    assert labels[0].strip() == LABEL_TEXT, f"label text must be exactly {LABEL_TEXT!r}, got {labels[0].strip()!r}"


def test_exactly_one_free_text_textarea_has_id_and_name_response():
    body = _session_body().get_data(as_text=True)
    with_id = [t for t in re.findall(r"<textarea\b[^>]*>", body)
               if re.search(r'\bid="response"', t)]
    assert len(with_id) == 1, f"expected exactly one textarea id=\"response\", found {len(with_id)}"
    assert re.search(r'\bname="response"', with_id[0]), "the id=\"response\" textarea must keep name=\"response\""


def test_label_target_matches_textarea_id():
    body = _session_body().get_data(as_text=True)
    assert re.search(r'<label\b[^>]*\bfor="response"', body), "label must target for=\"response\""
    assert re.search(r'<textarea\b[^>]*\bid="response"[^>]*\bname="response"'
                     r'|<textarea\b[^>]*\bname="response"[^>]*\bid="response"', body), \
        "a single textarea must carry both id=\"response\" and name=\"response\""


def test_label_does_not_duplicate_question_text():
    # The label is a short field name, not the question prompt.
    body = _session_body().get_data(as_text=True)
    qm = re.search(r'<p class="question">(.*?)</p>', body, re.DOTALL)
    assert qm, "question paragraph must be present"
    assert qm.group(1).strip() != LABEL_TEXT, "label must not duplicate the question text"


def test_label_is_visible_not_aria_substitute():
    body = _session_body().get_data(as_text=True)
    # Native visible label present; the increment adds no aria-* on the control.
    ta = [t for t in re.findall(r"<textarea\b[^>]*>", body) if 'id="response"' in t][0]
    assert "aria-label" not in ta, "increment must not add aria-label"
    assert "aria-labelledby" not in ta, "increment must not add aria-labelledby"
    assert "aria-describedby" not in ta, "increment must not add aria-describedby"


# --------------------------------------------------------- preservation invariants
# (pass on the base too; guard against regressions)

def test_placeholder_preserved():
    body = _session_body().get_data(as_text=True)
    assert PLACEHOLDER in body, "existing answer placeholder must remain unchanged"


def test_question_paragraph_preserved_not_heading():
    body = _session_body().get_data(as_text=True)
    assert '<p class="question">' in body, "question must remain a <p class=\"question\"> (not converted to a heading)"


def test_answer_hint_preserved():
    body = _session_body().get_data(as_text=True)
    assert "Answer in the box below, or choose one of the response options." in body


def test_radio_fieldset_legend_and_values_preserved():
    body = _session_body().get_data(as_text=True)
    assert "<fieldset" in body and "<legend" in body, "response-type fieldset/legend must remain"
    assert LEGEND in body, "fieldset legend text must remain"
    for v in RADIO_VALUES:
        assert f'value="{v}"' in body, f"radio option value {v!r} must remain"


def test_submit_cta_preserved():
    body = _session_body().get_data(as_text=True)
    assert re.search(r'<button[^>]*>\s*Submit\s*</button>', body), "Submit CTA must remain"


def test_one_h1_and_lang_en():
    body = _session_body().get_data(as_text=True)
    assert body.count("<h1") == 1, "exactly one <h1> must remain"
    assert '<html lang="en">' in body, "html lang marker must remain en"


def test_header_temporary_session_and_learn_more():
    hdr = _header_block(_session_body().get_data(as_text=True))
    assert "Temporary session" in hdr, "header Temporary session disclosure must remain"
    assert 'href="/data-and-session"' in hdr and "Learn more" in hdr, "header Learn more link must remain"


def test_missing_session_get_redirects_to_root():
    SESSION_STORE.pop("no-such-sid", None)
    r = app.test_client().get("/session/no-such-sid")
    assert r.status_code == 302 and r.headers.get("Location", "").endswith("/"), \
        "missing session must redirect to /"


def test_no_progress_or_future_controls():
    body = _session_body().get_data(as_text=True)
    assert "Step 1 of 9" not in body and "Step X of 9" not in body
    for forbidden in ("Saved Projects", "Sign in", "Log in", "Logout", "Account",
                      "Download PDF", "Email Delivery", "ACV",
                      "Keep current snapshot", "Refine this idea"):
        assert forbidden not in body, f"session must not introduce a {forbidden!r} control"


def test_s15_route_preserved():
    body = app.test_client().get("/data-and-session").get_data(as_text=True)
    import html as _html
    assert "Data & Session information" in _html.unescape(body)
    hdr = _header_block(body)
    assert 'href="/data-and-session"' not in hdr, "S15 header self-link must remain suppressed"
