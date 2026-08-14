# P9-MECH-SF — Governed Mechanical Safety-Cue Family — FORMAL CLOSURE RECORD (Candidate)

**Status of THIS record:** governance/documentation-only **FORMAL CLOSURE RECORD CANDIDATE** for the P9-MECH-SF
lane (OD-M2 clause 3 / D-P9-MECH-02). It implements nothing, changes no
runtime/test/pack/provenance/registry/activation/schema/persistence file, and closes NOTHING else. **The closure
statements in §4 become authoritative ONLY if/when this exact candidate is merged (create-a-merge-commit) and
post-merge verified** through the governed lifecycle (Mandatory Grill → independent external exact-candidate review
→ Owner acceptance → SHA-preserving publication → PR → pre/post-merge verification).
**`OWNER_DECISION_REGISTER.md` UNCHANGED** (closure-gate convention). **DOCUMENTED NO-VALID-RED.**

## §1. Closure basis and fresh verification

Base: `1a23552b75d68fac3741876651669e6192180b50` — the SHA-preserving merge (PR #484) of the accepted P9-MECH-SF
implementation candidate `2269d2d45fc202c164044e298138afc33c366d34` onto `d1b79ef4` (merge tree
`85a920e610a523dcef144af29cdab58ade910d53` == candidate tree; POST-MERGE PASS; freshly fetched; 0 newer; clean
tree). Fresh verification at THIS base:

- `has_governed_safety_cue_family("mechanical") is True`; `software` remains `False` (fail-safe preserved);
- focused suites: the safety-family evidence file **23**, I1 **18**, I2 **17**, I3 **18**, I4 **20**, I5 **16**,
  CF5-F001 seam **13**, D3 core neutrality **7**, D-GMPR-D3-PN **15** — all passed;
- full governed suite **2569 passed / 3 skipped / 1 xfailed / 0 failed** (parent-of-lane baseline 2546/3/1/0 + 23
  new evidence tests; zero regressions);
- `activated_domains() == ['electronics_electrical']`; `support_state("mechanical") ==
  "recognized_not_activated"`;
- declaration truthfulness cascade complete (the former "NOT COVERED pending…" wording survives nowhere in the
  merged pack); signal inventory byte-unchanged (canonical hashes `860ce084…`/`c14ae2d5…`); both re-frozen pack
  anchors verified at `a8a56450…`; `mechanical:PR005` present in the manifest.

## §2. Lineage (nothing reopened)

Contract lineage: first contract candidate `cfab650f` independently REJECTED (missed certain I5 pack-hash flip)
and preserved as immutable rejected evidence → corrected contract `349856de` accepted and merged (PR #483,
`d1b79ef4`) → implementation candidate `2269d2d4` created from that exact base, Grill-passed, independently
reviewed and accepted, published SHA-preserving, and merged (PR #484, **this base** `1a23552b`; merge tree ==
candidate tree; POST-MERGE PASS). The implementation delivered EXACTLY the contract §2 scope: the additive
governed `mechanical` entry in the F001 `_DOMAIN_CUE_FAMILIES` seam (electronics-precedent shape;
hazard-class-grounded, lay-accessible, detection-scoped, equality-pinned vocabulary; zero electronics-identity
collision; zero thermal vocabulary; provenance `mechanical:PR005`); the MANDATORY same-increment declaration
truthfulness cascade; the new 23-test evidence file; and EXACTLY the contract-§4 reconciliations in EXACTLY the
seven permitted files — the six certain family-presence flips and five certain declaration surfaces executed with
in-file disclosures (I4 AND I5 pack anchors re-frozen under ONE signal-inventory-unchanged proof; no corpus
rebuild), the four vocabulary-conditional derive-() pins verified UN-flipped. **No eighth reconciliation file was
required** (flip-sweep grep + zero-failure full suite). Electronics protection held: 24/24 electronics + None
derivation-corpus rows byte-identical; family constants hash-pinned; mutations m1–m10 all caught right-reason.

## §3. Independent-review observation disposition (non-blocking observations PRESERVED as observations — none is a closure blocker, none is silently dropped, none is converted into a new blocker)

1. **F001 focused count is 13, not the Creator-report's 15.** Recorded as the accurate count (fresh-verified in §1:
   the CF5-F001 seam file contains 13 tests). The Creator report's "15" was a transcription error (15 is the
   D-GMPR-D3-PN file's count); no test is missing — the file's introspection-free inventory was re-counted and every
   reconciled pin is present and green. Truth-of-record corrected here; no repository change required.
2. **`_MECH_CONTEXT_TERMS` are currently shape-parity content, unreachable in the current mechanical-domain call
   path.** Accurate and already truthfully documented in the merged module comment: the mechanical family is only
   consulted when the session domain IS `mechanical`, and the seam's owner branch then satisfies context directly.
   The terms are declared as shape-complete context vocabulary, NOT claimed as live behavior. Any future call-path
   change that would make them reachable belongs to its own governed gate. Non-blocking; no action.
