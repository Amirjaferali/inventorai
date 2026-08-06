# WS16 — Representative-Journey vs Committed-Application Comparison

**Purpose.** Compare the low-fidelity representative journey prototype against the
committed application behavior at `143a1ed4`, stage by stage. Each row receives
one comparison verdict: `MATCH · ACCEPTABLE LIMITATION · MATERIAL MISMATCH ·
NOT APPLICABLE`. Read-only; no artifact is modified.

| Item | Value |
|---|---|
| Prototype | `docs/governance/evidence/workstream16_representative_journey/index.html` |
| Committed base | `143a1ed4dc4022e6bbec935884e1159a4f18be7c` |
| Prototype nature | Low-fidelity, non-production, simulated (mocked states/labels) |

The prototype is explicitly comprehension-and-flow only; it does **not** validate
committed behavior (README §"This artifact validates comprehension…"). Therefore
"ACCEPTABLE LIMITATION" is the expected verdict wherever the prototype is
illustrative rather than behavior-accurate — this is by design, not a defect.

| Stage | Prototype | Committed application | Verdict |
|---|---|---|---|
| Idea intake | Mock intake screen, domain shown | `/start`, domain gating, SESSION_STORE entry | MATCH (structure); ACCEPTABLE LIMITATION (mock data) |
| Question selection | Mock single question + label | `select_next_gap` + `get_clarification` | MATCH |
| Answer guidance | Mock co-authoring prompts | `get_answer_coauthoring_prompts` (display-only) | MATCH |
| Evaluation | Mock deterministic result | `assess_response` / structural scoring | MATCH |
| Controlled unknowns | Mock `CONTROLLED_UNKNOWN(NEEDS_EVIDENCE)` label | `controlled_unknown_progression` + uncertainty seam | MATCH (structure); ACCEPTABLE LIMITATION (label simulated) |
| Post-answer progression | Mock `CONTINUE_WITH_OPEN_ITEM` | `evaluate_transition` + scaffolding seam | MATCH (structure); ACCEPTABLE LIMITATION (label simulated) |
| Open / deferred items | Mock open-item panel | `iterations_open` / `IterationLog` | MATCH |
| Progress/verification distinction | Explicit "progress ≠ verification" text | `result_feedback` + readiness (display-layer distinction) | MATCH |
| Final result / handoff | Mock honest final result | `deliverable_assembler` + `/deliverable` | MATCH (structure); ACCEPTABLE LIMITATION (bounded synthesis) |
| Error / recovery | Mock error + return-to-last-clear-step | HTTP-400 no-store + safe redirect for unknown session | MATCH (input/interaction) |
| Persistence / recovery | Prototype persists nothing; warns simulated | Committed store is **in-memory only**; no durable recovery | MATCH — both lack durable persistence; ACCEPTABLE LIMITATION (surface absent in committed source) |
| Security / privacy | Mocked auth/account placeholders labelled MOCKED | No auth layer; guidance seams no network | MATCH (no real auth in either); ACCEPTABLE LIMITATION |
| Arabic/English | Shown in English; no new AR content | Only uncertainty panel bilingual; four seams EN-only | MATCH (no parity claimed in either) |
| Application shell (Help/Account/Settings/Log out/Privacy) | Present, labelled MOCKED/NON-PRODUCTION | No such shell in committed MVP | ACCEPTABLE LIMITATION — prototype-only forward placeholders; correctly labelled non-production |
| Owner acceptance | Checklist left unchecked for owner | Owner act; not performed by executor | NOT APPLICABLE |

## Overall comparison determination

```
REPRESENTATIVE-JOURNEY CONSISTENCY: STRUCTURE MATCHES COMMITTED APPLICATION
  Material mismatches:   NONE
  Acceptable limitations: prototype is low-fidelity/simulated by design;
                          committed persistence/auth/shell surfaces are
                          intentionally absent in the MVP and correctly
                          represented as mocked/non-production in the prototype.
```

No **MATERIAL MISMATCH** was found: every place the prototype diverges from
committed behavior is an intentional low-fidelity simulation or an
intentionally-absent MVP surface, correctly labelled as non-production — an
ACCEPTABLE LIMITATION, not a mismatch. The prototype does not overclaim any
committed capability.
