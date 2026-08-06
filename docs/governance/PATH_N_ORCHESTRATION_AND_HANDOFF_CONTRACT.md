# PATH N ORCHESTRATION AND HANDOFF CONTRACT

STATUS: APPROVED AND FINAL — Level 2 architecture contract, in force as a governance constraint. Defines future-compatible structures only; implements nothing and activates no lane.
AUTHORITY LEVEL: Level 2 architecture contract under
docs/governance/TECHNICAL_REALIZATION_ANCHOR_COMPANION.md.
DEPENDS ON: anchor companion; MVP_SCOPE_FREEZE Amendment 1 carve-out.

This contract is prerequisite architecture, not a user-visible feature, and is
not itself the first lane. It defines future-compatible structures; it
implements nothing.

---

## 1. Orchestrated Idea Mode — what the platform leads

The **project participant using Orchestrated Idea Mode** describes, in plain
language: the invention idea, the problem, beneficiaries, desired
behaviour/outcome, operating environment, and constraints/preferences (cost,
size, runtime, connectivity, installation, usability). Guidance **adapts to the
participant's knowledge in the current domain and task**; the participant may be
technically knowledgeable in some domain yet still use this mode. The basic
journey must never require the participant to provide engineering parameters,
select components, write code, design circuits, perform calculations, use
unsupported specialist terminology, or coordinate specialists.

Within separately authorized bounded lanes, the platform progressively:
normalizes the idea; identifies involved domains; discloses capability (see §4);
converts plain-language answers into structured requirements; performs supported
technical work; maintains provenance and evidence status; and states clearly
what external technology, tool, laboratory, or specialist remains necessary and
how its result returns to the project.

**Cross-domain runtime transfer and orchestration remain unauthorized** unless a
separate bounded lane explicitly permits them. This contract defines only
future-compatible handoff structures for passing structured outputs between
domains. The proposed first bounded lane eligible for future authorization is
electronics-bounded and remains inactive until the complete governing activation
sequence is satisfied.

## 2. One coherent project storage architecture (reference model; mostly future)

Four bounded stores, unified by ONE shared project-identity model — not one
schema:
- **session store** — conversation, assessment, readiness, active workflow.
  Current reality: a paused, uncommitted, defect-bearing session-persistence
  implementation draft exists in the working tree as
  `inventorai-session-persist-v1`. It is not delivered, not active authority,
  and not evidence of an approved durable-session capability. A current
  session/idea identifier is distinct from a durable session store.
- **project record** — *future* identity, ownership refs, lifecycle, artifact
  refs (target architecture; not yet implemented);
- **artifact store** — *future* versioned decisions/artifacts/provenance/calcs/
  files/tool results/test evidence/revisions;
- **file/blob storage** — *future* large files.

Any conforming future session store MUST reference project and artifact
identifiers without becoming the artifact store itself. The paused, uncommitted
persistence draft is not evidence that this target reference relationship is
implemented. Persistence: PRESERVE UNMODIFIED AND PAUSE.

## 3. FDC-001 → Technical Realization handoff contract (`fdc-to-tr-handoff-v1`)

Project-scoped (one shared project-identity model across modes). Availability
class: [S] already-structured today · [F] free-text now · [D] bounded transform ·
[Q] new plain-language question · [X] verified external data · [C] deterministic
calculation · [K] specialist confirmation · [FUT] future target structure (not
yet implemented).

| Field | Class | Field | Class |
|---|---|---|---|
| current_session_id | [S] | future_project_identity | [FUT] |
| future_project_record_ref | [FUT] | source_session | [S] |
| normalized_problem | [F→D] | beneficiaries | [Q] |
| desired_outcome | [F→D/Q] | current_domain_context | [S] |
| candidate_domains | [D] | selected_domain | [D] (derived/confirmed) |
| structured_requirements | [F→D/Q] | constraints (+ constraint_strength) | [Q] |
| user_preferences | [Q] | assumptions | [S/F] |
| known_unknowns | [S] | evidence_map | [S→D] |
| unresolved_decisions | [Q] | capability_disclosures (support_status + authorization_status) | [D] |
| external_specialist_or_tool_requirements | [D/K] | safety_flags | [Q/K] |
| confirmation_records[] | [Q] | current_runtime_path_marker | [S] |
| normalized_invocation_mode_metadata | [S→D/FUT] | contributor_role_metadata | [FUT] |
| readiness_status | [D] | blocking_reasons[] | [D] |
| prohibited_claims | [S] | version / provenance | [S] |

