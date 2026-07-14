# Workstream 6 — Requirement Landscape Synthesis — Increment Contract

**Status:** OWNER-APPROVED — CONTRACT / CANONICAL (CANONICALLY RECORDED) — NO IMPLEMENTATION AUTHORIZED

**Canonical recording:** recorded through Draft PR #189 and merged into the
authoritative branch `feature/atomic-json-session-persistence` by true
two-parent merge `90f1c34877743510535c397798fcd7da88693606` (ordered parents
`622176980cc04273a415275332f3780f6ed3ba90` (base),
`6dee3dd2fb0b2ba51aa93961921e8deae334d919` (reviewed head)); independent
contract review and focused F1/F2 re-review: PASSED. This canonicalization
changes no scope, wording decision, RED gate, implementation boundary,
deferred requirement, or technical provision of this contract. BASE RED
remains NOT AUTHORIZED; implementation remains NOT AUTHORIZED.

**Workstream:** Workstream 6 — Requirement Landscape Synthesis (P1;
`DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §5 item 6, §15 row 6).

**Authoritative branch:** `feature/atomic-json-session-persistence`
**Authoritative base tip:** `622176980cc04273a415275332f3780f6ed3ba90`
**Recording branch:** `docs/ws6-contract-recording`

**Correction record:** corrected under the owner correction authorization
following the independent read-only review of Draft PR #189 — blocking
finding F1 (Section 14 pass-through coupling) corrected in §2, §4, §4.1, §6
(D4), §8, and §10; non-blocking finding F2 (anchor-kind / requirement-ID
identity) clarified in §3 and §8. The owner-approved D3 disposition coverage
is unchanged and NOT narrowed.

**Authority chain:** the CLAUDE.md governance contract;
`DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §§8–12; the accepted
Workstream 6 read-only source review performed at the authoritative base tip;
the Owner Direction Addendum (Capability Limits and Actionable Referral); the
Owner Decisions message approving D1–D7 with required corrections; and the
owner recording authorization for this document. This contract is subordinate
to all committed anchors. It authorizes NO implementation: recording, BASE
RED, implementation, evidence, and closure each require separate explicit
owner authorization.

---

## 1. Problem statement (demonstrated at the source-review baseline)

At the authoritative base tip, Section 13 ("Requirement Landscape") of the
deliverable produced from the canonical Workstream 1 reproduction journey
contains 13 requirement rows of which 8 are byte-identical repeats of one
verbatim inventor answer; a context-free "I don't know yet." row; and an
explicit `unknown`-disposition ledger record labeled "Recorded answer" with
the resolving action "Validate the recorded answer against the available
evidence." while `acknowledged_unknown_count` is 0. The landscape presents
transcript text without synthesis and erases the epistemic distinction
between an answered record and a declared unknown or deferral.

Demonstrated defect classes owned by this workstream (source review,
accepted): byte-identical repeated Requirement Landscape statements;
transcript text appearing instead of synthesis; context-free orphan
statements; `unknown` and `deferred` records represented as "Recorded
answer"; loss of uncertainty semantics in the landscape presentation.

---

## 2. Authorized scope (bounded; four items only)

Workstream 6 does NOT claim to complete Requirement Landscape synthesis in
any broader AI-generated or semantic sense. The authorized increment is
limited to exactly:

1. **Exact-repeat presentation synthesis.** Within one Phase-7C metadata
   group, byte-identical statements are presented once in the HTML rendering
   with the owner-approved D2 repetition sentence (§7). Grouping is
   byte-identity only (D1 Option A). No prefix, normalized, semantic, fuzzy,
   or AI-based grouping is authorized. Distinct statements, conditions,
   consequences, safety implications, and appended clauses must remain
   separately and fully visible.
2. **Truthful disposition labeling (D3 Option A).** Ledger records with
   disposition `unknown`, `deferred`, or `provisional_assumption` receive the
   owner-approved anchor labels, statuses, and resolving-action wordings of
   §7 in place of "Recorded answer" / "Validate the recorded answer against
   the available evidence.", in both the derivation vocabulary and the
   Section 13 serialization. Each remains distinct from an answered record.
   Because `engine/validation_plan.py` consumes the landscape's anchor
   display label and resolving-action statement, these approved disposition
   label and resolving-action values flow through the existing Requirement
   Landscape into Section 14 rows for the same records. This inherited
   wording change is authorized ONLY as a necessary pass-through consequence
   of the approved D3 vocabulary; it does not authorize any Workstream 7
   implementation (see §4.1).
3. **Bounded grouping metadata (D5).** One additive object
   `_session_meta.requirement_landscape_synthesis`, synthesized at the
   assembly boundary exclusively from the already-derived landscape and
   package values, carrying the group/repetition facts that the template
   renders. No new top-level deliverable key.
4. **Insufficient-information placeholder wording (D7).** The existing
   empty-content `_restate` placeholder path only, using the owner's exact
   revised wording (§7). No general insufficiency inference from answer
   quality, domain, vocabulary, or technical complexity.

**Disposition-handling rule.** Disposition classification is based SOLELY on
the exact existing `AssertionRecord.disposition` value. No lexical, semantic,
domain, or answer-quality inference of any kind is authorized.

**Unchanged-behavior rule.** `answered` records, `pending_evidence` records,
`pending_specialist` records, contradiction pairs, gap anchors, and every
disposition not explicitly listed in item 2 above remain byte-unchanged in
vocabulary and behavior — labels, statuses, resolving actions, precedence,
and rendering.

---

## 3. Frozen guarantees

- Section 13 row count unchanged (`total == len(requirements)`; the
  Section 13 ↔ Section 14 arithmetic tie preserved).
- Requirement IDs unchanged (scheme `req:assertion:rec_N`,
  `req:evidence:rec_N`, `req:specialist:rec_N`, `req:contradiction:…`,
  `req:gap:…`); Workstream 4 criticality confirmations are never orphaned by
  this increment.
- Inventor statements byte-unchanged: verbatim, untruncated, never
  paraphrased, never reworded.
- Ordering unchanged: display precedence and `rec_N` ordering byte-identical.
- JSON structure and key sets unchanged — the pinned Section 13 key set, all
  top-level package keys, and all row key sets — EXCEPT the approved additive
  `_session_meta.requirement_landscape_synthesis` object.
- `source_status`, anchor-label (`provenance`), and `resolving_action` field
  VALUES may change ONLY for rows whose underlying disposition is `unknown`,
  `deferred`, or `provisional_assumption` (and the D7 placeholder statement
  text for empty-content records); every other row is byte-identical.
- Workstream 4 criticality categories, authorities, and verbatim rationales;
  Workstream 5 `_session_meta.risk_safety_linkage` and its three exact
  wordings; the frozen zero-risk disclaimer; and all Workstream 1–5 closed
  behavior remain untouched.
- **Anchor-kind and requirement-ID identity (F2 clarification).** Workstream
  6 does NOT introduce new requirement anchor kinds or new requirement-ID
  prefixes. The three authorized dispositions retain: the existing
  requirement-id scheme; the existing record-linked identity; the existing
  precedence; the existing ordering; the existing Section 14 eligibility; and
  the existing one-row-per-record behavior. Only their public-facing anchor
  label, source status, and resolving-action wording may change. The
  implementation must not modify `_record_id_prefix`, precedence tables, or
  `_STEP_ANCHOR_KINDS` to create new semantic categories unless separately
  authorized.

---

## 4. Explicit exclusions

Not authorized under any reading of this contract:

- advisory referral lines of any kind on pending-evidence or
  pending-specialist rows (DEFERRED per D6 Option B to Workstream 7 or a
  separately owner-gated future capability workstream);
- a Domain Capability Registry, or any "capability not established" wording
  or trigger (no supporting state exists; recorded only as deferred future
  work, §11);
- specialist type, taxonomy, routing, marketplace, referral path, or
  preparation checklist generation;
- external tool, simulation, laboratory, engineering-analysis, or
  commercial-product guidance or naming;
- AI Coach behavior; Answer Clarification activation;
- journey, question, elicitation, or progression change;
- any change to Sections 4, 5, 6, 8, or 12, the safety-signal
  derivation, the criticality capture flow, or the Workstream 5 linkage;
- any Section 14 change outside the narrow authorized pass-through boundary
  of §4.1;
- content-level merging of non-byte-identical statements; any paraphrase,
  truncation, or rewording of inventor text;
- semantic or AI deduplication, or any heuristic upgrade;
- dropping any Section 13 JSON row; changing `requirement_id`s, `total`,
  `count_basis`, the count relationship, or the Section 13 ↔ Section 14
  arithmetic tie;
- persistence, transcript-schema, or serialized-state change; new top-level
  deliverable keys; changes to the pinned Section 13 key set;
- domain inference of any kind; any implication that the application supports
  every electrical or electronics subdomain.

### 4.1 Section 14 boundary (F1 correction — authorized pass-through only)

Workstream 6 makes NO change to Section 14 logic or behavior. Specifically,
ALL of the following are unchanged:

- Section 14 logic;
- validation-step generation logic;
- row and step counts;
- the requirement-to-validation-step mapping;
- responsibility logic;
- confidence logic;
- grouping and collapse behavior;
- ordering;
- the Section 13-to-Section 14 arithmetic tie;
- no Workstream 7 actionability, referral, specialist taxonomy, tool
  guidance, or validation planning is added.

Only the already-authorized disposition label, provenance, status, and
resolving-action wording may pass through into the existing Section 14 rows
for:

- `unknown`;
- `deferred`;
- `provisional_assumption`.

No other Section 14 wording or behavior may change. This pass-through is an
inherited wording consequence of the approved D3 vocabulary (authorized), as
distinct from any Workstream 7 logic or structure change (prohibited).

---

## 5. Stop conditions (non-waivable)

STOP immediately and report, without patching, if:

- any wording cannot be selected by exact disposition match on existing
  state;
- any protected assertion would need removal, weakening, broadening,
  replacement, bypass, or conversion into a non-asserting test (D4 limits);
- Section 13 row count, requirement IDs, ordering, or the Section 14
  arithmetic tie would change;
- grouping would merge non-byte-identical statements;
- any wording implies capability, verification, safety, deliberate inventor
  confirmation of repeats, or subdomain coverage;
- the assembler would need to re-derive disposition from raw state
  (vocabulary-seam duplication);
- any owner-approved wording cannot be rendered byte-exactly in both JSON and
  HTML.

---

## 6. Owner decisions D1–D7 (binding)

| Decision | Owner ruling | Binding effect |
|---|---|---|
| D1 Grouping rule | Option A — byte-identical statements only | No prefix, normalized, semantic, fuzzy, or AI grouping. Distinct statements, conditions, consequences, safety implications, and appended clauses remain separately visible. |
| D2 Repetition wording | Approved with revised exact wording | The exact sentence in §7. The wording must not imply the inventor deliberately confirmed the same requirement multiple times; repetition may result from the current journey or question design. |
| D3 Disposition coverage | Option A | `unknown`, `deferred`, and `provisional_assumption` are each distinguished from an answered record with the §7 wordings. |
| D4 Protected-test amendment | Approved with strict limits; extended by the F1 correction | The named Increment-4 and Phase-7C tests may be amended only where strictly necessary to add and pin the new owner-approved disposition vocabulary and presentation behavior. F1 correction: `tests/test_phase_7b_validation_plan_collapse.py` may additionally be amended, but ONLY where existing assertions pin the legacy generic label or resolving-action wording for `provisional_assumption`, `unknown`, or `deferred` records; its assertions protecting grouping, collapse behavior, responsibility, confidence, ordering, counts, and rendered structure must remain unchanged. Across all three files: no existing protected assertion may be removed, weakened, broadened, replaced, bypassed, or converted into a non-asserting check. Every changed assertion must be listed individually in the future PR description and evidence record. No other Workstream 7 test file is authorized for amendment unless a later BASE RED proves a directly coupled byte-exact wording assertion and the owner separately approves it. |
| D5 Metadata location | `_session_meta.requirement_landscape_synthesis` | No new top-level deliverable key. No persistence, transcript-schema, or serialized-state change. |
| D6 Advisory referral lines | DEFERRED — Option B | No advisory referral lines for pending-evidence or pending-specialist rows in Workstream 6. Workstream 6 may truthfully label the existing states (evidence required; specialist input required) but must not implement actionable referral logic. The detailed guidance belongs to Workstream 7 or a separately owner-gated future capability workstream. |
| D7 Insufficient-information wording | Approved with revised exact wording | Authorized ONLY for the existing empty-content placeholder path. No general insufficiency inference from answer quality, domain, vocabulary, or technical complexity. |

---

## 7. Exact public wordings (byte-exact; owner-approved)

All wordings below are byte-exact. They are selected solely by the exact
`AssertionRecord.disposition` value (or the empty-content placeholder path)
and are rendered identically in JSON and HTML.

### 7.1 Recorded unknown (`unknown`)

Anchor label:

```text
Recorded unknown
```

Status:

```text
You indicated that this is not known yet.
```

Resolving action:

```text
This item remains unresolved. It may later be addressed through additional information, evidence, or specialist input.
```

### 7.2 Deferred decision (`deferred`)

Anchor label:

```text
Deferred decision
```

Status:

```text
You chose to defer this item.
```

Resolving action:

```text
This item remains unresolved and can be revisited when you are ready to decide.
```

### 7.3 Provisional assumption (`provisional_assumption`)

Anchor label:

```text
Provisional assumption
```

Status:

```text
This assumption was recorded as a temporary direction and has not been validated.
```

Resolving action:

```text
Validate, revise, or replace it before relying on it.
```

### 7.4 Repetition presentation (per grouped distinct statement; HTML)

```text
This statement was recorded N times during the session.
```

where `N` is the exact byte-identical occurrence count. The statement itself
is shown once, verbatim, untruncated.

### 7.5 Insufficient information (empty-content placeholder path ONLY)

Replaces the existing "Recorded answer awaiting restatement." statement text:

```text
Insufficient information was recorded to organize this item reliably.
This does not indicate that the idea is invalid; the item remains unresolved.
```

### 7.6 Unchanged vocabularies

- Evidence required (`evidence_requested`): existing public vocabulary
  UNCHANGED. No advisory referral line.
- Specialist input required (`specialist_requested`): existing public
  vocabulary UNCHANGED. No specialist type, referral path, preparation
  checklist, external tool, simulation, laboratory, or commercial product may
  be generated.
- Answered (`answered`) records, contradiction pairs, gap anchors, and any
  unlisted disposition: UNCHANGED in label, status, resolving action, and
  rendering.
- Capability not established: NO wording is authorized in Workstream 6,
  because the current state does not support a truthful capability
  determination. Recorded only as a deferred future capability requirement
  (§11).

---

## 8. File surfaces

| File | Authorization |
|---|---|
| `engine/requirement_landscape.py` | CHANGE (bounded): apply disposition-aware anchor labels, source statuses, and resolving-action wordings for the three authorized dispositions; replace the empty-content placeholder wording (D7). F2 clarification: NO new anchor kinds and NO new requirement-ID prefixes; `_record_id_prefix`, precedence tables, and Section 14 eligibility semantics must not gain new semantic categories unless separately authorized. Requirement-ID scheme, record-linked identity, one-row-per-record, ordering, precedence, and all other vocabulary byte-unchanged. |
| `engine/deliverable_assembler.py` | CHANGE: synthesize the additive `_session_meta.requirement_landscape_synthesis` object (reads only derived landscape/package values); the Section 13 serialization passes the new derivation values through the existing public maps. No re-derivation of disposition from raw state in the assembler. |
| `web/templates/deliverable.html` | CHANGE: Section 13 block only — grouped exact-repeat presentation with the D2 sentence; renders the new labels. NO advisory referral lines. |
| `tests/test_increment_4_requirement_landscape.py` | AMEND under D4 strict limits only; every amendment individually listed. |
| `tests/test_phase_7c_requirement_landscape_collapse.py` | AMEND under D4 strict limits only; every amendment individually listed. |
| `tests/test_phase_7b_validation_plan_collapse.py` | AMEND under the F1-corrected D4 limits only: solely where existing assertions pin the legacy generic label or resolving-action wording for the three authorized dispositions; grouping/collapse/responsibility/confidence/ordering/count/structure assertions unchanged; every changed assertion individually listed. |
| `tests/test_requirement_landscape_synthesis.py` (new, single file) | CREATE at the separately authorized BASE RED gate. |
| `engine/idea_state.py`, `engine/progression_loop.py`, `engine/safety_signal.py`, `engine/validation_plan.py`, `web/app.py`, `web/templates/session.html`, persistence, benchmark/replay, and all other files | MUST NOT CHANGE. |

---

## 9. RED expectations (separately authorized; no test is created by this contract)

Deterministic BASE RED, driven by the recorded Workstream 1 reproduction
journey through the Flask test client plus minimal disposition fixtures
(`unknown`, `deferred`, `provisional_assumption`, empty-content). Every
wording is pinned byte-exactly to §7 of this contract; no unapproved wording
may be pinned.

- **R1 — exact-repeat presentation.** The byte-identical Workstream 1
  statement renders once with exactly
  `This statement was recorded 8 times during the session.` (BASE: 8
  separate identical rows and no count — RED). Non-identical-statement
  protection is recorded as the following invariant, not as a fragile
  narrative count alone:

  ```text
  Every non-byte-identical statement in the approved RED fixture must remain
  fully visible exactly once in the synthesized HTML presentation.
  ```

  The fixture may also pin exact expected statements and counts
  deterministically. No semantic, prefix, normalized, fuzzy, or AI grouping
  is authorized.
- **R2 — recorded unknown.** An `unknown`-disposition record carries none of
  `Recorded answer` / `Validate the recorded answer against the available
  evidence.` and carries the three exact §7.1 wordings, in JSON and HTML
  (BASE — RED).
- **R3 — deferred and provisional.** The same for `deferred` (§7.2) and
  `provisional_assumption` (§7.3) with their exact wordings (BASE — RED).
- **R4 — synthesis metadata and parity.**
  `_session_meta.requirement_landscape_synthesis` exists and its content is
  machine-compared for JSON/HTML parity — not merely checked through
  independent substring assertions (BASE — RED).
- **R5 — placeholder wording.** The empty-content placeholder path emits the
  exact §7.5 two-line wording (BASE — RED).

Protected P-class invariants (must pass on BASE and HEAD): the §3 frozen
guarantees; `answered`/pending/contradiction/gap vocabulary byte-unchanged;
Workstream 4 criticality fields and stale-confirmation metadata; Workstream 5
linkage object and exact wordings; the frozen zero-risk disclaimer; the
hygiene token rules over the new wordings; derivation purity, determinism,
and order-independence. If any RED case cannot be expressed without a
production change, STOP.

---

## 10. GREEN, regression, evidence, and closure gates

- **GREEN:** the new focused suite passes with zero skips and zero xfails (a
  placeholder skip or xfail at GREEN is a failed GREEN gate); every protected
  suite passes: increment-4 landscape 39 (as amended under D4), Phase-7C 7
  (as amended under D4), Phase-4A 8, increment-5 validation plan 55,
  Phase-7A 9, Phase-7B 9 (passing AFTER the strictly additive F1-corrected
  D4 wording-pin amendments; its grouping, collapse, responsibility,
  confidence, ordering, count, and structure assertions unchanged),
  deliverable hygiene 22, structured criticality 18,
  unified risk/safety 17, safety-signal 18 + stabilization 15, wps001
  invariants 21. The GREEN gate distinguishes: (1) authorized inherited
  wording changes in Section 14 rows for the three dispositions (§4.1) —
  expected and required; (2) prohibited Workstream 7 logic or structure
  changes — any such change fails the gate.
- **Regression:** the full suite compared against the preserved baseline —
  31 failures confined to `tests/test_domain_registry.py`, zero new
  failures, none reclassified or corrected by this workstream.
- **Evidence (separately authorized):**
  `docs/governance/evidence/workstream6_requirement_landscape_synthesis/`
  mirroring the Workstream 5 harness discipline: BASE artifacts generated
  from the RED commit and HEAD artifacts from the reviewed head, for (i) the
  canonical Workstream 1 journey and (ii) an
  unknown/deferred/provisional-assumption fixture journey; a machine
  JSON/HTML parity record; the individually listed D4 test amendments; the
  RED/GREEN record; a SHA-256 manifest. No advisory-referral artifacts.
- **Closure:** plan §12 in full — focused proof, accepted full regression,
  regenerated deliverable evidence demonstrating absence of the demonstrated
  defects, independent read-only review, explicit owner closure
  authorization, and the §15/roadmap docs-only synchronization. Closure must
  NOT claim: journey-side repetition causes fixed (Workstreams 8–10);
  Section 14 responsibility/confidence placeholders fixed (Workstream 7);
  referral capability added; capability determination added; or any broader
  semantic synthesis completed.

---

## 11. Deferred future capability requirements (recorded, not implemented)

Future, separately owner-gated work. Nothing here is implemented or implied
by Workstream 6:

1. A Domain Capability Registry and truthful capability-limit disclosure
   ("capability not established" — no supporting state exists today).
2. Specialist taxonomy, referral paths, and preparation checklists.
3. External tool, simulation, laboratory, and engineering-analysis guidance
   (never commercial-product naming without independent justification).
4. General insufficient-information detection beyond the empty-content
   placeholder path.
5. Turbine-style and other subdomain-specific organize-versus-must-not-invent
   guidance.
6. Section 14 responsibility/confidence placeholder remediation and
   validation-step actionability (Workstream 7).
7. Journey-side repetition prevention and question-context attachment
   (Workstreams 8–10); guided support for missing knowledge mid-journey
   (Workstream 13).

---

## 12. Non-authorization statement

This contract authorizes NO implementation. No RED test, source change,
template change, evidence artifact, roadmap or status change, or merge is
authorized by this document. BASE RED, implementation, independent review,
merge, evidence, and closure each require separate explicit owner
authorization. Workstream 6 is NOT started, NOT implemented, and NOT closed
by this recording. PR #167 and PR #162 remain outside this contract and
untouched. The AI Coach remains prohibited; Answer Clarification remains
inactive; persistence remains frozen; the official product state remains
`DEMO_READY_WITH_LIMITATIONS`; the MVP scope remains
electronics/electrical-only.
