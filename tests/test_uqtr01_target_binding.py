"""UQTR-01 Step 2B — target-aware question / answer binding (Candidate 02).

Proves, over the real web routes and the real durable store:

* the durable ``AssertionRecord.question_target`` (16th contract field), minted
  ONLY from the verified canonical RVR-7 identity, legacy-None on load, never
  inferred, inherited verbatim by a correction;
* the separate signed ``answer_target`` bound to the sid AND the exact answer
  token of the render that produced the form (never transferable);
* the new-write freshness rule: a consumed token still verifies statelessly but
  can never authorize a NEW write — only an exact durable duplicate is a silent
  no-op; everything else fails closed BEFORE assessment, progression or append;
* the ABA stale-form regression (a Q1 form stays dead after the journey leaves
  Q1 and a legitimate correction makes the same Q1 / gap / engine-contract
  version current again), and a fresh Q1 form then succeeding;
* the closed QUESTION / CRITICALITY_CORRECTION context discriminator;
* effective engine-contract-version binding; EN/AR refusal copy.

Stale, swap and tamper posts use ``answer_binding=False`` and values parsed from
the REAL rendered forms. Fixtures are neutral synthetic ideas written for this
file; the T1-C′ study corpus is not used.
"""
import base64
import html as _html
import json
import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    AssertionRecord, IdeaState, MECHANISM_COMPLETENESS,
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
)
from engine.record_contract import (
    CONTRACT_VERSION, ContractError, ProjectRecordContract, _ASSERTION_FIELDS,
    assertion_from_dict, assertion_to_dict,
)
from tests.csrf_client import csrf_client
from web import ui_text
import web.app as appmod

SEED = ("a small device that switches off a room heater when the room gets "
        "too warm, using a temperature sensor and a relay circuit")
ANSWER = ("The temperature sensor output is compared with a set threshold; when "
          "the room is too warm the comparator switches the relay and the relay "
          "cuts power to the heater until the room cools down again.")
ANSWER_CLOSING = (
    "A thermistor in a voltage divider feeds a comparator with hysteresis; the "
    "comparator output drives a transistor that energises the relay coil, and "
    "the relay contacts open the heater supply line when the measured "
    "temperature passes the set point, closing again once it falls below the "
    "lower threshold.")
WEAK = "I think it works somehow."
TAB_B_TEXT = "Tab B wrote this against the old form and it must never be saved."
NOTE = "I am not sure about this part yet."
STALE_EN = appmod.ANSWER_FORM_STALE_MESSAGE
STALE_AR = ("هذا النموذج لم يعد هو النموذج الحالي، لذلك لم يتم حفظ أي شيء. "
            "يرجى مراجعة السؤال الحالي والإجابة عنه.")
EXHAUSTED = ui_text.RVR7_EXHAUSTED_EXIT_PROMPT


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

@pytest.fixture()
def client():
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c


def _start(c, lang="en"):
    if lang == "ar":
        assert c.post("/ui-language", data={"lang": "ar"}).status_code in (200, 302)
    r = c.post("/start", data={"idea": SEED,
                               "domain_confirm": "electronics_electrical"})
    assert r.status_code == 302, r.status_code
    return r.headers["Location"].rsplit("/", 1)[-1]


def _body(c, sid):
    return c.get(f"/session/{sid}").get_data(as_text=True)


def _form_fields(form_html):
    tok = re.search(r'name="answer_token" value="([^"]*)"', form_html)
    tgt = re.search(r'name="answer_target" value="([^"]*)"', form_html)
    assert tok and tgt, "the rendered form must carry answer_token and answer_target"
    return {"answer_token": _html.unescape(tok.group(1)),
            "answer_target": _html.unescape(tgt.group(1))}


def _answer_form(c, sid):
    """The answer_token + answer_target of the REAL rendered answer form, as a
    browser tab would retain them."""
    body = _body(c, sid)
    m = re.search(r'<form id="answer-form".*?</form>', body, re.S)
    assert m, "the answer form must render"
    return _form_fields(m.group(0))


