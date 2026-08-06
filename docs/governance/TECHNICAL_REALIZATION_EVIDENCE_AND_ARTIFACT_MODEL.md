# TECHNICAL REALIZATION EVIDENCE AND ARTIFACT MODEL

STATUS: APPROVED AND FINAL — Level 2 architecture contract, in force as a governance constraint. Authorizes no generation, calculation, or selection.
AUTHORITY LEVEL: Level 2 architecture contract under
docs/governance/TECHNICAL_REALIZATION_ANCHOR_COMPANION.md.

One shared evidence/artifact model for the whole product. The system must never
collapse statuses into a vague "complete." A record carries values in MULTIPLE
independent dimensions simultaneously.

---

## 1. Independent state dimensions

Do not merge these into one vocabulary:

- **decision_status**: `candidate` · `recommended` · `owner_preferred` ·
  `technically_selected` · `frozen`.
- **artifact_origin_status**: `captured` · `inferred` · `calculated` ·
  `generated`.
- **verification_stage**: `static_analysis` · `compilation` · `simulation` ·
  `assembly` · `bench_test` · `field_test` · `demonstration` ·
  `specialist_review` · `certification`.
- **verification_outcome**: `pass` · `fail` · `inconclusive` · `not_run`.
- **currency_status**: `current` · `superseded`.
- **validity_status**: `pending` · `valid` · `stale` · `invalidated` ·
  `withdrawn` · `reopened`.
- **option_disposition**: see §2.

A single artifact may simultaneously be origin=`generated`,
verification_stage=`compilation`, verification_outcome=`pass`. Do NOT force a
mutually exclusive choice between "generated" and "compile-verified". Where a
single `artifact_evidence_status` term is referenced elsewhere, it is defined as
the composite of these independent dimensions, not a single mutually-exclusive
value.

`technically_selected` is the ONLY technical-selection state identifier (no
`selected` / `technical_selected` variants).

Currency vs validity: `current` means the latest applicable version, NOT that the
artifact is technically valid; a `current` artifact may still be `pending`,
blocked, failed verification, or inconclusive. A `superseded` artifact may remain
valid historical evidence for its own version but is not current for downstream
reliance.

## 2. OPTION DISPOSITION (separate, structured)

- option_status: `active` · `eliminated` · `deferred` · `blocked`;
- disposition_reason: `requirement_conflict` · `constraint_conflict` ·
  `verified_incompatibility` · `safety_conflict` · `regulatory_conflict` ·
  `missing_evidence` · `owner_rejection` · `superseded_by_better_option`;
- evidence_reference: the requirement/constraint/fact that drove the disposition;
- constraint_strength of the driving requirement: `preference` ·
  `soft_constraint` · `mandatory_constraint`. Final elimination for
  requirement_conflict requires a confirmed `mandatory_constraint` (or another
  applicable governing rule); preferences/soft constraints qualify or rank.

Do NOT create compound status names (e.g. "recommended_with_conditions",
"eliminated_by_requirement") as statuses. Conditions and dispositions are
structured data, not status strings.

## 3. RECOMMENDATION CONDITIONS (structured, attached to `recommended`)

`decision_status = recommended` may carry `conditions[] = [...]` (e.g.
`[calibration_required, physical_test_required]`). Conditions are data attached
to the status — never a separate or compound status.

Example (structured):
```
decision_status   = recommended
conditions        = [calibration_required, physical_test_required]
currency_status   = current
validity_status   = pending

option_status     = eliminated
disposition_reason= requirement_conflict
constraint_strength= mandatory_constraint
evidence_reference= installation_constraint:no_physical_brake_control_connection
```

## 4. Two distinct decision gates (evidence vs approvals)

Evidence and approvals are distinct. Manufacturer facts and system evidence are
**evidence**, not approvals.

**A. Technical-selection gate** — an option may receive
`decision_status = technically_selected` ONLY when BOTH its required evidence
gates AND its required approvals for its type/risk are satisfied. These are
distinct, and evidence is not approval:
- **required evidence gates**: manufacturer evidence; deterministic calculation
  evidence; compatibility evidence; safety evidence; source-of-truth requirements;
- **required approvals**: technical approval; safety-specialist approval;
  regulatory approval; and any other authorized approval required by decision
  type/risk.
`owner_preferred` is chosen among **currently eligible, non-disqualified,
non-blocked** alternatives and **does not prove technical validity**. A
safety-critical or regulated option must NOT become `technically_selected` while
its required specialist or regulatory approval remains pending.

**B. Freeze-approval gate** — a `technically_selected` option may become the
downstream baseline (`frozen`) ONLY with: all technical-selection approvals;
explicit baseline approval; fixed version and provenance; recorded downstream
dependencies; no unresolved blocking_reasons.

Conditional ordering: when multiple technically valid options remain and the
difference depends on participant priorities, `owner_preferred` is REQUIRED before
`technically_selected`; when technical evidence determines a single valid option
and no preference is material, the system MAY advance directly
`recommended → technically_selected`. Owner preference may set
preference/trade-offs/budget/usability/direction; it may NEVER override verified
incompatibility, safety, regulation, deterministic calculation, manufacturer
limitation, or missing required evidence.

## 5. Approval records (structured; no generic Boolean)

