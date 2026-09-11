"""T2-A Quantified Requirements Slice 1 — engine + durable-store proof.

File: tests/test_t2a_requirement_quantity_engine_store.py
Purpose: behaviour tests for the accepted Slice-1 data contract
(`engine/requirement_quantity.py`: the canonical `RequirementQuantity` row,
the closed six-token `quantity_kind` vocabulary, the exact `value_text`
policy, fail-closed history validation, per-anchor chain derivation with
replaced / withdrawn semantics, the canonical package rows), the additive
`IdeaState` carrier, and the additive `requirement_quantities` durable
history in `engine/record_store.py` (migration on a fresh AND an existing
populated pre-T2A database, INSERT-only append with history validation
INSIDE the write transaction, the per-project cap at 199/200/201,
one-active-chain / stale-head enforcement, the exact index set with direct
SQLite proofs, composite foreign keys, unique event key, project isolation,
fail-closed load, backup/restore parity). The canonical deliverable
assembler stays frozen.

Real on-disk SQLite only (pytest tmp_path); the real stores; no mocks of the
seams under test. Fail-closed assertions are never weakened.
"""
import dataclasses
import json
import os
import sqlite3
import uuid
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
    QuantityChainConflict, QuantityCapExceeded, QuantityAnchorIneligible,
)
from engine.requirement_quantity import (
    ANCHOR_ACTIVE, ANCHOR_INVALID, ANCHOR_WITHDRAWN, CANONICAL_ROW_FIELDS,
    MAX_REQUIREMENT_QUANTITIES_PER_PROJECT,
    MAX_VALUE_TEXT_CHARS, QUANTITY_EXACT_REPLAY, QUANTITY_INSERTED,
    QUANTITY_KINDS, QUANTITY_PROVENANCE,
    QUANTITY_VALIDATION_STATUS, REQUIREMENT_QUANTITIES_META_KEY,
    QuantityHistoryError, QuantityValueError, RequirementQuantity,
    active_quantities, answered_anchor_index, classify_ledger_anchor,
    classify_state_anchor, eligible_anchors, is_recorded_at, is_stored_value_text,
    normalize_value_text, quantity_chains, requirement_quantities_meta,
    requirement_statement, supersession_relations, superseded_ids,
    validate_new_quantity, validate_quantity_history, validate_quantity_kind,
)

PROBLEM = ("The problem is that cyclists have no reliable brake light because "
           "the microcontroller must switch the LED when the sensor voltage "
           "changes suddenly.")
MECHANISM = ("The mechanism works because the accelerometer outputs a voltage "
             "proportional to deceleration and the microcontroller drives the "
             "LED through a transistor.")
KIND = "target_value"
KIND2 = "maximum_value"
AT = "2026-09-11T12:00:00+00:00"


def _qid(n):
    return "qty-" + ("%032x" % n)


def _ek(n):
    return "%032x" % (n + 1000)


def _row(n, anchor="rec_1", kind=KIND, text="5 V", supersedes=None, seq=None,
         requirement_id=None, event_key=None, iteration=1, at=AT, **extra):
    row = {"quantity_seq": n if seq is None else seq, "quantity_id": _qid(n),
           "anchor_record_id": anchor,
           "requirement_id": ("req:assertion:" + anchor) if requirement_id is None else requirement_id,
           "quantity_kind": kind, "value_text": text,
           "supersedes_quantity_id": supersedes, "event_key": event_key or _ek(n),
           "recorded_iteration": iteration, "recorded_at": at}
    row.update(extra)
    return row


def _quantity(store, anchor="rec_1", kind=KIND, text="5 V", supersedes=None,
              event_key=None, requirement_id=None, iteration=1, at=AT):
    return RequirementQuantity(
        quantity_id=store.new_quantity_id(), quantity_seq=-1,
        anchor_record_id=anchor,
        requirement_id=("req:assertion:" + anchor) if requirement_id is None else requirement_id,
        quantity_kind=kind, value_text=text, supersedes_quantity_id=supersedes,
        event_key=event_key or uuid.uuid4().hex, recorded_iteration=iteration,
        recorded_at=at)


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


def _project_with_a_non_answer(store, pid):
    """A project whose ledger holds an ANSWERED rec_1 and a rec_2 that was
    never a valid answered assertion anchor (unknown disposition). Both records
    exist, so pointing a quantity at rec_2 satisfies every FOREIGN KEY while
    still being an invalid anchor."""
    state = IdeaState(idea_id="idea-" + pid)
    state.record_interaction(DISPOSITION_ANSWERED, PROBLEM,
                             gap_context="MECHANISM_COMPLETENESS", iteration=1)
    state.record_interaction(DISPOSITION_UNKNOWN, "",
                             gap_context="PHYSICAL_FEASIBILITY", iteration=1)
    store.create_project(ProjectRecordContract.from_state(state), project_id=pid)
    return state


def _point_anchor_at(store, project_id, anchor):
    """Repoint a stored quantity row's anchor (durable corruption injection)."""
    store._conn.execute(
        "UPDATE requirement_quantities SET anchor_record_id = ?, requirement_id = ? "
        "WHERE project_id = ?", (anchor, "req:assertion:" + anchor, project_id))
    store._conn.commit()


def _raw_insert(store, project_id, seq, qid, anchor, supersedes, event_key, kind=KIND):
    store._conn.execute(
        "INSERT INTO requirement_quantities VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (project_id, seq, qid, anchor, "req:assertion:" + anchor, kind, "9 V",
         supersedes, event_key, 1, AT))


# ==========================================================================
# 1. Data contract, kind vocabulary, value_text policy
# ==========================================================================
def test_canonical_row_has_exactly_the_accepted_fields_and_fixed_values():
    assert CANONICAL_ROW_FIELDS == (
        "quantity_id", "quantity_seq", "anchor_record_id", "requirement_id",
        "quantity_kind", "value_text", "supersedes_quantity_id", "event_key",
        "recorded_iteration", "recorded_at", "validation_status", "provenance")
    q = RequirementQuantity(_qid(1), 0, "rec_1", "req:assertion:rec_1", KIND, "5 V",
                            None, _ek(1), 3, AT)
    assert q.validation_status == QUANTITY_VALIDATION_STATUS == "UNVALIDATED"
    assert q.provenance == QUANTITY_PROVENANCE == "OWNER_STATED"
    assert "project_id" not in CANONICAL_ROW_FIELDS      # store/database scoping only
    with pytest.raises(FrozenInstanceError):
        q.value_text = "6 V"


