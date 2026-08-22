# PVCG-R3-C — Semantic Stability Contract / Diagnosis Gate

**Status of THIS record:** governance/documentation-only **INCREMENT-CONTRACT CANDIDATE**. It becomes
AUTHORITATIVE only through the governed lifecycle (Creator Grill → independent external exact-candidate
review → Owner acceptance → SHA-preserving publication → PR → create-a-merge-commit → post-merge
verification). **It implements nothing** (ZERO runtime, test, fixture, pack, script, pin or deployment
diff in this candidate) and, once authoritative, authorizes ONLY the bounded **PVCG-R3-I**
implementation increment defined below — which itself requires separate explicit Owner authorization.

**Authoritative base:** `ca98099e29f6729c29e7612d67f9187dbd0dccb6` (PR #550 merge — PVCG-R2 formal
closure; re-fetched live from `origin/feature/atomic-json-session-persistence` before drafting and
independently re-verified on all four merge criteria: first parent
`1ce2c89630b9bdbfdedb15ee85eafa410a03632a`, second parent
`25cf419c3b21201fc6403d4a53301281af7a2071`, merge tree
`9bd7a1169072598b3804e16ee3bc04dea4faa313`, empty candidate→merge diff; zero commits after the tip;
working tree clean).

**`OWNER_DECISION_REGISTER.md` UNCHANGED.** This record declares no release readiness of any kind and
opens no downstream gate.

---

## §0. Evidence-class legend (binding on every statement below)

| Class | Meaning |
|---|---|
| **[REPO]** | Authoritative repository fact, citable to a committed file and location at the base SHA. |
| **[EXEC]** | **Creator-local executed diagnostic evidence** produced by a read-only run in this session against the base tree. It is reproducible by re-running the same probe against the same SHA, but it is **NOT** promoted to permanent repository fact by being recorded here. R3-I must re-measure independently. |
| **[OWNER]** | An Owner decision or directive. Not a repository fact. |
| **[OPEN]** | Unresolved; owed to a later gate. |

Nothing in this record may be read as a repository fact unless marked **[REPO]**.

---

## §1. Why this gate exists

**§1.1 Authorization provenance, stated precisely.** The Owner has authorized PVCG-R3 — Semantic
Stability — as the next remediation increment, limited at this stage to *source-of-truth
reconstruction → bounded diagnosis → governance contract candidate → freeze → Creator Grill*
**[OWNER]**.

**§1.2 A governance-truth disclosure about "PVCG" and the "Minimum Launch-Conformance Set."** At the
base SHA there is **no committed document that defines PVCG or enumerates the Minimum
Launch-Conformance Set** **[REPO]**. Stated with its search scope explicit: **within
`docs/governance/`**, `PVCG` appears only in `CURRENT_PROJECT_STATE.md`,
`ACTIVE_INCREMENT_CONTRACT.md`, `ACTIVE_EXECUTION_ROADMAP.md`,
`PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md` and `PVCG_R2_FORMAL_CLOSURE_RECORD.md`, none of which
defines it. `PVCG` does occur elsewhere in the repository — **57 occurrences across 23 further files** under
`engine/`, `web/` and `tests/` at this base — and **every one of them is a gate reference of the form
`PVCG-R<n>` / `PVCG_R<n>` / `pvcg_r<n>`** in a docstring, comment, test name or module path; filtering
those forms out leaves **zero** remaining occurrences, and none of the 57 is a definition **[EXEC]**.
The no-definition proposition is therefore unaffected by the wider scope.
`Minimum Launch-Conformance Set` appears only as a status line (`SATISFIED: NO`) plus the single
`[OWNER]`-classed sentence at `PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md` §1 **[REPO]**. The
statement "R3 belongs to the Minimum Launch-Conformance Set" is therefore **[OWNER]**, not **[REPO]**,
and this contract classifies it that way — exactly as R2-C classified the equivalent claim for R2.
Whether the Set should be committed as its own document is **[OPEN]** and is not resolved here.

**§1.3 The repository-side reason this gate exists.** `PVCG_R2_FORMAL_CLOSURE_RECORD.md` §7 (merged,
authoritative) states that R2 closure explicitly does **not** prove or imply semantic equivalence,
multilingual semantic stability, English/Arabic behavioural equivalence, or paraphrase equivalence, and
that "an answer expressing the same intent in other wording, or in another language, is treated as NOT
eligible; that is the authorized fail-closed direction and a **declared known bound**" **[REPO]**.
§10 of the same record names `PVCG-R3 — Semantic Stability` as the next workstream while authorizing
nothing **[REPO]**. `PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md` §5 lists "PVCG-R3 Semantic
Stability — and specifically **EN/AR equivalence remediation**" as an explicit R2 non-goal **[REPO]**.

R3 exists to close that declared bound, and nothing wider.

---

## §2. THE PROVEN DEFECT

All findings below were produced by read-only probes executed against the base tree in this session and
are classified **[EXEC]**. No repository file was modified, no fixture was added, and no test was
written to produce them. R3-I must reproduce them independently.

### §2.1 The governed interaction accepts Arabic, by design

* `web/app.py` `MAX_FREE_TEXT_CHARS` policy states: rejection is **length or embedded NUL only** —
  "Newlines, tabs, punctuation, **Arabic**, and all other legitimate Unicode pass untouched; there is
  NO general control-character sanitizer and NO ASCII-only rule" **[REPO]**.
* `web/ui_text.py` `SUPPORTED_LANGS = ("en", "ar")` with an RTL direction seam **[REPO]**.
* `web/templates/session.html` §D-P6-18 comment and markup: the canonical technical/system question
  **stays English in BOTH UI languages** and is rendered `lang="en" dir="ltr"`; the question text is
  not translated **[REPO]**.

So an Arabic-UI inventor is served an English question, is permitted to answer in Arabic, and that
answer reaches the governed seam unmodified. This is the premise that makes §2.2–§2.5 launch-material
rather than theoretical.

### §2.2 D-1 — Eligibility divergence: 6 of 6 governed gaps [EXEC]

Method: for each governed gap type, one materially equivalent English/Arabic answer pair, each run from
an **identical fresh starting state** (`IdeaState`, `domain=mechanical`, `path=N`, `iteration=1`, the
served gap present and `OPEN`) through the canonical seam
`engine.progression_loop.integrate_response(state, gap_type, QUESTIONS[gap_type][0], answer)`.

