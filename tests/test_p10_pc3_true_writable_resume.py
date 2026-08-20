"""P10-PC3 — True Writable Resume (implementation of the authoritative contract).

File-creation contract:
  Path: tests/test_p10_pc3_true_writable_resume.py
  Purpose: behaviour tests for the LEVEL-1 implementation of
    `docs/governance/P10_PC3_TRUE_WRITABLE_RESUME_INCREMENT_CONTRACT.md`:
    continuation of the SAME DURABLE PROJECT in a NEW transient writable
    context via an EXPLICIT establishment POST (`/session/<sid>/resume`) —
    never an automatic GET side effect, never a claimed restoration of the
    original in-memory session. Base truth (probed live): the route does not
    exist (404) and a cold project cannot continue answering.
  Input contract: the live web app, the durable store (conftest per-test DB
    isolation), real /start→answer journeys; restart simulated by removing
    the SESSION_STORE entry while the durable DB persists (the governed
    P4-2/PC1/PC2 convention).
  Output contract: pass/fail evidence only; sessions cleaned up; no durable
    artifact left behind.
  Prohibited behaviors: NO activation doubles; NO fabricated transcript/
    last_result/non-answer history; NO weakening of ownership or fail-closed
    assertions; the ONLY monkeypatch-crafted reconstruction is the
    completed-project eligibility probe (documented inline) — every other
    path is the real replay.
"""
import html
import re

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from engine import account_credentials as _acct

PW = "Str0ng-Passw0rd!"
ELEC_IDEA = "ESP32 microcontroller circuit with a voltage sensor"
ANSWER_1 = ("The problem is that cyclists have no reliable brake light. My circuit "
            "senses deceleration with an accelerometer because sudden voltage change "
            "on the sensor indicates braking, so the microcontroller switches the LED "
            "because riders behind need warning.")
ANSWER_2 = ("The mechanism works because the accelerometer outputs a voltage "
            "proportional to deceleration; the microcontroller reads it through the "
            "ADC and drives the LED through a transistor because the LED current "
            "exceeds the GPIO limit.")
ANSWER_3 = ("The circuit uses a 3.3V regulator because the battery voltage varies; "
            "the sensor connects over I2C with pull-up resistors, and a fuse "
            "protects against overcurrent because a short would damage the battery.")

RESUMED_EN = "Resumed project — reconstructed continuation"
RESUMED_AR = "تم استئناف المشروع — متابعة مُعاد بناؤها"


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def _token(client, sid):
    body = client.get("/session/" + sid).get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', body)
    return m.group(1) if m else None


def _answer(client, sid, response):
    return client.post("/session/" + sid, data={
        "response": response, "action": "answered",
        "answer_token": _token(client, sid)})


def _store():
    return webapp._get_store()


def _journey(client, answers=(ANSWER_1, ANSWER_2)):
    """Real journey, then restart. Returns (sid, live_maturity, live_gaps,
    live_question, durable_count)."""
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    for a in answers:
        assert _answer(client, sid, a).status_code == 302
    live = SESSION_STORE[sid]["state"]
    facts = (sid, live.maturity_level,
             [(g.gap_type, g.status) for g in live.gaps],
             (SESSION_STORE[sid].get("last_result") or {}).get("question"),
             len(_store().load_accepted_answer_evidence(sid)))
    SESSION_STORE.pop(sid)
    return facts


def _resume(client, sid):
    return client.post("/session/%s/resume" % sid, data={})


# ==========================================================================
# Establishment: explicit, eligible, non-durable, truthful
# ==========================================================================
def test_eligible_cold_project_establishes_writable_continuation(client):
    sid, live_mat, live_gaps, _, n = _journey(client)
    r = _resume(client, sid)
    assert r.status_code == 302
    state = SESSION_STORE[sid]["state"]
    assert getattr(state, "domain", None) == "electronics_electrical"
    assert state.maturity_level == live_mat            # replay parity
    assert [(g.gap_type, g.status) for g in state.gaps] == live_gaps
    body = html.unescape(client.get("/session/" + sid).get_data(as_text=True))
    assert 'name="response"' in body                   # answering available again
    assert RESUMED_EN in body                          # truthful mode banner
    assert "restored" not in body.lower()              # no false restoration claim
    SESSION_STORE.pop(sid, None)


