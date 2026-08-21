"""Production WSGI serving configuration (INFRA-G1-R2 bounded implementation).

Gate provenance: INFRA-G1-R1 is the merged authoritative governance contract
that defined this bounded scope; INFRA-G1-R2 is this implementation.

File path: ``gunicorn.conf.py`` (repository root)
Purpose: express the GOVERNED production serving posture in one inspectable,
testable, PROVIDER-NEUTRAL artifact. It is a Gunicorn configuration file, not a
hosting-provider artifact: the same file serves the app on any Linux host.
Input contract: the platform-supplied ``PORT`` environment variable (optional;
a safe default applies when absent). Nothing else is read here — the
application's own configuration (``INVENTORAI_ENV`` / ``INVENTORAI_SECRET_KEY``
/ ``INVENTORAI_DB_PATH``) stays entirely in ``web/app.py`` and the platform
environment; no secret and no database path appears in this file.
Output contract: Gunicorn settings pinning ONE worker process and ONE thread,
with preloading and auto-reload disabled.
Prohibited: more than one worker; more than one thread; preloading the
application; auto-reload; embedding secrets or database paths; invoking Flask's
built-in development server.

Why exactly one worker and one thread (safety-critical, governed):
``engine/record_store.py`` is used through ONE application-scoped, thread-bound
SQLite connection, and the development path pins ``threaded=False`` for the same
reason (P4-1b-1 amendment, ``web/app.py _run_config``). A second worker process
would introduce concurrent writers to the single durable SQLite file and a
second thread would violate the connection's thread affinity. This file
preserves that invariant in production instead of relying on defaults —
Gunicorn's own default is a single sync worker, but the value is stated
explicitly so the invariant is visible, reviewable, and test-pinned.

``preload_app`` MUST remain False: with preloading, application import (and any
lazily built store) would happen in the master process before fork. Keeping it
disabled guarantees the store is created inside the single worker that uses it.

Start command (declared here so the runtime posture is reproducible):
    gunicorn -c gunicorn.conf.py web.app:app
"""
import os

# The platform supplies PORT. The default is used only when the variable is
# absent (e.g. a local production-posture check); it is deliberately NOT the
# development server's port, so a misconfigured production start cannot silently
# masquerade as the development path.
_DEFAULT_PORT = "10000"

bind = "0.0.0.0:%s" % os.environ.get("PORT", _DEFAULT_PORT)

# The governed single-instance invariant (see the module docstring).
workers = 1
threads = 1

# Never import the application in the master process (store/connection affinity).
preload_app = False

# No auto-reload in production.
reload = False

# Operational logging goes to the platform's stdout/stderr streams, which the
# existing structured-logging seam (``web/observability.py``) already targets.
accesslog = "-"
errorlog = "-"

# --- EMAIL-H1 / OBS-P5-2-01: access-log token redaction ----------------------
# The emailed verification and reset links carry a RAW single-use token in the
# URL PATH. Gunicorn's access log records the request line, so without this the
# governed production serving stack writes those raw tokens to stdout — an
# exposure this repository controls, independently reproduced before this fix:
#     "GET /reset/<RAW_TOKEN> HTTP/1.1" 200 ...
# Redaction (not suppression) is used deliberately: ordinary access logging for
# every other route is preserved unchanged, and even the token-bearing requests
# are still logged — only the token segment itself is replaced. Disabling
# `accesslog` globally would destroy request observability that P10-OB1 and the
# future provider-dependent PSRR items depend on, so it is NOT done here.
#
# Mechanism: a stdlib ``logging.Filter`` attached to the ``gunicorn.access``
# logger inside the worker (``post_fork``), where the access records are
# emitted. Gunicorn passes its atoms dict as ``record.args``; sanitizing those
# values rewrites the line before any handler formats it. This adds no new
# logging platform, no dependency, no proxy assumption, and no topology change.
#
# SCOPE BOUNDARY: this hardens the REPOSITORY-CONTROLLED access log only. What a
# hosting provider or reverse proxy records upstream remains OPEN and must be
# verified at the future provider-dependent gate.
import logging  # noqa: E402  (config module; imported where it is used)
import re       # noqa: E402

# Any path segment following /verify/ or /reset/ is a raw token. The segment is
# replaced wholesale, so percent-encoded tokens are redacted just as raw ones
# are; the route itself stays visible for observability.
_TOKEN_PATH_PATTERN = re.compile(r"(/(?:verify|reset)/)[^/\s?\"]+")
_TOKEN_REDACTION = r"\1[REDACTED]"


def _redact_token_paths(value):
    """Return ``value`` with any token-bearing path segment redacted."""
    if isinstance(value, str):
        return _TOKEN_PATH_PATTERN.sub(_TOKEN_REDACTION, value)
    return value


class _TokenPathRedactingFilter(logging.Filter):
    """Redact raw verification/reset tokens from Gunicorn access records.

    Never drops a record (always returns True): observability is preserved and
    only the sensitive path segment is rewritten."""

    def filter(self, record):
        args = getattr(record, "args", None)
        if isinstance(args, dict):
            for key, value in list(args.items()):
                args[key] = _redact_token_paths(value)
        elif isinstance(args, tuple):
            record.args = tuple(_redact_token_paths(v) for v in args)
        if isinstance(getattr(record, "msg", None), str):
            record.msg = _redact_token_paths(record.msg)
        return True


def _install_token_redaction():
    """Attach the redaction filter once to the Gunicorn access logger."""
    access_logger = logging.getLogger("gunicorn.access")
    if not any(isinstance(f, _TokenPathRedactingFilter)
               for f in access_logger.filters):
        access_logger.addFilter(_TokenPathRedactingFilter())


def post_fork(server, worker):        # noqa: ARG001  (Gunicorn hook signature)
    """Gunicorn hook: access records are emitted in the worker process."""
    _install_token_redaction()


def when_ready(server):               # noqa: ARG001  (Gunicorn hook signature)
    """Defensive: also cover any access record emitted by the arbiter."""
    _install_token_redaction()
