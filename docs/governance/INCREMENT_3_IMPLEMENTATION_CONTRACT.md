# Increment 3 — Visible Next Development Step — Bounded Implementation Contract

Status:
`DRAFT — NOT AUTHORIZED FOR IMPLEMENTATION`
`CORRECTED SIX-PATH BOUNDARY COMMITTED AND MERGED VIA PR #42 — OPERATIVE AS A BINDING IMPLEMENTATION BOUNDARY — NOT AUTHORIZED FOR IMPLEMENTATION`

This contract expressly relies on the separate owner authority-rulings document
`docs/governance/INCREMENT_3_AUTHORITY_RULINGS.md`
(`OWNER-RATIFIED AND MERGED AUTHORITY RULINGS`). It defines
bounded behavior only. It is not an implementation design and prescribes no
final Python class, exact field name, API signature, or CSS.

## 1. Authoritative baseline

- Authoritative branch `origin/feature/atomic-json-session-persistence` at tip
  `408385f3a7461393e8e9dc0b9f4e1c6433a0f5ce`.
- Remote `main` `0e89e4636399760965c9ff8086b465c90dbadf8e` — outside this lane.
- Frozen persistence worktree `/home/user/inventorai` at
  `aec9cf6409efc18e125b6745762002f59e529654`, seven paused paths, untouched.
- Increment 2 truthful state model is committed and in place: per-record
  provenance and validation status, an append-only assertion/interaction ledger,
  contradiction and supersession relationships, pending specialist/evidence
  dispositions, and a pure derived-readiness module.

## 2. Objective and identity

`INCREMENT 3 — VISIBLE NEXT DEVELOPMENT STEP`.

Convert Increment 2's truthful evidence and readiness state into ONE visible and
actionable next development step for the user's idea, while:

- preserving the six owner actions and all Increment 1/2 behavior;
- preserving deterministic one-question-per-iteration progression;
- preserving the stored forward-only gap lifecycle and stored maturity;
- preserving WPS-001, `score_case()`, golden, replay, and benchmark parity;
- remaining persistence-independent and derived-only.

Increment 3 develops the IDEA, not the inventor.

## 3. Unified scope (R-1)

Increment 3 implements one coherent derived capability — `NEXT DEVELOPMENT STEP` —
whose typed outputs are: (a) one prioritized next action; (b) gap-specific
evidence-request guidance; (c) structured specialist-handoff preparation; and
(d) contradiction-resolution guidance. These are typed payloads of a single
derived guidance flow, NOT separate feature programs. No general deliverable
redesign and no broad technical-recommendation generation are in scope.

## 4. Deterministic presentation priority (R-2)

The derivation selects EXACTLY ONE primary unresolved issue using this fixed
ordering (highest first): 1. active contradiction; 2. pending evidence request;
3. pending specialist request; 4. provisional assumption; 5. owner-provided but
unvalidated answer; 6. open gap; 7. remaining maturity deficiency.

This is presentation prioritization only. It must NOT adjudicate truth, select a
contradiction winner, change stored lifecycle/maturity, mutate assertion state,
delete/supersede records, or introduce scoring. The output MAY state that other
unresolved items remain, but MUST NOT present a ranked multi-item program.

Within-level tie-break (R-6): after applying the order above, if more than one
ACTIVE candidate exists at the selected level, choose exactly one by (1) lowest
numeric `record_id` of the `rec_N` form; (2) else earliest recorded `iteration`;
(3) else stable first-encountered order. Inactive/superseded records are excluded
before tie-breaking. Tie-breaking is presentation-only — no truth adjudication, no
quality ranking, no winner selection, no mutation, no scoring, no history
deletion, no free-form heuristic; identical state always yields the same primary
issue.

## 5. User-visible surfaces (R-3)

One shared derived payload is rendered on two surfaces:

1. a complete `Next Development Step` section in the deliverable;
2. a compact session-screen callout showing the primary issue and the immediate
   user action.

