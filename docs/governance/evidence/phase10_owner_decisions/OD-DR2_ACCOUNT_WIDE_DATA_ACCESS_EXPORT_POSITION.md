# Phase 10 — Owner Decision OD-DR2 — Account-Wide Data Access / Export Position

**Phase:** Phase 10 — Commercial, Legal, Security and Operational Readiness, under the authoritative
`docs/governance/P10_JURISDICTION_AND_DATA_RIGHTS_OWNER_DECISION_GATE.md` (merged PR #514) which registered
OD-DR2 as unresolved.
**Decision ID:** OD-DR2 (account-wide data access / export position).
**Scope:** documentation-only durable record of one Owner decision accepted **at strategy level**. **No
implementation. No export capability, route, schema, connector, or test change. No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified authoritative base at authoring:** `46756528509beebefc86ee399f331a796cbae6f2` (PR #516 merge —
OD-DR1 acceptance, authoritative; parents `f35a3999…` + `13c9f7d1…`, merge tree `5a02ad1c…` equal to the
accepted candidate tree — independently re-verified at authoring).

---

## 1. Decision status

```
OD-DR2 — OWNER DECISION ACCEPTED AT STRATEGY LEVEL
```

**Account-wide self-service export remains: `DEFERRED PENDING EXTERNAL LEGAL DETERMINATION AND SEPARATE OWNER
AUTHORIZATION`.** No account-wide export implementation is authorized now.

---

## 2. Current export truth (exact; nothing re-labeled, nothing expanded)

Verified at the base: exactly three export surfaces exist, and OD-DR2 changes none of them.

* **The only currently authorized P10-D3a self-service export is `PROJECT-SCOPED EXPORT`** — it exports one
  owned project's record dataset under its existing truthful-label contract (`Export project` / project-scoped
  wording only). It must NOT be described as a final-output export, an account export, "Export my data", or an
  account-wide export.
* The existing **FDC-001 Decision Workspace export is preserved unchanged**.
* The P7-I2 credentialed API export is likewise untouched.
* **No account-wide export exists**, and no existing export surface is expanded by OD-DR2.
* No current export exposes secrets, credential material, or internal security records (verified: the store
  persists only `password_hash` / `secret_hash` / `token_hash`, and no export surface reads them).

---

## 3. Owner future product priority (direction only)

For future user-facing export design, the product priority is:

```
USEFUL OUTPUT PORTABILITY OF FINAL PROJECT OUTPUTS / RESULTS
```

This may include future export of useful final project deliverables such as: final results; final decisions;
final conclusions; final structured outputs; final project artifacts where applicable.

This is **`FUTURE PRODUCT DIRECTION ONLY`**. It does NOT: create a new export surface; modify P10-D3a; modify
the Decision Workspace export; authorize implementation; or select any export format. **The existing P10-D3a
export is NOT described as a final-output export** — it remains the project-scoped record-dataset export it
is.

---

## 4. Product Export vs. Legal Data Access (distinct capabilities)

* **Product Export** — a user-facing product capability focused on useful project outputs.
* **Legal Data Access / Portability** — a potentially broader response required **if** applicable law or a
  legally valid request requires it.

These are NOT the same capability. A narrow product export must not be cited as proof that legal-access
obligations are satisfied, and a broader legal request must not silently redefine the normal product export.
**No conclusion is made that any particular legal regime applies.**

---

## 5. Account-wide no-foreclosure principle (architecture preservation only)

**No architectural decision may structurally foreclose a future, separately governed account-wide
data-access/export capability.** This is **`NO-FORECLOSURE / ARCHITECTURE-PRESERVATION ONLY`** — it is NOT an
instruction to build, prepare, pre-implement, create schema, create routes, create background jobs, or create
bulk-export infrastructure.

---

## 6. Legal-obligation escalation (OD-DR1-symmetric; escalation rule only)

**Deferring a self-service account-wide export feature does NOT suspend any legally applicable data-access or
portability obligation.** If a legally binding data-access/portability request is received before such a
capability exists, it must be **escalated to the Owner and external legal counsel**. OD-DR2 must not be cited
as grounds to refuse or improperly delay such a request. This is an escalation rule only — NOT a conclusion
that any particular law applies.

---

## 7. OD-DR1 / deletion boundary

