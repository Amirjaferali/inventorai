"""P4-1a — Durable-Store Proof (RED/GREEN).

Behavior-based tests for a datastore-neutral durable record store with a Python
standard-library SQLite reference adapter (`engine.record_store`). Governed by
the merged P4-1a Increment Contract in
`docs/governance/ACTIVE_INCREMENT_CONTRACT.md` (G-P4-1A-DOC-01, PR #355).

Durability is proved through ACTUAL SQLite persistence and a real
close-and-reopen (no module dicts, process caches, reused in-memory objects,
mocks, or file-existence-only assertions). The store reuses the P4-0 record
contract (`engine.record_contract`) as the canonical serialization/validation
boundary; readiness is never persisted or accepted as authoritative. Scope:
durable-store proof only — no runtime/web integration (P4-1b), no replay (P4-2),
no accounts (Phase 5). Provider-free and network-free; SQLite files live only in
pytest tmp_path.
"""
import uuid

import pytest

from engine.idea_state import (
    IdeaState,
    AssertionRecord,
    OWNER_STATED,
    LEGACY_UNSPECIFIED,
    UNVALIDATED,
    INDEPENDENTLY_VERIFIED,
    REASONED,
)
from engine.derived_readiness import derive_readiness
from engine.record_contract import (
    ProjectRecordContract,
    CONTRACT_VERSION,
    UnknownVersionError,
    InvalidReferenceError,
)

# Intended P4-1a store API — absent until GREEN. RED fails because this durable
# behavior does not exist (each test asserts real persistence/close-reopen/
# rollback/isolation behavior and still fails against an empty or
# NotImplementedError stub).
from engine.record_store import SqliteRecordStore, ProjectNotFound


# --- Non-trivial fixture (idea_state + record contract; no store dependency) --
def sample_contract():
    """5 append-only records, two gap contexts, two provenance values, two
    validation values, one supersession, one contradiction, stable ids."""
    st = IdeaState(idea_id="idea-p4-1a-001")
    r1 = st.record_interaction("answered", content="problem stated",
                               gap_context="problem", iteration=1)      # OWNER_STATED
    r1.validation_status = INDEPENDENTLY_VERIFIED
    st.record_interaction("deferred", content="",
                          gap_context="mechanism", iteration=2)          # LEGACY_UNSPECIFIED
    r3 = st.record_interaction("answered", content="old mechanism",
                               gap_context="mechanism", iteration=3)
    r3.validation_status = INDEPENDENTLY_VERIFIED
    r4 = st.record_interaction("answered", content="new mechanism",
                               gap_context="mechanism", iteration=4)
    r4.validation_status = INDEPENDENTLY_VERIFIED
    st.mark_supersession(r3.record_id, r4.record_id)
    r5 = st.record_interaction("answered", content="conflicting view",
                               gap_context="problem", iteration=5)
    r5.validation_status = INDEPENDENTLY_VERIFIED
    st.mark_contradiction(r1.record_id, r5.record_id)
    return ProjectRecordContract.from_state(st), st


def _db(tmp_path):
    return str(tmp_path / "p4_1a.sqlite")


_FIELDS = ("record_id", "disposition", "content", "gap_context", "iteration",
           "provenance", "validation_status", "quality", "pending",
           "responsibility", "resolves_gap", "contradicts", "supersedes",
           "superseded_by")


def _assert_records_equal(a_list, b_list):
    assert len(a_list) == len(b_list)
    for a, b in zip(a_list, b_list):
        for f in _FIELDS:
            assert getattr(a, f) == getattr(b, f), f


# --- RED-1: durable create + load round-trip --------------------------------
def test_red1_durable_create_and_load_roundtrip(tmp_path):
    contract, _ = sample_contract()
    store = SqliteRecordStore(_db(tmp_path))
    pid = store.create_project(contract)
    loaded = store.load_contract(pid)
    assert loaded.idea_id == contract.idea_id
    assert loaded.contract_version == CONTRACT_VERSION
    _assert_records_equal(loaded.assertions, contract.assertions)
    store.close()


# --- RED-2: MANDATORY real close-and-reopen survival ------------------------
def test_red2_close_reopen_survival(tmp_path):
    path = _db(tmp_path)
    contract, _ = sample_contract()
    store = SqliteRecordStore(path)
    pid = store.create_project(contract)
    store.close()
    del store, contract            # discard the original in-memory objects
    store2 = SqliteRecordStore(path)   # reopen the SAME sqlite database
    loaded = store2.load_contract(pid)
    fresh, _ = sample_contract()
    assert loaded.idea_id == "idea-p4-1a-001"
    _assert_records_equal(loaded.assertions, fresh.assertions)
    by_id = {r.record_id: r for r in loaded.assertions}
    assert by_id["rec_3"].superseded_by == "rec_4"
    assert "rec_3" in by_id["rec_4"].supersedes
    assert "rec_5" in by_id["rec_1"].contradicts
    store2.close()


# --- RED-3: atomic rollback, no partial write -------------------------------
def test_red3_atomic_rollback_no_partial(tmp_path):
    store = SqliteRecordStore(_db(tmp_path))
    before = set(store.project_ids())
    # A contract with a DUPLICATE record_id -> the atomic write must fail and
    # roll back entirely (SQLite integrity), leaving no partial project.
    dup = ProjectRecordContract(idea_id="idea-dup", assertions=[
        AssertionRecord(record_id="rec_1", disposition="answered",
                        content="a", gap_context="g", iteration=1),
        AssertionRecord(record_id="rec_1", disposition="answered",
                        content="b", gap_context="g", iteration=2),
    ])
    with pytest.raises(Exception):
        store.create_project(dup)
    assert set(store.project_ids()) == before      # nothing persisted
    store.close()


