# INVENTORAI — PROJECT STATE FREEZE v1.2

**Date:** 2026-05-29
**Prepared by:** Claude Sonnet 4.6 — Validation Lead
**Repository:** https://github.com/Amirjaferali/inventorai (private)
**Branch / HEAD:** main / 3f3a707
**Location:** docs/governance/INVENTORAI_PROJECT_STATE_FREEZE_v1.2.md

---

> **IMPORTANT:** This document supersedes all prior session notes. A new agent receiving only this document should be fully oriented without requiring access to prior conversation history. This is the primary governance baseline for the InventorAI project. `ARCHITECTURE_GUARDRAILS.md` and `MVP_SCOPE_FREEZE.md` are narrower-scope documents that are subordinate to this file.

---

## Changelog

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-05-29 | Initial document — validation campaign, findings, capabilities, foundation assessment |
| v1.1 | 2026-05-29 | Added Section 11 — Vision Governance Principles (Inventor Ownership, Improvement Not Generation, Multi-Domain Integration) |
| v1.2 | 2026-05-29 | Added GD-001 — Three-Stage Inventor Journey Architecture to Section 12 and Section 16 |

---

## Section 1 — Original Product Vision

InventorAI is a deterministic invention progression platform. It takes an inventor's idea description and guides them through a structured questioning process designed to reveal whether they genuinely understand the mechanism behind their invention.

The platform makes one narrow claim: this inventor has demonstrated, through their own expressed reasoning, that they can articulate the mechanism behind their idea at a quality level the protocol defines as sufficient for the current stage.

The platform does not evaluate whether an idea is good, feasible, commercially viable, or patentable. It evaluates one thing only: whether the inventor can articulate, in their own words, the causal mechanism by which their invention works.

### Intended Full Journey

- Idea Entry
- Domain Discovery — classify invention into electronics / mechanical / medical / software
- Gap Discovery — identify MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY
- Guided Completion — quality-gated questioning until each gap is closed
- External Work Identification — what the inventor must do outside the platform
- Validation Requirements — what external validation the invention requires
- Component and Material Suggestions — backed by ODS-001 Options Database
- FDC-001 Deliverable — structured report reflecting what the inventor proved

### Intended Maturity Progression

- LEVEL 0 — Initial idea, no mechanism articulated
- LEVEL 1 — Mechanism articulated, problem established
- LEVEL 2 — Mechanism, feasibility, and boundaries articulated — eligible for FDC-001

---

## Section 2 — Current Product Reality

> **The current platform is best described as: an Idea Structuring Tool.** It presents structured questions about mechanism. It does not currently enforce that those questions are answered at a sufficient quality level before the session ends.

### What the Platform Currently Does

- Accepts an idea description and classifies it into a domain (electronics/electrical validated)
- Presents structured gap questions with honest causal framing
- Classifies inventor responses as ASSERTED / REASONED / DEMONSTRATED
- Advances session stage on a fixed 3-iteration schedule
- Displays honest disclosure text about platform limitations
- Ends every session after 3 iterations with the same completion message

### What the Platform Does Not Currently Do

- Gate completion on response quality — weak responses advance the session identically to strong responses
- Close gaps when they are satisfied — gap labels remain ACTIVE at session completion
- Open the second or third gap — PHYSICAL_FEASIBILITY and BOUNDARY_AMBIGUITY were never observed in any live session
- Produce an FDC-001 deliverable — no live session generated a structured report
- Differentiate the inventor experience based on demonstrated quality
- Fire stall detection — STALL_THRESHOLD=3 does not activate in live sessions
- Identify external work requirements or validation requirements

### The Honest Minimum Claim

> The platform can reliably classify an electronics invention description into a domain and present a structured set of questions about its mechanism. The causal reasoning classifier correctly distinguishes assertion from reasoning. The disclosure layer correctly sets expectations.

### The Misleading Maximum Claim

> Any claim that the platform evaluates whether an inventor understands their invention is currently unsupported. Completion is triggered by iteration count, not demonstrated quality. Stage advancement is cosmetic, not earned.

---

## Section 3 — Validation Campaign Summary

Five synthetic sessions were run as part of the Disclosure Validation Campaign. Each session targeted a specific risk. The campaign was conducted under strict evidence collection discipline with no interpretation during execution.

