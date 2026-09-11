"""T2-A Quantified Requirements Slice 1 — engine + durable-store proof.

File: tests/test_t2a_requirement_quantity_engine_store.py
Purpose: behaviour tests for the frozen Slice-1 data contract
(`engine/requirement_quantity.py`: nine-field `RequirementQuantity`, closed
`quantity_kind` vocabulary, bounded `value_text` policy, fail-closed history
validation, per-anchor chain derivation with replaced / withdrawn semantics,
the presentation-row builder), the additive `IdeaState` carrier, and the
additive `requirement_quantities` durable history in `engine/record_store.py`
(migration on a fresh AND an existing populated pre-T2A database, INSERT-only
append with history validation INSIDE the write transaction, the per-project
cap at 199/200/201, one-active-chain / stale-head enforcement, composite
foreign keys, unique event key, project isolation, fail-closed load,
backup/restore parity). The canonical deliverable assembler stays frozen.

Real on-disk SQLite only (pytest tmp_path); the real stores; no mocks of the
seams under test. Fail-closed assertions are never weakened.
"""
import json
import os
import sqlite3
from dataclasses import FrozenInstanceError

import pytest

from engine import backup_service
from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import (
    IdeaState, DISPOSITION_ANSWERED, DISPOSITION_UNKNOWN,
)
from engine.record_contract import ProjectRecordContract
from engine.record_store import (
    SqliteRecordStore, RecordStore, StoreError, ProjectNotFound,
    QuantityChainConflict, QuantityCapExceeded,
)
from engine.requirement_quantity import (
    MAX_REQUIREMENT_QUANTITIES_PER_PROJECT, MAX_VALUE_TEXT_CHARS,
    QUANTITY_KINDS, REQUIREMENT_QUANTITIES_META_KEY, QuantityHistoryError,
    QuantityValueError, RequirementQuantity, active_quantities,
    eligible_anchors, is_stored_value_text, normalize_value_text,
    quantity_chains, requirement_quantities_meta, superseded_ids,
    validate_quantity_history, validate_quantity_kind,
)

PROBLEM = ("The problem is that cyclists have no reliable brake light because "
           "the microcontroller must switch the LED when the sensor voltage "
           "changes suddenly.")
MECHANISM = ("The mechanism works because the accelerometer outputs a voltage "
             "proportional to deceleration and the microcontroller drives the "
             "LED through a transistor.")
KIND = QUANTITY_KINDS[0]
KIND2 = QUANTITY_KINDS[1]


def _qid(n):
    return "qty-" + ("%032x" % n)


def _ek(n):
    return "%032x" % (n + 1000)


def _row(n, anchor="rec_1", kind=KIND, text="5 V", supersedes=None, seq=None,
         project_id="P1", requirement_id=None, event_key=None):
    return {"project_id": project_id, "quantity_seq": n if seq is None else seq,
            "quantity_id": _qid(n), "anchor_record_id": anchor,
            "requirement_id": requirement_id or ("req:assertion:" + anchor),
            "quantity_kind": kind, "value_text": text,
            "supersedes_quantity_id": supersedes, "event_key": event_key or _ek(n)}


def _quantity(store, project_id, anchor="rec_1", kind=KIND, text="5 V",
              supersedes=None, event_key=None, requirement_id=None):
    import uuid
    return RequirementQuantity(
        project_id=project_id, quantity_seq=-1, quantity_id=store.new_quantity_id(),
        anchor_record_id=anchor, requirement_id=requirement_id or ("req:assertion:" + anchor),
        quantity_kind=kind, value_text=text, supersedes_quantity_id=supersedes,
        event_key=event_key or uuid.uuid4().hex)


@pytest.fixture
def store(tmp_path):
    s = SqliteRecordStore(str(tmp_path / "t2a.sqlite"))
    try:
        yield s
    finally:
        s.close()


def _project(store, pid, answers=(PROBLEM,)):
    state = IdeaState(idea_id="idea-" + pid)
    for text in answers:
        state.record_interaction(DISPOSITION_ANSWERED, text,
                                 gap_context="MECHANISM_COMPLETENESS", iteration=1)
    store.create_project(ProjectRecordContract.from_state(state), project_id=pid)
    return state


