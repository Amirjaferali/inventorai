# R1 Engineering Acceptance Record — R1-ENGINEERING-ACCEPTANCE-PROOF-01

Recorded 2026-10-14. Base `c8b6d36e14636231f1a73de8bf2be0942a3162fc` (branch
`feature/atomic-json-session-persistence`). Owner-authorized, tests and evidence only.

**Applicability.** This record takes effect only on the verified merge of its PR into
`feature/atomic-json-session-persistence`. On the proposal branch it is a candidate.

## Scope and boundary

It records first-release acceptance results against the Owner-approved criteria for exactly
three delivered, bounded R1 engineering scopes of roadmap §8D:

- Mechanical;
- Electrical / Electronics;
- the Stage-15 integrated invention.

It closes §8D unresolved item (3) for these three rows only. The other R1 rows — Stage 17
capture and the exports as R1 rows of their own — keep open acceptance criteria.

It is **not**:

- a release-ready declaration;
- product acceptance;
- a Stage closure;
- deployment evidence;
- an engineering-validity claim about any invention.

A PASS means the delivered capability behaved as its contract states, on synthetic data,
through the real routes, engine and store. R2 depth stays unauthorized.

No product, runtime, template, persistence, calculation, source or contract file changed.

## Evidence added by this increment

Only the genuine coverage gaps found by mapping the criteria to existing tests got new tests.
Every other criterion reuses accepted evidence.

### `tests/test_r1_engineering_acceptance.py` — three joined journeys

These run through the real web routes, engine and store. The guidance gaps they check are the
gaps the inventor's own answers left open; none is injected.

- **`test_a_mechanical_r1_journey`**
  - The governed Mechanical questions on a new routing-aware project. PF:Q2 is never served, and
    the journey ends with PHYSICAL_FEASIBILITY PARTIAL and routed to a specialist.
  - The report and PDF, in EN and AR, explain exactly that gap: its context, the next steps and
    the force / moment / pressure fundamentals.
  - CAP-12 is reached from the session page, and CAP-13 gives 750.0 N / 250.0 N, UNVALIDATED,
    with the disclosure, then a refusal with no number.
  - Reading all of this wrote nothing.
  - Explicit risk acceptance reaches Level 2 while the specialist routing stays outstanding.
- **`test_b_electronics_r1_journey`**
  - The open mechanism gap with its three reference groups (sensing, accuracy / resolution,
    controller), in the report and PDF.
  - The governed Electronics questions (`N-MC` / `N-PF` / `N-BA`) through to the governed exit
    prompts, then the partial feasibility gap with the basic, energy-time and charge groups, in
    the report, PDF and AR report.
  - THERM-01 gives 25.0 K, UNVALIDATED, with the disclosure, then a screen-YES abstention.
  - Nothing is written.
  - Explicit risk acceptance closes the journey at Level 2.
- **`test_c_integrated_r1_journey`**
  - A three-part composition (with the optional control-loop part), then:
    - one component linked to both required parts, and one interface;
    - all three preparation inputs, a one-way dependency and one observation, each confirmed in
      the durable store;
    - one non-focused part answer.
  - CAP-13 and THERM-01 each name their own declared part.
  - The Parts, Components & Interactions view shows it all.
  - The report and PDF carry:
    - the three-part scope disclosure;
    - the component, the interface and the preparation;
    - the non-focused answer.
  - The observation stays out of the report.
  - The route-level Stage 35 Disclosure Export carries the three parts, the interface with its
    dependency and its two part references, and the component with its references.
  - Calculations, the view, the report, the PDF and the export wrote nothing.

### `tests/test_r1_engineering_acceptance_browser.py` — real Chromium

EN and AR, checked at 390 px and 1280 px for overflow, `lang` and RTL.

- **`test_mechanical_report_and_cap12_advisory`:**
  - the Mechanical questions answered in the browser;
  - the report's routed feasibility guidance;
  - CAP-12 opened from the session-page link and returning its alternatives.
- **`test_three_part_invention_interface_and_preparation`:**
  - the three-part composition form;
  - interface declaration through the session form, with three offered pairs;
  - preparation saved through its page;
  - the Parts, Components & Interactions view.

