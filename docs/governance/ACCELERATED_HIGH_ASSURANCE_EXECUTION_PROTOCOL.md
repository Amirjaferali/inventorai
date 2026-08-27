# InventorAI Accelerated High-Assurance Execution Protocol (AHAEP)

**Document ID:** ACCELERATED_HIGH_ASSURANCE_EXECUTION_PROTOCOL
**Type:** General lifecycle-mechanics standard operating protocol.
**Status:** PROPOSED / NON-AUTHORITATIVE — this document becomes authoritative only
if and when the exact candidate introducing it completes the full governed adoption
lifecycle: Independent Focused Governance Review, Owner exact-SHA acceptance, merge
via CREATE A MERGE COMMIT, and post-merge identity verification. Until then no rule
in this document governs anything.
**Subordinate to:** `CLAUDE.md`; `docs/governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md`
(binding; "Lean" below); the committed anchors; `MVP_SCOPE_FREEZE.md`;
`docs/governance/ACTIVE_EXECUTION_ROADMAP.md`; `docs/governance/ACTIVE_INCREMENT_CONTRACT.md`;
`docs/governance/OWNER_DECISION_REGISTER.md`; `docs/governance/DEFERRED_OBLIGATIONS_REGISTER.md`.
This protocol weakens no existing governance rule, review requirement, hold, or
authorization boundary.
**Permanently non-authorizing:** see §25.

---

## 1. Purpose and central principles

This protocol is the single documented owner of the **general candidate-lifecycle
mechanics** of the governed workflow — the layer previously carried only by standing
practice and per-gate instruction (the layer the Cross-Layer Standard's ownership map
calls "standing protocol + established workflow").

**Central principle:** *Accelerated does not mean fewer proofs. It means fewer proofs
of unchanged facts.*

**Anti-bureaucracy principle (applies to this protocol itself):** every element of
this protocol must provide proof, prevent a material failure, or eliminate redundant
work. An element doing none of these must be removed through the amendment rule
(§26). Compliance artifacts required here are deliberately compact; ceremonial
acknowledgement pages are themselves a protocol violation.

**Evidence principle:** generated evidence must be *reproducible*, not merely
machine-produced: every material evidence value carries its derivation method so an
independent party can recompute it. Machine evidence is evidence, never a source of
authority — repository/Git truth remains the authority over any generated artifact.

## 2. Ownership boundary

### 2.1 THIS PROTOCOL OWNS (general lifecycle mechanics only)

live-base guard; differential reconstruction; bounded candidate creation and
exact-SHA freeze; candidate identity and the no-rewrite rule; Creator Grill
mechanics; rejected-candidate evidence preservation and sibling differential
repair; the consolidated repair loop and closed-finding finality; lifecycle
finding-disposition classes; the review loop breaker; SHA-preserving bundle
mechanics; machine-evidence provenance and gate-report shape; execution modes
(§4); the Execution-Reachability Check; protocol-compliance evidence (§21);
the Owner exact-SHA acceptance boundary; Owner-controlled publication mechanics;
PR verification and the platform-mutation guard; separate merge authorization;
CREATE A MERGE COMMIT discipline and the exact-head guard; post-merge identity
verification; the post-merge governance-sync YES/NO decision mechanics; and the
per-gate Product Value review **obligation** (obligation only — never product
semantics).

### 2.2 THIS PROTOCOL REFERENCES BUT DOES NOT OWN

Lean risk LEVEL classification (Lean §3); Lean review DEPTH (Lean §4); Lean
independent-review policy and formal review independence (Lean §5); Lean
pre-delivery adversarial self-review (Lean §5A); Lean review economy, evidence
reuse, and full-suite trigger policy (Lean §5B); Lean governance recording
cadence (Lean §11); the Universal Guardrail Smoke floor
(`INVENTORAI_UNIVERSAL_CORE_GUARDRAIL_SMOKE_STANDARD.md`); Cross-Layer assurance
mechanisms C0–C4 (`CROSS_LAYER_EXECUTION_ASSURANCE_STANDARD.md`); the Deferred
Obligations Register and its return-gate rules; the Owner Decision Register;
FCORA (Owner Decision Register §D-2 and its register row); product-value
semantics (`STRATEGIC_PRODUCT_VISION.md`,
`INVENTORAI_COMMERCIAL_DIFFERENTIATION_DIRECTION.md`, `MVP_SCOPE_FREEZE.md`);
and the canonical architecture/domain owners.

