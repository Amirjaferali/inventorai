# WS6 Evidence — Section 13 JSON Comparison

Artifacts: base_/head_<case>_deliverable.json (normalized SESSION_ID /
IDEA_ID / GENERATED_AT_UTC); machine counts in ws6_repetition_counts_*.json.

Frozen guarantees proven identical BASE vs HEAD (case A, WS1 journey):
- 13 rows; requirement IDs req:assertion:rec_1..rec_13 via the derivation;
- every statement byte-verbatim and untruncated (8x core + 4 variants +
  the unknown text);
- ordering unchanged; one row per record;
- criticality "Not yet determined" / authority "assigned automatically by
  the system; not yet reviewed" on every row (WS4 untouched);
- section_13 key set, count_basis, count_relationship, risk_disclaimer
  byte-identical; section_14 step/blocked totals tie to 13.

Authorized JSON deltas ONLY (cases B-E): the provenance/status/
resolving_action VALUES of the three authorized disposition rows and the
empty-content placeholder STATEMENT text — exact wordings recorded in
WS6_DISPOSITION_WORDING_RECORD.md. The additive
_session_meta.requirement_landscape_synthesis object is the single
structural addition (no new top-level key; every other _session_meta key
unchanged).
