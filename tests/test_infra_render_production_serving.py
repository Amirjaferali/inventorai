"""INFRA-G1-R2 implementation — production serving posture (PSRR item 9).

Gate provenance: INFRA-G1-R1 is the merged, authoritative governance contract
(hosting/region selection recording + the bounded deployment-preparation
contract). INFRA-G1-R2 — this gate — is the bounded IMPLEMENTATION performed
under it.

File: tests/test_infra_render_production_serving.py
Purpose: pin the BOUNDED production-serving contract introduced for Render
deployment preparation — a production WSGI server (Gunicorn) driven by a
provider-neutral `gunicorn.conf.py`, enforcing the governed single-instance /
single-worker / single-thread invariant, binding the platform-provided `PORT`,
and never using Flask's built-in development server in the production path.
Input contract: `gunicorn.conf.py` (repository root); `requirements.txt`;
`.python-version`; `web/app.py` (`app`, `_run_config`).
Output contract: the production start posture is exactly workers=1, threads=1,
preload disabled, reload disabled, bind 0.0.0.0:$PORT; the WSGI target resolves
to the canonical Flask app; the development path is unchanged; no ProxyFix /
HSTS / database / email / monitoring / payment dependency is introduced.
Prohibited: weakening the single-worker/single-thread invariant to pass;
asserting on comments instead of behavior where behavior is testable.
"""
import ast
import importlib
import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF = os.path.join(ROOT, "gunicorn.conf.py")
REQUIREMENTS = os.path.join(ROOT, "requirements.txt")
PYTHON_VERSION_FILE = os.path.join(ROOT, ".python-version")
# SERIOUS-RELEASE-PRE-RELEASE-TRANCHE-01 Slice A: the container image is part of
# the SAME production serving posture this module already owns, so it is pinned
# here rather than in a second test family.
DOCKERFILE = os.path.join(ROOT, "Dockerfile")
DOCKERIGNORE = os.path.join(ROOT, ".dockerignore")

# The AUTHORITATIVE forbidden configuration terms. Membership is unchanged from
# the original guard; it is lifted to module scope only so the operative-string
# check and the docstring check derive from ONE list instead of two copies.
_FORBIDDEN_CONFIG_TERMS = ("secret", "sqlite", "/var/data", "db_path",
                           "password", "token", "api_key")

# The ONLY term the docstring check waives, and only in a docstring: EMAIL-H1
# documents access-log token redaction, so the word must be writable in prose.
# Operative strings waive nothing. Adding any further entry here would weaken
# the guard and requires its own authorization.
_DOCSTRING_ALLOWED_TERMS = ("token",)

# Dependency families that must NOT appear from this gate (scope guard).
_FORBIDDEN_DEPENDENCY_TOKENS = (
    "psycopg", "postgres", "mysql", "sqlalchemy", "alembic", "django",
    "boto3", "sendgrid", "resend", "postmark", "mailgun", "sentry",
    "datadog", "newrelic", "prometheus", "stripe", "paypal", "braintree",
)


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def _requirement_lines():
    return [ln.strip() for ln in _read(REQUIREMENTS).splitlines()
            if ln.strip() and not ln.strip().startswith("#")]


def _load_conf(port_value=None):
    """Import `gunicorn.conf.py` as a module under a controlled environment.

    Behavioural load (not a text scan): the file is executed, so the assertions
    below observe the values the production server would actually receive.
    """
    previous = os.environ.get("PORT")
    if port_value is None:
        os.environ.pop("PORT", None)
    else:
        os.environ["PORT"] = port_value
    try:
        spec = importlib.util.spec_from_file_location(
            "_inventorai_gunicorn_conf_probe", CONF)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        if previous is None:
            os.environ.pop("PORT", None)
        else:
            os.environ["PORT"] = previous
        sys.modules.pop("_inventorai_gunicorn_conf_probe", None)


# --- dependency contract ------------------------------------------------------

def test_gunicorn_is_pinned_exactly_in_requirements():
    pins = [ln for ln in _requirement_lines()
            if ln.lower().startswith("gunicorn")]
    assert len(pins) == 1, pins
    assert re.fullmatch(r"gunicorn==\d+\.\d+(\.\d+)?", pins[0]), pins[0]


