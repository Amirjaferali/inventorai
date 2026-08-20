"""P4-1b-2a — Durable Answered-Event Append + Web-Layer Idempotency (RED/GREEN).

Behaviour-based tests for the bounded P4-1b-2a increment under the merged
contract amendment G-P4-1B-2A-B3-CONTRACT-AMENDMENT-01 (OPTION A):

  * the deterministic engine ``record_id`` stays the positional ``rec_N`` — the
    derived-output engines are UNCHANGED (mixed-id stability, not mutation);
  * a SEPARATE durable idempotency identity (a server-issued-token-derived,
    project-bound HMAC) is stored separately in ``engine.record_store`` and is
    the durable duplicate backstop; it is NEVER an engine identifier;
  * every answered-producing submission MUST carry a valid server-issued token
    (no tokenless fallback); a tokenless / forged / cross-session token fails
    closed;
  * an accepted answer is durably appended EXACTLY ONCE, persist-before-ack, and
    survives a real store restart (cold-load);
  * a duplicate valid-token retry with the same accepted content is an idempotent
    no-op (one durable event); the same token with DIFFERENT content fails
    closed;
  * a validation-error re-render RETAINS the same unconsumed token.

Owner-locked implementation decisions carried by these tests:
  * storage: an additive nullable ``idempotency_key`` column on ``records`` with a
    partial/nullable UNIQUE ``(project_id, idempotency_key)``;
  * digest: ``HMAC-SHA-256(INVENTORAI_SECRET_KEY, sid || token)`` truncated to
    >= 128 bits, using the existing environment secret;
  * fingerprint: ``SHA-256(sid || target_step || resolved_action ||
    exact_accepted_response)`` — exact post-validation accepted value, only
    transport-safe normalisation, no whitespace collapsing.

Behaviour-based, fail-closed, no false-green: assertions inspect the DURABLE
store contents and engine state, never HTTP status or counts alone. The durable
SQLite database lives only under the pytest-managed ``INVENTORAI_DB_PATH`` set by
``tests/conftest.py``. No push / PR / merge is performed by this gate. Scope is
accepted-answer durability + idempotency only — no Keep/Refine durability, no
durable outputs, no replay (P4-2), no accounts (Phase 5).
"""
import os
import re

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from engine.record_store import SqliteRecordStore

IDEA_A = ("An electronic circuit uses a sensor and a switch to cut the power "
          "when the current gets too high.")
FORM = {"domain_confirm": "electronics_electrical"}

# The hidden token field the answered-producing forms must carry.
_TOKEN_RE = re.compile(
    r'name="answer_token"[^>]*value="([^"]+)"|value="([^"]+)"[^>]*name="answer_token"')


@pytest.fixture
def db_path():
    return os.environ["INVENTORAI_DB_PATH"]


def _reset_runtime():
    SESSION_STORE.clear()
    setattr(webapp, "_STORE", None)


def _start(client, idea=IDEA_A):
    resp = client.post("/start", data={"idea": idea, **FORM}, follow_redirects=False)
    loc = resp.headers.get("Location", "")
    assert "/session/" in loc, f"expected /session/<sid> redirect, got {loc!r}"
    return loc.rstrip("/").rsplit("/session/", 1)[1].split("?")[0]


def _render(client, sid):
    return client.get(f"/session/{sid}", follow_redirects=False)


def _token_from_html(html):
    m = _TOKEN_RE.search(html)
    if not m:
        return None
    return m.group(1) or m.group(2)


def _get_token(client, sid):
    html = _render(client, sid).get_data(as_text=True)
    tok = _token_from_html(html)
    assert tok, "no answer_token rendered on the session page"
    return tok


# --- shared EXPLICIT helpers for the B1 existing-test updates -----------------
# These are opt-in helpers, NOT auto-injection: a test that must prove the
# tokenless fail-closed path simply does not call them. They obtain a REAL
# server-issued token from the rendered page and submit it verbatim, weakening no
# assertion. Imported by the enumerated B1 test files so the mandatory-token
# requirement is honoured without duplicating token-fetch logic per file.
def get_answer_token(client, sid):
    """Fetch the server-issued answered-submission token rendered on the session
    page, or None if absent."""
    html = client.get(f"/session/{sid}", follow_redirects=False).get_data(as_text=True)
    return _token_from_html(html)