## Acceptance matrix

| # | Criterion (Owner-approved) | Evidence | Result |
|---|---|---|---|
| A1 | Mechanical question journey, respecting routing and specialist redirection | new `test_a…`, browser `test_mechanical…`; reused `test_safe_question_routing_pf_q2.py` (`test_19`, `test_01b`, `test_07d`), `…_weak_recovery.py::test_04` | PASS |
| A2 | OPEN / PARTIAL gap context and technical next steps in report / PDF | new `test_a…` (EN / AR, report + PDF), browser `test_mechanical…`; reused `test_cap01_mechanical_open_gap_context.py` (`test_15`–`17`, `f26`–`f31`), `test_stage18_gap_next_steps_closure.py` (`n80`–`n82`) | PASS |
| A3 | CAP-12 advisory accessible | new `test_a…`, browser `test_mechanical…`; reused `test_cap12_form_mockup_advisory.py` | PASS |
| A4 | CAP-13 within its contract: reactions or refusal / abstention | new `test_a…`; reused `test_cap13_static_reactions.py` (route, engine, refusal, abstention), `…_browser.py` | PASS |
| A5 | Explicit `UNVALIDATED`; no adequacy / safety claim | new `test_a…`; reused `test_cap13_static_reactions.py::test_every_cap13_string_is_bilingual_and_carries_no_verdict_wording`, `::test_no_safety_signal_report_export_or_api_surface` | PASS |
| B1 | Electrical / Electronics question journey | new `test_b…` | PASS |
| B2 | Gap guidance and reference fundamentals in their contracted surfaces | new `test_b…` (report + PDF + AR); reused the six `test_cap01_*_reference*` suites with their browser files, `test_stage18_*` | PASS |
| B3 | THERM-01 single-path calculation or its refusal / abstention | new `test_b…`; reused `test_therm01_temperature_difference.py`, `…_browser.py` | PASS |
| B4 | `UNVALIDATED` and applicability disclosures; no safety / rating / adequacy claim | new `test_b…`; reused `test_therm01_temperature_difference.py` (`…section_9…`, `…no_verdict_wording`, `…no_safety_signal…`) | PASS |
| C1 | Mechanical + Electrical / Electronics composition, with the optional `control_loop` part | new `test_c…`, browser `test_three_part…`; reused `test_stage15_integrated_invention_entry.py`, `test_stage28_control_loop_optional_part_slice1.py` | PASS |
| C2 | Declare and inspect parts, components and interfaces | new `test_c…`, browser `test_three_part…`; reused `test_component_inventory_*`, `test_stage15_subsystem_interface_declaration.py`, `test_stage15_parts_components_interactions_view*.py` | PASS |
| C3 | Interface verification preparation and observations | new `test_c…`, browser `test_three_part…` (preparation); reused `test_stage15_interface_preparation.py`, `test_stage15_interface_observations.py`, `test_stage15_observation_withdraw_browser.py` (observations in a browser) | PASS |
| C4 | Admitted calculations for their corresponding declared parts | new `test_c…`; reused `test_cap13_therm01_integrated_part_eligibility.py` (both focus directions, fail-closed cases), `…_browser.py` | PASS |
| C5 | Integrated views, report / PDF and Disclosure Export within their contracts | new `test_c…`; reused `test_28t5_nonfocused_part_report*.py`, `test_component_deliverable_value.py`, `test_stage35_component_disclosure_export.py`, `test_stage35_disclosure_projection.py` | PASS |
| X1 | EN / AR presentation correct | new journeys (AR report / PDF), both browser tests; per-capability AR suites above | PASS |
| X2 | User-facing journeys readable at 390 px and 1280 px | both new browser tests; the per-capability browser files above | PASS |
| X3 | Canonical data and technical meaning unchanged | no product file changed; reused contract-wording tests | PASS |
| X4 | No result promoted to validated evidence | new journeys (UNVALIDATED; no writes from calculations, reports or exports); reused CAP-13 / THERM-01 no-surface tests | PASS |
| X5 | No invented engineering, safety or compatibility conclusions | reused wording guards: CAP-13 and THERM-01 `…no_verdict_wording`, CAP-12 `test_no_ranking_or_best_wording_in_any_cap12_copy` and `test_the_advisory_names_no_grade_number_or_specific_polymer`, Parts view `test_b01_no_calculation_offer_or_engineering_conclusion` | PASS |
| X6 | No unauthorized persistence, progression, readiness or export effects | new journeys (database and engine state unchanged across reads, calculations and exports); reused per-capability no-effect tests | PASS |

