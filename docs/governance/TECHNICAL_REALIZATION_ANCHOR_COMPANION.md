# TECHNICAL REALIZATION ANCHOR COMPANION

STATUS: APPROVED AND FINAL — Level 1 companion (target architecture and lane-gating authority), in force as a governance constraint. Authorizes no implementation and activates no lane; the §0 activation sequence remains required.
AUTHORITY LEVEL: Level 1 companion to the Level 0 owner identity correction.

DERIVES AUTHORITY FROM (and remains subordinate to; creates no independent
product identity or path authority):
- `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md` — governing product
  identity;
- `docs/governance/DUAL_PATH_PRODUCT_ANCHOR.md` — governing dual-mode (Path N /
  Path T) authority.

EXECUTION-COORDINATION / LANE-GATING CONTEXT (NOT a source from which this
Level 1 companion derives authority):
- `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` — records execution lanes, the
  current lane, and the next governed step.

---

## 0. Non-authorization clause (binding)

This companion is **target architecture and lane-gating authority only**. It
authorizes no implementation, no generation, no Path T activation, no
multi-domain runtime orchestration, no accounts/collaboration, and no change to
any hold or closed state.

**Every bounded implementation lane requires ALL of:**
1. a separate per-lane authorization document;
2. explicit owner approval;
3. transition of each required document to its required non-DRAFT final status,
   and commit of that final status to the authoritative repository;
4. all prerequisite authority and architecture documents approved and committed
   in their required final status;
5. all declared activation prerequisites satisfied;
6. no unresolved governance or authority blocker;
7. the final roadmap state update (ACTIVE_EXECUTION_ROADMAP §§4–7) committed to
   record the lane as active.

A document committed while its governing status remains `DRAFT` does **not**
satisfy activation. A working-tree draft, an owner conversation, or an
uncommitted owner instruction **never** activates this companion or any lane.
"Commit to the authoritative repository" means the specific required final-status
commit of that document — not any generic or unrelated commit. Until all
activation conditions are met, the prior governance state and next authorized
action remain unchanged. Recognition of a technology, capability, or option by
any model never implies it is supported or authorized.

## 1. One product, one logical project-identity model

InventorAI is **one product** with **one logical project-identity model** (a
target architectural invariant — one project identity per project), **one shared
capability layer**, and **one shared evidence/artifact/provenance model**.

This is a target invariant, NOT a claim that a stable project identity or
project record is already implemented. Current committed runtime evidence must
be distinguished from target architecture: stable project identity and the
project record are **target architecture, not current implementation**. A
current session/idea identifier must not be represented as the future stable
project identity without explicit migration and committed evidence.

Participants are **not** permanently classified as technical or non-technical;
expertise is per-domain and per-task. A single project may begin with a
participant using Orchestrated Idea Mode, receive specialist technical
contributions, and return to that participant **within the same project record**
(target architecture) — never copied into a separate product, engine, project
record, or artifact system.

## 2. Technical Realization is the shared capability layer

Technical Realization (TR) is the **shared governed technical-capability layer**
of the one product. It is **not** permanently or exclusively subordinate to
Orchestrated Idea Mode (internal "Path N").

- The **only invocation direction eligible for future bounded authorization**
  under the current product direction is Orchestrated Idea Mode downstream of
  FDC-001, within separately authorized bounded lanes.
- **Future** Direct Technical Work Mode (internal "Path T") and specialist
  contribution may invoke the **same** layer **only when separately authorized**;
  both remain blocked/deferred now.

No invocation or lane is active merely because this companion exists, is
approved, or is committed; the complete §0 activation sequence remains required.
When implemented, the governed capability must use **one shared implementation**
invoked by interaction mode + permissions + guidance — **never duplicated
technical truth**.

## 3. Adaptive internal work modes

- **Orchestrated Idea Mode** (internal "Path N"): the platform leads —
  plain-language intake, capability disclosure, requirement translation, and
  supported technical work **performed only within separately authorized bounded
  lanes**. **Primary current direction.** Multi-domain runtime orchestration
  remains unauthorized; the proposed first bounded lane eligible for future
  authorization is single-domain (electronics) and remains inactive until the
  complete §0 activation sequence is satisfied.
- **Direct Technical Work Mode** (internal "Path T"): a domain-knowledgeable
  participant works directly within a supported domain. **BLOCKED for
  implementation. This companion does not unblock it.** The architecture must
  merely not foreclose it.

"Path N" / "Path T" are **internal governance labels**, not user-facing product
labels.

## 4. User-facing visibility rule

Deferred or blocked modes (including Direct Technical Work Mode) **must not be
displayed in the user interface** — not even as "coming later" — until ALL of:
(1) explicitly authorized; (2) backed by at least one useful supported technical
capability; (3) permissions and evidence rules implemented; (4) project/artifact
integration verified; and gated behind an explicit feature flag. Existence in
target architecture is **not** grounds to display a mode. Current user-facing
entry points are limited to actions that are implemented, supported, authorized
in the current lane, not blocked or stale, and whose required prerequisites are
satisfied.

