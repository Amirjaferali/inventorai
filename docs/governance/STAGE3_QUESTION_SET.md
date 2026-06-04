# STAGE3_QUESTION_SET.md
## Stage 3 Question Set

**Document ID:** STAGE3_QUESTION_SET
**Type:** Design Artifact
**Governance Level:** Level 3
**Status:** ADMITTED
**Date:** 2026-06-03
**Provenance:** Owner Authorization -- STAGE3_QUESTION_DESIGN_AUTHORIZATION 3e67339
**Depends on:** STAGE3_QUESTION_TRACEABILITY_METHOD, STAGE3_GAP_EVIDENCE_MODEL, STAGE3_EVALUATION_MODEL

---

## VALIDATION RULES APPLIED

Every question in this document has been reviewed against:
- VR-1: Traceability record complete
- VR-2: Primary Evidence Target unique within question type
- VR-3: Trigger condition defined for all probes
- VR-4: Probing depth limit respected (max 2 levels)
- VR-5: Domain-agnostic validation completed
- VR-6: No prohibited content (no scoring, progression, capability definitions)
- VR-7: Isolation Test -- question proves one evidence item only
- VR-8: Specificity Test -- correct answer requires mechanism-specific reasoning
- VR-9: Human Readability Test -- understandable without prior InventorAI knowledge

---

## PART 1: PROBLEM_MECHANISM_FIT QUESTIONS

### PMF-Q1 (Primary)

**Question Text:**
Without describing how your mechanism works, describe the problem you are trying to solve. What is happening for the person or system that has this problem, and why does it matter to them?

**Q-ID:** PMF-Q1
**Question Type:** PRIMARY
**Primary Evidence Target:** PMF-E1 (independent problem articulation)
**Associated Capability:** PMF-CAP
**Associated Resolution Condition:** PMF-R1
**Domain-Agnostic Validation:** Electronics -- works for sensor inventor describing measurement gap. Solar -- works for energy inventor describing power availability gap. Medical -- works for device inventor describing clinical need. Software -- works for algorithm inventor describing computational problem. No domain-specific language required.
**Protocol Learning Resistance:** The instruction 'without describing how your mechanism works' prevents restatement of mechanism as problem. A template answer cannot satisfy this without genuine problem articulation.
**VR-7 Isolation:** Proves only PMF-E1. Does not require PMF-E2 or PMF-E3 to answer.
**VR-8 Specificity:** Correct answer is unique to each inventor's problem context.
**VR-9 Readability:** Accessible to non-specialist inventors. No technical jargon.

---

### PMF-Q1-P1 (Conditional Probe)

**Question Text:**
You have described the problem. Now, looking at your mechanism specifically -- what is it about your mechanism that addresses exactly that problem, rather than a different problem?

**Q-ID:** PMF-Q1-P1
**Question Type:** CONDITIONAL_PROBE
**Trigger Condition:** PMF-Q1 response describes the problem in terms that closely mirror the mechanism description, suggesting the problem and mechanism have not been independently articulated.
**Primary Evidence Target:** PMF-E1 (independent problem articulation -- probing stability)
**Associated Capability:** PMF-CAP
**Associated Resolution Condition:** PMF-R1
**Domain-Agnostic Validation:** Applies across all domains without modification.
**VR-7 Isolation:** Still targets PMF-E1 stability, not PMF-E2.
**VR-8 Specificity:** Forces mechanism-problem connection that is unique to each inventor.
**VR-9 Readability:** Conversational follow-up, accessible.

---

### PMF-Q2 (Primary)

**Question Text:**
Why does your mechanism solve this problem rather than a different approach? What is it about how your mechanism works that makes it the right fit for this problem?

**Q-ID:** PMF-Q2
**Question Type:** PRIMARY
**Primary Evidence Target:** PMF-E2 (causal fit justification)
**Associated Capability:** PMF-CAP
**Associated Resolution Condition:** PMF-R2
**Domain-Agnostic Validation:** Electronics -- why does this circuit address this measurement need. Solar -- why does this collection approach address this power need. Medical -- why does this device mechanism address this clinical need. Software -- why does this algorithm address this computational need.
**Protocol Learning Resistance:** Requires causal reasoning from mechanism properties to problem requirements. Cannot be answered by asserting fit. 'Because it was designed to' does not satisfy this question.
**VR-7 Isolation:** Proves PMF-E2 only. Presupposes PMF-E1 but does not require demonstrating it within this answer.
**VR-8 Specificity:** Correct answer must reference specific mechanism properties of the inventor's design.
**VR-9 Readability:** Natural language, accessible to non-specialist.