| Served gap | EN eligible | AR eligible | EN gap status after | AR gap status after |
|---|---|---|---|---|
| `MECHANISM_COMPLETENESS` | True | **False** | `PARTIAL` | **`OPEN`** |
| `PHYSICAL_FEASIBILITY` | True | **False** | `PARTIAL` | **`OPEN`** |
| `BOUNDARY_AMBIGUITY` | True | **False** | `PARTIAL` | **`OPEN`** |
| `PROBLEM_MECHANISM_FIT` | True | **False** | `PARTIAL` | **`OPEN`** |
| `ASSUMPTION_INVENTORY` | True | **False** | `PARTIAL` | **`OPEN`** |
| `EXPERTISE_GAP_AWARENESS` | True | **False** | `PARTIAL` | **`OPEN`** |

`GAPS WITH MATERIAL EN/AR DIVERGENCE: 6/6` **[EXEC]**.

Worked example — served gap `MECHANISM_COMPLETENESS`, identical starting state:

* **EN:** "When the user presses the handle, the lever rotates and drives a spring-loaded latch, which
  opens the valve in three steps."
* **AR:** "عندما يضغط المستخدم على المقبض، تدور الذراع وتدفع مزلاجًا مزودًا بنابض، فيفتح الصمام على ثلاث خطوات."

| Material outcome | EN | AR |
|---|---|---|
| eligibility (`addresses_gap`) | `True` | **`False`** |
| quality (`assess_response`) | `REASONED` | **`ASSERTED`** |
| transition result | `WARN` | `WARN` |
| gap status after | `PARTIAL` | **`OPEN`** |
| `known_mechanism` established | `True` | **`False`** |
| `known_problem` established | `True` | **`False`** |
| reason classification | *partially addressed* | ***not addressed*** |

Cause **[REPO]**: `engine/gap_relevance.py` `_INTENT_WORDS` / `_INTENT_PHRASES` contain **264 declared
entries, all Latin-script English**, drawn verbatim from the vocabulary of the six governed questions;
`addresses_gap` matches phrases by substring and words by token over `re.compile(r"[a-z0-9]+")`. No
Arabic surface can match any entry, so `addresses_gap` returns `False` for every Arabic input and
`integrate_response` takes its fail-closed exit, leaving gap status untouched.

### §2.3 D-2 — Quality ceiling: an Arabic-only inventor can never close a gap [EXEC] — the decisive finding

Structural facts **[REPO]**: `engine/progression_loop.py` reaches `REASONED` only through
`_has_causal_structure` (32 `_CAUSAL_STRUCTURE_PATTERNS`), the Layer-2
`_connective_whole_word_substance_gate`, and the per-domain substance signals served by
`engine/domain_rules.py` from the committed packs. Measured **[EXEC]**: all 32 causal-structure
patterns are ASCII, all 15 `mechanical` substance signals are ASCII, and all 53
`electronics_electrical` substance signals are ASCII. Consequently, for a pure-Arabic answer
`_has_causal_structure` is `False` and the connective gate is `False`, so `assess_response` returns
`ASSERTED` unconditionally. Four substantive Arabic mechanism answers (97–100 chars, all well past
`MIN_REASONED_RESPONSE_LENGTH = 40`) all returned `ASSERTED`; the same holds for
`electronics_electrical` **[EXEC]**.

`integrate_response` closes a gap only on `REASONED` (from `PARTIAL`) or `DEMONSTRATED`, and
`DEMONSTRATED` is unreachable from `assess_response` at this tip (`progression_loop.py:703` —
`return ASSERTED  # DEMONSTRATED requires external evidence — not in MVP`) **[REPO]**. Therefore the
`ASSERTED` ceiling is a **hard progression block**.

Executed proof — eight iterations, same served gap, same domain, rotating substantive answers **[EXEC]**:

| | iter 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | gap ever `CLOSED`? |
|---|---|---|---|---|---|---|---|---|---|
| **Arabic** | `OPEN` | `OPEN` | `OPEN` | `OPEN` | `OPEN` | `OPEN` | `OPEN` | `OPEN` | **NO** |
| **English (control)** | `PARTIAL` | **`CLOSED`** | `CLOSED` | `PARTIAL` | **`CLOSED`** | `PARTIAL` | `PARTIAL` | **`CLOSED`** | YES (first at iter 2) |

**This is why the defect is launch-material.** It is not a wording difference and not a confidence
difference: an inventor who answers in Arabic cannot advance a single gap, cannot advance maturity, and
therefore cannot reach any downstream surface that depends on gap closure. Closing D-1 alone does not
remove this block — see §13.

### §2.4 D-3 — Hidden side effect divergence: the acknowledged-unknown parallel track [EXEC]

`engine/progression_loop.py` `_ACKNOWLEDGED_UNKNOWN_MARKERS` holds **18 markers, all ASCII** **[REPO]**,
and `_detect_acknowledged_unknown` runs **unconditionally**, before and independent of the R2
fail-closed exit **[REPO]**. Measured with equivalent explicit self-declared unknowns **[EXEC]**:

* EN "I do not know the exact spring tension that the latch will need in practice." → detected, basis
  `i do not know`.
* AR "لا أعرف قيمة شدّ النابض الدقيقة التي سيحتاجها المزلاج في الاستخدام الفعلي إطلاقًا." → **not detected**.

The same divergence applies to `_WEAK_PATTERNS` (15 entries, all ASCII) **[REPO]**. An Arabic inventor's
explicitly stated unknown is therefore never recorded in the acknowledged-unknown track — a divergence
in a **hidden side effect**, not merely in a displayed outcome.

### §2.5 D-4 — The divergence is not even disclosed, and the disclosure that exists is English-only [EXEC]

* `web/result_feedback.py` `get_result_feedback` maps WARN reasons by stable substrings; the R2 reason
  "`… not addressed — this answer does not respond to the question that was asked`" matches **none** of
  the specific branches and falls to the conservative fallback: *"This point cannot move forward yet.
  Review the result details for the specific reason."* **[EXEC]** — which does not identify language as
  the cause.
* `web.ui_text.localize_message` returns that fallback, and the raw engine reasons, **unchanged for
  `lang="ar"`** — they are English-only **[EXEC]**.

So the Arabic inventor is neither progressed nor told why. This is the situation the Owner's R3
principle addresses directly: disclosure alone would be insufficient, and at the base SHA even the
disclosure is absent.

