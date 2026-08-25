# InventorAI — Deferred Obligations Register (permanent, cross-cutting)

STATUS AT CREATION: `REGISTER CANDIDATE — NOT AUTHORITATIVE UNTIL MERGED AND
POST-MERGE VERIFIED.` Created under the Owner's permanent rule at the
post-W2-ID bounded status-sync + register write gate, seeded from the
repository-verified retrospective reconstruction (read-only gate, base
`516a184231f3e19fad6e8f6f3301b5b9c4ad9820`).

CURRENT STATUS: `AUTHORITATIVE` — merged via PR #566 (merge
`557548db2bb37b21b6b57f893afc2ae1af64744f`), post-merge verified.
Maintained through authoritative gates only; latest maintenance gate:
the post-Cross-Layer-Standard synchronization (base
`216cdc8e61eea141940de072105aa03a4cd801bb`, PR #571 — the authoritative
Cross-Layer Execution Assurance Standard merge). Rows touched at a
maintenance gate carry that gate as their last authoritative review
point; all other rows keep the seeding review point below.

## 1. Governance contract

**Owner permanent rule (binding, retrospective and prospective).** A
permanent Deferred Obligations Register must remain part of the InventorAI
Master Checklist and governance system. No project closure, serious release,
paid activation, production release, or applicable downstream release gate
may be approved until every material item in this register has been
re-examined and carries exactly one current disposition.

**Role.** `ROUTE + CURRENT OBLIGATION STATUS + RETURN GATE + CLOSURE
EVIDENCE`. This register is the canonical CROSS-CUTTING per-item status
ledger for deferred/open obligations. It is NOT a second roadmap, NOT a
second Owner Decision Register, NOT a second workstream status table, and
never replaces a source-owner document: the source owner remains
authoritative for the underlying capability/decision; this register owns
only the obligation's current disposition, return gate, and closure
evidence. It is routed from the Master Obligation Index
(`CURRENT_PROJECT_STATE.md`), which remains pointer-only.

**Scope.** Material obligations that are deferred; open; not authorized yet;
conditional; dormant-but-later-gated; Owner-decision-required; later
release-blocking; later paid-activation-blocking; or material residual
observations requiring revisit.
**Exclusions.** Cosmetic observations; speculative future features without
repository authority; already-closed items (beyond the retrospective rows in
§7 needed to prove obligation lineage); rejected candidates once their
supersession relation is recorded.

**Required fields per item.** (1) existing identifier if authoritative —
never fabricated for tidiness; (2) name; (3) source owner; (4) origin
file+section; (5) original classification; (6) current disposition; (7)
dependency/return trigger; (8) latest safe gate; (9) blocking level; (10)
closure evidence required; (11) replacement/supersession target where
relevant; (12) last authoritative review point.

**Disposition vocabulary (exact, exhaustive — one per item):**
`CLOSED — evidence verified` · `SUPERSEDED — replacement identified` ·
`RETIRED — explicitly no longer required` · `OPEN — return at defined gate`
· `BLOCKING — cannot pass next applicable gate`.
Additional metadata (`NOT AUTHORIZED YET`, `DORMANT`, `CONDITIONAL`, `FRB`,
`PAB`, `NBF`) refines but never replaces the five dispositions.

**Blocking levels for OPEN/BLOCKING items:** `CURRENT EXECUTION BLOCKER` ·
`FUTURE SERIOUS-RELEASE BLOCKER` (FRB) · `PAID-ACTIVATION BLOCKER` (PAB) ·
`CONDITIONAL` · `NON-BLOCKING FUTURE` (NBF).

**Release-closure rules (permanent).** Before approving SERIOUS RELEASE:
every `CURRENT EXECUTION BLOCKER` must already be closed; every applicable
`FUTURE SERIOUS-RELEASE BLOCKER` must be CLOSED, SUPERSEDED, or RETIRED
with evidence; every CONDITIONAL item whose trigger has become true must be
adjudicated. Before approving PAID ACTIVATION: the same, plus every
applicable `PAID-ACTIVATION BLOCKER`. `NON-BLOCKING FUTURE` never blocks
merely by existing, and nothing here requires every strategic idea to be
implemented.

**Maintenance rules.** At every major future gate: read this register;
check triggered obligations; check latest-safe-gate violations; update only
through authoritative governance (candidate → review → Owner acceptance →
merge); preserve history; NEVER delete an obligation to make a gate pass.
On closure record: evidence; authoritative SHA/PR/gate; a date only where
repository authority supports it; the replacement if superseded.

