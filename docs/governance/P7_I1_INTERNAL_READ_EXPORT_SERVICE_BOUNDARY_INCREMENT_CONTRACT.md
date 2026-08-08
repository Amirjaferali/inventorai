# P7-I1 — INTERNAL READ/EXPORT SERVICE BOUNDARY — BOUNDED INCREMENT CONTRACT

**Repository status of THIS document:** **CANONICAL P7-I1 CONTRACT PUBLICATION CANDIDATE** —
**PENDING independent pre-merge review, Owner acceptance, merge, and post-merge verification.**
It is **NOT** finally established for implementation. Under the Owner's **Standing Phase-7
Authorization** (`D-P7-STANDING-01`), P7-I1 implementation **MUST NOT begin** until the required
pre-merge review sequence and post-merge verification are complete (Permanent Execution-Gate Safety
Lock).

- **Standing Phase-7 Authorization:** GRANTED (`D-P7-STANDING-01`).
- **Canonical P7-I1 bounded contract:** DEFINED by this candidate — authoritative if/when this exact
  candidate is independently reviewed, Owner-accepted, merged, and post-merge verified.
- **P7-I1 implementation:** NOT STARTED. **Implementation Gate Lock: ACTIVE.**
- **Independent pre-merge review:** REQUIRED against this exact candidate SHA/tree/bundle before merge.
- **P7-I2:** NOT STARTED.
- **Authoritative basis tip:** `653f66a86744e9b66bbb4817599e1e9e6339db10`
  (`feature/atomic-json-session-persistence`; P7-C merge PR #401; parents `f82b18b` + `9800dee`;
  tree `59d7716`).
- **Governing contract-of-record:** `docs/governance/PHASE_7_API_AND_INTEGRATION_FOUNDATION_P7C_CONTRACT.md`
  (P7-C §8 first slice). This contract does not reopen P7-B or P7-C and introduces no new architecture.

## Source custody

This candidate is composed from the actual verbatim owner-provided materials plus the independent
review findings, with only the minimum corrections applied:

- **Source A (verbatim):** *P7-I1 — INTERNAL READ/EXPORT SERVICE BOUNDARY — INCREMENT CONTRACT PACKAGE*
  (original bounded contract) — owner-side reviewed.
- **Source B (verbatim):** *P7-I1 CONTRACT CORRECTION ADDENDUM* (Corrections 1–4) — owner-side reviewed.
- **Source C:** *Independent Pre-Implementation Review* — findings **IR-1…IR-6** (below).

Where IR-1…IR-6 supersede Source A/B wording, the superseded wording is **removed** (no conflicting
old + corrected rules are kept side by side). All unaffected Source A/B substance is preserved.

## Independent-review corrections integrated (IR-1…IR-6)

- **IR-1 (BLOCKING).** The P7-I1 read/export use cases **must not instantiate or initialize their own
  datastore** as part of the operation; they **consume an already-established store/dependency from the
  existing composition root / caller**. P7-I1 non-mutation applies to the **P7-I1 service operation
  itself**; the existing datastore initialization/migration lifecycle (which may run schema DDL /
  additive migrations / `BEGIN IMMEDIATE` in `SqliteRecordStore.__init__`) remains **outside** P7-I1 and
  is **not modified**. If implementation later proves datastore initialization is unavoidable inside the
  seam → **STOP and return to contract review**.
- **IR-2 (NON-BLOCKING OBSERVATION + IMPLEMENTATION GUARD).** Do **not** rely on
  `ProjectRecordContract.from_state(live_state)` as the boundary-construction mechanism where it can
  expose shared mutable `AssertionRecord` references; **prefer the durable validated load path**
  (`store.load_contract(project_id)`). If `from_state` over live mutable state ever appears required →
  **STOP and assess copy/mutability semantics separately**. `ProjectRecordContract` is **not modified**.
- **IR-3 (BLOCKING).** `SqliteRecordStore.load_owner` is **ALREADY OWNED — CONSUME**: it is already a
  Flask-free durable ownership-fact source. P7-I1 therefore **does not** extract authorization logic from
  `web/app.py` and **does not** build a new authorization framework; it **consumes `load_owner` plus an
  explicit caller-supplied identity**.