No generic `project_approved` flag. Three distinct collections are kept separate:
`required_evidence_gates[]` (evidence-state/gate evidence); `approval_requirements[]`
(what approvals are required); and `approval_records[]` (approvals actually
granted). System evidence-gate completion is **evidence-state/gate evidence, not a
human or regulatory approval**; a separate human approval may rely on that evidence
but remains a distinct record. Approval records carry: `approval_type`;
`approver_role`; `authority_basis`; `scope`; `decision_version`;
`evidence_references`; `approval_status`; `timestamp`; expiry/review date where
applicable. Distinguish: human or specialist approval; regulatory approval;
manufacturer evidence (evidence, not approval); external certification evidence
(§7). Approval types drawn from at least: `owner_approval` · `technical_approval`
· `safety_specialist_approval` · `regulatory_approval` — `system_evidence_gate_completion`
is NOT an approval type (it is an evidence gate). Owner preference alone must NEVER
freeze a technically unsafe or insufficiently evidenced decision.

## 6. Execution-evidence (origin + stage + outcome) — prohibited readings

| Stage / origin | Required evidence | Prohibited interpretation |
|---|---|---|
| origin=captured | participant-stated | "verified" |
| origin=inferred | platform derivation + provenance | "fact" |
| origin=calculated | reproducible calc from verified inputs | "measured" |
| origin=generated | artifact produced | "verified/tested" |
| stage=static_analysis (pass) | analyzer pass | "compiles" |
| stage=compilation (pass) | toolchain success | "works/simulated" |
| stage=simulation (pass) | sim run + settings recorded | "physically demonstrated" |
| stage=assembly | physical build evidence | "tested" |
| stage=bench_test (pass) | bench result | "field-proven" |
| stage=field_test (pass) | field result | "production-ready" |
| stage=demonstration | repeated success evidence | "certified" |
| stage=specialist_review | specialist sign-off | "certified" |
| stage=certification | external certification evidence (§7) | — |

## 7. Certification requires external certification evidence

No internal approval (owner/technical/safety/regulatory/system) creates a
certification. Certification requires **external certification evidence**, bound
to: exact artifact/product/configuration version; certified scope; authorized/
accredited issuing body; certificate reference/identifier; issue date; validity
period (expiry); suspension/revocation state; verification reference. Internal
approval may authorize recording or relying on a valid certificate, but cannot
create certification. Certification lifecycle is tracked by a separate
`certification_status` ∈ {`valid` · `expired` · `suspended` · `revoked` ·
`superseded`}; this lifecycle must NOT be forced into the generic
`verification_outcome` vocabulary.

## 8. Verification and failure outcomes (structured)

Each verification stage is recorded **separately from its outcome**; a stage that
merely occurred is never treated as successful. Where a tool, calculation,
compilation, simulation, or test is executed, record: `verification_stage`;
`verification_outcome` ∈ {`pass` · `fail` · `inconclusive` · `not_run`}; the
evidence and inputs; the affected version. Stages whose lifecycle is not captured
by the generic outcome vocabulary use separate stage-specific status fields rather
than overloading `verification_outcome` — e.g. `specialist_review_status` and
`certification_status` (§7) — so that assembly, demonstration, specialist review,
and certification are never implied successful merely because the stage occurred. A
`fail` carries structured context: `failure_type` · `failure_stage` ·
`failure_scope` · `failure_evidence` · `recoverability`. A failed test remains a
**valid evidence record of the failed outcome** (it is a `verification_outcome`,
not a `validity_status`): this validates the evidence record, not the tested
subject; it may block downstream reliance and does not establish technical
validity; and it must not be confused with an invalid or missing artifact. Currency,
validity, provenance, and affected-version references are preserved.

`specialist_review_status` ∈ {`pending` · `completed` · `inconclusive` ·
`withdrawn`} records the state of the specialist-review process only; it does not
itself create technical, safety, regulatory, or other approval. Any approval
resulting from specialist review must be recorded separately in `approval_records[]`,
and the specialist conclusion must retain provenance and evidence references.
`specialist_review_status` must NOT be used as a substitute for
`verification_outcome` or `approval_status`, and must not take `approved` or
`rejected` values (approval decisions belong in structured approval records).

## 9. Dependency-validity rules (dimension-consistent)

Statuses across different dimensions do not form one universal strength ordering.
A downstream artifact cannot be relied upon when a required upstream dependency
has:
- `validity_status` = `stale`, `invalidated`, or `withdrawn`;
- `currency_status` = `superseded` without an approved migration;
- `verification_outcome` = `fail`, or `inconclusive` where `pass` is required;
- unresolved blocking reasons; or
- missing required evidence or approval.
Each claim must satisfy the evidence requirements specific to that claim;
dependency effects must preserve provenance and version history.

**Staleness cascade is a required FUTURE behaviour, not a current capability
claim:** any conforming implementation MUST mark affected downstream artifacts
`validity_status=stale` (recording the triggering change in provenance) when an
upstream requirement, decision, component, calculation, or configuration changes.
This is an architectural requirement and is NOT evidence that the current runtime
implements automatic dependency propagation. A lane may claim this behaviour only
after separately authorized implementation and verification.

## 10. Preserved states

All holds and closed states remain unchanged. Path T remains BLOCKED. This model
authorizes no generation, calculation, or selection by itself.
