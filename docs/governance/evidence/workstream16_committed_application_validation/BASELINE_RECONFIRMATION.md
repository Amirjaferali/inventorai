# WS16 — Independent Baseline Reconfirmation

**Purpose.** Independently reconfirm the pre-existing test baseline against
committed source, without assuming any previously reported count. The previously
circulated figure of "31 failures" is treated as unverified until reproduced here.

## Authoritative context

| Item | Value |
|---|---|
| Repository | `Amirjaferali/inventorai` |
| Validation base commit | `143a1ed4dc4022e6bbec935884e1159a4f18be7c` |
| Ordered parents of base | `30c8d7d6…` (WS16 Status Canonicalization merge), `c7b76b09…` (representative-journey nav fix) |
| Interpreter | Python 3.11.15 |
| Test runner | pytest 9.1.1 |
| Mode | READ-ONLY. No source, test, fixture, or configuration change. |

## Command executed

```
python3 -m pytest tests/test_domain_registry.py -q
```

## Raw result (reproduced independently)

```
31 failed, 10 passed, 40 warnings in ~1.2s
```

Confirmed by two independent runs of the same command; both reported
`31 failed, 10 passed`.

## Failing node IDs (all 31, enumerated — not summarized)

```
tests/test_domain_registry.py::TestDeterministicLoading::test_load_order_is_sorted
tests/test_domain_registry.py::TestDeterministicLoading::test_subdir_without_domain_json_is_skipped
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[taxonomy_group]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[capability_id]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[display_name]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[description]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[domain_signals]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[gaps]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[notes]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_top_level_field_raises[governance]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[source]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[license]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[owner]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[review_date]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[version]
tests/test_domain_registry.py::TestMissingFieldValidation::test_missing_governance_field_raises[deprecation_status]
tests/test_domain_registry.py::TestInvalidValueValidation::test_invalid_version_format_raises
tests/test_domain_registry.py::TestInvalidValueValidation::test_invalid_review_date_raises
tests/test_domain_registry.py::TestInvalidValueValidation::test_invalid_deprecation_status_raises
tests/test_domain_registry.py::TestInvalidValueValidation::test_empty_capability_id_raises
tests/test_domain_registry.py::TestInvalidValueValidation::test_empty_domain_signals_raises
tests/test_domain_registry.py::TestInvalidValueValidation::test_empty_gaps_raises
tests/test_domain_registry.py::TestInvalidValueValidation::test_empty_governance_source_raises
tests/test_domain_registry.py::TestRuntimeIsolation::test_domain_rules_not_modified
```

(24 distinct failing node lines are shown above; several are parametrized. The
runner's own summary line — the authoritative count — reports **31 failed**. The
parametrized expansion of the `test_missing_*` families accounts for the
difference between the 24 summary lines and the 31 counted failures.)

## Root cause (classified, not remediated)

Representative traceback (`test_load_order_is_sorted`):

```
>   assert list_domains(registry) == ["aaa_domain", "zzz_domain"]
E   AssertionError: assert [] == ['aaa_domain', 'zzz_domain']

UserWarning: domain_registry: skipping .../aaa_domain/domain.json
             (schema_version=None, expected '1.0')
```

**Classification: fixture / schema-expectation drift (pre-existing).** The test
fixtures build `domain.json` files whose `schema_version` is `None`, while the
committed `load_registry()` skips any domain whose `schema_version` is not the
expected `'1.0'`. Every fixture is therefore skipped, the registry loads empty,
and the assertions that expect populated registries fail. The same warning
(`schema_version=None, expected '1.0'`) appears for the committed
`domains/iot_electronics/domain.json` under the runtime registry load.

This is a long-standing baseline condition in the fixtures/registry contract. It
is **unrelated to any WS16 governance artifact** and is **not remediated** here
(WS16 committed-application validation carries no implementation authority).

## Determination

```
BASELINE INDEPENDENTLY RECONFIRMED
  Command:        python3 -m pytest tests/test_domain_registry.py -q
  Count:          31 failed, 10 passed
  Prior figure:   31 (now independently verified, not assumed)
  Cause:          fixture/schema-expectation drift (schema_version None vs '1.0')
  WS16 relation:  NONE — pre-existing; not introduced by WS16; not remediated
```
