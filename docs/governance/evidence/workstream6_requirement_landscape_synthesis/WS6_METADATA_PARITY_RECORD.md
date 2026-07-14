# WS6 Evidence — Metadata Schema and Direct Parity Record

Object: _session_meta.requirement_landscape_synthesis (additive; no new
top-level package key; pinned top-level key set proven unchanged by the
focused P4 test).

Schema (implemented; machine copy in ws6_metadata_parity.json):
- synthesis_basis (str, constant "byte_identical_statement_and_metadata").
  Source: fixed. Purpose: self-describing D1 rule. Rendered: no.
  Needed: records the grouping law the artifacts obey.
- statement_groups (list). Per entry:
  - statement (str; the exact inventor statement). Source: Section 13 row.
    Purpose: parity anchor + template key. Rendered: yes (as the single
    visible statement). Needed: identifies what the count refers to.
  - provenance, status, criticality, criticality_authority,
    criticality_rationale, resolving_action (str/None; byte-equal to the
    row's already-public values). Source: Section 13 rows. Purpose: the D1
    same-metadata-group discriminator that lets the template locate the
    group inside the Phase 7C presentation WITHOUT re-deriving disposition
    from raw state. Rendered: not additionally (the rows already render
    them). Needed: prevents cross-metadata grouping (see the criticality
    split proof).
  - occurrence_count (int >= 1). Source: count of fully byte-identical
    rows. Purpose: the derived N. Rendered: only inside repetition_note.
    Needed: drives and proves the count.
  - repetition_note (str/None). Source: owner sentence template + derived
    count; None for singletons. Purpose: THE string the template renders,
    so HTML is literally metadata-driven. Rendered: yes. Needed: makes
    metadata<->HTML parity checkable byte-exactly.
- group_total, repeated_group_total (int). Source: derived. Purpose:
  bounded summary totals the parity test cross-checks against the rendered
  sentence count. Rendered: no.

Direct parity proof (ws6_metadata_parity.json, parity_ok=true): for every
group, metadata occurrence_count == the recomputed number of matching
byte-identical JSON rows; repetition_note byte-equals the sentence built
from the derived count (None for singletons); the metadata's own note
string renders in HTML; each metadata statement renders standalone exactly
once; the rendered repetition-sentence total equals repeated_group_total;
no internal metadata key leaks into the HTML page. The strengthened focused
R4 test enforces the same comparisons and fails on any metadata/HTML
divergence. The harness fatals (exit 2) if parity_ok is false.
