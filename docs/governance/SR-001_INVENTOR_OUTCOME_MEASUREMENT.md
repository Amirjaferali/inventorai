# SR-001: INVENTOR_OUTCOME_MEASUREMENT
## Inventor Development Model and Outcome Measurement Framework

**Document ID:** SR-001
**Governance Level:** Level 3
**Status:** PROPOSED — PENDING OWNER ADMISSION DECISION
**Date:** 2026-06-03
**Provenance:** Owner Authorization — post AB-006 closure
**Depends on:** STRATEGIC_PRODUCT_VISION.md (Level 0), SA-001A (Level 1), SA-001B (Level 1)

---

## 1. PURPOSE, SCOPE, AND DUAL ROLE

### 1.1 Why This Document Exists

AB-006 resolved authority governance and architectural debt. It does not demonstrate that InventorAI improves inventor outcomes.

GOVERNANCE-ROADMAP Priority 7 records: "ILT-001 proved session progression. It did not prove inventor development." SPV §5B confirms FDC-001 "Does Not Prove" inventor development.

This document addresses the next question: Does InventorAI improve inventors?

### 1.2 The Dual Role of SR-001

SR-001 serves two inseparable functions:

**Function 1 -- Inventor Development Model:**
Defines what it means for an inventor to improve. Without this, there is nothing to measure. A measurement framework that does not first define its subject measures platform activity, not inventor development.

**Function 2 -- Outcome Measurement Framework:**
Defines how improvement should be observed, what evidence is required, and what infrastructure must exist before measurement is valid.

These two functions cannot be separated. Defining measurement without defining development produces metrics that look positive while failing the product's actual purpose. SPV §3: "A platform that helps inventors complete sessions is different from a platform that helps inventors become better inventors."

### 1.3 Scope Boundaries

**In scope:**
- Defining inventor improvement at the vision level
- Classifying dimensions of improvement into structured layers
- Defining what constitutes evidence of improvement
- Identifying what is currently measurable and what is not
- Recording infrastructure requirements for future measurement

**Out of scope:**
- Implementing any measurement mechanism
- Designing Stages 3-6
- Resolving GOVERNANCE-ROADMAP Priority 3 (Session vs Project)
- Defining persistence architecture
- Authorizing domain expansion work

### 1.4 Strategic Transition Note

SR-001 marks the transition from architectural governance to outcome governance. AB-006 answered: "Is the architecture correct?" SR-001 begins answering: "Does InventorAI improve inventors?" These are distinct questions requiring distinct evidence.

### 1.5 Compatibility Guardrail

SR-001 must not define inventor success in a way that excludes future dimensions of the Inventor Development and Innovation Guidance Platform. The framework must remain compatible with:

- Implementation Readiness (Stage 3)
- Technical Readiness (Stage 4)
- Prototype Planning (Stage 5)
- Domain Navigation across future technical domains
- Commercial Readiness (Stage 6)

These are not currently measurable. They must not be excluded from the framework.

---

## 2. INVENTOR DEVELOPMENT MODEL

### 2.1 The Governing Definition

Derived from SPV §2 Owner Vision Lock. The platform measures and grows four things:

1. **Reasoning quality** -- the inventor's ability to articulate why their mechanism works
2. **Ownership depth** -- the inventor's demonstrated understanding of their own idea
3. **Gap precision** -- the precision and resolvability of identified knowledge gaps
4. **Implementation readiness proximity** -- the inventor's closeness to a state where they can act

An inventor has improved when any of these four dimensions shows measurable, verifiable growth across time. Not session completion. Not protocol traversal. Not iteration count.

### 2.2 What Improvement Is Not

Per SPV §5A, improvement is explicitly not defined by:
- Idea approval or positive scoring
- Domain completion
- Protocol completion
- Session completion rate
- REASONED rate in isolation within a single session

Per SPV §2 Principle 2: an inventor who learns to produce REASONED responses without developing genuine understanding has not improved -- they have learned the protocol. This is the central risk SR-001 must guard against.

### 2.3 The Critical Distinction

"How well the inventor answers InventorAI questions" is not the same as "How much the inventor has evolved because of InventorAI."

SR-001 governs the second. The first is a necessary but insufficient proxy.

### 2.4 Improvement Across the Full Journey

The four dimensions apply across all stages as defined in SA-001A §3.1:

