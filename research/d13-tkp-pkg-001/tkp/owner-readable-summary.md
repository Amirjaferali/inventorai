# D13-TKP-PKG-001 — Technical Knowledge Package: Owner-Readable Summary

## What this package is
A **knowledge record** for the approved concept class — single-signal sensor→microcontroller interfacing
(analog-voltage / single-ended-digital / pulse-frequency; low-voltage; non-safety-critical). It organizes what the
accepted Phase A and Phase B work established into seven knowledge units. It builds **nothing**: no code, no schema, no
architecture, no calculator, no device picker, no recommendations.

## The seven knowledge units (plain terms)
1. **KU-01 Output type** — a sensor's output is analog-voltage, single-ended-digital, or pulse-frequency; free text
   can't reliably classify it — you need a typed field or the datasheet.
2. **KU-02 Voltage range** — inputs have an absolute-maximum rating (~−0.5 V to just above the supply); overvoltage can
   destroy the part unless a pin is explicitly "5 V-tolerant." Exact numbers are device-specific and left open.
3. **KU-03 ADC range & logic levels** — an analog signal must fit the ADC's reference range; a digital signal must meet
   the input's HIGH/LOW thresholds. Both depend on the specific device.
4. **KU-04 Pulse/frequency** — read with a timer/counter, and the pulse must first meet the digital logic thresholds.
5. **KU-05 Impedance/loading** — a high-impedance sensor into an ADC can cause errors; rule-of-thumb limits exist
   (~10 kΩ for 8–10-bit, ~2.5 kΩ for 12-bit) and a buffer fixes it. Exact limit is device-specific.
6. **KU-06 Datasheet sufficiency** — the literature lists which parameters you need, and confirms that when they're
   missing the right action is to **abstain**, not guess. (We did **not** adopt a product abstention rule — that's a
   governance decision.)
7. **KU-07 Conditioning & routing** — you can flag that conditioning is needed and record the *decision* about which
   method to use, separately from actually doing it.

## Two honesty points carried forward
- **Not primary-verified.** Phase B could search authoritative sources but the environment **blocked direct downloads**
  of the original vendor PDFs (HTTP 403). So the governing parameters are corroborated across sources but not verified
  against the original documents — recorded truthfully, never dressed up as primary-source verification.
- **Device-specific numbers stay open.** Every exact figure (max ratings, VIH/VIL, VREF, source-impedance limits) is
  deliberately **abstained** — it needs the actual target datasheet, which isn't in the accepted evidence.

## What this does NOT mean
It approves no requirement, answers no research question officially, decides no real device, and authorizes building
nothing. Every specific numeric compatibility question still needs the actual datasheet, and every downstream step
(review, acceptance, architecture, implementation) is a **separate owner decision**.

## Status
Constructed as **uncommitted working-tree files** for independent (non-authoring) review. Nothing is committed, pushed,
or merged. The Phase A record is untouched (still locked at `57e2fac8`). Owner acceptance of the completed TKP, and the
mandatory post-D13 "Structured Invention Disclosure and Patent Export Owner Decision," remain separate future decisions.