**FAIL: none. NOT VERIFIED: none.**

## Limitations and exclusions (material)

- **Journey ending.** "The question journey" means the domain pack's governed questions and its
  existing exits.
  - Mechanical ends with feasibility routed to a specialist and PARTIAL.
  - On Electronics, the synthetic answers did not close feasibility or boundary. The governed
    exhausted-question exit and explicit risk acceptance were used. That is the supported path,
    and the quality of answers is not graded.
  - The general Stage-3 questions after Level 2 are outside these R1 engineering scopes and were
    not asserted.
- **Deliberate exclusions, not shortfalls:**
  - CAP-13 / THERM-01 results are session-only. They are not saved and are absent from the
    report, PDF and export.
  - Interface observations and integration evidence are absent from the report.
  - The CAP-12 advisory is session-only.
- **Integrated coverage split.** The joined integrated journey uses the Mechanical focus. The
  Electronics focus direction is covered by the reused eligibility, Parts-view and report suites.
- **Arabic CAP-01 sentences.** English canonical technical statements inside the Arabic report
  follow the Owner language policy. Their Arabic rendering is not a subject of this record.
- **Representative, not complete.** The synthetic inventions are representative only and prove
  no technical coverage beyond the bounded delivered scopes. The T1-C′ study corpus was not used.
- **Not evidence of the live service.** Results are from the local environment (author run) and
  the hosted required CI of the PR. They say nothing about the deployed service, which runs an
  older build.

## Addendum — R1-ACCEPTANCE-COMPLETION-01 (recorded 2026-10-14)

Recorded 2026-10-14 on base `0f1b3d1c9abb3e95cb0a4b84391cd896b11faf38`. Documentation only:
no product, runtime, template, persistence, test or contract file changed, and no new test was
added. **Applicability.** This addendum takes effect only on the verified merge of its PR into
`feature/atomic-json-session-persistence`; on the proposal branch it is a candidate.

It is separately scoped and dated. It does not change the record above: PR #814's acceptance of
Mechanical, Electrical / Electronics and the Stage-15 integrated invention, its criteria A1–C5
and X1–X6, and its results stand exactly as recorded. It is not a release-ready declaration,
product acceptance, a Stage closure, deployment evidence or an engineering-, commercial- or
legal-validity claim.

The cited tests are existing, accepted tests. All of them passed in the hosted required CI of
the tree this addendum is based on (FULL route, run 38638103997, head
`3a2ab3d867259ba46b12ad1674ce7a9a65e12484`, whose tree is the base tree).

### Part 1 — `control_loop` part-only: Owner-accepted criteria P1–P6

**Owner acceptance: GRANTED 2026-10-14**, for the PART-ONLY scope only: `control_loop` as the
ONE optional part of a Mechanical + Electrical / Electronics integrated invention. Root
activation stays UNAUTHORIZED; its qualification-record blockers and its R3 class are
unchanged. This is not acceptance of full Control Systems.

