# PATH N RUNTIME INTEGRATION AUTHORIZATION PLAN

## 1. Status

- PATH N RUNTIME INTEGRATION AUTHORIZATION PLAN
- PLAN ONLY — nothing in this document authorizes implementation
- Every phase below requires its own separate owner authorization

## 2. Source governance

This plan derives from, and must be read with:

| Commit | Artifact |
|--------|----------|
| `26fa3e1` | `PATH_N_CONTENT_CONFIG_ARTIFACT_APPROVAL_RECORD.md` |
| `8ceb5d4` | `path_n_content_config/electronics_electrical_path_n_questions.json` |
| `806a3c6` | `tests/test_path_n_content_config_artifact.py` |
| `fa26744` | `PATH_N_INTEGRATION_PLAN.md` (Option A: separate content file) |
| `4f0ce81` | `DESIGNATION_ONLY_PATH_INTERFACE_IMPLEMENTATION_PLAN.md` |
| `cdcd079` | `MVP_SCOPE_FREEZE_AMENDMENT_FUNCTIONAL_PATH_N.md` |
| `ccd1ecd` | `MVP_SCOPE_REVISION_DECISION_RECORD.md` (Option A; D-B resolution) |
| `e1095c6` | `QUESTION_FLOW_DISCOVERY_REPORT.md` |
| `a31010a` | `NON_SPECIALIST_QUESTIONING_POLICY.md` |
| `f271f35` | `NON_SPECIALIST_POLICY_ENFORCEMENT_PLAN.md` |
| `72b5f11` | `tests/test_non_specialist_questioning_policy.py` (strict xfail) |

## 3. Objective

Define the safest minimal path by which the approved Path N content
artifact (`8ceb5d4`) may later be connected to live sessions, restricted
to **route/config/session path selection only**, while preserving every
invariant in §4.

## 4. Non-negotiable invariants (inherited, restated)

1. Path T technical bank (`domains/electronics_electrical/domain.json`)
   remains byte-identical. Zero modifications.
2. Deterministic gap gates unchanged: `evaluate_transition()`,
   `assess_response()`, `integrate_response()` not modified.
3. No weakening, bypassing, or re-parameterizing of PASS/WARN/BLOCK logic.
4. Gap taxonomy unchanged. Path N changes asking strategy only (per
   `e2e6234` §scope).
5. `engine/progression_loop.py`: zero net changes. Any discovered
   necessity to modify it is a STOP condition (see §9).
6. Session path default = `legacy_undesignated_current_behavior`
   (per `4f0ce81`). Legacy and undesignated sessions are NEVER
   auto-labeled Path T and NEVER receive Path N content.
7. `runtime_integrated` remains `false` until runtime tests are
   approved AND pass. Per `26fa3e1` §4, changing this flag is itself
   a metadata change requiring re-testing and recorded re-approval.
8. The strict xfail in `72b5f11` converts only after runtime
   integration is verified AND a separate test-update authorization
   is granted.
9. No Workspace, no Engineering Translation stage, no Stage 4+,
   no auto-classification (freeze amendment `cdcd079` boundary).
10. R2 remains HELD until runtime-integrated Path N evidence exists
    (D-B, `ccd1ecd` §6.1).
11. Web routes contain no business logic; path selection at the web
    layer is limited to recording a designation and passing it through.

## 5. Integration design options

### Option I-A — Web-layer path designation + content-layer loader (RECOMMENDED)

- A dedicated route (or route parameter) sets `path = "N"` on session
  creation. All existing routes default to
  `legacy_undesignated_current_behavior`.
- A small, single-purpose loader module in the domain/content layer
  reads the approved JSON artifact and exposes the Path N question
  bank behind the existing question-lookup interface.
- Question selection consults the session's `path` value: `N` → Path N
  bank; any other value → current behavior, byte-identical.
- `domain.json` untouched; engine untouched; web layer carries
  designation only (no selection logic in routes).

### Option I-B — Domain-registry overlay

- Register the Path N artifact in `domain_registry.py` as a path-scoped
  content overlay for `electronics_electrical`.
- Pro: keeps all content routing inside the existing registry authority
  (AB-006). Con: touches registry loading semantics, a wider blast
  radius than I-A; registry schema currently has no path dimension.

### Option I-C — Parallel domain pack (REJECTED)

