# MECHANICAL — SPRING-MASS NATURAL FREQUENCY METHOD CONTRACT

STATUS: OWNER-AUTHORIZED BOUNDED METHOD CONTRACT — written with, and governing, the one bounded implementation increment
`MECHANICAL-NATURAL-FREQUENCY-01`, which the Owner authorized as ONE bounded (g1) step-3 engineering-depth increment
(method / source admission, the minimum calc / units owner Correction 12, implementation, focused tests and one pull
request). Applicability: this contract governs the delivered method only on the verified merge of that pull request into
`feature/atomic-json-session-persistence`; on its proposal branch it describes an Owner-authorized proposed method, not a
merged or delivered capability. Merge, deployment, production activation, a (g1) step-4 transition and any broader
capability admission are NOT authorized by it.
AUTHORITY LEVEL: subordinate to the accepted
[shared deterministic calculation and units owner boundary contract](SHARED_DETERMINISTIC_CALCULATION_AND_UNITS_OWNER_BOUNDARY_CONTRACT.md)
(the "calc/units contract", with its Correction 12, §13K, added by the same increment) and to the Mechanical Domain Pack's
governed authority. It amends no CAP-13 method contract: the two-support reactions, planar moment, planar required force
and rotational-load methods, their artifacts and behaviour stay unchanged. Where this document and the calc/units contract
differ, the calc/units contract wins and the difference is a defect of this document.

---

## 0. Preserved truth (binding)

- `ACTIVE CONTRACT: NONE` describes the state before and after this increment; this contract fills no active-contract slot
  after delivery and is not a delivery record. Current-truth delivery records belong to the post-merge closure sync.
- This method enters, completes or reopens no Stage and changes no roadmap count (27 of 45 complete); it stays within
  (g1) step 3. Stage 25 stays ENTERED / PARTIAL; `FULL CAP-13: NOT AUTHORIZED`; D-7 (the bounded stiffness method) stays
  NOT ADMITTED — this method takes the inventor's own stiffness value and computes none.
- The former `SRC-045 / NBS SP 615` basis is `IP-UNRESOLVED` and is relied upon by nothing here; no passage of it, including
  its 90° / maximum-amplitude verification passages, enters this increment.
- The eleven existing admitted methods keep their identities, artifacts, semantic pins, units and behaviour. The existing
  `angular_velocity` / `rad/s` record is neither weakened nor given a second meaning (§4).
- The Stage 15 integrated-part exception (`engine/subsystem_model.py`) is extended to this method by name only, for the
  declared Mechanical part (§1).

## 1. Purpose and scope

ONE optional, advisory, non-binding, request-local calculation: the undamped natural frequency `f₀` predicted by ONE
explicitly declared single-degree-of-freedom (SDOF) spring–mass model — ONE lumped mass `m` on ONE linear spring or mount
of stiffness `k`, whose other end is attached to an effectively rigid support. It gives a nontechnical inventor one
deterministic frequency figure for a model they declare themselves, so that they can compare the excitation they plan or
observe with it and ask for measurement or qualified engineering review — without inferring anything about the real
product.

Eligibility: a project whose trusted durable root domain (`confirmed_domain`, read as the CAP-12 gate reads it) is exactly
`mechanical`; or, whatever the initial analysis focus, the ONE inventor-declared Mechanical part of a valid durable
Stage-15 integrated composition, read only through the store-validated composition (`_calc_gate` / `_calc_declared_part`,
the rule the other Mechanical calculations use) and never from the request. On an integrated project the page names that
part with the existing CAP-13 attribution wording. A declared part makes the calculation OFFERED only: it establishes
neither that the project contains a spring–mass system, nor that the SDOF model applies, nor that the entered mass and
stiffness are correct, nor that resonance is safe or unsafe, and it supplies no value, declaration or screen answer — the
inventor still enters all of them. A missing, malformed, corrupt or unreadable composition grants nothing beyond the root
rule, and an unreadable root domain offers nothing (fail closed). The session link, the page and the submission read the
same one decision. Applicability comes only from the method's explicit declarations (§5).