def answered_post(client, sid, data=None, **kwargs):
    """POST an answered submission to /session/<sid> WITH a freshly obtained real
    token merged in (unless the caller already supplied one). It does NOT create
    or repair any durable project envelope — durable setup is always explicit:
    production ``/start`` (and the legacy start routes) create the envelope, and
    a directly-constructed unit session must call ``seed_direct_session_envelope``
    itself. This helper only obtains a real rendered token and submits it; extra
    form fields pass through unchanged and no assertion is weakened."""
    form = dict(data or {})
    form.setdefault("answer_token", get_answer_token(client, sid))
    return client.post(f"/session/{sid}", data=form, **kwargs)


def seed_direct_session_envelope(sid, state):
    """EXPLICIT durable-envelope seeding for a directly-constructed (non-/start)
    unit-test session — the test's own decision, called at the fixture, never
    hidden inside a request helper. It mirrors exactly what ``/start`` does under
    P4-1b-1 (``create_project(from_state(state), project_id=sid)``) using the one
    canonical store; it makes no claim that arbitrary in-memory sessions are
    automatically durable, weakens nothing, and adds no runtime fallback. Raises
    if the durable creation genuinely fails (so a real defect is never hidden)."""
    from web.app import _get_store
    from engine.record_contract import ProjectRecordContract
    _get_store().create_project(ProjectRecordContract.from_state(state), project_id=sid)


def _durable_answers(db_path, sid):
    """The durably persisted answered records for sid (fresh store handle)."""
    store = SqliteRecordStore(db_path)
    try:
        contract = store.load_contract(sid)
    finally:
        store.close()
    return [r for r in contract.assertions if r.disposition == "answered"]


# --- RED-B1: an answered POST WITHOUT a valid token fails closed --------------
def test_red_b1_tokenless_answered_post_fails_closed(db_path):
    client = app.test_client()
    sid = _start(client)
    before = len(_durable_answers(db_path, sid))
    # No answer_token in the form data.
    client.post(f"/session/{sid}",
                data={"response": "The sensor trips the relay at 5 amps.",
                      "action": "answered"}, follow_redirects=False)
    after = len(_durable_answers(db_path, sid))
    assert after == before, (
        "a tokenless answered submission must not durably append an answer")


# --- RED-B2: the main answer form carries a hidden server-issued token --------
def test_red_b2_main_answer_form_carries_token(db_path):
    client = app.test_client()
    sid = _start(client)
    html = _render(client, sid).get_data(as_text=True)
    assert 'name="answer_token"' in html, (
        "the answered-producing form must carry a hidden answer_token field")
    assert _token_from_html(html), "answer_token must have a server-issued value"


# --- RED-A6a: same token + same content twice => exactly ONE durable answer ---
def test_red_a6a_duplicate_retry_is_idempotent_single_event(db_path):
    client = app.test_client()
    sid = _start(client)
    tok = _get_token(client, sid)
    answer = "The current sensor opens the relay when current exceeds 5 A."
    client.post(f"/session/{sid}",
                data={"response": answer, "action": "answered",
                      "answer_token": tok}, follow_redirects=False)
    first = _durable_answers(db_path, sid)
    assert len(first) == 1, "the first accepted answer must be durably appended once"
    # Duplicate retry with the SAME (now-consumed) token and SAME content.
    client.post(f"/session/{sid}",
                data={"response": answer, "action": "answered",
                      "answer_token": tok}, follow_redirects=False)
    second = _durable_answers(db_path, sid)
    assert len(second) == 1, (
        "a duplicate valid-token retry must be an idempotent no-op (one event)")


