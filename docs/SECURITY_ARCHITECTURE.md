# Security Architecture
Status: APPROVED (truth-labeled per P10-SEC1 — sections are classified; a
HISTORICAL section states a superseded or unimplemented claim, not current truth)

## Authentication — IMPLEMENTED (historical "anonymous-only" claim SUPERSEDED per P10-C §9)
Full account authentication is live: register / login / logout / logout-all /
email verification / recovery / reset / deactivation (`web/app.py`); scrypt
password hashing, hashed-only tokens and API credentials, signed-cookie
sessions with server-side idle/absolute/epoch checks (`engine/account_store.py`,
`engine/auth_session.py`).

## Security headers — IMPLEMENTED NOW (P10-SEC1, provider-neutral)
One centralized `after_request` seam applies to EVERY response (HTML, JSON,
redirects, 4xx/5xx, static files, `/health`):
- `Content-Security-Policy: default-src 'none'; script-src 'self';
  style-src 'unsafe-inline'; frame-ancestors 'none'; base-uri 'none';
  form-action 'self'` — smallest policy supported by the verified inventory
  (only same-origin static JS; zero inline scripts/handlers; inline styles
  only; no external origins; no fetch/XHR; no framing; same-origin forms).
  No `'unsafe-eval'`; no wildcard/host/scheme sources; no reporting endpoint.
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` (consistent with `frame-ancestors 'none'`)
- `Referrer-Policy: strict-origin-when-cross-origin`
These headers harden responses; they are NOT a security review, NOT PSRR
execution, NOT a TLS posture, and NOT a compliance claim.

## HSTS — DEFERRED (truth boundary)
`Strict-Transport-Security` is deliberately NOT emitted anywhere: no TLS
termination and no trusted reverse-proxy semantics exist in this repository,
so sending HSTS (or trusting forwarded-proto headers) would assert an HTTPS
posture that does not exist. Deferred to the future production/infrastructure
gate; `includeSubDomains`/`preload` additionally need separate authorization.

## Secrets — IMPLEMENTED (env-based) / rotation policy HISTORICAL
- Flask secret from `INVENTORAI_SECRET_KEY`; fail-closed when
  `INVENTORAI_ENV=production`; never hard-coded (`web/app.py`).
- `.env` gitignored; API keys env-only.
- HISTORICAL/UNENFORCED: "ANTHROPIC_API_KEY rotation: 90 days" — no rotation
  mechanism exists; moot while AI transfer is disabled in code
  (`engine/ai_advisor.py`: `AI_ADVISORY_ENABLED = False`). PSRR item 8
  reassesses secrets operations.

## Input Validation — PARTIAL (labels per P10-RV1 revalidation; hardened by P10-SEC2)
- IMPLEMENTED: Jinja autoescape everywhere (zero `| safe`); no `eval()`/
  `exec()` anywhere; success-criteria fields capped at 1000 chars.
- IMPLEMENTED NOW (P10-SEC2): a transport-level request-body bound
  (`MAX_CONTENT_LENGTH` = 128 KiB → standard 413, security headers intact)
  on every surface; a semantic free-text bound (`MAX_FREE_TEXT_CHARS` =
  20,000 chars — justified from present product behavior, deliberately NOT
  the stale historical 10,000 figure) with NUL-byte REJECTION on the two
  primary free-text surfaces (`/start` idea text; `/session/<sid>`
  answer/action text). Explicit rejection only — never silent truncation,
  never stripping; Arabic/Unicode/multiline/punctuation pass untouched (no
  general control-character sanitizer, no ASCII-only rule). Legacy
  fixed-domain ILT-002 start routes remain transport-bounded only
  (historical evidence surfaces, behavior preserved).
- These bounds are robustness controls only: NOT a WAF, NOT DoS prevention,
  NOT a production proxy limit, NOT OWASP-compliance, NOT complete abuse
  prevention — PSRR item 1 still reassesses input security at release time.
- HISTORICAL — SUPERSEDED (was "NOT IMPLEMENTED"): the old unqualified
  "10000-char cap + null-byte stripping" claim; the implemented posture
  above (different limit; rejection, not stripping) replaces it.
- HISTORICAL/MOOT while AI is disabled: LLM output schema validation.

## Abuse Protection — PARTIAL
- IMPLEMENTED: store-backed auth-surface rate-limit floor with bounded
  cleanup (`auth_rate_limits`); CSRF tokens on state-changing routes;
  non-enumerating generic denials.
- NOT IMPLEMENTED (historical claim): "10 requests/minute per session_id"
  broad limiter and per-session token budgets. Broad abuse controls remain
  NOT CLAIMED DELIVERED (PSRR §8 preserved; PSRR items 23–25 reassess).

## Dependency auditing — LOCAL FOUNDATION IMPLEMENTED (P10-DEP1)
`scripts/run_dependency_audit.py` audits the single authoritative dependency
declaration (`requirements.txt`: Flask + pytest, pinned) with local,
provider-neutral `pip-audit` (OSV/PyPI advisories): evidence header
(repo SHA, input SHA-256, timestamp), tool exit status preserved verbatim —
findings and advisory-network failures are never converted into a clean
result; no automatic remediation. pip-audit is environment TOOLING only,
never a runtime dependency. A clean run is POINT-IN-TIME only (see
`docs/governance/evidence/phase10_p10_dep1/P10_DEP1_POINT_IN_TIME_AUDIT_
EVIDENCE.md`). NOT continuous scanning, NOT hosted monitoring, NOT CI
enforcement, NOT the formal production dependency/vulnerability review —
that remains PSRR-time (items 12–13).

## Pre-Release Checklist — SUPERSEDED BY PSRR (execution is PSRR-ONLY)
The old checklist (no hardcoded secrets; no eval; HTTPS enforced; .env not
committed; DEBUG off in production; pip audit) is subsumed by the registered
37-item PSRR scope (`docs/governance/PSRR_PRODUCTION_SECURITY_RELEASE_
READINESS_REGISTRATION.md` §7). PSRR is NOT executed and NOT complete;
public production deployment remains BLOCKED until PSRR = GO plus the OD-P
deployment gate and explicit Owner authorization. Current safe defaults that
already exist: debug off unless `INVENTORAI_DEBUG` truthy; loopback host
default; production-gated Secure session cookie; HttpOnly + SameSite=Lax.
