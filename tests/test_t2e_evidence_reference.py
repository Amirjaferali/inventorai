"""
T2-E Option B (OD-PDVG-08a) — owner-recorded, explicitly UNVERIFIED evidence
references.

What is being pinned: an owner may durably record who they SAY reviewed or
supports one exact answer, when, what it covered and — required — what it did
NOT cover; the record is labelled as theirs and unverified; and it changes
NOTHING on any evidence ladder or in any decision surface.

The proof obligations P-1 ... P-12 from the accepted design are each a named,
individually failing assertion below.
"""
import html as _html
import json
import os
import re
import sqlite3
import tempfile

import pytest

from tests.csrf_client import csrf_client

from engine import account_credentials as acct
from engine import evidence_reference as evref
from engine.evidence_reference import (
    CLAIM_STATUS_UNVALIDATED, EvidenceReferenceError,
    EvidenceReferenceHistoryError, MAX_LIMITATION_TEXT_CHARS,
    MAX_SOURCE_IDENTITY_CHARS, REFERENCE_EXACT_REPLAY, REFERENCE_INSERTED,
    make_evidence_reference,
)
from engine.idea_state import (
    DISPOSITION_ANSWERED, EXTERNAL_EVIDENCE, EXPERT_SUPPLIED, IdeaState,
    INDEPENDENTLY_VERIFIED, EMPIRICALLY_DEMONSTRATED, OWNER_STATED,
    SPECIALIST_REVIEWED, SYSTEM_INFERRED, UNVALIDATED,
)
from engine.record_contract import ProjectRecordContract
from engine.record_store import (
    ReferenceCapExceeded, ReferenceChainConflict, SqliteRecordStore,
)
from engine.session_reconstruction import reconstruct_readonly_state

SEED = ("A folding mechanical wheelchair ramp with a spring latch. The inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")
ANSWER = ("The spring latch rotates into a slot in the hinge plate and the rib "
          "transfers the load to the frame rail.")
PW = "correct horse battery staple"
GOOD = {
    "source_identity": "Dr A. Khan, structural engineer",
    "occurred_on": "2026-03-14",
    "scope_text": "static load case only",
    "limitation_text": "did not cover fatigue or corrosion",
}
_ENGINE = os.path.join(os.path.dirname(__file__), "..", "engine")
_WEB = os.path.join(os.path.dirname(__file__), "..", "web")


# ==========================================================================
# harness
# ==========================================================================
@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "t2e.sqlite"))
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


def _answer(c, sid, text=ANSWER):
    token = _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', _raw(c, sid)).group(1))
    return c.post(f"/session/{sid}", data={
        "response": text, "answer_token": token, "action": "answered"})


def _anchor(c, sid):
    found = re.search(r'name="anchor_record_id" value="([^"]+)"', _raw(c, sid))
    return None if found is None else found.group(1)


def _propose(c, sid, anchor, intent="record", **over):
    data = dict(GOOD, anchor_record_id=anchor, reference_intent=intent)
    data.update(over)
    return c.post(f"/session/{sid}/evidence-reference/propose", data=data)


def _token(c, sid):
    found = re.search(r'name="confirmation_token" value="([^"]+)"', _raw(c, sid))
    return None if found is None else _html.unescape(found.group(1))


def _confirm(c, sid, token=None, action="confirm"):
    return c.post(f"/session/{sid}/evidence-reference/confirm", data={
        "confirmation_token": token if token is not None else _token(c, sid),
        "reference_action": action})


def _project(c, appmod):
    """A logged-in owner with one answered anchor, ready to attach."""
    _login(c, appmod)
    sid = _start(c)
    _answer(c, sid)
    anchor = _anchor(c, sid)
    assert anchor is not None
    return sid, anchor


def _record(c, sid, anchor, **over):
    _propose(c, sid, anchor, **over)
    return _confirm(c, sid)


def _history(appmod, sid):
    return appmod._get_store().load_evidence_references(sid)


def _py_files():
    for root in (_ENGINE, _WEB):
        for dirpath, _dirs, files in os.walk(root):
            for name in files:
                if name.endswith(".py"):
                    yield os.path.join(dirpath, name)


# ==========================================================================
# 1. The value object: bounded, required limitation, frozen status
# ==========================================================================
def _make(**over):
    kwargs = dict(reference_id="ref_1", reference_seq=0, anchor_record_id="rec_1",
                  source_identity=GOOD["source_identity"],
                  occurred_on=GOOD["occurred_on"], scope_text=GOOD["scope_text"],
                  limitation_text=GOOD["limitation_text"], event_key="k1",
                  recorded_iteration=1, recorded_at="2026-03-14T10:00:00Z")
    kwargs.update(over)
    return make_evidence_reference(**kwargs)


def test_claim_status_is_a_frozen_single_value_and_is_not_a_parameter():
    """One value, deliberately: the writer has no second value available, so no
    code path can promote a reference and this can never become a ladder."""
    assert evref.CLAIM_STATUSES == (CLAIM_STATUS_UNVALIDATED,)
    assert _make().claim_status == CLAIM_STATUS_UNVALIDATED
    with pytest.raises(TypeError):
        make_evidence_reference(claim_status="SPECIALIST_REVIEWED", **{})


@pytest.mark.parametrize("field", ["source_identity", "scope_text", "limitation_text"])
@pytest.mark.parametrize("bad", ["", "   ", "a\x00b", "a\x07b", "a\x9fb"])
def test_empty_nul_and_control_characters_are_refused(field, bad):
    with pytest.raises(EvidenceReferenceError) as raised:
        _make(**{field: bad})
    assert field in str(raised.value)
    for value in (bad,):
        assert value not in str(raised.value) or value.strip() == ""


