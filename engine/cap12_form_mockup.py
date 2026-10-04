"""Stage 24 / CAP-12 - Form Mock-up Advisory - Slice 1: the pure advisory resolver.

Gate: the Owner-authorized bounded CAP-12 Slice 1 (recorded in
docs/governance/ACTIVE_INCREMENT_CONTRACT.md). It is ONE optional, advisory,
non-binding capability: for ONE explicitly declared NON-FUNCTIONAL form mock-up
component it lists the prototype material families and building-method families
that NASA material describes for early mock-up work, or it declines.

Input contract
  * ``resolve_advisory(root_domain, role_category, artifact=None)``.
    ``root_domain`` is the TRUSTED, server-resolved project root domain (the
    durable, immutable ``confirmed_domain``), never request input.
    ``role_category`` is the one closed token the Owner selected. NOTHING ELSE
    is an input: the Owner's component name and function are request-local
    display text owned by the web layer and are never passed here, so no
    keyword, text, classifier or model signal can reach the selection.

Output contract
  A plain ``dict`` with ``state`` exactly ``AVAILABLE`` or ``UNABLE_TO_RECOMMEND``.
  An unable result carries one closed ``reason`` token and no content. It never
  falls back to generic advice.

Boundaries
  * Pure and deterministic: no persistence, no mutation, no network, no
    provider or model, no clock. The only read is the committed governed
    artifact below.
  * Knowledge is CAP-12-owned. It lives in ONE artifact and is NOT a Domain Pack
    (``domains/``), is not in ``domains/domain_provenance.json`` and is not
    Manufacturing Evidence, Requirement Quantity or CAP-01 truth. Domain Packs
    are referenced by id only through the applicability key.
  * Family level only. The artifact and its validator admit no grade, subtype,
    brand, dimension, rating or suitability field: unknown keys are refused.
  * It writes no evidence and has no readiness, progression, gap, report,
    export or Structured Export effect. It is not CAP-13 (no thickness, load,
    stress, sizing, tolerance or specification), not CAP-14 (no image input)
    and not WS-PFV-001 (no validation, result interpretation or verdict).
"""
import copy
import json
import re
from pathlib import Path

ROLE_FORM_MOCKUP = "form_mockup"
ROLE_CATEGORIES = (ROLE_FORM_MOCKUP,)

# The ONLY applicable (trusted root domain, role category) pair in Slice 1.
SUPPORTED_APPLICABILITY = (("mechanical", ROLE_FORM_MOCKUP),)

STATE_AVAILABLE = "AVAILABLE"
STATE_UNABLE = "UNABLE_TO_RECOMMEND"

REASON_NO_CATEGORY = "NO_CATEGORY"
REASON_INVALID_CATEGORY = "INVALID_CATEGORY"
REASON_UNSUPPORTED_DOMAIN = "UNSUPPORTED_DOMAIN"
REASON_APPLICABILITY_NOT_ESTABLISHED = "APPLICABILITY_NOT_ESTABLISHED"
REASON_KNOWLEDGE_UNAVAILABLE = "KNOWLEDGE_UNAVAILABLE"
REASON_INSUFFICIENT_ALTERNATIVES = "INSUFFICIENT_ALTERNATIVES"
UNABLE_REASONS = (
    REASON_NO_CATEGORY, REASON_INVALID_CATEGORY, REASON_UNSUPPORTED_DOMAIN,
    REASON_APPLICABILITY_NOT_ESTABLISHED, REASON_KNOWLEDGE_UNAVAILABLE,
    REASON_INSUFFICIENT_ALTERNATIVES,
)

ADVISORY_MATERIAL = "material_family"
ADVISORY_PROCESS = "process_family"
ADVISORY_LIMITATION = "limitation"
ADVISORY_TYPES = (ADVISORY_MATERIAL, ADVISORY_PROCESS, ADVISORY_LIMITATION)

# Closed FAMILY vocabularies (Slice 1). Families only: a grade, alloy, polymer
# subtype or brand is not a token and cannot become one without a separate
# authorization. Wood / MDF is deliberately absent.
MATERIAL_FAMILY_TOKENS = ("foam_core", "thermoplastic")
PROCESS_FAMILY_TOKENS = ("manual_cut_and_join", "additive_fff_fdm")

