# P10-D3a — Self-Service Project Export — Bounded Increment Contract (definition only)

**Status:** GOVERNANCE-ONLY CANDIDATE. This contract **authorizes no implementation**. Its sole purpose is to
fix the exact future implementation boundary for `P10-D3a — Self-Service Project Export` so that a later,
separately-authorized implementation gate has a frozen, evidence-grounded target.

**Phase:** 10 — Commercial, Legal, Security and Operational Readiness.
**Governing phase-entry contract:**
`docs/governance/PHASE_10_COMMERCIAL_LEGAL_SECURITY_OPERATIONAL_READINESS_P10C_CONTRACT.md` (merged PR #508,
authoritative). This contract is subordinate to it and to every anchor above it in `CLAUDE.md`'s reading order.
**Authoritative base at drafting:** `bc85424afc0c90e8e1bfb17dd413c326f7a3ff69` (PR #509 merge —
`P10-D2 — Decision Workspace Access-Control Remediation`, authoritative; independently re-verified: first parent
`3f92d57e49a8d6b01b0c6a7184ec7b1442b87e8a`, second parent `871135d16eccd1e0507538dc30666b9bac1a8c6a`, tree
`62303523e27c02b531fbffacade6f3b7eb6a2998`, empty candidate→merge diff).

**Selection lineage.** The combined read-only Phase-10 selection session proposed a single
`P10-D3` gate pairing self-service export with account deactivation. The Independent External Reviewer
**rejected** that shape on two material grounds only: (1) export and deactivation must be **separate
increments**; (2) `P10-D3a` requires **its own committed candidate contract** before implementation
authorization. This document is the corrected response to both. `P10-D3b — Account Deactivation` remains a
**separate, future, unauthorized** increment; nothing here defines, prepares, or implies it.

---

## §1. Objective

Define the boundary for adding **one** browser/session-authenticated, self-service **project** export surface in
`web/app.py`, which **consumes the existing canonical internal export seam**
`engine.read_export_service.produce_project_export` using the caller identity from the **existing** account/session
seam.

The increment adds **reachability** for an already-built, already-owner-scoped capability. It creates no new
export capability, no new authorization model, no new identity system, and no new persistence.

---

## §2. Problem statement (evidence-grounded, verified at base `bc85424`)

Each fact below was re-verified against the working tree at the authoritative base for this contract; none is
copied forward from an earlier contract without revalidation.

1. `engine/read_export_service.py` exposes `produce_project_export(store, project_id, account_id)` — Flask-free,
   non-mutating, owner-scoped, raising the generic `ProjectAccessDenied` on every unauthorized case.
2. `web/app.py` **does not import or reference** `read_export_service` anywhere. Verified by direct search:
   zero occurrences of `read_export_service`, `produce_project_export`, or `get_authorized_project_read`.
3. The only shipped consumer of the seam is `web/api_v1.py` (P7-I2), whose two routes require a **machine
   Bearer credential** (`credential_id.secret`). Its module contract states the machine principal is
   **distinct** from the browser session and that it "never reads `_current_account`, the Flask signed-cookie
   session, or any login cookie", so "a browser-authenticated user without a machine credential does not
   authenticate."
4. `web/api_v1.issue_api_credential(...)` has **no shipped call site** in any route, template, or CLI. A
   signed-in human therefore has **no shipped path** to obtain a credential, and consequently **no shipped path**
   to the Structured Export.
5. `/account` (`web/app.py`) already lists the signed-in account's durably-owned `project_id`s via
   `_owned_projects()` → `store.project_ids_for_owner(...)`, and `web/templates/account.html` renders them as
   `/session/<pid>` links only. There is **no export control** on that page.
6. The nearest browser-reachable output surface, `/session/<sid>/deliverable`, is **not** the Structured Export
   and is **not durable-only**: it requires a live in-memory `SESSION_STORE` entry and returns to the index when
   none exists. It therefore cannot serve an owner returning in a later browser session.