def test_establishment_is_explicit_and_non_durable(client):
    """GET never establishes; the establishment POST itself writes nothing
    durable; the un-established cold view stays read-only before it."""
    sid, _, _, _, n = _journey(client)
    client.get("/session/" + sid)                      # cold GET: view only
    assert getattr(SESSION_STORE[sid]["state"], "domain", None) is None
    before = len(_store().load_accepted_answer_evidence(sid))
    assert _resume(client, sid).status_code == 302     # explicit establishment
    assert len(_store().load_accepted_answer_evidence(sid)) == before == n
    assert getattr(SESSION_STORE[sid]["state"], "domain", None) is not None
    SESSION_STORE.pop(sid, None)


def test_unestablished_cold_state_remains_unanswerable(client):
    """The successor of the blanket non-resume pin: WITHOUT establishment the
    cold view offers no form/token and a forged POST fails closed with no
    durable event (PC1 semantics preserved verbatim)."""
    sid, _, _, _, n = _journey(client)
    body = client.get("/session/" + sid).get_data(as_text=True)
    assert 'name="response"' not in body
    assert 'name="answer_token"' not in body
    r = client.post("/session/" + sid, data={
        "response": "forged continuation because the guard must hold.",
        "action": "answered", "answer_token": "forged-token"})
    assert r.status_code == 302
    assert len(_store().load_accepted_answer_evidence(sid)) == n
    assert getattr(SESSION_STORE[sid]["state"], "domain", None) is None
    SESSION_STORE.pop(sid, None)


def test_resumed_next_question_matches_pre_restart_truth(client):
    sid, _, _, live_q, _ = _journey(client)
    assert live_q                                      # engine served one live
    _resume(client, sid)
    body = html.unescape(client.get("/session/" + sid).get_data(as_text=True))
    assert live_q in body                              # same deterministic question
    SESSION_STORE.pop(sid, None)


# ==========================================================================
# History integrity + exactly-once continuation
# ==========================================================================
def test_prior_answers_unchanged_and_n_plus_1_appends_exactly_once(client):
    sid, _, _, _, n = _journey(client)
    before = [(rec.record_id, rec.content)
              for rec in _store().load_accepted_answer_evidence(sid)]
    _resume(client, sid)
    assert _answer(client, sid, ANSWER_3).status_code == 302
    after = _store().load_accepted_answer_evidence(sid)
    assert len(after) == n + 1                          # exactly one new record
    assert [(rec.record_id, rec.content) for rec in after[:n]] == before
    assert after[-1].content == ANSWER_3
    SESSION_STORE.pop(sid, None)


def test_duplicate_retry_does_not_reappend(client):
    sid, _, _, _, n = _journey(client)
    _resume(client, sid)
    token = _token(client, sid)
    for _ in range(3):                                  # browser/network retries
        client.post("/session/" + sid, data={
            "response": ANSWER_3, "action": "answered", "answer_token": token})
    assert len(_store().load_accepted_answer_evidence(sid)) == n + 1
    SESSION_STORE.pop(sid, None)


def test_stale_multitab_submission_does_not_duplicate(client):
    """A stale page (same consumed token, DIFFERENT content) after another tab
    advanced the project must fail closed — no duplicate, no corruption."""
    sid, _, _, _, n = _journey(client)
    _resume(client, sid)
    stale_token = _token(client, sid)                   # both tabs rendered this
    assert client.post("/session/" + sid, data={        # tab 1 advances
        "response": ANSWER_3, "action": "answered",
        "answer_token": stale_token}).status_code == 302
    mat = SESSION_STORE[sid]["state"].maturity_level
    r = client.post("/session/" + sid, data={           # tab 2, stale, different
        "response": "A completely different stale answer because tab two lagged.",
        "action": "answered", "answer_token": stale_token})
    assert r.status_code == 302
    assert len(_store().load_accepted_answer_evidence(sid)) == n + 1
    assert SESSION_STORE[sid]["state"].maturity_level == mat   # no corruption
    body = html.unescape(client.get("/session/" + sid).get_data(as_text=True))
    assert "could not be saved" in body                 # honest fail-closed message
    SESSION_STORE.pop(sid, None)


