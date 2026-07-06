# DOMAIN GATE / ENTRY UX — INCREMENT CONTRACT (POST-PR #99)

## 1. Status

`INCREMENT CONTRACT DRAFT — DOMAIN GATE / ENTRY UX IMPROVEMENT; NOT IMPLEMENTED;
NOT ACTIVATED; IMPLEMENTATION REQUIRES SEPARATE OWNER AUTHORIZATION`

This document defines a *possible future implementation increment*. It is a
planning artifact only. It does NOT authorize execution, code, schema, UI,
runtime, template, test, or persistence change, and no domain expansion,
technology-family activation, or compliance/validation claim. Implementation
requires a separate, explicit owner authorization after this contract is
reviewed and accepted.

Authoritative context:
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip after PR #99: `7e2b3105587ac2121b478c732997e80fc20e1e61`
- Official state: `DEMO_READY_WITH_LIMITATIONS`
- MVP remains electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).

---

## 2. Governing source chain

- PR #98 made the post-PR97 demo evidence record official
  (`docs/governance/DEMO_EVIDENCE_FINDINGS_POST_PR97.md`).
- PR #99 made the Domain Gate / Entry UX owner scope decision official
  (`docs/governance/DOMAIN_GATE_ENTRY_UX_SCOPE_DECISION_POST_PR98.md`), admitting
  this candidate for Increment Contract preparation only.
- This document is the next planning artifact only.
- Implementation still requires separate owner authorization after this contract
  is reviewed and accepted.

---

## 3. Problem statement

The current MVP can reject a genuinely electronics/electrical idea when a
non-specialist user describes it in everyday words that lack technical
electronics keywords, while an explicit electronics/electrical confirmation
checkbox does not resolve the conflict if the deterministic classifier returns
another supported domain such as `medical_device`.

Source evidence — Demo 3A (from the merged evidence record):
- natural lay wording about an elderly appliance-left-on alert was rejected;
- owner intent was electronics/electrical;
- the word "monitoring" triggered `medical_device`;
- the lay wording contained no electronics component keyword signal;
- the same idea with mechanism-explicit wording (current sensor, microcontroller,
  Wi-Fi alert) passed the gate — proving the limitation is a product-entry
  wording/classifier alignment issue, not idea invalidity.

---

## 4. Increment objective

Improve the first-entry experience so that valid electronics/electrical ideas
written in lay wording are either:
- admitted safely when bounded evidence supports electronics/electrical intent; or
- rejected with clearer, actionable, non-technical guidance that helps the user
  understand what is missing.

The objective is NOT to validate feasibility, safety, compliance, buildability,
or correctness. It is an entry-experience/classification-alignment improvement
only.

---

## 5. Authorized future implementation scope (only after separate implementation authorization)

If separately authorized later, the increment would be limited to:

- Improve domain-gate handling for lay electronics/electrical wording.
- Improve conflict handling between explicit owner electronics/electrical
  confirmation and deterministic classifier output.
- Improve user-facing rejection guidance for possibly valid electronics/electrical
  ideas.
- Add or refine bounded lay-term electronics/electrical signals such as
  "appliance," "plug," "socket," "power," "wire," "electricity," "current,"
  "alert," "household electrical appliance," and similar non-specialist terms —
  only if safely bounded.
- Add tests covering accepted and rejected examples.
- Preserve unsupported-domain rejection.

---

## 6. Explicit non-goals

The increment must NOT:

- add any new supported domain;
- activate `iot_electronics`;
- support `medical_device`;
- support `software`;
- support `mechanical`;
- support drone, solar, robotics, agriculture, water systems, or other
  technology families;
- implement a multi-technology router;
- silently bypass the domain gate;
- treat owner checkbox confirmation as an unconditional override;
- claim safety validation;
- claim feasibility validation;
- claim compliance validation;
- claim build-readiness;
- claim patentability;
- modify persistence;
- sync `main`;
- touch the frozen persistence worktree;
- implement answer clarification;
- implement More Detail Needed scoring changes;
- implement engineering translation;
- implement structured owner criticality capture;
- implement risk generation.

