# P7-I2 — Versioned Read/Export Public API + First-Public-Exposure Security Baseline — FORMAL CLOSURE RECORD

**Status of THIS record:** governance/documentation-only **closure candidate** — authoritative if/when
independently reviewed, Owner-accepted, and merged. It records an **increment closure only** under the
Owner's Standing Phase-7 Authorization (`D-P7-STANDING-01`). It does **not** close Phase 7, does not
start P7-I3, does not perform the §25 Phase-7 exit review, and does not register PSRR.

## 1. Identity and lineage (verified live, read-only at the merged tip)

- **Increment:** P7-I2 — Versioned Read/Export Public API + first-public-exposure security baseline (P7-C; second Phase-7 increment).
- **Authority:** `D-P7-STANDING-01`; P7-C contract-of-record (`D-P7C-01`).
- **Bounded contract established:** corrected candidate `ed72131` (independent verdict A + Owner-accepted) → **contract merged PR #405** → branch tip `7abdd06f1765fc2ecf16b7341a3986870e6dc7ae`. Superseded pre-review candidate `4933c26` is evidence only (NOT accepted).
- **Implementation:** accepted candidate **`cd46c7f5a973c62032d823d0e60f997c99b993cf`** (parent `7abdd06`; tree `a299bce1cc6e58b873fb3e20a1e6f98a7b1ab1ae`), independent implementation review **verdict A**, Owner-accepted, **merged PR #406**, merge **`5971b7a1c35186aa6bdb425b6846bd633d5f8b11`** (parents `7abdd06`+`cd46c7f`; merged tree `a299bce` == accepted candidate tree → **post-merge verified**).
- **Changed paths (implementation):** exactly `engine/account_store.py` + `web/api_v1.py` + `web/app.py` (blueprint mount) + `tests/test_p7_i2_public_api.py` (**+1076 / −0**).

## 2. What was delivered

A **versioned, read-only public API** (`web/api_v1.py`, blueprint `url_prefix="/api/v1"`, mounted in
`web/app.py` by registration only) exposing exactly the two product surfaces —
`GET /api/v1/projects/<project_id>` (Project Read) and `GET /api/v1/projects/<project_id>/export`
(Structured Export) — that **consumes the P7-I1 seam** `engine.read_export_service`
(`get_authorized_project_read` / `produce_project_export` / `ProjectAccessDenied`) with no
business-logic duplication. First-public-exposure security baseline: a distinct machine/API principal
(`Authorization`-header credential, never the browser session; bound to one `owner_account_id`;
token-style **hash-only** secret; issuance/revocation/expiry/rotation + bound-account-status
enforcement) with a single `project:read` scope; **API + export version identity** (`api_version`,
`export_contract_version`); a stable **non-enumerating** error envelope (cross-owner ≡ missing);
**request/correlation identity** (`request_id`; malformed caller value replaced); a durable minimal
**access/security audit** (`access_audit`; fail-closed on audit-write failure); and **two-tier rate
limiting** reusing the hardened atomic `record_rate_attempt` — a **pre-auth** limiter on a
bounded/normalized/hash-derived subject of the *presented* credential id (before secret verification)
plus a **post-auth `api_read`** limiter (both fail-closed). `api_credentials` and `access_audit` are
additive tables in the **existing** `SqliteAccountStore` schema lifecycle; no route handler performs
DDL/migration; no project/business-state mutation; no writes/import; no P7-I3/adapter code.

## 3. Closure obligation matrix (DELIVERED AND VERIFIED — reproduced at `5971b7a`)