| Session | Summary |
|---|---|
| A | Pure assertion test. Idea: IoT water leak sensor with microcontroller. Response: It detects water and sends a signal. Result: PASS — ASSERTED correctly, no advancement. Produced D-001, D-002. |
| B | ADR-004 false-positive guard test. Idea: IoT sensor for detecting water leaks using a microcontroller. Response: The sensor detects water and sends a signal to the phone using wifi. Result: PASS — ASSERTED correctly despite substance signal vocabulary. Confirmed D-001, D-002. |
| C | False-negative test + unexpected completion finding. Idea: Water leak detector using copper electrodes and microcontroller circuit. Response 1 (causal): advanced to Stage 2 — PASS. Response 2: It monitors somehow. — advanced to Stage 3 and declared completion — FAIL. Produced D-005. |
| D | Stall detection test. Idea: Smart home temperature monitor with sensor circuit. Submitted "It monitors temperature somehow." three times. Result: FAIL — no stall detection, no reframe, session continued normally. Produced D-006. |
| E | Full progression test. Idea: Soil moisture sensor for agricultural IoT using capacitive sensing with ESP32. High-quality causal responses submitted. Result: PASS on progression quality, FAIL on completion governance — Stage 3 reached on iteration 3 regardless of quality. Confirmed D-004, D-005. |

---

## Section 4 — Confirmed Findings

Evidence-backed defects reproduced during live validation sessions.

| ID | Severity | Category | Product Impact | Description | Sessions | Reproducible | Fix Phase |
|---|---|---|---|---|---|---|---|
| D-001 | MEDIUM | DISCLOSURE | VALIDATION ONLY | Internal constant MECHANISM_COMPLETENESS leaked in inventor-facing status text | A, B, D | Y | Post-validation |
| D-002 | LOW | DISCLOSURE | VALIDATION ONLY | Internal constant PROGRESSING leaked in Direction field of status text | A, B, C, D, E | Y | Post-validation |
| D-003 | MEDIUM | DISCLOSURE | POST-MVP | Domain classification fails on natural English invention descriptions lacking signal vocabulary | Pre-A, C-attempt | Y | Post-MVP |
| D-004 | LOW | DISCLOSURE | VALIDATION ONLY | electronics_electrical domain constant visible in inventor-facing metadata bar | C, E | Y | Post-validation |
| D-005 | CRITICAL | PROGRESSION + STATE | MVP BLOCKER | Session declares completion after 3 iterations regardless of response quality. Gap remains ACTIVE. Violation of Principle 1 (Inventor Ownership). | C, E | Y | Pre-ILT-001 |
| D-006 | CRITICAL | PROGRESSION | ILT-001 BLOCKER | Stall detection does not fire after 3 identical weak responses. STALL_THRESHOLD=3 defined in code but not active in live sessions. | D | Y | Pre-ILT-001 |

---

## Section 5 — Review Risks

| ID | Severity | Category | Product Impact | Description | Promotion Condition |
|---|---|---|---|---|---|
| R-001 | MEDIUM | STATE | POST-MVP | infer_domain() has no ADR, no accuracy baseline, no tie-breaking test. | Live session produces wrong domain classification |
| R-005 | LOW | STATE | POST-MVP | engine/ai_advisor.py and engine/extract_json.py error handling unverified. | Exception triggered in live session |
| R-006 | LOW | STATE | POST-MVP | _CAUSAL_STRUCTURE_PATTERNS at 32 of 35 ceiling with no enforcement test. | Ceiling breach confirmed |
| R-007 | LOW | STATE | ILT-001 BLOCKER | idea_summary read via getattr — likely always None. FDC-001 invention summary may render empty. | ILT-001 produces empty invention summary |
| R-008 | LOW | DISCLOSURE | DOCUMENTATION ONLY | domain_rules.py docstring says electronics only but contains 4 domains. | Docstring confirmed incorrect |

---

## Section 6 — Open Questions

| ID | Question | Product Impact | Status |
|---|---|---|---|
| OQ-007 | Does idea_summary ever get populated? | ILT-001 BLOCKER | Pending ILT-001 |
| OQ-012 | Does FDC-001 deliverable button appear at session completion when _eligible() == True? | ILT-001 BLOCKER | Pending ILT-001 |

All other open questions (OQ-001 through OQ-011) are closed. See Section 3 for resolutions.

---

## Section 7 — Proven Capabilities

