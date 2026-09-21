# InventorAI — Successor Lead Handover — 2026-09-21 — Stage 17 → Stage 18

> **INPUT ONLY — NOT EXECUTION AUTHORITY.**
> The successor must run the single boot sequence in `CLAUDE.md`, verify live Git identity,
> read current authority, and reconcile this checkpoint against the repository before mutation.
> Repository evidence prevails over this handover.

## Verification limitation

The Owner requested the outgoing Lead to run and quote:

```bash
git status -sb
git log --oneline -15
git branch -a --contains HEAD
git diff --stat
```

and the exact HEAD of every branch touched.

This ChatGPT execution environment has **no local checkout of Amirjaferali/inventorai** and
shell network access to GitHub is unavailable, so the exact shell commands above could not be
run without fabricating output. This handover therefore records the equivalent live GitHub
repository evidence where available and explicitly marks shell-only state as **UNVERIFIED**.
The successor MUST run those exact commands locally before mutation.

Live repository evidence verified before writing this checkpoint:

- authoritative branch: `feature/atomic-json-session-persistence`
- authoritative HEAD: `6c982e41d1d7fd45d9646b5a972c5a8f945571d7`
- authoritative tree: `7b2ef5bc574de0fe69e9262beee923242c8985d4`
- checkpoint branch: `stage17/depth-disposition-sync`
- checkpoint branch HEAD before this handover commit:
  `6c982e41d1d7fd45d9646b5a972c5a8f945571d7`

GitHub history equivalent to `git log --oneline -15`:

```text
6c982e41d1d7 Merge pull request #675 from Amirjaferali/stage17/d3-supporting-evidence-link
eebb285c732b Stage 17 D3: let one commercial item cite the item that supports it
43d13b20acad Merge pull request #674 from Amirjaferali/stage17/d2-commercial-quantities
b9890283c32b Stage 17 D2: record commercial amounts with a basis, or not at all
8c9e5a6f0ebf Merge pull request #673 from Amirjaferali/stage17/d1-commercial-lifecycle
00d6af44383d Stage 17 D1: make commercial evidence correctable and withdrawable
b6a655549f49 Merge pull request #672 from Amirjaferali/stage17/commercial-evidence-gap
f16c977aa10d Stage 17: correct the uncovered_topics() supersession wording
2f7d98553e16 Stage 17: show which commercial topics have nothing recorded yet
9ce9ac8c1c9d Merge pull request #671 from Amirjaferali/claude/adoring-brown-cvqnj9
bfd9c79e0e21 Stage 10: record the T2-C′ differential without changing the verdict
c1e137bd5722 Merge pull request #670 from Amirjaferali/claude/adoring-brown-cvqnj9
1383b4753825 Stage 9: record the T1-A′ disposition without closing the obligation
9f524d6b1be0 Merge pull request #669 from Amirjaferali/claude/adoring-brown-cvqnj9
f4811bfaa2a8 Stage 8: record the EN-AR divergence closure under Owner acceptance
```

Verified branch heads touched/relevant in this session:

- `feature/atomic-json-session-persistence` →
  `6c982e41d1d7fd45d9646b5a972c5a8f945571d7`
- `stage17/d2-commercial-quantities` →
  `b9890283c32b9d7381a87c717a03ccd546ec2c03`
- `stage17/d3-supporting-evidence-link` →
  `eebb285c732b0ca64282769eda1b8635fbed082b`
- `stage17/depth-disposition-sync` →
  `6c982e41d1d7fd45d9646b5a972c5a8f945571d7` before this handover commit
- `claude/adoring-brown-cvqnj9` →
  `bfd9c79e0e21ccc4bd3650fc484e823a01d03bd3`

For `git branch -a --contains HEAD`, live branch equality verified that the authoritative
branch and the checkpoint branch both pointed to the same pre-handover HEAD. The exact local
branch-containment listing is **UNVERIFIED**.

For `git diff --stat`, the checkpoint branch was identical to the authoritative tip before
the handover commit. The successor must verify the local diff state directly.