## 2. Method identity and version

Identity `mechanical:spring_mass_natural_frequency`, version `1.0`. Method-authority artifact
`docs/governance/mechanical_content_config/spring_mass_natural_frequency_v1.json`
(`mechanical_spring_mass_natural_frequency`, artifact version `1`), separate from every CAP-13 artifact; none loads
another. Adapter `engine/mechanical_natural_frequency_method.evaluate`; consumer
`engine/mechanical_natural_frequency.py`.

## 3. Method definition and derivation

`f₀ = √(k / m) / (2π)`.

1. NBS Technical Note 487 (NBS-NF-S1, §11), in its Mechanical Drive derivation, defines the square-root stiffness-over-mass
   quantity and states, in substance, that it is the accepted undamped natural frequency for one mass driven by one spring
   whose other end is attached to a relatively very large mass: the undamped natural angular frequency is `√(k / m)`.
2. NIST SP 330 (NIST-NF-U, §11) states that angular frequency in rad/s and frequency in Hz differ by the factor 2π, angular
   velocity, angular frequency and frequency being distinct quantities.

The ordinary natural frequency `f₀ = √(k / m) / (2π)` is therefore a bounded InventorAI derivation from two clean source
facts. With `k` in N/m and `m` in kg the result is directly in Hz; no conversion factor is applied. The SDOF restriction,
the declarations and the ordinary-frequency form are InventorAI's own bounded restatement in its own words; no source
prose, figure, table, accelerometer-specific numerical result, percentage criterion or example is reused, and neither NBS
nor NIST publishes this method. The product relies only on that one factual SDOF relationship.

## 4. Roles, quantity kinds and exact unit tokens

| Role | Meaning | Quantity kind | Exact unit token |
|---|---|---|---|
| `k` | stiffness of the one linear spring or mount (restoring force per unit deflection) | `stiffness` | `N/m` |
| `m` | the one moving mass | `mass` | `kg` |
| `f0` (`f₀`) | undamped natural frequency of the declared SDOF model | `frequency` | `Hz` |

The units are fixed and shown, never chosen. `kg`, `N/m` and `Hz` are three NEW owner records (calc/units §13K:
`dcu:U018`, `dcu:U019`, `dcu:U020`), each the one token of a NEW quantity kind; `N/m` is recorded as InventorAI's bounded
quantity usage of the coherent newton per metre that SP 330 lists. **Angular velocity, angular frequency and frequency
are distinct:** the output is bound to the new `frequency` kind, NOT to the existing `angular_velocity` kind merely
because an angular frequency could also be written in rad/s; no kind holds `rad/s` for a second meaning, nothing maps `Hz`
to `rad/s` and the factor 2π lives in the adapter alone. No conversion exists: `g`, `t`, `lb`, `N/mm`, `kN/m`, `lbf/in`,
`rpm`, `kHz` and `1/s` are not admitted, aliased or normalised. `f0` is the ASCII role identifier of `f₀`, never an alias.

## 5. Applicability declarations

Each is shown as its own statement and answered «applies» or «does not apply», none pre-selected. A missing answer is
`NOT_DECLARED`; «does not apply» is `MODEL_NOT_SUPPORTED`. InventorAI infers none of them. No numeric validity threshold
is stated or invented: a declaration only makes the bounded model applicable; it does not validate the physical product.

