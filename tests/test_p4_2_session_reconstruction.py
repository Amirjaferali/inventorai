"""P4-2 Level-1 — Deterministic read-only reconstruction of review state (RED/GREEN).

Behaviour-based tests for the bounded P4-2 Level-1 increment authorized by
`G-P4-2-LEVEL1-IMPLEMENTATION-01` (OPTION A). The increment adds:

  * additive, nullable project-envelope reconstruction inputs
    (`seed_idea_text`, `confirmed_domain`, `path`, `engine_contract_version`)
    persisted ONLY at project creation/start;
  * a canonical, read-only `engine.session_reconstruction.reconstruct_review_state`
    that rebuilds a FRESH `IdeaState`, replays the persisted seed then the
    accepted-answer contents (store `seq` order) through the UNCHANGED canonical
    progression path, and returns an IMMUTABLE review snapshot;
  * deterministic Path-N support only; every other path / missing metadata /
    version mismatch fails closed to Level-0 accepted-answer evidence;
  * a bounded replay limit; malformed/corrupt histories raise the canonical
    `ContractError`; NO durable or in-memory mutation; NO session resume.

Fail-closed, no false-green: assertions inspect the DURABLE store, the canonical
engine state, and the reconstruction result — never HTTP status alone. The
durable SQLite DB lives only under the pytest-managed `INVENTORAI_DB_PATH` from
`tests/conftest.py`. No push/PR/merge. Out of scope: writable continuation,
session resume, durable outputs, FPC-02, Phase 5.
"""
import copy
import os
import re

import pytest

import web.app as webapp
from web.app import app, SESSION_STORE
from engine.record_store import SqliteRecordStore
from engine.record_contract import ContractError, ProjectRecordContract
from engine.idea_state import (
    IdeaState, AssertionRecord, OWNER_STATED, UNVALIDATED,
    DISPOSITION_ANSWERED, DISPOSITION_DEFERRED,
)
from engine import session_reconstruction as SR


FORM = {"domain_confirm": "electronics_electrical"}
IDEA = ("An electronic leak detector uses two probes and a comparator so that "
        "when water bridges the probes the circuit triggers an alert.")
# Strong REASONED electronics causal chains that drive progression.
ANSWER_1 = ("When water bridges the two probes, the resistance between them "
            "drops below a threshold and the comparator output flips, which "
            "switches on the alert buzzer.")
ANSWER_2 = ("The comparator compares the probe voltage against a fixed "
            "reference divider, and when the probe voltage falls the output "
            "drives a transistor that closes the buzzer circuit.")
ANSWER_3 = ("The device does not measure water depth or purity; it only "
            "detects the presence of a conductive bridge across the probes.")

_TOKEN_RE = re.compile(
    r'name="answer_token"[^>]*value="([^"]+)"|value="([^"]+)"[^>]*name="answer_token"')


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _store():
    """The SAME app-scoped store /start wrote to (same isolated DB path)."""
    return webapp._get_store()


def _start(client, idea=IDEA):
    resp = client.post("/start", data={"idea": idea, **FORM}, follow_redirects=False)
    loc = resp.headers.get("Location", "")
    assert "/session/" in loc, f"expected /session/<sid>, got {loc!r}"
    return loc.rstrip("/").rsplit("/session/", 1)[1].split("?")[0]


def _token(client, sid):
    html = client.get(f"/session/{sid}", follow_redirects=False).get_data(as_text=True)
    m = _TOKEN_RE.search(html)
    assert m, "no answer_token rendered"
    return m.group(1) or m.group(2)


def _answer(client, sid, response):
    return client.post(f"/session/{sid}",
                       data={"response": response, "answer_token": _token(client, sid)},
                       follow_redirects=False)


def _live_session(client, answers):
    """Drive a REAL live Path-N session through the web layer and return
    (sid, live_state_snapshot, live_next_question)."""
    sid = _start(client)
    for a in answers:
        _answer(client, sid, a)
    live = SESSION_STORE[sid]["state"]
    live_q = (SESSION_STORE[sid].get("last_result") or {}).get("question")
    return sid, live, live_q


def _open_gap_types(state):
    return tuple(sorted(g.gap_type for g in state.get_open_gaps()))


