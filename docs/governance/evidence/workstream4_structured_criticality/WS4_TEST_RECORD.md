# WS4_TEST_RECORD — Workstream 4 HEAD GREEN verification (raw outputs)

Generated at HEAD GREEN commit `61f0b14cb6bf2f5c5328eb9958640bf036015720`
(tree `edf06078cdac4b88c29bef6b2a74266c83dff7c3`), repository root, immediately
before the evidence commit. Every output below is the unedited pytest result.

## 1. `python -m pytest tests/test_structured_criticality.py -v`

```
============================= test session starts ==============================
collecting ... collected 18 items

tests/test_structured_criticality.py::TestProtectedInvariants::test_p1_ai_q2_free_text_never_classifies_criticality PASSED [  5%]
tests/test_structured_criticality.py::TestProtectedInvariants::test_p2_iteration7_statement_recorded_verbatim PASSED [ 11%]
tests/test_structured_criticality.py::TestProtectedInvariants::test_p3_section13_never_interacted_public_wording PASSED [ 16%]
tests/test_structured_criticality.py::TestProtectedInvariants::test_p4_rendering_changes_nothing PASSED [ 22%]
tests/test_structured_criticality.py::TestProtectedInvariants::test_p5_no_raw_category_or_authority_tokens_inventor_facing PASSED [ 27%]
tests/test_structured_criticality.py::TestRecordedStateModelRed::test_r1_confirmation_history_exists PASSED [ 33%]
tests/test_structured_criticality.py::TestRecordedStateModelRed::test_r2_guarded_recorder_records_owner_confirmation PASSED [ 38%]
tests/test_structured_criticality.py::TestRecordedStateModelRed::test_r3_recorder_rejects_confirmed_undetermined PASSED [ 44%]
tests/test_structured_criticality.py::TestRecordedStateModelRed::test_r4_recorder_rejects_missing_rationale PASSED [ 50%]
tests/test_structured_criticality.py::TestEndToEndRepresentationRed::test_r5_confirmed_category_reaches_section13_json PASSED [ 55%]
tests/test_structured_criticality.py::TestEndToEndRepresentationRed::test_r6_confirmed_category_reaches_rendered_html PASSED [ 61%]
tests/test_structured_criticality.py::TestEndToEndRepresentationRed::test_r7_explicit_deferral_representable PASSED [ 66%]
tests/test_structured_criticality.py::TestEndToEndRepresentationRed::test_r8_history_append_only_latest_governs PASSED [ 72%]
tests/test_structured_criticality.py::TestGreenJourney::test_g1_summary_first_surface_five_actions_clean_vocabulary PASSED [ 77%]
tests/test_structured_criticality.py::TestGreenJourney::test_g2_accept_flow_end_to_end_no_adoption_before_acceptance PASSED [ 83%]
tests/test_structured_criticality.py::TestGreenJourney::test_g3_correction_and_missing_paths_store_nothing PASSED [ 88%]
tests/test_structured_criticality.py::TestGreenJourney::test_g4_uncertainty_and_deferral_zero_delta PASSED [ 94%]
tests/test_structured_criticality.py::TestGreenJourney::test_g5_manipulated_or_stale_posts_rejected PASSED [100%]

=============================== warnings summary ===============================
engine/domain_rules.py:7
  /home/user/inventorai/engine/domain_rules.py:7: UserWarning: domain_registry: skipping domains/iot_electronics/domain.json (schema_version=None, expected '1.0')
    _REGISTRY = load_registry("domains/")

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 18 passed, 1 warning in 0.78s =========================
```

Classification: **18 passed, zero failed, zero skipped, zero xfailed** (the
owner F1 gate: the former GREEN-only placeholder skip is gone, replaced by
the real journey tests G1–G5).

## 2. `python -m pytest tests/test_deliverable_hygiene.py -q`

```
22 passed, 1 warning in 0.42s
```

## 3. `python -m pytest tests/test_safety_signal.py -q`

```
18 passed, 1 warning in 0.25s
```

## 4. `python -m pytest tests/test_safety_signal_stabilization.py -q`

