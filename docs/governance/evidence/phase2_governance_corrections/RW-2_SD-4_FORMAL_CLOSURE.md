# RW-2 / SD-4 — Formal Closure (Candidate) — Owner Product Identity Correction §11 Activation-Model Remediation

**Item:** RW-2 / SD-4 — remediation of the obsolete activation model in
`docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
**Conflict:** CR-3 — product-identity correction activation ambiguity.
**Type:** documentation-only formal-closure candidate. **DOCUMENTED NO-VALID-RED.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Closure candidate base (verified live tip after PR #319):** `30d8f9aa15ac47b189dfa1a34c764d15dd1a0dbd`.

---

## 0. Lifecycle status (read first)

```text
RW-2 / SD-4:  FORMAL-CLOSURE CANDIDATE
              SUBSTANTIVE REMEDIATION MERGED AND POST-MERGE VERIFIED
              CR-3 TEXTUAL REMEDIATION MERGED AND VERIFIED
              NOT YET FORMALLY CLOSED
              POST-CLOSURE SYNCHRONIZATION STILL PENDING
```

This record does not assert that RW-2, SD-4, or CR-3 is already formally or durably closed. Durable and full formal closure requires this formal-closure record and a separate post-closure synchronization, each independently reviewed, owner-accepted, normally merged, and post-merge verified.

## 1. Closure is conditional until the gates complete

RW-2 / SD-4 and CR-3 become **FORMALLY CLOSED** only after this candidate completes:

```text
independent review
  -> owner acceptance
    -> normal merge
      -> post-merge verification
