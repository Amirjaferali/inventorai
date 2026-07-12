# DELIVERABLE HYGIENE INCREMENT CONTRACT (Workstream 3)

**Document ID:** DELIVERABLE_HYGIENE_INCREMENT_CONTRACT
**Type:** Increment Contract (DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md §9)
**Status:** OWNER-APPROVED — CANONICALLY RECORDED — NO IMPLEMENTATION AUTHORIZED
**Canonical recording:** recording PR #175; true two-parent merge `0189577f269366dc3201cb4cfeb32875a904d4e9` (ordered parents `3d288f2f51d18e47977f5213722993a25aeb7ba3`, `a196f9f9ef8d3b635220b5e4f87b57f9c3d1f53a`); contract pre-sync blob `113139067faa5048b9f38033bfe34548dc356f9c`; recorded 2026-07-12.
**Owner approval record:** WORKSTREAM 3 DELIVERABLE HYGIENE INCREMENT CONTRACT — APPROVED — 2026-07-12, incorporating the final revised contract plus the three binding recording corrections (Final-Deliverable serialization distinction; Defect-4 heading correction; existing-safety-test clarification).
**Workstream / Priority:** Workstream 3 — P0 Deliverable Hygiene
**Governing evidence:** remediation plan §§3.B(3–4), 5, 8–15; WS1 defect manifest rows 3–4; WS1 baseline `docs/governance/evidence/workstream1_deliverable_baseline/` (tree `a49a51338aaefd82d0f060308464c90dbe68b14c`); the Workstream 3 read-only Source Review, completed and accepted by the owner as sufficient for contract derivation (session record at tip `3d288f2f51d18e47977f5213722993a25aeb7ba3`; not itself a canonical repository artifact).
**Separate gating:** repository recording of this contract and Workstream 3 implementation remain SEPARATE owner-gated actions; neither is authorized by this document's content.

---

## 1. Problem statement (the two target defects only)

**Defect 3 — raw system-state leakage into the final deliverable.** Rendered
HTML shows `Criticality: UNDETERMINED (system-derived)` (§13) and
`[low] Evidence is REASONED (substantiated but not demonstrated).` (§6); the
final Deliverable JSON carries raw internal values throughout
(`UNDETERMINED`×27, `system-derived`×13, `REASONED`×22, `OWNER_EXECUTABLE`×12,
`LEGACY_UNSPECIFIED`×10, `CONFIDENCE_UNDETERMINED`, raw gap-type enums,
machine status tokens such as `resolution_status: "stated"`).

**Defect 4 — inconsistent or unexplained requirement counts.** §4 reports
`total: 8` (evidence-derived + closed-gap items), §13 reports `total: 13`
(assertion-led Requirement Landscape), §14 emits 13 steps — overlapping
"requirements" labeling with no declared basis or relationship.

## 2. Current behavior

`assemble_deliverable` serializes internal dataclass/enum values directly into
the package; `deliverable.html` renders §13 criticality/authority verbatim and
§6 prose embeds the raw quality token (both the `REASONED` and `ASSERTED`
branches have this shape); `_s4` and `derive_requirement_landscape` aggregate
different conceptual sets under the same label with independent totals; §14
derives from §13 without declaring the tie.

## 3. Required behavior

Both inventor-facing final-deliverable surfaces are free of internal
vocabulary; §4/§13/§14 totals carry the contract-bound machine identifiers,
meanings, and relationship of §7; every bound count equals the length of the
exact collection it claims to count; internal canonical state is unchanged and
fully traceable internally.

## 4. Definitions (binding)

- **Internal canonical state:** `IdeaState` and the engine dataclasses/enums
  (`RequirementLandscape`, `ValidationPlan`, `SafetySignal`, evidence/quality/
  status vocabularies). Unchanged by this workstream.
- **Final Deliverable JSON:** the complete package returned by
  `assemble_deliverable(state)` as served to the inventor, including
  `_session_meta` — an inventor-facing surface (owner Decision 1).
- **Final Deliverable HTML:** the rendered output of
  `web/templates/deliverable.html` — inventor-facing.
