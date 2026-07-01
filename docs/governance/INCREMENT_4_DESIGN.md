# Increment 4 Bounded Design — Atomic Requirements & Criticality-Aware Risk Register

Status:
`PROPOSED BOUNDED DESIGN — NOT AN IMPLEMENTATION AUTHORIZATION`

## 1. Document status and purpose

This document is the bounded, owner-gated DESIGN for Increment 4 (`Atomic
Requirements & Criticality-Aware Risk Register`). It resolves the design
decisions D-1 through D-7 identified by the read-only Increment 4
design/readiness assessment, at the level of semantics and rules only.

This document does NOT:

- authorize source implementation, tests-first work, or an implementation
  contract;
- decide the final module, function, class, payload-field, identifier,
  section-key, or test names (those are deferred to the implementation
  contract);
- modify any source, template, test, roadmap, or anchor;
- stage, commit, push, create a PR, or merge.

The rulings C4-R1 through C4-R13 in the merged
`docs/governance/INCREMENT_4_AUTHORITY_RULINGS.md` are binding authority and
control wherever this design and those rulings could differ. This design adds
no authority beyond faithfully realizing them.

## 2. Binding authority and base

- Authoritative branch: `feature/atomic-json-session-persistence`; design base
  tip `d75568d8510c4bb49bbce06997991c1decb51cd4` (PR #48 governance-sync
  true-merge). The live tip is always resolved from Git; this SHA is a
  document-publication baseline, not a permanent live-tip assertion.