def _correction_form(c, sid):
    body = _body(c, sid)
    forms = re.findall(r"<form\b[^>]*>.*?</form>", body, re.S)
    corr = [f for f in forms if 'data-draft-field="correction"' in f]
    assert corr, "the criticality-correction form must render"
    return _form_fields(corr[0])


def _decode(target):
    body = target.rpartition(".")[0]
    return json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))


def _post(c, sid, fields, response=ANSWER, action="answered"):
    data = dict(fields, response=response)
    if action is not None:
        data["action"] = action
    r = c.post(f"/session/{sid}", data=data, answer_binding=False)
    assert r.status_code == 302, r.status_code
    return r


def _answer_fresh(c, sid, text):
    _post(c, sid, _answer_form(c, sid), response=text)


def _entry(sid):
    return appmod.SESSION_STORE[sid]


def _state(sid):
    return _entry(sid)["state"]


def _durable(sid):
    return list(appmod._get_store().load_contract(sid).assertions)


def _structural(sid):
    s = _state(sid)
    return ([(g.gap_type, g.status, g.iterations_open) for g in s.gaps],
            s.maturity_level, s.current_stage, s.iteration,
            len(s.assertions), len(_entry(sid)["transcript"]))


def _context(sid):
    e = _entry(sid)
    q = appmod._resolve_question_context(e["state"], e.get("last_result"))
    return q.identity, q.gap_type, getattr(e["state"], "engine_contract_version", None)


class _Spy:
    """Counts the assessment and durable-append seams, so a refusal is proven to
    happen BEFORE any assessment, progression or append."""

    def __init__(self, monkeypatch):
        self.assess = 0
        self.append = 0
        real_run = appmod.run_iteration

        def run(*a, **k):
            self.assess += 1
            return real_run(*a, **k)
        monkeypatch.setattr(appmod, "run_iteration", run)
        store = appmod._get_store()
        real_append = store.append_record

        def append(*a, **k):
            self.append += 1
            return real_append(*a, **k)
        monkeypatch.setattr(store, "append_record", append)


def _assert_refused(c, sid, before_struct, before_durable, spy=None,
                    stale_text=None, message=STALE_EN):
    assert _structural(sid) == before_struct, "no progression on refusal"
    assert len(_durable(sid)) == before_durable, "nothing appended on refusal"
    if spy is not None:
        assert spy.assess == 0, "no assessment before target verification"
        assert spy.append == 0, "no durable append before target verification"
    body = _html.unescape(_body(c, sid))
    assert message in body
    if stale_text is not None:
        # The refused text is never transferred to the current question.
        assert stale_text not in body


def _drive_to_exhausted_partial(c, sid):
    """Weak answers exhaust the mechanism gap's prepared questions; one
    substantive answer leaves it PARTIAL on the same exhausted-exit identity."""
    for i in range(5):
        _answer_fresh(c, sid, "%s %d" % (WEAK, i))
    _answer_fresh(c, sid, ANSWER)
    assert _context(sid)[:2] == (EXHAUSTED, MECHANISM_COMPLETENESS)


# ---------------------------------------------------------------------------
# durable model — carrier and contract
# ---------------------------------------------------------------------------

def test_contract_has_sixteen_fields_and_version_is_unchanged():
    assert len(_ASSERTION_FIELDS) == 16
    assert _ASSERTION_FIELDS[-1] == "question_target"
    assert CONTRACT_VERSION == "p4-0-record-contract-v1"
    assert AssertionRecord(record_id="rec_1", disposition="answered", content="x",
                           gap_context=None, iteration=0).question_target is None


