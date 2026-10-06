# SHARED DETERMINISTIC CALCULATION AND UNITS OWNER — BOUNDARY CONTRACT (ACCEPTED)

STATUS: ACCEPTED BOUNDARY CONTRACT OF RECORD — DOCUMENTATION ONLY — NO IMPLEMENTATION AUTHORIZED. Records the ownership
boundary of a FUTURE shared owner. It implements
nothing and authorizes no implementation: no runtime owner, adapter, method, unit vocabulary, conversion, schema, store,
persistence, route, test or user-facing behaviour is created by this document.
AUTHORITY LEVEL: subordinate governance boundary contract under the existing P9-QS future deterministic-calculation
adapter gate lineage — [`P9_QS_PHASE_9_TECHNICAL_QUALITY_STANDARD_CONTRACT.md`](P9_QS_PHASE_9_TECHNICAL_QUALITY_STANDARD_CONTRACT.md)
§12 (Units & Dimensional Integrity), §13 (future deterministic-calculation adapter gate) and §22 (gate sequence) — and bound
by the [Technical Realization Evidence and Artifact Model](TECHNICAL_REALIZATION_EVIDENCE_AND_ARTIFACT_MODEL.md). It amends
neither document, the THERM-01 Register section, the CAP-13 Register entry nor the
[Technical Realization Anchor Companion](TECHNICAL_REALIZATION_ANCHOR_COMPANION.md).
DESIGNATION: descriptive only — "the shared calculation and units owner". UNNUMBERED: no CAP number is assigned and `CAP-06`
is not reused (P9-QS §13); assigning any identifier is a separate Owner decision.
RECORDED: 2026-10-04, by Owner authorization of a documentation-only contract candidate.
ACCEPTANCE: 2026-10-04, by Owner decision accepting the merged candidate as the boundary contract of record, recorded
documentation-only; no boundary clause (§§2–15, §17) was changed by the acceptance. This acceptance does not enter Stage 25, does not activate CAP-13, does not authorize THERM-01, does not implement the shared owner, does not authorize any first increment, and does not assign a CAP number. A future first
increment still requires a separate Owner authorization, a named authorized consumer (§13), the source inspection and
unit-source qualification of §9, and an implementation contract or a bounded implementation authorization.
Implementation, a named consumer and any method admission stay unauthorized; no CAP number is assigned and `CAP-06` is
not reused.
*(Superseded 2026-10-04 by the Owner's acceptance, preserved — was: "STATUS: CONTRACT CANDIDATE — DOCUMENTATION ONLY.";
the title read "(CANDIDATE)" and the authority level read "subordinate governance contract candidate".)*
CORRECTION 01: `CORRECTION 01 — METHOD-FIRST FIRST-INCREMENT SHAPE — ACCEPTED 2026-10-07 — DOCUMENTATION ONLY — NO
IMPLEMENTATION AUTHORIZED`. Proposed 2026-10-06 as a candidate after an architecture review (PASS WITH CONDITIONS; Option
A — two mutually exclusive first-increment shapes, A1 conversion-first and A2 method-first), reviewed by one independent
non-authoring Level-1 semantic review (§16; PASS WITH NON-BLOCKING NOTES, no blocking finding) and ACCEPTED by the Owner
on 2026-10-07 under Option A. It changed only the §3 "First-increment method" paragraph and the §13 first-increment shape
and exclusion list; every other clause, including §9, §14 and §16, is unchanged. The accepted Correction 01 wording is now
the applicable contract wording of record; the text of record before the correction stays preserved beside each changed
passage as history only. Acceptance implements nothing, authorizes no first increment, admits no method or conversion,
and does not enter Stage 25 or activate CAP-13.
BASIS: the Lead's read-only Stage 25 / CAP-13 feasibility gate (finding B — CAP-13 is feasible only after calculation and
units ownership is decided); the Lead's read-only calculation and units ownership gate (finding B — a new shared calculation
and units owner is required before CAP-13); an Astra architecture review and an independent Claude architecture / semantic
review, each PASS WITH CONDITIONS, whose conditions are folded into §§2–16. Those gate findings and reviews are session-level
review inputs held in Git / GitHub and the Owner's records, not committed repository authority.

