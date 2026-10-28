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
CORRECTION 02: `CORRECTION 02 — BOUNDED SECOND ADMISSION (THERM-01) — ACCEPTED — DOCUMENTATION ONLY — NO IMPLEMENTATION
AUTHORIZED — NO METHOD ADMISSION`. It records the already-reviewed bounded expansion of the delivered CAP-13 first admission
(the A2 shape of §13, delivered as Stage 25 — CAP-13 Two-Support Static Reactions — Slice 1) to exactly two methods and two
consumers, as fixed by the architecture decision record (AD-1 to AD-11) of the accepted
[THERM-01 method contract](STAGE27_THERM01_CONDUCTION_TEMPERATURE_DIFFERENCE_METHOD_CONTRACT.md) (PR #775, merge
`1b587da5c3555dda487be02589fa618f7a5a7cb8`; source qualification closed by PR #777, merge
`a72d25fe011582b4a0176722a1b1810daca6e683`). Review basis: the architecture reviews reconciled into that decision record
(Lead-reported; session-level review inputs held in Git / GitHub and the Owner's records, as for Correction 01). Accepted by
Owner authorization of this documentation-only record. It ADDS §13A and a short addition each to §3, §16 and §17; Correction 01
and every other clause — including §§7–10, §13 and §14 — are unchanged, and §13 stays the delivered first-increment shape
of record. Correction 02 authorizes the contract boundary only: it implements nothing, admits no method, changes no
runtime, artifact or test, enters no Stage and activates nothing. The shared-owner second admission stays NOT IMPLEMENTED
and NOT AUTHORIZED for implementation until a separate Owner implementation authorization.
CORRECTION 02 IMPLEMENTED (2026-10-09): the separately Owner-authorized, delivered Stage 27 — THERM-01 Single-Path Temperature-Difference — Slice 1 implements §13A exactly — `engine/deterministic_calculation.py` implementation version 1.1.0 admits exactly the two methods `cap13:static_reactions_two_support` 1.0 and `therm01:conduction_temperature_difference_single_path` 1.0, the kinds force / length / power / thermal_resistance / temperature_difference and the tokens N / mm / W / K/W / K (one unit per kind, no alias, no conversion); the owner artifact is content version 2; application wiring creates one immutable method-local binding per method; there is no registry, discovery or request-selected method; CAP-13 semantics, artifact and behaviour are unchanged. The sentences above that the second admission stays NOT IMPLEMENTED are preserved as the text of record at acceptance. §0 preserved truth describes the one-method state at this contract's acceptance and is history for the method count.
CORRECTION 03: `CORRECTION 03 — BOUNDED THIRD ADMISSION (CAP-13 PLANAR SINGLE-FORCE MOMENT) — OWNER-AUTHORIZED WITH ITS
IMPLEMENTATION`. Folded, narrowly, into the one Owner-authorized bounded increment `CAP-13 PLANAR SINGLE-FORCE MOMENT —
SLICE 1`, which implements it in the same pull request under the
[planar single-force moment method contract](STAGE25_CAP13_PLANAR_SINGLE_FORCE_MOMENT_METHOD_CONTRACT.md). Applicability:
it takes effect only on the verified merge of that pull request into `feature/atomic-json-session-persistence`; on its
proposal branch it is an Owner-authorized proposed amendment. It ADDS §13B and one bullet to §16; §13A, §13 and every other
clause — including §§7–10, §12 and §14 — are unchanged. It admits exactly one further method and nothing more (§13B).
CORRECTION 04: `CORRECTION 04 — BOUNDED FOURTH ADMISSION (CAP-13 LINEAR SPEED-DEPENDENT ROTATIONAL LOAD) — OWNER-AUTHORIZED
WITH ITS IMPLEMENTATION`. Folded, narrowly, into the one Owner-authorized increment `ROTATIONAL-LOAD-SLICE-01`, which
implements it in the same pull request under the
[linear speed-dependent rotational load method contract](STAGE25_CAP13_LINEAR_SPEED_DEPENDENT_ROTATIONAL_LOAD_METHOD_CONTRACT.md).
Applicability: it takes effect only on the verified merge of that pull request into `feature/atomic-json-session-persistence`;
on its proposal branch it is an Owner-authorized proposed amendment. It ADDS §13C and one bullet to §16; §13B, §13A, §13 and
every other clause — including §§7–10, §12 and §14 — are unchanged. It admits exactly one further method and nothing more.
CORRECTION 05: `CORRECTION 05 — BOUNDED FIFTH ADMISSION (SENSORS C3 TMP36 NOMINAL VOLTAGE-TO-TEMPERATURE) — OWNER-AUTHORIZED
WITH ITS IMPLEMENTATION`. Folded, narrowly, into the one Owner-authorized increment `TMP36-NOMINAL-VOLTAGE-TEMPERATURE-01`,
which implements it in the same pull request under the
[TMP36 nominal voltage-to-temperature method contract](SENSORS_C3_TMP36_NOMINAL_VOLTAGE_TO_TEMPERATURE_METHOD_CONTRACT.md).
Applicability: it takes effect only on the verified merge of that pull request into `feature/atomic-json-session-persistence`;
on its proposal branch it is an Owner-authorized proposed amendment. It ADDS §13D and one bullet to §16 and narrowly amends,
for this one method only, the §13A statements that no absolute `temperature` kind and no °C token are admitted; §13C, §13B,
§13A for THERM-01, §13 and every other clause — including §§7–10, §12 and §14 — are unchanged. It admits exactly one
further method and nothing more.
CORRECTION 06: `CORRECTION 06 — BOUNDED SIXTH ADMISSION (ELECTRICAL / ELECTRONICS DC RESISTIVE LOAD CURRENT) —
OWNER-AUTHORIZED WITH ITS IMPLEMENTATION`. Folded, narrowly, into the one Owner-authorized increment
`DC-RESISTIVE-LOAD-CURRENT-01`, which implements it in the same pull request under the
[DC resistive load current method contract](ELECTRICAL_DC_RESISTIVE_LOAD_CURRENT_METHOD_CONTRACT.md). Applicability: it
takes effect only on the verified merge of that pull request into `feature/atomic-json-session-persistence`; on its proposal
branch it is an Owner-authorized proposed amendment. It ADDS §13E and one bullet to §16 and narrowly amends, for the
`voltage` kind only, the "one unit per kind" rule of §13D (`mV` and `V` become two distinct exact tokens of that kind, with
no mapping between them); §13D for the TMP36 method, §13C, §13B, §13A, §13 and every other clause — including §§7–10, §12
and §14 — are unchanged. It admits exactly one further method and nothing more.
CORRECTION 07: `CORRECTION 07 — BOUNDED SEVENTH ADMISSION (ELECTRICAL / ELECTRONICS DC RESISTIVE LOAD POWER) —
OWNER-AUTHORIZED WITH ITS IMPLEMENTATION`. Folded, narrowly, into the one Owner-authorized increment
`DC-RESISTIVE-LOAD-POWER-01`, which implements it in the same pull request under the
[DC resistive load power method contract](ELECTRICAL_DC_RESISTIVE_LOAD_POWER_METHOD_CONTRACT.md). Applicability: it takes
effect only on the verified merge of that pull request into `feature/atomic-json-session-persistence`; on its proposal
branch it is an Owner-authorized proposed amendment. It ADDS §13F and one bullet to §16. It admits exactly one further
method on the EXISTING quantity kinds and exact unit tokens and nothing more; §13E and every earlier section and clause —
including §§7–10, §12 and §14 — are unchanged.
CORRECTION 08: `CORRECTION 08 — BOUNDED EIGHTH ADMISSION (ELECTRICAL / ELECTRONICS DC RESISTIVE LOAD ENERGY) —
OWNER-AUTHORIZED WITH ITS IMPLEMENTATION`. Folded, narrowly, into the one Owner-authorized increment
`DC-RESISTIVE-LOAD-ENERGY-01`, which implements it in the same pull request under the
[DC resistive load energy method contract](ELECTRICAL_DC_RESISTIVE_LOAD_ENERGY_METHOD_CONTRACT.md). Applicability: it
takes effect only on the verified merge of that pull request into `feature/atomic-json-session-persistence`; on its
proposal branch it is an Owner-authorized proposed amendment. It ADDS §13G and one bullet to §16. It admits exactly one
further method and exactly two further quantity kinds with one exact unit token each (`energy` / `J`, `time` / `s`) and
nothing more; §13F and every earlier section and clause — including §§7–10, §12 and §14 — are unchanged.
CORRECTION 09: `CORRECTION 09 — BOUNDED NINTH ADMISSION (CAP-13 PLANAR REQUIRED FORCE) — OWNER-AUTHORIZED WITH ITS
IMPLEMENTATION`. Folded, narrowly, into the one Owner-authorized increment `CAP13-PLANAR-REQUIRED-FORCE-01`, which implements
it in the same pull request under the [planar required force method contract](STAGE25_CAP13_PLANAR_REQUIRED_FORCE_METHOD_CONTRACT.md).
Applicability: it takes effect only on the verified merge of that pull request into `feature/atomic-json-session-persistence`;
on its proposal branch it is an Owner-authorized proposed amendment. It ADDS §13H and one bullet to §16. It admits exactly one
further method on the EXISTING quantity kinds and exact unit tokens (`moment` / `N·mm`, `length` / `mm`, `force` / `N`) and
nothing more; §13G and every earlier section and clause — including §§7–10, §12 and §14 — are unchanged.
BASIS: the Lead's read-only Stage 25 / CAP-13 feasibility gate (finding B — CAP-13 is feasible only after calculation and
units ownership is decided); the Lead's read-only calculation and units ownership gate (finding B — a new shared calculation
and units owner is required before CAP-13); an Astra architecture review and an independent Claude architecture / semantic
review, each PASS WITH CONDITIONS, whose conditions are folded into §§2–16. Those gate findings and reviews are session-level
review inputs held in Git / GitHub and the Owner's records, not committed repository authority.
CORRECTION 10: `CORRECTION 10 — BOUNDED TENTH ADMISSION (ELECTRICAL / ELECTRONICS DC CONSTANT-CURRENT CHARGE) —
OWNER-AUTHORIZED WITH ITS IMPLEMENTATION`. Folded, narrowly, into the one Owner-authorized increment
`DC-CONSTANT-CURRENT-CHARGE-01`, which implements it in the same pull request under the
[DC constant-current charge method contract](ELECTRICAL_DC_CONSTANT_CURRENT_CHARGE_METHOD_CONTRACT.md). Applicability: it
takes effect only on the verified merge of that pull request into `feature/atomic-json-session-persistence`; on its
proposal branch it is an Owner-authorized proposed amendment. It ADDS §13I and one bullet to §16. It admits exactly one
further method, exactly one further quantity kind with one exact unit token (`electric_charge` / `A·h`) and exactly one
further exact token of the EXISTING `time` kind (`h`, beside `s`, as the second named exception to one-token-per-kind) and
nothing more — no conversion between `h` and `s`, between `A·h` and `C` or `mA·h`, and no relation of `A·h` to `J`; §13H
and every earlier section and clause — including §§7–10, §12 and §14 — are unchanged.
CORRECTION 11: `CORRECTION 11 — BOUNDED ELEVENTH ADMISSION (ELECTRICAL / ELECTRONICS PWM AVERAGE VOLTAGE) —
OWNER-AUTHORIZED WITH ITS IMPLEMENTATION`. Folded, narrowly, into the one Owner-authorized increment
`PWM-AVERAGE-VOLTAGE-01`, which implements it in the same pull request under the
[PWM average-voltage method contract](ELECTRICAL_PWM_AVERAGE_VOLTAGE_METHOD_CONTRACT.md). Applicability: it takes effect
only on the verified merge of that pull request into `feature/atomic-json-session-persistence`; on its proposal branch it
is an Owner-authorized proposed amendment. It ADDS §13J and one bullet to §16. It admits exactly one further method on the
EXISTING quantity kinds and exact unit tokens (`voltage` / `V`, `time` / `s`) and nothing more — no new kind, token,
dimensionless or duty-cycle quantity, percentage, alias or conversion; §13I and every earlier section and clause —
including §§7–10, §12 and §14 — are unchanged. General Power Electronics / Motion (28-T3) stays BLOCKED; this admission is
one claim-level average-waveform relation only.

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
**Bounded second admission (Correction 02 — accepted).** Beyond the delivered first increment, the only further admission
this contract permits is the one bounded second admission of §13A; each method in it still needs its own separate Owner
authorization before it is admitted at runtime.
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

