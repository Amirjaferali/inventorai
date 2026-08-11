# P9-QS — Phase-9 Technical Quality Standard — Governance Contract (corrected)

**Status of THIS record:** governance/documentation-only **CONTRACT CANDIDATE** (P9-QS). **It becomes AUTHORITATIVE only if
this exact accepted candidate is independently reviewed, Owner-accepted, published SHA-preserving, merged (create-a-merge-commit),
and post-merge verified.** Until then it authorizes nothing. It is a **quality/governance standard**, **not** a runtime engine,
registry, ledger, readiness engine, constraint engine, unit engine, calculation engine, or prototype/manufacturing engine. It
**implements nothing**, changes no runtime/test/web/Domain-Pack/schema/prompt file, activates no domain, and starts no Phase-9
work. **DOCUMENTED NO-VALID-RED — GOVERNANCE-ONLY CONTRACT GATE.** This contract does not authorize Phase 9, any domain
activation, IoT, D8 resolution, D4, a future deterministic-calculation capability, units runtime, CAP-12/CAP-13/WS-PFV, STG,
Output-Language, calculation adapters, Phase 10, PSRR, deployment, or production.

**Authoritative base:** `99c08555351e031bd3cc11f536cf558c91dc0c32` (PR #436 — D3 formal closure merge; parents `e51eaf7` +
`9cb5b7f`; tree `0e08af0458f642715d247bfef11b28ac5015ec27`), verified read-only before editing; boot OK.

**Correction lineage (this is a fresh, corrected candidate).** A prior P9-QS candidate `6a3e25df79bfe2399474a1ecf9154ca3ccfbe307`
received independent review verdict **REJECT — GOVERNANCE INCONSISTENCY** and is **NOT** accepted / NOT merged / NOT to be reused
as an accepted candidate (historical rejected evidence only). This corrected candidate is built fresh from the authoritative
parent and fixes the two blocking findings — **B1** (the identifier `CAP-06` is repository-canonical for *Multi-Axis Invention
Readiness Dashboard* and must NOT denote deterministic calculations) and **B2** (Output-Language is NOT a repository-authoritative
pre-new-domain activation prerequisite) — and addresses the non-blocking observations O1/O2/O3.

**Basis (development/review inputs — NOT committed repository authority).** This contract's content derives from session-level
contract-development analysis: the Phase-9 Capability Overlap & Preservation Audit, the Expanded Phase-9 Audit Addendum, and the
Remaining-Obligation Sweep. **Those analyses are review/development inputs, not committed repository documents;** repository
evidence remains the authority for all durable claims herein. Subordinate to CLAUDE.md and the committed anchors. **D-FPC-MAP-06:**
reuse existing canonical owners; create no new owner. **Phase 9 remains NOT AUTHORIZED / INACTIVE.**

---

## §1. Purpose & non-goals

**Purpose.** Define the minimum technical/governance quality that MUST be satisfied **before any future Phase-9 specialist-domain
activation contract may proceed**. **Non-goals (binding):** P9-QS is NOT a runtime engine / new Domain Registry / new activation
policy / second evidence or decision-assumption ledger / second readiness or constraint engine / unit engine / calculation
engine / prototype-manufacturing engine. It reuses existing canonical owners only.

## §2. Binding separation of states

1. **Recognition does NOT imply qualification** (a RECOGNIZED_NOT_ACTIVATED pack, §5-I2, is not quality evidence).
2. **Qualification does NOT imply Owner authorization.**
3. **Owner authorization does NOT itself imply runtime activation** (activation = the governed §5-I2 allowlist gate completes).
4. **Activation does NOT imply multi-domain composition authority** (that is the separate **D4** gate).
5. **Phase-9 activation does NOT imply Phase 10, PSRR, deployment, production, or commercial readiness.**

## §3. Activation-quality standard (relative to each domain's TRUTHFUL declared capabilities)

A future activated specialist domain MUST, **within its declared capability boundaries**, be able to: ask correct domain-specific
questions; detect meaningful technical gaps; detect contradictions where evidence permits; distinguish evidence from assumptions;
preserve provenance; represent known unknowns; **refuse or degrade safely when unsupported**; consume deterministic checks where
applicable; preserve **recognition-vs-activation** separation; satisfy cross-domain boundary tests (§6); and provide objective
activation-qualification evidence (§7). **Quality is judged relative to the domain's truthful declared capabilities — a domain is
NOT required to support every technical function.**

