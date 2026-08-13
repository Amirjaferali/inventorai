# CF5-F001 — Shared-Core Electronics-Specific Safety Signal — Corrective Implementation Contract (Candidate)

**Status of THIS record:** governance/documentation-only **CORRECTIVE IMPLEMENTATION CONTRACT CANDIDATE** for CF-5 finding
**CF5-F001** (independently VALIDATED **C**; authoritative record
`docs/governance/CF5_F001_SAFETY_SIGNAL_INDEPENDENT_VALIDATION_RECORD.md`, merged PR #457). It defines **WHAT** a later
bounded implementation must achieve and **HOW** it will be proven; **it implements NOTHING** — no runtime, Web, CLI, test,
domain, activation, schema, or persistence change in this gate. **It does NOT close CF5-F001, CF-5, CF-6, CF-2, or any other
obligation, and selects/registers/activates no domain.** It becomes authoritative only through the governed lifecycle
(Mandatory Grill → independent external exact-candidate review → Owner exact-candidate acceptance → SHA-preserving
publication → PR → pre-merge verification → CREATE A MERGE COMMIT → post-merge verification). Expected engine / Web / CLI /
domains / Registry / activation / schema / persistence / API / test diff in THIS gate: **ZERO**.
**`OWNER_DECISION_REGISTER.md` UNCHANGED** (§3 records why no new Owner product-policy decision is required — the
CF5-F003-contract precedent).

**Authoritative base:** `17ff20cd18267b71ed2ce615ae144d4e94729ab3` (PR #457 — SHA-preserving merge of the accepted
validation record `23eb12b5`; merge tree == candidate tree; freshly fetched; 0 newer); boot OK;
`activated_domains() == ['electronics_electrical']`.

**Subordinate to** CLAUDE.md, the committed governance anchors, the CF-5 Audit contract (§7 validation / §8 C-policy), the
merged CF5-F001 validation record (its trigger, scope partition, NB-R1…NB-R4, fences, and re-disposition boundary govern),
the merged D-GMPR-01-D-D3 contract/implementation (D3-A history NOT reopened), and the WS2 stabilization contract (frozen
surfaces preserved).

---

## §1. Validated defect boundary (restated, authoritative)

`engine/safety_signal.py` residual shared-core electronics coupling (validation record §3): the `_MVP_DOMAIN` electronics
constant (`:55`); the electronics-gated mandatory context check `_has_electrical_context` (`:206-209`) with
`_ELECTRICAL_TERMS` (`:115-120`) as the sole non-electronics context; the electronics context/cue families (`:60-112`)
resident in shared core with **no governed per-domain seam**; and the `:272` missing-domain `domain_context` fallback (held
by the validation record as a contract-time examination item — dispositioned in §5/§6 below). **NB-R3 (binding):** the
electronics cues are **legitimately electronics-owned content**; the defect is **shared-core placement / unconditional
multi-domain exposure / lack of a governed per-domain seam** — nothing in this contract authorizes removing, renaming, or
"de-electronicsifying" the electronics vocabulary. Already-corrected **D3-A** history (the `domain_context` force-mapping)
is history and MUST NOT be reopened. **Trigger (binding, from the merged record §6):** the pre-trigger obligation applies
before the first point where a session whose domain is a non-electronics specialist domain can be produced by a production
surface and can reach `derive_inventor_stated_safety_signals`; current concrete enabler = activation-set broadening;
**equivalent future enablers** = any import/write/migration/continuation/reconstruction path or other production surface
capable of minting such a session; registration alone and empty activation are NOT triggers.

## §2. Corrective objective

Generalize the shared-core safety-signal derivation so that (a) domain-owned detection content is consumed through **one
governed domain-keyed seam** (electronics family byte-preserved as the sole populated entry), (b) a session domain without a
governed family truthfully yields **no signals plus a truthful capability-scope statement** (never electronics-cue
semantics, never a silent implication that detection ran meaningfully), (c) the presently reachable **NB-R1** electronics
live-vs-cold-load detection divergence is eliminated at its seam, and (d) current electronics live behavior is preserved
under differential parity. **No new derivation authority is created**: `derive_inventor_stated_safety_signals` remains the
single derivation owner; no second safety framework, registry, or orchestrator.

## §3. Architecture decision — D-direction: **PARAMETERIZE** (evidence-settled; no new Owner decision)

**Direction:** PARAMETERIZE — a single **domain-keyed cue/context-family seam inside `engine/safety_signal.py`**, with the
electronics family (the current `_FAILURE_CUES`/`_SUBJECT_CUES`/`_CONSEQUENCE_CUES`/`_ELECTRICAL_TERMS` vocabulary,
byte-preserved) as the sole populated entry, keyed by the canonical domain id. A domain with no governed family derives no
signals (plus the §6 truthful scope statement at the assembly surface). The seam keys on **domain identity** (content
ownership), not activation state — activation gates admission, never historical derivation (this is also the **NB-R4
disposition**: a legacy electronics session cold-loaded after a hypothetical electronics deactivation still derives its
electronics-owned signals truthfully, labeled with its historical domain).

**Why this direction is settled by repository evidence (not assumption):**
- **KEEP** fails the objective (leaves the validated coupling and the D3 `safety_signal` coupling undischarged, blocking
  activation permanently).
- **MOVE / DELEGATE** (family data into Domain-Pack schema or a new content owner) requires a Domain-Pack schema gate with
  no activated consumer, and no canonical owner of per-domain safety-cue content exists today (validation record §7) —
  strictly larger than minimal; it remains available later, at a new domain's own gate, as data relocation behind the SAME
  seam (explicitly out of scope here).
- **PARAMETERIZE** is the committed repository pattern for exactly this defect class: the merged **D3-B** correction
  (`engine/path_n_questions.py`) threads an optional canonical domain identity through the existing owner, serves the
  Electronics-owned artifact only for Electronics/None, and returns no-content for a foreign domain so canonical per-domain
  ownership governs later — "no parallel question framework". This contract applies the same accepted pattern to the safety
  seam.

**Why no Owner product-policy decision is required (recorded resolution of the validation record §8 question):** the
"silent no-signals vs. truthful capability-scope note" question is settled by already-committed Owner-locked truthfulness
authority, not by new policy: the F002 contract's §4.E made trigger-time copy truthfulness MANDATORY within its surface
without a new Owner decision (D1/D2 were consent policy, not truthfulness policy); P6-1 (truthful domain labeling) and the
truthful-state increments commit the same principle; and the committed safety-signal empty statement is deliberately
detection-scoped honest text. Under a broadened activation set, rendering the electronics-detection empty statement for a
domain with NO governed detection family would imply detection ran meaningfully — the same untruthfulness class §4.E
corrected. Therefore the truthful capability-scope statement is contract-mandated behavior; its exact WORDING is
implementation detail (subject to normal review), not product policy. Whether a new domain MUST ship a safety-cue family
before activation is a **P9-QS / activation-gate question, explicitly NOT decided here** (fence preserved; recorded as an
open input to that separate gate).

## §4. NB-R1 disposition (presently reachable; mechanically located; MANDATORY in the implementation)

**Located seam (contract-binding evidence):** `web/app.py` `_cold_load_entry(sid)` rebuilds a live runtime entry after
memory loss via `ProjectRecordContract.to_state()` (`engine/record_contract.py` — restores ONLY `idea_id` + assertions; no
`domain`/`domain_signal`), then serves it through `show_session` into `SESSION_STORE`, where the deliverable routes run
`assemble_deliverable` on a domain-less state: the mandatory context check loses its domain branch and `domain_context`
falls back at `engine/safety_signal.py:272` — the validated live-vs-cold-load electronics detection divergence.

**Required correction (minimum-path; no schema/migration):** `_cold_load_entry` MUST additionally restore the
safety-relevant domain identity from the **already-persisted** reconstruction inputs (`confirmed_domain`, written once at
creation and creation-validated) onto the rebuilt state (`domain` and `domain_signal`), and ONLY that. Legacy/partial
envelopes (NULL reconstruction columns) restore nothing and keep today's behavior (fail-safe; no migration, no rewrite, no
new persistence field). `path` restoration and any broader cold-load fidelity work remain OUT of scope (owned by the
P4-1b/P4-2 lanes); the consequential cold-load behavioral deltas that follow from restoring the domain (e.g. domain-keyed
question selection on a cold-loaded session becoming consistent with live) MUST be enumerated and categorized in the §7
differential — cold-load converging to live behavior is the correction, not a regression. `record_contract.to_state()` and
the contract schema are NOT modified.

