# CF5-F004 — Hardcoded Non-Activated Priority Fallback — Corrective Implementation Contract (Candidate)

**Status of THIS record:** governance/documentation-only **CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE** for CF-5 finding
**CF5-F004** (independently VALIDATED **C**; authoritative record
`docs/governance/CF5_F004_PRIORITY_FALLBACK_INDEPENDENT_VALIDATION_RECORD.md`, merged PR #461). It defines WHAT a later
bounded implementation must achieve and HOW it will be proven; **it implements NOTHING** — no runtime, Web, CLI, test,
domain-pack, registry, activation, schema, or persistence change in this gate. **It does NOT close CF5-F004, CF-3, CF-5,
CF-6, or CF-2, and registers/activates no domain.** It becomes authoritative only through the governed lifecycle
(Mandatory Grill → independent external exact-candidate review → Owner exact-candidate acceptance → SHA-preserving
publication → PR → pre/post-merge verification). The only production-relevant change this gate is the authoritative
recording of Owner decisions **OD1/OD2/OD3** (§2) in `OWNER_DECISION_REGISTER.md` as **D-CF5-F004-01** — a documentation
record, not code (the D-CF5-F002-01 precedent; the implementation gate makes ZERO ODR change).

**Authoritative base:** `5dc5055746eaeabc5c92550b1dc10ac66860d7cc` (PR #461 — SHA-preserving merge of the accepted F004
validation record `4c4a3262`; merge tree == candidate tree; freshly fetched; 0 newer); boot OK;
`activated_domains() == ['electronics_electrical']`.

**Subordinate to** CLAUDE.md, the committed anchors, the CF-5 audit contract (§8 C-policy), the merged F004 validation
record (its finding identity, failure arms, trigger, fences, and preserved statuses govern), and the closed
D3-D / P9-E2 / P9-E2-R / CF5-F003 / CF5-F002 gates (none reopened).

---

## §1. Validated defect boundary (restated, authoritative)

`engine/domain_rules.py::classify_domain` Case 0 (`:234-242`): the un-owned, registry-unsynchronized 4-id priority literal
`["medical_device", "electronics_electrical", "mechanical", "software"]`, consulted for every zero-activated-tied
classification. **Failure arm A:** a registered pack outside the literal as sole top scorer → the loop exhausts → silent
**NONE** (and, downstream, the validated dangerous chain: NONE → sole-electronics `/start` consent → possible
electronics-labeled persisted session). **Failure arm B:** a registered pack outside the literal tied at `best_score` with
a legacy literal member → the legacy member is **silently awarded** SINGLE, displacing the new pack. Not reachable today
(recognized registry set == literal set; `iot_electronics` schema-skipped). **Trigger:** the first successful
recognized-registry-set change; **per Owner decision OD1 (§2), the remediation obligation binds even earlier — before any
pack-schema/provenance WORK whose successful result could change the recognized-registry set.**

## §2. Owner decisions recorded (D-CF5-F004-01; the one justified ODR change, THIS gate only)

- **OD1 — Pre-trigger binding (safer sequencing):** F004 remediation MUST be complete **before any pack-schema or
  provenance work whose successful result could change the recognized-registry set** (e.g. any `iot_electronics`
  schema-fix work) — intentionally earlier than the actual successful registration event.
- **OD2 — Legacy precedence:** the current legacy precedence outcomes for the existing four recognized domains
  (`medical_device > electronics_electrical > mechanical > software`, zero-activated behavior) are **preserved**: no
  change to current user-visible classification or `/start` guidance flavor for existing four-domain inputs. For FUTURE
  registered domains, **no new arbitrary winner rule may be invented**; the policy must be deterministic and must never
  silently erase or displace a registered top-scoring domain merely because its id is absent from a hardcoded list.
- **OD3 — CF-3 discharge timing:** CF-3 and the D-GMPR-01-D-D3 hard-coded tie-break coupling discharge **only at eventual
  F004 formal closure**, after the implementation is authoritative and closure verification succeeds — never earlier,
  never implicitly.

## §3. Architecture decision — selected (minimum repository-compatible)

**Registry-derived candidate membership + explicit bounded legacy-compatibility precedence layer + truthful fail-closed
representation of otherwise-unresolvable zero-activated ties.** Concretely, Case 0 is replaced by:

1. **No membership assumption:** the zero-activated resolution consumes the top-scored tied set as computed over the
   canonical registry (which `classify_domain` already iterates) — no hardcoded recognized-domain membership list decides
   *whether* a domain can win.
2. **Legacy compatibility layer (explicit, bounded, byte-preserved):** the existing 4-id order
   `medical_device > electronics_electrical > mechanical > software` survives ONLY as an explicit compatibility precedence
   **among the legacy four ids** — reproducing today's outputs exactly for every current-registry input (OD2).
3. **Arm A resolution:** a registered domain that is the SOLE top scorer yields `SINGLE(that domain)` regardless of legacy
   membership — deterministic, truthful, existing result kind (the unique top scorer is not an "invented winner").
4. **Arm B resolution — NEW fail-closed result kind (mechanical necessity proven):** a zero-activated tie NOT resolvable
   by the legacy layer (any tie involving a non-legacy registered domain, or among multiple non-legacy domains) yields a
   NEW `DomainResultKind` (working name `UNRESOLVED_NON_ACTIVATED_TIE`) carrying the complete tied candidate set in
   canonical (sorted) order with the existing deterministic `EQUAL_SCORE` reason — **no winner, fail-closed downstream**.
   *Mechanical necessity (each alternative fails):* `SINGLE(legacy member)` = the validated silent displacement;
   `SINGLE(new domain)` = an invented arbitrary winner (OD2-forbidden); `NONE` = silent erasure feeding the validated
   dangerous admission chain; reusing `AMBIGUOUS_TIE` would require weakening its CLOSED P9-E2-R construction invariant
   ("every candidate ACTIVATED", D3-D) — reopening closed representation semantics. Hence a new kind is the ONLY truthful,
   deterministic, closed-gate-preserving representation. `AMBIGUOUS_TIE` itself is UNTOUCHED (activated-only, P9-E2).
5. **Consumers (bounded fail-closed dispatch only; no redesign):** `web/app.py` `/start` MUST add the new kind to its
   existing fail-closed refusal dispatch — mechanically required, because today an unrecognized kind falls through to the
   NONE consent path (the dangerous chain); the CLI's existing bounded-stop tuple gains the new kind for truthful
   messaging (it already fail-closes by refusal either way). `infer_domain` needs NO change: its frozen contract already
   fails loud (`AmbiguousDomainResultError`) for every non-SINGLE/NONE kind — the implementation MUST pin this.
6. **Determinism:** all candidate ordering is canonical (sorted); no dict-order, filesystem-order, or registry-iteration
   order dependence; a determinism probe over shuffled registry iteration is mandatory (§6).

## §4. Scope fence (later implementation)

**Allowed production paths (minimum, evidence-backed):**
- `engine/domain_rules.py` — the Case-0 replacement (§3.1–§3.4), the new result kind + its construction invariants
  (≥2 registry-recognized candidates, canonical order, deterministic reason, no winner, NO activation requirement —
  explicitly distinct from `AMBIGUOUS_TIE`), and nothing else in the file (matching semantics = CF5-F003, CLOSED;
  activated precedence = D3-D/P9-E2, CLOSED).
- `web/app.py` — ONLY the addition of the new kind to the existing `/start` fail-closed refusal dispatch (same refusal
  surface/message class as the existing ambiguity branches; no admission/UX redesign — F002 CLOSED).
- `scripts/run_cli.py` — ONLY the addition of the new kind to the existing bounded-stop tuple.
- Focused tests: NEW `tests/test_cf5_f004_priority_fallback_extensibility.py` (registry doubles are self-restoring
  in-process replacements of `engine.domain_rules._REGISTRY`; no pack file is created), plus mechanically-justified
  additions to existing tests (any assertion modification requires load-bearing proof + disclosure + Grill attention).
**Forbidden unless separately justified by repository evidence:** any second classifier/matcher/framework; any duplicate
registry/config source; domain-pack file or registry schema/data change; activation change; any alteration of
`AMBIGUOUS_TIE`/`MULTI_DOMAIN_NEEDS_D4` semantics, D3-D/P9-E2 precedence, CF5-F003 matching, or the F002 admission
policy/UX; `infer_domain` signature/contract change; dict/filesystem/iteration-order dependence; registry skip-warning
changes; IoT vocabulary / `_LAY_ELECTRICAL_WORDS` / strong-unsupported-family work (examination inputs only; CF-6/CF-2
lanes); D4 execution; D8; `OWNER_DECISION_REGISTER.md` in the implementation gate. Any additional production path → the
implementation gate **STOPs before expanding scope** and reports the evidence.

## §5. Required RED evidence (fail on the clean parent for the validated reasons)

- **R1:** simulated registered domain outside the legacy literal (registry double) as SOLE top scorer → parent yields
  NONE (arm A exposed).
- **R2:** simulated registered domain tied at `best_score` with a legacy non-activated member → parent silently awards
  the legacy member (arm B exposed).
- **R3:** legacy four-domain priority outputs pinned (e.g. `gear and catheter → medical_device`; representative corpus).
- **R4:** D3-D activated-over-recognized tie behavior unchanged (activation double).
- **R5:** P9-E2 ≥2-activated tie → `AMBIGUOUS_TIE` unchanged (activation double).
- **R6:** `infer_domain` compatibility pinned: SINGLE/NONE totality + fail-loud on every richer kind INCLUDING the new
  kind post-fix.
- **R7:** real `/start` chain (registry double): a registered-but-omitted pack's idea is admitted TODAY as an
  electronics-labeled session via the NONE consent path on the parent; post-fix the corrected classifier yields
  SINGLE(new domain) → the CLOSED F002 flow refuses it (recognized-not-activated) — no NONE-based electronics admission.
  (R3/R4/R5/R6 are pins that must pass on BOTH parent and candidate; R1/R2/R7 are the distinguishing RED probes. If any
  distinguishing probe cannot be reproduced mechanically, the implementation gate STOPs and reports the conflict.)

## §6. Required GREEN matrix + mutation + differential + suite evidence

**GREEN:** arm A → SINGLE(sole top scorer) for non-legacy registered domains; arm B (and non-legacy-only ties) → the new
fail-closed kind with the complete canonical candidate set; legacy-four behavior byte-compatible (full current-registry
differential corpus, ZERO deltas — OD2); `/start` fail-closed dispatch of the new kind (refusal, no session, truthful
copy surface); CLI bounded stop; `infer_domain` fail-loud on the new kind; new-kind construction invariants enforced
(rejecting <2 candidates, unsorted order, unrecognized ids, a carried winner, or an activation requirement);
**determinism probe** — identical results under shuffled registry iteration order; architecture/neutrality guardrail
tests green. **Mutation probes (each CAUGHT RED; bytes sha256-restored):** (m1) reintroduce literal-membership
fallthrough (arm A regresses to NONE); (m2) reintroduce silent legacy displacement (arm B regresses); (m3) invent an
arbitrary winner for an unresolvable tie; (m4) introduce registry-iteration-order dependence; (m5) drop the `/start`
dispatch of the new kind (electronics admission returns); (m6) weaken the `AMBIGUOUS_TIE` activated-only invariant.
**Differentials:** (d1) full current-registry corpus parent-vs-implementation → **ZERO deltas** (OD2 lock, includes
`/start` guidance flavor); (d2) simulated-registry corpus (registry doubles) → every delta categorized as arm-A
correction / arm-B truthful fail-closed representation / dispatch correction; 0 unexplained. **Full governed suite green**
(exact counts recorded; no pre-existing regression). `git diff --check` clean.

## §7. Backward compatibility & rollback

Under the current registry, every classification, `/start`, and CLI outcome is differentially identical to the parent
(d1 = zero deltas). The new kind is unreachable until a registry-set change occurs — and OD1 requires this remediation
BEFORE any work that could cause one. Rollback = revert the bounded changes in the three named files (no schema, pack,
persistence, or data change).

## §8. Exact closure criteria (the later implementation may close CF5-F004 ONLY when ALL hold)

§5 R1–R7 evidenced; §6 GREEN/mutations/differentials/suite all satisfied; new-kind invariants enforced; closed gates
untouched (D3-D, P9-E2, P9-E2-R representation of existing kinds, CF5-F003, F002 admission); no second
classifier/registry source; determinism proven; `infer_domain` contract pinned; Mandatory Grill PASS; independent
external exact-candidate review ACCEPT; Owner exact-candidate acceptance; SHA-preserving merge; post-merge verification.
**Only at the subsequent F004 FORMAL CLOSURE gate** (OD3) do CF-3 and the D-GMPR-01-D-D3 tie-break coupling discharge.
**This contract candidate closes nothing.**

## §9. Governance disposition & non-effects

**CF5-F004 = OPEN C — INDEPENDENTLY VALIDATED — corrective contract candidate (this record).** CF5-F001/F002 FORMALLY
CLOSED; CF5-F003 CLOSED; CF-5 OPEN; CF-6 OPEN (facets (i)–(iv) discharged only); CF-2 OPEN; CF-3 registered/retained
(discharge per OD3 only); registry skip-warning outside F004; IoT items examination inputs only; D4 SEPARATE /
UNEXECUTED; D8 Owner-reserved; Phase 10 NOT AUTHORIZED; PSRR NOT EXECUTED; deployment/production NOT AUTHORIZED.
`activated_domains() == ['electronics_electrical']`; **NO domain registered/activated; first new-domain activation
remains BLOCKED; and per OD1 the F004 obligation binds before any pack-schema/provenance work capable of changing the
recognized-registry set.**

## §10. Scope of THIS candidate & next gate

Governance/documentation only: this NEW contract record + `OWNER_DECISION_REGISTER.md` (D-CF5-F004-01, §2) +
`ACTIVE_EXECUTION_ROADMAP.md` (append-only) + `ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md`. **ZERO**
runtime / test / Web / CLI / domain / registry / activation / schema / persistence diff. **Next required gate: Mandatory
Grill on this exact candidate**; after this contract is authoritative, the bounded CF5-F004 **implementation** is the
subsequent separately governed gate.