- **Final Deliverable serialization contract (binding correction):** the
  inventor-facing serialization of the package produced by
  `engine/deliverable_assembler.py::assemble_deliverable`. This Workstream is
  explicitly authorized to make the narrow inventor-facing Final Deliverable
  JSON serialization changes required by this contract (enumerated in §9.6).
  Where this contract prohibits "schema" changes, that prohibition refers to
  the Prohibited Schemas and Models of §9.7 and NEVER to the Final Deliverable
  serialization changes §9.6 authorizes.
- **Inventor-facing language:** plain, truthful wording free of internal enum
  names, raw state tokens, internal authority/provenance/confidence values,
  internal gap-type names, scoring vocabulary, and implementation-oriented
  vocabulary; making no validation/readiness/safety/compliance/feasibility/
  patent claim.
- **Internal vocabulary leakage:** a Prohibited Token (§8.1) or an unambiguous
  syntactic equivalent appearing in an inventor-facing surface outside the
  §8.3 verbatim exemptions.
- **Verbatim inventor text (exempt):** an output value proven byte-derived
  from a specifically enumerated verbatim inventor-input field (§8.3). Nothing
  else is exempt: generated prose, synthesized summaries, labels, metadata,
  status, authority, provenance, confidence, scoring vocabulary, count
  explanations, and enum-derived values are never exempt.
- **Count basis:** the declared machine identifier of the exact collection a
  displayed total counts (§7).
- **Requirement Landscape (§13 set):** active assertion-led requirement
  anchors plus open-gap anchors, per Increment 4.
- **Evidence-derived requirement set (§4 set):** items derived specifically
  from recorded problem evidence, mechanism evidence, and resolved gaps, per
  `_s4`.