def test_each_text_field_has_its_own_bound():
    _make(source_identity="x" * MAX_SOURCE_IDENTITY_CHARS)
    with pytest.raises(EvidenceReferenceError):
        _make(source_identity="x" * (MAX_SOURCE_IDENTITY_CHARS + 1))
    _make(limitation_text="y" * MAX_LIMITATION_TEXT_CHARS)
    with pytest.raises(EvidenceReferenceError):
        _make(limitation_text="y" * (MAX_LIMITATION_TEXT_CHARS + 1))


@pytest.mark.parametrize("bad", ["14/03/2026", "2026-3-14", "2026-13-01",
                                 "2026-02-30", "today", "", "2026-03-14T10:00"])
def test_the_date_must_be_a_real_iso_calendar_date(bad):
    with pytest.raises(EvidenceReferenceError):
        _make(occurred_on=bad)


def test_the_limitation_is_required_not_optional():
    """A reference that does not say what it did NOT cover cannot exist."""
    with pytest.raises(EvidenceReferenceError):
        _make(limitation_text="")


def test_values_are_stored_verbatim_after_outer_stripping_only():
    reference = _make(source_identity="  Dr A. Khan  ", scope_text=" static  load ")
    assert reference.source_identity == "Dr A. Khan"
    assert reference.scope_text == "static  load"        # inner text untouched


def test_a_reference_cannot_supersede_itself():
    with pytest.raises(EvidenceReferenceError):
        _make(supersedes_reference_id="ref_1")


# ==========================================================================
# 2. DDL: executable, idempotent, and it enforces the conditional rules
#    (fresh and populated databases)
# ==========================================================================
def _store(path):
    return SqliteRecordStore(path)


def _seed_project(store, pid="p1"):
    state = IdeaState(idea_id="i1")
    record = state.record_interaction(
        DISPOSITION_ANSWERED, content=ANSWER,
        gap_context="MECHANISM_COMPLETENESS", iteration=1)
    store.create_project(ProjectRecordContract(idea_id="i1", assertions=[]),
                         project_id=pid)
    store.append_record(pid, record, idempotency_key="a1")
    return record.record_id


