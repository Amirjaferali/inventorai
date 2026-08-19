"""P10-OB1 — provider-neutral structured operational-logging seam.

File path: ``web/observability.py``
Purpose:   the smallest reusable, standard-library-only seam for emitting
           BOUNDED, machine-readable (JSON-line) operational events — runtime
           diagnostics such as health-probe failures and internal operational
           error categories. Operational logging is DISTINCT from the durable
           security/commercial audit tables in ``engine/account_store.py``
           (domain/security/commercial evidence — preserved, not duplicated
           here) and from analytics (which do not exist and are not added).

Input contract:
  * ``emit(event, level="info", **fields)`` — ``event`` must match the
    lower-case dotted token pattern; ``level`` one of debug/info/warning/
    error/critical; every keyword field must be in ``ALLOWED_FIELDS`` and
    carry a bounded safe value (bool, finite int/float, or a short string
    matching that field's grammar — lowercase dotted identifiers for
    vocabulary fields, an exception-class-shaped name for ``error_class``).
    Anything else is silently dropped — never emitted.

Output contract:
  * one JSON line per event on the process's standard error stream via the
    stdlib ``logging`` framework: stable keys ``ts``/``level``/``event`` plus
    the accepted allowlisted fields. Values are bounded tokens/numbers only.
  * ``emit`` NEVER raises — operational logging can never break the
    application.

Prohibited behaviors (binding, per the P10-OB1 authorization):
  * NO IP address, user-agent, device/network metadata, geography, account
    email, project/invention content, free-form user text, password, token,
    session identifier, API credential, or raw exception payload may pass
    through this seam — the field allowlist and value pattern enforce this;
  * NO analytics, behavioral tracking, or third-party telemetry/monitoring
    SDK/network export of any kind — standard library only;
  * NO log destination, retention, rotation, or aggregation policy is decided
    here (the framework-default stream is the provider-neutral seam);
  * NO duplication of the durable audit tables and NO schema change.
"""
import json
import logging
import math
import re

OPERATIONAL_LOGGER_NAME = "inventorai.operational"

# The complete bounded operational vocabulary. Adding a field is a governed
# code change, never a runtime capability.
ALLOWED_FIELDS = frozenset(
    {"component", "outcome", "error_class", "detail_code", "count",
     "duration_ms"})

_EVENT_RE = re.compile(r"^[a-z][a-z0-9_.]{0,63}$")
# Per-field value grammars. Vocabulary fields accept only lowercase dotted
# identifiers; ``error_class`` accepts only Python-exception-class-shaped
# names. Both exclude whitespace, '@' (emails), '/' (paths), '-' and
# mixed-case token shapes typical of secrets/credentials — free-form user
# text and common secret formats can never satisfy either. (A deliberately
# lowercase-identifier-formatted secret cannot be detected semantically;
# call sites are code-reviewed against that.)
_IDENT_RE = re.compile(r"^[a-z][a-z0-9_.]{0,63}$")
_CLASS_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_.]{0,63}$")
_STRING_FIELD_RES = {"component": _IDENT_RE, "outcome": _IDENT_RE,
                     "detail_code": _IDENT_RE, "error_class": _CLASS_RE}

_LEVELS = {"debug": logging.DEBUG, "info": logging.INFO,
           "warning": logging.WARNING, "error": logging.ERROR,
           "critical": logging.CRITICAL}


class OperationalJsonFormatter(logging.Formatter):
    """Deterministic JSON-line rendering with stable sorted keys."""

    def format(self, record):
        payload = {"ts": self.formatTime(record),
                   "level": record.levelname,
                   "event": getattr(record, "op_event", "operational.message")}
        for name, value in getattr(record, "op_fields", {}).items():
            payload[name] = value
        return json.dumps(payload, sort_keys=True)


def _value_allowed(name, value):
    """Bounded safe values only: bool, finite int/float, or a short string
    matching the field's grammar (`_STRING_FIELD_RES`). Everything else
    (objects, dicts, free text, emails, paths, hyphenated/mixed-case secret
    shapes, over-long strings) is rejected."""
    if isinstance(value, bool):
        return True
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, str):
        pattern = _STRING_FIELD_RES.get(name)
        return pattern is not None and bool(pattern.match(value))
    return False


def get_operational_logger():
    """Return the operational logger, idempotently wiring one stream handler
    with the JSON formatter. ``propagate`` is off so the bounded seam is the
    only rendering path for these events."""
    logger = logging.getLogger(OPERATIONAL_LOGGER_NAME)
    if not any(getattr(h, "_inventorai_operational", False)
               for h in logger.handlers):
        handler = logging.StreamHandler()
        handler._inventorai_operational = True
        handler.setFormatter(OperationalJsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger


def emit(event, level="info", **fields):
    """Emit one bounded structured operational event. Unsupported fields and
    unsafe values are dropped, an invalid event name is replaced with a fixed
    marker, and no failure of the logging path ever propagates."""
    try:
        if not isinstance(event, str) or not _EVENT_RE.match(event):
            event = "operational.invalid_event"
        clean = {}
        for name, value in fields.items():
            if name in ALLOWED_FIELDS and _value_allowed(name, value):
                clean[name] = value
        get_operational_logger().log(
            _LEVELS.get(level, logging.INFO), event,
            extra={"op_event": event, "op_fields": clean})
    except Exception:
        # Operational logging must never break the application.
        pass
