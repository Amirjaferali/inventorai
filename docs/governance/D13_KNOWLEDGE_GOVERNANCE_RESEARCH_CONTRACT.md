# D13 Knowledge-Governance Research Contract

**Status:** OWNER-APPROVED — CONTRACT / CANONICAL — NO RESEARCH AUTHORIZED

This owner-approved status becomes canonical only when this docs-only
contract-recording increment is merged into the authoritative branch. Neither
owner approval nor canonical recording authorizes the research phase to begin.

**Document form:** Bounded research-phase contract (not a Workstream, not an
implementation contract, not a production increment). This document does NOT
assign D13 a Workstream number, the identity of Workstream 8, a "Workstream
7A" identity, or any implementation vehicle.

**Governing effect:** This contract is owner-approved and becomes canonical
upon merge of this docs-only recording increment. Recording authorizes no
research, no external access, no repository mutation beyond this docs-only
increment, and no D13 or Workstream 8 activity. The research phase begins only
under a separate explicit owner research authorization (§16 Gate 3).

---

## 1. Contract identity and status

**Identity:** D13 Knowledge-Governance Research Contract (a bounded,
read-and-analysis research phase to determine whether D13 can be supported by
a defensible, governed, bounded technical-knowledge structure, and to define
the smallest safe implementation scope that could later be proposed).

**Status:** OWNER-APPROVED — CONTRACT / CANONICAL — NO RESEARCH AUTHORIZED.

**Explicitly not:** Workstream 8; Workstream 7A; any new numbered Workstream;
an implementation contract; a production increment; a design document; a
taxonomy; a decision-table set; a schema.

**Effect of recording this contract:** recording alone does NOT start research
and authorizes no research method. Research begins only upon a separate,
explicit owner research authorization naming this contract (see §12 and §16
Gate 3).

---

## 2. Canonical basis

- Authoritative branch: `feature/atomic-json-session-persistence`.
- Authoritative tip at recording time: `0a4a49478faf38827abeac81effd49a52822c73a`
  (PR #199 merge; ordered parents `ece7f23a3a165d78b1aac2fa802a86d4cf378ad6`
  and `0763d7f49fb04365b4c6ccd4e893d55919ff806e`; merge tree
  `fe31d462878253ae4e87b9592eeed5cc3577aaa6`).
- Owner decision (merged, canonical,
  `docs/governance/D13_PRIORITY_AND_KNOWLEDGE_GOVERNANCE_OWNER_DECISION.md`):
  D13 is the next owner priority before Workstream 8; a bounded
  knowledge-governance research phase is the selected next governance
  direction; that research phase is NOT authorized to begin; the governance
  vehicle is unresolved; Workstream 8 is NOT AUTHORIZED and NOT STARTED.
- D13 canonical status (unchanged, Workstream 7 Increment Contract §4): D13 is
  a MANDATORY FUTURE PRODUCT CAPABILITY — NOT CANCELLED — NOT SATISFIED BY
  GENERIC SPECIALIST REFERRAL — SEPARATELY OWNER-GATED — NOT AUTHORIZED IN
  WORKSTREAM 7.
- Strategic constraint (`STRATEGIC_PRODUCT_VISION.md`): InventorAI is a gap
  identification and tracking layer / knowledge-gap surface engine, NOT a
  domain expert, feasibility oracle, implementation-readiness certifier, or
  regulatory/compliance guide; domain packs must declare covered areas,
  not-covered areas, and known limitations explicitly (Coverage Declaration
  Principle); the commercial architecture preservation constraint is active.

---

## 3. Research question

**Primary question (owner-accepted wording; may be refined but not
broadened):** Can a bounded, governed technical-knowledge structure support
reliable D13 diagnosis and guidance for a deliberately limited
electronics/electrical scope, without creating false precision, unsafe advice,
unsupported specialist routing, or untraceable model inference?

The question must not be broadened into general AI research, general
engineering knowledge, or full electronics/electrical-domain coverage.

---

## 4. Research objectives

A future authorized research phase must determine:

1. the smallest defensible initial concept-class scope;
2. the evidence required to classify a user concept into a supported concept
   class;
3. the minimum required-input checklist for each accepted class;
4. the distinction between (a) user-stated facts, (b) user-stated unknowns,
   (c) repository-rule-derived findings, (d) governed-knowledge-derived
   findings, and (e) unresolved system inference;
5. the maximum safe specificity of missing-input diagnosis, technical
   subdomain identification, research-topic generation, and specialist
   escalation;
6. the required abstention conditions;
7. how every output could be traced to a rule and to user evidence;
8. how the knowledge structure would be governed, reviewed, versioned,
   deprecated, and updated;
9. whether the current Domain Registry can host the knowledge safely;
10. whether a separate governed knowledge structure is required;
11. the smallest safe post-research implementation candidate;
12. whether no implementation should proceed.

---

## 5. Explicit non-objectives

The research phase must NOT:

- implement D13;
- change the user journey;
- change question order;
- add guided-answer functionality;
- activate AI Coach;
- activate Answer Clarification;
- change persistence;
- change production schemas;
- add user-facing specialist routing;
- generate live research guidance;
- select commercial vendors;
- build a general electronics knowledge base;
- support all electronics/electrical concept classes;
- expand the MVP beyond electronics/electrical;
- assert engineering validation or safety approval;
- resolve Workstream 8, 12, or 13;
- fix unrelated historical failures (including the 31
  `tests/test_domain_registry.py` failures) unless separately authorized.

---

## 6. Candidate research scope and concept-class selection gate

The research phase must recommend a deliberately small scope. Candidate
concept classes (analytical only; NOT selected here):

- DC motor drive and control;
- battery-powered low-voltage supply;
- sensor and microcontroller interfacing;
- another narrower concept class supported by repository evidence.

For each candidate the research must assess: evidence currently available from
the journey; likely missing inputs; safety risk; false-precision risk;
knowledge-authoring difficulty; specialist-routing complexity; and suitability
as a first research scope.

**Concept-class selection is a later owner gate** (§16 Gate 2). Concept-class
selection is required before research execution and must be made in the
later explicit owner research authorization. It is not selected or authorized
by recording this contract.

**Non-binding recommendation (owner consideration only):** the recommended
first candidate is **sensor and microcontroller interfacing**, because it
provides a lower-safety-risk environment for validating missing-input
diagnosis, provenance, knowledge tracing, and safe abstention before power,
motor-drive, or battery-heavy scopes. This is a recommendation only and is
neither selected nor authorized by this contract.

---

## 7. Knowledge-source governance

The research phase must define categories of potentially acceptable knowledge
sources WITHOUT selecting, browsing, ingesting, quoting, or approving any
actual source. Categories to assess:

- internally authored expert decision tables;
- manufacturer technical documentation;
- recognized engineering standards;
- university or government technical references;
- curated specialist-reviewed rules;
- controlled external retrieval.

For each category, assess: authority; traceability; licensing; update
frequency; versioning; domain scope; safety implications; contradiction
handling; deprecation; citation requirements; and abstention behavior when
sources disagree or are absent. No external source access is authorized by
this contract.

---

## 8. AI technical-authority boundary (binding)

The executing AI agent may organize, compare, trace, challenge, and test
candidate technical knowledge supplied by owner-approved sources or
owner-approved qualified experts.

The AI agent is NOT the technical authority that originates governed
engineering rules, required-input checklists, specialist mappings, safety
limits, thresholds, or validation claims.

Any AI-proposed technical rule, checklist item, subdomain mapping, research
topic, or specialist condition must remain explicitly classified:

    UNVERIFIED CANDIDATE

until:

1. linked to an owner-approved authoritative source or supplied by an
   owner-approved qualified expert;
2. independently reviewed;
3. accepted through the defined knowledge-governance process;
4. versioned and recorded with provenance.

An UNVERIFIED CANDIDATE must not become: governed knowledge; product behavior;
user-facing guidance; an implementation requirement; a specialist-routing
rule; or a safety statement.