# --- RED-A6b: same token + DIFFERENT content => fail closed (no 2nd event) ----
def test_red_a6b_same_token_different_content_fails_closed(db_path):
    client = app.test_client()
    sid = _start(client)
    tok = _get_token(client, sid)
    client.post(f"/session/{sid}",
                data={"response": "First accepted answer about the sensor.",
                      "action": "answered", "answer_token": tok},
                follow_redirects=False)
    one = _durable_answers(db_path, sid)
    assert len(one) == 1
    # Reuse the same token but change the content: must fail closed, no 2nd event.
    client.post(f"/session/{sid}",
                data={"response": "A COMPLETELY DIFFERENT answer body.",
                      "action": "answered", "answer_token": tok},
                follow_redirects=False)
    two = _durable_answers(db_path, sid)
    assert len(two) == 1, (
        "same token with different content must fail closed (no second append)")
    assert two[0].content == one[0].content, "the prior durable content is unchanged"


# --- RED durable-append + real restart cold-load survival --------------------
def test_red_accepted_answer_survives_restart_coldload(db_path):
    client = app.test_client()
    sid = _start(client)
    tok = _get_token(client, sid)
    answer = "A shunt resistor measures current and the MCU opens the relay."
    client.post(f"/session/{sid}",
                data={"response": answer, "action": "answered",
                      "answer_token": tok}, follow_redirects=False)
    # Real restart: drop live memory + store handle; carry only the sid string.
    _reset_runtime()
    answers = _durable_answers(db_path, sid)
    assert any(answer == r.content for r in answers), (
        "the accepted answer must be durably persisted and survive a restart")


# --- RED-A9: the durable store enforces idempotency-key uniqueness ------------
def test_red_a9_store_enforces_idempotency_uniqueness(db_path):
    from engine.record_contract import ProjectRecordContract
    from engine.idea_state import IdeaState
    store = SqliteRecordStore(db_path)
    try:
        st = IdeaState(idea_id="idea-x")
        r1 = st.record_interaction(action="answered", content="one", iteration=1)
        contract = ProjectRecordContract(idea_id="idea-x", assertions=[])
        pid = store.create_project(contract, project_id="proj-unique-x")
        # First append with an idempotency key succeeds.
        store.append_record(pid, r1, idempotency_key="dup-key-123")
        r2 = st.record_interaction(action="answered", content="two", iteration=2)
        # Second append REUSING the same idempotency key must be rejected durably.
        import sqlite3
        with pytest.raises(sqlite3.IntegrityError):
            store.append_record(pid, r2, idempotency_key="dup-key-123")
    finally:
        store.close()


# --- RED-C8: Option A mixed-id STABILITY — record_id stays rec_N (no evt-*) ---
def test_red_c8_record_id_stays_recN_after_durable_append(db_path):
    client = app.test_client()
    sid = _start(client)
    tok = _get_token(client, sid)
    client.post(f"/session/{sid}",
                data={"response": "A relay driven by a comparator on the shunt.",
                      "action": "answered", "answer_token": tok},
                follow_redirects=False)
    _reset_runtime()
    store = SqliteRecordStore(db_path)
    try:
        state = store.load_contract(sid).to_state()
    finally:
        store.close()
    ids = [r.record_id for r in state.assertions]
    assert ids, "durable assertions must be present after cold-load"
    assert all(re.fullmatch(r"rec_\d+", rid) for rid in ids), (
        f"Option A: record_id must remain positional rec_N, got {ids!r}")
    assert not any(rid.startswith("evt-") for rid in ids), (
        "no evt-* id may be adopted as record_id under Option A")


# --- RED persist-before-ack: durable-append failure => no in-memory advance ---
def test_red_persist_before_ack_on_store_failure(db_path, monkeypatch):
    client = app.test_client()
    sid = _start(client)
    tok = _get_token(client, sid)
    # Force the durable append to fail; the accepted answer must NOT be published
    # to live memory and must NOT be durably present (fail closed, no partial).
    import engine.record_store as rs

    def _boom(self, *a, **k):
        raise rs.StoreError("append unavailable")

    monkeypatch.setattr(rs.SqliteRecordStore, "append_record", _boom)
    client.post(f"/session/{sid}",
                data={"response": "This answer must not be half-applied.",
                      "action": "answered", "answer_token": tok},
                follow_redirects=False)
    monkeypatch.undo()
    answers = _durable_answers(db_path, sid)
    assert not any("half-applied" in r.content for r in answers), (
        "a failed durable append must leave no durable answered record")
    live = SESSION_STORE.get(sid)
    if live is not None:
        assert not any("half-applied" in r.content
                       for r in live["state"].assertions), (
            "a failed durable append must not advance in-memory state")


