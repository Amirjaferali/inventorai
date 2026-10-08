# STAGE 27 / THERM-01 — SINGLE-PATH CONDUCTION TEMPERATURE-DIFFERENCE METHOD CONTRACT (CANDIDATE)

STATUS: DOCUMENTATION-ONLY CONTRACT CANDIDATE — NOT ACCEPTED — NO IMPLEMENTATION AUTHORIZED — NO METHOD ADMISSION — NO
NUMERICAL RESULT AUTHORIZED. `STAGE 27: NOT ENTERED` · `STAGE 27: NOT AUTHORIZED` · `THERM-01: NOT AUTHORIZED FOR
IMPLEMENTATION` · `SHARED-OWNER SECOND ADMISSION: NOT AUTHORIZED` · `ACTIVE CONTRACT: NONE`.
AUTHORITY LEVEL: subordinate to the THERM-01 section of the
[Capability Enrichment Register](INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md) (ODR `D-THERM-01`) and to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its accepted Correction 01). It amends neither. Where this document and either of them
differ, they win and the difference is a defect of this document.
PURPOSE: this candidate is the Register's mandatory THERM-01 feasibility / contract gate for ONE bounded thermal method —
it selects the supported physics, inputs, units, uncertainty, validation and solver boundary before any implementation,
as Master Roadmap row 27 requires. It enters no Stage, admits nothing and implements nothing.
BASE: cut from `feature/atomic-json-session-persistence` at `67f113d369a9909848c6eeda23c0b21113e2f3ba`.
ACCEPTANCE PATH (not started): one non-authoring Level-1 semantic / technical review of this candidate, any bounded
corrections with a targeted delta review, then a separate Owner acceptance. No new governance mechanism is created.

---

## 0. Preserved truth (binding)

- `STAGE 27: NOT ENTERED`; the Stage 27 roadmap checkbox stays UNTICKED and the roadmap count is unchanged.
- Current InventorAI performs NO governed thermal analysis, thermal simulation or temperature / heat prediction. The
  Mechanical P9-MECH-I1 "thermal behaviour and thermal simulation NOT COVERED" declaration
  (`domains/mechanical/domain.json`) and the Electrical / Electronics `P = V × I` limitation that excludes thermal rating
  (`electronics_electrical:PR004` / `PR005` context) stay true and unchanged.
- The shared deterministic calculation / units owner (`engine/deterministic_calculation.py`) admits exactly ONE method
  today — `cap13:static_reactions_two_support` version `1.0` — with kinds `force` / `length` and tokens `N` / `mm`. Nothing
  here changes it.
- Stage 25 stays ENTERED / PARTIAL for its CAP-13 Two-Support Static Reactions Slice 1 only; `FULL CAP-13: NOT AUTHORIZED`;
  the CAP-13 method, consumer, artifacts and pinned digests are untouched by this candidate.
- CAP-13 keeps thermal *consideration* (its `high_temperature` screen item abstains); WS-PFV-001 keeps physical validation;
  `engine/safety_signal.py` keeps its cue families. Thermal *simulation* stays inside the Register §1A exclusions.

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: for ONE heat path the inventor declares on a project whose
durable root domain (`confirmed_domain`) is `electronics_electrical`, the temperature difference across that path,
`ΔT = P × Rθ`, from the inventor's own heat flow `P` in W and the inventor's own total thermal resistance `Rθ` in K/W for
exactly that path. Output: `ΔT` in K — a temperature difference only, `UNVALIDATED`, not evidence.

Locked scope: Electrical / Electronics root only; steady state; one heat path; uniform one-dimensional heat flow; one
constant area; inventor-supplied total `Rθ` for exactly that path; `P > 0`, `Rθ > 0`.

## 2. Method identity and version

- Proposed method identifier: `method_id = "therm01:conduction_temperature_difference_single_path"` — exact,
  case-sensitive, NO aliases.
- Proposed initial version: `method_version = "1.0"`, carried separately from the identifier (calc/units contract).
- Version rule (as for CAP-13): any material change to the equation, applicability, declarations, numeric domain, refusal
  or abstention semantics, source authority or a role meaning is a new `method_version`; a result always carries the
  version it was produced under.