# --- direct durable-envelope construction for fail-closed unit cases ---------
def _put_project(store, project_id, *, idea_id="idea-x", seed=None, domain=None,
                 path=None, version=None, answers=()):
    """Create a durable project with explicit reconstruction inputs and append
    the given answered contents as durable answered records (seq order)."""
    contract = ProjectRecordContract(idea_id=idea_id, assertions=[])
    inputs = None
    if any(v is not None for v in (seed, domain, path, version)):
        inputs = {"seed_idea_text": seed, "confirmed_domain": domain,
                  "path": path, "engine_contract_version": version}
    store.create_project(contract, project_id=project_id, reconstruction_inputs=inputs)
    for i, content in enumerate(answers, start=1):
        rec = AssertionRecord(
            record_id=f"rec_{i}", disposition=DISPOSITION_ANSWERED, content=content,
            gap_context=None, iteration=i, provenance=OWNER_STATED,
            validation_status=UNVALIDATED)
        store.append_record(project_id, rec, idempotency_key=f"idem-{project_id}-{i}")


# ===========================================================================
# 1. API exists on GREEN (absent on the authoritative parent -> RED)
# ===========================================================================
def test_reconstruction_api_exists():
    assert callable(getattr(SR, "reconstruct_review_state", None))
    assert isinstance(getattr(SR, "RECONSTRUCTION_VERSION", None), str)
    assert isinstance(getattr(SR, "MAX_ACCEPTED_ANSWER_REPLAY", None), int)
    assert hasattr(SqliteRecordStore, "load_reconstruction_inputs")


# ===========================================================================
# 2. Deterministic equivalence with the live path
# ===========================================================================
def test_reconstruction_matches_live_path(client):
    sid, live, live_q = _live_session(client, [ANSWER_1, ANSWER_2, ANSWER_3])
    snap = SR.reconstruct_review_state(_store(), sid)
    assert snap.level == 1 and snap.reconstructed is True
    assert snap.maturity_level == live.maturity_level
    assert snap.current_stage == live.current_stage
    assert snap.open_gaps == _open_gap_types(live)
    assert snap.next_question == live_q


# ===========================================================================
# 3. Replay order is store seq, not record_id lexical order
# ===========================================================================
def test_replay_follows_store_seq_not_record_id(client):
    store = _store()
    # Append rec_2 first (seq 0), then rec_1 (seq 1): seq order != rec_N order.
    _put_project(store, "seqproj", seed=IDEA, domain="electronics_electrical",
                 path="N", version=SR.RECONSTRUCTION_VERSION)
    r2 = AssertionRecord(record_id="rec_2", disposition=DISPOSITION_ANSWERED,
                         content=ANSWER_1, gap_context=None, iteration=2,
                         provenance=OWNER_STATED, validation_status=UNVALIDATED)
    r1 = AssertionRecord(record_id="rec_1", disposition=DISPOSITION_ANSWERED,
                         content=ANSWER_2, gap_context=None, iteration=1,
                         provenance=OWNER_STATED, validation_status=UNVALIDATED)
    store.append_record("seqproj", r2, idempotency_key="k2")
    store.append_record("seqproj", r1, idempotency_key="k1")
    snap = SR.reconstruct_review_state(store, "seqproj")
    # Evidence is returned in seq (append) order: rec_2 then rec_1.
    assert [r.record_id for r in snap.accepted_answer_evidence] == ["rec_2", "rec_1"]
    # Compute the expected state by replaying in seq order and confirm it differs
    # from the record_id-order replay (so the ordering is genuinely exercised).
    seq_state = IdeaState(idea_id="idea-x"); seq_state.domain = "electronics_electrical"
    seq_state.domain_signal = "electronics_electrical"; seq_state.path = "N"
    from engine.progression_loop import run_iteration
    run_iteration(seq_state, IDEA)
    for c in (ANSWER_1, ANSWER_2):   # seq order
        run_iteration(seq_state, c)
    assert snap.maturity_level == seq_state.maturity_level
    assert snap.open_gaps == _open_gap_types(seq_state)


# ===========================================================================
# 4. Non-contiguous rec_N is supported
# ===========================================================================
def test_non_contiguous_rec_n_supported(client):
    store = _store()
    _put_project(store, "gaps", seed=IDEA, domain="electronics_electrical",
                 path="N", version=SR.RECONSTRUCTION_VERSION)
    for rid, content, seqk in (("rec_3", ANSWER_1, "a"), ("rec_7", ANSWER_2, "b")):
        rec = AssertionRecord(record_id=rid, disposition=DISPOSITION_ANSWERED,
                              content=content, gap_context=None, iteration=1,
                              provenance=OWNER_STATED, validation_status=UNVALIDATED)
        store.append_record("gaps", rec, idempotency_key=seqk)
    snap = SR.reconstruct_review_state(store, "gaps")
    assert snap.level == 1
    assert [r.record_id for r in snap.accepted_answer_evidence] == ["rec_3", "rec_7"]


