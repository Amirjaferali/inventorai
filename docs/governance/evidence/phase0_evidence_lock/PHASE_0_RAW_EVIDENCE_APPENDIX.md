# Phase 0 — Raw Evidence Appendix

Supporting evidence for the four Phase 0 registers. **This is an evidence
appendix, not a fifth governance register.** Read-only; no mutation.

## 1. Repository identity
- Repository: `Amirjaferali/inventorai`
- Remote: `http://…/git/Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Official tip: `1d1385f2140be4e8ab1612ce07596a2170cfa0a0`

## 2. PR #289 / PR #290 merge evidence
```
# PR #290 (this-plan status sync) — official tip is its merge commit
git log -1 --format="%s" 1d1385f2  →  Merge pull request #290 from Amirjaferali/docs/product-foundation-plan-post-merge-status-sync
git rev-list --parents -n1 1d1385f2 →
  1d1385f2140be4e8ab1612ce07596a2170cfa0a0 224def7572c6869d4aef35897f124900ae4e351b 4251e9977d96626b837d999e0b119f541decd752
# PR #289 (plan v2 adoption) merge commit
224def7572c6869d4aef35897f124900ae4e351b  — subject: Merge pull request #289 from …/docs/product-foundation-commercial-readiness-plan-v2
  ordered parents: 78490ab4146a220f9e2a91d9586f5be5c9ab2338 , 666b9330c36ff31f8c7a7b7aa5129f5770a022f8
