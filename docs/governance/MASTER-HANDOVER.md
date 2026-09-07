# InventorAI — Successor Handover

<a id="current-successor-routing--post-pr-625"></a>
## Current successor routing — post-PR #626

**ACTIVE CONTRACT: NONE**, as declared in
[ACTIVE_INCREMENT_CONTRACT.md](ACTIVE_INCREMENT_CONTRACT.md#current-authority--post-return-declaration).
No current product implementation or documentation-sync mandate exists.
PR #626 documentation sync: **COMPLETED / MERGED / POST-MERGE VERIFIED**.
The PR #625 product milestone remains closed. Verified authoritative tip/closure
baseline: `16890c8a121ba9bf4aea960ed046ab5e9e34cc5f` on
`feature/atomic-json-session-persistence`, with merge tree
`d9b3b6cf522be46a03bf896788fa2fd633a54c24`, identical to the reviewed documentation
candidate tree and with an empty candidate-to-merge diff. Exact evidence is in
[the roadmap closure entry](ACTIVE_EXECUTION_ROADMAP.md#pr-626-documentation-sync-completed-and-post-return-authority);
the prior [PRs #620–#625 entry](ACTIVE_EXECUTION_ROADMAP.md#pr-625-verified-product-closure-and-recent-increments)
remains historical evidence.
Resolve the live tip from Git; this recorded baseline is not a permanent pin.

Use CLAUDE.md's single boot sequence, the concise
[CURRENT_PROJECT_STATE.md](CURRENT_PROJECT_STATE.md) entry and the active contract.
CLAUDE.md's older A1 current-authority summary is superseded by the present Owner
instruction/current contract; its boot sequence and substantive safeguards remain.
Read only relevant current sections and latest Git evidence when work is authorized.
Do not load the whole historical stream or rerun completed evidence as a boot ritual.

**Operating automation: PLANNED — NOT ACTIVE.** Any future product, governance or
automation work requires a new explicit Owner authorization. The finite preparation
of this post-return closure candidate ends at its independent-review-ready return;
it leaves no active increment contract. No publication, PR, merge or deployment is
authorized for this candidate. Do not act on consumed A1/filter/PR #625/PR #626
permissions or old "next action" text.

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