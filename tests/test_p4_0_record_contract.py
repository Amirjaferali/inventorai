"""P4-0 — Readiness and Storage-Contract Proof (RED/GREEN).

Behavior-based tests for the datastore-neutral, versioned record contract
(`engine.record_contract`). Governed by the P4-0 Increment Contract Candidate
in `docs/governance/ACTIVE_INCREMENT_CONTRACT.md` (G-P4-0-DOC-01, merged
PR #352). These tests assert real round-trip/invariant BEHAVIOR via the
intended contract API; they are NOT satisfied by import success, dictionary
shape alone, an empty/NotImplementedError stub, empty fixtures, cached
readiness, or a datastore-specific model. Provider-free and DB-free.

Scope limit: P4-0 proves that readiness-relevant contract data survives
round-trip and can seed a FRESH `derive_readiness` call. P4-0 does NOT prove
full deterministic replay from accepted source inputs (that is P4-2).
"""
import dataclasses
import json

import pytest

from engine.idea_state import (
    AssertionRecord,
    IdeaState,
    OWNER_STATED,
    LEGACY_UNSPECIFIED,
    UNVALIDATED,
    INDEPENDENTLY_VERIFIED,
    REASONED,
)
from engine.derived_readiness import derive_readiness

# The intended P4-0 contract API. Absent until GREEN — RED tests fail because
# this behavior/capability does not yet exist (not merely because a file is
# absent): each test below still fails against an empty or NotImplementedError
# stub, since it asserts concrete round-trip/invariant behavior.
from engine.record_contract import (
    ProjectRecordContract,
    CONTRACT_VERSION,
    UnknownVersionError,
    UnknownFieldError,
    InvalidReferenceError,
    RelationshipCycleError,
    assertion_to_dict,
)

# Independent expected set of AssertionRecord's authoritative fields. Declared
# HERE (not imported from record_contract's own _ASSERTION_FIELDS) so the
# completeness guard cross-checks the contract against the authoritative
# dataclass, not against the implementation's own constant. A new authoritative
# field on AssertionRecord must break this test until the contract handles it.
_EXPECTED_ASSERTION_FIELDS = frozenset({
    "record_id", "disposition", "content", "gap_context", "iteration",
    "provenance", "validation_status", "quality", "pending", "responsibility",
    "resolves_gap", "contradicts", "supersedes", "superseded_by",
    # W2-A / RVR-4 (authoritative contract §3/§4, PR #567): deliberate
    # 15th authoritative field — explicit decision-context attachment. The
    # contract handles it with the bounded legacy load rule (a legacy payload
    # missing ONLY this field loads with None); see
    # tests/test_w2a_rvr4_contract_compat.py. This guard fired exactly as
    # designed and is reconciled here deliberately, additively.
    "decision_context_root",
})


# --- Non-trivial fixture (idea_state only; no contract dependency) -----------
def sample_state():
    """A non-trivial IdeaState: 5 append-only records, two gap contexts, two
    provenance values (OWNER_STATED, LEGACY_UNSPECIFIED), two validation values
    (INDEPENDENTLY_VERIFIED, UNVALIDATED), one supersession, one contradiction,
    stable identifiers."""
    st = IdeaState(idea_id="idea-p4-0-001")
    r1 = st.record_interaction("answered", content="problem stated",
                               gap_context="problem", iteration=1)   # OWNER_STATED
    r1.validation_status = INDEPENDENTLY_VERIFIED
    st.record_interaction("deferred", content="",
                          gap_context="mechanism", iteration=2)       # LEGACY_UNSPECIFIED, UNVALIDATED
    r3 = st.record_interaction("answered", content="old mechanism",
                               gap_context="mechanism", iteration=3)
    r3.validation_status = INDEPENDENTLY_VERIFIED
    r4 = st.record_interaction("answered", content="new mechanism",
                               gap_context="mechanism", iteration=4)
    r4.validation_status = INDEPENDENTLY_VERIFIED
    st.mark_supersession(r3.record_id, r4.record_id)                  # supersession link
    r5 = st.record_interaction("answered", content="conflicting problem view",
                               gap_context="problem", iteration=5)
    r5.validation_status = INDEPENDENTLY_VERIFIED
    st.mark_contradiction(r1.record_id, r5.record_id)                 # contradiction link
    return st


def _dumped(state):
    return json.loads(ProjectRecordContract.from_state(state).to_json())


