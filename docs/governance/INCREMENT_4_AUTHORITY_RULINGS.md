# Increment 4 Authority Rulings

Status:
`OWNER-APPROVED TEXT — PENDING COMMITTED GOVERNANCE INTEGRATION`

## 1. Document status

This document records the owner-approved authority-ruling TEXT for Increment 4
(`Atomic Requirements & Criticality-Aware Risk Register`). The text is
owner-approved, but it is NOT yet committed repository authority.

This document does NOT claim to be:

- committed;
- merged;
- active repository authority;
- an implementation authorization;
- a tests-first authorization;
- a design authorization;
- an implementation-contract authorization.

The rulings below become committed repository authority ONLY after a separate,
explicit independent review, and separate commit, push, PR, and true-merge
authorizations. Creating this document does not change the live authoritative
branch and does not advance the product-execution tip.

## 2. Repository and governance context

- Authoritative branch: `feature/atomic-json-session-persistence`.
- The live authoritative tip is always resolved from Git; it is not permanently
  pinned by this prose. At the time this text was prepared, the authoritative tip
  was the PR #46 governance-synchronization true-merge, and the recorded
  product-execution tip was the Increment 3 SOURCE true-merge (PR #45). Per the
  roadmap's stable-SHA rule, later merges do not falsify that publication baseline
  and require no recursive SHA-only update; no SHA is asserted here as the current
  live tip.
- Increment 3 — Visible Idea-Development Outputs — is IMPLEMENTED, TRUE-MERGED,
  POST-MERGE VERIFIED, and CLOSED; its implementation authority is CONSUMED AND
  CLOSED. This document preserves Increment 3 as closed.
- The active anchor and the committed governance ordering (Product-Value
  Correction Plan: 3 → 4 → 5 → 6) are preserved and unchanged.
- The frozen persistence worktree remains PRESERVE UNMODIFIED AND PAUSE and is not
  a dependency of Increment 4.

## 3. Increment 4 identity

Increment 4 is:

`Atomic Requirements & Criticality-Aware Risk Register`

It converts Increment 2's already-recorded truthful state (assertions, gaps,
contradictions, evidence and specialist dispositions, validation status) into
provenance-anchored ATOMIC requirements and an evidence-grounded,
CRITICALITY-AWARE view — making the requirement landscape and its grounded risks
visible for developing the IDEA. It adds no new truth; it reorganizes and explains
already-recorded facts.

## 4. Purpose of the rulings

These rulings fix the product and authority boundaries for Increment 4. They:

- do NOT authorize design, tests, or source implementation;
- preserve Increment 3 as closed;
- preserve the active anchor;
- prevent hidden scoring, fabricated requirements, unsupported criticality, and
  uncontrolled scope expansion.

## 5. Binding interpretation rules

Normative terms `MUST`, `MUST NOT`, and `MAY` are used in their usual sense. The
following principles are binding on every ruling below:

- No requirement MAY exist without one primary provenance anchor.
- One primary anchor MAY have zero or more supporting references.
- A source MAY yield more than one requirement only through provenance-safe
  deterministic splitting.
- Requirements MUST NOT be invented.
- Criticality MUST NOT depend on maturity, readiness, stage, scoring, or
  progression.
- `UNMET` MUST NOT automatically produce a risk.
- A risk requires a recorded grounded adverse consequence.
- Increment 4 MUST NOT modify Increment 3.
- Increment 4 remains stateless and non-persistent.
- The deliverable is the CORE visible surface.
- A session summary is OPTIONAL and separately authorized.
- `_s4` and `_s6` remain unchanged.
- Increment 4 MUST NOT turn InventorAI into a professional requirements-management
  workspace.

InventorAI remains an idea-development platform, not a professional
requirements-management workspace.

## 6. Scope classifications

### CORE

- provenance-anchored requirement formulation;
- deterministic atomic splitting;
- stable derived identifiers;
- source-mirrored lifecycle;
- grounded criticality categories;
- visible criticality authority;
- grounded-consequence risk traceability;
- one additive deliverable section;
- stateless derivation;
- Increment 3 non-reopening;
- `_s4`/`_s6` non-regression.