## §4. Domain Capability Contract (extension of existing Domain-Pack / Registry ownership — NO new registry)

Every future specialist Domain Pack MUST expose a **truthful, canonical/machine-readable capability declaration** through the
existing **`engine/domain_registry.py` (§5-I1)** Domain-Pack ownership, expressing, where applicable: supported analysis
categories; explicitly **unsupported** categories; required inputs/evidence; supported evidence categories; supported
deterministic checks; supported calculations; validation capabilities; safety boundaries; supported output classes;
dependencies; known limitations. **Truthfulness rule (binding):** a domain MUST NOT imply a capability that is not implemented and
qualified (e.g. FEA / fatigue analysis / manufacturing certification are **non-binding examples**, never per-domain requirements).
**No second registry is created.**

## §4b. Knowledge-source / provenance / licensing reuse (reference/reuse only — O3)

Future Domain-Pack knowledge sources and content MUST respect the **existing** knowledge-source / evidence-governance and
source-provenance/licensing governance — notably the **D13 knowledge-governance family** (e.g.
`D13_KNOWLEDGE_GOVERNANCE_RESEARCH_CONTRACT.md`, `D13_GATE3_APPOINTMENT_PACKAGE_AND_EVIDENCE_GOVERNANCE_STANDARD.md`,
`D13_PRIORITY_AND_KNOWLEDGE_GOVERNANCE_OWNER_DECISION.md`) and the existing evidence provenance owners
(`engine/record_contract.py`/`record_store.py`; the §5-I1 Domain-Pack provenance manifest). This is a **reference/reuse clause
only**: P9-QS creates **no** new knowledge-source or licensing framework, expands into no implementation, and does **not**
duplicate CAP-12/CAP-13 source-feasibility ownership.

## §5. Evidence / assumptions / contradictions (reuse existing owners — NO second ledger/engine)

Reuse the existing canonical owners: evidence/provenance (`engine/record_contract.py` + `engine/record_store.py`, verbatim
provenance; `engine/idea_state.py`); assumptions/decisions (`engine/decision_workspace.py`); contradiction/supersession (record
model + `engine/derived_readiness.py`); validation (`engine/validation_plan.py`; `engine/stage3_evaluator.py`);
requirements/criticality (`engine/requirement_landscape.py`); readiness/maturity (`engine/derived_readiness.py`). Domain-specific
constraint/contradiction checks MUST integrate as **evidence/validation producers under existing ownership** — NOT as a second
Engineering Evidence Ledger, Decision/Assumption Ledger, Constraint Engine, or readiness model.

## §6. Cross-domain boundary-test minimum + §7 activation qualification with regression protection

**Minimum boundary tests** every future domain qualification MUST consider, where relevant: positive representative journeys;
negative / out-of-domain cases; ambiguous-domain cases; known-unknown cases; recognition-vs-activation boundaries; **regression
against already-activated domains**; domain-specific safety behavior. **No numeric thresholds are invented** (none are governed
today). **Activation qualification MUST prove BOTH:** (A) the new domain works within its declared scope; **and** (B) the new
domain **does not materially degrade already-activated domains** (the D3 full-suite-green precedent generalized). Qualification
binds the existing benchmark governance (`benchmark/run_benchmark_v1.py`; `docs/benchmarks/…`), scoring
(`engine/scoring.py::score_case`, `scoring_version`), §5-I1 Domain-Pack validation, §5-I1 Domain Registry, §5-I2 Domain
Activation, regression evidence, and capability-declaration truthfulness (§4). **No separate benchmark framework is created.**

## §8. Graceful degradation / known-unknown rule (reuse existing semantics)

P9-QS **prohibits**: silent generic-LLM fallback where a governed technical capability is unavailable; fabricated deterministic
results; treating missing evidence as evidence of safety; silently replacing a failed engineering tool with an unverified AI
estimate; falsely marking a requirement validated after a tool failure. Reuse existing gap / readiness / validation / safety
semantics (`engine/controlled_unknown_progression.py`, `engine/derived_readiness.py`, `engine/validation_plan.py` blocked items,
safety validation-required). The contract registers the FUTURE requirement for explicit semantics equivalent to *unsupported
capability / unable to determine / additional evidence required / deterministic calculation required / specialist review
required*, but **invents no runtime status in this governance-only gate**.