Notes:
- **Domain:** `current_domain_context` is the current committed/default domain
  context (today a fixed electronics context — NOT an orchestrated
  domain-selection capability); `candidate_domains` is bounded inference;
  `selected_domain` is a derived or confirmed selection. Classify each by
  committed evidence; a fixed electronics default must not be represented as
  orchestrated domain selection.
- **Mode:** `current_runtime_path_marker` is the legacy runtime path value;
  `legacy_undesignated_current_behavior` does NOT prove Orchestrated Idea Mode is
  active. `normalized_invocation_mode_metadata` is the future normalized model
  ([S→D]/[FUT]); it is task/invocation metadata, not a permanent user identity.
- **Future structures:** stable project identity, project record, and
  contributor roles are [FUT]; not already implemented. Only the current session
  identifier exists today.

readiness_status (separate from blocking): `not_ready` ·
`ready_for_decision_preparation` · `ready_for_bounded_technical_realization`.
blocking_reasons[] (multiple simultaneous allowed): `missing_input` · `safety` ·
`authority` · `external_tool` · `specialist_review` · `unsupported_capability`.

## 4. Capability disclosure obligation (support vs authorization)

Before the platform creates any expectation of technical execution, it MUST, in
plain language, classify each piece of needed work and carry both dimensions,
each scoped per capability/operation/technology+version/lane:

- **support_status** ∈ `unsupported` · `partially_supported` · `supported` ·
  `unknown` · `stale` — whether (and how) the capability is technically
  supported by the platform/registry.
- **authorization_status** ∈ `not_authorized` · `authorized_for_disclosure_only`
  · `authorized_for_recommendation` · `authorized_for_execution` · `blocked` —
  whether the exact operation is authorized in the current lane.

Rules:
- absence of a verified registry/support record NEVER defaults to `supported`
  (it is `unknown`/`unsupported`);
- a supported capability is NOT executable unless the current lane authorization
  permits that exact operation (`authorized_for_execution`);
- `support_status` = `stale`, `unknown`, or `unsupported` must not be presented
  as supported; `support_status` = `partially_supported` must disclose the exact
  supported and unsupported boundaries and must not be presented as full support;
- `authorization_status` = `blocked` or `not_authorized` must not be presented as
  available for the affected operation.

The platform may state it **can perform a capability now only when it is both
supported and `authorized_for_execution` in the current lane AND its required
source/tool prerequisites are satisfied.** Disclosure classes: can-perform-now ·
can-partially-perform · can-only-recommend · requires-external-tool ·
requires-specialist · currently-unsupported. For external/unsupported items the
platform states what is missing, why it cannot perform it, which external
technology/specialist/laboratory/tool is required, and the re-entry path by which
the external result returns to the project with provenance. Capability disclosure
is NEVER permission for an unsupported claim.

## 5. Plain-language requirement translation (with constraint strength)

Each plain-language statement is translated into a structured technical
requirement or constraint with provenance back to the statement, and classified
by **constraint_strength**: `preference` · `soft_constraint` ·
`mandatory_constraint`. An option may be marked `eliminated` because of a
user-derived requirement ONLY when the relevant constraint is confirmed
`mandatory_constraint` (or another applicable governing decision policy permits
elimination). Preferences and soft constraints **qualify, rank, or defer**
options — they do not automatically eliminate them. Example: "I don't want wires
to the brake lever" → `installation_constraint =
no_physical_brake_control_connection`; once confirmed `mandatory_constraint`, a
wired brake-lever switch becomes `option_status=eliminated,
disposition_reason=requirement_conflict`.

## 6. Package assembly (bounded)

Authorized lanes may **contribute versioned artifacts toward future invention/
implementation packages**. **Full package assembly remains deferred** unless
separately authorized. No lane assembles a complete versioned invention or
implementation package by implication.

## 7. Collaboration and handoff (deferred target requirements only)

The architecture must not foreclose (recorded as deferred, NOT authorized):
project ownership; specialist contribution into an existing project; role-based
review; returning specialist output to the same project record; distinct owner
approval vs technical approval; artifact authorship; revision history. No
accounts/collaboration implementation is authorized.

## 8. Shared artifact name

The proposed first lane's authorized decision-readiness artifact, if that lane is
later activated, is named `adaptive-decision-readiness-v1` (mode-neutral,
shared-project). It does NOT imply a separate Path-N project schema or artifact
store.

## 9. Preserved states

All holds and closed states in the anchor companion §8 remain unchanged. Path T
remains BLOCKED.
