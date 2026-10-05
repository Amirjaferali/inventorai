# STAGE 35 — STRUCTURED INVENTION DISCLOSURE AND PATENT EXPORT — WORKSTREAM CONTRACT (ACCEPTED)

STATUS: ACCEPTED WORKSTREAM CONTRACT OF RECORD — DOCUMENTATION ONLY — NO IMPLEMENTATION AUTHORIZED. Records the
workstream boundary and the bounded first-slice shape that the existing Owner decision requires before any
implementation. It implements nothing and authorizes no implementation: no route, page, file generation, export, schema,
store, persistence, API, provider, test or user-facing behaviour is created by this document.
AUTHORITY LEVEL: subordinate governance workstream contract under
[`STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md`](STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md)
(the "Owner decision"), whose §10 requires a separate Owner-authorized workstream or contract before implementation. It
amends neither the Owner decision nor any Register entry, roadmap row or existing export contract.
DESIGNATION: descriptive only — "the disclosure export". No CAP number is assigned.
RECORDED: 2026-10-04, by Owner authorization of a documentation-only Stage 35 workstream contract candidate.
CORRECTION 01: 2026-10-04, by Owner authorization of a documentation-only correction after the Astra architecture review
and the non-authoring Level-1 review, each PASS WITH CONDITIONS; their conditions are folded into §§2–17. The status stays
CONTRACT CANDIDATE. The uncorrected candidate is preserved in Git history (PR #750, merge
`7e32dcb0c9c5d76efb9382f8b9886b2f8f767f8a`).
CORRECTION 02: 2026-10-04, by Owner authorization of a documentation-only correction that removes two internal
contradictions found by the Lead's acceptance-readiness re-read: the CAP-11 Form row versus the evidence-quality grade ban
(§5, §6, §7, §8, §12, §15), and system-metadata exclusions versus verbatim quoted inventor content (§8, §11, §15). The
status stays CONTRACT CANDIDATE. The Correction 01 text is preserved in Git history (PR #751, merge
`09000bf63ec56853906c259a6096e6102fce11c6`).
ACCEPTANCE: 2026-10-04, by Owner decision accepting the corrected Stage 35 workstream contract (PR #750 as corrected by
PR #751 and PR #752, merge `bf01bbd1d3bca4a03c87e7cec0b5b892bedc731d`) as the workstream contract of record, recorded
documentation-only; no boundary clause (§§0–16, §18) was changed by the acceptance. This acceptance does NOT enter
Stage 35; does NOT authorize implementation; does NOT authorize the first slice; does NOT activate patent export; does NOT
authorize export history; does NOT create or activate an approval workflow; does NOT authorize external transfer; does
NOT authorize API, provider or AI use; does NOT authorize email delivery (Stage 33); does NOT activate Stage 34, Stage 36
or Stage 39; does NOT authorize attachment processing; gives no legal advice; authorizes no patent claims drafting; makes
no patentability, prior-art, freedom-to-operate, legal-validity or filing-ready claim; assigns no CAP number; and changes
no Master Roadmap checkbox, marker or stage count. Of the §17 Owner decisions only decision 1 (acceptance) is taken;
decisions 2–10 stay OPEN.
VERIFICATION BASIS (truthful): the Astra architecture review returned PASS WITH CONDITIONS; the non-authoring Level-1
semantic review returned PASS WITH CONDITIONS; CORRECTION 01 (PR #751) addressed those conditions; CORRECTION 02
(PR #752) closed the final two internal contradictions; the final acceptance-readiness verification was a Lead / executor
re-read by the author of the corrections, not a new independent architecture review; and no additional full review was
required under the bounded-correction / no-review-recursion disposition.
FUTURE IMPLEMENTATION PREREQUISITES: any first implementation increment still requires (1) a separate Owner implementation
authorization; (2) an implementation contract; (3) the §5 source-to-envelope mapping; (4) compliance with the §4 seam
rule; (5) the UX / behaviour review before implementation; (6) independent verification; and (7) successful focused /
local checks plus hosted mandatory CI and the Sharded FULL suite on the implementation head. Stage 35 may be entered only
when an Owner-authorized product slice is delivered, and only by explicit Owner decision.
CORRECTION 03: 2026-10-04, by Owner authorization of a documentation-only snapshot-coherence authority clarification of
the accepted contract. It changes only §4 (the seam rule gains the bounded snapshot-participation adjustment and its
IR-01 invariant), §4A (coherence means one stable, observed, committed SQLite snapshot) and §15 requirement 6; every
other clause, the acceptance and the §17 decision states are unchanged, and the status stays ACCEPTED WORKSTREAM
CONTRACT OF RECORD. Basis: preparation of the first-slice implementation contract found that six readers the first slice
needs refuse inside the existing `read_snapshot()`, and no implementation contract was written; the Astra architecture
review and the independent non-authoring Claude reviewer each returned PASS WITH CONDITIONS on the bounded store-owned
snapshot-participation option (R1), and both rejected a second consistency mechanism (R2) and a narrowed first slice
(R3). Both preserved the Section 11 evidence-quality wording issue as a separate, later source-to-envelope mapping
issue; this correction does not resolve it. Correction 03 does NOT authorize product implementation, any modification of
`engine/record_store.py`, creation of the Stage 35 composer, a route, page or download, a runtime schema, a persistence
migration, export history, Stage 35 entry, deployment or the merge of any product change; it only fixes the authority
boundary so that a later implementation contract may describe the reviewed R1 solution. The pre-correction text is
preserved in Git history (PR #753, merge `2ef9ad9508253418f2018fec2999e5a12788467c`).
CORRECTION 04: 2026-10-04, by Owner decision on the review of the first-slice implementation contract candidate (PR #755;
the Astra architecture review fast-stopped on one failure-class defect of that candidate, and the independent Claude
reviewer returned PASS WITH CONDITIONS). Documentation only. It changes only: §5 (the Problem addressed and Materials,
dimensions, parameters and operating conditions rows), §6 (the problem-capture limitation, the requirement-quantity
bullet and the CAP-09 objective exception), §7 (the `RAW_TEXT_ONLY` bullet and the `reasoned_leading_claim` objective
exclusion) and §17 (decisions 2 and 3 ACCEPTED). Owner dispositions recorded with it: OD-A — owner-recorded requirement
quantities are carried in the first slice as opaque quoted inventor content; OD-B — Stage 15 interface observations are
omitted from the first slice (no seventh snapshot reader); OD-C — technical evidence stays as mapped (no Stage-3 reasoning
evidence or known boundaries are added to it); OD-D — the existing problem-resolution boundary stays, with a fixed
problem-capture limitation. Every other clause, the acceptance and decisions 1 and 4–10 are unchanged, and the status
stays ACCEPTED WORKSTREAM CONTRACT OF RECORD. Correction 04 does NOT authorize implementation, enter Stage 35, activate
CAP-13 or any calculation / units owner, create a typed-parameter owner, authorize export history, or authorize any
route, page, download, schema, persistence, migration, deployment or release. The pre-correction text is preserved in
Git history (PR #754, merge `0ab87dca9ab5abebc03da791d288d661727d7858`).
CORRECTION 05: 2026-10-04, by Owner authorization of a documentation-only UX correction after the UX / behaviour review
of the first-slice implementation contract candidate (PR #755) returned PASS WITH CONDITIONS (C1–C4); the architecture
review and the non-authoring semantic verification of that candidate are complete. It changes only §4 rule 4
(neutral export-only labels), §5 (contextual wording for envelope `NOT_APPLICABLE` rows) and §13 (one "How to read this
document" block and one fixed Risks clarification). These are presentation and explanation only: no token, marker,
truth, data, source, owner, persistence, mapping, legal conclusion, risk assessment or architecture changes, and no
label of any other product surface changes. Every other clause and every §17 decision state is unchanged, and the
status stays ACCEPTED WORKSTREAM CONTRACT OF RECORD. The pre-correction text is preserved in Git history (PR #755,
commit `adffbbf6b695e866dc80bfc4381fca5e66edb8d4`).
*(Superseded 2026-10-04 by the Owner's acceptance, preserved — was: "STATUS: CONTRACT CANDIDATE — DOCUMENTATION ONLY —
NO IMPLEMENTATION AUTHORIZED."; the title read "(CANDIDATE)" and the authority level read "subordinate governance
workstream contract candidate".)*
BASIS: the Lead's read-only post-CAP-13 roadmap selection reassessment and the Lead's read-only Stage 35 reassessment
(Stage 35 viable as the next bounded product direction; the disclosure package is distinct from the report, PDF and
Structured Export; a documentation-only workstream contract is the smallest safe next step), and the two reviews named in
CORRECTION 01. Those reassessments and reviews are session-level review inputs held in Git / GitHub and the Owner's
records, not committed repository authority.

---

## 0. Preserved truth (binding; unchanged by this contract)

- `ACTIVE CONTRACT: NONE`. This contract is not a product increment and fills no active-contract slot.
- Stage 35 (Patent export) stays NOT ENTERED and NOT AUTHORIZED. This candidate enters no Master Roadmap stage; its
  acceptance would not enter one either. At recording (2026-10-04) the Master Roadmap kept 45 top-level stages with
  23 / 45 incomplete and the MASTER ROADMAP SEQUENTIAL MARKER on Stage 25 for navigation only; this contract changes no
  checkbox, marker or count.
- The Owner decision stays non-activating and authoritative for the capability; this contract narrows nothing in it (§9 of
  the Owner decision) and does not represent it as implemented.
- The disclosure export is not legal advice, not a patentability opinion, not a prior-art search or clearance, not a
  freedom-to-operate opinion and not a filing-ready patent application, and InventorAI drafts no patent claim in it.
- No external transfer, API integration, provider, platform or AI use is authorized. Real invention, project and user data
  stays NOT AUTHORIZED for external transmission.
- Stage 33 (email delivery of output artifacts) stays NOT AUTHORIZED; Stage 36 stays deferred; the accepted rule that
  generated substantive output is English stays in force (Stage 34 unchanged); Stage 39 is neither activated nor
  pre-empted (§11).
- The report / deliverable, the PDF, the Structured Export, the self-service project export and the versioned public read /
  export API (whose public surfaces stay exactly the two P7-I2 surfaces) are unchanged by this contract and must stay
  unchanged by the first slice.
- Deployment, public release and paid activation stay NOT AUTHORIZED.

## 1. Product scope

The workstream covers the two future capabilities the Owner decision records:

1. **A structured invention-disclosure package** — the inventor's invention described in disclosure order, built only from
   information InventorAI already holds with its provenance and owner-held validation and limitation state (Owner decision
   §2, §5).
2. **An export artifact** — that package in a versioned form designed for a later handoff to a SEPARATE patent-drafting
   platform or workflow (Owner decision §3). The handoff itself is not part of this workstream's first slice.

InventorAI never gives legal advice through the disclosure export, never generates or drafts patent claims, never performs
or implies a prior-art search or clearance, never assesses novelty, inventive step, patentability or freedom to operate,
never produces a filing-ready document and never hard-codes a jurisdiction, filing format or filing provider (Owner
decision §3, §4, §6).

## 2. Duplication boundary versus report / PDF / Structured Export

| Existing surface | What it is | Why the disclosure export is different |
|---|---|---|
| Report / deliverable and PDF | An **assessment** of the invention (maturity, assessment overview, requirements, assumptions, risks, the proceed / revise verdict, unresolved items, reasoning, next steps, prototype test plan, next development step, Requirement Landscape, Validation Plan) | The disclosure export **describes the invention** in invention-description order for a later handoff; it carries no verdict and no maturity, readiness, evidence-quality, severity or criticality grade, and it marks every disclosure field InventorAI does not own (§5) |
| Structured Export (P7-I1), the self-service project export (P10-D3a) and the public read / export API (P7-I2) | Governed, machine-readable projections of the project record and its support state | The disclosure export is organized by the Owner decision's disclosure fields, carries the per-item envelope (§5) and the mandatory disclaimers (§10), and is not an API surface |

Binding rules:

1. **Projection, not a second assembler.** The disclosure export only selects, orders and labels values that existing
   canonical owners already produce, through a closed field map (§5). It derives, infers, synthesizes, summarizes, ranks,
   re-words or re-computes nothing. Any component that would derive new truth is outside this contract.
2. **Reuse before create.** It reads the same canonical owners the report and the Structured Export already read, on the
   P7-I3 adapter pattern (`engine/export_adapter.py`: pure deterministic transform, bounded explicit error, no state
   mutation), under the seam rule of §4. It never uses a presentation string of the report as source truth.
3. **No surface change.** It does not alter the report, the PDF, the Structured Export, the self-service project export
   or the public API, and it is not folded into any of them (Owner decision §9).
4. **No significance relabelling.** The report's proceed / revise verdict, maturity levels, readiness states, the
   Readiness Snapshot, evidence-quality grades, risk severity grades, Requirement Landscape criticality, gap closure and any
   `INSUFFICIENT_EVIDENCE` state are never exported and never presented as patent, legal, novelty or commercial
   significance.

## 3. Bounded first slice (only if separately authorized)

**First-slice scope (exact).** For ONE project owned by the authenticated account, on the owner's explicit request, the
first slice composes exactly ONE disclosure projection from ONE coherent source snapshot (§4A) — deterministically, from
canonical owner-produced data only (§6), with an explicit section status marker for every disclosure field (§5), the
per-item envelope of owner-held provenance, validation and limitation metadata (§5), versioned disclosure and export
schemas (§9) and the mandatory disclaimers (§10) — and offers it as an owner-private, project-scoped LOCAL DOWNLOAD only.
It uses no AI, no provider, no API, no external transfer and no attachments, retains no export artifact, creates no
export-history record and changes no stored state.

Shape:

- one machine-readable, versioned file of the projection; and one human-readable, self-contained document rendered solely
  from the same projection with no added content. Exact file types are fixed by the implementation authorization; PDF
  rendering is NOT part of the first slice.
- the disclaimers (§10) are shown before the download control and are carried inside both renderings.
- schema version 1 carries no per-item approval field and the human rendering prints no per-item approval line (§5).
- the page states only the factual retention behaviour of §11.

## 4. Architecture and seam boundary

- A read-only projection on existing seams (§2 rules 1–2). No new owner of invention truth, no new store, table, sidecar or
  schema migration, no new persistence of any kind.
- No new public API surface (the P7-I2 public surfaces stay exactly two), no email delivery (Stage 33), no Stage 36
  integration, no provider port, no MCP or external-tool path.
- No change to progression, gaps, readiness, evidence, validation, NeedRouting, decisions, assumptions, contradictions,
  experiments or any owner's semantics. Reading for the disclosure export never mutates state.
- Composition is bounded by the size of the one project; no unbounded or super-linear joins.

**Seam rule (pre-decided).**

1. A canonical seam is an engine-level owner read. A web-layer helper is NOT a canonical seam — for example the Stage 19
   execution-state projection (`web/app.py` `_experiment_execution_states`) and the Stage 21 declared-conflict view
   (`web/app.py` `_declared_conflict_view`) — and neither is a private engine helper reached across modules, such as the
   Section-2 problem resolution (`engine/deliverable_assembler.py` `_resolved_problem`).
2. Inside a future authorized implementation slice, and only there, a behaviour-preserving extraction of such a pure
   helper into an engine-level function is permitted under the existing opportunistic-modularization rule, provided the
   report, the PDF and every other surface that already uses the helper stay byte-identical for the same fixtures.
3. Anything beyond that and the bounded snapshot-participation adjustment below — changed semantics, new derivation, a
   second implementation of the same logic, a new owner or a change to an owner's write path — STOPS, and the gap is
   reported instead.
4. Public labels for canonical tokens stay with their existing label owner. The export emits canonical tokens and reuses
   those labels; it creates no second label vocabulary. Only the export's own fixed text (headings, section status
   markers, disclaimers, scope label, and the Correction 05 explanatory text of §5 and §13) is new.
   **Exception (Correction 05).** Because the human-readable rendering can be shared with third parties, it may show a
   neutral, export-only label for an existing canonical source or content token, and a neutral export-only equivalent
   of a reused product label whose wording addresses the reader in the second person (for example `OWNER_STATED`
   rendered as "Inventor" / "المخترع" instead of the product label "You" / "أنت"). This is presentation only: the
   token, its canonical owner, its provenance and validation meaning, the machine-readable file and every other product
   surface's labels are unchanged.

**Bounded snapshot-participation adjustment (Correction 03).** The existing `engine/record_store.py` `read_snapshot()`
stays the only coherence mechanism (§4A). Six existing readers the first slice needs refuse inside it today, because
their `_refuse_uncommitted_reads()` guard treats the store's own healthy read snapshot as an open transaction:

1. `load_interface_dependencies`
2. `load_success_criteria`
3. `load_measurement_methods`
4. `load_test_hypotheses`
5. `load_test_variables`
6. `load_result_events`

Inside the separately authorized first-slice implementation, and only there, a narrowly bounded adjustment of that
persistence owner is permitted so that exactly these six readers can take part in ONE store-owned healthy read snapshot.
It may consist only of private, store-owned evidence of the lifetime and ownership of a snapshot that `read_snapshot()`
itself opened; one private snapshot-aware reader admission guard; and the use of that guard by the six readers above and
by no other reader, writer or confirmation reader. Each of the six keeps its query semantics, ordering, validation,
project binding and corruption / failure behaviour. No second consistency mechanism is introduced — no change counter,
revision token, re-read-and-compare or retry. The adjustment governs reader admission only: no new store, sidecar or
durable state, and no table, schema, migration, data-model or storage-layout change.

**IR-01 invariant (binding).** Never expose this connection's uncommitted or unsafe write state as durable truth. The
adjustment therefore:

- refuses whenever the sticky unsafe state (`_connection_unsafe`) is set;
- refuses inside a write transaction the caller opened;
- never treats `_connection_unsafe == False` alone as proof that a read is safe, and does not copy the flag-only guard
  of `load_project_subsystems` onto the six readers;
- grants snapshot-aware admission only after `read_snapshot()` has itself acquired a store-owned read snapshot from a
  safe, transaction-resolved connection — never on its no-op branch, which opens nothing when the connection is not
  committed-state-readable;
- keeps every writer and every `committed_*` confirmation reader exactly as strict as today;
- keeps each of the six readers' existing refusal of a bare open transaction when no store-owned snapshot is held;
- never reconnects, repairs, retries or silently switches to another snapshot to hide a snapshot failure; and
- refuses the export when snapshot integrity is lost.

`_refuse_uncommitted_reads()` and `committed_state_readable()` are not relaxed globally. This adjustment is a boundary
for a future authorized implementation only; Correction 03 itself changes no code (see the header).

## 4A. Coherent source snapshot and failure classes

- The projection represents ONE coherent source snapshot of the ONE requested project: the export reflects one stable,
  observed, committed SQLite snapshot for all included source reads, acquired through the existing `read_snapshot()`
  (§4, bounded snapshot-participation adjustment). Every value in one export comes from that same snapshot; values from
  different committed states are never mixed into one apparently coherent document; this connection's own uncommitted
  state is never read; and nothing is read for the export after the snapshot ends.
- A commit by another connection after the snapshot is established does not make the in-progress export switch to the
  newer state and does not by itself refuse the export: newer committed state is not an error. Whether the store's
  SQLite locking makes that commit wait for the snapshot to end or lets it complete alongside the snapshot, the
  in-progress export does not see it. A later export, in a new snapshot, may observe the later committed state.
- If the snapshot cannot be acquired from a safe, transaction-resolved connection, or its integrity is lost before the
  last source read, the download is refused; it is never continued, retried on another snapshot or silently repaired.
- "Snapshot" names a read view only. No legal, durable or per-project revision identity exists or is implied.
- **Export-level refusal** (bounded error, no file, no partial output): authentication or authorization failure;
  project-binding failure (any record not bound to the requested project); failure to acquire or maintain the snapshot;
  an inconsistent source history (for example a broken supersession chain or an anchor defect); a global integrity or
  schema failure (an unknown token, a schema violation).
- **Section-level `UNAVAILABLE`** is limited to a section-local read failure of one source that leaves every other section
  coherent and correctly bound. A refusal-class failure never degrades to a section-level `UNAVAILABLE`. A document with
  any `UNAVAILABLE` section may carry one fixed top-level sentence: "One or more sections of this document could not be
  read and are marked Unavailable."
- Source tokens and the content digest (§9) let the owner compare later exports. They do not imply authenticity,
  approval, validation, notarization, a legal timestamp, priority or a durable project revision identity.

## 5. Disclosure schema (conceptual; no frozen field names)

**Section status markers (closed).** Every disclosure field carries exactly one; each has its own fixed wording, and none
is ever rendered as "none", empty, zero, blank or omitted:

| Marker | Meaning | Fixed English wording |
|---|---|---|
| `RECORDED` | The owner was read and holds items for this project | (the items) |
| `NOTHING_RECORDED` | The owner was read and holds no item for this project | "Nothing recorded in this project" |
| `NOT_CAPTURED` | InventorAI has no owner for this information | "Not captured by InventorAI", plus the field's fixed reason where §5 gives one |
| `RAW_TEXT_ONLY` | The information appears only as the inventor's own raw text inside another carried section; it is not typed, normalized or interpreted | "Only as the inventor's own wording in" + the named section |
| `EXCLUDED_FROM_FIRST_SLICE` | InventorAI holds related information, but this slice deliberately does not export it | "Not included in this export", plus the field's fixed reason |
| `NOT_APPLICABLE` | The field or metadata does not apply to this kind of source or item | "Not applicable" |
| `UNAVAILABLE` | A section-local source read failed (§4A) | "Unavailable — this information could not be read" |

`NOT_APPLICABLE` is used for envelope metadata and only for the section cases the implementation contract names; it never
replaces `NOT_CAPTURED` or `NOTHING_RECORDED`. `UNAVAILABLE` is never rendered as nothing recorded or not captured.

**Envelope-row context (Correction 05).** In the human rendering, a `NOT_APPLICABLE` envelope-metadata row (Source,
Validation, Limitation, Currency) may carry a fixed contextual explanation that no separate value of that kind is held
for the item, so that the marker is not read as "no limitation", "no source needed" or "no validation needed". The
marker token and its field-level wording "Not applicable" are unchanged, and no new marker or state is created.

**Field map.** Every disclosure field of the Owner decision §2 has exactly one first-slice disposition:

| Owner decision §2 field | First-slice disposition |
|---|---|
| Invention title | `NOT_CAPTURED` (never generated; see §17 decision 4) |
| Problem addressed | `RECORDED` through the existing problem-resolution boundary, with the fixed problem-capture limitation (§6) |
| Background and existing limitations | `NOT_CAPTURED` (never generated; no prior-art search) |
| Invention objective | `NOT_CAPTURED` |
| Technical concept | `RECORDED` from the known mechanism (§6) |
| System, component, process and method descriptions | Integrated project: `RECORDED` for the Owner-stated parts (Stage 15); component descriptions beyond those parts `NOT_CAPTURED`. Any other project: `NOT_CAPTURED` with the reason "In this first slice, InventorAI captures component descriptions only for integrated Mechanical + Electrical / Electronics projects." — never `NOTHING_RECORDED` |
| Relationships between components | Integrated project: `RECORDED` from Owner-declared interfaces and dependencies, or `NOTHING_RECORDED` when none is declared. Any other project: `NOT_CAPTURED` with the same reason as the row above |
| Operating sequence or workflow | `NOT_CAPTURED` |
| Alternative embodiments | `NOT_CAPTURED` |
| Materials, dimensions, parameters and operating conditions | `NOT_CAPTURED` as typed values (no typed-parameter owner exists). Owner-recorded requirement quantities: `RECORDED` as opaque quoted inventor content (§6), never parsed, normalized, converted, calculated or typed. Only when the requirement-quantity owner holds no quantity for the project: `RAW_TEXT_ONLY` where the inventor's own wording appears inside a Requirement Landscape statement, reproduced there unparsed. Interface verification-preparation inputs: `EXCLUDED_FROM_FIRST_SLICE` (planning metadata) |
| Novelty and differentiation statements | `NOT_CAPTURED` |
| Unresolved technical issues | `RECORDED` from unresolved gaps (OPEN or PARTIAL) and active Owner-declared contradictions |
| Assumptions | `RECORDED` from CAP-08 |
| Missing information | `RECORDED` from unresolved gaps, inventor-marked unknowns and outstanding routed specialist needs |
| Supporting measurements, tests, diagrams, files and evidence | Technical evidence `RECORDED` with its CAP-11 Source and Validation rows (§6); the CAP-11 Form row `EXCLUDED_FROM_FIRST_SLICE` (§6); Commercial, Manufacturing and Integration evidence `EXCLUDED_FROM_FIRST_SLICE` (§12); diagrams and files `NOT_CAPTURED` |
| Prototype status and validation results | Experiments and their execution state `RECORDED`; inventor-recorded result text `EXCLUDED_FROM_FIRST_SLICE`; validation results `NOT_CAPTURED` |
| Risks, uncertainty and abstentions | Risks `RECORDED` only as references to unresolved gaps (§6); uncertainty only as each item's owner-held validation state and limitation text |
| Inventor-entered corrections and approvals | Corrections `RECORDED` as supersession history; approvals `NOT_CAPTURED` with the sentence "InventorAI holds no inventor-approval record; this is not a statement that approval was withheld." |
| Source and provenance references | Carried on every item (envelope below) |

The Requirement Landscape is carried as its own `RECORDED` section (§6).

**System assertions versus quoted inventor content.** Every rendered value is exactly one of:

- a **system assertion** — InventorAI-authored or system-owned text: the export's fixed text (headings, markers,
  disclaimers, labels) and canonical system-generated statements such as gap labels and system-generated experiment
  objectives; or
- **quoted inventor content** — text the inventor wrote, reproduced verbatim and structurally and visibly marked as the
  inventor's words, next to its source label.

The prohibition on affirmative legal and patent assertions (§10) binds system assertions. Quoted inventor content is never
silently redacted, rewritten, filtered or classified, and no legal-content classifier is introduced: claim-like or legal
wording inside quoted inventor content is the inventor's own text, not an InventorAI statement. Verbatim preservation
holds at the text-value level: once its serialization is decoded, the value is identical to the text the owner holds. Safe
serialization, escaping and neutral quoting are allowed; Unicode normalization, trimming, case change, translation and any
treatment of inventor text as markup, script, link, formula or template are forbidden.

**Item envelope (every `RECORDED` item).** The verbatim value; its content class (system assertion or quoted inventor
content); its source owner (closed token); and its provenance, validation state, limitation text and currency exactly as
the owner holds them — `LEGACY_UNSPECIFIED` stays as it is and nothing is upgraded or reclassified. For each envelope field
the value is the owner-held value, `NOT_APPLICABLE` (the owner holds no such metadata for this kind of item) or
`UNAVAILABLE` (the read failed). Owner-specific metadata — for example the CAP-11 Source and Validation rows or the
Stage 19 execution state — travels under that owner's own tokens and is never mapped into a generic field. `UNVALIDATED`,
`OWNER_STATED`, `CURRENT` or any other value is never substituted merely to fill a field. Uncertainty is represented only by
owner-held validation state and limitation text; no uncertainty scale, score or level is derived.

**Approval.** Schema version 1 carries no per-item approval field, and the human rendering prints no per-item approval
line. The Owner decision §3 "version and approval metadata" is preserved only as a reserved, versioned extension point: a
later schema version may add approval metadata only after a separately authorized approval owner exists. This contract
creates no approval writer, approval lifecycle or implied approval system.

**Source-to-envelope mapping (required before implementation).** The implementation contract carries one bounded table
that maps each source owner and item kind to: its content class; its source-owner token; the envelope fields that owner
actually holds; the owner-specific metadata carried; how currency is determined; and the fields that are `NOT_APPLICABLE`.
A source without a row in that table is not read.

## 6. Data allowed from existing owners (first slice)

Composed verbatim, each item with its envelope:

- **the known problem**, read only through the existing problem-resolution boundary that the report's Section 2 uses
  (`engine/deliverable_assembler.py` `_resolved_problem`, which deliberately does not use `state.known_problem` because
  RISK-002 can populate that field from a mechanism answer). Reading `state.known_problem` directly is not authorized; the
  §4 seam rule governs how the boundary is reached. The problem item always carries, next to the problem text, ONE fixed
  system-assertion limitation (exact English wording): "InventorAI captures the problem statement at the step where the
  inventor describes the problem and may shorten it at a 500-character limit. The text shown here may therefore have been
  shortened; an ellipsis (…) at its end may indicate that shortening." It discloses the existing capture behaviour of
  that boundary (`engine/progression_loop.py` `_trim_idea_summary`) and is not new engineering truth. It is unconditional:
  truncation is never detected from the text, missing content is never reconstructed, the limitation never states that
  shortening occurred, and the problem text stays quoted inventor content exactly as the owner holds it. **The known
  mechanism** is read through the same Section-2 resolution;
- the Owner-stated parts, interfaces and dependencies of an integrated project (Stage 15);
- CAP-08 Owner-declared assumptions, with superseded entries as history;
- CAP-10 Owner-declared contradictions — active pairs, and declarations no longer active marked as history;
- unresolved gaps in their canonical state (OPEN or PARTIAL), inventor-marked unknowns and outstanding routed specialist
  needs, as missing information;
- the Requirement Landscape: each statement with its provenance, status and resolving action. Criticality grades are not
  carried (§8);
- owner-recorded requirement quantities (`engine/requirement_quantity.py`, read through the existing store reader
  `load_requirement_quantities`, which takes part in the existing `read_snapshot()` today and is not one of the six §4
  readers): each stored `value_text` as opaque quoted inventor content exactly as the owner holds it, with its closed
  `quantity_kind` token, the owner's own provenance, validation state and chain state, and a reference to the Requirement
  Landscape row of its anchoring answer while that answer is active. The value is never parsed, unit-split, normalized,
  converted, calculated, typed or interpreted, and it is not repeated inside any Requirement Landscape item. No
  typed-parameter owner, calculation / units owner or CAP-13 behaviour is created or activated;
- technical evidence items, with their CAP-11 Source and Validation rows kept as two separate rows where the owner holds
  them. The CAP-11 Form row is `EXCLUDED_FROM_FIRST_SLICE` with the fixed reason "Excluded from this first slice because
  the Form row is derived from the evidence-quality field, and this disclosure export does not carry evidence-quality
  grades." Commercial, Manufacturing and Integration evidence is not carried (§12);
- CAP-09 experiments, attributed per value: the objective and what to observe are system-generated (system assertions from
  the existing Section-11 generator), except that the objective of a `reasoned_leading_claim` experiment is
  `EXCLUDED_FROM_FIRST_SLICE` (§7); each planning field (success criterion, measurement method, test hypothesis, test
  variable / condition) carries the attribution its owner records, so an inventor-written value is quoted inventor content
  and a system-provided value is a system assertion; and the Stage 19 execution state (`NO RESULT`, `RECORDED N` or
  `UNAVAILABLE`), a system-derived count of the inventor's own unvalidated records;
- risks, only as references to unresolved gaps already carried under unresolved technical issues — no risk statement,
  severity, maturity, readiness, assessment-completeness or evidence-quality risk;
- correction / supersession history, with the current value marked.

## 7. Data not captured, raw text only, or excluded from the first slice

- `NOT_CAPTURED`, never generated or inferred: invention title; background and existing limitations; invention objective;
  operating sequence or workflow; component descriptions beyond the owned Stage-15 parts, and component descriptions and
  relationships of any project that is not an integrated composition; alternative embodiments (CAP-05 / CAP-07 decision
  alternatives are design-decision alternatives and are never relabelled as embodiments); typed materials, dimensions,
  parameters and operating conditions (no typed-parameter owner exists); novelty and differentiation statements (Stage-17
  commercial differentiation evidence is never relabelled as technical novelty); diagrams, files and attachments;
  validation results; inventor approval.
- `RAW_TEXT_ONLY`: materials, dimensions, parameters and operating conditions that appear only inside Requirement Landscape
  statements as the inventor's own wording — used only when the requirement-quantity owner holds no quantity for the
  project; when it holds one, its quantities are `RECORDED` (§6) and no "only in the Requirement Landscape" statement is
  made.
- `EXCLUDED_FROM_FIRST_SLICE`: the CAP-11 Form row of technical evidence items; Commercial, Manufacturing and
  Integration evidence; inventor-recorded experiment result text; interface verification-preparation inputs; and the
  generated objective of a `reasoned_leading_claim` experiment (`reasoned_leading_claim.objective`), with the fixed reason
  "Excluded from this first slice because this generated objective names an evidence-quality level, and this disclosure
  export does not carry evidence-quality grades." — the source objective names evidence-quality levels (§8). Only that
  slot is excluded; the rest of the experiment is carried. Rewording, sanitizing or replacing that source text stays
  prohibited, and no grade value is exported.

## 8. Data excluded entirely

Never present in either rendering: patent claims or claim-like text authored by InventorAI; novelty, inventive-step,
patentability or freedom-to-operate opinions; any prior-art statement by InventorAI; AI-written or generated legal or
descriptive prose; the report's proceed / revise verdict; maturity, readiness, Readiness Snapshot and
assessment-completeness states; evidence-quality grades, including any CAP-11 Form value (derived from the
evidence-quality field; its place shows only the §7 `EXCLUDED_FROM_FIRST_SLICE` marker); risk severity grades;
Requirement Landscape criticality grades (their authority labels and heuristic warnings stay with the Requirement
Landscape owner); Technical Realization artifacts; calculated values (no calculation owner is implemented — the shared
deterministic calculation and units owner exists only as an accepted boundary contract of record); the CAP-12 Form
Mock-up Advisory (session-only and non-binding); CAP-01 guidance prose; inventor-stated safety-signal output presented
as a safety determination; system-held metadata — account metadata, session metadata, storage metadata, internal
identifiers, system-held credentials, system-held tokens, system-held storage paths and system-owned e-mail or account
data, and any other InventorAI-authored or system-owned field outside the §6 data; anything belonging to another project
or another account.

The system-held metadata exclusion never filters, redacts, scans or classifies quoted inventor content. Inventor text
that itself contains an e-mail address, a token-like string, a path or similar wording is reproduced verbatim under the
§5 quoted-content rules, with safe escaping and neutral quoting.

## 9. Export schema and versioning

- Two version identities travel with every export: the **disclosure schema version** (the field map, markers and envelope
  of §5) and the **export format version** (the serialization). Any change to a field, token or meaning yields a new
  version; a version is never silently reused. Approval metadata is a reserved extension point only (§5).
- Machine-readable keys are language-neutral, closed and stable; unknown keys are never emitted. This contract freezes no
  final field names; the implementation contract freezes version 1.
- The disclosure export is not the Structured Export, not the self-service project export, not the public API
  representation and not the deliverable package.
- Determinism: one coherent snapshot and identical versions yield byte-identical projection content in every locale; the
  locale changes the human rendering only. A generation timestamp, if carried, sits in a declared metadata field outside
  the content digest. No randomness, clock dependence or network dependence affects content.
- A content digest of the projection is carried as an integrity aid for later comparison only (§4A); it excludes the
  timestamp.
- File names contain no inventor-authored text.

## 10. Legal boundary and mandatory disclaimers

Mandatory English disclaimer wording (exact), carried verbatim in both renderings and in both locales, and shown before the
download control:

1. "This document is not legal advice. InventorAI does not provide legal services."
2. "This document is not a patentability opinion. InventorAI has not assessed whether this invention is new, inventive or
   patentable."
3. "This document is not a prior-art search. InventorAI has not searched for or cleared prior art."
4. "This document is not a freedom-to-operate opinion."
5. "This document is not a filing-ready patent application."
6. "InventorAI has not drafted or generated any patent claim in this document. Any claim-like wording appears only inside
   text quoted from the inventor, reproduced as written and not assessed. Nothing in this document is a legally valid
   claim."
7. "Evidence recorded here is not a validated conclusion. Items marked unvalidated have not been checked by InventorAI."
8. "This document does not establish a conception date, an invention date, priority, inventorship or ownership."
9. "Any digest or date in this document is an integrity aid only. It is not a legal timestamp, a notarization or proof of
   priority."
10. "Sharing this document may count as a disclosure of the invention in some jurisdictions. Consult a qualified patent
    professional before sharing it."
11. "For legal advice, consult a qualified patent professional."

Conditional disclaimer (any later version that carries an inventor novelty or differentiation statement, verbatim):
"Novelty and differentiation statements here are the inventor's own words. InventorAI has not assessed them." In the first
slice such statements are `NOT_CAPTURED`, so this disclaimer does not render.

Exact scope label: "Invention disclosure export — this project only — not legal advice".

The prohibition on affirmative legal and patent assertions binds system assertions (§5); quoted inventor content is
reproduced as written. No jurisdiction, filing format, patent office or filing provider is named or assumed.

Arabic wording of the disclaimers, scope label and markers supplements the exact English disclaimers: in the Arabic locale
the exact English disclaimers stay present and the Arabic wording accompanies them, unless a later UX / legal review
decides otherwise. The Arabic wording is fixed, meaning-preserving, in the implementation contract and verified by the UX /
behaviour review (§13, §16). Whether a legal adviser reviews this wording before any user release is an Owner decision
(§17); it is not a prerequisite for this candidate.

## 11. Consent, privacy, security and retention

- **External transfer:** none. The first slice is an owner-private, project-scoped local download only. Any future
  transfer to a patent-drafting platform needs its own Owner authorization, explicit per-transfer user consent, export
  history before activation, and its own reviews (Owner decision §6, §7).
- **Access:** authenticated owner only, through the existing project-ownership check; a request for a missing project and a
  request for another account's project receive byte-identical denials (P10-D3a precedent); no other project or account is
  ever read into the projection. Existing authentication and session behaviour is preserved.
- **Data minimization:** only the §6 data; none of the §8 system-held metadata. Data minimization selects which owner
  data is read; it never filters, redacts, scans or classifies quoted inventor content, which is reproduced verbatim under
  §5.
- **Consent for the download itself:** the owner's explicit request is the trigger; the disclaimers are shown first;
  viewing them records nothing.
- **Retention, logs and export history (exact):**
  - no disclosure-export artifact is retained — the projection is composed per request in memory, and no server-side copy,
    cache entry or temporary file of the export is kept;
  - no export-history record is created in the first slice. This deferral holds only if the Owner accepts it (§17
    decision 2), and any future transfer capability requires export history before activation;
  - no invention content is written to logs; ordinary redacted operational and access logging may still apply, as for any
    other product request;
  - no disclosure or project state is mutated, and the response is marked not cacheable;
  - retention and deletion of the source data stay with their existing owners; the page states that InventorAI keeps no
    copy of the export file and cannot delete copies the owner has downloaded.
- **Stage 39 non-dependency:** deletion, record and consent-adjacent page statements are factual product-behaviour
  disclosures only; they are not a Privacy Policy, Terms, consent artifact or Stage 39 substitute, and they pre-empt
  nothing in Stage 39.
- **Self-contained output:** the human-readable document loads no external resource (scripts, fonts, images, styles or
  trackers) and carries no executable content; the machine-readable file carries no executable content.

## 12. Evidence and attachment handling

Technical evidence is carried as the owners' recorded text with its CAP-11 Source and Validation rows and its envelope;
the CAP-11 Form row is `EXCLUDED_FROM_FIRST_SLICE` (§6) because it is derived from the evidence-quality field.
Commercial, Manufacturing and Integration evidence is `EXCLUDED_FROM_FIRST_SLICE`, because of its confidentiality
exposure and because no Owner decision covers a patent handoff for these categories in the first slice. No attachment, file, image or diagram is uploaded,
processed, read, embedded, linked for fetching or interpreted; those fields are `NOT_CAPTURED`. Inventor-recorded
experiment result text is `EXCLUDED_FROM_FIRST_SLICE` (only the execution state is carried; §17 decision 5).

## 13. Bilingual, RTL and UX boundary

- Headings, section names, markers, disclaimers, scope label and journey labels are provided in English and Arabic,
  following the UI locale; Arabic renders right-to-left. Arabic disclaimers supplement the exact English disclaimers (§10).
- The locale affects the human rendering only, unless separately authorized: projection content, source identities and
  the content digest are identical across locales.
- Inventor-authored text is preserved verbatim (§5) — never translated, normalized or re-worded. Each inventor value is
  rendered in its own direction-isolated container next to its source and validation labels. The known mixed-direction
  rendering limitation does not waive the correct association of inventor text with its source labels, validation labels
  and the disclaimers.
- Canonical technical statements (for example gap labels and Requirement Landscape statements) stay in their source
  language under the current English-output rule (Stage 34 unchanged); first-use bilingual labelling follows the Owner
  language policy.
- English digits (0–9) are used for identifiers, versions, dates and counts (Owner decision §6).
- Machine-readable keys are language-neutral and versioned (§9); file names contain no inventor-authored text.
- Labels state the scope (this project only) and the non-legal nature plainly; no label, filename or help text may suggest
  a patent application, a filing, legal review or validation.
- **"How to read this document" (Correction 05).** The human rendering may carry exactly ONE fixed explanatory block,
  after the scope label and disclaimers and before the disclosure fields. It explains only the difference between quoted
  inventor content and InventorAI statements (§5) and the existing seven section status markers in their §5 meanings —
  in particular that `NOTHING_RECORDED` means InventorAI holds no record of it in this project, not that it does not
  exist; that `NOT_CAPTURED` means InventorAI does not capture that information; that `EXCLUDED_FROM_FIRST_SLICE` means
  InventorAI holds related information that this bounded export deliberately leaves out; and that `UNAVAILABLE` means
  the information could not be read. It states no conclusion or assessment and adds no marker.
- **Risks clarification (Correction 05).** The Risks field may carry ONE fixed clarification that it only references
  unresolved technical issues already carried in the export and is not an InventorAI risk assessment. No risk score,
  severity, probability, ranking, classification or assessment is added, and the field's source mapping (§5, §6) is
  unchanged.

## 14. Integration boundary

The export is designed so that a later, separately authorized handoff to a separate patent-drafting platform is possible
(versioned schema, provenance envelope, language-neutral keys). The first slice integrates with nothing: no API, platform,
vendor field mapping, email, provider, external tool or Stage 36 path, and no jurisdiction-specific format.

## 15. BASE RED requirements (contract requirements only; no tests are written by this document)

A future implementation must first show these failing, then passing:

1. **Prohibited wording (system assertions):** no system assertion in either rendering, in either locale, contains claim
   language or an assertion of patentability, novelty, inventive step, prior-art clearance, freedom to operate, filing
   readiness, legal validity or legal advice, except inside the exact disclaimer strings. The scan uses an English
   allow-list and an Arabic allow-list of the exact disclaimer strings, and it excludes quoted inventor content, which is
   identified structurally, not by a classifier.
2. **Disclaimers present:** every §10 disclaimer and the scope label appear verbatim in both renderings; the exact English
   disclaimers are present in both locales, with the Arabic wording accompanying them in the Arabic locale; all appear
   before the download control.
3. **Markers:** each §5 marker renders its own fixed wording; an injected section-local read failure renders `UNAVAILABLE`;
   no marker ever renders as "none", empty, zero, blank or omitted; a project that is not an integrated composition renders
   the component and relationship fields as `NOT_CAPTURED` with the fixed reason, never as `NOTHING_RECORDED`.
4. **No external transfer:** composition and download make no network call and import no provider, API client or e-mail
   module.
5. **Project separation and failure classes:** another account's project and a missing project are denied
   byte-identically; a projection never contains a record from another project; every §4A refusal-class failure refuses
   the download with no partial file and never degrades to a section-level `UNAVAILABLE`.
6. **Coherent snapshot:** (a) every source value in one export, including those from the six readers named in §4, comes
   from the same established store-owned snapshot; (b) a commit by another connection attempted after that snapshot is
   established never produces a mixed-state projection — the in-progress export reflects only the snapshot state,
   whether that commit waits for the snapshot to end or completes alongside it; (c) a later export, in a new snapshot,
   observes the later committed state; (d) failure to acquire the snapshot (the sticky unsafe state, a caller-owned open
   write transaction, the no-op branch of `read_snapshot()`) or loss of its integrity before the last source read
   refuses the export; (e) no partial file is produced in any refused case; and (f) the §4 IR-01 invariant holds — each
   of the six readers still refuses the sticky unsafe state and a bare open transaction when no store-owned snapshot is
   held, and writers and `committed_*` confirmation readers are unchanged. Newer committed state alone never refuses the
   download.
7. **Envelope fidelity:** every `RECORDED` item carries its content class, source owner and owner-held metadata, and the
   human rendering shows them next to the item; no default value is substituted for missing metadata; no per-item approval
   field or line exists.
8. **Excluded content absent:** with every §8 source populated, none of it appears — in particular no proceed / revise
   verdict, no maturity, readiness, evidence-quality, severity or criticality grade, no CAP-11 Form row, and no Commercial,
   Manufacturing or Integration evidence; risks appear only as references to unresolved gaps; technical evidence carries
   only its CAP-11 Source and Validation rows.
9. **Known-problem seam:** a state in which `state.known_problem` was populated from a mechanism answer still exports the
   problem resolved by the existing Section-2 boundary.
10. **No mutation:** stored state is identical before and after composition and download; no export-history record exists.
11. **Existing surfaces unchanged:** the report, PDF, Structured Export, self-service project export and public API outputs
    are byte-identical for the same fixtures before and after the implementation, including after any permitted helper
    extraction (§4).
12. **Determinism and versions:** identical state yields identical projection content and digest in both locales; the
    digest excludes the timestamp; both version identities are present.
13. **Hostile inventor text:** inventor text containing markup, script, links, template syntax, bidirectional control
    characters, control characters and very long values is safely escaped, never interpreted as markup or script, keeps
    its association with its source and validation labels, and round-trips to the identical owner-held value; inventor
    text that contains an e-mail address, a token-like string or a path is reproduced verbatim, never redacted, while no
    system-held metadata (§8) appears.
14. **Both locale outputs:** the English and the Arabic human renderings are both produced and both meet requirements 1–3,
    7 and 13.
15. **File names:** no file name contains inventor-authored text.
16. **Self-contained output:** the human-readable document references no external resource.

## 16. Acceptance criteria for a future first slice

The first slice is acceptable only if: the source-to-envelope mapping (§5) exists and has been reviewed; every §15
requirement passes; hosted mandatory CI and the Sharded FULL suite pass on the exact final head; the UX / behaviour review
(EN / AR, RTL, association of inventor text with its labels, comprehension of the disclaimers and markers) passes; the
independent verification finds no derived truth, relabelling, default substitution or surface change; and the Owner
accepts it. Delivery of that slice — not this contract — is the earliest point at which the Owner may decide to enter
Stage 35.

## 17. Review path and Owner decisions

- **Before acceptance of this candidate:** a targeted verification of CORRECTION 01 against the conditions of the Astra
  architecture review and the non-authoring Level-1 review — not a full review restart, unless the scope has expanded.
  DONE before the acceptance as a Lead / executor re-read (see VERIFICATION BASIS in the header), followed by CORRECTION
  02.
- **Before implementation:** a UX / behaviour review of the journey, labels, markers and disclaimers in EN / AR (optional
  for this candidate's journey wording).
- **Legal adviser review:** an Owner decision, not a blocker to drafting or accepting this candidate.

Owner decisions (state as of CORRECTION 04, 2026-10-04):

1. ACCEPTED (2026-10-04) — Acceptance of this candidate as the workstream contract of record.
2. ACCEPTED (2026-10-04, recorded by CORRECTION 04) — Export history: the first-slice deferral (§11) is accepted, limited
   to the local-download first slice; any future external transfer still requires export history before activation.
3. ACCEPTED (2026-10-04, recorded by CORRECTION 04) — The two first-slice renderings: one versioned JSON file and one
   self-contained HTML document generated solely from the same projection; PDF excluded from the first slice.
4. OPEN — Whether a later slice adds an invention title or the inventor's own original description, only if an existing canonical
   owner already holds it verbatim; never generated.
5. OPEN — Whether a later slice carries the inventor's recorded experiment result text.
6. OPEN — Any approval owner, and with it any use of the reserved approval extension point (a later, separately reviewed
   decision).
7. OPEN — Whether a later slice carries Commercial, Manufacturing or Integration evidence.
8. OPEN — Implementation authorization of the first slice, and with its delivery the decision whether to enter Stage 35.
9. OPEN — Legal adviser review of the disclaimer wording before any user release.
10. OPEN — separately unauthorized, and not now: any external transfer, API surface, email delivery, provider or AI use, or attachment handling.

## 18. Non-authorization (restated)

This document authorizes no implementation, route, page, download, file generation, export, schema, store, persistence,
export history, approval writer or lifecycle, new canonical owner, test, API, provider, AI, e-mail, attachment processing,
patent drafting, claim generation, prior-art search, legal analysis or legal advice; no change to the report, PDF,
Structured Export, self-service project export or public API; no Stage 33, Stage 34, Stage 36 or Stage 39 activation; no
Master Roadmap stage entry, checkbox, marker or count change; no CAP number; and no deployment or release.