This protocol never restates a referenced owner's definitions. Where any
referenced owner requires stricter verification, review, or reporting, the
referenced owner controls.

### 2.3 THIS PROTOCOL MUST NEVER OWN

current SHA or any volatile current state; the current RVR or any gate's
current status; any current or rejected candidate identity; roadmap truth;
Owner decisions; deferred-obligation contents; product requirements or
identity; architecture semantics; release, deployment, or production
authorization; risk taxonomy; review-depth taxonomy.

### 2.4 Non-duplication and false-force-fit balance

Every governance placement decision under this protocol protects BOTH
invariants: `NO DUPLICATE SEMANTIC OWNER` and `NO FALSE FORCE-FIT INTO AN
EXISTING OWNER`. A rule must live with its correct owner even when a tidier
single-document architecture would be more convenient, and a rule must not be
forced into an owner whose scope does not truly cover it. Existing mentions of
this protocol's mechanics inside other authoritative documents (for example a
quality-floor guarantee enumerating them, or a pipeline diagram naming them)
are references and guarantees, never competing definitions.

## 3. Applicability

This protocol governs material candidate-lifecycle work: any work intended to
produce, repair, review, accept, publish, merge, or synchronize a governed
candidate. It does not govern conversational analysis, and it adds no ceremony
to work that mutates nothing. Lean LEVEL/DEPTH determine how much scrutiny an
operation needs; this protocol determines the lifecycle steps through which
that scrutiny flows.

## 4. Execution modes (non-risk lifecycle axis)

Execution mode classifies the **lifecycle shape** of an operation. It is
orthogonal to — and can never substitute for or weaken — Lean risk LEVEL and
review DEPTH. (Heritage: migrated and renamed from the operation classes of the
superseded `GOVERNED_EXECUTION_EFFICIENCY_PROTOCOL.md` §3, which mislabeled
this axis "risk"; the risk axis belongs solely to Lean §3/§4.)

- **FULL SEMANTIC LIFECYCLE** — the operation changes meaning, behavior,
  authority, or product reality. Full lifecycle: reconstruction → implementation
  → freeze → Grill → bundle → independent review per Lean → Owner exact-SHA
  acceptance → Owner-controlled publication → verified merge → post-merge
  verification and sync decision.
- **FOCUSED DIFFERENTIAL LIFECYCLE** — a bounded delta over an already deeply
  verified baseline (typically a same-base sibling repair or a bounded
  governance candidate). The lifecycle runs over `previously proven claims +
  authorized delta` (§7, §12), never over a from-scratch reconstruction of
  unchanged truth.
- **MECHANICAL LIFECYCLE** — an identity-preserving operation that moves or
  verifies an already-reviewed exact artifact without changing repository
  content or authority (staging, verification, bundle creation, fetch-back,
  identity checks). Required workflow: pre-operation identity verification →
  the exact authorized operation → post-operation identity verification →
  targeted smoke where applicable → stop. Identity in must equal identity out;
  any identity or scope mismatch blocks immediately.

**Mandatory coupling rules:**

1. Execution mode may NEVER lower any Lean LEVEL/DEPTH requirement, any Lean
   §5/§5A/§5B review requirement, or any referenced owner's requirement.
2. When one authorization bundles distinct operations, the highest applicable
   mode governs the whole operation.
3. Uncertainty escalates the mode; it never de-escalates it.
4. Mode classification is provisional until evidence closes: new evidence
   discovered during execution may invalidate the initial mode selection, and
   the operation then re-enters under the corrected mode.
5. For material work the declared mode is recorded separately from the Lean
   LEVEL/DEPTH in the compliance blocks (§21) so the two axes stay auditable.

## 5. Live-base guard

Before candidate construction, before publication, and before every applicable
mutation, the executor fetches the live authoritative branch and proves
`LIVE_BASE == EXPECTED_BASE` from Git (never from a prose-pinned SHA). If the
base advanced: **STOP — BASE ADVANCED.** Report the new tip; never rebase or
silently reconstruct the candidate on the new base; the gate re-enters from
current authoritative truth under its governing authorization.

## 6. Differential reconstruction

Default review and reconstruction scope for a gate:

```text
LAST VERIFIED AUTHORITATIVE TRUTH
+ CURRENT DELTA
+ NEWLY FIRED OBLIGATIONS
+ NEW OWNER DECISIONS
=================================
CURRENT REVIEW SCOPE
```

