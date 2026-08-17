# Tier-1 EN/AR Mechanical Public Label — Activation-Readiness Edge — IMPLEMENTATION RECORD (Candidate)

**Status of THIS record:** implementation-and-documentation candidate. Implements exactly one truthful Tier-1
public label addition in the existing canonical owner, plus its regression tests. Does **NOT** activate
Mechanical, does **NOT** touch `engine/domain_activation.py` or `_ACTIVATED_DOMAINS`, does **NOT** change
classifier/admission/scoring/progression logic, and does **NOT** grant or imply Owner Mechanical activation
authorization. **`OWNER_DECISION_REGISTER.md` UNCHANGED** — this implements a requirement already authorized by
the existing `P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md` §13 (Requirement 9) once activation-readiness was
reached; no new Owner decision is required.

## §1. Basis and fresh verification

Base: `7cb5b6e726a726bba223fd997d9d94905173091f` (PR #501 — SHA-preserving merge of the accepted L10N-RH-01 formal
closure candidate `0b5e238c39a74b6a207bb04114f0ce0664318136` onto `c163a9d61d18434fa5cd6a68e01aa6a033ac7ce4`; merge
tree `1edef47a87b98eed47cc0fd6b89f1d1d6d20ba05` == candidate tree; candidate→merge diff EMPTY — independently
re-verified this gate: `git log -1 --format="%H %P %T"` confirms parents `c163a9d`+`0b5e238`; `origin/feature/
atomic-json-session-persistence` confirmed at this exact tip; working tree clean at checkout).

## §2. Activation-readiness matrix — independently reconfirmed fresh (not restated)

All 13 previously-PASS prerequisites re-verified live in the checked-out tree: D3, P9-MECH-SF safety-cue family,
CF-2 (`FORMALLY CLOSED`), CF-6 (`FULLY DISCHARGED`), ILT-002 (`RESOLVED BY OWNER DECISION` — `D-CF6CF2-ILT002-01`,
not a classifier defect), L2SC-01 (`FORMALLY CLOSED`), Path-N/domain-threading (`D-GMPR-D3-PN`), the hard-coded
electronics tie-break neutrality coupling (`D-GMPR-01-D-D3`/CF5-F004), CF5-F001/F002/F003 classifier/admission
boundaries, NMF-1+FU-1 (`DISCHARGED`). The previously-OPEN item, **`L10N-RH-01`, is now `FORMALLY CLOSED /
DISCHARGED`** (PR #500/#501, this exact base). `L2SC-02` reconfirmed **outside activation-readiness / not a
Mechanical-activation blocker**. **Explicit Owner Mechanical activation authorization reconfirmed ABSENT** —
`OWNER_DECISION_REGISTER.md` searched exhaustively; the only Mechanical-activation-adjacent decision is
`D-P9-MECH-01`, explicitly scoped as "selection + qualification-planning authorization only," stating
"qualification ≠ activation... activation remains a separate, explicitly-Owner-authorized §5-I2 gate."

**Conclusion: the matrix is now 14 PASS / 0 OPEN / 1 outside-scope (L2SC-02) / 1 Owner-decision-required
(explicit Mechanical activation authorization — still pending, not granted here).** This authorizes the Tier-1
label gate itself (per contract §13's own text: the label may be added "not before activation-readiness," now
reached) but authorizes NOTHING about activation itself.

## §3. Authoritative Tier-1 contract (verified fresh, no later supersession found)

`docs/governance/P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md` §13 (Requirement 9 — Public label /
localization): requires a truthful Tier-1 Mechanical public label in the EXISTING
`web/domain_label.py::_PUBLIC_DOMAIN_LABELS` owner, EN/AR canonical variants per the D-P6-16/17/18 language
*rendering* decisions (no simultaneous EN+AR; selected-UI-language rendering; no auto-switching), replacing the
Tier-0 fallback for `mechanical` only once the label becomes truthful — i.e., at activation-readiness, now
reached (§2). §16 (Requirement 12 — Activation separation) is explicit: **"Mechanical qualification does NOT
activate `mechanical`... Nothing in this contract, its future implementation gates, or a future qualification
declaration moves `activated_domains()` off `['electronics_electrical']`."** No later governance document (roadmap,
CPS, AIC, ODR) supersedes or amends §13/§16; `CURRENT_PROJECT_STATE.md`'s most recent statement (from the
just-merged L10N-RH-01 closure) itself names this as "the next pre-activation gate — not authorized or performed
here [by that closure]," confirming this gate, and only this gate, is now eligible.

D-P6-16/17/18 (checked fresh in `OWNER_DECISION_REGISTER.md`) govern *rendering mechanics* only (three-layer UI/
Input/Output language model; no simultaneous bilingual display; global UI-language selector) — they do not dictate
specific domain-label wording text. Label wording itself is derived (§4) from the existing electronics Tier-1
precedent and the domain registry's own truthful naming.

