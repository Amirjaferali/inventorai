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
BASIS: the Lead's read-only post-CAP-13 roadmap selection reassessment and the Lead's read-only Stage 35 reassessment
(Stage 35 viable as the next bounded product direction; the disclosure package is distinct from the report, PDF and
Structured Export; a documentation-only workstream contract is the smallest safe next step). Those reassessments are
session-level review inputs held in Git / GitHub and the Owner's records, not committed repository authority.

---

## 0. Preserved truth (binding; unchanged by this contract)

- `ACTIVE CONTRACT: NONE`. This contract is not a product increment and fills no active-contract slot.
- Stage 35 (Patent export) stays NOT ENTERED and NOT AUTHORIZED. This candidate enters no Master Roadmap stage; its
  acceptance would not enter one either. The Master Roadmap keeps 45 top-level stages with 23 / 45 incomplete; no checkbox,
  marker or count changes. The MASTER ROADMAP SEQUENTIAL MARKER stays Stage 25 for navigation only.
- The Owner decision stays non-activating and authoritative for the capability; this contract narrows nothing in it (§9 of
  the Owner decision) and does not represent it as implemented.
- The disclosure export is not legal advice, not a patentability opinion, not a prior-art search or clearance, not a
  freedom-to-operate opinion and not a filing-ready patent application, and it contains no patent claims.
- No external transfer, API integration, provider, platform or AI use is authorized. Real invention, project and user data
  stays NOT AUTHORIZED for external transmission.
- Stage 33 (email delivery of output artifacts) stays NOT AUTHORIZED; Stage 36 stays deferred; the accepted rule that
  generated substantive output is English stays in force (Stage 34 unchanged).
- The report / deliverable, the PDF, the Structured Export and the versioned public read / export API (whose public surfaces
  stay exactly the two P7-I2 surfaces) are unchanged by this contract and must stay unchanged by the first slice.
- Deployment, public release and paid activation stay NOT AUTHORIZED.

## 1. Product scope

The workstream covers the two future capabilities the Owner decision records:

1. **A structured invention-disclosure package** — the inventor's invention described in disclosure order, built only from
   information InventorAI already holds with its provenance, uncertainty and approval state (Owner decision §2, §5).
2. **An export artifact** — that package in a versioned form designed for a later handoff to a SEPARATE patent-drafting
   platform or workflow (Owner decision §3). The handoff itself is not part of this workstream's first slice.

The disclosure export never gives legal advice, never generates or drafts patent claims, never performs or implies a
prior-art search or clearance, never assesses novelty, inventive step, patentability or freedom to operate, never
produces a filing-ready document and never hard-codes a jurisdiction, filing format or filing provider (Owner decision
§3, §4, §6).

## 2. Duplication boundary versus report / PDF / Structured Export

| Existing surface | What it is | Why the disclosure export is different |
|---|---|---|
| Report / deliverable and PDF | An **assessment** of the invention (maturity, assessment overview, requirements, assumptions, risks, the proceed / revise verdict, unresolved items, reasoning, next steps, prototype test plan, next development step, Requirement Landscape, Validation Plan) | The disclosure export **describes the invention** in invention-description order for a later handoff; it carries no verdict, readiness or maturity statement and adds explicit "not captured" markers for disclosure fields InventorAI does not own |
| Structured Export (P7-I1) and the public read / export API (P7-I2) | A governed, machine-readable projection of the project record and its support state | The disclosure export is organized by the Owner decision's disclosure fields, carries the per-item provenance / uncertainty / approval envelope (§5) and the mandatory disclaimers (§10), and is not an API surface |

Binding rules:

1. **Projection, not a second assembler.** The disclosure export only selects, orders and labels values that existing
   canonical owners already produce, through a closed field map (§5). It derives, infers, synthesizes, summarizes, ranks,
   re-words or re-computes nothing. Any component that would derive new truth is outside this contract.
2. **Reuse before create.** It reads the same canonical owners the report and the Structured Export already read, through
   their existing read seams, on the P7-I3 adapter pattern (`engine/export_adapter.py`: pure deterministic transform,
   bounded explicit error, no state mutation). It never uses a presentation string of the report as source truth. If a
   required value cannot be read from a canonical owner without changing that owner, the implementation STOPS and reports
   the exact gap; it does not add a parallel reader.
