# FCORA — Full Capability & Obligation Reconciliation Audit
# Bounded execution contract — CANDIDATE

**Instruction of record:** `FCORA-CONTRACT-FREEZE-01` v1.0 (Owner), as corrected by
`FCORA-CONTRACT-CORRECTION-01` v1.0 (Owner) — one bounded round closing the
independent review's three MATERIAL findings: materiality bound to the existing
C0–C4 model (§6A), the roadmap added to the minimum corpus (§5 item 11), and the
PRE-FCORA eligibility provenance stated as an Owner-attested input (status block).
**Base:** `fafc94e151a4a6f06f8445dde1373bbac0212200` — the verified PR #654 merge
result on `feature/atomic-json-session-persistence`.

**Status of this document.**
`FCORA CONTRACT: CANDIDATE — NOT AUTHORITATIVE UNTIL OWNER-ACCEPTED AND MERGED` ·
`FCORA EXECUTION AUTHORIZED: NO` · `FCORA STARTED: NO` ·
`FCORA POSITIONALLY ELIGIBLE: YES`. This file defines and freezes the audit; it does
not perform it, schedule it, or authorize it. Eligibility is not authorization.

**Provenance of the eligibility basis (stated exactly).** The differential PRE-FCORA
recheck result is an **OWNER-ATTESTED EXECUTION INPUT** for this contract lifecycle,
not a repository citation. The exact accepted result is:

```
UNEXPLAINED MATERIAL DIFFERENCES = 0
SILENT DISAPPEARANCE CANDIDATES  = 0
UNACCOUNTED MATERIAL OBLIGATIONS = 0
verdict B — READY WITH NON-BLOCKING DEFERRED ITEMS
```

**No committed repository artifact is claimed to contain that recheck result**, and
this contract fabricates no repository citation for it: at this base the recheck exists
as the Owner's attestation in the authorizing instrument, and that attestation is what
establishes the input for this lifecycle. A future reader must not infer a committed
PRE-FCORA differential-recheck record from this statement, and must not manufacture one
to "prove" it. Positional eligibility established this way still does **NOT** authorize
FCORA execution: execution requires an authoritative merged contract AND a separate
Owner FCORA EXECUTION authorization (§14, §17). If the Owner later commits a recheck
artifact, this paragraph is superseded by that artifact's own citation — not by
assertion here.

---

## 1. Authority and subordination

This contract is **subordinate** and owns only the FCORA procedure:

| Concern | Existing owner | This contract's relationship |
|---|---|---|
| FCORA direction, mandate, position, `UNACCOUNTED / ORPHAN = 0` pass rule | `OWNER_DECISION_REGISTER.md` §D-2 | implements it; never amends, relaxes or re-scopes it |
| PRE-FCORA prerequisite gate and its pass conditions | `OWNER_DECISION_REGISTER.md` §D-2 amendment | unchanged; PRE-FCORA remains a mandatory immediate prerequisite |
| The FCORA obligation, its `FRB` level, return trigger and latest-safe gate | `DEFERRED_OBLIGATIONS_REGISTER.md` §3 FCORA row | this document is the "FCORA gate's own future contract" that row names as Source owner and return trigger; the row is **not** discharged, closed or moved by this document's existence |
| Canonical obligation ledger | `DEFERRED_OBLIGATIONS_REGISTER.md` | FCORA reads and reports; it never becomes a second ledger |
| Owner decisions and directions | `OWNER_DECISION_REGISTER.md` | FCORA reads; it never records a new Owner decision |
| Current mandate / active contract | `ACTIVE_INCREMENT_CONTRACT.md` | FCORA execution requires its own Owner authorization; this contract installs no mandate |
| Current state and successor routing | `CURRENT_PROJECT_STATE.md`, `MASTER-HANDOVER.md` | FCORA reads them as current-authority surfaces |
| Operating authority, risk, review depth, evidence reuse | Lean §§2–5B, §6, §10, §11 | FCORA operates inside them |
| Delivery / exact-head merge mechanics | AHAEP | unchanged |
| Capabilities CAP-01…CAP-18 | `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` (R7 preservation) | FCORA audits without amending; an R7 amendment needs explicit Owner approval |
| Continuous per-candidate traceability | `CROSS_LAYER_EXECUTION_ASSURANCE_STANDARD.md` §4 | FCORA verifies the accumulated chains; it does not replace the continuous rule |
| Universal fixed regression floor | `INVENTORAI_UNIVERSAL_CORE_GUARDRAIL_SMOKE_STANDARD.md` (P10-UG1) | FCORA may read its guard results as evidence; it does not extend the floor |
| Serious Release / Production Readiness authorization | the separate Owner/release gates (PSRR registration, PDVG-01, Phase-10 readiness surfaces) | FCORA precedes them and authorizes none of them |

