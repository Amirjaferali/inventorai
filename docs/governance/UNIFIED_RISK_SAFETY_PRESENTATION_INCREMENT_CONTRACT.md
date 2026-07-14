# UNIFIED RISK AND SAFETY PRESENTATION INCREMENT CONTRACT (Workstream 5)

**Document ID:** UNIFIED_RISK_SAFETY_PRESENTATION_INCREMENT_CONTRACT
**Type:** Increment Contract (DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md §9)
**Status:** OWNER-APPROVED — CLOSED / CANONICAL — IMPLEMENTED, VERIFIED, AND EVIDENCED
**Canonical recording:** recording PR #185; true two-parent merge `8b6868fce5e5fe81f221f3a6e8ab271552751339` (ordered parents `031f455825b2d03c7980e55e990953c063e436f6`, `23edeabeaec834d96d196fa61a53fa5b60cf4cd8`); contract blob `92029fdfcc2a6a05374a72b0782808c9d3fa24da`; recorded 2026-07-14.
**Canonical closure:** implementation and evidence PR #187; true two-parent merge `af8b89b5ea5dfa2d4c7025066a2a377a4d5671ef` (ordered parents `3bf67da09d2a0f64591ba6c874507eada54897c8`, `22cdda37d53dad33ec4b2dfb32a10b6a12acce21`; carrying RED `3cef5eb79a3c3483903f3e0acbe59c18dc05caf0`, GREEN `97b6725953150509059dd41ba623e438f939f094`, evidence `22cdda37d53dad33ec4b2dfb32a10b6a12acce21`); evidence directory `docs/governance/evidence/workstream5_unified_risk_safety/` (22 files, manifest 21/21 OK); independent HEAD GREEN review PASSED; independent evidence review PASSED; non-blocking findings N1/N2 and the Case-C prose observation remain recorded, not fixed; closed 2026-07-14.
**Owner approval record:** WORKSTREAM 5 OWNER CONTRACT DECISIONS AND RECORDING AUTHORIZATION — 2026-07-13/14, approving the proposed contract with owner decisions D1=A, D2=A (revised exact wordings below), D3=A, D4=B (no visual grouping in Workstream 5), D5=A, D6=A, and the D4 contract correction incorporated throughout.
**Workstream / Priority:** Workstream 5 — P1 Unified Risk and Safety Presentation
**Classification:** B — Deliverable assembly / synthesis only
**Authoritative base:** `031f455825b2d03c7980e55e990953c063e436f6`
**Governing authorities:** remediation plan §§3.B(10), 4, 5, 8–15; DELIVERABLE_STABILIZATION_OWNER_DECISION.md; the Workstream 1 Evidence Lock (no new Evidence Lock); the accepted Workstream 5 read-only Source Review (session record at this base; not itself a canonical repository artifact).
**Separate gating:** repository recording of this contract and Workstream 5 implementation remain SEPARATE owner-gated actions; neither is authorized by this document's content.

Provenance labels: **[CANONICAL]** fixed by committed documents · **[SOURCE]** source-review finding · **[OWNER]** owner decision · **[PROPOSED]** contractual requirement of this contract.

---

## 1. Problem statement

