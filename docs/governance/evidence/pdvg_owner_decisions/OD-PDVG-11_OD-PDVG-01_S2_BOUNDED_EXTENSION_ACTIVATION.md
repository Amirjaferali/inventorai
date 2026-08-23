# PDVG-01 — Owner Decisions OD-PDVG-11(a) and OD-PDVG-01(a) — Bounded S2 Extension Activation

**Gate:** Owner Decision Activation / Bounded S2 Extension Gate.
**Decision IDs:** `OD-PDVG-11` — OPTION (a); `OD-PDVG-01` (REVISED) — OPTION (a).
**Governing record:** `docs/governance/PDVG_01_PRE_RELEASE_PRODUCT_DEPTH_AND_VALUE_GATE_RECORD.md`
(PDVG-01), authoritative — accepted candidate `df941501f2f4fb1a86278bc28410049ae1673aa6`, merged as
`a9b9d53cb15165ec9ed0b35962577449750ff663` (PR #559).
**Scope:** documentation / governance-contract only. **No implementation. No benchmark run. No lane,
domain, or phase activation. No downstream authorization.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.

**Verified authoritative base at authoring (re-derived from Git, not from prose):**
`a9b9d53cb15165ec9ed0b35962577449750ff663` — parents `1295ed08ec902f2fcc21934eac3622548a44719b` and
`df941501f2f4fb1a86278bc28410049ae1673aa6`; merge tree `c726bd15b76de3932c3cdc370e8a8f0f46e69617`,
identical to the accepted candidate's tree; `a9b9d53c..origin/feature/atomic-json-session-persistence`
= **0 commits**. **Supersession check: NONE — the authoritative branch has not advanced.**

---

## 1. Evidence-class legend

Every material statement below is tagged, and the classes are never merged:

- **`[OWNER]`** — a decision made by the Owner in the authorization that opened this gate.
- **`[REPO]`** — an authoritative committed repository fact, cited to file and section.
- **`[EXEC]`** — evidence measured by executing or searching the repository at the base SHA.
- **`[OPEN]`** — an unresolved proposition; nothing here converts one into a decision.
- **`[HYPOTHESIS]`** — an interpretation that would require proof; none is relied on.

**An Owner preference is never recorded as a historical repository fact.**

---

## 2. The two decisions, exactly as made

### OD-PDVG-11 — OPTION (a) — ACCEPTED **`[OWNER]`**

**Approve the bounded S2 extension scope** defined by authoritative PDVG-01 (T1-A′): the minimum
extension — one mechanical frozen case alongside the electronics case, EN/AR as an evaluated dimension,
novice and experienced-technical evaluation perspectives, added criteria for question quality, critical
missing gaps, unsafe assumptions / prohibited claims, and specialist escalation, and explicit
`NOT APPLICABLE` classification for the criteria that are structurally bound to the paused Technical
Decision Workspace lane.

PDVG-01 §10 records the option set as (a) approve the T1-A′ minimum extension; (b) approve a narrower
subset; (c) decline **`[REPO]`**. **Option (a) is the accepted option.**

**Binding constraint carried with the approval `[OWNER]` + `[REPO]`:** criterion 12's stale-marking must be
marked `NOT APPLICABLE` and **never** satisfied by introducing targeted-partial-invalidation semantics into
the main product, which remains **PROHIBITED**. Expressed and made binding at
`docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md` §15.6 and §16.

### OD-PDVG-01 (REVISED) — OPTION (a) — ACCEPTED **`[OWNER]`**

**Authorize the bounded S2 extension and, after that extension becomes authoritative through the normal
high-assurance lifecycle, authorize one S2 run against the exact release candidate.**

PDVG-01 §10 records the option set as (a) authorize the bounded extension **and** one run; (b) authorize
one run of S2 unchanged; (c) defer to post-release; (d) decline **`[REPO]`**. **Option (a) is the accepted
option**; option (b) was specifically not recommended by PDVG-01 and is not taken.

**The run authorization is conditional and future-dated.** It becomes exercisable only after this
extension has itself completed: candidate creation → exact SHA freeze → Mandatory Creator Grill →
Independent External Review → Owner exact-SHA acceptance → SHA-preserving publication → PR → merge commit
→ post-merge identity verification. **`S2 BENCHMARK RUN EXECUTED: NO`.** Contract creation and benchmark
execution are deliberately **not** combined in one candidate.

---

## 3. No other OD-PDVG decision is recorded as made

PDVG-01 §11 records **14 actionable Owner decisions** (01, 02, 03, 04, 05, 06, 07, 08a, 08b, 09, 10, 11,
12, 13; `OD-PDVG-08` is a non-actionable container heading) **`[REPO]`**. Exactly **two** are now decided.

| Decision | Status after this gate |
|---|---|
| **OD-PDVG-01 (revised)** | **ACCEPTED — OPTION (a)** |
| OD-PDVG-02 | **`[OPEN]`** — not decided |
| OD-PDVG-03 | **`[OPEN]`** — not decided |
| OD-PDVG-04 (revised) | **`[OPEN]`** — not decided |
| OD-PDVG-05 (revised) | **`[OPEN]`** — not decided; **WS16 extension NOT authorized** |
| OD-PDVG-06 | **`[OPEN]`** — not decided; ILT-002 evidence collection remains NOT AUTHORIZED |
| OD-PDVG-07 | **`[OPEN]`** — not decided; **the MLC is NOT frozen** (§5) |
| OD-PDVG-08a | **`[OPEN]`** — not decided |
| OD-PDVG-08b | **`[OPEN]`** — not decided; the ordering defect stays recorded, not repaired |
| OD-PDVG-09 | **`[OPEN]`** — not decided; CAP-12 / CAP-13 unchanged |
| OD-PDVG-10 | **`[OPEN]`** — not decided; the adaptive-questioning ownership gap stays unowned |
| **OD-PDVG-11** | **ACCEPTED — OPTION (a)** |
| OD-PDVG-12 | **`[OPEN]`** — not decided |
| OD-PDVG-13 | **`[OPEN]`** — not decided |

`OWNER DECISIONS RECORDED AS MADE: 2 of 14.` **No approval of any other decision is inferred, implied, or
carried by adjacency.** Approving the S2 scope does not approve the WS16 extension (OD-PDVG-05), the ILT
round (OD-PDVG-06), or anything else that PDVG-01 lists in the same tier.

---

## 4. Superseded PDVG-01 status lines — stated, not hidden

PDVG-01's §11 status ledger is a snapshot *"effective ONLY if/when this candidate is merged and post-merge
verified"* **`[REPO]`**. **PDVG-01 is not edited by this gate.** Two of its lines are superseded by these
Owner decisions, and the supersession is recorded here so no reader treats the frozen ledger as live:

| PDVG-01 §11 line | Status after this gate |
|---|---|
| `OWNER DECISIONS RECORDED AS MADE: 0` | **superseded → 2** (OD-PDVG-11(a), OD-PDVG-01(a)) |
| `S2 EXTENSION AUTHORIZED: NO` | **superseded → YES (scope approved; contract defined; run still not executed)** |

**Every other PDVG-01 §11 line stands unchanged**, including `BENCHMARK RUN EXECUTED: NO`,
`ILT ROUND EXECUTED: NO`, `MLC DEFINITION FROZEN: NO`, `TIER-1 IMPLEMENTATION AUTHORIZED: NO`,
`PSRR GO: NO`, `DEPLOYMENT AUTHORIZED: NO`, `PRODUCTION AUTHORIZED: NO`, `PAID ACTIVATION AUTHORIZED: NO`,
`UNOWNED CAPABILITY GAP COUNT (PDVG-01 reconstruction): 1`, and
`ADAPTIVE-QUESTIONING OWNER ASSIGNED: NO`.

---

## 5. MLC boundary — preserved exactly

```
MLC DEFINITION FROZEN: NO
MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO
OD-PDVG-07 REMAINS A SEPARATE, UNDECIDED OWNER DECISION
OD-PDVG-10 BLOCKS MLC DEFINITION: NO
OD-PDVG-10 BLOCKS FIRST SERIOUS RELEASE: NO
```

Approving the S2 scope discharges **one** of the two reasons PDVG-01 gave for making no recommendation on
OD-PDVG-07 — reason (ii), *"T1-A′'s scope is undefined pending OD-PDVG-11"* **`[REPO]`**. **Reason (i)
stands undischarged:** the corrected Tier-1 set has not itself been independently reviewed. **Discharging
one of two reasons is not a decision**, and the Tier-1 set does **not** become the MLC by this gate or by
inference from it.

The authoritative correction is preserved verbatim in effect: **OD-PDVG-10 does not block MLC definition**
(PDVG-01 §4A.5) **`[REPO]`**. The old conflation is not reintroduced anywhere in this gate.

---

## 6. Anti-anchoring correspondence — falsification attempted before freeze

### A. Existing-owner falsification — *can S2 legitimately absorb this?*

Attempted falsification: that extending S2 violates S2's own contract. **Refuted on S2's own text
`[REPO]`:**

- **§2** provides an authorized case-revision mechanism requiring *a benchmark-case version; a reason; a
  date; and an explicit comparison-impact note* — all four are supplied for case M-1 (§15.2).
- **§11** states *"Benchmark criteria and protocol may be owner-approved"* — the added criteria `P1…P6`,
  the `NOT APPLICABLE` dispositions, and the Path-N core-gate variant are exactly owner-approved criteria
  and protocol.
- **§12** governs when a new versioned run is required and does not prohibit scope amendment.
- **§0**'s non-authorization boundary is preserved in full and re-stated by §15 and §16.

**Conclusion: extending S2 is legitimate under S2's own amendment mechanisms, not a force-fit.**

### B. Duplicate-owner falsification — *is a second owner needed?*

Attempted falsification: that S2 cannot carry a reasoning-quality/journey evaluation, so a new owner is
required. **Refuted:** nothing in S2 restricts it to one surface or one case; §2 and §11 are precisely the
mechanisms for adding both. No independent repository evidence proves the existing owner cannot carry the
function. **No second benchmark owner, no "Golden Reasoning Benchmark", no parallel evaluation programme,
and no duplicate reasoning-quality framework is created.** Integration Before Duplication.

### C. New-evidence self-invalidation — **one divergence found, disclosed, not silently resolved**

PDVG-01 T1-A′ anticipated marking *"the decision-workspace-only criteria (9–14, and the §6 core gate as
written)"* `NOT APPLICABLE` **`[REPO]`**. Direct source reconstruction narrows that set:

| Criterion | Finding | Disposition |
|---|---|---|
| 9 — decision record version preserved | `contract_version` / `engine_contract_version` are persisted columns in `engine/record_store.py` **`[EXEC]`** | **REUSED** |
| 10 — normalized direct-input snapshot preserved | `seed_idea_text` persisted in `engine/record_store.py`; the accepted-answer ledger is verbatim and append-only **`[EXEC]`** | **REUSED** |
| 11 — response to a changed requirement | Path-N answers a changed input by **full deterministic re-evaluation** **`[REPO]`** | **REUSED** |
| 12 — `validity_status=stale` | `validity_status` occurs in **no** Python file in the repository **`[EXEC]`**; targeted partial invalidation is PROHIBITED **`[REPO]`** | **NOT APPLICABLE** |
| 13 — `REVIEW REQUIRED` label | exists only inside `engine/decision_workspace.py` (definition at `:102`, use at `:1091`) and a test importing it **`[EXEC]`** | **NOT APPLICABLE** |
| 14 — exact change reason shown | `CORRECTION_APPLIED_ACK` in `web/app.py`; `withdrawn_source_records` in `engine/session_reconstruction.py` and `engine/deliverable_assembler.py` **`[EXEC]`** | **REUSED** |

**Exactly two criteria are `NOT APPLICABLE`: 12 and 13.**

