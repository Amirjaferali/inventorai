"""P4-1b-2b — bounded read-only accepted-answer evidence reconstruction (RED/GREEN).

Behaviour-based tests for `SqliteRecordStore.load_accepted_answer_evidence(sid)`
(gate G-P4-1b-2B-IMPLEMENTATION-01, Option A). The API reconstructs ONLY the
durably persisted accepted-answer evidence for one project/session, read-only, in
the authoritative persisted order (store `seq`).

Contract under test:
  * consumes the existing canonical `load_contract(sid)` / `ProjectRecordContract`;
  * returns ONLY records whose disposition is `answered`;
  * preserves authoritative durable order from store `seq` (never sorts by rec_N);
  * preserves each `record_id` exactly as `rec_N`; tolerates NON-CONTIGUOUS rec_N
    (only accepted answers are persisted, so gaps are expected and valid);
  * returns an immutable, externally non-mutating sequence (a tuple);
  * performs NO write / append / repair / rehydration / progression, and never
    reconstructs a resumable session;
  * preserves project/session isolation and fails closed on corrupt durable
    content (never converts corruption into a valid empty history).

These tests inspect durable store contents and the returned evidence directly —
never HTTP status, counts alone, or the web layer. Each durable database lives
only under the pytest-managed `tmp_path`. No push/PR/merge in this gate.
"""
import sqlite3

import pytest

from engine.record_store import SqliteRecordStore, ProjectNotFound
from engine.record_contract import ProjectRecordContract, ContractError
from engine.idea_state import IdeaState, DISPOSITION_ANSWERED, DISPOSITION_DEFERRED


# --- helpers -----------------------------------------------------------------
def _store(tmp_path, name="p4_1b2b.sqlite"):
    return SqliteRecordStore(str(tmp_path / name))


def _new_project(store, pid, idea="idea-1"):
    store.create_project(ProjectRecordContract(idea_id=idea, assertions=[]),
                         project_id=pid)
    return pid


def _mk_records():
    """Build a realistic in-memory ledger: answered rec_1, an in-memory-only
    non-answer rec_2 (deferred), answered rec_3 — mirroring production, where
    only answered interactions are durably appended (so durable rec_N is
    non-contiguous). Returns the three records."""
    st = IdeaState(idea_id="idea-1")
    r1 = st.record_interaction(action=DISPOSITION_ANSWERED, content="first answer",
                               gap_context="G1", iteration=1)
    r2 = st.record_interaction(action=DISPOSITION_DEFERRED, content="",
                               gap_context="G2", iteration=2)
    r3 = st.record_interaction(action=DISPOSITION_ANSWERED, content="third answer",
                               gap_context="G3", iteration=3)
    return r1, r2, r3


# --- 1. multiple accepted answers load in store seq order --------------------
def test_red_1_ordered_by_seq(tmp_path):
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        r1, _, r3 = _mk_records()
        store.append_record(pid, r1, idempotency_key="k1")
        store.append_record(pid, r3, idempotency_key="k3")
        ev = store.load_accepted_answer_evidence(pid)
        assert [r.record_id for r in ev] == ["rec_1", "rec_3"]
        assert [r.content for r in ev] == ["first answer", "third answer"]
    finally:
        store.close()


# --- 2. non-contiguous record_id (rec_1, rec_3) accepted, kept in seq order ---
def test_red_2_non_contiguous_recN_kept_in_seq_order(tmp_path):
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        r1, _, r3 = _mk_records()
        # append rec_3 first in a fresh project would not occur in production;
        # here rec_1 then rec_3 => seq 0,1 with a gap at rec_2 (never persisted).
        store.append_record(pid, r1, idempotency_key="k1")
        store.append_record(pid, r3, idempotency_key="k3")
        ev = store.load_accepted_answer_evidence(pid)
        ids = [r.record_id for r in ev]
        assert ids == ["rec_1", "rec_3"], "non-contiguous rec_N must be preserved in seq order"
        assert "rec_2" not in ids, "the in-memory-only non-answer record was never persisted"
    finally:
        store.close()


# --- 3. non-answer dispositions are excluded from the evidence ----------------
def test_red_3_excludes_non_answer_dispositions(tmp_path):
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        r1, r2_deferred, r3 = _mk_records()
        # A store CAN legally contain a non-answer record (append_record accepts
        # any AssertionRecord); the evidence API must exclude it by disposition.
        store.append_record(pid, r1, idempotency_key="k1")
        store.append_record(pid, r2_deferred)            # deferred, NULL idem key
        store.append_record(pid, r3, idempotency_key="k3")
        ev = store.load_accepted_answer_evidence(pid)
        assert all(r.disposition == DISPOSITION_ANSWERED for r in ev)
        assert [r.record_id for r in ev] == ["rec_1", "rec_3"]
    finally:
        store.close()