- A separate pseudo-domain for Path N. Rejected: distorts domain
  inference, duplicates gap taxonomy surface, violates the
  one-domain-one-pack structure, and risks the `iot_electronics`
  schema-drift pattern already on record.

Recommendation: **I-A**, pending the Phase 0 discovery verification
below. Final selection is an owner decision (§11).

## 6. Phased sequence (each phase = separate authorization)

| Phase | Content | Touches | Gate to next phase |
|-------|---------|---------|--------------------|
| 0 | Discovery verification: confirm the exact question-lookup call chain from session to `domain.json`, repository-verified (extends `e1095c6`) | Nothing (read-only) | Committed discovery addendum |
| 1 | Designation-only `path` field (per `4f0ce81`): sessions carry the field; behavior unchanged for all values | TBD by Phase 0 discovery; possible web/session creation layer only, designation-only, no business logic | Tests prove zero behavior change; WPS001 green |
| 2 | Path N content loader module + selection wiring per chosen option | Loader module (new); selection point identified in Phase 0 | New runtime test suite passes (§7) |
| 3 | Runtime test suite committed and green | `tests/` only | Owner review of full results |
| 4 | Eligibility for `runtime_integrated` metadata update after approved runtime tests pass; actual flag change requires separate owner authorization, JSON metadata update, re-testing, and recorded re-approval | Nothing automatic; flag change only under its own authorization | Recorded re-approval |
| 5 | Authorized conversion of `72b5f11` strict xfail | One test file | Owner authorization text |
| 6 | R2 execution authorization becomes eligible (not automatic) | Nothing | Separate owner decision |

No phase may be merged with another. No phase begins without its own
authorization text.

## 7. Runtime test requirements (design targets, not yet written)

1. Default/legacy sessions receive byte-identical question flow
   (regression guard; Path T untouched proof).
2. `path = "N"` sessions receive only N-* question IDs from the
   approved artifact.
3. Disallowed-term scan (per `a31010a` / `56343d6` term list) on
   questions actually served in a Path N session.
4. Deterministic gate proof: identical inputs → identical
   PASS/WARN/BLOCK outcomes regardless of path value.
5. WPS001 invariants suite green, unmodified.
6. Negative control: unknown path values fall back to legacy behavior,
   never to Path N.

## 8. Rollback strategy

- Phases 1–2 are additive and isolated: rollback = revert the specific
  commits; no data migration, no schema change.
- The approved JSON artifact is the single content source; removal of
  the loader restores pre-integration behavior exactly.
- `runtime_integrated` changes only under separately authorized Phase 4,
  after which rollback additionally requires a recorded reversal note
  (governance symmetry).

## 9. STOP conditions

STOP and report, without coding, if discovery or implementation reveals:

- Path N selection cannot be achieved without modifying
  `engine/progression_loop.py`, `evaluate_transition()`,
  `assess_response()`, or `integrate_response()`.
- Selection requires business logic inside web routes beyond recording
  the designation.
- `domain.json` modification appears necessary for any reason.
- Question lookup proves to be engine-internal in a way `e1095c6`
  did not capture.

## 10. What this plan does NOT authorize

- No implementation of any phase.
- No code, test, prompt, or config changes.
- No immediate modification of `web/app.py`. Any future modification is
  allowed only under separately authorized Phase 1 and must be
  designation-only, with no business logic in the route layer.
- No modification of `domain.json`, `engine/progression_loop.py`,
  or the Path T bank, in any phase, ever, under this plan.
- No `runtime_integrated` change.
- No xfail conversion.
- No R2 execution, FORM T work, S-6 classification, or AA-5 progression.

## 11. Required next owner decisions

1. Whether Option I-A is selected (or I-B, or further analysis).
2. Whether Phase 0 (read-only discovery verification) is authorized.
3. Whether Phase 1 follows `4f0ce81` as written or amended in light of
   Phase 0 discovery findings.
4. Confirmation that `runtime_integrated` remains false until a
   separately authorized Phase 4 re-approval, and that R2 remains held
   until runtime-integrated Path N evidence exists.

## 12. Governance effect

- Integration pathway defined; nothing implemented.
- All invariants of §4 restated and binding.
- R2: remains HELD. FORM T: remains BLOCKED.
- S-6: remains UNCLASSIFIED. AA-5: remains BLOCKED.