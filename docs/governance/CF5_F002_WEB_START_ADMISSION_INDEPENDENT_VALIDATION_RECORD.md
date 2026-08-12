# CF5-F002 — Web `/start` Electronics-Only Admission — Independent Validation Record (Candidate)

**Status of THIS record:** governance/documentation-only **INDEPENDENT VALIDATION CANDIDATE** for CF-5 finding **CF5-F002**,
produced under the CF-5 Audit contract §7 (independent validation of C/D/E findings, validation separated from remediation).
**VALIDATION ONLY.** It authorizes **no** remediation, no corrective implementation contract, no runtime/Web/CLI/test change, no
domain selection/registration/activation, no CF-6 execution, no CF-2 execution, and no D4/D8 work. It becomes authoritative only
if this exact candidate passes the Mandatory Grill and the subsequent separately governed steps (independent external
exact-candidate review → Owner acceptance → SHA-preserving publication → PR → merge → post-merge verification). **Until then it
authorizes nothing.** Expected engine / web / CLI / domains / Registry / activation / schemas / persistence / API / guardrail /
test / `OWNER_DECISION_REGISTER.md` diff: **ZERO**.

**Authoritative base:** `e5f7d42c5a2c7ff6590816a87cd9f5ca3f650da0` (PR #451 — CF5-F003 formal-closure merge; freshly fetched;
0 newer commits on `origin/feature/atomic-json-session-persistence`), verified read-only before validation; boot OK;
`activated_domains() == ['electronics_electrical']`.

