# STAGE3_GAP_EVIDENCE_MODEL.md
## Stage 3 Gap Evidence Model

**Document ID:** STAGE3_GAP_EVIDENCE_MODEL
**Type:** Design Artifact
**Governance Level:** Level 3
**Status:** PROPOSED -- PENDING OWNER ADMISSION DECISION
**Date:** 2026-06-03
**Provenance:** Owner Authorization -- post STAGE3_GAP_TAXONOMY_PROPOSAL admission
**Depends on:** SR-001, STAGE3_GAP_TAXONOMY_PROPOSAL, STAGE3_PURPOSE_CLARIFICATION

---

## PURPOSE OF THIS DOCUMENT

This document defines what constitutes valid evidence for each of the three Stage 3 canonical gap types. It precedes evaluation model design, question design, scoring, signals, and progression rules.

Evidence definition precedes evaluation design because Stage 3 evaluates inventor capability through demonstrated evidence rather than procedural compliance. This principle is established in STAGE3_GAP_TAXONOMY_PROPOSAL §6 and is consistent with the Evidence First governance standard throughout the project.

No evaluation logic is proposed here. No scoring is proposed. No questions are authored. No signals are defined.

---

## 1. GOVERNING PRINCIPLES FOR EVIDENCE DEFINITION

### 1.1 Evidence First

From MASTER-HANDOVER §19: Evidence first. Documentation second. Decision third. Implementation last.

Applied to Stage 3: no gap type may have an evaluation model until its evidence definition exists. No question may be authored until the evidence it is intended to elicit is defined. No exit condition may be specified until the evidence standard it must satisfy is established.

### 1.2 Minimum Sufficient Evidence Principle

Evidence requirements should remain as small as possible while still distinguishing genuine inventor development from procedural compliance. Accumulating additional evidence requirements beyond what is necessary to make this distinction increases governance burden without increasing measurement quality.

### 1.3 Capability Demonstration Requirement

Every evidence definition must identify:
- The underlying capability being demonstrated
- Why the evidence directly demonstrates that capability
- Why the evidence is not merely a proxy metric

Longer answers, more terminology, more details, and more iterations are proxy metrics, not evidence of inventor capability. The evidence model must not drift toward rewarding performance signals.

### 1.4 Domain-Agnostic Evidence Standard

Per SA-001B §2.4 and RESPONSE-QUALITY §9: evidence definitions must apply across all current and future domains without per-domain tuning. Every evidence definition in this document is tested for applicability beyond the current domain set.

### 1.5 Stage 3 Specificity Requirement

For each gap type, evidence must demonstrate a Stage 3 capability -- not a Stage 2 capability. Evidence that could be produced by a Stage 2-level response fails this requirement. The distinction between Stage 2 and Stage 3 evidence is not a matter of depth -- it is a matter of epistemic kind.

---

## 2. FOUR ACTIVE DESIGN RISKS

Four risks are recorded here and mitigated throughout this document.

**Risk A -- Taxonomy becoming an evaluation model (from STAGE3_GAP_TAXONOMY_PROPOSAL §6):**
Gap type definitions must not expand to include scoring, signals, or progression rules. This document defines evidence only.

**Risk B -- Protocol learning misclassified as inventor development (from STAGE3_GAP_TAXONOMY_PROPOSAL §6):**
Evidence must distinguish genuine capability growth from protocol familiarity and answer-pattern optimization. SR-001 §3.7 Transfer of Reasoning is the primary test.

**Risk C -- Evidence inflation:**
Evidence standards become so weak that ordinary Stage 2 responses are accepted as Stage 3 evidence. Mitigation: for every evidence definition, this document explicitly records what counts, what does not count, and why the evidence demonstrates a Stage 3 capability rather than a Stage 2 capability.

**Risk D -- Evidence overfitting:**
Evidence definitions become implicitly tied to current domains, especially electronics. Mitigation: every evidence definition is tested against domain-agnostic criteria and reviewed for applicability to solar, medical, software, and future domain families.

**Risk E -- Evidence proliferation:**
Each gap type accumulates excessive evidence requirements over time. Mitigation: minimum sufficient evidence principle in §1.2. Evidence requirements are bounded to what is necessary to distinguish genuine development from procedural compliance.

**Risk F -- Proxy evidence drift:**
The system begins measuring artifacts that correlate with development instead of development itself. Mitigation: every evidence definition identifies the underlying capability, why the evidence directly demonstrates it, and why it is not a proxy.

---

