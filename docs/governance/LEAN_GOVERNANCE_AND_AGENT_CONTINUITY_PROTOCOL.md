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

## 12. Scope and non-weakening guarantee

This protocol changes no product behavior, no engine, no schema, no runtime, and no phase
status. It activates no phase. Phase 3 remains NOT authorized for implementation.
Structured Technical Guidance remains RESERVED / INACTIVE / separately authorized. Domain
expansion, ACV/Download/Email implementation, main reconciliation, and deployment remain
NOT authorized. It becomes binding only through independent review, owner acceptance,
normal merge, and post-merge verification.