git merge-base --is-ancestor 224def75 1d1385f2  → ancestor OK (PR #289 merged)
git merge-base --is-ancestor 4251e997 1d1385f2  → ancestor OK (status-sync commit merged)
```

## 3. Phase 0 lifecycle correction
- During the performed operation: `PHASE 0 ACTIVE — READ-ONLY EVIDENCE-LOCK GATE`.
- **Authorization provenance (clarification):** the Phase 0 read-only evidence-lock
  operation was authorized **externally by the owner in the execution
  conversation**. **No in-repository authorization artifact exists for that
  operation**; this statement is **execution-context evidence, not repository
  evidence**. Phase 0 remains **OPEN and not formally closed**. (No new
  authorization document is created by this record.)
- Current: `PHASE 0 OPEN — READ-ONLY DISCOVERY COMPLETED — REGISTER DOCUMENTATION PREPARED — NOT YET MERGED OR FORMALLY CLOSED`.
- The earlier phrasing "eligible, not active" was inaccurate and is corrected here.

## 4. Official-tree scope and exclusions
- Scope: git-tracked files at official tip `1d1385f2140be4e8ab1612ce07596a2170cfa0a0`.
- Exclusions: `.git`; untracked transfer bundles (`*.bundle`) and other untracked transfer evidence; generated artifacts; binary files (`git grep -I` skips binaries). These are outside `git grep` / `git ls-tree <tip>` by construction.

## 5. Numerical evidence (commands + outputs)
```
InventorAI occurrences:  git grep -I -o -e "InventorAI" 1d1385f2 -- .   →  369
InventorAI files:        git grep -I -l -e "InventorAI" 1d1385f2 -- .   →  139
  split:  web/ = 14   engine/ = 0   docs/ = 287   (remainder: README/CLAUDE.md/scripts/domains)
  user-facing runtime strings in web/app.py:  L2 (docstring), L248, L351 (unsupported-domain messages)
governance Markdown:
  docs/governance/*.md (top level):  238
  docs/governance/**  (recursive):   304
  all tracked .md repo-wide:         377
routes:   git grep -c -e "@app.route" 1d1385f2 -- web/app.py   →  20
templates (web/templates/*.html): 5
  decision_workspace.html, deliverable.html, index.html, session.html, success_criteria.html
remote heads:  git ls-remote --heads origin | wc -l   →  299
  main    = 0e89e4636399760965c9ff8086b465c90dbadf8e
  official= 1d1385f2140be4e8ab1612ce07596a2170cfa0a0
evidence subdirs/entries under docs/governance/evidence/:  20
```
Note: the earlier review's "349 occurrences / 138 files" was measured at the
pre-plan tip `78490ab`. The current 369 / 139 reflects the added canonical plan +
roadmap/CLAUDE.md documentation — a documentation increase, not new code
hard-coding (web/ hard-coding is unchanged at 14).

## 6. Prior-review reuse proof (byte-identity, not ancestry-only)
Earlier reviewed commit `78490ab4146a220f9e2a91d9586f5be5c9ab2338`; current `1d1385f2140be4e8ab1612ce07596a2170cfa0a0`.
```
git diff --name-only 78490ab 1d1385f2  →  exactly:
  CLAUDE.md
  docs/governance/ACTIVE_EXECUTION_ROADMAP.md
  docs/governance/PRODUCT_FOUNDATION_AND_COMMERCIAL_READINESS_REMEDIATION_PLAN.md
git diff --stat 78490ab 1d1385f2  →  3 files changed, 717 insertions(+), 3 deletions(-)

Subtree object hashes (equal ⇒ byte-identical across the range):
  web:                       661b309b22f19670063bb0feddd8911cbc6e172c   IDENTICAL
  engine:                    853908201692019617ca36d35d72a42105868d76   IDENTICAL
  domains:                   bc38b62835cd00d4ea27ca993d44720e6edaee67   IDENTICAL
  tests:                     78a29b90c23bb214a74d564d051e4c4a3ea1815e   IDENTICAL
  docs/governance/evidence:  530cca92dbfa846635f67542db24d97142adc16c   IDENTICAL
```
Conclusion: every technical, architectural, runtime, register, and evidence
source reused from the earlier source review is byte-identical; only the three
governance-documentation files changed between the earlier-reviewed tip and now.

## 7. Refined CR-1 — code evidence
```
engine/domain_rules.py  (commit 02374a2c8b698aa5e7ef5ce36bf035f22348bcfe):
  L12  def infer_domain(idea_text: str) -> str | None:
  L21  priority = ["medical_device", "electronics_electrical", "mechanical", "software"]   (latent multi-domain)

web/app.py  (commit df4836bf1864e1abf84ee37ea80339115c17a0a2), /start L383–447:
  - require request.form["domain_confirm"] == DOMAIN_CONFIRM_VALUE else CONFIRMATION_REQUIRED_MESSAGE
  - _has_strong_unsupported_evidence(lowered) → UNSUPPORTED_DOMAIN_MESSAGE (no session)
  - domain in CONFLICTING_SUPPORTED_DOMAINS & insufficient lay-electrical → MECHANISM_GUIDANCE_MESSAGE (no session)
  - domain not None & unknown → UNSUPPORTED_DOMAIN_MESSAGE (refuse)
  - on admission:  state.domain = DOMAIN_CONFIRM_VALUE   (always electronics_electrical; never the inferred value)
Test evidence: `tests/test_domain_gate_entry_ux.py` was inspected but not run.
Existing committed tests support rejection-path behavior. No test-count claim is
relied upon for CR-1. Neutral repository audit facts (recorded here as audit facts
only, NOT as the basis for CR-1): 27 test functions; 18 total occurrences of
`_assert_not_admitted`; 17 calls excluding the helper definition.
```
Determination: `infer_domain` holds LATENT multi-domain capability; the active
`/start` gate admits only electronics_electrical sessions. Conflict is
documentation-/stale-report-vs-latent-code. **CR-1 severity = LOW.**

## 8. Refined CR-3 — branch and authority evidence
```
OWNER_PRODUCT_IDENTITY_CORRECTION.md (5768d31…) L18–21:
  "PROPOSED until §11 satisfied … EFFECTIVE only upon … HEAD = origin/main and ahead/behind = 0 0"
STRATEGIC_PRODUCT_VISION.md (6c2277f…) L46–47:
  "GOVERNING EFFECT AMENDED … amended by the active Level 0 Owner Amendment"
CLAUDE.md (4251e99…) L11: lists OWNER_PRODUCT_IDENTITY_CORRECTION.md as mandatory read #2
Branch: official feature tip 1d1385f2… ; origin/main 0e89e4636399760965c9ff8086b465c90dbadf8e
  ⇒ HEAD = origin/main is never satisfied on the feature branch.
```
Determination: literal §11 = PROPOSED; later/higher sources treat it operative ⇒
effective-vs-proposed ambiguity. **CR-3 = MEDIUM; sequenced as B — the first
Owner Decision inside Phase 1 (OD-C).**

## 9. SOURCE NOT FOUND
```
git ls-tree -r --name-only 1d1385f2 | grep -iE "start_here|architecture_index"  →  (no match)
```
- `START_HERE` — **SOURCE NOT FOUND** at the official tip (any path).
- `ARCHITECTURE_INDEX` — **SOURCE NOT FOUND** at the official tip (any path).
(Present instead: `ARCHITECTURE_GUARDRAILS.md`, `docs/WORKFLOW_PROTECTION_STANDARD.md`.)

## 10. Test-execution statement
Protected/domain-gate tests were **inspected (committed source read) but NOT
re-run** in this gate; no test execution or mutation-producing command was run.
No bundle files or untracked transfer evidence were included in any count above.
