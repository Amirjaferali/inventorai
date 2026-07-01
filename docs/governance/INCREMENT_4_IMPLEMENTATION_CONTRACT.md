# Increment 4 Implementation Contract — Atomic Requirements & Criticality-Aware Risk Register

Status:
`DRAFT IMPLEMENTATION CONTRACT — NOT TESTS-FIRST OR SOURCE AUTHORIZATION`

## 1. Document status and bounded authority

This document is the bounded, owner-gated IMPLEMENTATION CONTRACT DRAFT for
Increment 4 (`Atomic Requirements & Criticality-Aware Risk Register`). It
translates the already-merged authority rulings and bounded design into exact
implementation boundaries, concrete names, and future source and test path
permissions.

This document does NOT:

- authorize tests-first work, tests, source implementation, or template changes;
- authorize any product behavior change;
- modify any source, template, test, roadmap, anchor, or ruling;
- stage, commit, push, create a PR, or merge.

Its authority is bounded by and subordinate to, in this order:

1. `MVP_SCOPE_FREEZE.md` and the active governance anchors;
2. the merged Increment 4 authority rulings `C4-R1` through `C4-R13`
   (`docs/governance/INCREMENT_4_AUTHORITY_RULINGS.md`);
3. the merged Increment 4 bounded design `D-1` through `D-7`
   (`docs/governance/INCREMENT_4_DESIGN.md`);
4. the merged `docs/governance/ACTIVE_EXECUTION_ROADMAP.md`;
5. the closed Increment 3 authority (`INCREMENT_3_IMPLEMENTATION_CONTRACT.md`,
   `R-1` through `R-6`).

Where this contract and any of the above could differ, the above controls. This
contract adds no authority beyond faithfully realizing them; every name it fixes
is a contract-selected label over a design-required fact, never a new product
signal.

## 2. Identity and authority lineage

- Authoritative branch: `feature/atomic-json-session-persistence`.
- Drafting base (authoritative tip at drafting time):
  `289873cb2ee57693e3f9c9670138823939c0fa4d` — PR #50 governance-sync
  true-merge (ordered parents `aab6f88c1133ddb814007e0e3c61296b655b6356` then
  `3937c2127c5ceabbe1de41b0db7702a6e237fa6b`, tree
  `c1398aa7bcf709579add2a5144866f9759de8630`). The live tip is always resolved
  from Git; this SHA is a document-publication baseline, not a permanent
  live-tip assertion.
- Increment 4 authority lineage:
  - PR #47 true-merge `393537aa7671b9a6e0cfbcde5a05047e5e76c842` — merged the
    authority rulings `C4-R1` through `C4-R13`;
  - PR #48 true-merge `d75568d8510c4bb49bbce06997991c1decb51cd4` — post-rulings
    governance sync (rulings §12 amendment);
  - PR #49 true-merge `aab6f88c1133ddb814007e0e3c61296b655b6356` — merged the
    bounded design (`docs/governance/INCREMENT_4_DESIGN.md`, 402 lines, 22525
    bytes, SHA-256 `d30dad7edf0668c7138b86d0048f134cbe1bfa095ea99c0eec3da8e5fe2cd852`);
  - PR #50 true-merge `289873cb2ee57693e3f9c9670138823939c0fa4d` — post-design
    roadmap sync (roadmap 1047 lines, 110298 bytes, SHA-256
    `9cc2a293a001b742caca8ec66ce19d263417be407e6b03f6627f620614ba22b2`).
