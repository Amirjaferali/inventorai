# RW-1 / SD-3 — Formal Closure (Candidate) — Governance Boot-Path / Authority-Order Path Correction

**Item:** RW-1 / SD-3 — repair of the governance boot-path / authority-order path
drift in `CLAUDE.md` (Phase 0 stale-document `SD-3`).
**Type:** documentation-only formal-closure candidate. **DOCUMENTED NO-VALID-RED.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Closure candidate base (verified live tip after PR #316):**
`7f10d036b7506b1e5d7b26301f1ea21e5a5e9e47`.

---

## 0. Lifecycle status (read first)

```
RW-1 / SD-3:  FORMAL-CLOSURE CANDIDATE
              SUBSTANTIVE CORRECTION MERGED AND VERIFIED
              NOT YET FORMALLY CLOSED
              POST-CLOSURE SYNCHRONIZATION STILL PENDING
```

This record is a **formal-closure candidate**. It does **not** assert that RW-1 is
already formally closed or durably closed. Per the owner-selected closure path
**C**, durable and full formal closure requires this formal-closure record **and**
a **separate post-closure synchronization** stage, each independently reviewed,
owner-accepted, normally merged, and post-merge verified.

## 1. Closure is CONDITIONAL until the gates complete

RW-1 / SD-3 becomes **FORMALLY CLOSED** only after this formal-closure candidate
completes:

```
independent review
  -> owner acceptance
    -> normal merge
      -> post-merge verification
```

and it becomes **DURABLY AND FULLY FORMALLY CLOSED** only after the subsequent,
separately-gated **post-closure synchronization** stage completes the same gates.
This candidate presumes no gate below its own preparation is complete.

## 2. RW-1 / SD-3 name and purpose

**Name:** RW-1 / SD-3 — governance boot-path / authority-order path correction.
**Purpose:** repair the `CLAUDE.md` "Active Governance Documents" and "Document
Authority Order" sections identified by Phase 0 stale-document `SD-3`, in which the
governed files were referenced by **bare filename with no path**, diverging from
the repository's governed path convention.

## 3. Original gap

`SD-3` recorded that `CLAUDE.md` referenced `MVP_SCOPE_FREEZE.md`,
`GOVERNANCE_MODEL.md`, and `DECISION_PROGRESSION_MODEL.md` (and, in the authority
order, `CLAUDE.md`) by bare filename without an explicit path, and that two
review-scope names (`START_HERE`, `ARCHITECTURE_INDEX`) were absent at the tip —
a minor governance boot-path / authority-order path drift.

## 4. Substantive candidate and verified merge evidence (PR #316)

| Item | Value |
|---|---|
| Authoritative prerequisite (substantive base) | `1117fee9d7c0a0df9873200ea82857c4472fa2ad` |
| Substantive candidate | `ac91fa2688e8137d29bde4065428a05876ab06dc` |
| Substantive candidate parent | `1117fee9d7c0a0df9873200ea82857c4472fa2ad` |
| Substantive candidate tree | `4aa1bde3d6b230a43b483efba13eafaf8ff111f7` |
| Substantive PR | #316 — **MERGED / CLOSED** (normal merge commit) |
| Substantive merge commit | `7f10d036b7506b1e5d7b26301f1ea21e5a5e9e47` |
| Ordered merge parents | ① `1117fee9d7c0a0df9873200ea82857c4472fa2ad` · ② `ac91fa2688e8137d29bde4065428a05876ab06dc` |
| Merge tree == accepted candidate tree | `4aa1bde3d6b230a43b483efba13eafaf8ff111f7` (EQUAL) |
| Accepted independent verdict | **B — INDEPENDENT RW-1 / SD-3 PASS WITH NON-BLOCKING OBSERVATIONS** |
| Accepted post-merge verdict | **A — PR #316 POST-MERGE PASS** |
| `main` | `0e89e4636399760965c9ff8086b465c90dbadf8e` — STALE / UNRECONCILED / UNTOUCHED |

The merge tree equals the accepted candidate tree exactly, and the substantive
candidate `ac91fa2` is an ancestor of the authoritative tip.

## 5. Exact substantive scope (PR #316; verified)

```
M  CLAUDE.md
M  docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md
M  docs/governance/ACTIVE_EXECUTION_ROADMAP.md
```
`3 MODIFY · 0 ADD · 16 insertions(+) · 10 deletions(-)` — documentation-only.

## 6. What the substantive correction established (recap — not re-decided)

- The `SD-3`-named files (`MVP_SCOPE_FREEZE.md`, `GOVERNANCE_MODEL.md`,
  `DECISION_PROGRESSION_MODEL.md`, `CLAUDE.md`) were independently confirmed to
  exist at the **repository root**, and **no copies** exist under `docs/governance/`.
- Each `SD-3`-identified reference was therefore made an explicit
  **repository-root-relative** path (`./NAME`), with a clarifying note in the
  Document Authority Order section — truthfully aligned to the actual locations;
  **no** reference was relocated to a non-existent `docs/governance/` path.
- The authority hierarchy, ordering (1. MVP_SCOPE_FREEZE → 2. GOVERNANCE_MODEL →
  3. CLAUDE → 4. DECISION_PROGRESSION_MODEL), statuses (ACTIVE / ACTIVE FREEZE /
  PROPOSED), and semantics were preserved; no authority source was added or
  removed; the edit was not broadened into a general `CLAUDE.md` rewrite.
- `START_HERE.md` and `ARCHITECTURE_INDEX.md` were **absent** at the tip and were
  **not** invented or added; their absence was recorded only as an observation.

This closure candidate makes **no** further edit to `CLAUDE.md`.

## 7. Confirmations required at closure

- **Root-located files truthfully referenced:** CONFIRMED — the correction uses
  explicit repository-root-relative paths matching the files' actual root
  locations.
- **Authority hierarchy / ordering / statuses / semantics preserved:** CONFIRMED.
- **START_HERE.md / ARCHITECTURE_INDEX.md absent and not invented or added:**
  CONFIRMED (absent everywhere in the tree; not added).
- **Protected artifacts unchanged:** CONFIRMED (see §10).
- **No implementation / RW-2 / RW-7 / Phase 2 closure / Phase 3 / main
  reconciliation / Structured Technical Guidance work occurred:** CONFIRMED.
- **Post-closure synchronization remains separately gated:** CONFIRMED.

## 8. Accepted independent-review observations (five; all NON-BLOCKING)

The accepted independent verdict was
**`B — INDEPENDENT RW-1 / SD-3 PASS WITH NON-BLOCKING OBSERVATIONS`**, carrying
**five (5)** observations. All five were **reviewed and accepted by the owner as
non-blocking** before authorizing this formal-closure stage. They are historical,
accepted observations — **not** defects repaired by this formal-closure candidate.

- **O1 — OD-R / OD-S closure evidence location** (`NON-BLOCKING — EVIDENCE
  LOCATION`): the repository at the substantive prerequisite did not itself contain
  every owner-held Stage C review and post-merge verification artifact, but the
  owner confirmed and accepted the existing PR #315 post-merge evidence and the
  durable-closure result (`OD-R / OD-S: DURABLY AND FULLY FORMALLY CLOSED`).
- **O2 — Root-relative note placement** (`NON-BLOCKING — EDITORIAL`): the
  repository-root-relative clarification appears in the Document Authority Order
  section, while the Active Governance Documents section relies on the same
  path-notation context.
- **O3 — Commit signature verification** (`NON-BLOCKING — VERIFICATION
  ENVIRONMENT`): the SSH signature could not be cryptographically validated because
  the independent-review environment lacked an allowed-signers trust anchor; commit,
  parent, tree, bundle, and content identities were independently verified.
- **O4 — Prerequisite reachability topology** (`NON-BLOCKING — GOVERNANCE
  TOPOLOGY`): the prerequisite was reachable from the authoritative feature branch
  and not from stale/unreconciled `main`.
- **O5 — Cosmetic alignment** (`NON-BLOCKING — COSMETIC`): column padding changed
  only to accommodate the added path prefixes.

## 9. Lifecycle synchronization (candidate-time wording)

The substantive candidate-time strings (`DOCUMENTATION-CORRECTION CANDIDATE / NOT
YET REVIEWED / NOT YET MERGED / NOT YET CLOSED`) were accurate at substantive
preparation. Upon this closure candidate the plan and roadmap current-status
surfaces are synchronized to `FORMAL-CLOSURE CANDIDATE / SUBSTANTIVE CORRECTION
MERGED AND VERIFIED / NOT YET FORMALLY CLOSED / POST-CLOSURE SYNCHRONIZATION STILL
PENDING`, and to `FORMALLY CLOSED` only upon completion of the §1 formal-closure
gates, and to `DURABLY AND FULLY FORMALLY CLOSED` only upon completion of the
separate post-closure synchronization stage.

## 10. Protected artifacts unchanged (this closure candidate)

This candidate changes exactly three files (§12). The following remain
**byte-identical**: `CLAUDE.md` (blob `1ec4af23ce46a42cb2c50200fc63bbd7b684e243`);
all `engine/`, `web/`, `tests/`; all JSON, schema, CI, runtime, persistence, and
prompt artifacts; the OD-R record (`1685bd80…`), the OD-S record (`8984bb24…`),
`OD-R_OD-S_FORMAL_CLOSURE.md` (`4157d461…`), `P2I1/P2I2/P2I3_FORMAL_CLOSURE.md`
(`382e8c25…` / `747cf7a4…` / `373c26fa…`), `OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
`docs/ARCHITECTURE_DECISION.md`, `DOMAIN_SCOPE_GOVERNANCE_INCONSISTENCY_REPORT.md`,
all prior evidence records, and `main` (`0e89e4636399760965c9ff8086b465c90dbadf8e`).

## 11. Phase / authority boundary (preserved)

```
PHASE 2 INCREMENT 1 / 2 / 3:  FORMALLY CLOSED
OD-R / OD-S:                  DURABLY AND FULLY FORMALLY CLOSED
RW-1 / SD-3:                  FORMAL-CLOSURE CANDIDATE (closes only after §1; durable only after post-closure synchronization)
PHASE 2 OVERALL:              IN PROGRESS — NO OTHER PHASE 2 INCREMENT AUTHORIZED
PHASE 3 AND LATER:            NOT STARTED — NOT AUTHORIZED
PRODUCT STATUS:               DEMO_READY_WITH_LIMITATIONS / NOT PRODUCTION READY
MAIN:                         STALE / UNRECONCILED / UNTOUCHED
IMPLEMENTATION AUTHORITY:     NONE
RELEASE AUTHORITY:            NONE
DEPLOYMENT AUTHORITY:         NONE
```

RW-2 and RW-7 are **not** begun. Phase 2 is **not** declared closed. Post-closure
synchronization is **separately gated** and not authorized by this record.

## 12. In-scope files (exactly three)

1. **ADD** `docs/governance/evidence/phase2_governance_corrections/RW-1_SD-3_FORMAL_CLOSURE.md` (this record).
2. **MODIFY** `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` — RW-1 / SD-3 lifecycle-status synchronization only.
3. **MODIFY** `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` — one append-only closure-candidate record (prior content preserved as an exact byte prefix).

No re-edit of `CLAUDE.md`; no accepted Phase 0 / Phase 1 / Increment 1 / Increment 2 /
Increment 3 / OD-R / OD-S record modified; no code / JSON / schema / test / CI /
runtime change.

## 13. RED path

`DOCUMENTED NO-VALID-RED`. Documentation-only; it changes no runtime code, JSON,
behavior, or executable contract. Validation uses documentation consistency, exact
three-file scope, ancestry, protected tree/blob verification, roadmap byte-prefix
preservation, and the verified `merge tree == accepted candidate tree` identity —
not a test transition.

## 14. Evidence classification

Phase 2 governance-correction **formal-closure candidate** artifact. It becomes the
authoritative RW-1 / SD-3 formal-closure record only after independent review,
owner acceptance, normal merge, and post-merge verification (§1); RW-1 becomes
durably and fully formally closed only after the subsequent separately-gated
post-closure synchronization. It grants no implementation, release, or deployment
authority and certifies no runtime behavior.
