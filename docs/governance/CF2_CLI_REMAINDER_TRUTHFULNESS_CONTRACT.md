# CF-2 — Public-Message Truthfulness Full-Remainder Reconstruction & Bounded CLI Implementation Contract (governance-only; implements nothing)

**Status of THIS record:** governance/documentation-only **CONTRACT CANDIDATE**. It implements nothing in this
gate — no runtime, Web, CLI, test, domain, activation, schema, or persistence change. It defines WHAT a later,
separately-authorized bounded implementation must achieve and HOW it will be proven. It does NOT close CF-2 (only
this reconstruction's own narrower future increment, at that increment's own closure), does NOT reopen CF-6, does
NOT touch Tier-1, does NOT activate Mechanical, and does NOT redesign the classifier, activation, or persistence.
**`OWNER_DECISION_REGISTER.md` UNCHANGED.** **DOCUMENTED NO-VALID-RED.**

## §1. Authoritative base and fresh verification

Base: `5355ed54cbba17c16b5716865c1dc82e8b141941` (PR #491 — SHA-preserving merge of the accepted CF-6 full-scope
closure candidate `11d9450f` onto `1fe05e09`; merge tree `8d6aeb75` == candidate tree; POST-MERGE PASS; freshly
fetched; 0 newer; clean tree) — `CF-6 = FULLY DISCHARGED` for its authoritative scope; `CF-2` remains OPEN; full
governed suite **2577 passed / 3 skipped / 1 xfailed / 0 failed** (fresh re-verification).

## §2. Reconstructed CF-2 obligation — exact, fullest authoritative formulation

**Origin (`CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_CONTRACT.md` §4, area H, verbatim):** *"Public-message
truthfulness (CF-2) — AMBIGUOUS_TIE / MULTI_DOMAIN_NEEDS_D4 user-facing treatment; generic unsupported messaging;
future public reachability; misleading domain claims."*

**Fuller carry-forward formulations (both pre-date and are consistent with the audit contract):**
`P9_E2_MULTI_ACTIVATED_DOMAIN_TIE_PRECEDENCE_FORMAL_CLOSURE_RECORD.md` §7: *"CF-2 — Shared AMBIGUOUS/MULTI public
message: PENDING. `AMBIGUOUS_TIE` / `MULTI_DOMAIN_NEEDS_D4` currently fail closed through the existing
`UNSUPPORTED_DOMAIN_MESSAGE`, and richer kinds are production-unreachable today (electronics-only). Before those
states become genuinely user-reachable under future governed activation, verify public messaging remains
truthful and honor the already-governed UI-boundary sub-gate rather than silently adding copy."*
`CF5_F002_CF6_WEB_ADMISSION_CORRECTIVE_CONTRACT.md` §6 residual list: public-message truthfulness on every
surface beyond the `/start` admission flow's own discharged copy — *"CLI copy; legacy ILT-002 route copy;
templates/pages outside the `/start` admission flow that assert or imply electronics-only support; localization
of the generalized admission copy... and any other public 'electronics only' assertion."*

**What CF-2 covers (adopted, all confirmed applicable):** Web copy (`/start` flow — largely discharged, see §3);
CLI copy (open, see §4); templates/pages (swept, see §3); Arabic localization (open, see §5); session/domain
labels (swept, see §3 — `public_domain_label`); ILT-002 presentation (resolved, see §6 — truthful, no defect);
error/refusal text (swept, see §3); summary/demo public output (swept, see §3 — out of scope, not user-facing).

**Closure criteria:** every user/operator-facing domain-support claim, across every surface above, is either (a)
truthful under today's real activation state AND would remain truthful automatically under any future broadened
activation state (the established `activated_domains()`-derived pattern), or (b) an explicitly Owner-governed
exception (ILT-002), with no material match left unclassified.

**Explicit exclusions (not CF-2):** the future global Output Language selector / D-P6-18 (NOT implemented or
touched here — only CF-2 truthfulness/localization within already-authorized behavior); classifier/activation
redesign; persistence redesign; Tier-1 label implementation (label content is Mechanical-qualification-lane
territory, deferred to activation-readiness — not touched by CF-2 copy fixes); `scripts/run_summary_demo.py`
(confirmed this gate: a standalone, manually-run, non-CI, non-evidence-pipeline acceptance script whose printed
output makes no domain-support claim to a human reader — genuinely outside CF-2's user/operator-facing-copy
scope).

## §3. Mandatory repository-wide public-copy sweep — methodology and complete classification

