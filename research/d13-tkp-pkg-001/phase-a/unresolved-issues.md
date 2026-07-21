# Phase A Unresolved-Issues List (append-only)

- **UI-1 (coverage completeness).** The field-coverage map is representative for the D13-TKP-PKG-001 concept class, not an
  exhaustive enumeration of every repository field. Session/journey/output-formatting fields (`iteration`, `iteration_log[]`
  members, `path`, `direction`, `output.schema_version/domain/analysis_language/input_assessment.*/idea_summary.*/disclaimer_ar`)
  were inspected and noted as Present but not tabulated in full. A future authorized pass could complete the enumeration.
- **UI-2 (concept-class boundary).** Fields, missing fields, and capability gaps outside the concept class (multi-signal, bus,
  differential, wireless, mains, high-power, safety-critical) were intentionally excluded per Gate 2 §2. Whether any adjacent
  case should be brought in-scope is an owner decision, not resolved here.
- **UI-3 (RQ mapping).** Whether each proposed RQ (P-RQ-A1…P-RQ-A8) maps to the authorized RQ-01…RQ-11 set or is a PROPOSED
  ADDITION is an owner determination (Gate 3 §4); left open by design.
- **UI-4 (persistence).** `MVP_SCOPE_FREEZE` and the IdeaState comments state persistence is frozen and much state is
  in-memory/session-bounded. Whether the missing structured fields (MF-01…MF-10) could be captured without reopening
  persistence is out of Phase A scope and unresolved.
- **UI-5 (abstention rule).** The interfacing-specific abstention condition (CG-06 / P-RQ-A6) would require a defined rule and
  independent governance review before any use; undefined and unresolved here.
- **UI-6 (Phase A branch vs authoritative tip).** Product source was read at the Phase A base `57e2fac8`; governance documents
  were read at the authoritative tip. Product/application files are byte-identical between the two (only `docs/governance/`
  differs), so no divergence affected the analysis; recorded for transparency.
