# PHASE 4 PATH N RUNTIME INTEGRATION AUTHORIZATION

## 1. Status

APPROVED — EFFECTIVE UPON VERIFIED REPOSITORY ACTIVATION

This document has received explicit owner approval. Its presence in the
working tree does not make it effective. It becomes effective only after
the authorization commit containing this exact approved text is pushed
to `origin/main` and VERIFIED REPOSITORY ACTIVATION is confirmed by raw
post-push evidence.

Activation of this authorization document does not itself authorize
Phase 4 implementation. A later, separate, explicit owner execution
instruction remains mandatory before any implementation working-tree
edit begins.

## 2. Baseline

Exact current baseline:

    bc475ffd2b81ee1023382ea7334b9084e1f63f09

This document is drafted against that HEAD. If HEAD has advanced by the
time of owner review, the baseline must be re-verified before any
activation step.

## 3. Authority sources

| Commit / Path | Artifact |
|---|---|
| `d2b2a9a` | `PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION_PLAN.md` — defines Phase 4 (§6 row 4) and the §4.7 invariant |
| `26fa3e1` | `PATH_N_CONTENT_CONFIG_ARTIFACT_APPROVAL_RECORD.md` — establishes that any future `runtime_integrated` change requires re-testing and recorded re-approval |
| `8ceb5d4` | `path_n_content_config/electronics_electrical_path_n_questions.json` — the artifact whose metadata this document targets |
| `806a3c6` | `tests/test_path_n_content_config_artifact.py` — the test file whose two assertions this document targets |
| `7a3350c` | `POST_PHASE_2_AUTHORIZATION_REVIEW.md` — confirms the flag-flip is a defined process, not a synonym for "tests pass" |
| `db2c46e` | `LIMITED_EVIDENCE_AUTHORIZATION.md` — confirms E-2/E-3 evidence does not by itself make `runtime_integrated=true` eligible |
| `3a7bc13`, `bc475ff` | Phase 3 closure record and roadmap sync — establish Phase 3's technical criterion SATISFIED and operationally EFFECTIVE, the precondition this document treats as met |

## 4. What this document is responding to

A read-only Phase 4 eligibility assessment determined Phase 4 eligible
for owner review only, identified the future `status` value as a
blocking ambiguity, and required explicit (not inferred) authorization
for the tripwire test's treatment. This document resolves those
ambiguities by explicit owner decision, recorded here for the first
time. This document is self-contained: it does not rely on any prior
conversational draft for its operative content.

## 5. Exact authorized future file scope

### 5.1 Implementation-commit scope — exactly two files

1. `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json`
2. `tests/test_path_n_content_config_artifact.py`

These two files, and only these two, may appear in the implementation
commit (§9 step I).

### 5.2 Complete governed chain — exactly five paths

Across the entire governed sequence (§9), exactly five paths may ever be
created or modified under this authorization, and no others:

1. `docs/governance/PHASE_4_PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION.md` — this document, in the authorization commit only
2. `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json` — in the implementation commit only
3. `tests/test_path_n_content_config_artifact.py` — in the implementation commit only
4. `docs/governance/PHASE_4_PATH_N_RUNTIME_INTEGRATION_CLOSURE_RECORD.md` — in the closure commit only (this exact filename)
5. `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` — in the roadmap-synchronization commit only

No other path may be created or modified at any point in this governed
sequence.

Explicitly excluded from modification under this authorization, in
every commit at every stage:

- `tests/test_non_specialist_questioning_policy.py` (contains the
  `72b5f11` strict xfail — Phase 5 only)
- `engine/` (any file)
- `web/` (any file)
- `domains/electronics_electrical/domain.json`
- Any question text, question ID, or question ordering inside the
  artifact

## 6. Exact metadata before/after values

Current committed state (`8ceb5d4`, unchanged at baseline `bc475ff`):

```json
"metadata": {
    "path": "Path N",
    "domain": "electronics_electrical",
    "status": "approved_governance_content_not_runtime_integrated",
    "source_spec": "e2e6234",
    "approval_record": "effd040",
    "integration_plan": "fa26744",
    "artifact_plan": "932b7a8",
    "runtime_integrated": false
}
```

Authorized future target state, introduced in the working tree only
during §9 step D and committed only during §9 step I, after §13's
preconditions and all applicable §9 prerequisite steps are satisfied
in order:

