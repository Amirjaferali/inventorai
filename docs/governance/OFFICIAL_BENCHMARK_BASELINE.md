# OFFICIAL BENCHMARK BASELINE

**Status:** ACTIVE  
**Authority Level:** Level 2 (Governance Record)  
**Commit established:** e547eee  
**Date:** 2026-05-31  
**Author:** Incoming agent — established from repository evidence  

---

## 0. BENCHMARK GOVERNANCE PRINCIPLES

These principles govern how benchmark results are collected, reported, and interpreted across all sessions. They apply to all agents, all handover documents, and all governance artifacts.

**Principle 1 — Official benchmark ≠ Full test suite.**
The official benchmark is a defined subset of tests enforcing architectural invariants. The full test suite is broader. They are not interchangeable.

**Principle 2 — Benchmark success does not imply full-suite success.**
A clean official benchmark run confirms invariants are intact. It does not confirm that the full suite is passing. Both must be reported separately.

**Principle 3 — Full-suite success does not replace benchmark reporting.**
A clean full-suite run does not satisfy the benchmark reporting requirement. The official benchmark suite must be run and reported explicitly by name.

**Principle 4 — Every reported result must include all of the following fields:**

| Field | Example |
|-------|---------|
| Commit hash | `e547eee` |
| Suite name | `InventorAI Core Invariants Suite (WPS001)` |
| Exact command | `python -m pytest tests/test_wps001_invariants.py -v` |
| Collected count | `21 collected` |
| Passed | `20 passed` |
| Failed | `0 failed` |
| Skipped | `1 skipped` |
| Xfailed | `0 xfailed` |
| Xpassed | `0 xpassed` |

A result missing any field is incomplete and cannot be used as governance evidence.

**Principle 5 — Reporting only "tests passed" is prohibited.**
The phrase "tests passed" without suite name, command, commit hash, and counts is not a governance claim. It is noise. It must not appear in handover documents, session reports, or governance artifacts.

---

## 1. OFFICIAL BENCHMARK SUITE NAME

**InventorAI Core Invariants Suite**

Defined by: `tests/test_wps001_invariants.py`  
Suite identifier: `WPS001`

This is the single authoritative benchmark for session-to-session governance reporting. All handover documents, governance artifacts, and session reports MUST reference this suite by name when claiming "benchmark passed."

---

## 2. EXACT COMMAND TO RUN

```bash
python -m pytest tests/test_wps001_invariants.py -v
```

For governance reporting, always use `-v` (verbose) so individual test names appear in output. The `-q` flag is permitted for quick checks but NOT for governance evidence.

**Minimum required output fields in any governance report:**
- Command used (exact)
- Commit hash at time of run (`git rev-parse HEAD`)
- passed / failed / xfailed / xpassed counts
- Any FAILED test names listed explicitly

---

## 3. TESTS INCLUDED IN OFFICIAL BENCHMARK

All tests in `tests/test_wps001_invariants.py`. At HEAD `e547eee`, this file contains **21 collected tests** across 6 invariant groups:

| Group | ID | Test Name |
|-------|----|-----------|
| WeakInputLevelBlock | INV001 | test_substantive_input_can_advance |
| WeakInputLevelBlock | INV001 | test_weak_inputs_never_produce_pass_transition |
| WeakInputLevelBlock | INV001 | test_weak_inputs_never_reach_level_2 |
| WeakInputLevelBlock | INV001 | test_weak_inputs_never_satisfy_deliverable_eligibility |
| WeakInputLevelBlock | INV001 | test_weak_patterns_return_asserted_not_reasoned |
| BlockPreventsAdvancement | INV002 | test_level_1_to_2_allowed_with_reasoned_mechanism |
| BlockPreventsAdvancement | INV002 | test_level_1_to_2_blocked_by_asserted_mechanism |
| GapLifecycle | INV004 | test_closed_gap_does_not_reopen |
| GapLifecycle | INV004 | test_gap_constants_are_distinct |
| AuditLog | INV005 | test_iteration_log_grows_with_each_call |
| AIBoundary | INV007 | test_assess_response_deterministic |
| AIBoundary | INV007 | test_assess_response_no_ai_advisor |
| AIBoundary | INV007 | test_evaluate_transition_deterministic |
| AIBoundary | INV007 | test_evaluate_transition_no_ai_advisor |
| AIBoundary | INV007 | test_integrate_response_no_ai_advisor |
| ProductionPathImports | INV010 | test_no_forbidden_imports[engine/ai_advisor.py] |
| ProductionPathImports | INV010 | test_no_forbidden_imports[engine/deliverable_assembler.py] |
| ProductionPathImports | INV010 | test_no_forbidden_imports[engine/domain_rules.py] |
| ProductionPathImports | INV010 | test_no_forbidden_imports[engine/idea_state.py] |
| ProductionPathImports | INV010 | test_no_forbidden_imports[engine/progression_loop.py] |
| ProductionPathImports | INV010 | test_no_forbidden_imports[web/app.py] |

