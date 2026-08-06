# INVENTOR SUPPORTIVE GUIDANCE & NON-EXAM UX PRINCIPLE — OWNER SCOPE DECISION (POST-PR #131)

## 0. Status

`INVENTOR SUPPORTIVE GUIDANCE / NON-EXAM UX SCOPE DECISION — GUIDED UNCERTAINTY
SUPPORT CANDIDATE — DOCS-ONLY — NO IMPLEMENTATION AUTHORIZED`

This document establishes an owner product/UX principle — **InventorAI is a
supportive idea-development assistant, not an exam-like evaluator** — and, under
that principle, admits **Guided Uncertainty Support** as the next FUTURE
owner-gated increment candidate. It records an owner scope decision only. It
authorizes NO implementation, code, test, schema, UI, route, template, runtime,
session, scoring, maturity, readiness, criticality, persistence, or domain
change; no Increment Contract in this step; no roadmap change beyond a proposed
entry (§12/§15); no `main` synchronization; and no MVP activation of any kind.

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/INVENTOR_SUPPORTIVE_GUIDANCE_NON_EXAM_UX_SCOPE_DECISION.md`
- Purpose: record (a) the owner Supportive-Guidance / Non-Exam UX principle and
  (b) an owner admission decision for a future **Guided Uncertainty Support**
  candidate, with hard anti-drift boundaries.
- Input contract: the completed read-only post-PR #131 next-step selection review,
  the owner strategic clarification in this authorization, the committed product
  identity (`OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
  `STRATEGIC_PRODUCT_VISION.md`, `DUAL_PATH_PRODUCT_ANCHOR.md`), and the merged
  PR #125–#131 Guided Answer Co-Authoring record.
- Output contract: one principle statement (§2) and one admission decision (§5,
  §14) with their boundaries; nothing executable, nothing activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, scoring authorization, an Increment Contract, activation of the
  Inventor Answer Clarification / Improve Wording feature, or roadmap content.

Authoritative context (evidence-locked):
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip: `45f47af88588d1d8a172d96bb59c5ea5bb07af99` (PR #131 merge)
- Latest merged PR: #131
- Current official state remains: `DEMO_READY_WITH_LIMITATIONS`
- The MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); no `main` sync occurred or is
  authorized.
- The frozen persistence worktree remains paused and untouched
  (`aec9cf6409efc18e125b6745762002f59e529654`); the quarantined scratch branch
  remains untouched (`02586747c902d5e1ebb78adde54ddd4ecd1c174a`).

---

## 1. Current state

- Authoritative tip: `45f47af88588d1d8a172d96bb59c5ea5bb07af99`; latest merged PR
  #131.