- **IR-4 (BLOCKING).** **Default: DO NOT MODIFY `web/app.py` in P7-I1.** Current web legacy behavior
  remains unchanged; no web-route migration. Code deduplication alone is **not** sufficient justification.
  If later implementation evidence proves a `web/app.py` change is strictly necessary for P7-I1
  correctness → **STOP and return to contract review BEFORE making that change**. *(This supersedes the
  Source-A/Source-B proposal to extract/delegate `_project_authorized` and its single-web-edit permitted
  path.)*
- **IR-5 (BLOCKING).** NULL-owner semantics are explicit: current web legacy/anonymous behavior
  (including NULL-owner / `SESSION_STORE` cases) remains **unchanged in the web layer**; the **new
  internal durable read/export service does not treat `owner = NULL` as automatic authorization** —
  authorization must be **explicit and fail-closed** unless canonical authorization is established for
  that durable project. This is a deliberate **surface-policy distinction**, not accidental duplication.
  **P7-I2 does not inherit anonymous/legacy access automatically.** No governance mandates new-service
  access to NULL-owner durable projects; if any is later cited, quote the exact evidence or **STOP**.
- **IR-6 (BLOCKING).** P7-I1 preserves the **semantic distinction** between Project Read Representation
  and Structured Export, but **does not freeze a new independent public/export contract version
  identifier inside P7-I1** unless live evidence proves an internal version is strictly required now.
  P7-I1 establishes **deterministic structured-export composition behavior**; **public/export contract
  version identity remains a P7-I2 concern by default.** Structured Export is **not** collapsed into
  `ProjectRecordContract` JSON, and **no final public JSON field names are frozen.** *(Where Source B
  required Structured Export to carry an independent export version identity, IR-6 supersedes that
  specific requirement; all other Source B corrections remain preserved.)*

---

## 1. Scope (P7-C §8 first slice)

P7-I1 creates the **smallest internal, Flask-free read/export application/use-case seam** required by
accepted P7-B/P7-C, exposing exactly **two distinct read-side use cases**:

1. **Authorized durable Project Read** — retrieve an authorized project **read representation**.
2. **Structured Export** — produce a governed, deterministic **structured export**, semantically
   distinct from the Project Read representation.

P7-I1 is **INTERNAL ONLY**; it exposes **no public API/route**. Later consumers (web, the future P7-I2
public API, future adapters) call this seam instead of touching engine/store internals directly. The
seam **consumes an already-established store** (IR-1) and an **explicit caller-supplied identity**
(IR-3); identity **resolution** stays with the caller.

## 2. Minimum architecture

```
Caller (resolves identity → account_id; provides an already-established store)   ← IR-1, IR-3
        ▼
Internal Read/Export Use-Case Seam            ← P7-I1 (new; thin; Flask-free)
   • authorized project READ      → validated ProjectRecordContract via durable load path (IR-2)
   • authorized STRUCTURED EXPORT → distinct deterministic composition (not record JSON; IR-6)
        │        │
        │        └─ consumes: durable record data + canonical domain support-state (+ reconstructed
        │                     review state as needed) — composed deterministically
        └─ consumes: load_owner (durable ownership fact; IR-3) + explicit caller account_id; fail-closed
        ▼
Existing Engine + Persistence (consume-only; unchanged)
```

The seam MUST NOT become microservices, distributed architecture, service mesh, plugin framework,
Integration Orchestrator, ESB, second engine, generic repository-abstraction project, or a broad web
refactor. No new architectural layer beyond the thin seam; no new authorization framework (IR-3).

## 3. Internal Project-Read contract

Returns the project's durable **record/evidence state** by consuming the **durable validated load path**
`store.load_contract(project_id)` → a validated `ProjectRecordContract` (versioned, provenance +
validation_status). Per **IR-2**, the durable load path is preferred over `from_state(live_state)` to
avoid shared mutable `AssertionRecord` references. **Prohibited as boundary objects:** raw SQLite/store
rows; `assemble_deliverable()` presentation dicts; `IdeaState` (too mutable/internal). No new DTO family.
Serves only **durably-owned projects to their owner** (IR-5).