- Product-execution tip remains `b5a8e72b26acc5ddbee355bc69b419ff09152c50`
  (PR #45 Increment 3 SOURCE merge). This design is not itself product
  execution and does not advance that tip.
- Increment 4 authority rulings C4-R1 through C4-R13 are OWNER-RATIFIED AND
  MERGED REPOSITORY AUTHORITY.
- Increment 3 remains closed; `_s4`/`_s6` remain unchanged; persistence remains
  paused and prohibited for Increment 4; the active anchor is unchanged.

## 3. Owner scope decision (binding on this design)

`INCREMENT 4 OPTIONAL SESSION SUMMARY: EXCLUDED FROM THE FIRST MVP DESIGN AND
IMPLEMENTATION CONTRACT`

The first Increment 4 increment is DELIVERABLE-ONLY. The compact session
summary (C4-R11 OPTIONAL) is out of the first MVP design and its future
implementation contract. This is a bounded current-scope exclusion, not a
permanent prohibition; a session surface would require separate later
justification and authorization.

## 4. Product intent (idea-development, not requirements management)

Increment 4 reorganizes and explains ALREADY-RECORDED truthful state from
Increment 2 (assertions, gaps, contradictions, evidence and specialist
dispositions, validation status) into a provenance-anchored, criticality-aware,
evidence-grounded view that helps the inventor SEE what the idea concretely
requires, DISTINGUISH feasibility threats from refinements (or see them
honestly marked undetermined), UNDERSTAND why each requirement exists, and
IDENTIFY grounded risks rather than generic warnings. It adds no new truth.

`InventorAI remains an idea-development platform, not a professional
requirements-management workspace.`

## 5. Realization shape (additive, semantic; names deferred)

Increment 4 is realized as, at most:

- ONE new pure engine derivation (a read-only, deterministic, non-mutating
  function over the current `IdeaState`; it imports only engine state and no
  Flask / route / template / session / persistence / scoring / progression
  code — mirroring the Increment 3 derivation discipline);
- ONE new additive assembler section entry that carries the derived view into
  the deliverable package;
- ONE additive deliverable template section that renders it.

No final code symbol, payload-field, section-key, identifier-prefix, or test
name is fixed here. In particular this design does NOT adopt any
assessment-suggested placeholder name; all concrete names are deferred to the
implementation contract. The derivation is an ADDITIONAL selector: it is not
`derive_next_development_step`, does not call it, and does not alter it.

## 6. D-1 — Canonical derived-requirement structure (semantics only)

Each derived requirement is an immutable, render-time value (frozen-value
style, like the Increment 3 payload) restating or organizing exactly ONE
identified `IdeaState` record. Its semantic fields are:

1. a derived requirement identifier (encoding deferred — see D-3);
2. a requirement statement, restated or organized ONLY from the anchor's
   recorded content (no invented requirement, no inferred engineering
   obligation, no new domain fact — C4-R1);
3. exactly ONE primary provenance anchor, expressed as
   `{ anchor_kind, anchor_stable_reference }`, where `anchor_kind` is exactly
   one of the permitted primary anchors (C4-R1):
   - assertion,
   - gap,
   - active contradiction,
   - pending evidence need,
   - pending specialist need;
4. zero or more supporting references; a recommendation MAY appear ONLY here,
   never as a primary anchor; maturity MUST NOT be an anchor (C4-R1);
5. a source-mirrored status/lifecycle (D-3);
6. a criticality category (D-4);
7. a criticality authority (Section 11 / C4-R5);
8. a criticality rationale, required for every non-`UNDETERMINED` category
   (C4-R4);
9. an optional resolving action, distinctly labeled (D-6 / C4-R7);
10. zero or more linked risks, present only where a grounded adverse
    consequence is recorded (D-5 / C4-R6).

Optional fields are truthfully absent (not fabricated) when the recorded state
does not supply them. The exact container type and field names are deferred.

## 7. D-2 — Atomicity and source-fragment discriminator (C4-R2)

Decision for the first MVP: produce exactly ONE atomic requirement per active
primary anchor — a COARSE item.

Rationale grounded in repository evidence: an assertion's `content` and a gap's
type are free-text / categorical; the repository holds no stable,
machine-addressable "separable concern" fragmentation of that text. Under
C4-R2, when provenance-safe deterministic splitting is not possible the system
MUST preserve one unresolved coarse item rather than invent sub-requirements.
Therefore the first MVP performs NO splitting.

Deferred (not in the first MVP): if a future source provably contains multiple
separable concerns each traceable to a distinct, deterministically addressable
source fragment, additional atomic requirements MAY be produced, each retaining
(1) the same primary provenance anchor, (2) a deterministic source-local
discriminator derived from that fragment, and (3) zero or more supporting
references. The exact discriminator token syntax is deferred to the
implementation contract; no discriminator syntax is fixed here. Splitting MUST
NOT be enabled until such deterministic fragmentation is proven.

## 8. D-3 — Requirement identity, ordering, and lifecycle (C4-R3)

- Identity: the derived requirement identifier MUST be derived deterministically
  from the primary anchor's OWN stable identity and MUST NOT depend on global
  output order:
  - assertion anchor → the assertion record's stable, append-only record
    identity;
  - gap anchor → the gap's stable identity (its type, disambiguated by its
    stable opened-at ordinal when more than one gap shares a type);
  - active-contradiction anchor → the deterministic, order-normalized pair of
    the two stable record identities in conflict;
  - pending evidence / specialist need → the underlying record's stable
    identity.
  When (future) one source yields multiple requirements under D-2, the
  identifier appends the deterministic source-local discriminator. The exact
  identifier encoding is deferred to the implementation contract.
- Ordering: display order is a SEPARATE deterministic function of
  `(anchor-kind precedence, anchor stable key)`, reproducible and independent of
  identity; it introduces no new tie-break axis beyond a stable key. It reuses
  the spirit of the Increment 3 deterministic ordering without altering it.
- Lifecycle: status MUST mirror the source state. Inactive or superseded
  anchors MUST be excluded BEFORE derivation using the Increment 2 active-set
  rule (a record is active when it is not superseded). Requirement status MUST
  NOT be directly editable (it is a render-time derivation).
- Legacy / empty / malformed state MUST return a safe empty set without error.

## 9. D-4 — Criticality derivation boundary (C4-R4)

Criticality describes the EVIDENCED effect of an unmet requirement on the idea.
It MUST NOT depend on maturity, readiness, stage, scoring, or progression, and
maturity alone MUST NEVER ground it. The default is `UNDETERMINED`.

The four categories are the C4-R4 vocabulary; the default is `UNDETERMINED`. A
non-`UNDETERMINED` category MAY be produced ONLY from an explicitly represented,
structurally addressable, deterministic repository signal whose recorded meaning
directly supports that category:

- `FEASIBILITY-THREATENING`: failing the requirement may prevent the idea or
  mechanism from performing its stated essential function;
- `VALUE-ENHANCING`: the requirement improves usefulness, reliability, clarity,
  efficiency, or practical value but is not necessary for the essential function;
- `REFINEMENT`: the requirement improves an already viable or validated element
  without threatening the essential function;
- `UNDETERMINED`: no deterministic structural signal directly supports another
  category.

Determinism boundary (mandatory): ordinary free-text content, contradiction
text, gap text, pending-evidence text, provenance, maturity, quality, or
validation status alone MUST NOT be semantically interpreted as proof of
essential-function impact. No LLM, heuristic, keyword detector, or domain,
safety, regulatory, or specialist inference may elevate criticality. Where no
explicit deterministic structural signal directly supporting a category exists,
the correct result is `UNDETERMINED`. In the current MVP repository no such
structurally addressable essential-function-impact signal exists; therefore the
first MVP derives `UNDETERMINED` for every requirement (authority
`system-derived`). This is expected and is an honest signal, not a defect.

Constraints: no numeric scores; every non-`UNDETERMINED` category MUST carry a
recorded rationale referencing its deterministic structural grounding; the
system MUST NOT independently assert safety, regulatory, or specialist severity.
This design invents NO new repository field and authorizes NO source change. Any
future elevation rule requires separate implementation-contract precision and
MUST remain within C4-R4.

## 10. D-5 — Grounded adverse consequence and risk traceability (C4-R6)

An unmet or `UNDETERMINED` requirement MUST NOT automatically produce a risk,
and the system MUST NOT create a generic risk by merely restating that a
requirement is unmet.

A requirement-linked risk is emitted ONLY when the recorded state contains an
explicitly represented, structurally addressable adverse-consequence signal for
failing the requirement. Ordinary free-text content MUST NOT be parsed or
semantically classified as a consequence in the first MVP: contradictions,
acknowledged unknowns, assertions, gaps, and pending needs create NO risk merely
because their prose could imply harm. No LLM, heuristic semantic classifier,
keyword detector, or domain inference may manufacture the consequence.

If the current repository lacks a structural adverse-consequence signal, ZERO
risks is the mandatory and conformant result. In the current MVP repository no
such structural signal exists; therefore the first MVP emits zero
requirement-linked risks. Future structural adverse-consequence support requires
separate authority and design.

Traceability chain (applies only when a structural consequence signal exists in
a future increment):
`requirement → primary provenance anchor → supporting evidence or contradiction
→ structurally grounded adverse consequence → risk entry (when present)`.

Cardinality (future, when risks exist): one requirement MAY have zero or more
risks; one risk MAY be supported by one or more requirements.

A future risk entry would carry only the fields FORCED by C4-R6: linked
requirement reference(s), the structurally grounded consequence, grounding
reference(s), an authority, a status, and a rationale. No schema or field name is
fixed here. The existing `_s6` risk register MUST remain unchanged; this risk
view is additive and separate.

## 11. Criticality authority (C4-R5)

Each criticality label MUST carry an explicit authority, exactly one of:
`system-derived`, `owner-confirmed`, `specialist-confirmed`, `undetermined`.
The visible output MUST display the authority. A system inference MUST NEVER be
presented as owner-confirmed or specialist-confirmed.

First-MVP reachability from existing state: because the repository holds no
criticality-confirmation field, the first MVP produces only `system-derived`
(for a category derived under the D-4 rule set) or `undetermined`.
`owner-confirmed` and `specialist-confirmed` are DEFINED but not reachable in
the first MVP and are reserved for a separately authorized future
confirmation workflow (deferred). The existing Increment 2 pending-specialist
signal MAY be surfaced only.

## 12. D-6 — Resolving action and distinct label (C4-R7)

Each requirement MAY carry an optional resolving action, restating recorded
state only (inventing no obligation), derived from the anchor kind — for
example: provide the requested empirical evidence; obtain the requested
specialist input; reconcile the conflicting recorded answers (the system does
not choose a winner); validate the provisional or owner-stated answer; address
the open gap.