# ==========================================================================
# 1. Data contract, kind vocabulary, value_text policy
# ==========================================================================
def test_frozen_contract_has_exactly_the_nine_fields_and_is_immutable():
    fields = tuple(RequirementQuantity.__dataclass_fields__)
    assert fields == ("project_id", "quantity_seq", "quantity_id", "anchor_record_id",
                      "requirement_id", "quantity_kind", "value_text",
                      "supersedes_quantity_id", "event_key")
    q = RequirementQuantity("P1", 0, _qid(1), "rec_1", "req:assertion:rec_1", KIND,
                            "5 V", None, _ek(1))
    with pytest.raises(FrozenInstanceError):
        q.value_text = "6 V"


def test_kind_vocabulary_is_closed_and_ascii():
    assert len(set(QUANTITY_KINDS)) == len(QUANTITY_KINDS) >= 2
    for kind in QUANTITY_KINDS:
        assert validate_quantity_kind(kind) == kind
        assert kind.isascii() and kind.replace("_", "").isalnum()
    for bad in ("", None, "TARGET", "about", KIND + " ", "unit", 5):
        with pytest.raises(QuantityValueError):
            validate_quantity_kind(bad)


@pytest.mark.parametrize("raw,expected", [
    ("5 V", "5 V"), ("  12.5   V ", "12.5 V"), ("0.5 mm ± 0.1", "0.5 mm ± 0.1"),
    ("3\tto\t5 A", "3 to 5 A"), ("٢٥٠ نيوتن", "٢٥٠ نيوتن"), ("x" * MAX_VALUE_TEXT_CHARS,
                                                             "x" * MAX_VALUE_TEXT_CHARS),
])
def test_value_text_is_normalized_never_interpreted_and_idempotent(raw, expected):
    assert normalize_value_text(raw) == expected
    assert normalize_value_text(expected) == expected
    assert is_stored_value_text(expected)


@pytest.mark.parametrize("raw", [
    "", "   ", "\t", "x" * (MAX_VALUE_TEXT_CHARS + 1), "5\nV", "5\x00V", "5\x7fV",
    None, 5, "a b",
])
def test_value_text_policy_rejects_empty_long_and_control_input(raw):
    with pytest.raises(QuantityValueError):
        normalize_value_text(raw)
    assert not is_stored_value_text(raw)


def test_value_text_error_never_carries_the_text():
    with pytest.raises(QuantityValueError) as info:
        normalize_value_text("secret-value-123\n")
    assert "secret-value-123" not in str(info.value)


# ==========================================================================
# 2. History validation — zero rows valid; every corruption fails closed
# ==========================================================================
def test_zero_rows_are_a_valid_empty_history():
    assert validate_quantity_history([]) == ()
    assert validate_quantity_history(iter(()), "P1") == ()
    assert active_quantities(()) == {} and superseded_ids(()) == set()


def test_valid_chain_derives_active_and_superseded_rows():
    rows = [_row(1), _row(2, text="6 V", supersedes=_qid(1)),
            _row(3, anchor="rec_2", kind=KIND2, text="0.5 mm"),
            _row(4, text="7 V", supersedes=_qid(2))]
    history = validate_quantity_history(rows, "P1")
    assert [q.quantity_id for q in history] == [_qid(1), _qid(2), _qid(3), _qid(4)]
    assert superseded_ids(history) == {_qid(1), _qid(2)}
    active = active_quantities(history)
    assert set(active) == {"rec_1", "rec_2"}
    assert active["rec_1"].value_text == "7 V" and active["rec_2"].quantity_kind == KIND2
    assert rows[0] == _row(1)                        # input untouched


