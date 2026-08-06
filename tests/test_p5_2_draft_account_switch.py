"""P5-2 §15 — Draft Level 2 account-switch isolation on a shared device (RED/GREEN).

Proven in REAL headless Chromium against REAL rendered templates and REAL
``localStorage`` (server-only tests cannot prove client storage). A local draft
typed while signed in as account A must NEVER be surfaced under account B or
anonymously on the same device — and must NOT be silently deleted (it remains for
account A). Phase 5 consumes, and does not replace, Draft Level 2, and never
uploads the draft.

Chromium is pre-provisioned (``/opt/pw-browsers``); ``playwright`` is a TEST-ONLY
dependency. Missing browser → skip (or fail loudly when
INVENTORAI_DRAFT_L2_REQUIRE_BROWSER=1), matching the Draft L2 suite.
"""
import glob
import os
import re
import threading

import pytest

import web.app as webapp
from web.app import app
from engine import account_credentials as _acct

_REQUIRE_BROWSER = os.environ.get("INVENTORAI_DRAFT_L2_REQUIRE_BROWSER") == "1"
try:
    from playwright.sync_api import sync_playwright
except Exception as _exc:  # pragma: no cover - environment-dependent
    if _REQUIRE_BROWSER:
        raise RuntimeError(
            "P5-2 draft account-switch browser test requires the test-only "
            "'playwright' dependency (tests/requirements-draft-l2.txt).") from _exc
    pytest.skip("needs the test-only 'playwright' dependency", allow_module_level=True)

PW = "correct horse battery staple"
SEED_ANON_KEY = "inventorai:draft:v1:__seed__:idea:seed:v1"


def _chromium_exe():
    for pat in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                "/opt/pw-browsers/chromium/chrome-linux/chrome"):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None


@pytest.fixture
def server():
    from werkzeug.serving import make_server
    srv = make_server("127.0.0.1", 0, app, threaded=True)
    port = srv.server_port
    th = threading.Thread(target=srv.serve_forever, daemon=True)
    th.start()
    try:
        yield "http://127.0.0.1:%d" % port
    finally:
        srv.shutdown()
        th.join(timeout=5)


@pytest.fixture(scope="module")
def _browser():
    exe = _chromium_exe()
    with sync_playwright() as p:
        kw = {"headless": True, "args": ["--no-sandbox"]}
        if exe:
            kw["executable_path"] = exe
        browser = p.chromium.launch(**kw)
        yield browser
        browser.close()


@pytest.fixture
def page(_browser):
    ctx = _browser.new_context()
    pg = ctx.new_page()
    try:
        yield pg
    finally:
        ctx.close()


def _mk_account(email):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email),
                         _acct.hash_password(PW), "2026-01-01T00:00:00.000000Z")
    return aid


def _login(page, base, email):
    page.goto(base + "/login")
    page.fill("#email", email)
    page.fill("#password", PW)
    page.click("button[type=submit]")
    page.wait_for_load_state()


def _logout(page, base):
    page.goto(base + "/account")
    page.click('form[action="/logout"] button[type=submit]')
    page.wait_for_load_state()


def _type_seed_draft(page, base, text):
    page.goto(base + "/")
    page.fill("#idea", text)
    page.dispatch_event("#idea", "input")
    page.wait_for_timeout(1100)          # exceed the 800ms debounce so save() runs


def test_local_draft_isolated_across_account_switch(server, page):
    base = server
    a_id = _mk_account("switch-a@example.com")
    _mk_account("switch-b@example.com")

    # --- signed in as A: type a seed draft; it is stored under A's namespace ---
    _login(page, base, "switch-a@example.com")
    _type_seed_draft(page, base, "A private overcurrent cutoff idea")
    acct_keys = page.evaluate(
        "() => Object.keys(localStorage).filter(k => k.indexOf(':acct:') >= 0)")
    assert any((":acct:" + a_id) in k for k in acct_keys)
    # the anonymous seed key was NOT written while signed in
    assert page.evaluate("() => localStorage.getItem('%s')" % SEED_ANON_KEY) is None

    # --- sign out → anonymous: A's draft must NOT be offered, NOT deleted -------
    _logout(page, base)
    page.goto(base + "/")
    assert page.query_selector(".draft-recovery") is None      # not surfaced to anon
    assert page.evaluate("() => localStorage.getItem('%s')" % SEED_ANON_KEY) is None
    still_there = page.evaluate(
        "() => Object.keys(localStorage).filter(k => k.indexOf(':acct:%s') >= 0).length" % a_id)
    assert still_there == 1                                     # A's draft preserved

    # --- sign in as B: still not offered (B has its own empty namespace) --------
    _login(page, base, "switch-b@example.com")
    page.goto(base + "/")
    assert page.query_selector(".draft-recovery") is None

    # --- back to A: the draft is offered again and restores A's text -----------
    _logout(page, base)
    _login(page, base, "switch-a@example.com")
    page.goto(base + "/")
    box = page.query_selector(".draft-recovery")
    assert box is not None
    page.click(".draft-restore")
    assert page.eval_on_selector("#idea", "el => el.value") == "A private overcurrent cutoff idea"
