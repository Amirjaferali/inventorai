# InventorAI — Lean Governance and Agent Continuity Protocol

**Type:** Documentation-only governance protocol (candidate).
**Status on adoption:** BINDING on all future agents through the CLAUDE.md boot sequence.
**Authority level:** Operational protocol. **Subordinate to** all Level-0 authorities,
product identity, security/privacy boundaries, phase sequencing, active holds, and
separate-authorization requirements. It weakens none of them.
**Resolve current authority from:** `CLAUDE.md` → `docs/governance/CURRENT_PROJECT_STATE.md`
→ the current authoritative anchor → `docs/governance/OWNER_DECISION_REGISTER.md`
→ the active phase/increment contract → only the further documents the active contract cites.

---

## 0. Operating principle

```
History is evidence, not daily workload.
Current authority guides daily work.
Owner decisions are recorded once.
Agents execute bounded increments.
Independent review verifies outcomes.
The owner intervenes at major gates only.
```

This is an enforceable protocol, not an aspiration. Full historical audits are an
exception (§6), not the daily default.

## 1. Agent boot sequence (mandatory)

Before planning or implementation, every agent reads, in order:

1. `CLAUDE.md`;
2. `docs/governance/CURRENT_PROJECT_STATE.md`;
3. the current authoritative anchor (per CLAUDE.md);
4. `docs/governance/OWNER_DECISION_REGISTER.md`;
5. the active phase/increment contract;
6. only the additional documents the active contract references.

The agent then verifies the live authoritative tip from Git (never a prose-pinned SHA).
Reading beyond this set is required only when a §6 full-audit trigger is present or the
active contract cites more.

## 2. Authority hierarchy (unchanged)

1. Level-0 freeze/state records (`docs/governance/INVENTORAI_PROJECT_STATE_FREEZE_v1.2.md`,
   `MVP_SCOPE_FREEZE.md`) and the governing anchors.
2. `CLAUDE.md`.
3. The canonical plan (`docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md`)
   and the append-only `ACTIVE_EXECUTION_ROADMAP.md`.
4. Accepted owner-decision evidence (indexed by the Owner Decision Register).
5. The active increment contract.

Committed current authority always overrides handovers, chat memory, and prior reports.

## 3. Change-risk levels

- **LEVEL 1 — HIGH-RISK / STRATEGIC.** Separate explicit owner authorization **and**
  independent review required. Includes: product identity; architecture; database;
  authentication; authorization; privacy/security model; billing/subscription; domain
  activation; ACV implementation; Structured Technical Guidance; release/deployment;
  main reconciliation.
- **LEVEL 2 — AUTHORIZED PHASE INCREMENT.** May proceed inside an owner-approved contract
  without repeated per-file approval. Examples (only when in the approved contract):
  screen redesign; navigation; Arabic/RTL; accessibility; output UX; sponsor presentation;
  administrative-notice UX; privacy/trust presentation.
- **LEVEL 3 — LOW-RISK MAINTENANCE.** May proceed and be reported in the active increment
  when it changes no product meaning, no engine behavior, no data lifecycle, no
  authorization, crosses no protected path, and is covered by the active contract.
  Examples: copy corrections; labels; minor CSS; empty/error states; dead-code removal;
  non-behavioral cleanup.

## 4. Review depth (proportionate)

- **DEPTH 1 — new phase / high-risk strategic change:** boot sequence + current anchors +
  roadmap status + relevant owner decisions + phase plan + relevant architecture/freeze
  documents + independent review + explicit owner authorization.
- **DEPTH 2 — authorized phase increment:** boot sequence + active contract + only the
  relevant decisions/documents + bounded implementation + required tests + bounded
  independent review. No full historical audit unless a §6 trigger appears.
- **DEPTH 3 — low-risk maintenance inside a contract:** implementation → targeted
  verification → inclusion in the increment report. No separate per-file owner
  authorization.

## 5. Independent-review policy (proportionate)

Independent review stays mandatory where required; its scope is proportionate. For a
bounded increment the reviewer answers only: did the implementation match the active
contract; did any forbidden path change; did required tests pass; was scope expanded;
were owner decisions respected; were current limitations preserved honestly; did the
increment activate a later phase or a separate-authorization capability. The reviewer
does not repeat the full historical audit unless a §6 trigger is present.

