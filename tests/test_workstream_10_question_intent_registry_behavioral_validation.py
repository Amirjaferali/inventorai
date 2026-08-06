"""
test_workstream_10_question_intent_registry_behavioral_validation.py
Workstream 10 — Behavioral Validation BASE RED (D33).

Governance basis (merged, authoritative):
    docs/governance/WORKSTREAM_10_V1_RECORD_SHAPE_OWNER_DECISIONS.md            (D1–D17)
    docs/governance/WORKSTREAM_10_LOADER_INTERFACE_AND_BASE_RED_SEQUENCE_OWNER_DECISIONS.md (D18–D33)

Purpose (D33):
    Deterministic BASE RED for the approved BEHAVIORAL registry-loading and
    validation contract, exercised through the REAL public seam:

        load_question_intent_registry(registry_path, source_artifact_path)
            -> QuestionIntentRegistry
        QuestionIntentRegistry.get(question_id) / .list_records()

    Behavior is driven by TEMPORARY registry + source-artifact files (pytest
    tmp_path); the committed repository artifacts are never written. Private
    internals are not constructed — behavior is proven only through the public
    loader and the returned public object.

Controlled-RED discipline (D31/D33 quality requirements):
    The merged Minimal Interface GREEN loader is a fail-loud bounded placeholder
    that raises QuestionIntentRegistryLoadError(reason_code="MINIMAL_INTERFACE_
    PLACEHOLDER") for every call. Each test therefore fails NOW for the intended
    missing behavioral capability, surfaced as a clear, decision-tagged failure:
      * positive-behavior tests call the seam and, if the placeholder is still in
        place, fail with a "successful loading not implemented" message
        (_load_or_red);
      * validation tests assert the SPECIFIC approved D26 reason_code and fail
        because the placeholder returns the placeholder code instead
        (_expect_load_error).
    A mere `pytest.raises(placeholder)` is deliberately NOT used; the suite encodes
    the required future successful-loading and validation behavior.

Scope: no production code, existing test, governance doc, source artifact, or
registry JSON/schema is modified. No import-time registry I/O is introduced
(fixtures are built inside tests). engine.question_intent_registry already exists
(Minimal Interface GREEN merged), so it is imported at module scope.
"""

import json
import pathlib

import pytest

from engine.question_intent_registry import (
    load_question_intent_registry,
    QuestionIntentRegistry,
    QuestionIntentRegistryLoadError,
    QuestionIntentNotFoundError,
)

_PLACEHOLDER = "MINIMAL_INTERFACE_PLACEHOLDER"

# The ten ratified D26 reason codes (the only approved behavioral taxonomy).
_APPROVED_REASON_CODES = frozenset({
    "MISSING_REQUIRED_FIELD", "DUPLICATE_QUESTION_ID", "DUPLICATE_INTENT_ID",
    "INVALID_DESIGN_GAP_ID", "INVALID_METADATA", "SOURCE_ID_SET_MISMATCH",
    "SOURCE_REFERENCE_MISMATCH", "INVALID_SOURCE_ARTIFACT_PATH", "INVALID_JSON",
    "FILE_READ_ERROR",
})

# Canonical design gaps (D5) and the required record fields (D3).
_GAPS = ("MECHANISM_COMPLETENESS", "PHYSICAL_FEASIBILITY", "BOUNDARY_AMBIGUITY")
_REQUIRED_RECORD_FIELDS = (
    "question_id", "intent_id", "design_gap_id", "primary_intent",
    "answer_objective", "completion_condition", "source_reference",
)

# A small self-consistent source artifact in committed source order
# (gap-group order, then question order within each group — D29).
_SOURCE_QUESTIONS = (
    ("MECHANISM_COMPLETENESS", "N-MC-1", "How does it notice the problem?"),
    ("MECHANISM_COMPLETENESS", "N-MC-2", "What are the main parts?"),
    ("PHYSICAL_FEASIBILITY", "N-PF-1", "What must be true to work safely?"),
    ("BOUNDARY_AMBIGUITY", "N-BA-1", "Which situations should it handle?"),
)
_SOURCE_ORDER = [qid for (_gap, qid, _text) in _SOURCE_QUESTIONS]


def _write_json(path: pathlib.Path, obj) -> pathlib.Path:
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return path