**What these invariants enforce:**
- Weak inputs cannot advance maturity level (INV001)
- Asserted mechanism blocks Level 1→2 transition (INV002)
- Closed gaps do not reopen (INV004)
- Every iteration is logged (INV005)
- AI layer cannot control any gate decision (INV007)
- Production engine files contain no forbidden AI imports (INV010)

---

## 4. TESTS EXCLUDED FROM OFFICIAL BENCHMARK

The following test files exist in `tests/` but are NOT part of the official benchmark. They are tracked separately as the **Full Suite**.

| File | Test Count (approx) | Purpose | Benchmark Status |
|------|---------------------|---------|-----------------|
| `test_progression_benchmark.py` | ~50 | Core engine logic, transition rules, response quality, gap status | EXCLUDED — Full Suite only |
| `test_assess_response_adversarial.py` | ~40 | Adversarial edge cases for assess_response() | EXCLUDED — Full Suite only |
| `test_assess_response_replay.py` | ~15 | Replay matrix for response classification | EXCLUDED — Full Suite only |
| `test_architecture_guardrails.py` | ~12 | Domain-agnosticism and structural invariants | EXCLUDED — Full Suite only |
| `test_domain_registry.py` | ~35 | Domain registry loading, validation, isolation | EXCLUDED — Full Suite only |
| `test_f011_progression_quality_gate.py` | ~10 | F011 domain-specific progression quality | EXCLUDED — Full Suite only |
| `test_fdc001_contract.py` | ~40 | FDC001 deliverable contract structure | EXCLUDED — Full Suite only |
| `test_ilt001_level2_transition_contract.py` | ~6 | ILT-001 Level 1→2 transition contract | EXCLUDED — Full Suite only |
| `test_deliverable_assembler.py` | unknown | Deliverable assembly | EXCLUDED — Full Suite only |

**Total full suite:** 205 tests collected (at HEAD e547eee)

---

## 5. DISTINCTION BETWEEN SUITES

### 5.1 Official Benchmark (Core Invariants)
- **File:** `tests/test_wps001_invariants.py`
- **Command:** `python -m pytest tests/test_wps001_invariants.py -v`
- **Purpose:** Enforce the 6 architectural invariants that must NEVER be violated, regardless of any other work in progress.
- **Expectation:** 0 failures at all times. Any failure here is a blocker.
- **Count:** 21 tests

### 5.2 Progression Benchmark
- **File:** `tests/test_progression_benchmark.py`
- **Command:** `python -m pytest tests/test_progression_benchmark.py -v`
- **Purpose:** Validate core engine logic — response quality scoring, gap lifecycle, transition gate rules, idea summary invariants.
- **Expectation:** All pass. Failures indicate engine regression.
- **Note:** This is what earlier sessions called "the benchmark" without naming it explicitly.

### 5.3 Full Suite
- **Command:** `python -m pytest tests/ -v`
- **Purpose:** Complete health check — all 205 tests across all files.
- **Expectation:** Known failures documented in Section 6. Must be run before any commit that touches engine code.
- **Count:** 205 tests

### 5.4 Governance / Documentation Checks
- There is currently NO automated test suite for governance document structure or completeness.
- Governance validation is performed manually via `ls docs/governance/` and `wc -c` file size checks.
- This is a known gap. Automation is deferred to a future phase.

---

## 6. CURRENT KNOWN RESULTS AT HEAD e547eee

### 6.1 Official Benchmark (WPS001)

```
Command: python -m pytest tests/test_wps001_invariants.py -v
Commit:  e547eee
Result:  UNKNOWN — not yet run as isolated suite at this HEAD
```

**Action required:** Run this command at HEAD and record result in this document before next commit.

**Expected result based on bisect evidence:** At `4c6da9b` (last code commit), `test_wps001_invariants.py` produced **20 passed, 1 skipped, 0 failed**. No engine code changed between `4c6da9b` and `e547eee`. Expected result at HEAD: same.

### 6.2 Full Suite

```
Command: python -m pytest tests/ -q
Commit:  e547eee
Result:  14 failed, 166 passed, 1 xfailed, 24 xpassed
```

**Two explicitly named failures:**
- `test_wps001_invariants.py::TestWPS001_INV001_WeakInputLevelBlock::test_substantive_input_can_advance`
- `test_wps001_invariants.py::TestWPS001_INV004_GapLifecycle::test_closed_gap_does_not_reopen`

**Remaining 12 failures:** Not yet individually identified. Appear in other test files. Investigation deferred — see Section 7.

---