| Stage | Primary Growth Expected |
|-------|------------------------|
| 1 -- Situational Orientation | Ownership depth, gap precision baseline |
| 2 -- Gap Discovery | Reasoning quality, gap precision |
| 3 -- Implementation Readiness | Implementation readiness proximity, reasoning quality |
| 4 -- Engineering Readiness | Implementation readiness proximity, technical decision quality |
| 5 -- Prototype Readiness | Implementation readiness proximity, proof-of-concept precision |
| 6 -- Commercialization | All four within institutional deployment context |

SR-001 does not design these stages. It records that the measurement framework must remain compatible with each.

---

## 3. DIMENSIONS OF INVENTOR IMPROVEMENT

The ten dimensions are organized into three layers. This structure prevents conflating what develops in the inventor, how it develops, and across what time horizon it is observable.

---

### LAYER 1 -- CORE DEVELOPMENT DIMENSIONS

What develops in the inventor. Derived directly from SPV §2 Owner Vision Lock. These four dimensions are the governing definition of inventor improvement and remain constant across all stages and domains.

---

**3.1 Reasoning Growth**

The inventor's ability to articulate causal structure -- why their mechanism works, not only what it does.

*Vision basis:* SPV §2 dimension 1, §3 "Reasoning evidence growth"

*Currently observable:* Partially. REASONED/ASSERTED captures binary causal structure presence. Does not capture degree, depth, or trajectory across sessions.

*Infrastructure required:* Granular reasoning quality model beyond binary classification. Cross-session tracking.

*Lock-in risk:* REASONED rate must not become the success metric for Stage 3+. SA-001A §10 confirms rules sufficient for Stage 2 are not necessarily sufficient for Stage 3.

---

**3.2 Ownership Growth**

The inventor's demonstrated understanding of their own idea -- not AI-generated, not platform-echoed, genuinely theirs.

*Vision basis:* SPV §2 dimension 2, §3 "Ownership evidence growth", §7 Principle 1

*Currently observable:* Partially. idea_summary is enforced as inventor-supplied. AI Echo (RESPONSE-QUALITY §4 Category 6) is not currently detectable -- provenance tracking is absent.

*Infrastructure required:* Knowledge source separation (GD-002 §9). AI Echo detection. Neither designed nor authorized.

*Governance constraint:* SPV §10 -- any implementation that blurs the boundary between AI-generated content and inventor-demonstrated understanding violates Principle 1.

---

**3.3 Gap Evolution**

How identified knowledge gaps change in precision, actionability, and resolvability over time.

*Vision basis:* SPV §2 dimension 3, §3 "Gap evolution", §5A "Gap Quality"

*Currently observable:* Partially within a single session. Gap state (ACTIVE/PARTIAL/CLOSED) is tracked. Quality trajectory across sessions is not tracked -- no persistence.

*Infrastructure required:* Session persistence, inventor identity, cross-session gap state tracking.

---

**3.4 Implementation Readiness Progression**

The inventor's movement from abstract idea toward actionable, implementable concept -- able to identify next actions, name remaining unknowns, define proof-of-concept objectives.

*Vision basis:* SPV §2 dimension 4, §6 Layer 3 characterization, SA-001A §6

*Currently observable:* Not in Stage 2. Stage 3 is not yet designed.

*Infrastructure required:* Stage 3 design authorization. SA-001A §11 prerequisites: SA-001A committed, SA-001B committed, AB-006-A and AB-006-B resolved. Owner Stage 3 authorization not yet granted.

*Guardrail:* This dimension must be preserved in the framework even though it is not currently measurable. Excluding it reduces InventorAI to a Stage 2 assessment engine.

---

### LAYER 2 -- META-DEVELOPMENT DIMENSIONS

How the inventor develops. These dimensions do not measure what has grown but how growth occurs and whether it is genuine. They are the primary tools for distinguishing inventor development from protocol learning.

---

**3.5 Unknown Awareness**

The inventor's ability to identify what they do not know -- articulating gaps before being asked, naming uncertainties with precision.

*Vision basis:* SPV §2 dimension 3 "precision and resolvability", SA-001A §6 Stage 3 "Expertise-Gap Awareness"

*Currently observable:* Indirectly. Proactive BOUNDARY_AMBIGUITY responses suggest this capability. Not formally measured.

*Infrastructure required:* Stage 3 design. Proactive gap declaration tracking mechanism.