def test_carrier_mint_rules():
    s = IdeaState(idea_id="uqtr-carrier")
    r1 = s.record_interaction(action="answered", content="a",
                              gap_context=MECHANISM_COMPLETENESS,
                              question_target="PATHN:N-MC-1")
    assert r1.question_target == "PATHN:N-MC-1"
    with pytest.raises(ValueError):
        s.record_interaction(action="answered", content="b", question_target="")
    with pytest.raises(ValueError):
        s.record_interaction(action="answered", content="b", question_target=7)
    with pytest.raises(ValueError):
        s.record_interaction(action=DISPOSITION_DECISION_CONTEXT_DECLARED,
                             content="which latch?", question_target="PATHN:N-MC-1")
    # A correction inherits verbatim; a different target is refused, nothing appended.
    n = len(s.assertions)
    with pytest.raises(ValueError):
        s.record_interaction(action="answered", content="fixed",
                             gap_context=MECHANISM_COMPLETENESS,
                             supersedes=[r1.record_id], question_target="PATHN:N-MC-2")
    with pytest.raises(ValueError):
        s.record_interaction(action="answered", content="fixed",
                             gap_context=MECHANISM_COMPLETENESS,
                             supersedes=[r1.record_id])
    assert len(s.assertions) == n
    fixed = s.record_interaction(action="answered", content="fixed",
                                 gap_context=MECHANISM_COMPLETENESS,
                                 supersedes=[r1.record_id],
                                 question_target=r1.question_target)
    assert fixed.question_target == "PATHN:N-MC-1"
    # Legacy None stays None through a correction.
    legacy = s.record_interaction(action="answered", content="old")
    again = s.record_interaction(action="answered", content="old fixed",
                                 supersedes=[legacy.record_id])
    assert again.question_target is None


def _payload(**over):
    p = {"record_id": "rec_1", "disposition": "answered", "content": "c",
         "gap_context": MECHANISM_COMPLETENESS, "iteration": 1,
         "provenance": "OWNER_STATED", "validation_status": "UNVALIDATED",
         "quality": None, "pending": None, "responsibility": "OWNER_INPUT",
         "resolves_gap": False, "contradicts": [], "supersedes": [],
         "superseded_by": None, "decision_context_root": None}
    p.update(over)
    return p


def test_contract_round_trip_and_legacy_load_never_infers():
    s = IdeaState(idea_id="uqtr-rt")
    s.record_interaction(action="answered", content="a",
                         gap_context=MECHANISM_COMPLETENESS,
                         question_target="PATHN:N-MC-1")
    s.record_interaction(action="unknown", content="",
                         gap_context=MECHANISM_COMPLETENESS)
    data = ProjectRecordContract.from_state(s).to_dict()
    assert [p["question_target"] for p in data["assertions"]] == ["PATHN:N-MC-1", None]
    assert ProjectRecordContract.from_dict(data).to_dict() == data
    # Every payload persisted before the field existed loads with None — whatever
    # its disposition or content (content naming a question never becomes one).
    for disposition in ("answered", "unknown", "deferred", "risk_accepted"):
        legacy = _payload(disposition=disposition,
                          content="Answer to PATHN:N-MC-1 (the mechanism question)")
        assert "question_target" not in legacy
        assert assertion_from_dict(legacy).question_target is None
    ctx = _payload(disposition=DISPOSITION_DECISION_CONTEXT_DECLARED, gap_context=None)
    assert assertion_from_dict(ctx).question_target is None
    pre_w2a = _payload()
    del pre_w2a["decision_context_root"]
    assert assertion_from_dict(pre_w2a).question_target is None
    # Every other missing field still fails, and a bad value is rejected.
    broken = _payload()
    del broken["content"]
    with pytest.raises(ContractError):
        assertion_from_dict(broken)
    for bad in ("", 3, ["PATHN:N-MC-1"]):
        with pytest.raises(ContractError):
            assertion_from_dict(_payload(question_target=bad))


def test_contract_validate_rejects_target_on_decision_and_changed_inheritance():
    env = {"contract_version": CONTRACT_VERSION, "idea_id": "p", "assertions": []}
    ctx = _payload(record_id="rec_1", disposition=DISPOSITION_DECISION_CONTEXT_DECLARED,
                   gap_context=None, question_target="PATHN:N-MC-1")
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(dict(env, assertions=[ctx]))
    alt_ok = _payload(record_id="rec_2", disposition=DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
                      gap_context=None, decision_context_root="rec_1",
                      question_target=None)
    ctx_ok = dict(ctx, question_target=None)
    ProjectRecordContract.from_dict(dict(env, assertions=[ctx_ok, alt_ok]))
    prior = _payload(record_id="rec_1", question_target="PATHN:N-MC-1")
    moved = _payload(record_id="rec_2", supersedes=["rec_1"],
                     question_target="PATHN:N-MC-2")
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(dict(env, assertions=[prior, moved]))
    dropped = dict(moved, question_target=None)
    with pytest.raises(ContractError):
        ProjectRecordContract.from_dict(dict(env, assertions=[prior, dropped]))
    kept = dict(moved, question_target="PATHN:N-MC-1")
    loaded = ProjectRecordContract.from_dict(dict(env, assertions=[prior, kept]))
    assert [r.question_target for r in loaded.assertions] == ["PATHN:N-MC-1"] * 2