## 5. Technical Realization (TR) operating constraints

Within an activated bounded lane, TR:
- performs only the exact operations and produces only the exact artifact that
  the activated per-lane authorization declares;
- attaches provenance and evidence status to every output (see the Evidence and
  Artifact Model);
- never asserts assembled / operated / demonstrated / production-ready /
  certified without corresponding evidence;
- obeys the source-of-truth rule (a value from model memory alone is never
  promoted to verified fact, calculation, selection, frozen configuration, or
  safety conclusion).

## 6. One coherent project storage architecture (target; mostly not yet built)

One coherent architecture composed of **separate bounded stores connected by
shared project-identity references** (detailed in the Path N Orchestration and
Handoff Contract):
- **session store** — conversation, assessment, current readiness, active
  workflow state;
- **project record** — *future* stable project identity, ownership references,
  lifecycle, artifact references (target architecture; not yet implemented);
- **artifact store** — *future* versioned decisions, technical artifacts,
  provenance, calculations, generated files, tool results, test evidence,
  revisions;
- **file/blob storage** — *future* larger generated/uploaded files.

These are **not merged into one schema**; they are unified by shared references
and one coherent technical truth. The project record, artifact store, and blob
storage are **target architecture, not yet implemented**, and a current
session/idea identifier is distinct from any durable session store.

Session-persistence current reality: a paused, uncommitted session-persistence
implementation draft exists in the current working tree as
`inventorai-session-persist-v1`. It is defect-bearing, not delivered, not active
authority, and **not evidence of an approved durable-session capability**.
Persistence disposition: **PRESERVE UNMODIFIED AND PAUSE**; its two known defects
remain mandatory pre-delivery corrections; no persistence change is authorized
here.

## 7. Companion document set (read alongside this companion)

This companion is read alongside, and governs the consistency of:
1. the append-only `MVP_SCOPE_FREEZE.md` Amendment 1 carve-out;
2. `docs/governance/PATH_N_ORCHESTRATION_AND_HANDOFF_CONTRACT.md`;
3. `docs/governance/SUPPORTED_TECHNOLOGY_AND_SOURCE_OF_TRUTH_CONTRACT.md`;
4. `docs/governance/TECHNICAL_REALIZATION_EVIDENCE_AND_ARTIFACT_MODEL.md`;
5. the append-only bounded amendment to `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`;
6. the first-lane authorization, `docs/governance/FIRST_LANE_AUTHORIZATION_ADAPTIVE_IDEA_ORCHESTRATION.md`.

## 8. Preserved closed states and holds (unchanged)

R2 = HELD · FORM T = BLOCKED · S-6 = UNCLASSIFIED · AA-3 = BLOCKED ·
AA-4 = BLOCKED · AA-5 = BLOCKED · Phase 5 = UNAUTHORIZED · Phase 6 = UNAUTHORIZED ·
ILT-002 evidence collection = NOT AUTHORIZED · Path T = BLOCKED ·
Phase 4 = CLOSED · Gate 8 = CLOSED · runtime_integrated = TRUE.
None are reopened or modified by this companion.

## 9. Recorded future product direction — Preliminary Component / Prototype Realization & Engineering Handoff (Owner working label "T6"; NOT AUTHORIZED)

**Additive recording, 2026-10-04 (Owner-authorized documentation sync).** This section records a future product direction for the EXISTING Technical Realization layer (§2). It changes nothing above: §0 applies in full, no lane is activated, no implementation, generation, calculation, selection, store, schema, lifecycle or user-facing entry point is authorized, and every hold in §8 stands. "T6" is handover / navigation shorthand only — it is NOT a Master Roadmap Stage, NOT a Stage-28 subitem (`28-T6` does not exist), NOT a domain and NOT a Capability Register number. The direction is a cross-capability realization / composition direction, NOT a technical authority.

**9.1 Intended future flow.** Invention idea → functional decomposition → provisional technical participation → eligibility / authorization check → bounded technical-owner contributions → subsystem / component identities → interfaces → attributed technical contributions → ONE coherent preliminary realization package → later engineering-tool handoff. Participating technical owners contribute only where qualified and authorized; the future Stage-28 technical subitems (28-T1…28-T5, Master Roadmap §6 Stage F) are NOT prerequisites of this direction's core proof.

**9.2 What Technical Realization may do here.** Compose references to owner-produced contributions; expose missing engineering information; expose conflicting assumptions; show unresolved items; derive coherent user views; prepare structured engineering intent for a future handoff.

**9.3 What Technical Realization must NOT itself do.** Calculate; select; size; rate; dimension; validate; certify; determine safety; declare compatibility; invent missing technical truth. Canonical technical truth stays with its proper owner and is consumed by reference (Master Roadmap §8C A–C).

**9.4 Components across technologies.** The future product must support project components across technologies, not only electronics — e.g. Mechanical (gear, shaft, bearing, spring, pulley, belt, bracket, fastener, enclosure / housing, coupling), Electrical / Electronic (resistor, capacitor, transistor, MOSFET, IC, MCU, relay, sensor, battery, connector, power supply) and Motion (motor, actuator, driver). These examples are illustrative only: they are NOT a component library and NOT an authoritative taxonomy, and none is created by this recording.

