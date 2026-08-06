# Phase 2 — Increment 3 — Stale Governance-Report Supersession (SD-2 / CR-1)

**Phase:** Phase 2 — Governance and Architecture Corrections.
**Increment:** P2-I3 — Stale Governance-Report Supersession. Addresses Phase 2
Required-Work item 3 ("mark stale architecture documents as historical or
superseded") for `docs/governance/DOMAIN_SCOPE_GOVERNANCE_INCONSISTENCY_REPORT.md`
(**SD-2 / CR-1**) **ONLY**.
**Type:** documentation-only governance correction. **DOCUMENTED NO-VALID-RED.**
No engine/web/JSON/test/CI/schema/runtime change. No target-architecture
definition. No downstream activation.
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified base:** `274bdf00b5c6daedb6c284411cab8000daa94767`.

---

## 0. Lifecycle status (read first)

```
PHASE 2 INCREMENT 3:  IMPLEMENTATION CANDIDATE PREPARED
                      NOT YET OWNER-ACCEPTED
                      NOT YET MERGED
                      NOT YET FORMALLY CLOSED
```

This is an **Increment 3 implementation candidate**. It becomes authoritative as
the merged Increment 3 evidence artifact **only after** independent review, owner
acceptance, normal merge, and post-merge verification. **It does not itself
constitute formal closure of Increment 3.**

## 1. Purpose and boundary

Marks `docs/governance/DOMAIN_SCOPE_GOVERNANCE_INCONSISTENCY_REPORT.md`
**HISTORICAL — MISLEADING IF READ AS CURRENT / SUPERSEDED** and adds an
authoritative pointer, preserving its body unchanged. It resolves a
documentation-only inconsistency — a stale report describing a generic
domain-routing `/start` behavior that no longer exists — against the current
electronics/electrical-only admission runtime. **It defines no architecture and
certifies no runtime behavior.**

## 2. Superseded stale claims (SD-2 — recorded; the file body is not rewritten)

From the report's identity block and body (preserved as history):
- `Status: DRAFT — OWNER RESOLUTION REQUIRED` — **SUPERSEDED** as a current-status
  claim.
- "The generic `/start` route in `web/app.py` calls `infer_domain(idea_text)` and
  assigns the result to `state.domain`." — **SUPERSEDED**.
- "Through that route, a user may be routed into the `mechanical`,
  `medical_device`, or `software` domain." — **SUPERSEDED**.
- "No feature flag or authorization gate prevents non-electronics routing on the
  generic route." — **SUPERSEDED**.

## 3. Current runtime truth (web/app.py — electronics/electrical-only admission)

The `/start` route admits only electronics/electrical sessions:
- `DOMAIN_CONFIRM_VALUE = "electronics_electrical"`.
- `/start` requires an explicit electronics-electrical confirmation
  (`request.form.get("domain_confirm") != DOMAIN_CONFIRM_VALUE` → refuse).
- Strong unsupported / conflicting evidence returns `UNSUPPORTED_DOMAIN_MESSAGE`
  with **no session created**.
- On admission the runtime sets `state.domain = DOMAIN_CONFIRM_VALUE` (always
  `electronics_electrical`) — never an `infer_domain` non-electronics value.

The report's generic-routing claim is therefore contradicted by the committed
runtime. This is recorded from committed evidence; **no runtime investigation,
`engine/domain_rules.py` change, code comment, or code execution is performed or
authorized in this increment.** The `infer_domain` priority list remains latent
code and is **out of scope** here (its disposition is a separate item).

## 4. Authoritative current surfaces (govern in its place)

- **Governing authority:** `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`.
- **Active roadmap:** `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`.
- **Current runtime truth:** `web/app.py` (electronics/electrical-only admission; in-memory `SESSION_STORE`).
- **Conflict/stale evidence:** `docs/governance/evidence/phase0_evidence_lock/CONFLICT_REGISTER.md` (CR-1) and `docs/governance/evidence/phase0_evidence_lock/STALE_DOCUMENT_REGISTER.md` (SD-2).

**No definitive current target architecture is defined by this increment.**

## 5. Body-preservation method

A HISTORICAL/SUPERSEDED banner and authoritative pointer are inserted immediately
after the H1 title. The existing base content (base blob
`1ab6211caf173a417cf7852beea409fe691fb0df`) — including the `Status: DRAFT` block
and the stale generic-route claims — is **preserved unchanged** as history below
the banner; the report body from `## 1. Record identity` through end-of-file is
**byte-identical** to the base (base sub-body blob
`99fc98c10c9c4ebfa959080a561b899767ccbbab`).

## 6. Scope (exactly four files)

1. **MODIFY** `docs/governance/DOMAIN_SCOPE_GOVERNANCE_INCONSISTENCY_REPORT.md` — banner only (body preserved).
2. **ADD** `docs/governance/evidence/phase2_governance_corrections/P2I3_STALE_DOMAIN_SCOPE_REPORT_SUPERSESSION.md` (this record).
3. **MODIFY** `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` — current-status synchronization (L10/L11 only).
4. **MODIFY** `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` — one append-only Increment 3 candidate record.

No other file changes.

## 7. Excluded work and authority boundaries

Excluded (not touched, not defined, not activated): **`engine/domain_rules.py`; any
code comment; any runtime behavior; SD-3; SD-4; `CLAUDE.md`; target-architecture
definition; core/adapter boundaries; product sequencing; central branding
boundaries; domain/capability registries; persistence/subscription rules;
`main` reconciliation; Phase 3 or later; sponsor logos; colors; Themes;
authentication; subscriptions; deployment.**

```
PHASE 2 INCREMENT 2:          FORMALLY CLOSED
PHASE 2:                      IN PROGRESS — INCREMENT 3 ONLY (this candidate); NO OTHER PHASE 2 INCREMENT AUTHORIZED
CENTRAL BRANDING BOUNDARIES:  SEPARATELY GATED FUTURE PHASE 2 WORK — NOT YET AUTHORIZED
PHASE 3 AND LATER:            NOT STARTED / NOT AUTHORIZED
PRODUCT STATUS:               DEMO_READY_WITH_LIMITATIONS / NOT PRODUCTION READY
MAIN:                         STALE / UNRECONCILED (not touched here)
IMPLEMENTATION AUTHORITY:     NONE
RELEASE AUTHORITY:            NONE
DEPLOYMENT AUTHORITY:         NONE
```

## 8. RED path

`DOCUMENTED NO-VALID-RED`. Documentation-only; it changes no runtime code, JSON,
behavior, or executable contract. Validation uses documentation consistency, exact
four-file scope, protected tree/blob verification, target-body byte-identity, and
ancestry — not a test transition.

## 9. Evidence classification

Phase 2 governance-correction evidence artifact (implementation candidate). It
becomes the authoritative Increment 3 supersession record only after independent
candidate review, owner acceptance, normal merge, and post-merge verification
(§0). It grants no implementation, release, or deployment authority and certifies
no runtime behavior.
