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
| 5 | Unified Risk and Safety Presentation | P1 | CLOSED | Canonical closure (CLOSED / CANONICAL). Closure basis: canonical contract `docs/governance/UNIFIED_RISK_SAFETY_PRESENTATION_INCREMENT_CONTRACT.md` (recording PR #185, merge `8b6868fce5e5fe81f221f3a6e8ab271552751339`; status canonicalized via PR #186, merge `3bf67da09d2a0f64591ba6c874507eada54897c8`); implementation and evidence merged and canonical through PR #187 (true two-parent merge `af8b89b5ea5dfa2d4c7025066a2a377a4d5671ef`; RED `3cef5eb79a3c3483903f3e0acbe59c18dc05caf0`, GREEN `97b6725953150509059dd41ba623e438f939f094`, evidence `22cdda37d53dad33ec4b2dfb32a10b6a12acce21`; evidence directory `docs/governance/evidence/workstream5_unified_risk_safety/`, 22 files, manifest 21/21 OK); independent HEAD GREEN review PASSED; independent evidence review PASSED. Canonical test state: unified-risk-safety 17 passed (zero skipped/xfailed); protected set 148; contract-listed suites 91; fixed focused suite 333; full suite 31 failed / 1396 passed / 1 skipped / 1 xfailed / 24 xpassed with all 31 failures confined to the pre-existing `tests/test_domain_registry.py` baseline (not fixed by this closure). Non-blocking findings N1 (vocabulary seam), N2 (duplicate template lookup), and the Case-C prose observation remain recorded, not fixed. Workstream 6 is not authorized; AI Coach remains prohibited; PR #167 and PR #162 remain outside this closure and untouched; official product state remains `DEMO_READY_WITH_LIMITATIONS`; MVP scope remains electronics/electrical-only |
| 6 | Requirement Landscape Synthesis | P1 | CLOSED | CLOSED / CANONICAL — owner-closed after the canonical contract, BASE RED, implementation, GREEN, evidence, independent reviews, and final post-merge verification. Closure chain: Increment Contract recorded via PR #189 (merge `90f1c34877743510535c397798fcd7da88693606`); status canonicalized via PR #190 (merge `fbe645a761b278b18f57b27a9d691880d989597f`); deterministic BASE RED via PR #191 (merge `721b4613618d74e49707ced4d80b0571e5a2073f`); implementation, HEAD GREEN, owner-authorized protected-test compatibility amendments, and the 42-file evidence package via PR #192 (true two-parent merge `26cdb63e0c63dc3079eaf3b3e7b3612c3bb1c774`, the authoritative merge tip; reviewed head `9c3f6b25ffd7f371929e2910aa1700842192404a`; evidence directory `docs/governance/evidence/workstream6_requirement_landscape_synthesis/`, manifest 41/41 OK; evidence validator PASSED). Canonical gates: focused 12 passed; affected compatibility 34 passed; protected 249 passed with one known pre-existing skip; full suite retained the 31 known failures confined to `tests/test_domain_registry.py` (NOT fixed by this closure). Known limitations L1–L5 remain recorded, unresolved, and non-closure-blocking; the evidence-validator hardening observation remains non-blocking and unresolved. Non-authorizing: no Workstream 7 authorization follows automatically; all later gates remain separately owner-gated |
| 7 | Actionable Validation Plan | P1 | CLOSED | CLOSED / CANONICAL — owner-closed after the canonical contract, BASE RED, bounded implementation, HEAD GREEN, evidence, independent reviews, and final post-publication verification. Closure chain: Increment Contract recorded via PR #194 (merge `f120a3ed43053ba824adc330365e0ef7ad1c48d2`); status canonicalized via PR #195 (merge `4197e6925a3055547b8c17910a5415e0bab4f948`); deterministic BASE RED via PR #196 (RED commit `73a643663efe4646f9de8fd7ba518ce3db6deeee`, merge `e1e71b3b089cd41fc90ca4f2c0b7ce6a37e37268`); bounded implementation and the 39-file evidence package via PR #197 (implementation commit `52b1960fc99af6e746c522b9b32509df1a45076d`, evidence commit `e110ad472e83593020c044d8799a0c9c465c5069`, true two-parent final merge `cbd6cc789536774b8c2d174e92d1cdb4156387bf` — the authoritative tip; evidence directory `docs/governance/evidence/workstream7_actionable_validation_plan/`; validator PASS; manifest 38/38). Canonical gates: focused 18 passed; affected 113 passed; protected battery 259 passed + 1 known pre-existing skip; full suite 31 failed / 1426 passed / 1 skipped / 1 xfailed / 24 xpassed with all 31 failures confined to `tests/test_domain_registry.py` (known, pre-existing, NOT fixed by Workstream 7). D13 is preserved as a mandatory future, separately owner-gated capability — not cancelled, not satisfied by generic specialist referral, not authorized in Workstream 7. Non-authorizing: Workstream 8 is NOT authorized and is not started by this closure |
| 8 | Journey Reordering and Intent Alignment | P2 | CLOSED — CONTRACT CLARIFIED; NO VALID BASE RED SEAM; OBSERVABLE RESIDUE ALREADY SATISFIED; NO GREEN REQUIRED IN CURRENT SCOPE; EXPRESSED-INTENT OBJECTIVES DEFERRED | Increment Contract recorded via PR #231; status canonicalized via PR #232; clarified via Amendment 1 (PR #233) after independent verdict D. Owner-authorized read-only source analysis found the retained observable residue already satisfied by committed production behavior → NO VALID CORRECTED BASE RED SEAM FOUND (no RED invented; no test file or commit created). No BASE RED completed/passed, no GREEN, no intent-aligned reordering implemented, no expressed-intent capture; no revert required (rejected local commit `a2c0d183` never entered authoritative ancestry). Expressed-intent objectives formally deferred to Workstreams 9/10/11/14. Formal disposition/closure: `docs/governance/WORKSTREAM_8_NO_VALID_RED_DISPOSITION_AND_FORMAL_CLOSURE.md`. Must not be reopened without new owner evidence and authorization. |
| 9 | Single-Intent Question Design | P2 | CLOSED — BASE RED, GREEN, EVIDENCE, AND FINAL ACCEPTANCE COMPLETE | Increment Contract merged via PR #235 (`docs/governance/WORKSTREAM_9_SINGLE_INTENT_QUESTION_DESIGN_INCREMENT_CONTRACT.md`), including Addendum A (Critical Paid-Product Experience Requirements), Addendum B (F-1…F-5 resolution: operational single-intent rule + diagnostic probes; conditional Arabic/English parity; downstream-boundary tightening; UX evidence-method mapping), and Addendum C (WS9-FV-1/WS9-FV-2 drafting closure). Records the operational single-intent rule, the critical paid-product experience / non-technical accessibility requirements, and future-technology extensibility; Arabic/English parity remains mandatory but conditional for BASE RED while no committed Arabic variants exist. BASE RED accepted, merged, and published via PR #237 (true two-parent merge `f180eab882f5c5d395ad7ae87a7a09a54315d5f1`; ordered parents `4c7a57142e7714f331a280b4aaaba140da5d4de1` (base), `016f6d66fa84a2dc65911e7ae284ba1d6b78e6d1` (reviewed head, preserved 3-commit chain `a01beb78` → `5ecc0b4b` → `016f6d66`); merge tree `77ca698c575855c48b97b8170f294e725e08696a`, byte-identical to the reviewed head tree; only `tests/test_workstream_9_single_intent_question_design.py` (311 lines) entered the authoritative branch — no production, question-content, UI, registry, schema, evaluator, persistence, analytics, prompt, progression, or Workstream 10+ change), after independent review verdict B — READY WITH NON-BLOCKING RECOMMENDATIONS and owner acceptance. The deterministic BASE RED produces 3 intended assertion failures for the CONFIRMED MULTI-INTENT questions N-PF-1, N-PF-2, and N-BA-1 with 8 protected passes; the 31 known pre-existing `tests/test_domain_registry.py` failures remain the baseline (neither fixed nor worsened). Three non-blocking review recommendations are recorded for the future GREEN gate (GREEN must use natural single-intent wording rather than marker evasion; the exact protected-regression command/result must be recorded in the later WS9 evidence package; the artifact sweep and serving-surface parity diagnostic must remain coupled). GREEN implementation accepted, merged, and independently verified via PR #239 (true two-parent merge `d787a959ce2e66e7e328f761996792b33c237d05`; ordered parents `7fb1ff06` (base), `78f62c9d` (reviewed head); merge tree `437bf885`, byte-identical to the reviewed head tree; only `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json` changed, 3 insertions/3 deletions), rewriting the confirmed multi-intent questions N-PF-1, N-PF-2, and N-BA-1 to single-intent wording after independent GREEN review verdict B — GREEN VALID WITH NON-BLOCKING RECOMMENDATIONS. GREEN gates: WS9 focused 18 passed; protected WS1–8 214 passed; persistence/resume 129 passed + 1 skipped; full suite 31 failed / 1444 passed / 1 skipped / 1 xfailed / 24 xpassed with all 31 failures confined to the known pre-existing `tests/test_domain_registry.py` baseline and zero new unrelated failures. Durable evidence package: `docs/governance/evidence/workstream9_single_intent_question_design/` (MANIFEST.sha256; identity/ancestry, GREEN texts, focused/protected/persistence/full-suite raw outputs, failure-distribution proof). Accepted non-blocking findings preserved: the former "confusing situations" component is no longer directly asked (no N-BA-4 added; placement deferred to a separately authorized content/adaptive-follow-up gate); the N-BA-1 "responsible for handling" wording and N-BA-2 vocabulary overlap remain documented UX observations; the content-spec/implementation-plan quotes (`PATH_N_QUESTION_CONTENT_SPECIFICATION.md`, `FUNCTIONAL_PATH_N_IMPLEMENTATION_PLAN.md`, `NON_SPECIALIST_MODE_SEPARATION_DESIGN_PLAN.md`) are frozen historical defect-baseline records, left unsynchronized with a justified boundary (any forward spec-of-record reconciliation is a separately authorized documentation action). CLOSED / CANONICAL — owner-closed after the full lifecycle: Increment Contract (PR #235), contract status canonicalization (PR #236), deterministic BASE RED (PR #237, independent review verdict B — READY WITH NON-BLOCKING RECOMMENDATIONS), BASE RED status canonicalization (PR #238), GREEN implementation (PR #239, independent GREEN review verdict B — GREEN VALID WITH NON-BLOCKING RECOMMENDATIONS), and the GREEN evidence package + post-GREEN status synchronization (PR #240, independent follow-up verdict A — DOCUMENTARY CORRECTIONS VERIFIED) — all owner-accepted, merged, and independently verified; authoritative closure tip `27184d9e635b6ca72380aa8a5d02433be1ad9ed8`; durable evidence `docs/governance/evidence/workstream9_single_intent_question_design/` (MANIFEST.sha256, all 8 files verify OK). Accepted non-blocking observations are preserved as FUTURE REQUIREMENTS, not completed implementation: the dropped "confusing situations" component placement; no N-BA-4 added; the N-BA-1 "responsible for handling" wording and N-BA-2 vocabulary-overlap UX note; forward current-spec reconciliation of the frozen PATH_N content-spec / implementation-plan quotes; and the exact evidence commands and verdict records. These observations do NOT reopen Workstream 9 and require separate owner authorization if pursued later. Non-authorizing: Workstream 10 (Question Intent Registry) remains NOT STARTED and is not authorized or started by this closure; each later workstream remains separately owner-gated. |
| 10 | Question Intent Registry | P2 | CONTRACT RECORDED AND VERIFIED — STAGE 2 INVENTORY COMPLETED AND VERIFIED — V1 RECORD-SHAPE OWNER DECISIONS MERGED AND VERIFIED — LOADER INTERFACE AND BASE RED SEQUENCE DECISIONS MERGED AND VERIFIED — INTERFACE-CONTRACT BASE RED MERGED AND VERIFIED — MINIMAL INTERFACE GREEN MERGED AND VERIFIED — BEHAVIORAL VALIDATION BASE RED MERGED AND VERIFIED — BEHAVIORAL GREEN MERGED AND VERIFIED — WORKSTREAM 10 FORMALLY CLOSED | Increment Contract recorded and merged via PR #242 (`docs/governance/WORKSTREAM_10_QUESTION_INTENT_REGISTRY_INCREMENT_CONTRACT.md`; contract SHA-256 `922ca76c411bea80505d8e977bbd2f18681dfd0a60dbec357f081d299f556172`, 258 lines). True two-parent merge `456d55f1c456a1cd5b88ea4af385567f7148ce6c`; ordered parents `228f1115` (base), `1534b1e9c0c4f3144f96b04c1c797fb981539cf2` (reviewed contract head, 3-commit chain `1cf2f00` → `6089767` → `1534b1e`); owner-accepted and merged; post-merge verified PASS. The contract records the owner-ratified WS10 v1 decisions (Stage 2 Path N only; separate registry boundary; no persistence; design-time intent only; conditional language; WS10/WS11 evaluation boundary; candidate loader) and separates ratified decisions, invariants, candidate choices, unresolved decisions, future proposals, and current-status context. Prior contract status canonicalization merged and verified via PR #243 (§15 status recorded as CONTRACT RECORDED AND VERIFIED). Stage 2 question inventory COMPLETED AND INDEPENDENTLY VERIFIED (11 committed Stage 2 Path N questions in `electronics_electrical_path_n_questions.json`; all IDs unique; each question's design-gap directly evidenced by its committed JSON parent key; `question_id` unused at runtime; deterministic within-gap serving by `iterations_open`; fixed-priority gap-family selection; `_STALL_REFRAME` is a non-artifact display substitution, not one of the 11 questions; no sufficient behavioral BASE RED seam existed before owner record-shape decisions). v1 Record-Shape Owner Decisions merged and verified via PR #244 (true two-parent merge `b4e67d998cc50c99429d59d3cbce39efb37d4749`; ordered parents `49d26ed9` (base), `40be28674785e5d95122cd6964b5b1e8418c55e8` (reviewed decisions head, 3-commit chain `08487d5` → `52dcbee` → `40be286`); document `docs/governance/WORKSTREAM_10_V1_RECORD_SHAPE_OWNER_DECISIONS.md`; all D1–D17 recorded; D6 source-reference correction recorded — ID-based `{artifact_path, question_id}`, render-safe `N-PF-1` example, and the normative rule that `source_reference.question_id` MUST equal the record's `question_id`). Post-decisions status canonicalization merged and verified via PR #245. Loader Interface and BASE RED Sequence Owner Decisions merged and verified via PR #246 (true two-parent merge `ebed18a68403e0177c6591bf909edf78846b6f17`; ordered parents `116334e4` (base), `6ebf61933d36d502176589b47cedfa7d01a4df13` (reviewed decisions head); document `docs/governance/WORKSTREAM_10_LOADER_INTERFACE_AND_BASE_RED_SEQUENCE_OWNER_DECISIONS.md`; D18–D33 recorded — fixed loader module `engine/question_intent_registry.py`, explicit-path `load_question_intent_registry(registry_path, source_artifact_path)` with no import-time load, immutable public API `get`/`list_records` (no mutation), immutable dataclasses `QuestionIntentRecord`/`QuestionIntentRegistryMetadata`/`QuestionIntentRegistry`, exceptions `QuestionIntentRegistryLoadError` (with `reason_code`) and `QuestionIntentNotFoundError`, load-time validation with unknown-ID at `get`, no caching, stdlib JSON validation with no schema dependency, `{metadata, records}` top-level shape, source-artifact-order `list_records`, and strict no-fallback). Required sequence: Interface-Contract BASE RED → Minimal Interface GREEN → Behavioral Validation BASE RED → Behavioral GREEN. Interface-Contract BASE RED (D31) merged and verified via PR #248 (true two-parent merge `18e7f76836796ee039982372798cc3558edd59e3`; ordered parents `1c68149d` (base), `a4db901c2d7f1e7fc67780e800b21ba8034665d6` (reviewed RED head); one new test file `tests/test_workstream_10_question_intent_registry_interface_contract.py`; six tests collected; two deterministic focused executions each producing the same six controlled contract failures against the not-yet-existing approved module; protected regression `test_path_n_content_config_artifact` + `test_phase2_path_n_selection` + `test_workstream_9_single_intent_question_design` = 38 passed). Minimal Interface GREEN (D32) merged and verified via PR #251 (true two-parent merge `bca45458b90f30b9a7ad6fb88ff04894c8c3097e`; ordered parents `41e06653` (base), `035735db3175a4d75530f96b70e6ae606efb5e4c` (reviewed GREEN head); merge tree `621752f5`; exactly one new production file `engine/question_intent_registry.py`, 144 insertions / 0 deletions). Six Interface-Contract tests passed; protected regression 38 passed; import-no-I/O passed. The approved minimal public interface is implemented: frozen immutable dataclasses (`QuestionIntentRecord`, `QuestionIntentRegistryMetadata`, `QuestionIntentRegistry`) with the exact approved fields; a read-only registry API (`get`/`list_records`, no mutation, no mutable record collection); and the two approved exception types (`QuestionIntentRegistryLoadError` exposing a stable `reason_code`, `QuestionIntentNotFoundError`). `load_question_intent_registry(registry_path, source_artifact_path)` has the exact explicit two-Path signature and remains a fail-loud bounded placeholder using reason_code `MINIMAL_INTERFACE_PLACEHOLDER`, with no import-time loading/I/O and no global cache. No registry JSON or schema exists; successful registry loading is NOT implemented; Behavioral Validation BASE RED and Behavioral GREEN remain NOT STARTED; no runtime, Path N, persistence, database, UI, prompt, AI, or question-content integration exists; WS11 remains NOT STARTED. Implementation is limited to the approved minimal interface. This status synchronization authorizes no next gate automatically; Behavioral Validation BASE RED requires separate explicit owner authorization. Behavioral Validation BASE RED (D33) merged and verified via PR #253 (true two-parent merge `a897bac49a2e071003ebdfb1deae3296e236aa43`; ordered parents `72ab5e771cc335977b33587027b4ebd8ca81509a` (base), `4614661ac8a8001ee1bf293137d86acedb078ea6` (reviewed RED head); merge tree `c5239329b002cc96054e9abf36a3d179833db33f`; exactly one new test file `tests/test_workstream_10_question_intent_registry_behavioral_validation.py`, 357 insertions / 0 deletions). 27 tests collected cleanly; two deterministic focused RED executions each produced 27 controlled `WS10 Behavioral RED` failures with identical failing node IDs and zero collection, fixture, or unexpected errors; the ten asserted reason codes exactly match the owner-approved D26 taxonomy (`MISSING_REQUIRED_FIELD`, `DUPLICATE_QUESTION_ID`, `DUPLICATE_INTENT_ID`, `INVALID_DESIGN_GAP_ID`, `INVALID_METADATA`, `SOURCE_ID_SET_MISMATCH`, `SOURCE_REFERENCE_MISMATCH`, `INVALID_SOURCE_ARTIFACT_PATH`, `INVALID_JSON`, `FILE_READ_ERROR`). Interface-Contract control 6 passed; protected regression 38 passed. Production module `engine/question_intent_registry.py` remains unchanged; the loader remains the fail-loud placeholder using reason_code `MINIMAL_INTERFACE_PLACEHOLDER`; no registry JSON or schema exists; successful registry loading and behavioral validation remain unimplemented; Behavioral GREEN remains NOT STARTED; no runtime, Path N, persistence, database, UI, prompt, AI, or question-content integration exists; WS11 remains NOT STARTED. This synchronization authorizes no next gate automatically; Behavioral GREEN requires separate explicit owner authorization. Behavioral GREEN (D33) merged and verified via PR #255 (true two-parent merge `d309f4822a29dd2e0aa90c6fd6012672430f0941`; ordered parents `17a25e3b8a566296a4fabbb51c4917cb81619967` (base), `8a5b8eae1f28ff7ed7b90207222068c016146dc2` (reviewed GREEN head); merge tree `c959d0a83937bfd5e630235ae22085c75c3414a0`, identical to the reviewed-head tree; exactly one changed production file `engine/question_intent_registry.py`, 333 insertions / 52 deletions; no test or governance file changed in PR #255). Post-merge verified from an isolated worktree at the official merge commit: Behavioral Validation 27 passed twice (exit 0 each); Interface-Contract 6 passed; combined WS10 33 passed; protected regression 38 passed. The Minimal Interface placeholder behavior is removed (`MINIMAL_INTERFACE_PLACEHOLDER` occurrences 0) and replaced by the real loader, which uses only the approved D26 ten-code reason-code taxonomy, has no fallback or partial-success path, performs no import-time registry I/O, preserves committed source-artifact ordering, excludes `_STALL_REFRAME`, and raises `QuestionIntentNotFoundError` for unknown IDs. The full-suite `tests/test_domain_registry.py` failures were independently confirmed pre-existing by identical base-versus-GREEN failing node IDs (base 31 failed / 10 passed; GREEN 31 failed / 10 passed; node-ID diff exit 0), unrelated to WS10 and unmodified. No registry JSON or schema exists; no runtime, Path N, persistence, database, web, UI, prompt, AI, or question-content integration exists. FORMAL WORKSTREAM 10 CLOSURE: all authorized WS10 gates — Increment Contract, v1 Record-Shape Owner Decisions (D1–D17), Loader-Interface and BASE RED Sequence Owner Decisions (D18–D33), Interface-Contract BASE RED, Minimal Interface GREEN, Behavioral Validation BASE RED, and Behavioral GREEN — are complete, merged, and post-merge verified; the final production behavior was merged and post-merge verified; no unresolved WS10 implementation gate remains; WORKSTREAM 10 FORMALLY CLOSED. This closure does not automatically begin or authorize WS11; WS11 remains NOT STARTED and requires a separate explicit owner authorization. Phase A remains fixed at `57e2fac8`; PR #167 and PR #162 remain untouched. |
| 11 | Question-Aware Evaluation | P2 | OWNER DECISIONS CONTRACT MERGED AND VERIFIED — PROTECTED-GUARD AMENDMENT MERGED AND VERIFIED — BASE RED MERGED AND VERIFIED — GREEN MERGED AND POST-MERGE VERIFIED — OWNER ACCEPTANCE RECORDED — WORKSTREAM 11 FORMALLY CLOSED | Owner Decisions and Increment Contract merged and verified via PR #257 (true two-parent merge `9f7c2c9018b3d96092af6ec446a1f4d06b784ffd`; ordered parents `03591abc153bfcb0b7c5371085e2e0093501d535` (base), `036e533e12ff45e17012177d0d08a8353e98fb33` (reviewed contract head); merge tree `d6f84082d9c4a9157efe3503b25ce924f66c9c2c`; exactly one new governance document `docs/governance/WORKSTREAM_11_QUESTION_AWARE_EVALUATION_OWNER_DECISIONS.md`, 516 insertions / 0 deletions; no existing file changed in PR #257). The contract ratifies the F1–F11 repository baseline and eighteen owner decisions D1–D18: WS11 v1 is a deterministic, question-bound STRUCTURAL evaluation observation only (no gap closure, no `evaluate_transition` change, no `Evidence`/`IdeaState` mutation, no `scoring.py` change); atomic `ServedQuestion` binding of `question_id` + question text + `design_gap_id` from one immutable committed source entry, with `question_id` reconstruction, inference, derivation, parsing, matching, hashing, translation, normalization, fuzzy-matching, or reverse-lookup from question text expressly prohibited; the deterministic structural tier mapping (`DEMONSTRATED→SATISFIED`, `REASONED→PARTIALLY_SATISFIED`, `ASSERTED→NOT_SATISFIED`, integrity→`INVALID_INPUT`) explicitly does NOT prove semantic fulfilment of `answer_objective`/`completion_condition` (structural-versus-semantic boundary); content-intent matching remains deferred and blocked (no AI, LLM, embeddings, keyword approximation, or silent language-specific fallback); a new pure module `engine/question_aware_evaluation.py` consuming the injected WS10 registry, fail-loud typed errors, no persistence/UI/runtime change. Post-merge verified: canonical status files were unchanged in PR #257; protected surfaces unchanged; post-merge worktree clean. No production code, test, protected WS9 guard, registry artifact, or schema was changed. WS11 implementation remains NOT STARTED; the next prerequisite is the separately authorized protected-guard amendment (removing only `engine.question_aware_evaluation` from the WS9 absence guard while preserving the WS13/WS14 guards) before BASE RED. This canonicalization authorizes no next gate automatically and does not imply that BASE RED or implementation is authorized; the protected-guard amendment, BASE RED, and GREEN each require separate explicit owner authorization. WS10 remains FORMALLY CLOSED; Phase A remains fixed at `57e2fac8`; PR #167 and PR #162 remain untouched. Protected-guard amendment merged and verified via PR #259 (true two-parent merge `34cc8ed5dd45fdbc8df914bb1f6d5c00a20519ac`; ordered parents `f6f4b10c6b4c947d91850084bbc933a9f9e1edf4` (base), `941d49bb4903e2548defc49dbdbbf3ce850a0904` (reviewed guard-amendment head); merge tree `cf40a4b61ba0e53990a2436597bdc687ff7aa67d`; exactly one existing test file changed `tests/test_workstream_9_single_intent_question_design.py`, 13 insertions / 9 deletions; no production or governance file changed in PR #259). The stale WS11 absence guard for `engine.question_aware_evaluation` was removed from the protected tuple (the module is ratified as the future WS11 boundary by PR #257) and the protected test was truthfully renamed to `test_PROTECTED_no_workstream_13_to_14_capability_introduced`; the WS13 (`engine.guided_answer_support`) and WS14 (`engine.adaptive_follow_up`) absence guards remain intact. Post-merge verified: renamed test passed directly; complete WS9 file 18 passed; protected regression 38 passed; combined WS10 registry suites 33 passed; `engine/question_aware_evaluation.py` remains absent and no WS11 BASE RED test exists; post-merge worktree clean. BASE RED and GREEN remain NOT STARTED; the next gate is BASE RED under separate explicit owner authorization. BASE RED merged and verified via PR #261 (true two-parent merge `77adcbdad68153f38e68066b0cba4ae89495b1bf`; ordered parents `0be05b94d4b1f8a9c51a634451d3a5e95c070fa8` (base), `2130b2a49c5c9abc818a83e3e8c4006fa642d5f3` (reviewed BASE RED head); merge tree `86a20a9382551572cfd6dcf7b5274674deee751f`; exactly one new test file `tests/test_workstream_11_question_aware_evaluation_base_red.py`, 435 insertions / 0 deletions; no existing test and no production or governance file changed in PR #261). Post-merge verified: 15 tests collected successfully; RED run 1 15 failed with zero errors; RED run 2 15 failed with zero errors; identical failing node IDs across both runs; five failures for the absent atomic served-question seam (`engine.path_n_questions.get_served_question` / `ServedQuestion`, D4) and ten failures for the absent evaluator module (`engine.question_aware_evaluation`, D2/D3/D6/D9), all controlled decision-tagged `WS11 BASE RED` failures (no collection/fixture/unexpected error); complete WS9 file 18 passed; protected regression 38 passed; combined WS10 registry suites 33 passed; `engine/question_aware_evaluation.py` remains absent; post-merge worktree clean. GREEN remains NOT STARTED and requires separate explicit owner authorization after this BASE RED status canonicalization is merged and post-merge verified. GREEN implementation merged and post-merge verified via PR #264 (true two-parent merge `fe721e1e6a47fbc627cea88ad6c68c49040b8939`; ordered parents `6aadc9085fb69414d0d15642a759c47ea542d4a9` (base), `759f7acdac74509707039b3f84786040ae04c8db` (reviewed reconciled GREEN head); merged tree `735bb8ca0440f46128c312bc307334353e70536b`; merged production scope exactly `engine/path_n_questions.py` (M) and `engine/question_aware_evaluation.py` (A), 2 files changed / 193 insertions / 4 deletions; the reconciled GREEN implementation is byte-identical to the reviewed quarantined implementation — patch-id and both file blobs match). Post-merge verified: WS11 focused suite 15 passed; complete WS9 file 18 passed; protected regression 38 passed; WS10 registry suites 33 passed; affected Path N tests 91 passed; full suite 31 failed / 1492 passed / 1 skipped / 1 xfailed / 24 xpassed, with all 31 failures confined to the existing `tests/test_domain_registry.py` baseline and zero non-domain-registry failures. GREEN implements the ratified WS11 v1: the atomic frozen `ServedQuestion` (`question_id` + `text` + `design_gap_id` from one committed entry; `get_path_n_question` retained as a backward-compatible text wrapper; no `question_id` recovery from text) and the pure `evaluate_question_intent(question_id, base_quality, served_design_gap_id, registry) -> QuestionIntentEvaluation` (injected WS10 registry, deterministic structural tier→outcome, fail-loud typed errors, observation-only, no file I/O, no state mutation, no content-intent claim). FORMAL WORKSTREAM 11 CLOSURE: owner decisions CLOSED; protected-guard amendment CLOSED; BASE RED MERGED AND VERIFIED; GREEN MERGED AND POST-MERGE VERIFIED; owner acceptance RECORDED (OWNER ACCEPTED — PR #264); all authorized WS11 gates are complete, merged, and post-merge verified; no unresolved WS11 gate remains; WORKSTREAM 11 FORMALLY CLOSED. This closure does not begin or authorize any later Workstream; Workstream 12 (Controlled Unknown Progression) remains NOT STARTED and requires separate explicit owner authorization. WS10 remains FORMALLY CLOSED; Phase A remains fixed at `57e2fac8`; PR #167 and PR #162 remain untouched. |
| 12 | Controlled Unknown Progression | P2 | WS12 CONTRACT AND OWNER DECISIONS MERGED AND POST-MERGE VERIFIED — WS12 STATUS CANONICALIZATION MERGED AND POST-MERGE VERIFIED — WS12 BASE RED MERGED AND POST-MERGE VERIFIED — WS12 GREEN MERGED AND POST-MERGE VERIFIED — OWNER ACCEPTANCE RECORDED — WORKSTREAM 12 FORMALLY CLOSED | Fresh WS12 Controlled Unknown Progression increment contract and its ratified Owner Decisions merged and post-merge verified via PR #268 (true two-parent merge `be8bfd5ba8d72b288a3d2b67658ef6ea03d49031`; ordered parents `b4e38c0fae6be4c9a95e9bb92bdb75bf8e9ba656` (base, PR #267 tip), `4387ad754b9d53635bd4ce41e7ec2264aa80f7db` (verified correction head); merge tree `b8aa5d962872c7d675400b2fefa9c4ca4c80280b`; merged scope exactly one new governance document `docs/governance/WORKSTREAM_12_CONTROLLED_UNKNOWN_PROGRESSION_INCREMENT_CONTRACT.md` (A); `git diff --check` clean; no code, test, schema, persistence, UI, prompt, question-content, scoring, roadmap, remediation-plan, or capability-register change in the merged scope). The contract was authored fresh from the authoritative tip and fully supersedes the earlier premature WS12 artifact (branch `docs/workstream-12-increment-contract`, commit `12dbad1`, classified SUPERSEDED / PREMATURE — DO NOT USE), re-deriving all findings from the current repository. It records the evidence lock; source-review inventory; current deterministic behavior (`evaluate_transition`, `integrate_response`); current unknown-handling seams (the acknowledged-unknown parallel track with no progression effect; the append-only six-`INTERACTION_DISPOSITIONS` `AssertionRecord` ledger with `resolves_gap` always `False`; the non-destructive contradiction/supersession graph; the Increment-2 provenance/validation axes; the `ACCEPTED_RISK` gap-status seam that is defined in the source model but has no verified production-engine assignment path; the separate decision-workspace blocker model; WS11 observation-only evaluation); valid and invalid implementation seams; protected boundaries; a mandatory capability-register overlap review; scope and non-goals; proposed deterministic contract boundaries; and the sixteen ratified Owner Decisions OD-1…OD-16, each `OWNER DECISION — RATIFIED` and `RESOLVED BEFORE BASE RED`. OD-1 observation-only v1; OD-2 reuse `AcknowledgedUnknown` + `AssertionRecord` (no third record system); OD-3 the six proposed WS12 controlled-unknown path classifications (`NEEDS_EVIDENCE`, `NEEDS_MEASUREMENT`, `NEEDS_TEST`, `NEEDS_SPECIALIST`, `DEFERRED_BY_USER`, `OUT_OF_SCOPE`) are a SEPARATE vocabulary distinct from the six existing `INTERACTION_DISPOSITIONS` (`answered`, `unknown`, `deferred`, `provisional_assumption`, `specialist_requested`, `evidence_requested`), which — at contract-ratification time — were not yet present in tracked production source and were not yet authorized for implementation, and were subsequently implemented only through the separately authorized, merged, and post-merge-verified BASE RED and GREEN gates recorded below, with no silent mapping between the two; OD-4 blocker classification only (no blocking); OD-5 criticality read-only; OD-6 closure-path recommendation only (no `ACCEPTED_RISK`, no gap closure, no `resolves_gap=True`); OD-7 no false resolution; OD-8 supersession preserves history; OD-9 multiple records allowed (no auto-dedup); OD-10 uniform sufficiency; OD-11 safety-critical visibility; OD-12 in-memory / non-exporting; OD-13 D13 boundary only; OD-14 strict WS13/WS14 separation; OD-15 CAP-04/CAP-08/CAP-10 typed interface boundaries only; OD-16 no CAP-12/CAP-13/CAP-14 behavior. This recorded the completion of the WS12 contract and owner-decision prerequisite gate. At that contract and Owner-Decisions prerequisite gate, WS12 remained NOT STARTED; BASE RED had not started and was not authorized; GREEN was not authorized. Ratification of OD-1…OD-16 did not itself start WS12 or authorize a later gate, and no later Workstream or Capability activated automatically at that gate (the BASE RED, GREEN, and formal-closure gates recorded below were each subsequently and separately owner-authorized, merged, and post-merge verified). CAP-12, CAP-13, and CAP-14 remain `RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION`; Structured Technical Guidance / D13, Patent Export, and WS-PFV-001 remain inactive and separately gated. Workstreams 9, 10, and 11 remain FORMALLY CLOSED; Phase A remains fixed at `57e2fac8`; PR #167 and PR #162 remain untouched. WS12 status canonicalization (§15 pre-GREEN row and the roadmap) merged and post-merge verified via PR #269 (merge `26f1e044991dc2fef2fad89d4657ff5d077d3f85`). WS12 BASE RED merged and post-merge verified via PR #270 (true two-parent merge `3ab872c13d7e827b7f0569d762cda2679fe00b8b`; ordered parents `26f1e044991dc2fef2fad89d4657ff5d077d3f85` (base), `919432af39576395f68bbe221813b6b9fced0c08` (reviewed corrected BASE RED head); merge tree `bcfe42c1d4b99124fb866b9504e3d53e97249371`; exactly one new test file `tests/test_workstream_12_controlled_unknown_progression_base_red.py`, 22 deterministic tests that failed only because `engine.controlled_unknown_progression` was absent, with two focused runs producing identical failing node IDs and reason). WS12 GREEN merged and post-merge verified via PR #271 (true two-parent merge `046d4c0b0ab02511079165c3d5ebcbd8e4fea94b`; ordered parents `3ab872c13d7e827b7f0569d762cda2679fe00b8b` (base), `1011aa06d9b3bf12adff92bdba84b32c5ad4c7d2` (reviewed GREEN head); merge tree `a83332c087cc4772cf3dc6a73ab8fddbe9711df4`; exactly one new production module `engine/controlled_unknown_progression.py`, 203 insertions / 0 deletions; the merged RED tests unchanged). Post-merge verification from the authoritative tip `046d4c0b0ab02511079165c3d5ebcbd8e4fea94b`: focused WS12 suite 22 passed; WS9 18 passed; WS10 33 passed; WS11 15 passed; WS9/Path-N protected regression 38 passed; full suite 31 failed / 1514 passed / 1 skipped / 1 xfailed / 24 xpassed, with all 31 failures confined to the pre-existing `tests/test_domain_registry.py` baseline and zero non-domain-registry (new) failures. The GREEN module is deterministic, AI-free, network-free, in-memory, and observation-only, preserving every ratified boundary (OD-1 observation-only; OD-2 reuse of AcknowledgedUnknown/AssertionRecord with no third record system; OD-3 the six WS12 path classifications distinct from INTERACTION_DISPOSITIONS with no implicit mapping; OD-4 blocker report-only; OD-5 criticality read-only; OD-6 closure recommendation only with resolves_gap always False and ACCEPTED_RISK rejected; OD-8 supersession preserves history; OD-9 multiplicity without dedup; OD-10 uniform sufficiency; OD-11 safety-critical visibility; OD-12 in-memory/non-exporting; OD-13 D13 boundary; OD-14 WS13/WS14 separation; OD-15 CAP-04/08/10 interface-only; OD-16 no CAP-12/13/14 behavior). Durable evidence package: `docs/governance/evidence/workstream12_controlled_unknown_progression/` (MANIFEST.sha256; identity/ancestry, focused/protected/full-suite raw outputs, failure-distribution proof). FORMAL WORKSTREAM 12 CLOSURE: WS12 contract and Owner Decisions MERGED AND POST-MERGE VERIFIED; WS12 status canonicalization MERGED AND POST-MERGE VERIFIED; WS12 BASE RED MERGED AND POST-MERGE VERIFIED; WS12 GREEN MERGED AND POST-MERGE VERIFIED; owner acceptance RECORDED (OWNER ACCEPTED — PR #271); all authorized WS12 gates are complete, merged, and post-merge verified; no unresolved WS12 gate remains; WORKSTREAM 12 IS FORMALLY CLOSED. This closure does not begin or authorize any later Workstream or Capability; WS13 remains NOT STARTED — NOT AUTHORIZED, WS14 remains NOT STARTED, and the AI Coach (WS17) remains BLOCKED until Workstreams 1–16 are owner-closed. CAP-12, CAP-13, and CAP-14 remain RECORDED — NOT AUTHORIZED FOR IMPLEMENTATION; Structured Technical Guidance / D13, Patent Export, and WS-PFV-001 remain inactive and separately gated. |
| 13 | Guided Answer Support | P2 | OWNER DECISIONS MERGED AND VERIFIED — FRESH INCREMENT CONTRACT MERGED AND VERIFIED — BOUNDED OBSERVABLE-DEFECT SEARCH COMPLETED — NO VALID RED SEAM FOUND — DURABLE NO-VALID-RED EVIDENCE PACKAGE OWNER-ACCEPTED — PR #277 MERGED AND POST-MERGE VERIFIED — CLOSED WITHOUT BASE RED, IMPLEMENTATION, OR GREEN — WORKSTREAM 13 FORMALLY CLOSED | WS13 Evidence Lock and Fresh Source Review completed and accepted (read-only, on authoritative tip `8184c7ed66b076596d1f2ef0bc102cf95f6559c9`). WS13 Owner Decisions OD-1 through OD-14 merged and post-merge verified via PR #273 (true two-parent merge `26b39e7f49b702030882feb50a5ba457558254cc`; ordered parents `8184c7ed66b076596d1f2ef0bc102cf95f6559c9` (base), `d69042043597d91d2a4c3c970d8f3858e10cb0f1` (reviewed owner-decisions head); merge tree `6a355e2e0ce8055882065588a17a0265784eca7f`; merged scope exactly one new governance document `docs/governance/WORKSTREAM_13_GUIDED_ANSWER_SUPPORT_OWNER_DECISIONS.md`, 196 insertions / 0 deletions; protected verification PROTECTED_DIFF_EXIT=0). The ratified decisions bound a future WS13 Increment Contract: WS13 governs and boundedly improves the existing display-layer guided-answer support and is not treated as wholly absent (OD-1); WS13 v1 is web/display-layer only with no `engine.guided_answer_support` module (OD-2) and the existing absence guard preserved (OD-3); WS13 reads the served question, `question_id`/`design_gap_id`, `gap_type`, `last_result`, and explicit uncertainty but influences no assessment/scoring/progression/gap/maturity/completion/follow-up (OD-4); it helps the user write their own answer and never invents facts, authors/rewrites/completes, or submits/persists without explicit confirmation (OD-5); single-intent preserved (OD-6); strict D13 (OD-7), WS12 (OD-8), WS14 (OD-9), and WS15 (OD-10) separation; EN/AR parity where committed with missing Arabic reported as a gap (OD-11); deterministic provenance (OD-12); defect-driven minimal increment (OD-13); and a governed no-valid-RED closure path (OD-14). The existing display-layer WS13-like behavior (`web/answer_coauthoring_prompts.py`, `web/scaffolding_guidance.py`, `web/uncertainty_guidance.py`, `web/clarification_labels.py`, `web/result_feedback.py`) is recorded as pre-existing and is NOT silently reclassified as completed WS13 implementation. WS13 REMAINS NOT STARTED; the WS13 Increment Contract HAS NOT STARTED AND IS NOT AUTHORIZED; BASE RED, GREEN, implementation, status beyond this canonicalization, and closure are NOT AUTHORIZED. `engine.guided_answer_support` remains absent and the WS13 (`engine.guided_answer_support`) and WS14 (`engine.adaptive_follow_up`) absence guards remain unchanged. This canonicalization authorizes no next gate automatically; the WS13 Increment Contract requires a separate explicit owner authorization. WS14, WS15, WS16, WS17, D13 (Structured Technical Guidance), Patent Export, WS-PFV-001, and CAP-12/CAP-13/CAP-14 remain inactive, blocked, separately gated, or unauthorized. Workstreams 9, 10, 11, and 12 remain FORMALLY CLOSED; Phase A remains fixed at `57e2fac8`; PR #167 and PR #162 remain untouched. The WS13 Fresh Guided Answer Support Increment Contract is merged and post-merge verified via PR #275 (true two-parent merge `cbf3c3a7f7d33c03f19091af92572c99852f7f28`; ordered parents `8f08fbe0f2649b10f90545814bc02fe67fae714e` (base), `eafb9279e3c8997c8d2b50c4a9ee513400353536` (reviewed corrected contract head); merge tree `c0fdd8feead6c1cafffbdef4f3864393a7413a16`; accepted contract commit chain `885d387bc6522ed7bc63e890758caa4e90da4b1d` → `eafb9279e3c8997c8d2b50c4a9ee513400353536`; merged scope exactly one new governance document `docs/governance/WORKSTREAM_13_GUIDED_ANSWER_SUPPORT_INCREMENT_CONTRACT.md`, 314 insertions / 0 deletions; protected verification PROTECTED_DIFF_EXIT=0). The merged contract is documentation-only and bounds a future WS13: WS13 v1 stays web/display-layer only over the existing display-layer seams (`web/answer_coauthoring_prompts.py`, `web/scaffolding_guidance.py`, `web/uncertainty_guidance.py`, `web/clarification_labels.py`, `web/result_feedback.py`) with no `engine.guided_answer_support` module and the WS13/WS14 absence guards preserved; it ratifies the bounded no-valid-RED evidence-search path (WS13-CD-2 / OD-14) as the required outcome when the bounded search finds no proven observable defect; it records the English-only localization expansion as OUTSIDE WS13 v1 (WS13-CD-1); and it ratifies the §10 protected regression set for WS13 v1 (WS13-CD-3). The existing display-layer WS13-like behavior is recorded as pre-existing and is NOT reclassified as completed WS13 implementation. WS13 REMAINS NOT STARTED; BASE RED, GREEN, implementation, closure, and any later gate are NOT AUTHORIZED; `engine.guided_answer_support` remains absent and the WS13/WS14 absence guards remain unchanged. This canonicalization authorizes no next gate automatically; the bounded defect search, BASE RED, and every later gate each require a separate explicit owner authorization. FORMAL WORKSTREAM 13 CLOSURE (OD-14 / WS13-CD-2 no-valid-RED path): a bounded, read-only observable-defect search across the five existing display-layer seams (`web/answer_coauthoring_prompts.py`, `web/scaffolding_guidance.py`, `web/uncertainty_guidance.py`, `web/clarification_labels.py`, `web/result_feedback.py`) was completed and found NO VALID WS13 RED SEAM (**valid observable defect count: 0**); a durable no-valid-RED evidence package was produced, independently reviewed, and owner-accepted, and is retained under `docs/governance/evidence/workstream13_no_valid_red/`; the package was merged and post-merge verified via PR #277 (true two-parent merge `9ba3e68df69b601b70567cec85ae2c0c057f6c70`; ordered parents `0598a05137912866bab49f67b0c82048b282f85d` (base), `279d988b235ca900aa6bcb97a00aa1c215d3167f` (owner-accepted final evidence head); merge tree `7a1c10f0ee3a1a6a1da9f2e34bc099ab4d0e834b`; evidence-only scope; PROTECTED_DIFF_EXIT=0; the evidence manifest verifies successfully at the authoritative tip). WS13 is therefore CLOSED WITHOUT BASE RED, IMPLEMENTATION, OR GREEN: BASE RED was not required and must not be manufactured; no `engine.guided_answer_support` implementation was introduced and the WS13/WS14 absence guards remain unchanged; no GREEN implementation occurred; the closure follows OD-14 / WS13-CD-2. WORKSTREAM 13 IS FORMALLY CLOSED. This closure does not automatically activate WS14 or any later workstream; WS14 remains NOT STARTED and unauthorized; WS15, WS16, WS17, D13 (Structured Technical Guidance), Patent Export, WS-PFV-001, and CAP-12/CAP-13/CAP-14 remain inactive, blocked, separately gated, or unauthorized. Workstreams 9, 10, 11, and 12 remain FORMALLY CLOSED; Phase A remains fixed at `57e2fac8`. |
| 14 | Adaptive Follow-Up and Completion Logic | P2 | NOT STARTED | — |
| 15 | Guidance Consolidation | P2 | NOT STARTED | — |
| 16 | Final Deliverable Completion and full end-to-end owner validation | Gate | NOT STARTED | — |
| 17 | AI Coach | Post-gate | NOT STARTED — BLOCKED until 1–16 owner-closed | — |

---

*This plan authorizes no implementation. Every workstream and every
lifecycle step remains separately owner-gated. In effect upon commit.*