Unchanged, previously verified project truth is not re-reconstructed without
cause (a §7 invalidation, a fired obligation, a full-audit trigger under Lean
§6, or an explicit instruction). Reconstruction is performed from authoritative
repository sources — never from conversation memory, templates, or rejected
candidates.

## 7. Assurance reuse (claim-scoped, dependency-scoped, self-invalidating)

**Claim-scoped:** evidence inheritance attaches to individual claims, never to
whole candidates. A candidate is never inherited wholesale because one of its
conclusions was previously verified.

**Dependency-scoped:** each inherited claim must identify: the claim; the
identity it was verified at; the relevant tree/path identity; its dependencies;
its evidence; its invalidation conditions; whether the current delta touches
any dependency; and the result — `INHERITED`, `REVALIDATED`, or `INVALIDATED`.

**Self-invalidating:** new material evidence may invalidate any inherited
conclusion. Previous acceptance is never immune from new contradictory
evidence.

**Boundary with Lean §5B:** this section governs the Creator-side construction
of lifecycle scope across gates and candidates. Independent-Review evidence
reuse remains governed exclusively by Lean §5B; where a claim enters an
Independent Review, §5B controls what the Reviewer may reuse and what must be
independently rerun.

## 8. Execution-Reachability Check

"Docs-only" does NOT automatically prove zero runtime semantic delta. Before
inheriting any runtime or test conclusion across a change, prove either:

- **A.** the changed artifacts are not execution-, build-, generated-,
  config-, registry-, or loader-reachable; or
- **B.** every dependency supporting the inherited runtime conclusion remains
  byte-identical to its verified baseline.

Only then may the gate conclude `NO RUNTIME-REACHABLE SEMANTIC DELTA`, and the
conclusion must state which branch (A or B) carries it and on what evidence.

## 9. Candidate identity, freeze, and the no-rewrite rule

A material candidate is identified by its exact: commit SHA; parent(s) and
topology; tree; path manifest; and diffstat. After freeze: no amend, no rebase,
no squash, no rewrite of the frozen commit — ever. A frozen candidate that
needs change is replaced by a fresh sibling (§12); it is never mutated. A
candidate must not contain its own SHA in its tree (anti-circularity); its
identity lives in evidence artifacts outside the tree.

## 10. Creator lifecycle and Creator Grill

Where appropriate the Creator completes one governed session workflow:

```text
RECONSTRUCT → IMPLEMENT → CREATE → FREEZE → GRILL
→ BOUNDED SAME-SESSION REPAIR IF REQUIRED (as a fresh sibling, §12)
→ BUNDLE → RETURN ONLY THE GRILL-PASSED CANDIDATE
```

The **Creator Grill** is the Creator's mandatory adversarial self-interrogation
of the frozen candidate before delivery (it implements and extends the Lean §5A
self-review obligation at candidate level; §5A's required output block remains
mandatory where Lean requires it). Grill depth is risk-proportional: it follows
the semantic risk and the affected material claims of the specific candidate —
Grill quality outranks Grill question count. A Grill that fails blocks
delivery; only a Grill-passed candidate is returned.

## 11. Evidence integrity

An incorrect material evidence count or identity claim is a candidate/review
defect even if the underlying runtime behavior is correct (for example, "N
tests" claimed where N+1 actually ran, or an executed-module manifest that
conflates separate runs). Material quantities are mechanically collected or
derived, never hand-tallied; corrections are recorded with their root cause,
never silently overwritten.

## 12. Rejection handling and sibling differential repair

**Rejected evidence preservation:** a rejected frozen SHA remains rejected
evidence permanently. It is never relabeled as accepted, never rewritten, and
never made an ancestor of a later candidate. Rejected-evidence artifacts may be
local to the Creator environment (refs/bundles) and are recorded as such per
Lean §5B.15.

**Sibling differential repair:** a narrowly defective, deeply reviewed
candidate is repaired as a **fresh same-base sibling** (same exact authoritative
base; the rejected SHA is not an ancestor). Review scope for the sibling:

```text
PREVIOUSLY PROVEN CLAIMS + AUTHORIZED REPAIR DELTA = CURRENT REVIEW SCOPE
```

Previously verified claims may be inherited only under §7 (dependencies
unchanged); the repair delta must be proven to be exactly the authorized repair
and nothing else.

