# DOMAIN GATE / ENTRY UX — OWNER SCOPE DECISION (POST-PR #98)

## 1. Status

`OWNER SCOPE DECISION RECORD — DOMAIN GATE / ENTRY UX CANDIDATE ADMITTED FOR
FUTURE INCREMENT PLANNING; NOT IMPLEMENTED; NOT ACTIVATED`

This document records an owner scope decision only. It admits the Domain Gate /
Entry UX Improvement candidate for future Increment Contract preparation. It
authorizes NO implementation, code, schema, UI, runtime, template, test, or
persistence change, and no domain expansion or MVP activation of any kind.

Authoritative context:
- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip after PR #98: `61378d44cb86baf42250acc3a3b1b27dcb4b4744`
- Official state: `DEMO_READY_WITH_LIMITATIONS`
- The app remains electronics/electrical-only for the MVP
  (`MVP_SCOPE_FREEZE.md`).

---

## 2. Source evidence

This decision is grounded in the merged post-PR97 demo evidence record
`docs/governance/DEMO_EVIDENCE_FINDINGS_POST_PR97.md` (merged via PR #98). That
record documents:

- Demo 3A: an elderly appliance-left-on alert idea, written in natural lay
  wording, was **rejected at the domain gate** on the official tip.
- The idea was genuinely electronics/electrical in owner intent.
- The explicit electronics/electrical confirmation checkbox **did not override**
  the conflicting supported-domain classification.
- The read-only diagnostic found that the word "monitoring" matched a
  `medical_device` classification signal, while the natural lay wording
  contained **no electronics component keyword signal** (e.g. circuit, sensor,
  voltage, current, microcontroller), so `infer_domain` returned
  `medical_device` and `/start` refused with the unsupported-domain message.
- The **same idea** with mechanism-explicit wording (terms such as "current
  sensor," "microcontroller," "wifi alert") **passed** the gate — proving the
  limitation is a product-entry wording/classifier alignment issue, **not idea
  invalidity**.

The merged record ranks Domain Gate / Entry UX Improvement as the
**highest-priority** future candidate.

---

## 3. Owner decision

The Domain Gate / Entry UX Improvement candidate is **ADMITTED for future
Increment Contract preparation**, because it is now the highest-priority blocker
to non-specialist value delivery. Admission means this candidate may proceed to
Increment Contract drafting under a separate owner authorization; it does not
authorize any implementation.

---

## 4. What is admitted (future scope for planning only)

The following is admitted for future planning only:

- Improving the first-entry experience for valid electronics/electrical ideas
  written in non-specialist wording.
- Clarifying the relationship between explicit owner domain confirmation and a
  deterministic classifier conflict.
- Improving user-facing rejection guidance when a potentially valid idea is
  rejected.
- Considering safer treatment of ambiguous generic words such as "monitoring"
  when the owner explicitly confirms electronics/electrical intent.
- Considering lay-term electronics signals such as "appliance," "plug,"
  "socket," "power," "wire," "electricity," "alert," "household electrical
  appliance," and similar terms — but only as a **future design candidate**.
- Ensuring the current MVP entry-UX improvement does not hard-code assumptions
  that would block a future governed multi-technology intake/router (see §10) —
  a design-compatibility constraint only, not authorization of any such router.

---

## 5. What is NOT admitted

This scope decision does NOT authorize any of the following:

- implementation;
- code changes;
- domain classifier changes;
- schema changes;
- UI/template/runtime changes;
- tests;
- persistence work;
- `main` synchronization;
- broad domain expansion;
- medical-device support;
- `iot_electronics` activation;
- automatic relabeling of conflicting domains;
- unsafe bypass of the domain gate;
- MVP activation;
- any Increment Contract (drafting one requires a separate owner authorization);
- future multi-technology domain expansion;
- drone, solar, robotics, or other technology-family activation;
- any regulated-domain safety/compliance support.

---

## 6. Governance boundaries

- This decision admits the candidate for future Increment Contract drafting
  only.
- The app remains **electronics/electrical-only for the MVP** per
  `MVP_SCOPE_FREEZE.md`. No unsupported domain is added.
- No medical-device, software, mechanical, IoT, drone, solar, robotics, or other
  technology-family expansion is authorized.
- Any future implementation must preserve the principle that **user confirmation
  helps resolve ambiguity but must not silently override clear unsupported-domain
  evidence without a bounded rule**.
- Any future implementation must avoid false claims that the app validates
  safety, feasibility, buildability, medical compliance, electrical compliance,
  drone safety, solar safety, or any regulated technical safety area.
- Any future entry-UX change must preserve **advisory-only framing** and must
  not turn InventorAI into a compliance, certification, feasibility, safety,
  patentability, or build-readiness validator.

---

## 7. Future Increment Contract requirements

If a future Increment Contract for this candidate is separately authorized, it
must define:

- exact intended behavior;
- exact non-goals;
- accepted and rejected example inputs;
- domain-gate safety boundaries;
- user-facing messages;
- tests for natural lay electronics wording (should be admissible);
- tests for true unsupported-domain rejection (must still be refused);
- tests ensuring `medical_device`, `software`, `mechanical`, and unrelated ideas
  are still rejected;
- tests ensuring no drone, solar, robotics, IoT, or other technology-family
  activation occurs;
- tests ensuring no regulated-domain safety/compliance claims are introduced;
- tests ensuring no `main` synchronization or persistence work;
- rollback criteria;
- demo verification steps.

---

## 8. Priority relationship

The current priority order after PR #98 (from the merged evidence record) is:

1. Domain Gate / Entry UX Improvement
2. More Detail Needed Feedback / Guided Answer Scaffolding
3. Inventor Answer Clarification / Improve Wording Assistant
4. Deliverable Readability / Reference Compaction
5. EV Summary Ellipsis Diagnostic
6. Prototype & Test Plan Diversity
7. Owner-Confirmed Engineering Translation Layer
8. Owner-Stated Risk Capture
9. Structured Owner Criticality Capture
10. Registry Hygiene

This document admits candidate #1 (Domain Gate / Entry UX Improvement) for
future Increment Contract preparation only. It does not reorder, activate, or
implement any candidate.

---

## 9. Relationship to other candidates

This scope decision:

- does NOT implement or authorize the More Detail Needed fix;
- does NOT implement or authorize the Inventor Answer Clarification / Improve
  Wording Assistant;
- does NOT implement or authorize engineering translation;
- does NOT implement or authorize Structured Owner Criticality Capture;
- does NOT implement or authorize Registry Hygiene changes;
- does NOT implement or authorize any future multi-technology domain router.

Each of those remains a separate future candidate requiring its own separate
owner decision.

---

## 10. Future multi-technology architecture note (future-compatibility only)

Recorded as a future-compatibility note, NOT as current authorization:

InventorAI may later support multiple technology families beyond the current MVP
electronics/electrical scope, such as drones, solar energy, robotics,
agricultural systems, water systems, IoT-enabled devices, and hybrid
mechanical-electrical inventions. This Domain Gate / Entry UX scope decision must
therefore avoid future-hostile wording that assumes the product will permanently
remain electronics/electrical-only.

However, this document does NOT authorize any such expansion now. Specifically,
it does NOT authorize:

- drone support;
- solar-energy support;
- robotics support;
- IoT domain activation;
- medical-device support;
- mechanical-domain support;
- software-domain support;
- multi-domain routing implementation;
- regulatory, safety, compliance, or certification claims;
- validation of drone flight safety, solar electrical safety, or any other
  regulated technical safety area.

Future multi-technology support must be handled through a **separate
owner-approved domain-admission framework** and separate scope decisions for each
admitted technology family or routing architecture.

Any future multi-technology intake/router design must preserve:

- advisory-only framing;
- no validation claims;
- no safety/compliance certification;
- clear owner confirmation;
- clear unsupported-domain refusal;
- traceable domain classification;
- readable user-facing explanations when an idea is rejected or routed.

---

## 11. Governance final statement

This document records an owner scope decision only. It authorizes preparation of
a future Increment Contract for Domain Gate / Entry UX Improvement, but
authorizes **no implementation**.

It also records a future-compatibility note that InventorAI may later require a
governed multi-technology intake/router architecture. That future note does NOT
authorize any domain expansion, technology-family activation, compliance
support, regulated-domain validation, or implementation now.

Any future work under this candidate must proceed, in order, through: a separate
owner scope decision (this record satisfies the admission step only); a
separately authorized Increment Contract; an implementation branch; tests;
independent review; and an owner-authorized true merge. The app remains
electronics/electrical-only for the MVP until a separate governed decision states
otherwise.
