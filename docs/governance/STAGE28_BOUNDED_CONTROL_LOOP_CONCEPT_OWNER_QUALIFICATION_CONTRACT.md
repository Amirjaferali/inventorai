# Stage 28 — Bounded Control-Loop Concept Owner — Qualification Contract (candidate, documents only)

**Status of THIS record:** documents-only **QUALIFICATION-CONTRACT CANDIDATE**, written under the Owner's
authorization of 2026-10-01, which covers this contract and nothing else. It defines the future owner, its qualified
scope, what it does not cover, how it is separated from the existing owners, the source basis it may use, and what
must exist before it may be declared qualified or activated. **It qualifies nothing by itself, creates no Domain Pack,
activates no domain, changes no composition, classifier, question, schema, persistence, provenance record or runtime
code, and starts no Stage 30 work.** It is not an active product increment: `ACTIVE CONTRACT: NONE` is unchanged, and
it records no Stage-28 entry or completion. It becomes the accepted qualification contract only through the Owner's
explicit acceptance of this exact document; accepting it still does not qualify or activate the owner.

`CONTROL-LOOP OWNER QUALIFICATION CONTRACT: CANDIDATE — DOCUMENTS ONLY` ·
`BOUNDED CONTROL-LOOP CONCEPT OWNER: NOT QUALIFIED — NOT ACTIVATED — NO DOMAIN PACK EXISTS` ·
`QUALIFIED ≠ ACTIVATED` · `STAGE 30 REQUIRED BEFORE ACTIVATION` · `STAGE 28 RUNTIME: NOT AUTHORIZED`

## §1. Base and settled inputs (not reopened here)

Base: `feature/atomic-json-session-persistence` at `89ad1ceb801572704a321d60fd486b11b6caa88e` (evidence of the
recorded moment, not a permanent live-tip expectation). At that base `activated_domains()` returns exactly
`['electronics_electrical', 'mechanical']`; the Domain Registry recognizes `electronics_electrical`, `mechanical`,
`medical_device` and `software`; no control-loop pack exists; `engine/subsystem_model.py` holds
`COMPOSITION_DOMAINS = ("mechanical", "electronics_electrical")`.

The following conclusions are inputs to this contract and are not reopened by it:

| Gate | Settled result |
|---|---|
| Stage-28 portfolio reassessment | `ROBOTICS ASSESSMENT TRIGGER: FIRED`; `ROBOTICS ARCHITECTURE TRIGGERED` |
| Architecture review (Fable 5.1) | `OPTION A PREFERRED` — control truth for integrated inventions needs ONE governed owner, composable later as an optional additional part; not a Robotics domain and not an ownerless reasoning layer |
| Owner-identity qualification | `NEW BOUNDED EMBEDDED-CONTROL OWNER PREFERRED`; the existing Software pack is not the preferred owner; `INDEPENDENT PEER APPEARS CLEANEST` |
| Source-authority gate | `SOURCE BASIS PARTIALLY ESTABLISHABLE` |
| Claim-binding gate | `NARROW BASELINE IS DISTINCT AND QUALIFIABLE` — as a control-loop concept owner; embedded execution is not source-backed |
| Lead source re-inspection | DOE-HDBK-1013/2-92, NASA TM-101739 and NIST SP 811 confirmed for the narrowed basis (§6) |

The earlier gates used "embedded-control" as a working label. This contract replaces it with the truthful subject
name below, because the confirmed sources do not support embedded execution.

## §2. Subject name and identity

**Subject:** `BOUNDED CONTROL-LOOP CONCEPT OWNER`.

The name states exactly what the evidence supports: concept-level truth about a control loop — what is measured, what
it is compared with, what action results, what is commanded and what feedback closes the loop. It does not claim
execution, implementation or engineering-verification depth.

The owner is explicitly:

- **NOT a real-time embedded execution owner;**
- **NOT a firmware implementation owner;**
- **NOT a safety authority;**
- **NOT a stability / tuning / calculation authority.**

**Why it exists.** It exists because of one distinct, currently unowned truth seam: the control loop between what an
integrated invention measures and what it commands. The Electronics pack declares "Firmware and embedded software
logic" outside its authority (`domains/electronics_electrical/domain.json`, `coverage_declaration.not_covered_areas`)
and its questions ask what happens electrically; the Mechanical pack owns mechanism, motion and load; Stage 15 records
the inventor's own free-text description of how two parts interact but never questions a control loop. The pack
identifier, display label and localized labels are NOT assigned by this contract.

## §3. Qualified baseline claim families (exactly nine)

The contract may qualify ONLY these families. No claim text is authored here; the meanings below are the paraphrased
scope each family may later carry, subject to the page-level binding in §10.

