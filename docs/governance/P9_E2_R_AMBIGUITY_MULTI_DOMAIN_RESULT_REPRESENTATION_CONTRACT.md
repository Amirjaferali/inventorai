# P9-E2-R — Ambiguity / Multi-Domain Result Representation — IMPLEMENTATION CONTRACT CANDIDATE (bounded sub-gate, CORRECTED)

**Status of THIS record:** governance-only **CONTRACT CANDIDATE** — authoritative only if independently reviewed, Owner-accepted,
merged (create-a-merge-commit), and post-merge verified. It defines the bounded representation design, caller-safety matrix,
acceptance criteria, RED behavioral-test design, invariants, and exact non-goals for a **later, separately-run** P9-E2-R
implementation gate. **No runtime change, no test change, no domain activation, and no domain selection is performed or authorized
by this contract-first step.** **DOCUMENTED NO-VALID-RED / CONTRACT-FIRST** (RED tests are *designed* here, not implemented).

**Gate identifier.** `P9-E2-R` — the bounded inference-result representation sub-gate called out by the authoritative P9-E2
contract §6 as a prerequisite for honest Case-3 (ambiguous tie) / Case-4 (multi-domain) behavior.

**Correction lineage (this is the corrected reissue).** The immediately prior P9-E2-R candidate
`1b817f06e7d86b3af6e44b298bcf7a31102e5e32` was **REJECTED for publication by a Mandatory adversarial Grill** and **remains
immutable historical evidence only — NOT amended, NOT merged, NOT reused**. This is a **NEW independent candidate created from the
current authoritative parent `47fce397dfd21175a0012b652f8dde6548e31432`**, not a repair of the rejected SHA. The Grill's material
findings are incorporated here (see §22, "Grill-correction ledger"): fail-loud legacy wrapper + RED-R9; mandatory migration of all
six `web.app.infer_domain` monkeypatch surfaces; architecture-guardrail reconciliation of `infer_domain -> str | None` versus the
fail-loud richer-kind behavior; dispatch-by-kind (never truthiness/string comparison of the structured object) at web + CLI;
RED-R10 (`/start × MULTI_DOMAIN_NEEDS_D4`) and RED-R11 (CLI bounded stop); `state.domain` must remain a resolved string;
strengthened result invariants; deterministic/non-LLM `reason` semantics; a defensive type boundary preventing silent swallowing
of a `DomainClassification` by `str`-expecting activation/domain-id code; registration of the line-34 future Nth-domain
fallthrough hazard; and an explicit governance/risk classification of the future implementation.

**Authorization boundaries.** This authorization covers the full P9-E2-R governance + implementation lifecycle. It does **NOT**
authorize: the general P9-E2 tie-precedence runtime beyond what is strictly necessary to establish/consume the representation
seam; any new specialist-domain activation; any domain selection; D4 execution; D8 disposition; CAP-12 / CAP-13 / WS-PFV;
deterministic calculation capability; Phase 10; PSRR; deployment / production.

**Authoritative base.** `47fce397dfd21175a0012b652f8dde6548e31432` (live tip re-verified; PR #441 = two-parent merge of
`05184f91` + the P9-E2 contract candidate `1d29a26f`, merge tree `1f3cbf99` == candidate tree; **P9-E2 contract now
AUTHORITATIVE**; P9-E1 remains FORMALLY CLOSED / SATISFIED; boot OK; `activated_domains() == ['electronics_electrical']`; P9-E2
runtime + P9-E2-R unimplemented; D4 unexecuted; D8 Owner-reserved). Built in a disposable worktree; primary working tree +
historical bundles untouched; not newer.

---

## §1. Live baseline and confirmed representation gap

**Current result type (verified at `47fce39`):** `engine/domain_rules.py::infer_domain(idea_text: str) -> str | None`
(annotation confirmed at runtime). It returns a single domain id, or `None`, and therefore **conflates**: (1) genuine no-match;
(2) recognized-but-unsupported; (3) an activated-domain tie with no governed winner; (4) the tied candidate **set**; (5) a genuine
multi-domain-needs-D4 situation.