*Note:* An inventor who names an unknown before being asked demonstrates higher unknown awareness than one who provides confident but incomplete mechanism description. Current classification does not distinguish these.

---

**3.6 Inventor Independence**

The inventor's ability to reach comparable reasoning depth with fewer platform prompts over time.

*Vision basis:* SPV §7 Principle 1 "Progression credit belongs exclusively to the inventor", Principle 2 "InventorAI improves inventors -- it does not generate"

*Currently observable:* Partially within a session. Iterations per gap is tracked. Cross-session comparison is not possible without persistence.

*Infrastructure required:* Session persistence, inventor identity, per-gap iteration trajectory.

*Lock-in risk:* Without tracking prompt-dependency, the platform cannot distinguish genuine improvement from learning to respond to specific question patterns.

---

**3.7 Transfer of Reasoning**

Whether improvement in one gap type or domain transfers to other gap types or domains -- the primary test for genuine development versus protocol learning.

*Vision basis:* SA-001A §2.3 "Session vs Development Distinction" -- exit conditions must express measurable growth, not mechanical closure

*Currently observable:* Partially within a session -- REASONED rate across different gap types can be compared. Cross-session and cross-domain transfer is not measurable without persistence.

*Infrastructure required:* Cross-session tracking. Multi-domain IdeaState per SA-001B §9, Stage 4 placement per SA-001B §9.4.

*This is the most diagnostic dimension for distinguishing inventor growth from protocol completion.* An inventor whose improvement transfers to new gap types and domains has developed reasoning capability. An inventor whose improvement is confined to familiar patterns has learned the protocol.

---

**3.8 Structured Thinking Development**

The inventor's ability to decompose problems into mechanisms, constraints, dependencies, and assumptions -- the cognitive capability underlying all four core dimensions.

*Vision basis:* SPV §6 Layer 3 characterization, SA-001A §6 Stage 3 objectives, SPV §3

*Currently observable:* Not directly. REASONED/ASSERTED captures a proxy but not the underlying capability.

*Infrastructure required:* Stage 3 design authorization. Qualitative or semi-qualitative assessment mechanisms not yet designed.

*Governance note:* Any measurement mechanism must satisfy SPV §2 Substitution Prohibition -- it must improve the inventor's ability to reason, not reason on their behalf.

---

### LAYER 3 -- LONGITUDINAL PERSPECTIVES

The time horizon across which improvement is observable. These are not independent dimensions -- they are the temporal frame for observing Layer 1 and Layer 2 dimensions. Both require infrastructure that does not currently exist.

---

**3.9 Progressive Knowledge Acquisition**

Measurable deepening of domain understanding across multiple interactions -- the inventor demonstrably knows more, more precisely, over time.

*Vision basis:* SPV §3 "measurable deepening of domain understanding across iterations"

*Currently observable:* Not observable. Requires cross-session tracking.

*Infrastructure required:* Persistence layer, inventor identity model, longitudinal session records. Blocked by GOVERNANCE-ROADMAP Priority 3 resolution.

---

**3.10 Longitudinal Growth**

Observable trajectory of improvement across multiple sessions -- not isolated session success but directional development over time.

*Vision basis:* SPV §3 "across iterations", §5B FDC-001 "DOES NOT PROVE inventor development", GOVERNANCE-ROADMAP Priority 7

*Currently observable:* Not observable. Architecture is session-oriented with no persistence.

*Infrastructure required:* Full resolution of GOVERNANCE-ROADMAP Priorities 3, 4, and 5. Sequential dependencies, none resolved.

*This is the most strategically important perspective and the least technically feasible today.* Any persistence architecture designed under GOVERNANCE-ROADMAP Priority 3-4 must be designed to enable this measurement.

---

## 4. EVIDENCE OF IMPROVEMENT

This section applies the project's Evidence First governance principle to inventor outcome measurement. Evidence First means: a claim has standing only at the level it is documented. Applied to inventor development: improvement is not claimed until evidence meeting the standard defined here is collected, recorded, and verified.

### 4.1 Three Distinct Concepts

These three concepts must never be conflated:

**Improvement** -- a real change in an inventor's capability, reasoning quality, ownership depth, gap precision, or implementation readiness proximity. Improvement is the phenomenon we are trying to support.

**Evidence that improvement occurred** -- a documented, verifiable record that demonstrates improvement happened. Evidence is not the same as improvement. The inventor may have improved without us being able to prove it. We do not claim improvement without evidence.

