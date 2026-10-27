# TECH-SOURCES-001 — contradictions and unresolved issues

Append-only.

| Date | Question | Issue |
|---|---|---|
| 2026-10-27 | Q-01 | Not a contradiction but a scope clarification: every span-depth figure found (SRC-001, SRC-002) answers "when may shear be neglected", while the stiffness method already includes the shear term. The D-7 governing condition therefore remains open between (i) small-deflection geometry (SRC-003: qualitative only), (ii) a lower span-depth limit for the shear-inclusive formula itself (SRC-001 shows agreement over its tested range but states no limit) and (iii) an elastic (proportional-limit) condition. Choosing among them is a Lead / Owner decision, not a research finding. |
| 2026-10-27 | Q-01 | SRC-001 Table I agreement is partly calibrated (per-beam E back-computed from the same tests; F a fixed fraction of mean E) — it is not independent validation. |
| 2026-10-27 | Q-01 (run 2) | New lead, unverified: the bending moduli the method uses (Wood Handbook Table 5-3a) come from small-clear centre-loaded tests reported in search snippets to use a span-to-depth ratio of 14 (ASTM D143). If the Wood Handbook itself states this test basis, the "+10 %" shear correction in D5-3 is tied to that test geometry — a source-defined condition relevant to D-7. Needs direct inspection of FPL-GTR-190 Ch. 5 (host blocked here; the D-5 precedent used a Lead-supplied inspection). |
| 2026-10-27 | Q-06 (run 3) | CONTRADICTION in wording: DOE-HDBK-1011/2-92 ES-04 p. 2 says ampere-hours indicate "the amount of energy" a battery can deliver, while the admitted PR #802 reference (and SRC-008 / SRC-009, which treat Ah as charge and Wh as energy) states that A·h is an amount of charge, not energy. The admitted PR #802 boundary stands; SRC-007 must not be quoted for that sentence. |
| 2026-10-27 | Q-08 (run 3) | Sources disagree on a numeric sample-rate rule (≥ 30×, > 10×, 5–20×, 6–10× closed-loop bandwidth): evidence that no single class-level threshold exists. |
| 2026-10-27 | Q-01 (run 6) | RESOLVED lead: the span-to-depth-14 property basis (run 2 "UNVERIFIED") is now verified from the Wood Handbook itself (SRC-014 p. 5–8). |
| 2026-10-27 | Q-01 (run 6) | Unchanged: no inspected source gives a numeric small-deflection, elastic or span-to-depth validity limit for Eq. 9–2. |
