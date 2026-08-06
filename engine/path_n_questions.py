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


def get_path_n_question(gap_type: str, iterations_open: int) -> str | None:
    """Return approved Path N question text for gap_type, or None if unmapped."""
    gaps = _load_content()
    variants = gaps.get(gap_type)
    if not variants:
        return None
    index = min(iterations_open, len(variants) - 1)
    entry = variants[index]
    text = entry.get("text") if isinstance(entry, dict) else None
    if not isinstance(text, str) or not text.strip():
        raise ValueError(
            f"Path N artifact entry for {gap_type}[{index}] has no usable "
            "'text' — failing loudly, no fallback (b3a5fba §5)"
        )
    return text