### OPTIONAL

- supporting-reference display;
- richer rationale;
- a compact session summary, only after separate authorization.

### DEFERRED

- `_s4`/`_s6` consolidation or migration;
- persisted requirement records;
- an owner/specialist criticality-confirmation workflow beyond the existing
  pending-specialist signal;
- cross-domain orchestration.

### PROHIBITED

- requirements without provenance;
- invented facts or engineering obligations;
- numeric scoring;
- maturity/readiness/stage/progression effects;
- automatic risk from `unmet`;
- unsupported safety/regulatory/specialist criticality;
- persistence in Increment 4;
- domain expansion;
- domain-registry repair;
- a specialist workspace;
- a professional requirements-management workspace;
- `_s4` or `_s6` modification;
- UI redesign;
- optional session implementation without separate authorization.

## 7. Rulings

### C4-R1 — Requirement formulation authority

The system MAY formulate a requirement statement ONLY by restating or organizing
an existing, identified record resident in `IdeaState`. Each requirement MUST have
exactly ONE primary provenance anchor and MAY have zero or more supporting
references. No requirement MAY exist without a primary anchor. The system MUST NOT
invent a requirement, infer an unsupported engineering obligation, or create any
new domain fact.

Permitted primary anchors are exactly:

- assertion;
- gap;
- active contradiction;
- pending evidence need;
- pending specialist need.

A recommendation MAY appear ONLY as a supporting reference, never as a primary
anchor. Maturity state MUST NOT be a primary anchor.

### C4-R2 — Atomicity

```text
A requirement expresses exactly one independently resolvable or
verifiable concern and exactly one required outcome.

One primary provenance anchor may produce more than one atomic
requirement only when the source explicitly contains multiple
separable concerns and each requirement is traceable to a distinct
source fragment.

Each such requirement retains:
1. the same primary provenance anchor;
2. a deterministic source-fragment discriminator;
3. zero or more supporting references.

When provenance-safe deterministic splitting is not possible, the
system preserves one unresolved coarse item rather than inventing
sub-requirements.
```

### C4-R3 — Requirement identity and lifecycle

Requirement identifiers MUST be derived from the primary anchor's stable identity
and MUST NOT depend on global output order. When one source yields multiple
requirements under C4-R2, identifiers MUST append a deterministic source-local
discriminator tied to the distinct source fragment. Requirement status MUST mirror
the source state; inactive or superseded anchors MUST be excluded (per the
Increment 2 active-set rule). Requirements are stateless render-time derivations;
requirement status MUST NOT be directly editable. Legacy or empty state MUST
return a safe empty set without error. This ruling fixes stable semantics only and
prescribes no final code format.

### C4-R4 — Criticality meaning and categories

```text
Criticality describes the evidenced effect of an unmet requirement
on the idea. It does not describe an effect on maturity, stage,
readiness, scoring, or progression.

FEASIBILITY-THREATENING:
Failure to satisfy the requirement may prevent the idea or mechanism
from performing its stated essential function, as grounded in
recorded evidence.

VALUE-ENHANCING:
The requirement improves usefulness, reliability, clarity,
efficiency, or practical value but is not evidenced as necessary
for the essential function.

REFINEMENT:
The requirement improves an already viable or validated element
without evidence that its absence threatens the essential function.

UNDETERMINED:
The repository lacks sufficient authority for another category.
```

Additionally:

- there MUST be no numeric scores;
- maturity alone MUST NEVER ground criticality;
- every non-`UNDETERMINED` category MUST carry recorded rationale;
- the system MUST NOT independently assert safety, regulatory, or specialist
  severity.

### C4-R5 — Criticality confirmation authority

Each criticality label MUST carry an explicit authority, exactly one of:

- system-derived;
- owner-confirmed;
- specialist-confirmed;
- undetermined.

The visible output MUST display the authority. A system inference MUST NEVER be
presented as owner-confirmed or specialist-confirmed.

### C4-R6 — Requirement-to-risk relationship