| Ref | Id | Accepted statement |
|---|---|---|
| D-1 | `single_mass` | ONE mass only, represented by m: the moving body is treated as one rigid lump, and m is its whole moving mass |
| D-2 | `single_linear_spring` | ONE linear spring or mount only, represented by k: one elastic element whose restoring force is proportional to how far it is deflected, and k is that constant stiffness |
| D-3 | `rigid_support` | the other end of the spring or mount is attached to a support that is treated, for this model, as effectively rigid and of very large mass compared with the moving mass, so that it does not move |
| D-4 | `single_degree_of_freedom` | ONE degree of freedom only: the mass moves back and forth along one direction only, with no other motion, rotation or coupled movement |
| D-5 | `own_values` | the stiffness k and the mass m are the inventor's own values; InventorAI does not look them up, derive them, check them or decide that they are right |
| D-6 | `damping_not_modelled` | damping (friction, air, rubbing, material loss or any other energy loss) is NOT modelled in this calculation: the result is the undamped natural frequency of the declared model |
| D-7 | `outside_scope_excluded` | nonlinear stiffness, several masses or several springs, coupling between motions, and stiffness that changes with load, position, temperature or time are outside this model and are not included |

## 6. Numeric domain and numerical acceptance

- **Grammar and exact-decimal screening.** `k` and `m` are typed as strict unsigned ASCII decimals of up to twelve integer
  digits and up to nine fractional digits (no sign, exponent, separator, Unicode digit, unit suffix or normalization),
  each also capped at 64 characters for abuse protection only — a NON-PHYSICAL bound, never a range of valid stiffnesses
  or masses. The exact decimal value of each input must be strictly greater than zero, checked on the exact decimal
  before any binary rounding; anything else, a zero included, is `INVALID_NUMERIC_INPUT`, resolved before the shared owner
  is called. Each admitted decimal is converted ONCE, correctly rounded, to binary64 for the owner, which parses no string.
- **No physical magnitude ceiling exists.**
- **Binary execution and the mathematical-constant policy (method-local; no constants registry).** The adapter executes
  three correctly rounded binary64 operations in a fixed order: `ratio = k / m`, `omega = √ratio`, `f₀ = omega / TWO_PI`,
  with `TWO_PI = 2.0 × math.pi` — the exact doubling of the binary64 value nearest π (the Python / C library constant,
  round-to-nearest). Every reference computation uses instead the 50-decimal TRUNCATION of π as the rational interval
  `PI_LOW < π < PI_HIGH` (`PI_HIGH = PI_LOW + 10^-50`); both constants are verified independently of the implementation by
  test (a Machin-formula computation of π, and `float(PI_LOW) == math.pi`).
- **Binary acceptance (adapter).** From the two actual binary input values the EXACT rational ratio is formed; its square
  root is bracketed with integer arithmetic (`isqrt` at scale 10^40) and the natural frequency as
  `[s_low / (2 PI_HIGH), s_high / (2 PI_LOW)]`, an interval that contains the true `√(k/m) / (2π)` for those inputs. The
  computed `f₀` is accepted ONLY when it is finite, strictly positive and within a relative error of `2^-50` of that
  interval. For a normal ratio the three executed operations carry at most about `2.9 × 2^-53` relative error (the
  ratio's rounding `2^-53`, halved by the square root to `0.5 × 2^-53`; the square root's own rounding `2^-53`; the π
  constant below `0.4 × 2^-53`; the final division `2^-53`), so a correctly rounded execution always meets the bound; a subnormal ratio is accepted only when its larger rounding error still meets
  it. Overflow of `k / m` to infinity, underflow to zero, a non-finite or non-positive result and a result outside the
  bound are `FAILURE / EXECUTION_INTEGRITY_FAILURE` with no numerical payload, displayed as `KNOWLEDGE_UNAVAILABLE`,
  never rewritten as a refusal; they are unreachable from the page grammar (the ratio of two admitted decimals lies within
  `10^-21` to `10^21`) and are proven at owner and adapter level.