- Recorded only. No registry, artifact or implementation exists, and the method is NOT admitted.

## 3. Method definition and derivation

**Source relation (DOE authority — per-area form only).** DOE-HDBK-1012/2-92, Module 2 (Heat Transfer), HT-02, page 9,
equation (2-6), as inspected by the Lead: a steady-state relation between heat flux through a layered path, the overall
temperature difference across it and an area-normalized (per-unit-area) thermal resistance. In InventorAI's own notation,
with `q''` the heat flux (heat flow per unit area) and `R''` the per-area thermal resistance:

`ΔT = q'' × R''`

The DOE handbook expresses this in its own (English engineering) units; InventorAI's SI presentation is a notation and
unit normalization only — no conversion factor is used, reproduced or admitted, and it is NOT claimed that DOE wrote the SI
form.

**InventorAI's own bounded derivation (NOT a DOE statement).** Under declarations D-1 to D-6 (§5) — and only under them —
the heat flow through the path is the flux over its one constant area, and the total resistance of the path is the
per-area resistance divided by that same area:

```
Qdot = q'' × A
Rθ   = R'' / A
therefore
ΔT = q'' × R'' = (Qdot / A) × R'' = Qdot × (R'' / A) = Qdot × Rθ
```

The method takes `P` as `Qdot` (the steady heat flow through the declared path):

**`ΔT = P × Rθ`**

The area `A`, the flux `q''` and the per-area resistance `R''` appear only in this derivation; none is an input, output,
role or stored value, and InventorAI performs no area normalization at execution. Outside D-1 to D-6 the total form is not
supported by the DOE relation, and the method abstains or refuses (§7).

**Execution.** One multiplication of the two typed inputs; no subtraction, no tolerance, no rounding, no clamping and no
magnitude ceiling.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact token | Source of value |
|---|---|---|---|---|
| `P` | steady heat flow through the declared path | `power` | `W` | inventor-declared numeric input |
| `Rθ` | inventor-supplied total thermal resistance of exactly the declared path | `thermal_resistance` | `K/W` | inventor-declared numeric input |
| `ΔT` | temperature difference across the declared path | `temperature_difference` | `K` | output |

No alias tokens (`°C/W`, `C/W`, `K/w`, `mW`, `kW`, `°C`, `degC` and every other spelling are refused); no other unit is
accepted; no conversion. `temperature_difference` carries no offset semantics, and no absolute `temperature` kind is
admitted. A future implementation's ASCII role identifier for `Rθ` (for example `R_theta`) is an implementation detail
fixed in the implementation contract, never a second alias of the role.

## 5. Applicability declarations

Each declaration is closed and explicit, answered by the inventor through the consumer; none is inferred, defaulted or
pre-selected. A missing answer refuses `NOT_DECLARED`; a different answer refuses `PATH_NOT_SUPPORTED` (§7).

| ID | Declaration | The only accepted value in v1 |
|---|---|---|
| D-1 | condition | steady state: `P` is constant and temperatures along the path are no longer changing |
| D-2 | heat path | ONE path: all of `P` flows through this path; no parallel path, side loss or other heat source along it |
| D-3 | heat-flow geometry | uniform one-dimensional heat flow: the same heat flow crosses every layer of the path evenly |
| D-4 | area | ONE constant area through the whole path: no spreading, constriction or change of area |
| D-5 | resistance meaning | `Rθ` is the inventor's own total thermal resistance of exactly this path (the per-area resistance of its layers divided by that one common area), and already includes every layer, interface and surface film the inventor means to cover; InventorAI does not check it |
| D-6 | resistance constancy | `Rθ` does not change with `P` or with temperature over the condition being considered |

**No general admission of datasheet resistance.** A thermal-resistance figure taken from a datasheet, rating or vendor
document is accepted ONLY as the inventor's own `Rθ` under an explicit declaration that it meets D-1 to D-6 for this exact
path. InventorAI admits no datasheet resistance in general, looks nothing up, infers nothing and does not check the
declaration; datasheet junction-to-case, junction-to-ambient or heat-sink ratings are defined under their own test
conditions and are not established by the DOE relation.

## 6. Numeric domain