# --- RED obs#2: a validation error RETAINS the same unconsumed token ----------
def test_red_validation_error_retains_same_token(db_path):
    client = app.test_client()
    sid = _start(client)
    tok = _get_token(client, sid)
    # Answer chosen but empty response => validation error, token NOT consumed.
    client.post(f"/session/{sid}",
                data={"response": "   ", "action": "answered",
                      "answer_token": tok}, follow_redirects=False)
    tok_after = _get_token(client, sid)
    assert tok_after == tok, (
        "a validation-error re-render must retain the same unconsumed token")


# --- RED obs#4: distinct valid tokens are independent (no false dedup) --------
def test_red_distinct_tokens_are_independent(db_path):
    client = app.test_client()
    sid = _start(client)
    tok1 = _get_token(client, sid)
    client.post(f"/session/{sid}",
                data={"response": "First distinct accepted answer.",
                      "action": "answered", "answer_token": tok1},
                follow_redirects=False)
    # A fresh render issues a new token; a genuinely new submission is independent.
    tok2 = _get_token(client, sid)
    assert tok2 != tok1, "a consumed token must be rotated on acceptance"
    client.post(f"/session/{sid}",
                data={"response": "Second distinct accepted answer.",
                      "action": "answered", "answer_token": tok2},
                follow_redirects=False)
    answers = _durable_answers(db_path, sid)
    contents = {r.content for r in answers}
    assert "First distinct accepted answer." in contents
    assert "Second distinct accepted answer." in contents, (
        "distinct valid tokens must yield two independent durable answers")


# =============================================================================
# REV1 additions
# =============================================================================

def _state_assertions(sid):
    from web.app import SESSION_STORE
    e = SESSION_STORE.get(sid)
    return list(e["state"].assertions) if e and e.get("state") else []


def _reject_and_assert_unchanged(db_path, sid, token, response="A valid-looking answer body."):
    """Submit an answered POST with the given (bad) token and assert it was
    rejected: no durable answered append, no in-memory ledger growth, and the
    redirect does not acknowledge acceptance."""
    dbefore = len(_durable_answers(db_path, sid))
    sbefore = len(_state_assertions(sid))
    r = app.test_client().post(
        f"/session/{sid}",
        data={"response": response, "action": "answered", "answer_token": token},
        follow_redirects=False)
    assert len(_durable_answers(db_path, sid)) == dbefore, "durable storage must be unchanged"
    assert len(_state_assertions(sid)) == sbefore, "in-memory ledger must be unchanged"
    return r


# --- BF3: malformed token fails closed ---------------------------------------
def test_bf3_malformed_token_fails_closed(db_path):
    client = app.test_client()
    sid = _start(client)
    _reject_and_assert_unchanged(db_path, sid, token="not-a-valid-token-no-separator")


# --- BF3: valid format but invalid HMAC signature fails closed ---------------
def test_bf3_valid_format_invalid_hmac_fails_closed(db_path):
    client = app.test_client()
    sid = _start(client)
    real = _get_token(client, sid)
    nonce = real.split(".", 1)[0]
    forged = nonce + "." + ("0" * 32)   # correct shape, wrong signature
    assert forged != real
    _reject_and_assert_unchanged(db_path, sid, token=forged)


# --- BF3: token issued for session A reused in session B fails closed ---------
def test_bf3_cross_session_token_fails_closed(db_path):
    client = app.test_client()
    sid_a = _start(client)
    sid_b = _start(client)
    assert sid_a != sid_b
    token_a = _get_token(client, sid_a)   # signed for sid_a only
    _reject_and_assert_unchanged(db_path, sid_b, token=token_a)


