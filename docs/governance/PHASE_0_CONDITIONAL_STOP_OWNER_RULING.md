# PHASE 0 CONDITIONAL STOP — OWNER RULING DOCUMENT

## 1. Status

- PHASE 0 CONDITIONAL STOP OWNER RULING DOCUMENT
- ANALYSIS AND RULING RECORD — nothing in this document implements
  anything
- Rulings R-A through R-G are FILLED by owner decision, 2026-06-12
- This document records rulings; it does NOT amend the integration
  plan and does NOT authorize implementation (see §11)

## 2. Source governance

| Commit | Artifact |
|--------|----------|
| `2c0d2a5` | `PHASE_0_PATH_N_RUNTIME_DISCOVERY_REPORT.md` (the STOP record) |
| `d2b2a9a` | `PATH_N_RUNTIME_INTEGRATION_AUTHORIZATION_PLAN.md` (invariants §4, STOP §9) |
| `26fa3e1` | `PATH_N_CONTENT_CONFIG_ARTIFACT_APPROVAL_RECORD.md` |
| `8ceb5d4` | Path N content config artifact (JSON) |
| `4f0ce81` | Designation-only path interface plan (default = `legacy_undesignated_current_behavior`) |
| `cdcd079` | MVP scope freeze amendment (Functional Path N) |
| — | `ARCHITECTURE_GUARDRAILS.md` (§1 engine independence, §3 stable interfaces, §8 AI boundary) |

## 3. The problem, restated from Phase 0 evidence

FACT (Phase 0, owner-executed inspection at HEAD `d2b2a9a`):

1. `get_question(domain, gap_type, iterations_open)` lives in
   `engine/progression_loop.py`; no parameter can carry a path value.
2. The generic fallback bank `QUESTIONS` is engine-internal.
3. Question text reaches the user from two call sites:
   `web/app.py::show_session()` (display-time) and
   `engine/progression_loop.py::run_iteration()` (iteration-result).
4. No path/designation field exists in `SESSION_STORE` entries or
   `IdeaState`.

Constraint set in tension:

- Plan §4.5: `progression_loop.py` zero net changes.
- Plan §4.11 / NEXT_SESSION invariant 6: no business logic in web routes.
- Guardrails §1: no domain branching in `progression_loop.py`.
- Plan §9: STOP if selection requires modifying `progression_loop.py`.

## 3a. Authorization boundary of this document (binding on its reading)

- The rulings below establish admissibility and direction only.
- An `IdeaState.path` field is NOT authorized for implementation by
  this document.
- Call-site changes inside `engine/progression_loop.py` are NOT
  authorized for implementation by this document.
- Any amendment to integration plan §4.5 requires a separate
  committed amendment document (see §11, "No silent amendment").

## 4. Question 1 — Carrier analysis

### C-1: SESSION_STORE entry (web layer only)

- Reaches: `show_session()` display path only.
- FACT-based defect: `run_iteration(state, response)` receives only
  `state` and `response`; a SESSION_STORE-only path value cannot reach
  the engine's question return paths.
- Forcing consistency would require the web layer to discard/override
  engine-returned questions → question selection logic in routes →
  violates no-business-logic-in-routes.
- Verdict (analysis): NOT VIABLE alone. Admissible only as the web-side
  half of a combined carrier.

### C-2: Additive `IdeaState.path` field

- Reaches: both call sites in principle — `state` is present in
  `show_session()` (via SESSION_STORE) and travels into
  `run_iteration()`.
- Residual requirement: the path value must travel from `state` into
  the lookup. Two sub-variants:
  - C-2a: additive optional parameter on `get_question()`
    (e.g., `path=None`) + call sites read `state.path`.
    Touches `progression_loop.py` (narrow, additive).
  - C-2b: `get_question()` signature unchanged; call sites pass path
    into the domain layer through a new domain-layer function.
    Still touches call sites in `progression_loop.py`.
