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
    """The operative patterns, in file order.

    A UTF-8 BOM is deliberately NOT stripped here. Python's `str.strip()` does
    not remove `\ufeff` (it is not whitespace), so a BOM used to survive into a
    pattern and translate to a regex that could never match a walked path —
    making `<BOM>docs/` read as safe when Docker, which strips a leading BOM,
    would treat it as `docs/`. Carrying the BOM through to the grammar layer
    means such a file is REJECTED rather than silently accepted or silently
    repaired.
    """
    return [ln.strip() for ln in _read(DOCKERIGNORE).splitlines()
            if ln.strip() and not ln.strip().startswith("#")]


# Metacharacters this translator does NOT model. Go's `filepath.Match`, which
# Docker uses, gives `[`/`]` character-class meaning and `\\` escape meaning, so
# `d[o]cs` matches `docs`. Modelling them correctly is more surface than this
# guard needs; encountering one therefore FAILS CLOSED instead (see below).
# --- restricted `.dockerignore` grammar (the guard's safety contract) --------
# Emulating Docker's full pattern language turned out to be the recurring source
# of false negatives: each partial model let a different dangerous spelling read
# as safe (`./docs/`, `d[o]cs/`, a UTF-8 BOM, `!docs/**content_config`). This
# guard therefore stops emulating. It enforces a deliberately RESTRICTED grammar
# — only forms it can model EXACTLY are permitted — and any other form is
# REJECTED before inclusion/exclusion is evaluated at all. An unsupported pattern
# never becomes "matches everything" or "matches nothing"; it fails the suite.

class DockerignoreGrammarError(AssertionError):
    """Raised when a pattern falls outside the restricted grammar.

    An AssertionError subclass so a rejection surfaces as a test failure with the
    offending pattern and reason, rather than being absorbed into a verdict.
    """