# --- BF3: token issued for project A reused in project B fails closed ---------
def test_bf3_cross_project_token_fails_closed(db_path):
    # sid == durable project_id in this model; two independent /start projects.
    client = app.test_client()
    proj1 = _start(client)
    proj2 = _start(client)
    token_p1 = _get_token(client, proj1)
    _reject_and_assert_unchanged(db_path, proj2, token=token_p1)


# --- BF3: same token reused for a DIFFERENT target/operation fails closed -----
def test_bf3_same_token_different_target_operation_fails_closed(db_path):
    client = app.test_client()
    sid = _start(client)
    tok = _get_token(client, sid)
    # First accepted answer consumes the operation bound to this token.
    client.post(f"/session/{sid}",
                data={"response": "First accepted answer for this operation.",
                      "action": "answered", "answer_token": tok},
                follow_redirects=False)
    one = _durable_answers(db_path, sid)
    assert len(one) == 1
    # Reusing the SAME token for a DIFFERENT answer/operation must fail closed
    # (durable idempotency identity collides; content differs -> no second event).
    client.post(f"/session/{sid}",
                data={"response": "A different answer for a different operation.",
                      "action": "answered", "answer_token": tok},
                follow_redirects=False)
    assert len(_durable_answers(db_path, sid)) == 1, (
        "a consumed token reused for a different operation must not append again")


# --- Observation A: populated-database migration is additive & idempotent -----
def test_obs_a_populated_database_migration(tmp_path):
    """Create a PRE-AMENDMENT records table with rows (no idempotency_key column),
    then open it through the amended store: the migration must add the column and
    the partial unique index idempotently, keep old rows readable, allow multiple
    legacy NULL idempotency identities, and enforce uniqueness only for non-null
    keys."""
    import sqlite3
    dbp = str(tmp_path / "legacy.sqlite")
    conn = sqlite3.connect(dbp)
    with conn:
        conn.execute("CREATE TABLE projects (project_id TEXT PRIMARY KEY, "
                     "idea_id TEXT NOT NULL, contract_version TEXT NOT NULL)")
        conn.execute("CREATE TABLE records (project_id TEXT NOT NULL, seq INTEGER NOT NULL, "
                     "record_id TEXT NOT NULL, payload TEXT NOT NULL, "
                     "PRIMARY KEY (project_id, record_id), "
                     "FOREIGN KEY (project_id) REFERENCES projects(project_id))")
        conn.execute("INSERT INTO projects VALUES ('p1','idea-1','p4-0-record-contract-v1')")
        # two pre-amendment rows (no idempotency_key column exists yet)
        conn.execute("INSERT INTO records (project_id, seq, record_id, payload) "
                     "VALUES ('p1',0,'rec_1','{}')")
        conn.execute("INSERT INTO records (project_id, seq, record_id, payload) "
                     "VALUES ('p1',1,'rec_2','{}')")
    conn.close()

    # Open through the amended store TWICE -> migration must be idempotent.
    SqliteRecordStore(dbp).close()
    store = SqliteRecordStore(dbp)
    try:
        cols = [r[1] for r in store._conn.execute("PRAGMA table_info(records)").fetchall()]
        assert "idempotency_key" in cols, "migration must add the idempotency_key column"
        # old rows remain readable and keep NULL idempotency identities
        rows = store._conn.execute(
            "SELECT record_id, idempotency_key FROM records "
            "WHERE project_id='p1' ORDER BY seq").fetchall()
        assert [r[0] for r in rows] == ["rec_1", "rec_2"], "legacy rows must stay readable"
        assert all(r[1] is None for r in rows), "multiple legacy NULL identities are allowed"
        # non-null idempotency keys must be unique per project
        with store._conn:
            store._conn.execute("INSERT INTO records (project_id, seq, record_id, payload, idempotency_key) "
                                "VALUES ('p1',2,'rec_3','{}','k-1')")
        with pytest.raises(sqlite3.IntegrityError):
            with store._conn:
                store._conn.execute("INSERT INTO records (project_id, seq, record_id, payload, idempotency_key) "
                                    "VALUES ('p1',3,'rec_4','{}','k-1')")
    finally:
        store.close()