```json
"metadata": {
    "path": "Path N",
    "domain": "electronics_electrical",
    "status": "approved_governance_content_runtime_integrated",
    "source_spec": "e2e6234",
    "approval_record": "effd040",
    "integration_plan": "fa26744",
    "artifact_plan": "932b7a8",
    "runtime_integrated": true
}
```

[OWNER DECISION] The `status` value
`approved_governance_content_runtime_integrated` is introduced here, by
explicit owner decision, as the authorized replacement string. No prior
committed document defines this value; it must not be cited elsewhere
as a pre-existing fact.

No other field may change. No question ID, question text, or `gaps`
structure may change.

## 7. Exact permitted test-file changes

Within `tests/test_path_n_content_config_artifact.py`, exactly three
changes are authorized, and no others. No other assertion, test,
fixture, import, helper, formatting block, or source file in this or
any other file may change.

**A. `EXPECTED_METADATA["status"]` replacement:**

Before:
```python
"status": "approved_governance_content_not_runtime_integrated",
```

After:
```python
"status": "approved_governance_content_runtime_integrated",
```

**B. `test_metadata_correct`'s `runtime_integrated` assertion
replacement:**

Before:
```python
assert meta.get("runtime_integrated") is False, (
    f"runtime_integrated must be false, got: {meta.get('runtime_integrated')!r}"
)
```

After:
```python
assert meta.get("runtime_integrated") is True, (
    f"runtime_integrated must be true, got: {meta.get('runtime_integrated')!r}"
)
```

**C. Complete replacement test** (replacing
`test_runtime_integrated_remains_false` in full, including its name):

```python
def test_runtime_integrated_remains_true_post_phase4():
    """Post-Phase-4 invariant (Phase 4 authority
    PHASE_4_PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION.md): the flag must
    remain true after authorized runtime integration. Any future
    regression of this flag to false outside a separately authorized
    rollback action fails the suite loudly."""
    meta = load_artifact().get("metadata", {})
    assert meta.get("runtime_integrated") is True, (
        "runtime_integrated reverted to false unexpectedly — any "
        "reversal requires its own recorded rollback authorization"
    )
```

No other assertion, test, fixture, import, helper, formatting block, or
source file may change as part of this authorization.

## 8. Commit-role separation

No single commit listed below, by itself, makes Phase 4 operationally
effective. Operational effectiveness requires the full chain in §9
through step N, including both pushes defined in §10.

| Commit | Purpose | Permitted files | Changes `runtime_integrated` bytes? | Alone makes Phase 4 effective? |
|---|---|---|---|---|
| **Authorization commit** | Commits this document, once owner-approved, as the governing text for the sequence below | §5.2 path 1 only | No | No |
| **Implementation commit** | Performs the coordinated JSON metadata change and the three §7 test-file edits together | §5.2 paths 2–3 only | Yes — sets the committed byte to `true` | No — explicitly not treated as recorded re-approval (§9 step J) |
| **Closure commit** | Records owner review of test results and diff; declares the change reviewed and accepted | §5.2 path 4 only | No (declares, does not itself flip bytes) | No, alone — but is the textually required "recorded re-approval" |
| **Roadmap synchronization commit** | Updates `ACTIVE_EXECUTION_ROADMAP.md` baseline, chain, and lane narrative to reflect Phase 4 closure | §5.2 path 5 only | No | No, alone |

Four governed commits total. Only the complete chain, pushed per the
two-push model in §10 and each push's activation verified, constitutes
Phase 4 CLOSED.

## 9. Governed execution sequence

No step below may be merged with another. Each lettered step requires
the explicit authorization or instruction named, issued separately, in
order:

**A.** This Phase 4 authorization document is approved (revised to
   carry APPROVED — EFFECTIVE UPON VERIFIED REPOSITORY ACTIVATION
   status) and committed as the authorization commit (§8).

**B.** Push / Activation 1 (§10) is performed for the authorization
   commit alone, and VERIFIED REPOSITORY ACTIVATION is confirmed by raw
   post-push evidence.

**C.** A separate, explicit owner execution instruction authorizes the
   coordinated implementation. Push/Activation 1's completion in step B
   does not itself constitute this instruction.

**D.** The exact JSON metadata change (§6) and the exact three
   test-file changes (§7) are made together in the working tree, as one
   coordinated edit — never split across separate working states that
   leave the repository knowingly failing.

