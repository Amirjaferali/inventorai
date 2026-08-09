"""P7-I3 — Canonical Export + Local/Reference Adapter Proof (RED → GREEN).

Behavioral tests for the established, repository-established P7-I3 bounded increment
contract (`docs/governance/P7_I3_CANONICAL_EXPORT_LOCAL_REFERENCE_ADAPTER_PROOF_INCREMENT_CONTRACT.md`,
PR #408). The proof is OUTBOUND-ONLY, NON-MUTATING, NETWORK-FREE, VENDOR-NEUTRAL,
UNTRUSTED BY DEFAULT:

    canonical P7-I1 Structured Export
      → local/reference adapter (deterministic transform)
      → structurally distinct transformed representation
      → semantic inverse/equivalence validation (independent of the transform)

The happy-path/consumption tests consume the REAL P7-I1 export seam
(`engine.read_export_service.produce_project_export`); adversarial integrity tests
mutate a copy of a real export to exercise the validator's failure detection.

Provider-free, network-free; SQLite files live only in pytest tmp_path.
"""
import copy
import inspect
import types

import pytest

from engine.idea_state import (
    AssertionRecord, OWNER_STATED, LEGACY_UNSPECIFIED, UNVALIDATED,
    INDEPENDENTLY_VERIFIED,
)
from engine.record_contract import ProjectRecordContract
from engine.record_store import SqliteRecordStore
from engine import read_export_service as _seam

# The module under test (P7-I3 adapter). Absent on the base → genuine RED.
from engine import export_adapter as adp


OWNER = "acct_owner"


def _store(tmp_path):
    s = SqliteRecordStore(str(tmp_path / "p7i3.sqlite3"))
    contract = ProjectRecordContract(idea_id="idea-p7i3", assertions=[
        AssertionRecord(record_id="rec_1", disposition="answered", content="a",
                        gap_context="g1", iteration=1, provenance=OWNER_STATED,
                        validation_status=UNVALIDATED),
        AssertionRecord(record_id="rec_2", disposition="answered", content="b",
                        gap_context="g2", iteration=2, provenance=LEGACY_UNSPECIFIED,
                        validation_status=INDEPENDENTLY_VERIFIED),
    ])
    s.create_project(contract, project_id="p1",
                     reconstruction_inputs={"seed_idea_text": "s",
                                            "confirmed_domain": "electronics_electrical",
                                            "path": "path_n", "engine_contract_version": "v1"},
                     owner_account_id=OWNER)
    return s


def _canonical(tmp_path):
    # REAL P7-I1 canonical export (not a hand-built fake).
    return _seam.produce_project_export(_store(tmp_path), "p1", OWNER)


def _adapter():
    return adp.ReferenceExportAdapter()


# ---- Transform: acceptance, distinctness, determinism, provenance -----------

def test_real_canonical_export_accepted_and_distinct(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    assert isinstance(t, dict)
    assert t != canonical                       # structurally distinct, not identity
    assert "adapter" in t and "project" in t and "records" in t
    assert "assertions" not in t                # renamed away from canonical shape


def test_transform_is_deterministic_and_ordered(tmp_path):
    canonical = _canonical(tmp_path)
    a = _adapter()
    t1 = a.transform(canonical)
    t2 = a.transform(canonical)
    assert t1 == t2
    # Row order derives from canonical assertion order (deterministic).
    assert [r["id"] for r in t1["records"]] == [a_["record_id"] for a_ in canonical["assertions"]]


def test_adapter_provenance_present(tmp_path):
    t = _adapter().transform(_canonical(tmp_path))
    prov = t["adapter"]
    assert prov["adapter_id"] and prov["adapter_version"] and prov["output_type"]
    assert prov["source"] == "P7-I1 Structured Export seam"


def test_mandatory_preservation_floor_survives(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    assert set(("idea_id", "domain_support_state", "assertion_count")) <= set(t["project"])
    assert t["project"]["idea_id"] == canonical["idea_id"]
    assert t["project"]["domain_support_state"] == canonical["domain_support_state"]
    for r in t["records"]:
        assert set(r) >= {"id", "disposition", "provenance", "validation_status"}


# ---- Validation: valid path -------------------------------------------------

def test_valid_equivalence_passes(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    assert adp.validate_equivalence(canonical, t) == "valid"


# ---- Validation: integrity / tamper detection (adversarial) -----------------

def test_changed_mandatory_field_fails(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    bad = copy.deepcopy(t)
    bad["records"][0]["validation_status"] = "TAMPERED"
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, bad)


def test_missing_assertion_fails(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    bad = copy.deepcopy(t)
    bad["records"].pop()                        # drop a row
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, bad)


def test_duplicate_assertion_and_record_id_collision_fails(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    bad = copy.deepcopy(t)
    bad["records"][1]["id"] = bad["records"][0]["id"]   # record_id collision
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, bad)


def test_assertion_count_row_inconsistency_fails(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    bad = copy.deepcopy(t)
    bad["project"]["assertion_count"] = 99      # inconsistent with rows
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, bad)


def test_validation_summary_row_inconsistency_fails(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    bad = copy.deepcopy(t)
    bad["project"]["validation_summary"] = {"bogus": 5}
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, bad)


def test_provenance_summary_row_inconsistency_fails(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    bad = copy.deepcopy(t)
    bad["project"]["provenance_summary"] = {"bogus": 5}
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, bad)


def test_malformed_transformed_representation_fails(tmp_path):
    canonical = _canonical(tmp_path)
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, {"not": "a valid transformed shape"})


# ---- Source version metadata (only when supplied) ---------------------------

def test_unsupported_explicit_source_version_fails_when_supplied(tmp_path):
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical, source_version="999-bogus")
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, t, recognized_source_versions={"1"})


