# MECHANICAL — PLANAR CENTERED RECTANGULAR CLEARANCE — METHOD CONTRACT (BOARD-ENCLOSURE-PLANAR-CLEARANCE-01)

Status: Owner-authorized bounded increment BOARD-ENCLOSURE-PLANAR-CLEARANCE-01 (2026-11-01), implemented in ONE
PR with this contract. It admits ONE Mechanical geometric method through the shared deterministic calculation and
units owner (calc/units contract Correction 14, §13M), ONE narrowly typed, revisioned inventor-input declaration
under the existing Stage-15 composition owners, and ONE bounded D4 / interface-characterisation exception for this
declared nominal planar condition only. Merge, deployment, release and paid activation are NOT authorized by it.

## 1. Scope and eligibility

- A valid durable integrated Mechanical + Electrical / Electronics composition (Stage 15), ONE existing declared
  interaction of it and TWO DISTINCT current components that the inventor has said take part in that interaction
  (COMPONENT-INTERFACE-PARTICIPATION-01).
- The inventor explicitly chooses which of the two is the **board** and which is the **enclosure**. Nothing is
  inferred from names, functions or part links, and no component is classified automatically.
- Existing project authorization applies. No unrelated gap needs to close; the Project Compass, governed
  questions, progression, readiness and SafetySignal are unchanged and are not consulted.
- Identities are reused: project, subsystem, component (with its revision position) and interface identities; no
  second component inventory and no relationship graph.

## 2. Identity

Method `mechanical:planar_centered_rectangular_clearance`, version `1.0`. Method-authority artifact
`mechanical_planar_centered_rectangular_clearance`, artifact version `2`
(`docs/governance/mechanical_content_config/planar_centered_rectangular_clearance_v1.json`; version `1` sections
unchanged, version `2` adds the §3A `region_bound` section). Declaration contract
version `planar-clearance-declaration/1` (the inventor-input shape of §5 and §8). A stored declaration names the
method and declaration-contract versions it was made under; a mismatch is never silently substituted (§7). Derived
consequence `mechanical:planar_centered_rectangular_clearance/region_bound`, consequence version `1` (§3A).

## 3. Method definition and original derivation

Admitted configuration: ONE rectangular board outline; ONE selected rectangular usable region at the board plane,
unobstructed at that plane; the board placed **centered** and **axis-aligned** with the explicitly paired axes
(board X along region X, board Y along region Y). No rotation, placement search or optimization. Card-guide, rail
or slot mounting is outside the method. Features outside the selected region do not by themselves make the method
inapplicable; a feature that intrudes into the selected region does.

Derivation (InventorAI's own; elementary Euclidean geometry, independently checkable, no external text, table or
code). On one axis the region is the closed interval `[0, R]` and the centered board occupies
`[(R − B)/2, (R + B)/2]`. The free distance from each board edge to the nearer region edge is therefore
`(R − B)/2` on BOTH sides. Requiring a clear distance `c` on each side leaves the margin

    margin = (R − B) / 2 − c

The declared condition is met on that axis exactly when `margin ≥ 0`, equivalently `R ≥ B + 2c`. Applied to both
axes:

    margin_x = (region_x − board_x) / 2 − c          margin_y = (region_y − board_y) / 2 − c

The declared condition is **met** exactly when both margins are nonnegative; equality meets it. A board larger
than the region is a valid NOT MET case (a negative margin), not malformed input. A NOT MET result for the
declared placement does not show that every placement, orientation or a redesigned enclosure is impossible, and a
MET result does not show that the parts fit (§9).

## 3A. Derived consequence: minimum usable-region dimension

AMENDMENT (BOARD-ENCLOSURE-CONDITIONAL-REGION-BOUND-01, Owner-authorized 2026-11-02). The §3 equivalence
`R ≥ B + 2c` gives, per axis and holding the declared board dimension `B`, the clearance `c`, the centered,
axis-aligned placement and the applicability answers fixed:

    region_min = B + 2c          additional = max(0, region_min − R)