- **Decimal-reference acceptance (consumer; the independent oracle).** From the EXACT decimal inputs the consumer computes
  the reference with the `decimal` module at 60 significant digits — the correctly rounded quotient, its correctly rounded
  square root and the correctly rounded division by `2π` with the 60-decimal truncation of π — an algorithm independent of
  the adapter's integer bracket and of the binary64 execution, with a relative error far below `10^-57`. The accepted
  owner result must lie within a relative `2^-50` of it (the proven worst case of the binary path, the two input
  conversions included, is below `4 × 2^-53`); otherwise `KNOWLEDGE_UNAVAILABLE` and no number.
- **Display.** That decimal reference is rounded ONCE to 12 significant digits, half to even, with trailing zeros dropped;
  plain decimal notation for `10^-6 ≤ f₀ < 10^12`, `m × 10^e` otherwise; a nonzero value never displays as zero. The
  display is ALWAYS labelled rounded: the natural frequency of a rational `k / m` is never a terminating decimal because π
  is irrational, so no exact label exists for this method and none is shown. The display is accepted only when the
  reference widened by a relative `10^-55` on either side rounds to the same 12 digits; otherwise `KNOWLEDGE_UNAVAILABLE`.

## 7. Refusal and abstention semantics

Order after request integrity (CSRF), project authorization, eligibility and strict capture (a malformed request — an
unknown or repeated field, or an answer outside its closed choices — is a bare 400 with no reason token): (1) completeness —
every declaration and screen item answered, else `NOT_DECLARED`; (2) screen — any YES is `ENGINEERING_REVIEW_REQUIRED` and
the owner is not invoked; (3) declarations — any «does not apply» is `MODEL_NOT_SUPPORTED`; (4) numeric (§6) — grammar,
representation limits and strictly positive exact decimals, else `INVALID_NUMERIC_INPUT`; (5) the shared owner; (6) the
decimal-reference acceptance; (7) the guarded display. The first failing stage alone decides; no stage after it is
evaluated. Owner correspondence: `REFUSAL / INVALID_NUMERIC_INPUT` → `INVALID_NUMERIC_INPUT`;
`REFUSAL / UNIT_NOT_ADMITTED` or `UNKNOWN_UNIT` → `UNIT_NOT_SUPPORTED`; `REFUSAL / METHOD_NOT_REGISTERED` or
`VERSION_MISMATCH`, `UNABLE / SOURCE_UNAVAILABLE` and `FAILURE / EXECUTION_INTEGRITY_FAILURE` → `KNOWLEDGE_UNAVAILABLE`;
any other owner state → the neutral `UNMAPPED_OWNER_OUTCOME`. The owner state and token are preserved, never rewritten.

## 8. High-risk screen (declared; not a safety engine)

The same nine items as the other Mechanical calculation screens, in the same order and with the same copy: supports
people; overhead or falling hazard; use by or for children; safety-critical load path; pressure; high temperature;
battery containment; medical use; food contact. All NO answers only allow this bounded calculation to proceed and never
mean safe. The screen neither reads nor feeds SafetySignal.

## 9. Result, provenance and fixed disclosure

On success the page shows the inventor-declared `k` and `m` (echoed verbatim), the calculated `f₀` in Hz as the
12-significant-digit rounding of the decimal reference with the rounded label, labelled `UNVALIDATED` and `NOT EVIDENCE`,
the bounded next-step wording, the method identity and version, the method sources and unit records the owner carried,
the model declarations echoed and this fixed disclosure (English; pinned equal to the artifact):

1. This is the natural frequency f₀ predicted by the single-degree-of-freedom spring–mass model you declared: one mass m on one linear spring or mount of stiffness k, attached to an effectively rigid support, with no damping, using your own k and m.
2. It is a prediction of the declared model, not a measured property of your product: the real system may have several masses, several elastic parts, damping, nonlinear or changing stiffness and a support that moves, none of which is included.
3. It does not say that resonance will occur exactly at this frequency, that any frequency is safe or must be avoided, that any separation margin is acceptable, that any vibration is acceptable, or that any component is suitable.
4. It is preliminary, advisory, UNVALIDATED and not evidence: compare planned or observed excitation with this estimate and verify the real system by measurement or qualified engineering review before any reliance.
5. InventorAI does not check your stiffness, your mass or that your declarations match the real configuration; it looks nothing up.
6. Damping, resonant amplitude, transmissibility, vibration isolation, shock, fatigue, several degrees of freedom and modal analysis are outside this calculation.
7. Reference source material: National Bureau of Standards Technical Note 487 (Newman, 1969) for the undamped single-degree-of-freedom spring–mass relationship, and NIST Special Publication 330 for the SI units and the 2π relation between angular frequency and frequency; the method as offered here is InventorAI's own restatement.