# --- RED-4: append-only history preserved after reload ----------------------
def test_red4_append_only_history_preserved(tmp_path):
    path = _db(tmp_path)
    contract, _ = sample_contract()
    store = SqliteRecordStore(path)
    pid = store.create_project(contract)
    store.close()
    store2 = SqliteRecordStore(path)
    loaded = store2.load_contract(pid)
    assert [r.record_id for r in loaded.assertions] == \
           ["rec_1", "rec_2", "rec_3", "rec_4", "rec_5"]
    assert any(r.record_id == "rec_3" and r.superseded_by == "rec_4"
               for r in loaded.assertions)   # superseded record retained
    store2.close()


# --- RED-5: cross-project isolation -----------------------------------------
def test_red5_cross_project_isolation(tmp_path):
    store = SqliteRecordStore(_db(tmp_path))
    c_a, _ = sample_contract()
    st_b = IdeaState(idea_id="idea-B")
    st_b.record_interaction("answered", content="B-only", gap_context="problem", iteration=1)
    c_b = ProjectRecordContract.from_state(st_b)
    pid_a = store.create_project(c_a)
    pid_b = store.create_project(c_b)
    assert pid_a != pid_b
    a = store.load_contract(pid_a)
    b = store.load_contract(pid_b)
    assert len(a.assertions) == 5 and len(b.assertions) == 1
    assert {r.content for r in b.assertions} == {"B-only"}
    assert all(r.content != "B-only" for r in a.assertions)
    with pytest.raises(ProjectNotFound):
        store.load_contract("no-such-project")
    store.close()


# --- RED-6: stable ids survive durable reload -------------------------------
def test_red6_stable_ids_survive_reload(tmp_path):
    path = _db(tmp_path)
    contract, _ = sample_contract()
    orig_ids = [r.record_id for r in contract.assertions]
    store = SqliteRecordStore(path); pid = store.create_project(contract); store.close()
    loaded = SqliteRecordStore(path).load_contract(pid)
    assert [r.record_id for r in loaded.assertions] == orig_ids   # not regenerated


# --- RED-7: provenance + validation preserved verbatim ----------------------
def test_red7_provenance_and_validation_preserved(tmp_path):
    path = _db(tmp_path)
    contract, _ = sample_contract()
    provs = {r.record_id: r.provenance for r in contract.assertions}
    vals = {r.record_id: r.validation_status for r in contract.assertions}
    assert OWNER_STATED in provs.values() and LEGACY_UNSPECIFIED in provs.values()
    assert INDEPENDENTLY_VERIFIED in vals.values() and UNVALIDATED in vals.values()
    store = SqliteRecordStore(path); pid = store.create_project(contract); store.close()
    loaded = SqliteRecordStore(path).load_contract(pid)
    for r in loaded.assertions:
        assert r.provenance == provs[r.record_id]      # verbatim, no mapping/AI values
        assert r.validation_status == vals[r.record_id]


# --- RED-8: unknown contract version rejected through store load ------------
def test_red8_unknown_version_rejected_through_load(tmp_path):
    path = _db(tmp_path)
    contract, _ = sample_contract()
    bad = ProjectRecordContract(idea_id=contract.idea_id,
                                assertions=contract.assertions,
                                contract_version="p4-0-record-contract-v999")
    store = SqliteRecordStore(path); pid = store.create_project(bad); store.close()
    store2 = SqliteRecordStore(path)
    with pytest.raises(UnknownVersionError):
        store2.load_contract(pid)
    store2.close()


# --- RED-9: malformed reference rejected through store load ------------------
def test_red9_malformed_reference_rejected_through_load(tmp_path):
    path = _db(tmp_path)
    contract, _ = sample_contract()
    contract.assertions[0].superseded_by = "rec_missing"   # dangling reference
    store = SqliteRecordStore(path); pid = store.create_project(contract); store.close()
    store2 = SqliteRecordStore(path)
    with pytest.raises(InvalidReferenceError):
        store2.load_contract(pid)
    store2.close()


# --- durability-safe UUID identifiers for newly created durable records -----
def test_new_durable_record_id_is_uuid_safe(tmp_path):
    store = SqliteRecordStore(_db(tmp_path))
    ids = {store.new_record_id() for _ in range(1000)}
    assert len(ids) == 1000                       # collision-safe
    for rid in list(ids)[:20]:
        uuid.UUID(rid.replace("rec-", ""))        # valid uuid payload
        assert not rid.startswith("rec_")         # not the P4-0 sequence form
    store.close()


# --- no cached readiness persisted; fresh derivation after reload -----------
def test_no_readiness_persisted_fresh_derivation(tmp_path):
    path = _db(tmp_path)
    contract, st = sample_contract()
    store = SqliteRecordStore(path); pid = store.create_project(contract); store.close()
    loaded = SqliteRecordStore(path).load_contract(pid)
    # readiness re-derived from restored records, never restored as a value
    orig = derive_readiness(st)
    fresh = derive_readiness(loaded.to_state())
    assert fresh.overall_verified() == orig.overall_verified()
    for ctx in ("problem", "mechanism"):
        assert fresh.is_verified(ctx) == orig.is_verified(ctx)
    # the persisted contract dict carries no readiness fields
    dumped = loaded.to_dict()
    assert "readiness" not in dumped and "overall_verified" not in str(dumped)