**9.5 Component truth boundary.** Four meanings stay distinct and are never collapsed into one linear status: (A) whether an item is included in the project; (B) its provenance; (C) its technical support; (D) validation / evidence of particular claims. A participant may accept that a component exists while its size, rating, material, compatibility, safety and technical suitability remain unresolved or unvalidated. "Gear required" does not imply gear type, module, teeth count, diameter, material or suitability; "Resistor required" does not imply a value or power rating. The Evidence and Artifact Model §11 maps these meanings onto its existing independent dimensions; no new permanent enum is created by this recording.

**9.6 Candidate / confirmation boundary.** Owner-declared component; system-proposed component candidate; Owner-confirmed / accepted component; technically supported contribution; evidence / validation — five distinct meanings. A system-proposed candidate is never automatically canonical project truth. A confirmation must identify what is actually accepted: confirming "this is a gear" does not silently confirm diameter, teeth count, material, load capability or manufacturing suitability. Text-derived candidates and future CAP-14 visual candidates should eventually share consistent confirmation semantics while keeping distinct provenance; that seam is not implemented or authorized here.

**9.7 One physical component, many contributions.** ONE physical project component may carry MANY attributed technical contributions (e.g. one motor: Mechanical load, Electrical drive, Embedded execution, Control). That never creates several physical motors, and there is no separate Mechatronics component registry, Robotics component registry or domain-specific BOM store — the component / BOM architecture is shared and cross-domain. Not every contribution is a physical BOM row: firmware, control logic, a communication requirement, a calculation result or an interface condition may belong in the coherent engineering package without becoming a fictitious purchased component.

**9.8 Preliminary technical values / sizing — authority chain.** Technical requirement → responsible technical authority → explicit inputs → authorized method → attributed bounded result / range → assumptions / limitations / verification needs → Technical Realization projection. Technical Realization never calculates independently; no numerical result appears merely because it looks plausible; a range also requires technical support; when critical inputs are missing, the missing input / calculation requirement is shown and no value is invented. Illustrative subjects only — Mechanical (gear ratio, teeth count, module / pitch, diameter, shaft size, bearing class, spring characteristic, tolerance), Electrical (resistance, capacitance, voltage / current rating, transistor / MOSFET characteristics, power-supply requirement, connector / conductor requirement), Sensors (range, resolution, accuracy, sampling rate). No calculation is authorized by this recording.

**9.9 Preliminary engineering package.** Target: ONE coherent DERIVED preliminary engineering / realization package whose possible projections include component architecture, preliminary BOM, Make / Buy, Mechanical build view, Electrical / wiring view, interfaces, manufacturing view, assembly / prototype plan, unresolved inputs, required calculations, validation / verification requirements and a future engineering-tool handoff. ONE coherent package does NOT mean ONE central owner of engineering truth: the package composes references to the proper owners. The current BOM is not persisted as an independent editable truth source; no generic engineering ontology, generic component database, generic artifact platform, generic orchestration engine or duplicate evidence system is created.

**9.10 Make / Buy, supplier and COTS boundary.** Technical requirement → admissible candidate class → optional supplier / catalog match → suitability assessment for the specific candidate → explicit user selection. A supplier listing is NOT technical evidence; price is NOT technical evidence; availability is NOT technical validation; membership of the correct general catalog category does not prove that an item satisfies the engineering requirements. Supplier / procurement / ordering workflow stays outside core InventorAI unless separately authorized (Capability Register §1A). CAP-12 remains the future owner of its bounded prototype material / process / make-buy advisory where authorized.

**9.11 External engineering-tool boundary.** Technical Realization composes structured engineering intent. The Master Roadmap §8B / Stage 36 direction and the Phase-7 export / adapter boundaries own target-specific mapping, adapter behaviour, transport, tool compatibility, provider-neutral integration and consent / access / commercial execution where applicable — future examples: CAD, PCB / EDA, CAE / simulation, PLC engineering tools and other specialist engineering systems; no provider is selected. API / tool transport is not moved into Technical Realization, and nothing here implies current automatic CAD generation, automatic PCB generation or autonomous manufacturing-file generation. The return path obeys the Evidence and Artifact Model §11.4: TOOL RESULT RECEIVED ≠ EVIDENCE ADMITTED ≠ CLAIM ASSESSED / VALIDATED.

**9.12 Product honesty.** InventorAI helps move an inventor substantially closer to a realizable prototype; it does NOT claim to produce a guaranteed final engineered product. Future realization output stays visibly PRELIMINARY, ADVISORY and NON-BINDING where applicable, and preserves meanings such as unresolved input, calculation required, validation required, specialist review required, external tool verification required and unable to determine — meanings to preserve, not a new stored enum. No universal `FEASIBLE / IMPOSSIBLE` engine exists or is created; a plausible engineering path, unresolved feasibility, supported feasibility within a defined scope, safety, production readiness and certification stay distinct (Evidence and Artifact Model §6–§7).
