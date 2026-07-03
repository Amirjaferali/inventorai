# Governed Execution Efficiency Protocol

Status:
`ACTIVE SUBORDINATE OPERATIONAL PROTOCOL`
`— DOES NOT MODIFY PRODUCT, ANCHOR, SCOPE, OR LIFECYCLE AUTHORITY`

## 1. Purpose and bounded subject

This protocol governs, and governs ONLY:

- how an already-authorized operation is verified;
- review economy (how much review a given operation actually requires);
- finding disposition (which findings block a lifecycle transition);
- reporting economy (what evidence a report must contain).

It does NOT govern product behavior, architecture, state model, scope, anchors,
the roadmap, tests-first authority, source authorization, or any lifecycle gate.
It defines HOW an operation the owner has already authorized is efficiently
verified and reported — never WHETHER an operation may occur. Every lifecycle
mutation remains separately owner-authorized.

This protocol codifies existing repository practice (non-blocking observations,
closed-state finality, separate owner-gated lifecycle steps, repository-evidence
requirements). It introduces no new lifecycle authority and requires no anchor
amendment.

## 2. Authority hierarchy

This protocol is subordinate to committed repository authority and to the owner
authorization for the operation in hand. Two principles govern together:
repository authority and controlled anchor boundaries determine what MAY be
authorized; the explicit current owner authorization determines the exact
operation performed WITHIN those already-valid boundaries.

Authority order (each item is subordinate to those above it):

1. active anchors and `MVP_SCOPE_FREEZE.md`;
2. approved and committed controlled amendments or higher-authority governance
   changes applicable to those anchors or freezes;
3. `GOVERNANCE_MODEL.md`;
4. `CLAUDE.md`;
5. `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`;
6. merged increment-specific authority, design, contract, review, and closure
   documents;
7. the explicit current owner authorization for the operation in hand, exercised
   only within all applicable higher-authority boundaries.

An ordinary operational authorization may authorize an action only within the
current active-anchor, `MVP_SCOPE_FREEZE.md`, roadmap-hold, and closed-state
boundaries.

Changing or overriding an active anchor, `MVP_SCOPE_FREEZE.md`, an active roadmap
hold, or a closed governance state requires a separately approved, controlled,
and committed amendment or governance action under the applicable higher
authority.

A working-tree draft, conversation, or uncommitted instruction never overrides
committed repository authority.

The owner authorization controls the exact permitted mutation and the stop
boundary for the operation; it does not by itself change any higher repository
authority. Where the owner intends to change an anchor or a freeze, that
intention MUST be executed through the separately governed amendment path, and
committed, before any downstream work relies on it. `CLAUDE.md`, this protocol,
and the roadmap do not override an active anchor or `MVP_SCOPE_FREEZE.md`.

Where any higher authority requires stricter verification, review, or reporting
than this protocol, the higher authority controls. This protocol never relaxes a
stricter explicit instruction and never invents product or implementation
authority. If a specific owner authorization mandates fuller verification,
review, or full-document reproduction, that authorization controls for that
operation.

## 3. Operation risk classes

Every operation is classified into exactly one of three risk classes BEFORE it
runs. When a single owner authorization bundles distinct actions, the highest
applicable class governs the whole operation.

### 3.1 LOW-RISK IDENTITY OPERATION

An operation that moves or verifies an already-reviewed, exact artifact without
changing repository content or authority. Examples:

- staging an already-reviewed exact path;
- committing an already-staged exact path;
- pushing an already-verified exact branch;
- creating a PR from an exact verified head/base;
- reading metadata;
- verifying refs, SHAs, blobs, status, or worktree separation;
- a metadata correction that does not alter repository content, base/head, or
  authority.

Required workflow:

```text
pre-operation identity verification
→ exact authorized operation
→ post-operation identity verification
→ targeted smoke test
→ stop
```

Rules:

- no independent semantic review is triggered merely because the identity
  operation occurred;
- repository content MUST NOT have changed (identity in == identity out);
- each lifecycle mutation remains separately owner-authorized;
- any scope mismatch or identity mismatch blocks immediately.

### 3.2 MEDIUM-RISK BOUNDED CONTENT OPERATION

An operation that changes bounded document content without touching anchor,
product scope, architecture, state model, tests-first authority, source
authority, or behavior. Examples:

- one bounded governance-document draft;
- a local wording correction;
- a cross-reference correction;
- a deterministic vocabulary clarification.

Required workflow:

```text
one complete review of the bounded scope
→ one consolidated material-finding set
→ one bounded correction batch
→ one focused closure review
→ lifecycle identity operations
```

Rules:

- findings are consolidated, not emitted one at a time (§8);
- no repeated full review after each individual correction;
- no full-document reproduction unless content completeness itself is disputed
  (§9);