## §9. Versioning / historical truth / backward compatibility (reuse existing owners — NO new framework)

Technical results MUST retain enough identity to preserve historical meaning, via existing owners: Domain-Pack `version` /
`schema_version` + provenance manifest (§5-I1); `scoring_version`; the engine contract/version identity captured by
`engine/session_reconstruction.py`. **Principles (binding):** historical outputs retain their **producing-version identity**; a
new Domain-Pack version MUST NOT silently reinterpret old outputs; version mismatch remains **fail-closed** where the existing
architecture requires it; migration MUST be **explicitly governed** — **no silent migration**. **No new general versioning
framework is created.**

## §10. Domain lifecycle / deactivation / retirement (reuse existing lifecycle vs activation separation)

Preserve the separation between **registry lifecycle status** (`engine/domain_registry.py`: `registered` / `deprecated`;
`deprecation_status`: `active` / `deprecated` / `sunset` — lifecycle ONLY, D-S5-03) and **runtime activation status**
(`engine/domain_activation.py` §5-I2). Principles: future analysis may be **disabled** (removed from the §5-I2 activation
allowlist) **without deleting historical user data**; deactivation does not erase prior evidence/results; `deprecated`/`sunset`
does not rewrite historical meaning; rollback/retirement require **governed operational handling** (a future operational gate).
**No new lifecycle statuses are invented.**

## §11. Extensibility / Nth-domain rule

A future Nth specialist domain MUST normally be addable through: a **Domain Pack**; domain-owned rules/content/questions;
capability metadata (§4); tests; benchmark/qualification evidence — **without adding recurring domain-specific `if/elif` branches
to shared core**. P9-QS **prohibits** introducing domain-specific shared-core coupling merely to add another specialist domain,
unless a **separately reviewed one-time extension seam** is proven necessary (e.g. the already-registered Path-N caller
propagation obligation, §16).

## §12. Units & Dimensional Integrity — PLACEHOLDER ONLY (deferred)

No shared unit/dimension runtime owner exists today; **none is created here.** P9-QS registers only the FUTURE technical-quality
rule that **before deterministic engineering calculations or numerical prototype/specification recommendations are authorized**,
relevant engineering quantities MUST carry sufficient semantics conceptually equivalent to **`value + unit + quantity/dimension
identity + provenance + assumption/source`**, where technically applicable. **Actual runtime implementation remains DEFERRED** to
the future deterministic-calculation adapter gate (§13). This clause depends on **no** CAP identifier.

## §13. Future deterministic-calculation adapter gate — REFERENCE ONLY (deferred; unnumbered)

P9-QS does **not** implement any deterministic-calculation capability, and assigns it **no CAP identifier** (the repository has no
canonical CAP number for it; `CAP-06` is reserved for the *Multi-Axis Invention Readiness Dashboard* and MUST NOT be reused).
Referred to descriptively as the **future deterministic-calculation adapter gate**: if separately authorized later, engineering
calculations MUST use bounded **deterministic adapters** on the existing integration/adapter architecture
(`engine/export_adapter.py` P7-I3; the provider-port pattern); act as **evidence producers**; carry provenance, version identity,
and relevant unit/dimension semantics (§12); support reproducibility where technically possible; expose explicit
**success/failure/no-result** behavior; **fail without corrupting canonical state**; and **never silently become an AI estimate**.
It remains a **separate future capability/gate**; assigning it a canonical CAP identifier (if ever) is a separate Owner decision.

## §14. Prototype / manufacturing preservation — REFERENCE ONLY (do NOT duplicate)

P9-QS does **not** build or duplicate **CAP-12 (Prototype Materials & Manufacturing Recommendation)**, **CAP-13 (Component
Thickness / Specification / Safety Advisory)**, **WS-PFV-001**, or any prototype/manufacturing engine. It preserves only the
architectural seam **`Domain knowledge → Canonical structured state → Shared CAP-12 / CAP-13 / Prototype capability`**. A future
Domain-Pack contract may expose structured technical facts needed by shared future capabilities, but Phase 9 MUST NOT create
per-domain prototype engines. **CAP-12, CAP-13, and WS-PFV remain SEPARATE and each require their own authorization.**

