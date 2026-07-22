# D13-TKP-PKG-001 — TKP Construction Owner Decision and Scope

**Status:** OWNER DECISION — bounded scope definition for construction of the D13-TKP-PKG-001 Technical Knowledge
Package (TKP). **Non-activating:** recording (and merging) this decision **starts no construction**; a separate,
explicit owner start authorization is required (see §9). Prepared under the risk-based execution and review model
(PR #220).

## 1. Canonical evidence basis
The TKP may rely **only** on the accepted and merged Phase A and Phase B records and evidence — specifically **PR #219**
(Phase A formal closure), **PR #221** (Phase B decision and research scope), **PR #222** (Phase B research evidence
package), and **PR #223** (Phase B formal acceptance and closure) — together with the artifacts those PRs preserved
(the Phase A 12-file package under `research/d13-tkp-pkg-001/phase-a/` and the Phase B 8-file package under
`research/d13-tkp-pkg-001/phase-b/`). **No unrecorded session narrative, memory, or conversation history may be treated
as technical evidence.** Every knowledge unit must trace to a committed, accepted record.

## 2. Purpose of the TKP
The TKP is a **bounded technical-knowledge artifact** that organizes the **verified, reasoned, unresolved,
contradicted, and abstained** findings for the approved **single-signal sensor-to-microcontroller** concept class
(analog-voltage / single-ended-digital / pulse-frequency; low-voltage; non-safety-critical). It is a knowledge
record, not a product.

It is explicitly **not**: product implementation; application architecture; executable AI logic; a compatibility
calculator; a device-selection engine; a person or company recommendation system; or a final engineering approval.

## 3. Required TKP structure
The construction scope must define package sections that preserve, per knowledge unit, all of:
- concept-class and scope lock;
- unresolved technical subproblem;
- missing technical information;
- relevant technology or research topic;
- suggested technical search terms;
- required measurements, documents, or tests;
- governing technical parameters;
- evidence references and provenance;
- evidence grades;
- what InventorAI can verify;
- what InventorAI cannot verify;
- risk and uncertainty;
- contradictions and unresolved issues;
- explicit abstentions;
- specialist category **only when genuinely necessary** (category label only);
- validation and acceptance status.

## 4. Evidence semantics (no upgrading)
The TKP must **preserve the existing evidence distinctions without upgrading them**:
- **PRIMARY-VERIFIED** — only where independently established;
- **REASONED**;
- **DEMONSTRATED-analogue**;
- **SEARCH-SURFACED**;
- **DEVICE-SPECIFIC-ABSTAINED**;
- **unresolved** or **contradicted**.

The **primary vendor-document access limitation** (Phase B: primary PDFs returned HTTP 403 under the authoring
environment egress policy; governing parameters corroborated via search, not primary-verified) **must remain visible**
and **must not be misrepresented as primary-source verification**. **Device-specific numeric conclusions must remain
abstained** unless supported by the actual target datasheet or separately authorized primary evidence.

## 5. Technology-first ordering
Every technical guidance unit must preserve this order:

> technology and unresolved problem → missing information → verification method and required evidence →
> what can and cannot be verified → uncertainty and risk → specialist category only if necessary.

**No named person, company, candidate, or appointment may appear.** Competence attaches to evidence categories and
methods, never persons; any "specialist category" is a category label only.

## 6. Proposed construction outputs (NOT created here)
The future construction is scoped to produce:
- package README and scope lock;
- canonical knowledge-unit register;
- evidence and provenance register;
- uncertainty and abstention register;
- contradiction and unresolved-issue register;
- validation-status matrix;
- owner-readable package summary;
- construction completion and acceptance record.

**These outputs are NOT created under this authorization.** This document defines their scope only.

## 7. Acceptance criteria (for the future construction)
The future construction must **not** be considered complete unless **all** hold:
- every knowledge unit traces to accepted Phase A or Phase B evidence;
- no evidence grade is overstated;
- abstentions remain explicit;
- device-specific conclusions are not invented;
- out-of-scope buses, differential interfaces, wireless, mains, high-power, and safety-critical topics remain excluded;
- no candidate or appointment activity is introduced;
- independent non-authoring review verifies the package;
- the owner separately accepts the completed TKP.

## 8. Explicit non-authorization
Recording and merging this decision **starts no construction** and authorizes **none** of: creation of the TKP files;
architecture; schema or structured-output implementation; prompts or AI logic; database or persistence changes; UI;
BASE RED tests; coding or implementation; integration; full D13 closure; Workstream 8; candidate search,
recommendation, selection, or appointment; Structured Invention Disclosure or Patent Export implementation.

## 9. Separate start gate
**Actual TKP construction requires a later, separate, explicit owner start authorization** issued **after** this Draft
PR is reviewed and merged. Until then, no TKP file may be created.

## 10. Post-D13 requirement (preserved, still binding)
After formal D13 closure and **before** Workstream 8, an independent governance document — provisionally titled
**"Structured Invention Disclosure and Patent Export Owner Decision"** — must be recorded to capture the structured
disclosure package and the patent-platform export-file decision, **without** authorizing implementation. This
requirement remains binding and is **not** activated by this decision.

## 11. Governing identities and locks
Package `D13-TKP-PKG-001`; Gate 3 `D13-TKP-PKG-001-G3-ISS-001` (expiry 2026-10-16 23:59 Asia/Kuwait; RQ-01…RQ-11).
Phase A closed via PR #219; Phase B closed as a bounded research phase via PR #223. Phase A branch
`research/d13-tkp-pkg-001-phase-a-read-only-analysis` remains fixed at `57e2fac837f333224b2f985be285fe9e0a9f6243`.
PR #167 (`74ea297f…`) and PR #162 (`088ab884…`) remain untouched. No `.bundle` and no research-artifact change is part
of this record. Applied under the risk-based execution and review model (PR #220).