## §4. Implementation

**Canonical owner (unique, no duplication):** `web/domain_label.py::_PUBLIC_DOMAIN_LABELS`. Added:

```python
"mechanical": {
    "en": "Mechanical-informed review",
    "ar": "مراجعة مستنيرة بمجال الميكانيكا",
},
```

**Wording derivation:** exact structural parity with the existing, already-accepted electronics entry
(`"Electronics-informed review"` / `"مراجعة مستنيرة بمجال الإلكترونيات"`) — same `<Domain>-informed review` / `مراجعة
مستنيرة بمجال <field>` template, substituting the domain registry's own truthful field name. English domain word
follows `domains/mechanical/domain.json`'s `display_name: "Mechanical"`. Arabic uses `الميكانيكا` ("mechanics" —
the field), the standard modern-Arabic engineering term, structurally parallel to `الإلكترونيات` ("electronics").
No Tier-2/3/4 vocabulary ("Specialist," "Expert," "Professional," "Certified," "Licensed") in either variant —
confirmed by the pre-existing, still-passing `test_resolver_never_emits_tier2_3_4_wording` (already parametrized
over `"mechanical"` before this gate). EN and AR verified semantically equivalent (both: "a review informed by
the [domain] field," no additional claim in either).

**Module docstring updated** (`web/domain_label.py`, lines 8-24) to remain truthful after this change: the prior
wording ("Only the RUNTIME-OPERATED domain has a Tier-1 public label") would become **false** the moment a second,
non-activated domain gains a Tier-1 label, so it was rewritten to state the actual invariant — a Tier-1 label
reflects **truthful-labeling readiness, not activation**; `electronics_electrical` is both RUNTIME-OPERATED and
Tier-1-labeled, `mechanical` is Tier-1-labeled per contract §13 but NOT runtime-activated; the resolver has no
bearing on domain selectability (the `/start` picker is driven solely by `activated_domains()`, never by this
dict).

## §5. Critical truthfulness / no-activation-leak boundary — proven, not assumed

Independently traced the exact mechanism (fresh code read, `web/app.py`):

- The `/start` domain-picker's choice set (`index.html`'s `start_choice_domains`/`start_domain_labels`) is built
  at `web/app.py` from `_activated_specialist_domains()` → `domain_activation.activated_domains()`, and rendered
  via the **separate**, lower-tier local helper `_domain_label()` (`domain.replace("_", " ").title()`) — this
  helper does **not** call `public_domain_label()`/`_PUBLIC_DOMAIN_LABELS` at all. Confirmed live:
  `webapp._domain_label("mechanical") == "Mechanical"` (plain title-case), NOT the Tier-1 catalog string —
  proving the canonical Tier-1 owner is not duplicated into the picker helper and cannot leak through it.
- `public_domain_label()`'s only two call sites (`session.html:108`, `deliverable.html:153`) render a name for a
  domain value the caller **already possesses** (`state.domain`, `cap.capability_id`) — they never enumerate or
  offer domains. `state.domain` can only become `"mechanical"` for a real user session via the (unchanged)
  admission/activation gating elsewhere in `web/app.py`, which this gate does not touch.
- **Conclusion: adding the `mechanical` key cannot, by itself, expose Mechanical as a selectable/available domain
  to any user.** New regression tests below make this an explicit, load-bearing guard rather than an
  unverified claim.

## §6. UI_B_START_024 disposition

Left unchanged, per the L10N-RH-01 closure's own residual-observation boundary. This gate's Tier-1 label surface
(`public_domain_label`) is architecturally unrelated to the present-confirm checkbox catalog (`web/ui_text.py`);
no dependency exists, and none was introduced.

## §7. Tests (LOW/MEDIUM-RISK CONTROLLED; `tests/test_p6_1_truthful_domain_labeling.py`)

New/changed, all passing:

1. `test_resolver_maps_mechanical_to_tier1_bilingual` — Mechanical EN+AR resolve correctly.
2. `test_mechanical_label_distinct_from_electronics_label` — EN/AR pairs are distinct per domain.
3. `test_resolver_falls_back_to_general_never_electronics` — `"mechanical"` removed from the fallback
   parametrize list (it legitimately no longer falls back); `"MECHANICAL"` (case-variant) added, still falls back
   correctly, and the assertion now also checks `EN_MECHANICAL not in lbl.values()` for every remaining fallback
   case.
4. `test_session_page_shows_english_mechanical_label_via_test_double` — Mechanical's label renders correctly on
   the session surface (bounded `SESSION_STORE` test double, same established pattern as the pre-existing
   `test_session_fallback_general_when_domain_missing`, since `mechanical` is not reachable via a real `/start`
   admission today).