```

They become **DURABLY AND FULLY FORMALLY CLOSED** only after the later, separately gated post-closure synchronization completes the same gates.

## 2. Name and purpose

**Name:** RW-2 / SD-4 — Owner Product Identity Correction §11 activation-model remediation.

**Purpose:** replace the obsolete operative activation mechanism tied to `origin/main`, `HEAD = origin/main`, and `ahead/behind = 0 0` with the current governed official-branch authority model, while preserving the owner-ratified substantive product identity and historical evidence.

## 3. Original gap

OD-C ratified the substantive product identity but identified that the original §11 activation mechanism depended on a branch and local-state condition that was not the current authoritative governance model. CR-3 therefore remained owner-decision resolved but textually pending until the Phase 2 remediation completed review, merge, and verification.

## 4. Substantive candidate and verified merge evidence — PR #319

| Item | Value |
|---|---|
| Authoritative prerequisite | `90b068edbba683a512390fc11e5bad0c875c64b8` |
| Substantive candidate | `a323b9c0046c0d3622c6cbf38e4624537567c433` |
| Candidate parent | `90b068edbba683a512390fc11e5bad0c875c64b8` |
| Candidate tree | `bee53f152c8c36c7915343455926685769b4080b` |
| Substantive PR | #319 — **MERGED / CLOSED** |
| Substantive merge commit | `30d8f9aa15ac47b189dfa1a34c764d15dd1a0dbd` |
| Ordered merge parents | ① `90b068edbba683a512390fc11e5bad0c875c64b8` · ② `a323b9c0046c0d3622c6cbf38e4624537567c433` |
| Merge tree == accepted candidate tree | `bee53f152c8c36c7915343455926685769b4080b` — EQUAL |
| Accepted independent verdict | **B — INDEPENDENT RW-2 / SD-4 SUBSTANTIVE REVIEW PASS WITH NON-BLOCKING OBSERVATIONS** |
| Accepted post-merge result | **POST-MERGE VERIFIED** |
| `main` | `0e89e4636399760965c9ff8086b465c90dbadf8e` — STALE / UNRECONCILED / UNTOUCHED |

## 5. Exact substantive scope — PR #319

```text
M  docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md
```

```text
1 file changed
48 insertions(+)
28 deletions(-)
```

Documentation-only. No code, runtime, JSON, schema, test, CI, UI, persistence, account, authentication, subscription, billing, release, or deployment change occurred.

## 6. What the substantive remediation established

- The owner-ratified product identity remains unchanged.
- The obsolete positive activation requirements tied to `origin/main`, `HEAD = origin/main`, and `ahead/behind = 0 0` are no longer operative.
- The authoritative execution branch is identified by the latest committed governance sources, and its live tip is resolved from Git.
- An unmerged transport ref, review branch, local commit, or pull request has no authoritative repository effect merely by existing.
- No historical drafting SHA or prose-pinned SHA is treated as the current live authoritative tip.
- The remediation does not claim that the obsolete condition was historically satisfied.
- Historical Phase 0 and Phase 1 evidence remains preserved.

This closure candidate makes no further edit to `OWNER_PRODUCT_IDENTITY_CORRECTION.md`.

## 7. Accepted independent-review observations

The accepted verdict was **PASS WITH NON-BLOCKING OBSERVATIONS**; blocking findings were none. The four accepted observations concerned §14 declarative framing, §1 post-merge status perspective, later lifecycle synchronization, and one cosmetic rewrap. None required changing the accepted substantive candidate.

## 8. Confirmations required at closure

- Exact one-file substantive scope: **CONFIRMED**.
- Merge tree equals accepted candidate tree: **CONFIRMED**.
- Owner-ratified identity preserved: **CONFIRMED**.
- Obsolete operative activation language removed: **CONFIRMED**.
- No false historical satisfaction claim: **CONFIRMED**.
- No SHA-pinned live authority model: **CONFIRMED**.
- Historical evidence unchanged: **CONFIRMED**.
- No implementation or Phase 3 activation: **CONFIRMED**.
- Separate post-closure synchronization remains required: **CONFIRMED**.

## 9. Bounded lifecycle-status reconciliation

- RW-1 / SD-3 is synchronized to **DURABLY AND FULLY FORMALLY CLOSED** through PR #318, merge `90b068edbba683a512390fc11e5bad0c875c64b8`.
- CR-3 is synchronized to **TEXTUAL REMEDIATION MERGED AND POST-MERGE VERIFIED — FORMAL CLOSURE PENDING**.
- RW-2 / SD-4 is synchronized to **FORMAL-CLOSURE CANDIDATE — SUBSTANTIVE REMEDIATION MERGED AND VERIFIED — NOT YET FORMALLY CLOSED — POST-CLOSURE SYNCHRONIZATION STILL PENDING**.

Earlier roadmap records are preserved and not rewritten.

## 10. Protected artifacts unchanged

This candidate changes exactly three files. `OWNER_PRODUCT_IDENTITY_CORRECTION.md`, OD-C, Phase 0 evidence, `CLAUDE.md`, prior formal-closure records, all `engine/`, `web/`, `tests/`, JSON, schema, CI, runtime, persistence, prompt, database, and architecture artifacts, and `main` remain unchanged.

## 11. Phase and authority boundary

```text
PHASE 2 INCREMENT 1 / 2 / 3: FORMALLY CLOSED
OD-R / OD-S:                 DURABLY AND FULLY FORMALLY CLOSED
RW-1 / SD-3:                 DURABLY AND FULLY FORMALLY CLOSED
RW-2 / SD-4:                 FORMAL-CLOSURE CANDIDATE
CR-3:                        TEXTUAL REMEDIATION MERGED AND VERIFIED
                              FORMAL CLOSURE PENDING
PHASE 2 OVERALL:             IN PROGRESS
RW-7:                        NOT STARTED
PHASE 3 AND LATER:           NOT STARTED / NOT AUTHORIZED
PRODUCT STATUS:              DEMO_READY_WITH_LIMITATIONS / NOT PRODUCTION READY
MAIN:                        STALE / UNRECONCILED / UNTOUCHED
IMPLEMENTATION AUTHORITY:    NONE
RELEASE AUTHORITY:           NONE
DEPLOYMENT AUTHORITY:        NONE
```

## 12. In-scope files — exactly three

1. **ADD** `docs/governance/evidence/phase2_governance_corrections/RW-2_SD-4_FORMAL_CLOSURE.md`
2. **MODIFY** `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md` — bounded lifecycle-status reconciliation only.
3. **MODIFY** `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` — one append-only record; prior 658219-byte content preserved as an exact byte prefix.

No fourth file.

## 13. RED path

`DOCUMENTED NO-VALID-RED`. Validation is based on exact scope, ancestry, merge identity, protected hashes, documentation consistency, roadmap byte-prefix preservation, and `git diff --check`.

## 14. Evidence classification

This record becomes authoritative only after independent review, owner acceptance, normal merge, and post-merge verification. Durable closure still requires the separately gated post-closure synchronization. It grants no implementation, release, deployment, or Phase 3 authority.