```
15 passed in 0.06s
```

## 5. `python -m pytest tests/test_increment_4_requirement_landscape.py -q`

```
39 passed, 1 warning in 0.29s
```

## 6. Fixed 17-file focused suite + tests/test_structured_criticality.py

Command: the Workstream 3 canonical fixed 17-file focused-suite command
(docs/governance/evidence/workstream3_deliverable_hygiene/WS3_TEST_RECORD.md §4)
with `tests/test_structured_criticality.py` appended.

```
316 passed, 1 warning in 1.50s
```

(297 Workstream 3 baseline + 1 hygiene-hardening test + 18 structured-criticality = 316.)

## 7. Full suite — `python -m pytest -p no:cacheprovider -q`

```
31 failed, 1379 passed, 1 skipped, 1 xfailed, 24 xpassed, 111 warnings in 5.86s
```

Failure confinement (machine-checked): 31 FAILED lines total; 0 outside
`tests/test_domain_registry.py` — the known pre-existing baseline, identical
to the Workstream 3 canonical closure record. The single skip is the
pre-existing `tests/test_wps001_invariants.py:112` environmental skip
("No gaps reached CLOSED"), NOT the structured-criticality suite.

Complete sorted FAILED list:

```
FAILED tests/test_domain_registry.py::TestDeterministicLoading::test_load_order_is_sorted
FAILED tests/test_domain_registry.py::TestDeterministicLoading::test_subdir_without_domain_json_is_skipped
FAILED tests/test_domain_registry.py::TestGetDomain::test_get_domain_correct_content
FAILED tests/test_domain_registry.py::TestGetDomain::test_get_domain_returns_dict
FAILED tests/test_domain_registry.py::TestInvalidValueValidation::test_empty_capability_id_raises
FAILED tests/test_domain_registry.py::TestInvalidValueValidation::test_empty_domain_signals_raises
FAILED tests/test_domain_registry.py::TestInvalidValueValidation::test_empty_gaps_raises
FAILED tests/test_domain_registry.py::TestInvalidValueValidation::test_empty_governance_source_raises
FAILED tests/test_domain_registry.py::TestInvalidValueValidation::test_invalid_deprecation_status_raises
FAILED tests/test_domain_registry.py::TestInvalidValueValidation::test_invalid_review_date_raises
FAILED tests/test_domain_registry.py::TestInvalidValueValidation::test_invalid_version_format_raises
FAILED tests/test_domain_registry.py::TestListDomains::test_list_domains_contains_known_domain
FAILED tests/test_domain_registry.py::TestLoadValidDomain::test_domain_contains_expected_keys
FAILED tests/test_domain_registry.py::TestLoadValidDomain::test_governance_contains_expected_keys
FAILED tests/test_domain_registry.py::TestLoadValidDomain::test_load_iot_electronics_domain
FAILED tests/test_domain_registry.py::TestLoadValidDomain::test_registry_keyed_by_capability_id
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[deprecation_status]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[license]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[owner]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[review_date]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[source]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[version]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[capability_id]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[description]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[display_name]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[domain_signals]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[gaps]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[governance]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[notes]
FAILED tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[taxonomy_group]
FAILED tests/test_domain_registry.py::TestRuntimeIsolation::test_domain_rules_not_modified
```

## 8. Verified classifications (owner-mandated values, all met exactly)

| Gate | Expected | Observed |
|---|---|---|
| structured-criticality | 18 passed, 0 skipped, 0 xfailed | 18 passed, 0 skipped, 0 xfailed |
| hygiene | 22 passed | 22 passed |
| Safety Signal | 18 passed | 18 passed |
| Safety Signal stabilization | 15 passed | 15 passed |
| requirement landscape | 39 passed | 39 passed |
| fixed focused suite (+ new file) | 316 passed | 316 passed |
| full suite | 31 failed / 1379 passed / 1 skipped / 1 xfailed / 24 xpassed | identical |
| failure confinement | all 31 in tests/test_domain_registry.py | 31/31, 0 outside |
