"""C1-Lite — scripts/creator_probe_lister.py (advisory developer tooling).

Self-adversarial tests over THROWAWAY git repositories (tmp_path) plus one
hygiene guard over this repository's own failure_pattern markers. Proves:
marker validation (duplicates, malformed, missing invariant, unsupported
placement, stale owners), BASE-owned matching (HEAD-only markers are NEW and
never used; BASE markers removed / changed at HEAD are surfaced), structural
construct detection (known positives, unrelated-change negatives, AST failure
as UNKNOWN), unavailable revisions, deterministic output and zero mutation of
the working tree, index or refs. The tool has no authority; nothing here
selects, skips or gates a test.
"""
import ast
import glob
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts import creator_probe_lister as cpl  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")

STORE = '''import hmac

_BIND_DOMAIN = "x-binding-v1"


def append_rows(conn, rows):
    with _write(conn):
        conn.execute("INSERT INTO t VALUES (?)", rows)


def confirm(store):
    return store.committed_state_readable()


def unrelated(a, b):
    return a + b
'''

MARKERS = '''import pytest


@pytest.mark.failure_pattern(
    "FP-04", invariant="uncertain writes need committed confirmation",
    constructs=("persistence-writer", "committed-confirmation"))
def test_uncertain():
    pass


@pytest.mark.failure_pattern(
    "FP-07", invariant="duplicate positions fail closed",
    constructs=("parsed-identity-accumulation",))
def test_duplicates():
    pass
'''


def _git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True,
                          text=True).stdout.strip()


def _repo(tmp_path, files):
    repo = str(tmp_path / "r")
    os.makedirs(repo)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.invalid")
    _git(repo, "config", "user.name", "t")
    return _commit(repo, files)


def _commit(repo, files):
    for path, text in files.items():
        full = os.path.join(repo, path)
        if text is None:
            os.remove(full)
            continue
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c", "--allow-empty")
    return repo, _git(repo, "rev-parse", "HEAD")


def _pair(tmp_path, head_files, base_files=None):
    repo, base = _repo(tmp_path, base_files or {"engine/store.py": STORE,
                                                 "tests/test_store.py": MARKERS})
    _, head = _commit(repo, head_files)
    return repo, base, head, cpl.build_report(repo, base, head)


def _ids(report):
    return [m["id"] for m in report["matched_patterns"]]


# ---------------------------------------------------------------------------
# construct detection: known positives and false-positive probes
# ---------------------------------------------------------------------------

def test_known_positive_writer_change_surfaces_its_canonical_test(tmp_path):
    _, _, _, r = _pair(tmp_path, {"engine/store.py": STORE.replace(
        'conn.execute("INSERT INTO t VALUES (?)", rows)',
        'conn.execute("INSERT INTO t VALUES (?)", rows[1:])')})
    assert [(c["family"], c["name"], c["change"]) for c in r["changed_constructs"]] \
        == [("persistence-writer", "append_rows", "changed")]
    assert _ids(r) == ["FP-04"]
    assert r["matched_patterns"][0]["via"] == ["persistence-writer"]
    assert r["matched_patterns"][0]["tests"] == [
        {"test": "tests/test_store.py::test_uncertain", "present_at_head": True}]
    assert r["unmatched_construct_families"] == [] and r["unknown"] == []


def test_false_positive_probe_unrelated_change_matches_nothing(tmp_path):
    _, _, _, r = _pair(tmp_path, {"engine/store.py": STORE.replace(
        "return a + b", "return b + a") + "\n\ndef helper(x):\n    return [x]\n"})
    assert r["changed_constructs"] == [] and r["matched_patterns"] == []
    # a web.app change with NO risky construct is not "every pattern"
    _, _, _, r = _pair(tmp_path / "b", {"web/app.py": "def page():\n    return 'hi'\n"})
    assert r["changed_constructs"] == [] and r["matched_patterns"] == []


def test_formatting_and_comments_alone_are_not_a_construct_change(tmp_path):
    _, _, _, r = _pair(tmp_path, {"engine/store.py": STORE.replace(
        "def confirm(store):\n", "def confirm(store):  # reformatted\n\n")})
    assert r["changed_constructs"] == []