**FCORA is an audit gate, never an owner.** It takes ownership of nothing it audits.
Where this document and a governing owner appear to conflict, the governing owner
prevails and the conflict is returned to the Owner as a finding.

## 2. Purpose

FCORA is the final cross-layer audit required **before** Serious Release /
Production Readiness consideration. It reconciles

```
DOCUMENTED OBLIGATIONS  ↔  IMPLEMENTED CAPABILITIES
```

in **both** directions, so that no historically recorded capability, feature,
obligation, deferred item, future item or implementation silently disappears, and
no implemented capability exists without a documented owner and disposition.

**The eight detection classes.** FCORA must detect:

| Class | Defect |
|---|---|
| **A** | documented capability / obligation with no implementation **and** no disposition |
| **B** | implementation / capability with no documented owner, obligation, authority or disposition |
| **C** | duplicate ownership — two canonical owners for one item |
| **D** | silent disappearance — an item present in earlier authority, absent now, with no supersession, closure or carry-forward |
| **E** | superseded or retired items still presented as current |
| **F** | implemented capability whose release / production disposition is missing |
| **G** | current governance statement that materially contradicts runtime reality |
| **H** | runtime capability that materially contradicts governing product truth |

Classes **G** and **H** are the defect family the PRE-FCORA review actually found and
the PR #653 / PR #654 repairs closed; FCORA re-tests them against the whole corpus
rather than only the four current-facing surfaces.

## 3. FCORA is not product design

**FCORA MUST NOT BECOME THE PLACE WHERE PRODUCT CONCEPTS ARE FIRST DESIGNED.**

FCORA may classify existing evidence into a disposition **only where repository
authority already supports that classification**:

`IMPLEMENTED & VERIFIED` · `PARTIALLY IMPLEMENTED` (missing layers named, per
Cross-Layer §4.3) · `DEFERRED & OWNED` · `SUPERSEDED` · `REJECTED` · `BLOCKED` ·
`UNRESOLVED WITH AN EXISTING RETURN GATE`. Anything with no defensible disposition is
`UNACCOUNTED / ORPHAN`.

FCORA must **NOT**: invent a new engine; invent a new canonical owner; invent a new
readiness dimension; invent a new evidence store; create a new risk owner; redesign
product architecture; implement missing functionality; or silently force-fit a
residual into an unrelated existing owner to keep governance tidy.

**If a genuine product-design decision is required, FCORA returns it to the Owner as a
separate decision.** It is named, bounded and left undecided — not solved inside the
audit. A design question is not a disposition, and "returned to Owner" is itself a
defensible outcome for the item, recorded as `OWNER DECISION REQUIRED` with the exact
question.

## 4. Precedents reused, and what FCORA generalizes

FCORA has ancestry and must not claim otherwise. Each precedent below was inspected;
what FCORA adds is stated, and no precedent's owner is duplicated.

