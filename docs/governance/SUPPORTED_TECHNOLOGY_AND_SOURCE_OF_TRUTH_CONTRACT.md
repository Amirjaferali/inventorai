# SUPPORTED TECHNOLOGY AND SOURCE-OF-TRUTH CONTRACT

STATUS: APPROVED AND FINAL — Level 2 architecture contract, in force as a governance constraint. Authorizes no registry population, capability, or lane.
AUTHORITY LEVEL: Level 2 architecture contract under
docs/governance/TECHNICAL_REALIZATION_ANCHOR_COMPANION.md.

ONE shared Supported Technology Registry and ONE source-of-truth rule for the
whole product; both Orchestrated Idea Mode and the future Direct Technical Work
Mode use the same registry and rules. No duplication.

---

## 1. Distinct technology-status dimensions

Registry presence never implies support; support never implies lane
authorization. A technology carries separate dimensions:
- **registry_lifecycle_status** — registry lifecycle position (see §2);
- **registry_verification_status** — whether/when the entry was verified, recorded
  separately from lifecycle (see §2);
- **support_qualification_record** — the internal governed proof of supported
  versions/use-cases/toolchain/boundaries/maturity and its evidence (see §3); NOT
  regulatory or accredited certification;
- **support_qualification_status** — the lifecycle/status of that qualification
  record (see §3);
- **support_status** — current support state (see §2);
- **capability_authorization** and **lane_authorization** — see §8, scoped per
  §8.1.

A technology may be registered and verified but only partially supported, or
supported but not authorized in the current lane. Registry presence must never
imply capability activation or lane authorization. **Absence of a verified
support record never defaults to `supported`.**

## 2. Separate registry lifecycle, verification, and support status

`registry_lifecycle_status` (registry lifecycle position): `proposed` ·
`under_review` · `active` · `deprecated` · `suspended` · `stale` · `retired`.

`registry_verification_status` (verification state, recorded separately from
lifecycle; a `registry_verification_history[]` of prior verification events may
also be retained): `unverified` · `verified` · `verification_stale`. A single
lifecycle enum must NOT simultaneously contain `verified` and `active` —
verification is a distinct dimension from lifecycle position.

`support_status` (current support state): `unknown` · `unsupported` ·
`partially_supported` · `supported` · `suspended` · `stale`.

These are separate vocabularies. A technology may remain
`registry_lifecycle_status=active` while `registry_verification_history[]` records
an earlier `verified` event, and the current `registry_verification_status` and
`support_status` independently reflect their present states. A
previously verified entry must NOT remain current after its documentation,
version, toolchain, license, or support boundary changes — lifecycle,
verification, and support move to
`stale`/`deprecated`/`suspended`/`retired`/`verification_stale` accordingly.

## 3. Support qualification (internal; not accredited certification)

`support_qualification_record` is the governed internal evidence record
establishing: supported technology versions; supported use cases; supported
toolchain; supported generation boundaries; supported verification boundaries;
support maturity; qualification evidence; qualification date and version;
authority reference. **This internal qualification is not regulatory or accredited
certification.**

`support_qualification_status` is the distinct lifecycle/status of that record:
`proposed` · `qualified` · `suspended` · `invalidated` · `superseded` · `stale`.
The record and its status are separate dimensions; neither term may be used as the
other.

Registry-entry metadata: technology_id; technology_category; supported_versions /
applicable_version_range; official_documentation reference; manufacturer/
maintainer; last_verification_date; verifier_or_verification_process;
deprecation_or_suspension_reason; replacement_or_migration_reference.

## 4. Licensing and legal-use metadata (verified scope only)

Where applicable, each entry distinguishes: license name and version;
authoritative license reference; commercial-use permission; modification
permission; redistribution permission; source-disclosure obligations;
attribution obligations; dependency-license compatibility; generated-output or
embedded-code restrictions; trademark/branding limitations; jurisdiction or
market limitations; verification date and evidence. A registry entry records
**usability only within its verified scope**; it is **not a universal legal
guarantee and not legal advice**. No unauthorized copying; technologies are added
progressively, each by separate authorization.

## 5. Source, claim, and evidence (separate dimensions)

