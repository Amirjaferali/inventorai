# D13-TKP-PKG-001 — Phase B Source & Provenance Register

**Retrieval date:** 2026-07-22. **Retrieval channel:** WebSearch (allowed). **Method:** DOCUMENT REVIEW / DATASHEET
COMPARISON. **Scope:** Gate 2 concept class only.

## Access limitation (recorded truthfully)
Direct WebFetch of primary vendor PDFs and several reference pages returned **HTTP 403** under this session's
organization **egress policy** (destination hosts not allowed; confirmed against `/root/.ccr/README.md` and
`$HTTPS_PROXY/__agentproxy/status`, which reported the proxy healthy with no relay failures). Primary-source **exact
quotation could not be verified**; the governing parameters below are recorded as **surfaced via search and attributed
to the named authoritative sources**, and are graded on cross-source corroboration (see
`evidence/evidence-quality-assessment.md`). Hosts observed to 403: `analog.com`, `microchip.com`,
`developerhelp.microchip.com`, `ww1.microchip.com`, `interfacebus.com`, `controllerstech.com`.

## Source register
| Key | Source (as surfaced) | Publisher / authority class | URL | Retrieval basis |
|---|---|---|---|---|
| S1 | AN3521 — Analog Sensor Measurement and Acquisition | Microchip (vendor app note) | https://www.microchip.com/content/dam/mchp/documents/MCU08/ApplicationNotes/ApplicationNotes/Analog-Sensor-Measurement-and-Acquisition-DS00003521A.pdf | search-surfaced (PDF fetch 403) |
| S2 | ADC input voltage / absolute-maximum ratings discussion | TI E2E; STM32 community (vendor forums) | https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/1072558/ads130e08-maximum-and-minimum-analog-input-voltage · https://community.st.com/t5/stm32-mcus-products/stm32l47x-adc-maximum-input-voltage/td-p/452832 | search-surfaced |
| S3 | MT-098 — Low Voltage Logic Interfacing | Analog Devices (tutorial) | https://www.analog.com/media/en/training-seminars/tutorials/MT-098.pdf | search-surfaced (PDF fetch 403) |
| S4 | STM32 Input Capture; AN1473 pulse/duty-cycle; MSP/PIC pulse accumulator | ST / Microchip / TI (vendor) | https://controllerstech.com/input-capture-in-stm32/ · https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ApplicationNotes/ApplicationNotes/AN1473-Various-Solutions-Calculating-Pulse-Duty-Cycle-DS00001473.pdf | search-surfaced |
| S5 | ADC Acquisition Time & source impedance | Microchip Developer Help | https://developerhelp.microchip.com/xwiki/bin/view/products/data-converters/adc-specs/acquisition-time/ | search-surfaced (fetch 403) |
| S6 | Interfacing Sensors with Microcontrollers: ADC/I2C/SPI/1-Wire | NerdyElectronics (reference) | https://nerdyelectronics.com/interfacing-sensors-with-microcontrollers-adc-i2c-spi-and-1-wire/ | search-surfaced |
| S7 | Sensor Interfacing: A Complete Beginner's Guide | Electronics For U (reference) | https://www.electronicsforu.com/technology-trends/learn-electronics/sensor-interfacing | search-surfaced |
| S8 | Level shifting 5V↔3.3V; overvoltage / absolute-max VDD+0.3V | Random Nerd Tutorials; Hackaday (reference) | https://randomnerdtutorials.com/how-to-level-shift-5v-to-3-3v/ · https://hackaday.com/2016/12/05/taking-it-to-another-level-making-3-3v-and-5v-logic-communicate-with-level-shifters/ | search-surfaced |
| S9 | AD7709 datasheet (buffered input GND+100mV…VDD−100mV) | Analog Devices (vendor datasheet) | https://www.analog.com/media/en/technical-documentation/data-sheets/ad7709.pdf | search-surfaced (PDF fetch 403) |
| S10 | ADS130E08 (absolute input AVSS−300mV…AVDD+300mV) | Texas Instruments (vendor) | https://e2e.ti.com/support/data-converters-group/data-converters/f/data-converters-forum/1072558/ads130e08-maximum-and-minimum-analog-input-voltage | search-surfaced |
| S11 | Logic voltage thresholds by family (TTL/CMOS/LVCMOS) | interfacebus.com; Circuit Cellar (reference) | http://www.interfacebus.com/voltage_threshold.html · https://circuitcellar.com/resources/quickbits/logic-levels/ | search-surfaced (fetch 403) |
| S12 | TTL vs CMOS thresholds; 74HC 3.5V vs 74HCT 2.0V; 0.3/0.7·VDD | Zbotic; PIJA Education (reference) | https://zbotic.in/cmos-vs-ttl-logic-speed-power-and-voltage-comparison/ · https://pijaeducation.com/basic-electronics/computing/ttl-logic-levels/ | search-surfaced |
| S13 | AN4225 — properly acquiring analog signals (source impedance) | Microchip (vendor app note) | https://ww1.microchip.com/downloads/aemDocuments/documents/MCU08/ApplicationNotes/ApplicationNotes/Max-Signal-Properly-TipsTrick-Acq-Analog-Signals-DS00004225.pdf | search-surfaced (PDF fetch 403) |
| S14 | Improving ADC accuracy with high input source impedance | Analog Devices (technical article) | https://www.analog.com/en/resources/technical-articles/how-to-improve-adc-measurement-accuracy-with-highinput-source-impedance.html | search-surfaced (fetch 403) |
| S15 | Reading a datasheet: key electrical parameters (VIH/VIL/VOH/VOL) | Zbotic (reference) | https://zbotic.in/arduino-datasheet-reading-understand-any-sensor-or-ic-spec/ | search-surfaced |
| S16 | Datasheet parameter guidance; insufficient-info → abstain/seek specs | Zbotic; NTC datasheet guide (reference) | https://zbotic.in/arduino-datasheet-reading-understand-any-sensor-or-ic-spec/ · https://www.ptcntcsensor.com/blog/5-key-parameters-to-help-you-understand-an-ntc-temperature-sensor-datasheet | search-surfaced |
| S17 | Fundamental Signal Conditioning (level/attenuate/amplify/filter/impedance/linearize) | Digilent (vendor reference PDF) | https://files.digilent.com/datasheets/Signal-Conditioning.pdf | search-surfaced |
| S18 | Analog front-end signal conditioning; buffer when Zsource>10kΩ | Zbotic (reference) | https://zbotic.in/arduino-analog-front-end-signal-conditioning-for-sensors/ · https://zbotic.in/analog-sensor-signal-conditioning-op-amp-circuit-designs/ | search-surfaced |

## Provenance notes
- **Authority classes:** vendor primary (datasheets/app notes: S1, S3, S4, S5, S9, S10, S13, S14, S17); vendor
  support forums (S2, S10); independent technical references (S6, S7, S8, S11, S12, S15, S16, S18). Vendor-primary
  content is the strongest authority for governing parameters; references are used for corroboration and framing.
- **No production/journey/personal data** was used. No paid/restricted/confidential source was accessed. Retrieval was
  bounded to the seven named topics; no unbounded crawling.
- **Out-of-scope material encountered** (I²C/SPI/1-Wire bus interfacing, bidirectional MOSFET level shifters) was
  excluded from findings — see `evidence/contradictions-and-unresolved-issues.md`.
