# SAFETY SIGNAL STABILIZATION INCREMENT CONTRACT (Workstream 2)

**Document ID:** SAFETY_SIGNAL_STABILIZATION_INCREMENT_CONTRACT
**Type:** Increment Contract (DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md §9)
**Status:** OWNER-APPROVED CONTENT — RECORDED FOR OWNER CONTRACT RECORDING REVIEW — NO IMPLEMENTATION AUTHORIZED
**Owner contract approval classification:** `PASS — OWNER CONTRACT APPROVAL GRANTED — NO IMPLEMENTATION AUTHORIZED`
**Date:** 2026-07-11
**Governing:** DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md §5 item 2, §8–§13; DELIVERABLE_STABILIZATION_OWNER_DECISION.md; DELIVERABLE_STABILIZATION_EVIDENCE_BASIS.md; Workstream 1 baseline `docs/governance/evidence/workstream1_deliverable_baseline/` (tree `a49a51338aaefd82d0f060308464c90dbe68b14c` at tip `3209836b5648f55c70ebb4149db7dfdd5e4adbeb`).

---

## 0. Final owner decisions (binding)

1. **Adjacent-sentence pairing direction:** `condition → consequence` ONLY.
   `consequence → condition` is NOT approved in Workstream 2 — it creates a
   broader false-positive surface without a confirmed baseline need. The
   reordered cause/consequence metamorphic requirement is satisfied within a
   single sentence.
2. **Deduplication normalization:** APPROVED: whitespace collapse; Unicode
   NFC normalization (dedicated fixture required; must not alter the emitted
   raw inventor excerpt beyond the existing documented whitespace handling).
   NOT APPROVED: case folding; punctuation removal; stemming; suffix
   folding; semantic normalization; paraphrase similarity; probabilistic
   similarity.
3. **Positive-fixture design:** the complete-context fixture design is the
   preferred and approved design (see §6.1). The isolated phrase
   "dangerous appliance could remain powered" is NOT required to signal in
   isolation, and "could remain powered" is NOT classified as a
   failure-state cue in Workstream 2.
4. **Existing `_WARNING` fixture:** remains POSITIVE; the required negative
   "the device warns about fire risk but does not control power" is retained;
   the distinction is explained and tested (§6.3).

---

## 1. Objective

Stabilize `engine/safety_signal.py::derive_inventor_stated_safety_signals`
against meaning-equivalent wording variations of inventor-stated dangerous
consequences, without false positives, preserving: the conservative
three-category conjunction architecture (failure/invalid-use condition +
safety-relevant subject + consequence + electrical context, with negation
suppression), the full provenance contract, the `SafetySignal` public
fields, the `_s15` output shape, and the deliverable template. The
Workstream 1 false-negative journey must, at the deliverable level, produce
correct inventor-stated safety signals; the prior positive baseline must
continue to produce at least one valid signal.

## 2. Contract lifecycle and immutability

1. **Recording.** This contract is recorded as
   `docs/governance/SAFETY_SIGNAL_STABILIZATION_INCREMENT_CONTRACT.md` in a
   docs-only commit on a fresh branch from the authoritative tip, published
   via a Draft PR for owner contract recording review.
2. **Approved identity.** Upon the owner's recording approval, the approved
   identity is the pair (recording/merge commit SHA, contract blob SHA). The
   later Implementation Authorization MUST cite both values verbatim;
   implementation against any other contract state is unauthorized.
3. **Fixed boundary.** Once recorded and approved, this contract is a fixed
   owner-approved implementation boundary. The implementation phase MUST NOT
   change its substantive scope, design constraints, test requirements,
   exclusions, or closure criteria.
4. **Status-only updates.** The only later in-place edits permitted are to
   the `Status` header line and an appended lifecycle-log table (dates +
   step outcomes + evidence references), each via docs-only commit. Any
   substantive change requires a NEW owner contract review and approval
   producing a new approved identity. If implementation discovers that a
   substantive term cannot be met, it must STOP and return for re-review
   rather than adapt the contract or the code around it.

## 3. Design constraints

1. **Test-first (binding, plan §12).** The complete fixture matrix (§6) is
   committed and demonstrably failing (red) before any change to
   `engine/safety_signal.py`. See §13 for the mandatory
   BASE RED → IMPLEMENTATION → HEAD GREEN evidence.
