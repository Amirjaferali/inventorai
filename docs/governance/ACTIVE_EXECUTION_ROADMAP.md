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
| Latest relevant execution baseline | `2a33763` — E-2 safe retry implementation closure record (Gate B complete) |
| E-2 execution-attempt baseline | `feaff2a` — governance: amend E-2 server start command with repository PYTHONPATH |
| Phase 1 Path N designation | CLOSED |
| Phase 2 Path N content selection | CLOSED (implementation `165e0da`, gate amendment `71e90b3`, closure `ffaab93`) |
| Post-Phase-2 Authorization Review | COMMITTED (`7a3350c`) — review only, authorizes nothing |
| Limited Evidence Authorization | COMMITTED (`db2c46e`) |
| E-3 integration plan recovery | COMPLETE — artifact committed at `cfcc95f` |
| E-1 gate re-run | COMPLETE — results match authorized baseline; artifact committed at `cfcc95f` |
| E-2 operational procedure | COMMITTED (`f1a02a1`) |
| E-2 smoke session execution | STOP DECLARED — E-2 NOT ACCEPTED; session `830054a4` invalid; retry NOT AUTHORIZED |
| E-2 STOP incident record | COMMITTED (`a684aba`) |
| E-2 Safe Retry Gate A | COMMITTED (`1cb08cb`) — design only |
| E-2 Safe Retry Gate B | COMMITTED (`d8277f9`) — implementation only |
| Safe-retry design | AUTHORIZED |
| Safe-retry implementation | AUTHORIZED |
| Matcher implementation | COMMITTED AND PUSHED (`654ce07`) |
| Runner implementation | COMMITTED AND PUSHED (content `d12db64`; executable-mode correction `d631439`) |
| Gate B closure | CLOSED (`2a33763`) |
| E-2 retry execution | NOT AUTHORIZED |
| E-2 STOP | DECLARED AND RECORDED |
| Path N runtime integration | NOT FULLY CLOSED |
| `runtime_integrated` | `false` |
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
| `b3a5fba` | Phase 2 Path N content selection authorization |
| `71e90b3` | Phase 2 Gate Amendment 1 — adds `tests/test_phase1_path_designation.py` (one test) to authorized files; corrects §10 gate meaning |
| `165e0da` | Phase 2 Path N content selection implementation — approved Path N artifact consumed by `state.path == "N"`; gates passed before commit |
| `ffaab93` | Phase 2 Path N content selection implementation closure record |
| `7a3350c` | Post-Phase-2 Authorization Review — review only, authorizes nothing |
| `db2c46e` | Limited Evidence Authorization — E-1/E-3 execution authorized after roadmap refresh; E-2 objective authorized but execution blocked pending `E2_OPERATIONAL_PROCEDURE.md` |
| `cfcc95f` | E-3 integration plan recovery and E-1 gate re-run evidence — both accepted; E-2 still blocked |
| `f1a02a1` | E-2 operational procedure — committed; execution not yet started |
| `a684aba` | E-2 STOP incident record and byte-preserved failed-attempt artifacts — session `830054a4` |
| `1cb08cb` | E-2 Safe Retry Design Authorization — Gate A, design only |
| `d8277f9` | E-2 Safe Retry Implementation Authorization — Gate B, implementation only |
| `654ce07` | B-1 standalone exact matcher (`scripts/e2_exact_matcher.py`) and nine behavioral tests (`tests/test_e2_exact_matcher.py`) — gates passed before commit |
| `d12db64` | B-2 E-2 Path N smoke runner (`scripts/e2_path_n_smoke_runner.sh`) and five isolated preflight tests (`tests/test_e2_runner_preflight.py`) — B-2 gates passed before commit |
| `d631439` | B-2 runner executable-mode correction (100644 → 100755), required for direct `--preflight` invocation |
| `2a33763` | E-2 safe retry implementation closure record; Gate B implementation closed after V-1 through V-9 passed |

(Product-intent anchor `DUAL_PATH_PRODUCT_ANCHOR.md` at `60c809b`
is deliberately NOT in this table: it is a product-intent anchor,
not a Path N implementation step.)

## 6. Current execution lane

PATH N RUNTIME INTEGRATION — E-2 STOP remains declared.

Safe Retry Gate A was committed at `1cb08cb`.
Safe Retry Gate B was committed at `d8277f9`.

B-1 matcher implementation: COMPLETE (`654ce07`).
B-2 runner implementation: COMPLETE (content `d12db64`; executable-mode correction `d631439`).
B-3 Gate B closure record: COMMITTED (`2a33763`).
Gate B implementation: CLOSED.

This closes implementation readiness only.

No live E-2 retry has been executed.
E-2 retry remains NOT AUTHORIZED.
E-2 STOP remains declared.
All holds remain unchanged.

E-2 retry execution remains NOT AUTHORIZED.
No Flask startup, SID creation, or live retry session is authorized.

`runtime_integrated` remains `false`.
R2 HELD, FORM T BLOCKED, S-6 UNCLASSIFIED, AA-5 BLOCKED.

## 7. Next authorized step (exactly one)

1. Conduct the post-Gate-B authorization review to determine whether
   a separate Gate C authorization may be prepared.

   No Gate C implementation or live retry execution is authorized by
   this roadmap synchronization.

Constraints:

- No normal runner execution.
- No Flask startup.
- No SID creation.
- No live GET or POST session activity.
- No E-2 retry.
- No change to `runtime_integrated`.
- No release of R2.
- No FORM T movement.
- No S-6 classification.
- No AA-5 movement.
- No Gate C document unless separately authorized after review.

## 8. Required future sequence

1. ~~Commit `DUAL_PATH_PRODUCT_ANCHOR.md`~~ — DONE (`60c809b`)
2. ~~Commit `ACTIVE_EXECUTION_ROADMAP.md`~~ — DONE (`1982e2b`)
3. ~~Draft Phase 2 Authorization~~ — DONE
4. ~~Commit Phase 2 Authorization~~ — DONE (`b3a5fba`)
5. Explicit owner instruction to implement Phase 2 only
6. Run required test gates (authorization §10) and review diff
7. Commit Phase 2 implementation only if gates green and diff
   confined to the four authorized files
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
  and even inside the zone only under the committed Phase 2
  authorization plus the explicit implementation instruction
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
5. `docs/governance/PHASE_2_PATH_N_CONTENT_SELECTION_AUTHORIZATION.md` (`b3a5fba`, the phase authorization inforce)

If these are not read, the agent must not proceed.

## 11. Roadmap update rule and baseline semantics

Baseline semantics:
- §4's baseline is the latest relevant execution-event commit
  reflected in this roadmap. Roadmap-only commits (including this
  update's own commit) do NOT make the roadmap stale.
- Agents flag staleness only when phase/state-change events (below)
  have occurred AFTER the roadmap's last update — not because the
  roadmap's own commit advanced HEAD.

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
