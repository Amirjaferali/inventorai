# P7-I2 — VERSIONED READ/EXPORT PUBLIC API + FIRST-PUBLIC-EXPOSURE SECURITY BASELINE — BOUNDED INCREMENT CONTRACT

**Repository status of THIS document:** **CANONICAL P7-I2 CONTRACT PUBLICATION CANDIDATE (corrected)** —
**PENDING independent pre-merge contract re-review, Owner acceptance, merge, and post-merge
verification.** It is **NOT** finally established for implementation. Under the Owner's **Standing
Phase-7 Authorization** (`D-P7-STANDING-01`), P7-I2 implementation **MUST NOT begin** until the
required pre-merge review sequence completes (Permanent Execution-Gate Safety Lock). This corrected
candidate supersedes `4933c268aab1dc78a4c12870004920af4fb307e8` (independent verdict **B — required
pre-merge corrections**; preserved as evidence, **DO NOT MERGE**); it integrates the required
corrections (pre-auth rate limiting; schema-initialization boundary; RED-plan additions) and preserves
every independently-accepted decision.

- **Authority:** `D-P7-STANDING-01`; contract-of-record P7-C (`docs/governance/PHASE_7_API_AND_INTEGRATION_FOUNDATION_P7C_CONTRACT.md`, `D-P7C-01`).
- **Basis tip (verified read-only):** `afb1ba06981838e0e982d792d764cf0281bd2cc0` (P7-I1 closure merge PR #404; tree `ef3c850`).
- **P7-I1:** FORMALLY CLOSED. **P7-I2:** NOT STARTED. **P7-I3:** NOT STARTED. **Phase 7:** OPEN. **Implementation Gate Lock:** ACTIVE.

## 1. Purpose and scope

P7-I2 exposes the already-established P7-I1 internal read/export seam through a **governed, versioned,
read-only public API** — the **Versioned API Contracts** layer for the two initial product surfaces —
with the **first-public-exposure security baseline**. It does **not** duplicate P7-I1 business logic;
P7-I3 (canonical export + local/reference adapter proof) remains separate. Architecture:
Core Engine → Internal Service Layer (P7-I1) → **Versioned API Contracts (P7-I2)** → Integration
Adapters (P7-I3) → External Applications.

## 2. Public product surfaces (frozen — exactly two)

1. **Project Read representation.**
2. **Versioned Structured Output / Export.**

Domain/support-state and Evidence/Provenance remain **fields/projections within** those surfaces.
No standalone V1 resource for Domain/support-state, Evidence, Provenance, Gap, Risk, Validation, or
Subsystem (deferred unless separately authorized).

## 3. P7-I1 reuse — mandatory (ALREADY OWNED — CONSUME)

Public handlers **consume** the live P7-I1 seam `engine/read_export_service.py`:
`get_authorized_project_read(store, project_id, account_id)` and
`produce_project_export(store, project_id, account_id)` (both raise the generic `ProjectAccessDenied`).
P7-I2 **must not** reimplement ownership authorization, durable Project Read, Structured Export
composition, or canonical domain support-state composition. The seam's `account_id` parameter is the
join point: the resolved machine principal's **bound owner account** is passed as `account_id`, so the
seam's existing `owner == account_id` check enforces cross-owner isolation. **If the seam interface
proves insufficient for a safe public API → STOP and report; do not modify P7-I1 in implementation.**

## 4. Exact V1 route/method shape (frozen)

- `GET /api/v1/projects/<project_id>` → Project Read representation.
- `GET /api/v1/projects/<project_id>/export` → Structured Export.

**GET only** (read-only). No existing `/api`/`/v1` route exists today, so no route/version conflict.
Any non-GET method proposal → STOP. No collection endpoint (no pagination surface).

## 5. Public API + export version identity (owned here)

- **API version identity:** `v1` path segment + explicit `api_version` in every response envelope.
- **Structured Export public contract version identity:** explicit `export_contract_version` in the export envelope (defines the version identity deferred in P7-I1, IR-6).
- **Compatibility (accepted V1):** additive, backward-compatible changes only within `v1`; a **breaking change** requires a **new version** (`v2`), never a silent `v1` change.
- **Deprecation discipline (minimum):** any future removal of a `v1` element requires a documented deprecation path. No lifecycle-management platform is designed now.

## 6. Machine/API principal (distinct from human session; P7-I2 CANONICAL RESPONSIBILITY)

The public API principal is a **machine/API credential**, **distinct** from the human browser session;
it **MUST NOT** reuse `_current_account`, the Flask signed-cookie session, or browser login cookies.
Minimum V1 model:
- A credential = **public `credential_id`** + a **high-entropy secret** shown **only at issuance**; the store persists **only a hash/verifier** of the secret. **Hashing qualification:** use the existing high-entropy **token-style fast hash** pattern (as used for email tokens), **not** the password scrypt path — the secret is already high-entropy, so a slow KDF is unnecessary (D-FPC-MAP-06: EXTEND MINIMALLY; no new IAM platform).
- Bound to exactly **one owner account** (`owner_account_id`) on whose behalf it acts.
- Carries explicit **least-privilege scopes** (§7).
- Supports **revocation** (durable), an **expiry/bounded-lifecycle** field, and a **rotation path** (issue-new + revoke-old).
- Authentication: caller presents the credential via an `Authorization` header (never in URL/query); the server resolves `credential_id`, applies the **pre-auth rate limit (§10.A)**, then verifies the secret against the stored hash and checks not-revoked/not-expired/bound-account-active. Exact header/token encoding is an implementation detail bounded by these principles (no secret logged, no secret in URL/query).
- Principal taxonomy beyond this minimum (delegated/service/org/partner) remains **deferred**.

## 7. Machine ↔ owner authorization + scopes

- **Authorization relationship (grounded in existing authority):** a credential is bound to one `owner_account_id`; the handler resolves credential → bound `owner_account_id` → calls the P7-I1 seam with that `account_id`. The seam returns the project only when its durable owner equals that account. **A machine principal never gains access merely by knowing a project id; cross-owner isolation is mandatory and enforced by the consumed seam.** No organization/workspace/team model is invented (none exists in the repo).
- **Scopes (minimum):** a **single read scope `project:read`** authorizes both surfaces — both are read-only projections of the same owned project with identical sensitivity and owner-authorization, so separate scopes add no safety and violate Lean. **No write/mutate scopes** exist in P7-I2. Insufficient scope → deny (§11).

## 8. Public representation discipline (data-minimized)

- **Project Read public envelope:** `api_version` + resource identity (`idea_id`) + a **data-minimized projection** of the seam's `ProjectRecordContract` (NOT a blind `to_dict()`; the exact minimal field set is fixed at implementation) + the correlation id. Never exposes raw SQLite rows, internal schema, Flask/session details, private implementation-only fields, secrets, or credential material.
- **Structured Export public envelope:** `api_version` + `export_contract_version` + the P7-I1 Structured Export payload (consumed, not reconstructed) + the correlation id.
- Expose no more than required.

## 9. Stable public error envelope (non-enumerating)

One stable V1 error shape, e.g. `{ "error": { "code": <stable_code>, "message": <generic>, "request_id": <correlation_id> } }` (exact spelling fixed at implementation). Stable codes cover: unauthenticated; forbidden (insufficient scope); not-available (project); invalid request; rate-limited; internal error. **Never** leak exception messages, SQL, stack traces, or ownership/existence distinctions. **Non-enumeration:** cross-owner access and missing project **collapse to one identical generic "not available" response** (mirroring the web `_deny_project` precedent + the seam's generic `ProjectAccessDenied`). Authentication failures return a generic unauthenticated response; scope failures a generic forbidden response — neither reveals project existence.

## 10. Rate limiting — two clearly distinguished tiers (CORRECTED)

Both tiers use the existing hardened atomic counter `account_store.record_rate_attempt` (P5-2-PRE-01;
`BEGIN IMMEDIATE`, serialized). Both fail-closed on store error (deny). **IP/network-origin rate
limiting is NOT PART OF P7-I2** (no existing canonical precedent; new privacy/retention concerns; broad
distributed abuse control is a later P7-C obligation — DEFERRED / preserved for the §25 review).

**10.A — PRE-AUTH limiter (before secret verification).**
Flow: **presented credential identifier → validate/bound input → derive bounded subject digest → atomic
pre-auth rate-limit check → credential lookup / secret verification.**
- The rate-limit subject is a **bounded/normalized/hash-derived digest** of the *presented* credential
  identifier, following the existing login/email-digest precedent (`email_digest`-style fixed-size
  digest). Presented input is length/charset-bounded **before** the digest is derived, so an attacker
  supplying unbounded raw garbage identifiers **cannot** mint unbounded fresh limiter buckets (all such
  input normalizes/truncates into a fixed-size subject space).
- **Unknown credentials and invalid secrets consume the same pre-auth bucket** for that presented
  credential identifier — a wrong secret or an unknown id does not escape the limiter.
- Runs **before** any secret verification, so credential-guessing is throttled prior to auth work.

**10.B — POST-AUTH limiter (after authentication).**
Flow: **authenticated `credential_id` → authenticated `api_read` limiter → scope/owner/project
processing.** A distinct protective limit keyed on the authenticated `credential_id` + action
`api_read`. Pre-auth and post-auth protections are **distinct** and both applied. No quotas/tiers/
billing/Redis (deferred).

## 11. Security fallback matrix (no fail-open)

| Condition | Behavior |
|---|---|
| Pre-auth rate limit exceeded (presented credential id) | **DENY** — generic rate-limited (before any secret verification) |
| Missing / malformed / unknown credential | **DENY** — generic unauthenticated |
| Invalid secret | **DENY** — generic unauthenticated (same pre-auth bucket consumed) |
| Revoked credential | **DENY** — generic unauthenticated |
| Expired credential (expiry set) | **DENY** — generic unauthenticated |
| Bound account inactive/deleted | **DENY** — generic unauthenticated (per existing canonical account status semantics) |
| Insufficient scope | **DENY** — generic forbidden (no project detail) |
| Cross-owner project | **DENY** — generic not-available (collapsed with missing) |
| Missing project | **DENY** — generic not-available (collapsed with cross-owner) |
| Post-auth (`api_read`) rate limit exceeded | **DENY** — generic rate-limited |
| Internal auth-store failure | **FAIL-CLOSED (DENY)** — generic internal error |
| Rate-limit-store failure (either tier) | **FAIL-CLOSED (DENY)** |
| Audit-write failure (mandatory security event) | **FAIL-CLOSED (DENY)** — the decision is not served without its audit event |
| Correlation-id malformed/missing | **ALLOW** with a server-generated correlation id (not trusted/echoed unchanged; replaced) |

No fail-open path. Security events are not silently dropped.

## 12. Schema-initialization boundary (CORRECTED)

- `api_credentials` and `access_audit` are **additive schema additions to the EXISTING
  `SqliteAccountStore` construction/schema lifecycle** (which idempotently establishes schema via
  `CREATE TABLE IF NOT EXISTS` inside `BEGIN IMMEDIATE` in `__init__`).
- **API request handling must contain NO ad-hoc DDL or migration logic.** No route handler may execute
  `CREATE TABLE` / `ALTER TABLE` / schema migration / direct initialization logic.
- Store **construction/schema establishment remains OUTSIDE** the P7-I2 read/export operation. Once a
  store is established, public API processing **consumes** it; it never independently initializes or
  migrates storage. No separate broad migration framework is introduced.
- **Truthful lifecycle note:** the current application may **lazily construct** `SqliteAccountStore`;
  first use may therefore invoke the **existing** constructor, which idempotently creates its schema
  (including the new additive tables). This existing-constructor-owned idempotent schema creation is
  the accepted boundary — it is **distinct from API-handler-owned migration**, which is prohibited. The
  contract does **not** claim a separate pre-start migration phase exists. This preserves the IR-1
  lesson: a read/API use case must not itself own datastore initialization.

## 13. Credential issuance / management boundary

Durable machine credentials require persistence (in-memory would lose revocation durability across
restart — unsafe for accepted V1). V1 provides a **programmatic issue + revoke store path** (mirroring
`email_tokens`) sufficient for testability/bootstrap; an **owner-facing credential-management UI is
DEFERRED**. The secret is returned only at issuance and never stored in plaintext or logged. **If
issuance/management cannot be truthfully provided without an owner-facing UI, STOP** rather than
inventing production UX.

## 14. D-FPC-MAP-06 ownership map

| Element | Classification |
|---|---|
| P7-I1 Project Read / Structured Export | ALREADY OWNED — CONSUME |
| `ProjectRecordContract` | ALREADY OWNED — CONSUME (do not expose blindly) |
| Durable project ownership (`load_owner` via seam) | ALREADY OWNED — CONSUME |
| Human account/session auth (`_current_account`, Flask session) | ALREADY OWNED FOR HUMAN WEB — DO NOT MISUSE AS MACHINE API AUTH |
| Existing rate limiter (`record_rate_attempt`, PRE-01 hardened) | PARTIALLY OWNED — EXTEND MINIMALLY (pre-auth digest subject + post-auth `api_read`; SAFE) |
| Credential hash-only storage pattern (email tokens fast-hash) | PARTIALLY OWNED — EXTEND MINIMALLY (new `api_credentials` mirrors it) |
| Security/access audit store | GENUINELY NEW (minimal) — P7-I2 CANONICAL RESPONSIBILITY (none exists) |
| FDC-001 | INSPECT / PRECEDENT — NOT AUTOMATIC PUBLIC CONTRACT |
| Machine/API principal minimum | P7-I2 CANONICAL RESPONSIBILITY |
| Public transport/version/error/correlation layer | P7-I2 CANONICAL RESPONSIBILITY |

No duplicate repository abstraction, service layer, authorization framework, domain registry,
orchestrator, output model, audit framework, rate-limit framework, or migration framework is introduced.

## 15. Likely implementation paths (discovery only — NOT edited here)

| Path | Current owner | Why P7-I2 may need it | Modification |
|---|---|---|---|
| one small API transport module/blueprint (e.g. `web/api_v1.py`, name not frozen) | new | versioned public routes + pre-auth/post-auth limiting, auth/scope/error/correlation/audit wiring consuming the P7-I1 seam | REQUIRED |
| `engine/account_store.py` (extend) | account_store | additive `api_credentials` + minimal `access_audit` tables (in the existing `__init__` schema lifecycle, §12) + issue/verify/revoke/audit methods (mirroring hash-only + atomic-counter patterns) | REQUIRED (additive; STOP if it would alter existing auth/session behavior) |
| the two new tables live in the existing `SqliteAccountStore` schema lifecycle | account_store schema | durable credentials/audit require persistence; additive `CREATE TABLE IF NOT EXISTS` only; no change to existing tables; no migration framework | REQUIRED (additive only) |
| one focused public API test module (`tests/test_p7_i2_public_api.py`, name not frozen) | new | behavioral RED→GREEN + security evidence | REQUIRED |
| `web/app.py` (register blueprint only) | web | mount the API module | AVOIDABLE-OR-MINIMAL — register only; STOP-IF-NEEDED beyond a mount line |

If the path count expands materially beyond this, STOP and justify.

## 16. RED→GREEN plan (behavioral; CORRECTED with A–E additions)

Behavioral RED (not arbitrary module naming) covering: (1) no credential → deny; (2) malformed/unknown
credential → deny; (3) revoked credential → deny; (4) insufficient scope → deny; (5) authorized
principal + owned project → Project Read succeeds; (6) authorized principal + owned project → Structured
Export succeeds; (7) cross-owner project → non-enumerating not-available; (8) missing project →
identical non-enumerating not-available; (9) `api_version` present (Read + Export); (10) stable error
envelope shape; (11) correlation id present + echoed; (12) audit event created for served + denied
requests (non-enumerating project handling); (13) post-auth protective rate limit enforced; (14)
rate-limit-store / audit-store failure → fail-closed deny; (15) the P7-I1 seam is actually consumed;
(16) no project/business-state mutation; (17) no browser-session dependency; (18) no secret leaked;
(19) no P7-I3 adapter code; (20) no write/import route exists.

**Required additions (Correction 3):**
- **A. EXPIRED CREDENTIAL** — an expired credential → generic unauthenticated denial.
- **B. ROTATION** — issue replacement → revoke old → old credential denied → new credential accepted (if otherwise valid).
- **C. PRE-AUTH RATE LIMIT** — unknown-credential / invalid-secret attempts are counted **before** authentication against the bounded derived subject; threshold exceeded → deny; **and** oversized/junk presented identifiers **cannot** create unbounded limiter subject material (bounded/normalized/hash-derived subject proven fixed-size).
- **D. SCHEMA-INITIALIZATION BOUNDARY** — public route processing executes **no** ad-hoc DDL/migration (proven via call-boundary instrumentation or another robust repository-compatible mechanism; **not** raw database-byte equality).
- **E. CORRELATION-ID VALIDATION** — a malformed caller-provided correlation id is **not** trusted/echoed unchanged and is replaced by a server-generated valid request id.

No broad `pytest.raises(Exception)`; no manufactured breakage; existing tests unchanged.

## 17. STOP conditions

STOP and report before/within implementation if: the live P7-I1 seam cannot safely serve the public
transport layer; machine↔owner authorization cannot be grounded without a new major model; credential
storage would require a broad IAM architecture; safe atomic rate limiting (either tier) cannot be
achieved within bounded scope; audit persistence would require broad unrelated infrastructure; public
representation cannot be separated from raw persistence; route/version semantics conflict with a
canonical contract; a write/import endpoint becomes necessary; P7-I2 would require modifying unrelated
domain/business logic or ad-hoc DDL inside a handler; implementation-path count expands materially
beyond §15; or a genuinely new Owner architectural decision is required.

## 18. P7-C obligation classification (P7-I2)

| Obligation | Classification for P7-I2 |
|---|---|
| Authentication (machine) / Machine identity / Authorization | DELIVERED BY P7-I2 IF IMPLEMENTED |
| Scopes | PARTIALLY ADVANCED (single `project:read`; taxonomy deferred) |
| Version identity (API + export) | DELIVERED BY P7-I2 IF IMPLEMENTED |
| Stable error envelope / Correlation id / Basic access audit | DELIVERED BY P7-I2 IF IMPLEMENTED |
| Basic protective rate limit (pre-auth + post-auth) | DELIVERED BY P7-I2 IF IMPLEMENTED |
| Request provenance (read-side) | DELIVERED BY P7-I2 IF IMPLEMENTED |
| Secrets / revocation | PARTIALLY ADVANCED (issuance/revocation/rotation/expiry minimum; UI deferred) |
| Public export contract (read/export) | DELIVERED BY P7-I2 IF IMPLEMENTED |
| Quotas | DEFERRED TO LATER P7 INCREMENT |
| Pagination / Idempotency / Retries-timeouts | NOT APPLICABLE TO P7-I2 |
| Import / write / Webhooks / file exchange | DEFERRED (separate gate) |
| Integration adapters | DEFERRED TO P7-I3 |
| Partner/external sandbox | DEFERRED (P7-I2 provides local test harness only) |
| Deprecation | PARTIALLY ADVANCED (minimum v1 policy) |
| Monitoring | DEFERRED (audit ≠ monitoring) |
| Abuse controls (broad, incl. IP/network-origin) | DEFERRED (rate-limit floor is not full abuse control) |

**Nothing is classified as Phase-7 complete.** The §25 Remaining-Obligation / Exit-Criteria Review
remains reserved before P7-CLOSE.

## 19. Acceptance criteria

- **PUBLIC PROJECT READ / STRUCTURED EXPORT:** the two GET routes, consuming the P7-I1 seam, return the data-minimized envelopes with `api_version` (+ `export_contract_version` on export).
- **MACHINE AUTH:** credential verified against the stored fast-hash; browser session rejected on the API path.
- **AUTHORIZATION / SCOPES:** access only to projects owned by the credential's bound owner; cross-owner denied; `project:read` required; insufficient scope denied.
- **CREDENTIAL LIFECYCLE:** revoked, expired, and inactive-bound-account credentials denied; rotation (issue-new + revoke-old) behaves per §16.B.
- **PRE-AUTH RATE LIMIT:** enforced against a bounded derived subject before secret verification; unknown/invalid attempts share the bucket; junk identifiers cannot mint unbounded subjects.
- **POST-AUTH RATE LIMIT:** enforced per authenticated credential; both tiers fail-closed on store failure.
- **ERROR ENVELOPE / NON-ENUMERATION:** stable shape; cross-owner ≡ missing; no internal detail.
- **CORRELATION ID:** generated/normalized, malformed caller value replaced, echoed, audit-linked.
- **AUDIT:** event for served + denied requests (non-enumerating); audit-write failure fails closed.
- **SCHEMA BOUNDARY:** no handler executes DDL/migration; new tables live in the existing store schema lifecycle.
- **REQUEST PROVENANCE / NON-MUTATION:** provenance in audit only; no project-state change on any read.
- **P7-I1 REUSE · NO WRITE/IMPORT · NO P7-I3 · D-FPC-MAP-06 · LEAN:** satisfied.
- **TESTS:** behavioral RED→GREEN (§16 incl. A–E); full regression green; existing tests unchanged.

## 20. Status (this corrected candidate)

P7-I2 CONTRACT: CORRECTED PUBLICATION CANDIDATE — PENDING INDEPENDENT PRE-MERGE RE-REVIEW; NOT FINALLY
ESTABLISHED. Supersedes `4933c26` (evidence only, DO NOT MERGE). P7-I2 IMPLEMENTATION: NOT STARTED;
Implementation Gate Lock ACTIVE. P7-I3: NOT STARTED. Phase 7: OPEN. No code/tests/routes/migrations/
credentials created here.