| # | Criterion (Owner-accepted) | Existing evidence | Result |
|---|---|---|---|
| P1 | Part-only eligibility, distinct from root activation, with truthful three-part disclosure to the inventor | `test_stage28_control_loop_optional_part_slice1.py`: `test_the_part_only_allowlist_enables_exactly_control_loop`, `test_part_eligibility_is_distinct_from_root_activation`, `test_three_part_scope_shows_the_optional_part_with_truthful_copy`; `test_r1_engineering_acceptance.py::test_c_integrated_r1_journey` (three-part scope statement in report and PDF) | ACCEPTED |
| P2 | Durable optional-part identity inside the integrated invention; never the analysis focus | slice 1: `test_three_part_composition_round_trips_through_the_existing_table`, `test_cold_load_and_reconstruction_restore_the_three_parts`, `test_the_store_never_accepts_the_optional_part_as_the_focus`; `test_c_integrated_r1_journey` (store, view, report, PDF, Disclosure Export) | ACCEPTED |
| P3 | No standalone or root activation | slice 1: `test_root_activation_is_unchanged_and_control_loop_is_not_root_activated`, `test_a_single_control_loop_result_is_never_root_admission_nor_composes_when_withdrawn`; `test_stage28_control_loop_optional_part_slice2.py::test_control_loop_is_part_enabled_but_never_root_activated`; `test_stage28_control_loop_qualification_slice1.py::test_recognized_not_activated_refusal_stays_truthful` | ACCEPTED |
| P4 | No feasibility, safety or specialist conclusion: MECHANISM_COMPLETENESS and BOUNDARY_AMBIGUITY only; part answers outside gaps, progression, readiness and SafetySignal derivation, with that exclusion disclosed | slice 2: `test_only_mechanism_completeness_and_boundary_ambiguity_are_part_question_families`, `test_part_answers_touch_no_root_gap_progression_or_other_table`, `test_report_pdf_export_readiness_and_session_carry_no_part_answer`, `test_root_owners_never_read_part_answers`; `test_stage30_control_loop_part_safeguards_slice1.py`: `test_safety_signal_owner_holds_no_part_answer_read_path`, `test_part_page_discloses_the_safety_input_scope_editable_and_read_only`, `test_report_and_pdf_disclose_the_scope_only_for_projects_with_an_optional_part` | ACCEPTED |
| P5 | Correct existing EN / AR behaviour | `test_every_new_copy_key_has_english_and_arabic` (slice 1 and the Stage 30 suite); slice 2: `test_arabic_page_keeps_governed_text_verbatim_and_says_so`; `test_r1_engineering_acceptance_browser.py::test_three_part_invention_interface_and_preparation` (three-part form, EN / AR, 390 px and 1280 px) | ACCEPTED |
| P6 | Saved part answers readable and read-only if part eligibility is withdrawn | Stage 30 suite: `test_saved_answers_stay_readable_read_only_after_withdrawal`, `test_writes_are_refused_after_withdrawal`, `test_no_new_control_loop_part_can_be_created_after_withdrawal` | ACCEPTED |

**Optional, non-blocking limitation (preserved).** No real-browser test opens the `control_loop`
part-question page itself. That page is rendered by the same template and renderer
(`part_questions.html`, `_render_part_questions`) as the non-focused required-part page, which
`test_28t5_nonfocused_required_part_questions_browser.py` drives in EN / AR at 390 px and
1280 px; its Arabic content and disclosure are proven server-side. A dedicated browser check
stays optional and is not part of the accepted criteria.

### Part 2 — the other R1 rows: evidence mapping, Owner acceptance PENDING

The criteria below are PROPOSED, each stated within the row's delivered, bounded contract.
Every one maps to existing evidence and reads **EVIDENCED**. **They are NOT accepted:** Owner
acceptance stays open for these rows, as roadmap §8D records. Recording evidence is not
acceptance, not a validated commercial or manufacturing conclusion and not legal clearance.

**Manual supplier evidence and Stage-17 commercial evidence capture**
(`engine/commercial_evidence.py`, the shared evidence owner)