3. **No surface change.** It does not alter the report, the PDF, the Structured Export, the self-service project export
   or the public API, and it is not folded into any of them (Owner decision §9).
4. **No significance relabelling.** The report's proceed / revise verdict, maturity levels, readiness states, the
   Readiness Snapshot, gap closure or any `INSUFFICIENT_EVIDENCE` state are never exported and never presented as patent,
   legal, novelty or commercial significance.

## 3. Bounded first slice (only if separately authorized)

**First-slice scope (exact).** For ONE project owned by the authenticated account, on the owner's explicit request, the
first slice composes exactly ONE disclosure projection — deterministically, from canonical owner-produced data only (§6),
with an explicit "not captured by InventorAI" marker for every disclosure field InventorAI does not own (§7), the
provenance / uncertainty / approval envelope on every item (§5), versioned disclosure and export schemas (§9) and the
mandatory disclaimers (§10) — and offers it as an owner-private, project-scoped LOCAL DOWNLOAD only. It uses no AI, no
provider, no API, no external transfer and no attachments, persists nothing, records nothing and changes no stored state.

Shape:

- one machine-readable, versioned file of the projection; and one human-readable, self-contained document rendered solely
  from the same projection with no added content. Exact file types are fixed by the implementation authorization; PDF
  rendering is NOT part of the first slice.
- the disclaimers (§10) are shown before the download control and are carried inside both renderings.
- no export history is persisted in the first slice; the page states that InventorAI keeps no record of the download and
  no copy of the file (§11, Owner decision 2 in §17).
- no inventor-approval write path; every item's approval state is `NOT_RECORDED` (§5).

## 4. Architecture and seam boundary

- A read-only projection on existing seams (§2 rules 1–2). No new owner of invention truth, no new store, table, sidecar or
  schema migration, no new persistence of any kind.
- No new public API surface (the P7-I2 public surfaces stay exactly two), no email delivery (Stage 33), no Stage 36
  integration, no provider port, no MCP or external-tool path.
- No change to progression, gaps, readiness, evidence, validation, NeedRouting, decisions, assumptions, contradictions,
  experiments or any owner's semantics. Reading for the disclosure export never mutates state.
- Composition is bounded by the size of the one project; no unbounded or super-linear joins.

## 5. Disclosure schema (conceptual; no frozen field names)

**Field map.** Every disclosure field of the Owner decision §2 has exactly one first-slice disposition:

| Owner decision §2 field | First-slice disposition |
|---|---|
| Invention title | NOT_CAPTURED (never generated; see §17 decision 4) |
| Problem addressed | RECORDED from the known problem |
| Background and existing limitations | NOT_CAPTURED (never generated; no prior-art search) |
| Invention objective | NOT_CAPTURED |
| Technical concept | RECORDED from the known mechanism |
| System, component, process and method descriptions | RECORDED for the Owner-stated parts of an integrated project (Stage 15); component descriptions beyond those parts NOT_CAPTURED |
| Relationships between components | RECORDED from Owner-declared interfaces and dependencies (Stage 15), where present |
| Operating sequence or workflow | NOT_CAPTURED |
| Alternative embodiments | NOT_CAPTURED |
| Materials, dimensions, parameters and operating conditions | NOT_CAPTURED |
| Novelty and differentiation statements | NOT_CAPTURED |
| Unresolved technical issues | RECORDED from unresolved gaps and active declared contradictions |
| Assumptions | RECORDED from CAP-08 |
| Missing information | RECORDED from unresolved gaps, inventor-marked unknowns and outstanding routed specialist needs |
| Supporting measurements, tests, diagrams, files and evidence | Evidence RECORDED with CAP-11 rows; diagrams and files NOT_CAPTURED |
| Prototype status and validation results | Experiments and execution states RECORDED as unvalidated inventor records; validation results NOT_CAPTURED |
| Risks, uncertainty and abstentions | RECORDED from risks and the owners' own limitation statements |
| Inventor-entered corrections and approvals | Corrections RECORDED as supersession history; approvals NOT_CAPTURED |
| Source and provenance references | Carried on every item (envelope below) |

