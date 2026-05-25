# F-012 — TC-12 and TC-16: UNVERIFIABLE Ground Truth

**Status:** CLOSED (QUARANTINED) — No action required  
**Severity:** INFORMATIONAL  
**Filed:** 2026-05-26  
**Resolution:** Cases excluded from parity closure metrics. No fixture modification. No benchmark logic modification.

---

## 1. Summary

TC-12 and TC-16 fail benchmark criteria c4 (Confidence Calibration) and c7 (Restraint Check). Investigation established that the ground truth encoded in both fixtures cannot be verified or reconstructed. Both cases are classified **UNVERIFIABLE** and are excluded from parity closure metrics until re-recorded under the new fixture governance standard (see Section 5).

---

## 2. Evidence Chain

### 2.1 Failure Symptoms (R-002, pre-existing)

| Case  | Expected (fixture)                          | Actual (pipeline today)            | Criteria failed |
|-------|---------------------------------------------|------------------------------------|-----------------|
| TC-12 | `LOW / FEASIBILITY_UNCLEAR`                 | `MEDIUM / APPEARS_FEASIBLE_WITH_CAVEATS` | c4, c7     |
| TC-16 | `LOW / SIGNIFICANT_CONCERNS_IDENTIFIED`     | `MEDIUM / APPEARS_FEASIBLE_WITH_CAVEATS` | c4, c7     |

### 2.2 Investigation Command (2026-05-25)

```python
import json
for tc_id in ['TC-12', 'TC-16']:
    with open(f'tests/replay/cases/{tc_id}.json') as f:
        tc = json.load(f)
    raw = tc.get('trace', {}).get('raw_response', 'NOT FOUND')
    prov = tc.get('provenance', {})
    exp_norm = tc.get('expected', {}).get('normalized_output', 'NOT IN EXPECTED')
    print(f'raw_response (first 200): {str(raw)[:200]}')
    print(f'provenance: {json.dumps(prov, ensure_ascii=False)}')
    print(f'expected.normalized_output: {exp_norm}')
```

### 2.3 Output — TC-12

| Field | Value |
|-------|-------|
| `trace.raw_response` | **NOT FOUND** — field absent from fixture |
| `provenance.source_results_file` | `results_20260520_074904.json` |
| `provenance.recorded_at` | `2026-05-20T07:49:04+00:00` |
| `provenance.model` | `claude-sonnet-4-6` |
| `provenance.corpus_mode` | `diagnostic` |
| `expected.normalized_output.confidence_level` | `MEDIUM` |
| `expected.normalized_output.feasibility_signal` | `APPEARS_FEASIBLE_WITH_CAVEATS`

### 2.4 Output — TC-16

| Field | Value |
|-------|-------|
| `trace.raw_response` | **NOT FOUND** — field absent from fixture |
| `provenance.source_results_file` | `results_20260520_074904.json` |
| `provenance.recorded_at` | `2026-05-20T07:49:04+00:00` |
| `provenance.model` | `claude-sonnet-4-6` |
| `provenance.corpus_mode` | `diagnostic` |
| `expected.normalized_output.confidence_level` | `MEDIUM` |
| `expected.normalized_output.feasibility_signal` | `APPEARS_FEASIBLE_WITH_CAVEATS`

### 2.5 Key Observation

Both fixtures share an identical `source_results_file` and `recorded_at` timestamp. They were captured in the same batch run. The `expected.normalized_output` values in both fixtures (`MEDIUM / APPEARS_FEASIBLE_WITH_CAVEATS`) match the pipeline's current output — not the LOW-tier values the benchmark criteria require.

---

## 3. Why Ground Truth Cannot Be Reconstructed

Three independent reasons, each individually sufficient:

**Reason 1 — raw_response absent.**  
`trace.raw_response` is missing from both fixtures. The model's original text output at recording time was never stored. There is no artifact from which to re-derive what the model actually said on 2026-05-20. Reconstruction by re-running the model would produce a new inference, not a replay of the original.

**Reason 2 — expected values are pipeline-derived, not expert-authored.**  
The `expected.normalized_output` fields contain `MEDIUM / APPEARS_FEASIBLE_WITH_CAVEATS`. These match what the pipeline produces today, meaning they were almost certainly captured from the pipeline's own output at recording time rather than authored by a domain expert. No authoring record, rationale document, or reviewer sign-off exists for these expected values. The values cannot be treated as verified ground truth.

