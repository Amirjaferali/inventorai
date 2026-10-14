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
