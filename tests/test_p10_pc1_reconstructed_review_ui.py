"""P10-PC1 — User-Visible Reconstructed Review State (cold-load session truth).

File-creation contract:
  Path: tests/test_p10_pc1_reconstructed_review_ui.py
  Purpose: behaviour tests for the bounded product gate that surfaces the
    ALREADY-MERGED P4-2 Level-1 deterministic read-only reconstruction
    (engine.session_reconstruction — zero production call sites before this
    gate; served since PERF-01 by the single canonical
    `reconstruct_readonly_state` accessor whose `.review` IS the
    `reconstruct_review_state` snapshot) on the cold-loaded session page,
    replacing the
    current cold-load render that shows a FALSE LEVEL-0 maturity display, a
    generic domain label, no gaps, no question, and an answer form whose every
    submission fails closed with a "try again" message.
  Input contract: the live web app, the durable record store (conftest per-test
    DB isolation), and real /start→answer journeys; memory loss is simulated by
    removing the SESSION_STORE entry while the durable DB persists — the same
    convention the merged P4-2 suite uses.
  Output contract: pass/fail evidence only; admitted sessions are removed in
    cleanup; no durable artifact left behind.
  Prohibited behaviors: NO activation doubles; NO SESSION_STORE seeding for the
    journey tests (real /start only); NO weakening of the committed P4-1b-2a
    non-resume guard (a reconstructed view must remain unanswerable); the gate
    must NOT restore `state.domain` (display-only truth; the cold-load marker
    and its fail-closed guarantee stay intact).

Authorized product claim (exact, from the merged P4-2 Level-1 module):
  "View a read-only reconstruction of this idea's current review state,
   recomputed from its saved inputs and accepted answers. This is not a
   resumed session."
"""
from tests.csrf_client import csrf_client
import html
import re

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from web.gap_labels import get_maturity_label

CLAIM_EN = ("View a read-only reconstruction of this idea's current review state, "
            "recomputed from its saved inputs and accepted answers. "
            "This is not a resumed session.")

EN_ELECTRONICS = "Electronics-informed review"
EN_MECHANICAL = "Mechanical-informed review"

ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"
MECH_IDEA = "A hinge mounted bracket with a lever and a spring latch"

# Substantive causal answers that really advance the deterministic engine
# (problem establishment, then mechanism) — verified against the live journey.
ANSWER_1 = ("The problem is that cyclists have no reliable brake light. My circuit "
            "senses deceleration with an accelerometer because sudden voltage change "
            "on the sensor indicates braking, so the microcontroller switches the LED "
            "because riders behind need warning.")
ANSWER_2 = ("The mechanism works because the accelerometer outputs a voltage "
            "proportional to deceleration; the microcontroller reads it through the "
            "ADC and drives the LED through a transistor because the LED current "
            "exceeds the GPIO limit.")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return csrf_client(app)


def _start(client, idea=ELEC_IDEA, domain="electronics_electrical"):
    r = client.post("/start", data={"idea": idea, "domain_confirm": domain})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _token(client, sid):
    body = client.get("/session/" + sid).get_data(as_text=True)
    return re.search(r'name="answer_token" value="([^"]+)"', body).group(1)


def _answer(client, sid, response):
    r = client.post("/session/" + sid, data={
        "response": response, "action": "answered",
        "answer_token": _token(client, sid)})
    assert r.status_code == 302


def _journey(client, idea=ELEC_IDEA, domain="electronics_electrical"):
    """Real journey to maturity 1 with an open MECHANISM gap, then memory loss.
    Returns (sid, live_maturity, live_question)."""
    sid = _start(client, idea, domain)
    _answer(client, sid, ANSWER_1)          # WARN: problem not yet established
    _answer(client, sid, ANSWER_1)          # PASS: problem established -> LEVEL 1
    live = SESSION_STORE[sid]["state"]
    live_maturity = live.maturity_level
    live_question = (SESSION_STORE[sid].get("last_result") or {}).get("question")
    SESSION_STORE.pop(sid)                  # simulated restart; durable DB persists
    return sid, live_maturity, live_question


# ==========================================================================
# Reconstructed review state rendered (RED: missing product behavior today)
# ==========================================================================
def test_cold_page_shows_true_maturity_and_tier1_domain(client):
    sid, live_maturity, _ = _journey(client)
    assert live_maturity == 1               # journey really advanced the engine
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert EN_ELECTRONICS in body           # Tier-1 label, not the generic fallback
    # the truthful reconstructed maturity label (level 1), not the false
    # reset level-0 display the cold page previously showed
    assert get_maturity_label(1)["label"] in body        # "Problem established"
    assert get_maturity_label(0)["label"] not in body    # reset display gone
    SESSION_STORE.pop(sid, None)