- `P` and `Rθ` are finite numbers strictly greater than zero. A string, boolean, NaN, infinity, zero, negative value or any
  other non-finite or non-numeric value is `INVALID_NUMERIC_INPUT`, resolved before the shared owner is called.
- **No physical magnitude ceiling.** No upper physical bound is invented to avoid overflow, and none is part of the
  admitted engineering domain.
- **Execution integrity.** If a finite admitted pair produces an overflow or a non-finite `ΔT`, the future shared owner
  returns `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload; the consumer never rewrites it as a refusal.
- **Input text bound (non-physical).** A future consumer MAY cap each typed numeric field at a fixed character length
  (proposed: 64 characters) for abuse and resource protection only. That bound is explicitly NON-PHYSICAL, is NOT the
  admitted engineering domain and must never be described as a range of valid heat flows or resistances. Over-length text
  is `INVALID_NUMERIC_INPUT`.
- Grammar (future consumer): strict ASCII decimal, digits with an optional single fractional part, no sign, no exponent,
  no separators, no Unicode digits, no unit suffix and no normalization — the CAP-13 unsigned grammar.

## 7. Refusal and abstention semantics

Two layers, as in the CAP-13 contract (Correction 01): Layer A tokens below are THERM-01 display reasons; Layer B is the
shared owner's local states and §8 reason tokens (calc/units contract §7, §8), unchanged and authoritative. This contract
adds no owner state or token and forces no owner outcome to `REFUSAL`.

**Refusal (`UNABLE TO DETERMINE` display) — closed THERM-01 reason tokens.** Reused where exact: `NOT_DECLARED` ·
`INVALID_NUMERIC_INPUT` · `UNIT_NOT_SUPPORTED` · `KNOWLEDGE_UNAVAILABLE`. Added — exactly one method-level token:
`PATH_NOT_SUPPORTED`. Every refusal carries one reason and no numerical payload; nothing falls back to generic advice.

**Pre-owner outcomes (the owner is not called), in this fixed order:** completeness → screen → declarations → numeric.

| Condition | THERM-01 outcome |
|---|---|
| any §5 declaration or §8 screen item unanswered | `NOT_DECLARED` |
| any YES on the §8 screen | `THERMAL SPECIALIST REVIEW REQUIRED` (abstention) |
| any §5 declaration answered other than its accepted value | `PATH_NOT_SUPPORTED` |
| `P` or `Rθ` malformed, over-length, non-finite, zero or negative | `INVALID_NUMERIC_INPUT` |

**Requests that reach the owner** — the owner's state controls; THERM-01 only selects its display:

| Shared-owner local state / token (Layer B) | THERM-01 display (Layer A) |
|---|---|
| `REFUSAL` / `INVALID_NUMERIC_INPUT` | `INVALID_NUMERIC_INPUT` (defence in depth; exact state preserved internally) |
| `REFUSAL` / `UNIT_NOT_ADMITTED` or `UNKNOWN_UNIT` | `UNIT_NOT_SUPPORTED` |
| `REFUSAL` / `METHOD_NOT_REGISTERED` or `VERSION_MISMATCH` | `KNOWLEDGE_UNAVAILABLE` (exact state preserved) |
| `UNABLE_TO_DETERMINE` / `SOURCE_UNAVAILABLE` | `KNOWLEDGE_UNAVAILABLE` (exact state preserved) |
| `FAILURE` / `EXECUTION_INTEGRITY_FAILURE` | `KNOWLEDGE_UNAVAILABLE` may be displayed; no numerical payload; the owner `FAILURE` is preserved and never rewritten as `REFUSAL` |

Any owner-local outcome not mapped above fails closed with no numerical payload, its state preserved for diagnosis, with
no invented THERM-01 reason and no default mapping. A future implementation contract must not admit this consumer unless
every owner outcome reachable from its fixed request shape has a deterministic handling rule.

## 8. High-risk screen (declared; not a safety engine)

Each item is answered explicitly yes / no; none is pre-selected. Any unanswered item: `NOT_DECLARED`. Any YES:
`THERMAL SPECIALIST REVIEW REQUIRED`, with no numerical payload. The path or its heat source involves:

1. a battery or energy-storage cell;
2. mains or high voltage;
3. fire or ignition risk;
4. a surface people touch, skin contact or medical use;
5. a pressurized or sealed enclosure;
6. a safety-critical or life-supporting function;
7. aerospace or vehicle use;
8. a heat source other than steady electrical dissipation (combustion, chemical or similar);
9. cryogenic temperatures;
10. transient, pulsed or start-up loads.

All NO means only that this bounded calculation may proceed — it NEVER means safe. The screen neither reads nor feeds
SafetySignal and creates no second safety engine; CAP-13's screen is not changed or reused by reference.

## 9. Result, provenance and fixed disclosure

- **Calculated:** `ΔT` in K across the declared path only. `UNVALIDATED`; NOT evidence.
- **Provenance carried with a result:** method identity and version; the DOE source record and the InventorAI derivation
  statement; the NIST unit records once qualified (§11); the echoed inputs, declarations and screen answers.
- **Fixed disclosure requirements (EN; the Arabic wording is settled under a separate UX review before any display).** The
  disclosure must state, without weakening:
  1. this is the temperature difference across the one path the inventor declared, under the declared steady-state,
     single-path, uniform one-dimensional, constant-area conditions, using the inventor's own `P` and `Rθ`;
  2. it is NOT a component, junction, case, surface or ambient temperature and does not tell what temperature anything
     reaches;
  3. it is NOT compared with any rating, limit or margin, and says nothing about whether anything is safe, acceptable,
     suitable, compliant or reliable;
  4. it is preliminary, advisory, `UNVALIDATED` and not evidence, and must be confirmed by measurement or a thermal
     specialist before any reliance;
  5. InventorAI does not check `Rθ` or that the declarations match the real hardware, and a datasheet figure applies only
     where the real path matches the conditions it was defined under;
  6. convection, radiation, spreading, transient behaviour and every other path are outside this calculation;
  7. reference source material: U.S. DOE Fundamentals Handbook (archived; historical fundamentals reference only); the
     total-resistance form is InventorAI's own derivation.

## 10. Exclusions (binding)

- No absolute, ambient, junction, case, surface or component temperature; no °C and no offset handling.
- No rating, limit, margin, pass / fail, safety, acceptability, suitability, compliance or specification statement.
- No general admission of datasheet `Rθ`; no lookup, default or inference of `Rθ`; no material-property, conductivity,
  convection-coefficient or emissivity dataset.
- No convection or radiation modelling, transient analysis, thermal network, parallel paths, spreading resistance,
  geometry, CFD, FEA or numerical solver.
- No area, flux or per-area resistance input; no unit conversion; no alias token.
- No persistence, report, PDF, Structured Export, API, evidence, readiness, progression, gap or SafetySignal effect; no AI
  or provider call.
- No new calculation owner, registry, discovery mechanism, request-selected method or generic unit vocabulary.
- No Domain Pack, `domains/domain_provenance.json`, domain-activation, CAP-12, CAP-13, CAP-14 or WS-PFV-001 change.
- Mechanical and every other root domain stay out of scope for v1.

## 11. Source and source-use status (truthful; qualification NOT closed)

| Item | Status |
|---|---|
| DOE-HDBK-1012/2-92, *Thermodynamics, Heat Transfer, and Fluid Flow*, Vol. 2 of 3, Module 2 (Heat Transfer), HT-02 p. 9, eq. (2-6) | **LEAD-INSPECTED** (Lead-supplied; not independently re-inspected by the executor, whose egress to DOE hosts was blocked by environment policy). **Claim binding: the per-area steady-state relation `ΔT = q'' × R''` ONLY.** Still to record before admission: the official DOE URL, the exact official status and its date, the inspection date and the inspected wording location. |
| DOE status limitation | Archived DOE fundamentals handbook: historical fundamentals reference only; never a current-practice, compliance, rating or design basis. English engineering units in the source; SI presentation is InventorAI's notation normalization with no conversion factor. |
| InventorAI derivation (`Qdot = q'' × A`, `Rθ = R'' / A`, `ΔT = Qdot × Rθ`) | InventorAI's own bounded derivation under D-1 to D-6 — NOT a source claim and never attributed to DOE. |
| DOE source-use basis | **OPEN.** A THERM-01-scoped record restating the DOE Web Policies disposition on the `electronics_electrical:PR006` pattern (government information public domain with acknowledgement requested; privately contributed or contractor material may remain protected; the handbook was prepared with a DOE contractor training programme) — factual relation only, InventorAI-authored paraphrase only, no copied prose, worked examples, figures or tables, no endorsement implied. The Electrical pack record is NOT cited across domains. |
| NIST SP 330 (2019) — `K` as SI base unit (kelvin) | **LEAD-INSPECTED; NOT QUALIFIED.** Exact inspected location, URL / DOI and inspection date not yet recorded. |
| NIST SP 330 (2019) — `W` as SI derived unit (watt) | **LEAD-INSPECTED; NOT QUALIFIED.** Exact location not yet recorded. (`W` is already identified for Electrical reference use in `electronics_electrical:PR005` from NIST SP 811 Appendix B.9; that pack-scoped record is not an owner unit record.) |
| NIST SP 330 (2019) — `K/W` as a quotient of SI units | **LEAD-INSPECTED; NOT QUALIFIED.** The exact clause on forming derived units by products / quotients is not yet recorded. |
| NIST SP 330 (2019) — a temperature difference expressed in kelvin | **LEAD-INSPECTED; NOT QUALIFIED.** Exact location not yet recorded. |
| NIST source-use basis for SP 330 | **OPEN.** `dcu:SU001` was inspected for the owner's SP 811 unit identification; whether the same NIST Technical Series basis covers SP 330 must be confirmed and recorded (extend or add a record). |
| SP 811 / SP 330 reconciliation | **OPEN.** The owner's `dcu:U001` / `dcu:U002` cite SP 811 (2008); whether the new unit records cite SP 330 while those stay on SP 811 is an owner-artifact decision (§12, AD-6). |
| Any second source for a general lumped "total thermal resistance" | Not sought and not needed: the method does not admit general datasheet resistance. |

No source fact above is marked qualified. **Source qualification must be CLOSED — every row recorded with its exact
location, URL, date, inspection basis and use basis — before any runtime admission.**

## 12. Architecture decision record (reviewed future implementation boundary; NOT implemented here)

| ID | Decision of record |
|---|---|
| AD-1 | Existing shared deterministic owner only (`engine/deterministic_calculation.py`). No new calculation owner, solver, registry or discovery. |
| AD-2 | A second immutable `MethodBinding`, created by application wiring, for this one method and its one consumer. No request-selected method; each consumer holds exactly its own binding. |
| AD-3 | After a future implementation the owner admits EXACTLY two methods: `cap13:static_reactions_two_support` 1.0 and `therm01:conduction_temperature_difference_single_path` 1.0. The admitted sets stay closed code constants; each method's roles stay bound to its own kinds and tokens, and one method's tokens can never satisfy another's roles. |
| AD-4 | Added quantity kinds: `power`, `thermal_resistance`, `temperature_difference` (no absolute `temperature` kind). |
| AD-5 | Added exact unit tokens: `W`, `K/W`, `K`. No aliases, no dimensional equivalence, no conversion. |
| AD-6 | Owner artifact `docs/governance/deterministic_calculation_config/deterministic_calculation_owner_v1.json` content version moves to future `2`, adding the THERM-01 method record, kinds, unit records and an owner-local source-qualification snapshot (the `dcu:SU002` pattern); the SP 811 / SP 330 citation choice is settled there. |
| AD-7 | Owner implementation version moves to future `1.1.0`. |
| AD-8 | CAP-13 method and artifact semantics stay unchanged: its method record, roles, tokens, pinned digests, behaviour and tests stay identical. |
| AD-9 | A separate THERM-01 method-authority artifact (proposed: `docs/governance/therm01_content_config/conduction_temperature_difference_single_path_v1.json`) holds the method authority, declarations, screen, numeric domain, disclosure and THERM-01 source / source-use records. Not a Domain Pack; not in `domains/domain_provenance.json`. Neither artifact loads the other at execution. |
| AD-10 | Consumers stay separate: a THERM-01 consumer module and request-local page, gated on the durable `confirmed_domain == "electronics_electrical"` read the same way the CAP-12 / CAP-13 gates read it. THERM-01 never imports CAP-13 and CAP-13 never imports THERM-01. |
| AD-11 | No registry, discovery, conversion, generic unit vocabulary or request-selected method, ever, under this contract. |

AD-3, AD-4, AD-5 and AD-7 change the shared owner beyond the calc/units contract §13 first increment (which excludes "a
second method; a second consumer"): they require a separately accepted shared-owner contract amendment before any
implementation.

## 13. Future focused tests (for a separately authorized implementation; none is written now)

- **Owner:** exactly two admitted methods; closed kind and token sets equal exactly the two methods' needs; the THERM-01
  binding cannot execute the CAP-13 method and vice versa; `K/W` exact (aliases refused); no `temperature` or `°C` kind;
  bool / NaN / infinity refused; overflow and non-finite results → `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no payload.
