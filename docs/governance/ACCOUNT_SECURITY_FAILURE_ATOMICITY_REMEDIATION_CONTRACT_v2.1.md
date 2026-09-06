# Account Security Failure-Atomicity Remediation Contract v2.1

## Authority, source and scope

This document is the complete Owner-approved F-01/F-02 v2.1 contract of record.
ACTIVE_INCREMENT_CONTRACT.md identifies it as the active governing contract.
Active contract status is distinct from Implementation START. Contract adoption
grants no Creator implementation, publication, PR, merge, pilot or deployment authority.

Owner approval provenance is recorded in OWNER_DECISION_REGISTER.md, section
"F-01/F-02 v2.1 — contract approval and adoption authority".
Adoption lifecycle and the separate next gate are recorded in
ACTIVE_EXECUTION_ROADMAP.md, section
"F-01/F-02 v2.1 — repository adoption and active-contract installation".

## Exact approved text and historical-status interpretation

The approved packet below is reproduced without textual correction or substantive
change. Sections 1–18 govern the future F-01/F-02 implementation, including every
retained v2.0 decision and the controlling D-04/D-05 corrections. D-01 through
D-05 are closed contract-review findings, not assertions that runtime defects
F-01/F-02 are fixed.

Source: Pasted markdown(20260905-210921).md
File ID: file_00000000fd6c81f492db5c5bd4ae1b41
Source SHA-256: 94ddae95f90e6de36e4826dd3d3c50982a6825aeade8ca4e2e7997fd45677ca3
Source bytes: 23607; UTF-8; LF; 505 split lines; no final LF.
Approved packet byte range in source: [361, 21870), zero-based.
Approved packet bytes: 21509.
Approved packet SHA-256: a01665b80dfeaf21319c52792f773bc138346905d8400f057e9f176b62ec1140

"DECISION-READY", "OWNER APPROVAL: PENDING" and other preparation-stage status
statements within the preserved packet describe its original issue-time snapshot,
not current adoption status. The separately recorded issued Owner approval
establishes approval of its substance. Its technical requirements are not replaced
by this provenance wrapper. Its ban on governance edits applies to the future
implementation scope; the separate adoption authority owns this documentation-only
installation. No implementation authority is inferred from either instrument.

The preparation SHA in the packet is historical. Before a subsequent implementation
instruction, Lead must reconcile the bounded base-to-adoption delta, prove unchanged
implementation surfaces, and bind the separate Implementation START decision to the
verified adoption merge. No silent base transfer, contract rewrite, or second
contract-activation candidate is permitted.

<!-- BEGIN APPROVED V2.1 PACKET: exact 21509 bytes start after the following LF -->
## OWNER DECISION PACKET — VERSION 2.1

**INVENTORAI — ACCOUNT SECURITY FAILURE-ATOMICITY REMEDIATION**
**F-01 + F-02 ONLY**

**STATUS:** DECISION-READY — NOT AN EXECUTION AUTHORIZATION
**SUPERSEDES:** Packet v2.0 as the proposed decision text only. Neither version grants execution authority.

**Repository:** `Amirjaferali/inventorai`
**Authoritative execution branch:** `feature/atomic-json-session-persistence`
**Preparation base / last verified tip:** `2fb3e2166a1bd0b5c3d57850a4f9d50eeba14d45`

This packet does not assert a fresh live-tip verification. If the authoritative tip differs before a future execution instruction is released: STOP, reconcile the bounded delta, and do not silently rebase, transfer or execute this contract.

### 1. Subject and retained decisions

F-01 concerns suppressed session-epoch persistence failure in `POST /logout-all`, followed by a misleading normal logout redirect.

F-02 concerns separately committed password-reset steps that can leave token, password and session state inconsistent.

Retained decisions:

- Exact SQL UPDATE row-count proof for F-01.
- Generic HTTP 503 for operational failures; no false success.
- Two-stage password reset: read-only eligibility precheck, hashing outside the writer transaction, then authoritative transactional revalidation and completion.
- One transaction containing every F-02 mutation.
- Shared AccountStore `_write()` hardening: D-02 Option A.
- Honest distinction between confirmed rollback, confirmed commit and indeterminate durable outcome.
- Four-path change boundary, expanded shared-helper regression sweep and bounded post-candidate independent security review.
- F-03 and every unrelated product/governance state remain separate and unchanged.

**Implementation authorization: NO.**
**Creator instruction: NOT AUTHORIZED.**

