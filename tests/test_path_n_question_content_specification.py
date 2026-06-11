"""Validation tests for the Path N question content specification artifact.

These tests inspect only the Path N specification markdown file.
They do not read domain packs, do not import web frameworks, do not run sessions,
and do not modify any file.
"""

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = REPO_ROOT / "docs" / "governance" / "PATH_N_QUESTION_CONTENT_SPECIFICATION.md"

EXPECTED_IDS = [
    "N-MC-1", "N-MC-2", "N-MC-3", "N-MC-4",
    "N-PF-1", "N-PF-2", "N-PF-3", "N-PF-4",
    "N-BA-1", "N-BA-2", "N-BA-3",
]

DISALLOWED_TERM_PATTERNS = {
    "voltage": r"\bvoltage\b",
    "current": r"\bcurrent\b",
    "frequency": r"\bfrequency\b",
    "circuit architecture": r"\bcircuit architecture\b",
    "component-level selection": r"\bcomponent-level selection\b",
    "signal transformation": r"\bsignal transformation\b",
    "datasheet": r"\bdatasheet\b",
    "calculation": r"\bcalculation\b",
    "manufacturing tolerance": r"\bmanufacturing tolerance\b",
    "electrical constraints": r"\belectrical constraints\b",
}

R1_REGRESSION_PATTERNS = {
    "electronic circuit achieves": r"\belectronic circuit achieves\b",
    "electronic components": r"\belectronic components\b",
    "signal or energy transformation": r"\bsignal or energy transformation\b",
    "voltage/current/frequency": r"\bvoltage/current/frequency\b",
    "electrical constraints": r"\belectrical constraints\b",
}

KNOWN_UNKNOWN_PATTERNS = [
    r"\bunsure\b",
    r"what information would you need",
    r"what do you not know|what don't you know|don't know yet",
    r"ask (?:them|an engineer) to check",
]

_ID_LINE = re.compile(
    r'^\s*\|?\s*(N-(?:MC|PF|BA)-\d+)\s*(?:\||:)\s*(.*?)\s*\|?\s*$'
)


def load_spec_text() -> str:
    assert SPEC_PATH.exists(), f"specification not found: {SPEC_PATH}"
    text = SPEC_PATH.read_text(encoding="utf-8")
    assert text.strip(), "specification file is empty"
    return text


def extract_question_lines(text: str) -> dict[str, str]:
    questions: dict[str, str] = {}

    for line in text.splitlines():
        match = _ID_LINE.match(line)
        if not match:
            continue

        question_id, raw_text = match.group(1), match.group(2)
        question_text = raw_text.rstrip("|").strip().lstrip(":").strip().strip('"').strip()

        if question_text:
            questions[question_id] = question_text

    return questions


def test_spec_exists_and_readable():
    text = load_spec_text()
    assert len(text) > 100, "specification suspiciously short"


def test_all_path_n_ids_present():
    text = load_spec_text()
    missing = [question_id for question_id in EXPECTED_IDS if question_id not in text]
    assert not missing, f"missing Path N question IDs: {missing}"


def test_extraction_scoped_to_question_lines():
    questions = extract_question_lines(load_spec_text())

    assert set(questions) == set(EXPECTED_IDS), (
        f"extracted IDs {sorted(questions)} != expected {sorted(EXPECTED_IDS)}"
    )

    extracted_blob = " ".join(questions.values()).lower()
    assert "describe how your electronic circuit" not in extracted_blob, (
        "extraction leaked technical-contrast content from explanatory sections"
    )


def test_no_disallowed_terms_in_path_n_questions():
    questions = extract_question_lines(load_spec_text())
    violations = {}

    for question_id, question_text in questions.items():
        hits = [
            term
            for term, pattern in DISALLOWED_TERM_PATTERNS.items()
            if re.search(pattern, question_text, re.IGNORECASE)
        ]
        if hits:
            violations[question_id] = hits

    assert not violations, f"disallowed early-gate terms in Path N questions: {violations}"


def test_word_boundary_no_false_positive():
    assert not re.search(
        DISALLOWED_TERM_PATTERNS["current"],
        "Is the system currently working?",
        re.IGNORECASE,
    ), "word-boundary regex false-positives on 'currently'"

    assert re.search(
        DISALLOWED_TERM_PATTERNS["current"],
        "What current does it draw?",
        re.IGNORECASE,
    ), "word-boundary regex fails to match real 'current'"


def test_known_unknown_language_present():
    questions = extract_question_lines(load_spec_text())
    extracted_blob = " ".join(questions.values())

    matched = [
        pattern
        for pattern in KNOWN_UNKNOWN_PATTERNS
        if re.search(pattern, extracted_blob, re.IGNORECASE)
    ]

    assert len(matched) >= 2, (
        "insufficient known-unknown language in Path N questions; "
        f"matched only: {matched}"
    )


def test_r1_regression_markers_absent():
    questions = extract_question_lines(load_spec_text())
    violations = {}

    for question_id, question_text in questions.items():
        hits = [
            marker
            for marker, pattern in R1_REGRESSION_PATTERNS.items()
            if re.search(pattern, question_text, re.IGNORECASE)
        ]
        if hits:
            violations[question_id] = hits

    assert not violations, f"R1 regression markers found in Path N questions: {violations}"


def test_no_runtime_or_domain_dependency():
    source = Path(__file__).read_text(encoding="utf-8")
    body = source.split("def test_no_runtime_or_domain_dependency", 1)[0]

    assert "import flask" not in body.lower(), "test module imports web framework"
    assert "domain.json" not in body, "test module references domain pack file"
    assert "start_ilt002" not in body, "test module references session routes"
    assert "app.run" not in body, "test module starts the app"
