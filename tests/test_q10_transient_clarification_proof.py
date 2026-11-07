"""Q10 synthetic transient clarification proof — TEST-ONLY, synthetic data only.

One fixed clarification question (the preserved Q10 reply's own first
clarification question, read from the merged frozen fixture) and one synthetic
inventor reply are exchanged under the UQTR session-binding mechanisms
(`issue_transient_clarification` / `accept_transient_clarification` in
`web/app.py`). The proof shows: the right prompt accepts the right reply once;
stale, modified, replayed, swapped and cross-project submissions fail closed;
the governed answer token and the clarification token never stand in for each
other; the governed question is unchanged and still answerable; the ledger,
gap state, known mechanism, reconstruction, every durable table and the #893
picture are unchanged; and the AI-origin question and the inventor's verbatim
reply stay apart, with nothing interpreted. This is development evidence, not
a qualification or product admission of any AI model.
"""
import html as _html
import json
import os
import re
import sqlite3

import pytest

import web.app as appmod
from engine.session_reconstruction import reconstruct_readonly_state
from tests.test_t2g_versioned_journey import (  # noqa: F401 — fixture reuse
    client, _login, _start, _answer, _raw)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE = os.path.join(ROOT, "tests", "fixtures",
                       "g1_component_concept_v2_diagnostic.json")
with open(FIXTURE, encoding="utf-8") as _handle:
    _Q10 = json.load(_handle)["replies"]["Q10"]
PROMPT = _Q10["clarification_questions"][0]
IDEA = ("A small gadget for my bike that switches its light on by itself when "
        "it gets dark, and makes it flash when I slow down.")
REPLY = "Flash in daylight too. I haven't chosen how to sense slowing."
SOURCE = {"case_id": "Q10",
          "evidence_ref": "g1_component_concept_v1 run journal @ 2f6925bd"}
EE = "electronics_electrical"


@pytest.fixture()
def enabled(monkeypatch):
    monkeypatch.setitem(appmod.app.config, "UQTR_TRANSIENT_CLARIFICATION_ENABLED", True)


def _bike(c):
    return _start(c, IDEA, EE, {"domain_choice": EE})


def _tables(db):
    """Every durable row, table by table — the strongest 'nothing written'."""
    con = sqlite3.connect(db)
    try:
        names = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        return {name: con.execute('SELECT * FROM "%s"' % name).fetchall()
                for name in names}
    finally:
        con.close()


def _du(raw):
    start = raw.find("data-design-understanding")
    return raw[start:raw.find("</details>", start)] if start >= 0 else None


def _canonical(appmod, sid):
    state = appmod.SESSION_STORE[sid]["state"]
    return {
        "gaps": [(g.gap_type, g.status, g.iterations_open) for g in state.gaps],
        "known_mechanism": state.known_mechanism,
        "assertions": [(r.record_id, r.disposition, r.content)
                       for r in state.assertions],
        "unknowns": list(state.acknowledged_unknowns),
        "maturity": state.maturity_level,
        "answer_token": appmod.SESSION_STORE[sid].get("answer_token"),
        "identity": appmod._resolve_question_context(state, None).identity,
    }


def _form(raw):
    form = re.search(r'<form id="answer-form".*?</form>', raw, re.S).group(0)
    get = lambda name: _html.unescape(re.search(
        r'name="%s" value="([^"]*)"' % name, form).group(1))
    return get("answer_token"), get("answer_target")


# ==========================================================================
# 0. The prompt is the preserved one, and the proof is off by default
# ==========================================================================
def test_the_prompt_is_the_frozen_q10_clarification_question():
    assert PROMPT == ("Should the light flash when you slow down during the "
                      "day, or only when it is dark?")
    source = open(os.path.join(ROOT, "web", "app.py"), encoding="utf-8").read()
    assert PROMPT not in source                    # no prompt text in product code


def test_disabled_by_default_and_outside_testing(client, monkeypatch):
    c, appmod, _db = client
    sid = _bike(c)
    assert appmod.app.config["UQTR_TRANSIENT_CLARIFICATION_ENABLED"] is False
    assert appmod.issue_transient_clarification(sid, PROMPT, SOURCE) is None
    monkeypatch.setitem(appmod.app.config, "UQTR_TRANSIENT_CLARIFICATION_ENABLED", True)
    monkeypatch.setitem(appmod.app.config, "TESTING", False)
    assert appmod.issue_transient_clarification(sid, PROMPT, SOURCE) is None
    assert "_transient_clarification" not in appmod.SESSION_STORE[sid]


def test_no_route_or_page_exposes_the_clarification(client, enabled):
    c, appmod, _db = client
    sid = _bike(c)
    rules = " ".join(str(rule) for rule in appmod.app.url_map.iter_rules())
    assert "clarification" not in rules.lower()
    appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    assert PROMPT not in _html.unescape(_raw(c, sid))