**Critical production consequence (independent reviewer + Grill — CONFIRMED live).** In `web/app.py` `/start`
(lines 1363–1398): `domain = infer_domain(idea_text)`, then `_has_strong_unsupported_evidence(lowered)` (line 1368) may reject
first; `domain == "electronics_electrical"` → admitted; `domain in {"mechanical","medical_device","software"}`
(`CONFLICTING_SUPPORTED_DOMAINS`, line 845) → corroboration/guidance; `elif domain is not None` (line 1389) → refuse
`UNSUPPORTED_DOMAIN_MESSAGE`; **`domain is None` (lines 1393–1394) → admitted under explicit confirmation as electronics**
(`_admit_specialist_domain(DOMAIN_CONFIRM_VALUE == "electronics_electrical")`). **Therefore an ambiguous activated tie MUST NOT be
represented as ordinary `None`** (silent electronics admission), nor as a bare non-electronics string (refused as "unsupported"),
nor as a naive structured object (breaks the `== "electronics_electrical"` / `in CONFLICTING_SUPPORTED_DOMAINS` string comparisons
**and** the SINGLE-electronics admission path).

**CLI (`scripts/run_cli.py` lines 35–45):** `domain = infer_domain(idea)`; `print(f"Domain inferred: {domain or 'unknown'}")`;
`if domain != "electronics_electrical":` → "OUTSIDE MVP SCOPE" and return. A structured object would **stringify** in the f-string
(leaking `DomainClassification(...)` text) and break the comparison — the CLI must also dispatch by kind (§7.2).

**Architecture guardrail (verified).** `ARCHITECTURE_GUARDRAILS.md` (lines 103–104, "TEST 5") **freezes**
`infer_domain(idea_text: str) -> str | None`; `tests/test_architecture_guardrails.py::test_returns_str_or_none` asserts
`infer_domain(inp)` returns `str` or `None` for a fixed input set (all of which yield SINGLE/NONE today). Retaining the wrapper
preserves this frozen signature; the fail-loud richer-kind behavior (§4) requires an explicit, governed reconciliation of that
guardrail (§4.1).

**Reachability today:** with only `electronics_electrical` activated, an activated tie is **unreachable**; `infer_domain` today
yields only SINGLE (electronics, or a recognized-not-activated domain via the line-34 `priority` literal) or `None`. P9-E2-R
installs the representation seam so the **future** P9-E2 runtime can express ambiguity honestly and the callers are pre-safe.

---

## §2. Core representation design goal (the result kinds)

Distinguish, truthfully and deterministically, at least:
- **A. SINGLE** — one domain is the justified classification result (`selected_domain` present).
- **B. NONE** — no supported classification / no usable match.
- **C. AMBIGUOUS_TIE** — two or more **activated** specialist-domain candidates are tied and no governed winner exists.
- **D. MULTI_DOMAIN_NEEDS_D4** — evidence indicates a genuine multi-domain situation that cannot truthfully be collapsed to one
  domain and requires later D4 handling (a **marker/state only** — no composition; §16).

---

## §3. Recommended representation architecture (minimum-sufficient; retained)

Owned by the existing classification seam `engine/domain_rules.py` (one canonical classifier owner — no parallel classifier):
- `class DomainResultKind(enum.Enum): SINGLE; NONE; AMBIGUOUS_TIE; MULTI_DOMAIN_NEEDS_D4`.
- `@dataclass(frozen=True) class DomainClassification:` fields — `kind: DomainResultKind`; `selected_domain: str | None`;
  `candidates: tuple[str, ...]`; `reason: <deterministic enum/code> | None` (§12); optional minimal `score` / `matched_signals` /
  `policy_version` only with a named use (§13). **Frozen/immutable** (§11).
- **Canonical richer entry point** `classify_domain(idea_text: str) -> DomainClassification` — the single source of classification
  truth. Today it produces only SINGLE / NONE (behavior-equivalent to current `infer_domain`; it adds **no** tie detection — that
  is the later P9-E2 runtime, §8).
