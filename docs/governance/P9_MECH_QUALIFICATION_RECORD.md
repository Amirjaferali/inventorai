# P9-MECH — Mechanical Domain P9-QS QUALIFICATION RECORD (Terminal §15/§16 Evidence Package & Formal Qualification — Candidate)

> **OD-M2 CLAUSE-2 MANDATORY ANNOTATION (prominent, per D-P9-MECH-02 — no unannotated "QUALIFIED" claim exists or is
> permitted):** the qualification recorded below is **`MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS`**.
> **The governed Mechanical safety-cue family DOES NOT EXIST YET and is an OUTSTANDING ACTIVATION BLOCKER** (OD-M2
> clause 3: it MUST be complete, merged, and post-merge verified BEFORE any Owner activation authorization for
> `mechanical`). Additional activation blockers are listed in §5. **Mechanical remains NOT ACTIVATED**;
> `activated_domains() == ['electronics_electrical']`; first new-domain activation remains BLOCKED.

**Status of THIS record:** governance/documentation-only **TERMINAL QUALIFICATION RECORD CANDIDATE** under the
AUTHORITATIVE P9-MECH-QC contract (§15 item 10: "a qualification record proving each item above with exact SHAs, then
the governed lifecycle for that record"). It implements nothing and changes no runtime/test/pack/registry/activation
file. **`MECHANICAL = P9-QS QUALIFIED (WITH ACTIVATION BLOCKERS)` becomes authoritative ONLY if/when this exact
candidate is merged (create-a-merge-commit) and post-merge verified** through the governed lifecycle.
**`OWNER_DECISION_REGISTER.md` UNCHANGED** (qualification is an evidence determination under the accepted P9-QS
standard and D-P9-MECH-01/-02 — P9-QS §2: qualification ≠ Owner authorization ≠ activation; no new Owner
product-policy decision is made here). **DOCUMENTED NO-VALID-RED.**

## §1. Basis and fresh verification

Base: `ac8ac2d9fd17135befb990890dd57e838c24b671` (SHA-preserving merge of the accepted D-GMPR-D3-PN formal-closure
candidate `be40cc90` onto `17a4aca4`; merge tree `9a2da541` == candidate tree; POST-MERGE PASS; freshly fetched;
0 newer; clean tree) — `D-GMPR-01-D-D3` FULLY DISCHARGED is authoritative. Fresh verification at THIS base: all six
Mechanical evidence suites (I1/I2/I3/I4/I5 + the D-GMPR-D3-PN evidence file) **104 passed**; full governed suite
**2546 passed / 3 skipped / 1 xfailed / 0 failed**; `activated_domains() == ['electronics_electrical']`;
`support_state("mechanical") == "recognized_not_activated"`; `has_governed_safety_cue_family("mechanical") is
False` (truthfully declared NOT COVERED); the OD-M2 clause-1 statement and the §8.4 dormant-weight annotation
verified present in the merged pack.

## §2. §15 criterion matrix (every item evidence-proven with exact SHAs; nothing assumed)

| §15 item | Evidence (authoritative merges) | Status |
|---|---|---|
| 1. §5 capability contract + §6 real rule nuances + §7 coverage declaration, committed with provenance | I1 impl `f595fb60` (merge `f7ed7448`): capability/coverage declarations incl. OD-M2 clause-1 statement; PR002. I2 impl `3d51bb1c` (merge `4037a67d`): full-shape truthful nuances; PR003 | **DISCHARGED** |
| 2. Focused deterministic tests per capability/gap/nuance/boundary class, incl. negative + honest-precondition | I1 (18), I2 (17), I3 (18), I4 (20), I5 (16), D-GMPR-D3-PN (15) test files — 104 fresh-passing at this base | **DISCHARGED** |
| 3. Mutation/adversarial probes (every governed behavior load-bearing) | Executed and recorded per increment: I1 m1–m7, I2 m1–m10, I3 m1–m10, I4 m1–m6(+m2b), I5 m1–m7(+m6b), D-GMPR M1–M7(+M6a/b) — all CAUGHT right-reason | **DISCHARGED** |
| 4. Full-suite regression + §10 electronics non-degradation differentials | Byte-parity corpora at I1 (UUID-normalized /start + classification), I3 (categorized, zero unexplained), I4 (sibling pins), D-GMPR (34/34 electronics served capture; artifact byte-frozen); full suite green at every increment and fresh here (2546/3/1/0) | **DISCHARGED** |
| 5. Representative-journey cases within declared scope; truthful refusal/degradation outside | I4 terminal corpus (positive journeys; hard cases; ties by score parity; NONE/recall boundaries labeled as limitations); unactivated-refusal behavior governed by the merged activation-derived admission (D-CF5-F002-01) and pinned recognition/activation separation | **DISCHARGED** |
| 6. Provenance per §4b / verbatim-provenance owners | `mechanical:PR001`–`PR004` in the canonical manifest; every declaration/nuance/signal/question/artifact provenance-tagged and test-resolved | **DISCHARGED** |
| 7. Deterministic behavior | Determinism pins in every evidence file (classification, service, loads) | **DISCHARGED** |
| 8. Web/UI + CLI consistency where surfaces are touched | NO web/CLI surface was touched by any qualification increment (I1–I5, D-GMPR-D3-PN changed no web/CLI file); the governing admission surface remains the merged activation-derived D-CF5-F002-01 behavior — satisfied as not-applicable-with-reason | **DISCHARGED (N/A-with-reason)** |
| 9. OD-M2-decided safety-cue evidence | Per B-hardened (D-P9-MECH-02): clause 1 — declarations state derivation NOT COVERED (I1, verified fresh); clause 2 — THIS record's prominent annotation (header); clause 3 — ACTIVATION-ONLY (not executed here, §5) | **DISCHARGED for qualification** |
| 10. The qualification record itself | THIS candidate (exact SHAs throughout; governed lifecycle follows) | **This gate** |

**§12 recording:** §12(a) pack-content sufficiency DISCHARGED (I5 impl `baee2542`, merge `0dca782e`). **§12(b) —
non-specialist Path-N service — now RECORDED COMPLETE:** the D-GMPR dependency it was conditioned on is FULLY
DISCHARGED (closure merge `ac8ac2d9`), and the service is factual and evidence-proven (mechanical served its verbatim
committed artifact through the canonical seam; reconciled I5/D3/P9-E1 pins green fresh). **§8.4 confirmation (the
closure-time confirmation the I3 map deferred): CONFIRMED** — the pack-level dormant-weight annotation stands in the
merged pack, `weight`/`layer` remain unread by any runtime code, and the cross-pack residual remains with its
separate shared-core owner (untouched, unabsorbed). **§9 terminal boundary corpus:** DISCHARGED (I4 impl `3fe23a8c`,
merge `c7c9e413`); its inventory-scoped validity is intact (mechanical pack byte-unchanged since I3; verified). No
prior Mechanical evidence is stale after the D-GMPR remediation: the only affected pins were the five
contract-enumerated reconciliations, executed and green.

## §3. Determination

Every P9-MECH-QC qualification criterion (§5–§12, §15) is evidence-proven with authoritative merged SHAs, and P9-QS
§7's dual proof holds (A: works within truthful declared scope — the declarations exclude what is not implemented;
B: no material degradation of the activated domain — byte-parity + full-suite evidence). Therefore this record
declares, conditional on its own merge + post-merge verification:

