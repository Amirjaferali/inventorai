# Phase 1 — Owner Decisions OD-D and OD-E — Evidence Register and Legal Boundary

**Phase:** Phase 1 — Owner Product Decisions
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Decision IDs:** OD-D (evidence/provenance/contribution/ownership-claims register)
and OD-E (legal ownership, inventorship, and patentability boundary) — recorded
together because they are directly linked (OD-E constrains what OD-D's register
may assert).
**Scope:** documentation-only durable record of two accepted, linked owner
decisions. **No implementation. No register schema, database, persistence,
access control, enforcement, legal wording, or runtime change. No downstream
activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official base at authoring:** `abfca78216bd51c93419f29f52f4b5986acb8c40`
(official tip after PR #294, which merged the corrected OD-A/OD-B increment).

---

## 1. Decision status

```
OD-D — OWNER DECISION ACCEPTED
OD-E — OWNER DECISION ACCEPTED
```

This record records exactly two accepted owner decisions. It resolves no other
open owner decision, implements no register, states no legal finding, and
activates no downstream phase.

## 2. Accepted owner decisions (verbatim)

### OD-D — Evidence / Provenance / Contribution / Ownership-Claims Register

> **OD-D — OWNER DECISION ACCEPTED**
>
> ADOPT AN EPISTEMIC EVIDENCE, PROVENANCE, CONTRIBUTION, AND OWNERSHIP-CLAIMS
> REGISTER. DURABLE PERSISTENCE AND ENFORCEMENT ARE DEFERRED TO PHASE 4 UNDER
> SEPARATE AUTHORIZATION.

Required meaning:
- The register may record evidence items, source attribution, timestamps,
  contributor records, authorship claims, ownership claims, references,
  uncertainty, and supporting evidence.
- Every recorded ownership or authorship claim remains an assertion or evidence
  record, not a legal finding.
- No durable database model, persistence, migration, access control, retention
  policy, enforcement, or production capability is authorized now.
- Any durable implementation belongs to Phase 4 under separate owner
  authorization.

### OD-E — Legal Ownership, Inventorship and Patentability Boundary

> **OD-E — OWNER DECISION ACCEPTED**
>
> THE PRODUCT MAY DOCUMENT CLAIMS, EVIDENCE, PROVENANCE, AND CONTRIBUTIONS, BUT
> MUST NOT DETERMINE OR REPRESENT LEGAL OWNERSHIP, INVENTORSHIP, OR
> PATENTABILITY.

Required meaning:
- The product must not claim to prove legal ownership.
- The product must not determine legal inventorship.
- The product must not determine patentability.
- The product must not determine freedom to operate.
- The product must not claim prior-art clearance.
- The product must not determine legal validity, filing readiness, entitlement,
  or enforceability.
- The product must not replace legal counsel, patent counsel, or qualified
  intellectual-property advice.
- Any future legal-facing wording, workflow, export, or disclaimer requires
  separate review and authorization.

## 3. Distinguished status (must be read exactly)

```
EPISTEMIC RECORDING:              OWNER-APPROVED
LEGAL OWNERSHIP DETERMINATION:    PROHIBITED
INVENTORSHIP DETERMINATION:       PROHIBITED
PATENTABILITY DETERMINATION:      PROHIBITED
DURABLE REGISTER IMPLEMENTATION:  DEFERRED TO PHASE 4
CURRENT IMPLEMENTATION AUTHORITY: NONE
```

## 4. Why OD-D and OD-E are recorded together

OD-D authorizes an epistemic register that may *record* ownership and authorship
claims; OD-E defines the hard boundary that those recordings are assertions and
evidence, never legal determinations. The two are inseparable: the register
(OD-D) is safe to adopt only under the legal boundary (OD-E). Recording them in
one combined artifact keeps the linked decision coherent and is the smallest
durable increment. This combination is documentation structure only; each
decision retains its own identifier and status.

## 5. Prior Phase 0 recommendation status (context, not authority)

In the Phase 0 Open Owner Decisions Register both were recorded only as
`RECOMMENDATION — NOT OWNER DECISION`:
- OD-D recommendation: "epistemic register; durable form gated to Phase 4."
- OD-E recommendation: "confirm 'documents claims; no legal determination.'"

This record now converts those recommendations into **accepted decisions**. The
closed Phase 0 registers are unchanged by this record.

## 6. Canonical evidence references (repository truth)

- Plan §3.5 L163–169 — "Evidence, Provenance, Contribution and Ownership-Claims
  Register … must **eventually** support evidence items, source attribution,
  timestamps, contributor records, authorship claims, ownership claims, … access
  control, and retention/deletion rules." ("eventually" = deferred.)
- Plan §3.5 L171 — "The application may document claims and evidence but **MUST
  NOT** claim to legally determine ownership, inventorship, patentability,
  freedom to operate, prior-art clearance, legal validity, filing readiness, or
  entitlement."
- Plan L121 — "Evidence/provenance functions exist partially, but no durable
  legal ownership register is implemented."
- Plan Phase 4 "Must include" (L277) — "persistent project storage; … evidence
  model; provenance model; contribution model; **ownership-claims model**; …
  migration from the in-memory model" (durable form owned by Phase 4).
- Plan L271 (Phase 3 "Must not … prove legal ownership"), L338 (Phase 10
  "intellectual-property disclaimers; ownership-claims disclaimers"), L416
  (Patent Export not filing-ready/legally valid unless separately established).
- `docs/governance/evidence/phase0_evidence_lock/OPEN_OWNER_DECISIONS_REGISTER.md`
  — OD-D and OD-E entries (SPV §10, SPV §5B).

## 7. Accepted interpretation

1. An **epistemic** register is owner-approved: it may record evidence,
   provenance, contribution, and ownership/authorship *claims* with attribution,
   timestamps, references, and uncertainty.
2. Every recorded claim is an **assertion / evidence record**, never a legal
   finding.
3. The **durable** form of the register (persistence, access control, retention,
   audit, enforcement, migration) is deferred to **Phase 4** under separate
   authorization; nothing durable is authorized now.
4. The product **must not** determine or represent legal ownership,
   inventorship, patentability, freedom to operate, prior-art clearance, legal
   validity, filing readiness, entitlement, or enforceability, and must not
   replace professional legal/IP advice.

## 8. Rejected alternatives and reasons

| Alternative | Rejected because |
|---|---|
| Adopt a durable/enforcing register now | Needs Phase 4 persistence; Phase 4 is NOT STARTED / NOT AUTHORIZED; would authorize unbuilt DB/access-control/migration. |
| Let the product determine legal ownership/inventorship/patentability | Directly violates plan §3.5 L171; creates legal exposure and false assurance; rejected. |
| Weaken or omit the legal disclaimer | Same legal-exposure risk; §3.5 requires the MUST-NOT boundary. |
| Record OD-D without OD-E | Unsafe — a claims register without the legal boundary invites misreading claims as findings. |
| Edit the closed Phase 0 registers or merged OD records to add OD-D/OD-E | Those are append-only history / previously merged; a new Phase 1 record is the correct location. |

## 9. Immediate effect

- The epistemic recording scope (OD-D) and the legal boundary (OD-E) are
  owner-accepted and govern future design intent for evidence/claims handling.
- No document text changes beyond this durable record, the smallest plan status
  synchronization, and one appended roadmap record. No schema, code, persistence,
  or legal-facing wording changes.

## 10. Deferred effect

- **Durable register implementation** (persistence, data model, access control,
  retention/deletion, audit, enforcement, migration from the in-memory model) is
  deferred to **Phase 4** under separate authorization.
- **Any future legal-facing wording, workflow, export, or disclaimer** requires
  separate review and authorization.

## 11. Epistemic-register scope (recorded, non-activating)

The register may record: evidence items; source attribution; timestamps;
contributor records; authorship claims; ownership claims; references;
uncertainty; and supporting evidence. All such entries are assertions / evidence
records. No durable persistence, access control, retention, enforcement, or
production capability is authorized by this record.

## 12. Legal-boundary scope (recorded, non-activating)

The product must not: prove legal ownership; determine legal inventorship;
determine patentability; determine freedom to operate; claim prior-art
clearance; determine legal validity, filing readiness, entitlement, or
enforceability; or replace legal/patent/IP counsel. Any legal-facing wording is
gated to separate review and authorization.

## 13. Distinction between claims, evidence, and legal findings

```
CLAIM:          a recorded assertion (e.g. an ownership or authorship claim).
EVIDENCE:       recorded material supporting or contextualizing a claim.
LEGAL FINDING:  a determination of legal ownership/inventorship/patentability —
                NOT produced, represented, or implied by the product.
```

The register records claims and evidence; it never elevates them to legal
findings.

## 14. What this record authorizes

- Recording OD-D and OD-E as accepted owner decisions (documentation only).
- The smallest plan status synchronization and one appended roadmap record.

## 15. What this record prohibits

- Designing or implementing the register schema; creating database tables or
  migrations; implementing persistence, access control, retention, deletion,
  audit, enforcement, or production workflows.
- Creating legal conclusions or legal-advice language.
- Claiming ownership, inventorship, patentability, freedom to operate, prior-art
  clearance, filing readiness, entitlement, or legal validity.
- Modifying runtime code, tests, APIs, schemas, templates, exports, or UI.
- Modifying Phase 0 evidence, the OD-A/OD-B or OD-C records, or
  `OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
- Beginning OD-F…OD-Q.
- Activating Phase 2 or Phase 4.
- Any implementation or deployment authority.

## 16. Phase 4 durable-persistence dependency (textually supported)

Plan Phase 4 — Durable Data and Evidence Foundation, "Must include" (L277) —
explicitly lists "persistent project storage; … evidence model; provenance
model; contribution model; **ownership-claims model**; … migration from the
in-memory model", and its hard rule (L279) prohibits paid subscription until
Phase 4 is formally closed. Therefore the durable form of the OD-D register is
textually assigned to Phase 4 (proven, not inferred).

## 17. Phase 4 is not activated

```
PHASE 2: NOT STARTED — NOT AUTHORIZED
PHASE 4: NOT STARTED — NOT AUTHORIZED
```

Recording a Phase 4 dependency is sequencing only; it does not begin Phase 4. No
phase sequence or later-phase substantive scope is changed by this record.

## 18. Remaining owner decisions

`OD-F, OD-G, OD-H, OD-I, OD-J, OD-K, OD-L, OD-M, OD-N, OD-O, OD-P, OD-Q` remain
**OPEN and unresolved**. **OD-A, OD-B, OD-C** remain previously accepted and
merged and are **unchanged** by this record. Only OD-D and OD-E are decided here.

## 19. Implementation and deployment authority

```
IMPLEMENTATION AUTHORITY: NONE
DEPLOYMENT AUTHORITY:     NONE
```

Product remains `DEMO_READY_WITH_LIMITATIONS`; Electronics/Electrical remains the
only current MVP runtime scope; the product is NOT PRODUCTION READY.

## 20. Evidence classification

This is a **Phase 1 owner-decision evidence artifact** (documentation only). It
is authoritative as a record of the owner's accepted OD-D and OD-E decisions once
independently reviewed, owner-accepted, merged, and post-merge verified. Its
authority is that of a decision record; it grants no implementation or deployment
authority. No durable register is implemented; no legal determination is made or
implied; professional legal/IP advice is not replaced.