- **Legacy compatibility wrapper** `infer_domain(idea_text: str) -> str | None` — a thin wrapper over `classify_domain` (§4).

P9-E2-R MUST NOT create: a new orchestration/Result framework; a second router; a new registry; a new activation engine; or broad
schema infrastructure.

## §4. Legacy `infer_domain()` compatibility wrapper — FAIL-LOUD (corrected)

`infer_domain` delegates to `classify_domain` and maps **only** the two currently-reachable kinds: `SINGLE → selected_domain`;
`NONE → None`. For **AMBIGUOUS_TIE** and **MULTI_DOMAIN_NEEDS_D4** the wrapper **MUST fail loud** — it **MUST raise a dedicated,
bounded exception** (a purpose-named exception such as `AmbiguousDomainResultError`, a subclass of a standard runtime exception;
**NOT** `AssertionError`, which is elided under `python -O`; **NOT** a silent `return None`, which would reintroduce the §1 silent
electronics-admission hazard). The wrapper MUST **never** return `None` or an arbitrary domain for a richer kind. The wrapper is
**total over {SINGLE, NONE}** and **fail-loud over {AMBIGUOUS_TIE, MULTI_DOMAIN_NEEDS_D4}**. It MUST be marked **LEGACY** in code
comments and docs; **new production admission callers MUST use `classify_domain` and dispatch by `kind`** (§7); `infer_domain`
survives only for the frozen-guardrail signature and any legacy/test consumers that only ever encounter SINGLE/NONE. Because the
richer kinds are unreachable today, the wrapper is behavior-identical for every currently-reachable input — no currently-reachable
caller is silently broken — while the fail-loud rule guarantees that if a richer kind ever flows through the legacy seam it
**aborts loudly instead of being silently mis-admitted.**

### §4.1 Architecture-guardrail reconciliation (corrected)
The fail-loud wrapper and the frozen `-> str | None` guardrail are in tension (a fail-loud wrapper is **partial**, not a total
`str | None` function). The implementation gate MUST reconcile them explicitly: **update `ARCHITECTURE_GUARDRAILS.md`** to (a)
record `classify_domain(...) -> DomainClassification` as the **richer canonical classification entry** (single classifier owner;
`infer_domain` is the legacy wrapper over it); (b) state that `infer_domain` is **total over SINGLE/NONE and intentionally
fail-loud (raises) over richer kinds** — a governed, deliberate signature refinement, not drift; (c) require **new production
admission callers to consume `classify_domain` by kind**, not the legacy wrapper. The guardrail **test** may remain green (its
fixed inputs yield only SINGLE/NONE); the implementation MUST NOT weaken `test_returns_str_or_none` and SHOULD add a guardrail test
asserting the wrapper **raises** on richer kinds (RED-R9) and that the single-classifier-owner invariant holds. If reconciling
would require weakening an existing guardrail assertion, **STOP and report** rather than silently relaxing a guardrail.

## §5. Backward compatibility (bounded; proven, not assumed)

Exactly one classifier implementation (`classify_domain`); `infer_domain` delegates (no duplicate logic). Currently-reachable
inputs are behavior-identical (§1 reachability). The two admission callers (`web/app.py` `/start`, `scripts/run_cli.py`) migrate
to `classify_domain` (§7) so ambiguity never flows through the `str | None` bottleneck; the legacy wrapper's fail-loud rule (§4)
is the backstop, not the primary path.

## §6. Candidate-set semantics (minimum only)

`AMBIGUOUS_TIE` / `MULTI_DOMAIN_NEEDS_D4` carry the **canonicalized candidate domain ids** (deterministic ordering, §9) and a
deterministic `reason` (§12). Optional `score` / per-candidate `matched_signals` / `policy_version` permitted **only** with a named
current use for truthfulness / deterministic tests / explainability / safe caller handling / future D4 handoff — not overbuilt.
SINGLE carries `selected_domain` and an **empty** candidate set; NONE carries no candidate set. **No fabricated confidence.**

