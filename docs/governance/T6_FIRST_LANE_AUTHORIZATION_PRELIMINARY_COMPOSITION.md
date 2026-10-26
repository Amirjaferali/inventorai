# T6 FIRST-LANE AUTHORIZATION — PRELIMINARY ATTRIBUTED COMPOSITION

**Lane:** `T6-PRELIMINARY-COMPOSITION-PROJECTION-01`  
**STATUS: APPROVED AND FINAL (per-lane authorization) — NON-ACTIVATING.** The lane described here remains PROPOSED and INACTIVE and activates only upon the separate committed roadmap §§4–7 activation action. This finalization records no active-lane state and authorizes no implementation.

**Owner approval:** the Owner explicitly approved finalizing this per-lane authorization as APPROVED AND FINAL — NON-ACTIVATING on 2026-10-26, subject to four accuracy corrections (the MVP freeze carve-out statement in §1, the invocation entry in §2, and the §0 prerequisite table and roadmap findings in §5), which this text carries. Prepared in PR #875; finalized in its own documentation-only final-status commit.

**AUTHORITY LEVEL:** per-lane authorization under `docs/governance/TECHNICAL_REALIZATION_ANCHOR_COMPANION.md` §§0 and 9.

**DEPENDS ON (approval order):** anchor companion → path-N handoff contract → supported-technology / source-of-truth contract → evidence / artifact model → this document. `MVP_SCOPE_FREEZE.md` Amendment 1 is NOT in this chain: it does not cover this lane (§1); a separate append-only freeze carve-out for this lane is an activation prerequisite (§5), not a finalization prerequisite.

**Scope:** authorization material only; no product implementation, runtime invocation, generation, merge, deployment, Path T, D4, BOM, quantities, or multi-domain runtime orchestration is authorized by this document.

## 1. Authority and required activation sequence

This is the **separate per-lane authorization document** for this proposed lane, governed by `TECHNICAL_REALIZATION_ANCHOR_COMPANION.md` §§0 and 9; `OWNER_PRODUCT_IDENTITY_CORRECTION.md`; `DUAL_PATH_PRODUCT_ANCHOR.md`; `PATH_N_ORCHESTRATION_AND_HANDOFF_CONTRACT.md`; `SUPPORTED_TECHNOLOGY_AND_SOURCE_OF_TRUTH_CONTRACT.md`; `TECHNICAL_REALIZATION_EVIDENCE_AND_ARTIFACT_MODEL.md`; and `ACTIVE_EXECUTION_ROADMAP.md` §§4–7 and 12. The existing first-lane Adaptive Idea Orchestration authorization is **not** authorization for this T6 lane.

**MVP freeze carve-out — not covered.** `MVP_SCOPE_FREEZE.md` Amendment 1 narrows the freeze's "External document generation" item SOLELY for separately authorized, fully activated, **single-domain** Technical Realization work limited to capability disclosure, plain-language requirement translation, structured option analysis, option qualification or disposition, bounded recommendation and the `adaptive-decision-readiness-v1` decision-readiness artifact; it permits ONLY the operations and artifact declared by that activated per-lane authorization and expressly excludes BOM, component or material selection and complete invention / implementation package generation. This lane's composition is none of those operations, and it composes the records of an integrated two-part (Mechanical + Electrical / Electronics) project. Amendment 1 therefore does **not** cover this lane, and nothing here relies on it. A separate append-only freeze carve-out naming exactly this read-only composition is an **activation** prerequisite (§5, row 4); it is not created, proposed or implied by this document.

The Companion §0 sequence remains binding **in full**: (1) separate per-lane authorization; (2) explicit Owner activation approval; (3) all required documents finalized to their required non-DRAFT status and final-status commits; (4) prerequisite authority/architecture documents approved and committed; (5) all lane activation prerequisites met; (6) no unresolved authority/governance blocker; (7) the **final** roadmap §§4–7 active-lane state committed. Preparation, finalization or merge of this document satisfies **none** of the activation transitions: its Owner approval and final-status commit satisfy only §0(1)–(3) for this document itself (see §5). Until each condition is established from authoritative repository evidence, this lane stays **INACTIVE**.