---

### PMF-Q2-P1 (Conditional Probe)

**Question Text:**
Can you walk me through the connection more specifically? Which part of your mechanism directly addresses which part of the problem?

**Q-ID:** PMF-Q2-P1
**Question Type:** CONDITIONAL_PROBE
**Trigger Condition:** PMF-Q2 response asserts fit without providing a mechanism-property-to-problem-requirement causal chain.
**Primary Evidence Target:** PMF-E2 (causal fit justification -- probing specificity)
**Associated Capability:** PMF-CAP
**Associated Resolution Condition:** PMF-R2
**Domain-Agnostic Validation:** Applies across all domains.
**VR-7 Isolation:** Targets PMF-E2 specificity only.
**VR-8 Specificity:** Forces part-level connection unique to inventor's design.
**VR-9 Readability:** Conversational, accessible.

---

### PMF-Q3 (Primary)

**Question Text:**
Are there situations or conditions where your mechanism would not solve this problem, or would solve it less well? What are those conditions?

**Q-ID:** PMF-Q3
**Question Type:** PRIMARY
**Primary Evidence Target:** PMF-E3 (fit boundary awareness)
**Associated Capability:** PMF-CAP
**Associated Resolution Condition:** PMF-R3
**Domain-Agnostic Validation:** Electronics -- conditions under which sensor loses accuracy. Solar -- conditions under which collection efficiency drops. Medical -- patient populations where device is less effective. Software -- input conditions where algorithm degrades.
**Protocol Learning Resistance:** An inventor who asserts 'it works in all conditions' has not demonstrated fit boundary awareness. The question requires the inventor to identify a genuine limitation, which cannot be answered by a generic template.
**VR-7 Isolation:** Proves PMF-E3 only. Independent of PMF-E1 and PMF-E2.
**VR-8 Specificity:** Correct answer is mechanism-specific -- cannot be answered generically.
**VR-9 Readability:** Direct and accessible. 'Less well' provides an easier entry point than 'fails completely'.

---

### PMF-Q3-P1 (Conditional Probe)

**Question Text:**
For the condition you named -- in that situation, what happens to the problem? Does it go unsolved, or does it get solved by something else?

**Q-ID:** PMF-Q3-P1
**Question Type:** CONDITIONAL_PROBE
**Trigger Condition:** PMF-Q3 response names a condition but does not clarify whether the fit limit is a full failure or a partial degradation.
**Primary Evidence Target:** PMF-E3 (fit boundary awareness -- probing precision)
**Associated Capability:** PMF-CAP
**Associated Resolution Condition:** PMF-R3
**Domain-Agnostic Validation:** Applies across all domains.
**VR-7 Isolation:** Targets PMF-E3 precision only.
**VR-8 Specificity:** Answer is specific to the condition the inventor named.
**VR-9 Readability:** Natural follow-up, non-technical.

---

## PART 2: ASSUMPTION_INVENTORY QUESTIONS

### AI-Q1 (Primary)

**Question Text:**
What are you taking for granted about your mechanism that you have not yet tested or verified? These might be things you expect to be true, materials you assume are available, or conditions you assume will hold.

**Q-ID:** AI-Q1
**Question Type:** PRIMARY
**Primary Evidence Target:** AI-E1 (named assumptions beyond known gaps)
**Associated Capability:** AI-CAP
**Associated Resolution Condition:** AI-R1
**Domain-Agnostic Validation:** Electronics -- assumed component tolerances, signal behavior. Solar -- assumed irradiance levels, storage capacity. Medical -- assumed patient compliance, clinical environment. Software -- assumed data availability, API behavior. No domain-specific language required.
**Protocol Learning Resistance:** 'Taking for granted' and 'not yet tested' frame assumptions differently from gaps. An inventor who lists only known Stage 2 gaps has not answered this question. The phrase 'things you expect to be true' invites assumptions the inventor may not have recognized.
**VR-7 Isolation:** Proves AI-E1 only -- named assumptions distinct from known gaps.
**VR-8 Specificity:** Assumptions are mechanism-specific and unique to each inventor.
**VR-9 Readability:** Accessible phrasing with examples to guide non-specialist inventors.

---

