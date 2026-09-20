# Cost Governance Plan
Status: APPROVED (truth-labeled per P10-DOC1 — sections classified; nothing in a
PLANNED / NOT IMPLEMENTED section is an active control)

## Current cost reality — CURRENT (verified against source)

**Only the delimited region below states current truth.** Everything outside it — in this file
or any other — is history, plan or commentary, whatever its formatting, and states nothing about
today. Do not add a current claim outside the markers, and do not quote a past claim inside them.

<!-- CURRENT-TRUTH:COST:BEGIN -->
**Provider costs that DO exist today.** These are ordinary provider charges on the Owner's own
accounts, incurred outside this repository's control:

* **Production hosting exists** — Render, Frankfurt region, Docker runtime, one non-public web
  service, one persistent disk (OD-INFRA-1 / OD-INFRA-2).
* **An off-provider backup destination exists** — Cloudflare R2, private bucket, under
  OD-INFRA-5 — and it holds at least one stored backup object.
* **An email provider and adapter direction exists** — Resend under OD-INFRA-6, with the
  adapter, a durable SQLite outbox and one bounded dispatcher merged.
* **Monitoring rests on the hosting platform's own metrics, logs and `/health`**, at no separate
  charge. This is the selected approach under OD-INFRA-4, not an absence — see below.

**What costs nothing today, verified against source.**

* **AI token spend is zero** — AI advisory transfer is disabled in code
  (`engine/ai_advisor.py`, `AI_ADVISORY_ENABLED = False`); the dormant Anthropic call path is
  unreachable without a source change and configures no API key.
* **Live production email sending remains DEFERRED** to final pre-release and is NOT activated,
  so no send volume is billed. The email retry-budget P1 must be revisited before activation.
* **No payment provider is live** and **no live user billing exists**. The commercial and
  subscription tables in `engine/account_store.py` are architectural scaffolding carrying no live
  billing data. Public paid activation remains BLOCKED under `D-P8-PL-01 class C`.
* **No paid third-party monitoring service** is in use, and no dedicated monitoring provider has
  been adopted.

**What this repository's runtime code does NOT do.** **Runtime code does not provide a complete
provider-cost budgeting, capping or alerting system**, and this plan claims none. There is no kill
switch, no spending ceiling, no cost accumulator, no per-session token budget and no cost alert.
Nothing meters, budgets, caps or alerts on hosting, storage or email spend. Provider spend is
governed at the provider, by the Owner, not here.

**OD-INFRA-4 — monitoring selection.** `OD-INFRA-4 DECISION: SATISFIED AS A SELECTION DECISION.`
The selected approach is the platform's own metrics and logs plus `/health` and the P10-OB1
bounded logging seam; no dedicated third-party monitoring provider was adopted, and that is a
decision rather than a gap. **The decision being settled is not operational monitoring
readiness:** alerting, paging and notification behaviour, dashboards beyond the platform's own,
and any future dedicated provider if one is separately chosen all remain OPEN operations work.
Nobody is notified when something breaks.
<!-- CURRENT-TRUTH:COST:END -->

## HISTORICAL — SUPERSEDED / NOT IMPLEMENTED (previous claims, corrected)

**SUPERSEDED IN PART — v1.32 current-state correction (2026-09-19).** The prior current-reality
bullet claimed, verbatim and in full: *"There is NO live paid usage of any kind: AI advisory
transfer is disabled in code (`engine/ai_advisor.py`, `AI_ADVISORY_ENABLED = False` — the dormant
Anthropic call path is unreachable without a source change and configures no API key); email runs
to an in-memory development sink; there is no payment provider, no live billing, no hosted
monitoring, no offsite backup provider, and no production hosting/cloud infrastructure."* That is
**no longer true as a whole**. Hosting, off-provider storage and an email adapter all exist now.
The claim is named here rather than quietly deleted, and it states nothing about today.

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

**For current truth read the `CURRENT-TRUTH:COST` region above — this section states none.** What
remains true of this section's own subject: the OD-J2-delegated infrastructure gate and the later
provider gates still govern these decisions; a provisioned provider is not a decided cost policy;
payment processing remains unselected; and cost governance must be re-decided at the gate that
enables any metered or paid usage.
