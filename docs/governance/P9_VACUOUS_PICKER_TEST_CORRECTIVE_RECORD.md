# Phase 9 Vacuous Picker Test — Corrective Implementation Record

**Status of THIS record:** governance/documentation-only **CORRECTIVE IMPLEMENTATION RECORD**. It documents a
LOW-RISK, test-only correction identified as the sole MUST-FIX blocker by the Phase 9 Remaining-Obligation /
Exit-Criteria Review (verdict: `NOT YET ELIGIBLE`). Authoritative ONLY if/when this exact candidate is merged
(create-a-merge-commit) and post-merge verified.

## §1. Basis

Base: `48b81773f9ee68ca9d897931a43271609c3bdeac` (PR #504 merge — corrected Mechanical P9-QS qualification
governance, authoritative). Independently re-verified this gate: `origin/feature/atomic-json-session-persistence`
confirmed at this exact tip; working tree clean; `activated_domains() == ['electronics_electrical', 'mechanical']`
confirmed live.

## §2. Defect reproduced and root-caused

`tests/test_p6_1_truthful_domain_labeling.py::test_mechanical_not_offered_in_start_domain_picker` called
`client.get("/start")`. `/start` is registered POST-only (`@app.route("/start", methods=["POST"])`), so a GET
receives Flask's generic 405 error page — content that trivially never contains `"Mechanical-informed review"` or
`value="mechanical"`, regardless of the real picker's actual content. The test's assertions therefore passed
vacuously. Independently reconstructed the real picker surface: `web/app.py`'s `/start` POST handler, when the
submitted idea classifies `NONE` and no valid `domain_choice` is supplied, re-renders `index.html` with
`choice_domains=activated` (the real `activated_domains()` list, confirmed at `web/app.py:1753`) — this is the
actual, sole production source of the D2 explicit-choice picker's offered domains.

## §3. Correction

`tests/test_p6_1_truthful_domain_labeling.py::test_mechanical_not_offered_in_start_domain_picker` renamed to
**`test_start_domain_picker_offers_only_activated_domains`** (the prior name's premise — "Mechanical not offered"
— is now stale; Mechanical is genuinely, correctly activated and IS offered). The corrected test performs a real
`POST /start` with a NONE-classifying idea (`infer_domain(idea) is None`, confirmed live) and parses the real
rendered `domain_choice` radio options from the response body, asserting the offered set equals
`activated_domains()` exactly — `{"electronics_electrical", "mechanical"}` — and that a recognized-but-not-
activated domain (`medical_device`, `software`) is never offered. This proves the invariant the original test's
docstring claimed to prove (picker driven exclusively by `activated_domains()`) against the real production POST
flow, not a 405 error page.

## §4. Load-bearing proof (mutation probes, byte-restored after each)

- **Mutation A** (`_ACTIVATED_DOMAINS` reduced to `frozenset({"electronics_electrical"})`, removing mechanical):
  test → **RED**. Restored; `sha256sum engine/domain_activation.py` confirmed byte-identical to the original;
  `git diff --stat engine/domain_activation.py` empty.
- **Mutation B** (`_ACTIVATED_DOMAINS` extended to add an unintended `"software"`): test → **RED**. Restored;
  same byte-identical + empty-diff confirmation.
- Test GREEN before, and GREEN again after, both restorations.

## §5. Zero production diff

**Changed file: `tests/test_p6_1_truthful_domain_labeling.py` only** (test-only). `engine/domain_activation.py`,
`web/app.py`, all templates, the classifier, scoring, progression, persistence, security, and every domain pack
are byte-unchanged (confirmed via `git diff --stat` and hash checks above; the mutation-probe edits to
`engine/domain_activation.py` were transient and fully byte-restored, never part of the committed diff).

## §6. Test totals

Focused: `tests/test_p6_1_truthful_domain_labeling.py` — 32 passed (was 32; one test rewritten in place, net
count unchanged). Relevant activation/picker/admission suite (`test_p6_1_truthful_domain_labeling.py` +
`test_web_app.py` + `test_domain_gate_entry_ux.py` + `test_s5_i2_domain_activation.py`): 138 passed. Full governed
suite: **2696 passed / 3 skipped / 1 xfailed / 0 failed** — matches the expected baseline exactly (net test count
identical, since one existing test was corrected in place rather than added).

## §7. Boundary statements

1. **Phase 9 Remaining-Obligation / Exit-Criteria Review's sole identified MUST-FIX blocker is now corrected.**
2. This record does NOT re-declare Phase 9 closure-eligible; that determination requires a fresh Remaining-
   Obligation / Exit-Criteria Review, performed as a separate later gate, not here.
3. **Phase 9 remains OPEN.**
4. No runtime behavior changed anywhere in the system; this is a test-only correction.
5. Phase 10 / PSRR / deployment remain NOT AUTHORIZED.
6. No third domain activated or implied; no D4/D8 work performed or implied.
7. The other non-blocking debts named by the Remaining-Obligation Review (stale `classify_domain` docstring, 4
   historical test-file comments, `UI_B_START_024` wording, missing real E2E Tier-1 chain test, CLI real-banner
   coverage) are explicitly NOT touched by this candidate — retained for later consideration, per the Review's own
   scope instruction not to opportunistically fix non-blocking items in this bounded gate.
8. `OWNER_DECISION_REGISTER.md` UNCHANGED — no new Owner authorization event; this is a bounded test-hygiene
   correction of a repository-truth defect already identified by governance review, requiring no new decision.

## §8. Exact next gate

A fresh **Phase 9 Remaining-Obligation / Exit-Criteria Review**, performed as its own separate gate once this
candidate is merged and post-merge verified. Phase 9 formal closure remains not authorized, not performed, not
implied by this record.

## §9. Scope of THIS candidate

Test-only: `tests/test_p6_1_truthful_domain_labeling.py` (one test rewritten in place) + this new corrective
record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) + `ACTIVE_INCREMENT_CONTRACT.md` (active-contract section
replaced per this file's own convention) + `CURRENT_PROJECT_STATE.md` current-truth sync. **ZERO
production/classifier/scoring/progression/persistence/security/schema/registry diff.** `OWNER_DECISION_REGISTER.md`
UNCHANGED. Next required gate: Mandatory Grill on this exact candidate, then the governed lifecycle. After this
merges, the next eligible step is a fresh **Phase 9 Remaining-Obligation / Exit-Criteria Review** — not authorized
or performed here.
