"""W2-A / RVR-4 — web reachability, persistence ordering, EN/AR, correction
(frozen contract §14/§15; RVR4-REACH-1..7, RVR4-LANG-1..4, RVR4-CORR-1..4,
RVR4-OW6-5).

The bounded decision-capture capability lives INSIDE the existing Path-N
journey (session + deliverable surfaces): no second page, no second journey,
no Decision Workspace activation.
"""
import os, re, sys, html

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest

from engine.idea_state import (
    DECISION_ACTION_DISPOSITIONS,
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN,
    OWNER_STATED,
)


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "w2a.sqlite"))
    import web.app as appmod
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with appmod.app.test_client() as c:
        yield c, appmod


SEED = ("a manually foldable wheelchair ramp for a home doorway — the inventor "
        "wants the ramp to stay reliably locked in the flat, load-bearing "
        "position and to fold away without tools")
QUESTION = "Which latch mechanism should hold the ramp flat?"


def _start(c):
    r = c.post("/start", data={"idea": SEED, "domain_confirm": "mechanical"})
    assert r.status_code == 302 and "/session/" in r.headers["Location"]
    return r.headers["Location"].rsplit("/", 1)[-1]


def _token(c, sid):
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    m = re.search(r'name="answer_token" value="([^"]+)"', page)
    return html.unescape(m.group(1))


def _ledger(appmod, sid, disposition):
    state = appmod.SESSION_STORE[sid]["state"]
    return [r for r in state.assertions if r.disposition == disposition]


def _declare_context(c, sid, content=QUESTION):
    return c.post(f"/session/{sid}/decision/declare-context", data={
        "content": content, "answer_token": _token(c, sid)})


def _declare_alt(c, sid, root, content="Toggle latch"):
    return c.post(f"/session/{sid}/decision/declare-alternative", data={
        "content": content, "context_root": root,
        "answer_token": _token(c, sid)})


# --- RVR4-REACH-1/2: declare context + alternative through the journey -------

def test_reach_1_2_declare_context_and_alternative(client):
    c, appmod = client
    sid = _start(c)
    r = _declare_context(c, sid)
    assert r.status_code == 302
    recs = _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)
    assert len(recs) == 1 and recs[0].content == QUESTION
    assert recs[0].provenance == OWNER_STATED
    root = recs[0].record_id
    r = _declare_alt(c, sid, root)
    assert r.status_code == 302
    alts = _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED)
    assert len(alts) == 1 and alts[0].decision_context_root == root
    # composed state rendered on the session page (existing journey surface)
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert QUESTION in page and "Toggle latch" in page


# --- RVR4-REACH-3: refinement preserves identity -----------------------------

def test_reach_3_refine_alternative(client):
    c, appmod = client
    sid = _start(c)
    _declare_context(c, sid)
    root = _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)[0].record_id
    _declare_alt(c, sid, root)
    alt = _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED)[0]
    r = c.post(f"/session/{sid}/decision/refine-alternative", data={
        "content": "Toggle latch with locking spring",
        "supersedes_record_id": alt.record_id,
        "answer_token": _token(c, sid)})
    assert r.status_code == 302
    from engine.decision_composition import compose_decision_records
    rec = compose_decision_records(appmod.SESSION_STORE[sid]["state"])[0]
    assert [x.candidate_id for x in rec.candidates] == [f"cand-pn-{alt.record_id}"]
    assert rec.candidates[0].name == "Toggle latch with locking spring"


# --- RVR4-REACH-4: withdrawal ------------------------------------------------

def test_reach_4_withdraw_alternative(client):
    c, appmod = client
    sid = _start(c)
    _declare_context(c, sid)
    root = _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)[0].record_id
    _declare_alt(c, sid, root)
    alt = _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED)[0]
    r = c.post(f"/session/{sid}/decision/withdraw-alternative", data={
        "supersedes_record_id": alt.record_id, "reason": "not robust",
        "answer_token": _token(c, sid)})
    assert r.status_code == 302
    from engine.decision_composition import compose_decision_records
    rec = compose_decision_records(appmod.SESSION_STORE[sid]["state"])[0]
    assert rec.candidates == []                       # projected out
    state = appmod.SESSION_STORE[sid]["state"]
    assert any(x.record_id == alt.record_id for x in state.assertions)  # history kept
    assert _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN)


