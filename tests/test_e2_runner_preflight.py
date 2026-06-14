"""
test_e2_runner_preflight.py

Isolated preflight tests for scripts/e2_path_n_smoke_runner.sh (Gate B, B-2).

Five tests: P-1 through P-5.
All run inside isolated tmp_path fixture repositories.

Fixture layout:
    tmp_path/
        remote.git/   — bare Git repo used as origin
        worktree/     — isolated fixture working repository

Negative states (P-2, P-3, P-5) are constructed BEFORE commit.
No tracked fixture file is mutated after commit.
"""

import subprocess
import sys
from pathlib import Path

RUNNER = Path(__file__).parent.parent / "scripts" / "e2_path_n_smoke_runner.sh"
MATCHER = Path(__file__).parent.parent / "scripts" / "e2_exact_matcher.py"
ARTIFACT_PATH = (
    "docs/governance/path_n_content_config/"
    "electronics_electrical_path_n_questions.json"
)
DENIED_SID = "830054a4-f9cb-43fb-ab1c-f5d5f3cfb314"


def _git(args, cwd, check=True):
    """Run a git command in cwd."""
    return subprocess.run(
        ["git"] + args,
        cwd=str(cwd),
        check=check,
        capture_output=True,
        text=True,
    )


def _make_fixture(tmp_path: Path, extra_setup=None) -> Path:
    """
    Create an isolated fixture repository.

    extra_setup(worktree) is called after git init but BEFORE
    git add + commit + push, so negative states are committed.
    Returns the worktree path.
    """
    remote = tmp_path / "remote.git"
    worktree = tmp_path / "worktree"

    subprocess.run(["git", "init", "--bare", str(remote)], check=True,
                   capture_output=True)
    subprocess.run(["git", "init", str(worktree)], check=True,
                   capture_output=True)
    _git(["checkout", "-b", "main"], cwd=worktree)
    _git(["config", "user.email", "test@example.invalid"], cwd=worktree)
    _git(["config", "user.name", "Test"], cwd=worktree)

    if extra_setup:
        extra_setup(worktree)

    placeholder = worktree / ".gitkeep"
    # iterdir() sees .git/ even on empty init; check for non-.git entries
    non_git = [p for p in worktree.iterdir() if p.name != ".git"]
    if not placeholder.exists() and not non_git:
        placeholder.write_text("")

    _git(["add", "."], cwd=worktree)
    _git(
        ["-c", "user.name=Test", "-c", "user.email=test@example.invalid",
         "commit", "-m", "fixture"],
        cwd=worktree,
    )
    _git(["remote", "add", "origin", str(remote)], cwd=worktree)
    _git(["push", "-u", "origin", "main"], cwd=worktree)

    return worktree


