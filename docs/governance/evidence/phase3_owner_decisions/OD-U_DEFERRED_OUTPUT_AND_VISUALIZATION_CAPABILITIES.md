# OD-U — Deferred Output and Visualization Capabilities

**Type:** documentation-only owner decision (candidate). **DOCUMENTED NO-VALID-RED.**
**Authoritative branch:** `feature/atomic-json-session-persistence`.
**Verified prerequisite tip:** `7816bdaddd762c38e6fa8cbbf05b7de26022e306`.
**Scope:** canonicalize three owner-intended future capabilities and their governance
boundaries. **Authorizes no design and no implementation.**

---

## 0. Lifecycle status

`OD-U: CANDIDATE / NOT YET REVIEWED / NOT YET MERGED / NOT YET CLOSED.` Grants no
implementation authority. All three capabilities are **NOT implemented** and each remains a
LEVEL-1 / separately-gated future capability.

## A. Approximate Concept Visualization (ACV) — التصور البصري التقريبي للفكرة

### A.1 Apparent conflict — stated, not hidden

ACV generates an **image**, which apparently conflicts with:
- `STRATEGIC_PRODUCT_VISION.md §7 Principle 2 — Improvement, Not Generation` ("does not
  generate inventions, mechanisms, products, or technical answers"; prohibits using the
  platform as an idea-generation tool); and
- `MVP_SCOPE_FREEZE.md` "External document generation" freeze.

This conflict is **acknowledged**, not waived.

### A.2 Bounded carve-out (resolution)

ACV is admitted only within this boundary. ACV:
- visualizes an **already-captured, inventor-owned idea record**; it does **not** originate
  the core idea, invent missing knowledge, supply missing mechanism steps, or complete
  reasoning — so it does **not** cross Principle 2 (it improves/illustrates; it does not
  generate the invention);
- does **not** replace inventor authorship;
- does **not** present generated imagery as authoritative technical progress;
- is an **approximate concept illustration** — **not** CAD, **not** a manufacturing drawing,
  **not** dimensionally precise, **not** final engineering design, **not** simulation-ready
  geometry, **not** a patent figure by default, **not** guaranteed correct;
- makes **no** safety, compliance, feasibility, manufacturability, patentability, or readiness
  claim.

The corresponding Level-0-consistent narrowing is recorded as an **append-only bounded
allowance** in `MVP_SCOPE_FREEZE.md`. `STRATEGIC_PRODUCT_VISION.md` and
`INVENTORAI_PROJECT_STATE_FREEZE_v1.2.md` Principle-2 statements are **unchanged** and remain
binding; the carve-out is drafted to remain consistent with them. The carve-out must **not**
be broadened into general content generation, autonomous invention generation, external-
document generation, CAD, patent drafting, or Structured Technical Guidance.

### A.3 Intended governed workflow (design target only)

```
structured and approved idea record → eligibility gate → Visualization Brief →
controlled prompt → generation → inspection → user options → save the accepted image only
```

### A.4 Phase allocation

- **Phase 3:** UX placement and interaction design only, after the applicable separate Phase 3
  gate and owner authorization.
- **Phase 4:** persistence, privacy/data lifecycle, storage, retention, deletion, and
  generation/regeneration-limit foundations.
- **Phase 5:** accounts, authentication, ownership, and authorization foundations.
- **After Phase 5:** a separate owner-authorized implementation workstream for provider
  integration and actual image generation.

This candidate authorizes **no ACV UX design and no ACV implementation** — only canonicalization.

## B. Direct Output Download

Canonical named **future** capability, distinct from the already-implemented narrow **FDC-001
canonical-JSON decision-record export** (which is unchanged).

- **Phase 3 (UX only):** placement; availability/eligibility states; output-version selection;
  preparation/progress/error/success states; optional selection of output sections;
  relationship to an accepted ACV image; truthful privacy/limitation messages.
- **Phase 4 (implementation):** secure PDF generation; secure storage; authorized download;
  version binding; retention; deletion; lifecycle enforcement; audit record.

Authorizes **no** PDF implementation, no file storage, and no new download endpoint.

## C. Email Delivery

Canonical named **future** capability for delivering outputs or accepted ACV images.

- **Phase 3 (UX only):** placement; explicit opt-in; content selection; recipient display;
  send/resend/error/success states; **no silent delivery**.
- **Phase 4:** persistent output; delivery record; retention/deletion; delivery audit;
  rate-limit foundation.
- **Phase 5:** account ownership; authentication; authorization; verified email; verified
  ownership; account-bound delivery permissions.

**Anonymous sessions must not send protected outputs to an unverified or unowned destination.**
Authorizes **no** email service, sending implementation, verified-email implementation, or
delivery persistence.

## D. Authority

`ACV / DIRECT OUTPUT DOWNLOAD / EMAIL DELIVERY IMPLEMENTATION: NOT AUTHORIZED.` Each is LEVEL 1
and requires separate explicit owner authorization at the applicable gate. OD-U grants no UI,
runtime, schema, database, prompt, AI, test, domain, deployment, or main-reconciliation
authority.