**Consolidated repair loop:** prefer one complete review → one consolidated
material-finding set → one bounded correction batch → one focused closure
review. Findings are not intentionally deferred to later rounds, no finding
quota is invented, and unnecessary micro-rounds are not generated. A later,
additional finding is legitimate only when it depends on the correction itself
or its evidence was genuinely unavailable earlier.

**Closed-finding finality:** a finding recorded as closed, resolved, or
accepted may not be reopened unless new repository evidence directly
contradicts the recorded closure or a higher authority changed. Reopening
requires naming: the exact new evidence; the earlier closure; the direct
contradiction; and why reopening is necessary now. A new preference is not new
evidence.

## 13. Finding disposition

Lifecycle findings are classified as exactly one of:

- **BLOCKER** — always blocks the current lifecycle transition: safe or valid
  completion is impossible, required authority is missing, or the operation
  cannot lawfully proceed.
- **MAJOR** — always blocks: a material contradiction, scope breach,
  incorrect authority, substantive non-regression risk, or an
  implementation-invalid contract.
- **MINOR** — blocks only while it leaves implementation behavior, a test
  expectation, authority, deterministic identity/ordering, security,
  authorized scope, user-visible truthfulness, or required evidence integrity
  unresolved. A purely stylistic or optional-tightening MINOR does not block.
- **OBSERVATION** — never blocks the current operation.

No agent may relabel a material defect downward to avoid a gate, nor inflate a
stylistic preference to force one. Genuine classification uncertainty is
escalated (Lean §10), never resolved in the classifier's own favor.
(Heritage: migrated from the superseded `GOVERNED_EXECUTION_EFFICIENCY_PROTOCOL.md`
§4; this is the single canonical lifecycle finding taxonomy — no other document
defines a competing one.)

**Non-blocking proof:** a material finding may be dispositioned NON-BLOCKING
for the current gate only when evidence proves ALL of: it does not block the
current gate; it has a legitimate owner; it has a return trigger; it has a
latest safe gate; it remains discoverable (registered where required — the
Deferred Obligations Register owns deferred content); it creates no orphan; and
the deferral creates no unacceptable future risk. Unresolved material
uncertainty is never non-blocking.

## 14. Review loop breaker

Before requesting another review round on the same candidate lineage, the Lead
must identify at least one explicit question whose answer could materially
change the gate decision. If no such question exists: stop reviewing and
advance the gate. If the same issue cycles repeatedly without material new
evidence, the Lead forces adjudication to exactly one of: `ACCEPT`,
`BOUNDED REPAIR`, or `OWNER DECISION`. A genuine new BLOCKER/MAJOR is never
suppressed by any loop limit.

## 15. Independent review interface

Independent External Review policy — when it is required, its independence
conditions, its universal minimum, its evidence-reuse rules, and its full-suite
triggers — is owned by Lean §5/§5B and is unchanged by this protocol. Formal
Closure candidates always receive Independent Review. This protocol adds only
the lifecycle interface:

- the Reviewer receives the frozen candidate via the SHA-preserving bundle
  (§17) and independently verifies its identity per Lean §5/§5B.3;
- the Reviewer reviews the current delta and newly fired obligations, attempts
  falsification, and remains free to invalidate any previously verified
  finding (§7 self-invalidation applies to reviews too);
- **same-reviewer continuity without anchoring:** a connected candidate
  lineage may reuse the same Independent Reviewer to reduce onboarding cost,
  subordinate to Lean §5 independence (the Reviewer must still not have
  authored or modified the candidate). A follow-up review must explicitly
  separate: the inherited independently verified baseline; the new delta;
  newly fired obligations; and the conclusions requiring fresh falsification.
  A previous verdict is never evidence.

**Formal Closure semantic-risk classification:** a Formal Closure gate is not
automatically low-risk or automatically focused. Its scope is classified by
semantic consequence and escalated when the closure would change: authority;
canonical ownership; a disputed obligation's resolution; downstream
authorization semantics; release blockers; dependencies; or acceptance
criteria. Risk LEVEL itself remains a Lean §3 classification.

## 16. Machine evidence

**Machine-generated Evidence Manifest:** where useful, gate evidence is
generated outside the candidate tree as a manifest (for example
`candidate-evidence.json`). Every material field carries both a `value` and a
`derived_by` (its derivation method/command), so it is independently
reproducible. Typical fields: base; candidate SHA; parent(s); tree; commit
count; path list and count; insertions/deletions; self-SHA occurrence check;
bundle prerequisite; bundle SHA-256; fetch-back identity; relevant test
evidence; runtime-reachability classification with its basis (§8).