- **Internal diagnostic evidence vs. regenerated inventor-facing
  deliverables:** the WS3 evidence directory distinguishes (a) internal
  diagnostic records (token scans, count comparisons, internal-object dumps —
  MAY contain raw values) from (b) regenerated inventor-facing deliverable
  artifacts (MUST satisfy this contract's hygiene criteria). The two are
  stored and labeled separately.

## 5. Binding owner decisions

1. **Surface:** final Deliverable JSON **and** rendered HTML are both
   inventor-facing; raw internal tokens must not appear in either. Adding
   display labels while retaining raw tokens elsewhere in the final JSON does
   **not** close Defect 3.
2. **Traceability:** raw values remain available in internal state objects
   and committed internal diagnostic evidence; they are not exported inside
   the inventor-facing final JSON. Raw internal fields must NOT be preserved
   in the final Deliverable JSON merely for backward compatibility. If an
   existing consumer outside the final deliverable rendering/export path
   requires a raw field this contract removes, STOP and report the exact
   consumer before implementation. No prohibited-schema (§9.7) change unless
   proven unavoidable — in which case STOP and request contract reopening;
   the expected design is the §9.6 deliverable-generation boundary
   transformation in `assemble_deliverable`.
3. **Prohibited vocabulary:** the §8.1 token list at minimum; no
   indiscriminate natural-language blacklist; `recorded`/`stated` prohibited
   only as machine field values exposing a raw internal status or
   implementation contract, never as ordinary inventor-facing English; the
   leakage test is semantic and field-aware, not only a global substring
   search.
4. **Count semantics:** bound in §7 of this contract — no implementation-time
   renaming; never one artificial shared number; no silent overwrite of one
   set by the other.
5. **Existing tests:** governed by §12 — default rule: ALL existing tests
   remain unchanged; STOP-and-report before any enumerated, owner-approved
   exception. This contract approval grants NO test-edit authorization.

## 6. Safety-Signal requirements (no broad carve-out)

1. **Workstream 2 semantic invariance:** signal content, count, ordering, raw
   inventor statements (excerpts), and validation disclaimers remain
   unchanged; `derive_inventor_stated_safety_signals` is untouched.
2. **Hygiene applies to the block too:** no internal enum, authority,
   provenance, confidence, scoring, or implementation token may be exported
   in the final inventor-facing JSON or HTML anywhere, including within the
   Safety-Signal block. Only exact verbatim inventor text (the signal
   `statement` excerpts) is exempt from prohibited-token scanning.
3. Where the canonical Workstream 2 block is already inventor-facing, it must
   remain **byte-identical**.
4. **If hygiene would require changing the Workstream 2 block, STOP and
   request separate owner review.** This contract does not authorize that
   change. (Verified at drafting: the §8.1 Prohibited Tokens do not occur in
   the WS2 block's generated fields, so no conflict is currently expected;
   any discovery to the contrary triggers this STOP.)

## 7. Count semantics (contract-bound identifiers and meanings)

1. **Section 4:** `count_basis: evidence_derived_requirements` — meaning:
   requirements derived specifically from recorded problem evidence,
   mechanism evidence, and resolved gaps.
2. **Section 13:** `count_basis: requirement_landscape` — meaning: the
   broader set of active assertion-led requirement anchors and open-gap
   anchors.
3. **Required relationship (bound):** the evidence-derived set is a narrower,
   evidence-oriented view; it is NOT the same collection as the broader
   Requirement Landscape.
4. **Section 14:** `validation_plan_source: requirement_landscape`;
   `validation_step_total + blocked_item_total == Section 13 total`.
5. Natural inventor-facing wording may vary, but these identifiers, meanings,
   and the relationship may not change without contract reopening. No
   unqualified shared `requirements` label for different sets; each defined
   set is internally consistent.

## 8. Leakage-test specification (semantic, field-aware)

1. **Prohibited Tokens (minimum):** `UNDETERMINED`, `system-derived`,
   `REASONED`, `ASSERTED`, `OWNER_EXECUTABLE`, `LEGACY_UNSPECIFIED`,
   `CONFIDENCE_UNDETERMINED`, `PROBLEM_MECHANISM_FIT`,
   `MECHANISM_COMPLETENESS`. A newly discovered raw token may be added to the
   pinned list automatically ONLY when it is an unambiguous syntactic
   equivalent of an already prohibited internal token (e.g. another raw
   gap-type enum, another `CONFIDENCE_*` constant); any semantic ambiguity is
   a STOP condition requiring owner review. Every addition is disclosed in
   the implementation report.
2. **JSON test:** recursive walk of the final package asserting no Prohibited
   Token appears as any field value or inside any generated string, outside
   the §8.3 exemptions; `stated`/`recorded` additionally prohibited as values
   of machine fields (`resolution_status`-class), while permitted inside
   ordinary prose.
3. **Verbatim exemptions (provable, enumerated):** an output value is exempt
   only when proven byte-derived from a specifically enumerated verbatim
   inventor-input field. The implementation report MUST contain the
   exhaustive list of exempt JSON paths (expected members include
   assertion/statement excerpts, acknowledged-unknown verbatims,
   Safety-Signal `statement` fields, and evidence-registry verbatim content —
   the final list is whatever the implementation proves, enumerated
   exhaustively). HTML exemptions must trace to those enumerated JSON paths
   or explicitly marked verbatim template regions.
4. **HTML test:** rendered deliverable contains no Prohibited Token outside
   content traced to §8.3 exemptions.

## 9. Design constraints

1. Boundary transformation lives in `engine/deliverable_assembler.py`: every
   exported non-verbatim enum/status/authority/provenance/confidence/
   responsibility/gap-type value is mapped to inventor-facing language at
   assembly; existing label maps reused where present (`_QUALITY_LABELS`,
   gap labels, §14 `*_label` precedent); new mappings added only where
   missing; exact prose implementation-chosen within the §4 inventor-facing-
   language definition (tests assert token absence plus the §7 identifiers,
   not replacement prose).
2. Internal dataclasses, vocabularies, and derivations unchanged; internal
   criticality stays `UNDETERMINED` (derivation is Workstream 4);
   `engine/requirement_landscape.py` and `engine/validation_plan.py` are
   **prohibited by default — any need to modify either requires contract
   reopening**.
3. Verbatim inventor text is never rewritten.
4. `_s6` prose corrected for BOTH `REASONED` and `ASSERTED` branches.
5. Test-first (BASE RED → HEAD GREEN per the WS2 evidence pattern);
   deterministic; no new dependency; no external NLP; bounded scanning only.
6. **Final Deliverable serialization contract — authorized changes (binding
   correction).** This Workstream is explicitly authorized to make the narrow
   inventor-facing Final Deliverable JSON serialization changes required by
   this contract, applying ONLY to the package produced by
   `engine/deliverable_assembler.py::assemble_deliverable` as the
   inventor-facing final deliverable:
   - removing raw internal enum/status/authority/provenance/confidence/
     responsibility/gap-type values from the inventor-facing package;
   - replacing those exported values with truthful inventor-facing
     representations;
   - adding the contract-bound `count_basis` fields;
   - adding `validation_plan_source`;
   - adding the machine-checkable Section 4 ↔ Section 13 relationship
     metadata;
   - adding or adjusting inventor-facing collection names and count metadata;
   - removing inventor-facing machine-status fields that have no valid
     inventor-facing representation.
   Every changed JSON path must be enumerated and mapped to an explicit
   contract requirement.
7. **Prohibited schemas and models (binding correction).** The following
   remain prohibited: `IdeaState` structure; internal engine dataclasses and
   enums; persistence and database schemas; session-state schemas; transcript
   schemas; scoring structures; internal assertion-ledger structure;
   Safety-Signal derivation structures; API contracts unrelated to the final
   deliverable; storage migrations; domain-model changes. If satisfying the
   contract requires changing any prohibited internal schema or model,
   implementation must STOP and request contract reopening.

## 10. RED-test requirements (each defect proven independently; must fail on the authoritative base)

New file `tests/test_deliverable_hygiene.py` (the ONLY test file authorized by
default), using the WS1 fixture journey (Flask test client):

**Defect 3 (independent):** (1) HTML token-absence; (2) JSON field-aware
token-absence; (3) a dedicated ASSERTED-quality fixture proving the `_s6`
ASSERTED prose path.

**Defect 4 (independent, narrowed to the binding owner count-scope
decision):** (4) §4 `total == len(evidence-derived collection)` with
`count_basis: evidence_derived_requirements`; (5) §13 `total ==
len(Requirement Landscape collection)` with `count_basis:
requirement_landscape`; (6) §14 `validation_step_total ==
len(validation_steps)`; (7) §14 `blocked_item_total == len(blocked_items)`;
(8) `validation_step_total + blocked_item_total == §13 total`; (9) each
§4/§13/§14 `count_basis` matches the exact collection counted.

**Guards (not RED):** (10) Safety-Signal semantic invariance + byte-identity
per §6; (11) WS1 evidence tree untouched.

Counts in other sections (§3, §5, §6, §8) are **regression observations
only**: recorded, compared base-vs-head, and any newly discovered defect
reported — NOT repaired without owner authorization.

## 11. GREEN acceptance

All §10 tests pass; §14 batteries pass; §15 comparison proves both defects
absent. **JSON criteria:** §8.2–8.3 satisfied; §7 identifiers present and
correct; no raw machine status values in machine fields; raw values
recoverable from internal objects only. **HTML criteria:** §13 renders
inventor-facing criticality/authority wording; §6 bullets contain no raw
quality token in either branch; no Prohibited Token outside traced verbatim
regions; the §7 set meanings and relationship are rendered in natural wording
consistent with the bound meanings.

## 12. Existing-test rule (owner Decision 5; binding clarification)

**Default: all existing tests remain unchanged.** Discovery that ANY existing
test must change is a STOP-and-report condition. An exception is possible only
per assertion, with: (1) exact path and assertion identified; (2) proof it
fails only because of the approved boundary transformation; (3) proof the
underlying internal value is unchanged; (4) a separately presented exact
test-diff proposal; (5) a NEW, SEPARATE owner authorization approving the
exact proposed assertion diff BEFORE editing.

Regarding `tests/test_safety_signal.py` specifically: the file remains
unchanged by default; all 18 tests must pass unchanged; a specific assertion
may change only after the STOP-and-report procedure above and a new, separate
owner authorization approving the exact proposed assertion diff; **the current
contract approval does not grant that authorization.** (Preferred resolution
if the gate is ever exercised: relocate/narrow the assertion to the internal
`derive_requirement_landscape` object rather than weaken it.) No broad edits
to Increment 4/5/6, Phase 7, Stage 3, deliverable, or safety test files are
pre-authorized.

## 13. Internal-state and traceability invariance

`IdeaState`, ledger, gap lifecycle, maturity, transitions, reason strings,
scoring, persistence, transcripts, session templates and session view
unchanged; internal objects continue to expose raw vocabulary to tests and
internal diagnostic evidence.

## 14. Regression gates

Focused new file; `tests/test_safety_signal.py` (18 tests, unchanged and
passing per §12) and `tests/test_safety_signal_stabilization.py` (15,
unchanged and passing); replay+adversarial (26 passed, 18 xpassed); WPS-001
(20 passed, 1 skipped); benchmark (27 passed, 6 xpassed); causal gate (177);
deliverable/landscape/validation suites unchanged and passing unless a §12
exception is separately owner-approved; full suite vs the comparative
baseline — no new failures, failures confined to
`tests/test_domain_registry.py`, base-vs-head diff recorded, known baseline
failures separately disclosed.

## 15. WS1 baseline comparison

Per `WS1_CLOSURE_COMPARISON_REQUIREMENTS.md`: byte-identical journey inputs;
quote-level proof that manifest row-3 quotes and the row-4 totals mismatch are
absent at head; and **every base-to-head JSON and HTML delta enumerated by
JSON path or rendered section and mapped to an explicit contract requirement**
(hygiene mapping §8/§9, count semantics §7, or nothing else);
prohibited-regression checks.

## 16. F3 — loud-failure harness

The copied harness must prove: non-zero exit; explicit `JOURNEY INCOMPLETE`
message; **no new artifact written; no existing artifact modified** on an
incomplete journey.

## 17. F4 — evidence confinement

Prove the WS1 AND WS2 evidence trees are byte-identical before and after
Workstream 3, and that all WS3 outputs are confined to
`docs/governance/evidence/workstream3_deliverable_hygiene/`; the harness is a
COPY (the WS1 harness is never edited).

## 18. Journey requirements

Regenerate BOTH the false-negative and positive journeys with byte-identical
inputs, plus the §10.3 ASSERTED-path fixture.

## 19. Expected WS3 evidence directory contents

Copied harness; BASE RED outputs; HEAD GREEN outputs; regenerated
inventor-facing deliverable JSON+HTML for both journeys (hygiene-conformant);
**separately labeled internal diagnostic evidence** (machine-readable
token-scan results, machine-readable count-basis/relationship comparison,
internal-object dumps as needed); Safety-Signal invariance comparison; WS1 and
WS2 evidence-tree identity proofs; command/environment record; F3 proof; F4
proof; focused+full regression outputs; known-failure disclosure;
identity/hash records (WS2 pattern); the exhaustive exempt-JSON-path list
(§8.3).

## 20. Independent review

Read-only implementation review (code + tests + evidence + hashes + any
§12-approved test diff) before any merge authorization; correction rounds
re-reviewed.

## 21. Stop conditions (non-waivable)

Any Safety-Signal semantic delta, or any hygiene change that would require
modifying the WS2 block (§6.4); any needed change to ANY existing test before
its enumerated diff is separately owner-approved (§12); any needed change to
`engine/requirement_landscape.py` or `engine/validation_plan.py` (contract
reopening); any needed change to a §9.7 prohibited schema or model (contract
reopening); any raw field removed by this contract that an existing consumer
outside the final deliverable rendering/export path requires (STOP and report
the exact consumer); any needed change to `engine/progression_loop.py`,
`engine/safety_signal.py`, `engine/idea_state.py`, persistence, or session
surfaces; any semantically ambiguous token-list addition (§8.1); any
scoring/replay/WPS/benchmark/gate delta; any WS1/WS2 evidence mutation; a
newly discovered count defect outside §7's scope (report, do not repair); any
raw value unmappable without semantic loss; any term unmeetable as written →
STOP, report, await new owner review.

## 22. Explicit exclusions

Criticality derivation (WS4); risk/landscape synthesis quality (WS5/6);
validation-plan content quality (WS7); general copy editing; session-view
text; journey/question changes; unknown extraction; counts outside §7
(observed only); §9.7 prohibited schemas and models; AI Coach; `main` sync;
PR #167/#162. (For clarity: the §9.6 Final Deliverable serialization changes
are authorized and are NOT excluded by any use of the word "schema" in this
contract.)