## §7. Caller behavior matrix — DISPATCH BY KIND (corrected)

Both admission callers migrate to `classify_domain` and **branch on `result.kind`** — **never** on truthiness of, or a `==` /
`in` string comparison against, the `DomainClassification` object.

| kind | `web/app.py` `/start` | `scripts/run_cli.py` |
|---|---|---|
| **SINGLE** (electronics) | current electronics admission (unchanged) | proceed (unchanged) |
| **SINGLE** (recognized-not-activated) | current `CONFLICTING_SUPPORTED_DOMAINS` / refuse behavior (unchanged) | "OUTSIDE MVP SCOPE" (unchanged) |
| **NONE** | current explicit-confirmation electronics fallback (unchanged) | "OUTSIDE MVP SCOPE" (unchanged) |
| **AMBIGUOUS_TIE** | **MUST NOT enter the `None` fallback**; fail closed — no session; truthful clarification/ambiguity via an existing surface; never admit as electronics; never a winner | explicit **bounded stop**; never print an arbitrary winner, never treat as `None`, never activate, never D4 |
| **MULTI_DOMAIN_NEEDS_D4** | **MUST NOT be silently admitted as one domain**; fail closed with a truthful deferred/unavailable state via an existing surface; never execute D4; wording MUST NOT imply multi-domain analysis occurred (§16) | explicit **bounded stop**; same constraints; never D4 |

**§7.1 Web.** SINGLE(kind, selected_domain)→current branches exactly (dispatch on kind + `selected_domain` string, not on the
object). NONE→current None-fallback. AMBIGUOUS_TIE / MULTI_DOMAIN_NEEDS_D4→a **fail-closed** branch that does **not** reach the
line-1393 `None` fallback and does **not** admit/print an arbitrary domain. Minimum bounded behavior = fail-closed
refusal/clarification via an **existing** surface; **no new public UX** (§14). `state.domain` MUST remain a **resolved domain
string** (from `_admit_specialist_domain(...)`), **never** the `DomainClassification` object (§10).

**§7.2 CLI.** Dispatch on `result.kind`. SINGLE(electronics)→proceed; SINGLE(other)/NONE→"OUTSIDE MVP SCOPE";
AMBIGUOUS_TIE / MULTI_DOMAIN_NEEDS_D4→an explicit bounded stop message; **never** stringify the object into output, never an
arbitrary winner, never `None`-silent, never activation, never D4.

**§7.3 Monkeypatch-surface migration (corrected — mandatory, load-bearing).** Six live tests currently
`monkeypatch.setattr("web.app.infer_domain", …)` — `tests/test_web_app.py` lines **563, 575, 589, 661, 701, 790**. After `/start`
migrates to `classify_domain`, these patches would **stop intercepting the classifier**, leaving the tests green but no longer
exercising the admission path they name (a silent test detachment — a P9-QS no-silent-migration violation). The implementation
gate **MUST migrate every one of these surfaces** to patch the seam actually consumed (`web.app.classify_domain`, or the exact
imported symbol `/start` calls), returning `DomainClassification` values, and **MUST prove each migrated test still exercises the
real admission branch** (e.g. a deliberate mutation of the migrated call makes the test fail). No monkeypatch of the classifier
may be left detached. A repository-wide sweep for any other `infer_domain` patch/import consumer is required at implementation.

## §8. P9-E2 relationship (seam only; separable)

P9-E2-R creates the **representation seam only** and does **NOT** decide tie precedence. The tie *detection/policy* lives in
`infer_domain`'s block (lines 22–38) and is **separable**: `classify_domain` today reproduces current SINGLE/NONE behavior exactly
(one activated domain ⇒ no tie), so no selection behavior changes. The later P9-E2 runtime will populate AMBIGUOUS_TIE /
MULTI_DOMAIN_NEEDS_D4. If implementation reveals the representation cannot be installed without changing tie selection behavior,
**STOP and report.**

## §9. Deterministic ordering is NOT precedence (explicit)

