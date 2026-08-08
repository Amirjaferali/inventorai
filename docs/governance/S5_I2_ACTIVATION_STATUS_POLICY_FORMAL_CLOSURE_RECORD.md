# §5-I2 — Activation-status Policy + Explicit Unsupported-Domain Model — Formal Closure Record

Status: **FORMALLY ACCEPTED AND CLOSED** (owner decision, gate
`G-S5-I2-ACTIVATION-STATUS-POLICY-FORMAL-CLOSURE-01`).

Classification: documentation-only formal-closure record. It records committed
repository reality; it creates no new authority and authorizes no downstream work.
It makes no runtime/code/test/dependency/schema change, activates no domain, starts
no successor increment, and does not imply that Product-Foundation §5 as a whole is
complete. Only **§5-I2** is closed.

Repository truth overrides conversation, handover, memory, inference, and proposal.

Authoritative integration branch: `feature/atomic-json-session-persistence`
Authoritative integration tip at closure basis: `e224215228b52a53bb2a0cba8eacbdfc19e1ed78`
(PR #396 merge; parents `4770244` + `56afc7a`; merged tree `1576c9c`). `main` is out
of scope.

---

## 1. Identity and owner authorization

- **Gate:** §5-I2 — Activation-status policy + explicit unsupported-domain model —
  the second implementation increment of the accepted §5-C1 contract-of-record
  (`docs/governance/PRODUCT_FOUNDATION_S5_MULTI_DOMAIN_FOUNDATION_CONTRACT.md`;
  owner decisions **D-S5-C1**, **D-S5-01 … D-S5-09**, especially **D-S5-03**).
- **Owner authorization:** EXPLICITLY AUTHORIZED (bounded implementation gate), plus
  an explicit continuation authorization for the bounded post-review completion
  (web activation consumer + drift guards) within the same §5-I2 lane.

## 2. Accepted lineage and merge identity (independently re-verified)

| Item | SHA / value |
|---|---|
| Product base | `477024471b85c90e4b3fabd637dc3aa6def1533e` (PR #395 — Legacy Capability Capture merge) |
| Reviewed foundation candidate | `d32ca5d3f46f200276a90d6e22515cad4d900fb9` (tree `2cea01fa20bae6e6b74ba62398f6167bf877f2ed`) |
| Final remediated/completion candidate | `56afc7afb58ba2eaa7a6c2424049fbbe1016a333` (parent `d32ca5d`; tree `1576c9ca467da72d8a89b155ac9a5b7d5432da20`) |
| Publication branch | `publish/s5i2-activation-status` → `56afc7a` |
| PR | **#396** — "§5-I2 — Activation-status policy + explicit unsupported-domain model" |
| Merge (PR #396) | `e224215228b52a53bb2a0cba8eacbdfc19e1ed78` (true merge commit; no squash/rebase/force-push) |
| Merge parents | `477024471b85c90e4b3fabd637dc3aa6def1533e` + `56afc7afb58ba2eaa7a6c2424049fbbe1016a333` |
| Merged tree | `1576c9ca467da72d8a89b155ac9a5b7d5432da20` |

Lineage is exactly the two §5-I2 commits after `4770244`, SHA-preserving. Full-chain
diff **3 files changed / +346 / −9**; changed implementation paths:
`engine/domain_activation.py`, `tests/test_s5_i2_domain_activation.py`, `web/app.py`
only (**no** domain-pack metadata, **no** persistence, **no** schema/migration, **no**
dependency/CI, **no** governance file in the implementation diff). Tracked worktree
CLEAN.

## 3. What §5-I2 delivered (accepted result)

1. An explicit runtime activation/support policy (`engine/domain_activation.py`) —
   **foundation only**.
2. The canonical Domain Registry retained as the **recognition** authority (no second
   registry; D-FPC-MAP-06).
3. Pack lifecycle `status` kept **separate** from runtime specialist activation
   (D-S5-03: REGISTERED ≠ USER-ACTIVE).
4. Three bounded, testable support states: **ACTIVATED**, **RECOGNIZED_NOT_ACTIVATED**,
   **UNKNOWN_OR_UNSUPPORTED**.
5. `electronics_electrical` remains the **only** activated specialist domain.
6–8. `mechanical` / `medical_device` / `software` remain **recognized but not
   activated**.
9. Unknown domains remain **unsupported / fail-closed** (never silently electronics).
10. Aliases cannot independently grant activation (recognition-only resolution).
11. `activated_domains()` is constrained to canonically recognized domains
    (**ACTIVATED ⊆ RECOGNIZED**).
12. All current web specialist-admission sites (`/start` + three ILT-002 routes)
    consume the activation policy via a single `_admit_specialist_domain()` helper —
    the web layer holds **no competing activation decision**.
13. Explicit user-consent semantics (`DOMAIN_CONFIRM_VALUE`, the `domain_confirm`
    check) remain **separate** from runtime activation.
14. Classifier / evidence behavior (`CONFLICTING_SUPPORTED_DOMAINS`, unsupported
    refusal, lay-electrical corroboration, medical-conflict protection) unchanged.
15. **No user-facing copy changed.**
16. Persistence semantics unchanged (`confirmed_domain` untouched; no migration).
17. Domain packs unchanged.
18. No new domain activated.
19. CAP-16 (Safe Domain Suggestion Assistant) not started.

## 4. Independent review evidence

- **Foundation review** (reviewed candidate `d32ca5d`): **B —
  ACCEPT WITH NON-BLOCKING OBSERVATIONS**; BLOCKERS: NONE. Foundation architecture
  accepted; the web activation migration remained a non-blocking completion
  obligation inside the §5-I2 lane.
- **Completion delta review** (remediated candidate `56afc7a`): **B — ACCEPT DELTA
  WITH NON-BLOCKING OBSERVATIONS**; BLOCKERS: NONE. **§5-I2 IMPLEMENTATION COMPLETE:
  YES.** The four prior completion observations were closed: (1) `activated_domains`
  recognition cross-check; (2) web activation migration; (3) web/policy drift guard;
  (4) default registry-path coverage.

## 5. Test evidence (verified)

- **Delta RED on the reviewed foundation `d32ca5d`: 7 failed / 24 passed** — the
  accepted RED evidence (3 × `activated_domains` recognition cross-check/registry-
  invariant; 4 × missing web activation-binding integration).
- Focused GREEN: **31 passed**.
- Web/domain-entry regression: **27 passed**.
- Prior domain regression subset: **138 passed**.
- Playwright Draft-L2 browser subset: **30 passed** (drives the real `/start`
  electronics admission end-to-end).
- Full suite: **2009 passed / 1 skipped / 1 xfailed / 0 failed**.

**False-green correction (recorded truthfully).** An early draft of the web
activation-binding RED tests used a broad `pytest.raises(Exception)`, which would
have **false-passed** on the reviewed foundation because the missing helper raised
`AttributeError` (caught by the broad matcher). This was identified and corrected
**before final candidate delivery** by asserting the specific `DomainNotActivatedError`
semantics. The **accepted** RED evidence is **7 failed / 24 passed against `d32ca5d`**;
the early broad-`Exception` attempt is **not** represented as accepted RED evidence.

## 6. Retained non-blocking observations (NOT remediated by this closure)

1. Per-route admission-site bypass mutation is not directly test-detectable today;
   the helper/policy/browser tests protect current behavior, but a future per-route
   deactivation drift test could strengthen this.
2. `_admit_specialist_domain` currently returns the value passed in rather than
   canonicalizing to `pack_id`; harmless today (all callers pass canonical
   `electronics_electrical`), but future alias-accepting callers should revisit this.
3. The registry loads per specialist admission; cost is negligible and not a blocker;
   future caching may be considered if admission becomes a hot path.
4. Legacy `domains/iot_electronics` pack remains loader-skipped with a warning —
   pre-existing, unchanged, not part of §5-I2.

## 7. Scope truth and successor non-authorization

NEW DOMAIN ACTIVATED: **NO** · ELECTRONICS-ONLY SPECIALIST RUNTIME: **UNCHANGED** ·
LEGACY `iot_electronics`: **UNCHANGED / SKIPPED** · PERSISTENCE / DOMAIN PACKS:
**UNCHANGED** · **§5-I3 / §5-I4 / §5-CLOSE: NOT AUTHORIZED / NOT STARTED** · Phase 7:
**NOT AUTHORIZED / NOT STARTED** · new-domain activation: **NOT AUTHORIZED** · CAP-16:
**RECORDED — NOT AUTHORIZED**.

**Displacement guard.** Unfinished original Product-Foundation §5 work remains; no
recorded capability (CAP-15…CAP-18, QTA, WS17, etc.) displaces the original critical
path. **RECORDED ≠ AUTHORIZED.**

## 8. Closure status and next governance step

**§5-I2 — Activation-status policy + explicit unsupported-domain model: FORMALLY
ACCEPTED AND CLOSED** (**B — ACCEPT WITH NON-BLOCKING OBSERVATIONS**; zero blockers).
Implementation is merged (PR #396 `e224215`). **Product-Foundation §5 as a whole is
NOT complete** — only §5-I2 is closed; §5-C1 remains the contract of record.

**NEXT ELIGIBLE IMPLEMENTATION INCREMENT (per §5-C1 §18): §5-I3 — Subsystem +
cross-domain project model.** It is **ELIGIBLE FOR OWNER CONSIDERATION, NOT AUTHORIZED
/ NOT STARTED** — no successor gate is automatically authorized by this closure. Phase
4 & Phase 5 remain FORMALLY CLOSED; the executed Phase-6 lane remains FORMALLY CLOSED;
§5-I1 remains CLOSED; Decision D17 and the AISR seven-owner model are preserved.