def test_cold_page_shows_claim_and_suppresses_dead_form(client):
    sid, _, _ = _journey(client)
    body = client.get("/session/" + sid).get_data(as_text=True)
    # html.unescape: the claim contains an apostrophe ("idea's"), which Jinja
    # autoescape renders as &#39; — unescape before the exact-claim comparison
    assert CLAIM_EN in html.unescape(body)                   # exact authorized claim
    assert 'name="response"' not in body                     # dead-end form gone
    assert 'name="answer_token"' not in body
    SESSION_STORE.pop(sid, None)


def test_cold_page_shows_next_question_and_open_gap(client):
    sid, _, live_question = _journey(client)
    assert live_question                                     # engine served one live
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert live_question in body                             # same deterministic question
    assert "MECHANISM" in body or "Mechanism" in body or "mechanism" in body
    SESSION_STORE.pop(sid, None)


def test_cold_page_shows_accepted_answer_count(client):
    sid, _, _ = _journey(client)
    body = client.get("/session/" + sid).get_data(as_text=True)
    # anchored to the dedicated element so an unrelated "2" (e.g. the progress
    # bar) can never satisfy this: two accepted answers were replayed
    m = re.search(r'id="recon-answer-count"[^>]*>\s*2\s*<', body)
    assert m, "labeled accepted-answer count of 2 not rendered"
    SESSION_STORE.pop(sid, None)


def test_cold_page_mechanical_tier1_label(client):
    sid = _start(client, MECH_IDEA, "mechanical")
    SESSION_STORE.pop(sid)
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert EN_MECHANICAL in body
    assert CLAIM_EN in html.unescape(body)
    SESSION_STORE.pop(sid, None)


def test_cold_page_arabic_claim(client):
    sid, _, _ = _journey(client)
    r = client.post("/ui-language", data={"lang": "ar"})
    assert r.status_code in (200, 302)
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert bool(re.search(r"[؀-ۿ]", body))         # Arabic present
    assert "ليست جلسة مستأنفة" in body                        # "not a resumed session"
    assert 'name="response"' not in body
    SESSION_STORE.pop(sid, None)


# ==========================================================================
# Preservation — live pages, fail-closed paths, and the non-resume guard
# ==========================================================================
def test_live_page_unchanged(client):
    sid = _start(client)
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert 'name="response"' in body                         # live form intact
    assert CLAIM_EN not in html.unescape(body)               # no claim on live pages
    SESSION_STORE.pop(sid, None)


def test_reconstruction_failure_fails_closed_to_readonly_recovery(client, monkeypatch):
    sid, _, _ = _journey(client)
    before = webapp._get_store().load_contract(sid).to_json()

    def _boom(*_a, **_k):
        raise RuntimeError("forced reconstruction failure")
    # PERF-01: the cold page now runs ONE reconstruction pass through the
    # canonical `reconstruct_readonly_state` accessor, so the failure seam is
    # retargeted to it. The intent is unchanged and undiminished: an exception
    # raised by reconstruction must never reach the user as a 500 or a false
    # reconstruction claim, and must not disturb the durable contract.
    monkeypatch.setattr(webapp, "reconstruct_readonly_state", _boom)
    r = client.get("/session/" + sid)
    assert r.status_code == 200                              # never a 500
    body = r.get_data(as_text=True)
    assert CLAIM_EN not in html.unescape(body)               # no false recon claim
    # A1 removes the unusable cold answer box; it does not establish writable
    # continuation or reinterpret a failed reconstruction as a completed journey.
    assert 'name="response"' not in body
    assert 'id="resume-project"' not in body
    assert 'class="complete"' not in body
    assert "Saved view" in body and body.count("data-primary-action") == 1
    assert getattr(SESSION_STORE[sid]["state"], "domain", None) is None
    assert webapp._get_store().load_contract(sid).to_json() == before
    rejected = client.post("/session/" + sid, data={
        "response": "A forged answer must not revive this project.",
        "action": "answered", "answer_token": "forged-token"})
    assert rejected.status_code == 302
    assert webapp._get_store().load_contract(sid).to_json() == before
    SESSION_STORE.pop(sid, None)


