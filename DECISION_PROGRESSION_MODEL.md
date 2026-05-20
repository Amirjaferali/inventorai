# DECISION_PROGRESSION_MODEL.md
# Status: PROPOSED — not implemented
# Scope: MVP — electronics/electrical, LEVEL 0-2 only
# Date: 2026-05-20T20:54:20.663309

## 1. PRODUCT PURPOSE
Transform vague invention signal into defensible opportunity.
Not evaluation. Guided maturity discovery.

## 2. IS / IS NOT
IS: guided decision-discovery state machine
IS NOT: form, questionnaire, scoring engine, chatbot

## 3. IDEA STATE (MVP)
maturity_level : 0 | 1 | 2
known.problem  : Evidence | null
known.mechanism: Evidence | null
gaps           : [PHYSICAL_FEASIBILITY | BOUNDARY_AMBIGUITY | MECHANISM_COMPLETENESS]
direction      : PROGRESSING | STALLED | REGRESSING

## 4. MATURITY LEVELS
LEVEL 0: Raw signal — nothing established
LEVEL 1: Problem located — named, recognizable, has beneficiary
LEVEL 2: Solution shaped — mechanism described at functional level

## 5. TRANSITION REQUIREMENTS
0→1: problem quality >= ASSERTED + beneficiary named
1→2: mechanism quality >= REASONED + physical principle named (electronics)
     MECHANISM_COMPLETENESS must not be OPEN

## 6. GAP TYPES (3 only)
PHYSICAL_FEASIBILITY    : does mechanism obey physical constraints?
BOUNDARY_AMBIGUITY      : can invention be distinguished from context?
MECHANISM_COMPLETENESS  : are all mechanism components named?

## 7. PASS / WARN / BLOCK
PASS  : gap CLOSED, maturity may increment
WARN  : gap PARTIAL, maturity holds, tension documented
BLOCK : transition prevented, reason explicit, inventor told what must change

## 8. NEXT QUESTION LOGIC
Priority: MECHANISM_COMPLETENESS > PHYSICAL_FEASIBILITY > BOUNDARY_AMBIGUITY
If gap open 3+ iterations: reframe question, do not repeat
One question per iteration. Contextual framing allowed. No embedded second question.

## 9. DOMAIN RULES — ELECTRONICS/ELECTRICAL (lightweight)
- Physical operating principle required before LEVEL 2
- Power acknowledgment required if mechanism involves energy conversion
- Mechanism must not be named after a specific product/platform

## 10. DETERMINISTIC vs AI-ADVISORY
DETERMINISTIC: gap criticality, PASS/WARN/BLOCK, transition eligibility, stall detection
AI-ADVISORY  : question framing, reframing suggestions, gap exploration angles

## 11. MVP ACCEPTANCE CRITERIA
- Domain inferred without user selection
- One question per iteration traceable to open gap
- BLOCK prevents transition regardless of other gaps
- Same idea twice = identical IdeaState
- Stall after 3 iterations triggers reframe
- LEVEL 2 idea contains: physical principle + power acknowledgment + boundary statement

## 12. ANTI-GOALS
- Generic questionnaire: same questions regardless of IdeaState
- Score optimization: inventor games inputs without improving idea
- Domain-blind evaluation: electronics = software questions
- AI overrides blocking conditions
- Iteration without progression detection
- Artificial closure via ACCEPTED_RISK on all gaps
- Invisible blocking without explanation
