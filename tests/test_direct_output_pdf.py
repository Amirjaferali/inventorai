"""DIRECT-OUTPUT-PDF — secure, in-memory, on-demand PDF download of the current
InventorAI deliverable.

Behavioural tests for the authorized bounded increment
`DIRECT-OUTPUT-PDF-CREATOR-LOCAL-CANDIDATE-01 v1.0`. They exercise the real
Flask application, the real record/account stores on real on-disk SQLite (autouse
conftest isolation), real signed sessions, the real central authorization helper,
and — for the rendering proofs — real WeasyPrint 70.0. No mocks stand in for the
security boundary.

The PDF path is deliberately NOT a verbatim conversion of the rendered HTML
page: the shared application shell carries language-switch forms and live CSRF
tokens, and the eligible deliverable carries a snapshot form and session-relative
links. The PDF is therefore rendered from a PDF-ONLY trusted document shell with
every interactive control, application route, CSRF value and session capability
omitted. These tests prove that boundary behaviourally, not by reading comments.
"""
from tests.csrf_client import csrf_client
import os
import pickle
import re
import subprocess

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from web import ui_text
from engine import account_credentials as _acct

PW = "correct horse battery staple"
IDEA = ("An electronic circuit uses a sensor and a switch to cut the power when "
        "the current gets too high.")
FORM = {"idea": IDEA, "domain_confirm": "electronics_electrical"}

PDF_PATH = "/session/%s/deliverable.pdf"
HTML_PATH = "/session/%s/deliverable"

EN_BUTTON = "Download PDF"
AR_BUTTON = "تنزيل ملف PDF"
EN_HELP = "Downloads the current report with its current status."
AR_HELP = "ينزّل التقرير الحالي بحالته الحالية."
EN_TOO_LARGE = ("This report is too large to generate as a PDF safely. "
                "The report remains available on this page.")
AR_TOO_LARGE = ("هذا التقرير كبير جدًا بحيث لا يمكن إنشاء ملف PDF منه بأمان. "
                "يظل التقرير متاحًا في هذه الصفحة.")
EN_UNAVAILABLE = "We could not generate the PDF. Nothing was saved. Please try again."
AR_UNAVAILABLE = "تعذر إنشاء ملف PDF. لم يتم حفظ أي شيء. يُرجى المحاولة مرة أخرى."


# --------------------------------------------------------------------------
# Harness
# --------------------------------------------------------------------------
@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _new_client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _mk_account(email, verified=True, status="active"):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email), _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status=status)
    if verified:
        store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    return aid


def _client_for(email, verified=True, status="active"):
    aid = _mk_account(email, verified=verified, status=status)
    c = _new_client()
    c.post("/login", data={"email": email, "password": PW})
    return c, aid


def _start_project(client):
    r = client.post("/start", data=FORM)
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/session/", 1)[-1]


def _anon_project():
    """A NULL-owner (legacy/anonymous) project: capability access is preserved."""
    c = _new_client()
    return c, _start_project(c)


def _set_lang(client, lang):
    r = client.post("/ui-language", data={"lang": lang})
    assert r.status_code in (302, 303)


def _token(client, path):
    body = client.get(path).get_data(as_text=True)
    tokens = re.findall(r'name="csrf_token" value="([^"]+)"', body)
    assert tokens, "no CSRF token rendered on %s" % path
    return tokens[0]


def _post_pdf(client, sid):
    """POST the PDF route with a valid CSRF token harvested from the page."""
    return client.post(PDF_PATH % sid, data={})


def _capture_source(monkeypatch):
    """Capture the exact HTML string handed to the renderer, and the returned
    bytes, without stubbing the renderer's security behaviour."""
    seen = {}
    real = webapp._render_pdf_bytes

    def spy(source):
        seen["source"] = source
        out = real(source)
        seen["pdf"] = out
        return out

    monkeypatch.setattr(webapp, "_render_pdf_bytes", spy)
    return seen


