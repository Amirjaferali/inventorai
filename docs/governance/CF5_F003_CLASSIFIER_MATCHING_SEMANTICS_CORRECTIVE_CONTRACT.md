# CF5-F003 — Classifier Matching Semantics — Corrective Gate — Governance Contract (Corrected Candidate)

**Status of THIS record:** governance/documentation-only **CORRECTIVE CONTRACT CANDIDATE (corrected — supersedes REJECTED
`9857ba3e21a8bbd8d73bcde83cb85b7744d0f85b`)**. It becomes AUTHORITATIVE only if this exact accepted candidate is independently
reviewed (Mandatory Grill → independent external exact-candidate review), Owner-accepted, published SHA-preserving, merged
(create-a-merge-commit), and post-merge verified. **Until then it authorizes nothing.** It is the bounded corrective gate opened by
CF-5 finding **CF5-F003**, independently validated as **D — Material current issue, reachable now**. **It defines WHAT must be
corrected and the evidence the future implementation must produce; it implements NOTHING** — no runtime, no test, no behavior change
in this gate. **It does NOT solve CF5-F001, CF5-F002, or CF5-F004, does not close CF-5, and selects/qualifies/registers/activates
no domain.** **GOVERNANCE-ONLY CONTRACT GATE.** Expected engine / web / CLI / domains / schemas / persistence / API /
architecture-guardrail / test diff in THIS gate: **ZERO**.

**Provenance / why a corrected candidate.** The prior CF5-F003 corrective contract candidate
`9857ba3e21a8bbd8d73bcde83cb85b7744d0f85b` was **REJECTED by Mandatory Grill** (`GRILL FAIL — MATERIAL CORRECTION REQUIRED`),
blocking finding **BF-1**: its rule *"exact whole-token only / no plural inference; plurals matched only where the pack already
enumerates them"* would **regress ~76 single-word signals whose plural forms are currently matched via substring** (e.g. `LEDs`,
`sensors`, `circuits`, `gears`, `levers`, `catheters`, `apps`, `databases` → NONE, and `a system of gears and levers` would flip
Mechanical → Software), contradicting the contract's own preservation requirement. **BF-1 is a contract-design defect, not a new
runtime finding.** The rejected candidate is immutable rejected evidence — NOT amended, reused, or advanced. This corrected
candidate is built fresh from the authoritative tip and replaces the rejected rule with a **bounded, deterministic plural-preserving
whole-token rule** plus mandatory plural-preservation evidence.

**Authoritative base:** `8c38812086cfd3c17bc61ad47bba94e8b7a9de8d` (PR #447 — CF-5 Audit contract merge; parents `54a5565…` +
`6b59112f…`; merge tree `bf5baee9…`), verified read-only; boot OK; `activated_domains() == ['electronics_electrical']`; 0 newer;
rejected `9857ba3e` is NOT an ancestor. Subordinate to CLAUDE.md and the committed anchors. Reuse existing canonical owners.

---

## §1. Finding & validated classification (UNCHANGED — D preserved)

- **Finding CF5-F003:** the domain classifier scores signals with raw **substring** semantics (`signal in text`), so a signal
  matches inside unrelated words.
- **Independent validation verdict:** **CF5-F003 = VALIDATED D — Material current issue, reachable now.** This corrective gate is
  opened accordingly. The D classification is **not weakened or reclassified** by this correction.

## §2. Exact validated defect (reproduced under REAL `['electronics_electrical']`, tip `8c38812`)

`engine/domain_rules.py::classify_domain` counts a pack signal when `signal in idea_text.lower()`. Reproduced current-reachable
misclassifications: `a controlled release drug capsule` → `SINGLE(electronics_electrical)` (`controlled`→`led`); `a compiled
report` → electronics (`compiled`→`led`); `patriotic banner` → electronics (`patriotic`→`iot`); `concurrent tasks` → electronics
(`concurrent`→`current`); `a hearth warmer` → `SINGLE(medical_device)` (`hearth`→`heart`). **Current effects (reachable now):**
incorrect `SINGLE(...)` classification; untruthful CLI "Domain inferred / Domain confirmed"; Web `/start` mechanism-guidance bypass
/ incorrect electronics admission when the false-positive score changes the result. Hence **D, not merely latent.**