def test_non_resume_guard_untouched(client):
    """A forged direct POST against a reconstructed view still fails closed —
    the committed P4-1b-2a guard is preserved, not weakened, by this gate."""
    sid, _, _ = _journey(client)
    client.get("/session/" + sid)                            # render cold view
    state = SESSION_STORE[sid]["state"]
    assert getattr(state, "domain", None) is None            # marker NOT restored
    r = client.post("/session/" + sid, data={
        "response": "forged continuation because the guard must hold.",
        "action": "answered", "answer_token": "forged-token"})
    assert r.status_code == 302
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert "could not be saved" in body                      # fail-closed message
    SESSION_STORE.pop(sid, None)


def test_cold_render_makes_no_durable_write(client):
    sid, _, _ = _journey(client)
    store = webapp._get_store()
    before = len(store.load_accepted_answer_evidence(sid))
    client.get("/session/" + sid)
    client.get("/session/" + sid)
    assert len(store.load_accepted_answer_evidence(sid)) == before == 2
    SESSION_STORE.pop(sid, None)


# ==========================================================================
# PERF-01 — ONE reconstruction pass per cold page
#
# The gate is a DETERMINISTIC OPERATION COUNT, not a timing threshold: the cold
# page must run the canonical reconstruction accessor exactly once and must not
# run a second replay for the banner's display state. Nothing here asserts
# elapsed time.
# ==========================================================================
def _count_recon(monkeypatch):
    """Count `reconstruct_readonly_state` calls made through the web module,
    leaving behaviour untouched."""
    calls = []
    real = webapp.reconstruct_readonly_state

    def counting(store, project_id):
        calls.append(project_id)
        return real(store, project_id)
    monkeypatch.setattr(webapp, "reconstruct_readonly_state", counting)
    return calls


def _count_contract_loads(monkeypatch):
    """Count full `load_contract()` calls (deserialization + validation) on the
    real store class."""
    from engine.record_store import SqliteRecordStore
    calls = []
    real = SqliteRecordStore.load_contract

    def counting(self, project_id):
        calls.append(project_id)
        return real(self, project_id)
    monkeypatch.setattr(SqliteRecordStore, "load_contract", counting)
    return calls


def test_perf01_cold_page_runs_exactly_one_reconstruction_pass(client, monkeypatch):
    """ONE canonical accessor call AND — the load-bearing half — exactly ONE
    underlying deterministic reconstruction/replay pass. The page used to run
    two passes over the same durable history for one request."""
    import engine.session_reconstruction as SR
    passes = []
    real_reconstruct = SR._reconstruct

    def counting(store, project_id):
        passes.append(project_id)
        return real_reconstruct(store, project_id)
    monkeypatch.setattr(SR, "_reconstruct", counting)
    sid, _, _ = _journey(client)
    calls = _count_recon(monkeypatch)
    passes.clear()
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert CLAIM_EN in html.unescape(body)          # a real Level-1 render
    assert calls == [sid], calls                    # one canonical accessor call
    assert passes == [sid], passes                  # one reconstruction pass
    SESSION_STORE.pop(sid, None)


def test_perf01_cold_page_never_calls_reconstruct_review_state(client, monkeypatch):
    """Structural AND behavioural proof. The web module no longer binds
    `reconstruct_review_state` at all, and forcing the engine's own function to
    explode leaves the cold page fully working — so no path reaches it."""
    import engine.session_reconstruction as SR
    assert not hasattr(webapp, "reconstruct_review_state")

    def _boom(*_a, **_k):
        raise AssertionError("reconstruct_review_state must not run on the cold page")
    monkeypatch.setattr(SR, "reconstruct_review_state", _boom)
    sid, _, live_question = _journey(client)
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert CLAIM_EN in html.unescape(body)
    assert live_question and live_question in body
    SESSION_STORE.pop(sid, None)


def test_perf01_cold_page_performs_two_full_contract_loads(client, monkeypatch):
    """The successful known Level-1 cold page keeps exactly TWO safe full
    contract loads — the durable `_cold_load_entry` rebuild and the ONE
    reconstruction pass. The five it used to perform are gone, and the two
    remaining are deliberately NOT collapsed by rehydrating the render-only
    reconstructed state into SESSION_STORE."""
    sid, _, _ = _journey(client)
    loads = _count_contract_loads(monkeypatch)
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert CLAIM_EN in html.unescape(body)
    assert loads == [sid, sid], loads
    SESSION_STORE.pop(sid, None)


