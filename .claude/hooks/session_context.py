"""SessionStart hook: restore bounded working context from this checkout's CURRENT sources.

Run by Claude Code at every session start (fresh, resume, clear and compaction). It quotes, at
their current wording and location, the repository's own current-authority declaration and
execution rules, so a new or compacted session starts from them instead of from memory. It holds
no rule text of its own: every rule line below is read from its source file on each run, so the
output cannot drift from the instructions it points to.

Read-only and local: standard library only; two `git rev-parse` / `git status` reads with no
optional locks and a short timeout; no network, model call, test run, secret or transcript read,
repository write or environment change. The hook input is parsed as JSON data; only its `source`
field is used, checked against a closed set, and nothing from it reaches a shell or a path. Any
source that is missing, unreadable or ambiguous is reported as UNAVAILABLE, never filled in.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLAUDE_MD = "CLAUDE.md"
CONTRACT = "docs/governance/ACTIVE_INCREMENT_CONTRACT.md"
AHAEP = "docs/governance/ACCELERATED_HIGH_ASSURANCE_EXECUTION_PROTOCOL.md"
LEAN = "docs/governance/LEAN_GOVERNANCE_AND_AGENT_CONTINUITY_PROTOCOL.md"
SOURCES = {"startup", "resume", "clear", "compact"}
GIT_TIMEOUT_S = 2
ITEM_CAP = 700           # characters quoted per rule item
TOTAL_CAP = 9000         # characters of context in total

# Where each quoted rule lives: (file, paragraph label or table name, key phrase or None).
# Only locations are kept here; the wording is always read from the file.
MECHANISMS = ("NEXT-LOOP v1.0", "BMG", "FCR — Two Layers", "RE-SPE")
RULES = (
    (CLAUDE_MD, "**Lead and executor.**", "READ BEFORE BUILD / REUSE BEFORE CREATE"),
    (CLAUDE_MD, "**Review routing.**", None),
    (CLAUDE_MD, "**Test proportionality.**", None),
    (CLAUDE_MD, "**Technical Knowledge & Intellectual Property Source Boundary", None),
    (CLAUDE_MD, "- **D. Quality is preserved.**", None),
    (CLAUDE_MD, "## Continue, hold and return", None),
    (LEAN, "**9.5 Research-to-execution checkpoint.**", None),
)
HEADINGS = ((CLAUDE_MD, "## One boot sequence"), (LEAN, "## 2. Owner authority and milestone delegation"),
            (LEAN, "## 10. Reserved decisions and scoped holds"))

BOUNDARY = (
    "This is a read-out of repository text taken at session start; it is not an instruction source of "
    "its own and adds no authority. Checkout facts are LOCAL: verify the live branch, PR and CI state on "
    "GitHub before relying on them. Repository status grants no authority and never overrides an "
    "explicit, scoped Owner instruction. NEXT comes from the current task or its return: this context "
    "names no next task, and delivered or historical prose is not current authorization."
)


class Unavailable(Exception):
    pass


def _read(rel):
    try:
        return (ROOT / rel).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise Unavailable("%s cannot be read (%s)" % (rel, type(exc).__name__))


def _flat(text):
    return re.sub(r"\s+", " ", text).strip()


def _cap(text, where):
    if len(text) <= ITEM_CAP:
        return text
    return text[:ITEM_CAP].rsplit(" ", 1)[0] + " … (continues at %s)" % where


def _unique_line(lines, rel, prefix):
    hits = [i for i, line in enumerate(lines) if line.startswith(prefix)]
    if len(hits) != 1:
        raise Unavailable("%s: %r found %d times, expected once" % (rel, prefix, len(hits)))
    return hits[0]


def _paragraph(rel, label, phrase):
    lines = _read(rel).splitlines()
    start = _unique_line(lines, rel, label)
    if label.startswith("#"):                       # a section: its first paragraph after the heading
        start += 1
        while start < len(lines) and not lines[start].strip():
            start += 1
    end = start + 1
    while end < len(lines) and lines[end].strip() and not lines[end].startswith(("**", "- **", "#")):
        end += 1
    text = _flat(" ".join(lines[start:end]))
    text = text[2:] if text.startswith("- ") else text
    if phrase:
        sentences = re.split(r"(?<=[.;])\s+", text)
        found = [s for s in sentences if phrase in s]
        if len(found) != 1:
            raise Unavailable("%s:%d: %r found in %d sentences, expected one" % (rel, start + 1, phrase,
                                                                                len(found)))
        text = found[0]
    where = "%s:%d" % (rel, start + 1)
    return "%s — %s" % (where, _cap(text, where))


def _mechanism(lines, name):
    rows = [i for i, line in enumerate(lines) if line.startswith("| **%s** |" % name)]
    if len(rows) != 1:
        raise Unavailable("%s: table row %r found %d times, expected once" % (AHAEP, name, len(rows)))
    cells = [c.strip() for c in lines[rows[0]].strip().strip("|").split("|")]
    if len(cells) != 3:
        raise Unavailable("%s:%d: row %r is malformed" % (AHAEP, rows[0] + 1, name))
    where = "%s:%d" % (AHAEP, rows[0] + 1)
    return "%s (%s) — %s Owner: %s" % (name, where, _cap(cells[1], where), cells[2])


def _authority():
    lines = _read(CLAUDE_MD).splitlines()
    start = _unique_line(lines, CLAUDE_MD, "## Current authority")
    declared = [(i, m.group(0)) for i, line in enumerate(lines[start:], start)
                for m in re.finditer(r"\*\*ACTIVE CONTRACT: [^*]+?\.\*\*", line)]
    if len(declared) != 1:
        raise Unavailable("%s: %d bold ACTIVE CONTRACT declarations, expected exactly one"
                          % (CLAUDE_MD, len(declared)))
    line_no, declaration = declared[0]
    contract = _read(CONTRACT).splitlines()
    sections = [i for i, line in enumerate(contract) if line.startswith("## Current authority")]
    if not sections:
        raise Unavailable("%s: no '## Current authority' section" % CONTRACT)
    return ("%s at %s:%d (section %s:%d). Declaration owner and delivered history: %s — its FIRST "
            "'## Current authority' section is the live one (%s:%d: %s)."
            % (declaration, CLAUDE_MD, line_no + 1, CLAUDE_MD, start + 1, CONTRACT, CONTRACT,
               sections[0] + 1, _flat(contract[sections[0]])[:200]))


def _git(*args, where=ROOT):
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "GIT_OPTIONAL_LOCKS": "0", "LC_ALL": "C"}
    done = subprocess.run(["git", "-C", str(where), *args], capture_output=True, text=True,
                          timeout=GIT_TIMEOUT_S, env=env, check=False)
    if done.returncode != 0:
        raise Unavailable("git %s failed" % args[0])
    return done.stdout


def _checkout():
    top, git_dir, common, head = _git(
        "rev-parse", "--show-toplevel", "--absolute-git-dir", "--git-common-dir", "HEAD").splitlines()
    branch = _git("rev-parse", "--abbrev-ref", "HEAD").strip()
    branch = "(detached HEAD)" if branch == "HEAD" else branch
    common = (Path(top) / common).resolve() if not os.path.isabs(common) else Path(common)
    changed = len(_git("status", "--porcelain", "--untracked-files=no").splitlines())
    kind = "linked worktree" if Path(git_dir).resolve() != common.resolve() else "main checkout"
    return ("root %s (%s); branch %s; HEAD %s; %d tracked file(s) modified (local, unverified against "
            "GitHub)" % (top, kind, branch, head, changed))


def _same_checkout(cwd):
    """The session's working checkout must be the one this hook reads. Claude Code keeps
    $CLAUDE_PROJECT_DIR (and so this script) at the session's starting checkout after the session
    moves into another worktree, while the hook's working directory follows the session. Only the
    two checkouts' top-level identities are compared; nothing is read from the working directory."""
    if isinstance(cwd, str) and 0 < len(cwd) < 4096 and "\0" not in cwd and os.path.isabs(cwd):
        where = cwd
    else:
        where = os.getcwd()
    if not os.path.isdir(where):
        raise Unavailable("the session's working directory is not a directory")
    own = Path(_git("rev-parse", "--show-toplevel").strip()).resolve()
    working = Path(_git("rev-parse", "--show-toplevel", where=where).strip()).resolve()
    if working != own:
        raise Unavailable("the session's working checkout %s is not the checkout this hook reads (%s)"
                          % (working, own))