**Subordinate to** CLAUDE.md, the committed governance anchors, and the authoritative CF-5 Audit contract
(`docs/governance/CF5_RETROSPECTIVE_ADVERSARIAL_ARCHITECTURE_AUDIT_CONTRACT.md`, merged PR #447).

---

## §1. Authoritative defect statement (validated)

The Web `/start` admission surface (`web/app.py`) hardcodes a **single-activated-domain (electronics/electrical-only) admission
architecture** that does not consume the canonical activation set as a *set*. Its admission decision, consent contract,
conflict policy, rejection vocabulary, and public copy all assume `activated_domains() == ['electronics_electrical']`:

1. **Consent/admission constant** — `DOMAIN_CONFIRM_VALUE = "electronics_electrical"` (`web/app.py:837`) is the only
   representable user consent, and every admitted session is assigned
   `state.domain = _admit_specialist_domain(DOMAIN_CONFIRM_VALUE)` (`web/app.py:1420`): the admitted domain is a hardcoded
   constant, not the classified/consented domain.
2. **Hardcoded admission branch** — `if domain != "electronics_electrical":` (`web/app.py:1391`) plus the hardcoded
   `CONFLICTING_SUPPORTED_DOMAINS = {"mechanical", "medical_device", "software"}` (`web/app.py:845`) treat every
   non-electronics classification as a conflict/rejection regardless of activation state.
3. **Strong-unsupported vocabulary** — `_STRONG_UNSUPPORTED_WORDS` / `_STRONG_UNSUPPORTED_SUBSTRINGS`
   (`web/app.py:897-919`) encode signals of registered domains (mechanical/medical/software and non-registered families) as
   permanently "unsupported", independent of activation (the CF-6 / NB-4 concern).
4. **Public copy** — `UNSUPPORTED_DOMAIN_MESSAGE` / `MECHANISM_GUIDANCE_MESSAGE` (`web/app.py:826-829, 954-959`) state
   "InventorAI currently supports electronics and electrical ideas only", which is truthful **only while** electronics is the
   sole activated domain (the CF-2 concern).

`_admit_specialist_domain` itself (`web/app.py:853-868`) correctly binds admission to the canonical §5-I2 engine activation
policy and holds no competing activation decision; the defect is that **every caller passes the hardcoded electronics constant**,
so the binding can only ever admit electronics (and fails loud — unhandled `DomainNotActivatedError` → HTTP 500 — if
`electronics_electrical` were ever absent from the activation set; probe P-EDGE below).

**Category:** inherited **architectural debt producing a latent defect** — no present user-facing defect; becomes a present,
user-facing admission/truthfulness defect at its trigger (§5).

## §2. Exact runtime surfaces (tree `e5f7d42c`)

- `web/app.py:826-829` (`UNSUPPORTED_DOMAIN_MESSAGE`), `:837` (`DOMAIN_CONFIRM_VALUE`), `:845`
  (`CONFLICTING_SUPPORTED_DOMAINS`), `:853-868` (`_admit_specialist_domain`), `:897-919` (strong-unsupported vocabulary),
  `:933-940` (`_LAY_ELECTRICAL_WORDS`), `:1349-1458` (`/start` route; classifier dispatch `:1364-1375`; strong-unsupported
  gate `:1385-1390`; hardcoded admission branch `:1391-1409`; hardcoded admission `:1420`).
- Consumed (correct; NOT part of the defect): `engine/domain_rules.py::classify_domain` (`:190-242`, canonical classifier,
  P9-E2 tie policy, CF5-F003 whole-token matching) and `engine/domain_activation.py` (`:39` allowlist; §5-I2 policy).

## §3. Real `/start` path reconstruction (mechanically traced, this tree)

POST `/start` → (1) empty idea → redirect `/`; (2) `domain_confirm != DOMAIN_CONFIRM_VALUE` → `CONFIRMATION_REQUIRED_MESSAGE`,
no session; (3) `classify_domain(idea_text)` — `AMBIGUOUS_TIE` → fail-closed `UNSUPPORTED_DOMAIN_MESSAGE` (200, no session);
`MULTI_DOMAIN_NEEDS_D4` → same fail-closed branch (never produced by `classify_domain`; verified `kind=MULTI_DOMAIN_NEEDS_D4`
is constructed nowhere in `engine/domain_rules.py`); (4) `SINGLE` → selected domain, `NONE` → `None`;
(5) `_has_strong_unsupported_evidence` → `UNSUPPORTED_DOMAIN_MESSAGE`, no session; (6) `domain != "electronics_electrical"`:
conflicting supported domain without sufficient lay-electrical corroboration (≥2 for `medical_device`, ≥1 otherwise) →
`MECHANISM_GUIDANCE_MESSAGE`, no session; other non-None domain → `UNSUPPORTED_DOMAIN_MESSAGE`; `None` → fallback admission;
(7) admit: `state.domain = _admit_specialist_domain(DOMAIN_CONFIRM_VALUE)` — always `electronics_electrical` — then durable
project creation + `SESSION_STORE` entry + 302 redirect. **Recognition** (registry), **activation** (§5-I2 allowlist),
**classification** (`classify_domain`), **admission** (`/start` branches + `_admit_specialist_domain`), and **public
messaging** (message constants) are distinct layers; only the admission and messaging layers carry the F002 hardcoding.

## §4. Validation probes (real production `/start` via Flask test client; pinned Flask 3.1.3; isolated scratchpad
`INVENTORAI_DB_PATH`; bounded self-restoring activation doubles patching `engine.domain_activation._ACTIVATED_DOMAINS`
in-process only — the same mechanism as the committed P9-E2 test suite; NO repository state changed; NO real activation change)

- **P-A (activated electronics).** `a circuit with a sensor and battery` → `SINGLE(electronics_electrical)`; `/start` +confirm
  → **302 admitted**, `state.domain == 'electronics_electrical'`; without confirm → 200 `CONFIRMATION_REQUIRED`, no session.
  Current behavior correct.
- **P-B (NONE).** `a better way to organize my bookshelf at home` → `NONE`; strong-unsupported False; `/start` +confirm →
  **302 admitted as electronics** (governed None-fallback under explicit confirmation — Domain Gate contract behavior).
  No message shown; nothing untruthful (the user affirmatively declared electronics; ADR-001 explicit consent).
- **P-C (ambiguous tie, real activation).** `circuit and hinge` → `SINGLE(electronics_electrical)` (D3-D: sole activated
  domain in the tie outranks recognized-not-activated) → admitted. **A real `AMBIGUOUS_TIE` is production-unreachable today**
  (requires ≥2 activated tied domains). Under an elec+mech double the same input → `AMBIGUOUS_TIE(electronics_electrical,
  mechanical)` → `/start` **200 UNSUPPORTED, no session** (P9-E2 fail-closed branch works; ordered before the
  strong-unsupported gate).
