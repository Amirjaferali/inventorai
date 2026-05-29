# ADR-004: MECHANISM_COMPLETENESS Must Be CLOSED Before LEVEL 1 → LEVEL 2 Transition

**Status:** Accepted
**Date:** 2026-05-29
**Author:** InventorAI Architecture Review
**Depends on:** ADR-001, ADR-002, ADR-003
**Applies to:** engine/progression_loop.py (evaluate_transition)

---

## 1. Context

Validation campaign Session C and Session E (disclosure validation, 2026-05-29) demonstrated that a session could reach LEVEL 2 and display "Ready for structured review" after a response scored ASSERTED on the MECHANISM_COMPLETENESS gap. This is finding D-005 in the validation ledger.

Root cause investigation of evaluate_transition() (lines 281–315 of engine/progression_loop.py) confirmed the exact defect:

The LEVEL 1 → LEVEL 2 guard checked:

```python
if mech_gap and mech_gap.status == OPEN:
    return False, "BLOCK: MECHANISM_COMPLETENESS still open"
```

The gap status lifecycle is: OPEN → PARTIAL → CLOSED.

integrate_response() correctly sets gap.status = PARTIAL when a response scores ASSERTED. This means after one ASSERTED response, the gap is no longer OPEN. The guard above did not block on PARTIAL. evaluate_transition() returned True, state.maturity_level incremented to 2, and the completion UI rendered.

This violated Governance Principle 1 (Inventor Ownership): progression credit was awarded based on participation, not demonstrated quality. It also violated the LEVEL 1 → LEVEL 2 contract established by ADR-003, which states that the quality level of known_mechanism must be REASONED minimum for maturity transition.

The existing known_mechanism.quality guard correctly blocked ASSERTED quality on the known_mechanism field. However, known_mechanism is set once (at LEVEL 0) and not updated by subsequent ASSERTED responses at LEVEL 1. The gap status guard was the only mechanism capable of blocking low-quality iteration at LEVEL 1. That guard was insufficient.

---

## 2. Decision

The LEVEL 1 → LEVEL 2 transition guard in evaluate_transition() is changed from:

```python
if mech_gap and mech_gap.status == OPEN:
    return False, "BLOCK: MECHANISM_COMPLETENESS still open"
```

to:

```python
if mech_gap and mech_gap.status != CLOSED:
    return False, "BLOCK: MECHANISM_COMPLETENESS not yet closed"
```

PARTIAL is now explicitly blocking. Only CLOSED satisfies the gate.

This means: LEVEL 1 → LEVEL 2 requires the inventor to accumulate REASONED-quality evidence sufficient to close the MECHANISM_COMPLETENESS gap. A single REASONED response on first attempt closes the gap (integrate_response sets CLOSED when quality == REASONED and gap was OPEN). A REASONED follow-up after a PARTIAL response also closes the gap (integrate_response sets CLOSED when quality == REASONED and gap was PARTIAL). An ASSERTED response leaves the gap PARTIAL and the transition blocked.

---

## 3. Consequences

**Positive:**
- LEVEL 1 → LEVEL 2 transition now requires demonstrated mechanism understanding, not participation.
- Governance Principle 1 (Inventor Ownership) is restored: completion credit is awarded only when the inventor's own words satisfy the quality threshold.
- D-005 is resolved.
- The deterministic governance contract is strengthened: the classifier verdict now has binding effect on maturity advancement.

**Negative / Accepted trade-offs:**
- An inventor who provides a REASONED response on their first attempt at LEVEL 1 advances immediately as before. No change for the happy path.
- An inventor who provides ASSERTED responses repeatedly will remain at LEVEL 1 indefinitely until stall detection fires (D-006, separate finding). Until D-006 is resolved, such a session will loop without advancing or completing. This is the correct behavior — the platform must not award false completion — but it means the inventor receives no explicit guidance that they are stuck until D-006 is fixed.
- This change does not fix D-006. Stall detection remains non-functional. D-006 must be addressed separately.

**Unchanged:**
- assess_response() — not modified
- integrate_response() — not modified; its PARTIAL/CLOSED logic is correct and relied upon by this fix
- IdeaState schema — not modified
- GAP_PRIORITY — not modified
- _eligible() — not modified
- assemble_deliverable() — not modified
- Gap types — not modified
- GD-001 three-stage journey — not affected

---

## 4. Governance Compliance

This change is compliant with:
- Governance Principle 1 (Inventor Ownership): progression credit now requires demonstrated quality
- Governance Principle 2 (Improvement Not Generation): no generative capability added
- GD-001: Stage Two gap architecture unchanged; only the transition gate is tightened
- ADR-003: known_mechanism REASONED minimum requirement is now fully enforced end-to-end

This ADR does not require changes to any other ADR. It tightens the implementation of the contract established by ADR-003 without changing that contract.

---

## 5. Evidence

- Finding D-005, validation ledger, INVENTORAI_PROJECT_STATE_FREEZE_v1.2.md Section 4
- Session C screenshot evidence, 2026-05-29 4:02 PM: Stage 3 reached after "It monitors somehow." response
- Session E screenshot evidence, 2026-05-29 4:24 PM: Stage 3 reached on iteration 3 with ASSERTED-quality response
- Root cause trace: engine/progression_loop.py lines 281–315, evaluate_transition(), confirmed 2026-05-29