| Precedent | What it established | What FCORA generalizes beyond it |
|---|---|---|
| **G-MPR-01** — Master Phase & Roadmap Completeness Review (read-only, completed, historical) | a one-time, read-only completeness audit that halts forward execution until its findings are Owner-resolved | FCORA keeps the read-only-first posture and the execution halt, but audits **capabilities and obligations against implementation**, not phase/roadmap structure, and runs at the release boundary rather than mid-phase |
| **G-MPR-01-D** — Findings Disposition & Roadmap Registration (governance-only) | findings are converted into registered dispositions in existing owners by a **separate** bounded gate, not by the audit itself | FCORA adopts exactly this separation: audit returns findings; repair is a separate Owner-authorized candidate (§14) |
| **CAP register R7 — Preservation** | all eighteen CAP entries preserved exactly; "no entry may be silently added, dropped, merged, or reworded" without explicit Owner approval | FCORA raises the same no-silent-change invariant from one register to the **whole corpus**, and verifies it rather than only asserting it |
| **P10-UG1** — Universal Core Guardrail & Smoke Framework (+ its standard) | a fixed, composed core-invariant floor identical for every candidate; docs↔code invariant checks as executable guards | FCORA reads those guards as **evidence of implementation truth**; it audits coverage of the corpus, where UG1 fixes a floor for each candidate. FCORA adds no guard and changes no floor |
| **Deferred Obligations Register release-closure rules** | per-row owner, origin, disposition, return trigger, latest-safe gate, blocking level (`FRB`), required closure evidence | FCORA verifies every row's six fields are intact and defensible at the release boundary, and that no row's latest-safe gate has silently passed. The register remains canonical; FCORA writes nothing into it |
| **Cross-Layer Execution Assurance Standard §4** — Continuous Traceability Rule, C0–C4 proportionality, §4.3 partial implementation, §4.4 supersession/rename trace, §4.5 evidence strength | the per-candidate trace `Governance Owner → Decision/Requirement → Implementation Surface → User-Reachable Surface → Tests/Evidence → Current Disposition`, realized in existing owners with no competing registry | FCORA is the **terminal verification** of those accumulated chains across the entire history, in both directions, where the Standard is continuous and per-candidate. Per the Standard's own §9 owner map, continuous traceability makes FCORA "a verification, not a first attempt". FCORA adopts its `PARTIALLY IMPLEMENTED` decomposition and its rename/supersession trace form verbatim rather than inventing new ones |

**Non-duplication statement.** FCORA creates no second roadmap, obligation register,
authority register, capability register, checklist, traceability registry or guard
framework. Its only artifacts are its findings return and the dispositions it reports
into existing owners for the Owner to act on.

## 5. Required corpus

FCORA's minimum authoritative corpus:

1. the **current authoritative Git tree** at the exact FCORA HEAD (identity recorded);
2. `CURRENT_PROJECT_STATE.md` — current entry and preserved-state boundaries;
3. `ACTIVE_INCREMENT_CONTRACT.md` — current authority; historical declarations as
   evidence only;