def test_cross_project_forged_token_fails(client):
    sid_a, _, _, _, _ = _journey(client)
    _resume(client, sid_a)
    token_a = _token(client, sid_a)
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    sid_b = r.headers["Location"].rsplit("/", 1)[-1]
    n_b = len(_store().load_accepted_answer_evidence(sid_b))
    client.post("/session/" + sid_b, data={
        "response": ANSWER_3, "action": "answered", "answer_token": token_a})
    assert len(_store().load_accepted_answer_evidence(sid_b)) == n_b
    SESSION_STORE.pop(sid_a, None); SESSION_STORE.pop(sid_b, None)


def test_restart_after_resume_resumes_again(client):
    sid, _, _, _, n = _journey(client)
    _resume(client, sid)
    _answer(client, sid, ANSWER_3)
    mat_after = SESSION_STORE[sid]["state"].maturity_level
    SESSION_STORE.pop(sid)                              # second restart
    _resume(client, sid)
    state = SESSION_STORE[sid]["state"]
    assert state.maturity_level == mat_after            # replay incl. N+1
    assert len(_store().load_accepted_answer_evidence(sid)) == n + 1
    SESSION_STORE.pop(sid, None)


# ==========================================================================
# Ownership / eligibility / fail-closed
# ==========================================================================
def _mk_verified_client(email):
    store = webapp._get_account_store()
    aid = _acct.new_account_id()
    store.create_account(aid, _acct.normalize_email(email),
                         _acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status="active")
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    c = app.test_client()
    c.post("/login", data={"email": email, "password": PW})
    return c


