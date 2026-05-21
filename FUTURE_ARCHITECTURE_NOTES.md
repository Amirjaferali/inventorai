# InventorAI — Future Architecture Notes

This document captures architectural recommendations and product concepts
that are NOT required for current phases but must be considered before
the platform scales to multiple domains and real users.

---

## 1. Domain Capability Profile

### Problem This Solves

As InventorAI grows beyond electronics and mechanical domains, users must
know what the platform CAN and CANNOT evaluate BEFORE investing significant
effort in the progression workflow.

Presenting idea completeness as a percentage is subjective and potentially
misleading. Platform capability coverage is measurable and transparent.

### Key Principle

Do NOT say: "Your idea is 65% complete."
Instead say: "InventorAI currently supports approximately 65% of the
analysis capabilities for this domain."

### Proposed Structure

Each domain should expose a capability profile:

    DOMAIN_PROFILE = {
        "status": "beta",
        "coverage_percent": 65,
        "supported_capabilities": [
            "problem_definition",
            "mechanism_completeness",
            "boundary_analysis",
            "progression_guidance",
        ],
        "unsupported_capabilities": [
            "security_assessment",
            "compliance_review",
            "cost_modelling",
            "regulatory_mapping",
        ],
        "roadmap_notes": "Security and compliance planned for Phase H+",
    }

### Future User Experience (Pre-Journey Disclosure)

Before the progression journey begins, show the inventor:

    Detected Domain: Software
    Support Status: Beta
    Current Coverage: 65%

    Supported:
      + Problem Analysis
      + Mechanism Review
      + Risk Identification
      + Progression Guidance

    Not Yet Supported:
      - Security Architecture
      - Compliance Assessment
      - Cost Estimation

    Recommendation: You may continue, but results are limited to
    currently supported capabilities.

### Example JSON Profile

    {
      "domain": "software",
      "status": "beta",
      "coverage": 65,
      "supported": [
        "problem_definition",
        "user_identification",
        "workflow_analysis",
        "technical_architecture"
      ],
      "not_supported": [
        "security_assessment",
        "compliance_review",
        "cost_modelling"
      ]
    }

### Architectural Constraints

- Coverage values must NOT be hardcoded in the engine.
- Each domain owns its own profile metadata.
- The engine queries the profile; it does not define it.
- Profile disclosure happens BEFORE progression begins.
- Profile is advisory only — inventor may proceed regardless.

### When to Implement

Not required for Phase F-C or Phase F.
Recommended before: public launch, multi-domain beta, or Phase H (Web Interface).

---

## 2. Generic QUESTIONS Bank Relocation

Currently, the generic QUESTIONS bank lives inside progression_loop.py.
This is a known technical debt (see ARCHITECTURE_GUARDRAILS.md Section 10).

Future recommendation:
Move generic questions to a shared registry in domain_rules.py or a
dedicated questions_registry.py, so the engine contains zero question content.

This makes the engine a pure orchestrator with no content ownership.

When to implement: Phase G or before public launch.

---

## 3. Multi-Domain Idea Classification

Currently one idea maps to one domain.
Future ideas may span multiple domains simultaneously.

Examples:
    ["electronics", "ai"]       -- smart sensor with ML inference
    ["medical", "iot"]           -- remote patient monitoring device
    ["robotics", "software"]     -- autonomous navigation system

Architecture must support composable gap selection across domains
without restructuring the progression engine.

When to implement: Phase G+ or when first multi-domain idea is encountered.

---

## 4. Classifier Upgrade Path

Current domain inference is keyword-based (MVP-only).

Upgrade path:
    Phase F: keyword signals (current)
    Phase G: hybrid — keywords + LLM classification advisory
    Phase H: full ML or LLM classifier with confidence scoring

Interface must remain stable across all upgrades:
    def infer_domain(idea_text: str) -> str | None

---

Document owner: product + architecture
Review required before: public launch, Phase H start, multi-domain beta.
These are recommendations, not current requirements.
