# MORE DETAIL NEEDED / GUIDED ANSWER SCAFFOLDING — MANUAL DEMO VERIFICATION (POST-PR #109)

## 1. Status

`DOCUMENTATION-ONLY EVIDENCE RECORD — MANUAL DEMO / SMOKE VERIFICATION;
NON-ACTIVATING; AUTHORIZES NO IMPLEMENTATION`

This document records the result of a read-only / runtime-only manual demo
verification of the officially merged More Detail Needed / Guided Answer
Scaffolding implementation (PR #108), performed after PR #109. It records
evidence only. It changes no runtime behavior and authorizes nothing.

---

## 2. Authoritative context

- Repository: `Amirjaferali/inventorai`
- Authoritative branch: `feature/atomic-json-session-persistence`
- Authoritative tip verified against: `ee3e50558ff17e10fd8eecb8bd088f7d6493328d`
  (PR #109 roadmap-synchronization true merge)
- Verification date: 2026-07-07
- Verification method: the real Flask application was driven in-process through
  its WSGI test client (real `/start` and `/session/<sid>` routes and the real
  `web/templates/session.html` template) from a read-only detached worktree at
  the authoritative tip. No network/port was opened; no repository file was
  modified.
- Current official state remains `DEMO_READY_WITH_LIMITATIONS`; the MVP remains
  electronics/electrical-only (`MVP_SCOPE_FREEZE.md`).
- `main` remains `0e89e4636399760965c9ff8086b465c90dbadf8e` (unchanged); the
  frozen persistence worktree remains PRESERVE UNMODIFIED AND PAUSE at
  `aec9cf6409efc18e125b6745762002f59e529654` (untouched).

---

## 3. Verification classification

**MANUAL DEMO VERIFICATION PASS**

---

## 4. Demo path

`POST /start` → `POST /session/<sid>` (answer) → `GET /session/<sid>` (render),
plus a synthetic PASS render and an unsupported-domain `POST /start`.

---

## 5. Input idea (admitted by the Domain Gate)

`"A plug-in device with a current sensor and a microcontroller that alerts over
Wi-Fi."`

Observed: admitted — `POST /start` returned `302` redirecting to `/session/<sid>`.

---

## 6. Insufficient answer submitted

`"It alerts people."`

---

## 7. Observed WARN / More Detail Needed result

- `transition`: `WARN`
- `reason`: `"MECHANISM_COMPLETENESS asserted only — reasoning required"`
- The existing "More detail needed" WARN badge was present (unchanged behavior).

---

## 8. Observed guidance (the new display-only surface)

- Heading: **"What kind of detail to add"**
- Lead: explained that the answer says *what happens* but not *how or why it
  works* — "Your answer says what happens, but not how or why it works. Add the
  missing mechanism or reasoning — describe what makes it work."
- Five category prompts (content-free, category-level):
  - What physical part or mechanism does this use?
  - What condition triggers the action?
  - What does the device sense or detect?
  - What output or response happens?
  - What evidence or observation supports this?
- Non-mutation note present ("… do not change or grade your answer — you write
  it in your own words.").

---

## 9. Original answer preservation

Confirmed: the stored transcript response was exactly `"It alerts people."` —
byte-for-byte unchanged. The guidance did not write, rewrite, improve, correct,
or complete the answer; the prompts are a fixed deterministic set independent of
the answer text.

---

## 10. Direction text

Confirmed visible: `Direction: PROGRESSING` (existing behavior intact).

---

## 11. Increment 1B question-level clarification

Confirmed: the Increment 1B "Help me understand this question" expander remained
visible where expected (current question + clarification present on the WARN
page). It is a separate surface from the new answer-insufficiency guidance.

---

## 12. PASS renders no guidance

Confirmed: a synthetic session with a PASS `last_result` rendered **no** guidance
heading. Guidance appears only for WARN-class insufficiency.

---

## 13. Unsupported-domain rejection

Confirmed: `POST /start` with `"a purely mechanical gearbox with a rotating shaft
and bearing torque"` returned `200`, displayed the stable unsupported-domain
message ("… supports electronics and electrical ideas only …"), and created **no
session**. PR #101 Domain Gate behavior is preserved.

---

## 14. No Answer Clarification / Improve Wording flow

Confirmed: no rewrite/clarify/approve UI appeared. No Inventor Answer
Clarification / Improve Wording Assistant flow is present.

---

## 15. Forbidden fields absent from the rendered body

Confirmed absent from the rendered page: `suggested_clarified_answer`,
`user_approved_answer`, `original_user_answer`, `clarification_status`.

---

## 16. No repository mutation during verification

Confirmed: the verification was read-only. No repository file was edited, staged,
committed, pushed, merged, or otherwise changed; the temporary read-only worktree
was removed afterward. The only runtime side effect was the application's own
pre-existing behavior of appending an ILT-002 transcript line under `/tmp` on
answer submit — that is app behavior writing outside the repository, not a
repository or frozen-worktree change.

---

## 17. Official state

Confirmed unchanged: `DEMO_READY_WITH_LIMITATIONS`.

---

## 18. MVP scope

Confirmed unchanged: electronics/electrical-only.

---

## 19. Remaining limitation

The underlying scoring behavior is unchanged (e.g. `assess_response`'s
generic-verb trap and the two-`REASONED`-per-gap close requirement). The
increment improves the clarity of the *feedback* the inventor sees when an
answer is already scored WARN; it does not change how answers are scored. Any
scoring-behavior change remains a separate, not-yet-authorized future decision.

---

## 20. Final statement

This document records evidence only and authorizes no further implementation.
Any next step — a scoring-behavior review, the Inventor Answer Clarification /
Improve Wording Assistant, persistence work, or a new candidate — requires its
own separate owner scope decision, Increment Contract if needed, implementation
authorization, tests, independent review, and an owner-gated true merge.
