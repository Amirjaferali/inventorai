# STAGE 35 — STRUCTURED INVENTION DISCLOSURE EXPORT — FIRST BOUNDED SLICE — IMPLEMENTATION CONTRACT (CANDIDATE)

STATUS: IMPLEMENTATION CONTRACT CANDIDATE — DOCUMENTATION ONLY — NO IMPLEMENTATION AUTHORIZED.
AUTHORITY LEVEL: subordinate to the accepted workstream contract
[`STAGE35_STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_WORKSTREAM_CONTRACT.md`](STAGE35_STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_WORKSTREAM_CONTRACT.md)
(the "workstream contract", as corrected by Correction 03, PR #754) and to the Owner decision
[`STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md`](STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md).
It is the "implementation contract" that workstream-contract prerequisites (2) and (3) require. It narrows nothing in
the workstream contract and amends none of its clauses; where this document and the workstream contract differ, the
workstream contract wins and the difference is a defect of this document.
RECORDED: 2026-10-04, by Owner authorization of ONE documentation-only first-slice implementation-contract candidate.
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

## 0. Owner decisions recorded for the first slice

These decisions bind this implementation contract only. They do not change the workstream contract's §17 record, which
still reads OPEN for decisions 2 and 3; recording them there is a separate documentation act.

- **Decision 2 — export history: FIRST-SLICE DEFERRAL ACCEPTED.** The first slice creates no export-history record,
  retains no server-side disclosure-export artifact (no copy, cache entry or temporary file of the export) and
  introduces no persistence for export history. The deferral is limited to the local-download first slice. Any future
  external transfer still requires export history before activation (workstream contract §11); this decision is not a
  general decision against export history.
- **Decision 3 — renderings and file types: versioned JSON + self-contained HTML.** The machine-readable rendering is a
  versioned JSON file; the human-readable rendering is one self-contained HTML document generated solely from the same
  deterministic projection, adding no substantive content. PDF stays excluded from the first slice.

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
  Arabic supplements, the conditional disclaimer, the scope label) and the closed v1 token sets (§9);
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
| S13 | Assumptions, corrections, unknown dispositions | `state.assertions` (`AssertionRecord`: `disposition`, `content`, `provenance`, `validation_status`, `gap_context`, `superseded_by`, `supersedes`) | PUBLIC |
| S14 | Acknowledged unknowns | `state.acknowledged_unknowns` (`AcknowledgedUnknown.verbatim`, `.gap_context`) | PUBLIC |
| S15 | Routed needs | `engine.need_routing.active_routes(state)` (`NeedRoutingRevision.gap_type`, `.required_input`, `.provenance`) | PUBLIC |
| S16 | Requirement Landscape | `engine.requirement_landscape.derive_requirement_landscape(state).requirements` (`DerivedRequirement` fields) | PUBLIC |
| S17 | CAP-11 Source / Validation labels | `web/ui_text.py` keys `UI_ED_SOURCE_<provenance>`, `UI_ED_VALIDATION_<validation_status>`, `UI_ED_SOURCE`, `UI_ED_VALIDATION`, `UI_ED_FORM`, `UI_ED_HEADING` (tokens read from the Evidence object directly) | PUBLIC (render only) |
| S18 | Gap names | `web/gap_labels.py` `GAP_DISPLAY_NAMES` / `GAP_DISPLAY_NAMES_AR` (explicit locale; not `friendly_gap_name`, which depends on request state) | PUBLIC (render only) |
| S19 | Part labels | `web/ui_text.py` `UI_S15_SCOPE_MECH`, `UI_S15_SCOPE_ELEC`, `UI_S15_SCOPE_CTRL`, `UI_S15_SCOPE_FUNCTION` | PUBLIC (render only) |
| S20 | Section-11 labels | `UI_B_DELIV_075`, `UI_B_DELIV_078`, `UI_B_DELIV_080`, `UI_DELIV_METHOD_ABSENT_LABEL`, `UI_DELIV_HYPOTHESIS_ABSENT_LABEL`, `UI_DELIV_VARIABLE_ABSENT_LABEL`, `UI_S11_EXECUTION_LABEL`, and `web/app.py` `S11_EXECUTION_TEXT` | PUBLIC (render only) |
| S21 | Inactive-declaration wording / Landscape heading | `UI_T3A_CONFLICT_INACTIVE`; `UI_B_DELIV_036` | PUBLIC (render only) |
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
   c. the R1 reads, in this order: E2 `load_planning_metadata` (four R1 readers), S8 `load_interface_dependencies`,
      S7 `load_result_events` (always called, even for a project with no experiment).