**Net factual gap:** a real, tested, owner-scoped durable export exists in the engine layer and is reachable by
**no shipped human-facing path**.

---

## §3. Exact scope of the future implementation

**In scope, and nothing else:**

* **S-1.** One new route in `web/app.py`, HTTP **GET** only, project-scoped, returning the export for exactly one
  owned `project_id`.
* **S-2.** Caller identity obtained from the **existing** `_current_account()` seam (which already validates
  status / session epoch / idle / absolute expiry and fails closed). No new session, cookie, token, or header.
* **S-3.** The route calls `engine.read_export_service.produce_project_export(record_store, project_id,
  account_id)` via the existing `_get_store()` accessor. The engine seam is **consumed unmodified**.
* **S-4.** `ProjectAccessDenied` is translated into one **generic, non-enumerating** denial.
* **S-4a.** The success response is a **JSON serialization of the seam dict** (`application/json`), following the
  existing `/decision-workspace/<did>/export` precedent, with a deterministic `Content-Disposition: attachment`
  filename derived from the `project_id`. The payload is **not** rendered into HTML, not summarized, not
  paginated, and not reformatted. *(Without a fixed response format, "canonical payload unchanged" (§6.3) would
  not be a testable property; this clause makes it one.)*
* **S-4b.** Any unexpected error — anything other than `ProjectAccessDenied` — **fails closed**: no traceback,
  exception text, stack frame, SQL, or internal identifier reaches the response, matching the fail-closed posture
  of `web/api_v1.py::_handle`. A failure must never degrade into a partial or empty "successful" export.
* **S-5.** One entry-point control on the existing `/account` page (and/or the existing owned-projects list) so
  the route is reachable without URL guessing, using the existing `t(...)` i18n seam.
* **S-6.** New UI strings added to `web/ui_text.py` with **both** `en` and `ar` variants (`SUPPORTED_LANGS =
  ("en", "ar")`); English-only additions are a defect.

**Allowed paths (exhaustive):** `web/app.py`, `web/ui_text.py`, `web/templates/account.html`, and new/updated
files under `tests/`.
**Forbidden paths (non-exhaustive but binding):** `engine/read_export_service.py`, `engine/record_store.py`,
`engine/account_store.py`, `engine/auth_session.py`, `engine/decision_workspace.py`, `web/api_v1.py`,
`database/`, `schemas/`, any migration, any dependency manifest, any CI configuration.

---

## §4. Explicit exclusions

P10-D3a **does not** include, and any implementation drifting into these must STOP (§10):

* Account Deactivation in any form; `set_status(..., "deleted")`; any use of `accounts.deleted_at`.
* Physical deletion, purge, or retention cleanup of any row in any table.
* Account-wide export, multi-project export, or any "all my data" aggregation.
* Commercial, subscription, provider-mapping, usage, or lifecycle-event export.
* Audit export, and **any new `access_audit` write from the browser surface** (see §6.4).
* API credential issuance, exposure, or coupling of any kind.
* Email/notification behaviour of any kind.
* Decision Workspace (FDC-001) changes — its access-control model was closed by P10-D2 and is untouched here.
* Legal or privacy drafting; any GDPR / Kuwait-PDPL / statutory-retention / consent / subject-access
  determination.
* PSRR execution; deployment; production activation.

`P10-D3b — Account Deactivation` remains a **separate future increment**, neither authorized nor scoped here.

---

## §5. Truthful product label (binding)

The surface exports **one owned project's** record dataset. Wording must say exactly that.

**Required wording** — project-scoped only, e.g.:

* `Export project`
* `Export project data`

**Prohibited wording** — in `en` and `ar` alike, in labels, headings, filenames, aria text, and help text:

* `Export my data`
* `Export account`
* `Export all my data`
* any subject-access / "right to data" / legal-export framing.

**Rationale (factual, not legal):** the export payload is composed from one project's assertions plus that
project's domain support-state. It contains **no** account record, credential, commercial, subscription,
provider, audit, or cross-project data. A broader label would be untrue.

---

## §6. Architecture constraints (each traceable to verified repository evidence)

