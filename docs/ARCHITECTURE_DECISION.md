# Architecture Decision Document
**Version:** 1.0  
**Status:** Active  
**Last Updated:** 2025-05-17  
**Owner:** Project Lead

---

## 1. Project Identity

The platform is a deterministic, governance-first, AI-assisted invention analysis system.

It is a structured decision journey — not a conversation.  
It produces auditable, reproducible gate decisions — not AI opinions.  
It guides inventors through a defined workflow — not an open-ended chat.

---

## 2. What This Platform Is NOT

> These are binding constraints. Any feature request that conflicts with this list must be rejected without exception.

```
NON_GOALS.md

- NOT a chatbot
- NOT an autonomous AI agent
- NOT a CAD system
- NOT a product generator
- NOT a project execution platform
- NOT a system where AI decides workflow transitions
- NOT a system where AI determines gate outcomes
- NOT a system where UI controls state transitions
- NOT a fully automated engineering platform
- NOT a no-code replacement for engineers
- NOT a conversational AI interface
- NOT a multi-path dynamic workflow engine
- NOT a patent filing service
- NOT a simulation engine
- NOT an investor platform
```

---

## 3. Core Architectural Principles

| Principle | Meaning |
|---|---|
| **Single Source of Truth** | Workflow state lives in the database only. Never in memory, session, UI, or AI context. |
| **Deterministic Transitions** | Every state transition is defined in code. No transition can be triggered by AI output or UI action alone. |
| **Explicit State Ownership** | Every state has one owner: the server-side FSM. UI reads state. UI never writes state. |
| **Auditability** | Every action, AI call, and gate decision is logged immutably with full context. |
| **Traceability** | Any gate decision can be replayed from its stored inputs and produce the same output. |
| **Predictability** | The system must aim for operational consistency and reproducibility through: pinned model versions, fixed prompts, structured outputs, benchmark validation, and deterministic gate evaluation. |
| **Reproducibility** | Any analysis can be re-run from its stored prompt version, model version, and input hash. |
| **Governance-First** | Governance structures (gate rules, benchmarks, event logs) are built before features — not after. |
| **AI as Advisor** | AI produces structured recommendations. The server-side rule engine makes all decisions. |

---

## 4. Critical Constraints

```
HARD CONSTRAINTS — Never violated under any circumstance:

- No hidden workflow behavior
- No optimistic navigation (UI never assumes a transition will succeed)
- No autonomous AI routing decisions
- No uncontrolled orchestration
- No silent architectural drift
- No feature additions without pre-implementation checklist
- No framework-driven architecture decisions (no LangGraph, no LangChain)
- No "magic AI behavior"
- No AI calls outside of designated workflow states
- No "latest" model version in any environment
```

---

## 5. AI Boundary Contract

### AI Responsibilities — ALLOWED
- Analyze structured input fields
- Generate domain-specific engineering reports
- Detect contradictions between domain outputs
- Identify missing or incomplete information
- Provide structured JSON recommendations
- Explain risks and feasibility concerns
- Assist gate evaluation by producing structured evidence

### AI Responsibilities — FORBIDDEN
- Deciding workflow state transitions
- Modifying system state autonomously
- Bypassing gate evaluation
- Self-routing between analysis domains
- Hidden retries without logging
- Uncontrolled tool orchestration
- Changing gate rules or governance parameters
- Determining PASS / WARN / BLOCK outcomes

> **Rule:** AI analyzes. Server decides. Always.

---

## 6. Gate Architecture

### Gate Authority
All PASS / WARN / BLOCK decisions are **server-authoritative**.  
Gate decisions are made by a deterministic rule engine that reads from versioned YAML rule files.  
The rule engine receives structured JSON from AI analysis — it does not call AI.