Evidence tags: `[REPO]` file/section, `[EXEC]` executed probe at the stated
base, `[OWNER]` Owner decision/authority, `[OPEN]` undecided.
Last full authoritative review point for every seeded row: the post-W2-ID
read-only reconstruction at base `516a1842…` (this gate).

## 2. Before W2-A / current execution

| Item | Source owner | Origin | Disposition | Return trigger | Latest safe gate | Blocking | Closure evidence required |
|---|---|---|---|---|---|---|---|
| W2-A enactment set — exact decision-action disposition vocabulary; explicit context-attachment representation (incl. any exact bounded `AssertionRecord` field proposal); RVR-4 implementation-contract freeze. Carrier ARCHITECTURE itself is NOT open — decided by `OD-W2ID-LEDGER — APPROVED` `[OWNER]`. **CONTRACT DETAILS NOW FROZEN** via the authoritative W2-A contract (PR #567, merge `82758cb2…`, accepted candidate `b778cfe7…`): V2 vocabulary; `decision_context_root`; bounded legacy load rule; fail-closed carrier mint; `OWNER_STATED` provenance; OW-6 containment incl. the corrected requirement-landscape truth; frozen allowlist + RED inventory. This row's original closure-evidence wording ("authorization + frozen contract, merged") is SUPERSEDED by the later authoritative contract's own §21 transition plan, which keeps the enactment set OPEN until implementation | Owner (frozen W2-A contract) + RVR-4 contract | W2-ID v3 record §B/§C (PR #565); W2-A contract §21 (PR #567) | **CLOSED — evidence verified.** Closure criterion (§21, quoted): "may become CLOSED only with exact implementation + RED→GREEN evidence" after "a future accepted W2-A implementation merge". Satisfied entirely by PRIOR external evidence: exact Owner-accepted implementation candidate `d8c5aef988a00a8b342b26816afd6186e4262c42` (after Grill-failed `b3ada80…` and externally reviewed N-2-rejected `614a0c7…`, both preserved as remote evidence branches), merged via **PR #569** (`e17ca1477e55b49298b92ac5ec8db711e208496e`; second parent = the exact candidate; merge tree `4c1739ae…` identical; empty candidate→merge diff); the full RED inventory (ID/SUP/DET/COMPAT/OW6/SEAM/PROV/LANG/CORR/REACH + IG-17 + N-2 composition tests) GREEN in the merged tree — re-executed at this gate `[EXEC — 62 passed at e17ca147…]`; candidate full suite `4595 passed / 3 skipped / 1 xfailed / 0 failed` | n/a (closed) | n/a (closed) | n/a (closed) | PR #569 merge + merged RED inventory + `[EXEC]` re-run at tip (recorded) |
| **OD-W2-DW-LIFT — exercise OD-R3's bounded DW-lane-hold lift** exactly as the Wave-2 contract §D scopes it (class reuse only; no second journey; the S2 §13 `PRESERVE UNMODIFIED AND PAUSE` hold otherwise stands). OD-R3 = ACCEPTED IN PRINCIPLE; nothing here activates broader DW Path-T work | Owner (Wave-2 authoritative contract §P item 3) | WAVE_2_BOUNDED_IMPLEMENTATION_CONTRACT_CANDIDATE.md §P item 3 `[REPO :434-436]`; register OD-R3 row (Wave-1 section) | **CLOSED — evidence verified.** Closure criterion (this row): "explicit Owner exercise/authorization of OD-W2-DW-LIFT under the authoritative W2-A lifecycle" — a governance criterion requiring NO runtime evidence. Satisfied exactly: the Owner exercise is recorded in the authoritative W2-A contract §5 (three bounded permissions — FDC-001 class reuse by the composition seam; default-preserving constructor generalization; class vocabulary reuse — with the full forbidden list and the `PRESERVE UNMODIFIED AND PAUSE` hold preserved), Owner-accepted at exact SHA `b778cfe7fd31c82c583d7d97e5f73394e6bfda65`, merged PR #567 (`82758cb2…`), post-merge verified. The contract's own §21 names this row eligible for exactly this closure. IMPLEMENTATION of the lifted permission remains separately governed by the W2-A implementation gate + frozen allowlist; broader DW Path-T remains held | n/a (closed) | n/a (closed) | n/a (closed) | W2-A contract §5 + PR #567 merge `82758cb2…` (recorded) |
| Post-W2-ID status-surface synchronization + this register's creation | this write gate (Creator under Owner authorization) | read-only reconstruction §C/§D; this candidate | **CLOSED — evidence verified.** Closure criterion: "authoritative merge of this candidate + post-merge verification". Satisfied: merged via PR #566 (merge `557548db2bb37b21b6b57f893afc2ae1af64744f`, second parent = the exact accepted sync candidate `3910e86c…`, empty candidate→merge diff), post-merge verified at the W2-A read-only gate and re-verified at the post-W2-A-contract sync (PR #566's merge is the first parent of PR #567). Never self-certified: closure recorded only AFTER the merge, at a later gate | n/a (closed) | n/a (closed) | n/a (closed) | PR #566 merge `557548db…` + post-merge verification (recorded) |
| Wave-2-era authorization lineage recording in the Owner Decision Register | `OWNER_DECISION_REGISTER.md` (L5) | read-only reconstruction §C (`AUTHORIZATION EXERCISE EVIDENCED BY AUTHORITATIVE MERGED EXECUTION; DEDICATED REGISTER ENTRY ABSENT`) | **CLOSED — evidence verified.** Closure criterion: "merged register Wave-2 section". Satisfied: the Owner Decision Register's Wave-2 section (OD-W2ID-LEDGER row + lifecycle lineage table + open boundary) is present in the merged authoritative tree via PR #566 (`557548db…`), post-merge verified | n/a (closed) | n/a (closed) | n/a (closed) | PR #566 merge `557548db…`, ODR Wave-2 section (recorded) |

## 3. Before serious release

| Item | Source owner | Origin | Disposition | Return trigger | Latest safe gate | Blocking | Closure evidence required |
|---|---|---|---|---|---|---|---|
| W1-N3 — residual relevance false-negative (bounded question-id-scoped attempt; evidenced fallback = safe false-negative) | RVR-6b / W2-C (gap_relevance + WS10 intent content) | Wave-1 closure §4; Wave-2 contract §J | OPEN — return at defined gate | W2-C contract freeze | W2-C | CONDITIONAL | W2-C RED test vs frozen S2 R6 fixture passing without new false positives, or evidenced deferral record |
| W1-N2 — Arabic adversarial regression test (enumerated small-talk) | RVR-7 (Wave 3) | Wave-1 closure §4; Wave-2 contract §O | OPEN — return at defined gate | RVR-7 contract freeze | RVR-7 | FRB (verification input) | merged RVR-7 suite incl. the W1-N2 AR test |
| RVR-4 decision composition (W2-A implementation) | FDC-001 + composition seam per W2-ID; implementation contract = the authoritative W2-A contract (PR #567) | Wave-2 contract §D; W2-ID record; W2-A contract (PR #567, `82758cb2…`) | **CLOSED — evidence verified.** Closure criterion (this row): "W2-A implemented/merged under the frozen contract with its full RED inventory (ID/SUP/DET/COMPAT/OW6/SEAM/PROV/LANG/CORR/REACH) green" — satisfied by prior external evidence: Owner implementation authorization exercised through the full lifecycle; bounded `deliverable_assembler.py` allowlist extension separately Owner-authorized (IG-17); accepted candidate `d8c5aef…` merged via PR #569 (`e17ca147…`, identity verified); inventory + IG-17 + N-2 tests GREEN in the merged tree `[EXEC at tip]`. IMPLEMENTATION authoritative ≠ release value: T1-A′/TTV/Differentiation/R4-C remain OPEN in their own rows | n/a (closed) | n/a (closed) | n/a (closed) | PR #569 merge `e17ca147…` + merged RED inventory (recorded) |
| **Cross-Layer Execution Assurance Standard — governance/process hardening BEFORE W2-B execution.** Owner direction recorded at the post-W2-A-implementation sync: a durable cross-layer execution assurance standard (derived from the W2-A lifecycle lessons) is to be documented after W2-A and before W2-B proceeds, through its own full lifecycle (Creator → Grill → Independent Review → Owner acceptance → merge). NOT created here; contents NOT pre-defined; nothing about it authorizes W2-B. The standard establishes the continuous traceability practices that make the later FCORA gate (row below) easier and more reliable — sequencing relationship only; the full FCORA procedure is NOT embedded in the standard | Owner (direction) + `docs/governance/CROSS_LAYER_EXECUTION_ASSURANCE_STANDARD.md` (now the standard's own authoritative surface) | ODR §D-1 direction record; the merged standard | **CLOSED — evidence verified.** Closure criterion (this row): "the standard authored/reviewed/Owner-accepted/merged through its own lifecycle" — satisfied exactly by prior external evidence: authored candidate `015a8534fbecef7e790f87cb42c087f28807d86e`, Independent External Review (verdict carrying non-blocking observations O-1…O-5), Owner exact-SHA acceptance, merged via **PR #571** (`216cdc8e61eea141940de072105aa03a4cd801bb`; second parent = the exact candidate; merge tree `611d3da4…` identical; empty candidate→merge diff), post-merge verified. **`CROSS-LAYER EXECUTION ASSURANCE STANDARD: AUTHORITATIVE`** — its Continuous Traceability Rule and C0–C4 proportionality model are now MANDATORY current process for future applicable candidates (prospective only; no retroactive execution over closed historical gates is claimed; FCORA remains un-executed). The W2-B-execution prerequisite this row guarded is now satisfied — W2-B itself remains `AUTHORIZED: NO` (its authorization is a separate Owner decision) | n/a (closed) | n/a (closed) | n/a (closed) | PR #571 merge `216cdc8e…` (recorded) |
| **FCORA — Full Capability & Obligation Reconciliation Audit (Owner-mandated future release gate).** Owner direction recorded at the post-W2-A-implementation sync: a MANDATORY, release-blocking reconciliation/audit gate positioned **after RVR-8 and before Serious Release / Production Readiness**. Purpose: no historically recorded capability, feature, obligation, deferred item, future item, or implementation may silently disappear. Mandatory rule: every historically recorded item resolves to an authoritative disposition (`IMPLEMENTED & VERIFIED` / `DEFERRED & OWNED` / `SUPERSEDED` / `REJECTED` / `BLOCKED`); anything without a defensible disposition is `UNACCOUNTED / ORPHAN`; **Owner-required pass condition: `Unaccounted / Orphan capability count = 0`**. Must reconcile BIDIRECTIONALLY (governance/docs → implementation AND implementation → governance/docs) and detect omitted, partial, renamed/split/superseded, and dormant capabilities, deferred items without a durable owner, and runtime capabilities without a governance owner. **FCORA is an AUDIT gate, never an owner**: it audits — without taking ownership of — the existing owners' items (e.g. CAP-01…CAP-18 incl. CAP-12/CAP-13 [this register §5 + PDVG tier spine]; future ADDITIONAL domain activation IoT → drone → renewable [§5]; dormant-but-built WS11 [§5]; deferred specialist/manufacturing/standards ownership [§5]; release-value obligations [§3]). Duplication adjudicated at recording: NO existing gate owns bidirectional docs↔code reconciliation with zero unexplained disappearance (this register's release-closure rule is obligation-status-only and one-directional; PDVG is tier conformance; the per-gate Material Gap Sweep is bounded; CLAUDE.md's Depth-1 full audit is a document-authority reading audit; WS-PFV-001 is a product validation capability). Detailed procedure/vocabulary refinements (e.g. partial-implementation ambiguity handling) are OPEN design questions for the future FCORA contract — NOT decided here. NOT executed now; no audit performed here | Owner (direction at this sync gate); the FCORA gate's own future contract | this sync candidate (authoritative on its merge); ODR §D direction record | OPEN — return at defined gate | the FCORA gate's own future contract + execution, convened after RVR-8 | after RVR-8, before Serious Release / Production Readiness | FRB (release-blocking by Owner mandate) | FCORA contract authored + audit executed with `UNACCOUNTED / ORPHAN = 0`, Owner-adjudicated, merged |
| W2-A implementation residual — `derived_readiness.overall_verified()` groups by `gap_context` (`derived_readiness.py:46-48` `[EXEC]`), so decision-action records (gap_context=None) form a `None` context that could flip the aggregate flag. LATENT ONLY: no live path writes a validated status `[EXEC grep at the implementation gate — zero VALIDATED_STATUSES writers]`, so the rendered flag is False for every real project regardless. Governance-admissible evidence: escalated in the Creator return of the `b3ada80…` implementation gate, then **explicitly acknowledged and preserved non-blocking by the Owner's IG-17 repair gate direction** ("Do NOT modify derived_readiness.py … keep it classified MATERIAL NON-BLOCKING / FUTURE OR ALREADY OWNED") — recorded here so a deliberately deferred finding cannot silently disappear. No other row/owner carries it (no duplication) | derived-readiness owner at its next authorized touch | Owner IG-17-repair gate direction + `[EXEC]` code evidence (both cited above) | OPEN — return at defined gate | any gate that makes validation-status writes live-reachable (adjudicate then), or the surface's next authorized touch | before serious release (adjudication) | CONDITIONAL | bounded class-exclusion (or explicit adjudicated acceptance) merged under an authorized touch |
| W2-A implementation residual — deliverable withdrawn-note renders its English constant without localization (`deliverable.html` renders `_wsr.note` raw; the constant is registered in neither `_MESSAGE_KEYS` nor `_DEEP_AR` `[EXEC]`; pre-existing — PRE-dates W2-A). Governance-admissible evidence: identified during the IG-17 work and **explicitly ruled outside that repair's scope by the Owner's N-2 gate direction** ("Localization cleanup remains outside scope") — i.e. an Owner-deferred item that previously had NO durable owner row; recorded here so it cannot silently disappear. Cross-reference, not duplicate ownership: RVR-7 (§3 row above) remains the CAPABILITY owner of substantive Arabic parity; this row tracks only this one known concrete defect instance | deliverable/ui_text owners (defect); RVR-7 row (capability) | Owner N-2 gate direction + `[EXEC]` template/catalog evidence (cited above) | OPEN — return at defined gate | RVR-7 substantive Arabic parity, or the surface's next authorized touch | before serious release IF Arabic is represented as substantive (follows the RVR-7 row's conditionality) | NBF | localized rendering merged under an authorized touch |
| RVR-6a routing/register core (W2-B) | progression_loop seams per Wave-2 contract §H | Wave-2 contract §H; OD-R5 | OPEN — NOT AUTHORIZED YET | W2-B authorization (W/M values at its acceptance) | before serious release | FRB | W2-B merged with register/suppression/ordering tests green |
| RVR-6b WS10 content + intent-aware completion (W2-C) | WS10 (existing loader) + routing consumers | Wave-2 contract §I | OPEN — NOT AUTHORIZED YET | W2-C authorization (incl. corrected WS10 scope decision) | before serious release | FRB | W2-C merged; 21-id registry committed and loader-validated |
| RVR-7 — substantive Arabic parity | Path-N artifacts + ui_text + deliverable owners; D-P6-18 supersession decision at that gate | register OD-R4 (Wave 3); Wave-2 contract §O | OPEN — NOT AUTHORIZED YET | Wave-3 authorization after W2 content stabilizes | before serious release IF Arabic is represented as a substantive supported experience | FRB (conditional on Arabic positioning) | RVR-7 merged; EN/AR semantic-equivalence review + W1-N1/N2 inputs discharged |
| RVR-8 — integrated release-value verification (incl. any second S2 run) | separate Owner authorization | remediation contract; register Wave-1 boundaries | OPEN — NOT AUTHORIZED YET (not cancelled) | Owner authorization after RVR-7 | before serious release | FRB | executed RVR-8 evidence pack under its own authorization |
| T1-A′ closure — S2 release-value criteria met | S2 benchmark owner | PDVG-01 §8; S2 run record (NO FULL PASS) | OPEN — return at defined gate | remediated-behavior verification (RVR-8 path) | before serious release | FRB | authorized verification run meeting §15.7 criteria, Owner-adjudicated |
| T1-C′ — bounded real-user validation round (ILT-style; ILT-002 collection NOT AUTHORIZED) | ILT method owner; separate authorization | PDVG-01 §9 row 1 (:1018) | OPEN — NOT AUTHORIZED YET | Owner authorization of one bounded round (incl. experienced-technical participant) | before serious release | FRB | executed round evidence measuring perceived differentiation, return intent, decision impact, clarity/usefulness, trust, perceived responsiveness |
| T1-D — truthful disclosure (fixed question set; honest capability labels) — OD-PDVG-13 undecided | Phase-3 UX display lane | PDVG-01 §4.a, :1170 | OPEN — return at defined gate | OD-PDVG-13 decision | before serious release | FRB | decided OD-PDVG-13 + merged disclosure surface |
| OD-PDVG-12 — "Why this matters" question-explainability render | Phase-3 UX display lane (content: WS10) | PDVG-01 :1159/:1219; Wave-2 contract §I.3 | OPEN — return at defined gate | OD-PDVG-12 decision (optionally at W2-C freeze for inclusion) | W2-C freeze for inclusion; else with T2-B′ before serious release | CONDITIONAL | decision recorded; render merged if approved |
| T2-G / OD-PDVG-10 — minimum semantic (meaning-adaptive) questioning; ownership unassigned | Owner adjudication (UNOWNED — true gap) | PDVG-01 §4A, row 8b (:1026) | OPEN — return at defined gate | OD-PDVG-10 decision | SHOULD before first serious release; MUST before paid activation | FRB (should) / PAB (must) | ownership decision + bounded implementation under the decided owner |
| MG-8 — seed problem statement not captured as `known_problem` | governance owner NONE ESTABLISHED; implementation locus progression/intake seam | S2 evidence sweep (OBSERVATION, cause unproven); Wave-2 contract S-13 | OPEN — return at defined gate | W2-B/W2-C evidence packs diagnose/measure; any semantics change separately Owner-authorized | before serious release (adjudication, not necessarily change) | CONDITIONAL | diagnosis evidence + explicit Owner adjudication (fix, retire, or accept) |
| R4-C replay-order acceptance-lapse semantics — Owner decision open | R4-C semantics owner + Owner | W2-D implementation (PR #564): the seq-order replay property is recorded in committed evidence — `tests/test_wave2_w2d_n4_lapse_transparency.py` N4-1 comment ('a replacement record replays at the END of the amended stream') and the W2-D candidate record; W2-ID v3 §J (boundary preserved, not absorbed) | OPEN — return at defined gate | Owner adjudication (current behavior deterministic + visibly transparent since W2-D; W2-ID designed around it; does NOT block W2-A) | before serious release | CONDITIONAL | Owner decision recorded (keep-as-is with disclosure, or separately authorized change) |
| Phase-9 preserved non-blocking debts (stale `classify_domain` docstring; 4 historical test-file comments; `UI_B_START_024` wording; missing real E2E Tier-1 chain test; CLI real-banner coverage) + stale "six owner actions" docstring (`idea_state.py:340`) | respective code owners at next authorized touch | CURRENT_PROJECT_STATE :2426 (five Phase-9 debts); the "six owner actions" docstring staleness is a code-verified observation `[EXEC — idea_state.py:340 still reads 'six owner actions' while INTERACTION_DISPOSITIONS holds seven values]`, not a governance-record citation | OPEN — return at defined gate | next authorized touch of each surface; E2E test debt before serious release | before serious release (tests); next touch (comments) | NBF | debts repaired or explicitly RETIRED with Owner acknowledgment |
| Public product name / trademark (`InventorAI` = temporary working name, OD-A) | Brand gate | register OD-A | OPEN — return at defined gate | Brand gate convened | before public launch | FRB | Owner-decided final name + brand gate record |

## 4. Before paid activation

| Item | Source owner | Origin | Disposition | Return trigger | Latest safe gate | Blocking | Closure evidence required |
|---|---|---|---|---|---|---|---|
| T2-E — evidence-writer mapping (readiness axis reachability) | Increment-2 evidence axes owner | PDVG-01 §4.b (:215), :471 area | OPEN — return at defined gate | separately authorized increment | before paid activation | PAB | merged mapping + reachability evidence |
| T2-F — ordering-defect REPAIR (OD-PDVG-08b); guard tests already merged (Wave-1/RVR-3) | assess/order owner; Owner decision 08b | PDVG-01 :471; register Wave-1 OD-R2 row | OPEN — return at defined gate (guard portion CLOSED) | OD-PDVG-08b decision | before paid activation | PAB | repair merged under guard tests |
| T2-A WS6 quantified-requirements extension; T2-B′ WS10 content + explainability display; T2-C′ bounded WS16 user-value extension; T2-D user-feedback capture | respective WS owners; T2-D UNOWNED (see §6) | PDVG-01 §5 Tier-2 list (:462-472) | OPEN — return at defined gate | per-item Owner authorization | Tier-2 rule: SHOULD before serious release / MUST before paid activation | PAB | per-item merged increments (T2-B′ content partially covered by the W2-C authorization) |
| Paid-activation hard gates: D-P8-PL-01 class C; D-PSRR-01 `PSRR = GO` (execution NOT STARTED); OD-P deployment criteria + separate Deployment Gate + explicit Owner deployment authorization | Phase-10 owners | register :742-751; OD-P | OPEN — NOT AUTHORIZED YET | Phase-10 execution | before paid/production | PAB | PSRR GO record; deployment gate record; Owner authorization |
| External-adviser-dependent conclusions: OD-CJ1 tax scope; OD-DR1 erasure; OD-DR2 account-wide export/access; final terms/privacy artifacts; jurisdiction-specific implementation | Owner + external legal/tax advisers; Phase 8/10 | register Phase-10 rows | OPEN — return at defined gate | adviser input obtained | before paid/public/commercial activation | PAB | adviser-informed Owner decisions. Standing rule preserved `[OWNER]`: adviser absence does NOT block unrelated technical development |
| Payment provider selection + subscription/billing implementation (P8-I4 provider-neutral boundary EXISTS; no provider selected) | Phase 8 / P8-I4 owners | register P8/OD-CJ1 rows | OPEN — NOT AUTHORIZED YET | provider implementation/selection gate | before paid activation | PAB | provider gate record + implementation under P8-I4 boundary |
| Production security/ops set: Phase-7 §25 deferred items (monitoring; broad abuse controls; `access_audit` retention/cleanup; production secrets ops) + P5 observations (access-log redaction; browser-history exposure before production email-provider/reverse-proxy deployment) | PSRR execution reassesses; P5/P7 owners | PSRR registration :744; roadmap :4249/:4308; state :4600 | OPEN — return at defined gate | PSRR execution / deployment gate | before deployment/production (hence before paid) | PAB (deployment-class) | PSRR execution evidence covering each item |

## 5. Strategic / post-release / future (NBF — none blocks by existing)

All `OPEN — return at defined gate` with blocking level NBF and per-item
future authorization as the trigger; source owners per the Master Obligation
Index layers: WS17 AI Coach (NOT STARTED, separate authorization); WS13
guided-answer increment (contract merged, implementation NOT AUTHORIZED);
WS14/WS15 residuals (status per L1 §15 tracker); WS16 beyond the T2-C′
bounded extension; WS11 activation (dormant, zero non-test references; per PDVG-01 §6.F it is
TIER 4 — BLOCKED BY DEPENDENCY, not merely deferred: separable from WS10,
its unlock prerequisites are the evidence-writer/ordering dependency
(T2-E + T2-F) plus its own separate authorization — activating it today
would regress truthfulness because SATISFIED is unreachable); CAP-01…CAP-18 (RECORDED — NOT AUTHORIZED; CAP-12/13 = PDVG
T4-A/B post-gate behind the evidence-writer dependency; CAP-15/17 = T4-C
conditional on AI activation); STG (RESERVED/INACTIVE — LEVEL 1); ACV;
Direct Output Download (PDF) — no PDF export/generation capability exists
anywhere in the product today `[EXEC grep]`, and this obligation does NOT
reopen the already-implemented, distinct export surfaces (FDC-001 in-memory
JSON export; P10-D3a project-scoped export; P7-I1 structured export);
Email Delivery OF OUTPUT ARTIFACTS ONLY — the account-email infrastructure
is IMPLEMENTED and out of this obligation's scope (`engine/email_sender.py`
`EmailSender` abstraction; D-P5-10 scope = verification/recovery/future
email change only, "no output/marketing/notification email" `[REPO]`);
Output-Language override; account-wide export (deferred, OD-DR2);
production export connectors (P7-I3 architecture CLOSED — reference adapter
deliberate; connector future); **future ADDITIONAL domain activation only**
(IoT → drone → renewable and any other new domain: activation, governed
content/packs, qualification, and onboarding gates remain future — while
the **§5 Multi-Domain Foundation program is FORMALLY ACCEPTED AND CLOSED**:
§5-C1 contract; §5-I1 Domain Registry Validation Hardening — which
IMPLEMENTED AND CLOSED **D-P6-14** (PR #393 `9d5e3bf`, D-S5-I1-CLOSE);
§5-I2 activation-status policy (PR #396 `e224215`, D-S5-I2-CLOSE); §5-I3
subsystem/cross-domain model (PR #398 `dac5696`, D-S5-I3-CLOSE); §5-I4
EVIDENCE GATE NOT MET → SKIP; program closure D-S5-CLOSE with "ORIGINAL §5
unfinished material obligation = NONE" `[REPO CURRENT_PROJECT_STATE
§5 block]` — closed foundation work is NOT reopened here); §5-I3's named
genuinely-future residuals (durable subsystem persistence / subsystem
identity / display-name / subsystem-grain evidence-risk-validation —
"future / NOT delivered" `[REPO]`); WS-PFV-001;
D13; DW-lane Path T (PRESERVE UNMODIFIED AND PAUSE — the broader hold
stands; OD-R3 is ACCEPTED IN PRINCIPLE with implementation NOT
AUTHORIZED. The bounded DW-lane-hold-lift exercise **OD-W2-DW-LIFT is
now EXERCISED** in exactly its bounded form via the authoritative W2-A
contract §5 (PR #567, `82758cb2…`; closed row in §2) — the exercise
grants only the three governance permissions the W2-A composition seam
needs and preserves the full forbidden list; IMPLEMENTATION of the
lifted permission remains governed by the W2-A implementation gate, and
nothing activates broader DW Path-T work);
future FDC-001 persistence
(current-only limitation per W2-ID v3 §H); QTA (dormant status fence — the
Arabic substance obligation lives with RVR-7's committed-content approach);
`main` reconciliation (PROHIBITED without a dedicated gate, OD-Q); patent
export. Specialist/manufacturing/standards/handoff ownership remains future
per its own governance; product vision is not obligation severity.

## 6. Unowned items (no force-fit)

| Item | Truth | Disposition |
|---|---|---|
| User-feedback capture | `USER FEEDBACK OWNER: NONE` — PDVG-01 §9 row 5 ("UNOWNED (first link)", no OD assigned; force-fitting explicitly refused by PDVG-01 and the corrected Wave-2 contract S-12) `[REPO]` | OPEN — return at T2-D ownership decision; latest safe gate before paid activation; PAB |
| Semantic adaptive questioning (T2-G) | UNOWNED — Owner adjudicates via OD-PDVG-10 (see §3) | OPEN — see §3 row |
| MG-8 governance owner | NONE ESTABLISHED (locus ≠ owner) | OPEN — see §3 row |

## 7. Retrospective dispositions (lineage rows — proof the audit is durable)

| Item | Disposition | Evidence |
|---|---|---|
| W1-S2 substantive-attempt gate | CLOSED — evidence verified | implemented + merged PR #564 (W2-D), tests S2-1…S2-10; Wave-1 closure §4 origin |
| W1-N4 correction-lapse transparency | CLOSED — evidence verified | implemented + merged PR #564, tests N4-1…N4-8; reconstruction outcomes artifact |
| Wave-1 RVR-1 / RVR-2 / RVR-3 / RVR-5 + continuation repair | CLOSED — evidence verified | PR #561 merge + Wave-1 formal closure record (PR #562) |
| MG-5 provenance defect; MG-6-class correction-UX gap | CLOSED — evidence verified (within implemented scope) | RVR-3 / RVR-5 per Wave-1 closure §2 |
| MG-1 / MG-2 mechanisms | CLOSED at mechanism level — release-value verification remains with T1-A′/RVR-8 (§3), deliberately NOT promoted | Wave-1 closure §3 |
| OD-W2A-SCOPE (v1 single decision context) | RETIRED — explicitly no longer required | dissolved by W2-ID v2→v3 plural-context model |
| `"d1"` ordinal identity anchor; Model-A uuid identity for derived projections | SUPERSEDED — replacement identified (founding-record chain-root model) | W2-ID v2/v3 records |
| W2-ID v1 (`f2cfe745…`) and v2 (`538d57fa…`); Wave-2 contract candidates `89736887…`, `fd2e1052…` | SUPERSEDED — replacement identified (v3 / final contract) | immutable `refs/reviewed/*` evidence |
| TDVP Outcome A ("NO NEW TDVP PROGRAM REQUIRED") | CLOSED WITHIN ITS HISTORICAL SCOPE — valid authority-at-that-time; the later PDVG-discovered T2-G gap is a NEW obligation under OD-PDVG-10, not a retroactive falsification | PR #558 record; PDVG-01; ACTIVE_INCREMENT_CONTRACT superseded-block note |
| P7-I1/P7-I3 export architecture | CLOSED — evidence verified (architecture); production connector future (§5); second-canonical-model prohibition LIVE | export_adapter contract; P7 closure records |
| **D-P6-14 — Domain Registry validation hardening** | **CLOSED — evidence verified** (implemented AS §5-I1; originally a Phase-6-era deferred prerequisite — that earlier deferral is superseded by the later §5 lineage) | §5-I1 IMPLEMENTED / independently reviewed B / MERGED PR #393 `9d5e3bf` / D-S5-I1-CLOSE; `S5_I1_DOMAIN_REGISTRY_HARDENING_FORMAL_CLOSURE_RECORD.md` |
| Product-Foundation §5 Multi-Domain Foundation program (§5-C1 + §5-I1 + §5-I2 + §5-I3 + §5-I4 evidence-gate SKIP) | CLOSED WITHIN AUTHORIZED SCOPE — formally accepted (D-S5-CLOSE; "ORIGINAL §5 unfinished material obligation = NONE"); future ADDITIONAL domain activation and the §5-I3 named residuals remain separately OPEN in §5 above | `PRODUCT_FOUNDATION_S5_FORMAL_CLOSURE_RECORD.md`; S5_I2/S5_I3 closure records (PR #396/#398) |
| Mechanical domain activation | CLOSED — evidence verified (`activated_domains() == ['electronics_electrical','mechanical']` `[EXEC]`; Phase 9 formally closed) — Mechanical is ACTIVE, never a future item | Phase-9 formal closure record |
| Phases 4, 5, 8, 9; Phase-6 executed lane; P7 increments; PVCG R1–R4 | CLOSED WITHIN AUTHORIZED SCOPE (named preserved debts live in §3/§4) | respective formal closure records |
