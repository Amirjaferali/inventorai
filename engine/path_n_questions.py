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

Prohibited behaviors:
- No mutation of any artifact or its metadata.
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
    reverse-looked-up from ``text`` (D4.4)."""

    question_id: str
    text: str
    design_gap_id: str


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
    return ServedQuestion(question_id=question_id, text=text, design_gap_id=gap_type)


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
