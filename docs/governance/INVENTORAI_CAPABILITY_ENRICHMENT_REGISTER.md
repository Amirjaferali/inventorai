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
- **Post-Output AI-Assisted Specialist Refinement (AISR)** is governed by
  `POST_OUTPUT_AI_ASSISTED_SPECIALIST_REFINEMENT_CANONICAL_DECISION.md` (canonical, non-authorizing;
  status `ACCEPTED PRODUCT DIRECTION` / `IMPLEMENTATION NOT AUTHORIZED`; owner decisions D-AISR-01 …
  D-AISR-10). That record — not this register — governs AISR. Its directional responsibility model
  records that **WS17 may later become the user-facing advisory umbrella** and that **STG (D13/CAP-01)
  may later be a bounded specialist capability WS17 invokes where separately authorized**; it does
  **not** define WS17's functional scope and does **not** expand or activate STG. WS17 and STG remain
  governed by their own records above and remain NOT AUTHORIZED / NOT STARTED.

No existing canonical capability register enumerates these fourteen concepts; this record does not
duplicate or conflict with any existing authority.

---

## 1. Capability entries

All capabilities recorded here (CAP-01 … CAP-18) share the status **`RECORDED — NOT AUTHORIZED FOR
IMPLEMENTATION`** and require **separate explicit owner authorization** before any implementation (see
§R5/§R6). (CAP-15 … CAP-18 were added by the legacy post-mortem capture in §1A; the original fourteen
concepts referenced elsewhere in this register's genesis note are unchanged.)

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

### CAP-12 — Prototype Materials and Manufacturing Recommendation
- **Product problem:** a user may complete the invention journey without knowing what material each
  component should be made from, how a prototype component could be manufactured, or whether a component
  should be fabricated or purchased as a standard part.
- **User value:** an optional, understandable, component-by-component prototype materials and
  manufacturing recommendation that helps plan a first testable prototype without presenting it as a
  final engineering or production specification.
- **Intended future behavior:** for each identifiable and user-confirmed component, the capability MAY
  propose — component identity; component function; proposed prototype material; proposed material
  family; proposed material grade or subtype only where supportable; reason for the proposal; one or more
  alternatives; advantages and limitations of each alternative; proposed prototype manufacturing method;
  whether fabrication or procurement of a standard part may be preferable; possible standard component
  categories; the distinction between prototype material and possible production material; environmental
  and operating assumptions; missing information; required validation, measurements, calculations, tests,
  or documents; recommendation status; component-specific warnings; and source provenance and evidence
  quality. Possible material families (only where appropriate and sufficiently supported): aluminum,
  carbon steel, stainless steel, copper, engineering plastics, rubber, silicone, fiberglass, acrylic,
  wood or MDF for early mock-ups, foam, insulation materials, composites, adhesives, seals and gaskets,
  standard fasteners, purchased mechanical components, purchased electrical or electronic components.
  Possible prototype manufacturing approaches (where appropriate): 3D printing, CNC machining, laser
  cutting, water-jet cutting, sheet-metal cutting and bending, casting, molding, fiberglass lay-up,
  adhesive joining, mechanical fastening, use of commercially available components, manual mock-up
  construction.
- **Required advisory character:** **OPTIONAL — ADVISORY — NON-BINDING.** The user may request it,
  decline it, ignore it, request alternatives, or compare options by priorities such as speed, cost,
  weight, durability, or ease of fabrication. **Declining CAP-12 must not block completion of the core
  invention journey.**
- **Non-goals / protected boundaries:** must not create a mandatory material specification; must not
  claim final engineering approval; must not claim structural, electrical, thermal, chemical, medical,
  food-contact, environmental, or regulatory suitability without the required evidence; must not
  fabricate material properties, manufacturer specifications, standards, or certifications; must not
  silently treat a recommendation as verified evidence; must not replace qualified specialist review
  where risk is material; must clearly distinguish prototype material from production material; must not
  infer material solely from visual appearance; must not activate CAP-13 automatically; must not activate
  WS-PFV-001 automatically.
- **Dependencies and overlaps:** CAP-01, CAP-08, CAP-09, CAP-10, CAP-11, **CAP-13**, **CAP-14**,
  WS-PFV-001. Technical-guidance content defers to D13; prototype/validation content defers to WS-PFV-001.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Earliest activation:** a dedicated materials-and-manufacturing feasibility gate (§6), followed by:
  governed source review; data licensing review; knowledge-source contract; deterministic rule and
  calculation boundary; increment contract; owner decisions; separate owner authorization; BASE RED where
  applicable; GREEN; independent verification; owner acceptance and formal closure.
- **Separate owner authorization requirement:** yes. CAP-12 is a **distinct capability from CAP-13 and
  CAP-14** and must not be consolidated with either.

### CAP-13 — Component Thickness, Specification, and Safety Advisory
- **Product problem:** a general material recommendation is insufficient when the user does not know the
  proposed thickness, dimensional range, material grade, component-specific constraints, or safety
  limitations of a proposed prototype component.
- **User value:** an optional, component-specific advisory recommendation for material type or grade,
  thickness or thickness range, assumptions, missing inputs, validation requirements, and safety warnings.
- **Intended future behavior:** for each identifiable and user-confirmed component, the capability MAY
  propose — component identity; component function; proposed material type; proposed material grade or
  subtype where supportable; proposed thickness or thickness range; explicit unit; reason for the
  proposed range; manufacturing constraints affecting thickness; expected prototype use; load, support/
  attachment, heat, moisture, impact, vibration/fatigue, chemical-exposure, electrical, flexibility/
  rigidity, insulation, and outdoor/environmental assumptions; missing measurements and requirements;
  alternative thicknesses; alternative materials; required calculations, tests, documents, and specialist
  review; warning category; recommendation status; and source provenance and evidence quality.
- **Thickness behavior:** prefer an advisory range rather than false precision; use explicit units;
  distinguish conceptual thickness from prototype-suitable thickness, and prototype thickness from
  production thickness; do NOT provide a precise thickness where dimensions, geometry, loads, supports,
  joints, temperature, environment, manufacturing method, tolerance, safety factor, or applicable
  requirements are insufficient; do not infer final production thickness from prototype thickness; do not
  treat a proposed thickness as evidence, certification, or approval; identify the exact missing
  information when a recommendation cannot safely be produced.
- **Required recommendation levels:** `CONCEPTUAL` · `PROTOTYPE-SUITABLE` · `ENGINEERING REVIEW REQUIRED`
  · `UNABLE TO RECOMMEND`.
- **Required advisory character:** **OPTIONAL — ADVISORY — NON-BINDING.** Declining CAP-13 must not block
  completion of the core invention journey.
- **Mandatory warning categories:** *General* — preliminary and advisory, not a final engineering or
  manufacturing specification. *Structural* — do not rely on a proposed thickness before verifying loads,
  supports, stress, deformation, joints, fatigue, impact, and safety factor. *Electrical and battery* —
  verify insulation, flammability, heat resistance, electrical clearances, battery containment,
  short-circuit risks, and applicable requirements. *Heat and pressure* — do not use for pressure
  vessels, high-temperature systems, or safety-critical containment without specialist design and
  validation. *Medical, food-contact, or human-contact* — do not claim suitability before verifying
  biocompatibility, food-contact suitability, toxicity, cleaning, sterilization, skin-contact
  requirements, and applicable regulation. *Children and consumer safety* — review sharp edges, small
  parts, pinch points, entrapment, toxicity, impact, misuse, and applicable consumer-safety requirements.
  *Chemical and outdoor exposure* — verify corrosion, ultraviolet exposure, moisture, chemical
  compatibility, aging, sealing, and environmental degradation.
- **Non-goals / protected boundaries:** must never be presented as mandatory; must not constitute
  structural certification or safety approval; must not fabricate dimensions, loads, material grades,
  calculations, or standards; must not replace mechanical, materials, electrical, safety, medical, or
  regulatory specialist review where required; must expose assumptions, uncertainty, missing information,
  and validation needs; must clearly distinguish prototype recommendations from production
  specifications; must not infer a reliable thickness solely from an image or undimensioned drawing; must
  not activate CAP-12, CAP-14, or WS-PFV-001 automatically.
- **Dependencies and overlaps:** CAP-01, CAP-08, CAP-09, CAP-10, CAP-11, **CAP-12**, **CAP-14**,
  WS-PFV-001. Technical-guidance content defers to D13; prototype/validation content defers to WS-PFV-001.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Earliest activation:** a dedicated thickness-and-safety feasibility gate (§6), followed by a separate
  owner-approved increment. CAP-12 and CAP-13 may later be coordinated only through a separate,
  owner-approved contract; their registration here does not authorize consolidation or implementation.
- **Separate owner authorization requirement:** yes. CAP-13 is a **distinct capability from CAP-12 and
  CAP-14** and must not be consolidated with either.

### CAP-14 — 2D Drawing, Static Image, and Multi-View Component Interpretation
- **Product problem:** a user may understand the invention visually but be unable to describe its
  components, geometry, interfaces, visible movements, or assembly relationships in sufficiently
  structured technical language.
- **User value:** allow the user to provide one or more static images, a 2D drawing, an annotated sketch,
  or multiple static views so the future capability can propose a structured component inventory and
  identify information that remains visually unavailable, ambiguous, hidden, or technically unresolved.
- **Supported future input types:** one static image; multiple static images; front / side / top /
  perspective views; dimensioned 2D drawing; undimensioned 2D drawing; section view; annotated sketch;
  image containing a reference dimension; image containing a reliable scale object; user labels; movement
  arrows; component annotations.
- **VIDEO IS EXPLICITLY EXCLUDED.** The following are outside scope and NOT authorized: video upload;
  video interpretation; real-video analysis; AI-generated-video analysis; animation analysis;
  video-to-component inference; video-to-CAD; video-derived material recommendations; video-derived
  thickness recommendations; frame extraction as a way to bypass the video exclusion.
- **Intended future behavior:** the capability MAY — identify visible component candidates, interfaces,
  openings, joints, fasteners, and supports; identify possible relative movement shown by arrows or
  multiple views; read explicit dimensions and labels where reliably visible; distinguish known
  dimensions from inferred proportions; distinguish visible observations from model inferences; identify
  hidden, occluded, ambiguous, or missing components; identify possible contradictions between views;
  propose a preliminary component hierarchy; ask the user to confirm, reject, rename, split, or merge
  proposed components; preserve each image or drawing as source provenance; associate observations with
  their source image or view; convert ONLY user-confirmed observations into canonical structured
  component records; and identify additional views, dimensions, sections, labels, or explanations
  required before materials or thickness may be considered.
- **Required output classifications:** `OBSERVED` · `USER-CONFIRMED` · `INFERRED` · `AMBIGUOUS` ·
  `HIDDEN OR NOT VISIBLE` · `CONTRADICTORY` · `UNABLE TO DETERMINE`.
- **Confirmation boundary:** **no inferred component, relationship, dimension, movement, or interface may
  enter canonical invention state until the user confirms it.** The original visual source and the
  inference status must remain traceable.
- **Non-goals / protected boundaries:** static visual interpretation only; video, animation, and
  AI-generated-video analysis are excluded; must not treat inferred components as confirmed facts; must
  not infer internal mechanisms solely from external appearance; must not infer accurate scale without a
  reliable reference; must not fabricate dimensions, hidden geometry, material, thickness, load,
  tolerance, or manufacturing specifications; must not generate or claim a production-ready CAD model;
  must not claim that a visual concept is physically feasible; must NOT recommend materials, manufacturing
  methods, material grades, or thicknesses; must not activate CAP-12 or CAP-13 automatically; must not
  replace engineering drawings or specialist review; must preserve provenance, uncertainty, and user
  confirmation state.
- **Relationship to CAP-12 and CAP-13:** CAP-14 may provide a user-confirmed component inventory and
  known visual constraints; CAP-12 may LATER use confirmed component records when proposing materials and
  manufacturing methods; CAP-13 may LATER use confirmed dimensions and constraints when considering
  thickness or specification advice. **CAP-14 must not itself perform CAP-12 or CAP-13 behavior.**
- **Dependencies and overlaps:** WS12, CAP-01, CAP-08, CAP-10, CAP-11, **CAP-12**, **CAP-13**.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Earliest activation:** a dedicated static-visual-intake and component-interpretation feasibility gate
  (§6), followed by: architecture review; privacy and retention review; image-source and provenance
  contract; supported-format contract; model and vendor feasibility review; accuracy and failure-mode
  evaluation; owner decisions; separate owner-approved increment contract; BASE RED where applicable;
  GREEN; independent verification; owner acceptance and formal closure.
- **Separate owner authorization requirement:** yes. CAP-14 is a **distinct capability from CAP-12 and
  CAP-13** and must not be consolidated with either.

---

## 1A. Legacy post-mortem capability capture (source: failed legacy application "idea&reality")

The following four capability proposals (**CAP-15 … CAP-18**) were derived from an owner-supplied
post-mortem of the failed legacy application **idea&reality**. The legacy system is treated as a **source
of lessons and possible ideas, NOT authoritative architecture**; no legacy code is imported and its
architecture is not copied. Every entry below is **`RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`**.
**RECORDED ≠ AUTHORIZED. ELIGIBLE ≠ AUTHORIZED. IDEA ≠ ROADMAP COMMITMENT.** Recording these does **not**
change the active critical path: unfinished original Product-Foundation work remains, so these items are
captured but must **not** displace it (displacement check: PASS — recorded, non-displacing).

### CAP-15 — AI Provider Abstraction
- **Priority:** HIGH. **Status:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Purpose:** prevent InventorAI application/domain logic from becoming directly coupled to a specific AI
  vendor, SDK, or model name. Target principle: `Application/Domain Logic → AI Service Boundary → Provider
  Interface → Provider Implementation`. Potential future providers may include OpenAI, Anthropic, or
  others. **This record authorizes no provider migration and selects no provider.**
- **Expected benefits:** model/provider replacement without touching unrelated logic; centralized model
  selection, timeout/retry, response handling, and operational/cost controls; prevention of the legacy
  failure where many services independently instantiate model SDKs and hard-code model names.
- **Critical Lean rule:** do NOT create speculative provider abstractions before live AI usage justifies
  the boundary; do NOT build a plugin framework or a general AI-orchestration platform. Implement only when
  evidence shows direct provider coupling beginning to proliferate, or provider replaceability becomes a
  real requirement.
- **Proposed timing:** a separate future AI-platform gate after the current AI boundary is sufficiently
  evidenced and before direct provider usage proliferates. **Do not attach it automatically to §5-I2.**
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`. Separate explicit owner
  authorization required.

### CAP-16 — Safe Domain Suggestion Assistant
- **Priority:** HIGH. **Status:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Purpose:** let a non-technical user describe an idea naturally and have InventorAI **suggest** the most
  relevant technical domain instead of requiring manual engineering classification.
- **Critical product rule:** **DOMAIN SUGGESTION ≠ DOMAIN ACTIVATION.** The assistant may suggest a domain
  that has no activated specialist experience; if a suggested domain is not activated, InventorAI must say
  so truthfully and follow the permitted general/fallback behavior. It MUST consume the **canonical Domain
  Registry** and MUST NOT: maintain a parallel hard-coded domain list; create its own taxonomy; activate
  domains; treat confidence as specialist certification; or override runtime activation policy.
- **Preferred future model:** deterministic registry evidence first; AI assistance only where justified;
  possible output = suggested domain + supporting evidence/reason + confidence/evidence strength +
  alternative domain(s) + current support/activation status.
- **Legacy lesson:** the legacy app had classifiers covering many domains while runtime supported fewer —
  InventorAI must never repeat that divergence.
- **Proposed timing / dependency:** only after the §5 Domain Registry + activation-status +
  unsupported-domain foundations are sufficiently stable. It **depends on** the canonical §5 foundation and
  must **not** become a reason to accelerate new-domain activation.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`. Separate explicit owner
  authorization required.

### CAP-17 — Central Prompt and Model Configuration
- **Priority:** MEDIUM-HIGH. **Status:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Purpose:** prevent model names, prompts, system instructions, response schemas, timeouts, and task
  configuration from being scattered across unrelated services.
- **Initial Lean target:** repository-versioned configuration. Possible future concepts: task identifier;
  provider/model reference; prompt version; system-instruction version; expected output schema; timeout;
  safe fallback policy; provenance/version metadata.
- **Critical Lean rule:** do NOT begin with a database-managed prompt platform or an administrative
  prompt-management system without demonstrated operational need; a database-backed prompt registry is
  considered only if evidence later shows prompts must change independently of normal deployment/version
  control. Do not implement merely because the legacy system had scattered prompts.
- **Proposed timing:** alongside or after CAP-15 (AI Provider Abstraction).
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`. Separate explicit owner
  authorization required.

### CAP-18 — Commercial Readiness Snapshot
- **Priority:** LOWER than CAP-15…CAP-17. **Status:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.
- **Purpose:** a bounded commercial perspective after an invention concept is sufficiently structured.
  Possible future contents: target user/customer; problem/value proposition; commercialization assumptions;
  major cost drivers; evidence gaps; major commercial unknowns; questions requiring market validation;
  possible next validation actions.
- **Non-goals / protected boundaries:** must NOT become an ERP, investor marketplace, procurement system,
  accounting system, full financial-modeling suite, guaranteed-ROI analysis, or investment advice.
- **Proposed timing:** future output/product enrichment only after core idea-development and
  technical/domain foundations are stable. Must not displace original remediation or Product-Foundation
  work.
- **Current authorization state:** `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`. Separate explicit owner
  authorization required.

### Legacy patterns explicitly NOT recommended for InventorAI (intentional risk controls)

These legacy idea&reality patterns are **not** recommended for migration under the current product strategy
and are recorded as durable exclusions (none is authorized; each may be revisited only under separate
evidence, contract, and owner authorization):
1. **Physical / multi-physics simulation engines** (MultiPhysicsEngine-style; thermal-structural; flight
   physics; finite/calculated physical-simulation suites; generalized simulation orchestration) — excluded.
2. **Broad domain-specific engineering simulation suites** (mechanical / drone / PCB-circuit / solar /
   mold) — excluded; a narrowly bounded deterministic calculation is possible only under separate evidence,
   contract, and authorization.
3. **Authoritative safety/reliability engines** (legacy SafetyReliabilityAnalyzer as an authoritative
   capability; automatic FMEA conclusions; MTBF/availability guarantees; safety certification; compliance
   approval) — excluded. InventorAI is not a professional engineering certifier.
4. **Standards certification claims** (automatic ASTM/DIN/JIS/regulatory/professional-approval claims) —
   excluded; standards may become evidence/references in future authorized work, never certification claims.
5. **IoT device-management platform** (telemetry / firmware-management / live-device dashboard /
   cloud-device management) — excluded; separate products.
6. **PCB manufacturing/ordering platform** (manufacturer marketplace / quote engine / ordering /
   procurement workflow) — excluded from core InventorAI.
7. **Domain-specific mega-dashboards** (a separate large app/dashboard per domain) — excluded; prefer a
   shared product shell + canonical domain-pack-driven differences + minimum domain-specific presentation.
8. **Hundreds of domain-specific APIs before stable resource contracts** — excluded; Phase 7/API work
   remains separately governed.
9. **Parallel domain taxonomies** (independent AI-classifier / frontend / integration-engine / feature
   domain lists) — excluded; the **canonical Domain Registry remains the source of domain truth**.
10. **Duplicate component/material databases by default** (per-domain large libraries pre-created) —
    excluded; the accepted §5 principle is thin capability references first, a shared capability registry
    only if cross-domain reuse evidence later justifies it (D-S5-02).
11. **Multiple direct AI SDK integrations** (unrelated services independently instantiating vendor SDKs and
    hard-coding model names) — excluded; the exact failure CAP-15 is intended to prevent if/when authorized.
12. **Database prompt platform before need** — excluded; repository-versioned configuration is the Lean
    starting point if/when CAP-17 is authorized.
13. **Large Monte Carlo / financial simulation as a current requirement** (legacy EconomicSimulator; VaR;
    CVaR; Sharpe ratio; max drawdown; investment-style probability modeling) — excluded unless a future
    owner-authorized product need clearly justifies it; InventorAI must not drift into financial-advice or
    investment-analysis territory by default.
14. **Broad domain-module expansion before foundation completion** (the most important exclusion) — do NOT
    build many new domain implementations merely because the Domain Registry can describe them.
    **REGISTERED ≠ ACTIVATED. KNOWN DOMAIN ≠ IMPLEMENTED DOMAIN. SUGGESTED DOMAIN ≠ ACTIVATED DOMAIN.
    FOUNDATION FIRST.**

### Durable legacy lessons to preserve

1. Foundation before domain expansion. 2. Finish and verify one bounded increment before opening attractive
successor work. 3. Tests must prove real application behavior. 4. A passing arithmetic/unit-fixture test is
not a substitute for application-behavior coverage. 5. Avoid God files. 6. Avoid God tables. 7. Avoid
repeated domain infrastructure where a shared canonical contract can be consumed. 8. The Domain Registry
must remain the canonical source of domain truth. 9. Do not let classifier taxonomies diverge from runtime
support. 10. AI provider/model usage should gain a controlled boundary before provider calls proliferate.
11. Configuration should be versionable, replaceable, and reversible. 12. Feature flags do not justify
building large inactive modules early. 13. "Recorded" capability does not mean "authorized." 14. Attractive
future capability does not automatically outrank unfinished original remediation. 15. Frozen architecture is
not a substitute for modular architecture + behavior-sensitive tests. 16. Do not solve lack of confidence
by forbidding change; solve it through bounded modules, contracts, tests, and reversible changes. 17. Agents
must finish current authorized/broken work before adding unrelated capability. 18. Minimum-path
implementation is preferred over speculative framework building.

### Relation to current Product-Foundation §5 (recorded, non-authorizing)

§5-C1 is the **ACCEPTED CONTRACT OF RECORD**; **§5-I1 (Domain Registry Validation Hardening / D-P6-14) is
FORMALLY ACCEPTED AND CLOSED**; **Product-Foundation §5 as a whole is NOT complete**. The next eligible gate
is **§5-I2 — Activation-status policy + explicit unsupported-domain model**, which remains **ELIGIBLE FOR
OWNER CONSIDERATION, NOT AUTHORIZED / NOT STARTED**. **CAP-16 (Safe Domain Suggestion Assistant) must NOT be
implemented before its required §5 activation/support-state foundations are adequate.** CAP-15 / CAP-17 /
CAP-18 are separate future concerns and do **not** become part of §5 merely because they are recorded now.
The existing deferred items (QTA, WS17, STG, ACV, Output Language, PDF/download, email delivery, and
CAP-01…CAP-14) are **unchanged** and remain governed by their existing status. This capture activates
nothing, authorizes nothing, and changes no critical path.

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
| CAP-12 Prototype Materials and Manufacturing Recommendation | Dedicated materials-and-manufacturing feasibility gate → increment (defers to WS-PFV-001, D13) | CAP-01, CAP-08, CAP-09, CAP-10, CAP-11, CAP-13, CAP-14 | RECORDED — NOT AUTHORIZED |
| CAP-13 Component Thickness, Specification, and Safety Advisory | Dedicated thickness-and-safety feasibility gate → increment (defers to WS-PFV-001, D13) | CAP-01, CAP-08, CAP-09, CAP-10, CAP-11, CAP-12, CAP-14 | RECORDED — NOT AUTHORIZED |
| CAP-14 2D Drawing, Static Image, and Multi-View Component Interpretation | Dedicated static-visual-intake and interpretation feasibility gate → increment | WS12, CAP-01, CAP-08, CAP-10, CAP-11, CAP-12, CAP-13 | RECORDED — NOT AUTHORIZED |

The matrix is indicative sequencing only; it activates nothing. All eighteen capabilities (CAP-01…CAP-18) remain
`RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`.

## 3. Dependency map

- **D13** → CAP-01 → (feeds) CAP-04, CAP-06 (technical axes), CAP-09.
- **WS-PFV-001** → CAP-09 → (feeds) CAP-06 (prototype-readiness axis).
- **Patent Export decision** → CAP-06 (patent-disclosure-readiness axis).
- **WS12 Controlled Unknown Progression** → CAP-04, CAP-08, CAP-10 (closure paths / assumptions /
  contradictions over the unknown ledger).
- **Increment-2 provenance/validation axes + append-only ledger** → CAP-08, CAP-10, CAP-11.
- **Decision workspace (FDC-001)** → CAP-05, CAP-07, CAP-10.
- **WS8 / WS13 / WS14** → CAP-02, CAP-03.
- **CAP-11 (evidence ladder)** underpins evidence-strength expressions in CAP-05, CAP-06, CAP-08, and
  also CAP-12/CAP-13/CAP-14.
- **WS-PFV-001 + D13** → CAP-12, CAP-13 (prototype/validation content defers to WS-PFV-001;
  technical-guidance content defers to D13). CAP-12 and CAP-13 are **separate** capabilities that
  reference each other and share CAP-01/CAP-08/CAP-09/CAP-10/CAP-11 dependencies, but neither subsumes
  the other.
- **CAP-14 (static visual interpretation)** → may LATER feed **user-confirmed** component records to
  CAP-12 and confirmed dimensions/constraints to CAP-13; CAP-14 depends on WS12, CAP-01, CAP-08, CAP-10,
  CAP-11 and never itself performs CAP-12/CAP-13 behavior. No CAP-14 inference becomes canonical without
  user confirmation.
No dependency edge implies activation; every edge is subordinate to the authority it points to, and no
capability may activate another automatically.

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
6. **CAP-12 does not perform CAP-13 thickness behavior.**
7. **CAP-13 does not perform CAP-12 material/manufacturing selection** without its separately authorized
   boundary.
8. **CAP-14 does not perform CAP-12 or CAP-13 behavior** (no material, manufacturing, grade, or thickness
   recommendation from visual interpretation).
9. **CAP-14 visual inference does not become canonical without explicit user confirmation.**
10. **No Workstream may silently absorb any of CAP-12 through CAP-14**, and **no capability may activate
    another automatically.**

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
- **R7 — Preservation.** Later agents MUST preserve all eighteen entries (CAP-01…CAP-18) exactly, unless
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
6. **Preserve all eighteen capability entries (CAP-01…CAP-18) across handovers** unless the owner explicitly authorizes
   amendment, consolidation, rejection, replacement, or removal.

### A. Future-Agent Handover Checklist
Every handover must record (for all eighteen capabilities, CAP-01…CAP-18):
- [ ] register reviewed
- [ ] active capability IDs identified
- [ ] inactive capability IDs preserved
- [ ] activation conditions checked
- [ ] owner authorization status recorded
- [ ] no automatic activation assumed

Additionally, a later agent MUST explicitly report the status of **CAP-12, CAP-13, and CAP-14** whenever
its active task overlaps materials, manufacturing, thickness, specifications, safety, images, drawings,
multiple views, component inference, or prototype planning.

### B. Activation Review Rule
At the **formal closure of each Workstream from WS12 through WS16**, the closing agent MUST review this
register and state: which capabilities became **eligible for contract drafting** (explicitly including
whether **CAP-12, CAP-13, or CAP-14** became eligible for a feasibility gate or contract drafting); which
remain **blocked**; which require **separate owner authorization**; and which must remain **deferred**.
(This review records eligibility only; **eligibility must not be treated as implementation
authorization** — see R5.)

### C. Conflict-Prevention Rule
If a later Workstream overlaps with a registered capability, the agent MUST preserve the **narrower
existing Workstream scope** and MUST NOT absorb the full registered capability without a separate
owner-approved contract.

### D. No-Silent-Omission Rule
A future agent may **not** omit a registered capability from planning merely because it was not
mentioned in the latest user message or handover. All eighteen entries (CAP-01…CAP-18) remain in force at all times.

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
| CAP-12 Prototype Materials and Manufacturing Recommendation | RECORDED — NOT AUTHORIZED | Materials-and-manufacturing feasibility gate → increment | CAP-01, CAP-08, CAP-09, CAP-10, CAP-11, CAP-13, CAP-14; WS-PFV-001; D13; governed data/source/licensing gate (§6) | Yes | — | At the materials feasibility gate / WS12–WS16 closure |
| CAP-13 Component Thickness, Specification, and Safety Advisory | RECORDED — NOT AUTHORIZED | Thickness-and-safety feasibility gate → increment | CAP-01, CAP-08, CAP-09, CAP-10, CAP-11, CAP-12, CAP-14; WS-PFV-001; D13; governed data/source/licensing gate (§6) | Yes | — | At the thickness feasibility gate / WS12–WS16 closure |
| CAP-14 2D Drawing, Static Image, and Multi-View Component Interpretation | RECORDED — NOT AUTHORIZED | Static-visual-intake and interpretation feasibility gate → increment | WS12, CAP-01, CAP-08, CAP-10, CAP-11, CAP-12, CAP-13; static-image/2D feasibility gate (§6) | Yes | — | At the static-visual feasibility gate / WS12–WS16 closure |

"Last reviewed Workstream" is `—` at registration; each future agent performing a §B activation review
MUST update this table (via an owner-authorized register amendment, per R7) to record the reviewing
Workstream and the next mandatory review point. The table is amended only under owner authorization.

## Knowledge, Data, and Feasibility Boundary (CAP-12 / CAP-13 / CAP-14)

Recording CAP-12 and CAP-13 does **not** prove that the existing code, data model, external sources,
engineering tools, or knowledge architecture can support reliable material, manufacturing, grade, or
thickness recommendations. Before implementation of CAP-12 or CAP-13, a **separate feasibility gate**
must determine at minimum: available repository seams; the required component data model; required
dimensions and engineering inputs; allowed external knowledge sources; source licensing and
redistribution rights; source freshness and versioning; manufacturer-data provenance; standards-access
limitations; deterministic rules; calculation-engine requirements; specialist-review boundaries;
high-risk exclusion cases; `UNABLE TO RECOMMEND` conditions; operational costs; maintenance requirements;
and a realistic MVP boundary.

The register explicitly states:
- an **AI model must NOT be the sole authority** for material properties, manufacturing suitability,
  material grades, thickness, safety, or regulatory suitability;
- **external data may NOT be integrated** without a separate governed source and licensing decision;
- **implementation feasibility remains unproven** until the dedicated gate is completed;
- the system **must be allowed to refuse a recommendation** (`UNABLE TO RECOMMEND`) when evidence or
  inputs are insufficient.

For **CAP-14**, feasibility likewise **remains unproven** until a dedicated static-image and 2D
interpretation gate evaluates: supported image and drawing formats; OCR and dimension-reading limits;
multi-view consistency; image-quality requirements; privacy and retention; provenance storage;
model/vendor selection; error rates; ambiguity handling; the user-confirmation workflow; cost; latency;
security; and architectural compatibility with the current application. CAP-14 remains static-image/2D
only; **video, animation, and AI-generated-video analysis are excluded** (including frame extraction to
bypass the exclusion).

## 5. Non-authorization (restated)

This register records capability concepts and their boundaries only. It authorizes no production code,
RED, GREEN, contract execution, status change, persistence, schema, prompt, UI, database, registry,
external-data/knowledge-source integration, visual-analysis, material-selection, thickness-calculation,
engineering-analysis, CAD-generation, or architecture change, and starts/activates/resumes no Workstream.
All eighteen capabilities (CAP-01…CAP-18) are `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`. **This amendment activates
none of CAP-12, CAP-13, or CAP-14: recording CAP-12 (Prototype Materials and Manufacturing
Recommendation), CAP-13 (Component Thickness, Specification, and Safety Advisory), and CAP-14 (2D
Drawing, Static Image, and Multi-View Component Interpretation) implements nothing, authorizes no
material/manufacturing/thickness/visual-analysis behavior, and confers no implementation authority; they
are three distinct capabilities and are not consolidated.** Implementation feasibility for CAP-12,
CAP-13, and CAP-14 remains **unproven** until their dedicated feasibility gates complete; an AI model must
not be the sole authority for material, thickness, safety, or regulatory recommendations; and no external
data may be integrated without a separate governed source and licensing decision. Workstream 12 remains
NOT STARTED (paused) — and remains paused until this amendment is owner-accepted, merged, and post-merge
verified; Workstreams 13/14/15 remain NOT STARTED; the AI Coach (WS17) remains BLOCKED until Workstreams
1–16 are owner-closed. Official product state remains `DEMO_READY_WITH_LIMITATIONS`; MVP scope remains
electronics/electrical-only. The Phase A branch remains fixed at `57e2fac8`; PR #167 and PR #162 remain
untouched. Every implementation of any capability requires separate explicit owner authorization and the
full gated chain in R6.

## THERM-01 — Future Thermal Analysis / Thermal Simulation Capability (governed future path; Owner-approved amendment; NON-ACTIVATING)

**Amendment authority and status.** Owner-directed anti-forgetting registration (ODR **`D-THERM-01`**; this is the
explicit owner approval R7 requires for a register amendment). **NON-ACTIVATING and NON-AUTHORIZING** — recording this
section implements nothing, authorizes nothing, and is subordinate exactly as the register header states. It adds **no
new CAP entry** (the CAP-01…CAP-18 range and count are unchanged; D-GMPR-01-D-D6 preserved), creates **no new
workstream, framework, or owner**, and deliberately carries a **non-numeric designation (`THERM-01`)** so that no
pre-existing numeric cross-reference in this register (including the six historical section-6 feasibility-gate
cross-references in the CAP-12 / CAP-13 / CAP-14 entries and matrix rows, which are left byte-untouched and are NOT
re-bound, repaired, or reinterpreted here) can resolve to this section.

**Purpose (anti-forgetting).** The authoritative Mechanical P9-MECH-I1 declaration truthfully lists thermal behavior
and thermal simulation as NOT COVERED, and the §1A legacy exclusions intentionally exclude multi-physics/
thermal-structural simulation engines. Those statements are correct for current runtime capability and remain
unchanged. This section exists so that the truthful exclusion does NOT become an accidental permanent omission: it
preserves one governed future path for thermal capability, with existing owners kept authoritative for their parts.

**Four-way distinction (binding; these MUST NOT be conflated).**
1. **Thermal consideration / advisory** — temperature and heat as advisory inputs, constraints, and assumptions;
   warnings when thermal information is missing. **Existing owner: CAP-13** (heat among its recorded assumption
   inputs; the *Heat and pressure* mandatory warning category; `UNABLE TO RECOMMEND` on insufficient temperature/
   environment inputs), within CAP-12's evidence boundaries. Already covered; unchanged here; CAP-13 owns advisory
   consumption WITHOUT thereby owning any solver.
2. **Thermal analysis** — governed calculation or estimation of thermal behavior (heat-source/heat-generation
   reasoning; heat-transfer reasoning; temperature-rise and thermal-margin estimation). A **producer** capability that
   NO existing record explicitly owns. It is preserved HERE as a future feasibility subject which, if ever pursued,
   rides the EXISTING future deterministic-calculation adapter gate lineage (P9-QS §13, reference-only, deliberately
   unnumbered) together with Units & Dimensional Integrity (P9-QS §12) — no second calculation framework is created,
   and §1A exclusion 2's rule stands: only a narrowly bounded deterministic calculation is even eligible, and only
   under separate evidence, contract, and owner authorization.
3. **Thermal simulation** — numerical thermal modeling (CFD, conjugate heat transfer, spatial temperature
   distribution, transient simulation). This REMAINS inside §1A legacy exclusions 1–2 as an intentional risk control —
   **excluded by default**. §1A already carried a GENERIC revisit permission for its exclusions (revisitable only
   under separate evidence, contract, and owner authorization); what this section adds is the **explicit
   thermal-specific preservation and feasibility path** — the mandatory thermal feasibility/contract gate below —
   through which (and only through which, with explicit Owner authorization) that generic permission may ever be
   exercised for thermal simulation. Thermal simulation is preserved as a feasibility question DISTINCT from thermal
   analysis and is never implied by it.
4. **Physical validation** — measurements, sensors, thermal testing, prototype validation. **Existing owner:
   WS-PFV-001**, unchanged. Relationship: future thermal analysis/simulation (if ever implemented) would produce
   governed SOFTWARE evidence; WS-PFV-001 may validate that evidence PHYSICALLY; the two responsibilities are never
   merged.

**Consumers (dependency references only; nothing absorbed).** **CAP-13** = advisory/specification consumer of thermal
evidence (never a solver). **CAP-12** = consumer of thermal evidence for material selection, manufacturing
recommendation, and prototype feasibility (its non-goals — no thermal-suitability claim without required evidence —
unchanged). **D4** (`D-GMPR-01-D-D4` + Amendment 01) = the eventual SYSTEM-LEVEL cross-domain consumer/coordinator
where thermal behavior becomes a cross-domain compatibility concern (electronics heat vs enclosure; component heat vs
material; cooling vs mechanical packaging; thermal expansion vs fit/tolerance; battery/power vs heat) — referenced
only; D4 remains REGISTERED / NOT AUTHORIZED and is not invoked here. **Completeness note:** ADR-002's
`THERMAL_MANAGEMENT` entry is a future gap-taxonomy CONCEPT for a hypothetical child domain (a question/gap-type idea,
not an analysis capability); it is NOT a thermal-analysis owner and is unchanged by this section.

**Preserved future boundary.** Subject to the feasibility gate below and separate authorization, a future governed
thermal capability MAY include (future feasibility subjects — promised to be CONSIDERED, never promised to be
implemented): heat-source/heat-generation reasoning; steady-state thermal estimation; transient thermal behavior where
feasible; temperature rise; thermal margin; heat-transfer paths; conduction; convection; radiation when relevant;
cooling requirements; interface thermal resistance where supportable; ambient/environment effects; thermal constraints
on materials/components; interaction with Mechanical / Electronics / materials / enclosure decisions; explicit Known
Unknowns; confidence/evidence boundaries; and mandatory specialist or physical validation where software inference is
insufficient.

**Present-capability truthfulness (binding).** Current InventorAI does NOT perform governed thermal simulation, thermal
analysis, or temperature/heat prediction. The Mechanical P9-MECH-I1 NOT-COVERED status remains truthful and unchanged.
Registration here creates NO runtime capability, does NOT qualify Mechanical, does NOT activate Mechanical, and changes
no declaration. No calculated thermal result may ever be presented as certified engineering truth without the required
future evidence and validation; no CFD / FEA / solver capability is implied unless separately implemented and validated
under the gate below.

**Mandatory future thermal feasibility/contract gate (required before ANY thermal implementation).** A separate,
Owner-authorized gate MUST determine at minimum: whether the capability should be rule-based, equation-based,
numerical-solver-based, external-tool-assisted, or hybrid; supported thermal problem classes; required physical inputs;
units and dimensional consistency (P9-QS §12); material-property sources (governed source/licensing review — the same
boundary class as CAP-12/CAP-13); boundary conditions; heat-transfer coefficients; geometry requirements; uncertainty
treatment; validation datasets; acceptable error bounds; specialist-review requirements; regulatory/safety
implications; whether CFD/FEA-style computation is justified at all (the §1A exclusion revisit decision); compute/
performance cost; security implications of any external solver/tool; and failure / `UNABLE TO DETERMINE` behavior.
**No implementation architecture is pre-authorized.**

**Non-authorization (restated for this section).** Registration is not implementation authorization (R5); every future
implementation requires the full R6 gated chain. This section does not alter Mechanical P9-QS status, qualification, or
activation; does not touch `_ACTIVATED_DOMAINS`, runtime, domain packs, classifier, registry, questions, or the safety
family; does not close CF-6, CF-2, or the D-GMPR coupling; does not authorize D4; does not alter D8; and does not
authorize Phase 10, PSRR, or deployment.

---

## L2SC-01 — Layer-2 Scoring-Correction Domain-Scope Completeness (anti-forgetting; pre-second-domain-activation residual; NON-ACTIVATING)

Registered inside the CF-2 full-remainder reconstruction gate (canonical record:
`docs/governance/CF2_CLI_REMAINDER_TRUTHFULNESS_CONTRACT.md` §7; base
`5355ed54cbba17c16b5716865c1dc82e8b141941`). Deliberately NON-NUMERIC designation (mirroring the `THERM-01`
precedent) so no pre-existing numeric register cross-reference can resolve to it; NO new CAP entry —
CAP-01…CAP-18 unchanged.

**Finding.** `engine/progression_loop.py:415` (the "Layer-2 bounded scoring correction," Owner-authorized
2026-07-11) requires an electronics/electrical domain substance signal (whole-word match, same sentence as a
qualifying causal connective) before its specific scoring bonus applies. This is internal scoring logic — never
rendered to any user or operator — independently confirmed NOT a CF-2 public-message-truthfulness matter and NOT
a CF-6 classifier/activation-admission-consistency matter (CF-6 is `FULLY DISCHARGED` and is not reopened by
this registration).

**Why this matters (anti-forgetting only).** If/when a second domain is ever Owner-activated, ideas in that
domain would never benefit from this specific Layer-2 scoring correction — a scoring-completeness gap for future
domains, distinct from any admission/truthfulness concern. This registration exists ONLY so the gap is not
silently forgotten before any future second-domain-activation readiness review; it creates no obligation to act
now.

**Non-authorization (restated for this section).** Registration is not implementation authorization. This
section authorizes NO scoring-logic change, NO Layer-2 rule generalization, NO Mechanical (or any other domain)
extension of the correction, and does not alter Mechanical P9-QS status, qualification, or activation; does not
touch `_ACTIVATED_DOMAINS`, runtime, domain packs, classifier, registry, questions, or the safety family; does
not close or reopen CF-6; does not close CF-2; does not touch the D-GMPR coupling; does not authorize D4; does
not alter D8; and does not authorize Phase 10, PSRR, or deployment. Any future work on this item requires its
own separately authorized, bounded gate.

**Reconstruction Amendment (L2SC-01 Bounded Contract gate, base `c8e7af24adf2cee31104abc9c810d38e05569c52`).**
The original Finding above is preserved verbatim above — it accurately reflected what was known at registration
time. A dedicated read-only reconstruction gate has since traced the exact code and empirically confirmed a MORE
PRECISE finding, which supersedes the original Finding's framing without erasing it: **the Layer-2 correction's
substance-signal lookup (`engine.domain_rules.get_substance_signals(domain)`) is ALREADY fully domain-generic,
not electronics-specific** — it reads each domain's own registry-owned `substance_signals`, and Mechanical's
pack already carries 15 populated signals that already receive the correction correctly in singular form. The
CONFIRMED, narrow, externally-meaningful gap is specifically the hardcoded, electronics-only 8-pair
`_SUBSTANCE_PLURAL_ALIASES` map inside `engine/progression_loop.py`: a Mechanical response relying solely on a
new causal connective plus a PLURAL-only substance word can receive `ASSERTED` where its singular equivalent
receives `REASONED` — reproduced end-to-end through the real gap-closure state machine as a genuine
`WARN`-vs-`PASS` divergence. This amendment does not implement anything; L2SC-01 itself remains OPEN.

**Independent-review correction note.** A first bounded contract candidate (`219f7c10c4ba23f795f0461dd831f71052469e65`)
proposing 9 authorized Mechanical plural aliases was **REJECTED by independent external review** (verdict:
MATERIAL CORRECTION REQUIRED, defect MD-1 — the candidate authorized aliases using "is this the grammatically
normal plural?" alone, without screening for verb-form/idiom/meaning-shift false-positive risk; demonstrated
examples: "the gasket seals the joint", "the latch springs open", "the operator loses their bearings", "the
plant gears up"). That candidate is preserved immutable, unpushed, at
`refs/rejected/l2sc01-plural-alias-contract-219f7c1` and is NOT amended or built upon. A corrected contract,
applying a stricter alias-safety criterion, authorizes only **3** of the 15 Mechanical signals for plural
aliasing (`piston`, `valve`, `actuator`) — narrower than the rejected candidate's 9 — with the remaining 12
explicitly excluded on verb-form/idiom/mass-noun/meaning-shift grounds. Current canonical record:
`docs/governance/L2SC01_SUBSTANCE_SIGNAL_PLURAL_ALIAS_INCREMENT_CONTRACT.md`.

**Runtime implementation note.** The frozen contract above has since been Owner-authorized for runtime
implementation (base `c1cb421d73c53d24cc381ca9238e29613ca7e996`, PR #496) and implemented exactly as frozen —
see `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` for the full implementation record. The engine-hardcoded
`_SUBSTANCE_PLURAL_ALIASES` map described above no longer exists; plural-alias data now lives exclusively in
each domain pack's own `substance_signal_plural_aliases` field, read via
`engine.domain_rules.get_substance_signal_plural_aliases(domain)`. **`L2SC-01` is NOT formally closed by this
implementation candidate** — closure remains a separate, later determination against the contract's own closure
criteria (§15).

**Runtime implementation correction note (defect MD-A).** The implementation candidate referenced above,
`714d538fca7b22cb84e3b18802dcf27aa42e5707`, was **REJECTED by independent external review** — not for a runtime
defect (the runtime implementation was independently reconfirmed correct) but because the mandated MD-1
recurrence guard (§12.D of the frozen contract) was not load-bearing: 10 of its 12 rejected-alias adversarial
test sentences placed the alias word on the directional side of the connective the Layer-2 gate never inspects,
so those guards passed irrespective of alias state. That candidate is preserved immutable, unpushed, at
`refs/rejected/l2sc01-runtime-impl-714d538`. A corrected candidate reapplies the runtime/data changes
byte-identically (verified) and replaces only the defective test sentences with direction-correct constructions
plus an explicit poisoned-map/neutral-control differential proof. **`L2SC-01` remains OPEN** — not closed by
either candidate.

## L2SC-02 — Whole-Word Substance-Matcher Multi-Word-Signal Limitation (anti-forgetting; NON-ACTIVATING; NOT a Mechanical-activation blocker)

Registered inside the L2SC-01 Bounded Contract gate (canonical record:
`docs/governance/L2SC01_SUBSTANCE_SIGNAL_PLURAL_ALIAS_INCREMENT_CONTRACT.md` §16 and its preceding, rejected-and-
corrected predecessor; base `c8e7af24adf2cee31104abc9c810d38e05569c52`). Deliberately NON-NUMERIC-prefixed,
grouped in the same `L2SC` family as `L2SC-01` (same underlying `engine.progression_loop._has_whole_word_
substance` matching mechanism), with its own `-02` suffix so it is separately trackable and never conflated with
`L2SC-01`'s own (distinct) plural-alias gap. NO new CAP entry — CAP-01…CAP-18 unchanged.

**Finding.** The Layer-2 causal-connective substance-signal matcher tokenizes on single alphanumeric runs
(`_SUBSTANCE_WORD_RE = re.compile(r"[a-z0-9]+")`) and checks single-token membership. A domain-pack
`substance_signals` entry whose `signal` value is itself MULTIPLE words (confirmed: `software`'s
`"static analysis"`) can never match this whole-word check, in singular or plural form, for ANY domain that has
such a signal. **`mechanical` has ZERO multi-word substance signals** (independently verified) — this finding
does NOT affect Mechanical activation-readiness and is explicitly NOT a component of `L2SC-01`'s bounded
implementation scope.

**Why this matters (anti-forgetting only).** If a future domain pack (or a future edit to an existing pack, e.g.
`software`) relies on a multi-word substance signal reaching a REASONED classification through the Layer-2 gate,
that signal will silently never qualify via this path (though it may still qualify via the pre-existing,
domain-neutral `_CAUSAL_STRUCTURE_PATTERNS` path, which is unaffected). This registration exists only so the
limitation is not forgotten if/when `software` (or any future multi-word-signal domain) becomes activation-
relevant; it creates no obligation to act now and is independent of Mechanical's own activation timeline.

**Non-authorization (restated for this section).** Registration is not implementation authorization. This
section authorizes NO matcher change, NO multi-word tokenization support, NO Mechanical (or any other domain)
data change, and does not alter Mechanical P9-QS status, qualification, or activation; does not touch
`_ACTIVATED_DOMAINS`, runtime, domain packs, classifier, registry, questions, or the safety family; does not
close or reopen CF-6 or CF-2; does not touch `L2SC-01`'s own scope or its bounded contract; does not authorize
D4; does not alter D8; and does not authorize Phase 10, PSRR, or deployment. Any future work on this item
requires its own separately authorized, bounded gate.

## L10N-RH-01 — Pre-Mechanical-Activation Localization Regression-Hardening Residual (anti-forgetting; pre-second-domain-activation residual; NON-ACTIVATING)

Registered inside the CF-2 formal closure gate (canonical record:
`docs/governance/CF2_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md` §5/§7; base
`6c168a62df4754c0ecea7e99ff6316b66c6dfdb7`). Deliberately NON-NUMERIC designation (mirroring the `THERM-01`/
`L2SC-01` precedent) so no pre-existing numeric register cross-reference can resolve to it; NO new CAP entry —
CAP-01…CAP-18 unchanged.

**Finding.** The CF-2 Arabic Localization Remainder Fast Track candidate's independent external review returned
**ACCEPT WITH NON-BLOCKING OBSERVATIONS** (no material defect; current shipped Arabic copy independently
confirmed truthful) but raised three related future-facing observations, none of which is a current-behavior
defect:

1. **Arabic broadened-activation negative-semantic-guard gap.** A reviewer mutation that flipped the
   broadened-activation (2+ specialist domains) Arabic copy into a false electronics-only claim survived the
   current full test suite. Current shipped Arabic copy for this state was independently re-inspected and
   confirmed correct — this is a test-COVERAGE gap (the suite does not yet catch that specific class of
   regression), not a behavior defect.
2. **`SERVICE_UNAVAILABLE` localization-path regression-guard gap.** A mutation bypassing the canonical
   `ui_text.localize_message()` helper at the `SERVICE_UNAVAILABLE_MESSAGE` call sites (`web/app.py`) survived
   both the focused and full test suite. Current wiring was independently inspected and confirmed correct — same
   class of gap as (1).
3. **Present-confirm Arabic checkbox-label wording.** The Arabic present-confirm checkbox
   (`start_present_confirm_label`, broadened-activation branch) reuses prompt-style wording rather than a
   first-person consent affirmation. Content remains truthful; English behavior is correct and unaffected; this
   path is NOT production-reachable under today's real `['electronics_electrical']`-only activation state (it
   requires 2+ activated domains, exercised only via a bounded test double today).

**Why this matters (anti-forgetting only).** All three observations concern states that are either currently
unreachable in production (broadened/empty activation, present-confirm under 2+ domains) or a test-suite
strength gap rather than a shipped defect. If/when a second domain is ever Owner-activated, these states become
genuinely reachable for the first time, and (1)/(2)'s weaker regression coverage and (3)'s wording nuance become
worth reassessing before or alongside that activation. This registration exists ONLY so these three related,
already-identified, non-blocking items are not silently forgotten before any future second-domain-activation
readiness review; it creates no obligation to act now, and none of the three blocked CF-2's own closure (see
`CF2_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md` §5).

**Non-authorization (restated for this section).** Registration is not implementation authorization. This
section authorizes NO test-hardening implementation, NO wording change to any Arabic or English string, NO
Mechanical (or any other domain) activation, and does not alter Mechanical P9-QS status, qualification, or
activation; does not touch `_ACTIVATED_DOMAINS`, runtime, domain packs, classifier, registry, questions, or the
safety family; does not close or reopen CF-6; does not reopen CF-2 (closed by the same gate that registers this
item — see `CF2_FULL_SCOPE_FORMAL_CLOSURE_RECORD.md`); does not touch `D-CF6CF2-ILT002-01`, `L2SC-01`, or the
Tier-1 label; does not authorize D4; does not alter D8; and does not authorize Phase 10, PSRR, or deployment.
Any future work on this item requires its own separately authorized, bounded gate.
