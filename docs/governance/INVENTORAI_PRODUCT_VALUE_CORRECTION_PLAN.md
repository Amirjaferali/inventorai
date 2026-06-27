# INVENTORAI PRODUCT-VALUE CORRECTION PLAN

Status:
NON-AUTHORIZING GOVERNANCE COMPANION — IMPLEMENTATION NOT AUTHORIZED

Companion to:
`docs/governance/PRODUCT_ARCHITECTURE_AND_CREDIBILITY_ROADMAP.md`

## 1. Purpose

To record, as a non-authorizing design companion, how the InventorAI
idea-development product would be corrected to conform to its already-committed
governance — based on the accepted owner-observed validation findings
(`docs/validation/OWNER_OBSERVED_PRODUCT_VALIDATION_FINDINGS_2026-06-27.md`). It
sequences a dependency-ordered set of increments with acceptance gates. It exists
so that future, separately-authorized implementation work is grounded in one
coherent, governance-conformant plan rather than reconstructed from observation.

## 2. Authority and non-authorizing status

- This document is a NON-AUTHORIZING GOVERNANCE COMPANION. It authorizes no code,
  test, scoring, progression, template, persistence, configuration, benchmark,
  final-technical-selection, or scope change.
- It does not amend, supersede, or duplicate the authority of any active anchor.
- Presence of an increment in this plan is **not** implementation authority and
  **not** scope authorization. Each increment requires a separate, explicit,
  repository-grounded owner authorization for its exact scope.

## 3. Relationship to existing committed governance

This plan is subordinate to, and consistent with, the active governance set. It
references but does not restate the authority of:

- `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md` (Level 0; §7 owner–expert
  questioning and honest-gap rules)
