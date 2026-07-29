# Phase 2 — Increment 2 — Stale Architecture Decision Supersession (SD-1 / CR-2)

**Phase:** Phase 2 — Governance and Architecture Corrections.
**Increment:** P2-I2 — Stale Architecture Decision Supersession. Addresses Phase 2
Required-Work item 3 ("mark stale architecture documents as historical or
superseded") for `docs/ARCHITECTURE_DECISION.md` (**SD-1 / CR-2**) **ONLY**.
**Type:** documentation-only governance correction. **DOCUMENTED NO-VALID-RED.**
No engine/web/JSON/test/CI/schema/runtime change. No target-architecture
definition. No downstream activation.
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified base:** `42ccbe3a4c1d49843294a0bd63376d232a7f45dd`.

---

## 0. Lifecycle status (read first)

```
PHASE 2 INCREMENT 2:  IMPLEMENTATION CANDIDATE PREPARED
                      NOT YET OWNER-ACCEPTED
                      NOT YET MERGED
                      NOT YET FORMALLY CLOSED
```

This is an **Increment 2 implementation candidate**. It becomes authoritative as
the merged Increment 2 evidence artifact **only after** independent review, owner
acceptance, normal merge, and post-merge verification. **It does not itself
constitute formal closure of Increment 2**; formal closure remains a separately
authorized later gate.

## 1. Purpose and boundary

Marks `docs/ARCHITECTURE_DECISION.md` **HISTORICAL / SUPERSEDED** and adds an
authoritative pointer, preserving its body unchanged. It resolves a
documentation-only inconsistency — a stale Supabase/DB/Auth/append-only
architecture description versus the in-memory Flask runtime. **It defines no new
architecture and certifies no runtime behavior.**

## 2. Superseded stale claims (SD-1 — recorded; the file body is not rewritten)

- **L277** — `Database | Supabase (PostgreSQL + RLS) | Row-level security enforces idea isolation at DB layer` — **SUPERSEDED** (no Supabase database is built).
- **L278** — `Auth | Supabase Auth | Email verification, JWT, password reset — no custom auth` — **SUPERSEDED** (no Supabase authentication is built).
- **L161** — `All events are **append-only**. No event can be deleted or modified after write.` — **SUPERSEDED** (no append-only event store exists).
- **Header L3–L4** — `**Status:** Active` / `**Last Updated:** 2025-05-17` — **SUPERSEDED** as a current-authority claim.

Current-truth source: `web/app.py` L4 ("SESSION_STORE: in-memory, non-production,
temporary.") and L40 (`SESSION_STORE = {}`).

## 3. Authoritative current surfaces (govern in its place)

- **Governing authority:** `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` (canonical plan; phasing and status authority).
- **Current runtime truth:** `web/app.py` (in-memory, non-production Flask; temporary `SESSION_STORE`).
- **Conflict/stale evidence:** `docs/governance/evidence/phase0_evidence_lock/CONFLICT_REGISTER.md` (CR-2) and `docs/governance/evidence/phase0_evidence_lock/STALE_DOCUMENT_REGISTER.md` (SD-1).

## 4. Absence of a ratified definitive target architecture

There is **no ratified definitive "current target architecture" document**.
"Define the current target architecture" is a still-**pending** Phase 2
required-work item (plan L248, item 5). This increment does **not** define,
select, or ratify any replacement architecture; it only marks the stale document
historical and points to the governing plan and the current runtime truth.

## 5. Body-preservation method

A HISTORICAL/SUPERSEDED banner and authoritative pointer are inserted immediately
after the H1 title (`# Architecture Decision Document`). The existing base content
from `**Version:** 1.0` through the end of the file (base blob
`d36ef57511e508aec92d31fc13f6bce1ddacb14b`) is preserved **byte-identical** below
the banner. No body content is rewritten or deleted.

## 6. Scope (exactly four files)

1. **MODIFY** `docs/ARCHITECTURE_DECISION.md` — banner only (body preserved byte-identical).
2. **ADD** `docs/governance/evidence/phase2_governance_corrections/P2I2_STALE_ARCHITECTURE_DECISION_SUPERSESSION.md` (this record).
3. **MODIFY** `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` — current-status synchronization (three approved fragments only).
4. **MODIFY** `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` — one append-only Increment 2 candidate record (prior content preserved as exact byte prefix).

No other file changes.

## 7. Excluded work and authority boundaries

Excluded (not touched, not defined, not activated): **SD-2; SD-3; SD-4; `CLAUDE.md`;
`OWNER_PRODUCT_IDENTITY_CORRECTION.md` §11; target-architecture definition;
core/adapter boundaries; product sequencing; branding boundaries; sponsor logos;
colors; Themes; registry boundaries; persistence/subscription rules;
`engine/domain_rules.py`; any code/JSON/test/schema/CI/runtime change; `main`
reconciliation; Phase 3 or downstream activation; Increment 2 formal closure.**

```
PHASE 2:                  IN PROGRESS — INCREMENT 2 ONLY (this candidate); NO OTHER PHASE 2 INCREMENT AUTHORIZED
CENTRAL BRANDING BOUNDARIES:  SEPARATELY GATED FUTURE PHASE 2 WORK — NOT YET AUTHORIZED
PHASE 3 AND LATER:        NOT STARTED / NOT AUTHORIZED
PRODUCT STATUS:           DEMO_READY_WITH_LIMITATIONS / NOT PRODUCTION READY
MAIN:                     STALE / UNRECONCILED (not touched here)
IMPLEMENTATION AUTHORITY: NONE
RELEASE AUTHORITY:        NONE
DEPLOYMENT AUTHORITY:     NONE
```

## 8. RED path

`DOCUMENTED NO-VALID-RED`. Documentation-only; it changes no runtime code, JSON,
behavior, or executable contract. Validation uses documentation consistency, exact
four-file scope, protected tree/blob verification, target-body byte-identity, and
ancestry — not a test transition.

## 9. Evidence classification

Phase 2 governance-correction evidence artifact (implementation candidate). It
becomes the authoritative Increment 2 supersession record only after independent
candidate review, owner acceptance, normal merge, and post-merge verification
(§0). It grants no implementation, release, or deployment authority and certifies
no runtime behavior.