- **P-D (recognized-but-not-activated).** `a hinge` → classifier `SINGLE(mechanical)` (priority fallback);
  `is_activated('mechanical') == False`; `/start` +confirm → 200 `MECHANISM_GUIDANCE_MESSAGE`, no session. `a gear` /
  `a catheter` (strong words) → 200 `UNSUPPORTED_DOMAIN_MESSAGE`, no session. Messages truthful **today** (electronics-only
  support is a fact). Admission correctly refuses specialist runtime for non-activated domains.
- **P-E (second-domain hypothetical; elec+mech double; self-restoring; no commit).** The hardcoded electronics admission
  becomes incorrect in four mechanically demonstrated ways:
  1. `a hinge` (classifier `SINGLE(mechanical)`, mechanical **ACTIVATED** under the double) → still 200 GUIDANCE claiming
     "supports electronics and electrical ideas only" — **activation state has ZERO effect on the admission outcome**
     (byte-identical to P-D) and the message becomes untruthful.
  2. `a gearbox for a bicycle` → 200 UNSUPPORTED via the static strong-unsupported vocabulary even though mechanical is
     activated — an activated domain's own signals remain permanently "unsupported" (CF-6 / NB-4 collision, confirmed).
  3. `a hinge that you plug in` → classifier `SINGLE(mechanical)` (an ACTIVATED domain), yet `/start` **ADMITS it as an
     `electronics_electrical` specialist session** (weak-conflict lay-word resolution + hardcoded
     `_admit_specialist_domain(DOMAIN_CONFIRM_VALUE)`) — a genuine cross-domain session mislabeling, the sharpest form of
     the defect. (Under today's real activation the same input is also admitted as electronics, but that is the governed
     Domain Gate §7.C weak-conflict resolution toward the only activated, explicitly confirmed domain — not a defect today.)
  4. No consent path exists for the second domain at all: `DOMAIN_CONFIRM_VALUE` is the only representable confirmation, so
     an activated non-electronics domain can never be admitted truthfully whatever the input.
  Real activation verified restored (`['electronics_electrical']`) after every probe.
- **P-F (3+/D4).** Triple double (elec+mech+sw): `circuit and hinge and app` → `AMBIGUOUS_TIE` with the complete 3-way
  candidate set → `/start` 200 UNSUPPORTED fail-closed. `MULTI_DOMAIN_NEEDS_D4` is constructed nowhere in
  `engine/domain_rules.py` (verified); the `/start` branch for it (`web/app.py:1371-1375`) is dormant, fail-closed. D4 NOT
  executed; no unsupported behavior invented.
- **P-G (UI-language independence).** `/start` (`web/app.py:1349-1458`) contains no `ui_lang` read; probes with
  `ui_lang=ar` produced byte-identical admission outcomes (electronics idea → 302 admitted electronics; `a hinge` → 200
  GUIDANCE). Classification is a pure function of idea text. **PASS.**
- **P-EDGE (activation set without electronics; double `{'mechanical'}`).** `/start` on a valid electronics idea → unhandled
  `DomainNotActivatedError` → **HTTP 500, no session, no durable write** (the exception fires at `web/app.py:1420` before
  `create_project`). Fail-loud, not silent misadmission — but ungraceful; recorded as trigger-analysis evidence only.
- **P-H (session cleanup).** All probes ran in throwaway processes with `INVENTORAI_DB_PATH` pointed at session-scratchpad
  files (deleted afterward); `SESSION_STORE` is in-process memory discarded at exit; the repository tree is clean
  (`git status` empty of runtime changes); real `_ACTIVATED_DOMAINS` untouched. **PASS — no persistent session-state
  pollution.**

## §5. Present reachability & trigger (validated)

**Present reachability: NO PRESENT USER-FACING DEFECT — trigger-deferred.** Under the authoritative activation
`['electronics_electrical']`, every `/start` outcome probed is correct and every public message truthful; the electronics-only
admission hardcoding is *extensionally equivalent* to the canonical activation policy today. Nothing in the F002 surfaces
misbehaves for any reachable input.

**Exact trigger (narrowed; the historical wording is challenged and refined).** The historical trigger statement
"second-specialist-domain activation" is extensionally correct under the current state but is not the mechanically narrowest
event. The defect manifests at **the first moment the canonical activation set differs from `['electronics_electrical']`**:

- **adding** any non-electronics activated domain (under the current state this IS the second-specialist-domain activation)
  makes the admission surface wrong in the four P-E ways; and
- **removing** `electronics_electrical` (not a governed plan; evidence only) makes `/start` fail loud with HTTP 500 (P-EDGE).

**NOT the trigger (mechanically excluded):** second-domain *registration* (mechanical/medical_device/software are already
registered today — probes P-D show correct refusal); classifier *recognition* (already occurs today, no defect); Web admission
*configuration* (no such configuration exists — the values are hardcoded constants). Registration and recognition change
nothing at `/start` because admission consults only the activation policy and the hardcoded constants.

## §6. Validated classification

**C — Material latent issue, NOT currently reachable** (classification RETAINED on evidence, not inherited). The probes prove
both halves of the C definition: (a) no reachable defect under current Electronics-only operation (P-A…P-D, P-G — every
outcome correct and truthful today); (b) a mandatory pre-trigger prerequisite — the same surfaces mechanically produce wrong
admission (session mislabeling), wrong refusal (activated-domain signals refused as "unsupported"), and untruthful public copy
the moment a non-electronics domain is activated (P-E). Not **B** (this is not optional hardening; the trigger converts it
into a user-facing correctness/truthfulness defect). Not **D** (no reachable defect today). Not **E** (no architectural
contradiction: the canonical classifier, activation policy, and §5-I2 binding are sound and layered correctly; the Web
admission layer simply has not been generalized — a bounded, well-understood correction whose direction existing governance
already anticipates via CF-6/CF-2/CF-3). The finding is neither obsolete nor governance-misworded, except the trigger
narrowing recorded in §5.

## §7. CF-6 relationship

**Partly owned by CF-6; same trigger; same runtime surface; NOT a duplicate framework; neither obsoletes the other.** CF-6
(registered by the P9-E2 gate) governs the Web pre-classifier / strong-unsupported reachability interaction: which signals are
intercepted before `classify_domain`, Web/CLI consistency, truthful fail-closed behavior, no hidden Electronics admission, no
`AMBIGUOUS_TIE` bypass, and unsupported-copy truthfulness. That covers F002 facets 3 (strong-unsupported vocabulary, P-E.2)
and the hidden-electronics-admission facet (P-E.3). F002 is **broader on the admission architecture itself**: the hardcoded
consent constant, the `domain != "electronics_electrical"` branch, `CONFLICTING_SUPPORTED_DOMAINS`, and the constant-valued
`_admit_specialist_domain(DOMAIN_CONFIRM_VALUE)` call (facets 1, 2, 4 / P-E.1, P-E.4) are outside CF-6's stated pre-classifier
scope. The existing roadmap treatment ("the CF5-F002 / CF-6 Web-admission lane") is validated as correct: one future bounded
Web-admission gate at the shared trigger can disposition both without creating any new framework; CF-5 completion must not
auto-declare CF-6 executed (audit contract §13 preserved).

## §8. CF-2 relationship

