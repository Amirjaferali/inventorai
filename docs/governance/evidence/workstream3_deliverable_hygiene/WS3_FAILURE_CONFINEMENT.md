# WS3 Failure Confinement Proof (machine-verifiable)

## Claim

Every full-suite failure at the canonical merged tip
`0b04021d99290f8f747ee24d46b93c1dda69d66f` is in `tests/test_domain_registry.py`,
the identical 31 failures pre-exist at the authoritative pre-Workstream-3 base
`c64bd9206ef620078906831109562875055106de` (the tip before the PR #177 RED merge,
i.e. before any Workstream 3 test or source change), and there is no new
regression outside that file.

## Method

1. `python3 -m pytest tests/ -q -p no:cacheprovider` at the merged tip; extract
   the `FAILED` test ids and sort.
2. `git archive c64bd920... | tar -x` into a scratch directory; run the same
   command there; extract and sort the `FAILED` ids.
3. `diff` the two id sets.

## Results

- Merged tip totals: `31 failed, 1360 passed, 1 skipped, 1 xfailed, 24 xpassed, 111 warnings`
- Pre-WS3 base totals: `31 failed, 1339 passed, 1 skipped, 1 xfailed, 24 xpassed, 111 warnings`
  (the passed-count delta of +21 at the tip equals the 21 canonical hygiene tests added by Workstream 3)
- FAILED-id sets: 31 vs 31; `diff` output EMPTY — the sets are IDENTICAL.
- Count of merged-tip failures outside `tests/test_domain_registry.py`: **0**
  (`grep '^FAILED' | grep -cv test_domain_registry` = 0).

## The 31 identical failing test ids (both revisions)

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
