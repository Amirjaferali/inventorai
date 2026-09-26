"""T2-G legacy migration — EXPLICIT CONFIRMED engine-version adoption.

`T2G-LEGACY-MIGRATION-IMPLEMENT-01` (Owner policy B). Route-level journeys
against the real integrated code, plus the store's chain rules. Every fixture
is synthetic; no real-user record is used and no real project data is
migrated. Assertions read FULL served-question identities and canonical
state, never a selected phrase.

Plan items proven here (Owner instruction §10): A eligible P1 adoption changes
the reading by full replay · B eligible P2 adoption reaches the T2-G-2 reading
· C creation stamp unchanged · D raw answers/evidence/provenance unchanged ·
E GET/open/cold review never write · F ineligible projects refuse · G a
forged request version is ignored · H replay/restart/resume agree · I
append-back restores the prior reading byte-identically · J EN/AR
equivalence · K cold review/banner/deliverable reflect durable adoption
without mutation · L the T2-D feedback revision changes · M zero-adoption
projects are unchanged · N DDL idempotent on a populated pre-adoption
database · O no project-version UPDATE mutation.
"""
import copy
import html as _html
import inspect
import re
import sqlite3

import pytest

import web.app as appmod
from engine import account_credentials as acct
from engine.deliverable_assembler import assemble_deliverable
from engine.intent_serving import compute_intent_coverage
from engine.idea_state import MECHANISM_COMPLETENESS as MC
from engine.record_contract import ProjectRecordContract, assertion_to_dict
from engine.record_store import (
    SqliteRecordStore, EngineVersionAdoption, AdoptionChainConflict,
    AdoptionHistoryError, AdoptionCapReached, ADOPTION_INSERTED,
    ADOPTION_EXACT_REPLAY, MAX_ENGINE_VERSION_ADOPTIONS_PER_PROJECT,
    validate_adoption_history)
from engine.session_reconstruction import (
    ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2,
    RECONSTRUCTION_VERSION, SUPPORTED_ENGINE_CONTRACT_VERSIONS,
    STATUS_VERSION_MISMATCH, reconstruct_readonly_state,
    reconstruct_review_state)
from tests.csrf_client import csrf_client

PW = "correct horse battery staple"
MECH_SEED = ("A folding mechanical wheelchair ramp with a spring latch. The "
             "inventor wants the ramp to stay reliably locked in the flat, "
             "load-bearing position and to fold away without tools")

# The exact T2-G fixtures the accepted journeys used (byte-identical copies).
F1_AFFIRM = ("The load path runs from the deck panel into the hinge line and "
             "the spring latch transfers force into the frame rail, so the "
             "ramp stays locked flat.")
F2_UNKNOWN = ("I do not know the load path, and I have not worked out how the "
              "hinge line transfers force into the frame rail at all.")
CONCISE_EN = "Deck transfers force into rail."

Q2 = "PATHN:mechanical:MECHANISM_COMPLETENESS:Q2"
Q3 = "PATHN:mechanical:MECHANISM_COMPLETENESS:Q3"
COV_Q2 = ["mechanical:MECHANISM_COMPLETENESS:Q2"]

ADOPT_ROUTE = "/session/{sid}/engine-version"
EN_AFTER = "This project now runs under the adopted current rules"
AR_AFTER = "يعمل هذا المشروع الآن وفق القواعد الحالية المعتمدة"
EN_BEFORE = "This project was created under an earlier version of the rules"
AR_BEFORE = "أُنشئ هذا المشروع وفق إصدار أسبق من القواعد"
EN_COLD = "This saved project runs under rules it adopted after it was created"
AR_COLD = "يعمل هذا المشروع المحفوظ وفق قواعد اعتمدها بعد إنشائه"
EN_ACK = "This project now runs under the current rules."
AR_ACK = "يعمل هذا المشروع الآن وفق القواعد الحالية."
FORBIDDEN_WORDS = ("upgraded", "improved", "corrected", "invalid", "stale",
                   "engineering verified", "engineering-verified")


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("INVENTORAI_DB_PATH", str(tmp_path / "eva.sqlite"))
    monkeypatch.setattr(appmod, "_STORE", None)
    appmod.SESSION_STORE.clear()
    appmod.app.config["TESTING"] = True
    with csrf_client(appmod.app) as c:
        yield c, appmod, str(tmp_path / "eva.sqlite")


def _login(c, appmod, email="owner@example.com"):
    store = appmod._get_account_store()
    aid = acct.new_account_id()
    store.create_account(aid, acct.normalize_email(email), acct.hash_password(PW),
                         "2026-01-01T00:00:00.000000Z", status="active")
    store.mark_email_verified(aid, "2026-01-01T00:00:00.000000Z")
    assert c.post("/login", data={"email": email, "password": PW}).status_code == 302
    return aid


def _start(c, seed=MECH_SEED, domain="mechanical"):
    r = c.post("/start", data={"idea": seed, "domain_confirm": domain})
    assert r.status_code == 302
    return r.headers["Location"].rsplit("/", 1)[-1]


def _stamped_start(c, appmod, version, seed=MECH_SEED, domain="mechanical"):
    """A project genuinely CREATED under `version` (the creation constant is
    the only thing changed); no history is ever rewritten."""
    original = appmod.CURRENT_ENGINE_CONTRACT_VERSION
    appmod.CURRENT_ENGINE_CONTRACT_VERSION = version
    try:
        return _start(c, seed, domain)
    finally:
        appmod.CURRENT_ENGINE_CONTRACT_VERSION = original