## 4. Internal Structured-Export contract

A **distinct** internal operation producing a **deterministic structured export composed from canonical
project data** (durable record data + canonical domain support-state; reconstructed review state consumed
if needed). It is **not** `ProjectRecordContract` JSON and **not** `assemble_deliverable()`'s
presentation dict. Per **IR-6**, P7-I1 establishes the deterministic composition **behavior** and the
read/export **semantic distinction**, but **does not freeze** a new independent public/export version
identifier (a P7-I2 concern) and **does not freeze** final public JSON field names. Data-minimization /
selectability is a property, not a frozen schema. **If** the minimum export composition cannot be
established from canonical sources without reopening a P7-B/P7-C decision → **STOP and report the exact
ambiguity** (do not silently equate export with record JSON).

**What makes Structured Export semantically different from Project Read:** the Read returns the durable
record *as persisted*; the Export is a **governed, deterministic outward projection** composed from
canonical project data (with data-minimization/selectability), intentionally decoupled from both the
internal record shape and any future public wire schema.

## 5. Authorization enforcement approach

Authorization consumes the **existing durable ownership foundation** `store.load_owner(project_id) →
(exists, owner)` (**IR-3: ALREADY OWNED — CONSUME**) plus an **explicit caller-supplied `account_id`**.
Rule: **authorized ⇔ a durable owner is present AND `owner == account_id`; fail-closed otherwise.** Per
**IR-5**, `owner = NULL` is **not** automatic authorization for the durable service; missing/unowned →
fail-closed. Identity **resolution** (the current account / a future machine principal) stays with the
caller; the seam reads **no** Flask `request`/`session`/`SESSION_STORE`. No authorization logic is
extracted from `web/app.py` and **`web/app.py` is not modified** (IR-3, IR-4). The web layer keeps its
existing legacy/anonymous behavior unchanged; the internal service's fail-closed durable policy is a
deliberate surface-policy distinction (IR-5). **P7-I2 inherits no legacy/anonymous access.**

## 6. Non-mutation rule

Both use cases are strictly read-only **at the P7-I1 service-operation level**: the seam invokes only
non-mutating reads (`load_owner`, `load_contract`, and read-only reconstruction/support-state reads) on
an **already-established store** and performs **no** progression/validation/activation/Keep-Refine/write.
Per **IR-1**, the seam **does not instantiate/initialize a datastore** (schema DDL / additive migrations /
`BEGIN IMMEDIATE` in `SqliteRecordStore.__init__` are outside P7-I1 and untouched); the non-mutation
acceptance criterion is evaluated against the **service operation**, not the pre-existing store lifecycle.
Acceptance requires evidence of **no governed project/business-state mutation and no project
revision/content change** (semantic persisted-state equality/hash before vs after).

## 7. Explicit exclusions

No public HTTP/API route; no machine/API principal, credentials/tokens, scopes; no stable error envelope /
correlation headers / API audit / rate limiting; no writes/import/refinement/start-advance/progression/
Keep-Refine mutation; no subsystem persistence or public API; no async/job/webhooks; no external-result
ingestion; no adapter/vendor/Wokwi; no CAP-15…18 / AISR / QTA / ACV / WS17 / STG / PDF-Email /
Output-Language / Phase-9 activation; no P7-I2/P7-I3; no domain activation; no broad web-route migration;
**no `web/app.py` modification (IR-4)**; no `deliverable_assembler` presentation dict inside the seam; no
raw SQLite rows exposed; no `IdeaState` as the boundary object; **no SQLite initialization/concurrency/
migration change (IR-1)**; **no `ProjectRecordContract` change (IR-2)**; no engine/domains/schema/
migration/dependency/CI change; no new authorization framework (IR-3).

## 8. Permitted paths (illustrative names; final placement decided at implementation by evidence)

1. **One new Flask-free internal seam module** (e.g. `engine/read_export_service.py` — name not frozen).
   - WHY REQUIRED: the two read/export use cases must live somewhere Flask-free and import-safe; engine/
     is the deterministic home consumed by callers.
   - EXISTING OWNER: none (new seam). NEW RESPONSIBILITY: the two use cases + deterministic export
     composition + consumption of `load_owner`/`load_contract`.
   - LEAN JUSTIFICATION: one module; smallest unit that lets P7-I2 avoid calling engine/store internals.