@pytest.mark.parametrize("snippet,family", [
    ("@app.route('/x', methods=['POST'])\ndef x():\n    return 1\n", "flask-route"),
    ("def sig(k, m):\n    return hmac.new(k, m, 'sha256').hexdigest()\n", "hmac-signature"),
    ("def key(s):\n    return _canonical_message('dom-v1', s)\n", "signing-domain"),
    ("_NEW_DOMAIN = 'dom-v2'\n", "signing-domain"),
    ("def r(c):\n    c.execute('ROLLBACK')\n", "commit-recovery"),
    ("def pos(rows):\n    d = {}\n    for k, v in rows:\n        d[(int(k), 1)] = v\n"
     "    return d\n", "parsed-identity-accumulation"),
    ("def _canonical_position(s):\n    return s\n", "canonical-identifier-parsing"),
    ("def walk(rs):\n    for r in rs:\n        if r.superseded_by:\n            pass\n",
     "supersession-traversal"),
    ("def item_from_dict(d):\n    return d\n", "load-validation-boundary"),
])
def test_each_construct_family_has_a_known_positive(tmp_path, snippet, family):
    _, _, _, r = _pair(tmp_path, {"engine/new.py": "import hmac\n" + snippet})
    assert family in {c["family"] for c in r["changed_constructs"]}, r["changed_constructs"]


def test_the_original_cap08_collapse_shape_is_detected(tmp_path):
    shape = ("def classify(rows):\n    stored = {}\n    for key, payload in rows:\n"
             "        index, _, size = key.partition(':')\n"
             "        stored[(int(index), int(size))] = payload\n    return stored\n")
    _, _, _, r = _pair(tmp_path, {"engine/store.py": STORE + "\n\n" + shape})
    assert ("parsed-identity-accumulation", "classify", "added") in \
        [(c["family"], c["name"], c["change"]) for c in r["changed_constructs"]]
    assert _ids(r) == ["FP-07"]


def test_unknown_construct_family_is_reported_not_invented(tmp_path):
    _, _, _, r = _pair(tmp_path, {"web/app.py": (
        "@app.route('/p', methods=['POST'])\ndef post():\n    return 1\n")})
    assert r["matched_patterns"] == []
    assert r["unmatched_construct_families"] == ["flask-route"]


def test_unparseable_source_is_unknown_never_a_match(tmp_path):
    _, _, _, r = _pair(tmp_path, {"engine/store.py": STORE + "\ndef broken(:\n"})
    assert r["unknown"] == ["engine/store.py: does not parse at HEAD (AST unavailable)"]
    assert r["changed_constructs"] == [] and r["matched_patterns"] == []


def test_tests_are_not_product_constructs(tmp_path):
    _, _, _, r = _pair(tmp_path, {"tests/test_other.py":
                                  "def test_x():\n    hmac.new(b'k', b'm', 'sha256')\n"})
    assert r["changed_constructs"] == []


# ---------------------------------------------------------------------------
# markers: validation, BASE ownership, NEW and changed markers
# ---------------------------------------------------------------------------

def _problems(tmp_path, marker_src):
    _, _, _, r = _pair(tmp_path, {"tests/test_store.py": marker_src},
                       base_files={"engine/store.py": STORE, "tests/test_store.py": marker_src})
    return r["marker_problems"]["base"], r


def test_conflicting_duplicate_pattern_id_is_a_problem_and_never_used(tmp_path):
    src = MARKERS.replace('"FP-07", invariant="duplicate positions fail closed"',
                          '"FP-04", invariant="something else"')
    problems, r = _problems(tmp_path, src)
    assert any("FP-04: conflicting duplicate pattern ID" in p for p in problems)
    assert "FP-04" not in {m["id"] for m in r["matched_patterns"]}


def test_identical_duplicate_id_means_two_canonical_owners(tmp_path):
    second = MARKERS.split("\n\n\n")[1].replace("test_uncertain", "test_uncertain_two")
    src = MARKERS + "\n\n" + second
    repo, base = _repo(tmp_path, {"engine/store.py": STORE, "tests/test_store.py": src})
    owned = cpl.read_patterns(cpl.Snapshot(repo, base))
    assert owned["problems"] == []
    assert owned["patterns"]["FP-04"]["tests"] == [
        "tests/test_store.py::test_uncertain", "tests/test_store.py::test_uncertain_two"]


