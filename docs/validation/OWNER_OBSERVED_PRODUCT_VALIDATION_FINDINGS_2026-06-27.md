# OWNER-OBSERVED PRODUCT VALIDATION FINDINGS — 2026-06-27

## 1. Document status and authority

- Document type: Owner-observed product validation findings record (evidence preservation).
- Status: PRODUCT EVIDENCE — EFFECTIVE UPON COMMIT — NON-AUTHORIZING.
- Authority: records what was observed and what is provable from committed
  repository truth. It authorizes no code, test, scoring, progression, template,
  persistence, benchmark, final-technical-selection, or scope change. It does not
  amend any anchor.
- Authoritative base: committed repository at
  `91eff27f9342ee865a449ab8cd5127f2c57006be`
  (the PR #24 post-merge-closure true-merge of
  `origin/feature/atomic-json-session-persistence`; ordered parents
  `7dffea8333759f1e21f159ded51bf0e14c6e24ee` then
  `fed70067b6833d6e0dd4626836d2955642c60a0a`).
- Evidence precedence: **no screenshot or live observation alone overrides
  committed repository evidence.** Where an observation could not be reproduced
  from committed code, it is recorded as observational, not confirmed.

## 2. Session identity and evidence sources

- The live owner product-observation session and the generated FDC-001
  deliverable package were performed/dated **2026-06-27**, using the committed
  application launched (read-only) from the authoritative commit `91eff27…`.
- The governance review and finding classification recorded here were performed
  **2026-06-28**.
- The observed idea was a **hospital-power concept** run through the
  idea-development "session" workflow (`/start` → `/session/<sid>` →
  success-criteria → deliverable), which is distinct from the FDC-001/FDC-002
  bicycle braking-detection *decision-workspace* surface.
- Evidence sources used here are explicitly separated into four kinds:
  - **Direct owner-observed evidence** — what the owner saw/experienced in the UI.
  - **Exported-deliverable evidence** — fields/values in the generated FDC-001 package.
  - **Committed repository evidence** — exact committed code/templates/tests/docs.
  - **Interpretation** — analysis derived from the above, clearly labeled.

## 3. Direct owner experience

- The owner, a non-technical product owner, attempted to develop a hospital-power
  idea through the committed session workflow.
- The workflow asked for specialist engineering knowledge (e.g., voltage, current,
  frequency, electrical component selection, power architecture, protection
  behavior, generator/UPS/battery coordination).
- The owner could progress only because an external assistant supplied extensive
  technical answers. This is the central owner-experience observation: the
  workflow was **not completable by a non-specialist unaided.**
- The generated deliverable presented a confident closure posture (see §5, §8)
  that did not match the actual epistemic state of the idea.

## 4. Owner–expert boundary findings

- **Direct owner-observed evidence:** the session demanded specialist values the
  owner could not supply.
- **Committed repository evidence:** the engine classifies only evidence
  *quality* (`engine/idea_state.py`: `ASSERTED` / `REASONED` / `DEMONSTRATED`).
  There is **no** classification of questions/information as owner-answerable vs
  system-derivable vs expert-required vs evidence-required (`engine/enums.py`,
  `engine/idea_state.py`, `engine/progression_loop.py`). The session UI exposes a
  single free-text control (`web/templates/session.html`,
  `<textarea name="response">`) with no defer, provisional-assumption, or
  assign-to-specialist control. "I do not know" is only auto-detected
  (`engine/progression_loop.py` `_detect_acknowledged_unknown`, requires ≥ minimum
  length) and recording it does **not** resolve the gap.
  `docs/governance/NON_SPECIALIST_QUESTIONING_POLICY.md` is committed with status
  "COMMITTED GOVERNANCE POLICY — NOT IMPLEMENTED" and is not enforced in runtime
  code.
- **Conformance evidence:** committed governance
  `docs/governance/OWNER_PRODUCT_IDENTITY_CORRECTION.md §7` states the platform
  "must … defer questions the non-specialist cannot yet answer, or record the gap
  as an unknown. It must never demand engineering parameters the user cannot
  supply." The runtime contradicts this committed governance.