# A real advisory needs at least two independently source-qualified material
# alternatives; one option is never presented as a recommendation.
MIN_MATERIAL_ALTERNATIVES = 2

ARTIFACT_ID = "cap12_form_mockup_advisory"
ARTIFACT_SCHEMA_VERSION = "1.0"
ARTIFACT_PATH = (Path(__file__).resolve().parent.parent / "docs" / "governance"
                 / "cap12_content_config" / "form_mockup_advisory_v1.json")

_MAX_TEXT = 700
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
# Provenance narrative fields (governance note, inspected content) may be longer
# than a product-facing claim, which stays tightly bounded.
_MAX_LONG_TEXT = 2000
_LONG_FIELDS = frozenset({"governance_note", "inspected_content"})

_TOP_KEYS = frozenset({
    "artifact_id", "schema_version", "artifact_version", "owner", "slice",
    "governance_note", "scope", "sources", "claims"})
_SCOPE_KEYS = frozenset({"role_category", "applicable_domain"})
_SOURCE_KEYS = frozenset({
    "record_id", "record_type", "source_type", "publisher", "report_number",
    "ntrs_document_id", "source_title", "url", "inspected_location",
    "distribution", "copyright_status", "source_use_policy_ref",
    "inspection_basis", "inspection_date", "inspected_content",
    "supports_claim_ids", "paraphrase_only_limitation",
    "third_party_material_exclusion", "no_endorsement_limitation"})
_POLICY_EXTRA_KEYS = frozenset({"acknowledgement"})
_CLAIM_KEYS = frozenset({
    "claim_id", "advisory_type", "role_category", "applicable_domain",
    "family_token", "fact", "process_family_refs", "source_ref",
    "source_use_policy_ref", "limitation"})
_SOURCE_TEXT_FIELDS = (
    "record_id", "source_type", "publisher", "source_title",
    "inspected_location", "distribution", "copyright_status",
    "source_use_policy_ref", "inspection_basis", "inspection_date",
    "inspected_content", "paraphrase_only_limitation",
    "third_party_material_exclusion", "no_endorsement_limitation")
_SOURCE_OPTIONAL_TEXT = ("report_number", "ntrs_document_id", "url")


class Cap12KnowledgeError(ValueError):
    """The governed CAP-12 artifact is missing, unreadable or not valid. The
    resolver turns this into ``KNOWLEDGE_UNAVAILABLE``: never partial advice and
    never a generic fallback. The message names structure only, never content."""


def supports(root_domain, role_category=ROLE_FORM_MOCKUP):
    """True iff ``(root_domain, role_category)`` is an applicable pair. Pure;
    non-strings are never applicable."""
    if not isinstance(root_domain, str) or not isinstance(role_category, str):
        return False
    return (root_domain, role_category) in SUPPORTED_APPLICABILITY


def _text(value, field, allow_none=False):
    if value is None and allow_none:
        return
    limit = _MAX_LONG_TEXT if field in _LONG_FIELDS else _MAX_TEXT
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise Cap12KnowledgeError("%s: not a bounded non-empty string" % field)


def _validate_sources(sources):
    if not isinstance(sources, list) or not sources:
        raise Cap12KnowledgeError("sources: missing")
    by_id = {}
    for record in sources:
        if not isinstance(record, dict):
            raise Cap12KnowledgeError("sources: not an object")
        record_type = record.get("record_type")
        allowed = _SOURCE_KEYS | (_POLICY_EXTRA_KEYS
                                  if record_type == "source_use_policy"
                                  else frozenset())
        if set(record) != allowed:
            raise Cap12KnowledgeError("sources: unexpected or missing field")
        if record_type not in ("source", "source_use_policy"):
            raise Cap12KnowledgeError("sources: unknown record type")
        for field in _SOURCE_TEXT_FIELDS:
            _text(record[field], field)
        for field in _SOURCE_OPTIONAL_TEXT:
            _text(record[field], field, allow_none=True)
        if record_type == "source":
            # A source record must be traceable to the exact NASA report and
            # its record locator: a missing or blank URL invalidates the
            # artifact, so no advisory can render from it.
            _text(record["report_number"], "report_number")
            _text(record["ntrs_document_id"], "ntrs_document_id")
            _text(record["url"], "url")
        else:
            _text(record["acknowledgement"], "acknowledgement")
        if not _ISO_DATE.fullmatch(record["inspection_date"]):
            raise Cap12KnowledgeError("sources: inspection date malformed")
        if record["inspection_basis"] != "LEAD_SUPPLIED":
            raise Cap12KnowledgeError("sources: unknown inspection basis")
        ids = record["supports_claim_ids"]
        if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
            raise Cap12KnowledgeError("sources: supports_claim_ids malformed")
        if record["record_id"] in by_id:
            raise Cap12KnowledgeError("sources: duplicate record id")
        by_id[record["record_id"]] = record
    return by_id


