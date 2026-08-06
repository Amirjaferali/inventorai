# D13-TKP-PKG-001 — Phase B Owner Decision and Research Scope

**Status:** OWNER DECISION — bounded scope definition for Phase B. **Non-activating:** Phase B research does **not** begin
by recording this decision; a separate explicit owner start authorization is required (see §7). Prepared under the
risk-based execution and review model (PR #220).

## 1. Phase A is formally closed
Phase A (bounded, repository-only, read-only internal analysis) is **formally closed through PR #219**
(`docs/governance/D13_TKP_PKG_001_PHASE_A_FORMAL_CLOSURE_RECORD.md`). Its four outputs and supporting records are canonical
and preserved. Phase B builds on Phase A's recorded findings (missing fields MF-01…MF-10, capability gaps CG-01…CG-07,
proposed RQs P-RQ-A1…P-RQ-A8) without treating any of them as an approved requirement or an answered question.

## 2. Phase B definition (bounded evidence and research phase only)
Phase B is a **bounded evidence and research phase**: it authorizes, only upon a separate start authorization (§7), the
gathering and quality-graded recording of technical evidence to address the proposed research questions in §3, within the
Gate 2/Gate 3 concept class (single-signal sensor→microcontroller interfacing: analog-voltage / single-ended-digital /
pulse-frequency; low-voltage; non-safety-critical). Phase B produces evidence and answers **as recorded findings** — it does
not build product, code, schemas, prompts, or a Technical Knowledge Package.

## 3. Proposed Phase B research questions (technology-first; none answered here)
Each RQ maps to the Gate 3 authorized envelope (RQ-01…RQ-11) and preserves the technology-first fields. Nothing below is
answered; all are proposed for owner review.

**Common fields per RQ:** unresolved technical subproblem · missing technical information · required technology/research
topic · suggested technical search terms · required measurements/documents/tests · what InventorAI can verify · what
InventorAI cannot verify · risk/uncertainty · specialist category (only when genuinely necessary).

- **PB-RQ-1 — Sensor-output classification (→ RQ-01; from CG-01).** Subproblem: deterministically classify a sensor output as
  analog-voltage/single-ended-digital/pulse-frequency. Missing info: typed output classification. Topic: sensor output
  typing. Search terms: "sensor output signal type", "analog vs digital sensor interface". Required: governing-parameter
  documentation. Can verify: presence of a free-text description. Cannot verify: the true signal type structurally.
  Risk: low–moderate. Specialist: not necessary.
- **PB-RQ-2 — Voltage-range compatibility (→ RQ-02/03; from CG-02).** Subproblem: indicate voltage-range mismatch. Missing:
  sensor output range + target input range. Topic: voltage-range compatibility. Search terms: "sensor output voltage range",
  "MCU input voltage range". Required: governing-parameter documents. Can verify: free-text power notes. Cannot verify:
  numeric relationships (no calculation in scope). Risk: moderate. Specialist: not necessary.
- **PB-RQ-3 — ADC-reference / digital logic-level compatibility (→ RQ-05/06; from CG-03).** Subproblem: ADC input-range fit;
  single-ended digital level fit. Missing: target-MCU input attributes. Topic: ADC reference/input range; logic levels.
  Search terms: "ADC reference input range", "logic level compatibility". Required: device governing parameters. Cannot
  verify: fit without the target attributes. Risk: moderate. Specialist: not necessary.
- **PB-RQ-4 — Pulse/frequency compatibility (→ RQ-07; from CG-04).** Subproblem: pulse/frequency interfacing. Missing:
  pulse/frequency descriptor. Topic: frequency-output interfacing. Search terms: "frequency output sensor interfacing",
  "pulse counting input". Required: governing-parameter documents. Risk: moderate. Specialist: not necessary.
- **PB-RQ-5 — Impedance/loading relevance (→ RQ-04; from CG-05).** Subproblem: when impedance/loading matters. Missing:
  impedance context. Topic: source/load impedance in low-voltage interfacing. Search terms: "sensor output impedance
  loading", "input impedance loading effect". Risk: moderate. Specialist: possibly an electronics-interfacing reviewer
  category (only if a judgment call is genuinely required); no person/company named.
