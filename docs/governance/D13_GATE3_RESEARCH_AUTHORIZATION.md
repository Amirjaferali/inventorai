# D13 Gate 3 — Research Authorization

**Status:** OWNER AUTHORIZATION — GATE 3 RECORDED —
RESEARCH ACTIVATION BLOCKED —
NO D13 IMPLEMENTATION AUTHORIZED

This owner authorization becomes canonical only when this docs-only recording
increment is merged into the authoritative branch. Canonical recording alone
does NOT activate research. Research activation is separately gated by Gate 3A
(§4). No research method, external-source access, workspace creation, or
appointment execution begins through recording alone, and none begins
automatically upon merge.

Gate 3 is issued under the D13 Knowledge-Governance Research Contract
(`docs/governance/D13_KNOWLEDGE_GOVERNANCE_RESEARCH_CONTRACT.md`, §16 Gate 3)
and incorporates by reference the canonical Gate 2 Pre-Research Owner Decision
(`docs/governance/D13_GATE2_PRE_RESEARCH_OWNER_DECISION.md`) in full.

**Authoritative context:** authoritative branch
`feature/atomic-json-session-persistence`; authoritative tip
`aebdd53f316fcbbe964a9d110bb31e01f938beb2`; the D13 research contract and the
Gate 2 decision are CONTRACT / CANONICAL; D13 remains UNSATISFIED /
UNIMPLEMENTED; Workstream 8 remains NOT AUTHORIZED / NOT STARTED; official
product state DEMO_READY_WITH_LIMITATIONS; MVP scope electronics/electrical-only;
persistence FROZEN; AI Coach PROHIBITED / BLOCKED; Answer Clarification
INACTIVE.

---

## 1. Two distinct states

This authorization separates two states that must never be conflated:

- **Gate 3 canonical recording** — achieved by merging this docs-only
  increment. It records the authorization and its bounds. It activates
  nothing.
- **Gate 3 research activation** — achieved only when Gate 3A (§4) passes
  after merge. Research begins only after activation.

The lifecycle stages, each separately controlled, are: canonical Gate 3
recording; Gate 3A research activation; Phase A execution; Phase B controlled
source access; qualified-expert review; independent review; owner
research-completion decision. None of these later stages is authorized or
satisfied by recording this document.

---

## 2. Roles

**Executing AI agent:** Claude Code, acting as research coordinator and
evidence compiler. Claude Code is NOT the technical authority.

**Accountable governance authority:** the product owner.

**Technical authority:** the owner-approved qualified technical expert.

**Independent assurance:** the owner-approved independent reviewer.

No separate human research coordinator is required.

Claude Code MAY:

- analyze repository and journey data;
- organize approved source material;
- prepare UNVERIFIED CANDIDATE findings;
- maintain manifests, source inventories, provenance records, contradiction
  logs, and abstention logs;
- test candidate diagnostic structures;
- compile evidence.

Claude Code MAY NOT:

- act as the technical authority;
- originate governed engineering rules;
- approve technical conclusions;
- approve specialist mappings;
- override manufacturer documentation, standards, test evidence, or expert
  review;
- declare research complete.

No actual person or organization is appointed by this document.

---

## 3. Authorized concept class, objective, and phases

**Concept class (unchanged from Gate 2):** low-voltage, non-safety-critical,
single-signal sensor-to-microcontroller interfacing. Permitted comparison:
analog voltage output; single-ended digital logic output; pulse or frequency
output.

**Excluded (unchanged):** I²C; SPI; UART; CAN; USB; other communication buses;
differential signaling; wireless links; mains voltage; high-power systems;
battery management; motor-drive power stages; medical, automotive, aerospace,
or safety-critical applications; final circuit design; general embedded-system
design.