Candidate ids MAY be canonicalized (e.g. sorted) for deterministic storage/test equality. **`canonical order != precedence`.**
No code or later gate may read candidate order as winner precedence; an AMBIGUOUS_TIE has **no** selected winner regardless of
order. Duplicate candidate ids are **rejected**, not silently deduped (§11).

## §10. `state.domain` invariant (corrected)

`state.domain` and `state.domain_signal` MUST remain a **resolved domain string** (assigned by `_admit_specialist_domain(...)`),
**never** a `DomainClassification` object. Verified: `web/app.py` line 1403 and `engine/session_reconstruction.py` lines 166–167
persist/restore a string `confirmed_domain`; the richer result is consumed for the admission **decision** only and never assigned
to session state (so it never crosses into persistence/reconstruction/export — §15). The implementation MUST preserve this.

## §11. Representation invariants (strengthened — corrected)

- Result `kind` is explicit and is exactly one of the four.
- **Immutable** result (frozen dataclass; mutation attempts raise).
- **SINGLE:** exactly one `selected_domain`, which is **registry-recognized**; candidate set **empty**.
- **AMBIGUOUS_TIE:** **≥2** candidates; **no** `selected_domain`; **all candidates activated** (no recognized-not-activated domain
  may appear — guards D3-D).
- **MULTI_DOMAIN_NEEDS_D4:** **≥2** relevant candidates; **no** `selected_domain`; **no** implicit composition.
- **NONE:** no candidate set (unless repository evidence later requires diagnostic data) and no `selected_domain`.
- **Mutual exclusion:** a non-empty tie/relevant candidate set and a `selected_domain` are mutually exclusive.
- **Unique candidate ids** (no duplicates); ids are **canonicalized deterministically**; **canonicalization ≠ precedence** (§9).
- **No result kind changes activation state**; no result object contains fabricated confidence.

## §12. Deterministic / non-LLM `reason` semantics (corrected)

`reason` MUST be a **deterministic machine value** — a fixed enum/code (e.g. `EQUAL_SCORE`, `INSUFFICIENT_EVIDENCE`,
`OVERLAPPING_SCOPE`, `MULTI_DOMAIN`) — **not** free-form or model-generated prose. **No LLM/AI** participates in producing the
result or its `reason`. Any human-readable message is rendered at the caller from the deterministic code, so the representation
never implies reasoning/certainty beyond the classifier's evidence (§18).

## §13. Provenance / persistence / schema boundary

Minimum metadata: `kind`; `selected_domain` (SINGLE); `candidates` (C/D); deterministic `reason`. Optional `score` /
`matched_signals` / `policy_version` only with a named use. **No** database / session-persistence / schema migration — P9-E2-R is a
runtime classification result only (and, per §10, never reaches persisted state). If result persistence is ever required for
correctness, **STOP** and identify a bounded separately-reviewed sub-gate.

## §14. UI boundary

**No UI redesign.** Goal = safe caller behavior, not a new multi-domain UX. Minimum bounded behavior for ambiguity/multi at the web
boundary is fail-closed via an **existing** error/clarification surface. **If truthful public ambiguity/multi messaging cannot be
expressed with an existing surface, STOP and report a separately-reviewed UI sub-gate** — do not hide new UX in P9-E2-R.

## §15. API / integration boundary

The structured `DomainClassification` is an **internal** runtime type; it MUST NOT cross an existing public API / integration
contract boundary. Traced `classifier → /start → state.domain (resolved string) → session_reconstruction/record/export` — the
richer object does **not** cross into any persisted/external surface (§10). If a future change would make it cross such a boundary,
**STOP** before altering any external schema without a separately-governed contract.

## §16. D4 boundary

`MULTI_DOMAIN_NEEDS_D4` is only a **truthful marker/state.** P9-E2-R MUST NOT: execute multiple Domain Packs; combine questions;
combine gaps; reconcile contradictions; merge outputs; or decide cross-domain ownership (all D4). **Public/CLI wording MUST NOT
imply that multi-domain analysis occurred** — it must truthfully say the system cannot process this as a single supported domain
yet.

## §17. D8 boundary

