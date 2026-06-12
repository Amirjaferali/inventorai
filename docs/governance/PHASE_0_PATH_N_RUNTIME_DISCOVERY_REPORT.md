# PHASE 0 — PATH N RUNTIME DISCOVERY REPORT

## 1. Status

- PHASE 0 PATH N RUNTIME DISCOVERY REPORT
- Read-only discovery. No implementation authorized by this report.
- Extends QUESTION_FLOW_DISCOVERY_REPORT.md (`e1095c6`) with
  owner-executed repository inspection detail of the question
  lookup call chain.

## 2. Evidence basis

All findings below are FACT, sourced from owner-executed, owner-pasted
repository inspection output (grep/python inspection, 2026-06-12)
against HEAD `d2b2a9a`, unless explicitly labeled ASSUMPTION or UNKNOWN.

## 3. Exact files and functions in the question flow

| File | Function / object | Evidence (line) |
|------|-------------------|-----------------|
| `web/app.py` | imports `infer_domain`; `run_iteration`, `select_next_gap`, `get_question` | L8, L10 |
| `web/app.py` | `index()` | L18 |
| `web/app.py` | `start()` — infers domain, calls `run_iteration(state, idea_text)` | L22–L33 |
| `web/app.py` | `start_ilt002_water_leak()` — fixed-domain route | L38–L46 |
| `web/app.py` | `start_ilt002_combination_lock()` — fixed-domain route | L51–L59 |
| `web/app.py` | `show_session(sid)` — calls `get_question(state.domain, gap_type, iterations_open)` | L64, L77 |
| `web/app.py` | `submit_answer(sid)` — calls `run_iteration(state, response)` | L108, L115 |
| `web/app.py` | `SESSION_STORE = {}` — entries: `{"state", "last_result", "transcript"}` | L15, L34/47/60 |
| `engine/progression_loop.py` | `QUESTIONS` dict — generic question bank, incl. Stage 3 questions (verbatim from STAGE3_QUESTION_SET.md, admitted `5926b63`) | L96, L127 |
| `engine/progression_loop.py` | `get_question(domain, gap_type, iterations_open)` — asks domain layer first, falls back to generic `QUESTIONS` | L167–L177 |
| `engine/progression_loop.py` | `run_iteration()` — multiple question return paths; pattern `get_ai_question(...) or get_question(...)` | L522–L531, L559–L568, L590–L600 |
| `engine/domain_rules.py` | `_REGISTRY = load_registry("domains/")` (module import time) | L6–L7 |
| `engine/domain_rules.py` | `get_domain_question(domain, gap_type, iterations_open)` — reads `mapping.get("questions", [])`, returns `questions[index].get("text")` | L68–L83 |
| `engine/domain_registry.py` | `load_registry(domains_dir)` — loads `domains/<subdir>/domain.json`, validates `schema_version == "1.0"` | L96–L115 |
| `domains/electronics_electrical/domain.json` | top-level keys include `gap_type_mappings` (question source), `classification_signals`, `substance_signals`, `rule_nuances`, `journey_extension` | python key dump |
| `engine/idea_state.py` | `class IdeaState` — has `maturity_level`, `current_stage`; no path field observed | L86–L90 |

## 4. Observed question-lookup chain (FACT)

Domain-specific path:

    web/app.py
      → engine.progression_loop.get_question(domain, gap_type, iterations_open)
        → engine.domain_rules.get_domain_question(domain, gap_type, iterations_open)
          → _REGISTRY (loaded once from domains/ at import)
            → domains/electronics_electrical/domain.json
              → gap_type_mappings[].questions[index].text

Fallback path (when domain layer returns None):

    get_question() → QUESTIONS[gap_type] (generic bank, engine-internal)

AI-advisory path (inside run_iteration() only):

    get_ai_question(state.domain, gap, ctx) or get_question(...)
    — AI result takes precedence when non-None.

## 5. All question-generation entry points found (FACT)

1. **Display-time:** `web/app.py::show_session()` L77 calls
   `get_question()` directly to render the current question.
   (Also an `INTAKE_QUESTION` constant at L85 for the no-gap case.)
2. **Iteration-result:** `engine/progression_loop.py::run_iteration()`
   produces question text at multiple observed return paths
   (cascade-opened gap L522–L535; closing question L548; standard
   iteration L559–L568; post-integration cascade L590–L605).
3. **Generic fallback:** engine-internal `QUESTIONS` dict (L96),
   reached when `get_domain_question()` returns None.
4. **AI advisory:** `get_ai_question()` precedence inside
   `run_iteration()` only — NOT in the `show_session()` display path.

