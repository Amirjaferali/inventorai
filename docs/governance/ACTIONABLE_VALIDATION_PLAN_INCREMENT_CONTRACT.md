# Workstream 7 — Actionable Validation Plan — Increment Contract

**Status:** CONTRACT / CANONICAL — BASE RED NOT AUTHORIZED — NO IMPLEMENTATION AUTHORIZED

**Workstream:** Workstream 7 — Actionable Validation Plan (P1;
`DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §5 item 7, §15 row 7).

**Authoritative branch:** `feature/atomic-json-session-persistence`
**Authoritative base tip:** `245482fc1ba52f57e42be9590ebc37191807b42b`
**Recording branch:** `docs/ws7-actionable-validation-plan-contract`

**Authority chain:** the CLAUDE.md governance contract;
`DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` §§8–12; the accepted
Workstream 7 read-only source review performed at the authoritative base tip
(verdict A); the owner decision confirmations C1–C3 and the owner-mandated
D13 amendment; and the owner recording authorization for this document. This
contract is subordinate to all committed anchors. It authorizes NO
implementation: recording, BASE RED, implementation, independent reviews,
merges, evidence, and closure each require separate explicit owner
authorization. Workstream 7 explicitly does NOT implement, approximate, or
satisfy the mandatory future capability defined in D13.

---

## 1. Objective

Make Section 14 validation steps more useful and truthful USING ONLY DATA
ALREADY PRESENT IN THE REPOSITORY: requirement-linked validation actions for
eligible answered requirements; honest presentation of unresolved
responsibility; suppression of the meaningless confidence line; bounded
generic advisories for pending evidence and pending specialist input. No
domain-specific engineering instruction and no implied expertise (D1).

---

## 2. Governing evidence and source-review basis

The accepted Workstream 7 read-only source review at tip
`245482fc1ba52f57e42be9590ebc37191807b42b` (verdict A) and its deterministic
current-behavior record: the canonical Workstream 1 journey yields 13
Section 14 steps with only 2 distinct statements (the generic
`Validate the recorded answer against the available evidence.` twelve
times); `Responsibility undetermined` on unresolved rows; `Confidence
undetermined` on all 13 steps from a hard-coded token with no underlying
model; Section 11 produced exactly one experiment (defect 9 not reproduced).
Remediation plan §3.B defects 6 and 8; the Workstream 6 contract's deferred
item 6 and owner decision D6.

### 2.1 User-visible defect statement

A nontechnical inventor receives a "Validation Plan" whose steps are
indistinguishable generic sentences not visibly tied to any specific
recorded requirement, a placeholder responsibility phrase, and a confidence
phrase that mimics an assessment that never happened.

---

## 3. Exact scope (four items only)

1. **Requirement-linked validation actions (D3 as confirmed by C1; D4).**
   For eligible `answered`-record requirements, the Section 14 step
   statement becomes the owner-selected wording
   `Validate this recorded answer against the available evidence:
   “<requirement statement, byte-verbatim>”`, built at the
   `engine/validation_plan.py` layer from the requirement's already-derived
   statement. Binding C1 conditions: deterministic linkage to the source
   requirement; no paraphrase or semantic rewriting; byte-verbatim source
   preservation; no loss of clarity; no unnecessary duplicate visual
   rendering — where the identical requirement statement is already
   displayed immediately adjacent to the step, the presentation must avoid
   confusing duplication WITHOUT altering the owner-approved meaning, the
   byte-verbatim JSON statement, or the deterministic linkage (a
   presentation-layer concern only; the JSON step statement always carries
   the full owner wording with the verbatim embed). Contradiction, gap,
   pending, unknown, deferred, and provisional actions are unchanged. Only
   the fixed non-domain verbs of D4 are permitted (confirm; validate;
   compare against recorded evidence; obtain the missing evidence; resolve
   conflicting recorded information); no technical instruction generation.
2. **Responsibility presentation (D5 as confirmed by C3).** The internal
   token `UNDETERMINED` and the validation-engine classification remain
   unchanged; no actor of any kind is assigned (no engineer, specialist,
   team, department, supplier, laboratory, regulator, or named actor); the
   public presentation for `UNDETERMINED` becomes the exact two-sentence
   owner wording rendered as TWO SEPARATE LINES; grouping, ordering, IDs,
   and internal classification unchanged; no implication that the system
   knows the appropriate owner. No responsibility data model is authorized.
3. **Confidence presentation (D6).** The internal token and JSON structure
   remain byte-unchanged; the HTML confidence line is suppressed when the
   token is `UNDETERMINED`; no confidence model, score, percentage, or
   High/Medium/Low classification; no test may imply a confidence assessment
   occurred.
4. **Pending advisories (D7/D8 as carried per C2).** An ADDITIVE OPTIONAL
   per-step JSON field `advisory` — absent or null wherever no advisory
   applies; the exact owner wordings for `pending_evidence` and
   `pending_specialist` only; NO Section 14 section-level key; no
   step-count, ID, order, grouping, or collapse change; backward-compatible
   JSON; no advisory on unknown, deferred, provisional_assumption,
   answered, contradiction, or gap rows unless separately authorized. The
   pending-specialist advisory is an HONEST INTERIM LIMITATION NOTICE ONLY
   — it does not satisfy, approximate, or discharge D13.

---

## 4. Owner decisions D1–D13 (binding register)

- **D1 — Bounded objective.** As §1/§3: more useful and truthful Section 14
  steps from existing data only; no domain-specific engineering
  instructions; no implied expertise.
- **D2 — Section 11 and defect 9 excluded.** Defect 9 (duplicated prototype
  experiments) and all Section 11 prototype/test-plan generation are
  excluded: the defect did not reproduce on the canonical journey; Section
  11 is a separate surface; reopening requires separate reproduction, owner
  decision, and increment. `engine/deliverable_assembler.py::_s11`, Section
  11 templates, Section 11 tests, prototype experiment IDs, the existing
  lexical-overlap deduplication, and experiment count and ordering remain
  unchanged.
- **D3 — Requirement-linked validation actions.** Alternative (a) selected
  (owner confirmation C1), with the C1 anti-duplication presentation
  condition. The implementation must not paraphrase, summarize
  semantically, normalize, rewrite, infer technical meaning, or add
  thresholds, test methods, tools, standards, specialist types, or
  laboratory or simulation guidance.
- **D4 — Bounded generic verb vocabulary only.** Fixed non-domain-specific
  verbs (confirm; validate; compare against recorded evidence; obtain the
  missing evidence; resolve conflicting recorded information); these verbs
  must not imply that the system knows the technical procedure.
- **D5 — Responsibility presentation.** Exact wording, two displayed lines
  (owner confirmation C3); token and classification unchanged; no actor
  assigned.
- **D6 — Confidence presentation.** HTML suppression for `UNDETERMINED`;
  JSON structure and internal token unchanged for compatibility.
- **D7 — Pending-evidence advisory.** Exact wording; relies only on the
  recorded request; no test method, tool, standard, simulation, laboratory,
  or product; no technical-sufficiency inference; no claim that the
  evidence has been validated.
- **D8 — Pending-specialist advisory.** Exact wording including the
  explicit capability limitation; no specialist type, company, person,
  department, product, tool, laboratory, simulation, or standard; no
  implication that a referral was performed or that the system knows who is
  competent. Specialist taxonomy and routing remain separately owner-gated
  future capabilities.
- **D9 — Workstream 6 pass-through protected.** The Section 13 -> Section 14
  wording pass-through for unknown, deferred, and provisional_assumption
  remains unchanged; the Workstream 6 focused P5 assertion remains
  protected and must not require amendment. Workstream 7 may not alter
  Workstream 6 disposition labels, statuses, resolving actions, requirement
  IDs, Section 13 rows, ordering, one-row-per-record behavior, synthesis
  metadata, or metadata-to-HTML parity.
- **D10 — Grouping and collapse frozen.** Existing Section 14 grouping,
  collapse, headers, count wording, ordering, responsibility grouping,
  confidence grouping, and rendered structure remain frozen unless a future
  BASE RED proves a direct contradiction and the owner separately
  authorizes an amendment. Workstream 7 must not redesign the Phase 7A or
  7B presentation. Any reduction in duplicated presentation must result
  only from the authorized validation-action differentiation, not from a
  new collapse algorithm.
- **D11 — Structural invariants.** Exactly one Section 14 step or blocked
  item per eligible Section 13 requirement; the Section 13 -> 14 arithmetic
  tie; validation step IDs; source requirement IDs; order inherited from
  the Requirement Landscape; inventor statements byte-verbatim; existing
  blocked-item semantics; existing responsibility engine tokens; the
  existing confidence token; Workstream 4 criticality authority and
  rationale; Workstream 5 risk/safety linkage; Workstream 6 vocabulary and
  metadata; persistence, benchmark, and replay behavior.
- **D12 — Explicitly deferred future capabilities.** Full list in §12.
- **D13 — Mandatory Future Technical Capability Gap Detection and
  Actionable Research Guidance.** Status language:

  ```text
  MANDATORY FUTURE PRODUCT CAPABILITY —
  NOT CANCELLED —
  NOT SATISFIED BY GENERIC SPECIALIST REFERRAL —
  SEPARATELY OWNER-GATED —
  NOT AUTHORIZED IN WORKSTREAM 7
  ```

  The system must not treat generic guidance such as "consult an engineer",
  "consult a specialist", "search online", or "research electronics" as
  completion of this capability. Where supported by a future governed
  knowledge source, this capability must be able to:
  1. identify the exact unresolved subsystem or technical subproblem;
  2. identify the relevant technical subdomain at the narrowest reliably
     supported level;
  3. explain why the currently recorded information is insufficient;
  4. list the specific missing inputs, measurements, decisions, or
     constraints;
  5. provide precise research topics and search terms rather than a generic
     field name;
  6. distinguish what the inventor can investigate directly from what
     requires specialist input;
  7. state clearly what the system cannot currently verify;
  8. identify a specialist category only when supported by governed
     evidence;
  9. avoid inventing competence, tools, laboratories, standards, methods,
     products, or availability;
  10. preserve provenance from the inventor's recorded requirement to every
      identified gap and research direction.

  The Workstream 7 generic pending-specialist advisory is ONLY an honest
  interim limitation notice and must never be described as satisfying D13.

  A later owner-gated D13 Source Review must determine at minimum:
  subsystem decomposition method; technical subdomain taxonomy;
  capability-gap classification; governed knowledge sources; research-term
  derivation; provenance and citations; hallucination controls; safety
  boundaries; when a specialist type can be named; when tools, standards,
  laboratories, or simulations may be mentioned; how unsupported capability
  is disclosed; whether Domain Registry changes are required; and how this
  capability remains separate from AI Coach and Answer Clarification.
  Nothing in Workstream 7 designs or implements any part of D13.

---

## 5. Exact public wordings (byte-exact; owner-approved)

### 5.1 Requirement-linked answered action (D3/C1)

```text
Validate this recorded answer against the available evidence: “<requirement statement, byte-verbatim>”
```

where `<requirement statement, byte-verbatim>` is the requirement's
already-derived statement embedded byte-verbatim. The JSON step statement
always carries the full wording with the verbatim embed; the template
avoids confusing adjacent duplicate display without changing meaning or
bytes (C1).

### 5.2 Responsibility, `UNDETERMINED` only (D5/C3; two displayed lines)

```text
Responsibility has not yet been assigned.
Choose who will own this validation step before relying on the result.
```

### 5.3 Confidence (D6)

No wording — the `Confidence: …` HTML fragment is suppressed for
`UNDETERMINED`; the JSON `confidence` and `confidence_label` fields remain
byte-unchanged.

### 5.4 Pending-evidence advisory (D7)

```text
Additional evidence is still required for this item.
Prepare or obtain the evidence identified in the recorded request before treating the item as validated.
```

### 5.5 Pending-specialist advisory (D8)

```text
Specialist input is still required for this item.
The appropriate specialist has not yet been identified by the system.
```

### 5.6 Unchanged vocabularies

All Workstream 6 disposition wordings; the pending, contradiction, and gap
resolving actions; all other responsibility labels; the Phase 7A group
headers; and the Phase 7B collapse count wording remain byte-unchanged.

---

## 6. Authorized production files

1. `engine/validation_plan.py` — eligible-answered statement construction;
   advisory attachment data.
2. `engine/deliverable_assembler.py` — `_s14` and its label constants only.
3. `web/templates/deliverable.html` — Section 14 block only, including the
   C1 anti-duplication presentation and the D5 two-line rendering.

## 7. Authorized test files

One new focused file `tests/test_actionable_validation_plan.py` (created
only at the separately authorized BASE RED gate). Strictly bounded
wording-pin amendments, each individually listed in the PR description and
evidence record, ONLY in:

- `tests/test_increment_5_validation_plan.py` — assertions pinning the
  legacy answered-action copy or the two placeholder labels;
- `tests/test_phase_7b_validation_plan_collapse.py` — assertions pinning
  the rendered confidence line or the `Responsibility undetermined` wording
  only;
- `tests/test_phase_7a_validation_plan_grouping.py` — label-wording pins
  only;
- `tests/test_deliverable_hygiene.py` — the single responsibility-label
  value rule only, if triggered.

No grouping, collapse, count, order, key-set, or structure assertion may
change.

## 8. Prohibited and frozen files

`engine/requirement_landscape.py`, `engine/idea_state.py`,
`engine/progression_loop.py`, `engine/safety_signal.py`, `web/app.py`,
`web/templates/session.html`, `engine/deliverable_assembler.py::_s11` and
every Section 11 template/test/ID/dedup/count/ordering behavior (D2),
persistence code, transcript schemas, benchmark code, replay code, all
evidence directories, governance documents outside the contract-recording
step, PR #167, PR #162. MUST NOT CHANGE test surfaces:
`tests/test_requirement_landscape_synthesis.py` (including P5),
`tests/test_increment_4_requirement_landscape.py`,
`tests/test_phase_7c_requirement_landscape_collapse.py`, the Workstream 4
criticality, Workstream 5 risk/safety, safety-signal, and wps001 suites,
and all Section 11 suites.

---

## 9. BASE RED requirements (separately authorized; no test is created by this contract)

Deterministic; a single new file; wordings pinned byte-exact to §5:

- **R1** — the WS1 journey's 12 answered steps currently share one generic
  statement (fails when requirement-linked differentiation is required).
- **R2** — a minimal answered fixture must receive the exact C1 wording
  embedding the statement byte-verbatim (fails on the generic sentence).
- **R3** — an `UNDETERMINED`-responsibility row must present the exact
  two-line D5 wording while the internal token remains `UNDETERMINED`
  (fails on `Responsibility undetermined`).
- **R4** — HTML must not render a confidence line for `UNDETERMINED` while
  JSON retains the unchanged fields (fails: the line is present today).
- **R5** — the `pending_evidence` step carries the exact D7 advisory in the
  additive `advisory` field and in HTML (fails: absent).
- **R6** — the `pending_specialist` step carries the exact D8 advisory
  including the explicit capability limitation (fails: absent).

### 9.1 Protected invariants (pass on BASE and HEAD)

Exactly one step/blocked item per eligible Section 13 requirement; the
Section 13 <-> Section 14 arithmetic tie; step/blocked IDs and
landscape-inherited order unchanged; Section 13 rows/IDs/statements/
ordering byte-unchanged; unknown/deferred/provisional pass-through
byte-unchanged (the Workstream 6 P5 assertion is never amended); Phase
7A/7B grouping, collapse, headers, and count wording unchanged; inventor
statements byte-verbatim; the `advisory` field absent or null on all
non-pending rows; no specialist type, tool, simulation, laboratory,
standard, threshold, test method, product, or confidence score anywhere in
output; blocked-item semantics unchanged; internal responsibility and
confidence tokens unchanged; JSON backward-compatible (additive `advisory`
only; no section-level key); Workstream 4/5/6 surfaces untouched; no test
implies a confidence assessment occurred or that D13 is satisfied.

---

## 10. GREEN, regression, and evidence gates

- **GREEN:** the focused suite passes with zero skips and zero xfails (a
  placeholder skip or xfail at GREEN is a failed gate); every wording
  byte-exact; the C1 anti-duplication condition demonstrably met without
  altering JSON statements.
- **Protected regression suites:** increment-5 (55, as bounded-amended),
  Phase-7A (9), Phase-7B (9), increment-4 (39), Phase-7C (7), Phase-4A (8),
  the Workstream 6 focused suite (12, unamended), deliverable hygiene (22),
  structured criticality (18), unified risk/safety (17), safety-signal
  (18 + 15), wps001 invariants (21), and the Section 11 suites (unamended).
- **Full-suite gate:** 31 known failures confined to
  `tests/test_domain_registry.py`; zero new failures; no reclassification;
  no new skip or xfail; no xpass change. STOP and report if the baseline
  differs.
- **Evidence (separately authorized):**
  `docs/governance/evidence/workstream7_actionable_validation_plan/`
  mirroring the Workstream 5/6 harness discipline — deterministic BASE
  artifacts generated from the RED commit and HEAD artifacts from the
  reviewed head; machine-readable summaries; the individually listed
  protected-test amendments; a machine token scan demonstrating that no
  technical method, specialist type, tool, laboratory, simulation,
  standard, threshold, or confidence score was invented; a nontechnical-
  inventor output review; a deterministic evidence validator; a SHA-256
  manifest.
- **Required BASE/HEAD fixture cases:** the canonical Workstream 1 journey;
  answered; unknown; deferred; provisional_assumption; pending_evidence;
  pending_specialist; a contradiction pair.

---

## 11. Stop conditions (non-waivable)

STOP immediately and report, without patching, if:

- any wording cannot be built from already-derived values;
- a step would be added or dropped, or the tie, IDs, or order would change;
- the Workstream 6 P5 assertion would need amendment;
- Section 13 or the landscape derivation would need modification;
- grouping or collapse would need redesign;
- any output would name or imply a specialist type, tool, laboratory,
  simulation, standard, threshold, or method;
- a Section 14 section-level key would be needed;
- a step-level key-set pin surfaces that blocks the additive `advisory`
  field (report for a separate owner decision);
- any protected assertion outside the §7 bounded list must change;
- `_s11` or any Section 11 surface would be touched;
- any wording or test would imply that D13 is satisfied.

---

## 12. Known limitations, closure, no-claim boundaries, and deferred items

### 12.1 Known limitations after completion (recorded, not solved)

Responsibility remains genuinely unassigned (no role or organization
model); confidence remains unmodeled (suppressed, not measured); validation
actions remain non-domain-specific (no procedures, thresholds, standards,
or methods); the pending advisories remain generic interim limitation
notices; the D13 capability gap remains open in full ("The appropriate
specialist has not yet been identified by the system." is a limitation
statement, not a referral); the Workstream 6 limitations L1–L5 remain as
recorded.

### 12.2 Closure criteria

Plan §12 in full — focused proof; accepted full regression against the
preserved baseline; regenerated deliverable evidence from the recorded
journey demonstrating absence of the demonstrated forms of defects 6 and 8;
independent read-only implementation and evidence reviews; explicit owner
closure authorization; §15/roadmap docs-only synchronization.

### 12.3 No-claim boundaries

Closure must not claim that validation planning is complete; that any check
was performed, passed, or validated; that responsibility was assigned; that
confidence was assessed; that specialist referral, routing, or
identification exists; that D13 is satisfied, partially satisfied, or
discharged by the generic advisories; that defect 9 was addressed; that all
electrical/electronic subdomains are supported; or that the remediation
program is complete.

### 12.4 Future deferred items (recorded, not implemented)

D13 — Technical Capability Gap Detection and Actionable Research Guidance
(MANDATORY FUTURE PRODUCT CAPABILITY — NOT CANCELLED — NOT SATISFIED BY
GENERIC SPECIALIST REFERRAL — SEPARATELY OWNER-GATED — NOT AUTHORIZED IN
WORKSTREAM 7), including its ten capability requirements and its future
Source Review checklist (§4 D13); domain-specific validation methods;
technical test procedures; measurements or thresholds; standards guidance;
specialist taxonomy; specialist routing; marketplace or referral services;
tool recommendations; simulation recommendations; laboratory
recommendations; product recommendations; capability disclosure by
electrical subdomain; confidence modeling; responsibility assignment;
Section 11 prototype deduplication (defect 9 — excluded per D2; requires
separate reproduction and owner gate if reopened); AI Coach; Answer
Clarification; persistence changes.

---

## 13. No-implementation and no-merge boundary

This contract authorizes nothing by itself. Recording, BASE RED,
implementation, independent reviews, merges, evidence, and closure are each
separately owner-gated. No PR produced under this contract may be merged
without explicit owner authorization. Workstream 7 is not activated by this
document; its lifecycle state remains NOT STARTED until the owner
authorizes the next gate. PR #167 and PR #162 remain outside this contract
and untouched. The AI Coach remains prohibited; Answer Clarification
remains inactive; persistence remains frozen; the official product state
remains `DEMO_READY_WITH_LIMITATIONS`; the MVP scope remains
electronics/electrical-only.