- Guardrail check: `idea_state.py` is NOT on any frozen/untouched list
  (plan §10 lists `domain.json`, `progression_loop.py`, Path T).
  An additive field with default `"legacy_undesignated_current_behavior"`
  preserves all existing behavior and serialization additively.
- Verdict (analysis): candidate carrier; cannot avoid call-site
  touches in `progression_loop.py` (see Question 3).

### C-4 (recorded for completeness): module-level path context in domain layer

- A settable module variable in `domain_rules.py` consulted by
  `get_domain_question()`.
- Defect: hidden mutable state; breaks determinism transparency
  ("same idea twice = identical IdeaState" auditability); resembles
  the "hidden fallback logic" forbidden by CLAUDE.md.
- Verdict (analysis): REJECT. Recorded so it is not re-proposed later.

**R-A — OWNER RULING: ACCEPT.**
Combined carrier accepted: dedicated web route sets the designation,
stored as additive `IdeaState.path`, consumed by the
domain/question-selection layer. C-1 alone is rejected. C-4 hidden
module-level context is rejected.

## 5. Question 2 — Is an additive `idea_state.py` change admissible?

- FACT: `idea_state.py` is not named in plan §10's untouched list,
  nor in the Phase-blocking table, nor in Guardrails' frozen
  signatures.
- The change would be: one field, default
  `legacy_undesignated_current_behavior`, no behavioral effect for
  any existing value (per `4f0ce81` default rule).
- Risk: `idea_state.py` is engine territory; precedent discipline
  matters. Mitigation: dedicated authorization, dedicated tests
  proving default-value behavioral identity, WPS001 green.

**R-B — OWNER RULING: ACCEPT.**
An additive `IdeaState.path` field is admissible in principle, but
only under separately authorized Phase 1 and with
zero-behavior-change proof.

## 6. Question 3 — Call-site changes inside `progression_loop.py`

This is the heart of the STOP. Statement of the evidence:

- FACT: every carrier analyzed that reaches both call sites requires
  the path value to pass through code inside `progression_loop.py`
  (either a parameter on `get_question()` or a domain-layer call
  made from its call sites).
- Current Phase 0 evidence has not identified a safe
  zero-engine-change integration path. Any claim of feasibility now
  requires either a new evidence-backed design option or a formal
  narrow amendment.

Distinction available to the owner:

- PROHIBITED ZONE (unchanged under every analyzed option): the
  deterministic gates — `evaluate_transition()`, `assess_response()`,
  `integrate_response()` — and all PASS/WARN/BLOCK logic.
  No analyzed option touches these.
- On the relationship between path and domain branching:
  a path parameter is not automatically a domain branch, but any
  implementation must prove it contains no domain literals, no
  domain-specific conditions, and no gate behavior changes.
- CANDIDATE NARROW ZONE: `get_question()` plus its call sites —
  question *content selection*, explicitly the layer the domain
  is supposed to own (FACT: domain_rules.py L71 comment).

**R-C — OWNER RULING: ACCEPT.**
Narrow question-selection plumbing inside `progression_loop.py` is
admissible only if formally amended in the integration plan first.
The allowed zone is limited to question-selection plumbing only.
Deterministic gates remain frozen. No domain literals, no
domain-specific branching, no PASS/WARN/BLOCK changes.

## 7. Question 4 — Dual call-site consistency

- Requirement: `show_session()` and `run_iteration()` must never
  emit different-path content for the same session state.
- Design rule (analysis): both call sites must resolve content
  through ONE shared selection function with identical inputs
  (`domain, gap_type, iterations_open, path-from-state`).
  No site-local path logic.
- Mandatory runtime test (extension to plan §7): for a Path N
  session, display-time question == iteration-returned question for
  the same state; same assertion for legacy sessions.

**R-D — OWNER RULING: ACCEPT.**
Dual call-site consistency is mandatory. `show_session()` and
`run_iteration()` must resolve questions through one shared
selection mechanism, and runtime tests must prove no mixed-path
questions.