Derivation logic lives in the engine layer only. Templates render the result and
MUST NOT independently determine priority or truth state. The session callout and
deliverable section MUST remain consistent because they consume the SAME derived
payload.

Payload routing (R-5, O-2 operational definition): exactly ONE pure engine
function derives the primary-issue payload. `assemble_deliverable()` invokes or
consumes that derivation to add the deliverable section; the `show_session` route
in `web/app.py` invokes the SAME derivation using the SAME current in-memory
`IdeaState` and passes the resulting payload to `web/templates/session.html`. The
deliverable surface is reachable through the assembler; the session surface is
reachable ONLY through the `show_session` render context, which is why `web/app.py`
is added to the bounded scope (see §7 and R-5). Both surfaces MUST compare equal
by `issue_type` and one stable primary reference identifier (`record_id` or
`gap_type`). No payload is persisted. A future acceptance test
`test_session_and_deliverable_same_primary_issue` MUST demonstrate that the same
state yields the same `(issue_type, reference_id)` on both surfaces.

## 6. Truthfulness and scope boundary (R-4)

The implementation may only reorganize and explain already-recorded facts,
assertions, provenance, validation state, gaps, contradictions, pending requests,
and derived readiness. It must NOT fabricate domain-specific technical
requirements, claim technical verification, imply expert validation, generate
unsupported engineering recommendations, automatically resolve contradictions,
select a winner between assertions, delete history, modify scoring, redesign the
complete deliverable, create specialist-collaboration infrastructure or a
professional workspace, implement persistence, expand domains, or alter the
active anchor. A "technical recommendation" may be displayed ONLY as a truthful
restatement/organization of already-recorded content, with explicit uncertainty
and validation caveats.

## 7. Bounded implementation surfaces (six paths — R-5)

Subject to a SEPARATE later implementation authorization after source review, the
contract authorizes EXACTLY SIX paths and no others. This is the R-5 correction:
the prior version bounded five paths, which could not deliver the session callout
because the `show_session` route owns the session render context; `web/app.py` is
added solely for that reason. No additional path — no CSS, JavaScript, new route,
persistence file, helper module, fixture, or existing test file other than the one
new test file — is authorized. The six paths remain FUTURE scope only; tests-first
and source implementation remain separately unauthorized.

New:
- `engine/idea_development_outputs.py` — pure, deterministic, non-mutating
  derivation; selects one primary issue using §4 (including the R-6 tie-break);
  produces a typed, IMMUTABLE `Next Development Step` payload; reads existing
  assertions, gaps, provenance, validation, pending dispositions, contradiction
  relationships, and derived readiness; does NOT persist or mutate state; does NOT
  import `web/responsibility_labels.py` or any `web/` module (engine must not
  depend on the web layer).
- `tests/test_increment_3_visible_outputs.py` — unit, assembler, rendered-output,
  session-callout, truthfulness, legacy, contradiction, specialist,
  evidence-request, tie-break, O-1 no-fabrication, O-2 same-primary-issue,
  additive-integration, mutation-safety, and protected-hash acceptance coverage.

Modified:
- `engine/deliverable_assembler.py` — call the new pure derivation; add ONE
  additive development-guidance section or payload key; preserve all existing
  sections, verdict behavior, scoring, and readiness outputs unchanged; repurpose
  no existing package field; delete or rewrite no existing section.
- `web/app.py` — ONLY the `show_session` route or its direct render-context
  construction may change, and ONLY to call the shared pure Increment 3 derivation
  with the already-loaded in-memory `IdeaState` and pass the resulting payload to
  `web/templates/session.html`. It MUST NOT change routing behavior, add a route,
  change request methods, mutate state, change session storage, invoke
  persistence, write files, alter scoring, alter progression, change
  authentication or authorization, modify database behavior, change stage
  transitions, introduce a second priority implementation, import paused
  persistence code, or reconcile or reuse the frozen persistence worktree.
