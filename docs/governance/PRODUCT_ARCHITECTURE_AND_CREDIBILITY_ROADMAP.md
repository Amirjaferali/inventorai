# PRODUCT ARCHITECTURE AND CREDIBILITY ROADMAP
# Strategic sequencing and preservation document — NOT an execution authority

Current status:
ACTIVE STRATEGIC COORDINATION — NON-AUTHORIZING

Document role:
Committed non-authorizing strategic sequencing and preservation roadmap

Admission basis:
Explicit owner admission decision issued after initial commit, push,
and remote verification. This status is repository-effective only upon
commit, push, and remote verification of this status-activation amendment.

Authority boundary:
This roadmap coordinates strategic direction and sequencing only.
It does not authorize product implementation, activate any P0–P6 item,
override an active anchor, alter blocked or held states, or bind itself
into the mandatory reading order.
Level 3 classification:
Upon commit, push, and remote verification of this status-activation
amendment, this roadmap satisfies the Level 3 classification defined in
`STRATEGIC_PRODUCT_VISION.md` §12 as a committed governance artifact
with ACTIVE status.

This Level 3 classification does not expand the roadmap’s authority.
Its role remains limited to non-authorizing strategic coordination,
subject to the Authority boundary stated above.

---

## AUTHORITY DISCLAIMER (READ FIRST)

This roadmap is a strategic sequencing and preservation document.
Its inclusion of an item does not authorize implementation, repository
modification, execution, state movement, or a new active lane.

`ACTIVE_EXECUTION_ROADMAP.md` remains the sole authority for current execution
lanes, holds, blocked states, and authorized next actions.

This document creates no execution phase, no hold change, no authorization,
and no implementation right. Every item below requires its own separate,
future, explicit owner authorization before any working-tree write may occur.

---

## A. PURPOSE AND SCOPE

This document exists to preserve product-architecture and credibility
priorities discovered during strategic and technical assessment sessions,
so that this analysis is not lost or re-derived from scratch by a future
agent, and so that previously resolved questions are not reopened
unnecessarily.

**FACT:** The platform's primary product objective, as recorded in
`docs/governance/STRATEGIC_PRODUCT_VISION.md` §1–§3, is the progression and
development of the inventor's idea — not inventor development as the
platform's primary identity claim. `STRATEGIC_PRODUCT_VISION.md` §1 and §3
are themselves under an active Level 0 amendment
(`docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md`); this document does
not restate or reinterpret that amendment, and any future agent must read
the amendment directly rather than relying on this summary.

This roadmap does not redefine product identity. It sequences future
architecture and credibility work that has been identified but not yet
authorized.

This roadmap's P0–P5 sequencing is intended to support, without
authorizing or implementing, the owner's broader product direction:
Path N as the current non-technical idea-orchestration path; Path T
as a future specialist workspace that remains blocked; coordination
of one invention across multiple technical domains; honest disclosure
of platform capability boundaries; supported assembly, synthesis,
execution, or simulation only where actual platform capability
exists; specialist handoff where platform capability ends; and
user/project continuity and scalability as separately governed future
architecture areas. None of these directions is authorized,
implemented, or assumed to currently exist by virtue of this
statement.

---

## B. AUTHORITY SEPARATION

Five distinct authority layers exist in this repository. They must not be
conflated:

1. **Current execution authority** — `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`,
   read together with the mandatory reading order defined in `CLAUDE.md`
   §"Current Repository Execution Authority". This is the only document
   that defines what is currently authorized.

2. **Product-architecture sequencing** — this document. Strategic ordering
   only. No authorization.

3. **Historical replay-stabilization evidence** — the older
   "InventorAI — Refactor Governance Contract" section of `CLAUDE.md`,
   `benchmark/run_benchmark_v1.py`, `scripts/run_replay_benchmark_v2.py`,
   `docs/GOVERNANCE_DOCUMENTS.md`, `docs/WORKFLOW_PROTECTION_STANDARD.md`,
   and `tests/replay/cases/*.json`. **FACT:** `CLAUDE.md` itself states that
   its first section ("Current Repository Execution Authority") overrides
   "any older current-priority, active-document, or document-authority
   statement in this file when they conflict."

   The older replay-governance artifacts are not current execution-lane
   authority. Their historical phase sequence, replay priority, and migration
   status do not authorize current work.

   Non-conflicting engineering-integrity constraints contained in those
   artifacts remain repository context unless explicitly superseded by a
   later authority. This roadmap does not categorize all P-01 through P-10
   principles in `docs/GOVERNANCE_DOCUMENTS.md` as obsolete, cancelled, or
   inactive; it states only that they do not constitute current
   execution-lane authority.

