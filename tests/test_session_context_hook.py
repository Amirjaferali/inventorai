"""The project SessionStart hook (`.claude/hooks/session_context.py`, registered in
`.claude/settings.json`): it restores bounded context from the CURRENT sources of the
checkout it lives in, refreshes on every run, reports missing or ambiguous sources as
UNAVAILABLE instead of inventing them, and is read-only.

Each case copies the hook and the real current sources into a throw-away git repository,
so the hook reads exactly what it would read in a real checkout of that tree.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
HOOK = Path(".claude/hooks/session_context.py")
DOCS = ("CLAUDE.md",
        "docs/governance/ACTIVE_INCREMENT_CONTRACT.md",
        "docs/governance/ACCELERATED_HIGH_ASSURANCE_EXECUTION_PROTOCOL.md",
        "docs/governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md")


# Test-local Git configuration: a commit otherwise spawns git's detached
# auto-maintenance (``git maintenance run --auto``; ``gc --auto`` on older
# Git), which takes and removes ``.git/objects/maintenance.lock`` in the
# background and can race a test that deletes the throw-away ``.git`` right
# after the commit. The hook under test is unaffected: it only reads Git.
_NO_AUTO_MAINTENANCE = ("-c", "maintenance.auto=false", "-c", "gc.auto=0")


def _git(cwd, *args):
    return subprocess.run(["git", "-C", str(cwd), *_NO_AUTO_MAINTENANCE, *args],
                          capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def checkout(tmp_path):
    root = tmp_path / "repo"
    for rel in (*DOCS, str(HOOK)):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(REPO / rel, root / rel)
    _git(tmp_path, "init", "-q", "-b", "main", str(root))
    _git(root, "add", "-A")
    _git(root, "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q", "-m", "c")
    return root


def _run(root, stdin='{"source": "startup"}', cwd=None):
    done = subprocess.run([sys.executable, "-I", "-B", str(root / HOOK)], input=stdin,
                          capture_output=True, text=True, timeout=20, cwd=str(cwd or root))
    assert done.returncode == 0, done.stderr
    assert done.stderr == ""
    out = json.loads(done.stdout)
    assert set(out) == {"hookSpecificOutput"}
    spec = out["hookSpecificOutput"]
    assert spec["hookEventName"] == "SessionStart"
    return spec["additionalContext"]


def _snapshot(root):
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            files[str(path.relative_to(root))] = (hashlib.sha256(path.read_bytes()).hexdigest(),
                                                  path.stat().st_mtime_ns)
    return files


# ---- settings registration ------------------------------------------------------------------------
def test_settings_register_one_bounded_sessionstart_command_hook_only():
    settings = json.loads((REPO / ".claude/settings.json").read_text(encoding="utf-8"))
    assert set(settings) <= {"$schema", "hooks"}                  # no permissions, env or other settings
    assert set(settings["hooks"]) == {"SessionStart"}             # no PreToolUse / Stop / other events
    [group] = settings["hooks"]["SessionStart"]
    assert "matcher" not in group                                 # startup, resume, clear and compact
    [hook] = group["hooks"]
    assert hook["type"] == "command"
    assert hook["command"] == 'python3 -I -B "$CLAUDE_PROJECT_DIR/.claude/hooks/session_context.py"'
    assert 0 < hook["timeout"] <= 10


# ---- correct source selection ---------------------------------------------------------------------
def test_reports_the_current_sources_with_their_locations(checkout):
    text = _run(checkout)
    assert text.startswith("InventorAI session context (source: startup; all 16 items read)")
    claude = (checkout / "CLAUDE.md").read_text(encoding="utf-8").splitlines()
    [declaration] = re.findall(r"\*\*ACTIVE CONTRACT: [^*]+?\.\*\*", "\n".join(claude))
    line = next(i for i, l in enumerate(claude, 1) if declaration in l)
    assert "%s at CLAUDE.md:%d" % (declaration, line) in text
    ahaep = (checkout / DOCS[2]).read_text(encoding="utf-8").splitlines()
    for name in ("NEXT-LOOP v1.0", "BMG", "FCR — Two Layers", "RE-SPE"):
        row = next(i for i, l in enumerate(ahaep, 1) if l.startswith("| **%s** |" % name))
        meaning = ahaep[row - 1].strip().strip("|").split("|")[1].strip()
        assert "%s (%s:%d) — %s" % (name, DOCS[2], row, meaning) in text
    for phrase in ("READ BEFORE BUILD / REUSE BEFORE CREATE", "**Review routing.**", "**Test proportionality.**",
                   "NO TECHNICAL DEPTH WITHOUT SOURCE AUTHORITY", "**D. Quality is preserved.**",
                   "Escalate reserved decisions and scope changes as defined in Lean §2"):
        assert phrase in text, phrase
    head = _git(checkout, "rev-parse", "HEAD")
    assert "branch main; HEAD %s;" % head in text and "(main checkout)" in text
    assert "Checkout facts are LOCAL" in text and "never overrides an explicit, scoped Owner instruction" in text
    assert "this context names no next task" in text


def test_the_real_checkout_restores_every_item_within_bounds():
    done = subprocess.run([sys.executable, "-I", "-B", str(REPO / HOOK)], input='{"source": "compact"}',
                          capture_output=True, text=True, timeout=20, cwd=str(REPO))
    text = json.loads(done.stdout)["hookSpecificOutput"]["additionalContext"]
    assert "(source: compact; all 16 items read)" in text
    assert len(text) <= 9000
    # the FULL-route retry rule is restored whole, not cut off by the per-item cap
    assert ("reruns the whole FULL workflow as one complete attempt, never a single shard or job: "
            "`CI required` accepts only the five shard evidence packages of the same attempt.") in text


@pytest.mark.parametrize("source", ["startup", "resume", "clear", "compact"])
def test_every_supported_start_is_named(checkout, source):
    assert _run(checkout, json.dumps({"source": source})).startswith(
        "InventorAI session context (source: %s;" % source)


# ---- changed-source refresh -----------------------------------------------------------------------
def test_a_changed_source_is_read_again_on_the_next_run(checkout):
    before = _run(checkout)
    claude = checkout / "CLAUDE.md"
    raw = claude.read_text(encoding="utf-8")
    [declaration] = re.findall(r"\*\*ACTIVE CONTRACT: [^*]+?\.\*\*", raw)
    claude.write_text(raw.replace(declaration, "**ACTIVE CONTRACT: TEST-ONLY-INCREMENT.**", 1), encoding="utf-8")
    after = _run(checkout)
    assert declaration in before and declaration not in after
    assert "**ACTIVE CONTRACT: TEST-ONLY-INCREMENT.**" in after
    assert "1 tracked file(s) modified" in after


# ---- missing, ambiguous and malformed inputs -------------------------------------------------------
def test_a_missing_source_is_unavailable_never_invented(checkout):
    (checkout / DOCS[2]).unlink()
    text = _run(checkout)
    assert "RESTORATION INCOMPLETE: 1 of 13 items UNAVAILABLE" in text
    assert "UNAVAILABLE — %s cannot be read (FileNotFoundError); read that source directly." % DOCS[2] in text
    assert "NEXT-LOOP" not in text


def test_an_ambiguous_declaration_is_unavailable(checkout):
    claude = checkout / "CLAUDE.md"
    raw = claude.read_text(encoding="utf-8")
    claude.write_text(raw.replace("## One boot sequence", "**ACTIVE CONTRACT: OTHER.**\n\n## One boot sequence", 1),
                      encoding="utf-8")
    text = _run(checkout)
    assert "RESTORATION INCOMPLETE: 1 of 16 items UNAVAILABLE" in text
    assert "CLAUDE.md: 2 bold ACTIVE CONTRACT declarations, expected exactly one" in text
    assert "ACTIVE CONTRACT: OTHER" not in text


def test_a_moved_or_duplicated_rule_label_is_unavailable(checkout):
    claude = checkout / "CLAUDE.md"
    raw = claude.read_text(encoding="utf-8")
    claude.write_text(raw.replace("**Review routing.**", "**Routing of reviews.**", 1)
                      .replace("**Test proportionality.**", "**Test proportionality.** a\n\n**Test proportionality.**", 1),
                      encoding="utf-8")
    text = _run(checkout)
    assert "RESTORATION INCOMPLETE: 2 of 16 items UNAVAILABLE" in text
    assert "'**Review routing.**' found 0 times, expected once" in text
    assert "'**Test proportionality.**' found 2 times, expected once" in text


def test_a_malformed_mechanism_row_is_unavailable(checkout):
    ahaep = checkout / DOCS[2]
    raw = ahaep.read_text(encoding="utf-8")
    ahaep.write_text(re.sub(r"^\| \*\*BMG\*\* \|.*$", "| **BMG** | broken |", raw, count=1, flags=re.M),
                     encoding="utf-8")
    text = _run(checkout)
    assert re.search(r"UNAVAILABLE — %s:\d+: row 'BMG' is malformed" % re.escape(DOCS[2]), text)


@pytest.mark.parametrize("stdin", ["", "not json", "[]", '{"source": 7}', '{"source": "other"}',
                                   '{"source": "$(touch PWNED)"}', '{"source": "startup; touch PWNED"}',
                                   '{"source": []}', '{"source": {}}', '{"cwd": 5}', '{"cwd": "relative/dir"}'])
def test_malformed_or_hostile_hook_input_is_never_used(checkout, stdin):
    text = _run(checkout, stdin)
    assert text.startswith("InventorAI session context (source: unknown;")
    assert not list(checkout.rglob("PWNED")) and not (Path.cwd() / "PWNED").exists()


def test_outside_a_git_checkout_nothing_is_restored(checkout):
    shutil.rmtree(checkout / ".git")
    text = _run(checkout)
    assert text.startswith("InventorAI session context (source: startup; RESTORATION INCOMPLETE: the working "
                           "checkout is not confirmed)")
    assert "UNAVAILABLE — git rev-parse failed. Nothing was restored" in text
    assert "ACTIVE CONTRACT" not in text and "NEXT-LOOP" not in text


# ---- worktree / path handling ---------------------------------------------------------------------
def test_a_linked_worktree_reads_its_own_sources(checkout, tmp_path):
    wt = tmp_path / "wt"
    _git(checkout, "worktree", "add", "-q", "-b", "other", str(wt))
    claude = wt / "CLAUDE.md"
    raw = claude.read_text(encoding="utf-8")
    [declaration] = re.findall(r"\*\*ACTIVE CONTRACT: [^*]+?\.\*\*", raw)
    claude.write_text(raw.replace(declaration, "**ACTIVE CONTRACT: WORKTREE.**", 1), encoding="utf-8")
    text = _run(wt)
    assert "root %s (linked worktree); branch other;" % wt.resolve() in text
    assert "**ACTIVE CONTRACT: WORKTREE.**" in text
    assert declaration in _run(checkout)                          # the main checkout is untouched


def test_a_subdirectory_of_the_same_checkout_is_restored(checkout):
    sub = checkout / "docs" / "governance"
    for stdin in ('{"source": "startup", "cwd": "%s"}' % sub, '{"source": "startup"}'):
        text = _run(checkout, stdin, cwd=sub)
        assert text.startswith("InventorAI session context (source: startup; all 16 items read)")
        assert "root %s (main checkout)" % checkout.resolve() in text


def test_a_working_directory_outside_any_checkout_is_not_confirmed(checkout, tmp_path):
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    text = _run(checkout, '{"source": "startup", "cwd": "%s"}' % elsewhere, cwd=elsewhere)
    assert "RESTORATION INCOMPLETE: the working checkout is not confirmed" in text
    assert "ACTIVE CONTRACT" not in text


def _registered_command(project_dir, working_dir, stdin):
    """Run the exact command `.claude/settings.json` registers, the way Claude Code does: through a
    shell, with $CLAUDE_PROJECT_DIR set to the session's starting checkout."""
    settings = json.loads((REPO / ".claude/settings.json").read_text(encoding="utf-8"))
    [group] = settings["hooks"]["SessionStart"]
    [hook] = group["hooks"]
    env = dict(os.environ, CLAUDE_PROJECT_DIR=str(project_dir))
    done = subprocess.run(["/bin/sh", "-c", hook["command"]], input=stdin, capture_output=True, text=True,
                          timeout=20, cwd=str(working_dir), env=env)
    assert done.returncode == 0 and done.stderr == "", done.stderr
    return json.loads(done.stdout)["hookSpecificOutput"]["additionalContext"]


