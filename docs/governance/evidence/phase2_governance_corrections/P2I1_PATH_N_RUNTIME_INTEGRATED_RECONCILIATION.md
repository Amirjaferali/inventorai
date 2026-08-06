# Phase 2 — Increment 1 — Governance Document-Authority and Stale-Document Reconciliation — Path N `runtime_integrated`

**Phase:** Phase 2 — Governance and Architecture Corrections
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Increment:** P2-I1 — Governance Document-Authority and Stale-Document
Reconciliation (Path N `runtime_integrated`). Addresses Phase 2 Required-Work
items 2 ("clarify document authority and activation conditions") and 3 ("mark
stale architecture documents as historical or superseded").
**Type:** documentation-only governance correction. **No engine/web/JSON/test/CI/
schema/runtime change. No end-to-end runtime certification. No downstream
activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official base:** `9d210bdaf4594c2692038c96561390df8379d0fc`.

---

## 1. Purpose and boundary

This record reconciles the **document-authority** of the Path N
`runtime_integrated` state. It establishes the current **canonical governance
status** and marks the stale anchor as historical/superseded. It changes no code,
JSON, or runtime behavior and certifies no end-to-end runtime invocation.

## 2. Authoritative status of `runtime_integrated` (P2-OD-1)

```
CANONICAL GOVERNANCE-RECORDED STATUS:   runtime_integrated=true
COMMITTED SUPPORTING EVIDENCE:          the JSON metadata is true and a Path N content loader exists
END-TO-END RUNTIME INVOCATION:          NOT CERTIFIED BY THIS DOCUMENTATION-ONLY INCREMENT
```

The **current canonical governance status is `runtime_integrated=true`**, per the
canonical `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` (L56–57: byte state `true`
in committed JSON metadata `97a1a51`, approved governance state EFFECTIVE; L192:
"Phase 4 implementation — `runtime_integrated=true` committed and remotely
verified"; L238; L353–357: the anchor's `runtime_integrated=false` "is superseded
by committed `97a1a51`"). The stale anchor must **not** be treated as current
authority.

## 3. Committed supporting evidence (recorded, not modified) (P2-OD-2)

- `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json`
  — line 10: `"runtime_integrated": true` (committed `97a1a51`; blob
  `82eec7bf23a22231e2ae20e7856b3a287e42b1c6` at this base). **Unchanged.**
- `engine/path_n_questions.py` — a committed Path N content loader
  ("Load and serve approved Path N question content"; `_load_content()` reads the
  JSON above). **Unchanged.**

These support `runtime_integrated=true`. Their existence **does not prove** the
loader is invoked end-to-end through the live user request → question-selection →
question-serving path:

```
UNVERIFIED RUNTIME FACT — NOT A DEFECT FINDING
```

No new runtime investigation or code execution is performed or authorized in this
increment. This record makes **no claim** that end-to-end runtime integration is
verified, certified, or closed.

## 4. `PATH_N_CURRENT_EXECUTION_ANCHOR.md` — HISTORICAL / SUPERSEDED (P2-OD-3)

`docs/governance/PATH_N_CURRENT_EXECUTION_ANCHOR.md` is marked **HISTORICAL /
SUPERSEDED** where the canonical roadmap already says so (roadmap L353–357). Its
statements `runtime_integrated=false` (e.g. L182) and "No Path N content loader
has been implemented" (L90) are **superseded and must not be treated as current
authority.** The anchor's body is **preserved** (a status banner and an
authoritative pointer are added in this increment; no body content is rewritten
or deleted). The current authority for `runtime_integrated` is the canonical
roadmap and the committed JSON metadata.

## 5. AA-2 relationship (from AA-2's exact documented scope; not inferred) (P2-OD-4)

From `docs/governance/AA-2_TERMINAL_LANE_CLOSURE_NOT_COMPLETED_AUTHORIZATION.md`
(unchanged by this increment):
- §1 — "One-time owner-authority ruling (**operational lane closure only**)";
  "**Applies to:** AA-2 (Idea A Emergence Timing Table lock) for historical
  sessions `a4e42558-3f56-4e53-a9bc-bedcc134044c` and
  `63aa184d-e214-4635-979a-2acfa7a664d5` **ONLY**"; "Its effectiveness closes only
  the AA-2 operational lane as NOT COMPLETED."
- §8 (L154) — "This ruling does NOT … **move runtime_integrated**, R2, FORM T,
  S-6, or AA-5."
- §9 (L157–166) — "Downstream Status Effects (Preserved)" lists
  `runtime_integrated:   false` under "**No status above is moved by this
  ruling.**"

**Established (documentary, not inferred):** AA-2 **governs a different lane** —
the AA-2 Idea-A timing-table-lock operational lane for two named historical
sessions only — and **expressly does not govern or move `runtime_integrated`**.
Its `runtime_integrated: false` (L166) is a **preserved, non-governing status
snapshot at AA-2's drafting baseline (HEAD `1f4f5d2165e8f3517336ff8c7e9f432a8af18a0c`)**,
which the ruling itself declares it does not move. AA-2 therefore neither
establishes nor conflicts with the canonical `runtime_integrated=true`.

**Preserved residual (not inferred):** the *chronological* ordering of AA-2's
drafting baseline `1f4f5d21…` relative to the `97a1a51` true-commit is not
established by this documentation-only increment:

```
AUTHORITY RELATIONSHIP REQUIRES DOCUMENTARY CLARIFICATION
```

(a later read-only ancestry check; not required for the governing conclusion
above, which rests on AA-2 §1/§2/§8/§9).

## 6. History preservation (P2-OD-5)

This record **prospectively supersedes only the stale `runtime_integrated=false`
characterization**. It does **not** modify any accepted Phase 0 or Phase 1
record. Specifically preserved unchanged (their historical statements stand as
history, superseded prospectively by this record):
- `docs/governance/evidence/phase0_evidence_lock/STALE_DOCUMENT_REGISTER.md`;
- `docs/governance/evidence/phase1_owner_decisions/OD-L_OD-M_UX_EXPOSURE_AND_UNSUPPORTED_DOMAIN.md`
  — its statements `RUNTIME_INTEGRATED: FALSE` / "Path N content integration
  INCOMPLETE" were inherited from the now-superseded anchor and are **superseded
  prospectively** by §2 above;
- `docs/governance/evidence/phase1_owner_decisions/PHASE_1_FORMAL_CLOSURE.md`
  §6 — same inherited `runtime_integrated=false` characterization, superseded
  prospectively.

**OD-L's Owner Decisions are unaffected and remain valid:** the user-facing
experience exposes **Path N only**, and **Path T / FORM T remains BLOCKED**. This
reconciliation touches only the stale `runtime_integrated` characterization, not
those decisions.

## 7. Documentation-only inconsistency vs runtime defect

- **Documentation-only inconsistency (reconciled here):** stale anchor (`false` /
  "no loader") vs current canonical status (`true`), and the derived stale
  statements in OD-L and the closure record. Reconciled by establishing canonical
  authority and marking the anchor superseded — **no code/JSON/runtime change.**
- **Not a defect finding:** the end-to-end runtime invocation is recorded as an
  `UNVERIFIED RUNTIME FACT — NOT A DEFECT FINDING`; no runtime malfunction is
  asserted or investigated.

## 8. What this increment authorizes

- Recording P2-OD-1…P2-OD-5 (documentation only).
- Adding a HISTORICAL/SUPERSEDED banner + authoritative pointer to the anchor
  (body preserved).
- The smallest plan status synchronization and one appended roadmap record.

## 9. What this increment prohibits

- Any engine/web code change; any JSON change; any runtime behavior change; any
  end-to-end runtime certification or new runtime investigation.
- Modifying any accepted Phase 0 or Phase 1 record (register, OD-L, closure, or
  any other).
- CR-3 §11 remediation; CR-4 path-drift remediation; architecture redesign;
  `main` reconciliation.
- Product UX/UI, branding/sponsor, API, domain activation, persistence, account,
  commercial, release, or deployment work; Phase 3 or any downstream activation.

## 10. Status and authority boundaries (unchanged)

```
PHASE 1:                  FORMALLY CLOSED
PHASE 2:                  IN PROGRESS — INCREMENT 1 ONLY (this record); no later increment begun
PHASE 3 AND LATER:        NOT STARTED / NOT AUTHORIZED
PRODUCT STATUS:           DEMO_READY_WITH_LIMITATIONS / NOT PRODUCTION READY
IMPLEMENTATION AUTHORITY: NONE
RELEASE AUTHORITY:        NONE
DEPLOYMENT AUTHORITY:     NONE
AUTHORITATIVE BRANCH:     feature/atomic-json-session-persistence
MAIN:                     STALE / UNRECONCILED (OD-Q; not touched here)
```

## 11. Evidence classification

This is a **Phase 2 governance-correction evidence artifact** (documentation
only). It is authoritative as the Path N `runtime_integrated` document-authority
reconciliation once independently reviewed, owner-accepted, merged, and
post-merge verified. It grants no implementation, release, or deployment
authority, and certifies no end-to-end runtime behavior.
