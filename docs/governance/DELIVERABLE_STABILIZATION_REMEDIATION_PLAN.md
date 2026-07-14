# DELIVERABLE STABILIZATION REMEDIATION PLAN

**Document ID:** DELIVERABLE_STABILIZATION_REMEDIATION_PLAN
**Type:** Authoritative remediation plan (mandatory, owner-ordered)
**Status:** ACTIVE — governance documentation increment; no implementation authorized by this document
**Date:** 2026-07-11
**Authority level:** Owner-ordered remediation authority, subordinate to committed anchors and `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`
**Companion documents:**
`docs/governance/PATH_N_CURRENT_EXECUTION_ANCHOR.md` §13 (Deliverable Stabilization Gate)
`docs/governance/DELIVERABLE_STABILIZATION_OWNER_DECISION.md` (owner decision record)

---

## 1. Purpose and authority

This document is the single authoritative remediation plan for stabilizing
the InventorAI deliverable and the question/answer journey that feeds it. It
exists so the remediation program survives agent changes and cannot be
bypassed, reordered, or silently re-scoped by future implementation work.

Authority chain:

1. The owner ordered the remediation freeze and this plan (see the owner
   decision record above).
2. The Anchor's Deliverable Stabilization Gate
   (`PATH_N_CURRENT_EXECUTION_ANCHOR.md` §13) makes this plan blocking for
   unrelated feature work.
3. This plan defines WHAT must be remediated, in WHAT order, and WHAT
   closure requires. It authorizes NO implementation by itself: every
   workstream requires its own separately owner-gated lifecycle (§10, §11).

This plan is mandatory, not advisory. Analysis, recommendations, or team
consensus do not create authority to deviate from it.

Relationship to existing plans: `INVENTORAI_PRODUCT_VALUE_CORRECTION_PLAN.md`
remains a non-authorizing governance companion recording earlier
product-value findings; it is not replaced. Where subjects overlap, THIS
document controls remediation sequencing and closure.

---

## 2. Current freeze declaration

Effective upon commit of this document:

- All new analytical features, AI Coach capabilities, domain expansions,
  journey redesigns, monetization features, and unrelated product features
  are FROZEN until the closure gates in this plan are reached (Anchor §13).
- The freeze applies to UNRELATED work only: it does NOT block the
  remediation workstreams of this plan themselves. Work inside the
  currently owner-authorized remediation workstream remains permitted;
  however, no workstream (and no lifecycle step within it) may begin
  without its separate owner gate (§10, §11).
- The freeze does not reopen, alter, or unfreeze any previously frozen or
  paused lane (persistence remains frozen and paused; Safety Signals remain
  closed as a feature lane; Answer Clarification remains inactive; the
  replay/benchmark freeze in `CLAUDE.md` is unchanged).