# --- RED-1: lossless authoritative round-trip --------------------------------
def test_red1_authoritative_roundtrip_is_lossless():
    st = sample_state()
    contract = ProjectRecordContract.from_state(st)
    restored = ProjectRecordContract.from_dict(json.loads(contract.to_json()))
    assert restored.idea_id == st.idea_id
    assert len(restored.assertions) == len(st.assertions) == 5
    # Exhaustive per-field, per-record equality (not shape-only).
    fields = ("record_id", "disposition", "content", "gap_context", "iteration",
              "provenance", "validation_status", "quality", "pending",
              "responsibility", "resolves_gap", "contradicts", "supersedes",
              "superseded_by")
    for orig, back in zip(st.assertions, restored.assertions):
        for f in fields:
            assert getattr(back, f) == getattr(orig, f), f
    # JSON-compatible: the dumped form must be plain json.
    assert isinstance(contract.to_json(), str)


# --- RED-2: provenance + validation preserved verbatim -----------------------
def test_red2_provenance_and_validation_preserved_verbatim():
    st = sample_state()
    provs = {r.record_id: r.provenance for r in st.assertions}
    vals = {r.record_id: r.validation_status for r in st.assertions}
    assert OWNER_STATED in provs.values()
    assert LEGACY_UNSPECIFIED in provs.values()
    assert UNVALIDATED in vals.values()
    assert INDEPENDENTLY_VERIFIED in vals.values()
    restored = ProjectRecordContract.from_dict(_dumped(st))
    for r in restored.assertions:
        assert r.provenance == provs[r.record_id]
        assert r.validation_status == vals[r.record_id]


# --- RED-3: post-restore relationship validation -----------------------------
def test_red3_valid_links_preserved_and_invalid_refs_rejected():
    st = sample_state()
    restored = ProjectRecordContract.from_dict(_dumped(st))
    by_id = {r.record_id: r for r in restored.assertions}
    assert by_id["rec_3"].superseded_by == "rec_4"
    assert "rec_3" in by_id["rec_4"].supersedes
    assert "rec_5" in by_id["rec_1"].contradicts
    assert "rec_1" in by_id["rec_5"].contradicts
    # Unknown supersession reference must fail explicitly.
    blob = _dumped(st)
    blob["assertions"][0]["superseded_by"] = "rec_999"
    with pytest.raises(InvalidReferenceError):
        ProjectRecordContract.from_dict(blob)
    # Unknown contradiction reference must fail explicitly.
    blob2 = _dumped(st)
    blob2["assertions"][0]["contradicts"] = ["rec_999"]
    with pytest.raises(InvalidReferenceError):
        ProjectRecordContract.from_dict(blob2)


def test_red3_self_supersession_and_cycle_rejected():
    st = sample_state()
    # self-supersession
    blob = _dumped(st)
    blob["assertions"][0]["superseded_by"] = blob["assertions"][0]["record_id"]
    with pytest.raises((InvalidReferenceError, RelationshipCycleError)):
        ProjectRecordContract.from_dict(blob)
    # 2-cycle: rec_1 -> rec_2 -> rec_1 via superseded_by
    blob2 = _dumped(st)
    idx = {d["record_id"]: d for d in blob2["assertions"]}
    idx["rec_1"]["superseded_by"] = "rec_2"
    idx["rec_2"]["superseded_by"] = "rec_1"
    with pytest.raises(RelationshipCycleError):
        ProjectRecordContract.from_dict(blob2)


# --- RED-4: fresh readiness derivation after restore (NOT cached) ------------
def test_red4_fresh_readiness_derivation_after_restore():
    st = sample_state()
    contract = ProjectRecordContract.from_state(st)
    blob = contract.to_json()
    restored_state = ProjectRecordContract.from_json(blob).to_state()
    orig = derive_readiness(st)
    fresh = derive_readiness(restored_state)
    assert fresh.overall_verified() == orig.overall_verified()
    for ctx in ("problem", "mechanism"):
        assert fresh.is_verified(ctx) == orig.is_verified(ctx)
    # No cached readiness may be serialized or restored as authoritative.
    payload = json.loads(blob)
    assert "readiness" not in payload
    assert "overall_verified" not in blob
    assert "is_verified" not in blob


# --- RED-5: unknown-field governance (no silent drop) ------------------------
def test_red5_unknown_fields_rejected_not_silently_dropped():
    st = sample_state()
    blob = _dumped(st)
    blob["assertions"][0]["surprise_field"] = "x"
    with pytest.raises(UnknownFieldError):
        ProjectRecordContract.from_dict(blob)
    blob2 = _dumped(st)
    blob2["surprise_top_level"] = "y"
    with pytest.raises(UnknownFieldError):
        ProjectRecordContract.from_dict(blob2)