4. **Future governance specifications** — not yet committed. Includes any
   eventual Source/Claim/Recommendation contract, Stage 3 audit findings,
   or domain-adapter specifications.

5. **Product implementation authorizations** — separate, narrow, explicit
   owner authorizations for working-tree writes. This roadmap is not one.

**EXPLICIT CLARIFICATION (FACT):** The phase numbering "Phase 5 / Phase 6"
in `docs/GOVERNANCE_DOCUMENTS.md` (`P-10: Phase Order Enforcement. Phase 6
cannot start until Phase 5 approved`, referring to a domain-registry
migration: "Phase 4 to 5: Governance documents committed", "Phase 5 to 6:
Migration Plan approved by owner", "Phase 6 to 7: Registry passes 23/23
parity", "Phase 7 to 8: Second domain added and tested") is a **different
numbering sequence** from "Phase 5" / "Phase 6" as used in
`docs/governance/ACTIVE_EXECUTION_ROADMAP.md` (Path N Phase 5/Phase 6,
currently UNAUTHORIZED). These two sequences must never be conflated by any
future agent. Neither numbering authorizes the other.

---

## C. CURRENT VERIFIED BASELINE

```text
HEAD = origin/main = f5adaf4a8593347f0c26e4c655866eade8912071
```

**FACT — completed and remotely verified product-facing capabilities at this
baseline:**

- FDC-001 web deliverable exposure (`GET /session/<sid>/deliverable`,
  `web/templates/deliverable.html`).
- In-progress assessment snapshot vs eligible-deliverable language
  distinction on the session and deliverable pages.
- Acknowledged Unknowns Visibility on the session page
  (`web/templates/session.html`, reading `state.acknowledged_unknowns`).

**FACT:** No new product-execution lane is currently active. Any further
product implementation requires a separate, explicit, repository-grounded
owner authorization, per `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` §7.

---

## D. PRIORITY ROADMAP

### P0 — Roadmap preservation and authority clarity

- Preserve the current/historical authority distinction recorded in
  Section B above.
- Prevent agent reset: future agents must read this document before
  proposing new product architecture, in addition to (not instead of)
  the mandatory `CLAUDE.md` reading order.
- Prevent phase-number conflation between the historical replay-governance
  sequence and the active Path N sequence.
- Preserve repository-first rules: no claim in this document substitutes
  for direct repository inspection by a future agent.

### P1 — Source, Provenance, Licensing, and Claim Architecture

```text
GOVERNANCE PREPARATION REQUIRED
IMPLEMENTATION NOT AUTHORIZED
```

**INTERPRETATION (from prior read-only audit):** The repository currently
has no implemented Source Record, Claim Record, or Recommendation Record.
`engine/idea_state.py` `Evidence` carries only `content`, `quality`, and
`iteration` — no source-type or provenance field. `engine/deliverable_assembler.py`
contains no source-backed field. This is an absence, not a defect; no prior
authorization required these fields to exist.

Required future contracts (not yet specified in detail, not yet authorized):

- Source Record (fields under consideration: source_id, title, publisher,
  source_type, location, published_at, accessed_at, version, domain,
  jurisdiction, license_status, attribution_required, redistribution_status,
  quotation_limit, freshness_status, verification_status, usage_limitations).
- Claim Record (fields under consideration: claim_id, claim_text,
  claim_origin, source_ids, confidence, limitations, domain, created_at,
  review_status).
- Recommendation Record (fields under consideration: recommendation_id,
  recommendation_text, supporting_claim_ids, advisory_status,
  requires_specialist_review, prohibited_readiness_claims).
- License classification, attribution rules, quotation/summarization
  limits, freshness/versioning, conflicting-source handling, jurisdiction
  separation, source correction/removal, and a source audit trail.

**RECOMMENDATION (not yet approved):**

```text
Independent core Source & Evidence layer
linked by IDs
plus domain-specific adapters.
```

**Binding constraints any future P1 specification must satisfy, stated
explicitly per owner instruction:**

- External sources must never automatically advance maturity.
- External sources must never automatically close gaps.
- External facts must never be presented as inventor-demonstrated reasoning.
- Source presence must not imply feasibility, safety, compliance, patent
  validity, or readiness.

These constraints derive directly from `STRATEGIC_PRODUCT_VISION.md` §1
("AI is advisory only — it cannot gate, classify, score, or advance
state") and Principle 1 ("Inventor Ownership") and Principle 2
("Improvement, Not Generation"), applied by extension to any future
external-source mechanism.

### P2 — Stage 3 Runtime and Authority Audit

```text
STATIC AUDIT COMPLETED — FINDINGS CLASSIFIED
IMPLEMENTATION NOT AUTHORIZED
```

**AUDIT COMPLETED BY DIRECT REPOSITORY READ — the prior uncertainty has
been classified. This entry is documentary and non-authorizing; it does
not activate P2 implementation, any other P0–P6 item, or any held,
blocked, or unauthorized state.**

* `STAGE3_GAP_PRIORITY` and Stage 3 questions
  (`PROBLEM_MECHANISM_FIT`, `ASSUMPTION_INVENTORY`,
  `EXPERTISE_GAP_AWARENESS`) are present in committed code and are
  selected by `run_iteration()` once `state.current_stage == 3`.
* `state.current_stage` is set to `3` automatically inside
  `run_iteration()` when `maturity_level` reaches `2`, in the same
  conditional in both occurrences within `engine/progression_loop.py`.
* `web/templates/session.html` displays a progress label derived from
  `state.maturity_level`, not from `state.current_stage`. Direct
  inspection of `web/app.py`, `engine/progression_loop.py`, and
  `engine/stage3_evaluator.py` identified no reachable numeric divergence
  between these two fields across the currently committed execution
  paths inspected by this audit.
* `engine/stage3_evaluator.py` is confirmed absent from any committed
  production import or call path (`web/app.py`, `engine/progression_loop.py`).
  Its own module docstring states that its observations are advisory only,
  pending a separate human-review authorization layer
  (`TRANSITION_AUTHORIZATION_GOVERNANCE` OA-1). Its current non-integration
  is therefore consistent with an intentional deferred design and is not
  a confirmed defect. This finding does not authorize future integration;
  integration remains a separate, future, explicit owner decision.
* The previously unconfirmed Stage 3 dedicated-label presentation gap
  was independently confirmed and corrected at commit
  `7605e46bde6b96887b62bc44283ae8a682338e4d` (`web/gap_labels.py`,
  `tests/test_gap_labels.py`, 10 passing tests). This commit reference
  applies only to that dedicated gap-label mapping and its narrow
  mapping tests; it does not certify, correct, or authorize anything
  else referenced in this section.
* Direct rendered-template or Flask-route regression coverage for
  Stage 3 runtime-to-UI consistency remains absent. This is a recorded
  test-coverage gap, not evidence of a live product failure.
* The duplicated Stage 3 transition-advancement condition across two
  locations in `engine/progression_loop.py` remains an unresolved
  architectural drift risk. No refactoring of this logic is authorized
  by this entry.
* No live session was created and no observed live product failure was
  established under this audit. All findings above are based on static
  repository inspection only.

### P3 — Specialist Questions Section

```text
DEFERRED PENDING P1 GOVERNANCE DEFINITION
MAY LATER PROCEED AS USER-DATA-ONLY
```

Allowed future initial inputs (all already present as committed,
user-originated data):

- User assertions (`state.known_problem`, `state.known_mechanism`).
- Acknowledged unknowns (`state.acknowledged_unknowns`).
- Open gaps (`state.gaps` with `status == OPEN`).

Prohibited until P1 implementation and approval:

- External-source facts.
- Component recommendations.
- Feasibility claims.
- Standards claims.
- Safety claims.
- Regulatory claims.

### P4 — Source-backed Technical Recommendations

```text
BLOCKED UNTIL P1 GOVERNANCE AND TECHNICAL IMPLEMENTATION
```

Examples of recommendations that require P1 before they may be produced
by the platform:

- Components.
- Sensors.
- Voltage/current requirements.
- Materials.
- Communications protocols.
- Energy calculations.
- Standards references.
- Regulatory references.
- Simulation inputs.

### P5 — Cross-domain Expansion

```text
SEQUENCED AFTER CORE PROVENANCE CONTRACT
```

Recommended sequence (RECOMMENDATION — not yet approved):

1. Core provenance contract.
2. Electronics/electrical adapter.
3. Validation.
4. IoT adapter.
5. Validation.
6. Mechanical adapter.
7. Validation.
8. Drone/UAS adapter with jurisdiction separation.
9. Further domains.

### P6 — Known Defect Register

Recorded without fixing. Each entry: evidence path, risk, user-facing
status, governance sensitivity, smallest future correction type. No
implementation authorization is granted by this section.

1. **Misleading completeness label**
   - Evidence: `engine/deliverable_assembler.py`, function `_completeness()`,
     string literal `"COMPLETE — eligible for Phase 5 deliverable"`.
   - Risk: Implies an official "Phase 5" governance state that does not
     exist in the active Path N phase sequence; may confuse a reader into
     believing a governance phase transition occurred.
   - User-facing: Yes (rendered in `web/templates/deliverable.html` via
     `package.section_2_invention_summary.assessment_completeness`).
   - Governance-sensitive: Moderate.
   - Smallest future correction: Single-string text edit in
     `engine/deliverable_assembler.py`; no schema or test-contract change
     expected, but exact test coverage was not confirmed during drafting.
   - No implementation authorized here.

2. **Internal raw `gap_context` value in user-facing unknown display**
   - Evidence: `web/templates/session.html`, Acknowledged Unknowns section,
     `{{ u.gap_context }}` rendered directly (e.g. `MECHANISM_COMPLETENESS`)
     instead of a `GAP_LABELS`-translated heading.
   - Risk: Cosmetic only; reduces readability for a non-specialist user.
   - User-facing: Yes.
   - Governance-sensitive: No.
   - Smallest future correction: Single-line template change to use
     `GAP_LABELS.get(u.gap_context, GAP_LABELS["__default__"]).heading`.
   - No implementation authorized here.

3. **Stage 3 / UI presentation — audit completed**
   - Evidence: See P2 above for the complete classified findings.
   - Status: No confirmed numeric runtime/UI mismatch. The previously
     unconfirmed dedicated Stage 3 label gap was confirmed and corrected
     at commit `7605e46bde6b96887b62bc44283ae8a682338e4d`.
   - Remaining risk: Architectural duplication in the Stage 3 transition
     condition and absence of rendered-UI regression coverage both remain
     unresolved and were not corrected by that commit or by this entry.
   - User-facing: The corrected gap affected user-facing label content in
     committed code; no observed live user-facing failure was established.
     The remaining architectural and coverage risks have not been shown
     to produce a current user-facing failure.
   - Governance-sensitive: The completed label correction is narrow and
     non-authorizing. The remaining risks require separate assessment
     before any implementation decision.
   - Potential future follow-up: Rendered-template regression coverage and
     consolidation of the duplicated transition condition must be assessed
     separately and would each require explicit future owner authorization.
   - No implementation authorized here.

4. **Normal sessions writing to an ILT-002-named transcript path**
   - Evidence: `web/app.py`, function `submit_answer()`, variable
     `transcript_path = f"/tmp/ilt002_transcript_{sid}.jsonl"`, written
     unconditionally for every session including non-ILT-002 sessions
     started via `/start`.
   - Risk: Misleading naming; a normal user's session data is written to a
     path named after the ILT-002 evidence-collection mechanism, even
     though this write is unconditional and not itself new evidence
     collection authorization.
   - User-facing: No (disk path, not rendered to the user).
   - Governance-sensitive: Moderate — naming could mislead a future agent
     into believing this write is part of an active ILT-002 evidence
     campaign rather than a pre-existing, unconditional engineering
     behavior inherited from earlier work.
   - Smallest future correction: Not determined here; any correction
     touching this behavior requires its own separate, careful
     authorization given its proximity to ILT-002 governance, and is
     explicitly out of scope for this roadmap.
   - No implementation authorized here.

5. **Historical/current phase-number ambiguity**
   - Evidence: See Section B above (`docs/GOVERNANCE_DOCUMENTS.md` P-10 vs
     `ACTIVE_EXECUTION_ROADMAP.md` Path N Phase 5/6).
   - Risk: A future agent could conflate the two sequences and
     misclassify an old historical gate as relevant to current
     authorization.
   - User-facing: No.
   - Governance-sensitive: Yes.
   - Smallest future correction: None required; this roadmap's Section B
     documents the distinction. No file requires modification to resolve
     this ambiguity going forward, provided future agents read Section B.

---

## E. DEPENDENCY MAP

```text
P0 precedes all governed architecture work.

After P0:
- P1 governance preparation and the P2 read-only audit may proceed
  independently under separate authorizations.
- P1 governance precedes P3 user-data-only discovery.
- P1 governance plus P1 technical implementation precede P4.
- The P1 core contract precedes P5 domain expansion.
- P6 corrections remain separate narrow actions.
```

**CLARIFICATION:** P2 does not depend on P1 completion. P2 must not be
combined with P1 in one authorization or one working-tree change.

---

## F. ARCHITECTURE DECISION DIRECTION

```text
Option D — Hybrid
Independent source/provenance core
+
domain-specific source adapters
+
ID-based linkage to claims and recommendations
+
no automatic effect on deterministic progression.
```

```text
RECOMMENDED DIRECTION — NOT YET APPROVED AS FINAL SPECIFICATION
```

This direction was selected, during prior read-only assessment, over three
alternatives (embedded fields directly in `IdeaState`/FDC-001; an
independent layer with no domain adapters; domain-pack-owned registries
with no shared core) primarily because it satisfies `CLAUDE.md`
"Adapter Rules" ("Compatibility adapters are allowed ONLY for: legacy
field aliases, structural compatibility, schema bridging. Adapters must
NEVER alter semantic meaning.") without requiring any modification to
`engine/idea_state.py` or `engine/progression_loop.py`'s deterministic
transition logic.

---

## G. PRESERVED PRODUCT BOUNDARIES

```text
R2 = HELD
FORM T = BLOCKED
Path T = BLOCKED
  Preserved strategic direction: a future specialist technical
  workspace, not an active execution lane.
S-6 = UNCLASSIFIED
AA-3 = BLOCKED
AA-4 = BLOCKED
AA-5 = BLOCKED
Phase 5 = UNAUTHORIZED
Phase 6 = UNAUTHORIZED
ILT-002 evidence collection = NOT AUTHORIZED
AA-4 final S-6 classification = NOT PERFORMED
```

These statuses are recorded here for continuity only. The authoritative
source for these statuses at any future point in time remains
`docs/governance/ACTIVE_EXECUTION_ROADMAP.md`, not this document.

---

## H. AGENT HANDOVER PROTOCOL

Every future agent working on product architecture must:

1. Read current execution authority first — the `CLAUDE.md` mandatory
   reading order ending with `ACTIVE_EXECUTION_ROADMAP.md`.
2. Read this roadmap before proposing new product architecture.
3. Distinguish historical replay artifacts (Section B item 3) from active
   product architecture (Section B items 1, 2, 4, 5).
4. Not infer authorization from the mere presence of an item in this
   roadmap's priority ordering.
5. Not implement a later priority (e.g. P4) before its stated dependency
   (e.g. P1) is separately authorized and implemented.
6. Report roadmap staleness to the owner if a relevant architecture
   decision is committed after this document's last update and is not
   yet reflected here.

Until this roadmap is separately added to a mandatory repository reading
index, agents discovering it through governance inventory must treat it as
the active, non-authorizing product-architecture sequencing and
preservation record.

Binding this roadmap into a mandatory reading index requires a separate
authorization and is not authorized by this document.

```text
Mandatory-reading discoverability binding:
PENDING SEPARATE AUTHORIZATION
```

---

## I. ROADMAP UPDATE RULE

This roadmap must be updated when:

- A source architecture specification (P1) is approved.
- A source contract (P1) is implemented.
- A Stage 3 audit (P2) is completed.
- Specialist Questions (P3) is authorized or implemented.
- A domain adapter (P5) is authorized or implemented.
- A listed defect (P6) is resolved.
- A new cross-domain architecture decision is approved.

A roadmap-only commit does not itself make this roadmap stale.

---

## J. PLANNED ANCHOR COMPANION

Planned Anchor Companion intent:
RECORDED IN THIS ROADMAP BEFORE ADMISSION

This document records, in advance of admission, the owner's intent
that this roadmap may later become a mandatory strategic reading
companion. Recording this intent here is not itself a mandatory-
reading binding and does not place this document in any current
reading order.

Mandatory reading-order repository binding:
PENDING A LATER SEPARATE AUTHORIZATION

This document does not replace, amend, or override any active
anchor. `ACTIVE_EXECUTION_ROADMAP.md`, `DUAL_PATH_PRODUCT_ANCHOR.md`,
`ILT-002_GOVERNANCE_ANCHOR.md`, `OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
and any applicable phase-specific authorization remain fully
controlling for execution authority, permissions, holds, and blocked
states.

If and when mandatory-reading binding occurs, it is expected to occur
through a future addition to the mandatory reading order in
`CLAUDE.md`, unless later repository evidence demonstrates a better
mechanism. This expectation is not authorization to edit `CLAUDE.md`
now. A new anchor document must not be created to carry this binding
unless an independently demonstrated need is shown.

---

*This document is a sequencing and preservation artifact only.*
*It authorizes nothing. `ACTIVE_EXECUTION_ROADMAP.md` remains the sole*
*authority for current execution lanes, holds, and authorized next actions.*