2. **One new focused test module** (e.g. `tests/test_p7_i1_read_export_service.py` — name not frozen).
   - WHY REQUIRED: behavioral RED-first + ownership/non-mutation/no-leak/no-Flask evidence.
   - LEAN JUSTIFICATION: single focused test file.

**No `web/app.py` path** and **no other path** is permitted (IR-3/IR-4 removed the Source-A/B web-edit
path). Prefer fewer files if implementation shows one is unnecessary.

## 9. Prohibited paths

`web/app.py` (IR-4), `engine/record_store.py` (consume-only; IR-1 — no init/migration change),
`engine/record_contract.py` (consume-only; IR-2), `engine/session_reconstruction.py` /
`engine/deliverable_assembler.py` / `engine/idea_state.py` (consume-only or excluded), engine
scoring/progression/validation/domain modules, `domains/`, `schemas/`, `database/`/migrations,
`prompts/`, `scripts/`, CI, dependencies, all web routes/templates, all FDC-001 paths.

## 10. Web-migration decision

**DEFAULT: DEFER** (IR-4). `web/app.py` is **not modified** in P7-I1; existing read/export routes keep
their current behavior; no consumer is rewired to the seam (P7-I2 will consume it); the 36 routes are
**not** migrated. Deduplication alone is not justification. If a web change ever appears strictly
necessary for P7-I1 correctness → STOP and return to contract review.

## 11. RED → GREEN plan (for the future, separately-gated implementation)

**Behavioral RED on the then-current verified base** (fixtures via an already-established
`SqliteRecordStore`: an owned project + a cross-owner account): assert the **absent capability** —
(1) authorized durable-project read returns the record representation; (2) unauthorized/cross-owner read
fails closed (generic denial); (3) Structured Export is produced and is **distinct** from the Read
representation (deterministic composition; not record JSON); (4) neither read nor export mutates governed
project/business state. RED must fail **for the intended missing capability**, not merely because an
illustrative module/function name is absent; **no broad exception assertions**; **no manufactured
breakage**; **no weakening of existing tests**. **GREEN:** implement the thin seam consuming
`load_owner` + `load_contract` (+ explicit caller identity) to satisfy exactly these behaviors.

## 12. GREEN / regression plan

Full suite green; specifically `tests/test_p4_0_record_contract.py`, `test_p4_1a_record_store.py`,
`test_p4_2_session_reconstruction.py`, `test_p5_3_project_ownership_authorization.py`,
`test_deliverable_assembler.py` unchanged and passing (no read/export/ownership regression; `web/app.py`
untouched so P5-3 web behavior is unchanged). Additional GREEN evidence: the seam imports no Flask
`request`/`session`/`SESSION_STORE`; returns no raw store rows; adds no route; introduces no vendor
dependency; does not instantiate a datastore (IR-1); does not call `from_state(live_state)` (IR-2).

## 13. Security / ownership acceptance criteria

