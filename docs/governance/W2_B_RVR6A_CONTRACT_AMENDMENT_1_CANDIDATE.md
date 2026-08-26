# W2-B / RVR-6a — Contract Amendment 1 (Architecture Resolution) — CANDIDATE

**Status:** CANDIDATE — awaiting Independent External Review and Owner
exact-SHA acceptance. This document AUTHORIZES NOTHING by itself. It becomes
part of the authoritative W2-B contract lineage only through the complete
high-assurance lifecycle (review → Owner exact-SHA acceptance → merge →
post-merge verification). Even after it becomes authoritative, **W2-B
implementation start remains NOT authorized** until the separate Owner
instruction §14 requires.

**Authoritative base:** `ad70723e8fdb34493ac9e53d7a9a3ceb80850708`
(Merge PR #574; parents `48017ec0…` + `12267d94…`; tree `0d139401…`) —
verified live from Git at creation; the W2-B implementation contract
(PR #573) and its post-merge sync (PR #574) are authoritative at this base.

**What this document is:** the Owner-approved ARCHITECTURE RESOLUTION
amendment to the authoritative
`docs/governance/W2_B_RVR6A_IMPLEMENTATION_CONTRACT_CANDIDATE.md`
("the base contract", authoritative via PR #573), issued after Independent
External Review rejected the first W2-B implementation candidate lineage.
It supersedes exactly the clauses named in §2 and leaves every other clause
of the base contract in force. It changes NO runtime code, NO test, NO
status surface, and NO other governance document.

**Classification legend:** `[REPO]` verified in the tree at the base;
`[OWNER-PREMISE]` an Owner-ratified premise conveyed outside the repository
(recorded here as premise, never restated as historical repository fact);
`[DERIVED]` a conclusion derived from repository evidence;
`[PROPOSAL]` a contract term proposed by this amendment for freeze;
`[FUTURE-REQ]` a requirement on the future implementation candidate;
`[HYPOTHESIS]` a claim the future implementation's own evidence must
confirm or falsify.

---

## 1. Amendment mechanism and lineage `[DERIVED from repository precedent]`

Repository governance precedent resolves amendments by **additive
supersession documents**, never by in-place rewriting of accepted history:
the owner-approved remediation plan v2 "supersedes any earlier draft"
(CLAUDE.md item 7); `OWNER_PRODUCT_IDENTITY_CORRECTION.md` corrects earlier
statements additively; the Wave-2 contract carries its own §G/§M
corrections forward inside a successor candidate rather than editing merged
history; rejected candidates are preserved unamended as evidence. This
amendment therefore:

- is **ADDITIVE**: the base contract file is byte-unchanged in this
  candidate; its historical lineage (including the D-1/D-2 repair record)
  is preserved intact;
- **supersedes, upon authoritative merge, exactly the base-contract clauses
  listed in §2** — where this amendment and the base contract conflict,
  this amendment governs; where this amendment is silent, the base contract
  remains in force unchanged;
- follows the exact-SHA serialized lifecycle of Wave-2 §M and the base
  contract §N.

**AMENDMENT MECHANISM: additive clause supersession document.**
**HISTORICAL CONTRACT PRESERVED: YES.**

## 2. Supersession map (exact old → new)

| Base-contract clause | Disposition under this amendment |
|---|---|
| §B.3 "State-aware ordering … may promote exactly: a critical unresolved gap; a lapsed acceptance; newly comparable decision state; a completed-intent skip" + its multi-trigger determinism paragraph | **SUPERSEDED** by §4 (Capability 3 — Option C semantics) and §5 (trigger table) and §6 (precedence) of this amendment |
| §B.2 trigger vocabulary where it feeds §B.3 | unchanged as a capability; its interaction with Capability 3 is governed by §4-§5 here |
| §D bullet "Decision-capture state (W2-A) may be CONSUMED read-only ('newly comparable decision state' promotion)" | **SUPERSEDED**: decision-capture state may be consumed read-only for the `multiple_decision_alternatives_declared` transition (§5.C); the phrase "newly comparable decision state" is removed from the trigger vocabulary |
| §F composition-flow item "W2-A decision state → 'newly comparable' promotion" | **SUPERSEDED** by §11 flow D |
| §F Cross-Layer classification paragraph | **SUPERSEDED** by §9 (re-adjudicated classification) |
| §K.2(b) "multiple promotion triggers firing simultaneously — deterministic precedence/tie-break (§B.3)" | **SUPERSEDED** by §6 (precedence must resolve real serving consequences, not label order) |
| §K acceptance criteria as a whole | **EXTENDED** by §10 (user-value acceptance: cue-only adaptation fails) and §7 (FDC-001 fence tests); otherwise in force |
| §L RED categories `W2B-ROUTE-*` description | **SUPERSEDED** by §5/§6 test requirements (question/action-consequence tests; label-order-only tests are insufficient) |
| §G allowlist | **EXTENDED** by §8.3 (exactly one committed evidence-pack file) — no other change; the digest-pin allowance and forbidden-surface list remain in force verbatim |
| §C (W/M) | **EXTENDED** by §8.1-§8.2 (current permitted proposal W=2/M=2; falsification duty; anti-hard-coding rule); the §C semantics, constraints, and §P value-freeze procedure remain in force verbatim |
| §K.6 evidence-pack bullet | **SUPERSEDED** by §8.3 (the committed evidence-pack file and its schema) |
| §N lifecycle | **EXTENDED** by §14 (implementation-start reset); its states otherwise stand |
| §M product/user-value basis | **EXTENDED** by §10 (the product-truth acceptance test) |
| All other clauses (§A, §E non-goals, §H determinism/compat/reachability, §I ownership, §J sweep, §O health, §P self-invalidation) | **IN FORCE UNCHANGED** (with "promotion" read per §4 wherever it appears) |

## 3. Owner Architecture Resolution (recorded premises) `[OWNER-PREMISE]`

1. **Rejected evidence:** implementation candidate
   `91c5de53f1d6f4bb0a4d9cfe857a5e9511415250` (externally reviewed:
   REJECT — material reconstruction / Owner escalation) and its
   Creator-Grill-failed same-base sibling
   `7e0174ac838f21680521951d074a6b56a88aecc6` are REJECTED EVIDENCE:
   immutable, never amended/rebased/repaired/republished, never a parent of
   any successor candidate. Both are preserved via SHA-preserving evidence
   bundles. Their historical role: they proved the base contract's
   gap-level-promotion wording structurally unsatisfiable under the
   canonical architecture (the contradiction this amendment resolves).
2. **Architecture decision — OPTION C:** state-aware next-question /
   next-action prioritization WITHIN the canonical gap. `select_next_gap`
   remains the sole canonical owner of gap selection. W2-B introduces NO
   parallel OPEN/PARTIAL gap architecture, NO new canonical gap owner, NO
   gap-level promotion, NO pre-opening/next-gap ordering, NO canonical
   gap-cascade change, NO replay-semantics change, NO session-reconstruction
   change. **Option B** (pre-opening/next-gap ordering) is NOT authorized;
   it is recorded ONLY as a separately Owner-gated architectural alternative
   if question/action-level adaptation later proves insufficient. **Option
   A** (parallel eligible-gap ordering) is not selected.
3. **Product truth:** a cue, label, trigger tuple, or metadata change alone
   is NOT adaptive routing. Every reachable trigger must cause a real,
   truthful, user-reachable change in the next governed question or action
   within the canonical gap; a legitimately unreachable trigger must be
   declared unreachable, never faked.
4. **FDC-001:** sole owner of decision comparability, minimum comparison
   context, readiness, and decision-semantics truth. The trigger
   `newly_comparable_decision_state` is REMOVED and replaced by the
   truthful transition trigger `multiple_decision_alternatives_declared`.
5. **W/M:** the current Owner-PERMITTED implementation proposal is W=2,
   M=2 — NOT Owner-accepted, NOT frozen, NOT authoritative values. The
   prior M=1 proposal was invalidated by fresh oscillation/churn evidence
   and is no longer a current proposal.
6. **Lifecycle:** this amendment materially changes contract semantics, so
   the prior implementation-start authorization does NOT carry across (§14).

## 4. Capability 3 — amended authoritative semantics `[PROPOSAL]`

**Name:** STATE-AWARE NEXT-QUESTION / NEXT-ACTION PRIORITIZATION WITHIN THE
CURRENT CANONICAL GAP.

`select_next_gap(state)` continues to select the canonical gap `[REPO —
engine/progression_loop.py:99]`; W2-B never claims to reorder, promote, or
demote canonical gaps. The adaptive policy operates over the **bounded
candidate set of governed questions/actions available for the canonical
gap through the existing authorized serving seams** `[REPO]`: the gap's
governed question variants (generic `QUESTIONS` variants and, where a
committed Path-N artifact defines them, its `ServedQuestion` entries —
consumed by identity, never re-minted), the governed RVR-2
reframe/exhausted-exit vocabulary, the six governed owner actions, the
governed Accept-Risk affordance where its W2-D gate opens, and the existing
W2-A decision-capture affordances. No new question copy, action, or route
is created by this capability; if governed alternatives do not exist for a
state, the policy **fails closed to the existing governed serving
behavior** — adaptation is never fabricated.

**Definition of `prioritize` (binding):** a MATERIAL SERVING CONSEQUENCE —
the policy's output determines which governed question text and/or which
primary suggested governed action the user actually receives next for the
canonical gap. Label ordering, cue insertion, tuple/metadata changes, or
styling are NOT prioritization. The behavioral floor is:

> same canonical gap + different governed project state/history
> → potentially different truthful next question/action.

**Required properties (all binding):** deterministic; derived (pure
recomputation from committed content + canonical state); non-persisted (no
new stored field unless repository authority independently requires one —
none does today `[REPO]`); no second canonical gap owner; no canonical-state
mutation for display purposes; answer-target honesty (an answer always
integrates against the canonical gap the user was truthfully shown);
Accept-Risk correctness (the consent gate keeps comparing against the
canonical served gap `[REPO — web/app.py accept-risk gate]`); correction
correctness (R4-C semantics untouched); replay/reconstruction preservation
(`run_iteration`, `advance_after_disposition`, `accept_gap_risk`,
`substantive_attempt_recorded`, and `engine/session_reconstruction.py`
byte-unchanged; the policy is recomputed at serving time on live and
reconstructed state alike, which is what makes parity provable `[REPO —
session_reconstruction restores the ledger only after the replay loop]`);
exactly ONE primary user-reachable next question/action per serve
(MVP_SCOPE_FREEZE failure signal 5, "multiple questions per iteration",
remains binding `[REPO]`); and NO cue-only fake adaptation (§10).

## 5. The four triggers — amended authoritative table `[PROPOSAL]`

Exactly FOUR governed trigger classes exist after this amendment; no fifth
may be added or implied. Three are carried from the base contract
(reconstructed from its §B.3 text at this base `[REPO]`), one is replaced
by Owner decision `[OWNER-PREMISE]`.

| # | TRIGGER | AUTHORITATIVE INPUT | TYPE | REACHABILITY | NEXT-QUESTION/ACTION EFFECT | FAIL-CLOSED | TEST REQUIREMENT |
|---|---|---|---|---|---|---|---|
| 1 | `critical_unresolved_gap` | canonical state only: the served gap currently blocks the maturity transition (structural mirror of `evaluate_transition`, truth-linked by test) AND is stalled per the EXISTING `STALL_THRESHOLD` vocabulary `[REPO — progression_loop.py:55, evaluate_transition]`; WS4 requirement-criticality confirmations are NOT an input (session-bounded, reconstruction-unsafe `[REPO]`) and no WS4-competing criticality owner may be created — no user-facing wording may present this as WS4 criticality | state predicate | reachable (level-1 blocked+stalled states) | prioritize the most useful governed question/action for resolving the blocker — e.g. the governed reframe/exit vocabulary and the eligible governed exits instead of a naive repeat; where the gap's variants still contain an unserved truthful variant, that variant may be prioritized | no governed alternative for the state ⇒ existing serving behavior, no invented content | same-gap/different-state test proving a DIFFERENT served question/action; truth-link test to `evaluate_transition`; no-fire test below threshold |
| 2 | `lapsed_acceptance` | active `risk_accepted` ledger record whose gap is absent or OPEN/PARTIAL again — the exact state shape the existing W2-D correction-replay lapse produces `[REPO]`; no second correction or acceptance owner is created (the canonical writer and lapse machinery are consumed read-only) | state+ledger predicate over the canonical active set | reachable (via the real correction route) | prioritize truthful re-resolution of the now-open uncertainty: serve the gap's re-resolution question/action path (e.g. its primary truthful variant and the governed re-resolution exits) instead of a stale clamped repeat, with the truthful reopened-because-lapsed explanation | acceptance still holds (gap ACCEPTED_RISK) or record superseded ⇒ no fire; no alternative ⇒ existing behavior | end-to-end flow through the real correction route (§11.B); no-fire while acceptance holds; superseded-record no-fire |
| 3 | `multiple_decision_alternatives_declared` | the canonical active decision-action ledger (W2-A records, consumed read-only; decision records carry `gap_context=None` by carrier law `[REPO — idea_state carrier validation]`) | **TRUE TRANSITION**: active alternative count for a context < 2 → >= 2, attributable to the latest ledger event; a standing predicate that fires on every render is FORBIDDEN | reachable (live W2-A declare routes) | MAY prioritize a truthful, governed comparison-evidence-gathering next question/action (existing governed affordances only). MUST NOT: claim "comparable" / "ready to compare" / "comparison started" unless FDC-001 independently derives it; modify FDC-001 readiness; populate comparison context by inventing evidence; enter W2-A/Path-T scope to make itself useful | fewer than two active alternatives (including after withdrawal), or no governed evidence-gathering candidate ⇒ no fire / existing behavior | transition tests (fires exactly once per genuine crossing; withdrawal reverses; re-render does not re-fire); §7 fence tests |
| 4 | `completed_intent_skip` | clamped verbatim repeat detection through the existing serving seams + an ACTIVE substantive attempt (the W2-D `substantive_attempt_recorded` gate — superseded attempts never count `[REPO]`) + the derived register calibration (§8) | state+ledger predicate | reachable (generic-variant clamp class; the Path-N artifact exhaustion surface remains RVR-2's and is excluded) | materially avoid redundant serving: serve a truthful alternative next question/action or the governed exit vocabulary instead of the verbatim repeat; NO fabricated completion; NO W2-C intent-registry leakage (the W2-D attempt gate is the only completion signal) | register not elevated, no clamp, or no active attempt ⇒ existing behavior | active-set discipline tests; register-gating tests; RVR-2-exclusion tests; same-gap/different-history serving-difference test |

**Unreachable-trigger honesty rule `[PROPOSAL]`:** if implementation-time
evidence shows any trigger unreachable on real journeys under an
authoritative constraint, the implementation candidate must declare that
explicitly in the evidence pack (with the constraint cited) and must NOT
fabricate behavior to make it appear live.

## 6. Simultaneous triggers — precedence requirement `[PROPOSAL + FUTURE-REQ]`

Precedence must resolve **actual competing candidate next-question/action
consequences** — which question/action is actually served when two or more
triggers fire with different serving preferences. Ordering trigger LABELS is
explicitly insufficient. This amendment does NOT freeze a precedence (no
repository authority or Owner decision fixes one `[REPO — none exists]`);
the future implementation candidate MUST propose exactly ONE deterministic
precedence/tie-break rule as a PROPOSAL subject to Owner exact-SHA
acceptance, and evidence it with: each trigger individually; meaningful
trigger combinations; the ACTUAL serving consequence under each combination
(which question/action was served, not which labels sorted first);
deterministic tie-break (same canonical state → same served outcome,
across recomputation, ledger shuffle, and reload); starvation analysis (no
trigger's truthful consequence can be permanently starved while its
condition persists, and no resolution path is blocked); repeated-cycle
behavior; the fail-closed case (no governed alternative exists); and
no-fifth-trigger proof. A test that merely sorts trigger names FAILS this
requirement.

## 7. FDC-001 hard fence `[PROPOSAL]`

- **FDC-001 (`engine/decision_workspace.py`) is the SOLE owner of decision
  comparability and readiness semantics** `[REPO]`: a candidate is covered
  iff ≥1 decision-relevant input or constraint references it; minimum
  comparison context iff ≥2 ACTIVE candidates are each covered; readiness
  Rule 1 yields `insufficient_information` without it. W2-B may CONSUME
  FDC-001 output; it may never redefine, approximate, or contradict it.
- `multiple_decision_alternatives_declared` is DELIBERATELY NOT a
  comparability claim. The future implementation MUST NOT use
  `len(active_alternatives) >= 2` (or any equivalent) as a comparability
  proxy anywhere — trigger logic, cue text, evidence pack, or tests.
- The user-facing output must NEVER display contradictory decision-state
  truth: while FDC-001 derives `insufficient_information`, no W2-B surface
  may state or imply that comparison exists, is ready, or has started. The
  existing W2-A readiness note remains the only comparability statement.
- **Required RED/acceptance tests `[FUTURE-REQ]`:** (a) two alternatives
  declared, FDC-001 still `insufficient_information` — asserted from the
  canonical composed record; (b) no W2-B surface renders a "comparable"
  (or equivalent) claim in EN or AR; (c) the prioritized next
  question/action may gather comparison evidence without any comparability
  claim; (d) FDC-001 readiness is byte-unchanged by every W2-B computation;
  (e) any future true comparability remains derived exclusively by FDC-001.

## 8. W/M, register, and the committed evidence pack

**8.1 Current value status `[OWNER-PREMISE]`:**
`CURRENT OWNER-PERMITTED IMPLEMENTATION PROPOSAL: W = 2, M = 2.`
`NOT OWNER-ACCEPTED. NOT FROZEN. NOT AUTHORITATIVE IMPLEMENTATION VALUES.`
The prior M=1 proposal was invalidated by fresh oscillation/churn evidence
and is NO LONGER a current proposal. The base contract §C semantics,
constraints (bounded, deterministic, Owner-approvable, reversible,
hysteretic, NEUTRAL floor), and the Wave-2 §P value-freeze procedure remain
in force: values freeze ONLY at Owner exact-SHA acceptance of the final
implementation candidate containing the committed evidence.

**8.2 Falsification duty `[FUTURE-REQ]`:** the future implementation must
ATTEMPT TO FALSIFY W=2/M=2 with its own evidence: compare plausible bounded
alternatives (at minimum W ∈ {2,3} and M ∈ {1,2,3} or a justified superset)
across elevation latency; false elevation; de-elevation latency;
oscillation/churn (including repeated strong-strong-weak cycles);
starvation; reversibility; correction; supersession (both directions);
noisy/none sequences; a realistic bounded novice journey; a realistic
bounded technical-user journey; deterministic replay; and suppression
stability. **Anti-hard-coding rule:** a test that merely asserts the
constants equal 2/2, or calibration evidence produced only at the proposed
values, is NOT calibration evidence — the calibration mechanism must be
exercised at the alternative values with recorded comparative traces. If
fresh evidence disproves either value, the future Creator must report the
contradiction and propose the evidence-supported alternative — no silent
force-fit to 2/2. The register LEVEL COUNT is likewise a proposal
requiring its own rationale/evidence row (no repository authority
enumerates register levels `[REPO]`).

**8.3 Committed evidence pack — authorized home `[PROPOSAL]`:** the §G
allowlist is extended by exactly ONE file, to be CREATED AND POPULATED BY
THE FUTURE IMPLEMENTATION CANDIDATE inside its exact candidate tree (it is
NOT created by this amendment; no template/stub precedent requires
otherwise `[REPO]`):

`docs/governance/W2_B_RVR6A_IMPLEMENTATION_EVIDENCE_PACK.md`

Required sections (schema): (1) **Candidate Identity Binding** (per the
binding model below — recorded inside the pack: the exact authoritative
implementation BASE/PARENT SHA and the contract/amendment authority chain;
deliberately NOT the candidate's own final SHA or tree); (2) exact
changed-path inventory; (3) six-capability traceability; (4) trigger table
with per-trigger reachability and serving consequence; (5) state-aware
question/action behavior evidence; (6) W/M proposal table
(`FIELD | DEFINITION | CONSTRAINT CHECK | EVIDENCE | PROPOSED VALUE |
CONSEQUENCE`); (7) W/M alternatives/calibration traces (§8.2);
(8) register-level-count rationale; (9) MG-8 diagnosis (§13);
(10) serving-decision state-transition matrix; (11) behavioral-composition
flows (§11); (12) consumer propagation (§12); (13) reconstruction/reload
parity; (14) Cross-Layer classification/evidence (§9); (15) UI↔engine
parity; (16) deterministic-replay evidence; (17) focused/regression/
full-suite results with every delta explained; (18) Material Gap Sweep;
(19) fact / derived / Owner-premise classification of every material claim.

**Candidate Identity Binding model (binding, anti-circular):** a Git commit
SHA is a function of the complete tree content, so a file inside the
candidate can never truthfully embed its own final commit SHA or final tree
SHA — requiring that would be circular and unsatisfiable. The pack is
therefore FORBIDDEN from being required to embed, and from claiming to
embed, its own final candidate SHA or tree SHA; placeholder laundering,
amend-after-freeze workflows, fixed-point tricks, second commits, and any
post-freeze mutation are all forbidden. Instead the binding is:

- **Inside the committed pack (knowable before freeze):** the exact
  authoritative base/parent SHA; the contract/amendment authority
  identities; the exact changed-path inventory; all implementation and
  calibration evidence (schema items 2-19).
- **External post-freeze gate evidence (recorded after the candidate is
  frozen, outside the candidate tree):** the exact candidate SHA; the exact
  sole parent; the exact candidate tree SHA; the SHA-preserving bundle
  identity; the independent-review identity.
- **Owner exact-SHA acceptance binds the pack automatically**, because the
  pack is a blob inside the exact tree of the accepted candidate — the
  acceptance applies to the entire exact candidate tree, evidence pack
  included.

Binding chain: AUTHORITATIVE BASE → FROZEN CANDIDATE TREE CONTAINING THE
EVIDENCE PACK → EXACT CANDIDATE SHA RECORDED AFTER FREEZE → SHA-PRESERVING
BUNDLE / INDEPENDENT VERIFICATION → OWNER EXACT-SHA ACCEPTANCE. No
self-reference is necessary or permitted. **Chat-only freeze evidence is
insufficient and rejected.**

## 9. Cross-Layer Execution Assurance classification (re-adjudicated) `[DERIVED per the authoritative Standard]`

Option C composes: engine serving policy → serving consumer (session
render) → user-visible next-question/action composition. Under the
Standard's own class table: **C2 (material cross-layer change) + C4
(user-facing composition change)**. NOT C3: no durable write, no
idempotency/supersession change, no canonical state-transition change, and
NO mutating route is authorized by the Owner decision — **if a truthful
Option-C implementation were to require a new mutating route, the
implementation must STOP and escalate (C3 + §6.3 Intent-vs-Payload/Retry
Matrix would then be mandatory); this exclusion is reviewable.** Applicable
assurance union (C2+C4): §4 Continuous Traceability; §5 Requirement vs
Behavioral Composition coverage separation; Cross-Layer Composition Matrix;
consumer-propagation sweep; §8 adversarial attacks; both Grills; UI↔engine
parity (incl. EN/AR where rendered). Proportionally RETAINED as mandatory
evidence although not C3-triggered: a SERVING-DECISION transition matrix
(the serving outcome changes with state and must be enumerated) and
reconstruction/reload parity verification (the derived policy must
recompute identically on cold reconstruction).

## 10. User-value acceptance — shallow adaptation fails `[PROPOSAL]`

For EVERY reachable trigger, at least one future behavioral test must
establish through a real journey:

> same canonical gap + different relevant project state/history →
> different truthful next question/action, OR a governed truthful
> exit/skip where that is the capability.

NOT sufficient (each explicitly fails acceptance): a cue appears; CSS
changes; metadata/tuple changes; a trigger label appears or reorders;
explanatory text changes while the served question/action remains
materially identical. The product acceptance question is: **did the
journey actually respond to what the user already demonstrated, accepted,
declared, or left unresolved?** Governed explanatory cues remain REQUIRED
where the base contract requires them (truthful transparency), but they
never count as the adaptive behavior itself.

## 11. Behavioral composition requirements `[FUTURE-REQ]`

Real composed flows through real seams — isolated unit assertions do not
satisfy these. Required at minimum:

- **A.** substantive answer → prior-intent detection → question/action
  reprioritization or suppression → correction (real route) → truthful
  re-eligibility;
- **B.** accepted risk → no inappropriate repeat → correction lapse (real
  route) → truthful next question/action for the reopened uncertainty;
- **C.** register raise → adaptive next-question/action behavior →
  contrary evidence → register lower → behavior reverses truthfully;
- **D.** `multiple_decision_alternatives_declared` transition →
  comparison-evidence question/action prioritized → NO false comparability
  statement → FDC-001 readiness unchanged;
- **E.** reconstruction/reload → identical derived policy result;
- **F.** trigger-free legacy path → existing behavior preserved
  byte-identically.

REQUIREMENT COVERAGE and BEHAVIORAL COMPOSITION COVERAGE remain separate
reported dimensions; both must pass.

## 12. Consumer propagation `[PROPOSAL]`

The historical inventory (seven runtime `select_next_gap` call sites + the
`session_reconstruction` module import + test files, per the base contract
§A/§F) is SEED EVIDENCE ONLY — the count is NOT frozen. The future
implementation MUST re-sweep from its actual authoritative base with a
reproducible methodology: exact search commands/terms; direct calls;
imports; aliases; wrappers; indirect consumers; web consumers; CLI;
reconstruction; tests — and adjudicate EVERY consumer against the policy
(verified-contained / verified-updated / escalated).

**Option-C serving-consumer rule:** every user-reachable serving consumer
that the contract expects to provide W2-B behavior MUST consume the policy;
a silently narrower delivery than the contracted claim is a defect.
**Explicit scope truth:** W2-B's contracted behavioral surface is the
governed WEB session journey. The governed minimal CLI
(`scripts/run_cli.py`) is INTENTIONALLY OUTSIDE the W2-B behavioral scope:
it is not on the §G allowlist, receives no W2-B policy behavior, and must
remain byte-unchanged; this narrowing is stated here truthfully rather
than implied, and extending W2-B behavior to the CLI requires separate
scope authority.

## 13. MG-8 — complete diagnosis contract (DIAGNOSIS/MEASUREMENT ONLY) `[PROPOSAL + REPO]`

No MG-8 semantic repair is authorized; any semantics change remains a
separate Owner decision. The future evidence pack/tests must cover the
ACTUAL phenomenon `[REPO — verified at this base]`: `/start` admits, builds
a gapless state, and runs `run_iteration(state, idea_text)`; the seed
traverses the LEVEL-0 establishment branch whose capture guard is
`quality >= REASONED` alone (no relevance conjunct on that path); the seed
is durably stored ONLY in the reconstruction envelope
(`seed_idea_text`), never as an `AssertionRecord`; `idea_summary` capture
sits inside the SAME level-0 guard. Required evidence: (a) real `/start`
with a below-REASONED problem-prose seed → durable seed stored verbatim ∧
`known_problem is None` ∧ `idea_summary is None` ∧ no seed ledger record;
(b) real `/start` REASONED control → captured + summarized + durably
stored; (c) conjunct isolation distinguishing the level-0 seed path
(quality-only guard) from the later in-gap sibling guard
(`relevant ∧ quality >= REASONED`); (d) cause-vs-symptom diagnosis
(including a representative problem-prose corpus probe of `assess_response`
tiers, and consumption evidence that no path revisits the stored seed);
(e) cold reconstruction reproducing the pair identically; (f) proof that
no semantic change occurred (locus byte-unchanged). If implementation-time
repository truth disproves any item here, the evidence pack must correct
to primary-source truth and report the contradiction.

## 14. Implementation-start lifecycle reset `[OWNER-PREMISE + PROPOSAL]`

Historical premise: the Owner previously authorized implementation start
under the PRIOR (unamended) contract, outside the repository workflow; that
authorization produced the now-rejected evidence lineage and its
repository recording remains a pending later-sync obligation. Because this
amendment MATERIALLY changes the authorized contract semantics:

**THE PRIOR IMPLEMENTATION-START AUTHORIZATION DOES NOT AUTHORIZE
IMPLEMENTATION UNDER THE AMENDED CONTRACT.**

After this amendment becomes AUTHORITATIVE through the complete lifecycle,
a NEW, separate, explicit Owner implementation-start authorization is
MANDATORY before any new W2-B runtime implementation candidate is created.
Nothing in this document grants, implies, or pre-writes that authorization.
Lifecycle states: this candidate accepted+merged ⇒ `W2-B AMENDED CONTRACT
AUTHORITATIVE`; implementation start ⇒ only via the new Owner instruction;
`W2-B IMPLEMENTATION AUTHORITATIVE` ⇒ only at Owner exact-SHA acceptance +
merge of the future implementation candidate (which also freezes W/M per
§8/§C/§P); the register RVR-6a row closes only on that evidence.

## 15. Strict exclusions (preserved and extended) `[PROPOSAL]`

NOT authorized by this amendment or the amended contract: Option A
implementation; Option B implementation; parallel-open-gap architecture;
canonical gap-cascade changes; replay/reconstruction semantic changes;
W2-C; RVR-7; RVR-8; FCORA execution; CAP-12; CAP-13; IoT activation;
Drones activation; Renewable Energy activation; deployment; production;
Serious Release; Paid Activation; unrelated W2-A expansion; Path-T
implementation merely to make comparability reachable; MG-8 semantic
repair; unrelated cleanup/refactor; new persistence model; new datastore;
any second canonical decision/gap/readiness owner. The base contract's §E
non-goals and §G forbidden surfaces remain in force verbatim.

## 16. Self-invalidation record `[DERIVED — searched at this base]`

Falsification was attempted for each load-bearing premise: (a) *Option C
sufficiency* — the governed candidate sets (variants, exit vocabulary,
owner actions, Accept-Risk affordance, decision affordances) exist at this
base and the suppression precedent proved serving-level selection is
implementable and parity-safe; no repository authority forbids
question/action-level selection (MVP freeze forbids multiple questions per
iteration, which Option C preserves); (b) *no canonical-ownership change
needed* — confirmed (display-selection precedent: RVR-2/get_display_question);
(c) *every trigger can have a real consequence* — governed alternatives
exist for triggers 1, 2 and 4; trigger 3's consequence is bounded to
existing governed affordances and its fail-closed path is explicit —
`[HYPOTHESIS]` its usefulness is confirmed or falsified by implementation
evidence, and the unreachable-trigger honesty rule governs the failure
case; (d) *the replacement trigger removes the FDC-001 contradiction* —
confirmed: the only comparability-claiming W2-B surface was the removed
trigger's cue; FDC-001's predicate is untouched; (e) *W=2/M=2 plausible* —
recorded as Owner-permitted proposal with a mandatory falsification duty;
(f) *evidence pack without a second governance registry* — one schema'd
file recording evidence, not statuses; registers remain the status owners;
(g) *MG-8 diagnosis-only* — the diagnosis plan requires no locus change;
(h) *no replay change needed* — the policy computes at serving time on
live and reconstructed state; the replay loop is untouched; (i) *no new
mutating route needed* — prioritization and action surfacing are
GET-render serving decisions over existing routes; the C3 STOP rule (§9)
guards the residual risk. No premise was invalidated at this base.

## 17. Amendment lifecycle state

THIS DOCUMENT: CANDIDATE — NOT AUTHORITATIVE. `W2-B AMENDED CONTRACT
AUTHORITATIVE: NO` until review → Owner exact-SHA acceptance → merge →
post-merge verification. `W2-B IMPLEMENTATION START (POST-AMENDMENT)
AUTHORIZED: NO`. `W/M VALUES OWNER-ACCEPTED: NO`. `W/M VALUES FROZEN: NO`.
No governance status surface is modified by this candidate; the
post-acceptance status synchronization (including the pending
implementation-start recording correction) is a separate later gate.