# ==========================================================================
# 1. The right prompt accepts the right reply exactly once
# ==========================================================================
def test_the_correct_prompt_accepts_the_reply_once(client, enabled):
    c, appmod, _db = client
    sid = _bike(c)
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    assert token
    exchange = appmod.accept_transient_clarification(sid, token, PROMPT, SOURCE, REPLY)
    assert exchange is not None
    assert appmod.accept_transient_clarification(
        sid, token, PROMPT, SOURCE, REPLY) is None          # replay
    assert "_transient_clarification" not in appmod.SESSION_STORE[sid]


# ==========================================================================
# 2. Stale, modified, replayed and cross-context submissions fail closed
# ==========================================================================
@pytest.mark.parametrize("prompt, source, reply", [
    (PROMPT + " ", SOURCE, REPLY),                                  # modified prompt
    (PROMPT.replace("day", "night"), SOURCE, REPLY),
    (PROMPT, {"case_id": "Q11", "evidence_ref": SOURCE["evidence_ref"]}, REPLY),
    (PROMPT, {"case_id": "Q10", "evidence_ref": "other"}, REPLY),   # swapped source
    (PROMPT, dict(SOURCE, extra="x"), REPLY),                       # wrong shape
    (PROMPT, "Q10", REPLY),
    (PROMPT, SOURCE, ""),                                           # empty reply
    (PROMPT, SOURCE, "   "),
    (PROMPT, SOURCE, "bad\x00reply"),
    (PROMPT, SOURCE, "x" * (appmod.MAX_FREE_TEXT_CHARS + 1)),
    (PROMPT, SOURCE, None),
])
def test_modified_or_invalid_submissions_fail_closed(client, enabled, prompt,
                                                     source, reply):
    c, appmod, _db = client
    sid = _bike(c)
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    assert appmod.accept_transient_clarification(sid, token, prompt, source, reply) is None
    # the genuine exchange still works afterwards: a refusal consumes nothing
    assert appmod.accept_transient_clarification(sid, token, PROMPT, SOURCE, REPLY)


def test_a_tampered_or_foreign_token_fails_closed(client, enabled):
    c, appmod, _db = client
    sid = _bike(c)
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    nonce, _sep, sig = token.partition(".")
    for bad in (nonce + "." + sig[:-1] + ("0" if sig[-1] != "0" else "1"),
                nonce + "x." + sig, nonce, "", "." + sig, token + "é",
                "x" * 300, None, 42):
        assert appmod.accept_transient_clarification(sid, bad, PROMPT, SOURCE, REPLY) is None
    assert appmod.accept_transient_clarification(sid, token, PROMPT, SOURCE, REPLY)


def test_a_newer_clarification_makes_the_earlier_one_stale(client, enabled):
    c, appmod, _db = client
    sid = _bike(c)
    first = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    second = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    assert first != second
    assert appmod.accept_transient_clarification(sid, first, PROMPT, SOURCE, REPLY) is None
    assert appmod.accept_transient_clarification(sid, second, PROMPT, SOURCE, REPLY)


def test_a_change_to_the_governed_state_makes_it_stale(client, enabled):
    c, appmod, _db = client
    sid = _bike(c)
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    _answer(c, sid, "A light sensor notices when it gets dark and the circuit "
                    "switches the lamp on.")
    assert appmod.accept_transient_clarification(sid, token, PROMPT, SOURCE, REPLY) is None


def test_a_token_never_crosses_projects(client, enabled):
    c, appmod, _db = client
    first, second = _bike(c), _bike(c)
    token = appmod.issue_transient_clarification(first, PROMPT, SOURCE)
    assert appmod.accept_transient_clarification(second, token, PROMPT, SOURCE, REPLY) is None
    other = appmod.issue_transient_clarification(second, PROMPT, SOURCE)
    assert appmod.accept_transient_clarification(second, token, PROMPT, SOURCE, REPLY) is None
    assert appmod.accept_transient_clarification(first, other, PROMPT, SOURCE, REPLY) is None
    assert appmod.accept_transient_clarification(first, token, PROMPT, SOURCE, REPLY)
    assert appmod.accept_transient_clarification(second, other, PROMPT, SOURCE, REPLY)


def test_an_owned_project_needs_its_owner(client, enabled):
    c, appmod, _db = client
    _login(c, appmod)
    sid = _bike(c)
    # a different caller (a fresh request with no authenticated owner) is refused
    with appmod.app.test_request_context("/"):
        assert appmod.issue_transient_clarification(sid, PROMPT, SOURCE) is None
    c.get(f"/session/{sid}")                     # the owner's request context
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    assert token
    with appmod.app.test_request_context("/"):
        assert appmod.accept_transient_clarification(
            sid, token, PROMPT, SOURCE, REPLY) is None
    c.get(f"/session/{sid}")
    assert appmod.accept_transient_clarification(sid, token, PROMPT, SOURCE, REPLY)


