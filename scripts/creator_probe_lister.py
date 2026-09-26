"""Creator probe lister — ADVISORY, READ-ONLY developer tooling (C1-Lite).

Surfaces EXISTING historical adversarial regression tests when a change between
two revisions touches the same risky construct those tests guard.

The canonical regression test itself owns each failure pattern, through ONE
pytest marker (registered in pytest.ini):

    @pytest.mark.failure_pattern(
        "FP-04",
        invariant="an uncertain write is acknowledged only when durable state confirms it",
        constructs=("persistence-writer", "committed-confirmation"))

There is no separate manifest: patterns are read from the markers of test files
at a revision. By default they are read at BASE, so a candidate can neither
erase nor rewrite its own historical obligations: markers that exist only at
HEAD are reported as NEW, and BASE markers that disappear or change at HEAD are
reported as such.

What this tool is NOT: it has zero CI, merge, runtime, review-routing and
test-scope authority. It gives no READY / NOT READY, risk verdict, reviewer or
merge recommendation, and it never selects or skips a test. A match means only
"this known invariant and its canonical test are relevant to read and run" —
never that a defect exists or that the change is safe.

Read-only: every revision is read from git objects through the existing
repository-intelligence Snapshot (scripts/repository_intelligence.py, reused
unchanged); the working tree, the index and refs are never written.

Usage:
    python scripts/creator_probe_lister.py --base REV --head REV [--repo PATH]
                                           [--json] [--patterns-from REV]

Exit status: 0 when the advisory report was produced; 2 when it could not be
(a revision or the repository is unavailable).
"""
import argparse
import ast
import json
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from scripts.repository_intelligence import (  # noqa: E402  (reused, unchanged)
    AnalysisUnavailable, Snapshot, name_status,
)

TOOL_VERSION = "creator-probes-1.0"
AUTHORITY = ("advisory-only: no CI, merge, runtime, review-routing or test-scope "
             "authority; a match is a pointer to a known invariant, not a verdict")

# The closed construct vocabulary. A failure_pattern marker names the families
# its invariant guards; the detectors below recognise them structurally (AST).
FAMILIES = {
    "flask-route": "Flask route handler (a function decorated with .route(...))",
    "signing-domain": "signing / binding domain (a *_DOMAIN or *_KIND string, or the "
                      "domain passed to _canonical_message)",
    "hmac-signature": "HMAC signature mint or verify (hmac.new / compare_digest)",
    "persistence-writer": "append_* persistence writer (INSERT or a _write transaction)",
    "committed-confirmation": "committed-state confirmation logic",
    "commit-recovery": "COMMIT / ROLLBACK / BEGIN IMMEDIATE recovery logic",
    "parsed-identity-accumulation": "dict / set accumulation keyed by a parsed (int()) "
                                    "durable identity",
    "canonical-identifier-parsing": "canonical identifier parsing",
    "supersession-traversal": "supersession / replay traversal",
    "load-validation-boundary": "deserialize / load validation boundary",
}

_ID_RE = re.compile(r"^FP-[0-9]{2}$")
_MARKER = "failure_pattern"
_TEST_FILE_RE = re.compile(r"^tests/(.+/)?test_[^/]+\.py$")


# ---------------------------------------------------------------------------
# failure_pattern markers (the test is the owner)
# ---------------------------------------------------------------------------

def _dotted(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def _is_marker_call(node):
    return isinstance(node, ast.Call) and _dotted(node.func).endswith("mark." + _MARKER)


def _const_str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) \
        else None


