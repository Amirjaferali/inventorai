# WS6 Evidence — Protected-Test Amendment Record (every changed assertion)

1. tests/test_structured_criticality.py —
   TestGreenJourney::test_g4_uncertainty_and_deferral_zero_delta
   BEFORE: for every package key except section_13_requirement_landscape and
   generated_at: assert json.dumps(before[key]...) == json.dumps(after[key]...)
   AFTER: identical comparison, except for key == "_session_meta" both sides
   first drop ONLY the "requirement_landscape_synthesis" entry.
   REASON: the additive object is canonically DERIVED from Section 13, which
   the test already excludes because a deferral legitimately changes it.
   AUTHORIZATION: owner corrective authorization (GREEN continuation), F1
   ruling section 2. SURROUNDING PROTECTIONS: every other _session_meta key,
   maturity, iteration, direction, gaps, ledger length, unknown count,
   last_result, and all other sections remain strictly byte-compared; the
   whole WS4 suite passes (18) with no other change.

2. tests/test_phase_7b_validation_plan_collapse.py — module constant
   _GENERIC (used unchanged by test_identical_rows_collapse_to_one_with_count,
   test_count_matches_number_of_identical_steps,
   test_rows_with_different_metadata_not_collapsed)
   BEFORE: _GENERIC = "Validate the recorded answer against the available
   evidence."
   AFTER:  _GENERIC = "Validate, revise, or replace it before relying on it."
   REASON: the fixtures record provisional_assumption dispositions whose
   Section 14 step statement now carries the owner-approved action via the
   authorized pass-through. AUTHORIZATION: F1-corrected D4 (contract section
   6/8) + the owner corrective authorization. SURROUNDING PROTECTIONS: all
   grouping, collapse, responsibility, confidence, ordering, count, key-set,
   and rendered-structure assertions byte-unchanged; suite passes (9).

3. tests/test_phase_7c_requirement_landscape_collapse.py —
   test_no_forbidden_wording_introduced_by_collapse
   BEFORE: lowercased Section 13 region scanned for every _FORBIDDEN token.
   AFTER: the region first removes ONLY the byte-exact owner-approved negated
   sentence "This assumption was recorded as a temporary direction and has
   not been validated." (new constant _WS6_ALLOWED_NEGATED_SENTENCE), then
   the identical scan runs.
   REASON: the owner-approved status wording contains the token "validated"
   in negated form; the scan's intent (no positive maturity/validation
   claims) is preserved — any other occurrence of "validated" still fails.
   AUTHORIZATION: owner corrective authorization section 4. SURROUNDING
   PROTECTIONS: all other 7C assertions byte-unchanged; suite passes (7).

tests/test_increment_4_requirement_landscape.py: NO amendment was needed
(its fixtures use answered/evidence/specialist dispositions only); the D4
allowance for that file went unused. All 39 tests pass unmodified.
