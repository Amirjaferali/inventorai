# WS5_PROTECTED_BEHAVIOR — protected-behavior verification at HEAD GREEN

Verified at `97b6725953150509059dd41ba623e438f939f094` (raw outputs in
WS5_RED_GREEN_TEST_RECORD.md; artifact byte evidence in this directory):

1. **Safety-signal fields unchanged** — `engine/safety_signal.py` is
   byte-identical to the base; the rendered block equals the direct
   derivation field-by-field (test P1); `tests/test_safety_signal.py` 18 and
   `tests/test_safety_signal_stabilization.py` 15 pass (negation
   suppression, attribution guards, harmful-continuation/benign-failover
   semantics, sentence bounding, exact dedup all intact).
2. **Section 6 rows/totals unchanged** — identical rows BASE vs HEAD per
   case (artifacts); totals machine-compared in `ws5_json_html_parity.json`;
   test P2.
3. **Section 13 disclaimer byte-identical** — test P3 against the frozen
   constant; present verbatim in every artifact.
4. **No Section 13 key added** — the §13 exact-key-set pin
   (`tests/test_phase_7c_requirement_landscape_collapse.py:129`) passes.
5. **No new top-level section** — the top-level package key-set pins
   (evidence-registry / unknown-registry / increment-6 suites) pass; the
   linkage block is nested under `_session_meta` (committed additive-nesting
   precedent).
6. **No signal grouping or hiding** — owner decision D4: rendering is
   unchanged (tests P6/R6); no `<details>`, collapsing, suppression, or
   abbreviation exists in the template diff.
7. **No new inventor question** — no route, form, or session-page change;
   `web/app.py` and `web/templates/session.html` byte-identical to base.
8. **No persistence or schema change** — no persistence path touched; the
   in-memory state model (`engine/idea_state.py`) byte-identical to base.
9. **Machine-status hiding and public wordings** — hygiene 22 passes
   unmodified; Workstream 4 structured-criticality 18 and requirement
   landscape 39 pass (criticality surfaces untouched).
10. **Frozen lanes** — Answer Clarification inactive, AI Coach prohibited,
    persistence frozen, electronics/electrical-only scope: no change of any
    kind in the diff; PR #167 and PR #162 untouched.