# ---------------------------------------------------------------------------
# signed answer target
# ---------------------------------------------------------------------------

def test_render_signs_current_context_bound_to_the_render_token(client):
    sid = _start(client)
    form = _answer_form(client, sid)
    identity, gap, ecv = _context(sid)
    assert identity == "PATHN:N-MC-1" and gap == MECHANISM_COMPLETENESS and ecv
    assert _decode(form["answer_target"]) == {
        "k": "QUESTION", "q": identity, "g": gap, "v": ecv}
    assert form["answer_token"] == _entry(sid)["answer_token"]
    verified = appmod._verified_answer_target(sid, form["answer_token"],
                                              form["answer_target"])
    assert tuple(verified) == ("QUESTION", identity, gap, ecv)
    # Not transferable: another (valid) token, or another sid, never verifies.
    other = appmod._issue_answer_token(sid)
    assert appmod._valid_answer_token(sid, other)
    assert appmod._verified_answer_target(sid, other, form["answer_target"]) is None
    assert appmod._verified_answer_target("other-sid", form["answer_token"],
                                          form["answer_target"]) is None


def test_fresh_answer_mints_question_target_durably(client, monkeypatch):
    sid = _start(client)
    form = _answer_form(client, sid)
    identity = _context(sid)[0]
    _post(client, sid, form)
    rec = _state(sid).assertions[-1]
    assert (rec.disposition, rec.question_target) == ("answered", identity)
    durable = _durable(sid)[-1]
    assert (durable.record_id, durable.question_target) == (rec.record_id, identity)
    assert "question_target" in assertion_to_dict(durable)
    assert "answer_token" not in _entry(sid)          # consumed on acceptance


def test_non_answer_mints_target_and_consumes_token(client):
    sid = _start(client)
    form = _answer_form(client, sid)
    identity = _context(sid)[0]
    _post(client, sid, form, response=NOTE, action="unknown")
    rec = _durable(sid)[-1]
    assert (rec.disposition, rec.question_target) == ("unknown", identity)
    assert _entry(sid).get("answer_token") != form["answer_token"]


@pytest.mark.parametrize("mutation", [
    "missing", "empty", "garbage", "tampered_identity", "tampered_gap",
    "tampered_ecv", "unknown_kind", "non_ascii_sig", "oversized"])