**§6.1 — Preserve the existing authenticated account/session model.** Consume `_current_account()`; add no
parallel identity, no new cookie, no new token, no new decorator framework.

**§6.2 — Preserve the existing project-ownership model.** Ownership is the durable `projects.owner_account_id`
resolved through the seam's own `store.load_owner` path. Note the deliberate, pre-existing divergence that
implementation must **not** "reconcile": `web/app.py::_project_authorized` permits NULL-owner (legacy/anonymous)
capability access, while `read_export_service._is_authorized` **denies** a NULL durable owner (P7-I1 IR-5).
P10-D3a inherits the **seam's stricter rule**: legacy/anonymous NULL-owner projects are **not exportable** through
this surface. This is correct and must not be loosened.

**§6.3 — Preserve the canonical export payload unchanged.** The dict returned by `produce_project_export`
(`idea_id`, `domain_support_state`, `assertion_count`, `validation_summary`, `provenance_summary`, `assertions`)
is consumed as-is and serialized directly (§S-4a). No field may be added, removed, renamed, reordered in meaning,
or recomputed, and no wrapper key may be introduced around it.

**§6.4 — Do not extend `access_audit` to this surface.** `web/api_v1.py` writes a durable `access_audit` event
per served/denied decision; that obligation belongs to the P7-I2 public API. Phase-7 §25 records `access_audit`
retention/cleanup as **deferred / NOT delivered**, and `access_audit` is append-only with no cleanup path.
Adding browser-surface audit writes would enlarge an append-only table whose retention question is explicitly
open, and would reclassify a **closed** Phase-7 disposition. P10-D3a therefore writes **no** audit event, and
this contract **records that as a known, deliberate limitation** deferred to Phase-7 §25 / future Phase-10 work —
it does **not** reopen, reclassify, or rewrite the Phase-7 §25 disposition.

**§6.5 — Do not mount under `/api/`.** `tests/test_p7_i2_public_api.py::test_exactly_two_public_api_routes_registered`
asserts that the set of registered rules beginning with `/api/` is **exactly** the two P7-I2 routes. A new route
under `/api/` would break that assertion and would blur the machine/browser principal separation. The route must
live outside the `/api/` namespace (an `/account/...`-scoped path is the natural fit).
Additionally, `tests/test_draft_l2_local_continuity.py::test_no_server_draft_route_or_record` asserts no
registered rule contains `draft`; the new path must not contain that substring.

**§6.6 — Do not reuse the P7-I2 public wire identity.** `API_VERSION` and `EXPORT_CONTRACT_VERSION` are P7-I2
public-API identities. P7-I1 explicitly "freezes no public wire schema or export version identity". The browser
route must **not** emit or imply `api_version` / `export_contract_version`; doing so would silently extend a
public API contract.

**§6.7 — First `web/app.py` consumer of the seam (stated precisely).** P7-I1's IR-4 recorded
"DEFAULT: DEFER — `web/app.py` is not modified in P7-I1 ... no consumer is rewired to the seam (P7-I2 will
consume it)." That was a **scope boundary on P7-I1 itself**, not a standing prohibition: the seam's own module
contract names "the web UI" among its anticipated internal consumers. P10-D3a would be the **first `web/app.py`
consumer**, permitted only under separate Owner authorization for the implementation gate.

**§6.8 — No persistence or schema change.** No DDL, no migration, no new table, column, index, or store method.
The route is read-only and non-mutating (beyond the existing idle-window slide already performed inside
`_current_account()`).

**§6.9 — GET requires no CSRF token.** The surface is a non-mutating GET, consistent with the existing
`/decision-workspace/<did>/export` and `/session/<sid>/deliverable` GET precedents. No CSRF requirement is
introduced, and none of the existing POST CSRF behaviour changes.

---

## §7. Expected behaviour (the acceptance surface)

