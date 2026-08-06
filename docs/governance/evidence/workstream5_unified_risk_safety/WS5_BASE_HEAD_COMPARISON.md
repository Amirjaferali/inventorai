# WS5_BASE_HEAD_COMPARISON — defect at BASE, behavior at HEAD

## 1. The exact defect at BASE (plan §3.B defect 10)

At the RED commit (product surface byte-identical to the canonical base
`3bf67da0…`), one deliverable simultaneously communicated, with zero
cross-references: (a) "What could go wrong" showing only system-derived
process risks — on the WS1 journey a single `[low]` evidence-quality row,
with the inventor's stated fire/danger consequences appearing nowhere in the
section; (b) the Inventor-Stated Safety Signals block listing those stated
consequences; (c) the Section 13 disclaimer "No structurally grounded risks
are recorded…". Each statement was individually truthful; the presentation
was disconnected and could understate stated danger or read as
contradiction (compare `base_ws1_safety_deliverable.*` with the head
artifacts).

## 2. The exact RED failures

R1–R5 at `3cef5eb7` (raw output in WS5_RED_GREEN_TEST_RECORD.md §1): the
`_session_meta.risk_safety_linkage` object absent; the Section 6 linkage
note absent; the low process-risk row unreconciled with stated
consequences; the Section 13 adjacent note absent; the bare
"No risks recorded." rendering beside populated signals on the
mature/gap-free fixture; the disconnection present in BOTH JSON and HTML.

## 3. The exact GREEN behavior

At `97b67259`: `_session_meta.risk_safety_linkage` carries state facts
(signals_present, signal_total, Section 6 totals by severity,
section_13_has_structural_risks, acknowledged_unknown_count) plus the three
owner-approved D2 wordings byte-exact — `section_6_note` and
`section_13_note` whenever signals exist; `section_6_empty_qualification`
only when signals exist and Section 6 has zero rows; all three `None` in
the no-signal state. The template renders exactly these package values:
the Section 6 note inside "What could go wrong", the qualification
replacing the bare empty message only in the signal-bearing case, and the
contextual note adjacent to the unchanged frozen Section 13 disclaimer.

## 4. Preservation proofs

- **Section 6 rows:** byte-comparison of `base_ws1_safety_deliverable.json`
  vs `head_ws1_safety_deliverable.json` shows the identical single `[low]`
  evidence-quality row (`section_6_risks` totals and rows unchanged);
  machine-asserted by tests P2/G3/G4.
- **Section 13 disclaimer:** byte-identical in every artifact and pinned by
  test P3 against the frozen constant; `section_13_requirement_landscape`
  gained no key (its exact key set is separately pinned by the committed
  `tests/test_phase_7c_requirement_landscape_collapse.py:129`).
- **Safety-signal records:** all eleven per-signal fields equal the direct
  engine derivation (test P1); statements render byte-identically (P6/R6);
  signal counts identical BASE vs HEAD per case.
- **No risk creation / severity inference / signal promotion:** the linkage
  synthesizer emits only counts and fixed constants read from the assembled
  package; Section 13 `risks` remains `[]` everywhere; the mature/gap-free
  HEAD artifact still shows zero Section 6 rows (test P4); the wordings
  state explicitly that signals are "not confirmed risks" / "not structural
  risk records".
- **JSON/HTML parity:** machine-generated record `ws5_json_html_parity.json`
  (three cases × three wording fields + six totals each; every check
  hard-asserted by the harness) plus tests G3/G4/G5.
- **No-signal behavior:** `head_no_signal_deliverable.*` is rendered without
  any Workstream 5 wording; the linkage block records
  `signals_present: false` with every wording field `null`; the existing
  bare disclaimers are unchanged.

## 5. Inventor-stated vs system-derived separation

Inventor-stated facts (verbatim signal statements, provenance
`inventor_stated`) remain labeled and separate from system-derived values
(Section 6 process rows, structural-risk state); no inventor statement is
described as a confirmed risk anywhere in JSON, HTML, or this evidence.