@pytest.mark.parametrize("with_input_cwd", [True, False])
def test_a_session_moved_into_another_worktree_is_not_given_the_start_checkouts_authority(
        checkout, tmp_path, with_input_cwd):
    """Claude Code keeps $CLAUDE_PROJECT_DIR at the starting checkout after the session enters another
    worktree, while the hook's working directory (and input cwd) follow the session."""
    wt = tmp_path / "wt"
    _git(checkout, "worktree", "add", "-q", "-b", "other", str(wt))
    for root, marker in ((checkout, "MAIN-ONLY"), (wt, "WORKTREE-ONLY")):
        claude = root / "CLAUDE.md"
        raw = claude.read_text(encoding="utf-8")
        [declaration] = re.findall(r"\*\*ACTIVE CONTRACT: [^*]+?\.\*\*", raw)
        claude.write_text(raw.replace(declaration, "**ACTIVE CONTRACT: %s.**" % marker, 1), encoding="utf-8")
    stdin = json.dumps({"source": "resume", "cwd": str(wt)} if with_input_cwd else {"source": "resume"})
    text = _registered_command(checkout, wt, stdin)
    assert text.startswith("InventorAI session context (source: resume; RESTORATION INCOMPLETE: the working "
                           "checkout is not confirmed)")
    assert ("the session's working checkout %s is not the checkout this hook reads (%s)"
            % (wt.resolve(), checkout.resolve())) in text
    assert "MAIN-ONLY" not in text and "WORKTREE-ONLY" not in text and "all 16 items read" not in text
    # the same registered command from the starting checkout itself is restored normally
    same = _registered_command(checkout, checkout, json.dumps({"source": "resume", "cwd": str(checkout)}))
    assert "all 16 items read" in same and "**ACTIVE CONTRACT: MAIN-ONLY.**" in same


