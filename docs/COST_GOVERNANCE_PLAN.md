# Cost Governance Plan
Status: APPROVED

## Per-Session Budget
Level 0: 5 iterations ~1500 tokens = ~7500 tokens
Level 1: 5 iterations ~1800 tokens = ~9000 tokens
Level 2: 3 iterations ~2000 tokens = ~6000 tokens
Total: 13 iterations ~22500 tokens ~0.08-0.12 USD

## Hard Limits
Max input tokens per call: 4000 (ai_advisor.py)
Max output tokens per call: 1000 (max_tokens parameter)
Max iterations per session: 15 (progression_loop.py hard stop)
Max session cost USD: 0.25 (ai_advisor.py cumulative check)

## Kill Switch
1. Set INVENTORAI_KILL_SWITCH=1
2. web/app.py checks on every request
3. Returns HTTP 503 Service temporarily paused
4. To re-enable: unset variable and restart

## Monthly Budget
MVP Internal: 100 sessions ~10 USD
Early access: 1000 sessions ~100 USD
Growth: 10000 sessions ~1000 USD

## Cost Alerts
Daily spend >80% of daily budget: Email owner
Single session cost >0.20 USD: Log and flag
Monthly spend >50% by day 15: Email owner
Unexpected spike 3x average: Immediate email and auto-pause