def _parse_marker(call):
    """(pattern dict, problem or None) for one decorator call."""
    if len(call.args) != 1 or _const_str(call.args[0]) is None:
        return None, "the pattern ID must be exactly one literal positional string"
    pid = call.args[0].value
    if not _ID_RE.match(pid):
        return None, "pattern ID %r is not of the form FP-NN" % pid
    kw = {k.arg: k.value for k in call.keywords}
    if set(kw) - {"invariant", "constructs"} or None in kw:
        return None, "%s: only invariant= and constructs= keywords are allowed" % pid
    invariant = _const_str(kw.get("invariant"))
    if not invariant or not invariant.strip():
        return None, "%s: invariant= must be a non-empty literal string" % pid
    cnode = kw.get("constructs")
    if not isinstance(cnode, (ast.Tuple, ast.List)) or not cnode.elts:
        return None, "%s: constructs= must be a non-empty literal tuple" % pid
    constructs = [_const_str(e) for e in cnode.elts]
    if None in constructs:
        return None, "%s: constructs= must hold literal strings only" % pid
    unknown = sorted(set(constructs) - set(FAMILIES))
    if unknown:
        return None, "%s: unknown construct families %s" % (pid, unknown)
    if len(set(constructs)) != len(constructs):
        return None, "%s: constructs= repeats a family" % pid
    return {"id": pid, "invariant": invariant.strip(),
            "constructs": tuple(sorted(constructs))}, None


def read_patterns(snapshot):
    """{"owners": [...], "problems": [...]} from every test file at a revision.
    Only a decorator on a collectable test function (test_*, module level or a
    Test* class method) in tests/**/test_*.py can own a pattern; any other use
    of the marker is reported, never silently accepted."""
    owners, problems = [], []
    for path in sorted(p for p in snapshot.text if p.endswith(".py")):
        text = snapshot.text[path]
        if _MARKER not in text:
            continue
        try:
            tree = ast.parse(text)
        except SyntaxError:
            problems.append("%s: test file does not parse; its markers are unreadable" % path)
            continue
        used = set()

        def visit(body, prefix, in_test_class):
            for node in body:
                if isinstance(node, ast.ClassDef):
                    visit(node.body, prefix + node.name + "::",
                          node.name.startswith("Test"))
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for deco in node.decorator_list:
                        if not _is_marker_call(deco):
                            continue
                        used.add(id(deco))
                        nodeid = "%s::%s%s" % (path, prefix, node.name)
                        collectable = (_TEST_FILE_RE.match(path)
                                       and node.name.startswith("test")
                                       and (prefix == "" or in_test_class))
                        if not collectable:
                            problems.append("%s: marker is not on a collectable test" % nodeid)
                            continue
                        pattern, problem = _parse_marker(deco)
                        if problem:
                            problems.append("%s: %s" % (nodeid, problem))
                        else:
                            owners.append(dict(pattern, test=nodeid))
        visit(tree.body, "", False)
        for node in ast.walk(tree):
            if (isinstance(node, ast.Attribute) and node.attr == _MARKER
                    and _dotted(node).endswith("mark." + _MARKER)):
                parent_ok = any(id(d) in used for d in _decorators_using(tree, node))
                if not parent_ok:
                    problems.append("%s:%d: unsupported %s placement (only a test "
                                    "function decorator owns a pattern)"
                                    % (path, node.lineno, _MARKER))
    return _consolidate(owners, problems)


def _decorators_using(tree, attr):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for deco in node.decorator_list:
                if isinstance(deco, ast.Call) and deco.func is attr:
                    yield deco


def _consolidate(owners, problems):
    by_id = {}
    for o in owners:
        by_id.setdefault(o["id"], []).append(o)
    patterns = {}
    for pid, group in sorted(by_id.items()):
        texts = {(o["invariant"], o["constructs"]) for o in group}
        if len(texts) > 1:
            problems.append("%s: conflicting duplicate pattern ID (owners disagree on "
                            "invariant or constructs): %s"
                            % (pid, ", ".join(sorted(o["test"] for o in group))))
            continue
        tests = sorted({o["test"] for o in group})
        if len(tests) != len(group):
            problems.append("%s: the same test carries the pattern more than once" % pid)
        invariant, constructs = texts.pop()
        patterns[pid] = {"id": pid, "invariant": invariant,
                         "constructs": list(constructs), "tests": tests}
    return {"patterns": patterns, "problems": sorted(set(problems))}


