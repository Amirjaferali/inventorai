# SAFETY-AWARE CRITICALITY & INVENTOR-STATED RISK DERIVATION — OWNER SCOPE DECISION (POST-PR #117)

## 0. Status

`OWNER SCOPE DECISION ONLY — SAFETY-AWARE CRITICALITY & INVENTOR-STATED RISK
DERIVATION — FUTURE CANDIDATE — NO IMPLEMENTATION AUTHORIZED`

This document decides only whether a future **Safety-Aware Criticality &
Inventor-Stated Risk Derivation** capability should be admitted as a candidate
for a later, separately-authorized Increment Contract. It records an owner scope
decision only. It authorizes NO implementation, code, test, schema, UI, template,
runtime, session, scoring, maturity, readiness, persistence, report-generation,
or domain change; no Increment Contract in this step; no roadmap change beyond a
proposed entry (§16); no `main` synchronization; and no MVP activation of any
kind.

File-creation record (per `CLAUDE.md` File Creation Rules):
- File path: `docs/governance/SAFETY_AWARE_CRITICALITY_INVENTOR_STATED_RISK_DERIVATION_SCOPE_DECISION_POST_PR117.md`
- Purpose: governance evidence artifact recording an owner admission decision for
  a future safety-aware criticality/risk-derivation candidate.
- Input contract: the owner-observed live demo evidence after PR #117 (§2) and
  the merged PR #116/#117 record.
- Output contract: a single admission decision (§14) and its boundaries; nothing
  executable, nothing activating.
- Prohibited behaviors: this file must never be read as implementation
  authorization, scoring authorization, maturity/readiness authorization, an
  Increment Contract, or roadmap content.

Authoritative context (evidence-locked):
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip: `dae923e8d12bf9310c5cabc83fd022d5d85cb9f7` (PR #117 merge)
- Latest merged PR: #117
- Current official state remains: `DEMO_READY_WITH_LIMITATIONS`
- The MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).
- `main` remains separate and unchanged
  (`0e89e4636399760965c9ff8086b465c90dbadf8e`); no `main` sync occurred or is
  authorized.
- The frozen persistence worktree remains paused and untouched
  (`aec9cf6409efc18e125b6745762002f59e529654`); the quarantined scratch branch
  remains untouched (`02586747c902d5e1ebb78adde54ddd4ecd1c174a`).

---

## 1. Background

- **PR #116** implemented the Layer-1 Feedback Wording / Gap-Type-Aware Guidance
  increment as a display-only web-layer change (true-merged at
  `6b6d2ef7632e4be4a7c794893e0f1d8f119279f1`). Scoring was deliberately unchanged.
- **PR #117** recorded a `MANUAL DEMO VERIFICATION PASS` for that implementation
  (true-merged at `dae923e8d12bf9310c5cabc83fd022d5d85cb9f7`), 10/10 scenarios.
- **Live owner demo after PR #117** generated an FDC-001 deliverable package for
  an electronics/electrical **smart plug-in safety warning device** (household
  electricity, current/voltage sensing, battery conditions, heat, insulation, and
  user warnings).
- The deliverable reached **Maturity Level 2 — Mechanism established** and
  **INQUIRY COMPLETE**, and correctly preserved advisory / not-verified-readiness
  language — but criticality/risk derivation from the inventor's own
  safety-relevant statements remained weak.
- The owner's interpretation: in the electronics/electrical MVP, failure to
  elevate inventor-stated safety assumptions is not merely an analytical gap —
  it can become a **safety-signaling** problem, because a report that treats
  electrical insulation or delayed warning as UNDETERMINED may bury important
  safety implications in long narrative text.

This scope decision is the first governance step toward examining whether a
future, separately-authorized capability should address that gap.

---

## 2. Observed evidence (owner live demo, post-PR #117)

Recorded from the owner's live demo of the FDC-001 smart plug-in safety device
package (owner-reported observation; not a committed runtime artifact):