def validate_artifact(data):
    """Validate the WHOLE artifact or raise ``Cap12KnowledgeError``. Structural
    and referential only: every claim resolves to an inspected source record and
    to its source-use record, the source lists the claim back, a material and
    its process pairing are directly evidenced by ONE source, and unknown keys
    (a grade, rating or suitability field) are refused. Returns ``data``."""
    if not isinstance(data, dict) or set(data) != _TOP_KEYS:
        raise Cap12KnowledgeError("artifact: unexpected or missing field")
    if data["artifact_id"] != ARTIFACT_ID \
            or data["schema_version"] != ARTIFACT_SCHEMA_VERSION:
        raise Cap12KnowledgeError("artifact: unknown identity or version")
    for field in ("artifact_version", "owner", "slice", "governance_note"):
        _text(data[field], field)
    scope = data["scope"]
    if not isinstance(scope, dict) or set(scope) != _SCOPE_KEYS \
            or (scope["applicable_domain"], scope["role_category"]) \
            not in SUPPORTED_APPLICABILITY:
        raise Cap12KnowledgeError("scope: not the supported applicability")
    sources = _validate_sources(data["sources"])
    claims = data["claims"]
    if not isinstance(claims, list) or not claims:
        raise Cap12KnowledgeError("claims: missing")
    by_id, seen_family = {}, set()
    for claim in claims:
        if not isinstance(claim, dict) or set(claim) != _CLAIM_KEYS:
            raise Cap12KnowledgeError("claims: unexpected or missing field")
        for field in ("claim_id", "fact", "limitation", "source_ref",
                      "source_use_policy_ref"):
            _text(claim[field], field)
        if claim["claim_id"] in by_id:
            raise Cap12KnowledgeError("claims: duplicate claim id")
        if claim["advisory_type"] not in ADVISORY_TYPES:
            raise Cap12KnowledgeError("claims: unknown advisory type")
        if claim["role_category"] != scope["role_category"] \
                or claim["applicable_domain"] != scope["applicable_domain"]:
            raise Cap12KnowledgeError("claims: outside the artifact scope")
        kind, token = claim["advisory_type"], claim["family_token"]
        allowed_tokens = {ADVISORY_MATERIAL: MATERIAL_FAMILY_TOKENS,
                          ADVISORY_PROCESS: PROCESS_FAMILY_TOKENS}.get(kind)
        if allowed_tokens is None:
            if token is not None:
                raise Cap12KnowledgeError("claims: limitation carries a family")
        else:
            if token not in allowed_tokens or (kind, token) in seen_family:
                raise Cap12KnowledgeError("claims: family token not admitted")
            seen_family.add((kind, token))
        refs = claim["process_family_refs"]
        if not isinstance(refs, list) or (kind != ADVISORY_MATERIAL and refs) \
                or any(r not in PROCESS_FAMILY_TOKENS for r in refs) \
                or len(set(refs)) != len(refs):
            raise Cap12KnowledgeError("claims: process relation malformed")
        source = sources.get(claim["source_ref"])
        if source is None or source["record_type"] != "source":
            raise Cap12KnowledgeError("claims: source record unresolved")
        policy = sources.get(claim["source_use_policy_ref"])
        if policy is None or policy["record_type"] != "source_use_policy" \
                or source["source_use_policy_ref"] != claim["source_use_policy_ref"]:
            raise Cap12KnowledgeError("claims: source-use record unresolved")
        if claim["claim_id"] not in source["supports_claim_ids"]:
            raise Cap12KnowledgeError("claims: source does not list the claim")
        by_id[claim["claim_id"]] = claim
    for source in sources.values():
        for claim_id in source["supports_claim_ids"]:
            claim = by_id.get(claim_id)
            if claim is None or claim["source_ref"] != source["record_id"]:
                raise Cap12KnowledgeError("sources: lists an unbound claim")
    process_by_token = {c["family_token"]: c for c in claims
                        if c["advisory_type"] == ADVISORY_PROCESS}
    for claim in claims:
        for ref in claim["process_family_refs"]:
            partner = process_by_token.get(ref)
            # A pairing is only implied when ONE inspected source directly
            # supports both halves; otherwise the artifact is refused.
            if partner is None or partner["source_ref"] != claim["source_ref"]:
                raise Cap12KnowledgeError("claims: pairing not directly evidenced")
    return data