**Measurement mechanism** -- the tool or process that produces the evidence record. A measurement mechanism is not evidence itself -- it is the instrument that generates evidence when applied correctly.

Claiming improvement without evidence violates the project's governance standard. Treating measurement mechanism output as direct proof of improvement confuses the instrument with the result.

### 4.2 Evidence Within a Single Session

**Can demonstrate:**
- The inventor produced REASONED responses on specific gap types in this session
- The inventor's gap state progressed from PARTIAL to CLOSED on specific gaps
- The inventor's responses contained domain substance signals
- The session traversed all required gap types to completion
- The inventor's own words constitute the idea record (not AI-generated)

**Cannot demonstrate:**
- Whether reasoning quality is better than a previous session
- Whether the inventor would perform comparably without platform prompting
- Whether improvement will transfer to new gap types or domains
- Whether the inventor has genuinely developed versus learned the protocol

**Minimum data required for single-session evidence:**
- Session ID and timestamp
- Per-gap REASONED/ASSERTED classification record with iteration count
- Gap state trajectory (ACTIVE to PARTIAL to CLOSED)
- Domain assignment
- idea_summary (inventor-supplied, not AI-generated)

**Single-session evidence standard:** A single session constitutes evidence of protocol traversal quality. It does not constitute evidence of inventor development. This is the FDC-001 boundary established in SPV §5B.

### 4.3 Evidence Across Multiple Sessions

**Can demonstrate (when infrastructure exists):**
- REASONED rate trajectory across sessions on the same gap type
- Iterations-per-gap trajectory -- increasing efficiency over time
- Whether improvement on familiar gap types transfers to new gap types
- Whether gap articulation becomes more precise and actionable over time
- Whether the inventor requires fewer prompts to reach the same depth

**Cannot demonstrate (even with cross-session data):**
- Causal attribution -- whether improvement is due to InventorAI or other factors
- Genuine understanding versus learned response patterns without Transfer of Reasoning evidence
- AI Echo contamination without provenance tracking (GD-002)

**Minimum data required for cross-session evidence:**
- Stable inventor identity across sessions
- Session sequence record
- Per-session per-gap quality metrics as defined in §4.2
- Baseline session record for comparison
- At minimum two sessions on comparable invention problems

**Cross-session evidence standard:** Cross-session evidence constitutes the minimum basis for claiming inventor development. Single-session evidence alone is insufficient.

### 4.4 What Does Not Count as Evidence of Improvement

The following must not be cited as evidence that an inventor has improved:

- **Session completion** -- traversing all gaps does not prove development (SPV §5B, ILT-001 §8)
- **Iteration count** -- more iterations does not mean better reasoning
- **Isolated REASONED rate in a single session** -- one session establishes no trajectory
- **maturity_level at session end** -- measures gap closure state, not inventor development
- **Protocol familiarity** -- improving only on familiar question patterns is learning the system, not developing reasoning capability
- **AI Echo responses scored as REASONED** -- platform content re-entering the record as inventor knowledge is a governance violation, not evidence of improvement (RESPONSE-QUALITY §4 Category 6)
- **Absence of ASSERTED responses** -- reducing ASSERTED count by avoiding substance rather than improving reasoning is gaming, not improvement

### 4.5 The Evidence Gap

The current architecture can produce single-session evidence only. Cross-session evidence -- the minimum standard for claiming inventor development -- requires infrastructure that does not exist.

Until GOVERNANCE-ROADMAP Priorities 3-5 are resolved:
- InventorAI can demonstrate session progression quality
- InventorAI cannot demonstrate inventor development
- Claims of inventor development are not supportable by current evidence

This is the honest state of evidence. SR-001 records it as a governance constraint, not a criticism of current implementation quality.

---

## 5. MEASUREMENT ARCHITECTURE -- THREE LEVELS

### Level 1 -- Vision Outcomes (Permanent, Stage-Agnostic)

Derived from SPV §2. Valid across Stage 1 to Stage 6. Valid across all domains.

1. Reasoning quality grows
2. Ownership depth grows
3. Gap precision improves
4. Implementation readiness proximity increases

These are the success criteria for InventorAI as an Inventor Development and Innovation Guidance Platform. They do not change when stages change or domains expand.

### Level 2 -- Stage-Specific Indicators (Vary by Stage)