- diff, SHA-256, line/byte identity, and changed sections are the primary
  evidence.

### 3.3 HIGH-RISK SEMANTIC OR AUTHORITY OPERATION

Any operation that changes meaning, authority, or product reality. Includes:

- anchor creation or amendment;
- product identity or scope change;
- architecture change;
- state-model change;
- tests-first authority or test-design decisions;
- source implementation;
- template or product-behavior change;
- persistence behavior;
- security-sensitive behavior;
- merge authorization for substantively changed content;
- reopening a closed increment or governance state.

Required workflow:

- full independent review;
- complete applicable authority reading;
- substantive findings;
- explicit owner decision;
- strict evidence and non-regression verification.

Efficiency MUST NEVER downgrade a high-risk operation to a lower class. When in
doubt about the class, treat the operation as the higher class.

## 4. Finding-severity policy

### BLOCKER
Always blocks the current lifecycle transition. Use only when safe or valid
completion is impossible, required authority is missing, or the operation cannot
lawfully proceed.

### MAJOR
Always blocks. Use for a material contradiction, scope breach, product or
architecture error, incorrect authority, nondeterministic core behavior,
substantive non-regression risk, or an implementation-invalid contract.

### MINOR
Blocks ONLY when it leaves any of the following unresolved:

- implementation behavior;
- a test expectation;
- authority;
- deterministic identity or ordering;
- security;
- authorized scope;
- user-visible truthfulness;
- required evidence integrity.

A purely stylistic, editorial, optional-tightening, or future-improvement MINOR
does not block the current lifecycle transition.

### OBSERVATION
Never blocks the current operation. Use for an optional improvement, a future
enhancement, a stylistic preference, a platform limitation, a harmless
normalization, or informational context.

The reviewer MUST NOT relabel a material defect as a MINOR or OBSERVATION to
avoid a gate, and MUST NOT inflate a stylistic preference into a MAJOR/BLOCKER to
force one.

## 5. Closed-finding finality

```text
A finding recorded as closed, resolved, or accepted may not be reopened unless
new repository evidence directly contradicts the recorded closure or a higher
authority has changed.
```

A new wording preference, an alternative design, or a stricter personal
preference is NOT new contradictory evidence. To reopen a closed finding, the
reviewer MUST identify:

- the exact new evidence;
- the earlier closure being reopened;
- the direct contradiction between them;
- why reopening is necessary now.

## 6. Consolidated-review rule

For a bounded content review:

- inspect the complete authorized scope before issuing the final finding set;
- return all material findings together in one set;
- do not intentionally defer known findings to a later turn;
- do not invent a finding quota;
- do not present stylistic or optional findings as blockers;
- one correction batch should close all accepted material findings;
- one focused closure review follows the batch.

A later, additional finding is legitimate ONLY when it depends on the correction
itself, or when the evidence for it was genuinely unavailable earlier.

## 7. Evidence-first reporting economy

The default operation report uses repository evidence, not hand-copied content:

- exact path list;
- branch and full SHAs;
- file line count, byte count, and SHA-256;
- exact diff or changed-section excerpts;
- test / smoke-test output;
- staged / committed / remote blob identity;
- ahead / behind counts;
- protected-worktree state.

Do NOT return an entire long document when all three hold: its repository/blob
identity is already verified; only bounded sections changed; and content
completeness is not in dispute.

Complete reproduction IS required when: the owner explicitly requests it; the
artifact cannot otherwise be accessed; reporting completeness is itself disputed;
or the review genuinely requires whole-content delivery rather than repository
evidence. Repository evidence (SHA-256, blob identity, diff) is authoritative
over any hand-copied conversation rendering; where they disagree, the repository
evidence governs.

## 8. Repository identity versus platform metadata

### 8.1 Repository artifacts — strict byte identity
Strict byte identity applies to committed files, staged blobs, commits, trees,
test fixtures, and any generated repository artifact where identity is required.
These are never normalized away.

### 8.2 Harmless platform normalization — does not block
When meaning and the requested metadata are unchanged, the following do not block
and are disclosed when relevant:

- an HTML-entity representation that renders to the intended literal character;
- terminal-newline normalization;
- JSON escaping in tool output;
- field-order differences in API responses.

### 8.3 Substantive platform mutation — not harmless
The following are substantive and MUST be corrected or explicitly blocked, never
accepted as harmless merely because they are visually separated:

- appended attribution or generated-by trailers;
- added disclaimers;
- removed content;
- reordered normative sections;
- a changed base, head, or title;
- added reviewers, labels, auto-merge, or other unauthorized metadata.

## 9. Owner-gating preservation

This protocol explicitly prohibits using efficiency to:

- combine stage, commit, push, PR creation, review, and merge into one mutation
  without explicit owner authorization for each step;