**Separate; co-triggered; NOT absorbed.** No public-message defect is reachable today: every message probed is truthful under
Electronics-only activation (P-A…P-D), and the `AMBIGUOUS_TIE`/`MULTI` fail-closed copy is production-unreachable. At the F002
trigger, the shared `UNSUPPORTED_DOMAIN_MESSAGE` / `MECHANISM_GUIDANCE_MESSAGE` copy ("supports electronics and electrical
ideas only") becomes untruthful for activated non-electronics domains and for future real ties (P-E.1/P-E.2). That messaging
facet belongs to **CF-2** (public-message truthfulness) with the same trigger as F002; it is recorded here as a relationship,
not absorbed into F002, and no CF-2 work is performed or authorized by this record.

## §9. Stale `SUBSTRINGS` comment — validated disposition (NOT edited here)

- **Location:** `web/app.py:870-884` — the Domain Gate / Entry UX comment block in the `/start` admission code (the block
  immediately after `_admit_specialist_domain`, before `_TOKEN_RE`; the F003 closure record's label
  "`web/app.py::_admit_specialist_domain`" denotes this same block).
- **Staleness (verified mechanically):** the claim "`infer_domain()` matches classification signals as SUBSTRINGS"
  (`:873`) and the example "'app' is a substring of 'appliance' (-> software)" (`:876-877`) are FALSE after CF5-F003
  (whole-token matching; `a smart appliance` → `NONE` verified on this tree). The same block's "'monitoring' ->
  medical_device" example remains TRUE (`monitoring` is a registered medical signal, whole-token matched — verified). The
  comment is therefore **partly stale historical rationale**, purely comment/documentation hygiene.
- **Runtime consequence:** ZERO (comment only; the code it annotates is token-based and unchanged).
- **Canonical owner:** **CF5-F002 / CF-6 Web-admission lane** — CONFIRMED (it annotates the exact admission code F002/CF-6
  govern); earliest correction gate: the future F002/CF-6 Web-admission gate or a bounded doc-hygiene pass, per the F003
  closure record. **Not edited in this validation gate.**
- **Additional comment-hygiene observation (same lane; evidence only; NOT a new finding):** `web/app.py:1361-1363` still
  says "classify_domain() today yields only SINGLE / NONE … richer kinds are dormant until the later, separate P9-E2
  tie-precedence runtime produces them" — stale since the P9-E2 implementation (PR #445): `classify_domain` DOES produce
  `AMBIGUOUS_TIE` (production-unreachable under single activation). Zero runtime consequence; same canonical owner.

## §10. Effect of CF5-F003 remediation on F002 consequences

F003 (whole-token matching) changed which raw inputs reach which `/start` branch (e.g. `appliance` no longer manufactures a
software conflict; `controlled` no longer scores `led`), eliminating the F003 bypass/admission class — but it changed
**nothing** in the F002 admission architecture: all four hardcoded facets and their post-trigger consequences are identical
before and after F003. F003's only F002-lane effect is rendering the §9 comment stale.

## §11. What remains unknown

- The correct future multi-domain consent/admission UX (which domains a user may confirm; how `/start` should offer them) —
  an Owner product decision, required only pre-trigger (§12).
- Whether the future gate resolves the strong-unsupported vocabulary by activation-awareness, removal, or replacement —
  CF-6 design space; deliberately not prescribed here (validation defines the defect boundary only).
- Exact interaction with a future D4 multi-domain composition surface (D4 remains separate and unexecuted).

## §12. Disposition

- **Corrective remediation required NOW: NO** (no reachable defect; remediating now would also be unauthorized scope).
- **Pre-trigger corrective gate required: YES (binding).** Per audit-contract §8 policy for C, a bounded corrective
  prerequisite in the CF5-F002 / CF-6 Web-admission lane MUST close **before any activation gate makes
  `activated_domains() != ['electronics_electrical']`**. First new-domain activation remains BLOCKED behind it (among the
  other governed prerequisites).
- **Owner policy required before remediation: YES, at the future gate, none now** — the multi-domain consent/admission UX
  decision (§11) must exist before or within the corrective contract; this validation raises no Owner decision today and
  changes `OWNER_DECISION_REGISTER.md` in no way.

## §13. Preserved statuses and non-effects (exactly)

CF5-F002 = **OPEN C — INDEPENDENTLY VALIDATED (this candidate)**; CF5-F003 = **CLOSED**; CF5-F001 = **OPEN C**;
CF5-F004 = **OPEN C**; CF-5 = **OPEN**; CF-6 / CF-2 / CF-3 = **PENDING, separate, trigger-bound**; D4 SEPARATE / UNEXECUTED;
D8 Owner-reserved; `activated_domains() == ['electronics_electrical']`; NO domain selected/registered/activated; **first
new-domain activation remains BLOCKED**; Phase 10 NOT AUTHORIZED; PSRR NOT EXECUTED; deployment/production NOT AUTHORIZED.
This record does not reopen Gate C, run E-2, create a SID, modify preserved evidence, move any hold, or classify S-6.

## §14. Scope of this candidate

Governance/documentation only: this NEW record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. **ZERO** runtime / test / Web / CLI / domain /
Registry / activation / schema / persistence / API / guardrail / `OWNER_DECISION_REGISTER.md` diff. Next required gate:
**Mandatory Grill on this exact candidate**; any material finding rejects it as-is (fresh candidate from the authoritative
parent — no in-place amendment).
