"""Guided Uncertainty Support — deterministic, display-only supportive guidance.

DETERMINISTIC, DISPLAY-ONLY, CONTENT-FREE SUPPORTIVE GUIDANCE — WEB/DISPLAY LAYER.

Governed by
`docs/governance/GUIDED_UNCERTAINTY_SUPPORT_INCREMENT_CONTRACT.md` (true-merged
via PR #134) and its scope decision
`docs/governance/INVENTOR_SUPPORTIVE_GUIDANCE_NON_EXAM_UX_SCOPE_DECISION.md`
(PR #132). Realizes the merged principle that **InventorAI is a supportive
idea-development assistant, not an exam-like evaluator**.

When a user expresses uncertainty — e.g. "I don't know", "I'm not sure", "I don't
understand the question", or the Arabic equivalents "لا أعرف", "غير متأكد", "لا
أفهم السؤال" — this module returns short, supportive, OPTIONAL, content-free
prompts that help the inventor continue with what they DO know, without making
them feel tested, judged, or blocked. It helps the inventor DEVELOP THEIR OWN
idea; it does not author, rewrite, complete, grade, or replace the answer.

Strict boundaries (contract §5/§6/§8/§9/§10; scope decision §6/§8/§9):
  * Pure, deterministic, display-only. Computed at render time from the given
    text alone. No engine call, no AI/generative/LLM call, no network, no I/O, no
    persistence, no stored state, no hidden state, no imports of engine /
    scoring / persistence / Safety-Signals modules.
  * It NEVER reads, stores, rewrites, improves, corrects, completes, or mutates
    the inventor's answer; never closes a gap; never marks an uncertainty answer
    as sufficient; never advances maturity/readiness; never changes scoring or
    criticality; and never alters any PASS/WARN/BLOCK outcome.
  * It emits only bounded, supportive, content-free prompts. It NEVER supplies
    answer content, a component, a number, a material, a mechanism, a safety
    fact, or a domain detail, and never claims the answer/idea is correct,
    complete, feasible, safe, compliant, patent-ready, or engineering-ready.
  * This is NOT the Inventor Answer Clarification / Improve Wording Assistant: it
    introduces no `suggested_clarified_answer` / `user_approved_answer` /
    `original_user_answer` / `clarification_status` field or flow, and no
    equivalent; it adds no save/approve/apply control and no new session action.
  * The inventor remains the sole author and source of any saved answer.

Distinct from the existing display-only surfaces:
  * `web/answer_coauthoring_prompts.py` (Guided Answer Co-Authoring) offers
    "what you could include" prompts near a NORMAL question, keyed on gap_type.
  * This module responds to UNCERTAINTY ("I don't know" situations), keyed on the
    user's own expressed text — a distinct, complementary surface.
"""

# --- Supportive display payload (fixed, content-free) ----------------------
_HEADING = "That's okay — let's take it one step at a time."

# Supportive, optional, content-free prompts. None supplies answer content, a
# component, a value, a material, a mechanism, a safety fact, or a domain detail.
_PROMPTS = (
    "Start with what you already know — even a rough idea helps.",
    "Describe, in plain words, the result you want it to achieve.",
    "Tell us which part feels unclear, so we can take it slowly.",
    "What do you imagine happens first?",
    "You do not need technical terms yet — everyday words are fine.",
)

# Optional/authorship reminder. Truthful and non-exam-like: it negates
# validation/safety framing (contract §5/§6), never makes a positive claim.
_NOTE = (
    "This is optional guidance. You write your own answer in your own words — "
    "take your time. It is not validation, and it is not safety, compliance, "
    "patent, or engineering approval."
)

# --- Text normalization (pure; no imports) ---------------------------------
# Apostrophe variants stripped so "don't" == "dont".
_APOSTROPHES = ("'", "’", "´", "`", "ʼ")
# Arabic diacritics (harakat/tatweel/superscript alef) removed before matching.
_ARABIC_DIACRITICS = frozenset(
    [chr(c) for c in range(0x0610, 0x061B)]
    + [chr(c) for c in range(0x064B, 0x0660)]
    + [chr(0x0670), chr(0x0640)]
)
# Alef variants folded to bare alef so "أعرف" == "اعرف".
_ALEF_FOLD = {"أ": "ا", "إ": "ا",
              "آ": "ا", "ٱ": "ا"}


def _normalize(text):
    """Return a lowercased, apostrophe/diacritic-stripped, whitespace-collapsed
    form of ``text`` for deterministic cue matching. Pure; never raises."""
    if not isinstance(text, str):
        return ""
    t = text.strip().lower()
    for ch in _APOSTROPHES:
        t = t.replace(ch, "")
    folded = []
    for ch in t:
        if ch in _ARABIC_DIACRITICS:
            continue
        folded.append(_ALEF_FOLD.get(ch, ch))
    return " ".join("".join(folded).split())


# Curated, conservative uncertainty cues (normalized form). English cues cover
# the required examples and close variants; Arabic cues cover the required
# examples and common MSA equivalents.
_ENGLISH_CUES = (
    "dont know",            # I don't know / I don't know the term / how it works
    "do not know",
    "not sure",             # I'm not sure
    "dont understand",      # I don't understand the question
    "do not understand",
    "no idea",
    "unsure",
)
_ARABIC_CUES = (
    "لا اعرف",              # لا اعرف  (لا أعرف)
    "لا ادري",              # لا ادري
    "غير متاكد",  # غير متاكد (غير متأكد)
    "لست متاكد",  # لست متاكد
    "لا افهم",              # لا افهم  (لا أفهم)
)
_ALL_CUES = _ENGLISH_CUES + _ARABIC_CUES


def is_uncertainty_text(text):
    """Return True iff ``text`` expresses uncertainty (English or Arabic).

    Pure and deterministic. Matches a curated, conservative cue list against the
    normalized text. Never raises; performs no I/O; reads/mutates nothing else.
    """
    normalized = _normalize(text)
    if not normalized:
        return False
    return any(cue in normalized for cue in _ALL_CUES)


def get_uncertainty_guidance(text):
    """Return supportive, display-only guidance for uncertainty text, else None.

    Pure and deterministic. ``text`` is the user's own expressed answer/signal
    text (or None). Returns a fresh dict ``{heading, prompts, note}`` of
    supportive, content-free prompts when the text expresses uncertainty, or
    ``None`` otherwise. Never raises; performs no I/O; never reads, stores, or
    mutates any answer or state; never affects scoring, maturity, readiness,
    criticality, gaps, the transcript, or the IdeaState.
    """
    if not is_uncertainty_text(text):
        return None
    return {
        "heading": _HEADING,
        "prompts": list(_PROMPTS),
        "note": _NOTE,
    }