| # | Proposed criterion | Existing evidence | Result |
|---|---|---|---|
| S1 | The owner records commercial evidence in the closed 15-topic vocabulary; it is durable and an exact retry adds nothing | `test_commercial_evidence_capture.py`: `test_the_owner_can_record_commercial_evidence`, `test_recorded_evidence_survives_a_reload`, `test_an_identical_retry_does_not_create_a_duplicate`, `test_the_form_offers_exactly_the_closed_topic_vocabulary`; `test_commercial_evidence_owner.py::test_the_commercial_topic_vocabulary_is_exactly_the_authorized_set` | EVIDENCED |
| S2 | Manual supplier evidence: a supplier item is recordable in the manufacturing lane, and a quantified commercial item can name "A supplier quote" as its basis; a quantity without a documented basis is refused | `test_manufacturing_evidence_owner.py`: `test_the_manufacturing_vocabulary_is_exactly_the_authorized_set` (the `supplier` topic), `test_no_manufacturing_conclusion_is_implied` (records a `supplier` item), `test_manufacturing_evidence_persists_in_the_shared_table`; `test_commercial_evidence_capture.py`: `test_an_exact_amount_is_stored_as_one_truthful_value` (`supplier_quote` basis), `test_a_quantity_without_a_documented_basis_is_refused` | EVIDENCED |
| S3 | Owner-stated and unvalidated only; no readiness, marketability, manufacturability or supplier-readiness conclusion; the Readiness Snapshot stays at insufficient evidence | capture: `test_provenance_is_forced_and_is_not_a_control`, `test_claim_status_is_forced_and_is_not_a_control`, `test_no_readiness_conclusion_is_computed_anywhere_in_this_lane`, `test_no_marketability_or_profitability_claim_appears`; owner: `test_recording_a_statement_produces_no_commercial_conclusion`; manufacturing owner: `test_no_manufacturing_conclusion_is_implied`, `test_no_cad_pcb_bom_or_supplier_functionality_appears`; `test_manufacturing_readiness_snapshot.py`: `test_all_ten_topics_are_still_insufficient_evidence`, `test_positive_dispositions_are_structurally_unreachable` | EVIDENCED |
| S4 | Append-only correction and withdrawal; history kept | capture: `test_a_correction_appends_and_never_mutates_the_old_row`, `test_a_withdrawal_preserves_history_and_empties_the_active_view`; owner: `test_supersession_and_withdrawal_keep_every_earlier_row`, `test_no_update_statement_exists_for_this_table` | EVIDENCED |
| S5 | Owner-only writes; project isolation; CSRF | capture: `test_an_unauthenticated_request_cannot_write`, `test_another_account_cannot_write_to_this_project`, `test_projects_are_isolated`, `test_csrf_is_enforced`; manufacturing owner: `test_cross_account_write_and_read_are_refused` | EVIDENCED |
| S6 | EN / AR presentation | capture: `test_english_labels_render`, `test_arabic_labels_render_and_user_text_is_rtl_safe`, `test_every_topic_has_both_languages`; manufacturing owner: `test_arabic_labels_render_and_text_is_direction_safe`, `test_every_manufacturing_string_has_both_languages` | EVIDENCED |

Limitation: no real-browser test drives the capture forms; the EN / AR evidence is server-side.
Automated supplier discovery stays outside this row (R2), and procurement / ordering stays
excluded (R4).

**P7 Structured Export** (`engine/read_export_service.py`, `web/api_v1.py`,
`engine/export_adapter.py`)

| # | Proposed criterion | Existing evidence | Result |
|---|---|---|---|
| E1 | An authorized read and Structured Export from the durable contract, grounded and deterministic | `test_p7_i1_read_export_service.py`: `test_authorized_project_read_returns_durable_contract`, `test_authorized_structured_export_produced`, `test_export_record_content_grounded_no_invented_data`, `test_export_is_deterministic`; `test_p7_i2_public_api.py::test_authorized_structured_export_succeeds` | EVIDENCED |
| E2 | Every unauthorized request is denied, and cross-owner and missing projects are indistinguishable | i1: `test_cross_owner_read_denied`, `test_export_denials_mirror_read`; i2: `test_no_credential_denied`, `test_revoked_credential_denied`, `test_expired_credential_denied`, `test_insufficient_scope_denied`, `test_browser_session_alone_does_not_authenticate_api`, `test_cross_owner_and_missing_project_indistinguishable` | EVIDENCED |
| E3 | Read-only: no mutation and no write method | i1: `test_read_does_not_mutate_governed_state`, `test_export_does_not_mutate_governed_state`; i2: `test_no_write_methods_on_api_routes`, `test_public_reads_do_not_mutate_project_state` | EVIDENCED |
| E4 | No domain activation or inferred support state | i1: `test_export_does_not_activate_domain_or_mutate_registry`, `test_export_domain_support_state_grounded` | EVIDENCED |
| E5 | Credential and abuse controls | i2: `test_secret_stored_hash_only`, `test_secret_not_leaked_in_logs_or_responses`, `test_audit_event_recorded_for_served_and_denied`, `test_audit_write_failure_fails_closed`, `test_authenticated_api_read_limiter_enforced`, `test_rate_limit_store_failure_fails_closed` | EVIDENCED |
| E6 | The adapter keeps the mandatory fields, fails closed and makes no network call | `test_p7_i3_export_adapter.py`: `test_mandatory_preservation_floor_survives`, `test_changed_mandatory_field_fails`, `test_adapter_module_is_network_free_and_constructs_no_store` | EVIDENCED |

