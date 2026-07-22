# D13-TKP-PKG-001 — Technical Knowledge Package (TKP)

**Status:** constructed under the Owner Start Authorization "D13-TKP-PKG-001 TKP Construction Only", strictly within the
scope recorded and merged through **PR #224**
(`docs/governance/D13_TKP_PKG_001_TKP_CONSTRUCTION_OWNER_DECISION_AND_SCOPE.md`). **Working-tree artifacts — not
committed, not pushed, not published, not merged.** Delivered for independent (non-authoring) review.

**Authoritative base tip:** `829267d8e4f6f77c6e4d16e2704a36b50ac9ee33` (Merge PR #224; parents `760cc197`+`a4055934`;
tree `7077536c`). Workspace branch `research/d13-tkp-pkg-001-tkp-construction` created **from** this tip. The Phase A
branch `research/d13-tkp-pkg-001-phase-a-read-only-analysis` remains fixed at `57e2fac8` and is untouched.

## 1. What this package is
A **bounded technical-knowledge artifact** that organizes the verified, reasoned, unresolved, contradicted, and abstained
findings for the approved concept class. It is a **knowledge record**, tracing every unit to accepted Phase A / Phase B
evidence. It is **not**: product implementation; application architecture; executable AI logic; a compatibility
calculator; a device-selection engine; a person/company recommendation system; or a final engineering approval.

## 2. Scope lock (concept class — Gate 2)
Single-signal sensor→microcontroller interfacing: **analog-voltage / single-ended-digital / pulse-frequency;
low-voltage; non-safety-critical.**

**Excluded (must remain excluded):** buses (I²C/SPI/1-Wire/UART/CAN); differential interfaces; wireless; mains;
high-power; safety-critical systems.

## 3. Canonical evidence basis (accepted & merged only)
- **Phase A** — `research/d13-tkp-pkg-001/phase-a/` (PR #218 preserved; PR #219 closed): CG-01…CG-07, MF-01…MF-10.
- **Phase B** — `research/d13-tkp-pkg-001/phase-b/` (PR #222 merged; PR #223 accepted/closed): PB-RQ-1…PB-RQ-7,
  evidence grades, source register S1…S18, abstentions AB-1…AB-10, contradictions/scope-exclusions.
- **Governing decision** — PR #221 (Phase B scope), PR #224 (TKP construction decision). Risk model — PR #220.

**No unrecorded session narrative, memory, or conversation history is treated as technical evidence.** Every knowledge
unit carries a `Traces-to:` citation into the files above.

## 4. Package contents
| File | Purpose |
|---|---|
| `README.md` | Package index + scope lock (this file) |
| `knowledge-unit-register.md` | Canonical knowledge units KU-01…KU-07 (technology-first order) |
| `evidence-and-provenance-register.md` | Evidence items, grades, sources, provenance, access limitation |
| `uncertainty-and-abstention-register.md` | Explicit uncertainties and abstentions (AB-1…AB-10) |
| `contradiction-and-unresolved-issue-register.md` | Scope exclusions, resolution-dependent params, open issues |
| `validation-status-matrix.md` | Per-unit validation & acceptance status |
| `owner-readable-summary.md` | Plain-language package summary |
| `construction-completion-and-acceptance.md` | Completion record + acceptance-criteria check |

## 5. Invariants honored
- **Technology-first order** in every knowledge unit: technology & unresolved problem → missing information →
  verification method & required evidence → what InventorAI can verify → what it cannot verify → uncertainty & risk →
  specialist category only when genuinely necessary.
- **Evidence semantics preserved without upgrading:** PRIMARY-VERIFIED (only where independently established), REASONED,
  DEMONSTRATED-analogue, SEARCH-SURFACED, DEVICE-SPECIFIC-ABSTAINED, unresolved, contradicted.
- **Primary vendor-document access limitation remains visible** (Phase B primary PDFs returned HTTP 403; governing
  parameters corroborated via search, not primary-verified) — **not misrepresented as primary-source verification.**
- **Device-specific numeric conclusions remain abstained** unless supported by an actual target datasheet already in the
  accepted evidence basis (none is).
- **No-candidate / no-appointment:** no person/company search, recommendation, ranking, selection, outreach, or
  appointment; any specialist reference is a category label only.

## 6. Non-authorization
Constructing this package authorizes none of: architecture; schemas or structured-output implementation; prompts or AI
logic; database or persistence changes; UI; BASE RED tests; coding or implementation; integration; full D13 closure;
Workstream 8; Structured Invention Disclosure or Patent Export implementation. Owner acceptance of the completed TKP is a
separate decision; the mandatory post-D13 "Structured Invention Disclosure and Patent Export Owner Decision" remains
binding.