def test_perf01_cold_entry_stays_minimal_and_non_resumable(client):
    """The SESSION_STORE entry is still the minimal cold entry — NOT the
    render-only reconstructed state — so the committed P4-1b-2a non-resume
    guard (`state.domain is None`) is untouched and an answer still fails
    closed without changing the durable contract."""
    sid, _, _ = _journey(client)
    before = webapp._get_store().load_contract(sid).to_json()
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert CLAIM_EN in html.unescape(body)
    entry_state = SESSION_STORE[sid]["state"]
    assert getattr(entry_state, "domain", None) is None      # cold marker intact
    # The reconstructed render-only state is a DIFFERENT object that carries the
    # persisted domain; it was never placed into SESSION_STORE.
    import engine.session_reconstruction as SR
    recon = SR.reconstruct_readonly_state(webapp._get_store(), sid)
    assert recon.state is not entry_state
    assert getattr(recon.state, "domain", None) == "electronics_electrical"
    assert entry_state.assertions is not recon.state.assertions
    rejected = client.post("/session/" + sid, data={
        "response": "A forged answer must not revive this project.",
        "action": "answered", "answer_token": "forged-token"})
    assert rejected.status_code == 302
    assert webapp._get_store().load_contract(sid).to_json() == before
    SESSION_STORE.pop(sid, None)


def test_perf01_level1_wrapper_without_state_suppresses_the_claim(client, monkeypatch):
    """A Level-1 review WITHOUT a reconstructed state is not a valid
    reconstruction: the claim is suppressed rather than rendered from a missing
    state, and the page still returns 200 with no dead answer form."""
    import engine.session_reconstruction as SR
    sid, _, _ = _journey(client)
    real = webapp.reconstruct_readonly_state(webapp._get_store(), sid)
    assert real.review.level == 1 and real.state is not None
    monkeypatch.setattr(
        webapp, "reconstruct_readonly_state",
        lambda *_a, **_k: SR.ReconstructedReadonlySession(
            review=real.review, state=None))
    r = client.get("/session/" + sid)
    assert r.status_code == 200                                  # never a 500
    body = r.get_data(as_text=True)
    assert CLAIM_EN not in html.unescape(body)                   # no false claim
    assert 'name="response"' not in body
    SESSION_STORE.pop(sid, None)


def test_perf01_valid_state_with_failing_localization_falls_back_to_english(
        client, monkeypatch):
    """A DIFFERENT invariant from the one above: once a valid non-None state
    exists, a failure inside the display resolution falls back to the canonical
    English reconstruction evidence — the claim is still rendered."""
    sid, _, live_question = _journey(client)
    assert live_question

    hit = []

    def _boom(*_a, **_k):
        hit.append(1)
        raise RuntimeError("forced localization resolution failure")
    monkeypatch.setattr(webapp, "_rvr7_identity", _boom)
    client.post("/ui-language", data={"lang": "ar"})
    r = client.get("/session/" + sid)
    assert r.status_code == 200
    body = r.get_data(as_text=True)
    assert hit, "the display-resolution seam was never reached"
    assert live_question in body            # canonical English evidence rendered
    SESSION_STORE.pop(sid, None)


def test_perf01_english_and_arabic_cold_banners_unchanged(client):
    """EN/AR cold-page display parity is structurally and semantically the same
    after the single-pass change: the English page renders the canonical English
    ask, the Arabic page renders Arabic with the localized claim, and the
    question element never declares a language its text does not have."""
    sid, _, live_question = _journey(client)
    assert live_question
    en = client.get("/session/" + sid).get_data(as_text=True)
    assert CLAIM_EN in html.unescape(en)
    assert live_question in en
    SESSION_STORE.pop(sid, None)

    sid2, _, live_question2 = _journey(client)
    client.post("/ui-language", data={"lang": "ar"})
    ar = client.get("/session/" + sid2).get_data(as_text=True)
    assert bool(re.search(r"[؀-ۿ]", ar))
    assert "ليست جلسة مستأنفة" in ar
    assert 'name="response"' not in ar
    m = re.search(
        r'<p class="question"[^>]*lang="([a-z]{2})"[^>]*dir="(ltr|rtl)"[^>]*>(.*?)</p>',
        ar, re.S)
    if m:
        lang, direction, text = m.group(1), m.group(2), m.group(3).strip()
        assert (lang == "ar") == bool(re.search(r"[؀-ۿ]", text))
        assert (direction == "rtl") == (lang == "ar")
    SESSION_STORE.pop(sid2, None)