---

## A. Session identity

**Date:** 2026-09-21

**Base / authoritative branch:** `feature/atomic-json-session-persistence`

**Authoritative HEAD at session start:**  
`8c9e5a6f0ebf272676d3f1b1b3faddc1ee8f5a70`

That is the verified base from which D2 began in this session.

**Authoritative HEAD at session end before handover commit:**  
`6c982e41d1d7fd45d9646b5a972c5a8f945571d7`

**Authoritative tree:**  
`7b2ef5bc574de0fe69e9262beee923242c8985d4`

**Working/checkpoint branch at handover:**  
`stage17/depth-disposition-sync`

The outgoing Lead did not have a local checkout, so a shell-local HEAD is not available.
The branch HEAD above is verified from GitHub.

---

## B. Authoritative branch and live tip; working branch and HEAD

**Authoritative branch:** `feature/atomic-json-session-persistence`

**Authoritative live tip before the handover artifact:**  
`6c982e41d1d7fd45d9646b5a972c5a8f945571d7`

**Authoritative tree:**  
`7b2ef5bc574de0fe69e9262beee923242c8985d4`

**Working/checkpoint branch:** `stage17/depth-disposition-sync`

**Working/checkpoint branch HEAD before this handover commit:**  
`6c982e41d1d7fd45d9646b5a972c5a8f945571d7`

This handover commit advances only the checkpoint branch. The authoritative branch must remain
unchanged unless another actor advances it.

---

## C. Uncommitted and untracked changes

Local checkout state is **UNVERIFIED** because the outgoing Lead environment has no repository
checkout.

The successor MUST run:

```bash
git fetch origin feature/atomic-json-session-persistence stage17/depth-disposition-sync
git status -sb
git diff --stat
git rev-parse HEAD
git rev-parse HEAD^{tree}
git rev-parse refs/remotes/origin/feature/atomic-json-session-persistence
git rev-parse refs/remotes/origin/feature/atomic-json-session-persistence^{tree}
git branch -a --contains HEAD
git log --oneline -15
```

Do not reset, discard or commit unknown local changes until they are classified.

Before this handover file was created, the remote checkpoint branch had no content delta from
the authoritative branch.

---

## D. Commits created this session and remote branches pushed

### D2

Candidate:
`b9890283c32b9d7381a87c717a03ccd546ec2c03`

Message:
`Stage 17 D2: record commercial amounts with a basis, or not at all`

Merged as:
`43d13b20acad995a069112d924bd4ce62df66046`

Branch:
`stage17/d2-commercial-quantities`

### D3

Candidate:
`eebb285c732b0ca64282769eda1b8635fbed082b`

Message:
`Stage 17 D3: let one commercial item cite the item that supports it`

Merged as:
`6c982e41d1d7fd45d9646b5a972c5a8f945571d7`

Branch:
`stage17/d3-supporting-evidence-link`

### Lead-created checkpoint branch

`stage17/depth-disposition-sync`

It was created directly by the outgoing Lead at `6c982e41…`.
**No Stage-17 status synchronization content was committed to it.**

The Owner then corrected the operating model:
**Lead writes the instruction → Claude executes → Lead reviews.**

This branch now carries only this successor checkpoint artifact.

---

## E. PR / merge state

### PR #674 — D2

URL:
https://github.com/Amirjaferali/inventorai/pull/674

State:
**CLOSED / MERGED**

Base:
`8c9e5a6f0ebf272676d3f1b1b3faddc1ee8f5a70`

Head:
`b9890283c32b9d7381a87c717a03ccd546ec2c03`

Merge commit:
`43d13b20acad995a069112d924bd4ce62df66046`

Checks:
- `Verify candidate` — SUCCESS, completed 2026-09-21T14:43:18Z
- `CI required` — SUCCESS, completed 2026-09-21T14:43:24Z

Reviews: none.
Open review threads: none.

### PR #675 — D3

URL:
https://github.com/Amirjaferali/inventorai/pull/675

