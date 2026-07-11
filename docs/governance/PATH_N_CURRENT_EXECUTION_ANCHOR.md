# PATH N CURRENT EXECUTION ANCHOR

## 1. Purpose

This document is the current execution anchor for Path N after Phase 1 implementation.

It does not replace:

`docs/governance/ILT-002_GOVERNANCE_ANCHOR.md`

The ILT-002 Governance Anchor remains the mandatory boot and epistemic control document.

This document records the current Path N execution state so that future agents do not reconstruct state from memory, chat history, or assumptions.

---

## 2. Authority chain

| Commit    | Role                                                         |
| --------- | ------------------------------------------------------------ |
| `5084110` | Phase 1 Path N designation implementation                    |
| `16e020e` | Phase 1 Path N designation authorization                     |
| `bd1019c` | Amendment 1 to Path N runtime integration authorization plan |
| `2f6720d` | Phase 0 conditional STOP owner ruling                        |
| `2c0d2a5` | Phase 0 Path N runtime discovery report                      |
| `d2b2a9a` | Corrected Path N runtime integration authorization plan      |
| `26fa3e1` | Path N content config artifact approval                      |
| `806a3c6` | Path N content config artifact tests                         |
| `8ceb5d4` | Path N content config artifact                               |

Latest verified HEAD at time of this anchor:

`5084110 feat: implement Phase 1 Path N designation`

---

## 3. Current Path N execution state

Phase 1 has been implemented.

Phase 1 is designation-only.

Implemented in Phase 1:

* `engine/idea_state.py`

  * Added `path: str = "legacy_undesignated_current_behavior"`
* `web/app.py`

  * Added route:
    `/start_ilt002_combination_lock_path_n`
* `tests/test_phase1_path_designation.py`

  * Added Phase 1 designation tests

The new Path N route creates a designated session by setting:

`state.path = "N"`

---

## 4. What Phase 1 does NOT mean

Phase 1 does NOT mean Path N is runtime-integrated.

Phase 1 does NOT mean Path N content is live.

Phase 1 does NOT mean the platform now asks Path N questions.

Phase 1 does NOT authorize Phase 2.

Phase 1 does NOT authorize any classification update.

Phase 1 does NOT authorize R2.

Phase 1 does NOT unblock FORM T.

Phase 1 does NOT classify S-6.

Phase 1 does NOT unblock AA-5.

---

## 5. Runtime content status

Path N-designated sessions still receive legacy question content.

The designation is carried but not consumed.

No Path N content loader has been implemented.

No shared question-selection function has been implemented.

No runtime Path N content selection has been implemented.

---

## 6. Files explicitly not changed by Phase 1

The following remain untouched by Phase 1:

* `engine/progression_loop.py`
* `engine/domain_rules.py`
* `engine/domain_registry.py`
* `domains/electronics_electrical/domain.json`
* Path N JSON content artifact metadata
* deterministic gate logic
* PASS / WARN / BLOCK logic

---

## 7. Runtime integration flag

`runtime_integrated` remains:

`false`

Any future change to `runtime_integrated=true` requires separate authorization, runtime evidence, tests, and recorded approval.

---

## 8. Current blocked / held statuses

As of commit `5084110`:

| Item                       | Status         |
| -------------------------- | -------------- |
| R2                         | HELD           |
| FORM T                     | BLOCKED        |
| S-6                        | UNCLASSIFIED   |
| AA-5                       | BLOCKED        |
| Phase 2                    | NOT AUTHORIZED |
| Path N runtime integration | NOT COMPLETE   |

---

## 9. Required future sequence

The next possible step is not implementation by default.

Before Phase 2 implementation, the repository requires:

1. Phase 1 closure / evidence record.
2. Explicit Phase 2 authorization.
3. Exact Phase 2 scope definition.
4. Tests proving no mixed-path question behavior.
5. Tests proving Path N content selection cannot be overridden by AI advisor logic.
6. Evidence that legacy Path T behavior remains unchanged.

---

## 10. Forbidden interpretations

Future agents must NOT infer that:

* Path N is live because a Path N route exists.
* `state.path = "N"` means Path N content is selected.
* Phase 1 completion authorizes Phase 2.
* Phase 1 completion changes R2, FORM T, S-6, or AA-5.
* Legacy sessions are now Path N sessions.
* `runtime_integrated=false` can be changed without separate authorization.

---

## 11. Boot rule for future agents

Any future agent working on Path N must first read:

1. `docs/governance/ILT-002_GOVERNANCE_ANCHOR.md`
2. `docs/governance/PATH_N_CURRENT_EXECUTION_ANCHOR.md`
3. `docs/governance/PHASE_1_PATH_DESIGNATION_AUTHORIZATION.md`
4. `docs/governance/PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION_PLAN_AMENDMENT_1.md`

If these documents are not read, the agent must not reconstruct Path N state from memory or chat history.

---

## 12. Current conclusion

Path N has reached Phase 1 designation implementation only.

Path N is not runtime-integrated.

Path N content is not live.

The next governance-safe step is a Phase 1 closure / evidence record, not Phase 2 implementation.

---

## 13. Deliverable Stabilization Gate

This section is a stable gate declaration. The detailed and changeable
remediation content lives in the dedicated remediation-plan document, not
in this Anchor.

The authoritative remediation document is:

`docs/governance/DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md`

Gate rules:

1. No new analytical feature, AI Coach capability, domain expansion,
   journey redesign, monetization feature, or unrelated product feature
   may proceed until the active remediation plan reaches its defined
   closure gates.
2. Remediation items are NOT complete merely because code changed or
   focused tests passed.
3. Closure of any remediation item requires ALL of:
   - focused tests;
   - accepted full-regression results;
   - regenerated deliverable evidence;
   - absence of the target defect in that regenerated evidence;
   - independent read-only review;
   - explicit owner authorization.
4. This Anchor records only the gate itself. Workstream content, ordering,
   priorities, statuses, and closure detail MUST be read from the
   remediation-plan document above and must not be copied into, inferred
   from, or maintained in this Anchor.

This section does not alter any other section of this Anchor, does not
change Path N phase state, and authorizes no implementation by itself.