## 23. Closure criteria

Plan §12 items (1, 2, 5, 6 directly; 3–4 as regenerated-deliverable
defect-absence for Defects 3–4) + §§10–20 of this contract + explicit owner
closure authorization + §15-table/roadmap synchronization.

## 24. Lifecycle after approval

Record contract (docs-only Draft PR) → owner recording review/merge → status
canonicalization → separate implementation authorization citing the approved
identity (recording/merge commit SHA + contract blob SHA) verbatim → BASE RED
→ implementation → HEAD GREEN → evidence → independent review → owner merge →
post-merge verification → closure + §15-table/roadmap sync. Status-only
lifecycle-log updates per the WS2 §2.4 precedent; substantive changes require
a new owner contract review.

---

## Appendix A — File-scope matrix (approved)

| Category | Files |
|---|---|
| Likely | `engine/deliverable_assembler.py`; `web/templates/deliverable.html`; new `tests/test_deliverable_hygiene.py`; new `docs/governance/evidence/workstream3_deliverable_hygiene/` (evidence stage) |
| Conditional — per-assertion, separately owner-approved diff required first (§12) | the single §13-criticality assertion in `tests/test_safety_signal.py`; any individually enumerated raw-serialization assertion in other existing test files |
| Prohibited by default — contract reopening required | `engine/requirement_landscape.py`; `engine/validation_plan.py` |
| Prohibited | `engine/progression_loop.py`; `engine/safety_signal.py`; `engine/idea_state.py`; §9.7 prohibited schemas and models (persistence, session-state, transcript, scoring, ledger, Safety-Signal derivation structures, storage migrations, domain models, unrelated API contracts); session transcripts/templates; WS1 evidence; WS2 contract+evidence; WPS-001; benchmark; MVP scope; AI Coach |