**Bounded next-step wording.** The only allowed meaning: this is the natural frequency predicted by the declared SDOF
spring–mass model; compare planned or observed excitation with this estimate and verify the real system by measurement
or qualified engineering review. The page never says "safe frequency", never gives "avoid this frequency" as an automatic
verdict, never says resonance will occur exactly here, and states no acceptable separation margin, acceptable vibration or
component suitability.

## 9A. Arabic disclosure and UX wording

**A-1 Fixed disclosure (Arabic rendering of the seven §9 items, item by item; no meaning added, removed or softened).**

> 1. هذا هو التردد الطبيعي f₀ الذي يتنبأ به نموذج النابض والكتلة ذو درجة الحرية الواحدة الذي صرّحت به: كتلة واحدة m على نابض أو حامل خطي واحد صلابته k، مثبّت إلى سند جاسئ فعليًا، دون تخميد، باستخدام قيمتي k وm اللتين أدخلتهما أنت.
> 2. هذه تنبؤ بالنموذج المصرَّح به، وليست خاصية مقيسة لمنتجك: فقد يحتوي النظام الحقيقي على عدة كتل، وعدة أجزاء مرنة، وتخميد، وصلابة غير خطية أو متغيرة، وسند يتحرك، ولا شيء من ذلك مُدرَج.
> 3. لا يقول هذا الناتج إن الرنين (resonance) سيحدث عند هذا التردد بالضبط، ولا إن أي تردد آمن أو يجب تجنبه، ولا إن أي هامش فصل مقبول، ولا إن أي اهتزاز مقبول، ولا إن أي مكوّن مناسب.
> 4. هذه النتيجة أولية وإرشادية، وغير مُتحقَّق منها (UNVALIDATED)، وليست دليلًا: قارن الإثارة المخطَّطة أو الملاحَظة بهذا التقدير، وتحقق من النظام الحقيقي بالقياس أو بمراجعة هندسية مؤهلة قبل أي اعتماد عليه.
> 5. لا يتحقق InventorAI من قيمة الصلابة ولا من الكتلة ولا من مطابقة تصريحاتك للتكوين الفعلي؛ ولا يبحث عن أي شيء.
> 6. التخميد، وسعة الرنين، وقابلية الانتقال (transmissibility)، وعزل الاهتزاز، والصدمات، والكلال (fatigue)، وتعدد درجات الحرية، والتحليل النمطي (modal analysis) كلها خارج نطاق هذا الحساب.
> 7. المراجع: المذكرة الفنية رقم 487 للمكتب الوطني للمعايير (NBS Technical Note 487، نيومان، 1969) لعلاقة النابض والكتلة ذات درجة الحرية الواحدة غير المخمَّدة، والمنشور الخاص رقم 330 للمعهد الوطني للمعايير والتقنية (NIST SP 330) لوحدات النظام الدولي وعلاقة 2π بين التردد الزاوي والتردد؛ أما الطريقة بالصورة المقدَّمة هنا فهي إعادة صياغة خاصة بـInventorAI.

**A-2 Applicability declarations (§5).** The inventor answers «ينطبق على حالتي» or «لا ينطبق على حالتي», none pre-selected.