## 2. One exact future invocation boundary

**Only if separately activated:** one explicit, authorized, read-only request in existing **Orchestrated Idea Mode (Path N)**, for **one** existing saved project, entering through the existing central project authorization (the same authenticated project-access check every project route uses) and reading the Stage 15 owner **only** through its existing validated single-snapshot reader, `load_participation_preparations` (`engine/record_store.py`). That reader returns, from ONE consistent read snapshot validated whole, the project's declared interactions, its CURRENT component projection, every stored participation row and every stored participation preparation; the current notes are then selected by the Stage 15 owner's own `current_participation_preparations` (`engine/subsystem_model.py`). This is the mutually consistent set of current, authorized owner records the request observes. The FDC-001 → Technical Realization handoff (`fdc-to-tr-handoff-v1`, `PATH_N_ORCHESTRATION_AND_HANDOFF_CONTRACT.md` §3) is **not** the entry: its future structures are not implemented, and its fields carry no component, interface, participation or preparation identity. No second project identity, no Path T entry, no specialist-work transfer, no cross-domain technical execution or multi-domain runtime orchestration. Fail closed for unreadable, mismatched, foreign, stale, withdrawn, or unqualified owner references. It must never silently replace missing data with inferred data.

This is a **proposed invocation contract**, not a claim that the invocation exists or is currently permitted.

## 3. Smallest nonduplicative inventor-facing result

The future output is **one ephemeral, preliminary, non-binding attributed composition** of *existing* owner records, rather than an editable engineering record or a restatement of report sections. It may organize **explicit, identity-bound links** already held by the canonical Stage 15 owner:

- one current inventor-declared component identified by its existing `component_id` and current component revision;
- one current inventor-declared interface/interaction identified by its existing `interface_id`;
- a validated current `InterfaceParticipation` pair `(interface_id, component_id)` that explicitly says this component participates in that interaction;
- optional `ParticipationPreparation` for that **same pair**, exposing the inventor's stated expected observable contribution and evidence/review need, distinguishing currently recorded, earlier/not reconfirmed, not recorded, and unavailable without turning any note into verification.

**Illustrative conditional chain, not a fetched project or an inferred engineering fact:** *owner-declared component C* → *owner-declared participation (I,C)* → *owner-declared expected contribution / check preparation for (I,C)*. This is meaningful because a recipient can trace the **specific physical-component identity, the declared interaction participation, and the particular unresolved verification work** together. Existing report and PDF presentations are retained unchanged and are not treated as this future invocation. If these exact records do not exist or do not cross-validate, no chain is generated.

IdeaState statements, current requirements from Requirement Landscape, and Validation Plan steps may appear as **separately attributed references** only where their owning contract provides an exact qualified identity and relationship. A requirement-to-component link, an assumption conflict, or a technical-method result must **not** be joined by matching text, domain, proximity, or chronology. Missing qualified links are visibly **UNRESOLVED**, not constructed.

## 4. Truth ownership and excluded operations

Stage 15 exclusively owns components, subsystems, interfaces, participation and preparation. IdeaState owns inventor assertions/constraints; Requirement Landscape alone owns its governed derived requirement projection; Validation Plan alone owns its governed preparation steps; qualified technical methods keep their own scientific, numerical, licensing and IP authority. This proposed lane **only composes owner references**, with origin/provenance, current-versus-historical state, validation/evidence limits and missing/unknown markers attached. It does not modify any owner or persist an independent technical-truth artifact.

**Never:** infer components, mechanisms, extra participating parts, relationship direction, requirement satisfaction, calculation inputs/results, counts or BOM lines; select, size, rate, dimension, qualify suitability, claim compatibility, safety, validation, manufacture, assembly completion or production readiness. A stated component does not imply quantity one, verified applicability, or purchase suitability. A missing relationship is not an invitation to make one. No new engine, registry, ontology, artifact store, source-of-truth ledger, calculation owner or technical domain is authorized.