| Capability | Evidence |
|---|---|
| Domain Classification | Correctly identifies electronics inventions from technically-worded descriptions. Confirmed Sessions A-E. Returns Domain not recognized on natural-language descriptions (D-003). |
| Causal Reasoning Classifier | assess_response() with 32-pattern _CAUSAL_STRUCTURE_PATTERNS correctly distinguishes ASSERTED from REASONED. Session B confirmed false-positive rejection. Session C confirmed true-positive recognition. |
| Structured Question Delivery | Questions are well-formed, causally framed, consistently rendered. |
| Disclosure Layer | Epistemic disclosure text renders correctly at all stages. Honest and appropriate. |
| Session Isolation | Each session is independent with a unique UUID. Confirmed across all five sessions. |
| Deterministic Governance Architecture | AI generates questions only. AI does not control advancement. All progression decisions are deterministic. Must be preserved. |
| Progressive Questioning | Follow-up questions progress appropriately within a gap. Correct behavior. |

---

## Section 8 — Unproven Capabilities

| Capability | Status |
|---|---|
| Quality-Gated Completion | Classifier scores responses but completion is triggered by iteration count. Enforcement does not exist. |
| Gap Closure | No session showed a gap moving from ACTIVE to closed. Gap was ACTIVE at completion in every session. |
| Multi-Gap Sequencing | PHYSICAL_FEASIBILITY and BOUNDARY_AMBIGUITY were never opened in any live session. |
| Maturity Level Progression (earned) | Stage indicators advance on fixed schedule not tied to demonstrated quality. |
| Stall Detection | Three identical weak responses in Session D produced no behavior change. D-006 confirmed. |
| FDC-001 Deliverable | No live session has ever produced a deliverable. |
| Differentiated Inventor Experience | High-quality and low-quality inventors receive identical completion experiences. |

---

## Section 9 — Product Capability Gap Map Summary

### Capabilities Partially Present but Incomplete

- Quality-gated advancement — classifier works, enforcement missing
- Maturity level progression — visual indicators exist, earned advancement does not
- Gap sequencing — architecture defined, second and third gaps never reached
- Stall detection — threshold defined, behavior absent (D-006)
- Domain-aware questioning — domain classified, questions identical across domains
- FDC-001 deliverable — infrastructure exists, never triggered in live session

### Capabilities Completely Absent from Live Product

- Earned exit — completion currently guaranteed after 3 iterations regardless of quality
- Gap closure confirmation — inventor never receives confirmation a gap was satisfied
- Physical feasibility interrogation — PHYSICAL_FEASIBILITY gap never opened
- Boundary ambiguity interrogation — BOUNDARY_AMBIGUITY gap never opened
- Inventor-visible progression criteria — what constitutes a sufficient answer is invisible
- External work identification — no session produced work requirements
- Validation requirements specification — no session identified validation needs

### Shortest Path to Intended Vision

| Step | Requirement |
|---|---|
| Step 1 | Connect classifier output to completion condition. |
| Step 2 | Make gap closure visible and confirmatory. |
| Step 3 | Open the second and third gaps in sequence through demonstrated quality. |
| Step 4 | Produce the FDC-001 deliverable in a live session. |

---

## Section 10 — Foundation Assessment Summary

> **CONCLUSION: Preserve the foundation. Repair the governance layer.**

The separation of AI generation from deterministic governance is correct and rare. The foundation has two layers — assessment layer and completion layer — that are currently not connected. This is a governance gap, not a foundation flaw.

| Question | Answer |
|---|---|
| Foundation architecturally sound? | YES — separation of generation from governance is correct |
| Proven instruments worth preserving? | YES — classifier, domain recognition, disclosure, deterministic governance |
| Foundation the source of observed failures? | NO — failures are in the governance connection between assessment and completion |
| Foundation too narrow for full vision? | Scoped for MVP, not full vision — appropriate, not a flaw |
| Decision | PRESERVE foundation, IMPLEMENT governance connection, EXTEND later |

---

## Section 11 — Vision Governance Principles

> **These are permanent governance principles. Any agent, developer, architect, or reviewer working on InventorAI must treat these principles as binding constraints. A proposed change that violates any of these principles must be rejected regardless of its apparent technical merit.**

---

### Principle 1 — Inventor Ownership

> **The inventor owns the idea and the reasoning. The platform owns the structure and the questions. These two ownership domains must never be merged.**

The platform may question, challenge, structure, and identify gaps in an inventor's expressed reasoning. It may not fill those gaps on the inventor's behalf. It may not invent missing knowledge, supply missing mechanism steps, generate plausible-sounding explanations, or complete partial reasoning to make an inventor appear more advanced than they demonstrated.