## 13A. Bounded second admission — THERM-01 (Correction 02 — accepted; documentation only)

The delivered first increment (§13, shape A2) may be expanded, under a separate Owner implementation authorization, to
EXACTLY the following and nothing more. This section authorizes the contract boundary only; it implements nothing and
admits no method.

- **Owner.** The one existing shared owner (`engine/deterministic_calculation.py`). No second owner, solver, framework or
  calculation path is created.
- **Methods — exactly two:** `cap13:static_reactions_two_support` version `1.0` and
  `therm01:conduction_temperature_difference_single_path` version `1.0`. Each keeps its technical authority outside this
  owner (§3): CAP-13 in its own method-authority artifact, THERM-01 in its own separate method-authority artifact.
- **Consumers — exactly two:** the existing CAP-13 consumer and one THERM-01 consumer. Neither consumer imports the other,
  and neither method-authority artifact loads the other at execution.
- **Quantity kinds:** the existing `force` and `length`, plus exactly `power`, `thermal_resistance` and
  `temperature_difference`. No absolute `temperature` kind is admitted.
- **Exact unit tokens:** the existing `N` and `mm`, plus exactly `W`, `K/W` and `K`. No alias, no case folding, no
  dimensional equivalence, no °C token and no conversion of any kind (§13's exclusion of offset conversions such as
  temperature scales stands).
