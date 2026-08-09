# P7-I3 — CANONICAL EXPORT + LOCAL/REFERENCE ADAPTER PROOF — BOUNDED INCREMENT CONTRACT

**Repository status of THIS document:** **CANONICAL P7-I3 CONTRACT PUBLICATION CANDIDATE (corrected)** —
**PENDING independent pre-merge contract re-review, Owner acceptance, merge, and post-merge
verification.** It is **NOT** finally established for implementation. Under the Owner's **Standing
Phase-7 Authorization** (`D-P7-STANDING-01`), P7-I3 implementation **MUST NOT begin** until the
required pre-merge review sequence completes (Permanent Execution-Gate Safety Lock). This corrected
candidate supersedes `51b8fc65a298324f69d7c12d29b158788217ecad` (independent verdict **B — required
pre-merge corrections**; preserved as evidence, **DO NOT MERGE**); it integrates the five required
corrections and preserves every independently-accepted decision.

- **Authority:** `D-P7-STANDING-01`; contract-of-record P7-C (`docs/governance/PHASE_7_API_AND_INTEGRATION_FOUNDATION_P7C_CONTRACT.md`, `D-P7C-01`).
- **Basis tip (verified read-only):** `3cb5dcd388bda700f93667800376ee49b7fb6fa6` (P7-I2 closure merge PR #407; tree `d1094d3`).
- **P7-I1 / P7-I2:** FORMALLY CLOSED. **P7-I3:** NOT STARTED. **Phase 7:** OPEN. **Implementation Gate Lock:** ACTIVE.

## 1. Purpose and scope

P7-I3 is the bounded, **outbound-only, non-mutating** proof that a canonical export produced from the
established P7-I1/P7-I2 foundations can be transferred through a **local/reference adapter boundary**
without coupling InventorAI Core to a specific vendor or application. Architecture:
InventorAI Core → **Canonical Output Model (P7-I1 Structured Export)** → **Integration/Export Layer
(P7-I3 adapter boundary)** → External Tools. This increment is **NOT** a real external-vendor
integration and vendor connectors remain future work.

## 2. Mandatory first-proof shape (frozen)

*Canonical export → local/reference adapter → transformed representation → validation / inverse-equivalence
performed entirely OUTSIDE governed project-state mutation.* The proof **MUST NOT**: import results back
into project state; mutate project state; modify progression/refinement; write external results as
evidence; activate a domain; automatically trust adapter output; select a real vendor; introduce webhook
ingestion; introduce async external-job infrastructure.

## 3. Canonical export source + source-version provenance (CORRECTED — no invented version)

P7-I3 **consumes the canonical P7-I1 Structured Export payload** — `engine.read_export_service.produce_project_export(store, project_id, account_id)`,
whose deterministic dict is `{ idea_id, domain_support_state, assertion_count, validation_summary,
provenance_summary, assertions:[{record_id, disposition, provenance, validation_status}] }`. **No second
canonical export/output model is created.**

Repository truth (verified): the **P7-I1 Structured Export has NO independent canonical export-version
identity** (IR-6 deliberately deferred that decision); the only established export version identity is
P7-I2's public **`export_contract_version`**. Therefore:
1. P7-I3 consumes the canonical P7-I1 Structured Export payload.
2. P7-I3 **MUST NOT** invent a new internal export version identity — no `internal_export_version`,
   `adapter_export_version`, P7-I1 version constant, or new output-contract version (would require a
   separate future decision).
3. Source provenance identifies the canonical source **truthfully as the "P7-I1 Structured Export seam"**,
   and **may additionally carry explicit source contract/version metadata supplied by the integration/
   export boundary or caller**.
4. Where the payload originated through the P7-I2 public export surface, the existing P7-I2
   `export_contract_version` **may** be supplied as source contract metadata.
5. The P7-I2 public HTTP envelope is **not required** to become the canonical adapter payload source.
6. **Unsupported-version failure semantics apply ONLY where explicit source version metadata is supplied.**
7. If no explicit version metadata is presented, **canonical-input structural/semantic validation governs.**

If the canonical export proves insufficient for the adapter proof → STOP and report; do not create a
parallel output model or a new version owner.

## 4. Local/reference adapter (P7-I3 NEW BOUNDED RESPONSIBILITY)

A **local, deterministic, test-harness-quality reference adapter** (no external network; not a production
vendor connector) proving: canonical input accepted; a defined deterministic transformation occurs; the
transformed representation is structurally valid; transformation provenance is identifiable; a governed
inverse/equivalence check proves the adapter did not silently alter canonical meaning beyond its declared
transformation; and InventorAI project state remains unchanged.

## 5. Adapter contract + mandatory semantic preservation floor (CORRECTED)

Minimal adapter interface: `adapter_id`; `adapter_version`; input = canonical Structured Export (§3);
declared `output_type`; `transform` (pure, deterministic, no store/project access); transformation
provenance (§8); validation result (§6); failure semantics (§7); **no project mutation**. Not a plugin
system, adapter manager, orchestrator, registry, workflow engine, or marketplace (D-FPC-MAP-06).

**Mandatory semantic preservation FLOOR (contract-owned; NON-EMPTY; not derived from the transformed
output, the adapter's self-description, or runtime caller preference).** Every P7-I3 reference adapter
**MUST** preserve at minimum, equivalently recoverable/validatable:
- **Top level:** `idea_id`, `domain_support_state`, `assertion_count`.
- **Per assertion:** `record_id`, `disposition`, `provenance`, `validation_status`.

An adapter MAY preserve more fields; it **MAY NEVER** reduce or remove this floor. Intentional
structural/format transformation is allowed, but the floor's semantic values must remain equivalently
recoverable and validatable. **Deterministic ordering:** transformed rows derive deterministically from
the canonical assertions ordering (or another explicitly deterministic normalization); the proof must not
depend on accidental Python dict ordering — reordering is acceptable only if the validator normalizes it
explicitly.

## 6. Validation / inverse-equivalence + integrity/tamper protection (CORRECTED)

The governed check is a **semantic** inverse/normalized-projection comparison of the transformed
representation against the canonical source on the mandatory floor (§5) — **not** raw byte equality — and
it must be **independent enough to detect adapter corruption** (the validator must NOT simply reuse the
transform, or it would share the same bug). Result vocabulary is a **minimal bounded binary**
(`valid` / `invalid` or equivalent) — no workflow state machine.

The validator **MUST fail** when:
- **A.** an assertion is missing;
- **B.** an assertion is duplicated;
- **C.** a `record_id` collision would cause a flattened mapping to overwrite/merge rows (the
  adapter/validator MUST detect collision/duplication rather than silently collapsing rows into a dict
  keyed by `record_id` — note repository truth: `ProjectRecordContract.validate()` does **not** guarantee
  `record_id` uniqueness strongly enough for this proof; a duplicate `record_id` must never overwrite a
  prior row and still pass);
- **D.** `assertion_count` ≠ the transformed assertion population;
- **E.** `validation_summary` is inconsistent with the transformed assertion rows;
- **F.** `provenance_summary` is inconsistent with the transformed assertion rows;
- **G.** any mandatory preservation-floor field changes unexpectedly.

**Summary consistency:** where the transformed representation carries `assertion_count` /
`validation_summary` / `provenance_summary`, equivalence must **independently derive/check** their
consistency against the transformed assertion **rows** (not merely compare top-level summary values to the
original summary while ignoring the rows).

**False-green guards (binding on the RED plan and implementation):** proof tests consume the **real**
P7-I1 export (not a hand-constructed fake canonical input); the validator derives its check independently
of the transform; the preserved-field set is the contract floor (never taken from the transformed output);
a missing assertion is never silently ignored; a duplicate/collision is never silently overwritten;
summaries are checked against rows; equivalence can **never** succeed with an empty preservation set.

## 7. Failure semantics (bounded, explicit, non-mutating)

Safe behavior for: invalid canonical input; unsupported canonical version (only when explicit source
version metadata is supplied, §3.6); adapter transformation error; validation/inverse-equivalence failure;
unsupported output type; malformed adapter result. Every failure **must**: not mutate project state; not
silently fall back; not mark external output as trusted; and return/raise a **bounded explicit failure**.

## 8. Provenance (integration metadata, not project truth)

Adapter output carries/exposes: the truthful canonical source identity (**"P7-I1 Structured Export seam"**,
plus any explicit source contract/version metadata supplied — e.g. P7-I2 `export_contract_version` when
the payload came through the public surface); `adapter_id`; `adapter_version`; validation status; and a
transformation time **only if** deterministic-testability permits (default: omit). **Adapter provenance is
integration/export metadata — it does NOT mutate project evidence/provenance.**

## 9. Inbound-trust invariant (binding)

Any external/adapter result is **UNTRUSTED BY DEFAULT**. P7-I3 must NOT satisfy validation automatically,
prove safety, prove feasibility, change maturity/progression, alter evidence disposition, become canonical
project truth, or activate a domain. Inbound persistence/review remains a **separate** evidence gate.

## 10. Non-mutation

Non-mutating. Behavioral tests prove project state is unchanged after (a) successful transformation,
(b) failed transformation, and (c) validation failure — via canonical state comparison
(`store.load_contract(project_id).to_json()` equality), **not** raw database-byte equality. The
inverse/normalized projection is **validation-only and never writes state**.

## 11. P7-I2 relationship / public-API boundary

P7-I3 does **NOT** expand the public API; the proof consumes the internal canonical export seam directly;
no new public endpoint. **If a public integration endpoint seems necessary → STOP and justify.**

## 12. D-FPC-MAP-06 ownership map

| Element | Classification |
|---|---|
| P7-I1 Structured Export (`produce_project_export`) | ALREADY OWNED — CONSUME |
| P7-I2 public export (`web/api_v1.py`, `export_contract_version`) | ALREADY OWNED — optional source metadata only if relevant; do not duplicate |
| `ProjectRecordContract` | ALREADY OWNED |
| Domain Registry / `domain_activation` | ALREADY OWNED — DO NOT TOUCH |
| Adapter contract | P7-I3 BOUNDED RESPONSIBILITY |
| Reference adapter | P7-I3 BOUNDED RESPONSIBILITY |
| Equivalence validator | P7-I3 BOUNDED RESPONSIBILITY |
| Adapter registry / Integration Orchestrator / Plugin framework | MUST NOT EXIST |

No duplicate service layer, canonical output model, orchestrator, registry, plugin platform, adapter
manager, or workflow engine.

## 13. Likely implementation paths (discovery only — NOT edited here)

| Path | Current owner | Why P7-I3 may need it | Modification |
|---|---|---|---|
| one small adapter module (e.g. `engine/export_adapter.py`, name not frozen) — adapter contract/protocol + local/reference adapter + independent equivalence validator | new | the P7-I3 adapter boundary + deterministic transform + integrity/equivalence check consuming the P7-I1 export | REQUIRED |
| one focused test module (`tests/test_p7_i3_export_adapter.py`, name not frozen) | new | behavioral RED→GREEN + integrity/non-mutation/failure evidence | REQUIRED |
| `web/app.py` / `engine/account_store.py` / public API (`web/api_v1.py`) | — | — | **NONE expected** |

Expected footprint ≈ 2 paths. No public API / account-store / web/app.py change; no vendor SDK; no
network; no persistence/import. If the source-version correction appears to require a new canonical
version module → STOP (it should not; explicit source metadata is supplied at the boundary without a new
version owner).

## 14. RED→GREEN plan (behavioral, false-green-resistant; CORRECTED — full list)

RED (not arbitrary module naming): (1) **real** P7-I1 canonical export accepted (consumed, not a
hand-built fake); (2) structurally distinct transformed representation; (3) deterministic transform;
(4) adapter identity/version/output-type/provenance present; (5) mandatory preservation floor survives;
(6) valid equivalence succeeds; (7) a changed mandatory-floor field fails; (8) a missing assertion fails;
(9) a duplicated assertion fails; (10) a `record_id` collision fails bounded (no silent overwrite);
(11) `assertion_count`/row-population inconsistency fails; (12) `validation_summary`/rows inconsistency
fails; (13) `provenance_summary`/rows inconsistency fails; (14) malformed transformed representation fails;
(15) unsupported explicit source version fails **when version metadata is supplied**; (16) malformed
canonical input fails; (17) transform failure fails safely; (18) project state unchanged after success;
(19) project state unchanged after transform failure; (20) project state unchanged after validation
failure; (21) the inverse/normalized projection is validation-only and never writes state; (22) no
network; (23) no public API expansion; (24) no inbound import; (25) no external-result trust; (26) no
domain activation; (27) the P7-I1 canonical export is consumed, not duplicated; (28) no vendor dependency;
(29) no adapter registry; (30) no Integration Orchestrator; (31) no plugin framework. No broad
`pytest.raises(Exception)`; no manufactured breakage; existing tests unchanged; the validator must not
share the transform's implementation.

## 15. STOP conditions

STOP and report if: the canonical export is insufficient; the proof would require a second output model or
a new export-version owner; a real vendor must be selected (separate Owner decision); a public endpoint
appears necessary; the proof would import/trust adapter output as evidence or mutate project state; the
transform cannot be made deterministic/testable without network; implementation would exceed §13; or a
plugin/orchestrator/registry/manager appears.

## 16. P7-C obligation classification (P7-I3) (CORRECTED)

| Obligation | Classification for P7-I3 |
|---|---|
| Adapter contract | DELIVERED BY P7-I3 IF IMPLEMENTED (minimum) |
| Canonical export (consumed) | ALREADY DELIVERED (P7-I1/P7-I2); consumed here |
| External-tool transfer proof (local/reference) | DELIVERED BY P7-I3 IF IMPLEMENTED |
| Provenance (integration/export metadata) | DELIVERED BY P7-I3 IF IMPLEMENTED |
| Failure semantics | DELIVERED BY P7-I3 IF IMPLEMENTED |
| Validation / inverse-equivalence + integrity | DELIVERED BY P7-I3 IF IMPLEMENTED |
| **Reference / Test Harness** (local, deterministic, outbound-only, non-mutating, reference/test quality) | **DELIVERED BY P7-I3 IF IMPLEMENTED** |
| **Partner / External-Integration Sandbox** (distinct later obligation) | **DEFERRED** — not delivered/claimed by the reference adapter |
| **File Exchange** (governed file serialization/exchange) | **DEFERRED / NOT DELIVERED BY P7-I3** (an in-memory DTO/dict is not file exchange; no file writing added here) |
| Retries/timeouts | NOT APPLICABLE (no network/vendor) |
| Secrets | NOT APPLICABLE (no credentials) |
| Webhooks / inbound import / partner connectors | DEFERRED (separate gates) |
| Monitoring | DEFERRED (audit ≠ monitoring) |
| Async | DEFERRED |

**Nothing is classified as Phase-7 complete.** The §25 Remaining-Obligation / Exit-Criteria Review remains
reserved before P7-CLOSE.

## 17. Acceptance criteria

- **CANONICAL EXPORT CONSUMED:** the reference adapter takes the real P7-I1 Structured Export (no new model, no fake input in proof tests).
- **REAL ADAPTER BOUNDARY:** transformed representation structurally distinct (not identity); deterministic.
- **MANDATORY FLOOR:** the §5 floor is preserved and validated; equivalence cannot pass with an empty/reduced set.
- **INTEGRITY:** missing/duplicate assertions, `record_id` collisions, and `assertion_count`/`validation_summary`/`provenance_summary` inconsistencies all fail (§6 A–G); validator independent of the transform.
- **SOURCE PROVENANCE (truthful):** identifies the P7-I1 export seam + any explicit supplied source contract/version metadata; no invented export version.
- **FAILURE SEMANTICS:** bounded explicit failure; no mutation; no silent fallback; output never trusted.
- **NON-MUTATION:** project state unchanged after success, transform failure, and validation failure (canonical comparison).
- **NO VENDOR / NO NETWORK / NO PUBLIC API / NO INBOUND IMPORT / NO DOMAIN ACTIVATION / NO FILE WRITE.**
- **D-FPC-MAP-06 · LEAN:** consume canonical export; ≈2 new paths; no duplicate framework/registry/orchestrator.
- **TESTS:** behavioral RED→GREEN (§14, false-green-resistant); full regression green; existing tests unchanged.

## 18. Status (this corrected candidate)

P7-I3 CONTRACT: CORRECTED PUBLICATION CANDIDATE — PENDING INDEPENDENT PRE-MERGE RE-REVIEW; NOT FINALLY
ESTABLISHED. Supersedes `51b8fc6` (evidence only, DO NOT MERGE). P7-I3 IMPLEMENTATION: NOT STARTED;
Implementation Gate Lock ACTIVE. Phase 7: OPEN. The §25 Phase-7 Remaining-Obligation / Exit-Criteria
Review remains RESERVED (not performed here); PSRR remains a future governance registration after Phase-7
formal closure (not started here). No code/tests/adapters created.
