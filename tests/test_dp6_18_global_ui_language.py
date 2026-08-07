"""D-P6-18 — Global UI Language (English | العربية) — RED/GREEN behaviour tests.

Gate G-DP6-18-GLOBAL-UI-LANGUAGE-IMPLEMENTATION-01. These tests prove, through
REAL Flask routes rendering REAL templates (not source grep), the authorized
global UI-language capability:

  * a global, explicit UI-language selector (English | العربية) in the shared
    top-of-application UI, available consistently across active in-scope pages;
  * default UI language = English (LTR, ``<html lang="en">``);
  * an explicit Arabic selection that flips the shell to ``lang="ar"`` + RTL and
    renders the approved single-language Arabic UI chrome;
  * ONE language at a time for ordinary UI labels (never simultaneous EN + AR);
  * the P6-1 truthful domain label follows the selected UI language;
  * the canonical technical/system QUESTION text stays English in BOTH UI
    languages (hard boundary — the Question Translation Assistant is NOT this
    gate);
  * substantive generated OUTPUT is not translated by this gate;
  * UI language is not inferred from user input (mixed Arabic/English input does
    not change the UI language);
  * the corrected, product-truth-aligned sensitive copy replaces the stale
    Phase-4/5 no-account/no-durable-project claims.

The signed Flask session carries ``ui_lang``. No mocks; the test client persists
the session cookie across requests.
"""
import re

import pytest

from web.app import app, SESSION_STORE

# --- approved Arabic chrome fragments (from the finalized EN/AR copy package) ---
AR_START_BUTTON = "ابدأ"                       # index Start button (UI-B-INDEX-008)
AR_IDEA_LABEL = "صف فكرتك"                      # index idea label (UI-B-INDEX-005)
AR_SIGNIN = "تسجيل الدخول"                       # login "Sign in" (UI-A-LOGIN-001)
AR_SELECTOR_OPTION = "العربية"                  # the Arabic selector option label
AR_ELECTRONICS_LABEL = "مراجعة مستنيرة بمجال الإلكترونيات"   # P6-1 AR label
EN_ELECTRONICS_LABEL = "Electronics-informed review"        # P6-1 EN label

# --- corrected, product-truth-aligned sensitive copy (owner-approved) ----------
STALE_INDEX_04 = "There is no account or durable saved-projects area."
CORRECTED_INDEX_04 = ("You can start anonymously, or create an account and sign in "
                      "to keep and reopen your projects.")
STALE_DATA_04 = "There is no account or sign-in in this experience."
CORRECTED_DATA_02 = "Signed-in accounts can keep and reopen saved projects."

# --- a stable English fragment of a canonical system question ------------------
# The seeded electronics idea opens on the Path-N N-MC-1 question; its English
# text is canonical and must stay English in BOTH UI languages (hard boundary).
EN_INTAKE_QUESTION_FRAGMENT = "how you imagine the system would notice the problem"

IDEA = ("An electronic circuit uses a sensor and a switch to cut the power when "
        "the current gets too high.")
FORM = {"idea": IDEA, "domain_confirm": "electronics_electrical"}


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def _set_lang(client, lang):
    r = client.post("/ui-language", data={"lang": lang})
    assert r.status_code in (302, 303), r.status_code
    return r


def _start(client):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


# --- selector + route ----------------------------------------------------------
def test_ui_language_route_exists_and_redirects(client):
    r = client.post("/ui-language", data={"lang": "ar"})
    assert r.status_code in (302, 303)


def test_global_language_selector_present_and_text_labelled(client):
    body = client.get("/").get_data(as_text=True)
    # A real, accessible, text-labelled selector that posts to /ui-language.
    assert "/ui-language" in body
    assert "English" in body
    assert AR_SELECTOR_OPTION in body
    # keyboard-usable controls, not icon-only (a form with buttons or links).
    assert ("<button" in body) or ("<a " in body)


def test_selector_present_on_multiple_in_scope_pages(client):
    for path in ("/", "/login", "/register", "/data-and-session"):
        body = client.get(path).get_data(as_text=True)
        assert "/ui-language" in body, path
        assert AR_SELECTOR_OPTION in body, path


# --- default English / LTR -----------------------------------------------------
def test_default_ui_language_is_english_ltr(client):
    body = client.get("/").get_data(as_text=True)
    assert '<html lang="en">' in body
    assert '<html lang="ar"' not in body


# --- explicit Arabic selection -> RTL shell + Arabic chrome --------------------
def test_arabic_selection_sets_rtl_shell(client):
    _set_lang(client, "ar")
    body = client.get("/").get_data(as_text=True)
    assert '<html lang="ar" dir="rtl">' in body


