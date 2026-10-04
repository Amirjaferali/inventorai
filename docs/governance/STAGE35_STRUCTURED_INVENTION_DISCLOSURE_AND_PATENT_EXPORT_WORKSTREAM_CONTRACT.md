# STAGE 35 — STRUCTURED INVENTION DISCLOSURE AND PATENT EXPORT — WORKSTREAM CONTRACT (CANDIDATE)

STATUS: CONTRACT CANDIDATE — DOCUMENTATION ONLY — NO IMPLEMENTATION AUTHORIZED. Records the workstream boundary and the
bounded first-slice shape that the existing Owner decision requires before any implementation. It implements nothing and
authorizes no implementation: no route, page, file generation, export, schema, store, persistence, API, provider, test or
user-facing behaviour is created by this document.
AUTHORITY LEVEL: subordinate governance workstream contract candidate under
[`STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md`](STRUCTURED_INVENTION_DISCLOSURE_AND_PATENT_EXPORT_OWNER_DECISION.md)
(the "Owner decision"), whose §10 requires a separate Owner-authorized workstream or contract before implementation. It
amends neither the Owner decision nor any Register entry, roadmap row or existing export contract.
DESIGNATION: descriptive only — "the disclosure export". No CAP number is assigned.
RECORDED: 2026-10-04, by Owner authorization of a documentation-only Stage 35 workstream contract candidate.
CORRECTION 01: 2026-10-04, by Owner authorization of a documentation-only correction after the Astra architecture review
and the non-authoring Level-1 review, each PASS WITH CONDITIONS; their conditions are folded into §§2–17. The status stays
CONTRACT CANDIDATE. The uncorrected candidate is preserved in Git history (PR #750, merge
`7e32dcb0c9c5d76efb9382f8b9886b2f8f767f8a`).
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
3. Anything beyond that — changed semantics, new derivation, a second implementation of the same logic, a new owner or a
   change to an owner's write path — STOPS, and the gap is reported instead.
4. Public labels for canonical tokens stay with their existing label owner. The export emits canonical tokens and reuses
   those labels; it creates no second label vocabulary. Only the export's own fixed text (headings, section status
   markers, disclaimers, scope label) is new.

## 4A. Coherent source snapshot and failure classes

- The projection represents ONE coherent source snapshot of the ONE requested project: every section is read from the same
  committed project state, and the implementation proves that the state did not change between the first and the last
  read. If coherence cannot be shown, the download is refused. Records from different project revisions are never combined
  into one apparently coherent document.
- **Export-level refusal** (bounded error, no file, no partial output): authentication or authorization failure;
  project-binding failure (any record not bound to the requested project); snapshot incoherence; an inconsistent source
  history (for example a broken supersession chain or an anchor defect); a global integrity or schema failure (an unknown
  token, a schema violation).
- **Section-level `UNAVAILABLE`** is limited to a section-local read failure of one source that leaves every other section
  coherent and correctly bound. A refusal-class failure never degrades to a section-level `UNAVAILABLE`.
- Source tokens, revision identities and the content digest (§9) let the owner compare later exports. They do not imply
  authenticity, approval, validation, notarization, a legal timestamp or priority.

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

**Field map.** Every disclosure field of the Owner decision §2 has exactly one first-slice disposition:

| Owner decision §2 field | First-slice disposition |
|---|---|
| Invention title | `NOT_CAPTURED` (never generated; see §17 decision 4) |
| Problem addressed | `RECORDED` through the existing problem-resolution boundary (§6) |
| Background and existing limitations | `NOT_CAPTURED` (never generated; no prior-art search) |
| Invention objective | `NOT_CAPTURED` |
| Technical concept | `RECORDED` from the known mechanism (§6) |
| System, component, process and method descriptions | Integrated project: `RECORDED` for the Owner-stated parts (Stage 15); component descriptions beyond those parts `NOT_CAPTURED`. Any other project: `NOT_CAPTURED` with the reason "In this first slice, InventorAI captures component descriptions only for integrated Mechanical + Electrical / Electronics projects." — never `NOTHING_RECORDED` |
| Relationships between components | Integrated project: `RECORDED` from Owner-declared interfaces and dependencies, or `NOTHING_RECORDED` when none is declared. Any other project: `NOT_CAPTURED` with the same reason as the row above |
| Operating sequence or workflow | `NOT_CAPTURED` |
| Alternative embodiments | `NOT_CAPTURED` |
| Materials, dimensions, parameters and operating conditions | `NOT_CAPTURED` as typed values; `RAW_TEXT_ONLY` where the inventor's own wording appears inside a Requirement Landscape statement, reproduced there unparsed. Interface verification-preparation inputs: `EXCLUDED_FROM_FIRST_SLICE` (planning metadata) |
| Novelty and differentiation statements | `NOT_CAPTURED` |
| Unresolved technical issues | `RECORDED` from unresolved gaps (OPEN or PARTIAL) and active Owner-declared contradictions |
| Assumptions | `RECORDED` from CAP-08 |
| Missing information | `RECORDED` from unresolved gaps, inventor-marked unknowns and outstanding routed specialist needs |
| Supporting measurements, tests, diagrams, files and evidence | Technical evidence `RECORDED` (§6); Commercial, Manufacturing and Integration evidence `EXCLUDED_FROM_FIRST_SLICE` (§12); diagrams and files `NOT_CAPTURED` |
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
`UNAVAILABLE` (the read failed). Owner-specific metadata — for example the CAP-11 Form, Source and Validation rows or the
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
  §4 seam rule governs how the boundary is reached. **The known mechanism** is read through the same Section-2 resolution;
