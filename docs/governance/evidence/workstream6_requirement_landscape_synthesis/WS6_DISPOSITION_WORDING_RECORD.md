# WS6 Evidence — Disposition Wording Record (byte-exact)

Selection is SOLELY by the exact existing AssertionRecord.disposition value;
no content, vocabulary, quality, domain, or complexity inference exists.
Requirement IDs (req:assertion:rec_N), record-linked identity, anchor kind,
precedence, ordering, one-row-per-record, and Section 14 eligibility are
unchanged for all three dispositions (machine values in
ws6_repetition_counts_head.json).

unknown -> label "Recorded unknown"; status "You indicated that this is not
known yet."; action "This item remains unresolved. It may later be
addressed through additional information, evidence, or specialist input."

deferred -> label "Deferred decision"; status "You chose to defer this
item."; action "This item remains unresolved and can be revisited when you
are ready to decide."

provisional_assumption -> label "Provisional assumption"; status "This
assumption was recorded as a temporary direction and has not been
validated."; action "Validate, revise, or replace it before relying on it."

answered, evidence_requested, specialist_requested, contradiction pairs,
gap anchors, and every unlisted disposition: byte-unchanged legacy
vocabulary (proven by the base_/head_ emptycontent case: provenance/status/
action remain the legacy answered values; only the D7 statement wording
changed).
