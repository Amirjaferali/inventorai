# D13-TKP-PKG-001 — Phase B: Owner-Readable Summary

## What Phase B did
It gathered and quality-graded **technical evidence** for the seven Phase B research questions (PB-RQ-1…PB-RQ-7),
strictly within the single-signal sensor→microcontroller concept class (analog-voltage / single-ended-digital /
pulse-frequency; low-voltage; non-safety-critical). It is **evidence, not product**: no code, no schema, no
architecture, nothing built, nothing merged.

## What we found (in plain terms)
For each question, the technical literature clearly identifies **which governing parameters decide the answer** —
and confirms that InventorAI generally **cannot** decide a specific case without the target device's datasheet:

1. **Output type (PB-RQ-1):** Sensor outputs are analog-voltage, single-ended-digital, or pulse-frequency. Free text
   isn't enough to classify them reliably — you need a typed field or the datasheet.
2. **Voltage range (PB-RQ-2):** Every input has an absolute-maximum rating (roughly −0.5 V to just above the supply);
   overvoltage can destroy the part unless a pin is explicitly "5 V-tolerant." The exact numbers are device-specific.
3. **ADC range & logic levels (PB-RQ-3):** An analog signal must fit the ADC's reference range; a digital signal must
   meet the input's HIGH/LOW thresholds (VIH/VIL). Both depend on the specific target device.
4. **Pulse/frequency (PB-RQ-4):** These are read with a timer/counter, and the pulse must first meet the digital logic
   thresholds.
5. **Impedance/loading (PB-RQ-5):** A high-impedance sensor into an ADC can cause errors; there are rule-of-thumb limits
   (~10 kΩ for 8–10-bit, ~2.5 kΩ for 12-bit) and a buffer fixes it. The exact limit is device-specific.
6. **Datasheet sufficiency (PB-RQ-6):** The literature lists exactly which parameters you need — and confirms that when
   they're missing, **the correct action is to abstain**, not guess. (We did **not** adopt a product abstention rule;
   that's a governance decision.)
7. **Conditioning need & routing (PB-RQ-7):** You can diagnostically flag that conditioning is needed, and record the
   *decision* about which method to use separately from actually *doing* it.

## Honesty note you should know about
We could **search** authoritative sources (Analog Devices, Microchip, TI, etc.) but this session's network policy
**blocked direct downloads** of their PDFs (HTTP 403). So the governing parameters are **corroborated across multiple
sources** but not verified against the original PDF text, and all **device-specific numbers are deliberately left
unresolved (abstained)**. This is recorded truthfully throughout — nothing was invented.

## What this does NOT mean
It does not approve any requirement, answer any RQ officially, decide any real device, or authorize building anything.
Every specific numeric compatibility question still needs the actual target datasheet, and every downstream step
(review, acceptance, TKP, architecture, implementation) remains a **separate owner decision**.

## Where it stops
Research is finished for the authorized scope and **stops here** — before publication, merge, TKP, architecture, tests,
or implementation. The Phase A record is untouched (still locked at `57e2fac8`); nothing was committed, pushed, or
merged.