## §5. Scope fence (later implementation)

**Allowed production paths (minimum, evidence-backed):**
- `engine/safety_signal.py` — the domain-keyed family seam (electronics vocabulary byte-preserved as the sole entry), the
  context-check generalization consuming that seam, an additive read-only capability query (whether a governed family
  exists for a domain id) for the assembly surface, and the `:272` fallback disposition: with the NB-R1 restoration in
  place, the missing-domain fallback becomes reachable only for legacy/NULL-envelope states, where it retains today's
  electronics default label as the governed backward-compatible behavior (re-examined, retained, and documented — not
  silently changed).
- `web/app.py` — ONLY the bounded `_cold_load_entry` NB-R1 restoration (§4). No `/start`, admission, template, or route
  change.
- `engine/deliverable_assembler.py` — ONLY the bounded `_s15` assembly change required to carry the truthful
  capability-scope statement for a session domain with no governed family (additive field or conditioned empty statement;
  the committed electronics empty statement, advisory note, JSON location `_session_meta.inventor_stated_safety_signals`,
  and `risk_safety_linkage` semantics unchanged for electronics).
- Focused tests: NEW `tests/test_cf5_f001_safety_signal_domain_seam.py`, plus mechanically-justified additions to
  `tests/test_safety_signal.py` / `tests/test_d3_core_domain_neutrality.py` (additions preferred; any assertion
  modification requires load-bearing proof, F002-precedent disclosure, and Grill attention).