### AI-Q1-P1 (Conditional Probe)

**Question Text:**
Of the assumptions you just named, which ones would cause the biggest problem for your mechanism if they turned out to be wrong?

**Q-ID:** AI-Q1-P1
**Question Type:** CONDITIONAL_PROBE
**Trigger Condition:** AI-Q1 response names assumptions but does not distinguish between those that would critically affect the mechanism and those that would not.
**Primary Evidence Target:** AI-E1 (named assumptions -- probing criticality awareness, bridging to AI-E2)
**Associated Capability:** AI-CAP
**Associated Resolution Condition:** AI-R1
**Domain-Agnostic Validation:** Applies across all domains.
**VR-7 Isolation:** Targets AI-E1 depth. Note: this probe bridges toward AI-E2 but does not require full AI-E2 demonstration -- it asks for intuitive criticality, not formal load-bearing classification.
**VR-8 Specificity:** Answer depends on specific assumptions named by the inventor.
**VR-9 Readability:** Natural, accessible follow-up.

---

### AI-Q2 (Primary)

**Question Text:**
For each assumption you named, would your mechanism still work if that assumption turned out to be wrong? Which assumptions are essential -- the mechanism fails without them -- and which ones would just require you to adjust your approach?

**Q-ID:** AI-Q2
**Question Type:** PRIMARY
**Primary Evidence Target:** AI-E2 (load-bearing classification with reasoning)
**Associated Capability:** AI-CAP
**Associated Resolution Condition:** AI-R2
**Domain-Agnostic Validation:** The essential/adjust framing applies across all domains without domain-specific language.
**Protocol Learning Resistance:** Requires the inventor to apply the essential/peripheral distinction to their specific assumptions with reasoning. A generic answer ('all my assumptions are essential') does not satisfy this -- the question requires classification with justification.
**VR-7 Isolation:** Proves AI-E2 (load-bearing classification). Presupposes AI-E1 named assumptions exist but does not re-elicit them.
**VR-8 Specificity:** Classification must reference the inventor's specific assumptions and mechanism.
**VR-9 Readability:** 'Essential -- the mechanism fails' and 'just require you to adjust' are accessible non-technical framings of load-bearing vs peripheral.

---

### AI-Q2-P1 (Conditional Probe)

**Question Text:**
For the assumption you called essential -- can you explain why the mechanism fails if that assumption is wrong? What specifically breaks down?

**Q-ID:** AI-Q2-P1
**Question Type:** CONDITIONAL_PROBE
**Trigger Condition:** AI-Q2 response classifies an assumption as essential without providing a causal explanation for why the mechanism fails.
**Primary Evidence Target:** AI-E2 (load-bearing classification -- probing causal reasoning)
**Associated Capability:** AI-CAP
**Associated Resolution Condition:** AI-R2
**Domain-Agnostic Validation:** Applies across all domains.
**VR-7 Isolation:** Targets AI-E2 causal depth only.
**VR-8 Specificity:** Answer is specific to the assumption and mechanism named.
**VR-9 Readability:** Direct, accessible follow-up.

---

### AI-Q3 (Primary)

**Question Text:**
Now that you have thought through your assumptions -- is there anything you realize you were assuming that you had not recognized as an assumption before this conversation? Something that seemed obvious but is actually unverified?

**Q-ID:** AI-Q3
**Question Type:** PRIMARY
**Primary Evidence Target:** AI-E3 (assumption provenance awareness)
**Associated Capability:** AI-CAP
**Associated Resolution Condition:** AI-R3
**Domain-Agnostic Validation:** The question is meta-cognitive and domain-independent. Applies across all domains.
**Protocol Learning Resistance:** This question cannot be answered by a template. It requires the inventor to have genuinely discovered something new about their own thinking during this Stage 3 session. A pre-prepared answer would be implausible.
**VR-7 Isolation:** Proves AI-E3 (provenance awareness) only. The discovery must be new to this session.
**VR-8 Specificity:** Answer is unique to each inventor's session experience.
**VR-9 Readability:** 'Something that seemed obvious but is actually unverified' is accessible and conversational.

---

### AI-Q3-P1 (Conditional Probe)

**Question Text:**
Why did you not identify that as an assumption earlier? What made it seem like a given rather than something to verify?

