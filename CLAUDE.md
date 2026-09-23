# InventorAI — Current Repository Execution Instructions

## Current authority

**ACTIVE CONTRACT: STAGE 19 / CAP-09 SLICE-02 — DURABLE USER-WRITTEN MEASUREMENT METHOD
ONLY.** Stage 19 (WS-PFV-001 / CAP-09 Experiment-Plan Designer) is ENTERED / NOT COMPLETE.
The durable SuccessCriterion remediation (IMPLEMENTATION-01 / CORRECTION-01) is delivered
(PR #682). The only authorized implementation is CAP-09 SLICE-02: one inventor-written
measurement method per existing Section-11 experiment, durable in the same project store.
Full CAP-09 and full
WS-PFV-001 are NOT AUTHORIZED. Any other product, readiness, governance or automation work
requires a new explicit Owner authorization.
docs/governance/ACTIVE_INCREMENT_CONTRACT.md owns that declaration and the delivered
history, and is the file to read for authority — this paragraph routes, it does not
authorize. Stage 18 remains STARTED / PARTIAL / NOT COMPLETE: its two bounded CAP-01
increments are delivered (PR #678, PR #679), no further CAP-01 implementation is
authorized, full CAP-01 / full STG is not authorized, no other Stage is authorized, and
deployment, public release and paid activation remain NOT AUTHORIZED.

*(Superseded 2026-09-23, preserved so the change is visible rather than silent: this opened
"**ACTIVE CONTRACT: STAGE 19 / CAP-09 DURABLE SUCCESS-CRITERION REMEDIATION — IMPLEMENTATION-01
ONLY.** … The only authorized implementation is the durable SuccessCriterion remediation
(IMPLEMENTATION-01 / CORRECTION-01)". That was true until PR #682 delivered it and the Owner
authorized SLICE-02.)*

*(Superseded 2026-09-23, preserved so the change is visible rather than silent: this opened
"**ACTIVE CONTRACT: STAGE 19 / CAP-09 FOUNDATION CONTRACT ONLY.** … CAP-09 product
implementation is NOT STARTED / NOT AUTHORIZED YET, and schema / persistence implementation is
not authorized." That was true until the Owner authorized IMPLEMENTATION-01.)*

*(Superseded 2026-09-23, preserved so the change is visible rather than silent: this opened
"**ACTIVE CONTRACT: NONE.** No implementation mandate is currently active; any further
product, readiness, governance or automation work requires a new explicit Owner
authorization." and said "no successor Stage is started". Both were true until the Owner's
Stage-19 entry-contract authorization.)*

*(Superseded wording, preserved so the change is visible rather than silent: "ASTRA
MILESTONE 2 / A1 is the current bounded saved-project and recovery mandate under
ASTRA-M2-A1-PRODUCT-FIRST-SAVED-JOURNEY-DELIVER-01." **A1 is COMPLETED work, not the
current mandate.** Milestone 1, R-05 integration and A1's saved-journey and
safe-recovery delivery are all complete; A2, new human activity and successor
implementation remain deferred and separately authorized.)*

docs/governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md §2 owns milestone
authority and its precedence; §§3–5B own risk, tests and review. The
ACCELERATED_HIGH_ASSURANCE_EXECUTION_PROTOCOL.md owns delivery mechanics, not
another authorization model. This file owns the single boot sequence below.

## One boot sequence

Before ordinary planning or execution:

1. Read this CLAUDE.md.
2. Read the current entry and routing pointers in
   docs/governance/CURRENT_PROJECT_STATE.md, not its historical state stream.
3. Read the current milestone/contract in
   docs/governance/ACTIVE_INCREMENT_CONTRACT.md, not superseded declarations.
4. Read docs/governance/OWNER_DECISION_REGISTER.md only for relevant decisions
   referenced by that milestone or the assigned work.
5. Read the documents and applicable clauses materially relevant to the work,
   including Lean authority/risk and AHAEP mechanics when performing those functions.

Verify repository identity, working state and the live authoritative branch from
Git. The execution branch is feature/atomic-json-session-persistence; main is
not the execution base. A prose SHA is evidence of its recorded moment, not a
permanent live-tip expectation. Apply Lean §10 / AHAEP §5 to a base advance.

This sequence supersedes competing universal reading orders in this file, the
roadmap, historical anchors and old contracts. A reference to a large file is not
an instruction to read its entire history or recursively load every citation.
Consult enough relevant context to establish current authority and affected rules.

Full historical reconstruction is required only by a demonstrated authority
conflict, a continuity failure affecting current work, high-risk strategic
reconsideration, PRE-FCORA at its existing trigger, or another explicit full-audit
trigger under Lean §6. Ordinary high-risk implementation requires its relevant
security/data/architecture evidence, not an automatic full project-history audit.

Product direction and capability navigation: consult
[Commercial Differentiation Direction](docs/governance/INVENTORAI_COMMERCIAL_DIFFERENTIATION_DIRECTION.md)
(§16.G preserves the accepted North Star and future integrated readiness direction)
and the [Capability Enrichment Register](docs/governance/INVENTORAI_CAPABILITY_ENRICHMENT_REGISTER.md)
for materially relevant product work. These links create no second boot order,
current-state source or implementation authority.

Stage-by-stage product routing and the anti-drift operating practice live in the
[Master Execution Roadmap](docs/governance/INVENTORAI_MASTER_EXECUTION_ROADMAP.md)
(v1.32) and its
[Operating Checklist](docs/governance/INVENTORAI_MASTER_ROADMAP_EXECUTION_CHECKLIST.md).
**Both are DERIVED NAVIGATION and neither is execution authority**; conflicts resolve
upward — Git, then Owner decisions, then the authoritative governance/current-state
documents above, then merged PR evidence, then the roadmap, then the checklist. They add
no boot step, no current-state source and no approval stage. Two distinctions they carry
bind every agent regardless: **merged is not deployed, implemented is not activated, and
evidence captured is not a validated conclusion.** In particular the daily off-provider
backup scheduler is **MERGED, NOT DEPLOYED and NOT LIVE-ACTIVATED**, and public release,
deployment and paid activation all remain **NOT AUTHORIZED**.

## Lead execution continuity

These are operating rules for continuity, proportion and review routing. They add no boot
step, no authority level and no implementation authorization; the boot sequence above stays
the single boot sequence and the authority hierarchy above stays controlling.

**Continuity source.** Continuity never rests on Lead memory, chat memory or handover prose
alone. Use, in the order the task makes applicable: live Git/repository state; explicit Owner
decisions; the current authoritative governance/current-state documents; merged repository
evidence; the Master Execution Roadmap; the Operating Checklist; the current successor
handover and Lead Watchlist. Roadmap, checklist, handover and watchlist are continuity aids,
never independent execution authority.

**Product progress over governance.** Use the minimum governance proportionate to material
risk. Create no new review, document, gate, synchronization cycle or architecture exercise
unless it addresses a concrete material risk or an explicit current requirement. Do not reopen
completed or accepted work without new material evidence of a defect.

**Lead and executor.** The designated Lead owns sequencing, current-action selection,
architecture adjudication, evidence reconciliation, review routing and the next-step
recommendation. Claude Code or another bounded execution agent executes repository work within
the exact authorized scope; execution agents never silently redefine the roadmap or expand an
authorization.

**Review routing.** Use specialist review only when materially justified, never ritually.
Material UX / browser / E2E / localization changes go to the designated independent
UX/behaviour reviewer when needed. Architecture, persistence, schema, replay, provenance and
state-ownership questions escalate to the designated architecture reviewer (Astra role) when
materially necessary.

**Technical-proposal classification.** Every Lead technical proposal carries exactly one
class: **NOW** (required for the current authorized action); **NEXT TRIGGER** (useful only when
a named, evidence-based trigger occurs); **WATCH** (monitor, do not implement yet);
**PREMATURE** (technically possible, currently unjustified, not to be implemented). No agent
converts a WATCH or NEXT TRIGGER item into implementation without its stated trigger and
authority.

**Opportunistic modularization.** Launch no broad refactor because files are large. When
authorized product work touches a high-coupling area, consider the smallest bounded extraction
that materially reduces repeated logic or coupling. Current WATCH areas, not refactor
authorization: `web/app.py` growth and its repeated route–validation–save–recovery logic;
`engine/record_store.py` growth and persistence-ownership concentration.

**SQLite / datastore boundary.** Initiate no PostgreSQL or other datastore migration because it
might scale better. Migration needs an evidence-based trigger: material concurrent-writer
pressure, locking/latency constraints, a multi-instance requirement or another demonstrated
operational need. Until then it stays WATCH / PREMATURE as the evidence dictates.

**Domain-scaling boundary.** Study coverage of Electronics/Electrical + Mechanical is the
current baseline, not the permanent InventorAI domain ceiling. Before repeated future domain
activations, evaluate whether a bounded Domain Pack Conformance Validator would reduce repeated
manual validation; that validator is NEXT TRIGGER, not authorized implementation.

**Human-study boundary.** No recruitment, participant contact or human-data collection begins
without the required Owner authorization and applicable consent/custody readiness. Before the
first authorized T1-C′ human execution, perform an automated Study Dry Run once its
preconditions are satisfied. The accepted T1-C′ V1 study corpus
(`docs/validation/T1C_STANDARDIZED_STUDY_CORPUS_V1.md`) never becomes a pre-study
product-tuning or regression corpus.

**Test proportionality.** Default sequence where appropriate: focused tests → affected/adjacent
tests → stable full regression → hosted required CI. Never weaken mandatory CI; do not rerun
the full suite repeatedly during intermediate work when focused evidence is sufficient.

**Authority-document discipline.** Authority surfaces are already large: prefer concise current
truth, add no lifecycle prose or duplicate historical narration unless materially necessary,
and create no new governance document when an existing owner can truthfully hold the rule.

**Lead Watchlist.** For substantive continuity the Lead keeps a concise watchlist: current
action; material technical risks; high-leverage technical opportunities; NEXT TRIGGER items;
WATCH items; PREMATURE work; any trigger that has newly become true. It is continuity
information, not execution authority.

**Successor Lead (mandatory).** Before any repository mutation a successor Lead reconstructs,
from repository evidence and the handover/current sources, and returns: (1) authoritative
branch; (2) authoritative HEAD; (3) current executable action; (4) completed work that must not
be reopened; (5) current Lead Watchlist; (6) NOW items; (7) NEXT TRIGGER items; (8) WATCH items;
(9) PREMATURE / forbidden work; (10) execution-agent role; (11) architecture-review escalation
rule; (12) Owner-reserved decisions and authorization boundaries; (13) human-study
authorization state; (14) exactly ONE next action. A material inconsistency exposed by the
reconstruction is resolved before mutation. No ceremonial confirmation is required when the
reconstruction is materially correct. This applies Lean §9 (successor reconstruction and the
single checkpoint); it does not replace it.

**Successor handover.** Every substantive successor handover preserves at minimum: live
authoritative identity; current executable action; closed work that must not be reopened;
these Lead Execution Continuity Rules; the Lead Watchlist; NOW / NEXT TRIGGER / WATCH /
PREMATURE state; current material technical risks; current deferred obligations; reviewer
routing; Owner authorization boundaries; the exact stopping point and next action. This
complements the existing successor-handover protocol (Lean §9) and does not replace it.

## Historical material and substantive boundaries

Historical evidence, superseded contracts and candidate-lifecycle records are
evidence at their recorded time. They do not reimpose current approval stages,
reading duties or closed holds. ILT-002_GOVERNANCE_ANCHOR.md governs the integrity
and limits of the ILT evidence ledger; its restrictions on reconstructing missing
sessions do not prohibit repository continuity reconstruction under Lean §9.

The old replay/refactor mission and its old Current Priority were task-scoped,
not a permanent prohibition on Owner-authorized product implementation. When work
touches replay or scoring, retain truthful provenance, unchanged accepted evidence
unless expressly authorized, and faithful reporting of engine.scoring.score_case().
Fixtures and replay greenness are not substitutes for semantic truth. Investigate
the affected cause of a mismatch before changing behavior; never fabricate parity,
hide failed criteria, silently change product meaning or mutate preserved evidence.

Current product identity, ownership and security/privacy boundaries, domain
activation, evidence acceptance, and release/human-data gates remain with their
existing substantive owners. Unmodified documents' imported lifecycle mechanics
resolve through current Lean/AHAEP; they do not revive superseded routine approvals.
No phase or capability starts merely because a preceding one closed.

## Continue, hold and return

The active milestone determines permitted actions. Complete included routine work
without repeated per-file, command, START, publication or merge requests. Escalate
reserved decisions and scope changes as defined in Lean §2 and the actual mandate.

A missing roadmap SHA, PR label, merge record or other immaterial lifecycle update
does not stop work or create a synchronization candidate. Update materially changed
authority, product truth and dependencies with the implementation that changes them.
If a discrepancy affects safe authority or behavior, hold that affected work under
Lean §10; continue unrelated authorized work. Do not rewrite history to resolve it.

Only one designated Lead may mutate the project. The Lead may implement directly
or use bounded sub-agents; their authority never exceeds the Lead's. Same-session
child agents are technical assistance, not formal independent review. Apply the
existing OSP material-instruction control when its function is actually performed;
it does not create another workstream or routine Owner relay.

An Owner pause, stop or revocation is effective on receipt. Start no new mutation,
preserve accepted work, and return the single checkpoint specified by Lean §9.
