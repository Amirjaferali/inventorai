"""Draft Level 2 — Same-Device Unsubmitted-Text Recovery (RED/GREEN).

Behaviour-based tests for the bounded Draft Level 2 increment authorized by
`G-DRAFT-L2-LOCAL-CONTINUITY-IMPLEMENTATION-01` (contract
`G-DRAFT-L2-LOCAL-CONTINUITY-CONTRACT-01`, merged PR #371).

The client behaviours (real browser `localStorage` surviving reload/offline/
close, explicit recovery, stale/expired/corrupt rejection, no-network save,
storage-failure fail-closed, submit cleanup) are proven against **real rendered
templates in real headless Chromium** via Playwright — server-only tests cannot
prove client storage. The semantic-boundary proofs (a draft never reaches the
server / creates no `AssertionRecord` / triggers no evaluation / changes no
durable state; the no-JavaScript path stays valid Level 0; idempotency still
prevents duplicates) are proven server-side with the Flask test client and the
durable store.

Chromium is pre-provisioned (`/opt/pw-browsers`); the browser is launched via
`executable_path` (no download). `playwright` is a TEST-ONLY dependency
(`tests/requirements-draft-l2.txt`). Fail-closed, no false-green: each assertion
inspects real browser storage / DOM / the durable store, never mere existence.
"""
import glob
import json
import os
import re
import threading

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from engine.record_store import SqliteRecordStore

# By default a missing 'playwright' skips these browser tests so the full governed
# suite stays green where a browser is unavailable. Set
# INVENTORAI_DRAFT_L2_REQUIRE_BROWSER=1 to make the DEDICATED Draft L2 run FAIL
# LOUDLY (never silently skip) when the test-only dependency/browser is missing.
_REQUIRE_BROWSER = os.environ.get("INVENTORAI_DRAFT_L2_REQUIRE_BROWSER") == "1"
try:
    from playwright.sync_api import sync_playwright
except Exception as _exc:  # pragma: no cover - environment-dependent
    if _REQUIRE_BROWSER:
        raise RuntimeError(
            "Draft L2 browser tests require the test-only 'playwright' dependency "
            "(pip install -r tests/requirements-draft-l2.txt); Chromium is "
            "pre-installed at PLAYWRIGHT_BROWSERS_PATH. Unset "
            "INVENTORAI_DRAFT_L2_REQUIRE_BROWSER to allow skipping.") from _exc
    pytest.skip(
        "Draft L2 browser tests need the test-only 'playwright' dependency "
        "(tests/requirements-draft-l2.txt); set "
        "INVENTORAI_DRAFT_L2_REQUIRE_BROWSER=1 to fail instead of skip.",
        allow_module_level=True)

FORM = {"domain_confirm": "electronics_electrical"}
IDEA = ("An electronic overcurrent cutoff uses a sense resistor and a comparator "
        "so that when the current exceeds a threshold the relay opens.")
ANSWER = ("When the current through the sense resistor rises, the voltage across "
          "it crosses the comparator reference, the output flips, and it opens the relay.")


def _chromium_exe():
    for pat in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome",
                "/opt/pw-browsers/chromium/chrome-linux/chrome"):
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return None


# --- live server (function-scoped: conftest resets the store/SESSION_STORE) ----
@pytest.fixture
def server():
    from werkzeug.serving import make_server
    # Match the supported single-thread serving topology: the cached SQLite
    # stores must be used and closed on the thread that creates them.
    srv = make_server("127.0.0.1", 0, app, threaded=False)
    port = srv.server_port
    server_errors = []

    def serve():
        try:
            srv.serve_forever(poll_interval=0.05)
        except Exception as exc:
            server_errors.append(exc)
        finally:
            for name in ("_STORE", "_ACCOUNT_STORE"):
                store = getattr(webapp, name)
                if store is not None:
                    try:
                        store.close()
                    except Exception as exc:
                        server_errors.append(exc)
                    finally:
                        setattr(webapp, name, None)

    th = threading.Thread(target=serve, daemon=True)
    th.start()
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        srv.shutdown()
        th.join(timeout=5)
        srv.server_close()
        assert not th.is_alive(), "test server did not stop"
        assert not server_errors, f"test server/store cleanup failed: {server_errors!r}"


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


# --- helpers ------------------------------------------------------------------
def _start(page, base, idea=IDEA):
    page.goto(base + "/")
    page.fill("#idea", idea)
    _present_domain_confirmation(page, idea)
    return _confirm_start(page)


