# P8-AF — Access, Licensing & Organization Foundation — FORMAL CLOSURE RECORD

**Status of THIS record:** governance/documentation-only **closure candidate** — authoritative if/when independently
reviewed, Owner-accepted, and merged. It records the **formal closure of the `P8-AF` obligation** (the cross-cutting
Access, Licensing & Organization Foundation registered before `P8-CLOSE`). It does **not** close Phase 8, does **not** start
`P8-CLOSE`, does **not** activate any access/licensing/organization/commercial model, selects no payment provider, and
registers/executes no PSRR. **DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY FORMAL CLOSURE GATE** (no runtime behavior is created
here; the P8-AF-I1 and P8-AF-I2 RED→GREEN occurred at implementation time and are cited, not re-run). **Expected runtime/code/
test diff for this gate: ZERO.**

## 1. Gate identity & closure verdict

- **Gate:** P8-AF — Access, Licensing & Organization Foundation — Formal Closure / Current-Truth Synchronization.
- **Verdict:** **P8-AF — FORMALLY CLOSED / AUTHORITATIVE** (foundation-obligation closure only; authoritative if/when this
  governance candidate is merged). **Phase 8 is NOT closed.**

## 2. Identity & lineage (verified live, read-only at the merged tip)

- **Registered obligation:** `P8-AF` (`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_OBLIGATION.md`),
  registered by the P8-I4 formal closure gate as **mandatory before `P8-CLOSE`**.
- **Accepted foundation contract:** **P8-AF-C**
  (`docs/governance/P8_AF_ACCESS_LICENSING_ORGANIZATION_FOUNDATION_CONTRACT.md`) — contract candidate `4737587`, merged
  **PR #429** (`06683179f843b71f8d151f0c3c5647778b4b0acf`), post-merge verified.
- **P8-AF-I1 — Canonical Access-Grant + Access-Resolution Foundation:** accepted implementation candidate `b597850` —
  independent review **verdict A — ACCEPT**; merged **PR #430** (`1ac9c603b14a172a737f3577791e9f23a46533bd`; parents
  `06683179` + `b597850`; merged tree `c8f095cab414a15609011d7bfa3a4d7f634a1950`); **P8-AF-I1 accepted diffstat: 8 files
  changed, 693 insertions(+), 5 deletions(-)**; post-merge verified.
- **P8-AF Remaining-Obligation / Closure-Eligibility Review:** returned **verdict B — one small corrective/foundation
  increment required** (the sole mandatory blocker: the contract-required **uniform-subject / authenticated-account
  isolation** in the canonical resolver — P8-AF-C §5.1 "given an authenticated account"). All other observations were
  classified DEFERRED (before persistence / before first real runtime caller / by design).
- **P8-AF-I2 — Subject-Scoped Access Resolution (corrective):** accepted implementation candidate **`16a9d66`** —
  independent review **verdict A — ACCEPT** (which explicitly stated that, upon Owner acceptance, merge, and post-merge
  verification of that exact candidate, **P8-AF is ELIGIBLE FOR FORMAL CLOSURE**); merged **PR #431** — merge
  **`1132cfe8fde16a8c3a5784a2b1351a43620eda94`** (parent 1 `1ac9c603b14a172a737f3577791e9f23a46533bd`; parent 2
  `16a9d66228a179a4334eef2ba0e523e47f223545`; **merged tree `0ecd7def6f0abc779bdfdbd496025ec10a8ef8d1` == accepted candidate
  tree → post-merge verified**). **P8-AF-I2 diffstat: 6 files changed, 402 insertions(+), 29 deletions(-); roadmap numstat
  79 insertions / 0 deletions; `git diff --check` PASS.** Those merge and post-merge conditions are now satisfied.

## 3. RED → GREEN evidence (historical; cited, not re-run)

- **P8-AF-I1 (foundation):** modules absent on the base → genuine import RED; behavioral RED via six load-bearing mutation
  probes (remove expiry check / drop deterministic tie-break / invent precedence winner / add provider import / bypass
  malformed-input rejection / remove now-injection validation), each turning a targeted test RED and restored byte-identical.
  GREEN: focused 30; Phase-8 154; full suite 2228 passed / 3 skipped / 1 xfailed / 0 failed.
- **P8-AF-I2 (corrective — uniform-subject):** concrete behavioral RED — against the merged P8-AF-I1, two ACTIVE grants for
  `account-A` and `account-B` sharing an entitlement composed into one `granted=True` decision (`contributing=('gA','gB')`),
  and the subject-scoped API was absent; the 23 new subject-scoped tests failed (22 RED). Behavioral RED then confirmed by
  six mutation probes (remove subject equality check / invert it / scope-after-composition / empty-subject-as-wildcard /
  first-grant-subject / drop `foreign_subject` provenance), each turning a targeted test RED and restored byte-identical.
- **Combined GREEN (at the merged tip):** P8-AF-I2 focused **23 passed**; P8-AF-I1 + I2 **53 passed**; Phase-8
  (I1+I2+I3+I4-I1+AF-I1+AF-I2) **177 passed**; **full suite 2251 passed / 3 skipped / 1 xfailed / 0 failed**.