## §15. Domain Composition / D4 (reference; NOT executed)

**Multi-domain recognition ≠ multi-domain activated analysis.** §5-I3 (`engine/subsystem_model.py`) governs multi-domain
recognition as subsystem **metadata** (referencing a domain never activates it). Actual multi-domain composition is the already-
registered **D4 — Cross-Domain / Multi-Disciplinary Engineering Integration** gate (requires ≥2 activated domains). P9-QS does
**not** execute D4; it records that **D4 is required before multi-domain activated composition** and MUST preserve: domain
ownership of findings; provenance; **no silent overwrite** of one domain's technical truth by another; and **no hidden
cross-domain priority**.

## §16. Mandatory separate execution gates — referenced, NOT implemented

The two obligations below are **registered by the merged D3 formal closure record** as "MANDATORY FUTURE PREREQUISITE — Path-N
caller propagation" and "MANDATORY FUTURE PREREQUISITE — multi-activated tie precedence." The short labels **"P9-PREREQ-A" /
"P9-PREREQ-B" are convenient P9-QS labels for those already-registered obligations, not pre-existing canonical identifiers**
(the D3 closure record uses the descriptive wording).

- **P9-PREREQ-A — Path-N production caller propagation.** Trigger: **BEFORE the first second / non-electronics specialist-domain
  activation** (thread canonical `domain` through `engine/progression_loop.py::get_question`/`get_display_question` →
  `get_path_n_question` and stall/reframe comparison, so a foreign-domain session cannot inherit Electronics-owned Path-N
  content). Mandatory; a separate execution gate. **NOT implemented here.**
- **P9-PREREQ-B — governed multi-activated-domain tie/conflict precedence.** Trigger: **BEFORE more than one specialist domain can
  be ACTIVATED** (replace the current deterministic-single-domain `sorted(activated_tied)[0]` with a governed policy; alphabetical
  ordering MUST never silently become product/architecture policy). Mandatory; a separate execution gate. **NOT implemented here.**

## §17. D8 boundary (Owner-reserved; NOT resolved)

`domains/iot_electronics/**` remains **Owner-reserved**. P9-QS does NOT resolve D8, activate IoT, normalize/migrate/reuse/delete
reserved IoT artifacts, or assume IoT is first. **D8 remains required before IoT activation only.**

## §18. Separately-governed deferred capabilities (accurate status — corrected B2)

The following remain **separately governed** and are **NOT authorized or implemented by Phase 9**, and Phase 9 MUST NOT silently
absorb, redefine, or re-home any of them:

- **Output-Language override capability:** **DEFERRED / NOT IMPLEMENTED / NOT AUTHORIZED / separately governed** (D-P6-17 is the
  accepted *decision*, not the capability). **It is NOT a repository-authoritative pre-new-domain activation prerequisite** and
  MUST NOT be stated as one. *(The repository-authoritative pre-new-domain prerequisite is the separate **Domain Registry
  validation hardening, D-P6-14 / §5-I1**, which is already CLOSED; P9-QS's qualification clauses consume it.)*
- STG (Structured Technical Guidance): reserved / inactive / separately authorized.
- QTA (Question Translation Assistant); ACV; PDF/download; email delivery: deferred / not authorized.

## §19. Domain neutrality (Mechanical/future only as examples)

P9-QS is **domain-neutral**. Mechanical (and robotics, renewable energy, manufacturing technologies, drones/unmanned systems,
unknown future specialties) may be cited only as **future architectural examples**. P9-QS does NOT select, authorize, or imply
any first domain, and writes no domain-specific runtime requirement into the shared standard.

## §20. Canonical-owner preservation (no duplication)

Reuse and preserve: `engine/domain_registry.py` (§5-I1); `engine/domain_activation.py` (§5-I2); §5-I3
`engine/subsystem_model.py`; evidence/provenance (`record_contract`/`record_store`/`idea_state`); decision/assumption
(`decision_workspace`); validation/requirements (`validation_plan`/`requirement_landscape`/`stage3_evaluator`); readiness
(`derived_readiness`); benchmark/scoring (`benchmark/run_benchmark_v1.py`/`scoring.py`); canonical outputs
(`deliverable_assembler`/`normalize_output`/`idea_development_outputs`); the integration/export adapter boundary
(`export_adapter`/`payment_provider_port`); session/version reconstruction (`session_reconstruction`); Path-N (`path_n_questions`);
safety-signal (`safety_signal`); and the existing knowledge/evidence-governance owners (§4b). **No replacement owner is invented.**

## §21. P9-QS acceptance criteria (this candidate)

1. governance-only diff; 2. no runtime/test/web/domain/schema/prompt implementation changes; 3. Phase 9 remains NOT AUTHORIZED /
INACTIVE; 4. no domain activated; 5. D8 unchanged; 6. P9-PREREQ-A preserved (as a label for the D3-registered Path-N-caller
obligation); 7. P9-PREREQ-B preserved (as a label for the D3-registered tie-precedence obligation); 8. D4 preserved / not
executed; 9. **the future deterministic-calculation capability remains separately DEFERRED and UNNUMBERED** unless repository
authority gives it an identifier (it is NOT `CAP-06`); 10. **Output-Language remains separately governed / DEFERRED / NOT
AUTHORIZED and is NOT silently absorbed by Phase 9, and is NOT asserted to be a pre-new-domain prerequisite**; 11. Units runtime
remains deferred (placeholder); 12. CAP-12 / CAP-13 / WS-PFV remain separate; 13. no new global Engine/Registry/Ledger created;
14. Domain Capability Contract defined as an extension of existing Domain-Pack ownership (no new registry); 15. qualification
includes regression protection; 16. graceful-degradation principle preserved; 17. version/history/backward-compat principle
preserved; 18. lifecycle/deactivation preserves historical user data; 19. extensibility / no-recurring-core-branch principle
preserved; 20. canonical owners preserved (incl. the §4b knowledge/evidence-governance reuse reference); 21. **`CAP-06` appears
only with its repository-canonical meaning (Multi-Axis Invention Readiness Dashboard), if at all**; 22. audit/addendum/sweep are
referenced as review/development inputs, not committed repository authority; 23. no Phase-10 authorization; 24. PSRR remains
mandatory / NOT executed; 25. deployment/production remains unauthorized; 26. OD-M honest-reject / no-silent-redirect behavior
for unsupported domains is preserved; 27. `OWNER_DECISION_REGISTER.md` UNCHANGED unless repository precedent requires recording
this contract-creation authorization.

## §22. Proposed Phase-9 gate sequence (analytical; nothing authorized/registered as active)

- **Before P9-QS contract creation:** the audit + addendum + sweep review inputs — complete.
- **Before the first Phase-9 activation contract:** P9-QS accepted; a domain's capability declaration (§4) + qualification with
  regression (§6/§7); the **D-P6-14 / §5-I1** Domain-Registry-hardening pre-new-domain prerequisite (already CLOSED) consumed.
- **Before the first non-electronics activation:** **P9-PREREQ-A**.
- **Before the multi-activated state:** **P9-PREREQ-B**.
- **Before multi-domain composition:** **D4**.
- **Before a deterministic-calculation capability:** the future deterministic-calculation adapter gate (§13) + Units/Dimensional
  integrity (§12) + failure-isolation.
- **Domain-specific / future capability:** per-domain safety cues & validation; **D8** before IoT; CAP-12/CAP-13/WS-PFV; STG;
  Output-Language (separately governed).
- Governance-readiness, implementation-readiness, activation-readiness, and production-readiness are **distinct** and not
  collapsed.

## §23. Contract status & boundary

**P9-QS is a CONTRACT CANDIDATE — it becomes AUTHORITATIVE only if this exact accepted candidate is merged (create-a-merge-commit)
and post-merge verified.** It authorizes no Phase-9 start, domain activation, IoT, D8 resolution, D4, deterministic-calculation
capability, units runtime, CAP-12/CAP-13/WS-PFV, STG, Output-Language, calculation adapters, Phase 10, PSRR, deployment, or
production. **Phase 9 remains NOT AUTHORIZED / INACTIVE.** The rejected prior candidate `6a3e25d` is superseded by this corrected
candidate. Candidate only until independent review → Owner acceptance → merge → post-merge verification. Append-only; prior
history not rewritten.