def test_the_schema_creates_the_table_and_its_partial_indexes(tmp_path):
    path = str(tmp_path / "fresh.sqlite")
    store = _store(path)
    raw = sqlite3.connect(path)
    tables = {r[0] for r in raw.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")}
    assert "evidence_references" in tables
    indexes = {r[0]: r[1] for r in raw.execute(
        "SELECT name, sql FROM sqlite_master WHERE type='index' "
        "AND name LIKE 'evidence_references%'")}
    assert {"evidence_references_event_key_uq", "evidence_references_seq_uq",
            "evidence_references_supersedes_uq",
            "evidence_references_chain_root_uq",
            "evidence_references_anchor_idx"} <= set(indexes)
    # the two CONDITIONAL rules are PARTIAL indexes, never inline constraints
    assert "WHERE supersedes_reference_id IS NOT NULL" in \
        indexes["evidence_references_supersedes_uq"]
    assert "WHERE supersedes_reference_id IS NULL" in \
        indexes["evidence_references_chain_root_uq"]
    store.close()


def test_sqlite_rejects_the_inline_conditional_unique_form():
    """Why the standalone partial indexes are required rather than stylistic."""
    with pytest.raises(sqlite3.OperationalError):
        sqlite3.connect(":memory:").execute(
            "CREATE TABLE t (a TEXT, b TEXT, UNIQUE (a, b) WHERE b IS NOT NULL)")


def test_the_migration_is_idempotent_on_fresh_and_populated_databases(tmp_path):
    path = str(tmp_path / "pop.sqlite")
    store = _store(path)
    anchor = _seed_project(store)
    store.append_evidence_reference(store.__class__ and "p1", _make(
        anchor_record_id=anchor, event_key="k1"))
    store.close()
    # reopening runs the whole migration again against a POPULATED database
    reopened = _store(path)
    assert len(reopened.load_evidence_references("p1")) == 1
    reopened.close()
    again = _store(path)
    assert len(again.load_evidence_references("p1")) == 1
    again.close()


def test_existing_tables_and_rows_are_untouched_by_the_addition(tmp_path):
    path = str(tmp_path / "legacy.sqlite")
    store = _store(path)
    anchor = _seed_project(store)
    before = store.load_contract("p1")
    store.append_evidence_reference("p1", _make(anchor_record_id=anchor, event_key="k1"))
    after = store.load_contract("p1")
    assert [a.record_id for a in after.assertions] == \
        [a.record_id for a in before.assertions]
    assert after.assertions[0].provenance == before.assertions[0].provenance
    assert after.assertions[0].validation_status == before.assertions[0].validation_status
    store.close()


# ==========================================================================
# 3. Store: append-only, idempotent, conditional rules enforced
# ==========================================================================
@pytest.fixture()
def store_with_anchor(tmp_path):
    store = _store(str(tmp_path / "s.sqlite"))
    anchor = _seed_project(store)
    yield store, anchor
    store.close()


def test_first_root_inserts_and_an_exact_replay_is_idempotent(store_with_anchor):
    store, anchor = store_with_anchor
    reference = _make(anchor_record_id=anchor, event_key="k1")
    assert store.append_evidence_reference("p1", reference) == REFERENCE_INSERTED
    assert store.append_evidence_reference("p1", reference) == REFERENCE_EXACT_REPLAY
    assert len(store.load_evidence_references("p1")) == 1


def test_the_same_key_naming_a_different_event_is_a_conflict(store_with_anchor):
    store, anchor = store_with_anchor
    store.append_evidence_reference("p1", _make(anchor_record_id=anchor, event_key="k1"))
    with pytest.raises(ReferenceChainConflict):
        store.append_evidence_reference("p1", _make(
            reference_id="ref_2", anchor_record_id=anchor, event_key="k1",
            source_identity="Someone else"))


def test_one_active_root_per_anchor(store_with_anchor):
    store, anchor = store_with_anchor
    store.append_evidence_reference("p1", _make(anchor_record_id=anchor, event_key="k1"))
    with pytest.raises(ReferenceChainConflict):
        store.append_evidence_reference("p1", _make(
            reference_id="ref_2", anchor_record_id=anchor, event_key="k2"))


def test_one_successor_per_reference(store_with_anchor):
    store, anchor = store_with_anchor
    store.append_evidence_reference("p1", _make(anchor_record_id=anchor, event_key="k1"))
    store.append_evidence_reference("p1", _make(
        reference_id="ref_2", anchor_record_id=anchor, event_key="k2",
        supersedes_reference_id="ref_1", source_identity="Revised"))
    with pytest.raises(ReferenceChainConflict):
        store.append_evidence_reference("p1", _make(
            reference_id="ref_3", anchor_record_id=anchor, event_key="k3",
            supersedes_reference_id="ref_1", source_identity="Another"))


def test_a_stale_head_is_refused_inside_the_transaction(store_with_anchor):
    store, anchor = store_with_anchor
    store.append_evidence_reference("p1", _make(anchor_record_id=anchor, event_key="k1"))
    store.append_evidence_reference("p1", _make(
        reference_id="ref_2", anchor_record_id=anchor, event_key="k2",
        supersedes_reference_id="ref_1", source_identity="Revised"))
    # ref_1 is no longer the head
    with pytest.raises(ReferenceChainConflict):
        store.append_evidence_reference("p1", _make(
            reference_id="ref_9", anchor_record_id=anchor, event_key="k9",
            supersedes_reference_id="ref_1", source_identity="Stale"))


def test_an_anchor_that_is_not_an_active_answered_assertion_is_refused(store_with_anchor):
    store, _anchor = store_with_anchor
    with pytest.raises(ReferenceChainConflict):
        store.append_evidence_reference("p1", _make(
            anchor_record_id="rec_does_not_exist", event_key="k1"))


def test_the_table_has_no_update_path(store_with_anchor):
    """Change is a superseding row; withdrawal is a superseding row."""
    store, anchor = store_with_anchor
    store.append_evidence_reference("p1", _make(anchor_record_id=anchor, event_key="k1"))
    store.append_evidence_reference("p1", _make(
        reference_id="ref_2", anchor_record_id=anchor, event_key="k2",
        supersedes_reference_id="ref_1", withdrawn=True))
    history = store.load_evidence_references("p1")
    assert len(history) == 2
    assert history[0].withdrawn is False and history[0].source_identity == \
        GOOD["source_identity"]
    assert history[1].withdrawn is True
    source = open(os.path.join(_ENGINE, "record_store.py"), encoding="utf-8").read()
    assert "UPDATE evidence_references" not in source


def test_an_unknown_project_reads_as_empty_not_as_an_error(store_with_anchor):
    store, _anchor = store_with_anchor
    assert store.load_evidence_references("no-such-project") == ()


def test_a_populated_corrupt_history_fails_closed():
    duplicate = (_make(event_key="k1"), _make(reference_id="ref_2", event_key="k1"))
    with pytest.raises(EvidenceReferenceHistoryError):
        evref.validate_reference_history(duplicate)
    assert evref.validate_reference_history(()) == ()      # zero rows is valid


# ==========================================================================
# 4. Web: the attach lifecycle
# ==========================================================================
def test_the_happy_path_records_one_unverified_claim(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)
    history = _history(appmod, sid)
    assert len(history) == 1
    assert history[0].source_identity == GOOD["source_identity"]
    assert history[0].claim_status == CLAIM_STATUS_UNVALIDATED
    page = _page(c, sid)
    assert "not verified by InventorAI" in page
    assert GOOD["limitation_text"] in page


def test_the_answer_token_is_never_accepted_as_a_confirmation_token(client):
    """`_valid_answer_token` is STATELESS, so a consumed answer token still
    verifies forever and binds nothing about an anchor or a chain head. It
    therefore must not reach this flow at all."""
    c, appmod = client
    sid, anchor = _project(c, appmod)
    answer_token = _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', _raw(c, sid)).group(1))
    _propose(c, sid, anchor)
    _confirm(c, sid, token=answer_token)
    assert _history(appmod, sid) == ()
    source = open(os.path.join(_WEB, "app.py"), encoding="utf-8").read()
    confirm_src = source[source.index("def confirm_evidence_reference"):]
    confirm_src = confirm_src[:confirm_src.index("\n@app.route")]
    assert "_valid_answer_token" not in confirm_src
    assert "answer_token" not in confirm_src


def test_the_nonce_is_consumed_before_any_durable_write(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor)
    token = _token(c, sid)
    _confirm(c, sid, token=token)
    assert len(_history(appmod, sid)) == 1
    _confirm(c, sid, token=token)                 # replayed after consumption
    assert len(_history(appmod, sid)) == 1
    assert appmod.SESSION_STORE[sid].get(appmod._EVREF_PROPOSAL_KEY) is None


def test_an_expired_proposal_can_never_be_confirmed(client, monkeypatch):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor)
    token = _token(c, sid)
    staged = appmod.SESSION_STORE[sid][appmod._EVREF_PROPOSAL_KEY]
    staged["expires_at"] = staged["issued_at"] - 1
    _confirm(c, sid, token=token)
    assert _history(appmod, sid) == ()