## 3. EVIDENCE MODEL: PROBLEM_MECHANISM_FIT

### 3.1 Underlying Capability

The inventor can reason about the relationship between their mechanism and the problem it is intended to solve -- not only describe the mechanism, but evaluate whether the mechanism addresses the intended problem and articulate why.

### 3.2 What Counts as Evidence

**PMF-E1: Problem articulation independent of mechanism description.**
The inventor states the problem they are solving in terms that do not merely restate the mechanism. Evidence: the problem description would be recognizable as a problem even if the mechanism were unknown.
Why this is Stage 3: Stage 2 does not require the inventor to articulate the problem independently. Stage 2 evaluates mechanism description. Stage 3 evaluates whether the mechanism addresses a separately articulable problem.

**PMF-E2: Fit reasoning -- causal justification linking mechanism to problem.**
The inventor articulates why their mechanism addresses the problem rather than asserting that it does. Evidence: the inventor provides a causal chain connecting a mechanism property to a problem requirement.
Why this is Stage 3: Stage 2 REASONED classification requires causal structure about how the mechanism works. PMF-E2 requires causal structure about why this mechanism addresses this problem -- a different causal relationship.

**PMF-E3: Fit boundary awareness.**
The inventor can identify at least one condition under which the mechanism would not address the problem, or one aspect of the problem the mechanism does not address. Evidence: an inventor who can name the limits of fit demonstrates genuine fit reasoning rather than assumed fit.
Why this is Stage 3: Stage 2 BOUNDARY_AMBIGUITY asks where the mechanism scope ends. PMF-E3 asks where the problem-mechanism fit ends -- a different boundary.

### 3.3 What Does Not Count as Evidence

- Restating the mechanism description as a problem solution (Risk F proxy: mechanism length as fit evidence)
- Asserting that the mechanism solves the problem without causal justification (Risk C inflation: assertion accepted as reasoning)
- Describing the problem in terms that are synonymous with the mechanism (Risk B protocol: learned fit language without genuine fit analysis)
- Producing a longer or more detailed mechanism description (Risk F proxy: verbosity as evidence)

### 3.4 Domain-Agnostic Test

PMF-E1, PMF-E2, and PMF-E3 apply without modification to:
- Electronics: does the circuit design address the measurement problem?
- Solar: does the energy collection approach address the power requirement?
- Medical: does the device mechanism address the clinical need?
- Software: does the algorithm address the computational problem?
- Future domains: the evidence structure is problem-mechanism relational, not domain-specific.

Domain-agnostic standard: satisfied. No per-domain tuning required.

### 3.5 Minimum Sufficient Evidence

PMF requires evidence of: (1) independent problem articulation, (2) causal fit justification, (3) fit boundary awareness. These three are necessary and sufficient to distinguish genuine problem-mechanism fit reasoning from mechanism description restated as solution. No additional evidence requirements are proposed.

---

## 4. EVIDENCE MODEL: ASSUMPTION_INVENTORY

### 4.1 Underlying Capability

The inventor can identify assumptions they are making about their mechanism and implementation path -- including assumptions they had not previously recognized as assumptions. This is distinct from identifying known gaps (Stage 2) or validating assumptions (outside platform scope).

### 4.2 What Counts as Evidence

**AI-E1: Named assumptions in inventor's own words.**
The inventor names at least one assumption underlying their mechanism that is not already documented as a known gap. Evidence: an assumption stated as something the inventor is taking as given rather than something they have verified.
Why this is Stage 3: Stage 2 identifies gaps in mechanism description. AI-E1 identifies what the inventor is assuming despite not having verified it -- a different epistemic act. A Stage 2 inventor identifies what they do not know. A Stage 3 inventor identifies what they are assuming.

**AI-E2: Load-bearing vs peripheral classification.**
The inventor can distinguish between assumptions whose failure would invalidate the mechanism (load-bearing) and assumptions whose failure would require adaptation but not invalidation (peripheral). Evidence: the inventor provides a reason for the classification, not only the classification itself.
Why this is Stage 3: Stage 2 does not ask the inventor to evaluate the consequences of their assumptions. AI-E2 requires implementation-oriented reasoning about dependency -- what depends on this assumption being correct?

**AI-E3: Assumption provenance awareness.**
The inventor can identify at least one assumption they were not aware of making before Stage 3 began. Evidence: an assumption named in Stage 3 that was not surfaced or acknowledged in Stage 2.
Why this is Stage 3: this is the primary evidence of Unknown Awareness growth (SR-001 §3.5). It demonstrates that Stage 3 developed a capability that was genuinely absent at Stage 2 exit.

