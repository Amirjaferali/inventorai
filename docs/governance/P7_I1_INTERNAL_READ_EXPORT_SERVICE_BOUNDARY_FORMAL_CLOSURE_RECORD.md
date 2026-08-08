# P7-I1 — Internal Read/Export Service Boundary — FORMAL CLOSURE RECORD

**Status of THIS record:** governance/documentation-only **closure candidate** — authoritative
if/when this candidate is independently reviewed, Owner-accepted, and merged. It records an
**increment closure only** under the Owner's Standing Phase-7 Authorization (`D-P7-STANDING-01`).
It does **not** close Phase 7, create a public API, or satisfy any later Phase-7 obligation.

## 1. Identity and lineage (verified live, read-only)

- **Increment:** P7-I1 — Internal Read/Export Service Boundary (P7-C §8 first slice).
- **Authority:** Standing Phase-7 Authorization `D-P7-STANDING-01`; contract-of-record P7-C
  (`docs/governance/PHASE_7_API_AND_INTEGRATION_FOUNDATION_P7C_CONTRACT.md`, `D-P7C-01`).
- **Bounded contract established:** `docs/governance/P7_I1_INTERNAL_READ_EXPORT_SERVICE_BOUNDARY_INCREMENT_CONTRACT.md`
  — candidate `e5479e9` independently reviewed (verdict A) + Owner-accepted, **merged PR #402**,
  merge `004109745604e9ee860a4c3342f6804d977dd710` (parents `653f66a`+`e5479e9`; tree
  `0d99df00973d4c35223aa11811491cd587730112`); post-merge tree identical to the reviewed candidate.
- **Implementation:** candidate `acf0c46` (independent verdict **B — one required pre-merge
  correction**) → corrected candidate **`8f30f4fa42420d6a87d13bc42d96573cb631a727`** (tree
  `fba951ed86a269e2487352e206b3de65979e6e65`), independent re-review **FINAL VERDICT A**,
  Owner-accepted, **merged PR #403**, merge
  **`94ccccd4399847d5fc0fc477f24bed5145d9a7d3`** (parents `0041097`+`8f30f4f`; merged tree
  `fba951e` == accepted candidate tree → **post-merge verified**).
- **Changed paths (implementation):** exactly `engine/read_export_service.py` +
  `tests/test_p7_i1_read_export_service.py` (+448 insertions).
- **Superseded implementation candidate `acf0c46`:** EVIDENCE ONLY — **NOT accepted, NOT merged**
  (preserved as tag `evidence/p7i1-impl-superseded-acf0c46`).

## 2. What was delivered

One thin, Flask-free internal application/use-case seam `engine/read_export_service.py` with two
read-side use cases, consumed by future internal callers so the future P7-I2 public API and adapters
need not couple to engine/store internals:

1. **Authorized durable Project Read** — `get_authorized_project_read(store, project_id, account_id)`
   returns the validated `ProjectRecordContract` via the durable `store.load_contract` path (IR-2),
   or raises the generic non-enumerating `ProjectAccessDenied` (fail-closed).
2. **Distinct internal Structured Export** — `produce_project_export(store, project_id, account_id)`
   returns a deterministic, data-minimized outward projection composed from **durable record data
   AND the canonical domain support-state** (`store.load_reconstruction_inputs` → `confirmed_domain`
   classified by `engine.domain_activation.support_state`), semantically distinct from the Project
   Read, with no public/export version identity or field-name freeze (IR-6).

Authorization consumes the existing durable ownership fact `store.load_owner` plus an explicit
caller identity: authorized ⇔ durable owner present AND `owner == account_id`, else fail-closed;
a NULL durable owner is not auto-authorized (IR-5). The seam consumes an already-established store
and constructs none (IR-1), imports no Flask/`request`/`session`/`SESSION_STORE`, and mutates no
governed project/business state. Existing web behavior and `web/app.py` are unchanged (IR-3/IR-4).

## 3. Closure obligation matrix (DELIVERED AND VERIFIED — independently reproduced at `94ccccd`)