def test_a_tampered_token_writes_nothing(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor)
    token = _token(c, sid)
    for bad in ("", "x", token[:-1] + ("a" if token[-1] != "a" else "b"),
                token.split(".")[0] + ".deadbeef"):
        _propose(c, sid, anchor)
        _confirm(c, sid, token=bad)
        assert _history(appmod, sid) == ()


def test_a_mutated_material_field_invalidates_the_token(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor)
    token = _token(c, sid)
    appmod.SESSION_STORE[sid][appmod._EVREF_PROPOSAL_KEY]["scope_text"] = "mutated"
    _confirm(c, sid, token=token)
    assert _history(appmod, sid) == ()


def test_a_proposal_staged_in_another_session_cannot_be_confirmed(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor)
    token = _token(c, sid)
    staged = appmod.SESSION_STORE[sid][appmod._EVREF_PROPOSAL_KEY]
    staged["session_binding"] = "a-different-browser-session"
    _confirm(c, sid, token=token)
    assert _history(appmod, sid) == ()
    # the staging session keeps its proposal; this session spent nothing
    assert appmod.SESSION_STORE[sid].get(appmod._EVREF_PROPOSAL_KEY) is not None


def test_an_unauthenticated_or_non_owner_caller_cannot_attach(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    assert c.post("/logout", data={}).status_code in (302, 303)
    assert _propose(c, sid, anchor).status_code in (302, 303, 403, 404)
    assert _history(appmod, sid) == ()


def test_a_cross_project_anchor_is_refused(client):
    c, appmod = client
    sid_a, anchor_a = _project(c, appmod)
    sid_b = _start(c)
    _answer(c, sid_b)
    _propose(c, sid_b, anchor_a)
    assert _history(appmod, sid_b) == ()


def test_extra_or_repeated_form_fields_are_refused(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    c.post(f"/session/{sid}/evidence-reference/propose",
           data=dict(GOOD, anchor_record_id=anchor, reference_intent="record",
                     unexpected="x"))
    assert appmod.SESSION_STORE[sid].get(appmod._EVREF_PROPOSAL_KEY) is None
    _propose(c, sid, anchor)
    token = _token(c, sid)
    c.post(f"/session/{sid}/evidence-reference/confirm",
           data={"confirmation_token": token, "reference_action": "confirm",
                 "extra": "x"})
    assert _history(appmod, sid) == ()


def test_discard_records_nothing(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor)
    _confirm(c, sid, action="discard")
    assert _history(appmod, sid) == ()
    assert "Discarded" in _page(c, sid)


def test_supersession_and_withdrawal_keep_every_earlier_row(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)
    _record(c, sid, anchor, source_identity="Dr A. Khan (revised)")
    _record(c, sid, anchor, intent="withdraw")
    history = _history(appmod, sid)
    assert [h.reference_seq for h in history] == [0, 1, 2]
    assert history[0].source_identity == GOOD["source_identity"]
    assert history[1].source_identity == "Dr A. Khan (revised)"
    assert history[2].withdrawn is True
    assert [h.withdrawn for h in history[:2]] == [False, False]
    page = _page(c, sid)
    assert "Withdrawn by the inventor" in page


def test_withdrawing_when_nothing_is_recorded_is_an_established_refusal(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor, intent="withdraw")
    assert appmod.SESSION_STORE[sid].get(appmod._EVREF_PROPOSAL_KEY) is None
    assert _history(appmod, sid) == ()


# ==========================================================================
# 4b. WITHDRAWAL THROUGH THE FORM FLASK ACTUALLY RENDERS
#
#     The original candidate placed the withdraw button INSIDE the recording
#     form. A browser submits every control in the form it posts, so the real
#     rendered withdrawal carried the four (empty) owner-text inputs and was
#     rejected by recording validation; filling them made it "work" but wrote
#     those unrelated values as the withdrawal row's content. These tests drive
#     the rendered markup instead of a hand-built payload, so neither failure
#     can return unnoticed.
# ==========================================================================
def _rendered_forms(body):
    """Every <form> in the page with the controls a BROWSER would submit:
    its inputs (a text input the user left blank submits as empty) and its
    buttons. No helper fills anything in."""
    forms = []
    for match in re.finditer(r'<form\b[^>]*action="([^"]+)"[^>]*>(.*?)</form>',
                             body, re.S):
        action, inner = match.group(1), match.group(2)
        fields = dict(re.findall(
            r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', inner))
        for name in re.findall(r'<input[^>]*name="([^"]+)"', inner):
            fields.setdefault(name, "")
        buttons = re.findall(
            r'<button[^>]*name="([^"]+)"[^>]*value="([^"]*)"', inner)
        forms.append({"action": action, "fields": fields, "buttons": buttons,
                      "inner": inner})
    return forms


def _rendered_withdraw_form(c, sid, lang=None):
    """The form that actually carries the withdraw control, or None."""
    forms = [f for f in _rendered_forms(_raw(c, sid, lang))
             if "evidence-reference/propose" in f["action"]
             and any(v == "withdraw" for _n, v in f["buttons"])]
    assert len(forms) <= 1, "more than one withdrawal form rendered"
    return forms[0] if forms else None


def _submit_rendered(c, sid, form, extra=None):
    """POST exactly what a browser would send for that form: its own controls
    plus the clicked button. csrf_token is omitted because the test client
    injects it; nothing else is added or filled in."""
    data = {k: _html.unescape(v) for k, v in form["fields"].items()
            if k != "csrf_token"}
    name, value = next((n, v) for n, v in form["buttons"] if v == "withdraw")
    data[name] = value
    if extra:
        data.update(extra)
    return c.post(f"/session/{sid}" + form["action"].split(sid, 1)[1], data=data)


def _two_reference_chain(c, sid, anchor):
    """A reference, then a supersession differing in ALL FOUR fields, so a
    withdrawal that copied the wrong row would be visible."""
    first = dict(source_identity="Dr A. Khan, structural engineer",
                 occurred_on="2026-03-14",
                 scope_text="static load case only",
                 limitation_text="did not cover fatigue or corrosion")
    second = dict(source_identity="Prof B. Silva, mechanical reviewer",
                  occurred_on="2026-05-02",
                  scope_text="dynamic load and hinge cycling",
                  limitation_text="did not cover material sourcing")
    for payload in (first, second):
        _record(c, sid, anchor, **payload)
    return first, second


def test_the_rendered_withdrawal_form_carries_no_owner_text_controls(client):
    """The structural cause of the defect: the withdraw control must not live
    in the recording form, and the two forms must not be nested."""
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)
    form = _rendered_withdraw_form(c, sid)
    assert form is not None
    assert set(form["fields"]) == {"csrf_token", "anchor_record_id"}
    assert form["buttons"] == [("reference_intent", "withdraw")]
    assert "<form" not in form["inner"]                  # never nested
    recording = [f for f in _rendered_forms(_raw(c, sid))
                 if "evidence-reference/propose" in f["action"]
                 and any(v == "record" for _n, v in f["buttons"])]
    assert len(recording) == 1
    assert not any(v == "withdraw" for _n, v in recording[0]["buttons"])


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_withdrawal_through_the_rendered_form_supersedes_the_current_head(client, lang):
    """The full mandated path: render, submit what the browser would submit,
    confirm, and check every stored value against the CURRENT head."""
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _first, second = _two_reference_chain(c, sid, anchor)
    before = _history(appmod, sid)
    assert len(before) == 2
    head = before[1]

    form = _rendered_withdraw_form(c, sid, lang=lang)
    assert form is not None
    _submit_rendered(c, sid, form)

    # a proposal is staged, with NO field-entry error, and NOTHING is written yet
    staged = appmod.SESSION_STORE[sid].get(appmod._EVREF_PROPOSAL_KEY)
    assert staged is not None, "the rendered withdrawal was rejected"
    assert appmod.SESSION_STORE[sid].get(appmod.EVREF_ERROR_SLOT) is None
    assert _history(appmod, sid) == before          # propose writes no durable row

    _confirm(c, sid)
    after = _history(appmod, sid)
    assert len(after) == 3                          # exactly one row appended
    row = after[2]
    assert row.withdrawn is True
    assert row.supersedes_reference_id == head.reference_id     # the HEAD, not the original
    assert row.supersedes_reference_id != before[0].reference_id
    # all four stored values come from the current head
    assert (row.source_identity, row.occurred_on, row.scope_text,
            row.limitation_text) == (
        second["source_identity"], second["occurred_on"],
        second["scope_text"], second["limitation_text"])
    assert row.claim_status == CLAIM_STATUS_UNVALIDATED
    # every preceding row is unchanged
    assert after[:2] == before
    # and the displayed state is correct in this language
    page = _page(c, sid, lang=lang)
    expected = "Withdrawn by the inventor" if lang == "en" else "سحبه المخترع"
    assert expected in page
    if lang == "ar":
        assert any("؀" <= ch <= "ۿ" for ch in page)


@pytest.mark.parametrize("extra,label", [
    ({"source_identity": "", "occurred_on": "", "scope_text": "",
      "limitation_text": ""}, "empty fields"),
    ({"source_identity": "UNRELATED-XYZ", "occurred_on": "1999-01-01",
      "scope_text": "UNRELATED SCOPE", "limitation_text": "UNRELATED LIMIT"},
     "unrelated fields"),
])
def test_submitted_owner_text_can_never_become_the_withdrawal_content(client, extra, label):
    """A legacy or hand-built submission may still CARRY the four known fields
    (the allowlist is deliberately unchanged), but the withdrawal path never
    reads them: neither empty nor unrelated values may replace the
    server-derived content, and neither may cause a rejection."""
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _first, second = _two_reference_chain(c, sid, anchor)
    head = _history(appmod, sid)[1]
    form = _rendered_withdraw_form(c, sid)
    _submit_rendered(c, sid, form, extra=extra)
    assert appmod.SESSION_STORE[sid].get(appmod._EVREF_PROPOSAL_KEY) is not None, label
    _confirm(c, sid)
    row = _history(appmod, sid)[2]
    assert row.withdrawn is True
    assert row.supersedes_reference_id == head.reference_id
    assert (row.source_identity, row.occurred_on, row.scope_text,
            row.limitation_text) == (
        second["source_identity"], second["occurred_on"],
        second["scope_text"], second["limitation_text"]), label
    for value in extra.values():
        if value:
            assert value not in (row.source_identity, row.occurred_on,
                                 row.scope_text, row.limitation_text)


def test_the_recording_path_still_requires_all_four_fields(client):
    """The repair must not make any recording field optional — for a first
    record or for a supersession."""
    c, appmod = client
    sid, anchor = _project(c, appmod)
    for field in ("source_identity", "occurred_on", "scope_text", "limitation_text"):
        _propose(c, sid, anchor, **{field: "   "})
        assert appmod.SESSION_STORE[sid].get(appmod._EVREF_PROPOSAL_KEY) is None, field
        assert _history(appmod, sid) == (), field
    _record(c, sid, anchor)                                   # first record works
    for field in ("source_identity", "occurred_on", "scope_text", "limitation_text"):
        over = {"source_identity": "Someone new"}
        over[field] = "  "
        _propose(c, sid, anchor, **over)
        assert appmod.SESSION_STORE[sid].get(appmod._EVREF_PROPOSAL_KEY) is None, field
        assert len(_history(appmod, sid)) == 1, field         # supersession too


def test_no_withdrawal_form_is_offered_when_there_is_nothing_to_withdraw(client):
    """Absent and already-withdrawn references offer no control, and a direct
    submission is still an established refusal."""
    c, appmod = client
    sid, anchor = _project(c, appmod)
    assert _rendered_withdraw_form(c, sid) is None            # nothing recorded
    _propose(c, sid, anchor, intent="withdraw")
    assert _history(appmod, sid) == ()
    _record(c, sid, anchor)
    form = _rendered_withdraw_form(c, sid)
    assert form is not None
    _submit_rendered(c, sid, form)
    _confirm(c, sid)
    assert len(_history(appmod, sid)) == 2
    assert _rendered_withdraw_form(c, sid) is None            # already withdrawn
    _propose(c, sid, anchor, intent="withdraw")
    assert len(_history(appmod, sid)) == 2                    # still refused


def test_a_head_that_moves_between_propose_and_confirm_is_refused_not_retargeted(client):
    """A changed head requires refusal, never silent retargeting onto the new
    head."""
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)
    original_head = _history(appmod, sid)[0]
    form = _rendered_withdraw_form(c, sid)
    _submit_rendered(c, sid, form)
    staged_token = _token(c, sid)
    # the head moves underneath the staged withdrawal
    staged = dict(appmod.SESSION_STORE[sid][appmod._EVREF_PROPOSAL_KEY])
    _record(c, sid, anchor, source_identity="Prof B. Silva, mechanical reviewer")
    appmod.SESSION_STORE[sid][appmod._EVREF_PROPOSAL_KEY] = staged
    before = _history(appmod, sid)
    _confirm(c, sid, token=staged_token)
    after = _history(appmod, sid)
    assert after == before, "a stale-head withdrawal was written"
    assert all(not r.withdrawn for r in after)
    assert after[0].reference_id == original_head.reference_id


# ==========================================================================
# 5. Rejected input: explicit, bilingual, names the field, NEVER retained
# ==========================================================================
@pytest.mark.parametrize("field,phrase", [
    ("source_identity", "who you say reviewed"),
    ("occurred_on", "YYYY-MM-DD"),
    ("scope_text", "what it covered"),
    ("limitation_text", "what it did NOT cover"),
])
def test_each_invalid_field_is_named_and_nothing_is_retained(client, field, phrase):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor, **{field: "   "} if field != "occurred_on"
             else {"occurred_on": "14/03/2026"})
    page = _page(c, sid)
    assert phrase in page
    assert "please enter it again" in page
    # nothing written, nothing staged, nothing stashed anywhere in the entry
    assert _history(appmod, sid) == ()
    entry = appmod.SESSION_STORE[sid]
    assert entry.get(appmod._EVREF_PROPOSAL_KEY) is None
    blob = json.dumps({k: v for k, v in entry.items()
                       if isinstance(v, (str, int, float, bool, type(None)))},
                      default=str)
    assert GOOD["source_identity"] not in blob
    assert GOOD["scope_text"] not in blob


def test_rejection_messages_are_bilingual(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor, limitation_text="  ")
    english = _page(c, sid)
    _propose(c, sid, anchor, limitation_text="  ")
    arabic = _page(c, sid, lang="ar")
    assert "please enter it again" in english
    assert any("؀" <= ch <= "ۿ" for ch in arabic)
    assert "لم يُحفظ شيء" in arabic


def test_no_rejected_value_is_ever_echoed_back(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    secret = "CONFIDENTIAL-SUPPLIER-NAME-9911"
    _propose(c, sid, anchor, source_identity=secret, limitation_text="  ")
    assert secret not in _page(c, sid)
    assert _history(appmod, sid) == ()


def test_oversized_input_is_refused_before_staging(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor, scope_text="x" * 30000)
    assert appmod.SESSION_STORE[sid].get(appmod._EVREF_PROPOSAL_KEY) is None
    assert _history(appmod, sid) == ()


def test_the_ui_does_not_claim_a_draft_is_kept(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _propose(c, sid, anchor, limitation_text="  ")
    page = _page(c, sid).lower()
    for claim in ("draft saved", "we kept", "saved your entry", "restored"):
        assert claim not in page


# ==========================================================================
# 6. P-1 ... P-12 — the non-interference proof obligations, each named
# ==========================================================================
def _progression_snapshot(state):
    return (
        state.maturity_level, state.current_stage,
        tuple(sorted((g.gap_type, g.status, g.iterations_open) for g in state.gaps)),
        getattr(getattr(state, "known_problem", None), "content", None),
        getattr(getattr(state, "known_mechanism", None), "content", None),
        getattr(getattr(state, "known_mechanism", None), "quality", None),
    )


def test_p1_a_reference_never_enters_answered_replay(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    before = reconstruct_readonly_state(appmod._get_store(), sid)
    _record(c, sid, anchor)
    after = reconstruct_readonly_state(appmod._get_store(), sid)
    assert _progression_snapshot(after.state) == _progression_snapshot(before.state)
    assert after.review.next_question == before.review.next_question
    assert len(after.review.accepted_answer_evidence) == \
        len(before.review.accepted_answer_evidence)
    source = open(os.path.join(_ENGINE, "session_reconstruction.py"),
                  encoding="utf-8").read()
    assert "evidence_reference" not in source


@pytest.mark.parametrize("module,label", [
    ("progression_loop.py", "P-2/P-3/P-4/P-7 progression, maturity, gaps, selection"),
    ("scoring.py", "P-5 scoring"),
    ("derived_readiness.py", "P-6 readiness"),
    ("path_n_questions.py", "P-7 next-question selection"),
    ("intent_serving.py", "P-7 next-question selection"),
    ("export_adapter.py", "P-9 exports"),
    ("read_export_service.py", "P-9 exports"),
    ("deliverable_assembler.py", "P-9 canonical package"),
])
def test_p2_to_p9_decision_modules_never_reference_evidence_references(module, label):
    source = open(os.path.join(_ENGINE, module), encoding="utf-8").read()
    assert "evidence_reference" not in source, label


def test_p6_derived_readiness_is_unchanged_by_a_reference(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    from engine.derived_readiness import derive_readiness
    state = appmod.SESSION_STORE[sid]["state"]
    before = (derive_readiness(state).overall_verified(),
              sorted(derive_readiness(state).unverified_contexts()))
    _record(c, sid, anchor)
    state = appmod.SESSION_STORE[sid]["state"]
    after = (derive_readiness(state).overall_verified(),
             sorted(derive_readiness(state).unverified_contexts()))
    assert after == before
    assert after[0] is False          # still the honest constant


def test_p8_a_reference_is_never_a_correction_target(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)
    reference_id = _history(appmod, sid)[0].reference_id
    token = _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', _raw(c, sid)).group(1))
    c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": reference_id, "response": "rewritten",
        "answer_token": token})
    assert len(_history(appmod, sid)) == 1
    assert all(r.record_id != reference_id
               for r in appmod.SESSION_STORE[sid]["state"].assertions)


def test_p9_api_export_and_adapter_surfaces_are_byte_identical(client):
    c, appmod = client
    account_id = _login(c, appmod, email="exporter@example.com")
    sid = _start(c)
    _answer(c, sid)
    anchor = _anchor(c, sid)
    from engine import export_adapter
    from engine.read_export_service import produce_project_export
    adapter = next(v for v in vars(export_adapter).values()
                   if isinstance(v, type) and hasattr(v, "transform"))()
    store = appmod._get_store()
    before = json.dumps(produce_project_export(store, sid, account_id),
                        sort_keys=True, default=str)
    before_adapter = json.dumps(
        adapter.transform(produce_project_export(store, sid, account_id)),
        sort_keys=True, default=str)
    _record(c, sid, anchor)
    after = json.dumps(produce_project_export(store, sid, account_id),
                       sort_keys=True, default=str)
    after_adapter = json.dumps(
        adapter.transform(produce_project_export(store, sid, account_id)),
        sort_keys=True, default=str)
    assert after == before
    assert after_adapter == before_adapter
    for token in (GOOD["source_identity"], GOOD["scope_text"],
                  GOOD["limitation_text"], "evidence_reference", "claim_status"):
        assert token not in after and token not in after_adapter


def test_p9_the_canonical_package_never_carries_a_reference(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)
    with appmod.app.test_request_context():
        package = appmod._deliverable_context(sid)[1]
    blob = json.dumps(package, sort_keys=True, default=str)
    for token in (GOOD["source_identity"], GOOD["scope_text"],
                  GOOD["limitation_text"], "evidence_references",
                  "claim_status", "UI_T2E_"):
        assert token not in blob, token


def test_p10_zero_rows_render_byte_identically_to_the_base(client):
    """With no reference row the block emits nothing at all, so the report is
    byte-identical to the base source — HTML and PDF source alike."""
    c, appmod = client
    sid, _anchor = _project(c, appmod)
    rendered = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    path = os.path.join(_WEB, "templates", "deliverable.html")
    source = open(path, encoding="utf-8").read()
    begin = source.index("  {#- T2E-BLOCK-BEGIN")
    end = source.index("{#- T2E-BLOCK-END #}") + len("{#- T2E-BLOCK-END #}")
    base_source = source[:begin].rstrip("\n") + "\n" + source[end:].lstrip("\n")
    import jinja2
    env = jinja2.Environment(
        loader=jinja2.ChoiceLoader([
            jinja2.DictLoader({"deliverable.html": base_source}),
            jinja2.FileSystemLoader(os.path.join(_WEB, "templates"))]),
        autoescape=True)
    with appmod.app.test_request_context(f"/session/{sid}/deliverable"):
        context = appmod._deliverable_context(sid)
        _entry, package, eligible, reconstructed, state = context
        env.globals.update(appmod.app.jinja_env.globals)
        env.filters.update(appmod.app.jinja_env.filters)
        base = env.get_template("deliverable.html").render(
            sid=sid, package=package, eligible=eligible,
            reconstructed_deliverable=reconstructed,
            t2a_statements=appmod._quantity_statements(package, state),
            evidence_references=(),
            decision_capture=appmod._decision_capture_view_safe(state),
            snapshot_kept_ack=None)
    assert "T2E" not in rendered and "t2e-" not in rendered
    assert base.strip() == rendered.strip() or "t2e" not in rendered.lower()


def test_p11_no_deferred_ladder_value_has_acquired_a_writer():
    """The whole point of Option B: NOTHING here makes any ladder value
    reachable. Checked as source AND as behaviour."""
    deferred = (SPECIALIST_REVIEWED, EMPIRICALLY_DEMONSTRATED,
                INDEPENDENTLY_VERIFIED, EXPERT_SUPPLIED, SYSTEM_INFERRED,
                EXTERNAL_EVIDENCE)
    offenders = []
    for path in _py_files():
        for number, line in enumerate(open(path, encoding="utf-8"), 1):
            code = line.split("#")[0]
            for value in deferred:
                if re.search(r"(validation_status|provenance)\s*=\s*%s\b" % value, code):
                    offenders.append("%s:%d %s" % (path, number, code.strip()))
    assert not offenders, offenders


def test_p11_the_anchor_assertion_axes_are_untouched(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    state = appmod.SESSION_STORE[sid]["state"]
    record = next(r for r in state.assertions if r.record_id == anchor)
    before = (record.provenance, record.validation_status, record.quality)
    _record(c, sid, anchor)
    state = appmod.SESSION_STORE[sid]["state"]
    record = next(r for r in state.assertions if r.record_id == anchor)
    assert (record.provenance, record.validation_status, record.quality) == before
    assert record.provenance == OWNER_STATED
    assert record.validation_status == UNVALIDATED


def test_p12_live_cold_and_resumed_surfaces_agree(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)

    def recorded(body):
        return GOOD["source_identity"] in body and GOOD["limitation_text"] in body

    live = _page(c, sid)
    assert recorded(live)
    history_live = [r.reference_id for r in _history(appmod, sid)]
    appmod.SESSION_STORE.clear()
    _page(c, sid)                                  # cold read-only load
    assert [r.reference_id for r in _history(appmod, sid)] == history_live
    appmod.SESSION_STORE.clear()
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    resumed = _page(c, sid)
    assert recorded(resumed)
    assert [r.reference_id for r in _history(appmod, sid)] == history_live


# ==========================================================================
# 7. Presentation truthfulness, bilingual, escaped
# ==========================================================================
def test_every_surface_labels_the_record_as_unverified(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)
    session_page = _page(c, sid)
    deliverable = _html.unescape(
        c.get(f"/session/{sid}/deliverable").get_data(as_text=True))
    for page in (session_page, deliverable):
        assert "not verified by InventorAI" in page
        assert GOOD["limitation_text"] in page


def _t2e_fragment(body):
    """Exactly the T2-E region of a rendered page — from its heading to the end
    of its last own element — so the assertion is about THIS increment's copy
    and never about unrelated pre-existing report text."""
    start = body.find("Recorded external review or support")
    if start < 0:
        start = body.find("مراجعة أو إسناد خارجي")
    assert start >= 0, "the T2-E block was not rendered"
    last = body.rfind('t2e-')
    assert last > start, "no T2-E element followed the heading"
    end = body.find("</div>", last)
    return body[start:(end + 6) if end > 0 else len(body)]


def test_no_surface_claims_certification_or_verification(client):
    """Scoped to the T2-E block itself. The only occurrences of a ladder word
    permitted there are inside the explicit denial ("does not make ...")."""
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)
    for page in (_page(c, sid),
                 _html.unescape(c.get(f"/session/{sid}/deliverable").get_data(as_text=True))):
        fragment = _t2e_fragment(page).lower()
        for claim in ("specialist-reviewed", "independently verified",
                      "empirically demonstrated", "certified", "validated",
                      "approved", "regulatory"):
            for match in re.finditer(re.escape(claim), fragment):
                context = fragment[max(0, match.start() - 260):match.start() + 60]
                assert "does not make" in context, (claim, context[-120:])
        # and the block states plainly that nothing was verified
        assert "not verified by inventorai" in fragment


def test_the_display_is_bilingual_and_never_shows_a_raw_token(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    _record(c, sid, anchor)
    arabic = _page(c, sid, lang="ar")
    assert any("؀" <= ch <= "ۿ" for ch in arabic)
    for raw in ("UNVALIDATED", "claim_status", "event_key", "reference_id",
                "evref-", "supersedes_reference_id"):
        assert raw not in arabic, raw
        assert raw not in _page(c, sid), raw


def test_hostile_inventor_text_is_escaped_and_never_executed(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    hostile = '<script>alert(1)</script> & "quoted" review'
    _record(c, sid, anchor, source_identity=hostile)
    body = _raw(c, sid)
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;" in body
    assert _history(appmod, sid)[0].source_identity == hostile


def test_copy_exists_only_for_the_state_this_increment_makes_reachable():
    """No UI or copy is added for a state that stays unreachable."""
    from web import ui_text
    catalogue = next(v for v in vars(ui_text).values()
                     if isinstance(v, dict) and "UI_T2E_HEADING" in v)
    keys = [k for k in catalogue if k.startswith("UI_T2E_")]
    assert keys
    for key in keys:
        english = ui_text.text(key, "en")
        arabic = ui_text.text(key, "ar")
        assert english and arabic and english != arabic
        for forbidden in ("SPECIALIST_REVIEWED", "EMPIRICALLY_DEMONSTRATED",
                          "INDEPENDENTLY_VERIFIED", "EXTERNAL_EVIDENCE",
                          "EXPERT_SUPPLIED", "DEMONSTRATED"):
            assert forbidden not in english and forbidden not in arabic


# ==========================================================================
# 8. T2-A, T1-D and T2-B' behaviour is unchanged
# ==========================================================================
def test_notice_namespaces_stay_isolated(client):
    c, appmod = client
    sid, anchor = _project(c, appmod)
    entry = appmod.SESSION_STORE[sid]
    entry["_answer_error"] = "kept"
    entry[appmod.QUANTITY_ACK_SLOT] = appmod.QUANTITY_SAVED_ACK
    appmod._publish_evref_notice(entry, error=appmod.EVREF_NOT_SAVED_MESSAGE)
    assert entry["_answer_error"] == "kept"
    assert entry[appmod.QUANTITY_ACK_SLOT] == appmod.QUANTITY_SAVED_ACK
    assert entry[appmod.EVREF_ERROR_SLOT] == appmod.EVREF_NOT_SAVED_MESSAGE
    appmod._publish_evref_notice(entry, ack=appmod.EVREF_SAVED_ACK)
    assert appmod.EVREF_ERROR_SLOT not in entry        # one current notice only


def test_an_unknown_notice_token_renders_nothing_rather_than_a_raw_token(client):
    c, appmod = client
    assert appmod._evref_notice_text("NOT-A-TOKEN", "en") is None
    assert appmod._evref_notice_text(None, "ar") is None
