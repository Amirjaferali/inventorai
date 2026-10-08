# STAGE 25 / CAP-13 — TWO-SUPPORT STATIC REACTIONS METHOD CONTRACT (ACCEPTED)

STATUS: ACCEPTED DOCUMENTATION-ONLY CONTRACT OF RECORD — NO IMPLEMENTATION AUTHORIZED — NO METHOD ADMISSION — NO
NUMERICAL RESULT AUTHORIZED. `STAGE 25: NOT ENTERED` · `STAGE 25: NOT AUTHORIZED` · `CAP-13: NOT ACTIVATED` ·
`ACTIVE CONTRACT: NONE`.
AUTHORITY LEVEL: subordinate to the CAP-13 entry of the
[Capability Enrichment Register](INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md) and to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its accepted Correction 01). It amends neither. Where this document and either of them
differ, they win and the difference is a defect of this document.
RECORDED: 2026-10-07, by Owner authorization of ONE documentation-only contract candidate. The Owner selected
`CAP-13-STATIC-REACTIONS-TWO-SUPPORT-V1` as the FIRST-INCREMENT CANDIDATE for Stage 25 / CAP-13. That selection authorizes
only this documentation; it enters no Stage, activates nothing, implements nothing and admits nothing.
BASE: originally cut from `feature/atomic-json-session-persistence` at `daca52aaab6e2ff9da7b6d6969434d81fd1595f6`;
reconciled for review with the current authoritative base at `4a2620e3be7f2c0d63e5b0386e1f24e7be1b956e` (which adds only
the merged CI test-sharding correction).
LEVEL-1 REVIEW: `B — LEVEL-1 PASS WITH REQUIRED BOUNDED CORRECTIONS`; corrections C-1 (NASA source-use scope, §3) and C-2
(mandatory General and Structural disclosure meanings, §10) are applied. The method itself is unchanged.
RELATED: the [bounded stiffness method contract](STAGE25_CAP13_BOUNDED_STIFFNESS_METHOD_CONTRACT.md) stays
`ACCEPTED DOCUMENTATION-ONLY FUTURE METHOD CANDIDATE — NOT ADMITTED`, with D-1 and D-5 CLOSED and `D-7: OPEN`; nothing here
changes its technical clauses or closes or weakens its D-7.
ACCEPTANCE: 2026-10-07, by Owner decision after the independent non-authoring Level-1 semantic / technical review
(initial verdict `B — LEVEL-1 PASS WITH REQUIRED BOUNDED CORRECTIONS`), the applied corrections C-1 and C-2, and the
targeted delta review (`A — TARGETED DELTA PASS`; `NO FURTHER REVIEW`). Recorded documentation-only: the technical method
is unchanged by the acceptance, and references in the body to "this candidate" read as this accepted contract. The
acceptance does not implement anything, admit the method, authorize a numerical result or any user-facing CAP-13
behaviour, enter Stage 25 or activate CAP-13.
ACCEPTANCE PATH: COMPLETE — one non-authoring Level-1 semantic / technical review, its bounded corrections and targeted
delta review, then the Owner acceptance above. No new governance mechanism is created.
CORRECTION 01: `CORRECTION 01 — ACCEPTED DOCUMENTATION-ONLY CORRECTION OF RECORD`. It addresses ONLY the refusal /
shared-owner-state layering in §8 (the former sentence mapping every refusal to the shared owner's `REFUSAL` state
contradicted calc/units contract §7 / §8). The accepted method, its sources, numeric domain, declarations, screen,
disclosure, ownership and blockers are unchanged.
CORRECTION 01 ACCEPTANCE: 2026-10-07, by Owner decision after the independent non-authoring Level-1 semantic review
(`B — LEVEL-1 PASS WITH REQUIRED BOUNDED CORRECTIONS`), the one required pre-owner invalid-numeric correction (applied),
and the targeted delta review (`A — TARGETED DELTA PASS`; `NO FURTHER REVIEW`); architecture verdict
`NO ARCHITECTURE IMPACT`. Recorded documentation-only: it implements nothing, admits no method, closes no further
admission blocker, enters no Stage and activates nothing.
*(Superseded 2026-10-07 by the Owner's acceptance of Correction 01, preserved — was: "CORRECTION 01: `CORRECTION 01 —
DOCUMENTATION-ONLY CORRECTION CANDIDATE — NOT YET ACCEPTED`. … It needs one non-authoring Level-1 semantic review before
a separate Owner acceptance; the accepted contract of record stays as accepted until then.")*
*(Superseded 2026-10-07 by the Owner's acceptance, preserved — was: "STATUS: DOCUMENTATION-ONLY CONTRACT CANDIDATE — NOT
ACCEPTED — NO IMPLEMENTATION AUTHORIZED — NO METHOD ADMISSION — NO NUMERICAL RESULT AUTHORIZED."; the title read
"(CANDIDATE)".)*
A-3 JOURNEY GATE: `A-3 JOURNEY GATE — ACCEPTED DOCUMENTATION-ONLY DECISION OF RECORD`. Accepted 2026-10-07 by Owner
decision after the Lead review (`B — PASS WITH NON-BLOCKING NOTES`); merged in PR #772 (merge
`0acc6bca3337c2734aaecae5d3e3434841e70fd8`). §12A is the journey gate for the first user slice; it changes no clause of
§§1–12 and enables no user-facing capability.
*(Superseded 2026-10-07 by the Owner's acceptance and the PR #772 merge, preserved — was: "A-3 JOURNEY GATE: `A-3 JOURNEY
GATE — DOCUMENTATION-ONLY CANDIDATE — NOT YET ACCEPTED`. §12A records the journey gate for the first user slice and §15
records A-3 as closed by it, effective only on Owner acceptance and merge.")*
A-4 ARABIC UX: `A-4 ARABIC DISCLOSURE AND UX WORDING — ACCEPTED DOCUMENTATION-ONLY DECISION OF RECORD`. Accepted by Owner
decision after the Lead review; merged in PR #773 (merge `65f771d5f3b4820b8d2513797cd3f2d4b05c575d`). §12B is the Arabic
fixed disclosure and the Arabic wording of the first user slice; it changes no clause of §§1–12A and keeps the English as the
authority for meaning.
*(Superseded by the Owner's acceptance and the PR #773 merge, preserved — was: "A-4 ARABIC UX: `A-4 ARABIC DISCLOSURE AND UX
WORDING — DOCUMENTATION-ONLY CANDIDATE — NOT YET ACCEPTED`. §12B records the Arabic fixed disclosure and the Arabic wording of
the first user slice, consolidated from the independent Arabic review; §15 records A-4 as closed by it, effective only on
separate Owner acceptance and a verified merge. It changes no clause of §§1–12A, keeps the English as the authority for
meaning and enables no user-facing capability.")*
A-5 FIRST IMPLEMENTATION: `STAGE 25 — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1: DELIVERED` (recorded in its after-merge
form; Git / GitHub own its PR, merge and review identity). The separately Owner-authorized A2 first increment implements this
method with its ONE named consumer: the shared owner `engine/deterministic_calculation.py` (unnumbered) with its artifact
`docs/governance/deterministic_calculation_config/deterministic_calculation_owner_v1.json`, the method adapter
`engine/cap13_static_reactions_method.py`, the consumer `engine/cap13_static_reactions.py` with the CAP-13-owned artifact
`docs/governance/cap13_content_config/static_reactions_two_support_v1.json`, and the request-local page of §12A
(`/session/<sid>/support-reactions`). `STAGE 25: ENTERED / PARTIAL — CAP-13 TWO-SUPPORT STATIC REACTIONS SLICE 1 ONLY`;
`FULL CAP-13: NOT AUTHORIZED`. The STATUS line above and §§13 / 16 are this document's acceptance-time record; this
paragraph is the current state.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE`. This candidate fills no active-contract slot and is not a product increment.
- `STAGE 25: NOT ENTERED` · `STAGE 25: NOT AUTHORIZED` · `CAP-13: NOT ACTIVATED`. No roadmap checkbox, marker or count
  changes.
- The shared calculation / units owner is NOT implemented; no first increment is authorized; no method is admitted; no CAP-13
  runtime method exists; no numerical CAP-13 result is authorized.
- `CALCULATION RESULT ≠ SUPPORT CAPACITY ≠ SAFETY CONCLUSION`.
- `TECHNICAL DEEPENING SOURCE RULE: OPEN / LAWFULLY REUSABLE SOURCES ONLY` · `PUBLICLY VIEWABLE ≠ OPENLY REUSABLE`.

## 1. Purpose and scope

For ONE declared loaded configuration, the method states the two vertical support reactions required by the inventor's
DECLARED bounded planar static equilibrium model. Its user value: how the declared static total weight is split between
two declared supports — in particular for an off-centre centre of gravity — so the inventor knows the load each support or
attachment must subsequently be validated for.

**Non-goals.** No support capacity, attachment adequacy, bearing check, material check, deformation, deflection,
buckling, fracture, tipping or detachment analysis; no thickness or specification; no stability or safety conclusion; no
torque output; no inference of any declaration; no second method, solver, formula registry, materials database, unit
conversion or conversion graph.

## 2. Method identity and version

- Final method identifier (Owner decision 2026-10-07; closes A-2, §15): `method_id = "cap13:static_reactions_two_support"`
  — exact and case-sensitive, with NO aliases.
- Initial method version: `method_version = "1.0"`, carried separately from the identifier (calc/units contract); the
  version is not encoded in the identifier.
- Historical working identity (descriptive / pre-admission history only; not a runtime alias):
  `CAP-13-STATIC-REACTIONS-TWO-SUPPORT-V1`.
- The identifier and version are recorded only; no registry, artifact or implementation exists, and the method is NOT
  admitted.
- Version rule: any material change to the equations, the applicability, the declarations, the numeric domain, the
  refusal or abstention semantics, the source authority or a role meaning is a new version. A result always carries the
  version it was produced under. `method_id` stays stable while it remains the same method identity; such a material
  change takes a new `method_version`.

## 3. Source and source-use records (Lead-supplied inspection, 2026-10-07)

| Record | Source identity | Official location | Claims this record may support (and only these) |
|---|---|---|---|
| NASA-S1 | NASA Glenn Research Center — Beginners Guide to Aeronautics — "Equilibrium" | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/equilibrium/ | equilibrium requires zero net force; equilibrium requires zero net torque; torque / moment is force multiplied by perpendicular distance; opposing moments balance at equilibrium |
| NASA-S2 | NASA Glenn Research Center — Beginners Guide to Aeronautics — "Center of Gravity" | https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/center-of-gravity/ | the centre of gravity is the average location of an object's weight; the total weight acts through the centre of gravity; the weight-moment relationship represented by `cg × total weight` |

**Inspection basis.** Both records were inspected by the Lead on 2026-10-07 and are recorded here as Lead-supplied,
following the CAP-12 and bounded-stiffness precedent. The Lead's inspection found no third-party attribution attached to
the textual mathematical relationships relied upon on either page.

**Derivation, not publication.** The two-support reaction equations in §4 are CAP-13's own explicit method derivation
from these equilibrium and centre-of-gravity principles. NASA does not publish this CAP-13 method, and no statement here
says or implies that it does.

**Cross-reference (identity only, no duplicated metadata).** The NASA Glenn "Torque (Moment)" page is already recorded
as `mechanical:PR006` in `domains/domain_provenance.json`; it is cited here only as the same source identity for the
torque relationship. The Mechanical Domain Pack's reference fundamentals stay inert reference content and are not
calculation authority for this method.

**NASA source-use assessment for NASA-S1 and NASA-S2 (not a legal opinion).** The policy basis is the NASA STI Program
"Disclaimers, Copyright Notice, and Terms and Conditions of Use" (https://sti.nasa.gov/disclaimers/). The same policy page
is already identified in repository record `mechanical:PR010`, whose existing disposition stays scoped to
`mechanical:PR006`, `mechanical:PR007` and `mechanical:PR008` only; it does not cover NASA-S1 or NASA-S2. CAP-12 used the
same policy page through its own record `cap12:SU001`. This contract therefore records its OWN bounded, Lead-supplied
assessment for NASA-S1 and NASA-S2, inspected 2026-10-07: no third-party attribution was observed attached to the textual
mathematical relationships relied upon, and images, graphics, multimedia, branding and any unidentified or third-party
material stay excluded. The policy page supports, in substance: U.S. Government works are generally not protected
by copyright in the U.S. (17 U.S.C. §105); NASA-hosted pages may contain privately created copyrighted content; public
availability does not transfer third-party rights; and NASA material may not be used to imply endorsement. Use is
therefore factual and paraphrased only: no copied NASA explanatory prose; no NASA image, graphic, multimedia, logo,
insignia or branding; no third-party or unidentified page content; neutral source acknowledgement only; and no statement
or implication that NASA endorses, reviewed or approved InventorAI or any project. `PUBLICLY VIEWABLE ≠ OPENLY REUSABLE`
is preserved.

**Unit source.** NIST SP 811 (2008 Edition), DOI `10.6028/NIST.SP.811e2008`, as already recorded in the bounded
stiffness method contract §3A, D5-6 — reused by reference for `N` (newton, force) and `mm` (milli prefix with metre,
length) only. No conversion is needed or authorized, and `MPa` is not used by this method. That reference creates none of
the future shared owner's governed unit records (calc/units contract §9).

**Excluded.** ASTM, NDS and AWC text or values (no dependency exists); vendor data; any copied prose or imagery.

## 4. Method definition (CAP-13 method authority)

**Model.** One declared loaded configuration, represented by its declared total weight acting through its declared centre
of gravity, resting on exactly two declared parallel, horizontal, push-only support reaction lines, in a planar static
equilibrium model.

**Equilibrium (from NASA-S1 and NASA-S2).** Vertical force balance: `R_L + R_R = P`. Moment balance about the left
reaction line: `R_R × L = P × x`.

**Executed form.** `R_R = P × x / L` · `R_L = P × (L − x) / L`. Each output is computed from its own expression; the force
balance is the derivation and a disclosed identity, not a runtime equality check — no tolerance is authorized. No torque
or moment value is emitted, and the ratio `x / L` is an internal intermediate only: it is never a user input or an output
role.

**Dimensional check.** `N × mm / mm = N` for both outputs.

## 5. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact token | Source of value |
|---|---|---|---|---|
| `P` | total weight force of everything included in the declared modelled configuration | force | `N` | user-declared numeric input |
| `L` | horizontal separation between the two declared support reaction lines | length | `mm` | user-declared numeric input |
| `x` | horizontal position of the declared centre of gravity, measured perpendicular to the reaction lines from the left line | length | `mm` | user-declared numeric input |
| `R_L` | left vertical reaction | force | `N` | output |
| `R_R` | right vertical reaction | force | `N` | output |

No alias tokens; no other unit is accepted (`UNIT_NOT_SUPPORTED`).

## 6. Applicability declarations

Every declaration is closed and explicit, made by the inventor through the consumer. None is inferred, defaulted or
pre-answered; a missing answer refuses (`NOT_DECLARED`) and a different answer refuses (§8).

| Declaration | The only accepted value in v1 | Refusal if different |
|---|---|---|
| condition | static | `LOAD_NOT_SUPPORTED` |
| applied load | gravity is the only modelled applied load | `LOAD_NOT_SUPPORTED` |
| weight | `P` is the total weight force for everything included in the declared modelled configuration | `LOAD_NOT_SUPPORTED` |
| support count | exactly two support reaction lines | `SUPPORT_NOT_SUPPORTED` |
| support geometry | the two support lines are parallel and horizontal within the planar model, and `x` is measured perpendicular to them from the left line | `SUPPORT_NOT_SUPPORTED` |
| support action | both supports vertical, force-only | `SUPPORT_NOT_SUPPORTED` |
| support direction | both supports push-only / bearing; no hold-down tension | `SUPPORT_NOT_SUPPORTED` |
| support moment | no support moment or couple | `SUPPORT_NOT_SUPPORTED` |
| load paths | no third support and no additional load path | `SUPPORT_NOT_SUPPORTED` |
| centre of gravity | its position is explicitly declared by the inventor — never inferred and never defaulted to midspan | `NOT_DECLARED` |
| high-risk screen | all nine items answered (§9) | `NOT_DECLARED` |

**Outside the calculation (disclosed, not thresholded).** The model calculates no deformation. Deformation, support
movement, geometry change under load and load redistribution caused by deformation are outside this calculation. No
small-deflection, displacement, stiffness or deformation validity threshold is introduced.

## 7. Numeric domain (Owner decision)

- All values are finite typed numbers; no strings, booleans, NaN or infinities (`INVALID_NUMERIC_INPUT`).
- `P > 0` and `L > 0`; zero or negative `P` or `L` is `INVALID_NUMERIC_INPUT`.
- `0 ≤ x ≤ L` — the closed domain. No tolerance is authorized.
- **Endpoints are valid.** At `x = 0`: `R_L = P`, `R_R = 0`. At `x = L`: `R_L = 0`, `R_R = P`. A zero reaction is a
  boundary case of the declared idealized model; it does NOT establish physical stability, and the configuration is never
  called safe or stable.
- **Outside the support span.** `x < 0` or `x > L` returns `CG_OUTSIDE_SUPPORT_SPAN` with no numerical payload. This is a
  DOMAIN REFUSAL, not `INVALID_NUMERIC_INPUT`: the declared model uses push-only supports with no hold-down, and a negative
  reaction would contradict it.

## 8. Refusal and abstention semantics

**Refusal (`UNABLE TO RECOMMEND`) — closed reason tokens.** Reused where semantically exact: `NOT_DECLARED` ·
`LOAD_NOT_SUPPORTED` · `SUPPORT_NOT_SUPPORTED` · `INVALID_NUMERIC_INPUT` · `UNIT_NOT_SUPPORTED` · `KNOWLEDGE_UNAVAILABLE`
(a governed record missing, malformed or failing its integrity check). Added — exactly one method-level token:
`CG_OUTSIDE_SUPPORT_SPAN`. A refusal carries one reason and no numerical payload; nothing falls back to generic advice.

**Two layers (Correction 01).** These tokens are distinct from the shared owner's states and never redefine them:

- **Layer A — CAP-13 capability semantics (this contract).** Applicability, the method numeric domain (§7), the
  user-facing refusal reasons above, the abstention below and the fixed disclosure (§10). The tokens above are CAP-13
  display reasons, NOT shared-owner states or shared-owner reason tokens.
- **Layer B — shared-owner local states (calc/units contract §7, §8, unchanged and authoritative).** `SUCCESS` ·
  `UNABLE_TO_DETERMINE` · `FAILURE` · `REFUSAL` and their §8 reason tokens. This contract adds no owner state or token,
  changes no owner mapping and does not force any owner outcome to `REFUSAL`.

**Pre-owner outcomes (CAP-13 only; the owner is not called; no numerical payload).**

| Condition | CAP-13 outcome |
| --- | --- |
| A §6 declaration missing | `NOT_DECLARED` |
| Load not as declared in §6 | `LOAD_NOT_SUPPORTED` |
| Supports not as declared in §6 | `SUPPORT_NOT_SUPPORTED` |
| Any YES on the §9 screen | `ENGINEERING REVIEW REQUIRED` (abstention) |
| `P`, `L` or `x` violates the §7 numeric-type requirement — a string, a boolean, NaN, an infinity or any other non-finite or non-numeric value | `INVALID_NUMERIC_INPUT` |
| `P ≤ 0` or `L ≤ 0` (§7) | `INVALID_NUMERIC_INPUT` |
| A finite numeric `x` with `x < 0` or `x > L` (§7) | `CG_OUTSIDE_SUPPORT_SPAN` |

This pre-owner CAP-13 validation applies the inventor-facing §7 numeric domain before the shared owner is invoked; the
owner is not called after any of these outcomes. For `x`, an invalid type or non-finite value is `INVALID_NUMERIC_INPUT`,
while a finite numeric value outside `[0, L]` is `CG_OUTSIDE_SUPPORT_SPAN`; these stay distinct, and `x = 0` and `x = L`
stay valid. `CG_OUTSIDE_SUPPORT_SPAN` is a CAP-13 method-domain refusal: it is not `INVALID_NUMERIC_INPUT`, not an
owner-local state, and the owner must not be called after it.

**Requests that reach the owner.** The owner's §7 / §8 state controls, unchanged; CAP-13 only selects its display reason:

| Shared-owner local state / token (Layer B) | CAP-13 display (Layer A) |
| --- | --- |
| `REFUSAL` / `INVALID_NUMERIC_INPUT` | `INVALID_NUMERIC_INPUT` — defence in depth only for this first consumer: the inventor-facing §7 invalid-numeric cases are resolved by CAP-13 before the owner is called; if the owner nevertheless returns this, its exact state / token is preserved internally |
| `REFUSAL` / `UNIT_NOT_ADMITTED` or `REFUSAL` / `UNKNOWN_UNIT` | `UNIT_NOT_SUPPORTED` (the first consumer passes the fixed §5 unit tokens; the inventor chooses no unit) |
| `REFUSAL` / `METHOD_NOT_REGISTERED` | `KNOWLEDGE_UNAVAILABLE` (the governed admitted method basis is unavailable, so the capability cannot execute); the owner `REFUSAL` and its exact token are preserved internally |
| `REFUSAL` / `VERSION_MISMATCH` | `KNOWLEDGE_UNAVAILABLE`; the owner `REFUSAL` and its exact token are preserved internally |
| `UNABLE_TO_DETERMINE` / `SOURCE_UNAVAILABLE` (source unavailable only) | `KNOWLEDGE_UNAVAILABLE`; the owner `UNABLE_TO_DETERMINE` and its exact token are preserved internally |
| `FAILURE` / `EXECUTION_INTEGRITY_FAILURE` (the calc/units contract's post-admission integrity failure, including a tampered or integrity-failing governed record) | `KNOWLEDGE_UNAVAILABLE` may be displayed; no numerical payload; the owner `FAILURE` is preserved internally and is never rewritten as `REFUSAL` |

`SOURCE_UNAVAILABLE`, `METHOD_NOT_REGISTERED` and `VERSION_MISMATCH` stay distinct owner conditions, and
`EXECUTION_INTEGRITY_FAILURE` is never used in place of any of them. `KNOWLEDGE_UNAVAILABLE` is a CAP-13 display reason
only and therefore does not fix one owner state; no owner-local state or token is rewritten.

**Unmapped owner outcomes.** The table covers the expected first-consumer cases only; it does not redefine every
shared-owner token. Any owner-local state / token not mapped above stays authoritative as returned by the shared owner:
CAP-13 fails closed with no numerical payload, preserves that state / token for diagnosis, invents no CAP-13 reason, does
not map it to `KNOWLEDGE_UNAVAILABLE` by default and creates no new generic status. A later implementation contract must
not admit this consumer unless every owner-local outcome reachable from its exact fixed request shape has a deterministic
handling rule.

**Defence in depth.** The owner may itself fail closed on range or applicability. An owner `INPUT_OUTSIDE_ADMITTED_RANGE`
or `APPLICABILITY_REFUSED_BY_METHOD_AUTHORITY` is never relabelled `CG_OUTSIDE_SUPPORT_SPAN`; if one reaches the capability
despite the pre-owner gate, CAP-13 fails closed with no numerical payload and preserves the owner-local state for
diagnosis. No new generic status and no second calculation engine is introduced.

**Abstention (`ENGINEERING REVIEW REQUIRED`).** Any YES on the §9 screen: no calculation, no numerical payload, and
specialist engineering review is named.

## 9. High-risk screen (reused, not a new safety engine)

The existing CAP-13 nine-item declared screen of the bounded stiffness method contract §9 is reused unchanged. Each item is
answered explicitly yes / no: supports people; overhead or falling hazard; use by or for children; safety-critical load
path; pressure; high temperature; battery containment; medical use; food contact. Any unanswered item: `NOT_DECLARED`. Any
YES: `ENGINEERING REVIEW REQUIRED`, with no numerical payload. All NO means only that this bounded calculation may
proceed — it NEVER means safe. SafetySignal stays separate and untouched: the screen neither reads nor feeds it, and no
second safety engine is created or called. The CAP-13 register's mandatory warning categories stay binding.

## 10. Result, provenance and fixed disclosure

- **Calculated:** `R_L` and `R_R` in N — only the vertical support reactions required by the inventor's DECLARED bounded
  static equilibrium model. The result is `UNVALIDATED` and is NOT evidence.
- **Provenance carried with a result:** method identity and version; source records NASA-S1, NASA-S2 and the NIST unit
  reference; the echoed inputs and declarations; both outputs.
- **No thickness or recommendation level:** v1 recommends nothing and assigns neither `CONCEPTUAL` nor
  `PROTOTYPE-SUITABLE`.

**Fixed disclosure (English; the Arabic wording is settled under the UX review before any display).** It carries the
CAP-13 register's mandatory *General* and *Structural* warning meanings, adapted only in grammar to reaction outputs; it
adds no capacity, allowable-stress, design-value, safety-factor-value, adequacy or pass / fail statement.

> These are the vertical support reactions required by the static equilibrium model you declared: two parallel,
> horizontal, push-only supports carrying your stated total weight through your stated centre of gravity. This result is
> preliminary and advisory, not a final engineering or manufacturing specification. Do not rely on these reactions to
> size, select, approve or validate any support or attachment before independently verifying the real configuration,
> including, as applicable, the actual loads and load paths, the supports and attachments, joints, stress, deformation,
> fatigue, impact and safety factor. They are not
> validated and are not evidence. They do not establish support capacity, attachment adequacy, bearing adequacy, material
> adequacy, structural safety, code compliance, certification or production suitability, and they do not show that the
> configuration will not deflect, buckle, fracture, tip or detach. Deformation, support movement, geometry change under
> load and load redistribution caused by deformation are outside this calculation. InventorAI does not check that your
> declarations match the physical configuration. A zero reaction is a boundary case of this idealized model and does not
> establish physical stability. Reference source material: NASA Glenn Research Center (equilibrium and centre-of-gravity
> principles); the two-support equations are InventorAI's own derivation.

## 11. Ownership and the A2 mapping

- **CAP-13 owns:** the method authority (§4), the applicability declarations (§6), the numeric domain (§7), the source
  truth (§3), and the refusal, abstention and disclosure semantics (§8–§10) — in a future CAP-13-owned governed artifact,
  not a Domain Pack and not in `domains/domain_provenance.json`.
- **The shared calculation / units owner (future)** owns only the admission and execution envelope of the accepted A2
  shape (calc/units contract §3, §13): exact role → quantity kind → unit token validation; deterministic execution;
  result, digest and version integrity. It owns no load, support or centre-of-gravity truth.
- **The consumer (future CAP-13 user slice)** owns explicit declaration and numeric capture, and display only.
- **A2 mapping:** this ONE method is the one admitted method and the first CAP-13 user slice is the one named consumer. Role
  set: `P` force `N`; `L` and `x` length `mm`; `R_L` and `R_R` force `N`. No conversion operation, no dimensionless role, no
  alias token and no second method.

## 12. No persistence, no progression

Request-local / session-only. No store, schema, migration, report, PDF, Structured Export, API, ledger, evidence,
readiness, maturity, progression or deliverable effect. `engine/requirement_quantity.py` is neither read nor written, and
no requirement-quantity text is parsed.

## 12A. Journey gate for the first user slice (A-3)

Journey decision only. It adds no clause to §§4–11, no reason token, no state, no source and no owner; it reuses the
existing optional CAP-12 advisory pattern (`web/app.py` form-mockup advisory routes) without changing CAP-12 and without a
generic journey framework. Nothing here is implemented or enabled: a user-facing slice exists only after A-4 and A-5.

**Entry and eligibility.**
- ONE optional entry on the session page, beside the CAP-12 advisory entry, offered only while the project is eligible.
  It is never required, has no progression, readiness or answer-state dependency, and declining or ignoring it never
  blocks the core invention journey. It is not offered from the report, PDF, Structured Export or API.
- Eligible means: the request passes the existing project authorization (`_project_authorized`) AND the project's
  durable `confirmed_domain`, read from the durable reconstruction inputs as the CAP-12 gate reads it and never from the
  request, is `mechanical`. The entry and the submission read that same single value.
- An unreadable or any other root domain fails closed: no entry is offered and a submission is not evaluated (no
  calculation, no CAP-13 reason token).
- Gate-scope limitation, recorded explicitly: an integrated invention whose initial analysis focus is Electrical /
  Electronics is excluded even when it records a Mechanical part. This is a scope limit of this first slice, not a
  technical incompatibility verdict; widening it needs its own decision.

**Capture (one page; nothing inferred, defaulted or pre-answered).**
- Each §6 declaration is presented with its exact accepted v1 meaning, and the inventor explicitly answers whether the
  configuration matches that exact statement or differs from it. No generic confirmation replaces the individual
  declarations, no choice is pre-selected, and nothing is taken from classifier output, session answers, requirement
  quantities or any other project data.
- The centre-of-gravity declaration is satisfied only by the inventor's own entry of `x`; it is never defaulted to
  midspan.
- All nine §9 screen items are answered explicitly yes / no, none pre-selected.
- `P`, `L` and `x` are entered as numbers in the fixed units of §5 (`N`, `mm`); the units are displayed, not chosen.
- The existing request-integrity (CSRF) guard and project authorization apply; the form has a strict field allowlist
  and each field must occur exactly once, otherwise the request is rejected as malformed (no CAP-13 reason token, no
  calculation).

**Pre-owner evaluation order (deterministic, fail closed).** Evaluated in this order; the FIRST failing stage alone
determines the outcome, so a request carries exactly one reason (§8) and no later stage is evaluated:

1. Request integrity, project authorization and eligibility (above).
2. Completeness: any §6 declaration, any of the nine §9 items, or any of `P`, `L`, `x` left unanswered or empty →
   `NOT_DECLARED`.
3. High-risk screen: any YES → `ENGINEERING REVIEW REQUIRED`; the calculation owner is not invoked.
4. Load declarations (condition, applied load, weight) differing from §6 → `LOAD_NOT_SUPPORTED`.
5. Support declarations (count, geometry, action, direction, moment, load paths) differing from §6 →
   `SUPPORT_NOT_SUPPORTED`.
6. Numeric type and positivity (§7): any of `P`, `L`, `x` present but not a finite number, or `P ≤ 0` or `L ≤ 0` →
   `INVALID_NUMERIC_INPUT`.
7. Centre-of-gravity span (§7): a finite numeric `x` with `x < 0` or `x > L` → `CG_OUTSIDE_SUPPORT_SPAN`; `x = 0` and
   `x = L` are valid.
8. Only after stages 1–7 all pass is the shared calculation owner invoked, with the exact §11 role / unit request; its
   outcome is handled exactly as §8 states (Layer B owner states preserved; Layer A display reasons only; unmapped owner
   outcomes fail closed).

This order only fixes precedence among the existing outcomes; their meanings in §§7–9 are unchanged.

**Result presentation.** As the CAP-12 advisory does: rendered in the response to the submission itself, with no redirect
and nothing stored. On success it shows only `R_L` and `R_R` in `N`, the echoed declared inputs and declarations,
`method_id` and `method_version` (§2), the NASA-S1, NASA-S2 and NIST unit references (§3), the `UNVALIDATED` status and the
fixed disclosure (§10). A refusal or abstention shows its one reason and no numerical payload. §12 applies unchanged: no
persistence, evidence, readiness, progression, report, PDF, Structured Export or API effect.

**Language.** This section records the journey decision only. The Arabic disclosure and UX wording stay with A-4; no
Arabic display of the capability or its result is authorized before A-4 is closed.

## 12B. Arabic disclosure and UX wording for the first user slice (A-4)

Wording decision only. The English of §§5–10 and §12A stays the authority for meaning; this section adds no clause, reason
token, state, source, owner, route or store, and changes no calculation semantics. Any divergence between the Arabic below
and the English is a defect of the Arabic, and the English wins. The wording is Modern Standard Arabic and follows the
Arabic-first policy (precise English technical terms may stay in parentheses). It reuses the CAP-12 advisory wording
precedents (`web/ui_text.py`, `UI_CAP12_*`) by copying into future CAP-13-owned keys, never by changing CAP-12. Nothing
here is implemented or displayed: Arabic display needs this section accepted and merged, and a user-facing slice needs A-5.

**B-1 Fixed disclosure (Arabic rendering of §10, Lead-approved; shown in full wherever §10 is shown).**

> هذه هي ردود الأفعال الرأسية للمسندين التي يتطلبها نموذج الاتزان الساكن الذي صرّحت به: مسندان متوازيان أفقيان يعملان
> بالدفع فقط، ويحملان الوزن الكلي الذي ذكرته، والمؤثر عند مركز الثقل الذي حددته.
>
> هذه النتيجة أولية وإرشادية، وليست مواصفة هندسية أو تصنيعية نهائية.
>
> لا تعتمد على ردود الأفعال هذه لتحديد أبعاد أي مسند أو وسيلة تثبيت، أو اختيارهما أو اعتمادهما أو التحقق من صلاحيتهما،
> قبل التحقق المستقل من التكوين الفعلي، بما في ذلك، حسب الحالة: الأحمال الفعلية ومسارات انتقالها، والمساند ووسائل
> التثبيت، والوصلات، والإجهاد، والتشوّه، والكلال، والصدم، ومعامل الأمان.
>
> هذه النتائج غير مُتحقَّق منها وليست أدلة.
>
> ولا تثبت قدرة المسند على تحمل الأحمال، ولا كفاية وسائل التثبيت أو أسطح الارتكاز أو المواد، ولا السلامة الإنشائية، ولا
> الامتثال للأكواد والمعايير، ولا الحصول على شهادة اعتماد، ولا الملاءمة للإنتاج.
>
> كذلك لا تثبت أن التكوين لن يترخّم أو ينبعج أو ينكسر أو ينقلب أو ينفصل.
>
> التشوّه، وحركة المساند، وتغيّر الشكل الهندسي تحت الحمل، وإعادة توزيع الأحمال الناتجة عن التشوّه، كلها خارج نطاق هذا
> الحساب.
>
> لا يتحقق InventorAI من أن تصريحاتك تطابق التكوين المادي الفعلي.
>
> رد الفعل الصفري حالة حدّية في هذا النموذج المثالي، ولا يثبت الاستقرار الفيزيائي الفعلي.
>
> **المراجع:** مركز غلين للأبحاث التابع لناسا (NASA Glenn Research Center)، لمبادئ الاتزان ومركز الثقل. أما معادلتا
> حساب ردود أفعال المسندين فهما اشتقاق خاص بـInventorAI.

Parity with §10, sentence by sentence: the declared model (vertical reactions; two parallel, horizontal, push-only
supports; stated total weight through the stated centre of gravity) · preliminary and advisory, not a final engineering or
manufacturing specification · no sizing, selection, approval or validation of any support or attachment before independent
verification of the actual loads and load paths, supports and attachments, joints, stress, deformation, fatigue, impact and
safety factor · not validated, not evidence · no support capacity, attachment, bearing or material adequacy, structural
safety, code / standard compliance, certification or production suitability · no assurance against deflection, buckling,
fracture, tipping or detachment · deformation, support movement, geometry change under load and deformation-driven load
redistribution excluded · declarations not checked against the physical configuration · a zero reaction does not establish
physical stability · NASA Glenn principles distinguished from InventorAI's own derivation. No meaning is added, removed or
softened, and no source text is copied.

**B-2 Applicability declarations (§6).** Each is shown as its exact statement; the inventor answers «يطابق تكويني» or
«يختلف تكويني», none pre-selected. "Differs" yields the §6 refusal of that row.

| §6 declaration | Arabic statement |
|---|---|
| condition | الحالة ساكنة. |
| applied load | الجاذبية هي الحمل المطبَّق الوحيد في النموذج. |
| weight | الوزن الكلي هو قوة الوزن الكلية لكل ما يشمله التكوين المصرَّح به في النموذج. |
| support count | يوجد خطّان اثنان بالضبط لردود أفعال المسندين. |
| support geometry | خطّا ردّ فعل المسندين متوازيان وأفقيان ضمن النموذج المستوي، ويُقاس موضع مركز الثقل عموديًا عليهما ابتداءً من الخط الأيسر. |
| support action | يؤثر كل مسند بقوة ردّ فعل رأسية، وينقل قوة فقط. |
| support direction | يعمل كل مسند بالدفع فقط (ارتكاز)، ولا يوجد أي تثبيت يقاوم الارتفاع بالشد. |
| support moment | لا ينقل أي مسند عزمًا أو ازدواجًا. |
| load paths | لا يوجد مسند ثالث ولا أي مسار إضافي لانتقال الحمل. |
| centre of gravity | تُدخل موضع مركز الثقل بنفسك؛ لا يُستنتج ولا يُوضع في المنتصف تلقائيًا. |

**B-3 High-risk screen (§9).** Stem: «هل ينطبق أيٌّ مما يلي على التكوين؟ أجب عن كل بند بـ«نعم» أو «لا».» — none
pre-selected.

| §9 item | Arabic |
|---|---|
| supports people | يحمل أشخاصًا أو يسندهم |
| overhead or falling hazard | خطر علوي أو خطر سقوط |
| use by or for children | يستخدمه الأطفال أو صُمِّم لهم |
| safety-critical load path | مسار حمل حرج للسلامة |
| pressure | ينطوي على ضغط |
| high temperature | درجة حرارة عالية |
| battery containment | احتواء بطارية |
| medical use | استخدام طبي |
| food contact | تلامس مع الغذاء |

Screen note (always shown with the screen): «الإجابة بـ«لا» عن جميع البنود التسعة تستوفي هذا الفحص فقط؛ ولا تعني أن
التكوين آمن، ولا تُغني عن بقية شروط التطبيق والقيم الرقمية.»

**B-4 Outcome wording (§8, §12A).** One message per outcome, no numerical payload with any of them.

| Outcome | Arabic |
|---|---|
| `NOT_DECLARED` | لم تُجب عن جميع التصريحات وبنود الفحص والقيم المطلوبة. لم يُحسب شيء. |
| `ENGINEERING REVIEW REQUIRED` | أجبت بـ«نعم» عن بند واحد على الأقل في فحص المخاطر العالية. هذه الحالة تتطلب مراجعة هندسية متخصصة، لذلك لم يُحسب شيء. |
| `LOAD_NOT_SUPPORTED` | الحمل الذي صرّحت به خارج ما تغطيه هذه الطريقة. لم يُحسب شيء. |
| `SUPPORT_NOT_SUPPORTED` | المساند التي صرّحت بها خارج ما تغطيه هذه الطريقة. لم يُحسب شيء. |
| `INVALID_NUMERIC_INPUT` | يجب أن تكون القيم أرقامًا محدودة، وأن يكون الوزن الكلي والمسافة بين خطّي ردّ فعل المسندين أكبر من الصفر. لم يُحسب شيء. |
| `CG_OUTSIDE_SUPPORT_SPAN` | موضع مركز الثقل يقع خارج المسافة بين خطّي ردّ فعل المسندين. يتطلب ذلك ردّ فعل سالبًا (شدًّا) عند أحد المسندين، وهذا خارج النموذج المعتمد هنا الذي يفترض مساند تعمل بالدفع فقط. لم يُحسب شيء. |
| `UNIT_NOT_SUPPORTED` | الوحدة غير مدعومة؛ تقبل هذه الطريقة النيوتن (N) والملّيمتر (mm) فقط. لم يُحسب شيء. |
| `KNOWLEDGE_UNAVAILABLE` | المعرفة المرجعية لهذه الطريقة غير متاحة أو لم تجتز فحوصها. لم يُحسب شيء. |
| Owner outcome not mapped by §8 (no reason token) | تعذّر إكمال الحساب. لم يُحسب شيء. |
| Malformed request (§12A; no reason token) | تعذّرت قراءة هذا الطلب. لم يُحسب شيء. |

The unmapped-outcome line is neutral fail-closed wording, not a reason token: the exact shared-owner state and token stay
preserved internally as §8 requires, are not shown and are not mapped to any CAP-13 reason.

**B-5 Entry, input, result and provenance labels.**

| Use | Arabic |
|---|---|
| Session-page link | اختياري: ردود أفعال المسندين لحمل ساكن |
| Link note | حساب إرشادي لنموذج تصرّح به أنت. لا يُحفَظ ولا يكون مطلوبًا أبدًا. |
| Page title | ردود أفعال المسندين (اختياري، غير مُلزِم) |
| Page intro | هذه الصفحة اختيارية. تحسب ردّي الفعل الرأسيين للمسندين اللذين يتطلبهما نموذج الاتزان الساكن الذي تصرّح به. لا يُحفَظ شيء، ولا تُعيق مشروعك أبدًا. |
| Total weight input | الوزن الكلي — نيوتن (N) |
| Separation input | المسافة بين خطّي ردّ فعل المسندين — ملّيمتر (mm) |
| Centre-of-gravity input | موضع مركز الثقل مقيسًا من خط المسند الأيسر — ملّيمتر (mm) |
| Declaration answers | يطابق تكويني / يختلف تكويني |
| Screen answers | نعم / لا |
| Submit | احسب ردود الأفعال |
| Left reaction | ردّ فعل المسند الأيسر (R_L) — نيوتن (N) |
| Right reaction | ردّ فعل المسند الأيمن (R_R) — نيوتن (N) |
| Status | غير مُتحقَّق منه (UNVALIDATED) — ليست أدلة |
| Echoed inputs heading | القيم والتصريحات التي أدخلتها |
| Method line | الطريقة وإصدارها |
| Sources heading | المصادر |
| Sources note | مبادئ الاتزان ومركز الثقل من مواد ناسا (NASA)، ومرجع الوحدات من المعهد الوطني للمعايير والتقنية (NIST). لا تؤيّد ناسا InventorAI ولا هذا الحساب. |
| Back link | العودة إلى مشروعك |
| Scope note (Mechanical-only first slice) | يغطي هذا الحساب حاليًا المشاريع التي محور تحليلها الرئيسي ميكانيكي فقط. قد لا يتاح لاختراع متكامل محور تحليله الأولي كهربائي/إلكتروني حتى لو تضمّن جزءًا ميكانيكيًا؛ هذا قيد في نطاق هذه الشريحة الأولى، وليس حكمًا بعدم التوافق التقني. |

**B-6 Terminology.**

| English | Arabic | Note |
|---|---|---|
| support | مسند (مساند) | used throughout; «وسيلة تثبيت» is reserved for attachment |
| attachment | وسيلة تثبيت | |
| support reaction | ردّ فعل المسند | "vertical" qualifies the reaction force, never the physical member |
| push-only / bearing | يعمل بالدفع فقط (ارتكاز) | «الدفع» is kept distinct from «ضغط» (pressure) |
| no hold-down | لا يوجد تثبيت يقاوم الارتفاع بالشد | |
| force-only | ينقل قوة فقط | kept separate from push-only and no-moment |
| moment / couple | عزم / ازدواج | |
| centre of gravity | مركز الثقل | |
| static | ساكن | §6 meaning only; no added condition |
| pressure | ضغط | generic, not limited to pressure vessels |
| overhead or falling hazard | خطر علوي أو خطر سقوط | not limited to people beneath |
| approve | اعتماد | the verb for a support or attachment |
| certification | شهادة اعتماد | kept separate from code / standard compliance |
| code / standard compliance | الامتثال للأكواد والمعايير | |
| deflect / buckle / fatigue | يترخّم / ينبعج / الكلال | |
| advisory / non-binding | إرشادي / غير مُلزِم | CAP-12 precedent |
| unvalidated / not evidence | غير مُتحقَّق منه / ليست أدلة | existing UI precedent |

**B-7 Right-to-left rendering (requirement for the future implementation, A-5).** Numbers, the unit tokens `N` and `mm`,
the role symbols `R_L` and `R_R`, `method_id`, `method_version` and the English names in parentheses are rendered with
direction isolation inside Arabic text, so that no digit, sign, token or identifier is reordered; numerical values are
never translated or reformatted into a different meaning.

## 13. Stage and lifecycle

This candidate, its later acceptance or both together do not enter Stage 25, activate CAP-13, implement the shared owner,
admit the method, expose a numerical result or change the roadmap count. Stage 25 is entered only by a later, separately
authorized increment that admits a CAP-13 method together with its named consumer — for this method, the shared owner's
A2 first increment admitting it with the first CAP-13 user slice.

## 14. Review items (non-authoring Level-1 semantic / technical review, before acceptance)

- **R-1 Source fidelity:** NASA-S1 and NASA-S2 claims as bounded in §3; the derivation stated as CAP-13's own.
- **R-2 Equilibrium derivation and dimensional correctness** of §4.
- **R-3 Numeric domain:** the closed `0 ≤ x ≤ L`, the valid endpoints and `CG_OUTSIDE_SUPPORT_SPAN` (§7).
- **R-4 Declaration completeness and refusal mapping** of §6 and §8.
- **R-5 Safety boundary:** the reused high-risk screen and the disclosure (§9, §10).
- **R-6 A2 fit and ownership separation** (§11).
- **R-7 Source / IP fidelity:** NASA STI source-use basis, third-party exclusion, no endorsement, the NIST reference.

## 15. Admission blockers (before any method admission)

- **A-1** Owner acceptance of this contract after the §14 review — CLOSED 2026-10-07 (the Owner acceptance above). Method
  admission stays blocked by A-2 to A-5.
- **A-2** The final method identifier — CLOSED 2026-10-07 by Owner decision: `method_id =
  "cap13:static_reactions_two_support"`, `method_version = "1.0"` (§2). Method admission stays blocked by A-3 to A-5.
- **A-3** The journey gate for the future user slice — CLOSED 2026-10-07 by §12A (accepted by Owner decision; merged in
  PR #772, merge `0acc6bca3337c2734aaecae5d3e3434841e70fd8`). Method admission stays blocked by A-4 and A-5.
- **A-4** The Arabic disclosure wording, settled under the UX review — CLOSED by §12B (accepted by Owner decision; merged in
  PR #773, merge `65f771d5f3b4820b8d2513797cd3f2d4b05c575d`). *(Superseded, preserved — was: "CLOSED by §12B (candidate
  wording; effective only on separate Owner acceptance and a verified merge). Method admission stays blocked by A-5.")*
- **A-5** A separately authorized first increment of the shared owner (A2) with this method and its named consumer,
  carrying the guard strategy of calc/units contract §14 and the CAP-13-owned governed artifact with its source and unit
  records (calc/units contract §9). That artifact must carry its OWN bounded `source_use_policy` record for NASA-S1 and
  NASA-S2 on the established `cap12:SU001` pattern; no such record exists now. — CLOSED by the delivered
  Stage 25 — CAP-13 Two-Support Static Reactions — Slice 1 (header, "A-5 FIRST IMPLEMENTATION"): the CAP-13 artifact carries
  its own bounded `cap13:SU001` source-use record for NASA-S1 and NASA-S2, and the method is admitted for that one consumer
  only.

## 16. Non-authorization (restated)

This document authorizes no implementation, runtime owner, calculation, method admission, governed artifact, schema,
store, persistence, test, route, page or user-facing behaviour; no change to the calc/units contract, the register, the
roadmap, the checklist or any Domain Pack; no Stage 25 entry, checkbox, marker or count change; no CAP-13 activation; no
numerical result; no support-capacity, strength, safety, compliance or production conclusion; and no deployment or
release.
