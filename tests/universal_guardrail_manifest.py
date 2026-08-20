"""InventorAI Universal Core Guardrail inventory (P10-UG1).

File-creation contract:
  Path: tests/universal_guardrail_manifest.py
  Purpose: the single machine-checkable inventory of universal core guards.
    Each guard binds a durable, repository-authoritative invariant to its
    CANONICAL, ALREADY-EXISTING tests (composition by node-id reference —
    never duplication). Consumed by `scripts/run_universal_smoke.py` (the
    canonical smoke runner) and enforced by
    `tests/test_p10_ug1_universal_guardrail_framework.py` (which pins this
    inventory inside the governed full suite — the self-protection layer).
  Input contract: none at import time (pure data; no I/O, no network).
  Output contract: `GUARDS` — a list of dicts with the fields
    guard_id / owner / invariant / blocking / blocking_condition /
    canonical_tests / rationale / introduced_by.
  Prohibited behaviors: no test logic here (data only); no node outside the
    governed `tests/` suite; removing or downgrading a blocking guard is a
    governed framework change (it fails the pinned framework test) — never a
    routine edit.

Semantics:
  blocking=True  -> a failing/missing/skipped canonical test = SMOKE BLOCK.
  blocking=False -> a failing canonical test = reported OBSERVATION only
                    (a MISSING canonical test still BLOCKs — inventory
                    integrity is always blocking).

Extension process (governed; see
docs/governance/INVENTORAI_UNIVERSAL_CORE_GUARDRAIL_SMOKE_STANDARD.md):
append a new guard entry with all fields, introduced_by = the authorizing
gate, and update the pinned inventory in the framework test in the SAME
candidate. This framework is not a naming exercise: a guard exists only if
its canonical test exists and runs.
"""

