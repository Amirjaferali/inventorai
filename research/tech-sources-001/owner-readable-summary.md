# TECH-SOURCES-001 — owner readable summary

*Updated after run 1 (2026-10-27). Research evidence only: nothing here is admitted, implemented, activated or qualified as a product method.*

**Status:** ACTIVE · runs used 1 / 20 · Perplexity queries 4 / 240 · campaign ends 2026-11-26 at the latest.

**Questions registered:** 10 open-type questions (Q-01…Q-10: 3 Tier 1, 7 extracted at activation — 2 individual / verification, 5 cross-technology),
plus 4 held and 5 excluded items recorded so they are not re-derived (D13 sensor ↔ controller work, Sensors C3, D4 interface characterisation
and IoT stay held; delivered work stays excluded).

**Researched in run 1:** Q-01, Q-02, Q-03.

**Sources inspected directly (5):** NACA Report 180 (1924); NASA TN D-7572 (1974); NASA TM-86442 (1985); NASA TM X-68244 (1973); DOE-HDBK-1011/2-92 Vol. 2 (1992). Hash and page of each are in `evidence/source-provenance-register.md`.

**What we learned**
- *Motor ↔ mechanism (Q-02):* a qualified-candidate federal source (NASA TM X-68244) states, for any motor type, that a motor can drive a
  mechanism only if its torque covers the load's breakaway, accelerating and running torque across the whole speed range; steady speed means
  the torques balance. The DOE handbook supports the same for DC motors only. This is evidence for the blocked "preliminary motion" item; who
  would own it (Mechanical or Electrical / Electronics) is still your decision.
- *Wooden-beam stiffness regime (Q-01):* the strongest lead (NACA Report 180) is the historical test basis of the stiffness method's own
  formula and shows good agreement on spans of 2–14 ft, but it gives no stated limit of where the formula stops being valid. The other span /
  depth figures found only say when shear can be ignored, which this method does not do. So D-7 is narrowed but not closed.
- *Embedded output (Q-03):* not researchable yet — the exact claim is undefined and the item waits on a specialist owner.

**Unresolved scientific / IP points:** D-7 governing condition not sourced; DOE handbook authorship (contractor-prepared) has no blanket
public-domain conclusion; the USDA Forest Service hosts (FPL-RN-0210) are blocked from this environment.

**Excluded from further searching (delivered or settled):** transistor load switching (PR #885), DC resistive load calculations, TMP36
conversion, CAP-13 planar moment / required force / rotational load, THERM-01 single path, T2-G / R2, T6 quantity / BOM.

**Next independent questions:** Q-01 (one more targeted search), then Q-04 (stiffness verification measurements) and Q-05 (logic output ↔
driver input).
