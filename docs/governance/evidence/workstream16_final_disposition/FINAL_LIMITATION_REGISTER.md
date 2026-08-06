# WS16 — Final Limitation Register (Owner-Accepted, MVP-Bounded)

**Purpose.** Durable record of every WS16 limitation the owner has accepted for
the current MVP scope. This register records **owner-accepted limitations only**.
It does **not** remediate any limitation, does **not** record final stage-level
owner acceptance, and does **not** perform WS16 formal closure.

## Authoritative context

| Item | Value |
|---|---|
| Repository | `Amirjaferali/inventorai` |
| PR under disposition | #284 (open, not merged) |
| PR #284 final head | `cef898eedd010c5ddcefa0eb608957c2e7629692` |
| Correction parent | `d2d99687440e694ed2a2e294c873a5b6bce702b6` |
| Register branch base | `cef898eedd010c5ddcefa0eb608957c2e7629692` |
| Product state | `DEMO_READY_WITH_LIMITATIONS` |
| Approved MVP scope | ELECTRONICS / ELECTRICAL ONLY |

## Acceptance boundary (verbatim owner disposition)

```
ALL IDENTIFIED WS16 LIMITATIONS ACCEPTED FOR THE CURRENT MVP SCOPE
FINAL BLOCKERS: NONE
SEPARATE APPLICATION REMEDIATION REQUIRED BEFORE WS16 CLOSURE: NO
```

Acceptance is strictly bounded to product state `DEMO_READY_WITH_LIMITATIONS` and
MVP scope ELECTRONICS / ELECTRICAL ONLY. It does **not** mean production
readiness, deployment approval, full bilingual parity, durable session recovery,
authentication readiness, subscription readiness, regulatory compliance,
patentability, safety verification, or technical completion beyond the committed
evidence. No limitation below is remediated; each remains open and is routed to a
future, separately-authorized destination.

---

## Register entries

### WS16-IR-101 — In-memory-only session storage

- **finding_id:** WS16-IR-101
- **subject:** Sessions are stored in memory only (`SESSION_STORE = {}`).
- **source evidence:** `web/app.py` L4 (documented in-memory/non-production/temporary), L40; VALIDATION_REPORT §E; STAGE_RESULTS Stage 11.
- **severity:** MEDIUM
- **classification:** LIMITATION
- **affected stage or scenario:** Stage 11 (persistence and recovery).
- **user impact:** A session does not survive a process restart; work in progress is not durably retained across restarts.
- **verified boundary:** `SESSION_STORE` is a per-process in-memory dict; missing/unknown session redirects safely (no fabricated recovery).
- **unverified boundary:** Any durable-storage behavior — none exists to verify.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking; does not block WS16 closure.
- **future destination:** Durable session persistence/recovery — separately authorized technical workstream.
- **separate authorization required:** YES.

### WS16-IR-102 — Absence of durable/atomic session recovery

- **finding_id:** WS16-IR-102
- **subject:** No durable or atomic JSON session-recovery surface exists in committed source.
- **source evidence:** no `session_store`/persistence/atomic module in the tree at `143a1ed4`; only disk write is the append-only `/tmp` transcript; VALIDATION_REPORT §E (PR-1/2/4/5/6/8).
- **severity:** MEDIUM
- **classification:** LIMITATION — EXECUTION SURFACE ABSENT
- **affected stage or scenario:** Stage 11; PR-1, PR-2, PR-4, PR-5, PR-6, PR-8.
- **user impact:** Save/reload, restart recovery, and previous-valid-state preservation are not available.
- **verified boundary:** No atomic session-write / recovery path is reachable from `web/app.py`.
- **unverified boundary:** Recovery correctness — no recovery surface exists to exercise.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking. Recorded as a LIMITATION, not a blocker; not duplicated as a blocker (see PR-1…PR-8 subsection below).
- **future destination:** Durable session persistence/recovery — separately authorized technical workstream.
- **separate authorization required:** YES.

### WS16-IR-103 — No authentication layer

- **finding_id:** WS16-IR-103
- **subject:** No authentication/authorization layer in the committed MVP (no login/account routes).
- **source evidence:** VALIDATION_REPORT §D SP-1; STAGE_RESULTS Stage 12; absence of login/account routes in `web/app.py`.
- **severity:** MEDIUM
- **classification:** LIMITATION
- **affected stage or scenario:** Stage 12 (security and privacy); SP-1.
- **user impact:** No user accounts, sign-in, or per-user access control; the app is a non-authenticated demo surface.
- **verified boundary:** No auth boundary is claimed or present; no false auth behavior.
- **unverified boundary:** Any authentication/authorization guarantee — none exists.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking.
- **future destination:** Real registration/authentication/account/logout — separately authorized workstream **after** the Product UX/UI foundation.
- **separate authorization required:** YES.