**E.** The complete required test battery (§11) is executed in full.

**F.** Raw test output, `git status --short`, and the complete
   working-tree `git diff` are reviewed by the owner against this
   document's exact specifications (§5–§7, §11).

**G.** Stage exactly the two implementation files under a separate,
   explicit staging authorization, distinct from step F's review
   approval.

**H.** Review and approve the staged index byte-for-byte:
   - complete `git diff --cached`;
   - staged path count;
   - staged statuses;
   - staged blob SHA256;
   - confirmation of no unstaged changes.

**I.** Create the implementation commit — only under a separate,
   explicit commit authorization, distinct from step H's review
   approval — containing exactly the two §5.1 files.

**J.** Verify the implementation commit locally:
   - commit hash;
   - exact parent;
   - exact two paths;
   - committed blob SHA256;
   - clean working tree and index;
   - not pushed by itself (§10);
   - not recorded re-approval;
   - not operational activation.
   The byte value `runtime_integrated: true` now exists in local
   committed history at this point, but is not yet the approved
   governance state (§17).

**K.** Draft, review, approve, and commit the exact closure record:
   `docs/governance/PHASE_4_PATH_N_RUNTIME_INTEGRATION_CLOSURE_RECORD.md`
   (§5.2 path 4). This closure record may rely on the reviewed evidence
   from the verified local implementation commit (step J); it does not
   require that commit to have been pushed first.

**L.** Create the separate roadmap-synchronization commit (§5.2 path
   5), updating §4 baseline, §4 status row, §5 chain, and §6/§7
   narrative.

**M.** Perform Push / Activation 2 (§10): the implementation commit,
   closure commit, and roadmap-synchronization commit are pushed
   together as one exact linear fast-forward chain, after all three are
   locally committed and verified.

**N.** Only after complete post-push verification — `HEAD = origin/main`,
   all hashes match their approved values, the working tree is clean,
   and the complete chain is remotely verified by raw post-push evidence
   — may Phase 4 be classified CLOSED and `runtime_integrated=true` be
   treated as the approved governance state.

Editing the metadata, passing tests, or creating the implementation
commit alone does NOT complete Phase 4. Phase 4 closes only at step N.

## 10. Two-push activation model

**Push / Activation 1:**
- Authorization commit only.
- Pushed to `origin/main`.
- Post-push verification performed.
- The authorization becomes effective.
- Only then may the separate execution instruction (§9 step C) be
  issued.

**Push / Activation 2:**
- Implementation commit (§9 step I), closure commit (§9 step K), and
  roadmap-synchronization commit (§9 step L).
- Pushed together as one exact linear fast-forward chain only after the
  implementation commit has been verified under §9 step J and the
  closure and roadmap-synchronization commits have each been created
  and verified under their separately authorized review procedures.
  §9 step M performs the push and does not itself supply the required
  pre-push verification.
- Post-push verification confirms all three remote hashes and
  `HEAD = origin/main` (§9 step N).
- Only then may Phase 4 become CLOSED and `runtime_integrated=true`
  become the approved governance state.

Clarifications:

- The local implementation commit (step I) is not pushed by itself; it
  remains local until Push/Activation 2.
- The local closure record (step K) may rely on reviewed evidence from
  the verified local implementation commit (step J), without that
  commit having been separately pushed first.
- No remote operational state is claimed until Push/Activation 2
  completes.
- No single commit, and no Push/Activation 1 alone, closes Phase 4.

## 11. Mandatory test battery and result expectations

Required, by direct authority of the artifact approval contract
(`26fa3e1` §3, which names this exact suite as the artifact's evidence
basis):

    pytest tests/test_path_n_content_config_artifact.py -q

Expected result: exactly **10 passed**.

[OWNER DECISION] The following four are required under this
authorization as an owner-imposed regression requirement for Phase 4 —
not pre-existing mandatory Phase 4 text in `d2b2a9a` — included to
confirm no Path N selection behavior regressed as a side effect of this
metadata-only change:

    pytest tests/test_phase2_path_n_selection.py -q
    pytest tests/test_phase1_path_designation.py -q
    pytest tests/test_web_app.py -q
    pytest tests/test_wps001_invariants.py tests/test_path_n_content_config_artifact.py tests/test_non_specialist_questioning_policy.py -q