@pytest.mark.parametrize("label,rows,pid", [
    ("other project", [_row(1, project_id="P2")], "P1"),
    ("missing field", [{"quantity_id": _qid(1)}], None),
    ("non-mapping", ["nope"], None),
    ("seq not ascending", [_row(1, seq=5), _row(2, seq=5, anchor="rec_2")], None),
    ("seq negative", [_row(1, seq=-1)], None),
    ("seq bool", [_row(1, seq=True)], None),
    ("malformed id", [_row(1) | {"quantity_id": "qty-short"}], None),
    ("duplicate id", [_row(1), _row(2, anchor="rec_2") | {"quantity_id": _qid(1)}], None),
    ("malformed anchor", [_row(1, anchor="rec_0")], None),
    ("malformed anchor text", [_row(1, anchor="rec-abc")], None),
    ("empty requirement id", [_row(1, requirement_id="  ")], None),
    ("unknown kind", [_row(1, kind="about")], None),
    ("value not normalized", [_row(1, text=" 5 V")], None),
    ("value empty", [_row(1, text="")], None),
    ("value control", [_row(1, text="5\nV")], None),
    ("malformed event key", [_row(1, event_key="zz")], None),
    ("duplicate event key", [_row(1), _row(2, anchor="rec_2", event_key=_ek(1))], None),
    ("unknown supersedes", [_row(1, supersedes=_qid(9))], None),
    ("later supersedes", [_row(1, supersedes=_qid(2)), _row(2)], None),
    ("self supersedes", [_row(1, supersedes=_qid(1))], None),
    ("cross-anchor supersedes", [_row(1), _row(2, anchor="rec_2", supersedes=_qid(1))], None),
    ("requirement id changes", [_row(1), _row(2, supersedes=_qid(1), requirement_id="req:x")], None),
    ("double supersession", [_row(1), _row(2, supersedes=_qid(1)), _row(3, supersedes=_qid(1))], None),
    ("two active per anchor", [_row(1), _row(2, text="6 V")], None),
    ("over cap", [_row(i, anchor="rec_%d" % i) for i in range(1, MAX_REQUIREMENT_QUANTITIES_PER_PROJECT + 2)], None),
])
def test_every_structural_corruption_raises_with_nothing_returned(label, rows, pid):
    with pytest.raises(QuantityHistoryError):
        validate_quantity_history(rows, pid)


def test_corruption_message_names_structure_only_never_content():
    with pytest.raises(QuantityHistoryError) as info:
        validate_quantity_history([_row(1, text=" 77 secret", anchor="rec_77")])
    text = str(info.value)
    assert "secret" not in text and "rec_77" not in text and _qid(1) not in text


# ==========================================================================
# 3. Eligible anchors, chain derivation, presentation rows
# ==========================================================================
def _state_with_answers():
    state = IdeaState(idea_id="idea-x")
    state.record_interaction(DISPOSITION_ANSWERED, PROBLEM,
                             gap_context="MECHANISM_COMPLETENESS", iteration=1)
    state.record_interaction(DISPOSITION_ANSWERED, MECHANISM,
                             gap_context="MECHANISM_COMPLETENESS", iteration=2)
    state.record_interaction(DISPOSITION_UNKNOWN, "",
                             gap_context="PHYSICAL_FEASIBILITY", iteration=2)
    state.record_interaction(DISPOSITION_ANSWERED, "   ",
                             gap_context="BOUNDARY_AMBIGUITY", iteration=3)
    return state


def test_eligible_anchors_are_active_non_empty_answered_landscape_records():
    state = _state_with_answers()
    anchors = eligible_anchors(state)
    assert [rec.record_id for _req, rec in anchors] == ["rec_1", "rec_2"]
    assert [req.requirement_id for req, _rec in anchors] == [
        "req:assertion:rec_1", "req:assertion:rec_2"]
    state.record_interaction(DISPOSITION_ANSWERED, "corrected mechanism text",
                             gap_context="MECHANISM_COMPLETENESS", iteration=4,
                             supersedes=["rec_2"])
    assert [rec.record_id for _req, rec in eligible_anchors(state)] == ["rec_1", "rec_5"]
    state.mark_contradiction("rec_1", "rec_5")
    assert eligible_anchors(state) == ()