- `web/templates/deliverable.html` — ONLY IF mechanically required to render the scope statement (the existing
  `empty_statement` surface is expected to suffice; if a template change becomes necessary, the gate records why).

**Forbidden unless separately justified by repository evidence:** any second safety framework/derivation path; Domain-Pack
schema change or pack data edits; classifier (`engine/domain_rules.py`) or activation-policy/set
(`engine/domain_activation.py`) change; `record_contract`/store schema or migration; scoring, Section 6/13,
`RequirementLandscape.risks`, readiness, persistence semantics; Path-N (`engine/path_n_questions.py`); CAP-13 pre-building;
CF-2/CF-6 surfaces beyond §5; D4 execution; D8; ILT-002 routes; any de-electronicsifying of the cue vocabulary (NB-R3);
`OWNER_DECISION_REGISTER.md` (ZERO ODR diff in the implementation gate). Any additional production path → the
implementation gate **STOPs before expanding scope** and reports the evidence (the F002/Amendment-01 lesson).

## §6. Required GREEN behavioral matrix (the later implementation MUST satisfy exactly)

Activation state exercised ONLY via self-restoring `_ACTIVATED_DOMAINS` doubles; **no real activation change**.

- **A. Electronics live parity (backward compatibility — NO user-visible regression):** for live electronics sessions, the
  derivation and the assembled §15 block are behaviorally identical to the authoritative parent across the §7 differential
  corpus (signals, fields, order, labels, empty statement, advisory note, linkage block); all existing
  `tests/test_safety_signal.py` and D3 pins pass unchanged (or with load-bearing-proved additions only).
- **B. NB-R1 eliminated:** a real Flask electronics session whose signal-bearing statement carries no literal electrical
  term derives the SAME signals live and after durable cold-load (SESSION_STORE cleared, entry rebuilt); cold-loaded
  `domain_context` equals the restored session domain (not the `:272` fallback); legacy/NULL-envelope cold-load behavior
  unchanged.
- **C. Family-less domain (activation doubles):** a non-electronics-domain session (e.g. mechanical) derives NO signals —
  including for text containing electronics vocabulary (unconditional-exposure defect corrected) — and its assembled block
  carries the truthful capability-scope statement instead of the electronics-detection empty statement; no crash; no
  electronics `domain_context` stamping.
- **D. Domain-identity keying (NB-R4 disposition):** derivation keys on the session's domain identity, not activation
  state: an electronics-domain session still derives electronics signals under a double where electronics is absent from
  the activation set (historical sessions stay truthful).
- **E. Frozen surfaces preserved:** public API, `SafetySignal` fields, output shape, provenance/validation constants,
  excerpt behavior, JSON location, linkage-block semantics — all unchanged (WS2/Increment-6/WS5 obligations).
- **F. Determinism & purity:** derivation remains pure, deterministic, read-only; no I/O, no activation lookups inside the
  per-sentence hot path beyond the existing per-call cost envelope.

## §7. Required RED→GREEN + mutation + differential evidence