2. **Keyword-only expansion prohibited as the sole mechanism.** The change
   must introduce, together: (a) sentence bounding using the committed
   PR #166 boundary definition (`.` `?` `!` and line breaks); (b) explicit
   finite variant families per cue category (token-anchored; no stemming, no
   generic suffix folding — the PR #166 explicit-alias precedent);
   (c) sentence-scoped negation plus an attribution/deferred-determination
   guard family (at minimum: "no claim is made that", "a specialist will
   determine whether", "there is no evidence that"); (d) exact-duplicate
   statement deduplication per §4.
3. **Conjunction preserved.** A signal still requires a failure/invalid-use
   condition, a safety-relevant subject, a consequence, and electrical
   context — now satisfied within one sentence, or within one explicitly
   permitted adjacent-sentence pair (§5).
4. **Truthfulness preserved.** No final criticality or safety determination;
   every signal remains `provenance="inventor_stated"` and
   `validation_status="requires_independent_validation"`; no raw statement
   is rewritten (the existing 400-char whitespace-normalized excerpt rule is
   unchanged); the empty result keeps its "not a determination" wording.
5. **Public contract frozen.** Function name/signature, `SafetySignal`
   fields, `_s15` block shape and keys, `_session_meta` location, and
   `web/templates/deliverable.html` are unchanged.
6. **Bounded complexity and determinism.** No external NLP service or model;
   no new runtime dependency without separate owner approval; no
   probabilistic classification. Regexes limited to PR #166-style span
   splitting and anchored token alternations — no nested unbounded
   quantifiers or catastrophic-backtracking constructions. Matching is
   deterministic; output ordering is deterministic (source-record order per
   the existing `_inventor_texts` enumeration, then sentence index);
   processing is bounded by O(source records × sentences × cue-family
   sizes).

## 4. Deduplication (schema-preserving; owner-approved design)

1. **When.** Exact-duplicate detection runs BEFORE signal construction, over
   the ordered `(source, text)` pairs.
2. **Duplicate definition.** Two texts are duplicates ONLY if their
   normalized forms are identical under §4.4. Any other difference —
   however small — means they are materially different statements and are
   NOT deduplicated. No semantic, paraphrase, stemming, or similarity-based
   deduplication of any kind.
3. **Source precedence (deterministic).** The retained occurrence is the
   FIRST in the existing `_inventor_texts` enumeration order:
   `idea_summary` → assertions in ledger order → acknowledged unknowns in
   order → `known_problem` → `known_mechanism`. Its `source` label is the
   one emitted. Later exact duplicates emit nothing.
4. **Permitted normalization (duplicate detection only).**
   (a) whitespace collapse identical to the existing documented `_excerpt`
   handling (`" ".join(text.split())`); (b) Unicode NFC normalization —
   justified because byte-different composition forms of identical
   characters are the same inventor statement; covered by a dedicated
   fixture; must not alter the emitted raw inventor excerpt beyond the
   existing documented whitespace handling. NOTHING ELSE (owner decision §0.2):
   no case folding, no punctuation removal, no stemming, no suffix folding,
   no semantic normalization, no paraphrase similarity, no probabilistic
   similarity.
5. **Schema limitation (explicit).** The public schema keeps the single
   `source` field; NO `sources` field is added and no key is renamed.
   Consequently, full multi-source provenance for exact duplicates is NOT
   preserved in the output — the non-retained source labels remain
   recoverable from `IdeaState` but are not listed on the signal.
   Multi-source schema expansion is explicitly OUT OF SCOPE for
   Workstream 2 and deferred to a separately owner-gated future increment.

## 5. Adjacent-sentence pairing (bounded)

1. Pairing occurs ONLY inside the same source record's text; it NEVER
   crosses assertion records, acknowledged unknowns, or state fields.
2. Only IMMEDIATELY adjacent sentences (N, N+1) under the PR #166 boundary
   definition. Line breaks are boundaries, so adjacent list items within ONE
   recorded statement are adjacent sentences; pairing never spans
   non-adjacent bullets, and never spans separate recorded answers.
3. **Bounded relationship rule.** A pair qualifies only when sentence N
   contains a failure/invalid-use cue and sentence N+1 contains a
   consequence cue, with the safety-relevant subject present in either of
   the two, and electrical context satisfied over the pair. A negation or
   attribution/deferred-determination guard hit in EITHER sentence vetoes
   the pair. A pair must never be formed from two unrelated hazard mentions
   (two consequence-only or two subject-only sentences never pair).
4. **Permitted direction (owner decision §0.1): `condition → consequence`
   ONLY.** Within-sentence matching is inherently order-insensitive, so the
   reordered cause/consequence metamorphic group is satisfied inside one
   sentence without any pairing. `consequence → condition` pairing is NOT
   permitted in Workstream 2; it may be proposed later only with owner
   approval and its own fixtures.
5. Pairing behavior is covered by BOTH positive and negative fixtures (§6)
   and must be deterministic.

## 6. Required test matrix

All new fixture-matrix tests live in a NEW file
`tests/test_safety_signal_stabilization.py`. `tests/test_safety_signal.py`
is preserved UNCHANGED — no modification is enumerated, and none is
permitted without a new owner contract review naming the exact test and
reason. No fixture is duplicated across the two files.

### 6.1 Positive fixtures

Three explicitly distinguished classes:

- **Complete standalone statements** (each must signal in isolation):
  realistic full inventor sentences that clearly contain the required
  failure or invalid-use condition, including at minimum:
  - "If the sensing identifies the wrong load, the dangerous appliance
    could remain powered." (owner-approved complete-context design; the
    isolated phrase "dangerous appliance could remain powered" is NOT
    required to signal by itself, and "could remain powered" is NOT
    classified as a failure-state cue in Workstream 2);
  - a complete statement embedding "fails to disconnect power";
  - "If it trips the wrong branch, the wrong appliance could be
    disconnected and it would fail to isolate the actual source of danger."
    (covers "fail to isolate the actual source of danger" and "wrong
    appliance could be disconnected");
  - a complete statement embedding "leaving the appliance powered could
    allow overheating".
- **Incomplete fragments requiring same-source context:** "fire risk could
  continue" is NOT required to signal in isolation (it lacks a failure
  condition under the retained architecture); it is tested inside its
  realistic complete statement ("If the relay sticks, damage or overheating
  could continue and the fire risk could continue until someone notices.")
  and inside a permitted adjacent-sentence pair.
- **Adjacent-sentence pairs** (condition → consequence, same source), e.g.
  "If the sensing identifies the wrong load. The dangerous appliance could
  remain powered."
- **Deliverable-level requirement:** the full Workstream 1 false-negative
  journey inputs (`inputs_false_negative_journey.json`, byte-identical) must
  produce ≥1 correct inventor-stated signal per dangerous-consequence
  statement in the regenerated deliverable; isolated fragments are not
  required to signal independently unless they are complete claims under
  this contract.
- The two existing positives (`_INSULATION`, `_WARNING`) remain positive.

### 6.2 Negative fixtures

Each must produce 0 signals: "no claim is made that the appliance is
dangerous"; "a specialist will determine whether the condition is
dangerous"; a discussion-only sentence mentioning fire risk with no stated
failure consequence; "there is no evidence that the relay failed"; "the
device warns about fire risk but does not control power"; negated and
hypothetical variants of the positive statements; an adjacent-sentence
NON-pair (two unrelated hazard mentions in adjacent sentences); a
cross-record non-pair (condition in one recorded answer, consequence in the
next recorded answer → no signal).

### 6.3 The `_WARNING` distinction (owner decision §0.4; tested explicitly)

`_WARNING` ("Wrong results could make the device miss a real risk or warn
the user too late.") remains POSITIVE because it states a failure condition
("wrong results") with a stated consequence ("miss a real risk / too
late"). The negative "the device warns about fire risk but does not control
power" is a capability/control description with NO stated failure
condition. One test asserts both outcomes side by side with this rationale
in its docstring.

### 6.4 Metamorphic fixtures

Groups: fail to / fails to / failed to; disconnect / isolate / remove
power / remain energized; active↔passive voice; singular↔plural (explicit
pairs only); reordered cause and consequence (within-sentence);
same-meaning adjacent-sentence split (permitted pairing direction only);
intent-preserving paraphrases. For EACH group, the tests assert ALL of:
equal detection classification across members; unchanged `provenance`;
unchanged `validation_status`; each member's excerpt faithful to its OWN
original text (identical excerpts across paraphrases are NOT required); no
duplicate-count inflation caused only by surface wording; deterministic
output ordering; unchanged public output shape (key set).

### 6.5 Deduplication fixtures

Identical statement recorded in assertion + `known_problem` +
`known_mechanism` → exactly 1 signal with the precedence-determined source;
near-duplicates differing by one word, by case, or by punctuation → NOT
deduplicated; whitespace-only variants → deduplicated; a dedicated Unicode
NFC composition-variant fixture → deduplicated, with the emitted excerpt
unchanged beyond documented whitespace handling.

### 6.6 Isolation fixtures

Unchanged results for replay/adversarial, WPS-001, benchmark, causal-gate
(177), and the existing `tests/test_safety_signal.py` (18) — run
unmodified.

## 7. F3 — loud-failure comparison harness

The Workstream 2 harness
`docs/governance/evidence/workstream2_safety_stabilization/regenerate_and_compare.py`
(a COPY of the Workstream 1 script, per §8) MUST exit non-zero with an
explicit `JOURNEY INCOMPLETE` message if the completion branch is not
reached within the fixed iteration bound, and MUST NOT write any artifact
from an incomplete journey. Artifact writing occurs only after the
completion assertion passes.

## 8. F4 — baseline immutability and regeneration design

Post-remediation regeneration writes ONLY into the new directory
`docs/governance/evidence/workstream2_safety_stabilization/`. The REQUIRED
design is the copied-script convention (not an output-directory argument),
because `workstream1_deliverable_baseline/reproduce_baseline.py` is itself
an immutable committed evidence artifact — adding an argument would mutate
committed evidence, violating the Workstream 1 README immutability rule and
CLAUDE.md fixture rules. Each future workstream likewise copies the harness
into its own self-contained evidence directory. The canonical Workstream 1
baseline artifacts are never overwritten, edited, or regenerated in place.

## 9. File scope

May change: `engine/safety_signal.py`; NEW
`tests/test_safety_signal_stabilization.py`; NEW
`docs/governance/evidence/workstream2_safety_stabilization/` (harness copy,
regenerated artifacts, comparison record); this contract's status/
lifecycle-log lines only.

Must NOT change: `tests/test_safety_signal.py` (absent a new owner review),
`engine/progression_loop.py`, `engine/requirement_landscape.py`,
`engine/validation_plan.py`, `engine/deliverable_assembler.py`,
`engine/idea_state.py`, `engine/summary.py`, any `web/` file or template,
`benchmark/`, replay/adversarial/WPS/benchmark/gate tests, the entire
`workstream1_deliverable_baseline/` directory, roadmap/anchor/
owner-decision/evidence-basis documents, PR #167, PR #162, scoring,
progression transitions, question order, criticality, Requirement
Landscape, Validation Plan, persistence, schema, session storage, AI Coach,
Answer Clarification, Workstream 3+ behavior.

## 10. Closure criteria (all required)

(1) positive fixtures pass; (2) negative fixtures pass; (3) metamorphic
fixtures pass with the §6.4 invariants; (4) the Workstream 1 false-negative
baseline inputs are correctly detected in the regenerated deliverable;
(5) the prior positive baseline still produces ≥1 valid signal; (6) NO
requirement that any output contain exactly three signals; (7) provenance
remains inventor-stated and source-traceable under §4.3 precedence; (8) no
raw statement rewritten; (9) no safety determination made; (10) focused
tests pass (new file + unchanged existing 18); (11) full-regression
comparison per §11 recorded; (12) new deliverables regenerated into the new
evidence directory via the §7 harness; (13) base-vs-head comparison per
`WS1_CLOSURE_COMPARISON_REQUIREMENTS.md` (quote-level defect-absence proof,
allowed-changes enumeration, prohibited-regression checks);
(14) independent read-only review passes; (15) explicit owner authorization
before merge.

## 11. Regression interpretation rule

The historical full-suite result
(`31 failed, 1324 passed, 1 skipped, 1 xfailed, 24 xpassed`) is a
COMPARISON BASELINE, not a required failure count. Closure requires: no new
failures; no failure outside the previously known
`tests/test_domain_registry.py` set; the exact base-versus-head difference
recorded in the comparison record; fewer historical failures acceptable
ONLY if independently explained and shown unrelated to unauthorized scope;
replay, benchmark, WPS-001, causal-gate, and focused safety results show no
prohibited regression.

## 12. Stop conditions (non-waivable)

Any replay/benchmark/WPS/gate delta; any Workstream 1 artifact mutation;
any false positive in the negative matrix; any required schema change
discovered mid-implementation; any needed edit to
`tests/test_safety_signal.py`; any substantive contract term that cannot be
met as written; ambiguity about a fixture's expected classification. On any
of these: STOP, report, await a new owner review.

## 13. Test-first evidence requirement (BASE RED → IMPLEMENTATION → HEAD GREEN)

The implementation phase must preserve explicit evidence of
`BASE RED → IMPLEMENTATION → HEAD GREEN`. The implementation report MUST
include:

1. the exact focused test command run against the authoritative base after
   adding ONLY the new tests (no extraction change yet);
2. the expected failing tests and their failure reasons;
3. confirmation that no extraction code had yet changed at that point;
4. the implementation commit identity;
5. the exact focused test command and passing result at head.

A red intermediate test commit may exist ONLY on the implementation branch.
It must not be merged independently, and the final Draft PR must not remain
in a failing state.

---

*This contract authorizes no implementation. Implementation remains
separately owner-gated and must cite this contract's approved identity
(recording/merge commit SHA + contract blob SHA) verbatim.*