@pytest.mark.parametrize("marker,fragment", [
    ('"FP-4", invariant="x", constructs=("flask-route",)', "not of the form FP-NN"),
    ('"FP-40", constructs=("flask-route",)', "invariant= must be a non-empty"),
    ('"FP-40", invariant="  ", constructs=("flask-route",)', "invariant= must be a non-empty"),
    ('"FP-40", invariant=INV, constructs=("flask-route",)', "invariant= must be a non-empty"),
    ('"FP-40", invariant="x", constructs=()', "constructs= must be a non-empty"),
    ('"FP-40", invariant="x", constructs=("rocket",)', "unknown construct families"),
    ('"FP-40", invariant="x", constructs=("flask-route", "flask-route")', "repeats a family"),
    ('"FP-40", invariant="x", constructs=("flask-route",), owner="me"', "only invariant="),
    ('ID, invariant="x", constructs=("flask-route",)', "exactly one literal positional"),
])
def test_malformed_markers_are_problems_never_patterns(tmp_path, marker, fragment):
    src = ("import pytest\n\n\n@pytest.mark.failure_pattern(%s)\ndef test_m():\n"
           "    pass\n" % marker)
    problems, r = _problems(tmp_path, src)
    assert any(fragment in p for p in problems), problems
    assert r["matched_patterns"] == []


@pytest.mark.parametrize("path,src", [
    ("tests/test_store.py", "import pytest\n\n\n@pytest.mark.failure_pattern('FP-41', "
     "invariant='x', constructs=('flask-route',))\ndef helper():\n    pass\n"),
    ("tests/helpers.py", "import pytest\n\n\n@pytest.mark.failure_pattern('FP-41', "
     "invariant='x', constructs=('flask-route',))\ndef test_h():\n    pass\n"),
    ("tests/test_store.py", "import pytest\n\npytestmark = pytest.mark.failure_pattern("
     "'FP-41', invariant='x', constructs=('flask-route',))\n"),
    ("tests/test_store.py", "import pytest\n\n\ndef test_outer():\n"
     "    @pytest.mark.failure_pattern('FP-41', invariant='x', constructs=('flask-route',))\n"
     "    def test_inner():\n        pass\n"),
])
def test_nonexistent_or_uncollectable_owner_is_a_problem(tmp_path, path, src):
    repo, base = _repo(tmp_path, {path: src})
    owned = cpl.read_patterns(cpl.Snapshot(repo, base))
    assert owned["patterns"] == {} and owned["problems"], owned


def test_head_only_marker_is_new_and_never_used_for_matching(tmp_path):
    new = MARKERS + ('\n\n@pytest.mark.failure_pattern("FP-09", invariant="y",'
                     ' constructs=("load-validation-boundary",))\ndef test_new():\n'
                     '    pass\n')
    _, _, _, r = _pair(tmp_path, {"tests/test_store.py": new,
                                  "engine/store.py": STORE + "\n\ndef load_x(d):\n"
                                                             "    return d\n"})
    assert [p["id"] for p in r["new_patterns_at_head"]] == ["FP-09"]
    assert "FP-09" not in _ids(r)
    assert r["unmatched_construct_families"] == ["load-validation-boundary"]


def test_base_marker_removed_at_head_is_surfaced_and_still_owns_matching(tmp_path):
    stripped = MARKERS.replace(
        '@pytest.mark.failure_pattern(\n    "FP-04", invariant="uncertain writes need '
        'committed confirmation",\n    constructs=("persistence-writer", '
        '"committed-confirmation"))\n', "")
    assert stripped != MARKERS
    _, _, _, r = _pair(tmp_path, {"tests/test_store.py": stripped,
                                  "engine/store.py": STORE.replace("(?)\", rows)", "(?)\", rows[1:])")})
    assert {"id": "FP-04", "change": "removed at HEAD"} in r["base_patterns_changed_at_head"]
    assert _ids(r) == ["FP-04"]                         # BASE obligation still surfaced


def test_base_marker_changed_at_head_is_surfaced(tmp_path):
    _, _, _, r = _pair(tmp_path, {"tests/test_store.py": MARKERS.replace(
        "uncertain writes need committed confirmation", "weaker wording")})
    assert r["base_patterns_changed_at_head"] == [
        {"id": "FP-04", "change": "changed at HEAD: invariant"}]


def test_canonical_test_deleted_at_head_is_marked_absent(tmp_path):
    only_dup = "import pytest\n\n\n" + MARKERS.split("\n\n\n")[2]
    _, _, _, r = _pair(tmp_path, {"tests/test_store.py": only_dup,
                                  "engine/store.py": STORE.replace("(?)\", rows)", "(?)\", rows[1:])")})
    fp04 = [m for m in r["matched_patterns"] if m["id"] == "FP-04"][0]
    assert fp04["tests"] == [{"test": "tests/test_store.py::test_uncertain",
                              "present_at_head": False}]
    assert "[ABSENT AT HEAD]" in cpl.render_text(r)