## 4. P8-AF-C §22 closure-criteria matrix (each demonstrated)

| §22 criterion | Verdict | Evidence |
|---|---|---|
| **(a)** P8-AF-C independently reviewed, Owner-accepted, merged, post-merge verified | **PASS** | Contract `4737587` merged **PR #429** (`06683179`), post-merge verified |
| **(b)** the necessary minimum implementation increment(s) (§19) implemented with genuine RED→GREEN from the §20 matrix, proving the architecture can **represent and resolve** the models safely **without activating** any | **PASS** (via **P8-AF-I1 + P8-AF-I2**) | §20 items proven at the foundation level with fake/in-memory sources: #7 no-auth-bypass, #8 deterministic precedence (fail-closed ambiguity), #9 no double quota, #10 revocation removes access (not data), #11 provider independence; and the multi-subject safety dimension (#5/#6 / cross-account non-composition) now demonstrated by **P8-AF-I2** subject-scoped resolution. Items #1/#2/#3 (trial/campaign) and #12 (persistence) remain **N/A — evidence-triggered** (those sources are not activated); the architecture is shown able to represent them via the source-neutral Access-Grant without redesign |
| **(c)** authority boundaries (§4) and binding invariants (§6, §13, §16, §17, §18) demonstrated and unweakened | **PASS** | §4 authority boundaries: P8-I1 entitlement referenced-not-redefined, P8-I2 sole quota authority (no counter created/incremented/reset/summed), P8-I3 sole lifecycle authority (no competing machine), P8-I4 provider boundary (no provider import). §6 competing-entitlement fail-closed; §13 **account/data isolation now enforced** (foreign-subject grants never compose; billing/seat ≠ data); §16 no competing lifecycle machine; §17 deterministic revocation removes access not data; §18 no data-ownership inference / no data destruction. OD-N import guards unweakened |
| **(d)** dedicated `P8-AF` formal closure record produced | **PASS / SATISFIED BY THIS RECORD** | This document |

**All four §22 criteria are satisfied.** No criterion is marked PASS without the cited evidence.

## 5. Delivered foundation (P8-AF delivered ONLY this — no runtime activation)

- **Canonical source-neutral `AccessGrant`** — an immutable value object (`engine/access_grant.py`); fixed `__slots__`
  structurally forbid quota counters / provider identifiers / raw provider data / credentials / pricing / data-ownership
  fields; fail-closed `make_access_grant(...)`.
- **One deterministic, pure, read-only access-resolution seam** — `resolve_access(grants, *, subject, now)`
  (`engine/access_resolver.py`).
- **Provenance / explainability** — the resolution names the selected source and explains every exclusion.
- **P8-I1 entitlement authority reuse** — identity validated via `plan_catalog.entitlement_descriptor` (referenced, never
  redefined; capabilities never read for the access decision).
- **P8-I2 quota non-interference** — one entitlement/quota-policy path per decision; never additive, never reset.
- **P8-I3 lifecycle non-interference** — no competing trial/seat/campaign state machine.
- **P8-I4 provider independence** — no provider SDK / identifier / ingestion / webhook / reconciliation dependency.
- **Authenticated-subject-scoped resolution** — resolution is bound to one authenticated `subject`; scoping runs **before**
  entitlement composition.
- **Cross-account grant isolation** — a foreign-subject grant is excluded **INERTLY** (never contributes, never denies,
  never raises) with explicit `foreign_subject` provenance (smallest-ambiguity behavior).
- **Fail-closed competing-entitlement ambiguity** — >1 distinct effective entitlement → DENY (precedence deferred).
- **Deterministic injected-time behavior** — `now` is an injected epoch int; wall-clock is never read.
- **`[effective_from, effective_until)` semantics** — FROZEN (see §8).

This is a **backend composition foundation only.** No organization, seat, campaign, role, trial, or enterprise capability is
activated; no persistence/schema is introduced; no runtime/web caller exists.

## 6. Deferred capabilities — MUST REMAIN DEFERRED (no activation by this closure)

Organization identity — **NOT STARTED / DEFERRED**; Membership — **NOT STARTED / DEFERRED**; Named seats — **NOT STARTED /
DEFERRED**; Seat persistence — **NOT STARTED / DEFERRED**; Campaign configuration — **NOT STARTED / DEFERRED**; Global
promotional/free-access runtime — **NOT STARTED / DEFERRED**; Owner/Admin authorization seam — **NOT STARTED / DEFERRED**;
7-day trial activation — **NOT STARTED** (automatic day-7 hard deletion remains **NOT AUTHORIZED**); Enterprise/custom
billing — **NOT STARTED / DEFERRED**; SSO/domain onboarding — **NOT STARTED / DEFERRED**; Concurrent licensing — **NOT
STARTED / DEFERRED**. **No future source model is activated merely by closing P8-AF.**