# --- 4. session isolation: sid A never returns sid B evidence ----------------
def test_red_4_session_isolation(tmp_path):
    store = _store(tmp_path)
    try:
        pa = _new_project(store, "pA", idea="idea-A")
        pb = _new_project(store, "pB", idea="idea-B")
        ra, _, _ = _mk_records()
        store.append_record(pa, ra, idempotency_key="ka")
        stb = IdeaState(idea_id="idea-B")
        rb = stb.record_interaction(action=DISPOSITION_ANSWERED, content="B-only answer",
                                    gap_context="GB", iteration=1)
        store.append_record(pb, rb, idempotency_key="kb")
        ev_a = store.load_accepted_answer_evidence(pa)
        ev_b = store.load_accepted_answer_evidence(pb)
        assert [r.content for r in ev_a] == ["first answer"]
        assert [r.content for r in ev_b] == ["B-only answer"]
        assert "B-only answer" not in [r.content for r in ev_a]
    finally:
        store.close()


# --- 5. unknown/absent sid: defined empty result, no mutation, no leak --------
def test_red_5_unknown_sid_returns_empty(tmp_path):
    store = _store(tmp_path)
    try:
        ev = store.load_accepted_answer_evidence("does-not-exist")
        assert ev == ()
        # non-disclosing: an existing empty project returns the SAME empty result
        _new_project(store, "empty")
        assert store.load_accepted_answer_evidence("empty") == ()
    finally:
        store.close()


# --- 6. empty valid project returns an empty immutable sequence ---------------
def test_red_6_empty_project_empty_sequence(tmp_path):
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        ev = store.load_accepted_answer_evidence(pid)
        assert ev == ()
        assert isinstance(ev, tuple)
    finally:
        store.close()


# --- 7. malformed durable payload fails closed (no partial evidence) ----------
def test_red_7_malformed_payload_fails_closed(tmp_path):
    dbp = str(tmp_path / "p4_1b2b.sqlite")
    store = SqliteRecordStore(dbp)
    try:
        pid = _new_project(store, "p1")
        r1, _, r3 = _mk_records()
        store.append_record(pid, r1, idempotency_key="k1")
        store.append_record(pid, r3, idempotency_key="k3")
    finally:
        store.close()
    # Corrupt one record's payload directly (drops required contract fields).
    conn = sqlite3.connect(dbp)
    with conn:
        conn.execute("UPDATE records SET payload=? WHERE project_id=? AND record_id=?",
                     ('{"unexpected": true}', "p1", "rec_1"))
    conn.close()
    store2 = SqliteRecordStore(dbp)
    try:
        with pytest.raises(ContractError):
            store2.load_accepted_answer_evidence("p1")
    finally:
        store2.close()


# --- 8. unsupported contract version fails closed -----------------------------
def test_red_8_unsupported_version_fails_closed(tmp_path):
    dbp = str(tmp_path / "p4_1b2b.sqlite")
    store = SqliteRecordStore(dbp)
    try:
        pid = _new_project(store, "p1")
        r1, _, _ = _mk_records()
        store.append_record(pid, r1, idempotency_key="k1")
    finally:
        store.close()
    conn = sqlite3.connect(dbp)
    with conn:
        conn.execute("UPDATE projects SET contract_version=? WHERE project_id=?",
                     ("p4-0-record-contract-v999", "p1"))
    conn.close()
    store2 = SqliteRecordStore(dbp)
    try:
        with pytest.raises(ContractError):
            store2.load_accepted_answer_evidence("p1")
    finally:
        store2.close()


# --- 9. structurally valid partial history loads (no invented records) --------
def test_red_9_partial_history_no_invention(tmp_path):
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        r1, _, _ = _mk_records()
        store.append_record(pid, r1, idempotency_key="k1")   # only one answer so far
        ev = store.load_accepted_answer_evidence(pid)
        assert [r.record_id for r in ev] == ["rec_1"]
        assert len(ev) == 1, "must not invent missing later interactions"
    finally:
        store.close()