- Product-execution tip remains `b5a8e72b26acc5ddbee355bc69b419ff09152c50`
  (PR #45 Increment 3 SOURCE merge). This contract is not product execution and
  does not advance that tip.
- `origin/main` remains `0e89e4636399760965c9ff8086b465c90dbadf8e` and is
  outside this lane.
- This draft creates NO tests-first authority and NO implementation authority.

## 3. Exact future source boundary

The contract freezes the MAXIMUM candidate source scope for the future
Increment 4 implementation. No path is authorized by this contract; each remains
gated by a separate tests-first authorization and a separate source
authorization.

`REQUIRED` (maximum permitted source surface — three paths only):

1. ONE new pure Increment 4 engine module (name fixed in §4);
2. `engine/deliverable_assembler.py` — ONE additive section function and ONE
   additive package key only;
3. `web/templates/deliverable.html` — ONE additive deliverable section only.

`NOT REQUIRED` (must not be changed for MVP-1):

- `engine/idea_state.py` — no new field, no new method is required or permitted
  for MVP-1 (the derivation invents no `IdeaState` field);
- `web/app.py` — MVP-1 is deliverable-only; no route/session change;
- `web/templates/session.html` — MVP-1 renders no session surface.

`PROHIBITED` (must remain byte-identical / behavior-identical):

- `engine/idea_development_outputs.py` (Increment 3 frozen — `C4-R7`);
- `engine/scoring.py`, `engine/progression_loop.py` (`C4-R8`);
- the `_s4` and `_s6` bodies within `engine/deliverable_assembler.py`
  (`C4-R6`, `C4-R12`);
- `tests/test_increment_3_visible_outputs.py` (frozen tests-first artifact —
  `C4-R13`);
- persistence paths (`C4-R9`);
- domain-registry paths (`C4-R10`);
- active governance anchors and `CLAUDE.md`.

Naming a path here does NOT authorize editing it. Editing any `REQUIRED` path
requires the future tests-first authorization to have been committed and merged,
then a separate source authorization.

## 4. Concrete names (contract-frozen; deferred by the design)

The design (`INCREMENT_4_DESIGN.md` §5) deferred all concrete names to this
contract. The following names are frozen. None collides with Increment 3
(`derive_next_development_step`, `NextDevelopmentStep`, `_s12`,
`section_12_next_development_step`, "Next Development Step"); none implies stored
state, verification, professional approval, or risk certainty.

| Role | Frozen name |
|---|---|
| New engine module path | `engine/requirement_landscape.py` |
| Public derivation function | `derive_requirement_landscape(state)` |
| Immutable derived-requirement payload type | `DerivedRequirement` (frozen dataclass) |
| Primary provenance-anchor type | `ProvenanceAnchor` (frozen dataclass: `anchor_kind`, `anchor_reference`) |
| Supporting-reference type | `SupportingReference` (frozen dataclass: `reference_kind`, `reference`) |
| Criticality category field | `criticality` (string value; see §9.7 vocabulary) |
| Criticality-authority field | `criticality_authority` (string value; see §9.7 vocabulary) |
| Requirement-linked risk payload type | `GroundedRisk` (frozen dataclass) |
| Collection / result payload type | `RequirementLandscape` (frozen dataclass: ordered `requirements` tuple, ordered `risks` tuple) |
| Deliverable assembler section function | `_s13` (private, in `engine/deliverable_assembler.py`) |
| Deliverable package key | `section_13_requirement_landscape` |
| User-visible section title | `Requirement Landscape` |
| Future Increment 4 test-file path | `tests/test_increment_4_requirement_landscape.py` |

Name-selection rationale (compact): "requirement landscape" names the visible
product value — the COMPLETE set of active, provenance-anchored requirements —
without implying a professional requirements-management workspace (prohibited by
`C4-R10`), stored records (prohibited by `C4-R9`), or certainty. `Derived...`
and the frozen-dataclass style mirror the Increment 3 `NextDevelopmentStep`
discipline (pure, immutable, render-time) while remaining a distinct symbol.
`section_13_*` and `_s13` follow the existing additive-section numbering
(sections 1–12 exist today) and cannot collide with `section_12_*`/`_s12`.
`GroundedRisk` encodes that a risk exists ONLY on a grounded adverse consequence
(`C4-R6`), never a generic warning. String category/authority values (not new
enum imports) avoid reusing `engine.idea_state.UNDETERMINED` (a responsibility
label) as a criticality symbol.

## 4.1 Frozen payload data model (F-6 / F-7)

All payload dataclasses are `frozen=True`; every collection inside a public
payload is a `tuple`; equality is structural dataclass equality; the engine
result is immutable. The exact minimum frozen structures are:

`ProvenanceAnchor`:

```text
anchor_kind: str          # one of: assertion | gap | active_contradiction |
                          #         pending_evidence | pending_specialist
anchor_reference: str     # the stable reference used in §6.7
display_label: str        # human-readable label; never a raw enum
```

`SupportingReference`:

```text
reference_kind: str
reference: str            # existing stable reference (e.g. a recommendation ref)
display_label: str        # human-readable label; never a raw enum
```

`ResolvingAction` (optional on a requirement; restates recorded state only;
NEVER called or presented as the global Next Development Step):

```text
action_kind: str
statement: str            # restated from recorded state; invents no obligation
source_reference: str     # the anchor/recorded reference it restates
```

`GroundedRisk` (canonical risk record; see §9.8 source of truth):

```text
risk_id: str              # deterministically derived from the grounded structural
                          # consequence reference and the linked requirement IDs;
                          # NEVER from list position
linked_requirement_ids: tuple[str, ...]   # ordered, non-empty
consequence: str
grounding_references: tuple[SupportingReference, ...]
authority: str
status: str
rationale: str
```

`DerivedRequirement`:

```text
requirement_id: str                       # §6.7 identifier
statement: str                            # restated recorded content (C4-R1)
primary_anchor: ProvenanceAnchor
supporting_references: tuple[SupportingReference, ...]
source_status: str                        # source-status vocabulary, §4.2
criticality: str                          # §9.7 vocabulary
criticality_authority: str                # §9.7 vocabulary
criticality_rationale: str | None         # required only for non-UNDETERMINED
resolving_action: ResolvingAction | None
linked_risk_ids: tuple[str, ...]          # references into RequirementLandscape.risks
```

`RequirementLandscape`:

```text
requirements: tuple[DerivedRequirement, ...]
risks: tuple[GroundedRisk, ...]           # the CANONICAL risk store (F-6)
```

## 4.2 Source-status vocabulary (F-7)

`source_status` is a human-semantic, source-mirrored value that MUST NOT leak a
raw internal enum. Frozen minimum values by anchor kind:

```text
assertion            -> "recorded"
active_contradiction -> "active contradiction"
pending_evidence     -> "evidence pending"
pending_specialist   -> "specialist input pending"
open gap             -> "open"
partial gap          -> "partially addressed"
```

`CLOSED` and `ACCEPTED_RISK` gaps are NOT emitted as active gap requirements
(only `OPEN`/`PARTIAL` open gaps are anchors, §6.3). The contract distinguishes
this source-mirrored MEANING from any raw internal enum, which MUST NOT be
displayed (§7.3).

## 4.3 Immutability and JSON-safe conversion (F-7)

- All payload dataclasses are `frozen=True`; all public-payload collections are
  tuples; equality is structural.
- The engine result (`RequirementLandscape`) remains immutable.
- The assembler (`_s13`) converts it to plain JSON-safe dictionaries / lists /
  strings for the deliverable package (mirroring `_s12`); the conversion MUST NOT
  mutate the payload.
- Malformed optional source records degrade safely through per-record handling
  under §9.10.6: each malformed record is skipped independently, valid anchors
  continue to render, and the landscape becomes empty only when no valid active
  anchor remains.

## 5. Realization shape (additive; mirrors Increment 3 discipline)

Increment 4 MUST be realized as, at most: ONE new pure engine derivation
(`derive_requirement_landscape`) + ONE additive assembler section (`_s13`,
package key `section_13_requirement_landscape`) + ONE additive deliverable
template section ("Requirement Landscape"). The derivation is an ADDITIONAL,
INDEPENDENT selector over the same `IdeaState`; it is NOT
`derive_next_development_step`, MUST NOT call it, and MUST NOT alter it or its
payload/inputs/selected result.

`engine/requirement_landscape.py` import boundary (F-5, mirroring
`engine/idea_development_outputs.py`):

1. Python standard-library imports required for immutable pure payloads and
   deterministic processing are PERMITTED, including as needed: `dataclasses`,
   `typing`, `re`, `collections`. (These are permitted, not mandatory; the module
   need not import every listed module.)
2. Among PROJECT modules, the new module MAY import ONLY from `engine.idea_state`.
3. It MUST NOT import from `engine.idea_development_outputs`,
   `engine.deliverable_assembler`, scoring, progression, persistence, the domain
   registry, the web/application layers, Flask, templates, session, or
   `engine.ai_advisor`.

The architecture/import guardrail tests MUST assert this boundary (permitted
standard library; sole permitted project import `engine.idea_state`; the
prohibited set above).

## 6. Atomic-requirement contract (D-1, D-2, C4-R1, C4-R2)

6.1 Requirements are PURE DERIVED outputs, not stored lifecycle records. The
derivation MUST NOT mutate `IdeaState`, assertions, gaps, history, maturity,
readiness, or stage.

6.2 MVP-1 produces exactly ONE coarse atomic requirement per active primary
anchor. NO source-fragment splitting is performed in MVP-1 (`C4-R2` coarse-item
fallback; design §7). Splitting remains reserved (§6.7) and prohibited until a
future increment proves deterministic fragmentation.

6.3 Active-set semantics: only active records participate. A record is active
when `getattr(record, "superseded_by", None) is None` (the Increment 2 / design
§8 active-set rule, identical to `engine/idea_development_outputs._active_records`).
Superseded and inactive anchors MUST be excluded BEFORE derivation. Gap anchors
use `IdeaState.get_open_gaps()` (status `OPEN` or `PARTIAL`).

6.4 Supported primary anchors are exactly the five in `C4-R1`: assertion; gap;
active contradiction; pending empirical evidence; pending specialist input. Each
active anchor yields exactly one `DerivedRequirement`. A recommendation MAY
appear ONLY as a `SupportingReference`, never as a primary anchor; maturity MUST
NOT be a primary anchor.

6.5 Deterministic anchor derivation (contract-frozen; anchor assignment only —
carries NO severity or priority meaning).

Contradiction primary-anchor unit (F-2; design D-3): the contradiction
primary-anchor unit is the deterministic, order-normalized PAIR of two active
record IDs in conflict (`INCREMENT_4_DESIGN.md` §8 / D-3). Accordingly:

1. exactly ONE `DerivedRequirement` is produced per UNIQUE active contradiction
   pair (a pair `(a, b)` exists when `a` is active, `b` is active, and `b` is in
   `a.contradicts` — equivalently `a` in `b.contradicts`);
2. a single record MAY participate in more than one pair anchor (a record that
   contradicts two other active records participates in two distinct pairs);
   this pair participation is NORMAL and is NOT a record-duplication error;
3. pair identity is `req:contradiction:{lo}|{hi}` (§6.7), symmetric and
   deterministic, so the same pair yields the same requirement regardless of
   encounter order; identical pairs are deduplicated to one requirement;
4. NO connected-component aggregation is performed in MVP-1 (a chain
   A–B, B–C yields the two pairs (A,B) and (B,C), never a merged A–B–C unit);
5. NO assertion-level winner is selected (the system does not choose which
   conflicting answer is correct — mirroring Increment 3).

Non-contradiction active records: each active `AssertionRecord` that participates
in NO active contradiction pair maps to EXACTLY ONE of the following kinds, by
this precedence:

1. `pending_evidence` — `disposition == DISPOSITION_EVIDENCE_REQUESTED`;
2. else `pending_specialist` — `disposition == DISPOSITION_SPECIALIST_REQUESTED`;
3. else `assertion` — any remaining active content record.

Separately, each open gap (`get_open_gaps()`, deduplicated per §6.7) yields one
`gap` anchor. Thus every non-contradiction active record maps to exactly one
kind, while contradiction requirements are counted per unique pair (a record may
appear in more than one pair requirement). No unique anchor (pair, record, or
gap) is emitted twice.

6.6 Each `DerivedRequirement` restates or organizes ONLY the anchor's recorded
content (`C4-R1`): no invented requirement, no inferred engineering obligation,
no new domain fact. Its fields are exactly the frozen `DerivedRequirement`
structure in §4.1 (realizing the design §6 / D-1 semantic fields): `requirement_id`
(§6.7); `statement` (restated recorded content); exactly one `primary_anchor`
(`ProvenanceAnchor`); `supporting_references` (tuple of `SupportingReference`);
`source_status` (§4.2 vocabulary); `criticality` (§9.7); `criticality_authority`
(§9.7); `criticality_rationale` (required only for a non-`UNDETERMINED`
category, else `None`); optional `resolving_action` (`ResolvingAction`, §9.9);
and `linked_risk_ids` (a tuple of references into the canonical
`RequirementLandscape.risks`, §9.8 — NOT embedded `GroundedRisk` objects).
Optional fields are truthfully absent (`None` / empty tuple) when the recorded
state does not supply them; nothing is fabricated.

Statement-construction rule (R-4). For single-record anchors (assertion,
pending_evidence, pending_specialist) and the gap anchor, `statement` is the
deterministic restatement of that one anchor's recorded content or canonical
label (the gap statement per §6.7 clause 5). For a contradiction pair the
`statement` is the FIXED, order-independent text:

```text
Resolve the active contradiction between the two recorded answers.
```

The same exact statement is used for EVERY contradiction pair; it MUST NOT
concatenate the two free-text answers, MUST NOT select or infer a winning
answer, and does not vary with encounter order. Pair-specific identity and
provenance come from the normalized pair (§6.7) and the human-readable
provenance, not from the statement.

6.7 Identifier contract (deterministic, order-independent; `C4-R3`, design §8).
The `DerivedRequirement` identifier MUST be derived from the anchor's own stable
identity and MUST NOT depend on global output order:

- assertion → `req:assertion:{record_id}` (`record_id` is the stable append-only
  `rec_N`);
- gap → `req:gap:{gap_type}` (F-1). `gap_type` is the current model's logical gap
  key: the `Gap` model (`engine/idea_state.py`) has NO stable unique identifier
  beyond its logical type, and `IdeaState.get_gap()` treats `gap_type` as the
  lookup identity. Duplicate-gap canonical reconciliation (F-1 / R-3) — the exact
  MVP-1 rule for multiple active gap objects sharing one `gap_type`:
  1. they form ONE logical gap anchor `req:gap:{gap_type}`; duplicates create NO
     additional requirement identity;
  2. canonical representative selection: choose the object with the SMALLEST
     numeric `opened_at`;
  3. if multiple objects share that smallest `opened_at`, they are
     INDISTINGUISHABLE duplicate representations of the same logical anchor and
     MUST NOT be ordered or selected by list position (they collapse to the one
     anchor);
  4. source-status reconciliation: if any duplicate is `OPEN`, the emitted
     `source_status` is `open`; otherwise, if at least one is `PARTIAL`, it is
     `partially addressed` (per §4.2);
  5. statement: derived from the canonical human-readable gap label for
     `gap_type` (§9.10.5 label map); it MUST NOT choose arbitrary duplicate
     free-text content and MUST NOT concatenate conflicting duplicate text;
  6. provenance: the primary anchor remains the single logical `gap_type`;
  7. conflicting or malformed optional duplicate fields are ignored unless
     structurally required, and MUST NOT fabricate content;
  8. future support for distinct same-type gap instances requires a separately
     authorized state-model amendment and is OUTSIDE MVP-1;
- active contradiction → the order-normalized pair
  `req:contradiction:{lo}|{hi}` where `lo`/`hi` are the two participating
  `record_id`s ordered by the same numeric-`rec_N`-then-lexical rule used for
  ordering (§8); the pair is symmetric so the identifier is stable regardless
  of which partner is encountered first;
- pending evidence → `req:evidence:{record_id}`;
- pending specialist → `req:specialist:{record_id}`.

No requirement identifier — for any anchor kind — MAY depend on input list
position or first-encountered index; every identifier derives solely from stable
per-anchor keys (`rec_N`, `gap_type`, or the normalized `rec_N` pair).

Future-splitting reservation: when a future increment produces multiple
requirements from one anchor under `C4-R2`, the identifier appends a
deterministic source-local discriminator using the reserved suffix
`::{discriminator}`. The `::` suffix is RESERVED now and MUST NOT be emitted in
MVP-1 (no splitting occurs). No discriminator syntax beyond the reserved `::`
marker is fixed by this contract.

## 7. Provenance contract (C4-R1, D-1, D-7)

7.1 Every `DerivedRequirement` MUST have exactly one `ProvenanceAnchor`
(`anchor_kind` ∈ {`assertion`, `gap`, `active_contradiction`,
`pending_evidence`, `pending_specialist`}; `anchor_reference` = the stable
reference used in §6.7). No requirement MAY exist without a primary anchor.

7.2 `SupportingReference`s (R-1): (1) are DEDUPLICATED by `(reference_kind,
reference)`; (2) after deduplication are sorted lexically by `(reference_kind,
reference)`; (3) `display_label` participates in NEITHER identity NOR ordering;
(4) input iteration order MUST NOT affect supporting-reference order; (5)
repeated derivation and any reordered but logically equivalent input produce an
EQUAL supporting-reference tuple. They MUST use existing stable references (e.g.
a recommendation's stable reference); provenance MUST NOT be invented from free
text.

7.3 Raw internal enum values (dispositions, gap-type tokens, provenance/
validation constants, anchor-kind tokens, identifier strings) MUST NOT leak into
user-facing output; the deliverable section MUST render human-readable labels
only (mirroring the Increment 3 deliverable, which omits raw gap-type enums).

7.4 Unresolved or genuinely empty state degrades safely to the defined empty
state (§9.10) without error. Malformed individual records are distinct: they
degrade safely through per-record handling under §9.10.6 — each malformed
record is skipped independently, valid anchors continue to render, and the
landscape becomes empty only when no valid active anchor remains.

## 8. Deterministic ordering contract (C4-R3, D-3)

8.1 Ordering is a SEPARATE deterministic function of `(anchor-kind display
precedence, anchor stable key)`, reproducible and INDEPENDENT of identity and of
input record order. It reuses Increment 3's deterministic DISPLAY techniques
(stable numeric-`rec_N` key, then `iteration` / `opened_at`) but introduces NO
new tie-break axis. Every requirement's display order is fully determined by
canonical stable keys (R-2): NO positional tie-break — first-encountered index,
insertion position, or input list position — is permitted, for identity OR for
display. Because every stable key (`rec_N`, `gap_type`, the normalized pair) is
unique per anchor, ordering is total. If two candidates ever remained
indistinguishable under all authorized stable keys, they MUST be collapsed
(e.g. the gap-duplicate collapse, §6.7) or treated as malformed (§7.4), NEVER
positionally ordered.

8.2 Anchor-kind display precedence is a documentation-order convenience for a
stable, readable landscape and CARRIES NO SEVERITY, PRIORITY, OR IMPORTANCE
MEANING. It MUST NOT be described to the user as a ranking. It MUST NOT be
copied from or equated with the Increment 3 seven-level priority, and it does
not change Increment 3's selected result. Frozen display precedence:
`active_contradiction` (0) → `pending_evidence` (1) → `pending_specialist` (2) →
`assertion` (3) → `gap` (4).

8.3 Within an anchor kind, order by the stable key:
- assertion / pending_evidence / pending_specialist: numeric `rec_N` ascending
  (valid `rec_N` before any non-`rec_N`; then earliest `iteration`) — the display
  staging of `engine.idea_development_outputs._record_sort_key`; the `rec_N`
  identity is unique, so ordering is fully determined by it;
- gap: by `gap_type`, then `opened_at` (both stable; one anchor per `gap_type`
  after §6.7 collapse, so no index tie-break is used);
- active_contradiction: by the order-normalized pair key (the `(lo, hi)` numeric
  pair), ascending.

8.4 `SupportingReference` ordering within a requirement is the canonical lexical
sort by `(reference_kind, reference)` after deduplication (§7.2), NOT
first-encountered order; it is independent of input iteration order.

8.5 Risk ordering (only when risks exist; none in MVP-1): the canonical
`RequirementLandscape.risks` tuple (§4.1, §9.8) is ordered by the first linked
`requirement_id` (in requirement order), then by the grounded-consequence stable
reference; `risk_id`s and `linked_requirement_ids` are deduplicated. Risk order
never depends on input list position.

8.6 The derivation MUST be reproducible: the same `IdeaState` yields an EQUAL
`RequirementLandscape`; reordering input records MUST NOT change any identifier
or the rendered result.

## 9. Contract clauses

### 9.7 Criticality contract (C4-R4, C4-R5, D-4)

9.7.1 Permitted `criticality` category values (string), exactly four:
`FEASIBILITY-THREATENING`, `VALUE-ENHANCING`, `REFINEMENT`, `UNDETERMINED`.
The default and the MVP-1 value for every requirement is `UNDETERMINED`.

9.7.2 Criticality is DERIVED, not stored. It MUST NOT depend on maturity,
readiness, stage, scoring, or progression, and maturity alone MUST NEVER ground
it.

9.7.3 A non-`UNDETERMINED` category MAY be produced ONLY from an explicitly
represented, structurally addressable, deterministic repository signal whose
recorded meaning directly supports that category. Elevation MUST NOT arise from:
free-text wording; keywords; domain inference; maturity; safety-language
heuristics; specialist wording without structured confirmation; or any LLM
judgment. Where no explicit deterministic structural signal exists, the result
MUST be `UNDETERMINED`.

9.7.4 MVP-1 expectation (design §9): the current repository holds no
structurally addressable essential-function-impact signal; therefore MVP-1
derives `UNDETERMINED` for EVERY requirement. This contract invents NO such
signal and MUST NOT introduce one.

9.7.5 Permitted `criticality_authority` values (string), exactly four:
`system-derived`, `owner-confirmed`, `specialist-confirmed`, `undetermined`.
The visible output MUST display the authority. A system inference MUST NEVER be
presented as `owner-confirmed` or `specialist-confirmed`.

9.7.6 MVP-1 authority reachability (design §9 L191-192, §11): because the system
deterministically applies the D-4 rule set to a well-formed active anchor and
yields the `UNDETERMINED` category, the MVP-1 authority for every emitted
requirement is `system-derived`. `owner-confirmed` and `specialist-confirmed`
are DEFINED but not reachable in MVP-1 (no confirmation field exists) and are
reserved for a separately authorized future confirmation workflow. `undetermined`
authority is DEFINED and RESERVED for a state so malformed/empty that no rule
could be applied; MVP-1 emits requirements only for well-formed active anchors,
so the normal MVP-1 authority is `system-derived`. (This reconciles design §9's
"authority system-derived" with the §11 vocabulary; it is a contract-selected
precision, not new authority.)

9.7.7 No numeric scores. Every non-`UNDETERMINED` category MUST carry a recorded
rationale referencing its deterministic structural grounding. The system MUST
NOT independently assert safety, regulatory, or specialist severity. User-visible
criticality wording MUST remain truthful and MUST NOT overstate certainty.

### 9.8 Risk contract (C4-R6, D-5)

9.8.1 A requirement-linked `GroundedRisk` exists ONLY when the recorded state
contains an explicitly represented, structurally addressable adverse-consequence
signal for failing the requirement. An unmet, open, or `UNDETERMINED`
requirement alone MUST NOT create a risk. The system MUST NOT create a generic
risk by merely restating that a requirement is unmet, and MUST NOT parse or
semantically classify free text (contradictions, acknowledged unknowns,
assertions, gaps, pending needs) into a consequence. No LLM, heuristic, keyword
detector, or domain inference may manufacture the consequence.

9.8.2 Zero linked risks is a VALID and conformant result. MVP-1 expectation
(design §10): the current repository holds no structural adverse-consequence
signal; therefore MVP-1 emits ZERO requirement-linked risks
(`RequirementLandscape.risks` is empty).

9.8.3 Zero recorded grounded risks MUST NEVER be presented as, or allowed to
imply, "risk-free", "safe", "no risk", or "verified". The deliverable MUST use
this bounded truthful empty-risk wording (or wording of equivalent meaning that
preserves every clause): "No structurally grounded risks are recorded for the
current requirements. This is not a statement that the idea is risk-free, safe,
or verified; it means no structural adverse-consequence signal exists in the
recorded state."

9.8.4 Risk source of truth (F-6). There is exactly ONE canonical risk store:
`RequirementLandscape.risks` (a tuple of `GroundedRisk`, §4.1). A `GroundedRisk`
object is stored EXACTLY ONCE there. A `DerivedRequirement` MUST NOT embed
duplicate `GroundedRisk` objects; it references risks only by
`linked_risk_ids: tuple[str, ...]`. The required bidirectional consistency
invariant:

- every `DerivedRequirement.linked_risk_ids` entry MUST resolve to exactly one
  `GroundedRisk` in `RequirementLandscape.risks`;
- every `GroundedRisk.linked_requirement_ids` entry MUST resolve to an emitted
  `DerivedRequirement`;
- the two directions MUST be mutually consistent (a requirement lists a risk iff
  that risk lists the requirement);
- `risk_id`s, `linked_risk_ids`, and `linked_requirement_ids` are deterministic,
  ordered, and deduplicated (§8.5).

In MVP-1 both `RequirementLandscape.risks` and every
`DerivedRequirement.linked_risk_ids` are normally EMPTY (§9.8.2).

9.8.5 When risks exist (future only): each `GroundedRisk` carries only the fields
in §4.1 (forced by `C4-R6`): `risk_id`, `linked_requirement_ids`, `consequence`,
`grounding_references`, `authority`, `status`, `rationale`. `risk_id` is
deterministically derived from the grounded structural consequence reference and
the linked requirement IDs, never from list position. Risks are derived, never
stored across sessions, and cause no lifecycle mutation. The existing `_s6` risk
register MUST remain unchanged; this risk view is additive and separate. A
professional risk-management workflow remains excluded.

9.8.6 Future-only `GroundedRisk` boundary. `GroundedRisk` construction is
UNREACHABLE in MVP-1 because the current authorized state contains no
structurally grounded adverse-consequence signal. Therefore: current tests MUST
verify the empty-risk result and the truthful disclaimer (§9.8.3); current tests
MUST NOT invent non-empty risk `authority`/`status` vocabularies. Before any
future non-empty `GroundedRisk` implementation, a separately authorized contract
amendment MUST freeze the exact `risk_id` encoding, the risk `authority`
vocabulary, the risk `status` vocabulary, and the grounded-consequence reference
format. This clarification does NOT change the canonical risk source-of-truth
model (§9.8.4): `RequirementLandscape.risks` remains the single canonical store.

### 9.9 Increment 3 boundary (C4-R7)

9.9.1 Increment 4 reads the same existing `IdeaState` INDEPENDENTLY. It MUST
NOT call, wrap, replace, or modify `derive_next_development_step(state)`, its
inputs, its payload fields, its selected result, or the seven-level Increment 3
priority. `engine/idea_development_outputs.py` and
`tests/test_increment_3_visible_outputs.py` remain byte-identical.

9.9.2 The optional resolving action is the frozen `ResolvingAction` type (§4.1:
`action_kind`, `statement`, `source_reference`), carried on
`DerivedRequirement.resolving_action` (or `None`). It restates recorded state
only (inventing no obligation). The `action_kind` vocabulary is FROZEN, exactly
one per anchor kind (R-5), with fixed statement templates:

```text
assertion            -> action_kind: validate_recorded_answer
                        statement:  "Validate the recorded answer against the
                                     available evidence."
gap                  -> action_kind: address_open_gap
                        statement:  the exact frozen template
                                    "Address the open gap: {gap_label}." where
                                    {gap_label} is substituted ONLY from the fixed
                                    canonical human-readable gap-label map (§9.10.5);
                                    the glue text is exactly "Address the open gap: ",
                                    the statement ends with exactly one period, no
                                    raw gap_type token is displayed, and no free-text
                                    or LLM phrasing is permitted
active_contradiction -> action_kind: reconcile_recorded_contradiction
                        statement:  "Reconcile the conflicting recorded answers
                                     without assuming either is correct."
pending_evidence     -> action_kind: provide_requested_evidence
                        statement:  "Provide the requested empirical evidence."
pending_specialist   -> action_kind: obtain_requested_specialist_input
                        statement:  "Obtain the requested specialist input."
```

No other `action_kind` exists in MVP-1. All statements are fixed templates or
fixed-label substitutions — no LLM or free-text invention. `ResolvingAction` is
a DISTINCT type and label from the Increment 3 global "Next Development Step" and
MUST NEVER be called, presented, or treated as the global next step. Increment 3
remains closed.

### 9.10 Deliverable-only presentation contract (C4-R11, D-7)

9.10.1 MVP-1 presentation is DELIVERABLE-ONLY: exactly ONE additive deliverable
section (`section_13_requirement_landscape`, title "Requirement Landscape").
There MUST be NO `web/app.py` change and NO `web/templates/session.html` change;
the compact session summary remains excluded (`C4-R11` OPTIONAL; design §3).

9.10.2 Required visible fields (human-readable): requirement statement;
human-readable provenance; source-mirrored status; criticality category;
criticality authority; grounded rationale (only where a non-`UNDETERMINED`
category exists); linked risk only where a grounded adverse consequence exists;
requirement-specific resolving action when supported; supporting references when
present.

9.10.3 Rendering safety: no raw enum or internal identifier leakage; Jinja
autoescape preserved; a DEFINED empty state (idea-development-framed, not an
error, not a fabricated problem — mirroring the Increment 3 non-actionable
precedent) applies ONLY when no valid active anchor remains — not merely
because malformed records exist; malformed individual records instead degrade
safely through per-record handling under §9.10.6 (each skipped independently
while valid anchors continue to render); risks render only where present with
the §9.8.3 wording when none exist.

9.10.4 Visible product value: the section MUST show the COMPLETE active,
provenance-anchored requirement landscape (every active anchor's requirement,
each traced to its recorded origin, with source-mirrored status and, where
supported, a distinctly labelled resolving action). This is a distinct
idea-development improvement over the Increment 3 single next step and over the
heuristic `_s4`. The contract MUST NOT oversell the criticality or risk columns:
in MVP-1 they are honestly `UNDETERMINED` / empty. No engagement optimization and
no new user workflow are introduced.

9.10.5 Display labels (R-6). Every `display_label` (on `ProvenanceAnchor` and
`SupportingReference`) and every human-readable status/action string comes from a
deterministic, contract-defined label source; NO display label is generated from
free text. Permitted label sources are: fixed anchor-kind labels (one per the
five anchor kinds); the existing canonical human-readable gap-label mapping (the
`_GAP_LABELS`-style map used by the current deliverable); and fixed
supporting-reference-kind labels. Raw IDs and raw enum tokens remain hidden
(§7.3).

9.10.6 Malformed records (R-6). (1) A malformed optional individual record is
skipped INDEPENDENTLY; (2) one malformed record MUST NOT collapse the entire
landscape into the empty state; (3) valid anchors continue to render;
(4) the whole landscape is empty ONLY when no valid active anchor remains;
(5) malformed contradiction edges with a missing or inactive partner are ignored
(no pair is emitted); (6) malformed supporting references are omitted
individually; (7) no malformed data causes invented fallback content.

9.10.7 Empty-requirement state versus zero-risk state (R-6) — two DISTINCT
presentation states:
- Entirely empty landscape: shown ONLY when no valid active requirement exists;
  it displays the idea-development empty-state message (§9.10.3) and MUST NOT
  display the zero-grounded-risk disclaimer.
- Requirements exist, risks empty: shows all requirements AND the bounded
  zero-grounded-risk disclaimer from §9.8.3; it MUST NOT claim safety,
  verification, or risk-free status.

### 9.11 Tests-first contract (C4-R13, design §16)

9.11.1 Tests-first work MUST NOT begin until this contract is committed and
merged AND a separate tests-first authorization is issued. This contract creates
NO tests.

9.11.2 Future Increment 4 test path (frozen): `tests/test_increment_4_requirement_landscape.py`.

9.11.3 Governed pre-source form (frozen, F-3): `PLAIN PRE-SOURCE FAILING TESTS`,
adopting the Increment 3 frozen-tests-first precedent. The tests-first package
MUST:

- contain normal `pytest` tests;
- contain NO `xfail`, `skip`, or conditional implementation-absence markers;
- be authored BEFORE source implementation;
- fail or error because the required implementation does not yet exist (e.g. a
  missing `engine.requirement_landscape` module/function, a missing additive
  deliverable section, or a missing rendered field);
- remain UNCHANGED during source implementation;
- pass AFTER the authorized source implementation satisfies this contract.

Precedent accuracy: the Increment 3 frozen tests-first package
(`tests/test_increment_3_visible_outputs.py`) uses exactly this plain-test form
(no markers; expected to fail by implementation-absence; unchanged and green
after source). Increment 2 used a DIFFERENT precedent — `pytest.mark.xfail(strict=True)`,
whose true semantics report an absent behavior as XFAIL (the suite stays green)
and an unexpectedly-present behavior as XPASS (the suite fails), with the marker
removed once the behavior passed. This Increment 4 contract CHOOSES the
Increment 3 plain-test form, not the Increment 2 strict-xfail form. Tests MUST
verify the ratified rulings and this contract and MUST NOT make product decisions
inside the tests.

9.11.4 The tests-first package MUST cover at minimum: exact active-anchor
derivation (§6.5); one coarse item per active anchor and NO splitting (§6.2);
stable order-independent identifiers per anchor kind (§6.7); provenance presence
and correctness (§7.1); supporting-reference deduplication and ordering
(§7.2/§8.4); deterministic collection ordering (§8); repeated-run stability
(§8.6); source-mirrored status; criticality default `UNDETERMINED` (§9.7.4);
prohibited unsupported elevation (§9.7.3); authority values and rationale rules
(§9.7.5–§9.7.7); zero-risk validity (§9.8.2); grounded-risk creation only
(§9.8.1); no generic risk restatement (§9.8.1); no "risk-free"/"safe"/"verified"
wording (§9.8.3); optional resolving action (§9.9.2); distinction from the
Increment 3 global next step (§9.9); Increment 3 payload and selection
non-regression (§9.9.1); `_s4` and `_s6` byte/behavior preservation (§3, §9.13);
no `IdeaState` mutation (§6.1); persistence exclusion (§9.13); domain isolation
(§9.13); session-summary exclusion (§9.10.1); deliverable package correctness
(key `section_13_requirement_landscape`); rendered deliverable fields (§9.10.2);
empty state (§9.10.3); legacy/malformed compatibility (§9.12); Jinja autoescape;
no raw internal enum leak (§7.3); architecture/import guardrails including
permitted standard-library imports and the sole permitted project import (§5).
It MUST additionally cover (from the corrections): one record participating in
multiple contradiction pairs yields one requirement per unique pair with no
duplicate identical pair, pair symmetry, and NO connected-component collapse
(§6.5); duplicate same-`gap_type` open gaps collapse deterministically to one
gap anchor with no list-position dependence (§6.7); no identifier depends on
input list position or first-encountered index (§6.7, §8.1); risk
source-of-truth bidirectional consistency between `RequirementLandscape.risks`
and `DerivedRequirement.linked_risk_ids` (§9.8.4); and payload immutability with
JSON-safe conversion that does not mutate the payload (§4.1, §4.3, §9.12). It
MUST additionally cover (from the R-corrections): supporting references are
deduplicated and lexically sorted by `(reference_kind, reference)` and are
invariant under input reordering (§7.2, §8.4); no positional/first-encountered
tie-break affects any order (§8.1); duplicate same-`gap_type` gaps reconcile to
one anchor with the smallest-`opened_at` representative, `OPEN`-over-`PARTIAL`
status, and label-derived statement (§6.7); every contradiction pair yields the
identical fixed statement "Resolve the active contradiction between the two
recorded answers." including from the reversed edge / both directions and for a
record in multiple pairs (§6.6); the frozen `action_kind` vocabulary and fixed
statement templates, one per anchor kind (§9.9.2); display labels come only from
the fixed label sources with no free-text and no raw-enum leak (§9.10.5); a
single malformed record is skipped while valid anchors still render, and the
landscape is empty only when no valid anchor remains (§9.10.6); the empty
landscape shows the empty-state message and NOT the zero-risk disclaimer, while a
non-empty landscape with zero risks shows the disclaimer (§9.10.7); and the
empty-risk result with truthful disclaimer, without inventing risk
authority/status vocabularies (§9.8.6).

### 9.12 Compatibility and defensive access

9.12.1 No new required `IdeaState` constructor field is added; the derivation
operates safely on legacy `IdeaState` (empty ledger, no gaps). Defensive
`getattr` is used ONLY where the source already treats an attribute as optional
(e.g. `getattr(state, "assertions", [])`, `getattr(record, "superseded_by",
None)`, `getattr(record, "contradicts", [])`), mirroring
`engine.idea_development_outputs`.

9.12.2 No dynamic-domain dependency: the derivation MUST NOT depend on the
dynamically-attached `state.domain`. It MUST be domain-neutral in engine
semantics.

9.12.3 Payloads are the plain immutable `frozen=True` dataclasses defined in §4.1
(all public-payload collections are tuples; equality is structural); the
assembler renders them to plain JSON-safe dicts/lists/strings (mirroring `_s12`)
without mutating the payload (§4.3). No serialization dependency beyond plain
dict/str/tuple. No circular import (the new module imports only
`engine.idea_state` among project modules, plus permitted standard-library
modules — §5). Malformed optional records MUST NOT crash deliverable assembly;
they are skipped per-record under §9.10.6 while valid records remain.

### 9.13 Explicit exclusions (prohibited in MVP-1)

The following are PROHIBITED: persistence; domain expansion or domain-registry
repair; scoring changes; progression changes; routing changes; lifecycle or
maturity changes; `_s4` and `_s6` modification, consolidation, or migration; a
professional requirements-management workflow; approvals, assignees, due dates,
dashboards, or workflow controls; technical-verification claims; an
owner/specialist confirmation workflow; multi-fragment splitting; any session
presentation; the compact session summary; any LLM inference; any active-anchor
amendment; and any Increment 3 reopening.

### 9.14 Non-authorization and future sequence

9.14.1 Drafting this document authorizes NOTHING to be built. Contract merge
ALONE does NOT automatically authorize tests-first work.

9.14.2 Required future sequence (each a separate, explicit, owner-gated
authorization): (1) strict independent review of this draft; (2) staging;
(3) commit; (4) push; (5) PR creation; (6) independent PR review; (7) true
merge; (8) a separate tests-first readiness/authorization; (9) tests-first
creation, review, commit, push, PR, and true merge; (10) a separate source
authorization; (11) source creation, review, commit, push, PR, and true merge;
(12) post-merge verification; (13) a separate roadmap synchronization. No
roadmap synchronization occurs in the current operation.

## 10. Traceability matrix (rulings + design → contract → future tests)

| Authority | Contract section | Future test category |
|---|---|---|
| C4-R1 formulation authority | §6.4, §6.6, §7.1 | provenance-anchor presence; recommendation supporting-only; maturity-exclusion |
| C4-R2 atomicity | §6.2, §6.7 (reservation) | one coarse item per active anchor; no MVP splitting |
| C4-R3 identity/lifecycle | §6.3, §6.7, §8 | identity/order-independence; lifecycle/superseded; empty/legacy/malformed |
| C4-R4 criticality | §9.7.1–§9.7.4, §9.7.7 | `UNDETERMINED`-default; no-free-text/keyword/maturity/safety/LLM elevation; no numeric score |
| C4-R5 criticality authority | §9.7.5–§9.7.6 | authority display; `system-derived`/`undetermined` only in MVP; no spoofing |
| C4-R6 requirement→risk | §9.8 | no-auto-risk; grounded-consequence only; zero-risk fallback; no generic restatement; no "risk-free" wording |
| C4-R7 Increment 3 boundary | §5, §9.9 | Increment 3 payload/selection non-regression; distinct resolving-action label |
| C4-R8 progression boundary | §3 (PROHIBITED), §9.13 | no maturity/readiness/stage/scoring/progression effect |
| C4-R9 persistence boundary | §6.1, §9.12, §9.13 | statelessness/determinism; persistence isolation |
| C4-R10 domain/specialist boundary | §9.12.2, §9.13 | domain-neutrality; specialist/registry isolation |
| C4-R11 surfaces | §9.10 | deliverable rendering/autoescape; empty-state; human-readable-label; session EXCLUDED |
| C4-R12 `_s4`/`_s6` disposition | §3, §9.13 | `_s4` and `_s6` non-regression |
| C4-R13 tests-first boundary | §9.11 | governs test sequencing (process-verified) |
| D-1 canonical structure | §6.6 | field-presence / truthful-absence |
| D-2 atomicity | §6.2 | coarse-item fallback |
| D-3 identity/ordering | §6.7, §8 | identity/order-independence; superseded-source |
| D-4 criticality | §9.7 | `UNDETERMINED`-default; structural-only elevation |
| D-5 grounded risk | §9.8 | no-auto-risk; grounded-consequence; zero-risk fallback |
| D-6 resolving action | §9.9.2 | requirement-level action vs global-next-step separation |
| D-7 deliverable/fallback | §9.10 | deliverable rendering; autoescape; empty/legacy/malformed |
| Frozen payload data model (F-7) | §4.1, §6.6, §9.9.2 | payload field-presence; frozen immutability; tuple collections; structural equality; JSON-safe conversion |
| Source-status vocabulary (F-7) | §4.2 | source-mirrored status values; no raw-enum leak; CLOSED/ACCEPTED_RISK not emitted |
| Contradiction pair unit (F-2) | §6.5, §6.7 | one requirement per unique pair; multi-pair participation; pair symmetry; no component collapse |
| Gap-identifier collapse (F-1) | §6.7, §8.3 | one anchor per `gap_type`; deterministic duplicate collapse; no list-position identity |
| Risk source of truth (F-6) | §4.1, §8.5, §9.8.4 | single canonical `RequirementLandscape.risks`; `linked_risk_ids` references; bidirectional consistency |
| Tests-first form (F-3) | §9.11.3 | plain pre-source failing tests; no markers; unchanged through source |
| Import boundary (F-5) | §5 | permitted stdlib; sole project import `engine.idea_state`; prohibited set |
| Supporting-reference order (R-1) | §7.2, §8.4 | dedup + lexical `(reference_kind, reference)` sort; input-order invariance |
| No positional tie-break (R-2) | §8.1 | order fully by stable keys; no first-encountered/insertion/list-position ordering |
| Duplicate-gap reconciliation (R-3) | §6.7 | smallest-`opened_at` representative; OPEN-over-PARTIAL status; label-derived statement; no list position |
| Contradiction statement (R-4) | §6.6 | identical fixed statement per pair; no concatenation/winner; order-independent |
| Resolving-action vocabulary (R-5) | §4.1, §9.9.2 | frozen `action_kind` per anchor kind; fixed statement templates |
| Display labels / malformed / empty-states (R-6) | §9.10.5, §9.10.6, §9.10.7 | fixed label sources; per-record malformed skip; distinct empty-landscape vs zero-risk states |
| Future-only risk boundary | §9.8.6 | empty-risk verified; no invented risk vocabularies; future amendment before non-empty risks |

## 11. Candidate file matrix

| Path | Classification | Basis |
|---|---|---|
| `engine/requirement_landscape.py` (new) | REQUIRED | §3.1, §4, §5 |
| `engine/deliverable_assembler.py` | REQUIRED (one additive section + one key) | §3.2, §9.10 |
| `web/templates/deliverable.html` | REQUIRED (one additive section) | §3.2, §9.10 |
| `tests/test_increment_4_requirement_landscape.py` (new) | REQUIRED (after contract + tests-first auth) | §9.11 |
| `engine/idea_state.py` | NOT REQUIRED (no new field) | §3, §6.1 |
| `web/app.py` | NOT REQUIRED (deliverable-only) | §9.10.1 |
| `web/templates/session.html` | NOT REQUIRED (session excluded) | §9.10.1 |
| `engine/idea_development_outputs.py` | PROHIBITED (Increment 3 frozen) | §3, §9.9.1 |
| `tests/test_increment_3_visible_outputs.py` | PROHIBITED (frozen tests-first) | §3 |
| `engine/scoring.py`, `engine/progression_loop.py` | PROHIBITED | §3, §9.13 |
| `_s4` / `_s6` bodies | PROHIBITED (byte/behavior-identical) | §3, §9.13 |
| persistence paths | PROHIBITED | §9.13 |
| domain-registry paths | PROHIBITED | §9.13 |
| active anchors, `CLAUDE.md` | PROHIBITED | §3 |

## 12. Future implementation non-regression matrix

| Protected surface | Required proof at future source review |
|---|---|
| `engine/scoring.py`, `engine/progression_loop.py` | byte-identical |
| `_s4` (`section_4_requirements`) | byte/behavior-identical output |
| `_s6` (`section_6_risks`) | byte/behavior-identical output |
| `derive_next_development_step` + `NextDevelopmentStep` | byte-identical; same selected result for the same state |
| `tests/test_increment_3_visible_outputs.py` | unmodified (frozen) |
| `IdeaState` (fields + methods) | no new required field; no mutation by the derivation |
| persistence / domain-registry paths | untouched |
| `web/app.py`, `web/templates/session.html` | untouched (MVP-1 deliverable-only) |
| active anchors, `CLAUDE.md` | untouched |

## 13. Acceptance gates (for the future implementation, not this draft)

The future tests-first package and source implementation MUST satisfy, at
review: additive three-path scope (§3); frozen names (§4) and frozen payload data
model (§4.1) with source-status vocabulary (§4.2) and JSON-safe conversion (§4.3);
one coarse item per active anchor and no splitting (§6.2); one requirement per
unique contradiction pair with multi-pair participation and no component collapse
(§6.5); stable order-independent identifiers with per-`gap_type` collapse and no
list-position identity (§6.7, §8.1); provenance presence and dedup (§7);
deterministic ordering with canonical supporting-reference sort by
`(reference_kind, reference)` and NO positional tie-break, and repeated-run
stability (§7.2, §8); duplicate-gap reconciliation to one anchor
(smallest-`opened_at`, OPEN-over-PARTIAL, label-derived statement) (§6.7); the
fixed contradiction-pair statement and frozen resolving-action vocabulary
(§6.6, §9.9.2); fixed-source display labels, per-record malformed skip, and
distinct empty-landscape vs zero-risk presentation states (§9.10.5–§9.10.7);
criticality default `UNDETERMINED` with authority `system-derived` and no
unsupported elevation (§9.7); single canonical risk store with bidirectional
requirement↔risk consistency, the future-only risk boundary, and zero-risk
validity with no "risk-free" wording (§9.8); plain pre-source failing tests with
no markers (§9.11.3); Increment 3 and
`_s4`/`_s6` non-regression (§12); persistence/domain/session-summary exclusion
(§9.13); deliverable-only rendering with defined empty-state, autoescape, and no
raw-enum leak (§9.10); legacy/malformed safety (§9.12); architecture/import
guardrails with permitted stdlib and sole project import `engine.idea_state` (§5).
Any wording that creates implementation-contract-exceeding authority, or that
presents zero risks as risk-free, is a blocking defect.

## 14. Non-authorization boundary

This document is a DRAFT IMPLEMENTATION CONTRACT. It authorizes no tests-first
work, no tests, no source, no template change, no product behavior change, no
staging, commit, push, PR, merge, roadmap change, anchor change, or protocol
creation. Every concrete name it fixes is a contract label over a design-required
fact, adding no product signal. The next governed action after this draft is
independently reviewed and (separately) merged is a separate TESTS-FIRST
READINESS/AUTHORIZATION decision — not automatic tests-first or implementation.