---

## 7. Proposed behavior model (proposed, not implemented)

The contract PROPOSES the following bounded model; it does NOT implement it.

**A. Clear electronics/electrical evidence.** If the idea contains clear
electronics/electrical signals and the owner confirms electronics/electrical →
admit.

**B. Lay electronics/electrical evidence.** If the owner confirms
electronics/electrical and the wording includes lay household electrical signals
(appliance, plug, socket, power, electricity, current, switch, alert, or
sensor-like behavior), do NOT reject immediately only because technical component
terms are missing. Instead, either admit under bounded MVP assumptions or show a
clarification-style entry message asking for a simple mechanism phrase.

**C. Conflicting supported-domain evidence.** If the classifier returns
`medical_device`, `software`, `mechanical`, or another supported-but-not-MVP
domain based on weak/ambiguous generic terms such as "monitoring," and the owner
explicitly confirms electronics/electrical, apply a bounded ambiguity-resolution
rule. Do NOT silently override strong unsupported-domain evidence. Do NOT admit
ideas that are genuinely medical, software-only, mechanical-only, or unrelated.

**D. True unsupported-domain evidence.** If the idea clearly belongs outside
electronics/electrical → reject with a clear message.

**E. User-facing rejection guidance.** Replace vague refusal with guidance such
as: "This MVP currently supports electronics/electrical ideas only. Your
description does not yet show the electrical mechanism. Try adding a simple phrase
such as: it uses a sensor, current, switch, circuit, power, plug, or
microcontroller." Exact wording may be refined during implementation, but the
contract specifies this intended guidance type.

---

## 8. Acceptance examples — should be admitted or guided, not hard-rejected

A future implementation must handle these so they are NOT hard-rejected solely
for lacking technical terms:

- **A.** "A device that alerts my mother if the stove or iron stays on too long."
  → should not be hard-rejected only for lacking technical terms; should ask for
  electrical-mechanism clarification or admit if bounded rules are met.
- **B.** "A home appliance alert that detects if power stays on unusually long and
  sends a phone alert." → electronics/electrical lay wording; admitted or guided.
- **C.** "A plug-in device that senses current from an appliance and sends a
  Wi-Fi alert." → admitted.
- **D.** "A socket device that warns when an appliance remains powered for more
  than a set time." → admitted.
- **E.** "A sensor device that detects appliance electrical current and alerts the
  user." → admitted.

---

## 9. Rejection examples — must still be rejected

- **A.** "A medical monitor that tracks heart rhythm and alerts doctors." →
  reject as `medical_device` / unsupported for MVP.
- **B.** "An app that reminds elderly people to turn off appliances based only on
  manual checklists." → reject / not admit as electronics/electrical if no
  electrical mechanism exists.
- **C.** "A purely mechanical timer that shuts off a gas valve." → reject as
  mechanical / outside MVP.
- **D.** "A drone that checks farms and sprays crops." → reject; drone/agriculture
  not activated.
- **E.** "A solar farm optimizer that validates panel wiring safety." → reject;
  solar/compliance not activated.
- **F.** "A software-only AI assistant that predicts appliance use." → reject as
  software-only.
- **G.** "A device that diagnoses dementia by monitoring elderly behavior." →
  reject as medical/sensitive unsupported domain.

---

## 10. Conflict examples (required tests for conflict cases)

- "monitoring" alone must NOT force `medical_device` when the rest of the wording
  and owner confirmation indicate a household electrical appliance alert.
- "medical monitoring" or "heart monitoring" must STILL reject.
- "appliance monitoring" with power/current/plug/sensor context should be treated
  differently from medical monitoring.