### 2. F-01 — authoritative success proof

Existing authenticated-account and CSRF guards remain unchanged.

Inside the existing AccountStore `_write()` transaction, increment the exact account’s epoch using:

```sql
UPDATE accounts
SET session_epoch = session_epoch + 1,
    updated_at = ?
WHERE account_id = ?
```

Success requires:

1. The exact UPDATE row count equals **1**.
2. COMMIT is confirmed successful.
3. The route receives an unambiguous successful store result.

A missing account, zero rows or any unexpected non-1 row count is an operational/invariant failure.

Do not compare against an epoch previously read by the web route as the production success guard. That snapshot may be stale. A returned resulting epoch may be retained, but absence of an exception alone is insufficient proof.

After confirmed success:

- Clear the current authenticated browser session.
- Preserve the existing UI-language behavior.
- Return the established login redirect.
- Previously issued sessions with older epochs become invalid.
- Change no password, reset token, project, ownership or unrelated account state.

An isolated test must still prove an exact epoch delta of **+1** for one successful logout-all request.

### 3. F-01 — failure semantics, corrected by D-04

All operational failures return a generic, non-disclosing **HTTP 503**, without a login success redirect or logout-all success claim.

#### A. Failure confirmed rolled back before durable commit

- Do not clear the current browser session.
- Preserve its CSRF and UI-language state.
- Prove that the current session remains authenticated under controlled test conditions.
- Prove the epoch and unrelated durable state are unchanged.
- Do not claim global revocation.

#### B. COMMIT exception with confirmed committed or indeterminate durable state

- Do not deliberately clear or rewrite local browser-session material.
- Preserve local cookie/session material to the extent the response mechanism permits.
- **Do not guarantee continued authentication.**
- Let the next normal server-side epoch validation determine actual validity.
- Do not claim successful global revocation or confirmed rollback.
- Do not automatically retry.

Preserving local session material must not bypass epoch validation. A later normal validation may legitimately invalidate or clear a stale session.

Tests and evidence must distinguish:

| Evidence classMeaning                      |                                                             |
| ------------------------------------------ | ----------------------------------------------------------- |
| Local material not deliberately cleared    | No deliberate logout/session rewrite by the failure handler |
| Authenticated validity confirmed preserved | Normal validation independently accepted the session        |
| Authenticated validity invalidated         | Normal validation rejected the session                      |
| Validity indeterminate                     | Available evidence cannot establish validity                |

The first class is never proof of the second.

### 4. F-01 — separate acceptance tests

Required tests:

1. Normal success returns the established redirect.
2. One isolated success produces an exact epoch delta of +1.
3. Success clears the initiating authenticated browser session.
4. A distinct pre-existing session is rejected after success.
5. Missing and invalid CSRF retain existing rejection behavior.
6. Epoch UPDATE exception returns generic 503.
7. Missing-account/zero-row and unexpected non-1 results fail closed.
8. COMMIT exception returns generic 503 without a success claim.
9. Confirmed rollback preserves current session material, CSRF and language; normal validation confirms authentication.
10. Confirmed rollback leaves epoch and other-session validity unchanged under controlled conditions.
11. A simulated commit-then-error does not deliberately clear local session material; subsequent normal validation rejects the old epoch.
12. Indeterminate COMMIT outcome does not claim either continued authentication or confirmed rollback.
13. No unrelated durable mutation occurs.
14. Production success does not depend on a previously read epoch snapshot.

Evidence must separately record local-session handling, actual server-side validity and durable-state certainty.

### 5. F-02 Stage A — read-only resource guard

Proposed store seam:

```text
password_reset_eligible(token_hash, now_iso) -> bool
```

The precheck must:

- Perform no INSERT, UPDATE, DELETE, token reservation or durable mutation.
- Require an existing RESET token that is unused and unexpired.
- Require an existing active account.
- Return False for nonexistent, expired, replayed, wrong-type or ineligible-account tokens.
- Distinguish operational store failure from ordinary ineligibility.

On False:

- Do not invoke password hashing.
- Perform zero durable mutation.
- Return the established generic invalid-token HTTP 400.

On operational precheck failure:

- Do not invoke password hashing.
- Return generic HTTP 503.
- Do not deliberately clear browser-session material.
- Perform zero intentional reset mutation.

All ordinary ineligibility reasons share the same generic response. Operational responses must not disclose account/token existence, status, type, age, replay state or the failed check.