# --- 10. legacy records with NULL idempotency_key load ------------------------
def test_red_10_legacy_null_idempotency_key_loads(tmp_path):
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        r1, _, _ = _mk_records()
        store.append_record(pid, r1)   # no idempotency_key -> NULL (legacy shape)
        ev = store.load_accepted_answer_evidence(pid)
        assert [r.record_id for r in ev] == ["rec_1"]
        assert ev[0].content == "first answer"
    finally:
        store.close()


# --- 11. reading does not mutate durable rows / order -------------------------
def test_red_11_read_does_not_mutate(tmp_path):
    dbp = str(tmp_path / "p4_1b2b.sqlite")
    store = SqliteRecordStore(dbp)
    try:
        pid = _new_project(store, "p1")
        r1, r2, r3 = _mk_records()
        store.append_record(pid, r1, idempotency_key="k1")
        store.append_record(pid, r2)
        store.append_record(pid, r3, idempotency_key="k3")
        before = store._conn.execute(
            "SELECT record_id, seq, payload, idempotency_key FROM records "
            "WHERE project_id='p1' ORDER BY seq").fetchall()
        store.load_accepted_answer_evidence(pid)
        store.load_accepted_answer_evidence(pid)   # twice — still no mutation
        after = store._conn.execute(
            "SELECT record_id, seq, payload, idempotency_key FROM records "
            "WHERE project_id='p1' ORDER BY seq").fetchall()
        assert before == after, "read-only evidence load must not mutate durable rows/order"
        # It must not touch the runtime SESSION_STORE either (store-level API).
        import web.app as webapp
        assert "p1" not in webapp.SESSION_STORE
    finally:
        store.close()


# --- 12. record_id remains rec_N (not replaced by idempotency identity) -------
def test_red_12_record_id_stays_recN(tmp_path):
    import re
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        r1, _, r3 = _mk_records()
        store.append_record(pid, r1, idempotency_key="deadbeef-not-a-record-id")
        store.append_record(pid, r3, idempotency_key="cafef00d-not-a-record-id")
        ev = store.load_accepted_answer_evidence(pid)
        for r in ev:
            assert re.fullmatch(r"rec_\d+", r.record_id), r.record_id
        assert [r.record_id for r in ev] == ["rec_1", "rec_3"]
    finally:
        store.close()


# --- 13. result is immutable / externally non-mutating -----------------------
def test_red_13_immutable_result(tmp_path):
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        r1, _, _ = _mk_records()
        store.append_record(pid, r1, idempotency_key="k1")
        ev = store.load_accepted_answer_evidence(pid)
        assert isinstance(ev, tuple)
        assert not hasattr(ev, "append")
        with pytest.raises(TypeError):
            ev[0] = None            # tuples reject item assignment
    finally:
        store.close()


# --- 14. result carries no resumable-session fields --------------------------
def test_red_14_no_resumable_session_fields(tmp_path):
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        r1, _, _ = _mk_records()
        store.append_record(pid, r1, idempotency_key="k1")
        ev = store.load_accepted_answer_evidence(pid)
        assert not isinstance(ev, IdeaState)
        for r in ev:
            # evidence entries expose accepted-answer fields only
            assert hasattr(r, "record_id") and hasattr(r, "content")
            assert hasattr(r, "gap_context") and hasattr(r, "iteration")
            assert hasattr(r, "provenance") and hasattr(r, "validation_status")
            for forbidden in ("gaps", "maturity_level", "current_stage", "path",
                              "domain", "last_result", "transcript"):
                assert not hasattr(r, forbidden), forbidden
    finally:
        store.close()


# --- 15. existing P4-1b-2a append + idempotency behaviour still holds ---------
def test_red_15_p4_1b2a_append_idempotency_preserved(tmp_path):
    store = _store(tmp_path)
    try:
        pid = _new_project(store, "p1")
        r1, _, _ = _mk_records()
        store.append_record(pid, r1, idempotency_key="k-dup")
        # the durable idempotency backstop still rejects a duplicate key
        st2 = IdeaState(idea_id="idea-1")
        r_other = st2.record_interaction(action=DISPOSITION_ANSWERED, content="other",
                                         iteration=9)
        with pytest.raises(sqlite3.IntegrityError):
            store.append_record(pid, r_other, idempotency_key="k-dup")
        # and the new read reflects exactly the one durably accepted answer
        ev = store.load_accepted_answer_evidence(pid)
        assert [r.record_id for r in ev] == ["rec_1"]
    finally:
        store.close()