def test_kind_vocabulary_is_the_frozen_six_token_set():
    assert QUANTITY_KINDS == ("target_value", "minimum_value", "maximum_value",
                              "range", "count", "other_quantity")
    for kind in QUANTITY_KINDS:
        assert validate_quantity_kind(kind) == kind
    for bad in ("", None, "TARGET_VALUE", "target", "tolerance", "unit", KIND + " ", 5):
        with pytest.raises(QuantityValueError):
            validate_quantity_kind(bad)


@pytest.mark.parametrize("raw,expected", [
    ("5 V", "5 V"),
    ("  12.5   V ", "12.5   V"),                       # internal spaces preserved exactly
    ("0.5 mm ± 0.1", "0.5 mm ± 0.1"),
    ("٢٥٠ نيوتن", "٢٥٠ نيوتن"),
    ("a" * MAX_VALUE_TEXT_CHARS, "a" * MAX_VALUE_TEXT_CHARS),      # 120 accepted
    ("  " + "b" * MAX_VALUE_TEXT_CHARS + "\n", "b" * MAX_VALUE_TEXT_CHARS),
    ("١" * MAX_VALUE_TEXT_CHARS, "١" * MAX_VALUE_TEXT_CHARS),     # code points, not bytes
    ("5 V", "5 V"),                          # no extra Unicode exclusion
    ("1,000  volts", "1,000  volts"),                  # no parsing or conversion
    ("00012", "00012"),                                # no numeric normalization
])
def test_value_text_policy_strips_outer_whitespace_only(raw, expected):
    assert normalize_value_text(raw) == expected
    assert normalize_value_text(expected) == expected
    assert is_stored_value_text(expected)


@pytest.mark.parametrize("raw", [
    "", "   ", "\t", "\n", None, 5, b"5 V",
    "a" * (MAX_VALUE_TEXT_CHARS + 1),                  # 121 rejected
    "5\tV", "5\nV", "5\rV", "5\x00V", "5\x1fV",        # C0 controls (tab included)
    "5\x7fV", "5\x85V", "5\x9fV",                      # C1 controls
])
def test_value_text_policy_rejects_empty_long_and_control_input(raw):
    with pytest.raises(QuantityValueError):
        normalize_value_text(raw)
    assert not is_stored_value_text(raw)
    assert MAX_VALUE_TEXT_CHARS == 120


def test_value_text_error_never_carries_the_text():
    with pytest.raises(QuantityValueError) as info:
        normalize_value_text("secret-value-123\tx")
    assert "secret-value-123" not in str(info.value)


def test_recorded_at_must_be_utc_iso8601():
    assert is_recorded_at("2026-09-11T12:00:00+00:00")
    assert is_recorded_at("2026-09-11T12:00:00Z")
    for bad in ("", None, "2026-09-11", "2026-09-11T12:00:00", "2026-09-11T12:00:00+02:00",
                "yesterday", 5):
        assert not is_recorded_at(bad)


# ==========================================================================
# 2. History validation — zero rows valid; every corruption fails closed
# ==========================================================================
def test_zero_rows_are_a_valid_empty_history():
    assert validate_quantity_history([]) == ()
    assert validate_quantity_history(iter(())) == ()
    assert active_quantities(()) == {} and superseded_ids(()) == set()


def test_valid_chain_derives_active_and_superseded_rows_with_fixed_values():
    rows = [_row(1), _row(2, text="6 V", supersedes=_qid(1)),
            _row(3, anchor="rec_2", kind=KIND2, text="0.5 mm"),
            _row(4, text="7 V", supersedes=_qid(2))]
    history = validate_quantity_history(rows)
    assert [q.quantity_id for q in history] == [_qid(1), _qid(2), _qid(3), _qid(4)]
    assert all(q.validation_status == "UNVALIDATED" and q.provenance == "OWNER_STATED"
               for q in history)
    assert superseded_ids(history) == {_qid(1), _qid(2)}
    active = active_quantities(history)
    assert set(active) == {"rec_1", "rec_2"}
    assert active["rec_1"].value_text == "7 V" and active["rec_2"].quantity_kind == KIND2
    assert rows[0] == _row(1)                        # input untouched
    # explicit canonical fixed values are accepted; non-canonical ones are not
    assert validate_quantity_history([_row(1, validation_status="UNVALIDATED",
                                           provenance="OWNER_STATED")])


@pytest.mark.parametrize("label,rows", [
    ("missing field", [{"quantity_id": _qid(1)}]),
    ("non-mapping", ["nope"]),
    ("seq not ascending", [_row(1, seq=5), _row(2, seq=5, anchor="rec_2")]),
    ("seq negative", [_row(1, seq=-1)]),
    ("seq bool", [_row(1, seq=True)]),
    ("malformed id", [_row(1) | {"quantity_id": "qty-short"}]),
    ("duplicate id", [_row(1), _row(2, anchor="rec_2") | {"quantity_id": _qid(1)}]),
    ("malformed anchor", [_row(1, anchor="rec_0")]),
    ("malformed anchor text", [_row(1, anchor="rec-abc")]),
    ("requirement id mismatch", [_row(1, requirement_id="req:assertion:rec_2")]),
    ("empty requirement id", [_row(1, requirement_id="")]),
    ("unknown kind", [_row(1, kind="tolerance")]),
    ("value not stored form", [_row(1, text=" 5 V")]),
    ("value empty", [_row(1, text="")]),
    ("value control", [_row(1, text="5\tV")]),
    ("value too long", [_row(1, text="a" * 121)]),
    ("malformed event key", [_row(1, event_key="zz")]),
    ("duplicate event key", [_row(1), _row(2, anchor="rec_2", event_key=_ek(1))]),
    ("negative iteration", [_row(1, iteration=-1)]),
    ("bool iteration", [_row(1, iteration=True)]),
    ("malformed recorded_at", [_row(1, at="yesterday")]),
    ("non-utc recorded_at", [_row(1, at="2026-09-11T12:00:00+02:00")]),
    ("non-canonical validation status", [_row(1, validation_status="VERIFIED")]),
    ("non-canonical provenance", [_row(1, provenance="SYSTEM_INFERRED")]),
    ("unknown supersedes", [_row(1, supersedes=_qid(9))]),
    ("later supersedes", [_row(1, supersedes=_qid(2)), _row(2)]),
    ("self supersedes", [_row(1, supersedes=_qid(1))]),
    ("cross-anchor supersedes", [_row(1), _row(2, anchor="rec_2", supersedes=_qid(1))]),
    ("double supersession", [_row(1), _row(2, supersedes=_qid(1)), _row(3, supersedes=_qid(1))]),
    ("second root for one anchor", [_row(1), _row(2, text="6 V")]),
    ("over cap", [_row(i, anchor="rec_%d" % i) for i in range(1, MAX_REQUIREMENT_QUANTITIES_PER_PROJECT + 2)]),
])
def test_every_structural_corruption_raises_with_nothing_returned(label, rows):
    with pytest.raises(QuantityHistoryError):
        validate_quantity_history(rows)