- Owner checkbox confirmation must help resolve ambiguity but must NOT become an
  unconditional override.

---

## 11. Required implementation files — candidate only

File names below are **candidate future implementation areas only**; NO file
change is authorized by this contract draft. Actual paths must be re-confirmed
against the repository at implementation time under separate authorization.

- `web/app.py` — the `/start` route and its domain-gate branch (the
  `infer_domain` conflict/confirmation logic and the unsupported-domain message).
- The domain inference location identified from the governing evidence
  (`engine/domain_rules.py` `infer_domain`, and the domain packs under
  `domains/` for bounded lay-term signals) — inspection candidate only.
- Tests covering `/start` / domain-gate behavior (a new/expanded test module).
- Relevant templates (`web/templates/index.html`) only if user-facing rejection
  message changes are authorized later.

---

## 12. Required tests for future implementation

- tests for lay electronics/electrical accepted-or-guided behavior;
- tests for mechanism-explicit electronics admission;
- tests for unsupported `medical_device` rejection;
- tests for software-only rejection;
- tests for mechanical-only rejection;
- tests for drone/solar/robotics/IoT non-activation;
- tests for owner confirmation NOT acting as an unconditional bypass;
- tests for rejection guidance containing actionable non-technical wording;
- tests ensuring no persistence files are changed;
- tests ensuring no `main` sync;
- regression tests preserving the existing valid electronics/electrical path
  (including WPS001 and the current increment test baselines).

---

## 13. Demo verification plan (future, manual)

- **Demo A** — Input: elderly appliance-left-on alert lay wording. Expected: no
  hard unsupported-domain rejection solely due to lack of technical terms; app
  either admits or gives targeted mechanism guidance.
- **Demo B** — Input: mechanism-explicit current sensor + microcontroller + Wi-Fi
  alert wording. Expected: admit.
- **Demo C** — Input: medical heart monitoring. Expected: reject.
- **Demo D** — Input: drone farm monitoring. Expected: reject.
- **Demo E** — Input: solar panel compliance validator. Expected: reject.

---

## 14. Safety and governance boundaries

- advisory-only;
- no safety validation;
- no electrical compliance validation;
- no medical compliance validation;
- no drone or solar compliance validation;
- no feasibility/buildability validation;
- no patentability validation;
- no supported-domain expansion;
- no multi-technology router;
- electronics/electrical-only MVP remains intact.

---

## 15. Rollback criteria

Rollback or block merge if:

- unsupported domains become admitted;
- the checkbox becomes an unconditional bypass;
- medical/heart/health monitoring is admitted;
- drone/solar/robotics/IoT examples are admitted;
- a user-facing message claims validation, safety, feasibility, compliance, or
  build-readiness;
- persistence files are touched;
- `main` is touched;
- required tests are missing;
- changes exceed the authorized Increment Contract scope.

---

## 16. Implementation authorization gate

This Increment Contract draft does NOT authorize implementation. After review and
merge of this contract, the owner must SEPARATELY authorize implementation.
Implementation must happen in a dedicated branch/worktree and must include tests
and independent review before any merge.

---

## 17. Relationship to other candidates

This contract does NOT authorize:

- More Detail Needed Feedback / Guided Answer Scaffolding;
- Inventor Answer Clarification / Improve Wording Assistant;
- Engineering Translation Layer;
- Structured Owner Criticality Capture;
- Owner-Stated Risk Capture;
- Registry Hygiene;
- Deliverable Readability / Reference Compaction;
- EV Summary Ellipsis Diagnostic.

Each remains a separate future candidate requiring its own separate owner
decision.

---

## 18. Final contract statement

This document is a contract draft for a possible future Domain Gate / Entry UX
implementation increment. It defines intended behavior, non-goals, examples,
tests, demo verification, and rollback boundaries. It authorizes no
implementation until separately owner-approved. The app remains
electronics/electrical-only for the MVP until a separate governed decision states
otherwise.