```text
An unmet requirement does not automatically produce a risk.

A requirement-linked risk may exist only when a grounded adverse
consequence of failing the requirement is recorded.

Traceability:
requirement
→ primary provenance anchor
→ supporting evidence or contradiction
→ grounded adverse consequence
→ risk entry, when present.

One requirement may have zero or more risks.
One risk may be supported by one or more requirements.

The system must not create a generic risk by merely restating that
the requirement is unmet.
```

The existing `_s6` risk register MUST remain unchanged during Increment 4.

### C4-R7 — Increment 3 boundary

Increment 4 MUST NOT modify:

- the seven-level Increment 3 presentation priority;
- rulings R-1 through R-6;
- `derive_next_development_step`;
- its inputs;
- its payload fields;
- its selected result.

A requirement-specific resolving action MUST use a distinct label and MUST NOT be
presented or treated as the global Next Development Step.

### C4-R8 — Progression and maturity boundary

Unmet or critical requirements MUST have no effect on:

- maturity;
- readiness;
- stage;
- scoring;
- progression.

No indirect effect is permitted.

### C4-R9 — Persistence boundary

Increment 4 outputs MUST be:

- derived;
- stateless;
- non-persistent;
- dependent only on committed `IdeaState` evidence;
- independent of the frozen persistence worktree.

### C4-R10 — Domain and specialist boundary

Increment 4 MUST be:

- idea-driven;
- domain-neutral in engine semantics;
- bounded to the currently authorized MVP.

It MUST NOT expand domains, MUST NOT repair the domain registry, MUST NOT create a
new specialist workflow, and MUST NOT create a specialist workspace or a
professional requirements-management workspace. The existing Increment 2
pending-specialist signal MAY be surfaced only.

InventorAI remains an idea-development platform, not a professional
requirements-management workspace.

### C4-R11 — User-visible surfaces

CORE:

```text
one additive Increment 4 deliverable section
```

Required visible fields:

- requirement statement;
- human-readable provenance;
- source-mirrored status;
- criticality category;
- criticality authority;
- grounded rationale;
- linked risk only where a grounded adverse consequence exists;
- requirement-specific resolving action when supported.

OPTIONAL and NOT part of the minimum Increment 4 contract:

```text
compact session summary
```

A session surface requires later separate justification and authorization; it is
not part of the minimum contract unless a later design assessment proves distinct
user value beyond the Increment 3 global next-step callout. The output MUST NOT
leak raw enums, MUST use human-readable labels, MUST be autoescaped, MUST degrade
safely on legacy state, and MUST define empty-state behavior.

### C4-R12 — Existing `_s4` and `_s6` disposition

A new Increment 4 output is additive. `_s4` (requirements) MUST remain unchanged
and `_s6` (risk register) MUST remain unchanged during Increment 4. Overlap and
duplication between the new output and `_s4`/`_s6` are acknowledged and are
expressly NOT resolved by Increment 4. Any consolidation or migration is DEFERRED
and requires separate authorization.

### C4-R13 — Tests-first authority boundary

Tests-first work MUST NOT begin until C4-R1 through C4-R12 are committed and merged
as repository authority. Tests MUST verify ratified rulings and MUST NOT make
product decisions inside the tests. Session-surface tests are out of scope by
default; any optional session behavior requires separate authorization. Tests MUST
preserve Increment 3 and MUST preserve `_s4`/`_s6` unchanged.

## 8. Cross-ruling consistency

- One primary anchor MAY yield multiple requirements (C4-R2) with stable,
  order-independent, source-local discriminated identifiers (C4-R3).
- Criticality (C4-R4) is severed from maturity/readiness/stage/scoring/progression
  (C4-R8) and never grounded by maturity alone.
- `UNMET` does not automatically mean risk; a risk requires a grounded adverse
  consequence, with zero-to-many and many-to-one traceability (C4-R6).
- The deliverable is CORE and the session summary is OPTIONAL (C4-R11); tests-first
  excludes the session by default (C4-R13).
- `_s4` and `_s6` remain unchanged (C4-R6, C4-R12); the new section is additive
  only (C4-R11).
- Increment 3 remains closed (C4-R7); a requirement action is distinctly labeled
  and is never the global next step.