# ---- read-only behaviour and bounds ---------------------------------------------------------------
def test_the_hook_writes_nothing(checkout):
    _git(checkout, "status", "--porcelain")                      # settle the index once
    before = _snapshot(checkout)
    for source in ("startup", "resume", "clear", "compact"):
        _run(checkout, json.dumps({"source": source}))
    assert _snapshot(checkout) == before                          # no file, index or cache change


def test_output_is_bounded(checkout):
    claude = checkout / "CLAUDE.md"
    raw = claude.read_text(encoding="utf-8")
    long_line = " ".join(["reviewed"] * 4000)
    claude.write_text(raw.replace("**Review routing.**", "**Review routing.** " + long_line, 1), encoding="utf-8")
    text = _run(checkout)
    assert len(text) <= 9000
    assert "… (continues at CLAUDE.md:" in text


def test_the_helper_stays_local_and_read_only_by_construction():
    source = (REPO / HOOK).read_text(encoding="utf-8")
    for forbidden in ("import socket", "urllib", "http.client", "requests", "shell=True", "os.system",
                      "write_text", "eval(", "exec(", "transcript_path", "CLAUDE_ENV_FILE"):
        assert forbidden not in source, forbidden
    assert not re.search(r"open\([^)]*['\"][wa]", source)
    assert "timeout=GIT_TIMEOUT_S" in source and "GIT_OPTIONAL_LOCKS" in source