- **Closed inventory.** The admitted methods, kinds and tokens stay closed, exact sets validated on load; anything outside
  them is refused as today.
- **Method-local bindings.** Each method's roles are bound to its own kinds and exact tokens; one method's tokens never
  satisfy another method's roles, and the dimensional derivation stays method-authority content.
- **Bindings.** One additional immutable, application-wired method binding for the THERM-01 consumer, beside the existing
  CAP-13 binding; each consumer holds exactly its own binding. No registry, discovery mechanism, dynamic module path,
  generic conversion, generic unit vocabulary or request-selected method is authorized under this admission; any later
  architecture stays subject to a separate decision.
- **Versions.** One shared-owner governed artifact (§9), whose content version moves to future `2`; owner implementation
  version future `1.1.0`. Every unit and method record in it keeps the §9 source and inspection requirements; the existing
  SP 811 unit records `N` / `mm` and their source-use record stay as they are.
- **CAP-13 preserved.** The CAP-13 method `1.0`, its authority artifact version `1`, its equations, roles, units, semantic
  pins and user-facing behaviour stay unchanged; no CAP-13 method-semantic change is authorized. Bounded updates to
  assertions on the shared-owner artifact content version, the implementation version and the owner's closed-inventory /
  digest identities, caused only by this second admission, are expected and allowed.
