# WS4_TRACEABILITY — RED→GREEN and journey-test traceability

## 1. R1–R8: the exact implementation behavior that turned each GREEN

| RED test | Contract | Implementation behavior that turned it GREEN |
|---|---|---|
| R1 `confirmation_history_exists` | §6.1 | `IdeaState.criticality_confirmations: list = field(default_factory=list)` — session-bounded, append-only, seeded empty (`engine/idea_state.py`, commit `df4836bf`) |
| R2 `guarded_recorder_records_owner_confirmation` | §6.3 + §6.1 | `IdeaState.record_criticality_confirmation(...)` appends one frozen `CriticalityConfirmation` carrying the §6.1 fields — byte-verbatim rationale, `reused_statement:<rec_N>` attribution, `provenance="owner_confirmed"` |
| R3 `recorder_rejects_confirmed_undetermined` | §4 clarification / §6.3 | recorder guard: `confirmed` requires `category ∈ {FEASIBILITY-THREATENING, VALUE-ENHANCING, REFINEMENT}` — `UNDETERMINED` (and anything else) raises `ValueError`, nothing stored |
| R4 `recorder_rejects_missing_rationale` | §6.3 | recorder guard: `confirmed` without a non-empty `rationale_verbatim` (or with an invalid `rationale_source`) raises, nothing stored |
| R5 `confirmed_category_reaches_section13_json` | §11(4) / §12 / §4 | `_CRITICALITY_PUBLIC` gains "Essential to feasibility" / "Important to value" / "Refinement or improvement"; `_CRITICALITY_AUTHORITY_PUBLIC` gains `owner-confirmed → "Confirmed by the inventor"`; `_s13` passes the rationale through verbatim (`engine/deliverable_assembler.py`) |
| R6 `confirmed_category_reaches_rendered_html` | §11(4) / §8 | no template change needed — the pre-existing dormant rationale line (`web/templates/deliverable.html:203-205`) renders the mapped §13 values |
| R7 `explicit_deferral_representable` | §11(5) / §4 | `derive_requirement_landscape` applies the §16.1 three-state model from the current lookup: deferred → `UNDETERMINED` / `undetermined` / no rationale → "Confirmation not yet available" (`engine/requirement_landscape.py`) |
| R8 `history_append_only_latest_governs` | §6.1–§6.2 | latest-per-`requirement_id` lookup over the append-ordered history; earlier records retained; `dataclasses.replace` applies only the latest action |

## 2. G1–G5: the user-facing behavior each journey test proves

| GREEN test | Proves |
|---|---|
| G1 `summary_first_surface_five_actions_clean_vocabulary` | the completed real WS1 journey presents the summary-first block ("This is what I understood from your explanation:", the inventor's own recorded words) with ALL FIVE owner-mandated lightweight actions byte-exact — and exposes **no raw category/authority/requirement-id token and no §7.9 banned governance phrase** |
| G2 `accept_flow_end_to_end_no_adoption_before_acceptance` | **explicit confirmation**: one supportive clarification ("Would the idea still achieve its purpose if this part changed?") with the four exact plain-language choices; **no silent classification / no state adoption before explicit acceptance** (derivation asserted unchanged mid-flow); **zero-retype rationale reuse** (prefilled verbatim statement accepted as displayed → `reused_statement:rec_N`); public JSON/HTML wordings byte-exact end-to-end |
| G3 `correction_and_missing_paths_store_nothing` | **explicit correction** and the **missing-information path**: "Change this part" / "Something is missing" store no confirmation and return the inventor to the existing free-text answer path on the same journey |
| G4 `uncertainty_and_deferral_zero_delta` | **uncertainty** ("I am not sure yet") and **deferral** ("Decide later") each record one explicit deferred action with **zero side effects**: maturity, scoring, gaps, transitions, iteration, direction, ledger, acknowledged unknowns, last result, and every unrelated deliverable section proven unchanged before/after |
| G5 `manipulated_or_stale_posts_rejected` | **manipulated/stale rejection**: wrong focus token, unknown action, clarify-without-summary, manipulated `UNDETERMINED` category (route-level confirmed+UNDETERMINED analogue), and emptied rationale — all HTTP 400 with nothing stored |

Additional standing coverage: P1–P5 keep proving no silent classification
from free text, verbatim preservation, never-interacted public wordings,
render-without-accepting purity, and token hygiene; R8 proves **append-only
history with the latest explicit action governing**.

## 3. Suite finality

`python -m pytest tests/test_structured_criticality.py -v` at HEAD GREEN:
**18 passed — zero failed, ZERO SKIPPED, ZERO XFAILED** (raw output in
WS4_TEST_RECORD.md §1). The owner F1 gate — no surviving skip or xfail —
is met.
