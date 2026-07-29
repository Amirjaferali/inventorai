# Phase 2 — Increment 2 — Formal Closure (Candidate) — Stale Architecture Decision Supersession (SD-1 / CR-2)

**Increment:** Phase 2 Increment 2 — Stale Architecture Decision Supersession
(SD-1 / CR-2; `docs/ARCHITECTURE_DECISION.md`).
**Type:** documentation-only formal-closure candidate. **DOCUMENTED NO-VALID-RED.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Closure candidate base (verified tip after PR #307):**
`82ee103259d24a79758d348207afc3fbd3f1c3d2`.

---

## 0. Lifecycle status (read first)

```
PHASE 2 INCREMENT 2:  MERGED AND POST-MERGE VERIFIED
                      FORMAL-CLOSURE CANDIDATE PREPARED
                      NOT YET FORMALLY CLOSED
```

This record is a **formal-closure candidate**. It does **not** assert that
Increment 2 is already formally closed.

## 1. Closure status is CONDITIONAL until the gates complete

Phase 2 Increment 2 becomes **FORMALLY CLOSED** **only after** all of:

```
independent candidate review
  -> owner acceptance
    -> normal merge
      -> post-merge verification
```

```
PHASE 2 INCREMENT 2:  FORMAL-CLOSURE CANDIDATE PREPARED
                      FORMALLY CLOSED ONLY AFTER INDEPENDENT REVIEW, OWNER ACCEPTANCE, NORMAL MERGE, AND POST-MERGE VERIFICATION
```

This candidate does **not** assert that formal closure has already occurred, and
no gate below its own preparation is presumed complete.

## 2. Increment identity and verified merge evidence (PR #307)

| Item | Value |
|---|---|
| PR | #307 — **MERGED / CLOSED** |
| Accepted candidate | `b43571aea319a464b6d888b4933904c3091542a3` |
| Merge commit | `82ee103259d24a79758d348207afc3fbd3f1c3d2` |
| Ordered parents | ① `42ccbe3a4c1d49843294a0bd63376d232a7f45dd` · ② `b43571aea319a464b6d888b4933904c3091542a3` |
| Merge tree == accepted candidate tree | `ed96f43cf3a66247eb93d239aca735c1ed89ee1c` (EQUAL) |
| Prior authoritative tip | `42ccbe3a4c1d49843294a0bd63376d232a7f45dd` |
| Authoritative tip after merge | `82ee103259d24a79758d348207afc3fbd3f1c3d2` |
| Post-merge verdict | **A — POST-MERGE PASS** |
| `main` | `0e89e4636399760965c9ff8086b465c90dbadf8e` — STALE / UNRECONCILED / UNTOUCHED |

## 3. What Increment 2 established (recap — not re-decided)

Increment 2 (merged candidate `b43571a`, four documentation files) established,
documentation-only, for **SD-1 / CR-2 only**:
- `docs/ARCHITECTURE_DECISION.md` marked **HISTORICAL / SUPERSEDED** (banner +
  authoritative pointer after the H1); its body from `**Version:** 1.0` through
  end-of-file **preserved byte-identical** (body blob
  `389f9488e82659d9cbb6701a75ec0c08ceffcc24`).
- Superseded stale claims: `Database | Supabase (PostgreSQL + RLS)` (L277),
  `Auth | Supabase Auth` (L278), "All events are append-only" (§7, L161), and the
  `Status: Active` / `Last Updated: 2025-05-17` header; current-truth source
  `web/app.py` (in-memory `SESSION_STORE = {}`).
- **No definitive current target architecture was defined** ("define the current
  target architecture" remains a separate pending Phase 2 item).
- New evidence record `P2I2_STALE_ARCHITECTURE_DECISION_SUPERSESSION.md`.

## 4. SD-1 / CR-2 closure statement

`SD-1` (`MISLEADING — NEEDS SUPERSESSION`, Phase 2) and `CR-2` (MEDIUM — stale
architecture document vs in-memory runtime) are **documentation-superseded** for
`docs/ARCHITECTURE_DECISION.md` by the merged Increment 2 banner and evidence
record — documentation-only; no code/JSON/runtime change and no target-architecture
definition. Only SD-1 / CR-2 for this one document is addressed; SD-2, SD-3, SD-4
and every other conflict remain untouched.

## 5. Lifecycle synchronization (candidate-time wording)

The merged candidate-time strings `IMPLEMENTATION CANDIDATE PREPARED` /
`NOT YET OWNER-ACCEPTED` / `NOT YET MERGED` / `NOT YET FORMALLY CLOSED` were
accurate at candidate preparation. Upon this closure they are **superseded as
current status**: the plan and roadmap current-status surfaces are synchronized to
`MERGED AND POST-MERGE VERIFIED` / `FORMAL-CLOSURE CANDIDATE PREPARED` /
`NOT YET FORMALLY CLOSED` now, and to `FORMALLY CLOSED` only upon completion of the
§1 gates (a later post-closure synchronization). `P2I2_STALE_ARCHITECTURE_DECISION_SUPERSESSION.md`
§0 is **preserved unchanged as history** — its candidate-time wording stands as a
record of that artifact's state at creation and is not rewritten.

## 6. Phase boundary

```
PHASE 2 INCREMENT 2:  FORMAL-CLOSURE CANDIDATE (closes only after the §1 gates)
PHASE 2 OVERALL:      IN PROGRESS — NO OTHER PHASE 2 INCREMENT AUTHORIZED
PHASE 3 AND LATER:    NOT STARTED — NOT AUTHORIZED
```

Central-branding-boundaries work remains `SEPARATELY GATED FUTURE PHASE 2 WORK —
NOT YET AUTHORIZED`. Formal closure of Increment 2 does not declare Phase 2 closed.

## 7. Authority boundaries (preserved)

```
PRODUCT STATUS:            DEMO_READY_WITH_LIMITATIONS / NOT PRODUCTION READY
MAIN:                      STALE / UNRECONCILED / UNTOUCHED
IMPLEMENTATION AUTHORITY:  NONE
RELEASE AUTHORITY:         NONE
DEPLOYMENT AUTHORITY:      NONE
```

No target-architecture / core-adapter / sequencing / branding / registry /
persistence-subscription definition; no SD-2/SD-3/SD-4; no `CLAUDE.md`; no §11; no
`engine/domain_rules.py`; no code/JSON/schema/test/CI/runtime change; no `main`
reconciliation; no next increment; no Phase 3 or downstream activation.

## 8. RED path

`DOCUMENTED NO-VALID-RED`. Documentation-only; it changes no runtime code, JSON,
behavior, or executable contract. Validation uses documentation consistency, exact
three-file scope, ancestry, protected tree/blob verification, and the verified
`merge tree == accepted candidate tree` identity — not a test transition.

## 9. In-scope files (exactly three)

1. **ADD** `docs/governance/evidence/phase2_governance_corrections/P2I2_FORMAL_CLOSURE.md` (this record).
2. **MODIFY** `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` — three current-status fragments synchronized (L10/L11 only).
3. **MODIFY** `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` — one append-only closure-candidate record (prior content preserved as exact byte prefix).

No re-edit of `docs/ARCHITECTURE_DECISION.md` or
`P2I2_STALE_ARCHITECTURE_DECISION_SUPERSESSION.md`; no accepted Phase 0/Phase 1/
Increment 1 record modified; no code/JSON/schema/test/CI change.

## 10. Evidence classification

Phase 2 governance-correction **formal-closure candidate** artifact. It becomes the
authoritative Increment 2 closure record only after independent candidate review,
owner acceptance, normal merge, and post-merge verification (§1). It grants no
implementation, release, or deployment authority and certifies no runtime behavior.