- begin tests-first work merely because a contract was merged;
- begin source work merely because tests exist;
- bypass an active hold;
- change an anchor indirectly;
- treat CI or smoke-test success as product or merge authority;
- modify a protected, paused worktree.

Efficiency reduces repeated verification, not owner control. The one-authorization
-per-turn discipline is preserved in full for every operation except the single
narrow, conditional case defined in §9.1: this protocol changes only how a single
authorized operation is verified and reported, and — outside §9.1 — never how many
operations one authorization permits.

### 9.1 Conditional reversible LOW-RISK lifecycle sequence

This subsection narrows — and ONLY narrows — the one-authorization-per-turn
statement above, and only for reversible LOW-RISK identity lifecycle actions
(§3.1). It creates no delegated, standing, or blanket authority.

A single explicit owner authorization MAY conditionally cover, within one turn,
this bounded sequence of reversible LOW-RISK identity lifecycle actions on one
already-reviewed exact artifact:

```text
precondition verification
→ exact-path staging
→ commit
→ normal non-force push
→ PR creation
```

This conditional fast path is available ONLY when ALL of the following are true.
If any is not, the fast path is unavailable and every step reverts to its own
separate owner authorization:

1. the exact artifact has already passed the required independent review;
2. the authorized changed-path set is fixed and explicit;
3. the expected base and head identities are known in advance;
4. the relevant focused and regression tests have passed at the accepted baseline;
5. no Source correction remains open;
6. no scope expansion is required;
7. no persistence, migration, authentication, security, privacy, destructive, or
   history-rewriting operation is involved;
8. the operation is fully reversible before merge;
9. every step has explicit stop conditions;
10. any deviation stops the sequence before any further mutation.

This is a conditional bounded sequence, NOT unlimited or delegated authority. It
permits exactly the five listed reversible pre-merge Git actions on the one
authorized artifact and nothing else. It confers no authority to run a second
artifact's sequence, to repeat after a stop, or to proceed past any unmet
precondition.

The following remain SEPARATELY owner-gated and are never part of the fast path:

- true merge (always a separate owner authorization; automatic merge is never
  permitted);
- any HIGH-RISK operation (§3.3);
- any semantic or authority change;
- any destructive or irreversible action;
- persistence or migration work;
- force push, reset, rebase, history rewrite, branch deletion, or data deletion;
- any action taken after an unexpected test result, a changed path, a changed
  SHA, or any scope difference — such a difference STOPS the sequence before any
  further mutation and returns control to the owner.

Reversibility distinction (governing this subsection):

- REVERSIBLE PRE-MERGE GIT LIFECYCLE ACTIONS — staging, commit on a
  non-authoritative lifecycle branch, normal non-force push of that branch, and
  PR creation — do not alter the authoritative integration branch, are undoable
  before merge (the branch or PR may be closed or replaced without rewriting
  shared history), and change no product reality. These are the ONLY actions the
  fast path may cover.
- IRREVERSIBLE OR AUTHORITY-CHANGING ACTIONS — true merge, force push, reset,
  rebase, history rewrite, branch or data deletion, persistence or migration, and
  any semantic, scope, anchor, or authority change — alter shared or product
  reality and ALWAYS require their own explicit owner authorization.

All existing controls are preserved and NOT weakened by this subsection:
mandatory risk classification before the operation (§3); repository evidence over
chat (§7); closed-finding finality (§5); independent review wherever the risk
class requires it (§3); exact-path staging; test-baseline verification; true-merge
verification and owner control over merge; the persistence pause; the
stop-on-difference rule; and the prohibition on silent scope expansion. Efficiency
still reduces repeated verification and routine round-trips, never owner control
over irreversible or authority-changing actions.

## 10. Reporting and stop behavior

Each operation report should contain only:

1. starting identity;
2. the operation performed;
3. the material result;
4. automated verification;
5. findings that affect the gate;
6. the disposition;
7. stop confirmation.

Avoid: repeating the full authorization text; repeating already-closed historical
narratives; commenting on a platform stop-hook unless it reveals a real material
difference; and suggesting a next operation when the authorization says not to.

## 11. Prospective application

- This protocol applies prospectively only, after it is merged and explicitly
  adopted by the owner.
- It does not retroactively change any recorded historical disposition.
- It does not invalidate existing closed evidence.
- An open operation may rely on it only after merge and explicit owner adoption.
- The drafting operation that creates this document modifies no other artifact;
  in particular, PR #51 is not modified by drafting this protocol.

## 12. Non-authority boundary

This protocol authorizes NONE of the following: tests; source; templates; product
behavior; architecture; state-model changes; anchor changes; roadmap changes;
merges; or any repository lifecycle mutation by itself. It defines only how an
already-authorized operation is efficiently verified and reported. Adopting or
merging this protocol confers no execution authority and starts no downstream
work; each later action remains a separate, explicit, owner-gated operation.