For these four commands, each must satisfy:

- process exit code 0;
- zero failed;
- zero errors;
- no interruption;
- no collection error.

No exact result count is claimed for these four commands as a
pre-established fact in this document.

In the command including `tests/test_non_specialist_questioning_policy.py`,
the strict xfail `72b5f11` must:

- remain xfailed;
- not be passed;
- not be xpassed;
- not be skipped for another reason;
- not be removed;
- not be converted.

## 12. STOP conditions

- The artifact suite must report exactly 10 passed; any other count:
  STOP.
- Each of the other four authorized commands must exit successfully
  with zero failed and zero errors; any unexpected result count, skip,
  xfail, xpass, warning escalation, or collection anomaly must be
  reported for owner review before staging — STOP and report, do not
  proceed to staging.
- The strict xfail `72b5f11` must remain xfailed and must not become
  passed, xpassed, skipped for a different reason, removed, or
  converted; any such change: STOP.
- If execution reveals a failure in any additional test or dependency
  not included in the authorized battery: STOP and report it; do not
  expand the test or modification scope without new owner
  authorization.
- Any file outside the §5.1 implementation-commit scope shows as
  modified in `git status` during the implementation step: STOP.
- The §7 Change C renamed test cannot be made to pass without touching
  any other test, fixture, or source file: STOP.
- The `status` string substitution is found, upon re-verification at
  execution time, to require updating any other repository file: STOP.
- Any edit appears to require touching `engine/`, `web/`, or
  `domain.json` for any reason: STOP.

## 13. Mandatory preconditions (before any working-tree edit)

1. `git status --short` returns empty.
2. `git rev-parse HEAD` equals the baseline recorded at execution time
   (re-verified, not assumed from §2 if time has passed), and equals
   `origin/main`.
3. Working-tree SHA256 of both §5.1 files equals their committed HEAD
   SHA256 (no pre-existing drift).
4. This document is committed as the authorization commit, Push/
   Activation 1 (§10) is complete, and VERIFIED REPOSITORY ACTIVATION
   is confirmed by raw post-push evidence, before any working-tree edit
   to the two implementation files begins (§9 steps A–B before D).
5. A separate, explicit owner execution instruction (§9 step C) has
   been issued after Push/Activation 1's confirmed activation.

## 14. Rollback rules

**Case A — before the implementation commit (§9 steps D–H, not yet
I):**

- Discard only the authorized uncommitted edits (`git checkout --
  <files>` or equivalent).
- Verify clean restoration to the baseline (`git status --short` empty,
  SHA256 of both files matches pre-edit committed values).
- Record the aborted-execution evidence (what was attempted, why
  aborted, raw verification of restoration) for the governance record,
  consistent with this repository's pattern of recording even
  incomplete/aborted operations.

**Case B — after the implementation commit, or after any further step
through verified Phase 4 activation (§9 step I onward):**

- Rollback requires its own separate owner authorization — it is not
  available as a unilateral or automatic action.
- Rollback consists of: implementation revert (reverting the
  implementation commit); regression re-testing (re-running §11's
  battery against the reverted state); a recorded reversal / re-
  approval document (mirroring §9 step K's structure, but documenting
  reversal rather than adoption); roadmap synchronization (reflecting
  the reversion); a controlled push of the reversal chain; and
  post-push verification.
- After a closure record or roadmap-sync commit exists referencing the
  Phase 4 state as adopted, silently reverting only the implementation
  commit — without the accompanying reversal documentation,
  re-testing, and roadmap sync — would create governance inconsistency
  (a roadmap and closure record asserting a state the code no longer
  reflects) and is prohibited.

## 15. Evidence requirements

- Full raw terminal output of all five §11 commands, pasted verbatim by
  the owner, before the staging step (§9 step G) begins.
- `git diff` reviewed and confirmed to touch exactly the two
  implementation files, matching exactly the §6/§7 specifications,
  before the staging step (§9 step G) begins.
- SHA256 verification of both files before and after edit.
- Post-push verification at both Push/Activation 1 and Push/Activation
  2 (§10), each following the same pattern used for the Phase 3 closure
  and roadmap-sync push (HEAD/origin/main match, ahead-behind 0 0,
  remote file SHA256 confirmation).

## 16. Explicit non-authorizations