# Every character a permitted pattern may contain. A positive whitelist, so a
# form nobody anticipated — a BOM, a control character, a shell metacharacter,
# whitespace inside a pattern — is rejected by construction rather than by a
# blacklist someone has to remember to extend.
_ALLOWED_PATTERN_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-./*?")

_BOM = "﻿"


def _grammar_violation(pattern):
    """Return the reason `pattern` is outside the restricted grammar, else None.

    Each rejection names the Docker behaviour this guard declines to model:

    * a UTF-8 BOM — Docker strips a leading BOM, so `<BOM>docs/` IS `docs/` to
      Docker while a naive model sees a different string entirely;
    * `!` negation — Docker's re-inclusion interacts with globstars in ways this
      guard will not model, and InventorAI's packaging needs no negation;
    * `[` `]` character classes and `{` `}` braces — matched by Go's
      `filepath.Match`, so `d[o]cs` matches `docs`;
    * `\\` escapes — pattern syntax, not a literal;
    * `..` — path traversal that `filepath.Clean` resolves;
    * any `**` that is not a complete LEADING segment — Docker's treatment of a
      mid-pattern `**` differs from the obvious reading, which is exactly how
      `!docs/**content_config` slipped through.
    """
    if _BOM in pattern:
        return "contains a UTF-8 BOM"
    if pattern.startswith("!"):
        return "negation (`!`) is prohibited by this guard's safety contract"
    for char in pattern:
        if char not in _ALLOWED_PATTERN_CHARS:
            return "contains the unmodelled character %r" % char
    segments = pattern.split("/")
    if any(segment == ".." for segment in segments):
        return "contains a `..` parent-traversal segment"
    globstars = [index for index, segment in enumerate(segments)
                 if "**" in segment]
    for index in globstars:
        # The ONLY permitted globstar: a whole leading segment, `**/...`.
        if index != 0 or segments[index] != "**" or len(segments) < 2:
            return ("`**` is permitted only as a complete leading segment "
                    "(`**/...`); got %r" % pattern)
    if not [seg for seg in segments if seg not in ("", ".")]:
        return "cleans to an empty pattern"
    return None


def assert_safe_dockerignore_grammar(patterns):
    """Reject every pattern outside the restricted grammar, with its reason.

    Called BEFORE any effective-context evaluation, so unsupported syntax can
    never participate in an inclusion/exclusion verdict.
    """
    violations = [(pattern, _grammar_violation(pattern)) for pattern in patterns]
    violations = [item for item in violations if item[1] is not None]
    if violations:
        raise DockerignoreGrammarError(
            "`.dockerignore` pattern(s) outside the restricted grammar: "
            + "; ".join("%r -> %s" % item for item in violations))


def _normalize_pattern(pattern):
    """Apply the part of Go `filepath.Clean` that changes whether a pattern
    matches: drop `.` segments and collapse duplicate separators.

    Docker cleans every pattern before matching, so `./docs/`, `docs//` and
    `docs` are the SAME pattern to it. Without this, `./docs/` translated to a
    regex that could never match a walked path and the guard called a genuinely
    dangerous pattern safe. A leading `/` normalizes away too, which is the
    conservative direction: it can raise a false alarm, never grant a false pass.
    """
    return "/".join(seg for seg in pattern.split("/") if seg not in ("", "."))


def _pattern_to_regex(pattern):
    """Translate one GRAMMAR-VALID pattern to a regex over a relative path.

    Docker matches against the WHOLE cleaned relative path and `*` does not cross
    `/`; the one permitted `**/` prefix matches zero or more leading segments.
    Raises `DockerignoreGrammarError` for anything the grammar forbids, so a
    caller cannot obtain a verdict for an unmodelled form.
    """
    reason = _grammar_violation(pattern)
    if reason is not None:
        raise DockerignoreGrammarError("%r -> %s" % (pattern, reason))
    pattern = _normalize_pattern(pattern)
    out, i = [], 0
    while i < len(pattern):
        char = pattern[i]
        if char == "*":
            if pattern[i:i + 3] == "**/":        # the one permitted globstar
                out.append("(?:.*/)?")
                i += 3
                continue
            out.append("[^/]*")
        elif char == "?":
            out.append("[^/]")
        elif char == ".":
            out.append(r"\.")
        else:
            out.append(char)
        i += 1
    return re.compile("^" + "".join(out) + "$")


def _excluded_from_build_context(rel_path, patterns=None):
    """Whether Docker would drop `rel_path` from the build context.

    The restricted grammar is enforced FIRST: an unsupported pattern raises
    before any matching happens, so it cannot be silently folded into a verdict.
    For permitted patterns, Docker's documented rules apply — every pattern is
    tested against the path AND each of its ancestor directories (an excluded
    directory takes its contents with it), and the last match decides. With
    negation prohibited, "last match wins" reduces to "any match excludes", but
    the loop is kept faithful to Docker's rule rather than shortcut.

    `patterns` lets a control pass a hypothetical `.dockerignore` without
    mutating module or repository state; it defaults to the real file.
    """
    if patterns is None:
        patterns = _dockerignore_patterns()
    assert_safe_dockerignore_grammar(patterns)
    candidates = [rel_path]
    parts = rel_path.split("/")
    for index in range(1, len(parts)):
        candidates.append("/".join(parts[:index]))
    excluded = False
    for pattern in patterns:
        regex = _pattern_to_regex(pattern)
        if any(regex.match(candidate) for candidate in candidates):
            excluded = True
    return excluded


def test_live_dockerignore_satisfies_the_restricted_grammar():
    """The live file must contain only forms this guard models exactly.

    This is the contract that removes the whole false-negative family: rather
    than the guard trying to keep up with Docker's pattern language, the file is
    held to the subset the guard can model. A future pattern outside it fails
    HERE, with its reason, instead of quietly weakening the context proof."""
    patterns = _dockerignore_patterns()
    assert patterns, "the live .dockerignore has no operative patterns"
    offenders = [(pat, _grammar_violation(pat)) for pat in patterns
                 if _grammar_violation(pat) is not None]
    assert not offenders, offenders
    assert_safe_dockerignore_grammar(patterns)          # raises with the reason


def test_every_live_pattern_translates_exactly():
    """Each permitted pattern yields a compiled regex — no silent None path."""
    for pattern in _dockerignore_patterns():
        assert _pattern_to_regex(pattern) is not None, pattern


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


# Every spelling of "exclude the docs tree" that Docker honours, plus the forms
# the restricted grammar refuses outright. Each must be CONTAINED — either
# rejected before evaluation, or evaluated and caught. Never "safe".
#
# `(form, must_be_rejected)`: True where the grammar refuses the form, False
# where the grammar permits it and the matcher must then catch it.
DANGEROUS_DOCS_EXCLUSION_FORMS = (
    ("docs", False),
    ("docs/", False),
    ("./docs", False),
    ("./docs/", False),
    ("docs//", False),
    ("doc?/", False),
    ("do*/", False),
    ("**/path_n_content_config", False),
    ("docs/governance/path_n_content_config", False),
    ("﻿docs/", True),                       # UTF-8 BOM
    ("d[o]cs/", True),                            # character class
    ("docs/[a-z]*", True),                        # character class
    ("{docs,web}", True),                         # brace form
    ("../docs", True),                            # parent traversal
    ("doc\\s", True),                             # backslash pattern syntax
    ("!docs/**content_config", True),             # negation
    ("docs/**content_config", True),              # unrecognised globstar placement
    ("docs/**/../x", True),                       # globstar + traversal
)


def _containment_of(form):
    """How the guard contains `form`: 'rejected' or 'caught'.

    Raises if the form would reach a "safe" verdict — the outcome this whole
    repair exists to make impossible.
    """
    hypothetical = _dockerignore_patterns() + [form]
    try:
        verdicts = [_excluded_from_build_context(rel, patterns=hypothetical)
                    for rel in RUNTIME_REQUIRED_CONTEXT_FILES]
    except DockerignoreGrammarError:
        return "rejected"
    assert all(verdicts), (
        "form %r reached a SAFE verdict: the artifacts would silently "
        "disappear from the image" % (form,))
    return "caught"


@pytest.mark.parametrize("form,must_be_rejected", DANGEROUS_DOCS_EXCLUSION_FORMS)
def test_every_dangerous_form_is_contained(form, must_be_rejected):
    containment = _containment_of(form)
    assert containment == ("rejected" if must_be_rejected else "caught"), (
        form, containment)


def test_astra_combined_negation_case_fails_before_context_evaluation():
    """The exact reported combination. `docs/governance/*` alone would exclude
    the artifacts; the `!docs/**content_config` re-include is what a partial
    model read as making them safe again. Negation is now rejected BEFORE any
    matching, so the combination cannot reach a packaged-layout verdict at all."""
    combined = ["docs/governance/*", "!docs/**content_config"]
    with pytest.raises(DockerignoreGrammarError) as excinfo:
        _excluded_from_build_context(RUNTIME_REQUIRED_CONTEXT_FILES[0],
                                     patterns=_dockerignore_patterns() + combined)
    message = str(excinfo.value)
    assert "negation" in message, message
    assert "docs/**content_config" in message, message


def test_rejection_happens_before_any_matching():
    """Order matters: a prohibited pattern must abort evaluation even when the
    path could not possibly match it, so no verdict is ever computed from a
    pattern set containing unmodelled syntax."""
    for form in ("!anything", "﻿nothing-to-do-with-docs", "a[b]c"):
        with pytest.raises(DockerignoreGrammarError):
            _excluded_from_build_context("web/app.py",
                                         patterns=_dockerignore_patterns() + [form])


def test_bom_can_never_be_read_as_safe():
    """Explicit control for the reported `\\ufeffdocs/`."""
    assert _grammar_violation("﻿docs/") == "contains a UTF-8 BOM"
    with pytest.raises(DockerignoreGrammarError):
        _pattern_to_regex("﻿docs/")
    assert _containment_of("﻿docs/") == "rejected"


@pytest.mark.parametrize("form,expected_reason_fragment", [
    ("!docs", "negation"),
    ("d[o]cs", "unmodelled character"),
    ("{a,b}", "unmodelled character"),
    ("a\\b", "unmodelled character"),
    ("../x", "parent-traversal"),
    ("docs/**x", "complete leading segment"),
    ("a/**/b", "complete leading segment"),
    ("﻿x", "BOM"),
    ("./", "empty pattern"),
])
def test_grammar_rejection_reasons_are_specific(form, expected_reason_fragment):
    """Each rejection must say WHY, so a future contributor can fix the pattern
    rather than guess at the guard."""
    reason = _grammar_violation(form)
    assert reason is not None, form
    assert expected_reason_fragment in reason, (form, reason)


def test_permitted_globstar_forms_are_exactly_those_the_live_file_needs():
    """`**` is whitelisted only as a complete leading segment — the shape every
    live pattern uses. Any other placement is rejected."""
    for permitted in ("**/*.pyc", "**/__pycache__/", "**/*.sqlite", "**/.env",
                      "**/*.bak", "**/.pytest_cache/"):
        assert _grammar_violation(permitted) is None, permitted
        assert _pattern_to_regex(permitted) is not None, permitted
    for prohibited in ("docs/**", "docs/**/x", "**docs", "a/**/b", "**x/y"):
        assert _grammar_violation(prohibited) is not None, prohibited


def test_no_docs_exclusion_in_any_spelling_is_present_today():
    """The live file must contain none of those forms, in any spelling."""
    present = _dockerignore_patterns()
    for form, _ in DANGEROUS_DOCS_EXCLUSION_FORMS:
        assert form not in present, form
    normalized = {_normalize_pattern(pat) for pat in present}
    assert "docs" not in normalized
    assert "docs/governance" not in normalized
    assert "docs/governance/path_n_content_config" not in normalized


def test_pattern_normalization_matches_docker_cleaning():
    """`./docs/`, `docs//` and `docs` are ONE pattern to Docker; the matcher must
    agree, because that equivalence is what an earlier false negative hinged on."""
    for form in ("docs", "docs/", "./docs", "./docs/", "docs//", "./docs//"):
        assert _normalize_pattern(form) == "docs", form
    assert _normalize_pattern("**/*.pyc") == "**/*.pyc"
    assert _normalize_pattern("./") == ""


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