**Q-ID:** AI-Q3-P1
**Question Type:** CONDITIONAL_PROBE
**Trigger Condition:** AI-Q3 response names a newly recognized assumption but does not explain why it was previously unrecognized.
**Primary Evidence Target:** AI-E3 (assumption provenance -- probing awareness depth)
**Associated Capability:** AI-CAP
**Associated Resolution Condition:** AI-R3
**Domain-Agnostic Validation:** Applies across all domains.
**VR-7 Isolation:** Targets AI-E3 provenance depth only.
**VR-8 Specificity:** Answer is specific to the inventor's cognitive process.
**VR-9 Readability:** Accessible meta-cognitive question.

---

## PART 3: EXPERTISE_GAP_AWARENESS QUESTIONS

### EGA-Q1 (Primary)

**Question Text:**
What areas of technical knowledge would someone need to actually build or implement your mechanism? List the domains of expertise required -- not what you know, but what the implementation itself demands.

**Q-ID:** EGA-Q1
**Question Type:** PRIMARY
**Primary Evidence Target:** EGA-E1 (named expertise with implementation justification)
**Associated Capability:** EGA-CAP
**Associated Resolution Condition:** EGA-R1
**Domain-Agnostic Validation:** Electronics -- firmware, power management, PCB design. Solar -- power electronics, grid integration. Medical -- regulatory pathway, biocompatibility. Software -- systems architecture, security. The question is framed around implementation demands, not domain-specific knowledge.
**Protocol Learning Resistance:** 'Not what you know, but what the implementation itself demands' separates expertise identification from self-assessment. This framing prevents generic answers about the importance of having experts.
**VR-7 Isolation:** Proves EGA-E1 (named expertise with implementation connection). Does not require self-assessment (EGA-E2).
**VR-8 Specificity:** Expertise domains must be connected to the specific implementation requirements of the inventor's mechanism.
**VR-9 Readability:** Accessible. 'What the implementation itself demands' is clear non-technical framing.

---

### EGA-Q1-P1 (Conditional Probe)

**Question Text:**
For each expertise area you named -- can you say specifically what aspect of your mechanism requires it? What would go wrong if someone tried to implement your mechanism without that expertise?

**Q-ID:** EGA-Q1-P1
**Question Type:** CONDITIONAL_PROBE
**Trigger Condition:** EGA-Q1 response lists expertise domains without connecting them to specific implementation requirements of the inventor's mechanism.
**Primary Evidence Target:** EGA-E1 (named expertise -- probing implementation connection)
**Associated Capability:** EGA-CAP
**Associated Resolution Condition:** EGA-R1
**Domain-Agnostic Validation:** Applies across all domains.
**VR-7 Isolation:** Targets EGA-E1 connection depth only.
**VR-8 Specificity:** Answer requires mechanism-specific implementation reasoning.
**VR-9 Readability:** Direct, accessible follow-up.

---

### EGA-Q2 (Primary)

**Question Text:**
Of the expertise areas you just identified -- which ones do you have sufficient working knowledge of to proceed, and which ones represent genuine gaps where you would need to learn more or bring in someone else?

**Q-ID:** EGA-Q2
**Question Type:** PRIMARY
**Primary Evidence Target:** EGA-E2 (self-assessment with reasoning)
**Associated Capability:** EGA-CAP
**Associated Resolution Condition:** EGA-R2
**Domain-Agnostic Validation:** The known/gap framing applies across all domains.
**Protocol Learning Resistance:** Requires honest self-assessment relative to specific expertise demands. 'I would need to learn more or bring in someone else' acknowledges real gaps. A generic answer ('I have all the knowledge I need') does not satisfy this question.
**VR-7 Isolation:** Proves EGA-E2 (self-assessment). Presupposes EGA-E1 expertise list but does not re-elicit it.
**VR-8 Specificity:** Assessment must reference the specific expertise domains named in EGA-Q1.
**VR-9 Readability:** 'Sufficient working knowledge' and 'genuine gaps' are accessible framings.

---

### EGA-Q2-P1 (Conditional Probe)

**Question Text:**
For the gaps you identified -- why do you say you lack sufficient knowledge there? What specifically would you need to know that you do not currently know?

**Q-ID:** EGA-Q2-P1
**Question Type:** CONDITIONAL_PROBE
**Trigger Condition:** EGA-Q2 response identifies expertise gaps without providing reasoning for why knowledge is insufficient.
**Primary Evidence Target:** EGA-E2 (self-assessment -- probing reasoning specificity)
**Associated Capability:** EGA-CAP
**Associated Resolution Condition:** EGA-R2
**Domain-Agnostic Validation:** Applies across all domains.
**VR-7 Isolation:** Targets EGA-E2 reasoning depth only.
**VR-8 Specificity:** Answer is specific to the gaps named by the inventor.
**VR-9 Readability:** Accessible, direct follow-up.