Progression credit belongs exclusively to the inventor. It is awarded when, and only when, the inventor's own expressed words satisfy the quality threshold the protocol defines.

**What This Principle Forbids:**
- The AI suggesting mechanism steps that the inventor has not articulated
- The platform completing a gap on behalf of an inventor who cannot answer
- Advancement credit awarded based on iteration count rather than demonstrated quality
- The platform generating technical content to help an inventor appear more knowledgeable
- Any framing that presents AI-generated content as inventor-demonstrated understanding

**Relationship to D-005:** Finding D-005 is a direct violation of this principle. Resolving D-005 is required to restore compliance with Principle 1.

---

### Principle 2 — Improvement, Not Generation

> **InventorAI improves inventors. It does not generate inventions, mechanisms, products, or technical answers for inventors who cannot provide them.**

The platform is a structured mirror that reflects the inventor's own reasoning back to them at increasing levels of precision. It is not a creativity tool, product design tool, business plan generator, or substitute for engineering knowledge.

**What This Principle Forbids:**
- Using InventorAI as an idea generation tool
- Using InventorAI as a product generator
- Using InventorAI as a business plan generator
- The platform generating mechanism descriptions for inventors who cannot provide their own
- Platform-generated technical content being presented as session progress
- Completion experiences that do not reflect actual demonstrated quality

**The Correct Success State:** The platform succeeds when an inventor leaves with a more precise articulation of what they understand, a clear identification of what they do not yet understand, and an honest record of what was demonstrated.

---

### Principle 3 — Multi-Domain Integration Vision

> **The long-term vision is integrated cross-domain understanding of one product — not parallel single-domain analyses of separate components.**

Real inventions span multiple domains. The gaps that matter most exist at domain intersections. The intended vision is to help an inventor understand how multiple domains contribute to one integrated product and identify the gaps at those intersections.

**What This Principle Forbids:**
- Architectural decisions that treat multi-domain support as additive parallel analyses
- Domain classification that permanently assigns one domain label to a multi-domain invention
- Multi-domain implementation that produces separate domain reports rather than integrated cross-domain gap analysis
- Future scope expansion that adds domains without addressing the intersection problem

**What This Principle Requires of Future Architectural Decisions:**
- Multi-domain architecture must reason about domain intersections, not only domain membership
- The gap discovery layer must eventually identify gaps that exist between domains
- The FDC-001 deliverable must eventually represent a cross-domain concept
- Domain classification must eventually support multi-domain assignment

**Current MVP Scope Note:** The current MVP is correctly scoped to electronics/electrical only. This principle does not require multi-domain implementation before MVP is proven. It requires that when multi-domain work begins, it is built toward integration rather than isolation.

---

## Section 12 — Current Governance Rules

### Architectural Governance — Must Never Be Violated

- evaluate_transition() is governed by ADRs. No changes without owner decision.
- IdeaState schema is governed by MVP_SCOPE_FREEZE.md.
- GAP_PRIORITY order must not change — it defines the entire progression sequence.
- _eligible() logic is the eligibility gate for deliverable assembly. Do not alter.
- assemble_deliverable() is a pure function: IdeaState to FDC-001 dict, no LLM calls, no state mutation.
- The assemble() signature must not have parameters added without an ADR.
- The AI must never be given any role in progression decisions. Generation and governance are permanently separated.

### Existing Guardrails — Must Remain Passing

- tests/test_architecture_guardrails.py — enforces infer_domain() signature stability, statelessness, determinism
- tests/test_wps001_invariants.py — WPS-001 workflow protection standard
- tests/test_fdc001_contract.py — FDC-001 deliverable contract including ODS-001 deferred-section enforcement

### Validation Campaign Governance — Still Active

- D-001 and D-002 fixes must not be applied until the disclosure validation record is formally committed.
- D-003 must not be investigated by expanding the signal list until post-MVP.
- ILT-001 must not be run until D-005 is resolved.
- STALL_THRESHOLD must not be changed before D-006 is investigated and a fix is verified in a live session.

### Inventor Journey Architecture — Frozen Decision GD-001

> **GOVERNANCE DECISION GD-001 — Adopted 2026-05-29.** The inventor journey is a three-stage architecture. The three-gap mechanism knowledge assessment is Stage Two and must not be modified to absorb situational knowledge. This decision is frozen and must not be reopened without new evidence.

