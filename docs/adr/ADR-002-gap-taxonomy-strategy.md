# ADR-002: Gap Taxonomy Strategy

**Status:** Accepted
**Date:** 2026-05-27
**Author:** InventorAI Architecture Review
**Depends on:** ADR-001
**Applies to:** domains/*/domain.json, engine/domain_rules.py, engine/domain_registry.py

---

## 1. Context

The current engine evaluates every invention against three gaps defined in engine/domain_rules.py and mirrored in domains/iot_electronics/domain.json:

- MECHANISM_COMPLETENESS
- PHYSICAL_FEASIBILITY
- BOUNDARY_AMBIGUITY

This gap set was designed for IoT and embedded electronics inventions. It is the only gap set in the system. No taxonomy governance exists. Gap identifiers are plain strings with no schema, no universality designation, no domain prefix, and no uniqueness enforcement across future domain packs.

As the platform approaches multi-domain capability, two risks emerge. First, the current three gaps are insufficient to evaluate inventions outside electronics — a software or biomedical invention evaluated against this model receives an incomplete or misleading result. Second, adding domain packs without gap taxonomy governance creates identifier collision risk and makes cross-domain gap management unenforceable.

This ADR defines which gaps are universal, which are domain-specific, what taxonomy changes are mandatory before a second domain pack is introduced, and what is deferred.

---

## 2. Decision

**Universal gaps are formally designated.** MECHANISM_COMPLETENESS and BOUNDARY_AMBIGUITY are universal. They apply to every invention in every domain. PHYSICAL_FEASIBILITY is domain-class-specific — it applies to physical inventions but requires reframing for software.

**Gap schema must be extended before a second domain pack is committed.** Each gap entry in domain.json must carry id, label, and universal fields. Plain string gap lists are not sufficient for multi-domain operation.

**Gap identifier uniqueness must be enforced by the registry validator before a second domain pack is loaded.** The validator must reject a domain pack whose gap identifiers collide with any already-loaded domain.

**Domain-specific gap additions are approved in principle but not yet implemented.** The gap sets defined in Section 5 of this ADR are the approved taxonomy for each named domain class. No domain pack may introduce gaps outside its approved taxonomy without a taxonomy amendment.

**Gap severity weighting, cross-domain gap reuse registry, and prompt-level domain framing are deferred.** These are enhancements, not prerequisites.

---

## 3. Universal vs Domain-Specific Gaps

### Universal (apply to all domains)

**MECHANISM_COMPLETENESS**
Every invention must demonstrate that its core operating mechanism is sufficiently described and internally consistent. The evidence standard differs by domain but the gap concept is domain-agnostic.

**BOUNDARY_AMBIGUITY**
Every invention must define what it is and what it is not. Claim boundary clarity is a prerequisite for any meaningful evaluation regardless of domain.

### Domain-class-specific

**PHYSICAL_FEASIBILITY**
Applies directly to all physical inventions. For software inventions, must be reframed as COMPUTATIONAL_FEASIBILITY. The identifier must not be reused across domain classes with different meanings — this constitutes a silent semantic collision.

---

## 4. Domain Evaluability Assessment

### Software inventions against current model
Partial. MECHANISM_COMPLETENESS and BOUNDARY_AMBIGUITY apply. PHYSICAL_FEASIBILITY produces a false positive — software has no physical constraints, so the gap closes trivially, giving the inventor unwarranted confidence. Critical gaps entirely absent: ALGORITHMIC_CORRECTNESS, PRIOR_ART_DISTINGUISHABILITY, PLATFORM_DEPENDENCY. Result: incomplete evaluation, not surfaced to inventor.

### Biomedical inventions against current model
Inadequate. MECHANISM_COMPLETENESS applies but requires clinical and biological evidence framing absent from current question generation. PHYSICAL_FEASIBILITY applies only in a weakened form. BOUNDARY_AMBIGUITY applies. Critical gaps entirely absent: CLINICAL_EVIDENCE_BASIS, REGULATORY_PATHWAY, BIOCOMPATIBILITY. A biomedical invention that closes all three current gaps remains unassessed on its most critical dimensions. The evaluation result would be misleading.

---

## 5. Approved Gap Taxonomy by Domain Class

### Software
- MECHANISM_COMPLETENESS (universal)
- BOUNDARY_AMBIGUITY (universal)
- COMPUTATIONAL_FEASIBILITY (replaces PHYSICAL_FEASIBILITY)
- ALGORITHMIC_CORRECTNESS
- PRIOR_ART_DISTINGUISHABILITY
- PLATFORM_DEPENDENCY
- Optional: DATA_PRIVACY_COMPLIANCE (for data-handling inventions)

### Electronics / IoT (current)
- MECHANISM_COMPLETENESS (universal)
- BOUNDARY_AMBIGUITY (universal)
- PHYSICAL_FEASIBILITY
- Future additions: SIGNAL_INTEGRITY, POWER_BUDGET, REGULATORY_CERTIFICATION

### PCB
- MECHANISM_COMPLETENESS (universal)
- BOUNDARY_AMBIGUITY (universal)
- PHYSICAL_FEASIBILITY
- MANUFACTURING_TOLERANCES
- THERMAL_MANAGEMENT
- DFM_COMPLIANCE
- COMPONENT_AVAILABILITY

### Solar Energy
- MECHANISM_COMPLETENESS (universal)
- BOUNDARY_AMBIGUITY (universal)
- PHYSICAL_FEASIBILITY
- EFFICIENCY_CLAIM_SUPPORT
- ENVIRONMENTAL_DEGRADATION
- GRID_INTEGRATION_FEASIBILITY
- MATERIALS_SCARCITY (for novel material inventions)

### Medical Devices
- MECHANISM_COMPLETENESS (universal)
- BOUNDARY_AMBIGUITY (universal)
- BIOCOMPATIBILITY (replaces PHYSICAL_FEASIBILITY for implantable/in-contact devices)
- CLINICAL_EVIDENCE_BASIS
- REGULATORY_PATHWAY (mandatory, not optional)
- HUMAN_FACTORS_VALIDATION
- STERILITY_AND_PACKAGING (for implantable or sterile devices)

---

## 6. Mandatory Changes Before a Second Domain Pack Exists

These must be completed and committed before any second domain.json is created:

**1. Gap schema extension.**
domain.json gap entries must change from plain strings to objects:
  - id: string, globally unique gap identifier
  - label: human-readable name
  - universal: boolean

The registry validator must be updated to enforce this schema. domains/iot_electronics/domain.json must be migrated to the new schema. This is a breaking change to the current domain.json format and requires a registry validator update, a domain.json migration, and a new test suite run confirming 123+ tests still pass.

**2. Gap identifier uniqueness enforcement.**
load_registry() must check for identifier collisions across all loaded domain packs and raise RegistryLoadError on collision. This must be implemented in engine/domain_registry.py before any second domain pack is loaded in any environment.

**3. Universal gap formal designation.**
MECHANISM_COMPLETENESS and BOUNDARY_AMBIGUITY must be marked universal: true in the updated domain.json schema. The engine must be capable of distinguishing universal gaps from domain-specific gaps, even if it does not yet treat them differently in progression logic.

**4. evaluate_transition() generalisation.**
If progression currently checks for closure of named gap identifiers (MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, BOUNDARY_AMBIGUITY by name), it must be generalised to check closure of all session-scoped gaps before a second domain is deployed. This requires separate approval per ADR-001 Section 5 and full benchmark verification.

---

## 7. Optional Changes (Deferred)

**Gap severity weighting.**
Domain packs may eventually declare gap priority or blocking status (e.g. REGULATORY_PATHWAY as a hard blocker for medical devices). Not required for correctness at MVP scale.

**Cross-domain gap reuse registry.**
A shared library of gap definitions that multiple packs reference by identifier. Reduces duplication. Optional until three or more domain packs exist.

**Domain-specific question framing in prompts.**
AI advisor question templates framed around domain context. Improves quality but does not affect gap correctness or progression determinism.

**Deprecation mechanism for gap identifier variants.**
If PHYSICAL_FEASIBILITY is eventually split by domain class, a deprecation and migration path is required. Deferred until multi-domain coexistence is active.

**Gap amendment process.**
A formal process for adding gaps to an existing domain pack post-deployment (versioning, migration of in-flight sessions). Deferred until the first production domain pack requires amendment.

---

## 8. Forbidden Changes

- Introducing a second domain pack without completing all items in Section 6
- Adding gap identifiers to any domain pack that collide with identifiers in any other domain pack
- Encoding gap closure thresholds, scoring weights, or progression rules inside domain.json gap entries
- Reusing a gap identifier across domain classes with different semantic meanings (e.g. PHYSICAL_FEASIBILITY in both electronics and software with different evidence standards)
- Removing MECHANISM_COMPLETENESS or BOUNDARY_AMBIGUITY from any domain pack
- Modifying gap lifecycle logic in assess_response(), integrate_response(), or evaluate_transition() without separate approval per ADR-001

---

## 9. Risks If Ignored

**If gap schema is not extended before second domain pack:**
Gap entries remain plain strings. The registry has no way to identify universal gaps, enforce uniqueness, or carry metadata needed for domain-aware question generation. All downstream domain features must be retrofitted against an inadequate schema.

**If gap identifier uniqueness is not enforced:**
Two domain packs may define gaps with identical identifiers but different semantics. A cross-domain session would close a gap from domain A when domain B evidence is provided, silently producing incorrect progression decisions.

**If evaluate_transition() is not generalised before second domain deployment:**
Progression for non-electronics domains may trigger incorrectly if the transition check looks for MECHANISM_COMPLETENESS, PHYSICAL_FEASIBILITY, and BOUNDARY_AMBIGUITY by name. A solar energy invention with all solar gaps closed but PHYSICAL_FEASIBILITY absent from its domain pack would never trigger a maturity transition.

**If biomedical inventions are evaluated without domain-appropriate gaps:**
An inventor of a medical device receives a passing evaluation result missing REGULATORY_PATHWAY and CLINICAL_EVIDENCE_BASIS assessment. The platform produces a false confidence signal on an invention that may be clinically unsafe or commercially non-viable. This is a product liability risk, not merely a quality risk.

---

*This ADR depends on ADR-001. It may be superseded by a replacement ADR approved by the project owner. Section 8 forbidden changes apply immediately upon acceptance.*
