# ADR-003: Evidence Quality Model

**Status:** Accepted
**Date:** 2026-05-27
**Author:** InventorAI Architecture Review
**Depends on:** ADR-001, ADR-002
**Applies to:** engine/progression_loop.py (assess_response, integrate_response, evaluate_transition), engine/domain_rules.py, domains/*/domain.json

---

## 1. Context

The InventorAI engine classifies every inventor response into one of three quality levels: ASSERTED, REASONED, or DEMONSTRATED. These levels determine gap status transitions and maturity progression. They are the evidence standard of the platform.

Investigation of assess_response() (lines 162-195 of engine/progression_loop.py) revealed that the current implementation does not correctly discriminate between these levels. Specifically:

- A single domain vocabulary token in any response returns REASONED regardless of length, structure, or meaning.
- The length gate (len(r) < 20) is unreachable when any substance token is present, because the substance check fires first.
- The weak token filter (five words) is bypassed by any substance token, meaning vague responses containing one technical term return REASONED.
- DEMONSTRATED is permanently disabled in the MVP.
- known_problem has no quality floor in evaluate_transition(), while known_mechanism requires REASONED minimum.

These are not implementation bugs. They reflect an underspecified evidence standard. This ADR establishes the formal definitions as the authoritative governance standard before any code change is made.

---

## 2. Decision

The three quality levels are formally defined by this ADR. Any implementation of assess_response() must conform to these definitions. Any deviation is a defect, not a design choice.

The definitions are domain-independent at the structural level. What constitutes grounding differs by domain, but the structural criteria apply universally.

DEMONSTRATED is not permanently disabled. It is deferred for the MVP but must be implementable in a future release without changing the quality level schema.

The quality level of known_problem must match known_mechanism in evaluate_transition(). Both require REASONED minimum for maturity transition. This is a governance rule.

---

## 3. Formal Definitions

### ASSERTED

Definition: The inventor has made a claim without providing reasoning, mechanism, or technical grounding that would allow a domain expert to evaluate it. The response states a position but provides no basis for that position.

Structural signature:
- Claim present, basis absent
- Or: no claim at all (empty, filler, deflection)
- Or: vocabulary present but no causal or mechanistic relationship described

Boundary condition: The presence of a technical term does not elevate a response to REASONED. Technical terms are evidence of domain familiarity, not evidence of reasoning. "sensor" is ASSERTED. "the sensor detects X by measuring Y" is REASONED.

Gap effect: ASSERTED on an OPEN gap -> PARTIAL. ASSERTED on a PARTIAL gap -> PARTIAL (no change). ASSERTED never closes a gap.

### REASONED

Definition: The inventor has provided a technically grounded response that a domain expert could evaluate, challenge, or build upon. The response describes not just what the invention does but how, with sufficient specificity that the mechanism is traceable.

Structural signature:
- Claim present AND basis present
- Basis must include at least one of: named mechanism, named component with function, physical principle with application, architectural decision with rationale
- Response must be of sufficient length and density to contain a claim-basis pair
- Technical terms must appear in a causal or descriptive relationship, not as isolated tokens

Boundary condition: "microcontroller" alone is ASSERTED. "the microcontroller reads the sensor and transmits the result" is REASONED. The minimum unit of REASONED evidence is: component/principle + what it does + in what context.

Gap effect: REASONED on an OPEN gap -> PARTIAL. REASONED on a PARTIAL gap -> CLOSED. REASONED is the minimum quality required for gap closure and for maturity transition.

### DEMONSTRATED

Definition: The inventor has provided externally verifiable evidence that the claimed behavior exists or has been observed. The evidence is not reasoning about what should happen but documentation of what did happen.

Structural signature:
- Measurement: quantified result with conditions and reference
- Citation: published or registered external document with identifier (DOI, FCC ID, ISO number)
- Test result: structured outcome with sample size, duration, and pass/fail criterion
- Regulatory or certification evidence: named body, named standard, outcome

Boundary condition: Claiming tests were performed is ASSERTED. Describing protocol without results is REASONED. Providing quantified results with conditions is DEMONSTRATED.

Gap effect: DEMONSTRATED on any gap status -> CLOSED immediately.

Current implementation status: Disabled in MVP. assess_response() always returns ASSERTED as final fallback. The quality level must not be removed from the schema.

---

## 4. Evidence Required for Each Level

### ASSERTED — evidence requirements

None beyond response presence. ASSERTED is the floor, not a quality target.

The following are always ASSERTED regardless of length or vocabulary:
- Responses containing only technical labels without relational context
- Responses where vague language tokens outnumber specific technical tokens
- Responses shorter than the minimum threshold for a claim-basis pair
- Responses that deflect, restate the question, or express uncertainty without technical content

### REASONED — evidence requirements

All of the following must be present:

Requirement 1 — Minimum content length. The response must be long enough to contain a claim-basis pair. A single token or phrase cannot constitute a claim and its basis simultaneously. The minimum is defined by the presence of a subject, a predicate, and a qualifying phrase — not by character count.

Requirement 2 — Specific technical content. The response must contain at least one Tier 1 specific technical term: a named component, named protocol, named physical principle, or named architectural element. Generic vocabulary (data, signal, output, process) does not satisfy this requirement alone.

Requirement 3 — Relational structure. The technical term must appear in a relationship that conveys mechanism or function. "the sensor" is a label. "the sensor measures X" is a relationship. "the sensor measures X by detecting Y" is a mechanism description.

Requirement 4 — Vague language not dominant. If vague or hedge tokens outnumber specific technical tokens, the response is ASSERTED regardless of any specific technical content present.

### DEMONSTRATED — evidence requirements

At least one of the following must be present:
- A quantified measurement result with stated conditions and reference or tolerance
- An external document identifier that can be independently verified (DOI, FCC ID, ISO standard number, patent number, certification body reference)
- A structured test result with sample size, duration, and stated outcome against a defined criterion
- A regulatory filing or certification reference with named authority and outcome

Self-reported claims that sound precise but cannot be verified ("our internal tests show 99% accuracy") are REASONED, not DEMONSTRATED.

---

## 5. Canonical Examples by Level

### ASSERTED examples

| Response | Reason |
|---|---|
| "It works using advanced technology." | No mechanism. Weak token (technology). No substance. |
| "The system detects and solves the problem." | Circular. No technical content. |
| "sensor" | Single label. No relational structure. No claim-basis pair. |
| "it processes data" | Generic Tier 2 token only. No mechanism. |
| "it somehow uses a sensor to detect things" | Vague tokens (somehow, things) outnumber specific tokens (sensor). Weak dominant. |
| "voltage and current are used" | Generic Tier 2 tokens. No mechanism described. |
| "we tested it and it worked" | Claimed test without result, condition, or criterion. |
| "it's basically a wireless device" | No Tier 1 token. No mechanism. |

### REASONED examples

| Response | Reason |
|---|---|
| "A Hall effect sensor detects shaft rotation by measuring magnetic field polarity change, outputting one pulse per revolution." | Named principle, named mechanism, defined output. |
| "The ESP32 reads temperature from DS18B20 via OneWire at 500ms intervals and publishes over MQTT." | Named components, named protocols, named timing. |
| "The piezoelectric transducer converts pipe wall vibration to electrical signal, amplified before ADC conversion at 10kHz." | Named transduction principle, signal chain, sampling rate. |
| "BLE beacon transmits at 100ms intervals; RSSI averaged over 10 readings before distance calculation via path loss model." | Named protocol, timing, signal processing method, physical model. |
| "The comparator circuit switches at 1.2V threshold, latching the output until the reset pin is pulled low." | Named circuit type, named threshold, named state, named reset condition. |

### DEMONSTRATED examples

| Response | Reason |
|---|---|
| "Bench testing at 25 degrees C: plus-or-minus 0.5 degrees accuracy across 50 samples vs NIST-calibrated reference." | Quantified result, stated conditions, external reference standard. |
| "FCC ID: 2ABCDE-XYZ01 — RF module certified under Part 15, emissions confirmed within limits." | External identifier, named authority, stated standard, outcome. |
| "DOI: 10.1109/JSEN.2021.3085432 confirms 3% accuracy at 30cm depth for this sensor design." | External citation identifier, quantified claim, specific design reference. |
| "72-hour endurance test: 1,200 actuations, zero mechanical failures, power consumption within 5% of spec." | Duration, sample count, outcome, quantified tolerance. |
| "ISO 13485:2016 certification obtained from BSI Group (certificate MD12345) for the manufacturing process." | Named standard, named body, named certificate identifier, outcome. |

---

## 6. Evidence Standards Across All Domains

The following standards apply in every domain without exception:

Universal Standard 1 — Claim-basis pair requirement for REASONED.
Every REASONED response must contain both a claim (what the invention does or is) and a basis (how or why it does it). This is domain-independent.

Universal Standard 2 — Specific over generic vocabulary.
Domain vocabulary tokens divide into Tier 1 (specific: component names, protocol names, physical principles, named mechanisms) and Tier 2 (generic: data, signal, output, input, process, control, system). Tier 2 tokens alone do not satisfy REASONED in any domain.

Universal Standard 3 — Vague language dominance rule.
If vague hedge tokens outnumber Tier 1 specific tokens in a response, the response is ASSERTED regardless of domain. Starting universal vague token set: {somehow, something, technology, stuff, things, basically, simply, just, kind of, sort of, some kind, maybe, probably, I think, not sure}.

Universal Standard 4 — External reference requirement for DEMONSTRATED.
DEMONSTRATED requires an externally verifiable reference: an identifier, a measurement with conditions and reference, or a named regulatory body with outcome. Self-report without external anchor is REASONED at best.

Universal Standard 5 — Quality asymmetry is forbidden.
known_problem and known_mechanism must have identical quality floors in evaluate_transition(). Both must be REASONED minimum. Setting a lower quality floor for known_problem than for known_mechanism violates this standard.

---

## 7. Domain-Specific Evidence Standards

The following standards vary by domain and must be specified in each domain pack when domain-specific evaluation is activated.

### Electronics / IoT
- Tier 1 tokens: component names (specific ICs, sensors, MCU families), protocol names (MQTT, I2C, SPI, BLE, Zigbee), physical principles (piezoelectric, Hall effect, capacitive sensing)
- DEMONSTRATED markers: measured values with units and tolerances, FCC/CE certification references, power consumption figures with load conditions
- REASONED minimum: named component + named function + named interface or output

### Software
- Tier 1 tokens: algorithm names, data structure names, language/runtime names, API names, named design patterns
- DEMONSTRATED markers: benchmark results with hardware and dataset specified, published paper citations with DOI, reproducible test suite references
- REASONED minimum: named algorithm or approach + what problem it solves + what its output or guarantee is

### Medical Devices
- Tier 1 tokens: named biological mechanism, named anatomical target, named clinical endpoint, named regulatory class
- DEMONSTRATED markers: clinical trial registration numbers (ClinicalTrials.gov ID), peer-reviewed citations, FDA 510(k) or PMA numbers, ISO 13485 certification references
- REASONED minimum: named mechanism of action + named target tissue or system + named measurable clinical outcome
- Additional constraint: biocompatibility claims require material names and ISO 10993 reference to reach DEMONSTRATED

### PCB
- Tier 1 tokens: named component values with tolerances, named layer stackup, named manufacturing process (reflow, wave, press-fit)
- DEMONSTRATED markers: Gerber file reference, DFM report, IPC standard compliance reference, test coverage percentage with named standard
- REASONED minimum: named component + function in circuit + named interface signal

### Solar Energy
- Tier 1 tokens: named cell technology (monocrystalline, perovskite, CdTe), named efficiency metric (PCE, Jsc, Voc), named degradation mechanism
- DEMONSTRATED markers: IEC 61215 or IEC 61646 test results, certified efficiency under STC with named test lab, published journal citations with DOI
- REASONED minimum: named cell technology + named operating principle + named efficiency claim with physical basis

---

## 8. How Quality Should Influence Gap Closure

### Current model (as implemented)

ASSERTED  + OPEN gap    -> PARTIAL
ASSERTED  + PARTIAL gap -> PARTIAL (no change)
REASONED  + OPEN gap    -> PARTIAL
REASONED  + PARTIAL gap -> CLOSED
DEMONSTRATED + any gap  -> CLOSED (disabled in MVP)

### Governance rules

Rule 1 — ASSERTED never closes a gap. Correctly implemented. No change required.

Rule 2 — REASONED requires two iterations to close an OPEN gap. First REASONED: OPEN -> PARTIAL. Second REASONED: PARTIAL -> CLOSED. This two-step path is intentional. Collapsing it to one step would lower the evidence bar. No change required.

Rule 3 — DEMONSTRATED closes immediately. Correctly specified in integrate_response(). Blocked by assess_response() never returning DEMONSTRATED. The rule is correct; the implementation has a known gap. When DEMONSTRATED is re-enabled, no change to integrate_response() is required.

Rule 4 — Quality floors for transition must be symmetric. evaluate_transition() currently requires known_mechanism.quality != ASSERTED but checks known_problem is not None only. Required change: add known_problem.quality == ASSERTED as a blocking condition. This is a protected function change requiring separate owner approval.

Rule 5 — Gap closure is permanent. Once a gap reaches CLOSED it cannot be reopened. Correctly implemented. No change required.

Rule 6 — Quality accumulates within a gap, not across gaps. REASONED on gap A does not improve gap B. Correctly implemented. No change required.

### Proposed addition — quality decay warning (future, not current)

If a gap is PARTIAL and the inventor's next response is ASSERTED, the engine should issue a WARN with a reframe prompt rather than leaving the gap silently in PARTIAL. This is an enhancement, not a correction, and requires separate approval.

---

## 9. Forbidden Behaviors

- Any implementation of assess_response() that returns REASONED for a response containing only Tier 2 generic tokens violates this ADR.
- Any implementation that returns REASONED for a response shorter than a claim-basis pair violates this ADR.
- Any implementation that allows vague-dominant responses to return REASONED violates this ADR.
- Removing DEMONSTRATED from the quality level schema violates this ADR.
- Setting a lower quality floor for known_problem than for known_mechanism in evaluate_transition() violates this ADR.
- Allowing any domain pack to define its own gap closure rules violates this ADR. Gap closure rules are universal and defined here only.

---

## 10. Implementation Guidance (Pre-Code)

Before any code change to assess_response() is written:

1. The full set of adversarial examples in Section 5 must be converted to unit tests and run against the current implementation to establish baseline failure counts.
2. The proposed revised evaluation model must be validated against all REASONED examples in Section 5 — all must still return REASONED after the fix.
3. The Tier 1 / Tier 2 vocabulary split must be applied to _SUBSTANCE_SIGNALS and reviewed for completeness before encoding in source.
4. The length threshold (in words, not characters) must be calibrated so that "Hall effect sensor detects rotation" (5 words, legitimate short REASONED) passes and "sensor" (1 word, ASSERTED) fails.
5. A separate benchmark replay suite covering gap response evaluation end-to-end must be created before the fix is committed. The existing benchmark tests the extraction pipeline only.
6. All changes to assess_response(), integrate_response(), and evaluate_transition() require explicit owner approval per ADR-001 Section 5.

---

*This ADR supersedes no prior decision record on evidence quality. It may be superseded by a replacement ADR approved by the project owner. Section 9 forbidden behaviors apply immediately upon acceptance.*

---

## Step 6 Implementation Note — Anti-Triviality Guard Only

Date: 2026-05-27

### What was changed
A minimum length threshold (`len(r) >= 40`) was added to `assess_response()`
before returning `REASONED` when a substance token is detected.

### What this is NOT
This threshold does NOT validate reasoning quality.
It does NOT confirm claim + basis + relationship structure.
It is a minimum anti-triviality guard only.

Purpose: prevent trivially short token-triggered promotion to REASONED.

### Known false-negative risk
Concise but legitimate technical explanations (e.g. "Hall sensor detects rotation via magnetic flux")
may be classified as ASSERTED despite containing genuine reasoning structure.
This is an accepted limitation of the current vocabulary-based approach.
Resolution: future structure-based reasoning model (not approved for implementation).

### Governance boundary
Step 6 is approved as: stabilization fix only.
Not approved as: semantic reasoning validation.
Not approved as: Tier system, domain vocabulary, or AI classification.
