# WS4_REVIEW_FINDINGS — independent HEAD GREEN review disposition

Independent HEAD GREEN review of Draft PR #183 (head
`61f0b14cb6bf2f5c5328eb9958640bf036015720`): **PASS. Blocking findings:
NONE.** (Owner-communicated result, recorded verbatim from the evidence
authorization.)

## The four non-blocking findings — recorded exactly, classified as FUTURE
## HARDENING OBSERVATIONS, not current blockers

Per the owner evidence authorization these are recorded only; **none is
fixed in this evidence step**, and none blocks the current gate. Any future
fix requires its own owner authorization.

1. **Completion-stage gate re-check absent in POST.** The criticality POST
   branch validates the re-derived focus and token but does not re-check the
   completion-stage condition (`maturity_level >= 2 and no open gaps`) that
   gates rendering. Future hardening observation: add the same stage guard
   to `_handle_criticality_action` for defense in depth.

2. **`rationale_source` CRLF attribution edge.** Reused-statement detection
   compares the submitted rationale byte-equal to the ledger record content.
   A browser submitting CRLF-normalized textarea content that differs from
   the stored statement would be attributed `inventor_edited` rather than
   `reused_statement:<rec_N>`. Truthfulness is preserved (the stored
   rationale is exactly what the inventor submitted); only the attribution
   granularity is affected. Future hardening observation: normalize line
   endings before the reuse comparison.

3. **Mutable confirmation-list reference.** `IdeaState.criticality_confirmations`
   is a plain list attribute; callers could in principle mutate it directly,
   bypassing the guarded recorder (the records themselves are frozen
   dataclasses). All committed call sites go through the recorder. Future
   hardening observation: expose a read-only accessor mirroring
   `get_assertions()`.

4. **Minimal form-field-name pinning in journey tests.** G-tests locate the
   confirmation surface via the `focus_token` / `rationale` form-field names,
   which are implementation-chosen rather than contract-pinned. Future
   hardening observation: introduce a stable test-hook marker if the surface
   is ever redesigned.
