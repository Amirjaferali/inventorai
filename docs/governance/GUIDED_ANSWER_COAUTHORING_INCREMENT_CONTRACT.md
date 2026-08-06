# GUIDED ANSWER CO-AUTHORING / "CLARIFY AND BUILD MY ANSWER" — INCREMENT CONTRACT DRAFT

## 0. Status

`GUIDED ANSWER CO-AUTHORING INCREMENT CONTRACT DRAFT — DOCS-ONLY — NO
IMPLEMENTATION AUTHORIZED`

This document defines a **minimal, safe, owner-gated future implementation
contract** for the first possible Guided Answer Co-Authoring increment, derived
from the merged scope decision
(`GUIDED_ANSWER_COAUTHORING_SCOPE_DECISION.md`, PR #125; roadmap-recorded by
PR #126). It is **contract documentation only**. It authorizes NO
implementation, code, test, schema, UI, route, template, runtime, session,
scoring, maturity, readiness, criticality, persistence, or domain change; no
roadmap change in this step; and no `main` synchronization or MVP activation of
any kind.

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/GUIDED_ANSWER_COAUTHORING_INCREMENT_CONTRACT.md`
- Purpose: define the smallest future Guided Answer Co-Authoring increment and
  its hard boundaries, so that a later — separately authorized — implementation
  has an evidence-grounded, anti-drift contract to build against.
- Input contract: the merged scope decision
  (`GUIDED_ANSWER_COAUTHORING_SCOPE_DECISION.md`), the committed dual-path
  product intent (`DUAL_PATH_PRODUCT_ANCHOR.md`), `MVP_SCOPE_FREEZE.md`, and the
  evidence-locked state at authoritative tip
  `3ec137a6eac1768dcdcf22cd6d70360ee0e0e32c`.
- Output contract: a single future-implementation contract draft (§13
  classification) with its objective, boundaries, required future tests,
  guardrails, governance gates, and risks; nothing executable, nothing
  activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, scoring authorization, activation of the Inventor Answer
  Clarification / Improve Wording feature, a roadmap update, or a `main`/frozen/
  quarantined branch change.

---

## 1. Current state (evidence-locked)

- Repository: `Amirjaferali/inventorai`.
- Authoritative branch: `feature/atomic-json-session-persistence`.
- Authoritative tip: `3ec137a6eac1768dcdcf22cd6d70360ee0e0e32c`.
- Latest merged PR: **#126**.
- Official state: **`DEMO_READY_WITH_LIMITATIONS`**.
- MVP scope: **electronics/electrical-only** (`MVP_SCOPE_FREEZE.md`).
- The Guided Answer Co-Authoring scope decision (PR #125) is **merged and
  roadmap-recorded by PR #126**; its current status is **FUTURE OWNER-GATED
  INCREMENT CANDIDATE ONLY**.
- The Inventor-Stated Safety Signals lineage (PR #118–#124) is **fully closed
  and recorded**; no Safety-Signals follow-up is owed and none is reopened here.
- **No implementation is authorized yet.** No product-execution lane is open;
  per roadmap §8, no lane may be inferred, and a separate explicit owner
  authorization is required before any working-tree write or product
  implementation.
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); the frozen persistence worktree
  remains paused and untouched (`aec9cf6409efc18e125b6745762002f59e529654`); the
  quarantined scratch branch remains untouched
  (`02586747c902d5e1ebb78adde54ddd4ecd1c174a`).

---

## 2. Contract objective

Define the **smallest future increment** that helps the inventor write a better
answer **through advisory prompts and bounded guidance**, while **preserving the
inventor as the source of all saved content**. The increment's value is centered
on **idea development** — progressing the inventor's own idea — not on inventor
education as a product identity, and not on answer generation. The system may
prompt and structure; only the inventor authors what is saved.

---

## 3. Proposed increment name

**Guided Answer Co-Authoring Increment 1 — Advisory Prompt Support.**

---

## 4. Proposed user value

Help **non-specialist inventors** (the committed Path N audience;
`DUAL_PATH_PRODUCT_ANCHOR.md` §3) understand **what kind of information would
strengthen their own answer** to a scaffolding question, so they can add their
own specifics. The value stays anchored to **idea development**, not to inventor
education as product identity: the increment elicits and structures the
inventor's own content; it does not teach a curriculum and does not become a
generic tutor.

---

## 5. Strict MVP boundary

- **Electronics/electrical-only.** No domain expansion of any kind.
- **No general writing assistant.** Guidance is scoped to invention scaffolding
  questions, not open-ended prose help.
- **No generic tutor mode.** No lessons, courses, or education-product framing.
- Consistent with `MVP_SCOPE_FREEZE.md` and the scope decision §5, §9: the
  minimal increment must be provable as **display-only / advisory and
  non-mutating** before any implementation.

---

## 6. In-scope future behavior (only if separately authorized later)

A later, separately-authorized implementation **may**:

- show **advisory guidance near a question**;
- show **bounded "what to include" prompts** (category-level, content-free);
- show **examples of categories of information** — not fabricated answers;
- ask **optional follow-up prompts**;
- **encourage the user to add their own specifics**;
- **label all suggestions as advisory** and visibly user-controlled;
- **preserve user-entered text as the only saved answer source**;
- **operate without scoring / readiness / criticality effects.**

These are candidate behaviors for a future increment only; none is implemented
or authorized by this contract.

---

## 7. Out-of-scope behavior (forbidden)

A future implementation **must not**:

- **rewrite** the inventor's answer;
- **silently replace** user text;
- **auto-save** generated text;
- create **approval / save clarified-answer flows**;
- add `original_user_answer` / `suggested_clarified_answer` /
  `user_approved_answer` / `clarification_status` fields (or any equivalent);
- **activate Answer Clarification / Improve Wording**;
- claim an answer is **correct, complete, validated, safe, compliant,
  patent-ready, or engineering-ready**;
- **change scoring** (`assess_response` / `integrate_response` /
  `evaluate_transition` / thresholds / generic-verb trap / causal tokens);
- **change maturity / readiness**;
- **change criticality** (the Increment-4 `criticality` field stays
  `UNDETERMINED` / system-derived);
- **change Section 6 risks**;
- **populate `RequirementLandscape.risks`** (stays `()`);
- **change persistence / session schema**;
- **change the Increment-6 deliverable structure** (the 14 canonical sections +
  `_session_meta` top-level set is pinned;
  `test_traceability_no_orphan_toplevel_keys` forbids new top-level sections);
- **change Increment-5 validation-plan semantics**;
- **reopen Safety Signals** (`engine/safety_signal.py`, the
  `_session_meta.inventor_stated_safety_signals` surface, or the deliverable
  panel).

This forbidden list is the anti-drift core of the contract; any drift toward it
is the (non-authorized) Answer Clarification feature by another name and is out
of scope (scope decision §6, §7).

---

## 8. Suggested implementation surface for a later PR (inspect only — do not change now)

The following are **candidate surfaces to inspect during a later read-only
source review** — they are named from present repository evidence, not
prescribed as edit targets. No file below may be changed by this contract, and
the exact change set must be established by that later review, not assumed here:

- **Existing advisory/scaffolding guidance modules** (evidence of an additive,
  display-only guidance precedent to mirror rather than a schema/scoring path):
  - `web/scaffolding_guidance.py`
  - `web/clarification_labels.py`
- **Question-level display surfaces** (where a bounded advisory panel could
  later render, adjacent to a scaffolding question):
  - `web/templates/decision_workspace.html`
  - `web/templates/session.html`
- **Read-only domain context** already available to a guidance surface (do not
  modify; referenced only to confirm advisory guidance needs no new engine
  mutation):
  - `engine/requirement_landscape.py`

A **later read-only source review is required before any implementation** to (a)
confirm the minimal increment can be delivered purely as display-only/advisory
guidance with **no** persistence/session-schema field, **no** approval/save
flow, and **no** Answer-Clarification interaction; (b) fix the exact, minimal
surface; and (c) prove the §7 forbidden set is untouched. Until that review, no
surface is committed and no code change is prescribed.

---

## 9. Required future tests (for a later implementation)

A future implementation must include tests proving:

1. **Advisory guidance appears** for eligible electronics/electrical scaffolding
   questions.
2. **The saved answer remains user-authored** — persisted answer content equals
   the inventor's own entered text.
3. **Generated guidance is not persisted as the answer** (guidance text never
   becomes stored answer content).
4. **No scoring / readiness / criticality changes** — the locked scoring suites
   (`tests/test_assess_response_replay.py`,
   `tests/test_assess_response_adversarial.py`) and criticality/readiness
   behavior are unchanged (baseline: failures confined to
   `tests/test_domain_registry.py`; zero new failures).
5. **No persistence / schema changes** unless separately authorized — the
   Increment-6 deliverable top-level contract
   (`test_traceability_no_orphan_toplevel_keys`) still holds.
6. **Answer Clarification fields/flows are absent** — no `original_user_answer` /
   `suggested_clarified_answer` / `user_approved_answer` / `clarification_status`
   field or flow exists.
7. **Safety Signals remain untouched** — `engine/safety_signal.py` and the
   `_session_meta.inventor_stated_safety_signals` surface are unchanged.
8. **The electronics/electrical MVP boundary holds** — no domain expansion.

---

## 10. Required wording guardrails (for future UI)

Any future UI wording must clearly state:

- **suggestions are optional**;
- the **user remains responsible for their own answer**;
- **guidance is not validation**;
- **guidance is not safety / compliance / patent / engineering approval**;
- the assistant is **helping the user think through details, not certifying
  correctness**.

Provenance must be visibly distinct: system-offered prompts vs inventor-authored
text must never be confusable (scope decision §12).

---

## 11. Governance gates

This contract draft:

- **does not authorize implementation**;
- **requires independent review** (a separate session; the authoring session
  cannot self-approve);
- **requires owner-gated true merge** (2-parent merge; never squash/rebase);
- **after merge, implementation still requires separate owner authorization** —
  merging this contract does not start any implementation;
- any implementation PR **must be independently reviewed** and owner-gated
  true-merged;
- **manual demo evidence and roadmap synchronization remain later, separate
  owner-gated steps** if — and only if — implementation is later authorized and
  occurs.

Per the scope decision §9–§10, a future implementation is additionally
conditioned on the read-only source review (§8) resolving the MVP display-only
ambiguity before authorization.

---

## 12. Risks

A future review/implementation must address at least:

- **Scope drift into answer rewriting** — Co-Authoring quietly becoming Answer
  Clarification. Mitigation: §7 forbidden fields/flows; forbidden-field tests
  (§9.6).
- **Accidental Answer Clarification activation** — the separate, not-activated
  feature switching on by side effect. Mitigation: §7; §9.6 absence tests.
- **Persistence / schema creep** — adding a stored field to "remember" a
  clarified answer. Mitigation: §7 no persistence/schema change; persistence
  lane stays PAUSED/untouched.
- **Scoring / readiness coupling** — guidance leaking into `assess_response` /
  gap-closure / maturity / readiness. Mitigation: §7; §9.4 regression proof.
- **User over-reliance** — the inventor deferring to prompts instead of
  authoring specifics. Mitigation: advisory, content-free prompts; inventor
  remains the source; §10 wording.
- **Product-identity drift into education** — becoming an inventor-education tool
  rather than an idea-development orchestrator. Mitigation: §4 objective; §5
  no-tutor boundary; `OWNER_PRODUCT_IDENTITY_CORRECTION` /
  `DUAL_PATH_PRODUCT_ANCHOR` intent preserved.
- **Domain expansion** — Mitigation: §5 electronics/electrical-only.
- **Unclear provenance of generated suggestions** — ambiguity over whether text
  is inventor-authored or system-suggested. Mitigation: §10 visible provenance;
  inventor remains the source of any saved content.
- **Safety / compliance overclaiming** — guidance implying validation or
  approval. Mitigation: §7 no-claim rule; §10 wording; Safety Signals stay
  closed (§7).

---

## 13. Decision boundary

This document is classified as:

**FUTURE IMPLEMENTATION CONTRACT DRAFT — NO IMPLEMENTATION AUTHORIZED.**

It defines the boundaries and required proofs for a future Guided Answer
Co-Authoring Increment 1. It does not authorize implementation, does not create
UI or routes, does not create persistence/session schema fields, does not start
Guided Answer Co-Authoring implementation, and does not activate Answer
Clarification / Improve Wording. Any implementation requires a separate owner
authorization, an independent review, and owner-gated true merge, per §11.

---

## 14. Final classification

`GUIDED ANSWER CO-AUTHORING INCREMENT CONTRACT DRAFT — DOCS-ONLY — NO
IMPLEMENTATION AUTHORIZED`