# --- Observation B: restart durability through a NEW store/app context --------
def test_obs_b_restart_durability_new_context(db_path):
    """After an accepted answer, drop the live runtime entirely (new store handle
    + cleared SESSION_STORE) and cold-load through a fresh context: the durable
    answer SURVIVES and remains the authority.

    RECORDED LIMITATION (bounded scope): a cold-loaded session restores the
    durable ledger + fresh readiness ONLY (P4-1b-1). Continuing to ANSWER it is
    complete session resume (P4-2) and is deliberately NOT supported here — a new
    answered submission on a cold-loaded session fails closed GENERICALLY (no
    500/traceback, no second durable event), which this test also asserts. The
    durable evidence stays viewable; it is simply not extendable in this
    increment. No false cross-restart resume is claimed."""
    client = app.test_client()
    sid = _start(client)
    tok = _get_token(client, sid)
    first = "The shunt sensor opens the relay above the trip current."
    client.post(f"/session/{sid}", data={"response": first, "action": "answered",
                                         "answer_token": tok}, follow_redirects=False)
    assert len(_durable_answers(db_path, sid)) == 1
    # Real restart: new store handle + cleared live memory; carry only sid.
    _reset_runtime()
    assert sid not in SESSION_STORE
    # Cold-load rebuilds a viewable session from the durable envelope + records.
    assert app.test_client().get(f"/session/{sid}", follow_redirects=False).status_code == 200
    survived = _durable_answers(db_path, sid)
    assert any(r.content == first for r in survived), "accepted answer survives a full restart"
    # A new answered submission on the cold-loaded session fails closed cleanly
    # (no 500, no second durable event) — resume-answering is out of scope.
    # P10-PC1 reconciliation (disclosed): the cold-loaded page now renders the
    # Level-1 READ-ONLY reconstructed review state and deliberately no longer
    # offers an answering form or token — a STRENGTHENING of this recorded
    # limitation (previously the cold page showed a form whose submissions
    # always failed). The guarantee under test is unchanged and asserted
    # directly: even a FORGED direct POST fails closed with a redirect and no
    # second durable event.
    client2 = app.test_client()
    cold_html = _render(client2, sid).get_data(as_text=True)
    assert _token_from_html(cold_html) is None, (
        "the reconstructed cold page must not offer an answering token")
    assert 'name="response"' not in cold_html, (
        "the reconstructed cold page must not offer an answering form")
    r = client2.post(f"/session/{sid}",
                     data={"response": "Attempt to keep answering after restart.",
                           "action": "answered", "answer_token": "forged-token"},
                     follow_redirects=False)
    assert r.status_code in (301, 302), "resume-answer must fail closed with a redirect, never a 500"
    assert len(_durable_answers(db_path, sid)) == 1, (
        "resume-answering after cold-load must not durably append (out of scope)")


# --- Observation C: durable-success / memory-publication-failure limitation ---
def test_obs_c_memory_publication_failure_not_reachable_recorded():
    """LIMITATION (recorded for review): in the bounded single-thread design the
    in-memory publish after a durable append is a plain in-place ``dict.update``
    on an already-constructed staged state — it has NO truthful, reachable
    failure mode that could leave a durable record without its memory view
    without ARTIFICIAL fault injection. No recovery mechanism is claimed or
    tested here; C6's durable-authoritative reconciliation remains the contract
    of record for any future genuinely-reachable failure. This test documents the
    limitation deterministically rather than asserting an invented recovery."""
    import inspect
    import web.app as webapp
    src = inspect.getsource(webapp.submit_answer)
    # The publish step is an in-place update performed only AFTER durable success.
    assert "state.__dict__.update(staged.__dict__)" in src
    assert "_get_store().append_record(" in src
