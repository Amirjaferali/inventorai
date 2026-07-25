# WS13 No-Valid-RED — Seam Inventory

The five examined display-layer seams at authoritative base
`0598a05137912866bab49f67b0c82048b282f85d`. All are deterministic, display-only,
content-free; all wired in `web/app.py` (imports `:28–32`, rendered `:579–618`).

## 1. `web/answer_coauthoring_prompts.py`
- **Public entry point:** `get_answer_coauthoring_prompts(gap_type)` (`:109`).
- **Accepted inputs (OD-4):** `gap_type` (a committed gap id) or `None`; unknown/None → `_FALLBACK`.
- **Observable outputs:** fresh `{heading, prompts, note}`; `prompts` is a list of content-free strings naming KINDS of detail the inventor could add to their own answer.
- **Language coverage:** English-only.
- **web/app.py wiring:** imported `:30`; rendered `current_answer_coauthoring=get_answer_coauthoring_prompts(gap_type) if gap_type else None` (`:607`).
- **Current committed tests:** `tests/test_guided_answer_coauthoring_increment_1.py`.
- **Classification:** NOT A DEFECT (deterministic, side-effect-free, tested).

## 2. `web/scaffolding_guidance.py`
- **Public entry point:** `get_scaffolding_guidance(last_result, gap_type=None)` (`:196`).
- **Accepted inputs (OD-4):** already-computed `last_result` (WARN-class insufficiency) + current `gap_type`.
- **Observable outputs:** dict of neutral guidance naming the KIND of missing detail on WARN; `None` for non-WARN/empty results.
- **Language coverage:** English-only.
- **web/app.py wiring:** imported `:29`; rendered `current_scaffolding_guidance=get_scaffolding_guidance(last_result, gap_type)` (`:587`).
- **Current committed tests:** `tests/test_more_detail_needed_scaffolding.py`, `tests/test_layer1_feedback_wording.py`.
- **Classification:** NOT A DEFECT.

## 3. `web/uncertainty_guidance.py`
- **Public entry points:** `get_uncertainty_guidance(text)` (`:174`), `is_uncertainty_text(text)` (`:144`).
- **Accepted inputs (OD-4):** explicit user uncertainty text (EN or AR).
- **Observable outputs:** short, supportive, optional, content-free prompts; `is_uncertainty_text` returns a deterministic boolean.
- **Language coverage:** **Bilingual (EN + AR).**
- **web/app.py wiring:** imported `:31`; rendered `current_uncertainty_guidance=get_uncertainty_guidance(_uncertainty_text)` (`:618`).
- **Current committed tests:** `tests/test_guided_uncertainty_support.py`.
- **Classification:** NOT A DEFECT (EN/AR committed parity holds).

## 4. `web/clarification_labels.py`
- **Public entry point:** `get_clarification(gap_type)` (`:171`).
- **Accepted inputs (OD-4):** `gap_type` (or None → `_FALLBACK`).
- **Observable outputs:** fresh `{label, plain_language, information_needed, answer_shape, support_hint}` explaining the CURRENT question only.
- **Language coverage:** English-only.
- **web/app.py wiring:** imported `:28`; rendered `current_clarification=get_clarification(gap_type) if gap_type else None` (`:579`).
- **Current committed tests:** `tests/test_increment_1b_clarification_routing.py`, `tests/test_phase_8a_section4_clarification.py`.
- **Classification:** NOT A DEFECT.

## 5. `web/result_feedback.py`
- **Public entry point:** `get_result_feedback(last_result)` (`:86`).
- **Accepted inputs (OD-4):** already-computed session `last_result` (transition + raw reason).
- **Observable outputs:** short, supportive plain-language explanation for the primary feedback line; the raw authoritative reason is preserved unchanged by the caller.
- **Language coverage:** English-only.
- **web/app.py wiring:** imported `:32`; rendered `current_result_feedback=get_result_feedback(last_result)` (`:596`).
- **Current committed tests:** `tests/test_plain_language_result_feedback.py`, `tests/test_advisory_panel_precedence.py`.
- **Classification:** NOT A DEFECT.

## Language-coverage summary
- Bilingual (EN + AR): `uncertainty_guidance.py` — parity holds.
- English-only: `answer_coauthoring_prompts.py`, `scaffolding_guidance.py`,
  `clarification_labels.py`, `result_feedback.py` — **OUTSIDE WS13 v1 — RECORDED
  LOCALIZATION GAP** (WS13-CD-1); not a WS13 defect.