- **Method:** worked values of `ΔT = P × Rθ`; `P ≤ 0` and `Rθ ≤ 0` refused before the owner; no ceiling applied.
- **Consumer:** strict grammar matrix including the non-physical length cap; every declaration and screen item explicit
  and never pre-selected; the fixed pre-owner order; one reason per non-success; owner FAILURE never remapped to REFUSAL;
  unmapped owner outcomes fail closed.
- **Gating:** Electrical / Electronics root only; Mechanical and other roots refused; ownership isolation and CSRF.
- **Artifacts:** both artifacts validated with pinned digests; tampering, version mismatch or a missing source / source-use
  record fails closed; CAP-13 digests and behaviour unchanged.
- **No side effects:** nothing persisted (database dump and session snapshot); no report, PDF, export, evidence, readiness
  or SafetySignal effect; import isolation (no network, clock, randomness or provider).
- **Wording and layout:** EN disclosure equals §9 meanings; AR from its accepted UX section; RTL `bdi` isolation of
  numbers, `W`, `K/W`, `K` and `ΔT`; a real-browser check at phone width.
- **Guards:** domain thermal-exclusion declarations unchanged; the Mechanical safety-cue family still free of thermal
  vocabulary; navigation guards accept only the exact scoped wording of any future Stage-27 entry.

