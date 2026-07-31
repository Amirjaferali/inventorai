# Phase 0 — Stale Document Register

**Phase:** Phase 0 — Evidence Lock and Governance Reconciliation.
**Official tip:** `1d1385f2140be4e8ab1612ce07596a2170cfa0a0`.
**Mode:** Read-only. **No stale source is edited in Phase 0.** Classifications:
`MISLEADING — NEEDS SUPERSESSION` · `ACTIVE — NEEDS CORRECTION` ·
`HISTORICAL — SAFE TO RETAIN` · `HISTORICAL — MISLEADING IF READ AS CURRENT`.

---

## SD-1 — `docs/ARCHITECTURE_DECISION.md` (last relevant commit `cce03b3589cc8227dbec8e30ad7f81ac273f7a7f`; dated 2025-05-17)

- **Exact stale text:** L277 "Database | Supabase (PostgreSQL + RLS) | Row-level security enforces idea isolation at DB layer"; L278 "Auth | Supabase Auth | Email verification, JWT, password reset — no custom auth"; L161 "All events are **append-only**. No event can be deleted or modified after write."
- **Exact current-truth text:** `web/app.py` (`df4836b…`) L4 "SESSION_STORE: in-memory, non-production, temporary."; L40 `SESSION_STORE = {}`.
- **Line ranges:** stale L161, L277–278 / truth `web/app.py` L4, L40.
- **Why stale:** describes a Supabase DB + Supabase Auth + append-only event-log architecture that is not built; runtime is in-memory Flask with no DB/auth.
- **Classification:** **MISLEADING — NEEDS SUPERSESSION** (Phase 2). Cross-ref CR-2.

## SD-2 — `docs/governance/DOMAIN_SCOPE_GOVERNANCE_INCONSISTENCY_REPORT.md` (last relevant commit `13264cd6339647789990afce2c0abf52d129ce7b`)

- **Exact stale text:** L119–120 "The generic `/start` route in `web/app.py` calls `infer_domain(idea_text)` and assigns the result to `state.domain`."; L121–126 "Through that route, a user may be routed into the `mechanical`, [medical, software] … the generic route."
- **Exact current-truth text:** `web/app.py` (`df4836b…`) L434 "`state.domain = DOMAIN_CONFIRM_VALUE`" (always electronics_electrical); strong-unsupported branch L402 → `UNSUPPORTED_DOMAIN_MESSAGE` return L407; L409–422 conflicting supported → `MECHANISM_GUIDANCE_MESSAGE`.
- **Line ranges:** stale L119–126 / truth `web/app.py` L391–445.
- **Why stale:** describes a superseded `/start` (the Domain Gate Entry UX increment changed it). The report itself (L105) notes "document header dates are the only sequencing signal."
- **Classification:** **HISTORICAL — MISLEADING IF READ AS CURRENT** (supersede/annotate in Phase 2). Cross-ref CR-1.

## SD-3 — `CLAUDE.md` "Active Governance Documents" / "Document Authority Order" (last relevant commit `4251e9977d96626b837d999e0b119f541decd752`)

- **Exact stale text:** "Document Authority Order" entries L304–307 (heading L301) "1. MVP_SCOPE_FREEZE.md … 2. GOVERNANCE_MODEL.md … 4. DECISION_PROGRESSION_MODEL.md" (bare filenames, no path).
- **Exact current-truth text:** these files exist at repo root (`MVP_SCOPE_FREEZE.md` `d63e783…`; `GOVERNANCE_MODEL.md`/`DECISION_PROGRESSION_MODEL.md` `51bbbf7…`); `START_HERE`/`ARCHITECTURE_INDEX` (named in the review scope) do not exist at the tip.
- **Line ranges:** Document Authority Order L301–307 (the related "Active Governance Documents" descriptive block is L263–299).
- **Why stale:** path-drift (bare names resolve at root but diverge from the `docs/governance/` convention); two review-scope names are absent.
- **Classification:** **ACTIVE — NEEDS CORRECTION (minor, path drift)** (Phase 2). Cross-ref CR-4.

## SD-4 — `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md` §11 (last relevant commit `5768d315e8bdf11eac8b639576dcd0232b88c514`)

