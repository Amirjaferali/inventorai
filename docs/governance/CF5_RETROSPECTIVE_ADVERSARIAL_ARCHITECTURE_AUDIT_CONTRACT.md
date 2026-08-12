# CF-5 — Retrospective Adversarial Architecture Audit — Governance Contract / Entry (Candidate)

**Status of THIS record:** governance/documentation-only **CONTRACT / ENTRY CANDIDATE**. It becomes AUTHORITATIVE only if this
exact accepted candidate is independently reviewed (Mandatory Grill → independent external exact-candidate review), Owner-accepted,
published SHA-preserving, merged (create-a-merge-commit), and post-merge verified. **Until then it authorizes nothing.** It defines
the entry, scope, finding taxonomy, validation, correction-gate policy, and completion criteria for the mandatory **CF-5 —
Retrospective Adversarial Architecture Audit**. **It does NOT execute the Audit, produce findings, select/qualify/activate any
domain, execute CF-6 / CF-2 / CF-3 / P9-QS qualification / D4 / D8, start Phase 10 / PSRR, or authorize deployment/production.**
**GOVERNANCE-ONLY CONTRACT GATE — DOCUMENTED NO-VALID-RED.** Expected engine / web / CLI / domains / Domain Registry / activation /
schemas / persistence / API / architecture-guardrail / test diff: **ZERO**.

**Authoritative base:** `54a5565bdcdfa37ff247ceb9e806bd5b2b42cb9d` (PR #446 — P9-E2 formal-closure merge; parents
`f33663710d6edf506a082b1bfa2f02e9c3fef7ac` + accepted P9-E2 closure candidate `23f746faac311b9712e298fa7ba929aa2a5c3541`; merge
tree `cf4198c567fd5f9df20b67e7f1510956500d2ae1`), verified read-only before editing; boot OK; `activated_domains() ==
['electronics_electrical']`; 0 newer.

**Subordinate to** CLAUDE.md and the committed anchors. Reuse existing canonical owners; create no new owner, engine, registry,
ledger, or framework. **This contract authorizes no Phase-9 activation and starts no Audit run.**

---

## §1. Purpose & non-goals

**Purpose.** Define exactly (a) when the CF-5 Audit is entered; (b) what inherited architecture must be adversarially attacked;
(c) how findings are classified, validated, and dispositioned; (d) which findings block first new-domain activation; (e) how
corrective gates are spawned; (f) how (and whether) previously closed architecture may be reopened; and (g) what constitutes Audit
completion. **Non-goals (binding):** this contract is NOT the Audit, NOT a runtime engine / registry / activation policy /
readiness engine, and implements nothing. It records no conclusions about actual findings except already-authoritative
carry-forward observations (§16). It selects/qualifies/activates no domain and discharges no other carry-forward.

## §2. CF-5 identity, status & trigger