**Machine-provable vs human-reasoned:** facts that Git or tooling can prove
mechanically (base, SHA, parent, tree, commit count, paths, diffstat, bundle
prerequisite and hash, remote exact SHA, merge parents, merge tree,
candidate→merge diff) are proven mechanically — agent prose never substitutes
for available mechanical proof. Judgments that require reasoning (authority,
supersession, obligation-trigger meaning, architecture ownership,
false-force-fit, product value, invalidation conditions, orphan risk,
release/security materiality) require explicit human/semantic review and are
never delegated to a script's exit code.

## 17. SHA-preserving bundle

A material reviewed candidate is transferred by SHA-preserving bundle where
current governance requires it: the bundle carries the exact frozen commit
object over the exact authoritative prerequisite. Creator-side procedure:
create the bundle against the exact base; record its SHA-256; verify it
(`git bundle verify`, head listing); and prove **isolated fetch-back** — in a
clean repository, fetching the base from authoritative truth and the candidate
from the bundle reproduces the exact candidate SHA, sole parent, and tree.
Bundle identity must be independently reproducible; Reviewer-side verification
duties remain owned by Lean §5/§5B.3.

## 18. Owner exact-SHA acceptance

Independent Review does not equal Owner acceptance. Owner acceptance attaches
to the exact reviewed candidate SHA and to nothing else. Eligibility is not
authorization; authorization is not acceptance; acceptance of one gate is not
closure of another; no status is ever treated as a different status. Any
mutation after acceptance requires a new governed candidate or sibling — the
accepted SHA is never edited.

## 19. Publication

**Owner-controlled publication default:** Creator candidate preparation ends
before publication unless publication is separately and explicitly authorized.
Owner exact-SHA acceptance does not itself authorize the Creator to publish.
Publication (branch push, PR creation) follows the Owner-controlled governed
lifecycle. The historical fast path of the superseded efficiency protocol is
NOT active (§23).

**SHA-preserving publication:** publication must preserve the exact accepted
candidate object: no amend, no rebase, no cherry-pick recreation, no
equivalent-but-different commit. The published head is the accepted SHA.

**PR verification:** before merge consideration, verify from live platform
truth: exact base; exact head (= accepted SHA); exact paths and diff; body
truth (the PR describes the candidate truthfully); absence of substantive
platform mutation; and mergeability.

**Platform-mutation guard:** publication and PR mechanics must detect and
reject unexpected substantive mutation, including: wrong head; wrong base;
extra commits; content mutation; materially added trailers or disclaimers;
changed title/base/head; added reviewers, labels, auto-merge, or any other
unauthorized lifecycle mutation. Harmless platform normalization (rendering
entities, terminal-newline display, JSON escaping in tool output, API field
order) does not block and is disclosed when relevant; committed repository
artifacts themselves always keep strict byte identity. (Heritage: migrated
from the superseded `GOVERNED_EXECUTION_EFFICIENCY_PROTOCOL.md` §8.)

## 20. Merge and post-merge

**Separate Owner merge authorization:** Owner exact-SHA acceptance does NOT
imply merge authorization. Merge is always a separate Owner decision;
automatic merge is never permitted; CI, smoke, or review success is never
merge authority. (Heritage: consolidates the superseded risk model §6 and
efficiency protocol §9.)

**CREATE A MERGE COMMIT only:** where established doctrine requires
merge-commit identity, the merge uses CREATE A MERGE COMMIT — never a squash
or rebase replacement that would destroy the accepted candidate's identity.

**Exact-head guard:** where the platform supports it, the merge is guarded so
it can only merge the exact accepted head (for example
`--match-head-commit <EXACT_ACCEPTED_SHA>`); where no mechanical guard exists,
the head SHA is verified immediately before merge.

**Post-merge identity verification:** before any gate reports
`AUTHORITATIVE: YES`, prove from live Git truth: expected parent count; first
parent = prior authoritative base; second parent = the exact accepted
candidate; merge tree = candidate tree (where the merge is expected to be
tree-identical); candidate→merge diff = EMPTY; PR state = MERGED; and the
authoritative branch tip = the merge commit.