> **`MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS` (see the header annotation and §5).**

Qualification is declared relative to the TRUTHFUL DECLARED capability scope (P9-QS §3): concept-level mechanical
reasoning ONLY; everything declared NOT COVERED (incl. inventor-stated safety-signal derivation, pending the
governed family) remains NOT COVERED.

## §4. What qualification does NOT mean (P9-QS §2 separations — binding)

Qualification ≠ Owner authorization ≠ activation ≠ composition authority. This record activates nothing, changes no
admission behavior, adds no user-facing Mechanical capability, and creates no activation eligibility beyond what the
committed prerequisites define. D4 remains REGISTERED / NOT AUTHORIZED; D8 Owner-reserved; THERM-01 future-only;
Phase 10 NOT AUTHORIZED; PSRR NOT EXECUTED; deployment NOT AUTHORIZED.

## §5. OUTSTANDING ACTIVATION BLOCKERS (prominent; none waived, none moved by this record)

Before any Owner activation authorization for `mechanical`, ALL of the following remain outstanding:
1. **OD-M2 clause 3 — the governed Mechanical safety-cue family** (F001 seam; provenance-tagged hazard vocabulary;
   focused/negative/mutation evidence; electronics non-degradation; complete + merged + post-merge verified). NOT
   started; NOT executed here.
2. **Tier-1 EN/AR Mechanical public label** (P9-MECH-QC §13; activation-readiness edge; CF-2 not absorbed).
3. **CF-6** (Web/CLI pre-classifier consistency remainder, incl. the CLI electronics literal) — OPEN, separate owner.
4. **CF-2** (public-message truthfulness beyond `/start`) — OPEN, separate owner.
5. **NMF-1 + FU-1** (pre-activation test-hardening carry-forwards) — their registered lane.
6. **Explicit Owner activation authorization** (§5-I2 allowlist gate) — never implied by qualification.
Residuals with separate owners, unaffected: dormant-weight cross-pack residual (shared-core); the stale
`progression_loop.py` comment-hygiene item (registered at the D-GMPR-D3-PN closure; documentation-level; NOT a §15
criterion and correctly outside this record); THERM-01/CAP-12/13/WS-PFV-001/D4/D8.

## §6. Scope of THIS candidate and next gate

Governance/documentation only: this NEW qualification record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. ZERO
runtime/test/pack/registry/activation/schema/persistence/ODR diff. **Next required gate: Mandatory Grill on this
exact candidate**, then the governed lifecycle. After this record merges, the natural next Owner decisions are the
activation-blocker gates (the OD-M2 clause-3 safety-family gate first among them) — each separately authorized;
nothing is auto-activated.