### Gate Rule Format
```yaml
# gate_rules/iot_electronics_v1.yaml
rules:
  - id: "GR-001"
    version: "1.0"
    domain: "iot_electronics"
    condition: "feasibility_score < 30"
    outcome: "BLOCK"
    rationale: "Technical feasibility below minimum threshold"
    
  - id: "GR-002"
    version: "1.0"
    domain: "iot_electronics"
    condition: "missing_fields.length > 2"
    outcome: "WARN"
    rationale: "Insufficient input data for reliable analysis"
    
  - id: "GR-003"
    version: "1.0"
    domain: "iot_electronics"
    condition: "patent_conflict == true"
    outcome: "BLOCK"
    rationale: "Potential patent conflict detected"
```

### Gate Decision Log (required fields)
```json
{
  "event_id": "uuid",
  "timestamp": "ISO8601",
  "workflow_state": "GATE_EVALUATION",
  "gate_outcome": "PASS | WARN | BLOCK",
  "gate_rule_version": "1.0",
  "gate_input_payload": {},
  "ai_model_version": "claude-sonnet-4-20250514",
  "prompt_version": "iot_electronics_v1.0",
  "input_hash": "sha256",
  "output_schema_version": "1.0",
  "user_id": "uuid",
  "rationale_ids": ["GR-001"],
  "error_code": null
}
```

---

## 7. Event Logging Contract

All events are **append-only**. No event can be deleted or modified after write.

### Required fields for every event
```
event_id          — UUID, unique per event
timestamp         — ISO8601, server-generated
workflow_state    — current FSM state at time of event
event_type        — STATE_TRANSITION | AI_CALL | GATE_DECISION | ERROR | USER_ACTION
user_id           — UUID
idea_id           — UUID
ai_model_version  — pinned model string (when applicable)
prompt_version    — prompt file version (when applicable)
input_hash        — SHA256 of normalized input (when applicable)
output_schema_version — schema version used (when applicable)
gate_outcome      — PASS | WARN | BLOCK | null
gate_rule_version — rule file version | null
error_code        — error identifier | null
duration_ms       — execution time in milliseconds
```

---

## 8. Prompt Governance

### Model Version Pinning
```
Production model: claude-sonnet-4-20250514
Never use: "latest" or any alias
Model changes require: full benchmark migration protocol
```

### Prompt Versioning
- All prompts stored as versioned files in `/prompts/`
- Naming convention: `{domain}_system_prompt_v{major}.{minor}.md`
- Every prompt change requires benchmark regression before deployment
- Rollback: revert to previous prompt file version

### Prompt Change Classification

| Change Type | Evidence Required |
|---|---|
| Gate rule modification | Full evidence: E2E tests, benchmark delta, domain expert sign-off |
| Prompt wording change | Reviewed: benchmark delta check + domain expert sign-off |
| UI text / labels | Lightweight: PR review only |
| Schema field addition | Full evidence: backward compatibility check + benchmark delta |
| Model version migration | Full evidence: full benchmark suite against new model |

---

## 9. Benchmark Validation

### Minimum Requirements for Phase 1
- **20 test cases** covering IoT + Electronics domain
- **8 PASS cases** — valid, complete, feasible ideas
- **8 WARN cases** — valid but with identified challenges
- **4 BLOCK cases** — invalid, incomplete, or infeasible ideas
- **4 adversarial cases** — designed to test edge cases and manipulation attempts

### Acceptance Thresholds
```
Output schema compliance:  ≥ 90%
Gate decision agreement:   ≥ 85% (reviewed by domain expert)
```

> If thresholds are not met: fix prompts → re-run benchmark → no deployment.

### Rollback Trigger
If benchmark success rate drops more than **10% within 24 hours** of a deployment → automatic rollback to last stable prompt version.

---

## 10. Change Management Protocol

### Pre-Implementation Checklist (required for all critical changes)
Every new state, gate rule, domain, schema field, or prompt change must document:

```
1. Current State       — what exists today
2. Gap Analysis        — what is missing or broken
3. Risks               — what could go wrong
4. Acceptance Criteria — what "done" looks like
5. Evidence Required   — how we prove it works (full vs lightweight)
6. Backward Compatibility Check — does this break existing data or workflows
```

### Evidence Levels

**Full Evidence Required:**
- Workflow state transitions
- Gate authority changes
- Auth / session logic
- Billing logic
- Security boundaries
- State integrity changes
- Model version migrations
- Schema breaking changes

**Reviewed (Lightweight Evidence):**
- Prompt wording adjustments
- Gate rule description changes
- Report section titles
- Domain expert sign-off required

**Lightweight (PR Review Only):**
- UI text, labels, translations
- Spacing, icons, cosmetic changes
- Documentation updates

---

## 11. Technology Decisions

| Component | Decision | Rationale |
|---|---|---|
| Frontend | Next.js + Tailwind | RTL/LTR support, SSR, proven |
| Backend | Python FastAPI | Typed, fast, clean for FSM logic |
| Database | Supabase (PostgreSQL + RLS) | Row-level security enforces idea isolation at DB layer |
| Auth | Supabase Auth | Email verification, JWT, password reset — no custom auth |
| AI | Anthropic Claude API | Pinned version, structured output |
| Async Processing | Minimal background processing only (Phase 1) | Phase 1 prioritizes simplicity, observability, and operational clarity over distributed scalability. Advanced queue orchestration is deferred until proven operational need. |
| FSM | Custom Python FSM | No LangGraph — deterministic, no framework drift |
| Gate Rules | YAML files (versioned in git) | Human-readable, auditable, and version-controlled. Rule changes still require review, benchmark validation, audit logging, and governance approval before activation. |
| Contracts | JSON Schema | Language-agnostic, human-readable, auditable |
| Export | WeasyPrint (Phase 2) | Proven Arabic RTL PDF support |
| Hosting | VPS + Domain + GitHub | Standard, controllable |

---

## 12. User Experience Principles

The platform must remain usable, understandable, and low-friction despite its governance-heavy architecture.

### UX Principles

| Principle | Requirement |
|---|---|
| **Cognitive Load** | Minimize the mental effort required at every step |
| **Workflow Friction** | Minimize unnecessary steps between user intent and result |
| **Time-to-First-Analysis** | Must remain short — governance must not create unnecessary delay |
| **State Transparency** | Users must always know their current workflow state and next required action |
| **Gate Clarity** | Users must always understand why a gate result (PASS/WARN/BLOCK) occurred |
| **Error Actionability** | Every error message must tell the user exactly what to do next |
| **Architectural Invisibility** | The UI must never expose internal architectural complexity to the user |
| **Governance Transparency** | Deterministic architecture should feel simple and trustworthy — not bureaucratic |

### UX Anti-Patterns — Forbidden

```
✗ Multi-step flows without visible progress indicators
✗ Hidden validation failures (silent errors)
✗ Technical terminology exposed to non-technical users
✗ AI-generated ambiguity in workflow guidance
✗ Excessive confirmation dialogs
✗ Long waiting periods without visible status updates
✗ PASS/WARN/BLOCK results without clear human-readable explanation
✗ Error states that leave users without a clear recovery path
```

### Governing Balance

> Governance ensures correctness. UX ensures the platform gets used.
> A perfectly governed platform that users abandon has failed its purpose.
> Every governance decision must be evaluated against its UX cost.

---

## 12b. Draft Persistence Principle

Users think slowly. They stop, return, reconsider, and revise. Punishing this behavior with data loss contradicts the platform's purpose.

### What Drafts Are

Drafts are pre-workflow persistence. They exist outside the deterministic FSM entirely.

```
Draft persistence exists to:
- Reduce cognitive interruption
- Prevent idea loss during composition
- Support thoughtful, non-linear input behavior
- Respect that good ideas take time to articulate
```

### What Drafts Are NOT