- Official state: `DEMO_READY_WITH_LIMITATIONS`; MVP electronics/electrical-only.
- The **Guided Answer Co-Authoring Increment 1 — Advisory Prompt Support**
  lineage is **complete and roadmap-recorded** (scope decision PR #125 → sync PR
  #126 → Increment Contract PR #127 → sync PR #128 → implementation PR #129 →
  manual demo evidence PR #130 → roadmap sync PR #131). No mandatory follow-up is
  owed.
- No product-execution lane is currently open or owner-authorized; per roadmap
  §8.1–§8.2, no new lane may be inferred and a separate explicit owner
  authorization is required before any working-tree write or product
  implementation.

---

## 2. Product / UX principle (owner clarification)

**InventorAI is a supportive idea-development assistant, not an exam-like
evaluator.**

Many users are not technical. They may not know how to describe electronics,
electricity, drones, or future domains in full technical language; even technical
users may not understand every domain. The application must help users **express
and develop their ideas step by step** without making them feel **tested, judged,
or blocked**. In particular, uncertainty answers — "I don't know", "I'm not
sure", "I don't understand the question", "I don't know the technical term", "I
don't know how it works" — must become a **supported path, not a dead end**.

This is a product-identity clarification within existing governance intent, not a
scope expansion. Governance documents may later be amended, under separate
owner-gated action, to preserve this principle; this document does not itself
amend `STRATEGIC_PRODUCT_VISION.md`, `OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
`DUAL_PATH_PRODUCT_ANCHOR.md`, or `CLAUDE.md`.

---

## 3. Relationship to existing product identity

- **Preserved:** the product identity remains **idea development, not inventor
  education** (`OWNER_PRODUCT_IDENTITY_CORRECTION.md`;
  `STRATEGIC_PRODUCT_VISION.md` §2 four objectives; `DUAL_PATH_PRODUCT_ANCHOR.md`
  §3 Path N non-specialist guided journey).
- **Supportive guidance is NOT tutor mode.** It does not teach a curriculum, run
  lessons, or turn the product into an education tool. It helps the user
  **express their own idea** — eliciting and structuring the inventor's own
  content — not learn a subject.
- **The platform leads the journey** within governed limits
  (`DUAL_PATH_PRODUCT_ANCHOR.md` §3.4) and **preserves invention gaps and
  known-unknowns** rather than papering over them (§3.5). Supportive framing
  changes the *tone and support* of asking, never the gap taxonomy, scoring, or
  the inventor's authorship of any saved answer.

---

## 4. Problem statement

On the current Path N journey a non-specialist (or a specialist outside their
domain) may respond to a scaffolding question with an uncertainty answer:

- "I don't know";
- "I'm not sure";
- "I don't understand the question";
- "I don't know the technical term";
- "I don't know how it works".

Today the journey already supports honest non-answer actions (unknown, deferred,
provisional assumption, specialist requested, evidence requested; Increment 1A)
and displays neutral clarification/scaffolding surfaces. The product need this
decision addresses is that such moments must feel **supportive and forward-
moving** — "start with what you know" — rather than exam-like, harsh, or a dead
end. The inventor must never feel they *failed* the question.

---

## 5. Candidate name

**Guided Uncertainty Support.**

---

## 6. Candidate objective

Provide **supportive, non-judgmental, optional** guidance when the user is
uncertain — helping them find a way forward and express what they *do* know —
**without writing the answer for the user**. The objective is **idea-development
value** (reducing drop-off, keeping non-specialist inventors progressing;
`STRATEGIC_PRODUCT_VISION.md` §2 objectives #2 ownership and #3 gap precision) —
not inventor education, and not answer generation. The inventor remains the
author and source of any saved answer content.

---

## 7. Explicit in-scope possibilities for a future increment

If admitted, a future — separately gated — increment *could* explore:

- **detecting uncertainty-style answers or user actions** (e.g. the existing
  "I do not know this yet" action, or uncertainty phrasing) at render time;
- responding with **simpler, gentler guiding prompts**;
- asking **what the user does know** already;
- asking **what result the user wants** the idea to achieve;
- asking **which part is unknown** or unclear;
- offering **non-technical starter questions** (category-level, content-free);
- **preserving the inventor as the source** of any saved answer at all times;
- keeping all guidance **optional, advisory, and visibly user-controlled**;
- keeping the **electronics/electrical MVP scope**.

These are candidate possibilities only; none is implemented or authorized here.

---

## 8. Explicit out-of-scope boundaries

This scope decision, and any increment it may later admit, does NOT authorize and
must NOT perform:

- **writing the answer for the user**;
- **inventing** components, numbers, materials, mechanisms, safety facts, or
  domain details on the user's behalf;
- **silent replacement** of user text;
- **auto-saving** generated text;
- introducing **approval / save clarified-answer flows**;
- **activating Answer Clarification / Improve Wording**;
- introducing `original_user_answer` / `suggested_clarified_answer` /
  `user_approved_answer` / `clarification_status` fields (or any equivalent);
- changing scoring (`assess_response` / `integrate_response` /
  `evaluate_transition` / thresholds / generic-verb trap / causal tokens);
- changing maturity / readiness / criticality (the Increment-4 `criticality`
  field stays `UNDETERMINED` / system-derived);
- changing Section 6 risks;
- populating `RequirementLandscape.risks` (stays `()`);
- changing persistence / session schema;
- reopening Safety Signals (`engine/safety_signal.py`, the
  `_session_meta.inventor_stated_safety_signals` surface, or the deliverable
  panel);
- claiming an answer or idea is **correct, complete, feasible, safe, compliant,
  patent-ready, or engineering-ready**;
- **domain expansion** beyond the electronics/electrical MVP.

---

## 9. UX wording principle

Future UI language must **avoid exam-like framing**, such as:

- "wrong";
- "failed";
- "insufficient";
- "you did not answer correctly".

and must **prefer supportive, non-judgmental wording**, such as:

- "That's okay — start with what you know.";
- "You can describe the result you want.";
- "If you are unsure, tell us which part is unclear.";
- "You do not need technical terms yet."

Supportive wording must remain **truthful**: it may not convert an open gap into
a closed one, imply an answer is validated, or hide a known-unknown. It changes
tone, not epistemic state.

---

## 10. Relationship to Guided Answer Co-Authoring

- **Guided Answer Co-Authoring (Increment 1, merged PR #129)** gives **optional,
  content-free prompts near normal questions** — "what you could include".
- **Guided Uncertainty Support (this candidate)** handles **uncertainty / "I
  don't know" cases** — helping the user find a way forward when they are stuck.
- Both must remain **advisory and display-only** unless separately authorized
  otherwise, and both must **preserve inventor authorship**.
- Neither may become **Answer Clarification / Improve Wording**: no rewriting,
  approving, or saving of a clarified answer, and none of the forbidden §8
  fields/flows. Any drift in that direction is the (non-authorized) Answer
  Clarification feature by another name and is out of scope.

---

## 11. Relationship to Prioritized Next-Action Rationale

- The **Prioritized Next-Action Rationale** candidate from the post-PR #131
  review remains a **valuable later candidate** and is **not withdrawn**.
- **Guided Uncertainty Support is prioritized first** because it addresses an
  earlier point in the journey: it **prevents user drop-off** and supports
  non-technical inventors *at the moment they get stuck*, before the journey
  reaches the stage where explaining next-action priority (a Layer-3 /
  implementation-readiness concern) is meaningful. Keeping users moving is a
  precondition for the later next-action-rationale value to be realized.

---

## 12. Governance path

This document is **only a scope decision**; it authorizes no implementation. If
accepted (independently reviewed and owner-gated true-merged), the future
sequence is:

scope decision merge → roadmap sync (separate, if required) → **separate
Increment Contract draft** → independent review → owner-gated true merge of the
contract → **read-only source review** → **separate implementation
authorization** → implementation → tests → independent review → owner-gated true
merge → **separate manual demo verification** → **separate roadmap
synchronization**.

Any implementation must be **separately owner-gated**. No step beyond this scope
decision is authorized here, and none may be inferred (roadmap §8.1–§8.2).

---

## 13. Risks

A future review/contract must address at least:

- **Drift into Answer Clarification** — supportive guidance quietly becoming
  rewrite/approve/save. Mitigation: §8 forbidden fields/flows; §10 strict
  distinction; forbidden-field tests in any future implementation.
- **Answer rewriting** — the system composing the user's answer. Mitigation: §6
  no answer generation; inventor remains the source; §8.
- **Invented technical details** — the system supplying components/numbers/
  materials/mechanisms/safety facts. Mitigation: §8 no-invention rule;
  content-free, category-level prompts only.
- **User over-reliance** — the inventor deferring to prompts instead of authoring
  their own specifics. Mitigation: advisory, optional prompts; §6 objective; §9
  "start with what you know" framing.
- **Tutor-mode drift** — the product becoming an education tool. Mitigation: §3
  supportive-guidance-is-not-tutor-mode; product identity preserved.
- **Scoring / readiness coupling** — supportive handling leaking into
  `assess_response` / gap-closure / maturity / readiness / criticality.
  Mitigation: §8 no-scoring/no-maturity/no-readiness/no-criticality; display-only
  default; regression proof in any future implementation.
- **Persistence / schema creep** — introducing a stored field to "remember"
  uncertainty state or a clarified answer. Mitigation: §8 no persistence/schema
  change; the persistence lane stays PAUSED/untouched.
- **Domain expansion** — Mitigation: §8 electronics/electrical-only preserved.
- **Safety / compliance overclaiming** — supportive wording implying validation
  or approval. Mitigation: §8 no-claim rule; §9 truthful wording; Safety Signals
  stay closed.

---

## 14. Decision

The **Inventor Supportive Guidance & Non-Exam UX Principle** (§2) is recorded as
an owner product/UX principle, and **Guided Uncertainty Support** is classified
as a **FUTURE OWNER-GATED INCREMENT CANDIDATE — SCOPE DECISION ONLY — NO
IMPLEMENTATION AUTHORIZED**.

Admission means only that the candidate may proceed to a separately-authorized
Increment Contract under a separate owner authorization, on condition that any
such contract honors the out-of-scope boundaries (§8), the UX wording principle
(§9), the Guided Answer Co-Authoring / Answer-Clarification distinction (§10), and
the risk mitigations (§13). This decision does NOT authorize implementation, does
NOT start an Increment Contract, and does NOT make the Answer Clarification /
Improve Wording feature current. The app remains electronics/electrical-only for
the MVP, and the current official state remains `DEMO_READY_WITH_LIMITATIONS`,
until separate governed decisions state otherwise.

---

## 15. Roadmap handling (proposed only)

A roadmap entry recording this scope decision is **proposed only** and is NOT made
by this document. Per repository governance, roadmap synchronization is a
separate, owner-gated documentation step performed after (and if) this scope
decision is merged. This document changes no roadmap file.

---

## 16. Final classification

`INVENTOR SUPPORTIVE GUIDANCE / NON-EXAM UX SCOPE DECISION — GUIDED UNCERTAINTY
SUPPORT CANDIDATE — DOCS-ONLY — NO IMPLEMENTATION AUTHORIZED`