# ---- research continuity: source-backed navigation, never execution authority ---------------------
CHECKPOINT_LABEL = "**9.5 Research-to-execution checkpoint.**"


@pytest.mark.parametrize("source", ["startup", "resume", "clear", "compact"])
def test_research_checkpoint_is_restored_on_every_start(checkout, source):
    text = _run(checkout, json.dumps({"source": source}))
    lean = (checkout / DOCS[3]).read_text(encoding="utf-8").splitlines()
    line = next(i for i, value in enumerate(lean, 1) if value.startswith(CHECKPOINT_LABEL))
    assert "%s:%d" % (DOCS[3], line) in text
    for phrase in (CHECKPOINT_LABEL, "Navigation only", "Flux/tool execution",
                   "Zoo/editable engineering source", "CELUS/typed interfaces",
                   "CadQuery/tray is a CANDIDATE", "not an approved product step",
                   "No new product increment, provider call, merge or deployment is authorized here."):
        assert phrase in text, phrase
    assert "all 16 items read" in text and len(text) <= 9000
    # Policy text is read from its existing owner, not copied into the hook.
    hook = (checkout / HOOK).read_text(encoding="utf-8")
    assert "CadQuery/tray" not in hook and "Flux/tool execution" not in hook


def test_research_checkpoint_refreshes_from_its_source(checkout):
    lean = checkout / DOCS[3]
    old = "CadQuery/tray is a CANDIDATE"
    new = "UPDATED-RESEARCH-POINTER is a CANDIDATE"
    assert old in _run(checkout)
    raw = lean.read_text(encoding="utf-8")
    assert raw.count(old) == 1
    lean.write_text(raw.replace(old, new), encoding="utf-8")
    refreshed = _run(checkout, '{"source": "compact"}')
    assert new in refreshed and old not in refreshed
    assert "No new product increment" in refreshed