# --- RVR4-REACH-5 / RVR4-OW6-5-adjacent: persist-before-acknowledge ----------

def test_reach_5_no_false_success_on_persistence_failure(client):
    c, appmod = client
    sid = _start(c)
    from engine.record_store import StoreError
    store = appmod._get_store()

    def _boom(*a, **k):
        raise StoreError("durable append unavailable")
    orig = store.append_record
    try:
        store.append_record = _boom
        r = _declare_context(c, sid)
        assert r.status_code == 302
    finally:
        store.append_record = orig
    # NOTHING acknowledged, NOTHING in live state
    assert _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED) == []
    entry = appmod.SESSION_STORE[sid]
    assert entry.get("_interaction_ack") is None
    assert entry.get("_answer_error")          # the truthful failure message


# --- invalid form input fails closed, nothing minted -------------------------

def test_invalid_decision_posts_fail_closed(client):
    c, appmod = client
    sid = _start(c)
    # alternative with no declared context
    r = _declare_alt(c, sid, "rec_999")
    assert r.status_code == 302
    assert _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED) == []
    # forged token
    r = c.post(f"/session/{sid}/decision/declare-context", data={
        "content": QUESTION, "answer_token": "forged"})
    assert _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED) == []
    # empty content
    c.post(f"/session/{sid}/decision/declare-context", data={
        "content": "   ", "answer_token": _token(c, sid)})
    assert _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED) == []


# --- RVR4-REACH-6: composed state on session AND deliverable surfaces --------

def test_reach_6_rendered_on_deliverable_surface(client):
    c, appmod = client
    sid = _start(c)
    _declare_context(c, sid)
    root = _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)[0].record_id
    _declare_alt(c, sid, root)
    page = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    assert QUESTION in page and "Toggle latch" in page


# --- RVR4-REACH-7 / RVR4-CORR: reload parity + provenance integrity ----------

def test_reach_7_reconstruction_returns_same_decision_truth(client):
    c, appmod = client
    sid = _start(c)
    _declare_context(c, sid)
    root = _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)[0].record_id
    _declare_alt(c, sid, root)
    alt = _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED)[0]
    c.post(f"/session/{sid}/decision/refine-alternative", data={
        "content": "Refined toggle", "supersedes_record_id": alt.record_id,
        "answer_token": _token(c, sid)})
    import json
    from engine.decision_composition import compose_decision_records
    live = [json.dumps(r.to_record_dict(), sort_keys=True)
            for r in compose_decision_records(appmod.SESSION_STORE[sid]["state"])]
    # cold reconstruction from the durable store
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    cold = [json.dumps(r.to_record_dict(), sort_keys=True)
            for r in compose_decision_records(recon.state)]
    assert cold == live


def test_corr_existing_correction_route_refuses_decision_targets(client):
    # RVR4-OW6-5 + RVR4-CORR: RVR-5 /correct stays answered-only — a decision
    # record can never be "corrected" into the answered stream.
    c, appmod = client
    sid = _start(c)
    _declare_context(c, sid)
    ctx = _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)[0]
    r = c.post(f"/session/{sid}/correct", data={
        "supersedes_record_id": ctx.record_id, "response": "overwrite attempt",
        "answer_token": _token(c, sid)})
    assert r.status_code == 302
    state = appmod.SESSION_STORE[sid]["state"]
    fresh = [x for x in state.assertions if x.record_id == ctx.record_id][0]
    assert fresh.superseded_by is None        # untouched
    assert appmod.SESSION_STORE[sid].get("_answer_error")


# --- N-2 repair: retry identity vs new user intent (route-level) -------------
# Independent External Review finding N-2 (MATERIAL): the decision routes must
# distinguish an accidental retry/double-submit (same issued token = same
# request instance) from a DELIBERATE new founding declaration with byte-
# identical text (new render = new token). Text equality is never canonical
# event identity. These compose the frozen engine-level ID-5 semantics with
# the real user route (the composition the original 51-item inventory lacked).