| # | Obligation | Status |
|---|---|---|
| 1 | Exactly two GET public surfaces | DELIVERED AND VERIFIED |
| 2 | P7-I1 seam reused | DELIVERED AND VERIFIED |
| 3 | Machine/API auth distinct from browser session | DELIVERED AND VERIFIED |
| 4 | Owner-bound authorization (cross-owner isolation) | DELIVERED AND VERIFIED |
| 5 | `project:read` scope | DELIVERED AND VERIFIED |
| 6 | Hash-only high-entropy credential secret | DELIVERED AND VERIFIED |
| 7 | Issuance | DELIVERED AND VERIFIED |
| 8 | Revocation | DELIVERED AND VERIFIED |
| 9 | Expiry | DELIVERED AND VERIFIED |
| 10 | Rotation | DELIVERED AND VERIFIED |
| 11 | Account-status enforcement | DELIVERED AND VERIFIED |
| 12 | Pre-auth rate limit (before secret verification) | DELIVERED AND VERIFIED |
| 13 | Authenticated (`api_read`) rate limit | DELIVERED AND VERIFIED |
| 14 | Fail-closed rate-limit failure | DELIVERED AND VERIFIED |
| 15 | Stable error envelope | DELIVERED AND VERIFIED |
| 16 | Non-enumeration (cross-owner ≡ missing) | DELIVERED AND VERIFIED |
| 17 | Correlation/request identity | DELIVERED AND VERIFIED |
| 18 | Durable access/security audit | DELIVERED AND VERIFIED |
| 19 | Fail-closed audit-write failure | DELIVERED AND VERIFIED |
| 20 | API version identity | DELIVERED AND VERIFIED |
| 21 | Export contract version identity | DELIVERED AND VERIFIED |
| 22 | Data-minimized Project Read | DELIVERED AND VERIFIED |
| 23 | Structured Export consumes P7-I1 | DELIVERED AND VERIFIED |
| 24 | No route-owned schema migration | DELIVERED AND VERIFIED |
| 25 | No project-state mutation | DELIVERED AND VERIFIED |
| 26 | No write/import | DELIVERED AND VERIFIED |
| 27 | No P7-I3 | DELIVERED AND VERIFIED |
| 28 | D-FPC-MAP-06 | DELIVERED AND VERIFIED |
| 29 | Lean | DELIVERED AND VERIFIED |

**Test evidence (independently reproduced at the merged tip `5971b7a`):** P7-I2 focused
`tests/test_p7_i2_public_api.py` **36 passed**; P7-I1 + ownership + record-store regressions **52
passed**; full suite **2083 passed / 1 skipped / 1 xfailed / 0 failed** (P7-I1-closed baseline 2047 +
36 new P7-I2 tests; the skip/xfail/warnings are pre-existing/environmental).

## 4. Retained non-blocking observations (not blockers)

1. **Governance recording lag** after PR #405 (contract merged but current-truth still said "candidate pending") — **CORRECTED by this synchronization.**
2. Post-auth (`api_read`) limiter ordering: the scope check occurs before the `api_read` limiter — accepted as non-blocking.
3. Residual micro-timing on an unknown credential id — accepted as non-blocking.
4. `API_CREDENTIAL_STATUSES` is currently inert/documentary; no `Authorization`-header request is denied before the limiter because there is no presented id — accepted as non-blocking.
5. `access_audit` is append-only with **no retention/cleanup path** — preserved as a **later obligation**; audit retention is **NOT** solved here.

## 5. Boundary — what this closure does NOT do

- **Phase 7 is NOT closed** — it remains OPEN / IN PROGRESS. The mandatory §25 **Phase-7
  Remaining-Obligation / Exit-Criteria Review** remains RESERVED and is **not** performed here.
- **Not all Phase-7 obligations are complete** — quotas, import/write, webhooks/file-exchange,
  integration adapters (P7-I3), partner/external sandbox, monitoring, broad abuse controls (incl.
  IP/network-origin), and audit retention remain governed by P7-C and later increments.
- **P7-I3 is NOT STARTED** — next-eligible only: *Canonical Export + Local/Reference Adapter Proof
  (outbound-only, non-mutating)*, requiring its own bounded contract + review sequence.
- **PSRR is NOT started** and remains a future governance registration after Phase-7 formal closure —
  not lost, not pre-satisfied.

## 6. Result

**P7-I2: CONTRACT ESTABLISHED / MERGED (PR #405) / IMPLEMENTED / INDEPENDENTLY REVIEWED (A) / OWNER
ACCEPTED / MERGED (PR #406, `5971b7a`) / POST-MERGE VERIFIED / DELIVERED / FORMALLY ACCEPTED AND CLOSED**
(increment closure only; authoritative if/when this governance candidate is merged). There is no active
implementation increment. **Next-eligible: P7-I3 — NOT STARTED. Phase 7 remains OPEN.**