- **Meaning.** `region_min` is the smallest selected unobstructed INTERNAL region dimension at the board plane that
  meets the declared nominal condition on that axis; it is not an enclosure outer dimension, a selected component, a
  manufacturing dimension or a verified requirement. Equality meets the nominal condition only; tolerances and
  physical fit stay unassessed. A changed physical configuration still needs declarations that describe it.
- **Per side versus total.** With the board centered, a negative per-side margin `m` means a TOTAL additional region
  dimension of `−2m` (half on each side): a margin of −1 mm means 2 mm more region, not 1 mm. An axis that already
  meets the condition shows an additional dimension of 0 and "no increase needed for this condition"; it is never
  offered as a size to reduce to.
- **Eligibility.** Derived only after the evaluation reached MET or NOT MET through every §7 gate (artifact,
  applicability, completeness, grammar, owner, bridge) and only for a current binding (§8). NEEDS RECONFIRMATION,
  INAPPLICABLE, MISSING INFORMATION, COULD NOT BE COMPUTED, UNAVAILABLE and a withdrawn declaration show no bound.
- **Numerics and ownership.** Computed by the method consumer (`engine/mechanical_planar_clearance.py`) in exact
  rational arithmetic on the entered decimals, after the shared owner's success and the bridge acceptance for that
  same request; cross-checked against the §3 margin (`region_min − R = −2 × margin` exactly; a mismatch is an
  execution-integrity failure with no verdict). It adds no owner output, no adapter change and no formula outside
  the consumer. Shown exactly (at most four fractional digits), never rounded. A `region_min` above the §6 entry
  grammar is shown exactly with an "outside this tool's current entry range" note — never truncated and never
  called physically impossible.
- **No automatic change.** The outcome, margins, sketch, stored values and revision identity are unchanged by the
  bound; nothing is prefilled, corrected, reduced, resized, rotated, searched or recommended.
- **Versioning.** The consequence is a separately pinned section of the artifact with its own version; the method
  version `1.0` and the declaration-contract version are unchanged, so no stored declaration is relabelled,
  migrated or asked to be reconfirmed because of it, and an existing method / declaration version mismatch still
  reads NEEDS RECONFIRMATION. The output names the consequence id and version; an earlier downloaded report or PDF
  is not retroactively given a bound it did not carry.
- **Language.** English and Modern Standard Arabic through the existing catalogue (§14); the English meaning lines
  are the artifact's `region_bound.statements` word for word.

## 4. Roles and units

Inputs, all `length` in the exact token `mm` (owner record `dcu:U002`, NIST SP 811; no conversion, no other
token): `board_x`, `board_y` (board outline), `region_x`, `region_y` (selected usable region), each strictly
positive; `c` (required clear distance per side, the same on all four sides), zero or positive. Outputs
`margin_x`, `margin_y` in `mm`, signed. The owner checks `greater_than_zero` on the four dimensions; `c ≥ 0` is
checked from the exact decimal before the owner and again by the adapter (integrity failure).

## 5. Inventor declaration (inputs, not results)

Each value is entered as an exact decimal, explicitly marked **unknown**, or left **not entered**; missing or
blank is never zero. Additionally:

- **Region description** (required for a comparison; at most 300 characters): where the board plane and the
  selected usable region are, so that the numbers do not float free of their geometric meaning.
- **Axis pairing**: fixed `board_x_along_region_x` — the only admitted pairing; it is stored and shown.
- **Basis notes** (optional, at most 300 characters each) for the board dimensions, the region dimensions and the
  clearance: where the inventor's value comes from (a measurement, a drawing, a design target). An absent note
  reads "basis not recorded"; a note or a URL inside it is never fetched and verifies nothing.
- **Applicability declarations**, each answered explicitly (`applies` / `does not apply`; no default):

