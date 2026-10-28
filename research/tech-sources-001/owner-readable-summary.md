# TECH-SOURCES-001 — owner readable summary

*Updated after run 9 (2026-10-27). Research evidence only: nothing here is admitted, implemented, activated or qualified as a product method.*

**Status:** ACTIVE — not complete. Runs 12 / 20 · Perplexity queries 38 / 240 · deep-research calls 0 · window ends 2026-11-26.
**Questions registered:** 23 (Q-01…Q-23) plus held / excluded items. **Sources inspected directly:** 41 (hash, page and rights in `evidence/`).

| Q | Topic | Result |
|---|---|---|
| Q-01 | Wood-beam stiffness — D-7 conditions | Inspected facts qualified: property test geometry span/depth 14 VERIFIED (Wood Handbook p. 5–8); elastic, straight-beam, constant-section, creep, moisture and temperature conditions stated qualitatively. **No machine-checkable criterion exists** in the USDA sources. Decision DR-2 is yours. |
| Q-02 | Motor ↔ mechanism | Qualified candidate. Ownership decided by you: DR-1 Option C (base 692c2d9). SRC-004 residual authorship / IP qualification still open. |
| Q-03 | Embedded "execution-facing output" | No exact claim in any record (DR-3). |
| Q-04 | Deflection-test measurements | Qualified candidate, now including moisture, temperature, load rate and creep. |
| Q-05 | Logic output ↔ driver | UNVERIFIED — ibiblio now fails certificate trust (emSign root missing in this environment); NXP server refuses. |
| Q-06 | Battery capacity vs rate / temperature | Qualified candidate. |
| Q-07 | PLC sinking / sourcing | Partial: sinking concept, I/O circuit types and datasheet checks qualified (ModEL PLC, CC BY 4.0); explicit pairing rule UNVERIFIED. |
| Q-08 | Control sample rate | Qualified candidate. |
| Q-09 | Thermal-resistance measurement | Qualified candidate. |
| Q-10 | Fits and tolerances | Qualified candidate (one point indirect). |
| Q-11 | PWM average voltage | Partial (duty × supply implied by a NASA example, not stated). |
| Q-12 | Two-link kinematics | Partial (general forward-solution principle; explicit formula UNVERIFIED on clean-rights source). |
| Q-13 | Free-space path loss | Partial (NASA link-budget statement; far-field / inverse-square conditions UNVERIFIED — NTIA host refused). |
| Q-14 | Cells in series / parallel, balancing | Qualified candidate (DOE + NASA, reused). |
| Q-15 | Imaging spatial resolution | Source candidate only — IP unresolved (mixed NASA / contractor preprint); USGS refused. |
| Q-16 | Duty-cycled average current | Source candidate only — IP unresolved (NIST-hosted journal / conference papers); core claim UNVERIFIED. |
| Q-17 | Multirotor hover thrust and margin | Qualified candidate (NASA Ames). |
| Q-18 | PV rating conditions | Partial: standard test conditions sourced (DOE FEMP); temperature effect not yet on a clean-rights source. |
| Q-19 | Vacuum outgassing screening | Qualified candidate (NASA PT-TE-1410). |
| Q-20 | Double-acting cylinder forces | Partial: DOE hydraulics basics found; rod-side area and speed–flow unverified. |
| Q-21 | Inverse-square irradiance conditions | Qualified candidate (NIST SP 250-95). |
| Q-22 | Thermal expansion and mismatch | Qualified candidate (NBS Circular 486, NASA TP-2226). |
| Q-23 | Resonance (spring–mass) | Queued for run 11. |
| Q-13, Q-24, Q-25 (run 11) | Free-space conditions; IoT security baseline; firmware update integrity / recovery | Qualified candidates (NBS TN 12 / TN 101; NIST blog + FAQ; NIST SP 800-193). |
| Q-26, Q-28, Q-30 (run 12) | IoT power / failure; real radio channels; battery limits and BMS protection | Q-28, Q-30 qualified candidates (NIST TN 1604, NISTIR 8243; NASA battery guideline); Q-26 partial. |
| Q-24…Q-40 | IoT security / updates / power / privacy, RF channel and capacity, battery limits and ageing, converters, motor classes, watchdogs, interlocks, Earth-observation trade-offs, hover power, MPPT, eclipse power, vibration isolation | Added 2026-10-28 (Owner correction) from the roadmap's recorded concerns; queued by priority. |

**Decisions:** DR-1 decided by you (Option C, recorded on the base branch). Still open with you and the Execution Lead: DR-2 which condition D-7
governs; DR-3 definition of the 28-T2 "execution-facing output" claim. Details in `evidence/decision-records.md`.

**Current access blockers:** www.ibiblio.org — certificate chain to emSign Root CA - G1 not trusted in this environment (passed this morning,
fails since the session restart); www.nxp.com — NXP returns its own 404 page; www.nrc.gov document — NRC's CDN returns 403;
its.ntia.gov, stac.astrogeology.usgs.gov and openmodelica.org — proxy policy denial; www.faa.gov — no response. To unblock ibiblio, the environment needs the emSign root trusted or the earlier
routing restored; nothing was bypassed.