The precheck creates **no mutation authority**, reservation or TOCTOU guarantee. True permits only proceeding to password hashing. It must never become a trusted eligibility flag passed to Stage B.

### 6. F-02 — password hashing

Order:

1. Existing password-policy and confirmation validation.
2. Read-only eligibility precheck.
3. Existing password hashing, only after a True precheck.
4. Atomic completion.

Hashing must occur outside `_write()`, outside `BEGIN IMMEDIATE` and without holding the SQLite writer lock.

On hashing failure:

- Zero reset mutation.
- Generic HTTP 503.
- No deliberate session clearing.
- No sensitive disclosure.

The precheck does not promise that a token cannot become ineligible during hashing. Stage B handles that race independently.

### 7. F-02 Stage B — one authoritative transaction

Proposed store seam:

```text
complete_password_reset(token_hash, new_password_hash, now_iso)
```

Within one `_write()` / `BEGIN IMMEDIATE` transaction:

1. Independently resolve the token by hash and RESET type.
2. Revalidate existence, unused state and expiry.
3. Independently resolve the account and revalidate existence and active status.
4. Only after all eligibility conditions pass, conditionally mark the exact submitted token used.
5. Require that token UPDATE row count equals exactly 1.
6. Update the exact account’s password hash and timestamp; require exactly 1 row.
7. Increment that account’s epoch by one in SQL; require exactly 1 row.
8. Supersede every other still-active RESET token for that account.
9. Commit only after all steps succeed.
10. Return account\_id only after confirmed COMMIT success.

No trusted Stage-A eligibility flag, nested transaction or call to a public method that independently owns another `_write()` transaction is permitted.

Strictly necessary private cursor-level factoring is allowed only if it never begins, commits or rolls back transactions and preserves unrelated public behavior.

### 8. F-02 — classification corrected by D-05

#### A. Ordinary ineligibility / normal concurrent loser

If Stage B’s initial authoritative revalidation observes an already-used, expired, superseded, wrong-type or otherwise ineligible token/account **before mutation**:

- Return no account\_id.
- Perform zero mutation by this request.
- Return generic invalid-token HTTP 400.
- Do not deliberately clear the browser session.
- Do not reveal which check failed.

A normal concurrent same-token loser must follow this branch.

#### B. Unexpected conditional UPDATE after eligibility passed

After eligibility was established inside the transaction, if the exact submitted-token conditional UPDATE affects anything other than one row:

- Classify it as an **invariant/operational failure**.
- Roll back.
- Return generic HTTP 503.
- Report the unexpected row-count evidence in the technical return.
- Disclose no sensitive details at the web boundary.

Do not normalize this branch into an ordinary concurrent loser.

Password or epoch UPDATE row counts other than one are also invariant/operational failures requiring rollback and generic 503.

### 9. F-02 — rollback, COMMIT and success

For every pre-COMMIT mutation exception or invariant failure:

- Roll back the complete transaction.
- Report no reset success.
- Return generic HTTP 503.
- Do not deliberately clear the browser session.
- Establish unchanged submitted-token `used_at`, password hash, epoch and other reset-token states.

On COMMIT exception:

1. Never report success.
2. Inspect whether the connection remains in a transaction.
3. If so, attempt defensive rollback.
4. Preserve the original COMMIT failure.
5. Return generic HTTP 503.
6. Do not deliberately clear/rewrite local session material.
7. Do not guarantee continued authentication if the epoch may have committed.
8. Classify final durable state as confirmed unchanged, confirmed committed or indeterminate.
9. Do not automatically retry or blindly reuse an unsafe connection.

Do not claim universal rollback guarantees for physical storage/COMMIT failures. If required deterministic rollback/identity evidence cannot be established, STOP the candidate lifecycle and disclose the limitation.

After confirmed successful COMMIT:

- Submitted token consumed.
- Password replaced once.
- Epoch incremented once.
- Other active RESET tokens superseded.
- Previous authenticated sessions invalidated.
- No automatic sign-in.
- Success response permitted.

### 10. Shared `_write()` hardening — retained Option A

`_write()` remains the single transaction owner. No parallel F-02 transaction mechanism is introduced.

Required behavior:

1. Acquire the existing lock and execute `BEGIN IMMEDIATE`.
2. Yield the connection.
3. On body exception, attempt rollback if still in a transaction and propagate failure.
4. On body success, attempt COMMIT.
5. On COMMIT exception, attempt rollback if still in a transaction; never report success.
6. If rollback also fails, retain the original failure, propagate operational failure and treat the connection as unsafe for blind continuation.
7. Do not silently retry BEGIN, mutations, COMMIT or rollback.
8. Do not expose sensitive database details at the web boundary.

Final durable certainty must be reported honestly.

### 11. F-02 — separate acceptance tests

#### Resource and precheck tests

For random invalid, expired, replayed, wrong-type, missing-account, disabled-account and deleted-account tokens, prove:

- No password-hashing invocation.
- Zero durable mutation.
- Identical generic ordinary-ineligibility behavior.

For operational precheck failure, prove no hashing, zero intentional mutation and generic 503.

#### Two-stage and TOCTOU tests

Prove:

- Eligible precheck permits hashing.
- Hashing occurs outside any active AccountStore write transaction and before Stage B’s `BEGIN IMMEDIATE`.
- Stage B does not trust a precheck flag.
- Consumption, expiry, supersession or account ineligibility between stages is caught by initial in-transaction revalidation, yielding generic 400 with zero mutation by the losing request.
- Every token/account condition is independently checked inside Stage B.

#### Mutation and row-count tests

Inject failures:

- Immediately after submitted-token consumption.
- Immediately after password update.
- Immediately after epoch increment.
- During other-token supersession.
- At unexpected token, password and epoch UPDATE row counts.

For each pre-COMMIT operational failure prove complete rollback, generic 503, no success and no deliberate session clearing.

**D-05 branches must be tested independently:**

- Initial in-transaction ineligibility → 400, no mutation.
- Post-eligibility unexpected token UPDATE row count → rollback, 503, invariant evidence.

#### COMMIT tests

Prove:

- COMMIT exception cannot report success.
- Rollback is attempted when the connection remains transactional.
- Rollback failure does not become success or erase the original failure.
- No blind retry occurs.
- Transaction/connection state is inspected.
- Confirmed rollback is claimed only when established.
- Indeterminate durable state is explicitly labeled.
- Local session-material preservation is not treated as proof of authentication.

#### Concurrency, replay and successful reset

Two competing same-token requests must show:

- Exactly one confirmed successful commit.
- The loser rejected by initial in-transaction eligibility revalidation **before mutation**.
- No normalization of unexpected post-eligibility row counts.
- One password replacement and one epoch increment.
- Other reset tokens superseded.
- Replay causes zero additional mutation.
- Old password rejected; new password accepted.
- Existing sessions revoked.
- No automatic sign-in.

Existing password-policy and confirmation tests remain required.

Failure injection must introduce no production-visible endpoint, environment switch, persistent hook or schema field.

### 12. Exact change boundary

Only after separate implementation authorization, changes may occur in:

1. `web/app.py`
2. `engine/account_store.py`
3. `tests/test_p5_1_account_credential_foundation.py`
4. `tests/test_p5_2_auth_sessions_verification_recovery.py`

Allowed effects are limited to F-01 handling, exact epoch row-count proof, reset precheck/hash placement, atomic reset completion, shared `_write()` hardening and their bounded tests.

If a demonstrable test dependency cannot be satisfied within the two test files: STOP and return the exact additional path, dependency, insufficiency of current paths and proposed change. No additional path is automatically authorized.

### 13. Forbidden changes

No:

- Schema/migration, account/session/token-format, password-policy, scrypt-parameter or TTL changes.
- CSRF redesign, email-provider/proxy change, template/catalogue expansion or new public API.
- Project ownership, `owner=NULL`, anonymous-project or claim/backfill changes.
- Commercial, subscription or AI activation.
- Deployment/infrastructure or worker/thread-topology changes.
- Dependency or governance-document edits.
- Unrelated cleanup/refactoring, automatic transaction retries or production fault controls.
- Branch, commit, publication, PR or merge under this packet.

### 14. Dependency-bounded transitive sweep

Because `_write()` is shared, enumerate every AccountStore caller and classify it as:

- Behaviorally unaffected.
- Receiving safer COMMIT-failure propagation only.
- Materially affected.

Verify:

- No caller depends on suppressed COMMIT failure or unsafe continuation.
- Existing BEGIN/body-exception behavior and transaction ownership remain sound.
- No nested transaction is introduced.
- Registration, account status, verification, token issuance/consumption, rate-limit atomicity and commercial-assignment storage preserve existing behavior.
- All epoch, password and reset-token callers are inspected.
- Authentication validation, account deactivation, login, reset replay and concurrency remain correct.

