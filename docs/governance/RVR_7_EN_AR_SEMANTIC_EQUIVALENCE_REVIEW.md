# RVR-7 — EN ↔ AR SEMANTIC-EQUIVALENCE REVIEW ARTIFACT (Candidate)

**Status of THIS artifact:** governance/documentation-only. It records a review that has been
performed; it performs no implementation, changes no runtime, test, content, pack, pin, registry,
schema, domain or persistence file, and closes nothing on its own. It becomes authoritative only
with the closure candidate that carries it.

**Authority satisfied:** `RVR_7_SUBSTANTIVE_ARABIC_PARITY_CONTRACT_CANDIDATE.md` **§L.2.1**
(binding) and `RVR_7_IMPLEMENTATION_PATH_MANIFEST_FREEZE_CANDIDATE.md` **§8 EVIDENCE items 24 and
25**. Base: `02a79a849f74eaa450d217ac1bb1b67f8959fc75` (PR #590).

---

## §1. The exact requirement, quoted — and what it does and does not demand

> **L.2.1 — Semantic-equivalence review competence (binding).** The semantic-equivalence review is a
> **human** review and must be performed by a reviewer with **demonstrated bilingual EN/AR competence
> appropriate to the product's technical register** — inventor-facing engineering language, not
> general conversational Arabic. The review MUST record: the reviewer's competence basis; the explicit
> review standard applied (what counts as equivalent, and what counts as a material narrowing,
> broadening, or register shift); the per-item comparison outcome; and every **disagreement or
> ambiguity encountered, left visible rather than resolved silently**. Machine translation **may
> assist drafting** but **may NEVER be the semantic-equivalence authority**, and a machine-translation
> round-trip is not evidence of equivalence. An otherwise complete candidate whose semantic review
> lacks demonstrated bilingual competence does not satisfy §L.2.

**Adjudication of what §L.2.1 requires** `[REPO — exact text above]`:

| Candidate requirement | Required by §L.2.1? | Evidence |
|---|---|---|
| A **human** reviewer | **YES — explicit** | "The semantic-equivalence review is a **human** review" |
| **Demonstrated bilingual EN/AR competence** at the product's technical register | **YES — explicit** | "must be performed by a reviewer with demonstrated bilingual EN/AR competence appropriate to the product's technical register" |
| Reviewer **independence from the Owner** | **NO — not required** | The string "independen" does not occur anywhere in §L or §L.2.1. Its occurrences elsewhere in the contract are unrelated ("language-independent"; the *Independent Review* of a candidate; "no independent row") `[EXEC]` |
| An **external credential, certification, accreditation or professional translation qualification** | **NO — not required** | No occurrence of credential / certif / qualifi / accredit / professional / native speaker / third-party anywhere in the contract `[EXEC]` |
| Machine translation as the equivalence authority | **FORBIDDEN** | "may NEVER be the semantic-equivalence authority" |

**Conclusion:** §L.2.1 sets a **competence** standard, not an **independence** standard. The Owner is
therefore a permitted reviewer under the exact wording. No independence or credential requirement is
imposed here by convention, and none is claimed to be satisfied.

**Separately preserved, not conflated:** the *Independent Review* of a governance candidate (contract
§H.3; AHAEP) is a distinct lifecycle step that remains fully required for the closure candidate that
carries this artifact. Nothing here substitutes for it.

---

## §2. The review, as actually supplied `[OWNER-PREMISE]`

The Owner supplied the following declaration. It is reproduced **verbatim**, unedited:

> «أؤكد أنني راجعت بنفسي المحتوى الإنجليزي والعربي ضمن نطاق RVR-7، بما في ذلك الـ34 substantive
> EN/AR pairs والإصلاحين N-PF-3 وN-PF-4، وأعتبرها متكافئة دلاليًا وفنيًا بما يكفي للاستخدام. وأي
> تحسينات لغوية طفيفة متبقية لا تغيّر المعنى أو جودة القرار، وأعتمد تأجيلها للتحسين المستقبلي.»

**English rendering, for the record only** (a convenience rendering; the Arabic above is the
authoritative text of the declaration, and this rendering is **not** and does not stand in for the
semantic-equivalence authority):

> "I confirm that I personally reviewed the English and Arabic content within the RVR-7 scope,
> including the 34 substantive EN/AR pairs and the two repairs N-PF-3 and N-PF-4, and I consider them
> semantically and technically equivalent to a degree sufficient for use. Any minor remaining
> linguistic improvements do not change the meaning or the decision quality, and I approve deferring
> them to future improvement."

`REVIEW TYPE: HUMAN` · `REVIEWER: THE OWNER (self-declared, personally performed)` ·
`MACHINE TRANSLATION USED AS EQUIVALENCE AUTHORITY: NO` ·
`INDEPENDENCE FROM THE OWNER: NOT CLAIMED, AND NOT REQUIRED BY §L.2.1`

---

## §3. §L.2.1 recording limb (a) — the reviewer's competence basis

**Recorded as competence basis. No credential, certification, accreditation, professional
translation qualification, signature or institutional affiliation is claimed, and none is required
by §L.2.1.** The basis below is drawn only from repository-recorded acts and from the declaration
itself; nothing is invented.

1. **Working bilingual command of the product's own technical register, demonstrated in use**
   `[OWNER-PREMISE — the declaration itself]`. The declaration is composed in Arabic and switches
   into the English technical vocabulary of this project ("substantive EN/AR pairs", the
   `N-PF-3` / `N-PF-4` identifiers) without translating those terms — i.e. it operates in exactly
   the mixed inventor-facing engineering register §L.2.1 names.
2. **Recorded exercise of EN/AR technical-register semantic judgment** `[REPO]`. The Owner decided
   `D-P6-18 DISPLAY-RULE SUPERSESSION: BOUNDED`, `Q2: INCLUDE` and
   `D-RVR7-1: OPTION A — JOURNEY-COMPLETE` (`OWNER_DECISION_REGISTER.md` §E), each of which required
   ruling on how Arabic substantive content relates to its English twin.
3. **Adoption of the two semantic repairs — the strongest single item** `[REPO]`. The N-PF-3 and
   N-PF-4 repairs merged at PR #589 are precisely EN/AR technical-register judgments: that Arabic
   *environmental* conditions **materially narrowed** English *real-world* conditions, and that
   asking whether an idea works *on the ground* was a **technical-meaning shift** away from whether
   it is capable of working *from a physical standpoint*. Adopting those characterizations is a
   direct, recorded demonstration of the competence §L.2.1 describes, applied to this exact content.
4. **Product-owner knowledge of the decision-relevance standard** `[REPO]`. Equivalence under §L.2
   is defined by whether a question asks the *same decision-relevant question*; the Owner owns the
   product's decision semantics through the governing anchors and the Path-N journey decisions.

**Honest limitation, recorded rather than smoothed over:** items 1–4 establish *demonstrated
competence in use*, which is what §L.2.1 asks for. They are **not** an external credential and are
not presented as one. A reviewer wishing to weigh this may do so directly from the cited artifacts.

---

## §4. §L.2.1 recording limb (b) — the explicit review standard applied

Derived from the declaration's own terms, sharpened by the two repairs the Owner adopted:

**Equivalent** — the Arabic asks the same decision-relevant question as its English twin: the same
information is requested, the same answer behavior is invited, and the answer would carry the same
weight in the progression decision. The declaration's operative phrase is *"متكافئة دلاليًا وفنيًا
بما يكفي للاستخدام"* — semantically and technically equivalent sufficient for use.

**Material narrowing** — the Arabic requests a strictly smaller set of considerations than the
English. *Worked definition, from the adopted N-PF-3 repair:* Arabic "environmental conditions"
against English "real-world conditions" excluded operational, handling and ageing factors. **Material.**

**Material broadening** — the Arabic admits considerations the English excludes, inviting answers the
English question would not.

**Register shift** — the Arabic moves the question out of the inventor-facing engineering register so
that a different *kind* of answer is invited. *Worked definition, from the adopted N-PF-4 repair:*
asking whether the idea works "on the ground" could invite cost, market or convenience answers rather
than physical capability. **Material.**

**Non-material (deferrable)** — wording, style or fluency differences that change neither the meaning,
the kind of answer invited, nor the decision quality. The declaration's own disposition:
*"لا تغيّر المعنى أو جودة القرار"*.

---

## §5. §L.2.1 recording limb (c) — the per-item comparison outcome

**Review universe, enumerated mechanically at this base — 34 items, matching the declaration's
"الـ34 substantive EN/AR pairs" exactly** `[EXEC]`: 21 committed `question_id` pairs carrying
`text` + `text_ar` in their own record (11 electronics + 10 mechanical), plus 13 identity-keyed
substantive asks in `web/ui_text.py::RVR7_SUBSTANTIVE_AR`. This is the D-RVR7-1 Option A
(Journey-Complete) scope.

**Disposition recorded — how to read it.** The Owner's declaration states one outcome over the whole
enumerated universe. It is recorded that way: a **uniform declaration-level disposition applied to
each of the 34 items**, traceable to the declaration alone. **No individualized per-item reviewer
commentary, reasoning, or score is recorded, because the Owner supplied none and inventing any would
be fabrication.**

`PER-ITEM OUTCOME (all 34): EQUIVALENT — ACCEPTED FOR USE` (uniform disposition, per §2)

| # | Domain / surface | Item | Outcome |
|---|---|---|---|
| 1–4 | electronics_electrical | `N-MC-1` … `N-MC-4` | EQUIVALENT — accepted for use |
| 5–6 | electronics_electrical | `N-PF-1`, `N-PF-2` | EQUIVALENT — accepted for use |
| 7 | electronics_electrical | **`N-PF-3`** | EQUIVALENT — accepted for use **after the adopted material-narrowing repair** |
| 8 | electronics_electrical | **`N-PF-4`** | EQUIVALENT — accepted for use **after the adopted technical-meaning-shift repair** |
| 9–11 | electronics_electrical | `N-BA-1` … `N-BA-3` | EQUIVALENT — accepted for use |
| 12–15 | mechanical | `mechanical:MECHANISM_COMPLETENESS:Q1` … `Q4` | EQUIVALENT — accepted for use |
| 16–17 | mechanical | `mechanical:PHYSICAL_FEASIBILITY:Q1`, `Q2` | EQUIVALENT — accepted for use |
| 18–21 | mechanical | `mechanical:BOUNDARY_AMBIGUITY:Q1` … `Q4` | EQUIVALENT — accepted for use |
| 22 | identity-keyed | `_STALL_REFRAME` | EQUIVALENT — accepted for use |
| 23 | identity-keyed | `_EXHAUSTED_EXIT_PROMPT` | EQUIVALENT — accepted for use |
| 24 | identity-keyed | `INTAKE_QUESTION` | EQUIVALENT — accepted for use |
| 25 | identity-keyed | `_CLOSING_Q` | EQUIVALENT — accepted for use |
| 26–28 | identity-keyed | `GENERIC:PROBLEM_MECHANISM_FIT:0..2` | EQUIVALENT — accepted for use |
| 29–31 | identity-keyed | `GENERIC:ASSUMPTION_INVENTORY:0..2` | EQUIVALENT — accepted for use |
| 32–34 | identity-keyed | `GENERIC:EXPERTISE_GAP_AWARENESS:0..2` | EQUIVALENT — accepted for use |

`ITEMS REVIEWED: 34 / 34` · `MISSING AR VARIANTS: 0` `[EXEC]` · `ITEMS REJECTED: 0`

---

## §6. §L.2.1 recording limb (d) — disagreements and ambiguities, left visible

**Not "none".** The declaration itself discloses a residual, and it is recorded here rather than
resolved silently:

**OBS-RVR7-LANG-1 — residual minor linguistic polish across the Arabic surface.** The Owner states
that minor linguistic improvements remain available and that they change neither meaning nor decision
quality (*"أي تحسينات لغوية طفيفة متبقية لا تغيّر المعنى أو جودة القرار"*), and approves deferring
them. Recorded as visible, non-material, and **DEFERRED by explicit Owner disposition** — not as a
defect, and not as a silent resolution.

- **Class:** wording/style polish only. Explicitly NOT a narrowing, broadening or register shift.
- **Owner:** the RVR-7 Arabic content surfaces (the two committed Path-N artifacts +
  `web/ui_text.py::RVR7_SUBSTANTIVE_AR`) — the existing owners; no new owner is created.
- **Trigger:** the next authorized touch of those Arabic content surfaces.
- **Latest safe gate:** before Serious Release.
- **Blocking level:** `NBF` — non-blocking, by the Owner's own materiality finding.
- **Does it block RVR-7 Formal Closure?** **NO.** §L.2 is a meaning standard, not a style standard;
  the declaration finds meaning and decision quality unaffected.
- **Explicitly NOT authorized by recording it:** no new semantic-repair cycle, no fresh
  implementation SHA for wording preference.

**No other disagreement or ambiguity was reported by the reviewer, and none is invented here.**

---

## §7. §L.2.1 satisfaction statement

| §L.2.1 limb | Status | Source |
|---|---|---|
| Human review | **SATISFIED** | §2 — personally performed, declared |
| Demonstrated bilingual EN/AR competence at the technical register | **SATISFIED** | §3 — demonstrated in use; no credential claimed or required |
| Independence from the Owner | **NOT REQUIRED** | §1 — absent from §L.2.1 |
| (a) competence basis recorded | **SATISFIED** | §3 |
| (b) explicit review standard recorded | **SATISFIED** | §4 |
| (c) per-item comparison outcome recorded | **SATISFIED** | §5 — 34/34, uniform declaration-level disposition, no fabricated per-item commentary |
| (d) disagreements/ambiguities left visible | **SATISFIED** | §6 — OBS-RVR7-LANG-1 recorded, deferred, not silently resolved |
| MT never the equivalence authority | **SATISFIED** | §2 — human review; the §2 English rendering is explicitly not the authority |

**`§L.2.1 SATISFIED: YES`** · **`§L.2 SEMANTIC PARITY — REVIEW REQUIREMENT: SATISFIED`**

**What this artifact does NOT do:** it does not close RVR-7, does not authorize RVR-8, does not
discharge W1-N1 or W1-N2 (their evidence is separate), and does not represent any review other than
the one actually supplied.
