# Structured Owner Criticality Capture — Bounded Governance Design (Proposal)

Status:
`PROPOSED BOUNDED GOVERNANCE DESIGN — NON-ACTIVATING; NOT AN IMPLEMENTATION AUTHORIZATION`

Authoritative baseline at drafting:
`1a8558fa37eab8ffcdaea0204e5b4d45906200e5` (feature/atomic-json-session-persistence
tip; two-parent merge of PR #94, parents `045d3cc` and `305b7af`). The live tip is
always resolved from Git; this SHA is a document-publication baseline, not a
permanent live-tip assertion.

## 0. Authority, order, and non-authorization

This document is a bounded, owner-gated **DESIGN PROPOSAL** for a possible future
feature, *Structured Owner Criticality Capture*. It is subordinate to, and must be
read after, the CLAUDE.md-ordered authority set:
`ILT-002_GOVERNANCE_ANCHOR.md`, `OWNER_PRODUCT_IDENTITY_CORRECTION.md`,
`STRATEGIC_PRODUCT_VISION.md`, `PATH_N_CURRENT_EXECUTION_ANCHOR.md`,
`DUAL_PATH_PRODUCT_ANCHOR.md`, `ACTIVE_EXECUTION_ROADMAP.md`, the merged Increment 4
authority/design/contract (`INCREMENT_4_AUTHORITY_RULINGS.md`,
`INCREMENT_4_DESIGN.md`, `INCREMENT_4_IMPLEMENTATION_CONTRACT.md`), Increment 5, and
`MVP_SCOPE_FREEZE.md`. Where any of those and this proposal could differ, they
control.

This document authorizes NOTHING to be built. It creates no implementation
contract, no tests-first authority, no tests, no source/schema/session/template
change, no persistence work, no question-flow change, no roadmap state change, and
no `main` sync. It does not activate any lane, gate, increment, or carve-out. It is
a design record for owner review only. See §7 for the explicit non-activation
clause.

This proposal follows the read-only assessment that concluded free-text criticality
derivation is governance-blocked under C4-R4/D-4 ("no keyword detector, heuristic,
or LLM inference may elevate criticality"), and that the only governance-compatible
future direction is an **explicit, structured, owner-confirmed** signal — never
extraction from prose.

---

## 1. Product purpose

### 1.1 The gap this addresses
Today the deliverable honestly reports `Criticality: UNDETERMINED (system-derived)`
for every requirement, because the repository holds **no structurally addressable
signal** of how important the inventor considers each assumption, requirement,
constraint, unknown, or validation item. This is correct and conformant under
Increment 4 (D-4), not a defect. But it means the deliverable cannot yet reflect
the inventor's own sense of what is essential versus adjustable.

### 1.2 Why structured capture may improve InventorAI
Asking the inventor **explicit, structured** questions — e.g. "Which of these
assumptions are essential to your idea?", "Which are adjustable?", "Which requirement
is non-negotiable?", "Which items remain unknown?" — and preserving the discrete
answers as **owner-confirmed** signals would let the deliverable surface the
inventor's *own* prioritization. This supports the MVP core hypothesis ("structured
progression materially improves inventor clarity and decision quality") by helping
the inventor separate what the idea depends on from what it can flex on — a thinking
aid, not a judgement.

### 1.3 What it is explicitly NOT
It is not, and must never become: validation, verification, scoring, readiness,
safety assessment, feasibility assessment, certification, patentability, market
assessment, or an engineering/medical/veterinary/legal/regulatory judgement. It
records **what the inventor said about importance**, tagged as owner-confirmed and
not validated — nothing more. It introduces no numeric score and no maturity/stage
coupling (C4-R4: "maturity alone MUST NEVER ground criticality"; "there MUST be no
numeric scores").

---

## 2. Governance boundary (hard constraints on any future implementation)

Any future implementation of this feature MUST observe all of the following. These
mirror C4-R4/D-4 (criticality derivation boundary) and D-5/C4-R6 (risk grounding):

- **No keyword detection** of words like "essential", "must", "critical",
  "adjusted", or any lexical trigger.
- **No semantic parsing** of free-text answers to infer importance.
- **No LLM / heuristic / classifier inference** of criticality from prose.
- **No automatic risk generation from prose.** D-5/C4-R6 forbid manufacturing a
  risk (or a "dependency concern" derived as a consequence) from free text; the
  `_s6` risk register MUST remain unchanged; any structural adverse-consequence
  support requires separate authority and design.
- **No system inference presented as owner-confirmed** (C4-R5). Only an explicit,
  discrete owner selection may carry `owner-confirmed`.
- **No technical / safety / specialist validation claims**, and no implication of
  feasibility, readiness, certification, patentability, or market fit.
- **Structured input only.** The signal must originate from a discrete owner choice
  (e.g. a selection among presented options), never from parsing what the inventor
  typed in a free-text field.

If, at design time, any of these cannot be honored deterministically, the correct
result remains `UNDETERMINED (system-derived)` and the feature is not built.

---

## 3. Authority model

### 3.1 Owner-confirmed authority (already defined by C4-R5)
C4-R5 already defines exactly four criticality authorities:
`system-derived`, `owner-confirmed`, `specialist-confirmed`, `undetermined`. This
feature would populate **`owner-confirmed`** — and only from an explicit structured
owner selection. C4-R5 is explicit that "a system inference MUST NEVER be presented
as owner-confirmed or specialist-confirmed"; this feature must satisfy that by
sourcing the label solely from a discrete owner choice, with a recorded rationale
referencing that structured selection (C4-R4: "every non-`UNDETERMINED` category
MUST carry recorded rationale").

### 3.2 Visible authority label preserved
The deliverable MUST continue to display the authority next to the category, e.g.
`Criticality: <category> (owner-confirmed; not validated)`. The authority is never
hidden, never spoofed, and never upgraded to `specialist-confirmed` or to any
technical-validation status.

### 3.3 Default behavior preserved (backward compatibility)
When **no** structured owner signal exists for an item — which is every existing
session and every item the inventor does not classify — the output MUST remain
exactly `Criticality: UNDETERMINED (system-derived)`. The current Increment 4
behavior is the default and is preserved byte-for-byte in the absence of an explicit
owner selection. No migration of existing behavior; absence of the signal is an
honest `UNDETERMINED`, not an error.

---

## 4. Category design

### 4.1 The committed C4-R4 vocabulary is authoritative
The governed criticality categories are fixed by C4-R4:
`FEASIBILITY-THREATENING`, `VALUE-ENHANCING`, `REFINEMENT`, `UNDETERMINED`. These
describe the *evidenced effect of an unmet requirement on the idea's essential
function* — not maturity, readiness, stage, scoring, or progression.

### 4.2 Reconciling owner-friendly labels
The inventor-facing wording (essential / adjustable / optional / unresolved) is a
plain-language *presentation* of the owner's choice and is **not** a new stored
category. A proposed (future, approval-required) mapping to the committed vocabulary:

| Owner-facing choice (plain language) | Committed C4-R4 category | Authority |
|---|---|---|
| "Essential — my idea fails without it" | `FEASIBILITY-THREATENING` | `owner-confirmed` |
| "Adjustable — the idea still works with design changes" | `VALUE-ENHANCING` | `owner-confirmed` |
| "Optional — a refinement, not required" | `REFINEMENT` | `owner-confirmed` |
| "Unresolved / not sure" | `UNDETERMINED` | `system-derived` (or `undetermined`) |

Notes and cautions on the mapping (all deferred to a later, separately-approved
design/contract; nothing fixed here):
- The mapping above is **proposed**, not adopted. It must be reviewed against the
  exact C4-R4 semantic definitions before any adoption; the owner's "essential"
  must be shown to correspond to the C4-R4 *essential-function-impact* meaning, not
  to a looser everyday sense.
- **No new active criticality category is introduced.** If a future design concludes
  the owner's mental model cannot be faithfully expressed within the four committed
  categories, then adding or renaming a category is a **separate C4-R4 amendment**
  requiring its own governance approval and implementation-contract precision
  (D-4: "Any future elevation rule requires separate implementation-contract
  precision and MUST remain within C4-R4"). This document does not make that change
  and does not authorize it.
- Because the label reflects owner opinion, not evidence of essential-function
  impact, the deliverable wording must keep it clearly owner-sourced and
  not-validated (see §5), to avoid implying the system evidenced the category.

---

## 5. Advisory language (mandatory framing for any future rendering)

Any owner-confirmed criticality shown in the deliverable MUST be accompanied by
framing that preserves every boundary, for example:
`Criticality: FEASIBILITY-THREATENING (owner-confirmed; not validated)`,
with the section carrying the advisory that these reflect the inventor's own stated
importance and are:

- **owner-confirmed only** — the inventor's stated view, recorded verbatim as a
  discrete choice;
- **not technically validated**;
- **not safety validated**;
- **not build-ready**;
- **not certification-ready**;
- **not market-ready**;
- **advisory only** — no analysis, judgement, or verification is implied.

This framing is consistent with the deliverable's existing honesty language
("Derived readiness", "not technically verified") and MUST NOT be weakened.

---

## 6. Future implementation path (sequenced, each step separately owner-gated)

This feature is **increment-sized**, not a bounded presentation PR. If the owner
later chooses to pursue it, the safe sequence is:

1. **Governance design approval** — owner review and approval of this document (and
   any revision of it) as the semantic/boundary design.
2. **MVP_SCOPE_FREEZE revision or amendment (if required)** — the ACTIVE freeze
   treats new question flows as scope expansion governed by its REVISION PROTOCOL
   ("Freeze expands only after: 3 real ideas tested through LEVEL 0-2; ≥1 genuine
   BLOCK understood; ≥1 idea reached LEVEL 2 with documented clarity improvement;
   missing gap/rule identified through real usage, not anticipation"). A structured
   capture question flow needs either that protocol satisfied or an explicit
   owner scope decision/amendment. Owner approval required.
3. **Separate increment implementation contract** — a sibling to Increment 4/5
   fixing exact semantics, the stored field, category mapping, rendering, backward-
   compatible defaults, and test obligations (tests-first authority granted there,
   not here).
4. **Schema / session-state design** — a new structured per-item field capturing the
   discrete owner classification; default absent → `UNDETERMINED (system-derived)`;
   no persistence work implied (sessions remain in-memory unless the persistence
   lane is separately authorized).
5. **UI / question-flow design** — explicit structured prompts capturing discrete
   owner selections (one-per-iteration-compatible), never free-text parsed.
6. **Engine / rendering changes** — a deriver reads the structured signal → sets the
   governed category + `owner-confirmed` authority + recorded rationale; the default
   `UNDETERMINED (system-derived)` path is unchanged; `_s6` unchanged.
7. **Tests** — owner-confirmed display; default-`UNDETERMINED` preservation;
   no-free-text-elevation; authority never spoofed; `_s6` unchanged; Sections
   10/11/13/14 regression; full-suite/baseline (`test_domain_registry.py`) unchanged.
8. **Review and true-merge** — each step delivered as a bounded, owner-authorized PR,
   independently read-only reviewed, then owner-authorized true (two-parent) merge,
   followed by post-merge verification — the discipline used for PRs #91–#94.

Every step above is future and separately gated; none is authorized by this
document.

---

## 7. Explicit non-activation clause

- This document does **not** authorize implementation.
- This document does **not** change current behavior or runtime output.
- This document does **not** authorize criticality extraction from free text.
- This document does **not** authorize risk generation (from prose or otherwise);
  `_s6` remains unchanged.
- This document does **not** authorize persistence work.
- This document does **not** authorize schema, session-state, question-flow,
  template, or test changes.
- This document does **not** authorize a `main` sync, a PR, or a merge.
- This document does **not** adopt the §4.2 mapping or any new category; that mapping
  is a proposal requiring separate C4-R4-conformant approval.
- Absent a separate, fully-approved increment contract and the applicable
  authorizations, the current Increment 4 behavior (`UNDETERMINED (system-derived)`)
  remains the only conformant output.

This is a design record for owner review. It confers no authority by implication.
