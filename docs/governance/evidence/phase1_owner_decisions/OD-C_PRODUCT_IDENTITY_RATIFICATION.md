# Phase 1 — Owner Decision OD-C — Product-Identity Ratification

**Phase:** Phase 1 — Owner Product Decisions
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Decision ID:** OD-C (Phase 0 Open Owner Decisions Register).
**Scope:** documentation-only durable record of a single accepted owner decision.
**No implementation. No code, test, or engine change. No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official tip at reconstruction:** `168703aac4e6f7887d76fa3e89cccfcce8ed14de`.

---

## 1. Decision status

```
OD-C — OWNER DECISION ACCEPTED
```

This record is a durable Phase 1 evidence artifact. It records exactly one
accepted owner decision. It resolves no other open owner decision, remediates no
conflict textually, and activates no downstream phase or capability.

## 2. Accepted owner decision (verbatim)

> **OD-C — OWNER DECISION ACCEPTED / RATIFY THE SUBSTANTIVE PRODUCT-IDENTITY
> CORRECTION, AND AMEND ITS ACTIVATION CONDITIONS TO THE CURRENT GOVERNED
> OFFICIAL-BRANCH MODEL.**

The owner ratifies the **substance** of the product-identity correction recorded
in `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md` — that InventorAI is a
governed idea-development and cross-domain invention-orchestration platform, in
which the idea is the primary subject and inventor learning is a secondary
effect. The owner further decides that the **activation mechanism** of that
correction — its §11 EFFECTIVE conditions, which literally require
`HEAD = origin/main` and `ahead/behind = 0 0` — must be **amended** to the
current governed official-branch authority model, because those literal §11
conditions cannot be satisfied on the authoritative feature branch.

## 3. Required status block

```
SUBSTANTIVE PRODUCT IDENTITY:            OWNER-RATIFIED
ORIGINAL §11 ACTIVATION CONDITIONS:      NOT SATISFIED
ACTIVATION MECHANISM:                    REQUIRES GOVERNED TEXTUAL AMENDMENT
CR-3:                                    OWNER DECISION RESOLVED /
                                         TEXTUAL REMEDIATION PENDING /
                                         NOT FORMALLY CLOSED
IMPLEMENTATION AUTHORITY:                NONE
DEPLOYMENT AUTHORITY:                    NONE
```

## 4. Prior Phase 0 recommendation status (context, not authority)

In the Phase 0 Open Owner Decisions Register, OD-C was recorded only as a
`RECOMMENDATION — NOT OWNER DECISION`, sequenced as **B — the first owner
decision inside Phase 1** (sequencing only; it did not begin Phase 1). The
options recorded there were: (a) ratify effective status; (b) amend §11 to the
current branch model; (c) formally keep PROPOSED. This record now converts the
owner's choice into an **accepted decision**: ratify the substance (a) **and**
amend the activation mechanism (b). Phase 0 registers remain unchanged by this
record.

## 5. Related conflict — CR-3

- **Conflict:** CR-3 — Product-identity correction activation ambiguity (MEDIUM).
- **Basis (Phase 0 Conflict Register / Raw Evidence Appendix §8):**
  - `OWNER_PRODUCT_IDENTITY_CORRECTION.md` (`5768d31…`) §1 L18–21 / §11 L331–354
    — "PROPOSED until §11 satisfied … EFFECTIVE only upon … HEAD = origin/main
    and ahead/behind = 0 0".
  - `STRATEGIC_PRODUCT_VISION.md` (`6c2277f…`) L46–47 — "GOVERNING EFFECT
    AMENDED … amended by the **active** Level 0 Owner Amendment".
  - `CLAUDE.md` (`4251e99…`) L11 — lists the identity correction as mandatory
    read #2.
  - Branch evidence — official feature tip ≠ `origin/main`
    (`0e89e4636399760965c9ff8086b465c90dbadf8e`); `HEAD = origin/main` never
    holds on the feature branch.
- **Effect of OD-C on CR-3:** the owner **decision** that resolves the ambiguity
  is now recorded, but the governing document text (§11) is **not yet amended**.
  CR-3 is therefore **OWNER DECISION RESOLVED / TEXTUAL REMEDIATION PENDING /
  NOT FORMALLY CLOSED**. This record does not formally close CR-3.

## 6. Canonical evidence references (repository truth)

- `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md` — Level 0 owner
  amendment; the subject of ratification; its §11 activation clause is the CR-3
  subject. **Not modified by this record.**
- `docs/governance/evidence/phase0_evidence_lock/CONFLICT_REGISTER.md` — CR-3.
- `docs/governance/evidence/phase0_evidence_lock/OPEN_OWNER_DECISIONS_REGISTER.md`
  — OD-C and OD-A…OD-Q.
- `docs/governance/evidence/phase0_evidence_lock/PHASE_0_RAW_EVIDENCE_APPENDIX.md`
  — §8 (refined CR-3 branch and authority evidence).
- `docs/governance/evidence/phase0_evidence_lock/FORMAL_CLOSURE.md` — Phase 0
  formal closure (CR-3/OD-C carried forward unresolved).
- `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`
  — canonical plan; Phase 2 required work includes "clarify document authority
  and activation conditions".

## 7. Accepted interpretation

1. The product identity described in `OWNER_PRODUCT_IDENTITY_CORRECTION.md` is
   **owner-ratified as substantively correct** and governs product intent: the
   idea is the primary subject; inventor learning is a secondary effect; the
   deterministic engine is authoritative and AI is advisory-only.
2. The identity correction's **literal §11 activation conditions are not
   satisfied** and, on the authoritative feature-branch model, cannot be
   satisfied as written.