- **States and failure semantics unchanged.** §7 states, §8 reason tokens and their mapping, §10 numerical policy and §12
  persistence rule apply unchanged; an overflow or non-finite result stays `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no
  numerical payload, and an owner `FAILURE` is never rewritten as `REFUSAL`.
- **Still excluded:** a third method or consumer; ranges; string parsing; any conversion; a generic solver; a generic unit
  registry or conversion graph; persistence; provider, AI or external-tool execution; and every other §13 exclusion.

## 13B. Bounded third admission — CAP-13 planar single-force moment (Correction 03)

The delivered second admission (§13A) is expanded, by the Owner-authorized increment named in the CORRECTION 03 header,
to EXACTLY the following and nothing more.

- **Owner.** The one existing shared owner. No second owner, solver, framework, numerical policy engine or calculation
  path is created.
- **Methods — exactly three:** `cap13:static_reactions_two_support` 1.0, `therm01:conduction_temperature_difference_single_path`
  1.0 and `cap13:planar_single_force_moment` 1.0. The third keeps its technical authority outside this owner (§3), in its own
  CAP-13 method-authority artifact `cap13_planar_single_force_moment` version 1, separate from the two-support artifact.
- **Consumers — exactly three:** the existing two and one planar-moment consumer. No consumer imports another, and no
  method-authority artifact loads another at execution.
- **Quantity kinds:** the existing five, plus exactly `moment`. **Exact unit tokens:** the existing five, plus exactly
  `N·mm`. One unit per kind; no alias, no case folding, no dimensional equivalence (a moment is never a "force × length"
  pair the owner composes) and no conversion of any kind (`N·mm` is never converted to `N·m`).
- **Method-local bindings and wiring.** One additional immutable, application-wired binding for the planar-moment consumer;
  each consumer holds exactly its own binding. No registry, discovery, dynamic module path, generic unit vocabulary or
  request-selected method.
- **Versions.** The shared-owner artifact moves to content version `3` and the implementation to `1.2.0`. The new unit
  record (`dcu:U006`, NIST SP 811) and source-use records (`dcu:SU005` NASA STI, `dcu:SU006` NIST) keep the §9 source and
  inspection requirements; every content-version-2 record is unchanged.
- **Numerical policy.** §10 applies unchanged. The method-specific acceptance of the planar moment — a result accepted only
  when finite, strictly positive and within a relative error of `2^-52` of the exact product of its two binary inputs,
  subnormal results accepted when they meet that bound — is method-authority content held in its adapter and contract
  (§6 there); it is NOT a generic owner numerical policy and changes nothing for the other two methods. A result that fails
  it is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload.
- **Existing methods preserved.** The two-support and THERM-01 methods, their authority artifacts, semantics, pins and
  user-facing behaviour stay unchanged. Bounded updates to assertions on the owner artifact content version, the
  implementation version and the closed inventory, caused only by this admission, are expected and allowed.
- **Still excluded:** a fourth method or consumer; ranges; string parsing in the owner; any conversion; a generic solver,
  unit registry or conversion graph; persistence (§12); provider, AI or external-tool execution; and every other §13 / §13A
  exclusion.

## 13C. Bounded fourth admission — CAP-13 linear speed-dependent rotational load (Correction 04)

The delivered third admission (§13B) is expanded, by the Owner-authorized increment named in the CORRECTION 04 header, to
EXACTLY the following and nothing more.

- **Owner.** The one existing shared owner. No second owner, solver, simulation, model selection, range policy or
  calculation path is created, and the owner acquires no persistence and no scientific authority.
- **Methods — exactly four:** the three of §13B plus `cap13:linear_speed_dependent_rotational_load` 1.0, whose technical
  authority stays outside this owner (§3), in its own CAP-13 method-authority artifact
  `cap13_linear_speed_dependent_rotational_load` version 1.
- **Consumers — exactly four:** the existing three and one rotational-load consumer. No consumer imports another, and no
  method-authority artifact loads another at execution.
- **Quantity kinds:** the existing six, plus exactly `torque` and `angular_velocity`. **Exact unit tokens:** the existing
  six, plus exactly `N·m` and `rad/s`. One unit per kind; no alias, no case folding, no dimensional equivalence (`torque`
  and `moment` stay distinct kinds and `N·m` is never derived from or converted to `N·mm`) and no conversion of any kind.
- **Condition vocabulary.** The closed applicability / result-range vocabulary the owner checks mechanically gains exactly
  `less_than_zero`, used for the new method's negative nominal torque. The owner only evaluates a condition a method record
  declares; it chooses none.
- **Method-local binding and wiring.** One additional immutable, application-wired binding; each consumer holds exactly its
  own binding. No registry, discovery, dynamic module path or request-selected method.
- **Versions.** The shared-owner artifact moves to content version `4` and the implementation to `1.3.0`. The new unit
  records (`dcu:U007` `N·m`, `dcu:U008` `rad/s`, from `Modelica.Units.SI` v4.1.0) and source-use record (`dcu:SU007`, the
  Modelica Standard Library BSD 3-Clause License) keep the §9 source and inspection requirements; every content-version-3
  record is unchanged.
- **Numerical policy.** §10 applies unchanged. The new method's acceptance (exact rational value rounded once; exact zero at
  zero speed; a nonzero result within `2^-52` of the exact result, subnormal results only when they meet that bound) is
  method-authority content held in its adapter and contract; it is NOT a generic owner policy and changes nothing for the
  other three methods. A failure is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload.
- **Existing methods preserved.** The two-support, THERM-01 and planar-moment methods, their authority artifacts,
  semantics, pins and user-facing behaviour stay unchanged; bounded updates to assertions on the owner content version, the
  implementation version and the closed inventory, caused only by this admission, are expected and allowed.
- **Still excluded:** a fifth method or consumer; ranges; string parsing in the owner; any conversion; a generic solver,
  unit registry or conversion graph; persistence (§12); provider, AI, external-tool or external-library execution
  (including Modelica runtimes); and every other §13 / §13A / §13B exclusion.

## 13D. Bounded fifth admission — Sensors C3 TMP36 nominal voltage-to-temperature (Correction 05)

The delivered fourth admission (§13C) is expanded, by the Owner-authorized increment named in the CORRECTION 05 header, to
EXACTLY the following and nothing more.

- **Owner.** The one existing shared owner. No second owner, solver, conversion graph, unit registry, range policy or
  calculation path is created, and the owner acquires no persistence and no scientific authority.
- **Methods — exactly five:** the four of §13C plus `tmp36:nominal_voltage_to_temperature` 1.0, whose technical authority
  stays outside this owner (§3), in its own Sensors / Instrumentation C3 method-authority artifact
  `tmp36_nominal_voltage_to_temperature` version 1.
- **Consumers — exactly five:** the existing four and one TMP36 consumer. No consumer imports another, and no
  method-authority artifact loads another at execution.
- **Quantity kinds:** the existing eight, plus exactly `voltage` and `celsius_temperature`. **Exact unit tokens:** the
  existing eight, plus exactly `mV` and `°C`. One unit per kind; no alias (`mV` is never `millivolt`, `mv` or `V`; `°C` is
  never `C`, `degC` or `℃`), no case folding, no dimensional equivalence and no conversion of any kind.
- **Celsius temperature (narrow amendment of §13A for this one method).** `celsius_temperature` / `°C` is admitted ONLY as
  the output of the TMP36 method: a temperature on the Celsius scale given by that method's own nominal relation. The owner
  never converts it to or from `K`, never relates it to THERM-01's `temperature_difference` and performs no offset
  arithmetic; the affine relation `T = (V_OUT − 500) / 10` is method-authority content held in the adapter. §13's exclusion
  of owner offset conversions between temperature scales stands, and THERM-01 keeps its own "no absolute temperature, no °C"
  boundary unchanged.
- **Condition vocabulary.** Unchanged. The new method declares only the existing `greater_than_zero` on `v_out`; its
  nominal-model interval (100 mV to 1750 mV inclusive) is method-authority content, checked by its consumer from the exact
  decimal input before any binary rounding and defended again in its adapter, never an owner range policy.
- **Method-local binding and wiring.** One additional immutable, application-wired binding; each consumer holds exactly its
  own binding. No registry, discovery, dynamic module path or request-selected method.
- **Versions.** The shared-owner artifact moves to content version `5` and the implementation to `1.4.0`. The new unit
  records (`dcu:U009` `mV`, from NIST SP 811 Appendix B.9 and Chapter 4 Table 5; `dcu:U010` `°C`, from `Modelica.Units`
  v4.1.0) and source-use records (`dcu:SU008` NIST, `dcu:SU009` the Modelica Standard Library BSD 3-Clause License,
  `dcu:SU010` the Analog Devices data-sheet notice) keep the §9 source and inspection requirements; every content-version-4
  record is unchanged.
- **Numerical policy.** §10 applies unchanged: the owner still receives typed binary64 numbers and parses no string. The new
  method's decimal bridge (strict decimal grammar, exact-decimal interval check, one correctly rounded conversion), its
  binary acceptance (exact rational value rounded once; exact zero at 500 mV; a nonzero result within `2^-52` of the exact
  result and inside −40 to 125) and its decimal-reference acceptance (within `2^-45` °C of the exact decimal relation, then
  shown as that exact decimal) are method-authority content held in its consumer, adapter and contract; they are NOT a
  generic owner policy and change nothing for the other four methods. A failure is `FAILURE / EXECUTION_INTEGRITY_FAILURE`
  with no numerical payload.
- **Existing methods preserved.** The two-support, THERM-01, planar-moment and rotational-load methods, their authority
  artifacts, semantics, pins and user-facing behaviour stay unchanged; bounded updates to assertions on the owner content
  version, the implementation version and the closed inventory, caused only by this admission, are expected and allowed.
- **Still excluded:** a sixth method or consumer; owner ranges; string parsing in the owner; any conversion, including
  between temperature scales; a generic solver, unit registry or conversion graph; persistence (§12); provider, AI,
  external-tool or external-library execution; and every other §13 / §13A / §13B / §13C exclusion.

## 13E. Bounded sixth admission — Electrical / Electronics DC resistive load current (Correction 06)

The delivered fifth admission (§13D) is expanded, by the Owner-authorized increment named in the CORRECTION 06 header, to
EXACTLY the following and nothing more.

- **Owner.** The one existing shared owner. No second owner, solver, conversion graph, unit registry, range policy or
  calculation path is created, and the owner acquires no persistence and no scientific authority.
- **Methods — exactly six:** the five of §13D plus `electrical:dc_resistive_load_current` 1.0, whose technical authority
  stays outside this owner (§3), in its own Electrical / Electronics method-authority artifact
  `electrical_dc_resistive_load_current` version 1.
- **Consumers — exactly six:** the existing five and one DC load consumer. No consumer imports another, and no
  method-authority artifact loads another at execution.
- **Quantity kinds:** the existing ten, plus exactly `electric_resistance` and `electric_current`. **Exact unit tokens:**
  the existing ten, plus exactly `V`, `Ω` (U+03A9) and `A`. No alias (`Ω` is never `ohm`, `Ohm` or the separate ohm sign U+2126; `A` is never
  `amp`; `V` is never `volt` or `v`), no case folding, no dimensional equivalence and no conversion of any kind.
- **Two exact voltage tokens (narrow amendment of §13D's one-unit-per-kind rule, for `voltage` only).** The `voltage` kind
  holds exactly the token set {`mV`, `V`}, named once in the owner (`KIND_TOKEN_EXCEPTIONS`); every other kind keeps one
  token, and any other second token still fails closed. Each role still binds exactly ONE token (TMP36 `v_out` → `mV`; DC
  load `v_load` → `V`); a request in the other token is `REFUSAL / UNIT_NOT_ADMITTED`. Nothing relates `mV` to `V`: there is
  no scale factor, no prefix arithmetic and no conversion, in the owner or anywhere else.
- **Condition vocabulary.** Unchanged. The new method declares only the existing `greater_than_zero` on `r_load`; its sign
  convention, input representation limits and positive-resistance refusal are method-authority content, checked by its
  consumer from the exact decimal input before any binary rounding, never an owner range policy. No result range is
  declared: the current is signed.
- **Method-local binding and wiring.** One additional immutable, application-wired binding; each consumer holds exactly its
  own binding. No registry, discovery, dynamic module path or request-selected method.
- **Versions.** The shared-owner artifact moves to content version `6` and the implementation to `1.5.0`. The new unit
  records (`dcu:U011` `V`, `dcu:U012` `Ω`, `dcu:U013` `A`, from NIST SP 811 Appendix B.9 as recorded in
  `electronics_electrical:PR005`) and source-use records (`dcu:SU011` NIST; `dcu:SU012` the DOE Web Policies snapshot of the
  method's own `dcload:SU001`, itself the `electronics_electrical:PR006` disposition applied to this method) keep the §9
  source and inspection requirements; every content-version-5 record is unchanged.
- **Numerical policy.** §10 applies unchanged: the owner still receives typed binary64 numbers and parses no string. The new
  method's decimal bridge (strict signed decimal grammar with representation limits, exact-decimal positive-resistance
  check, one correctly rounded conversion per input), its binary acceptance (exact rational quotient rounded once; exact zero
  for a zero voltage; a nonzero result finite, of the exact sign and within `2^-52` of the exact result), its
  decimal-reference acceptance (within a relative `2^-51` of the exact decimal quotient) and its display (the exact quotient
  rounded once to 12 significant digits, half to even, labelled exact or rounded) are method-authority content held in its
  consumer, adapter and contract; they are NOT a generic owner policy and change nothing for the other five methods. A
  failure is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload.
- **Existing methods preserved.** The two-support, THERM-01, planar-moment, rotational-load and TMP36 methods, their
  authority artifacts, semantics, pins and user-facing behaviour stay unchanged; bounded updates to assertions on the owner
  content version, the implementation version, the closed inventory and the binding count, caused only by this admission,
  are expected and allowed.
- **Still excluded:** a seventh method or consumer; owner ranges; string parsing in the owner; any conversion, including
  `mV` ↔ `V`; a generic solver, circuit solver, unit registry or conversion graph; persistence (§12); provider, AI,
  external-tool or external-library execution; and every other §13 / §13A / §13B / §13C / §13D exclusion.

## 13F. Bounded seventh admission — Electrical / Electronics DC resistive load power (Correction 07)

The delivered sixth admission (§13E) is expanded, by the Owner-authorized increment named in the CORRECTION 07 header,
to EXACTLY the following and nothing more.

- **Owner.** The one existing shared owner. No second owner, solver, conversion graph, unit registry, range policy or
  calculation path is created, and the owner acquires no persistence and no scientific authority.
- **Methods — exactly seven:** the six of §13E plus `electrical:dc_resistive_load_power` 1.0, whose technical authority
  stays outside this owner (§3), in its own Electrical / Electronics method-authority artifact
  `electrical_dc_resistive_load_power` version 1.
- **Consumers — exactly seven:** the existing six and one DC load power consumer. No consumer imports another (the power
  consumer keeps its own display rule rather than importing the DC load current consumer), and no method-authority
  artifact loads another at execution.
- **Quantity kinds and exact unit tokens: unchanged.** The method uses the existing `voltage` / `V`,
  `electric_resistance` / `Ω` and `power` / `W`. No kind, token, alias, case folding, dimensional equivalence or
  conversion is added; `V` stays bound to `v_load` and `mV` is refused for it (`UNIT_NOT_ADMITTED`); `mW` and `kW` are
  unknown tokens. The existing `W` unit record (`dcu:U003`) is reused unchanged; its THERM-01-scoped source-use snapshot
  (`dcu:SU003`) is not extended — the method's own artifact carries its source-use basis for the watt (NIST SP 811
  Appendix B.9, as recorded in `electronics_electrical:PR005` / `PR007`).
- **Condition vocabulary.** Unchanged. The new method declares only the existing `greater_than_zero` on `r_load`; its
  input representation limits and positive-resistance refusal are method-authority content, checked by its consumer from
  the exact decimal input before any binary rounding. No result range is declared; non-negativity of the result is
  defended by the method adapter and the consumer, never an owner range policy.
- **Method-local binding and wiring.** One additional immutable, application-wired binding; each consumer holds exactly
  its own binding. No registry, discovery, dynamic module path or request-selected method.
- **Versions.** The shared-owner artifact moves to content version `7` and the implementation to `1.6.0`. One new
  source-use record (`dcu:SU013`, the DOE Web Policies snapshot of the method's own `dcpower:SU001`, itself the
  `electronics_electrical:PR006` disposition applied to this method) keeps the §9 source and inspection requirements;
  every content-version-6 record is unchanged.
- **Numerical policy.** §10 applies unchanged: the owner still receives typed binary64 numbers and parses no string. The
  new method's decimal bridge (the §13E strict signed decimal grammar and representation limits, exact-decimal
  positive-resistance check, one correctly rounded conversion per input), its binary acceptance (exact rational
  `v_load² / r_load` rounded once; exact zero for a zero voltage, never a negative zero; a nonzero result finite,
  positive and within `2^-52` of the exact result), its decimal-reference acceptance (within a relative `2^-50` of the
  exact decimal value) and its display (the exact value rounded once to 12 significant digits, half to even, labelled
  exact or rounded) are method-authority content held in its consumer, adapter and contract; they are NOT a generic owner
  policy and change nothing for the other six methods. A failure is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no
  numerical payload.
- **Existing methods preserved.** The two-support, THERM-01, planar-moment, rotational-load, TMP36 and DC load current
  methods, their authority artifacts, semantics, pins and user-facing behaviour stay unchanged; bounded updates to
  assertions on the owner content version, the implementation version, the closed inventory and the binding count,
  caused only by this admission, are expected and allowed.
- **Still excluded:** an eighth method or consumer; owner ranges; string parsing in the owner; any conversion; any
  temperature, thermal, rating, energy or protection result; a generic solver, circuit solver, unit registry or
  conversion graph; persistence (§12); provider, AI, external-tool or external-library execution; and every other §13 /
  §13A–§13E exclusion.

## 13G. Bounded eighth admission — Electrical / Electronics DC resistive load energy (Correction 08)

The delivered seventh admission (§13F) is expanded, by the Owner-authorized increment named in the CORRECTION 08 header,
to EXACTLY the following and nothing more.

- **Owner.** The one existing shared owner. No second owner, solver, conversion graph, unit registry, range policy,
  integration or time-stepping path is created, and the owner acquires no persistence and no scientific authority.
- **Methods — exactly eight:** the seven of §13F plus `electrical:dc_resistive_load_energy` 1.0, whose technical
  authority stays outside this owner (§3), in its own Electrical / Electronics method-authority artifact
  `electrical_dc_resistive_load_energy` version 1.
- **Consumers — exactly eight:** the existing seven and one DC load energy consumer. No consumer imports another (the
  energy consumer keeps its own display rule rather than importing the DC load power or current consumer), and no
  method-authority artifact loads another at execution.
- **Quantity kinds and exact unit tokens: exactly two added.** `energy` (dimension M L² T⁻²) with the one exact token
  `J`, and `time` (dimension T) with the one exact token `s`, each with its own unit record (`dcu:U014` J, `dcu:U015` s:
  NIST SP 811 Chapter 4, Tables 3 and 1, the Lead-level textual source check recorded as `electronics_electrical:PR009`)
  and one new source-use record (`dcu:SU014`, the NIST snapshot of the method's own `dcenergy:SU002`, itself the
  `electronics_electrical:PR011` disposition applied to this method). The pack record `electronics_electrical:PR009`
  keeps its own scope (reference text of its reference group, which admits no owner unit) and is unchanged; the owner
  admits `J` and `s` only through its own records. The method also uses the existing `voltage` / `V` and
  `electric_resistance` / `Ω`. No other kind, token, alias, case folding, dimensional equivalence or conversion is
  added: `J` is not related to `W` or to `N·m`, `s` to no other time unit, and `Wh`, `kWh`, `kJ`, `mAh`, `min` and `h`
  are unknown tokens. The `voltage` kind keeps the one named token exception of §13E; `energy` and `time` hold one token
  each.
- **Condition vocabulary.** Unchanged. The new method declares only the existing `greater_than_zero` on `r_load`; its
  input representation limits, positive-resistance refusal and not-negative-duration refusal are method-authority
  content, checked by its consumer from the exact decimal input before any binary rounding (the adapter refuses a
  negative duration again as an integrity failure). No result range is declared; non-negativity of the result is
  defended by the method adapter and the consumer, never an owner range policy.
- **Method-local binding and wiring.** One additional immutable, application-wired binding; each consumer holds exactly
  its own binding. No registry, discovery, dynamic module path or request-selected method.
- **Versions.** The shared-owner artifact moves to content version `8` and the implementation to `1.7.0`. Two new
  source-use records (`dcu:SU014` above, and `dcu:SU015`, the DOE Web Policies snapshot of the method's own
  `dcenergy:SU001`, itself the `electronics_electrical:PR006` and `PR010` dispositions applied to this method) keep the
  §9 source and inspection requirements; every content-version-7 record is unchanged.
- **Numerical policy.** §10 applies unchanged: the owner still receives typed binary64 numbers and parses no string. The
  new method's decimal bridge (the §13E strict signed decimal grammar and representation limits for `V` and `R`, a
  duration grammar of up to nine integer and nine fractional digits, exact-decimal checks of `R > 0` and then `t ≥ 0`,
  one correctly rounded conversion per input), its binary acceptance (exact rational `v_load² × t_duration / r_load`
  rounded once; exact zero for a zero voltage or duration, never a negative zero; a nonzero result finite, positive and
  within `2^-52` of the exact result), its decimal-reference acceptance (within a relative `2^-50` of the exact decimal
  value) and its display (the exact value rounded once to 12 significant digits, half to even, labelled exact or
  rounded) are method-authority content held in its consumer, adapter and contract; they are NOT a generic owner policy
  and change nothing for the other seven methods. A failure is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical
  payload.
- **Existing methods preserved.** The two-support, THERM-01, planar-moment, rotational-load, TMP36, DC load current and
  DC load power methods, their authority artifacts, semantics, pins and user-facing behaviour stay unchanged; bounded
  updates to assertions on the owner content version, the implementation version, the closed inventory and the binding
  count, caused only by this admission, are expected and allowed.
- **Still excluded:** a ninth method or consumer; owner ranges; string parsing in the owner; any conversion (no Wh, kWh,
  mAh, minute or hour); any battery capacity, charge, state-of-charge, runtime or sizing result; any temperature,
  thermal, rating or protection result; varying-power, average-power or integrated energy; a generic solver, circuit
  solver, unit registry or conversion graph; persistence (§12); provider, AI, external-tool or external-library
  execution; and every other §13 / §13A–§13F exclusion.

## 13H. Bounded ninth admission — CAP-13 planar required force (Correction 09)

The delivered eighth admission (§13G) is expanded, by the Owner-authorized increment named in the CORRECTION 09 header, to
EXACTLY the following and nothing more.

- **Owner.** The one existing shared owner. No second owner, solver, conversion graph, unit registry, range policy or
  inverse-calculation path is created, and the owner acquires no persistence and no scientific authority.
- **Methods — exactly nine:** the eight of §13G plus `cap13:planar_required_force` 1.0, whose technical authority stays
  outside this owner (§3), in its own CAP-13 method-authority artifact `cap13_planar_required_force` version 1. It is a
  separate method, not a mode of `cap13:planar_single_force_moment`, which is unchanged.
- **Consumers — exactly nine:** the existing eight and one planar required force consumer. No consumer imports another (it
  keeps its own display rule rather than importing a DC load consumer, and restates the planar-moment evidence in its own
  records rather than loading that artifact), and no method-authority artifact loads another at execution. No result is
  transferred between methods.
- **Quantity kinds and exact unit tokens: none added.** The method uses the existing `moment` / `N·mm` (input),
  `length` / `mm` (input) and `force` / `N` (output) and their unit records `dcu:U006`, `dcu:U002` and `dcu:U001`,
  unchanged. No alias, case folding, dimensional equivalence or conversion is added: nothing relates `N·mm` to `N·m`.
- **Condition vocabulary.** Unchanged. The new method declares only the existing `greater_than_zero` on `d_perp`; its input
  representation limits and positive-distance refusal are method-authority content, checked by its consumer from the exact
  decimal input before any binary rounding (the adapter refuses a non-positive distance or a negative target moment again
  as an integrity failure). No condition is declared on `M_target` and no result range is declared: a zero target moment
  and a zero force are admitted.
- **Method-local binding and wiring.** One additional immutable, application-wired binding; each consumer holds exactly its
  own binding. No registry, discovery, dynamic module path or request-selected method.
- **Versions.** The shared-owner artifact moves to content version `9` and the implementation to `1.8.0`. One new
  source-use record (`dcu:SU016`, the NASA STI snapshot of the method's own `cap13f:SU001`) keeps the §9 source and
  inspection requirements; no new source is introduced and every content-version-8 record is unchanged.
- **Numerical policy.** §10 applies unchanged: the owner still receives typed binary64 numbers and parses no string. The
  new method's decimal bridge (a strict unsigned grammar of up to twelve integer digits for `M_target`, nine for `d_perp`
  and nine fractional digits, an exact-decimal check of `d_perp > 0`, one correctly rounded conversion per input), its
  binary acceptance (exact rational `M_target / d_perp` rounded once; exact zero for a zero target moment, distinct from a
  nonzero underflow, which is a failure; a nonzero result finite, strictly positive and within `2^-52` of the exact
  result), its decimal-reference acceptance (within a relative `2^-51` of the exact decimal quotient) and its display (the
  exact quotient rounded once to 12 significant digits, half to even, labelled exact or rounded) are method-authority
  content held in its consumer, adapter and contract; they are NOT a generic owner policy and change nothing for the other
  eight methods. A failure is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload.
- **Existing methods preserved.** The two-support, THERM-01, planar-moment, rotational-load, TMP36, DC load current, DC load
  power and DC load energy methods, their authority artifacts, semantics, pins and user-facing behaviour stay unchanged;
  bounded updates to assertions on the owner content version, the implementation version, the closed inventory and the
  binding count, caused only by this admission, are expected and allowed.
- **Still excluded:** a tenth method or consumer; owner ranges; string parsing in the owner; any conversion; any target
  moment estimate, friction, efficiency, starting, holding or safety allowance or margin; any actuator, motor, spring or
  human-effort capability, selection or sizing and any motion requirement; any result transfer between calculations; a
  generic solver, inverse solver, unit registry or conversion graph; persistence (§12); provider, AI, external-tool or
  external-library execution; and every other §13 / §13A–§13G exclusion.

## 13I. Bounded tenth admission — Electrical / Electronics DC constant-current charge (Correction 10)

The delivered ninth admission (§13H) is expanded, by the Owner-authorized increment named in the CORRECTION 10 header, to
EXACTLY the following and nothing more.

- **Owner.** The one existing shared owner. No second owner, solver, conversion graph, unit registry, range policy,
  integration or time-stepping path is created, and the owner acquires no persistence and no scientific authority.
- **Methods — exactly ten:** the nine of §13H plus `electrical:dc_constant_current_charge` 1.0, whose technical authority
  stays outside this owner (§3), in its own Electrical / Electronics method-authority artifact
  `electrical_dc_constant_current_charge` version 1.
- **Consumers — exactly ten:** the existing nine and one DC constant-current charge consumer. No consumer imports another
  (the charge consumer keeps its own display rule rather than importing a DC load consumer), and no method-authority
  artifact loads another at execution. No result is transferred between methods.
- **Quantity kinds and exact unit tokens: one kind and two tokens added.** `electric_charge` (dimension T I) with the one
  exact token `A·h` (unit record `dcu:U017`), and the EXISTING `time` kind (dimension T) gains the second exact token `h`
  (unit record `dcu:U016`) beside `s`, both records resting on NIST SP 811 Appendix B.9 (ampere hour row,
  `1 A · h = 3.6 × 10³ C`) read with Chapter 4, Table 3 (coulomb, `s · A`), the Lead-level primary-source inspection
  recorded as `electronics_electrical:PR020`, and one new source-use record (`dcu:SU017`, the NIST snapshot of the
  method's own `dcq:SU002`, itself the `electronics_electrical:PR021` disposition applied to this method). The pack record
  `electronics_electrical:PR020` keeps its own scope (reference text of its reference group, which admits no owner unit)
  and is unchanged; the owner admits `h` and `A·h` only through its own records. The method also uses the existing
  `electric_current` / `A` (`dcu:U013`). **Second named token exception (narrow amendment of the one-token-per-kind rule,
  for `time` only).** The `time` kind holds exactly the token set {`s`, `h`}, named once in the owner beside the `voltage`
  exception of §13E (`KIND_TOKEN_EXCEPTIONS`); every other kind keeps one token. Each role binds exactly ONE of the two: the
  DC resistive load energy duration stays `s` and the DC constant-current charge duration is `h`; a request in the other
  token is refused `UNIT_NOT_ADMITTED`; nothing maps `h` to `s` (the factor 3600 is never applied), and `h` is no alias,
  no scale relation and no conversion. No other kind, token, alias, case folding, dimensional equivalence or conversion is
  added: `A·h` is not related to `C`, `mA·h`, `Ah`, `J` or `W·h` (the Appendix B.9 factor is recorded for unit
  identification only and never applied), and `h` to no minute, day or second; `C`, `mA·h`, `mAh`, `Ah`, `min`, `W·h`
  and `Wh` are unknown tokens. A separate NIST statement that the hour is accepted for use with the SI is not recorded as
  an inspected location and is not relied upon; identification of `h` rests on the inspected ampere hour row alone.
- **Condition vocabulary.** Unchanged. The new method declares NO owner condition (the vocabulary has no not-negative
  condition and none is added); its input representation limits, not-negative-current refusal and not-negative-duration
  refusal are method-authority content, checked by its consumer from the exact decimal input before any binary rounding
  (the adapter refuses a negative current or duration again as an integrity failure). No result range is declared; a zero
  current or a zero duration gives exactly zero, and non-negativity of the result is defended by the method adapter and the
  consumer, never an owner range policy.
- **Method-local binding and wiring.** One additional immutable, application-wired binding; each consumer holds exactly
  its own binding. No registry, discovery, dynamic module path or request-selected method.
- **Versions.** The shared-owner artifact moves to content version `10` and the implementation to `1.9.0`. Two new
  source-use records (`dcu:SU017` above, and `dcu:SU018`, the DOE Web Policies snapshot of the method's own `dcq:SU001`,
  itself the `electronics_electrical:PR019` disposition applied to this method) keep the §9 source and inspection
  requirements; every content-version-9 record is unchanged.
- **Numerical policy.** §10 applies unchanged: the owner still receives typed binary64 numbers and parses no string. The
  new method's decimal bridge (a strict signed decimal grammar of up to nine integer and nine fractional digits for `I` and
  `t`, exact-decimal checks of `I ≥ 0` and then `t ≥ 0`, one correctly rounded conversion per input), its binary
  acceptance (exact rational `i_load × t_duration` rounded once; exact zero for a zero current or duration, never a
  negative zero; a nonzero result finite, positive and within `2^-52` of the exact result), its decimal-reference
  acceptance (within a relative `2^-51` of the exact decimal product) and its display (the exact value rounded once to 12
  significant digits, half to even, labelled exact or rounded) are method-authority content held in its consumer, adapter
  and contract; they are NOT a generic owner policy and change nothing for the other nine methods. A failure is
  `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload.
