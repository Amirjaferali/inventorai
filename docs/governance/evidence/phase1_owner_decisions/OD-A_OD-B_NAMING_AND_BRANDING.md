# Phase 1 — Owner Decisions OD-A and OD-B — Product Name and Centralized Branding

**Phase:** Phase 1 — Owner Product Decisions
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Decision IDs:** OD-A (final public product name) and OD-B (centralized branding
indirection) — recorded together because they are explicitly linked.
**Scope:** documentation-only durable record of two accepted, linked owner
decisions. **No implementation. No code, test, template, schema, API, identifier,
or runtime change. No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official base at authoring:** `ba692f54eb05b4f88a854650b71fd2a0f32bffc3`
(official tip after PR #293, which merged OD-C).

---

## 1. Decision status

```
OD-A — OWNER DECISION ACCEPTED
OD-B — OWNER DECISION ACCEPTED
```

This record records exactly two accepted owner decisions. It resolves no other
open owner decision, remediates no conflict textually, implements no branding,
selects no final public name, and activates no downstream phase.

## 2. Accepted owner decisions (verbatim)

### OD-A — Final Public Product Name

> **OD-A — OWNER DECISION ACCEPTED**
>
> KEEP "InventorAI" AS A TEMPORARY INTERNAL WORKING NAME. DEFER THE FINAL PUBLIC
> PRODUCT NAME UNTIL A SEPARATE MARKET, TRADEMARK, DOMAIN, AND BRAND VALIDATION
> GATE.

Required status:

```
FINAL PUBLIC PRODUCT NAME:   NOT YET SELECTED
CURRENT "InventorAI" NAME:   TEMPORARY WORKING NAME ONLY
PUBLIC BRAND APPROVAL:       NOT GRANTED
IMMEDIATE RENAME:            NOT AUTHORIZED
```

### OD-B — Centralized Branding Indirection

> **OD-B — OWNER DECISION ACCEPTED**
>
> ADOPT CENTRALIZED BRANDING INDIRECTION AS A REQUIRED PHASE 3 FOUNDATION BEFORE
> ANY BROAD PRODUCT-UI IMPLEMENTATION OR PUBLIC BRAND ROLLOUT.

Required status:

```
CENTRALIZED BRANDING INDIRECTION:  OWNER-APPROVED FUTURE FOUNDATION
IMPLEMENTATION:                    DEFERRED TO PHASE 3
SEPARATE PHASE 3 AUTHORIZATION:    REQUIRED
IMPLEMENTATION AUTHORITY NOW:      NONE
DEPLOYMENT AUTHORITY:              NONE
```

## 3. Distinguished status (must be read exactly)

```
OWNER PRODUCT DECISION:               ACCEPTED
BRANDING FOUNDATION REQUIREMENT:      APPROVED FOR FUTURE PHASE 3 IMPLEMENTATION
CURRENT BRANDING IMPLEMENTATION:      NOT AUTHORIZED
FINAL PUBLIC NAME:                    NOT SELECTED
CURRENT "InventorAI" USE:             TEMPORARY INTERNAL WORKING NAME ONLY
```

## 4. Why OD-A and OD-B are recorded together

The two decisions are directly interdependent (Phase 0 register: OD-A depends on
OD-B; OD-B depends on OD-A). Deferring the final public name (OD-A) is only safe
if the product can later adopt any approved name without code churn — which is
exactly what centralized branding indirection (OD-B) provides. Recording them in
one combined artifact keeps the linked decision coherent and is the smallest
durable increment. This combination is documentation structure only; each
decision retains its own identifier and status.

## 5. Prior Phase 0 recommendation status (context, not authority)

In the Phase 0 Open Owner Decisions Register both were recorded only as
`RECOMMENDATION — NOT OWNER DECISION`:
- OD-A recommendation: "defer final name; add centralized branding indirection."
- OD-B recommendation: "adopt as a Phase 3 foundation."

This record now converts those recommendations into **accepted decisions**. The
closed Phase 0 registers are unchanged by this record.

## 6. Canonical evidence references (repository truth)

- Plan L12 — "`InventorAI` … temporary working name only; not approved as the
  final public brand."
- Plan L122 — "The name `InventorAI` is hard-coded in many locations and is not
  centrally configurable."
- Plan §3.1 "Product name and branding" L131–138:
  - (1) `InventorAI` is a temporary working name.
  - (2) The final public name remains undecided because of possible market and
    intellectual-property conflicts.
  - (3) The product must support centralized brand replacement.
  - (4) Product identity must not be hard-coded into core contracts, database
    meaning, domain logic, or engine behavior.
  - (5) Future branding must use centrally managed values such as `PRODUCT_NAME`,
    `PRODUCT_SHORT_NAME`, `PRODUCT_TAGLINE`, `LEGAL_ENTITY_NAME`, `SUPPORT_EMAIL`,
    `PRIMARY_DOMAIN`.
  - (6) Renaming must not alter project IDs, evidence IDs, API resource
    identities, or historical audit records without an explicit migration
    decision.
- `docs/governance/evidence/phase0_evidence_lock/OPEN_OWNER_DECISIONS_REGISTER.md`
  — OD-A and OD-B entries.
- Plan Phase 2 "Required work" — includes "define central branding **boundaries**".
- Plan Phase 3 — "Must include: **brand-neutral application shell** …"; Phase 3F
  Bounded Implementation Increments (where implementation is contracted).

## 7. Accepted options

- **OD-A:** keep `InventorAI` as a temporary internal working name; defer the
  final public product name to a separate market/trademark/domain/brand
  validation gate.
- **OD-B:** adopt centralized branding indirection as a required Phase 3
  foundation; the future foundation may centralize values such as `PRODUCT_NAME`,
  `PRODUCT_SHORT_NAME`, `PRODUCT_TAGLINE`, `LEGAL_ENTITY_NAME`, `SUPPORT_EMAIL`,
  `PRIMARY_DOMAIN`.

## 8. Rejected alternatives and reasons

| Alternative | Rejected because |
|---|---|
| Select the final public name now | Market/IP/trademark/domain conflicts are unassessed; a separate validation gate is required (plan §3.1 (2)). Premature selection risks rework and legal exposure. |
| Immediate repository-wide rename | The name is hard-coded in many locations (plan L122) and renaming could touch IDs/APIs/DB/audit records; §3.1 (6) forbids that without an explicit migration decision. |
| Implement branding constants now | Implementation belongs to Phase 3 (brand-neutral shell / bounded increments); Phase 3 is NOT STARTED / NOT AUTHORIZED. |
| Embed branding into engine/contracts/IDs | Violates §3.1 (4) and the required design boundary; would couple identity to semantics. |
| Leave the name hard-coded with no indirection plan | Blocks any future rename; contradicts §3.1 (3). |

## 9. Immediate effects

- `InventorAI` is confirmed as a temporary internal working name only; no public
  brand approval is granted.
- Centralized branding indirection is an owner-approved **future** Phase 3
  foundation requirement.
- No document text changes beyond this durable record, the smallest plan status
  synchronization, and one appended roadmap record. No code, template, or
  identifier changes.

## 10. Deferred effects

- **Final public name** is deferred to a separate market/trademark/domain/brand
  validation gate (not scheduled or authorized here).
- **Branding-indirection implementation** is deferred to Phase 3 under a separate
  Phase 3 authorization.
- Any migration affecting identifiers, APIs, database meaning, or historical
  records requires a separate explicit owner decision and governed implementation
  gate.

## 11. Required design boundary (forward constraint, non-activating)

The future branding foundation may centralize: `PRODUCT_NAME`,
`PRODUCT_SHORT_NAME`, `PRODUCT_TAGLINE`, `LEGAL_ENTITY_NAME`, `SUPPORT_EMAIL`,
`PRIMARY_DOMAIN`. Branding values must **not** alter or become embedded in: core
engine behavior; deterministic progression contracts; project identifiers;
evidence identifiers; database semantic identity; API resource identity; domain
logic; historical audit records. This is a recorded constraint for future work;
it authorizes no implementation.

## 12. Exact authorization boundaries — what this record authorizes

- Recording OD-A and OD-B as accepted owner decisions (documentation only).
- The smallest plan status synchronization and one appended roadmap record.

## 13. What this record does NOT authorize

- Selecting or suggesting a final public product name.
- Any trademark, domain, or brand clearance (none is performed or claimed here).
- Implementing branding constants or centralized values.
- Editing UI, templates, runtime code, tests, schemas, APIs, database structures,
  or identifiers.
- Renaming the repository, package, modules, historical records, or evidence.
- Modifying the OD-C record, closed Phase 0 evidence, or
  `OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
- Beginning OD-D…OD-Q.
- Activating Phase 2 or Phase 3.
- Any implementation or deployment authority.

## 14. Product-name status

```
FINAL PUBLIC PRODUCT NAME:   NOT YET SELECTED
CURRENT "InventorAI" NAME:   TEMPORARY INTERNAL WORKING NAME ONLY
PUBLIC BRAND APPROVAL:       NOT GRANTED
IMMEDIATE RENAME:            NOT AUTHORIZED
```

## 15. Branding-indirection status

```
CENTRALIZED BRANDING INDIRECTION:  OWNER-APPROVED FUTURE FOUNDATION
CURRENT BRANDING IMPLEMENTATION:   NOT AUTHORIZED
IMPLEMENTATION:                    DEFERRED TO PHASE 3
SEPARATE PHASE 3 AUTHORIZATION:    REQUIRED
```

## 16. Phase 2 boundary-definition dependency (textually supported)

Phase 2 — Governance and Architecture Corrections, "Required work" — explicitly
includes **"define central branding boundaries"**. Therefore the *boundary
definition* for branding is textually assigned to Phase 2 (proven, not inferred).
Phase 2 remains **NOT STARTED / NOT AUTHORIZED**.

## 17. Phase 3 implementation dependency

Phase 3 — Product UX/UI Foundation — owns the brand-neutral application shell and
the bounded implementation increments (Phase 3F) where any branding-indirection
implementation would occur. OD-B's implementation is therefore deferred to
Phase 3. Phase 3 remains **NOT STARTED / NOT AUTHORIZED**.

## 18. Neither Phase 2 nor Phase 3 is activated

```
PHASE 2: NOT STARTED — NOT AUTHORIZED
PHASE 3: NOT STARTED — NOT AUTHORIZED
```

Recording a Phase 2/Phase 3 dependency is sequencing only; it does not begin
either phase. No phase sequence or later-phase substantive scope is changed by
this record.

## 19. Remaining open owner decisions

`OD-D, OD-E, OD-F, OD-G, OD-H, OD-I, OD-J, OD-K, OD-L, OD-M, OD-N, OD-O, OD-P,
OD-Q` remain **OPEN and unresolved**. **OD-C** remains previously accepted and
merged via PR #293 and is **unchanged** by this record. Only OD-A and OD-B are
decided here.

## 20. Implementation and deployment authority

```
IMPLEMENTATION AUTHORITY: NONE
DEPLOYMENT AUTHORITY:     NONE
```

Product remains `DEMO_READY_WITH_LIMITATIONS`; Electronics/Electrical remains the
only current MVP runtime scope; the product is NOT PRODUCTION READY.

## 21. Evidence classification

This is a **Phase 1 owner-decision evidence artifact** (documentation only). It
is authoritative as a record of the owner's accepted OD-A and OD-B decisions once
independently reviewed, owner-accepted, merged, and post-merge verified. Its
authority is that of a decision record; it grants no implementation or deployment
authority. No final public name is selected; no trademark/domain clearance is
claimed; no branding implementation is claimed.