Separate three dimensions:
- **source_type** — where the information came from: `applicable_law_or_regulation`
  · `recognized_standard_requirement` · `official_certification_requirement` ·
  `verified_manufacturer_fact` · `manufacturer_document` · `platform_tool` ·
  `specialist_reviewed_conclusion` · `user_preference` · `user_observation` ·
  `user_measurement` · `explicit_platform_inference` · `unverified_model_suggestion`.
- **claim_type** — what kind of statement/result it is: e.g. `electrical_limit` ·
  `compatibility` · `calculated_result` · `measurement` · `test_result` ·
  `regulatory_requirement` · `recommendation`.
- **evidence_status** — how strongly established: e.g. `advisory` · `reproducible`
  · `verified` · `inconclusive`.

Examples: (source_type=manufacturer_document, claim_type=electrical_limit,
evidence_status=verified); (source_type=platform_tool, claim_type=calculated_result,
evidence_status=reproducible). For each source_type, the evidence required before
it may be treated as verified must be defined (e.g. a user measurement becomes a
verified measurement only with recorded method + instrument + reproducibility).

## 6. Hard promotion rule

A technical value originating ONLY from model memory (`unverified_model_suggestion`)
remains advisory and may NEVER be promoted to: verified fact · calculated result
· selected component · technically_selected decision · frozen configuration · or
any safety-relevant conclusion.

## 7. Claim-specific conflict policy (not one fixed linear hierarchy)

There is **no single universal precedence chain**. Each conflict is resolved by a
**claim-specific policy** evaluating: legal/regulatory authority; applicability to
the product, jurisdiction, use case, and version; source scope; recency; evidence
quality; reproducibility; independence; verified inputs; safety relevance.
- Applicable law or mandatory regulation may override optional standards.
- Manufacturer limits, system requirements, calculations, and standards are often
  **different simultaneous constraints**, not mutually exclusive competing answers
  — all applicable constraints hold at once.
- A source that is stale, version-mismatched, jurisdictionally inapplicable, or
  outside its scope must NOT prevail merely because of its source category.

## 8. Four distinct technology authorizations

These are distinct; no earlier level automatically grants a later one:
1. **registry-entry approval** — permits recording a technology and its evidence;
2. **platform support qualification** — establishes exact supported versions, use
   cases, toolchain, generation/verification boundaries, and maturity;
3. **capability authorization** — permits a specific capability (generation,
   calculation, static analysis, compilation, simulation);
4. **lane authorization** — permits that capability to be invoked within a
   specific bounded lane.

Adding or verifying a technology entry must NOT activate generation, verification,
or lane use.

### 8.1 Authorization scoping record

`authorization_status` is NOT one broad property of a technology. Its complete
canonical vocabulary is: `not_authorized` · `authorized_for_disclosure_only` ·
`authorized_for_recommendation` · `authorized_for_execution` · `blocked`.
Authorization is scoped by a record: technology_id; technology_version;
capability_id; operation; lane_id; authorization_status; authority reference;
activation date/version; constraints and expiration where applicable. A technology
may be `authorized_for_disclosure_only` or `authorized_for_recommendation` but not
for generation, compilation, simulation, or another operation.

`authorized_for_execution` is scoped to the exact
technology/version/capability/operation/lane record; it is NOT a blanket
authorization for the technology. An authorization expires, is revoked, or becomes
ineffective when its authority, support qualification, scope, version, or
prerequisites are no longer valid.

## 9. Support-qualification invalidation and downstream effect

A `support_qualification_status` may become `suspended` · `invalidated` ·
`superseded` · `stale`. When this occurs:
- affected capability authorizations must be re-evaluated;
- affected lane authorizations must be re-evaluated;
- the capability must not be presented as currently available;
- affected downstream artifacts/decisions must be reviewed under the Evidence and
  Artifact Model;
- version-mismatched or stale support evidence cannot support current execution.

No lane may continue invoking a capability merely because it was supported in an
earlier version.

## 10. Technology neutrality

This contract is technology-neutral. No technology family, vendor, platform, or
tool receives preference, support, or authorization by mention or implication.
Every technology requires its own verified registry entry, support qualification,
capability authorization, and lane authorization as applicable.

## 11. Preserved states

All holds and closed states remain unchanged. Path T remains BLOCKED. This
contract authorizes no registry population, no calculation engine, and no
generation.
