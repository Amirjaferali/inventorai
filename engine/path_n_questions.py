"""Path N approved question content loader — domain-neutral canonical seam.

Authorization: PHASE_2_PATH_N_CONTENT_SELECTION_AUTHORIZATION.md (b3a5fba) §5;
domain-neutral remediation: DGMPR_D3_PATH_N_DOMAIN_NEUTRAL_SERVICE_CONTRACT.md
(D-GMPR-D3-PN — the D-GMPR-01-D-D3 lane's own gate).

Purpose : Load and serve approved Path N question content per domain. Nothing else.
Input   : gap_type (str), iterations_open (int), optional canonical domain identity.
Output  : question text (str) / ServedQuestion, or None if the gap_type has no
          Path N mapping (§8 fallthrough) or the domain has no committed artifact
          (fail-safe: the caller's existing generic fallthrough governs).
Source  : docs/governance/path_n_content_config/<domain>_path_n_questions.json —
          READ-ONLY committed artifacts resolved through the EXPLICIT BOUNDED
          domain→artifact mapping below (D-GMPR-D3-PN §2: a raw domain string is
          NEVER used as a filesystem path component; only canonical keys of the
          mapping resolve — unmapped/unknown/traversal-shaped identities → None).
          Electronics artifact location pinned by 806a3c6 / 26fa3e1 (byte-frozen);
          mechanical artifact is the D-GMPR-D3-PN verbatim projection of the
          I5-proven pack questions.

RVR-7 language boundary (authoritative path manifest freeze, PR #588): a record now
carries BOTH committed surfaces, but ``get_path_n_question`` and every engine caller
keep consuming the English ``text`` alone. Language selection happens at the render
edge from an already-resolved semantic identity — never here, never in progression,
and never by translating or reverse-looking-up text.

Prohibited behaviors:
- No mutation of any artifact or its metadata.
- No runtime/machine translation, and no language parameter on this seam.
- No fallback to Path T content or another domain's artifact on partial data —
  fail loudly, per artifact, without poisoning another domain's cache.
- No AI calls.
- No caching beyond per-domain load-once.
"""

import json
from dataclasses import dataclass
from pathlib import Path

# Electronics remains the backward-compatible default owner for ``domain=None``
# (existing callers unchanged); it is one mapped domain among several — NOT a
# shared-core assumption that Electronics is the only possible domain (D3-B).
_ELECTRONICS_DOMAIN = "electronics_electrical"

_ARTIFACT_DIR = (
    Path(__file__).resolve().parent.parent
    / "docs" / "governance" / "path_n_content_config"
)

# D-GMPR-D3-PN §2 — the EXPLICIT BOUNDED domain→artifact mapping. Committed
# artifacts only; adding a domain here is a governed content gate, never a
# runtime discovery. Raw domain strings never reach the filesystem: resolution
# happens ONLY through exact keys of this mapping.
_DOMAIN_ARTIFACTS = {
    _ELECTRONICS_DOMAIN: _ARTIFACT_DIR / "electronics_electrical_path_n_questions.json",
    "mechanical": _ARTIFACT_DIR / "mechanical_path_n_questions.json",
}

# Per-domain load-once caches. Populated only on a fully successful load, so a
# malformed artifact fails loudly WITHOUT poisoning any other domain's cache.
_PATH_N_GAPS: dict[str, dict] = {}


def _load_content(domain_key: str) -> dict:
    """Per-domain load-once, read-only. Fails loudly on missing/malformed artifact."""
    if domain_key not in _PATH_N_GAPS:
        artifact_path = _DOMAIN_ARTIFACTS[domain_key]
        if not artifact_path.exists():
            raise FileNotFoundError(
                f"Path N approved artifact not found: {artifact_path}"
            )
        with open(artifact_path, encoding="utf-8") as f:
            data = json.load(f)
        gaps = data.get("gaps")
        if not isinstance(gaps, dict) or not gaps:
            raise ValueError(
                f"Path N artifact malformed for {domain_key!r}: top-level 'gaps' "
                "mapping missing or empty — no fallback permitted (b3a5fba §5)"
            )
        _PATH_N_GAPS[domain_key] = gaps
    return _PATH_N_GAPS[domain_key]


@dataclass(frozen=True)
class ServedQuestion:
    """Immutable served-question identity (WS11 D4).

    ``question_id``, ``text``, and ``design_gap_id`` are read atomically from the
    SAME committed question entry (the entry at the deterministic index under its
    ``design_gap_id`` parent key), so identity, text, and design-gap always
    describe one physical record. ``question_id`` is NEVER reconstructed, inferred,
    derived, parsed, hashed, normalized, translated, fuzzy-matched, or
    reverse-looked-up from ``text`` (D4.4).

    RVR-7 (authoritative path manifest freeze, PR #588): ``text_ar`` is the
    ADDITIVE committed Arabic variant of the SAME record — same ``question_id``,
    same ``design_gap_id``, read atomically from the SAME entry in the SAME read.
    It is display content only: ``text`` remains the canonical English surface
    that every engine caller consumes, so no language signal reaches progression.
    ``None`` when the record commits no Arabic variant; the render edge then falls
    back to ``text`` deterministically — it is the RVR-7 evidence gate, not the
    runtime, that fails when a required Arabic variant is absent."""

    question_id: str
    text: str
    design_gap_id: str
    text_ar: "str | None" = None