- `docs/governance/STRATEGIC_PRODUCT_VISION.md` (Level 0; §4 coverage/"what it is
  not", §6 layered evolution, §7 "Improvement Not Generation", "Inventor Ownership")
- `docs/governance/DUAL_PATH_PRODUCT_ANCHOR.md` (§2 honest gap/known-unknowns)
- `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` (execution control)
- `docs/governance/NON_SPECIALIST_QUESTIONING_POLICY.md` (committed; NOT IMPLEMENTED)
- `docs/adr/ADR-003-evidence-quality-model.md` (evidence quality definitions)
- `MVP_SCOPE_FREEZE.md` (active scope freeze)
- `docs/governance/PRODUCT_ARCHITECTURE_AND_CREDIBILITY_ROADMAP.md` (parent
  strategic sequencing)
- domain-pack / source-of-truth / handoff contracts:
  `docs/governance/DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md`,
  `docs/governance/SUPPORTED_TECHNOLOGY_AND_SOURCE_OF_TRUTH_CONTRACT.md`,
  `docs/governance/PATH_N_ORCHESTRATION_AND_HANDOFF_CONTRACT.md`

## 4. Accepted product-value findings

From the accepted validation record (summary; full evidence in that record):

- A — Owner–expert question boundary: `CONFIRMED PRODUCT DEFECT` (conformance) +
  `CONFIRMED PRODUCT CAPABILITY GAP`.
- B — Gap/evidence closure honesty: `DOCUMENTATION/TRUTH DEFECT` + `CONFIRMED
  PRODUCT DEFECT`.
- C — Response-depth / closure feedback: `CONFIRMED PRODUCT DEFECT` (proxy-based
  closure; generic feedback).
- D — Visible idea-development value: `CONFIRMED PRODUCT CAPABILITY GAP`.
- E — Deliverable: E2/E3/E4/E8 `CONFIRMED PRODUCT DEFECT`; E10 + E6-underlying
  `CONFIRMED PRODUCT CAPABILITY GAP`; E1/E5/E7/E9/E11 `OBSERVATIONAL`/partial; the
  literal "single hard-coded low risk" is `NOT CONFIRMED`.
- F — Hospital-power: `DOMAIN-SPECIFIC EXPERT GAP` + `CONFIRMED PRODUCT CAPABILITY
  GAP` (generic standards/jurisdiction/specialist mechanism contracted but not
  implemented; specific standards must never be asserted as globally mandatory).

## 5. Governance-to-runtime conformance diagnosis

The defining diagnosis: **the governing principles already exist in committed
governance; the runtime does not yet conform to them.** This is primarily a
conformance program, not a new-principle program:

- Owner–expert boundary is committed (`OWNER_PRODUCT_IDENTITY_CORRECTION.md §7`,
  `STRATEGIC_PRODUCT_VISION.md §7 "Inventor Ownership"`) but unenforced at runtime.
- Honest gap semantics are committed (`DUAL_PATH_PRODUCT_ANCHOR.md §2`,
  `OWNER_PRODUCT_IDENTITY_CORRECTION.md §7`) but the runtime collapses states.
- No-text-length-closure intent is committed (`ADR-003`) but the runtime uses a
  keyword+length proxy.
- Visible-value and stage-bounded-verdict intents are committed
  (`ACTIVE_EXECUTION_ROADMAP.md §4`, `STRATEGIC_PRODUCT_VISION.md §6`) but the
  deliverable is mostly restatement with a binary verdict.
- Standards/compliance honesty is committed (`DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md §6`,
  `SUPPORTED_TECHNOLOGY_AND_SOURCE_OF_TRUTH_CONTRACT.md §7`,
  `STRATEGIC_PRODUCT_VISION.md §4`) but no runtime mechanism applies it per-idea.

## 6. Common epistemic foundation (PROPOSED DESIGN — not implemented authority)

Increments 1 and 2 share one foundation that must be designed (and separately
authorized) before runtime implementation. The following are PROPOSED design
distinctions, not final enums and not authority:

- **Question responsibility** must distinguish at minimum:
  owner-answerable; system-derivable; expert-required; evidence-required.
- **Knowledge / evidence status** must distinguish at minimum:
  unknown; owner-stated; system-inferred; assumed/provisional;
  expert-review-required; expert-reviewed; demonstrated; verified.

Final enum names, transition rules, provenance fields, persistence/serialization
shape, migration of existing `ASSERTED/REASONED/DEMONSTRATED` data, and backward
compatibility all require a **separate design authorization**. This plan asserts
none of them as final.

## 7. Dependency-ordered increments

**Foundation design (shared by Increments 1 and 2).** Design the question
responsibility model, knowledge/evidence states, transition rules, provenance,
migration, and backward compatibility before any runtime implementation. Increments
1 and 2 must not begin runtime work until this foundation is authorized.

**Increment 1 — Owner–Expert Question Boundary.** Enforce the committed
non-specialist policy (`NON_SPECIALIST_QUESTIONING_POLICY.md`) and provide a future
path for: "I do not know"; defer; record a provisional assumption; route to a
specialist; continue without inventing technical values. No question may demand
engineering parameters a non-specialist cannot supply.

**Increment 2 — Truthful Gap and Evidence State.** Prevent owner text, response
length, or causal wording alone from being treated as technical verification or
becoming a generic "resolved" status. Distinct states (per §6) must be preserved
and exported, and the deliverable's resolved/verdict semantics must reflect them.

**Increment 3 — Visible Idea-Development Outputs.** Define bounded, identity-
preserving platform-added value: inference; alternatives; trade-offs; explicit
decisions; recommendation; ranked risk; one concrete next action — while preserving
the committed "Improvement Not Generation" identity (§10).

**Increment 4 — Atomic Requirements and Criticality-Aware Risk Register.**

**Increment 5 — Concrete Validation-Plan Generation.**

**Increment 6 — Deliverable Redesign.** Intentionally **last**, because it depends
on corrected source semantics (Increments 1–2) and corrected outputs
(Increments 3–5); a deliverable redesign on uncorrected sources would re-encode the
current defects.

## 8. Acceptance gates

For every increment, authorization and closure require all of: required
user-visible behavior; required truth/provenance behavior; test expectations;
backward-compatibility expectations; explicit failure conditions; documentation
closure requirement.

**Increment 1 — Owner–Expert Question Boundary**
- User-visible: each question carries a responsibility type; the owner can defer,
  mark a provisional assumption, route to an expert, or proceed without inventing
  values.
- Truth/provenance: deferred/unknown items are preserved as such, not silently
  resolved.
- Tests: a non-specialist run reaches the deliverable with zero demanded specialist
  parameters; tests fail if engineering-heavy demands appear in the non-specialist
  path (operationalizing `NON_SPECIALIST_QUESTIONING_POLICY.md §9`).
- Backward-compat: existing sessions/data remain readable.
- Failure conditions: any question demands an unsupplyable specialist value; a
  deferral is treated as an answer.
- Doc closure: an increment closure record + roadmap synchronization.

**Increment 2 — Truthful Gap and Evidence State**
- User-visible: gaps show their true state (e.g., assumed vs reasoned vs verified),
  not a single "resolved".
- Truth/provenance: a gap never reaches "verified/demonstrated" from text alone;
  closure feedback identifies what is actually missing.
- Tests: a long causal-keyword answer without verification cannot produce
  "resolved/PROCEED"; WPS001 benchmark and replay parity preserved (parity proof
  required before any scoring change).
- Backward-compat: migration of existing `ASSERTED/REASONED/DEMONSTRATED` records.
- Failure conditions: any path equates owner text/length with verification; any
  silent scoring drift without parity proof.
- Doc closure: closure record + roadmap synchronization.

**Increment 3 — Visible Idea-Development Outputs**
- User-visible: the deliverable contains bounded platform-added value (≥1
  architecture hypothesis where appropriate, alternatives, ranked risk, one
  concrete next action), each labeled owner-vs-platform.
- Truth/provenance: every platform-added item carries provenance and confidence;
  nothing is presented as owner-verified fact.
- Tests: provenance labeling present; "Improvement Not Generation" boundary
  preserved.
- Failure conditions: platform output presented as owner-authored or as verified.

**Increments 4–6** (atomic requirements + criticality-aware risk; validation-plan
generator; deliverable redesign): analogous gates, each with user-visible,
truth/provenance, test, backward-compatibility, failure-condition, and
documentation-closure requirements, to be detailed under their own authorizations.

**Target end-state (acceptance for the program as a whole).** A non-technical owner
can complete a new idea session and receive, without inventing specialist
engineering values: (1) problem definition; (2) a bounded system-generated
architecture hypothesis; (3) owner-versus-expert question separation; (4) open
technical unknowns; (5) criticality-aware ranked risks; (6) at least two
alternatives where appropriate; (7) a recommended direction with confidence and
provenance; (8) atomic testable requirements; (9) an expert handoff package; (10)
one concrete next validation action.

## 9. Scope-freeze interaction

`MVP_SCOPE_FREEZE.md` is an ACTIVE FREEZE. Each increment must be explicitly
classified before authorization as one of:
- **Conformance fix** — enforces already-authorized/committed behavior (e.g.,
  Increments 1 and 2 enforce committed governance) and is most defensible under the
  freeze.
- **Capability addition** — may exceed the active MVP scope freeze (e.g., some of
  Increments 3–6) and requires an explicit owner scope decision / freeze amendment
  before authorization.
No increment may treat its presence in this plan as scope authorization.

## 10. Improvement-versus-generation boundary

`STRATEGIC_PRODUCT_VISION.md §7` commits the product to "Improvement Not
Generation" and "Inventor Ownership." Increment 3's bounded platform-added value
must therefore: derive from and clearly attribute to owner-stated content and
captured evidence; carry provenance and confidence; never overwrite owner ownership
of the idea or reasoning; and never present generated analysis as owner-verified
fact. Any generative behavior that would shift idea ownership to the platform is
out of scope and requires explicit owner product-philosophy resolution before it
may be designed.

## 11. Migration and compatibility risks

- Changing gap/evidence semantics (Increment 2) risks the WPS001 benchmark and
  replay parity; the CLAUDE.md refactor-governance contract requires
  behavior-preservation and parity proof before any scoring/closure change.
- Broad test impact is expected (e.g., `test_assess_response_*`, `test_stage3_*`,
  `test_progression_*`, golden/replay fixtures, `test_deliverable_assembler.py`,
  `test_fdc001_user_value.py`).
- Existing serialized `IdeaState` data must migrate cleanly to any new
  state model.
- Non-specialist path changes must not move any held/blocked state.

## 12. Protected states

This plan changes nothing and preserves: persistence `PRESERVE UNMODIFIED AND
PAUSE`; benchmark `NOT RUN`; final technical selection `NONE`; R2 HELD; FORM T
BLOCKED; S-6 UNCLASSIFIED; AA-3/AA-4/AA-5 BLOCKED; Phase 5/6 UNAUTHORIZED; and all
prior FDC-001/FDC-002 closure facts.

## 13. Anchor decision

- No substantive standalone anchor amendment is currently required.
- The relevant principles already exist in committed governance (owner–expert
  boundary; honest gap semantics; no-text-length closure; visible value;
  stage-bounded verdicts; standards/compliance honesty).
- The primary issue is governance-to-runtime conformance, addressed by this plan
  and future implementation — not by new anchor language.
- An optional future cross-reference consolidation that merely *names* the existing
  principles in one place may be proposed separately, but it is not required for
  correction execution and is not authorized here.

## 14. Separate future authorization requirements / Final non-authorization statement

Each of the following requires its own separate, explicit, repository-grounded
owner authorization for that exact scope: the shared epistemic-foundation design;
each increment's implementation; any scope-freeze classification or amendment; any
scoring/closure change (with parity proof); any deliverable-template change; any
domain-pack/standards mechanism; and any change to persistence, benchmark, or final
technical selection. Nothing in this document authorizes any of them. Implementation
has not started and is not authorized.
