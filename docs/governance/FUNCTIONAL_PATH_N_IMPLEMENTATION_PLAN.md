# FUNCTIONAL PATH N IMPLEMENTATION PLAN

## 1. Status

COMMITTED FUNCTIONAL PATH N IMPLEMENTATION PLAN — NO IMPLEMENTATION AUTHORIZED

Date: 2026-06-11

This is sequencing step 3 after:

1. MVP scope revision decision record ccd1ecd
2. MVP scope freeze amendment cdcd079
3. This implementation plan

No code, content, prompt, test, or runtime implementation is authorized by this plan.

## 2. Source Governance

- MVP_SCOPE_FREEZE_AMENDMENT_FUNCTIONAL_PATH_N.md — commit cdcd079
- MVP_SCOPE_REVISION_DECISION_RECORD.md — commit ccd1ecd
- DESIGNATION_ONLY_PATH_INTERFACE_IMPLEMENTATION_PLAN.md — commit 4f0ce81
- NON_SPECIALIST_PATH_SEPARATION_SCOPE_REVIEW.md — commit 110f4b1
- NON_SPECIALIST_MODE_SEPARATION_DESIGN_PLAN.md — commit d3b2349
- Characterization tests — commit 72b5f11
- NON_SPECIALIST_QUESTIONING_POLICY.md — commit a31010a
- R-2_R1_PRODUCT_ALIGNMENT_DRIFT_RECORD.md — commit 10d6876

## 3. Implementation Objective

Functional Path N is a non-specialist-safe questioning path for the existing Stage 1-3 journey.

It should allow a non-technical inventor to continue the guided invention journey without being blocked early by engineering-heavy questions.

It must preserve gaps as gaps rather than hiding them.

A user who cannot specify voltage, current, components, or datasheet requirements still has a PHYSICAL_FEASIBILITY gap. Path N changes how the gap is asked about and recorded, not whether the gap exists.

## 4. Minimal Implementation Boundary

Functional Path N may include only:

- non-specialist-safe question wording
- plain-language alternatives to early engineering-heavy questions
- known-unknown recording
- deferral language for engineering details
- Stage 1-3 only
- existing gap taxonomy
- deterministic gates unchanged

Functional Path N must not include:

- Professional Workspace
- Mode B implementation
- Engineering Translation stage
- Stage 4+
- automatic user classification
- engine gate changes
- technical-bank removal
- Path T modification unless separately authorized

Ambiguity resolves toward the freeze.

## 5. Candidate Implementation Approach

O-1: Content-first Path N question bank or variant set.

O-2: Route/config-based Path N selection with Path N content.

O-3: Minimal session path field plus Path N content.

O-4: Defer plumbing and first define Path N content as a governance artifact.

Recommendation:

Start with O-4.

Reason:

Content correctness is the root issue. Route or session plumbing without safe content does not make the non-specialist path safe.

The first next artifact should be a governed Path N question-content specification before touching code, domain files, routes, session state, or engine logic.

## 6. Required Path N Question Policy

Path N questions should ask about:

- idea
- problem
- user or beneficiary
- context
- current failure
- desired outcome
- rough mechanism in plain language
- what the user believes may make it work
- what the user does not know
- what information would be needed later

Path N questions must not use early as gates:

- voltage
- current
- frequency
- circuit architecture
- component-level selection
- signal transformation
- datasheet-level requirements
- engineering calculations
- manufacturing tolerances

Engineering-heavy gaps should be:

- translated
- recorded as known unknowns
- deferred
- routed later only by separate authorization

Example:

R1 gate question:

"Are there any known electrical constraints that your design must stay within to function correctly?"

Path N equivalent:

"What would need to be true for this system to work safely, and what information would you need later to confirm it?"

Same gap. Different asking strategy. Journey continues.

## 7. Files Likely Affected Later — Planning Only

All are NOT AUTHORIZED now:

- possible Path N question content specification file
- possible future update to domains/electronics_electrical/domain.json only if separately authorized
- possible route/config/session path field only if separately authorized
- possible future tests update only if separately authorized
- no engine change unless separately authorized

Any touch to engine/progression_loop.py requires separate ARCHITECTURE_GUARDRAILS review.

## 8. Test Strategy Later

The existing xfail in 72b5f11 remains xfail until Path N content exists.

Later tests may verify:

- Path N content avoids engineering-gated terms early
- Path T technical content remains allowed
- user-volunteered technical vocabulary is not penalized
- R1 regression does not recur in Path N

If O-4 is chosen, the first test update target should be the Path N content specification artifact.

No tests are created or modified by this plan.

## 9. R2 / AA-4 Implications

- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked
- R2 may restart only after Functional Path N exists and produces non-specialist-safe evidence
- this plan alone does not unblock R2

The chain to R2 is:

content specification -> content approval -> implementation plan authorization -> implementation -> verification -> R2 authorization

Each step requires separate owner authorization.

## 10. Governance Effect

- code changes are not authorized
- prompt changes are not authorized
- question-bank changes are not authorized
- tests are not modified
- implementation is not authorized
- R2 remains HELD
- FORM T remains blocked
- S-6 remains unclassified
- AA-5 remains blocked

## 11. Required Next Owner Decision

The owner must decide:

1. Whether to authorize a Path N question-content specification.
2. Whether implementation should be content-first before route/session changes.
3. Whether test updates should wait until content is approved.
4. Whether any code implementation is allowed after content approval.

## 12. Boundary Statement

No code was modified by this plan.

No prompts were modified by this plan.

No domain question bank was modified by this plan.

No routes were modified by this plan.

No engine logic was modified by this plan.

No tests were modified by this plan.

No FORM T comparison has been performed.

No S-6 classification has been performed.

No AA-5 verdict has been started.

R2 remains HELD.

AA-4 final S-6 classification has NOT been performed.