- No persistence (C4-R9) and no progression effect (C4-R8) enter indirectly.
- No requirements-management or specialist workspace is created (C4-R10).

These rulings are internally consistent with no residual conflict.

## 9. Tests-first preconditions

Before any Increment 4 tests-first work is authorized, C4-R1 through C4-R12 MUST be
committed and merged as repository authority. Tests express and verify those
ratified rulings; they do not create product decisions, do not assume the OPTIONAL
session surface, and do not modify Increment 3 or `_s4`/`_s6`.

## 10. Authority and stop boundary

This document does NOT authorize:

- design;
- implementation-contract drafting;
- tests-first work;
- source implementation;
- branch or worktree creation for implementation;
- staging;
- commit;
- push;
- PR creation;
- merge;
- persistence work;
- domain-registry work;
- an Increment 3 amendment;
- an anchor amendment.

The next governed action after this text is eventually reviewed and merged is a
separate design/readiness decision — not automatic implementation.

## 11. Owner-approval record

The owner approved the final Increment 4 ruling text after amending:

- C4-R2 (atomicity);
- C4-R4 (criticality categories and meaning);
- C4-R6 (requirement-to-risk relationship);
- C4-R11 (user-visible surfaces).

The owner approved the aligned final wording of:

- C4-R1;
- C4-R3;
- C4-R5;
- C4-R7 through C4-R10;
- C4-R12;
- C4-R13.

Status:
`OWNER-APPROVED TEXT — PENDING COMMITTED GOVERNANCE INTEGRATION`

This document is owner-approved text only. It is not active or merged repository
authority until the separate review, commit, push, PR, and true-merge
authorizations are completed.

## 12. Post-merge authority-status amendment

### 12.1 Historical-status preservation

The original status recorded near the top and bottom of this document —
`OWNER-APPROVED TEXT — PENDING COMMITTED GOVERNANCE INTEGRATION` — accurately
described this document when it was created and independently reviewed, before it was
committed and merged. That original status and the §1 / §11 non-authorization language
are preserved as historical provenance and MUST NOT be retroactively rewritten or
deleted.

### 12.2 Current authority status

Current status:

`OWNER-RATIFIED AND MERGED REPOSITORY AUTHORITY`

- PR: `#47`
- Source commit: `f2eae3eb883d9b6d5397541406733c702741feb9`
- True-merge commit: `393537aa7671b9a6e0cfbcde5a05047e5e76c842`
- Ordered parents:
  1. `2048fe8ab211117362b5c4ad3ecc4ee5cb45b2d6`
  2. `f2eae3eb883d9b6d5397541406733c702741feb9`
- Merged file SHA-256: `445e283198e60ecd057b9726948d3ff2cf52fd907d89b3d4215ee3ca6f49e1a9`

### 12.3 Authority effect

C4-R1 through C4-R13 are now binding merged repository authority for subsequent
Increment 4 decisions. This merge is governance-document-only: the product-execution
tip does NOT advance and remains `b5a8e72b26acc5ddbee355bc69b419ff09152c50` (PR #45
Increment 3 SOURCE merge); `main` remains `0e89e4636399760965c9ff8086b465c90dbadf8e`.

### 12.4 Non-authorization boundary

This merge does NOT itself authorize:

- design creation;
- implementation-contract drafting;
- tests-first work;
- source implementation;
- persistence work;
- domain expansion;
- domain-registry repair;
- a specialist workspace;
- a professional requirements-management workspace;
- an Increment 3 amendment;
- an active-anchor amendment.

Increment 3 remains closed and unmodified, and the active anchor is unchanged.

### 12.5 Next governed action

`READ-ONLY INCREMENT 4 DESIGN/READINESS ASSESSMENT`

- It is a separate owner-gated operation.
- No design artifact may be created during that assessment.
- Tests-first remains unauthorized until a separate later decision; C4-R13's
  prerequisite (C4-R1 through C4-R12 committed and merged) is now satisfied, but that
  satisfaction does NOT automatically authorize tests-first work.
- The product-execution tip remains `b5a8e72b26acc5ddbee355bc69b419ff09152c50`.