```
Drafts do NOT:
- Trigger AI analysis
- Trigger gate evaluation
- Transition workflow_state
- Lock input fields
- Generate input_hash
- Enter the deterministic FSM in any way
```

### The Boundary

Only explicit user submission (pressing Analyze / Submit) starts the deterministic workflow. Until that moment, all data is a draft — mutable, recoverable, and invisible to the analysis pipeline.

### Implementation Note

Draft state is a separate lightweight persistence layer — not a state in the FSM. Do not add DRAFT to the workflow_state enum. A simple `draft_fields` JSONB column on the ideas table (or a separate drafts table) is sufficient. The FSM begins at IDLE when the user submits — not before.

### Language Principle

When a user returns to an unfinished draft:

```
✗ "You have unfinished input"     — implies failure or obligation
✓ "تم حفظ تقدم فكرتك ويمكنك المتابعة من حيث توقفت"
                                  — implies continuity and respect
```

The difference is psychological. The platform is a partner in refining an idea — not a form waiting to be completed.

---

## 12c. Multi-Idea Workspace Principle

One user account is not one idea. Users may have multiple ideas simultaneously — at different stages, in different states, with completely isolated histories.

### Core Rule

Each idea is an independent workspace. No idea may overwrite, reference, or interfere with another idea belonging to the same user.

### What Each Idea Owns Independently

```
Each idea_id owns exclusively:
- Its own workflow_state
- Its own draft state (pre-submission)
- Its own input fields (locked after submission)
- Its own input_hash
- Its own AI analysis output
- Its own gate decision and rationale
- Its own report
- Its own event log entries
- Its own archived status and timestamp
```

### User-Facing States

The dashboard must present ideas in clearly distinguishable states. The technical state maps to user language as follows:

| Technical State | User-Facing Label (Arabic) |
|---|---|
| Draft (pre-FSM) | مسودة — لم تُرسل بعد |
| IDLE / INPUT_RECEIVED / COMPLETENESS_CHECK | قيد الإعداد |
| DOMAIN_ANALYSIS / GATE_EVALUATION | جاري التحليل |
| REPORT_GENERATED | مكتمل — التقرير جاهز |
| ARCHIVED | مؤرشف |
| ERROR | توقف — يحتاج مراجعة |

### Dashboard Requirements

The user dashboard must allow:

```
✓ Create a new idea workspace
✓ Continue an unfinished draft
✓ View ideas currently in analysis
✓ Open completed reports
✓ Archive completed ideas
✓ Distinguish clearly between all six states above
✓ Access event history per idea (Phase 2)
```

### Naming Convention

```
For users:    "مشاريعي" or "أفكاري" — natural language
For the DB:   idea records identified by idea_id — never "files"
For the API:  /ideas/{idea_id} — never /projects or /files
```

Using "files" technically creates confusion between document storage and workflow records. idea_id is the canonical identifier at every layer.

### Isolation Guarantee

The database enforces this through:
- RLS: every query is scoped to `auth.uid() = user_id`
- Every event_log entry carries both `user_id` and `idea_id`
- No cross-idea queries are possible through the client view
- No shared mutable state exists between ideas

One idea's ERROR state, BLOCK decision, or archival has zero effect on any other idea in the same account.

---

## 13. First Production Target

The first deployed version must be exactly this — nothing more:

```
✓ One domain: IoT + Electronics
✓ One workflow: single analysis path
✓ One language: Arabic (English in Phase 2)
✓ Five input fields: idea, problem, solution, beneficiary, domain
✓ One deterministic gate system: PASS / WARN / BLOCK
✓ One structured text report (no PDF in Phase 1)
✓ Benchmark-tested outputs (≥ 90% schema, ≥ 85% gate agreement)
✓ Full event logging from day one
✓ Privacy and disclaimer screen before first use
```

