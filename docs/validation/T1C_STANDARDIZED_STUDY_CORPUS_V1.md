# T1-C′ Standardized Synthetic Study Corpus — V1

## A. Status / purpose

**T1-C′ STANDARDIZED SYNTHETIC STUDY CORPUS**
**PREPARATION ARTIFACT**
**HUMAN EXECUTION NOT AUTHORIZED**

This file is a frozen, standardized, synthetic *input* corpus prepared for the future T1-C′
bounded real-user round (PDVG-01 §6.C; `DEFERRED_OBLIGATIONS_REGISTER.md` row "T1-C′"). It is a
validation/study input artifact, not a governance authority surface. It authorizes nothing: no
recruitment, no participant contact, no data collection, no human-study execution, no benchmark
run, no deployment. It is NOT a benchmark, NOT a regression fixture, NOT a product-tuning corpus,
NOT a classifier-training corpus, NOT a T1-A′ artifact, NOT a general domain-validation suite,
and NOT evidence that the product passed T1-C′.

## B. Corpus identity

- Version: **V1**
- Cases: **exactly 2**
- Domains: `electronics_electrical` (T1C-EE-01), `mechanical` (T1C-ME-01)
- Languages per case: English and Arabic, semantically aligned; natural-wording differences are
  permitted and no literal linguistic identity is claimed.
- File identity (SHA-256 / bytes / lines) and the per-case participant-text hashes are recorded
  in the candidate return and commit that introduce this file, never inside this file.

## C. Freeze / non-tuning rule

After acceptance for T1-C′:

1. The exact study text in the two participant-text blocks below is frozen.
2. Product code must not be tuned against these cases before the human round.
3. The cases must not be added as regression fixtures for pre-study improvement.
4. The cases must not enter T1-A′ (the S2 benchmark) or any other governed benchmark.
5. The cases must not be used to modify, extend or re-weight classifier or domain signals.
6. Any change to the study text creates a NEW corpus version (V2, …) and must not silently
   replace V1; V1 remains as recorded so an executed round can always be tied to its exact text.
7. No automated product test may consume the participant-text blocks.

### Participant-text block boundaries and hashing rule

Each case's participant-facing text is delimited by an explicit BEGIN and END marker line. The
per-case SHA-256 is computed over the UTF-8 bytes of everything strictly between the two marker
lines: from the first byte after the BEGIN line's newline up to, but not including, the first
byte of the END line. Verify before any study round with:

```
awk '/^<!-- T1C-EE-01 PARTICIPANT TEXT BEGIN -->$/{f=1;next} /^<!-- T1C-EE-01 PARTICIPANT TEXT END -->$/{f=0} f' \
  docs/validation/T1C_STANDARDIZED_STUDY_CORPUS_V1.md | sha256sum
```

(`awk` prints each captured line with a trailing LF, which equals the bytes between the markers.)
Replace `EE` with `ME` for the second case.

## D. T1C-EE-01

- Intended domain: `electronics_electrical`

<!-- T1C-EE-01 PARTICIPANT TEXT BEGIN -->
EN — idea: A plug-through safety adapter for a clothes iron. The iron plugs into the adapter and the adapter plugs into the wall socket. If the iron is left resting face-down and has not been moved for a few minutes, the adapter cuts the power to the iron until someone picks the iron up or presses a reset button on the adapter.

EN — context: The inventor lives with a relative who sometimes forgets to switch the iron off. They want something that works with the ordinary iron they already own, without modifying the iron itself. They imagine a small sensing unit that sits on the iron's handle or cord and signals the adapter, but they are not sure whether that is the right approach. Nothing has been built yet.

EN — known constraint: The adapter must carry the full current of a normal household iron and fit an ordinary wall socket.

AR — idea: محوّل أمان يُركَّب بين مكواة الملابس ومقبس الحائط. تُوصَل المكواة بالمحوّل، ويُوصَل المحوّل بمقبس الحائط. إذا تُركت المكواة مستقرة على وجهها ولم تُحرَّك لبضع دقائق، يقطع المحوّل الكهرباء عن المكواة إلى أن يرفعها أحد أو يضغط زر إعادة التشغيل الموجود على المحوّل.

AR — context: يعيش المخترع مع قريب ينسى أحياناً إطفاء المكواة. يريد شيئاً يعمل مع المكواة العادية التي يملكها بالفعل دون تعديل المكواة نفسها. يتصور وحدة استشعار صغيرة تُثبَّت على مقبض المكواة أو سلكها وترسل إشارة إلى المحوّل، لكنه غير متأكد من أن هذا هو النهج الصحيح. لم يُصنع أي شيء بعد.

