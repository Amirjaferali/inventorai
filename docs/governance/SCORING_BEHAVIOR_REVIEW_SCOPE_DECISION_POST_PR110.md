# SCORING-BEHAVIOR REVIEW — OWNER SCOPE DECISION (POST-PR #110)

## 1. Status

`OWNER SCOPE DECISION — SCORING-BEHAVIOR REVIEW CANDIDATE; ADMISSION DECISION
ONLY; NO IMPLEMENTATION AUTHORIZED; NO SCORING CHANGE AUTHORIZED`

This document decides only whether a future **scoring-behavior review** should be
admitted as a candidate for a later, separately-authorized increment. It records
an owner scope decision only. It authorizes NO implementation, code, test, schema,
UI, template, runtime, session, scoring, persistence, or domain change; no
increment contract in this step; no roadmap change beyond a proposed entry (§10);
no `main` synchronization; and no MVP activation of any kind.

Authoritative context:
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip: `20c8a400572ef78fcf158a6271c16c66e694763c`
  (PR #110 manual-demo-verification evidence true merge)
- Latest merged PR: #110
- Current official state remains: `DEMO_READY_WITH_LIMITATIONS`
- The MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); no `main` sync occurred or is
  authorized.
- The frozen persistence worktree remains paused and untouched
  (`aec9cf6409efc18e125b6745762002f59e529654`); no paused persistence path is
  modified or authorized.

---

## 2. Background (PR #108 and PR #110)

- **PR #108** implemented the More Detail Needed / Guided Answer Scaffolding
  increment as a **display-only / guidance-only** change (true-merged at
  `bb70c116a58449ee3e0398d2f986703de5f1fde1`). It shows bounded, deterministic,
  render-time guidance naming the KIND of missing detail to add when the engine
  has ALREADY returned a WARN-class insufficiency. It deliberately did NOT change
  scoring: `engine/scoring.py` and `engine/progression_loop.py` (including
  `assess_response`, `integrate_response`, `evaluate_transition`, and the
  gap-close rules) were unchanged.
- **PR #110** recorded a **MANUAL DEMO VERIFICATION PASS** for that implementation
  (true-merged at `20c8a400572ef78fcf158a6271c16c66e694763c`). The evidence note
  confirmed the guidance behaves correctly and explicitly recorded a remaining
  limitation: *the underlying scoring behavior is unchanged; the increment
  improves feedback clarity only.* Both the PR #108 increment contract (PR #106,
  §8) and the PR #110 evidence note flagged any scoring change as a **separate,
  not-yet-authorized future decision.**

This scope decision is the first governance step toward examining whether that
separate scoring-behavior decision should be pursued.

---

## 3. Problem statement

The demo evidence (`docs/governance/DEMO_EVIDENCE_FINDINGS_POST_PR97.md`, Demo 3B;
§5; §6.B) recorded that ordinary, plain-language inventor answers can repeatedly
receive "More detail needed" (WARN). The recorded deterministic cause is that
`assess_response` scores plain-language answers as `ASSERTED` — the generic-verb
trap penalizes natural verbs such as "detects"/"sends" unless paired with a fixed
causal-structure keyword — so gaps remain `PARTIAL`; this is compounded by a
two-`REASONED`-answers-per-gap close requirement. PR #108's guidance now explains
*what* to add, but it does not change *how* answers are scored. The open question
is whether the scoring behavior itself is, in some cases, **too strict or
unnatural for ordinary inventor answers**, and whether that is a genuine product
limitation worth a future, carefully-bounded review — or an intended, historically
grounded behavior that must be preserved.

This document does not answer that question. It decides only whether the question
is **admitted as a candidate** for a later, separately-authorized review.

---

## 4. Candidate boundaries (what a future review WOULD and would NOT consider)

If admitted, the future scoring-behavior review would be a **read-only analysis
and design-decision exercise only** (no code). It would examine, and clearly
separate, four distinct layers — because they carry very different risk and must
never be conflated:

1. **Feedback wording improvements** — the user-facing text of WARN / More Detail
   Needed messages and the PR #108 guidance. Lowest risk; display-only; does NOT
   change any PASS/WARN/BLOCK outcome. (Note: PR #108 already delivered the
   guidance surface; further wording refinement is display-only.)
2. **Scoring threshold changes** — the `assess_response` ASSERTED/REASONED
   classification, the generic-verb trap, the substance-signal handling, and any
   numeric/length thresholds that decide whether an answer is "reasoned enough".
   Changes here alter the deterministic score of an answer.
3. **Evidence classification changes** — how answers map to evidence
   provenance/validation status and quality (Increment 2 truthful-state model),
   and whether that mapping is too strict/lenient.
4. **Gap closure logic changes** — `evaluate_transition`, the
   two-`REASONED`-answers-per-gap close requirement, mechanism-completeness
   expectations, and maturity-transition gates.

The review would treat layers 2–4 as **HIGH-RISK, benchmark-affecting** and layer
1 as display-only. Its only permitted output is a written analysis and, if
warranted, a recommendation for a future increment contract — never code.

---

## 5. Explicit non-goals

This scope decision, and any review admitted by it, does NOT authorize and must
NOT perform:

- any implementation, code, or test change;
- any scoring change (`assess_response`, `integrate_response`,
  `evaluate_transition`, the generic-verb trap, substance signals, the
  two-`REASONED` gap-close requirement, mechanism-completeness expectations, or
  any threshold);
- any evidence-classification or gap-closure logic change;
- any persistence/schema change;
- any deliverable-generation change;
- activation of the Inventor Answer Clarification / Improve Wording Assistant, or
  introduction of `suggested_clarified_answer` / `user_approved_answer` /
  `original_user_answer` / `clarification_status`;