OD-DR2 does NOT: modify OD-DR1; reopen OD-DR1; reinterpret P10-D3b; deactivate an account; delete data;
trigger erasure; or alter retention. **OD-DR1's recorded conditional truthful export opportunity remains
unchanged — neither expanded nor foreclosed by OD-DR2.**

---

## 8. Normal product-export exclusion principle (defaults, not legal conclusions)

A normal product/final-output export must NOT automatically expose internal/system-sensitive material such as:
password hashes; API credential secrets or hashes; API credential records; email verification tokens;
password-reset tokens; session/security metadata; fraud/abuse indicators; internal security signals;
rate-limit records; internal operational metadata; provider internals; third-party confidential data; another
user's data; or institution-owned data the requester is not authorized to export.

The following must be **classified separately, rather than automatically exposed**:
`subscription_lifecycle_events`; `commercial_audit`; `provider_event_dedupe`; `access_audit`; backups;
replicas; derived copies/logs.

These exclusions are **`NORMAL PRODUCT-EXPORT DEFAULTS`**. They are NOT absolute legal conclusions about what
could ever be reachable through a legally valid broader request — any such broader determination remains with
the Owner and external legal counsel.

---

## 9. Local browser-data truth

Client-side browser drafts stored in `localStorage` are **not server-held data** (verified: the draft
mechanism is explicitly "in this browser's localStorage only"). A server-side export must NOT claim
completeness over client-only local drafts. No mechanism to collect them is created by this candidate.

---

## 10. Identity / authorization principle (future principle only)

Any future account-wide or broader sensitive export capability should require **strong identity and
authorization verification**. Recorded as a future principle only — the authentication workflow is NOT
designed now. The future gate must consider: account ownership; compromised-session risk; export exfiltration
risk; institutional authority; administrator authority. No implementation is authorized.

---

## 11. Institutional export boundary (reserved)

Reserved to a later institutional/legal gate: employee/student data; institution-owned project data; workspace
data; administrator-controlled records; shared project ownership; contractual/confidential records; who has
authority to export institutional data. OD-DR2 creates **`NO INSTITUTIONAL EXPORT AUTHORITY`** and activates
**`NO INSTITUTIONAL FEATURE`**.

---

## 12. Third-party / other-user protection

Any future broader export must not expose data merely because it is technically reachable. Explicitly
preserved protections: another user's personal information; another user's project data; institution-owned
confidential information; third-party licensed/confidential content; external provider secrets. Final rules
are NOT created now.

---

## 13. Format neutrality

No specific future export format is selected. Future possibilities may include: structured machine-readable
output; a human-readable report; a portable file package; Integration/Export Layer output. OD-DR2 does NOT
authorize: PDF delivery; email delivery; cloud delivery; vendor-specific export; a new connector; a new
adapter; or a new external integration.

---

## 14. Authoritative canonical architecture (reference only)

Repository truth confirms the authoritative P7-I3 principle (verbatim from
`docs/governance/P7_I3_CANONICAL_EXPORT_LOCAL_REFERENCE_ADAPTER_PROOF_INCREMENT_CONTRACT.md`):

```
InventorAI Core → Canonical Output Model (P7-I1 Structured Export) → Integration/Export Layer
(P7-I3 adapter boundary) → External Tools
```

Any future export surface should preserve this architecture. OD-DR2 does NOT create a second Canonical Output
Model, vendor coupling, connector activation, or provider activation. Architecture reference only.

---

## 15. Database-dump rejection

The product assumption **`user export = dump every database row` is explicitly rejected.** The future
product-facing export should prioritize **`USEFUL OUTPUT PORTABILITY`**, not a **`DATABASE DUMP`**. Any
broader data-access request must use separate classification/legal handling (§4, §6, §8).

---

## 16. Preserved decisions and boundaries

**OD-CJ1** (commercial jurisdiction / tax scope) remains **REGISTERED AND UNRESOLVED**. **OD-DR1 remains
accepted and unchanged** (PR #516). OD-J1/OD-J2 remain authoritative; OD-A continues to govern brand/name.
P10-D3a, P10-D3b, and the Decision Workspace export are preserved exactly as merged.

---

## 17. Non-authorization (binding)

This record authorizes **no** implementation of any kind: no account-wide or final-output export capability;
no export-surface change; no connector, adapter, or delivery mechanism (PDF/email/cloud/vendor); no
institutional functionality; no legal-artifact drafting; no infrastructure work; no PSRR execution; no
deployment. Every subsequent step remains separately Owner-authorized under P10-C §10.