Consequence (FACT, structural): question text reaches the user from
TWO independent call sites (web display-time + engine iteration-result).
Any Path N integration must produce consistent content at BOTH, or
sessions could display mixed-path questions.

## 6. Session path/designation field (FACT)

- `SESSION_STORE` entries contain exactly `state`, `last_result`,
  `transcript` (plus `last_question` added at render time, L92–L93).
- `IdeaState` shows no path/designation field in inspected lines.
- FACT: no path or designation field currently exists at either the
  web-session level or the engine-state level.

## 7. Candidate integration points (analysis — NO selection made)

| Candidate | Mechanics | Risk profile |
|-----------|-----------|--------------|
| C-1: Path stored in `SESSION_STORE` entry (web layer) | New dedicated route sets `"path": "N"`; default absent = legacy | Least invasive to store. BUT: `get_question()` and `run_iteration()` do not receive the session entry — path would not reach the lookup without further plumbing. Display-time call site could consult it; engine call site could not. |
| C-2: Path stored as `IdeaState` field | `state` travels into `run_iteration()` and is available at both call sites via `state` | Touches `engine/idea_state.py` (additive field). `get_question(domain, gap_type, iterations_open)` still would not see it without signature change or reading from state at call sites. |
| C-3: Path-scoped lookup inside domain layer | `get_domain_question()` consults a path value to choose Path N JSON vs `gap_type_mappings` | Keeps selection in the layer that "owns questions" (L71 comment). Same plumbing problem: path must arrive at `domain_rules` somehow. |

No candidate is selected by this report. Selection is an owner
decision contingent on the §8 ruling.

## 8. STOP-adjacent finding (recorded, NOT resolved)

FACT: `get_question()` is defined inside `engine/progression_loop.py`
and its signature `(domain, gap_type, iterations_open)` carries no
path-capable parameter. The generic fallback bank `QUESTIONS` is also
engine-internal.

Tension with invariants:
- Plan §4.5: `progression_loop.py` zero net changes.
- Plan §9: STOP if "Path N selection cannot be achieved without
  modifying engine/progression_loop.py".

Assessment: this is a CONDITIONAL STOP, not a confirmed STOP.
This report records it and does not resolve it. Path designation can
plausibly reach the domain layer without engine modification only if
the carrier is something already passed through the chain. The only
candidates already passed are `domain`, `gap_type`,
`iterations_open`, and (into `run_iteration()`) `state`.

- UNKNOWN: whether the owner would treat an additive `IdeaState` field
  (C-2) as compatible with the invariant set (idea_state.py is not in
  the untouched list, but `get_question()` reading state would still
  require call-site changes inside progression_loop.py).
- UNKNOWN: whether `get_ai_question()` behavior for Path N sessions is
  defined anywhere (AI advisory precedence inside run_iteration()
  could override Path N content if AI is ever enabled).
- ASSUMPTION (from NEXT_SESSION.md, dated 2026-05-22):
  AI_ADVISORY_ENABLED = False in production — currency unverified.

Per the plan's STOP discipline: no integration option is selected.
The owner must rule on the conditional STOP before any Phase 1
authorization.

## 9. Additional observations (FACT)

- `_REGISTRY` loads once at module import (`domain_rules.py` L7) —
  any Path N content file loaded the same way inherits this
  load-once behavior; content changes require process restart.
- Fixed-domain ILT routes (L38, L51) bypass `infer_domain()` —
  consistent with D-003 mitigation; a future Path N route would
  follow this same dedicated-route pattern.
- `domain.json` question content lives under `gap_type_mappings` —
  consistent with `e1095c6`.

## 10. Authorization and integrity confirmations

- No implementation is authorized by this report.
- No files were modified during Phase 0. All commands executed were
  read-only (grep, head, python key inspection), owner-executed
  in Codespace.
- `domain.json`, `web/app.py`, `engine/progression_loop.py`,
  Path T bank: untouched.
- R2 remains HELD.
- FORM T remains BLOCKED.
- S-6 remains UNCLASSIFIED.
- AA-5 remains BLOCKED.

## 11. Required next owner decisions

1. Ruling on the §8 conditional STOP: which carrier (if any) may
   transport the path designation, and whether any additive change
   to `idea_state.py` or call sites inside `progression_loop.py`
   is admissible or prohibited.
2. Whether AI-advisor precedence for Path N sessions must be
   specified before Phase 1.
3. Whether the dual call-site consistency requirement (§5) becomes
   a mandatory runtime test (addition to plan §7).