@pytest.mark.parametrize("count", [0, 2])
def test_missing_or_ambiguous_research_checkpoint_is_not_silently_omitted(checkout, count):
    lean = checkout / DOCS[3]
    raw = lean.read_text(encoding="utf-8")
    if count == 0:
        raw = raw.replace(CHECKPOINT_LABEL, "**Moved checkpoint.**", 1)
    else:
        raw += "\n" + CHECKPOINT_LABEL + " duplicated\n"
    lean.write_text(raw, encoding="utf-8")
    text = _run(checkout)
    assert "RESTORATION INCOMPLETE: 1 of 16 items UNAVAILABLE" in text
    assert "found %d times, expected once" % count in text
    assert "CadQuery/tray" not in text
    assert "ACTIVE CONTRACT" in text                  # unrelated authority restoration continues


def test_research_continuity_keeps_owner_routes_and_candidate_boundaries():
    raw = (REPO / DOCS[3]).read_text(encoding="utf-8")
    checkpoint = raw.split(CHECKPOINT_LABEL, 1)[1].split("## 10.", 1)[0]
    for phrase in ("ACTIVE_INCREMENT_CONTRACT.md", "CURRENT_PROJECT_STATE.md", "CLAUDE.md",
                   "not the next authorized increment", "PR #890 stays HOLD",
                   "BLOCKED/DEFER", "reopening triggers", "PCRA/SFR", "G1/NEXT-LOOP",
                   "Technical Realization", "Stage 15", "current Proof B task"):
        assert phrase in checkpoint, phrase
    assert "No additional product" in checkpoint
    assert "No new product increment, provider call, merge or deployment is authorized here." in checkpoint


def test_g1_engineering_integration_target_stays_a_bounded_candidate():
    raw = (REPO / DOCS[3]).read_text(encoding="utf-8")
    checkpoint = raw.split(CHECKPOINT_LABEL, 1)[1].split("## 10.", 1)[0]
    label = "**G1-3/4 engineering-integration target"
    assert checkpoint.count(label) == 1
    target = " ".join(checkpoint.split(label, 1)[1].split("\nSource leads retained", 1)[0].split())
    for phrase in (
            # the approved direction: the core vision, not the demonstration
            "Approved direction", "coherent, revisable, evidence-grounded engineering design of "
            "the inventor's whole invention", "inform the design of another",
            "within the scope of admitted methods", "must not silently remain represented as current",
            "not AI-generated designs, independent calculators, attractive CAD models",
            "ONE qualified relationship", "reproducible engineering check",
            "inspectable engineering artifact",
            "Decompose -> Evaluate -> Assemble & Verify -> Revise",
            "only where a qualified mathematical objective, method and constraints exist",
            # the candidate demonstration and its limits
            "Candidate demonstration, not the definition of the product",
            "PCB-to-enclosure geometric integration", "covers geometric fit",
            "no engineering authority or D4 physical-compatibility qualification transfers",
            # what stays unauthorized
            "Not authorized by this note", "CAD integration, cross-domain verification capability "
            "or AI proposal writer", "its own Owner authorization", "IP/license review",
            "TR Evidence Model §11", "OD-2", "no general compatibility engine",
            "never presented to the inventor as verified", "Proof B work completes first",
            "PR #890 HOLD and D4 BLOCKED"):
        assert phrase in target, phrase
    # the quoted opening paragraph is unchanged, so SessionStart output is unchanged
    opening = checkpoint.split("\n\n", 1)[0]
    assert "PCB" not in opening and "No new product increment" in opening
