"""T2-A Quantified Requirements Slice 1 — engine + durable-store proof.

File: tests/test_t2a_requirement_quantity_engine_store.py
Purpose: behaviour tests for the pure quantity module
(`engine/requirement_quantity.py`), the additive `IdeaState` carrier, the
additive `requirement_quantities` durable history in `engine/record_store.py`
(migration on a fresh AND an existing populated pre-T2A database, INSERT-only
append, one-active-chain enforcement, idempotency backstop, project isolation,
foreign keys, fail-closed validation on load, backup/restore parity), and the
pure presentation-row builder (the canonical assembler stays frozen).

Real on-disk SQLite only (pytest tmp_path); the real stores; no mocks of the
seams under test. Fail-closed assertions are never weakened: a corrupt
populated history must raise with NOTHING returned, and a project with zero
quantities must assemble a package with NO new key.
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
    QuantityChainConflict,
)
from engine.requirement_quantity import (
    QUANTIFIED_REQUIREMENTS_META_KEY, quantified_requirements_meta,
    QUANTITY_BOUNDS, QUANTITY_UNITS, QuantityHistoryError, QuantityValueError,
    RequirementQuantity, active_quantities, canonical_value,
    derive_quantified_requirements, eligible_anchors, is_canonical_value,
    validate_bound, validate_quantity_history, validate_unit,
)

PROBLEM = ("The problem is that cyclists have no reliable brake light because "
           "the microcontroller must switch the LED when the sensor voltage "
           "changes suddenly.")
MECHANISM = ("The mechanism works because the accelerometer outputs a voltage "
             "proportional to deceleration and the microcontroller drives the "
             "LED through a transistor.")


def _qid(n):
    return "qty-" + ("%032x" % n)


def _row(qid, anchor="rec_1", bound="target", value="5", unit="V", supersedes=None):
    return {"quantity_id": qid, "anchor_record_id": anchor, "bound": bound,
            "value": value, "unit": unit, "supersedes": supersedes}


@pytest.fixture
def store(tmp_path):
    s = SqliteRecordStore(str(tmp_path / "t2a.sqlite"))
    try:
        yield s
    finally:
        s.close()


def _project(store, pid, answers=()):
    state = IdeaState(idea_id="idea-" + pid)
    for text in answers:
        state.record_interaction(DISPOSITION_ANSWERED, text,
                                 gap_context="MECHANISM_COMPLETENESS", iteration=1)
    store.create_project(ProjectRecordContract.from_state(state), project_id=pid)
    return state


# ==========================================================================
# 1. Canonical stored value — one form, ASCII grammar, idempotent
# ==========================================================================
@pytest.mark.parametrize("raw,expected", [
    ("5", "5"), ("05", "5"), (" 12.50 ", "12.5"), ("0.50", "0.5"),
    ("1000", "1000"), ("-12.340", "-12.34"), ("0", "0"), ("-0", "0"),
    ("0.000001", "0.000001"), ("123456789012.123456", "123456789012.123456"),
    ("-0.0", "0"), ("100.000", "100"),
])
def test_canonical_value_is_one_plain_decimal_form(raw, expected):
    assert canonical_value(raw) == expected
    assert canonical_value(expected) == expected           # idempotent
    assert is_canonical_value(expected)


@pytest.mark.parametrize("raw", [
    "", "   ", "abc", "1e3", "1E3", "1,000", "1 000", "+5", "1.2345678",
    "1234567890123", ".5", "5.", "--5", "5-", "١٢", "１２", "1٫5", "NaN",
    "Infinity", "0x10", "5 V", "1" * 40, None, 5,
])
def test_non_canonical_or_foreign_input_is_rejected(raw):
    with pytest.raises(QuantityValueError):
        canonical_value(raw)


def test_non_canonical_stored_text_is_never_accepted_as_canonical():
    for text in ("05", "5.0", "-0", "1.50", " 5", "5 ", "1e3", "", None):
        assert not is_canonical_value(text)


def test_bound_and_unit_vocabularies_are_closed():
    assert set(QUANTITY_BOUNDS) == {"target", "minimum", "maximum"}
    assert len(set(QUANTITY_UNITS)) == len(QUANTITY_UNITS) >= 10
    for b in QUANTITY_BOUNDS:
        assert validate_bound(b) == b
    for u in QUANTITY_UNITS:
        assert validate_unit(u) == u
        assert u.isascii() and u.replace("_", "").isalnum()
    for bad in ("", "TARGET", "about", None, "volts", "V ", "furlong"):
        with pytest.raises(QuantityValueError):
            validate_bound(bad)
        with pytest.raises(QuantityValueError):
            validate_unit(bad)


# ==========================================================================
# 2. History validation — zero rows valid; every corruption fails closed
# ==========================================================================
def test_zero_rows_are_a_valid_empty_history():
    assert validate_quantity_history([]) == ()
    assert validate_quantity_history(iter(())) == ()
    assert active_quantities(()) == {}


def test_valid_chain_derives_inverse_edges_and_one_active_per_anchor():
    rows = [_row(_qid(1)), _row(_qid(2), value="6", supersedes=_qid(1)),
            _row(_qid(3), anchor="rec_2", unit="mm", value="0.5"),
            _row(_qid(4), value="7", bound="maximum", supersedes=_qid(2))]
    history = validate_quantity_history(rows)
    assert [q.quantity_id for q in history] == [_qid(1), _qid(2), _qid(3), _qid(4)]
    assert history[0].superseded_by == _qid(2)
    assert history[1].superseded_by == _qid(4)
    assert history[2].superseded_by is None
    assert history[3].superseded_by is None and history[3].supersedes == _qid(2)
    active = active_quantities(history)
    assert set(active) == {"rec_1", "rec_2"}
    assert active["rec_1"].value == "7" and active["rec_1"].bound == "maximum"
    assert active["rec_2"].unit == "mm"
    # frozen: never mutated in place
    with pytest.raises(FrozenInstanceError):
        history[0].value = "9"
    # the input rows were not mutated
    assert rows[0] == _row(_qid(1))


@pytest.mark.parametrize("label,rows", [
    ("malformed id", [_row("qty-short")]),
    ("malformed id prefix", [_row("rec_" + "0" * 32)]),
    ("duplicate id", [_row(_qid(1)), _row(_qid(1), anchor="rec_2")]),
    ("malformed anchor", [_row(_qid(1), anchor="rec_0")]),
    ("malformed anchor text", [_row(_qid(1), anchor="rec-abc")]),
    ("unknown bound", [_row(_qid(1), bound="about")]),
    ("unknown unit", [_row(_qid(1), unit="furlong")]),
    ("non-canonical value", [_row(_qid(1), value="05")]),
    ("non-canonical trailing zero", [_row(_qid(1), value="5.0")]),
    ("exponent value", [_row(_qid(1), value="1E+3")]),
    ("unknown supersedes", [_row(_qid(1), supersedes=_qid(9))]),
    ("later supersedes", [_row(_qid(1), supersedes=_qid(2)),
                          _row(_qid(2), supersedes=None)]),
    ("self supersedes", [_row(_qid(1), supersedes=_qid(1))]),
    ("cross-anchor supersedes", [_row(_qid(1)),
                                 _row(_qid(2), anchor="rec_2", supersedes=_qid(1))]),
    ("double supersession", [_row(_qid(1)), _row(_qid(2), supersedes=_qid(1)),
                             _row(_qid(3), supersedes=_qid(1))]),
    ("two active per anchor", [_row(_qid(1)), _row(_qid(2), value="6")]),
    ("missing field", [{"quantity_id": _qid(1)}]),
    ("non-mapping row", ["not a row"]),
    ("None value", [_row(_qid(1), value=None)]),
])
def test_every_structural_corruption_raises_with_nothing_returned(label, rows):
    with pytest.raises(QuantityHistoryError):
        validate_quantity_history(rows)


def test_corruption_message_names_structure_only_never_content():
    rows = [_row(_qid(1), value="05", anchor="rec_77")]
    with pytest.raises(QuantityHistoryError) as info:
        validate_quantity_history(rows)
    text = str(info.value)
    assert "05" not in text and "rec_77" not in text and _qid(1) not in text


# ==========================================================================
# 3. Eligible anchors and the read-only derivation
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
    assert [req.statement for req, _rec in anchors] == [PROBLEM, MECHANISM]
    # a withdrawn (superseded) answer is no longer eligible — deterministically
    state.record_interaction(DISPOSITION_ANSWERED, "corrected mechanism text",
                             gap_context="MECHANISM_COMPLETENESS", iteration=4,
                             supersedes=["rec_2"])
    assert [rec.record_id for _req, rec in eligible_anchors(state)] == ["rec_1", "rec_5"]
    # a contradiction pair anchors a contradiction requirement, not an assertion
    state.mark_contradiction("rec_1", "rec_5")
    assert eligible_anchors(state) == ()


def test_derivation_omits_inactive_anchors_and_superseded_rows_and_mutates_nothing():
    state = _state_with_answers()
    history = validate_quantity_history([
        _row(_qid(1), anchor="rec_1", value="5", unit="V"),
        _row(_qid(2), anchor="rec_1", value="6", unit="V", supersedes=_qid(1)),
        _row(_qid(3), anchor="rec_2", value="0.5", unit="mm"),
        _row(_qid(4), anchor="rec_9", value="1", unit="count"),   # no such anchor
    ])
    state.requirement_quantities = list(history)
    before = json.dumps([q.__dict__ for q in state.requirement_quantities], sort_keys=True)
    rows = derive_quantified_requirements(state)
    assert [(r.anchor_record_id, r.quantity.value) for r in rows] == [
        ("rec_1", "6"), ("rec_2", "0.5")]
    assert rows[0].statement == PROBLEM
    # withdrawing the answer that rec_2 anchors makes its chain inactive
    state.record_interaction(DISPOSITION_ANSWERED, "corrected", iteration=4,
                             gap_context="MECHANISM_COMPLETENESS", supersedes=["rec_2"])
    rows = derive_quantified_requirements(state)
    assert [r.anchor_record_id for r in rows] == ["rec_1"]
    assert json.dumps([q.__dict__ for q in state.requirement_quantities],
                      sort_keys=True) == before
    assert derive_quantified_requirements(IdeaState(idea_id="empty")) == ()


def test_idea_state_carrier_defaults_empty_and_is_not_contract_serialized():
    state = _state_with_answers()
    assert state.requirement_quantities == []
    state.requirement_quantities = list(validate_quantity_history([_row(_qid(1))]))
    payload = ProjectRecordContract.from_state(state).to_dict()
    assert "requirement_quantities" not in json.dumps(payload)
    assert "qty-" not in json.dumps(payload)


# ==========================================================================
# 4. Presentation rows — additive nested key, invisible at zero; assembler frozen
# ==========================================================================
def test_zero_quantities_produce_no_meta_and_the_assembler_adds_no_key():
    state = _state_with_answers()
    assert quantified_requirements_meta(state) is None
    package = assemble_deliverable(state)
    assert QUANTIFIED_REQUIREMENTS_META_KEY not in package["_session_meta"]
    assert QUANTIFIED_REQUIREMENTS_META_KEY not in package
    # rows that attach to no current anchor also produce nothing
    state.requirement_quantities = list(validate_quantity_history(
        [_row(_qid(4), anchor="rec_9", value="1", unit="count")]))
    assert quantified_requirements_meta(state) is None


def test_quantities_produce_one_nested_meta_with_canonical_tokens_and_no_claim():
    state = _state_with_answers()
    state.requirement_quantities = list(validate_quantity_history([
        _row(_qid(1), anchor="rec_1", value="5", unit="V"),
        _row(_qid(2), anchor="rec_1", value="6", unit="V", bound="maximum",
             supersedes=_qid(1)),
        _row(_qid(3), anchor="rec_2", value="0.5", unit="mm", bound="minimum"),
    ]))
    meta = quantified_requirements_meta(state)
    assert meta["total"] == 2
    assert meta["items"] == [
        {"statement": PROBLEM, "bound": "maximum", "value": "6", "unit": "V",
         "provenance": "Recorded by the inventor (not yet verified)"},
        {"statement": MECHANISM, "bound": "minimum", "value": "0.5", "unit": "mm",
         "provenance": "Recorded by the inventor (not yet verified)"},
    ]
    blob = json.dumps(meta)                         # JSON-safe
    assert "qty-" not in blob                       # no internal identifier
    assert "not been checked, validated, or assessed" in meta["note"]
    # the canonical assembler is FROZEN (G-3 A-20/A-21 pin): it never reads the
    # carrier, so its package is identical with and without quantities and the
    # nested key is composed only at the web deliverable seam.
    with_quantities = assemble_deliverable(state)
    state.requirement_quantities = []
    without = assemble_deliverable(state)
    with_quantities["generated_at"] = without["generated_at"] = "fixed"
    assert json.dumps(with_quantities, sort_keys=True) == json.dumps(without, sort_keys=True)
    assert QUANTIFIED_REQUIREMENTS_META_KEY not in with_quantities["_session_meta"]
    assert set(with_quantities) == set(assemble_deliverable(IdeaState(idea_id="z")))


# ==========================================================================
# 5. Durable store — migration, append, chain rule, isolation, validation
# ==========================================================================
def test_fresh_database_creates_additive_table_indexes_and_foreign_key(store):
    conn = store._conn
    tables = sorted(r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"))
    assert tables == ["projects", "records", "requirement_quantities"]
    cols = [r[1] for r in conn.execute("PRAGMA table_info(requirement_quantities)")]
    assert cols == ["project_id", "seq", "quantity_id", "anchor_record_id", "bound",
                    "value_canonical", "unit", "supersedes_quantity_id",
                    "idempotency_key"]
    assert "superseded_by" not in cols                # inverse edge is derived
    indexes = {r[1] for r in conn.execute("PRAGMA index_list(requirement_quantities)")}
    assert {"requirement_quantities_seq_uq",
            "requirement_quantities_idempotency_key_uq",
            "requirement_quantities_supersedes_uq"} <= indexes
    fks = conn.execute("PRAGMA foreign_key_list(requirement_quantities)").fetchall()
    assert [(fk[2], fk[3], fk[4]) for fk in fks] == [("projects", "project_id", "project_id")]
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
    before = conn.execute("SELECT * FROM projects").fetchall(), \
        conn.execute("SELECT * FROM records").fetchall()
    conn.close()

    s = SqliteRecordStore(path)                    # migration on open
    try:
        assert s.load_requirement_quantities("legacy") == ()     # zero rows valid
        assert s.load_owner("legacy") == (True, "acct_1")
        assert [r.record_id for r in s.load_contract("legacy").assertions] == ["rec_1"]
        q = RequirementQuantity(s.new_quantity_id(), "rec_1", "target", "5", "V")
        s.append_requirement_quantity("legacy", q, idempotency_key="k")
        assert s._conn.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        s.close()
    s2 = SqliteRecordStore(path)                   # idempotent re-open
    try:
        assert [x.value for x in s2.load_requirement_quantities("legacy")] == ["5"]
        conn = s2._conn
        assert (conn.execute("SELECT * FROM projects").fetchall(),
                conn.execute("SELECT * FROM records").fetchall()) == before
    finally:
        s2.close()


def test_append_and_load_round_trip_survives_close_and_reopen(tmp_path):
    path = str(tmp_path / "durable.sqlite")
    s = SqliteRecordStore(path)
    _project(s, "P1", [PROBLEM])
    q1 = RequirementQuantity(s.new_quantity_id(), "rec_1", "target", "5", "V")
    q2 = RequirementQuantity(s.new_quantity_id(), "rec_1", "maximum", "6.5", "V",
                             supersedes=q1.quantity_id)
    s.append_requirement_quantity("P1", q1, idempotency_key="k1")
    s.append_requirement_quantity("P1", q2, idempotency_key="k2")
    s.close()
    s = SqliteRecordStore(path)
    try:
        history = s.load_requirement_quantities("P1")
        assert [(q.quantity_id, q.bound, q.value, q.unit, q.supersedes, q.superseded_by)
                for q in history] == [
            (q1.quantity_id, "target", "5", "V", None, q2.quantity_id),
            (q2.quantity_id, "maximum", "6.5", "V", q1.quantity_id, None)]
        assert s.requirement_quantity_for_idempotency_key("P1", "k2") == {
            "quantity_id": q2.quantity_id, "anchor_record_id": "rec_1",
            "bound": "maximum", "value": "6.5", "unit": "V",
            "supersedes": q1.quantity_id}
        assert s.requirement_quantity_for_idempotency_key("P1", "nope") is None
        assert s.requirement_quantity_for_idempotency_key("P1", None) is None
        assert s.requirement_quantity_for_idempotency_key("P2", "k2") is None
    finally:
        s.close()


def test_one_active_chain_per_anchor_is_enforced_atomically(store):
    _project(store, "P1", [PROBLEM])
    q1 = RequirementQuantity(store.new_quantity_id(), "rec_1", "target", "5", "V")
    store.append_requirement_quantity("P1", q1)
    # a second ACTIVE row for the same anchor is refused
    with pytest.raises(QuantityChainConflict):
        store.append_requirement_quantity(
            "P1", RequirementQuantity(store.new_quantity_id(), "rec_1", "minimum", "6", "V"))
    q2 = RequirementQuantity(store.new_quantity_id(), "rec_1", "minimum", "6", "V",
                             supersedes=q1.quantity_id)
    store.append_requirement_quantity("P1", q2)
    # the same target cannot be superseded twice
    with pytest.raises(QuantityChainConflict):
        store.append_requirement_quantity(
            "P1", RequirementQuantity(store.new_quantity_id(), "rec_1", "minimum", "7", "V",
                                      supersedes=q1.quantity_id))
    # an unknown / absent target is refused
    with pytest.raises(QuantityChainConflict):
        store.append_requirement_quantity(
            "P1", RequirementQuantity(store.new_quantity_id(), "rec_1", "minimum", "7", "V",
                                      supersedes=_qid(99)))
    # a target of ANOTHER anchor is refused
    with pytest.raises(QuantityChainConflict):
        store.append_requirement_quantity(
            "P1", RequirementQuantity(store.new_quantity_id(), "rec_2", "minimum", "7", "V",
                                      supersedes=q2.quantity_id))
    # QuantityChainConflict is a StoreError (one failure family for callers)
    assert issubclass(QuantityChainConflict, StoreError)
    history = store.load_requirement_quantities("P1")
    assert len(history) == 2 and list(active_quantities(history)) == ["rec_1"]
    assert active_quantities(history)["rec_1"].quantity_id == q2.quantity_id


def test_unknown_project_and_wrong_type_are_refused_with_nothing_written(store):
    q = RequirementQuantity(store.new_quantity_id(), "rec_1", "target", "5", "V")
    with pytest.raises(ProjectNotFound):
        store.append_requirement_quantity("missing", q)
    _project(store, "P1")
    with pytest.raises(StoreError):
        store.append_requirement_quantity("P1", {"not": "a quantity"})
    assert store._conn.execute(
        "SELECT COUNT(*) FROM requirement_quantities").fetchone()[0] == 0
    assert store.load_requirement_quantities("missing") == ()   # non-disclosing


def test_idempotency_key_is_a_durable_duplicate_backstop_that_rolls_back(store):
    _project(store, "P1", [PROBLEM, MECHANISM])
    store.append_requirement_quantity(
        "P1", RequirementQuantity(store.new_quantity_id(), "rec_1", "target", "5", "V"),
        idempotency_key="same")
    with pytest.raises(sqlite3.IntegrityError):
        store.append_requirement_quantity(
            "P1", RequirementQuantity(store.new_quantity_id(), "rec_2", "target", "1", "mm"),
            idempotency_key="same")
    assert len(store.load_requirement_quantities("P1")) == 1
    # a NULL key never collides (legacy/mixed-state compatible)
    store.append_requirement_quantity(
        "P1", RequirementQuantity(store.new_quantity_id(), "rec_2", "target", "1", "mm"))
    assert len(store.load_requirement_quantities("P1")) == 2
    # the connection holds no lock after the rolled-back write
    store._conn.execute("BEGIN IMMEDIATE")
    store._conn.execute("ROLLBACK")


def test_project_isolation_across_projects(store):
    _project(store, "A", [PROBLEM])
    _project(store, "B", [PROBLEM])
    qa = RequirementQuantity(store.new_quantity_id(), "rec_1", "target", "5", "V")
    store.append_requirement_quantity("A", qa, idempotency_key="k")
    # same anchor id, same idempotency key, different project: independent
    qb = RequirementQuantity(store.new_quantity_id(), "rec_1", "maximum", "9", "A")
    store.append_requirement_quantity("B", qb, idempotency_key="k")
    assert [q.value for q in store.load_requirement_quantities("A")] == ["5"]
    assert [q.value for q in store.load_requirement_quantities("B")] == ["9"]
    # B cannot supersede A's row
    with pytest.raises(QuantityChainConflict):
        store.append_requirement_quantity(
            "B", RequirementQuantity(store.new_quantity_id(), "rec_1", "maximum", "10", "A",
                                     supersedes=qa.quantity_id))
    assert store.requirement_quantity_for_idempotency_key("B", "k")["value"] == "9"
    assert store._conn.execute("PRAGMA foreign_key_check").fetchall() == []


@pytest.mark.parametrize("sql", [
    "UPDATE requirement_quantities SET value_canonical = '05'",
    "UPDATE requirement_quantities SET unit = 'furlong'",
    "UPDATE requirement_quantities SET bound = 'about'",
    "UPDATE requirement_quantities SET anchor_record_id = 'rec_0'",
    "UPDATE requirement_quantities SET quantity_id = 'qty-bad' WHERE seq = 0",
    "UPDATE requirement_quantities SET supersedes_quantity_id = quantity_id WHERE seq = 1",
    "UPDATE requirement_quantities SET supersedes_quantity_id = NULL WHERE seq = 1",
    "UPDATE requirement_quantities SET anchor_record_id = 'rec_2' WHERE seq = 1",
])
def test_tampered_populated_history_fails_closed_on_load(store, sql):
    _project(store, "P1", [PROBLEM])
    q1 = RequirementQuantity(store.new_quantity_id(), "rec_1", "target", "5", "V")
    q2 = RequirementQuantity(store.new_quantity_id(), "rec_1", "maximum", "6", "V",
                             supersedes=q1.quantity_id)
    store.append_requirement_quantity("P1", q1)
    store.append_requirement_quantity("P1", q2)
    _project(store, "P2", [PROBLEM])
    store.append_requirement_quantity(
        "P2", RequirementQuantity(store.new_quantity_id(), "rec_1", "target", "1", "mm"))
    with store._write():
        # bypass the store API on purpose: simulate on-disk corruption of P1 only
        store._conn.execute(sql + (" AND project_id = 'P1'" if "WHERE" in sql
                                   else " WHERE project_id = 'P1'"))
    with pytest.raises(QuantityHistoryError):
        store.load_requirement_quantities("P1")
    # another project is unaffected; nothing was silently repaired for P1
    assert [q.value for q in store.load_requirement_quantities("P2")] == ["1"]
    with pytest.raises(QuantityHistoryError):
        store.load_requirement_quantities("P1")


def test_storage_unavailability_propagates_instead_of_returning_empty(store):
    _project(store, "P1", [PROBLEM])
    store.append_requirement_quantity(
        "P1", RequirementQuantity(store.new_quantity_id(), "rec_1", "target", "5", "V"))
    store.close()
    with pytest.raises(sqlite3.ProgrammingError):
        store.load_requirement_quantities("P1")
    store._conn = sqlite3.connect(":memory:")       # keep the fixture's close() safe


# ==========================================================================
# 6. Backup / restore parity includes the additive history
# ==========================================================================
def test_backup_restore_parity_carries_the_quantity_history(tmp_path):
    source = str(tmp_path / "live.sqlite")
    s = SqliteRecordStore(source)
    _project(s, "P1", [PROBLEM])
    q1 = RequirementQuantity(s.new_quantity_id(), "rec_1", "target", "5", "V")
    s.append_requirement_quantity("P1", q1, idempotency_key="k1")
    s.append_requirement_quantity(
        "P1", RequirementQuantity(s.new_quantity_id(), "rec_1", "minimum", "7", "V",
                                  supersedes=q1.quantity_id), idempotency_key="k2")
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
        assert [(q.value, q.supersedes) for q in restored.load_requirement_quantities("P1")] == [
            ("5", None), ("7", q1.quantity_id)]
        assert restored._conn.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        restored.close()
    assert backup_service.validate_sqlite_database(
        backup, required_tables=("projects", "records", "requirement_quantities"))
    assert os.path.getsize(backup) > 0
