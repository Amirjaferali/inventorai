# Phase 3B — Owner UX/Product Decision Agenda

**Type:** documentation-only agenda record (candidate). **DOCUMENTED NO-VALID-RED.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified prerequisite tip:** `7816bdaddd762c38e6fa8cbbf05b7de26022e306`.

This record **collects the agenda only**. It decides no Phase 3B UX choice unless the owner has
already made an explicit, current, committed decision. It does **not** activate Phase 3 and
grants no implementation authority.

## Canonical Phase 3 structure (unchanged — do not rename)

```
3A — Discovery and Current-State Inventory (read-only)
3B — Owner UX/Product Decisions
3C — Low-Fidelity Prototype (non-production design only)
3D — Independent Usability and Accessibility Review
3E — Owner Acceptance of the Exact Design
3F — Bounded Implementation Increments (each separately contracted/tested/reviewed/accepted/merged/verified)
```

Phase 3F increments run under the Lean Governance protocol: once a Phase 3F increment contract
is authorized, the agent completes it without per-file approval, still requiring
contract → implementation → required verification → bounded independent review → concise owner
acceptance report → separately authorized merge where required.

## Phase 3B agenda (decisions to be made by the owner in 3B)

1. Target user-facing screens.
2. Target audience and non-specialist journey.
3. Technical Decision Workspace classification: user-facing / operator-facing / internal /
   advanced mode / excluded.
4. Project Technology Profile specification.
5. Primary/secondary domain and subsystem presentation.
6. Active / reserved / inactive / unsupported state taxonomy.
7. Arabic/English parity strategy.
8. Default language and language switching.
9. Page-level RTL.
10. Mobile-first vs desktop-first priority.
11. Design-system approach.
12. Flask-template continuation vs separately governed frontend architecture.
13. Product shell and navigation.
14. Help, Settings, Privacy & Terms, and future Account locations.
15. Sponsor placement and eligible pages.
16. Multiple-sponsor ordering.
17. Theme ownership: administrator, user, or both.
18. Administrative-notice timing, frequency, close, and acknowledgment behavior.
19. Privacy/trust communication placement.
20. Output states and user acceptance.
21. Direct Output Download placement.
22. Email Delivery placement.
23. ACV placement and eligibility.
24. ACV relationship to the output.
25. User approval and output-version selection.
26. Guidance-panel hierarchy and consolidation.
27. Expressed-intent clarity from WS8 (design depth only; do not reopen WS8).
28. Deeper answer-support design boundary from WS13 (do not reopen WS13).
29. Follow-up/completion design boundary from WS14 (do not reopen WS14).
30. Guidance-consolidation design depth from WS15 (do not reopen WS15).
31. Progress-vs-verification presentation.
32. Legacy ILT-002 route disposition: preserve historical evidence route / convert to test-only /
    guard by non-production environment / retire through a later bounded increment.

## Bottom-of-page owner notes (mandatory inputs — carried forward, not decided here)

**A. Sponsor recognition, multiple sponsors, themes, colors.** Phase 2 recorded boundaries only
(OD-R-A). Phase 3 decides/designs placement; one-or-many; ordering; activate/deactivate;
global/page scope; Arabic/English; RTL; responsive; theme/color. Recognition-only — not
advertising, behavioral targeting, campaign management, or auctioning. Must never alter technical
evaluation, idea progression, evidence assessment, scoring, or engine behavior. Durable admin /
per-user state depend on later foundations.

**B. Centrally configurable administrative notice.** Phase 3 designs title; message; Arabic/English;
optional image; active/inactive; start/end; page applicability; onboarding/first use;
once/per-user/per-version/controlled frequency; close; optional acknowledgment; priority;
non-disruptive presentation. Durable per-user/per-version frequency and acknowledgment depend on
Phase 4 persistence and Phase 5 accounts.

**C. Privacy, confidentiality, user trust.** Preserve the layered model: (1) onboarding notice;
(2) inline contextual notice; (3) permanent Privacy & Terms location; (4) popup only when
appropriate. The popup must not be the only privacy mechanism. No absolute or unsupported claims;
every user-facing statement must match actually-implemented controls. Use the narrow user-facing
"idea" terminology rule in privacy/trust/onboarding/sensitive-data contexts. **No** repository-wide
technical replacement of the word "invention".

**D. Arabic/English, RTL, accessibility.** Current Arabic/RTL support is narrow and panel-scoped.
Full Arabic/English design, page-level RTL, locale ownership, switching, responsive behavior, and
accessibility are Phase 3 matters. Current absence stays honestly visible. No implementation
authorized here.

**E. Multi-domain target identity.** Product identity is multi-domain and cross-domain;
Electronics/Electrical is the current experimental MVP runtime scope. Phase 3 prepares honest
multi-domain-ready UX; Phase 6 owns domain/capability/subsystem foundations; Phase 9 owns per-domain
activation. No inactive domain may be shown as currently supported; no domain expansion authorized.

**F. Structured Technical Guidance.** RESERVED / INACTIVE. Must not be absorbed into Phase 3, ACV,
output design, or any increment. Separate explicit owner authorization is mandatory before any UI,
schema, prompt/AI, database, test, architecture, or implementation work.

These reminders are discoverable from `OWNER_DECISION_REGISTER.md` and this agenda — not from chat
memory or footer text.
