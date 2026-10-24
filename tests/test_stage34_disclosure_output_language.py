"""Stage 34 — STAGE34-OUTPUT-LANGUAGE-01 — explicit output language for the ONE
Stage-35 disclosure HTML download.

The pre-download page offers one HTML control per output language (``en`` /
``ar``); the existing HTML route accepts exactly one of those values in its
``lang`` query value and otherwise keeps the UI language (unchanged behaviour).
Anything else is refused (bare 400), never normalised, and only after the
unchanged authorization, so a denial stays byte-identical whatever is asked.
The language changes presentation only: the projection, digest, version,
filename, headers and every substantive value stay the same; nothing is stored.
"""
import json
import re

import pytest

import web.app as webapp
from tests.csrf_client import csrf_client
from tests.test_stage19_durable_success_criteria import _client_for
from tests.test_stage35_disclosure_projection import DISCLAIMERS_EN, SCOPE_AR, SCOPE_EN
from tests.test_stage35_disclosure_routes import (
    HTML_CSP, HTML_URL, JSON_URL, PAGE, _dump, _null_owner_project, _sig, owned,  # noqa: F401
)
from web import ui_text

TS = "2026-10-14T00:00:00Z"
INVALID = ["lang=", "lang=fr", "lang=EN", "lang=Ar", "lang=en%20", "lang=ar-SA",
           "lang=english", "lang=en&lang=en", "lang=en&lang=ar", "lang=ar&lang=xx"]


@pytest.fixture()
def fixed_time(monkeypatch):
    monkeypatch.setattr(webapp._disclosure, "generated_at_now", lambda: TS)


def _html(c, sid, query=""):
    return c.get(HTML_URL % sid + (("?" + query) if query else ""))


def _values(body):
    """Every rendered substantive value block, in document order."""
    return re.findall(r'<div class="value"[^>]*>.*?</div>', body, re.S)


def _english_spans(body):
    return re.findall(r'<(?:p|span) lang="en" dir="ltr">.*?</(?:p|span)>', body, re.S)


# ===========================================================================
# pre-download page
# ===========================================================================
@pytest.mark.parametrize("ui", ["en", "ar"])
def test_page_offers_one_html_control_per_output_language(owned, ui):
    c, aid, sid = owned
    if ui == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    before = _dump()
    body = c.get(PAGE % sid).get_data(as_text=True)
    for lang in ("en", "ar"):
        anchor = '<a href="%s?lang=%s" hreflang="%s" data-output-lang="%s">%s</a>' % (
            HTML_URL % sid, lang, lang, lang,
            ui_text.text("UI_S35_HTML_CONTROL_" + lang.upper(), ui))
        assert body.count(anchor) == 1
    assert body.count('href="%s' % (HTML_URL % sid)) == 2       # no language-less control
    assert ui_text.text("UI_S35_PAGE_OUTPUT_LANGUAGE_NOTE", ui).replace("'", "&#39;") in body
    assert _dump() == before                                   # the page records nothing


# ===========================================================================
# explicit output language
# ===========================================================================
@pytest.mark.parametrize("ui", ["en", "ar"])
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_explicit_language_wins_over_ui_language(owned, fixed_time, ui, lang):
    c, aid, sid = owned
    if ui == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    before = _dump()
    r = _html(c, sid, "lang=" + lang)
    assert r.status_code == 200
    assert r.headers["Content-Type"] == "text/html; charset=utf-8"
    assert r.headers["Content-Disposition"] == \
        'attachment; filename="inventorai-disclosure-export-v3.html"'
    assert r.headers["Cache-Control"] == "no-store"
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["Content-Security-Policy"] == HTML_CSP
    body = r.data.decode("utf-8")
    direction = "rtl" if lang == "ar" else "ltr"
    assert '<html lang="%s" dir="%s">' % (lang, direction) in body
    assert "inventorai-disclosure-html/3" in body          # v3 (PATHN-CONSTRAINT-DECLARATION-01)
    assert (SCOPE_AR in body) == (lang == "ar")
    assert SCOPE_EN in body and all(en in body for en in DISCLAIMERS_EN)
    assert sid not in body and aid not in body
    assert _dump() == before                                   # nothing stored
    # the choice is request-local: the UI language is unchanged afterwards
    with c.session_transaction() as flask_session:
        assert flask_session.get("ui_lang", "en") == ui


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_explicit_language_equals_the_unchanged_ui_language_rendering(owned, fixed_time, lang):
    c, aid, sid = owned
    if lang == "ar":
        c.post("/ui-language", data={"lang": "ar"})
    default = _html(c, sid)                                    # no override: unchanged path
    explicit = _html(c, sid, "lang=" + lang)
    assert default.status_code == explicit.status_code == 200
    assert default.data == explicit.data
    # the rolling session cookie is refreshed on every request; every other header matches
    strip = lambda r: {k: v for k, v in r.headers.items() if k != "Set-Cookie"}
    assert strip(default) == strip(explicit)


def test_language_changes_presentation_only(owned, fixed_time):
    c, aid, sid = owned
    digest = json.loads(c.get(JSON_URL % sid).data.decode("utf-8"))["content_digest"]
    en = _html(c, sid, "lang=en").data.decode("utf-8")
    ar = _html(c, sid, "lang=ar").data.decode("utf-8")
    assert digest in en and digest in ar
    assert _values(en) and _values(en) == _values(ar)          # every substantive value
    assert _english_spans(en)                                  # English text kept in Arabic
    assert [s for s in _english_spans(ar) if s in _english_spans(en)] == _english_spans(en)


def test_json_download_is_unaffected(owned, fixed_time):
    c, aid, sid = owned
    plain = c.get(JSON_URL % sid)
    for query in ("lang=ar", "lang=en", "lang=fr"):
        other = c.get(JSON_URL % sid + "?" + query)
        assert (other.status_code, other.data) == (plain.status_code, plain.data)


# ===========================================================================
# invalid explicit values: refused, never normalised
# ===========================================================================
@pytest.mark.parametrize("query", INVALID)
def test_invalid_explicit_language_is_refused(owned, query):
    c, aid, sid = owned
    before = _dump()
    r = _html(c, sid, query)
    assert (r.status_code, r.data) == (400, b"")
    assert "Content-Disposition" not in r.headers
    assert _dump() == before


@pytest.mark.parametrize("query", ["lang=en", "lang=ar"] + INVALID)
def test_denial_is_unchanged_whatever_language_is_asked(owned, query):
    c, aid, sid = owned
    other, _other_aid = _client_for("s34-lang-other@example.com")
    missing = other.get(HTML_URL % "no-such-project")
    assert missing.status_code == 302
    assert _sig(other.get(HTML_URL % "no-such-project" + "?" + query)) == _sig(missing)
    assert _sig(other.get(HTML_URL % sid + "?" + query)) == _sig(missing)
    with csrf_client(webapp.app) as anon:
        assert _sig(anon.get(HTML_URL % sid + "?" + query)) == _sig(missing)
    assert _sig(c.get(HTML_URL % _null_owner_project() + "?" + query)) == _sig(missing)


def test_output_language_values_are_exactly_en_and_ar():
    assert webapp._DISCLOSURE_OUTPUT_LANGS == ("en", "ar")
    for key in ("UI_S35_HTML_CONTROL_EN", "UI_S35_HTML_CONTROL_AR",
                "UI_S35_PAGE_OUTPUT_LANGUAGE_NOTE"):
        assert ui_text.text(key, "en") and ui_text.text(key, "ar")
        assert ui_text.text(key, "en") != ui_text.text(key, "ar")
    assert not ui_text.has_string("UI_S35_HTML_CONTROL")
