# InventorAI — Successor Handover

## Current successor routing — post-PR #625

**Only current authority:** the bounded source-of-truth documentation sync recorded
in [ACTIVE_INCREMENT_CONTRACT.md](ACTIVE_INCREMENT_CONTRACT.md). The PR #625 product
milestone is **CLOSED — MERGED AND POST-MERGE VERIFIED**. Its verified authoritative
tip/documentation baseline is `ab5915e68851b25e46d5742ec49877b50eebee5c` on
`feature/atomic-json-session-persistence`, with merge tree
`04c25394547558e82a6bf379671d7eca2c64155d`, identical to the reviewed candidate tree
and with an empty candidate-to-merge diff. The exact evidence and PRs #620–#625 are
in [the roadmap closure entry](ACTIVE_EXECUTION_ROADMAP.md#pr-625-verified-product-closure-and-recent-increments).
Resolve the live tip from Git; this recorded baseline is not a permanent pin.

Use CLAUDE.md's single boot sequence, the concise
[CURRENT_PROJECT_STATE.md](CURRENT_PROJECT_STATE.md) entry and the active contract.
CLAUDE.md's older A1 current-authority summary is superseded by the present Owner
instruction/current contract; its boot sequence and substantive safeguards remain.
Only relevant current sections and latest Git evidence are needed for this sync.
Do not load the whole historical stream or rerun completed evidence as a boot ritual.

The **operating-automation build is PLANNED — NOT ACTIVE** under this synchronization.
This local documentation candidate ends at one independent-review-ready return.
No product implementation, merge, deployment or successor scope is authorized.
Do not act on consumed A1/filter/PR #625 permissions or old "next action" text.
An incoming agent must establish a still-applicable Owner mandate before any new work.

Preserve all [open gates, issues and observations](CURRENT_PROJECT_STATE.md#preserved-state-and-boundaries),
their existing owners and return conditions. FDC-001 / DecisionRecord stays canonical.
No closed product work or governance lane is reopened; no new source-of-truth document,
external-evidence linkage, gate closure or automation implementation is created here.

## Historical handover body — superseded operating instructions

The body below is preserved verbatim as historical evidence, not current execution
authority. Its chat-only authority prohibition, separate commit approval, sole-handover
claim, full-document boot reading, automatic benchmark rerun and old HEAD instructions
are superseded by current Lean §2/§§3–5B, AHAEP and CLAUDE.md's single boot sequence.
A direct Owner instruction takes effect on receipt under Lean §2; the active contract
records successor-relevant authority. Existing technical invariants retain their
substantive owners and are not relaxed by this notice.

**Rule:** A claim has standing only at the level it is documented.
Chat-only conclusions do not supersede committed artifacts.
Planned artifacts have no standing until committed.

---

## 18. ARCHITECTURAL INVARIANTS — NEVER VIOLATE

1. `progression_loop.py` must NEVER contain domain-specific branching
2. AI must NEVER control maturity, gaps, or gate decisions
3. Official benchmark (WPS001) must remain at 0 failed — see OFFICIAL_BENCHMARK_BASELINE.md
4. Web routes must contain no business logic
5. `idea_summary` must not be AI-generated or overwritten after first capture
6. Platform must never optimize for protocol completion at the expense of user
   progression toward implementation readiness

---

## 19. GOVERNANCE RULE

**Work Completed is not Work Preserved**

Every conclusion requires:

1. Evidence collected
2. Artifact written
3. Artifact location identified
4. Status assigned (ACTIVE / HISTORICAL / DEPRECATED)
5. Supersession relationship documented
6. Commit authorized by owner before implementation

**Evidence first. Documentation second. Decision third. Implementation last.**

---

## 20. WARNING — NON-AUTHORITATIVE HANDOVERS

Do not rely on any handover document other than the latest committed version
of MASTER-HANDOVER.md.

All prior handover documents produced in chat are non-authoritative from the
moment this document is committed.

If MASTER-HANDOVER.md content is absent, the authoritative state is the repository
at the current HEAD combined with the governance documents listed in Section 7.

Verify repository state before acting. Never act on chat-only context alone.

---

## 21. FIRST STEPS FOR ANY INCOMING AGENT

1. Read this document completely
2. Run `git log --oneline --decorate -3` — confirm HEAD
3. Run `python -m pytest tests/test_wps001_invariants.py -v` — confirm WPS001 benchmark passes
4. Run `ls docs/governance/` — confirm committed artifacts match Section 7
5. Check Section 12 for open blockers before any action
6. Check Section 14 for authorization status before any action
7. Do NOT start implementation without explicit owner instruction
8. HEAD at time of this document: ce72c28 — STAGE3_READINESS_DECISION.md and AB-005_MISSING_EVIDENCE_SUPPLEMENT.md admitted at ce72c28. WPS001 restored at 65acf6e.

---

*This document is produced to be accurate, not reassuring.*
*Verify everything against the repository before acting.*
*No implementation without evidence. No evidence without repository inspection.*