def _alt_records(appmod, sid):
    return _ledger(appmod, sid, DISPOSITION_DECISION_ALTERNATIVE_DECLARED)


def test_n2_1_identical_alternative_redeclare_after_withdraw_succeeds(client):
    c, appmod = client
    sid = _start(c)
    state = appmod.SESSION_STORE[sid]["state"]
    iter_before = state.iteration
    _declare_context(c, sid)
    root = _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)[0].record_id
    _declare_alt(c, sid, root, "Toggle latch")
    a1 = _alt_records(appmod, sid)[0]
    c.post(f"/session/{sid}/decision/withdraw-alternative", data={
        "supersedes_record_id": a1.record_id, "answer_token": _token(c, sid)})
    # deliberate redeclaration, BYTE-IDENTICAL text, no iteration advance
    r = _declare_alt(c, sid, root, "Toggle latch")
    assert r.status_code == 302
    alts = _alt_records(appmod, sid)
    assert len(alts) == 2                                  # NEW founding record
    redeclared = alts[1]
    assert redeclared.record_id != a1.record_id            # NEW root
    assert redeclared.superseded_by is None and not redeclared.supersedes
    from engine.decision_composition import compose_decision_records
    rec = compose_decision_records(state)[0]
    assert [x.candidate_id for x in rec.candidates] == [
        f"cand-pn-{redeclared.record_id}"]                 # NEW cand-pn identity
    assert f"cand-pn-{a1.record_id}" not in [x.candidate_id for x in rec.candidates]
    assert state.iteration == iter_before                  # no iteration advance
    assert appmod.SESSION_STORE[sid].get("_answer_error") is None


def test_n2_2_redeclare_still_succeeds_after_reload(client):
    c, appmod = client
    sid = _start(c)
    _declare_context(c, sid)
    root = _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)[0].record_id
    _declare_alt(c, sid, root, "Toggle latch")
    a1 = _alt_records(appmod, sid)[0]
    c.post(f"/session/{sid}/decision/withdraw-alternative", data={
        "supersedes_record_id": a1.record_id, "answer_token": _token(c, sid)})
    # simulate a reload between withdrawal and redeclaration: the entry's
    # rendered token is dropped and re-issued on the next GET (the durable
    # idempotency keys survive in the store regardless).
    appmod.SESSION_STORE[sid].pop("answer_token", None)
    c.get(f"/session/{sid}")
    r = _declare_alt(c, sid, root, "Toggle latch")
    assert r.status_code == 302
    assert len(_alt_records(appmod, sid)) == 2
    # and the durable store carries both founding declarations
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    durable_alts = [x for x in recon.state.assertions
                    if x.disposition == DISPOSITION_DECISION_ALTERNATIVE_DECLARED]
    assert len(durable_alts) == 2


def test_n2_3_identical_text_context_declarations_are_distinct_events(client):
    # Contract-valid (W2-A contract §2/§7: contexts are plural and user-created;
    # every no-supersedes declaration FOUNDS a context; identity is root-based,
    # never text-based): two byte-identical context declarations are two
    # distinct founding events with distinct roots.
    c, appmod = client
    sid = _start(c)
    _declare_context(c, sid, QUESTION)
    r = _declare_context(c, sid, QUESTION)                 # identical bytes
    assert r.status_code == 302
    ctxs = _ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)
    assert len(ctxs) == 2
    assert ctxs[0].record_id != ctxs[1].record_id
    from engine.decision_composition import compose_decision_records
    recs = compose_decision_records(appmod.SESSION_STORE[sid]["state"])
    assert len(recs) == 2 and recs[0].decision_id != recs[1].decision_id


def test_n2_4_sequential_double_submit_mints_no_duplicate(client):
    c, appmod = client
    sid = _start(c)
    tok = _token(c, sid)
    data = {"content": QUESTION, "answer_token": tok}
    c.post(f"/session/{sid}/decision/declare-context", data=data)
    # accidental re-POST of the SAME form (same token, same bytes)
    c.post(f"/session/{sid}/decision/declare-context", data=data)
    assert len(_ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)) == 1
    # durable protection, not just live-state: the store holds exactly one
    from engine.session_reconstruction import reconstruct_readonly_state
    recon = reconstruct_readonly_state(appmod._get_store(), sid)
    assert len([x for x in recon.state.assertions
                if x.disposition == DISPOSITION_DECISION_CONTEXT_DECLARED]) == 1