5. Every source value the projection needs is materialized into memory inside the snapshot. As the last statement of
   the `with` block the composer checks `store.committed_state_readable()`: inside a healthy store-owned snapshot it is
   `False` (the read transaction is open); `True` means the read transaction ended underneath the composer, so the
   export refuses. No source is read after the block ends.
6. After leaving the snapshot, if `store.committed_state_readable()` is `False` (a release failure left the connection
   unresolved, or the sticky unsafe state is set), refuse.
7. Pure, in-memory composition (applying the loaded planning metadata to the reconstructed state,
   `assemble_deliverable`, `derive_requirement_landscape`, `active_routes`, contradiction pairs, the field map) and the
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
lost snapshot is detected by the final R1 admission (step 4c) and refuses the export. "Snapshot" names a read view only;
no revision identity is created or implied.

### 3.4 Failure classification (frozen)

| Condition | Class |
|---|---|
| No account; `ProjectAccessDenied` from S1 (missing project, another account's project, NULL owner, ownership-lookup failure) | DENIAL (`_deny_project()`) |
| Step 2 or step 6 false; `SAVEPOINT` failure; `RecordStoreConnectionUnsafe` anywhere | REFUSAL |
| `review.level != 1`; `ContractError`; `MalformedAssumptionAncestryError`; `ReconstructionReplayLimitError`; `ProjectNotFound` inside the snapshot | REFUSAL |
| Any store `*Corrupt` error (`SuccessCriterionCorrupt`, `ResultEventsCorrupt`, interface / dependency corruption, …) | REFUSAL (inconsistent source history) |
| Any exception from a pure derivation (S3, S6, S11, S12, S15, S16) or a failed v1 schema check (§9.6) | REFUSAL (global integrity / schema failure) |
| A ledger anchor, endpoint or part reference that does not resolve by identity in the same snapshot | REFUSAL (project-binding / anchor defect) |
| `sqlite3.Error` (not one of the above) from the E2 planning load | SECTION-LOCAL: the four planning slots of every experiment are `UNAVAILABLE` |
| `sqlite3.Error` (not one of the above) from `load_interface_dependencies` | SECTION-LOCAL: the `dependency` and `dependency_note` slots of every interface are `UNAVAILABLE` |
| `sqlite3.Error` (not one of the above) from `load_result_events` | SECTION-LOCAL: the `execution_state` slot of every experiment is `UNAVAILABLE` |
| Any section-local error after which `store.committed_state_readable()` is `True` while still inside the `with` block (the read transaction ended) | REFUSAL (snapshot lost) — checked immediately after the error and again at step 5 |

A refusal is a bounded error with no file and no partial output. The JSON route and the HTML route answer a refusal with
a bare, empty-bodied 503, exactly like the P10-D3a self-service export. A refusal never degrades to `UNAVAILABLE`.

The disclosure export is stricter than the Stage-19 web helper on purpose: that helper maps every failure, corruption
included, to UNAVAILABLE for its own surfaces (unchanged by E3); the disclosure export refuses on corruption, as
workstream contract §4A requires.

## 4. Authentication and authorization (frozen)

- One authenticated owner: the route resolves the account through the existing `_current_account()` seam only.
  Anonymous callers receive `_deny_project()`.
- One explicitly requested owned project: authorization is the existing `get_authorized_project_read`, called inside
  the snapshot so the ownership decision and the content come from the same committed state. It denies a missing
  project, another account's project, a project with a NULL (anonymous / legacy) durable owner and any ownership-lookup
  failure identically; every such denial maps to the same `_deny_project()` response, so a missing project and another
  account's project are indistinguishable.
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
- `assemble_deliverable` is called on the reconstructed state after `attach_planning_metadata` succeeded; its
  `generated_at` and every non-Section-11 key are ignored.
- Allow-list per item: `experiment_id` (join key only; never exported), `experiment_title`, `objective`,
  `what_to_observe`, `traceability.source_type` (decision input for §6 only; never exported), `success_criterion`,
  `success_criterion_provenance`, `success_criterion_status`, `measurement_method`, `measurement_method_provenance`,
  `test_hypothesis`, `test_hypothesis_provenance`, `test_variable`, `test_variable_provenance`. Every other key
  (`source_basis`, `minimum_prototype`, `failure_or_revision_condition`, `expected_evidence_upgrade`,
  `required_expertise_or_tools`, `traceability.source_ref`, `traceability.content`) and every plan-level key
  (`shared_required_expertise`, `stale_*`, `note`, `empty_statement`) is not exported.
- If planning metadata is section-locally `UNAVAILABLE` (§3.4), `assemble_deliverable` still runs (experiment identity
  does not depend on planning metadata), but the four planning slots are `UNAVAILABLE` and the values the generator
  would have computed without the durable metadata are discarded.

## 6. Section 11 finding — disposition (preserved by Astra, the independent reviewer and Correction 03)

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
   allowed system assertions (workstream contract §6). The objective of a `reasoned_leading_claim` experiment cannot be
   exported: workstream contract §8 excludes evidence-quality grades from both renderings. Its `objective` slot carries
   `EXCLUDED_FROM_FIRST_SLICE` with reason `OBJECTIVE_NAMES_EVIDENCE_LEVEL`, following the same in-place-marker pattern
   §8 already prescribes for the CAP-11 Form value. The experiment itself (title, what to observe, planning fields,
   execution state) is carried: none of those values states a grade. The source text is not reworded and no sanitized
   objective is synthesized. The decision input is the structural token `traceability.source_type`, never the
   objective text.

This disposition relies on §8 (the grade exclusion) and the §8 Form-row in-place-marker precedent; the targeted review
(§15) confirms it. If the reviewer finds the precedent insufficient, the fallback is a one-line workstream-contract
correction naming this slot in §7, not a change to the source text.

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
structure supports the distinction completely.

## 8. Source-to-envelope mapping (frozen)

### 8.1 Envelope

Every `RECORDED` value slot carries `content_class`, `source_owner` and an envelope of four fields. Each envelope field
is `{"marker": "RECORDED", "value": <owner value>}`, `{"marker": "NOT_APPLICABLE", "value": null}` (the owner holds no
such metadata for this kind of item) or `{"marker": "UNAVAILABLE", "value": null}`. No value is ever substituted.

- **provenance:** the owner's own provenance token where the owner object holds one (`Evidence.provenance`,
  `AssertionRecord.provenance`, `Subsystem.provenance`, `SubsystemInterface.provenance`,
  `NeedRoutingRevision.provenance`, and the Section-11 planning provenance tokens `user_defined` / `source_stated`);
  otherwise `NOT_APPLICABLE`.