# --- RED-6: unknown contract version rejected --------------------------------
def test_red6_unknown_contract_version_rejected():
    st = sample_state()
    good = _dumped(st)
    assert good["contract_version"] == CONTRACT_VERSION
    bad = dict(good, contract_version="p4-0-record-contract-v999")
    with pytest.raises(UnknownVersionError):
        ProjectRecordContract.from_dict(bad)
    missing = {k: v for k, v in good.items() if k != "contract_version"}
    with pytest.raises(UnknownVersionError):
        ProjectRecordContract.from_dict(missing)


# --- Append-only preservation (count/order/ids/superseded history) -----------
def test_appendonly_history_preserved_through_roundtrip():
    st = sample_state()
    restored = ProjectRecordContract.from_dict(_dumped(st))
    assert [r.record_id for r in restored.assertions] == \
           [r.record_id for r in st.assertions]
    # the superseded record remains present (not collapsed/removed)
    assert any(r.record_id == "rec_3" and r.superseded_by == "rec_4"
               for r in restored.assertions)


# ============================================================================
# RC-1 (independent-review verdict C) — test-only authoritative-value coverage.
# The prior fixture never exercised non-default pending/quality/resolves_gap, so
# an implementation hardcoding pending=None/quality=None/resolves_gap=False
# could still pass. These tests close that false-green gap and add a
# dataclass-based field-completeness guard. No production code is changed.
# ============================================================================
def _state_with_nondefault_pending_and_quality():
    """A state that additionally exercises non-default pending and quality via
    the real runtime API: specialist_requested -> pending 'specialist';
    evidence_requested -> pending 'evidence'; plus a non-None quality."""
    st = sample_state()
    r6 = st.record_interaction("specialist_requested",
                               gap_context="mechanism", iteration=6)
    r7 = st.record_interaction("evidence_requested",
                               gap_context="mechanism", iteration=7)
    # Sanity: the runtime API itself produced non-default pending values.
    assert r6.pending == "specialist"
    assert r7.pending == "evidence"
    r6.quality = REASONED   # non-default (non-None) quality
    return st, r6.record_id, r7.record_id


def test_rc1_nondefault_pending_and_quality_roundtrip():
    st, r6_id, r7_id = _state_with_nondefault_pending_and_quality()
    restored = ProjectRecordContract.from_dict(_dumped(st))
    by_id = {r.record_id: r for r in restored.assertions}
    # non-default pending survives exactly
    assert by_id[r6_id].pending == "specialist"
    assert by_id[r7_id].pending == "evidence"
    # non-default quality survives exactly
    assert by_id[r6_id].quality == REASONED
    # and the default (None) values elsewhere are preserved as None, not coerced
    assert by_id["rec_1"].pending is None
    assert by_id["rec_1"].quality is None


def test_rc1_resolves_gap_true_survives_via_contract_api():
    # The public IdeaState construction path always yields resolves_gap=False,
    # so per the contract this field is proved through a valid serialized record
    # dictionary passed through the governed contract API.
    blob = _dumped(sample_state())
    assert blob["assertions"][0]["resolves_gap"] is False   # default baseline
    blob["assertions"][0]["resolves_gap"] = True
    restored = ProjectRecordContract.from_dict(blob)
    assert restored.assertions[0].resolves_gap is True
    # survives a further serialize/restore round-trip unchanged
    again = ProjectRecordContract.from_json(
        ProjectRecordContract(idea_id=restored.idea_id,
                              assertions=restored.assertions).to_json())
    assert again.assertions[0].resolves_gap is True
    # untouched records keep the default exactly
    assert again.assertions[1].resolves_gap is False


def test_rc1_field_completeness_guard_matches_authoritative_dataclass():
    """Independent completeness guard: compare the AUTHORITATIVE dataclass field
    names (dataclasses.fields(AssertionRecord)) against the expected set and the
    contract's serialized keys. A new authoritative field added to
    AssertionRecord must fail this test until the contract deliberately handles
    it — preventing a future field from being silently omitted while green."""
    actual = {f.name for f in dataclasses.fields(AssertionRecord)}
    # 1) authoritative dataclass == the independently-declared expected set
    assert actual == _EXPECTED_ASSERTION_FIELDS, (
        "AssertionRecord authoritative fields changed (symmetric difference: "
        "%s); update engine/record_contract.py and this proof deliberately."
        % sorted(actual ^ _EXPECTED_ASSERTION_FIELDS))
    # 2) the contract's serialization covers exactly the authoritative fields
    sample = sample_state().assertions[0]
    assert set(assertion_to_dict(sample)) == actual, (
        "contract serialization keys do not match AssertionRecord fields")