def test_corruption_message_names_structure_only_never_content():
    with pytest.raises(QuantityHistoryError) as info:
        validate_quantity_history([_row(1, text=" 77 secret", anchor="rec_77")])
    text = str(info.value)
    assert "secret" not in text and "rec_77" not in text and _qid(1) not in text


# ==========================================================================
# 3. Eligible anchors, chain derivation, canonical package rows
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
    assert requirement_statement(state, "rec_2") == MECHANISM      # retained text
    assert requirement_statement(state, "rec_1") == PROBLEM
    assert requirement_statement(state, "rec_99") == ""
    state.mark_contradiction("rec_1", "rec_5")
    assert eligible_anchors(state) == ()


def test_chains_expose_active_replaced_and_withdrawn_anchor_deterministically():
    """A VALID current chain and a GENUINELY withdrawn chain, and nothing else.
    Only an anchor the ledger really superseded may present as withdrawn."""
    state = _state_with_answers()
    state.requirement_quantities = list(validate_quantity_history([
        _row(1, anchor="rec_2", text="3 A"),
        _row(2, anchor="rec_1", text="5 V"),
        _row(3, anchor="rec_1", text="6 V", supersedes=_qid(2)),
    ]))
    chains = quantity_chains(state)
    assert [(c.anchor_record_id, c.active.value_text, [r.value_text for r in c.replaced],
             c.anchor_active) for c in chains] == [
        ("rec_1", "6 V", ["5 V"], True), ("rec_2", "3 A", [], True)]
    # A GENUINE withdrawal through the governed correction path: rec_2 keeps its
    # rows and becomes a withdrawn-anchor chain; rec_1 stays current.
    state.record_interaction(DISPOSITION_ANSWERED, "corrected", iteration=4,
                             gap_context="MECHANISM_COMPLETENESS", supersedes=["rec_2"])
    chains = quantity_chains(state)
    assert [(c.anchor_record_id, c.anchor_active) for c in chains] == [
        ("rec_1", True), ("rec_2", False)]
    assert quantity_chains(state) == chains                      # deterministic
    assert quantity_chains(IdeaState(idea_id="empty")) == ()
    assert len(state.requirement_quantities) == 3                # nothing deleted


@pytest.mark.parametrize("label, anchor, mutate", [
    # An anchor that never existed in the ledger at all.
    ("nonexistent", "rec_9", None),
    # An existing record that was NEVER a valid answered assertion anchor
    # (recorded with a non-answered disposition).
    ("never-answered", "rec_3", None),
    # An existing answered record with empty content — never a valid anchor.
    ("empty-answer", "rec_4", None),
])
def test_unresolvable_anchors_never_render_as_withdrawn_history(label, anchor, mutate):
    """CR-1: a missing, never-answered or otherwise invalid anchor FAILS CLOSED
    on every derived surface. It is never presented as legitimate withdrawn
    history, and the durable row is neither repaired nor deleted."""
    state = _state_with_answers()
    rows = [_row(1, anchor="rec_1", text="5 V"), _row(2, anchor=anchor, text="1 kg")]
    state.requirement_quantities = list(validate_quantity_history(rows))
    assert classify_state_anchor(state, anchor) == ANCHOR_INVALID
    with pytest.raises(QuantityHistoryError):
        quantity_chains(state)
    with pytest.raises(QuantityHistoryError):
        requirement_quantities_meta(state)
    assert len(state.requirement_quantities) == 2                # untouched


def test_inconsistent_requirement_anchor_relationship_fails_closed():
    """CR-1: a requirement identity that is not the canonical
    ``req:assertion:<anchor>`` of the row's own anchor is rejected, and an
    anchor the ledger still calls active while the landscape derives no
    requirement for it is INVALID (inconsistent), never withdrawn."""
    with pytest.raises(QuantityHistoryError):
        validate_quantity_history([_row(1, anchor="rec_1",
                                        requirement_id="req:assertion:rec_2")])
    state = _state_with_answers()
    state.mark_contradiction("rec_1", "rec_2")     # landscape derives no assertion
    assert eligible_anchors(state) == ()
    assert classify_ledger_anchor(state.assertions, "rec_1") == ANCHOR_ACTIVE
    assert classify_state_anchor(state, "rec_1") == ANCHOR_INVALID
    state.requirement_quantities = list(validate_quantity_history([_row(1, anchor="rec_1")]))
    with pytest.raises(QuantityHistoryError):
        quantity_chains(state)


# --------------------------------------------------------------------------
# R3 — a supersession is withdrawn history ONLY when it is fully reciprocal
# --------------------------------------------------------------------------
def _corrected_state():
    """A state whose rec_2 was genuinely superseded through the governed
    correction path (rec_5.supersedes == ["rec_2"] and rec_2.superseded_by ==
    "rec_5" — both durable sides present)."""
    state = _state_with_answers()
    state.record_interaction(DISPOSITION_ANSWERED, "corrected mechanism text",
                             gap_context="MECHANISM_COMPLETENESS", iteration=4,
                             supersedes=["rec_2"])
    return state


