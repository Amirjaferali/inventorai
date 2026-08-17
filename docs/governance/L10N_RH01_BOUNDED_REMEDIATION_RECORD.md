# L10N-RH-01 — Bounded Remediation Record (Candidate)

**Status of THIS record:** implementation record for the bounded, LOW-RISK CONTROLLED remediation of the 3
observations registered under `L10N-RH-01`. Runtime change is confined to one data-only string
(`web/ui_text.py`'s `UI_B_START_024` entry); `web/app.py` and `engine/domain_activation.py` are byte-unchanged.
**This record does NOT claim `L10N-RH-01` FORMALLY CLOSED** — remediation and formal closure remain separate
gates per this repository's established convention; `L10N-RH-01` is **IMPLEMENTED / READY FOR FORMAL CLOSURE**.
**`OWNER_DECISION_REGISTER.md` UNCHANGED.**

## §1. Basis and fresh verification

Base: `585d1f8d02d4e16f8154c66d2e3297958735ef16` (PR #499 — SHA-preserving merge of the accepted, corrected
L10N-RH-01 reassessment candidate `283326885441749ca21570c10f16eec0f8cab07c` onto
`3b7783f19d7b1ee9f6618342a00ed47362b35ac4`; merge tree == candidate tree, diff empty — independently re-verified
this gate; `origin/feature/atomic-json-session-persistence` confirmed at this exact tip; working tree clean).

## §2. Exact source reconstruction for all 3 registered observations (from repository truth, not memory)

Authoritative registration: `docs/governance/INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md` `## L10N-RH-01`
section (verbatim, re-read this gate). Corrected identification for Observation #3:
`docs/governance/L10N_RH01_REASSESSMENT_AND_MECHANICAL_ACTIVATION_READINESS_RECORD.md` (accepted, merged PR #499).

1. **Arabic broadened-activation negative-semantic-guard gap.** Surface: `web/ui_text.py`'s `UI_B_START_026`
   (`start_scope_sentence`, broadened 2+ activation). Defect: the pre-existing test
   (`tests/test_cf2_arabic_localization_remainder.py::test_green_ar_broadened_generalized_context_no_english_leak`)
   asserts `ui_text.UI_STRINGS["UI_B_START_026"]["ar"] in body` — tautological, derives its expected value from
   the same dict a mutation would corrupt. Defect class: missing semantic regression protection, not a current
   production defect (current shipped Arabic content independently re-confirmed truthful this gate).
2. **`SERVICE_UNAVAILABLE` localization-path regression-guard gap.** Surface: `web/app.py`'s two
   `SERVICE_UNAVAILABLE_MESSAGE` call sites (line 1802, inside `start()`; line 1842, inside
   `_finalize_started_session()`, reached from `start_ilt002_water_leak`/`start_ilt002_combination_lock`/
   `start_ilt002_combination_lock_path_n`). Defect: the pre-existing test
   (`test_green_ar_service_unavailable_localize_message_wired`) tests `ui_text.localize_message()` in isolation
   and explicitly documents it does not exercise the real call sites ("this suite does not induce" the durable-
   store failure). Defect class: missing regression protection, not currently broken production wiring (both call
   sites independently re-confirmed correctly routed through `ui_text.localize_message()` this gate).
3. **Present-confirm Arabic checkbox-label wording nuance.** Authoritative surface (per the corrected
   reassessment, `L10N_RH01_REASSESSMENT_...RECORD.md`): `start_present_confirm_label` (broadened-activation
   branch) / `UI_B_START_024`, consumed identically by both the error paragraph (`_present_confirm_message`) and
   the checkbox label (`present_confirm_label` at `web/app.py:1244`). Defect: prompt/instruction wording ("A
   supported domain was recognized... Please confirm...") rather than a first-person consent affirmation, unlike
   the English sibling used elsewhere in the same function ("I confirm that my idea belongs to the ... domain.").
   `UI_B_START_030` (`start_confirm_label`, a DIFFERENT template variable) is explicitly out of scope — already
   correctly first-person, confirmed unaffected. `UI_B_START_023` (electronics-only present-confirm) is explicitly
   out of scope — already production-reachable and independently accepted at the CF-2 Arabic Localization
   Remainder Fast Track gate; NOT opportunistically changed.

## §3. Risk classification

**LOW-RISK CONTROLLED**, confirmed by the actual implementation: exactly one data-only string changed in
`web/ui_text.py`; zero `web/app.py` behavioral change (both `SERVICE_UNAVAILABLE` call sites are byte-identical
to base); zero `engine/`, `domains/`, persistence, security, quota, or API change; zero classifier/admission/
activation change. No Tier-1 label work — the corrected `UI_B_START_024` string names no domain in either
language (verified structurally, §7 below).

## §4. Observation #1 implementation and RED→GREEN mutation proof

**Implementation:** new test `tests/test_l10n_rh01_remediation.py::
test_red_broadened_scope_sentence_ar_independent_semantic_guard` — asserts the rendered broadened-activation
page contains an independently hardcoded literal excerpt of the TRUE plural-domain claim
("أكثر من مجال متخصص واحد") and does NOT contain a hardcoded literal excerpt of a plausible false
electronics-only narrowing claim ("الإلكترونيات فقط"), neither derived from `ui_text.UI_STRINGS`.

**Mutation proof:** CLEAN → GREEN (confirmed, full focused file 7/7 passed before mutation). `UI_B_START_026`'s
Arabic value temporarily replaced with `"يُدعم حاليًا مجال الإلكترونيات فقط."` (a false electronics-only claim) →
MUTATED → **RED**: `test_red_broadened_scope_sentence_ar_independent_semantic_guard` FAILED (`AssertionError`, both
positive and negative markers absent from/present in the mutated body as expected). Restored byte-identically
(`sha256sum` verified: `0d4cd946...` unchanged before/after this probe) → RESTORED → GREEN (re-confirmed).

## §5. Observation #2 implementation, protected call sites, and RED→GREEN mutation proof

**Implementation:** new parametrized test
`tests/test_l10n_rh01_remediation.py::test_red_service_unavailable_real_call_seam_ar[...]` — two cases, one per
protected call site: `/start` (reaches `web/app.py:1802`, inside `start()`) and `/start_ilt002_water_leak`
(reaches `web/app.py:1842`, inside `_finalize_started_session()`). Each forces a real durable-store failure via a
monkeypatched `_get_store()` returning a store whose `create_project()` raises — exercising the ACTUAL production
except-Exception fallback, not `ui_text.localize_message()` in isolation — then asserts the response is a real
503 with the independently hardcoded literal Arabic `SERVICE_UNAVAILABLE` copy
("هذه الخدمة غير متاحة مؤقتًا") present and the raw English fallback absent.

**Protected call sites:** both of the two materially equivalent sites are covered by ONE parametrized test (per
the bounded-remediation instruction's own suggested resolution — a single parameterized test load-bears both,
since both share the identical code shape and the identical defect risk).

**Mutation proof:** CLEAN → GREEN (confirmed). Both call sites temporarily changed from
`error=ui_text.localize_message(SERVICE_UNAVAILABLE_MESSAGE, _current_ui_lang())` to
`error=SERVICE_UNAVAILABLE_MESSAGE` (raw English constant) → MUTATED → **RED**: both parametrized cases FAILED
(the raw English string rendered instead of the Arabic literal). Restored byte-identically (`sha256sum` verified:
`38ca03f6...` unchanged before/after this probe, exactly matching the pre-gate baseline) → RESTORED → GREEN
(re-confirmed).

## §6. Observation #3 implementation, exact old/new semantic role, and RED→GREEN mutation proof

**Implementation (`web/ui_text.py`, data-only):**

```
Old EN (dead — never consumed for English rendering; see §7): "A supported domain was recognized for your
  idea. Please confirm this domain to start, or revise your description."
Old AR: "تم التعرف على مجال مدعوم لفكرتك. يرجى تأكيد هذا المجال للبدء، أو تعديل الوصف."
  → prompt/instruction register ("يرجى تأكيد" — "please confirm").

New EN: "I confirm that this idea belongs to the domain that was recognized for it."
New AR: "أؤكد أن هذه الفكرة تنتمي إلى المجال الذي تم التعرف عليه لها."
  → first-person consent-affirmation register ("أؤكد أن" — "I confirm that"), matching
    UI_B_START_030's already-accepted grammatical pattern exactly. Domain-neutral throughout — no domain
    name appears in either language.
```

**New test:** `tests/test_l10n_rh01_remediation.py::
test_red_broadened_present_confirm_ar_first_person_not_prompt_style` — asserts the `<p class="error">` content
(scoped extraction, needed because the page's unrelated `UI_B_START_026` scope sentence incidentally shares the
phrase "يرجى تأكيد") contains the independently hardcoded first-person marker ("أؤكد أن") and does NOT contain
the independently hardcoded prompt-style marker ("يرجى تأكيد"), plus confirms no domain name ("Mechanical" /
"ميكانيكي") appears anywhere on the page.

**Mutation proof:** CLEAN → GREEN (confirmed, after the fix was applied). `UI_B_START_024` temporarily reverted
to the OLD prompt/instruction Arabic wording → MUTATED → **RED**:
`test_red_broadened_present_confirm_ar_first_person_not_prompt_style` FAILED. Restored to the corrected wording
(`sha256sum` verified: `0d4cd946...` unchanged before/after this probe) → RESTORED → GREEN (re-confirmed).

Two additional structural guard tests added: `test_green_ui_b_start_024_still_domain_neutral` (no domain name in
either language) and `test_green_ui_b_start_023_and_030_unaffected` (both explicitly-out-of-scope siblings remain
byte-unchanged).

## §7. `UI_B_START_023` and `UI_B_START_030` disposition

**`UI_B_START_023`:** NOT modified. Confirmed byte-unchanged via
`test_green_ui_b_start_023_and_030_unaffected`. Not opportunistically changed, per the bounded-remediation
instruction's explicit prohibition — it is production-reachable (electronics is the real activated domain) and
was already independently reviewed and accepted at the CF-2 Arabic Localization Remainder Fast Track gate.

**`UI_B_START_030`:** NOT modified. Confirmed byte-unchanged via the same test. Already correctly first-person in
both languages ("I confirm that this idea is primarily a supported-domain idea." /
"أؤكد أن هذه الفكرة هي في الأساس فكرة ضمن المجال المدعوم.") — was the grammatical-register PRECEDENT this
remediation matched `UI_B_START_024` to, never itself a target of change.

**`UI_B_START_024`'s "en" field is dead data**: independently confirmed via `grep` — `_present_confirm_message`
and the `present_confirm_label` assignment in `web/app.py` both call `ui_text.text("UI_B_START_024", lang)` ONLY
inside their `is_ar`/`lang == "ar"` branches; the English branch uses a separate, always-first-person, dynamically
domain-named string (`"I confirm that my idea belongs to the " + labels[present_domain] + " domain."`). Changing
`UI_B_START_024`'s "en" value therefore has zero live behavioral effect — confirmed by the unchanged full-suite
pass count.

## §8. Tier-1 non-modification proof

`git diff --name-only` against base shows `web/domain_label.py` NOT present in the changed-path list.
`_PUBLIC_DOMAIN_LABELS` unchanged — `"mechanical"` was never added. `test_green_ui_b_start_024_still_domain_neutral`
additionally confirms structurally that the corrected string names no domain in either language. No Tier-1
translation work was performed or proposed as executed.

## §9. Mechanical activation-state proof

`engine.domain_activation.activated_domains()` — the REAL public function, which returns a **sorted list**, not
the internal `_ACTIVATED_DOMAINS` frozenset constant — returns `['electronics_electrical']`, verified via live
interpreter call both before and after every mutation probe in §4/§5/§6. `engine/domain_activation.py` is
byte-unchanged (not present in the changed-path list). **Mechanical remains NOT ACTIVATED.**

## §10. Runtime architecture non-modification proof

`git diff --name-only` against base: `web/ui_text.py` (one data-only entry changed) and
`tests/test_l10n_rh01_remediation.py` (new file) are the ONLY non-governance paths changed.
`web/app.py` is byte-unchanged (`sha256sum` `38ca03f6...`, identical to base — confirmed after both the
Observation #2 mutation probe's restoration and at final freeze). No change to `engine/domain_activation.py`,
any file under `engine/` (scoring, progression, classification, admission), `domains/`, persistence, security,
quotas, or any API unrelated to these 3 observations.

## §11. Test totals

**Focused (`tests/test_l10n_rh01_remediation.py`):** 7 passed (1 activation-honesty baseline; 3 load-bearing
mutation-tested guards, one parametrized ×2; 2 structural out-of-scope guards; 1 net new parametrize case —
total 7 collected items, all green).

**Relevant localization/web (`tests/test_cf2_arabic_localization_remainder.py` +
`tests/test_web_app.py`):** 76 passed (31 + 45), zero regressions.

**Full governed suite:** **2684 passed / 3 skipped / 1 xfailed / 0 failed** (baseline before this gate
2677/3/1/0; delta **+7 passed**, exactly matching the 7 new focused tests; 0 regressions; 0 unexplained
skips/failures).

## §12. Governance disposition

- **Observation #1 = REMEDIATED** (§4).
- **Observation #2 = REMEDIATED** (§5) — both authoritative call sites protected.
- **Observation #3 = REMEDIATED** (§6) — corrected surface (`UI_B_START_024`), corrected defect class
  (register, not domain-naming), `UI_B_START_023`/`UI_B_START_030` confirmed unaffected.
- **`L10N-RH-01` = IMPLEMENTED / READY FOR FORMAL CLOSURE** — NOT claimed FORMALLY CLOSED by this record; the
  registration's own governing pattern (mirrored throughout this repository's history) treats implementation and
  formal closure as separate, sequential gates. A future, separate closure gate may formally discharge
  `L10N-RH-01` once it independently re-verifies this remediation.
- **Mechanical remains NOT ACTIVATED**; **Tier-1 EN/AR label remains the next pre-activation gate** (not
  authorized or performed here); **explicit Owner Mechanical activation authorization remains later**, not
  requested or implied; **Phase 9 remains OPEN**.

## §13. Scope of THIS candidate and next gate

Runtime: `web/ui_text.py` (one data-only string entry). Tests: new `tests/test_l10n_rh01_remediation.py` (7
tests). Governance: this new record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) + `ACTIVE_INCREMENT_CONTRACT.md`
+ `CURRENT_PROJECT_STATE.md` + `INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md`'s `L10N-RH-01` entry (remediation
note only). `OWNER_DECISION_REGISTER.md` UNCHANGED. `web/app.py` and `engine/domain_activation.py` confirmed
byte-unchanged. **Next required gate: Mandatory Grill on this exact candidate**, then the governed lifecycle.
After this candidate merges and is independently reviewed, the next roadmap item becomes the **Tier-1 EN/AR
Mechanical public label** gate (a separate L10N-RH-01 formal closure gate may run first or alongside, at the
Owner's discretion) — neither is authorized or performed here.
