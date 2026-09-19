# Data Retention Policy
Status: APPROVED (truth-labeled per P10-DOC1 — every statement below is classified;
this document records what EXISTS and what is OPEN; it creates no new retention rule)

```
RETENTION POLICY SUBSTANCE: OPEN — EXTERNAL LEGAL/TAX INPUT REQUIRED
```

No retention duration, deletion deadline, or erasure schedule is decided by this document.
Substantive retention/erasure rules await the open external legal/tax input (P10-LT1 registers,
notably LQ-09/LQ-10/TQ-07) and separate Owner acceptance.

## Data Inventory — CURRENT (verified against source)

| Data | Where it actually lives | Sensitive |
|---|---|---|
| Account identity (opaque id, normalized email, scrypt password hash, status, timestamps) | Durable SQLite (`accounts`, via `INVENTORAI_DB_PATH`) | YES |
| Email verification / password-reset tokens | Durable SQLite (`email_tokens`) — HASH only, never raw | YES |
| API credentials | Durable SQLite (`api_credentials`) — hashed secret only | YES |
| Auth sessions | Signed cookie (client) + server-side epoch/idle/absolute checks; no session rows | YES |
| Projects / records (user invention content) | Durable SQLite (`projects`, `records`) | YES |
| Audit / commercial scaffolding (`access_audit`, `commercial_audit`, lifecycle, dedupe, usage) | Durable SQLite, append-only; NO live billing data | Partly |
| Auth rate-limit counters | Durable SQLite (`auth_rate_limits`) — privacy-digest keys, no raw email | NO |
| Outbound email outbox (OD-INFRA-6) | Durable SQLite (`email_outbox`) — recipient address + token-bearing verification/reset body, TRANSIENT: deleted on confirmed provider acceptance, scrubbed (recipient/subject/body nulled) when the bounded retry budget is exhausted; never logged, never exported | YES (while pending) |
| Off-provider backup scheduler state (OD-INFRA-5) | Durable SQLite (`offsite_backup_state`) — one row: timestamps, the owning run's claim id, a consecutive-failure counter, a stable failure code, and the last stored object's key, byte count and SHA-256; no credential, no user data | NO |
| Live progression-session working state | In-memory `SESSION_STORE` (web/app.py) — ephemeral; durable evidence appended to `records` | YES |
| Browser draft text | Client-side `localStorage` ONLY (never server-held) | YES (client-only) |
| Operational logs (P10-OB1) | Process stderr stream, bounded no-PII events; NOT retained as files | NO |
| Benchmark fixtures | `tests/replay/cases/` (git-controlled) | NO |

HISTORICAL — SUPERSEDED: the previous inventory ("Invention descriptions / responses / session
state: In-memory session store"; "Audit logs: Log files") predates durable SQLite persistence
(P4-1b), accounts (P5), the durable audit tables, and the P10-OB1 stream-only operational logging.

## What actually happens to data today — CURRENT

* Durable SQLite data is retained **indefinitely**: NO enforced server-side retention lifecycle,
  NO automatic expiry, and NO physical-erasure capability exists (OD-DR1: erasure DEFERRED pending
  external legal determination + separate Owner authorization).
* Account exit is **Deactivation only** (P10-D3b): a status tombstone that blocks all use but
  removes no row. DEACTIVATION ≠ PHYSICAL DELETION.
* The ONLY automatic deletions anywhere are two operational cleanups, neither of which touches
  user content or account data: bounded cleanup of **expired auth rate-limit rows**
  (`cleanup_expired_rate_limits` — operational counters), and — SUPERSEDED IN PART (was: the
  rate-limit cleanup alone) under OD-INFRA-6 — removal of a **delivered outbound email message**
  from the `email_outbox` table the moment the provider confirms acceptance
  (`mark_email_delivered`). The outbox row is a transient carrier for a token-bearing message;
  deleting it promptly is operational message cleanup and decides no user-data retention rule.
* Browser drafts expire client-side after a 7-day lazy TTL (`web/static/js/local_draft.js`,
  `TTL_MS = 7 days`) — a client mechanism, not a server retention rule.
* Self-service export is project-scoped only (P10-D3a); account-wide export DEFERRED (OD-DR2).
* Local backups (P10-BR1) are byte-consistent copies of the durable database: they inherit all
  data above and have NO retention/rotation schedule. SUPERSEDED IN PART (was: "NO offsite/
  production backup exists"): an off-provider upload CAPABILITY to Cloudflare R2 now exists
  (OD-INFRA-5, `scripts/inventorai_offsite_backup.py`). SUPERSEDED IN PART (was: "It is not
  activated by the repository"): when the `INVENTORAI_R2_*` configuration is complete, the ONE
  bounded in-process scheduler (`engine/offsite_backup_scheduler.py`) runs that upload
  approximately once per 24 hours from the production web-service process; the bucket and the
  credential are still created outside the repository. It inherits exactly the same data, and
  it has NO retention, expiry or deletion path — so each uploaded copy persists, and copies
  accumulate daily, until a retention decision exists. That decision is still OPEN in this
  lane; nothing here decides it. Any future erasure obligation would have to reach these copies
  too, which is an additional reason the substance below remains adviser-open.

## What does NOT exist — CURRENT

* No comprehensive server-side automatic retention lifecycle.
* No account-wide physical erasure path (and none is promised here).
* No finalized audit-record retention (the `access_audit` lifecycle is an open PSRR-tracked
  operational observation).
* No finalized backup retention.
* No legally approved retention periods of any kind.
* No log files with retention tiers (the historical "DEBUG 7 days / INFO 30 / AUDIT 365" schedule
  was never implemented and is HISTORICAL — SUPERSEDED; no such rule is in force).

## Privacy — CURRENT

1. Invention descriptions are the user's intellectual property and must not be used for
   retraining (standing product commitment).
2. HISTORICAL — SUPERSEDED: "Anthropic API receives descriptions." NO live external transfer
   exists: AI advisory transfer is disabled in code (`engine/ai_advisor.py`,
   `AI_ADVISORY_ENABLED = False`; the dormant call path is unreachable without a source change),
   and no payment/webhook/analytics/telemetry transfer exists. Email: SUPERSEDED IN PART (was:
   "email runs to an in-memory development sink only") — development/test still use that sink,
   and production now uses either a sender that cannot deliver at all or, when OD-INFRA-6 is
   fully configured, the Resend HTTPS API. When configured, a transactional message (recipient
   address, subject, and a verification/reset link) IS transferred to that provider; the
   conclusion above is unchanged for every other data class, and no invention/project content
   is ever included in such a message.
3. HISTORICAL — SUPERSEDED: "No PII collected in MVP." Accounts exist and store personal data
   (normalized email + identity). The condition in "GDPR/PDPL review required before adding
   accounts" has therefore FIRED: that review is commissioned as external questions LQ-04…LQ-11
   under the merged P10-LT1 gate and is `OPEN — EXTERNAL ADVISER REQUIRED`. No applicability
   conclusion is made here.

## Open items (not decided here)

Personal-data retention durations; erasure obligations and scope (including backups); audit and
financial/tax record retention; data-subject request procedures/timelines. All are
`OPEN — EXTERNAL ADVISER REQUIRED` (P10-LT1 LQ/TQ registers), then Owner acceptance.
