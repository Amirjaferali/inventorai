# D13-TKP-PKG-001 — Phase B Research Workspace (uncommitted)

**Status:** Phase B bounded evidence & research — working-tree artifacts, **not committed, not pushed, not merged, not published.**
**Authorization:** Owner Start Authorization — D13-TKP-PKG-001 Phase B Research Only.
**Authoritative base tip:** `6a9834319075127dce5a774e2781362962d8fca5` (Merge PR #221; parents
`735d6eb4…` + `29521d52…`; tree `4072c54d…`). Workspace branch `research/d13-tkp-pkg-001-phase-b-research`
was created **from** this tip. The Phase A branch `research/d13-tkp-pkg-001-phase-a-read-only-analysis`
remains fixed at `57e2fac8` and is not touched by this workspace.

## Scope lock
- Concept class (Gate 2): single-signal sensor→microcontroller interfacing — analog-voltage / single-ended-digital /
  pulse-frequency; low-voltage; non-safety-critical. **Excludes** buses (I²C/SPI/1-Wire/UART/CAN), differential,
  wireless, mains, high-power, and safety-critical interfaces.
- Method (per Phase B decision §5): **DOCUMENT REVIEW / DATASHEET COMPARISON only.** No measurement, no bench work,
  no calculation asserted as a product output, no code, no implementation.
- Research questions: **PB-RQ-1 … PB-RQ-7** (mapping to Gate 3 RQ-01…RQ-11; from Phase A capability gaps CG-01…CG-07).

## Files
| File | Purpose |
|---|---|
| `findings/per-rq-findings.md` | Per-RQ bounded findings, technology-first field order |
| `evidence/source-provenance-register.md` | Sources, URLs, retrieval basis/date, provenance, access limitations |
| `evidence/evidence-quality-assessment.md` | Per-item evidence-quality grade + validation-status marker |
| `evidence/contradictions-and-unresolved-issues.md` | Conflicts, scope-boundary exclusions, open items |
| `evidence/abstention-log.md` | Recorded abstentions where evidence is insufficient |
| `completion/phase-b-completion-and-acceptance.md` | Completion + acceptance-criteria check + CG resolution status |
| `owner-readable-summary.md` | Plain-language summary |

## Governing constraints honored
- **Technology-first** field order preserved on every finding.
- **No-candidate / no-appointment:** competence attaches to evidence categories and methods; any "specialist category"
  is a category label only — no person or company is named, searched, screened, ranked, selected, recommended,
  appointed, or implied as a provider/candidate.
- **No invented conclusions:** nothing is asserted beyond what the cited evidence supports; abstentions are recorded.
- **Evidence quality is recorded truthfully**, never inferred from vocabulary.

## Material evidence-access limitation (recorded honestly)
Direct retrieval of primary vendor PDFs (e.g. `analog.com`, `microchip.com`) returned HTTP 403 under this session's
organization egress policy (confirmed via `$HTTPS_PROXY/__agentproxy/status` — proxy healthy, no relay failures; the
block is an egress-policy denial of those destination hosts, per `/root/.ccr/README.md`). Search retrieval was
available and surfaced quoted governing parameters attributed to those authoritative sources. Consequently, evidence
is graded on **corroboration across multiple authoritative sources (REASONED)** rather than on primary-source
verified quotation (**DEMONSTRATED**). Device-specific numeric values are **abstained** — consistent with the Phase A
finding that InventorAI cannot verify device-specific relationships without the target governing-parameter documents.