def test_missing_malformed_or_tampered_target_fails_closed(client, monkeypatch, mutation):
    sid = _start(client)
    form = _answer_form(client, sid)
    body, _, sig = form["answer_target"].rpartition(".")
    payload = _decode(form["answer_target"])

    def reencode(p):
        raw = json.dumps(p, sort_keys=True, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(raw).decode().rstrip("=") + "." + sig
    target = {
        "missing": None, "empty": "", "garbage": "not-a-target",
        "tampered_identity": reencode(dict(payload, q="PATHN:N-MC-2")),
        "tampered_gap": reencode(dict(payload, g="PHYSICAL_FEASIBILITY")),
        "tampered_ecv": reencode(dict(payload, v="p4-2-level1-recon-v1")),
        "unknown_kind": reencode(dict(payload, k="SOMETHING_ELSE")),
        "non_ascii_sig": body + ".é" + sig[2:],
        "oversized": "a" * 5000 + "." + sig,
    }[mutation]
    fields = {"answer_token": form["answer_token"]}
    if target is not None:
        fields["answer_target"] = target
    before, n = _structural(sid), len(_durable(sid))
    spy = _Spy(monkeypatch)
    _post(client, sid, fields)
    _assert_refused(client, sid, before, n, spy)


def test_target_cannot_be_paired_with_another_answer_token(client, monkeypatch):
    sid = _start(client)
    first = _answer_form(client, sid)
    _post(client, sid, first, response=NOTE, action="unknown")     # rotates token
    second = _answer_form(client, sid)
    assert second["answer_token"] != first["answer_token"]
    # Same question context in both renders — only the token pairing differs.
    assert _decode(second["answer_target"]) == _decode(first["answer_target"])
    before, n = _structural(sid), len(_durable(sid))
    spy = _Spy(monkeypatch)
    _post(client, sid, {"answer_token": second["answer_token"],
                        "answer_target": first["answer_target"]})
    _post(client, sid, {"answer_token": first["answer_token"],
                        "answer_target": second["answer_target"]})
    _assert_refused(client, sid, before, n, spy)
    monkeypatch.undo()
    _post(client, sid, second)                                   # the true pair
    assert len(_durable(sid)) == n + 1


def test_consumed_token_never_authorizes_a_new_write(client, monkeypatch):
    """The non-answer leaves the SAME question current (serving-only
    suppression), so the old form's identity, gap and ECV all still match —
    only the current-token rule refuses it."""
    sid = _start(client)
    old = _answer_form(client, sid)
    _post(client, sid, old, response=NOTE, action="deferred")
    assert appmod._valid_answer_token(sid, old["answer_token"])   # still verifies
    assert _decode(_answer_form(client, sid)["answer_target"]) \
        == _decode(old["answer_target"])
    before, n = _structural(sid), len(_durable(sid))
    spy = _Spy(monkeypatch)
    _post(client, sid, old, response=ANSWER)
    _post(client, sid, old, response=NOTE, action="unknown")
    _assert_refused(client, sid, before, n, spy, stale_text=ANSWER)


def test_exact_durable_duplicate_retry_stays_a_silent_no_op(client):
    sid = _start(client)
    form = _answer_form(client, sid)
    _post(client, sid, form)
    after_first, n = _structural(sid), len(_durable(sid))
    _post(client, sid, form)                                    # refresh / double submit
    assert _structural(sid) == after_first and len(_durable(sid)) == n
    body = _html.unescape(_body(client, sid))
    assert STALE_EN not in body and "could not be saved" not in body
    # Non-answer double submit: one record, the truthful acknowledgement again.
    form = _answer_form(client, sid)
    _post(client, sid, form, response=NOTE, action="unknown")
    n = len(_durable(sid))
    _post(client, sid, form, response=NOTE, action="unknown")
    assert len(_durable(sid)) == n
    body = _html.unescape(_body(client, sid))
    assert STALE_EN not in body


def test_same_old_token_with_different_content_or_target_fails_closed(client, monkeypatch):
    sid = _start(client)
    form = _answer_form(client, sid)
    identity, gap, ecv = _context(sid)
    _post(client, sid, form)
    before, n = _structural(sid), len(_durable(sid))
    spy = _Spy(monkeypatch)
    # (a) same token, different content
    _post(client, sid, form, response=ANSWER + " (edited)")
    _assert_refused(client, sid, before, n, spy, stale_text=ANSWER + " (edited)")
    # (b) same token, same content, but a target (validly signed for that very
    #     token by the server) naming another question: not the stored event,
    #     so it is refused — never the silent duplicate no-op.
    other = appmod._issue_answer_target(
        sid, form["answer_token"],
        appmod._AnswerTarget("QUESTION", "PATHN:N-MC-2", gap, ecv))
    _post(client, sid, {"answer_token": form["answer_token"], "answer_target": other})
    _assert_refused(client, sid, before, n, spy)


def test_cross_session_form_is_refused(client):
    sid_a, sid_b = _start(client), _start(client)
    form_a, form_b = _answer_form(client, sid_a), _answer_form(client, sid_b)
    before, n = _structural(sid_b), len(_durable(sid_b))
    _post(client, sid_b, form_a)                                # token is sid-bound
    _assert_refused(client, sid_b, before, n,
                    message=appmod.ANSWER_NOT_SAVED_MESSAGE)
    _post(client, sid_b, {"answer_token": form_b["answer_token"],
                          "answer_target": form_a["answer_target"]})
    _assert_refused(client, sid_b, before, n)


def test_engine_contract_version_is_bound_and_re_resolved(client, monkeypatch):
    sid = _start(client)
    form = _answer_form(client, sid)
    state = _state(sid)
    live = state.engine_contract_version
    assert _decode(form["answer_target"])["v"] == live
    other = next(v for v in appmod.SUPPORTED_ENGINE_CONTRACT_VERSIONS if v != live)
    state.engine_contract_version = other                      # effective ECV moved
    before, n = _structural(sid), len(_durable(sid))
    spy = _Spy(monkeypatch)
    _post(client, sid, form)
    _assert_refused(client, sid, before, n, spy)
    monkeypatch.undo()
    state.engine_contract_version = live
    _post(client, sid, _answer_form(client, sid))
    assert len(_durable(sid)) == n + 1


# ---------------------------------------------------------------------------
# ABA stale-form regression
# ---------------------------------------------------------------------------

def test_aba_stale_form_is_refused_after_the_same_question_returns(client, monkeypatch):
    sid = _start(client)
    _drive_to_exhausted_partial(client, sid)
    # A. Q1 renders in tab A and tab B; tab B keeps the complete old form.
    tab_a = _answer_form(client, sid)
    tab_b = _answer_form(client, sid)
    assert tab_a == tab_b
    q1 = _decode(tab_b["answer_target"])
    assert (q1["k"], q1["q"], q1["g"]) == ("QUESTION", EXHAUSTED, MECHANISM_COMPLETENESS)
    # B. Tab A submits a valid current response; the journey advances past Q1.
    _post(client, sid, tab_a, response=ANSWER_CLOSING)
    advanced = _context(sid)
    assert advanced[0] != EXHAUSTED and advanced[1] != MECHANISM_COMPLETENESS
    # C. The existing correction path withdraws that answer; replay makes the
    #    SAME canonical Q1 current again under the SAME effective ECV.
    closing = _state(sid).assertions[-1]
    assert closing.question_target == EXHAUSTED
    r = client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": closing.record_id,
        "response": WEAK + " (corrected)",
        "answer_token": appmod._answer_token_for(sid, _entry(sid))})
    assert r.status_code == 302
    assert _entry(sid).get("_interaction_ack") == appmod.CORRECTION_APPLIED_ACK
    assert _state(sid).assertions[-1].question_target == EXHAUSTED  # inherited
    assert _context(sid) == (q1["q"], q1["g"], q1["v"])            # Q1 is back
    # D. The ORIGINAL tab-B form: identity, gap and ECV all equal — still refused.
    before, n = _structural(sid), len(_durable(sid))
    spy = _Spy(monkeypatch)
    _post(client, sid, tab_b, response=TAB_B_TEXT)
    _post(client, sid, tab_b, response=TAB_B_TEXT, action="unknown")
    _assert_refused(client, sid, before, n, spy, stale_text=TAB_B_TEXT)
    # D'. Tab B resubmitting EXACTLY tab A's accepted event is the verified
    #     durable duplicate: a silent no-op — nothing appended, nothing assessed.
    _post(client, sid, tab_b, response=ANSWER_CLOSING)
    assert _structural(sid) == before and len(_durable(sid)) == n
    assert spy.assess == 0 and spy.append == 0
    monkeypatch.undo()
    # E/F. A FRESH Q1 form (same Q1 context, new token) is accepted normally.
    fresh = _answer_form(client, sid)
    assert fresh["answer_token"] != tab_b["answer_token"]
    assert _decode(fresh["answer_target"]) == q1
    _post(client, sid, fresh, response=ANSWER_CLOSING + " Checked again.")
    assert len(_durable(sid)) == n + 1
    rec = _durable(sid)[-1]
    assert (rec.content, rec.question_target) == (
        ANSWER_CLOSING + " Checked again.", EXHAUSTED)
    assert STALE_EN not in _html.unescape(_body(client, sid))