def test_n2_5_race_shaped_duplicate_key_protection_intact(client):
    # A concurrent race is two requests carrying the SAME issued token over the
    # same live state -> both derive the SAME durable key; the loser hits the
    # store's UNIQUE index. The sequential same-token re-POST above exercises
    # exactly that durable-key path; here we additionally prove the durable
    # UNIQUE constraint itself rejects a second append under the same key.
    c, appmod = client
    sid = _start(c)
    tok = _token(c, sid)
    c.post(f"/session/{sid}/decision/declare-context",
           data={"content": QUESTION, "answer_token": tok})
    import sqlite3 as _sq
    from engine.idea_state import IdeaState
    state = appmod.SESSION_STORE[sid]["state"]
    m = IdeaState(idea_id=state.idea_id)
    m.assertions = list(state.assertions)
    dup = m.record_interaction(action=DISPOSITION_DECISION_CONTEXT_DECLARED,
                               content="racing duplicate")
    key = appmod._interaction_idempotency_key(
        sid, "w2a:declare-context@" + tok, None, state.iteration, QUESTION)
    try:
        appmod._get_store().append_record(sid, dup, idempotency_key=key)
        raised = False
    except _sq.IntegrityError:
        raised = True
    assert raised                                          # UNIQUE key still guards


def test_n2_6_friendly_duplicate_acknowledgement_is_reachable(client):
    # The repaired fingerprint comparison must recognise a true same-request
    # retry like-with-like and acknowledge it (no error, no duplicate).
    c, appmod = client
    sid = _start(c)
    tok = _token(c, sid)
    data = {"content": QUESTION, "answer_token": tok}
    c.post(f"/session/{sid}/decision/declare-context", data=data)
    appmod.SESSION_STORE[sid].pop("_interaction_ack", None)
    appmod.SESSION_STORE[sid].pop("_answer_error", None)
    c.post(f"/session/{sid}/decision/declare-context", data=data)   # retry
    entry = appmod.SESSION_STORE[sid]
    assert entry.get("_interaction_ack")                   # friendly ack
    assert entry.get("_answer_error") is None
    assert len(_ledger(appmod, sid, DISPOSITION_DECISION_CONTEXT_DECLARED)) == 1


# --- RVR4-LANG-1..4 ----------------------------------------------------------

def test_lang_1_every_w2a_key_has_en_and_ar():
    from web import ui_text
    keys = [k for k in ui_text.UI_STRINGS if k.startswith("UI_W2A_")]
    assert keys, "W2-A UI keys must exist"
    for k in keys:
        entry = ui_text.UI_STRINGS[k]
        assert entry.get("en") and entry.get("ar"), k
        assert entry["en"] != entry["ar"], k


def test_lang_2_3_active_language_selects_single_rendering(client):
    from web import ui_text
    c, appmod = client
    sid = _start(c)
    _declare_context(c, sid)
    heading_en = ui_text.UI_STRINGS["UI_W2A_SECTION_HEADING"]["en"]
    heading_ar = ui_text.UI_STRINGS["UI_W2A_SECTION_HEADING"]["ar"]
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert heading_en in page and heading_ar not in page
    with c.session_transaction() as fs:
        fs["ui_lang"] = "ar"
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    assert heading_ar in page and heading_en not in page


def test_lang_4_arabic_input_does_not_switch_ui_language(client):
    from web import ui_text
    c, appmod = client
    sid = _start(c)
    c.post(f"/session/{sid}/decision/declare-context", data={
        "content": "أي آلية مزلاج يجب أن تثبت المنحدر؟",
        "answer_token": _token(c, sid)})
    page = c.get(f"/session/{sid}").get_data(as_text=True)
    heading_en = ui_text.UI_STRINGS["UI_W2A_SECTION_HEADING"]["en"]
    assert heading_en in page                  # UI stays English
    # the user's Arabic content renders verbatim (content is never translated)
    assert "أي آلية مزلاج" in page