**[CANONICAL]** Plan §3.B defect 10: "Contradiction between safety, risk, evidence, and unknown sections" (with a presentation-level touch of §3.B.5 duplication). **[SOURCE]** Proven on the committed Workstream 1 baseline deliverable: Section 6 shows one `[low]` system process-risk row; the Inventor-Stated Safety Signals block shows three inventor-stated fire/danger signals; Section 13 renders "No structurally grounded risks are recorded…" — three architecturally isolated pipelines (`_s6`, `_s15`, `_s13`) with zero cross-references (machine-verified: the safety derivation's only consumer is `_s15`), four uncoordinated risk vocabularies, and near-duplicate signal excerpts.

## 2. User-impact statement

**[OWNER + SOURCE]** A nontechnical inventor reading "What could go wrong" sees a single mild process note and never their own stated fire hazard; elsewhere the same document lists that hazard and also says "no structurally grounded risks are recorded." The net effect can understate stated danger or read as mutual contradiction. After this increment the inventor can see, in one coherent story: what they personally stated (verbatim, labeled), what the system derived, what remains unknown, what has not been established as a structural risk — and why none of that means the invention is safe or risk-free. No inventor-stated safety signal is ever converted into a confirmed risk.

## 3. Verified current behavior

**[SOURCE]** (a) `_s6` emits only system-generated process risks (maturity / evidence-quality / open-gap rows). (b) `_s15` renders the pure safety-signal derivation into `_session_meta.inventor_stated_safety_signals` and the top HTML panel; no other section references signals. (c) `_s13` emits `risks: []`, `has_risks: false`, and the frozen `_ZERO_RISK_DISCLAIMER`. (d) Section 5 carries `risk_if_invalid`; unknowns live in §5/§8/§10/§11 with registry ids. (e) Findings F-A (disconnection), F-B (near-duplicate excerpts), F-C (vocabulary fragmentation), F-D (truthful-limitation juxtaposition: empty Section 6 beside populated signals) are deterministically reproducible; each surface is individually truthful — the defect is disconnection, not falsehood.

## 4. Exact in-scope behavior (cross-reference and synthesis model)

**[OWNER D1/D3/D5 + PROPOSED]** Never an undifferentiated merged-risk list. Exactly:

1. **One additive package-level linkage block** at `_session_meta.risk_safety_linkage` (D5), synthesized ONLY from values already present in the assembled deliverable: signal total, Section 6 risk totals by severity, Section 13 structural-risk state, acknowledged-unknown count, plus the fixed public linkage wordings of §5. It must not perform text mining, re-run safety detection, infer severity, create risks, promote a signal to a risk, or alter any underlying record.
2. **Section 6 linkage note** rendered inside "What could go wrong" whenever inventor-stated safety signals exist, using the exact §5.1 wording.
3. **Qualified empty-Section-6 state**: the bare "No risks recorded." never renders unqualified while signals exist; the exact §5.2 wording is used instead.
4. **Section 13 adjacent contextual note** (D3): rendered next to the untouched frozen disclaimer when signals exist, using the exact §5.3 wording, sourced from the linkage block; NO key inside `section_13_requirement_landscape` is added or modified.
5. **JSON/HTML parity**: every linkage fact rendered in HTML exists as a field in the inventor-facing JSON package, and vice versa.

The authorized linkage locations are limited to: the Section 6 "What could go wrong" presentation, the conditional Section-13-adjacent note, and linkage to the existing Inventor-Stated Safety Signals panel. **No vocabulary notes are added to Section 5 or Section 7 during this increment (D1).**

## 5. Approved exact public wordings (D2 — byte-exact; pinned by the GREEN tests)

**5.1 Section 6 linkage note (signals present):**

```
You also described possible safety consequences in your own words.
See “Inventor-Stated Safety Signals.”

These are your statements, not confirmed risks, and they still require
independent validation.
```

**5.2 Section 6 empty-state qualification (no system-derived risks, signals present):**

```
No system-derived risks were identified from the current session state.

This does not mean the idea is safe or risk-free. Safety consequences you
described are listed separately under “Inventor-Stated Safety Signals” and
have not been independently validated.
```

**5.3 Section 13 adjacent contextual note (signals present):**

```
You also described possible safety consequences in your own words.

They are listed separately under “Inventor-Stated Safety Signals.” They are
not structural risk records and have not been independently validated.
```

The existing frozen Section 13 disclaimer remains byte-identical and is not replaced or rewritten.

## 6. Exact out-of-scope behavior

**[OWNER]** Safety-signal derivation changes of any kind; new risk detection; lexical severity inference; `RequirementLandscape.risks` population; state-model, persistence, transcript-schema, scoring, maturity, gap-logic, or inventor-input-route changes; questionnaire behavior or any new inventor question; AI Coach; Answer Clarification; domain expansion; deletion or semantic merging of any signal or risk row; editing the frozen `_ZERO_RISK_DISCLAIMER`, signal field values, caution text, or any Workstream 2/3/4 public wording; **any visual grouping, progressive disclosure, `<details>`, collapsing, hiding, suppression, or abbreviated rendering of safety-signal statements (D4)**; session-page surfaces (`web/app.py`, `web/templates/session.html`) — this is the deliverable-only design; PR #167/#162 content; `main` synchronization; Workstream 6–16 subject matter.

## 7. Authorized files (closed list)

| File | Necessity |
|---|---|
| `engine/deliverable_assembler.py` | `risk_safety_linkage` synthesis, Section 6 additive fields, the §5 wording constants |
| `web/templates/deliverable.html` | rendering the §5.1 note, the §5.2 qualified empty state, and the §5.3 Section-13-adjacent note |
| `tests/test_unified_risk_safety_presentation.py` (new) | RED/GREEN gate; the only test file authorized by default |

`tests/test_deliverable_hygiene.py` is **NOT** authorized at this stage (D6): the future implementation contract may authorize a narrowly bounded literal amendment ONLY if BASE RED or implementation demonstrates a specific hygiene-protection need that cannot be covered in `tests/test_unified_risk_safety_presentation.py`; such a need triggers STOP and a separate owner decision first. No other file may change; any additional need is a STOP-and-report condition.

## 8. Protected files and frozen behaviors

**[OWNER + SOURCE]** Protected files: `engine/safety_signal.py`, `engine/requirement_landscape.py`, `engine/idea_state.py`, `engine/progression_loop.py`, `web/app.py`, `web/templates/session.html`, persistence/schema files, all Workstream 1–4 evidence trees, `tests/test_deliverable_hygiene.py` (per D6). Frozen behaviors: Workstream 2 detection semantics (negation suppression, attribution guards, benign-failover, sentence bounding, **exact-duplicate dedup — unchanged**); the hygiene guard pinning the safety block's eleven per-signal fields identical to the direct derivation (only additive keys are permitted anywhere in the package); Section 13's exact key set (`tests/test_phase_7c_requirement_landscape_collapse.py:129` — no new §13 keys); the top-level package key set (no new top-level section); Section 6's existing rows and its lowercase "asserted" prose; Workstream 4 criticality wordings and surfaces; machine-status hiding and all committed public wordings; inventor-verbatim preservation; Answer Clarification INACTIVE; persistence FROZEN; AI Coach PROHIBITED; electronics/electrical-only MVP scope.

## 9. Data-provenance rules

Inventor-stated content remains explicitly labeled inventor-stated everywhere it is referenced; linkage fields are synthesized only from values already in the assembled package; every cross-reference names its source category in plain language (the inventor's statements vs system-derived process risks vs structural risk records); verbatim statements are never rewritten, truncated further, paraphrased, or re-detected; every `signal_id`, provenance, and validation status survives unchanged into both JSON and HTML.

## 10. Public-wording rules

All new inventor-facing strings are exactly the §5 wordings — no variants, no paraphrase. No wording may claim safety, claim no danger exists, promote a signal to a risk, soften or replace a disclaimer, or contain any raw internal machine token (all committed hygiene scans must remain green). "Risk", "signal", and "unknown" keep their distinct meanings.

## 11. JSON-package rules

Additive fields only. The linkage block lives at `_session_meta.risk_safety_linkage` (D5; the committed additive-nesting precedent). No key is added to `section_13_requirement_landscape`; no new top-level section is created. Defined no-signal semantics: when zero signals exist, the linkage block records that state truthfully and the §5 notes do not render (the existing unqualified Section 6 presentation is unchanged in that case). The JSON package is inventor-facing: every linkage fact rendered in HTML must exist in JSON.

## 12. HTML-rendering rules

The template reads only values already present in the assembled package (the existing `_s15`-panel precedent). The §5.1 note renders inside the "What could go wrong" section; the §5.2 wording replaces the bare "No risks recorded." only when signals exist; the §5.3 note renders adjacent to the Section 13 disclaimer only when signals exist. No section is reordered or removed. **Signal rendering is byte-for-byte the current behavior: every existing signal continues to render exactly as today (D4).**

## 13. Cross-reference and synthesis rules

Distinct semantic categories are retained; linkage is explicit in reading order (panel ↔ Section 6 ↔ Section 13); apparently conflicting messages are reconciled by explanation, never by deleting or weakening either side; all truthful disclaimers are preserved byte-identical; provenance is preserved; no undifferentiated merged list anywhere.

## 14. Near-duplicate signal presentation (D4 — corrected)

**Near-duplicate signal presentation is not changed in Workstream 5. All existing signal records and current rendering remain intact. Visual grouping is deferred as a known limitation.**

No progressive disclosure, `<details>`, collapsing, grouping, hiding, suppression, or abbreviated rendering of safety-signal statements is authorized. Exact-dedup semantics are untouched. Every underlying signal record, identifier, provenance, and full statement remains in JSON and renders in HTML exactly as today.

## 15. RED test contract (prove on the authorized base; deterministic committed inputs)

The new test file must prove on base, each failure being the missing linkage behavior itself (never a fixture defect; loud fixture guards required):

| # | RED proof | Fixture |
|---|---|---|
| R1 | populated signals + Section 6 lacks any linkage/reference to them (JSON linkage fields absent; the rendered "What could go wrong" region contains no pointer to the signals panel) | the committed Workstream 1 baseline journey (byte-identical inputs) |
| R2 | a `[low]` process-risk row coexists with serious inventor-stated consequences with zero reconciliation | same |
| R3 | the Section 13 disclaimer renders with no adjacent qualification while the signal state is populated | same |
| R4 | a mature/gap-free state renders the bare empty-Section-6 message beside populated signals without the §5.2 qualification | direct-state fixture through the real assembler (maturity 2, no open gaps, demonstrated-quality evidence, one safety-bearing ledger statement) |
| R5 | the disconnection exists identically in JSON and rendered HTML | both fixtures |
| R6 | **documentation-only, NOT a RED-to-GREEN gate (D4):** record the existing repetitive near-duplicate excerpt presentation as a known limitation (a non-failing observation assertion is permitted; it must pass on base AND at head, since the presentation is unchanged) | the committed Workstream 1 baseline journey |

Protected-invariant tests (PASS on base and at head): signal panel content equals the direct derivation; Section 6 rows truthful and untouched; the Section 13 disclaimer byte-identical; no raw internal token inventor-facing; signal rendering byte-identical to current behavior.

## 16. GREEN acceptance contract

At head: the §5 wordings render byte-exact in their three authorized locations under the correct conditions; explicit inventor-stated vs system-derived distinction in every linkage string; the §5.2 qualification replaces the bare empty message only when signals exist; all existing disclaimers byte-identical; JSON↔HTML semantic parity (machine-compared linkage facts); zero severity invention (severity vocabulary and values unchanged); zero new risk rows (Section 6 totals unchanged per fixture; Section 13 `risks == []`); zero removal or alteration of safety records (signal totals, ids, fields, statements, and rendering unchanged); no session-page change (deliverable-only design — no overlap with PR #167 or PR #162); Workstream 2–4 behavior unregressed; zero skips and zero xfails in the new test file.

## 17. Regression suites

`tests/test_safety_signal.py` (18) · `tests/test_safety_signal_stabilization.py` (15) · `tests/test_deliverable_hygiene.py` (22, unmodified) · `tests/test_structured_criticality.py` (18) · `tests/test_increment_4_requirement_landscape.py` (39) · `tests/test_increment_6_deliverable_redesign.py` · `tests/test_phase_5a1_why_this_matters.py` · `tests/test_deliverable_assembler.py` · `tests/test_fdc001_user_value.py` · the unknown-reference suites (`tests/test_evidence_registry_phase3a.py`, `tests/test_unknown_registry_phase3b1.py`, `tests/test_phase_3b2a_section10_unknown_refs.py`, `tests/test_phase_3b2b_section11_unknown_refs.py`) · `tests/test_phase_7b_validation_plan_collapse.py`, `tests/test_phase_7c_requirement_landscape_collapse.py` · the fixed 17-file focused suite plus `tests/test_structured_criticality.py` and the new file (316 baseline + new) · the full suite with no new failure outside the known 31 `tests/test_domain_registry.py` baseline (canonical Workstream 4 closure state: 31 failed / 1379 passed / 1 skipped / 1 xfailed / 24 xpassed).

## 18. Evidence requirements (later-gated; no new Evidence Lock)

A new `docs/governance/evidence/workstream5_unified_risk_safety/` directory only: BASE RED and HEAD GREEN raw outputs; a regenerated Workstream-1-journey deliverable (JSON + HTML) demonstrating the linkage present and defect §3.B.10 absent; the R4 mature/gap-free artifact; a JSON/HTML parity record; a manifest with SHA-256 identities; a deterministic loud-failure harness following the Workstream 3/4 conventions; Workstream 1–4 evidence trees byte-identical.

## 19. Independent-review requirements

Independent read-only review of code + tests + wordings + regenerated evidence + hashes before any merge authorization; corrections re-reviewed. The review must explicitly verify: the §5 wordings byte-exact; the frozen disclaimer byte-identical; no signal promotion; no severity invention; no Section 13 key change; no signal-rendering change; JSON/HTML parity.

## 20. STOP conditions (non-waivable)

Any file outside §7; any change to `engine/safety_signal.py`, the landscape, the state model, routes, or session templates; any `section_13_requirement_landscape` key addition; any frozen-string edit; any severity or risk invention; any signal promotion to risk; any dedup-semantics change; **any visual grouping, disclosure, or abbreviated signal rendering (D4)**; any hygiene-file need (STOP for a separate owner decision per D6); any questionnaire or new-inventor-question drift; any governance-vocabulary leak; any persistence/schema pressure; any reliance on PR #167 or PR #162; ambiguity in any owner decision → STOP and report.

## 21. Merge and closure gates

Lifecycle per plan §11 and the Workstream 3/4 precedent, each step separately owner-gated: contract recording (docs-only Draft PR) → recording review/merge → status canonicalization (plan §15 row 5 → CONTRACT) → separate implementation authorization citing this contract's recorded identity (recording/merge commit SHA + contract blob SHA) verbatim → BASE RED → implementation → HEAD GREEN → evidence → independent review → owner merge (normal true two-parent) → post-merge verification → closure + §15/roadmap sync.

## 22. Known limitations remaining after the increment

Defect 10 is remediated at the deliverable-presentation level only; the architectural separation of the four pipelines remains (by design). Section 5 `risk_if_invalid` and Section 7 caution vocabulary receive no reconciliation in this increment (D1). Session-page presentation is untouched. **Near-duplicate signal presentation is not changed in Workstream 5. All existing signal records and current rendering remain intact. Visual grouping is deferred as a known limitation.** The four Workstream 4 non-blocking hardening observations remain open.

## 23. Resolved owner decisions

D1 = Option A (Section 6 + Section-13-adjacent + panel linkage only; no §5/§7 notes). D2 = Option A with the revised exact wordings of §5. D3 = Option A (conditional note; sourced from the linkage block; §13 keys untouched). D4 = Option B (no visual change; known limitation; corrected throughout this contract). D5 = Option A (`_session_meta.risk_safety_linkage`). D6 = Option A (no hygiene amendment at recording; future need = STOP + separate owner decision).

## 24. Open owner decisions

**None.** All decisions are resolved by the owner decision record of §23; this document records the owner-approved final contract.

---

*This contract authorizes no implementation, no test creation or edit, no evidence generation, and no status-table or roadmap change. Repository recording and implementation remain separate owner-gated actions; implementation must cite this contract's recorded identity (recording/merge commit SHA + contract blob SHA) verbatim.*
