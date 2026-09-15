# InventorAI — Successor Handover

<a id="current-successor-routing--post-pr-625"></a>
<a id="current-successor-routing--post-pr-653"></a>
## Current successor routing — post-PR #653

Repository **Amirjaferali/inventorai**, authoritative branch
**feature/atomic-json-session-persistence**; `main` is outside execution authority.
Current recorded authoritative merge baseline:
`e95292730eb31dede41ce1c153962187eb23a525`, the verified PR #653 merge result.
**Always resolve the live tip from Git**; this recorded baseline is evidence of its
moment, not a permanent pin.

**ACTIVE CONTRACT: NONE**, as declared in
[ACTIVE_INCREMENT_CONTRACT.md](ACTIVE_INCREMENT_CONTRACT.md#current-authority--post-652-declaration).
This means **no NEW implementation mandate is currently active**. It does NOT mean
that PRs #647–#652 lacked authority, that the Readiness runtime is unauthorized, that
the Manufacturing evidence owner is unauthorized, or that Commercial and Manufacturing
evidence capture are not authoritative: each was separately Owner-authorized, merged
and post-merge verified. Any new work requires a new explicit Owner authorization.

**Completed authoritative work.** PRs #647–#652 are completed authoritative
product/readiness work — the Commercial evidence owner and its capture surface, the
Manufacturing evidence owner and its capture surface on ONE shared
`readiness_evidence` substrate, readiness truth hardening, and the canonical Readiness
Snapshot. PR #653 is completed authoritative governance reconciliation work. The PR
#625 product milestone and the PR #626 documentation sync remain closed; their
recorded closure baselines are evidence at their own moments and are no longer the
current position.

**Current Readiness truth.** The Readiness Snapshot is **authoritative and read-only**
over three dimensions:

- Technical — `INSUFFICIENT_EVIDENCE` only.
- Commercial — `INSUFFICIENT_EVIDENCE` only.
- Manufacturing — `INSUFFICIENT_EVIDENCE` only.

There is **no** overall, composite, score, percentage or weakest-link readiness result
anywhere in the product, and no manufacturability conclusion. FDC-001 / DecisionRecord
stays the canonical decision owner.

**Positive Readiness remains RESERVED.** `PASS`, `PASS_WITH_CONDITIONS` and `HOLD` are
NOT authorized in the current version, nor is a qualifying-authority writer,
specialist promotion, human or external validation promotion, overall/composite
readiness, or automatic readiness advancement.

**Human and external evidence remain NOT AUTHORIZED**, including
`HUMAN-STUDY EXECUTION: NOT AUTHORIZED` and `EVIDENCE COLLECTION: NOT AUTHORIZED`. The
A2 claim-eligibility human-review evidence gate, CEHR / Route-B, T1-A′, HICR, RUN-004,
G-4-A, G-4-B, M-1, F-03 and F-04 keep their existing owners, triggers and return
conditions. Read them at
[preserved state and boundaries](CURRENT_PROJECT_STATE.md#preserved-state-and-boundaries)
rather than restating them here.

**PRE-FCORA / FCORA.** PRE-FCORA was **EXECUTED** previously and returned
**C — NOT READY**, solely because of governance-authority drift. **PR #653** repaired
the three primary authority surfaces; **this MASTER-HANDOVER sync** addresses the
remaining successor-facing drift. The differential PRE-FCORA recheck has **NOT** been
performed, and nothing here may be read as that recheck having passed. **FCORA: NOT
AUTHORIZED. NOT STARTED.**

**Routing.** Use CLAUDE.md's single boot sequence, the concise
[CURRENT_PROJECT_STATE.md](CURRENT_PROJECT_STATE.md) current entry and the active
contract. **CLAUDE.md's current single boot sequence and the current authority/state
files supersede the historical first-step instructions below:** a successor must NOT
treat the old HEAD `ce72c28`, the automatic WPS001 rerun text or any other Section 21
step as current routing, and must not load the whole historical stream or rerun
completed evidence as a boot ritual. CLAUDE.md's older A1 current-authority summary is
likewise superseded by the current contract, while its boot sequence and substantive
safeguards remain applicable. Read only relevant current sections and the latest Git
evidence when work is authorized.

**Operating automation: PLANNED — NOT ACTIVE.** This routing records already-existing
state and creates no authority: it authorizes no new implementation, no new readiness
capability, no FCORA, no deployment, no paid activation, no human study, no evidence
collection, no CAD/PCB/BOM, no supplier API and no MCP. Do not act on consumed
A1/filter/PR #625/PR #626 permissions or old "next action" text. No closed product
work or governance lane is reopened; no new source-of-truth document,
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