def _present_domain_confirmation(page, idea=IDEA):
    # With Electronics and Mechanical active, the first submit classifies the
    # idea; it must not create a session or silently supply explicit consent.
    assert page.locator("input[name=domain_confirm]").count() == 0
    page.click("input[type=submit], button[type=submit]")
    page.wait_for_load_state()
    assert page.url.endswith("/start")
    assert page.input_value("#idea") == idea
    choices = page.locator("input[name=domain_choice]")
    if choices.count():
        # The unrelated-session fixture has no classified domain. Follow the
        # real chooser rather than treating its Electronics intent as consent.
        assert sorted(choices.evaluate_all("els => els.map(e => e.value)")) == [
            "electronics_electrical", "mechanical"]
        page.check('input[name=domain_choice][value="electronics_electrical"]')
        page.click("input[type=submit], button[type=submit]")
        page.wait_for_load_state()
        assert page.url.endswith("/start")
        assert page.input_value("#idea") == idea
    confirmation = page.locator("input[name=domain_confirm]")
    assert confirmation.count() == 1
    assert confirmation.input_value() == "electronics_electrical"
    assert not confirmation.is_checked()


def _confirm_start(page):
    page.check("input[name=domain_confirm]")
    page.click("input[type=submit], button[type=submit]")
    page.wait_for_load_state()
    assert "/session/" in page.url
    return page.url.rsplit("/session/", 1)[1].split("?")[0]


def _answer_key(page):
    return page.evaluate(
        "() => Object.keys(localStorage).filter(k => k.indexOf(':answer:') >= 0)")


SEED_KEY = "inventorai:draft:v1:__seed__:idea:seed:v1"


# ===========================================================================
# 1. Seed idea text survives reload (RED: no autosave on parent -> lost)
# ===========================================================================
def test_seed_idea_survives_reload(server, page):
    page.goto(server + "/")
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)  # debounce flush
    stored = page.evaluate(f"localStorage.getItem('{SEED_KEY}')")
    assert stored and IDEA in stored
    page.reload()
    assert page.eval_on_selector("#idea", "e => e.value") == ""  # not auto-filled
    assert page.locator(".draft-recovery .draft-restore").count() == 1
    page.click(".draft-recovery .draft-restore")
    assert page.eval_on_selector("#idea", "e => e.value") == IDEA


# ===========================================================================
# 2. Main answer text survives reload before submit
# ===========================================================================
def test_main_answer_survives_reload(server, page):
    _start(page, server)
    page.fill("#response", ANSWER)
    page.wait_for_timeout(1000)
    assert _answer_key(page), "answer draft not stored"
    page.reload()
    assert page.eval_on_selector("#response", "e => e.value") == ""
    assert page.locator(".draft-recovery .draft-restore").count() == 1
    page.click(".draft-recovery .draft-restore")
    assert page.eval_on_selector("#response", "e => e.value") == ANSWER


# ===========================================================================
# 3. Offline typing remains locally recoverable
# ===========================================================================
def test_offline_typing_retained(server, page):
    sid = _start(page, server)
    page.context.set_offline(True)
    page.fill("#response", ANSWER)
    page.wait_for_timeout(1000)
    keys = _answer_key(page)
    assert keys, "offline draft not stored locally"
    page.context.set_offline(False)
    page.reload()
    assert page.locator(".draft-recovery .draft-restore").count() == 1


# ===========================================================================
# 4. Interruption (pagehide) preserves the latest saved local version
# ===========================================================================
def test_interruption_preserves_latest(server, page):
    _start(page, server)
    page.fill("#response", ANSWER)
    # Simulate an interruption flush via pagehide, then navigate away and back.
    page.evaluate("window.dispatchEvent(new Event('pagehide'))")
    page.wait_for_timeout(100)
    assert _answer_key(page), "pagehide flush did not persist the draft"
    page.reload()
    assert page.locator(".draft-recovery .draft-restore").count() == 1


# ===========================================================================
# 5/6. Matching draft offered; never silently overwrites newer visible text
# ===========================================================================
def test_matching_draft_offered_for_restore(server, page):
    page.goto(server + "/")
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)
    page.reload()
    assert page.locator(".draft-recovery").count() == 1