### 4.3 What Does Not Count as Evidence

- Listing known gaps already identified in Stage 2 as assumptions (Risk C inflation: Stage 2 content accepted as Stage 3 evidence)
- Asserting that assumptions exist without naming them (Risk F proxy: acknowledgment as evidence)
- Producing a comprehensive list without load-bearing classification (Risk E proliferation: list length as evidence)
- Naming domain-specific constraints that were already captured as PHYSICAL_FEASIBILITY gaps (Risk C inflation: Stage 2 repetition as Stage 3 evidence)

### 4.4 Domain-Agnostic Test

AI-E1, AI-E2, and AI-E3 apply without modification to:
- Electronics: what are you assuming about component availability, operating conditions, or signal behavior?
- Solar: what are you assuming about irradiance consistency, storage capacity, or grid compatibility?
- Medical: what are you assuming about patient compliance, regulatory pathway, or clinical environment?
- Software: what are you assuming about data availability, system load, or API stability?
- Future domains: the evidence structure is assumption-identification relational, not domain-specific.

Domain-agnostic standard: satisfied. No per-domain tuning required.

### 4.5 Minimum Sufficient Evidence

ASSUMPTION_INVENTORY requires evidence of: (1) named assumptions beyond known gaps, (2) load-bearing classification with reasoning, (3) at least one assumption not previously recognized. These three are necessary and sufficient to distinguish genuine assumption awareness from gap list repetition. No additional evidence requirements are proposed.

---

## 5. EVIDENCE MODEL: EXPERTISE_GAP_AWARENESS

### 5.1 Underlying Capability

The inventor can identify what domain expertise their implementation requires that they do not currently possess, and can articulate why that expertise is required rather than merely acknowledging its absence.

### 5.2 What Counts as Evidence

**EGA-E1: Named expertise domain with implementation justification.**
The inventor names a domain of expertise required for their implementation and explains why that domain is required -- what aspect of implementation depends on it. Evidence: the connection between the expertise domain and a specific implementation requirement is stated explicitly.
Why this is Stage 3: Stage 2 BOUNDARY_AMBIGUITY identifies where the inventor's mechanism scope ends. EGA-E1 identifies what expertise is required to move beyond that boundary toward implementation -- a forward-looking capability Stage 2 does not develop.

**EGA-E2: Self-assessment of current expertise level.**
The inventor distinguishes between expertise domains where they have working knowledge and domains where they do not. Evidence: the inventor provides a reason for the distinction rather than asserting it.
Why this is Stage 3: this requires the inventor to evaluate their own capability relative to an implementation requirement -- an implementation-oriented self-assessment that Stage 2 does not require.

**EGA-E3: Expertise gap consequence awareness.**
The inventor can articulate what would happen if the identified expertise gap were not resolved before implementation proceeded. Evidence: a described consequence that is specific to the inventor's mechanism, not a generic statement about the importance of expertise.
Why this is Stage 3: this connects expertise awareness to implementation reasoning. A Stage 3 inventor does not merely acknowledge expertise gaps -- they understand why those gaps matter for their specific implementation path.

### 5.3 What Does Not Count as Evidence

- Naming expertise areas without connecting them to implementation requirements (Risk F proxy: terminology as evidence)
- Acknowledging that expertise gaps exist without naming them (Risk F proxy: acknowledgment as evidence)
- Listing expertise domains that are unrelated to the inventor's specific mechanism (Risk E proliferation: list length as evidence)
- Restating BOUNDARY_AMBIGUITY gaps from Stage 2 as expertise gaps (Risk C inflation: Stage 2 content as Stage 3 evidence)
- Domain-specific jargon without demonstrated understanding of why the expertise is required (Risk B protocol: learned terminology without genuine awareness)

### 5.4 Domain-Agnostic Test

EGA-E1, EGA-E2, and EGA-E3 apply without modification to:
- Electronics: what electrical engineering expertise does your PCB layout require that you do not have?
- Solar: what power systems expertise does your storage integration require?
- Medical: what clinical expertise does your device validation pathway require?
- Software: what systems architecture expertise does your scalability requirement depend on?
- Future domains: the evidence structure is expertise-implementation relational, not domain-specific.

Domain-agnostic standard: satisfied. No per-domain tuning required.

### 5.5 Minimum Sufficient Evidence

