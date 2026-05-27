# ADR — Product Decision Contract
Date: 2026-05-19
Status: DRAFT — pending review before engine extraction

---

## 1. Internal Evaluator Signals (engine layer — never exposed to user)

feasibility_signal:
  APPEARS_FEASIBLE
  APPEARS_FEASIBLE_WITH_CAVEATS
  FEASIBILITY_UNCLEAR
  SIGNIFICANT_CONCERNS_IDENTIFIED
  INSUFFICIENT_INPUT

confidence_level:
  LOW     — input is sparse or vague
  MEDIUM  — input covers main aspects
  HIGH    — input is detailed and specific

missing_information.items[].severity:
  CRITICAL   — blocks analysis
  IMPORTANT  — significantly limits analysis
  HELPFUL    — would improve analysis

identified_concerns.items[].severity:
  MINOR
  NOTABLE
  SIGNIFICANT

---

## 2. Product Decision States (API layer — exposed to frontend)

PASS:
  trigger: feasibility_signal IN [APPEARS_FEASIBLE, APPEARS_FEASIBLE_WITH_CAVEATS]
           AND confidence_level IN [MEDIUM, HIGH]
           AND no CRITICAL missing_information
           AND no SIGNIFICANT identified_concerns
  meaning: idea is technically feasible with current information

WARN:
  trigger: feasibility_signal == APPEARS_FEASIBLE_WITH_CAVEATS
           OR confidence_level == LOW
           OR IMPORTANT missing_information exists
           OR NOTABLE identified_concerns exist
  meaning: idea shows promise but requires clarification before investment

BLOCK:
  trigger: feasibility_signal IN [SIGNIFICANT_CONCERNS_IDENTIFIED,
                                  FEASIBILITY_UNCLEAR,
                                  INSUFFICIENT_INPUT]
           OR CRITICAL missing_information exists
           OR SIGNIFICANT identified_concerns exist
  meaning: critical feasibility gaps detected before investment

Priority: BLOCK > WARN > PASS
(if any BLOCK condition is true, result is BLOCK regardless of other signals)

---

## 3. UX Translation Layer

PASS:
  headline_ar:  "فكرتك قابلة للتطبيق من الناحية التقنية"
  subtext_ar:   "بناءً على المعلومات المقدمة، لا توجد عوائق تقنية حرجة."
  color:        green
  icon:         check

WARN:
  headline_ar:  "فكرتك واعدة — لكن تحتاج بعض التوضيحات"
  subtext_ar:   "يمكن المضي قدماً بعد معالجة النقاط التالية."
  color:        amber
  icon:         info

BLOCK:
  headline_ar:  "تم اكتشاف فجوات حرجة تحتاج معالجة قبل الاستثمار"
  subtext_ar:   "هذا ليس رفضاً للفكرة — بل تحديد للمخاطر قبل البدء."
  color:        red
  icon:         warning

Internal signals (NEVER shown to user):
  feasibility_signal raw value
  schema_version
  domain
  analysis_language
  component_specificity

---

## 4. Recovery Protocol (WARN and BLOCK only)

Structure:
  main_reason:          string — one sentence, plain Arabic, max 100 chars
  top_recovery_actions: array — max 3 items, each actionable and specific
  re_evaluate_prompt:   string — call to action after user updates idea

Source mapping:
  main_reason          ← feasibility.signal_basis_ar (summarized)
  top_recovery_actions ← missing_information.items (CRITICAL first, then IMPORTANT)
                         + identified_concerns.items (SIGNIFICANT first)
                         max 3 total, prioritized by severity
  re_evaluate_prompt   ← static: "بعد تحديث فكرتك، أعد التقييم للحصول على نتيجة أدق"

Re-evaluate loop:
  User updates intake fields → resubmit → new evaluation cycle
  Previous snapshot_id stored for comparison (future feature)
  No human review required in current phase

---

## 5. API Output Contract (normalize layer output)

{
  "decision": "PASS | WARN | BLOCK",
  "headline_ar": "string",
  "subtext_ar": "string",
  "main_reason": "string | null",
  "top_recovery_actions": ["string"] | [],
  "re_evaluate_prompt": "string | null",
  "analysis_confidence": "LOW | MEDIUM | HIGH"  // renamed: reflects input completeness, not idea quality,
  "snapshot_id": "uuid"
}

analysis_confidence UX note:
  Never show raw LOW/MEDIUM/HIGH to user.
  LOW  → "نحتاج معلومات إضافية لتحسين دقة التقييم"
  HIGH → shown only implicitly via result confidence

analysis_confidence UX note:
  Never show raw LOW/MEDIUM/HIGH to user.
  LOW  → "نحتاج معلومات إضافية لتحسين دقة التقييم"
  HIGH → shown only implicitly via result confidence

Internal fields (stored, not returned to frontend):
  raw_analysis (full schema output)
  feasibility_signal
  all schema fields

---


---

## Deterministic Decision Policy

The LLM never directly determines PASS/WARN/BLOCK.

The model produces internal evaluator signals only:
  - feasibility_signal
  - confidence_level (internal name, mapped to analysis_confidence in API)
  - missing_information.items[].severity
  - identified_concerns.items[].severity

Product decision state is computed deterministically
inside compute_decision.py using explicit mapping rules.

Mapping is:
  IF any CRITICAL missing_information OR SIGNIFICANT identified_concerns
     OR feasibility_signal IN [SIGNIFICANT_CONCERNS_IDENTIFIED, FEASIBILITY_UNCLEAR, INSUFFICIENT_INPUT]
  → BLOCK

  ELIF feasibility_signal == APPEARS_FEASIBLE_WITH_CAVEATS
     OR confidence_level == LOW
     OR any IMPORTANT missing_information
     OR any NOTABLE identified_concerns
  → WARN

  ELSE → PASS

Priority: BLOCK > WARN > PASS
First matching rule wins.

This policy is version-controlled and auditable independently from the prompt.

---


---

## Deterministic Decision Policy

The LLM never directly determines PASS/WARN/BLOCK.
The model produces internal evaluator signals only.
Product decision is computed deterministically in compute_decision.py.

DECISION_CONTRACT_VERSION = "v1"

Mapping (priority: BLOCK > WARN > PASS, first match wins):

  BLOCK if:
    feasibility_signal IN [SIGNIFICANT_CONCERNS_IDENTIFIED, FEASIBILITY_UNCLEAR, INSUFFICIENT_INPUT]
    OR any missing_information.severity == CRITICAL
    OR any identified_concerns.severity == SIGNIFICANT

  WARN if:
    feasibility_signal == APPEARS_FEASIBLE_WITH_CAVEATS
    OR confidence_level == LOW
    OR any missing_information.severity == IMPORTANT
    OR any identified_concerns.severity == NOTABLE

  PASS otherwise

Extraction invariants:
  - benchmark score must not change after extraction
  - normalize_output must be idempotent
  - compute_decision must be pure: no HTTP, no Anthropic, no filesystem, no env vars
  - raw_text + extracted_json + normalized_output stored separately
  - internal enums never leaked to frontend

---

## Reopen Trigger
Revise contract if:
- contradiction_detection becomes product-critical
- new domain added beyond IOT_ELECTRONICS
- user research reveals translation mismatch