---

## 0. Preserved truth (binding; unchanged by this contract and its acceptance)

- `ACTIVE CONTRACT: NONE`. This contract is not a product increment and fills no active-contract slot.
- Stage 25 / CAP-13: `STAGE 25: NOT ENTERED` · `STAGE 25: NOT AUTHORIZED` · `CAP-13: NOT ACTIVATED`. CAP-13 stays blocked
  until this owner is implemented under a later, separate authorization, and even then needs its own contract.
- Stage 27 / THERM-01 stays NOT AUTHORIZED; its own thermal feasibility / contract gate (Register THERM-01 section) stays
  required.
- Technical Realization never calculates, selects, sizes, rates or dimensions (Anchor Companion §9.3, §9.8).
- Stage 36: external engineering tools stay deferred, and an external tool output is untrusted by default (Evidence and
  Artifact Model §11.4; Anchor Companion §9.11).
- Stage 14 stays blocked where the Master Roadmap records it as blocked.
- The Master Roadmap keeps 45 top-level stages with 23 / 45 incomplete; no checkbox, marker or count changes. This owner
  enters no Master Roadmap stage unless the Owner separately decides otherwise.
- This contract is not CAP-13, THERM-01, Technical Realization or Stage-36 implementation.

## 1. Purpose

CAP-13 numerical output and THERM-01 thermal analysis both depend on a deterministic calculation and units capability that
P9-QS §12 / §13 keep deferred, and the THERM-01 Register section records that no second calculation framework is created.
This contract fixes the boundary of that capability once, before any consumer exists, so that no consumer builds its own and
no shared owner grows into a technical super-owner.

## 2. Owner placement and dependency direction

1. **Placement.** An independent, narrow, shared owner under the existing P9-QS §13 deterministic-calculation adapter
   lineage, carrying the P9-QS §12 quantity semantics for the requests it executes. It is NOT CAP-13, NOT THERM-01, NOT
   Technical Realization, NOT Stage 36, NOT a Domain Pack, NOT a second domain registry, NOT an evidence owner and NOT an
   artifact store.
2. **Designation.** Descriptive and unnumbered (see header). No CAP number; `CAP-06` is never reused.
3. **Dependency direction.** Consumers depend on the owner; the owner depends on nothing a consumer owns. The owner reads
   only (a) the request it is handed and (b) its own governed artifact (§9). It imports no consumer module and reads no
   project, session, ledger, store, requirement quantity, answer or part answer.
4. **Execution locality.** Local, in-process deterministic execution does not wait for Stage 36. Any provider or
   external-tool execution remains Stage 36 and is outside this owner.

## 3. Execution envelope versus method authority

**The owner owns the execution envelope only:** request validation; physical quantity identity; admitted units; dimensional
checks; admitted conversions; numeric integrity checks; result packaging; producing identity (method version, unit-record
version, governed-artifact version, implementation version, request digest and result identity); and failure isolation.

**Method authority stays outside the owner.** Every method is a registered deterministic adapter supplied by, and attributed
to, a technical authority — a governed Domain Pack or an Owner-authorized capability contract. That authority owns the
method's equations, constants, physical assumptions, applicability, error bounds and method qualification. The owner records
the method identity it was given and never defines, edits, derives or extends a method. Admission of a method into the
owner's governed artifact is structural only: it checks that the authority's record is complete, closed and source-bound
(§9); it does not judge technical correctness. Each method admission requires its own Owner authorization tied to a named
consumer (§13).