def _record_of(state, record_id):
    return next(r for r in state.assertions if r.record_id == record_id)


def test_supersession_relations_are_built_from_the_forward_edge_only():
    """The durable forward edge (`successor.supersedes`) is the governed truth;
    `superseded_by` is load-derived and can be stale or one-sided, so it never
    manufactures its own evidence."""
    state = _corrected_state()
    forward, by_id = supersession_relations(state.assertions)
    assert forward == {"rec_2": "rec_5"}
    assert set(by_id) == {"rec_1", "rec_2", "rec_3", "rec_4", "rec_5"}
    # A record that only CLAIMS to be superseded contributes no forward edge.
    _record_of(state, "rec_1").superseded_by = "rec_5"
    forward, _ = supersession_relations(state.assertions)
    assert forward == {"rec_2": "rec_5"}
    # Two different successors naming one prior record leave no usable edge.
    state.record_interaction(DISPOSITION_ANSWERED, "second corrected text",
                             gap_context="MECHANISM_COMPLETENESS", iteration=5)
    _record_of(state, "rec_6").supersedes = ["rec_2"]
    forward, _ = supersession_relations(state.assertions)
    assert "rec_2" not in forward
    assert classify_ledger_anchor(state.assertions, "rec_2") == ANCHOR_INVALID


@pytest.mark.parametrize("label, corrupt", [
    # One-sided: the old record points forward, nothing points back.
    ("one-sided superseded_by",
     lambda st: setattr(_record_of(st, "rec_2"), "superseded_by", "rec_1")),
    # Reciprocal reference to the WRONG old record.
    ("reciprocal to the wrong record",
     lambda st: setattr(_record_of(st, "rec_2"), "superseded_by", "rec_1")),
    # The alleged successor does not exist at all.
    ("missing successor",
     lambda st: setattr(_record_of(st, "rec_2"), "superseded_by", "rec_404")),
    # Self-supersession.
    ("self supersession",
     lambda st: setattr(_record_of(st, "rec_2"), "superseded_by", "rec_2")),
])
def test_one_sided_or_inconsistent_supersession_is_invalid_not_withdrawn(label, corrupt):
    """R3: a non-null `superseded_by` is never sufficient on its own."""
    state = _state_with_answers()
    corrupt(state)
    assert classify_ledger_anchor(state.assertions, "rec_2") == ANCHOR_INVALID, label
    assert classify_state_anchor(state, "rec_2") == ANCHOR_INVALID, label
    state.requirement_quantities = list(validate_quantity_history([_row(1, anchor="rec_2")]))
    with pytest.raises(QuantityHistoryError):
        quantity_chains(state)
    with pytest.raises(QuantityHistoryError):
        requirement_quantities_meta(state)
    assert len(state.requirement_quantities) == 1          # retained, not erased


def test_a_cyclic_supersession_relationship_is_invalid_not_withdrawn():
    """R3: a cycle is never a genuine correction, on either side."""
    state = _corrected_state()
    assert classify_ledger_anchor(state.assertions, "rec_2") == ANCHOR_WITHDRAWN
    _record_of(state, "rec_5").supersedes = ["rec_2"]
    _record_of(state, "rec_2").supersedes = ["rec_5"]
    _record_of(state, "rec_5").superseded_by = "rec_2"
    assert classify_ledger_anchor(state.assertions, "rec_2") == ANCHOR_INVALID
    assert classify_ledger_anchor(state.assertions, "rec_5") == ANCHOR_INVALID


def test_valid_reciprocal_correction_remains_withdrawn_history_control():
    """R3 passing control: genuine withdrawal behaviour is preserved exactly."""
    state = _corrected_state()
    assert classify_ledger_anchor(state.assertions, "rec_2") == ANCHOR_WITHDRAWN
    assert classify_state_anchor(state, "rec_2") == ANCHOR_WITHDRAWN
    assert classify_state_anchor(state, "rec_1") == ANCHOR_ACTIVE
    state.requirement_quantities = list(validate_quantity_history([_row(1, anchor="rec_2")]))
    (chain,) = quantity_chains(state)
    assert (chain.anchor_record_id, chain.anchor_active) == ("rec_2", False)
    assert requirement_quantities_meta(state)["rows"][0]["anchor_active"] is False


# --------------------------------------------------------------------------
# R1 — a new event requires a CURRENTLY eligible durable anchor
# --------------------------------------------------------------------------
def test_a_new_event_against_a_withdrawn_anchor_is_refused_inside_the_transaction(store):
    """R1: durable truth controls. A new insertion or chain successor whose
    anchor the ledger no longer holds as eligible writes nothing, while an
    exact replay of an event recorded before the withdrawal stays idempotent
    and the historical row is untouched."""
    state = _project(store, "P1", answers=(PROBLEM, MECHANISM))
    first = _quantity(store, anchor="rec_2", event_key="b" * 32)
    assert store.append_requirement_quantity("P1", first) == QUANTITY_INSERTED
    # A genuine governed correction withdraws rec_2 durably.
    state.record_interaction(DISPOSITION_ANSWERED, "corrected mechanism text",
                             gap_context="MECHANISM_COMPLETENESS", iteration=2,
                             supersedes=["rec_2"])
    store.append_record("P1", _record_of(state, "rec_3"))
    assert classify_ledger_anchor(store._ledger_records("P1"), "rec_2") == ANCHOR_WITHDRAWN
    # A brand-new root event against the withdrawn anchor: refused.
    with pytest.raises(QuantityAnchorIneligible):
        store.append_requirement_quantity("P1", _quantity(store, anchor="rec_2", text="9 V"))
    # A chain SUCCESSOR against the withdrawn anchor: also refused.
    with pytest.raises(QuantityAnchorIneligible):
        store.append_requirement_quantity("P1", _quantity(
            store, anchor="rec_2", text="9 V", supersedes=first.quantity_id))
    rows = store.load_requirement_quantities("P1")
    assert [r.value_text for r in rows] == ["5 V"]          # history preserved
    assert rows[0].quantity_id == first.quantity_id
    # The exact event recorded BEFORE the withdrawal still replays idempotently.
    assert store.append_requirement_quantity(
        "P1", _quantity(store, anchor="rec_2", event_key="b" * 32)) == QUANTITY_EXACT_REPLAY
    assert len(store.load_requirement_quantities("P1")) == 1
    # An anchor that is still active accepts a new event normally.
    assert store.append_requirement_quantity(
        "P1", _quantity(store, anchor="rec_1", text="4 V")) == QUANTITY_INSERTED
    assert store._conn.execute("PRAGMA foreign_key_check").fetchall() == []