**Formal review independence (mandatory where independent review is required).** Proportionate
scope never weakens independence. A formal independent review must be performed in a genuinely
separate review session that did not author or modify the candidate. A subagent, child agent, or
agent function operating inside the implementation or authoring session does **not** qualify as a
formally independent reviewer, and an agent identifier alone is **not** sufficient evidence of
separate-session independence. The reviewer must record: its separate session (or equivalent
verifiable review) identity; a declaration that it did not author or modify the candidate; the
exact candidate SHA; the parent SHA; the tree where applicable; the verified changed paths; and
the evidence source or transfer artifact it independently inspected. When a bundle or transferred
candidate is used, the review must verify the artifact's identity rather than rely on the filename
alone — checking the applicable file size, SHA-256, `git bundle list-heads`, candidate SHA, parent
SHA, tree, and changed paths. A review that cannot satisfy these conditions is recorded as
technical verification only, with formal independent review `NOT YET SATISFIED`.

## 5A. Mandatory Pre-Delivery Adversarial Self-Review

Before DELIVERING any material gated deliverable, the authoring or reporting session
MUST perform an adversarial review of its own output and record the result. This
self-review is a precondition of delivery; it authorizes nothing and does not replace
owner authorization or independent review.

Material gated deliverables include: plans and owner-decision packages; proposed
increment/gate contracts; implementation candidates; completion-evidence packages;
independent-review reports; publication and merge-verification reports; and closure or
governance-synchronization proposals. Trivial conversational replies do not require the
formal block below.

The self-review examines, WHERE RELEVANT: (1) authoritative evidence vs unsupported
inference; (2) mandatory requirement vs preferred best practice; (3) scope vs
exclusions; (4) permitted paths vs required implementation paths; (5) the current gate
vs later or separately authorized gates; (6) RED criteria vs actual pre-change
behavior; (7) GREEN criteria vs achievable authorized behavior; (8) source checks vs
runtime/behavioral evidence; (9) false-green and false-positive tests; (10) fallback,
bypass, logging, persistence, security, and privacy; (11) temporary-session
truthfulness; (12) accessibility, RTL/LTR, and responsive claims; (13) minimum
necessary files, changes, and process; (14) prior accepted observations and lessons
learned; (15) Lean proportionality; (16) unresolved ambiguity and missing evidence.

**Mandatory behavior.** Every avoidable blocking defect found MUST be corrected before
delivery. If correction requires unauthorized scope, the agent MUST STOP and report
instead of expanding scope. If any material ambiguity or unresolved blocker remains, the
package MUST NOT be presented as ready for owner authorization. The agent MUST NOT
fabricate certainty or fill an evidence gap with preference. Non-blocking observations
MUST be disclosed, not silently hidden. When the same avoidable defect class recurs
across deliverables, a lessons-learned note is recorded at the next authorized
governance-maintenance opportunity (see §11).

**Author vs reviewer scope.** For an authoring/implementation session, the self-review
targets defects in its own proposed plan, contract, candidate, or evidence package, and
corrects every avoidable defect within authorization. For an independent-review session,
the self-review targets defects in its own review reasoning and report; the independent
reviewer MUST NOT modify the candidate merely to satisfy this requirement. In an
independent-review report, the block fields **BLOCKING DEFECTS FOUND AND CORRECTED** and
**REMAINING BLOCKING DEFECTS** refer to defects in the review report/reasoning unless the
report explicitly labels candidate findings separately; candidate findings remain
separately classified as `BLOCKING` / `NON-BLOCKING` / `OBSERVATION` / `NO FINDING`.

**Self-review is not independence.** 

    SELF-REVIEW:
    MANDATORY
    NOT INDEPENDENT

    INDEPENDENT REVIEW:
    SEPARATELY REQUIRED WHEN THE GOVERNANCE GATE REQUIRES IT

Self-review MUST NEVER be cited as satisfying the §5 independence requirement, and a
same-session subagent does not become independent merely by performing a review.

**Proportionality.** The self-review is concise for small bounded material deliverables
and deeper for security, governance, architecture, persistence, identity, or broad UX
work. By default it performs no full repository re-audit, does not repeat already-proved
evidence unless identity, base, scope, or content changed, corrects within authorization
where possible, stops and reports when correction exceeds authorization, and never
requires a separate repository gate merely to store a self-review result.

