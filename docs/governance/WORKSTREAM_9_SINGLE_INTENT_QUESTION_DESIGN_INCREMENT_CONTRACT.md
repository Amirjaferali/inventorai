# Workstream 9 — Single-Intent Question Design: Increment Contract

**Status:** INCREMENT CONTRACT — **docs-only, non-implementing.** Recording (and merging) this contract records the
Workstream 9 scope and gates only; it authorizes **no** BASE RED, tests, code, question-text change, or implementation.
Prepared under the risk-based execution and review model (PR #220), on authoritative tip `1d4b7da9` (Merge PR #234).
First gate of the Workstream 9 lifecycle (Contract → status canonicalization → BASE RED → implementation → HEAD GREEN →
evidence → independent reviews → owner closure).

## 0. Grounding (committed repository evidence only)
- Remediation plan §5/§15: Workstream 9 = **"Single-Intent Question Design" (P2)**, currently **NOT STARTED**;
  Workstreams 1–8 are closed (WS8 closed via PR #234 as no-valid-RED / expressed-intent objectives deferred to WS9/10/11/14).
- Committed question content is served **verbatim** from `docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json`
  via `engine/path_n_questions.py:get_path_n_question(gap_type, iterations_open)` (index into the per-gap variant list).
- Stage 3 questions are sourced verbatim from `STAGE3_QUESTION_SET.md` and embedded in `engine/progression_loop.py`
  (each annotated with a single "Primary Evidence Target", e.g. PMF-E1).
- No unrecorded session narrative is used. Every multi-intent finding below quotes committed question text.

## 1. Current-state problem statement
Several committed user-facing questions bundle **multiple independent intents** into one prompt, so a single answer can
satisfy one part while leaving another unresolved, and the question text, answer expectation, and evaluation target are
not one-to-one. This is confirmed defect class §3.C-13 "Multi-intent questions". Committed multi-intent evidence
(Path N Stage 2 set, quoted verbatim):
- **MI-1 · N-MC-2:** "What are the main parts of your idea … **and** what does each part do?" — (a) enumerate parts, (b) describe each part's function.
- **MI-2 · N-PF-1:** "What would need to be true for this system to work safely, **and** what information would you need later to confirm it?" — (a) safe-operation conditions, (b) future confirmation information.
- **MI-3 · N-PF-2:** "What do you think would keep the system running, **and** what do you not know yet about that?" — (a) sustaining factors, (b) acknowledged unknowns.
- **MI-4 · N-PF-3:** "Are there real-world conditions … that might stop it from working? **Which ones worry you most?**" — (a) enumerate conditions, (b) rank/prioritise.
- **MI-5 · N-BA-1:** "When should the system work, when should it not work, **and** what situations might confuse it?" — three intents (operate / not-operate / confusion cases).
Borderline (bundled but potentially one atomic answer; flagged, not asserted as defects): N-MC-1 ("notice … and respond"),
N-BA-2 ("your idea responsible for … and … someone/something else's job"), N-BA-3 (react-example and stay-quiet example).
Stage 3 candidates (in the WS8-protected Stage 3 set; noted, not primary WS9 targets): PMF-Q1 ("What is happening … and
why does it matter"), EGA-Q2 ("which ones … to proceed, and which ones represent genuine gaps").

## 2. Exact bounded scope
Workstream 9 is bounded to the **single-intent design of existing user-facing questions**: ensuring each question has one
primary intent, one answer expectation, and one observable completion purpose, by **splitting or re-scoping** multi-intent
questions (content-level). It does **not** change journey ordering (WS8), evaluation logic (WS11), unknown-progression
policy (WS12), guided answers (WS13), or follow-up/completion algorithms (WS14), and does **not** build a registry (WS10).

## 3. Definition of a single-intent question
A question is **single-intent** when it has: one primary user decision or information request; one answer objective; one
observable completion condition; one gap/issue context; no hidden secondary task; no combined "describe, compare, justify,
and measure" bundle unless the combined parts are **inseparable for one atomic answer**; and no requirement for the user
to answer **unrelated** technical dimensions in one response.

## 4. In-scope question types and journey stages
- **Stage 2** Path N approved question content (`electronics_electrical_path_n_questions.json`) for gaps
  MECHANISM_COMPLETENESS / PHYSICAL_FEASIBILITY / BOUNDARY_AMBIGUITY.
- **Stage 3** questions (from `STAGE3_QUESTION_SET.md`) **only** to the extent of single-intent conformance analysis,
  respecting each question's existing Primary Evidence Target; any change to Stage 3 content that WS8 protected requires
  the protected-behavior guard (§6).
- Scope is the **content/intent structure** of these questions, not their ordering, evaluation, or rendering.

## 5. Out-of-scope behavior
Not in scope, and must not be silently absorbed: journey ordering / transitions (**WS8**, closed); a question-intent
registry / taxonomy / identifier system / persistent mapping (**WS10**); scoring, semantic evaluation, or answer-quality
redesign beyond the minimum needed to state the question contract (**WS11**); unknown/incomplete-answer progression policy
(**WS12**); guided technical answer generation / specialist guidance (**WS13**); adaptive follow-up / completion algorithm
(**WS14**); guidance consolidation (**WS15**); final deliverable/E2E (**WS16**); **Structured Technical Guidance** (D13
product implementation — no unresolved-subproblem diagnosis, research-term generation, evidence recommendation,
verification-boundary output, or specialist-category logic); **WS-PFV-001**; **Structured Invention Disclosure / Patent
Export**. Also excluded: anything outside the electronics/electrical MVP scope, and the frozen persistence paths.

## 6. Protected behavior from Workstreams 1–8 (must not regress)
WS1 Evidence Lock baseline (tree `a49a51338aaefd82d0f060308464c90dbe68b14c`); WS2 safety signals
(`engine/safety_signal.py`); WS3 deliverable hygiene; WS4 structured criticality; WS5 unified risk/safety; WS6
requirement landscape (`engine/requirement_landscape.py`); WS7 validation plan (`engine/validation_plan.py`); WS8
deterministic ordering / transition coherence / selection-presentation consistency (its retained observable residue).
The known pre-existing `tests/test_domain_registry.py` baseline (31 failures) is out of scope and must be neither fixed
nor worsened. Splitting a multi-intent question must not alter gap taxonomy, scoring, safety extraction, or the WS8
ordering contract.

## 7. Required user-visible outcomes
- Every in-scope question presents **one** primary intent with one answer expectation and one completion purpose.
- A user answering the single asked intent **completes** that question; no hidden second requirement silently remains.
- No safety, criticality, risk, landscape, validation-plan, or ordering behavior changes in substance.

## 8. Deterministic acceptance criteria
- **AC-1:** Each in-scope committed question maps to **exactly one** primary intent (one answer objective, one completion
  condition, one gap context). Deterministic, checkable against committed/redesigned content.
- **AC-2:** No in-scope question requires **two independently answerable** requests or **two unrelated evidence types**
  for a single completion event.
- **AC-3:** Question text ↔ answer expectation ↔ completion target are **one-to-one** for each in-scope question.
- **AC-4:** The **CONFIRMED MULTI-INTENT** questions (N-PF-1, N-PF-2, N-BA-1) are demonstrably **non-compliant** until
  corrected. Questions marked **UNRESOLVED — PENDING BASE RED** (N-MC-2, N-PF-3, N-BA-2, N-BA-3) are **not** asserted
  non-compliant here; their disposition is decided by BASE RED source analysis under Addenda B.1–B.2 and C.1.
  Already-single-intent questions (e.g. N-MC-3, N-MC-4, N-PF-4) remain compliant. (Amended per WS9-FV-1; see Addendum C.)
- **AC-5:** WS1–8 protected outputs are unchanged in substance for protected fixtures.
- **AC-6:** No out-of-scope artifact (WS10–16, STG, WS-PFV-001, SID) is introduced; the `test_domain_registry.py`
  baseline is unchanged.
- **AC-7:** Language variants (where committed/added) preserve the same primary intent and answer objective (§10).

## 9. Proposed BASE RED test classes (NOT created here)
Proposed for a later, separately authorized BASE RED increment (this contract creates **no** tests; final RED count is
derived from source analysis, not fixed here):
- **R1:** a question with two independently answerable requests is rejected / must be split into atomic questions.
- **R2:** a question must not require two unrelated evidence types for one completion event.
- **R3:** surfaced question, expected answer, and completion target align to one primary intent.
- **R4:** Arabic and English variants preserve the same primary intent and answer objective.
- **R5:** a partial answer does not falsely complete a multi-part question.
- **R6:** the committed multi-intent questions (MI-1…MI-5) remain demonstrably non-compliant until corrected.
**Protected classes:** P1 existing valid single-intent questions; P2 WS1–8 safety/risk/requirement/validation/ordering
behavior; P3 unknown/deferred/provisional/abstention states; P4 persistence/resume behavior; P5 bilingual & RTL behavior;
P6 no WS10–16 capability introduced.

## 10. Arabic/English and RTL requirements
The committed Path N content is currently English-only; no Arabic question variants exist in
`electronics_electrical_path_n_questions.json`. Where bilingual variants exist or are added, each variant must carry the
**same single primary intent and answer objective**, preserve RTL presentation semantics, and keep English digits where
already required in generated output. Workstream 9 adds no translation and no directionality change; it only constrains
intent parity across variants.

## 11. Unknown / deferred / provisional / abstention / partial-answer handling
Single-intent redesign must preserve existing acknowledged-unknown capture (`AcknowledgedUnknown`), deferred/provisional
dispositions, and abstention states. A **partial** answer to a (now single-intent) question must not be treated as full
completion, and splitting a formerly multi-intent question must not convert a previously-captured unknown into a silent
completion. WS9 defines no new unknown-progression policy (that is WS12).

## 12. Persistence and resumed-session boundaries
No persistence/schema change. The frozen persistence worktree and paths remain untouched. Resumed-session behavior must
remain stable: the same committed state yields the same served question deterministically
(`get_path_n_question` indexes by `iterations_open`).

## 13. Safety and criticality preservation
Safety-signal extraction (WS2) and structured criticality (WS4) must be unchanged in substance by any single-intent
redesign. A safety-relevant question must not lose its safety-relevant intent through splitting; safety presentation
integrity (WS5) is protected.

## 14. Evidence and regression requirements
A later evidence increment (separately authorized) will use a dedicated directory
`docs/governance/evidence/workstream9_single_intent_question_design/` with a manifest and validator PASS (mirroring
WS6/WS7). Regression: focused suite GREEN; affected-compatibility GREEN; WS1–8 protected battery GREEN; full suite
unchanged except the known `test_domain_registry.py` baseline. Independent implementation + evidence reviews (PASS)
precede owner closure.

## 15. Explicit non-authorization of implementation
This contract authorizes **none** of: tests; BASE RED; production-code change; question-text change; UI change; a
registry or schema; prompt or AI-logic change; database or persistence change; evaluation-behavior implementation;
adaptive follow-up; Workstream 10-or-later work; Structured Technical Guidance implementation; WS-PFV-001 implementation;
Structured Invention Disclosure / Patent Export implementation. It does not build the Workstream 10 Question Intent
Registry; it may describe a **conceptual** primary intent for contract/testing purposes only, without implementing or
prescribing a registry schema. Each later Workstream 9 gate requires its own separate owner authorization. Phase A branch
remains fixed at `57e2fac8`; PR #167 (`74ea297f…`) / PR #162 (`088ab884…`) untouched; product state
`DEMO_READY_WITH_LIMITATIONS`; MVP electronics/electrical-only; AI Coach (WS17) BLOCKED until Workstreams 1–16 owner-closed.

---

# Addendum A — Critical Paid-Product Experience Requirements

**Status:** OWNER-DESIGNATED contract expansion (docs-only, non-implementing). The owner designates Workstream 9 as a
**critical product-conversion, retention, and trust** workstream: the question experience is a major point at which users
decide whether to continue using and paying for the application. This addendum binds the Workstream 9 contract to treat
question design as **both** (1) an evidence-integrity and remediation concern **and** (2) a professional user-experience
and perceived-value concern. It authorizes no UI change, no question-text change, no user research, and no analytics in
this contract-recording gate.

## A.1 User-facing question requirements
Every in-scope user-facing question must:
- default to **plain language** understandable by non-technical inventors;
- **never require prior engineering terminology** merely to progress;
- **ask one clear thing at a time** (consistent with the single-intent definition, §3);
- be **directly connected** to the user's idea and prior answers;
- **avoid sounding like a generic fixed questionnaire**;
- avoid **interrogation fatigue, repetition, jargon, and premature technical depth**;
- **progress** from easier, confidence-building questions toward deeper ones;
- **explain why a question matters** when that explanation provides real value;
- provide **examples or guided choices** where ambiguity is likely;
- support responses such as: *I do not know yet* · *I am not sure* · *show me an example* · *help me understand what is
  needed* · *let me return to this later*;
- **never treat lack of technical knowledge as user failure**;
- **never fabricate** completion, feasibility, certainty, or understanding;
- surface **visible progress and intermediate value** without misleading completion percentages;
- support **save and resume** without losing question context;
- preserve the **same simplicity, intent, and answer expectation in Arabic and English**;
- remain **extensible** to technologies and domains added in the future.

## A.2 Progressive internal translation
The system should progressively translate the user's everyday description into **structured technical meaning
internally**. Technical terminology may be introduced **only when genuinely necessary**, and must then be **explained in
plain language**. This translation is an internal-representation goal; it does not authorize changing question text,
building an evaluator, or implementing a registry in this gate.

## A.3 Engagement vs. manipulation (prohibited)
The contract distinguishes **engagement** from **manipulation** and prohibits:
- exaggerated praise;
- false assurance that an idea is feasible, complete, unique, or ready;
- dark patterns;
- artificial urgency;
- hiding uncertainty;
- optimizing for continued interaction at the expense of correctness.
Truthful uncertainty and evidence integrity (WS2/WS4/WS5 preservation, §13) always take precedence over engagement.

## A.4 User-experience acceptance criteria (deterministic where observable; otherwise evaluated in the future plan A.5)
- **UX-1 First-read clarity:** a question's primary intent is understandable on first read without technical background.
- **UX-2 Answer-expectation clarity:** what a good answer looks like is evident (one answer objective, §3).
- **UX-3 Perceived relevance:** the question connects observably to the user's idea and prior answers.
- **UX-4 Confidence & psychological safety:** phrasing does not imply user failure for not knowing; "I don't know"
  paths exist.
- **UX-5 Fatigue & repetition risk:** no near-duplicate or redundant question within a session for the same gap.
- **UX-6 Early visible value:** intermediate value/progress is surfaced without misleading completion percentages.
- **UX-7 Non-technical accessibility:** progression never requires unexplained engineering terminology.
- **UX-8 "I don't know" handling:** unknown/uncertain responses are accepted and preserved (§11), never scored as
  failure.
- **UX-9 Abandonment/drop-off awareness:** likely abandonment points are identified (future plan A.5), not asserted here.
- **UX-10 Evidence integrity & truthful uncertainty:** no fabricated completion/feasibility/certainty; uncertainty stays
  visible.

UX-1…UX-8 and UX-10 that are observable from question content/structure are testable at the WS9 BASE RED/GREEN gates;
UX-9 and the perceptual dimensions of UX-1/UX-3/UX-4 are evaluated by the future validation plan (A.5), not in this gate.

## A.5 Future validation plan (defined here; NOT performed in this gate)
A later, separately authorized usability/product-evaluation increment must validate the question experience with
representative users: a non-technical inventor with only an early idea; a user with partial domain knowledge; a technical
user; a user who does not know key implementation details; a user resuming an incomplete session; and Arabic and English
users. It must measure UX-1…UX-10 and evidence integrity. **This contract does not conduct user research, change the UI,
modify question text, or implement analytics** — it only defines the future evidence to be gathered under its own owner
gate.

## A.6 Boundary reaffirmed
This addendum is docs-only and authorizes no implementation of any kind (no UI, question-text, evaluator, registry,
analytics, prompt/AI-logic, database/persistence, or downstream workstream). All prohibitions and protections of §5, §6,
§13, and §15 remain in force; Addendum A adds product-experience and truthfulness requirements to the Workstream 9 scope
without expanding it into Workstreams 10–16, Structured Technical Guidance, WS-PFV-001, or Structured Invention
Disclosure / Patent Export.

---

# Addendum B — Independent-Review Resolution (Findings F-1…F-5, before BASE RED)

**Status:** OWNER-AUTHORIZED clarification addendum resolving the independent-review verdict **B — READY WITH
NON-BLOCKING RECOMMENDATIONS** for Draft PR #235. Docs-only, non-implementing. It refines the contract for the BASE RED
design gate; it authorizes no tests, BASE RED, production/question-text/UI change, registry/schema/evaluator/analytics/
persistence/adaptive-follow-up/technology-profile, and no Workstream 10-or-later work. Supersedes §1/§3/§9/§10 wording
where they conflict.

## B.1 (F-1) Operational multi-intent separation rule
A question is **multi-intent** when it contains **two or more answer components** such that **all** of the following hold:
1. one component can be answered fully while another remains unanswered;
2. each component has a **distinct answer objective or completion condition**; and
3. the components are **not jointly necessary** to express one indivisible atomic decision, relationship,
   classification, or description.

A compound question is **single-intent only** when all included parts are **inseparable for one atomic answer**.

**Mandatory diagnostic probes** (applied per question; not implemented in code at this gate):
- **Independent-answer probe:** can one part be fully answered while another is omitted?
- **Completion-divergence probe:** could one part satisfy its completion condition while another remains open?
- **Separate-follow-up probe:** could the unanswered part reasonably be asked later without changing the meaning of the
  answered part?
- **Atomic-dependency probe:** are all parts necessary together to express one indivisible answer?

**Decision:** if the first three probes are **true** and the atomic-dependency probe is **false**, the question is
multi-intent and must be split or redesigned. This rule makes §8 AC-1/AC-2 deterministically applicable at BASE RED.

## B.2 (F-2) Disposition of borderline questions under B.1
Re-evaluated against B.1; recorded contract-level disposition (three states: **CONFIRMED MULTI-INTENT** /
**CONFIRMED ATOMIC-OR-DEPENDENT** / **UNRESOLVED — PENDING BASE RED SOURCE ANALYSIS**). Where committed evidence remains
ambiguous, the disposition is left UNRESOLVED rather than forced.
- **N-MC-2** ("main parts … and what each does"): **UNRESOLVED — PENDING BASE RED.** May be **atomic** when "parts and
  what each does" is one component-to-function mapping answer; may be multi-intent if enumerating parts and describing
  each function have separate completion conditions. BASE RED source analysis decides under B.1.
- **N-PF-3** ("conditions … which worry you most?"): **UNRESOLVED — PENDING BASE RED.** May be **dependent** (ranking
  follows necessarily from the same list → single-intent) but **must be split** if listing and prioritization have
  **separate completion conditions** (completion-divergence probe true).
- **N-BA-2** ("your idea responsible for … and … someone/something else's job"): **UNRESOLVED — PENDING BASE RED**, to be
  decided by the independent-answer and completion-divergence probes (own-responsibility vs. others'-responsibility are
  prima facie independently answerable; likely CONFIRMED MULTI-INTENT if the probes hold).
- **N-BA-3** ("a situation where it should react, and one where it should stay quiet"): **UNRESOLVED — PENDING BASE RED**,
  decided by the same probes (two independent examples are prima facie independently answerable).
The previously "confirmed" MI-1 (N-MC-2) and MI-4 (N-PF-3) are hereby **reclassified to UNRESOLVED — PENDING BASE RED**
under B.1; MI-2 (N-PF-1), MI-3 (N-PF-2), and MI-5 (N-BA-1) remain **CONFIRMED MULTI-INTENT** (each satisfies all three
probes with atomic-dependency false).

## B.3 (F-3) Arabic/English parity — conditional BASE RED status
Arabic/English intent parity **remains a mandatory product requirement** (Addendum A.1, §10) and is **not removed**. It is
**conditional for BASE RED**: the committed Path N content is currently English-only, so **no Arabic-parity RED case may
be fabricated from absent committed content**, and **absence of Arabic content must not be misreported as parity
success**. When Arabic question content is introduced, parity must be verified for: **primary intent; answer objective;
completion condition; technical difficulty; plain-language accessibility; examples and help wording.** **§9 R4 is
amended:** R4 is a **conditional/deferred** class that yields **no** BASE RED case in the current repository and activates
only once committed Arabic variants exist.

## B.4 (F-4) Downstream-boundary tightening (affordance-only)
The following are **question-design affordance requirements only**; WS9 may define **how a single question presents** them
but may **not implement** any downstream mechanism:
- **Guided choices** = bounded examples or answer affordances presented in the question — **not** generated technical
  recommendations (that is **WS13**).
- **Examples** = illustrative, fixed, non-generated wording within the question.
- **"Return later"** = the question **wording and state boundary** are defined — **not** a redesign of progression
  (**WS12**) or persistence mechanisms (persistence remains frozen).
- **Progressive internal translation** (Addendum A.2) = a **future-compatible design principle** — **not** an implemented
  interpretation engine, and not a registry (**WS10**), evaluation/semantic scoring (**WS11**), adaptive follow-up
  selection/completion (**WS14**), Structured Technical Guidance, or Domain Capability Profiles.
WS9 may not implement WS10 registry/taxonomy, WS11 evaluation/scoring, WS12 unknown/deferred progression decisions, WS13
generated guidance/answer coaching, WS14 adaptive follow-up/completion logic, Structured Technical Guidance, or Domain
Capability Profiles.

## B.5 (F-5) UX acceptance-criteria → evidence-method mapping
- **Automated / deterministic repository evidence** (candidates for BASE RED or protected tests): one primary intent; one
  answer objective; one completion condition; no hidden secondary task; presence of approved uncertainty/help affordances
  where required; absence of misleading fixed completion percentages; no prohibited feasibility/uniqueness/readiness/
  completion claims; preservation of question context across existing save/resume behavior **where an observable
  committed seam exists**; Arabic/English parity **only when both committed variants exist** (per B.3).
- **Independent usability / product evidence** (must **not** be represented as unit-test outcomes): first-read clarity;
  perceived relevance; user confidence; psychological safety; professional tone; question fatigue; abandonment risk;
  perceived value; whether explanations and examples are genuinely helpful. These require **representative-user review,
  structured expert review, or another approved usability-evidence method in a later gate** (Addendum A.5). No user
  research or analytics is conducted at this gate.

## B.6 Boundary reaffirmed
Addendum B is docs-only and authorizes no implementation of any kind. All §5/§6/§13/§15 and Addendum A prohibitions and
protections remain in force; nothing here begins BASE RED, implementation, Arabic parity verification, or any downstream
workstream. Phase A branch remains fixed at `57e2fac8`; PR #167/#162 untouched; product state
`DEMO_READY_WITH_LIMITATIONS`; MVP electronics/electrical-only; AI Coach (WS17) BLOCKED until Workstreams 1–16 owner-closed.

---

# Addendum C — Final Drafting Closure (WS9-FV-1, WS9-FV-2)

**Status:** OWNER-AUTHORIZED final drafting clarification resolving the last two independent findings for Draft PR #235.
Docs-only, non-implementing. Authorizes no tests, BASE RED, production/question-text/UI/schema/persistence/analytics/
prompt/AI-logic change, and no Workstream 10-or-later artifact.

## C.1 (WS9-FV-1) AC-4 / Addendum B.2 conflict resolved
The prior §8 **AC-4** wording ("MI-1…MI-5 are demonstrably non-compliant") conflicted with Addendum B.2, which
reclassified N-MC-2 (MI-1) and N-PF-3 (MI-4) to **UNRESOLVED — PENDING BASE RED**. **AC-4 has been amended in place**
(the single justified edit in this addendum's commit) so that it asserts non-compliance **only** for the CONFIRMED
MULTI-INTENT set and defers the UNRESOLVED set — leaving the governing clause self-consistent without requiring the
reader to infer precedence. The final, canonical dispositions are:
- **CONFIRMED MULTI-INTENT:** N-PF-1, N-PF-2, N-BA-1.
- **UNRESOLVED — PENDING BASE RED SOURCE ANALYSIS:** N-MC-2, N-PF-3, N-BA-2, N-BA-3.
No unresolved item is forced into confirmed-defect status; no confirmed item is downgraded. The legacy labels MI-1…MI-5
in §1 are historical evidence notes; the authoritative dispositions are those above and in Addendum B.2, and AC-4 as
amended.

## C.2 (WS9-FV-2) Disposition rule for mixed probe outcomes
Applying Addendum B.1's four diagnostic probes and conjunctive decision rule, the following disposition rule is binding:

- A question is classified **MULTI-INTENT only when all required multi-intent conditions are satisfied** (the conjunctive
  rule of B.1: independent-answer, completion-divergence, and separate-follow-up all true, and atomic-dependency false).
- If **one or more required conditions are not satisfied**, the question **must not be automatically classified as
  multi-intent.** It must instead be classified as either:
  - **ATOMIC / DEPENDENT** — when the committed evidence supports that conclusion; or
  - **UNRESOLVED — PENDING BASE RED SOURCE ANALYSIS** — when the evidence is insufficient or the probe outcomes are
    **mixed**.
- The **absence of a multi-intent classification does not automatically prove** that the question is valid, clear, or
  ready for implementation; a non-multi-intent question may still fail other acceptance criteria (§3, §7, §8, Addendum A).

This clarification **preserves**: the four diagnostic probes (B.1); the conjunctive decision rule (B.1); the three-state
disposition model (B.2: CONFIRMED MULTI-INTENT / CONFIRMED ATOMIC-OR-DEPENDENT / UNRESOLVED — PENDING BASE RED); and the
prohibition against subjective classification based only on question length or the presence of the word "and".

## C.3 Boundary reaffirmed
Addendum C is docs-only and authorizes no implementation. All §5/§6/§13/§15 and Addenda A/B prohibitions and protections
remain in force; nothing here begins BASE RED, implementation, Arabic parity verification, or any downstream workstream.
No claim is made that BASE RED, implementation, Arabic parity, or downstream capabilities have begun or passed. Phase A
branch remains fixed at `57e2fac8`; PR #167/#162 untouched; product state `DEMO_READY_WITH_LIMITATIONS`; MVP
electronics/electrical-only; AI Coach (WS17) BLOCKED until Workstreams 1–16 owner-closed.