def _source_obj():
    gaps: dict = {g: [] for g in _GAPS}
    for gap, qid, text in _SOURCE_QUESTIONS:
        gaps[gap].append({"question_id": qid, "text": text})
    return {
        "metadata": {
            "path": "Path N",
            "domain": "electronics_electrical",
            "runtime_integrated": True,
        },
        "gaps": gaps,
    }


def _record(qid: str, gap: str, source_artifact_path: str, **overrides):
    rec = {
        "question_id": qid,
        "intent_id": "QI-" + qid,
        "design_gap_id": gap,
        "primary_intent": f"design-time intent for {qid}",
        "answer_objective": f"a complete answer for {qid}",
        "completion_condition": f"observable completion for {qid}",
        "source_reference": {"artifact_path": source_artifact_path, "question_id": qid},
    }
    rec.update(overrides)
    return rec


def _registry_obj(source_artifact_path: str, records=None):
    sap = source_artifact_path
    if records is None:
        gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
        records = [_record(qid, gap_of[qid], sap) for qid in _SOURCE_ORDER]
    return {
        "metadata": {
            "schema_version": "1.0.0",
            "registry_version": "1.0.0",
            "owner": "InventorAI Owner",
            "source_artifact": sap,
            "review_date": "2026-07-24",
            "stage": 2,
            "language": "en",
        },
        "records": records,
    }


def _valid_pair(tmp_path: pathlib.Path):
    """Write a valid, self-consistent (source, registry) pair; return their paths."""
    src = _write_json(tmp_path / "source.json", _source_obj())
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src)))
    return reg, src


def _load_or_red(reg_path, src_path, decision):
    """Call the real seam for a POSITIVE-behavior test; convert the still-present
    Minimal Interface placeholder into a controlled Behavioral RED."""
    try:
        return load_question_intent_registry(reg_path, src_path)
    except QuestionIntentRegistryLoadError as exc:
        if getattr(exc, "reason_code", None) == _PLACEHOLDER:
            pytest.fail(
                f"WS10 Behavioral RED ({decision}): load_question_intent_registry "
                f"has not implemented successful registry loading (still the Minimal "
                f"Interface placeholder): {exc}"
            )
        raise


def _expect_load_error(reg_path, src_path, expected_codes, decision):
    """Assert the seam fails loudly with one of the SPECIFIC approved reason codes
    for a VALIDATION test; the placeholder (wrong code) yields a controlled RED."""
    expected = frozenset(expected_codes)
    assert expected <= _APPROVED_REASON_CODES, "test uses only ratified D26 reason codes"
    try:
        load_question_intent_registry(reg_path, src_path)
    except QuestionIntentRegistryLoadError as exc:
        rc = getattr(exc, "reason_code", None)
        if rc == _PLACEHOLDER:
            pytest.fail(
                f"WS10 Behavioral RED ({decision}): validation not implemented; the "
                f"loader returns the Minimal Interface placeholder instead of a "
                f"reason_code in {sorted(expected)}."
            )
        assert rc in expected, (
            f"WS10 Behavioral RED ({decision}): expected reason_code in "
            f"{sorted(expected)}, got {rc!r}."
        )
        return
    pytest.fail(
        f"WS10 Behavioral RED ({decision}): expected a fail-loud "
        f"QuestionIntentRegistryLoadError with reason_code in {sorted(expected)}, "
        f"but the load succeeded (no-fallback / fail-loud not implemented)."
    )


# ── 1. Valid registry loading (D19/D30) ──
def test_valid_registry_loads_and_returns_registry(tmp_path):
    reg_path, src_path = _valid_pair(tmp_path)
    registry = _load_or_red(reg_path, src_path, "D19 valid load")
    assert isinstance(registry, QuestionIntentRegistry)
    records = registry.list_records()
    assert isinstance(records, tuple)
    assert [r.question_id for r in records] == _SOURCE_ORDER


# ── 2. Stable source-artifact ordering (D29) ──
def test_list_records_follows_source_artifact_order(tmp_path):
    src = _write_json(tmp_path / "source.json", _source_obj())
    gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
    shuffled = [_record(qid, gap_of[qid], str(src)) for qid in reversed(_SOURCE_ORDER)]
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src), records=shuffled))
    registry = _load_or_red(reg, src, "D29 source-artifact ordering")
    assert [r.question_id for r in registry.list_records()] == _SOURCE_ORDER, (
        "list_records() must follow committed source-artifact order, not registry "
        "insertion order."
    )