def test_chains_expose_active_replaced_and_withdrawn_anchor_deterministically():
    state = _state_with_answers()
    state.requirement_quantities = list(validate_quantity_history([
        _row(1, anchor="rec_2", text="3 A"),
        _row(2, anchor="rec_1", text="5 V"),
        _row(3, anchor="rec_1", text="6 V", supersedes=_qid(2)),
        _row(4, anchor="rec_9", text="1 kg"),          # anchor never existed
    ]))
    chains = quantity_chains(state)
    assert [(c.anchor_record_id, c.active.value_text, [r.value_text for r in c.replaced],
             c.anchor_active) for c in chains] == [
        ("rec_1", "6 V", ["5 V"], True), ("rec_2", "3 A", [], True), ("rec_9", "1 kg", [], False)]
    # withdrawing rec_2 makes its chain a withdrawn-anchor chain, rows retained
    state.record_interaction(DISPOSITION_ANSWERED, "corrected", iteration=4,
                             gap_context="MECHANISM_COMPLETENESS", supersedes=["rec_2"])
    chains = quantity_chains(state)
    assert [(c.anchor_record_id, c.anchor_active) for c in chains] == [
        ("rec_1", True), ("rec_2", False), ("rec_9", False)]
    assert quantity_chains(state) == chains          # deterministic
    assert quantity_chains(IdeaState(idea_id="empty")) == ()
    assert len(state.requirement_quantities) == 4    # nothing deleted


def test_meta_is_none_at_zero_rows_and_carries_replaced_and_withdrawn_otherwise():
    state = _state_with_answers()
    assert requirement_quantities_meta(state) is None
    state.requirement_quantities = list(validate_quantity_history([
        _row(1, anchor="rec_1", text="5 V"),
        _row(2, anchor="rec_1", kind=KIND2, text="6 V", supersedes=_qid(1)),
        _row(3, anchor="rec_2", text="3 A"),
    ]))
    state.record_interaction(DISPOSITION_ANSWERED, "corrected", iteration=4,
                             gap_context="MECHANISM_COMPLETENESS", supersedes=["rec_2"])
    meta = requirement_quantities_meta(state)
    assert meta["total"] == 2 and meta["active_total"] == 1 and meta["withdrawn_total"] == 1
    assert meta["items"] == [
        {"statement": PROBLEM, "status": "current", "anchor_active": True, "kind": KIND2,
         "value_text": "6 V", "provenance": "Recorded by the inventor (not yet verified)",
         "replaced": [{"kind": KIND, "value_text": "5 V"}]},
        {"statement": MECHANISM, "status": "anchor_withdrawn", "anchor_active": False,
         "kind": KIND, "value_text": "3 A",
         "provenance": "Recorded by the inventor (not yet verified)", "replaced": []},
    ]
    blob = json.dumps(meta)
    assert "qty-" not in blob and "rec_" not in blob and "req:" not in blob
    assert "not been checked, validated, or assessed" in meta["note"]
    assert REQUIREMENT_QUANTITIES_META_KEY == "requirement_quantities"


def test_idea_state_carrier_defaults_empty_and_is_not_contract_serialized():
    state = _state_with_answers()
    assert state.requirement_quantities == []
    state.requirement_quantities = list(validate_quantity_history([_row(1)]))
    payload = json.dumps(ProjectRecordContract.from_state(state).to_dict())
    assert "requirement_quantities" not in payload and "qty-" not in payload


def test_canonical_assembler_is_frozen_and_emits_no_quantity_key():
    state = _state_with_answers()
    state.requirement_quantities = list(validate_quantity_history([_row(1)]))
    with_rows = assemble_deliverable(state)
    state.requirement_quantities = []
    without = assemble_deliverable(state)
    with_rows["generated_at"] = without["generated_at"] = "fixed"
    assert json.dumps(with_rows, sort_keys=True) == json.dumps(without, sort_keys=True)
    assert REQUIREMENT_QUANTITIES_META_KEY not in with_rows["_session_meta"]