| Id | Declaration |
|---|---|
| D-1 `rectangular_board` | The board outline is treated as one rectangle `board_x` × `board_y`. |
| D-2 `rectangular_region` | The selected usable region is one rectangle `region_x` × `region_y`, at the board plane, inside the enclosure. |
| D-3 `region_unobstructed` | Nothing intrudes into the selected region at the board plane (features outside it are allowed). |
| D-4 `centered_axis_aligned` | The board sits centered in the region, board X along region X and board Y along region Y, with no rotation. |
| D-5 `same_plane` | The board and region dimensions are taken in the same plane, the board plane. |
| D-6 `not_guide_mounted` | The board is not held by card guides, rails or slots. |
| D-7 `uniform_clearance` | `c` is the clear distance required on each of the four sides. |
| D-8 `nominal_values` | The values are nominal; tolerances are not part of this comparison. |

All values and notes are OWNER_STATED / UNVALIDATED.

## 6. Numeric domain and numerical acceptance

- **Grammar (representation policy, NOT physical ratings).** A strict unsigned ASCII decimal of one to six integer
  digits and up to four fractional digits (`[0-9]{1,6}(\.[0-9]{1,4})?`); no sign, exponent, separator, Unicode
  digit, unit suffix or normalization; no silent truncation or coercion — anything else is refused at capture and
  never stored. Dimensions must be strictly positive and `c` zero or positive, decided on the exact decimal.
- **Geometric decision on the exact entered decimals, before any display.** The consumer computes the exact
  rational margins from the entered decimals and decides MET / NOT MET from their signs (the independent form
  `region ≥ board + 2c` per axis gives the same decision). Example: `region_x = 100.1`, `board_x = 99.9`,
  `c = 0.1` gives exactly `0` — MET — although the binary path cancels to about `−5.7 × 10⁻¹⁵`.
- **Binary path (shared owner and adapter).** Each admitted decimal is converted once, correctly rounded, to
  binary64. The adapter forms the exact rational margin of the binary inputs and rounds it once (relative error at
  most `2⁻⁵³`); an exact zero returns `+0.0`.
- **Bridge acceptance (consumer).** With `u = 2⁻⁵³`, the exact decimal margin `m` and the binary result `v` must
  satisfy `|v − m| ≤ e + (|m| + e)·u`, where `e = ((R + B)/2 + c)·u` bounds the effect of the three input
  conversions (each `|fl(x) − x| ≤ |x|·u`; every admitted value is a normal binary64 number). This is an absolute /
  mixed bound derived from the inputs: no relative-to-zero test, no sign agreement near zero and no epsilon in the
  geometric decision. A violation is an execution-integrity failure: no verdict, no number.
- **Display.** The exact decimal margins have at most five fractional digits and are shown exactly — no rounding,
  so display can never change MET into NOT MET or the reverse.
- **Execution failure is not a geometric failure.** Any owner non-success or bridge violation yields no verdict.

## 7. Outcomes (scoped presentation meanings, not a validation ladder)

Order: method artifact → applicability (any `does not apply` → **INAPPLICABLE**) → completeness (any value not
entered or unknown, a missing region description or an unanswered declaration → **MISSING INFORMATION**, listing
what is missing) → grammar → shared owner → bridge → **MET** / **NOT MET** (naming each axis that falls short and
its shortfall, and — amended by §3A — the derived minimum usable-region dimension of each axis). Separately: a declaration whose bound component, participation or versions changed reads
**NEEDS RECONFIRMATION** (§8) and is not evaluated; unreadable or corrupt data reads **UNAVAILABLE**; an owner or
bridge failure reads **COULD NOT BE COMPUTED**. The shared owner's state and reason token are preserved.

## 8. Lifecycle, binding and staleness

- Owner of semantics: `engine/subsystem_model.py`; persistence: one append-only family
  `planar_clearance_revisions` in the project record store (`engine/record_store.py`).
- Each immutable revision binds: project and declaration identity; the interface; the board and enclosure
  component identities and their component revision positions; the participation removal generation of each
  (below); the axis pairing; the region description; the exact entered values or unknowns; the basis notes; the
  eight answers; the method id / version and the declaration-contract version.