def test_no_silent_overwrite_of_newer_text(server, page):
    # A stored draft exists, but the field already holds newer text on load:
    page.goto(server + "/")
    page.evaluate(
        "(k) => localStorage.setItem(k, JSON.stringify({v:1,text:'OLD DRAFT TEXT',"
        "ts:Date.now(),scope:'__seed__',field:'idea',context:'seed',ctxver:'v1'}))",
        SEED_KEY)
    page.eval_on_selector("#idea", "e => { e.value = 'newer typed text'; }")
    page.evaluate("() => document.dispatchEvent(new Event('DOMContentLoaded'))")
    page.wait_for_timeout(100)
    # No prompt is shown and the newer visible text is untouched.
    assert page.locator(".draft-recovery").count() == 0
    assert page.eval_on_selector("#idea", "e => e.value") == "newer typed text"


# ===========================================================================
# 7/8/9. Wrong session / wrong field-or-question / stale-context not restored
# ===========================================================================
def test_wrong_session_draft_not_restored(server, page):
    sid = _start(page, server)
    # A draft under a DIFFERENT session scope must never be offered here.
    page.evaluate(
        "() => localStorage.setItem('inventorai:draft:v1:other-sid:answer:ctx:v1',"
        "JSON.stringify({v:1,text:'FOREIGN',ts:Date.now(),scope:'other-sid',"
        "field:'answer',context:'ctx',ctxver:'v1'}))")
    page.reload()
    assert page.locator(".draft-recovery").count() == 0


def test_stale_context_draft_not_restored(server, page):
    sid = _start(page, server)
    # Store a draft under the CURRENT answer key but with a MISMATCHED stored
    # context (a stale/changed question); the defence-in-depth check rejects it.
    ctx = page.eval_on_selector("#response", "e => e.getAttribute('data-draft-context')")
    key = f"inventorai:draft:v1:{sid}:answer:{ctx}:v1"
    page.evaluate(
        "(k) => localStorage.setItem(k, JSON.stringify({v:1,text:'STALE',"
        "ts:Date.now(),scope:'X',field:'answer',context:'DIFFERENT',ctxver:'v1'}))",
        key)
    page.reload()
    assert page.locator(".draft-recovery").count() == 0


# ===========================================================================
# 10. Expired draft is not restored (and is purged)
# ===========================================================================
def test_expired_draft_not_restored(server, page):
    page.goto(server + "/")
    page.evaluate(
        "(k) => localStorage.setItem(k, JSON.stringify({v:1,text:'OLD',"
        "ts: Date.now() - 8*24*60*60*1000, scope:'__seed__',field:'idea',"
        "context:'seed',ctxver:'v1'}))", SEED_KEY)
    page.reload()
    assert page.locator(".draft-recovery").count() == 0
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')") is None  # purged


# ===========================================================================
# 11. Corrupted draft is ignored safely (and purged), no crash
# ===========================================================================
def test_corrupted_draft_ignored(server, page):
    page.goto(server + "/")
    page.evaluate(f"localStorage.setItem('{SEED_KEY}', 'not-json{{')")
    page.reload()
    assert page.locator(".draft-recovery").count() == 0
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')") is None
    # The page and its form remain usable.
    assert page.locator("#idea").count() == 1


# ===========================================================================
# 12. localStorage failure is truthful and does not block submission
# ===========================================================================
def test_storage_failure_nonblocking(server, page):
    # Fail ONLY the draft write (quota) so the init probe still succeeds and the
    # feature wires up — the actual save then fails and reports it truthfully.
    page.add_init_script(
        "(() => { const orig = Storage.prototype.setItem;"
        " Storage.prototype.setItem = function(k, v){"
        "   if (typeof k === 'string' && k.indexOf('inventorai:draft:v1:') === 0)"
        "     throw new Error('quota');"
        "   return orig.apply(this, arguments); }; })();")
    page.goto(server + "/")
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)
    status = page.locator(".draft-status").first
    assert "Could not save" in (status.text_content() or "")
    # Submission still works despite the storage failure.
    _present_domain_confirmation(page)
    _confirm_start(page)
    assert "/session/" in page.url


def test_full_storage_unavailable_is_level0(server, page):
    # When localStorage is ENTIRELY unavailable, the feature fails closed to Level
    # 0 (no wiring, no status) and the form still works — no error, no block.
    page.add_init_script(
        "Storage.prototype.setItem = function(){ throw new Error('denied'); };")
    page.goto(server + "/")
    page.fill("#idea", IDEA)
    _present_domain_confirmation(page)
    _confirm_start(page)
    assert "/session/" in page.url