3. **The capability/coverage declarations retain `provenance_ref: mechanical:PR002` while `mechanical:PR005`
   carries the cascade lineage.** Accurate: PR002 remains the declarations' ORIGIN record (the I1 gate), and the
   cascade's lineage is carried by PR005 plus the pack's `p9_mech_sf_safety_family` governance note and the
   evidence-file pins (which assert the PR005 references in the declaration statements and the note). This split
   is the same origin-vs-amendment layering the pack already uses for I2/I3 (PR003/PR004 amend content whose
   fields keep their origin refs). Recorded truthfully; not a defect; no action.
4. **Inherited negation / conservative-miss limitations.** The mechanical family inherits the F001/WS2 detection
   semantics unchanged — sentence-bounded conjunctive matching, finite token-anchored cue lists, negation/
   attribution vetoes, no stemming. Conservative misses (inventor hazard phrasings outside the finite vocabulary
   derive nothing) are the SAME truthful design property the electronics family has carried since WS2, and the
   empty tuple is never a safety statement (the caution/validation labeling is unchanged). Any vocabulary
   extension is a future governed change under the same equality-pin discipline. Non-blocking; no action.
5. **Additive governance note observation.** The cascade added the `p9_mech_sf_safety_family` note to the pack's
   `_governance_notes` (historical record of the replacement, the inventory-unchanged proof, and the NOT-ACTIVATED
   status). Additive-only alongside the prior i1/i2/i3/disposition notes, which are byte-unchanged; the note is
   evidence-pinned via the pack's PR005 references. Recorded; no action.

## §4. Closure statements (authoritative ONLY after this candidate's own merge + post-merge verification)

1. **The P9-MECH-SF implementation is AUTHORITATIVE** (merge `1a23552b`; §1 fresh verification; §2 lineage).
2. **The governed Mechanical safety-cue family EXISTS, is merged, and is post-merge verified.** Therefore
   **OD-M2 clause 3 (D-P9-MECH-02) — activation blocker #1 of the qualification record's §5 — is DISCHARGED**, at
   THIS closure gate and not before. The clause's requirement ("complete, merged, and post-merge verified BEFORE
   any Owner activation authorization") is now satisfied as evidence, discharging the blocker — NOT granting,
   implying, or advancing any activation authorization.
3. **The qualification status is unchanged in kind: `MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS;
   NOT ACTIVATED`** — the blocker set shrinks by exactly one. The qualification record's clause-2 prominent
   annotation retains its force with the remaining blockers (§5 below); this closure's governance sync is the
   recorded update path the qualification record itself specified.
4. **Mechanical remains NOT ACTIVATED**: `activated_domains() == ['electronics_electrical']`;
   `support_state("mechanical") == "recognized_not_activated"`; admission untouched; first new-domain activation
   remains BLOCKED.
5. **Electronics is preserved** — byte-identical family constants and derivation corpus outputs (24/24), unchanged
   None-default, full suite green (2569/3/1/0).
6. **The declaration truthfulness cascade is COMPLETE** (no stale NOT-COVERED-pending wording anywhere in the
   pack; "safety determination" remains NOT COVERED; detection-scoped statements equality-pinned), and the
   **signal inventory is unchanged** (the ONE canonical-hash proof behind both re-frozen I4/I5 pack anchors; no
   corpus rebuild was required or performed).

## §5. REMAINING ACTIVATION BLOCKERS (reconstructed from repository truth; none waived, combined, or executed here)

Before any Owner activation authorization for `mechanical`, ALL of the following remain outstanding:
1. **Tier-1 EN/AR Mechanical public label** (P9-MECH-QC §13; activation-readiness edge; correctly LAST of the
   technical blockers; CF-2 not absorbed).
2. **CF-6** (Web/CLI pre-classifier consistency remainder, incl. the CLI electronics literal) — OPEN, separate
   owner.
3. **CF-2** (public-message truthfulness beyond `/start`) — OPEN, separate owner.
4. **NMF-1 + FU-1** (pre-activation test-hardening carry-forwards) — disposition due no later than the
   pre-activation readiness review; their registered lane.
5. **Explicit Owner activation authorization** (§5-I2 allowlist gate) — never implied by qualification,
   family existence, or this closure.
Residuals with separate owners, unaffected: the dormant-weight cross-pack residual (shared-core); the stale
`progression_loop.py` comment-hygiene item; THERM-01 (future-only; untouched — no thermal vocabulary or claim
entered the family or declarations); CAP-12/13; WS-PFV-001; D4 REGISTERED / NOT AUTHORIZED; D8 Owner-reserved;
Phase 10 / PSRR / deployment NOT AUTHORIZED; no P9 closure.

## §6. Scope of THIS candidate and next gate

Governance/documentation only: this NEW closure record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. ZERO
runtime/test/pack/provenance/registry/activation/schema/persistence/ODR diff. **Next required gate: Mandatory
Grill on this exact candidate**, then the governed lifecycle through Owner-side SHA-preserving publication, PR,
and post-merge verification. After this closure merges, the natural next Owner decisions are the remaining
activation-blocker gates (§5) — each separately authorized; nothing is auto-activated.
