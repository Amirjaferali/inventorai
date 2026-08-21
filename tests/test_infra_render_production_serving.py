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


def _conf_code_strings():
    return [n.value for n in ast.walk(_conf_code_tree())
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
    variable — PORT. No secret and no database path is read or embedded."""
    assert _conf_environ_keys() == ["PORT"], _conf_environ_keys()
    for value in _conf_code_strings():
        lowered = value.lower()
        for forbidden in ("secret", "sqlite", "/var/data", "db_path",
                          "password", "token", "api_key"):
            assert forbidden not in lowered, value


def test_production_config_does_not_enable_debug_or_reload():
    conf = _load_conf()
    assert getattr(conf, "reload", False) is False
    assert getattr(conf, "spew", False) is False
    for value in _conf_code_strings():
        assert "debug" not in value.lower(), value
