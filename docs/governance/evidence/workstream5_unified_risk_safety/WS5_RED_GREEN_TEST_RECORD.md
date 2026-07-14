# WS5_RED_GREEN_TEST_RECORD — Workstream 5 verification (raw outputs)

All outputs below are unedited pytest results. BASE outputs were produced in a
clean read-only worktree checkout of the RED commit
`3cef5eb79a3c3483903f3e0acbe59c18dc05caf0`; HEAD outputs at the GREEN commit
`97b6725953150509059dd41ba623e438f939f094` (tree `4c8cdb186d20635df98477c65854574e8ec6d538`).

## 1. BASE RED — `python -m pytest tests/test_unified_risk_safety_presentation.py -q` at `3cef5eb7`

```
-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_unified_risk_safety_presentation.py::TestLinkageRed::test_r1_linkage_block_and_section6_reference_exist
FAILED tests/test_unified_risk_safety_presentation.py::TestLinkageRed::test_r2_low_process_risk_reconciled_with_stated_danger
FAILED tests/test_unified_risk_safety_presentation.py::TestLinkageRed::test_r3_section13_adjacent_note_exists
FAILED tests/test_unified_risk_safety_presentation.py::TestLinkageRed::test_r4_empty_section6_qualified_when_signals_exist
FAILED tests/test_unified_risk_safety_presentation.py::TestLinkageRed::test_r5_disconnection_in_both_json_and_html
5 failed, 7 passed, 1 warning in 0.53s
```

Classification: **5 failed / 7 passed / 1 warning** — the five intended linkage
failures (R1–R5, each an obligation-specific "missing behavior" assertion), six
protected invariants plus the documentation-only R6 passing. No fixture, import,
skip, or xfail defect.

## 2. HEAD GREEN — `python -m pytest tests/test_unified_risk_safety_presentation.py -q` at `97b67259`

```
17 passed, 1 warning in 0.53s
```

**17 passed — zero failed, zero skipped, zero xfailed** (P1–P6, R1–R5 now GREEN,
G1–G5 byte-exact wordings + machine-compared parity, R6 unchanged).

## 3. Protected suite (safety 18 + stabilization 15 + hygiene 22 + structured-criticality 18 + landscape 39 + increment-6 + phase-5a1)

```
148 passed, 1 warning in 0.87s
```

## 4. Contract-listed suites (assembler, fdc001_user_value, evidence/unknown registries, 3b2a/3b2b, 7b, 7c)

```
91 passed, 1 warning in 0.40s
```

## 5. Fixed focused suite (WS4-closure 17-file set + structured-criticality + the WS5 file)

```
333 passed, 1 warning in 1.50s
```

## 6. Full suite — `python -m pytest -p no:cacheprovider -q` at `97b67259`

```
31 failed, 1396 passed, 1 skipped, 1 xfailed, 24 xpassed, 111 warnings in 4.53s
```

Failure confinement (machine-checked): 31 FAILED lines total, 0 outside
`tests/test_domain_registry.py`; the sorted FAILED list is `diff`-identical to
the canonical Workstream 4 closure baseline (the same 31 pre-existing cases).
The single skip is the pre-existing `tests/test_wps001_invariants.py:112`
environmental skip. The full suite does NOT pass completely; the 31 known
baseline failures remain and are neither hidden nor reclassified.

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