**Objective:** determine whether D13 can, for one sensor output connected to
one microcontroller input within the class above, reliably identify: the
unresolved technical subproblem; why it matters; the missing information;
bounded research topics; the required evidence or test; what InventorAI cannot
verify; the supported specialist discipline; the required abstention
condition; and per-finding provenance. This is a diagnostic-capability test.
It does not design a circuit and does not fill the inventor's knowledge gap on
the inventor's behalf.

**Phase A — Repository and journey-data analysis.** Identify what the existing
journey captures; identify what is absent; map acknowledged unknowns and
unresolved claims; inventory existing rule surfaces; analyze current
provenance surfaces; identify diagnostic-method failure modes; identify
abstention needs; prepare candidate research questions. Phase A must not assert
engineering facts as authoritative, create governed rules, create a final
required-input checklist, select specialist mappings, or access external
sources.

**Phase B — Controlled source-based validation.** Allowed only after all
required appointments are active and the Phase A manifest and research-question
set are accepted by the qualified expert (Gate 3C). Validates Phase A
candidates against approved sources, in-class only.

No technical checklist or engineering rule is created by this authorization.

---

## 4. Gate 3A — research activation

Research activation is blocked until Gate 3A passes. Gate 3A minimum
activation conditions:

1. the executing AI agent (Claude Code) is recorded;
2. the qualified technical expert is appointed, verified against the Gate 2
   §10 competency criteria, and owner-approved;
3. confidentiality and conflict-of-interest declarations are recorded;
4. the isolated workspace location (§12) is approved;
5. the research caps (§11) are approved;
6. no material scope or repository divergence exists.

No research method or external-source access begins before Gate 3A.

---

## 5. Evidence and review gates

- **Gate 3A** — appointments (executing agent + qualified expert) and
  activation conditions satisfied.
- **Gate 3B** — Phase A manifest and scope verification.
- **Gate 3C** — qualified-expert approval of the Phase A research-question set.
- **Gate 3D** — controlled Phase B source access begins.
- **Gate 3E** — candidate knowledge package complete (independent reviewer must
  be appointed and verified before this gate begins).
- **Gate 3F** — qualified-expert review complete.
- **Gate 3G** — independent review complete (cannot occur without an active,
  verified independent reviewer).
- **Gate 3H** — owner research-completion decision.

Passing Gate 3A–3H completes the research phase only. It does not implement or
satisfy D13 and does not authorize any later contract gate.

---

## 6. Appointment timing

**Qualified technical expert:** appointment required before Gate 3C; must
review and approve the Phase A research-question set; must be active before
Phase B begins.

**Independent reviewer:** not required to record Gate 3 canonically; not
required for Gate 3A; must be appointed and verified before Gate 3E begins;
mandatory before Gate 3G; must remain independent of the executing AI agent,
the qualified expert, and every candidate-content author. If the reviewer
later contributes to candidate technical content, independence is lost for
that content, the affected artifacts are re-reviewed by a newly appointed
independent reviewer, and the loss is logged.

Appointment records must capture, at minimum, for the expert and the reviewer:
accountable identity or organization; competency evidence against the Gate 2
criteria; conflict-of-interest declaration; confidentiality commitment; scope
acceptance; availability; explicit written acceptance; and owner approval. No
individual or organization is appointed by this document.

---

## 7. Source-access boundary

**Permitted retrieval:** targeted retrieval limited to the explicitly approved
source categories —

- public manufacturer datasheets;
- public manufacturer application notes;
- public university or government technical references;
- publicly accessible standards summaries for context only.

**Prohibited retrieval:** open-ended or unrestricted web browsing used as
technical authority, and any retrieval from PROHIBITED source categories
(forums; blogs; community answers; unrestricted web retrieval; commercial
databases; vendor APIs; anonymous or unattributed technical content).

**Restricted:** full licensed or subscription standards text remains behind a
separate, source-specific owner access confirmation.

Every actual source later used must be inventoried, versioned, dated, cited,
license-reviewed, and provenance-linked. No source is selected or accessed by
this authorization.

---

## 8. Claim-specific authority model and AI boundary

Authority is claim-specific, not role-based:

- named-component electrical limits: manufacturer-controlled technical
  documentation is primary;
- normative engineering or safety requirements: the applicable recognized
  standard is primary;
- observed technical behavior: documented test evidence is primary;
- engineering interpretation and system application: qualified-expert review
  is required;
- AI-originated technical content: UNVERIFIED CANDIDATE only.

Every AI-originated technical item remains UNVERIFIED CANDIDATE until it is
supported by approved authoritative material, reviewed by the qualified expert,
independently reviewed, formally accepted through the knowledge-governance
process, versioned, and provenance-linked. An
UNVERIFIED CANDIDATE must never become governed knowledge, product behavior,
user-facing guidance, an implementation requirement, a specialist-routing
rule, or a safety statement. The qualified expert may interpret and adjudicate
but must not silently override manufacturer specifications, applicable
standards, or documented test results. AI content must remain visibly distinct
from source-linked or expert-supplied content at every stage.

---

## 9. Research questions

For one in-class sensor output into one microcontroller input, the authorized
questions determine whether InventorAI can reliably state: (1) the precise
unresolved technical subproblem; (2) why it matters; (3) the missing
information; (4) the bounded technical topic to investigate; (5) the required
evidence or test; (6) what the application cannot verify; (7) when it must
abstain; (8) the relevant technical discipline; (9) the provenance supporting
each of the above; and (10) whether (1)–(9) can be produced without
originating an ungoverned engineering fact. The questions test diagnostic
capability; they do not design a circuit.

---

## 10. Required research outputs

Generated only under an activated research phase; each remains explicitly
identifiable, independently reviewable, and provenance-linked in the evidence
manifest: research manifest; approved-scope statement; appointment records;
source-category decision record; source inventory with versions and retrieval
dates; licensing and provenance record; repository/journey-data findings;
scenario inventory; candidate unresolved-subproblem patterns; candidate
missing-information patterns; candidate bounded research-topic patterns;
candidate evidence/test-needed patterns; candidate cannot-verify statements;
candidate abstention conditions; candidate specialist-discipline conditions;
accepted-candidate log; rejected-candidate log; contradiction log;
unresolved-issues register; qualified-expert-review record;
independent-review record; hash and version manifest; final research
recommendation; smallest-safe-implementation-candidate recommendation or
rejection. Separately identifiable and never consolidated away: the
expert-review record, the independent-review record, the manifest, and the
owner-decision register. All technical candidate outputs remain UNVERIFIED
CANDIDATE until the expert (Gate 3F) and independent (Gate 3G) reviews accept
them. All research artifacts committed to the repository must use synthetic or
fictional invention examples; actual confidential user invention records must
never be committed (see §13).

---

## 11. Time and effort boundaries

Owner-selected execution caps (caps, not completion promises):

- Phase A: maximum 5 working days or 30 execution hours, whichever occurs
  first.
- Phase B: maximum 10 working days or 60 execution hours, whichever occurs
  first.
- maximum scenarios: 6;
- maximum actual component examples: 3;
- maximum primary sources per component example: 3;
- optional contextual standards summaries: maximum 1 per component example
  where necessary;
- maximum qualified-expert review cycles: 2;
- maximum independent-review cycles: 2.

Any extension requires explicit owner authorization (Contract §16 Gate 4).

---

## 12. Research workspace and Domain Registry boundary

**Proposed isolated workspace:** `docs/governance/research/d13/`.

- research-only; non-production;
- outside `engine/`, `web/`, `domains/`, templates, persistence, and schemas;
- not created by this Gate 3 recording; may be created only after Gate 3 is
  merged and Gate 3A activation passes;
- committed workspace artifacts use synthetic or fictional invention examples
  only; no actual confidential user invention record is written to the
  workspace or to any other repository path; this repository-data hygiene rule
  does not restrict runtime processing of real invention information (see §13);
- no Domain Registry artifact is written or modified.