**Reason 3 — provenance file not inspectable at this time.**  
`results_20260520_074904.json` is cited as the source. Even if that file were inspected, it would yield the same pipeline output snapshot —"not an independent human judgment of what the correct feasibility signal should be for these ideas. The recording methodology did not include independent expert validation.

**Combined effect:** Neither the model's original output nor an authoritative human judgment is available. Classification of the expected values as ground truth is not defensible. Modification of the fixture expectations would be equally indefensible — there is no verified target to modify toward.

---

## 4. What Was Ruled Out

The following root causes were considered and are **not confirmed**:

| Hypothesis | Status | Reason |
|---|---|---|
| Model drift (model output changed since recording) | Not confirmed | No raw_response to compare against |
| Fixture authoring error (human typed wrong value) | Not confirmed | No evidence of manual authoring; values appear pipeline-derived |
| Pipeline defect (normalizer bug produces wrong signal) | Not confirmed | Pipeline behavior is consistent; no regression detected |
| CLASS 3 mismatch (fixture correct, pipeline regressed) | Not confirmed | Cannot establish fixture correctness without raw_response |

The honest classification is: **unknown root cause, unverifiable fixture**.

---

## 5. Resolution and Governance Actions

### 5.1 Immediate

- TC-12 and TC-16 are **excluded from parity closure metrics** effectively immediately.
- They remain in `tests/replay/cases/` as-is. No modification to fixture files.
- No modification to benchmark logic or scoring.
- R-002 is closed as UNVERIFIABLE (not as PASS or FAIL).
- Excluded cases remain reported separately and must not be silently omitted from benchmark reports.

### 5.2 Fixture Governance Standard (mandatory for all future fixtures)

All future replay fixtures MUST store the following at recording time. A fixture missing any of these fields MUST NOT be used for parity closure.

```
trace.raw_response          -- full model text output, unprocessed
expected.normalized_output  -- pipeline output from the same run
expected.authored_by        -- "pipeline" | "expert:<name>" | "consensus"
expected.rationale          -- if authored_by is expert or consensus, reasoning required
provenance.source_results_file
provenance.recorded_at
provenance.model
provenance.schema_version
```

**Authoring rule:** If `authored_by` is `"pipeline"`, the fixture documents what the pipeline produced -- it is a regression guard, not a correctness assertion. If `authored_by` is `"expert:*"` or `"consensus"`, the fixture asserts correctness and may be used for parity closure.

TC-12 and TC-16, had they been recorded under this standard with `authored_by: "pipeline"`, would have been correctly treated as regression guards rather than ground-truth validators. The current failure would not have been interpreted as a parity gap.

### 5.3 Re-recording Criteria

TC-12 and TC-16 may be re-recorded as valid fixtures if:

1. A domain expert reviews the original idea inputs for each case.
2. The expert determines and documents the correct feasibility signal with written rationale.
3. A fresh run is executed, raw_response is captured, and the full fixture governance standard is met.
4. The new fixture is committed with `authored_by: "expert:<name>"`.

Until those conditions are met, neither case may be included in parity metrics.

---

## 6. Impact on Active Risk Register

| Risk | Previous Status | Updated Status |
|------|----------------|----------------|
| R-002 — TC-12/TC-16 unresolved failures | IN PROGRESS | **CLOSED (QUARANTINED) — UNVERIFIABLE** |

R-001 (v1/v2 parity) is unaffected. TC-12 and TC-16 are now excluded from the denominator of parity closure calculations. Document this exclusion in any future parity report.

---

## 7. Decision Record

**DR-006 — TC-12 and TC-16 exclusion from parity metrics**

| Field | Value |
|-------|-------|
| Decision | Exclude TC-12 and TC-16 from parity closure metrics -- status CLOSED (QUARANTINED) |
| Rationale | Ground truth unverifiable; raw_response absent; expected values not expert-authored |
| Decided by | User, 2026-05-26 |
| Options considered | A: Update fixtures; B: Retire cases; C: Manual authoring; D: Classify UNVERIFIABLE |
| Option selected | D |
| Fixture modified | No |
| Benchmark logic modified | No |
| Re-recording authorized | No -- criteria defined in Section 5.3 |

---

*End of F-012*