- `web/templates/deliverable.html` — visibly render the complete
  `Next Development Step` output (issue, reason, required action, evidence or
  specialist input, unlock condition, remaining uncertainty).
- `web/templates/session.html` — render a compact callout from the same derived
  payload passed in by `show_session`; presentation-only; MUST NOT implement
  priority or truth logic in the template.

No existing test file other than the new test file may be modified, unless an
existing test conflicts with the committed Increment 3 truthfulness requirements,
in which case implementation STOPS and reports rather than editing it.

## 8. Derived output model

The derivation produces a small, typed, deterministic, testable output model
containing only fields equivalent to:

- `issue_type`
- `title`
- `why_it_matters`
- `next_action`
- `evidence_needed`
- `suggested_provider`
- `sufficiency_condition`
- `unlock_condition`
- `remaining_uncertainty`
- references to the relevant stored assertion or gap IDs

These fields MUST NOT be persisted. The exact Python representation is determined
during implementation review, but it must remain typed, deterministic, testable,
and IMMUTABLE (a frozen dataclass or equivalent immutable typed structure). The
immutability requirement introduces no persistence, schema migration,
serialization authority, or API authority. Unused/optional fields default to a
truthful absence value (e.g. None / empty), never a fabricated value.

O-1 grounding and layering. `suggested_provider` may use only engine-resident
responsibility information and MUST resolve to one of `OWNER_INPUT`,
`SYSTEM_ANALYSIS`, `SPECIALIST_INPUT`, `EMPIRICAL_EVIDENCE`, `UNDETERMINED`, or a
truthful absence (None). It is grounded in the disposition kind and the recorded
`AssertionRecord.responsibility` (e.g. an evidence request implies empirical
evidence, a specialist request implies specialist input, an owner answer carries
`OWNER_INPUT`); the engine module MUST NOT import `web/responsibility_labels.py`
or any `web/` module. No free-form provider may be invented; ungrounded provider
information resolves to `UNDETERMINED` or absence. `sufficiency_condition` MUST be
grounded in recorded gap, assertion, evidence, or validation context; unsupported
regulatory, engineering, scientific, commercial, or domain criteria are
prohibited. Future tests MUST include: provider is in the approved vocabulary or
absent; an unknown context does not invent a provider; and sufficiency language is
traceable to recorded state.

## 9. Per-issue behaviors

- **Active contradiction:** display both conflicting claims, their provenance and
  validation state, why the conflict blocks readiness, and a request for
  clarification or stronger evidence. Never select a winner automatically; never
  delete history.
- **Pending evidence request:** display the specific recorded claim or gap, what
  evidence is needed, why it is needed, what would count as sufficient, and what
  decision or readiness state it could unlock. Do NOT invent domain-specific test
  standards.
- **Pending specialist request:** produce a structured handoff PREPARATION
  containing recorded facts, assumptions, unknowns, contradictions, requested
  expertise, a precise question for the specialist, and a validation caveat. Do
  NOT create communication, assignment, account, workflow, or professional-
  workspace infrastructure.
- **Provisional assumption:** ask the user to validate, replace, or explicitly
  retain it as provisional. Do NOT silently promote it to verified fact.
- **Owner-unvalidated answer:** explain that the answer is recorded but not
  independently validated, and identify the next evidence action.
- **Open gap:** use existing gap context and guidance to state the exact missing
  input without fabricating technical requirements.
- **Maturity deficiency:** use ONLY as the final fallback after all
  higher-priority issue types. Do NOT treat maturity as verified readiness.

## 10. Required visible user journey

The implementation must guarantee the user can see: 1. the current truthful idea
state; 2. the single most important unresolved issue; 3. why it matters; 4. the
exact next action; 5. the evidence or specialist input needed; 6. what resolution
would unlock; 7. what uncertainty remains. The session callout and deliverable
section remain consistent via the shared derived payload.