**Methodology.** An independent read-only Explore-agent sweep searched, beyond the bare `"electronics_electrical"`
identifier, EVERY prose variant (`electronics/electrical`, `electronics only`, `supports...only`, `Scope:`,
`supported domain`/`unsupported domain`/`specialist domain`) across `web/*.py engine/*.py scripts/*.py`; every
`web/templates/*.html` file (all 13, not just `index.html`); the full `web/ui_text.py` catalogue (252 keys,
EN/AR parity programmatically verified — 252/252 have both languages, zero gaps in that catalogue); the full
`web/domain_label.py`; `scripts/run_summary_demo.py` in full; every `_MESSAGE = ` constant in `web/app.py` and its
localization-mechanism participation. This session personally re-verified the exact current line content of every
CLI candidate defect and the exact gating logic of every flagged `web/app.py` message function before classifying.

**Complete classification table:**

| Item | Location | Classification |
|---|---|---|
| `UNSUPPORTED_DOMAIN_MESSAGE` (raw constant) | `web/app.py:858-861` | **1 — ALREADY CANONICAL / TRUTHFUL** (only ever returned by `_unsupported_domain_message` when `activated == ["electronics_electrical"]`; auto-generalizes otherwise — the discharged F002 pattern) |
| `_unsupported_domain_message()` generalized/empty branches | `web/app.py:921-933` | **1 — ALREADY CANONICAL / TRUTHFUL** |
| `CONFIRMATION_REQUIRED_MESSAGE` (raw constant) + `_confirmation_required_message()` | `web/app.py:874-877,936-942` | **1 — ALREADY CANONICAL / TRUTHFUL** (verified this gate: gated identically to `_unsupported_domain_message`'s pattern — byte-identical for electronics, domain-labeled otherwise) |
| `MECHANISM_GUIDANCE_MESSAGE` (raw constant) + call site | `web/app.py:1091-1096,1655` | **1 — ALREADY CANONICAL / TRUTHFUL** (verified this gate: the ONLY call site is nested inside the F002-governed weak-conflict branch gated on `sole == "electronics_electrical"`, which is structurally unreachable the moment activation broadens past one domain — the message is truthful in every state it can actually fire in) |
| `DOMAIN_CHOICE_MESSAGE` | `web/app.py:955-958` | **1 — ALREADY CANONICAL / TRUTHFUL** (already domain-neutral text — "one supported domain" — makes no electronics-specific claim) |
| `SERVICE_UNAVAILABLE_MESSAGE` | `web/app.py:153-154` | **1 — ALREADY CANONICAL / TRUTHFUL** (domain-neutral) |
| `ANSWER_REQUIRED_MESSAGE`, `ANSWER_NOT_SAVED_MESSAGE` | `web/app.py:569,574` | **1 — ALREADY CANONICAL / TRUTHFUL**, and bilingual (route through `ui_text._MESSAGE_KEYS`/`localize_message`) |
| Five `/start`-flow error-path constants' localization | `UNSUPPORTED_DOMAIN_MESSAGE`, `CONFIRMATION_REQUIRED_MESSAGE`, `MECHANISM_GUIDANCE_MESSAGE`, `DOMAIN_CHOICE_MESSAGE`, `SERVICE_UNAVAILABLE_MESSAGE` — traced end-to-end through `_render_start_page` → `render_template` → `index.html`'s raw `{{ error }}` | **4 — CF-2 DEFECT — REQUIRES REMEDIATION, but DEFERRED to its own future gate** (confirmed this gate: NONE of the five ever route through `ui_lang`/`t()`/`localize_message`/`localize_deep` — they render in English regardless of the user's selected language, including when truthful in content; see §5 — a materially different, larger responsibility than the CLI fix, not bundled here) |
| `UI_B_INDEX_004/006/007/009` (index-page initial-load copy) | `web/ui_text.py:144-164`; `web/templates/index.html:22,26,54,59` | **1 — ALREADY CANONICAL / TRUTHFUL** (fully bilingual — EN+AR both present — AND gated behind `start_is_electronics_only`/`start_sole_domain`, both server-computed from the real activation set) |
| Every other `web/templates/*.html` file (12 of 13) | `account.html base.html data_session.html decision_workspace.html deliverable.html login.html recover.html register.html reset.html session.html success_criteria.html verify_result.html` | **1 — ALREADY CANONICAL / TRUTHFUL** (zero "electronics" occurrences found in any of them — swept in full) |
| `web/domain_label.py` (`_PUBLIC_DOMAIN_LABELS`, `_GENERAL_LABEL`) | `web/domain_label.py:23-31` | **1 — ALREADY CANONICAL / TRUTHFUL** (single Tier-1 entry, bilingual; truthful neutral bilingual fallback for every other domain; docstring: "NEVER silently to electronics") |
| ILT-002 session presentation (`Review type: {{ public_domain_label(state.domain) }}`) | `web/templates/session.html:100-109`; `web/ui_text.py:464` | **3 — GOVERNED EXCEPTION** (resolved this gate — see §6: truthful under the scenario-route contract, not a classification claim) |
| `scripts/run_cli.py:39-41` (unconditional startup banner) | verified this gate, exact current content: `print("  Scope: Electronics/Electrical, Level 0-2")` | **4 — CF-2 DEFECT — REQUIRES REMEDIATION** (prints before any classification/activation check; unconditional; would misstate scope the moment a second domain activates) |
| `scripts/run_cli.py:64-70` (richer-kind bounded-stop message) | verified this gate, exact current content: `print("This MVP supports electronics/electrical ideas only, and this idea")` inside the `AMBIGUOUS_TIE`/`MULTI_DOMAIN_NEEDS_D4`/`UNRESOLVED_NON_ACTIVATED_TIE` dispatch block | **4 — CF-2 DEFECT — REQUIRES REMEDIATION** (unconditional; not gated on `activated_domains()`; a richer-kind tie by construction means more than one domain was relevant, so an "electronics only" claim here is structurally suspect the moment activation broadens) |
| `scripts/run_cli.py:90-102` (`OUTSIDE MVP SCOPE` branch, incl. the line-91 sub-branch) | verified this gate, full context read | **1 — ALREADY CANONICAL / TRUTHFUL** (this session's own already-merged CLI facet work — CORRECTLY gated: byte-identical electronics-only sub-branch at line 91 fires ONLY inside `if activated == ["electronics_electrical"]:`; truthful multi-domain and empty-activation branches already present) |
| `scripts/run_cli.py:106-109` (`Domain confirmed:` line) | verified this gate | **1 — ALREADY CANONICAL / TRUTHFUL** (already-merged CLI facet work; correctly domain-labeled) |
| `scripts/run_summary_demo.py` (`state.domain_signal = "electronics"`) | full file read this gate | **6 — TEST/EVIDENCE ONLY — NON-PRODUCT** (standalone, manually-run, no CI/pipeline consumer found repo-wide; printed output makes no domain-support claim to a human reader) |
| `engine/progression_loop.py:415` (Layer-2 scoring-correction electronics-substance requirement) | full context read this gate | **7 — OUTSIDE CF-2 — NEW pre-second-domain-activation residual; registered separately, see §7** (Owner-authorized 2026-07-11 scoring logic, not public copy) |
| Module docstrings/comments referencing "electronics/electrical" scope (`engine/progression_loop.py:3`, `engine/idea_state.py:3`, `engine/domain_rules.py:2`, `scripts/run_cli.py:3`, and various `web/app.py` comments) | throughout | **5 — HISTORICAL / GOVERNANCE ONLY** (source comments/docstrings, never rendered to any user or operator) |

**Result: exactly two CF-2 defects requiring remediation, both in `scripts/run_cli.py`, both immediately
actionable; one CF-2-class defect (the Arabic localization gap) requiring remediation but of materially different
responsibility, deferred to its own future gate; one item (`progression_loop.py:415`) requiring separate
anti-forgetting registration outside CF-2 entirely.**

## §4. Confirmed CLI defects — exact current content (this gate's bounded scope)

**Defect 1 — unconditional startup banner (`scripts/run_cli.py:39-41`):**
```
print("  InventorAI — Progression Engine MVP")
print("  Scope: Electronics/Electrical, Level 0-2")
```
Prints before `classify_domain` or `activated_domains()` is ever consulted; makes an unconditional scope claim.

**Defect 2 — richer-kind bounded-stop message (`scripts/run_cli.py:68-69`):**
```
print("This MVP supports electronics/electrical ideas only, and this idea")
print("could not be resolved to a single supported domain.")
```
Inside the `AMBIGUOUS_TIE`/`MULTI_DOMAIN_NEEDS_D4`/`UNRESOLVED_NON_ACTIVATED_TIE` dispatch block
(`scripts/run_cli.py:55-71`); unconditional; not derived from `activated_domains()`.

**Required fix shape (specification only — not implemented here):** both must adopt the SAME
`activated_domains()`-derived truthful-copy discipline already established and merged in this file's own
`_cli_supported_domains_phrase`/`_cli_domain_label` helpers and the `OUTSIDE MVP SCOPE` branch (§3 row,
CANONICAL): byte-identical text under `['electronics_electrical']` (today's only governed state); a truthful
generalized phrase when the activation set is broader; truthful copy for the empty-activation edge case where
reachable. No new admission mechanism; no classifier change; no activation change; the richer-kind DISPATCH
LOGIC itself (which branch fires) remains completely untouched — only the printed COPY inside the existing
branch changes.

## §5. Arabic localization gap — reconstructed and explicitly deferred (NOT implemented, NOT folded into this increment)

**Exact finding (corrects the prior roadmap's imprecise characterization):** the prior CF-6/CF-2 CLI scoping
contract's residual list described this as "localization of the generalized admission copy (Arabic strings exist
only for the electronics-only state)." Fresh code-level tracing this gate found the gap is actually BROADER: all
five `/start`-flow error-path message constants (`UNSUPPORTED_DOMAIN_MESSAGE`, `CONFIRMATION_REQUIRED_MESSAGE`,
`MECHANISM_GUIDANCE_MESSAGE`, `DOMAIN_CHOICE_MESSAGE`, `SERVICE_UNAVAILABLE_MESSAGE`) bypass `ui_lang`/`t()`/
`localize_message`/`localize_deep` ENTIRELY and render in English regardless of the user's selected language —
including the electronics-only state, which has NO Arabic variant either (contrary to the prior text's "Arabic
strings exist... for the electronics-only state"). This is recorded as a later, additional evidence-based
clarification of the prior record — not a claim that the prior record was invalid; it correctly identified the
gap's existence, only its precise shape needed fresh verification.

**Why deferred, not bundled:** this is a materially different responsibility from the CLI copy fix (§4) — it
requires designing HOW these five constants participate in the localization catalogue (new `UI_STRINGS` keys?
routing `error=` through `localize_message`? RTL considerations on the raw-rendered `index.html` error paragraph?
D-P6-18/Output-Language-selector boundary discipline to avoid over-scoping into that separate future program) —
none of which this contract is authorized to design without its own dedicated scoping. Per this gate's own
splitting instruction, it is named, evidenced, and explicitly carried forward as its own future CF-2 increment —
not silently dropped, not bundled into the smaller CLI-only increment below.

## §6. ILT-002 presentation truthfulness — resolved this gate (no defect; `D-CF6CF2-ILT002-01` unchanged)

The ILT-002 session page shows `t('UI_B_SESSION_010')` ("Review type:") followed by
`public_domain_label(state.domain)[ui_lang]` — for these routes `state.domain` is ALWAYS
`"electronics_electrical"` by the route's own governed, fixed-domain design (`D-CF6CF2-ILT002-01`), so the
rendered label ("Electronics-informed review" / its Arabic equivalent) truthfully describes the KIND OF REVIEW
actually being run (the engine genuinely executes electronics-domain questions/rules for this session) — it does
NOT claim the submitted idea text was classified as electronics. No `/start`-flow classification-implying copy
is reachable from an ILT-002 route (these routes never render `index.html`/`_render_start_page` at all — they
redirect straight to `/session/<sid>`). **Determination: TRUTHFUL under the governed scenario-route contract. No
CF-2 remediation surface exists here.** `D-CF6CF2-ILT002-01` is not reopened, altered, or reinterpreted.

## §7. `engine/progression_loop.py:415` — classified OUTSIDE CF-2; new anti-forgetting registration (not implemented)

Full context read this gate: an Owner-authorized (2026-07-11) "Layer-2 bounded scoring correction" — a narrow,
deliberately-gated scoring-logic path requiring an electronics/electrical domain substance signal (whole-word
match, same sentence as a qualifying causal connective) before a specific scoring bonus applies. This is
**internal scoring logic, never rendered to any user or operator** — NOT public-message truthfulness, NOT CF-2.
It is also not classifier/activation-admission-truth consistency — NOT CF-6 (already closed; this record does not
reopen it). **Classification: (C) a NEW pre-second-domain-activation residual** — if/when a second domain
activates, ideas in that domain would never benefit from this specific scoring correction (a scoring-completeness
gap for future domains), which is worth not forgetting but is NOT actionable now and NOT CF-2/CF-6 scope. Per
this gate's instruction, it is registered in the EXISTING canonical anti-forgetting mechanism
(`docs/governance/INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md`, the THERM-01 precedent — a deliberately
non-numeric designation avoiding any CAP-01…18 collision) as a new, small, NON-ACTIVATING, non-authorizing
section: **`L2SC-01` — Layer-2 Scoring-Correction Domain-Scope Completeness**. This registration is NOT part of
CF-2's own scope or closure criteria; it is a separate, independent anti-forgetting entry synchronized in this
same governance-only commit purely to avoid opening a disproportionate standalone gate for a three-line
observation, exactly as THERM-01 itself was registered.

## §8. The bounded FUTURE implementation — exact definition (governance only; NOT executed by this contract)

```
INCREMENT CONTRACT — CF-2 CLI Remainder Truthfulness (Defects 1-2 only)   [implementation NOT started]
Responsibility:   Replace the two confirmed unconditional/ungated hardcoded electronics-only prints in
                  scripts/run_cli.py (§4) with the SAME activated_domains()-derived truthful-copy discipline
                  already established and merged in this file (_cli_supported_domains_phrase,
                  _cli_domain_label, the OUTSIDE MVP SCOPE branch). Byte-identical output under
                  ['electronics_electrical'] (today's only governed activation state); truthful generalized
                  copy under any broader activation set (reachable only via a bounded test double today); no
                  change to which branch/dispatch path fires, only to what is printed inside the existing
                  paths. No admission-mechanism change; no classifier change; no activation change.
Allowed paths:    scripts/run_cli.py (the startup-banner scope line + the richer-kind dispatch block's copy
                  ONLY — no other CLI behavior change: the classifier dispatch logic itself, the already-
                  correct OUTSIDE MVP SCOPE branch, the iteration loop, and the summary output are UNTOUCHED);
                  the reconciliation test file(s) the future implementation's own exhaustive sweep identifies
                  (none currently pinning these two exact lines are known — the future gate MUST perform its
                  own fresh sweep, this contract does not pre-conclude it); closure-time governance sync only.
Forbidden paths:  web/app.py; web/templates/*; web/ui_text.py; web/domain_label.py (the Arabic-localization
                  gap, §5, is explicitly OUT OF SCOPE here); every ILT-002 route; every E-2 tooling script;
                  engine/progression_loop.py (L2SC-01, §7, is explicitly OUT OF SCOPE here — registration
                  only, no implementation); every engine file; every domain pack; every other existing test.
                  FORBIDDEN OUTCOMES: any Electronics-only behavior delta; any activation state change; any
                  Tier-1 label work; any ILT-002 route change; any duplicate/new admission mechanism; any CF-6
                  reopening; any CF-2 full-lane closure claim; any Arabic-localization implementation.
Required tests:   current electronics-only banner/message text preserved byte-identical (positive pin); a
                  broadened activation set (bounded test double, mirroring the pattern already used for the
                  OUTSIDE MVP SCOPE branch) produces truthful generalized copy for BOTH defect sites, naming
                  the real activated domain(s), never asserting "electronics/electrical ideas only" when that
                  is untrue; empty-activation truthful copy where reachable; explicit negative assertions that
                  neither fixed site ever prints the literal "electronics/electrical ideas only" (or "Scope:
                  Electronics/Electrical") string when activation is broadened past electronics-only; the
                  richer-kind dispatch LOGIC (which branch fires for AMBIGUOUS_TIE/MULTI_DOMAIN_NEEDS_D4/
                  UNRESOLVED_NON_ACTIVATED_TIE) unchanged and re-pinned; full governed suite green; mutation
                  probes proving the new pins are load-bearing (reintroduce each hardcoded literal; confirm
                  CAUGHT).
```

## §9. Closure criteria and boundaries

**This contract's own closure:** Mandatory Grill PASS on this exact candidate, independent review, Owner
acceptance, merge, post-merge verification — authorizes ONLY the §8 bounded implementation as a SEPARATE future
gate. **Non-effects:** does NOT close CF-2 (only §8's own narrow future increment, at that increment's own
closure — CF-2's Arabic-localization gap, §5, and any residual beyond this record's sweep remain fully OPEN);
does NOT reopen or alter CF-6 (`CF-6 = FULLY DISCHARGED` stands, unmodified); does NOT touch `D-CF6CF2-ILT002-01`
or the ILT-002 routes; does NOT touch the Tier-1 label; does NOT activate Mechanical; no D4/D8/THERM-01/Phase
10/PSRR/deployment; no P9 closure. `activated_domains() == ['electronics_electrical']` unchanged.
`MECHANICAL = P9-QS QUALIFIED — WITH ACTIVATION BLOCKERS; NOT ACTIVATED` unchanged. **STOP conditions for the
future implementation:** any Electronics behavior delta; any flip beyond its own exhaustive sweep; any touch to
a forbidden path; any Owner-policy question. **Next required gate: Mandatory Grill on this exact contract
candidate**, then the governed lifecycle; thereafter the separately-authorized CLI-remainder implementation gate.
