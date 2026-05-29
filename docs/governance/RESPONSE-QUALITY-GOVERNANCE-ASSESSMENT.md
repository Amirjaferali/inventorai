# Response Quality Governance Assessment

**Document type:** Governance assessment only
**Date:** 2026-05-30
**Last updated:** 2026-05-30
**Requested by:** Owner — post ILT-001 closure
**Status:** Assessment only — no implementation authorized
**Depends on:** GD-001, GD-002

---

## 1. Problem Definition

The platform currently distinguishes ASSERTED from REASONED responses using
assess_response(). This classifier detects causal structure. It was not
designed to detect the absence of meaningful participation.

These are two different problems.

The existing problem (solved): Does this response contain genuine causal
reasoning, or does it merely assert outcomes?

The new problem (unsolved): Does this response represent a genuine attempt
to engage, or is it noise, filler, repetition, or non-participation that
should not advance the session at all?

The distinction matters because the existing classifier correctly scores
asdfasdfasdf as ASSERTED — technically accurate — but ASSERTED still affects
gap state (sets PARTIAL). A noise response should not affect gap state.
It should be rejected before classification.

---

## 2. The Participation Floor vs the Quality Floor

Participation Floor: Did the inventor make a genuine attempt to respond?
Binary. Either genuine or not.

Quality Floor: Is the response ASSERTED or REASONED? A quality gradient
applied after the participation floor is passed.

Currently the platform has only a Quality Floor. It has no Participation
Floor. Any string of 40+ characters passes into the classifier regardless
of whether it represents genuine participation.

The proposed Response Quality Contract from GD-002 is a Participation Floor,
not a Quality Floor upgrade.

---

## 3. Scope Constraint — What the Participation Floor Must Not Evaluate

The Participation Floor must not be used to evaluate:

- engineering correctness
- expertise level
- educational background
- domain specialization

Its sole purpose is to distinguish participation from non-participation.

This constraint is not negotiable. InventorAI is intended to support
non-specialist inventors. A floor that penalizes domain-naive language,
informal reasoning style, or non-technical vocabulary would contradict
the core product purpose defined in GD-002.

A non-specialist inventor who writes "I think the water makes the electricity
behave differently" is participating. The response is ASSERTED in quality.
It is not non-participation.

The floor must protect this inventor, not reject them.

---

## 4. Categories of Non-Participation

Category 1 — Keyboard noise
Random character sequences. No words, syntax, or semantic content.
Examples: 444444444444, asdfasdfasdf

Category 2 — Filler repetition
Repeated words or phrases. Linguistic tokens present, zero information density.
Example: I don't know I don't know I don't know

Category 3 — Off-topic responses
Valid text with no connection to the question asked.

Category 4 — Content-free acknowledgment
Acknowledges the question without answering it.
Examples: I understand, okay, yes that sounds right

Category 5 — Restated question
The inventor reflects the question back as an answer.
Example: Platform asks about physical principle; inventor responds
"the physical principle my mechanism relies on is important."

Category 6 — AI Echo Response
The inventor copies or paraphrases platform-provided guidance without
contributing original reasoning, assumptions, constraints, decisions,
trade-offs, or analysis.

Example: The platform explains that capacitive sensing works by measuring
dielectric constant changes. The inventor responds with a near-verbatim
restatement of this explanation.

The response may appear high quality and score REASONED in the existing
classifier, while demonstrating no original inventor understanding.

This category is currently low-risk because the platform does not provide
significant technical guidance in the current lifecycle. It becomes a
foreseeable governance concern if a Technical Guidance layer is introduced
under GD-002. AI Echo assessment must be explicitly revisited before any
Technical Guidance layer is deployed.

Distinguishing feature from other categories: AI Echo responses are not
empty — they contain genuine domain content. The governance problem is
provenance, not quality. The content originated with the platform, not
the inventor. This connects directly to the knowledge source separation
requirement in GD-002 and the Inventor Ownership Principle.

---

## 5. Governance Risks

Risk 1 — False rejection of non-specialist inventors (primary risk)
The floor must be calibrated on participation intent, not domain vocabulary.

Risk 2 — Gaming by surface compliance
An inventor who learns the system can produce a response that passes the
floor while providing no genuine content. The floor must detect Category 5.

Risk 3 — Stall interaction
The floor and stall detection are related but distinct. If not coordinated,
a non-participating inventor could cycle between slightly varied noise
responses, passing the floor while evading stall detection. Governance must
define how these two mechanisms interact.

Risk 4 — Classifier boundary creep
Any implementation must be a pre-classifier gate, not a modification to
the existing assess_response() function.

Risk 5 — Inventor experience degradation
Rejection must be accompanied by clear non-technical guidance. The floor
cannot be a silent barrier.

Risk 6 — AI Echo amplification under Technical Guidance
If a future Technical Guidance layer provides detailed explanations,
AI Echo responses become systematically more likely. The classifier
may score them as REASONED. The Inventor Ownership Principle would be
violated at scale. This risk does not require immediate mitigation but
must be tracked and assessed before GD-002 implementation begins.

---

## 6. Iteration Governance Observation

The question of whether floor rejection should count as an iteration is
unresolved. Before design begins, the following governance observation
is recorded:

Rejected non-participation should not automatically be treated as a valid
inventor iteration.