5. `test_mechanical_not_in_activated_domains` — `activated_domains() == ['electronics_electrical']` unchanged;
   `"mechanical"` absent.
6. `test_mechanical_not_offered_in_start_domain_picker` — the real `/start` page never shows the Mechanical label
   or a `value="mechanical"` choice.
7. `test_mechanical_idea_still_rejected_at_entry_gate` — a clearly-Mechanical idea POSTed with
   `domain_confirm=mechanical` is still rejected (no session created).
8. `test_mechanical_label_owner_is_unique_not_duplicated_in_picker_helper` — `webapp._domain_label("mechanical")
   == "Mechanical"`, distinct from the Tier-1 catalog string, proving single ownership.

Focused: `tests/test_p6_1_truthful_domain_labeling.py` — **30 passed** (22 pre-existing/adjusted + 8 new).
Related/activation-boundary: `tests/test_p6_1_truthful_domain_labeling.py` + `tests/test_s5_i3_subsystem_model.py`
+ `tests/test_l10n_rh01_remediation.py` — **53 passed**. Full governed suite: **2691 passed / 3 skipped / 1
xfailed / 0 failed** (baseline was 2684; +7 net new tests — the 8 additions minus the 1 parametrize case removed
[`"mechanical"`] plus the 1 parametrize case added [`"MECHANICAL"`], i.e. 8 new test functions, 0 net change in
the parametrized fallback test's case count).

## §8. Mutation/differential proof

Pre-mutation `web/domain_label.py` SHA-256: `4b8cbb27949e219907a71831d3a31bc5ce3b5a63fd7c997de7531e82b1ad3d5c`.
Mutated the new Mechanical entry's `en`/`ar` values to the General fallback's values (in place, via direct file
write). **RED:** `pytest -k mechanical` → **2 failed** (`test_resolver_maps_mechanical_to_tier1_bilingual`,
`test_session_page_shows_english_mechanical_label_via_test_double`), 6 still passing (the leak/activation/
uniqueness guards are unaffected by this specific mutation class, as expected — they test a different
invariant). Restored the exact implementation content (re-applied the same edit, since the mutation was an
in-place file write with no prior commit to `git checkout` back to). Post-restore SHA-256:
`4b8cbb27949e219907a71831d3a31bc5ce3b5a63fd7c997de7531e82b1ad3d5c` — **byte-identical to pre-mutation, confirmed
via `sha256sum` diff.** **GREEN:** full focused re-run — 30 passed.

## §9. Activation and boundary re-verification (post-implementation, live)

`engine.domain_activation.activated_domains()` → `['electronics_electrical']` (live interpreter call).
`engine/domain_activation.py` byte-unchanged (`git diff --stat` empty for this path). No
classifier/admission/scoring/progression file touched (`git status --porcelain` shows only
`web/domain_label.py` + `tests/test_p6_1_truthful_domain_labeling.py`, both confirmed via `grep` against
`engine/(domain_rules|domain_registry|classifier|scoring|progression)`). `web/domain_label.py`'s
`_PUBLIC_DOMAIN_LABELS` now contains exactly two entries (`electronics_electrical`, `mechanical`) — no third,
no duplicate.

## §10. Boundary statements

1. **Tier-1 EN/AR Mechanical public label: IMPLEMENTED** — activation-readiness edge requirement (contract §13)
   satisfied.
2. **Mechanical remains NOT ACTIVATED** — `activated_domains() == ['electronics_electrical']`; no activation
   implied, granted, or advanced by this gate.
3. **No activation leak** — independently traced and test-guarded (§5, §7 items 5-8); the label cannot make
   Mechanical selectable/available.
4. **Explicit Owner Mechanical activation authorization remains a separate, later, explicit decision** — never
   implied by this implementation.
5. **L10N-RH-01 remains `FORMALLY CLOSED / DISCHARGED`** — unaffected, untouched by this gate.
6. **Phase 9 remains OPEN.**
7. **`OWNER_DECISION_REGISTER.md` is UNCHANGED.**
8. **`UI_B_START_024` left unchanged** — no interaction with this gate's scope.

## §11. Scope of THIS candidate

Exactly two files: `web/domain_label.py` (label entry + docstring truthfulness update) and
`tests/test_p6_1_truthful_domain_labeling.py` (regression tests). Plus this record and governance sync
(`ACTIVE_EXECUTION_ROADMAP.md`, `ACTIVE_INCREMENT_CONTRACT.md`, `CURRENT_PROJECT_STATE.md`). **ZERO
classifier/admission/scoring/progression/persistence/activation-constant diff.** Next required gate: Mandatory
Grill on this exact candidate, then the governed lifecycle. After this merges, the next Owner decision point is
**explicit Mechanical activation authorization** — not authorized or performed here.