| # | Claim family | Bounded meaning (scope, not claim text) | Source (§6) |
|---|---|---|---|
| 1 | Control-loop fundamentals | A control system keeps a variable at, or within a range around, a desired value by monitoring it and causing action; open loop versus closed loop | DOE-HDBK-1013/2-92 |
| 2 | Feedback fundamentals | The measured result is returned and compared with the reference, which closes the loop | DOE-HDBK-1013/2-92 |
| 3 | Measured-input / reference comparison concept | The measured value of the controlled variable is compared with a reference (setpoint); the difference is what drives action | DOE-HDBK-1013/2-92 |
| 4 | Controller-side control-action concept | The comparison produces an actuating signal that acts on the controlled element — the concept only, never a control law | DOE-HDBK-1013/2-92 |
| 5 | Output / controlled-element relationship | The controlled element changes the manipulated variable, which affects the controlled output | DOE-HDBK-1013/2-92 |
| 6 | Disturbance concept, where supported | An outside influence that acts on the controlled system and that the loop responds to — only to the extent the bound source section supports it | DOE-HDBK-1013/2-92 |
| 7 | Measurement sampling / observation-rate concept only | Sampling means observing a measured signal at discrete times; observing too slowly for how fast the signal changes loses information | NASA TM-101739 |
| 8 | Time / frequency unit discipline — shared mapped knowledge | Correct naming of time and rate units; mapped from the shared NIST fact, never re-owned | NIST SP 811 |
| 9 | Explicit limits / abstention / specialist boundary | What the owner does not cover (§4), when it abstains and when a specialist is needed | InventorAI governance records |

**No other claim family is authorized by this contract.** Any future gap use stays within ADR-002
(`docs/adr/ADR-002-gap-taxonomy-strategy.md`): no new gap identifier without a taxonomy amendment, and no gap
identifier reused with a different meaning.

## §4. NOT COVERED (binding)

Each item below is **NOT COVERED**. None is implied, partially supported or supported by inference from §3:

- real-time scheduling;
- deadlines;
- jitter;
- embedded execution architecture;
- firmware implementation;
- discrete state-machine design;
- control-law design;
- PID design / tuning;
- stability analysis;
- controller tuning;
- actuator saturation / rate calculations;
- software ↔ hardware interface design;
- sensor physics;
- filtering;
- signal conditioning;
- electrical characteristics;
- mechanical response;
- project-specific control calculations;
- fail-safe / safety determination;
- SIL / ASIL;
- regulatory compliance.

In addition, the controller's own action / update rate is not covered: the bound sampling source supports only how
often a measured signal is observed (§3 family 7).

## §5. Owner-separation contract

**Electronics owns**

- electrical sensor / device characteristics;
- electrical signals;
- filtering / signal conditioning;
- voltage / current / power;
- electrical constraints;
- actuator electrical characteristics.

**Mechanical owns**

- mechanism;
- motion;
- load;
- force;
- physical actuation response.

**Stage 15 owns**

- subsystem interfaces;
- interface preparation;
- observations;
- Integration evidence;
- Integration status.

**The future bounded control-loop owner owns only**

- control-loop relationship;
- reference / comparison semantics;
- control-action relationship;
- feedback relationship;
- conceptual measurement observation rate;
- bounded control-side interpretation.

No parallel truth graph. No re-ownership. General application software, cloud / backend software and IoT networking /
platform behaviour are not owned by this owner. The existing Software pack is unchanged and is not this owner. The
time / frequency unit fact stays one shared fact, mapped to this owner, never duplicated.

## §6. Source binding (narrowed basis only)

**DOE-HDBK-1013/2-92 — DOE Fundamentals Handbook, Instrumentation and Control, Volume 2 of 2** — Module IC-07
*Principles of Control Systems*: the section of that name (control-system terminology, input, output, open and closed
loop, feedback) and the *Control Loop Diagrams* section.

- Bound ONLY to: control-loop fundamentals; open vs closed loop; feedback; reference / comparison; controlled element /
  manipulated variable relationship (and the disturbance concept, family 6, where that section supports it).
- Treatment: archived DOE handbook — fundamentals / historical reference only (the same treatment as
  `electronics_electrical:PR004`, DOE-HDBK-1011/1-92); paraphrase only; no figures or tables; DOE attribution and a
  source-use record required; contractor-material caution (contributed or licensed material may remain protected).
- Not bound: the control-mode sections (two-position, proportional, reset, rate, PID), controllers, valve actuators
  and every detector section.

**NASA TM-101739 — *Digital Signal Conditioning for Flight Test*** — NASA Technical Memorandum by Glenn A. Bever, NASA
Ames Research Center (Dryden Flight Research Facility); NTRS copyright metadata `Work of the US Gov. Public Use
Permitted`.

- Bound ONLY to: observation / sampling at discrete times; loss of information when the observation rate is too low
  for the changing signal.
- NOT bound: controller action rate; real-time scheduling; filtering; aliasing (§3.5.3); encoding / transmission.
- Treatment: paraphrase only; no figures; NASA neutral acknowledgement with no implied endorsement; source-use record
  required.