# ---------------------------------------------------------------------------
# criticality-correction context
# ---------------------------------------------------------------------------

def _completed_at_correction_stage():
    from tests import test_structured_criticality as ws4
    c, sid = ws4._start(ws4.IDEA_WS1)
    ws4._drive_ws1_journey_to_completion(c, sid)
    ftok = ws4._focus_token(ws4._page(c, sid))
    assert c.post(f"/session/{sid}", data={
        "criticality_action": "summary_change", "focus_token": ftok}).status_code == 302
    return c, sid, ws4


def test_criticality_correction_context_is_explicit_and_mints_no_question():
    c, sid, _ = _completed_at_correction_stage()
    form = _correction_form(c, sid)
    ecv = _state(sid).engine_contract_version
    assert _decode(form["answer_target"]) == {
        "k": "CRITICALITY_CORRECTION", "q": None, "g": None, "v": ecv}
    n = len(_durable(sid))
    text = "The enclosure also needs a vent near the relay."
    _post(c, sid, form, response=text, action=None)
    rec = _durable(sid)[-1]
    assert len(_durable(sid)) == n + 1
    assert (rec.content, rec.gap_context, rec.question_target) == (text, None, None)
    appmod.SESSION_STORE.pop(sid, None)


def test_question_context_cannot_be_substituted_for_criticality_correction(monkeypatch):
    c, sid, ws4 = _completed_at_correction_stage()
    form = _correction_form(c, sid)
    ecv = _state(sid).engine_contract_version
    # Identical null identity / null gap / ECV — only the kind differs.
    forged = appmod._issue_answer_target(
        sid, form["answer_token"], appmod._AnswerTarget("QUESTION", None, None, ecv))
    before, n = _structural(sid), len(_durable(sid))
    spy = _Spy(monkeypatch)
    _post(c, sid, {"answer_token": form["answer_token"], "answer_target": forged},
          response="Substituted context text.", action=None)
    _assert_refused(c, sid, before, n, spy, stale_text="Substituted context text.")
    appmod.SESSION_STORE.pop(sid, None)