This action MUST carry a label DISTINCT from the Increment 3 global "Next
Development Step" and MUST NOT be presented or treated as the global next step.
Increment 3's `derive_next_development_step`, its inputs, its payload fields,
and its selected result are NOT modified.

## 13. D-7 — Deliverable surface, empty-state, and rendering safety (C4-R11)

CORE surface: exactly ONE additive Increment 4 deliverable section (final
section key deferred). Required visible fields (human-readable): requirement
statement; human-readable provenance; source-mirrored status; criticality
category; criticality authority; grounded rationale; linked risk only where a
grounded adverse consequence exists; requirement-specific resolving action when
supported; supporting references when present.

Rendering safety and fallback:

- output MUST use human-readable labels and MUST NOT leak raw internal enums or
  identifiers (following the Increment 3 deliverable precedent, which omits raw
  gap-type enums from the rendered deliverable);
- output MUST be autoescaped by the template layer;
- empty-state MUST be defined: when no active anchors yield requirements, the
  section renders a defined idea-development-framed empty statement (not an
  error, not a fabricated problem), mirroring the Increment 3 non-actionable
  precedent;
- legacy or malformed state MUST degrade safely to that same empty state;
- risks render only where present.

No session surface is designed or rendered in the first MVP (Section 3).

## 14. Additive boundary and non-regression (C4-R7 / R8 / R9 / R10 / R12)

The first MVP MUST be added WITHOUT modifying: R-1 through R-6; the seven-level
Increment 3 priority; `derive_next_development_step`, its inputs, its payload,
or its selected result; `_s4` (requirements); `_s6` (risk register); persistence;
the domain registry; any specialist workflow; the active anchor. The only
Increment 3 template change permitted is the addition of ONE deliverable
section.

Overlap between the new output and `_s4`/`_s6` is acknowledged and is expressly
NOT resolved by Increment 4; any consolidation or migration is DEFERRED and
requires separate authorization.

Progression / persistence / domain boundaries: the derived output MUST have no
effect (direct or indirect) on maturity, readiness, stage, scoring, or
progression; MUST be derived, stateless, non-persistent, dependent only on
committed `IdeaState` evidence, and independent of the frozen persistence
worktree; MUST be domain-neutral in engine semantics and MUST NOT expand
domains, repair the domain registry, or create a specialist or professional
requirements-management workspace.

## 15. Statelessness and determinism (C4-R8 / R9)

The derivation MUST be deterministic, stateless, non-persistent, and fully
reproducible from the current `IdeaState`. Same state yields an equal output;
reordering input records MUST NOT change identity or the rendered result
(identity and ordering both derive from stable per-anchor keys); superseded and
malformed records are excluded or degrade to the safe empty set. No persistence
is designed or authorized.

## 16. Test-boundary note (informative; not a test contract, C4-R13)

This section is informative only and creates NO tests and NO test contract.
Tests-first work MUST NOT begin until a separate authorization following the
implementation contract. When authorized, tests will verify the ratified rulings
and the decisions above; they will not make product decisions; they will preserve
Increment 3 and `_s4`/`_s6` unchanged; and session-surface tests remain excluded
by default. The frozen `tests/test_increment_3_visible_outputs.py` must not be
modified.

The matrix below is informative design-to-future-tests traceability ONLY. It
writes no test code, fixes no final test filename, authorizes no tests-first
work, and defines no session tests. Session-surface tests are EXCLUDED from the
first MVP matrix (owner session-summary exclusion, §3).

Authority / decision → future test category:

| Source | Future test category |
|---|---|
| C4-R1 (formulation authority) | provenance-anchor tests (every requirement has exactly one primary anchor from the five permitted kinds); recommendation supporting-only tests; maturity-exclusion tests |
| C4-R2 (atomicity) | coarse-item fallback tests (one requirement per active anchor; no MVP splitting) |
| C4-R3 (identity/lifecycle) | identity/order-independence tests; lifecycle and superseded-source tests; empty/legacy/malformed-state tests |
| C4-R4 (criticality) | `UNDETERMINED`-default criticality tests; no-free-text-elevation tests; no-numeric-score tests; no maturity/safety/regulatory/specialist inference tests |
| C4-R5 (criticality authority) | criticality-authority display tests; no-spoofing (`system-derived`/`undetermined` only in MVP) tests |
| C4-R6 (requirement→risk) | no-auto-risk tests; structurally grounded-consequence tests; zero-risk fallback tests; no generic-restatement tests |
| C4-R7 (Increment 3 boundary) | requirement-level action versus global-next-step separation tests; Increment 3 contract non-regression tests |
| C4-R8 (progression boundary) | no maturity/readiness/stage/scoring/progression effect tests |
| C4-R9 (persistence boundary) | statelessness/determinism tests; persistence isolation tests |
| C4-R10 (domain/specialist boundary) | domain-neutrality and specialist/registry isolation tests |
| C4-R11 (surfaces) | deliverable rendering and autoescaping tests; empty-state tests; human-readable-label (no raw-enum) tests; session-surface EXCLUDED |
| C4-R12 (`_s4`/`_s6` disposition) | `_s4` non-regression tests; `_s6` non-regression tests |
| C4-R13 (tests-first boundary) | (governs test sequencing only; verified by process, not by product tests) |
| D-1 canonical structure | field-presence / truthful-absence tests |
| D-2 atomicity | coarse-item fallback tests |
| D-3 identity/ordering | identity/order-independence, superseded-source tests |
| D-4 criticality | `UNDETERMINED`-default and structural-only-elevation tests |
| D-5 grounded risk | no-auto-risk, structurally grounded-consequence, zero-risk fallback tests |
| D-6 resolving action | requirement-level action vs global-next-step separation tests |
| D-7 deliverable/fallback | deliverable rendering, autoescaping, empty/legacy/malformed-state tests |
| Increment 3 non-regression | Increment 3 contract non-regression; frozen-test non-modification; `_s4`/`_s6` non-regression; persistence/domain/anchor isolation tests |

## 17. Deferred and prohibited

Deferred (out of the first MVP; each needs separate authorization): multi-fragment
atomic splitting and its discriminator syntax; the compact session summary; an
owner/specialist criticality-confirmation workflow; `_s4`/`_s6` consolidation or
migration; richer supporting-reference presentation.

Prohibited (by C4-R1 through C4-R13 and the active roadmap): requirements without
provenance; invented facts or engineering obligations; numeric scoring;
maturity/readiness/stage/progression effects; automatic risk from an unmet
requirement; unsupported safety/regulatory/specialist criticality; persistence in
Increment 4; domain expansion; domain-registry repair; a specialist or
professional requirements-management workspace; any `_s4` or `_s6` modification;
UI redesign; any Increment 3 amendment; any active-anchor amendment.

The following professional requirements-management lifecycle features are
explicitly deferred AND prohibited in the first MVP (the broader
professional-requirements-management-workspace prohibition above continues to
apply): dashboards; workflow controls; approvals; assignments; owners/assignees;
due dates; requirement-state workflow controls; and professional
requirements-management lifecycle tooling.

## 18. Non-authorization boundary and next governed action

This design authorizes nothing to be built. It does NOT authorize: an
implementation contract; tests-first work; source or template changes; final
name selection; staging, commit, push, PR, or merge; roadmap or anchor changes;
persistence, domain-registry, or specialist work; or any Increment 3 change.

The next governed action after this design is independently reviewed and
(separately) merged is a separate IMPLEMENTATION-CONTRACT DRAFTING authorization,
which will fix the concrete module/function/payload/section/identifier/test
names, the exact bounded file scope, and the tests-first boundary — none of
which is decided here.

## 19. Design conclusion

`DESIGN COMPLETE WITH NON-BLOCKING DEFERRED ITEMS — READY FOR STRICT INDEPENDENT
REVIEW`

This conclusion means readiness for STRICT INDEPENDENT REVIEW only. It does NOT
mean readiness for staging, commitment, merge, implementation-contract execution,
tests-first, or implementation. Each of those remains a separate, explicit,
owner-gated authorization.