def test_no_out_of_scope_dependency_family_added():
    joined = " ".join(_requirement_lines()).lower()
    for token in _FORBIDDEN_DEPENDENCY_TOKENS:
        assert token not in joined, token


def test_python_version_pin_matches_the_tested_runtime_minor():
    assert os.path.isfile(PYTHON_VERSION_FILE)
    pinned = _read(PYTHON_VERSION_FILE).strip()
    assert re.fullmatch(r"3\.\d+(\.\d+)?", pinned), pinned
    running = "%d.%d" % (sys.version_info[0], sys.version_info[1])
    assert pinned.split(".")[0] + "." + pinned.split(".")[1] == running, (
        pinned, running)


# --- WSGI target --------------------------------------------------------------

def test_wsgi_target_resolves_to_the_canonical_flask_app():
    """`web.app:app` — the exact target the production command names."""
    module = importlib.import_module("web.app")
    target = getattr(module, "app")
    assert target.__class__.__name__ == "Flask"
    # WSGI callable contract (what the server will actually invoke).
    assert callable(getattr(target, "wsgi_app"))


# --- single-worker / single-thread invariant (safety-critical) ----------------

def test_production_posture_is_exactly_one_worker():
    assert _load_conf().workers == 1


def test_production_posture_is_exactly_one_thread():
    assert _load_conf().threads == 1


def test_application_is_not_preloaded_so_the_store_opens_in_the_worker():
    """`preload_app` must stay False: the single application-scoped, thread-bound
    SQLite connection must be created inside the worker process, never in the
    master before fork."""
    assert _load_conf().preload_app is False


def test_no_auto_reload_in_production():
    assert getattr(_load_conf(), "reload", False) is False


# --- platform PORT consumption ------------------------------------------------

def test_bind_consumes_the_platform_supplied_port():
    conf = _load_conf(port_value="8123")
    assert conf.bind == "0.0.0.0:8123", conf.bind


def test_bind_tracks_a_different_platform_port_value():
    """Behavioural proof that the port is read, not hard-coded."""
    conf = _load_conf(port_value="9456")
    assert conf.bind == "0.0.0.0:9456", conf.bind


def test_bind_has_a_safe_default_when_port_is_absent():
    conf = _load_conf(port_value=None)
    assert conf.bind.startswith("0.0.0.0:"), conf.bind
    assert conf.bind.split(":")[1].isdigit(), conf.bind


def test_production_bind_never_hard_codes_the_development_port():
    """5000 is the development-only `_run_config` port; production must not
    pin it."""
    assert _load_conf(port_value="8123").bind != "0.0.0.0:5000"


# --- development-server separation -------------------------------------------

def _conf_code_tree():
    """Parse `gunicorn.conf.py` and drop the module docstring, so the assertions
    below inspect EXECUTABLE CODE rather than documentation prose."""
    tree = ast.parse(_read(CONF))
    body = list(tree.body)
    if (body and isinstance(body[0], ast.Expr)
            and isinstance(body[0].value, ast.Constant)
            and isinstance(body[0].value.value, str)):
        body = body[1:]
    return ast.Module(body=body, type_ignores=[])


def _docstring_node_ids(tree):
    """Identities of the FUNCTION and CLASS docstring constants in `tree`.

    The MODULE docstring is not included here because `_conf_code_tree()` has
    already removed it — that exclusion is pre-existing base behaviour and is
    unchanged by this gate. Identity (not value) is used so an operative string
    that merely happens to equal a docstring is still scanned as operative."""
    ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, "body", [])
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                ids.add(id(body[0].value))
    return ids


def _conf_code_strings():
    """Every string constant outside the module docstring — operative strings
    AND function/class docstrings. This is the ORIGINAL scanning scope and is
    deliberately unchanged: the debug/reload guard below keeps applying to
    documentation prose exactly as it always did."""
    return [n.value for n in ast.walk(_conf_code_tree())
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def _conf_operative_strings():
    """String constants that are OPERATIVE CODE — `_conf_code_strings()` minus
    the function/class docstrings. The FULL forbidden-term list applies here,
    with no exception of any kind."""
    tree = _conf_code_tree()
    doc_ids = _docstring_node_ids(tree)
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and id(n) not in doc_ids]


