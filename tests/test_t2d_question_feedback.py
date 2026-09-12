"""
T2-D — OPTIONAL contextual feedback on the question actually displayed.

Bound to the canonical, LANGUAGE-FREE context the one shared resolver produced
— never to question text. Feedback is not an answer, evidence, replay input,
promotion, scoring signal, quota event or selector, and the journey works
normally without it.

Tests drive the markup Flask actually renders, in English and Arabic, and use
synthetic fixtures only. No real-user record is used anywhere.
"""
import html as _html
import json
import os
import re
import sqlite3

import pytest

from tests.csrf_client import csrf_client

from engine import account_credentials as acct
from engine import question_feedback as qfb
from engine.question_feedback import (
    CONTEXT_VERSION, EMPTY_LEDGER_REVISION, FEEDBACK_CHOICES,
    MAX_FEEDBACK_ROWS_PER_PROJECT, NO_GAP_SENTINEL, NO_ITERATIONS_SENTINEL,
    QuestionFeedbackError, QuestionFeedbackHistoryError, context_key,
    ledger_revision, make_question_feedback,
)
from engine.idea_state import DISPOSITION_ANSWERED, IdeaState
from engine.record_contract import ProjectRecordContract
from engine.record_store import (
    FeedbackCapReached, FeedbackChainConflict, SqliteRecordStore,
)

SEED = ("A folding mechanical wheelchair ramp with a spring latch. The inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")
ANSWER = ("The spring latch rotates into a slot in the hinge plate and the rib "
          "transfers the load to the frame rail.")
PW = "correct horse battery staple"
_WEB = os.path.join(os.path.dirname(__file__), "..", "web")
_ENGINE = os.path.join(os.path.dirname(__file__), "..", "engine")


# ==========================================================================
# harness — nothing here fills or defaults a choice
# ==========================================================================
@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "t2d.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod


def _login(c, appmod, email="owner@example.com"):
    store = appmod._get_account_store()
    aid = acct.new_account_id()
    store.create_account(aid, acct.normalize_email(email), acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status="active")
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    assert c.post("/login", data={"email": email, "password": PW}).status_code == 302
    return aid


def _start(c):
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _raw(c, sid, lang=None):
    if lang:
        assert c.post("/ui-language", data={"lang": lang}).status_code in (302, 303)
    body = c.get(f"/session/{sid}").get_data(as_text=True)
    if lang:
        c.post("/ui-language", data={"lang": "en"})
    return body


def _page(c, sid, lang=None):
    return _html.unescape(_raw(c, sid, lang))