State:
**CLOSED / MERGED**

Base:
`43d13b20acad995a069112d924bd4ce62df66046`

Head:
`eebb285c732b0ca64282769eda1b8635fbed082b`

Merge commit:
`6c982e41d1d7fd45d9646b5a972c5a8f945571d7`

Checks:
- `Verify candidate` — SUCCESS, completed 2026-09-21T15:34:57Z
- `CI required` — SUCCESS, completed 2026-09-21T15:35:02Z

Reviews: none.
Open review threads: none.

### Stage-17 disposition synchronization

No PR exists.
No candidate commit exists.
Do not infer completion from the existence of `stage17/depth-disposition-sync`.

---

## F. Tests run this session

Exact shell command strings used by Claude were not included in the returned execution reports
and are therefore **UNVERIFIED**. Do not invent them.

### D2 evidence

- focused suite: **362 passed**
- full regression: **6876 passed, 5 skipped, 1 xfailed, 0 failed**
- post-merge commercial suites: **119 passed**
- GitHub `Verify candidate`: SUCCESS
- GitHub `CI required`: SUCCESS

One scratch verification script initially rebuilt every column as `TEXT`, causing
`withdrawn` to be interpreted as a truthy string. Claude identified that as a defect in the
throwaway verification DDL, not product code, reran with original column types, and the check
passed. Exact traceback text is **UNVERIFIED**.

### D3 evidence

- focused set: **448 passed**
- relevant regression: **6904 passed, 3 skipped, 1 xfailed, 0 failed**
- seven Playwright browser files excluded because Playwright was absent
- merged-head commercial owner/capture verification: **147 passed**
- GitHub `Verify candidate`: SUCCESS
- GitHub `CI required`: SUCCESS

During D3 test authoring, an over-broad forbidden-word sweep falsely triggered on truthful
negative copy such as “InventorAI has verified none of it” and “nothing is counted, rated or
ranked.” Claude corrected the test scope, not the truthful copy.

---

## G. Unresolved findings, known bugs and risks

### G1 — Stage 17 product-depth is sufficient; commercial validation is not

Commercial Data Depth Recheck result:

- pre-D1/D2/D3 depth: **MODERATE**
- post-D1/D2/D3 depth: **MODERATE-DEEP**
- D1 material impact: YES
- D2 material impact: YES
- D3 material impact: YES
- 15 / 15 governed Commercial topics are sufficiently deep for the current Stage-17 product axis
- additional Stage-17 product-depth implementation: **NOT JUSTIFIED**

But:

- `COMMERCIAL READINESS: PARTIAL`
- `VALIDATED COMMERCIAL CONCLUSION: NO`
- `READINESS CEILING: INSUFFICIENT_EVIDENCE`

Remaining material layers:
- L5 provenance depth
- L6 evidence quality
- L8 validation state

Owner:
**deferred T2-E / OD-PDVG-08b evidence-writer reachability**, not Stage 17.

### G2 — D3 has no database FK by design today

D3 added:

`supporting_evidence_id`

to the existing `readiness_evidence` table.

Current protection lives in the canonical owner/store path:
- target exists
- same project
- same dimension
- not self
- not the superseded item
- no cycle
- entire resulting history validated before insert

#### D3 FK hardening note — preserve

Re-evaluate a true composite FK:

`(project_id, supporting_evidence_id) → readiness_evidence(project_id, evidence_id)`

**when either:**

1. a future migration can safely rebuild `readiness_evidence` for **all existing databases**
   so fresh and migrated databases receive identical constraints; or
2. the datastore moves to a platform such as PostgreSQL where the constraint can be introduced
   consistently.

Until then:
- no fresh-only FK;
- no unequal fresh/migrated enforcement;
- no SQLite trigger merely to imitate part of the constraint;
- retain owner/store validation;
- a future automated integrity audit may be useful as defense-in-depth.

### G3 — Governance/navigation drift exists

The latest Owner decision is not yet durably synchronized.