## 11. Legacy and fallback behavior

Required:

- no assertion ledger → conservative fallback to the existing gap-based
  next-step behavior;
- missing optional fields → no crash and no fabricated value;
- no open gaps but unverified evidence → a validation-focused next step;
- verified-ready state → do NOT invent a problem; present a truthful
  readiness-completion or next bounded validation statement;
- superseded records remain historical and do not become the primary current
  issue;
- active contradictions continue to block readiness.

## 12. Protected boundaries

The following must remain byte-identical / unchanged: `engine/scoring.py`;
`engine/progression_loop.py`; `score_case()`; `assess_response()`;
`integrate_response()`; `evaluate_transition()`; the domain registry; ILT content;
golden/replay fixtures; persistence; database or migrations; question
identifiers; stage-transition authority; the active anchor. No schema migration
and no new persisted field is authorized.

## 13. Acceptance requirements (each testable)

- exactly one visible primary next action;
- deterministic priority per §4 (R-2);
- issue-specific reasoning (not a restated gap label);
- evidence-request payload;
- specialist-handoff payload;
- contradiction-resolution payload;
- provisional-assumption behavior;
- owner-unvalidated-answer behavior;
- open-gap fallback;
- maturity fallback;
- fully verified-ready behavior;
- consistent deliverable and session output (same derived payload);
- deterministic within-level tie-break (R-6): identical state yields the same
  primary issue;
- session callout and deliverable section render the same `(issue_type,
  reference_id)` (O-2);
- `suggested_provider` is in the approved vocabulary or truthfully absent, never
  invented (O-1);
- the assembler change is strictly additive (existing sections/verdict/scoring/
  readiness unchanged);
- the `web/app.py` change is confined to the `show_session` render context and
  changes no routing, method, state, storage, persistence, scoring, progression,
  auth, database, or stage-transition behavior;
- the immutable output model cannot be mutated after construction;
- no verification overclaim;
- no automatic contradiction winner;
- no mutation of stored state;
- no persistence dependency;
- conservative legacy behavior (no ledger);
- protected functions unchanged.

## 14. Test plan (minimum)

Pure-derivation unit tests; priority-order tests; active-contradiction tests;
evidence-request tests; specialist-request tests; provisional-assumption tests;
owner-unvalidated-answer tests; open-gap fallback tests; maturity fallback tests;
no-ledger legacy tests; no-open-gap-but-unverified tests; verified-ready tests;
within-level tie-break tests (R-6); `test_session_and_deliverable_same_primary_issue`
(O-2); O-1 provider-vocabulary and no-fabrication tests; additive-integration test
(existing assembler outputs unchanged); `web/app.py` show_session render-context
constraint test (no routing/method/state/persistence/scoring/progression change);
output-model immutability test; assembler integration tests; rendered-deliverable
tests; rendered session-callout tests; mutation-safety tests; protected-hash
verification; and the full regression suite. The known 31 failures in
`tests/test_domain_registry.py` must remain isolated and unchanged (baseline: full
suite `680 passed, 31 failed, 1 skipped, 1 xfailed, 24 xpassed`, plus the new
Increment 3 tests).

## 15. Explicit non-goals

No persistence; no database; no scoring change; no progression-loop change; no
domain expansion; no ILT change; no professional workspace; no specialist
communication infrastructure; no inventor-education program; no business-plan or
patent generation; no full deliverable redesign; no automated truth adjudication;
no automated contradiction resolution; no multi-issue ranked program; no `main`
merge; no Increment 4–6 work.

## 16. Authorization state

- Owner rulings R-1 through R-4 are APPROVED (see
  `INCREMENT_3_AUTHORITY_RULINGS.md`), and that rulings document is committed and
  merged.