| Stage | Purpose and Status |
|---|---|
| Stage One — Situational Orientation | Pre-gap intake phase. Surfaces problem statement, mechanism hypothesis, and acknowledged unknowns. **Currently absent from the live product.** |
| Stage Two — Mechanism Knowledge Assessment | The existing three-gap architecture: MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY. Quality-gated. Deterministic. Must not be modified to accommodate situational knowledge. |
| Stage Three — Deliverable Reflection | Post-gap reflection phase using gap journey evidence to produce FDC-001. **Currently absent from the live product in any meaningful form.** |

Three situational knowledge concepts are explicitly excluded from Stage Two gap types:

| Concept | Correct Location and Exclusion Rule |
|---|---|
| Problem-Mechanism Fit | Belongs in Stage One and Stage Three. Must not be added as a Stage Two gap type. |
| Assumption Inventory | Surfacing belongs in Stage One. Reassessment belongs in Stage Three. Must not be added as a Stage Two gap type. |
| Expertise-Gap Awareness | Assessment belongs in Stage Three. Must not be added as a Stage Two gap type. |

**What GD-001 Forbids:**
- Adding PROBLEM_MECHANISM_FIT, ASSUMPTION_INVENTORY, EXPERTISE_GAP, or any situational knowledge variant as a Stage Two gap type
- Modifying the gap architecture contract to ask questions of the form "does your mechanism solve your problem"
- Treating the three-stage journey structure as a roadmap item rather than as the governing conceptual frame
- Implementing Stage One or Stage Three in ways that push situational knowledge questions into the Stage Two gap sequence

**What GD-001 Requires:**
- Stage One must be a distinct intake phase that precedes gap questioning and does not award or withhold gap progression credit
- Stage Three must be a distinct reflection phase that uses gap journey evidence as its primary input and produces FDC-001 as its output
- The gap architecture (Stage Two) must remain a pure mechanism-knowledge instrument with its current three-gap contract intact
- Any future gap type additions must assess a dimension of mechanism knowledge, not situational knowledge

---

## Section 13 — Explicit Scope Freeze

> **The following items are frozen. They must not be reopened without explicit owner authorization and new evidence.**

### Frozen In — MVP Scope

- Electronics/electrical domain — the only validated domain
- LEVEL 0, 1, 2 maturity progression only
- Three gap types: MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY
- Deterministic progression engine — no AI advancement decisions
- FDC-001 deliverable package with honest deferred sections
- In-memory session storage

### Frozen Out — Explicitly Deferred Post-MVP

- ODS-001 — Options Database for materials and manufacturing
- Component summary in deliverable
- Second domain proof
- Web and Supabase persistence
- Production hardening
- CI pipeline
- Precision and recall benchmarking
- Semantic contract test infrastructure
- apparent_components_ar and apparent_domain_tags fields in IdeaState — Option C accepted, deferred

---

## Section 14 — MVP Boundaries

ILT-001 — the Integrated Lifecycle Test — is the MVP proof. It must demonstrate that one real idea can travel through the complete LEVEL 0 to LEVEL 2 progression lifecycle via the actual web session flow, with all three gaps opened and closed in sequence, all state transitions verified, and a valid FDC-001 deliverable produced.

**Until ILT-001 succeeds and its evidence artifact is committed, MVP is not proven.**

> **ILT-001 cannot be run until D-005 is resolved.** D-005 (iteration-count completion) is an MVP BLOCKER. D-006 (stall detection failure) is an ILT-001 BLOCKER. Both must be resolved before ILT-001 can produce valid evidence.

### ILT-001 Prerequisites

- D-005 resolved and verified in a live session
- D-006 resolved and verified in a live session
- Disclosure validation record committed (Sessions A-E evidence)
- D-001 and D-002 fixes applied and committed
- ILT-001 fixture defined (exact idea text, responses, expected states at each transition)

### ILT-001 Success Criteria

- One real idea travels LEVEL 0 to LEVEL 2 via actual web session flow
- All three gaps opened and closed in sequence
- All state transitions verified
- Valid FDC-001 deliverable produced
- Evidence artifact committed to docs/ILT-001-evidence.md

---

## Section 15 — Post-MVP Items

