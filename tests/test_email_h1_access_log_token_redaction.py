"""EMAIL-H1 repair — repository-controlled Gunicorn access-log token redaction.

File: tests/test_email_h1_access_log_token_redaction.py
Purpose: reproduce and pin the BLOCKING finding that the governed production
serving stack (`gunicorn -c gunicorn.conf.py web.app:app`) wrote RAW
verification/reset tokens into its access log. This suite exercises the ACTUAL
repository-controlled Gunicorn logging seam — a Flask `test_client` cannot
observe it — and additionally boots the real server end-to-end.
Input contract: `gunicorn.conf.py` (`_TokenPathRedactingFilter`,
`_redact_token_paths`, `post_fork`); the routes `/verify/<token>` and
`/reset/<token>`.
Output contract: no raw token and no percent-encoded token in access-log output;
the token-bearing routes remain logged in redacted form; ordinary routes keep
full access logging; no record is dropped.
Prohibited: disabling access logging to pass; asserting on a stubbed logger that
does not represent the governed seam.
Scope note: PROVIDER/REVERSE-PROXY ACCESS-LOG BEHAVIOUR IS OUT OF SCOPE and
remains OPEN — it is not provable from this repository.
"""
import importlib.util
import logging
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONF_PATH = os.path.join(ROOT, "gunicorn.conf.py")
RAW_TOKEN = "AccessLogProbeToken" + "K" * 24 + "9"
ENCODED_FRAGMENT = "%41%63%63%65%73%73"        # percent-encoded "Access"


def _load_conf():
    spec = importlib.util.spec_from_file_location(
        "_inventorai_gunicorn_conf_logprobe", CONF_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


# --- the governed logging seam, exercised directly ----------------------------

def _record(fmt, atoms):
    """Build an access record carrying Gunicorn's atoms dict.

    ``args`` is assigned after construction: ``LogRecord.__init__`` special-cases
    a single-element mapping and would raise, whereas Gunicorn sets the atoms
    dict as ``record.args`` through the normal logging call path."""
    record = logging.LogRecord("gunicorn.access", logging.INFO, __file__, 0,
                               fmt, None, None)
    record.args = atoms
    return record


def test_filter_redacts_the_raw_token_from_the_request_line():
    conf = _load_conf()
    rec = _record("%(r)s", {"r": 'GET /reset/%s HTTP/1.1' % RAW_TOKEN})
    assert conf._TokenPathRedactingFilter().filter(rec) is True   # never dropped
    assert RAW_TOKEN not in rec.args["r"]
    assert "/reset/[REDACTED]" in rec.args["r"]


def test_filter_redacts_the_verify_route_too():
    conf = _load_conf()
    rec = _record("%(r)s", {"r": 'GET /verify/%s HTTP/1.1' % RAW_TOKEN})
    conf._TokenPathRedactingFilter().filter(rec)
    assert RAW_TOKEN not in rec.args["r"]
    assert "/verify/[REDACTED]" in rec.args["r"]


def test_filter_redacts_the_url_atom_and_the_referer_atom():
    conf = _load_conf()
    rec = _record("%(U)s %(f)s", {"U": "/reset/%s" % RAW_TOKEN,
                                  "f": "http://x/verify/%s" % RAW_TOKEN})
    conf._TokenPathRedactingFilter().filter(rec)
    assert RAW_TOKEN not in rec.args["U"]
    assert RAW_TOKEN not in rec.args["f"]


def test_filter_redacts_a_percent_encoded_token_segment():
    conf = _load_conf()
    rec = _record("%(r)s", {"r": 'GET /reset/%sSuffix HTTP/1.1' % ENCODED_FRAGMENT})
    conf._TokenPathRedactingFilter().filter(rec)
    assert ENCODED_FRAGMENT not in rec.args["r"]


def test_filter_leaves_ordinary_paths_untouched():
    conf = _load_conf()
    rec = _record("%(r)s", {"r": 'GET /login HTTP/1.1'})
    conf._TokenPathRedactingFilter().filter(rec)
    assert rec.args["r"] == 'GET /login HTTP/1.1'


def test_filter_is_installed_idempotently_by_the_worker_hook():
    conf = _load_conf()
    access_logger = logging.getLogger("gunicorn.access")
    before = list(access_logger.filters)
    try:
        conf.post_fork(None, None)
        conf.post_fork(None, None)
        installed = [f for f in access_logger.filters
                     if type(f).__name__ == "_TokenPathRedactingFilter"]
        assert len(installed) == 1
    finally:
        access_logger.filters = before


def test_access_logging_is_not_globally_disabled():
    """The fix must redact, never suppress: ordinary observability is kept."""
    conf = _load_conf()
    assert conf.accesslog == "-"
    assert conf.errorlog == "-"


# --- end-to-end against the real governed serving stack -----------------------

@pytest.mark.skipif(shutil.which("gunicorn") is None,
                    reason="TOOL MISSING: gunicorn is a pinned production "
                           "dependency; a clean environment must install "
                           "requirements.txt before this evidence is valid")
def test_real_gunicorn_access_log_contains_no_raw_token(tmp_path):
    """Boots `gunicorn -c gunicorn.conf.py web.app:app` — the exact governed
    command — and inspects the real access log."""
    port = _free_port()
    access_log = tmp_path / "access.log"
    env = dict(os.environ,
               INVENTORAI_SECRET_KEY="email-h1-access-log-probe",
               INVENTORAI_DB_PATH=str(tmp_path / "probe.sqlite"),
               PORT=str(port))
    env.pop("INVENTORAI_ENV", None)
    proc = subprocess.Popen(
        ["gunicorn", "-c", "gunicorn.conf.py", "web.app:app",
         "--access-logfile", str(access_log),
         "--error-logfile", str(tmp_path / "error.log")],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, start_new_session=True)
    try:
        base = "http://127.0.0.1:%d" % port
        for _ in range(30):
            time.sleep(1)
            try:
                urllib.request.urlopen(base + "/health", timeout=3)
                break
            except Exception:
                continue
        else:                                      # pragma: no cover - probe
            pytest.fail("gunicorn did not become ready")
        for path in ("/reset/%s" % RAW_TOKEN, "/verify/%s" % RAW_TOKEN,
                     "/reset/%sTail" % ENCODED_FRAGMENT, "/login"):
            try:
                urllib.request.urlopen(base + path, timeout=10).read()
            except urllib.error.HTTPError:
                pass
        time.sleep(1)
    finally:
        proc.terminate()
        proc.wait(timeout=25)

    text = access_log.read_text(encoding="utf-8")
    assert text.strip(), "access log must not be empty (observability preserved)"
    assert RAW_TOKEN not in text
    assert ENCODED_FRAGMENT not in text
    assert "/reset/[REDACTED]" in text
    assert "/verify/[REDACTED]" in text
    assert "GET /login" in text            # ordinary logging still works