# ── 3. Exact source question-ID set equality (D11 / SOURCE_ID_SET_MISMATCH) ──
@pytest.mark.parametrize("case", ["missing_source_question", "extra_registry_question"])
def test_source_id_set_equality(tmp_path, case):
    src = _write_json(tmp_path / "source.json", _source_obj())
    gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
    records = [_record(qid, gap_of[qid], str(src)) for qid in _SOURCE_ORDER]
    if case == "missing_source_question":
        records = records[:-1]  # drop N-BA-1
    else:  # extra_registry_question
        records.append(_record("N-XX-9", "MECHANISM_COMPLETENESS", str(src)))
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src), records=records))
    _expect_load_error(reg, src, {"SOURCE_ID_SET_MISMATCH"}, f"D11 set-equality/{case}")


# ── 4. _STALL_REFRAME exclusion (D15) ──
def test_stall_reframe_not_registered(tmp_path):
    src = _write_json(tmp_path / "source.json", _source_obj())
    gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
    records = [_record(qid, gap_of[qid], str(src)) for qid in _SOURCE_ORDER]
    records.append(_record("_STALL_REFRAME", "MECHANISM_COMPLETENESS", str(src)))
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src), records=records))
    # _STALL_REFRAME is not a committed source question, so a registry that treats
    # it as a record must be rejected (set mismatch), never accepted.
    _expect_load_error(reg, src, {"SOURCE_ID_SET_MISMATCH"}, "D15 _STALL_REFRAME exclusion")


# ── 5. Missing required record field (D3 / MISSING_REQUIRED_FIELD) ──
@pytest.mark.parametrize("field", _REQUIRED_RECORD_FIELDS)
def test_missing_required_field_rejected(tmp_path, field):
    src = _write_json(tmp_path / "source.json", _source_obj())
    gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
    records = [_record(qid, gap_of[qid], str(src)) for qid in _SOURCE_ORDER]
    del records[0][field]  # remove one approved field from the first record
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src), records=records))
    _expect_load_error(reg, src, {"MISSING_REQUIRED_FIELD"}, f"D3 required field/{field}")


# ── 6. Duplicate question_id (D11 / DUPLICATE_QUESTION_ID) ──
def test_duplicate_question_id_rejected(tmp_path):
    src = _write_json(tmp_path / "source.json", _source_obj())
    gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
    records = [_record(qid, gap_of[qid], str(src)) for qid in _SOURCE_ORDER]
    records[1] = _record("N-MC-1", "MECHANISM_COMPLETENESS", str(src))  # duplicate id
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src), records=records))
    _expect_load_error(reg, src, {"DUPLICATE_QUESTION_ID"}, "D11 duplicate question_id")


# ── 7. Duplicate intent_id (D11 / DUPLICATE_INTENT_ID) ──
def test_duplicate_intent_id_rejected(tmp_path):
    src = _write_json(tmp_path / "source.json", _source_obj())
    gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
    records = [_record(qid, gap_of[qid], str(src)) for qid in _SOURCE_ORDER]
    records[1]["intent_id"] = records[0]["intent_id"]  # duplicate intent_id, distinct qid
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src), records=records))
    _expect_load_error(reg, src, {"DUPLICATE_INTENT_ID"}, "D11 duplicate intent_id")


# ── 8. Invalid design_gap_id (D5 / INVALID_DESIGN_GAP_ID) ──
def test_invalid_design_gap_id_rejected(tmp_path):
    src = _write_json(tmp_path / "source.json", _source_obj())
    gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
    records = [_record(qid, gap_of[qid], str(src)) for qid in _SOURCE_ORDER]
    records[0]["design_gap_id"] = "NOT_A_CANONICAL_GAP"
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src), records=records))
    _expect_load_error(reg, src, {"INVALID_DESIGN_GAP_ID"}, "D5 canonical design_gap_id")