(a) No read/export unless `owner present AND owner == account_id`; (b) cross-owner access denied
(ownership-isolation: account A cannot read/export account B's owned project); (c) anonymous/invalid
`account_id` on an owned project denied (fail-closed); (d) `owner = NULL` / missing → denied by the
durable service (IR-5; not automatic authorization); (e) denial is generic/non-enumerating; (f) no Flask
session reliance inside the seam; (g) authorization consumes the existing `load_owner` foundation — no
second authorization system (IR-3). No machine-identity criteria (P7-I2 scope).

## 14. D-FPC-MAP-06 classification

| Element | Classification |
|---|---|
| Durable project read (`load_contract`) | ALREADY OWNED — CONSUME |
| Durable ownership fact (`load_owner`) | ALREADY OWNED — CONSUME (IR-3) |
| Serialization/provenance (`ProjectRecordContract`) | ALREADY OWNED — CONSUME (unmodified; IR-2) |
| Reconstructed review state (if needed) | ALREADY OWNED — CONSUME |
| Internal read/export use-case seam + deterministic export composition | P7-I1 CANONICAL RESPONSIBILITY |
| Datastore init/migration lifecycle | FUTURE / OTHER OWNER — OUTSIDE P7-I1 (IR-1) |
| Machine identity, public routes, DTO family, error envelope, correlation, rate-limit, export version identity | FUTURE / OTHER OWNER (P7-I2+; IR-6) |
| Presentation dict / raw rows / `IdeaState` as boundary | PROHIBITED |
| `web/app.py` authorization edit | NOT REQUIRED — DEFER (IR-3, IR-4) |

## 15. Lean check

Required by P7-C §8; consumes four existing canonical foundations; adds **one** module + **one** test
file; touches **no** `web/app.py`, engine internals, or governance-forbidden paths; duplicates nothing
(IR-3); freezes no public/export schema or version (IR-6); defers all routes/migration (IR-4); does not
reopen SQLite lifecycle (IR-1). Minimum safe path.

## 16. Top risks (with mitigations)

Project-Read/Structured-Export collapse → §3/§4 + IR-6 (distinct deterministic composition; no version
freeze; not record JSON). Legacy/NULL-owner leakage → §5 + IR-5 (fail-closed durable policy; web
unchanged; P7-I2 inherits nothing). Duplicate authorization → §5 + IR-3 (consume `load_owner`; no
framework). Hidden datastore-init writes under a "read-only" claim → §6 + IR-1 (store pre-established;
non-mutation scoped to the operation). `from_state` shared-reference mutation → §3 + IR-2 (durable load
path). `web/app.py` becoming an implementation requirement → §10 + IR-4 (DEFER; STOP if necessary).
Presentation/raw-row/`IdeaState` leakage → §3/§9. Over-engineering/DTO proliferation → §14/§15. False
RED/GREEN → §11 (behavioral, specific). Public-schema/version freeze → §4/IR-6. Scope creep → §7.

## 17. Pre-existing blockers / observations

- **NOT RELEVANT TO P7-I1:** single-threaded `SqliteRecordStore` serving (`threaded=False`) — accepted
  MVP limitation; not reopened (IR-1 keeps SQLite lifecycle outside P7-I1).
- **ACCEPTED LIMITATION / IR-5:** web `_project_authorized` NULL-owner and `sid in SESSION_STORE`
  branches are web-layer legacy behavior; the durable service does not inherit them (fail-closed).
- **IMPLEMENTATION GUARD / IR-2:** `ProjectRecordContract.from_state` shallow-reference risk — use the
  durable load path; do not build the boundary object over live mutable state.
- No PRE-EXISTING BLOCKER to read/export correctness found.

## 18. Implementation stop conditions

STOP and return to contract review if, at implementation: datastore initialization proves unavoidable
inside the seam (IR-1); `from_state(live_state)` appears required (IR-2); a `web/app.py` change appears
strictly necessary (IR-4); the minimum export composition cannot be established without a P7-B/P7-C
decision (IR-6/§4); NULL-owner durable-service access appears mandated (cite evidence or STOP — IR-5); any
mutation proves unavoidable; the seam cannot be Flask-free; a second authorization system becomes
tempting; a public-schema/endpoint/version freeze appears necessary; or Git history shows a state-change
not reflected in the roadmap.

## 19. Status (this candidate)

- P7-I1 CONTRACT: PUBLICATION CANDIDATE — PENDING INDEPENDENT PRE-MERGE REVIEW.
- REPOSITORY CONTRACT STATUS: CANDIDATE ONLY — NOT FINALLY ESTABLISHED FOR IMPLEMENTATION.
- P7-I1 IMPLEMENTATION: NOT STARTED. IMPLEMENTATION GATE LOCK: ACTIVE.
- INDEPENDENT REVIEW: REQUIRED against this exact candidate SHA/tree/bundle before merge.
- OWNER ACCEPTANCE: PENDING after independent acceptance.
- P7-I2: NOT STARTED. Phases 8/9/10 / deployment: NOT AUTHORIZED.
- IR-1…IR-6: INTEGRATED. Source A + Source B substance preserved except where IR supersedes.