AR — known constraint: يجب أن يتحمل المحوّل التيار الكامل لمكواة منزلية عادية وأن يناسب مقبس حائط عادياً.
<!-- T1C-EE-01 PARTICIPANT TEXT END -->

## E. T1C-ME-01

- Intended domain: `mechanical`

<!-- T1C-ME-01 PARTICIPANT TEXT BEGIN -->
EN — idea: A laundry drying rack that hangs on the outside of a balcony railing. The rack has two arms that fold flat against the railing when not in use and swing out and lock in a level position when laundry is hung on it, so that it does not take up space on the balcony floor.

EN — context: The inventor lives in a small apartment where the balcony is the only place to dry laundry. They want the rack to be fitted and removed by hand, without drilling into the railing or the wall. They imagine hinged arms with a locking position but are not sure how to keep the rack from tipping or slipping when it is loaded with wet laundry. Nothing has been built yet.

EN — known constraint: The rack must hold a full load of wet laundry on a railing of ordinary height without damaging the railing.

AR — idea: منشر غسيل يُعلَّق على الجهة الخارجية لسور الشرفة. للمنشر ذراعان تنطويان بشكل مسطح على السور عند عدم الاستخدام، وتنفتحان وتنقفلان في وضع أفقي عند تعليق الغسيل عليهما، بحيث لا يشغل المنشر مساحة من أرضية الشرفة.

AR — context: يعيش المخترع في شقة صغيرة الشرفة فيها هي المكان الوحيد لتجفيف الغسيل. يريد أن يُركَّب المنشر ويُنزَع باليد، دون ثقب السور أو الجدار. يتصور ذراعين بمفصلات لهما وضع قفل، لكنه غير متأكد من كيفية منع المنشر من الانقلاب أو الانزلاق عندما يُحمَّل بالغسيل المبلل. لم يُصنع أي شيء بعد.

AR — known constraint: يجب أن يتحمل المنشر حمولة كاملة من الغسيل المبلل على سور بارتفاع عادي دون إلحاق ضرر بالسور.
<!-- T1C-ME-01 PARTICIPANT TEXT END -->

## F. Provenance

- Both cases are synthetic.
- Both were created specifically for T1-C′ preparation (2026-09-23).
- No participant invention is used or imitated.
- No confidential third-party material is used.
- No proprietary external text is copied.
- Neither case belongs to, or renames, an existing benchmark, ILT-002, activation-smoke or
  boundary-corpus concept family.

## G. Observed admission behaviour at preparation time (descriptive only)

Measured read-only at authoritative HEAD `079a9000bd23d19328b10c3854490264bf9b1697`, by calling
`engine.domain_rules.classify_domain` on the full participant text (idea + context + known
constraint) and by driving the normal `/start` admission with a throwaway local database:

| Case / language | Classifier result on full text | Admission path observed |
|---|---|---|
| T1C-EE-01 EN | `SINGLE` → `electronics_electrical` | direct confirmation of `electronics_electrical` |
| T1C-EE-01 AR | `NONE` | governed classifier-miss path: explicit domain choice → confirmation |
| T1C-ME-01 EN | `NONE` | governed classifier-miss path: explicit domain choice → confirmation |
| T1C-ME-01 AR | `NONE` | governed classifier-miss path: explicit domain choice → confirmation |

All four versions were admitted into a normal Path-N session with the intended domain and a
durable project; the first question was served in the selected UI language.

This table is **evidence-at-preparation-time and descriptive only**. It is not an expected study
result, it must not be used to justify product tuning before the study, and the case text was not
reworded after these observations were obtained. A future release candidate may behave
differently; any such difference must be observed and recorded, not corrected to match this table.

## H. Claim / generalization limit

These two cases are a bounded first-round study corpus only. They do NOT represent all invention
types, all current or future domains, all safety profiles, commercial validation, market demand,
product-market fit, or universal usability. The current two-domain coverage is the current study
baseline, not a permanent product-domain ceiling: future activated domains follow their own
governed activation and validation paths and are not added to this corpus by existence alone.

## I. Study-design observations (recorded, not product requirements)

1. The two English cases currently have different admission paths (see §G). Domain-to-domain
   performance in a round must therefore not be interpreted as if admission conditions were
   identical.
2. Both cases carry meaningful safety considerations (a mains-powered heating appliance; a loaded
   structure on a balcony railing). This is acceptable for the round, but later conclusions must
   not be generalized to low-risk or unrelated invention classes.
3. Arabic current behaviour remains `NONE` → explicit domain choice → confirmation. No Arabic
   classifier vocabulary is added for the study, and this path is an accepted current product path.

None of the observations above creates a product requirement.
