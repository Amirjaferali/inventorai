# TECH-SOURCES-001 — owner readable summary

*Updated after run 5 (2026-10-27). Research evidence only: nothing here is admitted, implemented, activated or qualified as a product method.*

**Status:** HELD — not complete. Every reachable source has been used; the rest needs documents, host access or decisions from you. Runs 5 / 20 · Perplexity queries 21 / 240 · deep-research calls 0.

**Questions registered:** 10 (Q-01…Q-10) plus 4 held and 5 excluded items recorded so they are not re-derived.
**Researched:** all 10.

| Q | Topic | Result | Key source(s) |
|---|---|---|---|
| Q-01 | Wood-beam stiffness method — where the formula stops being valid (D-7) | BLOCKED — narrowed; property-basis and small-deflection claims UNVERIFIED | NACA Report 180; NASA TM-86442; NASA TN D-7572 (not transferable) |
| Q-02 | Can a motor drive a mechanism — load characteristics | QUALIFIED-CANDIDATE | NASA TM X-68244; DOE-HDBK-1011/2-92 (DC only) |
| Q-03 | Embedded controller "execution-facing output" | QUESTION UNCLEAR / AUTHORITY BLOCKED | — |
| Q-04 | What a deflection test must measure before comparing with the estimate | QUALIFIED-CANDIDATE | NBS Report 10568; NACA Report 180 |
| Q-05 | Logic output ↔ driver / load | SOURCE ACCESS BLOCKED — claim UNVERIFIED | (NXP AN2434 / AN2433, Kuphaldt Vol. IV — hosts refused) |
| Q-06 | Battery capacity vs discharge rate and temperature | QUALIFIED-CANDIDATE | NASA/TM-2009-215751; DOE-HDBK-1084-95 |
| Q-07 | PLC sinking / sourcing I/O ↔ field device | PARTIAL — levels supported; sinking/sourcing rule UNVERIFIED | NISTIR 5331 (levels only) |
| Q-08 | Digital control sample rate vs loop bandwidth | QUALIFIED-CANDIDATE | NASA TM-88346 |
| Q-09 | Measuring a thermal resistance | QUALIFIED-CANDIDATE | NIST SP 400-86 |
| Q-10 | Fits and tolerances vs manufacturing process | QUALIFIED-CANDIDATE (one point indirect) | NISTIR 4509 |

**Sources inspected directly (13):** each with its file hash, exact page and rights record in `evidence/`.

**Unresolved scientific / IP points:** D-7 governing condition; the Wood Handbook test basis (span-to-depth 14) seen only in snippets of a
protected ASTM standard; DOE fundamentals handbooks have no blanket public-domain conclusion (contractor-prepared); manufacturer application-note
rights not read; one DOE sentence calls ampere-hours "energy", conflicting with the admitted PR #802 boundary (the admitted boundary stands).

**Blocked hosts:** USDA Forest Service (research.fs.usda.gov, fpl.fs.usda.gov), standards.doe.gov, govinfo.gov, nal.usda.gov, archive.org,
UNT digital library, ibiblio.org, nxp.com, nrc.gov.

**Excluded from searching (delivered or settled):** transistor load switching (PR #885), DC resistive load calculations, TMP36 conversion,
CAP-13 planar moment / required force / rotational load, THERM-01 single path, T2-G / R2, T6 quantity / BOM; held: D13 sensor ↔ controller,
Sensors C3, D4 interface characterisation, IoT.

**What you must supply to finish (any item restarts the campaign):**

| For | Exact document / permission | URL that is refused here | Evidence still missing |
|---|---|---|---|
| Q-01 | USDA FPL, *Wood Handbook* FPL-GTR-190 (2010), Ch. 5 "Mechanical Properties of Wood" — p. 5-2 and Table 5-3a notes (test method / span-to-depth basis of bending E) | https://research.fs.usda.gov/treesearch/37427 | Whether the tabulated bending moduli rest on centre-loaded tests at span/depth 14 |
| Q-01 | USDA FPL, *Wood Handbook* FPL-GTR-190, Ch. 9 "Structural Analysis Equations" (any stated applicability limit of Eq. 9-2) | https://research.fs.usda.gov/treesearch/37423 | A source-stated validity range of the shear-inclusive deflection equation |
| Q-01 | I. Orosz, *Simplified Method for Calculating Shear Deflections of Beams*, USDA FPL Research Note FPL-0210 (1970) | https://research.fs.usda.gov/download/treesearch/5840.pdf | Its criterion for when shear deflection matters |
| Q-01 | Your choice of the condition D-7 must govern (decision, not a document) | — | — |
| Q-05 | T. R. Kuphaldt, *Lessons in Electric Circuits* Vol. IV "Digital", logic-output / sourcing-sinking sections, with its licence appendix | https://www.ibiblio.org/kuphaldt/electricCircuits/Digital/ | Class-level logic-output drive statement under a checked licence |
| Q-05 | NXP (Freescale) AN2434 and AN2433, plus NXP's terms of use for application notes | https://www.nxp.com/docs/en/application-note/AN2434.pdf ; https://www.nxp.com/docs/en/application-note/AN2433.pdf | Same claim from a manufacturer, with a reuse basis |
| Q-07 | T. R. Kuphaldt ModEL module "PLC" (mod_plc.pdf, CC BY 4.0 per the author's index page) | http://ibiblio.org/kuphaldt/socratic/model/mod_plc.pdf | Sinking / sourcing pairing rule |
| Q-07 | U.S. NRC ADAMS ML063530382, "The Programmable Logic Controller and Its …" | https://www.nrc.gov/docs/ml0635/ml063530382.pdf | Federal statement of the same rule |
| Q-03 | An exact definition of the "execution-facing output" claim (Owner / Lead) | — | — |

Alternatively, allow these hosts in the environment's network settings (cloud environment menu → Edit → Network access → Allowed domains):
research.fs.usda.gov, www.ibiblio.org, ibiblio.org, www.nxp.com, www.nrc.gov. Documents you supply are inspected and hashed like any other source.

**Decisions that are yours (pending, not assumed):** (1) owner of the motor ↔ mechanism evidence (Q-02: Mechanical or Electrical / Electronics);
(2) the condition D-7 must govern (Q-01).