`domains/iot_electronics/**` remains untouched and Owner-reserved. No D8 choice, no IoT activation/selection.

## §18. False-certainty / epistemic boundary

The representation carries **classifier state only**, never engineering truth beyond its evidence: SINGLE is not emitted on weaker
evidence than current thresholds; MULTI_DOMAIN_NEEDS_D4 is a *marker of need*, not a proven multi-domain claim; `reason` is a
deterministic code (§12); the candidate set is the classifier's matched set, not an exhaustive engineering enumeration.

## §19. Defensive type boundary at the activation/domain-id seam (corrected)

`engine/domain_activation._resolve_pack_id` silently returns `None` for a non-`str` input (`if not isinstance(domain, str) …`), so
a `DomainClassification` accidentally passed to `support_state` / `is_activated` (or any `str`-expecting domain-id code) would be
**silently swallowed** as `UNKNOWN_OR_UNSUPPORTED` — another silent truth-loss path. The implementation MUST add a **defensive
fail-loud boundary** (a type assertion/guard at the classifier→admission→activation seam so a `DomainClassification` can never be
silently coerced to "unknown domain") **and** a defensive test proving it fails loud. This does not change activation policy
(§5-I2) and activates nothing.

## §20. RED behavioral test design (designed; IMPLEMENTED ONLY at the later gate)

Self-restoring test doubles only (patch `domain_activation._ACTIVATED_DOMAINS` and restore; construct `DomainClassification`
values directly; patch the **migrated** classifier seam for caller tests). **NO real domain activation.** Proposed:
`tests/test_p9e2r_result_representation.py` (+ migrated caller tests in `tests/test_web_app.py` and a CLI test).

- **RED-R1** — AMBIGUOUS_TIE is a distinct representation, not `None`, not a single domain.
- **RED-R2** — `/start` caller safety: an AMBIGUOUS_TIE result MUST NOT enter the `None` fallback (no electronics session).
- **RED-R3** — MULTI_DOMAIN_NEEDS_D4 distinguishable from SINGLE; never silently one domain.
- **RED-R4** — candidate-order determinism; canonical order used for equality but **not** precedence (no `selected_domain` on
  AMBIGUOUS_TIE regardless of order).
- **RED-R5** — recognized-not-activated exclusion (only activated domains form tie candidates; D3-D).
- **RED-R6** — genuine no-match still behaves as NONE and preserves current safe fallback.
- **RED-R7** — line-34 no-activated-tie fallback behaviorally unchanged (GREEN guard).
- **RED-R8** — ≥3-way activated tie remains deterministic and preserves the **full** tied candidate set (no pairwise collapse).
- **RED-R9 (corrected)** — the **legacy `infer_domain` wrapper fails loud** (raises the dedicated exception) on AMBIGUOUS_TIE and
  MULTI_DOMAIN_NEEDS_D4, and never returns `None`/an arbitrary domain for them; total over SINGLE/NONE.
- **RED-R10 (corrected)** — **`/start` × MULTI_DOMAIN_NEEDS_D4**: fails closed to a truthful deferred state, distinct from the
  AMBIGUOUS_TIE path and from the `None` fallback; never admitted as one domain; never D4.
- **RED-R11 (corrected)** — **CLI bounded stop**: AMBIGUOUS_TIE and MULTI_DOMAIN_NEEDS_D4 produce an explicit bounded stop, never
  an arbitrary winner, never a stringified object, never activation/D4.
- **Additional (required):** duplicate-candidate **rejection**; empty/singleton tie **impossible** (constructor rejects);
  frozen-result **mutation raises**; **migrated-monkeypatch load-bearing** proof (a mutation of the migrated admission call fails
  the migrated web tests); defensive **type-boundary** fail-loud (§19).

All RED tests must fail on the live baseline for the stated behavioral reason and become GREEN only after the bounded
implementation; ≥1 load-bearing mutation probe per governed decision point.

## §21. Line-34 future Nth-domain fallthrough hazard (registered obligation — corrected)