4. `OWNER_DECISION_REGISTER.md` — the relevant substantive decisions;
5. `DEFERRED_OBLIGATIONS_REGISTER.md` — the canonical obligation ledger, all rows;
6. `MASTER-HANDOVER.md` — **only** for current successor-routing consistency;
7. authoritative capability / architecture registers —
   `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` (CAP-01…CAP-18),
   `DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §15 (WS12–16, deferred WS17),
   `STAGE3_CAPABILITY_MODEL.md`, and the domain-activation and architecture surfaces
   they cite;
8. applicable **formal closure records** (RVR-6a/6b/7/8, CF/D13/DGMPR and phase
   closures) at their recorded scope;
9. applicable **accepted implementation contracts**, including the current post-PR-652
   declaration and the merged evidence for PRs #647–#654;
10. `CROSS_LAYER_EXECUTION_ASSURANCE_STANDARD.md` and
    `INVENTORAI_UNIVERSAL_CORE_GUARDRAIL_SMOKE_STANDARD.md` — traceability and floor
    mechanics;
11. `ACTIVE_EXECUTION_ROADMAP.md` — the **required roadmap / lanes / historical-trace
    surface**. FCORA needs it for lane, history, supersession and
    silent-disappearance tracing: it is where an item's lane, its movement between
    phases, its rename or supersession, and its disappearance from forward execution
    are recorded. Its entries are **evidence at their recorded time**, and its stale
    historical "current" wording is **NOT automatically current authority** — current
    authority remains owned by the current authority/state surfaces (items 2–3, with
    item 6 for successor routing). **FCORA must distinguish historical routing from
    current routing** and must report, not adopt, any historical routing statement
    that reads as current. The roadmap is **not** promoted into canonical current
    authority, a second obligation ledger, a second owner, or execution authority;
12. the **current Master Checklist view — NAVIGATION ONLY** (§6);
13. **actual implementation** — modules, routes, stores, schemas: `engine/`, `web/`
    (routes, templates, `ui_text.py`), the live database schema, and migrations;
14. **tests / guards only where they establish implementation or invariant truth** — a
    guard that pins a behavior is evidence; a green suite is not, by itself, a
    capability.

**Historical material is evidence at its recorded time, not automatically current
authority.** Full historical reconstruction is used where FCORA's own trigger requires
it (Lean §6 names PRE-FCORA and explicit full-audit triggers); it is still bounded by
the actual question, and a prose or lifecycle mismatch immaterial to authority or
behavior is recorded, not escalated.

## 6. Master Checklist boundary

`MASTER CHECKLIST = OWNER-FACING DERIVED NAVIGATION VIEW` ·
`MASTER CHECKLIST ≠ SOURCE OF TRUTH` · `MASTER CHECKLIST ≠ EXECUTION AUTHORITY`.

FCORA may use it as a **coverage index** and must verify checklist ↔ repository
traceability in both directions rather than trusting the checklist as proof. A checklist
item marked complete is a claim to be verified against the corpus; an item absent from
the checklist is not thereby absent from the repository.

Recorded limits FCORA must carry rather than resolve by assertion: the reconstructed
current view is 54 items with `BASELINE UNMAPPED: 0`, and
`EXACT HISTORICAL MASTER-CHECKLIST ARTIFACT / FILE / SHA: UNKNOWN — RECOVERY
UNRESOLVED`. The reconstruction is structurally self-confirming; it is **not** evidence
of recovery and **not** proof that nothing disappeared. **FCORA must not create a
Master Checklist artifact** and must not treat the reconstructed denominator as an
exhaustive historical denominator. Where coverage cannot be established from the
corpus, the item is reported `UNRESOLVED` with its existing return gate, never silently
counted as covered.

## 6A. Materiality — bound to the existing C0–C4 model

"Material" is a load-bearing filter in five of the seven pass counters, so it is bound
here to existing authority. **FCORA invents no materiality scale.** It uses the change
classes already defined by `CROSS_LAYER_EXECUTION_ASSURANCE_STANDARD.md` §2, with their
exact repository meanings:

| Class | Repository meaning (§2, verbatim examples) |
|---|---|
| **C0** | trivial/local governance or text — typo fix, pin update, status entry |
| **C1** | bounded single-layer change — one module's internal logic, a display-only tweak |
| **C2** | material cross-layer change — new capability crossing engine + route + UI; changed carrier semantics |
| **C3** | state/persistence mutation — new/changed durable writes, idempotency, supersession |
| **C4** | user-facing composition change — new journey affordances, rendered semantics |

**6A.1 The binding.** For each audited item, FCORA assigns the class of the change that
the item's existence, absence, or corrected disposition would represent. An item at
**C1 or above is MATERIAL**. Only a genuine **C0** item — trivial/local governance or
text — may be classified non-material. An item spanning classes takes the union, and
therefore the highest class. Where the class is itself unclear, the item is treated as
material until the Owner decides otherwise (6A.4).

**6A.2 Every non-material classification must be justified on its face.** For each item
FCORA calls non-material it must record, in the return:

1. the applicable **C-level** (necessarily `C0`);
2. a **cited repository basis** — the specific file, section, row or commit that
   supports the classification; and
3. a **short rationale** in one or two sentences.

An item lacking any of the three is **not** non-material; it goes back into the
material population. Per the Standard's own §2, "the classification and every exclusion
are themselves reviewable statements" — a wrong class or an unjustified exclusion is a
review finding, not an audit convenience.

**6A.3 What can never establish non-materiality.** Silence; the absence of a complaint;
the absence of a test failure; the fact that nothing has broken yet; the age of an
item; the effort required to disposition it; the fact that counting it would prevent a
counter from reaching zero; or any other audit convenience. **Absence of evidence is
never evidence of non-materiality.** Non-materiality must be shown affirmatively from
cited authority, never inferred from what is missing.

**6A.4 Disputed or counter-affecting materiality goes to the Owner.** Where materiality
is disputed, ambiguous, or where the classification would change whether a pass counter
reaches zero, FCORA must return the item as **`OWNER DECISION REQUIRED`**, stating the
item, both candidate classifications and their consequences for the counters. **The
auditor must not resolve such a dispute in its own favour**, and must not pass with the
dispute unresolved: an unresolved counter-affecting materiality question leaves the
affected counter non-zero, which under §16 is verdict **C**.

**6A.5 Subject matter materiality cannot evade.** A materiality classification must
never be used to evade: canonical ownership; product truth; security; user-reachable
behavior; release blocking; obligation closure; evidence integrity; or current
authority consistency. An item touching any of these is **material regardless of any
C-level argument**, and no rationale under 6A.2 can move it out of the material
population.

**6A.6 All counter-affecting materiality decisions are exposed.** FCORA's return must
carry a materiality register listing **every** materiality decision that affects a
counter — item, assigned class, material/non-material, cited basis, rationale, and the
counter it affects — so a reviewer can re-derive each counter from the same evidence.

**6A.7 Class → counter interface.** Materiality feeds the counters through the
detection classes of §2, not through a separate judgement:

| Detection class | Counter it can raise |
|---|---|
| **A** documented, no implementation and no disposition | `UNACCOUNTED DOCUMENTED MATERIAL OBLIGATIONS` |
| **B** implemented, no owner/authority/disposition | `UNACCOUNTED IMPLEMENTED MATERIAL CAPABILITIES` |
| **C** duplicate ownership | `DUPLICATE CANONICAL OWNERS` |
| **D** silent disappearance | `SILENT DISAPPEARANCE CANDIDATES` |
| **E** superseded presented as current | `MATERIAL CURRENT-STATE AUTHORITY CONTRADICTIONS` |
| **F** implemented, release disposition missing | `MATERIAL ITEMS WITHOUT CURRENT DISPOSITION` |
| **G** governance contradicts runtime | `UNEXPLAINED MATERIAL DOC↔IMPLEMENTATION CONTRADICTIONS` |
| **H** runtime contradicts governing product truth | `UNEXPLAINED MATERIAL DOC↔IMPLEMENTATION CONTRADICTIONS` |

An item that is material and unresolved raises its counter. **A self-serving zero is
therefore impossible**: reaching zero requires either a disposition defensible from
cited authority, or an Owner decision — never the auditor's own judgement that an
inconvenient item did not count.

## 7. Pass conditions

FCORA passes only when **every** counter is exactly zero:

```
UNACCOUNTED DOCUMENTED MATERIAL OBLIGATIONS          = 0
UNACCOUNTED IMPLEMENTED MATERIAL CAPABILITIES        = 0
SILENT DISAPPEARANCE CANDIDATES                      = 0
DUPLICATE CANONICAL OWNERS                           = 0
UNEXPLAINED MATERIAL DOC↔IMPLEMENTATION CONTRADICTIONS = 0
MATERIAL CURRENT-STATE AUTHORITY CONTRADICTIONS      = 0
MATERIAL ITEMS WITHOUT CURRENT DISPOSITION           = 0
```

These implement, and do not relax, the Owner's `UNACCOUNTED / ORPHAN = 0` condition in
ODR §D-2. Counters are exact integers: no ranges, no approximations, no
scope-dependent alternatives.

Five of these counters are scoped by "material"; that word means exactly what §6A
binds it to, and every counter-affecting materiality decision is exposed per §6A.6.

**Every material item must end in a defensible current disposition.** "Defensible"
means the disposition is supported by identified repository authority, cited, and not
inferred from silence.

**FCORA does not require every future capability to be implemented.** A valid pass may
classify an item `DEFERRED & OWNED`, and a deferred item is not a defect.

## 8. Deferred-item rule

FCORA must distinguish:

**MUST BE DISPOSITIONED BEFORE FCORA CAN PASS** — any item that is unaccounted,
duplicated, silently disappeared, materially contradictory, presented as current while
superseded, at or past its latest-safe gate, falsely represented as completed, or
release-blocking for the current release decision.

**MAY REMAIN DEFERRED BEYOND FCORA** — provided **all** of the following hold:

1. explicitly owned (a named durable owner);
2. not silently disappeared (present and findable in its owner);
3. not at or after its latest-safe gate;
4. not falsely represented as completed;
5. not release-blocking for the current release decision.

If any one fails, the item moves to the blocking limb. **Deferred work is not promoted
into a blocker merely for being old, large, unimplemented or inconvenient.**

## 9. Release-gate boundary

FCORA sits **before** Serious Release / Production Readiness authorization.

```
FCORA PASS  ≠  RELEASE AUTHORIZATION
```

FCORA PASS does not authorize Serious Release, production, deployment, paid activation
or public launch. Those remain separate Owner / release gates with their existing
owners (PSRR registration, PDVG-01, the Phase-10 readiness surfaces) and are neither
satisfied, moved nor pre-empted by any FCORA outcome.

## 10. Readiness boundary

Current-version Readiness truth, preserved unchanged by FCORA:

- Technical — `INSUFFICIENT_EVIDENCE` only.
- Commercial — `INSUFFICIENT_EVIDENCE` only.
- Manufacturing — `INSUFFICIENT_EVIDENCE` only.

The Readiness Snapshot is authoritative and **read-only**: evidence-sufficiency
presentation, not a product verdict, not an overall or composite verdict, not a score,
not a percentage, not a weakest-link result, and no manufacturability conclusion.
FDC-001 / DecisionRecord remains the canonical decision owner.

**FCORA must not use its audit role to promote `PASS`, `PASS_WITH_CONDITIONS` or
`HOLD`, and must not create a qualifying-authority path.** Auditing an evidence
dimension is not awarding it a tier; `INDEPENDENTLY_VERIFIED` remains a value no owner
or system action may award. Readiness promotion remains a separate future Owner
authorization, and FCORA's own findings are not evidence for it.

## 11. Human and external evidence

FCORA authorizes none of: human-study execution; participant recruitment; interviews;
surveys; usability sessions; external-evidence collection; specialist validation;
independent-verification awarding.

`HUMAN-STUDY EXECUTION: NOT AUTHORIZED` · `EVIDENCE COLLECTION: NOT AUTHORIZED` remain
in force, as do the existing owners, triggers and return conditions of the A2
claim-eligibility human-review evidence gate, CEHR / Route-B, T1-A′, HICR, RUN-004,
G-4-A, G-4-B, M-1, F-03 and F-04. Auditing a gate never satisfies it; FCORA reports a
gate's state and leaves it standing.

## 12. Evidence reuse — fewer loops, same or higher assurance

Per Lean §5B and AHAEP: **reuse accepted evidence for unchanged facts.** FCORA must
**not** rerun full test suites, closed historical reviews or completed phase analyses
unless the audit finds a **material reason that invalidates the prior evidence** —
named, cited and recorded when invoked.

Differential verification is preferred: establish what changed since the accepted
evidence (by tree/path comparison and merge ancestry) and verify only that. An unchanged
path with accepted evidence is not re-derived. When prior evidence is reused, FCORA
records which evidence, from which gate, and why it still holds.

## 13. Review-loop compression — standing process rule

FCORA execution applies the `OWNER REVIEW-LOOP COMPRESSION REQUIREMENT`:

- **single-pass defect accumulation** — findings are accumulated, then returned once;
- **complete material finding set** — no drip-feed of findings across rounds;
- **dependency-bounded sweep** — follow only what the question actually depends on;
- **no minor-only repair lifecycle** — cosmetic and MINOR items are recorded, not
  given their own gate;
- **no reviewer recursion without material decision impact**;
- **no reopening of closed work without new material evidence.**

## 14. Execution model — read-only audit first

**FCORA executes as a READ-ONLY audit.** During the audit FCORA does not modify
repository files, create commits or branches, push, open or modify PRs, merge,
implement fixes, promote readiness states, collect evidence, or reopen completed work.

If FCORA finds a material defect, FCORA **classifies and returns it**. FCORA does
**not** implement the repair. Any repair requires a **separate bounded Owner
authorization**, following the G-MPR-01 → G-MPR-01-D precedent (audit, then a distinct
disposition/repair gate) and the PRE-FCORA → PR #653 / PR #654 precedent already
executed under this project's own history.

FCORA does not authorize itself: execution requires an authoritative merged FCORA
contract **and** a separate Owner FCORA EXECUTION authorization.

## 15. Required FCORA outputs

FCORA execution returns **one consolidated report** containing:

1. exact authoritative HEAD and tree, branch, repository, clean-state result;
2. the corpus **actually** inspected (not the aspirational list), with what was reused
   rather than re-derived and why;
3. **docs→implementation** findings (class A, E, G);
4. **implementation→docs** findings (class B, F, H);
5. obligation dispositions — every material documented obligation with its disposition
   and cited authority;
6. capability dispositions — every material implemented capability likewise, with
   `PARTIALLY IMPLEMENTED` decomposed by missing layer;
7. duplicate-owner findings (class C);
8. silent-disappearance findings (class D);
9. unresolved material contradictions;
10. deferred-but-owned items, each showing all five §8 conditions met;
11. release-blocking items;
12. non-blocking future items;
13. any `OWNER DECISION REQUIRED` items returned undecided per §3 or §6A.4;
14. the **materiality register** required by §6A.6 — every counter-affecting
    materiality decision with its class, cited basis, rationale and affected counter;
15. the exact counters:

```
UNACCOUNTED DOCUMENTED MATERIAL OBLIGATIONS            = <int>
UNACCOUNTED IMPLEMENTED MATERIAL CAPABILITIES          = <int>
SILENT DISAPPEARANCE CANDIDATES                        = <int>
DUPLICATE CANONICAL OWNERS                             = <int>
UNEXPLAINED MATERIAL DOC↔IMPLEMENTATION CONTRADICTIONS = <int>
MATERIAL CURRENT-STATE AUTHORITY CONTRADICTIONS        = <int>
MATERIAL ITEMS WITHOUT CURRENT DISPOSITION             = <int>
```

16. the verdict per §16, and an explicit statement that FCORA performed no repository
    mutation and that release is not authorized.

## 16. Final verdict model

Exactly three verdicts:

| Verdict | Meaning |
|---|---|
| **A — FCORA PASS** | all seven counters are 0 and no meaningful deferred items remain |
| **B — FCORA PASS WITH NON-BLOCKING DEFERRED ITEMS** | all seven counters are 0, and the remaining deferred items each satisfy all five §8 conditions |
| **C — FCORA FAIL — MATERIAL RELEASE-BLOCKING RECONCILIATION DEFECT** | any counter is greater than 0 |

**A and B do NOT authorize release automatically** — see §9. **C identifies material
defects but does NOT authorize their implementation** — see §14. No verdict may be
self-certified as satisfying any other gate.

## 17. What this contract does not authorize

This document authorizes nothing. Specifically it does not authorize: FCORA execution;
product implementation; code, runtime, schema, migration, route, configuration or CI
changes; architecture creation or product redesign; positive Readiness promotion;
human or external evidence work; Serious Release; production; deployment; paid
activation; public launch; MCP; CAD/PCB/BOM; supplier APIs; or any CAP activation.

`FCORA EXECUTION AUTHORIZED: NO` · `FCORA STARTED: NO` ·
`SERIOUS RELEASE AUTHORIZED: NO` · `READINESS PROMOTION AUTHORIZED: NO` ·
`HUMAN-STUDY EXECUTION: NOT AUTHORIZED` · `EVIDENCE COLLECTION: NOT AUTHORIZED`.

Completing this contract's own lifecycle authorizes no successor phase or capability.
Merging it makes the **procedure** authoritative, not the audit.

## 18. Compliance statement for this document

Governance-only. Drafted by read-only reconstruction against base
`fafc94e151a4a6f06f8445dde1373bbac0212200`. No product, runtime, test, schema,
migration, route, configuration or CI file is touched by the candidate that introduces
it. No second roadmap, register, checklist or traceability registry is created. The
FCORA obligation row in `DEFERRED_OBLIGATIONS_REGISTER.md` §3 keeps its owner, origin,
disposition, return trigger, latest-safe gate, `FRB` level and required closure
evidence unchanged; nothing in it is discharged by this document. ODR §D-2 is
implemented, not amended. Per Lean §2, only an explicit Owner instruction may authorize
the execution this contract describes.