3. The correct remedy is a **governed textual amendment** of the activation
   mechanism (§11) to the current official-branch authority model — performed
   later, under separate authorization, not in this record.

## 8. Rejected alternatives and reasons

| Alternative | Rejected because |
|---|---|
| (c) Keep the correction formally PROPOSED | Leaves the effective-vs-proposed ambiguity (CR-3) unresolved; higher/later sources already treat the identity as operative, so "PROPOSED" contradicts governing effect. |
| Declare §11 already satisfied / silently treat as EFFECTIVE | False against repository truth — `HEAD = origin/main` is not satisfied; would inject an unverifiable activation claim. |
| Amend §11 text now, inside this record | Out of authorized scope; textual remediation of a Level 0 amendment belongs to Phase 2 ("clarify document authority and activation conditions") under separate authorization. |
| Edit the closed Phase 0 registers to record OD-C | Phase 0 is FORMALLY CLOSED; its evidence is append-only history and must not be mutated. A new Phase 1 record is the correct location. |

## 9. Immediate effect

- The **substance** of the product identity is owner-ratified and may be relied
  upon as the governing product-identity intent.
- No document text is changed by this decision beyond this durable record, the
  smallest plan status synchronization, and one appended roadmap record.
- `OWNER_PRODUCT_IDENTITY_CORRECTION.md` is **unchanged**; its §11 remains
  literally unsatisfied and awaits governed amendment.

## 10. Deferred textual remediation

The governed textual amendment of the §11 activation conditions to the current
official-branch model is **deferred to Phase 2 — Governance and Architecture
Corrections**, whose required work explicitly includes "clarify document
authority and activation conditions". This assignment is **textually proven** in
the canonical plan (Phase 2 "Required work"), not inferred. Phase 2 is
**NOT STARTED and NOT AUTHORIZED** by this record.

## 11. What this record authorizes

- Recording OD-C as an accepted owner decision (documentation only).
- Relying on the ratified product identity as governing product intent.
- The smallest plan status synchronization and one appended roadmap record
  reflecting that Phase 1 has started and OD-C is accepted.

## 12. What this record does NOT authorize

- Any code, test, engine, schema, scoring, fixture, or runtime change.
- Amending, editing, or activating `OWNER_PRODUCT_IDENTITY_CORRECTION.md` §11.
- Formally closing CR-3.
- Deciding or resolving any other open owner decision (OD-A, OD-B, OD-D…OD-Q).
- Starting or authorizing Phase 2 or any later phase.
- Any implementation, deployment, multi-domain activation, persistence,
  accounts, authentication, subscription, or billing work.
- Modifying the closed Phase 0 evidence set.
- Closing, modifying, or reopening PR #162 or PR #167, or deleting any branch.

## 13. Phase 2 dependency (textually proven)

The §11 textual amendment depends on Phase 2. Proof (canonical plan, Phase 2 —
Governance and Architecture Corrections, "Required work"): the list explicitly
contains **"clarify document authority and activation conditions"**. No inference
is used. Phase 2 remains **NOT STARTED / NOT AUTHORIZED**.

## 14. CR-3 current status

```
CR-3 — OWNER DECISION RESOLVED — TEXTUAL REMEDIATION PENDING — NOT FORMALLY CLOSED
```

The owner decision exists; the governing text is not yet amended; CR-3 is not
formally closed by this record.

## 15. Remaining open owner decisions

`OD-A, OD-B, OD-D, OD-E, OD-F, OD-G, OD-H, OD-I, OD-J, OD-K, OD-L, OD-M, OD-N,
OD-O, OD-P, OD-Q` remain **OPEN and unresolved**. Only OD-C is decided by this
record.

## 16. Implementation authority

```
IMPLEMENTATION AUTHORITY: NONE
```

## 17. Deployment authority

```
DEPLOYMENT AUTHORITY: NONE
```

Product remains `DEMO_READY_WITH_LIMITATIONS`; Electronics/Electrical remains the
only current MVP runtime scope; the product is NOT PRODUCTION READY.

## 18. Evidence classification

This is a **Phase 1 owner-decision evidence artifact** (documentation only). It
is authoritative as a record of the owner's accepted OD-C decision once it has
been independently reviewed, owner-accepted, merged, and post-merge verified. Its
authority is that of a decision record; it grants no implementation or deployment
authority.

## 19. Reconstruction provenance

This record is a **fresh reconstruction**. The four kinds of evidence it draws on
are distinguished as follows:

- **Owner-decision evidence:** the owner's accepted OD-C decision, issued in the
  execution conversation as an owner authorization. This is the authority for the
  *decision content* recorded in §2–§3.
- **Repository evidence:** the committed canonical sources — the Phase 0 evidence
  registers, `OWNER_PRODUCT_IDENTITY_CORRECTION.md`, and the canonical plan — at
  verified official tip `168703aac4e6f7887d76fa3e89cccfcce8ed14de`. This is the
  authority for every citation of conflict, activation clause, and Phase 2
  assignment.
- **Executor-created documentation:** this file and the accompanying smallest
  plan status synchronization and single appended roadmap record. These are
  drafted by the executing session and carry no authority until independently
  reviewed, owner-accepted, merged, and post-merge verified.
- **Lost-unreviewed-candidate history:** a prior local candidate for this record.

> A prior local candidate was reported but was never independently verified,
> pushed, merged, or made authoritative and became unavailable in an ephemeral
> environment. This record is a fresh reconstruction from the accepted owner
> decision and current canonical repository evidence.

No content, SHA, bundle identity, or timestamp of the lost candidate is reused or
cited as authoritative. This reconstruction is derived solely from the accepted
owner decision and current committed repository evidence.
