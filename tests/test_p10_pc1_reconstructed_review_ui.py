"""P10-PC1 — User-Visible Reconstructed Review State (cold-load session truth).

File-creation contract:
  Path: tests/test_p10_pc1_reconstructed_review_ui.py
  Purpose: behaviour tests for the bounded product gate that surfaces the
    ALREADY-MERGED P4-2 Level-1 deterministic read-only reconstruction
    (engine.session_reconstruction.reconstruct_review_state — zero production
    call sites before this gate) on the cold-loaded session page, replacing the
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
    return app.test_client()


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


def test_reconstruction_failure_fails_closed_to_prior_page(client, monkeypatch):
    sid, _, _ = _journey(client)

    def _boom(*_a, **_k):
        raise RuntimeError("forced reconstruction failure")
    monkeypatch.setattr(webapp, "reconstruct_review_state", _boom)
    r = client.get("/session/" + sid)
    assert r.status_code == 200                              # never a 500
    body = r.get_data(as_text=True)
    assert CLAIM_EN not in html.unescape(body)               # no false recon claim
    assert 'name="response"' in body                         # prior cold page kept
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
