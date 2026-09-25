"""InventorAI Repository Intelligence (RIG) — advisory impact analysis.

File-creation contract:
  Path: scripts/repository_intelligence.py
  Purpose: developer infrastructure ONLY. For two exact git revisions
    (BASE, HEAD) build a deterministic file-level evidence graph of each,
    resolve change impact over BASE ∪ HEAD, and let a SEPARATE policy layer
    propose an ADVISORY test scope (SMOKE / AFFECTED-CANDIDATE / FULL) plus a
    bounded agent-context package. Architecture contract: RIG-1B,
    `rig-contract-1b.0`.
  Input contract: `--base REV --head REV [--repo PATH]` for an impact report,
    or `--health REV [--repo PATH]` for one revision's completeness report.
    Revisions are read from git objects only (`git ls-tree`, `git cat-file`,
    `git diff --name-status -M`); no working-tree file is read and no
    application module is ever imported.
  Output contract: deterministic JSON on stdout (sorted keys, sorted lists).
    Exit 0 = report produced; exit 2 = analysis unavailable (the JSON then
    says so and its advisory scope is FULL). Nothing is written to disk.
  Prohibited behaviors: RIG has ZERO CI authority — it never skips, selects
    or runs a test, and its wording never implies that anything was skipped.
    No network, no LLM, no credential, no database, no cache, no daemon, no
    third-party package (Python 3.11 standard library + git only). No
    relationship is ever inferred from matching method or function names,
    and git co-change is never a dependency edge.

Evidence kinds are kept apart: observed syntax (never exported), resolved
EDGES (closed vocabulary below), derived reachability (computed at query time,
never stored), UNCERTAINTIES (source-anchored, scoped) and history (identity,
renames and recent-commit context only). Unknown is never reported as "no
dependency": a relationship RIG cannot prove becomes an uncertainty, and an
uncertainty it cannot bound pushes the advisory scope to FULL.
"""
import argparse
import ast
import collections
import fnmatch
import json
import os
import posixpath
import re
import subprocess
import sys

CONTRACT_VERSION = "rig-contract-1b.0"
TOOL_VERSION = "rig-1c.1"

EDGE_TYPES = ("import", "fixture_use", "literal_path", "artifact_reference")

# PROVISIONAL ADVISORY POLICY CONSTANT — not a derived fact and not authorized
# for production CI decisions: a changed path whose BASE ∪ HEAD reverse
# closure reaches more than this share of the HEAD test inventory is escalated
# to FULL.
CENTRALITY_ESCALATION_SHARE = 0.25

SCOPE_RANK = {"SMOKE": 0, "AFFECTED-CANDIDATE": 1, "FULL": 2}

ENVIRONMENT_ASSUMPTIONS = (
    "relative path literals resolve against the repository root (tests and CI run from the root)",
    "Flask templates resolve from the default `templates/` folder beside the rendering module",
    "pytest bare-name imports inside a test directory resolve against that directory",
    "Python modules map 1:1 to tracked `.py` files; `pkg/__init__.py` is module `pkg`",
)

# --------------------------------------------------------------------------
# Policy declarations (reviewed policy, not derived facts)
# --------------------------------------------------------------------------

RIG_SELF_PATHS = (
    "scripts/repository_intelligence.py",
    "scripts/verify_repository_intelligence_replay.py",
    "tests/test_repository_intelligence.py",
    "tests/fixtures/repository_intelligence_replay_v1.json",
)
DECLARED_STATE_CONTRACT = (
    "engine/idea_state.py", "engine/record_contract.py", "engine/record_store.py",
    "engine/session_reconstruction.py", "engine/account_store.py",
)
MANDATORY_GUARDRAILS = ("scripts/run_universal_smoke.py", "tests/universal_guardrail_manifest.py")
PROTECTED_PATTERNS = (
    (".github/workflows/*", "ci-workflow"),
    ("requirements*.txt", "dependency-manifest"),
    ("*/requirements*.txt", "dependency-manifest"),
    (".python-version", "interpreter-config"),
    ("pytest.ini", "test-runner-config"),
    ("setup.cfg", "test-runner-config"),
    ("tox.ini", "test-runner-config"),
    ("pyproject.toml", "build-or-test-config"),
    ("Dockerfile", "container-build"),
    (".dockerignore", "container-build"),
    ("gunicorn.conf.py", "runtime-entrypoint-config"),
    ("*.sql", "database-schema"),
    ("database/*", "database-schema"),
)
ANALYSED_SUFFIXES = (".py", ".md", ".json", ".jsonl", ".txt", ".csv", ".html", ".js", ".css",
                     ".sql", ".yml", ".yaml", ".ini", ".sh", ".toml", ".cfg")
ANALYSED_NAMES = ("Dockerfile", ".python-version", ".dockerignore", ".gitignore")

# Uncertainty kinds that load CODE versus kinds that read DATA. A Markdown
# document can be consumed only by a data-reading kind (or by an unknown
# subprocess, which may do anything); a build-input record is image scope.
CODE_LOADING_KINDS = ("computed-dynamic-import", "unresolved-spec-path", "unresolved-monkeypatch-target")
BUILD_ONLY_KINDS = ("broad-build-input",)

# --------------------------------------------------------------------------
# git access
# --------------------------------------------------------------------------


class AnalysisUnavailable(RuntimeError):
    pass