GUARDS = [
    {
        "guard_id": "UG-CORE-01",
        "owner": "engine/progression_loop.py + engine/session_reconstruction.py",
        "invariant": ("Core progression is deterministic: replaying the same "
                      "accepted inputs reproduces the same review state "
                      "(maturity, stage, gaps, next question)."),
        "blocking": True,
        "blocking_condition": "live-vs-replay parity test fails",
        "canonical_tests": [
            "tests/test_p4_2_session_reconstruction.py::test_reconstruction_matches_live_path",
        ],
        "rationale": "InventorAI remains a deterministic Idea Maturity Engine, not a generic chatbot.",
        "introduced_by": "P4-2 Level-1 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-02",
        "owner": "engine/domain_rules.py (classify_domain canonical entry)",
        "invariant": ("Domain classification keeps governed word-boundary "
                      "semantics (no substring false positives) and the single "
                      "canonical classifier entry."),
        "blocking": True,
        "blocking_condition": "classifier false-positive or canonical-entry test fails",
        "canonical_tests": [
            "tests/test_cf5_f003_classifier_matching_semantics.py::test_red_controlled_not_electronics",
            "tests/test_cf5_f003_classifier_matching_semantics.py::test_red_hearth_not_medical",
            "tests/test_architecture_guardrails.py::TestGuardrails_Sec9_ClassifierReconciliation",
        ],
        "rationale": "Misclassification corrupts admission, labeling, and progression downstream.",
        "introduced_by": "CF5-F003 / GUARDRAILS §9 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-03",
        "owner": "web/app.py /start + engine/domain_activation.py",
        "invariant": ("Mechanical remains really activated and admittable "
                      "end-to-end via the REAL consent-first /start chain "
                      "through the truthful Tier-1 render (no doubles)."),
        "blocking": True,
        "blocking_condition": "real activation precondition or E2E chain test fails",
        "canonical_tests": [
            "tests/test_p10_dbt1_phase9_debt_remediation.py::test_real_activation_state_is_the_chain_precondition",
            "tests/test_p10_dbt1_phase9_debt_remediation.py::test_real_mechanical_admission_to_tier1_render_e2e_chain",
        ],
        "rationale": "Protects the activated-domain product surface and consent-first admission.",
        "introduced_by": "P10-DBT1 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-04",
        "owner": "engine/domain_activation.py",
        "invariant": "Electronics/Electrical remains really activated in production state.",
        "blocking": True,
        "blocking_condition": "real activation baseline pin fails",
        "canonical_tests": [
            "tests/test_cf5_f002_web_admission_multidomain.py::test_baseline_real_activation_unchanged",
        ],
        "rationale": "The original activated domain must not silently deactivate or drift.",
        "introduced_by": "CF5-F002 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-05",
        "owner": "engine core (domain-agnostic seams)",
        "invariant": ("Engine seams stay domain-neutral: no forced-electronics "
                      "context, no hardcoded domain coupling in the core."),
        "blocking": True,
        "blocking_condition": "neutrality or domain-agnostic-engine test fails",
        "canonical_tests": [
            "tests/test_d3_core_domain_neutrality.py::test_d3a_non_electronics_domain_context_not_forced_electronics",
            "tests/test_d3_core_domain_neutrality.py::test_d3b_seam_honors_non_electronics_domain_identity",
            "tests/test_architecture_guardrails.py::TestGuardrails_Sec1_DomainAgnosticEngine",
        ],
        "rationale": "Future domains must plug in without core rewrites; neutrality is architecture.",
        "introduced_by": "D3 / ARCHITECTURE_GUARDRAILS §1 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-06",
        "owner": "engine/idea_state.py",
        "invariant": "IdeaState progression fields remain stable (FSM/state integrity).",
        "blocking": True,
        "blocking_condition": "IdeaState field-stability guardrail fails",
        "canonical_tests": [
            "tests/test_architecture_guardrails.py::TestGuardrails_Sec4_IdeaStateFieldStability",
        ],
        "rationale": "Silent state-shape drift breaks persistence, replay, and progression at once.",
        "introduced_by": "ARCHITECTURE_GUARDRAILS §4 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-07",
        "owner": "web/app.py submit_answer + engine/record_store.py",
        "invariant": ("Accepted answers persist durably (persist-before-"
                      "acknowledge), survive a real restart, and a forged "
                      "post-restart submission fails closed with no second "
                      "durable event."),
        "blocking": True,
        "blocking_condition": "restart-durability / fail-closed test fails",
        "canonical_tests": [
            "tests/test_p4_1b2a_durable_answer_append.py::test_obs_b_restart_durability_new_context",
        ],
        "rationale": "No accidental state loss; durable truth is the product's memory.",
        "introduced_by": "P4-1b-2a (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-08",
        "owner": "web/app.py show_session cold-load + engine/session_reconstruction.py",
        "invariant": ("Reconstructed cold views are READ-ONLY: rendering writes "
                      "nothing durable, `state.domain` stays absent, and "
                      "writable resume stays deactivated."),
        "blocking": True,
        "blocking_condition": "read-only render or non-resume guard test fails",
        "canonical_tests": [
            "tests/test_p10_pc1_reconstructed_review_ui.py::test_cold_render_makes_no_durable_write",
            "tests/test_p10_pc1_reconstructed_review_ui.py::test_non_resume_guard_untouched",
        ],
        "rationale": "Accidental writable-resume activation is a governed-boundary violation.",
        "introduced_by": "P10-PC1 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-09",
        "owner": "web/app.py _project_authorized + engine/account_store.py",
        "invariant": ("Project/account ownership boundaries hold: non-owner, "
                      "anonymous, and sid-possession access to owned projects "
                      "is denied."),
        "blocking": True,
        "blocking_condition": "any ownership-denial test fails",
        "canonical_tests": [
            "tests/test_p5_3_project_ownership_authorization.py::test_non_owner_denied_on_real_owned_project",
            "tests/test_p5_3_project_ownership_authorization.py::test_anonymous_denied_on_owned_project_all_verbs",
            "tests/test_p5_3_project_ownership_authorization.py::test_sid_possession_is_not_ownership",
        ],
        "rationale": "Cross-user access is the highest-severity product breach class.",
        "introduced_by": "P5-3 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-10",
        "owner": "engine/decision_workspace.py + engine/deliverable_assembler.py",
        "invariant": "The FDC-001 deliverable envelope stays deterministic and contract-complete.",
        "blocking": True,
        "blocking_condition": "FDC-001 envelope contract test fails",
        "canonical_tests": [
            "tests/test_fdc001_contract.py::TestFDC001_Envelope",
        ],
        "rationale": "Decision Workspace output semantics are governed product truth.",
        "introduced_by": "FDC-001 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-11",
        "owner": "web/domain_label.py (single central resolver)",
        "invariant": ("EN/AR Tier-1 public labels stay truthful and bilingual; "
                      "unknown domains fall back to the general label and NEVER "
                      "to electronics; raw pack ids never become public labels."),
        "blocking": True,
        "blocking_condition": "any Tier-1 resolver truth test fails",
        "canonical_tests": [
            "tests/test_p6_1_truthful_domain_labeling.py::test_resolver_maps_runtime_domain_to_tier1_bilingual",
            "tests/test_p6_1_truthful_domain_labeling.py::test_resolver_maps_mechanical_to_tier1_bilingual",
            "tests/test_p6_1_truthful_domain_labeling.py::test_resolver_falls_back_to_general_never_electronics",
        ],
        "rationale": "Public language truth (EN/AR) is an owner-decided product boundary.",
        "introduced_by": "P6-1 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-12",
        "owner": "engine/export_adapter.py (canonical output -> integration layer)",
        "invariant": ("Canonical export stays deterministic/ordered and the "
                      "mandatory preservation floor survives adaptation — the "
                      "Core -> Canonical Output Model -> Integration/Export "
                      "architecture stays vendor-neutral."),
        "blocking": True,
        "blocking_condition": "export determinism or preservation-floor test fails",
        "canonical_tests": [
            "tests/test_p7_i3_export_adapter.py::test_transform_is_deterministic_and_ordered",
            "tests/test_p7_i3_export_adapter.py::test_mandatory_preservation_floor_survives",
        ],
        "rationale": "No vendor coupling may silently enter the core output architecture.",
        "introduced_by": "P7-I3 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-13",
        "owner": "web/app.py (_apply_security_headers, MAX_CONTENT_LENGTH, _free_text_error)",
        "invariant": ("Authoritative security headers and transport/input "
                      "limits remain in force (no silent disappearance of a "
                      "merged guard)."),
        "blocking": True,
        "blocking_condition": "security-header or input-limit preservation test fails",
        "canonical_tests": [
            "tests/test_p10_sec1_security_headers.py::test_html_landing_page_hardened",
            "tests/test_p10_sec1_security_headers.py::test_json_health_response_hardened",
            "tests/test_p10_sec2_input_hardening.py::test_idea_over_limit_rejected_explicitly_no_truncation",
            "tests/test_p10_sec2_input_hardening.py::test_answer_over_limit_rejected_no_mutation",
        ],
        "rationale": "No known guard may be disabled merely to make new functionality work.",
        "introduced_by": "P10-SEC1/SEC2 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-14",
        "owner": "engine/ai_advisor.py + engine/entitlement_service.py + engine/plan_catalog.py",
        "invariant": ("No implicit paid activation: the AI transfer path stays "
                      "hardcoded-disabled, and entitlement resolution fails "
                      "closed on unknown plans (structural AI boundary intact)."),
        "blocking": True,
        "blocking_condition": "AI-dormancy, entitlement fail-closed, or AI-boundary test fails",
        "canonical_tests": [
            "tests/test_p10_doc1_retention_cost_truth.py::test_cost_plan_matches_source_truth",
            "tests/test_p8_i1_plan_entitlement_foundation.py::test_unknown_plan_reference_fails_closed",
            "tests/test_architecture_guardrails.py::TestGuardrails_Sec6_AIBoundaryStructural",
        ],
        "rationale": "Paid activation is BLOCKED by D-P8-PL-01 class C until separately authorized.",
        "introduced_by": "P8 / P10-DOC1 / GUARDRAILS §6 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-CORE-15",
        "owner": "engine/domain_activation.py (governed allowlist)",
        "invariant": ("No unauthorized domain activation: the real support-state "
                      "policy (activated / recognized-not-activated / unknown) "
                      "holds and aliases cannot bypass activation."),
        "blocking": True,
        "blocking_condition": "real registry support-state policy test fails",
        "canonical_tests": [
            "tests/test_s5_i2_domain_activation.py::TestRealRegistrySupportState",
        ],
        "rationale": "Domain activation requires explicit owner authorization — always.",
        "introduced_by": "S5-I2 (composed by P10-UG1)",
    },
    {
        "guard_id": "UG-META-01",
        "owner": "tests/test_p10_ug1_universal_guardrail_framework.py",
        "invariant": ("The guardrail framework protects itself: the pinned "
                      "blocking inventory is intact and every canonical guard "
                      "test remains collectable."),
        "blocking": True,
        "blocking_condition": "framework inventory pin or collectability test fails",
        "canonical_tests": [
            "tests/test_p10_ug1_universal_guardrail_framework.py::test_core_blocking_inventory_pinned",
            "tests/test_p10_ug1_universal_guardrail_framework.py::test_all_canonical_tests_collectable",
        ],
        "rationale": "A guardrail that can be silently deleted is not a guardrail.",
        "introduced_by": "P10-UG1",
    },
    {
        "guard_id": "UG-OBS-01",
        "owner": "scripts/run_cli.py (startup banner)",
        "invariant": ("The CLI banner names the real activated domains "
                      "truthfully (user-facing copy, not a core invariant)."),
        "blocking": False,
        "blocking_condition": ("never blocks: a wording drift is reported as an "
                               "OBSERVATION for gate-specific review"),
        "canonical_tests": [
            "tests/test_p10_dbt1_phase9_debt_remediation.py::test_real_cli_banner_names_both_activated_domains",
        ],
        "rationale": "Truthful copy matters but must not be inflated into a core BLOCK.",
        "introduced_by": "P10-DBT1 (composed by P10-UG1)",
    },
]