- Already-open Draft PRs (#162, #167) keep their existing separately
  owner-gated lifecycles; this plan neither advances nor blocks them.

---

## 3. Confirmed defect classes

The following issues are CONFIRMED (owner-accepted evidence basis: the
comprehensive read-only product journey and deliverable diagnosis performed
against merged tip `c62bd9ab8f3cd1fa137b15415283672611109261`, preserved as
`docs/governance/DELIVERABLE_STABILIZATION_EVIDENCE_BASIS.md`).

### 3.A Safety correctness (highest severity)

1. Safety-signal false negative despite inventor-stated dangerous
   consequences.
2. Safety extraction regression between previously successful and current
   wording.

### 3.B Deliverable content quality

3. Raw system-state leakage into the final deliverable.
4. Inconsistent counts across deliverable sections.
5. Low-value orphan statements.
6. Vague responsibility placeholders.
7. Criticality remaining `UNDETERMINED` despite explicit essential/adjustable
   discussion.
8. Generic and duplicated validation actions.
9. Duplicated prototype experiments.
10. Contradiction between safety, risk, evidence, and unknown sections.

### 3.C Journey and question design

11. Unnatural question order.
12. Title/question-intent mismatch.
13. Multi-intent questions.

### 3.D Evaluation fit

14. Causal scoring applied to non-causal question types.
15. Semantically strong answers rejected due to linguistic-pattern
    dependence.
16. Fixed two-answer closure behavior.

### 3.E Guidance and support

17. Guidance contradicting question intent.
18. Unknown responses causing a dead end.
19. Excessive and fragmented guidance panels.
20. Insufficient project-specific support for non-technical users.
21. Dependence on external ChatGPT assistance.
22. Risk of AI-assisted wording overstating actual inventor knowledge.

No additional defect may be silently appended to this list; additions
require an owner-authorized amendment to this document.

---

## 4. Priority levels

| Priority | Meaning |
|---|---|
| **P0** | Safety correctness and deliverable-integrity defects. Nothing else proceeds while a P0 workstream is open. |
| **P1** | Deliverable content-quality synthesis defects. Proceed only after P0 closure. |
| **P2** | Journey, question-design, evaluation-fit, and guidance defects. Proceed only after the preceding P1 gates close. |

Priorities may not be re-assigned without written owner authorization.

---

## 5. Mandatory execution order

The workstreams below MUST execute in this order. The sequence may not be
reordered, bypassed, merged, or materially re-scoped without written owner
authorization (owner decision record §3).

1. Evidence Lock and baseline preservation.
2. P0 Safety Signal Stabilization.
3. P0 Deliverable Hygiene.
4. P1 Structured Criticality Capture.
5. P1 Unified Risk and Safety Presentation.
6. P1 Requirement Landscape Synthesis.
7. P1 Actionable Validation Plan.
8. P2 Journey Reordering and Intent Alignment.
9. P2 Single-Intent Question Design.
10. P2 Question Intent Registry.
11. P2 Question-Aware Evaluation.
12. P2 Controlled Unknown Progression.
13. P2 Guided Answer Support.
14. P2 Adaptive Follow-Up and Completion Logic.
15. P2 Guidance Consolidation.
16. Final Deliverable Completion and full end-to-end owner validation.
17. AI Coach — only after ALL preceding gates are owner-closed.

---

## 6. Scope and exclusions

In scope: the defect classes of §3, remediated through the lifecycle of
§10/§11, in the order of §5.

Explicitly excluded from this plan (each remains governed by its own
existing authority and freeze state):

- persistence (frozen: PRESERVE UNMODIFIED AND PAUSE at
  `aec9cf6409efc18e125b6745762002f59e529654`);
- replay/benchmark behavior (`CLAUDE.md`; historical truth
  `benchmark/run_benchmark_v1.py`);
- domain expansion beyond electronics/electrical;
- Answer Clarification / Improve Wording activation;
- `main` synchronization;
- PR #162 and PR #167 lifecycles;
- roadmap restructuring beyond §11-conformant entries;
- monetization, marketing, or commercial-differentiation implementation.

### 6.A Disposition of earlier owner-gated contracts

The existing owner-gated contracts concerning Guided Uncertainty Support,
Guided Answer Co-Authoring, and Advisory Panel Precedence remain
historically valid, but they are NOT independently executable while this
remediation plan is active. They may be reused, amended, superseded, or
incorporated into Workstreams 12 (Controlled Unknown Progression),
13 (Guided Answer Support), or 15 (Guidance Consolidation) only through new
written owner authorization and the applicable Increment Contract (§9). The
execution timing of any such work is governed by this plan's mandatory
sequence (§5). This provision does not alter or close those earlier
contracts.

---

## 7. Evidence-lock requirements (Workstream 1)

Before any remediation implementation:

1. Preserve the exact pre-remediation baseline: authoritative tip SHA, full
   regression counts, and the failing-test inventory.
2. Regenerate and commit (as documentation evidence) at least one complete
   deliverable produced by the CURRENT build from a scripted, reproducible
   journey, so every §3 defect that is observable in the deliverable has a
   frozen "before" artifact.
3. Record the reproduction script/inputs verbatim so the same journey can be
   regenerated after each workstream.
4. Raw transcript preservation and user-facing synthesis are SEPARATE
   concerns: evidence artifacts preserve raw state verbatim; no evidence
   artifact may be beautified, summarized, or corrected.
5. Evidence artifacts, once committed, are immutable (fixture rules in
   `CLAUDE.md` apply).

---

## 8. Source-review requirements

Every workstream MUST begin with an owner-gated READ-ONLY source review
that:

- traces the defect to its origin (structural, semantic, fixture, runtime
  dependency, or actual logic defect — per the `CLAUDE.md` classification
  rule) BEFORE any patching;
- identifies the exact files, contracts, and tests involved;
- states whether the fix is presentation-only, synthesis-only, or
  engine-affecting;
- identifies every replay/benchmark/scoring surface the change could touch
  and how it will be proven untouched (or, if scoring must change, what
  parity proof will be provided);
- ends with an explicit feasibility verdict and stops (no mutation in the
  same step).

---

## 9. Increment Contract requirement

After the source review and before implementation, every workstream MUST
have a committed Increment Contract document (docs-only PR) that pins:

- exact scope and prohibited behaviors;
- input/output contracts of any new file (per `CLAUDE.md` file-creation
  rules);
- acceptance gates (testable);
- stop conditions (non-waivable);
- the evidence that closure will require (§12).

No implementation may begin from an unwritten or unmerged contract unless
the owner explicitly authorizes a combined step in writing.

---

## 10. Owner-gated authorization rules

- Every lifecycle step (source review, increment contract, implementation,
  independent review, merge, post-merge verification, evidence regeneration,
  closure) requires its own explicit owner authorization.
- Authorization is step-scoped and non-transferable: authorization of one
  workstream or step never implies authorization of the next.
- Analysis, recommendations, replay greenness, or team consensus are not
  authorization.
- Any ambiguity is a STOP condition: diagnose and report; do not proceed
  speculatively.

---

## 11. Implementation and review lifecycle

Each workstream follows this fixed lifecycle, each step separately
owner-gated:

1. Read-only source review (§8).
2. Increment Contract (§9).
3. Implementation on a fresh branch from the exact authoritative tip —
   tests-first where the contract requires it; safety stabilization
   (Workstream 2) is ALWAYS test-first.
4. Focused tests + full regression battery + comparison against the
   preserved failure baseline.
5. Independent read-only review.
6. Owner-gated merge.
7. Post-merge verification.
8. Regenerated deliverable evidence from the recorded reproduction journey
   (§7.3), demonstrating absence of the target defect.
9. Owner closure authorization; status table update (§15) via a
   docs-only sync.

---

## 12. Closure criteria

A remediation workstream is closed ONLY when all of the following exist:

1. focused tests proving the specific fix;
2. accepted full-regression results (compared against the preserved
   baseline; no unexplained new failure);
3. regenerated deliverable evidence from the recorded journey;
4. demonstrated absence of the target defect in that regenerated evidence;
5. independent read-only review;
6. explicit owner closure authorization.

Passing one example does NOT establish stability. Code change alone, or
focused-test greenness alone, is NOT closure.

Additional binding closure constraints:

- Safety stabilization is TEST-FIRST; simple keyword expansion alone is
  insufficient; positive, negative, AND metamorphic fixtures are required
  before the safety-extraction change is accepted.
- No final criticality may be derived solely from lexical cues; structured
  owner confirmation is required for criticality (Workstream 4).
- Raw transcript preservation and user-facing synthesis remain separate
  concerns; no synthesis change may rewrite, truncate, or reinterpret
  preserved raw state.
- No remediation workstream may be marked complete without regenerated
  deliverable evidence and independent review.

---

## 13. Prohibited shortcuts

The following are forbidden in all workstreams:

- marking an item complete because code changed or a focused test passed;
- keyword-list expansion presented as safety stabilization;
- deriving final criticality from lexical cues alone;
- patching replay, fixtures, or scoring for greenness (see `CLAUDE.md`);
- hidden fallback logic, silent schema coercion, implicit semantic upgrades;
- collapsing lifecycle steps without written owner authorization;
- reordering, merging, or re-scoping §5 without written owner authorization;
- treating regenerated evidence from a DIFFERENT journey as proof for the
  recorded journey;
- starting any §5 item while an earlier item's closure gate is open;
- starting AI Coach work before every preceding gate is owner-closed.

---

## 14. Agent-handover requirements

Any future agent (including any Agent Teams teammate) MUST, before acting
on anything touched by this plan, read in order:

1. `docs/governance/ILT-002_GOVERNANCE_ANCHOR.md` and the `CLAUDE.md`
   mandatory reading chain;
2. `docs/governance/PATH_N_CURRENT_EXECUTION_ANCHOR.md` (including §13);
3. `docs/governance/DELIVERABLE_STABILIZATION_OWNER_DECISION.md`;
4. this document, in full, including the §15 status table;
5. `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` (latest committed);
6. the latest post-merge evidence record;
7. the latest regenerated deliverable evidence.

Agents must not reconstruct remediation state from memory, chat history, or
assumption. If the §15 status table disagrees with Git history, STOP and
request synchronization. Unrelated implementation is unauthorized while the
freeze (§2) is active.

---

## 15. Workstream status table

Statuses may only change through the lifecycle of §11 with owner
authorization, recorded by a docs-only update to this table. Allowed status
values: `NOT STARTED`, `SOURCE REVIEW`, `CONTRACT`, `IMPLEMENTATION`,
`INDEPENDENT REVIEW`, `MERGED — CLOSURE PENDING`, `CLOSED`, `BLOCKED`.

| # | Workstream | Priority | Status | Closure evidence |
|---|---|---|---|---|
| 1 | Evidence Lock and baseline preservation | Gate | CLOSED | PR #169; true two-parent merge `3209836b5648f55c70ebb4149db7dfdd5e4adbeb`; canonical evidence tree `a49a51338aaefd82d0f060308464c90dbe68b14c`; independent final closure verification PASS; explicit owner closure authorization granted 2026-07-12 |
| 2 | Safety Signal Stabilization | P0 | CLOSED | Implementation PR #172; implementation merge `523d4306dc4ce0d02b865550eedab80793637dab`; roadmap-sync PR #173; authoritative closure merge `1d532bf046e098956d8c936110b0ef33d4298eed`; evidence directory `docs/governance/evidence/workstream2_safety_stabilization/` |
| 3 | Deliverable Hygiene | P0 | CLOSED | Canonical closure (CLOSED / CANONICAL). Closure basis: canonical contract `docs/governance/DELIVERABLE_HYGIENE_INCREMENT_CONTRACT.md` (recording PR #175, merge `0189577f269366dc3201cb4cfeb32875a904d4e9`; status canonicalized via PR #176); canonical RED gate PR #177 (merge `d82ff156d7c3aaf1856908f79d944a2c207a36e8`); canonical GREEN implementation including the F1 Section 12 correction PR #178 (merge `0b04021d99290f8f747ee24d46b93c1dda69d66f`); canonical evidence package PR #179 (merge `aa608e57d27d02460d9a10c39a739736b29e9b6a`; `docs/governance/evidence/workstream3_deliverable_hygiene/`); independent implementation review PASS; independent evidence review PASS. The known 31 `tests/test_domain_registry.py` failures remain the pre-existing baseline and were not introduced (or corrected) by Workstream 3; Workstream 4 is not authorized; AI Coach remains prohibited; PR #167 and PR #162 remain outside this closure and untouched; official product state remains `DEMO_READY_WITH_LIMITATIONS`; MVP scope remains electronics/electrical-only |
| 4 | Structured Criticality Capture | P1 | CLOSED | Canonical closure (CLOSED / CANONICAL). Closure basis: canonical contract `docs/governance/STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md` (recording PR #181, merge `cb1f4fd8fb4854864ef89c3f3df2275d818785c9`; status canonicalized via PR #182, merge `9825ae0b012e59ed96e843a86390dee5088bb0a9`); implementation and evidence merged and canonical through PR #183 (true two-parent merge `961b92591782d3e78e39ae48a3c0e4df5453d8da`; RED baseline `dd591353`, hygiene hardening `05069e4d`, implementation `df4836bf`, GREEN journey coverage `61f0b14c`, evidence `1c30c1c2`; evidence directory `docs/governance/evidence/workstream4_structured_criticality/`, 17 files, manifest 16/16 OK); independent HEAD GREEN review PASS; independent evidence review PASS; no blocking findings (four non-blocking findings recorded as future hardening observations, not fixed). Canonical test state: structured-criticality 18 passed (zero skipped/xfailed); hygiene 22; Safety Signal 18; stabilization 15; requirement landscape 39; fixed focused suite 316; full suite 31 failed / 1379 passed / 1 skipped / 1 xfailed / 24 xpassed with all 31 failures confined to the pre-existing `tests/test_domain_registry.py` baseline. No further source or test authorization remains open; Workstream 5 is not authorized; AI Coach remains prohibited; PR #167 and PR #162 remain outside this closure and untouched; official product state remains `DEMO_READY_WITH_LIMITATIONS`; MVP scope remains electronics/electrical-only |
| 5 | Unified Risk and Safety Presentation | P1 | CONTRACT | CONTRACT / CANONICAL — Workstream 5 read-only Source Review complete (accepted at base `031f455825b2d03c7980e55e990953c063e436f6`); Increment Contract owner-approved (owner decisions D1–D6 incorporated) and canonically recorded at `docs/governance/UNIFIED_RISK_SAFETY_PRESENTATION_INCREMENT_CONTRACT.md` (recording PR #185; true two-parent merge `8b6868fce5e5fe81f221f3a6e8ab271552751339`; contract blob `92029fdfcc2a6a05374a72b0782808c9d3fa24da`); independent contract review PASS. Non-authorizing: IMPLEMENTATION NOT AUTHORIZED; RED tests NOT AUTHORIZED; evidence generation NOT AUTHORIZED; all later lifecycle gates remain separately owner-gated |
| 6 | Requirement Landscape Synthesis | P1 | NOT STARTED | — |
| 7 | Actionable Validation Plan | P1 | NOT STARTED | — |
| 8 | Journey Reordering and Intent Alignment | P2 | NOT STARTED | — |
| 9 | Single-Intent Question Design | P2 | NOT STARTED | — |
| 10 | Question Intent Registry | P2 | NOT STARTED | — |
| 11 | Question-Aware Evaluation | P2 | NOT STARTED | — |
| 12 | Controlled Unknown Progression | P2 | NOT STARTED | — |
| 13 | Guided Answer Support | P2 | NOT STARTED | — |
| 14 | Adaptive Follow-Up and Completion Logic | P2 | NOT STARTED | — |
| 15 | Guidance Consolidation | P2 | NOT STARTED | — |
| 16 | Final Deliverable Completion and full end-to-end owner validation | Gate | NOT STARTED | — |
| 17 | AI Coach | Post-gate | NOT STARTED — BLOCKED until 1–16 owner-closed | — |

---

*This plan authorizes no implementation. Every workstream and every
lifecycle step remains separately owner-gated. In effect upon commit.*
