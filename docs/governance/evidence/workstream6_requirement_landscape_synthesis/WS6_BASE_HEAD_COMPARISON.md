# WS6 Evidence — BASE vs HEAD Behavior Comparison

Machine summaries: ws6_repetition_counts_base.json /
ws6_repetition_counts_head.json (same harness, same byte-identical inputs).

| Aspect (canonical WS1 journey) | BASE 721b4613 | HEAD 4f89d1ae |
|---|---|---|
| Section 13 JSON rows | 13 | 13 (unchanged) |
| JSON rows with the byte-identical core statement | 8 | 8 (unchanged) |
| Requirement IDs | req:assertion:rec_1..rec_13 | identical |
| HTML standalone renderings of the core statement | 8 | 1 |
| Owner repetition sentence | absent | exactly once: "This statement was recorded 8 times during the session." |
| Non-byte-identical statements rendered | each once | each once (unchanged) |
| _session_meta.requirement_landscape_synthesis | absent | present (6 groups; 1 repeated) |
| unknown record provenance/status/action | Recorded answer / Recorded from your answers (not yet verified) / Validate the recorded answer against the available evidence. | Recorded unknown / You indicated that this is not known yet. / This item remains unresolved. It may later be addressed through additional information, evidence, or specialist input. |
| deferred record | legacy Recorded answer vocabulary | Deferred decision / You chose to defer this item. / This item remains unresolved and can be revisited when you are ready to decide. |
| provisional_assumption record | legacy Recorded answer vocabulary | Provisional assumption / This assumption was recorded as a temporary direction and has not been validated. / Validate, revise, or replace it before relying on it. |
| empty-content placeholder statement | Recorded answer awaiting restatement. | Insufficient information was recorded to organize this item reliably.\nThis does not indicate that the idea is invalid; the item remains unresolved. |
| answered records | legacy vocabulary | byte-identical legacy vocabulary (unchanged) |
| Section 13-14 tie (step+blocked == total) | holds | holds |

No hidden expansion: no semantic synthesis, no Workstream 7 logic, no
referral/capability wording, no persistence/transcript change, no AI Coach,
no Answer Clarification (engine/validation_plan.py, engine/idea_state.py,
engine/progression_loop.py, engine/safety_signal.py, web/app.py,
web/templates/session.html: zero diff BASE..HEAD).