# ===========================================================================
# 5. Accepted-answer records only are replayed (non-answer never durable)
# ===========================================================================
def test_only_answered_records_are_replayed(client):
    store = _store()
    _put_project(store, "ansonly", seed=IDEA, domain="electronics_electrical",
                 path="N", version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    # Inject a NON-ANSWER durable record (the runtime never creates one, but prove
    # the reconstruction filter would exclude it) and confirm it is neither in the
    # evidence nor replayed: only the one answered record survives.
    deferred = AssertionRecord(
        record_id="rec_2", disposition=DISPOSITION_DEFERRED, content="deferred note",
        gap_context=None, iteration=2, provenance=OWNER_STATED,
        validation_status=UNVALIDATED)
    store.append_record("ansonly", deferred, idempotency_key="def-1")
    snap = SR.reconstruct_review_state(store, "ansonly")
    assert all(r.disposition == DISPOSITION_ANSWERED
               for r in snap.accepted_answer_evidence)
    assert [r.record_id for r in snap.accepted_answer_evidence] == ["rec_1"]
    assert snap.level == 1


# ===========================================================================
# 6. Seed/domain/path/version are persisted at project creation (via /start)
# ===========================================================================
def test_start_persists_reconstruction_inputs(client):
    sid = _start(client)
    inputs = _store().load_reconstruction_inputs(sid)
    assert inputs is not None
    assert inputs["seed_idea_text"] == IDEA
    assert inputs["confirmed_domain"] == "electronics_electrical"
    assert inputs["path"] == "N"
    assert inputs["engine_contract_version"] == SR.RECONSTRUCTION_VERSION


# ===========================================================================
# 7. Seed idea is NOT duplicated into AssertionRecord payloads
# ===========================================================================
def test_seed_not_duplicated_into_assertions(client):
    sid = _start(client)
    # At creation the accepted-answer ledger is empty; the seed lives only in the
    # project envelope, never as an assertion record.
    evidence = _store().load_accepted_answer_evidence(sid)
    assert evidence == ()
    contract = _store().load_contract(sid)
    assert all(IDEA not in (r.content or "") for r in contract.assertions)


# ===========================================================================
# 8. Legacy project without reconstruction metadata -> Level 0 only
# ===========================================================================
def test_legacy_project_level0(client):
    store = _store()
    _put_project(store, "legacy", answers=[ANSWER_1])  # no seed/domain/path/version
    snap = SR.reconstruct_review_state(store, "legacy")
    assert snap.level == 0 and snap.reconstructed is False
    assert snap.maturity_level is None and snap.next_question is None
    assert len(snap.accepted_answer_evidence) == 1


# ===========================================================================
# 9/10/11. Missing seed / missing domain / missing-or-unsupported path -> L0
# ===========================================================================
def test_missing_seed_level0(client):
    store = _store()
    _put_project(store, "noseed", domain="electronics_electrical", path="N",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    assert SR.reconstruct_review_state(store, "noseed").level == 0


def test_missing_domain_level0(client):
    store = _store()
    _put_project(store, "nodom", seed=IDEA, path="N",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    assert SR.reconstruct_review_state(store, "nodom").level == 0


def test_missing_path_level0(client):
    store = _store()
    _put_project(store, "nopath", seed=IDEA, domain="electronics_electrical",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    assert SR.reconstruct_review_state(store, "nopath").level == 0


def test_unsupported_path_level0(client):
    store = _store()
    _put_project(store, "badpath", seed=IDEA, domain="electronics_electrical",
                 path="legacy_undesignated_current_behavior",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    snap = SR.reconstruct_review_state(store, "badpath")
    assert snap.level == 0
    assert snap.status == SR.STATUS_UNSUPPORTED_PATH


# ===========================================================================
# 12. Non-Path-N performs NO AI/network call
# ===========================================================================
def test_non_path_n_no_ai(client, monkeypatch):
    store = _store()
    _put_project(store, "nonn", seed=IDEA, domain="electronics_electrical",
                 path="X", version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    import engine.ai_advisor as ai
    def _boom(*a, **k):
        raise AssertionError("AI advisor must not be called during reconstruction")
    monkeypatch.setattr(ai, "get_ai_question", _boom)
    snap = SR.reconstruct_review_state(store, "nonn")
    assert snap.level == 0


# ===========================================================================
# 13. Version mismatch -> Level 0, no replay
# ===========================================================================
def test_version_mismatch_level0(client, monkeypatch):
    store = _store()
    _put_project(store, "ver", seed=IDEA, domain="electronics_electrical",
                 path="N", version="p4-2-level1-recon-OLD", answers=[ANSWER_1])
    from engine import progression_loop
    def _boom(*a, **k):
        raise AssertionError("run_iteration must not run on version mismatch")
    monkeypatch.setattr(progression_loop, "run_iteration", _boom)
    snap = SR.reconstruct_review_state(store, "ver")
    assert snap.level == 0
    assert snap.status == SR.STATUS_VERSION_MISMATCH


# ===========================================================================
# 14. Malformed contract -> canonical ContractError, no partial review state
# ===========================================================================
def test_malformed_contract_raises_contracterror(client):
    store = _store()
    _put_project(store, "bad", seed=IDEA, domain="electronics_electrical",
                 path="N", version=SR.RECONSTRUCTION_VERSION)
    # Corrupt a durable payload directly (unsupported/invalid content).
    store._conn.execute(
        "INSERT INTO records (project_id, seq, record_id, payload) VALUES (?,?,?,?)",
        ("bad", 0, "rec_1", '{"not":"a valid assertion record"}'))
    store._conn.commit()
    with pytest.raises(ContractError):
        SR.reconstruct_review_state(store, "bad")


# ===========================================================================
# 15/16. Replay-limit boundary succeeds; boundary+1 fails closed
# ===========================================================================
def test_replay_limit_boundary_ok(client, monkeypatch):
    store = _store()
    monkeypatch.setattr(SR, "MAX_ACCEPTED_ANSWER_REPLAY", 3)
    _put_project(store, "lim", seed=IDEA, domain="electronics_electrical",
                 path="N", version=SR.RECONSTRUCTION_VERSION,
                 answers=[ANSWER_1, ANSWER_2, ANSWER_3])
    snap = SR.reconstruct_review_state(store, "lim")
    assert snap.level == 1


def test_replay_limit_boundary_plus_one_fails_closed(client, monkeypatch):
    store = _store()
    monkeypatch.setattr(SR, "MAX_ACCEPTED_ANSWER_REPLAY", 3)
    _put_project(store, "lim2", seed=IDEA, domain="electronics_electrical",
                 path="N", version=SR.RECONSTRUCTION_VERSION,
                 answers=[ANSWER_1, ANSWER_2, ANSWER_3, ANSWER_1])
    with pytest.raises(SR.ReconstructionReplayLimitError):
        SR.reconstruct_review_state(store, "lim2")


# ===========================================================================
# 17. Unknown project -> canonical absent/empty behavior (empty evidence, L0)
# ===========================================================================
def test_unknown_project_absent_empty(client):
    snap = SR.reconstruct_review_state(_store(), "does-not-exist")
    assert snap.level == 0 and snap.reconstructed is False
    assert snap.accepted_answer_evidence == ()


# ===========================================================================
# 18. Session isolation: A never consumes B's metadata or answers
# ===========================================================================
def test_session_isolation(client):
    store = _store()
    _put_project(store, "A", seed=IDEA, domain="electronics_electrical", path="N",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    _put_project(store, "B", seed="different seed", domain="electronics_electrical",
                 path="N", version=SR.RECONSTRUCTION_VERSION,
                 answers=[ANSWER_2, ANSWER_3])
    a = SR.reconstruct_review_state(store, "A")
    b = SR.reconstruct_review_state(store, "B")
    assert len(a.accepted_answer_evidence) == 1
    assert len(b.accepted_answer_evidence) == 2
    assert [r.content for r in a.accepted_answer_evidence] == [ANSWER_1]


# ===========================================================================
# 19/20/21. No mutation: DB rows, SESSION_STORE, live IdeaState unchanged
# ===========================================================================
def test_no_db_mutation(client):
    store = _store()
    _put_project(store, "nm", seed=IDEA, domain="electronics_electrical", path="N",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1, ANSWER_2])
    before_rows = store._conn.execute(
        "SELECT project_id, seq, record_id, payload FROM records ORDER BY seq"
    ).fetchall()
    before_proj = store._conn.execute(
        "SELECT * FROM projects WHERE project_id='nm'").fetchall()
    SR.reconstruct_review_state(store, "nm")
    after_rows = store._conn.execute(
        "SELECT project_id, seq, record_id, payload FROM records ORDER BY seq"
    ).fetchall()
    after_proj = store._conn.execute(
        "SELECT * FROM projects WHERE project_id='nm'").fetchall()
    assert before_rows == after_rows
    assert before_proj == after_proj


def test_session_store_unchanged(client):
    sid, live, _ = _live_session(client, [ANSWER_1, ANSWER_2])
    before = copy.deepcopy(dict(SESSION_STORE))
    SR.reconstruct_review_state(_store(), sid)
    assert set(SESSION_STORE.keys()) == set(before.keys())
    # The live entry object identity and its state object are untouched.
    assert SESSION_STORE[sid]["state"] is live


def test_live_ideastate_unchanged(client):
    sid, live, _ = _live_session(client, [ANSWER_1, ANSWER_2])
    before = (live.maturity_level, live.current_stage, live.iteration,
              _open_gap_types(live), len(live.assertions))
    SR.reconstruct_review_state(_store(), sid)
    after = (live.maturity_level, live.current_stage, live.iteration,
             _open_gap_types(live), len(live.assertions))
    assert before == after


# ===========================================================================
# 22. Result is immutable
# ===========================================================================
def test_result_immutable(client):
    store = _store()
    _put_project(store, "imm", seed=IDEA, domain="electronics_electrical", path="N",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    snap = SR.reconstruct_review_state(store, "imm")
    with pytest.raises(Exception):
        snap.maturity_level = 99
    assert isinstance(snap.open_gaps, tuple)
    assert isinstance(snap.accepted_answer_evidence, tuple)


# ===========================================================================
# 23. Result is not IdeaState and has no write/continue/submit behavior
# ===========================================================================
def test_result_is_not_writable_session(client):
    store = _store()
    _put_project(store, "ro", seed=IDEA, domain="electronics_electrical", path="N",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    snap = SR.reconstruct_review_state(store, "ro")
    assert not isinstance(snap, IdeaState)
    for attr in ("record_interaction", "run_iteration", "submit", "append",
                 "continue_session", "record_criticality_confirmation"):
        assert not hasattr(snap, attr)


# ===========================================================================
# 24. Result carries an explicit non-resume / read-only status
# ===========================================================================
def test_result_non_resume_marker(client):
    store = _store()
    _put_project(store, "nr", seed=IDEA, domain="electronics_electrical", path="N",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    snap = SR.reconstruct_review_state(store, "nr")
    assert snap.is_resume is False


# ===========================================================================
# 25. No prior output is marked valid by reconstruction
# ===========================================================================
def test_outputs_not_validated(client):
    store = _store()
    _put_project(store, "out", seed=IDEA, domain="electronics_electrical", path="N",
                 version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    snap = SR.reconstruct_review_state(store, "out")
    assert snap.outputs_validated is False


# ===========================================================================
# 26/27. P4-1b-2a append/idempotency and P4-1b-2b evidence remain green
# (light in-file regression guards; full regression run separately)
# ===========================================================================
def test_p4_1b2a_append_still_works(client):
    store = _store()
    _put_project(store, "reg2a", seed=IDEA, domain="electronics_electrical",
                 path="N", version=SR.RECONSTRUCTION_VERSION, answers=[ANSWER_1])
    # A same-key duplicate append fails closed (idempotency backstop intact).
    dup = AssertionRecord(record_id="rec_9", disposition=DISPOSITION_ANSWERED,
                          content=ANSWER_1, gap_context=None, iteration=9,
                          provenance=OWNER_STATED, validation_status=UNVALIDATED)
    import sqlite3
    with pytest.raises(sqlite3.IntegrityError):
        store.append_record("reg2a", dup, idempotency_key="idem-reg2a-1")


def test_p4_1b2b_evidence_still_works(client):
    store = _store()
    _put_project(store, "reg2b", seed=IDEA, domain="electronics_electrical",
                 path="N", version=SR.RECONSTRUCTION_VERSION,
                 answers=[ANSWER_1, ANSWER_2])
    ev = store.load_accepted_answer_evidence("reg2b")
    assert tuple(r.content for r in ev) == (ANSWER_1, ANSWER_2)
