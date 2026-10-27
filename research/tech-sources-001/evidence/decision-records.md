# TECH-SOURCES-001 — decisions returned to the Owner and Execution Lead (not resolved here)

Recorded per the Owner's 2026-10-27 architecture-boundary instruction. Nothing below is decided, implemented or sent to a reviewer.

## DR-1 — Q-02: which owner holds the motor ↔ mechanism evidence
- **Question:** under which existing owner(s) the qualified-candidate evidence (SRC-004 NASA TM X-68244; SRC-005 DOE DC motors) would sit.
- **Evidence:** SRC-004 splits naturally into load-side claims (breakaway / accelerating / running torque of the mechanism, inertia reflected through a reduction) and the torque-balance condition between motor and load; SRC-005 is motor-side (DC torque–speed behaviour, thermal continuous rating). Roadmap 28-T3 already records split authority: Electrical / Electronics owns drive / switching / conversion truth, Mechanical owns loads, transmission and mechanical suitability, and their interaction is composed through interfaces (Stage 15). The delivered CAP-13 rotational-load method (Mechanical) evaluates one declared running-load model and says it does not discharge this blocker.
- **Alternatives:** (A) Mechanical only; (B) Electrical / Electronics only; (C) bounded division — load-side claims with Mechanical, motor-side claims with Electrical / Electronics, the balance condition held only as an interface statement under Stage 15.
- **Evidence-based recommendation (not a selection):** (C) best matches the recorded 28-T3 split and the existing CAP-13 load method; it creates no new owner. Implication: any statement that a *particular* motor can drive a *particular* mechanism would be a compatibility conclusion, which stays outside current authority (D4 NOT ACTIVATED).
- **Decision owner:** Owner, with the ChatGPT Execution Lead.
- **Outcome (recorded from the base branch, not decided here):** CLAUDE.md on `feature/atomic-json-session-persistence` at `692c2d9` (PR #889, 2026-10-27) records that the Owner approved **Option C for ownership only**: Mechanical owns load-side motion, force, speed and torque requirements; Electrical / Electronics owns motor electrical and drive characteristics; Stage 15 composes attributed interface statements without assessing a particular pairing. It notes SRC-004 is not admitted production provenance and its residual authorship / IP qualification stays explicit.

## DR-2 — Q-01: which condition D-7 must govern
- **Question:** which applicability condition D-7 requires before the stiffness method could ever be admitted, and whether a qualitative declaration may satisfy it when no numeric criterion exists.
- **Evidence:** run-6 table in `findings/per-question-findings.md` (SRC-014/015/016; NACA 180; TM-86442). Verified: elastic condition (qualitative), constant-section / straight-beam / creep / moisture / temperature conditions (qualitative), property test geometry span/depth 14 (fact). Not found: any numeric small-deflection, elastic-limit or span-to-depth validity limit for Eq. 9–2.
- **Alternatives:** (1) govern by small deflection (no qualified numeric source yet); (2) govern by elastic condition (qualitative only); (3) govern by the property test geometry (e.g. an applicability declaration tied to span/depth relative to 14 — a policy choice, not a source-stated limit); (4) accept qualitative declarations (as THERM-01 D-1…D-6 do) instead of a numeric criterion; (5) keep D-7 open.
- **Implications:** (1)–(3) as numeric gates would require a source the research has not found, or an Owner-chosen threshold (the contract forbids arbitrary thresholds); (4) would need a contract amendment; (5) keeps the method unadmitted.
- **Decision owner:** Owner, with the ChatGPT Execution Lead. No condition selected here.

## DR-3 — Q-03: definition of the 28-T2 "execution-facing output" claim
- **Question:** the exact statement the deferred item refers to.
- **Evidence:** only CLAUDE.md (e) names it; roadmap 28-T2 lists candidate concerns, not a claim.
- **Missing:** an exact claim (which concern, what statement). Without it no source can be qualified. D13 stays PAUSED; no Embedded / Firmware execution is implied.
- **Decision owner:** Owner, with the ChatGPT Execution Lead.