def test_criticality_correction_cannot_be_substituted_for_question(client, monkeypatch):
    sid = _start(client)
    form = _answer_form(client, sid)
    forged = appmod._issue_answer_target(
        sid, form["answer_token"],
        appmod._AnswerTarget("CRITICALITY_CORRECTION", None, None,
                             _state(sid).engine_contract_version))
    before, n = _structural(sid), len(_durable(sid))
    spy = _Spy(monkeypatch)
    _post(client, sid, {"answer_token": form["answer_token"], "answer_target": forged},
          action=None)
    _assert_refused(client, sid, before, n, spy)


def test_reentering_correction_context_retires_the_earlier_correction_form(monkeypatch):
    c, sid, ws4 = _completed_at_correction_stage()
    old = _correction_form(c, sid)
    # Leave the correction stage without writing, then enter it again.
    _post(c, sid, {"answer_token": old["answer_token"], "answer_target": "x"},
          response="leave", action=None)
    ftok = ws4._focus_token(ws4._page(c, sid))
    c.post(f"/session/{sid}", data={"criticality_action": "summary_change",
                                     "focus_token": ftok})
    new = _correction_form(c, sid)
    assert new["answer_token"] != old["answer_token"]
    assert _decode(new["answer_target"]) == _decode(old["answer_target"])
    before, n = _structural(sid), len(_durable(sid))
    spy = _Spy(monkeypatch)
    _post(c, sid, old, response="Old correction form text.", action=None)
    _assert_refused(c, sid, before, n, spy, stale_text="Old correction form text.")
    appmod.SESSION_STORE.pop(sid, None)


# ---------------------------------------------------------------------------
# correction / legacy / reconstruction
# ---------------------------------------------------------------------------