def _forms(body):
    """Every form with the controls a BROWSER would submit."""
    out = []
    for m in re.finditer(r'<form\b[^>]*action="([^"]+)"[^>]*>(.*?)</form>',
                         body, re.S):
        action, inner = m.group(1), m.group(2)
        fields = dict(re.findall(
            r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', inner))
        buttons = re.findall(
            r'<button[^>]*name="([^"]+)"[^>]*value="([^"]*)"', inner)
        out.append({"action": action, "fields": fields, "buttons": buttons,
                    "inner": inner})
    return out


def _fb_form(c, sid, lang=None):
    forms = [f for f in _forms(_raw(c, sid, lang))
             if "question-feedback" in f["action"]]
    assert len(forms) <= 1
    return forms[0] if forms else None


def _submit(c, sid, form, choice, extra=None):
    data = {k: _html.unescape(v) for k, v in form["fields"].items()
            if k != "csrf_token"}
    data["choice"] = choice
    if extra:
        data.update(extra)
    return c.post(f"/session/{sid}/question-feedback", data=data)


def _choose(c, sid, choice, lang=None):
    form = _fb_form(c, sid, lang)
    assert form is not None
    return _submit(c, sid, form, choice)


def _answer(c, sid, text=ANSWER):
    token = _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', _raw(c, sid)).group(1))
    return c.post(f"/session/{sid}", data={
        "response": text, "answer_token": token, "action": "answered"})


def _history(appmod, sid):
    return appmod._get_store().load_question_feedback(sid)


def _ctx(appmod, sid):
    entry = appmod.SESSION_STORE[sid]
    state = entry["state"]
    return appmod._feedback_context(sid, state, appmod._resolve_question_context(
        state, entry.get("last_result")))


def _project(c, appmod):
    _login(c, appmod)
    return _start(c)


# ==========================================================================
# 1. The shared resolver — GET and POST cannot drift
# ==========================================================================
def test_there_is_exactly_one_question_selector(client):
    import inspect
    _c, appmod = client
    module = inspect.getsource(appmod)
    assert module.count("_canonical_q = get_question(") == 1
    resolver = inspect.getsource(appmod._resolve_question_context)
    assert "_canonical_q = get_question(" in resolver
    page = inspect.getsource(appmod.show_session)
    route = inspect.getsource(appmod.submit_question_feedback)
    assert "_resolve_question_context(" in page and "_resolve_question_context(" in route
    # S4: selection is complete before any display localisation
    for localiser in ("_rvr7_display(", "_current_ui_lang("):
        assert localiser not in resolver


def test_get_and_post_resolve_the_same_context(client):
    c, appmod = client
    sid = _project(c, appmod)
    before = _ctx(appmod, sid)
    _choose(c, sid, "HELPFUL")
    after = _ctx(appmod, sid)
    assert before["key"] == after["key"]
    assert _history(appmod, sid)[0].context_key == before["key"]


def test_identity_is_verified_forward_against_the_canonical_english_ask(client):
    c, appmod = client
    sid = _project(c, appmod)
    entry = appmod.SESSION_STORE[sid]
    qctx = appmod._resolve_question_context(entry["state"], entry.get("last_result"))
    assert appmod._rvr7_verify_english(qctx.identity, qctx.served, qctx.question)
    assert _ctx(appmod, sid)["identity"] == qctx.identity
    # a mismatched canonical ask is not eligible: no control, no context
    class _Mismatch:
        gap_type, iterations_open = qctx.gap_type, qctx.iterations_open
        question, identity, served = "a completely different ask", qctx.identity, qctx.served
    assert appmod._feedback_context(sid, entry["state"], _Mismatch()) is None


def test_no_control_when_no_question_owns_the_slot(client):
    c, appmod = client
    sid = _project(c, appmod)
    entry = appmod.SESSION_STORE[sid]

    class _NoQuestion:
        gap_type, iterations_open, question, identity, served = None, 0, None, None, None
    assert appmod._feedback_context(sid, entry["state"], _NoQuestion()) is None
    assert appmod._feedback_context(sid, entry["state"], None) is None


# ==========================================================================
# 2. Context identity, revision and staleness
# ==========================================================================
def test_the_context_is_language_free(client):
    c, appmod = client
    sid = _project(c, appmod)
    english = _ctx(appmod, sid)["key"]
    _raw(c, sid, lang="ar")
    arabic = _ctx(appmod, sid)["key"]
    assert english == arabic


def test_answering_moves_to_a_different_context(client):
    c, appmod = client
    sid = _project(c, appmod)
    before = _ctx(appmod, sid)
    _choose(c, sid, "HELPFUL")
    _answer(c, sid)
    after = _ctx(appmod, sid)
    assert after["key"] != before["key"]
    assert after["iteration"] != before["iteration"] or \
        after["revision"] != before["revision"]
    # the earlier choice stays with the earlier question
    assert "No choice saved" in _page(c, sid)
    assert len(_history(appmod, sid)) == 1


def test_the_ledger_revision_covers_corrections_and_non_answer_records():
    assert ledger_revision([]) == EMPTY_LEDGER_REVISION
    base = ledger_revision(["rec_1"])
    assert base != EMPTY_LEDGER_REVISION
    assert ledger_revision(["rec_1", "rec_2"]) != base        # a record was added
    assert ledger_revision(["rec_2", "rec_1"]) != ledger_revision(["rec_1", "rec_2"])


def test_a_runtime_snapshot_behind_the_durable_ledger_gets_no_context(client):
    """A fresh durable revision must never be attached to stale cached state."""
    c, appmod = client
    sid = _project(c, appmod)
    assert _ctx(appmod, sid) is not None
    state = appmod.SESSION_STORE[sid]["state"]
    _answer(c, sid)                                   # durable ledger advances
    state = appmod.SESSION_STORE[sid]["state"]
    kept = list(state.assertions)
    state.assertions = []                             # runtime now behind
    try:
        assert appmod._feedback_context(
            sid, state, appmod._resolve_question_context(state, None)) is None
    finally:
        state.assertions = kept


def test_a_stale_tab_is_refused_and_never_retargeted(client):
    c, appmod = client
    sid = _project(c, appmod)
    stale = _fb_form(c, sid)
    _choose(c, sid, "HELPFUL")                        # the head moves
    before = _history(appmod, sid)
    _submit(c, sid, stale, "NOT_RELEVANT")            # the old tab submits
    after = _history(appmod, sid)
    assert after == before
    assert "moved on" in _page(c, sid)


def test_a_stale_tab_from_a_previous_question_is_refused(client):
    c, appmod = client
    sid = _project(c, appmod)
    stale = _fb_form(c, sid)
    _answer(c, sid)                                   # a new question is displayed
    _submit(c, sid, stale, "HELPFUL")
    assert _history(appmod, sid) == ()


def test_no_gap_prompts_use_the_explicit_sentinels():
    assert NO_GAP_SENTINEL == "-" and NO_ITERATIONS_SENTINEL == -1
    row = make_question_feedback(
        feedback_id="f1", feedback_seq=0, context_version=CONTEXT_VERSION,
        context_key="k", rvr7_identity="INTAKE", gap_type=NO_GAP_SENTINEL,
        iterations_open=NO_ITERATIONS_SENTINEL, iteration=0,
        ledger_revision=EMPTY_LEDGER_REVISION, choice="HELPFUL",
        event_key="e1", recorded_at="t")
    assert row.gap_type == NO_GAP_SENTINEL


# ==========================================================================
# 3. Rendered controls, EN and AR
# ==========================================================================
@pytest.mark.parametrize("lang", ["en", "ar"])
def test_the_rendered_control_is_its_own_form_with_no_default(client, lang):
    c, appmod = client
    sid = _project(c, appmod)
    form = _fb_form(c, sid, lang)
    assert form is not None
    assert set(form["fields"]) == {"csrf_token", "context_token"}
    assert [v for _n, v in form["buttons"]] == list(FEEDBACK_CHOICES)
    assert "<form" not in form["inner"]                 # never nested
    assert "aria-pressed" not in form["inner"]          # nothing preselected


@pytest.mark.parametrize("lang,expected", [
    ("en", ["Helpful", "Unclear", "Not relevant to my idea"]),
    ("ar", ["مفيد", "غير واضح", "لا يناسب فكرتي"]),
])
def test_the_three_choices_render_in_both_languages(client, lang, expected):
    c, appmod = client
    sid = _project(c, appmod)
    page = _page(c, sid, lang)
    for label in expected:
        assert label in page


def test_the_journey_works_without_ever_using_feedback(client):
    c, appmod = client
    sid = _project(c, appmod)
    before = _page(c, sid)
    assert _answer(c, sid).status_code in (302, 303)
    assert _history(appmod, sid) == ()
    assert "question" in _page(c, sid).lower()


def test_no_raw_token_or_identifier_is_displayed(client):
    c, appmod = client
    sid = _project(c, appmod)
    _choose(c, sid, "UNCLEAR")
    for lang in ("en", "ar"):
        page = _page(c, sid, lang)
        for raw in ("context_key", "event_key", "feedback_id", "qfb-",
                    "ledger_revision", "rvr7_identity", "PATHN:"):
            assert raw not in page, (lang, raw)


def test_copy_never_promises_delivery_review_anonymity_or_learning(client):
    from web import ui_text
    c, appmod = client
    sid = _project(c, appmod)
    _choose(c, sid, "HELPFUL")
    catalogue = next(v for v in vars(ui_text).values()
                     if isinstance(v, dict) and "UI_T2D_PROMPT" in v)
    keys = [k for k in catalogue if k.startswith("UI_T2D_")]
    assert keys
    for key in keys:
        english, arabic = ui_text.text(key, "en"), ui_text.text(key, "ar")
        assert english and arabic and english != arabic
        lowered = english.lower()
        for promise in ("team", "reviewed", "anonym", "we will read",
                        "improve automatically", "deleted after", "retention"):
            assert promise not in lowered, (key, promise)


# ==========================================================================
# 4. Event semantics: EXACT_REPLAY vs ALREADY_CURRENT vs A -> B -> A
# ==========================================================================
def test_resubmitting_the_same_rendered_form_is_an_idempotent_replay(client):
    c, appmod = client
    sid = _project(c, appmod)
    form = _fb_form(c, sid)
    _submit(c, sid, form, "HELPFUL")
    assert len(_history(appmod, sid)) == 1
    _submit(c, sid, form, "HELPFUL")                    # same form, same choice
    assert len(_history(appmod, sid)) == 1


def test_a_fresh_form_with_the_unchanged_choice_is_already_current(client):
    """Not a new row — and deliberately NOT reported as an exact event replay."""
    c, appmod = client
    sid = _project(c, appmod)
    _choose(c, sid, "HELPFUL")
    _choose(c, sid, "HELPFUL")                          # fresh form, same choice
    assert len(_history(appmod, sid)) == 1
    assert "already your saved choice" in _page(c, sid)


def test_a_to_b_to_a_is_three_legitimate_recorded_choices(client):
    c, appmod = client
    sid = _project(c, appmod)
    for choice in ("HELPFUL", "UNCLEAR", "HELPFUL"):
        _choose(c, sid, choice)
    history = _history(appmod, sid)
    assert [r.choice for r in history] == ["HELPFUL", "UNCLEAR", "HELPFUL"]
    assert history[1].supersedes_feedback_id == history[0].feedback_id
    assert history[2].supersedes_feedback_id == history[1].feedback_id
    assert _page(c, sid).count("Your saved choice:") == 1


def test_a_delayed_retry_never_restores_an_old_selection(client):
    c, appmod = client
    sid = _project(c, appmod)
    old_form = _fb_form(c, sid)
    _submit(c, sid, old_form, "HELPFUL")
    _choose(c, sid, "UNCLEAR")
    _submit(c, sid, old_form, "HELPFUL")                # the delayed retry
    history = _history(appmod, sid)
    assert [r.choice for r in history] == ["HELPFUL", "UNCLEAR"]
    page = _page(c, sid)
    assert "Unclear" in page                            # still the current one


def test_a_historical_exact_replay_is_not_proof_the_choice_is_current():
    """An EXACT_REPLAY says the EVENT happened, never that its choice stands."""
    assert qfb.FEEDBACK_EXACT_REPLAY != qfb.FEEDBACK_ALREADY_CURRENT
    assert "choice" not in qfb.FEEDBACK_EVENT_MATERIAL_FIELDS[:1]
    assert "choice" in qfb.FEEDBACK_EVENT_MATERIAL_FIELDS   # compared, not keyed


def test_the_event_key_is_derived_from_the_signed_submission_not_the_choice(client):
    import inspect
    _c, appmod = client
    source = inspect.getsource(appmod._feedback_event_key)
    assert "nonce" in source and "context_key" in source and "head_id" in source
    assert "choice" not in source.split('"""')[2]


# ==========================================================================
# 5. Authorization, CSRF and malformed input
# ==========================================================================
def test_an_unauthenticated_or_non_owner_caller_cannot_write(client):
    c, appmod = client
    sid = _project(c, appmod)
    form = _fb_form(c, sid)
    assert c.post("/logout", data={}).status_code in (302, 303)
    _submit(c, sid, form, "HELPFUL")
    assert _history(appmod, sid) == ()


def test_a_cross_project_submission_is_refused(client):
    c, appmod = client
    sid_a = _project(c, appmod)
    form_a = _fb_form(c, sid_a)
    sid_b = _start(c)
    _submit(c, sid_b, form_a, "HELPFUL")                # A's token against B
    assert _history(appmod, sid_b) == ()


def test_a_token_from_another_browser_session_is_refused(client):
    c, appmod = client
    sid = _project(c, appmod)
    form = _fb_form(c, sid)
    appmod.SESSION_STORE[sid]["_qfb_issued_at"] = 1     # binding/issue drift
    _submit(c, sid, form, "HELPFUL")
    assert _history(appmod, sid) == ()


@pytest.mark.parametrize("bad", ["", "x", "nonce.deadbeef"])
def test_a_tampered_or_missing_token_writes_nothing(client, bad):
    c, appmod = client
    sid = _project(c, appmod)
    form = _fb_form(c, sid)
    _submit(c, sid, form, "HELPFUL", extra={"context_token": bad})
    assert _history(appmod, sid) == ()


def test_an_expired_token_is_refused(client):
    c, appmod = client
    sid = _project(c, appmod)
    form = _fb_form(c, sid)
    appmod.SESSION_STORE[sid]["_qfb_issued_at"] -= (
        appmod.FEEDBACK_TOKEN_TTL_SECONDS + 1)
    _submit(c, sid, form, "HELPFUL")
    assert _history(appmod, sid) == ()


@pytest.mark.parametrize("choice", ["", "OTHER", "helpful", "HELPFUL ", None])
def test_an_unknown_choice_is_refused(client, choice):
    c, appmod = client
    sid = _project(c, appmod)
    form = _fb_form(c, sid)
    _submit(c, sid, form, choice if choice is not None else "")
    assert _history(appmod, sid) == ()


def test_unknown_or_repeated_fields_are_refused(client):
    c, appmod = client
    sid = _project(c, appmod)
    form = _fb_form(c, sid)
    _submit(c, sid, form, "HELPFUL", extra={"unexpected": "x"})
    assert _history(appmod, sid) == ()
    # a REPEATED field must reach the view's duplicate check, so use a
    # MultiDict (the CSRF client injects the token only into dict-like data)
    from werkzeug.datastructures import MultiDict
    token = _html.unescape(form["fields"]["context_token"])
    repeated = MultiDict([("context_token", token),
                          ("choice", "HELPFUL"), ("choice", "UNCLEAR")])
    c.post(f"/session/{sid}/question-feedback", data=repeated)
    assert _history(appmod, sid) == ()


def test_the_route_is_in_the_unsafe_route_inventory():
    inventory = open(os.path.join(os.path.dirname(__file__),
                                  "test_r05_request_integrity.py"),
                     encoding="utf-8").read()
    assert '"/session/<sid>/question-feedback"' in inventory


# ==========================================================================
# 6. Cold read-only, resume and restart
# ==========================================================================
def test_a_saved_choice_survives_restart_and_explicit_resume(client):
    c, appmod = client
    sid = _project(c, appmod)
    _choose(c, sid, "UNCLEAR")
    key = _ctx(appmod, sid)["key"]
    appmod.SESSION_STORE.clear()                        # process restart
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _ctx(appmod, sid)["key"] == key
    assert "Unclear" in _page(c, sid)
    assert len(_history(appmod, sid)) == 1


def test_a_cold_read_only_session_is_never_writable_here(client):
    c, appmod = client
    sid = _project(c, appmod)
    form = _fb_form(c, sid)
    appmod.SESSION_STORE.clear()
    _page(c, sid)                                       # cold read-only load
    assert getattr(appmod.SESSION_STORE[sid]["state"], "domain", None) is None
    _submit(c, sid, form, "HELPFUL")
    assert _history(appmod, sid) == ()
    # and the route never rehydrates SESSION_STORE into a writable session
    assert getattr(appmod.SESSION_STORE[sid]["state"], "domain", None) is None


def test_a_cold_session_never_assigns_feedback_to_another_question(client):
    """When a runtime-only context cannot be reproduced, nothing is shown —
    saved feedback is never attached to a different ask."""
    c, appmod = client
    sid = _project(c, appmod)
    _choose(c, sid, "HELPFUL")
    appmod.SESSION_STORE.clear()
    cold = _page(c, sid)
    assert "Your saved choice:" not in cold
    assert len(_history(appmod, sid)) == 1              # history is intact


# ==========================================================================
# 7. Storage: fresh/populated databases, chain integrity, cap, failures
# ==========================================================================
def _seed_store(path):
    store = SqliteRecordStore(path)
    state = IdeaState(idea_id="i1")
    record = state.record_interaction(
        DISPOSITION_ANSWERED, content=ANSWER, gap_context="G", iteration=1)
    store.create_project(ProjectRecordContract(idea_id="i1", assertions=[]),
                         project_id="p1")
    store.append_record("p1", record, idempotency_key="a1")
    return store


def _row(store, choice, sup=None, ek="e1", fid="f1", ck="ck"):
    return make_question_feedback(
        feedback_id=fid, feedback_seq=0, context_version=CONTEXT_VERSION,
        context_key=ck, rvr7_identity="PATHN:x", gap_type="G",
        iterations_open=0, iteration=1, ledger_revision="rev", choice=choice,
        supersedes_feedback_id=sup, event_key=ek, recorded_at="t")


def test_fresh_database_creates_the_table_and_partial_indexes(tmp_path):
    path = str(tmp_path / "fresh.sqlite")
    store = SqliteRecordStore(path)
    raw = sqlite3.connect(path)
    assert "question_feedback" in {r[0] for r in raw.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    sql = {r[0]: r[1] for r in raw.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='index' "
        "AND name LIKE 'question_feedback%'")}
    assert "WHERE supersedes_feedback_id IS NULL" in sql["question_feedback_root_uq"]
    assert "WHERE supersedes_feedback_id IS NOT NULL" in \
        sql["question_feedback_successor_uq"]
    store.close()


def test_the_migration_is_idempotent_on_fresh_and_populated_databases(tmp_path):
    path = str(tmp_path / "pop.sqlite")
    store = _seed_store(path)
    store.append_question_feedback("p1", _row(store, "HELPFUL"),
                                   expected_head_id=None)
    before = store.load_contract("p1")
    store.close()
    for _ in range(2):
        reopened = SqliteRecordStore(path)
        assert len(reopened.load_question_feedback("p1")) == 1
        after = reopened.load_contract("p1")
        assert [a.record_id for a in after.assertions] == \
            [a.record_id for a in before.assertions]
        reopened.close()


def test_chain_integrity_is_enforced_in_the_transaction(tmp_path):
    store = _seed_store(str(tmp_path / "chain.sqlite"))
    store.append_question_feedback("p1", _row(store, "HELPFUL"),
                                   expected_head_id=None)
    with pytest.raises(FeedbackChainConflict):            # second root
        store.append_question_feedback("p1", _row(store, "UNCLEAR", fid="f2",
                                                  ek="e2"), expected_head_id=None)
    with pytest.raises(FeedbackChainConflict):            # same key, other event
        store.append_question_feedback("p1", _row(store, "UNCLEAR", fid="f9"),
                                       expected_head_id=None)
    store.append_question_feedback("p1", _row(store, "UNCLEAR", sup="f1",
                                              fid="f3", ek="e3"),
                                   expected_head_id="f1")
    with pytest.raises(FeedbackChainConflict):            # stale expected head
        store.append_question_feedback("p1", _row(store, "HELPFUL", sup="f1",
                                                  fid="f4", ek="e4"),
                                       expected_head_id="f1")
    assert len(store.load_question_feedback("p1")) == 2
    store.close()


def test_the_table_has_no_update_path(tmp_path):
    store = _seed_store(str(tmp_path / "noupd.sqlite"))
    store.append_question_feedback("p1", _row(store, "HELPFUL"),
                                   expected_head_id=None)
    store.append_question_feedback("p1", _row(store, "UNCLEAR", sup="f1",
                                              fid="f2", ek="e2"),
                                   expected_head_id="f1")
    history = store.load_question_feedback("p1")
    assert [r.choice for r in history] == ["HELPFUL", "UNCLEAR"]
    source = open(os.path.join(_ENGINE, "record_store.py"), encoding="utf-8").read()
    assert "UPDATE question_feedback" not in source
    store.close()


def test_the_sql_layer_rejects_an_unknown_choice(tmp_path):
    path = str(tmp_path / "check.sqlite")
    store = _seed_store(path)
    store.close()
    raw = sqlite3.connect(path)
    with pytest.raises(sqlite3.IntegrityError):
        raw.execute("INSERT INTO question_feedback VALUES "
                    "('p1',0,'x',1,'c','i','G',0,1,'r','BOGUS',NULL,'e','t')")


def test_the_per_project_cap_refuses_without_truncating_history(tmp_path, monkeypatch):
    monkeypatch.setattr("engine.record_store.MAX_FEEDBACK_ROWS_PER_PROJECT", 2)
    store = _seed_store(str(tmp_path / "cap.sqlite"))
    store.append_question_feedback("p1", _row(store, "HELPFUL"),
                                   expected_head_id=None)
    store.append_question_feedback("p1", _row(store, "UNCLEAR", sup="f1",
                                              fid="f2", ek="e2"),
                                   expected_head_id="f1")
    with pytest.raises(FeedbackCapReached):
        store.append_question_feedback("p1", _row(store, "HELPFUL", sup="f2",
                                                  fid="f3", ek="e3"),
                                       expected_head_id="f2")
    assert len(store.load_question_feedback("p1")) == 2      # nothing truncated
    store.close()


def test_empty_unavailable_and_corrupt_histories_are_distinguished(tmp_path):
    store = _seed_store(str(tmp_path / "corrupt.sqlite"))
    assert store.load_question_feedback("p1") == ()          # EMPTY, not corrupt
    assert store.load_question_feedback("unknown") == ()
    duplicate = (_row(store, "HELPFUL"), _row(store, "UNCLEAR", fid="f2"))
    with pytest.raises(QuestionFeedbackHistoryError):        # POPULATED corrupt
        qfb.validate_feedback_history(duplicate)
    store.close()


def test_a_read_failure_suppresses_the_block_and_never_disables_answering(client):
    c, appmod = client
    sid = _project(c, appmod)
    _choose(c, sid, "HELPFUL")
    real = appmod._get_store().load_question_feedback

    def _boom(project_id):
        raise sqlite3.OperationalError("unavailable")

    appmod._get_store().load_question_feedback = _boom
    try:
        page = _page(c, sid)
        assert "Your saved choice:" not in page
        assert "No choice saved" not in page          # never implies "nothing saved"
        assert _answer(c, sid).status_code in (302, 303)   # answering still works
    finally:
        appmod._get_store().load_question_feedback = real


def test_an_uncertain_write_is_resolved_by_durable_readback(client):
    c, appmod = client
    sid = _project(c, appmod)
    _choose(c, sid, "HELPFUL")
    stored = _history(appmod, sid)[0]
    assert appmod._resolve_feedback_write(sid, stored) == appmod._FEEDBACK_EXACT_REPLAY

    class _Absent:
        event_key = "never-written"
    assert appmod._resolve_feedback_write(sid, _Absent()) == \
        appmod._FEEDBACK_STORAGE_FAILURE


# ==========================================================================
# 8. Non-interference — before/after invariance
# ==========================================================================
def _snapshot(appmod, sid, account_id):
    from engine.derived_readiness import derive_readiness
    from engine.read_export_service import produce_project_export
    entry = appmod.SESSION_STORE[sid]
    state = entry["state"]
    qctx = appmod._resolve_question_context(state, entry.get("last_result"))
    with appmod.app.test_request_context():
        package = appmod._deliverable_context(sid)[1]
    return {
        "maturity": state.maturity_level,
        "stage": state.current_stage,
        "gaps": sorted((g.gap_type, g.status, g.iterations_open) for g in state.gaps),
        "assertions": [r.record_id for r in state.assertions],
        "next_question": qctx.question,
        "identity": qctx.identity,
        "readiness": derive_readiness(state).overall_verified(),
        "quantities": len(getattr(state, "requirement_quantities", []) or []),
        "export": json.dumps(produce_project_export(
            appmod._get_store(), sid, account_id), sort_keys=True, default=str),
        "package": json.dumps(package, sort_keys=True, default=str),
    }


def test_feedback_changes_nothing_else_at_all(client):
    c, appmod = client
    account_id = _login(c, appmod, email="inv@example.com")
    sid = _start(c)
    _answer(c, sid)
    before = _snapshot(appmod, sid, account_id)
    for choice in ("HELPFUL", "UNCLEAR", "NOT_RELEVANT"):
        _choose(c, sid, choice)
    after = _snapshot(appmod, sid, account_id)
    assert after == before
    assert len(_history(appmod, sid)) == 3
    for token in ("HELPFUL", "UNCLEAR", "NOT_RELEVANT", "question_feedback",
                  "context_key", "UI_T2D_"):
        assert token not in after["export"], token
        assert token not in after["package"], token


@pytest.mark.parametrize("module", [
    "session_reconstruction.py", "progression_loop.py", "scoring.py",
    "derived_readiness.py", "path_n_questions.py", "intent_serving.py",
    "export_adapter.py", "read_export_service.py", "deliverable_assembler.py",
    "requirement_quantity.py", "evidence_reference.py",
])
def test_no_decision_module_references_feedback(module):
    source = open(os.path.join(_ENGINE, module), encoding="utf-8").read()
    assert "question_feedback" in source or True
    assert "question_feedback" not in source, module


def test_feedback_never_reaches_the_deliverable_pdf_api_or_exports(client):
    c, appmod = client
    _login(c, appmod, email="deliv@example.com")
    sid = _start(c)
    _choose(c, sid, "NOT_RELEVANT")
    deliverable = _html.unescape(
        c.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    for token in ("Not relevant to my idea", "t2d-", "question-feedback",
                  "UI_T2D_"):
        assert token not in deliverable, token
    template = open(os.path.join(_WEB, "templates", "deliverable.html"),
                    encoding="utf-8").read()
    assert "question_feedback" not in template and "t2d" not in template.lower()
    api = open(os.path.join(_WEB, "api_v1.py"), encoding="utf-8").read()
    assert "question_feedback" not in api


def test_result_feedback_and_observability_are_untouched():
    """`result_feedback.py` stays the system-to-user explanation owner and the
    operational log is never the feedback store."""
    result = open(os.path.join(_WEB, "result_feedback.py"), encoding="utf-8").read()
    assert "question_feedback" not in result
    obs = open(os.path.join(_WEB, "observability.py"), encoding="utf-8").read()
    assert "question_feedback" not in obs and "choice" not in obs
    app_source = open(os.path.join(_WEB, "app.py"), encoding="utf-8").read()
    route = app_source[app_source.index("def submit_question_feedback"):]
    route = route[:route.index("\n@app.route")]
    assert "observability" not in route and "emit(" not in route


def test_notice_namespaces_stay_isolated(client):
    c, appmod = client
    sid = _project(c, appmod)
    entry = appmod.SESSION_STORE[sid]
    entry["_answer_error"] = "kept"
    entry[appmod.QUANTITY_ACK_SLOT] = appmod.QUANTITY_SAVED_ACK
    entry[appmod.EVREF_ACK_SLOT] = appmod.EVREF_SAVED_ACK
    appmod._publish_feedback_notice(entry, error=appmod.FEEDBACK_NOT_SAVED_MESSAGE)
    assert entry["_answer_error"] == "kept"
    assert entry[appmod.QUANTITY_ACK_SLOT] == appmod.QUANTITY_SAVED_ACK
    assert entry[appmod.EVREF_ACK_SLOT] == appmod.EVREF_SAVED_ACK
    appmod._publish_feedback_notice(entry, ack=appmod.FEEDBACK_SAVED_ACK)
    assert appmod.FEEDBACK_ERROR_SLOT not in entry
    assert appmod._feedback_notice_text("NOT-A-TOKEN", "en") is None


def test_no_ladder_writer_or_learning_path_is_introduced():
    engine_src = open(os.path.join(_ENGINE, "question_feedback.py"),
                      encoding="utf-8").read()
    # the CODE only: the module docstring deliberately NAMES these concepts to
    # state what feedback is not, and that prose must not trip the guard.
    body = "\n".join(
        line for line in engine_src.split('"""')[2].splitlines()
        if not line.strip().startswith("#"))
    for forbidden in ("validation_status", "provenance", "quality",
                      "DEMONSTRATED", "SPECIALIST_REVIEWED", "readiness",
                      "score", "quota", "openai", "anthropic", "requests",
                      "urllib", "socket"):
        assert forbidden not in body, forbidden
