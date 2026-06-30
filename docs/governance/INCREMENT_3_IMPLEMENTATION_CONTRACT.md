# Increment 3 — Visible Next Development Step — Bounded Implementation Contract

Status:
`DRAFT — NOT AUTHORIZED FOR IMPLEMENTATION`
`COMMITTED AND MERGED VIA PR #40 — OPERATIVE AS A BINDING IMPLEMENTATION BOUNDARY — NOT AUTHORIZED FOR IMPLEMENTATION`

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

## 5. User-visible surfaces (R-3)

One shared derived payload is rendered on two surfaces:

1. a complete `Next Development Step` section in the deliverable;
2. a compact session-screen callout showing the primary issue and the immediate
   user action.

Derivation logic lives in the engine layer only. Templates render the result and
MUST NOT independently determine priority or truth state. The session callout and
deliverable section MUST remain consistent because they consume the SAME derived
payload.

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

## 7. Bounded implementation surfaces

Subject to a SEPARATE later implementation authorization after source review, the
contract authorizes only the following minimum surfaces. No other path may be
included without a later owner ruling.

New:
- `engine/idea_development_outputs.py` — pure, deterministic, non-mutating
  derivation; selects one primary issue using §4; produces a typed
  `Next Development Step` payload; reads existing assertions, gaps, provenance,
  validation, pending dispositions, contradiction relationships, and derived
  readiness; does NOT persist or mutate state.

Modified:
- `engine/deliverable_assembler.py` — call the new pure derivation; add ONE
  additive development-guidance section; preserve all existing sections and the
  existing verdict behavior unchanged.
- `web/templates/deliverable.html` — visibly render the complete
  `Next Development Step` output (issue, reason, required action, evidence or
  specialist input, unlock condition, remaining uncertainty).
- `web/templates/session.html` — render a compact callout from the same derived
  payload; MUST NOT implement priority logic in the template.

New tests:
- `tests/test_increment_3_visible_outputs.py` — unit, assembler, rendered-output,
  session-callout, truthfulness, legacy, contradiction, specialist, and
  evidence-request acceptance coverage.

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
during implementation review, but it must remain typed, deterministic, and
testable. Unused/optional fields default to a truthful absence value (e.g. None /
empty), never a fabricated value.

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
assembler integration tests; rendered-deliverable tests; rendered session-callout
tests; mutation-safety tests; protected-hash verification; and the full
regression suite. The known 31 failures in `tests/test_domain_registry.py` must
remain isolated and unchanged (baseline: full suite `680 passed, 31 failed, 1
skipped, 1 xfailed, 24 xpassed`, plus the new Increment 3 tests).

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