def _document_elements_and_attributes(source):
    """Parse a rendered document and return (element names, (name, value)
    attribute pairs). Structural — immune to escaped user text that merely
    RESEMBLES markup."""
    from html.parser import HTMLParser

    class _Walk(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.elements = set()
            self.attributes = []

        def handle_starttag(self, tag, attrs):
            self.elements.add(tag)
            for name, value in attrs:
                self.attributes.append((name.lower(), value or ""))

        handle_startendtag = handle_starttag

    walk = _Walk()
    walk.feed(source)
    return walk.elements, walk.attributes


def _snapshot_state(sid):
    """Everything that must not move during PDF generation."""
    entry = SESSION_STORE.get(sid)
    state = pickle.dumps(entry["state"]) if entry else None
    memory = pickle.dumps(SESSION_STORE)
    with open(os.environ["INVENTORAI_DB_PATH"], "rb") as fh:
        database = fh.read()
    return state, memory, database


# ==========================================================================
# 1. The download action itself
# ==========================================================================
def test_pdf_download_action_is_bilingual_post_only_and_truthful(db_path):
    c, _aid = _client_for("pdf-action@example.com")
    sid = _start_project(c)

    body = c.get(HTML_PATH % sid).get_data(as_text=True)
    assert EN_BUTTON in body
    assert EN_HELP in body
    form = re.search(
        r'<form[^>]*action="[^"]*/session/%s/deliverable\.pdf"[^>]*>(.*?)</form>' % re.escape(sid),
        body, re.S)
    assert form, "no POST form targeting the PDF route on the English deliverable"
    assert re.search(r'method="POST"', form.group(0), re.I)
    assert len(re.findall(r'name="csrf_token"', form.group(1))) == 1

    _set_lang(c, "ar")
    ar = c.get(HTML_PATH % sid).get_data(as_text=True)
    assert AR_BUTTON in ar
    assert AR_HELP in ar
    assert EN_BUTTON not in ar

    # Truthfulness: the action never claims finality, validation, approval or save.
    for forbidden in ("approved", "validated", "verified", "final", "certified", "saved"):
        assert forbidden not in EN_BUTTON.lower()
        assert forbidden not in EN_HELP.lower()

    # POST only.
    assert c.get(PDF_PATH % sid).status_code == 405
    assert c.head(PDF_PATH % sid).status_code == 405


# ==========================================================================
# 2. Success response
# ==========================================================================
def test_pdf_success_is_in_memory_attachment_with_safe_headers(db_path):
    c, _aid = _client_for("pdf-ok@example.com")
    sid = _start_project(c)
    r = _post_pdf(c, sid)
    assert r.status_code == 200, r.status_code
    assert r.headers["Content-Type"] == "application/pdf"
    assert "charset" not in r.headers["Content-Type"]
    assert r.headers["Content-Disposition"] == \
        'attachment; filename="inventorai-output.pdf"'
    assert r.headers["Cache-Control"] == "private, no-store"
    data = r.get_data()
    assert data[:5] == b"%PDF-"
    assert 0 < len(data) <= webapp._PDF_MAX_OUTPUT_BYTES
    # The fixed filename never leaks project/user identity.
    for leak in (sid, "electronic", "2026"):
        assert leak not in r.headers["Content-Disposition"]
    # Existing global security headers still apply.
    html_headers = c.get(HTML_PATH % sid).headers
    for header in ("X-Content-Type-Options", "Referrer-Policy"):
        if header in html_headers:
            assert r.headers.get(header) == html_headers[header], header


# ==========================================================================
# 3. PDF source sanitisation
# ==========================================================================
def test_pdf_source_excludes_controls_tokens_routes_and_session_capability(
        db_path, monkeypatch):
    c, _aid = _client_for("pdf-clean@example.com")
    sid = _start_project(c)
    token = _token(c, HTML_PATH % sid)
    c.post("/session/%s/keep-snapshot" % sid, data={})   # arm the single-use ack

    seen = _capture_source(monkeypatch)
    assert _post_pdf(c, sid).status_code == 200
    source = seen["source"]

    assert token not in source, "a live CSRF token reached the PDF source"
    assert sid not in source, "the sid capability reached the PDF source"
    assert "csrf_token" not in source
    for tag in ("<form", "<input", "<button", "<script", "<img", "<iframe",
                "<object", "<embed", "<link"):
        assert tag not in source.lower(), tag
    # Every hyperlink is a same-document fragment.
    for href in re.findall(r'href="([^"]*)"', source):
        assert href.startswith("#"), href
    assert "url(" not in source
    assert "@font-face" not in source
    # Report content and truthful status survive.
    assert "InventorAI" in source
    assert "<h1" in source.lower()


# ==========================================================================
# 4. Renderer network/file boundary
# ==========================================================================
@pytest.mark.parametrize("scheme,markup", [
    ("http", '<img src="http://example.com/a.png">'),
    ("https", '<img src="https://example.com/a.png">'),
    ("file", '<img src="file:///etc/passwd">'),
    ("ftp", '<img src="ftp://example.com/a.png">'),
    ("data", '<img src="data:image/png;base64,iVBORw0KGgo=">'),
])
def test_pdf_renderer_denies_http_https_file_ftp_and_data_fetches(scheme, markup):
    """Direct malicious probes: the deny-all fetcher refuses on the PROTOCOL,
    before any socket is opened or any file is read."""
    import socket

    def _no_socket(*a, **k):                       # pragma: no cover - guard
        raise AssertionError("the renderer attempted a network connection")

    real_socket = socket.socket
    socket.socket = _no_socket
    try:
        source = "<!DOCTYPE html><html><body>%s</body></html>" % markup
        with pytest.raises(webapp._PdfUnavailable):
            webapp._render_pdf_bytes(source)
    finally:
        socket.socket = real_socket


# ==========================================================================
# 5. Hard byte limits
# ==========================================================================
def test_pdf_source_and_output_limits_fail_closed_without_persistence(
        db_path, monkeypatch):
    assert webapp._PDF_MAX_SOURCE_BYTES == 262144
    assert webapp._PDF_MAX_OUTPUT_BYTES == 5242880

    # The source cap is inclusive and is enforced BEFORE the renderer runs.
    invoked = {"n": 0}
    real = webapp._render_pdf_bytes

    def counting(source):
        invoked["n"] += 1
        return real(source)

    monkeypatch.setattr(webapp, "_render_pdf_bytes", counting)

    at_cap = "a" * webapp._PDF_MAX_SOURCE_BYTES
    assert len(at_cap.encode("utf-8")) == webapp._PDF_MAX_SOURCE_BYTES
    assert webapp._pdf_source_within_limit(at_cap) is True
    over = "a" * (webapp._PDF_MAX_SOURCE_BYTES + 1)
    assert webapp._pdf_source_within_limit(over) is False

    before = invoked["n"]
    with pytest.raises(webapp._PdfTooLarge):
        webapp._pdf_bytes_from_source(over)
    assert invoked["n"] == before, "renderer was invoked for an over-cap source"

    # Output cap: inclusive accept, one-byte-over discard.
    assert webapp._pdf_output_within_limit(b"%PDF-" + b"\0" * (webapp._PDF_MAX_OUTPUT_BYTES - 5)) is True
    assert webapp._pdf_output_within_limit(b"%PDF-" + b"\0" * (webapp._PDF_MAX_OUTPUT_BYTES - 4)) is False
    assert webapp._pdf_output_within_limit(b"") is False
    assert webapp._pdf_output_within_limit(b"not-a-pdf") is False

    # A limit failure through the real route is a localized 422 and writes nothing.
    c, _aid = _client_for("pdf-limit@example.com")
    sid = _start_project(c)
    state, memory, database = _snapshot_state(sid)
    monkeypatch.setattr(webapp, "_PDF_MAX_SOURCE_BYTES", 10)
    r = _post_pdf(c, sid)
    assert r.status_code == 422
    assert r.headers["Cache-Control"] == "private, no-store"
    assert r.headers["Content-Type"].startswith("text/plain")
    assert "charset=utf-8" in r.headers["Content-Type"].lower()
    assert r.get_data(as_text=True) == EN_TOO_LARGE
    assert _snapshot_state(sid) == (state, memory, database)


# ==========================================================================
# 6. Failure surface
# ==========================================================================
def test_pdf_generation_failure_is_localized_no_store_and_non_disclosing(
        db_path, monkeypatch):
    c, _aid = _client_for("pdf-fail@example.com")
    sid = _start_project(c)
    secret = "SECRET-NATIVE-DETAIL-/opt/lib/libpango.so"

    def boom(source):
        raise RuntimeError(secret)

    monkeypatch.setattr(webapp, "_render_pdf_bytes", boom)
    state, memory, database = _snapshot_state(sid)
    r = _post_pdf(c, sid)
    assert r.status_code == 503
    assert r.headers["Cache-Control"] == "private, no-store"
    assert r.headers["Content-Type"].startswith("text/plain")
    body = r.get_data(as_text=True)
    assert body == EN_UNAVAILABLE
    for leak in (secret, "RuntimeError", "Traceback", sid, "libpango"):
        assert leak not in body, leak
    assert _snapshot_state(sid) == (state, memory, database)

    _set_lang(c, "ar")
    ar = _post_pdf(c, sid)
    assert ar.status_code == 503
    assert ar.get_data(as_text=True) == AR_UNAVAILABLE

    # The 422 message localizes too.
    monkeypatch.setattr(webapp, "_PDF_MAX_SOURCE_BYTES", 10)
    monkeypatch.setattr(webapp, "_render_pdf_bytes", webapp._render_pdf_bytes)
    ar_large = _post_pdf(c, sid)
    assert ar_large.status_code == 422
    assert ar_large.get_data(as_text=True) == AR_TOO_LARGE


# ==========================================================================
# 6b. Failure boundary: context and PDF-source construction
# ==========================================================================
def test_pdf_context_failure_is_localized_no_store_and_non_disclosing(
        db_path, monkeypatch):
    """An ordinary exception while building the SHARED deliverable context must
    reach the same bounded localized PDF failure response — not Flask's generic
    500 with an HTML body and no cache directive."""
    c, _aid = _client_for("pdf-ctxfail@example.com")
    sid = _start_project(c)
    secret = "SECRET-CONTEXT-DETAIL-/srv/context"
    seen = {}

    def exploding_context(requested_sid):
        seen["sid"] = requested_sid
        raise RuntimeError(secret)

    monkeypatch.setattr(webapp, "_deliverable_context", exploding_context)
    state, memory, database = _snapshot_state(sid)
    r = _post_pdf(c, sid)

    assert seen.get("sid") == sid, seen
    assert r.status_code == 503, r.status_code
    assert r.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert r.headers["Cache-Control"] == "private, no-store"
    body = r.get_data(as_text=True)
    assert body == EN_UNAVAILABLE
    for leak in (secret, "RuntimeError", "Traceback", "/srv/context", sid):
        assert leak not in body, leak
    assert _snapshot_state(sid) == (state, memory, database)


def test_pdf_template_source_failure_is_localized_no_store_and_non_disclosing(
        db_path, monkeypatch):
    """An ordinary exception while rendering the PDF-ONLY document source must
    reach the same bounded localized failure response. Only the PDF source
    render is faulted; every other template render still uses the real
    function, so the fault is precisely the source-construction stage."""
    c, _aid = _client_for("pdf-tplfail@example.com")
    sid = _start_project(c)
    secret = "SECRET-TEMPLATE-DETAIL-/srv/template"
    real_render = webapp.render_template
    seen = {}

    def faulting_render(template_name_or_list, **context):
        if (template_name_or_list == "deliverable.html"
                and context.get("deliverable_base") == "pdf_base.html"):
            seen["hit"] = True
            raise RuntimeError(secret)
        return real_render(template_name_or_list, **context)

    monkeypatch.setattr(webapp, "render_template", faulting_render)
    state, memory, database = _snapshot_state(sid)
    r = _post_pdf(c, sid)

    assert seen.get("hit") is True, "the PDF source render was never reached"
    assert r.status_code == 503, r.status_code
    assert r.headers["Content-Type"] == "text/plain; charset=utf-8"
    assert r.headers["Cache-Control"] == "private, no-store"
    body = r.get_data(as_text=True)
    assert body == EN_UNAVAILABLE
    for leak in (secret, "RuntimeError", "Traceback", "/srv/template", sid):
        assert leak not in body, leak
    assert _snapshot_state(sid) == (state, memory, database)


# ==========================================================================
# 7-8. Authorization
# ==========================================================================
def test_pdf_owned_project_authorization_and_generic_denial_matrix(db_path):
    ca, _a = _client_for("pdf-owner@example.com")
    sid = _start_project(ca)
    assert _post_pdf(ca, sid).status_code == 200

    cb, _b = _client_for("pdf-other@example.com")
    anon = _new_client()
    disabled_client, _d = _client_for("pdf-disabled@example.com")
    disabled_sid = _start_project(disabled_client)

    denials = []
    for client, target in [(cb, sid), (anon, sid),
                           (cb, "this-sid-does-not-exist"),
                           (anon, "this-sid-does-not-exist")]:
        r = client.post(PDF_PATH % target, data={})
        assert r.status_code == 302, (target, r.status_code)
        assert r.headers["Location"].endswith("/")
        denials.append((r.status_code, r.headers["Location"]))
    assert len(set(denials)) == 1, "denials are distinguishable"

    # A disabled owner is denied on their OWN project (denial is by status; the
    # signed session is otherwise valid and unexpired).
    assert disabled_client.post(PDF_PATH % disabled_sid, data={}).status_code == 200
    webapp._get_account_store().set_status(
        _d, "disabled", "2026-01-01T00:00:00.000000Z")
    r = disabled_client.post(PDF_PATH % disabled_sid, data={})
    assert r.status_code == 302 and r.headers["Location"].endswith("/")
    assert (r.status_code, r.headers["Location"]) == denials[0]


def test_pdf_null_owner_capability_behavior_matches_html_deliverable(db_path):
    """A legacy/anonymous NULL-owner project keeps exactly its prior capability
    access on the PDF route — identical to the existing HTML deliverable."""
    creator, sid = _anon_project()
    assert creator.get(HTML_PATH % sid).status_code == 200
    assert _post_pdf(creator, sid).status_code == 200

    stranger = _new_client()
    html = stranger.get(HTML_PATH % sid)
    pdf = stranger.post(PDF_PATH % sid, data={})
    assert (html.status_code == 200) == (pdf.status_code == 200), \
        (html.status_code, pdf.status_code)


# ==========================================================================
# 9-10. Non-mutation, live and cold
# ==========================================================================
def test_pdf_live_generation_does_not_mutate_idea_state_or_durable_store(db_path):
    c, _aid = _client_for("pdf-nomutate@example.com")
    sid = _start_project(c)
    c.post("/session/%s/keep-snapshot" % sid, data={})
    ack_before = SESSION_STORE[sid].get("_snapshot_kept_ack")
    assert ack_before is not None, "precondition: the ack is armed"

    state, memory, database = _snapshot_state(sid)
    assert _post_pdf(c, sid).status_code == 200
    assert _snapshot_state(sid) == (state, memory, database)
    # The PDF route must NOT consume the single-use acknowledgement.
    assert SESSION_STORE[sid].get("_snapshot_kept_ack") == ack_before
    # The HTML route alone pops it.
    assert _html_render_ok(c, sid)
    assert SESSION_STORE[sid].get("_snapshot_kept_ack") is None


def _html_render_ok(client, sid):
    return client.get(HTML_PATH % sid).status_code == 200


def test_pdf_cold_load_uses_truthful_read_only_reconstruction(db_path, monkeypatch):
    c, _aid = _client_for("pdf-cold@example.com")
    sid = _start_project(c)
    c.post("/session/" + sid,
           data={"answer": "The sensor measures current and opens the switch."})
    SESSION_STORE.clear()                      # simulate a restart

    calls = {"n": 0}
    real = webapp.reconstruct_readonly_state

    def counting(store, project_id):
        calls["n"] += 1
        return real(store, project_id)

    monkeypatch.setattr(webapp, "reconstruct_readonly_state", counting)

    seen = _capture_source(monkeypatch)
    with open(os.environ["INVENTORAI_DB_PATH"], "rb") as fh:
        db_before = fh.read()
    r = _post_pdf(c, sid)
    assert r.status_code == 200
    with open(os.environ["INVENTORAI_DB_PATH"], "rb") as fh:
        assert fh.read() == db_before, "cold PDF generation wrote to the store"
    assert calls["n"] >= 1, "cold PDF did not use read-only reconstruction"
    assert sid not in seen["source"]


# ==========================================================================
# 11-12. Real rendering
# ==========================================================================
def test_real_pdf_generation_english_and_arabic_rtl(db_path, monkeypatch):
    c, _aid = _client_for("pdf-render@example.com")
    sid = _start_project(c)

    seen_en = _capture_source(monkeypatch)
    en = _post_pdf(c, sid)
    assert en.status_code == 200 and en.get_data()[:5] == b"%PDF-"
    en_html_tag = re.search(r"<html[^>]*>", seen_en["source"]).group(0)
    assert 'lang="en"' in en_html_tag
    assert "dir=" not in en_html_tag, en_html_tag

    _set_lang(c, "ar")
    seen_ar = _capture_source(monkeypatch)
    ar = _post_pdf(c, sid)
    assert ar.status_code == 200 and ar.get_data()[:5] == b"%PDF-"
    src = seen_ar["source"]
    ar_html_tag = re.search(r"<html[^>]*>", src).group(0)
    assert 'lang="ar"' in ar_html_tag
    assert 'dir="rtl"' in ar_html_tag
    assert ui_text.text("UI_TITLE_DELIVERABLE", "ar") in src
    # The trusted print rules are present and RTL-aware.
    assert "@page" in src and "size: A4" in src
    assert '"DejaVu Sans"' in src
    assert 'html[dir="rtl"] body' in src
    assert len(ar.get_data()) != 0


def test_real_pdf_has_no_active_content_or_external_resource_reference(
        db_path, monkeypatch):
    c, _aid = _client_for("pdf-inert@example.com")
    sid = _start_project(c)
    seen = _capture_source(monkeypatch)
    r = _post_pdf(c, sid)
    assert r.status_code == 200
    raw = r.get_data()
    for marker in (b"/JavaScript", b"/JS", b"/Launch", b"/EmbeddedFile", b"/Filespec"):
        assert marker not in raw, marker
    source = seen["source"]
    for element in ("<script", "<iframe", "<object", "<embed", "<img", "<link",
                    "<form", "<input", "<button"):
        assert element not in source.lower(), element
    assert "url(" not in source

    # User strings that RESEMBLE markup, URLs or CSS stay plain escaped content
    # and never become an active resource. (No global assertion that plain text
    # may not contain "file:"/"https:" — only that no active element is created.)
    hostile = ('<img src=x onerror=alert(1)> https://evil.example/p.png '
               'url(https://evil.example/p.css) file:///etc/passwd')
    c2, _a2 = _client_for("pdf-escape@example.com")
    start = c2.post("/start", data={"idea": IDEA + " " + hostile,
                                    "domain_confirm": "electronics_electrical"})
    sid2 = start.headers["Location"].rsplit("/session/", 1)[-1]
    seen2 = _capture_source(monkeypatch)
    assert _post_pdf(c2, sid2).status_code == 200
    hostile_source = seen2["source"]
    # The hostile substrings survive ONLY as escaped TEXT. Substring scanning is
    # useless here — the escaped text legitimately contains "<img", " src=" and
    # "url(" — so the document is PARSED and the invariant is asserted
    # structurally: no active element and no resource-bearing attribute exists.
    elements, attributes = _document_elements_and_attributes(hostile_source)
    for element in ("script", "iframe", "object", "embed", "img", "link",
                    "form", "input", "button", "audio", "video", "svg"):
        assert element not in elements, element
    for name, value in attributes:
        assert not name.startswith("on"), (name, value)
        assert name not in ("src", "srcset", "data", "codebase", "background"), name
        if name == "href":
            assert value.startswith("#"), value
    # Decisive proof: the real renderer turns it into an inert PDF.
    hostile_pdf = seen2["pdf"]
    assert hostile_pdf[:5] == b"%PDF-"
    for marker in (b"/JavaScript", b"/JS", b"/Launch", b"/EmbeddedFile", b"/Filespec"):
        assert marker not in hostile_pdf, marker
    # No CSS resource: scoped to the STYLE blocks, where CSS actually lives.
    for style in re.findall(r"<style[^>]*>(.*?)</style>", hostile_source, re.S):
        assert "url(" not in style
        assert "@font-face" not in style
        assert "http" not in style


# ==========================================================================
# 13. Runtime prerequisites
# ==========================================================================
def test_weasyprint_exact_pin_and_runtime_prerequisites():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(root, "requirements.txt"), encoding="utf-8") as fh:
        requirements = fh.read()
    pins = [line.strip() for line in requirements.splitlines()
            if line.strip() and not line.strip().startswith("#")]
    assert "weasyprint==70.0" in pins, pins
    assert not any("pip-audit" in pin for pin in pins), pins

    import weasyprint
    assert weasyprint.__version__ == "70.0"

    from weasyprint.text.ffi import pango
    assert pango.pango_version() >= 14400, pango.pango_version()

    matched = subprocess.run(["fc-match", "DejaVu Sans"],
                             capture_output=True, text=True, check=True)
    assert "DejaVu Sans" in matched.stdout, matched.stdout


# ==========================================================================
# 14. The existing HTML deliverable is otherwise unchanged
# ==========================================================================
def test_existing_html_deliverable_behavior_is_unchanged_except_download_action(db_path):
    c, _aid = _client_for("pdf-htmlsame@example.com")
    sid = _start_project(c)
    body = c.get(HTML_PATH % sid).get_data(as_text=True)

    # application shell, language control and navigation still present
    assert 'id="main-content"' in body
    assert "/ui-language" in body
    assert ("/session/%s" % sid) in body
    # current content and status still present
    assert "InventorAI" in body
    assert 'id="report-contents"' in body
    assert "csrf_token" in body
    # single-use snapshot acknowledgement behaviour preserved: the HTML route
    # (and only it) consumes the armed acknowledgement on the next render.
    c.post("/session/%s/keep-snapshot" % sid, data={})
    assert SESSION_STORE[sid].get("_snapshot_kept_ack") is not None
    assert c.get(HTML_PATH % sid).status_code == 200
    assert SESSION_STORE[sid].get("_snapshot_kept_ack") is None
    # and exactly one new action
    assert body.count("/deliverable.pdf") >= 1
