# Workstream 9 — Single-Intent Question Design — GREEN Evidence Package

**Record type:** durable governance evidence package for Workstream 9 (Single-Intent Question Design)
BASE RED and GREEN, captured after the owner-accepted, merged, and independently verified GREEN.

**Status:** docs/evidence-only. Authorizes no implementation, no closure, and no Workstream 10 work.
Workstream 9 remains **OPEN — GREEN MERGED AND VERIFIED — EVIDENCE AND CLOSURE PENDING**.

**Authoritative branch:** `feature/atomic-json-session-persistence`
**Authoritative tip at capture:** `d787a959ce2e66e7e328f761996792b33c237d05`

---

## 1. Repository and ancestry

Full raw capture: [`IDENTITY_ANCESTRY.txt`](./IDENTITY_ANCESTRY.txt).

| Gate | PR | Merge commit | Ordered parents | Tree | Changed files |
|------|----|--------------|-----------------|------|---------------|
| BASE RED | #237 | `f180eab882f5c5d395ad7ae87a7a09a54315d5f1` | `4c7a5714` (base), `016f6d66` (head) | `77ca698c` | `A tests/test_workstream_9_single_intent_question_design.py` |
| BASE RED status canonicalization | #238 | `7fb1ff06c890edaf233a94e9d9985a3a231ccacb` | `f180eab8` (base), `b5750d9a` (head) | `9bb61152` | `M ACTIVE_EXECUTION_ROADMAP.md`, `M DELIVERABLE_STABILIZATION_REMEDIATION_PLAN.md` |
| GREEN | #239 | `d787a959ce2e66e7e328f761996792b33c237d05` | `7fb1ff06` (base), `78f62c9d` (head) | `437bf885` | `M docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json` |

Integrity: the PR #239 merge tree `437bf885…` is byte-identical to the reviewed GREEN head `78f62c9d`'s
tree — the merge introduced exactly the reviewed content and nothing else.

The BASE RED reviewed head `016f6d66` preserved the 3-commit chain `a01beb78 → 5ecc0b4b → 016f6d66`.

## 2. BASE RED evidence