At the authoritative tip:
- `ACTIVE_INCREMENT_CONTRACT.md` still routes from an older Stage-10 state and says
  ACTIVE CONTRACT: NONE;
- `INVENTORAI_MASTER_EXECUTION_ROADMAP.md` v1.32 does not yet record the Stage-17
  post-D1/D2/D3 disposition;
- `INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md` still presents Stage 11 as the
  current frontier;
- `CURRENT_PROJECT_STATE.md` is older than D2/D3/Stage-17 recheck, but the Owner instructed
  the sync not to touch it unless live inspection proves necessary.

Treat this as bounded documentation drift, not a new governance workstream.

### G4 — WATCH-01 planned, not implemented

Future:
**Automated Authoritative-State / Documentation-Drift Control**

Desired direction:
one machine-readable authoritative current-state source → automated drift detection →
derived status synchronization → optional sync PR.

Must NOT automatically:
- decide stage pass/closure
- discharge residuals
- authorize humans/RUN-004/MCP/deployment/release
- promote readiness
- replace Owner decisions
- auto-merge material changes

### G5 — material carried residuals remain

Preserve existing owners/triggers for:
- T1-A′ OPEN / FRB; closure evidence not met; RUN-004 not authorized
- T2-C′ PARTIAL
- real user value unevidenced
- product differentiation unevidenced
- Stage 11 T1-C′ / A2 human evidence deferred
- CEHR deferred, not cancelled; Route-B preserved
- G-4-A / G-4-B existing return gates
- HICR / PRE-FCORA existing triggers
- T2-A random-skip debt
- T2-D observations
- PR #640 findings
- N-3 through N-6
- Stages 14–16 dependency-based deferrals
- no positive readiness promotion path
- deployment/release/paid activation boundaries
- Stage 44 lineage gate
- Stage 45 deployment gate

Do not reopen or close them without current evidence/authority.

---

## H. Incomplete work

### H1 — Stage-17 product-depth disposition synchronization

**State:** DECIDED BY OWNER, NOT IMPLEMENTED.

Owner decision to record:

- Stage-17 product-depth work:
  **COMPLETED FOR CURRENT AUTHORIZED PRODUCT SCOPE**
- Commercial Readiness:
  **PARTIAL**
- Validated commercial conclusion:
  **NO**
- Depth:
  **MODERATE → MODERATE-DEEP**
- D1/D2/D3:
  completed/merged
- 15 / 15 topics:
  sufficiently deep for current Stage-17 product axis
- remaining L5/L6/L8 gap:
  T2-E / OD-PDVG-08b
- next executable roadmap stage:
  Stage 18 — D13 / CAP-01
- Stage 18 started:
  NO
- roadmap version:
  remain v1.32

The outgoing Lead briefly started direct GitHub execution and created
`stage17/depth-disposition-sync`, but no synchronization content was committed before the
Owner corrected the execution model.

**Next command/action for successor:**
after boot and live verification, have Claude execute the already-bounded minimal
documentation-only sync from the then-current authoritative tip.

**Must NOT:**
- treat the checkpoint branch as a completed sync candidate
- start Stage 18 implementation during the sync
- start T2-E writer work
- collect human/market evidence
- change runtime/schema
- create v1.33
- add stages/tracking IDs
- rewrite historical sections
- expand into generalized governance cleanup

### H2 — Stage 18 — D13 / CAP-01 Structured Technical Guidance

**State:** NEXT STAGE DECIDED, NOT STARTED, NOT IMPLEMENTED.

First Stage-18 adjudication must explicitly reconsider the preserved
**Multilingual Semantic Normalization Layer**.

This is **not** “use an LLM everywhere.”

Intended bounded architecture:

```text
Arabic / English / future supported user input
        ↓
Multilingual Semantic Normalization Layer
        ↓
canonical InventorAI concepts
        ↓
existing deterministic progression / decision engine
```

The model may assist interpretation of multilingual free-form input into existing canonical
concepts. The deterministic engine remains final progression/decision owner.