---

## §3. WHAT IS **NOT** A DEFECT — negative diagnosis (equally binding)

R3-I must not "repair" any of the following. Each was measured, not assumed.

**N-1 — Latin/English normalization is ALREADY stable; R3 adds none.** Eight normalization variants of
one English answer (uppercase, punctuation stripped, doubled spaces, leading/trailing whitespace,
Unicode NFD, curly apostrophe, hyphen→space, non-breaking spaces) produced an **identical** material
outcome tuple to the base in **8/8** cases **[EXEC]**. Adding Latin casing/punctuation/Unicode
normalization to R3 would be unjustified surface area. Classification: **C — cosmetic, no action.**

**N-2 — Arabic-internal normalization is NOT currently a divergence source.** Seven Arabic variants
(bare-alef folding, tatweel insertion, diacritic stripping, NFD, teh-marbuta→heh, yeh→alef-maqsura)
produced outcomes **identical to the Arabic base** **[EXEC]** — because Arabic recognition is uniformly
zero, so every Arabic string is equally unrecognised. It is therefore **false** to claim an Arabic
normalization defect exists today. Arabic normalization becomes material **only conditionally**, the
moment R3-I registers any Arabic surface. §9 governs it on that conditional basis and on no other.
Classification: **D today → mandatory bounded governance in R3-I.**