The BASE RED suite `tests/test_workstream_9_single_intent_question_design.py` (merged via PR #237)
is a deterministic marker-based guard against cosmetic single-intent passes, swept over the committed
serving surface `engine.path_n_questions.get_path_n_question`.

At the BASE RED (before GREEN), against the then-committed multi-intent question content, the focused
suite produced:

- **3 intended RED failures** — the CONFIRMED MULTI-INTENT questions **N-PF-1, N-PF-2, N-BA-1**, each
  presenting markers for ≥ 2 independent intent components.
- **15 passes**, comprising:
  - **8 protected** (single-intent verbatim N-MC-3 / N-MC-4 / N-PF-4; deterministic serving by index;
    WS8 fixed-priority selection; PARTIAL/unknown states; WS1–8 modules intact; no WS10–14 module);
  - **6 adversarial-control** (formerly-excluded-index defect still flagged; verbatim defect appended
    as a new variant flagged; N-PF-2 inflection flagged; honest single-intent split passes; exact
    UNRESOLVED baselines excluded but rewrites not; N-PF-4 protected baseline excluded from sweep);
  - **1 diagnostic** (serving seam reaches every artifact-defined variant).

**Independent BASE RED review verdict: B — VALID WITH NON-BLOCKING DOCUMENTARY RECOMMENDATIONS**
(after two prior verdict-C hardening cycles: WS9-BR-F1/F2/F3, then F8/F9/F10). Accepted non-blocking
recommendations preserved for this package:

1. Record the complete focused result profile (3 RED + 15 passes = 8 protected + 6 adversarial + 1 diagnostic).
2. Preserve the independent BASE RED verdict-B review as a durable committed artifact (this README §7).
3. GREEN must satisfy single-intent through natural wording, not marker evasion (the `react` / `not react`
   substring adjacency must not be exploited).
4. The exact protected-regression command and result must be recorded in this evidence package
   (see [`PROTECTED_WS1_8.txt`](./PROTECTED_WS1_8.txt)).
5. The artifact sweep and serving-surface parity diagnostic must remain coupled.

The BASE RED status was canonicalized to `BASE RED ACCEPTED AND PUBLISHED — GREEN NOT AUTHORIZED`
via PR #238.

## 3. GREEN evidence

GREEN (PR #239, reviewed head `78f62c9d`) made the minimum question-content change: it rewrote the three
CONFIRMED MULTI-INTENT served questions to single-intent, natural, non-technical wording. Only the runtime
serving artifact changed (`engine.path_n_questions` serves the text verbatim, so no code change was needed).
Exactly 3 insertions / 3 deletions in one file. N-PF-3, N-PF-4, N-BA-2, N-BA-3, and all N-MC questions were
preserved byte-verbatim.

**Final single-intent question texts** (also [`GREEN_QUESTION_TEXTS.txt`](./GREEN_QUESTION_TEXTS.txt)):

| ID | Gap | Final text |
|----|-----|-----------|
| N-PF-1 | PHYSICAL_FEASIBILITY | `What would need to be true for this system to work safely in the real world?` |
| N-PF-2 | PHYSICAL_FEASIBILITY | `What do you think would keep the system running reliably over time?` |
| N-BA-1 | BOUNDARY_AMBIGUITY | `Which situations should the system be responsible for handling?` |

**Execution evidence (exact commands + raw outputs committed in this package):**

| Gate | Command file | Result |
|------|-------------|--------|
| WS9 focused | [`WS9_FOCUSED.txt`](./WS9_FOCUSED.txt) | **18 passed** |
| Protected WS1–8 | [`PROTECTED_WS1_8.txt`](./PROTECTED_WS1_8.txt) | **214 passed** |
| Persistence / resume | [`PERSISTENCE_RESUME.txt`](./PERSISTENCE_RESUME.txt) | **129 passed, 1 skipped** |
| Full suite | [`FULL_SUITE.txt`](./FULL_SUITE.txt) | **31 failed, 1444 passed, 1 skipped, 1 xfailed, 24 xpassed** |
| Failure distribution | [`FAILURE_DISTRIBUTION.txt`](./FAILURE_DISTRIBUTION.txt) | all 31 failures confined to `tests/test_domain_registry.py`; **0** failures outside it |

The 31 failures are the known pre-existing `tests/test_domain_registry.py` baseline (neither fixed nor
worsened by a question-content change); the non-zero full-suite exit code is solely due to that documented
baseline. There are **zero new unrelated failures** and no import, fixture, malformed-JSON, or harness error.

**Non-evasion:** the BASE RED test file was not modified by GREEN, so the marker sets are unchanged; the
6 adversarial controls still flag synthetic multi-intent strings; the three final texts contain neither
`react` nor `not react`. GREEN passes because the questions are genuinely single-intent.

**Independent GREEN implementation review verdict: B — GREEN VALID WITH NON-BLOCKING RECOMMENDATIONS**
(no blocking findings; identity/scope/tests/non-evasion/governance all verified; gates reproduced exactly).

## 4. Preserved non-blocking findings

1. **Dropped "confusing situations" component (information-loss).** Original N-BA-1 probed three asks
   (when the system should act, when it should not, and what situations might confuse it). The single-intent
   rewrite retains only the positive scope ("which situations it should be responsible for handling"). The
   negative-boundary and confusable-edge elicitation are therefore no longer directly asked. This is the
   correct single-intent reduction. **No `N-BA-4` or follow-up question is added under this authorization;**
   its proper placement is deferred to a separately authorized content or adaptive-follow-up (WS14) gate.
2. **N-BA-1 wording / vocabulary overlap (UX).** "responsible for handling" is understandable but mildly
   abstract/formal for a fully non-technical inventor, and overlaps in vocabulary with N-BA-2
   (`What is your idea responsible for, and what is someone or something else's job?`). This is a documented
   UX observation only; the reviewed GREEN head is **not** altered under this authorization.
3. **Protected and persistence battery commands** are committed here (`PROTECTED_WS1_8.txt`,
   `PERSISTENCE_RESUME.txt`) with their exact command lines.

## 5. Content-spec / implementation-plan drift — determination

The current-state N-PF-1 / N-PF-2 / N-BA-1 multi-intent texts are also quoted in:

- `docs/governance/PATH_N_QUESTION_CONTENT_SPECIFICATION.md` (lines 85, 129, 131, 139)
- `docs/governance/FUNCTIONAL_PATH_N_IMPLEMENTATION_PLAN.md` (line 125)
- `docs/governance/NON_SPECIALIST_MODE_SEPARATION_DESIGN_PLAN.md` (line 108)

**Determination: these are frozen, point-in-time governance records, NOT current normative documents whose
text the runtime must match.** Each is dated 2026-06-10/11 and carries the status
`COMMITTED … — NO IMPLEMENTATION AUTHORIZED` ("Content is specified before any code, domain file, prompt,
route, session, or test changes"). Their quoted question text is the **documented defect baseline** — the
same MI-* multi-intent strings recorded as defect #13 in
`docs/governance/evidence/workstream1_deliverable_baseline/WS1_DEFECT_MANIFEST.md` and in the WS9 contract
(§3 evidence). The single current normative source of served content is the runtime artifact
`docs/governance/path_n_content_config/electronics_electrical_path_n_questions.json`
(`metadata.runtime_integrated: true`), which now serves the corrected single-intent text.

**Boundary (justified):** these historical documents are **NOT synchronized** in this increment, because
rewriting their quoted text would rewrite historical defect evidence (an explicit stop condition) and would
desynchronize them from the WS1 defect manifest that cites them. Any forward "spec of record" reconciliation
(e.g., adding a WS9-aware amendment/annotation that records the corrected text alongside the preserved
original) is a normative-documentation action **recorded here as PENDING**, to be performed only under a
separate owner authorization. This increment changes no historical defect evidence.

## 6. Governance invariants at capture

- Workstream 9 remains **OPEN** — GREEN merged and verified; evidence acceptance and formal closure pending.
- No Workstream 9 closure is claimed or recorded.
- Workstream 10 (Question Intent Registry) remains **NOT STARTED**; no WS10+ capability is introduced.
- Phase A branch `research/d13-tkp-pkg-001-phase-a-read-only-analysis` remains fixed at
  `57e2fac837f333224b2f985be285fe9e0a9f6243`.
- PR #167 (`74ea297f…`) and PR #162 (`088ab884…`) remain untouched.
- No production question-content, test, engine, UI, schema, registry, evaluator, persistence, analytics,
  prompt, or progression change is made by this evidence increment.

## 7. Owner authorization and independent reviews (durable record)

- **Owner BASE RED acceptance and PR #237 merge authorization** — accepted verdict B; merged as
  `f180eab8`.
- **Owner BASE RED status-canonicalization acceptance and PR #238 merge authorization** — accepted
  verdict B; merged as `7fb1ff06`; §15 status → `BASE RED ACCEPTED AND PUBLISHED — GREEN NOT AUTHORIZED`.
- **Independent BASE RED review — verdict B** — VALID WITH NON-BLOCKING DOCUMENTARY RECOMMENDATIONS.
- **Owner GREEN implementation authorization** — minimal question-content change for N-PF-1/N-PF-2/N-BA-1.
- **Independent GREEN implementation review — verdict B** — GREEN VALID WITH NON-BLOCKING RECOMMENDATIONS;
  no blocking findings.
- **Owner GREEN acceptance and PR #239 merge authorization** — accepted verdict B; merged as `d787a959`.
- **Owner evidence-package and post-GREEN status-synchronization authorization** — this increment.

## 8. Package contents

| File | Purpose |
|------|---------|
| `README.md` | this narrative |
| `IDENTITY_ANCESTRY.txt` | raw PR #237 / #238 / #239 merge identities, parents, trees, changed files |
| `GREEN_QUESTION_TEXTS.txt` | the three final single-intent texts on the authoritative tip |
| `WS9_FOCUSED.txt` | WS9 focused suite command + raw output (18 passed) |
| `PROTECTED_WS1_8.txt` | protected WS1–8 battery command + raw output (214 passed) |
| `PERSISTENCE_RESUME.txt` | persistence/resume command + raw output (129 passed, 1 skipped) |
| `FULL_SUITE.txt` | full-suite command + raw output (31 failed / 1444 passed / 1 skipped / 1 xfailed / 24 xpassed) |
| `FAILURE_DISTRIBUTION.txt` | proof all 31 failures are confined to `tests/test_domain_registry.py` |
| `MANIFEST.sha256` | SHA-256 of every other file in this package |