def load_artifact(path=None):
    """Read and validate the committed artifact. Any failure raises
    ``Cap12KnowledgeError``. Reads a local file only."""
    target = Path(path) if path is not None else ARTIFACT_PATH
    try:
        with open(target, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        raise Cap12KnowledgeError("artifact: unreadable") from None
    return validate_artifact(data)


def _unable(reason):
    return {"state": STATE_UNABLE, "reason": reason}


def resolve_advisory(root_domain, role_category, artifact=None):
    """The ONE advisory decision. See the module docstring. Never raises.

    Order of refusal: category, then root domain, then knowledge. The result is
    composed only from the artifact's own claims, in artifact order, with no
    ranking, and carries deep copies so a caller can never alter governed truth.
    """
    if role_category is None or role_category == "":
        return _unable(REASON_NO_CATEGORY)
    if not isinstance(role_category, str) or role_category not in ROLE_CATEGORIES:
        return _unable(REASON_INVALID_CATEGORY)
    if not isinstance(root_domain, str) or not root_domain.strip():
        return _unable(REASON_APPLICABILITY_NOT_ESTABLISHED)
    if not supports(root_domain, role_category):
        return _unable(REASON_UNSUPPORTED_DOMAIN)
    try:
        data = load_artifact() if artifact is None else validate_artifact(artifact)
    except Cap12KnowledgeError:
        return _unable(REASON_KNOWLEDGE_UNAVAILABLE)
    claims = [c for c in data["claims"]
              if c["role_category"] == role_category
              and c["applicable_domain"] == root_domain]
    sources = {s["record_id"]: s for s in data["sources"]}
    boundary = [c for c in claims if c["advisory_type"] == ADVISORY_LIMITATION]
    process = {c["family_token"]: c for c in claims
               if c["advisory_type"] == ADVISORY_PROCESS}
    alternatives = []
    for claim in claims:
        if claim["advisory_type"] != ADVISORY_MATERIAL:
            continue
        paired = [process[r] for r in claim["process_family_refs"]
                  if r in process]
        if paired:
            alternatives.append({"family_token": claim["family_token"],
                                 "material": claim, "processes": paired})
    if not boundary or len(alternatives) < MIN_MATERIAL_ALTERNATIVES:
        return _unable(REASON_INSUFFICIENT_ALTERNATIVES)
    used, order = {}, []
    for claim in boundary + [c for alt in alternatives
                             for c in [alt["material"]] + alt["processes"]]:
        for ref in (claim["source_ref"], claim["source_use_policy_ref"]):
            if ref not in used:
                used[ref] = sources[ref]
                order.append(ref)
    result = {
        "state": STATE_AVAILABLE,
        "reason": None,
        "role_category": role_category,
        "root_domain": root_domain,
        "role_boundary": boundary[0],
        "alternatives": alternatives,
        "sources": [used[r] for r in order
                    if used[r]["record_type"] == "source"],
        "source_use_policy": next(used[r] for r in order
                                  if used[r]["record_type"]
                                  == "source_use_policy"),
    }
    return copy.deepcopy(result)