## 7. CLASSIFICATION OF THE 14 FAILURES

### 7.1 Two WPS001 Failures

| Test | Classification |
|------|---------------|
| `INV001::test_substantive_input_can_advance` | **UNTRIAGED TEST DEBT** |
| `INV004::test_closed_gap_does_not_reopen` | **UNTRIAGED TEST DEBT** |

**Rationale:** These appear in the official benchmark suite. They were NOT present at `4c6da9b` when the suite was run in isolation (20 passed, 1 skipped). The discrepancy suggests a test interaction effect when run as part of the full suite — possibly shared fixture state or import side effects. Root-cause analysis has not been performed. We cannot yet determine whether these are regressions, test interaction artifacts, misconfigured tests, or obsolete tests. Classification will be updated after triage.

**These are NOT accepted failures. They are NOT blockers for governance work. They ARE blockers for any engine code modification.**

### 7.2 Remaining 12 Failures

| Classification | Rationale |
|---------------|-----------|
| **OUTSIDE OFFICIAL BENCHMARK** | They do not appear in `test_wps001_invariants.py` |
| **UNTRIAGED TEST DEBT** | Individual test names not yet identified; root-cause analysis not performed; cannot determine whether technical debt, regression, obsolete test, misconfiguration, or expected failure |
| **NOT blockers for governance work** | Governance tasks (updating MASTER-HANDOVER.md, GOVERNANCE-ROADMAP.md) do not require full suite to pass |
| **ARE blockers for engine code changes** | Full suite must be clean before any engine modification |

**Action required:** Individual identification of all 14 failures with their file and test name. This is deferred — not forgotten. Must be completed before AB-001 or AB-005 resolution is authorized.

---

## 8. RULES FOR FUTURE REPORTING

### 8.1 Mandatory fields in any benchmark claim

Every session report, handover document, or governance artifact that makes a benchmark claim MUST include:

```
Suite:   [Official Benchmark | Progression Benchmark | Full Suite]
Command: [exact command used]
Commit:  [git rev-parse HEAD output]
Result:  [N passed, N failed, N xfailed, N xpassed]
Failed:  [list each failed test name, or "none"]
```

Omitting any field invalidates the claim.

### 8.2 Forbidden reporting patterns

The following are PROHIBITED in all governance documents:

- "Benchmark passed" without naming the suite
- "27 passed" without specifying which suite and command
- Comparing results from different suites as equivalent (e.g., "last session: 27 passed, this session: 166 passed — improvement")
- Reporting full suite results as if they are invariant suite results
- Claiming "0 failures" when only a subset of tests was run

### 8.3 Suite equivalence rule

Results from different suites are NOT comparable. The following comparisons are invalid:

| Invalid comparison | Why invalid |
|-------------------|-------------|
| WPS001 (21 tests) vs Full Suite (205 tests) | Different scope |
| Progression Benchmark vs WPS001 | Different invariants measured |
| Any suite run with `-q` vs `-v` | Output format differs; `-q` suppresses failure names |

### 8.4 Handover document requirement

Every handover document MUST include the official benchmark result (Section 6.1 format) as a mandatory field. A handover document that reports only full suite results without an isolated WPS001 run is incomplete.

### 8.5 Pre-commit requirement

Before any commit that modifies engine code:
1. Run `python -m pytest tests/test_wps001_invariants.py -v` — must show 0 failed
2. Run `python -m pytest tests/ -v` — record all failures by name
3. Confirm no new failures introduced by the change
4. Include both results in the commit message or linked governance record

---

## 9. OPEN ACTIONS FROM THIS DOCUMENT

| ID | Action | Priority | Owner |
|----|--------|----------|-------|
| BB-001 | Run `python -m pytest tests/test_wps001_invariants.py -v` at HEAD e547eee and record exact result in Section 6.1 | HIGH — first action | Agent |
| BB-002 | Identify all 14 failures by name (run `python -m pytest tests/ -v 2>&1 \| grep FAILED`) | HIGH — before any engine work | Agent |
| BB-003 | Investigate INV001 and INV004 failures — determine if caused by test interaction or genuine engine regression | HIGH — before AB-001/AB-005 | Agent + Owner approval |
| BB-004 | Update MASTER-HANDOVER.md benchmark field to reference WPS001 suite and this document | MEDIUM | Agent |

---

## 10. DOCUMENT HISTORY

| Version | Date | Commit | Change |
|---------|------|--------|--------|
| v1.0 | 2026-05-31 | e547eee (established at) | Initial creation — evidence-based baseline from full suite analysis |

---

*Evidence source: 11 terminal screenshots showing `--collect-only` output (205 tests), bisect result at `4c6da9b` (20 passed, 1 skipped), full suite run at HEAD (14 failed, 166 passed).*  
*No engine code was modified to produce this document.*