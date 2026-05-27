# ADR-001: Domain Assignment and Multi-Domain Strategy

**Status:** Accepted
**Date:** 2026-05-27
**Author:** InventorAI Architecture Review
**Applies to:** engine/domain_registry.py, engine/domain_rules.py, engine/idea_state.py, engine/progression_loop.py

---

## 1. Context

Phase 5 Step 3 delivered engine/domain_registry.py: a validated, tested loader that reads capability packs from domains/*/domain.json and returns an immutable registry keyed by capability_id. The registry is complete and correct. It is not yet wired to any runtime component.

The current production path reads gap names and domain signals from hardcoded Python in engine/domain_rules.py. The registry and the hardcoded values represent the same domain — iot_electronics — in two different representations. No mechanism currently enforces parity between them.

idea_state carries no domain assignment field. The engine has no concept of domain selection, domain-scoped gap sets, or multi-domain evaluation. All progression logic assumes a single fixed set of gaps defined at the Python level.

A value assessment concluded that Step 4 wiring delivers no user-visible capability until a second domain pack exists, introduces moderate regression risk to the deterministic progression engine, and should not proceed on roadmap momentum alone. A multi-domain strategy assessment identified eight architectural preconditions that must be satisfied before a second domain pack can be introduced safely.

This ADR formalises the decisions reached as a result of those assessments.

---

## 2. Decision

**Step 4 wiring is frozen.** engine/domain_registry.py will not be imported by or wired into any engine runtime component until the conditions in Section 6 are met and explicit owner approval is granted.

**Single-domain explicit assignment is the only approved near-term model.** When domain assignment is eventually implemented, a project will be assigned exactly one domain at session creation time via an explicit assigned_domain field. That assignment will be validated against the loaded registry and will remain fixed for the lifetime of the session.

**Multi-domain support is deferred indefinitely.** No architecture, code, or schema may be designed or implemented for multi-domain session evaluation until this ADR is superseded by a replacement decision record.

**Signal-based automatic domain classification is not approved.** The engine will not inspect invention descriptions to infer a domain. Domain assignment is explicit or it does not occur.

**No changes to progression logic without separate approval.** assess_response(), integrate_response(), and evaluate_transition() remain protected. Any change to maturity thresholds, gap lifecycle logic, PASS/WARN/BLOCK semantics, or transition conditions requires a separate, explicitly approved change record and full benchmark verification.

---

## 3. Rationale

**Why Step 4 is frozen:**
With one domain pack, Step 4 produces no observable difference for any user. The registry and the hardcoded values in domain_rules.py describe the same domain. Wiring them together eliminates a maintenance duplication that is currently low-severity. The risk introduced — silent progression behavior change if registry values diverge from hardcoded values, import-time engine failure if the domains directory is missing or malformed — is not justified by the value delivered at single-domain scale.

**Why explicit assignment over signal detection:**
Signal-based classification is probabilistic. A misclassification silently affects all subsequent gap evaluation, question generation, and progression decisions for the entire session with no error surfaced to the inventor or operator. The deterministic evaluation guarantee — which is the core architectural principle of InventorAI — is incompatible with a probabilistic domain assignment step upstream of it. Explicit assignment preserves determinism end-to-end.

**Why multi-domain is deferred:**
Multi-domain support requires gap identifier uniqueness enforcement across packs, a domain composition strategy for gap set construction, generalization of the progression transition trigger away from named gap identifiers, and session-scoped gap state isolation. None of these exist today. Attempting multi-domain support before single-domain wiring is proven introduces compounded risk with no intermediate validation checkpoint.

**Why the registry work already delivered is still valuable:**
The registry provides a validated, tested loading mechanism with a stable public API. When Step 4 does resume, it has a known correct contract to wire against. The governance metadata enforcement (KSP-001) is in place for all future domain packs. The infrastructure cost has been paid. Freezing Step 4 does not undo that value.

---

## 4. Accepted Technical Debt

**Dual-representation maintenance risk.**
domains/iot_electronics/domain.json and engine/domain_rules.py contain the same domain information in two representations. A change to gap names or domain signals in the JSON file has no effect on runtime behavior until Step 4 is wired. Any contributor modifying domain content must update both representations until this debt is resolved.

**No enforced parity between registry and hardcoded values.**
There is no automated test that asserts the gap names and domain signals in domain.json exactly match those in domain_rules.py. A divergence would be silent. This test must be written as the first action when Step 4 resumes, before any hardcoded value is removed.

**test_extract_json_contract.py and test_normalize_output_contract.py break pytest collection.**
Both files are untracked, contain module-level sys.exit(1) guards, and cause INTERNALERROR when pytest attempts to collect them. They are excluded from all test runs via --ignore. Resolution is deferred as a separate technical debt item. Options: convert to proper pytest tests, relocate to scripts/, or confirm obsolete and delete. Must be resolved as a standalone task, not bundled with any engine change.

**tests/replay/replay_report_v1.json contains working-tree changes not committed.**
The skipped count changed from 3 to 6 in the working tree, matching the accepted handover baseline of 6. This file was not committed as part of any Step 3 change. Its status must be reviewed and either committed as a baseline update or restored before Step 4 begins.

---

## 5. Forbidden Changes

The following changes are forbidden without explicit supersession of this ADR or separate written approval:

- Importing domain_registry in engine/domain_rules.py, engine/progression_loop.py, or web/app.py
- Adding domain selection, domain detection, or domain classification logic to any engine component
- Adding a domain field or domain-related fields to idea_state before Step 4 preconditions are met
- Modifying assess_response(), integrate_response(), or evaluate_transition() for any domain-related purpose
- Changing maturity thresholds, gap lifecycle rules, or PASS/WARN/BLOCK semantics
- Creating a second domain pack and expecting it to affect runtime behavior before Step 4 wiring is complete
- Encoding progression rules, thresholds, or maturity definitions inside any domain.json file
- Allowing domain_registry.py to import from any engine module

---

## 6. Conditions Required Before Step 4 Can Resume

1. Owner explicitly approves resumption.
2. A second domain pack is actively planned.
3. test_extract_json_contract.py and test_normalize_output_contract.py SystemExit issues resolved and committed.
4. replay_report_v1.json working-tree state confirmed or restored.
5. Parity test written and passing before any hardcoded value is removed.
6. Defensive loading strategy approved and documented.
7. Full benchmark baseline confirmed and locked before Step 4 changes any runtime path.

---

## 7. Conditions Required Before Adding a Second Domain Pack

1. Step 4 wiring complete and committed.
2. idea_state carries assigned_domain. No domain-unassigned execution path exists.
3. Gap set is session-scoped from idea_state.assigned_domain at session start.
4. evaluate_transition() checks dynamic gap closure, not hardcoded gap names. Requires separate approval.
5. Gap identifier uniqueness enforced by registry validator across all loaded packs.
6. New domain pack passes full registry validation without error.
7. Independent replay benchmarks pass for both domains.
8. No shared mutable state between domain sessions verified.

---

## 8. Risks If Ignored

**If Step 4 is implemented without parity verification:**
Registry values and hardcoded values may diverge silently. Inventors receive incorrect progression decisions. The defect may not be detected until a gap closure that should have triggered a transition fails to do so.

**If signal-based domain classification is introduced:**
A probabilistic step is inserted upstream of a deterministic engine. Misclassification produces a completely different gap set and progression path. The deterministic evaluation guarantee is broken.

**If multi-domain support is attempted before single-domain wiring is proven:**
Gap lifecycle logic and progression transition behaviour may regress in a large diff touching multiple systems simultaneously, with no intermediate validation checkpoint.

**If test_extract_json_contract.py is left unresolved:**
The INTERNALERROR during pytest collection continues to mask potential test suite failures. The test suite cannot be trusted as a complete regression signal.

**If the registry is used as decision authority rather than data source:**
If a domain pack encodes threshold values or progression conditions and the engine acts on them, the deterministic engine has been replaced by a data-driven rule system without formal review. AI governance boundaries are weakened.

---

*This ADR supersedes no prior decision record. It may be superseded by a replacement ADR approved by the project owner. No implementation action may be taken in contradiction of Section 5 without that supersession.*