**Post-merge governance-sync decision:** after every material merge the gate
explicitly returns `POST-MERGE GOVERNANCE SYNC REQUIRED: YES / NO`, with: the
reason; the canonical surfaces whose truth changed; and, if NO, why no
material canonical truth changed. Merge alone does not automatically require a
sync. This protocol owns only this decision mechanics; the recording cadence
and update responsibilities remain owned by Lean §11 and the registers'
own rules.

## 21. Protocol compliance as gate evidence

Compliance with this protocol is **gate evidence**, not reading advice. A
material candidate is not gate-ready merely because an agent claims to have
read this document. Compact compliance blocks are required at: start of
material work; candidate return; Independent Review; and Lead adjudication.

### 21.1 Start-of-material-task block (required minimum)

```text
PROTOCOL COMPLIANCE — TASK START
SOP READ: YES
LEAN RISK LEVEL: <per Lean §3>
LEAN REVIEW DEPTH: <per Lean §4>
SOP EXECUTION MODE: FULL SEMANTIC / FOCUSED DIFFERENTIAL / MECHANICAL
INHERITED CLAIMS: <or NONE>
DEPENDENCIES: <of inherited claims, or N/A>
INVALIDATION CONDITIONS: <or N/A>
CURRENT DELTA: <bounded statement>
NEWLY FIRED OBLIGATIONS: <or NONE>
ESCALATION TRIGGERS: <mode/level escalation conditions being watched>
KNOWN PROTOCOL DEVIATIONS: NONE / <describe>
```

### 21.2 Candidate-return block (required minimum)

```text
PROTOCOL COMPLIANCE — CANDIDATE RETURN
LIVE BASE GUARD: PASS / FAIL
LEAN LEVEL / DEPTH PRESERVED: YES / NO
EXECUTION MODE: <final mode; note any mid-task escalation>
CLAIM-SCOPED ASSURANCE REUSE: PASS / N/A
DEPENDENCY INVALIDATION SWEEP: PASS
EXECUTION-REACHABILITY: PASS / N/A
DOR FIRED OBLIGATIONS: ACCOUNTED / N/A
ARCHITECTURE OWNER SWEEP: PASS / N/A
PRODUCT VALUE REVIEW: PASS / N/A
REJECTED-SHA / NO-REWRITE RULE: PASS / N/A
EVIDENCE INTEGRITY: PASS
INDEPENDENT REVIEW REQUIRED: YES / NO + BASIS
OWNER EXACT-SHA ACCEPTANCE REQUIRED: YES
SEPARATE MERGE AUTHORIZATION REQUIRED: YES
PROTOCOL DEVIATIONS: NONE / <describe>
```

A material protocol deviation is never hidden: it is declared and its
consequence classified under §13.

### 21.3 Independent Review compliance check

An applicable Independent Review reports:

```text
SOP COMPLIANCE: PASS / FAIL
CREATOR COMPLIANCE CLAIM VERIFIED: YES / NO
MATERIAL PROTOCOL DEVIATIONS: <or NONE>
DOES ANY DEVIATION CHANGE THE GATE DECISION: YES / NO
```

The Reviewer reconstructs material compliance independently where evidence
permits; Creator self-certification is never sufficient.

### 21.4 Lead gate rule

A candidate is not ready to be presented for Owner exact-SHA acceptance until
the Lead is satisfied with BOTH: (1) the candidate's semantic truth; and
(2) its protocol-compliance truth.

## 22. Interfaces to referenced owners

- **Security/release escalation:** security, privacy, billing, legal-sensitive
  release, production, destructive-data, irreversible-migration,
  serious-release, or equivalent risk is Lean LEVEL 1 territory (Lean §3);
  such work automatically takes the FULL SEMANTIC LIFECYCLE mode and every
  Lean escalation, as repository truth requires. This protocol adds no
  independent security taxonomy.
- **Deferred Obligations Register consultation:** gates do not deeply
  re-review every deferred obligation at every gate. An obligation enters the
  gate's scope when: its return trigger fires; a dependency is touched; its
  latest safe gate approaches; a release gate fires; or FCORA occurs. Closing
  a register row must never cause obligation loss. This protocol owns only
  this consultation mechanics; the register owns its content and rules.
- **FCORA:** the Final Complete Obligation Reconciliation Audit remains
  owned and governed by its canonical source (Owner Decision Register §D-2
  and its register row). The accelerated workflow must never hide long-tail
  obligations from it.
