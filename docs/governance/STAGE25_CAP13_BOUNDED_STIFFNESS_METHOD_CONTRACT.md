# STAGE 25 / CAP-13 — BOUNDED STIFFNESS METHOD CONTRACT (ACCEPTED)

STATUS: ACCEPTED BOUNDED METHOD CONTRACT OF RECORD — DOCUMENTATION ONLY — NO IMPLEMENTATION AUTHORIZED — STAGE 25 NOT
ENTERED — CAP-13 NOT ACTIVATED.
AUTHORITY LEVEL: subordinate to the CAP-13 entry of the
[Capability Enrichment Register](INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md) and to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract"). It amends neither. Where this document and either of them differ, they win and the difference
is a defect of this document.
RECORDED: 2026-10-06, by Owner authorization of ONE documentation-only CAP-13 bounded method contract candidate.
ACCEPTANCE: 2026-10-06, by Owner decision after one non-authoring Level-1 semantic / technical review and the targeted
delta review returned B — DELTA PASS WITH NON-BLOCKING NOTES; recorded documentation-only. No technical or method clause
(§§0–14) was changed by the acceptance; references in the body to "this candidate" read as this accepted contract. D-1,
D-5 and D-7 remain OPEN, and `METHOD ADMISSION: BLOCKED UNTIL D-5 AND D-7 ARE CLOSED` stands. The review's non-blocking
notes remain future-touch / future-UX considerations and do not change the accepted contract boundary. This acceptance
does not enter Stage 25, does not activate CAP-13, does not admit the method to runtime execution, does not implement the
calculation and units owner or authorize its first increment, authorizes no numerical result, no user-facing CAP-13 slice
and no thickness recommendation, establishes no safety, strength or production suitability, and authorizes no
deployment or release. `STAGE 25: NOT ENTERED` · `STAGE 25: NOT AUTHORIZED` · `CAP-13: NOT ACTIVATED` ·
`ACTIVE CONTRACT: NONE` are unchanged.
*(Superseded 2026-10-06 by the Owner's acceptance, preserved — was: "STATUS: CONTRACT CANDIDATE — DOCUMENTATION ONLY — NOT
ACCEPTED — NO IMPLEMENTATION AUTHORIZED — STAGE 25 NOT ENTERED — CAP-13 NOT ACTIVATED."; the title read "(CANDIDATE)".)*
CONFORMING SYNC: `D-1 / CALC-OWNER CORRECTION 01 CONFORMING SYNC — CORRECTION 01 ACCEPTED BY THE OWNER 2026-10-07 — NO
IMPLEMENTATION AUTHORIZED`. Only the calc/units sequencing wording in §0, §11 and the §12 D-1 entry is synchronized with
the calc/units Correction 01, now accepted by the Owner; no technical or method clause changes, and D-1 (pending
repository reconciliation after the accepted correction is merged), D-5 and D-7 stay OPEN.
BASE: `feature/atomic-json-session-persistence` at `3a65e91642b9669bd5e80f5ac78b00b60dcdd2f6`; `ACTIVE CONTRACT: NONE`;
Stage 25 NOT ENTERED / NOT AUTHORIZED; CAP-13 NOT ACTIVATED; the Master Roadmap at 20 / 45 incomplete.
BASIS: the Lead's read-only Stage-25 reassessment (blocked on source / IP: no qualified method / material source pair); a
read-only source-qualification inquiry that could not open primary sources in its environment; the Lead's own inspection of
the official USDA primary PDFs, supplied to this candidate and recorded here as Lead-supplied; a read-only bounded design
return, accepted with two Lead corrections (F1 — source-native grain orientation; F2 — Loblolly as the one property
record). Those inputs are session-level records held in Git / GitHub and the Owner's records, not committed repository
authority.
NON-AUTHORIZATION: this document implements nothing and authorizes nothing. It creates no runtime owner, calculation, unit
conversion, adapter, governed artifact, route, page, form, schema, store, persistence, test or user-facing behaviour. It
does not implement or amend the calc/units contract, does not admit any method into it, does not enter Stage 25, does not
activate CAP-13, recommends no thickness and assigns no identifier globally.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE`. This candidate fills no active-contract slot and is not a product increment.
- `STAGE 25: NOT ENTERED` · `STAGE 25: NOT AUTHORIZED` · `CAP-13: NOT ACTIVATED`. No roadmap checkbox, marker or count
  changes.
- The calc/units contract stays unimplemented. Its Correction 01 was accepted by the Owner on 2026-10-07 and is its
  applicable wording of record: two mutually exclusive first-increment shapes, conversion-first (A1) or method-first (A2)
  (calc/units contract §3, §13). Nothing here implements the owner, authorizes a first increment or admits the CAP-13
  method.
- Stage 14 stays PARTIAL / DEFERRED; THERM-01 stays NOT AUTHORIZED; CAP-12 and CAP-14 are unchanged.
- `CALCULATION RESULT ≠ THICKNESS RECOMMENDATION ≠ SAFETY CONCLUSION`.
- `DEFORMATION CONSTRAINT SATISFIED ≠ SAFE ≠ STRUCTURALLY ADEQUATE`.
- `TECHNICAL DEEPENING SOURCE RULE: OPEN / LAWFULLY REUSABLE SOURCES ONLY` · `PUBLICLY VIEWABLE ≠ OPENLY REUSABLE`.
- `METHOD ADMISSION: BLOCKED UNTIL D-5 AND D-7 ARE CLOSED` (§12). This contract may be accepted as documentation while
  either is open; the method is then not admitted for runtime execution and no numerical CAP-13 result is shown.

## 1. Purpose and scope

CAP-13 is recorded as an optional, advisory, non-binding thickness / specification / safety capability whose numerical
output depends on the shared calculation and units owner. This candidate defines the smallest first technical method that
CAP-13 could later own: ONE stiffness / deformation method with ONE source-governed material-property record.

The v1 method produces an ESTIMATED SHORT-TERM MIDSPAN DEFLECTION ONLY. It does not solve for a thickness, does not compare
against any limit, recommends no thickness and reaches no strength, safety, compliance or production conclusion.

## 2. Method identity

- Working identity (proposed; descriptive; not globally registered): `CAP-13-STIFFNESS-WOOD-SS-MIDPOINT-V1`. The final
  identifier is fixed only by a later method-admission authorization.
- Version rule: any change to the equation, a constant, a section relation, the property record, the shear-correction
  rule, the orientation rule, the applicability conditions or the refusal semantics is a new version. A result always
  carries the version it was produced under.
- One method only. No other load case, support case, section shape, species or orientation belongs to v1.

## 3. Source records (Lead-supplied inspection)

| Record | Source identity | Author (federal) | Official record | Claims this record may support |
|---|---|---|---|---|
| S0 publication | *Wood Handbook — Wood as an Engineering Material*, General Technical Report FPL-GTR-190, USDA Forest Service, Forest Products Laboratory, 2010 (Centennial edition) | — | GovInfo `GOVPUB-A13-PURL-gpo11821`: https://www.govinfo.gov/app/details/GOVPUB-A13-PURL-gpo11821 | publication identity and government-publication status only |
| S1 method | FPL-GTR-190, Chapter 9 — "Structural analysis equations" | Douglas R. Rammer, Research General Engineer, USDA FPL | Treesearch: https://research.fs.usda.gov/treesearch/37423 | Equation 9-2 (straight-beam deflection); the Table 9-1 row for a concentrated load at midspan with both ends simply supported, midspan deflection (`kb = 1/48`, `ks = 1/4`); the rectangular-section relations `I = b·h³/12` and `A′ = 5·b·h/6`; the source-native orientation statements for `G` (§6); the linkage of `E` and `G` to Chapter 5; the statement that material variability must be considered |
| S2 property | FPL-GTR-190, Chapter 5 — "Mechanical properties of wood" | David E. Kretschmann, Research General Engineer, USDA FPL | Treesearch: https://research.fs.usda.gov/treesearch/37427 | the Table 5-3a `Loblolly` row at 12% moisture (bending modulus of elasticity `12,300 MPa`); the Table 5-1 `Loblolly` row (`GLR / EL = 0.082`; `GLT / EL = 0.081`); the statement that tabulated bending `EL` includes a shear-deflection effect and may be increased by approximately 10% to remove it; the Table 5-6 representative coefficient of variation of approximately 22% for clear-wood bending modulus of elasticity; the clear, straight-grained source-property basis |

**Inspection basis.** Every value and statement above was supplied by the Lead's own inspection of the official USDA
primary PDFs and is recorded as Lead-supplied, following the CAP-12 precedent (its governed artifact records sources "as
verified by the Lead" / "as inspected by the Lead"). It was reported to the drafting session on 2026-10-06. The exact
inspection date and page / table markers for each claim must be added to the record before any admission (§12, D-5).

**Source-use basis (not a legal opinion).** Both chapters are works of federal employees made in their official duties at
the USDA Forest Service Forest Products Laboratory; GovInfo records the handbook as a USDA Forest Service government
publication; USDA Forest Service publishing guidance treats such works as public-domain works; and 17 U.S.C. §105 makes
copyright protection unavailable for works of the United States Government (all Lead-supplied). The basis is authorship and
statute, not public accessibility, so `OPEN / LAWFULLY REUSABLE SOURCES ONLY` is met and `PUBLICLY VIEWABLE ≠ OPENLY
REUSABLE` is preserved.

**What may be used.** Only federal-authored factual and method content bound to the claims above: the equation structure,
the two constants, the two section relations, the orientation statements, the named property values and ratios, the
shear-correction statement and the variability statement, each recorded as a factual paraphrase with its source location.

**Excluded unless separately qualified.** ASTM text (including the test standards the USDA work reports its procedures were
based on — that report creates no dependency on, and no licence to, the ASTM text); NDS / AWC text and design values;
any figure, photograph or table in either chapter credited to a third party; vendor data; and any other external
copyrighted handbook material. A credited third-party item inside a source chapter is excluded even though the chapter is
federal work. Before admission, the specific Table 9-1, 5-1, 5-3a and 5-6 entries used must be confirmed free of a
third-party credit (§12, D-5).

## 4. Method definition

**Source-structured equation (S1, Equation 9-2):**

`Δ = kb · W · L³ / (E · I) + ks · W · L / (G · A′)`

**Constants for the one admitted case (S1, Table 9-1 — concentrated load at midspan, both ends simply supported, midspan
deflection):** `kb = 1/48` · `ks = 1/4`.

**Section relations (S1, rectangular section):** `I = b · h³ / 12` · `A′ = 5 · b · h / 6`.

**Symbols.** `W` — the single concentrated load at midspan; `L` — the span between the two simple supports; `b` and `h` —
the breadth and the depth of the rectangular section, with `h` the dimension in the plane of loading, exactly as Chapter 9
defines them (to be confirmed against S1 at admission, R-1); `E` and `G` — §5.

**Units (v1).** `W` in N; `L`, `b`, `h` and `Δ` in mm; `E` and `G` in MPa (N/mm²). Dimensional check: `W·L³ / (E·I)` →
N·mm³ / (N/mm² · mm⁴) = mm; `W·L / (G·A′)` → N·mm / (N/mm² · mm²) = mm.

**Executed form.** A future admitted method executes the source-structured equation together with the section relations
and the §5 derivations. The expanded form `Δ = W·L³ / (4·E·b·h³) + 3·W·L / (10·G·b·h)` is an algebraic substitution made
in drafting, recorded only as an independent cross-check for a future test oracle; it carries no separate method
authority.

**Output.** `Δ` — the estimated short-term elastic midspan deflection, in mm, under the declared inputs and conditions.
No inversion: `h` is never solved for in v1 (deferred; §11).

## 5. The one material-property record

- **Species row identity:** `Loblolly` — the exact row label in BOTH S2 Table 5-1 and S2 Table 5-3a. The consumer token
  `LOBLOLLY_PINE` maps to that row and to nothing else.
- **Source property basis:** clear, straight-grained wood; source moisture condition approximately 12%.
- **Tabulated bending modulus:** `E_tab = 12,300 MPa` (S2 Table 5-3a, 12% moisture).
- **Shear-correction rule (S2):** tabulated bending `EL` includes a shear-deflection effect and may be increased by
  approximately 10% to remove it. The method uses the corrected modulus `E = E_tab × (1 + c)`, with the source-stated
  `c` of approximately 0.10, so that it does not intentionally combine an apparent bending modulus containing test shear
  effects with Equation 9-2's separate explicit shear term. Because the source correction is approximate, no exact
  cancellation of shear influence is claimed. That pairing of the Chapter-5 correction with the Chapter-9 shear term is
  this contract's interpretation (review item R-2; D-5 items 3 and 5). `E` is derived deterministically at execution
  from the record; no rounded derived value is stored or stated as source truth, and the correction is disclosed as
  approximate.
- **Shear modulus (orientation `EDGE_GRAINED_VERTICAL_FACES` only):** `G = (GLR / EL) × E = 0.082 × E`. Whether the
  Table 5-1 ratio is to be applied to the corrected `E` is review item R-2 and stays open under D-5 item 4.
- **Not admitted in v1:** `GLT / EL = 0.081` is present in the same S2 Table 5-1 row and is recorded here only to show the
  row identity; v1 does not use it (§6).
- **Variability (S2 Table 5-6):** a representative coefficient of variation of approximately 22% for clear-wood bending
  modulus of elasticity — disclosure only (§8).

No other species, grade, condition or property belongs to the v1 record.

## 6. Source-native orientation rule (Lead correction F1)

S1 Chapter 9 states the orientation rule directly: **flat-grained vertical faces → `G = GLT`**; **edge-grained vertical
faces → `G = GLR`**. This contract preserves those source-native terms. It does not translate them into any other
woodworking vocabulary; any such mapping would need its own source qualification.

v1 admits exactly ONE orientation: `EDGE_GRAINED_VERTICAL_FACES`, therefore `G = GLR`. The consumer must declare it
explicitly. `FLAT_GRAINED_VERTICAL_FACES`, any other value or no declaration is a refusal (`ORIENTATION_NOT_SUPPORTED` or
`NOT_DECLARED`). The orientation is never inferred, defaulted or switched.

## 7. Applicability conditions and inputs

Every condition is a closed declaration made by the inventor through the consumer. None is inferred, prefilled or
defaulted. A missing or different answer refuses (§9).

| Declaration | The only accepted value in v1 |
|---|---|
| member | straight |
| section | solid, constant rectangular cross-section — no notch, hole, taper, lamination or composite |
| grain | longitudinal grain parallel to the member axis |
| support | both ends simply supported |
| load | one concentrated load at midspan |
| load character | static and short-term — not sustained, long-term, cyclic, dynamic or impact |
| orientation | `EDGE_GRAINED_VERTICAL_FACES` |
| species | `LOBLOLLY_PINE` (S2 row `Loblolly`) |
| material condition | clear, straight-grained (the source-property basis) |
| moisture condition | approximately 12% (the source condition) |
| environment | no elevated-temperature use; no outdoor, wet or unusual-moisture use; no ultraviolet, chemical or corrosive exposure; no environmental aging outside the source condition; no other unusual environmental or temperature exposure |
| high-risk screen | all nine items answered (§9) |

Elastic behaviour is an assumption of the method, disclosed and not verified: no strength check is made, so the member may
yield or fail before the estimated deflection is reached. No numeric temperature range is encoded; elevated-temperature
use and unusual exposure are abstentions only.

**Numeric inputs (v1):** `W` (N), `L` (mm), `b` (mm), `h` (mm) — scalar, finite, strictly positive, typed numbers. No
deflection limit is taken in v1. No unit other than N and mm is accepted in v1.

**Method regime (open — D-7).** Unconstrained inputs can produce a numerical result outside the regime in which this
simplified model should be trusted. This contract sets no numeric regime criterion: no deflection-to-span ratio,
slenderness ratio, span-to-depth limit, load limit or safety factor is defined here, and none may be substituted. The
criterion must come from source authority under D-7 (§12) before the method may be admitted.

## 8. Output, result states and fixed disclosure

- **Calculated:** `Δ` in mm, with its provenance: method identity and version, source records S0–S2, the property record,
  the echoed inputs, and the `E` and `G` actually derived. The result is `UNVALIDATED`, is not evidence, and persists
  nothing.
- **No recommendation level for a thickness.** v1 recommends no thickness, so it assigns neither `CONCEPTUAL` nor
  `PROTOTYPE-SUITABLE`. It reuses the register's `UNABLE TO RECOMMEND` (refusal) and `ENGINEERING REVIEW REQUIRED`
  (high-risk abstention) wording.
- **No comparison in v1.** v1 emits no `DEFORMATION CONSTRAINT SATISFIED` / `NOT SATISFIED` state. If a later,
  separately authorized user-facing slice compares `Δ` with an Owner-stated deformation limit, the token meaning is fixed
  now: it means only that the estimate is within the stated limit at source-governed average clear-wood stiffness — never
  `SAFE` or `STRUCTURALLY ADEQUATE`.
- **Calc-owner mapping.** A future executing owner reports `SUCCESS` / `UNABLE_TO_DETERMINE` / `FAILURE` / `REFUSAL`
  exactly as the calc/units contract §7 and §11 define; this contract adds no status value.

**Fixed disclosure (English; the Arabic wording is settled under the UX review before any display):**

> This is a model estimate of short-term elastic deflection at midspan for the inputs and conditions you declared, using
> the average stiffness of clear, straight-grained Loblolly pine from the USDA Forest Products Laboratory *Wood Handbook*
> (2010). It is preliminary and advisory, not a final engineering or manufacturing specification. It is not a thickness
> recommendation. Do not rely on this estimate, or on any thickness or section you choose with its help, before
> verifying loads, supports, stress, deformation, joints, fatigue, impact, and safety factor. It is not a strength,
> safety, buckling, fatigue, impact, connection, code-compliance, production-suitability or certification result. No
> strength check was made: the member may yield or fail before this deflection is reached. The model does not include
> the member's own weight (it could enter only as a separately source-qualified load case), bearing or local
> indentation at the supports or at the load point, support compliance or flexibility, connection deformation, or local
> stress effects; these are outside this estimate, and they are not claimed to be negligible. The source values are
> averages for clear wood; stiffness varies (about 22% coefficient of variation in the source), and real stock can
> differ materially.

**Register warning categories.** The disclosure carries the CAP-13 register's *General* and *Structural* mandatory
warning meanings, adapted only in grammar because v1 proposes no thickness. The register's other mandatory warning
categories — *Electrical and battery*, *Heat and pressure*, *Medical, food-contact, or human-contact*, and *Children and
consumer safety* — remain binding whenever applicable. Where v1's §9 high-risk screen covers the class concerned
(battery containment, pressure, high temperature, medical use, food contact, use by or for children), v1 abstains before
any calculation; none of these categories is turned into a calculation. *Chemical and outdoor exposure* — corrosion,
ultraviolet exposure, moisture, chemical compatibility, aging, sealing and environmental degradation require
verification. For v1, outdoor, wet or unusual-moisture use, ultraviolet exposure, chemical or corrosive exposure and
environmental aging outside the source-governed condition are out of scope: v1 abstains through the existing
environment and moisture declarations (§7), with the existing refusal reasons `ENVIRONMENT_EXCLUDED` or
`MOISTURE_CONDITION_NOT_SUPPORTED` (§9). None of them is calculated, no threshold is introduced and no environmental
suitability is implied.

**Variability treatment.** Disclosure only: no percentile, interval, safety factor, margin or probability; no adjustment
to `E`; no uncertainty propagated inside the calculation owner. Any treatment beyond disclosure needs separate method
authority.

## 9. Refusal, abstention and high-risk boundaries

**Refusal (`UNABLE TO RECOMMEND`) — proposed closed reason tokens:** `NOT_DECLARED` (any required declaration missing) ·
`SPECIES_NOT_SUPPORTED` · `ORIENTATION_NOT_SUPPORTED` · `SUPPORT_NOT_SUPPORTED` · `LOAD_NOT_SUPPORTED` ·
`SECTION_NOT_SUPPORTED` · `MATERIAL_CONDITION_NOT_SUPPORTED` · `MOISTURE_CONDITION_NOT_SUPPORTED` ·
`ENVIRONMENT_EXCLUDED` · `INVALID_NUMERIC_INPUT` (non-numeric, boolean, NaN, infinite, zero or negative) ·
`UNIT_NOT_SUPPORTED` · `KNOWLEDGE_UNAVAILABLE` (a governed record missing, malformed or failing its integrity check). A
refusal carries one reason and no numerical payload. Nothing falls back to generic advice.

**High-risk screen (`ENGINEERING REVIEW REQUIRED`).** Nine closed yes / no items, each answered explicitly: supports people;
overhead or falling hazard; use by or for children; safety-critical load path; pressure; high temperature; battery
containment; medical use; food contact. Any unanswered item refuses (`NOT_DECLARED`). Any YES abstains: no calculation is
shown and specialist engineering review is named. All NO never implies safe; it only allows the stiffness estimate under
§8's disclosure.

## 10. Numeric-capture seam and ownership

- **Capture seam (defined, not built).** A CAP-13-owned, request-local, session-only form, on the CAP-12 pattern: typed
  numeric fields in N and mm, closed declaration controls, a strict decimal grammar, no free-text parsing, no locale
  guessing and no units inside text. Nothing is persisted or logged; there is no ledger, report, PDF, Structured Export,
  API, evidence, readiness or progression effect. `engine/requirement_quantity.py` is neither read nor written, and its
  value text is never parsed.
- **No durable component model.** One member is described per request, as CAP-12 describes one component per request. A
  durable component owner is not needed for v1 and is not created.
- **CAP-13 owns** the method authority (through this contract once accepted), the applicability conditions, the USDA
  property record (in a future CAP-13-owned governed artifact — not a Domain Pack, not in
  `domains/domain_provenance.json`), the disclosures and the refusal / abstention semantics.
- **The calculation owner** (future; calc/units contract) owns the execution envelope only: it receives typed numeric
  values with their provenance and the method identity, executes the admitted method, persists nothing, and owns no wood,
  species or material truth. It never reads project, session, store, ledger or requirement-quantity data.
- **Not created, now or later, by this method:** a formula registry framework, a generic structural solver, a materials
  database or a general engineering calculator.

## 11. Calculation / units sequencing (calc/units contract with accepted Correction 01)

Under the calc/units contract's text of record before Correction 01, its first increment could admit only ONE unit
conversion and had to have a genuine named consumer (§3, §13), so the CAP-13 deflection method could never be part of that
first increment. The calc/units Correction 01, accepted by the Owner on 2026-10-07, lets a separately authorized first
increment select exactly one of two mutually exclusive shapes: A1 conversion-first or A2 method-first.

- **CASE A — a later authorized CAP-13 user slice genuinely supports inch input.** Then `in → mm` (with its own NIST SP 811
  inspection record; the repository's `mechanical:PR009` / `mechanical:PR011` records are context only) is a real
  named-consumer requirement, and a conversion-first first increment (A1) may become eligible if separately authorized.
- **CASE B — the authorized first CAP-13 slice is metric-only (as v1 here is: N and mm).** Then the metric-only method has
  no genuine conversion need: a unit-conversion first increment is NOT justified by CAP-13, and inch input is never added
  merely to create such a need. With Correction 01 now accepted, CASE B could use the method-first shape (A2) instead, if
  separately authorized — this one method as the one admitted method and the first CAP-13 user slice as the one named consumer — without
  inventing a conversion.

**Consequence recorded truthfully (Owner decision D-1).** Under the text of record before Correction 01 and CASE B there
was no calculation owner on which the v1 method could be admitted, because the owner's first increment could only be a
conversion and none is genuinely needed. The v1 method could then reach execution only through (i) a genuine CASE-A need
decided on product grounds, (ii) another genuine consumer of a first conversion increment, or (iii) a separately decided
change to the calc/units contract, which that contract's §16 routes through one Level-1 semantic review. Correction 01 is
that route (iii); it has been reviewed and accepted by the Owner (2026-10-07). The Owner acceptance satisfies the decision
condition for D-1, but D-1 stays OPEN pending repository reconciliation after the accepted Correction 01 is merged; the
shared owner is NOT implemented, no first increment is authorized, the CAP-13 method is NOT admitted (method admission
stays blocked until D-5 and D-7 are closed), Stage 25 is NOT entered and CAP-13 is NOT activated.

**Method-first envelope this method would bring under the accepted Correction 01 (sequencing statement only; the method
itself is unchanged).** Roles, each bound to one quantity kind and one exact unit token:

- user numeric capture (§7, §10): `W` — force — `N`; `L`, `b`, `h` — length — `mm`;
- method-derived (§5): `E`, `G` — elastic modulus — `MPa`, derived by this method from its CAP-13-owned, source-governed
  property record and its accepted deterministic derivations; they are never user numeric inputs;
- output (§4, §8): `Δ` — length — `mm`.

`N/mm²` dimensional equivalence does not make it an admitted alias of `MPa`. The shared owner would validate exact role →
quantity kind → unit token consistency only; the equation's dimensional derivation (§4) stays with this method authority.

**Later method admission (described, not authorized).** After a calculation owner exists, and only once D-5 and D-7
are closed (§12), a separate increment may admit this ONE closed method record and pair it with the first CAP-13 user
slice — the point at which Stage 25 would be
entered. It would execute the source-structured equation with the section relations and the §5 derivations, over the
quantity kinds force (N), length (mm) and modulus (MPa); carry the guard strategy of calc/units contract §14 in full
(among it: independent expected numerical results — the §4 cross-check form may serve as one; invalid-value and
out-of-scope rejection; failure on a tampered method, source or version record; no mutation; no network or model
fallback; no numerical payload on refusal); keep results `UNVALIDATED`; and take a UX / behaviour review before calculated
values are first displayed (calc/units contract §16). Inversion for `h` stays excluded until separately qualified and
admitted.

## 12. Review items and open Owner decisions

**Non-authoring Level-1 semantic / technical review (required before acceptance).**

- **R-1 Source fidelity:** Equation 9-2, the Table 9-1 row and its constants, and the symbol definitions of `W`, `L`, `b`
  and `h` against S1.
- **R-2 `E` / `G` semantics:** applying the Chapter-5 shear correction because Equation 9-2 carries its own shear term
  (no double counting), and whether the Table 5-1 ratio applies to the shear-corrected `E`.
- **R-3 Orientation:** the S1 statements (flat-grained vertical faces → `GLT`; edge-grained vertical faces → `GLR`)
  preserved exactly, with v1 limited to `EDGE_GRAINED_VERTICAL_FACES`.
- **R-4 Record identity:** the `Loblolly` row identity in S2 Tables 5-1 and 5-3a, the 12% moisture condition and the
  clear-wood basis.
- **R-5 Dimensional correctness** of §4.
- **R-6 Applicability and refusal completeness** of §7 and §9.
- **R-7 Safety boundary** wording of §0 and §8.
- **R-8 Calculation-owner separation and the CASE A / CASE B sequencing** of §10 and §11.
- **R-9 Source / IP fidelity**, including the third-party-credit status of the specific table entries used.

**Open Owner decisions and pre-admission blockers before any implementation.**

- **D-1** Calculation-owner sequencing (§11) — OPEN, pending repository reconciliation. The calc/units Correction 01 is the
  resolution path and the Owner accepted it on 2026-10-07; D-1 is reconciled only after the accepted correction is merged.
- **D-2** The journey gate for the future user slice (for example, CAP-12's durable mechanical root-domain gate).
- **D-3** The final method identifier.
- **D-4** Whether a later user slice compares `Δ` with an Owner-stated deformation limit.
- **D-5** Completion of the inspection record — OPEN. Before method admission it must verify and record, without closing
  any item by assumption: (1) the exact page / table location of every admitted value and statement, with the
  inspection date; (2) the third-party-credit status of each entry used; (3) the Chapter-5 wording that defines the
  relevant `EL` basis; (4) whether the Table 5-1 `GLR / EL` ratio is intended against the corrected, shear-free `EL` this
  contract uses; (5) whether Chapter 9 prescribes or constrains which `E` is used in Equation 9-2; (6) the unit-source
  inspection records that the calc/units contract requires for the admitted quantities and units (N, mm, MPa), if and
  when method admission is later authorized.
- **D-6** The Arabic disclosure wording, settled under the UX review.
- **D-7 — METHOD-REGIME QUALIFICATION** — OPEN. Before this method may ever be admitted to the calculation owner, a
  technically authoritative and lawfully reusable source must establish the applicability / validity criterion needed
  to reject inputs outside the method's bounded regime. D-7 determines, from source authority only: whether the
  governing issue is small-deflection validity, short / deep-member applicability or another source-defined regime
  condition; and the exact machine-checkable criterion, if one exists. Until D-7 is closed, this contract may be accepted
  as documentation, the method must not be admitted for runtime execution, no numerical CAP-13 result may be shown, and
  no arbitrary threshold may be substituted.

`METHOD ADMISSION: BLOCKED UNTIL D-5 AND D-7 ARE CLOSED.`

## 13. Duplication check

| Existing owner | Relationship |
|---|---|
| Mechanical Domain Pack | holds reference fundamentals only and performs no project calculation; untouched |
| CAP-12 | recommends materials for a form mock-up; CAP-13 v1 recommends no material — the species is declared and every other species refuses |
| CAP-14 | no image or drawing input; dimensions are typed |
| THERM-01 | no thermal content; elevated temperature abstains |
| Technical Realization | never calculates; it may only project an attributed result later |
| CAP-09 / WS-PFV-001 | physical validation and test planning stay theirs; CAP-13 v1 may point to them only |
| SafetySignal | separate; the high-risk screen is declared and neither reads nor feeds SafetySignal |
| Stage-15 interfaces | not used |
| calc/units owner | execution envelope only; method authority and material truth stay with CAP-13 |

## 14. Non-authorization (restated)

This document authorizes no implementation, runtime owner, calculation, unit conversion, method admission, governed
artifact, schema, store, persistence, test, route, page or user-facing behaviour; no change to the calc/units contract; no
Stage 25 entry, checkbox, marker or count change; no CAP-13 activation; no thickness recommendation; no strength, safety,
compliance or production conclusion; no source ingestion beyond the bounded factual records named in §3; and no deployment
or release.