The contract prohibits laundering model-generated content into apparently
expert-authored knowledge. Any research artifact must keep AI-proposed content
visibly distinct from source-linked or expert-supplied content at every stage.

---

## 9. Domain Registry decision gate

The known 31 `tests/test_domain_registry.py` failures are a CONDITIONAL
DEPENDENCY. The research must determine: whether the Domain Registry can be
used after remediation; whether governance-metadata validation must be
enforced first; whether the silent-skip behavior disqualifies the registry
from knowledge governance; whether a new independently governed structure is
safer; whether session-data-only findings can remain isolated from the
registry; and what decision is required before any knowledge-dependent
implementation. This contract does NOT authorize fixing, reclassifying, or
altering the registry or those failures. The registry architecture decision
itself is reserved to §16 Gate 6.

---

## 10. Safe-abstention contract

The research must define the conditions under which D13 must refuse to
diagnose or guide, at minimum: insufficient user evidence; unsupported concept
class; ambiguous component role; conflicting rules; absent governed rule;
obsolete or unreviewed knowledge; unsupported domain; safety-critical
uncertainty; specialist category not evidence-supported; search topic not
rule-supported. The required output is an abstention-POLICY proposal, not
production abstention behavior.

---

## 11. Provenance and inference controls

The research must propose how future D13 outputs could preserve: originating
requirement id; originating user statement; rule or source identifier; source
version; derivation category; confidence or support classification;
unsupported or abstained status; timestamp or knowledge-version context; and
the distinction between user knowledge and system inference. The research must
NOT define final product schema.

---

## 12. Research-method authorization model

- Recording this contract authorizes NO research method.
- The later owner research authorization (§16 Gate 3), incorporating the
  approved pre-research decision package (§16 Gate 2), must identify: the
  permitted method set; the selected concept-class scope; the approved
  knowledge-source categories for actual assessment; the external-access
  boundary; and the executing and reviewing roles.
- Within that authorization, the executing agent may run any method in the
  permitted set without seeking method-by-method re-authorization.
- A NEW owner authorization (§16 Gate 4) is required only when the research
  would exceed the approved method set, source boundary, concept-class scope,
  external-access boundary, role assignment, or research objective.

Candidate methods a research authorization may permit include: repository
analysis; rule inventory; concept-class comparison; expert-authored candidate
tables; source-quality assessment; adversarial scenario analysis;
contradiction analysis; failure-mode analysis; provenance mapping; and
abstention-threshold analysis. Listing a method here does not authorize it.

---

## 13. Research outputs required

A future authorized research phase must produce: (A) research evidence
register; (B) candidate concept-class comparison; (C) available-data /
required-data matrix; (D) candidate required-input checklists; (E)
knowledge-source governance matrix; (F) Domain Registry suitability decision;
(G) provenance model proposal; (H) abstention-policy proposal; (I)
specialist-escalation evidence rules; (J) research-topic generation boundary
proposal; (K) risk and hallucination register; (L) candidate first
implementation scope; (M) deferred capability register; (N) owner-decision
register; (O) final recommendation (proceed with a limited implementation
contract / conduct additional research / split D13 into multiple capabilities
/ do not implement).

The required outputs may be consolidated into a smaller set of research
artifacts, provided each required output remains explicitly identifiable,
independently reviewable, provenance-linked, and included in the evidence
manifest. No required output may be weakened or deleted. All outputs remain
research artifacts, never product behavior.

---

## 14. Evidence and reproducibility requirements

No research evidence is generated under the current contract-recording
authorization.

Once separately authorized, the research phase executed under this contract
must generate and preserve the required evidence and reproducibility package,
including: source inventory; source identifiers and versions;
licensing/provenance notes; author or reviewer identity; decision logs;
rejected alternatives; scenario inputs; analysis outputs; hashes; a manifest;
review findings; and unresolved limitations. No provision of this contract
permits an authorized research phase to operate without that evidence and
reproducibility package.

---

## 15. Independent review requirements