The Requirement Landscape is carried as its own RECORDED section.

**Section states (closed).** `RECORDED` (the owner was read and holds items) · `NOTHING_RECORDED` (the owner was read and
holds none — rendered as "Nothing recorded in this project") · `NOT_CAPTURED` (InventorAI owns no such information) ·
`UNAVAILABLE` (a read or validation failure). `UNAVAILABLE` is never rendered as nothing recorded, "none", empty or zero, and
`NOT_CAPTURED` is never rendered as "none", empty or zero.

**Item envelope (every RECORDED item).** The verbatim value; its source owner (closed token); its provenance, validation
state and limitation exactly as the owner holds them (never upgraded, never reclassified — `LEGACY_UNSPECIFIED` stays as
it is); its currency (`CURRENT`, `SUPERSEDED` or `NO_LONGER_ACTIVE`); and its approval state, which is `NOT_RECORDED` in
the first slice because no inventor-approval owner exists.

## 6. Data allowed from existing owners (first slice)

Composed verbatim, each with its envelope:

- the known problem and the known mechanism;
- the Owner-stated parts, interfaces and dependencies of an integrated project, where already owned (Stage 15);
- CAP-08 Owner-declared assumptions, with superseded entries as history;
- CAP-10 Owner-declared contradictions — active pairs, and declarations no longer active marked as history;
- unresolved gaps in their canonical state (OPEN or PARTIAL), inventor-marked unknowns and outstanding routed specialist
  needs, as missing information;