**The divergence is from T1-A′'s parenthetical enumeration, not from its rule.** T1-A′'s rule — a
criterion is `NOT APPLICABLE` only where it is structurally bound to another product lane — is applied
unchanged; applying it to the evidence yields `{12, 13}`. Excusing 9, 10, 11 and 14 would understate what
the instrument can legitimately judge and would let a genuine weakness be reported as `N/A` instead of
`FAIL`. **This is disclosed here and in §15.5 of the benchmark rather than applied silently.** It narrows
what the extension excuses; it enlarges nothing and authorizes nothing.

**No other inherited owner, scope, release tier, dependency, or sequencing assumption was invalidated by
new evidence.**

### D. Contradiction escalation

**No contradiction between the approved S2 scope and later authoritative repository truth was found.** The
one divergence is recorded in **C** above and requires no Owner decision: it applies T1-A′'s stated rule
more narrowly than T1-A′'s example enumeration, entirely inside the approved scope. Should the Owner
prefer T1-A′'s literal enumeration, the smallest decision needed would be a one-line instruction to also
mark criteria 9, 10, 11 and 14 `NOT APPLICABLE` — which this record does **not** recommend, because each
has a real Path-N counterpart.

---

## 7. Where the contract lives

The bounded S2 extension contract is **`docs/benchmarks/BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md`
§§15–17** — *Path-N Release-Evaluation Extension v1*. It defines the exact owner, evaluation surface, case
set (E-1 electronics unchanged; M-1 mechanical, new), EN/AR coverage, novice and experienced-technical
evaluation perspectives, reused / added / `NOT APPLICABLE` criteria, the required-dimension coverage map,
the criterion-12 architectural protection, the **domain-gate admissibility protection**, the Path-N core
success gate, baselines, result and evidence mechanics, deterministic/repeatable execution expectations,
exact-commit identity, the one-run-only boundary made countable (**2 cases × 2 languages × 2 perspectives
= 8 evaluation records; no more, no fewer**), interpretation limits, and the prohibited changes.

