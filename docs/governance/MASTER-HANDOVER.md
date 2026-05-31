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
8. HEAD at time of this document: 65acf6e — OFFICIAL_BENCHMARK_BASELINE.md committed

---

*This document is produced to be accurate, not reassuring.*
*Verify everything against the repository before acting.*
*No implementation without evidence. No evidence without repository inspection.*