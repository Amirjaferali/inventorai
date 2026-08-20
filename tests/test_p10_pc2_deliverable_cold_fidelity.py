"""P10-PC2 — Cold-Load Deliverable Fidelity (truthful report after restart).

File-creation contract:
  Path: tests/test_p10_pc2_deliverable_cold_fidelity.py
  Purpose: behaviour tests for the bounded product gate that makes the
    deliverable — the product's primary output — truthful for a cold-loaded
    (post-restart) session by assembling it from the Level-1 deterministic
    read-only reconstruction. Base defects proven live: (1) a DIRECT GET of a
    cold project's deliverable redirects away (no cold-load fallback); (2) an
    indirectly rehydrated cold deliverable is FALSE in ten sections (claims
    "problem statement not yet established", HIGH Level-0 risk, zero
    gaps/requirements/assumptions, lost prototype plan) despite durable truth.
  Input contract: the live web app, the durable store (conftest per-test DB
    isolation), real /start→answer journeys; memory loss simulated by
    removing the SESSION_STORE entry (durable DB persists) — the P4-2/P10-PC1
    convention.
  Output contract: pass/fail evidence only; sessions cleaned up; no durable
    artifact left behind.
  Prohibited behaviors: NO doubles for the journey; NO weakening of the
    non-resume boundary (the deliverable surface is GET-only and stays so);
    NO duplication of replay logic in tests (parity is asserted against the
    canonical assembler + reconstruction seams).
"""
import html
import json
import re

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE, assemble_deliverable

CLAIM_EN = ("View a read-only reconstruction of this idea's current review state, "
            "recomputed from its saved inputs and accepted answers. "
            "This is not a resumed session.")

ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"
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


def _token(client, sid):
    body = client.get("/session/" + sid).get_data(as_text=True)
    return re.search(r'name="answer_token" value="([^"]+)"', body).group(1)


def _journey(client):
    """Real journey to maturity 1 (problem established, mechanism partial),
    capture the LIVE deliverable package, then simulate a restart.
    Returns (sid, live_package)."""
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    for answer in (ANSWER_1, ANSWER_1, ANSWER_2):
        rr = client.post("/session/" + sid, data={
            "response": answer, "action": "answered",
            "answer_token": _token(client, sid)})
        assert rr.status_code == 302
    live_state = SESSION_STORE[sid]["state"]
    assert live_state.maturity_level == 1          # the journey really advanced
    live_package = assemble_deliverable(live_state)
    SESSION_STORE.pop(sid)                         # simulated restart
    return sid, live_package


def _strip_volatile(package):
    p = json.loads(json.dumps(package, default=str))
    p.pop("generated_at", None)                    # wall-clock stamp
    return p


# ==========================================================================
# Truthful cold deliverable (RED: false/degraded or unreachable today)
# ==========================================================================
def test_direct_cold_deliverable_get_reachable(client):
    """A direct bookmark to the deliverable of a saved project must work after
    a restart (no prior session-page visit) — today it redirects away."""
    sid, _ = _journey(client)
    r = client.get("/session/%s/deliverable" % sid)
    assert r.status_code == 200
    body = html.unescape(r.get_data(as_text=True))
    assert "brake light" in body                   # durable truth rendered
    SESSION_STORE.pop(sid, None)


def test_cold_deliverable_package_matches_live_truth(client):
    """The cold deliverable must equal the pre-restart live package (modulo
    the wall-clock stamp): same assessment completeness, gaps, requirements,
    assumptions, risks, recommendations, and prototype plan."""
    sid, live_package = _journey(client)
    client.get("/session/%s/deliverable" % sid)    # render path executed cold
    cold_state = SESSION_STORE[sid]["state"]
    # the render path must have used the TRUTHFUL reconstructed package; we
    # assert the user-visible outcome through the page itself below and the
    # package parity through the same canonical seams the route uses:
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(webapp._get_store(), sid)
    assert recon.review.level == 1
    cold_package = assemble_deliverable(recon.state)
    assert _strip_volatile(cold_package) == _strip_volatile(live_package)
    assert cold_state is not recon.state           # never rehydrated as live state
    SESSION_STORE.pop(sid, None)


def test_cold_deliverable_page_shows_true_sections(client):
    sid, _ = _journey(client)
    body = html.unescape(client.get("/session/%s/deliverable" % sid)
                         .get_data(as_text=True))
    text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))
    # truthful maturity-1 statements, not the false level-0 reset claims
    assert "PARTIAL — mechanism or boundaries still required" in text
    assert "problem statement not yet established" not in text
    assert "accelerometer" in text                 # captured mechanism evidence
    SESSION_STORE.pop(sid, None)


def test_cold_deliverable_carries_reconstruction_claim(client):
    sid, _ = _journey(client)
    body = html.unescape(client.get("/session/%s/deliverable" % sid)
                         .get_data(as_text=True))
    assert CLAIM_EN in body
    SESSION_STORE.pop(sid, None)


def test_live_deliverable_unchanged_no_claim(client):
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    body = html.unescape(client.get("/session/%s/deliverable" % sid)
                         .get_data(as_text=True))
    assert CLAIM_EN not in body                    # live pages carry no claim
    SESSION_STORE.pop(sid, None)


def test_cold_deliverable_arabic_claim(client):
    sid, _ = _journey(client)
    client.post("/ui-language", data={"lang": "ar"})
    body = html.unescape(client.get("/session/%s/deliverable" % sid)
                         .get_data(as_text=True))
    assert "ليست جلسة مستأنفة" in body             # the same claim, localized
    SESSION_STORE.pop(sid, None)


# ==========================================================================
# Preservation — fail-closed, read-only, engine seam unchanged
# ==========================================================================
def test_reconstruction_failure_fails_closed_to_prior_behavior(client, monkeypatch):
    sid, _ = _journey(client)
    client.get("/session/" + sid)                  # rehydrate (P4-1b-1 path)

    def _boom(*_a, **_k):
        raise RuntimeError("forced reconstruction failure")
    monkeypatch.setattr(webapp, "reconstruct_readonly_state", _boom)
    r = client.get("/session/%s/deliverable" % sid)
    assert r.status_code == 200                    # never a 500
    assert CLAIM_EN not in html.unescape(r.get_data(as_text=True))
    SESSION_STORE.pop(sid, None)


def test_cold_deliverable_render_makes_no_durable_write(client):
    sid, _ = _journey(client)
    store = webapp._get_store()
    before = len(store.load_accepted_answer_evidence(sid))
    client.get("/session/%s/deliverable" % sid)
    client.get("/session/%s/deliverable" % sid)
    assert len(store.load_accepted_answer_evidence(sid)) == before == 3
    SESSION_STORE.pop(sid, None)


def test_reconstruct_review_state_behavior_unchanged(client):
    """The additive engine accessor must not alter the merged P4-2 Level-1
    seam: reconstruct_review_state returns the identical review snapshot."""
    sid, _ = _journey(client)
    from engine.session_reconstruction import (
        reconstruct_review_state, reconstruct_readonly_state)
    store = webapp._get_store()
    old = reconstruct_review_state(store, sid)
    new = reconstruct_readonly_state(store, sid)
    assert old == new.review                       # byte-identical snapshot
    assert new.state is not None and new.state.maturity_level == old.maturity_level
    SESSION_STORE.pop(sid, None)


def test_unknown_project_deliverable_still_generic_redirect(client):
    r = client.get("/session/no-such-project/deliverable")
    assert r.status_code == 302                    # non-enumerating, unchanged