## 8. Question 5 — AI-advisor precedence for Path N

- FACT (Phase 0): `get_ai_question(...) or get_question(...)` —
  AI output takes precedence inside `run_iteration()` when non-None.
- ASSUMPTION (NEXT_SESSION.md, 2026-05-22): AI_ADVISORY_ENABLED =
  False — currency unverified at HEAD `d2b2a9a`.
- Risk: if AI is ever enabled, unapproved AI text would override
  approved Path N content, silently bypassing the content approval
  chain (`effd040`, `26fa3e1`).

**R-E — OWNER RULING: ACCEPT.**
For `path = N` sessions, AI advisory must not override approved
Path N content. Path N must resolve deterministically from the
approved artifact unless a future separate governance chain
authorizes AI augmentation.

## 9. Question 6 — Does Option I-A survive Phase 0?

- I-A as written assumed the web layer carries designation and the
  content layer selects. Phase 0 shows the designation must ride in
  `IdeaState` to reach both call sites.
- Revised form **I-A′**: dedicated route (designation only, no
  logic) → `IdeaState.path` (additive) → shared selection function →
  domain-layer loader of the approved JSON artifact (`8ceb5d4`).
  `domain.json` untouched; gates untouched; QUESTIONS fallback
  untouched for legacy paths.
- I-B (registry overlay) remains second choice: wider blast radius,
  registry schema has no path dimension (FACT: validated keys list).

**R-F — OWNER RULING: ACCEPT.**
I-A′ is selected as the preferred direction: dedicated route
designation → additive `IdeaState.path` → shared selection
function → domain-layer loader for the approved JSON artifact.
I-B remains reserve only. I-C remains rejected.

## 10. Question 7 — Disposition of the conditional STOP

Three possible rulings, stated neutrally:

| Disposition | Meaning | Consequence |
|-------------|---------|-------------|
| RESOLVED via narrow amendment | R-C narrow zone admitted; plan §4.5 formally amended in a separate committed document | Phase 1 becomes authorizable after the amendment commit |
| REMAINS CONDITIONAL | More analysis or alternatives demanded | Phases stay blocked; new discovery scope needed |
| CONFIRMED STOP | Zero-engine-change is mandatory and absolute | Functional Path N runtime integration is infeasible as currently scoped; escalation to freeze-amendment review (`cdcd079`) |

**R-G — OWNER RULING: ACCEPT.**
The conditional STOP is resolved only via narrow, formally recorded
amendment. This ruling does not itself amend the integration plan
and does not authorize implementation.

Effect of R-G: the STOP's disposition is RESOLVED-VIA-AMENDMENT in
principle, but its practical blocking effect persists — Phase 1
remains non-authorizable — until the plan §4.5 amendment is
committed as a separate document.

## 11. No silent amendment

This document cannot itself amend the integration plan. The owner
has ruled (R-C, R-G) that narrow question-selection plumbing is
admissible; therefore the integration plan must be amended in a
separate committed document before any Phase 1 implementation
authorization.

## 12. What this document does NOT do

- No implementation. No code, test, or prompt changes.
- No modification of `domain.json`, `web/app.py`,
  `engine/progression_loop.py`, `engine/idea_state.py`, or Path T.
- No amendment enacted. Phase 1 not authorized.
- R2 remains HELD. FORM T remains BLOCKED.
- S-6 remains UNCLASSIFIED. AA-5 remains BLOCKED.

## 13. Sequence after this ruling (informational only)

(1) This ruling document committed — satisfied by the commit of
this file. (2) Plan §4.5 amendment document drafted, owner-reviewed,
committed. (3) Phase 1 authorization (designation field + dedicated
route, with zero-behavior-change tests, WPS001 green). (4) Phase 2
per I-A′. Each step separately authorized, per the established
one-authorization-one-artifact protocol.