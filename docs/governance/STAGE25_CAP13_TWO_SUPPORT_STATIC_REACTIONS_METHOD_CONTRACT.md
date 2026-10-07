# STAGE 25 / CAP-13 — TWO-SUPPORT STATIC REACTIONS METHOD CONTRACT (CANDIDATE)

STATUS: DOCUMENTATION-ONLY CONTRACT CANDIDATE — NOT ACCEPTED — NO IMPLEMENTATION AUTHORIZED — NO METHOD ADMISSION — NO
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
BASE: `feature/atomic-json-session-persistence` at `daca52aaab6e2ff9da7b6d6969434d81fd1595f6`.
RELATED: the [bounded stiffness method contract](STAGE25_CAP13_BOUNDED_STIFFNESS_METHOD_CONTRACT.md) stays
`ACCEPTED DOCUMENTATION-ONLY FUTURE METHOD CANDIDATE — NOT ADMITTED`, with D-1 and D-5 CLOSED and `D-7: OPEN`; nothing here
changes its technical clauses or closes or weakens its D-7.
ACCEPTANCE PATH: one non-authoring Level-1 semantic / technical review, then a separate Owner acceptance. No new governance
mechanism is created.

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

- Working identity (descriptive only; not globally registered): `CAP-13-STATIC-REACTIONS-TWO-SUPPORT-V1`. The final
  runtime / admission identifier is a later admission decision.
- Version rule: any material change to the equations, the applicability, the declarations, the numeric domain, the
  refusal or abstention semantics, the source authority or a role meaning is a new version. A result always carries the
  version it was produced under.

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

**NASA source-use basis (not a legal opinion).** The NASA STI Program "Disclaimers, Copyright Notice, and Terms and
Conditions of Use" (https://sti.nasa.gov/disclaimers/) — the source-use disposition already recorded as
`mechanical:PR010`, reused here by reference — supports, in substance: U.S. Government works are generally not protected
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
A future executing owner maps each refusal to its `REFUSAL` state (calc/units contract §7, §8); this contract adds no
owner status value.

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

**Fixed disclosure (English; the Arabic wording is settled under the UX review before any display):**

> These are the vertical support reactions required by the static equilibrium model you declared: two parallel,
> horizontal, push-only supports carrying your stated total weight through your stated centre of gravity. They are not
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

- **A-1** Owner acceptance of this contract after the §14 review.
- **A-2** The final method identifier.
- **A-3** The journey gate for the future user slice.
- **A-4** The Arabic disclosure wording, settled under the UX review.
- **A-5** A separately authorized first increment of the shared owner (A2) with this method and its named consumer,
  carrying the guard strategy of calc/units contract §14 and the CAP-13-owned governed artifact with its source and unit
  records (calc/units contract §9).

## 16. Non-authorization (restated)

This document authorizes no implementation, runtime owner, calculation, method admission, governed artifact, schema,
store, persistence, test, route, page or user-facing behaviour; no change to the calc/units contract, the register, the
roadmap, the checklist or any Domain Pack; no Stage 25 entry, checkbox, marker or count change; no CAP-13 activation; no
numerical result; no support-capacity, strength, safety, compliance or production conclusion; and no deployment or
release.