| Obligation | Status |
|---|---|
| Authorized durable Project Read | DELIVERED AND VERIFIED |
| Explicit caller identity | DELIVERED AND VERIFIED |
| Durable ownership authorization (`load_owner`) | DELIVERED AND VERIFIED |
| Fail-closed cross-owner | DELIVERED AND VERIFIED |
| None/empty identity denial | DELIVERED AND VERIFIED |
| NULL-owner denial | DELIVERED AND VERIFIED |
| Missing project denial | DELIVERED AND VERIFIED |
| Generic non-enumerating denial | DELIVERED AND VERIFIED |
| `load_owner` failure fail-closed | DELIVERED AND VERIFIED |
| Durable validated `load_contract` path | DELIVERED AND VERIFIED |
| `from_state` live-reference guard | DELIVERED AND VERIFIED |
| Structured Export distinct from Project Read | DELIVERED AND VERIFIED |
| Canonical domain support-state composition | DELIVERED AND VERIFIED |
| Deterministic export | DELIVERED AND VERIFIED |
| Data-minimized outward projection | DELIVERED AND VERIFIED |
| No public export version freeze | DELIVERED AND VERIFIED |
| Flask-free | DELIVERED AND VERIFIED |
| No SESSION_STORE | DELIVERED AND VERIFIED |
| No datastore construction inside seam | DELIVERED AND VERIFIED |
| No `web/app.py` change | DELIVERED AND VERIFIED |
| Non-mutation (read + export) | DELIVERED AND VERIFIED |
| No domain activation | DELIVERED AND VERIFIED |
| No registry mutation | DELIVERED AND VERIFIED |
| No public API | DELIVERED AND VERIFIED |
| No P7-I2 work | DELIVERED AND VERIFIED |
| D-FPC-MAP-06 | DELIVERED AND VERIFIED |
| Lean (2 changed paths) | DELIVERED AND VERIFIED |

**Test evidence (independently reproduced at the merged tip `94ccccd`):** focused
`tests/test_p7_i1_read_export_service.py` **22 passed**; regression anchors
(`test_p4_0_record_contract` / `test_p4_1a_record_store` / `test_p4_2_session_reconstruction` /
`test_p5_3_project_ownership_authorization` / `test_deliverable_assembler`) **69 passed**; full
suite **2047 passed / 1 skipped / 1 xfailed / 0 failed** (pre-existing skip/xfail/warnings).

## 4. Retained non-blocking observations (not blockers)

1. Post-authorization `load_contract` exceptions propagate to the durable owner; no enumeration
   leak (an unauthorized caller is denied before any contract/recon read — test-proven).
2. Defensive `getattr(contract, "assertions", [])` is cosmetic/unreachable for a canonical
   `ProjectRecordContract`.
3. Some malformed/blank domain variants were independently verified but not all have dedicated
   candidate tests (the canonical None/blank/unknown/recognized/activated cases are tested).
4. Historical/local evidence artifacts (bundles) remain untracked working artifacts.
5. Superseded candidate `acf0c46` is evidence only and MUST NOT be presented as accepted
   implementation.

## 5. Boundary — what this closure does NOT do

- **Phase 7 is NOT closed** — it remains OPEN / IN PROGRESS. The mandatory §25 **Phase-7
  Remaining-Obligation / Exit-Criteria Review** remains reserved before any P7-CLOSE.
- **No public API exists.** P7-I1 is an internal seam only.
- **No later Phase-7 obligation is satisfied** — API security, versioning, machine/API identity,
  scopes, rate limits, audit, adapters, import/export, external integrations remain governed by
  P7-C and later accepted increments.
- **No P7-I2 work is authorized here.** The next-eligible increment is **P7-I2 — Versioned
  Read/Export Public API + first-public-exposure security baseline — NOT STARTED**, requiring its
  own bounded contract + review sequence under `D-P7-STANDING-01` before code begins.

## 6. Result

**P7-I1: IMPLEMENTED / INDEPENDENTLY REVIEWED (A) / MERGED (PR #403, `94ccccd`) / POST-MERGE
VERIFIED / FORMALLY ACCEPTED AND CLOSED** (increment closure only; authoritative if/when this
governance candidate is merged). There is no active implementation increment. Phase 7 remains OPEN.