**Two architectural protections, not one.** §15.6 keeps criterion 12 from pulling stale-marking into the
product. §15.2's **domain-gate admissibility protection** does the same job at the entry gate.

Measured at the base commit by calling `engine.domain_rules.classify_domain` directly **[EXEC]** (the
classifier function only — the full `/start` flow adds the unsupported-evidence check, the classifier-miss
consent path, and `_admit_specialist_domain`): **neither case's bare product concept resolves to a
domain**, and which domain a case resolves to **depends on which of its own sentences is typed**. Most
sharply, the **electronics** case E-1 resolves to **`mechanical`** when stated with its own §3 candidate 1
(`bicycle automatic brake light with a wired brake-lever switch`), and to `electronics_electrical` only
under other phrasing. An evaluator free to choose the phrasing could therefore steer the domain.

The contract closes that by **freezing the English seed text itself** (the **Arabic** seeds freeze **at
first use**, admissible only because an Arabic seed cannot resolve a domain at all — see below), under one
construction applied identically to both cases — *the product-concept line, then the user-context sentence, verbatim, joined by an em
dash*. Applying it yields two frozen English seeds whose measured results are **`NONE`** for E-1 and
**`SINGLE` → `mechanical`** for M-1. **That asymmetry is recorded, not corrected:** the rule was fixed as
a construction and the outcome of applying it disclosed — the seeds were not selected to obtain these
outcomes. The contract further **prohibits rewording a case to change a gate outcome** (any seed change is
a §2 case revision), **prohibits changing `engine/domain_rules.py`, the registry, the activation set, or
the `/start` admission policy to admit a benchmark case**, and **prohibits treating a resolved domain as
the case's "correct" domain**. A blocked, mis-classified, or consent-routed frozen case is a **truthful
reportable result**, never a product defect to be corrected for the benchmark's convenience.