- Revision 0 declares; corrections append (at most 20); ONE reserved terminal withdrawal follows any number of
  corrections. Withdrawal is not erasure. At most ONE active declaration per interface and at most 50 lifetime
  declaration identities per project (resource limits, not physical or commercial limits).
- Signed submission identity, central authorization and CSRF; inside ONE serialized write the project, the
  expected declaration head, the interface, both component revisions, both current participations and both
  generations are re-validated; stale, forged or cross-project submissions write nothing; an exact retry of a
  committed submission writes nothing and never revives a stale or withdrawn declaration.
- **Removal generation (ABA guard).** A database trigger on `subsystem_interface_components` increments a
  per-(interface, component) removal counter (`subsystem_interface_participation_epochs`) in the same transaction as
  every deletion of that participation row, whichever build issues it — so the guard also holds across a rollback to
  the pre-increment build and back. Reads fail closed (UNAVAILABLE) if the trigger is absent. A declaration records the counter value it was made against, so a participant removed and later
  re-added no longer matches: the old binding never revives. A component correction (new revision position) or
  withdrawal, or loss of participation, likewise suspends evaluation (NEEDS RECONFIRMATION) until the inventor
  explicitly rebinds through a new correction. Rendering never writes.
- Reads use ONE coherent store snapshot (composition, interfaces, component history, participation, removal
  counters and the whole declaration history); a malformed or unknown table or history reads UNAVAILABLE, never
  NOT RECORDED. The family never enters the answer stream, IdeaState replay or reconstruction.

## 9. Disclosure (every result)

Nominal declared values only; inputs not verified by InventorAI; no tolerance assessment; planar geometry at the
board plane only; no height, connector, insertion-path, mounting, electrical-clearance, thermal, strength, safety
or manufacturing assessment. No "the parts fit", whole-system compatibility, engineering verification, readiness or
certification follows. A failed declared placement does not prove that no placement or design could work.

## 10. Output boundary

Results are derived on every read from the validated current input snapshot; no numerical result, result history
or artifact is stored (calc/units §12 unchanged; the §3A bound is likewise derived on read and never stored). The interaction page, the report and the PDF consume ONE shared
presentation model built from ONE snapshot, with a simple explanatory 2D diagram (not to scale, not a drawing; a
NOT MET case shows the overlap, never a fit). A downloaded report or PDF is a historical snapshot naming its
declaration revision and generation time; it cannot be refreshed, revoked or kept current.

## 10A. CAD reference download (outbound only)

AMENDMENT (BOARD-ENCLOSURE-CAD-DOWNLOAD-01, Owner-authorized 2026-11-03). ONE download on the interaction page
returns ONE ZIP for a CURRENT declaration whose evaluation is MET or NOT MET: `geometry.dxf`, `companion.json`
bound to that exact DXF by SHA-256, and a UTF-8 `README.txt` guide in English and Arabic with the notices.

- **Content.** The DECLARED board and usable internal region at the board plane, centred and axis-aligned, as two
  closed polylines on two layers (`IAI_DECLARED_USABLE_REGION`, `IAI_DECLARED_BOARD_OUTLINE`); DXF R2013,
  `$INSUNITS` millimetres; origin at the region centre (a drawing convention, not a physical feature). A NOT MET
  declaration is exported as declared; the §3A bound is NEVER geometry and never replaces or resizes a declared
  value — it travels only in the companion, labelled conditional. The companion carries the project, interaction,
  component and revision references, the declaration revision, the snapshot digest, the original decimal inputs,
  the method / consequence versions, the outcome, margins, bound, the handoff format version and the limitations.
- **Ownership and boundary (ACE disposition).** The method consumer still owns every verdict, margin and bound; the
  Stage-15 owners still own the declaration; the shared presentation model builds the handoff from ONE validated
  snapshot; a separate adapter (`engine/planar_clearance_cad_export.py`) maps coordinates and formats only and
  recomputes nothing. It is an OUTBOUND, target-neutral reference export under the external engineering-tool
  boundary of the Technical Realization companion (§9.11) and the Phase-7 adapter pattern: NOT a Technical
  Realization lane, NOT a T6 / §0 activation, NOT CAD generation or design, NOT a D4 widening, no tool result is
  admitted (TOOL RESULT RECEIVED ≠ EVIDENCE ADMITTED), and no CAD tool or provider is selected or called.
