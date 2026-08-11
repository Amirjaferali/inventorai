# P9-E1 — Path-N Production Caller Domain Propagation — IMPLEMENTATION CONTRACT CANDIDATE

**Status:** GOVERNANCE-ONLY **CONTRACT CANDIDATE** — it becomes the authoritative implementation
contract-of-record only if independently reviewed, Owner-accepted, merged (create-a-merge-commit), and
post-merge verified. It defines the bounded scope, acceptance criteria, RED test design, rollback/safety
requirements, and exact non-goals for a **later, separately-run** P9-E1 implementation gate. **No runtime
change, no test change, and no domain activation is performed or authorized by this contract gate.**

**Gate identifier.** `P9-E1` = `P9-PREREQ-A` — Path-N production caller domain propagation: the mandatory
prerequisite registered by the D3 formal closure and carried into the now-authoritative Phase-9 Technical
Quality Standard (P9-QS §16: *"P9-PREREQ-A — Path-N production caller propagation … Trigger: BEFORE the first
second / non-electronics specialist-domain activation"*).

**Authorization.** Owner authorization begins Phase 9 **only** at this bounded gate. This contract gate does
**not** authorize: activation/selection of any new specialist domain; Mechanical or IoT activation; D8
disposition; P9-E2 implementation; D4 execution; multi-domain activated analysis; deterministic calculations;
CAP-12; CAP-13; WS-PFV; STG; Output-Language implementation; Phase 10; PSRR execution; deployment / production.

**Authoritative base.** `f08dd2e0319b2777c47dad9cdb49c05d106bc7a0` (live tip re-verified this gate; two-parent
merge PR #437 of base `99c0855` + the corrected P9-QS candidate `2f435c68`; P9-QS now AUTHORITATIVE; boot OK;
`activated_domains() == ['electronics_electrical']`). Built in a disposable worktree; primary working tree and
historical evidence bundles untouched; not newer than the live tip.

---

## §1. Purpose and framing

P9-E1 closes exactly one prerequisite: the shared Path-N question-selection seam already accepts a canonical
`domain` identity (added by D3-B), but the **production callers inside `engine/progression_loop.py` do not
propagate the session domain into it** — they rely on the backward-compatible `domain=None` default, so the
Electronics-owned Path-N artifact is served regardless of the session's canonical domain. Today this is
**non-blocking** (electronics is the only activated specialist domain, so no non-electronics specialist session
exists), but it MUST be closed **before any second / non-electronics specialist-domain activation**, so a
future foreign-domain session cannot silently inherit Electronics Path-N content.

P9-E1 is **caller propagation only**: thread the canonical domain that the callers already hold into the
existing domain-aware seam. It is **not** a redesign, a new router, a registry change, an activation change, or
any domain selection.

---

## §2. Live baseline evidence (independently verified at `f08dd2e`)

**The seam is already domain-aware (no change needed here).** `engine/path_n_questions.py`:
- `get_served_question(gap_type, iterations_open, domain=None)` (lines 76–117): `if domain is not None and
  domain != _ELECTRONICS_DOMAIN: return None` (line 92–93). `_ELECTRONICS_DOMAIN = "electronics_electrical"`
  (line 29).
- `get_path_n_question(gap_type, iterations_open, domain=None)` (lines 120–129): thin wrapper that already
  forwards `domain=domain` to `get_served_question` (line 128).

**The production callers drop the domain (the gap).** `engine/progression_loop.py`:
- `get_question(domain, gap_type, iterations_open, path=None)` (def line 213): on `path == "N"` it calls
  **`get_path_n_question(gap_type, iterations_open)`** at **line 232** — the in-scope `domain` parameter is NOT
  threaded.
- `get_display_question(domain, gap_type, iterations_open, path=None)` (def line 247): on `path == "N"` it
  calls **`get_path_n_question(gap_type, iterations_open)`** at **line 269** and
  **`get_path_n_question(gap_type, iterations_open - 1)`** at **lines 273–274** (the stall-reframe
  exhaustion comparison) — the in-scope `domain` parameter is NOT threaded at either call.

**Canonical domain identity is available at every caller.** `get_question` and `get_display_question` both
receive `domain` as their first parameter, supplied by their own callers as the canonical session domain:
- `web/app.py:1566` → `get_display_question(getattr(state, "domain", None), gap_type, iterations_open,
  path=state.path)` (the `/start_ilt002_combination_lock_path_n` non-specialist Path-N route; the `/start`
  routes attach `state.domain`).
- `engine/progression_loop.py:904, 944, 981` → `get_question(state.domain, …, path=state.path)` (internal
  cascade callers; `state.path` may be `"N"`).
- `scripts/run_cli.py:79` → `get_question(state.domain, gap_type, iters_open)` (CLI; default path, not `"N"`).

**No other production caller and no hidden domain-blind path.** The only non-test production callers of
`get_path_n_question` are the three sites above (all inside `progression_loop.py`); there is **no** direct
production caller of `get_served_question` outside the `get_path_n_question` wrapper (verified by
repository-wide search). Threading `domain` at those three sites closes the seam completely.

**Behavioral proof of the live defect (executed at `f08dd2e`).** With `MECHANISM_COMPLETENESS` (a Stage-2 gap
present in BOTH the Electronics Path-N artifact and the generic `QUESTIONS` fallthrough, whose texts differ):
- `domain_activation.support_state("mechanical") == "recognized_not_activated"`;
  `support_state("electronics_electrical") == "activated"`.
- `progression_loop.get_question("mechanical", "MECHANISM_COMPLETENESS", 0, path="N")` returns the **Electronics
  artifact text** (domain-blind) — it does NOT fall through to the domain-neutral generic variant.
- `progression_loop.get_question("electronics_electrical", "MECHANISM_COMPLETENESS", 0, path="N")` returns the
  Electronics artifact text (correct; must remain unchanged).
- The seam already yields the correct value for a foreign domain:
  `path_n_questions.get_path_n_question("MECHANISM_COMPLETENESS", 0, domain="mechanical") is None`.

**Conclusion: P9-E1 IS STILL REQUIRED.** The prerequisite has not been satisfied by later work; the gap is live
and isolated to caller propagation.

---

## §3. Bounded implementation scope (for the later implementation gate)

Minimum required to propagate canonical domain identity from the progression callers into the existing
domain-aware Path-N selection. Expected pattern:

> existing canonical caller `domain` → existing `get_path_n_question(..., domain=...)` → domain-aware Path-N
> resolution (foreign recognized domain → `None` → existing generic fallthrough).

Exactly three call sites change, all in `engine/progression_loop.py`:
1. `get_question` line 232: `get_path_n_question(gap_type, iterations_open)` →
   `get_path_n_question(gap_type, iterations_open, domain=domain)`.
2. `get_display_question` line 269: `get_path_n_question(gap_type, iterations_open)` →
   `get_path_n_question(gap_type, iterations_open, domain=domain)`.
3. `get_display_question` lines 273–274: `get_path_n_question(gap_type, iterations_open - 1)` →
   `get_path_n_question(gap_type, iterations_open - 1, domain=domain)`.

No signature change is required (`domain` is already the first parameter of both functions). No change to the
seam, the artifact, the registry, the activation policy, the web routes, or the CLI. Comment/docstring updates
adjacent to the three sites are permitted for accuracy; no other edits.

**Reframe correctness note (must be preserved, not redesigned).** In `get_display_question`, once domain is
threaded, a recognized-not-activated domain yields `current is None` at line 269, so the `if current is not
None …` reframe branch is skipped and control falls through to `get_question(...)` → generic variant. The
Electronics-specific stall reframe (`_STALL_REFRAME`) therefore correctly does NOT fire for a foreign domain,
and Electronics/`None` reframe behavior is byte-for-byte unchanged. The implementation MUST preserve this; it
MUST NOT add domain-specific branching to compute the reframe.

---

## §4. Explicit non-goals (STOP-and-report if any becomes tempting)

P9-E1 MUST NOT: redesign Path-N; add a second question router/framework; add or change Domain Registry logic;
activate or select any domain (no Mechanical, no IoT, no "first future domain"); modify the §5-I2 activation
policy (`_ACTIVATED_DOMAINS`); add domain-specific `if/elif` branching to shared core; add Mechanical/IoT
content; modify Domain Packs (`docs/governance/path_n_content_config/**`, `domains/**`) — including
`domains/iot_electronics/**` (D8, Owner-reserved); touch `web/app.py` routing/state/method behavior; broaden
into P9-E2 (`sorted(activated_tied)[0]` tie precedence); broaden into D4 (multi-domain composition); implement
deterministic calculations, CAP-12, CAP-13, WS-PFV, STG, or Output-Language; start Phase 10; execute PSRR; or
touch deployment/production. If live evidence during implementation shows any of these is *inseparable* from
the propagation, STOP and report the coupling rather than broadening automatically.

---

## §5. Acceptance criteria (implementation gate)

The P9-E1 implementation gate is acceptable only if ALL hold:

1. Canonical domain identity is threaded through **every** relevant production Path-N caller — the three sites
   in §3 (the complete set; no other production caller of the seam exists at the authoritative base).
2. Electronics behavior is **unchanged** for the currently activated domain: `get_question` /
   `get_display_question` with `domain == "electronics_electrical"` (and the backward-compatible `domain=None`
   default) return exactly the same text, reframe, and fallthrough as the baseline.
3. An explicit **non-electronics recognized-not-activated** domain (neutral fixture, e.g. `"mechanical"`)
   reaches the existing domain-aware selection path in tests **without any activation**: on `path == "N"` it no
   longer receives Electronics artifact content and instead falls through to the existing generic variant.
4. Unsupported / not-activated domain semantics remain **honest**: no foreign-domain session is served
   Electronics-owned content; no fabricated per-domain Path-N content is invented (the seam returns `None` and
   the existing generic fallthrough governs).
5. No new specialist domain is activated (`activated_domains() == ['electronics_electrical']` unchanged).
6. No new shared-core domain-specific `if/elif` branching is introduced (propagation only).
7. No duplicate question router / parallel question framework is introduced.
8. No change to the §5-I2 activation policy (`engine/domain_activation.py`).
9. No change to D8 (`domains/iot_electronics/**` untouched).
10. No change to D4 (no multi-domain composition).
11. No P9-E2 implementation (`sorted(activated_tied)[0]` in `engine/domain_rules.py` untouched).
12. Focused **RED→GREEN** tests prove the propagation gap (§6): RED on the live baseline, GREEN only after the
    bounded propagation; at least one load-bearing mutation probe per corrected site turns a targeted test RED
    and is restored byte-identical.
13. The full regression suite remains green at the implementation gate (baseline: 2258 passed / 3 skipped / 1
    xfailed / 0 failed; a skip is not a pass — count preserved or the delta explained by the new tests only).
14. P9-QS quality rules are preserved (recognition ≠ qualification ≠ authorization ≠ activation; canonical
    owners consumed, never duplicated; evidence-vs-assumption honesty; deterministic selection).
15. No unrelated web/schema/prompt/governance/benchmark expansion; changed runtime paths limited to
    `engine/progression_loop.py` + the new focused test file.
16. *(Repository-evidenced addition.)* The `get_display_question` stall-reframe path is preserved exactly for
    Electronics/`None` and correctly suppressed (falls through to the generic variant, no `_STALL_REFRAME`) for
    a recognized-not-activated foreign domain — proven by test, not by inspection.

---

## §6. RED test design (specified here; IMPLEMENTED ONLY at the later gate)

Behavioral tests (assert selection behavior, not source text). Neutral fixture domain: `"mechanical"`
(recognized-not-activated; used only as an example fixture per repository convention — no domain sequence is
chosen). Gap: `MECHANISM_COMPLETENESS` (Stage-2; present in both the artifact and generic `QUESTIONS`; texts
differ). Proposed location: `tests/test_p9e1_path_n_caller_domain_propagation.py`.

- **RED-1 (get_question foreign-domain fallthrough).** Assert
  `get_question("mechanical", "MECHANISM_COMPLETENESS", 0, path="N")` **equals the generic `QUESTIONS` variant**
  and **does not equal** the Electronics artifact text. On the live baseline it returns the Electronics artifact
  text → **RED**. After propagation → generic variant → **GREEN**.
- **RED-2 (get_display_question foreign-domain fallthrough + no Electronics reframe).** Assert
  `get_display_question("mechanical", "MECHANISM_COMPLETENESS", iterations_open, path="N")` (at an
  exhaustion-triggering position) **does not equal** the Electronics artifact text and **does not equal**
  `_STALL_REFRAME`, and **equals** the generic variant. RED on baseline (returns Electronics text or the
  Electronics reframe) → GREEN after the fix.
- **GREEN-guard-1 (Electronics unchanged).** Assert `get_question("electronics_electrical",
  "MECHANISM_COMPLETENESS", 0, path="N")` still returns the Electronics artifact text, and that the `domain=None`
  default (`get_path_n_question(gap, it)`) is unchanged — guards against over-fix. Passes on baseline and after
  the fix.
- **GREEN-guard-2 (Electronics reframe unchanged).** Assert the Electronics/`None` stall-reframe still fires at
  the exhaustion position. Passes on baseline and after the fix.

Mutation probes (implementation gate): reverting each of the three threaded `domain=domain` arguments
individually must turn RED-1 or RED-2 red; restore byte-identical.

The RED tests MUST fail on the live baseline for the stated behavioral reason (domain not propagated), not
because of source-string inspection.

---

## §7. Rollback / safety requirements

- The change is a pure additive keyword-argument propagation with an unchanged default; it is trivially
  reversible by removing the three `domain=domain` arguments (returns to baseline behavior).
- Fail-closed / honest-unknown behavior is preserved: a missing/`None` domain still serves the
  backward-compatible Electronics default (existing external callers unchanged); a recognized foreign domain
  falls through to the domain-neutral generic variant; an unsupported domain is never served fabricated
  content.
- No persistence, schema, I/O, LLM, or scoring behavior is touched; the Path-N flow remains
  deterministic and non-AI.
- Deterministic: no `Date.now`/randomness; selection is position-clamped as before.

---

## §8. Separation of adjacent gates (must remain separate)

- **P9-E2 / P9-PREREQ-B — governed multi-activated tie/conflict precedence** (`sorted(activated_tied)[0]` in
  `engine/domain_rules.py`) is a **separate future execution gate**. P9-E1 MUST NOT fix it. Live evidence shows
  it is separable: the tie-break lives in `infer_domain`, not in the Path-N caller chain, and is deterministic
  with one activated domain. If implementation reveals inseparability, STOP and report the coupling.
- **D4 — multi-domain activated composition** remains a later gate. P9-E1 is caller propagation only; no
  subsystem composition.
- **D8 — `iot_electronics`** remains Owner-reserved; `domains/iot_electronics/**` untouched; no IoT sequencing
  decided.

---

## §9. Governance scope of THIS contract candidate

Governance docs only:
- NEW `docs/governance/P9_E1_PATH_N_CALLER_DOMAIN_PROPAGATION_CONTRACT.md` (this file);
- `docs/governance/ACTIVE_EXECUTION_ROADMAP.md` (append-only entry);
- `docs/governance/ACTIVE_INCREMENT_CONTRACT.md` (current-truth sync; prior P9-QS block demoted to history);
- `docs/governance/CURRENT_PROJECT_STATE.md` (current-truth paragraph).

`OWNER_DECISION_REGISTER.md` **UNCHANGED** — P9-E1 is a governance-registered engineering prerequisite, not a
new accepted Owner product-policy decision (consistent with D3 / P8-AF / P8-CLOSE / P9-QS candidate precedent).
**ZERO** runtime / test / schema / prompt / benchmark / web / CI diff in this contract gate.

---

## §10. Candidate-vs-authoritative boundary

**P9-E1 = CONTRACT CANDIDATE ONLY.** It becomes the authoritative implementation contract-of-record only if
this exact accepted candidate is independently reviewed, Owner-accepted, merged (create-a-merge-commit), and
post-merge verified. The P9-E1 **runtime implementation and its tests are a separate, later, separately-run
gate** — NOT authorized by this contract gate. No domain is activated or selected here. Phase 9 has begun only
through this bounded gate; Phase 10 NOT AUTHORIZED; PSRR NOT EXECUTED; deployment / production NOT AUTHORIZED.