Run relevant targeted tests, the complete suite because the helper is shared, and Universal Guardrail Smoke.

Outside the four paths the sweep is read-only. Necessary out-of-scope corrections require STOP and Owner disposition.

### 15. Preserved states

- F-03: OPEN — separate Owner product-decision gate.
- Project ownership, `owner=NULL`, anonymous behavior and claim/backfill: unchanged.
- R-05 CSRF and F-04 `_answer_error`: retained for their later gates.
- R-06 scaling, R-07 commercial reachability and R-09 AI path: unchanged; no activation.
- G-4-A: CURRENT — NOT FIXED; direct remediation DEFERRED — NOT CANCELLED.
- CEHR/Route-B: preserved.
- T1-A′, HICR, readiness and RUN-004: existing authorities and return gates preserved.
- PRE-FCORA: MANDATORY LATER — NOT STARTED.
- FCORA, human study/recruitment/collection, pilot, production, deployment and paid activation: NOT AUTHORIZED.
- OSP closure is not reopened.

**SILENT STATUS CHANGE: 0 REQUIRED.**

### 16. Future Creator evidence return

One complete package must include:

- Verified starting branch/SHA and worktree disclosure.
- Exact paths, complete diff, diff SHA-256/bytes and `git diff --check`.
- Candidate SHA, sole parent, tree, file count and additions/deletions when separately authorized.
- Separate F-01 and F-02 outputs.
- Resource/hash-invocation and outside-transaction evidence.
- TOCTOU, rollback, COMMIT, concurrency and replay outputs.
- Independent proof of both D-05 branches.
- Failure matrix with pre/post durable state.
- Separate session-material handling, authenticated validity and durable-certainty classifications.
- `_write()` caller inventory and transitive-sweep results.
- Targeted tests, full suite and Smoke raw outputs.
- Forbidden-change and preserved-state attestations.
- Final worktree and publication/PR/merge status.
- All deviations, limitations and indeterminate outcomes.

Creator evidence is not Lead acceptance, independent-review PASS, Owner exact-SHA acceptance or publication/PR/merge authority.

### 17. STOP conditions

STOP for:

- Base mismatch or authority/provenance conflict.
- Defect no longer reproducible.
- Mutating/reserving Stage A.
- Hashing initially ineligible tokens or hashing inside the writer transaction.
- Stage-B reliance on precheck truth or incomplete transactional revalidation.
- Nested transactions or inability to contain all reset mutations in one transaction.
- Out-of-scope production/test dependency.
- COMMIT failure reported as success, blind retry or unsafe connection reuse.
- Treating local session preservation as authentication proof.
- Treating post-eligibility unexpected token row count as an ordinary concurrent loser.
- Missing deterministic required evidence, material regression or weakened security invariant.
- Required schema/product/ownership/public-surface decision.
- Any review-invalidating contradiction.

No improvisation, silent substitution or adjacent repair.

### 18. Lifecycle and Owner decision requested

This packet seeks **contract approval only**.

After approval:

1. Record the exact Owner decisions.
2. Obtain separate implementation authority before releasing an executable instruction.
3. Prepare one final Creator instruction and complete OSP MC-01–MC-18; MC-18 PASS required before send.
4. Creator performs only authorized work and returns evidence.
5. Lead performs identity, differential and invariant review.
6. Bounded independent security review examines F-01/F-02 and materially affected shared-helper invariants.
7. Lead final adjudication.
8. Separate Owner exact-SHA, publication, PR and merge decisions.

No additional broad review is required.

**Requested approval covers all retained v2.0 decisions, with these controlling corrections:**

- **D-04:** distinguish preserved local browser-session material from actual authenticated validity, using confirmed-rollback versus committed/indeterminate failure semantics.
- **D-05:** initial transactional ineligibility is generic 400; unexpected submitted-token UPDATE row count after eligibility passed is rollback plus generic 503.

```text
PACKET VERSION:
2.1

OWNER APPROVAL:
PENDING

IMPLEMENTATION AUTHORIZATION:
NO

CREATOR INSTRUCTION:
NOT AUTHORIZED

BRANCH / COMMIT / PUBLICATION / PR / MERGE:
NOT AUTHORIZED

END OWNER DECISION PACKET
```
<!-- END APPROVED V2.1 PACKET: preceding framing LF excluded from packet bytes -->
