# ACTIVE EXECUTION ROADMAP
# Single source of execution continuity across agent changes

## 1. Purpose of this document

Any agent joining this project reads this roadmap to know the
current lane and next step WITHOUT reconstructing state from chat
history, memory, or assumption. Repository truth overrides any
conversation. This roadmap is execution control only — product
meaning lives in `DUAL_PATH_PRODUCT_ANCHOR.md` (`60c809b`);
epistemic rules live in `ILT-002_GOVERNANCE_ANCHOR.md`.

## 2. What the application is

InventorAI: a deterministic invention-progression platform.
The engine is the single source of truth; AI is advisory only and
never decides maturity, closes gaps, or issues PASS/WARN/BLOCK.
Three-stage journey (GD-001) frozen. WPS001 benchmark must remain
green.

## 3. What the product target is

A dual-path guided inventor journey — see
`DUAL_PATH_PRODUCT_ANCHOR.md` (commit `60c809b`): Path N serves
non-specialist inventors with approved non-specialist questioning;
Path T serves technical questioning contexts. The platform
preserves gaps and known-unknowns; it never falsely solves or
hides them.

## 4. Current official state

| Item | State |
|------|-------|
| Roadmap baseline HEAD before this document | `60c809b` — governance: correct dual path product anchor content |
| Phase 1 Path N designation | CLOSED |
| Path N runtime integration | NOT COMPLETE |
| `runtime_integrated` | `false` |
| Phase 2 | NOT AUTHORIZED |
| R2 | HELD |
| FORM T | BLOCKED |
| S-6 | UNCLASSIFIED |
| AA-5 | BLOCKED |

## 5. Completed chain (Path N lane only, commit order)

| Commit | Artifact |
|--------|----------|
| `e2e6234` / `effd040` | Path N question content specification + approval |
| `8ceb5d4` | Path N content config artifact (JSON) |
| `806a3c6` | Path N content config artifact tests (10 passed) |
| `26fa3e1` | Path N content config artifact approval record |
| `d2b2a9a` | Path N runtime integration authorization plan (corrected) |
| `2c0d2a5` | Phase 0 runtime discovery report |
| `2f6720d` | Phase 0 conditional STOP owner ruling (R-A…R-G ACCEPT) |
| `bd1019c` | Plan Amendment 1 (narrow question-selection plumbing zone) |
| `16e020e` | Phase 1 authorization (designation field + route) |
| `5084110` | Phase 1 implementation (`IdeaState.path`, `/start_ilt002_combination_lock_path_n`, tests) |
| `aa068fd` | Path N current execution anchor |
| `3c15c32` | Phase 1 implementation closure record |

(Product-intent anchor `DUAL_PATH_PRODUCT_ANCHOR.md` at `60c809b`
is deliberately NOT in this table: it is a product-intent anchor,
not a Path N implementation step.)

## 6. Current execution lane

PATH N RUNTIME INTEGRATION — between Phase 1 (closed) and Phase 2
(not yet authorized). The Amendment 1 plumbing zone exists but has
NOT been consumed. Path N-designated sessions still receive legacy
content.

## 7. Next authorized step (exactly one)

Draft Phase 2 Authorization — DRAFT ONLY
(`PHASE_2_PATH_N_CONTENT_SELECTION_AUTHORIZATION.md`).
Nothing else is next. No implementation precedes the committed
authorization plus a separate explicit implementation instruction.

## 8. Required future sequence

1. ~~Commit `DUAL_PATH_PRODUCT_ANCHOR.md`~~ — DONE (`60c809b`)
2. Commit `ACTIVE_EXECUTION_ROADMAP.md` (this document)
3. Draft Phase 2 Authorization only
4. Commit Phase 2 Authorization only after owner review
5. Implement Phase 2 only after separate explicit instruction
6. Run required test gates and review diff
7. Commit Phase 2 implementation only if gates green and diff confined
8. Create Phase 2 closure record
9. Only after runtime evidence: review whether R2 / FORM T / S-6
   can move — each requires its own authorization; nothing moves
   automatically

## 9. What is blocked and what must not be done

Blocked: R2 (HELD — D-B, `ccd1ecd` §6.1), FORM T, S-6
classification, AA-5, `runtime_integrated=true` (plan Phase 4
process only), conversion of the `72b5f11` strict xfail
(plan Phase 5 only).

Must not be done by any agent without explicit owner authorization:
- Modify `domains/electronics_electrical/domain.json` (Path T bank)
- Touch deterministic gates (`evaluate_transition()`,
  `assess_response()`, `integrate_response()`) or PASS/WARN/BLOCK
- Modify `engine/progression_loop.py` outside the Amendment 1 zone,
  and even inside the zone only under a committed phase authorization
- Mutate the Path N JSON artifact or its metadata
- Auto-label legacy sessions with any path
- Reconstruct global state, infer missing evidence, or treat
  absence of evidence as a negative fact
- Bundle multiple authorizations into one action

## 10. Mandatory reading before any analysis

1. `docs/governance/ILT-002_GOVERNANCE_ANCHOR.md` (epistemic boot — mandatory first)
2. `docs/governance/PATH_N_CURRENT_EXECUTION_ANCHOR.md` (`aa068fd`, execution state)
3. `docs/governance/DUAL_PATH_PRODUCT_ANCHOR.md` (`60c809b`, product intent)
4. This roadmap (current lane and next step)
5. The phase authorization in force, if any

If these are not read, the agent must not proceed.

## 11. Roadmap update rule and baseline semantics

Baseline semantics:
- §4's baseline HEAD is the commit BEFORE this roadmap's own
  creation commit. The roadmap creation commit itself does NOT make
  this roadmap stale: at creation, §4's baseline equals the
  creation commit's parent, and that is the correct, fresh state.
- Agents flag staleness only when phase/state-change events (below)
  have occurred AFTER the roadmap's last update — not because the
  roadmap's own commit (or other roadmap-only commits) advanced HEAD.

This roadmap MUST be updated (and the update committed) at every
one of these events, and is otherwise stale:
- A phase authorization is committed
- A phase implementation is committed
- A phase closure record is committed
- Any of R2 / FORM T / S-6 / AA-5 changes status
- `runtime_integrated` changes
- Any STOP is declared or resolved

Each update revises §4 (baseline and state), §5 (chain), §6 (lane),
and §7 (next step). Staleness check for agents: review repository
history since §4's baseline; if any event from the list above
appears and is not reflected here, trust git, flag the roadmap,
and request a roadmap update before proceeding.