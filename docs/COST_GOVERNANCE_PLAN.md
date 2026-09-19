# Cost Governance Plan
Status: APPROVED (truth-labeled per P10-DOC1 — sections classified; nothing in a
PLANNED / NOT IMPLEMENTED section is an active control)

## Current cost reality — CURRENT (verified against source)

* **SUPERSEDED IN PART — v1.32 current-state correction (2026-09-19). Read this first.**
  The prior bullet claimed, verbatim and in full: *"There is NO live paid usage of any kind: AI
  advisory transfer is disabled in code (`engine/ai_advisor.py`, `AI_ADVISORY_ENABLED = False` —
  the dormant Anthropic call path is unreachable without a source change and configures no API
  key); email runs to an in-memory development sink; there is no payment provider, no live
  billing, no hosted monitoring, no offsite backup provider, and no production hosting/cloud
  infrastructure."* That is **no longer true as a whole**, and the false half is named here
  rather than quietly deleted.
* **Still true, verified against source:** AI advisory transfer remains disabled in code —
  `engine/ai_advisor.py`, `AI_ADVISORY_ENABLED = False`, the dormant Anthropic call path
  unreachable without a source change and configuring no API key — so **AI token spend is zero**.
  There is **no payment provider**, **no live billing of users**, and **no hosted monitoring**.
  Public paid activation remains BLOCKED under `D-P8-PL-01 class C`.
* **No longer true — provider costs now exist and are outside runtime control.** Production
  hosting exists (Render, Frankfurt region, Docker runtime, one non-public web service, one
  persistent disk), an **off-provider backup destination exists** (Cloudflare R2, private bucket,
  under OD-INFRA-5) and holds at least one stored backup object, and **email no longer runs only
  to a development sink** — a Resend adapter, a durable SQLite outbox and one bounded dispatcher
  are merged under OD-INFRA-6, with **live sending activation still deferred to final
  pre-release**. These are ordinary provider charges on the Owner's own accounts. **No usage of
  them is metered, budgeted, capped or alerted on by this repository's runtime code**, and this
  plan claims no such control.
* NO runtime cost control exists: no kill
  switch, no spending ceiling, no cost accumulator, no per-session token budget, no cost alerts.
  (The commercial/subscription tables in `engine/account_store.py` are architectural scaffolding —
  they carry no live billing data; public paid activation remains BLOCKED under
  `D-P8-PL-01 class C`.)

## HISTORICAL — SUPERSEDED / NOT IMPLEMENTED (previous claims, corrected)

The following statements from earlier versions of this plan described controls that were never
implemented, or an AI-usage model that is currently disabled. None is an active control:

* "Kill Switch: INVENTORAI_KILL_SWITCH… web/app.py checks on every request" —
  **NOT IMPLEMENTED** (no such check exists in `web/app.py`; adding one would be a separately
  authorized runtime gate).
* "Max input tokens per call: 4000" / "Max output tokens per call: 1000" —
  **NOT IMPLEMENTED as stated** (the dormant disabled path uses `max_tokens: 150`).
* "Max iterations per session: 15 (progression_loop.py hard stop)" —
  **NOT IMPLEMENTED** (no iteration hard stop exists in `engine/progression_loop.py`).
* "Max session cost USD: 0.25 (ai_advisor.py cumulative check)" —
  **NOT IMPLEMENTED** (no cost accumulator exists).
* Per-session token budgets, monthly budgets (MVP/early-access/growth), and cost alerts
  (daily-spend email, spike auto-pause) — **NOT IMPLEMENTED / MOOT** while no paid usage exists
  (and no email provider exists to deliver an alert).

## PLANNED / NOT IMPLEMENTED — future design input only

If AI advisory transfer or other paid provider usage is ever re-enabled (a separately authorized
gate), cost governance must be re-decided at that gate. The historical structure above (per-call
token caps, per-session budget, cumulative session cost ceiling, monthly budget tiers, spend
alerts, an operational kill switch) is retained as PLANNED design input ONLY — none of it is
active, and re-enabling AI without re-deciding cost controls is prohibited by this plan's intent.

## PROVIDER-DEPENDENT — deferred

**SUPERSEDED IN PART — v1.32.** The prior text read: *"Production infrastructure costs (hosting,
monitoring, backup storage, email delivery, payment processing) do not exist today and are
governed by the future OD-J2-delegated infrastructure gate and later provider gates. No
cloud/provider billing is currently incurred or controlled by runtime code, and no such control
is claimed."*

**Current truth:** hosting and backup-storage costs **do** exist today (OD-INFRA-1 Render /
OD-INFRA-2 Frankfurt / OD-INFRA-5 Cloudflare R2), and an email provider is selected under
OD-INFRA-6 with live sending not yet activated. **Monitoring (OD-INFRA-4) and payment processing
remain unselected and cost nothing.** What has not changed is the part that matters for this
document: **no cloud or provider billing is metered, budgeted, capped, alerted on or otherwise
controlled by runtime code, and no such control is claimed here.** The OD-J2-delegated
infrastructure gate and the later provider gates still govern these decisions; a provisioned
provider is not a decided cost policy, and cost governance must be re-decided at the gate that
enables any metered or paid usage.