- **Exact stale text:** L18–21 "EFFECTIVE only upon completion of all activation conditions in §11, including successful remote verification confirming HEAD = origin/main and ahead/behind = 0 0"; L343 same clause.
- **Exact current-truth text:** authoritative branch is `feature/atomic-json-session-persistence` (roadmap §4); `origin/main` = `0e89e4636399760965c9ff8086b465c90dbadf8e` ≠ official tip; SPV L46–47 already treats the amendment as "active."
- **Line ranges:** L18–21, L343 / SPV L46–47.
- **Why stale:** the activation condition references a branch model (`HEAD = origin/main`) that cannot be satisfied on the feature branch, while the amendment is treated operative.
- **Classification:** **ACTIVE — NEEDS CORRECTION / RATIFICATION** (Phase 1). Cross-ref CR-3 / OD-C.

## SD-5 — Plan header provenance line (last relevant commit `4251e9977d96626b837d999e0b119f541decd752`)

- **Exact stale text:** `PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` L3 "Draft revision: `v2 — owner review candidate`".
- **Exact current-truth text:** L10 "Document status: `CANONICAL GOVERNANCE PLAN — MERGED VIA PR #289 — POST-MERGE VERIFIED …`".
- **Line ranges:** L3 vs L10.
- **Why stale:** "owner review candidate" wording post-dates adoption; L3 is provenance, not a status claim.
- **Classification:** **HISTORICAL — SAFE TO RETAIN** (optional cleanup). Cross-ref CR-5.

## SD-6 — Superseded roadmap records (last relevant commit `4251e9977d96626b837d999e0b119f541decd752`)

- **Exact stale text:** earlier `ACTIVE_EXECUTION_ROADMAP.md` records stating the plan was "OWNER-DRAFT — NOT YET CANONICAL" and that "Push was 403-blocked in-session … awaits … before push or PR."
- **Exact current-truth text:** the appended PR #289/#290 post-merge synchronization records ("the plan is now canonical"; "prior … push/PR-pending statements are historical and superseded").
- **Line ranges:** roadmap tail (append-only history).
- **Why stale:** superseded by later append-only records.
- **Classification:** **HISTORICAL — SAFE TO RETAIN** (append-only roadmap; supersession stated in-line).

---

## Phase 3-preparation append (OD-T / DISC dispositions — documentation-only)

Added by the Audit-Disposition & Lean-Governance gate on verified tip
`7816bdaddd762c38e6fa8cbbf05b7de26022e306`. Append-only; no prior entry rewritten.

## SD-7 — `NEXT_SESSION.md` (root)
- **Why stale:** session-time notes snapshot; not current execution authority.
- **Action:** banner added — `HISTORICAL — NOT CURRENT EXECUTION AUTHORITY`; body preserved.
- **Classification:** **HISTORICAL — NOT CURRENT EXECUTION AUTHORITY** (DISC-008).

## SD-8 — `FUTURE_ARCHITECTURE_NOTES.md` (root)
- **Why stale:** forward-looking recommendations/concepts, not adopted authority.
- **Action:** banner added — `HISTORICAL / FORWARD-LOOKING — NOT CURRENT EXECUTION AUTHORITY`; body preserved.
- **Classification:** **HISTORICAL — NOT CURRENT EXECUTION AUTHORITY** (DISC-008/011).

## SD-9 — `VALIDATION_LOG.md` (root)
- **Why stale:** historical validation log; superseded by committed evidence/closures.
- **Action:** banner added — `HISTORICAL — NOT CURRENT EXECUTION AUTHORITY`; body preserved.
- **Classification:** **HISTORICAL — SAFE TO RETAIN / NOT CURRENT EXECUTION AUTHORITY** (DISC-008).

## SD-10 — `replay_debug.txt` (root, raw diagnostic output)
- **Why stale:** raw Replay Benchmark Runner diagnostic output; not current authority.
- **Action:** **register-only** disposition; the raw output is a forbidden-to-modify artifact,
  so **no in-file banner** is added. Recorded here as historical.
- **Classification:** **HISTORICAL — RAW OUTPUT — NOT CURRENT EXECUTION AUTHORITY** (DISC-016).

## SD-11 — `GOVERNANCE_MODEL.md` (root)
- **Why partially current:** parts of its authority/boot model remain referenced; its
  replay-era `Status: PROPOSED — pending review` header and some sections are historical.
- **Action:** bounded-purpose clarification banner added (NOT marked entirely obsolete);
  directs agents to resolve current authority from CLAUDE.md, current anchors, canonical plan,
  latest roadmap records, and current owner decisions.
- **Classification:** **PARTIALLY CURRENT — BOUNDED PURPOSE / NOT SOLE CURRENT AUTHORITY** (DISC-017).