**RED (fail pre-fix for the validated defect reasons; pass post-fix):** (r1) a non-electronics-domain session's assembled
block lacks any truthful capability-scope statement while rendering the electronics-detection empty statement; (r2) a
non-electronics-domain session WITH electronics vocabulary in its text derives an electronics-cue signal (unconditional
exposure); (r3) NB-R1 reproduction on the real Flask surface: live electronics signal (statement without literal electrical
terms) disappears after durable cold-load; (r4) cold-loaded state's `domain_context` produced by the `:272` fallback rather
than the session's actual domain. If any RED cannot be reproduced mechanically, the implementation gate STOPs and reports
the evidence conflict (it must not fake a reproduction).
**Mutation probes (each CAUGHT RED; bytes sha256-restored; bytecode caches cleared):** (m1) re-hardcode the context gate to
the electronics constant, bypassing the family seam; (m2) leak the electronics family to ALL domains (unconditional
exposure restored); (m3) drop the `_cold_load_entry` domain restoration (NB-R1 regression); (m4) restore a wrong/hardcoded
domain value at cold-load; (m5) suppress the capability-scope statement for a family-less domain OR emit it for electronics
(parity break); (m6) mutate a frozen surface (a `SafetySignal` field or the JSON location) — caught by the frozen-surface
pins.
**Differential sweeps (every delta categorized; ZERO unexplained):** (d1) live electronics corpus, parent vs implementation
→ REQUIRED zero deltas; (d2) cold-load corpus, parent vs implementation → every delta categorized as the governed NB-R1
correction (including consequential cold-load-converges-to-live effects, enumerated); (d3) activation-double corpus
(non-electronics domains) → every delta categorized as family-seam correction / truthful-scope statement. **Full governed
suite green** (record exact counts; no pre-existing regression).

## §8. Backward compatibility & rollback

Live electronics behavior: differential parity (§6.A, §7.d1 — zero deltas). Cold-load behavior changes ONLY as the governed
NB-R1 correction with the delta enumerated. Rollback = revert the bounded changes in the three named files (no schema, no
migration, no data rewrite; legacy envelopes unaffected either way). The change is a bounded generalization of one shared
derivation seam plus one cold-load identity restoration.

## §9. Exact closure criteria (the later implementation may close CF5-F001 ONLY when ALL hold)

§6 A–F GREEN via the real surfaces; §7 RED r1–r4 reproduced pre-fix; m1–m6 CAUGHT; d1–d3 categorized with zero unexplained;
full suite green; frozen surfaces proven unchanged; NB-R1 eliminated with legacy fail-safe preserved; NB-R3 honored
(electronics vocabulary byte-preserved); NB-R4 dispositioned per §3/§6.D; no second framework; no pack-schema change; no
ODR diff; Mandatory Grill PASS; independent external exact-candidate review ACCEPT; Owner exact-candidate acceptance;
SHA-preserving merge; post-merge verification. **This contract candidate does NOT close CF5-F001.** At implementation
closure the gate MUST state exactly: the D3-coupling portion discharged, the NB-R1/NB-R4 dispositions applied, the open
P9-QS input (§3), and any residual F001-adjacent observations.

## §10. Governance disposition & non-effects

**CF5-F001 = OPEN C — INDEPENDENTLY VALIDATED — corrective contract candidate (this record).** CF5-F002 FORMALLY CLOSED;
CF5-F003 CLOSED; CF5-F004 OPEN C; CF-5 OPEN; CF-6 OPEN (facets (i)–(iv) discharged only); CF-2 OPEN; CAP-13 untouched;
Path-N untouched; D4 SEPARATE / UNEXECUTED; D8 Owner-reserved; `activated_domains() == ['electronics_electrical']`; **NO
domain selected/registered/activated; first new-domain activation remains BLOCKED** behind CF5-F001, CF5-F004, remaining
CF-6, CF-2, CF-3, per-domain P9-QS, D8 (if IoT), and explicit Owner activation authorization. Phase 10 NOT AUTHORIZED; PSRR
NOT EXECUTED; deployment/production NOT AUTHORIZED. FU-1 remains outside F001 (registered once, CF-5 lane). The
Owner-re-disposition boundary of the validation record §13 continues to govern.

## §11. Scope of THIS candidate & next gate

Governance/documentation only: this NEW corrective-contract record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. **ZERO** runtime / test / Web / CLI /
domain / Registry / activation / schema / persistence / API / guardrail / ODR diff. **Next required gate: Mandatory Grill
on this exact candidate**; any material finding rejects it as-is (fresh candidate from the authoritative parent — no
in-place amendment). After this contract is authoritative, the bounded CF5-F001 **implementation** is the subsequent
separately governed gate.