def test_arabic_selection_renders_arabic_index_chrome(client):
    _set_lang(client, "ar")
    body = client.get("/").get_data(as_text=True)
    assert AR_START_BUTTON in body
    assert AR_IDEA_LABEL in body


def test_english_selection_keeps_english_chrome(client):
    _set_lang(client, "ar")
    _set_lang(client, "en")
    body = client.get("/").get_data(as_text=True)
    assert '<html lang="en">' in body
    assert ">Start<" in body
    # Arabic idea-label chrome must not render under English selection.
    assert AR_IDEA_LABEL not in body


# --- no simultaneous EN + AR for ordinary labels (D-P6-16) --------------------
def test_login_single_language_english_default(client):
    body = client.get("/login").get_data(as_text=True)
    assert "Sign in" in body
    # The Arabic content translation of the same label must NOT co-render.
    assert AR_SIGNIN not in body


def test_login_single_language_arabic_when_selected(client):
    _set_lang(client, "ar")
    body = client.get("/login").get_data(as_text=True)
    assert AR_SIGNIN in body
    # The English label must NOT co-render as page content under Arabic.
    # (Allow the selector's own "English" option token; assert the label span.)
    assert "<h1>Sign in</h1>" not in body


# --- persistence across navigation --------------------------------------------
def test_ui_language_persists_across_navigation(client):
    _set_lang(client, "ar")
    for path in ("/", "/data-and-session", "/login", "/register"):
        body = client.get(path).get_data(as_text=True)
        assert '<html lang="ar" dir="rtl">' in body, path


# --- P6-1 truthful domain label follows the UI language -----------------------
def test_p6_1_label_follows_ui_language(client):
    sid = _start(client)
    en_body = client.get("/session/" + sid).get_data(as_text=True)
    assert EN_ELECTRONICS_LABEL in en_body
    assert AR_ELECTRONICS_LABEL not in en_body
    _set_lang(client, "ar")
    ar_body = client.get("/session/" + sid).get_data(as_text=True)
    assert AR_ELECTRONICS_LABEL in ar_body
    assert EN_ELECTRONICS_LABEL not in ar_body


# --- HARD BOUNDARY: canonical question text stays English in BOTH languages ----
def test_canonical_question_stays_english_in_both_languages(client):
    sid = _start(client)
    en_body = client.get("/session/" + sid).get_data(as_text=True)
    assert EN_INTAKE_QUESTION_FRAGMENT in en_body
    _set_lang(client, "ar")
    ar_body = client.get("/session/" + sid).get_data(as_text=True)
    # The system question itself is NOT translated by D-P6-18.
    assert EN_INTAKE_QUESTION_FRAGMENT in ar_body


# --- OUTPUT boundary: substantive generated output not falsely Arabic ---------
def test_output_language_boundary_english_marker_on_arabic_ui(client):
    sid = _start(client)
    _set_lang(client, "ar")
    body = client.get("/session/" + sid + "/deliverable").get_data(as_text=True)
    # UI chrome is Arabic (shell RTL) but substantive package output stays English;
    # a stable English structural token from generated output remains present.
    assert '<html lang="ar" dir="rtl">' in body
    assert "InventorAI" in body


# --- UI language is NOT inferred from input -----------------------------------
def test_mixed_input_does_not_change_ui_language(client):
    sid = _start(client)
    # default English UI
    assert '<html lang="en">' in client.get("/session/" + sid).get_data(as_text=True)
    # submit an answer containing Arabic script; the UI language must not flip.
    client.post("/session/" + sid,
                data={"response": "الدائرة تستشعر التيار ثم تفصل الطاقة",
                      "action": "answered"})
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert '<html lang="en">' in body
    assert '<html lang="ar"' not in body


# --- corrected, product-truth-aligned sensitive copy --------------------------
def test_index_sensitive_copy_corrected_no_stale_claim(client):
    body = client.get("/").get_data(as_text=True)
    assert STALE_INDEX_04 not in body
    assert CORRECTED_INDEX_04 in body


def test_data_session_sensitive_copy_corrected_no_stale_claim(client):
    body = client.get("/data-and-session").get_data(as_text=True)
    assert STALE_DATA_04 not in body
    assert CORRECTED_DATA_02 in body


# --- default English render must not regress the exact P6-1 English behaviour --
def test_default_english_session_label_is_english_only(client):
    sid = _start(client)
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert EN_ELECTRONICS_LABEL in body
    assert AR_ELECTRONICS_LABEL not in body