- the Owner-stated parts, interfaces and dependencies of an integrated project (Stage 15);
- CAP-08 Owner-declared assumptions, with superseded entries as history;
- CAP-10 Owner-declared contradictions — active pairs, and declarations no longer active marked as history;
- unresolved gaps in their canonical state (OPEN or PARTIAL), inventor-marked unknowns and outstanding routed specialist
  needs, as missing information;
- the Requirement Landscape: each statement with its provenance, status and resolving action. Criticality grades are not
  carried (§8);
- technical evidence items, with their CAP-11 Form, Source and Validation rows kept as three separate rows where the owner
  holds them. Commercial, Manufacturing and Integration evidence is not carried (§12);
- CAP-09 experiments, attributed per value: the objective and what to observe are system-generated (system assertions from
  the existing Section-11 generator); each planning field (success criterion, measurement method, test hypothesis, test
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
  statements as the inventor's own wording.
- `EXCLUDED_FROM_FIRST_SLICE`: Commercial, Manufacturing and Integration evidence; inventor-recorded experiment result
  text; interface verification-preparation inputs.

## 8. Data excluded entirely

Never present in either rendering: patent claims or claim-like text authored by InventorAI; novelty, inventive-step,
patentability or freedom-to-operate opinions; any prior-art statement by InventorAI; AI-written or generated legal or
descriptive prose; the report's proceed / revise verdict; maturity, readiness, Readiness Snapshot and assessment-completeness
states; evidence-quality grades; risk severity grades; Requirement Landscape criticality grades (their authority labels and
heuristic warnings stay with the Requirement Landscape owner); Technical Realization artifacts; calculated values (no
calculation owner is implemented — the shared deterministic calculation and units owner exists only as an accepted
boundary contract of record); the CAP-12 Form Mock-up Advisory (session-only and non-binding); CAP-01 guidance prose;
inventor-stated safety-signal output presented as a safety determination; internal identifiers, account data, e-mail
addresses, credentials, tokens or storage paths; anything belonging to another project or another account.

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
- **Data minimization:** only the §6 data; none of the §8 identifiers or account data.
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

Technical evidence is carried as the owners' recorded text with its CAP-11 rows and envelope. Commercial, Manufacturing and
Integration evidence is `EXCLUDED_FROM_FIRST_SLICE`, because of its confidentiality exposure and because no Owner decision
covers a patent handoff for these categories in the first slice. No attachment, file, image or diagram is uploaded,
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
6. **Coherent snapshot:** a change to the project state between the first and the last read refuses the download.
7. **Envelope fidelity:** every `RECORDED` item carries its content class, source owner and owner-held metadata, and the
   human rendering shows them next to the item; no default value is substituted for missing metadata; no per-item approval
   field or line exists.
8. **Excluded content absent:** with every §8 source populated, none of it appears — in particular no proceed / revise
   verdict, no maturity, readiness, evidence-quality, severity or criticality grade, and no Commercial, Manufacturing or
   Integration evidence; risks appear only as references to unresolved gaps.
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
    its association with its source and validation labels, and round-trips to the identical owner-held value.
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
- **Before implementation:** a UX / behaviour review of the journey, labels, markers and disclaimers in EN / AR (optional
  for this candidate's journey wording).
- **Legal adviser review:** an Owner decision, not a blocker to drafting or accepting this candidate.

Owner decisions still required:

1. Acceptance of this candidate as the workstream contract of record.
2. Export history: accept the first-slice deferral (§11), or require export history now.
3. The two first-slice renderings and their file types (PDF excluded from the first slice).
4. Whether a later slice adds an invention title or the inventor's own original description, only if an existing canonical
   owner already holds it verbatim; never generated.
5. Whether a later slice carries the inventor's recorded experiment result text.
6. Any approval owner, and with it any use of the reserved approval extension point (a later, separately reviewed
   decision).
7. Whether a later slice carries Commercial, Manufacturing or Integration evidence.
8. Implementation authorization of the first slice, and with its delivery the decision whether to enter Stage 35.
9. Legal adviser review of the disclaimer wording before any user release.
10. Separately and not now: any external transfer, API surface, email delivery, provider or AI use, or attachment handling.

## 18. Non-authorization (restated)

This document authorizes no implementation, route, page, download, file generation, export, schema, store, persistence,
export history, approval writer or lifecycle, new canonical owner, test, API, provider, AI, e-mail, attachment processing,
patent drafting, claim generation, prior-art search, legal analysis or legal advice; no change to the report, PDF,
Structured Export, self-service project export or public API; no Stage 33, Stage 34, Stage 36 or Stage 39 activation; no
Master Roadmap stage entry, checkbox, marker or count change; no CAP number; and no deployment or release.
