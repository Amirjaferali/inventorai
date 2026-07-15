# D13 Gate 2 — Pre-Research Owner Decision

**Status:** OWNER DECISION — GATE 2 COMPLETE — NO RESEARCH AUTHORIZED —
GATE 3 NOT ISSUED

This owner-approved decision becomes canonical only when this docs-only
recording increment is merged into the authoritative branch. Gate 2
completion approves governance decisions and role requirements for the D13
Knowledge-Governance Research Contract
(`docs/governance/D13_KNOWLEDGE_GOVERNANCE_RESEARCH_CONTRACT.md`, §16 Gate 2).
It authorizes no research, appoints no person or organization, selects and
accesses no source, and does not issue Gate 3.

**Authoritative context:** authoritative branch
`feature/atomic-json-session-persistence`; authoritative tip
`730ba6b185df37dc84599f85d3c7990eb7eb6012`; the D13 Knowledge-Governance
Research Contract is CONTRACT / CANONICAL; D13 remains UNSATISFIED /
UNIMPLEMENTED; Workstream 8 remains NOT AUTHORIZED / NOT STARTED; official
product state DEMO_READY_WITH_LIMITATIONS; MVP scope electronics/electrical-only;
persistence FROZEN; AI Coach PROHIBITED / BLOCKED; Answer Clarification
INACTIVE.

---

## 1. Gate 2 classification

- **Gate 2:** OWNER-APPROVED / COMPLETE AS A PRE-RESEARCH DECISION PACKAGE.
- **Gate 3:** NOT ISSUED.
- **Research:** NOT AUTHORIZED.

Gate 2 completion approves the governance decisions and role requirements
below. Gate 2 completion does NOT appoint any person or organization. The
actual appointments of the executing agent, the qualified technical expert,
and the independent reviewer are MANDATORY GATE 3 EXECUTION PREREQUISITES —
NOT YET SATISFIED. They are not unresolved Gate 2 decisions; they are
execution prerequisites that must be named and verified inside the future
Gate 3 research authorization.

Gate 3 must:

- name the executing agent or accountable execution role;
- name the owner-approved qualified technical expert;
- name the independent reviewer;
- verify that the appointed expert and reviewer satisfy the Gate 2
  competency and independence requirements (§§10–11 below);
- incorporate this complete Gate 2 decision package by reference.

No research may begin without all three appointments and the complete Gate 3
authorization.

---

## 2. Selected concept class

Low-voltage, non-safety-critical, single-signal sensor-to-microcontroller
interfacing.

Permitted research comparison:

- analog voltage output;
- single-ended digital logic output;
- pulse or frequency output.

Excluded:

- I²C;
- SPI;
- UART;
- CAN;
- USB;
- other communication buses;
- differential signaling;
- wireless links;
- mains voltage;
- high-power systems;
- battery management;
- motor-drive power stages;
- medical, automotive, aerospace, or safety-critical applications;
- final circuit design;
- general embedded-system design.

No required-input checklist or engineering rule is created or approved by this
decision.

---

## 3. Bounded research objective

Determine whether D13 can, for one sensor output connected to one
microcontroller input within the class above, reliably identify: the
unresolved technical subproblem; why it matters; the missing information;
bounded research topics; the required evidence or test; what InventorAI cannot
verify; the supported specialist discipline; the required abstention
condition; and per-finding provenance.

Out of scope: product implementation; final schema design; live user guidance;
multi-signal or system design; power; patent-export work.

---

## 4. Research phases

- **Phase A — Repository and journey-data analysis.**
- **Phase B — Controlled source-based validation** within the approved source
  categories and external-access boundary.

Both phases remain unauthorized until Gate 3. No new owner authorization is
required between Phase A and Phase B if Gate 3 expressly authorizes both and
all source boundaries remain unchanged.

---

## 5. Source categories

**PERMITTED:**

- public manufacturer datasheets;
- public manufacturer application notes;
- public university or government technical references;
- owner-approved qualified-expert input.

**CONTEXT-ONLY:**

- publicly accessible summaries of recognized engineering standards.

**RESTRICTED — SEPARATE ACCESS CONFIRMATION:**

- full standards text requiring subscription, license, or controlled access.

**PROHIBITED:**

- forums;
- blogs;
- community answers;
- unrestricted web retrieval;
- commercial databases;
- vendor APIs;
- anonymous or unattributed technical content.

No actual source is selected or accessed by this decision. Every actual source
later used must be inventoried, versioned, cited, license-reviewed, and
provenance-linked.

---

## 6. Claim-specific authority model

Authority is claim-specific, not role-based:

- named-component electrical limits: manufacturer-controlled technical
  documentation is primary;
- normative engineering or safety requirements: the applicable recognized
  standard is primary;