## 5. Exact lane prerequisites and activation STOP

| Companion §0 condition | Status of this proposal | Evidence/action required before activation |
|---|---|---|
| 1. Separate per-lane authorization | **SATISFIED** | This document, APPROVED AND FINAL (per-lane authorization) — NON-ACTIVATING |
| 2. Explicit Owner approval | **Per-lane authorization: SATISFIED (2026-10-26). Activation: NOT SATISFIED** | Separate express Owner approval to activate this exact bounded lane; approval of this document is not activation approval |
| 3. Required non-DRAFT final-status commits | **SATISFIED for this document by its own final-status commit, effective on the verified merge of its documentation-only PR; NOT SATISFIED for the freeze carve-out of row 4** | Each further required document needs its own final status and final-status commit; a PR or unrelated commit does not count |
| 4. Approved committed prerequisite authorities | **NOT SATISFIED — MVP freeze carve-out missing** | The Companion, the handoff contract, the supported-technology / source-of-truth contract and the evidence / artifact model state APPROVED AND FINAL. `MVP_SCOPE_FREEZE.md` Amendment 1 does not cover this lane (§1): a separate, Owner-authorized append-only carve-out for exactly this read-only composition, in its own final status and final-status commit, is required before activation |
| 5. Declared activation prerequisites | **NOT YET DEMONSTRATED** | Verify exact current-record consistency, project authorization, provenance/status and lane-invocation gates in the separately approved scope; no feature or runtime existence is presumed |
| 6. No unresolved authority blocker | **NOT ESTABLISHED** | Confirm lane does not invoke D4, Path T, inactive cross-domain orchestration, unqualified links or an ineligible report/technical capability |
| 7. Final roadmap §§4–7 active-state commit | **NOT SATISFIED** | A separately authorized §§4–7 activation update and its commit, **only after** all preceding conditions |

**Roadmap findings (read directly from `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` at the finalization base `99dee6c2a9ff3e163c2e79bf529e9e10669c8cec`).** §4 records exactly one lane state, the Adaptive Idea Orchestration first lane, ACTIVE by its own committed §§4–7 update; §§4–7 record **no** T6 lane, proposed or active; §6 records the completed Phase 4 lane; §7 authorizes only read-only verification and review without an exact-scope Owner authorization. §12 (APPROVED AND FINAL, non-activating) records and gates the first lane only; its §12.A states that the finalization, approval or commit of a non-activating proposed-lane authorization does NOT trigger active-lane state recording and does NOT make the roadmap stale. This finalization therefore requires, and makes, **no** roadmap change; only a later committed §§4–7 activation update could record this lane as active. No existing active Path-N lane activates this separate T6 operation.

**STOP / reopening trigger:** Any unsatisfied §0 condition keeps the lane inactive. Reopen for activation only on the exact final-status documentary evidence, completed prerequisite proof, express Owner activation decision and eligible roadmap state commit. A preliminary preferred scope, this document's preparation, or an unrelated merge supplies no authority.

## 6. Minimal future acceptance evidence (not implementation authority)

If and only if activation and later implementation are separately authorized, the scope must be proven against a synthetic saved project with explicitly declared `component_id`, `interface_id`, participation and optional preparation: identity/provenance fidelity, historical/withdrawn/unavailable abstention, no invented relationships, authenticated project isolation, deterministic read-only behavior, bilingual disclosure where applicable, and absence of effect on present reports, exports, persistence, D4, Path T, BOM and all engineering conclusions. Tests and hosted CI follow the existing repository FCR policy when a separately authorized PR actually implements product behavior.

**Current state: APPROVED AND FINAL (per-lane authorization) — NON-ACTIVATING. The lane remains PROPOSED and INACTIVE. No runtime or product behavior changes, and no activation, implementation, Path T, D4, BOM or roadmap state change is authorized.**
