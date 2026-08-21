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