**Explicitly excluded from Phase 1:**
- PDF export
- Supplier API integrations
- Patent search
- Second language
- Versioning system
- Contradiction detection
- Second domain
- Paid subscription system

---

## 14. Architecture Decision Log

All significant decisions must be recorded here before implementation.

| ID | Decision | Rationale | Alternatives Rejected | Date |
|---|---|---|---|---|
| ADR-001 | Custom FSM over LangGraph | Deterministic control, no framework drift, full auditability | LangGraph introduces agent behavior incompatible with governance model | 2025-05-17 |
| ADR-002 | Gate rules in YAML, not code | Human-readable, auditable, changeable without deployment | Hardcoded if-else makes rules invisible and untestable | 2025-05-17 |
| ADR-003 | Supabase RLS for idea isolation | DB-layer enforcement cannot be bypassed by application bugs | Application-layer guards are insufficient for IP confidentiality | 2025-05-17 |
| ADR-004 | Pinned model version only | Silent model drift is the most likely quality failure mode | Floating "latest" breaks reproducibility and benchmark validity | 2025-05-17 |
| ADR-005 | Arabic first, English in Phase 2 | University cohort is Arabic-speaking; bilingual from day one doubles content complexity | Simultaneous bilingual launch before market validation is premature | 2025-05-17 |
| ADR-006 | IoT + Electronics as first domain | Covers 70%+ of submitted ideas; has quantifiable engineering calculations | Starting with mechanical or structural requires different calculation engines | 2025-05-17 |
| ADR-007 | No chatbot interface | Contradicts NON_GOALS; adds uncontrolled conversational state | Structured form enforces input quality and enables deterministic analysis | 2025-05-17 |
| ADR-008 | Append-only event log | Auditability requires immutable history; any mutable log is not an audit log | Mutable logs cannot be trusted in IP disputes or governance reviews | 2025-05-17 |
| ADR-009 | Predictability redefined from absolute determinism to operational consistency | LLMs are non-deterministic by nature — claiming "always produces same outputs" is technically false and undermines document credibility | Replaced with: consistency through pinned versions, fixed prompts, structured outputs, benchmark validation, and deterministic gate evaluation | 2025-05-17 |
| ADR-010 | User Experience Principles added as first-class architectural concern | A governance-heavy platform that users abandon has failed — UX cost must be evaluated alongside every governance decision | UX was implicit before; now explicit and binding with forbidden anti-patterns | 2025-05-17 |
| ADR-011 | Gate Rules YAML description corrected to require governance pipeline | "No deployment needed" implied rules could be changed without governance approval — a governance bypass risk | Clarified: YAML changes still require review, benchmark validation, audit logging, and governance approval before activation | 2025-05-17 |
| ADR-012 | Product name removed from architecture documents | Brand names change frequently — architecture must outlive branding. Name coupling causes costly refactoring across schemas, prompts, APIs, logs, and docs | Replaced all product name references with neutral "platform" or "system" terminology | 2025-05-17 |
| ADR-013 | Queue infrastructure deferred from Phase 1 | Premature queue orchestration adds distributed complexity, async debugging overhead, and eventual consistency risk before operational need is proven | Replaced with minimal background processing — queue introduced only when load metrics justify it | 2025-05-17 |
| ADR-014 | Draft Persistence added as pre-workflow layer separate from FSM | Users think non-linearly — punishing interrupted composition with data loss contradicts platform purpose. Draft state must not enter the FSM or trigger any analysis pipeline | Draft persistence is a separate lightweight layer. DRAFT is not a workflow_state. FSM begins at IDLE on explicit submission only | 2025-05-17 |
| ADR-015 | Multi-Idea Workspace Principle — one account supports many independent ideas | Users need to evaluate multiple ideas over time. A single-idea account model creates artificial constraints and forces destructive overwriting | Each idea_id is a fully isolated workspace with independent state, audit log, and lifecycle. No shared mutable state between ideas | 2025-05-17 |
