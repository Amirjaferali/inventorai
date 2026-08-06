"""Path N approved question content loader.

Authorization: PHASE_2_PATH_N_CONTENT_SELECTION_AUTHORIZATION.md (b3a5fba) §5.

Purpose : Load and serve approved Path N question content. Nothing else.
Input   : gap_type (str), iterations_open (int).
Output  : question text (str), or None if gap_type has no Path N mapping.
          None for Stage 3 gap types is the explicit §8 fallthrough.
          None for a Stage 2 gap type must not occur (§11 STOP condition 3).
Source  : docs/governance/path_n_content_config/
          electronics_electrical_path_n_questions.json — READ-ONLY,
          committed location pinned by 806a3c6 / 26fa3e1.

Prohibited behaviors:
- No mutation of the artifact or its metadata.
- No fallback to Path T content on partial data — fail loudly.
- No AI calls.
- No caching beyond load-once.
"""

import json
from dataclasses import dataclass
from pathlib import Path

_ARTIFACT_PATH = (
    Path(__file__).resolve().parent.parent
    / "docs" / "governance" / "path_n_content_config"
    / "electronics_electrical_path_n_questions.json"
)

_PATH_N_GAPS: dict | None = None


def _load_content() -> dict:
    """Load-once, read-only. Fails loudly on missing/malformed artifact."""
    global _PATH_N_GAPS
    if _PATH_N_GAPS is None:
        if not _ARTIFACT_PATH.exists():
            raise FileNotFoundError(
                f"Path N approved artifact not found: {_ARTIFACT_PATH}"
            )
        with open(_ARTIFACT_PATH, encoding="utf-8") as f:
            data = json.load(f)
        gaps = data.get("gaps")
        if not isinstance(gaps, dict) or not gaps:
            raise ValueError(
                "Path N artifact malformed: top-level 'gaps' mapping "
                "missing or empty — no fallback permitted (b3a5fba §5)"
            )
        _PATH_N_GAPS = gaps
    return _PATH_N_GAPS


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


def get_served_question(gap_type: str, iterations_open: int) -> "ServedQuestion | None":
    """Return the atomically-bound approved Path N ServedQuestion for gap_type
    (WS11 D4), or None if gap_type has no Path N mapping (the §8 Stage 3
    fallthrough). Reads the committed artifact read-only (load-once) and fails
    loudly with no fallback on a malformed committed entry (b3a5fba §5). The
    ServedQuestion's three fields come from one entry in a single read."""
    gaps = _load_content()
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


def get_path_n_question(gap_type: str, iterations_open: int) -> str | None:
    """Backward-compatible text accessor (WS11 D4.3): returns the served
    question's text for gap_type, or None if unmapped. This is a thin wrapper over
    ``get_served_question`` and is no longer an independent question-identity
    source. Its return contract (text | None; fail-loud on unusable text) is
    unchanged."""
    served = get_served_question(gap_type, iterations_open)
    return served.text if served is not None else None