def _conf_docstring_strings():
    """The function/class docstrings of `gunicorn.conf.py`."""
    tree = _conf_code_tree()
    doc_ids = _docstring_node_ids(tree)
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and id(n) in doc_ids]


def _all_conf_strings():
    """EVERY string constant in the file, module docstring included."""
    return [n.value for n in ast.walk(ast.parse(_read(CONF)))
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def _conf_environ_keys():
    """Every environment variable the executable configuration actually reads."""
    keys = []
    for node in ast.walk(_conf_code_tree()):
        if (isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "get"
                and isinstance(node.func.value, ast.Attribute)
                and node.func.value.attr == "environ"):
            if node.args and isinstance(node.args[0], ast.Constant):
                keys.append(node.args[0].value)
    return keys


def test_production_config_does_not_invoke_the_flask_dev_server():
    """AST-level: the production configuration executes no `.run(...)` call and
    references neither the development run-config helper nor werkzeug's
    development server."""
    tree = _conf_code_tree()
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr != "run", ast.dump(node)
    names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    attrs = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    assert "_run_config" not in names | attrs
    imported = {a.name for n in ast.walk(tree)
                if isinstance(n, ast.Import) for a in n.names}
    imported |= {n.module for n in ast.walk(tree)
                 if isinstance(n, ast.ImportFrom) and n.module}
    assert not any(m.startswith("werkzeug") or m.startswith("flask")
                   for m in imported), imported


def test_development_run_config_is_unchanged_and_still_single_threaded():
    """The dev path stays exactly as governed (P4-1b-1 amendment): not threaded,
    port 5000. This gate changes the production path only."""
    module = importlib.import_module("web.app")
    cfg = module._run_config()
    assert cfg["threaded"] is False
    assert cfg["port"] == 5000


# --- security regression guards ----------------------------------------------

def test_no_proxyfix_or_forwarded_header_trust_introduced():
    joined = _read(CONF) + _read(os.path.join(ROOT, "web", "app.py"))
    assert "ProxyFix" not in joined
    assert "X-Forwarded-For" not in joined
    assert "X-Forwarded-Proto" not in joined


def test_no_hsts_header_is_emitted():
    """Behavioural: HSTS remains DEFERRED (RL-C4) — no response carries it."""
    module = importlib.import_module("web.app")
    module.app.config["TESTING"] = True
    client = module.app.test_client()
    for path in ("/", "/health", "/definitely-not-a-route"):
        response = client.get(path)
        assert "Strict-Transport-Security" not in response.headers, path


def test_production_config_reads_only_the_platform_port():
    """AST-level: the executable configuration consults exactly one environment
    variable — PORT. No secret and no database path is read or embedded.

    The forbidden-term list is unchanged from the original guard and applies to
    operative strings with NO exception."""
    assert _conf_environ_keys() == ["PORT"], _conf_environ_keys()
    for value in _conf_operative_strings():
        lowered = value.lower()
        for forbidden in _FORBIDDEN_CONFIG_TERMS:
            assert forbidden not in lowered, value


def test_production_config_docstrings_carry_no_forbidden_term_except_token():
    """Documentation is NOT exempt from the forbidden-term guard.

    The SAME authoritative `_FORBIDDEN_CONFIG_TERMS` list is applied to every
    function/class docstring, minus exactly one narrowly justified word:
    ``token``. EMAIL-H1 legitimately DOCUMENTS access-log token redaction, so
    the concept must be nameable in prose; every other governed term — secret,
    sqlite, /var/data, db_path, password, api_key — stays rejected in
    docstrings exactly as before. This is a narrow exception, not a blanket
    docstring exemption."""
    for value in _conf_docstring_strings():
        lowered = value.lower()
        for forbidden in _FORBIDDEN_CONFIG_TERMS:
            if forbidden in _DOCSTRING_ALLOWED_TERMS:
                continue
            assert forbidden not in lowered, value


def test_production_config_embeds_no_credential_shaped_literal_anywhere():
    """ADDITIVE coverage on top of the two term checks above: scans EVERY string
    in the file — the module docstring included, which the term checks do not
    reach — for a literal that could be a real secret (long hex or base64-ish
    runs). Documentation may name a concept; it may never carry a value."""
    for value in _all_conf_strings():
        assert not re.search(r"[A-Fa-f0-9]{32,}", value), value
        assert not re.search(r"[A-Za-z0-9+/]{40,}={0,2}", value), value


def test_production_config_does_not_enable_debug_or_reload():
    conf = _load_conf()
    assert getattr(conf, "reload", False) is False
    assert getattr(conf, "spew", False) is False
    for value in _conf_code_strings():
        assert "debug" not in value.lower(), value


# --- SERIOUS-RELEASE-PRE-RELEASE-TRANCHE-01 Slice A: container image ----------
# The Owner-fixed production topology is a Docker runtime on a managed container
# platform, one instance, with the canonical SQLite database on an attached
# persistent disk (OD-INFRA-1 / OD-INFRA-2). These assertions pin the image's
# governed properties. They are deliberately STATIC: the repository CI does not
# build container images, so an assertion that required a running Docker daemon
# would be a skip in every environment, which is not evidence.


def _dockerfile_lines():
    """Operative Dockerfile lines — comments and blank lines removed."""
    return [ln.strip() for ln in _read(DOCKERFILE).splitlines()
            if ln.strip() and not ln.strip().startswith("#")]


def _dockerfile_operative_text():
    return "\n".join(_dockerfile_lines())


def test_dockerfile_exists_and_declares_one_base_image():
    assert os.path.isfile(DOCKERFILE)
    froms = [ln for ln in _dockerfile_lines() if ln.upper().startswith("FROM ")]
    assert len(froms) == 1, froms


def test_dockerfile_python_tracks_the_repository_pin():
    """The base image must carry the interpreter `.python-version` pins, so the
    built image and the tested runtime can never drift apart silently."""
    pinned = _read(PYTHON_VERSION_FILE).strip()
    major_minor = ".".join(pinned.split(".")[:2])
    base = next(ln for ln in _dockerfile_lines() if ln.upper().startswith("FROM "))
    assert ("python:" + major_minor) in base, (base, pinned)


def test_dockerfile_installs_the_pinned_python_dependencies():
    text = _dockerfile_operative_text()
    assert "requirements.txt" in text
    assert re.search(r"pip install[^\n]*-r requirements\.txt", text), text


def test_dockerfile_installs_the_weasyprint_os_stack_and_an_arabic_font():
    """Direct Output PDF must remain supported (Owner decision). These are the
    OS packages `requirements.txt` records as "OS packages, not pip packages",
    plus the ONE font family `web/templates/pdf_base.html` selects for both the
    Latin and the Arabic deliverable."""
    text = _dockerfile_operative_text()
    for package in ("libpango-1.0-0", "libpangoft2-1.0-0", "libharfbuzz0b",
                    "libfontconfig1", "fonts-dejavu-core"):
        assert package in text, package


def test_dockerfile_font_family_matches_the_pdf_template():
    """The installed font package must actually provide the family the PDF
    template asks for; otherwise Arabic would silently render as tofu."""
    template = _read(os.path.join(ROOT, "web", "templates", "pdf_base.html"))
    assert "DejaVu Sans" in template
    assert "fonts-dejavu-core" in _dockerfile_operative_text()


def test_dockerfile_start_command_is_the_governed_gunicorn_entry_point():
    text = _dockerfile_operative_text()
    assert "gunicorn" in text and "-c" in text
    assert "gunicorn.conf.py" in text
    assert "web.app:app" in text


def test_dockerfile_does_not_invoke_the_flask_development_server():
    text = _dockerfile_operative_text().lower()
    for forbidden in ("flask run", "app.run", "python web/app.py",
                      "python -m flask"):
        assert forbidden not in text, forbidden


def test_dockerfile_does_not_restate_or_weaken_the_serving_invariants():
    """Exactly ONE place may set workers/threads/preload: `gunicorn.conf.py`.
    A `--workers`/`--threads`/`--preload` flag in the image would create a second
    source of truth that could silently override the single-writer posture."""
    text = _dockerfile_operative_text().lower()
    for forbidden in ("--workers", "--threads", "--preload", "-w ", "--reload"):
        assert forbidden not in text, forbidden


def test_dockerfile_embeds_no_configuration_or_credential_value():
    """The image carries no environment-specific value: no secret, no database
    path, no mount path. Those come from the platform at run time."""
    text = _dockerfile_operative_text()
    lowered = text.lower()
    for forbidden in _FORBIDDEN_CONFIG_TERMS:
        assert forbidden not in lowered, forbidden
    for name in ("INVENTORAI_SECRET_KEY", "INVENTORAI_DB_PATH", "INVENTORAI_ENV"):
        assert name not in text, name
    assert not re.search(r"[A-Fa-f0-9]{32,}", text), "credential-shaped literal"


def test_dockerfile_declares_no_volume_that_could_host_an_ephemeral_database():
    """A `VOLUME` declaration would invite a container-local database directory
    that looks durable and is not. The durable path is the platform's disk."""
    assert not any(ln.upper().startswith("VOLUME") for ln in _dockerfile_lines())


def test_dockerfile_creates_no_database_in_the_image():
    text = _dockerfile_operative_text().lower()
    for forbidden in ("sqlite3 ", ".sqlite", ".db"):
        assert forbidden not in text, forbidden


def test_dockerfile_adds_no_out_of_scope_dependency_family():
    lowered = _dockerfile_operative_text().lower()
    for token in _FORBIDDEN_DEPENDENCY_TOKENS:
        assert token not in lowered, token


def test_dockerignore_excludes_local_secrets_and_databases():
    """`COPY . .` must not be able to carry a local `.env`, a local database or
    the git directory into an image layer.

    Asserted behaviourally through the build-context matcher below rather than by
    matching literal pattern spellings: the property is what must hold, and the
    spelling legitimately changed in the M1 repair (`.env` -> `**/.env`) so that
    it also covers nested occurrences."""
    assert os.path.isfile(DOCKERIGNORE)
    for rel in (".env", "local.sqlite", ".git/config"):
        assert _excluded_from_build_context(rel), rel


def test_dockerignore_keeps_the_backup_operator_cli_in_the_image():
    """The backup/restore CLI must be runnable inside the running container,
    which is where the persistent disk is mounted."""
    entries = [ln.strip() for ln in _read(DOCKERIGNORE).splitlines()
               if ln.strip() and not ln.strip().startswith("#")]
    assert "scripts/" not in entries and "scripts" not in entries


# --- M1 repair: runtime artifacts must survive the Docker build context -------
# An earlier `.dockerignore` excluded `docs/` wholesale while runtime code reads
# committed JSON from `docs/governance/path_n_content_config/`. The image would
# have started, answered `/health` with 200, and failed the guided journey for
# both activated domains. These assertions observe the EFFECTIVE BUILD CONTEXT,
# not just the repository tree, so re-adding a broad `docs` exclusion fails here.

# The runtime-required artifacts, at the exact repository-relative paths the two
# loaders resolve. Moving a file is as breaking as excluding it, so the paths are
# asserted rather than discovered.
PATH_N_CONFIG_DIR = "docs/governance/path_n_content_config"
RUNTIME_REQUIRED_CONTEXT_FILES = (
    PATH_N_CONFIG_DIR + "/electronics_electrical_path_n_questions.json",
    PATH_N_CONFIG_DIR + "/electronics_electrical_question_intent_registry.json",
    PATH_N_CONFIG_DIR + "/mechanical_path_n_questions.json",
    PATH_N_CONFIG_DIR + "/mechanical_question_intent_registry.json",
)


def _dockerignore_patterns():
    """The operative patterns, in file order (order matters: last match wins)."""
    return [ln.strip() for ln in _read(DOCKERIGNORE).splitlines()
            if ln.strip() and not ln.strip().startswith("#")]


def _pattern_to_regex(pattern):
    """Translate one Docker ignore pattern to a regex over a relative path.

    Docker matches a pattern against the WHOLE relative path and `*` does not
    cross `/`; `**` does. Returns None for any form this translator does not
    model, which callers treat CONSERVATIVELY (as if it matched) so an
    unmodelled pattern can never produce a false "included" verdict.
    """
    pattern = pattern.rstrip("/")
    if not pattern or pattern.startswith("/"):
        return None
    out, i = [], 0
    while i < len(pattern):
        char = pattern[i]
        if char == "*":
            if pattern[i:i + 2] == "**":
                out.append("(?:.*)")
                i += 2
                if pattern[i:i + 1] == "/":      # `**/` may match zero segments
                    out[-1] = "(?:.*/)?"
                    i += 1
                continue
            out.append("[^/]*")
        elif char == "?":
            out.append("[^/]")
        elif char in ".^$+{}[]|()\\":
            out.append(re.escape(char))
        else:
            out.append(char)
        i += 1
    return re.compile("^" + "".join(out) + "$")


def _excluded_from_build_context(rel_path):
    """Whether Docker would drop `rel_path` from the build context.

    Applies Docker's documented rules: every pattern is tested against the path
    AND against each of its ancestor directories (an excluded directory takes its
    contents with it), and the LAST matching pattern decides — a `!` pattern
    re-includes. Deliberately conservative: an unmodelled pattern counts as a
    match, so a "not excluded" result is a sound proof, never an optimistic one.
    """
    candidates = [rel_path]
    parts = rel_path.split("/")
    for index in range(1, len(parts)):
        candidates.append("/".join(parts[:index]))
    excluded = False
    for pattern in _dockerignore_patterns():
        negated = pattern.startswith("!")
        regex = _pattern_to_regex(pattern[1:] if negated else pattern)
        if regex is None:                         # unmodelled → assume it matches
            excluded = not negated
            continue
        if any(regex.match(candidate) for candidate in candidates):
            excluded = not negated
    return excluded


def test_dockerignore_uses_only_modelled_pattern_forms():
    """Guard on the guard: if a future pattern uses a form the matcher above does
    not model, this fails loudly instead of the build-context proof silently
    weakening."""
    for pattern in _dockerignore_patterns():
        body = pattern[1:] if pattern.startswith("!") else pattern
        assert _pattern_to_regex(body) is not None, pattern


def test_runtime_required_artifacts_exist_at_their_declared_paths():
    for rel in RUNTIME_REQUIRED_CONTEXT_FILES:
        assert os.path.isfile(os.path.join(ROOT, rel)), rel


def test_runtime_loaders_still_point_at_those_paths():
    """Paths must stay where the loaders look; a move is as breaking as an
    exclusion, and would otherwise slip past a context-only assertion."""
    assert PATH_N_CONFIG_DIR in _read(os.path.join(ROOT, "engine",
                                                   "intent_serving.py"))
    questions = _read(os.path.join(ROOT, "engine", "path_n_questions.py"))
    for segment in ('"docs"', '"governance"', '"path_n_content_config"'):
        assert segment in questions, segment


def test_runtime_required_artifacts_survive_the_build_context():
    """The M1 assertion: each artifact is present in the EFFECTIVE context."""
    for rel in RUNTIME_REQUIRED_CONTEXT_FILES:
        assert not _excluded_from_build_context(rel), rel


def test_a_broad_docs_exclusion_would_be_caught():
    """Proves the assertion above has teeth: with `docs` excluded, the same
    matcher must report the artifacts as dropped."""
    patterns = _dockerignore_patterns()
    assert "docs" not in patterns and "docs/" not in patterns
    original = _dockerignore_patterns

    def _with_docs_excluded():
        return patterns + ["docs"]

    globals()["_dockerignore_patterns"] = _with_docs_excluded
    try:
        for rel in RUNTIME_REQUIRED_CONTEXT_FILES:
            assert _excluded_from_build_context(rel), rel
    finally:
        globals()["_dockerignore_patterns"] = original


def test_the_application_packages_survive_the_build_context():
    """The rest of what the running service needs, asserted the same way."""
    for rel in ("web/app.py", "web/templates/pdf_base.html", "gunicorn.conf.py",
                "requirements.txt", "engine/path_n_questions.py",
                "engine/intent_serving.py", "domains/electronics_electrical/domain.json",
                "scripts/inventorai_backup.py"):
        assert not _excluded_from_build_context(rel), rel


def test_local_secrets_and_databases_are_dropped_at_any_depth():
    """The §4 nested-pattern correction, asserted behaviourally rather than by
    reading the patterns: a nested `.env`, database or cache must not ship."""
    for rel in (".env", "web/.env", "data/local.sqlite", "a/b/c.db",
                "engine/__pycache__/app.pyc", "tests/__pycache__/x.pyc",
                ".pytest_cache/CACHEDIR.TAG", "engine/x.bak"):
        assert _excluded_from_build_context(rel), rel