- **Existing methods preserved.** The two-support, THERM-01, planar-moment, rotational-load, TMP36, DC load current, DC
  load power, DC load energy and planar required force methods, their authority artifacts, semantics, pins and
  user-facing behaviour stay unchanged (the energy method's `s` duration is unchanged); bounded updates to assertions on
  the owner content version, the implementation version, the closed inventory, the named exception set and the binding
  count, caused only by this admission, are expected and allowed.
- **Still excluded:** an eleventh method or consumer; owner ranges; string parsing in the owner; any conversion (no
  `A·h` ↔ `C`, no `mA·h`, no `h` ↔ `s`, no minute, no `W·h`); any battery capacity, battery need, runtime, state of
  charge, charging, chemistry, BMS, sizing, selection, suitability or rating-comparison result; varying-current,
  average-current, duty-cycle or integrated charge; any energy result from this method; a generic solver, circuit solver,
  unit registry or conversion graph; persistence (§12); provider, AI, external-tool or external-library execution; and
  every other §13 / §13A–§13H exclusion.

## 13J. Bounded eleventh admission — Electrical / Electronics PWM average voltage (Correction 11)

The delivered tenth admission (§13I) is expanded, by the Owner-authorized increment named in the CORRECTION 11 header, to
EXACTLY the following and nothing more.

- **Owner.** The one existing shared owner. No second owner, solver, conversion graph, unit registry, range policy,
  waveform model, filter or time-stepping path is created, no 28-T3 owner is created, and the owner acquires no persistence
  and no scientific authority.
- **Methods — exactly eleven:** the ten of §13I plus `electrical:pwm_average_voltage` 1.0, whose technical authority stays
  outside this owner (§3), in its own Electrical / Electronics method-authority artifact `electrical_pwm_average_voltage`
  version 1. It is the arithmetic time-average over one period of an ideal two-level voltage waveform (the declared supply
  level during the on-interval, zero otherwise): `v_avg = v_supply × t_on / t_period`. It is not a DC load method, not a
  converter and not a drive; the DC resistive load current, power and energy methods are unchanged and no result is
  transferred between them and this method.
- **Consumers — exactly eleven:** the existing ten and one PWM average-voltage consumer. No consumer imports another (it
  keeps its own display rule rather than importing a DC load consumer), and no method-authority artifact loads another at
  execution.
- **Quantity kinds and exact unit tokens: none added.** The method uses the existing `voltage` / `V` (input `v_supply` and
  output `v_avg`; record `dcu:U011`) and the existing `time` / `s` (inputs `t_on` and `t_period`; record `dcu:U015`),
  unchanged. No dimensionless or duty-cycle kind, no percentage token, no alias, case folding, dimensional equivalence or
  conversion is added: the ratio `t_on / t_period` exists only inside the method's product, `ms`, `µs`, `Hz`, `kHz`, `mV`,
  `kV` and `%` are unknown tokens, and the `time` kind keeps exactly the two tokens of §13I (this method binds `s` only).
- **Condition vocabulary.** Unchanged. The new method declares only the existing `greater_than_zero` on `t_period` and the
  existing `within_zero_and_role` on `t_on` bound to `t_period` (inclusive at both ends, so `t_on = 0` and
  `t_on = t_period` are admitted); its input representation limits, not-negative-supply refusal and the ordered exact-decimal
  screening (supply level, period, on-time, on-time against period) are method-authority content, checked by its consumer
  from the exact decimal input before any binary rounding (the adapter refuses a negative supply level, a non-positive
  period, a negative on-time or an on-time above the period again as an integrity failure). No result range is declared;
  the bound `v_avg ≤ v_supply` is defended by the adapter and the consumer, never an owner range policy.
- **Nonnegative-voltage convention.** `v_supply ≥ 0` only: the admitted waveform switches between zero and the declared
  supply level. No signed or bipolar waveform, no polarity inference, no reference-direction model and no reuse of the DC
  load methods' passive sign convention; a signed or bipolar waveform would need its own separate bounded qualification.
- **Method-local binding and wiring.** One additional immutable, application-wired binding; each consumer holds exactly
  its own binding. No registry, discovery, dynamic module path or request-selected method.
- **Versions.** The shared-owner artifact moves to content version `11` and the implementation to `1.10.0`. One new
  source-use record (`dcu:SU019`, the NASA STI snapshot of the method's own `pwm:SU001`, resting on the TECH-SOURCES-001
  research-stream inspections SRC-042 and SRC-018, Lead-supplied for this method) keeps the §9 source and inspection
  requirements; every content-version-10 record is unchanged. The CAP-13 NASA STI snapshots `dcu:SU002`, `dcu:SU005` and
  `dcu:SU016` are not extended to this method.
- **Numerical policy.** §10 applies unchanged: the owner still receives typed binary64 numbers and parses no string. The
  new method's decimal bridge (a strict signed decimal grammar of up to nine integer and nine fractional digits for all
  three inputs, exact-decimal checks of `v_supply ≥ 0`, then `t_period > 0`, then `t_on ≥ 0`, then `t_on ≤ t_period`, one
  correctly rounded conversion per input), its binary acceptance (exact rational `v_supply × t_on / t_period` rounded once;
  exact zero for a zero supply level or on-time, never a negative zero; exactly `v_supply` for an on-time equal to the
  period; a nonzero result finite, positive and within `2^-52` of the exact result), its decimal-reference acceptance
  (within a relative `2^-50` of the exact decimal value and not above the binary64 supply level) and its display (the exact
  value rounded once to 12 significant digits, half to even, labelled exact or rounded) are method-authority content held in
  its consumer, adapter and contract; they are NOT a generic owner policy and change nothing for the other ten methods. A
  failure is `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload.
- **Existing methods preserved.** The two-support, THERM-01, planar-moment, rotational-load, TMP36, DC load current, DC
  load power, DC load energy, planar required force and DC constant-current charge methods, their authority artifacts,
  semantics, pins and user-facing behaviour stay unchanged; bounded updates to assertions on the owner content version,
  the implementation version, the closed inventory and the binding count, caused only by this admission, are expected and
  allowed.
- **Still excluded:** a twelfth method or consumer; owner ranges; string parsing in the owner; any conversion or
  duty-cycle / percentage quantity; any equivalent-DC, load-response, motor-speed, torque, heating, average-power, RMS,
  current, ripple, filter, switching-frequency, time-constant, free-wheeling, driver, switching-device, dead-time or loss
  result; any converter (buck, boost or other) result; any bipolar waveform; any result transfer between calculations;
  general 28-T3 activation; a generic solver, waveform model, unit registry or conversion graph; persistence (§12);
  provider, AI, external-tool or external-library execution; and every other §13 / §13A–§13I exclusion.

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
- Correction 02 (§13A) is recorded as accepted on the reconciled architecture reviews of the THERM-01 decision record; an
  implementation of it still needs its own Owner authorization and risk-appropriate independent verification.
- Correction 03 (§13B) is Owner-authorized together with its bounded implementation; it carries the same proportionate,
  risk-appropriate verification as that implementation (focused tests and hosted required CI).
- Correction 04 (§13C) is Owner-authorized together with its bounded implementation, under the same proportionate,
  risk-appropriate verification.
- Correction 05 (§13D) is Owner-authorized together with its bounded implementation, under the same proportionate,
  risk-appropriate verification.
- Correction 06 (§13E) is Owner-authorized together with its bounded implementation, under the same proportionate,
  risk-appropriate verification.
- Correction 07 (§13F) is Owner-authorized together with its bounded implementation, under the same proportionate,
  risk-appropriate verification.
- Correction 08 (§13G) is Owner-authorized together with its bounded implementation, under the same proportionate,
  risk-appropriate verification.
- Correction 09 (§13H) is Owner-authorized together with its bounded implementation, under the same proportionate,
  risk-appropriate verification.
- Correction 10 (§13I) is Owner-authorized together with its bounded implementation, under the same proportionate,
  risk-appropriate verification.
- Correction 11 (§13J) is Owner-authorized together with its bounded implementation, under the same proportionate,
  risk-appropriate verification.

## 17. Non-authorization (restated)

This document authorizes no implementation, runtime owner, adapter, method, unit vocabulary, conversion factor, constant,
equation, schema, store, persistence, test, route or user-facing behaviour; no CAP-13, THERM-01, Technical Realization or
Stage-36 work; no Master Roadmap stage entry, checkbox, marker or count change; no CAP number; and no deployment or release.
Correction 02 (§13A) authorizes the bounded second-admission contract boundary only: no THERM-01 method admission, runtime,
artifact or test change, and no Stage 27 entry.
