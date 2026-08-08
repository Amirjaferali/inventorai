# §5-I3 — Subsystem + Cross-Domain Project Model Foundation — Formal Closure Record

Status: **FORMALLY ACCEPTED AND CLOSED** (owner decision, gate
`G-S5-I3-SUBSYSTEM-CROSS-DOMAIN-MODEL-FORMAL-CLOSURE-01`) — **authoritative only
if/when this governance closure candidate is itself merged** (temporal note §9).

Classification: documentation-only formal-closure record. It records committed
repository reality; it creates no new authority and authorizes no downstream work.
It makes no runtime/code/test/dependency/schema change, activates no domain, starts
no successor increment, and does not imply that Product-Foundation §5 as a whole is
complete. Only **§5-I3** is closed.

Repository truth overrides conversation, handover, memory, inference, and proposal.

Authoritative integration branch: `feature/atomic-json-session-persistence`
Authoritative integration tip at closure basis: `dac5696ebcf9c9814b2adb66887a535e089a6c85`
(PR #398 merge; parents `04a9c4d` + `0a7f135`; merged tree `63a63e3`). `main` is out
of scope.

---

## 1. Identity and owner authorization

- **Gate:** §5-I3 — Subsystem / Cross-Domain Project Model Foundation — the third
  implementation increment of the accepted §5-C1 contract-of-record (decisions
  **D-S5-04**, **D-S5-05**), under the owner's continuing authorization to complete
  the remaining Product-Foundation §5 work through formal §5 closure.
- **Owner authorization:** EXPLICITLY AUTHORIZED (bounded implementation gate).

## 2. Accepted lineage and merge identity (independently re-verified)

| Item | SHA / value |
|---|---|
| Product base | `04a9c4d820a58a2036aa85bef817d58ced53f65a` (PR #397 — §5-I2 formal closure merge) |
| Implementation candidate | `0a7f1359426b95287932f26f5ef57c9d584a207b` (parent `04a9c4d`; tree `63a63e3b4268e1b2af831ea4af9e2240bcbba1d3`) |
| Publication branch | `publish/s5i3-subsystem-model` → `0a7f135` |
| PR | **#398** — "§5-I3 — Subsystem + cross-domain project model foundation" |
| Merge (PR #398) | `dac5696ebcf9c9814b2adb66887a535e089a6c85` (true merge commit; no squash/rebase/force-push) |
| Merge parents | `04a9c4d820a58a2036aa85bef817d58ced53f65a` + `0a7f1359426b95287932f26f5ef57c9d584a207b` |
| Merge tree | `63a63e3b4268e1b2af831ea4af9e2240bcbba1d3` |
| Delivered bundle SHA256 | `16be7b3b473915011380a3bcd0fa6f062107c9188c307a8cac9cec5a008a37c2` |

Full-chain diff **3 files changed / +246 / −0**; changed implementation paths:
`engine/idea_state.py`, `engine/subsystem_model.py`, `tests/test_s5_i3_subsystem_model.py`
only (**no** persistence, **no** web/UI, **no** domain-pack, **no** schema/migration,
**no** dependency/CI, **no** governance file in the implementation diff). Tracked
worktree CLEAN.

## 3. What §5-I3 delivered NOW (accepted result)

- The canonical `IdeaState` project model **extended additively** (D-FPC-MAP-06 — no
  second project model) with one **in-memory, persistence-independent** `subsystems`
  field (empty by default; absence preserves single-domain behavior).
- A minimum subsystem descriptor + operations (`engine/subsystem_model.py`): one
  project → zero or more subsystems → each may reference a canonical domain.
- **Subsystem-domain assignment** as **metadata only** — a reference never activates a
  domain and never changes the scalar root domain (`state.domain` /
  `confirmed_domain`).
- **Support-state integration** with the §5-I2 activation policy (recognized /
  recognized-not-activated / unknown); an unknown reference is never silently
  defaulted to electronics.
- **Root-domain / backward compatibility** preserved: no peer-root `domains = [...]`
  list (D-S5-04); the scalar stays scalar; the canonical Domain Registry remains the
  domain authority.

## 4. What §5-I3 did NOT deliver (future / not implemented)

- **Durable subsystem persistence** (foundation is in-memory only — OBS-1).
- **System-generated immutable/deterministic subsystem identity**, **display-name**
  semantics, and **subsystem-grain evidence/gaps/risks/validation** persistence or
  workflow (part of the D-S5-05 conceptual contract; NOT implemented now — OBS-2 /
  GAP-3).
- No new domain activation; no persistence/schema migration; no web/UI; no Phase-7
  API; no CAP-16; no §5-I4 implementation / Technology Capability Registry.

Governance must not claim these future semantics were implemented.

## 5. Independent review and test evidence

- **Independent §5-I3 implementation review:** **B — ACCEPT WITH NON-BLOCKING
  OBSERVATIONS**; BLOCKERS: NONE. Independently verified candidate `0a7f135`, parent
  `04a9c4d`, tree `63a63e3`, bundle SHA256 `16be7b3b…a37c2`; exactly 3 changed paths;
  **+246 / −0**; diff-check clean.
- **Implementation RED** (`pytest tests/test_s5_i3_subsystem_model.py` on base):
  `ImportError` — the intended new subsystem-model boundary did not exist; accepted as
  valid RED.
- Focused GREEN: **16 passed**. Model/domain regression: **153 passed**. Persistence
  regression: **55 passed**. Independent full-suite confirmation: **2025 passed / 1
  skipped / 1 xfailed / 0 failed**. Independent browser suites: **31 passed**.
- **Browser classification:** NO WEB SURFACE CHANGED / BROWSER NOT REQUIRED FOR THE
  IMPLEMENTATION GATE.

## 6. Retained non-blocking observations (NOT remediated by this closure)

- **OBS-1 — Durable subsystem persistence.** The foundation is intentionally in-memory
  only; durable subsystem persistence is a separately-governed schema/persistence
  increment. Durable subsystem persistence does **not** currently exist.
- **OBS-2 — D-S5-05 conceptual-contract delta.** Immutable/deterministic subsystem
  identity, display name, and subsystem-grain evidence/gaps/risks/validation are not
  yet implemented; not required to block §5-I3 acceptance; must be reconciled before
  §5-CLOSE (GAP-3).
- **OBS-3 — Duplicate subsystem identifiers.** The in-memory helper allows duplicate
  subsystem ids; no current lookup/persistence depends on uniqueness; identity
  semantics must be defined before subsystem ids become durable identity.
- **OBS-4 — Alias canonicalization before persistence.** Subsystem domain references
  may retain the supplied canonical id or alias in memory and resolve through the
  §5-I2 policy at query time; before any durable persistence, canonicalize-to-pack-id
  semantics must be explicitly decided (do not persist aliases blindly).
- **OBS-5 — Object mutability.** `project_subsystems()` returns a copied list
  container; `Subsystem` instances remain mutable — accepted for the in-memory model,
  not a blocker.
- **OBS-6 — Implementation-path reconciliation.** `engine/subsystem_model.py` was a
  valid bounded implementation path derived from live architecture though not literally
  enumerated in the earlier illustrative §5-C1 path list — accepted **minimum-path
  execution, not scope expansion**.
- **OBS-7 — Persistence-envelope hardening.** No current generic serializer persists
  `IdeaState.subsystems`; persistence uses explicit/fixed contracts; a future test
  pinning the durable project-envelope key-set is useful hardening but not required for
  §5-I3 closure.

## 7. §5-I4 evidence decision

**§5-I4 NECESSITY EVIDENCE: NONE.** No active v1.0 domain pack contains repeated
cross-domain capability references requiring stable central identity; the legacy
`iot_electronics` capability-shaped data is loader-skipped / evidence-only; no second
activated domain exists; no repeated capability reuse justifies a standalone Technology
Capability Registry. **§5-I4 — EVIDENCE GATE NOT MET.** Recommended disposition:
**SKIP IMPLEMENTATION AT CURRENT EVIDENCE STATE.** This is not a permanent prohibition:
**no §5-I4 implementation is required for current Product-Foundation §5 closure unless
new live evidence emerges before §5-CLOSE.** No Technology Capability Registry is
created; §5-I4 is not started.

## 8. Pre-§5-CLOSE governance obligations (retained for the later §5-CLOSE gate)

- **GAP-1 — §5-C1 pack provenance wording.** Reconcile the earlier embedded per-pack
  provenance-block wording (§5-C1 §8) with the accepted manifest-based validation
  behavior from §5-I1. (Already recorded as a pre-§5-CLOSE obligation.)
- **GAP-2 — D-S5-09 Phase-6 naming seam.** Resolve/document the stale Product-Foundation
  plan §11/§12 status and the relevant `docs/GOVERNANCE_DOCUMENTS.md` annotation before
  §5-CLOSE (no unrelated Phase-6 implementation).
- **GAP-3 — D-S5-05 conceptual-vs-delivered wording.** Make governance truthful about
  what §5-I3 delivered now (subsystem resource-model foundation; subsystem-domain
  assignment; support-state integration; root-domain compatibility) versus what remains
  future (durable subsystem identity; display-name semantics; subsystem-grain
  evidence/risk/validation persistence/workflow).
- **GAP-4 — Roadmap synchronization.** Reflect §5-I3 CLOSED; §5-I4 evidence-gate-not-met
  / skipped at current evidence; Product-Foundation §5 still OPEN; §5-CLOSE the next
  eligible governance gate under continuing owner authorization; Phase 7 NOT AUTHORIZED
  / NOT STARTED.

## 9. Temporal closure semantics

The **implementation** is already merged (PR #398, merge `dac5696`). This **formal
governance closure** becomes authoritative only if/when this closure candidate is
itself merged; until then it is a prepared closure record, not authoritative history.

## 10. Owner architectural decision preserved (Integration-Ready — NOT implemented here)

The owner established a durable architectural requirement recorded in
`OWNER_DECISION_REGISTER.md` (**D-INTEGRATION-READY-01**): InventorAI must be an
**integration-ready platform** — `InventorAI Core → Canonical Output Model →
Integration / Export Layer → External Tools` — without coupling the core to any one
vendor/tool; future connectors may use API / file export / webhook / CLI / MCP / direct
link / connector-adapter mechanisms (external tools such as Wokwi are examples only);
adding an integration must not require rewriting the reasoning engine, Domain Registry,
or canonical project model. **This is preserved as an owner architectural decision and
a future Phase-7 boundary requirement only.** No integration layer, API endpoint,
Wokwi-specific code, or Phase-7 work is implemented, authorized, or started by this
closure.

## 11. Closure status and next governance step

**§5-I3 — Subsystem + Cross-Domain Project Model Foundation: FORMALLY ACCEPTED AND
CLOSED** (**B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**; zero blockers), conditioned on
merge of this governance closure candidate. **Product-Foundation §5 as a whole is NOT
complete** — §5-C1 remains the contract of record; §5-I1, §5-I2, and §5-I3 are closed;
§5-I4 is EVIDENCE-GATE-NOT-MET / recommended SKIP.

**NEXT ELIGIBLE GATE: §5-CLOSE — Product-Foundation §5 formal closure + the bounded
governance reconciliation (GAP-1…GAP-4)** — under the owner's continuing §5
authorization, subject to successful §5-I3 closure merge and no new material evidence.
It remains **NOT STARTED**; no successor gate is automatically authorized by this
closure. **Phase 7: NOT AUTHORIZED / NOT STARTED.** Phase 4 & Phase 5 remain FORMALLY
CLOSED; the executed Phase-6 lane remains FORMALLY CLOSED; §5-I1 and §5-I2 remain
CLOSED; Decision D17 and the AISR seven-owner model are preserved.
