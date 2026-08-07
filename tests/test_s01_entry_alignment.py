"""G-UX-ENTRY — Existing Entry Surface Alignment (S01).

Behavioral RED->GREEN tests via Flask test_client for the live entry surface `/`.

RED against base cc71ab7: the entry page has no visible `<label for="idea">Describe
your idea</label>`, the idea textarea carries no `id="idea"`, and the exact
temporary-session intake-disclosure sentence does not render. GREEN after the
bounded index.html additions.

All assertions exercise rendered HTML (not source grep) and verify the actual
label-to-textarea association, not merely the presence of substrings. No real
server/port is opened; no durable file is created; no session is mutated.
"""

import re

from web.app import app

# ---- owner-approved exact copy ---------------------------------------------
LABEL_TEXT = "Describe your idea"
# D-P6-18: truth-corrected, owner-approved product-truth copy (UI-SENS-INDEX-04).
# Accounts and durable/reopenable projects now exist; the prior "no account /
# no durable saved-projects" sentence was stale Phase-4/5 copy and was replaced.
DISCLOSURE = ("You can start anonymously, or create an account and sign in to keep "
              "and reopen your projects. Your current working session may still "
              "contain temporary state.")

# ---- pinned pre-existing copy (preservation invariants, NOT RED) ------------
PINNED_INTRO = "Describe your invention idea to begin."
PINNED_SUPPORT = "Currently supported: electronics and electrical ideas."


def _entry_body():
    return app.test_client().get("/").get_data(as_text=True)


# ------------------------------------------------------------------ RED -> GREEN

def test_entry_returns_200():
    assert app.test_client().get("/").status_code == 200


def test_exactly_one_label_for_idea_with_exact_text():
    body = _entry_body()
    labels = re.findall(r'<label\b[^>]*\bfor="idea"[^>]*>(.*?)</label>', body, re.DOTALL)
    assert len(labels) == 1, f"expected exactly one <label for=\"idea\">, found {len(labels)}"
    assert labels[0].strip() == LABEL_TEXT, f"label text must be exactly {LABEL_TEXT!r}, got {labels[0].strip()!r}"


def test_exactly_one_textarea_has_id_and_name_idea():
    body = _entry_body()
    textareas = re.findall(r"<textarea\b[^>]*>", body)
    with_id = [t for t in textareas if re.search(r'\bid="idea"', t)]
    assert len(with_id) == 1, f"expected exactly one textarea with id=\"idea\", found {len(with_id)}"
    assert re.search(r'\bname="idea"', with_id[0]), "the id=\"idea\" textarea must keep name=\"idea\""


def test_label_target_matches_textarea_id():
    # The label's for target must be the id of the actual idea textarea (real association).
    body = _entry_body()
    assert re.search(r'<label\b[^>]*\bfor="idea"', body), "label must target for=\"idea\""
    assert re.search(r'<textarea\b[^>]*\bid="idea"[^>]*\bname="idea"|<textarea\b[^>]*\bname="idea"[^>]*\bid="idea"', body), \
        "a single textarea must carry both id=\"idea\" and name=\"idea\""


def test_exact_disclosure_renders_exactly_once():
    body = _entry_body()
    assert body.count(DISCLOSURE) == 1, f"exact disclosure sentence must render exactly once (found {body.count(DISCLOSURE)})"


# --------------------------------------------------------- preservation invariants
# (these pass on the base too; they guard against regressions in the increment)

def test_start_cta_present():
    assert ">Start<" in _entry_body(), "primary Start CTA must remain"


def test_form_method_post_action_start():
    body = _entry_body()
    # D-P6-18 adds a global UI-language selector form (action="/ui-language") at
    # the top of the shell; the entry form is identified by its /start action.
    m = re.search(r'<form\b[^>]*action="/start"[^>]*>', body)
    assert m, "entry form (POST /start) must be present"
    tag = m.group(0)
    assert 'method="POST"' in tag and 'action="/start"' in tag, "form must remain POST to /start"


def test_domain_confirm_checkbox_unchanged():
    body = _entry_body()
    assert re.search(r'<input\b[^>]*type="checkbox"[^>]*name="domain_confirm"[^>]*value="electronics_electrical"'
                     r'|<input\b[^>]*name="domain_confirm"[^>]*value="electronics_electrical"', body), \
        "domain_confirm checkbox (value electronics_electrical) must remain"


def test_header_temporary_session_and_learn_more():
    body = _entry_body()
    header = re.search(r"<header\b.*?</header>", body, re.DOTALL)
    assert header, "shared shell header must remain"
    hdr = header.group(0)
    assert "Temporary session" in hdr, "header Temporary session disclosure must remain"
    assert 'href="/data-and-session"' in hdr and "Learn more" in hdr, "header Learn more link must remain"


def test_pinned_existing_copy_preserved():
    body = _entry_body()
    assert PINNED_INTRO in body, "pre-existing intro copy must remain (copy-debt, unchanged)"
    assert PINNED_SUPPORT in body, "pre-existing support line must remain"


def test_exactly_one_h1_and_lang_en():
    body = _entry_body()
    assert body.count("<h1") == 1, "exactly one <h1> must remain"
    assert '<html lang="en">' in body, "html language marker must remain en"


def test_no_stepper_and_no_future_controls():
    body = _entry_body()
    assert "Step 1 of 9" not in body, "no nine-step stepper may be introduced"
    for forbidden in ("Saved Projects", "Sign in", "Log in", "Logout", "Account",
                      "Download PDF", "Email Delivery", "ACV",
                      "Keep current snapshot", "Refine this idea"):
        assert forbidden not in body, f"entry must not introduce a {forbidden!r} control"


def test_disclosure_is_plain_body_text_not_a_control():
    # The disclosure sentence must be ordinary body text: not a link, button, or input.
    body = _entry_body()
    m = re.search(r'<([a-z0-9]+)[^>]*>[^<]*' + re.escape(DISCLOSURE), body)
    assert m, "disclosure sentence must render inside an element"
    tag = m.group(1).lower()
    assert tag not in ("a", "button", "input", "label"), \
        f"disclosure must be plain body text, not a {tag} control"


def test_s15_route_preserved():
    # Proportionate preservation check: S15 remains reachable and its copy intact.
    body = app.test_client().get("/data-and-session").get_data(as_text=True)
    assert "Data &amp; Session information" in body or "Data & Session information" in body
    hdr = re.search(r"<header\b.*?</header>", body, re.DOTALL).group(0)
    assert 'href="/data-and-session"' not in hdr, "S15 header self-link must remain suppressed"
