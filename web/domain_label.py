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
  * A Tier-1 public label reflects truthful-labeling readiness, NOT runtime
    activation. ``electronics_electrical`` is both RUNTIME-OPERATED and
    Tier-1-labeled. ``mechanical`` is Tier-1-labeled per
    P9_MECHANICAL_DOMAIN_QUALIFICATION_CONTRACT.md §13 (Requirement 9) once
    Mechanical activation-readiness was reached, but is NOT runtime-activated —
    ``engine.domain_activation.activated_domains()`` stays ``['electronics_electrical']``
    (contract §16, Requirement 12: labeling never activates a domain). This
    resolver has no bearing on domain selectability; the ``/start`` domain
    picker is driven solely by ``activated_domains()`` (see ``web/app.py``),
    never by this dict. Every other value — missing, None, unknown, invalid,
    or an unsupported/non-qualified pack id (medical_device / software /
    iot_electronics) — resolves to the neutral Tier-0 "General idea review"
    fallback and NEVER silently to electronics or mechanical.
  * Tier 0-1 only. No Tier-2/3/4 wording ("Specialist", "Expert", "Professional",
    "Certified", "Licensed", ...) is ever produced.
"""

# Tier-1 public labels — keyed by domain id. Presence here means truthful-
# labeling readiness, NOT activation (see module docstring; contract §16).
_PUBLIC_DOMAIN_LABELS = {
    "electronics_electrical": {
        "en": "Electronics-informed review",
        "ar": "مراجعة مستنيرة بمجال الإلكترونيات",
    },
    "mechanical": {
        "en": "Mechanical-informed review",
        "ar": "مراجعة مستنيرة بمجال الميكانيكا",
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