## §3. Repository plural inventory (mechanically reproduced this gate, tip `8c38812`)

Over the registered packs (`electronics_electrical`, `mechanical`, `medical_device`, `software`): **76 single-word signals; 5
multi-word signals** (`drug delivery`, `data pipeline`, `machine learning`, `ml model`, `neural network`). Of the 76 single-word
signals, **essentially all rely on substring matching to catch their common plural** (none of the four packs enumerate plurals).
Special forms found: exactly one signal ends in a sibilant (`diagnosis`) — its irregular English plural `diagnoses` is **not**
matched by the current substring rule either (`diagnosis` is not a substring of `diagnoses`), so it carries **no** preservation
obligation; `esp32` is the only numeric-bearing signal (`esp32s` is a simple `+s`); `respiratory` is the only consonant+`y` signal
(its plural is rare and not required). **No cross-pack `+s`/`+es` collision exists** (no signal's `+s`/`+es` form equals another
pack's signal). Conclusion: a bounded **`+s` / `+es`** whole-token plural rule preserves the currently-correct plural matches
without irregular-plural or cross-pack-collision hazards.

## §4. Required matching semantics (deterministic, domain-neutral, N-domain capable)

The future implementation MUST define matching per pack signal against the lowercased idea text as follows:

1. **Tokenization (§5.1).** Lowercase the text; tokenize into maximal ASCII-alphanumeric runs (`[a-z0-9]+`); punctuation and
   whitespace are delimiters (so `ESP32.`, `(LED)`, `PCB,`, `drug-delivery` tokenize to `esp32` / `led` / `pcb` / `drug` `delivery`).
2. **Exact single-word token match (§5.2).** A single-word signal `S` matches when some input **token equals `S` exactly**.
3. **Bounded plural preservation (§5.3).** A single-word signal `S` **additionally** matches when some input token equals **`S+"s"`
   or `S+"es"`** — nothing else. This is the ONLY inflection permitted. **FORBIDDEN:** arbitrary stemming, fuzzy matching, edit
   distance, semantic similarity, prefix/suffix/substring matching, `+ies`/irregular-plural inference, or any morphology beyond the
   literal `+s`/`+es` whole-token forms. The rule is exact, total, and deterministic.
4. **Collision guard (§5.4) — load-bearing.** Because matching is over **whole tokens** (never substrings), the bounded plural rule
   does NOT recreate substring behavior. The following MUST remain **false** (validated this gate): `controlled`↛`led`,
   `compiled`↛`led`, `patriotic`↛`iot`, `concurrent`↛`current`, `hearth`↛`heart` (none of these tokens equals `led`/`iot`/`current`/
   `heart` or their `+s`/`+es` forms).
5. **Multi-word / phrase signal (§5.5).** A multi-word signal matches only as a **contiguous sequence of whole tokens** equal to the
   signal's token sequence; the **`+s`/`+es` bounded plural is permitted on the FINAL token only** (e.g. `neural networks`,
   `drug deliveries` is NOT inferred — `+es` on `delivery` would be `deliverys`, not the English `deliveries`, and is not required;
   the rule applies the literal `+s`/`+es` to the last token only). No token skipping; no reordering; intermediate tokens match
   exactly.
6. **Technical-token preservation (§5.6).** Standalone and `+s` plural technical tokens MUST be recognized: `led`/`leds`,
   `pcb`/`pcbs`, `api`/`apis`, `app`/`apps`, `iot`, `web`, `sensor`/`sensors`, `circuit`/`circuits`, `resistor`/`resistors`,
   `gear`/`gears`, `lever`/`levers`, `catheter`/`catheters`, `database`/`databases`, `esp32`/`esp32s` — as defined by the actual
   registered signal inventory (§3), not an assumed list.