Required properties to adjudicate:
- shadow-first
- pinned model/version
- confidence boundary
- fail closed on ambiguity
- deterministic fallback
- provider-neutral adapter
- no automatic concept creation
- no model ownership of final decisions
- no automatic evidence validation
- no automatic readiness promotion
- no unsupported engineering conclusion
- auditability of source input → normalized candidate → selected canonical concept, subject
  to privacy boundaries

Read-only Stage-18 adjudication should determine:
1. whether the layer belongs inside D13/CAP-01;
2. exact input/output contract;
3. shadow-mode evidence;
4. confidence/fallback rules;
5. provider abstraction/model pinning;
6. what data may leave the deterministic boundary;
7. whether security/privacy/evidence-trust reserved decisions are triggered.

Only after adjudication should an implementation mandate be proposed.

---

## I. Decisions taken this session and justification

### I1 — D2 merged

Four monetary topics received structured quantity support:
- `price`
- `willingness_to_pay`
- `cost_revenue_assumption`
- `funding_need`

Rules:
- USD default/current supported currency
- `EXACT`
- `ESTIMATED_RANGE`
- `NONE / NOT_ESTABLISHED`
- **NO DEFENSIBLE BASIS → NO ACCEPTED NUMBER**
- basis-less numeric input refused
- NONE explicit
- zero ≠ NONE
- no invented midpoint
- no invented range
- validation remains UNVALIDATED

### I2 — D3 merged

Accepted design:
one direct nullable `supporting_evidence_id` on the existing Commercial Evidence row.

Rejected:
repurposing assertion-anchored `evidence_reference`, because Commercial Evidence already owns
source/date/scope/limitation and reuse would duplicate provenance semantics.

Truth rule:
`REFERENCE EXISTS ≠ SOURCE TRUSTWORTHY ≠ VALIDATED ≠ PROVEN ≠ READY`.

### I3 — Commercial Data Depth Recheck accepted

Disposition:
**D — remaining material gaps belong to deferred T2-E / other existing owners, not Stage 17.**

Therefore no additional Stage-17 product-depth fields are justified.

### I4 — latest Owner decision not yet recorded in repository

Owner explicitly accepted:
- Stage-17 product-depth complete for current scope
- Commercial Readiness remains partial
- next executable stage = Stage 18
- Stage 18 not started
- minimal status sync only
- roadmap remains v1.32

### I5 — execution model corrected

Owner reaffirmed:
**Lead writes instructions → Claude executes → Lead reviews/adjudicates.**

Do not directly mutate the repository as Lead unless the Owner explicitly asks for direct execution.

### I6 — governance principle

Standing Owner requirement:

**USE THE MINIMUM NECESSARY GOVERNANCE PROPORTIONATE TO RISK.**

Do not create new documents, review loops or gates unless they address a specific material risk
not already controlled. Product progress over ceremony. Do not reopen completed work absent new
material defect evidence. Aggregate defects into one repair and use differential re-review only
when needed.

### I7 — data-depth principle

Standing:

**Presence ≠ Depth ≠ Evidence ≠ Provenance ≠ Validation ≠ Decision Value.**

For material capability/stage assessment, consider:
1. presence
2. statement capture
3. structured context
4. evidence linkage
5. provenance depth
6. evidence quality
7. contradiction/supersession
8. validation state
9. decision usefulness
10. longitudinal depth

Prefer fewer high-value structured fields over field bloat.

---

## J. Current authority

Repository `CLAUDE.md` currently states:

**ACTIVE CONTRACT: NONE.**

It directs agents to `ACTIVE_INCREMENT_CONTRACT.md` for the live durable mandate.

However, after those files became stale, the Owner directly issued a new chat decision:
**Stage-17 product-depth disposition + minimal status synchronization only.**

That Owner decision was active in the outgoing session but was not yet durably synchronized.

For the successor:
- this handover is not authority;
- run the CLAUDE.md boot sequence;
- verify whether another actor has since recorded the decision;
- if the Owner explicitly tells the successor to continue under this checkpoint, that direct
  instruction applies;