- **PB-RQ-6 — Datasheet sufficiency / abstention (→ RQ-09/11; from CG-06).** Subproblem: whether governing parameters are
  sufficient to advise, and when to abstain. Missing: parameter-availability indicator + abstention criteria. Topic:
  datasheet/governing-parameter sufficiency. Search terms: "datasheet key parameters interface", "abstention criteria
  technical advice". Required: governing-parameter documents + a governance-reviewed abstention rule. Risk: moderate–high
  (abstention correctness). Specialist: governance/technical reviewer category, only to validate the abstention rule.
- **PB-RQ-7 — Conditioning-need & method-routing indication (→ RQ-08/10; from CG-07).** Subproblem: signal a
  conditioning-need diagnostically and record a method-routing decision distinct from execution. Missing: diagnostic +
  routing fields. Topic: signal-conditioning need indication; decision routing. Search terms: "signal conditioning need",
  "decision routing rules". Risk: moderate. Specialist: not necessary.

## 4. No-candidate / no-appointment (preserved)
Phase B performs **no** person search, screening, identification, ranking, selection, recommendation, outreach, or
appointment. Competence attaches to evidence categories and methods, never persons. `UNVERIFIED CANDIDATE` remains a
content-status label only; historical candidate/appointment documents remain historical and non-activatable. Any
"specialist category" above is a category label only — never a named person or company.

## 5. Permitted evidence sources and evidence-quality requirements
Permitted sources (only upon a separate start authorization, and only within the authorized method — DOCUMENT REVIEW /
DATASHEET COMPARISON — when Gate 3A authorizes it): governing-parameter/technical documentation for the concept class;
authoritative standards/reference material for the named topics. **Excluded:** journey/personal/production data; paid or
restricted sources unless separately approved; confidential or uncertain-access sources; unbounded web retrieval. Every
recorded evidence item must carry: source identity, retrieval basis, an evidence-quality grade (e.g. ASSERTED / REASONED /
DEMONSTRATED-analogue), a validation-status marker, and an explicit uncertainty/abstention note. Evidence quality is never
inferred from vocabulary; it is recorded truthfully.

## 6. Phase B outputs and acceptance criteria (no technical conclusions invented here)
- **Outputs:** a per-RQ evidence record (sources + quality grades + what is/ is not established); an updated capability
  resolution status (which CG items evidence addresses vs. remains open); an explicit abstention log; a provenance record;
  and an owner-readable summary. No product artifact.
- **Acceptance criteria:** each addressed RQ has graded evidence with explicit uncertainty; abstentions are recorded where
  evidence is insufficient; no engineering conclusion is asserted beyond what the evidence supports; scope stayed within the
  concept class; provenance complete; ready for independent (non-authoring) review. Meeting acceptance does **not** convert
  any finding into an approved requirement or an implementation instruction.

## 7. Separate start authorization required
External research or any method execution **must not begin** until a **separate explicit owner start authorization** is
issued after reviewing this Draft PR. Recording this decision (and merging its PR) starts nothing.

## 8. Non-authorization boundary
This decision does not authorize: external research execution; TKP construction; architecture; schemas; prompts or AI logic;
database or persistence changes; UI changes; BASE RED tests; coding or implementation; integration; full D13 closure;
Workstream 8.

## 9. Mandatory post-D13 action (preserved)
After formal D13 closure, and **before** Workstream 8, an independent governance document — provisionally titled
**"Structured Invention Disclosure and Patent Export Owner Decision"** — must be created to record the structured disclosure
package and the patent-platform export-file decision, **without** authorizing implementation. This requirement is preserved
here and is not itself activated by this decision.

## 10. Governing identities
Package `D13-TKP-PKG-001`; Gate 3 `D13-TKP-PKG-001-G3-ISS-001` (expiry 2026-10-16 23:59 Asia/Kuwait; RQ-01…RQ-11);
Gate 3A `D13-TKP-PKG-001-G3A-ACT-001-PHASE-A` (Phase A only — a separate activation is required for any Phase B method);
Phase A closure via PR #219; risk-based model via PR #220. Applied under the risk-based execution and review model.