EXPERTISE_GAP_AWARENESS requires evidence of: (1) named expertise domain with implementation justification, (2) self-assessment distinguishing known from unknown with reasoning, (3) consequence awareness specific to the inventor's mechanism. These three are necessary and sufficient to distinguish genuine expertise gap awareness from boundary ambiguity restated as expertise acknowledgment. No additional evidence requirements are proposed.

---

## 6. CROSS-GAP EVIDENCE CONSIDERATIONS

### 6.1 Evidence Progression Across Gap Types

The three gap types have a logical dependency (STAGE3_GAP_TAXONOMY_PROPOSAL §3.1). The evidence model reflects this:

PMF evidence (§3) establishes which problem the mechanism is intended to solve. This scopes the assumption inventory -- assumptions are about a mechanism-problem relationship, not a mechanism in isolation.

AI evidence (§4) names the assumptions underlying that mechanism-problem relationship. This scopes expertise gap identification -- expertise gaps are those required to validate or resolve the load-bearing assumptions.

EGA evidence (§5) identifies the expertise required to resolve those assumptions. This connects to the Stage 3 exit characterization: the inventor can now define a proof-of-concept objective (what would validate a load-bearing assumption) and identify a prioritized next action (engaging the expertise most critical to resolving it).

### 6.2 Protocol Learning Mitigation Across All Gap Types

Risk B (protocol learning) is present across all three gap types. The mitigation is consistent: evidence must be traceable to the inventor's specific mechanism, not to generic knowledge about the gap type.

An inventor who produces textbook-correct responses about problem-mechanism fit, assumption inventory, or expertise gaps without connecting those responses to their specific mechanism and implementation context has demonstrated protocol familiarity, not genuine Stage 3 development.

The Transfer of Reasoning test from SR-001 §3.7 applies: genuine Stage 3 development transfers across different aspects of the same invention. Protocol learning produces correct responses for familiar question patterns but fails when the question probes an unfamiliar aspect of the same mechanism.

---

## 7. EVIDENCE SUMMARY TABLE

| Gap Type | Evidence ID | Underlying Capability | Stage 3 Specific? |
|---|---|---|---|
| PROBLEM_MECHANISM_FIT | PMF-E1 | Independent problem articulation | Yes -- Stage 2 does not require it |
| PROBLEM_MECHANISM_FIT | PMF-E2 | Causal fit justification | Yes -- different causal relationship than Stage 2 |
| PROBLEM_MECHANISM_FIT | PMF-E3 | Fit boundary awareness | Yes -- different boundary than Stage 2 BA |
| ASSUMPTION_INVENTORY | AI-E1 | Named assumptions beyond known gaps | Yes -- different epistemic act than gap identification |
| ASSUMPTION_INVENTORY | AI-E2 | Load-bearing classification with reasoning | Yes -- implementation-oriented dependency reasoning |
| ASSUMPTION_INVENTORY | AI-E3 | Assumption provenance awareness | Yes -- demonstrates Unknown Awareness growth |
| EXPERTISE_GAP_AWARENESS | EGA-E1 | Named expertise with implementation justification | Yes -- forward-looking beyond Stage 2 boundary |
| EXPERTISE_GAP_AWARENESS | EGA-E2 | Self-assessment with reasoning | Yes -- implementation-oriented self-evaluation |
| EXPERTISE_GAP_AWARENESS | EGA-E3 | Consequence awareness specific to mechanism | Yes -- connects expertise to implementation path |

Nine evidence items total. Three per gap type. Each demonstrating a Stage 3-specific capability.

---

## 8. WHAT THIS DOCUMENT DOES NOT DEFINE

- No evaluation model (REASONED vs ASSERTED criteria for Stage 3)
- No substance signals
- No questions
- No scoring
- No progression rules
- No exit conditions
- No implementation
- No domain expansion

---

## 9. NEXT DESIGN ARTIFACT

If this evidence model is accepted, the next artifact is:

**Stage 3 Evaluation Model** -- defining what constitutes REASONED vs ASSERTED quality for each of the nine evidence items, building directly on the evidence definitions established here.

The evaluation model must not introduce new evidence requirements. It must define quality criteria for evidence already defined in this document.

Owner authorization required before evaluation model design begins.

---

*This document is produced to be accurate, not reassuring.*
*Evidence definition precedes evaluation design.*
*Nine evidence items. Three per gap type. Each demonstrating a Stage 3-specific capability.*
*Evidence must demonstrate inventor capability growth, not procedural success, verbosity, protocol familiarity, or domain-specific pattern matching.*