**The Arabic dimension carries the same protection.** `engine/domain_rules.py` contains **no Arabic
text**, and **no domain pack under `domains/` contains Arabic text** **[EXEC]**, so the classifier holds
**no Arabic vocabulary** and an Arabic-only seed **cannot** resolve to a domain — measured `NONE` for the
Arabic rendering of both frozen seeds. An Arabic run therefore reaches the classifier-miss / admission
path for **both** cases. That is a **property to be evaluated**, and this gate authorizes **no** addition
of Arabic (or any other language's) vocabulary to the classifier, the domain packs, or the admission
policy.

**§§0–14 of that record are unchanged.** The extension replaces nothing.

---

## 8. Explicit non-authorizations

This gate authorizes **none** of the following:

the S2 run itself; rendered correction UX; ILT real-user execution; T1-D disclosure implementation; WS6
Quantified Requirements; WS10 content; WS11 activation; WS16 extension; evidence-writer implementation;
ordering-defect repair; semantic adaptive-questioning implementation; CAP-12; CAP-13; new workstreams; new
domains; AI activation; PSRR GO; deployment; production; paid activation.

It further creates no new workstream, no new owner, no new numbering, no lane activation, no product code
change, and no test change. **A favourable future benchmark result would authorize nothing** (S2 §0).

---

## 9. Rejected evidence from this gate

**Every candidate rejected in this gate — whether by the Mandatory Creator Grill or by Independent
External Review, as each row states — is enumerated below and preserved unchanged, unamended, unrebased,
and unpublished (newest first). This table is the authoritative list, and it
carries no separate count — a numeral restated beside its own enumeration goes stale the moment the
enumeration grows, which is precisely the failure mode two of these rejections record.**

| Rejected SHA | Rejection reason |
|---|---|
| `eb54037a99d1be6c3b7e5067fd94f32df87b3b7e` | **F-1 (Independent External Review REJECT) — rejected-evidence enumeration divergence / stale duplicated list.** The roadmap, active-contract, and project-state entries each still restated a detailed rejected-SHA enumeration (already stale — none named this candidate), while this section simultaneously claimed to be the only enumeration: an internally false uniqueness claim, and the known list-drift failure mode repeating **through** review despite three prior in-gate repairs of the same class (G-14, G-18, G-19). Repaired structurally: the three summary surfaces now carry **no** SHA, **no** reason, and **no** count — only the ref pattern and a pointer to this section, which is now the single detailed enumeration in fact as well as in claim. |
| `3a7ccf0d05ca805bbe0fb4c1943b792f368c10e1` | **G-19 (blocking)** — the roadmap's rejected-evidence paragraph enumerated five candidates and then closed with *"**All three** are retained as local refs (…3c986803, …95d4bbc2, …f5830ea0)"*: a stale numeral **and** a short list, sitting directly beside the full enumeration it was supposed to summarize. This is the B24 failure mode of PDVG-01 recurring — a second copy of a list going stale as the first one grows — and it survived the very repair that removed the numerals from the enumeration headings. Repaired by deleting the duplicate lists outright: each surface now states the ref **pattern** (`refs/rejected/s2ext-<short-sha>`, one per candidate enumerated above) so there is no second list to fall out of step. |
| `e647c8899d1842299afb580e57d095d719209f2a` | **G-18 (blocking)** — the §10 status ledger asserted `SEED TEXT FROZEN IN THE CONTRACT: YES` without the English-only qualifier, contradicting §7 of this same record, which freezes the English seeds here and the Arabic seeds at first use. **G-14 repaired the prose surfaces and left the ledger standing** — the identical cross-surface failure mode, one repair later. The ledger also carried no rejected-candidate line at all. Repaired by splitting the ledger line into its English and Arabic halves and by pointing the rejected-candidate line at §9's enumeration instead of restating a count that goes stale at every repair. |
| `8d2ca5f6da519f4e12c70ed050f683e2ace79a1f` | **G-14, G-15** — cross-surface propagation defects. **G-14 (blocking):** the repaired contract froze the **English** seeds here and the **Arabic** seeds at first use, but the roadmap, active contract, project state and this register each still said the contract *"freezes the seed text"* without the English-only qualifier — the same class of cross-surface failure as PDVG-01's F-1, where a proposition was repaired in one file and left standing in others. **G-15:** §15.4 had been corrected to record criterion 15 (*understandable*) as reader-relative, while §15.5's table still gave its basis as bare *"surface-neutral"*. |
| `f5830ea03e973096ee06558a11c3cdbb78a1937a` | **G-9 … G-13** — four defects in the repaired disclosure itself. **G-11 (blocking):** a measured row was labelled *"M-1's own user-context sentence"* when the string tested was a **paraphrase**, not verbatim — an accuracy defect in the very clause that exists to enforce exact wording. **G-10 (blocking):** rule 1 declared *"the two frozen seeds above are the seed text"* while §15.3 left the **Arabic** seeds to be produced at run time — for an Arabic run there was no frozen seed, contradicting the rule as written. **G-13:** criterion 15 (*standalone export **understandable** without the conversation*) was listed among the criteria judged identically across perspectives, though understandability is reader-relative by the criterion's own wording. **G-9:** the frozen seeds are line-wrapped in the document with no statement that each is a single-line, whitespace-collapsed string. |
| `95d4bbc2914dbd25acc46276920b713f8d15eda7` | **G-8 (blocking)** — the domain-gate disclosure added by the previous repair was **itself inaccurate**: it stated that M-1's product concept resolves to `mechanical` (the bare concept returns `NONE`; only the concept plus its user-context sentence resolves) and that E-1's concept with its §2/§3 mechanism words resolves to `electronics_electrical` (E-1's own §3 candidate wording resolves to **`mechanical`**, and the §3 candidate 2 and 3 phrasings return `NONE`). It also left the seed text to the evaluator, which — given that wording steers the domain — handed the evaluator the result the rule existed to protect. Repaired by measuring every quoted string exactly and by **freezing the seed text** under an outcome-independent construction. |
| `3c986803e0216407c2439f70c182b89a09d25aea` | **G-1 (blocking)** — the contract froze two cases without protecting the **domain gate**: no requirement to record the exact seed text, no prohibition on rewording a case to obtain a convenient classification, and no prohibition on changing the classifier / registry / activation set / admission policy to admit a case. The measured classification facts (E-1's §2 concept returns `NONE`; M-1's returns `mechanical`) were not disclosed, leaving the run open to being engineered into admission. Also **G-2** imprecise PVCG-R4 citation; **G-3** the two evaluation perspectives were named but not operationally distinguished; **G-4** M-1's §2-required date was deferred rather than recorded; **G-5** "one run" was not countable, leaving the one-run boundary ambiguous; **G-6** Baseline B could be misread as product AI activation; **G-7** criteria 11 and 14 had no stated evaluation path, leaving a direct route call reportable as a `PASS`. |

Each is retained as a local ref under `refs/rejected/s2ext-<short-sha>` — one per row above — and every
one is carried in the SHA-preserving bundle. **This table is the single detailed enumeration**: the
roadmap, active-contract, and project-state entries for this gate carry only the ref pattern and a
pointer here — no SHA, no reason, no count — so there is no second list to fall out of step. That is the
durable form of the lesson three of these rejections (G-18, G-19, F-1) record: this uniqueness claim was
itself false at `eb54037a…`, where the pointer surfaces still carried their own stale lists, and it became
true only when those lists were **removed**, not refreshed. Each surviving candidate is a **sibling built from the authoritative
base**, never an amendment of a rejected one. The count follows the fixed-point rule: every candidate
rejected up to and including the surviving candidate's predecessor; a surviving candidate is never a
member of its own rejected set.

---

## 10. Status ledger (effective ONLY if/when this candidate is merged and post-merge verified)

```
OD-PDVG-11(a) RECORDED: YES
OD-PDVG-01(a) RECORDED: YES
OWNER DECISIONS RECORDED AS MADE: 2 of 14 (OD-PDVG-11, OD-PDVG-01) — all others OPEN
S2 BOUNDED EXTENSION CONTRACT DEFINED: YES (BICYCLE_BRAKE_LIGHT_COMPETITIVE_BENCHMARK.md §§15-17)
S2 EXTENSION AUTHORITATIVE: NO — not until merge + post-merge verification
S2 BENCHMARK RUN EXECUTED: NO
S2 BENCHMARK RUN AUTHORIZED NOW: NO — conditional on this extension becoming authoritative
SECOND BENCHMARK OWNER CREATED: NO      NEW EVALUATION PROGRAMME CREATED: NO
NEW DOMAINS ACTIVATED: NO (electronics_electrical + mechanical unchanged)
NEW WORKSTREAMS CREATED: 0              NEW OWNERS CREATED: 0
EXECUTABLE PRODUCT-CODE DELTA: 0        TEST DELTA: 0
CRITERIA MARKED NOT APPLICABLE: 2 (12, 13) + the S2 §6 core gate as written
validity_status / STALE-MARKING INTRODUCED INTO PRODUCT: NO
DOMAIN RULES / REGISTRY / ACTIVATION SET / ADMISSION POLICY CHANGED FOR THE BENCHMARK: NO
ENGLISH SEED TEXT FROZEN IN THE CONTRACT: YES (E-1 -> classifier NONE; M-1 -> mechanical; disclosed)
ARABIC SEED TEXT FROZEN AT FIRST USE: YES — admissible only because an Arabic seed cannot resolve
  a domain at all (the classifier holds no Arabic vocabulary), so no translation choice can steer it
D17 / D-AISR-06 / PVCG-R4 SEMANTICS CHANGED: NO
ONE RUN = 2 CASES x 2 LANGUAGES x 2 PERSPECTIVES = 8 EVALUATION RECORDS (no more, no fewer)
AI ACTIVATED BY ANY RUN: NO — Baseline B is an evaluator activity outside the product
MLC DEFINITION FROZEN: NO               MINIMUM LAUNCH-CONFORMANCE SET SATISFIED: NO
OD-PDVG-07 DECIDED: NO
OD-PDVG-10 BLOCKS MLC DEFINITION: NO    OD-PDVG-10 BLOCKS FIRST SERIOUS RELEASE: NO
TIER-1 IMPLEMENTATION AUTHORIZED GENERALLY: NO
WS16 EXTENSION AUTHORIZED: NO           ILT ROUND AUTHORIZED: NO
AI ACTIVATED: NO                        PSRR GO: NO
DEPLOYMENT AUTHORIZED: NO               PRODUCTION AUTHORIZED: NO
PAID ACTIVATION AUTHORIZED: NO
T1-C' STILL INDEPENDENTLY REQUIRED: YES — S2 does not substitute for it
REJECTED CANDIDATES (this gate): see the enumeration in section 9 — deliberately NOT restated as a
  number here, because a second copy of a count that changes at every repair is exactly how such a
  line goes stale. NONE published to origin; NONE amended, rebased, or squashed
```
