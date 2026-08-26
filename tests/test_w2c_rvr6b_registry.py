"""W2-C / RVR-6b — committed WS10 registry instances (OD-W2-WS10-SCOPE).

Proves the exercised Owner decision exactly: TWO per-domain registry
instances (electronics 11 ids / mechanical 10 ids / total 21 existing
committed ids) validated through the UNMODIFIED D11/D19 loader, plus the
EN/AR pairing invariant of the W2-C-authored marker table and the
fail-closed accessor negatives."""
import json
from pathlib import Path

import pytest

from engine.question_intent_registry import (
    load_question_intent_registry,
    QuestionIntentRegistryLoadError,
)
import engine.intent_serving as intent_serving
from engine.intent_serving import (
    _DOMAIN_REGISTRY_FILES, _INTENT_MARKERS, _load_registry, _matches_intent,
)

ELEC = "electronics_electrical"
MECH = "mechanical"

EXPECTED_ELEC_IDS = [
    "N-MC-1", "N-MC-2", "N-MC-3", "N-MC-4",
    "N-PF-1", "N-PF-2", "N-PF-3", "N-PF-4",
    "N-BA-1", "N-BA-2", "N-BA-3",
]
EXPECTED_MECH_IDS = [
    "mechanical:MECHANISM_COMPLETENESS:Q1",
    "mechanical:MECHANISM_COMPLETENESS:Q2",
    "mechanical:MECHANISM_COMPLETENESS:Q3",
    "mechanical:MECHANISM_COMPLETENESS:Q4",
    "mechanical:PHYSICAL_FEASIBILITY:Q1",
    "mechanical:PHYSICAL_FEASIBILITY:Q2",
    "mechanical:BOUNDARY_AMBIGUITY:Q1",
    "mechanical:BOUNDARY_AMBIGUITY:Q2",
    "mechanical:BOUNDARY_AMBIGUITY:Q3",
    "mechanical:BOUNDARY_AMBIGUITY:Q4",
]


def _fresh_cache(monkeypatch):
    monkeypatch.setattr(intent_serving, "_REGISTRY_CACHE", {})


def test_exactly_two_per_domain_registry_instances():
    assert set(_DOMAIN_REGISTRY_FILES) == {ELEC, MECH}


def test_electronics_registry_loads_with_exact_11_ids():
    reg_path, src_path = _DOMAIN_REGISTRY_FILES[ELEC]
    registry = load_question_intent_registry(Path(reg_path), Path(src_path))
    assert [r.question_id for r in registry.list_records()] == EXPECTED_ELEC_IDS


def test_mechanical_registry_loads_with_exact_10_ids():
    reg_path, src_path = _DOMAIN_REGISTRY_FILES[MECH]
    registry = load_question_intent_registry(Path(reg_path), Path(src_path))
    assert [r.question_id for r in registry.list_records()] == EXPECTED_MECH_IDS


def test_total_committed_id_count_is_21_and_no_invented_ids():
    all_ids = set(EXPECTED_ELEC_IDS) | set(EXPECTED_MECH_IDS)
    assert len(all_ids) == 21
    # marker table covers exactly the 21 committed ids — nothing invented
    assert set(_INTENT_MARKERS) == all_ids


def test_every_marker_entry_is_en_ar_paired_and_nonempty():
    for qid, (en_set, ar_set) in _INTENT_MARKERS.items():
        assert en_set and all(isinstance(m, str) and m for m in en_set), qid
        assert ar_set and all(isinstance(m, str) and m for m in ar_set), qid
        # EN markers are lowercase (matched on lowered text)
        assert all(m == m.lower() for m in en_set), qid


def test_registry_records_carry_committed_intent_metadata():
    for domain in (ELEC, MECH):
        reg_path, src_path = _DOMAIN_REGISTRY_FILES[domain]
        registry = load_question_intent_registry(Path(reg_path), Path(src_path))
        for record in registry.list_records():
            assert record.primary_intent
            assert record.answer_objective
            assert record.completion_condition
            assert record.intent_id == "intent:" + record.question_id
            assert record.source_reference.question_id == record.question_id


