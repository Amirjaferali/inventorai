# InventorAI — Current Project State

**Purpose:** the concise current-state entry point for every agent. It is **not** a second
roadmap. For detail, see the canonical plan
(`docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`), the
append-only `ACTIVE_EXECUTION_ROADMAP.md`, and the accepted owner-decision evidence indexed
by `docs/governance/OWNER_DECISION_REGISTER.md`.
**Keep concise; refresh at each phase/increment boundary.**

---

## Authoritative pointers

- **Authoritative branch:** `feature/atomic-json-session-persistence`.
- **Live tip:** resolve from Git each session
  (`git rev-parse origin/feature/atomic-json-session-persistence`). Do **not** trust a
  prose-pinned SHA. Last independently verified tip:
  `0330273b0d8b15fc66a285bcb9b866c6aa81b8e5` (PR #327 merge) — historical evidence only.
- **`main`:** `0e89e4636399760965c9ff8086b465c90dbadf8e` — STALE / UNRECONCILED / NOT authority.

## Phase and gate

- **Phase 1:** FORMALLY CLOSED. **Phase 2:** FORMALLY CLOSED (PR #325) and status-synchronized (PR #326).
- **Phases 3–10:** NOT STARTED / NOT AUTHORIZED. **Phase 3B:** NOT STARTED.
- **Completed gate:** Audit-Disposition & Handover-Gap Canonicalization + Lean-Governance
  adoption — **FORMALLY CLOSED** (merged via PR #327, merge `0330273b`; independent review
  `B — PASS WITH NON-BLOCKING OBSERVATIONS`; owner ACCEPTED AS-IS; post-merge PASS).
- **Lean Governance and Agent Continuity Protocol:** **MERGED AND EFFECTIVE** on the
  authoritative branch (this document, the Owner Decision Register, the Active Increment
  Contract, and the Handover Template are now the binding continuity inputs).
- **Current active work:** NONE — AWAITING NEXT OWNER-AUTHORIZED GATE. No implementation authority.
- **Next proposed gate (not started, not authorized here):** Phase 3A formal
  discovery/current-state inventory closure, or the minimum Lean-Governance-aligned
  preparation required by the canonical roadmap. A separate explicit owner authorization is
  required before any Phase 3A step.

## Product / runtime distinction

- **Product identity:** multi-domain and cross-domain idea-development platform.
- **Current experimental MVP runtime:** Electronics/Electrical only.
- **Product state:** `DEMO_READY_WITH_LIMITATIONS`. **Production ready:** NO. **Deployment authority:** NONE.
- **Historical implementation:** MATERIALLY CONFORMING (independent audit verdict
  `B — MATERIAL CONFORMANCE WITH DOCUMENTATION DRIFT`; see OD-T).

## Implemented capabilities (current)

- Deterministic engine (scoring, progression, gaps, safety signals) — transport-free core.
- Flask app; Path N guided journey; electronics/electrical admission gate; decision workspace;
  success-criteria; deliverable view; FDC-001 narrow canonical-JSON decision-record export.
- In-memory `SESSION_STORE` only.

## Not implemented / not authorized

- Durable persistence; accounts; authentication; authorization; billing/subscription.
- ACV (Approximate Concept Visualization); Direct Output Download (PDF); Email Delivery.
- Sponsors/themes; administrative notice; privacy-control implementation; full Arabic/RTL;
  accessibility; multi-domain runtime; Path T / FORM T (BLOCKED).
- Structured Technical Guidance — RESERVED / INACTIVE / separately authorized.

## Accepted limitations (honest, not waived)

End-to-end runtime invocation not certified; `main` stale/unreconciled; `/tmp` transcript
handling (Phase 4 remediation); latent domain packs (Phase 6); pre-existing
`tests/test_domain_registry.py` failing baseline (~31; Phase 6 / separately authorized);
narrow Arabic/RTL. Full register: OD-T and the canonical plan.

## Active holds / forbidden work now

No implementation, UI, runtime, engine, schema, database, prompt/AI, tests-as-gates,
domain activation, ACV/Download/Email, sponsors/notice/privacy implementation, Arabic/RTL,
accessibility, Structured Technical Guidance, Phase 3 activation, main reconciliation, or PR
merge is authorized by the current gate.

## Open owner decisions

None blocking the current gate. Phase 3B owner UX/product decisions are pending and are
staged (not decided) in `docs/governance/evidence/phase3_owner_decisions/PHASE_3B_OWNER_DECISION_AGENDA.md`.