def _run_preflight(worktree: Path) -> tuple:
    result = subprocess.run(
        ["bash", str(RUNNER), "--preflight"],
        cwd=str(worktree),
        capture_output=True,
        text=True,
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode


# ── P-1: all checks pass ─────────────────────────────────────────────────────

def test_p1_all_checks_pass(tmp_path):
    """Full valid worktree — PREFLIGHT OK."""

    def setup(worktree: Path):
        (worktree / "engine").mkdir()
        (worktree / "engine" / "__init__.py").write_text("")
        (worktree / "docs" / "governance").mkdir(parents=True)
        scripts_dir = worktree / "scripts"
        scripts_dir.mkdir()
        matcher_src = MATCHER.read_text(encoding="utf-8")
        (scripts_dir / "e2_exact_matcher.py").write_text(matcher_src, encoding="utf-8")
        artifact_dir = worktree / "docs" / "governance" / "path_n_content_config"
        artifact_dir.mkdir(parents=True)
        artifact_content = (
            '{"metadata": {"runtime_integrated": false}, '
            '"gaps": {"MECHANISM_COMPLETENESS": ['
            '{"question_id": "N-MC-1", "text": "Explain in everyday words '
            'how you imagine the system would notice the problem and respond."}'
            ']}}'
        )
        (artifact_dir / "electronics_electrical_path_n_questions.json").write_text(
            artifact_content, encoding="utf-8"
        )

    worktree = _make_fixture(tmp_path, setup)
    stdout, stderr, code = _run_preflight(worktree)

    assert stdout == "PREFLIGHT OK"
    assert stderr == ""
    assert code == 0


# ── P-2: missing matcher ──────────────────────────────────────────────────────

def test_p2_missing_matcher(tmp_path):
    """No matcher committed — PREFLIGHT FAIL: CHECK 4."""

    def setup(worktree: Path):
        (worktree / "engine").mkdir()
        (worktree / "engine" / "__init__.py").write_text("")
        (worktree / "docs" / "governance").mkdir(parents=True)
        (worktree / "scripts").mkdir()
        artifact_dir = worktree / "docs" / "governance" / "path_n_content_config"
        artifact_dir.mkdir(parents=True)
        (artifact_dir / "electronics_electrical_path_n_questions.json").write_text(
            '{"metadata": {}, "gaps": {}}', encoding="utf-8"
        )

    worktree = _make_fixture(tmp_path, setup)
    stdout, stderr, code = _run_preflight(worktree)

    assert stdout == "PREFLIGHT FAIL: CHECK 4"
    assert stderr == ""
    assert code == 1


# ── P-3: invalid matcher syntax ───────────────────────────────────────────────

def test_p3_invalid_matcher_syntax(tmp_path):
    """Syntactically invalid matcher committed — PREFLIGHT FAIL: CHECK 5."""

    def setup(worktree: Path):
        (worktree / "engine").mkdir()
        (worktree / "engine" / "__init__.py").write_text("")
        (worktree / "docs" / "governance").mkdir(parents=True)
        scripts_dir = worktree / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "e2_exact_matcher.py").write_text("if True:\n", encoding="utf-8")
        artifact_dir = worktree / "docs" / "governance" / "path_n_content_config"
        artifact_dir.mkdir(parents=True)
        (artifact_dir / "electronics_electrical_path_n_questions.json").write_text(
            '{"metadata": {}, "gaps": {}}', encoding="utf-8"
        )

    worktree = _make_fixture(tmp_path, setup)
    stdout, stderr, code = _run_preflight(worktree)

    assert stdout == "PREFLIGHT FAIL: CHECK 5"
    assert stderr == ""
    assert code == 1


# ── P-4: prior SID rejected ───────────────────────────────────────────────────

def test_p4_prior_sid_rejected(tmp_path):
    """--validate-sid on denied SID returns STOP: denied prior SID.

    Runs inside an isolated fixture repository per Gate B §9.
    """

    # Build a minimal isolated fixture repo so P-4 runs from a real
    # tmp_path fixture repository, not merely a bare temporary directory.
    worktree = _make_fixture(tmp_path)

    result = subprocess.run(
        ["bash", str(RUNNER), "--validate-sid", DENIED_SID],
        cwd=str(worktree),
        capture_output=True,
        text=True,
    )
    stdout = result.stdout.strip()
    stderr = result.stderr.strip()
    code = result.returncode

    assert stdout == "STOP: denied prior SID"
    assert stderr == ""
    assert code != 0


# ── P-5: missing artifact ─────────────────────────────────────────────────────

def test_p5_missing_artifact(tmp_path):
    """No artifact at CHECK 6 path committed — PREFLIGHT FAIL: CHECK 6."""

    def setup(worktree: Path):
        (worktree / "engine").mkdir()
        (worktree / "engine" / "__init__.py").write_text("")
        (worktree / "docs" / "governance").mkdir(parents=True)
        scripts_dir = worktree / "scripts"
        scripts_dir.mkdir()
        matcher_src = MATCHER.read_text(encoding="utf-8")
        (scripts_dir / "e2_exact_matcher.py").write_text(matcher_src, encoding="utf-8")
        # artifact directory NOT created

    worktree = _make_fixture(tmp_path, setup)
    stdout, stderr, code = _run_preflight(worktree)

    assert stdout == "PREFLIGHT FAIL: CHECK 6"
    assert stderr == ""
    assert code == 1
