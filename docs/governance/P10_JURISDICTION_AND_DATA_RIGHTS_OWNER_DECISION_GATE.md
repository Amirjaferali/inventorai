# Phase 10 — Jurisdiction & Data-Rights Owner-Decision Gate (governance-only; decision registration only)

**Status:** GOVERNANCE-ONLY CANDIDATE. This gate **registers unresolved Owner decisions and required external
legal-input questions**. It decides nothing, drafts nothing, implements nothing, and authorizes nothing.

**Phase:** 10 — Commercial, Legal, Security and Operational Readiness, under
`docs/governance/PHASE_10_COMMERCIAL_LEGAL_SECURITY_OPERATIONAL_READINESS_P10C_CONTRACT.md` (merged PR #508,
authoritative) and its §10 gate-selection rule (evidence-based; smallest sufficient scope; Owner-selected;
separately authorized). Subordinate to every anchor above it in `CLAUDE.md`'s reading order.

**Authoritative base at drafting:** `07389b24ce9c4a606526315f2c19118f292f04db` (PR #513 merge — P10-D3b
Account Deactivation implementation, authoritative; independently re-verified: first parent
`46c80714a35e5c6cf289b4d807d6f7a31d17cf5d`, second parent `a751cb3b1ffb882ea8596cefafe7ef1a9222cd81`, merge
tree `886d06f605bf08b36b765a96a528bd42047af0de`, empty candidate→merge diff).

**Selection lineage.** After P10-D3b closed, a read-only Phase-10 Remaining-Obligations review determined the
exit criteria are NOT satisfied and that the next gate is Owner-selected per P10-C §10. The Owner then selected
a read-only Privacy / Legal Readiness Assessment, whose accepted result identified that **every remaining legal
artifact and the registered GDPR/PDPL open question are blocked on a small set of unregistered Owner decisions
and external legal inputs**. The Owner selected this bounded gate to register exactly those — nothing more.

---

## §1. Why this gate exists (the blocking finding, restated minimally)

Repository evidence is **insufficient to determine legal-regime applicability**: no launch country, no
user-residence scope, no target commercial jurisdiction, and no hosting/data-location assumption is registered
anywhere in repository authority. The only regime references are `docs/DATA_RETENTION_POLICY.md`'s historical
trigger clause — *"No PII collected in MVP. GDPR/PDPL review required before adding accounts"* — and P10-C §9's
registration of that clause as a now-triggered, unresolved, load-bearing open question (real accounts exist).
No legal artifact (Privacy Policy, Terms, consent, cookie notice, data-rights scope, payment/refund terms) can
be **truthfully scoped** until the decisions below are answered and external counsel input is obtained against
those answers.

---

## §2. P10-D3b closure synchronization (recorded here; nothing reopened)

**P10-D3b IMPLEMENTATION AUTHORITATIVE: YES.** Implementation candidate
`a751cb3b1ffb882ea8596cefafe7ef1a9222cd81` (parent `46c80714…`, tree `886d06f6…`) was Owner-accepted at that
exact SHA after Contract Compliance PASS, Creator Grill PASS, Independent External Review `ACCEPT WITH
NON-BLOCKING OBSERVATIONS`, and Independent Reviewer Grill PASS, and merged via **PR #513**, tip
`07389b24ce9c4a606526315f2c19118f292f04db` (identity above, independently re-verified). Scope: 5 files,
+487/−1 (`web/app.py`, `web/ui_text.py`, `web/templates/account.html`, `web/templates/login.html`,
`tests/test_p10_d3b_account_deactivation.py`). Delivered: `POST /account/deactivate` — authenticated + CSRF +
password re-entry; existing `set_status`/`increment_session_epoch` primitives; all sessions/logins/API
credentials fail via existing status gates; **no row deleted anywhere**; truthful EN/AR deactivation wording.
Focused 18/18 GREEN (RED 14/4/0 first); full suite 2754/0/3/1. **This synchronization records the already-
authoritative state only; P10-D3b is not reopened, reinterpreted, or modified.**

---

## §3. Data-truth baseline (minimum facts; each revalidated at base `07389b2` before freezing)