**First-increment method (Correction 01 — accepted 2026-10-07).** A separately authorized first increment
selects exactly ONE of the two mutually exclusive shapes of §13: (A1) one unit conversion whose authority is the unit source
itself; or (A2) one deterministic method whose technical authority stays outside this owner. This contract itself admits
neither shape and supplies no method, conversion factor, constant or unit vocabulary; each enters only through the owner's
governed artifact with its own inspection record (§9), and only under a separate Owner authorization tied to a named
consumer (§13).
*(Text of record before Correction 01, preserved as history; superseded by the accepted Correction 01 — "**First-increment
method.** In a future first increment the only admitted method may be a unit conversion whose authority is the unit source
itself. This contract documents no conversion factor, no constant and no unit vocabulary; each enters only through the
owner's governed artifact with its own inspection record (§9).")*

## 4. Explicit non-goals — the owner never

- holds technical-method authority, or authority over equations, constants, physical assumptions or applicability;
- writes advice wording, selects a safety factor, or selects a material or component;
- reaches a suitability, safety or compliance conclusion;
- promotes evidence, or makes a readiness decision;
- owns inventor data;
- reads project state, the ledger, requirement quantities, answers or part answers;
- parses the value text held by the quantity owner, or extracts anything from free text;
- infers a unit from context, or supplies a default or assumed value;
- judges plausibility or order of magnitude;
- propagates uncertainty or tolerance;
- gives rounding, precision or significant-figure guidance;
- localizes unit display;
- converts currency;
- produces or accepts an AI estimate;
- executes an external tool;
- writes canonical state;
- persists anything or owns a store;
- performs general simulation;
- activates CAP-13, THERM-01 or Technical Realization, automatically or otherwise.

## 5. Data-model semantics (conceptual; no schema)

The names below are conceptual. The implementing contract fixes exact field names. No schema, table, column, store or
persistence is created by this section.

- **Value or range** — a scalar, or explicit lower and upper bounds. A future first increment admits scalars only; a range
  is refused.
- **Unit** — an admitted unit token from the owner's governed artifact; never a free-text symbol.
- **Physical quantity kind** — what is quantified, from a closed vocabulary in the governed artifact.
- **Dimension** — the dimensional identity of that kind.
- **Subject / component / scenario binding** — an opaque reference supplied by the consumer and echoed unchanged; the owner
  never resolves it against project state.
- **Provenance** — owner-local tokens `OWNER_STATED` · `SOURCE_STATED` · `CALCULATED`.
- **Source or assumption reference** — for a source-stated input, its source-record identity; for an owner-stated input, the
  consumer's record reference; assumptions as structured references supplied by the method authority.
- **Method identity and version**; **unit-record version**; **governed-artifact version**; **implementation version**.
- **Applicability conditions** — declared by the method authority; the owner checks only that a request falls inside
  declared, machine-checkable conditions.
- **Input completeness** — per required input: provided, missing or not admitted.
- **Limitations** — the method authority's declared limitations plus the fixed statements of §7.
- **Execution result** — the owner-local result state (§7) and, for every non-success state, exactly one closed reason
  token (§8).

## 6. Required distinctions

- Physical quantity kind is not dimension: different kinds may share a dimension and are never interchanged on that basis.
- Physical quantity kind is not T2-A requirement intent: the closed `quantity_kind` vocabulary of
  `engine/requirement_quantity.py` states what a requirement says about a value (target, minimum, maximum, range, count,
  other). It carries no unit or dimension and is never reinterpreted as a physical quantity kind.
- Range bounds, tolerance, uncertainty and advisory intervals are distinct. The owner handles explicit range bounds only
  where a method admits them, and never creates, widens or propagates a tolerance, an uncertainty or an advisory interval.
- Calculated provenance retains input lineage: every `CALCULATED` output names its inputs, their provenance and their source
  or assumption references.
- "Retained input provenance" means echoed in the result. It is never stored by this owner.
- `SUCCESS` does not mean suitable, safe, compliant, validated, verified, recommended or based on correct inputs. It means
  only that an admitted operation ran on the inputs as given and the checks of §10 passed.
- Result states are owner-local and are mapped onto the Evidence and Artifact Model (§11). They are not a new shared
  artifact-state vocabulary.

## 7. Result states (owner-local)

- **`SUCCESS`** — the admitted operation completed and its structural and numerical checks passed. It carries a bounded
  numerical result with full input lineage. It maps to calculated relative to the inputs as given, claim status
  `UNVALIDATED` and `validity_status = pending`; it never sets `verification_outcome = pass`. Every `SUCCESS` result carries
  the fixed statements: calculated from the inputs as given; inputs not checked for correctness; not a design or
  specification value; not validated or verified.
- **`UNABLE_TO_DETERMINE`** — a required basis, capability or applicability is absent. No numerical payload.
- **`FAILURE`** — an execution or integrity fault occurred after admission. No numerical payload.
- **`REFUSAL`** (rejected request) — a malformed or non-admitted request is refused before execution. No execution occurred
  and there is no numerical payload.

## 8. Closed reason tokens

Following the CAP-12 precedent (`engine/cap12_form_mockup.py` keeps a closed reason-token set and refuses unknown keys), the
owner uses a closed set of reason tokens. Every non-success result carries exactly one token, never free text and never a
numerical payload. An unknown token is refused. The spellings below are provisional; the implementing contract fixes them.

| Reason (required) | Provisional token | Result state |
|---|---|---|
| Operation not admitted | `OPERATION_NOT_ADMITTED` | `REFUSAL` |
| Unit not admitted | `UNIT_NOT_ADMITTED` | `REFUSAL` |
| Unknown unit | `UNKNOWN_UNIT` | `REFUSAL` |
| Incompatible dimension | `INCOMPATIBLE_DIMENSION` | `REFUSAL` |
| Semantic-kind mismatch | `SEMANTIC_KIND_MISMATCH` | `REFUSAL` |
| Missing provenance | `MISSING_PROVENANCE` | `REFUSAL` |
| Method not registered | `METHOD_NOT_REGISTERED` | `REFUSAL` |
| Version mismatch | `VERSION_MISMATCH` | `REFUSAL` |
| Invalid numeric input | `INVALID_NUMERIC_INPUT` | `REFUSAL` |
| Input missing | `INPUT_MISSING` | `UNABLE_TO_DETERMINE` |
| Input outside admitted range | `INPUT_OUTSIDE_ADMITTED_RANGE` | `UNABLE_TO_DETERMINE` |
| Applicability refused by method authority | `APPLICABILITY_REFUSED_BY_METHOD_AUTHORITY` | `UNABLE_TO_DETERMINE` |
| Source unavailable | `SOURCE_UNAVAILABLE` | `UNABLE_TO_DETERMINE` |
| Execution integrity failure | `EXECUTION_INTEGRITY_FAILURE` | `FAILURE` |

A non-finite result, a result outside the admitted range, a result-unit inconsistency, an overflow, or a tampered method,
source or version record detected after admission is reported as `EXECUTION_INTEGRITY_FAILURE`.

## 9. Governed artifact, unit-source governance and version identity

- **One governed artifact** owned by this owner, validated CAP-12-style: closed records, exact keys, unknown keys refused,
  fail-closed loading. It is NOT a Domain Pack and NOT an entry in the pack-scoped `domains/domain_provenance.json`.
- **Every unit record and every method record** carries source identity, exact edition or date, URL, source-use basis,
  inspection basis and inspection date; a method record also carries its technical-authority attribution.
- **NIST SP 811 precedent.** The repository already records NIST SP 811 for bounded unit identification —
  `electronics_electrical:PR005`, `mechanical:PR009` and `control_loop:PR005` — with recorded source-use dispositions
  `electronics_electrical:PR007`, `mechanical:PR011` and `control_loop:PR006`: NIST employee-authored Technical Series works
  are not subject to U.S. copyright protection, NIST acknowledgement is required, and third-party material is excluded. Those
  records bind unit identification only and expressly reproduce no conversion factor or table. They are precedent and
  source-use context only: this owner's artifact needs its own inspection record for every admitted unit and conversion
  before implementation.
- **Unknown rights mean no method and no unit.**
- **Protected standards** may be referenced but never copied; where compatible, only a factual paraphrase is recorded.
- **Manufacturer data** needs its own provenance and licensing record; none is admitted by a first increment.
- **AI is never an authority.** No unit knowledge enters from model memory.
- **Chained conversions** record every source in the chain.
- **Version identity.** Any change to a unit record, method record or the artifact yields a new version; every result
  carries the versions it was produced under.

## 10. Numerical policy

A future implementation must define and enforce:

- numeric input type only — no strings and no parsing;
- booleans refused, never treated as integers;
- NaN and infinities refused;
- explicit overflow handling, reported as `FAILURE`;
- a finite result;
- a result inside the admitted range;
- a result unit consistent with the declared quantity identity;
- an explicit rounding policy — preferably none in the first increment, and never rounding, precision or significant-figure
  guidance;
- determinism: the same request under the same versions yields the same result, with no clock or randomness.

## 11. Evidence boundary and Evidence and Artifact Model mapping

- Calculation execution is separate from evidence admission.
- The adapter is an evidence producer, not an evidence promoter (P9-QS §13).
- A successful calculation does not promote readiness, validation or verification.
- A result may become evidence only when an existing evidence owner records it through an authorized acceptance path.
- The shared owner writes nothing.
- Technical Realization `artifact_origin_status = calculated` must not be granted from owner-stated or unvalidated inputs
  unless the Evidence and Artifact Model conditions — including §6, a reproducible calculation from verified inputs — are
  explicitly satisfied by the retaining owner.
- In a first increment the result validation state stays `UNVALIDATED` only.

| Owner-local state | Mapping onto the Evidence and Artifact Model |
|---|---|
| `SUCCESS` | calculated relative to the inputs as given; claim status `UNVALIDATED`; `validity_status = pending` if a retaining owner records it; no `verification_stage` recorded and `verification_outcome = pass` never set by this owner |
| `UNABLE_TO_DETERMINE` | no numerical payload; a consumer may show the existing display meanings of §11.2 (unable to determine, missing input, calculation required), never a new status value |
| `FAILURE` | no numerical payload and nothing to retain |
| `REFUSAL` | no execution, no numerical payload and nothing to retain |

## 12. Persistence rule

- Persistence is forbidden for this owner.
- Persistence may be reconsidered only when the first authorized consumer must cite a result as evidence, or must detect
  staleness under the Evidence and Artifact Model §9 / §11.4 cascade.
- Even then, retention belongs to an existing evidence owner, or to a future artifact store under its own authorization.
- The shared owner never gains a store.

## 13. Minimum viable future first increment (only if separately authorized)

*(Correction 01 wording — accepted 2026-10-07; the earlier text of record is preserved below as history only.)*

A first increment must have exactly one named, authorized consumer and must not be built as a consumer-less library.
Possible triggers: the first authorized method consumer, a CAP-13 feasibility-gate increment, or a THERM-01 contract. It
selects exactly ONE of the following two mutually exclusive shapes and never combines them.

**A1 — conversion-first.** Bounded to:

- one physical quantity kind;
- a very small governed unit vocabulary;
- one independently checked, source-qualified unit conversion.

**A2 — method-first.** Bounded to:

- exactly one separately admitted deterministic method, whose technical authority (§3: equations, constants, physical
  assumptions, applicability, error bounds and qualification) stays outside this owner;
- only the physical quantity kinds and the exact unit tokens that this one method requires, closed over the method's
  declared roles — each role bound to one quantity kind and one exact unit token;
- validation of exact role → quantity kind → unit token consistency only: a dimensionally equivalent expression is not an
  admitted alias of a token, and the method's dimensional derivation stays method-authority content;
- every method record and unit record governed under §9;
- no conversion operation.

**Both shapes retain:**

- explicit scalar numeric input, with ranges refused;
- mandatory unit-record, method and implementation versions;
- input provenance echoed in the result;
- a request digest and result identity, for later staleness detection by a retaining owner;
- the `SUCCESS` / `UNABLE_TO_DETERMINE` / `FAILURE` / `REFUSAL` states;
- no user-facing thickness, specification or thermal recommendation.

It must exclude: unsupported ranges; string parsing; boolean-as-integer behaviour; offset conversions such as temperature
scales; logarithmic units such as decibels; symbol aliases; case folding; Unicode normalization; live retrieval; network
access; clock dependence; randomness; provider calls; external tools; AI fallback; stale-value fallback; zero substitutes;
partial recommendations; a second method; a second consumer; any conversion not independently justified by the named
consumer; a generic solver; and a generic unit registry or conversion graph.

*(Text of record before Correction 01, preserved as history; superseded by the accepted Correction 01 — "A first increment must have
a named, authorized consumer and must not be built as a consumer-less library. Possible triggers: the first authorized method
consumer, a CAP-13 feasibility-gate increment, or a THERM-01 contract. It is bounded to: one physical quantity kind; a very
small governed unit vocabulary; explicit scalar numeric input, with ranges refused; one independently checked,
source-qualified unit conversion; mandatory unit-record, method and implementation versions; input provenance echoed in the
result; a request digest and result identity, for later staleness detection by a retaining owner; the `SUCCESS` /
`UNABLE_TO_DETERMINE` / `FAILURE` / `REFUSAL` states; no user-facing thickness, specification or thermal recommendation. It
must exclude: unsupported ranges; string parsing; boolean-as-integer behaviour; offset conversions such as temperature
scales; logarithmic units such as decibels; symbol aliases; case folding; Unicode normalization; live retrieval; network
access; clock dependence; randomness; provider calls; external tools; AI fallback; stale-value fallback; zero substitutes;
and partial recommendations.")*

## 14. Required guard strategy for a future implementation

- independent expected numerical results;
- a source test vector, plus an inverse round-trip within a stated tolerance where applicable;
- unknown-unit rejection;
- invalid-value rejection;
- incompatible-meaning rejection;
- out-of-scope method rejection;
- provenance preservation;
- subject-binding preservation;
- failure on a tampered method, source or version record;
- no mutation on success or on failure;
- no network or model fallback;
- no validation or readiness promotion;
- no numerical payload on refusal.

## 15. Reused patterns (reference only; nothing here changes them)

- `engine/export_adapter.py` (P7-I3) — pure deterministic transform, bounded explicit error, untrusted-by-default output and
  no state mutation; the adapter architecture P9-QS §13 names.
- `engine/cap12_form_mockup.py` — governed artifact, closed keys, unknown keys refused, closed reason tokens, fail-closed
  loading.
- `engine/commercial_evidence.py` — no basis, no number; amounts compared but never used for arithmetic. The owner reads none
  of its data.
- `engine/requirement_quantity.py` — the inventor's value text is kept verbatim and never parsed. The owner never parses it;
  a consumer that needs a numeric input obtains it through its own authorized capture path.

## 16. Reviewer path and Owner decisions

- The Astra review and the independent Claude architecture / semantic review were sufficient to draft the candidate. The
  Owner accepted it on 2026-10-04 as the boundary contract of record without changing any boundary clause.
- If the contract changes materially before implementation, one adequate non-authoring Level-1 semantic review is required.
- Any implementation needs risk-appropriate independent verification.
- A UX / behaviour review is required only when a consuming capability first shows calculated values to users.
- Owner decisions still required: any identifier for the owner; and, separately, any first increment, its named consumer
  and each method admission. Acceptance of the candidate is recorded in the header (ACCEPTANCE).

## 17. Non-authorization (restated)

This document authorizes no implementation, runtime owner, adapter, method, unit vocabulary, conversion factor, constant,
equation, schema, store, persistence, test, route or user-facing behaviour; no CAP-13, THERM-01, Technical Realization or
Stage-36 work; no Master Roadmap stage entry, checkbox, marker or count change; no CAP number; and no deployment or release.