### WS16-IR-104 — `/tmp` transcript contains user idea text

- **finding_id:** WS16-IR-104
- **subject:** The append-only `/tmp/ilt002_transcript_{sid}.jsonl` transcript persists user-authored idea text locally as ILT-002 evidence.
- **source evidence:** `web/app.py` L778–L781; VALIDATION_REPORT §D SP-2; STAGE_RESULTS Stage 12.
- **severity:** MEDIUM
- **classification:** LIMITATION
- **affected stage or scenario:** Stage 12 (security and privacy); SP-2.
- **user impact:** User-authored idea text is written in plaintext to a predictable local path with no lifecycle/cleanup; no secrets/credentials are exposed.
- **verified boundary:** No secrets, tokens, credentials, or stack traces are written; content is the user's own idea text; "No engine effect".
- **unverified boundary:** Transcript retention/cleanup lifecycle — none defined.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking.
- **future destination:** Privacy hardening and transcript lifecycle — separately authorized security/privacy workstream.
- **separate authorization required:** YES.

### WS16-IR-105 — Partial Arabic/English coverage and no full RTL

- **finding_id:** WS16-IR-105
- **subject:** Only the uncertainty-support panel is bilingual (EN+AR); four other guidance seams are English-only; no page-level RTL; no canonical locale owner.
- **source evidence:** Unicode inspection of `web/uncertainty_guidance.py` (Arabic present) vs the four other seams (no Arabic script); VALIDATION_REPORT §G; STAGE_RESULTS Stage 13.
- **severity:** LOW
- **classification:** LIMITATION
- **affected stage or scenario:** Stage 13 (Arabic/English limitations).
- **user impact:** Arabic-reading users receive bilingual support only on the uncertainty panel; the rest is English-only; no RTL layout.
- **verified boundary:** No full bilingual parity is claimed; existing Arabic on the uncertainty panel is present.
- **unverified boundary:** Full bilingual parity / RTL correctness — not implemented.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking.
- **future destination:** Arabic/RTL completion — separately authorized localization workstream.
- **separate authorization required:** YES.

### WS16-IR-106 — Progress-versus-verification clarity limitation

- **finding_id:** WS16-IR-106
- **subject:** The progression↔technical-verification boundary is communicated at the display layer and partly relies on wording.
- **source evidence:** STAGE_RESULTS Stage 8; `web/result_feedback.py`, scaffolding guidance, `engine/derived_readiness.py`.
- **severity:** LOW
- **classification:** LIMITATION
- **affected stage or scenario:** Stage 8 (progress/completion/progression/verification distinctions).
- **user impact:** A user could under-read the distinction that progression is not technical verification/completion/safety/patentability/readiness.
- **verified boundary:** The product never asserts verification/readiness from progression; product state `DEMO_READY_WITH_LIMITATIONS`.
- **unverified boundary:** UX-level comprehension strength — a forward UX/UI concern.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking.
- **future destination:** Product UX/UI and Accessibility — after formal WS16 closure.
- **separate authorization required:** YES.

### WS16-IR-107 — Bounded final-result/handoff limitation

- **finding_id:** WS16-IR-107
- **subject:** Deliverable synthesis quality is bounded; deeper synthesis improvements remain a recorded forward backlog.
- **source evidence:** STAGE_RESULTS Stage 9; `engine/deliverable_assembler.py`; representative-journey README "Current limitations".
- **severity:** LOW
- **classification:** LIMITATION
- **affected stage or scenario:** Stage 9 (final result or handoff).
- **user impact:** The final result/handoff is honest but limited in synthesis depth; it must not appear more complete/verified than it is.
- **verified boundary:** Result is presented with explicit limitations; no overclaim of completeness/verification.
- **unverified boundary:** Deeper synthesis quality — unimplemented backlog.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking.
- **future destination:** Recorded forward deliverable-synthesis backlog (post-closure, separately authorized).
- **separate authorization required:** YES.

### WS16-IR-002 — Incomplete ARIA tablist pattern (representative journey)

- **finding_id:** WS16-IR-002
- **subject:** The representative-journey stepper does not implement the complete ARIA tablist pattern.
- **source evidence:** prior representative-journey independent review; `docs/governance/evidence/workstream16_representative_journey/` (non-production prototype).
- **severity:** LOW
- **classification:** LIMITATION
- **affected stage or scenario:** Representative-journey prototype (non-production; comprehension artifact only).
- **user impact:** Assistive-technology semantics of the stepper are incomplete in the low-fidelity prototype; no committed-application impact.
- **verified boundary:** Prototype is explicitly non-production; committed application unaffected.
- **unverified boundary:** Full accessibility conformance — not implemented in the prototype.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking.
- **future destination:** Product UX/UI and Accessibility — after formal WS16 closure.
- **separate authorization required:** YES.