**N-3 — Arbitrary English paraphrase is expected lexical boundedness, not an R3 defect.** An English
paraphrase carrying no governed intent vocabulary ("Pushing the grip makes the arm swing round, which
lets go of the catch held by a coiled wire, so the flap swings wide.") is `relevant=False`, gap stays
`OPEN` **[EXEC]**. This is the declared R2 bound behaving exactly as declared, and the Owner's
directive states explicitly that arbitrary-paraphrase understanding must not be promised. R3 does
**not** undertake to stabilise unregistered English paraphrase. Classification: **B — expected lexical
boundedness.**

**N-4 — A single embedded English token flipping an Arabic answer is a collision risk to GUARD, not a
divergence to fix.** The Arabic mechanism answer with its final word replaced by the English token
`steps` becomes `relevant=True`, gap `PARTIAL`, `known_mechanism=True` **[EXEC]**. This is the lexical
mechanism working as designed; it becomes dangerous only once Arabic surfaces exist alongside English
ones. Classification: **C today → mandatory adversarial category in R3-I (§10.2).**

**N-5 — R3 is not required to make the two languages byte-identical.** The raw reason strings embed the
gap-type token and are English-only; requiring byte equality would be a false success criterion. §7
defines equality over the material outcome set instead.

---

## §4. THE R3 PRODUCT TRUTH (frozen by this contract)

> Within the **governed equivalence boundary** defined in §5, two inputs that activate the same
> governed concept set for the served gap MUST produce the same **material progression outcome**
> defined in §7, whether they are written in English or in Arabic, from the same authoritative
> starting state and the same served gap.
>
> Outside that boundary the system makes **no** equivalence claim of any kind. The R2 fail-closed
> direction is preserved and extended verbatim: **uncertain equivalence ≠ satisfied**. A widening
> mechanism may only ever widen recognition **inside** an explicitly registered, provenance-traced
> equivalence class; it may never create a generic "this looks technical, therefore it is relevant"
> escape hatch, and it may never convert an ineligible answer into a `BLOCK`, a contradiction, or an
> input-validation failure.

R3-I must describe the delivered mechanism **truthfully**: if it is a registered bilingual concept
mapping, it must be called that, and its inability to handle unregistered wording must be stated as a
known bound — not concealed and not framed as understanding meaning. R3 must not claim universal
language understanding, arbitrary paraphrase understanding, or semantic equivalence beyond what the
implementation deterministically decides.

---

## §5. "MATERIALLY EQUIVALENT" — the executable bounded definition

Vague formulations such as "the same meaning" are **prohibited** as the operative definition. R3 defines
equivalence **by construction**, so that it is decidable by table lookup and auditable by inspection.

**§5.1 The governed concept.** A *governed concept* is a record with:

1. a stable `concept_id`;
2. exactly one **owning governed gap family** (one of the six frozen gap types);
3. a **provenance reference** to the specific governed question text in
   `engine.progression_loop.QUESTIONS` (or the domain pack question artifact) from which the concept is
   drawn — a concept with no governed-question provenance MUST NOT be registered;
4. an **English surface set** and an **Arabic surface set**, each surface tagged `word` or `phrase`;
5. a declared `match_mode` per surface (token for `word`, substring for `phrase`) — see §9.3.

**§5.2 Activation.** For input `x` and gap `G`, `activated(x, G)` is the set of `concept_id`s owned by
`G` for which at least one registered surface matches `x` under that surface's `match_mode`, after the
bounded normalization of §9.

**§5.3 Governed equivalence (the operative definition).** Two inputs `x` and `y` are
**governed-equivalent for gap `G`** if and only if `activated(x, G) == activated(y, G)` **and** both
carry the same **structural class** membership defined in §5.4. Equivalence is a property of registered
concept activation — never of unregistered wording, never of similarity, never of length, and never of
a model's opinion.

**§5.4 Structural classes (required because eligibility alone does not close D-2).** In addition to
intent concepts, R3-I must register:

* a **causal-structure class** — the governed Arabic counterparts of the existing English
  `_CAUSAL_STRUCTURE_PATTERNS` role, each traced to the construction it mirrors;
* a **domain-substance class** — the governed Arabic surfaces for the *already-committed* per-domain
  substance signals, one-to-one with an existing pack signal and adding **no new signal concept**.

Registering an Arabic surface for an existing signal is a *surface* addition, never a new substance
concept and never a domain-capability change. **A pack MUST NOT gain a new substance signal, and no
domain may be activated, recognised, or re-scoped by R3.**

**§5.5 What equivalence is NOT.** Not translation quality; not paraphrase; not synonymy in general; not
transliteration; not edit distance; not embedding proximity; not "both answers are on topic". Anything
not registered is, by definition, not governed-equivalent, and the fail-closed direction applies.

**§5.6 Minimum required classes.** R3-I must determine the minimum class set from repository truth
(the six governed questions and the committed pack signals) and must justify each registered concept by
its provenance reference. **Inventing a concept that no governed question expresses is prohibited.**

---

## §6. Deterministic mechanism constraints

**§6.1 Required.** `R3 DETERMINISTIC: YES`. Same authoritative starting state + same served gap + same
normalized input MUST yield the same material outcome, on every run, in every process.

**§6.2 Prohibited without a separate Owner authorization** — the contract preserves this boundary
explicitly and R3-I must state each as a fact of the delivered code:

```
LLM ADDED: NO
EMBEDDINGS ADDED: NO
VECTOR STORE ADDED: NO
EXTERNAL NLP SERVICE ADDED: NO
PROBABILISTIC SEMANTIC CLASSIFIER ADDED: NO
MODEL-BASED ADJUDICATION ADDED: NO
```

Also prohibited: network calls, clock reads, randomness, filesystem writes at decision time, hidden
state, per-sentence special-casing, machine-learned weights, statistical thresholds, stemming, fuzzy
matching, transliteration inference, and edit-distance semantics.

**§6.3 Extensibility without lock-in.** The registry must be a plain committed data structure in the
repository, readable and diffable, with no vendor dependency and no external service. Adding a third
language later must be a governed data addition, not an architectural change. R3 authorizes **no**
third language.

**§6.4 Candidate mechanisms.** The mechanism is not pre-selected by this contract beyond the §5
structure. R3-I may realise §5 as governed bilingual canonical aliases, a canonical concept-token
registry, registered phrase families, or question-scoped concept equivalence sets — provided every
§5.1 field is present, every §6.2 prohibition holds, and §10 passes.

---

## §7. THE MATERIAL PROGRESSION OUTCOME SET (the executable success condition)

**§7.1 Compared fields.** For governed-equivalent inputs from the same starting state and the same
served gap, these MUST be equal:

| # | Field | Source |
|---|---|---|
| 1 | eligibility | `engine.gap_relevance.addresses_gap(answer, gap_type)` |
| 2 | quality tier | `engine.progression_loop.assess_response(answer, domain)` |
| 3 | transition result | `integrate_response(...)[0]` — `PASS` / `WARN` / `BLOCK` |
| 4 | reason **classification** | the branch selected by `web.result_feedback.get_result_feedback` (see §7.2) |
| 5 | served gap `status` after | `OPEN` / `PARTIAL` / `CLOSED` |
| 6 | served gap `closed_at` set-or-unset | `Gap.closed_at is None` |
| 7 | Stage-3 gap evidence append count | `len(gap.evidence)` delta |
| 8 | `known_mechanism` established | `state.known_mechanism is not None` |
| 9 | `known_problem` established | `state.known_problem is not None` |
| 10 | acknowledged-unknown append count | `len(state.acknowledged_unknowns)` delta |

**§7.2 Deliberately NOT required equal** (legitimate metadata difference, per the Owner's directive):
the **byte content** of the raw reason string (it is English-only and embeds the gap-type token); the
stored verbatim answer text; record ids; iteration counters; and any timestamp. Field 4 compares the
reason's **classification**, not its bytes — because the classification is what reaches the user.

**§7.3 The success condition.** For every registered equivalence class `C`, every governed gap `G` that
owns a concept in `C`, and every pair `(x, y)` of registered surfaces of `C`:

> `same authoritative starting state` + `same served gap G` + `x` governed-equivalent to `y`
> ⟹ all ten fields of §7.1 are equal.

**§7.4 Scope of the guarantee.** The guarantee is asserted **only** over registered classes. R3-I must
publish the registered class inventory as part of its evidence so the guarantee's exact extent is
auditable, and must state the residual — unregistered wording in either language — as a known bound.

---

## §8. USER-VISIBLE BEHAVIOUR IN SCOPE

R3 governs actual progression behaviour, not internal matching alone. In scope: eligibility, quality
outcome, gap state transition, the hidden side effects of §7.1 fields 7–10, and the reason
classification that reaches `result_feedback`.

**Out of scope, explicitly:** next-question *selection* logic, question skip / reorder / add, full
adaptive questioning, conversation-level semantics, WS10 / WS11 / WS12 activation, `stage3_evaluator`
integration, and any change to `get_display_question`'s inputs
(`domain, gap_type, iterations_open, path`).

**§8.1 A bounded disclosure obligation (necessary, not sufficient).** Because §7.4 leaves a real
residual, R3-I must ensure that a not-eligible outcome is not silently misreported. At minimum the R2
reason must reach a truthful, specific `result_feedback` classification rather than the conservative
unknown-reason fallback (§2.5), and any user-facing wording R3-I introduces must be available in both
supported UI languages through the existing `web/ui_text.py` seam. **Disclosure does not substitute for
the §7.3 guarantee** — it accompanies it.

---

## §9. NORMALIZATION BOUNDARY

**§9.1 Latin / English: NO normalization is added.** Justified by N-1 (8/8 variants already stable)
**[EXEC]**. R3-I must not add Latin casing, punctuation, whitespace or Unicode normalization.

**§9.2 Arabic: a bounded, conditional, evidence-gated set.** Because N-2 shows Arabic normalization is
non-material *today*, each transformation below is authorized **only if R3-I demonstrates by execution
that omitting it causes two registered surfaces of the same concept to diverge on §7.1**:

| Transformation | Disposition |
|---|---|
| Unicode NFC | **Authorized** (canonical form; prerequisite for stable comparison) |
| Tatweel (`U+0640`) removal | **Authorized on demonstrated necessity** |
| Arabic diacritics / harakat removal (combining marks) | **Authorized on demonstrated necessity** |
| Alef variants `أ إ آ ٱ` → bare `ا` | **Authorized on demonstrated necessity** |
| Teh marbuta `ة` → `ه` | **NOT authorized by default** — lossy; may only be proposed with an explicit collision analysis and a separate governed decision |
| Yeh `ي` → alef maqsura `ى` (or the reverse) | **NOT authorized by default** — same condition |
| Arabic-Indic digits → ASCII digits | **NOT authorized** — no evidence of necessity at this tip |

**§9.3 Token boundary — a direct inheritance of R2 residual 3.** Arabic attaches clitics (`و`, `ال`,
`ب`, `ل`, `ك`, `ف`, pronominal suffixes) without spaces, so a naive substring rule over Arabic surfaces
will over-match far more aggressively than the English tables do. R3-I MUST:

* declare `match_mode` per surface and justify every `substring` choice;
* apply the R2 lesson literally — **a phrase→word containment argument is unsound**, because phrases
  match by substring and words by token (`PVCG_R2_FORMAL_CLOSURE_RECORD.md` §6) **[REPO]**;
* prove token-boundary behaviour for Arabic surfaces by execution, including token-dissolving
  adversarial inputs, exactly as the R2-I marker-coverage suite does for English.

**§9.4 Absolutely prohibited:** stemming, lemmatization, root extraction, fuzzy matching, edit distance,
transliteration inference, soundex-style matching, and any statistical tokenizer.

---

## §10. FALSE-POSITIVE PROTECTION — R2 MUST NOT REGRESS

**§10.1 Preserved R2 properties (each must be re-proven GREEN by R3-I, not assumed).**

| Property | Preservation requirement |
|---|---|
| Gap-specific relevance | The authoritative 6×6 **closure** control (`test_each_genuine_answer_closes_only_its_own_gap`) must stay GREEN, and its Arabic / mixed-language counterparts over registered surfaces must produce no off-diagonal **closure or satisfaction**. Not a zero-eligibility requirement — see §16.1. |
| Cross-gap protection | No registered R3 surface may create a cross-gap satisfaction or closure path that does not exist at the authoritative base (differential, *no new leakage*). Pre-existing English off-diagonal eligibility is out of scope (§14 residual 1). |
| Repetition protection | Re-submitting the same answer must not manufacture additional progression. |
| Fail-closed | Unregistered / uncertain / unrecognised ⇒ **not eligible**, never eligible-by-default. |
| Non-punitive rejection | Ineligibility never becomes `BLOCK`, a contradiction, or an input-validation failure; the answer is still recorded and its assessed quality is unchanged. |
| Determinism | §6.1. |
| R1 durable epistemic memory | §11. |
| P9-MECH-I3/I4/I5 pins | §13. |

**§10.2 Mandatory adversarial categories.** R3-I must include explicit tests for each, and must fail
closed wherever a mapping creates unsafe ambiguity:

1. **Translation collisions** — one Arabic surface that plausibly renders concepts in two different gap families.
2. **Synonym collisions** — two concepts in the same family whose surfaces overlap.
3. **One concept, multiple gaps** — a concept that a governed question expresses in more than one family; it must be registered to exactly one owner or fail closed.
4. **Technical nouns appearing off-topic** — the Arabic analogue of the R2 `battery` surface question.
5. **Negation** — "لا يعمل بأي خطوات" and the English "It does not work by any steps"; measured at the base tip, the English negated form is already `relevant=True` **[EXEC]**, so R3-I must not *worsen* this and must state truthfully whether it changes.
6. **Uncertainty and "I don't know"** — including the D-3 case; measured at the base tip, "I don't know how it works yet, honestly." is already `relevant=True` for `MECHANISM_COMPLETENESS` **[EXEC]**.
7. **Contradicted statements.**
8. **Cross-gap answer reuse** — full off-diagonal, both languages and mixed, measured against the closure/satisfaction property defined in **§16.1**, not against a zero-eligibility property (which does not hold at the base).
9. **Mixed English/Arabic answers** — mandatory because of N-4; a one-token flip must be characterised, not discovered later.
10. **Substring / token ambiguity** — §9.3, including token-dissolving forms.
11. **Empty / whitespace-only input** — must remain not eligible (verified at the base tip **[EXEC]**).

**§10.3 Coverage adequacy — the T-1 / T-1b lesson is binding.** `PVCG_R2_FORMAL_CLOSURE_RECORD.md` §6
records that a finite corpus cannot establish mutant equivalence and that a phrase→word containment
proof is unsound **[REPO]**. R3-I therefore MUST:

* generate probes from a **declared registry inventory**, never from the live tables (a probe generated
  from the live table vanishes with the entry it protects);
* machine-validate probe **isolation** (no probe may carry a second same-family surface or any
  foreign-family surface) and refuse at collection otherwise;
* run a **complete single-entry mutation sweep** over every operative registered surface with bytecode
  caching disabled and an explicit load-verification delta guard;
* **never** declare a surviving mutant an equivalent mutant on finite-corpus evidence.

---

## §11. R1 PRESERVATION

`PVCG-R1 — Durable Epistemic Memory` is authoritative (PR #547, merge `c70bad19…`) **[REPO]**. R3-I MUST
keep the five governed non-answer dispositions (`unknown`, `deferred`, `provisional_assumption`,
`specialist_requested`, `evidence_requested`) persisting and reconstructing with their recorded meaning,
MUST leave `tests/test_pvcg_r1_durable_epistemic_memory.py` **byte-unchanged**, and MUST report the R1
focused suite GREEN (26/26) on the exact frozen candidate. R3 introduces no schema change, no migration,
and no change to `engine/record_contract.py` `_ASSERTION_FIELDS`.

---

## §12. R2 PRESERVATION

R3 sits **on top of** R2 and must not reintroduce manufactured satisfaction. The R2 product truth
(`PVCG_R2_C_GAP_RELEVANCE_HARDENING_CONTRACT.md` §4) remains binding verbatim **[REPO]**: generic
technical substance, domain vocabulary, causal language or signal density alone remain insufficient to
establish satisfaction for an unrelated gap. R3-I must report the R2 behavioural suite and the marker
coverage suite GREEN on the frozen candidate, and must state explicitly whether either test file
changed and why.

---

## §13. PIN AND CONTRACT IMPACT ANALYSIS

Measured at the base SHA **[REPO]** / **[EXEC]**:

| File | Live digest | Pinned in |
|---|---|---|
| `engine/progression_loop.py` | **RECONCILED BY PVCG-R3-I** — was `07c9bff500662de54ac0f7388c1f2e13a721549c6f4943cde865b98a22c525d6` at this contract's base; the live digest is now `3cbd76849c0f572191a552db1a41a8cd418d02fac1d59d9b8804c72883239a55`, updated in all three ENFORCING locations in the R3-I candidate under §13.2/§13.2a. | **3 ENFORCING** locations: `test_p9_mech_i3_signal_quality.py`, `test_p9_mech_i4_boundary_corpus.py`, `test_p9_mech_i5_question_sufficiency.py`. The same digest is additionally **recorded** (not enforced) in active governance surfaces and in historical entries — see **§13.2a**, which separates the three kinds and states which must be synchronized and which must not be rewritten. |
| `engine/domain_rules.py` | `0e47326ad92a6e5b0a63eb06db9e3ad96ae72c9aaf64471dd21621265b1db1ab` | the same 3 files |
| `engine/path_n_questions.py` | `a1a682d38293defd4b351e6238aeb870b4f765eaf3fc0f105c4932f75286ce7f` | I5 |
| all five `domains/*/domain.json` | see `_FROZEN_PACK_SHA256` in I3/I4 | **I3 pins 4** (`electronics_electrical`, `medical_device`, `software`, `iot_electronics` — deliberately **not** `mechanical`) / **I4 pins all 5** (adds `mechanical` `901dd718…`) |
| mechanical pack fields outside the two authorized signal lists | `_FROZEN_MECH_FIELDS` in I3 — `gap_type_mappings` `857820ed…`, `aliases` `bc7f35e4…` | I3 |
| `engine/gap_relevance.py` | `773a10acb31dc1595a35540b1431346858ca98a2676b711e504ffcd19bb7dbfd` | **NOT byte-pinned anywhere** — no `_FROZEN_*` table in `tests/` holds this digest (a search of `tests/` returns no match) **[EXEC]**. Its only occurrences in the repository are the two descriptive governance references introduced by this candidate itself (this table and the roadmap entry), neither of which enforces anything. |

**§13.1 The consequence, stated plainly.** Closing **D-1** (eligibility) can be done inside
`engine/gap_relevance.py` plus a new registry module and moves **no pin**. Closing **D-2** — the
decisive launch-material finding — cannot, because the `ASSERTED` ceiling is produced by
`assess_response` inside the **pinned** `engine/progression_loop.py`. **R3-I therefore requires a pin
movement, and this contract does not pretend otherwise.**

**§13.2 Bounded pin-reconciliation rule (binding on R3-I).**

* **Exactly one** engine pin may move: `engine/progression_loop.py`.

**§13.2a — two distinct kinds of location hold this digest; R3-I must synchronize both, and must not
confuse them.**

| Kind | What it is | Locations at this base | R3-I obligation |
|---|---|---|---|
| **(1) ENFORCING pin locations** | `_FROZEN_ENGINE_SHA256` entries whose assertion fails when the file changes | exactly **3**: `tests/test_p9_mech_i3_signal_quality.py`, `tests/test_p9_mech_i4_boundary_corpus.py`, `tests/test_p9_mech_i5_question_sufficiency.py` | **MUST** be updated to the new digest, all three **in the same candidate**, simultaneously and disclosed — never one at a time, never silently. Missing one leaves the suite RED. |
| **(2) ACTIVE CURRENT-TRUTH governance references** | prose in a live status surface that records the digest as *currently* in force, so it goes stale the moment the pin moves | `ACTIVE_INCREMENT_CONTRACT.md`, `ACTIVE_EXECUTION_ROADMAP.md`, `CURRENT_PROJECT_STATE.md`, and this contract's own §13 table | **MUST** be synchronized in the same implementation candidate. These fail no test, so nothing catches them automatically — an R3-I that updates only the three enforcing pins leaves a green suite and a false governance record. |
| **(3) HISTORICAL records — do NOT rewrite** | append-only roadmap gate entries, `Superseded (retained as history)` blocks, and the merged `PVCG_R2_FORMAL_CLOSURE_RECORD.md` §4 evidence row | the remaining occurrences | **MUST be left byte-unchanged.** They record what was true at their own gate and are not current-truth claims. Rewriting them would falsify history and is outside this contract. |

R3-I must state, in its own evidence, the old digest, the new digest, and the exhaustive list of
locations it changed under (1) and (2) together with the locations it deliberately left unchanged
under (3). An R3-I candidate that reports "all three pin locations updated" **without** addressing
kind (2) has not completed the reconciliation.
* `engine/domain_rules.py`, `engine/path_n_questions.py`, **all five pack digests** and I3's
  `_FROZEN_MECH_FIELDS` (`gap_type_mappings`, `aliases`) **MUST remain byte-identical.** The Arabic
  causal-structure and substance surfaces therefore live in the new unpinned R3 registry module and are
  *consulted* by `progression_loop.py`; they are **not** added to the packs and **not** added to
  `domain_rules.py`. A pack edit of any kind is outside R3 and would additionally re-open pack-pin and
  domain-capability questions this contract does not authorize.
* RED must be established **before** any pin is touched, at the authoritative base, and must
  demonstrate the §7.1 divergence — not merely a digest mismatch. A pin reconciliation whose only
  justification is "the file changed" is not acceptable.
* The reconciliation must state the old digest, the new digest, the three locations, and the reason,
  and must include a diff-scope statement showing the edit is confined to the seam R3 governs.
* **No pin is changed by THIS candidate.** Expected pin diff here: `0`.

**§13.3 Contract impact.** R3-I changes no other governed contract. `PVCG_R2_C_...` §4 and
`PVCG_R2_FORMAL_CLOSURE_RECORD.md` §7 remain authoritative and unamended; §7 of the closure record
declares a bound that R3 *closes within its registered boundary* and does not contradict.

---

## §14. R2 RESIDUAL CLASSIFICATION (inputs to R3, not automatic repair scope)

The seven residuals of `PVCG_R2_FORMAL_CLOSURE_RECORD.md` §8 **[REPO]**, each classified. **Listing a
residual here authorizes no work on it.**

| # | Residual | Classification | Basis |
|---|---|---|---|
| 1 | Lexical cross-talk between families | **DIRECTLY MATERIAL TO R3** | Adding a second script multiplies the cross-talk surface. Measured at the base tip: a single sentence already activates **2** families in two independent probes **[EXEC]**. §10.2/1–3 governs it. |
| 2 | Broad `"does not"` / `"doesn't"` boundary phrases | **DIRECTLY MATERIAL TO R3** | Their Arabic counterparts (`لا`, `ليس`, `لم`, `لن`) are far broader than the English forms and must not be mirrored naively. Measured: "It does not matter much." and "This doesn't apply here." are both already `BOUNDARY_AMBIGUITY`-eligible; "I do not know." is not **[EXEC]**. R3 must not widen this in Arabic; the **English** breadth itself is NOT reopened. |
| 3 | Substring/token boundary asymmetry | **DIRECTLY MATERIAL TO R3** | §9.3. Arabic clitic attachment makes this the single highest false-positive risk in the increment. Re-verified at the base tip: `"zstep by stepz"` matches the phrase, `"zstepz"` does not match the word **[EXEC]**. |
| 4 | WS1 helper coupling in the corrected journey fixtures | **ADJACENT — OUT OF SCOPE** | Test-harness structure only; no bearing on EN/AR equivalence. |
| 5 | Acknowledged-unknown fixture coverage shift | **ADJACENT — OUT OF SCOPE** | The *fixture* shift is out of scope. Note carefully: the English-only `_ACKNOWLEDGED_UNKNOWN_MARKERS` table is a **separate, newly measured R3 finding (D-3)** and IS in scope — the two must not be conflated. |
| 6 | `battery` as a question-derived marker | **ADJACENT — OUT OF SCOPE for English** | Investigated under R2 and found not to be a defect. Re-measured: "The battery is red." is `PHYSICAL_FEASIBILITY`-eligible **[EXEC]**. R3 does not reopen the English surface; it must, however, avoid creating the same shape in Arabic without an explicit off-topic-noun guard (§10.2/4). |
| 7 | `test_progression_benchmark.py::test_B1` passes for a different reason | **NO ACTION** | Declared under R2; unrelated to equivalence. |

R3 does **not** silently absorb residuals 1–3: it inherits them as *constraints on its own design*, and
must not present improvement of the English tables as R3 work.

---

## §15. REQUIRED R3-I RED / GREEN SHAPE

**§15.1 RED, at the authoritative base, before any implementation byte.** R3-I must independently
reproduce, at minimum:

* D-1 across **all six** governed gaps, with the starting state, served gap, both inputs, and the full
  §7.1 tuple recorded per gap;
* D-2 by the multi-iteration closure proof — Arabic never `CLOSED`, English control `CLOSED`;
* D-3 for the acknowledged-unknown track;
* D-4 for the reason classification and its localization state.

RED must be genuine: manufactured RED (a test written to fail for a reason other than the defect) is a
rejection condition, and any test that passes for an unrelated reason must be declared.

**§15.2 GREEN.** Every §7.1 field equal for every registered class (§7.3); every §10.1 property
re-proven; every §10.2 category tested; every negative control (§16) holding.

**§15.3 Mutation / adversarial adequacy.** §10.3 in full, with the sweep result reported as
`processed / killed / survived / skipped / LOADFAIL` and a byte-identical restore count.

**§15.4 Regression.** The targeted R2 + R1 + P9 pin suites, the universal guardrail smoke
(`python3 scripts/run_universal_smoke.py` → `UNIVERSAL GUARDRAIL SMOKE: PASS`), and the full suite.

---

## §16. NEGATIVE CONTROLS (binding — "equivalent behaves equivalently" must not become "anything similar is accepted")

R3-I must prove that **non**-equivalent inputs remain distinguishable. At minimum:

1. **Cross-gap, both languages and mixed — stated against the property the repository actually has.**
   The authoritative R2 control is
   `tests/test_pvcg_r2i_gap_relevance.py::test_each_genuine_answer_closes_only_its_own_gap` **[REPO]**,
   which asserts, over the curated `GENUINE` corpus with `times=2`, that the diagonal **closes** and
   that the off-diagonal set of **CLOSED** gaps is empty — a property over **closure**, not over
   eligibility. R3-I must preserve exactly that, and must extend it to the languages R3 registers:
   * the authoritative 6×6 **closure** control must stay GREEN, and its Arabic and mixed-language
     counterparts over registered surfaces must produce **no off-diagonal closure and no off-diagonal
     satisfaction** (no `known_mechanism` / `known_problem` establishment, no Stage-3 evidence append)
     for an answer registered to a different gap family;
   * **no registered R3 surface may create a cross-gap satisfaction or closure path that does not exist
     at the authoritative base** — the R3 obligation is *no new leakage*, measured differentially
     against the base;
   * unregistered surfaces in either language remain fail-closed under the existing bounded R2 model
     (§4, §5.5, §7.4).

   **This control deliberately does NOT require zero off-diagonal *eligibility*, because that property
   does not hold at the authoritative base and the repository has never claimed it.** Measured this
   gate over ordinary (non-curated) English answers: **2** off-diagonal eligible activations
   — `PHYSICAL_FEASIBILITY` answer eligible for `BOUNDARY_AMBIGUITY`, and `EXPERTISE_GAP_AWARENESS`
   answer eligible for `PHYSICAL_FEASIBILITY` **[EXEC]**; the independent reviewer measured **6** with
   a different corpus, and over the curated `GENUINE` corpus the count is **0** **[EXEC]**. The count
   is corpus-dependent, which is precisely why a universal zero-eligibility requirement would be
   unsound. Requiring it would (a) assert a property the base does not satisfy, (b) manufacture RED out
   of the pre-existing, R2-accepted English lexical cross-talk recorded at §14 residual 1, and
   (c) implicitly reopen the English marker tables, which §14 forbids. **R3-I must not treat existing
   English off-diagonal eligibility as a defect to repair.**
2. **Unregistered Arabic wording** — an Arabic answer carrying no registered surface must remain **not
   eligible**; a general "it is Arabic and technical, therefore accept" behaviour is a rejection
   condition.
3. **Unregistered English paraphrase** — must remain not eligible (N-3); R3 must not accidentally widen
   English while adding Arabic.
4. **Empty and whitespace-only** — not eligible (holds at the base tip **[EXEC]**).
5. **Off-topic answer to the served gap** — an expertise answer served against `MECHANISM_COMPLETENESS`
   must remain not eligible in **both** languages (holds in English at the base tip **[EXEC]**).
6. **A near-miss surface** — a string differing from a registered Arabic surface by a governed
   normalization step that §9.2 did **not** authorize must remain not eligible.
7. **Quality negative control** — an Arabic answer with a registered intent concept but **no**
   registered causal structure must remain `ASSERTED`, exactly as its English counterpart would.

---

## §17. EXPLICIT NON-GOALS — NOT AUTHORIZED BY THIS CONTRACT

R3-C authorizes none of the following, and R3-I must not introduce any of them:

* **PVCG-R4** (user correction / deterministic invalidation) and any contradiction engine;
* full **Adaptive Questioning**; question **skip / reorder / add**; any change to next-question
  selection;
* **WS10 / WS11 / WS12** activation or integration; **`stage3_evaluator`** integration;
* any **LLM / NLP subsystem**, embeddings, vector store, probabilistic classifier, model-based
  adjudication, or external semantic model call (§6.2);
* a **third language** of any kind;
* **domain expansion, activation, recognition change, or pack capability change**;
* new **gap types** (the six remain frozen in the engine);
* **numeric / unit / quantitative** reasoning of any kind;
* versioning / change-impact; **Render**; **`main` reconciliation**; deployment; provider selection;
* any change to `OWNER_DECISION_REGISTER.md`.

---

## §18. FULL-SUITE RECONCILIATION RULE (binding on R3-I)

The full suite must be reported with its **environment precondition stated**, because the figure is not
comparable otherwise: Python 3.11.15, Flask 3.1.3, SQLite 3.45.1, and **gunicorn resolvable on `PATH`**
so the serving-stack access-log tests EXECUTE rather than SKIP.

**Baseline provenance, stated precisely rather than loosely.** The figure **3776 passed / 3 skipped /
1 xfailed / 0 failed** is recorded in `PVCG_R2_FORMAL_CLOSURE_RECORD.md` §5 **[REPO]**, and that
record's own §1 shows it was executed against the tip **`1ce2c896…`** / the frozen closure candidate
`25cf419c…` — **not** against this contract's base SHA `ca98099e…` **[REPO]**. It is nonetheless the
correct comparison baseline for this lineage, because `ca98099e…` is the SHA-preserving merge of
`25cf419c…` whose entire delta over `1ce2c896…` is **4 governance documents, +332 / -1, with zero
`engine/`, `web/`, `tests/`, `domains/` or `scripts/` change** (independently re-verified this gate)
**[REPO]**. The Creator did **not** execute the full suite at `ca98099e…`. Two later measurements were
made directly on a frozen R3-C candidate rather than inherited: the independent external reviewer
measured **3776 / 3 / 1 / 0** on candidate `6f7720ab…`, and the Creator measured **3776 passed /
3 skipped / 1 xfailed / 0 failed** on the review-repair candidate under the environment precondition
above, re-run on this record's final tree **[EXEC]** (§21 records both). R3-I must nevertheless **re-measure the full suite itself on its
own frozen state** rather than inherit any of these numbers.

Any delta must be reconciled test-by-test with a stated cause; an unexplained delta is a rejection
condition. A skipped serving-stack test reported as a
pass, or a lower total reported without the precondition, is a governance-truth defect.

---

## §19. CLOSURE CRITERIA FOR PVCG-R3

R3 is closable only when **all** hold:

1. R3-C is authoritative (merged, post-merge verified);
2. R3-I is Owner-authorized separately, implemented, independently reviewed, Owner-accepted, merged and
   post-merge verified;
3. §7.3 proven GREEN over the published registered-class inventory;
4. every §10.1 property re-proven and every §10.2 category tested;
5. every §16 negative control holding;
6. §13.2 pin reconciliation performed exactly as specified, with packs, `domain_rules.py` and
   `path_n_questions.py` byte-identical;
7. R1 26/26 GREEN with its test file byte-unchanged; R2 suites GREEN;
8. universal guardrail smoke PASS; full suite reconciled per §18;
9. the residual — unregistered wording in either language — stated truthfully as a known bound, not
   concealed;
10. a formal closure record merged, exactly as R2 required.

Closing R3 closes **only** R3. It does not satisfy PVCG, does not satisfy the Minimum
Launch-Conformance Set, and authorizes no deployment.

---

## §20. STATUS LEDGER PRESERVED BY THIS GATE

```
PVCG-R1 AUTHORITATIVE: YES
PVCG-R2-C AUTHORITATIVE: YES
PVCG-R2-I AUTHORITATIVE: YES
PVCG-R2 AUTHORITATIVELY CLOSED: YES
PVCG-R3 CONTRACT CANDIDATE: FROZEN / NOT AUTHORITATIVE UNTIL MERGED
PVCG-R3 IMPLEMENTATION STARTED: NO
PVCG-R4 IMPLEMENTATION STARTED: NO
FULL ADAPTIVE QUESTIONING ACTIVATED: NO
LLM/NLP SUBSYSTEM ADDED: NO
EMBEDDINGS ADDED: NO
EXTERNAL NLP SERVICE ADDED: NO
PROBABILISTIC SEMANTIC CLASSIFIER ADDED: NO
RUNTIME MODIFIED: NO
TESTS MODIFIED: NO
RENDER REOPENED: NO
MAIN RECONCILIATION STARTED: NO
PVCG SATISFIED: NO
MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO
DEPLOYMENT AUTHORIZED: NO
```

WS10, WS11 and WS12 remain dormant and unwired; no LLM or NLP subsystem exists; the six governed gap
types remain frozen in the engine; no domain is activated, recognised differently, or re-scoped.

---

## §21. REVIEW PATH

LEVEL 2 governance-only under the LEAN §5B risk-based review model. **Zero executable bytes change in
this candidate** (expected runtime delta `0`, test delta `0`, pack delta `0`, pin delta `0`), so §5B.1's
full-suite Creator-evidence trigger is not met by an implementation change.

**Full-suite provenance for this candidate — consistent with §18, and stated without back-dating.** The
Creator did **not** execute the full suite at the authoritative base `ca98099e…` before independent
review, and no statement here or in §18 may be read as claiming otherwise. The `3776 / 3 / 1 / 0`
figure originates from `PVCG_R2_FORMAL_CLOSURE_RECORD.md` §5, measured on the R2 closure lineage
(`1ce2c896…` / candidate `25cf419c…`), and carries to this base only because the intervening R2 closure
merge is governance-only (§18). Two later measurements were then made **directly on a frozen R3-C
candidate**, so the figure no longer rests on the carry-over argument at all:

| Who | Measured on | Result |
|---|---|---|
| Independent external reviewer | frozen candidate `6f7720ab51a58e83270f2b28bcf6d650d5661bc4` | 3776 passed / 3 skipped / 1 xfailed / 0 failed |
| Creator, this review-repair gate **[EXEC]** | this record's own frozen tree (re-run after this section reached its final text) | 3776 passed / 3 skipped / 1 xfailed / 0 failed |

Both were run under the §18 environment precondition (Python 3.11.15, Flask 3.1.3, SQLite 3.45.1,
gunicorn 26.1.0 on `PATH`). R3-I must still re-measure on its own frozen state (§18).

Every **[EXEC]** finding in §2 and §3 was produced by read-only probes that modified no repository file
and added no test fixture; a reviewer should re-measure independently rather than accept them as
repository fact.