def _git(repo, *args, data=None):
    try:
        proc = subprocess.run(["git", "-C", repo, *args], input=data, capture_output=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", b"") or b""
        raise AnalysisUnavailable(f"git {' '.join(args[:2])} failed: {detail.decode('utf-8', 'replace').strip()[:200]}") from exc
    return proc.stdout


def _read_text(p):
    return p.endswith(ANALYSED_SUFFIXES) or p.split("/")[-1] in ANALYSED_NAMES


class Snapshot:
    """All tracked paths of one exact revision, and the text of analysable files."""

    def __init__(self, repo, rev):
        self.repo = repo
        self.rev = _git(repo, "rev-parse", "--verify", f"{rev}^{{commit}}").decode().strip()
        raw = _git(repo, "ls-tree", "-r", "-z", "--name-only", self.rev).decode("utf-8", "replace")
        self.paths = frozenset(p for p in raw.split("\0") if p)
        wanted = sorted(p for p in self.paths if _read_text(p))
        out = _git(repo, "cat-file", "--batch", data="".join(f"{self.rev}:{p}\n" for p in wanted).encode())
        self.text, i = {}, 0
        for p in wanted:
            j = out.index(b"\n", i)
            header = out[i:j].split()
            if len(header) < 3 or header[1] != b"blob":
                i = j + 1
                continue
            size = int(header[2])
            self.text[p] = out[j + 1:j + 1 + size].decode("utf-8", "replace")
            i = j + 1 + size + 1
        self.dirs = frozenset("/".join(p.split("/")[:k]) for p in self.paths for k in range(1, p.count("/") + 1))


# --------------------------------------------------------------------------
# Bounded path evaluator (NOT a general constant evaluator)
# --------------------------------------------------------------------------

_PATH_CALLS = {"Path", "pathlib.Path", "PurePath", "str", "os.fspath", "os.path.abspath", "os.path.realpath",
               "os.path.normpath", "os.path.expanduser"}


def _norm(p):
    if p is None:
        return None
    p = posixpath.normpath(p.replace("\\", "/")) if p else ""
    if p in (".", ""):
        return ""
    if p.startswith("../") or p == ".." or p.startswith("/"):
        return None
    return p


def _eval_path(node, consts, here):
    """Evaluate a path expression built ONLY from string literals, module
    constants, `__file__` and the fixed pathlib/os.path forms below. Returns a
    repository-relative string (possibly still containing glob characters) or
    None when the value cannot be proven."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return _norm(node.value)
    if isinstance(node, ast.Name):
        if node.id == "__file__":
            return here
        return consts.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left, right = _eval_path(node.left, consts, here), _eval_path(node.right, consts, here)
        return None if left is None or right is None else _norm(posixpath.join(left, right))
    if isinstance(node, ast.Attribute) and node.attr == "parent":
        inner = _eval_path(node.value, consts, here)
        return None if inner is None else _norm(posixpath.dirname(inner))
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute) and node.value.attr == "parents" \
            and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, int):
        inner = _eval_path(node.value.value, consts, here)
        if inner is None:
            return None
        for _ in range(node.slice.value + 1):
            inner = posixpath.dirname(inner)
        return _norm(inner)
    if isinstance(node, ast.Call):
        fn = ast.unparse(node.func)
        if isinstance(node.func, ast.Attribute) and node.func.attr in ("resolve", "absolute") and not node.args:
            return _eval_path(node.func.value, consts, here)
        if isinstance(node.func, ast.Attribute) and node.func.attr == "joinpath":
            parts = [_eval_path(node.func.value, consts, here)] + [_eval_path(a, consts, here) for a in node.args]
            return None if None in parts else _norm(posixpath.join(*parts))
        if fn == "os.path.join" and node.args:
            parts = [_eval_path(a, consts, here) for a in node.args]
            return None if None in parts else _norm(posixpath.join(*parts))
        if fn == "os.path.dirname" and len(node.args) == 1:
            inner = _eval_path(node.args[0], consts, here)
            return None if inner is None else _norm(posixpath.dirname(inner))
        if fn in _PATH_CALLS and len(node.args) == 1:
            return _eval_path(node.args[0], consts, here)
    return None


def _glob_dir(pattern):
    """Deterministic directory of a glob pattern: the part before its first wildcard."""
    cut = re.split(r"[*?\[]", pattern, maxsplit=1)[0]
    return _norm(cut if cut.endswith("/") or cut == pattern else posixpath.dirname(cut))


# --------------------------------------------------------------------------
# Evidence graph
# --------------------------------------------------------------------------


class EvidenceGraph:
    def __init__(self, snap):
        self.snap = snap
        self.edges = []
        self.uncertainties = []
        self.parse_failures = []
        self.unresolved_imports = []
        self.external_literal_imports = 0
        self.fixture_defs = collections.defaultdict(dict)   # conftest -> {fixture: autouse}
        self.fixture_requests = collections.defaultdict(set)
        self.local_fixtures = collections.defaultdict(set)
        self.hooks = collections.defaultdict(set)           # file -> hook / plugin declarations
        self.persistence = set()
        self.artifact_failures = []
        self.artifacts_analysed = []
        self._strings = collections.defaultdict(list)
        self.python = sorted(p for p in snap.paths if p.endswith(".py"))
        self.tests = sorted(p for p in self.python if p.startswith("tests/") and p.split("/")[-1].startswith("test_"))
        self.modules = {}
        for f in self.python:
            name = f[:-3].replace("/", ".")
            self.modules[name[:-9] if name.endswith(".__init__") else name] = f
        self._top_level = {m.split(".")[0] for m in self.modules} | {d for d in snap.dirs if "/" not in d}
        for f in self.python:
            self._python(f)
        self._fixture_edges()
        self._artifacts()
        self._documents()
        self._bind_discovery()
        self.edges = sorted({tuple(sorted(e.items())) for e in self.edges})
        self.edges = [dict(e) for e in self.edges]
        self.uncertainties = sorted(self.uncertainties, key=lambda u: (u["source"], u["location"], u["kind"], u["detail"]))
        self.reverse = collections.defaultdict(set)
        self.forward = collections.defaultdict(set)
        for e in self.edges:
            if e["resolution_status"] == "resolved":
                self.reverse[e["target"]].add(e["source"])
                self.forward[e["source"]].add(e["target"])

    # -- recording -----------------------------------------------------------------
    def _edge(self, source, target, etype, location, rule, status="resolved"):
        assert etype in EDGE_TYPES, etype
        if target == source:
            return
        self.edges.append({"source": source, "target": target, "type": etype, "source_location": location,
                           "derivation_rule": rule, "resolution_status": status})

    def _uncertain(self, source, location, kind, detail, scope):
        self.uncertainties.append({"source": source, "location": location, "kind": kind,
                                   "detail": detail[:160], "scope": scope, "binding": None})

    # -- strict module resolution ------------------------------------------------------------
    def module_file(self, dotted):
        """Exact resolution only: `pkg/__init__.py` never stands in for `pkg.missing`."""
        return self.modules.get(dotted)

    def _candidates(self, dotted, importer):
        cands = [dotted]
        if importer.startswith("tests/"):
            here = posixpath.dirname(importer).replace("/", ".")
            cands.append(f"{here}.{dotted}")
        return cands

    def _is_repo_local(self, dotted, importer):
        top = dotted.split(".")[0]
        if top in self._top_level:
            return True
        return importer.startswith("tests/") and f"{posixpath.dirname(importer).replace('/', '.')}.{top}" in self.modules

    def is_namespace_package(self, dotted):
        """A tracked directory of modules without `__init__.py` (PEP 420)."""
        path = dotted.replace(".", "/")
        return dotted not in self.modules and path in self.snap.dirs and any(
            p.startswith(path + "/") and p.endswith(".py") for p in self.python)

    def _import(self, f, loc, dotted, names=None):
        """Record `import dotted` / `from dotted import names`. Returns True when resolved."""
        for cand in self._candidates(dotted, f):
            target = self.module_file(cand)
            if target is None and self.is_namespace_package(cand):
                ok = True
                for n in names or ():                              # from <namespace> import <submodule>
                    sub = self.module_file(f"{cand}.{n}")
                    if sub:
                        self._edge(f, sub, "import", loc, "ast-import-submodule")
                    elif not self.is_namespace_package(f"{cand}.{n}"):
                        self.unresolved_imports.append({"location": loc, "module": f"{cand}.{n}"})
                        ok = False
                return ok
            if target is None:
                continue
            parts = cand.split(".")
            for k in range(1, len(parts)):                       # parents are imported too
                parent = self.module_file(".".join(parts[:k]))
                if parent:
                    self._edge(f, parent, "import", loc, "ast-import-parent-package")
            self._edge(f, target, "import", loc, "ast-import")
            for n in names or ():
                sub = self.module_file(f"{cand}.{n}")
                if sub:
                    self._edge(f, sub, "import", loc, "ast-import-submodule")
            return True
        if self._is_repo_local(dotted, f):
            self.unresolved_imports.append({"location": loc, "module": dotted})
        return False

    # -- python -------------------------------------------------------------------------------
    def _python(self, f):
        src = self.snap.text.get(f, "")
        try:
            tree = ast.parse(src)
        except SyntaxError:
            self.parse_failures.append(f)
            return
        docstrings = set()
        for n in ast.walk(tree):
            for child in ast.iter_child_nodes(n):
                child._rig_parent = n
            if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and n.body \
                    and isinstance(n.body[0], ast.Expr) and isinstance(n.body[0].value, ast.Constant) \
                    and isinstance(n.body[0].value.value, str):
                docstrings.add(id(n.body[0].value))
        consts = {}
        for stmt in tree.body:                                     # module constants: literal paths only
            if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Name):
                v = _eval_path(stmt.value, consts, f)
                if v is not None:
                    consts[stmt.targets[0].id] = v
        package = posixpath.dirname(f).replace("/", ".")
        is_conftest = f.split("/")[-1] == "conftest.py"
        for n in ast.walk(tree):
            loc = f"{f}:{getattr(n, 'lineno', 0)}"
            if isinstance(n, ast.Import):
                for a in n.names:
                    self._import(f, loc, a.name)
            elif isinstance(n, ast.ImportFrom):
                base = n.module or ""
                if n.level:
                    pkg_parts = package.split(".") if package else []
                    keep = len(pkg_parts) - (n.level - 1)
                    if keep < 0:
                        self.unresolved_imports.append({"location": loc, "module": "." * n.level + base})
                        continue
                    base = ".".join([*pkg_parts[:keep], *( [base] if base else [])])
                if base:
                    self._import(f, loc, base, [a.name for a in n.names])
            elif isinstance(n, ast.Call):
                self._call(f, loc, n, consts)
            elif isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docstrings:
                self._strings[f].append(n.value)
                if not f.startswith("tests/") and re.search(r"\bCREATE\s+TABLE\b", n.value, re.I):
                    self.persistence.add(f)
                for m in re.findall(r"(?<![\w/.])((?:[\w.-]+/)*[\w.-]+\.(?:py|json|jsonl|yml|yaml|sql|txt|html|js|sh|ini|csv|md|toml))\b", n.value):
                    if m in self.snap.paths:
                        self._edge(f, m, "literal_path", loc, "string-literal-path")
                d = _norm(n.value)
                if d and n.value.endswith("/") and d in self.snap.dirs:
                    self._uncertain(f, loc, "directory-reference", n.value, "dir:" + d)
            elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div) and not isinstance(getattr(n, "_rig_parent", None), ast.BinOp):
                p = _eval_path(n, consts, f)
                if p is not None and p in self.snap.paths:
                    self._edge(f, p, "literal_path", loc, "path-expression")
                elif p and p in self.snap.dirs:
                    self._uncertain(f, loc, "directory-reference", ast.unparse(n), "dir:" + p)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                decorators = [ast.unparse(d) for d in n.decorator_list]
                is_fixture = any(re.search(r"\bfixture\b", d) for d in decorators)
                if is_fixture:
                    if is_conftest:
                        self.fixture_defs[f][n.name] = any("autouse=True" in d for d in decorators)
                    else:
                        self.local_fixtures[f].add(n.name)
                if is_conftest and n.name.startswith("pytest_"):
                    self.hooks[f].add(n.name)
                if n.name.startswith("test") or is_fixture:
                    self.fixture_requests[f].update(a.arg for a in n.args.args if a.arg not in ("self", "cls", "request"))
                for d in decorators:
                    for group in re.findall(r"usefixtures\(([^)]*)\)", d):
                        self.fixture_requests[f].update(re.findall(r"['\"](\w+)['\"]", group))
                    if "parametrize" in d and "indirect=True" in d:
                        m = re.search(r"parametrize\(\s*['\"]([\w, ]+)['\"]", d)
                        if m:
                            self.fixture_requests[f].update(x.strip() for x in m.group(1).split(","))
            if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "pytest_plugins" for t in n.targets):
                self.hooks[f].add("pytest_plugins")

    def _call(self, f, loc, n, consts):
        fn = ast.unparse(n.func)
        short = fn.split(".")[-1]
        a0 = n.args[0] if n.args else None
        lit = a0.value if isinstance(a0, ast.Constant) and isinstance(a0.value, str) else None
        text = ast.unparse(n)
        if short in ("import_module", "__import__"):
            if lit is not None:
                if not self._import(f, loc, lit):
                    if not self._is_repo_local(lit, f):
                        self.external_literal_imports += 1
            else:
                scope = "repo"
                if isinstance(a0, ast.BinOp) and isinstance(a0.left, ast.Constant) and isinstance(a0.left.value, str):
                    scope = "prefix:" + a0.left.value
                elif isinstance(a0, ast.JoinedStr) and a0.values and isinstance(a0.values[0], ast.Constant):
                    scope = "prefix:" + a0.values[0].value
                self._uncertain(f, loc, "computed-dynamic-import", text, scope)
        elif short in ("spec_from_file_location", "run_path"):
            arg = n.args[1] if short == "spec_from_file_location" and len(n.args) > 1 else a0
            p = _eval_path(arg, consts, f) if arg is not None else None
            if p is not None and p in self.snap.paths:
                self._edge(f, p, "literal_path", loc, "literal-spec-path")
            else:
                self._uncertain(f, loc, "unresolved-spec-path", text, "repo")
        elif fn.startswith("subprocess.") or fn in ("os.system", "Popen", "check_output", "check_call"):
            self._subprocess(f, loc, n, consts, text)
        elif short == "register_blueprint":
            self._uncertain(f, loc, "flask-registration", text, "application")
        elif short == "setattr" and fn.endswith("monkeypatch.setattr") and lit is not None and "." in lit:
            parts = lit.split(".")
            for k in range(len(parts) - 1, 0, -1):
                target = self.module_file(".".join(parts[:k]))
                if target:
                    self._edge(f, target, "literal_path", loc, "monkeypatch-string-target")
                    break
            else:
                if self._is_repo_local(lit, f):
                    self._uncertain(f, loc, "unresolved-monkeypatch-target", lit, "repo")
        elif short == "getfixturevalue":
            if lit is not None:
                self.fixture_requests[f].add(lit)
            else:
                self._uncertain(f, loc, "dynamic-fixture-lookup", text, "fixtures")
        elif short == "render_template":
            if lit is not None:
                path = posixpath.join(posixpath.dirname(f), "templates", lit)
                if path in self.snap.paths:
                    self._edge(f, path, "literal_path", loc, "flask-default-template-folder")
                else:
                    self._uncertain(f, loc, "unresolved-template", lit, "templates")
            else:
                self._uncertain(f, loc, "unresolved-template", text, "templates")
        elif short in ("scandir", "listdir", "iterdir", "glob", "rglob", "walk", "iglob") and not fn.startswith("ast."):
            self._discovery(f, loc, n, consts, text, short)

    def _subprocess(self, f, loc, n, consts, text):
        found = False
        argv = n.args[0] if n.args else None
        items = argv.elts if isinstance(argv, (ast.List, ast.Tuple)) else ([argv] if argv is not None else [])
        values = [_eval_path(x, consts, f) for x in items]
        for v in values:
            if v and v in self.snap.paths and v.endswith((".py", ".sh")):
                self._edge(f, v, "literal_path", loc, "subprocess-literal-script")
                found = True
        for i, v in enumerate(values[:-1]):
            if v == "-m" and values[i + 1] and self._import(f, loc, values[i + 1]):
                found = True
        first = items[0] if items else None
        external_tool = isinstance(first, ast.Constant) and isinstance(first.value, str) \
            and first.value not in ("python", "python3") and _norm(first.value) not in self.snap.paths
        if not found and not external_tool:
            self._uncertain(f, loc, "unknown-subprocess-target", text, "repo")

    def _discovery(self, f, loc, n, consts, text, short):
        target = None
        if short in ("glob", "iglob") and isinstance(n.func, ast.Attribute) and ast.unparse(n.func.value) == "glob" and n.args:
            pat = _eval_path(n.args[0], consts, f)
            target = _glob_dir(pat) if pat is not None else None
        elif isinstance(n.func, ast.Attribute) and short in ("glob", "rglob", "iterdir"):
            target = _eval_path(n.func.value, consts, f)
        elif n.args:
            target = _eval_path(n.args[0], consts, f)
        if target is not None and (target == "" or target in self.snap.dirs):
            self._uncertain(f, loc, "runtime-discovery", text, "repo" if target == "" else "dir:" + target)
            self.uncertainties[-1]["binding"] = "evaluated-literal"
        else:
            self._uncertain(f, loc, "runtime-discovery", text, "unbound")

    def _bind_discovery(self):
        """Caller-literal binding: an unbound discovery call in module M binds to
        the literal directories referenced by M itself or by M's importers."""
        dirs = collections.defaultdict(set)
        for u in self.uncertainties:
            if u["kind"] == "directory-reference":
                dirs[u["source"]].add(u["scope"])
        importers = collections.defaultdict(set)
        for e in self.edges:
            if e["type"] == "import":
                importers[e["target"]].add(e["source"])
        for u in self.uncertainties:
            if u["kind"] == "runtime-discovery" and u["scope"] == "unbound":
                own = dirs.get(u["source"], set())
                callers = set().union(*[dirs.get(c, set()) for c in importers.get(u["source"], ())]) if importers.get(u["source"]) else set()
                bound = own or callers
                u["binding"] = "own-literal" if own else ("caller-literal" if callers else "unbound")
                u["scope"] = "repo" if not bound else "|".join(sorted(bound))

    # -- pytest -------------------------------------------------------------------------------------
    def _conftests_for(self, f):
        d = posixpath.dirname(f)
        out = []
        while True:
            c = posixpath.join(d, "conftest.py") if d else "conftest.py"
            if c in self.fixture_defs or c in self.snap.paths:
                out.append(c)
            if not d:
                return out
            d = posixpath.dirname(d)

    def _fixture_edges(self):
        for f in sorted(self.fixture_requests):
            for name in sorted(self.fixture_requests[f]):
                if name in self.local_fixtures.get(f, ()):
                    continue                                       # module-local definition shadows conftest
                for c in self._conftests_for(f):
                    if c != f and name in self.fixture_defs.get(c, {}):
                        self._edge(f, c, "fixture_use", f, f"fixture-request:{name}")
                        break
        for c in sorted(self.fixture_defs):
            if any(self.fixture_defs[c].values()):
                scope = posixpath.dirname(c)
                for t in self.tests:
                    if not scope or t.startswith(scope + "/"):
                        self._edge(t, c, "fixture_use", c, "autouse-fixture")

    # -- artifacts -----------------------------------------------------------------------------------
    def _artifacts(self):
        for p in sorted(self.snap.text):
            src = self.snap.text[p]
            if p.startswith(".github/workflows/"):
                self.artifacts_analysed.append(p)
                for m in re.findall(r"-r\s+([\w./-]+\.txt)", src):
                    self._artifact_ref(p, m, "pip-install-r")
                for m in re.findall(r"python3?\s+([\w./-]+\.py)\b", src):
                    self._artifact_ref(p, m, "python-script")
                if re.search(r"-m['\",\s]+pytest|\bpytest\b", src):
                    for t in self.tests:                           # the workflow depends on the tests it runs
                        self._edge(p, t, "artifact_reference", p, "pytest-invocation")
            elif p == "Dockerfile":
                self.artifacts_analysed.append(p)
                for line in src.splitlines():
                    m = re.match(r"\s*COPY\s+(?!--)(.+?)\s+(\S+)\s*$", line)
                    if not m:
                        continue
                    for s in m.group(1).split():
                        if s == ".":
                            self._uncertain(p, p, "broad-build-input", line.strip(), "repo")
                        else:
                            self._artifact_ref(p, s.rstrip("/"), "docker-copy")
                g = re.search(r'CMD\s*\[[^\]]*"-c",\s*"([^"]+)"[^\]]*"([\w.]+):(\w+)"', src)
                if g:
                    self._artifact_ref(p, g.group(1), "gunicorn-config")
                    target = self.module_file(g.group(2))
                    if target:
                        self._edge(p, target, "artifact_reference", p, "runtime-entrypoint")
                    else:
                        self.artifact_failures.append({"artifact": p, "reference": g.group(2), "rule": "runtime-entrypoint"})
            elif p == "pytest.ini":
                self.artifacts_analysed.append(p)
                if re.search(r"^\s*testpaths\s*=", src, re.M):
                    for t in self.tests:
                        self._edge(t, p, "artifact_reference", p, "pytest-testpaths")

    def _artifact_ref(self, artifact, target, rule):
        if target in self.snap.paths:
            self._edge(artifact, target, "artifact_reference", artifact, rule)
        elif target in self.snap.dirs:
            self._uncertain(artifact, artifact, "broad-build-input", f"{rule}: {target}/", "dir:" + target)
        else:
            self.artifact_failures.append({"artifact": artifact, "reference": target, "rule": rule})

    # -- documents ----------------------------------------------------------------------------------------
    def _documents(self):
        by_name = collections.defaultdict(list)
        for p in self.snap.paths:
            if p.endswith(".md"):
                by_name[p.split("/")[-1]].append(p)
        for f in self.python:
            names = set()
            for s in self._strings.get(f, ()):                    # executable string literals only
                names.update(re.findall(r"[\w.-]+\.md\b", s))
            for name in sorted(names):
                cands = sorted(by_name.get(name, ()))
                rule = "document-name-unique" if len(cands) == 1 else "document-name-ambiguous-superset"
                for c in cands:
                    self._edge(f, c, "literal_path", f, rule)

    # -- queries ------------------------------------------------------------------------------------------
    def dependents(self, target):
        seen, stack = {}, [target]
        while stack:
            x = stack.pop()
            for y in sorted(self.reverse.get(x, ())):
                if y not in seen and y != target:
                    seen[y] = x
                    stack.append(y)
        return seen                                                # dependent -> the node it reached through

    def completeness(self):
        tracked_tests = len(self.tests)
        parsed_tests = len([t for t in self.tests if t not in self.parse_failures])
        return {
            "revision": self.snap.rev,
            "contract_version": CONTRACT_VERSION,
            "tool_version": TOOL_VERSION,
            "tracked_python": len(self.python),
            "parsed_python": len(self.python) - len(self.parse_failures),
            "tracked_tests": tracked_tests,
            "parsed_tests": parsed_tests,
            "parse_failures": sorted(self.parse_failures),
            "unresolved_imports": sorted(self.unresolved_imports, key=lambda x: (x["location"], x["module"])),
            "unresolved_dynamic_targets": dict(sorted(collections.Counter(
                u["kind"] for u in self.uncertainties if u["kind"] != "directory-reference").items())),
            "artifacts_analysed": sorted(set(self.artifacts_analysed)),
            "artifact_failures": sorted(self.artifact_failures, key=lambda x: (x["artifact"], x["reference"])),
            "external_literal_imports": self.external_literal_imports,
            "environment_assumptions": list(ENVIRONMENT_ASSUMPTIONS),
            "status": "complete" if not self.parse_failures and not self.unresolved_imports and not self.artifact_failures
                      else "complete-with-reported-gaps",
        }

    def summary(self):
        return {
            "edges_by_type": dict(sorted(collections.Counter(e["type"] for e in self.edges).items())),
            "edges_by_rule": dict(sorted(collections.Counter(e["derivation_rule"].split(":")[0] for e in self.edges).items())),
            "uncertainties_by_kind": dict(sorted(collections.Counter(u["kind"] for u in self.uncertainties).items())),
            "uncertainty_scopes": dict(sorted(collections.Counter(u["scope"].split(":")[0] for u in self.uncertainties).items())),
        }


# --------------------------------------------------------------------------
# Impact resolver (BASE ∪ HEAD)
# --------------------------------------------------------------------------


def _covers(u, path):
    scope = u["scope"]
    if u["kind"] in CODE_LOADING_KINDS and not path.endswith((".py", ".sh")):
        return False
    if scope == "repo":
        return True
    if scope.startswith("prefix:"):
        mod = path[:-3].replace("/", ".") if path.endswith(".py") else None
        if mod and mod.endswith(".__init__"):
            mod = mod[:-9]
        return bool(mod and mod.startswith(scope[len("prefix:"):]))
    if scope == "templates":
        return "/templates/" in path
    if scope == "fixtures":
        return path.split("/")[-1] == "conftest.py"
    if scope == "application":
        return path.startswith("web/")
    return any(path.startswith(d[len("dir:"):].rstrip("/") + "/") or path == d[len("dir:"):]
               for d in scope.split("|") if d.startswith("dir:"))


def name_status(repo, base, head):
    raw = _git(repo, "diff", "--name-status", "-M", "-z", base, head).decode("utf-8", "replace").split("\0")
    out, i = [], 0
    while i < len(raw) and raw[i]:
        status = raw[i]
        if status[0] in "RC":
            out.append({"status": status[0], "old": raw[i + 1], "new": raw[i + 2]})
            i += 3
        else:
            out.append({"status": status[0], "old": raw[i + 1], "new": raw[i + 1]})
            i += 2
    return out


def resolve_impact(gb, gh, changes):
    changed = sorted({p for c in changes for p in (c["old"], c["new"])})
    impacted, via, widening = set(), {}, []
    for p in changed:
        for side, g in (("base", gb), ("head", gh)):
            for dep, through in g.dependents(p).items():
                if dep not in impacted:
                    via.setdefault(dep, f"{side}:{through}")
                impacted.add(dep)
            for u in g.uncertainties:
                if u["source"] != p and _covers(u, p):
                    observers = {u["source"]} | set(g.dependents(u["source"]))
                    widening.append({"side": side, "changed_path": p, "kind": u["kind"], "source": u["source"],
                                     "location": u["location"], "scope": u["scope"], "observers": len(observers)})
                    for o in observers:
                        via.setdefault(o, f"{side}:uncertainty:{u['kind']}@{u['source']}")
                    impacted |= observers
    return changed, impacted, via, widening


# --------------------------------------------------------------------------
# Policy / safety layer (separate from graph construction)
# --------------------------------------------------------------------------


def _protected_class(path):
    name = path.split("/")[-1]
    if path in RIG_SELF_PATHS:
        return "rig-self-certification"
    if path in MANDATORY_GUARDRAILS:
        return "mandatory-guardrail"
    if path in DECLARED_STATE_CONTRACT:
        return "state/record/persistence-contract"
    if name == "__init__.py":
        return "package-initializer"
    for pattern, cls in PROTECTED_PATTERNS:
        if fnmatch.fnmatch(path, pattern):
            return cls
    return None


def _module_paths(module, importer):
    """Candidate tracked paths a dotted module name could denote (for explaining broken imports)."""
    base = module.replace(".", "/")
    out = {base + ".py", base + "/__init__.py"}
    if importer.startswith("tests/"):
        here = posixpath.dirname(importer)
        out |= {posixpath.join(here, base) + ".py", posixpath.join(here, base, "__init__.py")}
    return out


def decide(gb, gh, changes, changed, impacted, widening):
    """Ordered advisory policy. Returns (scope, reasons, qualification)."""
    head_tests = set(gh.tests)
    all_tests = set(gb.tests) | head_tests
    n_tests = max(1, len(head_tests))
    limit = CENTRALITY_ESCALATION_SHARE * n_tests
    full, qualification = [], []
    deleted_or_moved = {c["old"] for c in changes if c["status"] in ("D", "R")}

    # 1. health / completeness of the analysis for THIS change
    for p in changed:
        if p.endswith(".py") and p in gh.parse_failures:
            full.append(f"analysis-incomplete: changed file does not parse at head: {p}")
    concerned = set(changed) | impacted
    for u in gh.unresolved_imports:
        src = u["location"].rsplit(":", 1)[0]
        if src not in concerned:
            continue
        if not (_module_paths(u["module"], src) & deleted_or_moved):   # explained only by this change's delete/rename
            full.append(f"analysis-incomplete: unresolved repository import at head: {u['module']} ({u['location']})")
    # 2. protected triggers
    for c in changes:
        for p in {c["old"], c["new"]}:
            cls = _protected_class(p)
            if cls:
                full.append(f"protected:{cls}: {p}")
            if p.split("/")[-1] == "conftest.py":
                for g in (gb, gh):
                    if any(g.fixture_defs.get(p, {}).values()) or g.hooks.get(p):
                        full.append(f"protected:autouse-or-hook-conftest: {p}")
            for g in (gb, gh):
                if g.hooks.get(p) and "pytest_plugins" in g.hooks[p]:
                    full.append(f"protected:pytest-plugins: {p}")
                if p in g.persistence:
                    full.append(f"protected:persistence-ddl: {p}")
                if any(e["derivation_rule"] == "runtime-entrypoint" and e["target"] == p for e in g.edges):
                    full.append(f"protected:runtime-entrypoint: {p}")
                if any(u["kind"] == "flask-registration" and u["source"] == p for u in g.uncertainties):
                    full.append(f"protected:application-registration: {p}")
            if not (p.endswith(ANALYSED_SUFFIXES) or p.split("/")[-1] in ANALYSED_NAMES):
                full.append(f"unclassified-changed-path: {p}")
    # 3. material uncertainty
    for w in widening:
        g = gb if w["side"] == "base" else gh
        observers = {w["source"]} | set(g.dependents(w["source"]))
        obs_tests = observers & all_tests
        if len(obs_tests) > limit or observers & set(DECLARED_STATE_CONTRACT) or _protected_class(w["source"]) == "state/record/persistence-contract":
            full.append(f"material-uncertainty: {w['kind']} in {w['source']} (scope {w['scope']}) is observed by central or protected code")
    # centrality escalation (may escalate; low centrality never authorizes anything)
    for p in changed:
        reach = {d for g in (gb, gh) for d in g.dependents(p) if d in all_tests}
        if len(reach) > limit:
            full.append(f"centrality-escalation: {p} reaches {len(reach)}/{n_tests} tests "
                        f"(> CENTRALITY_ESCALATION_SHARE={CENTRALITY_ESCALATION_SHARE}, provisional advisory constant)")
    # passive documentation
    passive = []
    for p in changed:
        if not p.endswith(".md"):
            continue
        consumers = set(gb.dependents(p)) | set(gh.dependents(p))
        readers = [w for w in widening if w["changed_path"] == p and w["kind"] not in BUILD_ONLY_KINDS]
        if not consumers and not readers:
            passive.append(p)
    # positive qualification for everything that is not passive documentation
    for p in changed:
        if p in passive or _protected_class(p):
            continue
        if p in head_tests:
            qualification.append(f"{p}: changed test (selected itself)")
            continue
        pair = {p} | {c["old"] for c in changes if c["status"] == "R" and c["new"] == p} \
            | {c["new"] for c in changes if c["status"] == "R" and c["old"] == p}  # a rename is one entity
        reach = {d for g in (gb, gh) for q in pair for d in g.dependents(q) if d in all_tests}
        bounded_readers = sorted({w["source"] for w in widening if w["changed_path"] == p and w["scope"] != "repo"
                                  and w["kind"] not in BUILD_ONLY_KINDS})
        if reach:
            qualification.append(f"{p}: {len(reach)} test(s) reached through resolved evidence")
        elif not p.endswith(".py") and bounded_readers:
            qualification.append(f"{p}: bounded directory reader(s) {bounded_readers}")
        else:
            full.append(f"no-positive-evidence: no test is proven to exercise {p}")
    full = sorted(set(full))
    if full:
        scope = "FULL"
    elif changed and all(p in passive for p in changed):
        scope = "SMOKE"
    elif qualification:
        scope = "AFFECTED-CANDIDATE"
    else:
        scope = "FULL"
        full = ["no-positive-evidence: nothing qualified the change"]
    return scope, full, sorted(set(qualification)), sorted(passive)


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------

DISCLAIMER = ("ADVISORY ONLY. RIG has no CI authority: nothing was skipped, selected or run. The candidate tests "
              "are those proven by evidence plus uncertainty observers; they are not claimed to be all affected "
              "tests, and no change is claimed to be safe.")


def analyse(repo, base, head):
    sb, sh = Snapshot(repo, base), Snapshot(repo, head)
    gb, gh = EvidenceGraph(sb), EvidenceGraph(sh)
    changes = name_status(repo, sb.rev, sh.rev)
    changed, impacted, via, widening = resolve_impact(gb, gh, changes)
    scope, reasons, qualification, passive = decide(gb, gh, changes, changed, impacted, widening)
    head_tests = set(gh.tests)
    candidate_tests = sorted((impacted | set(changed)) & head_tests)
    evidence_tests = sorted({t for p in changed for g in (gb, gh) for t in g.dependents(p) if t in head_tests} | (set(changed) & head_tests))
    affected_source = sorted(p for p in impacted if p not in head_tests and p not in set(gb.tests) and (p in sh.paths or p in sb.paths))
    upstream = sorted({f"{e['target']} <- {e['source']} [{e['type']}:{e['derivation_rule']}]"
                       for g in (gb, gh) for e in g.edges if e["source"] in changed and e["resolution_status"] == "resolved"})
    downstream = sorted({f"{d} -> {p}" for p in changed for g in (gb, gh) for d in g.reverse.get(p, ())})
    artifact_consumers = sorted({f"{e['source']} -> {e['target']} [{e['derivation_rule']}]"
                                 for g in (gb, gh) for e in g.edges
                                 if e["type"] == "artifact_reference" and e["target"] in changed and not e["source"].startswith("tests/")})
    central = any(r.startswith(("centrality-escalation", "protected:")) for r in reasons)
    code_changed = [p for p in changed if p.endswith(".py") and p not in head_tests and p in sh.paths]
    read_first = (code_changed + [t for t in changed if t in head_tests]
                  + sorted({e["target"] for e in gh.edges if e["source"] in code_changed and e["type"] == "import"})
                  + [t for t in evidence_tests if t not in changed])
    seen, suggested = set(), []
    for p in read_first:
        if p not in seen:
            seen.add(p)
            suggested.append(p)
    try:
        recent = _git(repo, "log", "-n", "5", "--format=%H %s", sh.rev, "--", *changed).decode().strip().splitlines() if changed else []
    except AnalysisUnavailable:
        recent = []
    widen_summary = sorted({f"{w['kind']} in {w['source']} (scope {w['scope']})" for w in widening})
    return {
        "rig": {"contract_version": CONTRACT_VERSION, "tool_version": TOOL_VERSION, "authority": "advisory-only"},
        "identity": {"base": sb.rev, "head": sh.rev},
        "analysis_health": {"base": gb.completeness(), "head": gh.completeness()},
        "changed_paths": [dict(sorted(c.items())) for c in changes],
        "evidence_summary": {"base": gb.summary(), "head": gh.summary()},
        "affected_source_files": affected_source,
        "candidate_tests": candidate_tests,
        "evidence_tests": evidence_tests,
        "candidate_test_evidence": {t: via.get(t, "changed") for t in candidate_tests},
        "artifact_consumers": artifact_consumers,
        "central_or_shared": central,
        "uncertainties_in_scope": widen_summary,
        "scope_widening": {"widened_by": len(widen_summary),
                           "observer_tests_added": len(set(candidate_tests) - set(evidence_tests))},
        "advisory_scope": scope,
        "policy_reasons": reasons,
        "qualification_evidence": qualification,
        "passive_documents": passive,
        "agent_context": {
            "revision": sh.rev,
            "changed_paths": changed,
            "relevant_source": affected_source[:50],
            "candidate_tests": candidate_tests,
            "upstream_dependencies": upstream[:60],
            "downstream_dependents": downstream[:60],
            "artifact_consumers": artifact_consumers,
            "central_or_shared": central,
            "uncertainties": widen_summary,
            "suggested_files_to_read_first": suggested[:10],
            "recent_commits": recent,
            "not_claimed": ["all affected files", "all affected tests", "safe change", "complete capability"],
        },
        "disclaimer": DISCLAIMER,
    }


def health(repo, rev):
    g = EvidenceGraph(Snapshot(repo, rev))
    return {"rig": {"contract_version": CONTRACT_VERSION, "tool_version": TOOL_VERSION, "authority": "advisory-only"},
            "analysis_health": g.completeness(), "evidence_summary": g.summary()}


def _dump(obj):
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)


def main(argv=None):
    p = argparse.ArgumentParser(description="Advisory repository intelligence (RIG). Read-only; no CI authority.")
    p.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    p.add_argument("--base")
    p.add_argument("--head")
    p.add_argument("--health", metavar="REV")
    args = p.parse_args(argv)
    try:
        if args.health:
            report = health(args.repo, args.health)
        elif args.base and args.head:
            report = analyse(args.repo, args.base, args.head)
        else:
            p.error("give --base and --head, or --health")
    except AnalysisUnavailable as exc:
        print(_dump({"analysis_status": "unavailable", "advisory_scope": "FULL", "reason": str(exc),
                     "rig": {"contract_version": CONTRACT_VERSION, "tool_version": TOOL_VERSION, "authority": "advisory-only"}}))
        return 2
    print(_dump(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