**Registered as a mandatory future governed obligation.** `engine/domain_rules.py` line 34
`priority = ["medical_device","electronics_electrical","mechanical","software"]` is the no-activated-tie fallback. **Today all four
recognized packs are in this list, so no fallthrough hazard exists.** A **future 5th recognized pack** that uniquely matches
(best_score), is not activated, and is not added to this list would fall through to `return None` (line 26) → `/start` admits as
electronics. P9-E2-R does **not** increase reachability (classifier logic unchanged). **This is registered as a MANDATORY
obligation to be resolved BEFORE the first new Nth-domain registration/activation** (govern the fallback deterministically, or
route the unrepresented-uniquely-best case to a truthful non-admission state via the P9-E2-R seam). **Not fixed here (scope).**

## §22. Governance/risk classification of the future implementation (corrected)

The future P9-E2-R **implementation** changes the **runtime classification contract**, **production admission callers**
(`web/app.py`, `scripts/run_cli.py`), the **compatibility seam** (`infer_domain`), the **architecture guardrails**
(`ARCHITECTURE_GUARDRAILS.md` + its test), and **test surfaces** (six migrated monkeypatches). It is therefore an
**architecture-affecting, higher-governance change — NOT a routine bounded edit** — and MUST proceed through the full
independent-review + guardrail-update process, genuine RED→GREEN with load-bearing mutation probes, full regression, an
implementation candidate + independent exact-candidate review, SHA-preserving publication with a merge commit, post-merge
verification, and (if precedent requires) formal closure.

**Grill-correction ledger (this reissue vs rejected `1b817f06`).** (1) wrapper fail-loud raise — §4; (2) RED-R9 — §20; (3)
monkeypatch migration mandatory — §7.3; (4) guardrail reconciliation — §4.1; (5) `classify_domain` richer canonical entry, one
owner — §3/§4.1; (6) web dispatch-by-kind — §7/§7.1; (7) CLI dispatch-by-kind — §7.2; (8) RED-R10 — §20; (9) RED-R11 — §20; (10)
`state.domain` resolved-string invariant — §10; (11) strengthened invariants (unique ids, ≥2 candidates, all-activated, mutual
exclusion, duplicate rejection, immutable) — §11; (12) deterministic non-LLM `reason` — §12; (13) defensive type boundary vs
silent swallowing — §19; (14) line-34 hazard registered — §21; (15) governance/risk classification — this §22; (16) D4
marker-only + no-analysis-implied wording — §16/§18.

## §23. Acceptance criteria (implementation gate — testable minimum)

1. Ambiguity distinct from `None`. 2. MULTI_DOMAIN_NEEDS_D4 distinct from SINGLE/NONE. 3. No silent caller fallback from
ambiguity. 4. No arbitrary winner. 5. Deterministic candidate-set representation. 6. Deterministic ordering explicitly
non-precedential (§9). 7. recognition ≠ activation preserved (D3-D). 8. Activation policy unchanged. 9. No domain activated. 10.
Old NONE behavior preserved. 11. Line-34 fallback preserved (+ hazard registered, §21). 12. Electronics-only behavior preserved
(incl. P9-E1 Path-N). 13. One classifier owner; no duplicate router/framework. 14. **Legacy wrapper fails loud on richer kinds;
total over SINGLE/NONE** (§4) + **RED-R9**. 15. **Architecture-guardrail reconciled/updated** (§4.1); no guardrail silently
weakened. 16. **All six monkeypatch surfaces migrated and proven load-bearing** (§7.3). 17. **Web + CLI dispatch by `kind`**, never
truthiness/string comparison of the object (§7); + **RED-R10**, **RED-R11**. 18. **`state.domain` remains a resolved string**
(§10). 19. Strengthened result invariants hold (§11). 20. **Deterministic non-LLM `reason`** (§12). 21. **Defensive type boundary**
prevents silent `DomainClassification` swallowing (§19) + test. 22. No persistence/schema expansion (§13). 23. No public
API/integration expansion; object does not cross a public boundary (§15). 24. D4 marker-only; wording implies no analysis (§16). 25.
D8 untouched (§17). 26. Immutable result. 27. ≥3-way tie covered (RED-R8). 28. Focused **RED→GREEN** (R1…R11 + additional §20). 29.
Full regression green (baseline 2264 passed / 3 skipped / 1 xfailed / 0 failed; delta = new tests only; the governing suites
`test_web_app.py`, `test_domain_gate_entry_ux.py`, `test_s5_i2_domain_activation.py`, `test_d3_core_domain_neutrality.py`,
`test_architecture_guardrails.py` stay green). 30. P9-E1 remains intact. 31. Nth-domain extensibility preserved. 32. No
unsupported certainty (§18).

