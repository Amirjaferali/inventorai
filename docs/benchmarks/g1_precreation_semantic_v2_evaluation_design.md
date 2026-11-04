# INVENTORAI — G1 semantic v2 candidate and independent evaluation preparation

**EXECUTION EFFICIENCY CORRECTION — BMG / PCRA / SFR / FCR / RE-SPE / IP-FIRST**  
**Status:** BOUNDED EVALUATION-PREPARATION CANDIDATE ONLY. **NOT A PROVIDER-RUN AUTHORIZATION.**

## Source and control

- Authoritative start: `feature/atomic-json-session-persistence` at `28f5d4f4d9e73c2a29229535e288e5f71c03916f`, following [PR #924](https://github.com/Amirjaferali/inventorai/pull/924).
- The one consumed G1 campaign is frozen under [PR #923](https://github.com/Amirjaferali/inventorai/pull/923): **NO_GO, 17/20**. P08, P10, P11 failed the composition threshold; K4/P12, K6 and G5 remain **NOT ASSESSED**. No reinterpretation, rerun, prompt change or scoring change applies to those files.
- Reuse `scripts/run_g1_precreation_semantic_eval.py` for canonical concept lists, schema, reference-free validation functions and offline evaluation patterns. Its original `_instructions`, pinned preregistration, rules, references and test cases stay unchanged.
- [Prior diagnostic case pack](../../tests/fixtures/g1_precreation_semantic_boundary_challenge_v1.json) (16 cases; PR #924) is **development-only, not an independent holdout**. Never present its performance as fresh qualification.

## Candidate change — narrow hypothesis, not truth

`scripts/g1_precreation_semantic_v2_candidate.py` constructs an evaluation-only prompt by replacing **exactly two identified spans** of the frozen v1 instruction string. It fails closed if an expected original span is absent or duplicated; it reuses the existing schema and `v1.governed_concepts()`. There is **no new interpretation engine**, scoring/validation owner, production route, persistence, request adapter or model invocation.

The two candidate hypotheses:

1. **Finished-assembly inclusion is not authorship.** A reused/previously bought circuit board, motor, sensor or module explicitly installed or functionally incorporated in the inventor's finished assembly may be listed as **a proposed stated included component**. This does not say the inventor invented, built, legally owns, tested, certified or verified that component. A laptop, tablet, bike/handlebar, third-party camera or shipping package that stays an external target, accessory or context is not included by mere proximity.
2. **Clarification depends on unresolved *composition*, not the existence of any question.** Unknown invention identity/function or unsettled assembly membership should lead to `CLARIFY_FIRST`. Questions about size/mounting on an otherwise clear integrated or single-domain assembly must not automatically flip the composition decision. When a referenced part is ambiguous, ask instead of silently assigning it.

These are **development hypotheses informed by the failed P08/P10/P11 examples**. They are not a validated fix, and must not be claimed to generalize from that same consumed data. Product Stage-15/intent/confirmation, ownership, provenance, domain activation and deterministic orchestration are unaffected.

## Independent held-out qualification — NOT BUILT OR RUN HERE

Before a new provider run, a **different non-authoring agent/session** must create and seal the next evaluation fixture and human reference, with explicit independent authorship identity. The author can use the documented acceptance *principles* but should **not** read this candidate prompt, tune against its outputs or reuse the G1 v1 twenty cases and post-hoc sixteen development cases. Cases and references must be independently scrutinized for semantic ambiguity *before* model calls; blind adjudication must be anchored in the same intended-assembly-vs-external distinction without leaking the candidate's wording to the test author.

Suggested **provisional** breadth: at least 24 synthetic English ideas with balanced intended-integrated versus external/no-integration outcomes and substantial genuinely ambiguous/clarify cases, plus controls for negation, shipping packaging, previously owned modules, reused parts, third-party equipment and generic goals. The author independently chooses the actual ideas and expert meaning labels; the Lead checks near-duplicates and leakage. **These are targets, not a frozen pack or a newly authorized campaign.**

The *final evaluation contract* must be pre-registered and frozen **before seeing any responses**, including: exact case count and category mix; independently settled `allowed_composition` and provenance-aware required/forbidden-part criteria; whether `CLARIFY_FIRST` is allowed for ambiguous assembly; an explicit false-integration critical rule; per-case parts, negations and unknowns; independent K4/K6/G5 human-assessment obligations; numerical minimums for composition, integration recall, stated-part grounding and negations; deterministic baseline comparison; permissible provider errors/abstentions; decision for incompleteness and NO_GO; exact pinned inputs/reference/instructions/schema/model/code/price manifest and cryptographic hashes. No threshold is adjusted after provider responses.

Important: **frozen v1 scores do not transfer** to a different case mix. Do not copy 18/20 or 23/25 blindly without denominators and independently justified thresholds. A green CLI or synthetic fixture test is not a model qualification.

## Runner and authority boundary

The current `scripts/run_g1_precreation_campaign.py` is **single-run**, bound to the consumed v1 pack/evidence, and calls `ev.load_pack()`. Its `G1_PRECREATION_CAMPAIGN_AUTHORIZED` flag is not an authorization for this candidate. Do not alter it to accept another pack, spoof a different HEAD, erase evidence, bypass a journal guard or send a paid smoke request. A separately authorized, bounded, **new** campaign (and any new runner support truly required for that campaign) must reuse its recording, budget, refusal, manifest and one-run protections, with a distinct case/manifest/evidence identity.

No real inventor content or product project data. No tool calls inside the model. Minimum required access and fixed hard cost/request caps; no loops or automatic retry. Human review is always explicit and cannot be inferred from successful output parsing.

A new provider run requires exact Owner authorization **after** the held-out test and manifest have been independently prepared and the actual budget and model access are known. Product AI remains **BLOCKED**. Do not merge, deploy or activate a product increment on this artifact's existence.

## Evidence, review and next decision

This preparation PR proves only that the candidate is *constructible and isolated*, with offline tests that guard unchanged v1 behavior and schema ownership. It does **not** prove the candidate is semantically better, nor that blind test data already exist.

- **SFR:** v1 canonical evaluator/validator/schema/domain owners = REUSE; narrow instruction candidate = EXTEND for offline evaluation only; separate independent holdout = NEXT TRIGGER; product engine = NO CHANGE.
- **FCR:** MEDIUM evaluation-preparation risk (with evidence-trust implications); focused tests plus required hosted CI, and one separate-session non-authoring review. If a future change affects Stage-15 product truth, question selection, persistence, architecture or security, escalate with existing ACE and reclassify.
- **NEXT-LOOP:** independent test authoring and reference adjudication are the next eligible tasks after this PR, **not automatically authorized** by it. Then the actual provider campaign is independently authorized against a new immutable digest. Preserve all BLOCKED/DEFER decisions and agreed G1 sequence.

Sources: [CLAUDE.md](../../CLAUDE.md), [Lean §9](../governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md), [frozen G1 scorer](../../scripts/run_g1_precreation_semantic_eval.py), [PR #924 semantics](g1_precreation_semantic_followup.md).