- the Requirement Landscape;
- evidence items with their CAP-11 Form, Source and Validation rows, kept as three separate rows;
- CAP-09 experiments (the system-generated objective and the inventor's own planning fields) and their Stage 19 execution
  state (`NO RESULT`, `RECORDED N` or `UNAVAILABLE`), labelled as the inventor's own unvalidated records;
- risks, labelled as InventorAI's existing assessment output, not an engineering risk analysis;
- correction / supersession history, with the current value marked.

## 7. Data unavailable / not captured (first slice)

Rendered with the marker "Not captured by InventorAI", never generated or inferred: invention title; background and
existing limitations; invention objective; operating sequence or workflow (unless a later slice names an owner that already
captures it); component descriptions beyond the owned Stage-15 parts; alternative embodiments (CAP-05 / CAP-07 decision
alternatives are design-decision alternatives and are never relabelled as embodiments); materials, dimensions, parameters
and operating conditions (no typed-parameter owner exists; interface verification-preparation inputs are planning metadata
and are never relabelled); novelty and differentiation statements (Stage-17 commercial differentiation evidence is never
relabelled as technical novelty); diagrams, files and attachments; validation results; inventor approval state.

## 8. Data excluded entirely

Never present in either rendering: patent claims or claim-like text; novelty, inventive-step, patentability or
freedom-to-operate opinions; any prior-art statement; AI-written or generated legal or descriptive prose; the report's
proceed / revise verdict; maturity, readiness or Readiness Snapshot states where they could imply validation; Technical
Realization artifacts; calculated values (no calculation owner is implemented — the shared deterministic calculation and
units owner exists only as an accepted boundary contract of record); the CAP-12 Form Mock-up Advisory (session-only and
non-binding); CAP-01 guidance prose; inventor-stated safety-signal output presented as a safety determination; internal
identifiers, account data, e-mail addresses, credentials, tokens or storage paths; anything belonging to another project
or another account.

## 9. Export schema and versioning

- Two version identities travel with every export: the **disclosure schema version** (the field map, section states and
  envelope of §5) and the **export format version** (the serialization). Any change to a field, token or meaning yields a
  new version; a version is never silently reused.
- Machine-readable keys are language-neutral, closed and stable; unknown keys are never emitted. This contract freezes no
  final field names; the implementation contract freezes version 1.
- The disclosure export is not the Structured Export, not the public API representation and not the deliverable package.
- Determinism: identical canonical project state and identical versions yield byte-identical projection content. A
  generation timestamp, if carried, sits in a declared metadata field outside the content digest. No randomness, clock
  dependence or network dependence affects content.
- A content digest of the projection is carried for later integrity and traceability checks.
- Fail closed: a source-owner read failure marks that section `UNAVAILABLE`; a projection integrity failure (unknown token,
  schema violation, a record from another project, a supersession inconsistency) refuses the download with a bounded error
  and never emits a partial file.

## 10. Legal boundary and mandatory disclaimers

Mandatory English disclaimer wording (exact), carried verbatim in both renderings and shown before the download control:

1. "This document is not legal advice. InventorAI does not provide legal services."
2. "This document is not a patentability opinion. InventorAI has not assessed whether this invention is new, inventive or
   patentable."
3. "This document is not a prior-art search. InventorAI has not searched for or cleared prior art."
4. "This document is not a freedom-to-operate opinion."
5. "This document is not a filing-ready patent application."
6. "This document contains no patent claims, and nothing in it is a legally valid claim."
7. "Evidence recorded here is not a validated conclusion. Items marked unvalidated have not been checked by InventorAI."
8. "For legal advice, consult a qualified patent professional."

Conditional disclaimer (any later version that carries an inventor novelty or differentiation statement, verbatim):
"Novelty and differentiation statements here are the inventor's own words. InventorAI has not assessed them." In the first
slice such statements are `NOT_CAPTURED`, so this disclaimer does not render.

Exact scope label: "Invention disclosure export — this project only — not legal advice".

The Arabic wording of the disclaimers, scope label and markers is fixed, meaning-preserving, in the implementation contract
and verified by the UX / behaviour review (§13, §16). No jurisdiction, filing format, patent office or filing provider is
named or assumed. Whether a legal adviser reviews this wording before any user release is an Owner decision (§17); it is not
a prerequisite for this candidate.

## 11. Consent, privacy, security and retention

- **External transfer:** none. The first slice is an owner-private, project-scoped local download only. Any future
  transfer to a patent-drafting platform needs its own Owner authorization, explicit per-transfer user consent, export
  history and its own reviews (Owner decision §6, §7).
- **Access:** authenticated owner only, through the existing project-ownership check; a request for a missing project and a
  request for another account's project receive byte-identical denials (P10-D3a precedent); no other project or account is
  ever read into the projection.
- **Data minimization:** only the §6 data; none of the §8 identifiers or account data.
- **Consent for the download itself:** the owner's explicit request is the trigger; the disclaimers are shown first;
  viewing them records nothing.
- **Export history:** proposed DEFERRED AND DISCLOSED for the first slice — nothing is persisted, and the page states that
  InventorAI keeps no record of the download. Export history becomes required before any transfer capability (Owner
  decision 2 in §17).
- **Retention and deletion:** the projection is composed per request in memory; no server-side copy, cache or temporary file
  is kept; invention content is never written to logs; the response is marked not cacheable. Retention and deletion of the
  source data stay with their existing owners. The page states that InventorAI cannot delete copies the owner has
  downloaded.
- **Self-contained output:** the human-readable document loads no external resource (scripts, fonts, images, styles or
  trackers) and carries no executable content; the machine-readable file carries no executable content.

## 12. Evidence and attachment handling

Evidence is carried as the owners' recorded text with its CAP-11 rows and envelope. No attachment, file, image or diagram
is uploaded, processed, read, embedded, linked for fetching or interpreted; those fields are `NOT_CAPTURED`. Experiment
result text recorded by the inventor is not part of the first slice (only the execution state; Owner decision 5 in §17).

## 13. Bilingual and UX boundary

- Headings, section names, markers, disclaimers, scope label and journey labels are provided in English and Arabic,
  following the UI locale; Arabic renders right-to-left.
- Inventor-authored text is preserved verbatim — never translated, normalized or re-worded. Mixed-direction inventor text
  keeps its known rendering limitation, disclosed, not corrected here.
- Canonical technical statements (for example gap labels, Requirement Landscape rows and risk statements) stay in their
  source language under the current English-output rule (Stage 34 unchanged); first-use bilingual labelling follows the
  Owner language policy.
- English digits (0–9) are used for identifiers, versions, dates and counts (Owner decision §6).
- Machine-readable keys are language-neutral and versioned (§9).
- Labels state the scope (this project only) and the non-legal nature plainly; no label, filename or help text may suggest
  a patent application, a filing, legal review or validation.

## 14. Integration boundary

The export is designed so that a later, separately authorized handoff to a separate patent-drafting platform is possible
(versioned schema, provenance envelope, language-neutral keys). The first slice integrates with nothing: no API, platform,
vendor field mapping, email, provider, external tool or Stage 36 path, and no jurisdiction-specific format.

## 15. BASE RED requirements (contract requirements only; no tests are written by this document)

A future implementation must first show these failing, then passing:

1. **Prohibited wording:** neither rendering, in either locale, contains claim language or any assertion of patentability,
   novelty, inventive step, prior-art clearance, freedom to operate, filing readiness, legal validity or legal advice,
   except inside the exact §10 disclaimer strings (allow-listed).
2. **Disclaimers present:** all §10 disclaimers and the scope label appear verbatim in both renderings and both locales,
   before the download control.
3. **Markers:** every `NOT_CAPTURED` field renders the not-captured marker; an injected read failure renders
   `UNAVAILABLE`; neither ever renders as "none", empty, zero or omitted.
4. **No external transfer:** composition and download make no network call and import no provider, API client or e-mail
   module.
5. **Project separation:** another account's project and a missing project are denied byte-identically; a projection never
   contains a record from another project.
6. **Provenance visible:** every RECORDED item carries its source owner, provenance, validation state, currency and approval
   state, and the human rendering shows them.
7. **Excluded content absent:** with every §8 source populated, none of it appears — in particular no proceed / revise
   verdict and no readiness or maturity state.
8. **No mutation:** stored state is identical before and after composition and download; no export-history row exists.
9. **Existing surfaces unchanged:** the report, PDF, Structured Export and public API outputs are byte-identical for the
   same fixtures before and after the implementation.
10. **Determinism and versions:** identical state yields identical projection content and digest; both version identities
    are present.
11. **Verbatim inventor text:** inventor text, including Arabic and mixed-direction text, is byte-preserved.
12. **Fail closed:** an integrity failure refuses the download with no partial file.
13. **Self-contained output:** the human-readable document references no external resource.

## 16. Acceptance criteria for a future first slice

The first slice is acceptable only if: every §15 requirement passes; hosted mandatory CI and the Sharded FULL suite pass on
the exact final head; the UX / behaviour review (EN / AR, RTL, comprehension of the disclaimers and markers) passes; the
independent verification finds no derived truth, relabelling or surface change; and the Owner accepts it. Delivery of that
slice — not this contract — is the earliest point at which the Owner may decide to enter Stage 35.

## 17. Review path and Owner decisions

- **Before acceptance of this candidate:** an Astra architecture review (the projection composes many canonical owners and
  crosses privacy, versioning and export boundaries) and one adequate non-authoring Level-1 semantic review (legal-boundary
  wording, no implied novelty or validation, no relabelling).
- **Before implementation:** a UX / behaviour review of the journey, labels, markers and disclaimers in EN / AR (optional
  for this candidate's journey wording).
- **Legal adviser review:** an Owner decision, not a blocker to drafting or accepting this candidate.

Owner decisions still required:

1. Acceptance of this candidate as the workstream contract of record.
2. Export history: accept DEFERRED AND DISCLOSED for the first slice, or require it now.
3. The two first-slice renderings and their file types (PDF excluded from the first slice).
4. Whether a later slice adds an invention title or the inventor's own original description, only if an existing canonical
   owner already holds it verbatim; never generated.
5. Whether a later slice carries the inventor's recorded experiment result text.
6. Any inventor-approval write path (a later, separately reviewed decision).
7. Implementation authorization of the first slice, and with its delivery the decision whether to enter Stage 35.
8. Legal adviser review of the disclaimer wording before any user release.
9. Separately and not now: any external transfer, API surface, email delivery, provider or AI use, or attachment handling.

## 18. Non-authorization (restated)

This document authorizes no implementation, route, page, download, file generation, export, schema, store, persistence,
test, API, provider, AI, e-mail, attachment processing, patent drafting, claim generation, prior-art search, legal
analysis or legal advice; no change to the report, PDF, Structured Export, self-service project export or public API; no
Master Roadmap stage entry, checkbox, marker or count change; no CAP number; and no deployment or release.