def test_genuinely_superseded_anchor_is_the_only_withdrawn_presentation():
    """CR-1: exactly one anchor state may present as withdrawn."""
    state = _state_with_answers()
    assert classify_state_anchor(state, "rec_2") == ANCHOR_ACTIVE
    state.record_interaction(DISPOSITION_ANSWERED, "corrected mechanism text",
                             gap_context="MECHANISM_COMPLETENESS", iteration=4,
                             supersedes=["rec_2"])
    assert classify_state_anchor(state, "rec_2") == ANCHOR_WITHDRAWN
    assert classify_ledger_anchor(state.assertions, "rec_2") == ANCHOR_WITHDRAWN
    assert classify_ledger_anchor(state.assertions, "rec_99") == ANCHOR_INVALID
    assert set(answered_anchor_index(state.assertions)) == {"rec_1", "rec_2", "rec_5"}
    state.requirement_quantities = list(validate_quantity_history([_row(1, anchor="rec_2")]))
    (chain,) = quantity_chains(state)
    assert (chain.anchor_record_id, chain.anchor_active) == ("rec_2", False)
    meta = requirement_quantities_meta(state)
    assert [(r["anchor_record_id"], r["anchor_active"]) for r in meta["rows"]] == [("rec_2", False)]


def test_history_is_validated_against_the_durable_ledger_assertions():
    """CR-1: quantity history is validated against the project's LEDGER
    assertions, not only against the other quantity rows."""
    state = _state_with_answers()
    rows = [_row(1, anchor="rec_1"), _row(2, anchor="rec_9", text="1 kg")]
    assert len(validate_quantity_history(rows)) == 2            # rows alone: valid
    with pytest.raises(QuantityHistoryError):                   # against the ledger: not
        validate_quantity_history(rows, assertions=state.assertions)
    assert len(validate_quantity_history([_row(1, anchor="rec_1")],
                                         assertions=state.assertions)) == 1
    for bad in ("rec_3", "rec_4"):        # unknown disposition / empty content
        with pytest.raises(QuantityHistoryError):
            validate_quantity_history([_row(1, anchor=bad)], assertions=state.assertions)


