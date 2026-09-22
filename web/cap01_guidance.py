"""Stage 18 / CAP-01 — the bounded CAP-01 presentation-profile resolver.

Gate: the Owner-authorized FIRST bounded Stage-18 / CAP-01 guidance increment
(contract in ACTIVE_INCREMENT_CONTRACT.md).

Purpose
  The ONE place that answers "does an AUTHORIZED CAP-01 guidance profile exist
  for this canonical domain, and which copy keys does it render?". It owns
  capability AVAILABILITY and profile STRUCTURE. It owns no text: every string
  stays in ``web/ui_text.py``, and this module only names the stable keys that
  catalogue resolves. Availability is not translation, which is why the two do
  not share a module.

Input contract
  * ``profile_for_domain(domain_id)`` / ``profile_copy(domain_id)`` — ``domain_id``
    is a TRUSTED, server-resolved canonical domain identifier (``state.domain`` /
    ``state.domain_signal`` / a package ``capability_id`` derived from them),
    never request, query, form or free-text input.
  * ``profiles_for_package(package)`` — an already-assembled deliverable package.
    It is read, never mutated, and nothing is derived that the assembler did not
    already decide.

Output contract
  Copy KEYS only, never resolved text, so the caller renders through the existing
  ``ui_text.text`` / ``t()`` / ``ui_lang`` seam and exactly ONE language can reach
  a reader. Every function is pure and never raises, so it is safe on any
  template path.

Boundaries
  * Presentation only. It activates no domain, classifies no text, infers no
    concept-class membership, changes no deterministic evaluation, and owns no
    evidence, risk, assumption, contradiction, readiness or gap truth.
  * DOMAIN ACTIVATION IS NOT CAP-01 PROFILE AVAILABILITY. A domain can be fully
    activated and still have no CAP-01 profile — ``mechanical`` is exactly that
    case today. "No profile" means ONLY *no domain-specific CAP-01 guidance
    profile is authorized yet*. It NEVER means unsupported, invalid,
    not-activated, failed or incomplete, and nothing here may drive an
    unsupported-domain message.
  * CAP-01 is a GUIDANCE owner, not a technical-production owner. It absorbs no
    responsibility from CAP-04, CAP-06, CAP-07, CAP-08, CAP-09, CAP-10, CAP-11,
    CAP-12, CAP-13, CAP-14, THERM-01, WS-PFV-001 or the shared Technical
    Realization layer (roadmap §8C, invariants A–C and I).
  * This first slice is presentation-only and class-general. It is a FIRST
    increment, not CAP-01's ceiling, and not its permanent architecture
    (invariants D and H).
  * No plugin framework, no generic capability registry, no unused future row.
"""
from web import ui_text

# The domain -> AUTHORIZED CAP-01 guidance-profile table: the ONLY place a CAP-01
# domain literal lives. The deterministic core (progression_loop / idea_state /
# domain_rules / domain_activation / semantic_registry / requirement_landscape /
# validation_plan) carries no CAP-01 vocabulary and needs NO change to gain a
# future profile — a separately-authorized profile is ONE row here plus its own
# ``UI_<profile id>_*`` copy keys in the catalogue. There is deliberately no
# permanent ``if electronics / elif mechanical`` chain anywhere.
CAP01_PROFILE_BY_DOMAIN = {
    "electronics_electrical": "CAP01_ELECTRONICS_INTERFACE_V1",
}

# The copy parts every CAP-01 profile supplies, mapped to the view key the caller
# reads. Item keys are discovered by the ``_ITEM_<n>`` convention instead of being
# listed, so a future profile picks its own item count with no code change here.
_COPY_PARTS = {
    "title_key":    "TITLE",
    "intro_key":    "INTRO",
    "boundary_key": "BOUNDARY",
    "limit_key":    "LIMIT",
    "evidence_key": "EVIDENCE",
}

# Where the canonical, already-assembled domain rows live. Read as a COLLECTION,
# deliberately: today the assembler emits exactly one capability, but that is a
# CURRENT RUNTIME LIMITATION, not the CAP-01 domain model (invariant F). Reading
# ``[0]`` would harden today's shape into the architecture and force a rewrite
# the day a package legitimately carries more than one canonical domain.
_SECTION = "section_3_assessment_overview"
_ROWS = "capabilities_assessed"


def profile_for_domain(domain_id):
    """The AUTHORIZED CAP-01 guidance-profile id for a trusted canonical domain
    id, or ``None`` when no CAP-01 profile is authorized for it.

    Pure and data-driven: it reads the table above and nothing else. ``None``
    means "no CAP-01 profile authorized yet", never "unsupported domain"."""
    if isinstance(domain_id, str):
        return CAP01_PROFILE_BY_DOMAIN.get(domain_id.strip())
    return None


def profile_copy(domain_id):
    """The CAP-01 copy KEYS to render for a trusted canonical domain id, or
    ``None`` when no authorized profile exists for it (or its copy is incomplete).

    Returns a fresh dict of catalogue keys — ``profile_id``, the five part keys
    and an ordered ``item_keys`` tuple. Never text. An incomplete profile fails
    closed rather than rendering half a block, and ``None`` is a silent
    no-render, not an unsupported-domain signal."""
    profile_id = profile_for_domain(domain_id)
    if profile_id is None:
        return None
    prefix = "UI_" + profile_id + "_"
    view = {name: prefix + part for name, part in _COPY_PARTS.items()}
    if not all(ui_text.has_string(key) for key in view.values()):
        return None
    item_keys = []
    while ui_text.has_string(prefix + "ITEM_%d" % (len(item_keys) + 1)):
        item_keys.append(prefix + "ITEM_%d" % (len(item_keys) + 1))
    if not item_keys:
        return None
    view["profile_id"] = profile_id
    view["item_keys"] = tuple(item_keys)
    return view


def _rows(package):
    """The canonical capability rows of an assembled package, as a tuple.

    Defensive by design: a package shape this does not recognise yields no rows
    and therefore no CAP-01 block, which is the safe outcome on a template path."""
    try:
        rows = package[_SECTION][_ROWS]
    except (TypeError, KeyError, IndexError):
        return ()
    if not isinstance(rows, (list, tuple)):
        return ()
    return tuple(row for row in rows if isinstance(row, dict))


def profiles_for_package(package):
    """Zero or more authorized CAP-01 presentation profiles for an assembled
    package, in source order, deduplicated by profile.

    Three separate facts decide, all of them already canonical in the package and
    none of them derived here: the capability row's trusted ``capability_id``,
    whether an AUTHORIZED CAP-01 profile exists for it, and whether that row
    still reports at least one unresolved/open gap. A row failing any of the
    three contributes nothing, and a package whose domains have no authorized
    profile yields an empty tuple — which renders nothing and says nothing about
    those domains' support.

    Consuming the rows as a COLLECTION is the forward-compatible part. It is not
    a claim that the runtime supports multiple domains today: it does not, the
    assembler emits one row, and nothing here creates multi-domain truth,
    infers subsystem membership or activates anything. It only means that the day
    a package legitimately carries more than one canonical domain, this resolver
    extends rather than needing replacement."""
    seen, profiles = set(), []
    for row in _rows(package):
        if not row.get("gaps_open"):
            continue
        view = profile_copy(row.get("capability_id"))
        if view is None or view["profile_id"] in seen:
            continue
        seen.add(view["profile_id"])
        profiles.append(view)
    return tuple(profiles)
