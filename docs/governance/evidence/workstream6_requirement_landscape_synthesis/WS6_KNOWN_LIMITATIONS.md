# WS6 Evidence — Known Limitations (honest record; none repaired here)

L1 — Linear template lookup. The Section 13 template locates a statement's
metadata group by scanning statement_groups linearly inside the member loop
(O(groups x members)). Classification: NON-BLOCKING performance
observation. Acceptable because real landscapes are bounded (tens of rows;
the canonical journey has 13 rows / 6 groups) and rendering is
request-scoped; no optimization is authorized in this gate.

L2 — Wide metadata discriminator. Each statement group mirrors six public
row fields to enforce exact same-metadata-group separation (D1).
Classification: OBSERVATION, not an error. Possible future hardening: an
opaque group key. Recorded only.

L3 — Multiple empty-content rows. Two or more empty-content records with
identical metadata would group and render "This statement was recorded N
times during the session." for the placeholder statement itself.
Classification: KNOWN UX LIMITATION / NOT CURRENTLY DEMONSTRATED IN THE
CANONICAL JOURNEY. Not concealed; not repaired in this gate.

L4 — Empty-content resolving action. The empty-content row's statement uses
the new insufficiency wording while its resolving action remains the legacy
"Validate the recorded answer against the available evidence." (D7
authorized only the statement wording). Classification: KNOWN WORDING
LIMITATION / OUTSIDE D7 AUTHORIZATION. Not concealed; not repaired here.

L5 — Cosmetic focused-test naming. The focused P2 test name ends
"..._exactly_once_or_more" while its assertion is strictly == 1 (the
correct, stricter form). Classification: COSMETIC ONLY.