This document, even once activated at §9 step B, does NOT authorize:

- Immediate repository modification upon Push/Activation 1 — §9 step
  C's separate explicit owner instruction is required before step D
  begins.
- `runtime_integrated=true` as the approved governance state before §9
  step N completes (see §17 on byte state vs. approved state).
- Phase 5 (conversion of the `72b5f11` strict xfail).
- R2 release or execution.
- FORM T unblock.
- S-6 classification.
- AA-3, AA-4, or AA-5 progression.
- ILT-002 evidence collection.
- Any downstream AA execution.
- Any claim of production readiness.
- Any change to `engine/`, `web/`, `domains/electronics_electrical/domain.json`,
  question content, scoring, deterministic gates, or PASS/WARN/BLOCK
  logic.

## 17. Byte state vs. approved governance state

- During the authorized implementation step (§9 steps D–I), the JSON
  working-tree value and, after step I, the implementation-commit value
  may become `runtime_integrated: true`.
- That byte value must NOT be described as the approved operational
  governance state until the closure record (step K), roadmap
  synchronization (step L), Push/Activation 2 (§10, step M), and
  VERIFIED REPOSITORY ACTIVATION (step N) are all complete.
- `runtime_integrated: true` existing in local committed history
  (post-step I, pre-step N) is not proof of live runtime behavior or
  production readiness, and is not yet the approved governance state —
  it is an implementation byte pending governance ratification.

## 18. R2 / Phase 5 boundary

- Phase 5 (strict-xfail conversion) requires its own separate
  authorization text (`d2b2a9a` §6 row 5: "Owner authorization text" as
  the gate). This document does not supply that text.
- R2 remains HELD both before and after this document's full execution
  through step N. Completing Phase 4 does not itself authorize R2
  execution.
- Phase 6 (R2 execution authorization eligibility) remains, per `d2b2a9a`
  §6 row 6, "not automatic" even after Phase 4 and Phase 5 are both
  complete — it requires its own "separate owner decision."
