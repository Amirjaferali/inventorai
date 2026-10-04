# STAGE 35 — STRUCTURED INVENTION DISCLOSURE EXPORT — FIRST BOUNDED SLICE — IMPLEMENTATION CONTRACT (CANDIDATE)

STATUS: IMPLEMENTATION CONTRACT CANDIDATE — DOCUMENTATION ONLY — NO IMPLEMENTATION AUTHORIZED.
AUTHORITY LEVEL: subordinate to the accepted workstream contract
[`STAGE35_STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_WORKSTREAM_CONTRACT.md`](STAGE35_STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_WORKSTREAM_CONTRACT.md)
(the "workstream contract", as corrected by Correction 03, PR #754, and Correction 04, PR #755) and to the Owner decision
[`STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md`](STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md).
It is the "implementation contract" that workstream-contract prerequisites (2) and (3) require. It narrows nothing in
the workstream contract and amends none of its clauses; where this document and the workstream contract differ, the
workstream contract wins and the difference is a defect of this document.
RECORDED: 2026-10-04, by Owner authorization of ONE documentation-only first-slice implementation-contract candidate.
CONSOLIDATED CORRECTION 01: 2026-10-04, by Owner authorization of ONE documentation-only correction pass after the
Astra architecture review (fast stop on one failure-class defect) and the independent Claude reviewer (PASS WITH
CONDITIONS). It applies workstream Correction 04 (OD-A requirement quantities carried; OD-B interface observations
omitted; OD-C technical evidence unchanged; OD-D problem-capture limitation; the `reasoned_leading_claim` objective
exclusion; decisions 2 and 3 ACCEPTED), corrects the failure classification (§3.4: no downgrade of an unclassified
storage failure to `UNAVAILABLE`), fixes the E2 / `ProjectNotFound` consistency rule and extends the BASE RED plan. The
uncorrected candidate is preserved in Git history (PR #755, commit `749d2febf0afda0abd1673beeeeed8bb11c3cb2b`).
CONSOLIDATED CORRECTION 02: 2026-10-04, by Owner authorization of ONE documentation-only correction pass closing the four
remaining conditions of the completed Astra architecture review (PASS WITH CONDITIONS): (A) assumption-origin history
references (§8.3); (B) attribution for truth-bearing items and explicit reference-only inheritance (§8.1, §8.3, §9, §10);
(C) S1 authorization DENIAL versus post-authorization storage REFUSAL (§3.4, §4); (D) §5 aligned with the §3.1 sequence.
Every item that review closed is unchanged; the workstream contract is not changed. The Correction 01 text is preserved
in Git history (PR #755, commit `6538ad24340405decbcbe32711ce08bb5495f901`).
CONSOLIDATED CORRECTION 03: 2026-10-04, by Owner authorization of ONE documentation-only correction closing the one
residual finding (F1) of the independent non-authoring verification of Correction 02 (PASS WITH CONDITIONS): an active
record that is an endpoint of an active contradiction pair has no own Requirement Landscape row, so a reference to "its
field-29 row" could dangle and refuse a valid export. §7 now freezes ONE structural rule for the field-29 row(s)
canonically representing a record, applied in §8.3 to the assumption, `recorded_unknown` and `requirement_quantity`
references, with BASE RED #28. Every other clause, including Conditions B, C and D, is unchanged; the workstream contract
is not changed. The Correction 02 text is preserved in Git history (PR #755, commit
`6d470767dbc9133be5ce35b858d5ff8a2aaf1ad0`).
CORRECTION 04 (UX): 2026-10-04, by Owner authorization of ONE documentation-only UX correction pass after the UX /
behaviour review returned PASS WITH CONDITIONS (C1–C4); the architecture review and the non-authoring semantic
verification (including the Correction 03 delta) are complete. Under workstream contract Correction 05 it changes only
HTML copy and presentation: C1 neutral export labels (§12.4, §12.5, §12.7), C2 contextual envelope `NOT_APPLICABLE`
wording (§12.8), C3 one "How to read this document" block and one Risks clarification (§12.9, §12.10), C4 viewport,
wrapping and direction rules (§10), with UX obligations #29–#32 (§14) and a targeted re-check package (§16). No token,
marker, mapping, source, owner, schema, snapshot, failure or authorization rule changes. The Correction 03 text is
preserved in Git history (PR #755, commit `adffbbf6b695e866dc80bfc4381fca5e66edb8d4`).
CORRECTION 05 (final UX): 2026-10-04, by Owner authorization of ONE final documentation-only UX correction after the
targeted UX re-check returned PASS WITH CONDITIONS (C2 and C3 closed; Correction 05 authority, Arabic / RTL handling and
the narrow regression check passed; no further UX or architecture review required). It closes only R-C1 (one legend
sentence explaining existing owner-held "you" / "your" wording, §12.7, §12.9; #29 narrowed) and R-C4 (page-level
wrapping for the header digest and version identifiers, §10; #32 extended). No owner-held string, JSON value, token,
label semantics or other rule changes. The Correction 04 (UX) text is preserved in Git history (PR #755, commit
`c10da9014977d8cdb9ba9c53e977bb6be9eeaf6b`).
BASE: `feature/atomic-json-session-persistence` at `0ab87dca9ab5abebc03da791d288d661727d7858` (tree
`8cfd87c026298df7f31fd13cf082c6efe470ee7e`); `ACTIVE CONTRACT: NONE`; Stage 35 NOT ENTERED / NOT AUTHORIZED; the Master
Roadmap at 23 / 45 incomplete.
NON-AUTHORIZATION: this document implements nothing and authorizes no implementation. No route, page, download, file
generation, export, runtime schema, store change, persistence, migration, export history, test, API, provider, AI,
e-mail, attachment processing or user-facing behaviour is created by it. It does not enter Stage 35, does not implement
R1, does not modify `engine/record_store.py` and does not merge any product change. Implementation still needs the
remaining workstream-contract prerequisites: a separate Owner implementation authorization (prerequisite 1), the UX /
behaviour review before implementation (5), independent verification (6) and the focused / hosted checks (7).

---

## 0. Owner decisions applied

Workstream contract §17 decisions 2 and 3 are ACCEPTED (Correction 04) and are the authority; this contract only applies
them. Decision 2: no export-history record, no retained server-side export artifact and no export-history persistence in
this local-download first slice (§12.5, §13). Decision 3: one versioned JSON file and one self-contained HTML document from
the same projection; no PDF (§9, §10).

## 1. Slice summary

For ONE project owned by the authenticated account, on the owner's explicit request, the first slice composes ONE
deterministic disclosure projection from ONE store-owned SQLite read snapshot (§3), with one closed field map (§8), and
offers it as two owner-private local downloads: the JSON file and the HTML document. Composition reads canonical owner
data only, derives no new truth, mutates nothing, retains nothing, makes no network call and uses no AI or provider.

## 2. Module boundary and seam / extraction table

### 2.1 Projection module (frozen)

ONE new narrow engine module, `engine/disclosure_export.py`, is the only owner of the projection. It:

- composes references and values that existing owners produce; it derives no engineering truth, infers nothing,
  summarizes nothing and re-words nothing;
- holds the export's own fixed text that travels inside the projection (the eleven disclaimers in English with their
  Arabic supplements, the conditional disclaimer, the scope label, the problem-capture limitation of §12.6) and the
  closed v1 token sets (§9);
- performs no network call, imports no provider, API client or e-mail module, persists nothing and writes no log line
  carrying invention content;
- renders no legal conclusion, no patent claim, no assessment and no HTML.

`engine/read_export_service.py` is NOT extended: its module contract limits it to exactly two use cases (the authorized
Project Read and the Structured Export). The new module CONSUMES its existing public `get_authorized_project_read` and
`ProjectAccessDenied` unchanged (§4).

The HTML document and the pre-download page are rendered in the web layer (`web/app.py` route glue, two new templates,
new `UI_S35_*` keys in `web/ui_text.py`) from the finished projection only (§10).

### 2.2 Seam / extraction table (frozen)

Classes: **PUBLIC** = existing canonical public engine read; **STORE** = existing store-owner read, admitted inside the
snapshot today; **R1** = one of the six Correction-03 snapshot-participation readers; **EXTRACT** = permitted
behaviour-preserving extraction (workstream contract §4 rule 2), performed only inside the authorized implementation;
**PROHIBITED** = must not be used.

| # | Source need | Seam | Class |
|---|---|---|---|
| S1 | Authorization + validated ledger | `engine.read_export_service.get_authorized_project_read(store, project_id, account_id)` (`store.load_owner`, `store.load_contract`) | PUBLIC (+ STORE inside) |
| S2 | Reconstructed canonical state | `engine.session_reconstruction.reconstruct_readonly_state(store, project_id)` → `.review.level`, `.state` (reads `load_reconstruction_inputs`, `load_contract`, `load_need_routing`, `load_subsystem_composition` — all admitted inside the snapshot today) | PUBLIC (+ STORE inside) |
| S3 | Section-2 problem resolution | `engine.deliverable_assembler._resolved_problem` → public `resolved_problem(state)` | EXTRACT (E1) |
| S4 | Known mechanism | `state.known_mechanism` (`engine.idea_state.Evidence`) | PUBLIC |
| S5 | Planning metadata (success criterion, measurement method, test hypothesis, test variable / condition) | `web/app.py` `_durable_success_criteria`, `_durable_measurement_methods`, `_durable_test_hypotheses`, `_durable_test_variables`, `_attach_planning_metadata` → engine-level `load_planning_metadata` / `attach_planning_metadata` | EXTRACT (E2) over R1 readers |
| S6 | Section-11 experiments | `engine.deliverable_assembler.assemble_deliverable(state)["section_11_prototype_test_plan"]["items"]` (§5) | PUBLIC |
| S7 | Execution state | `web/app.py` `_experiment_execution_states` → engine-level `engine.experiment_result.execution_states(events, experiment_ids)`; events from `store.load_result_events` | EXTRACT (E3) over R1 reader |
| S8 | Interface dependencies | `store.load_interface_dependencies(project_id)` | R1 |
| S9 | Parts and interfaces | `state.subsystems`, `state.subsystem_interfaces` (from S2) | PUBLIC |
| S10 | Unresolved gaps | `state.gaps` filtered to status `OPEN` / `PARTIAL` | PUBLIC |
| S11 | Gap status label | `engine.deliverable_assembler._STATUS_LABELS` → public `gap_status_label(status)` | EXTRACT (E4) |
| S12 | Declared contradictions | `engine.idea_state.active_declared_contradiction_pairs(state.assertions)` + `contradiction_declared` records in `state.assertions` | PUBLIC |
| S13 | Assumptions, corrections, unknown dispositions | `state.assertions` (`AssertionRecord`: `disposition`, `content`, `provenance`, `validation_status`, `gap_context`, `superseded_by`, `supersedes`); chain shape classified only by the existing `engine.idea_state.classify_assumption_ancestry` | PUBLIC |
| S14 | Acknowledged unknowns | `state.acknowledged_unknowns` (`AcknowledgedUnknown.verbatim`, `.gap_context`) | PUBLIC |
| S15 | Routed needs | `engine.need_routing.active_routes(state)` (`NeedRoutingRevision.gap_type`, `.required_input`, `.provenance`) | PUBLIC |
| S16 | Requirement Landscape | `engine.requirement_landscape.derive_requirement_landscape(state).requirements` (`DerivedRequirement` fields) | PUBLIC |
| S17 | CAP-11 Source / Validation labels | `web/ui_text.py` keys `UI_ED_SOURCE_<provenance>`, `UI_ED_VALIDATION_<validation_status>`, `UI_ED_SOURCE`, `UI_ED_VALIDATION`, `UI_ED_FORM`, `UI_ED_HEADING` (tokens read from the Evidence object directly) | PUBLIC (render only) |
| S18 | Gap names | `web/gap_labels.py` `GAP_DISPLAY_NAMES` / `GAP_DISPLAY_NAMES_AR` (explicit locale; not `friendly_gap_name`, which depends on request state) | PUBLIC (render only) |
| S19 | Part labels | `web/ui_text.py` `UI_S15_SCOPE_MECH`, `UI_S15_SCOPE_ELEC`, `UI_S15_SCOPE_CTRL`, `UI_S15_SCOPE_FUNCTION` | PUBLIC (render only) |
| S20 | Section-11 labels | `UI_B_DELIV_075`, `UI_B_DELIV_078`, `UI_B_DELIV_080`, `UI_DELIV_METHOD_ABSENT_LABEL`, `UI_DELIV_HYPOTHESIS_ABSENT_LABEL`, `UI_DELIV_VARIABLE_ABSENT_LABEL`, `UI_S11_EXECUTION_LABEL`, and `web/app.py` `S11_EXECUTION_TEXT` | PUBLIC (render only) |
| S21 | Inactive-declaration wording / Landscape heading | `UI_T3A_CONFLICT_INACTIVE`; `UI_B_DELIV_036` | PUBLIC (render only) |
| S22 | Requirement quantities (OD-A) | `store.load_requirement_quantities(project_id)` — validated history; no `_refuse_uncommitted_reads()` call (it reads `requirement_quantities` rows and `load_contract`, both admitted inside the snapshot today); NOT a seventh R1 reader and not changed | STORE |
| S23 | Requirement-quantity rows | `engine.requirement_quantity.requirement_quantities_meta(state)` (pure; the owner's canonical rows with its `active` / `anchor_active` booleans; fails closed on an unresolvable anchor) | PUBLIC |
| S24 | Requirement-quantity labels | `UI_T2A_KIND_<TOKEN>`, `UI_T2A_CURRENT`, `UI_T2A_REPLACED`, `UI_T2A_WITHDRAWN_ANCHOR`, `UI_T2A_WITHDRAWN_NOTE` | PUBLIC (render only) |
| P1 | `state.known_problem` | — | PROHIBITED (RISK-002; workstream contract §6) |
| P2 | `web/app.py` `_declared_conflict_view`, `_evidence_details`, `_experiment_execution_states` called as-is | — | PROHIBITED (web-layer helpers are not canonical seams) |
| P3 | Any rendered report / PDF / HTML string as source truth | — | PROHIBITED |
| P4 | Private store validators (`_validated_dependencies`, `_validated_result_events`, …) called from outside the store | — | PROHIBITED |

### 2.3 Permitted extractions (frozen; performed only inside the authorized implementation)

| # | Current helper | Destination | Existing consumers | Byte-identical invariant |
|---|---|---|---|---|
| E1 | `engine/deliverable_assembler.py` `_resolved_problem(state)` | public `resolved_problem(state)` in the same module; `_resolved_problem` stays as an alias bound to it | `_s2`, `_evidence_registry` | report HTML, PDF and the canonical deliverable package (minus `generated_at`) identical for the same fixtures |
| E2 | `web/app.py` `_durable_success_criteria`, `_durable_measurement_methods`, `_durable_test_hypotheses`, `_durable_test_variables`, `_attach_planning_metadata` | `engine/session_reconstruction.py`: `load_planning_metadata(store, project_id)` (loads all four collections, builds the same `SuccessCriterion` / `MeasurementMethod` / `TestHypothesis` / `TestVariable` maps, returns `None` per collection on `ProjectNotFound`, RAISES every other failure), pure `apply_planning_metadata(state, metadata)` (today's assignment step: a `None` collection leaves its carrier as it is) and `attach_planning_metadata(store, project_id, state)` (load + apply with exactly today's all-or-nothing semantics: any exception → `False`, `state` untouched); the five web helpers become thin wrappers with unchanged names, signatures and return values | three `_attach_planning_metadata` call sites (session render, cold read-only render, planning page) | report HTML, PDF, planning page, session page and every existing test identical |
| E3 | `web/app.py` `_experiment_execution_states(sid, package)` and the constants `_EXECUTION_NONE` / `_EXECUTION_RECORDED` / `_EXECUTION_UNAVAILABLE` | `engine/experiment_result.py`: constants `EXECUTION_NONE = "none"`, `EXECUTION_RECORDED = "recorded"`, `EXECUTION_UNAVAILABLE = "unavailable"` and pure `execution_states(events, experiment_ids)` (count = `len(result_chains(events, eid))`; never reads the store, never swallows); the web helper keeps its name, signature and catch-all UNAVAILABLE behaviour, its constants become aliases | Section-11 report and PDF rendering | report HTML and PDF identical, including the UNAVAILABLE case |
| E4 | `engine/deliverable_assembler.py` `_STATUS_LABELS` | public `gap_status_label(status)` returning `_STATUS_LABELS.get(status)`; the dict is unchanged | existing internal users unchanged | report HTML, PDF and package identical |

No other extraction is permitted. No helper is copied into a second implementation; the disclosure module calls the
extracted function, never a re-implementation.

**E2 / `ProjectNotFound` composer rule.** `load_planning_metadata` returns `None` for a collection only when that
collection's reader raised `ProjectNotFound`. Inside Stage 35 composition any `None` collection is REFUSAL (§3.4) — never
an empty collection, never `NOTHING_RECORDED` and never `UNAVAILABLE` — and the composer does not call
`apply_planning_metadata` with it. Outside Stage 35 the existing web behaviour is unchanged: `attach_planning_metadata`
and the five web wrappers keep today's semantics (a `None` collection leaves its carrier as it is).

## 3. Snapshot coherence and the R1 contract

### 3.1 Composition sequence (frozen)

`compose_disclosure_projection(store, project_id, account_id)`:

1. The web route has already resolved the account through `_current_account()`; `None` → `_deny_project()` (§4).
2. If `store.committed_state_readable()` is `False`, refuse (the snapshot cannot be acquired from a safe,
   transaction-resolved connection).
3. Enter exactly ONE outer `with store.read_snapshot():`. With step 2 true, this executes the store's `SAVEPOINT`; an
   exception there refuses.
4. Inside the snapshot, in this order:
   a. S1 `get_authorized_project_read(...)` — `ProjectAccessDenied` propagates as a denial (§4);
   b. S2 `reconstruct_readonly_state(store, project_id)` — `review.level != 1` refuses;
   c. S22 `load_requirement_quantities(project_id)` (STORE; always called, even for a project with no quantity);
   d. the R1 reads, in this order: E2 `load_planning_metadata` (four R1 readers), S8 `load_interface_dependencies`,
      S7 `load_result_events` (always called, even for a project with no experiment).
5. Every source value the projection needs is materialized into memory inside the snapshot. As the last statement of
   the `with` block the composer checks `store.committed_state_readable()`: inside a healthy store-owned snapshot it is
   `False` (the read transaction is open); `True` means the read transaction ended underneath the composer, so the
   export refuses. No source is read after the block ends.
6. After leaving the snapshot, if `store.committed_state_readable()` is `False` (a release failure left the connection
   unresolved, or the sticky unsafe state is set), refuse.
7. Pure, in-memory composition (applying the loaded planning metadata to the reconstructed state, assigning the S22
   history to the in-memory reconstructed state's `requirement_quantities` carrier exactly as the existing cold-load seam
   does, `assemble_deliverable`, `derive_requirement_landscape`, `requirement_quantities_meta`, `active_routes`,
   contradiction pairs, the field map) and the
   v1 schema check (§9.6) then run without any store access. JSON serialization and HTML rendering consume only the
   finished projection.

The checks in steps 2, 5 and 6 use only the existing public `committed_state_readable()`; no public snapshot predicate
is added, nothing is re-read, retried or reconnected.

### 3.2 R1 shape (described here; implemented only under a later authorization)

Correction 03 is binding. The existing `read_snapshot()` stays the sole coherence authority.

- **Private store-owned ownership evidence.** One private in-memory attribute on `SqliteRecordStore` (for example
  `_read_snapshot_owned`, initially `False`). `read_snapshot()` sets it to `True` only on the branch that actually
  executed `SAVEPOINT` (immediately after it succeeds), and the same call resets it in its `finally`. The no-op branch
  (taken when the connection is not committed-state-readable, which includes every nested call) never sets or clears it.
  No other code writes it. Nothing about it is durable.
- **One private admission guard** (for example `_admit_snapshot_read()`), in this exact order:
  1. if `_connection_unsafe` → raise `RecordStoreConnectionUnsafe` (same type and message as today);
  2. if the ownership evidence is set: if the connection is no longer in a transaction, the snapshot was lost
     underneath the owner → raise `RecordStoreConnectionUnsafe`; otherwise admit;
  3. otherwise call the existing `_refuse_uncommitted_reads()` unchanged (standalone behaviour, including refusal of any
     bare caller-owned transaction).
- **Exactly six substitutions.** In `load_interface_dependencies`, `load_success_criteria`, `load_measurement_methods`,
  `load_test_hypotheses`, `load_test_variables` and `load_result_events`, the leading `self._refuse_uncommitted_reads()`
  call is replaced by `self._admit_snapshot_read()`. Nothing else in those readers changes: query text, ordering,
  validation, project binding, `ProjectNotFound`, the `*Corrupt` classes and their internal `with self.read_snapshot()`
  (a no-op inside the outer snapshot) stay as they are.
- **Unchanged.** `_refuse_uncommitted_reads()`, `committed_state_readable()`, `_transaction_resolved()`, `_write()`,
  every writer, every `committed_*` confirmation reader, every other reader, the schema, every table and every
  migration. The flag-only guard of `load_project_subsystems` is not copied.
- **IR-01 holds.** Admission happens only inside a snapshot the store itself acquired from a safe, transaction-resolved
  connection; a caller-owned transaction or the sticky unsafe state is refused; a lost snapshot is refused, never
  reconnected, repaired, retried or switched. Writers stay refused inside the snapshot by their existing guards.
- **Threading.** The store is one application-scoped connection under the existing single-process, `threaded=False`
  design; the evidence is per store instance. Multi-threaded or multi-worker use is outside this contract, as it is for
  the store today.

### 3.3 What coherence means here (workstream contract §4A as corrected)

Every value in one export comes from the one snapshot opened in step 3. A commit by another connection after that point
neither switches the export to newer state nor refuses it; a later export, in a new snapshot, sees the later state. A
lost snapshot is detected by the final R1 admission (step 4d) or the step-5 check and refuses the export. "Snapshot"
names a read view only; no revision identity is created or implied.

### 3.4 Failure classification (frozen)

| Condition | Class |
|---|---|
| No account; `ProjectAccessDenied` from S1 — raised by the existing authorization owner for a missing project, another account's project, a NULL owner and any ownership-lookup failure, which `_is_authorized` deliberately converts (every exception from `store.load_owner`, storage errors included) | DENIAL (`_deny_project()`; byte-identical, non-enumerating; no file) |
| Any failure that propagates from S1 AFTER authorization succeeded (from `store.load_contract`: `ContractError`, `ProjectNotFound`, any `sqlite3.Error`) | REFUSAL (never converted to a denial) |
| Step 2 or step 6 false; `SAVEPOINT` failure; `RecordStoreConnectionUnsafe` anywhere; the step-5 check `True` (snapshot lost) | REFUSAL (snapshot acquisition / loss) |
| `review.level != 1`; `ContractError`; `MalformedAssumptionAncestryError`; `ReconstructionReplayLimitError` | REFUSAL |
| `ProjectNotFound` from any reader inside the snapshot; a `None` collection from E2 `load_planning_metadata` (§2.3 composer rule) | REFUSAL (project binding) |
| Any store `*Corrupt` error (`SuccessCriterionCorrupt`, `ResultEventsCorrupt`, interface / dependency corruption, …); `QuantityHistoryError` | REFUSAL (inconsistent source history) |
| Any exception from a pure derivation (S3, S6, S11, S12, S15, S16, S23) or a failed v1 schema check (§9.6) | REFUSAL (global integrity / schema failure) |
| A ledger anchor, endpoint, part or quantity-anchor reference that does not resolve by identity in the same snapshot | REFUSAL (project-binding / anchor defect) |
| Missing table; missing column; malformed or invalid schema (for example `sqlite3.OperationalError` "no such table" / "no such column") | REFUSAL (schema failure) |
| Database integrity failure or corruption (for example `sqlite3.DatabaseError` "database disk image is malformed", `sqlite3.IntegrityError`) | REFUSAL (integrity failure) |
| Any other `sqlite3.Error`, from any source read (S1 after authorization, S2, S22, E2 planning load, `load_interface_dependencies`, `load_result_events`) | REFUSAL (unclassified storage failure) |
| Any other exception whose section locality is not positively proven, or any failure that could affect more than one source or the meaning of a source | REFUSAL |

**`UNAVAILABLE` admission rule.** A source failure may be shown as section-local `UNAVAILABLE` only when ALL of the
following hold: (1) the failing source or collection is explicitly named by this contract as section-local; (2) the
error's own semantics positively establish that locality; (3) the snapshot is still valid; (4) every unaffected source
remains coherent; and (5) the failure is not a schema, integrity, corruption or global storage failure. "The read
transaction is still open" is NOT proof of locality.

**First-slice positively-local set: EMPTY.** At this base no first-slice source read exposes a failure class whose
semantics positively establish section locality: S1, S2, S22 and the six R1 readers raise only `ProjectNotFound`,
`RecordStoreConnectionUnsafe`, their owners' `*Corrupt` / history-error classes, contract / reconstruction errors or raw
`sqlite3.Error`, none of which is section-scoped. Every first-slice source failure is therefore REFUSAL, and no v1
composition produces `UNAVAILABLE`. The marker, its §12.3 wording, `unavailable_notice` and the top sentence stay in the
closed v1 schema and rendering (workstream contract §4A, §5); admitting a positively local failure class later needs a
named source, a contract correction and review. This contract invents no error class.

A refusal is a bounded error: no JSON, no HTML, no file and no partial output. The JSON route and the HTML route answer a
refusal with a bare, empty-bodied 503, exactly like the P10-D3a self-service export. A refusal never degrades to
`UNAVAILABLE`.

The disclosure export is stricter than the Stage-19 web helper on purpose: that helper maps every failure, corruption
included, to UNAVAILABLE for its own surfaces (unchanged by E3); the disclosure export refuses on every first-slice
source failure, corruption included, as workstream contract §4A and the admission rule above require.

## 4. Authentication and authorization (frozen)

- One authenticated owner: the route resolves the account through the existing `_current_account()` seam only.
  Anonymous callers receive `_deny_project()`.
- One explicitly requested owned project: authorization is the existing `get_authorized_project_read`, called inside
  the snapshot so the ownership decision and the content come from the same committed state. It denies a missing
  project, another account's project, a project with a NULL (anonymous / legacy) durable owner and any ownership-lookup
  failure identically; every such denial maps to the same `_deny_project()` response, so a missing project and another
  account's project are indistinguishable.
- **DENIAL versus REFUSAL at S1.** Only what the authorization owner itself converts to `ProjectAccessDenied` is a
  DENIAL — including a storage failure during the ownership lookup, which `_is_authorized` deliberately swallows. A
  failure that propagates after authorization succeeded (from `store.load_contract`) is a REFUSAL (empty 503, §3.4) and
  is never re-mapped to a denial; a denial is never re-mapped to a 503. A refusal raised before S1 (steps 2–3) depends
  only on the connection, never on the project, so it discloses nothing about the project.
  `get_authorized_project_read`, `_is_authorized` and `_deny_project()` are unchanged.
- The pre-download page uses the same two seams (outside any snapshot; it composes nothing). No new authentication,
  session, capability or API-credential mechanism is introduced, and the permissive `_project_authorized` capability
  helper is never used.

## 5. Experiment-source ruling (one answer)

**Ruling: the projection consumes the canonical deliverable package's Section 11 —
`assemble_deliverable(state)["section_11_prototype_test_plan"]["items"]` — read-only, through a closed key allow-list.**

- `assemble_deliverable` is the existing public engine function the report and PDF already use; the items are the
  generator's structured data, not rendered presentation text, and the canonical `experiment_id` keys the planning and
  execution joins exactly as the Stage-19 helper does.
- No extraction of `_s11` is made, so no second derivation exists and the report and PDF cannot change.
- Sequence (exactly §3.1): `load_planning_metadata(store, project_id)` runs INSIDE the outer snapshot (step 4d) and its
  result is materialized; after the snapshot exits, the pure `apply_planning_metadata(state, metadata)` applies that
  already-loaded object to the in-memory reconstructed state, and `assemble_deliverable(state)` then runs (step 7) with
  no further store read. The composer never calls the store-reading `attach_planning_metadata` or any web wrapper
  (`_attach_planning_metadata`, `_durable_*`); those keep their existing behaviour for the existing web surfaces.
  `generated_at` and every non-Section-11 key of the package are ignored.
- Allow-list per item: `experiment_id` (join key only; never exported), `experiment_title`, `objective`,
  `what_to_observe`, `traceability.source_type` (decision input for §6 only; never exported), `success_criterion`,
  `success_criterion_provenance`, `success_criterion_status`, `measurement_method`, `measurement_method_provenance`,
  `test_hypothesis`, `test_hypothesis_provenance`, `test_variable`, `test_variable_provenance`. Every other key
  (`source_basis`, `minimum_prototype`, `failure_or_revision_condition`, `expected_evidence_upgrade`,
  `required_expertise_or_tools`, `traceability.source_ref`, `traceability.content`) and every plan-level key
  (`shared_required_expertise`, `stale_*`, `note`, `empty_statement`) is not exported.
- If the planning load fails or returns a `None` collection, the export refuses (§2.3 composer rule, §3.4); there is no
  planning-only `UNAVAILABLE`, and `assemble_deliverable` never runs on state without the durable planning metadata.

## 6. Section 11 finding — disposition (authorized by workstream contract §7, Correction 04)

Evidence, `engine/deliverable_assembler.py` `_s11` at this base:

1. **Grade wording reaches the objective text — yes, for one source type.** For the priority-3 experiment
   (`traceability.source_type == "reasoned_leading_claim"`) the generated objective is the fixed string "Build a minimum
   prototype of the described mechanism and observe whether it behaves as the inventor described, to raise the evidence
   from Reasoned toward Demonstrated." "Reasoned" and "Demonstrated" are the evidence-quality grade names
   (`engine.idea_state.REASONED` / `DEMONSTRATED`).
2. **Selection and text.** That experiment exists only when `_overall_quality(state) == REASONED` — its selection is
   itself grade-conditioned, AND its objective text names the grades. The two other source types
   (`acknowledged_unknown`: "Evaluate the inventor's stated unknown under controlled conditions to reduce its
   uncertainty."; `assumption_inventory_evidence`: "Test an essential or untested assumption the mechanism depends on.")
   contain no grade word; their selection is not grade-conditioned at the experiment level (Stage-3 gap evidence, the
   priority-2 source, is admitted only at `REASONED` or better by `engine/progression_loop.py`, a general admission
   threshold that the exported text does not state). `what_to_observe` contains no grade word for any of the three
   types; `experiment_title` contains none (the priority-3 title uses the verb "demonstrate", not a grade label).
   `expected_evidence_upgrade` names a grade for all three types and `source_basis` does for `reasoned_leading_claim`;
   neither is ever exported (§5).
3. **Disposition.** The objectives of the `acknowledged_unknown` and `assumption_inventory_evidence` experiments are
   allowed system assertions (workstream contract §6). The objective of a `reasoned_leading_claim` experiment is not
   exported: workstream contract §7 (Correction 04) explicitly names `reasoned_leading_claim.objective` as
   `EXCLUDED_FROM_FIRST_SLICE`, with the fixed reason quoted in §12.4 (`OBJECTIVE_NAMES_EVIDENCE_LEVEL`), and §6 carries
   the matching CAP-09 exception. Only that slot carries the marker. The experiment itself (title, what to observe,
   planning fields, execution state) is carried: none of those values states a grade. The source text is not reworded,
   no sanitized objective is synthesized, no grade value is exported and the experiment generator is unchanged. The
   decision input is the structural token `traceability.source_type`, never the objective text.

## 7. Requirement Landscape content-class ruling

The Landscape owner composes some statements by interpolating inventor text into a system template
(`_DECLARED_STATEMENT`, `_INTERFACE_STATEMENT`). The projection never exports such a combined string as one value and
never parses free text. Each row is classified only by `primary_anchor.anchor_kind` and by resolving
`primary_anchor.anchor_reference` by exact identity in the same snapshot:

| Row (anchor kind; reference resolution) | System-assertion slots | Quoted-inventor slots | Combined statement string |
|---|---|---|---|
| `assertion`, `pending_evidence`, `pending_specialist`; reference = an id in `state.assertions` | `label` (`display_label`), `status` (`source_status`), `resolving_action` (`resolving_action.statement`) | `statement` = that record's own `content`, with that record's envelope; structurally empty content → `NOTHING_RECORDED` (the owner's placeholder is not exported) | not exported |
| `pending_evidence`, `pending_specialist`; reference not a ledger id (routing row, `routing:` reference) | `label`, `status`, `resolving_action`, `statement` (owner text built only from fixed wording and a gap label) | none | exported as the system `statement` |
| `gap`; reference = a gap type | `label`, `status`, `resolving_action`, `statement` (the gap label) | none | exported as the system `statement` |
| `active_contradiction` whose pair is in `active_declared_contradiction_pairs(state.assertions)` | `label`, `status`, `resolving_action` | `answer_a`, `answer_b` = the two endpoint records' `content` (pair order), each with its own envelope | NOT exported (system template + quoted text) |
| `active_contradiction` not declared (legacy edge) | `label`, `status`, `resolving_action`, `statement` (`_CONTRADICTION_STATEMENT`, system-only) | `answer_a`, `answer_b` as above | exported as the system `statement` |
| `subsystem_interface`; reference = an `interface_id` in `state.subsystem_interfaces` | `label`, `status`, `resolving_action` | `part_a`, `part_b` (the endpoint parts' `display_name`), `description`, with the interface envelope | NOT exported (system template + quoted text) |

The pair order and the endpoint identities come from the owner's own reference format (`lo|hi`, split exactly as the
owner's `_order_key` does) and from `SubsystemInterface.subsystem_a_id` / `subsystem_b_id`. A declared-contradiction
row refs its field-15 item; an interface row refs its field-8 item. Criticality,
criticality authority, criticality rationale, linked risk ids and Grounded Risks are never exported (§8 of the
workstream contract). The internal `requirement_id` and `anchor_reference` values are never exported; cross-references
use v1 item keys (§9). An unresolvable reference refuses the export (§3.4). No classifier is introduced: existing
structure supports the distinction completely. No `requirement` item carries a requirement-quantity value: each quantity
value appears once, in its field-12 `requirement_quantity` item, which refs the field-29 row canonically representing
its anchoring answer (always that answer's own `assertion` row, §8.3).

**Canonical field-29 representation of a record (Correction 03).** Wherever this contract references "the field-29
row(s) canonically representing record X" (X an active ledger record), the target is resolved structurally from the one
existing Landscape derivation (`derive_requirement_landscape`), never from text:

1. **Own row.** X's own record-anchored `requirement` item — anchor kind `assertion`, `pending_evidence` or
   `pending_specialist`, `primary_anchor.anchor_reference` = X — when field 29 holds it.
2. **Contradiction row.** Otherwise, every `active_contradiction` `requirement` item whose anchor pair (`lo|hi`, split
   exactly as the owner's `_order_key` does) names X, in owner order. The owner emits one such row per active pair and
   no own row for either endpoint (it derives the pairs first and then skips every paired record), and the row carries
   X's content with X's own envelope in its `answer_a` or `answer_b` slot. The rule is identical for a declared pair and
   a legacy edge: the two §7 row forms differ only in their `statement` slot. When X is an endpoint of more than one
   active pair, the reference lists every such row.
3. **Refusal.** No row resolves → REFUSAL (anchor / reference defect, §3.4).

The two cases are mutually exclusive in the owner's derivation, so X is never represented twice and no row is ever
created for it. No second Landscape derivation, contradiction inference, classifier or text match is introduced.

## 8. Source-to-envelope mapping (frozen)

### 8.1 Envelope

Every `RECORDED` value slot carries `content_class`, `source_owner` and an envelope of four fields. Each envelope field
is `{"marker": "RECORDED", "value": <owner value>}`, `{"marker": "NOT_APPLICABLE", "value": null}` (the owner holds no
such metadata for this kind of item) or `{"marker": "UNAVAILABLE", "value": null}`. No value is ever substituted.

- **provenance:** the owner's own provenance token where the owner object holds one (`Evidence.provenance`,
  `AssertionRecord.provenance`, `Subsystem.provenance`, `SubsystemInterface.provenance`,
  `NeedRoutingRevision.provenance`, `RequirementQuantity.provenance`, and the Section-11 planning provenance tokens
  `user_defined` / `source_stated`); otherwise `NOT_APPLICABLE`.
- **validation_state:** `Evidence.validation_status`, `AssertionRecord.validation_status`,
  `Subsystem.validation_state`, `SubsystemInterface.validation_state`, `RequirementQuantity.validation_status`; otherwise
  `NOT_APPLICABLE`.
- **limitation:** `NOT_APPLICABLE` for every first-slice source — no first-slice owner holds a per-item limitation-text
  field. Owner limitations travel as the owner's own status tokens and wording (validation state, Landscape status and
  resolving action, the Stage-19 execution wording). The problem-capture limitation is not owner-held: it is the
  export's own fixed system-assertion slot on the `resolved_problem` item (§8.3), never envelope limitation text.
- **currency:** `CURRENT` / `SUPERSEDED` only for ledger records (`superseded_by is None` → `CURRENT`); otherwise
  `NOT_APPLICABLE`. A requirement quantity's chain state travels under the owner's own tokens `active` / `anchor_active`
  (§8.3) and is never mapped into `currency`.

Owner-specific metadata travels in an item's `tokens` map under closed keys (§9.3), never in a generic field.
`LEGACY_UNSPECIFIED` stays as it is.

**Attribution coverage (Correction 02).** Every `RECORDED` item is exactly one of:

- **Truth-bearing** — it carries at least one source fact. Every such item has at least one `RECORDED` slot with
  `content_class`, `source_owner` and the four-field envelope above, filled only with values the canonical owner holds
  and `NOT_APPLICABLE` where the owner holds no such metadata; nothing is defaulted. A fact the owner states without
  text is carried as a `SYSTEM_ASSERTION` slot with value `null` whose `tokens` hold that fact (as `execution_state`
  already does), so the fact and its attribution travel together. Item-level tokens are only (i) fields of the same
  owner object as one of the item's `RECORDED` slots, attributed by that slot's envelope, or (ii) the export's
  structural ordering tokens `chain` and `position`, which state no source fact.
- **Reference-only** — exactly two kinds, `gap_reference` and `evidence_reference`. Such an item has no `RECORDED` slot
  of its own (`evidence_reference`'s only slot is the `EXCLUDED_FROM_FIRST_SLICE` `cap11_form` marker), creates no
  independent source fact, and has exactly one ref. It inherits, structurally through that ref and never from text,
  exactly the referenced slot's `content_class`, `source_owner` and envelope: `gap_reference` from the `gap_state`
  slot of its field-15 `unresolved_gap` item; `evidence_reference` from the `text` slot of `problem_addressed.1` or
  `technical_concept.1`, whose provenance and validation state are the CAP-11 Source and Validation rows. Its
  placement in field 17, 18 or 24 is the export's fixed field map, not a source fact. A dangling ref refuses (§3.4).

No other kind is reference-only, and a truth-bearing kind is never labelled reference-only to avoid an envelope.

### 8.2 Field map (29 fields, fixed order)

Each Owner-decision §2 row with more than one first-slice disposition is split into fields that each carry exactly one
marker. "Integrated" means the reconstructed state holds a durable Owner-declared composition (`state.subsystems`
non-empty).

| # | Field token | Disposition | Owner / seam | Items |
|---|---|---|---|---|
| 1 | `invention_title` | `NOT_CAPTURED` | — | — |
| 2 | `problem_addressed` | `RECORDED` / `NOTHING_RECORDED` | S3 `resolved_problem` | 1 item, kind `resolved_problem`, with its fixed `capture_limitation` slot |
| 3 | `background_and_existing_limitations` | `NOT_CAPTURED` | — | — |
| 4 | `invention_objective` | `NOT_CAPTURED` | — | — |
| 5 | `technical_concept` | `RECORDED` / `NOTHING_RECORDED` | S4 `state.known_mechanism` | 1 item, kind `known_mechanism` |
| 6 | `parts` | integrated: `RECORDED`; otherwise `NOT_CAPTURED`, reason `NON_INTEGRATED_PROJECT` | S9 | kind `part`, composition order |
| 7 | `component_descriptions_beyond_parts` | `NOT_CAPTURED` (otherwise-case reason `NON_INTEGRATED_PROJECT`) | — | — |
| 8 | `relationships` | integrated: `RECORDED` / `NOTHING_RECORDED`; otherwise `NOT_CAPTURED`, reason `NON_INTEGRATED_PROJECT` | S9 + S8 | kind `interface`, interface order |
| 9 | `operating_sequence_or_workflow` | `NOT_CAPTURED` | — | — |
| 10 | `alternative_embodiments` | `NOT_CAPTURED` | — | — |
| 11 | `typed_materials_dimensions_parameters_conditions` | `NOT_CAPTURED` | — | — |
| 12 | `raw_materials_dimensions_parameters_conditions` | `RECORDED` when the requirement-quantity owner holds at least one row; otherwise `RAW_TEXT_ONLY`, pointer `requirement_landscape`, when field 29 holds at least one quoted slot; otherwise `NOTHING_RECORDED` | S22 + S23 | kind `requirement_quantity`, owner order |
| 13 | `interface_verification_preparation_inputs` | `EXCLUDED_FROM_FIRST_SLICE`, reason `PLANNING_INPUTS` | — (not read) | — |
| 14 | `novelty_and_differentiation` | `NOT_CAPTURED` | — | — |
| 15 | `unresolved_technical_issues` | `RECORDED` / `NOTHING_RECORDED` | S10 + S12 | kinds `unresolved_gap`, `declared_contradiction`, `declared_contradiction_history` |
| 16 | `assumptions` | `RECORDED` / `NOTHING_RECORDED` | S13 | kind `assumption` |
| 17 | `missing_information` | `RECORDED` / `NOTHING_RECORDED` | S10 + S13 + S14 + S15 | kinds `gap_reference`, `acknowledged_unknown`, `recorded_unknown`, `routed_specialist_need` |
| 18 | `technical_evidence` | `RECORDED` / `NOTHING_RECORDED` | S3 + S4 | kind `evidence_reference` |
| 19 | `commercial_manufacturing_integration_evidence` | `EXCLUDED_FROM_FIRST_SLICE`, reason `CONFIDENTIAL_EVIDENCE_CATEGORIES` | — (not read) | — |
| 20 | `diagrams_and_files` | `NOT_CAPTURED` | — | — |
| 21 | `experiments` | `RECORDED` / `NOTHING_RECORDED` | S6 + E2 + E3 | kind `experiment` |
| 22 | `experiment_result_text` | `EXCLUDED_FROM_FIRST_SLICE`, reason `RESULT_TEXT_NOT_CARRIED` | — (not read as text) | — |
| 23 | `validation_results` | `NOT_CAPTURED` | — | — |
| 24 | `risks` | `RECORDED` / `NOTHING_RECORDED` | refs to field 15 | kind `gap_reference` |
| 25 | `uncertainty_and_abstentions` | `NOT_APPLICABLE`, reason `CARRIED_ON_EVERY_ITEM` | — | — |
| 26 | `corrections` | `RECORDED` / `NOTHING_RECORDED` | S13 | kind `correction_version` |
| 27 | `approvals` | `NOT_CAPTURED`, reason `NO_APPROVAL_RECORD` | — | — |
| 28 | `source_and_provenance_references` | `NOT_APPLICABLE`, reason `CARRIED_ON_EVERY_ITEM` | — | — |
| 29 | `requirement_landscape` | `RECORDED` / `NOTHING_RECORDED` | S16 | kind `requirement`, owner order |

`NOT_APPLICABLE` is used at field level only for fields 25 and 28 (the cases this contract names, workstream contract
§5). No v1 composition produces `UNAVAILABLE`, at field or slot level: the first-slice positively-local set is empty
(§3.4). Field 12 never classifies, parses or types inventor text: it carries the requirement-quantity owner's rows as
opaque quoted values, and its `RAW_TEXT_ONLY` pointer is used only when that owner holds no row, so it never states that
the inventor's wording appears only in the Requirement Landscape while a quantity row exists. The pointer does not
assert that such values are present.

### 8.3 Item and slot mapping

`content_class` is `QUOTED_INVENTOR_CONTENT` (Q) or `SYSTEM_ASSERTION` (S). "Env" lists provenance / validation_state /
currency (limitation is always `NOT_APPLICABLE`; §8.1).

| Kind | Slots (class) | Env | Tokens / refs | Nothing / failure behaviour |
|---|---|---|---|---|
| `resolved_problem` | `text` (Q) = `resolved_problem(state).content`; `capture_limitation` (S) = the exact §12.6 English text, always present, source owner `DISCLOSURE_EXPORT` | `text`: `Evidence.provenance` / `.validation_status` / NA; `capture_limitation`: NA / NA / NA | — | field `NOTHING_RECORDED` when `resolved_problem` is `None` (no item, so no limitation); the limitation never depends on the problem text |
| `known_mechanism` | `text` (Q) = `state.known_mechanism.content` | `Evidence.provenance` / `.validation_status` / NA | — | field `NOTHING_RECORDED` when `known_mechanism` is `None` |
| `part` | `name` (Q) `display_name`; `function` (Q) `function_text` | `Subsystem.provenance` / `.validation_state` / NA | `part_domain` (`mechanical`, `electronics_electrical`, `control_loop`) | — |
| `interface` | `description` (Q); `dependency` (S, value `null`); `dependency_note` (Q) | `SubsystemInterface.provenance` / `.validation_state` / NA on `description`; NA on the dependency slots | refs `[part_a, part_b]`; `dependency` tokens `dependency_kind` (`one_way` / `mutual`), `dependent_part`, `depends_on_part` (item keys; one-way only) | no declaration → `dependency` and `dependency_note` `NOTHING_RECORDED`; declaration without note → `dependency_note` `NOTHING_RECORDED`; any read failure refuses (§3.4) |
| `unresolved_gap` | `gap_state` (S, value `null`), source owner `GAP_LIFECYCLE` (the reconstructed state's gap lifecycle, `state.gaps`) | NA / NA / NA (`Gap` holds no provenance, validation-state or currency field; an unresolved gap holds no `resolution_source`) | `gap_state` tokens `gap_type`, `gap_status` (`OPEN` / `PARTIAL`) | — |
| `declared_contradiction` | `declaration` (S, value `null`), source owner `LEDGER`; `answer_a`, `answer_b` (Q) = endpoint `content` | `declaration`: the `contradiction_declared` record's own provenance / validation / currency; each answer: its endpoint record's provenance / validation / currency | `declaration` token `active: true`; ref to the matching field-29 row | — |
| `declared_contradiction_history` | `declaration` (S, value `null`), source owner `LEDGER`; `answer_a`, `answer_b` (Q) | as `declared_contradiction` | `declaration` token `active: false` | — |
| `assumption` | `text` (Q) = record `content` (every `provisional_assumption` record, ledger order) | record provenance / validation / currency | `gap_type` (= `gap_context`); ref to the item of its immediate successor (`superseded_by`): a `provisional_assumption` successor → its field-16 `assumption` item; an `answered` successor that is still active (the only answer of its chain) → the field-29 row(s) canonically representing that answer (§7: its own `assertion` row, or the `active_contradiction` row(s) naming it); an `answered` successor that was itself corrected → its field-26 `correction_version` item; no successor → `[]` | — |
| `acknowledged_unknown` | `text` (Q) = `verbatim` | NA / NA / NA | `gap_type` (= `gap_context`) | — |
| `recorded_unknown` | `unknown_disposition` (S, value `null`), source owner `LEDGER` (every ACTIVE `unknown`-disposition record, ledger order) | the record's own provenance / validation / currency | `unknown_disposition` tokens `disposition` (`unknown`), `gap_type` (= `gap_context`); ref to the field-29 row(s) canonically representing the record (§7) | — |
| `routed_specialist_need` | `routed_need` (S, value `null`), source owner `NEED_ROUTING` | `NeedRoutingRevision.provenance` / NA / NA (the revision holds no validation-state or currency field) | `routed_need` tokens `gap_type`, `required_input` (`SPECIALIST` only, per the workstream contract's "routed specialist needs"); ref to the field-29 routing row | — |
| `gap_reference` | none (REFERENCE-ONLY, §8.1) | inherited from the referenced `gap_state` slot | ref to the field-15 `unresolved_gap` item | — |
| `evidence_reference` | `cap11_form` → `EXCLUDED_FROM_FIRST_SLICE`, reason `FORM_ROW_QUALITY_DERIVED` (REFERENCE-ONLY, §8.1) | inherited from the referenced `text` slot: the CAP-11 Source and Validation rows are its provenance and validation_state, which the HTML shows inside this item's container as two separate rows | ref to `problem_addressed.1` or `technical_concept.1` | one item per present Evidence; none → field `NOTHING_RECORDED` |
| `experiment` | `title` (S); `objective` (S, or `EXCLUDED_FROM_FIRST_SLICE` reason `OBJECTIVE_NAMES_EVIDENCE_LEVEL`, §6); `what_to_observe` (S); `success_criterion` (Q); `measurement_method` (Q); `test_hypothesis` (Q); `test_variable` (Q); `execution_state` (S, value `null`) | planning slots: provenance = the item's `*_provenance` token; others NA | `execution_state` tokens `state` (`none` / `recorded`), `count` | `success_criterion_status == "required"` → `NOTHING_RECORDED`; an absent method / hypothesis / variable → `NOTHING_RECORDED`; any planning or execution read failure refuses (§3.4) |
| `correction_version` | `text` (Q) = record `content` | record provenance / validation / currency | `chain`, `position` (1-based), `gap_type`, `disposition` (the record's own disposition, e.g. `answered`); ref: the first member of an assumption-origin answered segment → the field-16 `assumption` item it supersedes; otherwise `[]` | — |
| `requirement` | per §7 | per §7 | `anchor_kind`; refs per §7 | per §7 |
| `requirement_quantity` | `value_text` (Q) = `RequirementQuantity.value_text`, verbatim and opaque | `RequirementQuantity.provenance` / `.validation_status` / NA | `quantity_kind` (the owner's six closed tokens); `active`, `anchor_active` (the owner's booleans); ref: `anchor_active` true → the field-29 row canonically representing the anchoring answer (§7), which is always that answer's own `assertion` row resolved by `requirement_id` identity — the owner sets `anchor_active` only for an anchor the Landscape derives as an `assertion` row, and classifies an anchor represented only by an `active_contradiction` row as invalid (`QuantityHistoryError`, below); `anchor_active` false → `[]` (the owner derives no Landscape row for a withdrawn answer) | owner holds no row → field 12 per §8.2; `QuantityHistoryError`, or an `anchor_active` row whose field-29 item does not resolve, refuses (§3.4) |

Selection rules, all by owner tokens:

- `unresolved_gap`: every `state.gaps` entry with status `OPEN` or `PARTIAL`, in state order. `gap_reference` items
  (fields 17 and 24) point to these, one each.
- Declared contradictions: every `contradiction_declared` record in ledger order; `active` if its endpoint pair is in
  `active_declared_contradiction_pairs`, otherwise history. Legacy undeclared edges are not Owner-declared and appear
  only through the Landscape.
- `correction_version` (Correction 02 — assumption-origin history). Chains are the ledger's own supersession chains
  over interaction-disposition records (`INTERACTION_DISPOSITIONS` minus `DECISION_ACTION_DISPOSITIONS`), followed only
  through `supersedes` / `superseded_by`; nothing is inferred from text.
  - A chain with no `provisional_assumption` record and two or more members: every member, positions 1..n (unchanged).
  - A chain with a `provisional_assumption` record is classified by the existing `classify_assumption_ancestry` on its
    head. `ANCESTRY_ASSUMPTION_ORIGIN` (one or more assumptions, then zero or more answers) is valid history: its
    `provisional_assumption` members are field-16 `assumption` items, and its answered segment — the `answered`
    records after the last assumption, each keeping its own disposition — is carried here as one chain, positions 1..n,
    whenever that segment has two or more members (assumption → answer A → corrected answer B gives A at position 1,
    `SUPERSEDED`, and B at position 2, `CURRENT`). A one-answer segment is not a correction; that answer is reached
    through the field-29 row(s) canonically representing it (§7). `ANCESTRY_MALFORMED` refuses (inconsistent source history), as reconstruction already
    does for such ledgers; valid multi-answer ancestry is never treated as corruption.
  - No record is relabelled: assumptions stay `assumption` items, answers stay answers in correction history, and no
    chain owner, lifecycle or persisted state is created.
  - Chain order = ledger order of each carried chain's first carried member.
- Field 18 carries the Section-2 evidence registry only (the resolved problem and the known mechanism, the evidence
  CAP-11 already describes with Source and Validation rows). See §11 for evidence owners not carried.
- `requirement_quantity`: every row of `requirement_quantities_meta(state)["rows"]` — the owner's canonical rows in
  `quantity_seq` order, with its `active` and `anchor_active` booleans — after the S22 history is assigned to the
  in-memory reconstructed state (§3.1 step 7). `value_text` is never parsed, unit-split, normalized, converted,
  calculated, typed or re-worded, and no numeric, unit or derived field exists. The owner's identifiers
  (`quantity_id`, `anchor_record_id`, `requirement_id`, `supersedes_quantity_id`, `event_key`) and recording facts
  (`quantity_seq`, `recorded_iteration`, `recorded_at`) are never exported; `requirement_id` is used only to resolve the
  field-29 reference.

## 9. Version 1 schema and JSON contract

### 9.1 Version identities and file names

- Disclosure schema version: `inventorai-disclosure/1`.
- Export format versions: JSON `inventorai-disclosure-json/1`; HTML `inventorai-disclosure-html/1`.
- File names (constant; no project id, no inventor text): `inventorai-disclosure-export-v1.json` and
  `inventorai-disclosure-export-v1.html`.

### 9.2 JSON top level (exactly five keys)

`content` (object), `content_digest` (`"sha256:"` + 64 lowercase hex), `disclosure_schema_version`,
`export_format_version`, `generated_at` (UTC `YYYY-MM-DDTHH:MM:SSZ`, from the clock at serialization; outside the
digest).

### 9.3 Content

`content` has exactly four keys:

- `disclaimers`: the eleven ordered objects `{"id": "D01".."D11", "en": <exact §10 English>, "ar": <§12 Arabic>}`
  (the conditional disclaimer `D12` is not emitted while field 14 is `NOT_CAPTURED`);
- `scope_label`: `{"en": ..., "ar": ...}`;
- `unavailable_notice`: `true` when any slot is `UNAVAILABLE`, else `false`;
- `fields`: the 29 field objects in §8.2 order.

Field object keys: `field`, `marker`, `reason` (token or `null`), `pointer` (field token or `null`), `items` (list;
empty unless `RECORDED`).
Item keys: `item_key` (`<field token>.<n>`, 1-based), `kind`, `tokens` (object, closed keys), `refs` (list of item
keys), `slots` (object: slot token → value object).
Value object keys: `marker`, `reason`, `content_class`, `value`, `tokens`, `source_owner`, `envelope`. For a marker
other than `RECORDED`, `content_class`, `value`, `source_owner` and `envelope` are `null` and `tokens` is `{}`.
Envelope keys: `provenance`, `validation_state`, `limitation`, `currency`, each `{"marker", "value"}` (§8.1).

Closed token sets:

- markers: `RECORDED`, `NOTHING_RECORDED`, `NOT_CAPTURED`, `RAW_TEXT_ONLY`, `EXCLUDED_FROM_FIRST_SLICE`,
  `NOT_APPLICABLE`, `UNAVAILABLE`;
- content classes: `SYSTEM_ASSERTION`, `QUOTED_INVENTOR_CONTENT`;
- reasons: `NON_INTEGRATED_PROJECT`, `PLANNING_INPUTS`, `CONFIDENTIAL_EVIDENCE_CATEGORIES`, `RESULT_TEXT_NOT_CARRIED`,
  `CARRIED_ON_EVERY_ITEM`, `NO_APPROVAL_RECORD`, `FORM_ROW_QUALITY_DERIVED`, `OBJECTIVE_NAMES_EVIDENCE_LEVEL`;
- source owners: `SECTION2_RESOLUTION`, `LEDGER`, `SUBSYSTEM_COMPOSITION`, `INTERFACE_DEPENDENCY`,
  `ACKNOWLEDGED_UNKNOWNS`, `NEED_ROUTING`, `GAP_LIFECYCLE`, `REQUIREMENT_LANDSCAPE`, `REQUIREMENT_QUANTITY`,
  `PROTOTYPE_TEST_PLAN`,
  `PLANNING_METADATA`, `EXPERIMENT_RESULTS`, `DISCLOSURE_EXPORT` (the export's own fixed text; used only for the
  `capture_limitation` slot);
- item kinds: the seventeen kinds of §8.3;
- slot tokens: `text`, `name`, `function`, `description`, `dependency`, `dependency_note`, `answer_a`, `answer_b`,
  `part_a`, `part_b`, `label`, `status`, `resolving_action`, `statement`, `cap11_form`, `title`, `objective`,
  `what_to_observe`, `success_criterion`, `measurement_method`, `test_hypothesis`, `test_variable`, `execution_state`,
  `value_text`, `capture_limitation`, `gap_state`, `routed_need`, `unknown_disposition`, `declaration`;
- token keys: `part_domain`, `gap_type`, `gap_status`, `active`, `anchor_active`, `quantity_kind`, `dependency_kind`,
  `dependent_part`, `depends_on_part`, `required_input`, `disposition`, `anchor_kind`, `chain`, `position`, `state`,
  `count`;
- `quantity_kind` values: exactly the owner's `QUANTITY_KINDS` (`target_value`, `minimum_value`, `maximum_value`,
  `range`, `count`, `other_quantity`);
- the field tokens of §8.2.

No internal identifier (record id, subsystem id, interface id, experiment id, question id, quantity id, event key,
requirement id, project id, account id, routing reference) and none of the workstream contract §8 data appears anywhere
in `content`.

### 9.4 Serialization

- Canonical serialization (digest input) and digest:

  ```python
  canonical = json.dumps(content, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":"), allow_nan=False).encode("utf-8")
  content_digest = "sha256:" + hashlib.sha256(canonical).hexdigest()
  ```

- File serialization, UTF-8 without BOM, served as `application/json; charset=utf-8`:

  ```python
  body = json.dumps(top_level, sort_keys=True, ensure_ascii=False, indent=2,
                    separators=(",", ": "), allow_nan=False) + "\n"
  ```
- Ordering: object keys sorted; list order is the owner order fixed in §8.
- Escaping and round trip: standard JSON escaping only; every quoted value decodes to exactly the owner-held string (no
  normalization, trimming, case change or translation). A value that cannot be encoded as UTF-8 refuses the export.

### 9.5 Determinism

The same snapshot and the same versions yield byte-identical `content` and digest in every locale. Only
`generated_at` varies. No randomness, clock or network input reaches `content`.

### 9.6 Schema check and unknown keys

Before serialization the module validates the finished projection against §9.2–§9.3: an unknown key, token, marker,
reason or kind refuses the export (global schema failure). The check also refuses when a `requirement_quantity` item
carries any slot or token outside §8.3 (so no parsed, numeric, unit or calculated field can be emitted), when a
`resolved_problem` item lacks its `capture_limitation` slot or that slot's value differs from the exact §12.6 English
text, or when any ref does not name an existing item key. It also refuses (Correction 02) when a `RECORDED` item of a
truth-bearing kind has no `RECORDED` slot with `content_class`, `source_owner` and a four-field envelope; when a
reference-only item (`gap_reference`, `evidence_reference`) has a `RECORDED` slot of its own or not exactly one ref to
an item of the kind §8.1 names; or when an item-level token is not one §8.1 allows. The module never emits an unknown
key. A v1 reader rejects unknown keys.

## 10. Self-contained HTML contract

- Rendered by one template from the finished projection plus the locale, `generated_at` and the digest; it reads no
  store, state or request data beyond the locale. It adds no substantive content: every substantive value comes from the
  projection; the only other text is fixed chrome (headings, labels, marker and reason wording, retention lines) from
  existing label owners (§2.2 S17–S21) or new `UI_S35_*` keys (§12).
- Self-contained: `<!doctype html>`, `<meta charset="utf-8">`,
  `<meta name="viewport" content="width=device-width, initial-scale=1">` (Correction 04, C4), one inline `<style>` and
  this policy meta element:

  ```html
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'none'; style-src 'unsafe-inline'; img-src 'none'; base-uri 'none'; form-action 'none'">
  ```

  No `<script>`, event-handler attribute, `<link>`, `<img>`, `<iframe>`, `<object>`, `<form>`,
  external URL, web font, tracker or `javascript:` URL. In-document fragment links (`#<item_key>`) are allowed.
- Escaping: autoescape on; no projection value ever passes through `|safe`; attribute values come only from closed
  tokens.
- Locale: `<html lang="en" dir="ltr">` or `<html lang="ar" dir="rtl">`, from the UI locale at download. In the Arabic
  locale every exact English disclaimer stays present, each followed by its Arabic supplement; the scope label shows
  English and Arabic. English digits for versions, dates, counts and item keys. In the Arabic document every exact
  English fixed-text element — each English disclaimer, the English scope label and the English `capture_limitation` —
  sits in its own element with `lang="en" dir="ltr"` (C4).
- Order: scope label; versions, `generated_at`, digest; the disclaimers; the optional `UNAVAILABLE` sentence; the one
  fixed "How to read this document" block (§12.9, C3); the 29 fields in §8.2 order, each with its heading and either
  its marker wording (+ reason, + pointer) or its items. Field 24 (Risks) always carries the fixed §12.10 clarification
  directly under its heading, whatever its marker (C3).
- Every value sits in its own direction-isolated container (`dir="auto"`, `<bdi>` for inline values) with
  `white-space: pre-wrap` and `overflow-wrap: anywhere` (C4), so a long unbroken value wraps inside its container and
  never forces horizontal page overflow at phone width; nothing is trimmed or normalized, and wrapping changes only the
  display, never the value. Labels sit outside the `dir="auto"` value element.
- **Page-level wrapping (Correction 05, R-C4).** `overflow-wrap: anywhere` also applies at the document `body` level, so
  the header's content digest (`sha256:` + 64 lowercase hex), the disclosure-schema and export-format version
  identifiers and every other long generated string wrap within the viewport; `white-space: pre-wrap` stays on
  projection values only. The digest and version strings are emitted unchanged — no soft hyphen, zero-width or other
  character is inserted — so selecting and copying the digest yields the exact original; wrapping is presentation
  only. A quoted value carries the adjacent label "Inventor's own
  words"; a system value carries "InventorAI statement". The Source and Validation labels (CAP-11 `UI_ED_*`), the
  currency label and any marker wording sit inside the same item container, next to the value they describe.
- **Attribution invariant (Correction 02).** For every truth-bearing item, each `RECORDED` slot — a value-`null`
  `SYSTEM_ASSERTION` slot such as `gap_state`, `routed_need`, `unknown_disposition`, `declaration` or `execution_state`
  included, which renders through its existing label owners (§2.2 S11, S18, S20, S21) or the label of its referenced
  field-29 row — shows inside the item container its content-class label and its Source, Validation and Limitation
  rows (the owner-held value's label, or, for `NOT_APPLICABLE`, that row's fixed §12.8 contextual wording — C2), plus
  Currency when that is `RECORDED`. A reference-only item shows its link and, next to it, the rows inherited from the referenced slot,
  labelled as belonging to that target. No row is ever filled with a default.
- The `resolved_problem` item shows its `capture_limitation` inside the same item container, directly after the problem
  text, labelled "InventorAI statement": the exact English text, followed in the Arabic locale by its §12.6 Arabic
  supplement. It is shown whatever the problem text is.
- A `requirement_quantity` item shows the quoted `value_text` exactly as held (never split, reformatted, unit-styled or
  aligned as a number), its kind label (`UI_T2A_KIND_<TOKEN>`), the Source / Validation labels, the owner's chain state
  through the existing T2-A labels (`UI_T2A_CURRENT` when `active`, `UI_T2A_REPLACED` when not; `UI_T2A_WITHDRAWN_ANCHOR`
  with `UI_T2A_WITHDRAWN_NOTE` when `anchor_active` is false) and, when it has one, a `#<item_key>` link to its field-29
  row.
- Canonical English system statements stay English in both locales (Stage 34 rule) and are direction-isolated.
- **Neutral export labels (Correction 04, C1; workstream contract §4 rule 4 exception).** Where §12.7 defines a
  Stage-35 label, it replaces, in this HTML only, the reused label named in §2.2 (S17, S20, S24) for the same token or
  state; the reused label and every other surface stay unchanged, and the JSON emits the same tokens as before.

## 11. Existing owners not read by the first slice

Workstream contract §5: "A source without a row in that table is not read." The following owners exist at this base,
hold project information near a disclosure field and are NOT read. None is added here; adding any of them needs a
workstream-contract correction and an Owner decision. (T2-A requirement quantities are no longer in this list: OD-A
carries them through S22 / S23, workstream contract Correction 04.)

| Owner | Nearest disclosure field | Snapshot admission today | Final disposition |
|---|---|---|---|
| Stage 15 Slice 4 interface observations (`engine/interface_observation.py`; `load_interface_observations`) | 22 / 23 (prototype status and validation results) | REFUSED (carrying them would need a seventh R1 reader, beyond Correction 03) | **OD-B: intentionally omitted from the first slice.** No seventh reader is added. Interface observations are the inventor's own unvalidated records, not validation results; the omission makes no existing field or marker false — field 23 stays `NOT_CAPTURED` and field 22 stays `EXCLUDED_FROM_FIRST_SLICE` for result text. |
| Stage-3 reasoning-gap evidence (`Gap.evidence`, report Section 9) and Section-2 `known_boundaries` | 18 (technical evidence) | in reconstructed state | **OD-C: not added to field 18.** Field 18 stays as mapped (the CAP-11-described Section-2 evidence only); these owners are not relabelled as technical evidence and ledger content is not duplicated under a broader evidence label. No implementation seam is added. |
| T2-E owner-recorded evidence references (`engine/evidence_reference.py`) | 18 | admitted | Not evidence by its owner's own definition; omission consistent. |
| CAP-08 dependency edges (`assumption_dependency_declared`) | 16 | in ledger | Assumptions carried without their declared dependent answers. |
| Control-loop part answers (`PartAnswer`, `subsystem_part_answers`) | 6 / 7 | not checked | Part name and function carried; part answers not. |
| CAP-05 / CAP-07 decision records | 10 | in ledger | Never relabelled as embodiments (workstream contract §7). |
| Stale planning values (`stale_*` of Section 11) | 21 | via package | Current experiments only, as Stage 19. |

Two further limitations the reviews must see:

- **OD-D (final).** The Section-2 problem value is the owner-held value the existing resolution boundary selects —
  usually `state.idea_summary`, which the capture step trims at 500 characters at a word boundary and ends with a
  system-appended "…" (`engine/progression_loop.py` `_trim_idea_summary`). The export keeps that boundary, reproduces
  the value exactly as `QUOTED_INVENTOR_CONTENT` and adds the unconditional §12.6 problem-capture limitation (workstream
  contract §6, Correction 04). `state.known_problem` is not read; truncation is not detected from the text and missing
  content is not reconstructed.
- Ledger content is exported as quoted inventor content for every record; the record's own provenance token
  (`OWNER_STATED` or `LEGACY_UNSPECIFIED`) states its origin.

## 12. Fixed wording (English and Arabic)

The English disclaimers, scope label and the reasons quoted from the workstream contract are exact; the Arabic wording
supplements them and is meaning-preserving. Inventor-authored content is never translated; source-owned technical
statements are never altered for this export.

### 12.1 Scope label

- EN (exact): "Invention disclosure export — this project only — not legal advice"
- AR: "تصدير الإفصاح عن الاختراع — هذا المشروع فقط — ليس استشارة قانونية"

### 12.2 Disclaimers (EN exact, workstream contract §10; AR supplement)

| Id | Arabic supplement |
|---|---|
| D01 | هذه الوثيقة ليست استشارة قانونية، ولا يقدّم InventorAI خدمات قانونية. |
| D02 | هذه الوثيقة ليست رأيًا بشأن قابلية الاختراع للحصول على براءة. لم يقيّم InventorAI ما إذا كان هذا الاختراع جديدًا أو ينطوي على خطوة ابتكارية أو قابلًا للحصول على براءة. |
| D03 | هذه الوثيقة ليست بحثًا في التقنية السابقة (prior art). لم يبحث InventorAI عن التقنية السابقة ولم يؤكد خلوّ الطريق منها. |
| D04 | هذه الوثيقة ليست رأيًا بشأن حرية الاستغلال (freedom to operate). |
| D05 | هذه الوثيقة ليست طلب براءة اختراع جاهزًا للإيداع. |
| D06 | لم يصِغ InventorAI أي مطالبة براءة (patent claim) في هذه الوثيقة ولم يولّدها. أي صياغة تشبه المطالبات لا ترد إلا داخل نص منقول عن المخترع، مُستنسَخ كما كُتب ودون تقييم. لا شيء في هذه الوثيقة مطالبة صالحة قانونيًا. |
| D07 | الأدلة المسجّلة هنا ليست استنتاجًا متحقَّقًا منه. العناصر الموسومة بأنها غير متحقَّق منها لم يتحقق منها InventorAI. |
| D08 | لا تُثبت هذه الوثيقة تاريخ تصوّر الاختراع ولا تاريخ الاختراع ولا الأسبقية ولا صفة المخترع ولا الملكية. |
| D09 | أي بصمة رقمية (digest) أو تاريخ في هذه الوثيقة أداة للتحقق من سلامة المحتوى فقط، وليس ختمًا زمنيًا قانونيًا ولا توثيقًا رسميًا ولا دليلًا على الأسبقية. |
| D10 | قد تُعدّ مشاركة هذه الوثيقة إفصاحًا عن الاختراع في بعض الولايات القضائية. استشر مختصًا مؤهلًا في البراءات قبل مشاركتها. |
| D11 | للحصول على استشارة قانونية، استشر مختصًا مؤهلًا في البراءات. |
| D12 (conditional; not emitted in v1) | عبارات الجِدّة والتمايز الواردة هنا هي كلمات المخترع نفسه، ولم يقيّمها InventorAI. |

### 12.3 Marker wording

| Marker | EN (exact, workstream contract §5) | AR |
|---|---|---|
| `NOTHING_RECORDED` | Nothing recorded in this project | لا شيء مسجّل في هذا المشروع |
| `NOT_CAPTURED` | Not captured by InventorAI | لا يلتقط InventorAI هذه المعلومة |
| `RAW_TEXT_ONLY` | Only as the inventor's own wording in + section | فقط بصياغة المخترع نفسه في + القسم |
| `EXCLUDED_FROM_FIRST_SLICE` | Not included in this export | غير مُضمَّن في هذا التصدير |
| `NOT_APPLICABLE` | Not applicable | لا ينطبق |
| `UNAVAILABLE` | Unavailable — this information could not be read | غير متاح — تعذّرت قراءة هذه المعلومة |
| top sentence | One or more sections of this document could not be read and are marked Unavailable. | تعذّرت قراءة قسم أو أكثر من هذه الوثيقة، ووُسِم بأنه غير متاح. |

### 12.4 Reasons

| Reason | EN | AR |
|---|---|---|
| `NON_INTEGRATED_PROJECT` | In this first slice, InventorAI captures component descriptions only for integrated Mechanical + Electrical / Electronics projects. (exact) | في هذه الشريحة الأولى، لا يلتقط InventorAI أوصاف المكوّنات إلا للمشاريع المتكاملة التي تجمع جزءًا ميكانيكيًا وجزءًا كهربائيًا / إلكترونيًا. |
| `NO_APPROVAL_RECORD` | InventorAI holds no inventor-approval record; this is not a statement that approval was withheld. (exact) | لا يحتفظ InventorAI بأي سجل لموافقة المخترع، وهذا لا يعني أن الموافقة حُجبت. |
| `FORM_ROW_QUALITY_DERIVED` | Excluded from this first slice because the Form row is derived from the evidence-quality field, and this disclosure export does not carry evidence-quality grades. (exact) | مُستبعَد من هذه الشريحة الأولى لأن صف «الصيغة» مشتق من حقل جودة الدليل، وهذا التصدير لا يحمل درجات جودة الأدلة. |
| `OBJECTIVE_NAMES_EVIDENCE_LEVEL` | Excluded from this first slice because this generated objective names an evidence-quality level, and this disclosure export does not carry evidence-quality grades. (exact, workstream contract §7) | مُستبعَد من هذه الشريحة الأولى لأن هذا الهدف المولَّد يذكر مستوى جودة الدليل، وهذا التصدير لا يحمل درجات جودة الأدلة. |
| `PLANNING_INPUTS` | Excluded from this first slice because these are planning inputs for checking an interaction between parts, not a description of the invention. | مُستبعَد من هذه الشريحة الأولى لأن هذه مدخلات تخطيط للتحقق من تفاعل بين الأجزاء، وليست وصفًا للاختراع. |
| `CONFIDENTIAL_EVIDENCE_CATEGORIES` | Excluded from this first slice because commercial, manufacturing and integration evidence can be confidential. | مُستبعَد من هذه الشريحة الأولى لأن الأدلة التجارية وأدلة التصنيع والتكامل قد تكون سرية. |
| `RESULT_TEXT_NOT_CARRIED` | Excluded from this first slice: this export shows whether the inventor recorded executions, not the text of the recorded results. | مُستبعَد من هذه الشريحة الأولى: يُظهر هذا التصدير ما إذا كان المخترع قد سجّل تنفيذات، لا نص النتائج المسجّلة. |
| `CARRIED_ON_EVERY_ITEM` | Not applicable as a separate section: each item in this document carries its own source, validation and limitation details. | لا ينطبق كقسم مستقل: يحمل كل عنصر في هذه الوثيقة تفاصيل مصدره والتحقق منه وقيوده. |

### 12.5 Journey, retention and document labels (`UI_S35_*`)

| Purpose | EN | AR |
|---|---|---|
| Account-page link | Invention disclosure export | تصدير الإفصاح عن الاختراع |
| Page intro | This export describes your invention using only what you have recorded in this project, with its source and validation details. Read the notices below before downloading. | يصف هذا التصدير اختراعك باستخدام ما سجّلته في هذا المشروع فقط، مع تفاصيل المصدر والتحقق. اقرأ التنبيهات أدناه قبل التنزيل. |
| Notices heading | Before you download | قبل التنزيل |
| JSON control | Download machine-readable file (JSON) | تنزيل الملف المقروء آليًا (JSON) |
| HTML control | Download readable document (HTML) | تنزيل المستند المقروء (HTML) |
| Same-data line | The readable document is generated from the same data as the machine-readable file and adds nothing to it. | يُولَّد المستند المقروء من البيانات نفسها التي في الملف المقروء آليًا، ولا يضيف إليها شيئًا. |
| Retention heading | What InventorAI keeps | ما يحتفظ به InventorAI |
| Retention 1 | InventorAI keeps no copy of this export file. Each download is composed when you request it. | لا يحتفظ InventorAI بأي نسخة من ملف التصدير هذا؛ يُنشأ كل تنزيل عند طلبك له. |
| Retention 2 | InventorAI creates no record of your exports. Ordinary access logs, which do not contain your invention content, may still record the request. | لا ينشئ InventorAI سجلًا لعمليات التصدير التي تجريها. وقد تسجّل سجلات الوصول الاعتيادية الطلب، وهي لا تتضمن محتوى اختراعك. |
| Retention 3 | InventorAI cannot delete copies you have downloaded. | لا يستطيع InventorAI حذف النسخ التي نزّلتها. |
| Retention 4 | Creating this export does not change your project. | إنشاء هذا التصدير لا يغيّر مشروعك. |
| Quoted label | Inventor's own words | كلمات المخترع كما كتبها |
| System label | InventorAI statement | عبارة من InventorAI |
| Current | Current | حالي |
| Superseded | Earlier version, kept as history | نسخة سابقة محفوظة ضمن السجل |
| Reference | See | انظر |
| Versions | Disclosure schema version / Format version | إصدار مخطط الإفصاح / إصدار التنسيق |
| Generated | Generated (UTC) | وقت الإنشاء (UTC) |
| Digest | Content digest | البصمة الرقمية للمحتوى |

Field headings (EN / AR), §8.2 order: Invention title / عنوان الاختراع; Problem addressed / المشكلة التي يعالجها;
Background and existing limitations / الخلفية والقيود القائمة; Invention objective / هدف الاختراع; Technical concept /
المفهوم التقني; Parts of the invention / أجزاء الاختراع; Other system, component, process and method descriptions /
أوصاف أخرى للنظام والمكوّنات والعمليات والطرق; Relationships between parts / العلاقات بين الأجزاء; Operating sequence or
workflow / تسلسل التشغيل أو سير العمل; Alternative embodiments / التجسيدات البديلة; Materials, dimensions, parameters
and operating conditions as typed values / المواد والأبعاد والمعاملات وظروف التشغيل كقيم محدَّدة النوع; Materials,
dimensions, parameters and operating conditions in the inventor's own wording / المواد والأبعاد والمعاملات وظروف التشغيل بصياغة المخترع;
Interface verification-preparation inputs / مدخلات التحضير للتحقق من التفاعل بين الأجزاء; Novelty and differentiation
statements / عبارات الجِدّة والتمايز; Unresolved technical issues / المسائل التقنية غير المحسومة; Assumptions /
الافتراضات; Missing information / المعلومات الناقصة; Technical evidence / الأدلة التقنية; Commercial, manufacturing and
integration evidence / الأدلة التجارية وأدلة التصنيع والتكامل; Diagrams and files / الرسومات والملفات; Proposed
experiments and their execution state / التجارب المقترحة وحالة تنفيذها; Text of recorded experiment results / نص نتائج
التجارب المسجّلة; Validation results / نتائج التحقق; Risks / المخاطر; Uncertainty and abstentions / عدم اليقين والامتناع
عن الحكم; Inventor's corrections / تصحيحات المخترع; Inventor approvals / موافقات المخترع; Source and provenance references / مراجع
المصدر والأصل; Requirement Landscape (existing `UI_B_DELIV_036`).

### 12.6 Problem-capture limitation (`capture_limitation` slot; OD-D)

Unconditional on every `resolved_problem` item. It states a possibility only: it never states that shortening
occurred, and it is never chosen, varied or omitted by inspecting the problem text.

- EN (exact, workstream contract §6; the slot value): "InventorAI captures the problem statement at the step where the
  inventor describes the problem and may shorten it at a 500-character limit. The text shown here may therefore have
  been shortened; an ellipsis (…) at its end may indicate that shortening."
- AR (supplement, a new `UI_S35_*` key; HTML only): "يُلتقَط بيان المشكلة في الخطوة التي يصف فيها المخترع المشكلة، وقد
  يُختصَر عند حدّ 500 حرف. لذلك قد يكون النص المعروض هنا مختصرًا، وقد تدلّ علامة الحذف (…) في نهايته على هذا الاختصار."

### 12.7 Neutral export labels (Correction 04, C1; new `UI_S35_*` keys; HTML only)

The downloaded document may be read by people other than the inventor, so its Stage-35-authored copy never addresses
the reader as the inventor. Existing owner-held statements keep their canonical wording; where they say "you" or
"your", the §12.9 legend explains it (Correction 05, R-C1). These keys replace, in the disclosure HTML only, the reused labels named; the reused keys, every other surface
and every JSON token are unchanged. The neutral field headings 12 and 26 and the neutral `RESULT_TEXT_NOT_CARRIED`
reason are fixed in §12.4 and §12.5. The pre-download page (§13) is addressed to the signed-in inventor and keeps its
second-person wording.

| Purpose | Replaces in the HTML | EN | AR |
|---|---|---|---|
| Source label, `OWNER_STATED` | `UI_ED_SOURCE_OWNER_STATED` ("You" / "أنت") | Inventor | المخترع |
| Source label, Section-11 planning provenance `user_defined` | — (no existing label) | Inventor | المخترع |
| Source label, Section-11 planning provenance `source_stated` | — (no existing label) | Taken from the inventor's recorded text | مأخوذ من نص المخترع المسجّل |
| Withdrawn-answer note (`anchor_active` false) | `UI_T2A_WITHDRAWN_NOTE` | The answer this value was attached to has been withdrawn. The value is kept in the project history and is no longer current. | سُحبت الإجابة التي كانت هذه القيمة مرتبطة بها. تُحفظ القيمة في سجل المشروع ولم تعد حالية. |
| Execution state `none` | `web/app.py` `S11_EXECUTION_TEXT` (none) | No result recorded. | لا توجد نتيجة مسجّلة. |
| Execution state `recorded` | `web/app.py` `S11_EXECUTION_TEXT` (recorded) | The inventor recorded {n} execution(s). These are the inventor's own recorded observations. InventorAI has not checked them and they are not a pass/fail judgement. | عدد التنفيذات التي سجّلها المخترع: {n}. هذه ملاحظات سجّلها المخترع بنفسه، ولم يتحقق منها InventorAI، وليست حكمًا بالنجاح أو الإخفاق. |

Every other source and validation token keeps its existing `UI_ED_*` label, which is already neutral.

### 12.8 Envelope `NOT_APPLICABLE` context (Correction 04, C2)

Shown in a truth-bearing item's Source, Validation, Limitation or Currency row when that envelope field is
`NOT_APPLICABLE` (§10 attribution invariant). The JSON marker stays `NOT_APPLICABLE`, and the field-level marker
wording "Not applicable" (§12.3) is unchanged. Each sentence states only that no separate value is held; none implies
that the item is validated, unlimited, approved or complete, or that a source or validation is unnecessary.

| Row | EN | AR |
|---|---|---|
| Source | No separate source value is held for this item. This does not mean the item has no source. | لا توجد قيمة مصدر مستقلة محفوظة لهذا العنصر. ولا يعني ذلك أن العنصر بلا مصدر. |
| Validation | No separate validation value is held for this item. This does not mean the item was validated or that validation is unnecessary. | لا توجد قيمة تحقق مستقلة محفوظة لهذا العنصر. ولا يعني ذلك أنه جرى التحقق منه أو أن التحقق غير لازم. |
| Limitation | No separate limitation note is held for this item. This does not mean the item has no limitations. | لا توجد ملاحظة قيود مستقلة محفوظة لهذا العنصر. ولا يعني ذلك أن العنصر بلا قيود. |
| Currency | No separate current-or-earlier status is held for this item. | لا توجد حالة مستقلة محفوظة تبيّن ما إذا كان هذا العنصر حاليًا أو سابقًا. |

Under the unchanged §10 invariant the Currency row is rendered only when `RECORDED`, so the Currency sentence is defined
for completeness and is not shown in version 1.

### 12.9 "How to read this document" (Correction 04, C3; workstream contract §13)

ONE fixed block, after the disclaimers (and the optional `UNAVAILABLE` sentence) and before field 1. It uses the
existing content-class labels (§12.5) and marker wording (§12.3) and their workstream §5 meanings; it adds no marker,
conclusion or assessment.

EN:

- Heading: "How to read this document"
- "Each section shows either the items InventorAI holds for this project or one status."
- "“Inventor's own words”: text quoted exactly as the inventor recorded it. InventorAI has not checked or assessed it."
- "“InventorAI statement”: fixed or system-generated wording from InventorAI."
- "When an existing InventorAI statement uses “you” or “your”, it refers to the inventor who recorded this project."
  (Correction 05, R-C1: explanatory only; the owner-held statements are not rewritten.)
- "Items listed: records InventorAI holds for this project. Each item shows its source and validation details."
- "“Nothing recorded in this project”: InventorAI holds no record of this in this project. It does not mean that none
  exists."
- "“Not captured by InventorAI”: InventorAI does not capture this kind of information."
- "“Only as the inventor's own wording in …”: this information appears only inside the inventor's own text in the named
  section. It has not been separated out or interpreted."
- "“Not included in this export”: InventorAI holds related information, but this first export deliberately leaves it
  out, for the reason shown."
- "“Not applicable”: the section does not apply to this kind of item. Next to an item, a detail that is not held is
  explained in place; this never means that the item has no limitations."
- "“Unavailable — this information could not be read”: the information could not be read when this document was
  created."

AR:

- العنوان: «كيفية قراءة هذه الوثيقة»
- «يعرض كل قسم إما العناصر التي يحتفظ بها InventorAI لهذا المشروع، وإما حالة واحدة.»
- «"كلمات المخترع كما كتبها": نص منقول حرفيًا كما سجّله المخترع، ولم يتحقق منه InventorAI ولم يقيّمه.»
- «"عبارة من InventorAI": صياغة ثابتة أو مولَّدة من InventorAI.»
- «عندما تستخدم عبارةٌ قائمةٌ من InventorAI كلمتَي "أنت" أو "لك"، فإنها تشير إلى المخترع الذي سجّل هذا المشروع.»
- «العناصر المدرجة: سجلات يحتفظ بها InventorAI لهذا المشروع، ويعرض كل عنصر تفاصيل مصدره والتحقق منه.»
- «"لا شيء مسجّل في هذا المشروع": لا يحتفظ InventorAI بأي سجل لذلك في هذا المشروع، ولا يعني ذلك أنه غير موجود.»
- «"لا يلتقط InventorAI هذه المعلومة": لا يلتقط InventorAI هذا النوع من المعلومات.»
- «"فقط بصياغة المخترع نفسه في …": ترد هذه المعلومة فقط داخل نص المخترع نفسه في القسم المذكور، ولم تُفصَل عنه ولم
  تُفسَّر.»
- «"غير مُضمَّن في هذا التصدير": يحتفظ InventorAI بمعلومات ذات صلة، لكن هذا التصدير الأول يستبعدها عمدًا للسبب المبيّن.»
- «"لا ينطبق": لا ينطبق هذا القسم على هذا النوع من العناصر. وإلى جانب كل عنصر، يُوضَّح في موضعه أي تفصيل غير محفوظ،
  ولا يعني ذلك أبدًا أن العنصر بلا قيود.»
- «"غير متاح — تعذّرت قراءة هذه المعلومة": تعذّرت قراءة هذه المعلومة عند إنشاء هذه الوثيقة.»

### 12.10 Risks clarification (Correction 04, C3; workstream contract §13)

Always shown directly under the field-24 heading, whatever its marker. Explanatory chrome only: field 24's mapping
(`gap_reference` items, §8.2) is unchanged and no severity, probability, score, ranking, classification or assessment
is added.

- EN: "This section references unresolved technical issues listed in this export. InventorAI has not performed a risk
  assessment here."
- AR: «يشير هذا القسم إلى المسائل التقنية غير المحسومة الواردة في هذا التصدير. لم يُجرِ InventorAI تقييمًا للمخاطر هنا.»

## 13. Routes and journey (frozen)

- Entry: one link per project row on the account page (`web/templates/account.html`).
- `GET /account/projects/<project_id>/disclosure-export`: the page. Order: scope label, intro, "Before you download"
  with the eleven disclaimers (EN exact; AR supplement after each in the Arabic locale), the two download controls, the
  same-data line, the retention block. Viewing records nothing.
- The two download routes, `GET /account/projects/<project_id>/disclosure-export/json` and
  `GET /account/projects/<project_id>/disclosure-export/html`, compose (§3) and answer `200` with
  `Content-Disposition: attachment; filename="<§9.1 name>"`, `Cache-Control: no-store` and
  `X-Content-Type-Options: nosniff`. The HTML response also carries
  `Content-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; sandbox`. Denial: `_deny_project()`.
  Refusal: a bare, empty 503.
- No other route, no POST, no API surface, no email, no cache, no temporary file, no log line with invention content.

## 14. BASE RED plan (future tests; none written by this document)

Each obligation must first fail on the implementation base, then pass. Files:
`tests/test_record_store_snapshot_admission.py` (R), `tests/test_stage35_disclosure_projection.py` (P),
`tests/test_stage35_disclosure_html.py` (H), `tests/test_stage35_disclosure_routes.py` (W),
`tests/test_stage35_extraction_invariance.py` (X).

| # | Requirement | File | Fails first because | Seam | Passes when | Protected invariant |
|---|---|---|---|---|---|---|
| 1 | §15.1 prohibited wording in system assertions | H, P | no projection | module + template | scan of every `SYSTEM_ASSERTION` value and all chrome, EN and AR, finds none outside the exact disclaimer allow-lists; quoted values located structurally by `content_class` | no affirmative legal / patent assertion |
| 2 | §15.2 disclaimers present and before the controls | H, W | no page | page + template | eleven EN disclaimers verbatim in JSON, HTML (both locales) and page; AR supplements in AR; all precede the download controls | §10 |
| 3 | §15.3 markers | P, H | no projection | field map | each marker renders its §12.3 wording; the section-local `UNAVAILABLE` case is #24; non-integrated project → fields 6–8 `NOT_CAPTURED` + reason, never `NOTHING_RECORDED`; no marker renders empty | §5 |
| 4 | §15.4 no external transfer | P | no module | module | import-graph and socket-blocking tests: no network call, no provider / API / e-mail import | §11 |
| 5 | §15.5 project separation and failure classes | W, P | no routes | routes + §3.4 | missing and foreign projects give byte-identical denials; a NULL-owner project is denied (the S1 split is #26); no record of another project appears; every refusal-class fault (unsafe connection, corrupt history, level 0, anchor defect, schema failure and every case of #23) returns 503 with no file | §4A |
| 6a | §15.6(a) one snapshot | P | no composer | §3.1 | instrumented store shows every source read, S22 included, between one SAVEPOINT and its RELEASE, R1 reads last | §4A |
| 6b | §15.6(b) concurrent commit | P | no composer | §3.1 | a second connection's commit attempted mid-composition never yields mixed state; the export equals the pre-commit state whether the commit waits or completes | §4A |
| 6c | §15.6(c) later snapshot | P | no composer | §3.1 | a second export after that commit reflects it | §4A |
| 6d | §15.6(d) acquisition / integrity failure | P | no composer | §3.1 steps 2, 3, 6 + R1 | unsafe connection, caller-owned transaction, no-op branch and a snapshot lost mid-composition each refuse | IR-01 |
| 6e | §15.6(e) no partial file | W | no routes | routes | every refusal returns an empty 503 | §4A |
| 6f | §15.6(f) IR-01 | R | guard absent | R1 | see R1–R12 below | IR-01 |
| 7 | §15.7 envelope fidelity | P, H | no projection | §8 | every `RECORDED` slot has class, owner and owner-held metadata; `NOT_APPLICABLE` where the owner holds none; no substitution; no approval field or line; HTML shows the metadata inside the item container | §5 |
| 8 | §15.8 excluded content absent | P, H | no projection | §8 | with every workstream §8 source populated (verdict, maturity, readiness snapshot, quality grades, Form row, severity, criticality + rationale, Grounded Risks, CAP-12, CAP-01 prose, safety signals, Commercial / Manufacturing / Integration evidence, internal ids) none appears; the `reasoned_leading_claim` objective is `EXCLUDED` | §8 |
| 9 | §15.9 known-problem seam | P | no projection | E1 | a state whose `known_problem` came from a mechanism answer exports the Section-2 resolved problem | RISK-002 |
| 10 | §15.10 no mutation | P, W | no composer | §3 | full store dump identical before and after compose and both downloads; no export-history row, file or cache entry | Decision 2 |
| 11 | §15.11 existing surfaces unchanged | X | extractions absent | E1–E4 | report HTML, PDF (existing harness normalization), canonical package minus `generated_at`, planning page, session page, Structured Export, self-service export and public API identical for the same fixtures before and after | §4 rule 2 |
| 12 | §15.12 determinism and versions | P | no projection | §9 | identical state → identical `content` and digest in EN and AR; digest excludes `generated_at`; both version ids present | §9 |
| 13 | §15.13 hostile inventor text | P, H | no projection | §9.4, §10 | markup, script, links, template syntax, bidi and control characters and very long values are escaped, never interpreted, stay next to their labels and round-trip exactly; e-mail-, token- and path-like inventor text is reproduced verbatim while no system-held metadata appears | §5, §8 |
| 14 | §15.14 both locales | H | no template | §10 | EN and AR documents both satisfy 1–3, 7 and 13 | §13 |
| 15 | §15.15 file names | W | no routes | §9.1 | file names are the two constants | §9 |
| 16 | §15.16 self-contained | H | no template | §10 | parser finds no external resource, script, handler or form | §11 |
| 17 | no DB reads after materialization | P | no composer | §3.1 step 5 | a store spy fails any call after the snapshot exits; serialization and HTML rendering succeed | Correction 03 |
| 18 | experiment slots | P | no projection | §5, §6 | allow-list only; planning classes per provenance token; `required` → `NOTHING_RECORDED` | §6 |
| 19 | Landscape classes | P | no projection | §7 | composed rows never exported as one string; parts resolved by identity; unresolvable anchor refuses | §5 |
| 20 | OD-A requirement quantities | P, H | no projection | S22, S23, §8.3 | (a) each owner row's `value_text` is carried verbatim as a `QUOTED_INVENTOR_CONTENT` `value_text` slot with the owner's `quantity_kind`, `active`, `anchor_active`, provenance and validation, in owner order; (b) values such as "12 V", "0.5–0.8 mm", "≈3 kg", "1,5 bar", "10^3 N" and "about 20" round-trip unchanged, and no parsed, numeric, unit, normalized, converted or calculated field exists anywhere in `content` (the §9.6 check refuses one); (c) an `anchor_active` row refs exactly the field-29 row canonically representing its anchoring answer (its own `assertion` row, §7), and a withdrawn-anchor row has `refs` `[]` and renders the existing withdrawn-answer note; (d) no field-29 item carries a quantity value, and each quantity value is emitted once; (e) field 12 is `RECORDED` when any row exists, `RAW_TEXT_ONLY` + pointer only when none exists and field 29 holds a quoted slot, otherwise `NOTHING_RECORDED`, and never renders the "Only as the inventor's own wording in" pointer wording while a row exists; (f) `QuantityHistoryError` and an `anchor_active` row whose field-29 item does not resolve each refuse | OD-A, workstream §6 |
| 21 | OD-D problem limitation | P, H | no projection | S3, §8.3, §12.6 | every `resolved_problem` item carries `capture_limitation` with the exact §12.6 English text, for a short text, a text of exactly 500 characters, a trimmed text ending in "…" and a text the inventor ended with "…" alike; the HTML shows it inside the problem item's container directly after the text, with the Arabic supplement after it in the Arabic locale; the limitation never states that shortening occurred (it asserts possibility only, and no variant wording exists); the `text` slot equals the owner-held value exactly; the projection module's source never references `known_problem`, and a `known_problem` sentinel held by no other owner appears nowhere in `content` | OD-D, RISK-002 |
| 22 | reference integrity | P | no projection | §7, §8.3, §9.6 | in populated fixtures (assumption chains with assumption and answered successors, including `provisional assumption → answer A → corrected answer B` (#25); answers and unknowns that are endpoints of active contradiction pairs (#28); acknowledged unknowns; active `unknown` records, routed specialist needs, open and partial gaps, active and withdrawn-anchor quantities), every ref of every field-16 and field-17 item resolves to exactly one existing item of the kind the mapping names; the same holds for the refs of fields 12, 15, 18, 24 and 29; a fixture with a dangling ref refuses | §8 |
| 23 | failure classes (Astra) | P, W | no composer | §3.4 | each of the following refuses with an empty 503, no JSON, no HTML, no file and never `UNAVAILABLE`: a missing table and a missing column, each injected for every first-slice store read after authorization (S1's `load_contract`, S2, S22, the four E2 readers, `load_interface_dependencies`, `load_result_events`; a failure inside S1's ownership lookup is a DENIAL, #26); database corruption / integrity failure (`sqlite3.DatabaseError` "malformed", `sqlite3.IntegrityError`); a snapshot lost mid-composition; `ProjectNotFound` inside the snapshot; a `None` E2 collection; an unclassified `sqlite3.Error`; an unclassified exception | §3.4, workstream §4A |
| 24 | `UNAVAILABLE` admission | P, H | no composer | §3.4 | (a) the composer's failure classification maps no first-slice source failure to `UNAVAILABLE` (exhaustive source × failure table); (b) a demonstrably section-local outcome — supplied at the composer's section-outcome seam as already-materialized projection data, because no first-slice source has a positively local failure class at this base (§3.4) — renders `UNAVAILABLE` in its own slots only, sets `unavailable_notice`, renders the top sentence, leaves every other section byte-identical to the unfailed projection and passes the §9.6 check | workstream §4A, §15.3 |
| 25 | assumption-origin history (Condition A) | P | no projection | S13, §8.3 | with a populated fixture `provisional assumption → answer A → corrected answer B` (and the variants assumption → assumption → answer, and assumption → answer only): no REFUSAL; the assumption is a field-16 `assumption` item and nothing else; A and B are a field-26 `correction_version` chain (positions 1 and 2, `disposition` `answered`, currency `SUPERSEDED` / `CURRENT`), never `assumption` items; the assumption's ref resolves to A's field-26 item (to the field-29 row(s) canonically representing the answer when it is the only answer, §7); A's ref resolves to the assumption item; the field-29 row(s) canonically representing B exist (§7); every ref resolves; a ledger the owner classifies `ANCESTRY_MALFORMED` refuses | §6, §8 |
| 26 | S1 DENIAL versus REFUSAL (Condition C) | W, P | no routes | §3.4, §4 | (1) missing project, (2) another account's project, (3) NULL owner and (4) an ownership-lookup failure that `_is_authorized` converts to `ProjectAccessDenied` (an exception injected into `store.load_owner`, a storage error included) each give the same byte-identical `_deny_project()` response; (5) a storage, schema or integrity failure injected into `store.load_contract` after authorization succeeded gives the empty 503; (6) every case produces no file; `get_authorized_project_read`, `_is_authorized` and `_deny_project()` are unchanged | §4, P10-D3a |
| 27 | attribution coverage (Condition B) | P, H | no projection | §8.1, §8.3, §9.6, §10 | in a fully populated fixture: every `RECORDED` item of a truth-bearing kind has a `RECORDED` slot with `content_class`, `source_owner` and a four-field envelope whose values equal the owner-held fields or are `NOT_APPLICABLE` where the owner holds none (`unresolved_gap`, `routed_specialist_need`, `recorded_unknown` and both declared-contradiction kinds included); only `gap_reference` and `evidence_reference` are reference-only, each with exactly one ref to a valid item of the kind §8.1 names and no slot of its own carrying metadata; the schema check refuses a truth-bearing item without attribution, a reference-only item with its own metadata or a dangling ref, and an injected default value; the HTML shows Source, Validation and Limitation (and Currency where recorded) inside each truth-bearing item's container, and the inherited rows next to each reference | §5, workstream §15.7 |
| 28 | canonical field-29 representation (F1) | P | no projection | §7, §8.3, live `derive_requirement_landscape` | (1) `assumption → answer A` with A an endpoint of an active declared contradiction: no REFUSAL; the assumption's ref resolves to the one `active_contradiction` row naming A; A has no own row and none is created; (2) `assumption → answer A → corrected answer B` with the terminal B in an active declared contradiction: no REFUSAL and every successor / history ref resolves (A and B in field 26; B carried in the contradiction row); (3) A an endpoint of two active pairs: the ref lists both rows in owner order; (4) an active `unknown` record joined by a legacy `contradicts` edge: its `recorded_unknown` ref resolves to the legacy `active_contradiction` row; (5) the ordinary fixtures without contradictions still resolve to own `assertion` rows; (6) an `anchor_active` quantity resolves to its anchor's own `assertion` row, and a quantity whose anchor became a contradiction endpoint refuses through the owner's `QuantityHistoryError` (owner semantics, §8.3), not through an export reference defect; no case uses text matching or a second Landscape derivation | §5, §7 |
| 29 | C1 neutral wording | H | no template | §12.4, §12.5, §12.7 | an `OWNER_STATED` (and `user_defined`) Source renders "Inventor" / "المخترع", never "You" / "أنت"; fields 12 and 26, the `RESULT_TEXT_NOT_CARRIED` reason, the withdrawn-answer note and the execution-state text use the neutral §12.7 wording; a scan of every Stage-35-authored fixed-text string — the §12 copy and the new `UI_S35_*` keys — in the EN and AR documents finds no ambiguous second-person "you" / "your" (EN) or second-person address (AR) other than the exact workstream disclaimers' imperatives; existing owner-held / owner-generated strings keep their canonical wording, and the ONLY allowed families are (i) Requirement Landscape owner statements (the exported `label`, `status`, `resolving_action` and `statement` slots, e.g. "Contradiction you declared", "Interface you declared", "declared by you; not validated", "You indicated that this is not known yet.", "You chose to defer this item.") and (ii) Section-11 owner / system-generated experiment text (e.g. `what_to_observe` "… under conditions you control."); when any rendered string of those families contains "you" / "your", the §12.9 legend sentence explaining it is present in both locales; no other copy is exempt; quoted inventor content (located structurally) is out of scope; the reused keys, the owner strings and other surfaces are unchanged, and the JSON is byte-identical (Correction 05, R-C1) | workstream §4 rule 4 |
| 30 | C2 envelope context | H | no template | §10, §12.8 | every `NOT_APPLICABLE` Source, Validation and Limitation row of a truth-bearing item renders its §12.8 sentence (EN and AR), never a bare "Not applicable"; each sentence states that no separate value is held and its second sentence rules out "no source", "validated / validation unnecessary" and "no limitations"; field-level `NOT_APPLICABLE` (fields 25, 28) still renders "Not applicable"; the JSON marker is unchanged | workstream §5 |
| 31 | C3 legend and Risks clarification | H | no template | §10, §12.9, §12.10 | the one "How to read this document" block appears after the disclaimers and before field 1, in EN and AR, and explains both content classes and all seven markers with the §12.3 wording; with fixtures where fields 15, 16, 17 and 24 are each `NOTHING_RECORDED`, the legend line for that marker states that it does not mean none exists; the §12.10 clarification sits under the field-24 heading whatever its marker; neither text contains a severity, probability, score, ranking or assessment word, and the field-24 items are unchanged | workstream §13 |
| 32 | C4 phone width and long values | H | no template | §10 | the document has the viewport meta; at a 360–390 px viewport: (A) a 2,000-character unbroken inventor value (no spaces) causes no horizontal page overflow, wraps inside its container and still decodes to the exact owner-held value; (B) a normal generated header with the disclosure-schema version, the export-format version and the full `sha256:` content digest keeps the page width within the viewport with no horizontal document overflow, the digest text in the document is byte-identical to the JSON `content_digest`, and selecting / copying it yields exactly that digest (no inserted soft hyphen or zero-width character; the digest is never altered to make the test pass) (Correction 05, R-C4); `white-space: pre-wrap`, `dir="auto"` / `<bdi>`, escaping and labels outside the value element are unchanged; in the Arabic document each exact English disclaimer, the English scope label and the English `capture_limitation` carry `lang="en" dir="ltr"`, and Arabic mixed-direction fixtures keep each value next to its own labels | workstream §13 |

R1-focused obligations (file R):

| # | Obligation | Passes when |
|---|---|---|
| R1 | six readers inside a healthy snapshot | each of the six returns its normal result inside `with store.read_snapshot()` |
| R2 | six readers standalone | outside any transaction each behaves exactly as before (results, ordering, `ProjectNotFound`, `*Corrupt`) |
| R3 | bare caller-owned transaction | after a raw `BEGIN IMMEDIATE` on the connection each of the six raises `RecordStoreConnectionUnsafe` |
| R4 | sticky unsafe state | with `_connection_unsafe` set each of the six refuses, inside or outside a snapshot |
| R5 | nested snapshots | an inner `read_snapshot()` neither sets nor clears the evidence; reads after the inner exit, still inside the outer, are admitted |
| R6 | no-op branch | `read_snapshot()` entered while not committed-state-readable grants no admission |
| R7 | release / cleanup failure | a failing `RELEASE` keeps today's handling (unsafe marking when unresolved) and the composer refuses at step 6 |
| R8 | write inside a read snapshot | every writer still refuses inside the snapshot; the snapshot and stored state are unchanged |
| R9 | lifetime expiry | after the owning `read_snapshot()` exits, the six readers return to standalone behaviour |
| R10 | snapshot lost underneath | if the read transaction ends while the evidence is set, the next R1 admission refuses, and the composer's step-5 check refuses the export even when no R1 read follows |
| R11 | writers and `committed_*` readers unchanged | their existing tests pass unmodified; inside a snapshot they still refuse |
| R12 | no global relaxation | `_refuse_uncommitted_reads()` and `committed_state_readable()` source and behaviour unchanged; no new durable state, table or migration |
| R13 | S22 is not an R1 reader | `load_requirement_quantities` is unchanged and does not call `_admit_snapshot_read()`; inside a healthy snapshot it returns the same validated history as standalone |

## 15. Targeted architecture-review appendix

Purpose: verify that this implementation contract faithfully implements the accepted architecture. R1 selection is
settled and is not re-opened. Questions for the reviewer:

1. **R1 shape (§3.2):** do the evidence lifecycle, the three-step guard and the six substitutions satisfy every
   Correction-03 IR-01 bullet, including the "snapshot lost underneath" refusal and the unchanged standalone path?
2. **Integrity checks (§3.1 steps 2, 5, 6):** is the existing `committed_state_readable()` — `True` before entry,
   `False` at the end of the snapshot body, `True` after exit — a sufficient snapshot-loss check for every read,
   including the non-R1 reads (S1, S2, S22), given that no public snapshot predicate is added? It detects a lost
   snapshot only; it is never used as proof that a failure is section-local (§3.4).
3. **Source-to-envelope mapping (§8):** is any slot mis-classed, any envelope value substituted or any owner token
   mis-sourced?
4. **Extractions (§2.3):** are E1–E4 pure, behaviour-preserving and byte-identical, and is the E2 split (raising loader
   + unchanged swallowing wrapper, with the §2.3 composer rule that a `None` collection refuses) the minimal way to give
   the composer failure classes?
5. **Experiment source (§5):** is consuming `assemble_deliverable(...)` Section 11 through an allow-list acceptable
   versus extracting `_s11`?
6. **Section 11 disposition (§6):** settled by workstream contract §7 (Correction 04); confirm only that the candidate
   applies it to that one slot.
7. **Landscape ruling (§7):** does splitting the owner's `lo|hi` reference count as structural identity use rather than
   parsing?
8. **Module boundary (§2.1):** is `engine/disclosure_export.py` the right narrow home, with `read_export_service`
   consumed but not extended?
9. **Authorization (§4):** is calling `get_authorized_project_read` inside the snapshot correct, and is the denial /
   refusal split correct?
10. **Failure classification (§3.4, corrected after the Astra fast stop):** "the read transaction is still open" is no
    longer used as proof of locality; schema, integrity, corruption, snapshot and every unclassified storage failure
    refuse. Confirm (a) the empty first-slice positively-local set, and (b) that #24's projection-seam case satisfies
    workstream contract §15.3 while no first-slice source can produce `UNAVAILABLE`.
11. **Requirement quantities (S22 / S23, §8.3):** is `load_requirement_quantities` correctly a STORE seam rather than a
    seventh R1 reader, and is the `requirement_quantity` item (owner tokens only; `currency` `NOT_APPLICABLE`; no ref for
    a withdrawn-anchor row) faithful to the owner?

## 16. UX / behaviour review package (targeted C1–C4 re-check; UX PASS NOT YET CLAIMED)

Review status: the architecture review is complete; the non-authoring semantic verification, including the Correction 03
delta, is complete; the broad UX / behaviour review (journey, download controls, disclaimers, scope label, markers and
reasons, retention wording, inventor-text association, requirement quantities, system statements, attribution rows, EN
/ AR and RTL) is complete with PASS WITH CONDITIONS C1–C4. That broad review is NOT repeated. Correction 04 changes UX
wording and presentation only, so the next reviewer performs only this targeted copy / presentation check, in EN and AR:

- **C1 — neutral wording:** a third-party reader sees "Inventor" / "المخترع" as the Source of the inventor's records, the
  neutral field-12 and field-26 headings, the neutral `RESULT_TEXT_NOT_CARRIED` reason, withdrawn-answer note and
  execution-state text (§12.4, §12.5, §12.7); no Stage-35-authored copy addresses the reader as the inventor, and
  owner-held "you" / "your" is explained by the §12.9 legend sentence (Correction 05).
- **C2 — envelope `NOT_APPLICABLE`:** the §12.8 sentences cannot be read as "no source", "validated", "validation
  unnecessary" or "no limitations", and field-level "Not applicable" (fields 25, 28) still reads correctly.
- **C3 — legend and Risks:** the "How to read this document" block (§12.9) correctly explains both content classes and
  all seven markers, so that "Nothing recorded in this project" on unresolved technical issues, assumptions, missing
  information and risks cannot reasonably be read as "none exist"; the §12.10 Risks clarification is present and reads
  as no risk assessment.
- **C4 — phone width and direction:** at 360–390 px a long unbroken inventor value causes no horizontal page overflow and
  stays readable and exact; English fixed text inside the Arabic document reads left-to-right (§10); mixed-direction
  fixtures keep each value next to its own labels.
- **Not in scope:** anything outside C1–C4, and the legal sufficiency of the disclaimer wording (Owner decision 9).

Outcome: the targeted re-check returned PASS WITH CONDITIONS (C2 and C3 closed); its two residuals, R-C1 and R-C4, are
closed by Correction 05 (final UX), and the reviewer recorded that no further UX or architecture review is required.

## 17. Unresolved issues and pre-implementation Owner decisions

Resolved by Owner decision and workstream contract Correction 04 (2026-10-04):

- **OD-A:** requirement quantities CARRIED (S22 / S23, field 12, §8.3).
- **OD-B:** interface observations OMITTED (§11).
- **OD-C:** field 18 KEPT as mapped (§11).
- **OD-D:** problem-resolution boundary KEPT, with the unconditional §12.6 limitation.
- **§6 objective exclusion:** authorized by workstream contract §7.
- **Decisions 2 and 3:** ACCEPTED in workstream contract §17 (§0).

Closed by the completed Astra architecture review (PASS WITH CONDITIONS): `UNAVAILABLE` reachability (§3.4, #24) and the
withdrawn-answer quantity mapping (§8.3). Its four conditions are addressed by Correction 02: (A) assumption-origin
history (§8.3, #25); (B) attribution coverage (§8.1, §8.3, §9.6, §10, #27); (C) S1 DENIAL versus REFUSAL (§3.4, §4,
#26); (D) §5 aligned with §3.1.

The independent non-authoring verification of Correction 02 (PASS WITH CONDITIONS) closed B, C and D; its one residual,
F1 (a contradiction endpoint has no own field-29 row), is addressed by Correction 03 (§7 canonical representation rule,
§8.3, #28), so conditions A–D are intended closed.

The targeted non-authoring delta verification of Correction 03 returned PASS. The UX / behaviour review returned PASS
WITH CONDITIONS C1–C4, addressed by Correction 04 (UX) under workstream contract Correction 05.

The targeted UX re-check returned PASS WITH CONDITIONS (C2, C3 closed); Correction 05 (final UX) closes R-C1 and R-C4.
No further UX or architecture review is required.

Still open:

- **Final Lead diff verification** of Correction 05 and hosted CI on the final head.
- **Owner decision** on accepting and merging this implementation contract.
- **Implementation authorization** (workstream contract §17 decision 8) has not been given.
- **Owner-level note (no export change):** a requirement quantity whose anchoring answer later becomes an endpoint of an
  active contradiction is classified invalid by the existing T2-A owner (`QuantityHistoryError`), so every surface of
  that owner fails closed — the report and PDF deliverable seam included — and this export refuses consistently with
  it. Changing that is an owner (runtime) decision outside this contract.

## 18. Non-authorization (restated)

This document authorizes no implementation, R1 change, `engine/record_store.py` change, Stage 35 composer, extraction,
route, page, download, template, `ui_text` key, runtime schema, persistence, migration, export history, test, API,
provider, AI, e-mail, attachment processing, deployment or release; no change to the report, PDF, Structured Export,
self-service project export or public API; no Stage 33, 34, 36 or 39 activation; no Master Roadmap stage entry,
checkbox, marker or count change; and no CAP number.