# ==========================================================================
# 4. Durable store — schema, migration, append, cap, chain rule, isolation
# ==========================================================================
def test_fresh_database_creates_additive_table_keys_and_composite_foreign_keys(store):
    conn = store._conn
    tables = sorted(r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"))
    assert tables == ["projects", "records", "requirement_quantities"]
    cols = [r[1] for r in conn.execute("PRAGMA table_info(requirement_quantities)")]
    assert cols == ["project_id", "quantity_seq", "quantity_id", "anchor_record_id",
                    "requirement_id", "quantity_kind", "value_text",
                    "supersedes_quantity_id", "event_key"]
    fks = sorted((fk[0], fk[2], fk[3], fk[4]) for fk in
                 conn.execute("PRAGMA foreign_key_list(requirement_quantities)"))
    by_id = {}
    for fk_id, table, frm, to in fks:
        by_id.setdefault((fk_id, table), []).append((frm, to))
    assert sorted(sorted(v) for v in by_id.values()) == sorted(sorted(v) for v in [
        [("project_id", "project_id")],
        [("project_id", "project_id"), ("anchor_record_id", "record_id")],
        [("project_id", "project_id"), ("supersedes_quantity_id", "quantity_id")],
    ])
    assert {t for (_i, t) in by_id} == {"projects", "records", "requirement_quantities"}
    indexes = {r[1] for r in conn.execute("PRAGMA index_list(requirement_quantities)")}
    assert "requirement_quantities_supersedes_uq" in indexes
    uniques = [tuple(c[2] for c in conn.execute("PRAGMA index_info(%s)" % name))
               for name, unique in ((r[1], r[2]) for r in
                                    conn.execute("PRAGMA index_list(requirement_quantities)"))
               if unique]
    assert ("project_id", "quantity_seq") in uniques
    assert ("project_id", "event_key") in uniques
    assert ("project_id", "quantity_id") in uniques
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    assert isinstance(store, RecordStore)


def test_existing_populated_pre_t2a_database_migrates_additively_and_idempotently(tmp_path):
    path = str(tmp_path / "pre_t2a.sqlite")
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE projects (project_id TEXT PRIMARY KEY, idea_id TEXT NOT NULL, "
                 "contract_version TEXT NOT NULL, seed_idea_text TEXT, confirmed_domain TEXT, "
                 "recon_path TEXT, engine_contract_version TEXT, owner_account_id TEXT)")
    conn.execute("CREATE TABLE records (project_id TEXT NOT NULL, seq INTEGER NOT NULL, "
                 "record_id TEXT NOT NULL, payload TEXT NOT NULL, idempotency_key TEXT, "
                 "PRIMARY KEY (project_id, record_id), "
                 "FOREIGN KEY (project_id) REFERENCES projects(project_id))")
    conn.execute("INSERT INTO projects (project_id, idea_id, contract_version, owner_account_id) "
                 "VALUES ('legacy', 'idea', 'p4-0-record-contract-v1', 'acct_1')")
    payload = json.dumps({
        "record_id": "rec_1", "disposition": "answered", "content": PROBLEM,
        "gap_context": "MECHANISM_COMPLETENESS", "iteration": 1,
        "provenance": "OWNER_STATED", "validation_status": "UNVALIDATED",
        "quality": None, "pending": None, "responsibility": "OWNER_INPUT",
        "resolves_gap": False, "contradicts": [], "supersedes": [],
        "superseded_by": None, "decision_context_root": None}, sort_keys=True)
    conn.execute("INSERT INTO records VALUES ('legacy', 0, 'rec_1', ?, NULL)", (payload,))
    conn.commit()
    before = (conn.execute("SELECT * FROM projects").fetchall(),
              conn.execute("SELECT * FROM records").fetchall())
    conn.close()
    s = SqliteRecordStore(path)                    # migration on open
    try:
        assert s.load_requirement_quantities("legacy") == ()
        assert s.load_owner("legacy") == (True, "acct_1")
        s.append_requirement_quantity("legacy", _quantity(s, "legacy"))
        assert s._conn.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        s.close()
    s2 = SqliteRecordStore(path)                   # idempotent re-open
    try:
        assert [x.value_text for x in s2.load_requirement_quantities("legacy")] == ["5 V"]
        assert (s2._conn.execute("SELECT * FROM projects").fetchall(),
                s2._conn.execute("SELECT * FROM records").fetchall()) == before
    finally:
        s2.close()


def test_append_and_load_round_trip_survives_close_and_reopen(tmp_path):
    path = str(tmp_path / "durable.sqlite")
    s = SqliteRecordStore(path)
    _project(s, "P1")
    q1 = _quantity(s, "P1", text="5 V", event_key="a" * 32)
    s.append_requirement_quantity("P1", q1)
    q2 = _quantity(s, "P1", kind=KIND2, text="6.5 V", supersedes=q1.quantity_id,
                   event_key="b" * 32)
    s.append_requirement_quantity("P1", q2)
    s.close()
    s = SqliteRecordStore(path)
    try:
        history = s.load_requirement_quantities("P1")
        assert [(q.project_id, q.quantity_seq, q.quantity_id, q.anchor_record_id,
                 q.requirement_id, q.quantity_kind, q.value_text,
                 q.supersedes_quantity_id, q.event_key) for q in history] == [
            ("P1", 0, q1.quantity_id, "rec_1", "req:assertion:rec_1", KIND, "5 V", None, "a" * 32),
            ("P1", 1, q2.quantity_id, "rec_1", "req:assertion:rec_1", KIND2, "6.5 V",
             q1.quantity_id, "b" * 32)]
        assert s.requirement_quantity_for_event_key("P1", "b" * 32) == {
            "project_id": "P1", "quantity_seq": 1, "quantity_id": q2.quantity_id,
            "anchor_record_id": "rec_1", "requirement_id": "req:assertion:rec_1",
            "quantity_kind": KIND2, "value_text": "6.5 V",
            "supersedes_quantity_id": q1.quantity_id, "event_key": "b" * 32}
        assert s.requirement_quantity_for_event_key("P1", "nope") is None
        assert s.requirement_quantity_for_event_key("P1", None) is None
        assert s.requirement_quantity_for_event_key("P2", "b" * 32) is None
    finally:
        s.close()


def test_one_active_chain_and_stale_head_are_enforced_inside_the_transaction(store):
    _project(store, "P1")
    q1 = _quantity(store, "P1")
    store.append_requirement_quantity("P1", q1)
    with pytest.raises(QuantityChainConflict):          # second active row
        store.append_requirement_quantity("P1", _quantity(store, "P1", text="6 V"))
    q2 = _quantity(store, "P1", text="6 V", supersedes=q1.quantity_id)
    store.append_requirement_quantity("P1", q2)
    with pytest.raises(QuantityChainConflict):          # stale head (q1 already replaced)
        store.append_requirement_quantity(
            "P1", _quantity(store, "P1", text="7 V", supersedes=q1.quantity_id))
    with pytest.raises(QuantityChainConflict):          # unknown target
        store.append_requirement_quantity(
            "P1", _quantity(store, "P1", text="7 V", supersedes=_qid(99)))
    with pytest.raises(QuantityChainConflict):          # requirement id drift in a chain
        store.append_requirement_quantity(
            "P1", _quantity(store, "P1", text="7 V", supersedes=q2.quantity_id,
                            requirement_id="req:other"))
    assert issubclass(QuantityChainConflict, StoreError)
    history = store.load_requirement_quantities("P1")
    assert len(history) == 2 and active_quantities(history)["rec_1"].quantity_id == q2.quantity_id


def test_composite_foreign_keys_refuse_foreign_anchor_and_foreign_supersession(store):
    _project(store, "P1")
    _project(store, "P2")
    qa = _quantity(store, "P1")
    store.append_requirement_quantity("P1", qa)
    with pytest.raises(sqlite3.IntegrityError):         # rec_9 is not a record of P1
        store.append_requirement_quantity("P1", _quantity(store, "P1", anchor="rec_9"))
    # P2 cannot name P1's row: the store's chain check refuses it first; the
    # composite FK is the database-level backstop, proven by a direct insert
    with pytest.raises(QuantityChainConflict):
        store.append_requirement_quantity(
            "P2", _quantity(store, "P2", text="9 V", supersedes=qa.quantity_id))
    with pytest.raises(sqlite3.IntegrityError):
        store._conn.execute(
            "INSERT INTO requirement_quantities VALUES ('P2', 0, ?, 'rec_1', 'req', ?, "
            "'9 V', ?, ?)", (_qid(5), KIND, qa.quantity_id, "c" * 32))
    with pytest.raises(sqlite3.IntegrityError):         # orphan project
        store._conn.execute(
            "INSERT INTO requirement_quantities VALUES ('NOPE', 0, ?, 'rec_1', 'req', ?, "
            "'9 V', NULL, ?)", (_qid(6), KIND, "d" * 32))
    with pytest.raises(sqlite3.IntegrityError):         # single successor backstop
        store._conn.execute(
            "INSERT INTO requirement_quantities VALUES ('P1', 7, ?, 'rec_1', 'req', ?, "
            "'9 V', ?, ?)", (_qid(7), KIND, qa.quantity_id, "e" * 32))
        store._conn.execute(
            "INSERT INTO requirement_quantities VALUES ('P1', 8, ?, 'rec_1', 'req', ?, "
            "'9 V', ?, ?)", (_qid(8), KIND, qa.quantity_id, "f" * 32))
    store._conn.execute("DELETE FROM requirement_quantities WHERE quantity_seq >= 7")
    assert store._conn.execute("PRAGMA foreign_key_check").fetchall() == []
    assert [q.value_text for q in store.load_requirement_quantities("P1")] == ["5 V"]
    assert store.load_requirement_quantities("P2") == ()


def test_unique_event_key_is_the_durable_exact_replay_backstop(store):
    _project(store, "P1", answers=(PROBLEM, MECHANISM))
    store.append_requirement_quantity("P1", _quantity(store, "P1", event_key="a" * 32))
    with pytest.raises(sqlite3.IntegrityError):
        store.append_requirement_quantity(
            "P1", _quantity(store, "P1", anchor="rec_2", event_key="a" * 32))
    assert len(store.load_requirement_quantities("P1")) == 1
    _project(store, "P2")
    store.append_requirement_quantity("P2", _quantity(store, "P2", event_key="a" * 32))
    assert len(store.load_requirement_quantities("P2")) == 1     # project-scoped
    store._conn.execute("BEGIN IMMEDIATE")                        # no lock held after rollback
    store._conn.execute("ROLLBACK")


def test_unknown_project_wrong_type_and_project_mismatch_write_nothing(store):
    with pytest.raises(ProjectNotFound):
        store.append_requirement_quantity("missing", _quantity(store, "missing"))
    _project(store, "P1")
    with pytest.raises(StoreError):
        store.append_requirement_quantity("P1", {"not": "a quantity"})
    with pytest.raises(StoreError):
        store.append_requirement_quantity("P1", _quantity(store, "P2"))
    assert store._conn.execute("SELECT COUNT(*) FROM requirement_quantities").fetchone()[0] == 0
    assert store.load_requirement_quantities("missing") == ()


@pytest.mark.parametrize("attempts,expect_last_ok", [(199, True), (200, True), (201, False)])
def test_per_project_cap_at_199_200_and_201_attempts(store, attempts, expect_last_ok):
    _project(store, "P1")
    head = None
    ok = 0
    failed = 0
    for _ in range(attempts):
        q = _quantity(store, "P1", text="v %d" % ok, supersedes=head)
        try:
            store.append_requirement_quantity("P1", q)
            head = q.quantity_id
            ok += 1
        except QuantityCapExceeded:
            failed += 1
    assert ok == min(attempts, MAX_REQUIREMENT_QUANTITIES_PER_PROJECT)
    assert failed == (0 if expect_last_ok else attempts - MAX_REQUIREMENT_QUANTITIES_PER_PROJECT)
    history = store.load_requirement_quantities("P1")
    assert len(history) == ok and len(active_quantities(history)) == 1
    assert issubclass(QuantityCapExceeded, StoreError)
    # another project is unaffected by P1's cap
    _project(store, "P2")
    store.append_requirement_quantity("P2", _quantity(store, "P2"))


def test_project_isolation_across_projects(store):
    _project(store, "A")
    _project(store, "B")
    qa = _quantity(store, "A", event_key="a" * 32)
    store.append_requirement_quantity("A", qa)
    store.append_requirement_quantity("B", _quantity(store, "B", kind=KIND2, text="9 A",
                                                     event_key="a" * 32))
    assert [q.value_text for q in store.load_requirement_quantities("A")] == ["5 V"]
    assert [q.value_text for q in store.load_requirement_quantities("B")] == ["9 A"]
    assert store.requirement_quantity_for_event_key("B", "a" * 32)["value_text"] == "9 A"
    assert store._conn.execute("PRAGMA foreign_key_check").fetchall() == []


@pytest.mark.parametrize("sql", [
    "UPDATE requirement_quantities SET value_text = ' 5 V'",
    "UPDATE requirement_quantities SET quantity_kind = 'about'",
    "UPDATE requirement_quantities SET requirement_id = ''",
    "UPDATE requirement_quantities SET event_key = 'zz' WHERE quantity_seq = 0",
    "UPDATE requirement_quantities SET quantity_seq = 5 WHERE quantity_seq = 0",
    "UPDATE requirement_quantities SET supersedes_quantity_id = NULL WHERE quantity_seq = 1",
    "UPDATE requirement_quantities SET requirement_id = 'req:x' WHERE quantity_seq = 1",
])
def test_tampered_history_fails_closed_on_load_and_blocks_writes_inside_the_transaction(store, sql):
    _project(store, "P1")
    q1 = _quantity(store, "P1")
    store.append_requirement_quantity("P1", q1)
    q2 = _quantity(store, "P1", text="6 V", supersedes=q1.quantity_id)
    store.append_requirement_quantity("P1", q2)
    _project(store, "P2")
    store.append_requirement_quantity("P2", _quantity(store, "P2", text="1 mm"))
    with store._write():
        store._conn.execute("PRAGMA foreign_keys = OFF")
        store._conn.execute(sql + (" AND project_id = 'P1'" if "WHERE" in sql
                                   else " WHERE project_id = 'P1'"))
        store._conn.execute("PRAGMA foreign_keys = ON")
    with pytest.raises(QuantityHistoryError):
        store.load_requirement_quantities("P1")
    # a write on top of the corrupt history is refused INSIDE the transaction
    with pytest.raises(QuantityHistoryError):
        store.append_requirement_quantity(
            "P1", _quantity(store, "P1", text="7 V", supersedes=q2.quantity_id))
    assert store._conn.execute(
        "SELECT COUNT(*) FROM requirement_quantities WHERE project_id = 'P1'").fetchone()[0] == 2
    assert [q.value_text for q in store.load_requirement_quantities("P2")] == ["1 mm"]
    store._conn.execute("BEGIN IMMEDIATE")
    store._conn.execute("ROLLBACK")


def test_storage_unavailability_propagates_instead_of_returning_empty(store):
    _project(store, "P1")
    store.append_requirement_quantity("P1", _quantity(store, "P1"))
    store.close()
    with pytest.raises(sqlite3.ProgrammingError):
        store.load_requirement_quantities("P1")
    store._conn = sqlite3.connect(":memory:")


# ==========================================================================
# 5. Backup / restore parity includes the additive history
# ==========================================================================
def test_backup_restore_parity_carries_the_quantity_history(tmp_path):
    source = str(tmp_path / "live.sqlite")
    s = SqliteRecordStore(source)
    _project(s, "P1")
    q1 = _quantity(s, "P1")
    s.append_requirement_quantity("P1", q1)
    s.append_requirement_quantity("P1", _quantity(s, "P1", text="7 V", supersedes=q1.quantity_id))
    s.close()
    backup = str(tmp_path / "backup.sqlite")
    target = str(tmp_path / "restored.sqlite")
    report = backup_service.backup_database(source, backup)
    assert "requirement_quantities" in report["tables"]
    backup_service.restore_database(backup, target)
    parity = backup_service.database_parity_report(source, target)
    assert parity["schema_equal"] is True and parity["row_counts_equal"] is True
    assert parity["mismatches"] == [] and parity["tables_compared"] >= 3
    restored = SqliteRecordStore(target)
    try:
        assert [(q.value_text, q.supersedes_quantity_id)
                for q in restored.load_requirement_quantities("P1")] == [
            ("5 V", None), ("7 V", q1.quantity_id)]
        assert restored._conn.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        restored.close()
    assert backup_service.validate_sqlite_database(
        backup, required_tables=("projects", "records", "requirement_quantities"))
    assert os.path.getsize(backup) > 0
