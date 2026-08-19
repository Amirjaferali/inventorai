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
* The ONLY automatic deletion anywhere is bounded cleanup of **expired auth rate-limit rows**
  (`cleanup_expired_rate_limits` — operational counters, not user content).
* Browser drafts expire client-side after a 7-day lazy TTL (`web/static/js/local_draft.js`,
  `TTL_MS = 7 days`) — a client mechanism, not a server retention rule.
* Self-service export is project-scoped only (P10-D3a); account-wide export DEFERRED (OD-DR2).
* Local backups (P10-BR1) are byte-consistent copies of the durable database: they inherit all
  data above, have NO retention/rotation schedule, and NO offsite/production backup exists.

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
   email runs to an in-memory development sink only, and no payment/webhook/analytics/telemetry
   transfer exists.
3. HISTORICAL — SUPERSEDED: "No PII collected in MVP." Accounts exist and store personal data
   (normalized email + identity). The condition in "GDPR/PDPL review required before adding
   accounts" has therefore FIRED: that review is commissioned as external questions LQ-04…LQ-11
   under the merged P10-LT1 gate and is `OPEN — EXTERNAL ADVISER REQUIRED`. No applicability
   conclusion is made here.

## Open items (not decided here)

Personal-data retention durations; erasure obligations and scope (including backups); audit and
financial/tax record retention; data-subject request procedures/timelines. All are
`OPEN — EXTERNAL ADVISER REQUIRED` (P10-LT1 LQ/TQ registers), then Owner acceptance.
