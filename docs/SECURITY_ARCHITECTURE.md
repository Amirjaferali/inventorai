# Security Architecture
Status: APPROVED

## Authentication
Current MVP: Anonymous sessions keyed by UUID4 session_id.
Target: Email/password or OAuth. HMAC-SHA256 signed tokens.

## Secrets
- API keys in .env only
- .env in .gitignore NEVER commit keys
- ANTHROPIC_API_KEY rotation: 90 days

## Input Validation
- Max length 10000 characters
- Strip null bytes and control characters
- No HTML rendering of user input
- All LLM output validated against JSON schema (INV-008)
- No eval() of LLM output

## Abuse Protection
- Rate limit: 10 requests/minute per session_id
- Hard token budget per session
- User input never interpolated into system prompt

## Pre-Release Checklist
- [ ] No hardcoded secrets
- [ ] No eval() or exec() on user or LLM input
- [ ] HTTPS enforced
- [ ] .env not committed
- [ ] DEBUG mode disabled in production
- [ ] pip audit run no critical CVEs