---

### EGA-Q3 (Primary)

**Question Text:**
For the expertise gaps you identified -- what would happen to your implementation if those gaps were not addressed before you started building? What specific problems would you run into?

**Q-ID:** EGA-Q3
**Question Type:** PRIMARY
**Primary Evidence Target:** EGA-E3 (consequence awareness specific to mechanism)
**Associated Capability:** EGA-CAP
**Associated Resolution Condition:** EGA-R3
**Domain-Agnostic Validation:** Consequence reasoning applies across all domains. Electronics -- failed PCB layout. Solar -- grid integration failure. Medical -- regulatory rejection. Software -- security vulnerability.
**Protocol Learning Resistance:** Requires specific consequence reasoning connected to the inventor's mechanism. 'Problems would arise' is not sufficient. The inventor must name what specifically breaks down in their specific implementation.
**VR-7 Isolation:** Proves EGA-E3 (consequence awareness). Independent of EGA-E1 and EGA-E2 in content, though logically follows from them.
**VR-8 Specificity:** Consequences must be specific to the inventor's mechanism and implementation path.
**VR-9 Readability:** 'What would happen' and 'what specific problems' are accessible framings.

---

### EGA-Q3-P1 (Conditional Probe)

**Question Text:**
Of those problems -- which one would be hardest to recover from once you had already started building? Why?

**Q-ID:** EGA-Q3-P1
**Question Type:** CONDITIONAL_PROBE
**Trigger Condition:** EGA-Q3 response names consequences without distinguishing between recoverable and non-recoverable problems.
**Primary Evidence Target:** EGA-E3 (consequence awareness -- probing severity reasoning)
**Associated Capability:** EGA-CAP
**Associated Resolution Condition:** EGA-R3
**Domain-Agnostic Validation:** Applies across all domains.
**VR-7 Isolation:** Targets EGA-E3 consequence depth only.
**VR-8 Specificity:** Severity assessment is specific to the inventor's implementation path.
**VR-9 Readability:** 'Hardest to recover from' is accessible and intuitive.

---

## PART 4: COHERENCE QUESTIONS

### COH-Q1 (Primary -- CCT-1)

**Question Text:**
Looking at the assumptions you identified earlier -- are any of them assumptions about the problem itself, rather than about your mechanism? Are you assuming anything about who has the problem, how severe it is, or whether your solution addresses what they actually need?

**Q-ID:** COH-Q1
**Question Type:** PRIMARY
**Coherence Test Target:** CCT-1 (internal consistency -- PMF articulation consistent with AI assumption inventory)
**Associated Capability:** IOC (per IOC_POSITION_STATEMENT)
**Associated Resolution Condition:** SL-R2
**Domain-Agnostic Validation:** Problem-assumption consistency applies across all domains.
**Protocol Learning Resistance:** Requires the inventor to cross-reference their problem articulation with their assumption inventory -- a synthesis act that cannot be pre-prepared.
**VR-7 Isolation:** Targets CCT-1 only -- internal consistency between PMF and AI.
**VR-8 Specificity:** Answer requires connecting specific assumptions to specific problem articulation.
**VR-9 Readability:** Accessible, no technical jargon.

---

### COH-Q2 (Primary -- CCT-2)

**Question Text:**
Looking at the essential assumptions you identified -- which of them would require expertise you said you do not have to verify or validate? Are there assumptions that you cannot check yourself?

**Q-ID:** COH-Q2
**Question Type:** PRIMARY
**Coherence Test Target:** CCT-2 (dependency alignment -- load-bearing assumptions connected to expertise gaps)
**Associated Capability:** IOC (per IOC_POSITION_STATEMENT)
**Associated Resolution Condition:** SL-R2
**Domain-Agnostic Validation:** Assumption-expertise dependency applies across all domains.
**Protocol Learning Resistance:** Requires cross-referencing essential assumptions with expertise gaps -- a synthesis act across two gap types.
**VR-7 Isolation:** Targets CCT-2 dependency alignment only.
**VR-8 Specificity:** Requires connecting specific essential assumptions to specific expertise gaps.
**VR-9 Readability:** Accessible. 'Cannot check yourself' is intuitive.