| Fact | Class | Evidence |
|---|---|---|
| Accounts store real user data (email, scrypt password hash, status, timestamps) | LIVE | `engine/account_store.py` `accounts` |
| Project/record invention content is stored server-side | LIVE | `engine/record_store.py` |
| Self-service export is PROJECT-SCOPED ONLY (one owned project's assertions + domain support-state) | LIVE | P10-D3a route `account_project_export` |
| Account deactivation exists and RETAINS all data (status flag + `deleted_at`; nothing removed) | LIVE | P10-D3b route `account_deactivate` |
| No physical deletion/erasure capability exists; the only `DELETE FROM` in `engine/` is rate-limit cleanup | LIVE (absence verified) | full-tree grep at base |
| No enforced retention exists for any user data | LIVE (absence verified) | same sweep |
| No analytics/telemetry | NOT IMPLEMENTED | template/static grep at base |
| No IP/device/network metadata collection | NOT IMPLEMENTED | zero `remote_addr`/`user_agent` reads in `web/app.py`/`web/api_v1.py` |
| No live payment provider (tables exist; no webhook route; no live callers) | NOT IMPLEMENTED | `payment_ingestion` caller sweep |
| No live production email provider (`DevMemoryEmailSender` "never sends over a network") | NOT IMPLEMENTED | `engine/email_sender.py` |
| External AI transfer disabled (`AI_ADVISORY_ENABLED = False`, hardcoded, checked first, no override) | DISABLED | `engine/ai_advisor.py:11` |
| **No live third-party transfer path exists without a source-code change** | LIVE (absence verified) | conjunction of the above |
| Browser draft text is client-side localStorage only (7-day lazy TTL, 64KB cap) | CLIENT-SIDE ONLY | `web/static/js/local_draft.js` |
| `database/supabase_schema.sql` | HISTORICAL / NON-LIVE | zero references (unchanged: `engine/`+`database/` byte-identical since `bc85424`) |
| The live trust page itself states Privacy Policy/Terms content is not provided | LIVE | `web/ui_text.py` `UI_SENS_DATA_07`; `/data-and-session` |

These facts are why the decisions below are needed; this section is a baseline, not a second diagnostic report.

---

## §4. Owner Decision Set (REGISTERED AS UNRESOLVED — no answer is proposed or implied)

No repository authority answers any of the following (verified by sweep at base; supersession checked).

**OD-J1 — Intended Launch Markets / User-Residence Scope.** The Owner must determine the intended initial
public launch market(s) and/or expected user-residence scope. Repository truth contains **no authoritative
launch-country scope**; nothing here assumes Kuwait-only, GCC, EU, worldwide, or any national jurisdiction.
*Status: OWNER DECISION REQUIRED.*

**OD-J2 — Hosting / Data Location.** The Owner must determine the intended production hosting/data-location
strategy, or explicitly delegate it to a later infrastructure gate. No region or provider is invented here.
*Status: OWNER DECISION REQUIRED BEFORE LEGAL-REGIME FINALIZATION* (a delegation decision is itself an
acceptable answer).

**OD-DR1 — Physical Deletion / Erasure Product Position.** The Owner must decide whether physical
deletion/erasure should be offered as a general product feature, offered only if legally required, or remain
undecided pending counsel. **No implementation is authorized by any answer recorded later**; the D3b truth is
unchanged: *Account Deactivation ≠ Physical Deletion* — deactivation retains all data. Known technical context
(factual only): three append-only stores (`subscription_lifecycle_events`, `commercial_audit`,
`provider_event_dedupe`) plus `access_audit` are erasure-hostile by current design, and no deletion method
exists in either store. *Status: OWNER DECISION REQUIRED (may be informed by counsel).*

**OD-DR2 — Account-Wide Data Access / Export Product Position.** The Owner must decide whether InventorAI
should provide only the current project-scoped export, a future account-wide access/export capability, or defer
the scope pending legal determination. **P10-D3a is not expanded**; project-scoped export remains authoritative
and unchanged. *Status: OWNER DECISION REQUIRED (may be informed by counsel).*

**OD-CJ1 — Commercial Jurisdiction / Tax Scope.** Before any paid activation, the Owner must determine the
intended commercial jurisdiction/tax scope (consumed by the existing deferred business-decision registers:
`P8C` §5 "tax handling / jurisdictions"; P8-I4 "tax treatment / supported jurisdictions"). No tax treatment is
selected, no payment terms are created, and no billing is activated here. *Status: OWNER DECISION REQUIRED
BEFORE PAID ACTIVATION.*

**OD-B1 — Final Product / Brand Name Dependency (reference to EXISTING authority; no new decision).** Final
product naming is already governed by **OD-A** (ACCEPTED: "Final public product name deferred; `InventorAI`
temporary working name"; evidence
`docs/governance/evidence/phase1_owner_decisions/OD-A_OD-B_NAMING_AND_BRANDING.md`; brand-validation gate
pending). This gate **records the dependency only**: final legally named artifacts (Privacy Policy, Terms,
payment terms) may depend on the authoritative brand/name resolution under OD-A's existing gate. No duplicate
decision is created and the product is not renamed. *Status: EXISTING AUTHORITY REFERENCED; brand gate remains
pending under OD-A.*

**Register mechanics.** `OWNER_DECISION_REGISTER.md` indexes **accepted** decisions ("Append or supersede rows
as owner decisions are accepted and committed") and is therefore **UNCHANGED by this candidate**. When the
Owner later answers any item above through a separately authorized acceptance gate, that gate appends the
corresponding register row and evidence file.

---

## §5. External Legal Input Request Register (requirements to obtain — NOT conclusions)

Each item below is registered as an input to obtain from external counsel **once the OD-J1/OD-J2 facts exist**;
each explicitly depends on the eventual jurisdiction/market answers, and **no statement here asserts that any
specific law applies**:

1. **GDPR applicability, if any**, given the OD-J1/OD-J2 answers.
2. **Applicable national PDPL / privacy regime(s), if any**, given the same answers.
3. **Resulting requirements** for: a Privacy Policy; Terms of Service; privacy consent (if applicable); a
   cookie notice (if applicable — the product currently sets a signed session cookie and no notice exists).
4. **Data-subject-rights requirements**, if any: access; portability/export (informing OD-DR2);
   deletion/erasure (informing OD-DR1); retention (no enforced retention currently exists).
5. **User-content / IP terms**, consistent with existing OD-D/OD-E boundaries (recorded claims are assertions,
   never legal findings) and the openly-acknowledged unfinalized confidentiality/staff-access position
   (`UI_SENS_DATA_06`).
6. **Payment / refund / subscription terms** required before paid activation (consumed with OD-CJ1 and the
   existing P8C §5 item 25 register).

Counsel input must be evaluated against the **data-truth baseline in §3** — in particular the LIVE /
DISABLED / NOT IMPLEMENTED distinctions — so that any future notice describes only processing that actually
occurs.

---

## §6. Explicit non-decisions (binding)

This gate does **NOT** decide: applicable law; lawful basis; consent requirements; retention periods;
deletion/erasure implementation; account-wide export implementation; final Privacy Policy text; final Terms
text; payment/refund language; tax treatment; hosting provider; deployment; PSRR. It also does not modify,
reopen, or reinterpret P10-D2, P10-D3a, P10-D3b, Phase-7 §25, or any append-only store semantics.

---

## §7. Next-gate semantics (no auto-activation)

After this candidate is independently reviewed, Owner-accepted, published, and post-merge verified, **no
successor gate is activated automatically**. The next step depends on the Owner's actual answers; possible
future outcomes include an external legal-input gate, a legal-artifact drafting contract, a data-rights
technical-gap contract, the OD-A brand gate, or a commercial-jurisdiction decision gate — **none is
pre-authorized here**. P10-C §10 remains binding: evidence-based, smallest sufficient scope, Owner-selected,
separately authorized.

---

## §8. Boundary statements

* Governance-only; **zero runtime/test diff**; no schema, persistence, or architecture change.
* `OWNER_DECISION_REGISTER.md` UNCHANGED (§4 register mechanics).
* **No PSRR trigger** — PSRR remains "Mandatory: BEFORE FIRST PUBLIC PRODUCTION DEPLOYMENT" (registration §4);
  Phase-10 continuation does not trigger it.
* **No deployment authority** — `OD-P`'s separate deployment gate and explicit Owner deployment authorization
  both remain independently required and unsatisfied.
* No payment-provider selection; no monitoring/backup/security implementation; no legal drafting of any kind.
* Authoritative ONLY if/when this exact candidate is merged and post-merge verified. Next required step:
  Independent External Review of this exact SHA + bundle.

---

## §9. Governance truth sweep (performed at base `07389b2` before freezing)

Classification of every material statement:

| Statement | Class | Verification |
|---|---|---|
| P10-D3b merge identity + authoritative status (§2) | supported current fact | fetched and re-derived from git this session |
| Every §3 baseline row | supported current fact (or verified absence) | each re-verified by direct grep/read at this exact tip this session |
| No jurisdiction/market/hosting registration exists | supported current fact (verified absence) | repository-wide sweep for GDPR/PDPL/jurisdiction/launch-market terms |
| GDPR/PDPL open question registered + triggered | supported current fact | `DATA_RETENTION_POLICY.md` (read in full) + P10-C §9 |
| OD-A governs product naming | supported current fact | `OWNER_DECISION_REGISTER.md` row + evidence file present |
| P8C/P8-I4 defer tax/jurisdiction business decisions | supported current fact | `P8C` §5; P8-I4 contract (grep-verified lines) |
| ODR indexes accepted decisions only | supported current fact | register header text, read this session |
| Append-only stores are erasure-hostile | supported current fact | schema comments, re-verified engine tree identity since `bc85424` |
| "Legal artifacts cannot be truthfully scoped before these decisions" | bounded derived conclusion | derived from the verified absence of jurisdiction facts + the §5 dependency structure |
| All six OD items unresolved (except OD-B1's referenced existing authority) | Owner decision request | sweep confirmed no authoritative answer exists |
| All §5 items | external-input request | none stated as a conclusion; each conditioned on OD-J1/OD-J2 |

**Rejected during the sweep:** any assumed jurisdiction or law applicability; any implied deletion or
account-wide export; any invented retention period, lawful basis, consent requirement, or third-party
processing; any premature PSRR/deployment language. **Result: zero unsupported or stale current-state claims.**
