# PATH N QUESTION CONTENT SPECIFICATION

## 1. Status

COMMITTED PATH N QUESTION CONTENT SPECIFICATION — NO IMPLEMENTATION AUTHORIZED

Date: 2026-06-11

This is the O-4 governance artifact authorized after Functional Path N implementation plan cf63f13.

Content is specified before any code, domain file, prompt, route, session, or test changes.

## 2. Source Governance

- FUNCTIONAL_PATH_N_IMPLEMENTATION_PLAN.md — commit cf63f13
- MVP_SCOPE_FREEZE_AMENDMENT_FUNCTIONAL_PATH_N.md — commit cdcd079
- MVP_SCOPE_REVISION_DECISION_RECORD.md — commit ccd1ecd
- NON_SPECIALIST_QUESTIONING_POLICY.md — commit a31010a
- Characterization tests — commit 72b5f11
- R-2_R1_PRODUCT_ALIGNMENT_DRIFT_RECORD.md — commit 10d6876

## 3. Content Objective

Path N questions allow a non-technical inventor to continue the Stage 1-3 guided journey without early engineering-gated blockers.

Path N does not remove gaps.

Path N changes how gaps are asked and recorded.

Missing engineering knowledge remains a known unknown or feasibility gap.

## 4. Allowed Path N Question Categories

Path N may ask about:

- idea description
- problem being solved
- beneficiary or affected user
- context of use
- current failure or pain point
- desired outcome
- rough mechanism in plain language
- assumptions in plain language
- known unknowns
- what information would be needed later
- evidence or observations the user already has
- what would make the idea useful or not useful

## 5. Disallowed Early Gate Categories

Path N must not use these early as gates:

- voltage
- current
- frequency
- circuit architecture
- component-level selection
- signal transformation
- datasheet-level requirements
- engineering calculations
- manufacturing tolerances

These may be recorded as future engineering unknowns, not demanded as early answers.

## 6. Gap Mapping

### MECHANISM_COMPLETENESS

Technical-style question:

"Describe how your electronic circuit achieves its intended function."

Path N equivalent:

"Explain in everyday words how you imagine the system would notice the problem and respond."

### PHYSICAL_FEASIBILITY

Technical-style question:

"Do you know the voltage/current/frequency requirements?"

Path N equivalent:

"What would need to be true for this system to work safely, and what information would you need later to confirm it?"

### BOUNDARY_AMBIGUITY

Path N question:

"When should the system work, when should it not work, and what situations might confuse it?"

## 7. R1 Regression Prevention

R1 is the canonical negative example.

Path N must not repeat the R1 pattern:

- circuit function
- electronic components
- signal or energy transformation
- power source
- voltage/current/frequency
- repeated electrical constraints

Path N must reframe repeated stalls instead of repeating the same engineering-gated question.

On stall, the next question moves to:

- what the user does know
- a plainer phrasing
- known-unknown capture
- what information would be needed later

## 8. Proposed Path N Question Set

### MECHANISM_COMPLETENESS

N-MC-1: "Explain in everyday words how you imagine the system would notice the problem and respond."

N-MC-2: "What are the main parts of your idea, in your own words, and what does each part do?"

N-MC-3: "Walk through what happens step by step, from the moment the problem starts to the moment someone knows about it."

N-MC-4: "Is there any part of how it works that you're unsure about or imagining loosely? Describe it as best you can."

### PHYSICAL_FEASIBILITY

N-PF-1: "What would need to be true for this system to work safely, and what information would you need later to confirm it?"

N-PF-2: "What do you think would keep the system running, and what do you not know yet about that?"

N-PF-3: "Are there real-world conditions, such as heat, water, time, or wear, that might stop it from working? Which ones worry you most?"

N-PF-4: "If an engineer offered to check one thing about whether this can physically work, what would you ask them to check first?"

### BOUNDARY_AMBIGUITY

N-BA-1: "When should the system work, when should it not work, and what situations might confuse it?"

N-BA-2: "What is your idea responsible for, and what is someone or something else's job?"

N-BA-3: "Describe a situation where the system should definitely react, and one where it should definitely stay quiet."

## 9. Known Unknowns Recording Rule

When the user does not know engineering details, Path N asks:

1. What they do know.
2. What they suspect.
3. What information would be needed.
4. Who or what could verify it later.

The missing engineering detail is recorded as an unknown, not treated as immediate failure.

The gap remains open or partial under the deterministic engine's normal rules.

## 10. Test Implication Later

No tests are modified by this specification.

Later tests may validate this specification artifact before runtime integration.

The existing xfail in 72b5f11 remains xfail until approved Path N content is integrated and verified.

## 11. Governance Effect

- code changes are not authorized
- prompt changes are not authorized
- question-bank changes are not authorized
- tests are not modified
- implementation is not authorized
- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked

## 12. Required Next Owner Decision

The owner must decide:

1. Whether to approve the question content.
2. Whether to authorize tests against the specification artifact.
3. Whether to authorize integration into domain or question files later.
4. Whether R2 remains held until integrated Path N evidence exists.

## 13. Boundary Statement

No code was modified by this specification.

No prompts were modified by this specification.

No domain question bank was modified by this specification.

No routes were modified by this specification.

No engine logic was modified by this specification.

No tests were modified by this specification.

No FORM T comparison has been performed.

No S-6 classification has been performed.

No AA-5 verdict has been started.

R2 remains HELD.

AA-4 final S-6 classification has NOT been performed.
