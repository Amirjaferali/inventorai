# STAGE 27 / THERM-01 — SINGLE-PATH CONDUCTION TEMPERATURE-DIFFERENCE METHOD CONTRACT (ACCEPTED)

STATUS: ACCEPTED DOCUMENTATION DECISION OF RECORD — NO IMPLEMENTATION AUTHORIZED — NO METHOD ADMISSION — NO NUMERICAL
RESULT AUTHORIZED. `STAGE 27: NOT ENTERED` · `STAGE 27: NOT AUTHORIZED` · `THERM-01: NOT AUTHORIZED FOR
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
MERGED: PR #775, merge `1b587da5c3555dda487be02589fa618f7a5a7cb8` (reviewed head `9c1033c435949c854b45fa3d2fc9f2c98db671cd`,
carrying the bounded AD-8 / AD-11 corrections; merge tree = reviewed-head tree).
ACCEPTANCE: by Lead / Owner decision after the merge of PR #775, this contract is the ACCEPTED DOCUMENTATION DECISION OF
RECORD for the THERM-01 method / feasibility gate. Recorded documentation-only: the technical method, sources, scope,
declarations, screen, exclusions, architecture decisions and blockers are unchanged by the acceptance, and references in
the body to "this candidate" read as this accepted contract. The acceptance closes §15 blocker 1 only; blockers 2, 3, 4
and 5 stay OPEN. It implements nothing, admits no method, closes no source qualification, enters no Stage and authorizes
no THERM-01 runtime or shared-owner second admission.
*(Superseded by this acceptance, preserved — was: "STATUS: DOCUMENTATION-ONLY CONTRACT CANDIDATE — NOT ACCEPTED — …" and
"ACCEPTANCE PATH (not started): one non-authoring Level-1 semantic / technical review of this candidate, any bounded
corrections with a targeted delta review, then a separate Owner acceptance. No new governance mechanism is created.")*

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

## 11. Source and source-use status (truthful; qualification CLOSED for the recorded claims only)

**Inspection basis.** Two Lead inspections, recorded with their own dates and never backdated:

- **Inspection A (supplied 2026-10-08).** DOE-HDBK-1012/2-92 HT-02 p. 9 eq. (2-6), NIST SP 330 (2019) Section 2 and the
  NIST Technical Series source-use policy were inspected by the Lead and supplied to the executor with their URLs and
  inspected locations on 2026-10-08 (base `0a519210d523cd118153792dc64c82271f3d9ddf`). No earlier or more precise
  inspection date was stated, and none is claimed: these rows carry the supply date 2026-10-08.
- **Inspection B (2026-10-09).** The Lead independently verified the DOE Web Policies page and the official
  DOE-HDBK-1012/2-92 record on 2026-10-09.

The executor did not independently re-inspect any reference: its egress to `energy.gov` and `nist.gov` was refused by the
environment network policy. No row below rests on model memory.

**Sources and supported claims.**

| ID | Source and inspected location | Exact supported claim (InventorAI's own factual paraphrase) | Status |
|---|---|---|---|
| THERM-S1 | U.S. Department of Energy, DOE-HDBK-1012/2-92, *DOE Fundamentals Handbook: Thermodynamics, Heat Transfer, and Fluid Flow*, Volume 2 of 3, Module 2 (Heat Transfer), HT-02, page 9, equation (2-6). URL: https://www.energy.gov/documents/doe-hdbk-1012-92vol2 | For steady-state heat transfer through a layered path, the heat flux equals the overall temperature difference divided by the area-normalized (per-unit-area) thermal resistance of the path; written by InventorAI as `ΔT = q'' × R''`. Bound to this per-area relation ONLY. | **LEAD-INSPECTED — identity, URL, location and claim RECORDED.** |
| THERM-S1 status | Official DOE record of DOE-HDBK-1012/2-92: https://www.energy.gov/ehss/articles/doe-hdbk-10122-92 (Inspection B, 2026-10-09). | Status: **Archive**. Approved: **1996-01-22**. Last updated: **2014-12-29**. These are the record's approval and last-update dates; neither is the date the handbook moved to Archive. The date of transition to Archive is **NOT established** and no cancellation or archive date is recorded or inferred. | **RECORDED (G-2 CLOSED).** |
| THERM-S1 limitation | Same source. | Archived DOE fundamentals handbook: historical fundamentals reference only; never a current-practice, compliance, rating or design basis. The source uses English engineering units; InventorAI's SI presentation is a notation normalization with no conversion factor, and it is NOT claimed that DOE wrote the SI form. | **PRESERVED.** |
| THERM-D1 | InventorAI's own derivation (§3): `Qdot = q'' × A`, `Rθ = R'' / A`, therefore `ΔT = Qdot × Rθ`, valid only under D-1 to D-6. | — | **InventorAI derivation — NOT a source claim, never attributed to DOE.** |
| THERM-U1 | NIST Special Publication 330, *The International System of Units (SI)*, 2019 edition, Section 2. URL: https://www.nist.gov/pml/special-publication-330/sp-330-section-2 | The kelvin, symbol `K`, is the SI base unit of thermodynamic temperature. | **LEAD-INSPECTED — RECORDED** (location: SP 330 Section 2, as supplied; no finer subsection reference was supplied). |
| THERM-U2 | Same, Section 2. | The watt, symbol `W`, is the SI coherent derived unit with a special name for power (one joule per second). | **LEAD-INSPECTED — RECORDED** (Section 2). |
| THERM-U3 | Same, Section 2. | Coherent SI derived units are formed as products and quotients of SI units; hence kelvin per watt, written `K/W`, is a coherent SI unit (used here for thermal resistance). `K/W` is not a named SI unit; the quantity name "thermal resistance" is InventorAI's usage. | **LEAD-INSPECTED — RECORDED** (Section 2). |
| THERM-U4 | Same, Section 2. | A temperature difference (interval) may be expressed in kelvin; a difference of one kelvin equals a difference of one degree Celsius. Used only to justify the `K` output token for a temperature difference; no Celsius scale, offset or conversion is admitted. | **LEAD-INSPECTED — RECORDED** (Section 2). |

**Source-use dispositions (not legal opinions).**

| ID | Basis | Disposition | Status |
|---|---|---|---|
| THERM-SU-NIST | NIST — *Copyright, Fair Use, and Licensing Statements for SRD, Data, Software, and Technical Series Publications*. URL: https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications | Lead-inspected (same basis as above). NIST employee-authored Technical Series publications are not subject to U.S. copyright protection; NIST acknowledgement is required; third-party material inside a NIST publication is excluded from that statement. SP 330 is a NIST Special Publication (Technical Series). THERM-01 use is limited to the four unit facts THERM-U1 to THERM-U4, stated in InventorAI's own words, with NIST acknowledgement; no SP 330 prose, table, figure or symbol list is reproduced; no endorsement is implied. SP 330 is NIST's edition of the SI as defined by the BIPM: any BIPM-originated wording or tables in it are treated as third-party material and are NOT reproduced; only the unit facts themselves are used. | **RECORDED — THERM-01-SCOPED.** This is a separate THERM-01 record on the same NIST policy page that `dcu:SU001` and `electronics_electrical:PR007` already cite; it does NOT extend the scope of either of those records, which stay bound to their own unit facts. |
| THERM-SU-DOE | DOE Web Policies. URL: https://www.energy.gov/web-policies (Inspection B, 2026-10-09). | Government information is generally in the public domain, and DOE acknowledgement is requested; third-party and contractor material may remain protected. THERM-01 disposition: the handbook was prepared with a DOE contractor training programme, so no blanket public-domain claim is made for its expressive content. Use is limited to the one factual relation THERM-S1, stated in InventorAI's own paraphrase with DOE acknowledgement; no handbook prose, worked example, figure or table is copied; no endorsement is implied. This is a separate THERM-01 record: `electronics_electrical:PR006` is NOT cited across domains and its scope is NOT extended. | **RECORDED — THERM-01-SCOPED (G-1 CLOSED).** |

**SP 811 / SP 330 reconciliation (decision of record).** The shared owner's existing unit records `dcu:U001` (`N`) and
`dcu:U002` (`mm`) and their source-use record `dcu:SU001` stay on NIST SP 811 (2008) exactly as used by CAP-13; nothing here
changes, re-cites or re-dates them. The THERM-01 unit facts `W`, `K`, `K/W` and temperature difference cite NIST SP 330
(2019) (THERM-U1 to THERM-U4). Where the future owner artifact (AD-6) records these new unit records is an implementation
detail of that separately authorized change; it may not alter the SP 811 records. **RECORDED.**

**Not sought:** any second source for a general lumped "total thermal resistance" — not needed, because the method does not
admit general datasheet resistance.

**Gap closure:**

- **G-1 — DOE source-use basis: CLOSED** by THERM-SU-DOE (Inspection B, 2026-10-09).
- **G-2 — DOE official status: CLOSED** by the THERM-S1 status row (Archive; approved 1996-01-22; last updated
  2014-12-29; archive-transition date not established and not inferred).
- **G-3 — Inspection dates: CLOSED** by the inspection-basis statement above: Inspection A carries its supply date
  2026-10-08 and Inspection B its verification date 2026-10-09; nothing is backdated.

Every source and source-use row now carries its URL, inspected location, date, inspection basis and use basis, so source
qualification is **CLOSED** for exactly the recorded claims (THERM-S1, THERM-U1 to THERM-U4) under their recorded
limitations. It qualifies nothing else, admits no method and authorizes no runtime: method admission still needs blockers 3
and 5, and any display needs blocker 4.

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
| AD-8 | CAP-13 compatibility: the CAP-13 method `cap13:static_reactions_two_support` version `1.0`, its CAP-13 authority artifact version `1`, its equations, roles, units, semantic pins (`_SEMANTIC_DIGESTS`) and user-facing behaviour stay unchanged. No CAP-13 method-semantic change is authorized. This does NOT claim that every CAP-13 test or every shared-owner identity stays byte-identical: bounded updates to assertions on the shared-owner artifact content version, the owner implementation version and the shared-owner closed-inventory / digest identities, caused only by the separately reviewed second admission (AD-3 to AD-7), are expected and allowed. |
| AD-9 | A separate THERM-01 method-authority artifact (proposed: `docs/governance/therm01_content_config/conduction_temperature_difference_single_path_v1.json`) holds the method authority, declarations, screen, numeric domain, disclosure and THERM-01 source / source-use records. Not a Domain Pack; not in `domains/domain_provenance.json`. Neither artifact loads the other at execution. |
| AD-10 | Consumers stay separate: a THERM-01 consumer module and request-local page, gated on the durable `confirmed_domain == "electronics_electrical"` read the same way the CAP-12 / CAP-13 gates read it. THERM-01 never imports CAP-13 and CAP-13 never imports THERM-01. |
| AD-11 | No registry, discovery mechanism, generic conversion, generic unit vocabulary or request-selected method is authorized by this contract or by this bounded second admission. Any future architecture beyond it stays subject to a separate decision; nothing here pre-authorizes it. |

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
  record fails closed; the CAP-13 method `1.0`, its authority artifact version `1`, its semantic pins and its behaviour
  unchanged (bounded shared-owner version / identity assertion updates allowed per AD-8).
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
- any change to CAP-13 method semantics, behaviour, its authority artifact or its semantic pins (beyond the bounded
  shared-owner assertion updates AD-8 allows);
- thermal output routed into SafetySignal, evidence, readiness, progression, report or export;
- any AI or provider call;
- any implementation step before every open blocker in §15 is closed.

## 15. Open blockers (before any method admission)

1. **Acceptance of this contract** — `CLOSED`: accepted by Lead / Owner decision as the documentation decision of record
   after PR #775 (merge `1b587da5c3555dda487be02589fa618f7a5a7cb8`).
2. **Source qualification closed** — `CLOSED`: recorded in §11 — the DOE relation THERM-S1 (identity, URL, location,
   claim binding, official Archive status and dates), the InventorAI derivation THERM-D1, the NIST SP 330 unit facts
   THERM-U1 to THERM-U4, the THERM-01-scoped source-use records THERM-SU-NIST and THERM-SU-DOE, the SP 811 / SP 330
   reconciliation and the inspection dates (2026-10-08 and 2026-10-09); G-1, G-2 and G-3 closed.
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
