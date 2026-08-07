"""P6-1 — Truthful Domain Labeling Foundation: the single central public label resolver.

Gate G-P6-1-TRUTHFUL-DOMAIN-LABELING-FOUNDATION-IMPLEMENTATION-01 (Option A;
contract in ACTIVE_INCREMENT_CONTRACT.md). The ONE source of truth that maps a
TRUSTED, server-resolved runtime domain identifier to a bilingual (English/Arabic)
public label for user-facing surfaces.

Boundaries (contract §4 / §10; D-P6-02 / D-P6-07):
  * Presentation only — it activates no domain, changes no deterministic
    evaluation, and reads NO client-provided text. Callers pass the trusted
    server value (``state.domain`` / ``state.domain_signal`` / a package
    ``capability_id`` derived from them), never request/query/form input.
  * Only the RUNTIME-OPERATED domain (``electronics_electrical``) has a Tier-1
    public label. Every other value — missing, None, unknown, invalid, or an
    unsupported/non-runtime pack id (mechanical / medical_device / software /
    iot_electronics) — resolves to the neutral Tier-0 "General idea review"
    fallback and NEVER silently to electronics.
  * Tier 0-1 only. No Tier-2/3/4 wording ("Specialist", "Expert", "Professional",
    "Certified", "Licensed", ...) is ever produced.
"""

# Tier-1 public labels — keyed by RUNTIME-OPERATED domain id only.
_PUBLIC_DOMAIN_LABELS = {
    "electronics_electrical": {
        "en": "Electronics-informed review",
        "ar": "مراجعة مستنيرة بمجال الإلكترونيات",
    },
}

# Tier-0 neutral fallback for missing / unknown / invalid / unsupported state.
_GENERAL_LABEL = {"en": "General idea review", "ar": "مراجعة عامة للفكرة"}


def public_domain_label(domain_id):
    """Return a fresh ``{"en": ..., "ar": ...}`` dict for a TRUSTED runtime domain
    id. An unmapped / non-string / blank / unsupported id returns the General
    fallback — never electronics. Never raises (safe in any template path)."""
    if isinstance(domain_id, str):
        entry = _PUBLIC_DOMAIN_LABELS.get(domain_id.strip())
        if entry is not None:
            return dict(entry)
    return dict(_GENERAL_LABEL)


def is_general_fallback(label):
    """True when ``label`` is the neutral General fallback (both languages)."""
    return (label or {}).get("en") == _GENERAL_LABEL["en"]