# ===========================================================================
# 13. Failed submission retains the draft (and re-offers it)
# ===========================================================================
def test_failed_submit_retains_draft(server, page):
    sid = _start(page, server)
    page.fill("#response", ANSWER)
    page.wait_for_timeout(1000)
    assert _answer_key(page)
    # Force a token-invalid answered submit (fails closed server-side, PRG back).
    page.eval_on_selector("input[name=answer_token]", "e => { e.value = 'forged'; }")
    page.click("input[type=submit], button[type=submit]")
    page.wait_for_load_state()
    # The draft is still present and offered for recovery.
    assert _answer_key(page), "draft was wrongly cleared on a failed submit"
    assert page.locator(".draft-recovery .draft-restore").count() == 1


# ===========================================================================
# 14. Confirmed successful submission clears only the matching draft
# ===========================================================================
def test_successful_submit_clears_matching_draft(server, page):
    sid = _start(page, server)
    # A foreign draft for another session must survive.
    page.evaluate(
        "() => localStorage.setItem('inventorai:draft:v1:other:answer:c:v1',"
        "JSON.stringify({v:1,text:'KEEP',ts:Date.now(),scope:'other',"
        "field:'answer',context:'c',ctxver:'v1'}))")
    page.fill("#response", ANSWER)
    page.wait_for_timeout(1000)
    assert any(sid in k for k in _answer_key(page)), "sid draft not stored pre-submit"
    page.click("input[type=submit], button[type=submit]")  # real token -> accepted
    page.wait_for_load_state()
    # The matching (this-session) answer draft is cleared; the foreign one survives.
    assert not any(sid in k for k in _answer_key(page)), \
        "matching answer draft not cleared after accept"
    assert page.evaluate(
        "localStorage.getItem('inventorai:draft:v1:other:answer:c:v1')") is not None


# ===========================================================================
# 20. Explicit discard removes only the matching draft
# ===========================================================================
def test_explicit_discard_removes_draft(server, page):
    page.goto(server + "/")
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)
    page.reload()
    page.click(".draft-recovery .draft-discard")
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')") is None
    assert page.locator(".draft-recovery").count() == 0


# ===========================================================================
# 21. No raw draft text in the URL, and no network request on save
# ===========================================================================
def test_no_network_or_url_leak_on_save(server, page):
    reqs = []
    page.on("request", lambda r: reqs.append(r.url + " " + (r.post_data or "")))
    page.goto(server + "/")
    reqs.clear()
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)
    # Saving is localStorage-only: no request is made while typing.
    assert reqs == [], f"unexpected network on draft save: {reqs}"
    # The idea text never appears in the URL.
    assert IDEA not in page.url


# ===========================================================================
# Disclosure present (privacy)
# ===========================================================================
def test_local_draft_disclosure_present(server, page):
    page.goto(server + "/data-and-session")
    body = page.text_content("body") or ""
    assert "this browser on this device only" in body
    assert "expires after 7 days" in body