- Contract drafting is authorized; this draft is its product.
- This document was independently reviewed, committed in
  `6a11cb2ad389c318ea8f19ea18d95b06c04f59f6`, merged through PR #40, and
  incorporated into the authoritative branch by the documentation-only true-merge
  `429e4b6b88a3fb3d7cece522a0386ec424cf8a1e`. It is therefore OPERATIVE AS A
  BINDING IMPLEMENTATION BOUNDARY.
- Operative as a binding boundary is NOT the same as authorized for
  implementation. This document remains `DRAFT — NOT AUTHORIZED FOR
  IMPLEMENTATION`.
- The corrected SIX-PATH boundary (R-5 / R-6) added by §4, §5, §7, §8, and §18 was
  committed in `8a81ce99aef3bfc05054a812d327247b57c263eb` and merged via PR #42
  (true-merge `083a0bb1de5dd2f62f8d275bc45423f29f70ff64`, ordered parents
  `cb36da8665b5c2704c52235d1b6752ecb0e5e252` then
  `8a81ce99aef3bfc05054a812d327247b57c263eb`). It is now OPERATIVE AS THE BINDING
  future implementation boundary, superseding the prior five-path version (PR #40 /
  PR #41) for current authority.
- Source implementation is NOT yet authorized.
- Tests-first or source work requires a separate, explicit, repository-grounded
  owner authorization for the exact scope, after source review of this contract.

## 17. Non-authorization

This contract: is a committed and merged governance boundary document that is
operative as a binding boundary but is NOT authorized for implementation; does
not authorize Increment 3 implementation; does not authorize code or test
changes; does not authorize tests-first work, an implementation worktree, or any
product-code change; does not authorize persistence, scoring, progression,
domain, or anchor changes; does not authorize a `main` merge; and does not begin
Increment 4, 5, or 6. Any implementation requires a separate, explicit,
repository-grounded owner authorization for the exact scope, after source review
of this contract.

## 18. Six-path scope correction (R-5 / R-6) — merged and binding

This section consolidates the bounded correction. It was committed and merged via
PR #42 (true-merge `083a0bb1de5dd2f62f8d275bc45423f29f70ff64`) and is now OPERATIVE
as the binding Increment 3 implementation boundary, superseding the prior five-path
version. It does not, by itself, authorize implementation.

Blocking finding (from the completed read-only implementation-authorization
review, disposition `INCREMENT 3 IMPLEMENTATION CONTRACT REQUIRES CORRECTION
BEFORE AUTHORIZATION`): the merged five-path scope cannot deliver the R-3 session
callout, because the `show_session` route in `web/app.py` is the sole owner of the
session render context and `web/templates/session.html` (presentation-only) cannot
obtain the engine-selected payload without it. No implementation authorization was
issued.

Owner correction (R-5, R-6):

- Both visible surfaces are preserved (deliverable section + session callout); O-2
  is not deferred and the session callout is not removed.
- Future implementation scope is expanded from five to exactly SIX paths by adding
  `web/app.py`, which is permitted only for the narrow `show_session`
  render-context routing described in §7 and R-5 and is otherwise fully
  constrained.
- One pure engine derivation feeds both surfaces; both compare equal by
  `issue_type` and a stable reference identifier (O-2).
- `suggested_provider` is grounded only in engine-resident responsibility
  information and never invented (O-1); the engine module must not import any
  `web/` module.
- The derived payload is immutable; the assembler change is strictly additive.
- Within-level ties are broken deterministically by R-6 (ascending `rec_N`
  `record_id`, else earliest `iteration`, else stable first-encountered order).

Lifecycle: the corrected six-path contract is now the currently binding boundary
(merged via PR #42), superseding the prior five-path version; tests-first =
unauthorized; source implementation = unauthorized; implementation-worktree
creation = unauthorized. No active-anchor amendment is required: the correction
resolves technical routing and deterministic selection inside the already-approved
Increment 3 identity and changes no product identity, increment sequence, domain
authority, scoring, persistence, or stage-transition authority.
