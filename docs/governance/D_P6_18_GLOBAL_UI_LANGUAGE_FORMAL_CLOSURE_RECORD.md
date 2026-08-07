# D-P6-18 — Global UI Language (English | العربية) — Formal Closure Record

Status: **FORMALLY ACCEPTED AND CLOSED** (owner decision, gate
`G-DP6-18-GLOBAL-UI-LANGUAGE-FORMAL-CLOSURE-01`).

Classification: documentation-only formal-closure record. It records committed
repository reality; it creates no new authority and authorizes no downstream work.
It makes no runtime/code/test/dependency/schema change, activates no new capability,
implements no Question Translation Assistant and no Output-Language override, and
starts no successor increment or Master Obligation Index work.

Repository truth overrides conversation, handover, memory, inference, and proposal.

Authoritative integration branch: `feature/atomic-json-session-persistence`
Authoritative integration tip at closure: `b47bf4bb57446956c47488283248cfbacd603e85`
(PR #388 merge). `main` is out of scope and not synchronized here.

---

## 1. Accepted lineage and merge identity (independently re-verified)

| Item | SHA / value |
|---|---|
| Pre-D-P6-18 base | `a0426cbb6a188a366006d22472c875ec4e5e446b` |
| Original candidate | `98c47d51e91467b1911c3fbe46b121acff526703` (Global UI Language seam + shared selector + in-scope surfaces) |
| Remediation child #1 | `8920f4664e1c440fe34c1a94fd90a369623a4192` (answer-action controls, correction/placeholders, active page titles) |
| Final accepted candidate | `62818a8c71a83be487928d8b2ccaa2feb4dd678d` (question-flow UI chrome reclassified; actual asks kept English) |
| Merge (PR #388) | `b47bf4bb57446956c47488283248cfbacd603e85` |
| Merge parents | `a0426cbb6a188a366006d22472c875ec4e5e446b` + `62818a8c71a83be487928d8b2ccaa2feb4dd678d` |
| Merged tree | `f6ed63d94db15a5e84326f9e551a7c1eddd3dd34` |

Lineage is exactly the three D-P6-18 commits after `a0426cb`, SHA-preserving — never
squashed, rebased, amended, or force-pushed. Cumulative implementation scope
**27 files changed, +2012 / −337**, entirely under `web/` and `tests/`. `git diff --check`
clean. No `engine/`, no `domains/`, no schema/migration, no dependency, no CI, and no
governance file in the implementation diff.

## 2. Independent review and post-merge test evidence

- Independent final re-review verdict: **B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**; **BLOCKERS: NONE**.
- Independent final review on the accepted tree: **1944 passed / 1 skipped / 1 xfailed / 0 failed**;
  Playwright/browser subset **31 passed**.
- Owner Codespace post-merge verification on merge `b47bf4b`: **1913 passed / 3 skipped / 1 xfailed / 0 failed**.
- The 31-test difference is exactly the Playwright/browser subset the owner Codespace did not run; the independent
  reviewer reproduced all 31 on the identical accepted tree. Environmental/test-only — **not** a regression.
- Tracked worktree CLEAN before and after post-merge tests.

## 3. What D-P6-18 delivered (accepted product result)

- Global explicit English / Arabic UI-language selection; default UI language = English.
- The selected UI language applies consistently across active application UI chrome.
- Arabic shell uses RTL semantics; English uses LTR semantics.
- Canonical actual questions remain English; actual asks remain English while surrounding non-question UI chrome follows
  the selected UI language.
- User-authored echoed content is not intentionally translated.
- The P6-1 truthful domain labels follow the selected UI language.
- Generated substantive output remains **OUTSIDE** this UI-language increment.
- PR #148 Input Language remains separate from UI Language.
- Localization is presentation-only: a central `web/ui_text.py` seam (catalogue + `localize_message` / `localize_deep`)
  consuming the existing English source-of-truth; the deterministic guidance modules are unchanged (no forked/parallel
  question registry). Reuses the G-UX-SHELL and `web/domain_label.py` (D-FPC-MAP-06 — extend/consume).

## 4. What remains NOT implemented / NOT authorized (unchanged by this closure)

Question Translation Assistant (**NOT IMPLEMENTED / NOT AUTHORIZED**); Output-Language capability (**NOT IMPLEMENTED**);
`decision_workspace` (deferred/untouched); new domain activation; Domain Registry validation hardening (D-P6-14);
schema/migration; WS17; STG; ACV; PDF/download; output email. Closing D-P6-18 authorizes none of these.

## 5. Non-blocking observations retained (not remediated by this closure)

1. The criticality clarification "Would the idea still achieve its purpose if this part changed?" remains English as an
   actual ask, while its surrounding controls localize. Gap-label headings are localized as UI framing. Both correctly
   applied under the product-function classifier.
2. `localize_deep` uses exact-match localization and could theoretically localize echoed user content only if the user
   enters a byte-identical mapped UI-chrome sentence — assessed negligible / cosmetic by independent review.
3. Six `session.html` criticality literals exist both through `t()` catalogue keys and in `_DEEP_AR` — harmless
   redundancy.

## 6. Closure status and next governance step

**D-P6-18 — Global UI Language: FORMALLY ACCEPTED AND CLOSED.** Phase 6 as a whole is **NOT** complete. The next
governance step is the **separately authorized Master Obligation Index gate** (governance/documentation reconciliation
only) — **NOT** the implementation of any new capability; it remains **ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED**.
No successor capability (Question Translation Assistant or any other) is authorized or started by this closure. Phase 5
remains FORMALLY CLOSED; P4-2 Level-1, Draft Level 2, P5-1, P5-2, P5-3, and P6-1 remain CLOSED. Decision **D17** and the
AISR seven-owner model are preserved.