Limitation: the Structured Export does not carry the Stage-15 composition (S15-N2; EXPORT-A,
an accepted non-blocking omission). EN / AR does not apply to this JSON API surface.

**Stage-35 Disclosure Export** (`engine/disclosure_export.py`)

| # | Proposed criterion | Existing evidence | Result |
|---|---|---|---|
| D1 | Owner-only access; denials identical; no other project's data | `test_stage35_disclosure_routes.py::test_05_26_denials_are_byte_identical`; `test_stage35_component_disclosure_export.py::test_foreign_and_anonymous_access_are_denied_like_a_missing_project`; `test_stage35_disclosure_projection.py::test_05_projection_never_contains_another_project` | EVIDENCED |
| D2 | One coherent store snapshot; any source failure refuses the whole export and produces no file | projection: `test_06a_every_read_inside_one_snapshot_r1_reads_last`, `test_06b_06c_concurrent_commit_never_mixes_state_and_a_later_export_sees_it`, `test_23_24a_every_source_failure_refuses_never_unavailable`; routes: `test_06e_23_refusals_produce_no_file` | EVIDENCED |
| D3 | JSON and HTML downloads carry the same versioned, deterministic data | routes: `test_15_json_download`, `test_15_html_download_same_data`; projection: `test_12_versions_top_level_and_determinism`; component suite: `test_v2_versions_and_closed_vocabulary` | EVIDENCED |
| D4 | Disclaimers precede the controls; no patentability, FTO or legal-validity wording | projection: `test_02_disclaimers_and_scope_label`, `test_01_no_prohibited_wording_in_system_assertions`; html: `test_01_no_prohibited_wording_outside_the_disclaimer_allow_lists`; routes: `test_02_page_order_disclaimers_before_controls` | EVIDENCED |
| D5 | No mutation, no retained artifact, no API surface, no network or provider call | routes: `test_10_no_mutation_and_no_retention`, `test_routes_add_no_api_surface`; projection: `test_10_no_mutation`, `test_04_no_network_no_provider_import`; component suite: `test_downloads_write_nothing` | EVIDENCED |
| D6 | Self-contained HTML in EN / AR with RTL and no overflow at phone width | html: `test_16_self_contained_document`, `test_02_disclaimers_scope_and_direction`, `test_32_wrapping_and_direction_rules`, `test_32_phone_width_no_horizontal_overflow`; `test_stage34_disclosure_output_language.py`; browser files `test_stage34_disclosure_output_language_browser.py`, `test_stage35_component_disclosure_export_browser.py` | EVIDENCED |
| D7 | The inventor's own text is kept verbatim and escaped | projection: `test_13_hostile_text_round_trips_exactly`; html: `test_13_hostile_text_escaped_and_exact` | EVIDENCED |

Limitation: the legal-adviser review of the disclaimer wording before any user release
(workstream contract §17, decision 9) stays OPEN; this mapping does not address it.

**Remaining gaps.** No material test-evidence gap was found for any of the four rows; no new
test is proposed. Open items: Owner acceptance of S1–S6, E1–E6 and D1–D7; the optional
`control_loop` part-question browser check; the Stage-35 legal-adviser review.