def test_accessor_returns_validated_registry_and_caches(monkeypatch):
    _fresh_cache(monkeypatch)
    first = _load_registry(MECH)
    assert first is not None
    assert _load_registry(MECH) is first  # load-once


def test_accessor_fails_closed_for_unknown_domain(monkeypatch):
    _fresh_cache(monkeypatch)
    assert _load_registry("software") is None
    assert _load_registry(None) is None


def test_accessor_fails_closed_on_missing_registry_file(monkeypatch):
    _fresh_cache(monkeypatch)
    monkeypatch.setitem(
        intent_serving._DOMAIN_REGISTRY_FILES, MECH,
        ("docs/governance/path_n_content_config/does_not_exist.json",
         _DOMAIN_REGISTRY_FILES[MECH][1]))
    assert _load_registry(MECH) is None
    # a failure is not cached — the domain can recover
    assert MECH not in intent_serving._REGISTRY_CACHE


def test_loader_rejects_malformed_registry(tmp_path):
    reg_path, src_path = _DOMAIN_REGISTRY_FILES[MECH]
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(QuestionIntentRegistryLoadError) as err:
        load_question_intent_registry(bad, Path(src_path))
    assert err.value.reason_code == "INVALID_JSON"


def test_loader_rejects_partial_coverage(tmp_path):
    # dropping one committed record must fail SOURCE_ID_SET_MISMATCH —
    # no partial registry is ever returned (fail-closed, D11/D14)
    reg_path, src_path = _DOMAIN_REGISTRY_FILES[MECH]
    data = json.loads(Path(reg_path).read_text(encoding="utf-8"))
    data["records"] = data["records"][:-1]
    partial = tmp_path / "partial.json"
    # keep the committed source_artifact string intact so only the ID set fails
    partial_rel = partial
    text = json.dumps(data, ensure_ascii=False)
    partial_rel.write_text(text, encoding="utf-8")
    with pytest.raises(QuestionIntentRegistryLoadError) as err:
        load_question_intent_registry(partial_rel, Path(src_path))
    assert err.value.reason_code in ("SOURCE_ID_SET_MISMATCH",
                                     "SOURCE_REFERENCE_MISMATCH",
                                     "INVALID_METADATA")


def test_loader_rejects_duplicate_question_id(tmp_path):
    reg_path, src_path = _DOMAIN_REGISTRY_FILES[MECH]
    data = json.loads(Path(reg_path).read_text(encoding="utf-8"))
    dup = dict(data["records"][0])
    dup["intent_id"] = "intent:duplicate"
    data["records"].append(dup)
    bad = tmp_path / "dup.json"
    bad.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(QuestionIntentRegistryLoadError) as err:
        load_question_intent_registry(bad, Path(src_path))
    assert err.value.reason_code in ("DUPLICATE_QUESTION_ID",
                                     "SOURCE_REFERENCE_MISMATCH",
                                     "INVALID_METADATA")


def test_cross_domain_ids_never_leak_between_marker_scopes():
    # an electronics answer phrase must not match a mechanical id and
    # vice versa: marker consultation is strictly per question_id
    assert _matches_intent("force path through the hinge line",
                           "mechanical:MECHANISM_COMPLETENESS:Q2")
    assert not _matches_intent("force path through the hinge line", "N-MC-2")
    assert _matches_intent("the main parts are a sensor and a buzzer",
                           "N-MC-2")
    assert not _matches_intent("the main parts are a sensor and a buzzer",
                               "mechanical:MECHANISM_COMPLETENESS:Q2")


def test_unknown_question_id_matches_nothing():
    assert not _matches_intent("force path", "unknown:id")
    assert not _matches_intent("", "N-MC-1")
    assert not _matches_intent(None, "N-MC-1")