# ---------------------------------------------------------------------------
# construct detection (structural, per top-level function / method)
# ---------------------------------------------------------------------------

_DOMAIN_NAME_RE = re.compile(r"^_?[A-Z0-9_]*_(DOMAIN|KIND)$")
_REGEX_NAME_RE = re.compile(r"_RE$")
_LOAD_NAME_RE = re.compile(r"(^|_)(from_dict|load|check|validate)(_|$)")


def _names(node):
    for n in ast.walk(node):
        if isinstance(n, ast.Name):
            yield n.id
        elif isinstance(n, ast.Attribute):
            yield n.attr


def _strings(node):
    for n in ast.walk(node):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            yield n.value


def _calls(node):
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            yield n, _dotted(n.func)


def _has_int_call(node):
    return any(dotted == "int" for _c, dotted in _calls(node))


def function_families(fn):
    """The construct families one function / method exhibits."""
    fams = set()
    names = set(_names(fn))
    strings = set(_strings(fn))
    calls = list(_calls(fn))
    lname = fn.name.lower()
    for deco in fn.decorator_list:
        if isinstance(deco, ast.Call) and _dotted(deco.func).split(".")[-1] == "route":
            fams.add("flask-route")
    for call, dotted in calls:
        last = dotted.split(".")[-1]
        if last == "_canonical_message" and call.args and _const_str(call.args[0]):
            fams.add("signing-domain")
        if (last == "new" and "hmac" in dotted.lower()) or last == "compare_digest":
            fams.add("hmac-signature")
    if any(_DOMAIN_NAME_RE.match(n) for n in names):
        fams.add("signing-domain")
    if fn.name.startswith("append_") and (
            any("INSERT INTO" in s for s in strings) or "_write" in names):
        fams.add("persistence-writer")
    if ({"committed_state_readable", "_refuse_uncommitted_reads"} & names
            or any(n.startswith("committed_") for n in names) or "committed" in lname):
        fams.add("committed-confirmation")
    if {"COMMIT", "ROLLBACK", "BEGIN IMMEDIATE"} & strings or "in_transaction" in names:
        fams.add("commit-recovery")
    for n in ast.walk(fn):
        targets = []
        if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            targets = n.targets if isinstance(n, ast.Assign) else [n.target]
        for t in targets:
            if isinstance(t, ast.Subscript) and _has_int_call(t.slice):
                fams.add("parsed-identity-accumulation")
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr in ("add", "setdefault")
                and n.args and _has_int_call(n.args[0])):
            fams.add("parsed-identity-accumulation")
    uses_regex_match = any(dotted.split(".")[-1] in ("match", "fullmatch")
                           and _REGEX_NAME_RE.search(dotted.split(".")[0] if "." in dotted
                                                     else "")
                           for _c, dotted in calls)
    if ("canonical" in lname or uses_regex_match
            or ("isdigit" in names and _has_int_call(fn))):
        fams.add("canonical-identifier-parsing")
    walks_supersession = False
    for n in ast.walk(fn):
        if isinstance(n, (ast.For, ast.comprehension, ast.While)):
            if {"superseded_by", "supersedes"} & set(_names(n)):
                walks_supersession = True
    if walks_supersession or any(k in lname for k in ("replay", "reconcile",
                                                       "supersession", "reconstruct")):
        fams.add("supersession-traversal")
    if _LOAD_NAME_RE.search(lname):
        fams.add("load-validation-boundary")
    return fams