7. **Determinism.** A bare `\bsignal\b` regex is NOT assumed sufficient (it does not express multi-word phrase matching, digit-bearing
   tokens, or the bounded plural rule cleanly); the token/phrase definition above is authoritative and MUST be satisfied exactly.

**Acceptance boundary (explicit).** The corrective goal is to eliminate **arbitrary in-word substring matches** (the F003 false
positives, and incidentally benign compound reductions such as `subsystem`/`ecosystem`→`system`) while **preserving legitimate
singular and bounded-plural whole-token matches.** Rare legitimate prefixed/compound forms that the old substring rule caught
(e.g. `misdiagnosis`→`diagnosis`) are **NOT required** to be preserved and are out of scope for this correction (any future desire
to recognize them is a separate Domain-Pack-data decision, not this matching-semantics gate).

## §5. Required preservation properties (behavior that MUST NOT change)

Canonical ownership by `classify_domain(...)`; immutable frozen `DomainClassification` semantics/invariants; P9-E2-R legacy
fail-loud `infer_domain(...)`; P9-E2 governed tie policy (0→fallback / 1→SINGLE / ≥2→AMBIGUOUS_TIE, selected=None, canonical
candidates, EQUAL_SCORE); activated-domain precedence (D3-D); recognized-but-not-activated semantics; **all currently correct
Electronics / Mechanical / Medical Device / Software classifications, INCLUDING their common plural forms** (§4.6); Web / CLI /
core semantic parity; **no new `MULTI_DOMAIN_NEEDS_D4` producer**; D4 separation; **no activation change**; the non-activated
priority fallback list unchanged (CF5-F004 out of scope).

## §6. Required RED evidence (must demonstrate the ACTUAL defect, not only score deltas)

RED tests failing on the pre-fix parent and GREEN after the fix for at least: `controlled` → not-electronics; `compiled` →
not-electronics; one `iot` collision (`patriotic banner`) → not-electronics; `concurrent` → not-electronics; one medical-signal
collision (`hearth`→ not medical_device); a **real Web `/start` guidance-bypass / incorrect-admission reproduction** (real route,
real classifier — no injected object); and a **real CLI incorrect-domain-confirmation reproduction**. At least one RED MUST assert an
observable Web/CLI consequence (admission/confirmation), not merely a score integer.

## §7. Required GREEN preservation evidence — MANDATORY; explicitly repairs BF-1

The implementation candidate MUST include GREEN tests proving valid **plural** inputs still classify to the correct domain (from the
§3 inventory), at minimum: **Electronics** — `LEDs`, `sensors`, `circuits`, `resistors`, `PCBs`; **Mechanical** — `gears`, `levers`,
plus another real pack plural; **Medical Device** — `catheters`, plus another real pack plural; **Software** — `apps`, `databases`,
`APIs`. Plus preservation of: singular forms; punctuation-adjacent technical tokens (`ESP32.`, `PCB,`); valid multi-word signals;
existing Electronics / Mechanical / Medical Device / Software recognition; 0/1/2/3+ activated-domain classifier scenarios (via
self-restoring `_ACTIVATED_DOMAINS` doubles); AMBIGUOUS_TIE semantics; recognized-not-activated behavior; Web/core parity;
CLI/core parity. **Mandatory regression case:** `a system of gears and levers` MUST classify **Mechanical** and MUST NOT flip to
Software.

## §8. Required mutation / adversarial evidence (each probe CAUGHT RED, bytes restored, bytecode-isolated)

Probes that MUST fail if: (a) raw substring matching is restored; (b) whole-token anchoring is removed; (c) **bounded plural
preservation is removed** (a valid plural stops matching); (d) the **plural rule is made over-broad** (e.g. reintroducing substring
or adding unbounded morphology so a false positive like `controlled`→`led` returns); (e) punctuation handling regresses; (f) a valid
short technical token (`led`/`iot`/`api`/`app`/`pcb`/`web`) becomes unrecognizable; (g) Web or CLI bypasses the canonical classifier
semantics.