def _legacy_start(c, appmod):
    return _stamped_start(c, appmod, RECONSTRUCTION_VERSION)


def _t2g1_start(c, appmod):
    return _stamped_start(c, appmod, ENGINE_CONTRACT_VERSION_T2G1)


def _raw(c, sid, lang=None):
    if lang:
        assert c.post("/ui-language", data={"lang": lang}).status_code in (302, 303)
    body = c.get(f"/session/{sid}").get_data(as_text=True)
    if lang:
        c.post("/ui-language", data={"lang": "en"})
    return body


def _page(c, sid, lang=None):
    return _html.unescape(_raw(c, sid, lang))


def _token(c, sid):
    return _html.unescape(re.search(
        r'name="answer_token" value="([^"]+)"', _raw(c, sid)).group(1))


def _answer(c, sid, text):
    return c.post(f"/session/{sid}", data={
        "response": text, "answer_token": _token(c, sid), "action": "answered"})


def _adopt(c, sid, action="adopt", confirm="yes", extra=None, token=None):
    data = {"answer_token": token or _token(c, sid),
            "version_action": action, "confirm_adoption": confirm}
    if extra:
        data.update(extra)
    return c.post(ADOPT_ROUTE.format(sid=sid), data=data)


def _snapshot(appmod, sid):
    entry = appmod.SESSION_STORE[sid]
    state = entry["state"]
    qctx = appmod._resolve_question_context(state, entry.get("last_result"))
    gap = state.get_gap(qctx.gap_type) if qctx.gap_type else None
    return {
        "version": getattr(state, "engine_contract_version", None),
        "identity": qctx.identity,
        "gap": qctx.gap_type,
        "status": None if gap is None else gap.status,
        "known_mechanism": (None if state.known_mechanism is None
                            else state.known_mechanism.quality),
        "known_problem": (None if state.known_problem is None
                          else state.known_problem.quality),
        "coverage": sorted(compute_intent_coverage(state, qctx.gap_type) or []),
        "unknowns": len(getattr(state, "acknowledged_unknowns", [])),
        "records": len(state.assertions),
        "maturity": state.maturity_level,
        "stage": state.current_stage,
        "gaps": sorted((g.gap_type, g.status) for g in state.gaps),
    }


def _stamp(db, sid):
    con = sqlite3.connect(db)
    try:
        return con.execute(
            "SELECT engine_contract_version FROM projects WHERE project_id=?",
            (sid,)).fetchone()[0]
    finally:
        con.close()


def _adoption_rows(db, sid):
    con = sqlite3.connect(db)
    try:
        return con.execute(
            "SELECT adoption_seq, from_version, to_version, supersedes_adoption_id "
            "FROM engine_version_adoptions WHERE project_id=? ORDER BY adoption_seq",
            (sid,)).fetchall()
    finally:
        con.close()


def _ledger(appmod, sid):
    return [assertion_to_dict(r)
            for r in appmod._get_store().load_contract(sid).assertions]


def _pinned_package(monkeypatch, state):
    """The canonical deliverable package with the ONLY volatile field (the
    generation clock) pinned, so two packages from equal state compare
    byte-identically — the accepted T2-G-2 test-local pin precedent."""
    import engine.deliverable_assembler as da
    monkeypatch.setattr(da, "_now_iso", lambda: "2026-01-01T00:00:00Z")
    return assemble_deliverable(copy.deepcopy(state))


LEGACY_READING = {"identity": Q3, "status": "PARTIAL", "known_mechanism": "REASONED",
                  "coverage": COV_Q2, "unknowns": 1}
CURRENT_READING = {"identity": Q2, "status": "OPEN", "known_mechanism": None,
                   "coverage": [], "unknowns": 1}


def _reading(snap):
    return {k: snap[k] for k in LEGACY_READING}