Keyboard noise, filler repetition, and content-free acknowledgements should
not consume meaningful inventor progress. If floor rejections count as
iterations, a non-participating inventor could exhaust stall detection
without ever making a genuine response.

If floor rejections do not count as iterations, the iteration count becomes
a record of genuine participation attempts only. This is more aligned with
the intent of the iteration log as an evidence record.

This is not an implementation decision. It is a governance constraint that
must be respected during future design.

---

## 7. Connection to Inventor Ownership and GD-002

The Participation Floor exists to protect knowledge integrity.

The chain of dependency is:

Inventor Ownership Principle
  → GD-002 (recommendations are not inventor knowledge)
    → Knowledge Source Separation (inventor knowledge vs platform guidance)
      → Participation Floor (protects the boundary between genuine reasoning
        and non-participation)
        → AI Echo governance (protects against platform content re-entering
          the record as inventor knowledge)

The Participation Floor is not a standalone mechanism. It is one layer in
a governance stack whose purpose is to ensure the invention record contains
only genuine inventor reasoning.

It must not become:
- a correctness gate (rejects wrong answers)
- an expertise gate (rejects non-specialist language)

It must remain:
- a participation gate (rejects non-engagement)

This distinction must be preserved in any future design or implementation.

---

## 8. Candidate Governance Approaches

Approach A — Linguistic Structure Gate
Require minimum distinct word types and sentence count.
Catches: Category 1, partially Category 4.
Weakness: Categories 2 and 5 pass easily. Category 6 passes.

Approach B — Novelty Gate
Require content not present in the question, gap label, or prior response.
Catches: Categories 2 and 5.
Weakness: Short genuine responses may fail if they reuse question vocabulary.
Does not catch Category 6 (AI Echo content is novel relative to prior
inventor responses, but not novel relative to platform guidance).

Approach C — Information Density Signal
Measure ratio of unique meaningful tokens to total tokens.
Catches: Categories 1, 2, partially 4.
Weakness: Does not detect off-topic responses or Category 6.

Approach D — Layered Gate
Apply A, B, C in sequence. Most comprehensive for Categories 1-5.
Does not address Category 6 without an additional provenance check.

Approach E — Stall-first governance
Rely on existing stall detection. No new classification mechanism.
Weakness: Allows 3 non-participating responses before intervention.
Does not address Category 6.

Note on Category 6: AI Echo responses are not detectable by any of the
above approaches without provenance tracking — comparing the inventor
response against prior platform output. This requires a different mechanism
that is not appropriate for the current architecture and must be assessed
separately as part of GD-002 Technical Guidance layer design.

---

## 9. Implications for Multi-Domain Inventor Journeys

The Participation Floor must be domain-agnostic. It cannot require domain
signal words. It must require participation signal regardless of domain
vocabulary.

Any selected approach must be validated against non-specialist response
fixtures from at least two domains before adoption.

The floor must remain stable as new domains are added. Per-domain tuning
would violate the domain-agnostic engine principle.

---

## 10. Relationship to Existing Architecture

MIN_REASONED_RESPONSE_LENGTH: Currently the only participation-adjacent guard.
The floor operates above this threshold.

_CAUSAL_STRUCTURE_PATTERNS: Operates inside assess_response(). The floor
must be upstream — a pre-classifier gate only.

Stall detection: Complementary. The floor catches single instances
immediately. Stall detection catches patterns over multiple turns.
Coordination between floor and stall detection must be defined before
implementation.

---

## 11. Governance Questions Before Design

1. What is the correct response to a floor rejection? Silent re-prompt,
   explicit guidance, or session pause?
2. Should floor rejection count as a valid inventor iteration?
   (Governance observation: it should not — see Section 6.)
3. Is there a maximum number of floor rejections before escalation?
4. Should the floor be uniformly applied across all three gaps?
5. Who governs floor calibration changes?
6. How does Category 6 (AI Echo) governance interact with the Participation
   Floor once a Technical Guidance layer exists?

---

## 12. Assessment Conclusion

The Response Quality Contract is a Participation Floor problem, not a
Quality Floor problem. These are distinct.

The primary governance risk is false rejection of non-specialist inventors.
The secondary governance risk, foreseeable under GD-002, is AI Echo Response
— platform content re-entering the invention record as inventor knowledge.

Of five candidate approaches, Approach D offers the most comprehensive
coverage for Categories 1-5. None of the five approaches addresses
Category 6 without a separate provenance mechanism.

The most defensible path is to answer the six governance questions before
selecting an approach, validate against non-specialist fixtures from at
least two domains, and revisit AI Echo governance explicitly before any
Technical Guidance layer is deployed.

No implementation proposed. No architecture proposed.

---

## 13. Future Dependency

If Technical Guidance is implemented under GD-002, AI Echo Response
governance must be assessed and resolved before deployment. The risk is
low in the current lifecycle because the platform provides minimal
technical guidance. It becomes a primary governance concern once the
platform begins explaining technologies, presenting alternatives, and
recommending paths to inventors.

---

*Assessment date: 2026-05-30*
*Updated: 2026-05-30 — added Category 6 (AI Echo), scope constraint,
iteration governance observation, GD-002 alignment, future dependency note*
*Requested under: GD-002 Response Quality Contract (governance proposal only)*
*Next step: owner review of governance questions 1-6 before any design work*
