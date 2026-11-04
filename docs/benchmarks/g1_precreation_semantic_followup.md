# INVENTORAI — G1 pre-creation semantic-boundary diagnosis (post-campaign 01)

**EXECUTION EFFICIENCY CORRECTION — BMG / PCRA / SFR / RE-SPE.**  
**Status: proposed evaluation semantics; no product or engineering-authority change.**

## Verified evidence and unchanged verdict

The frozen single-run campaign 01 (manifest `8e149e563ddf21857370beb6767b5975e29fcfb7fa205845e0406aaafcbf094d`) is archived unchanged after [PR #923](https://github.com/Amirjaferali/inventorai/pull/923), on authoritative merge `0879c258691db359bdac106febab667029d0178c`. It remains **NO_GO**: G1 17/20 versus the frozen >=18/20 threshold, missed P08, P10 and P11. K4/P12, K6/20 responses and G5/7 unknowns remain **NOT ASSESSED**. No rerun or reinterpretation can turn this consumed campaign into a GO.

The original frozen input, reference, prompt, `PREREGISTRATION_REVISION = 4`, validation/scoring rules, report and journal are *not changed* by this slice.

## Proposed semantic distinction to qualify (not an already-approved runtime rule)

**Assembly constituent (candidate):** A board, motor, sensor or other module the inventor already owns or acquired may be part of their *intended finished invention assembly* if the inventor explicitly describes installing, fastening, connecting or integrating it as part of that assembly. “Included in the intended assembly” does **not** mean the inventor designed/manufactured/owns all rights to that module; it establishes no engineering suitability, electrical/physical compatibility, tested capability, safety, or inventor-confirmed persisted truth.

**External context (candidate):** A stand holding a tablet, a case merely carrying a still-separate laptop, a bracket for a neighbor's camera, a handlebar onto which a device mounts, existing target equipment, packaging for shipping, inspiration and negated/hypothetical parts are **not** included constituents by proximity or mention alone. The inventor must explicitly say the target becomes part of the assembly to change this reading.

**Unresolved assembly membership:** If the inventor has not specified whether a sensor will be installed inside a shell or used next to it, the interpretation should request clarification rather than invent an electrical component or conclusively rule out integration. An underspecified goal with no identifiable artifact/function similarly needs `CLARIFY_FIRST`. A clearly single-domain artifact with unknown dimensions can still receive `NO_INTEGRATED_SUGGESTION`.

**Never apply “any question => CLARIFY_FIRST”.** A grounded integrated design can have questions about dimensions, mounting, materials or function while the integrated composition is already clear. Conversely, `NO_INTEGRATED_SUGGESTION` must not silently mean “nothing is missing”; it only expresses composition classification.

## Observed evidence and diagnosis

| Case | Model's actual response | Most defensible explanation |
| --- | --- | --- |
| P08 | Asked what would help with a stressful morning, recorded the unknown, but returned `NO_INTEGRATED_SUGGESTION` | The structured composition label did not reflect unresolved invention identity. Validator currently passes through well-formed non-integrated labels, without semantic consistency checking. |
| P10 | Listed the weatherproof housing and unknown board dimensions/mounting, but omitted the existing sensor board | The instruction excludes devices the invention “only holds or works with”; may conflict with the reference's intentional assembly membership. |
| P11 | Listed snap shell but omitted an existing electronics card meant to go inside | Same ambiguity: preexisting component versus mere external object. |
| P12 | Listed PCB and casing, treated the bike handlebar as external | Positive control: an inclusive rule cannot blindly admit everything physically nearby. |

These are **evidence-supported hypotheses**, not proof that a particular prompt edit will improve outcomes.

## Owner / architecture boundaries

- **REUSE:** Stage 15 `engine/subsystem_model.py` keeps canonical inventor-declared project/subsystem composition and the two relevant domain owners. Domain activation remains with `engine/domain_activation.py`. Current inventor confirmation / attribution / evidence ownership and the deterministic /start path remain unchanged.
- **REUSE WITHOUT EDITS:** campaign 01 frozen evaluation in `scripts/run_g1_precreation_semantic_eval.py`, archived journal and report, and all G1 v1 criteria.
- **EXTEND IN A FUTURE SEPARATELY AUTHORIZED EVALUATION ONLY:** candidate interpretation of installed old components versus external context and the decision semantics of genuine pre-composition uncertainty.
- **BLOCKED:** model production activation, new durable truth, change of Stage-15 participation / cross-owner semantics, or engineering compatibility conclusions. Escalate under the existing ACE procedure *only if* a subsequently proposed change materially crosses an owner/architecture boundary.
- **DO NOT CREATE:** another authority record, another interpretation engine, another roadmap, new domain taxonomy or a second independent analysis path.

## New diagnostic cases

`tests/fixtures/g1_precreation_semantic_boundary_challenge_v1.json` includes **16 newly authored synthetic-English counterfactuals** in eight pairs covering explicit inclusion, separate external objects, ambiguous assembly membership, vague goals, packaging versus permanent housing, reused modules and third-party devices. `tests/test_g1_precreation_semantic_boundary_challenge.py` checks integrity, canonical concepts, source terms and separation from the consumed G1 v1 pack.

**These are development cases, not genuinely independently held-out data**: the author knew the P08/P10/P11 failures. Passing their structural tests proves neither LLM comprehension nor semantic qualification.

The next *candidate* is to resolve the semantic-owner interpretation with the existing G1 intent/confirmation and Stage-15 owners; only afterward propose a revised evaluation prompt using existing code, with an independently authored held-out synthetic pack, predetermined acceptance thresholds, human K4/K6/G5 reviews, conservative budget bounds and explicit new Owner authorization. Do not retune to the archived outcomes, rerun the original campaign, use real inventor data or activate production AI. Arabic MSA, Kuwaiti/Gulf and Egyptian variants remain mandatory for later qualification, not covered by these English-only cases.

**NEXT-LOOP:** current authorized work ends with this bounded evaluation-design candidate and its PR. New provider execution, prompt modification, production product increment or merge requires its actual separate authority and risk checks.

Sources: [original report](evidence/g1_precreation_semantic_v1/campaign_01_report.json), [frozen scorer](../../scripts/run_g1_precreation_semantic_eval.py), [existing Lean protocol](../governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md), and [PR #923](https://github.com/Amirjaferali/inventorai/pull/923).