- **Classification:** `CONFIRMED PRODUCT DEFECT` (governance-to-runtime conformance)
  **and** `CONFIRMED PRODUCT CAPABILITY GAP` (no owner/system/expert/evidence
  responsibility model; no defer/assumption/expert-routing controls).

## 5. Gap/evidence truth findings

- **Exported-deliverable evidence:** the package reported `Gaps total/open/resolved:
  6/0/6`, `No unresolved items`, and `Verdict: PROCEED`, with rationale that all
  identified gaps were resolved — while simultaneously acknowledging no prototype,
  no demonstration, no technical validation, no expert review, no confirmed
  success criteria, and no compliance assessment.
- **Committed repository evidence:** gap closure
  (`engine/progression_loop.py`, ~lines 412–428) marks a gap `CLOSED` on a
  `DEMONSTRATED` response **or** a `REASONED` follow-up; `assess_response` returns
  `ASSERTED` on the `DEMONSTRATED` branch ("DEMONSTRATED requires external evidence
  — not in MVP"), so in practice gaps close on reasoned *text* alone. The
  deliverable computes `gaps_resolved = len(CLOSED)`
  (`engine/deliverable_assembler.py`, ~lines 137–139) and the PROCEED verdict from
  `_RECOMMENDATION_A` at maturity ≥ 2 with zero open gaps. There is **no**
  verified / assumed / expert-reviewed distinction in the closure path.
- **Conformance evidence:** contradicts committed governance
  `DUAL_PATH_PRODUCT_ANCHOR.md §2` and `OWNER_PRODUCT_IDENTITY_CORRECTION.md §7`
  ("must not falsely represent unsupported gaps as solved, resolved, or closed").
- **Classification:** `DOCUMENTATION/TRUTH DEFECT` **and** `CONFIRMED PRODUCT
  DEFECT` — the product collapses answered/described/assumed/reasoned into a single
  "resolved" state and reports a confident verdict not backed by verification.

## 6. Response-depth and closure-feedback findings

- **Direct owner-observed evidence:** the system repeatedly returned "partially
  addressed — needs more depth" and "asserted only — reasoning required," even
  after long, detailed responses.
- **Committed repository evidence:** `engine/progression_loop.py` `assess_response`
  (~lines 299–358) classifies a response `REASONED` only if it contains a
  causal-structure keyword pattern **and** meets a minimum length
  (`MIN_REASONED_RESPONSE_LENGTH = 40`) **and** is not a generic-verb trap. A gap
  can therefore close on a 40+ character answer that contains causal keywords,
  with no verification. The status strings are generic and do **not** identify the
  exact missing reasoning; the richer per-evidence-item analysis in
  `engine/stage3_evaluator.py` is separated and does not drive progression or UI
  feedback.
- **Interpretation:** closure is a keyword+length proxy, not verification; it is
  **not** length alone (causal wording is also required).
- **Classification:** `CONFIRMED PRODUCT DEFECT` (proxy-based closure; generic,
  non-specific missing-reasoning feedback).

## 7. Visible idea-development value findings

- **Exported-deliverable / committed repository evidence:** the deliverable
  largely restates owner-entered text. In `engine/deliverable_assembler.py`:
  alternative architectures, explicit decisions, trade-off analysis, atomic
  requirements, and expert assignments are **ABSENT**; platform inferences and
  recommendations are **PARTIAL** (provenance selection + a static
  `_RECOMMENDATION_A` lookup); ranked risks and a concrete next action are
  **IMPLEMENTED** (risks are generated dynamically; next action is generic and
  templated). The optional AI advisor is disabled
  (`engine/ai_advisor.py: AI_ADVISORY_ENABLED = False`).
- **Interpretation:** the product is, by current MVP design, a deterministic
  elicitation/assembly workflow rather than a generative one. Most intended
  value-adding outputs are not produced.
- **Classification:** `CONFIRMED PRODUCT CAPABILITY GAP`.

## 8. Deliverable findings

Inspected against committed `engine/deliverable_assembler.py`,
`web/templates/deliverable.html`, and tests. The owner's observations are recorded
honestly, including where committed code does **not** confirm an observation.

| # | Owner/exported observation | Classification | Committed evidence note |
|---|---|---|---|
| E2 | long copied source text presented as requirements | `CONFIRMED PRODUCT DEFECT` | REQ-001/REQ-002 = full owner text (`_s4`) |
| E3 | non-atomic requirements | `CONFIRMED PRODUCT DEFECT` | requirement = whole compound statement |
| E4 | large repetition of owner answers | `CONFIRMED PRODUCT DEFECT` | full verbatim across §2/§4/§9/§10/§11 |
| E8 | "Owner-defined criterion required" placeholder | `CONFIRMED PRODUCT DEFECT` | literal `_OWNER_CRITERION_REQUIRED` |
| E10 | no comparison of architectural alternatives | `CONFIRMED PRODUCT CAPABILITY GAP` | Categories B/C DEFERRED (no options DB) |
| E7 | generic prototype/test-plan text | `OBSERVATIONAL FINDING — REQUIRES MORE EVIDENCE` (partial) | template structure is static; experiment basis is evidence-grounded |
| E11 | no clear owner-vs-platform distinction | `OBSERVATIONAL FINDING — REQUIRES MORE EVIDENCE` (partial) | provenance exists in data (`basis`/quality) but is **not** sufficiently visible in the rendered deliverable |
| E12 | over-broad PROCEED verdict | `CONFIRMED PRODUCT DEFECT` (via §5) | verdict conditional but binary; inflated by "resolved" semantics |
| E1 | apparent truncation in Known Problem / REQ-001 | `NOT CONFIRMED` in `deliverable_assembler`; `OBSERVATIONAL FINDING — REQUIRES MORE EVIDENCE` | no truncation in the deliverable path; `engine/summary.py` truncates to 200 chars in a *separate* summary view |
| E6 | single low risk despite life-critical concept | `OBSERVATIONAL FINDING — REQUIRES MORE EVIDENCE`; confirmed underlying gap = `CONFIRMED PRODUCT CAPABILITY GAP` | risk count/severity are **dynamic**, not a hard-coded single low risk; the confirmed gap is **lack of domain/safety criticality awareness** |
| E9 | no concrete prioritized experiment | `NOT CONFIRMED` in engine; `OBSERVATIONAL FINDING — REQUIRES MORE EVIDENCE` | `_s11` generates concrete, prioritized, de-duplicated experiments; observed genericness is input-dependent |
| E5 | weak synthesis | `OBSERVATIONAL FINDING — REQUIRES MORE EVIDENCE` | synthesis intentionally disabled in MVP; maps to §7 capability gap |

**Explicit non-overstatement (per the accepted readiness assessment):**
- Deliverable truncation is **observational and not confirmed** in
  `deliverable_assembler`.
- A single **hard-coded** low risk is **not confirmed**; the confirmed gap is the
  lack of domain/safety criticality awareness.
- "No concrete prioritized experiment" is **not confirmed** in the engine; the
  observed generic output remains observational/input-dependent.
- Owner-versus-platform provenance exists **partially in data** but is **not
  sufficiently visible** in the rendered deliverable.

## 9. Hospital-power domain-specific expert gaps

The hospital-power example surfaced potential specialist concerns: candidate
medical/electrical standards; jurisdiction and adopted edition; emergency
transfer-time classification; dynamic load-shedding policy; industrial-control
cybersecurity; medical-location isolated-power / medical IT systems; insulation
monitoring; clinical load prioritization.

- These are **domain-specific specialist gaps**, separated here from generic
  product defects.
- **Committed repository evidence:** the runtime engine has **no generic mechanism**
  that, given an idea, identifies potentially applicable standards, jurisdiction
  uncertainty, the required specialist, the evidence needed, or compliance status.
  It has only disclaimers (`engine/deliverable_assembler.py`, e.g. "not
  engineering certification, regulatory approval, or legal advice") and an
  expertise-gap keyword detector (`engine/stage3_evaluator.py`: "consult /
  specialist / expert / beyond my knowledge"). A comprehensive mechanism exists
  only as **governance contracts** (`SUPPORTED_TECHNOLOGY_AND_SOURCE_OF_TRUTH_CONTRACT.md`,
  `DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md §6`, `PATH_N_ORCHESTRATION_AND_HANDOFF_CONTRACT.md §4`),
  **not implemented at runtime.**
- The specific standards must **not** be treated as globally mandatory; the
  platform correctly does not assert IEC, NFPA, or any specific standard as
  universally required, and any future mechanism must preserve that honesty.
- **Classification:** `DOMAIN-SPECIFIC EXPERT GAP` (the specific standards) **and**
  `CONFIRMED PRODUCT CAPABILITY GAP` (the generic standards/jurisdiction/specialist
  mechanism is contracted in governance but absent from runtime).

## 10. Confirmed versus observational finding matrix

| Finding | Classification |
|---|---|
| A. Owner–expert question boundary | `CONFIRMED PRODUCT DEFECT` + `CONFIRMED PRODUCT CAPABILITY GAP` |
| B. Gap/evidence closure honesty | `DOCUMENTATION/TRUTH DEFECT` + `CONFIRMED PRODUCT DEFECT` |
| C. Response-depth / closure feedback | `CONFIRMED PRODUCT DEFECT` |
| D. Visible idea-development value | `CONFIRMED PRODUCT CAPABILITY GAP` |
| E. Deliverable (E2/E3/E4/E8 confirmed; E10/E6-gap capability; E12 via B) | mixed — see §8 |
| E1/E5/E7/E9/E11 | `OBSERVATIONAL FINDING — REQUIRES MORE EVIDENCE` / partial |
| E6 "single hard-coded low risk" | `NOT CONFIRMED` (gap = criticality awareness) |
| F. Hospital-power specialist concerns | `DOMAIN-SPECIFIC EXPERT GAP` + `CONFIRMED PRODUCT CAPABILITY GAP` |

## 11. Product impact

- A non-technical owner cannot today complete an idea session unaided without
  inventing specialist values (Finding A) — this blocks the intended
  non-specialist use.
- The deliverable can present a confident, closed, PROCEED posture that overstates
  the true epistemic state (Findings B, E12) — an honesty risk.
- The output adds limited visible idea-development value beyond restatement
  (Finding D) — a product-value risk.
- For high-criticality domains (e.g., hospital power) the platform neither
  surfaces required specialists/standards nor reflects criticality in risk
  (Findings F, E6) — though it correctly avoids asserting specific standards as
  mandatory.

## 12. Required corrective direction

The corrective direction (to be designed and authorized separately, not here) is to
make the product conform to its already-committed governance: a non-specialist-safe
owner–expert question boundary; truthful, distinct gap/evidence states that never
equate owner text/length with verification; visibly value-adding (but
identity-preserving) idea-development outputs; atomic requirements and
criticality-aware risk; concrete validation planning; and a redesigned deliverable
that distinguishes owner content from platform-added analysis. The detailed,
dependency-ordered program is recorded in the non-authorizing companion
`docs/governance/INVENTORAI_PRODUCT_VALUE_CORRECTION_PLAN.md`.

## Principal conclusion

The current product is **functional as a structured deterministic elicitation and
assembly workflow**, but it **does not yet consistently provide the intended
non-specialist-safe, evidence-honest, visibly value-adding idea-development
experience required by committed governance.**

## 13. Explicit non-authorization boundary

This record authorizes nothing. It does not change code, tests, scoring,
progression logic, templates, persistence, or configuration; it does not amend any
anchor, identity correction, strategic vision, scope-freeze, policy, ADR, or
architecture roadmap; it does not run a benchmark, make a final technical
selection, or move any closed/held/blocked/deferred/paused/unauthorized state.
Persistence remains PRESERVE UNMODIFIED AND PAUSE; benchmark remains NOT RUN; final
technical selection remains NONE. Any implementation requires separate, explicit,
repository-grounded owner authorization for that exact scope.