The research phase must be independently reviewed for: scope discipline;
source authority; safety boundaries; provenance; hallucination controls;
licensing concerns; the Domain Registry decision; abstention criteria; the
AI technical-authority boundary (§8); and the implementation-readiness
conclusion. The research phase must NOT close based only on the executing
agent's report.

---

## 16. Owner decision gates (separate; never combined)

### Gate 1 — Contract recording

Canonical recording of this contract.

Contract recording authorizes no research method, source access, concept-class
selection, expert engagement, or research execution.

### Gate 2 — Pre-research owner decision package

Before research authorization, the owner must approve a complete package
identifying:

- the selected concept-class scope;
- the precise bounded research scope;
- the permitted research-method set;
- the approved knowledge-source categories for actual assessment;
- the external-access boundary;
- the executing role;
- any owner-approved qualified technical expert role;
- the independent reviewer role;
- the applicable Domain Registry isolation or non-reliance boundary during
  research;
- the evidence and reproducibility expectations.

No research may begin while any required part of this package is unresolved.

### Gate 3 — Explicit research authorization

The owner may authorize research only by expressly incorporating the complete
approved Gate-2 decision package and naming this recorded contract.

Research authorization must not be inferred from contract recording,
concept-class discussion, source-category discussion, reviewer selection, or
any partial decision.

### Gate 4 — Research-scope expansion

A new owner authorization is required before exceeding the approved:

- concept-class scope;
- method set;
- source-category boundary;
- external-access boundary;
- executing or reviewing role;
- research objective.

### Gate 5 — Research-output acceptance

The owner decides whether the completed research outputs and independent
review are accepted, rejected, or require additional research.

### Gate 6 — Domain Registry architecture decision

After considering the research findings, the owner decides whether to:

- remediate the current registry;
- isolate D13 from it;
- approve a separately governed knowledge structure;
- or decline knowledge-dependent implementation.

### Gate 7 — Implementation-vehicle selection

The owner separately decides whether D13 proceeds as:

- one Workstream with multiple increments;
- multiple Workstreams;
- a capability program;
- a limited implementation increment;
- additional research;
- or no implementation.

### Gates 8–13 — Later delivery gates

8. implementation contract;
9. RED authorization;
10. implementation authorization;
11. evidence and merge;
12. closure;
13. Workstream 8 activation.

None of Gates 5–13 is authorized or satisfied by recording or executing the
research contract.

---

## 17. Stop conditions

The research phase must stop if: repository state diverges; scope expands
beyond the owner-selected concept classes; an external source is needed but
not authorized; knowledge authority cannot be established; licensing is
unclear; contradiction cannot be resolved; safe abstention cannot be defined;
provenance cannot be preserved; the AI technical-authority boundary would be
breached; Domain Registry behavior creates silent capability loss; findings
begin to resemble production implementation; Workstream 8 or AI Coach scope
becomes necessary; or the evidence is insufficient to recommend an
implementation vehicle.

---

## 18. Completion criteria

"Research complete" is distinct from "D13 implemented." The research phase may
be considered complete only if: all authorized questions were answered or
explicitly classified unresolved; evidence is preserved; independent review is
complete; limitations are recorded; owner decisions are clearly identified;
and a defensible next-step recommendation exists. Research completion must NOT
mean D13 implemented, D13 satisfied, user-facing behavior changed, Workstream
8 authorized, or product readiness increased.

---

## 19. Required status language (preserved)

- D13: UNSATISFIED / UNIMPLEMENTED.
- D13 research: NOT AUTHORIZED UNTIL SEPARATE OWNER ACTION.
- Workstream 8: NOT AUTHORIZED / NOT STARTED.
- Workstreams 1–7: CLOSED / CANONICAL.
- Official product state: DEMO_READY_WITH_LIMITATIONS.
- MVP scope: electronics/electrical-only.
- Persistence: FROZEN.
- AI Coach: PROHIBITED / BLOCKED.
- Answer Clarification: INACTIVE.
- Remediation program: INCOMPLETE.

The Workstream 7 Increment Contract §4 D13 status language is unchanged and is
not altered by this contract. Nothing in this contract authorizes or completes
any later D13 phase.