def test_cross_account_resume_denied(client):
    owner = _mk_verified_client("pc3-owner@example.com")
    r = owner.post("/start", data={"idea": ELEC_IDEA,
                                   "domain_confirm": "electronics_electrical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    SESSION_STORE.pop(sid)
    intruder = _mk_verified_client("pc3-intruder@example.com")
    r = intruder.post("/session/%s/resume" % sid, data={})
    assert r.status_code == 302                         # generic denial
    assert sid not in SESSION_STORE or \
        getattr(SESSION_STORE[sid]["state"], "domain", None) is None
    anonymous = app.test_client()
    r = anonymous.post("/session/%s/resume" % sid, data={})
    assert r.status_code == 302
    assert sid not in SESSION_STORE or \
        getattr(SESSION_STORE[sid]["state"], "domain", None) is None
    SESSION_STORE.pop(sid, None)


def test_completed_project_does_not_reopen(client, monkeypatch):
    """Eligibility probe for the completed case. Crafting a genuinely completed
    real journey is disproportionate here, so the reconstruction seam is
    monkeypatched to return a REAL replayed state mutated to the completed
    shape (maturity 2, no open gaps) — the route's own eligibility logic is
    what is under test; every other test in this file uses the real replay."""
    sid, _, _, _, _ = _journey(client)
    from engine.session_reconstruction import reconstruct_readonly_state
    real = reconstruct_readonly_state(_store(), sid)
    real.state.maturity_level = 2
    for g in real.state.gaps:
        g.status = "CLOSED"
    monkeypatch.setattr(webapp, "reconstruct_readonly_state",
                        lambda *_a, **_k: real)
    r = _resume(client, sid)
    assert r.status_code == 302
    entry = SESSION_STORE.get(sid)
    assert entry is None or getattr(entry["state"], "domain", None) is None
    SESSION_STORE.pop(sid, None)


def test_non_activated_domain_not_establishable(client, monkeypatch):
    """Eligibility probe for the deactivated/unsupported-domain case (same
    documented monkeypatch convention as the completed-case probe): a Level-1
    reconstruction whose domain is recognized-but-NOT-activated must be
    refused establishment — no resume-specific admission path exists."""
    sid, _, _, _, _ = _journey(client)
    from engine.session_reconstruction import reconstruct_readonly_state
    real = reconstruct_readonly_state(_store(), sid)
    real.state.domain = "medical_device"               # recognized, NOT activated
    monkeypatch.setattr(webapp, "reconstruct_readonly_state",
                        lambda *_a, **_k: real)
    r = _resume(client, sid)
    assert r.status_code == 302
    entry = SESSION_STORE.get(sid)
    assert entry is None or getattr(entry["state"], "domain", None) is None
    SESSION_STORE.pop(sid, None)


def test_reconstruction_failure_fails_closed_readonly(client, monkeypatch):
    sid, _, _, _, _ = _journey(client)

    def _boom(*_a, **_k):
        raise RuntimeError("forced reconstruction failure")
    monkeypatch.setattr(webapp, "reconstruct_readonly_state", _boom)
    r = _resume(client, sid)
    assert r.status_code == 302                         # never a 500
    entry = SESSION_STORE.get(sid)
    assert entry is None or getattr(entry["state"], "domain", None) is None
    SESSION_STORE.pop(sid, None)


def test_unknown_project_resume_generic(client):
    r = client.post("/session/no-such-project/resume", data={})
    assert r.status_code == 302                         # non-enumerating


# ==========================================================================
# PC1 / PC2 preservation + EN/AR truth
# ==========================================================================
def test_pc1_readonly_view_preserved_before_establishment(client):
    sid, _, _, _, _ = _journey(client)
    body = html.unescape(client.get("/session/" + sid).get_data(as_text=True))
    assert "This is not a resumed session." in body     # exact PC1 claim intact
    assert 'name="response"' not in body
    SESSION_STORE.pop(sid, None)


def test_pc2_cold_deliverable_preserved(client):
    sid, _, _, _, _ = _journey(client)
    body = html.unescape(client.get("/session/%s/deliverable" % sid)
                         .get_data(as_text=True))
    assert "This is not a resumed session." in body
    SESSION_STORE.pop(sid, None)


def test_resumed_banner_arabic(client):
    sid, _, _, _, _ = _journey(client)
    _resume(client, sid)
    client.post("/ui-language", data={"lang": "ar"})
    body = html.unescape(client.get("/session/" + sid).get_data(as_text=True))
    assert RESUMED_AR in body
    SESSION_STORE.pop(sid, None)


def test_no_fabricated_history_in_resumed_context(client):
    sid, _, _, _, _ = _journey(client)
    _resume(client, sid)
    entry = SESSION_STORE[sid]
    assert entry["transcript"] == []                    # never fabricated
    assert entry["last_result"] is None
    assert "interaction_actions" not in entry
    SESSION_STORE.pop(sid, None)


# ==========================================================================
# B1 repair (Independent Review REJECT of ee8a0dad…): record-id collision
# after resume with interleaved non-answer history. Non-answer structured
# actions consume in-memory rec_N identifiers without durable persistence;
# after restart the reconstructed ledger holds only the durable answered
# subset, so a length-derived mint can re-mint an existing durable id and
# the durable append fails with a PRIMARY KEY collision that no retry can
# ever clear. The mint authority must be the ledger's max rec_N (equal to
# the durable max after reconstruction), never the ledger length.
# ==========================================================================
def _nonanswer(client, sid, text="I do not know this yet because I lack data."):
    r = client.post("/session/" + sid, data={
        "response": text, "action": "unknown",
        "answer_token": _token(client, sid) or "unused"})
    assert r.status_code == 302


def test_b1_interleaved_nonanswer_history_resume_appends_safely(client):
    """The reviewer's exact reproduction: answered -> non-answer action ->
    answered -> restart -> resume -> new answered must append exactly once
    (no rec_N collision, no permanently failing retry)."""
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    assert _answer(client, sid, ANSWER_1).status_code == 302   # rec_1 (durable)
    _nonanswer(client, sid)                                    # rec_2 (memory only)
    assert _answer(client, sid, ANSWER_2).status_code == 302   # rec_3 (durable)
    durable = _store().load_accepted_answer_evidence(sid)
    assert [rec.record_id for rec in durable] == ["rec_1", "rec_3"]  # sparse by design
    SESSION_STORE.pop(sid)
    assert _resume(client, sid).status_code == 302
    assert _answer(client, sid, ANSWER_3).status_code == 302   # must NOT collide
    after = _store().load_accepted_answer_evidence(sid)
    assert len(after) == 3                                     # exactly once
    assert after[-1].content == ANSWER_3
    assert after[-1].record_id not in ("rec_1", "rec_3")       # no historical reuse
    body = html.unescape(client.get("/session/" + sid).get_data(as_text=True))
    assert "could not be saved" not in body                    # no stuck failure
    SESSION_STORE.pop(sid, None)


def test_b1_multiple_interleaved_nonanswers_and_sparse_ids(client):
    """Denser interleaving: several never-durable actions between answers
    produce a sparser durable history; resume must still append safely."""
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    _nonanswer(client, sid, "Deferred because I need to check the datasheet first.")
    _nonanswer(client, sid, "I would need a specialist for the EMC question.")
    assert _answer(client, sid, ANSWER_1).status_code == 302   # rec_3 (durable)
    _nonanswer(client, sid, "Provisionally assuming a 2 m/s^2 threshold for now.")
    assert _answer(client, sid, ANSWER_2).status_code == 302   # rec_5 (durable)
    durable = _store().load_accepted_answer_evidence(sid)
    assert [rec.record_id for rec in durable] == ["rec_3", "rec_5"]
    SESSION_STORE.pop(sid)
    assert _resume(client, sid).status_code == 302
    assert _answer(client, sid, ANSWER_3).status_code == 302
    after = _store().load_accepted_answer_evidence(sid)
    assert len(after) == 3
    assert [rec.record_id for rec in after[:2]] == ["rec_3", "rec_5"]  # unchanged
    assert int(after[-1].record_id[4:]) > 5                    # past the durable max
    SESSION_STORE.pop(sid, None)


def test_b1_restart_after_repaired_resume_appends_again(client):
    """Second restart after a repaired sparse-history resume: the cycle must
    stay collision-free indefinitely."""
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    assert _answer(client, sid, ANSWER_1).status_code == 302
    _nonanswer(client, sid)
    assert _answer(client, sid, ANSWER_2).status_code == 302
    SESSION_STORE.pop(sid)
    _resume(client, sid)
    assert _answer(client, sid, ANSWER_3).status_code == 302   # first repaired append
    SESSION_STORE.pop(sid)                                     # restart again
    _resume(client, sid)
    extra = ("The threshold is set at 2 m/s^2 because normal coasting stays "
             "below that; the firmware debounces the signal because vibration "
             "causes false positives.")
    assert _answer(client, sid, extra).status_code == 302      # second repaired append
    after = _store().load_accepted_answer_evidence(sid)
    assert len(after) == 4
    assert len({rec.record_id for rec in after}) == 4          # all ids unique
    SESSION_STORE.pop(sid, None)


def test_b1_pure_answered_history_unchanged(client):
    """Equivalence pin: with a contiguous all-answered ledger the repaired
    mint must produce exactly the ids the previous length-derived mint
    produced (rec_1..rec_N in order) — live behavior byte-identical."""
    r = client.post("/start", data={"idea": ELEC_IDEA,
                                    "domain_confirm": "electronics_electrical"})
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    for a in (ANSWER_1, ANSWER_2, ANSWER_3):
        assert _answer(client, sid, a).status_code == 302
    durable = _store().load_accepted_answer_evidence(sid)
    assert [rec.record_id for rec in durable] == ["rec_1", "rec_2", "rec_3"]
    SESSION_STORE.pop(sid, None)
