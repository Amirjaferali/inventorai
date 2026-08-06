# Phase 1 — Owner Decision OD-Q — Branch Strategy and Main-Branch Reconciliation Policy

**Phase:** Phase 1 — Owner Product Decisions
(of `docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`).
**Decision ID:** OD-Q (branch strategy and main-branch reconciliation policy).
**Scope:** documentation-only durable record of one accepted owner decision
(policy only). **No branch, `main`, tag, release, deployment, CI, workflow,
branch-protection, default-branch, runtime, or evidence change. No reconciliation.
No downstream activation.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified official base at authoring:** `95e2ca98c349d3b1386fdc214bd4d119eecec013`
(official tip after PR #300, which merged the OD-K increment).

---

## 1. Decision status

```
OD-Q — OWNER DECISION ACCEPTED
```

This establishes **policy only**. It selects, authorizes, and executes no
reconciliation, merge, fast-forward, rebase, force-push, branch/default-branch
change, tag move, release, or deployment. No other open owner decision is
resolved, CR-4 is not remediated, and no downstream phase is activated.

## 2. Accepted owner decision (verbatim)

> **OD-Q — OWNER DECISION ACCEPTED**
>
> THE CURRENT AUTHORITATIVE GOVERNING BRANCH SHALL REMAIN
> `feature/atomic-json-session-persistence` UNTIL A SEPARATE, OWNER-AUTHORIZED,
> INDEPENDENTLY REVIEWED, EVIDENCE-BACKED MAIN-BRANCH RECONCILIATION GATE IS
> FORMALLY COMPLETED. THE `main` BRANCH MUST NOT BE TREATED AS CURRENT,
> AUTHORITATIVE, RELEASE-READY, DEPLOYABLE, OR PRODUCTION-READY MERELY BECAUSE IT
> IS THE DEFAULT GITHUB BRANCH. NO AUTOMATIC, IMPLICIT, BULK, OR UNREVIEWED
> RECONCILIATION INTO `main` IS AUTHORIZED.

## 3. Distinguished status (must be read exactly)

```
AUTHORITATIVE GOVERNING BRANCH:            feature/atomic-json-session-persistence
CURRENT AUTHORITATIVE TIP AT DECISION BASE: 95e2ca98c349d3b1386fdc214bd4d119eecec013
CURRENT MAIN TIP:                          0e89e4636399760965c9ff8086b465c90dbadf8e
MAIN STATUS:                               STALE / UNRECONCILED / NOT CURRENT PRODUCT AUTHORITY
MAIN-ONLY COMMITS:                         0
AUTHORITATIVE-ONLY COMMITS:                640
CURRENT MERGE BASE:                        0e89e4636399760965c9ff8086b465c90dbadf8e
CURRENT TECHNICAL FAST-FORWARD POSSIBILITY: YES / INFORMATIONAL ONLY / NOT AUTHORIZED
AUTOMATIC RECONCILIATION:                  PROHIBITED
SEPARATE GOVERNED RECONCILIATION GATE:     REQUIRED
RECONCILIATION METHOD:                     NOT YET SELECTED
DEFAULT-BRANCH STATUS:                     DOES NOT ESTABLISH PRODUCT OR GOVERNANCE AUTHORITY
CR-4:                                      LOW / RECORDED / UNRESOLVED / NOT REMEDIATED BY THIS INCREMENT
CURRENT IMPLEMENTATION AUTHORITY:          NONE
CURRENT RELEASE AUTHORITY:                 NONE
CURRENT DEPLOYMENT AUTHORITY:              NONE
```

## 4. Prior Phase 0 recommendation status (context, not authority)

In the Phase 0 Open Owner Decisions Register OD-Q was recorded only as a
`RECOMMENDATION — NOT OWNER DECISION`: "decide a governed reconciliation policy."
This record now converts that recommendation into an **accepted decision**. The
closed Phase 0 registers are unchanged by this record.

## 5. Canonical evidence references (repository truth)

- Phase 0 register **OD-Q** (source basis CR-4; roadmap §4).
- **CR-4 — LOW** (Conflict Register): "Official vs main divergence + CLAUDE.md
  path drift"; "main is intentionally behind"; "Blocks Phase 1? No"; options
  (a) keep main behind / (b) plan a governed main reconciliation; "Not resolved
  here."
- Roadmap §4 (row): "Reconciliation of `origin/main` … with this lane branch is
  **a separate governed question, not decided here**"; multiple rows record
  "`main` remains `0e89e463…` and is outside these merges."
- Verified topology (read-only, at this base): `main` = `0e89e463…`; authoritative
  = `95e2ca98…`; merge-base = `0e89e463…` (= `main`); main-only 0, authoritative-only
  640; `main` is a strict ancestor of the authoritative branch.
- Release tag `refs/tags/phase-j-stable` (`4795a879…`) exists.
- `docs/governance/evidence/phase0_evidence_lock/OPEN_OWNER_DECISIONS_REGISTER.md`
  and `CONFLICT_REGISTER.md`.

## 6. Accepted interpretation

The authoritative governing branch remains `feature/atomic-json-session-persistence`;
`main` is stale/unreconciled and is **not** current product, governance, release,
or deployment authority despite being the default GitHub branch. Any
`main` reconciliation requires a separate, owner-authorized, independently
reviewed, evidence-backed gate. No automatic/implicit/bulk/unreviewed
reconciliation is authorized.

## 7. Rejected alternatives and reasons

| Alternative | Rejected because |
|---|---|
| Treat `main` as canonical/authoritative because it is the default branch | Default-branch status establishes no product/governance/release/deployment authority; `main` is 640 commits behind. |
| Auto/implicit/bulk reconcile `main` now | Prohibited by OD-Q; a default-branch change has operational (CI/protection/release/Pages/clone) implications requiring a governed gate. |
| Select the reconciliation method now | Deferred — git evidence favors fast-forward, but platform/operational checks are incomplete; method belongs to the gate. |
| Assume evidence/state is present on `main` | Must be independently verified there; not assumed. |
| Squash/reconstruct/force-push to reconcile | Would destroy evidence-bearing history and reviewed merge topology; prohibited without separately approved necessity and review. |

## 8. Authoritative-branch rule

The authoritative source of current product, technical, and governance truth
remains `feature/atomic-json-session-persistence`. Its tip at this decision base
is `95e2ca98c349d3b1386fdc214bd4d119eecec013`.

## 9. Current `main` status

`main` = `0e89e4636399760965c9ff8086b465c90dbadf8e` — **STALE / UNRECONCILED /
NOT CURRENT PRODUCT AUTHORITY**. It is behind the authoritative branch and must be
described honestly as intentional, governed, stale/unreconciled, and not yet
resolved.

## 10. Current exact branch SHAs

```
AUTHORITATIVE: 95e2ca98c349d3b1386fdc214bd4d119eecec013
MAIN:          0e89e4636399760965c9ff8086b465c90dbadf8e
```

## 11. Verified ancestry and ahead/behind facts

```
MERGE BASE:                 0e89e4636399760965c9ff8086b465c90dbadf8e  (= main tip)
MAIN-ONLY COMMITS:          0
AUTHORITATIVE-ONLY COMMITS: 640
MAIN IS ANCESTOR OF AUTHORITATIVE: YES
AUTHORITATIVE IS ANCESTOR OF MAIN: NO
```

`main` is a strict ancestor of the authoritative branch with no unique commits.

## 12. Technical fast-forward possibility vs governance authorization (explicit distinction)

```
TECHNICAL FAST-FORWARD POSSIBILITY: YES (informational only)
GOVERNANCE AUTHORIZATION:           NONE — automatic reconciliation PROHIBITED
```

That `main` could be fast-forwarded (strict ancestor, 0 unique commits, no
conflicts) is a **technical fact**, not owner authorization. Technical
possibility must **never** be represented as authorization.

## 13. Default-branch non-authority rule

Default-branch status does not establish product authority, governance authority,
release authority, deployment readiness, production readiness, or canonical
evidence status.

## 14. Release and deployment non-authority rule

No release or deployment is authorized. `main` must not be treated as
release-ready, deployable, or production-ready.

## 15. Reconciliation-gate requirements

A future main reconciliation must include: refreshed ancestry and ahead/behind
analysis; intervening-commit analysis; file and conflict analysis;
protected-evidence verification; branch-protection review; default-branch
configuration review; required-check and CI review; GitHub Pages and environment
review; release and deployment dependency review; tag review (including
`phase-j-stable`); downstream clone and contributor impact; legacy/stale branch
handling; rollback or recovery planning where applicable; independent review;
explicit owner acceptance; and post-reconciliation verification.

## 16. History-preservation rule

Reconciliation must preserve the authoritative branch history and accepted merge
topology.

## 17. Protected-evidence rule

Reconciliation must not squash away evidence-bearing history, reconstruct
accepted history, silently drop commits, rewrite protected evidence, force-push
without a separately approved necessity, normalize unresolved conflicts without
explicit review, or imply deployment/production readiness. (At this verified
point, main-only = 0, so no `main` history would be dropped by reconciliation;
the authoritative history is a strict superset.)

## 18. Branch-protection and required-check review requirement

Branch protection, required checks, default-branch configuration, CI, Pages,
environments, and release/deployment dependencies **have not yet been fully
reviewed** and must be inspected via the platform in the reconciliation gate.

## 19. Release-tag review requirement

The release tag `phase-j-stable` (`4795a879…`) exists and must be considered by
the reconciliation gate.

## 20. Rollback and post-reconciliation verification requirement

The gate must include rollback/recovery planning where applicable and
post-reconciliation verification (ancestry, evidence reachability, topology,
platform config).

## 21. Current unreadable or unverified platform configuration

Branch-protection and default-branch settings are **not readable via git** and
were not verified in this read-only preflight; no CI workflow triggering on
`main` surfaced in readable configuration. These remain gate inputs, not resolved
here.

## 22. Current honest limitations (recorded, not resolved)

`main` remains behind the authoritative branch; `main` contains no unique commits
at this verified point; the authoritative branch contains 640 commits absent from
`main`; fast-forward appears technically possible; branch protection,
default-branch, CI, required checks, Pages, environment, release, and deployment
implications have not yet been fully reviewed; release tag `phase-j-stable`
exists and must be considered; CR-4 remains unresolved; `DEMO_READY_WITH_LIMITATIONS`;
NOT PRODUCTION READY; no release or deployment authority. Technical fast-forward
possibility does **not** equal owner authorization.

## 23. CR-4 preservation

```
CR-4: LOW / RECORDED / UNRESOLVED / NOT REMEDIATED BY THIS INCREMENT
```

CR-4 (official vs main divergence + CLAUDE.md path drift) remains recorded and
unresolved; the path-drift sub-item remains a Phase 2 item. This record neither
resolves nor reclassifies CR-4.

## 24. What this record authorizes

- Recording OD-Q as an accepted owner decision (documentation, policy only).
- The smallest plan status synchronization and one appended roadmap record.

## 25. What this record prohibits

- Modifying `main` or the authoritative branch (outside this documentation
  candidate); merge, fast-forward, rebase, cherry-pick, reset, or force-push.
- Changing the default branch, branch protections, or required checks; creating,
  moving, or deleting tags; creating a release; deploying; archiving/deleting
  branches.
- Selecting the final reconciliation method; beginning the reconciliation gate.
- Modifying CI, workflows, Pages, environments, deployment configuration,
  runtime, UI, schemas, APIs, tests, templates, or evidence.
- Resolving or reclassifying CR-4.
- Modifying Phase 0 evidence, the OD-A…OD-O records, or
  `OWNER_PRODUCT_IDENTITY_CORRECTION.md`.
- Beginning OD-P; beginning Phase 1 closure.
- Activating Phase 2.
- Any implementation, release, or deployment authority.

## 26. Immediate effect

- The authoritative-branch rule and main-reconciliation policy are owner-ratified
  and govern branch authority going forward.
- No document text changes beyond this durable record, the smallest plan status
  synchronization, and one appended roadmap record. No branch/main/tag/deploy
  operation.

## 27. Deferred effect

- **Main reconciliation** (method selection and execution, with full ancestry/
  conflict/protection/CI/release/tag/rollback analysis, independent review, owner
  acceptance, and post-reconciliation verification) → a separate governed
  reconciliation gate under separate owner authorization.

## 28. Remaining open owner decision

`OD-P` remains **OPEN and unresolved**. **OD-A, OD-B, OD-C, OD-D, OD-E, OD-F,
OD-G, OD-H, OD-I, OD-J, OD-K, OD-L, OD-M, OD-N, OD-O** remain previously accepted
and merged and are **unchanged** by this record. Only OD-Q is decided here.

## 29. Implementation, release, and deployment authority

```
IMPLEMENTATION AUTHORITY: NONE
RELEASE AUTHORITY:        NONE
DEPLOYMENT AUTHORITY:     NONE
```

Product remains `DEMO_READY_WITH_LIMITATIONS`; NOT PRODUCTION READY.

## 30. Evidence classification

This is a **Phase 1 owner-decision evidence artifact** (documentation, policy
only). It is authoritative as a record of the owner's accepted OD-Q decision once
independently reviewed, owner-accepted, merged, and post-merge verified. Its
authority is that of a decision record; it grants no implementation, release, or
deployment authority. No reconciliation is selected or executed; `main` is
unchanged; technical fast-forward possibility is informational only; CR-4 remains
recorded and unresolved.