- otherwise do not infer a renewed mutation mandate from the handover alone.

Lean §10 scoped holds:
hold only affected work if repository identity is unverified, whole-milestone authority is
invalid, working state is unsafe, or a cross-cutting defect materially invalidates the mandate.
A moved tip alone is not a global STOP.

---

## K. Safest single next action

**Run the CLAUDE.md boot sequence and exact local Git verification, then—if the Owner explicitly continues the pending Stage-17 disposition mandate—have Claude create one minimal documentation-only status-sync candidate from the live authoritative tip; do not start Stage 18 implementation.**

---

## L. Files the successor must read first, in order

1. **`CLAUDE.md`**  
   Owns the single boot sequence and repository execution rules.

2. **`docs/governance/CURRENT_PROJECT_STATE.md` current entry only**  
   Current-state routing. It is stale relative to D2/D3/Stage-17 recheck; do not let stale
   routing override newer Owner evidence.

3. **`docs/governance/ACTIVE_INCREMENT_CONTRACT.md` current entry only**  
   Owns durable mandate. It does not yet contain the latest Stage-17 disposition.

4. **`docs/governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md` §§2–5B, 9, 10, 11**  
   Authority, proportionate risk/testing/review, successor propagation, holds, durable updates.

5. **`docs/governance/INVENTORAI_MASTER_EXECUTION_ROADMAP.md` v1.32 current routing overrides**  
   Derived navigation only; stale for present routing after Stage 17.

6. **`docs/governance/INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md`**  
   The Master Checklist / anti-drift operating aid. Derived, not authority. It currently still
   routes Stage 11 and therefore needs bounded sync.

7. **PR #674 / merge `43d13b20…`**  
   D2 exact merged evidence.

8. **PR #675 / merge `6c982e41…`**  
   D3 exact merged evidence.

9. **This handover**  
   New/different facts and pending work only.

Do not recursively reload project history unless a material contradiction or Lean §6 trigger exists.

---

# Successor operating rules requested explicitly by the Owner

## 1. Communication style

- Owner-facing discussion: Arabic unless asked otherwise.
- Claude/Creator instructions: English.
- Put every material Claude instruction in one copyable code block.
- Do not make the Owner reconcile several partial instructions.

## 2. Required end-of-message footer

At the end of every substantive project message, include:

### Master Checklist — Standing Watch

List only the current material watch items.

Then include:

### آخر 5 مراحل حالية / القادمة

Show exactly five relevant stages with status markers and refresh them after each stage materially changes.

At this checkpoint:

- [⏸ DEFERRED] **Stage 14 — MRL-Compatible View**
- [⏸ DEFERRED] **Stage 15 — IRL-Compatible View**
- [⏸ DEFERRED] **Stage 16 — SRL-Compatible Composition**
- [▶ CURRENT] **Stage 17 — Market Reality / Commercial Readiness** — product depth complete;
  minimal status sync still pending; Commercial Readiness remains PARTIAL.
- [📌 NEXT] **Stage 18 — D13 / CAP-01 Structured Technical Guidance** — not started;
  first adjudication must revisit Multilingual Semantic Normalization Layer.

After Stage-17 synchronization is accepted, move Stage 17 out of CURRENT. Move Stage 18 to
CURRENT only when a separate explicit Stage-18 mandate exists.

## 3. How to write material instructions to Claude

For load-bearing execution instructions, include enough of:

A. MASTER ROADMAP STAGE  
B. GROUP  
C. SUBTASK  
D. ENTRY CONDITION — exact repo/branch/base HEAD/tree/prerequisites/authority  
E. EXIT CONDITION  
F. NON-NEGOTIABLE INVARIANTS  
G. FAILURE-CLASS / ADVERSARIAL CHECKS  
H. SCOPE / FORBIDDEN ACTIONS  
I. REQUIRED EVIDENCE RETURN  

Also include concise STOP conditions.