def test_patterns_from_another_revision_is_labelled_not_base(tmp_path):
    repo, base, head, _ = _pair(tmp_path, {"engine/store.py": STORE + "\n"})
    r = cpl.build_report(repo, base, head, patterns_rev=head)
    assert r["patterns_from_base"] is False
    assert "(NOT BASE — replay / what-if use only)" in cpl.render_text(r)


# ---------------------------------------------------------------------------
# availability, determinism, no mutation, no authority wording
# ---------------------------------------------------------------------------

def test_unavailable_base_exits_2_without_a_report(tmp_path, capsys):
    repo, base = _repo(tmp_path, {"engine/store.py": STORE})
    assert cpl.main(["--repo", repo, "--base", "0" * 40, "--head", base]) == 2
    out, err = capsys.readouterr()
    assert out == "" and err.startswith("CREATOR PROBE LISTER: UNAVAILABLE")
    assert cpl.main(["--repo", str(tmp_path / "nope"), "--base", "x", "--head", "y"]) == 2


def test_output_is_deterministic_and_read_only(tmp_path, capsys):
    repo, base, head, _ = _pair(tmp_path, {"engine/store.py": STORE.replace(
        "(?)\", rows)", "(?)\", rows[1:])")})
    with open(os.path.join(repo, "scratch.txt"), "w") as fh:     # untracked, dirty tree
        fh.write("x")
    before = (_git(repo, "status", "--porcelain"), _git(repo, "rev-parse", "HEAD"),
              _git(repo, "for-each-ref"),
              sorted((p, os.path.getmtime(p)) for p in glob.glob(repo + "/**", recursive=True)))
    outs = []
    for args in (["--json"], [], ["--json"], []):
        assert cpl.main(["--repo", repo, "--base", base, "--head", head, *args]) == 0
        outs.append(capsys.readouterr().out)
    assert outs[0] == outs[2] and outs[1] == outs[3]
    json.loads(outs[0])
    after = (_git(repo, "status", "--porcelain"), _git(repo, "rev-parse", "HEAD"),
             _git(repo, "for-each-ref"),
             sorted((p, os.path.getmtime(p)) for p in glob.glob(repo + "/**", recursive=True)))
    assert before == after


def test_report_makes_no_verdict_or_routing_claim(tmp_path):
    _, _, _, r = _pair(tmp_path, {"engine/store.py": STORE.replace("(?)\", rows)", "(?)\", rows[1:])")})
    header, _, body = cpl.render_text(r).upper().partition("\n")
    assert "NO CI, MERGE, RUNTIME, REVIEW-ROUTING OR TEST-SCOPE AUTHORITY" in header
    for claim in ("READY", "RISK", "REVIEWER", "MERGE", "SKIP", "APPROVE", "SAFE"):
        assert claim not in body, claim
    assert set(r) >= {"authority", "changed_constructs", "matched_patterns",
                      "new_patterns_at_head", "base_patterns_changed_at_head", "unknown"}


# ---------------------------------------------------------------------------
# hygiene of THIS repository's markers (working tree)
# ---------------------------------------------------------------------------

class _WorkingTree:
    def __init__(self):
        self.text = {}
        for path in glob.glob(os.path.join(ROOT, "tests", "**", "*.py"), recursive=True):
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            with open(path, encoding="utf-8") as fh:
                self.text[rel] = fh.read()


def test_repository_markers_are_well_formed_and_owned_by_real_tests():
    tree = _WorkingTree()
    owned = cpl.read_patterns(tree)
    assert owned["problems"] == [], owned["problems"]
    assert len(owned["patterns"]) >= 8
    functions = cpl._test_functions(tree)
    for pattern in owned["patterns"].values():
        assert set(pattern["constructs"]) <= set(cpl.FAMILIES)
        for test in pattern["tests"]:
            assert test in functions, test
    # the tool, the marker and this guard stay registered and read-only
    with open(os.path.join(ROOT, "pytest.ini")) as fh:
        assert "failure_pattern(id, invariant, constructs):" in fh.read()
    src = open(os.path.join(ROOT, "scripts", "creator_probe_lister.py")).read()
    tree_ast = ast.parse(src)
    written = [n for n in ast.walk(tree_ast) if isinstance(n, ast.Call)
               and cpl._dotted(n.func).split(".")[-1] in ("remove", "unlink", "rmtree",
                                                           "write_text", "makedirs")]
    assert written == []
    assert '"w"' not in src and "'w'" not in src