- observed technical behavior: documented test evidence is primary;
- engineering interpretation and system application: qualified-expert review
  is required;
- AI-generated technical content: UNVERIFIED CANDIDATE only.

The qualified expert may interpret and adjudicate but must not silently
override manufacturer specifications, applicable standards, or documented test
results. Licensing and permitted use are assessed per source; no assumption is
made that manufacturer-document licensing is generally permissive.

---

## 7. Executing AI role

The AI may organize, compare, trace, challenge, and test candidate material.
The AI is NOT the technical authority and may not originate governed rules,
validated checklist items, thresholds, safety claims, compatibility
conclusions, or specialist mappings. Every AI-originated technical item is
classified UNVERIFIED CANDIDATE; the AI must abstain and escalate on any need
to assert an unsupported technical fact, name a specialist, or generate an
unsupported research topic.

---

## 8. Domain Registry boundary

- read-only contextual use only;
- not a governed knowledge authority;
- no research artifact written into it;
- all D13 research artifacts isolated from production and persistence;
- no remediation authorized;
- the final remediate/isolate/replace architecture decision is deferred to
  §16 Gate 6 of the research contract.

---

## 9. Evidence and reproducibility requirements

Minimum research evidence package (generated only under a future authorized
research phase): research manifest; source-category decision record; source
inventory and versions; licensing/provenance notes; scenario inventory;
input/output records; accepted-and-rejected candidate log; contradiction log;
abstention-decision log; expert-review record; independent-review record;
unresolved-issues register; hashes; version history; owner-decision register;
final recommendation. Separately identifiable (never consolidated away): the
expert-review record, the independent-review record, the manifest, and the
owner-decision register.

---

## 10. Qualified technical expert — competency and responsibility

Approved competency criteria: demonstrable competence in low-voltage embedded
electronics; sensor-interface design; microcontroller input/output constraints
(logic levels, input impedance, ADC basics); datasheet interpretation;
measurement and test planning; failure-mode reasoning; technical
documentation; and the ability to distinguish engineering fact from
assumption. The expert must review every candidate technical rule,
required-input item, subdomain mapping, and specialist condition. The expert
must not decide legal patentability, inventorship, commercial strategy, or
governance scope. No individual is appointed by this decision.

---

## 11. Independent reviewer — competency and independence

Approved criteria: distinct from the executing AI, the primary technical
expert, and any candidate-rule author; comparable low-voltage-electronics
competency; no conflict of interest with the reviewed content. Review scope:
scope discipline; source authority; provenance integrity; abstention
correctness; hallucination controls; the AI technical-authority boundary; and
the implementation-readiness conclusion. Required outputs: a written verdict,
itemized findings, and a pass/return recommendation. No individual is
appointed by this decision.

---

## 12. Stop conditions

Concept-class drift beyond single-signal sensor-to-microcontroller (including
any bus, differential, or wireless creep); need for unauthorized sources or
RESTRICTED text without separate access confirmation; unresolved source
authority or licensing; provenance cannot be preserved; a contradiction the
expert cannot resolve; a breach of the AI technical-authority boundary; an
unsafe or unsupported specialist mapping; an unsupported research-topic
generation; any registry read that risks silent capability loss or production
contamination; findings that begin to resemble implementation; Workstream 8 or
AI Coach scope becoming necessary; or evidence insufficient to recommend an
implementation vehicle.

---

## 13. Completion threshold

The research phase may be considered complete only when: all authorized
questions are answered or explicitly classified unresolved; the evidence
package is complete; qualified-expert review is complete; independent review
is complete; an abstention policy is proposed; a provenance model is proposed;
a Domain Registry suitability recommendation is produced; the smallest safe
implementation candidate is identified or rejected; limitations are recorded;
and owner decisions are identified. Completion must not imply D13
implementation, D13 satisfaction, product-readiness increase, Workstream 8
authorization, or patent-export readiness.

---

## 14. Preserved boundaries

Gate 2 is complete as a governance decision package; Gate 3 cannot be issued
until the actual execution, expert, and reviewer appointments are named and
verified. No appointment is made by this document; no source is selected; no
source is accessed; no research is authorized; no technical rule, checklist,
threshold, or mapping is created. D13 remains UNSATISFIED / UNIMPLEMENTED; no
Workstream number or implementation vehicle is assigned; Workstream 8 remains
NOT AUTHORIZED / NOT STARTED; Workstreams 1–7 remain CLOSED / CANONICAL; the AI
Coach remains prohibited and blocked; Answer Clarification remains inactive;
the persistence freeze is unchanged; the official product state remains
DEMO_READY_WITH_LIMITATIONS; the MVP scope remains electronics/electrical-only;
PR #167 and PR #162 remain OPEN / DRAFT, outside this decision, and untouched;
the remediation program remains INCOMPLETE.