def test_package_rows_are_canonical_ordered_by_seq_and_absent_at_zero():
    state = _state_with_answers()
    assert requirement_quantities_meta(state) is None
    state.requirement_quantities = list(validate_quantity_history([
        _row(1, anchor="rec_1", text="5 V"),
        _row(2, anchor="rec_2", text="3 A"),
        _row(3, anchor="rec_1", kind=KIND2, text="6 V", supersedes=_qid(1), iteration=4),
    ]))
    state.record_interaction(DISPOSITION_ANSWERED, "corrected", iteration=4,
                             gap_context="MECHANISM_COMPLETENESS", supersedes=["rec_2"])
    meta = requirement_quantities_meta(state)
    assert set(meta) == {"total", "rows"} and meta["total"] == 3
    assert [set(r) for r in meta["rows"]] == [set(CANONICAL_ROW_FIELDS) | {"active", "anchor_active"}] * 3
    assert [(r["quantity_seq"], r["active"], r["anchor_active"]) for r in meta["rows"]] == [
        (1, False, True), (2, True, False), (3, True, True)]
    assert meta["rows"][2] == {
        "quantity_id": _qid(3), "quantity_seq": 3, "anchor_record_id": "rec_1",
        "requirement_id": "req:assertion:rec_1", "quantity_kind": KIND2, "value_text": "6 V",
        "supersedes_quantity_id": _qid(1), "event_key": _ek(3), "recorded_iteration": 4,
        "recorded_at": AT, "validation_status": "UNVALIDATED", "provenance": "OWNER_STATED",
        "active": True, "anchor_active": True}
    blob = json.dumps(meta)
    for forbidden in ("title", "note", "label", "statement", "Recorded by", "replaced"):
        assert forbidden not in blob
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
# 4. Durable store — schema, index set, migration, append, cap, chain rule
# ==========================================================================
def test_fresh_database_creates_the_exact_table_index_set_and_composite_foreign_keys(store):
    conn = store._conn
    tables = sorted(r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"))
    assert tables == ["projects", "records", "requirement_quantities"]
    cols = [r[1] for r in conn.execute("PRAGMA table_info(requirement_quantities)")]
    assert cols == ["project_id", "quantity_seq", "quantity_id", "anchor_record_id",
                    "requirement_id", "quantity_kind", "value_text",
                    "supersedes_quantity_id", "event_key", "recorded_iteration",
                    "recorded_at"]
    by_id = {}
    for fk in conn.execute("PRAGMA foreign_key_list(requirement_quantities)"):
        by_id.setdefault((fk[0], fk[2]), []).append((fk[3], fk[4]))
    assert sorted(sorted(v) for v in by_id.values()) == sorted(sorted(v) for v in [
        [("project_id", "project_id")],
        [("project_id", "project_id"), ("anchor_record_id", "record_id")],
        [("project_id", "project_id"), ("supersedes_quantity_id", "quantity_id")],
    ])
    assert {t for (_i, t) in by_id} == {"projects", "records", "requirement_quantities"}
    indexes = {r[1]: bool(r[2]) for r in conn.execute("PRAGMA index_list(requirement_quantities)")}
    assert indexes == {
        "sqlite_autoindex_requirement_quantities_1": True,      # PK (project_id, quantity_id)
        "requirement_quantities_event_key_uq": True,
        "requirement_quantities_seq_uq": True,
        "requirement_quantities_supersedes_uq": True,
        "requirement_quantities_chain_root_uq": True,
        "requirement_quantities_anchor_idx": False,
    }
    sql = {r[0]: r[1] for r in conn.execute(
        "SELECT name, sql FROM sqlite_master WHERE tbl_name = 'requirement_quantities' "
        "AND type = 'index' AND sql IS NOT NULL")}
    assert "WHERE supersedes_quantity_id IS NULL" in sql["requirement_quantities_chain_root_uq"]
    assert "WHERE supersedes_quantity_id IS NOT NULL" in sql["requirement_quantities_supersedes_uq"]
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    assert isinstance(store, RecordStore)


def test_direct_sqlite_proofs_of_the_relational_constraints(store):
    _project(store, "P1")
    _project(store, "P2")
    conn = store._conn
    _raw_insert(store, "P1", 0, _qid(1), "rec_1", None, "a" * 32)
    with pytest.raises(sqlite3.IntegrityError):         # a second root for one anchor
        _raw_insert(store, "P1", 1, _qid(2), "rec_1", None, "b" * 32)
    _raw_insert(store, "P1", 1, _qid(2), "rec_1", _qid(1), "b" * 32)
    with pytest.raises(sqlite3.IntegrityError):         # a second successor for one quantity
        _raw_insert(store, "P1", 2, _qid(3), "rec_1", _qid(1), "c" * 32)
    with pytest.raises(sqlite3.IntegrityError):         # cross-project anchor (rec_1 of P1 only)
        _raw_insert(store, "P1", 2, _qid(3), "rec_9", None, "c" * 32)
    with pytest.raises(sqlite3.IntegrityError):         # cross-project supersession
        _raw_insert(store, "P2", 0, _qid(4), "rec_1", _qid(1), "d" * 32)
    with pytest.raises(sqlite3.IntegrityError):         # orphan project
        _raw_insert(store, "NOPE", 0, _qid(5), "rec_1", None, "e" * 32)
    with pytest.raises(sqlite3.IntegrityError):         # duplicate event key (project-scoped)
        _raw_insert(store, "P1", 2, _qid(6), "rec_1", _qid(2), "a" * 32)
    with pytest.raises(sqlite3.IntegrityError):         # duplicate sequence
        _raw_insert(store, "P1", 1, _qid(7), "rec_1", _qid(2), "f" * 32)
    assert conn.execute("PRAGMA foreign_key_check").fetchall() == []
    assert [q.value_text for q in store.load_requirement_quantities("P1")] == ["9 V", "9 V"]
    assert len(active_quantities(store.load_requirement_quantities("P1"))) == 1
    assert store.load_requirement_quantities("P2") == ()


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
    s = SqliteRecordStore(path)
    try:
        assert s.load_requirement_quantities("legacy") == ()
        assert s.load_owner("legacy") == (True, "acct_1")
        s.append_requirement_quantity("legacy", _quantity(s))
        assert s._conn.execute("PRAGMA foreign_key_check").fetchall() == []
        idx = {r[1] for r in s._conn.execute("PRAGMA index_list(requirement_quantities)")}
        assert {"requirement_quantities_chain_root_uq", "requirement_quantities_anchor_idx"} <= idx
    finally:
        s.close()
    s2 = SqliteRecordStore(path)
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
    q1 = _quantity(s, text="5 V", event_key="a" * 32, iteration=2)
    s.append_requirement_quantity("P1", q1)
    q2 = _quantity(s, kind=KIND2, text="6.5   V", supersedes=q1.quantity_id,
                   event_key="b" * 32, iteration=3, at="2026-09-11T13:00:00+00:00")
    s.append_requirement_quantity("P1", q2)
    s.close()
    s = SqliteRecordStore(path)
    try:
        history = s.load_requirement_quantities("P1")
        assert history == (
            RequirementQuantity(q1.quantity_id, 0, "rec_1", "req:assertion:rec_1", KIND, "5 V",
                                None, "a" * 32, 2, AT),
            RequirementQuantity(q2.quantity_id, 1, "rec_1", "req:assertion:rec_1", KIND2,
                                "6.5   V", q1.quantity_id, "b" * 32, 3,
                                "2026-09-11T13:00:00+00:00"))
        assert s.requirement_quantity_for_event_key("P1", "b" * 32) == {
            "quantity_seq": 1, "quantity_id": q2.quantity_id, "anchor_record_id": "rec_1",
            "requirement_id": "req:assertion:rec_1", "quantity_kind": KIND2,
            "value_text": "6.5   V", "supersedes_quantity_id": q1.quantity_id,
            "event_key": "b" * 32, "recorded_iteration": 3,
            "recorded_at": "2026-09-11T13:00:00+00:00"}
        assert s.requirement_quantity_for_event_key("P1", "nope") is None
        assert s.requirement_quantity_for_event_key("P1", None) is None
        assert s.requirement_quantity_for_event_key("P2", "b" * 32) is None
    finally:
        s.close()


def test_one_active_chain_and_stale_head_are_enforced_inside_the_transaction(store):
    _project(store, "P1")
    q1 = _quantity(store)
    store.append_requirement_quantity("P1", q1)
    with pytest.raises(QuantityChainConflict):          # second active row
        store.append_requirement_quantity("P1", _quantity(store, text="6 V"))
    q2 = _quantity(store, text="6 V", supersedes=q1.quantity_id)
    store.append_requirement_quantity("P1", q2)
    with pytest.raises(QuantityChainConflict):          # stale head (q1 already replaced)
        store.append_requirement_quantity(
            "P1", _quantity(store, text="7 V", supersedes=q1.quantity_id))
    with pytest.raises(QuantityChainConflict):          # unknown target
        store.append_requirement_quantity(
            "P1", _quantity(store, text="7 V", supersedes=_qid(99)))
    with pytest.raises(QuantityChainConflict):          # requirement id drift in a chain
        store.append_requirement_quantity(
            "P1", _quantity(store, text="7 V", supersedes=q2.quantity_id,
                            requirement_id="req:other"))
    assert issubclass(QuantityChainConflict, StoreError)
    history = store.load_requirement_quantities("P1")
    assert len(history) == 2 and active_quantities(history)["rec_1"].quantity_id == q2.quantity_id


def test_unique_event_key_is_the_durable_exact_replay_backstop(store):
    """CR-4: the stable event key is resolved BEFORE chain position. The exact
    same canonical event replays idempotently; a DIFFERENT event reusing the
    key is a conflict/rejection that writes nothing."""
    _project(store, "P1", answers=(PROBLEM, MECHANISM))
    first = _quantity(store, event_key="a" * 32)
    assert store.append_requirement_quantity("P1", first) == QUANTITY_INSERTED
    # The identical canonical event again: recognised as the SAME event, not
    # classified as a second chain root for an anchor that already has one.
    replay = _quantity(store, event_key="a" * 32)
    assert store.append_requirement_quantity("P1", replay) == QUANTITY_EXACT_REPLAY
    # A DIFFERENT event under the same key stays a conflict; nothing is written.
    with pytest.raises(QuantityChainConflict):
        store.append_requirement_quantity(
            "P1", _quantity(store, anchor="rec_2", event_key="a" * 32))
    rows = store.load_requirement_quantities("P1")
    assert len(rows) == 1 and rows[0].quantity_id == first.quantity_id
    _project(store, "P2")
    assert store.append_requirement_quantity(
        "P2", _quantity(store, event_key="a" * 32)) == QUANTITY_INSERTED
    assert len(store.load_requirement_quantities("P2")) == 1
    store._conn.execute("BEGIN IMMEDIATE")
    store._conn.execute("ROLLBACK")


def test_direct_store_caller_cannot_commit_an_invalid_canonical_row(store):
    """CR-1: the PROPOSED row is validated together with the existing history
    INSIDE the write transaction, so no direct caller can commit an invalid
    kind, a malformed generated identity, an inconsistent requirement identity
    or an invalid anchor relationship."""
    _project(store, "P1", answers=(PROBLEM, MECHANISM))
    invalid = {
        "invalid kind": _quantity(store, kind="bogus_kind"),
        "malformed quantity id": dataclasses.replace(
            _quantity(store), quantity_id="not-a-quantity-id"),
        "malformed event key": _quantity(store, event_key="ZZZ"),
        "inconsistent requirement id": _quantity(
            store, requirement_id="req:assertion:rec_2"),
        "nonexistent anchor": _quantity(store, anchor="rec_9"),
        "malformed anchor id": _quantity(store, anchor="record-one"),
        "unstored value text": _quantity(store, text="  5 V  "),
        "malformed recorded_at": _quantity(store, at="not-a-timestamp"),
    }
    for label, candidate in invalid.items():
        with pytest.raises((QuantityHistoryError, StoreError, sqlite3.IntegrityError)), \
                pytest.MonkeyPatch.context():
            store.append_requirement_quantity("P1", candidate)
        assert store.load_requirement_quantities("P1") == (), label
        assert store._conn.execute(
            "SELECT COUNT(*) FROM requirement_quantities").fetchone()[0] == 0, label
    # A supersession edge naming ANOTHER anchor's row is refused as well.
    assert store.append_requirement_quantity("P1", _quantity(store)) == QUANTITY_INSERTED
    head = store.load_requirement_quantities("P1")[0]
    with pytest.raises((QuantityChainConflict, QuantityHistoryError)):
        store.append_requirement_quantity(
            "P1", _quantity(store, anchor="rec_2", supersedes=head.quantity_id))
    assert len(store.load_requirement_quantities("P1")) == 1


def test_anchor_that_is_not_a_valid_answered_record_fails_closed_on_load(store):
    """CR-1: a durable row whose anchor does not resolve to a valid answered
    assertion record of THIS project is corruption. It fails closed on load and
    blocks further writes; it is never silently repaired, deleted or served."""
    _project_with_a_non_answer(store, "P1")
    assert store.append_requirement_quantity("P1", _quantity(store)) == QUANTITY_INSERTED
    _point_anchor_at(store, "P1", "rec_2")      # exists, but never an answered anchor
    with pytest.raises(QuantityHistoryError):
        store.load_requirement_quantities("P1")
    with pytest.raises(QuantityHistoryError):
        store.append_requirement_quantity("P1", _quantity(store))
    assert store._conn.execute(
        "SELECT COUNT(*) FROM requirement_quantities").fetchone()[0] == 1   # retained
    # Relational integrity is intact — this corruption is SEMANTIC, which is
    # exactly why a foreign key alone cannot catch it and the ledger check must.
    assert store._conn.execute("PRAGMA foreign_key_check").fetchall() == []


def test_unrelated_project_is_isolated_from_another_projects_corruption(store):
    """CR-1: corruption and anchor resolution are strictly project-scoped."""
    _project_with_a_non_answer(store, "P1")
    _project(store, "P2", answers=(PROBLEM, MECHANISM))
    assert store.append_requirement_quantity("P1", _quantity(store)) == QUANTITY_INSERTED
    assert store.append_requirement_quantity("P2", _quantity(store, text="9 A")) == QUANTITY_INSERTED
    _point_anchor_at(store, "P1", "rec_2")
    with pytest.raises(QuantityHistoryError):
        store.load_requirement_quantities("P1")
    assert [r.value_text for r in store.load_requirement_quantities("P2")] == ["9 A"]
    assert store.append_requirement_quantity(
        "P2", _quantity(store, anchor="rec_2", text="4 V")) == QUANTITY_INSERTED
    assert [r.value_text for r in store.load_requirement_quantities("P2")] == ["9 A", "4 V"]
    assert store._conn.execute("PRAGMA foreign_key_check").fetchall() == []


def test_pragma_foreign_key_check_stays_empty_across_the_whole_lifecycle(store):
    """CR-1: relational integrity holds after every accepted and refused
    operation — inserts, a correction chain, refusals and a second project."""
    _project(store, "P1", answers=(PROBLEM, MECHANISM))
    _project(store, "P2", answers=(PROBLEM,))
    store.append_requirement_quantity("P1", _quantity(store))
    head = store.load_requirement_quantities("P1")[0]
    store.append_requirement_quantity(
        "P1", _quantity(store, text="6 V", supersedes=head.quantity_id))
    store.append_requirement_quantity("P1", _quantity(store, anchor="rec_2", text="3 A"))
    store.append_requirement_quantity("P2", _quantity(store, text="1 A"))
    for bad in (_quantity(store, anchor="rec_9"), _quantity(store, kind="bogus"),
                _quantity(store, text="   ")):
        with pytest.raises((QuantityHistoryError, StoreError, QuantityValueError)):
            store.append_requirement_quantity("P1", bad)
    assert store._conn.execute("PRAGMA foreign_key_check").fetchall() == []
    assert len(store.load_requirement_quantities("P1")) == 3
    assert len(store.load_requirement_quantities("P2")) == 1


def test_unknown_project_and_wrong_type_write_nothing(store):
    with pytest.raises(ProjectNotFound):
        store.append_requirement_quantity("missing", _quantity(store))
    _project(store, "P1")
    with pytest.raises(StoreError):
        store.append_requirement_quantity("P1", {"not": "a quantity"})
    assert store._conn.execute("SELECT COUNT(*) FROM requirement_quantities").fetchone()[0] == 0
    assert store.load_requirement_quantities("missing") == ()


@pytest.mark.parametrize("attempts,expect_last_ok", [(199, True), (200, True), (201, False)])
def test_per_project_cap_at_199_200_and_201_attempts(store, attempts, expect_last_ok):
    _project(store, "P1")
    head = None
    ok = 0
    failed = 0
    for _ in range(attempts):
        q = _quantity(store, text="v %d" % ok, supersedes=head)
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
    _project(store, "P2")
    store.append_requirement_quantity("P2", _quantity(store))


def test_project_isolation_across_projects(store):
    _project(store, "A")
    _project(store, "B")
    store.append_requirement_quantity("A", _quantity(store, event_key="a" * 32))
    store.append_requirement_quantity("B", _quantity(store, kind=KIND2, text="9 A",
                                                     event_key="a" * 32))
    assert [q.value_text for q in store.load_requirement_quantities("A")] == ["5 V"]
    assert [q.value_text for q in store.load_requirement_quantities("B")] == ["9 A"]
    assert store.requirement_quantity_for_event_key("B", "a" * 32)["value_text"] == "9 A"
    assert store._conn.execute("PRAGMA foreign_key_check").fetchall() == []


@pytest.mark.parametrize("sql", [
    "UPDATE requirement_quantities SET value_text = ' 5 V'",
    "UPDATE requirement_quantities SET quantity_kind = 'tolerance'",
    "UPDATE requirement_quantities SET requirement_id = 'req:assertion:rec_2'",
    "UPDATE requirement_quantities SET event_key = 'zz' WHERE quantity_seq = 0",
    "UPDATE requirement_quantities SET quantity_seq = 5 WHERE quantity_seq = 0",
    "UPDATE requirement_quantities SET recorded_at = 'x' WHERE quantity_seq = 1",
    "UPDATE requirement_quantities SET recorded_iteration = -1 WHERE quantity_seq = 1",
])
def test_tampered_history_fails_closed_on_load_and_blocks_writes_inside_the_transaction(store, sql):
    _project(store, "P1")
    q1 = _quantity(store)
    store.append_requirement_quantity("P1", q1)
    q2 = _quantity(store, text="6 V", supersedes=q1.quantity_id)
    store.append_requirement_quantity("P1", q2)
    _project(store, "P2")
    store.append_requirement_quantity("P2", _quantity(store, text="1 mm"))
    with store._write():
        store._conn.execute("PRAGMA foreign_keys = OFF")
        store._conn.execute(sql + (" AND project_id = 'P1'" if "WHERE" in sql
                                   else " WHERE project_id = 'P1'"))
        store._conn.execute("PRAGMA foreign_keys = ON")
    with pytest.raises(QuantityHistoryError):
        store.load_requirement_quantities("P1")
    with pytest.raises(QuantityHistoryError):
        store.append_requirement_quantity(
            "P1", _quantity(store, text="7 V", supersedes=q2.quantity_id))
    assert store._conn.execute(
        "SELECT COUNT(*) FROM requirement_quantities WHERE project_id = 'P1'").fetchone()[0] == 2
    assert [q.value_text for q in store.load_requirement_quantities("P2")] == ["1 mm"]
    store._conn.execute("BEGIN IMMEDIATE")
    store._conn.execute("ROLLBACK")


def test_storage_unavailability_propagates_instead_of_returning_empty(store):
    _project(store, "P1")
    store.append_requirement_quantity("P1", _quantity(store))
    store.close()
    with pytest.raises(sqlite3.ProgrammingError):
        store.load_requirement_quantities("P1")
    store._conn = sqlite3.connect(":memory:")


# ==========================================================================
# 5. Backup / restore parity includes the additive history
# ==========================================================================
def test_backup_restore_parity_carries_the_complete_quantity_rows(tmp_path):
    source = str(tmp_path / "live.sqlite")
    s = SqliteRecordStore(source)
    _project(s, "P1")
    q1 = _quantity(s)
    s.append_requirement_quantity("P1", q1)
    s.append_requirement_quantity("P1", _quantity(s, text="7 V", supersedes=q1.quantity_id,
                                                  iteration=4))
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
        assert restored.load_requirement_quantities("P1") == \
            SqliteRecordStore(source).load_requirement_quantities("P1")
        assert [(q.value_text, q.supersedes_quantity_id, q.recorded_iteration, q.recorded_at)
                for q in restored.load_requirement_quantities("P1")] == [
            ("5 V", None, 1, AT), ("7 V", q1.quantity_id, 4, AT)]
        assert restored._conn.execute("PRAGMA foreign_key_check").fetchall() == []
    finally:
        restored.close()
    assert backup_service.validate_sqlite_database(
        backup, required_tables=("projects", "records", "requirement_quantities"))
    assert os.path.getsize(backup) > 0