| §5 | Arabic statement |
|---|---|
| D-1 single_mass | كتلة واحدة فقط يمثّلها الرمز m: يُعامَل الجسم المتحرك على أنه كتلة صلبة واحدة مجمَّعة، وm هي كامل كتلته المتحركة. |
| D-2 single_linear_spring | نابض أو حامل مرن خطي واحد فقط يمثّله الرمز k: عنصر مرن واحد تتناسب قوة إرجاعه مع مقدار انحرافه، وk هي صلابته (stiffness) الثابتة. |
| D-3 rigid_support | الطرف الآخر من النابض أو الحامل مثبّت إلى سند يُعامَل في هذا النموذج على أنه جاسئ فعليًا وذو كتلة كبيرة جدًا مقارنةً بالكتلة المتحركة، بحيث لا يتحرك. |
| D-4 single_degree_of_freedom | درجة حرية واحدة فقط: تتحرك الكتلة ذهابًا وإيابًا على امتداد اتجاه واحد فقط، دون أي حركة أخرى أو دوران أو حركة مقترنة. |
| D-5 own_values | قيمتا الصلابة k والكتلة m هما قيمتا المخترع نفسه؛ لا يبحث عنهما InventorAI ولا يشتقّهما ولا يتحقق منهما ولا يقرر أنهما صحيحتان. |
| D-6 damping_not_modelled | التخميد (الاحتكاك أو مقاومة الهواء أو الاحتكاك الداخلي أو فقد الطاقة في المادة أو أي فقد آخر للطاقة) غير مُدرَج في هذا الحساب: النتيجة هي التردد الطبيعي غير المخمَّد للنموذج المصرَّح به. |
| D-7 outside_scope_excluded | الصلابة غير الخطية، وتعدد الكتل أو النوابض، والاقتران بين الحركات، والصلابة المتغيرة مع الحمل أو الموضع أو درجة الحرارة أو الزمن كلها خارج هذا النموذج وغير مُدرَجة. |

**A-3 Screen (§8).** The Arabic screen stem, items, answers and note are the existing Mechanical screen copy
(`UI_CAP13_SCREEN_*`), reused unchanged; the integrated-part attribution is the existing `UI_CAP13_PART_*` copy.

**A-4 Right-to-left rendering.** Numbers, the role symbols `k`, `m` and `f₀`, the unit tokens `N/m`, `kg` and `Hz`, the
relation `√(k / m) / (2π)`, the method identity and `UNVALIDATED` / `NOT EVIDENCE` are each direction-isolated
(`<bdi dir="ltr">`) on the Arabic page; the inventor's typed values are shown left-to-right.

## 10. Exclusions (binding)

No damping-ratio calculation, damped natural frequency, resonant-amplitude calculation, transmissibility, vibration
isolation, Q-40 activation, shock response, fatigue, allowable-vibration criterion, separation margin, multi-degree-of-freedom
or modal analysis, finite-element analysis; no stiffness lookup, mass lookup, spring selection, sensor selection, motor
compatibility, component sizing, suitability or safety conclusion; no inference of any declaration, stiffness or mass; no
unit conversion; no result persistence, result transfer into another calculation, report, PDF, Structured Export, API,
evidence, readiness, progression, gap or SafetySignal effect (the existing calculation presentation pattern carries none of
these); no AI or provider effect; no eligibility for any part other than the one declared Mechanical part (§1), and no
inference from a part's name or function. No Stage is entered, completed or reopened.

## 11. Source and source-use status