**NIST SP 811 — Guide for the Use of the International System of Units (SI)**

- Bound ONLY to: the time unit; the frequency unit; unit discipline.
- Shared knowledge: it is already a bound source for Electronics and Mechanical unit facts
  (`electronics_electrical:PR005`, `mechanical:PR009`); this owner maps the same fact and creates no duplicate
  technical ownership.
- Treatment: NIST Technical Series reuse basis; NIST acknowledgement and a source-use record required.

**InventorAI governance records** carry family 9 only (precedent: `mechanical:PR002`–`PR005`, `governance_record`).

No other source is bound. Protected standards, vendor documentation, NonCommercial-licensed texts and sources whose
reuse basis is unconfirmed are not part of this basis.

## §7. Source-use records — contract requirement only

Future qualification / implementation requires source-use records for **DOE**, **NASA** and **NIST**, following the
existing precedent of a technical source paired with an explicit source-use-policy record
(`electronics_electrical:PR004` ↔ `PR006`, `PR005` ↔ `PR007`; `mechanical:PR006`–`PR009` ↔ `PR010`–`PR011`). No
existing precedent requires those records at contract time — the Mechanical and Electrical records arrived with
their bounded implementation slices — so none is created here. `domains/domain_provenance.json` is unchanged. The
Domain Registry refuses a pack with no provenance record (`engine/domain_registry.py`, `load_registry`), so source
records and any future pack arrive together, in a separately authorized slice.

## §8. Domain family / placement

`INDEPENDENT PEER APPEARS CLEANEST` — architecture direction only:

- **Software is in the wrong semantic class:** ADR-002 §5 gives Software computational feasibility in place of
  PHYSICAL_FEASIBILITY, and ADR-002 §8 forbids reusing a gap identifier across domain classes with different
  meanings.
- **Software child placement is not currently valid:** the Software pack declares no `domain_family_role`, so it is
  treated as standalone, and a standalone pack may not authorize child domains
  (`docs/governance/DOMAIN_PACK_GOVERNANCE_STANDARD_v1.md`, Domain Family Role Fields).
- **Electronics child placement would introduce a new inheritance-schema decision** — the child representation "will
  be defined when the first child-domain pack is authorized" — and would blur Electronics' explicit firmware
  exclusion.
- **An independent peer preserves one owner per truth.**

No family metadata is created; no existing pack is modified.

## §9. Composition boundary

The owner is recorded as **eligible in the future** to be an OPTIONAL third composable part of an integrated
invention. This contract does NOT authorize that composition change.
`COMPOSITION_DOMAINS = ("mechanical", "electronics_electrical")` is preserved until a separate Owner-authorized
Stage-15 composition slice changes it. No generic N-domain composition, no analysis-focus switching and no
relationship graph is introduced or implied.

## §10. Qualification and activation boundary

**QUALIFIED ≠ ACTIVATED.**

Before the owner may be declared qualified, a separately authorized qualification step must provide at least:

1. page-level binding of every §3 family to the exact source pages / sections;
2. the three source-use records of §7;
3. a coverage declaration and a capability declaration that carry §3 and §4 without widening either;
4. a classification / signal conflict review against Electronics (for example `microcontroller`, `controls`,
   `calculates`, `samples`, `threshold`, `filter`) and Mechanical (`actuator`) under the existing tie policy, with no
   classifier redesign;
5. cross-domain boundary tests and Electronics / Mechanical non-degradation evidence (P9-QS §6 and §7-B);
6. a truthful public label and localization;
7. the qualification evidence package required by P9-QS §7.

Any future activation additionally requires:

- separate Owner authorization;
- Stage 30 safeguards (`STAGE 30 REQUIRED BEFORE ACTIVATION`);
- qualification evidence;
- source / provenance completion;
- classification / signal conflict review;
- an exact activation decision (activation stays the existing explicit allowlist in `engine/domain_activation.py`).

Nothing is activated here.

## §11. Robotics boundary

This owner exists because of a distinct, unowned control-loop truth seam. **It is NOT a Robotics Domain Pack and does
NOT own Robotics as a whole.** Robotics, IoT and Drone / Unmanned may later compose it only if separately authorized;
none of those consumers is implemented, designed or authorized here.

## §12. Change surface of this gate and stop conditions

This gate adds this document and one registration row in the live section of
`docs/governance/ACTIVE_INCREMENT_CONTRACT.md`. It changes no runtime code, test, Domain Pack, registry, activation
allowlist, composition, classifier, question, schema, persistence or provenance record.

Writing or applying this contract stops, and the exact dependency is returned instead, if it would require: a new
domain schema; pack creation; classifier changes; family inheritance changes; runtime composition changes; Stage-30
implementation; source ingestion; or provenance mutation.
