# CF5-F004 — Hardcoded Non-Activated Priority Fallback — INDEPENDENT VALIDATION RECORD (Candidate)

**Status of THIS record:** governance/documentation-only **INDEPENDENT VALIDATION RECORD CANDIDATE** for CF-5 finding
**CF5-F004**. It records the completed independent validation — verdict **ACCEPT WITH NON-BLOCKING OBSERVATIONS (blocking:
NONE)** — performed by a genuinely independent reviewer in a separate session (Lean §5 independence) over the
executing-agent disposition analysis and its Mandatory Grill. **It implements NOTHING** — no runtime, Web, CLI, test,
domain, registry, activation, schema, or persistence change; **it creates no corrective contract, authorizes no remediation
or code work, selects/registers/activates no domain, and does not close CF5-F004, CF-3, CF-5, CF-6, or CF-2.** It becomes
authoritative only through the governed lifecycle (Mandatory Grill → independent external exact-candidate review → Owner
exact-candidate acceptance → SHA-preserving publication → PR → pre/post-merge verification).
**`OWNER_DECISION_REGISTER.md` UNCHANGED** (validation records register no new Owner product-policy decision — the
CF5-F002/F001 validation-record precedent).

## §1. Authoritative repository tip and evidence basis

Validation basis: authoritative tip `e39f667a934f0702301ab71d5b17a6b1121a4ecf`
(`feature/atomic-json-session-persistence`; PR #460 merge of the CF5-F001 formal-closure candidate `203772f8`; merge tree ==
candidate tree; freshly fetched at candidate creation; 0 newer); boot OK; `activated_domains() ==
['electronics_electrical']`. Evidence inputs: the CF-5 audit registration ("CF5-F004 — hardcoded non-activated priority
fallback / CF-3", open C); the P9-E2-R CF-3 carry-forward registration ("no reachable defect today; MANDATORY to resolve
BEFORE first Nth-domain registration/activation that could exercise an omitted-pack fallthrough"); the executing-agent
disposition analysis (read-only, produced against this same tip, Grill PASS WITH NON-BLOCKING OBSERVATIONS); and the
independent reviewer's own read-only re-derivation.

## §2. Classification

**CF5-F004 = OPEN C — INDEPENDENTLY VALIDATED**: a real material defect, **currently dormant** (class C retained on
evidence). Validation only; no remediation is performed or authorized by this record.

## §3. Finding identity (exact)

The **hardcoded non-activated priority fallback literal** in `engine/domain_rules.py::classify_domain`, Case 0
(`:234-242`): `priority = ["medical_device", "electronics_electrical", "mechanical", "software"]` — a fixed 4-id policy
literal consulted whenever the top-scored set contains zero ACTIVATED domains; it produces every
recognized-but-not-activated SINGLE result in the system. **The literal has no canonical owner and no synchronization
mechanism with the canonical Domain Registry — that absence is itself part of the defect.** **F004 and CF-3 are distinct
governance records over the same residual classifier surface**: CF-3 is the standing P9-E2-R carry-forward obligation; F004
is the CF-5 audit finding; neither status substitutes for the other, and **both discharge only at eventual F004 formal
closure** (never earlier, never implicitly).

## §4. Exact failure arms (independently validated)

1. **Omitted-pack sole-top fallthrough:** a registered pack whose id is outside the literal top-scores alone → the loop
   exhausts → **silent NONE** despite an unambiguous single-domain classification.
2. **Omitted-pack tie absorption:** a registered pack outside the literal ties at `best_score` with a legacy literal member
   → the literal member is **silently awarded the SINGLE result**, absorbing the new pack with no tie surfaced.

**Dangerous Web chain (validated):** registered-but-omitted pack → classifier NONE → the sole-electronics `/start`
governed NONE-consent path → a possible **electronics-labeled persisted session** for a non-electronics idea
(mislabel-class). **Not reachable today:** the recognized registry set currently equals the literal set exactly
(mechanically verified; `iot_electronics` is schema-skipped and therefore unregistered), so no omitted registered pack can
exist at this tip.

## §5. Exact trigger (binding; precision language)

**The first successful change to the recognized-registry set** — including: the first successful registration of a new
pack; a schema+provenance change that causes a previously skipped pack to register (the `iot_electronics` schema-fix corner
is the nearest concrete example); or a rename/removal skew of a literal member.
- **Registration IS the trigger.**
- **Activation is NOT the trigger and is too late** (activated domains bypass the literal via the closed D3-D/P9-E2
  precedence; the defect fires while the new pack is merely recognized).
- **Empty activation is NOT a trigger.**

## §6. Closed behavior that must NOT be reopened

**D3-D** (activated outranks recognized-not-activated on ties), **P9-E2** (≥2 activated tie → AMBIGUOUS_TIE, no winner),
**CF5-F003** (whole-token matching semantics), and the **CF5-F002** activation-derived `/start` admission are CLOSED,
authoritative behavior; the literal governs ONLY zero-activated-tied cases and was deliberately "retained unchanged" by
those gates. Nothing in this record or any later F004 gate re-litigates them.

## §7. Canonical ownership

Classification = `classify_domain` (single owner; any remediation stays inside it — no second classifier/matcher);
recognition = the canonical Domain Registry (§5-I1); activation = `engine/domain_activation` (§5-I2); activated-tie
precedence = the closed D3-D/P9-E2 policy. The non-activated fallback literal is the un-owned residue (§3).

## §8. Backward compatibility, determinism, and `infer_domain`

Unless explicitly governed otherwise in the future corrective contract: the **current 4-domain-registry classification
outputs are backward-compatibility-locked** (differential parity; committed pins include RED-R7 `gear and catheter →
medical_device` and the CF5-F002 electronics-only parity corpus — the literal's live precedence flavor on `/start`
guidance included); **strict determinism** is mandatory (no dict-/registration-order dependence without an explicit
governed rule); the legacy **`infer_domain` `str|None` + fail-loud contract is frozen** and must remain total over
SINGLE/NONE with fail-loud richer kinds. Whether the legacy precedence order must be preserved for FUTURE packs, or may be
replaced, is an OPEN Owner question (§10).

## §9. Disposition

**Architecture remains OPEN** (registry-derived fallback vs. fail-closed NONE-with-recognized-candidates vs. other — no
direction is selected by this record). **Remediation is trigger-bound and NOT required now**; the binding bounded
pre-trigger corrective prerequisite applies before the §5 trigger. **A bounded corrective contract is required only after
this validation record becomes authoritative**, followed by the separately governed implementation gate; Owner
re-disposition remains a legitimate outcome only as an explicit governed, recorded Owner decision that cannot silently
waive the pre-trigger obligation or CF-5 completion. **Out of / adjacent to scope:** the registry loader's skip-warning
path remains OUTSIDE F004 (adjacent lane input); the IoT vocabulary observations — `_LAY_ELECTRICAL_WORDS` content and the
absence of an IoT strong-unsupported family — are **examination inputs only** for future gates, NOT new F004 obligations.

## §10. Owner-policy questions preserved OPEN (for the future corrective-contract gate; decided by no one here)

1. Whether the pre-trigger obligation should bind **before any pack-schema work capable of causing registration** (the
   `iot_electronics` corner), i.e., earlier than the registration event itself.
2. Whether the current legacy precedence order must be **preserved** for future packs or **may be replaced** under an
   explicit Owner decision.
3. Confirmation that **CF-3 discharge occurs only at F004 formal closure** (carried as stated in §3).

## §11. Governance disposition & non-effects

**CF5-F004 = OPEN C — INDEPENDENTLY VALIDATED (this record, candidate).** CF5-F001 = FORMALLY CLOSED; CF5-F002 = FORMALLY
CLOSED; CF5-F003 = CLOSED (all as already recorded — unchanged). CF-5 = OPEN; CF-6 = OPEN (facets (i)–(iv) discharged
only); CF-2 = OPEN; CF-3 = registered/retained (distinct, §3); the D-GMPR-01-D-D3 hard-coded tie-break coupling remains
OPEN and discharges only at eventual F004 formal closure. D4 SEPARATE / UNEXECUTED; D8 Owner-reserved; Phase 10 NOT
AUTHORIZED; PSRR NOT EXECUTED; deployment/production NOT AUTHORIZED. `activated_domains() == ['electronics_electrical']`;
**NO domain selected/registered/activated; first new-domain activation remains BLOCKED** — and per §5, the F004 pre-trigger
obligation additionally binds BEFORE any first registry-set change.

## §12. Scope of THIS candidate & next gate

Governance/documentation only: this NEW validation record + `ACTIVE_EXECUTION_ROADMAP.md` (append-only) +
`ACTIVE_INCREMENT_CONTRACT.md` + `CURRENT_PROJECT_STATE.md` current-truth sync. **ZERO** runtime / test / Web / CLI /
domain / Registry / activation / schema / persistence / API / guardrail / ODR diff. **Next required gate: Mandatory Grill
on this exact validation-record candidate**; after this record is authoritative, the bounded CF5-F004 **corrective
contract** is the subsequent separately governed gate (direction frozen there; §10 Owner questions resolved there).
