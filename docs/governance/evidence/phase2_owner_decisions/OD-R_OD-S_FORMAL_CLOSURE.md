# OD-R / OD-S — Combined Formal Closure (Candidate)

**Decisions:** OD-R (Cross-Application Communication, Sponsorship, Privacy and
Trust Boundaries) and OD-S (Phase 2 Closure Criteria) — **two separate owner
decision records** governed through **one combined formal-closure lifecycle**.
**Type:** documentation-only formal-closure candidate. **DOCUMENTED NO-VALID-RED.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Closure candidate base (verified live tip after PR #313):**
`947c1f84ff23aaba809cd78c0f0ce95753d621b6`.

---

## 0. Lifecycle status (read first)

```
OD-R / OD-S:  FORMAL-CLOSURE CANDIDATE
              MERGED AT STAGE A
              NOT YET FORMALLY CLOSED
```

This record is a **Stage B formal-closure candidate**. It does **not** assert
that OD-R or OD-S is already formally closed, durably closed, that Phase 2 is
closed, or that Phase 3 is authorized. The Stage A substantive increment is
merged; formal closure is not yet in effect.

## 1. Two separate decisions, one combined lifecycle

OD-R and OD-S are **distinct** owner decision records with distinct subject
matter:
- **OD-R** records three architecturally-separate cross-application
  product-governance/architectural **boundaries only** (A. Sponsor Recognition
  and Configurable Branding; B. Centrally Configurable Administrative Notice;
  C. Privacy, Confidentiality and User Trust Communication).
- **OD-S** records the finite Phase 2 closure criteria and the authoritative
  disposition of every remaining Phase 2 obligation (RW-1…RW-10 and X-1…X-5).

By owner authorization they are prepared, merged, and closed through **one
combined documentation-only lifecycle** with three stages:

```
Stage A  substantive candidate  -> independent review -> owner acceptance
         -> normal merge -> post-merge verification            [COMPLETE]
Stage B  combined formal-closure candidate                     [THIS RECORD]
Stage C  post-closure synchronization                          [SEPARATELY GATED]
```

## 2. Closure status is CONDITIONAL until the Stage B gates complete

OD-R / OD-S becomes **FORMALLY CLOSED** **only after** all of:

```
independent review of this Stage B candidate
  -> owner acceptance
    -> normal PR merge
      -> post-merge verification
```

This candidate presumes **no** gate below its own preparation is complete. It
records candidate preparation only.

## 3. Stage A verified merge evidence (PR #313)

| Item | Value |
|---|---|
| PR | #313 — **MERGED / CLOSED** (normal merge commit) |
| Accepted Stage A candidate | `8ce4b341c4fcfd5b711daa87929c9644b180b810` |
| Merge commit | `947c1f84ff23aaba809cd78c0f0ce95753d621b6` |
| Ordered parents | ① `b9f9320ddd933be7bcd4513e9afb919237f81c37` · ② `8ce4b341c4fcfd5b711daa87929c9644b180b810` |
| Merge tree == accepted candidate tree | `c529e81f52934b57a4706e8257b865bba2e65d62` (EQUAL) |
| Prior authoritative tip (pre-merge base) | `b9f9320ddd933be7bcd4513e9afb919237f81c37` |
| Authoritative tip after merge | `947c1f84ff23aaba809cd78c0f0ce95753d621b6` |
| Accepted independent verdict | **B — INDEPENDENT CANDIDATE PASS WITH NON-BLOCKING OBSERVATIONS** |
| Accepted post-merge verdict | **A — PR #313 POST-MERGE PASS** |
| `main` | `0e89e4636399760965c9ff8086b465c90dbadf8e` — STALE / UNRECONCILED / UNTOUCHED |

The live authoritative tip is the merge commit; the accepted Stage A candidate
`8ce4b341` is an ancestor of that tip; the merge tree equals the accepted
candidate tree `c529e81`.

## 4. Exact four-file Stage A scope (verified)

Stage A changed **exactly four files** (`8ce4b341` vs base `b9f9320`),
**332 insertions / 3 deletions**, documentation-only:

```
A  docs/governance/evidence/phase2_owner_decisions/OD-R_CROSS_APPLICATION_COMMUNICATION_SPONSORSHIP_PRIVACY_TRUST_BOUNDARIES.md   (+180)
A  docs/governance/evidence/phase2_owner_decisions/OD-S_PHASE_2_CLOSURE_CRITERIA.md                                              (+143)
M  docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md                                              (+6 / -3)
M  docs/governance/ACTIVE_EXECUTION_ROADMAP.md                                                                                  (+6)
```

No engine, web, JSON, schema, test, CI, or runtime file changed at Stage A.

## 5. The four accepted independent-review observations (enumerated; all NON-BLOCKING)

The accepted independent verdict was
**`B — INDEPENDENT CANDIDATE PASS WITH NON-BLOCKING OBSERVATIONS`**, carrying
**four (4)** observations. Each is enumerated in full below and classified
**NON-BLOCKING**. This section is self-contained: no external or owner-held
evidence is required to understand the substance of these observations. These
are **historical, accepted, non-blocking observations from the Stage A
independent review**; they are **not** defects introduced by, or repaired in,
Stage B.

### Observation 1 — Shallow-clone environment
The independent-review environment was initially a shallow clone and did not
contain the prerequisite history. The reviewer ran `git fetch --unshallow origin`
to obtain the full history.
- **Classification:** `NON-BLOCKING — ENVIRONMENTAL`.
- **Rationale:** no substitute base was used, and candidate identity, history, and
  scope were independently verified afterward.

### Observation 2 — Unverified commit signature
The Stage A candidate commit carried an SSH signature, but the independent-review
environment did not contain an allowed-signers trust anchor, so cryptographic
trust validation of the signature was not performed.
- **Classification:** `NON-BLOCKING — VERIFICATION ENVIRONMENT`.
- **Rationale:** signature validation was not an acceptance requirement of the
  Stage A contract; commit, parent, tree, bundle, and content identities were
  independently verified.

### Observation 3 — Prerequisite reachability
The Stage A prerequisite was reachable from
`origin/feature/atomic-json-session-persistence` and not from the current default
`main` lineage.
- **Classification:** `NON-BLOCKING — GOVERNANCE TOPOLOGY`.
- **Rationale:** this was consistent with the repository's recorded state that
  `main` was stale/unreconciled and that the feature integration lineage was
  authoritative.

### Observation 4 — X-5 representation
OD-S represented X-5 through two table rows — `X-5 / CR-6, CR-7` and `X-5 / CR-5`.
- **Classification:** `NON-BLOCKING — REPRESENTATIONAL`.
- **Rationale:** this matched the owner-approved split dispositions — CR-6 and
  CR-7 closed / no further action; CR-5 separately gated optional cleanup /
  non-blocking. It did not create an unresolved disposition or violate the
  authoritative decision structure.

### Owner acceptance of the four observations
The owner reviewed and **accepted all four observations as NON-BLOCKING before
authorizing the Stage A transfer and merge** ("the non-blocking observations are
acknowledged and do not prevent owner acceptance"). None of the four blocked the
independent-review PASS, owner acceptance, the normal merge (PR #313), or the
`A — PR #313 POST-MERGE PASS` post-merge verdict, and none alters the merged
content, the four-file scope, the disposition table, the finite endpoint, or any
protected artifact. Recording their verbatim substance here is a documentation
completeness measure and is **not** a Phase 2 closure prerequisite (OD-S §5).

## 6. What OD-R and OD-S established (recap — not re-decided)

Stage A (merged candidate `8ce4b341`) established, documentation-only:
- **OD-R** — three separate boundaries **only** (A/B/C), defining no interface,
  storage, database, administration screen, visual design, frequency behavior, or
  runtime; all design and implementation deferred to Phase 3 or separately
  authorized downstream workstreams; the narrow user-facing `idea`-terminology
  rule with **no** repository-wide replacement of `invention`; the truthful-claims
  rule; and the launch constraint. OD-A, OD-B, OD-I, OD-K, OD-N remain binding and
  are extended prospectively only.
- **OD-S** — the finite **12-condition** Phase 2 closure endpoint; the explicit
  non-prerequisites; the Phase 3 stop requirement; and the authoritative
  disposition of every RW-1…RW-10 and X-1…X-5 item, with **no item classified
  `OWNER DECISION STILL REQUIRED`**.

This Stage B record **re-decides none** of the above. It makes **no** edit to the
merged OD-R or OD-S records, the disposition table, the finite endpoint, the
accepted limitations, the non-prerequisites, or the Phase 3 stop requirement.

## 7. Protected artifacts unchanged (Stage B)

Stage B changes exactly three files (§10). The following remain **byte-identical**:
the merged `OD-R_CROSS_APPLICATION_COMMUNICATION_SPONSORSHIP_PRIVACY_TRUST_BOUNDARIES.md`
(blob `1685bd8031a41b23ba9b052cd46a64258cfc5b10`) and
`OD-S_PHASE_2_CLOSURE_CRITERIA.md` (blob `8984bb243e8062bd5985e55e0f0fef2f78317cba`);
all `engine/`, `web/`, and `tests/`; all JSON, schema, CI, and runtime artifacts;
`CLAUDE.md`; `OWNER_PRODUCT_IDENTITY_CORRECTION.md`; `docs/ARCHITECTURE_DECISION.md`;
`docs/governance/DOMAIN_SCOPE_GOVERNANCE_INCONSISTENCY_REPORT.md`; all previous
evidence records; and `main`.

## 8. No implementation and no Phase 3 activation

No implementation, UI, runtime, schema, database, legal-policy, account,
authentication, authorization, subscription, payment, sponsor-management,
popup/notice behavior, or privacy-control work occurred or is authorized. **No
Phase 3 work began.** Formal closure of OD-R / OD-S — once the §2 gates complete —
must **not** activate Phase 3; the Phase 3 stop requirement (OD-S §6) is
preserved. Phase 3 requires a new, separate, explicit owner authorization.

## 9. Stage C remains separately gated

Stage C (post-closure synchronization) is **separately gated** and requires a
distinct owner authorization. This Stage B candidate begins no Stage C work, no
Phase 2 formal-closure gate, and no downstream activation. The separate Phase 2
formal-closure candidate (OD-S §4 condition 12) is likewise a later,
independently reviewed, owner-accepted gate.

## 10. In-scope files (exactly three) — Stage B

1. **ADD** `docs/governance/evidence/phase2_owner_decisions/OD-R_OD-S_FORMAL_CLOSURE.md` (this record).
2. **MODIFY** `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` — OD-R / OD-S lifecycle-status synchronization only (L10/L11); no RW/X disposition, finite endpoint, accepted-limitation, non-prerequisite, Phase 3 stop, or unrelated-phase change.
3. **MODIFY** `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` — one append-only Stage B formal-closure-candidate record (prior content preserved as an exact byte prefix).

No re-edit of the merged OD-R or OD-S records; no accepted Phase 0 / Phase 1 /
Increment 1 / Increment 2 / Increment 3 record modified; no code / JSON / schema /
test / CI / runtime change.

## 11. Authority boundaries (preserved)

```
PHASE 2 INCREMENT 1 / 2 / 3:  FORMALLY CLOSED
OD-R / OD-S:                  FORMAL-CLOSURE CANDIDATE / MERGED AT STAGE A / NOT YET FORMALLY CLOSED
PHASE 2 OVERALL:              IN PROGRESS — NO OTHER PHASE 2 INCREMENT AUTHORIZED
PHASE 3 AND LATER:            NOT STARTED — NOT AUTHORIZED
PRODUCT STATUS:               DEMO_READY_WITH_LIMITATIONS / NOT PRODUCTION READY
MAIN:                         STALE / UNRECONCILED / UNTOUCHED
IMPLEMENTATION AUTHORITY:     NONE
RELEASE AUTHORITY:            NONE
DEPLOYMENT AUTHORITY:         NONE
```

## 12. RED path

`DOCUMENTED NO-VALID-RED`. Documentation-only; it changes no runtime code, JSON,
behavior, or executable contract. Validation uses documentation consistency, exact
three-file scope, ancestry, protected tree/blob verification, roadmap byte-prefix
preservation, and the verified `merge tree == accepted candidate tree` identity —
not a test transition.

## 13. Provenance of this record

This is the **corrected replacement** Stage B candidate. A first Stage B
preparation attempt (candidate `d0a3af1a82af37952ef0e17cfe5088577181ef7c`) recorded
the four observations only by count, classification, and owner acknowledgment; the
owner determined that a self-contained formal-closure record must enumerate the
four observations in full and authorized this corrected replacement. The original
`d0a3af1` candidate remains intact and untouched as evidence of the first attempt;
it is `SUPERSEDED FOR REVIEW PURPOSES / NOT ACCEPTED`. This corrected candidate is a
new, distinct candidate (new commit, tree, and bundle).

## 14. Evidence classification

Phase 2 owner-decision **combined formal-closure candidate** artifact. It becomes
the authoritative OD-R / OD-S formal-closure record only after independent review
of this Stage B candidate, owner acceptance, normal PR merge, and post-merge
verification (§2). It grants no implementation, release, or deployment authority,
certifies no runtime behavior, closes no other Phase 2 item, and does not itself
close Phase 2 or authorize Phase 3.