# ── 9. Invalid metadata (D8 / INVALID_METADATA) ──
@pytest.mark.parametrize("case", ["missing_metadata_field", "mismatched_source_artifact"])
def test_invalid_metadata_rejected(tmp_path, case):
    src = _write_json(tmp_path / "source.json", _source_obj())
    obj = _registry_obj(str(src))
    if case == "missing_metadata_field":
        del obj["metadata"]["schema_version"]
    else:  # mismatched_source_artifact
        obj["metadata"]["source_artifact"] = str(tmp_path / "some_other_artifact.json")
    reg = _write_json(tmp_path / "registry.json", obj)
    _expect_load_error(reg, src, {"INVALID_METADATA"}, f"D8 metadata/{case}")


# ── 10. Source-reference validation (D6 / SOURCE_REFERENCE_MISMATCH) ──
@pytest.mark.parametrize("case", ["wrong_artifact_path", "wrong_question_id"])
def test_source_reference_mismatch_rejected(tmp_path, case):
    src = _write_json(tmp_path / "source.json", _source_obj())
    gap_of = {qid: gap for (gap, qid, _t) in _SOURCE_QUESTIONS}
    records = [_record(qid, gap_of[qid], str(src)) for qid in _SOURCE_ORDER]
    if case == "wrong_artifact_path":
        records[0]["source_reference"]["artifact_path"] = str(tmp_path / "elsewhere.json")
    else:  # wrong_question_id (source_reference.question_id != record question_id, D6 MUST)
        records[0]["source_reference"]["question_id"] = "N-BA-1"
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src), records=records))
    _expect_load_error(reg, src, {"SOURCE_REFERENCE_MISMATCH"}, f"D6 source_reference/{case}")


# ── 11. Source-artifact validation (D14) ──
@pytest.mark.parametrize(
    "case,expected",
    [
        ("missing", {"INVALID_SOURCE_ARTIFACT_PATH", "FILE_READ_ERROR"}),
        ("malformed_json", {"INVALID_JSON"}),
        ("wrong_structure", {"INVALID_SOURCE_ARTIFACT_PATH"}),
    ],
)
def test_source_artifact_validation(tmp_path, case, expected):
    reg_obj = _registry_obj(str(tmp_path / "source.json"))
    reg = _write_json(tmp_path / "registry.json", reg_obj)
    src = tmp_path / "source.json"
    if case == "missing":
        pass  # never written
    elif case == "malformed_json":
        src.write_text("{ this is not valid json", encoding="utf-8")
    else:  # wrong_structure — no committed question structure
        _write_json(src, {"metadata": {"path": "Path N"}, "unexpected": True})
    _expect_load_error(reg, src, expected, f"D14 source-artifact/{case}")


# ── 12. Registry-artifact validation (D14) ──
@pytest.mark.parametrize(
    "case,expected",
    [
        ("missing", {"FILE_READ_ERROR"}),
        ("malformed_json", {"INVALID_JSON"}),
        ("invalid_toplevel", {"INVALID_METADATA", "MISSING_REQUIRED_FIELD"}),
    ],
)
def test_registry_artifact_validation(tmp_path, case, expected):
    src = _write_json(tmp_path / "source.json", _source_obj())
    reg = tmp_path / "registry.json"
    if case == "missing":
        pass  # never written
    elif case == "malformed_json":
        reg.write_text("{ not: valid", encoding="utf-8")
    else:  # invalid_toplevel — missing the {metadata, records} shape (D28)
        _write_json(reg, {"records": []})
    _expect_load_error(reg, src, expected, f"D14 registry-artifact/{case}")


# ── 13. Unknown question lookup raises typed error (D22/D23) ──
def test_unknown_question_id_raises_not_found(tmp_path):
    reg_path, src_path = _valid_pair(tmp_path)
    registry = _load_or_red(reg_path, src_path, "D23 unknown-ID lookup")
    with pytest.raises(QuestionIntentNotFoundError):
        registry.get("N-XX-DOES-NOT-EXIST")


# ── 14. No fallback on invalid input (D30) ──
def test_no_fallback_on_invalid_registry(tmp_path):
    src = _write_json(tmp_path / "source.json", _source_obj())
    # A registry with an empty records set can never satisfy source-ID set equality;
    # the loader must fail loud, not return an empty/fallback registry.
    reg = _write_json(tmp_path / "registry.json", _registry_obj(str(src), records=[]))
    _expect_load_error(reg, src, {"SOURCE_ID_SET_MISMATCH"}, "D30 no-fallback")