# ==========================================================================
# 3. The governed answer token and the clarification token never substitute
# ==========================================================================
def test_the_governed_token_is_not_a_clarification_token(client, enabled):
    c, appmod, _db = client
    sid = _bike(c)
    appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    answer_token, answer_target = _form(_raw(c, sid))
    for bad in (answer_token, answer_target):
        assert appmod.accept_transient_clarification(sid, bad, PROMPT, SOURCE, REPLY) is None


def test_the_clarification_token_is_not_a_governed_token(client, enabled):
    c, appmod, db = client
    sid = _bike(c)
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    _answer_token, answer_target = _form(_raw(c, sid))
    before = _tables(db)
    canonical = _canonical(appmod, sid)
    for target in (answer_target, ""):
        response = c.post(f"/session/{sid}", answer_binding=False, data={
            "response": REPLY, "action": "answered", "answer_token": token,
            "answer_target": target})
        assert response.status_code in (302, 303)
    assert appmod._valid_answer_token(sid, token) is False
    assert appmod._verified_answer_target(sid, token, answer_target) is None
    assert _tables(db) == before
    assert _canonical(appmod, sid) == canonical


# ==========================================================================
# 4 + 5. The governed question is unchanged and answerable; nothing canonical
#        or durable changes
# ==========================================================================
def test_the_exchange_changes_no_canonical_or_durable_state(client, enabled):
    c, appmod, db = client
    sid = _bike(c)
    raw_before = _raw(c, sid)
    durable = _tables(db)
    canonical = _canonical(appmod, sid)
    picture = _du(raw_before)
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    assert _tables(db) == durable                       # issuing writes nothing
    assert appmod.accept_transient_clarification(sid, token, PROMPT, SOURCE, REPLY)
    assert _tables(db) == durable                       # accepting writes nothing
    assert _canonical(appmod, sid) == canonical         # ledger, gaps, mechanism
    raw_after = _raw(c, sid)
    assert _du(raw_after) == picture is not None        # the #893 picture
    assert REPLY not in _html.unescape(raw_after)       # never shown as recorded
    assert _form(raw_after) == _form(raw_before)        # same governed form
    live = canonical
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert [(g.gap_type, g.status) for g in session.state.gaps] == \
        [(g, s) for g, s, _n in live["gaps"]]
    assert session.state.known_mechanism is None
    assert list(session.state.assertions) == []


def test_the_governed_question_is_still_answerable_afterwards(client, enabled):
    c, appmod, _db = client
    sid = _bike(c)
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    assert appmod.accept_transient_clarification(sid, token, PROMPT, SOURCE, REPLY)
    assert _answer(c, sid, REPLY).status_code == 302
    state = appmod.SESSION_STORE[sid]["state"]
    assert [r.content for r in state.assertions] == [REPLY]
    assert state.assertions[0].question_target == "PATHN:N-MC-1"
    # under the current version the pending choice earns nothing (#939)
    assert state.get_gap("MECHANISM_COMPLETENESS").status == "OPEN"


# ==========================================================================
# 6. The AI question and the inventor's verbatim reply stay apart
# ==========================================================================
def test_the_question_and_the_reply_stay_apart_and_uninterpreted(client, enabled):
    c, appmod, _db = client
    sid = _bike(c)
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    exchange = appmod.accept_transient_clarification(sid, token, PROMPT, SOURCE, REPLY)
    assert exchange.question == PROMPT
    assert exchange.question_origin == "AI_PROPOSED"
    assert exchange.question_status == "UNQUALIFIED_SYNTHETIC"
    assert exchange.response == REPLY                   # verbatim
    assert exchange.response_origin == "INVENTOR_STATED"
    assert exchange.response_status == "NOT_ASSESSED_NOT_RECORDED"
    assert exchange.response_parts == (
        "Flash in daylight too.", "I haven't chosen how to sense slowing.")
    assert all(part in REPLY for part in exchange.response_parts)
    text = exchange.describe()
    assert PROMPT in text and REPLY in text
    assert "has not interpreted, checked or recorded" in text
    for claim in ("behaviour", "behavior", "unresolved", "requirement",
                  "validated", "confirmed", "mechanism"):
        assert claim not in text.lower()
    with pytest.raises(Exception):
        exchange.response = "changed"                   # frozen


def test_whitespace_in_the_reply_is_kept_exactly(client, enabled):
    c, appmod, _db = client
    sid = _bike(c)
    reply = "  Flash in daylight too.\n\nI haven't chosen how to sense slowing.  "
    token = appmod.issue_transient_clarification(sid, PROMPT, SOURCE)
    exchange = appmod.accept_transient_clarification(sid, token, PROMPT, SOURCE, reply)
    assert exchange.response == reply
    assert exchange.response_parts == (
        "Flash in daylight too.", "I haven't chosen how to sense slowing.")