def module_constructs(text):
    """{(family, qualname): fingerprint} for one module, or raises SyntaxError.
    Constructs are top-level functions, class methods and module-level
    *_DOMAIN / *_KIND string definitions."""
    tree = ast.parse(text)
    out = {}

    def add_function(fn, qual):
        fingerprint = ast.dump(fn, include_attributes=False)
        for fam in function_families(fn):
            key = (fam, qual)
            if fam == "flask-route":
                paths = [_const_str(d.args[0]) for d in fn.decorator_list
                         if isinstance(d, ast.Call) and d.args
                         and _dotted(d.func).split(".")[-1] == "route"]
                key = (fam, "%s [%s]" % (qual, ", ".join(p or "?" for p in paths)))
            out[key] = fingerprint

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            add_function(node, node.name)
        elif isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    add_function(sub, "%s.%s" % (node.name, sub.name))
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if (isinstance(t, ast.Name) and _DOMAIN_NAME_RE.match(t.id)
                        and _const_str(node.value) is not None):
                    out[("signing-domain", t.id)] = ast.dump(node.value)
    return out


def _is_product_source(path):
    return path.endswith(".py") and not path.startswith("tests/")


def changed_constructs(base, head, changes):
    """(constructs, unknown) for the changed product-source Python files.
    A construct is added, removed or changed (its AST fingerprint differs;
    formatting and comments are ignored)."""
    constructs, unknown = [], []
    for ch in changes:
        paths = sorted({ch["old"], ch["new"]})
        if not any(_is_product_source(p) for p in paths):
            continue
        sides = {}
        for label, snap, path in (("base", base, ch["old"]), ("head", head, ch["new"])):
            if ch["status"] == "A" and label == "base" or ch["status"] == "D" and label == "head":
                sides[label] = {}
                continue
            if not _is_product_source(path):
                sides[label] = {}
                continue
            text = snap.text.get(path)
            if text is None:
                unknown.append("%s: source unavailable at %s" % (path, label.upper()))
                sides[label] = None
                continue
            try:
                sides[label] = module_constructs(text)
            except SyntaxError:
                unknown.append("%s: does not parse at %s (AST unavailable)"
                               % (path, label.upper()))
                sides[label] = None
        if sides.get("base") is None or sides.get("head") is None:
            continue
        where = ch["new"] if ch["status"] != "D" else ch["old"]
        b, h = sides["base"], sides["head"]
        for key in sorted(set(b) | set(h)):
            if key not in b:
                change = "added"
            elif key not in h:
                change = "removed"
            elif b[key] != h[key]:
                change = "changed"
            else:
                continue
            constructs.append({"family": key[0], "file": where, "name": key[1],
                               "change": change})
    return constructs, sorted(set(unknown))


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

def build_report(repo, base_rev, head_rev, patterns_rev=None):
    base = Snapshot(repo, base_rev)
    head = Snapshot(repo, head_rev)
    source = base if patterns_rev in (None, base_rev) else Snapshot(repo, patterns_rev)
    owned = read_patterns(source)
    at_head = read_patterns(head)
    constructs, unknown = changed_constructs(base, head, name_status(repo, base.rev, head.rev))
    changed_families = {c["family"] for c in constructs}
    head_test_functions = _test_functions(head)

    matched = []
    for pid, p in sorted(owned["patterns"].items()):
        via = sorted(set(p["constructs"]) & changed_families)
        if via:
            matched.append({"id": pid, "invariant": p["invariant"], "via": via,
                            "tests": [{"test": t, "present_at_head": t in head_test_functions}
                                      for t in p["tests"]]})
    covered = {f for m in matched for f in m["via"]}
    unmatched = sorted({c["family"] for c in constructs} - covered)

    base_ids, head_ids = set(owned["patterns"]), set(at_head["patterns"])
    new_at_head = [at_head["patterns"][i] for i in sorted(head_ids - base_ids)]
    changed_at_head = []
    for pid in sorted(base_ids):
        before = owned["patterns"][pid]
        after = at_head["patterns"].get(pid)
        if after is None:
            changed_at_head.append({"id": pid, "change": "removed at HEAD"})
        elif after != before:
            what = [k for k in ("invariant", "constructs", "tests") if after[k] != before[k]]
            changed_at_head.append({"id": pid, "change": "changed at HEAD: " + ", ".join(what)})
    return {
        "tool_version": TOOL_VERSION,
        "authority": AUTHORITY,
        "base": base.rev, "head": head.rev,
        "patterns_from": source.rev,
        "patterns_from_base": source.rev == base.rev,
        "changed_constructs": constructs,
        "matched_patterns": matched,
        "unmatched_construct_families": unmatched,
        "unknown": unknown,
        "new_patterns_at_head": new_at_head,
        "base_patterns_changed_at_head": changed_at_head,
        "marker_problems": {"base": owned["problems"], "head": at_head["problems"]}
        if source.rev == base.rev else
        {"patterns_source": owned["problems"], "head": at_head["problems"]},
    }


