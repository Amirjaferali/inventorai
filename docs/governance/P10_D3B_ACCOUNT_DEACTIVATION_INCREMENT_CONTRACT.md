# P10-D3b — Account Deactivation — Bounded Increment Contract (definition only)

**Status:** GOVERNANCE-ONLY CANDIDATE. This contract **authorizes no implementation**. Its sole purpose is to
fix the exact future implementation boundary for `P10-D3b — Account Deactivation` so a later,
separately-authorized implementation gate has a frozen, evidence-grounded target.

**Phase:** 10 — Commercial, Legal, Security and Operational Readiness.
**Governing phase-entry contract:**
`docs/governance/PHASE_10_COMMERCIAL_LEGAL_SECURITY_OPERATIONAL_READINESS_P10C_CONTRACT.md` (merged PR #508,
authoritative). Subordinate to it and to every anchor above it in `CLAUDE.md`'s reading order.
**Authoritative base at drafting:** `d649a4df5889cf037096014ce69d362adb2fb00b` (PR #511 merge —
`P10-D3a — Self-Service Project Export` implementation, authoritative; independently re-verified: first parent
`1a87bf58b892b2924a91727a7b3fc4425d909db7`, second parent `4c5f325fb20ce0ecf508d1ebce8b38ed9dc83262`, tree
`acd8c16ab3012904505d6c5be31255f51595bd09`, empty candidate→merge diff).

**Selection lineage.** The Independent External Reviewer's split of the original combined `P10-D3` proposal
(export and deactivation must be separate increments, each behind its own committed contract) produced
`P10-D3a` (now merged and implemented) and this `P10-D3b`. This contract is the second half of that split,
created under explicit Owner authorization for this governance-candidate session only.

---

## §1. Objective — and what this gate truthfully is

Define the boundary for ONE self-service account state transition — **Deactivate Account** — for a currently
authenticated account.

**This gate is technically truthful about what it is NOT:**

* It is **NOT physical deletion** — no row in any table is removed.
* It is **NOT account-data erasure** — every durable byte remains present.
* It is **NOT retention cleanup** — no retention policy is defined, changed, or implied.
* It is **NOT legal "right to erasure" compliance** — no legal claim of any kind is made.

What it IS: the existing bounded store primitive `set_status(account_id, "deleted", now_iso)` finally gains a
reachable, self-service, authenticated trigger, and the already-existing status-gated denial machinery does the
rest.

---

## §2. Verified runtime facts (each re-verified at base `d649a4d`, not carried from memory)

**F-1 — Store primitive.** `engine/account_store.py::set_status(account_id, status, now_iso)` exists. It
validates `status` against `ACCOUNT_STATUSES = frozenset({"active", "disabled", "deleted"})` (raising
`AccountStoreError` otherwise), and executes exactly one `UPDATE accounts SET status = ?, deleted_at = ?,
updated_at = ? WHERE account_id = ?`. `deleted_at` is stamped with `now_iso` when the new status is `"deleted"`
and cleared to NULL otherwise. **No other column is touched; no row is deleted.** Its own docstring records it
as a "Bounded lifecycle primitive (no public admin route in P5-2)".

**F-2 — Web session invalidation is status-driven and already fail-closed.**
`engine/auth_session.py::validate_session` returns `(False, "inactive")` whenever
`account.get("status") != "active"`, and `web/app.py::_current_account()` responds to ANY failed validation by
popping the auth session and returning `None`. Consequence: the moment an account's status is `"deleted"`,
**every** session of that account — current browser and all others — fails closed on its very next request.
Status is the **primary** invalidation mechanism; no new session infrastructure is needed.

**F-3 — Login is status-gated.** `web/app.py::login_submit` accepts "only an active account with a correct
password": `if account is None or account["status"] != "active" or not password_ok: → identical generic 401`.
A deactivated account cannot sign back in, and the denial is the same non-enumerating failure as a wrong
password.