## 14. STOP conditions

Stop and return to the Lead / Owner if any of these arises:

- a need for CFD, FEA, a numerical solver, geometry, convection, radiation, transient behaviour, a network or parallel
  paths;
- absolute temperature, °C or offset handling, or any rating, margin, safety or suitability output;
- a material-property or coefficient dataset, or general datasheet-resistance admission;
- a source fact that cannot be inspected and bound with a compatible use basis;
- a second calculation framework, a THERM-01-owned calculation owner, a registry or a request-selected method;
- any change to CAP-13 behaviour, artifacts or digests;
- thermal output routed into SafetySignal, evidence, readiness, progression, report or export;
- any AI or provider call;
- any implementation step before every open blocker in §15 is closed.

## 15. Open blockers (before any method admission)

1. **Acceptance of this contract** — `OPEN`: Level-1 review, any bounded corrections and the Owner acceptance.
2. **Source qualification closed** — `OPEN`: every §11 row recorded with exact location, URL, date, inspection basis and
   use basis (DOE record, DOE source-use record, NIST SP 330 unit facts for `K`, `W`, `K/W` and temperature difference, the
   NIST use basis for SP 330, and the SP 811 / SP 330 reconciliation).
3. **Shared-owner contract amendment accepted** — `OPEN`: a calc/units contract amendment admitting a second method and a
   second consumer under AD-1 to AD-11, with architecture review of AD-2 to AD-7 and AD-10.
4. **Arabic wording and UX** — `OPEN`: Arabic disclosure and journey wording settled before any display.
5. **Separate Owner implementation authorization** — `OPEN`.

`SHARED-OWNER SECOND ADMISSION: NOT AUTHORIZED` until blockers 1, 2, 3 and 5 are all closed.

## 16. Non-authorization (restated)

This candidate is documentation only. It implements nothing, admits no method, authorizes no numerical result or
user-facing thermal behaviour, changes no runtime, artifact, schema, persistence, Domain Pack, test or navigation surface,
enters no Stage (`STAGE 27: NOT ENTERED`) and activates nothing. Deployment, public release and paid activation stay NOT
AUTHORIZED.