Rules:
- exact identifiers where load-bearing
- one bounded pass
- accumulate defects instead of serial one-finding loops
- no full historical review without Lean §6 trigger
- no automatic independent review for low-risk work
- risk-proportionate testing/review under Lean §§3–5B
- no reopening completed work without new material evidence

## 4. Stage-18 semantic-normalization note — full intent

The proposed layer is a **bounded multilingual semantic normalization layer**, not an LLM that
replaces InventorAI.

The intended path is:

```text
User free-form input (Arabic / English / future supported language)
        ↓
semantic normalization
        ↓
existing canonical InventorAI concepts
        ↓
existing deterministic progression / decision engine
```

What the model is allowed to do:
- interpret phrasing
- propose mapping to existing canonical concepts
- help reduce Arabic/English phrasing variance

What the model is NOT allowed to do:
- create new concepts automatically
- become the decision engine
- promote readiness
- validate evidence
- invent engineering conclusions
- silently override deterministic logic

Required first-phase characteristics:
- shadow-first
- pinned model/version
- confidence threshold
- fail closed
- deterministic fallback
- provider-neutral abstraction
- auditability
- privacy boundary review before sending sensitive data externally

**When to act:** first Stage-18 D13/CAP-01 adjudication, after Stage-17 status sync.
**Why:** improve multilingual semantic consistency while preserving deterministic ownership,
explainability and safety.

## 5. Standing notes and activation timing

### WATCH-01 — Automated Authoritative-State / Documentation-Drift Control
**When:** later bounded hardening when it no longer interrupts higher-value product work.  
**What:** machine-readable state source + drift detection + derived sync, optional sync PR.  
**Must not:** decide closure/pass, authorize humans/deploy/release, promote readiness,
replace Owner decisions or auto-merge material changes.

### WATCH-04 — Data Depth Principle
**When:** every future material capability/stage assessment.  
**What:** use the ten depth layers above.  
**Why:** deeper structured data supports differentiation, commercial reasoning and accuracy.

### D3 FK Hardening
**When:** safe all-database table rebuild becomes possible, or datastore moves to e.g. PostgreSQL.  
**What:** reconsider composite FK on `(project_id, supporting_evidence_id)`.  
**Do not:** add fresh-only FK or unequal enforcement.

### Stage 18 Multilingual Semantic Normalization
**When:** first Stage-18 adjudication.  
**What:** bounded semantic normalization ahead of deterministic engine, shadow-first.  
**Do not:** make the LLM the final decision owner.

---

# Status classification

## DONE AND VERIFIED

- PR #674 / D2 merged.
- PR #675 / D3 merged.
- D1/D2/D3 depth plan completed.
- Commercial Data Depth Recheck completed read-only.
- Post-D1/D2/D3 depth = MODERATE-DEEP.
- 15/15 Commercial topics sufficiently deep for current Stage-17 product axis.
- D3 FK hardening note preserved.
- Stage-18 multilingual semantic-normalization note preserved.

## DONE BUT UNVERIFIED

- None known.

## STARTED NOT FINISHED

- `stage17/depth-disposition-sync` exists.
- No Stage-17 status-sync content was committed.
- This handover artifact is the only intended new content on that branch.

## DECIDED BUT NOT IMPLEMENTED

- Minimal Stage-17 disposition synchronization.
- Stage 18 is next executable roadmap stage, but not started.
- First Stage-18 adjudication must revisit multilingual semantic normalization.
- WATCH-01 remains planned, not implemented.

## OPEN QUESTION FOR OWNER

- No new decision is required merely to finish the already-issued Stage-17 status sync if the
  successor session is explicitly told to continue that mandate.
- Stage 18 implementation itself requires a separate mandate after adjudication.
- T2-E evidence-writer activation, human/market evidence collection, provider spending,
  release/deployment and reserved-boundary changes remain separately authorized.

HANDOVER COMPLETE — verified against HEAD 6c982e41d1d7fd45d9646b5a972c5a8f945571d7