- **Lifecycle.** Eligibility and the requested revision and digest are re-checked at download time against the ONE
  snapshot the response is built from; a stale, withdrawn, reconfirmation-needing, missing, inapplicable,
  unavailable or failed-evaluation state returns the page with a notice and no file; nothing is partially returned.
  Generated transiently in memory; nothing is stored or retained server-side (`Cache-Control: no-store`).
- **Meaning.** A planar reference snapshot of declared values — not an enclosure design, manufacturing approval,
  parametric model or whole-product verification. External CAD edits are unassessed and never synchronise back.
  The hash binds the delivered files; it is not physical verification. Any CAD measurement tolerance is a property
  of the receiving tool, never part of the §6 exact-decimal decision.

## 11. Source and IP qualification

- Claim: the margin relation of §3 for the configuration of §3 and §5. Authority: InventorAI's original derivation
  (§3), deductive and independently checkable; no external text, figure, table, dataset or code is used. Source-use
  basis: original InventorAI text.
- Unit authority: the existing owner record `dcu:U002` (NIST SP 811, millimetre) under `dcu:SU001`, reused
  unchanged.
- CGAL and Hammond enclosure documentation were discovery / reference leads only; nothing from them is imported,
  copied or relied upon. No protected standard, manufacturer table or third-party code is used.
- Owner authorization of this increment is not scientific validation and is no exception to source / IP rules.

## 12. Bounded D4 / interface-characterisation exception

D4 stays unactivated except for this ONE declared nominal planar comparison between the two components the inventor
named on ONE declared interaction. It is not a general compatibility evaluation, adds no other engineering
relationship and activates no T6 / Technical Realization lane or Stage 35 change.

## 13. Exclusions

Rotation or placement search; non-rectangular outlines or regions; per-side or per-axis clearance; tolerances or
stack-ups; height, insertion, connectors, mounting hardware, guides or slots; electrical clearance or creepage;
thermal, strength, vibration, safety, manufacturing or assembly assessment; CAD, simulation or external geometry
libraries; component suggestions or a "safe" clearance; result persistence; external AI / provider calls. AMENDED by
§10A: the outbound DXF reference download of declared values is admitted; CAD design, CAD generation, upload,
round-trip, simulation and any CAD tool or library at runtime other than the DXF writer stay excluded.

## 14. Language availability

AMENDED by BOARD-ENCLOSURE-ARABIC-QUALIFICATION-01 (the former English-only clause is superseded for the scope
below). The journey is available in English and Modern Standard Arabic through the existing UI-copy catalogue:
the interaction page renders in the interface language (right to left in Arabic) and the report / PDF section in
the report document's language. The English variant of every applicability statement and disclosure line is this
artifact's text word for word, so each Arabic line translates one governed meaning; method, declaration and
artifact versions are unchanged, and a language change is presentation only — never a new declaration, revision,
outcome or result. Numbers, `mm`, X / Y, identifiers and digests are LTR-isolated; the sketch is never mirrored.
Inventor text is stored and shown verbatim, never translated. Numeric entry keeps the §6 ASCII grammar: Arabic-Indic
or Persian digits, Arabic decimal or group separators, units and words are refused with an Arabic explanation and
never read as a number (native-digit entry is NOT delivered; it would be a separately scoped numeric-input change).
Qualified by synthetic fixtures in Modern Standard Arabic, Kuwaiti / Gulf and Egyptian Arabic alongside English:
free text (names, region descriptions, basis notes, including uncertainty and negation) is preserved and never
converted into a dimension, an unknown or an applicability answer — this is NOT understanding of unrestricted
dialect text, and no other dialect is claimed.