- any domain expansion or activation of IoT / robotics / drone / solar /
  medical_device / software-domain / mechanical-domain / multi-technology router;
- any change to the WPS001 benchmark behavior, golden fixtures, or replay
  baselines;
- any `main` synchronization;
- any modification of the frozen persistence worktree or use of the quarantined
  scratch branch;
- any change to the current official state (`DEMO_READY_WITH_LIMITATIONS`) or MVP
  scope (electronics/electrical-only).

---

## 6. Governance risks

- **Historical-behavior risk.** `benchmark/run_benchmark_v1.py` is the historical
  behavioral authority, and scoring changes touch the deterministic engine that is
  the single source of truth. Any threshold/classification/gap-closure change is
  benchmark-affecting and risks silent semantic drift, replay divergence, or
  benchmark gaming — the exact failure modes the refactor governance contract
  (`CLAUDE.md`) exists to prevent.
- **Scope-creep risk.** A "make WARN less strict" framing could quietly become a
  scoring-threshold change, an evidence-classification change, or a gap-closure
  change without those being separately classified and authorized — hence the
  mandatory four-layer separation in §4.
- **Authority-conflation risk.** Feedback wording (display-only, low risk) must
  never be bundled with scoring/gap-closure logic (HIGH risk) in a single
  authorization.
- **Provenance risk.** Any proposed change must be traced through the mandated
  provenance chain (raw_response → extraction → normalization → fixture → replay
  scoring → report) rather than patched at the scorer; scorer patching is a
  standing stop condition.

---

## 7. Product UX risks

- **Under-strict risk.** Loosening scoring could let genuinely thin answers close
  gaps and advance maturity, producing a false sense of readiness — directly
  against the Increment 2 truthful-state principle (a stored `CLOSED` gap is not
  verified readiness).
- **Over-strict risk (the reported symptom).** Leaving scoring unchanged may keep
  non-specialist inventors looping on "More detail needed" even after reasonable
  plain-language answers, reducing visible idea-development value.
- **Inconsistency risk.** Changing scoring without aligning the PR #108 guidance
  wording (or vice-versa) could make the feedback and the outcome disagree.
- **Expectation risk.** Users may read any softened threshold as the system
  "approving" their idea; advisory-only framing and honest gap semantics must be
  preserved regardless of any change.

---

## 8. Possible future review questions

Illustrative only; a future review would refine these:

- Is the generic-verb trap mis-penalizing ordinary electronics/electrical
  plain-language mechanism descriptions (e.g. "the sensor detects current and the
  microcontroller sends an alert")? With what measured frequency, on what inputs?
- Is the two-`REASONED`-answers-per-gap close requirement appropriate for Path N
  (non-specialist) sessions, or should the requirement be re-expressed without
  changing the underlying truth semantics?
- Can feedback-wording improvements (layer 1) alone materially reduce the reported
  loop without any scoring change?
- If a scoring-threshold change (layer 2) is ever considered, what parity proof
  and benchmark-lineage evidence would be required before it could even be
  proposed?
- How would any change interact with WPS001 invariants and the existing
  adversarial/replay assess-response tests?
- Which layer (1–4), if any, is the minimum that addresses the symptom?

---

## 9. Required evidence before any later implementation contract

Before ANY future increment contract for a scoring change could be drafted (each
still separately owner-gated), the admitted review must first produce, read-only:

- a reproducible characterization of the symptom: exact inputs, the observed
  ASSERTED/REASONED classification, and the resulting WARN/gap-`PARTIAL` outcome,
  traced through the provenance chain;
- a measured frequency/impact estimate on representative Path N
  electronics/electrical inputs;
- an explicit four-layer classification (§4) of any proposed direction, stating
  which layer(s) it touches and why;
- for any layer 2–4 (scoring/evidence/gap-closure) direction: a documented
  benchmark-lineage and parity analysis showing whether the change preserves
  historical benchmark intent, plus the WPS001 and replay implications — with the
  default disposition being **preserve historical behavior** unless parity proof
  exists;
- confirmation that a feedback-wording-only (layer 1) option was considered first;
- a rollback/limitation statement.

Absent this evidence, no implementation contract may be drafted, and no scoring
change may be proposed.

---

## 10. Roadmap handling (proposed only)

A roadmap entry recording this scope decision is **proposed only** and is NOT made
by this document. Per repository governance, roadmap synchronization is a separate,
owner-gated documentation step performed after (and if) this scope decision is
merged. This document changes no roadmap file.

---

## 11. Decision

The Scoring-Behavior Review candidate is **ADMITTED FOR A FUTURE, SEPARATELY-
AUTHORIZED READ-ONLY REVIEW ONLY**, on the condition that any such review honors
the four-layer separation (§4), the non-goals (§5), and the evidence requirements
(§9). Admission means the candidate may proceed to a read-only review under a
separate owner authorization; it does not authorize the review to begin, any
increment contract, or any implementation.

Any subsequent work must proceed, in order, through: this scope decision
(admission only); a separately authorized read-only scoring-behavior review; a
separately authorized increment contract (only if the review's evidence supports
one); a separate implementation authorization; tests; independent review; and an
owner-gated true merge. The app remains electronics/electrical-only for the MVP,
and the current official state remains `DEMO_READY_WITH_LIMITATIONS`, until
separate governed decisions state otherwise.

---

## 12. Final classification

`SCOPE DECISION ONLY — NO IMPLEMENTATION AUTHORIZED`
