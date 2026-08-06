# WS6 Evidence — Section 13 HTML Comparison

Artifacts: base_/head_<case>_deliverable.html; machine counts in
ws6_repetition_counts_*.json (standalone counting is byte-identical,
longest-first — no prefix/normalized/semantic/fuzzy/AI matching).

Case A (WS1 journey):
- BASE: the byte-identical core statement rendered 8 separate times; zero
  repetition sentences; the four appended-clause variants and the unknown
  text each rendered once.
- HEAD: the core statement rendered exactly once, followed by exactly
  "This statement was recorded 8 times during the session." (count derived
  from data; the literal 8 appears nowhere in production code); every
  non-byte-identical statement still rendered fully, exactly once;
  html_repetition_sentence_count == 1 == repeated_group_total; the
  Phase 7C shared-metadata block and "(shared by 13 entries)" marker
  unchanged; no internal metadata key appears anywhere in the page.
- System-worded rows (contradiction pairs, gap anchors, pending requests)
  are excluded from grouping by the four-label provenance filter, so
  inventor repetition language can never attach to them.

Cases B-D: HEAD Section 13 shows the exact approved label, status, and
resolving action for each disposition; the verbatim inventor statement
remains visible. Case E: the exact two-line insufficiency wording renders.