**Domain Registry:** read-only contextual use only; not a governed knowledge
authority; no research artifact written into it; all research artifacts
isolated from production and persistence; no remediation authorized; the final
remediate/isolate/replace architecture decision is deferred to Contract §16
Gate 6. The 31 `tests/test_domain_registry.py` failures remain unfixed and
unreclassified.

---

## 13. Confidentiality, repository-data hygiene, and intellectual-property boundary

Product capability and repository material are separate concerns.

The repository's current public visibility does not prohibit, narrow, remove,
or defer any approved InventorAI capability.

The application may be designed and implemented to capture, process, analyze,
preserve, and export actual user invention information under the approved
runtime storage, confidentiality, retention, and access-control architecture.

The public repository may contain source code, schemas, workflows, generic
templates, synthetic fixtures, fictional invention examples, confidentiality
logic, storage logic, and export structures.

The public repository must not contain actual confidential user invention
records, unpublished user-specific disclosures, production credentials, live
secrets, private user-specific expert submissions, or other production-sensitive
information.

All committed research examples, tests, fixtures, documentation, and evidence
samples must therefore use synthetic, fictional, or properly de-identified
material.

This is a repository-data hygiene boundary only.

It is not a restriction on invention capture, runtime invention processing, D13
technical-gap analysis, structured invention disclosure, future patent-export
functionality, or the final application vision.

Later conversion of the repository to private does not retroactively remove
prior public availability.

Manufacturer and expert-supplied material must remain attributed, versioned,
license-reviewed, and provenance-linked.

Research outputs must not be treated as patentability or inventorship
determinations. Patent-export architecture remains outside this research
increment but is not prohibited or cancelled.

---

## 14. Stop conditions

Concept-class drift; bus, differential, wireless, power, or safety-critical
creep; use of an unauthorized source; need for RESTRICTED material without
owner confirmation; unresolved licensing; inability to preserve provenance;
contradiction unresolved by the required authority; AI technical-authority
boundary breach; unsupported research-topic generation; unsupported specialist
mapping; Domain Registry contamination or silent-capability-loss risk; findings
beginning to resemble implementation; AI Coach or Workstream 8 scope becoming
necessary; expert or reviewer independence loss; appointment withdrawal;
inadequate evidence; or a non-reproducible finding. Each condition results in a
defined disposition: temporary pause; owner escalation; source rejection;
candidate rejection; appointment replacement; or termination of the research
increment.

---

## 15. Research-completion threshold

Research completes only when every authorized question is answered or
explicitly classified unresolved; the evidence package is complete; provenance
is complete; licensing status is recorded; qualified-expert review is
complete; independent review is complete; an abstention model is proposed;
specialist-routing conditions are proposed or rejected; a Domain Registry
suitability recommendation is produced; the smallest safe implementation
candidate is identified or rejected; limitations and unresolved risks are
recorded; and the owner issues the Gate 3H research-completion decision.
Completion must not imply D13 satisfaction, D13 implementation,
product-readiness increase, RED authorization, Workstream 8 authorization, or
patent-export readiness.

---

## 16. Preserved boundaries

Gate 3 is recorded as an authorization only; research activation remains
blocked until Gate 3A passes after merge. No person or organization is
appointed by this document; no source is selected or accessed; no technical
rule, checklist, threshold, mapping, taxonomy, or decision table is created.
D13 remains UNSATISFIED / UNIMPLEMENTED; no Workstream number or implementation
vehicle is assigned; Workstream 8 remains NOT AUTHORIZED / NOT STARTED;
Workstreams 1–7 remain CLOSED / CANONICAL; the AI Coach remains prohibited and
blocked; Answer Clarification remains inactive; the persistence freeze is
unchanged; the official product state remains DEMO_READY_WITH_LIMITATIONS; the
MVP scope remains electronics/electrical-only; PR #167 and PR #162 remain OPEN
/ DRAFT, outside this authorization, and untouched; the remediation program
remains INCOMPLETE.
