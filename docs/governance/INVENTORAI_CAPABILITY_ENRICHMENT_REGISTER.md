# InventorAI Capability Enrichment Register

**Record type:** canonical, cross-cutting **capability enrichment register**.
**Status:** governance-documentation only — **NON-ACTIVATING and NON-AUTHORIZING**. Recording (and
merging) this register **implements nothing** and **authorizes nothing**. Prepared under the risk-based
execution and review model (PR #220), on authoritative tip `2775242c415cd9f26947a454938900a1b5b303ec`
(Merge PR #265; Workstream 11 formally closed).

**Purpose.** Preserve the owner-approved InventorAI enrichment concepts across agents and future
workstreams, define their boundaries and intended sequencing, and prevent either accidental omission or
premature implementation. This register is a durable inventory; it is subordinate to the committed
anchors, `ACTIVE_EXECUTION_ROADMAP.md`, `DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md`, and every
committed increment contract and owner decision. Where this register and any committed authority
conflict, the committed authority controls.

**Authority boundary (binding).** This register creates no active lane, implementation authority,
technical-selection authority, artifact-generation authority, verification claim, RED/GREEN
authorization, persistence authorization, or status change. It does not start, activate, or resume any
Workstream. It does not amend, override, or reinterpret any anchor, roadmap, contract, owner decision,
or protected boundary. Registration is **not** implementation authorization (see §R5).

**Relationship to existing authorities (evidence).** The following committed records already govern
capabilities that overlap this register; those records — not this register — remain authoritative for
their capabilities:
- **Structured Technical Guidance** is the existing **D13** capability ("Mandatory Future Technical
  Capability Gap Detection and Actionable Research Guidance"; `ACTIONABLE_VALIDATION_PLAN_INCREMENT_
  CONTRACT.md` §4 D13; `D13_FORMAL_CLOSURE_RECORD.md` and the `D13_*` records). CAP-01 defers to D13.
- **Patent Export** is governed by `STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md`
  (non-activating owner decision, associated with PR #229). CAP-06's patent-disclosure-readiness axis
  and any patent capability defer to it.
- **WS-PFV-001 — Prototype Feasibility and Validation** is governed by
  `PROTOTYPE_FEASIBILITY_AND_VALIDATION_FUTURE_WORKSTREAM_OWNER_DECISION.md` (non-activating future
  workstream reservation, associated with PR #227). CAP-09 defers to it.
- **Workstreams 12–17** are defined in `DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §15 (WS12
  Controlled Unknown Progression; WS13 Guided Answer Support; WS14 Adaptive Follow-Up and Completion
  Logic; WS15 Guidance Consolidation; WS16 Final Deliverable Completion and full end-to-end owner
  validation (Gate); WS17 AI Coach (Post-gate)).

No existing canonical capability register enumerates these eleven concepts; this record does not
duplicate or conflict with any existing authority.

---

## 1. Capability entries

All eleven capabilities share the initial status **`RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`** and
require **separate explicit owner authorization** before any implementation (see §R5/§R6).

### CAP-01 — Structured Technical Guidance
- **Product problem:** users hit technical subproblems the system cannot answer, and generic "consult a
  specialist" is not actionable.
- **User value:** a precise, honest map of the unresolved technical gap and how to close it.
- **Intended behavior:** identify the exact unresolved technical subproblem, the missing technical
  information, the exact research topic and suggested search terms, required measurements/tests/
  documents, what the system can and cannot verify, risk and uncertainty, and the appropriate specialist
  category only when necessary and evidence-supported.
- **Non-goals:** must not invent a technical answer, perform engineering execution, silently close a
  gap, or replace professional judgment.
- **Dependencies/prerequisites:** the committed **D13** capability and its governed knowledge sources;
  D13 Source Review outcomes.
- **Proposed workstream / activation gate:** **D13** (separately owner-gated). CAP-01 *is* the
  user-facing D13 capability and does not create a parallel authority.
- **Overlap risks:** WS-PFV-001 (validation framework); CAP-04 Gap Action Packs; CAP-09 Experiment
  Designer; AI Coach.
- **Protected boundaries:** must never be described as satisfied by generic referral; D13 status language
  (`MANDATORY FUTURE PRODUCT CAPABILITY — NOT CANCELLED — NOT SATISFIED BY GENERIC SPECIALIST REFERRAL —
  SEPARATELY OWNER-GATED`) governs.
- **Proposed acceptance criteria:** deterministic gap identification with full provenance from the
  recorded requirement; no invented competence/tools/standards; explicit abstention where unsupported.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION` (governed by D13).
- **Activation conditions:** the D13 Source Review and D13 owner-gated authorization chain.
- **Separate owner authorization requirement:** yes — via the D13 authority.

### CAP-02 — Simplified One-Step Journey Presentation
- **Product problem:** the internal governance model is too complex for a lay inventor to navigate.
- **User value:** a calm, legible journey.
- **Intended behavior:** present the user-facing journey through four simple concepts — what is known,
  what is unknown, why it matters, and the single next action.
- **Non-goals:** internal governance and deterministic gates remain intact and must not be weakened or
  bypassed by the simplified surface.
- **Dependencies/prerequisites:** committed state (gaps, unknowns, transitions); WS8 Journey Reordering
  and Intent Alignment; WS12 unknown states; CAP-04.
- **Proposed workstream / activation gate:** presentation layer aligned with **WS8** / a later UX gate.
- **Overlap risks:** CAP-06 dashboard; CAP-07 decision room; AI Coach.
- **Protected boundaries:** must not collapse or hide deterministic gate outcomes; no scoring/transition
  change.
- **Proposed acceptance criteria:** the four concepts derive deterministically from canonical records;
  no invented "next action"; gates unchanged.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Activation conditions:** a separately authorized presentation/UX increment.
- **Separate owner authorization requirement:** yes.

### CAP-03 — Adaptive Assistance by User Expertise
- **Product problem:** non-technical users need scaffolding; technical users are slowed by unnecessary
  intervention.
- **User value:** right-sized assistance.
- **Intended behavior:** provide more explanation/structure for non-technical users while minimizing
  unnecessary intervention for users who provide technically sufficient answers.
- **Non-goals:** must not rely on permanent self-declared expert status alone; safety, integrity,
  evidence, and deterministic sufficiency boundaries remain applicable to every user; must not
  reinterpret expertise as an unknown.
- **Dependencies/prerequisites:** deterministic sufficiency (`assess_response`); WS12 (no
  expertise→unknown reinterpretation); WS13/WS14.
- **Proposed workstream / activation gate:** **WS13 / WS14** family (guided answer / adaptive
  follow-up).
- **Overlap risks:** WS13, WS14, AI Coach, CAP-02.
- **Protected boundaries:** existing deterministic sufficiency/safety/evidence gates apply to every
  user; no per-user gate relaxation.
- **Proposed acceptance criteria:** adaptation is deterministic and never lowers a safety/evidence
  boundary; expert status never overrides sufficiency.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Activation conditions:** WS13/WS14 owner authorization.
- **Separate owner authorization requirement:** yes.

### CAP-04 — Gap Action Packs
- **Product problem:** an unresolved gap is not actionable to the user.
- **User value:** a concrete external-work package to close a gap.
- **Intended behavior:** convert an unresolved gap into an actionable external-work package containing
  the required action, the reason it is required, how to obtain the information, the acceptable result,
  and what becomes possible after completion.
- **Non-goals:** must not perform the external work, fabricate results, or treat the action pack as
  evidence.
- **Dependencies/prerequisites:** WS12 closure paths; D13 (technical action packs); the gap/blocker
  model.
- **Proposed workstream / activation gate:** **WS12** (closure paths) with D13 for technical content.
- **Overlap risks:** CAP-01, CAP-09, WS13.
- **Protected boundaries:** an action pack is never Evidence and never closes a gap; no fabricated
  result.
- **Proposed acceptance criteria:** deterministically derived from a recorded gap/closure path; no
  invented facts; not counted as evidence.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Activation conditions:** WS12 (and D13 where technical) owner authorization.
- **Separate owner authorization requirement:** yes.

### CAP-05 — Decision Trace
- **Product problem:** decisions are opaque; users cannot see what supports them.
- **User value:** transparent, auditable decisions.
- **Intended behavior:** for each important decision, expose the decision, supporting evidence,
  assumptions, unresolved information, confidence/uncertainty basis, and what could change the decision.
- **Non-goals:** must not create false numerical precision or replace the canonical evidence record.
- **Dependencies/prerequisites:** the decision-workspace (FDC-001) model; the Increment-2 evidence/
  provenance axes; CAP-08 assumptions; CAP-11 evidence ladder.
- **Proposed workstream / activation gate:** decision-support increment aligned with the decision
  workspace.
- **Overlap risks:** CAP-07 decision room; CAP-08; CAP-11.
- **Protected boundaries:** traceable to canonical records; no fabricated confidence numbers.
- **Proposed acceptance criteria:** every element cites a canonical record; uncertainty is qualitative
  unless a separately authorized quantitative basis exists.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Activation conditions:** a separately authorized decision-support increment.
- **Separate owner authorization requirement:** yes.

### CAP-06 — Multi-Axis Invention Readiness Dashboard
- **Product problem:** a single readiness score misleads.
- **User value:** honest, multi-dimensional readiness.
- **Intended behavior:** provide separate readiness views for problem clarity, mechanism completeness,
  physical feasibility, evidence strength, assumption integrity, testability, prototype readiness, and
  patent-disclosure readiness.
- **Non-goals:** must not collapse these dimensions into a misleading single score unless separately
  authorized and justified.
- **Dependencies/prerequisites:** committed gap/evidence/criticality state; CAP-11 (evidence strength);
  Patent Export decision (patent-disclosure readiness); WS-PFV-001 (prototype readiness).
- **Proposed workstream / activation gate:** a readiness-presentation increment; patent-disclosure axis
  defers to the Patent Export decision; prototype axis defers to WS-PFV-001.
- **Overlap risks:** CAP-02, CAP-07, CAP-11, Patent Export, WS-PFV-001.
- **Protected boundaries:** no misleading single score; each axis is independently derived from canonical
  records.
- **Proposed acceptance criteria:** each axis is deterministic and separately sourced; no hidden
  weighting.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Activation conditions:** a separately authorized dashboard increment (with Patent Export / WS-PFV-001
  for the respective axes).
- **Separate owner authorization requirement:** yes.

### CAP-07 — Invention Decision Room
- **Product problem:** no consolidated final decision workspace exists for the inventor.
- **User value:** one place to make the go/no-go and next-step decisions.
- **Intended behavior:** a consolidated final decision workspace containing proven items, unresolved
  unknowns, risks, provisional decisions, accepted decisions, next action, and required tests/documents/
  specialists.
- **Non-goals:** must remain traceable to canonical records and must not independently alter state or
  evidence.
- **Dependencies/prerequisites:** decision-workspace (FDC-001); WS12 unknowns; CAP-05; CAP-08; CAP-10.
- **Proposed workstream / activation gate:** aligned with **WS16** final-deliverable/decision
  consolidation or a decision-support increment.
- **Overlap risks:** CAP-02, CAP-05, CAP-06, CAP-08, CAP-10; AI Coach.
- **Protected boundaries:** read-only over canonical records; no independent state/evidence mutation.
- **Proposed acceptance criteria:** every item traces to a canonical record; no state mutation.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Activation conditions:** a separately authorized consolidation increment.
- **Separate owner authorization requirement:** yes.

### CAP-08 — Assumption Register
- **Product problem:** material assumptions are untracked and can masquerade as facts.
- **User value:** disciplined assumption tracking to resolution.
- **Intended behavior:** record each material assumption with identity, source, affected decision/gap,
  impact, risk, review status, evidence required to confirm/reject it, and supersession/closure history.
- **Non-goals:** an assumption must never be presented as verified evidence.
- **Dependencies/prerequisites:** the Increment-2 provenance/validation axes and the append-only ledger
  (supersession/contradiction); WS12; CAP-11.
- **Proposed workstream / activation gate:** an assumption-tracking increment (leveraging the existing
  ledger).
- **Overlap risks:** CAP-05, CAP-07, CAP-10, CAP-11; WS12.
- **Protected boundaries:** assumptions are never Evidence; append-only, non-destructive history.
- **Proposed acceptance criteria:** deterministic; assumptions never auto-promote to evidence; full
  provenance and supersession history.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Activation conditions:** a separately authorized assumption-register increment.
- **Separate owner authorization requirement:** yes.

### CAP-09 — Experiment Designer
- **Product problem:** inventors lack a structured way to plan validation experiments.
- **User value:** a rigorous, honest experiment plan.
- **Intended behavior:** create a structured experiment plan containing hypothesis, variable,
  measurement method, success criterion, failure criterion, risks, and required result.
- **Non-goals:** must not claim scientific validity, execute simulations or tests, fabricate results, or
  replace specialist review.
- **Dependencies/prerequisites:** **WS-PFV-001** (Prototype Feasibility and Validation); the existing
  `SuccessCriterion` planning-metadata precedent.
- **Proposed workstream / activation gate:** **WS-PFV-001** (separately owner-gated future workstream).
- **Overlap risks:** CAP-01, CAP-04, CAP-06 (prototype readiness); D13.
- **Protected boundaries:** planning metadata only; never a result; never graded; never executed.
- **Proposed acceptance criteria:** deterministic structure; explicit non-execution and non-validity
  disclaimers; specialist review preserved.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION` (governed by
  WS-PFV-001).
- **Activation conditions:** the WS-PFV-001 activation chain.
- **Separate owner authorization requirement:** yes — via WS-PFV-001.

### CAP-10 — Contradiction Detector
- **Product problem:** conflicting statements/constraints/assumptions/evidence go unnoticed.
- **User value:** early, deterministic surfacing of contradictions.
- **Intended behavior:** identify deterministic contradictions across user statements, constraints,
  assumptions, specifications, and evidence.
- **Non-goals:** must report the contradiction and its provenance without silently selecting a preferred
  answer or solution.
- **Dependencies/prerequisites:** the append-only ledger's `mark_contradiction` /
  `has_unresolved_contradiction`; decision-workspace `UNRESOLVED_EVIDENCE_CONFLICT`; CAP-08.
- **Proposed workstream / activation gate:** a contradiction-detection increment (leveraging the
  existing contradiction graph).
- **Overlap risks:** CAP-05, CAP-07, CAP-08; WS12.
- **Protected boundaries:** report-only with provenance; never auto-resolve or pick a winner.
- **Proposed acceptance criteria:** deterministic contradiction detection with provenance; no silent
  resolution.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Activation conditions:** a separately authorized contradiction-detection increment.
- **Separate owner authorization requirement:** yes.

### CAP-11 — Evidence Quality Ladder
- **Product problem:** evidence of very different strength is treated alike.
- **User value:** an honest hierarchy of evidence provenance and strength.
- **Intended behavior:** classify evidence provenance and strength using a controlled hierarchy such as
  opinion → assumption → calculation → manufacturer specification → test result → prototype evidence →
  independent verification.
- **Non-goals:** the final vocabulary and semantics require a separate contract and must not be
  implemented from this register alone.
- **Dependencies/prerequisites:** the committed Increment-2 provenance (`LEGACY_UNSPECIFIED /
  OWNER_STATED / SYSTEM_INFERRED / EXPERT_SUPPLIED / EXTERNAL_EVIDENCE`) and validation
  (`UNVALIDATED / SPECIALIST_REVIEWED / EMPIRICALLY_DEMONSTRATED / INDEPENDENTLY_VERIFIED`) axes; a
  separate owner-approved ladder contract.
- **Proposed workstream / activation gate:** a dedicated evidence-quality contract (separate).
- **Overlap risks:** CAP-05, CAP-06 (evidence strength axis), CAP-08.
- **Protected boundaries:** must not silently redefine the committed provenance/validation axes; no
  auto-promotion; final semantics require a separate contract.
- **Proposed acceptance criteria:** deterministic mapping from committed axes; no inference from text; a
  ratified ladder contract before implementation.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Activation conditions:** a separately authorized evidence-quality-ladder contract.
- **Separate owner authorization requirement:** yes.

---

## 2. Capability-to-Workstream activation matrix

| Capability | Primary activation gate / authority | Also spans | Current status |
|---|---|---|---|
| CAP-01 Structured Technical Guidance | **D13** (owner-gated) | WS-PFV-001, CAP-04, CAP-09 | RECORDED — NOT AUTHORIZED |
| CAP-02 Simplified One-Step Journey | WS8 / later UX increment | CAP-06, CAP-07 | RECORDED — NOT AUTHORIZED |
| CAP-03 Adaptive Assistance | WS13 / WS14 | CAP-02, AI Coach | RECORDED — NOT AUTHORIZED |
| CAP-04 Gap Action Packs | WS12 (+ D13 for technical) | CAP-01, CAP-09 | RECORDED — NOT AUTHORIZED |
| CAP-05 Decision Trace | Decision-support increment | CAP-07, CAP-08, CAP-11 | RECORDED — NOT AUTHORIZED |
| CAP-06 Readiness Dashboard | Readiness increment (+ Patent Export, WS-PFV-001 axes) | CAP-02, CAP-07, CAP-11 | RECORDED — NOT AUTHORIZED |
| CAP-07 Invention Decision Room | WS16 / decision-support increment | CAP-05, CAP-06, CAP-08, CAP-10 | RECORDED — NOT AUTHORIZED |
| CAP-08 Assumption Register | Assumption-tracking increment | WS12, CAP-05, CAP-10, CAP-11 | RECORDED — NOT AUTHORIZED |
| CAP-09 Experiment Designer | **WS-PFV-001** (owner-gated) | CAP-01, CAP-04, CAP-06 | RECORDED — NOT AUTHORIZED |
| CAP-10 Contradiction Detector | Contradiction-detection increment | WS12, CAP-05, CAP-08 | RECORDED — NOT AUTHORIZED |
| CAP-11 Evidence Quality Ladder | Dedicated evidence-quality contract | CAP-05, CAP-06, CAP-08 | RECORDED — NOT AUTHORIZED |

The matrix is indicative sequencing only; it activates nothing.

## 3. Dependency map

- **D13** → CAP-01 → (feeds) CAP-04, CAP-06 (technical axes), CAP-09.
- **WS-PFV-001** → CAP-09 → (feeds) CAP-06 (prototype-readiness axis).
- **Patent Export decision** → CAP-06 (patent-disclosure-readiness axis).
- **WS12 Controlled Unknown Progression** → CAP-04, CAP-08, CAP-10 (closure paths / assumptions /
  contradictions over the unknown ledger).
- **Increment-2 provenance/validation axes + append-only ledger** → CAP-08, CAP-10, CAP-11.
- **Decision workspace (FDC-001)** → CAP-05, CAP-07, CAP-10.
- **WS8 / WS13 / WS14** → CAP-02, CAP-03.
- **CAP-11 (evidence ladder)** underpins evidence-strength expressions in CAP-05, CAP-06, CAP-08.
No dependency edge implies activation; every edge is subordinate to the authority it points to.

## 4. Overlap and conflict-prevention rules
1. A capability's overlapping portion is governed by the **most specific committed authority** (e.g. any
   technical-guidance content is governed by D13; prototype/experiment content by WS-PFV-001; patent
   content by the Patent Export decision), never by this register.
2. No capability may weaken, bypass, or reinterpret a deterministic gate, safety/evidence boundary, or
   protected surface.
3. No capability may introduce a second truth source for a concept already governed by a committed
   record (evidence axes, criticality, gaps, unknown ledger, registry).
4. Presentation capabilities (CAP-02, CAP-06, CAP-07) are read-only over canonical records and never
   mutate state or evidence.
5. Where two capabilities could produce the same artifact, the register defers to the workstream/gate
   named in the activation matrix; conflicts are resolved by the committed roadmap, not this register.

---

## R. Governance rules (binding on all future agents)

- **R4 — Multi-Workstream spanning.** A single capability may span multiple Workstreams (e.g. CAP-01
  spans D13 and informs CAP-04/CAP-06/CAP-09) **without being automatically activated** in any of them.
  Spanning is descriptive, not activating.
- **R5 — Registration is not implementation authorization.** Recording a capability here confers no
  authority to design, test, or implement it. Status `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`
  means exactly that.
- **R6 — Every implementation requires the full gated chain.** Before any capability is implemented it
  requires, in order: repository evidence review; an increment contract; owner decisions; BASE RED where
  applicable; GREEN; independent verification; owner acceptance; and merge with formal status
  synchronization. No step may be skipped or combined without explicit owner authorization.
- **R7 — Preservation.** Later agents MUST preserve all eleven entries (CAP-01…CAP-11) exactly, unless
  the owner explicitly approves amendment, rejection, consolidation, or removal. No entry may be
  silently added, dropped, merged, or reworded.
- **R8 — Relationship to committed authorities.** This register is subordinate to and does not amend:
  **Workstreams 12–16** (`DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §15); **Structured Technical
  Guidance / D13** (`ACTIONABLE_VALIDATION_PLAN_INCREMENT_CONTRACT.md` §4 D13; `D13_FORMAL_CLOSURE_
  RECORD.md`); **Patent Export** (`STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md`,
  PR #229); **WS-PFV-001** (`PROTOTYPE_FEASIBILITY_AND_VALIDATION_FUTURE_WORKSTREAM_OWNER_DECISION.md`,
  PR #227); and **AI Coach / Workstream 17** (§15; BLOCKED until Workstreams 1–16 are owner-closed).
  Each of those records remains the sole authority for its capability.
- **R9 — Workstream 12 status.** **Workstream 12 (Controlled Unknown Progression) remains NOT STARTED
  and is temporarily paused** by owner decision until this register is reviewed, owner-accepted, merged,
  and post-merge verified. This register does not resume, start, or activate WS12; any prior
  authorization to begin the WS12 contract is superseded and suspended per the owner decision.

---

## Mandatory Review by Future Agents

Every future agent working on InventorAI (team lead, subagent, or Agent Teams teammate) MUST:

1. **Read this capability register** before: beginning any new Workstream; drafting any increment
   contract; proposing a new capability; or modifying guidance, evidence, progression, export,
   validation, or user-assistance behavior.
2. **Check whether the active Workstream** activates a registered capability; partially overlaps with
   one; creates a prerequisite for one; or risks duplicating or contradicting one.
3. **Explicitly report in every future handover:** which registered capabilities were reviewed; whether
   any activation condition was reached; whether owner authorization is still required; and whether any
   capability remains deferred.
4. **Never treat** registration, prerequisite completion, Workstream closure, or technical feasibility
   as automatic implementation authorization.
5. **Stop and request owner authorization** if an active task would: implement any registered
   capability; change its scope; merge two capabilities; remove or replace a capability; move its
   activation gate; or alter its protected boundaries.
6. **Preserve all eleven capability entries across handovers** unless the owner explicitly authorizes
   amendment, consolidation, rejection, replacement, or removal.

### A. Future-Agent Handover Checklist
Every handover must record:
- [ ] register reviewed
- [ ] active capability IDs identified
- [ ] inactive capability IDs preserved
- [ ] activation conditions checked
- [ ] owner authorization status recorded
- [ ] no automatic activation assumed

### B. Activation Review Rule
At the **formal closure of each Workstream from WS12 through WS16**, the closing agent MUST review this
register and state: which capabilities became **eligible for contract drafting**; which remain
**blocked**; which require **separate owner authorization**; and which must remain **deferred**. (This
review records eligibility only; it activates nothing — see R5.)

### C. Conflict-Prevention Rule
If a later Workstream overlaps with a registered capability, the agent MUST preserve the **narrower
existing Workstream scope** and MUST NOT absorb the full registered capability without a separate
owner-approved contract.

### D. No-Silent-Omission Rule
A future agent may **not** omit a registered capability from planning merely because it was not
mentioned in the latest user message or handover. All eleven entries remain in force at all times.

### Capability review-tracking table

| Capability ID | Current status | Earliest activation gate | Prerequisites | Owner authorization required | Last reviewed Workstream | Next mandatory review point |
|---|---|---|---|---|---|---|
| CAP-01 Structured Technical Guidance | RECORDED — NOT AUTHORIZED | D13 (owner-gated) | D13 governed knowledge sources; D13 Source Review | Yes (via D13) | — (none since registration) | At WS12–WS16 closure and any D13 gate |
| CAP-02 Simplified One-Step Journey | RECORDED — NOT AUTHORIZED | WS8 / later UX increment | Committed state; WS8; WS12 unknowns; CAP-04 | Yes | — | At the UX increment / WS12–WS16 closure |
| CAP-03 Adaptive Assistance | RECORDED — NOT AUTHORIZED | WS13 / WS14 | Deterministic sufficiency; WS12; WS13/WS14 | Yes | — | At WS13/WS14 authorization / WS12–WS16 closure |
| CAP-04 Gap Action Packs | RECORDED — NOT AUTHORIZED | WS12 (+ D13 for technical) | WS12 closure paths; D13; gap/blocker model | Yes | — | At WS12 closure and any D13 gate |
| CAP-05 Decision Trace | RECORDED — NOT AUTHORIZED | Decision-support increment | Decision workspace; evidence axes; CAP-08; CAP-11 | Yes | — | At the decision-support increment / WS12–WS16 closure |
| CAP-06 Readiness Dashboard | RECORDED — NOT AUTHORIZED | Readiness increment (+ Patent Export, WS-PFV-001 axes) | CAP-11; Patent Export decision; WS-PFV-001 | Yes | — | At the readiness increment / WS12–WS16 closure |
| CAP-07 Invention Decision Room | RECORDED — NOT AUTHORIZED | WS16 / decision-support increment | Decision workspace; WS12; CAP-05/08/10 | Yes | — | At WS16 closure / decision-support increment |
| CAP-08 Assumption Register | RECORDED — NOT AUTHORIZED | Assumption-tracking increment | Provenance/validation axes; ledger; WS12; CAP-11 | Yes | — | At the assumption increment / WS12–WS16 closure |
| CAP-09 Experiment Designer | RECORDED — NOT AUTHORIZED | WS-PFV-001 (owner-gated) | WS-PFV-001; SuccessCriterion precedent | Yes (via WS-PFV-001) | — | At any WS-PFV-001 gate / WS12–WS16 closure |
| CAP-10 Contradiction Detector | RECORDED — NOT AUTHORIZED | Contradiction-detection increment | Contradiction graph; UNRESOLVED_EVIDENCE_CONFLICT; CAP-08 | Yes | — | At the contradiction increment / WS12–WS16 closure |
| CAP-11 Evidence Quality Ladder | RECORDED — NOT AUTHORIZED | Dedicated evidence-quality contract | Committed provenance/validation axes; ladder contract | Yes | — | At the evidence-quality contract / WS12–WS16 closure |

"Last reviewed Workstream" is `—` at registration; each future agent performing a §B activation review
MUST update this table (via an owner-authorized register amendment, per R7) to record the reviewing
Workstream and the next mandatory review point. The table is amended only under owner authorization.

## 5. Non-authorization (restated)

This register records capability concepts and their boundaries only. It authorizes no production code,
RED, GREEN, contract execution, status change, persistence, schema, prompt, UI, database, registry, or
architecture change, and starts/activates/resumes no Workstream. All eleven capabilities are
`RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`. Workstream 12 remains NOT STARTED (paused);
Workstreams 13/14/15 remain NOT STARTED; the AI Coach (WS17) remains BLOCKED until Workstreams 1–16 are
owner-closed. Official product state remains `DEMO_READY_WITH_LIMITATIONS`; MVP scope remains
electronics/electrical-only. The Phase A branch remains fixed at `57e2fac8`; PR #167 and PR #162 remain
untouched. Every implementation of any capability requires separate explicit owner authorization and the
full gated chain in R6.