## 7. Mandatory future hardening / trigger obligations (preserved so they cannot be forgotten)

1. **Direct `AccessGrant` constructor hardening — BEFORE THE FIRST REAL RUNTIME CALLER.** Raw `AccessGrant(...)` construction
   can bypass `make_access_grant` validation, and an adversarial raw subject object with a custom `__eq__` could match another
   subject. This is **NOT** a P8-AF closure blocker (no runtime caller exists), but it **MUST** be closed as an activation
   guard before the first real caller (e.g. validate in the constructor and/or require canonical string subjects at the
   resolver boundary).
2. **Durable duplicate grant-identity conflict rule — BEFORE THE FIRST PERSISTENCE / DURABLE-GRANT increment.** Same canonical
   `grant_id` + materially different content must have explicit conflict semantics (mirroring the P8-I4 durable-dedupe
   pattern). Deferred until grants are persisted.
3. **Future real second access source — SEPARATE GOVERNED PRECEDENCE REQUIRED.** Before activating a second real source
   (campaign / seat / Owner-Admin / enterprise), a separately governed precedence / source-composition rule is required. **Do
   NOT invent that precedence now** (the resolver currently fail-closes on competing distinct entitlements).
4. **Global / non-account scope semantics — SEPARATELY GOVERNED.** No wildcard subject exists; any global campaign/free-access
   grant requires separately governed scope semantics before activation.
5. **Data ownership remains independent.** Billing / grant / access status does **not** grant permission to read another
   account's content; cross-account content access stays governed by the existing Phase-4/Phase-5 ownership/authorization
   rules.

## 8. Time semantics — FROZEN foundation convention

`effective_from` — **INCLUSIVE**; `effective_until` — **EXCLUSIVE**; canonical interval **`[effective_from,
effective_until)`**. This is the existing tested deterministic implementation convention (not a new Owner/business decision);
it is frozen here and its runtime behavior is unchanged.

## 9. Authority boundaries (unchanged; composition, not duplication — D-FPC-MAP-06)

P8-I1 remains the plan/entitlement authority; P8-I2 remains the **sole** commercial usage/quota authority; P8-I3 remains the
canonical subscription-lifecycle authority; P8-I4 remains the provider-neutral payment boundary. **P8-AF composes** these via
the access-grant model + the single resolution seam; it created **no** second plan catalog, quota counter, or lifecycle state
machine, and **no** new authority.

## 10. Boundary — what this closure does NOT do

- **Phase 8 is NOT closed** — NOT complete; NOT billing-live; NOT paid-active.
- **`P8-CLOSE` — NOT STARTED.** **Phase 9 / Phase 10 — NOT AUTHORIZED.** **PSRR EXECUTION — NOT STARTED.** **Production — NOT
  AUTHORIZED.** **Public paid activation — BLOCKED** until applicable Phase-10 legal/readiness + PSRR = GO/PASS + a governing
  separate Deployment Gate + explicit Owner deployment authorization.
- No access/licensing/organization/commercial model activated; no provider selected; no persistence/schema/role/organization/
  seat/campaign created; no automatic trial-data deletion.
- **`OWNER_DECISION_REGISTER.md`: UNCHANGED** — this foundation-obligation closure registers no new durable Owner decision,
  consistent with the P8-I1 / P8-I2 / P8-I3 / P8-I4 increment/closure precedent (purely evidentiary closure leaves the ODR
  unchanged; the still-OPEN commercial/provider decisions remain governed by the P8-I3-C / P8-I4-C register entries, and the
  P8-AF mandate + directional options remain recorded under the P8-I4-CLOSE register entry).

## 11. Result

**P8-AF — Access, Licensing & Organization Foundation: CONTRACT ESTABLISHED (P8-AF-C, PR #429) / IMPLEMENTED (P8-AF-I1
RED→GREEN, PR #430) / CLOSURE-ELIGIBILITY REVIEWED (verdict B — one corrective increment required) / CORRECTED (P8-AF-I2
uniform-subject isolation, RED→GREEN) / INDEPENDENTLY REVIEWED (P8-AF-I1 A; P8-AF-I2 A) / OWNER-ACCEPTED / MERGED (PR #431,
`1132cfe`) / POST-MERGE VERIFIED / FORMALLY ACCEPTED AND CLOSED** (foundation-obligation closure only; authoritative if/when
this governance candidate is merged). **P8-AF-C = CLOSED / AUTHORITATIVE; P8-AF-I1 = CLOSED / AUTHORITATIVE; P8-AF-I2 = CLOSED
/ AUTHORITATIVE; P8-AF = CLOSED / AUTHORITATIVE.** There is no active implementation increment under P8-AF. All future access/
licensing/organization/campaign/Owner-Admin/trial/enterprise source models remain **NOT STARTED / DEFERRED**, with the §7
hardening/trigger obligations preserved. **Next Phase-8 gate: the separate Phase-8 Remaining-Obligation / Exit-Criteria Review
and `P8-CLOSE` — NOT STARTED. Phase 8 remains OPEN.**