# ==========================================================================
# A / B / C / D — confirmed adoption changes the reading by FULL replay
# ==========================================================================
def test_a_p1_confirmed_adoption_changes_the_reading_through_full_replay(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    before = _snapshot(appmod, sid)
    assert _reading(before) == LEGACY_READING            # pre-T2-G reading
    assert before["version"] == RECONSTRUCTION_VERSION
    assert _adopt(c, sid).status_code == 302
    after = _snapshot(appmod, sid)
    assert _reading(after) == CURRENT_READING            # T2-G-2 reading
    assert after["version"] == ENGINE_CONTRACT_VERSION_T2G2
    assert after["records"] == before["records"]         # nothing added/removed
    assert _adoption_rows(db, sid) == [
        (0, RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2, None)]
    page = _page(c, sid)
    assert EN_ACK in page and EN_AFTER in page
    assert "recognising some ways of saying you do not know" in page  # t2g2 copy


def test_b_p2_confirmed_adoption_reaches_the_t2g2_reading(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _t2g1_start(c, appmod)
    _answer(c, sid, CONCISE_EN)
    before = _snapshot(appmod, sid)
    # The accepted T2-G-1 reading of a concise answer: relevant and recorded
    # as ASSERTED, but NOT covered, so Q2 is served again.
    assert before["identity"] == Q2 and before["status"] == "PARTIAL"
    assert before["known_mechanism"] == "ASSERTED" and before["coverage"] == []
    assert _adopt(c, sid).status_code == 302
    after = _snapshot(appmod, sid)
    assert after["version"] == ENGINE_CONTRACT_VERSION_T2G2
    assert after["identity"] == Q3 and after["status"] == "PARTIAL"
    assert after["known_mechanism"] == "ASSERTED" and after["coverage"] == COV_Q2
    assert _adoption_rows(db, sid) == [
        (0, ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2, None)]


def test_c_the_creation_stamp_is_never_updated(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert _adopt(c, sid).status_code == 302
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION
    assert appmod._get_store().load_reconstruction_inputs(sid)[
        "engine_contract_version"] == RECONSTRUCTION_VERSION
    assert _adopt(c, sid, action="revert").status_code == 302
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION
    assert len(_adoption_rows(db, sid)) == 2


def test_d_raw_answers_evidence_and_provenance_are_unchanged(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F1_AFFIRM)
    _answer(c, sid, F2_UNKNOWN)
    ledger_before = _ledger(appmod, sid)
    inputs_before = appmod._get_store().load_reconstruction_inputs(sid)
    assert _adopt(c, sid).status_code == 302
    assert _ledger(appmod, sid) == ledger_before
    assert appmod._get_store().load_reconstruction_inputs(sid) == inputs_before
    assert _adopt(c, sid, action="revert").status_code == 302
    assert _ledger(appmod, sid) == ledger_before


# ==========================================================================
# E / K — GET, open, cold review and deliverable never write
# ==========================================================================
def test_e_get_open_cold_review_and_deliverable_never_write(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    for _ in range(3):
        assert c.get(f"/session/{sid}").status_code == 200
    appmod.SESSION_STORE.clear()
    cold = _page(c, sid)
    assert "engine-version" not in cold and EN_BEFORE not in cold
    assert c.get(f"/session/{sid}/deliverable").status_code == 200
    assert reconstruct_review_state(appmod._get_store(), sid).adoption_count == 0
    assert _adoption_rows(db, sid) == []
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION
    # The offer appears only on a WRITABLE session (explicit resume).
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert "engine-version" in _raw(c, sid)
    assert _adoption_rows(db, sid) == []


def test_k_cold_review_banner_and_deliverable_reflect_durable_adoption_without_mutation(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert _adopt(c, sid).status_code == 302
    live = _snapshot(appmod, sid)
    appmod.SESSION_STORE.clear()
    cold = _page(c, sid)
    assert EN_COLD in cold
    assert "engine-version" not in cold                    # no control offered
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert session.review.effective_engine_contract_version == ENGINE_CONTRACT_VERSION_T2G2
    assert session.review.adoption_count == 1
    assert appmod._resolve_question_context(session.state, None).identity == live["identity"]
    deliverable = c.get(f"/session/{sid}/deliverable")
    assert deliverable.status_code == 200
    assert _adoption_rows(db, sid) == [
        (0, RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2, None)]
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION
    assert _page(c, sid, lang="ar").count(AR_COLD) == 1


# ==========================================================================
# F — ineligible / unsupported / current-version / read-only projects refuse
# ==========================================================================
def test_f_a_current_version_project_refuses(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _start(c)            # the routing-aware current stamp (Slice 1)
    _answer(c, sid, F2_UNKNOWN)
    assert "engine-version" not in _raw(c, sid)
    assert _adopt(c, sid).status_code == 302
    assert _adoption_rows(db, sid) == []
    assert "could not be applied just now" in _page(c, sid)
    from engine.session_reconstruction import ENGINE_CONTRACT_VERSION_NR1
    assert _snapshot(appmod, sid)["version"] == ENGINE_CONTRACT_VERSION_NR1


def test_f_a_project_without_an_active_answer_refuses(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    assert "engine-version" not in _raw(c, sid)
    assert _adopt(c, sid).status_code == 302
    assert _adoption_rows(db, sid) == []


def test_f_a_cold_read_only_session_refuses(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    token = _token(c, sid)
    appmod.SESSION_STORE.clear()
    _raw(c, sid)                                           # cold-loads a read-only entry
    assert getattr(appmod.SESSION_STORE[sid]["state"], "domain", None) is None
    assert _adopt(c, sid, token=token).status_code == 302
    assert _adoption_rows(db, sid) == []


def test_f_a_non_path_n_legacy_ilt_project_refuses(client):
    c, appmod, db = client
    _login(c, appmod)
    r = c.post("/start_ilt002_water_leak", data={
        "idea": "A water leak sensor that cuts power to the pump when wet."})
    assert r.status_code == 302
    sid = r.headers["Location"].rsplit("/", 1)[-1]
    state = appmod.SESSION_STORE[sid]["state"]
    assert getattr(state, "path", None) != "N"
    assert appmod._eva_eligibility(sid, state) is None
    assert _adoption_rows(db, sid) == []


def test_f_a_p0_project_without_reconstruction_state_is_never_eligible(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "p0.sqlite"))
    store.create_project(ProjectRecordContract(idea_id="idea-p0", assertions=[]),
                         project_id="p0")
    assert store.load_reconstruction_inputs("p0") is None
    assert reconstruct_review_state(store, "p0").level == 0
    assert store.load_engine_version_adoptions("p0") == ()
    store.close()


# ==========================================================================
# G — the request never controls the version; explicit confirmation required
# ==========================================================================
@pytest.mark.parametrize("extra", [
    {"version": ENGINE_CONTRACT_VERSION_T2G1},
    {"engine_contract_version": "p4-2-level1-recon-v1-bogus"},
    {"to_version": ENGINE_CONTRACT_VERSION_T2G2},
])
def test_g_a_forged_request_version_is_ignored(client, extra):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert _adopt(c, sid, extra=extra).status_code == 302
    assert _adoption_rows(db, sid) == []
    assert _reading(_snapshot(appmod, sid)) == LEGACY_READING


@pytest.mark.parametrize("action, confirm", [
    ("adopt", ""), ("adopt", "no"), ("upgrade", "yes"), ("", "yes"),
    ("revert", "yes"),                       # nothing to revert yet
])
def test_g_missing_confirmation_or_unknown_action_refuses(client, action, confirm):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert _adopt(c, sid, action=action, confirm=confirm).status_code == 302
    assert _adoption_rows(db, sid) == []


def test_g_a_missing_or_forged_answer_token_refuses_before_any_durable_call(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert _adopt(c, sid, token="forged.token").status_code == 302
    assert _adoption_rows(db, sid) == []
    assert _reading(_snapshot(appmod, sid)) == LEGACY_READING


def test_g_a_cross_project_token_refuses(client):
    c, appmod, db = client
    _login(c, appmod)
    sid_a = _legacy_start(c, appmod)
    _answer(c, sid_a, F2_UNKNOWN)
    sid_b = _legacy_start(c, appmod)
    _answer(c, sid_b, F2_UNKNOWN)
    assert _adopt(c, sid_a, token=_token(c, sid_b)).status_code == 302
    assert _adoption_rows(db, sid_a) == []


# ==========================================================================
# H — live replay, restart and explicit resume agree after adoption
# ==========================================================================
@pytest.mark.parametrize("starter", [_legacy_start, _t2g1_start])
def test_h_replay_restart_and_resume_agree_after_adoption(client, starter):
    c, appmod, db = client
    _login(c, appmod)
    sid = starter(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert _adopt(c, sid).status_code == 302
    live = _snapshot(appmod, sid)
    assert live["version"] == ENGINE_CONTRACT_VERSION_T2G2
    appmod.SESSION_STORE.clear()
    session = reconstruct_readonly_state(appmod._get_store(), sid)
    assert getattr(session.state, "engine_contract_version", None) == \
        ENGINE_CONTRACT_VERSION_T2G2
    assert appmod._resolve_question_context(session.state, None).identity == \
        live["identity"]
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _snapshot(appmod, sid) == live
    # A later answer on the resumed session is read under the adopted version.
    _answer(c, sid, F1_AFFIRM)
    assert _snapshot(appmod, sid)["version"] == ENGINE_CONTRACT_VERSION_T2G2


# ==========================================================================
# I — append-back adoption restores the prior reading byte-identically
# ==========================================================================
def test_i_append_back_restores_the_prior_reading_byte_identically(client, monkeypatch):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F1_AFFIRM)
    _answer(c, sid, F2_UNKNOWN)
    before = _snapshot(appmod, sid)
    package_before = _pinned_package(monkeypatch, appmod.SESSION_STORE[sid]["state"])
    assert _adopt(c, sid).status_code == 302
    adopted = _snapshot(appmod, sid)
    assert adopted != before
    assert _adopt(c, sid, action="revert").status_code == 302
    reverted = _snapshot(appmod, sid)
    assert reverted == before
    assert _pinned_package(monkeypatch, appmod.SESSION_STORE[sid]["state"]) == package_before
    rows = _adoption_rows(db, sid)
    assert [(r[1], r[2]) for r in rows] == [
        (RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2),
        (ENGINE_CONTRACT_VERSION_T2G2, RECONSTRUCTION_VERSION)]
    assert rows[1][3] is not None                          # a successor, not a deletion
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION
    page = _page(c, sid)
    assert "This project has returned to the earlier rules" in page
    assert EN_AFTER not in page                            # runs under its creation rules again
    assert "does not read the meaning of your answers" in page   # legacy disclosure again
    # And it can adopt again — another appended row, still no rewrite.
    assert _adopt(c, sid).status_code == 302
    assert _snapshot(appmod, sid) == adopted
    assert len(_adoption_rows(db, sid)) == 3


def test_f1_a_second_revert_after_adopt_then_revert_is_refused(client):
    """F-1 (`T2G-LEGACY-MIGRATION-REPAIR-01`): after adopt → revert the head is
    `t2g2 → v1`; a further `revert` would append `v1 → t2g2` while the
    confirmation still says "return to the earlier rules". Revert is offered and
    accepted only when the head's `from_version` is not the current version."""
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert _adopt(c, sid).status_code == 302
    assert 'id="engine-version-revert"' in _raw(c, sid)      # genuine revert offered
    assert _adopt(c, sid, action="revert").status_code == 302
    reverted = _snapshot(appmod, sid)
    rows_after_revert = _adoption_rows(db, sid)
    assert len(rows_after_revert) == 2
    assert reverted["version"] == RECONSTRUCTION_VERSION
    # 1. no revert form/control after the first revert; adopt still offered
    page = _page(c, sid)
    assert 'id="engine-version-revert"' not in page
    assert "Return to the earlier rules" not in page
    assert 'id="engine-version-adopt"' in page
    elig = appmod._eva_eligibility(sid, appmod.SESSION_STORE[sid]["state"])
    assert elig["can_revert"] is False and elig["can_adopt"] is True
    assert elig["adopted"] is False
    # 2./3. a direct manual second revert POST is refused and appends nothing
    assert _adopt(c, sid, action="revert").status_code == 302
    assert _adoption_rows(db, sid) == rows_after_revert
    assert "could not be applied just now" in _page(c, sid)
    # 4. the effective version remains the earlier version, live and durable
    assert _snapshot(appmod, sid) == reverted
    appmod.SESSION_STORE.clear()
    review = reconstruct_review_state(appmod._get_store(), sid)
    assert review.effective_engine_contract_version == RECONSTRUCTION_VERSION
    assert review.adoption_count == 2
    # 5. disclosure stays consistent: creation rules, no "adopted rules" line
    cold = _page(c, sid)
    assert EN_COLD not in cold
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    page = _page(c, sid)
    assert EN_AFTER not in page and "does not read the meaning of your answers" in page
    assert 'id="engine-version-revert"' not in page
    # 6. adopt remains available and works; then a genuine revert is offered again
    assert _adopt(c, sid).status_code == 302
    assert len(_adoption_rows(db, sid)) == 3
    assert _snapshot(appmod, sid)["version"] == ENGINE_CONTRACT_VERSION_T2G2
    assert 'id="engine-version-revert"' in _raw(c, sid)
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION


def test_i_a_cold_reconstruction_after_revert_matches_the_pre_adoption_reconstruction(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    appmod.SESSION_STORE.clear()
    original = reconstruct_review_state(appmod._get_store(), sid)
    _raw(c, sid)
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert _adopt(c, sid).status_code == 302
    assert _adopt(c, sid, action="revert").status_code == 302
    appmod.SESSION_STORE.clear()
    reverted = reconstruct_review_state(appmod._get_store(), sid)
    fields = ("level", "status", "maturity_level", "current_stage", "open_gaps",
              "next_question", "accepted_answer_evidence", "withdrawn_source_records",
              "effective_engine_contract_version")
    assert {f: getattr(reverted, f) for f in fields} == \
        {f: getattr(original, f) for f in fields}
    assert reverted.adoption_count == 2 and original.adoption_count == 0


# ==========================================================================
# J — English and Arabic flows are equivalent
# ==========================================================================
def test_j_english_and_arabic_flows_are_equivalent(client):
    c, appmod, db = client
    _login(c, appmod)
    sid_en = _legacy_start(c, appmod)
    _answer(c, sid_en, F2_UNKNOWN)
    assert _adopt(c, sid_en).status_code == 302
    en_after = _snapshot(appmod, sid_en)
    sid_ar = _legacy_start(c, appmod)
    _answer(c, sid_ar, F2_UNKNOWN)
    assert c.post("/ui-language", data={"lang": "ar"}).status_code in (302, 303)
    offer = _html.unescape(c.get(f"/session/{sid_ar}").get_data(as_text=True))
    assert AR_BEFORE in offer and EN_BEFORE not in offer
    assert 'dir="rtl"' in offer
    assert _adopt(c, sid_ar).status_code == 302
    after = _html.unescape(c.get(f"/session/{sid_ar}").get_data(as_text=True))
    assert AR_ACK in after and AR_AFTER in after and EN_AFTER not in after
    c.post("/ui-language", data={"lang": "en"})
    ar_after = _snapshot(appmod, sid_ar)
    assert _reading(ar_after) == _reading(en_after) == CURRENT_READING
    assert ar_after["version"] == en_after["version"] == ENGINE_CONTRACT_VERSION_T2G2
    assert _adoption_rows(db, sid_ar) == _adoption_rows(db, sid_en)


def test_j_the_copy_never_uses_the_forbidden_words(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    offer = _page(c, sid)
    block = offer[offer.index('id="engine-version"'):offer.index("EVA-BLOCK-END")
                  if "EVA-BLOCK-END" in offer else len(offer)]
    for word in FORBIDDEN_WORDS:
        assert word not in block.lower()
    assert _adopt(c, sid).status_code == 302
    after = _page(c, sid)
    for word in FORBIDDEN_WORDS:
        assert word not in after[after.index(EN_ACK):after.index(EN_ACK) + 400].lower()
        assert word not in after[after.index(EN_AFTER):after.index(EN_AFTER) + 300].lower()
    import web.ui_text as ui_text
    for key, entry in ui_text.UI_STRINGS.items():
        if key.startswith("UI_EVA_"):
            for word in FORBIDDEN_WORDS:
                assert word not in entry["en"].lower(), (key, word)


# ==========================================================================
# L — the T2-D feedback context revision changes after an adoption
# ==========================================================================
def test_l_the_feedback_revision_changes_after_adoption(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    state = appmod.SESSION_STORE[sid]["state"]
    store = appmod._get_store()
    before = appmod._feedback_ledger_revision(sid, state)
    assert before is not None
    assert store.feedback_revision_ids(sid) == store.ledger_record_ids(sid)
    assert _adopt(c, sid).status_code == 302
    state = appmod.SESSION_STORE[sid]["state"]
    after = appmod._feedback_ledger_revision(sid, state)
    assert after is not None and after != before
    ids = store.feedback_revision_ids(sid)
    assert ids[:-1] == store.ledger_record_ids(sid) and ids[-1].startswith("eva:")
    assert _adopt(c, sid, action="revert").status_code == 302
    state = appmod.SESSION_STORE[sid]["state"]
    reverted = appmod._feedback_ledger_revision(sid, state)
    assert reverted not in (before, after)                 # history matters, not just the version


def test_l_a_feedback_context_rendered_before_an_adoption_is_refused_after_it(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F1_AFFIRM)
    page = _raw(c, sid)
    m = re.search(r'name="context_token" value="([^"]+)"', page)
    assert m is not None
    context_token = _html.unescape(m.group(1))
    assert _adopt(c, sid).status_code == 302
    r = c.post(f"/session/{sid}/question-feedback",
               data={"context_token": context_token, "choice": "HELPFUL"})
    assert r.status_code == 302
    assert appmod._get_store().load_question_feedback(sid) == ()


# ==========================================================================
# M — zero-adoption projects and deliverables are unchanged
# ==========================================================================
@pytest.mark.parametrize("starter", [_legacy_start, _t2g1_start, _start])
def test_m_zero_adoption_projects_render_and_reconstruct_exactly_as_before(client, starter):
    c, appmod, db = client
    _login(c, appmod)
    sid = starter(c) if starter is _start else starter(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    page = _page(c, sid)
    assert EN_AFTER not in page and EN_ACK not in page and "eva-notice" not in page
    store = appmod._get_store()
    assert store.feedback_revision_ids(sid) == store.ledger_record_ids(sid)
    assert store.load_engine_version_adoptions(sid) == ()
    appmod.SESSION_STORE.clear()
    review = reconstruct_review_state(store, sid)
    assert review.level == 1 and review.adoption_count == 0
    assert review.effective_engine_contract_version == _stamp(db, sid)
    cold = _page(c, sid)
    assert EN_COLD not in cold and "engine-version" not in cold
    assert c.get(f"/session/{sid}/deliverable").status_code == 200
    assert _adoption_rows(db, sid) == []


# ==========================================================================
# N / O — DDL idempotent on a populated pre-adoption database; no UPDATE path
# ==========================================================================
def _seed_store(path):
    store = SqliteRecordStore(path)
    store.create_project(
        ProjectRecordContract(idea_id="idea-1", assertions=[]), project_id="p1",
        reconstruction_inputs={"seed_idea_text": MECH_SEED,
                               "confirmed_domain": "mechanical", "path": "N",
                               "engine_contract_version": RECONSTRUCTION_VERSION})
    return store


def _adoption(store, from_v, to_v, sup=None, aid=None, ek=None):
    return EngineVersionAdoption(
        adoption_id=aid or store.new_adoption_id(), adoption_seq=-1,
        from_version=from_v, to_version=to_v, supersedes_adoption_id=sup,
        event_key=ek or ("ek-" + (aid or "x")), recorded_iteration=0,
        recorded_at="2026-01-01T00:00:00+00:00")


def test_n_the_migration_is_idempotent_on_a_populated_pre_adoption_database(tmp_path):
    path = str(tmp_path / "pop.sqlite")
    store = _seed_store(path)
    before = store.load_contract("p1")
    store.close()
    # Simulate an existing populated PRE-adoption database exactly: the table
    # this candidate adds does not exist yet; every other table and row does.
    con = sqlite3.connect(path)
    con.execute("DROP TABLE engine_version_adoptions")
    con.commit()
    assert con.execute("SELECT engine_contract_version FROM projects WHERE project_id='p1'"
                       ).fetchone()[0] == RECONSTRUCTION_VERSION
    con.close()
    for _ in range(3):
        reopened = SqliteRecordStore(path)
        assert reopened.load_engine_version_adoptions("p1") == ()
        after = reopened.load_contract("p1")
        assert [a.record_id for a in after.assertions] == \
            [a.record_id for a in before.assertions]
        assert reopened.load_reconstruction_inputs("p1")["engine_contract_version"] == \
            RECONSTRUCTION_VERSION
        assert reopened._conn.execute("PRAGMA foreign_key_check").fetchall() == []
        reopened.close()
    reopened = SqliteRecordStore(path)
    assert reopened.append_engine_version_adoption(
        "p1", _adoption(reopened, RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2,
                        aid="a1"), expected_head_id=None) == ADOPTION_INSERTED
    assert reopened.load_reconstruction_inputs("p1")["engine_contract_version"] == \
        RECONSTRUCTION_VERSION
    reopened.close()


def test_n_a_fresh_database_creates_the_exact_index_set(tmp_path):
    store = SqliteRecordStore(str(tmp_path / "fresh.sqlite"))
    names = {row[0] for row in store._conn.execute(
        "SELECT name FROM sqlite_master WHERE tbl_name='engine_version_adoptions'")}
    assert {"engine_version_adoptions", "engine_version_adoptions_event_key_uq",
            "engine_version_adoptions_seq_uq", "engine_version_adoptions_successor_uq",
            "engine_version_adoptions_root_uq"} <= names
    store.close()


def test_o_no_project_version_update_mutation_is_introduced():
    import engine.record_store as rs
    source = inspect.getsource(rs)
    # No SQL UPDATE statement anywhere in the project store (the word may
    # appear in prose that states exactly this; a statement is a string).
    assert not re.search(r"""["']\s*UPDATE\b""", source)
    assert not re.search(r"\bexecute\([^)]*\bUPDATE\b", source)
    route = inspect.getsource(appmod.adopt_engine_version)
    store_method = inspect.getsource(rs.SqliteRecordStore.append_engine_version_adoption)
    for text in (route, store_method):
        assert not re.search(r"""["']\s*UPDATE\b""", text)
        assert "engine_contract_version =" not in text.replace("adoption.", "")


# ==========================================================================
# Store chain rules — refusals decided before any row is written
# ==========================================================================
def test_store_chain_rules_refuse_before_writing(tmp_path):
    store = _seed_store(str(tmp_path / "chain.sqlite"))
    with pytest.raises(AdoptionChainConflict):             # wrong from_version
        store.append_engine_version_adoption(
            "p1", _adoption(store, ENGINE_CONTRACT_VERSION_T2G1,
                            ENGINE_CONTRACT_VERSION_T2G2, aid="w"), expected_head_id=None)
    with pytest.raises(AdoptionChainConflict):             # stale expected head
        store.append_engine_version_adoption(
            "p1", _adoption(store, RECONSTRUCTION_VERSION,
                            ENGINE_CONTRACT_VERSION_T2G2, aid="s"), expected_head_id="ghost")
    assert store.load_engine_version_adoptions("p1") == ()
    assert store.append_engine_version_adoption(
        "p1", _adoption(store, RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2,
                        aid="a1", ek="e1"), expected_head_id=None) == ADOPTION_INSERTED
    assert store.append_engine_version_adoption(          # exact replay: no second row
        "p1", _adoption(store, RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2,
                        aid="a1-again", ek="e1"), expected_head_id=None) == ADOPTION_EXACT_REPLAY
    with pytest.raises(AdoptionChainConflict):             # same key, different event
        store.append_engine_version_adoption(
            "p1", _adoption(store, ENGINE_CONTRACT_VERSION_T2G2, RECONSTRUCTION_VERSION,
                            sup="a1", aid="x", ek="e1"), expected_head_id="a1")
    with pytest.raises(AdoptionChainConflict):             # second root
        store.append_engine_version_adoption(
            "p1", _adoption(store, RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2,
                            aid="r2", ek="e2"), expected_head_id=None)
    with pytest.raises(AdoptionChainConflict):             # does not continue the head
        store.append_engine_version_adoption(
            "p1", _adoption(store, RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G1,
                            sup="a1", aid="c", ek="e3"), expected_head_id="a1")
    with pytest.raises(AdoptionChainConflict):             # a no-op version pair
        store.append_engine_version_adoption(
            "p1", _adoption(store, ENGINE_CONTRACT_VERSION_T2G2, ENGINE_CONTRACT_VERSION_T2G2,
                            sup="a1", aid="n", ek="e4"), expected_head_id="a1")
    assert store.append_engine_version_adoption(
        "p1", _adoption(store, ENGINE_CONTRACT_VERSION_T2G2, RECONSTRUCTION_VERSION,
                        sup="a1", aid="a2", ek="e5"), expected_head_id="a1") == ADOPTION_INSERTED
    history = store.load_engine_version_adoptions("p1")
    assert [(r.adoption_id, r.adoption_seq, r.supersedes_adoption_id) for r in history] == \
        [("a1", 0, None), ("a2", 1, "a1")]
    with pytest.raises(Exception):                         # unknown project
        store.append_engine_version_adoption(
            "nope", _adoption(store, RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2),
            expected_head_id=None)
    store.close()


def test_store_cap_is_enforced_inside_the_transaction(tmp_path):
    store = _seed_store(str(tmp_path / "cap.sqlite"))
    head, current = None, RECONSTRUCTION_VERSION
    for i in range(MAX_ENGINE_VERSION_ADOPTIONS_PER_PROJECT):
        target = (ENGINE_CONTRACT_VERSION_T2G2 if current == RECONSTRUCTION_VERSION
                  else RECONSTRUCTION_VERSION)
        aid = f"a{i}"
        store.append_engine_version_adoption(
            "p1", _adoption(store, current, target, sup=head, aid=aid, ek=f"e{i}"),
            expected_head_id=head)
        head, current = aid, target
    with pytest.raises(AdoptionCapReached):
        store.append_engine_version_adoption(
            "p1", _adoption(store, current, RECONSTRUCTION_VERSION
                            if current != RECONSTRUCTION_VERSION else ENGINE_CONTRACT_VERSION_T2G2,
                            sup=head, aid="over", ek="over"), expected_head_id=head)
    assert len(store.load_engine_version_adoptions("p1")) == \
        MAX_ENGINE_VERSION_ADOPTIONS_PER_PROJECT
    store.close()


def test_a_corrupt_or_unsupported_adoption_history_fails_closed(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    # An adoption to a version this code does not support, written outside
    # the governed route: reconstruction fails closed to Level 0 — it never
    # silently falls back to the creation stamp while an adoption exists.
    con = sqlite3.connect(db)
    con.execute("INSERT INTO engine_version_adoptions VALUES (?,?,?,?,?,?,?,?,?)",
                (sid, 0, "bogus", RECONSTRUCTION_VERSION, "p4-2-level1-recon-v1-x",
                 None, "ek-bogus", 0, "2026-01-01T00:00:00+00:00"))
    con.commit()
    con.close()
    appmod.SESSION_STORE.clear()
    review = reconstruct_review_state(appmod._get_store(), sid)
    assert review.level == 0 and review.status == STATUS_VERSION_MISMATCH
    assert c.get(f"/session/{sid}").status_code == 200        # read-only, no 500
    assert c.post(f"/session/{sid}/resume", data={}).status_code == 302
    assert getattr(appmod.SESSION_STORE[sid]["state"], "domain", None) is None  # not established
    # A structurally broken chain raises the store's history error (no partial
    # state) and every web surface fails closed generically.
    con = sqlite3.connect(db)
    con.execute("DELETE FROM engine_version_adoptions WHERE project_id=?", (sid,))
    con.execute("INSERT INTO engine_version_adoptions VALUES (?,?,?,?,?,?,?,?,?)",
                (sid, 0, "r", RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2,
                 None, "ek-r", 0, "2026-01-01T00:00:00+00:00"))
    con.execute("INSERT INTO engine_version_adoptions VALUES (?,?,?,?,?,?,?,?,?)",
                (sid, 1, "b", ENGINE_CONTRACT_VERSION_T2G1, RECONSTRUCTION_VERSION,
                 "r", "ek-b", 0, "2026-01-01T00:00:00+00:00"))
    con.commit()
    con.close()
    with pytest.raises(AdoptionHistoryError):
        appmod._get_store().load_engine_version_adoptions(sid)
    with pytest.raises(AdoptionHistoryError):
        reconstruct_review_state(appmod._get_store(), sid)
    appmod.SESSION_STORE.clear()
    assert c.get(f"/session/{sid}").status_code == 200
    assert c.get(f"/session/{sid}/deliverable").status_code in (200, 302)
    assert appmod._eva_durable_position(sid) is None


def test_validate_adoption_history_accepts_only_one_continuing_chain():
    def row(aid, f, t, sup):
        return EngineVersionAdoption(aid, 0, f, t, sup, "e" + aid, 0, "2026")
    v1, g1, g2 = (RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G1,
                  ENGINE_CONTRACT_VERSION_T2G2)
    assert validate_adoption_history([]) == []
    good = [row("a", v1, g2, None), row("b", g2, v1, "a"), row("c", v1, g2, "b")]
    assert validate_adoption_history(good) == good
    for bad in ([row("a", v1, g2, "ghost")],
                [row("a", v1, g2, None), row("b", g2, v1, "a"), row("c", v1, g2, "a")],
                [row("a", v1, g2, None), row("b", g1, v1, "a")],
                [row("a", v1, v1, None)]):
        with pytest.raises(AdoptionHistoryError):
            validate_adoption_history(bad)


def test_the_effective_version_is_resolved_once_from_durable_state_only(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert _adopt(c, sid).status_code == 302
    from engine.session_reconstruction import ENGINE_CONTRACT_VERSION_NR1
    assert set(SUPPORTED_ENGINE_CONTRACT_VERSIONS) == {
        RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G1, ENGINE_CONTRACT_VERSION_T2G2,
        ENGINE_CONTRACT_VERSION_NR1}
    source = inspect.getsource(reconstruct_readonly_state.__globals__["_reconstruct"])
    assert source.count("effective_engine_contract_version(") == 1
    module_source = inspect.getsource(
        inspect.getmodule(reconstruct_readonly_state))
    assert "flask" not in module_source and "request.form" not in module_source


# ==========================================================================
# T3-A extension (T3A-PROJECT-RECORD-IMPLEMENT-01): the adoption ledger is
# rendered truthfully in the Project Record as rule changes — adopt then
# return, in ledger order, live and cold, with no consequence claim — and the
# existing EVA disclosure is neither changed nor duplicated by it.
# ==========================================================================
def test_t3a_project_record_lists_adoption_events_truthfully_live_and_cold(client):
    c, appmod, db = client
    _login(c, appmod)
    sid = _legacy_start(c, appmod)
    _answer(c, sid, F2_UNKNOWN)
    assert _adopt(c, sid).status_code == 302
    assert _adopt(c, sid, action="revert").status_code == 302
    con = sqlite3.connect(db)
    try:
        rows = con.execute(
            "SELECT adoption_id, from_version, to_version FROM engine_version_adoptions "
            "WHERE project_id=? ORDER BY adoption_seq", (sid,)).fetchall()
    finally:
        con.close()
    assert [(r[1], r[2]) for r in rows] == [
        (RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2),
        (ENGINE_CONTRACT_VERSION_T2G2, RECONSTRUCTION_VERSION)]

    def record_block(body):
        start = body.index('id="t3a-project-record"')
        end = body.rfind("</details>", start, body.index("</main>", start))
        return body[start:end + len("</details>")]

    def rule_kinds(block):
        return re.findall(r'data-record-kind="(rules_[a-z]+)" data-adoption-id=', block)

    live = _raw(c, sid)
    live_block = record_block(live)
    assert rule_kinds(live_block) == ["rules_adopted", "rules_returned"]
    for word in FORBIDDEN_WORDS + ("recomputed", "asked again", "owed again"):
        assert word not in live_block.lower(), word
    # the EVA disclosure is untouched: after the return the project is back on
    # its creation rules, so the AFTER line is absent as before and the control
    # block is offered once; neither lives inside the record
    assert live.count(EN_AFTER) == 0 and live.count('id="engine-version"') == 1
    assert "engine-version" not in live_block and EN_AFTER not in live_block
    assert "Earlier answers were kept exactly as recorded." in live_block
    appmod.SESSION_STORE.clear()
    cold = _raw(c, sid)
    assert rule_kinds(record_block(cold)) == ["rules_adopted", "rules_returned"]
    assert 'id="engine-version"' not in cold
    assert _adoption_rows(db, sid) == [
        (0, RECONSTRUCTION_VERSION, ENGINE_CONTRACT_VERSION_T2G2, None),
        (1, ENGINE_CONTRACT_VERSION_T2G2, RECONSTRUCTION_VERSION, rows[0][0])]   # unchanged by the cold GET
    assert _stamp(db, sid) == RECONSTRUCTION_VERSION
    assert rule_kinds(record_block(_raw(c, sid, lang="ar"))) == ["rules_adopted", "rules_returned"]
    assert "اعتُمدت قواعد أحدث" in _page(c, sid, lang="ar")