def get_served_question(gap_type: str, iterations_open: int,
                        domain: "str | None" = None) -> "ServedQuestion | None":
    """Return the atomically-bound approved Path N ServedQuestion for gap_type
    (WS11 D4), or None if gap_type has no Path N mapping (the §8 Stage 3
    fallthrough). Reads the domain's committed artifact read-only (per-domain
    load-once) and fails loudly with no fallback on a malformed committed entry
    (b3a5fba §5). The ServedQuestion's three fields come from one entry in a
    single read.

    D-GMPR-D3-PN (domain-neutral canonical seam): the ``domain`` identity selects
    the domain's OWN committed artifact via the explicit bounded mapping.
    ``None`` keeps the backward-compatible Electronics default (existing callers
    unchanged, byte-identical service). A domain with NO committed artifact —
    recognized-but-artifact-less (e.g. software/medical_device today), unknown,
    or any non-canonical string — receives ``None`` so the caller's existing
    fallthrough governs and the canonical per-domain Domain-Pack question
    ownership remains authoritative (no parallel question framework/registry;
    no cross-domain content service is possible by construction)."""
    domain_key = _ELECTRONICS_DOMAIN if domain is None else domain
    if domain_key not in _DOMAIN_ARTIFACTS:
        return None
    gaps = _load_content(domain_key)
    variants = gaps.get(gap_type)
    if not variants:
        return None
    index = min(iterations_open, len(variants) - 1)
    entry = variants[index]
    if not isinstance(entry, dict):
        raise ValueError(
            f"Path N artifact entry for {gap_type}[{index}] is malformed — "
            "failing loudly, no fallback (b3a5fba §5)"
        )
    text = entry.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError(
            f"Path N artifact entry for {gap_type}[{index}] has no usable "
            "'text' — failing loudly, no fallback (b3a5fba §5)"
        )
    question_id = entry.get("question_id")
    if not isinstance(question_id, str) or not question_id.strip():
        raise ValueError(
            f"Path N artifact entry for {gap_type}[{index}] has no usable "
            "'question_id' — failing loudly, no fallback (b3a5fba §5)"
        )
    # RVR-7: the committed Arabic variant of the SAME entry, read in the SAME
    # single read as identity/text/design-gap. Absent, non-string or blank ->
    # None (English stays the deterministic fallback). Never fabricated, never
    # derived from ``text``, never translated at runtime.
    text_ar = entry.get("text_ar")
    if not isinstance(text_ar, str) or not text_ar.strip():
        text_ar = None
    return ServedQuestion(question_id=question_id, text=text,
                          design_gap_id=gap_type, text_ar=text_ar)


def get_served_question_by_id(gap_type: str, question_id: str,
                              domain: "str | None" = None) -> "ServedQuestion | None":
    """FORWARD identity -> record lookup: the committed ServedQuestion of this gap
    whose ``question_id`` equals the one supplied, or None.

    RVR-7 render-edge support (PR #588). The direction is identity -> content and
    never the reverse: ``question_id`` is an INPUT here, supplied by a caller that
    already holds it (e.g. the W2-C serving decision), so nothing is inferred,
    parsed, translated, fuzzy-matched or reverse-looked-up from ``text`` (D4.4).
    Walks the gap's committed variants in artifact order through the same
    ``get_served_question`` seam — no second reader, no second truth source, no
    new caching. Returns None for an unmapped gap/domain or an unknown id."""
    if not isinstance(question_id, str) or not question_id.strip():
        return None
    index = 0
    previous_id = None
    while True:
        served = get_served_question(gap_type, index, domain=domain)
        if served is None:
            return None
        if served.question_id == question_id:
            return served
        if served.question_id == previous_id:
            return None          # clamp reached — the id is not in this gap
        previous_id = served.question_id
        index += 1


def get_path_n_question(gap_type: str, iterations_open: int,
                        domain: "str | None" = None) -> str | None:
    """Backward-compatible text accessor (WS11 D4.3): returns the served
    question's text for gap_type, or None if unmapped. This is a thin wrapper over
    ``get_served_question`` and is no longer an independent question-identity
    source. Its return contract (text | None; fail-loud on unusable text) is
    unchanged. The optional canonical ``domain`` identity is threaded through to
    the domain-aware selection seam (default ``None`` = Electronics-compatible
    existing behavior)."""
    served = get_served_question(gap_type, iterations_open, domain=domain)
    return served.text if served is not None else None