**Stage 2 indicators (current):**
- REASONED rate per gap type
- maturity_level trajectory within session
- Gap closure quality (PARTIAL vs CLOSED distribution)
- Iterations per gap

**Stage 3 indicators (not yet defined -- requires Stage 3 design authorization):**
- Problem-mechanism fit articulation quality
- Assumption inventory precision
- Expertise-gap self-identification rate

**Stage 4-6 indicators:** Not yet defined -- deferred to stage design.

**Governance constraint:** Stage 2 indicators must not be used as evaluation criteria for Stage 3-6. SA-001A §10: "Rules sufficient for Stage 2 are not necessarily sufficient for Stage 3."

### Level 3 -- Infrastructure Requirements

| Requirement | Enables | Governance Reference |
|---|---|---|
| Inventor identity model | Dimensions 3.9, 3.10, 3.6, 3.7 | GOVERNANCE-ROADMAP Priority 3 |
| Session persistence | Dimensions 3.9, 3.10, 3.3, 3.6 | GOVERNANCE-ROADMAP Priority 3-4 |
| Knowledge source separation | Dimension 3.2 | GD-002, Priority 5 |
| AI Echo detection | Dimension 3.2 | RESPONSE-QUALITY §4 Category 6 |
| Stage 3 design | Dimensions 3.5, 3.8, 3.4 | SA-001A §11 |
| Cross-session gap tracking | Dimension 3.3 | GOVERNANCE-ROADMAP Priority 4 |

---

## 6. GOVERNANCE CONSTRAINTS ON FUTURE MEASUREMENT DESIGN

**6.1 Substitution Prohibition (SPV §2):** No measurement mechanism may substitute platform assessment for inventor demonstration.

**6.2 Non-Specialist Compatibility (RESPONSE-QUALITY §3):** Measurement must not penalize non-specialist language, informal reasoning, or domain-naive vocabulary.

**6.3 Stage-Level Independence:** Measurement criteria must be defined per stage. Stage 2 criteria must not govern Stage 3+ assessments.

**6.4 Commercial Integrity (SPV §11):** Measurement thresholds and advancement criteria may not be adjusted for commercial reasons.

**6.5 Domain-Agnostic Measurement (SA-001B §2.4):** Measurement mechanisms must function correctly across all current and future domains without per-domain tuning.

**6.6 Stage Naming Conflict:** STAGE3_READINESS_DECISION uses "Stage 3" to mean Domain Validation. SA-001A uses "Stage 3" to mean Implementation Readiness. SR-001 uses SA-001A terminology (Level 1 authority). Resolution requires explicit owner decision -- not authorized by this document.

---

## 7. OPEN QUESTIONS

1. Does SR-001 authorize any infrastructure requirements as first steps, or is it governance-only?

2. Should SR-001 define a minimum data collection protocol for current sessions -- before full infrastructure exists?

3. How does SR-001 interact with GOVERNANCE-ROADMAP Priority 7 -- does it supersede, satisfy, or extend it?

4. Does the owner wish to resolve the Stage naming conflict before SR-001 is committed?

5. Should long-term Inventor Development be evaluated purely as cognitive and reasoning growth, or as growth that demonstrably increases real-world implementation readiness and execution capability?

   The current framework implies both -- SPV §2 dimension 4 includes "implementation readiness proximity" as a governing dimension alongside reasoning quality and ownership depth. However, an unresolved strategic tension exists:

   A purely cognitive evaluation model measures whether the inventor thinks more clearly about their idea. An implementation readiness evaluation model measures whether the inventor moves closer to being able to act on their idea in the real world.

   These may require different evidence standards, different stage exit criteria, and different measurement mechanisms. The answer to this question may influence Stage 3, Stage 4, and Stage 5 governance decisions in ways that cannot be fully anticipated at SR-001 drafting time.

   This question is recorded as an open strategic position that requires explicit owner decision before Stage 3 design begins.

---

## 8. CLOSURE CRITERIA

SR-001 is complete when:
- The Inventor Development Model is reviewed and accepted
- The three-layer dimension structure is accepted
- The Evidence of Improvement section is accepted
- Open questions in §7 are answered or explicitly deferred
- The document is committed to the repository

---

*This document is produced to be accurate, not reassuring.*
*It does not authorize any implementation.*
*Improvement is not claimed without evidence meeting the standard defined in §4.*
*Measurement of inventor outcomes must never be confused with measurement of platform activity.*