def test_supported_source_version_ok_and_none_ok(tmp_path):
    canonical = _canonical(tmp_path)
    a = _adapter()
    t_ok = a.transform(canonical, source_version="1")
    assert adp.validate_equivalence(canonical, t_ok, recognized_source_versions={"1"}) == "valid"
    t_none = a.transform(canonical)             # no version metadata → structural validation governs
    assert t_none["adapter"]["source_version"] is None
    assert adp.validate_equivalence(canonical, t_none) == "valid"


# ---- Malformed / failing canonical input ------------------------------------

def test_malformed_canonical_input_fails(tmp_path):
    with pytest.raises(adp.AdapterError):
        _adapter().transform({"missing": "idea_id and assertions"})


def test_transform_failure_on_non_dict(tmp_path):
    with pytest.raises(adp.AdapterError):
        _adapter().transform(["not", "a", "dict"])


# ---- Non-mutation (success, transform failure, validation failure) ----------

def _project_snapshot(store):
    return store.load_contract("p1").to_json()


def test_project_state_unchanged_after_success(tmp_path):
    store = _store(tmp_path)
    before = _project_snapshot(store)
    canonical = _seam.produce_project_export(store, "p1", OWNER)
    t = _adapter().transform(canonical)
    adp.validate_equivalence(canonical, t)
    assert _project_snapshot(store) == before


def test_project_state_unchanged_after_transform_failure(tmp_path):
    store = _store(tmp_path)
    before = _project_snapshot(store)
    with pytest.raises(adp.AdapterError):
        _adapter().transform(["bad"])
    assert _project_snapshot(store) == before


def test_project_state_unchanged_after_validation_failure(tmp_path):
    store = _store(tmp_path)
    before = _project_snapshot(store)
    canonical = _seam.produce_project_export(store, "p1", OWNER)
    t = _adapter().transform(canonical)
    bad = copy.deepcopy(t)
    bad["records"][0]["provenance"] = "TAMPERED"
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, bad)
    assert _project_snapshot(store) == before


# ---- Boundary hygiene: network-free, no store construction, no web coupling --

def _all_names(mod):
    names = set()
    for v in vars(mod).values():
        if isinstance(v, types.FunctionType):
            names |= set(v.__code__.co_names)
        elif isinstance(v, type):
            for m in vars(v).values():
                if isinstance(m, types.FunctionType):
                    names |= set(m.__code__.co_names)
    return names


def test_adapter_module_is_network_free_and_constructs_no_store():
    # No network / web-framework module imported into the adapter namespace.
    assert not any(
        getattr(v, "__name__", "") in ("socket", "urllib", "requests", "http",
                                       "flask", "werkzeug")
        for v in vars(adp).values() if isinstance(v, types.ModuleType))
    names = _all_names(adp)
    for forbidden in ("SqliteRecordStore", "load_owner", "load_contract",
                      "save", "append_record", "create_project", "socket",
                      "urlopen", "request", "session"):
        assert forbidden not in names, "adapter must not reference %s" % forbidden


def test_validator_is_independent_of_transform(tmp_path):
    # The validator compares transformed-vs-canonical; it must reject a transformed
    # payload whose rows disagree with canonical even though it is otherwise shaped
    # like a valid transform (i.e. it does not merely re-run transform and self-agree).
    canonical = _canonical(tmp_path)
    t = _adapter().transform(canonical)
    bad = copy.deepcopy(t)
    bad["project"]["idea_id"] = "SOMETHING-ELSE"
    with pytest.raises(adp.AdapterError):
        adp.validate_equivalence(canonical, bad)