- **Product Value review obligation:** material product/runtime work must
  demonstrate actual product/user/decision value at its gate (the material
  gap / product-value sweep). A mechanical pass with no served product
  difference is a product-value failure to be reported, not masked. This
  protocol owns only the obligation to perform this review; what counts as
  product value is owned by the product anchors (§2.2). (Heritage: obligation
  migrated from the superseded `GOVERNED_PRODUCT_EXECUTION_PROTOCOL.md` §A/§D.8.)

## 23. Historical / deferred mechanisms — NOT ACTIVE

**Bounded reversible mechanical fast path (historical EF §9.1):** the
superseded `GOVERNED_EXECUTION_EFFICIENCY_PROTOCOL.md` §9.1 defined a
conditional mechanism by which one explicit Owner authorization could cover a
bounded reversible pre-merge sequence (verification → exact-path staging →
commit → normal non-force push → PR creation) under strict preconditions.

Classification: `HISTORICAL / DEFERRED OPTIONAL MECHANICAL FAST PATH — NOT
ACTIVE`. `REQUIRES SEPARATE FUTURE OWNER AUTHORIZATION BEFORE ANY USE.`

This protocol does NOT activate that mechanism, does not carry it as standing
authority, and grants no pre-authorization of any kind. The Owner-controlled
publication default (§19) governs. Any future activation would itself be a
governed protocol amendment (§26) plus an explicit Owner decision — never an
inference from this record.

## 24. Current-state separation

This protocol never hard-codes: a current SHA; the current RVR or gate; a
current or rejected candidate; the current next gate; or any other volatile
current state. Volatile state is owned exclusively by the canonical
current-state surfaces (`CURRENT_PROJECT_STATE.md`, the roadmap, the
registers, the active contract). This protocol is written to remain stable
across future RVRs; the currency of its examples is never evidence of current
state.

## 25. Permanent non-authorization

This protocol defines HOW governed work moves through its lifecycle. It
authorizes NOTHING. It does not activate, and can never be cited to activate:
any RVR or gate; any capability; any merge; any release; any deployment; any
domain; any payment/billing behavior; any production operation. Adoption of
this protocol confers no execution authority and starts no downstream work.
Every lifecycle mutation remains separately Owner-authorized under the
applicable authorities.

## 26. Amendment rule

This protocol is NOT amended merely because the current SHA, RVR, candidate,
or project state changes (§24 makes that unnecessary). It is amended only
for: a proven workflow defect; a validated better control; an architecture
requirement; an explicit Owner safeguard change; or authoritative
supersession. Material amendments follow the full governed candidate
lifecycle defined here, including Independent Review and Owner exact-SHA
acceptance.

## 27. Legacy migration and supersession record

This protocol was introduced together with the status adjudication of three
legacy process documents (each retains its full original text below its
banner as historical record):

- `RISK_BASED_EXECUTION_AND_REVIEW_MODEL.md` → `SUPERSEDED — HISTORICAL ONLY`.
  Its risk taxonomy is superseded by Lean §3/§4; its Draft-PR-default and
  bundle-by-exception rules contradict current doctrine; its separate-merge
  rule (§6) is consolidated into §20 here.
- `GOVERNED_PRODUCT_EXECUTION_PROTOCOL.md` → `SUPERSEDED — HISTORICAL ONLY`.
  Its product-value review obligation survives as §22 here (semantics remain
  anchor-owned); its finding classification is superseded by §13; its
  embedded constraint-status table is a historical snapshot, never current
  truth.
- `GOVERNED_EXECUTION_EFFICIENCY_PROTOCOL.md` → `SUPERSEDED — RULES
  MIGRATED`: §3 → §4 here (execution modes, de-risked); §3.1 → §4 MECHANICAL
  workflow; §4 → §13; §5 → §12 closed-finding finality; §6 → §12 consolidated
  repair loop; §7 → §16 evidence economy; §8 → §19 platform-mutation guard;
  §9 → §19/§20 owner-gating and separate merge authorization; §9.1 → §23
  (NOT ACTIVE); §10 → §21/§16 report shape.

No unique legacy safeguard was discarded without a named successor; no legacy
rule already owned by a current authority was duplicated here.

---

*This document owns general lifecycle mechanics only. It is subordinate to
CLAUDE.md and the Lean protocol, defers to every referenced owner, embeds no
volatile current state, and authorizes nothing.*