- **NBS-NF-S1** — National Bureau of Standards Technical Note 487, *Considerations in Computing the Useful Frequency Range
  of Piezoelectric Accelerometers*, Nathan Newman, Institute for Applied Technology, National Bureau of Standards, issued
  July 1969; official NIST / NBS copy, recorded at the NIST legacy-publications location
  (<https://nvlpubs.nist.gov/nistpubs/Legacy/TN/nbstechnicalnote487.pdf>). Supports, for this method, only the one
  relationship of §3 (Mechanical Drive derivation; location recorded at derivation level, no page number supplied).
  Inspected by the Execution Lead and supplied in the Owner-authorized MECHANICAL-NATURAL-FREQUENCY-01 brief (2026-10-29);
  not independently re-inspected by the executor (egress to the NIST host was blocked). Not reused: source prose, figures,
  tables, accelerometer-specific numerical results, percentage criteria, examples, any third-party material.
- **NIST-NF-U** — NIST Special Publication 330 (2019 Edition), *The International System of Units (SI)*, Section 2
  (<https://www.nist.gov/pml/special-publication-330/sp-330-section-2>). Supports only the unit facts of §4 — the kilogram
  as the SI base unit of mass; coherent derived units formed as products and quotients of SI units, the newton per metre
  `N m^-1` among those listed; the hertz as the SI coherent derived unit with a special name for frequency — and the 2π
  relation between angular frequency (rad/s) and frequency (Hz) with the distinction between angular velocity, angular
  frequency and frequency. Lead-supplied (same brief, 2026-10-29), location recorded at section level.
- **Source use** (not legal opinions): the NIST Technical Series rights pattern already recorded in the repository —
  NBS / NIST employee-authored Technical Series works are not subject to U.S. copyright protection; attribution is
  preserved; no endorsement is implied; third-party content is excluded; commercial / product use is permitted on the
  recorded NIST basis — applied as this method's own bounded records `mnf:SU001` (NBS-NF-S1) and `mnf:SU002` (NIST-NF-U),
  with the owner snapshots `dcu:SU020` and `dcu:SU021`. Use is factual paraphrase and unit identification only. The
  existing records (`dcu:SU001`, `dcu:SU003`, `mechanical:PR011`, `THERM-SU-NIST`) keep their own scopes and are not
  extended. All inspections are LEAD_SUPPLIED claim-level inspections; TECH-SOURCES-001 is neither waited for nor
  mutated.

## 12. Implementation boundary

The one existing shared owner executes the method through ONE additional immutable binding created by application wiring
(`_MNF_BINDING` in `web/app.py`), beside the eleven existing bindings; there is no registry, discovery, dynamic module path
or request-selected method (calc/units §13K). Routes: `GET` / `POST /session/<sid>/natural-frequency`, behind the central
project authorization and the global CSRF guard; the session page shows one optional link on an eligible project.
Eligibility reuses `_calc_gate(sid, consumer)` (§1). The square root is executed inside the adapter and is never exposed as
a generic owner operation; the consumer imports no other consumer. Nothing is persisted; the POST renders its result
directly.

## 13. Verification

Focused tests (`tests/test_mechanical_natural_frequency.py`, `tests/test_mechanical_natural_frequency_browser.py`): the
adapter against an independent oracle (the `decimal` module at 60 digits with a Machin-formula π, and an exact identity
check `(2π f₀)² m ≈ k`) for normal and boundary values and a random sample; the π constants verified independently;
overflow, underflow and subnormal ratios; zero-input refusal versus underflow; non-finite, invalid and out-of-scope input;
unit / method / version / adapter integrity failing closed; owner artifact v12 integrity (every content-version-11 record
unchanged by digest) and method-artifact tamper; the §7 order and owner correspondence; the exact-decimal screening and
the 12-digit rounded display; the Mechanical-root and declared-Mechanical-part gate with malformed, stale and corrupt
compositions failing closed; request integrity, isolation and no persistence; the eleven existing methods unchanged; EN /
AR fidelity, RTL isolation and real-browser EN / AR journeys at phone width. Hosted required CI on the final PR head is the
merge gate.

## 14. STOP conditions

Stop and return to the Owner on a source or IP deficiency, a contract incompatibility, unprovable numerical integrity, a
required broad owner redesign or generic conversion mechanism, or any scope expansion (another method, consumer, unit,
conversion, eligibility beyond §1, persistence, result transfer or report surface).