### WS16-IR-003 — Focus not preserved after direct stage navigation (representative journey)

- **finding_id:** WS16-IR-003
- **subject:** After direct stage navigation in the prototype, keyboard focus is not preserved/managed.
- **source evidence:** prior representative-journey independent review; representative-journey prototype.
- **severity:** LOW
- **classification:** LIMITATION
- **affected stage or scenario:** Representative-journey prototype (non-production).
- **user impact:** Keyboard/AT users may lose focus context on direct navigation in the prototype; no committed-application impact.
- **verified boundary:** Prototype non-production; committed application unaffected.
- **unverified boundary:** Focus-management conformance — not implemented in the prototype.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking.
- **future destination:** Product UX/UI and Accessibility — after formal WS16 closure.
- **separate authorization required:** YES.

### WS16-IR-004 — Fragile attribute-escaping pattern with no current exposure (representative journey)

- **finding_id:** WS16-IR-004
- **subject:** A fragile attribute-escaping pattern exists in the prototype with no current exposure.
- **source evidence:** prior representative-journey independent review; representative-journey prototype.
- **severity:** LOW
- **classification:** LIMITATION
- **affected stage or scenario:** Representative-journey prototype (non-production).
- **user impact:** None currently exposed; pattern is fragile and could matter if the prototype were ever productized (it must not be).
- **verified boundary:** No current exposure; prototype is static/non-production with no network, no untrusted input path.
- **unverified boundary:** Robustness under productization — out of scope for a non-production prototype.
- **owner disposition:** ACCEPTED for current MVP scope.
- **closure effect:** Non-blocking.
- **future destination:** Product UX/UI and Accessibility — after formal WS16 closure.
- **separate authorization required:** YES.

---

## Persistence/recovery scenarios (recorded as LIMITATIONs, not blockers)

The six absent-surface persistence scenarios are recorded here as LIMITATIONs
under WS16-IR-102 and are **not** duplicated as separate blockers.

| Scenario | Classification |
|---|---|
| PR-1 — Normal save and reload | LIMITATION — EXECUTION SURFACE ABSENT |
| PR-2 — Process-restart recovery | LIMITATION — EXECUTION SURFACE ABSENT |
| PR-4 — Malformed/unreadable artifact | LIMITATION — EXECUTION SURFACE ABSENT |
| PR-5 — Partial/interrupted write | LIMITATION — EXECUTION SURFACE ABSENT |
| PR-6 — Previous valid-state preservation | LIMITATION — EXECUTION SURFACE ABSENT |
| PR-8 — Recovery evidence integrity | LIMITATION — EXECUTION SURFACE ABSENT |

`PR-3 — Missing session artifact` and `PR-7 — Session identity isolation` remain
`PASS` (not limitations). No claim is made that durable persistence or recovery
exists.

---

## Pre-existing baseline (not a WS16 limitation, not a WS16 blocker)

The 31 `tests/test_domain_registry.py` failures are a **PRE-EXISTING NON-WS16
BASELINE ISSUE**, **NOT ATTRIBUTABLE TO WS16** (fixture/schema-expectation drift:
`schema_version=None` vs expected `'1.0'`). They are recorded in
`FINAL_BLOCKER_REGISTER.md` as non-WS16 and require a **SEPARATE REMEDIATION PATH
IF LATER AUTHORIZED**. They are neither an accepted WS16 limitation nor a WS16
blocker.

---

## Register totals

```
OWNER-ACCEPTED LIMITATIONS (distinct finding_ids): 10
  WS16-IR-101, WS16-IR-102, WS16-IR-103, WS16-IR-104, WS16-IR-105,
  WS16-IR-106, WS16-IR-107, WS16-IR-002, WS16-IR-003, WS16-IR-004
PERSISTENCE SCENARIOS recorded under WS16-IR-102: PR-1, PR-2, PR-4, PR-5, PR-6, PR-8
ALL LIMITATIONS: UNREMEDIATED, OWNER-ACCEPTED FOR MVP SCOPE
FUTURE WORKSTREAMS: NOT ACTIVATED
```

## Future-destination sequence (approved order; none activated here)

1. Product UX/UI and Accessibility — after formal WS16 closure.
2. Real registration/authentication/account/logout — separately authorized, after the Product UX/UI foundation.
3. Subscription and billing — only after authentication.
4. Durable session persistence/recovery — separately authorized technical workstream.
5. Arabic/RTL completion — separately authorized localization workstream.
6. Privacy hardening and transcript lifecycle — separately authorized security/privacy workstream.

None of the above is activated by this register.