| Item | Deferral Reason |
|---|---|
| ODS-001 | Options Database for materials, components, and manufacturing. No implementation until post-MVP. |
| Component Summary | FDC-001 component section. Requires ODS-001. |
| Second Domain | Mechanical, medical, or software domain proof. MVP is electronics only. |
| DB Persistence | Supabase schema exists. Not activated for MVP. |
| D-003 Investigation | Signal list expansion or error message improvement. Investigation only, post-MVP. |
| R-001 | infer_domain() accuracy baseline, ADR, tie-breaking test. Post-MVP governance. |
| R-005 | ai_advisor.py and extract_json.py error handling verification. Low priority post-MVP. |
| R-006 | _CAUSAL_STRUCTURE_PATTERNS ceiling enforcement test. Low priority post-MVP. |
| R-008 | domain_rules.py docstring correction. Documentation only, post-MVP. |
| Document B | Operational governance document. Premature until multi-domain operation with real users. |
| CI Pipeline | Production infrastructure. Not required for MVP proof. |
| Stage One — Situational Orientation | Intake phase of the three-stage journey (GD-001). Design and implementation post-MVP. |
| Stage Three — Deliverable Reflection | Reflection phase of the three-stage journey (GD-001). Full implementation post-MVP; FDC-001 basic output is MVP-required. |

---

## Section 16 — Decisions That Must Not Be Reopened Without New Evidence

- The AI does not control advancement decisions. This is a governance contract, not an implementation choice. It must not be changed.
- ODS-001 is deferred post-MVP. Option C was accepted. apparent_components_ar and apparent_domain_tags are not added to IdeaState for MVP.
- The three-gap architecture (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY) is sufficient for MVP. New gap types must not be added.
- Electronics/electrical is the only validated domain for MVP. Second domain proof is post-MVP.
- In-memory session storage is sufficient for MVP proof. Supabase persistence is post-MVP.
- The assemble() pure-function contract must be preserved. No LLM calls in the assembler.
- The disclosure validation record must be committed before D-001 and D-002 fixes are applied. The evidence chain must be preserved.
- ILT-001 must run through the actual web session flow, not through synthetic state objects. Synthetic state tests do not constitute ILT-001 evidence.
- **GD-001:** The three-stage inventor journey is frozen. MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, and BOUNDARY_AMBIGUITY are the correct and complete Stage Two gap types. Problem-mechanism fit, assumption inventory, and expertise-gap awareness are not gap types. Any proposal to add them as Stage Two gap types is architecturally incorrect unless new evidence justifies reopening GD-001.

---

## Section 17 — Current Strategic Conclusion

### What Has Been Proven

- The domain classifier works for technical vocabulary descriptions
- The causal reasoning classifier correctly distinguishes assertion from reasoning
- The disclosure layer is honest and renders correctly
- Session isolation works
- The deterministic governance architecture is sound

### What Has Not Been Proven

- Quality gates advancement — not demonstrated in any live session
- Gaps close when satisfied — never observed
- Multiple gaps sequence correctly — second gap never reached
- FDC-001 deliverable is produced — never observed
- Inventor experience differs based on demonstrated quality — not demonstrated

### What Remains a Hypothesis

- The full LEVEL 0 to LEVEL 2 progression produces a meaningful structured deliverable reflecting what a specific inventor demonstrated about their specific invention
- The platform can reliably distinguish between inventors who understand their mechanism and inventors who do not, at the completion level

### The Single Milestone That Determines Direction

> A single live session in which an inventor's response quality determines whether they advance — and the session produces a different outcome for a high-quality inventor than for a low-quality inventor. Until this milestone is reached, the project has a well-designed classifier embedded in a fixed-iteration interview. After it is reached, the project has a progression platform.

### Final Positioning

| | |
|---|---|
| Current product description | Idea Structuring Tool |
| Intended product description | Deterministic Invention Progression Platform |
| Foundation status | Sound — preserve and build on |
| Critical gap | Classifier output is not connected to completion condition |
| Blocker before ILT-001 | D-005 (completion by iteration count) and D-006 (stall detection absent) |
| Next milestone | One live session where quality determines advancement |
| MVP status | NOT PROVEN — ILT-001 not yet run |
| Test suite status | 172 passed, 0 failed as of HEAD 3f3a707 |

---

*End of Document — INVENTORAI PROJECT STATE FREEZE v1.2*
*Prepared by Claude Sonnet 4.6 | 2026-05-29 | HEAD: 3f3a707 | Branch: main*
*v1.2 adds GD-001 three-stage inventor journey governance decision to Sections 12 and 16*