**F-4 — API credentials of a non-active account already fail.** `web/api_v1.py::_authenticate` checks, after
credential verification: `account = store.get_account_by_id(row["owner_account_id"]); if account is None or
account["status"] != "active": → generic denied_unauthenticated` (its own comment: "canonical account
semantics: only an ACTIVE bound account authenticates"). **Explicit per-credential revocation is therefore NOT
technically required for deactivation to cut API access** — it would be defense-in-depth only, and this gate
does not add it (§6.5).

**F-5 — Session-epoch primitive exists.** `engine/account_store.py::increment_session_epoch` atomically bumps
`accounts.session_epoch`; `validate_session` rejects any session whose epoch mismatches (`epoch_mismatch`).
`web/app.py::logout_all` is the existing consumer precedent.

**F-6 — Password re-verification helper exists.** `engine/account_credentials.py::verify_password(
password_hash, password)` — the same Werkzeug-scrypt check used by login. No second password subsystem is
needed.

**F-7 — CSRF pattern exists and is the account-mutation norm.** `web/app.py::_csrf_valid()` (constant-time via
`_auth.csrf_matches`) and `_csrf_reject()` (generic 403) guard the existing authenticated POSTs `/logout`,
`/logout-all`, and `/account/resend-verification`; `web/templates/account.html` posts the hidden `csrf_token`
field on each. The deactivation POST must reuse exactly this pattern.

**F-8 — No physical-deletion path exists to accidentally invoke.** The ONLY `DELETE FROM` statement in the
entire `engine/` tree is `cleanup_expired_rate_limits` (`auth_rate_limits` rows only). No code path deletes
accounts, projects, records, tokens, credentials, commercial, subscription, provider, or audit rows.

**Stop-condition sweep result:** all nine registered stop conditions (§10) were probed against these facts at
the base tip; **none is triggered**. In particular: `"deleted"` status DOES block web auth (F-2, F-3); API
credentials DO fail for a non-active account (F-4); password verification and CSRF ARE safely reusable (F-6,
F-7); no schema change and no physical deletion are needed (F-1, F-8).

---

## §3. Exact scope of the future implementation

**In scope, and nothing else:**

* **S-1.** One new route in `web/app.py`: `POST /account/deactivate` (or the nearest repository-consistent
  equivalent under `/account/`). **POST only** — no GET mutation, no query-param mutation.
* **S-2.** Guard order follows the existing `logout_all` precedent: authenticated `_current_account()` required
  (anonymous → redirect to login, no mutation); then `_csrf_valid()` required (failure → `_csrf_reject()`, no
  mutation); then **password re-entry** verified via the existing `verify_password` against the live account's
  `password_hash` (wrong password → safe generic failure, **no state change**).
* **S-3.** On success, exactly two store calls, both existing primitives consumed unmodified:
  1. `set_status(account_id, "deleted", now_iso)` — status transition + `deleted_at` stamp (F-1);
  2. `increment_session_epoch(account_id, now_iso)` — **defense-in-depth** revocation (F-5). Status is already
     the sufficient primary mechanism (F-2); the epoch bump is required here because it is one existing call
     that also hardens against any future code path that might check epoch before status, at zero new
     infrastructure cost.
  Then clear the Flask session (preserving `ui_lang`, per the `logout_all` precedent) and redirect to a
  non-authenticated page with a truthful notice.
* **S-4.** Wrong password, missing CSRF, and invalid CSRF each leave the account row byte-identical (status,
  `deleted_at`, `session_epoch`, `updated_at` all unchanged).
* **S-5.** Unexpected internal failure **fails closed**: no traceback, exception text, or internal identifier
  reaches the response, and no success notice is shown unless `set_status` actually succeeded. A failure after
  `set_status` but before the redirect must NOT claim failure-with-rollback — the truthful outcome is that the
  account is deactivated and the next request will confirm it (F-2 makes this self-healing).
* **S-6.** One entry-point control on the existing `/account` page: a password-input + submit form posting to
  the new route with the hidden `csrf_token`, using the existing `t(...)` i18n seam.
* **S-7.** New UI strings in `web/ui_text.py` with **both** `en` and `ar` variants.

**Allowed paths (exhaustive):** `web/app.py`, `web/ui_text.py`, `web/templates/account.html` (and, only if a
truthful post-deactivation notice needs one, an existing non-authenticated template), and new/updated files
under `tests/`.
**Forbidden paths (non-exhaustive but binding):** `engine/account_store.py`, `engine/auth_session.py`,
`engine/account_credentials.py`, `engine/record_store.py`, `engine/read_export_service.py`, `web/api_v1.py`,
`database/`, `schemas/`, any migration, any dependency manifest, any CI configuration.

---

## §4. Truthful user-facing label (binding)

**Required concept:** `Deactivate Account`.
**Arabic:** technically equivalent wording such as `تعطيل الحساب` ("disable/deactivate the account"). The
Arabic MUST NOT imply erasure or deletion of data.

**Prohibited wording** — in `en` and `ar` alike, in labels, buttons, notices, confirmations, and help text:

* `Delete Account` / `حذف الحساب`
* `Erase Account Data` / `مسح بيانات الحساب`
* `Delete All My Data` / `حذف كل بياناتي`
* `Right to Erasure`, `permanent data deletion`, or any data-portability/subject-access legal framing.

**Rationale (factual, not legal):** the operation changes one status column and stamps one timestamp. Every
durable row remains physically present (§7). Wording that implies erasure would be untrue. Any confirmation
copy shown to the user may truthfully state that the account is deactivated and sign-in is disabled; it must
not state that data has been deleted.

---

## §5. Success / failure semantics (the acceptance surface)

| Case | State change | Response |
|---|---|---|
| Anonymous caller | none | redirect to login (existing pattern) |
| Missing/invalid CSRF | none | `_csrf_reject()` — generic 403, fail closed |
| Wrong password | none | safe generic failure; no enumeration of why |
| Correct password + valid CSRF | status → `"deleted"`, `deleted_at` stamped, epoch bumped, session cleared | truthful non-erasure notice; signed out |
| Unexpected internal failure | fail closed | generic failure; no traceback; no partial-success claim |

After success: the current session is unusable (F-2 + cleared cookie), every other session is unusable (F-2;
epoch bump as belt-and-braces), future login is denied with the generic 401 (F-3), and every API credential
owned by the account stops authenticating (F-4). All of these are enforced by EXISTING code paths that this
gate consumes, not by new enforcement logic.

---

## §6. Architecture constraints

**§6.1 — Consume, never duplicate.** The route is glue over `_current_account()`, `_csrf_valid()`,
`verify_password`, `set_status`, and `increment_session_epoch`. No second password-validation subsystem, no
second CSRF system, no new session infrastructure, no new store method.

**§6.2 — Status vocabulary unchanged.** The transition targets the EXISTING `"deleted"` status value (F-1).
No new status value, and no reinterpretation of `"disabled"` (which remains a distinct, untouched state).

**§6.3 — No schema/persistence change.** No DDL, no migration, no new table/column/index.

**§6.4 — No reactivation path.** This gate defines deactivation only. No un-delete, restore, or grace-period
mechanism is defined or implied; any such capability would be a separate future gate. (The store primitive can
technically set status back to `"active"`, clearing `deleted_at`; this gate deliberately exposes no route to
it.)

**§6.5 — No per-credential revocation.** F-4 proves credentials of a non-active account already fail closed at
authentication. Calling `revoke_api_credential` per credential is therefore NOT required and is excluded — it
would add write-fanout without changing observable behavior. If future evidence contradicts F-4, that is
stop-condition 2, not a license to add revocation silently.

**§6.6 — No `access_audit` write and no audit/append-only touch.** Identical posture to P10-D3a §6.4: no
browser-surface `access_audit` event; `subscription_lifecycle_events`, `commercial_audit`,
`provider_event_dedupe`, and `access_audit` are neither written, deleted, nor reinterpreted. The Phase-7 §25
disposition is consumed as current fact only — not reopened, reclassified, or rewritten. The resulting absence
of a deactivation audit event is recorded as a deliberate, truthful limitation of this bounded gate.

**§6.7 — Non-enumeration preserved.** The wrong-password failure must not reveal anything a failed login would
not reveal. The generic-401 login behavior for a deactivated account (F-3) must remain byte-identical to the
wrong-password case — this gate must not add any "this account was deactivated" disclosure to login.

---

## §7. Data preservation (binding, explicit)

P10-D3b does **NOT** delete, truncate, or rewrite any row in any of these tables — after deactivation every one
of them remains physically present exactly as before, except the single `accounts` row's `status`,
`deleted_at`, `updated_at`, and `session_epoch` columns:

`accounts` (row preserved; columns above updated) · `projects` · `records` · `email_tokens` ·
`api_credentials` · `commercial_assignments` · `commercial_audit` · `commercial_usage` ·
`commercial_usage_idempotency` · `subscription_lifecycle_events` · `subscription_lifecycle_state` ·
`provider_mapping` · `provider_event_dedupe` · `access_audit`.

**No claim is made about how long any of these must or should be retained.** Retention is a separate,
unaddressed question outside this gate's authority.

---

## §8. Explicit exclusions

P10-D3b does **not** include, and any implementation drifting into these must STOP (§10):

* Physical deletion or purge of any row; project deletion; record deletion.
* Account-wide export, or ANY change to P10-D3a's export surface.
* Retention cleanup of any kind.
* Email/notification provider work (no deactivation email).
* API credential issuance or revocation (§6.5).
* Commercial / subscription / provider remediation of any kind.
* Reactivation / restore / grace-period mechanics (§6.4).
* Legal or privacy drafting; any GDPR / Kuwait-PDPL / statutory-retention / consent / erasure determination.
* PSRR execution; deployment; production activation.

---

## §9. Required tests for the future implementation (RED → GREEN; not written now)

1. Anonymous caller cannot deactivate (no state change).
2. Authenticated account with wrong password cannot deactivate (account row byte-unchanged).
3. Missing CSRF token cannot deactivate (fail closed, no state change).
4. Invalid CSRF token cannot deactivate (fail closed, no state change).
5. Correct password + valid CSRF deactivates.
6. The `accounts` row remains physically present after deactivation.
7. `status` becomes exactly `"deleted"`.
8. `deleted_at` is stamped (non-NULL).
9. The current session is unusable after success.
10. Another pre-existing session of the same account is unusable after success.
11. Future login with the correct password is denied, byte-identical to the generic wrong-password 401.
12. An existing API credential owned by the account can no longer authenticate on the P7-I2 surface.
13. Owned projects remain physically present (row count unchanged).
14. Owned records remain physically present (row count unchanged).
15. No append-only/audit row is deleted (`subscription_lifecycle_events`, `commercial_audit`,
    `provider_event_dedupe`, `access_audit` counts unchanged).
16. The EN label is `Deactivate Account` (or approved equivalent) and no §4-prohibited EN phrase appears.
17. The AR label is technically equivalent (e.g. `تعطيل الحساب`) and no §4-prohibited AR phrase appears.
18. Unexpected internal failure is fail-closed: no traceback/internal detail, no false success notice.
19. Full relevant regressions green — at minimum the P5-2 auth/session suite, P5-3 ownership suite, P7-I2
    public-API suite, P10-D3a export suite, and UI/i18n suites.
20. Full repository suite green.
21. `git diff --check` clean.

---

## §10. Stop conditions for the future implementation

Implementation must **STOP and report** — not work around — if fresh repository truth shows:

1. The `"deleted"` status does not actually block web authentication. *(Current evidence: F-2/F-3 — not
   triggered.)*
2. API credentials remain usable for a non-active account. *(Current evidence: F-4 — not triggered.)*
3. Existing password verification cannot be safely reused. *(F-6 — not triggered.)*
4. The existing CSRF pattern cannot be reused. *(F-7 — not triggered.)*
5. Deactivation appears to require physical deletion for correctness.
6. A schema change appears required.
7. A legal or policy determination becomes necessary to proceed.
8. Append-only history would have to be mutated.
9. The route's real semantics can no longer be truthfully described as "Deactivate Account".

---

## §11. Completion criteria for **this contract** (the governance gate only)

This gate is complete when this document is created, frozen at an exact SHA, Creator-Grilled, bundled
SHA-preservingly, independently reviewed, Owner-accepted at that exact SHA, published, and post-merge verified.
It delivers **a definition only** — no route, no test, no runtime change.

---

## §12. Governance and authorization boundary (binding, explicit)

* **Creating or merging this contract does NOT authorize runtime implementation.** Implementation requires a
  separate, explicit Owner authorization naming the P10-D3b implementation gate.
* **No automatic successor.** Closing this contract activates nothing — no `P10-D3c`, no reactivation gate, no
  other Phase-10 finding. This matches the P10-C §10 gate-selection rule.
* **No PSRR trigger.** PSRR remains consumed within Phase-10 ownership, triggered before first public
  production deployment — untouched here.
* **No deployment authority.** `OD-P`'s separate deployment gate and explicit Owner deployment authorization
  both remain independently required and unsatisfied.
* **No physical-deletion authority.** Nothing in this contract creates, implies, or schedules authority to
  physically delete any data, now or later.
* **Phase-7 §25 preserved** (§6.6). `OWNER_DECISION_REGISTER.md` is UNCHANGED. No Level-0 / product-identity /
  security-boundary / phase-sequencing change; no active hold is moved.
* **Zero runtime diff in this candidate.** This candidate touches only `docs/governance/`.

---

## §13. Governance truth sweep (performed at base `d649a4d` before freezing)

Classification of every material claim:

| Claim | Class | Evidence |
|---|---|---|
| `set_status` semantics (statuses, `deleted_at`, columns, no DELETE) | supported current fact | `engine/account_store.py` read at tip |
| `validate_session` "inactive" fail-closed + `_current_account` pop | supported current fact | `engine/auth_session.py`, `web/app.py` read at tip |
| Login requires `status == "active"`, generic 401 | supported current fact | `web/app.py::login_submit` read at tip |
| API auth requires bound account `status == "active"` | supported current fact | `web/api_v1.py::_authenticate` lines read at tip |
| `increment_session_epoch` exists; `logout_all` consumes it | supported current fact | store + route read at tip |
| `verify_password` reusable | supported current fact | `engine/account_credentials.py` read at tip |
| CSRF helpers + account-POST precedent | supported current fact | `_csrf_valid`/`_csrf_reject` + 3 routes + template read at tip |
| Only `DELETE FROM` in engine is rate-limit cleanup | supported current fact | full-tree grep at tip |
| `set_status` had no public route before this gate | supported current fact | its docstring + route grep |
| P10-D3a merged/authoritative at `d649a4d` | supported current fact | merge identity independently re-verified this session |
| Epoch bump is defense-in-depth, not primary | bounded derived conclusion | derived from F-2 (status checked before epoch in `validate_session`) |
| Credential revocation unnecessary | bounded derived conclusion | derived from F-4; guarded by stop-condition 2 |
| Phase-7 §25 `access_audit` disposition deferred | supported historical fact | consumed only; not restated as new work |

**Result:** no material unsupported or stale current-state claim. Statements not verifiable as fact are marked
as bounded derived conclusions with their evidence and guarding stop conditions.