- **Canonical identifier:** **CF-5 — Retrospective Adversarial Architecture Audit.**
- **Status before this gate (repository truth):** **REGISTERED / PENDING; NOT EXECUTED; NOT YET AUTHORIZED AS AN ACTIVE AUDIT RUN**
  (registered by the P9-E2-R formal closure record §5 and re-affirmed by the P9-E2 formal closure record §7; "this registration
  authorizes no execution of the audit now").
- **Mandatory timing:** the Audit MUST be completed and all material (C/D/E) findings dispositioned as governed **BEFORE the first
  new-domain activation.**
- **Genericity:** CF-5 is **generic to the inherited architecture** and does **NOT require a selected next domain to begin.** A
  future domain selection may inform later *targeted* checks, but selection MUST NOT be required for CF-5 entry.
- **Entry authorization:** the Owner's continuation instruction is sufficient to author this bounded contract/entry candidate; the
  **Audit execution run** begins only after this contract candidate is Grilled, independently reviewed, Owner-accepted, published,
  merged (create-a-merge-commit), and post-merge verified (§20).

## §3. Audit objective (adversarial)

The Audit must adversarially challenge whether the inherited platform architecture remains **safe, truthful, domain-neutral,
extensible, and governable** when the platform moves from **one activated specialist domain** to **multiple activated specialist
domains**. It is **not** a routine code review. It must attempt to discover hidden architecture assumptions, latent domain
coupling, scaling defects, future-activation blockers, governance contradictions, and reachability-dependent technical debt. **The
Audit is designed to DISPROVE readiness, not to confirm it.**

## §4. Minimum mandatory Audit scope (each area independently attacked during execution)

**A. Shared-core architecture** — electronics-specific / pair-specific / domain-order / domain-count assumptions; hidden domain
names in logic; hidden specialization leakage. **B. Domain Registry** — pack discovery; schema/version validation; metadata
completeness; pack-id / alias collisions; lifecycle semantics; provenance; activation metadata; future-domain registration
behavior. **C. Activation mechanism** (`engine/domain_activation.py`, §5-I2) — activation source of truth; state isolation;
deterministic ordering; persistence (if any); test-double restoration; accidental activation; Registry-state interaction.
**D. Classifier ownership** — `classify_domain(...)` remains the sole canonical owner; attack alternate classifier paths,
duplicated ownership, legacy `infer_domain(...)` misuse, hidden consumers bypassing canonical classification. **E. Classifier
scoring & signals** — substring matching; false positives; short-signal collisions; cross-domain signal overlap; canonicalization;
deterministic tie handling; three-way / N-way behavior (seed NB-2; do not repair here). **F. Hardcoded fallback priority** (CF-3
concerns) — recognized-but-not-activated priority list; Nth-domain omission; future-pack completeness; hidden first-domain bias;
ordering assumptions. **G. Web strong-unsupported layer** (CF-6 concerns) — pre-classifier vs post-classifier ordering;
strong-unsupported vocabulary; future activated-domain collisions; admission; ambiguity; session creation; fail-closed behavior.
**H. Public-message truthfulness** (CF-2) — AMBIGUOUS_TIE / MULTI_DOMAIN_NEEDS_D4 user-facing treatment; generic unsupported
messaging; future public reachability; misleading domain claims. **I. Web / CLI / core consistency** — all consumers use the same
canonical classifier, interpret richer result kinds consistently, fail closed consistently, preserve the candidate set truthfully.
**J. Persistence & session state** — domain coupling / assumptions; future-domain compatibility; session-state contamination;
domain-identity persistence. **K. Domain isolation** — whether one pack can alter another's behavior, leak aliases/signals,
overwrite ids, or modify shared metadata. **L. Schema / version governance** — schema-version handling; backward/forward
compatibility; warning/skip behavior; invalid-pack behavior (seed NB-5 IoT/D8 warning as evidence). **M. Domain-pack
extensibility** — third/fourth/Nth-domain behavior; registration; discovery; routing; qualification handoff; activation handoff.
**N. Hidden Electronics assumptions** — electronics-only constants; electronics-first fallback; electronics-special Web copy;
electronics-specific routing; tests that encode current single-domain truth as universal truth. **O. Test architecture** —
genuine N-way coverage; causally meaningful mutation probes; whether construction invariants mask behavioral gaps (seed NB-3);
fixture activation-state restoration; environment-quirk dependence. **P. Reachable-on-activation deferred debt** — anything
currently non-reachable under Electronics-only operation that becomes material once a second domain is activated. **Plus** any
additional area discovered during execution.

## §5. Explicit scope boundaries

The Audit does **NOT** automatically reopen every historical phase; historical closed work remains closed unless a finding meets
the §6 taxonomy threshold (C/D/E) and passes §7 independent validation. The Audit is **NOT** authorization to redesign the
product, add features, or execute D4, D8, CAP-12, CAP-13, WS-PFV, deterministic calculations, knowledge-source features, Phase 10,
PSRR, or deployment. It selects/qualifies/activates **no** domain.

## §6. Finding taxonomy (existing authoritative CF-5 taxonomy — preserved exactly; NOT a new taxonomy)

- **A — No issue.** No defect; no action.
- **B — Hardening / future improvement.** Non-blocking; carry forward under governed future work if useful; does not reopen closed
  architecture.
- **C — Material latent issue, NOT currently reachable.** Not blocking current Electronics-only operation, but a **mandatory
  prerequisite before its trigger becomes reachable**; must be dispositioned before first new-domain activation if activation makes
  it reachable.
- **D — Material current issue, reachable now.** Requires a **bounded corrective gate before affected work continues.**
- **E — Architectural contradiction.** Requires an **explicit architecture and/or Owner decision**; no implementation proceeds
  through the contradiction.

## §7. Independent validation requirement

**Any material finding classified C, D, or E requires independent validation before previously closed architecture is reopened.**
The Audit team's own conclusion is insufficient to reopen a closed gate. Material-finding **validation MUST be separated from
remediation implementation** (distinct roles / distinct exact-candidate steps).

## §8. Correction-gate policy

- **A:** no action. **B:** carry forward / hardening; no closure reopening required.
- **C:** create a bounded **pre-trigger corrective prerequisite** that must close before the relevant trigger becomes reachable.
- **D:** create a bounded **corrective gate immediately before affected work continues.**
- **E:** **STOP**; require an explicit architecture/Owner decision before any correction design.
- All corrective work MUST preserve: bounded scope; contract/implementation separation; independent review where required; exact
  candidate identity; SHA-preserving publication; and pre/post-merge verification.

## §9. Audit completion criteria (CF-5 is complete only when ALL hold)

1. all mandatory §4 areas reviewed; 2. every finding classified A/B/C/D/E; 3. no finding unclassified; 4. all C/D/E findings have
independent validation (§7); 5. every D finding corrected or its affected work remains blocked; 6. every E finding has an explicit
architecture/Owner decision and required corrective path; 7. every C finding has a binding pre-trigger obligation; 8. all
first-new-domain-activation-relevant material findings dispositioned; 9. the Audit closure record is merged and post-merge
verified; 10. current activation remains unchanged unless a later separately authorized activation gate executes. **This Audit
CONTRACT does NOT complete CF-5.**

## §10. Audit evidence requirements (future execution run)

For each Audit area / finding the execution run MUST record, reproducibly: source path; exact relevant code/governance location;
reproduction procedure; test/probe if applicable; reachability classification; current-vs-future trigger; finding classification
(A/B/C/D/E); proposed disposition; and independent-validation status. **No unsupported narrative findings.**

## §11. Audit deliverables (future execution run — NOT produced by this gate)

Audit evidence report; finding register; classification per finding; trigger/reachability map; independent-validation evidence for
C/D/E; corrective-gate map where required; Audit completion/closure record. None are generated during this contract-candidate gate.

## §12. Relationship to P9-QS (separate)

The **P9-QS contract is AUTHORITATIVE** (merged PR #437); per-domain qualification **execution** remains separate and is
per-domain (P9-QS §3/§4). **Domain selection MUST precede per-domain P9-QS execution.** CF-5 qualifies no domain. CF-5 may occur
before domain selection. **Recommended sequence:** CF-5 Audit → domain selection → per-domain P9-QS → trigger-bound CF-6 / CF-2 /
CF-3 disposition → explicit Owner activation authorization. Where the repository governs gates only as a **partial order**, this
contract preserves that partial order and does not invent strict sequencing the repository does not require (e.g. CF-5 and domain
selection are not repository-ordered relative to each other; CF-5 is prudently before P9-QS because its D-class findings can
invalidate qualification).

## §13. Relationship to CF-6 (separate)

CF-6 remains separate: **PENDING PRE-SECOND-SPECIALIST-DOMAIN-ACTIVATION.** The Audit may discover/validate architecture evidence
relevant to CF-6, but **CF-5 completion MUST NOT automatically declare CF-6 executed**; CF-6 closes only via a later separately
governed CF-6 gate.

## §14. Relationship to CF-2 and CF-3 (separate)

CF-2 (public-message truthfulness) and CF-3 (non-activated priority/fallback completeness) remain separate trigger-bound
obligations. The Audit may surface evidence relevant to them, but **Audit completion does NOT automatically discharge either.**

## §15. D8 / IoT boundary

**D8 remains Owner-reserved.** The known IoT warning at `domains/iot_electronics/domain.json` may be **observed as evidence only**.
No IoT remediation, no D8 execution, no IoT activation, and no IoT domain qualification occur inside CF-5 (contract or execution)
unless separately authorized.

## §16. Known non-blocking observations seeded into the Audit (evidence only; classification NOT predetermined)

- **NB-2** — classification signal matching is substring-based; short signals such as `led` / `web` may false-positive.
- **NB-3** — one mutation probe is partly protected by `DomainClassification` construction invariants rather than a pure
  behavior-level assertion.
- **NB-4** — Web strong-unsupported vocabulary may conflict with future activated domains.
- **NB-5** — the IoT schema/version warning / skip (`domains/iot_electronics/domain.json`) is pre-existing and D8-bound.
These are already-authoritative carry-forward facts seeded for attention; **their A/B/C/D/E classification is determined only
during Audit execution.** No additional finding is manufactured while drafting this contract.

## §17. Forbidden work (unchanged; the Audit and this contract authorize none of it)

D4 composition; D8/IoT execution or activation; Mechanical / Medical Device / Software / any unnamed domain activation; CAP-12;
CAP-13; WS-PFV; deterministic-calculations capability; knowledge-source capability; Phase 10; PSRR; deployment; production. All
remain **NOT AUTHORIZED.**

## §18. Contract acceptance criteria (this candidate)

1. governance-only diff; 2. zero runtime/test/web/CLI/domain/Registry/activation/schema/persistence/API/guardrail change; 3. no
domain selected/qualified/activated; 4. `activated_domains() == ['electronics_electrical']` unchanged; 5. D8 unchanged /
Owner-reserved; 6. finding taxonomy A/B/C/D/E preserved exactly (no new taxonomy); 7. independent validation required for C/D/E;
8. CF-6 / CF-2 / CF-3 / P9-QS preserved as separate obligations (none discharged); 9. Audit remains NOT EXECUTED / execution NOT
YET AUTHORIZED; 10. `OWNER_DECISION_REGISTER.md` UNCHANGED unless repository precedent mechanically requires recording this
contract-creation authorization (it does not — a contract candidate records no new accepted Owner product-policy decision,
consistent with D3 / P9-QS / P9-E1 candidate precedent).

## §19. Governance scope of this contract candidate

Governance/documentation only: this NEW contract record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. **`OWNER_DECISION_REGISTER.md` UNCHANGED.** ZERO
runtime / engine / test / domain / Registry / activation / web / CLI / schema / persistence / API / architecture-guardrail diff.

## §20. Candidate state & next gate

**CF-5 status before/at this candidate:** REGISTERED / PENDING; **CONTRACT CANDIDATE ONLY; AUDIT NOT EXECUTED; AUDIT EXECUTION NOT
YET AUTHORIZED.** This candidate does **not** claim the Audit is ACTIVE, COMPLETE, or PASSED. It becomes the authoritative CF-5
contract-of-record only after **Mandatory Grill → independent external exact-candidate review → Owner exact-candidate acceptance →
SHA-preserving publication → PR → pre-merge verification → CREATE A MERGE COMMIT → post-merge verification.** Only after that
authoritative merge may the CF-5 Audit **execution** gate begin. **Next required gate: MANDATORY GRILL ON THIS EXACT CF-5 CONTRACT
CANDIDATE.** No domain activated; no domain selected; first new-domain activation remains BLOCKED behind CF-5 completion, per-domain
P9-QS qualification, CF-6, CF-2, CF-3, D8 (if IoT), and explicit Owner activation authorization.