- **validation_state:** `Evidence.validation_status`, `AssertionRecord.validation_status`,
  `Subsystem.validation_state`, `SubsystemInterface.validation_state`; otherwise `NOT_APPLICABLE`.
- **limitation:** `NOT_APPLICABLE` for every first-slice source — no first-slice owner holds a per-item limitation-text
  field. Owner limitations travel as the owner's own status tokens and wording (validation state, Landscape status and
  resolving action, the Stage-19 execution wording).
- **currency:** `CURRENT` / `SUPERSEDED` only for ledger records (`superseded_by is None` → `CURRENT`); otherwise
  `NOT_APPLICABLE`.

Owner-specific metadata travels in an item's `tokens` map under closed keys (§9.3), never in a generic field.
`LEGACY_UNSPECIFIED` stays as it is.

### 8.2 Field map (29 fields, fixed order)

Each Owner-decision §2 row with more than one first-slice disposition is split into fields that each carry exactly one
marker. "Integrated" means the reconstructed state holds a durable Owner-declared composition (`state.subsystems`
non-empty).

| # | Field token | Disposition | Owner / seam | Items |
|---|---|---|---|---|
| 1 | `invention_title` | `NOT_CAPTURED` | — | — |
| 2 | `problem_addressed` | `RECORDED` / `NOTHING_RECORDED` | S3 `resolved_problem` | 1 item, kind `resolved_problem` |
| 3 | `background_and_existing_limitations` | `NOT_CAPTURED` | — | — |
| 4 | `invention_objective` | `NOT_CAPTURED` | — | — |
| 5 | `technical_concept` | `RECORDED` / `NOTHING_RECORDED` | S4 `state.known_mechanism` | 1 item, kind `known_mechanism` |
| 6 | `parts` | integrated: `RECORDED`; otherwise `NOT_CAPTURED`, reason `NON_INTEGRATED_PROJECT` | S9 | kind `part`, composition order |
| 7 | `component_descriptions_beyond_parts` | `NOT_CAPTURED` (otherwise-case reason `NON_INTEGRATED_PROJECT`) | — | — |
| 8 | `relationships` | integrated: `RECORDED` / `NOTHING_RECORDED`; otherwise `NOT_CAPTURED`, reason `NON_INTEGRATED_PROJECT` | S9 + S8 | kind `interface`, interface order |
| 9 | `operating_sequence_or_workflow` | `NOT_CAPTURED` | — | — |
| 10 | `alternative_embodiments` | `NOT_CAPTURED` | — | — |
| 11 | `typed_materials_dimensions_parameters_conditions` | `NOT_CAPTURED` | — | — |
| 12 | `raw_materials_dimensions_parameters_conditions` | `RAW_TEXT_ONLY`, pointer `requirement_landscape`, when field 29 holds at least one quoted slot; otherwise `NOT_CAPTURED` | — | — |
| 13 | `interface_verification_preparation_inputs` | `EXCLUDED_FROM_FIRST_SLICE`, reason `PLANNING_INPUTS` | — (not read) | — |
| 14 | `novelty_and_differentiation` | `NOT_CAPTURED` | — | — |
| 15 | `unresolved_technical_issues` | `RECORDED` / `NOTHING_RECORDED` | S10 + S12 | kinds `unresolved_gap`, `declared_contradiction`, `declared_contradiction_history` |
| 16 | `assumptions` | `RECORDED` / `NOTHING_RECORDED` | S13 | kind `assumption` |
| 17 | `missing_information` | `RECORDED` / `NOTHING_RECORDED` | S10 + S13 + S14 + S15 | kinds `gap_reference`, `acknowledged_unknown`, `recorded_unknown_reference`, `routed_specialist_need` |
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
§5). `UNAVAILABLE` never appears at field level in the first slice: the only section-local failures are slot-level
(§3.4). Field 12 does not classify inventor text: it points to where the inventor's own unparsed wording is carried and
does not assert that such values are present.