| Caller | Project | Expected |
|---|---|---|
| Authenticated owner | own, durably owned | export served |
| Authenticated non-owner | someone else's | generic denial |
| Anonymous / invalid-expired session | any | denied; never served |
| Any caller | nonexistent `project_id` | generic denial |
| Authenticated caller | NULL-owner legacy/anonymous project | generic denial (§6.2) |

**Non-enumeration invariant (binding):** for a given caller, the responses for *nonexistent project*,
*non-owned project*, and *NULL-owner project* must be **indistinguishable** — same status, same body, same
location header. A denial must never reveal whether a project exists or who owns it.

**No API credential is required, accepted, or consulted** on this route.

---

## §8. Migration and compatibility

* **No migration.** No schema, no data backfill, no store change.
* **No behaviour change to any existing route.** The P7-I2 API routes, `/session/<sid>` family,
  `/session/<sid>/deliverable`, the Decision Workspace routes (including P10-D2's access control), `/account`'s
  existing content, and the anonymous journey all keep their current behaviour byte-for-byte.
* **Legacy/anonymous projects are unaffected** — they simply remain outside this surface (§6.2).
* **Backward compatible by construction:** the change is additive (one route, one control, new i18n keys).

---

## §9. Required tests for the future implementation (RED → GREEN; not written now)

The implementation gate must add focused tests proving:

1. Authenticated owner exports an owned project successfully.
2. Authenticated **non-owner** is denied.
3. **Anonymous** caller is denied.
4. **Nonexistent** project is denied.
5. **Missing vs. non-owned** denials are **byte-identical** (no existence disclosure).
6. The canonical export payload is **unchanged** — the parsed JSON response body equals
   `engine.read_export_service.produce_project_export(...)` for the same project/account **exactly**, with no
   added, removed, renamed, or wrapping key, and the response is `application/json` (§S-4a).
7. An unexpected internal failure **fails closed** (§S-4b): no traceback or internal detail in the response, and
   no partial/empty payload served as success.
8. No API credential is required, and presenting none still succeeds for the owner.
9. The rendered label is project-scoped in **both** `en` and `ar`, and none of the prohibited §5 phrasings
   appears.
10. The `/api/` route set is still exactly the two P7-I2 routes (§6.5 regression guard).
11. Full relevant regression suites remain green — at minimum `tests/test_p7_i2_public_api.py`,
   `tests/test_p10_d2_decision_workspace_access_control.py`, `tests/test_draft_l2_local_continuity.py`, and the
   localization suites.
12. Full repository suite green.
13. `git diff --check` clean.

These tests are **not** written by this contract and must not be written before implementation authorization.

---

## §10. Stop conditions for the future implementation

Implementation must **STOP and report** — not work around — if:

1. `produce_project_export` cannot be consumed safely from the authenticated web/session surface without API
   credential coupling. *(Current evidence indicates this condition is not triggered: the seam is Flask-free and
   takes `account_id` explicitly. The condition remains binding if implementation evidence contradicts that.)*
2. Implementation appears to require changing the canonical export schema.
3. Implementation appears to require any schema or persistence change.
4. A truthful project-only export label cannot be maintained.
5. Legal or policy interpretation becomes necessary to proceed.
6. Scope expands into Account Deactivation or any other Phase-10 finding.
7. Implementation appears to require touching `access_audit`, or reopening the Phase-7 §25 disposition.
8. Implementation appears to require modifying `web/api_v1.py` or adding a route under `/api/`.

---

## §11. Completion criteria for **this contract** (the governance gate only)

This gate is complete when this document is created, frozen at an exact SHA, Creator-Grilled, bundled
SHA-preservingly, independently reviewed, Owner-accepted at that exact SHA, published, and post-merge verified.

Completion of this gate delivers **a definition only**. It delivers no route, no test, and no runtime change.

---

## §12. Governance and authorization boundary (binding, explicit)

* **Creating or merging this contract does NOT authorize implementation.** A merged definition is not a
  permission to build.
* **Implementation of P10-D3a requires separate, explicit Owner authorization** naming that gate.
* **No automatic successor gate.** Closing this contract activates nothing — not `P10-D3b`, not any other
  Phase-10 finding, not any downstream phase. This matches the P10-C §10 gate-selection rule
  (evidence-based, smallest sufficient scope, Owner-selected; no successor pre-named).
* **No PSRR trigger.** PSRR remains a cross-phase release gate consumed within Phase-10 ownership, triggered
  before first public production deployment. Nothing here triggers, starts, or partially performs it.
* **No deployment authority.** `OD-P`'s separate deployment gate **and** explicit Owner deployment authorization
  both remain independently required and unsatisfied.
* **No Level-0 / product-identity / security-privacy-boundary / phase-sequencing change.** No active hold is
  moved. `OWNER_DECISION_REGISTER.md` is **UNCHANGED**.
* **Phase-7 §25 preserved.** The `access_audit` disposition is consumed as current fact only (§6.4); it is not
  reopened, reclassified, or rewritten.
* **Zero runtime diff.** This candidate touches no `engine/`, `web/`, `tests/`, `domains/`, `schemas/`,
  `database/`, `scripts/`, or CI path.

---

## §13. Governance truth sweep (performed at base `bc85424` before freezing)

Every material claim in §2 and §6 was verified directly against the tree at the authoritative base, not carried
from an earlier contract:

| Claim | Verification |
|---|---|
| Seam signature and generic denial | `engine/read_export_service.py` read in full |
| `web/app.py` does not consume the seam | direct search: zero matches for the three seam symbols |
| API principal is distinct from browser session | `web/api_v1.py` module contract + `_authenticate` read in full |
| `issue_api_credential` has no shipped call site | direct search across the repository |
| `/account` lists owned projects, offers no export | `web/app.py::account_home`/`_owned_projects` + `account.html` read |
| Deliverable route needs a live in-memory session | `web/app.py::show_deliverable` read |
| Seam denies NULL durable owner; web permits it | `read_export_service._is_authorized` vs `web/app.py::_project_authorized` |
| Exactly-two-`/api/`-routes assertion exists | `tests/test_p7_i2_public_api.py` |
| No-`draft`-route assertion exists | `tests/test_draft_l2_local_continuity.py` |
| i18n requires `en` + `ar` | `web/ui_text.py` `SUPPORTED_LANGS` |
| `access_audit` retention deferred by Phase-7 §25 | `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` §25 entries |
| P7-I1 IR-4 was a P7-I1 scope boundary, not a ban | `P7_I1_..._INCREMENT_CONTRACT.md` IR-4 + seam module contract |

**Result:** no stale or unsupported live-current claim carried into this contract. Statements that could not be
established as fact are marked as such rather than asserted.

---

## §14. Creator Grill record (rejected candidate preserved as evidence)

The first frozen candidate for this contract, **`e8e6ed7bff9e0916117875684be54bcd830e0f1d`** (parent
`bc85424afc0c90e8e1bfb17dd413c326f7a3ff69`, tree `221894be4cb56c561b04faec3c37a228826ad3ce`), **FAILED** the
Mandatory Creator Grill on two material defects. It is preserved unmodified as rejected evidence and is **not**
the candidate offered for review.

* **D-1 — unspecified response format.** The contract required the canonical export payload to remain unchanged
  but never fixed the response format, so an implementation could render the payload as HTML and "unchanged"
  would not be a testable property. **Correction:** §S-4a now fixes the response as a direct `application/json`
  serialization of the seam dict with an attachment filename, §6.3 forbids any wrapper key, and §9 test 6 asserts
  exact key-for-key equality against the seam output.
* **D-2 — no fail-closed requirement for unexpected errors.** Only `ProjectAccessDenied` was addressed, leaving
  an internal failure free to leak a traceback where the `web/api_v1.py` precedent fails closed. **Correction:**
  §S-4b mandates fail-closed handling with no internal detail and no partial payload served as success, and §9
  test 7 asserts it.

Both defects were self-identified during the adversarial phase of the Grill; neither was reported by an external
party. No other section was altered, and no factual claim in §2, §6, or §13 was weakened by the correction.