## §24. Mandatory Phase-9 completeness checklist (all 10 dispositioned)

1. **Engineering knowledge quality:** `NOT APPLICABLE` — result representation, not domain knowledge content.
2. **Technical truthfulness / known-unknown:** `APPLICABLE / PASS (by design)` — ambiguity/no-match/multi-domain are distinct
   honest states; fail-loud wrapper + deterministic `reason` prevent silent/false certainty.
3. **Real specialization without core coupling:** `APPLICABLE / PASS (by design)` — one classifier, one result type; dispatch by
   kind; no per-domain `if/elif`; no second router.
4. **Pre-activation qualification:** `APPLICABLE / PASS (by design)` — RED-R1…R11 + invariant/mutation/monkeypatch-load-bearing
   tests cover positive/negative/ambiguous/boundary(≥3-way)/safety + regression; full domain qualification is a separate gate.
5. **Cross-domain interaction/composition:** `APPLICABLE / PASS (by design)` for truthful-surfacing/no-silent-collapse/
   no-hidden-precedence; actual composition/contradiction reconciliation `DEFERRED TO D4` (marker only).
6. **Materials/manufacturing/prototype:** `DEFERRED TO CAP-12 / CAP-13 / WS-PFV` (owners untouched).
7. **Deterministic calculations/units:** `DEFERRED TO SEPARATE GOVERNED FUTURE GATE`.
8. **Knowledge sources / provenance / licensing:** `DEFERRED TO DOMAIN QUALIFICATION & KNOWLEDGE-SOURCE GOVERNANCE` (D13).
9. **Nth-domain extensibility:** `APPLICABLE / PASS (by design)` — general result representation + registered line-34 obligation
   (§21) let future domains + P9-E2 policy express ambiguity/multi-domain without shared-core redesign.
10. **End-to-end disciplined engineering reasoning:** `APPLICABLE / PASS (by design)` — the fail-loud wrapper + load-bearing
    migrated tests + deterministic `reason` close the silent-truth-loss holes the Grill found, so downstream reasoning is not
    built on a fabricated single-domain premise.

**No acceptance-relevant `APPLICABLE / GAP` remains.** Forward dependencies (P9-E2 tie policy; possible UI sub-gate; possible
public-API check; line-34 obligation) are explicitly deferred/registered/STOP-gated, not unresolved gaps.

## §25. Candidate-vs-authoritative boundary

**P9-E2-R = CONTRACT CANDIDATE ONLY (contract-first, corrected).** Authoritative only if this exact accepted candidate is
independently reviewed, Owner-accepted, merged (create-a-merge-commit), and post-merge verified. The P9-E2-R **runtime
implementation + tests are a separate, later, separately-run gate — NOT authorized by this contract-first step.** The rejected
candidate `1b817f06` remains **immutable historical evidence only.** **NO domain is activated or selected here.** Governance scope:
this NEW contract doc + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) + `ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md`
current-truth sync; **`OWNER_DECISION_REGISTER.md` UNCHANGED**; **ZERO** runtime/test/domain/web/CLI/schema/prompt/benchmark/CI
diff. P9-E1 remains FORMALLY CLOSED / SATISFIED; P9-E2 (tie precedence) remains a separate later runtime gate; D4
separate/unexecuted; D8 Owner-reserved; Phase 10 NOT AUTHORIZED; PSRR NOT EXECUTED; deployment / production NOT AUTHORIZED.