- **Maturity Level 2 — Mechanism established.**
- **Gaps total/open/resolved: 6 / 0 / 6** (INQUIRY COMPLETE; Eligible assessment
  package).
- **Advisory / not-verified-readiness language present** — the report correctly
  did not claim verified readiness.
- **Safety-relevant inventor statements present**, including (inventor-stated):
  - "If the device cannot be electrically insulated safely inside the plug-in
    housing, the idea should not be used because it could create a safety risk."
  - "Wrong results could make the device miss a real risk or warn the user too
    late."
  - the idea involves household electricity, current/voltage sensing, battery
    conditions, heat, insulation, and warnings.
- **Criticality remained `UNDETERMINED`.**
- **Risks section did not produce inventor-stated safety risks** — the risk
  output remained primarily **evidence-quality based** (e.g. a low-severity item
  such as "[low] Evidence is REASONED"), with **no explicit safety-critical
  risk** derived from the inventor's own statements.

The display/output truncation problems observed in earlier lanes appear stable
and clean across the recent deliverables; the gap here is analytical/safety-
signaling, not rendering.

---

## 3. Problem statement

The current package can **close inquiry gaps and reach INQUIRY COMPLETE / Level 2
while failing to elevate safety-relevant assumptions into visible criticality and
risk signals.** As a result, important safety implications the inventor explicitly
stated (electrical insulation failure, missed or delayed warning) can be **buried
in long narrative text** while the structured criticality/risk surfaces show
`UNDETERMINED` and only evidence-quality risks. This matters acutely because the
current MVP domain is **electronics/electrical**, which naturally includes
safety-sensitive ideas.

This document does not fix that. It decides only whether the question is admitted
as a candidate for a later, separately-authorized review/contract.

---

## 4. Candidate concept

**Name:** Safety-Aware Criticality & Inventor-Stated Risk Derivation.

If admitted, the candidate would explore **deterministic, evidence-grounded**
derivation of criticality and risk signals **strictly from what the inventor has
already stated and the system already recorded**, such as:

- If an inventor marks an assumption as **essential** and ties it to
  safety / failure / unsafe operation, derive a **visible criticality label** for
  that assumption.
- If an inventor states that a **failed assumption** could create safety risk,
  missed warning, delayed warning, heat risk, electrical risk, or unsafe use,
  derive a **visible risk item** attributed to the inventor's statement.
- **Preserve advisory language** throughout and **avoid claiming verification** —
  every derived signal is labelled inventor-stated and not independently
  validated.

The derivation must be traceable to recorded evidence (an inventor statement /
acknowledged assumption), deterministic, and free of generative inference.

---

## 5. Possible criticality labels to evaluate (candidates only)

Illustrative label set for a future review to evaluate and refine — **not to
implement in this PR**:

- `UNDETERMINED`
- `ADJUSTABLE`
- `ESSENTIAL`
- `ESSENTIAL — SAFETY`
- `VERIFICATION REQUIRED`
- `SAFETY-CRITICAL ASSUMPTION`

A future review must decide which (if any) of these labels are warranted, how
they are deterministically assigned from recorded evidence, and how they are
worded to remain advisory.

---

## 6. Possible risk derivation examples (illustrative only)

From inventor-stated evidence → potential derived risk item (illustrative; not
implemented here):

- Inventor-stated: *"If the device cannot be electrically insulated safely … it
  could create a safety risk."*
  → **Safety-critical assumption:** electrical insulation failure could create
  unsafe operation. *Inventor-stated; not independently validated.*
- Inventor-stated: *"Wrong results could make the device miss a real risk or warn
  the user too late."*
  → **Warning-reliability risk:** inaccurate sensing or delayed response could
  cause a missed or late warning. *Inventor-stated; not independently validated.*

Each derived item must carry an explicit inventor-stated / not-verified
attribution and must not be phrased as a system determination of danger.

---

## 7. Required boundaries (for any future implementation)

The future feature, if ever built, must NOT:

- infer new risks unsupported by recorded evidence;
- claim the product **is unsafe** as a final determination;
- claim the product **is safe** if no risk is detected;
- replace expert review;
- replace testing or certification;
- change scoring thresholds;
- silently reopen closed gaps;
- silently change maturity;
- silently mark readiness as verified.

Absence of a derived safety signal must be presented as "no safety signal was
derived from your statements", never as "no safety risk exists".

---

## 8. Scoring and maturity boundary (explicit stance)

The candidate is explicitly framed to keep criticality/risk derivation
**separate from maturity scoring at first**. Preferred stance for a future
Increment Contract:

- **Do NOT change maturity scoring** in the first implementation.
- Add **visible safety-criticality / risk signals to the report and validation
  plan only** — a presentation/derivation layer over already-recorded evidence.
- Any interaction with maturity, gap-closure, readiness, or scoring thresholds
  must be a **separately authorized** later decision (a Layer-2+/scoring-adjacent
  change under the existing four-layer separation discipline), never bundled with
  the first safety-signal implementation.

This preserves the deterministic engine's source-of-truth status: the derivation
would surface signals from evidence the engine already holds, without altering
how gaps close or maturity advances.

---

## 9. Report / UI impact analysis (for a future review to scope)

A future implementation **may** require changes to some of the following; a
future Increment Contract must enumerate exactly which, with tests:

- risk extraction (deriving inventor-stated risk items);
- criticality derivation (assigning a visible criticality label from recorded
  evidence / acknowledged assumptions);
- FDC-001 deliverable rendering (surfacing the derived criticality/risk clearly,
  not buried);
- validation-plan wording (reflecting safety-critical assumptions to verify);
- prototype / test-plan prioritization (elevating safety-sensitive checks);
- risk-section ordering (safety-critical items surfaced first);
- summary warnings (a concise advisory safety summary);
- tests for safety-sensitive phrases (deterministic phrase/assumption handling).

Relevant existing surfaces to trace during a future review include the
criticality authority (currently `UNDETERMINED (system-derived)`), the risk
output path, the FDC-001 deliverable assembler, and the validation-plan
rendering — none of which is changed by this document.

---

## 10. Product rationale

Why this matters:

- The **electronics/electrical MVP naturally includes safety-sensitive ideas**
  (mains voltage, current sensing, batteries, heat, insulation, warnings).
- **User-stated safety assumptions should not remain buried** in narrative text
  while structured surfaces show `UNDETERMINED`.
- **Paid users need clearer risk visibility** to trust the advisory output.
- Advisory reports must clearly distinguish **"not verified"** from **"no safety
  signal"** — the current output can conflate the two.
- Surfacing inventor-stated safety signals **improves trust without claiming
  certification** — it echoes the user's own stated concerns back to them,
  clearly labelled as inventor-stated and unverified.

---

## 11. Risks of the future feature

A future review/contract must address at least:

- **Over-triggering safety labels** — labelling too much as safety-critical,
  diluting the signal and alarming users;
- **False sense of legal/safety completeness** — users treating derived signals
  as a safety certification;
- **Keyword-only fragility** — naive keyword matching missing paraphrases or
  firing on false positives;
- **Alarming users unnecessarily** — over-warning on benign statements;
- **Mixing inventor-stated risk with system-verified risk** — the two must stay
  visibly distinct;
- **Coupling risk derivation to wording** — a derivation change silently becoming
  a display change or vice-versa (the Layer-1 wording lesson);
- **Changing maturity behavior accidentally** — any leak into gap-closure or
  maturity would be a scoring/benchmark-affecting change;
- **Scope drift into certification or compliance advice** — the feature must stay
  an advisory echo of inventor statements, not a compliance engine.

---

## 12. Explicit non-goals

This scope decision, and any candidate it admits, does NOT authorize and must NOT
perform:

- any implementation;
- any Increment Contract (unless separately authorized);
- any code change;
- any test change;
- any persistence/schema change;
- any scoring change;
- any maturity change;
- any readiness change;
- any domain expansion;
- any certification/compliance engine;
- any `main` synchronization;
- any Guided Answer Co-Authoring implementation;
- any Answer Clarification / Improve Wording activation.

---

## 13. Decision options considered

1. **Reject for now** — treat the gap as acceptable. *Rejected:* in the
   electronics/electrical MVP this is a safety-signaling gap, not cosmetic.
2. **Defer pending more examples** — wait for additional demos. *Not preferred:*
   the observed evidence is already concrete and safety-relevant; deferral delays
   a safety-visibility improvement without materially reducing uncertainty about
   admission (a future review still gathers evidence before any contract).
3. **Admit as future report-wording-only improvement** — reword existing output
   without deriving new signals. *Insufficient:* wording alone cannot surface a
   criticality/risk signal that is not derived; the problem is missing
   derivation, not phrasing.
4. **Admit as a deterministic safety-aware criticality/risk derivation
   candidate** — admit for a future, separately-authorized review/Increment
   Contract, report/validation-plan surfaces only, maturity untouched.
   **Preferred.**
5. **Admit directly to a future Increment Contract** — skip the review step.
   *Not chosen:* the required evidence, label set, boundaries, and report-impact
   scoping (§5/§7/§8/§9/§11) must first be worked out under a bounded review
   before a contract; direct-to-contract would risk scope drift and the
   maturity-coupling and over-triggering risks above.

**Preferred recommendation:** admit per option 4 — a **future deterministic
safety-aware criticality & inventor-stated risk derivation candidate**, with
**priority above Guided Answer Co-Authoring**, because it affects safety
signaling in the current electronics/electrical MVP.

---

## 14. Decision

The **Safety-Aware Criticality & Inventor-Stated Risk Derivation** candidate is
**ADMITTED FOR A FUTURE, SEPARATELY-AUTHORIZED REVIEW / INCREMENT CONTRACT
ONLY**, on condition that any such work honors the candidate boundaries (§7), the
scoring/maturity boundary (§8), and the non-goals (§12), and that it derives
signals only from recorded inventor-stated evidence with advisory, not-verified
attribution.

Admission means only that the candidate may proceed to a separately-authorized
read-only review and/or Increment Contract under a separate owner authorization.
This decision does NOT:

- authorize implementation;
- start implementation;
- start any scoring, maturity, or readiness change;
- start risk derivation or criticality derivation;
- create an Increment Contract in this step.

Any subsequent work must proceed, in order, through: this scope decision
(admission only); a separately authorized review and/or Increment Contract; a
separate implementation authorization; tests; independent review; an owner-gated
true merge; and separate manual-demo verification. The app remains
electronics/electrical-only for the MVP, and the current official state remains
`DEMO_READY_WITH_LIMITATIONS`, until separate governed decisions state otherwise.

---

## 15. Relationship to Guided Answer Co-Authoring

The owner has separately identified a distinct UX/product candidate — **Guided
Answer Co-Authoring / "Clarify and Build My Answer"**. That candidate remains
important but is **separate** from this one, and **this PR must not mix** UX
co-authoring with safety-criticality/risk derivation. Guided Answer Co-Authoring
is neither admitted nor scoped here; it remains a separate future candidate
requiring its own owner scope decision. Per §13, the safety-aware
criticality/risk candidate is prioritized **above** Guided Answer Co-Authoring
because it affects safety signaling in the current MVP domain.

---

## 16. Roadmap handling (proposed only)

A roadmap entry recording this scope decision is **proposed only** and is NOT
made by this document. Per repository governance, roadmap synchronization is a
separate, owner-gated documentation step performed after (and if) this scope
decision is merged. This document changes no roadmap file.

---

## 17. Final classification

`OWNER SCOPE DECISION ONLY — SAFETY-AWARE CRITICALITY & INVENTOR-STATED RISK
DERIVATION — FUTURE CANDIDATE — NO IMPLEMENTATION AUTHORIZED`