### 8.3 Item and slot mapping

`content_class` is `QUOTED_INVENTOR_CONTENT` (Q) or `SYSTEM_ASSERTION` (S). "Env" lists provenance / validation_state /
currency (limitation is always `NOT_APPLICABLE`; §8.1).

| Kind | Slots (class) | Env | Tokens / refs | Nothing / failure behaviour |
|---|---|---|---|---|
| `resolved_problem` | `text` (Q) = `resolved_problem(state).content` | `Evidence.provenance` / `.validation_status` / NA | — | field `NOTHING_RECORDED` when `resolved_problem` is `None` |
| `known_mechanism` | `text` (Q) = `state.known_mechanism.content` | `Evidence.provenance` / `.validation_status` / NA | — | field `NOTHING_RECORDED` when `known_mechanism` is `None` |
| `part` | `name` (Q) `display_name`; `function` (Q) `function_text` | `Subsystem.provenance` / `.validation_state` / NA | `part_domain` (`mechanical`, `electronics_electrical`, `control_loop`) | — |
| `interface` | `description` (Q); `dependency` (S, value `null`); `dependency_note` (Q) | `SubsystemInterface.provenance` / `.validation_state` / NA on `description`; NA on the dependency slots | refs `[part_a, part_b]`; `dependency` tokens `dependency_kind` (`one_way` / `mutual`), `dependent_part`, `depends_on_part` (item keys; one-way only) | no declaration → `dependency` and `dependency_note` `NOTHING_RECORDED`; declaration without note → `dependency_note` `NOTHING_RECORDED`; section-local read failure → both `UNAVAILABLE` |
| `unresolved_gap` | none | — | `gap_type`, `gap_status` (`OPEN` / `PARTIAL`) | — |
| `declared_contradiction` | `answer_a`, `answer_b` (Q) = endpoint `content` | each endpoint record's provenance / validation / currency | `active: true`; ref to the matching field-29 row | — |
| `declared_contradiction_history` | `answer_a`, `answer_b` (Q) | each endpoint record's provenance / validation / currency | `active: false` | — |
| `assumption` | `text` (Q) = record `content` (every `provisional_assumption` record, ledger order) | record provenance / validation / currency | `gap_type` (= `gap_context`); ref to the successor's item (an `assumption` item, or the field-29 row of an active successor) | — |
| `acknowledged_unknown` | `text` (Q) = `verbatim` | NA / NA / NA | `gap_type` (= `gap_context`) | — |
| `recorded_unknown_reference` | none | — | ref to the field-29 row of each ACTIVE `unknown`-disposition record | — |
| `routed_specialist_need` | none | provenance = `NeedRoutingRevision.provenance` carried in tokens | `gap_type`, `required_input` (`SPECIALIST` only, per the workstream contract's "routed specialist needs"); ref to the field-29 routing row | — |
| `gap_reference` | none | — | ref to the field-15 `unresolved_gap` item | — |
| `evidence_reference` | `cap11_form` → `EXCLUDED_FROM_FIRST_SLICE`, reason `FORM_ROW_QUALITY_DERIVED` | none on the item: the CAP-11 Source and Validation rows are the referenced `text` slot's provenance and validation_state, which the HTML shows inside this item's container as two separate rows | ref to `problem_addressed.1` or `technical_concept.1` | one item per present Evidence; none → field `NOTHING_RECORDED` |
| `experiment` | `title` (S); `objective` (S, or `EXCLUDED_FROM_FIRST_SLICE` reason `OBJECTIVE_NAMES_EVIDENCE_LEVEL`, §6); `what_to_observe` (S); `success_criterion` (Q); `measurement_method` (Q); `test_hypothesis` (Q); `test_variable` (Q); `execution_state` (S, value `null`) | planning slots: provenance = the item's `*_provenance` token; others NA | `execution_state` tokens `state` (`none` / `recorded`), `count` | `success_criterion_status == "required"` → `NOTHING_RECORDED`; an absent method / hypothesis / variable → `NOTHING_RECORDED`; planning or execution section-local failure → those slots `UNAVAILABLE` |
| `correction_version` | `text` (Q) = record `content` | record provenance / validation / currency | `chain`, `position` (1-based), `gap_type` | — |
| `requirement` | per §7 | per §7 | `anchor_kind`; refs per §7 | per §7 |

Selection rules, all by owner tokens:

- `unresolved_gap`: every `state.gaps` entry with status `OPEN` or `PARTIAL`, in state order. `gap_reference` items
  (fields 17 and 24) point to these, one each.
- Declared contradictions: every `contradiction_declared` record in ledger order; `active` if its endpoint pair is in
  `active_declared_contradiction_pairs`, otherwise history. Legacy undeclared edges are not Owner-declared and appear
  only through the Landscape.
- `correction_version`: every supersession chain of length two or more over interaction-disposition records
  (`INTERACTION_DISPOSITIONS` minus `DECISION_ACTION_DISPOSITIONS`) that contains no `provisional_assumption` record;
  chains that contain one are carried in field 16. Chain order = order of the chain root in the ledger.
- Field 18 carries the Section-2 evidence registry only (the resolved problem and the known mechanism, the evidence
  CAP-11 already describes with Source and Validation rows). See §11 for evidence owners not carried.

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
  `ACKNOWLEDGED_UNKNOWNS`, `NEED_ROUTING`, `REQUIREMENT_LANDSCAPE`, `PROTOTYPE_TEST_PLAN`, `PLANNING_METADATA`,
  `EXPERIMENT_RESULTS`;
- item kinds: the sixteen kinds of §8.3;
- slot tokens: `text`, `name`, `function`, `description`, `dependency`, `dependency_note`, `answer_a`, `answer_b`,
  `part_a`, `part_b`, `label`, `status`, `resolving_action`, `statement`, `cap11_form`, `title`, `objective`,
  `what_to_observe`, `success_criterion`, `measurement_method`, `test_hypothesis`, `test_variable`, `execution_state`;
- token keys: `part_domain`, `gap_type`, `gap_status`, `active`, `dependency_kind`, `dependent_part`,
  `depends_on_part`, `required_input`, `provenance`, `anchor_kind`, `chain`, `position`, `state`, `count`;
- the field tokens of §8.2.

No internal identifier (record id, subsystem id, interface id, experiment id, question id, project id, account id,
routing reference) and none of the workstream contract §8 data appears anywhere in `content`.

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
reason or kind refuses the export (global schema failure). The module never emits an unknown key. A v1 reader rejects
unknown keys.

## 10. Self-contained HTML contract

- Rendered by one template from the finished projection plus the locale, `generated_at` and the digest; it reads no
  store, state or request data beyond the locale. It adds no substantive content: every substantive value comes from the
  projection; the only other text is fixed chrome (headings, labels, marker and reason wording, retention lines) from
  existing label owners (§2.2 S17–S21) or new `UI_S35_*` keys (§12).
- Self-contained: `<!doctype html>`, `<meta charset="utf-8">`, one inline `<style>` and this policy meta element:

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
  English and Arabic. English digits for versions, dates, counts and item keys.
- Order: scope label; versions, `generated_at`, digest; the disclaimers; the optional `UNAVAILABLE` sentence; the 29
  fields in §8.2 order, each with its heading and either its marker wording (+ reason, + pointer) or its items.
- Every value sits in its own direction-isolated container (`dir="auto"`, `<bdi>` for inline values) with
  `white-space: pre-wrap`; nothing is trimmed or normalized. A quoted value carries the adjacent label "Inventor's own
  words"; a system value carries "InventorAI statement". The Source and Validation labels (CAP-11 `UI_ED_*`), the
  currency label and any marker wording sit inside the same item container, next to the value they describe.
- Canonical English system statements stay English in both locales (Stage 34 rule) and are direction-isolated.

## 11. Existing owners not read by the first slice

Workstream contract §5: "A source without a row in that table is not read." The following owners exist at this base,
hold project information near a disclosure field and are NOT read. None is added here; adding any of them needs a
workstream-contract correction and an Owner decision.

| Owner | Nearest disclosure field | Snapshot admission today | Concern |
|---|---|---|---|
| T2-A requirement quantities (`engine/requirement_quantity.py`; `load_requirement_quantities`) — inventor value text with a closed kind, anchored to a requirement | 11 / 12 (materials, dimensions, parameters, conditions) | admitted | **Truthfulness.** On a project with quantities, field 12's "Only as the inventor's own wording in Requirement Landscape" omits inventor wording held elsewhere. Owner decision required before implementation (§16 OD-A). |
| Stage 15 Slice 4 interface observations (`engine/interface_observation.py`; `load_interface_observations`) | 22 / 23 (prototype status and validation results) | REFUSED (carrying them would need a seventh R1 reader, beyond Correction 03) | Omission only; field 23's "Not captured" stays true (observations are not validation results). Owner decision (OD-B). |
| Stage-3 reasoning-gap evidence (`Gap.evidence`, report Section 9) and Section-2 `known_boundaries` | 18 (technical evidence) | in reconstructed state | Field 18 carries only the CAP-11-described Section-2 evidence. Owner decision (OD-C). |
| T2-E owner-recorded evidence references (`engine/evidence_reference.py`) | 18 | admitted | Not evidence by its owner's own definition; omission consistent. |
| CAP-08 dependency edges (`assumption_dependency_declared`) | 16 | in ledger | Assumptions carried without their declared dependent answers. |
| Control-loop part answers (`PartAnswer`, `subsystem_part_answers`) | 6 / 7 | not checked | Part name and function carried; part answers not. |
| CAP-05 / CAP-07 decision records | 10 | in ledger | Never relabelled as embodiments (workstream contract §7). |
| Stale planning values (`stale_*` of Section 11) | 21 | via package | Current experiments only, as Stage 19. |

Two further limitations the reviews must see:

- The Section-2 problem value is the owner-held `state.idea_summary`, which the owner trims at 500 characters at a word
  boundary and ends with a system-appended "…" (`engine/progression_loop.py` `_trim_idea_summary`). The export
  reproduces exactly that value under "Inventor's own words"; the full statement sits only in the prohibited
  `state.known_problem`. Owner decision (OD-D): accept, or correct the workstream contract.
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
| `OBJECTIVE_NAMES_EVIDENCE_LEVEL` | Excluded from this first slice because this generated objective names an evidence-quality level, and this disclosure export does not carry evidence-quality grades. | مُستبعَد من هذه الشريحة الأولى لأن هذا الهدف المولَّد يذكر مستوى جودة الدليل، وهذا التصدير لا يحمل درجات جودة الأدلة. |
| `PLANNING_INPUTS` | Excluded from this first slice because these are planning inputs for checking an interaction between parts, not a description of the invention. | مُستبعَد من هذه الشريحة الأولى لأن هذه مدخلات تخطيط للتحقق من تفاعل بين الأجزاء، وليست وصفًا للاختراع. |
| `CONFIDENTIAL_EVIDENCE_CATEGORIES` | Excluded from this first slice because commercial, manufacturing and integration evidence can be confidential. | مُستبعَد من هذه الشريحة الأولى لأن الأدلة التجارية وأدلة التصنيع والتكامل قد تكون سرية. |
| `RESULT_TEXT_NOT_CARRIED` | Excluded from this first slice: this export shows whether you recorded executions, not the text of your recorded results. | مُستبعَد من هذه الشريحة الأولى: يُظهر هذا التصدير ما إذا كنت قد سجّلت تنفيذات، لا نص النتائج التي سجّلتها. |
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
dimensions, parameters and operating conditions in your own wording / المواد والأبعاد والمعاملات وظروف التشغيل بصياغتك;
Interface verification-preparation inputs / مدخلات التحضير للتحقق من التفاعل بين الأجزاء; Novelty and differentiation
statements / عبارات الجِدّة والتمايز; Unresolved technical issues / المسائل التقنية غير المحسومة; Assumptions /
الافتراضات; Missing information / المعلومات الناقصة; Technical evidence / الأدلة التقنية; Commercial, manufacturing and
integration evidence / الأدلة التجارية وأدلة التصنيع والتكامل; Diagrams and files / الرسومات والملفات; Proposed
experiments and their execution state / التجارب المقترحة وحالة تنفيذها; Text of recorded experiment results / نص نتائج
التجارب المسجّلة; Validation results / نتائج التحقق; Risks / المخاطر; Uncertainty and abstentions / عدم اليقين والامتناع
عن الحكم; Your corrections / تصحيحاتك; Inventor approvals / موافقات المخترع; Source and provenance references / مراجع
المصدر والأصل; Requirement Landscape (existing `UI_B_DELIV_036`).

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
| 3 | §15.3 markers | P, H | no projection | field map | each marker renders its §12.3 wording; injected `sqlite3.Error` in each section-local read renders `UNAVAILABLE` + top sentence; non-integrated project → fields 6–8 `NOT_CAPTURED` + reason, never `NOTHING_RECORDED`; no marker renders empty | §5 |
| 4 | §15.4 no external transfer | P | no module | module | import-graph and socket-blocking tests: no network call, no provider / API / e-mail import | §11 |
| 5 | §15.5 project separation and failure classes | W, P | no routes | routes + §3.4 | missing and foreign projects give byte-identical denials; a NULL-owner project is denied; no record of another project appears; every refusal-class fault (unsafe connection, corrupt history, level 0, anchor defect, schema failure) returns 503 with no file | §4A |
| 6a | §15.6(a) one snapshot | P | no composer | §3.1 | instrumented store shows every source read between one SAVEPOINT and its RELEASE, R1 reads last | §4A |
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

## 15. Targeted architecture-review appendix

Purpose: verify that this implementation contract faithfully implements the accepted architecture. R1 selection is
settled and is not re-opened. Questions for the reviewer:

1. **R1 shape (§3.2):** do the evidence lifecycle, the three-step guard and the six substitutions satisfy every
   Correction-03 IR-01 bullet, including the "snapshot lost underneath" refusal and the unchanged standalone path?
2. **Integrity checks (§3.1 steps 2, 5, 6):** is the existing `committed_state_readable()` — `True` before entry,
   `False` at the end of the snapshot body and after any section-local error, `True` after exit — a sufficient
   snapshot-integrity check for every read, including the non-R1 reads, given that no public snapshot predicate is
   added?
3. **Source-to-envelope mapping (§8):** is any slot mis-classed, any envelope value substituted or any owner token
   mis-sourced?
4. **Extractions (§2.3):** are E1–E4 pure, behaviour-preserving and byte-identical, and is the E2 split (raising loader
   + unchanged swallowing wrapper) the minimal way to give the composer failure classes?
5. **Experiment source (§5):** is consuming `assemble_deliverable(...)` Section 11 through an allow-list acceptable
   versus extracting `_s11`?
6. **Section 11 disposition (§6):** does the §8 Form-row precedent authorize the in-place `EXCLUDED` marker on the
   `reasoned_leading_claim` objective?
7. **Landscape ruling (§7):** does splitting the owner's `lo|hi` reference count as structural identity use rather than
   parsing?
8. **Module boundary (§2.1):** is `engine/disclosure_export.py` the right narrow home, with `read_export_service`
   consumed but not extended?
9. **Authorization (§4):** is calling `get_authorized_project_read` inside the snapshot correct, and is the denial /
   refusal split correct?
10. **Failure classification (§3.4):** is "`sqlite3.Error` with the read transaction still open" a sound test for
    "section-local", with every validation (`*Corrupt`) error refusing?

## 16. UX / behaviour review package (UX PASS NOT CLAIMED)

The required pre-implementation UX review (workstream contract §17) should cover, in EN and AR (RTL):

- **Journey:** account-page link → pre-download page → two downloads; no other step; nothing recorded on view.
- **Download controls:** the JSON vs HTML choice and the same-data line; whether a non-technical inventor understands
  which file to choose.
- **Disclaimers:** comprehension of the eleven notices before the controls; in AR, English followed by Arabic for each.
- **Scope label:** "this project only — not legal advice" prominence on the page and in both files.
- **Markers and reasons:** whether "Not captured by InventorAI", "Nothing recorded in this project", "Not included in
  this export" and "Unavailable" are distinguishable; the Form-row and objective exclusions; the field-12 pointer
  wording.
- **Retention wording:** the four retention lines, especially "creates no record of your exports" next to the
  access-log sentence.
- **Inventor text association:** each quoted value inside its own isolated container with "Inventor's own words", Source
  and Validation labels adjacent; mixed-direction and long values; the trimmed problem statement ending in "…" (§11).
- **System statements:** English canonical statements inside the Arabic document (Stage 34 rule).
- **Not in scope of the review:** legal sufficiency of the disclaimer wording (Owner decision 9).

## 17. Unresolved issues and pre-implementation Owner decisions

- **OD-A (blocking for field 12 truthfulness):** T2-A requirement quantities — carry them (needs a workstream
  correction; their reader is already admitted inside the snapshot) or mark them excluded (also a correction), before
  implementation authorization.
- **OD-B:** Stage 15 interface observations — leave out (current reading) or carry later (would need a further R1
  reader and a correction).
- **OD-C:** Stage-3 reasoning evidence and known boundaries outside field 18.
- **OD-D:** the trimmed Section-2 problem value with its system-appended "…".
- **§6 precedent:** confirm, or add the objective slot to workstream §7 by a one-line correction.
- **Workstream §17 record:** decisions 2 and 3 are recorded here only; the workstream contract still shows them OPEN.
- **Reviews:** the targeted architecture review (§15) and the UX / behaviour review (§16) have not been performed.

## 18. Non-authorization (restated)

This document authorizes no implementation, R1 change, `engine/record_store.py` change, Stage 35 composer, extraction,
route, page, download, template, `ui_text` key, runtime schema, persistence, migration, export history, test, API,
provider, AI, e-mail, attachment processing, deployment or release; no change to the report, PDF, Structured Export,
self-service project export or public API; no Stage 33, 34, 36 or 39 activation; no Master Roadmap stage entry,
checkbox, marker or count change; and no CAP number.