def _item(fn, *args):
    try:
        return True, fn(*args)
    except Unavailable as exc:
        return False, "UNAVAILABLE — %s; read that source directly." % exc
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return False, "UNAVAILABLE — %s; read that source directly." % type(exc).__name__


def build_context(source, cwd=None):
    try:
        _same_checkout(cwd)
    except (Unavailable, OSError, ValueError, subprocess.SubprocessError) as exc:
        reason = str(exc) if isinstance(exc, Unavailable) else type(exc).__name__
        return ("InventorAI session context (source: %s; RESTORATION INCOMPLETE: the working checkout "
                "is not confirmed)\n%s\n- UNAVAILABLE — %s. Nothing was restored: no authority or rule "
                "from %s is presented as this session's context. Read CLAUDE.md and its boot sequence in "
                "the working checkout directly." % (source, BOUNDARY, reason, ROOT))
    results = []
    sections = []

    def add(title, items):
        sections.append(title)
        for ok, text in items:
            results.append(ok)
            sections.append("- " + text)

    add("1. Local checkout", [_item(_checkout)])
    add("2. Current authority", [_item(_authority)])
    ahaep = _item(lambda: _read(AHAEP).splitlines())
    if ahaep[0]:
        add("3. Named execution mechanisms (AHAEP §1A table; §1A.1 says how to apply them)",
            [_item(_mechanism, ahaep[1], name) for name in MECHANISMS])
    else:
        add("3. Named execution mechanisms", [ahaep])
    add("4. Standing rules (quoted from their source)", [_item(_paragraph, *rule) for rule in RULES])
    add("5. Where to read further", [
        _item(lambda rel, h: "%s:%d — %s" % (rel, _unique_line(_read(rel).splitlines(), rel, h) + 1, h),
              rel, heading) for rel, heading in HEADINGS])
    missing = results.count(False)
    status = ("all %d items read" % len(results) if not missing else
              "RESTORATION INCOMPLETE: %d of %d items UNAVAILABLE (listed below)" % (missing, len(results)))
    head = "InventorAI session context (source: %s; %s)\n%s\n" % (source, status, BOUNDARY)
    text = head + "\n".join(sections)
    if len(text) > TOTAL_CAP:
        text = text[:TOTAL_CAP].rsplit("\n", 1)[0] + "\n… (context truncated at %d characters)" % TOTAL_CAP
    return text


def main():
    try:
        payload = json.loads(sys.stdin.read(65536) or "{}")
        payload = payload if isinstance(payload, dict) else {}
    except (ValueError, OSError):
        payload = {}
    source = payload.get("source")
    source = source if isinstance(source, str) and source in SOURCES else "unknown"
    try:
        context = build_context(source, payload.get("cwd"))
    except Exception as exc:                        # never block a session start
        context = ("InventorAI session context UNAVAILABLE (%s): read CLAUDE.md and its boot sequence "
                   "directly.\n%s" % (type(exc).__name__, BOUNDARY))
    json.dump({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}},
              sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