---

### COH-Q3 (Primary -- CCT-3)

**Question Text:**
Based on everything you have worked through -- the problem your mechanism addresses, the assumptions you are making, and the expertise gaps you have identified -- what would you do next if you were going to move forward with this? What is the most important thing to resolve first, and why?

**Q-ID:** COH-Q3
**Question Type:** PRIMARY
**Coherence Test Target:** CCT-3 (problem-path alignment -- next action follows from PMF+AI+EGA combined)
**Associated Capability:** IOC (per IOC_POSITION_STATEMENT)
**Associated Resolution Condition:** SL-R2 and SL-R3
**Domain-Agnostic Validation:** Next action reasoning applies across all domains.
**Protocol Learning Resistance:** 'The most important thing to resolve first, and why' requires synthesis of all three gap types. The justification must connect to the specific combination of problem, assumptions, and expertise gaps -- not a generic next step.
**VR-7 Isolation:** Targets CCT-3 and simultaneously contributes to SL-R3 exit characterization.
**VR-8 Specificity:** Next action and justification are specific to the inventor's complete Stage 3 picture.
**VR-9 Readability:** Natural, conversational. 'If you were going to move forward' is accessible framing.

---

## QUESTION SET SUMMARY

| Q-ID | Type | Primary Target | Capability | Resolution |
|---|---|---|---|---|
| PMF-Q1 | PRIMARY | PMF-E1 | PMF-CAP | PMF-R1 |
| PMF-Q1-P1 | PROBE | PMF-E1 | PMF-CAP | PMF-R1 |
| PMF-Q2 | PRIMARY | PMF-E2 | PMF-CAP | PMF-R2 |
| PMF-Q2-P1 | PROBE | PMF-E2 | PMF-CAP | PMF-R2 |
| PMF-Q3 | PRIMARY | PMF-E3 | PMF-CAP | PMF-R3 |
| PMF-Q3-P1 | PROBE | PMF-E3 | PMF-CAP | PMF-R3 |
| AI-Q1 | PRIMARY | AI-E1 | AI-CAP | AI-R1 |
| AI-Q1-P1 | PROBE | AI-E1 | AI-CAP | AI-R1 |
| AI-Q2 | PRIMARY | AI-E2 | AI-CAP | AI-R2 |
| AI-Q2-P1 | PROBE | AI-E2 | AI-CAP | AI-R2 |
| AI-Q3 | PRIMARY | AI-E3 | AI-CAP | AI-R3 |
| AI-Q3-P1 | PROBE | AI-E3 | AI-CAP | AI-R3 |
| EGA-Q1 | PRIMARY | EGA-E1 | EGA-CAP | EGA-R1 |
| EGA-Q1-P1 | PROBE | EGA-E1 | EGA-CAP | EGA-R1 |
| EGA-Q2 | PRIMARY | EGA-E2 | EGA-CAP | EGA-R2 |
| EGA-Q2-P1 | PROBE | EGA-E2 | EGA-CAP | EGA-R2 |
| EGA-Q3 | PRIMARY | EGA-E3 | EGA-CAP | EGA-R3 |
| EGA-Q3-P1 | PROBE | EGA-E3 | EGA-CAP | EGA-R3 |
| COH-Q1 | PRIMARY | CCT-1 | IOC | SL-R2 |
| COH-Q2 | PRIMARY | CCT-2 | IOC | SL-R2 |
| COH-Q3 | PRIMARY | CCT-3 | IOC + SL-R3 | SL-R2 + SL-R3 |

**Total: 21 questions (9 primary gap questions + 9 conditional probes + 3 coherence questions)**

SC-1 Coverage: 9 evidence items covered by primary questions. Satisfied.
SC-3 Protocol Resistance: Each gap type has conditional probes targeting unfamiliar aspects. Satisfied.
SC-4 Coherence Coverage: CCT-1, CCT-2, CCT-3 each have a dedicated question. Satisfied.
SC-5 Domain-Agnostic: All 21 questions validated across four domain contexts. Satisfied.
SC-6 No Prohibited Content: No scoring, progression, capability definitions, or resolution conditions in question text. Satisfied.

---

*This document is produced to be accurate, not reassuring.*
*Every question knows its architectural purpose.*
*Questions elicit evidence. They do not evaluate it.*