def _test_functions(snapshot):
    """Every collectable test function node id at a revision (for the
    present-at-HEAD check of a BASE-owned canonical test)."""
    ids = set()
    for path, text in snapshot.text.items():
        if not _TEST_FILE_RE.match(path):
            continue
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                    and node.name.startswith("test"):
                ids.add("%s::%s" % (path, node.name))
            elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                            and sub.name.startswith("test"):
                        ids.add("%s::%s::%s" % (path, node.name, sub.name))
    return ids


def render_text(r):
    lines = ["CREATOR PROBE LISTER %s — %s" % (r["tool_version"], r["authority"]),
             "BASE %s" % r["base"], "HEAD %s" % r["head"]]
    if r["patterns_from_base"]:
        lines.append("PATTERNS FROM BASE %s" % r["patterns_from"])
    else:
        lines.append("PATTERNS FROM %s (NOT BASE — replay / what-if use only)"
                     % r["patterns_from"])

    def section(title, rows):
        lines.append("")
        lines.append(title)
        lines.extend(rows if rows else ["  (none)"])

    section("CHANGED CONSTRUCTS", ["  %-29s %-8s %s :: %s" % (c["family"], c["change"],
                                                             c["file"], c["name"])
                                   for c in r["changed_constructs"]])
    section("MATCHED FAILURE PATTERNS", ["  %s  via %s" % (m["id"], ", ".join(m["via"]))
                                         for m in r["matched_patterns"]])
    section("INVARIANTS", ["  %s: %s" % (m["id"], m["invariant"])
                           for m in r["matched_patterns"]])
    section("CANONICAL TESTS TO PROBE",
            ["  %s  %s%s" % (m["id"], t["test"],
                             "" if t["present_at_head"] else "  [ABSENT AT HEAD]")
             for m in r["matched_patterns"] for t in m["tests"]])
    section("NEW PATTERNS AT HEAD (not used for matching)",
            ["  %s: %s  [%s]  %s" % (p["id"], p["invariant"], ", ".join(p["constructs"]),
                                     ", ".join(p["tests"]))
             for p in r["new_patterns_at_head"]])
    section("BASE PATTERNS REMOVED OR CHANGED AT HEAD",
            ["  %s: %s" % (c["id"], c["change"]) for c in r["base_patterns_changed_at_head"]])
    problems = [("  %s: %s" % (side.upper(), p)) for side, ps in
                sorted(r["marker_problems"].items()) for p in ps]
    section("MARKER PROBLEMS", problems)
    section("UNKNOWN / UNMATCHED MATERIAL CONSTRUCTS",
            ["  unknown: %s" % u for u in r["unknown"]]
            + ["  unmatched family (no pattern owns it): %s" % f
               for f in r["unmatched_construct_families"]])
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--patterns-from", default=None,
                    help="read patterns at this revision instead of BASE "
                         "(replay / what-if only; the report says so)")
    a = ap.parse_args(argv)
    try:
        report = build_report(a.repo, a.base, a.head, a.patterns_from)
    except AnalysisUnavailable as exc:
        sys.stderr.write("CREATOR PROBE LISTER: UNAVAILABLE — %s\n" % str(exc)[:300])
        return 2
    sys.stdout.write(json.dumps(report, indent=2, sort_keys=True) + "\n" if a.json
                     else render_text(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