## Appendix B — RED/GREEN and evidence matrix (approved)

| Check | RED on base? | Defect | Evidence artifact |
|---|---|---|---|
| HTML token absence | yes | 3 | token scan (diagnostic) + regenerated HTML |
| JSON field-aware token absence + exempt-path list | yes | 3 | token scan + exhaustive exempt-path list |
| ASSERTED prose path | yes | 3 | dedicated fixture output |
| §4 total == len + `evidence_derived_requirements` | yes (basis absent) | 4 | count-basis comparison |
| §13 total == len + `requirement_landscape` | yes (basis absent) | 4 | count-basis comparison |
| §14 step/blocked totals == len | yes (fields absent) | 4 | count-basis comparison |
| §14 steps+blocked == §13 total (declared tie) | yes (declaration absent) | 4 | count-basis comparison |
| Safety-Signal semantic invariance + byte-identity | guard | — | invariance comparison |
| WS1 + WS2 tree identity (before/after) | guard | — | tree-identity proofs |
| Other-section counts | observation only | — | base-vs-head observation record |
| F3 (no new artifact, no modified artifact) / F4 (confinement) | guard | — | loud-failure + confinement proofs |
| Batteries / full regression | guard | — | outputs + known-failure disclosure |

## Appendix C — Ambiguity statement (approved)

No ambiguity remains that prevents this contract from being fully testable.
All previously deferred decisions (set names/relationship, surface scope,
exemption rules, test-modification policy, serialization-vs-schema
distinction) are bound in this contract; the only implementation freedom left
is non-contractual prose wording, which tests deliberately do not pin.

---

*This contract authorizes no implementation, no test edit, no evidence
generation, no status-table or roadmap change. Repository recording and
implementation remain separate owner-gated actions; implementation must cite
this contract's approved identity (recording/merge commit SHA + contract blob
SHA) verbatim.*