# ===========================================================================
# 16. Idempotency still prevents duplicate accepted answers (server-side)
# ===========================================================================
def test_idempotency_prevents_duplicate():
    # Server-side proof that the draft feature does not alter the accepted-answer
    # idempotency model: the same token + same content submitted twice yields ONE
    # durable answered record.
    client = app.test_client()
    r = client.post("/start", data={"idea": IDEA, **FORM})
    sid = r.headers["Location"].rsplit("/session/", 1)[1]
    html = client.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token"[^>]*value="([^"]+)"', html)
    token = m.group(1)
    client.post(f"/session/{sid}", data={"response": ANSWER, "answer_token": token})
    client.post(f"/session/{sid}", data={"response": ANSWER, "answer_token": token})
    store = webapp._get_store()
    ev = store.load_accepted_answer_evidence(sid)
    assert len([r for r in ev if r.content == ANSWER]) == 1


# ===========================================================================
# 17/18/19. Draft interaction creates no server draft / record / evaluation
# ===========================================================================
def test_no_server_draft_route_or_record():
    # There is NO server route that accepts or stores a draft; the only durable
    # writes remain create_project + append_record (accepted answers only).
    import inspect
    src = inspect.getsource(webapp)
    assert "append_record" in src  # sanity: the accepted-answer path still exists
    rules = sorted(r.rule for r in app.url_map.iter_rules())
    assert not any("draft" in r.lower() for r in rules), \
        f"no draft server route may exist: {rules}"


def test_rendering_creates_no_records():
    # Rendering the pages (where drafts live entirely client-side) creates no
    # durable answered records and no session mutation beyond normal start.
    client = app.test_client()
    r = client.post("/start", data={"idea": IDEA, **FORM})
    sid = r.headers["Location"].rsplit("/session/", 1)[1]
    client.get(f"/session/{sid}")
    client.get(f"/session/{sid}")
    store = webapp._get_store()
    assert store.load_accepted_answer_evidence(sid) == ()  # no answers appended


# ===========================================================================
# 22. No-JavaScript fallback remains valid Level 0
# ===========================================================================
def test_no_js_fallback_level0():
    # The Flask test client executes no JavaScript; the server-rendered forms and
    # the accepted-answer flow must behave exactly as before (Level 0), unaffected
    # by the additive data-draft-* attributes.
    client = app.test_client()
    r = client.post("/start", data={"idea": IDEA, **FORM})
    assert r.status_code in (301, 302)
    sid = r.headers["Location"].rsplit("/session/", 1)[1]
    html = client.get(f"/session/{sid}").get_data(as_text=True)
    assert 'name="response"' in html and 'name="answer_token"' in html
    m = re.search(r'name="answer_token"[^>]*value="([^"]+)"', html)
    resp = client.post(f"/session/{sid}",
                       data={"response": ANSWER, "answer_token": m.group(1)})
    assert resp.status_code in (301, 302)  # accepted, PRG — no JS required
    assert webapp._get_store().load_accepted_answer_evidence(sid)  # durably appended


# ===========================================================================
# REMEDIATION (G-DRAFT-L2-LOCAL-CONTINUITY-REMEDIATION-01) — B1, B2, B3.
# ===========================================================================

# --- B1: seed draft must not be deleted by rendering an UNRELATED session ----
def test_b1_seed_draft_survives_unrelated_session_nav(server, page):
    # An existing, unrelated session (its own start already consumed its signal).
    sid_a = _start(page, server, idea="A separate electronic relay overcurrent idea for session A.")
    # A NEW, unsubmitted seed idea is typed on the entry page.
    page.goto(server + "/")
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')")
    # Opening the existing unrelated session (bookmark/history) must NOT delete it.
    page.goto(server + f"/session/{sid_a}")
    page.wait_for_load_state()
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')"), \
        "B1: an unrelated session render wrongly deleted the unsent seed draft"


def test_b1_seed_cleared_only_after_matching_start(server, page):
    page.goto(server + "/")
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')")
    _present_domain_confirmation(page)
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')"), \
        "seed draft must survive classification before explicit acceptance"
    _confirm_start(page)
    assert "/session/" in page.url
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')") is None  # matching seed cleared


# --- B2: an untouched/empty field must not delete a stored draft on hide -----
def test_b2a_unrestored_draft_survives_leave_and_return(server, page):
    page.goto(server + "/")
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)
    page.reload()
    assert page.locator(".draft-recovery").count() == 1  # offered; field empty; not restored
    # Leave without restoring/discarding (fires pagehide), then return.
    page.goto(server + "/data-and-session")
    page.wait_for_load_state()
    page.goto(server + "/")
    page.wait_for_load_state()
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')"), \
        "B2: an unrestored (untouched empty field) draft was deleted on leave"
    assert page.locator(".draft-recovery").count() == 1


def test_b2b_intentional_clear_removes_only_matching(server, page):
    page.goto(server + "/")
    page.evaluate(
        "() => localStorage.setItem('inventorai:draft:v1:other:answer:c:v1',"
        "JSON.stringify({v:1,text:'KEEP',ts:Date.now(),scope:'other',"
        "field:'answer',context:'c',ctxver:'v1'}))")
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')")
    # The user intentionally clears the field in this tab.
    page.fill("#idea", "")
    page.wait_for_timeout(1000)
    assert page.evaluate(f"localStorage.getItem('{SEED_KEY}')") is None       # matching removed
    assert page.evaluate(
        "localStorage.getItem('inventorai:draft:v1:other:answer:c:v1')") is not None  # unrelated kept


# --- B3: an empty sibling tab must not delete another tab's draft ------------
def test_b3a_empty_sibling_tab_does_not_delete(server, _browser):
    ctx = _browser.new_context()
    try:
        p1 = ctx.new_page()
        p2 = ctx.new_page()
        p1.goto(server + "/")
        p1.fill("#idea", IDEA)
        p1.wait_for_timeout(1000)
        assert p1.evaluate(f"localStorage.getItem('{SEED_KEY}')")
        p2.goto(server + "/")  # empty field; shares this browser's localStorage
        p2.evaluate("window.dispatchEvent(new Event('pagehide'))")
        p2.evaluate("Object.defineProperty(document, 'visibilityState', "
                    "{get: () => 'hidden', configurable: true}); "
                    "document.dispatchEvent(new Event('visibilitychange'))")
        p1.wait_for_timeout(300)
        assert p1.evaluate(f"localStorage.getItem('{SEED_KEY}')"), \
            "B3: an empty sibling tab deleted the other tab's stored draft"
    finally:
        ctx.close()


def test_b3b_newer_copy_awareness_no_overwrite(server, _browser):
    ctx = _browser.new_context()
    try:
        p1 = ctx.new_page()
        p2 = ctx.new_page()
        p1.goto(server + "/")
        p1.eval_on_selector("#idea", "e => { e.value = 'older visible text in tab one'; }")
        p2.goto(server + "/")
        # Tab 2 saves a NEWER draft -> fires a storage event in tab 1.
        p2.fill("#idea", "NEWER DRAFT TEXT FROM TAB TWO")
        p2.wait_for_timeout(1000)
        p1.wait_for_timeout(400)
        # Tab 1 (non-empty visible text) gets a low-emphasis awareness notice; its
        # visible text is NOT overwritten and the newer stored draft is NOT deleted.
        assert p1.locator(".draft-awareness").count() == 1, \
            "B3: no newer-draft awareness shown in the non-empty tab"
        assert p1.eval_on_selector("#idea", "e => e.value") == "older visible text in tab one"
        assert p2.evaluate(f"localStorage.getItem('{SEED_KEY}')")
    finally:
        ctx.close()


# --- Test-gap closure: correction surface, Arabic locale, ambiguous submit ---
def test_correction_surface_wired():
    from engine.idea_state import IdeaState
    sid = "corr-remediation-sid"
    st = IdeaState(idea_id=sid)
    st.domain = "electronics_electrical"
    st.domain_signal = "electronics_electrical"
    st.maturity_level = 2
    st.current_stage = 3
    SESSION_STORE[sid] = {"state": st, "last_result": None, "transcript": [],
                          "criticality_correction": True}
    try:
        html = app.test_client().get(f"/session/{sid}").get_data(as_text=True)
        assert 'data-draft-field="correction"' in html
        assert "Describe the change or the missing part" in html
    finally:
        SESSION_STORE.pop(sid, None)


def test_arabic_locale_recovery_reachable(server, page):
    page.goto(server + "/")
    page.fill("#idea", IDEA)
    page.wait_for_timeout(1000)
    # Force an Arabic document locale for the next navigation (before the deferred
    # draft script runs), proving the bilingual strings are reachable under `ar`.
    page.add_init_script(
        "const s = () => { if (document.documentElement) "
        "document.documentElement.setAttribute('lang', 'ar'); };"
        "s(); document.addEventListener('readystatechange', s);")
    page.reload()
    assert page.eval_on_selector("html", "e => e.getAttribute('lang')") == "ar"
    box = page.locator(".draft-recovery").first
    assert box.count() == 1
    assert "غير مرسل" in (box.text_content() or "")  # Arabic "unsent"


def test_ambiguous_submit_interrupted_retains_draft(server, page):
    sid = _start(page, server)
    page.fill("#response", ANSWER)
    page.wait_for_timeout(1000)
    assert any(sid in k for k in _answer_key(page))
    # Ambiguous / unconfirmed submission: the client receives NO truthful accepted
    # signal (here a same-origin 503, keeping localStorage readable). The draft
    # must be retained (no accepted-signal cleanup on a non-success result).
    page.route(f"**/session/{sid}",
               lambda route: route.fulfill(status=503, content_type="text/html",
                                           body="temporarily unavailable")
               if route.request.method == "POST" else route.continue_())
    try:
        page.click("input[type=submit], button[type=submit]")
        page.wait_for_timeout(500)
    except Exception:
        pass
    page.unroute(f"**/session/{sid}")
    assert any(sid in k for k in _answer_key(page)), \
        "ambiguous/unconfirmed submit must retain the draft"