- [INTERPRETATION, not FACT] The committed phase table (`d2b2a9a` §6,
  rows 4–6), read together with §4 invariant 10 ("R2 remains HELD until
  runtime-integrated Path N evidence exists"), strongly supports a
  Phase 4 → Phase 5 → Phase 6 sequential dependency. No single clause in
  any committed document states this conjunction verbatim. This
  conclusion is constructed from reading the phase table in sequence and
  must not be cited elsewhere as a directly quoted FACT.

## 19. Assumptions and hidden assumptions

**Stated assumption:** that the `status` string's internal
self-description should match the `runtime_integrated` boolean's actual
value, motivating the §6 owner-decided replacement string. This is an
owner decision, not a textual requirement derived from any committed
clause.

**Hidden assumption:** that "coordinated" in §9 step D means the JSON
and test-file edits land in the same working-tree session and the same
implementation commit (step I), not merely the same review session.
This document adopts that reading explicitly to avoid any intermediate
failing state.

**Hidden assumption:** that renaming
`test_runtime_integrated_remains_false` (rather than only editing its
body) is required to avoid a misleading test name. No committed text
mandates a rename versus an in-place edit; this is a drafting choice
recorded as an owner decision, not a discovered fact.

## 20. Invalidating evidence

The following, if found true at execution time, would invalidate this
authorization and require re-drafting rather than execution as-is:

- If `status` is referenced verbatim in any file outside the two
  implementation-commit files (not found in the prior assessment's
  repository-wide grep, but not re-verified at execution time —
  re-verification is a mandatory precondition per §13).
- If any test outside `tests/test_path_n_content_config_artifact.py`
  is found to assert on the literal `status` string value.
- If `git status` is not clean at execution time, indicating
  uncommitted drift since this document's drafting baseline.

## 21. Red-team controls

- Risk: treating `runtime_integrated: true` as proof of runtime
  behavior. Mitigated by §17's explicit byte-state-vs-approved-state
  distinction.
- Risk: silently leaving the tripwire test failing after the metadata
  change. Mitigated by §9 step D's coordinated, same-session edit
  requirement and step I's single-commit scope.
- Risk: scope creep into Phase 5 via the regression battery's inclusion
  of `tests/test_non_specialist_questioning_policy.py`. Mitigated by
  §11's explicit statement that running this suite does not authorize
  modification or advance Phase 5, and §12's explicit xfail-integrity
  STOP condition.
- Risk: premature R2 inference from Phase 4 completion alone. Mitigated
  by §18's restatement that R2 remains HELD and Phase 6 is separately
  non-automatic.
- Risk: this document being treated as self-executing upon its own
  commit or Push/Activation 1. Mitigated by §9 step C's requirement of
  a separate, explicit owner execution instruction.
- Risk: a later silent partial rollback creating governance
  inconsistency. Mitigated by §14 Case B's explicit prohibition.
- Risk: claiming remote operational state before Push/Activation 2.
  Mitigated by §10's explicit clarification that no remote operational
  state is claimed until Push/Activation 2 completes.
- Risk: staging and commit creation collapsing into one undifferentiated
  action. Mitigated by §9 steps G/H/I being three distinct steps, each
  requiring its own separate authorization.
- Risk: treating the push operation (§9 step M) itself as supplying
  pre-push verification. Mitigated by §10's explicit statement that
  step M performs the push and does not itself supply the required
  pre-push verification, which instead comes from steps J, K, and L.

## 22. Activation model

This document must be committed only after its status line is converted
from RESPONSE-ONLY DRAFT — NOT EFFECTIVE to APPROVED — EFFECTIVE UPON
VERIFIED REPOSITORY ACTIVATION. Once committed in that APPROVED form,
Push/Activation 1 (§10) is performed and VERIFIED REPOSITORY ACTIVATION
is confirmed by raw post-push evidence (`HEAD = origin/main`,
ahead/behind `0 0`, file SHA256 match) — exactly the pattern used for
the Phase 3 closure record and the ILT-002 disposition. Only after that
activation does §9 step C (the separate execution instruction) become
possible to issue.

## 23. Amendment 1 — §11/§12 expected test count correction

This amendment corrects a defect discovered during the first execution
attempt under this authorization. It does not expand, narrow, or
reinterpret any other section of this document.

**What happened:** Under the original §11/§12 text, the artifact suite
(`pytest tests/test_path_n_content_config_artifact.py -q`) was executed
as part of an authorized Step E attempt. The actual result was 10
passed, exit code 0 — not the 9 passed required by the original text.
This discrepancy triggered the mandatory STOP condition in the original
§12 as written at the time.

**Restoration:** Following the STOP, both files in the §5.1
implementation-commit scope (the JSON content file and the test file)
were restored to a clean `HEAD`. No staging, no implementation commit,
and no push occurred under the rejected attempt. The restoration was
documented at the time by SHA256 equality between each restored
working-tree file and its corresponding `HEAD` blob, together with a
clean `git status`.

**Correction:** §11 and §12 are corrected so that the artifact suite's
expected result is exactly 10 passed, matching the actually observed
test count. No other expected count, STOP condition, or authorized
scope in this document is altered by this correction.

**Explicit prohibitions and requirements:**
- The rejected Step D/Step E attempt is not retroactively accepted as
  successful and must not be characterized as such in any future
  record.
- Step D and Step E must be repeated in full from a clean working tree
  after this amendment is activated. The prior rejected attempt does
  not substitute for this repetition.
- A new, separate, explicit owner authorization is required before
  Step D may be restarted. This amendment does not itself constitute
  that authorization.
- The two authorized implementation-commit paths defined in §5.1 remain
  unchanged and exhaustive; this amendment authorizes no additional
  file.
- All other STOP conditions in §12, all preconditions in §13, all
  rollback rules in §14, and all other controls in this document remain
  unchanged and in full force.
- `runtime_integrated` remains governance-approved as `false` until the
  full controlled Phase 4 sequence (§9) and final closure are completed
  under a corrected and successfully repeated Step D/Step E.
- R2 remains HELD. FORM T remains blocked. Phase 5, Phase 6, AA-3, AA-4,
  and AA-5 remain unauthorized under the current governing repository
  authority and are not authorized by this amendment.
- The commit that activates this amendment is an exceptional
  authority-correction commit. It is not an implementation commit and
  does not itself touch any §5.1 implementation-commit-scope file.
- This correction creates no precedent for silently adjusting any
  future expected test count without an equivalent documented
  amendment, STOP record, and owner authorization.
- This amendment becomes effective only after its own commit, push,
  and post-push verification against `origin/main` — following the
  same activation pattern described in §22.