## §9. Scope restraint (binding)

Expected implementation scope: the classifier matching logic in `engine/domain_rules.py` (the scoring comprehension only) + focused
classifier tests + focused Web/CLI regression tests **only if required** to hold §6. **Forbidden in this corrective line:** broad
Web admission redesign (CF5-F002/CF-6); safety-signal redesign (CF5-F001); fallback-priority redesign (CF5-F004); domain
activation/selection/registration; D4; D8; MULTI production; persistence changes; unrelated public-copy changes. **Domain-Pack
signal-data edits remain FORBIDDEN** unless repository evidence proves a minimal pack-data correction is absolutely required (the §3
inventory shows the bounded `+s`/`+es` matcher preserves current behavior **without** pack-data edits, so none is expected). If a
production file beyond `engine/domain_rules.py` becomes mechanically required, the implementation gate STOPs before expanding scope.

## §10. Canonical ownership

`classify_domain(...)` remains the **sole canonical domain-classifier owner**; Web and CLI remain **consumers** that dispatch by
`result.kind`. The tokenization/matching logic MUST live once inside the canonical classifier; **no duplicate matching logic may be
introduced into Web or CLI.**

## §11. Governance disposition

- **CF5-F003 = VALIDATED D; corrective gate OPEN** (this corrected contract).
- **Previous candidate `9857ba3e` = REJECTED BY MANDATORY GRILL (BF-1)** — immutable rejected evidence; not reused; retained in
  history (not erased).
- **BF-1 = contract-design defect, not a new runtime finding.**
- Affected classifier-dependent work remains BLOCKED until the corrective implementation is merged and post-merge verified.
- **First new-domain activation remains BLOCKED.**
- This gate **does NOT discharge CF5-F001 / CF5-F002 / CF5-F004** (each remains an open C finding) and **does NOT close CF-5**.
- `OWNER_DECISION_REGISTER.md` **UNCHANGED** — a bounded technical plural-preservation matching rule is within existing architecture
  and records no new accepted Owner product-policy decision (D3 / P9-QS / P9-E1 / CF-5 candidate precedent).

## §12. Required downstream gate discipline (future implementation candidate)

Mandatory Grill → Independent External exact-candidate Review → Owner exact-candidate acceptance → SHA-preserving publication → PR →
pre-merge verification → **CREATE A MERGE COMMIT ONLY** → post-merge verification. Built directly from the then-current authoritative
tip; RED-first; bytecode-isolated mutation probes; full governed suite green (current baseline 2307 passed / 3 skipped / 1 xfailed)
plus the new focused tests, with the exact delta explained.

## §13. Governance scope of THIS contract candidate

Governance/documentation only: this NEW corrected contract record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. **`OWNER_DECISION_REGISTER.md` UNCHANGED.** ZERO
runtime / engine / test / domain / schema / persistence / API / web / CLI / architecture-guardrail diff.

## §14. Candidate state & next gate

**CF5-F003 corrected corrective contract = CANDIDATE ONLY; IMPLEMENTATION NOT STARTED.** It does not claim the fix is implemented or
that CF5-F003 is corrected. It becomes the authoritative corrective contract-of-record only after Mandatory Grill → independent
external exact-candidate review → Owner exact-candidate acceptance → SHA-preserving publication → PR → pre-merge verification →
CREATE A MERGE COMMIT → post-merge verification. **Next required gate: MANDATORY GRILL OF THIS EXACT CORRECTED CF5-F003 CONTRACT
CANDIDATE.** CF-5 remains OPEN; CF5-F001 / CF5-F002 / CF5-F004 remain open C findings; no domain activated or selected; first
new-domain activation remains BLOCKED.