def test_correction_inherits_target_even_after_the_question_moved(client):
    sid = _start(client)
    _answer_fresh(client, sid, ANSWER)
    first = _state(sid).assertions[-1]
    assert first.question_target == "PATHN:N-MC-1"
    assert _context(sid)[0] != "PATHN:N-MC-1"           # the journey moved on
    _body(client, sid)
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": first.record_id, "response": ANSWER + " Revised.",
        "answer_token": _entry(sid)["answer_token"]})
    corrected = _durable(sid)[-1]
    assert corrected.supersedes == [first.record_id]
    assert corrected.question_target == "PATHN:N-MC-1"  # never re-derived


def _strip_question_target_from_durable_rows(sid):
    """Rewrite this project's stored payloads to the pre-field shape (no
    `question_target` key) — simulating rows persisted before this change."""
    con = sqlite3.connect(os.environ["INVENTORAI_DB_PATH"])
    try:
        rows = con.execute("SELECT record_id, payload FROM records "
                           "WHERE project_id = ?", (sid,)).fetchall()
        for record_id, payload in rows:
            data = json.loads(payload)
            data.pop("question_target", None)
            con.execute("UPDATE records SET payload = ? WHERE project_id = ? "
                        "AND record_id = ?",
                        (json.dumps(data, sort_keys=True), sid, record_id))
        con.commit()
    finally:
        con.close()
    return len(rows)


def test_resume_preserves_targets_and_legacy_rows_load_none(client):
    sid = _start(client)
    _answer_fresh(client, sid, ANSWER)
    _post(client, sid, _answer_form(client, sid), response=NOTE, action="unknown")
    targets = [r.question_target for r in _durable(sid)]
    assert targets[0] == "PATHN:N-MC-1" and all(targets)
    # Restart + explicit writable resume: reconstruction keeps them verbatim.
    appmod.SESSION_STORE.pop(sid)
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert [r.question_target for r in _state(sid).assertions
            if r.record_id in {d.record_id for d in _durable(sid)}] == targets
    # Legacy rows (no key at all) load with None — nothing is inferred — and a
    # correction of such a record keeps None.
    appmod.SESSION_STORE.pop(sid)
    assert _strip_question_target_from_durable_rows(sid) >= 2
    assert [r.question_target for r in _durable(sid)] == [None] * len(targets)
    assert client.post(f"/session/{sid}/resume", data={}).status_code == 302
    legacy = next(r for r in _state(sid).assertions if r.disposition == "answered")
    assert legacy.question_target is None
    _body(client, sid)
    client.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": legacy.record_id, "response": ANSWER + " Legacy fix.",
        "answer_token": _entry(sid)["answer_token"]})
    fixed = _durable(sid)[-1]
    assert fixed.supersedes == [legacy.record_id] and fixed.question_target is None
    # A NEW write after resume still mints from the verified identity.
    identity = _context(sid)[0]
    _post(client, sid, _answer_form(client, sid))
    assert _durable(sid)[-1].question_target == identity


# ---------------------------------------------------------------------------
# EN / AR refusal copy
# ---------------------------------------------------------------------------

def test_catalogue_pair_is_the_owner_copy():
    assert ui_text.text("UI_UQTR_FORM_STALE", "en") == STALE_EN == (
        "This response form is no longer current, so nothing was saved. "
        "Please review the current question and respond there.")
    assert ui_text.text("UI_UQTR_FORM_STALE", "ar") == STALE_AR
    assert ui_text.localize_message(STALE_EN, "ar") == STALE_AR


@pytest.mark.parametrize("lang", ["en", "ar"])
def test_stale_form_refusal_is_localized_and_generic(client, lang):
    sid = _start(client, lang=lang)
    old = _answer_form(client, sid)
    _post(client, sid, old, response=NOTE, action="unknown")
    _post(client, sid, old, response=TAB_B_TEXT)
    body = _html.unescape(_body(client, sid))
    expected = STALE_AR if lang == "ar" else STALE_EN
    assert re.search(r'<p id="answer-error" role="alert"[^>]*>' + re.escape(expected) + "</p>",
                     body)
    assert TAB_B_TEXT not in body
    if lang == "ar":
        assert re.search(r'<html lang="ar" dir="rtl">', body)
        assert STALE_EN not in body
    # Nothing names the failed condition.
    for word in ("token", "signature", "target", "engine-contract", "hmac"):
        assert word not in expected.lower()
