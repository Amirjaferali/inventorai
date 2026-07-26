# WS16 — Test Execution Evidence (Read-Only)

**Purpose.** Record raw commands and results for existing-test execution against
committed source at the WS16 validation base. No test, source, fixture, or
configuration was modified. New failures are separated honestly from pre-existing
baseline failures.

| Item | Value |
|---|---|
| Validation base commit | `143a1ed4dc4022e6bbec935884e1159a4f18be7c` |
| Interpreter / runner | Python 3.11.15 / pytest 9.1.1 |
| Mode | READ-ONLY existing-test execution |

---

## 1. Protected WS9–WS15 suites

```
python3 -m pytest \
  tests/test_workstream_9_single_intent_question_design.py \
  tests/test_workstream_10_question_intent_registry_behavioral_validation.py \
  tests/test_workstream_10_question_intent_registry_interface_contract.py \
  tests/test_workstream_11_question_aware_evaluation_base_red.py \
  tests/test_workstream_12_controlled_unknown_progression_base_red.py \
  -q
```

Result:

```
88 passed, 1 warning in ~0.4s
```

**Disposition: PASS.** All protected WS9–WS15 behavioral/interface suites pass.
Zero failures. The single warning is the pre-existing
`schema_version=None, expected '1.0'` registry-load warning (baseline; see
`BASELINE_RECONFIRMATION.md`).

---

## 2. Session-friendly / display-seam suite

```
python3 -m pytest tests/test_session_friendly_gap_labels.py -q
```

Result:

```
17 passed, 1 warning in ~0.6s
```

**Disposition: PASS.**

---

## 3. Baseline reconfirmation suite

```
python3 -m pytest tests/test_domain_registry.py -q
```

Result:

```
31 failed, 10 passed, 40 warnings in ~1.2s
```

**Disposition: PRE-EXISTING BASELINE (NOT NEW).** Full enumeration, node IDs, and
root-cause classification are in `BASELINE_RECONFIRMATION.md`.

---

## 4. Full test directory (total picture)

```
python3 -m pytest tests/ -q
```

Result:

```
31 failed, 1514 passed, 1 skipped, 1 xfailed, 24 xpassed, 111 warnings in ~5.4s
```

Failure containment check:

```
python3 -m pytest tests/ -q | grep '^FAILED' | sed 's/::.*//' | sort | uniq -c
   31 FAILED tests/test_domain_registry.py
```

**All 31 failures are confined to `tests/test_domain_registry.py`** — the exact
pre-existing baseline. No failure appears in any other file.

---

## 5. New-failure determination

```
ZERO-NEW-FAILURES DETERMINATION
  Total failures (full suite):     31
  Baseline failures (reconfirmed): 31  (all in tests/test_domain_registry.py)
  New failures introduced:          0
  Protected WS9–WS15 suites:       88 passed / 0 failed
```

The WS16 governance artifacts committed to the branch (Owner Decisions, Increment
Contract, representative-journey files, and this validation evidence) are
documentation-only and touch no test, source, fixture, or configuration. The test
picture at the validation base is therefore identical to the pre-existing
baseline: **zero new failures**.

> Note on `xpassed` (24): these are tests marked `xfail` that currently pass.
> They are not failures and are unchanged from the baseline condition; they are
> recorded here for completeness, not remediated.