**Required output block.** Every material gated deliverable MUST end with this exact
minimum block, reporting the ACTUAL result — it MUST NEVER be filled with predetermined
successful values:

    PRE-DELIVERY ADVERSARIAL SELF-REVIEW:
    COMPLETED

    BLOCKING DEFECTS FOUND AND CORRECTED:
    [COUNT]

    REMAINING BLOCKING DEFECTS:
    [COUNT]

    KNOWN NON-BLOCKING OBSERVATIONS:
    [LIST OR NONE]

    UNRESOLVED EVIDENCE GAPS:
    [LIST OR NONE]

    UNAUTHORIZED SCOPE REQUIRED TO CORRECT ANY REMAINING ISSUE:
    [YES/NO]

    READY FOR OWNER OR INDEPENDENT REVIEW:
    [YES/NO]

Binding consistency rules for the block:

- If `REMAINING BLOCKING DEFECTS` is greater than 0, `READY FOR OWNER OR INDEPENDENT
  REVIEW` MUST be `NO`.
- If a material unresolved evidence gap prevents a reliable decision, `READY FOR OWNER OR
  INDEPENDENT REVIEW` MUST be `NO`.
- If correcting a remaining issue requires unauthorized scope, `UNAUTHORIZED SCOPE
  REQUIRED TO CORRECT ANY REMAINING ISSUE` MUST be `YES`, and the agent MUST stop.
- `READY` may be `YES` only when no unresolved blocker or material ambiguity remains.

When the package is not ready, the last two fields MUST honestly reflect that and the
agent MUST stop rather than deliver it as ready.

## 6. Full-historical-audit triggers (exceptions only)

A full historical review is required only when one or more applies: current authority
cannot be resolved; a material contradiction appears between governing records; product
identity is being changed; architecture is being materially changed; repository state
materially conflicts with committed status; a long-unattended project lacks a reliable
current-state record; the owner explicitly requests a historical audit; an implementation
claim materially exceeds available evidence. Otherwise agents use current authority and
the active contract.

## 7. Owner-interruption policy

Agents must not request approval for every file, command, text change, or minor action.
The owner is asked when: a required product decision is unresolved; evidence materially
conflicts; the change crosses the active contract; a Level-1 change is required; a
separate-authorization capability is implicated; an increment reaches owner-acceptance
status; or merge / phase progression requires owner authority. Within a valid approved
contract the agent completes the bounded work and returns one concise evidence report.

## 8. Phase / increment contracts

Bounded work runs under an active contract (see
`docs/governance/ACTIVE_INCREMENT_CONTRACT.md`, which holds the reusable template and the
declaration rule). A contract states: objective; owner authorization; allowed paths;
forbidden paths; expected behavior; non-goals; acceptance criteria; required tests; tests
not required; dependencies; unresolved decisions; stop conditions; independent-review
scope; merge authority. Where the active contract is declared is fixed by that document so
future agents can always discover it.

## 9. Handover rules

Handovers are informative, never authoritative. Every agent must be able to continue from
the five core inputs (§1.1–1.5). A handover conflicting with committed current authority
loses. A handover-only idea must be marked `NOT CANONICAL — REQUIRES OWNER DECISION` and
routed to the Owner Decision Register with committed owner-decision evidence — never
silently implemented. Use `docs/governance/HANDOVER_TEMPLATE.md`.

## 10. Contradiction escalation and stop conditions

Stop and escalate to the owner when: current authority cannot be resolved; governing
records materially contradict; the requested work crosses the active contract or a
Level-1 boundary; or a separate-authorization capability would be touched. Do not resolve
a material contradiction by editing history — report it and request canonicalization.

## 11. Update responsibilities

- The Owner Decision Register is updated (append/supersede row) whenever an owner decision
  is accepted and committed.
- `CURRENT_PROJECT_STATE.md` is refreshed at each phase/increment boundary and kept
  concise — it points to the roadmap/evidence for detail and must not become a second
  roadmap.
- The active-contract declaration is updated when a new increment is authorized.
- The append-only roadmap receives one record per governed gate.
- When the same avoidable defect class recurs across deliverables (per §5A), a
  lessons-learned note is appended at the next authorized governance-maintenance
  opportunity.

## 12. Scope and non-weakening guarantee

This protocol changes no product behavior, no engine, no schema, no runtime, and no phase
status. It activates no phase. Phase 3 remains NOT authorized for implementation.
Structured Technical Guidance remains RESERVED / INACTIVE / separately authorized. Domain
expansion, ACV/Download/Email implementation, main reconciliation, and deployment remain
NOT authorized. It becomes binding only through independent review, owner acceptance,
normal merge, and post-merge verification.
