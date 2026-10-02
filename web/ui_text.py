"""D-P6-18 — Global UI Language: the single central UI-string selection seam.

Gate G-DP6-18-GLOBAL-UI-LANGUAGE-IMPLEMENTATION-01.

Purpose
  The ONE presentation-only catalogue that maps a stable UI-string key to its
  English / Arabic variant, plus the tiny helpers that resolve the selected UI
  language. It is consumed by ``web/app.py`` (context processor + ``t`` template
  global) so every in-scope UI surface renders ONE language at a time.

Input contract
  * ``text(key, lang)`` — ``key`` is a stable catalogue key; ``lang`` is any value
    (normalised to ``"en"`` / ``"ar"``). Never raises: an unknown key or missing
    variant falls back to English and finally to the key itself.
  * ``normalize(value)`` / ``direction(lang)`` — pure functions over ``ui_lang``.
  * ``localize_message(english, lang)`` — resolves a KNOWN server-side English
    message constant to the selected language; unknown text passes through.

Output contract
  A plain ``str`` (the selected-language UI string / direction token).

Prohibited behaviours (boundaries)
  * Presentation only — activates no domain, changes no deterministic evaluation,
    reads NO client free-text, and is NOT an authorization/ownership signal.
  * Canonical technical/system QUESTION text is NOT in this catalogue: D-P6-18 does
    not translate questions (the Question Translation Assistant is a separate,
    later gate). Category-C generated OUTPUT and Category-D question/guided-prompt
    copy are intentionally excluded and remain English, with ONE explicit,
    Owner-elected exception: the bounded Stage 18 / CAP-01 guidance-profile copy
    (the ``UI_CAP01_*`` keys below) is carried here in English AND Arabic. That
    exception is limited to the authorized CAP-01 advisory block. This file owns
    that block's COPY only; which domains have an authorized CAP-01 profile, and
    what parts a profile renders, belong to ``web/cap01_guidance.py`` — capability
    availability is not translation and does not live in the string catalogue. It does NOT widen
    the Category-C rule and authorizes no general generated-output translation, no
    Question Translation Assistant, no automatic/model translation, and no further
    deliverable localization.
  * No new dependency, no framework, no gettext/Babel.
"""

SUPPORTED_LANGS = ("en", "ar")
DEFAULT_LANG = "en"


def normalize(value):
    """Return a supported UI language token. Anything other than ``"ar"`` is
    treated as the English default (fail-safe, never raises)."""
    return "ar" if value == "ar" else "en"


def direction(lang):
    """LTR/RTL writing direction for a UI language."""
    return "rtl" if normalize(lang) == "ar" else "ltr"


def text(key, lang):
    """Resolve a catalogue key to the selected-language string.

    Fallback order: requested language -> English -> the key itself. Never raises,
    so it is safe on any template path."""
    entry = UI_STRINGS.get(key)
    if not isinstance(entry, dict):
        return key
    lang = normalize(lang)
    return entry.get(lang) or entry.get("en") or key


def has_string(key):
    """True when the catalogue carries copy for ``key`` in every supported language.

    The ONE read-only predicate other presentation modules use to ask whether copy
    exists, so a caller that owns STRUCTURE (which keys a thing renders) never has
    to reach into ``UI_STRINGS`` or hold text of its own. Never raises."""
    entry = UI_STRINGS.get(key)
    return (isinstance(entry, dict)
            and all(isinstance(entry.get(lang), str) and entry[lang].strip()
                    for lang in SUPPORTED_LANGS))


# Known server-side English message constants (web/app.py) -> catalogue key, so a
# message stored in English can be rendered in the selected UI language WITHOUT
# changing where/how it is stored (storage stays English; only display localises).
_MESSAGE_KEYS = {
    "Enter an answer, or choose one of the response options below.":
        "UI_B_SESSION_039",
    "That answer could not be saved just now. Please try again.":
        "UI_B_SESSION_040",
    # PVCG-R1: the durable-failure message for the five non-answer actions
    # (same mechanism as UI_B_SESSION_040; separate string so a deferred or
    # "I don't know" action is not misdescribed as an answer).
    "That response could not be saved just now. Please try again.":
        "UI_B_SESSION_049",
    ("Current working snapshot selected for this temporary session. It has not "
     "been permanently saved or approved."): "UI_B_DELIV_105",
    # CF-2 Arabic-localization remainder: the five /start-flow error-path
    # constants (web/app.py) previously bypassed this mechanism entirely and
    # always rendered in English. Registered here unchanged (storage stays
    # English; only display localises), matching the existing pattern above.
    ("InventorAI currently supports electronics and electrical ideas only. "
     "Please describe an electronics or electrical invention."):
        "UI_B_START_010",
    ("Please confirm that your idea is an electronics or electrical idea "
     "before starting."): "UI_B_START_011",
    ("InventorAI currently supports electronics and electrical ideas only. Your "
     "description does not yet clearly show the electrical mechanism. Try adding a "
     "simple phrase describing how it works electrically — for example that it uses "
     "a sensor, current, switch, circuit, power, plug, or microcontroller."):
        "UI_B_START_012",
    ("Your description did not clearly match one supported domain. Please choose "
     "the domain that best fits your idea, then confirm it."): "UI_B_START_013",
    ("This service is temporarily unavailable. Please try again in a moment."):
        "UI_B_START_014",
    # CF-2: the two success-criteria raw rejection messages (web/app.py
    # `_reject`) had the same bypass shape as the five /start messages above.
    ("A submitted experiment is not part of the current plan. "
     "No changes were saved."): "UI_B_SC_007",
    ("A criterion exceeds the 1000-character "
     "limit. No changes were saved."): "UI_B_SC_008",
    # Stage 19 / CAP-09 durable SuccessCriterion: the truthful outcome
    # messages of the durable criteria routes (web/app.py), registered the
    # same way. They are DISTINCT because the outcomes are distinct.
    # SLICE-02 / SLICE 3 / SLICE 4: the same outcomes, now naming all four
    # planning concepts the page saves, plus the per-concept limits.
    (
     "Success criteria, test hypotheses, test variables / conditions and "
     "measurement methods can only be kept for a saved project. This session "
     "is not saved as a project, so they cannot be saved here. Nothing was "
     "changed."): "UI_SC_ERR_NOT_SAVED_PROJECT",
    (
     "The current Prototype & Test Plan is not available from this saved "
     "project, so success criteria, test hypotheses, test variables / "
     "conditions and measurement methods cannot be shown or changed from "
     "this page. Nothing was changed."): "UI_SC_ERR_PLAN_UNAVAILABLE",
    (
     "Your saved success criteria, test hypotheses, test variables / "
     "conditions and measurement methods could not be read, so they cannot "
     "be shown or changed from this page. Nothing was changed."): "UI_SC_ERR_CRITERIA_UNAVAILABLE",
    (
     "Your success criteria, test hypotheses, test variables / conditions "
     "and measurement methods could not be saved just now. Nothing was "
     "changed."): "UI_SC_ERR_NOT_SAVED",
    (
     "Your success criteria, test hypotheses, test variables / conditions "
     "and measurement methods were saved to your project, but this page "
     "could not show them. Reload this page to see what your project holds."): "UI_SC_ERR_SAVED_NOT_SHOWN",
    (
     "We could not confirm whether your success criteria, test hypotheses, "
     "test variables / conditions and measurement methods were saved. Reload "
     "this page to see what your project currently holds before entering "
     "them again."): "UI_SC_ERR_OUTCOME_UNKNOWN",
    ("A measurement method exceeds the 1000-character limit. "
     "No changes were saved."): "UI_SC_ERR_METHOD_TOO_LONG",
    ("A test hypothesis exceeds the 1000-character limit. "
     "No changes were saved."): "UI_SC_ERR_HYPOTHESIS_TOO_LONG",
    ("A test variable / condition exceeds the 1000-character limit. No changes "
     "were saved."): "UI_SC_ERR_VARIABLE_TOO_LONG",
    # PVCG-R4-C §13 E-1: the correction path must be bilingual, so its three
    # server messages are registered here exactly like every other one.
    ("That correction could not be applied just now. "
     "Nothing was changed."): "UI_B_CORRECT_001",
    ("Select which of your earlier answers to withdraw, and enter the "
     "corrected answer."): "UI_B_CORRECT_002",
    ("Your earlier answer was withdrawn and kept in the project history. "
     "Everything shown has been recomputed from your remaining answers."):
        "UI_B_CORRECT_003",
    # NB-1: the post-durable replay-failure notice. Rendered through the
    # `_answer_error` slot, which `show_session` localises with
    # `localize_message`, so it is registered HERE — the map that path uses.
    ("Your correction was saved, but the page could not be updated just now. "
     "What you see below has not changed yet. The saved correction will be "
     "reflected whenever this project can be rebuilt successfully."):
        "UI_B_CORRECT_004",
    # W2-A decision-capture failure message (web/app.py) — same registration
    # pattern as every other server message (storage stays English).
    ("That decision entry could not be saved just now. "
     "Nothing was changed."): "UI_W2A_ERR_001",
    # T2-A Quantified Requirements Slice 1 (web/app.py): the two rejection
    # messages render through the `_answer_error` slot (localize_message), so
    # they are registered here; the ack renders through `_interaction_ack`
    # (localize_deep) and is registered in `_DEEP_AR` below.
    ("That quantity could not be saved just now. Nothing was changed."):
        "UI_T2A_ERR_NOT_SAVED",
    ("Choose what kind of value this is and enter it as short plain text for "
     "the selected item. Nothing was changed."): "UI_T2A_ERR_INVALID",
    # The three truthful outcome messages. They are DISTINCT because the three
    # durable outcomes are distinct: an established refusal that wrote nothing,
    # an outcome that could not be determined at all (which asserts neither a
    # write nor a rollback), and a quantity that IS saved but could not be
    # reattached for display. None of them is the answer-correction wording.
    ("The recorded values for this item changed while you were confirming, so "
     "that quantity was not saved. Nothing was changed. Review the values shown "
     "here and enter it again if you still want it."): "UI_T2A_ERR_CONFLICT",
    ("We could not confirm whether that quantity was saved. Reload this page to "
     "see the values your project currently holds before entering it again."):
        "UI_T2A_ERR_UNKNOWN",
    ("Your quantity was saved to your project, but it could not be shown here "
     "just now. Reload this page shortly to see it."): "UI_T2A_ERR_SAVED_NOT_SHOWN",
    # UQTR-01 Step 2B: the ONE high-level refusal for a stale, reused, swapped
    # or cross-context response form (web/app.py ANSWER_FORM_STALE_MESSAGE).
    ("This response form is no longer current, so nothing was saved. "
     "Please review the current question and respond there."):
        "UI_UQTR_FORM_STALE",
    # CAP-10 Slice 1 (web/app.py declare_conflict): its refusals render through
    # the `_answer_error` slot, so they are registered here.
    ("That conflict could not be saved just now. Nothing was changed."):
        "UI_CAP10_ERR_NOT_SAVED",
    ("Choose exactly two of your current recorded answers and confirm that you "
     "believe they conflict. Nothing was changed."): "UI_CAP10_ERR_INVALID",
    ("One of those answers is no longer current, or that conflict is already "
     "recorded, so nothing was saved. Review your current answers and try "
     "again."): "UI_CAP10_ERR_STALE",
    ("We could not confirm whether that conflict was saved. Reload this page "
     "to see what your project holds before recording it again."):
        "UI_CAP10_ERR_UNKNOWN",
    # CAP-08 Slice 1 (web/app.py declare_dependency): its refusals render
    # through the `_answer_error` slot, so they are registered here.
    # Stage 20 closure (web/app.py assumption_action): refusals render through
    # the `_answer_error` slot, so they are registered here.
    'That change to your assumption could not be saved just now. Nothing was changed.':
        'UI_S20_ERR_NOT_SAVED',
    'Enter your revised assumption or your answer. Nothing was changed.':
        'UI_S20_ERR_INVALID',
    'That assumption is no longer current, or this page no longer matches what your project holds, so nothing was saved. Review your current assumptions and try again.':
        'UI_S20_ERR_STALE',
    'This assumption is your note on a question that is waiting for specialist or evidence input, so it cannot be replaced by your own answer. You can still revise it. Nothing was changed.':
        'UI_S20_ERR_ROUTED',
    'We could not confirm whether that change was saved. Reload this page to see what your project holds before trying again.':
        'UI_S20_ERR_UNKNOWN',
    'Your revised assumption was saved to your project, but this page could not show it just now. Reload this page to see what your project holds.':
        'UI_S20_ERR_REVISION_NOT_SHOWN',
    'Your replacement was saved, but it could not be applied to this page just now. What you see below has not changed yet. The saved replacement will be reflected whenever this project can be rebuilt successfully.':
        'UI_S20_ERR_REPLACEMENT_NOT_APPLIED',
    ("That dependency could not be saved just now. Nothing was changed."):
        "UI_CAP08_ERR_NOT_SAVED",
    ("Choose one of your provisional assumptions and at least one of your "
     "current recorded answers, and tick the declaration box. Nothing was "
     "changed."): "UI_CAP08_ERR_INVALID",
    ("One of those records is no longer current, or that dependency is already "
     "recorded, so nothing was saved. Review your current records and try "
     "again."): "UI_CAP08_ERR_STALE",
    ("We could not tell whether that dependency was saved. Reload this page "
     "to see what your project holds before recording it again."):
        "UI_CAP08_ERR_UNKNOWN",
    # Stage 15 Slice 2 (web/app.py declare_interface): its refusals render
    # through the `_answer_error` slot, so they are registered here.
    ("That interaction could not be saved just now. Nothing was changed."):
        "UI_S15_IFC_ERR_NOT_SAVED",
    ("Describe the interaction in your own words and tick the declaration "
     "box. Nothing was changed."): "UI_S15_IFC_ERR_INVALID",
    ("An interaction description can be at most 300 characters. Nothing was "
     "changed - please shorten it and submit again."): "UI_S15_IFC_ERR_TOO_LONG",
    ("The interaction description contains an invalid character. Nothing was "
     "changed - please remove it and submit again."): "UI_S15_IFC_ERR_INVALID_CHAR",
    ("This form is no longer current, so nothing was saved. Review the page "
     "and record the interaction again."): "UI_S15_IFC_ERR_STALE",
    ("We could not confirm whether that interaction was saved. It is not "
     "shown as saved until that can be confirmed. Submitting it again from "
     "here is safe: it will never be recorded twice."):
        "UI_S15_IFC_ERR_UNKNOWN",
    # Stage 15 Slice 3 (web/app.py save_interface_preparation): its outcomes
    # render through the page's error / notice slots, so they are registered.
    ("Verification-preparation inputs can only be kept for a saved project. "
     "This session is not saved as a project, so nothing can be saved here. "
     "Nothing was changed."): "UI_S15_PREP_MSG_NO_PROJECT",
    ("Your saved interactions and their preparation could not be read, so "
     "they cannot be shown or changed from this page. Nothing was changed."):
        "UI_S15_PREP_MSG_UNAVAILABLE",
    ("A submitted interaction is not part of this project. No changes were "
     "saved."): "UI_S15_PREP_MSG_UNKNOWN_INTERFACE",
    ("A preparation input exceeds the 1000-character limit. No changes were "
     "saved."): "UI_S15_PREP_MSG_TOO_LONG",
    ("Your preparation could not be saved just now. Nothing was changed."):
        "UI_S15_PREP_MSG_NOT_SAVED",
    ("Your preparation was saved to your project. It has not been checked, "
     "and saving it does not verify the interaction."): "UI_S15_PREP_MSG_SAVED",
    ("Your project already holds exactly these inputs, so nothing needed to "
     "change."): "UI_S15_PREP_MSG_UNCHANGED",
    ("Your preparation was saved to your project, but this page could not "
     "show it. Reload this page to see what your project holds."):
        "UI_S15_PREP_MSG_SAVED_NOT_SHOWN",
    # CAP-09 Result Event Slice 1 (web/app.py record_experiment_result).
    ("Your result could not be saved just now. Nothing was changed."):
        "UI_R_MSG_NOT_SAVED",
    ("Your result was recorded. It has not been checked by InventorAI and is "
     "not a pass/fail judgement."): "UI_R_MSG_SAVED",
    ("Describe what actually happened in your own words. Nothing was "
     "changed."): "UI_R_MSG_INVALID",
    ("A result can be at most 1000 characters. Nothing was changed."):
        "UI_R_MSG_TOO_LONG",
    ("That experiment is not part of the current plan, so no result can be "
     "recorded or corrected for it here. Nothing was changed."):
        "UI_R_MSG_NOT_CURRENT",
    ("That result has already been corrected, or it does not belong to this "
     "experiment, so nothing was saved. Review the page and try again."):
        "UI_R_MSG_STALE_TARGET",
    ("We could not confirm whether your result was saved. Reload this page to "
     "see what your project holds before entering it again."):
        "UI_R_MSG_UNKNOWN",
    ("We could not confirm whether your preparation was saved. Reload this "
     "page to see what your project currently holds before entering it "
     "again."): "UI_S15_PREP_MSG_UNKNOWN",
    # Stage 28 Optional Part Slice 2 (web/app.py save_part_answers).
    ("Answers about a part can only be kept for a saved project. This session "
     "is not saved as a project, so nothing can be saved here. Nothing was "
     "changed."): "UI_PQ_MSG_NO_PROJECT",
    ("Questions about an optional part are not offered for this project. "
     "Nothing was changed."): "UI_PQ_MSG_NOT_OFFERED",
    ("The questions for this part or your saved answers could not be read, so "
     "they cannot be shown or changed from this page. Nothing was changed."):
        "UI_PQ_MSG_UNAVAILABLE",
    ("A submitted answer does not belong to a current question about this "
     "part of this project. No changes were saved."):
        "UI_PQ_MSG_UNKNOWN_QUESTION",
    ("An answer exceeds the 1000-character limit. No changes were saved."):
        "UI_PQ_MSG_TOO_LONG",
    ("Your answers could not be saved just now. Nothing was changed."):
        "UI_PQ_MSG_NOT_SAVED",
    ("Your answers were saved to your project. They have not been checked, and "
     "saving them changes no gap, analysis focus, progression or readiness."):
        "UI_PQ_MSG_SAVED",
    ("Your project already holds exactly these answers, so nothing needed to "
     "change."): "UI_PQ_MSG_UNCHANGED",
    ("Your answers were saved to your project, but this page could not show "
     "them. Reload this page to see what your project holds."):
        "UI_PQ_MSG_SAVED_NOT_SHOWN",
    ("We could not confirm whether your answers were saved. Reload this page "
     "to see what your project currently holds before entering them again."):
        "UI_PQ_MSG_UNKNOWN",
    # Stage 30 Slice 1 (web/app.py save_part_answers, read-only part page).
    ("Recording, editing or clearing answers about this part is not available "
     "now. Your saved answers are shown below, unchanged. Nothing was changed."):
        "UI_PQ_MSG_READ_ONLY",
    # Stage 15 Slice 4 (web/app.py record_interface_observation).
    ("Your observation could not be saved just now. Nothing was changed."):
        "UI_S15_OBS_MSG_NOT_SAVED",
    ("Your observation was saved to your project. It has not been checked or "
     "validated by InventorAI, and InventorAI does not decide whether the "
     "acceptance criterion was met."): "UI_S15_OBS_MSG_SAVED",
    ("Describe in your own words what actually happened when you checked this "
     "interaction. Nothing was changed."): "UI_S15_OBS_MSG_INVALID",
    ("An observation can be at most 1000 characters. Nothing was changed."):
        "UI_S15_OBS_MSG_TOO_LONG",
    ("That interaction is not part of this project, so no observation can be "
     "recorded or corrected for it here. Nothing was changed."):
        "UI_S15_OBS_MSG_NOT_CURRENT",
    ("That observation has already been corrected, or this page no longer "
     "matches what your project holds, so nothing was saved. Review the page "
     "and try again."): "UI_S15_OBS_MSG_STALE",
    ("This project already holds the maximum of 200 recorded observations, so "
     "no new one can be added. Nothing was changed and no earlier entry was "
     "removed."): "UI_S15_OBS_MSG_CAP",
    ("We could not confirm whether your observation was saved. Reload this "
     "page to see what your project holds before entering it again."):
        "UI_S15_OBS_MSG_UNKNOWN",
    # Stage 15 closure (web/app.py: the dependency on save_interface_preparation
    # and record_integration_evidence).
    ("A dependency must name the two parts of that interaction, or both. No "
     "changes were saved."): "UI_S15_DEP_MSG_INVALID",
    ("A dependency explanation can be at most 300 characters. No changes were "
     "saved."): "UI_S15_DEP_MSG_TOO_LONG",
    ("An explanation can only accompany a declared dependency. Choose who "
     "relies on whom, or clear the explanation. No changes were saved."):
        "UI_S15_DEP_MSG_NOTE_ALONE",
    ("Your integration evidence was saved to your project. It is your own "
     "statement: InventorAI has not checked it, and it does not show that the "
     "parts are compatible."): "UI_S15_IEV_MSG_SAVED",
    ("Your correction was saved as a new entry; the earlier entry stays in the "
     "history. InventorAI has not checked it."): "UI_S15_IEV_MSG_CORRECTED",
    ("That evidence item was withdrawn. It stays in the history and no longer "
     "counts as current evidence."): "UI_S15_IEV_MSG_WITHDRAWN",
    ("Your integration evidence could not be saved just now. Nothing was "
     "changed."): "UI_S15_IEV_MSG_NOT_SAVED",
    ("Some of the text could not be accepted. Fill in every required field "
     "within its length limit. Nothing was changed."):
        "UI_S15_IEV_MSG_TEXT_REJECTED",
    ("That interaction is not part of this project, so no evidence can be "
     "recorded for it here. Nothing was changed."): "UI_S15_IEV_MSG_NOT_CURRENT",
    ("That evidence item has already been corrected or withdrawn, or this page "
     "no longer matches what your project holds, so nothing was saved. Review "
     "the page and try again."): "UI_S15_IEV_MSG_STALE",
    ("This project already holds the maximum number of evidence items, so no "
     "new one can be added. Nothing was changed."): "UI_S15_IEV_MSG_CAP",
    ("We could not confirm whether your integration evidence was saved. Reload "
     "this page to see what your project holds before entering it again."):
        "UI_S15_IEV_MSG_UNKNOWN",
}


def localize_message(english, lang):
    """Return the selected-language variant of a KNOWN English server message.
    Unknown/None text passes through unchanged (fail-open, never raises)."""
    if not isinstance(english, str):
        return english
    key = _MESSAGE_KEYS.get(english)
    return text(key, lang) if key else english


# ---------------------------------------------------------------------------
# RVR-7 — substantive Path-N asks that have NO committed ``question_id``
# (authoritative implementation path manifest freeze, PR #588).
#
# The 21 committed Path-N questions carry their Arabic surface inside their own
# committed record (`ServedQuestion.text_ar`). The remaining substantive asks of
# the SAME journey have no record to carry it, so they are keyed here by an
# EXPLICIT SEMANTIC IDENTITY resolved at the render edge from canonical state.
#
# Identity-keyed, never text-keyed: an edit to an English engine constant can
# therefore never silently detach its Arabic surface the way a text-lookup would.
# This is a presentation catalogue for identities the engine already owns — it is
# NOT a second question registry: no identity is minted here, English content and
# question identity stay in their existing owners, and nothing here is consulted
# by progression.
#
# Scope is exactly the Owner-decided D-RVR7-1 Option A (Journey-Complete) set
# minus the committed-record questions: the two governed exhaustion/reframe
# prompts, the intake ask, the maturity-2 closing ask, and the REACHABLE Stage-3
# generic asks. The Stage-2 generic variants are deliberately ABSENT — they are
# unreachable in both activated domains and are owned by the future-domain
# activation obligation, not by RVR-7.
# ---------------------------------------------------------------------------

RVR7_STALL_REFRAME = "_STALL_REFRAME"
RVR7_EXHAUSTED_EXIT_PROMPT = "_EXHAUSTED_EXIT_PROMPT"
RVR7_INTAKE_QUESTION = "INTAKE_QUESTION"
RVR7_CLOSING_Q = "_CLOSING_Q"


def rvr7_generic_identity(gap_type, index):
    """The explicit semantic identity of a generic (non-artifact) substantive ask.

    Derived from canonical state — the served gap type and the deterministic
    variant index — never from the displayed text."""
    return f"GENERIC:{gap_type}:{index}"


RVR7_SUBSTANTIVE_AR = {
    RVR7_STALL_REFRAME: (
        "لنتناول هذا الجزء بعبارات أبسط. بكلماتك أنت، ما الذي تعرفه بالفعل عن هذا "
        "الجانب من فكرتك — وما المعلومات التي تظن أنك ستحتاجها، أو من يمكنه مساعدتك "
        "في إيجادها، لاستكمال الباقي؟ وإن لم تكن متأكدا، يمكنك أيضا استخدام الخيارات "
        "أدناه لتحديده كغير معروف، أو تأجيله، أو تسجيل افتراض مبدئي، أو طلب مختص أو دليل."
    ),
    # UQTR-01 truth fix, paired with the English engine constant: no promise
    # of the accept-as-known-risk exit, which exists only where offered.
    RVR7_EXHAUSTED_EXIT_PROMPT: (
        "لقد استُنفدت الأسئلة المعدّة لهذا الجانب، ولن يساعد تكرارها على إحراز مزيد من "
        "التقدم. الخيارات المتاحة لك الآن: أضف معلومات جديدة فعلًا في خانة الإجابة؛ أو "
        "حدّد هذه النقطة على أنها غير معروفة أو مؤجلة؛ أو سجّل افتراضًا مبدئيًا؛ أو "
        "اطلب رأي مختص أو دليلًا. ولا يمكن قبول هذا الجانب كمخاطرة معروفة إلا إذا ظهر "
        "هذا الخيار في الصفحة."
    ),
    RVR7_INTAKE_QUESTION: (
        "صِف اختراعك بمزيد من التفصيل — ما المشكلة المحددة التي يحلها، وكيف يحلها؟"
    ),
    RVR7_CLOSING_Q: (
        "بدأت آليتك تتضح. الآن اذكر بوضوح: ما الذي لا يقوم به اختراعك أو لا يغطيه؟ "
        "اذكر حدا واحدا على الأقل."
    ),
    # Stage-3 generic substantive asks — reachable on the success path once
    # maturity reaches 2 and the Stage-3 gap priority opens these gaps.
    "GENERIC:PROBLEM_MECHANISM_FIT:0": (
        "دون أن تصف كيف تعمل آليتك، صِف المشكلة التي تحاول حلها. ما الذي يحدث للشخص "
        "أو النظام الذي يعاني من هذه المشكلة، ولماذا تهمه؟"
    ),
    "GENERIC:PROBLEM_MECHANISM_FIT:1": (
        "لماذا تحل آليتك هذه المشكلة بدلا من نهج آخر؟ ما الذي في طريقة عمل آليتك "
        "يجعلها الأنسب لهذه المشكلة تحديدا؟"
    ),
    "GENERIC:PROBLEM_MECHANISM_FIT:2": (
        "هل هناك مواقف أو ظروف لن تحل فيها آليتك هذه المشكلة، أو ستحلها بشكل أقل "
        "جودة؟ ما هي تلك الظروف؟"
    ),
    "GENERIC:ASSUMPTION_INVENTORY:0": (
        "ما الأمور التي تعدّها مسلَّما بها بخصوص آليتك ولم تختبرها أو تتحقق منها بعد؟ "
        "قد تكون أمورا تتوقع أنها صحيحة، أو مواد تفترض أنها متوفرة، أو ظروفا تفترض "
        "أنها ستستمر."
    ),
    "GENERIC:ASSUMPTION_INVENTORY:1": (
        "بالنسبة لكل افتراض ذكرته، هل ستظل آليتك تعمل لو تبيّن أن ذلك الافتراض خاطئ؟ "
        "أي الافتراضات أساسية — أي تفشل الآلية بدونها — وأيها يتطلب منك فقط تعديل نهجك؟"
    ),
    "GENERIC:ASSUMPTION_INVENTORY:2": (
        "الآن بعد أن فكرت في افتراضاتك — هل هناك شيء تدرك أنك كنت تفترضه دون أن تعدّه "
        "افتراضا قبل هذه المحادثة؟ شيء بدا بديهيا لكنه في الواقع غير متحقق منه؟"
    ),
    "GENERIC:EXPERTISE_GAP_AWARENESS:0": (
        "ما مجالات المعرفة التقنية التي سيحتاجها شخص ما لبناء آليتك أو تنفيذها فعليا؟ "
        "اذكر مجالات الخبرة المطلوبة — لا ما تعرفه أنت، بل ما يتطلبه التنفيذ نفسه."
    ),
    "GENERIC:EXPERTISE_GAP_AWARENESS:1": (
        "من بين مجالات الخبرة التي حددتها للتو — أيها لديك معرفة عملية كافية بها "
        "للمضي قدما، وأيها يمثل فجوات حقيقية تحتاج فيها إلى التعلم أكثر أو الاستعانة "
        "بشخص آخر؟"
    ),
    "GENERIC:EXPERTISE_GAP_AWARENESS:2": (
        "بالنسبة لفجوات الخبرة التي حددتها — ماذا سيحدث لتنفيذك لو لم تُعالج تلك "
        "الفجوات قبل أن تبدأ البناء؟ ما المشكلات المحددة التي ستواجهها؟"
    ),
}


def rvr7_substantive_text(identity, english, lang):
    """Forward identity -> substantive display text for the selected language.

    ``identity`` is the semantic identity already resolved from canonical state;
    ``english`` is the canonical English text the engine decided on. Returns the
    committed Arabic variant when Arabic is selected and one is committed for that
    identity, otherwise the unchanged ``english``.

    Forward-only by construction: the identity is an input, never derived from
    ``english``. There is no text matching and no translation — a missing Arabic
    variant yields deterministic English, and it is the RVR-7 evidence gate that
    fails on absence, never the runtime."""
    if normalize(lang) != "ar" or not identity:
        return english
    variant = RVR7_SUBSTANTIVE_AR.get(identity)
    if isinstance(variant, str) and variant.strip():
        return variant
    return english


def localize_deep(value, lang):
    """Recursively localise KNOWN English UI-chrome strings inside a value.

    D-P6-18 final UI-chrome boundary: the deterministic guidance modules
    (clarification / scaffolding / co-authoring / result-feedback / responsibility
    / gap-label heading-guidance-stage_note) and the criticality/non-answer-ack
    constants keep ENGLISH as their source of truth; this helper maps their known
    English chrome to the selected language at the PRESENTATION boundary only.

    ``value`` may be a str / dict / list / tuple (the exact shapes those modules
    return). ONLY strings present in ``_DEEP_AR`` are translated — canonical
    questions, the criticality clarification ask, user content, tokens, and
    identifiers are NOT in the map and therefore pass through unchanged, so actual
    asks and user text are never translated. English selection returns the value
    unchanged (parity-preserving). Never raises."""
    if normalize(lang) == "en":
        return value
    if isinstance(value, str):
        return _DEEP_AR.get(value, value)
    if isinstance(value, dict):
        return {k: localize_deep(v, lang) for k, v in value.items()}
    if isinstance(value, tuple):
        return tuple(localize_deep(v, lang) for v in value)
    if isinstance(value, list):
        return [localize_deep(v, lang) for v in value]
    return value


# The catalogue. Keys are stable; every value is a fresh ``{"en", "ar"}`` pair.
# English is verbatim from the live templates/constants (parity-preserving);
# Arabic is the finalized, owner-approved copy (including the truth-corrected
# sensitive paragraphs). Category-C output and Category-D question/guided-prompt
# copy are deliberately absent, except for the ONE Owner-elected bounded exception
# recorded in the module docstring: the CAP-01 ``UI_CAP01_*`` keys.
UI_STRINGS = {
    # --- Stage 15 Slice 1 — Integrated Invention Entry & scope disclosure -----
    # Plain user-facing language only: no Domain Pack, D4, IRL, subsystem
    # architecture or classification wording. The Owner's own part text is
    # never in this catalogue (it is rendered verbatim, escaped).
    "UI_S15_OFFER_LABEL": {
        "en": "My invention includes mechanical and electrical/electronic parts that work together.",
        "ar": "يتضمن اختراعي أجزاءً ميكانيكية وأجزاءً كهربائية / إلكترونية تعمل معًا.",
    },
    "UI_S15_TITLE": {"en": "The parts of your invention", "ar": "أجزاء اختراعك"},
    "UI_S15_INTRO_TIE": {
        "en": "Your description mentions both mechanical and electrical / electronic aspects, so InventorAI needs one clarification before it starts.",
        "ar": "يذكر وصفك جوانب ميكانيكية وكهربائية / إلكترونية معًا، لذلك يحتاج InventorAI إلى توضيح واحد قبل البدء.",
    },
    "UI_S15_INTRO_DECLARED": {
        "en": "You said your invention includes mechanical and electrical / electronic parts that work together. Please confirm this before InventorAI starts.",
        "ar": "ذكرتَ أن اختراعك يتضمن أجزاءً ميكانيكية وأجزاءً كهربائية / إلكترونية تعمل معًا. يُرجى تأكيد ذلك قبل أن يبدأ InventorAI.",
    },
    "UI_S15_IDEA_LABEL": {"en": "Your description", "ar": "وصفك"},
    "UI_S15_QUESTION": {
        "en": "Does your invention contain mechanical and electrical/electronic parts that work together as parts of the same invention?",
        "ar": "هل يحتوي اختراعك على أجزاء ميكانيكية وأجزاء كهربائية / إلكترونية تعمل معًا بوصفها أجزاءً من الاختراع نفسه؟",
    },
    "UI_S15_YES": {"en": "Yes", "ar": "نعم"},
    "UI_S15_NO": {"en": "No", "ar": "لا"},
    "UI_S15_NOT_SURE": {"en": "Not sure", "ar": "لست متأكدًا"},
    "UI_S15_IF_YES": {
        "en": "If yes, describe each part briefly:",
        "ar": "إذا كانت إجابتك «نعم»، فصِف كل جزء باختصار:",
    },
    "UI_S15_MECH_LEGEND": {"en": "Mechanical part", "ar": "الجزء الميكانيكي"},
    "UI_S15_ELEC_LEGEND": {"en": "Electrical / electronic part", "ar": "الجزء الكهربائي / الإلكتروني"},
    "UI_S15_PART_NAME": {"en": "Short name (up to 80 characters)", "ar": "اسم مختصر (حتى 80 حرفًا)"},
    "UI_S15_PART_FUNCTION": {
        "en": "What it does in your invention (up to 300 characters)",
        "ar": "ما الذي يفعله في اختراعك (حتى 300 حرف)",
    },
    "UI_S15_FOCUS_PROMPT": {
        "en": "Which part should InventorAI examine first?",
        "ar": "أيّ جزء تريد أن يفحصه InventorAI أولًا؟",
    },
    "UI_S15_FOCUS_MECH": {"en": "The mechanical part", "ar": "الجزء الميكانيكي"},
    "UI_S15_FOCUS_ELEC": {"en": "The electrical / electronic part", "ar": "الجزء الكهربائي / الإلكتروني"},
    "UI_S15_FOCUS_NOTE": {
        "en": "InventorAI will examine your invention through this part first, and this choice cannot be changed later for this project. The other part is recorded, but it is not evaluated in this project yet.",
        "ar": "سيفحص InventorAI اختراعك من خلال هذا الجزء أولًا، ولا يمكن تغيير هذا الاختيار لاحقًا في هذا المشروع. يُسجَّل الجزء الآخر، لكنه لا يُقيَّم في هذا المشروع بعد.",
    },
    "UI_S15_NOTHING_SAVED": {
        "en": "Nothing is saved until you answer Yes and complete every field.",
        "ar": "لا يُحفظ أي شيء إلا بعد أن تجيب بـ«نعم» وتكمل جميع الحقول.",
    },
    "UI_S15_SUBMIT": {"en": "Continue", "ar": "متابعة"},
    "UI_S15_ERR_ANSWER": {
        "en": "Please choose Yes, No or Not sure. Nothing was saved.",
        "ar": "يُرجى اختيار «نعم» أو «لا» أو «لست متأكدًا». لم يُحفظ أي شيء.",
    },
    "UI_S15_ERR_FIELDS": {
        "en": "Please give a short name and a short description of what it does for both parts. Nothing was saved.",
        "ar": "يُرجى كتابة اسم مختصر ووصف مختصر لما يفعله كلٌّ من الجزأين. لم يُحفظ أي شيء.",
    },
    "UI_S15_ERR_TOO_LONG": {
        "en": "A part name can be at most 80 characters and a part description at most 300 characters. Nothing was saved - please shorten it and submit again.",
        "ar": "يمكن أن يصل اسم الجزء إلى 80 حرفًا على الأكثر، ووصفه إلى 300 حرف على الأكثر. لم يُحفظ أي شيء — يُرجى تقصير النص وإعادة الإرسال.",
    },
    "UI_S15_ERR_INVALID_CHAR": {
        "en": "A part field contains an invalid character. Nothing was saved - please remove it and submit again.",
        "ar": "يحتوي أحد حقول الأجزاء على رمز غير صالح. لم يُحفظ أي شيء — يُرجى إزالته وإعادة الإرسال.",
    },
    "UI_S15_ERR_FOCUS": {
        "en": "Please choose which part InventorAI should examine first. Nothing was saved.",
        "ar": "يُرجى اختيار الجزء الذي تريد أن يفحصه InventorAI أولًا. لم يُحفظ أي شيء.",
    },
    "UI_S15_GUIDE_NO": {
        "en": "Nothing was saved and no project was created. Please revise your description so it clearly states what your invention does and how it works, then submit it again.",
        "ar": "لم يُحفظ أي شيء ولم يُنشأ أي مشروع. يُرجى تعديل وصفك ليوضّح ما يفعله اختراعك وكيف يعمل، ثم أعد إرساله.",
    },
    "UI_S15_GUIDE_NOT_SURE": {
        "en": "Nothing was saved and no project was created. That is fine - please add a sentence describing the main parts of your invention and how they work together (for example, which part moves and which part uses electricity), then submit it again.",
        "ar": "لم يُحفظ أي شيء ولم يُنشأ أي مشروع. لا بأس بذلك — يُرجى إضافة جملة تصف الأجزاء الرئيسية لاختراعك وكيف تعمل معًا (مثلًا: أيّ جزء يتحرك وأيّ جزء يستخدم الكهرباء)، ثم أعد إرساله.",
    },
    "UI_S15_SCOPE_TITLE": {"en": "Integrated invention scope", "ar": "نطاق الاختراع المتكامل"},
    "UI_S15_SCOPE_MECH": {"en": "Mechanical part", "ar": "الجزء الميكانيكي"},
    "UI_S15_SCOPE_ELEC": {"en": "Electrical / electronic part", "ar": "الجزء الكهربائي / الإلكتروني"},
    "UI_S15_SCOPE_FUNCTION": {"en": "What it does:", "ar": "ما يفعله:"},
    "UI_S15_SCOPE_FOCUS": {"en": "Initial analysis focus", "ar": "محور التحليل الأولي"},
    "UI_S15_SCOPE_FOCUS_MECH": {"en": "Mechanical", "ar": "الميكانيكا"},
    "UI_S15_SCOPE_FOCUS_ELEC": {"en": "Electrical / Electronics", "ar": "الكهرباء / الإلكترونيات"},
    "UI_S15_SCOPE_STATEMENT": {
        "en": "This project records both parts as belonging to the same invention. InventorAI is currently evaluating the invention through the selected initial analysis focus. The other part and the integration between the parts have not yet been independently evaluated or validated.",
        "ar": "يسجّل هذا المشروع الجزأين بوصفهما جزأين من الاختراع نفسه. يقيّم InventorAI الاختراع حاليًا من خلال محور التحليل الأولي المختار. أما الجزء الآخر والتكامل بين الجزأين فلم يُقيَّما بعدُ ولم يُتحقَّق منهما بشكل مستقل.",
    },
    "UI_S15_SCOPE_PROVENANCE": {
        "en": "Both parts are recorded as you described them; they have not been checked or verified.",
        "ar": "سُجّل الجزآن كما وصفتهما، ولم يُفحصا ولم يُتحقَّق منهما.",
    },
    # --- Stage 28 — Control-Loop Optional Part — Slice 1 (dormant) ----------
    # Shown ONLY when the composition offers or holds the optional part slot
    # (no domain is part-eligible today, so none of these renders yet); every
    # two-part page keeps the keys above. Plain user-facing language only.
    "UI_S15_CTRL_LEGEND": {"en": "Control-loop part (optional)", "ar": "جزء حلقة التحكم (اختياري)"},
    "UI_S15_CTRL_NOTE": {
        "en": "Optional. If one part of your invention measures something, compares it with a target and acts on the result, you can describe that part here. Give both a short name and what it does, or leave both empty. It is recorded as you describe it; it cannot be the part examined first, and it is not evaluated in this project.",
        "ar": "اختياري. إذا كان أحد أجزاء اختراعك يقيس شيئًا ويقارنه بهدف ثم يتصرّف بناءً على النتيجة، فيمكنك وصف ذلك الجزء هنا. اكتب اسمًا مختصرًا وما يفعله معًا، أو اترك الحقلين فارغين. يُسجَّل كما تصفه؛ ولا يمكن أن يكون الجزء الذي يُفحص أولًا، ولا يُقيَّم في هذا المشروع.",
    },
    "UI_S15_ERR_OPTIONAL_FIELDS": {
        "en": "For the optional control-loop part, give both a short name and what it does, or leave both empty. Nothing was saved.",
        "ar": "بالنسبة إلى جزء حلقة التحكم الاختياري، اكتب اسمًا مختصرًا وما يفعله معًا، أو اترك الحقلين فارغين. لم يُحفظ أي شيء.",
    },
    "UI_S15_FOCUS_NOTE_OPTIONAL": {
        "en": "InventorAI will examine your invention through this part first, and this choice cannot be changed later for this project. The other parts are recorded, but they are not evaluated in this project yet.",
        "ar": "سيفحص InventorAI اختراعك من خلال هذا الجزء أولًا، ولا يمكن تغيير هذا الاختيار لاحقًا في هذا المشروع. تُسجَّل الأجزاء الأخرى، لكنها لا تُقيَّم في هذا المشروع بعد.",
    },
    "UI_S15_NOTHING_SAVED_OPTIONAL": {
        "en": "Nothing is saved until you answer Yes and complete every field for the mechanical and the electrical / electronic part.",
        "ar": "لا يُحفظ أي شيء إلا بعد أن تجيب بـ«نعم» وتكمل جميع حقول الجزء الميكانيكي والجزء الكهربائي / الإلكتروني.",
    },
    "UI_S15_SCOPE_CTRL": {"en": "Control-loop part", "ar": "جزء حلقة التحكم"},
    "UI_S15_SCOPE_STATEMENT_3": {
        "en": "This project records all three parts as belonging to the same invention. InventorAI is currently evaluating the invention through the selected initial analysis focus. The other parts and the integration between the parts have not yet been independently evaluated or validated.",
        "ar": "يسجّل هذا المشروع الأجزاء الثلاثة بوصفها أجزاءً من الاختراع نفسه. يقيّم InventorAI الاختراع حاليًا من خلال محور التحليل الأولي المختار. أما الأجزاء الأخرى والتكامل بين الأجزاء فلم تُقيَّم بعدُ ولم يُتحقَّق منها بشكل مستقل.",
    },
    "UI_S15_SCOPE_PROVENANCE_3": {
        "en": "All three parts are recorded as you described them; they have not been checked or verified.",
        "ar": "سُجّلت الأجزاء الثلاثة كما وصفتها، ولم تُفحص ولم يُتحقَّق منها.",
    },
    "UI_S15_IFC_TITLE_3": {"en": "How the parts interact", "ar": "كيف تتفاعل الأجزاء"},
    "UI_S15_IFC_NONE_3": {
        "en": "No interaction between the parts has been recorded yet.",
        "ar": "لم يُسجَّل أي تفاعل بين الأجزاء بعد.",
    },
    "UI_S15_IFC_FORM_SUMMARY_3": {
        "en": "Record how the parts interact",
        "ar": "سجّل كيف تتفاعل الأجزاء",
    },
    "UI_S15_IFC_INTRO_3": {
        "en": "Record, in your own words, how two parts of your invention are intended to interact — for example, what one part provides to, receives from or does to the other. For each interaction, InventorAI adds one preparation step to your Validation Plan. It does not check or assess the interaction.",
        "ar": "سجّل بكلماتك كيف يُفترض أن يتفاعل جزآن من أجزاء اختراعك — مثلًا: ما الذي يقدّمه أحد الجزأين للآخر، أو يستقبله منه، أو يُحدثه فيه. ولكل تفاعل يضيف InventorAI خطوة تحضير واحدة إلى خطة التحقق (Validation Plan). ولا يفحص InventorAI التفاعل ولا يقيّمه.",
    },
    "UI_S15_IFC_PAIR_LEGEND": {
        "en": "Which two parts does this interaction join?",
        "ar": "ما الجزآن اللذان يربط بينهما هذا التفاعل؟",
    },
    "UI_S15_IFC_FIELD_3": {
        "en": "Describe one interaction between the two chosen parts (up to 300 characters)",
        "ar": "صِف تفاعلًا واحدًا بين الجزأين المختارين (حتى 300 حرف)",
    },
    "UI_S15_IFC_CONFIRM_3": {
        "en": "This is my own description. I understand it is not checked, and that compatibility between the parts is not assessed.",
        "ar": "هذا وصفي الخاص. وأفهم أنه لا يُفحص، وأن التوافق بين الأجزاء لا يُقيَّم.",
    },
    "UI_S15_PREP_INTRO_3": {
        "en": "For each interaction you declared between two parts, you can record in your own words the intended operating conditions, an observable acceptance criterion and the evidence or review that will be needed. You can fill in one, two or all three, and change or clear them later. They are saved exactly as you write them and are not checked.",
        "ar": "لكل تفاعل أعلنته بين جزأين، يمكنك أن تسجّل بكلماتك ظروف التشغيل المقصودة، ومعيار قبول يمكن ملاحظته، وما سيلزم من أدلة أو مراجعة. يمكنك تعبئة حقل واحد أو اثنين أو الثلاثة، وتعديلها أو مسحها لاحقًا. تُحفظ كما تكتبها تمامًا، ولا تُفحص.",
    },
    "UI_S15_PREP_NO_INTERFACES_3": {
        "en": "No interaction between the parts has been recorded yet. Record an interaction on your project page first.",
        "ar": "لم يُسجَّل أي تفاعل بين الأجزاء بعد. سجّل تفاعلًا في صفحة مشروعك أولًا.",
    },
    "UI_S15_IEV_INTRO_3": {
        "en": "Evidence about how two parts work together through each interaction — for example a test, an inspection, a specification or a review. Each item is your own statement, tied to exactly one interaction. A correction or a withdrawal adds a new entry and keeps the earlier one in the history. Your observations above are not evidence and are not counted here.",
        "ar": "أدلة عن كيفية عمل جزأين معًا عبر كل تفاعل — مثل اختبار أو فحص أو مواصفة أو مراجعة. كل عنصر هو قولك أنت، ومرتبط بتفاعل واحد بالضبط. التصحيح أو السحب يضيف إدخالًا جديدًا ويُبقي السابق في السجلّ. ملاحظاتك أعلاه ليست أدلة ولا تُحتسب هنا.",
    },
    # --- Stage 28 Optional Part Slice 2 — questions about the control-loop part
    # (dormant). Plain user-facing copy only: the governed question text itself
    # is NOT in this catalogue (it is the pack text, verbatim, in its own
    # language — no canonical Arabic wording exists for it yet).
    "UI_PQ_TITLE": {"en": "Questions about the control-loop part",
                    "ar": "أسئلة عن جزء حلقة التحكم"},
    "UI_PQ_LINK": {"en": "Answer the questions about this part",
                   "ar": "أجب عن الأسئلة الخاصة بهذا الجزء"},
    "UI_PQ_INTRO": {
        "en": "These questions are about the control-loop part of your invention only. Answer in your own words; you can answer some now and the rest later, and change or clear an answer at any time. Your answers are saved exactly as you write them and are not checked.",
        "ar": "تتعلق هذه الأسئلة بجزء حلقة التحكم في اختراعك فقط. أجب بكلماتك؛ يمكنك الإجابة عن بعضها الآن والبقية لاحقًا، وتعديل أي إجابة أو مسحها في أي وقت. تُحفظ إجاباتك كما تكتبها تمامًا، ولا تُفحص.",
    },
    "UI_PQ_NOT_ROOT": {
        "en": "They do not apply to the project's initial analysis focus, which stays unchanged. Your answers do not close or change any gap of the project, and they do not change its progression, its readiness or its Integration evidence.",
        "ar": "ولا تنطبق على محور التحليل الأولي للمشروع، الذي يبقى دون تغيير. ولا تُغلق إجاباتك أي فجوة في المشروع ولا تغيّرها، ولا تغيّر تقدّمه ولا جاهزيته ولا أدلة التكامل (Integration evidence) الخاصة به.",
    },
    "UI_PQ_SOURCE_NOTE": {
        "en": "Each question is shown exactly as written in InventorAI's governed question set for this part.",
        "ar": "يُعرض كل سؤال كما ورد حرفيًا في مجموعة الأسئلة المعتمدة لهذا الجزء في InventorAI، وبلغته الأصلية الإنجليزية؛ إذ لا تتوفر بعدُ صياغة عربية معتمدة لهذه الأسئلة.",
    },
    "UI_PQ_PART": {"en": "Control-loop part:", "ar": "جزء حلقة التحكم:"},
    "UI_PQ_FAMILY_MECHANISM": {
        "en": "How the control loop works (mechanism completeness of this part)",
        "ar": "كيف تعمل حلقة التحكم (اكتمال آلية هذا الجزء — Mechanism Completeness)",
    },
    "UI_PQ_FAMILY_BOUNDARY": {
        "en": "What the control loop covers (boundary of this part)",
        "ar": "ما الذي تشمله حلقة التحكم (حدود هذا الجزء — Boundary Ambiguity)",
    },
    "UI_PQ_FAMILY_NONE": {"en": "None of these answers is recorded yet.",
                          "ar": "لم تُسجَّل أي إجابة من هذه الإجابات بعد."},
    "UI_PQ_FAMILY_SOME": {"en": "Some of these answers are recorded.",
                          "ar": "سُجّل بعض هذه الإجابات."},
    "UI_PQ_FAMILY_ALL": {"en": "All of these answers are recorded.",
                         "ar": "سُجّلت جميع هذه الإجابات."},
    "UI_PQ_RECORDED": {"en": "Answer recorded", "ar": "الإجابة مسجّلة"},
    "UI_PQ_NOT_RECORDED": {"en": "Not recorded yet", "ar": "لم تُسجَّل بعد"},
    "UI_PQ_PRESENCE_NOTE": {
        "en": "\"Recorded\" only means that an answer is saved. It does not mean the answer was checked, that anything is resolved, or that the part works.",
        "ar": "تعني «مسجّلة» فقط أن الإجابة محفوظة، ولا تعني أنها فُحصت، ولا أن شيئًا قد حُسم، ولا أن الجزء يعمل.",
    },
    "UI_PQ_LIMIT": {
        "en": "Each answer can be up to {limit} characters. Leave an answer empty to clear it.",
        "ar": "يمكن أن تصل كل إجابة إلى {limit} حرف. اترك الإجابة فارغة لمسحها.",
    },
    "UI_PQ_SAVE": {"en": "Save my answers", "ar": "احفظ إجاباتي"},
    "UI_PQ_BACK": {"en": "Back to your project", "ar": "العودة إلى مشروعك"},
    "UI_PQ_DRAFT_UNSAVED": {
        "en": "The text below was NOT saved. It is shown so you can correct it and submit again.",
        "ar": "لم يُحفظ النص أدناه. يُعرض لكي تتمكن من تصحيحه وإرساله مجددًا.",
    },
    "UI_PQ_STALE": {
        "en": "One or more answers you entered earlier belong to a question that is no longer asked for this part. They have been preserved but are not attached to any current question.",
        "ar": "تعود إجابة أو أكثر أدخلتها سابقًا إلى سؤال لم يعد يُطرح لهذا الجزء. وقد حُفظت، لكنها غير مرتبطة بأي سؤال حالي.",
    },
    "UI_PQ_MSG_NO_PROJECT": {
        "en": "Answers about a part can only be kept for a saved project. This session is not saved as a project, so nothing can be saved here. Nothing was changed.",
        "ar": "لا يمكن الاحتفاظ بالإجابات الخاصة بجزء إلا لمشروع محفوظ. هذه الجلسة غير محفوظة كمشروع، لذا لا يمكن حفظ أي شيء هنا. لم يتغيّر شيء.",
    },
    "UI_PQ_MSG_NOT_OFFERED": {
        "en": "Questions about an optional part are not offered for this project. Nothing was changed.",
        "ar": "لا تُعرض أسئلة عن جزء اختياري لهذا المشروع. لم يتغيّر شيء.",
    },
    "UI_PQ_MSG_UNAVAILABLE": {
        "en": "The questions for this part or your saved answers could not be read, so they cannot be shown or changed from this page. Nothing was changed.",
        "ar": "تعذّرت قراءة أسئلة هذا الجزء أو إجاباتك المحفوظة، لذا لا يمكن عرضها أو تغييرها من هذه الصفحة. لم يتغيّر شيء.",
    },
    "UI_PQ_MSG_UNKNOWN_QUESTION": {
        "en": "A submitted answer does not belong to a current question about this part of this project. No changes were saved.",
        "ar": "إحدى الإجابات المُرسلة لا تخص سؤالًا حاليًا عن هذا الجزء من هذا المشروع. لم يُحفظ أي تغيير.",
    },
    "UI_PQ_MSG_TOO_LONG": {
        "en": "An answer exceeds the 1000-character limit. No changes were saved.",
        "ar": "إحدى الإجابات تتجاوز حد 1000 حرف. لم يُحفظ أي تغيير.",
    },
    "UI_PQ_MSG_NOT_SAVED": {
        "en": "Your answers could not be saved just now. Nothing was changed.",
        "ar": "تعذّر حفظ إجاباتك الآن. لم يتغيّر شيء.",
    },
    "UI_PQ_MSG_SAVED": {
        "en": "Your answers were saved to your project. They have not been checked, and saving them changes no gap, analysis focus, progression or readiness.",
        "ar": "حُفظت إجاباتك في مشروعك. لم تُفحص، وحفظها لا يغيّر أي فجوة ولا محور التحليل ولا التقدّم ولا الجاهزية.",
    },
    "UI_PQ_MSG_UNCHANGED": {
        "en": "Your project already holds exactly these answers, so nothing needed to change.",
        "ar": "يحتوي مشروعك بالفعل على هذه الإجابات نفسها تمامًا، لذا لم يلزم أي تغيير.",
    },
    "UI_PQ_MSG_SAVED_NOT_SHOWN": {
        "en": "Your answers were saved to your project, but this page could not show them. Reload this page to see what your project holds.",
        "ar": "حُفظت إجاباتك في مشروعك، لكن هذه الصفحة تعذّر عليها عرضها. أعد تحميل الصفحة لترى ما يحتويه مشروعك.",
    },
    # --- Stage 30 — Control-Loop Part-Enablement Safeguards — Slice 1 --------
    # Read-only view of saved part answers, and the Safety Signal input scope.
    "UI_PQ_INTRO_READ_ONLY": {
        "en": "These are the answers you recorded about the control-loop part of your invention, shown exactly as you wrote them. They are your own statements and have not been checked.",
        "ar": "هذه هي الإجابات التي سجّلتها عن جزء حلقة التحكم في اختراعك، معروضةً كما كتبتها تمامًا. وهي أقوالك أنت ولم تُفحص.",
    },
    "UI_PQ_READ_ONLY": {
        "en": "Recording, editing or clearing answers about this part is not available now. Your saved answers are shown below, read-only; nothing has been removed.",
        "ar": "تسجيل الإجابات عن هذا الجزء أو تعديلها أو مسحها غير متاح حاليًا. تُعرض إجاباتك المحفوظة أدناه للقراءة فقط، ولم يُحذف منها شيء.",
    },
    "UI_PQ_LINK_READ_ONLY": {"en": "View your saved answers about this part",
                             "ar": "اعرض إجاباتك المحفوظة عن هذا الجزء"},
    "UI_PQ_SAFETY_SCOPE": {
        "en": "InventorAI does not read your answers about this part when it looks for inventor-stated safety signals. If no safety signal is shown, that does not mean this part has been reviewed for safety or is safe.",
        "ar": "لا يقرأ InventorAI إجاباتك عن هذا الجزء عند البحث عن إشارات السلامة كما ذكرها المخترِع. وإذا لم تظهر أي إشارة سلامة، فهذا لا يعني أن هذا الجزء قد رُوجع من حيث السلامة أو أنه آمن.",
    },
    "UI_PQ_MSG_READ_ONLY": {
        "en": "Recording, editing or clearing answers about this part is not available now. Your saved answers are shown below, unchanged. Nothing was changed.",
        "ar": "تسجيل الإجابات عن هذا الجزء أو تعديلها أو مسحها غير متاح حاليًا. تُعرض إجاباتك المحفوظة أدناه دون تغيير. لم يتغيّر شيء.",
    },
    # Report / PDF safety block: shown only when the project's composition holds
    # an optional part, beside the unchanged empty statement or signals.
    "UI_SS_OPTIONAL_PART_SCOPE": {
        "en": "These safety signals are derived only from your idea description and what you recorded in the main analysis (your answers and the unknowns you noted). Your answers about an optional part of the invention, such as a control-loop part, are not read for safety signals, so the absence of a signal says nothing about that part's safety.",
        "ar": "تُستخرج إشارات السلامة هذه فقط من وصف فكرتك ومما سجّلته في التحليل الرئيسي (إجاباتك والمجهولات التي دوّنتها). أما إجاباتك عن جزء اختياري من الاختراع، مثل جزء حلقة التحكم، فلا تُقرأ لاستخراج إشارات السلامة، ولذلك فإن عدم ظهور إشارة لا يدل على شيء بشأن سلامة ذلك الجزء.",
    },
    "UI_PQ_MSG_UNKNOWN": {
        "en": "We could not confirm whether your answers were saved. Reload this page to see what your project currently holds before entering them again.",
        "ar": "لم نتمكن من التأكد مما إذا كانت إجاباتك قد حُفظت. أعد تحميل الصفحة لترى ما يحتويه مشروعك حاليًا قبل إدخالها مجددًا.",
    },
    # --- Stage 15 Slice 2 — how the two parts interact (Owner declarations) --
    # Plain user-facing language only (same boundary as the Slice-1 keys).
    # The Owner's own interaction text is never in this catalogue (it is
    # rendered verbatim, escaped).
    "UI_S15_IFC_TITLE": {
        "en": "How the parts interact",
        "ar": "كيف يتفاعل الجزآن",
    },
    "UI_S15_IFC_INTRO": {
        "en": "Record, in your own words, how the two parts of your invention are intended to interact — for example, what one part provides to, receives from or does to the other. For each interaction, InventorAI adds one preparation step to your Validation Plan. It does not check or assess the interaction.",
        "ar": "سجّل بكلماتك كيف يُفترض أن يتفاعل جزآ اختراعك — مثلًا: ما الذي يقدّمه أحد الجزأين للآخر، أو يستقبله منه، أو يُحدثه فيه. ولكل تفاعل يضيف InventorAI خطوة تحضير واحدة إلى خطة التحقق (Validation Plan). ولا يفحص InventorAI التفاعل ولا يقيّمه.",
    },
    "UI_S15_IFC_NONE": {
        "en": "No interaction between the parts has been recorded yet.",
        "ar": "لم يُسجَّل أي تفاعل بين الجزأين بعد.",
    },
    "UI_S15_IFC_BETWEEN": {"en": "Between", "ar": "بين"},
    "UI_S15_IFC_AND": {"en": "and", "ar": "و"},
    "UI_S15_IFC_DESCRIPTION": {"en": "Your description:", "ar": "وصفك:"},
    "UI_S15_IFC_PROVENANCE": {
        "en": "Recorded as you described it; it has not been checked or validated.",
        "ar": "سُجّل كما وصفته، ولم يُفحص ولم يُتحقَّق منه.",
    },
    "UI_S15_IFC_ACTION_LABEL": {
        "en": "Verification preparation:",
        "ar": "التحضير للتحقق:",
    },
    "UI_S15_IFC_ACTION": {
        "en": "Establish how this declared interaction will be checked: define the intended operating conditions, an observable acceptance criterion, and what evidence or review will be needed.",
        "ar": "حدّد كيف سيُفحص هذا التفاعل المُعلَن: عرّف ظروف التشغيل المقصودة، ومعيار قبول يمكن ملاحظته، وما يلزم من أدلة أو مراجعة.",
    },
    "UI_S15_IFC_NOT_ESTABLISHED": {
        "en": "Engineering compatibility between the parts has NOT been established. Completing this preparation does not verify the interaction.",
        "ar": "لم يُثبَت التوافق الهندسي بين الجزأين. وإكمال هذا التحضير لا يعني التحقق من التفاعل.",
    },
    "UI_S15_IFC_FORM_SUMMARY": {
        "en": "Record how the parts interact",
        "ar": "سجّل كيف يتفاعل الجزآن",
    },
    "UI_S15_IFC_FIELD": {
        "en": "Describe one interaction between the two parts (up to 300 characters)",
        "ar": "صِف تفاعلًا واحدًا بين الجزأين (حتى 300 حرف)",
    },
    "UI_S15_IFC_CONFIRM": {
        "en": "This is my own description. I understand it is not checked, and that compatibility between the parts is not assessed.",
        "ar": "هذا وصفي الخاص. وأفهم أنه لا يُفحص، وأن التوافق بين الجزأين لا يُقيَّم.",
    },
    "UI_S15_IFC_BUTTON": {"en": "Record the interaction", "ar": "تسجيل التفاعل"},
    # Stage 15 Slice 3 — the inventor's verification-preparation inputs.
    # CAP-09 Result Event Slice 1.
    'UI_R_HEADING': {
        "en": 'What actually happened — your recorded results',
        "ar": 'ما الذي حدث فعلًا — النتائج التي سجّلتها',
    },
    'UI_R_INTRO': {
        "en": 'After you perform an experiment, record in your own words what actually happened. Each time you perform it again, record it as a new execution. Your results are kept as history: a correction adds a new entry and keeps the earlier ones. InventorAI does not check your results and does not judge them as a pass or a fail.',
        "ar": 'بعد أن تُجري تجربة، سجّل بكلماتك ما الذي حدث فعلًا. وفي كل مرة تُجريها من جديد، سجّلها كتنفيذ جديد. تُحفظ نتائجك كسجلّ: التصحيح يضيف إدخالًا جديدًا ويُبقي الإدخالات السابقة. لا يفحص InventorAI نتائجك ولا يحكم عليها بالنجاح أو الفشل.',
    },
    'UI_R_LABEL': {
        "en": 'Recorded by you; not checked by InventorAI and not a pass/fail judgement.',
        "ar": 'سجّلته أنت؛ لم يفحصه InventorAI، وليس حكمًا بالنجاح أو الفشل.',
    },
    'UI_R_EXECUTION': {
        "en": 'Execution',
        "ar": 'التنفيذ',
    },
    'UI_R_EARLIER': {
        "en": 'Earlier entries of this execution (kept as history)',
        "ar": 'إدخالات سابقة لهذا التنفيذ (محفوظة كسجلّ)',
    },
    'UI_R_CONTEXT': {
        "en": 'Context at recording',
        "ar": 'السياق عند التسجيل',
    },
    'UI_R_CONTEXT_NOTE': {
        "en": 'What this experiment carried when you first recorded this execution. It does not show that the test was performed with these values.',
        "ar": 'ما كانت تتضمنه هذه التجربة عندما سجّلت هذا التنفيذ أول مرة. ولا يُثبت أن الاختبار أُجري بهذه القيم.',
    },
    'UI_R_CONTEXT_EXPERIMENT': {
        "en": 'Experiment',
        "ar": 'التجربة',
    },
    'UI_R_CONTEXT_ABSENT': {
        "en": 'Not recorded at that time',
        "ar": 'لم يكن مُسجَّلًا في ذلك الوقت',
    },
    'UI_R_CORRECT': {
        "en": 'Correct this result',
        "ar": 'صحّح هذه النتيجة',
    },
    'UI_R_CORRECT_NOTE': {
        "en": 'A correction is added as a new entry; the earlier text stays in the history.',
        "ar": 'يُضاف التصحيح كإدخال جديد؛ ويبقى النص السابق في السجلّ.',
    },
    'UI_R_CORRECT_BUTTON': {
        "en": 'Save correction',
        "ar": 'حفظ التصحيح',
    },
    'UI_R_RECORD': {
        "en": 'Record what actually happened',
        "ar": 'سجّل ما الذي حدث فعلًا',
    },
    'UI_R_RECORD_NOTE': {
        "en": 'Up to 1000 characters. Recording a result does not mark the experiment as passed or failed.',
        "ar": 'حتى 1000 حرف. تسجيل نتيجة لا يعني أن التجربة نجحت أو فشلت.',
    },
    'UI_R_RECORD_BUTTON': {
        "en": 'Record result',
        "ar": 'تسجيل النتيجة',
    },
    'UI_R_STALE': {
        "en": 'Results you recorded for experiments that are no longer in the current plan are kept as history:',
        "ar": 'النتائج التي سجّلتها لتجارب لم تعد في الخطة الحالية محفوظة كسجلّ:',
    },
    'UI_R_UNAVAILABLE': {
        "en": 'Your recorded results could not be read, so they cannot be shown or changed from this page.',
        "ar": 'تعذّرت قراءة النتائج التي سجّلتها، لذا لا يمكن عرضها أو تغييرها من هذه الصفحة.',
    },
    # Stage 19 — Experiment Execution-State Disclosure — Closure: the Section-11
    # row LABEL only (interface chrome, like the sibling Section-11 field labels).
    # The execution-state wording and the Section-11 note are generated content
    # and stay English (web/app.py); they are not part of this catalogue.
    'UI_S11_EXECUTION_LABEL': {
        "en": 'Recorded executions:',
        "ar": 'التنفيذات المسجّلة:',
    },
    'UI_R_MSG_NOT_SAVED': {
        "en": 'Your result could not be saved just now. Nothing was changed.',
        "ar": 'تعذّر حفظ نتيجتك الآن. لم يتم تغيير أي شيء.',
    },
    'UI_R_MSG_SAVED': {
        "en": 'Your result was recorded. It has not been checked by InventorAI and is not a pass/fail judgement.',
        "ar": 'سُجّلت نتيجتك. لم يفحصها InventorAI، وليست حكمًا بالنجاح أو الفشل.',
    },
    'UI_R_MSG_INVALID': {
        "en": 'Describe what actually happened in your own words. Nothing was changed.',
        "ar": 'صِف بكلماتك ما الذي حدث فعلًا. لم يتم تغيير أي شيء.',
    },
    'UI_R_MSG_TOO_LONG': {
        "en": 'A result can be at most 1000 characters. Nothing was changed.',
        "ar": 'يمكن أن تكون النتيجة 1000 حرف كحدّ أقصى. لم يتم تغيير أي شيء.',
    },
    'UI_R_MSG_NOT_CURRENT': {
        "en": 'That experiment is not part of the current plan, so no result can be recorded or corrected for it here. Nothing was changed.',
        "ar": 'هذه التجربة ليست جزءًا من الخطة الحالية، لذا لا يمكن تسجيل نتيجة لها أو تصحيحها هنا. لم يتم تغيير أي شيء.',
    },
    'UI_R_MSG_STALE_TARGET': {
        "en": 'That result has already been corrected, or it does not belong to this experiment, so nothing was saved. Review the page and try again.',
        "ar": 'صُحّحت هذه النتيجة من قبل، أو أنها لا تخص هذه التجربة، لذا لم يُحفظ شيء. راجع الصفحة وحاول مرة أخرى.',
    },
    'UI_R_MSG_UNKNOWN': {
        "en": 'We could not confirm whether your result was saved. Reload this page to see what your project holds before entering it again.',
        "ar": 'تعذّر علينا التأكد مما إذا كانت نتيجتك قد حُفظت. أعد تحميل الصفحة لترى ما يحتفظ به مشروعك قبل إدخالها مرة أخرى.',
    },
    "UI_S15_PREP_TITLE": {
        "en": "Prepare how each interaction will be checked",
        "ar": "حضّر كيف سيُفحص كل تفاعل",
    },
    "UI_S15_PREP_INTRO": {
        "en": "For each interaction you declared between the two parts, you can record in your own words the intended operating conditions, an observable acceptance criterion and the evidence or review that will be needed. You can fill in one, two or all three, and change or clear them later. They are saved exactly as you write them and are not checked.",
        "ar": "لكل تفاعل أعلنته بين الجزأين، يمكنك أن تسجّل بكلماتك ظروف التشغيل المقصودة، ومعيار قبول يمكن ملاحظته، وما سيلزم من أدلة أو مراجعة. يمكنك تعبئة حقل واحد أو اثنين أو الثلاثة، وتعديلها أو مسحها لاحقًا. تُحفظ كما تكتبها تمامًا، ولا تُفحص.",
    },
    "UI_S15_PREP_CONDITIONS": {
        "en": "Intended operating conditions",
        "ar": "ظروف التشغيل المقصودة",
    },
    "UI_S15_PREP_ACCEPTANCE": {
        "en": "Observable acceptance criterion",
        "ar": "معيار قبول يمكن ملاحظته",
    },
    "UI_S15_PREP_EVIDENCE": {
        "en": "Evidence or review needed",
        "ar": "الأدلة أو المراجعة اللازمة",
    },
    "UI_S15_PREP_CONDITIONS_HINT": {
        "en": "Under which conditions is this interaction meant to work?",
        "ar": "في أي ظروف يُفترض أن يعمل هذا التفاعل؟",
    },
    "UI_S15_PREP_ACCEPTANCE_HINT": {
        "en": "What could someone observe that would show the interaction works as you intend?",
        "ar": "ما الذي يمكن ملاحظته ليُظهر أن التفاعل يعمل كما تقصد؟",
    },
    "UI_S15_PREP_EVIDENCE_HINT": {
        "en": "What evidence, or whose review, will be needed to check it?",
        "ar": "ما الأدلة، أو مراجعة مَن، التي ستلزم لفحصه؟",
    },
    "UI_S15_PREP_LIMIT": {
        "en": "Each field holds up to {limit} characters (a line break counts as two). Leave a field empty to clear it.",
        "ar": "يتسع كل حقل حتى {limit} حرف (يُحسب سطر جديد حرفين). اترك الحقل فارغًا لمسحه.",
    },
    "UI_S15_PREP_SAVE": {"en": "Save preparation", "ar": "حفظ التحضير"},
    "UI_S15_PREP_BACK": {"en": "Back to your project", "ar": "العودة إلى مشروعك"},
    "UI_S15_PREP_LINK": {
        "en": "Record or edit how each interaction will be checked, and record what happened when you checked it",
        "ar": "سجّل أو عدّل كيف سيُفحص كل تفاعل، وسجّل ما الذي حدث عندما فحصته",
    },
    "UI_S15_PREP_NOT_RECORDED": {"en": "Not recorded yet", "ar": "لم يُسجَّل بعد"},
    "UI_S15_PREP_NONE": {
        "en": "Preparation: none of the three inputs is recorded yet.",
        "ar": "التحضير: لم يُسجَّل أي من المُدخلات الثلاثة بعد.",
    },
    "UI_S15_PREP_PARTIAL": {
        "en": "Preparation: partly recorded; the inputs marked below as not recorded yet are still missing.",
        "ar": "التحضير: مُسجَّل جزئيًا؛ ما زالت المُدخلات المشار إليها أدناه بأنها لم تُسجَّل بعد ناقصة.",
    },
    "UI_S15_PREP_ALL": {
        "en": "Preparation: all three inputs are recorded. They have not been checked, and this does not verify the interaction.",
        "ar": "التحضير: المُدخلات الثلاثة مُسجَّلة. لم تُفحص، وهذا لا يعني التحقق من التفاعل.",
    },
    "UI_S15_PREP_OWNER_STATED": {
        "en": "Recorded by you as preparation; not checked, not a result.",
        "ar": "سجّلته أنت كتحضير؛ لم يُفحص، وليس نتيجة.",
    },
    "UI_S15_PREP_DRAFT_UNSAVED": {
        "en": "What you typed is shown below, but it has NOT been saved.",
        "ar": "ما كتبته معروض أدناه، لكنه لم يُحفظ.",
    },
    "UI_S15_PREP_NO_INTERFACES": {
        "en": "No interaction between the parts has been recorded yet. Record an interaction on your project page first.",
        "ar": "لم يُسجَّل أي تفاعل بين الجزأين بعد. سجّل تفاعلًا في صفحة مشروعك أولًا.",
    },
    "UI_S15_PREP_MSG_NO_PROJECT": {
        "en": "Verification-preparation inputs can only be kept for a saved project. This session is not saved as a project, so nothing can be saved here. Nothing was changed.",
        "ar": "لا يمكن الاحتفاظ بمُدخلات التحضير للتحقق إلا لمشروع محفوظ. هذه الجلسة غير محفوظة كمشروع، لذا لا يمكن حفظ شيء هنا. لم يتم تغيير أي شيء.",
    },
    "UI_S15_PREP_MSG_UNAVAILABLE": {
        "en": "Your saved interactions and their preparation could not be read, so they cannot be shown or changed from this page. Nothing was changed.",
        "ar": "تعذّرت قراءة تفاعلاتك المحفوظة وتحضيرها، لذا لا يمكن عرضها أو تغييرها من هذه الصفحة. لم يتم تغيير أي شيء.",
    },
    "UI_S15_PREP_MSG_UNKNOWN_INTERFACE": {
        "en": "A submitted interaction is not part of this project. No changes were saved.",
        "ar": "أحد التفاعلات المُرسلة ليس جزءًا من هذا المشروع. لم يُحفظ أي تغيير.",
    },
    "UI_S15_PREP_MSG_TOO_LONG": {
        "en": "A preparation input exceeds the 1000-character limit. No changes were saved.",
        "ar": "أحد مُدخلات التحضير يتجاوز حد 1000 حرف. لم يُحفظ أي تغيير.",
    },
    "UI_S15_PREP_MSG_NOT_SAVED": {
        "en": "Your preparation could not be saved just now. Nothing was changed.",
        "ar": "تعذّر حفظ تحضيرك الآن. لم يتم تغيير أي شيء.",
    },
    "UI_S15_PREP_MSG_SAVED": {
        "en": "Your preparation was saved to your project. It has not been checked, and saving it does not verify the interaction.",
        "ar": "حُفظ تحضيرك في مشروعك. لم يُفحص، وحفظه لا يعني التحقق من التفاعل.",
    },
    "UI_S15_PREP_MSG_UNCHANGED": {
        "en": "Your project already holds exactly these inputs, so nothing needed to change.",
        "ar": "مشروعك يحتفظ بهذه المُدخلات نفسها تمامًا، لذا لم يلزم أي تغيير.",
    },
    "UI_S15_PREP_MSG_SAVED_NOT_SHOWN": {
        "en": "Your preparation was saved to your project, but this page could not show it. Reload this page to see what your project holds.",
        "ar": "حُفظ تحضيرك في مشروعك، لكن تعذّر على هذه الصفحة عرضه. أعد تحميل الصفحة لترى ما يحتفظ به مشروعك.",
    },
    "UI_S15_PREP_MSG_UNKNOWN": {
        "en": "We could not confirm whether your preparation was saved. Reload this page to see what your project currently holds before entering it again.",
        "ar": "تعذّر علينا التأكد مما إذا كان تحضيرك قد حُفظ. أعد تحميل الصفحة لترى ما يحتفظ به مشروعك حاليًا قبل إدخاله مرة أخرى.",
    },
    # Stage 15 Slice 4 — the inventor's own observation of what actually
    # happened when they tested or checked a declared interaction.
    "UI_S15_OBS_HEADING": {
        "en": "What actually happened when you checked each interaction",
        "ar": "ما الذي حدث فعلًا عندما فحصت كل تفاعل",
    },
    "UI_S15_OBS_INTRO": {
        "en": "After you test or check an interaction, record in your own words what actually happened. Each time you check it again, record it as a new check. Your observations are kept as history: a correction adds a new entry and keeps the earlier ones.",
        "ar": "بعد أن تختبر تفاعلًا أو تفحصه، سجّل بكلماتك ما الذي حدث فعلًا. وفي كل مرة تفحصه من جديد، سجّله كفحص جديد. تُحفظ ملاحظاتك كسجلّ: التصحيح يضيف إدخالًا جديدًا ويُبقي الإدخالات السابقة.",
    },
    "UI_S15_OBS_SEPARATE": {
        "en": "Recording an observation is separate from the preparation above: it does not save, change or clear anything in the preparation fields. Use \"Save preparation\" for those.",
        "ar": "تسجيل ملاحظة منفصل عن التحضير أعلاه: فهو لا يحفظ أي شيء في حقول التحضير ولا يغيّره ولا يمسحه. استخدم «حفظ التحضير» لذلك.",
    },
    "UI_S15_OBS_LABEL": {
        "en": "Recorded by you; not checked or validated by InventorAI. InventorAI does not decide whether the acceptance criterion was met.",
        "ar": "سجّلته أنت؛ لم يفحصه InventorAI ولم يتحقق من صحته. ولا يقرّر InventorAI ما إذا كان معيار القبول قد استُوفي.",
    },
    "UI_S15_OBS_NONE": {
        "en": "No observation has been recorded for this interaction yet.",
        "ar": "لم تُسجَّل أي ملاحظة لهذا التفاعل بعد.",
    },
    "UI_S15_OBS_CHECK": {"en": "Check", "ar": "الفحص"},
    "UI_S15_OBS_EARLIER": {
        "en": "Earlier entries of this check (kept as history)",
        "ar": "إدخالات سابقة لهذا الفحص (محفوظة كسجلّ)",
    },
    "UI_S15_OBS_CONTEXT": {
        "en": "Preparation recorded at that time",
        "ar": "التحضير المُسجَّل في ذلك الوقت",
    },
    "UI_S15_OBS_CONTEXT_NOTE": {
        "en": "The preparation your project held when you first recorded this check: planning context at that time, not the current preparation above. It is not a claim about the conditions actually used in the check, and later changes to the preparation do not change it.",
        "ar": "التحضير الذي كان يحتفظ به مشروعك عندما سجّلت هذا الفحص أول مرة: سياق تخطيط في ذلك الوقت، وليس التحضير الحالي أعلاه. ولا يعني أن الفحص أُجري فعلًا في هذه الظروف، ولا تغيّره أي تعديلات لاحقة على التحضير.",
    },
    "UI_S15_OBS_CONTEXT_ABSENT": {
        "en": "Not recorded at that time",
        "ar": "لم يكن مُسجَّلًا في ذلك الوقت",
    },
    "UI_S15_OBS_CORRECT": {
        "en": "Correct this observation",
        "ar": "صحّح هذه الملاحظة",
    },
    "UI_S15_OBS_CORRECT_NOTE": {
        "en": "A correction is added as a new entry; the earlier text stays in the history. It is not checked or validated by InventorAI.",
        "ar": "يُضاف التصحيح كإدخال جديد؛ ويبقى النص السابق في السجلّ. ولا يفحصه InventorAI ولا يتحقق من صحته.",
    },
    "UI_S15_OBS_CORRECT_BUTTON": {"en": "Save correction", "ar": "حفظ التصحيح"},
    "UI_S15_OBS_RECORD": {
        "en": "Record what actually happened when you checked this interaction",
        "ar": "سجّل ما الذي حدث فعلًا عندما فحصت هذا التفاعل",
    },
    "UI_S15_OBS_RECORD_NOTE": {
        "en": "Up to {limit} characters (a line break counts as two). Your observation is kept exactly as you write it. It is not checked or validated by InventorAI, and InventorAI does not decide whether the acceptance criterion was met.",
        "ar": "حتى {limit} حرف (يُحسب سطر جديد حرفين). تُحفظ ملاحظتك كما تكتبها تمامًا. لا يفحصها InventorAI ولا يتحقق من صحتها، ولا يقرّر InventorAI ما إذا كان معيار القبول قد استُوفي.",
    },
    "UI_S15_OBS_RECORD_BUTTON": {"en": "Record observation", "ar": "تسجيل الملاحظة"},
    "UI_S15_OBS_UNAVAILABLE": {
        "en": "Your recorded observations could not be read, so they cannot be shown or added to from this page. Your preparation above is not affected.",
        "ar": "تعذّرت قراءة الملاحظات التي سجّلتها، لذا لا يمكن عرضها أو الإضافة إليها من هذه الصفحة. ولا يتأثر تحضيرك أعلاه.",
    },
    # Stage 15 closure — the per-interaction status view, the Owner-declared
    # dependency and Integration evidence. Factual presence only: no string
    # says compatible, integrated, verified or ready, and absence and
    # unavailability never read as a finding.
    "UI_S15_ST_HEADING": {
        "en": "Where each interaction stands",
        "ar": "أين يقف كل تفاعل",
    },
    "UI_S15_ST_INTRO": {
        "en": "A factual summary of what your project currently holds for each interaction you declared. It lists what has been recorded; it does not decide whether the parts work together.",
        "ar": "ملخّص وقائعي لما يحتفظ به مشروعك حاليًا عن كل تفاعل صرّحت به. يذكر ما سُجِّل فقط؛ ولا يقرّر ما إذا كان الجزآن يعملان معًا.",
    },
    "UI_S15_ST_DEPENDENCY": {"en": "Dependency", "ar": "الاعتماد"},
    "UI_S15_ST_CHECKS": {"en": "Your recorded checks", "ar": "الفحوص التي سجّلتها"},
    "UI_S15_ST_CHECKS_COUNT": {"en": "{count} recorded", "ar": "المُسجَّل: {count}"},
    "UI_S15_ST_CHECKS_NOT_EVIDENCE": {
        "en": "(your observations — not evidence, and not counted as evidence)",
        "ar": "(ملاحظاتك — ليست أدلة، ولا تُحتسب أدلة)",
    },
    "UI_S15_ST_EVIDENCE": {"en": "Current integration evidence", "ar": "أدلة التكامل الحالية"},
    "UI_S15_ST_EVIDENCE_COUNT": {
        "en": "{count} current item(s), each your own statement, not checked by InventorAI",
        "ar": "العناصر الحالية: {count}، وكل منها قولك أنت ولم يفحصه InventorAI",
    },
    "UI_S15_ST_EVIDENCE_HISTORY": {
        "en": "· {count} earlier or withdrawn entry(ies) kept as history",
        "ar": "· إدخالات سابقة أو مسحوبة محفوظة كسجلّ: {count}",
    },
    "UI_S15_ST_UNAVAILABLE": {
        "en": "Could not be read just now. This is not the same as nothing recorded.",
        "ar": "تعذّرت قراءته الآن. وهذا لا يعني أنه لم يُسجَّل شيء.",
    },
    "UI_S15_ST_NOT_A_VERDICT": {
        "en": "This shows only what has been recorded. It is not a compatibility or integration verdict: InventorAI has not established that these parts work together.",
        "ar": "يعرض هذا ما سُجِّل فقط. وليس حكمًا على التوافق أو التكامل: لم يُثبت InventorAI أن هذين الجزأين يعملان معًا.",
    },
    "UI_S15_PREP_FORM_HEADING": {
        "en": "Prepare each interaction",
        "ar": "حضّر كل تفاعل",
    },
    "UI_S15_DEP_LEGEND": {
        "en": "Does one part rely on the other through this interaction? (optional)",
        "ar": "هل يعتمد أحد الجزأين على الآخر عبر هذا التفاعل؟ (اختياري)",
    },
    "UI_S15_DEP_NOT_DECLARED": {"en": "Not declared", "ar": "لم يُصرَّح به"},
    "UI_S15_DEP_RELIES_ON": {"en": "relies on", "ar": "يعتمد على"},
    "UI_S15_DEP_MUTUAL": {
        "en": "Each part relies on the other",
        "ar": "كل جزء يعتمد على الآخر",
    },
    "UI_S15_DEP_NOTE": {
        "en": "Explain the dependency in your own words (optional)",
        "ar": "اشرح الاعتماد بكلماتك (اختياري)",
    },
    "UI_S15_DEP_GUIDANCE": {
        "en": "Up to {limit} characters. This records what you state about who relies on whom; InventorAI does not check it, and it does not show that the parts are compatible. It is saved, changed or cleared with \"Save preparation\".",
        "ar": "حتى {limit} حرف. يسجّل هذا ما تذكره عن أيّ الجزأين يعتمد على الآخر؛ لا يفحصه InventorAI، ولا يعني أن الجزأين متوافقان. يُحفظ أو يُغيَّر أو يُمسح بزر «حفظ التحضير».",
    },
    "UI_S15_IEV_HEADING": {
        "en": "Integration evidence you recorded",
        "ar": "أدلة التكامل التي سجّلتها",
    },
    "UI_S15_IEV_INTRO": {
        "en": "Evidence about how the two parts work together through each interaction — for example a test, an inspection, a specification or a review. Each item is your own statement, tied to exactly one interaction. A correction or a withdrawal adds a new entry and keeps the earlier one in the history. Your observations above are not evidence and are not counted here.",
        "ar": "أدلة عن كيفية عمل الجزأين معًا عبر كل تفاعل — مثل اختبار أو فحص أو مواصفة أو مراجعة. كل عنصر هو قولك أنت، ومرتبط بتفاعل واحد بالضبط. التصحيح أو السحب يضيف إدخالًا جديدًا ويُبقي السابق في السجلّ. ملاحظاتك أعلاه ليست أدلة ولا تُحتسب هنا.",
    },
    "UI_S15_IEV_UNAVAILABLE": {
        "en": "Your integration evidence could not be read, so it cannot be shown or added to from this page. Nothing else on this page is affected.",
        "ar": "تعذّرت قراءة أدلة التكامل التي سجّلتها، لذا لا يمكن عرضها أو الإضافة إليها من هذه الصفحة. ولا يتأثر أي شيء آخر في هذه الصفحة.",
    },
    "UI_S15_IEV_READONLY": {
        "en": "Only the owner of this project, signed in with a confirmed email address, can record, correct or withdraw integration evidence here.",
        "ar": "لا يمكن تسجيل أدلة التكامل أو تصحيحها أو سحبها هنا إلا لمالك هذا المشروع بعد تسجيل دخوله ببريد إلكتروني مؤكَّد.",
    },
    "UI_S15_IEV_NONE": {
        "en": "No integration evidence has been recorded for this interaction yet. That is a blank page, not a finding about whether the parts work together.",
        "ar": "لم تُسجَّل أي أدلة تكامل لهذا التفاعل بعد. هذه صفحة فارغة، وليست نتيجة بشأن ما إذا كان الجزآن يعملان معًا.",
    },
    "UI_S15_IEV_LABEL": {
        "en": "Your own statement; not checked by InventorAI. It does not show that the parts are compatible.",
        "ar": "قولك أنت؛ لم يفحصه InventorAI. ولا يعني أن الجزأين متوافقان.",
    },
    "UI_S15_IEV_CORRECT": {"en": "Correct this evidence item", "ar": "صحّح عنصر الأدلة هذا"},
    "UI_S15_IEV_CORRECT_NOTE": {
        "en": "A correction is added as a new entry for the same interaction; the earlier one stays in the history.",
        "ar": "يُضاف التصحيح كإدخال جديد للتفاعل نفسه؛ ويبقى الإدخال السابق في السجلّ.",
    },
    "UI_S15_IEV_CORRECT_BUTTON": {"en": "Save correction", "ar": "حفظ التصحيح"},
    "UI_S15_IEV_WITHDRAW_BUTTON": {"en": "Withdraw this item", "ar": "اسحب هذا العنصر"},
    "UI_S15_IEV_HISTORY": {
        "en": "{count} earlier or withdrawn entry(ies) are kept as history and are not counted as current evidence.",
        "ar": "إدخالات سابقة أو مسحوبة: {count}، محفوظة كسجلّ ولا تُحتسب أدلةً حالية.",
    },
    "UI_S15_IEV_RECORD": {
        "en": "Record evidence for this interaction — what kind of evidence is it?",
        "ar": "سجّل دليلًا لهذا التفاعل — ما نوع هذا الدليل؟",
    },
    "UI_S15_IEV_RECORD_NOTE": {
        "en": "Every field except the date is required, including what your evidence does not cover. It is kept exactly as you write it and is not checked by InventorAI.",
        "ar": "كل الحقول مطلوبة ما عدا التاريخ، بما فيها ما لا يغطّيه دليلك. يُحفظ كما تكتبه تمامًا ولا يفحصه InventorAI.",
    },
    "UI_S15_IEV_RECORD_BUTTON": {"en": "Record evidence", "ar": "تسجيل الدليل"},
    "UI_IEV_TOPIC_INTERFACE_TEST": {
        "en": "A test of this interaction", "ar": "اختبار لهذا التفاعل"},
    "UI_IEV_TOPIC_INTERFACE_INSPECTION": {
        "en": "An inspection or measurement", "ar": "فحص أو قياس"},
    "UI_IEV_TOPIC_INTERFACE_SPECIFICATION": {
        "en": "A specification or datasheet", "ar": "مواصفة أو ورقة بيانات"},
    "UI_IEV_TOPIC_INTERFACE_REVIEW": {
        "en": "A design or specialist review", "ar": "مراجعة تصميم أو مراجعة متخصص"},
    "UI_S15_DEP_MSG_INVALID": {
        "en": "A dependency must name the two parts of that interaction, or both. No changes were saved.",
        "ar": "يجب أن يسمّي الاعتماد جزأي ذلك التفاعل، أو كليهما معًا. لم يُحفظ أي تغيير.",
    },
    "UI_S15_DEP_MSG_TOO_LONG": {
        "en": "A dependency explanation can be at most 300 characters. No changes were saved.",
        "ar": "يمكن أن يكون شرح الاعتماد 300 حرف كحدّ أقصى. لم يُحفظ أي تغيير.",
    },
    "UI_S15_DEP_MSG_NOTE_ALONE": {
        "en": "An explanation can only accompany a declared dependency. Choose who relies on whom, or clear the explanation. No changes were saved.",
        "ar": "لا يمكن إرفاق شرح إلا مع اعتماد مُصرَّح به. اختر أيّ الجزأين يعتمد على الآخر، أو امسح الشرح. لم يُحفظ أي تغيير.",
    },
    "UI_S15_IEV_MSG_SAVED": {
        "en": "Your integration evidence was saved to your project. It is your own statement: InventorAI has not checked it, and it does not show that the parts are compatible.",
        "ar": "حُفظ دليل التكامل في مشروعك. إنه قولك أنت: لم يفحصه InventorAI، ولا يعني أن الجزأين متوافقان.",
    },
    "UI_S15_IEV_MSG_CORRECTED": {
        "en": "Your correction was saved as a new entry; the earlier entry stays in the history. InventorAI has not checked it.",
        "ar": "حُفظ تصحيحك كإدخال جديد؛ ويبقى الإدخال السابق في السجلّ. لم يفحصه InventorAI.",
    },
    "UI_S15_IEV_MSG_WITHDRAWN": {
        "en": "That evidence item was withdrawn. It stays in the history and no longer counts as current evidence.",
        "ar": "سُحب عنصر الأدلة ذلك. يبقى في السجلّ ولم يعد يُحتسب دليلًا حاليًا.",
    },
    "UI_S15_IEV_MSG_NOT_SAVED": {
        "en": "Your integration evidence could not be saved just now. Nothing was changed.",
        "ar": "تعذّر حفظ دليل التكامل الآن. لم يتم تغيير أي شيء.",
    },
    "UI_S15_IEV_MSG_TEXT_REJECTED": {
        "en": "Some of the text could not be accepted. Fill in every required field within its length limit. Nothing was changed.",
        "ar": "تعذّر قبول بعض النص. املأ كل حقل مطلوب ضمن حدّ طوله. لم يتم تغيير أي شيء.",
    },
    "UI_S15_IEV_MSG_NOT_CURRENT": {
        "en": "That interaction is not part of this project, so no evidence can be recorded for it here. Nothing was changed.",
        "ar": "هذا التفاعل ليس جزءًا من هذا المشروع، لذا لا يمكن تسجيل أدلة له هنا. لم يتم تغيير أي شيء.",
    },
    "UI_S15_IEV_MSG_STALE": {
        "en": "That evidence item has already been corrected or withdrawn, or this page no longer matches what your project holds, so nothing was saved. Review the page and try again.",
        "ar": "سبق تصحيح عنصر الأدلة ذلك أو سحبه، أو لم تعد هذه الصفحة تطابق ما يحتفظ به مشروعك، لذا لم يُحفظ شيء. راجع الصفحة وحاول مرة أخرى.",
    },
    "UI_S15_IEV_MSG_CAP": {
        "en": "This project already holds the maximum number of evidence items, so no new one can be added. Nothing was changed.",
        "ar": "يحتوي هذا المشروع بالفعل على أقصى عدد من عناصر الأدلة، لذا لا يمكن إضافة عنصر جديد. لم يتم تغيير أي شيء.",
    },
    "UI_S15_IEV_MSG_UNKNOWN": {
        "en": "We could not confirm whether your integration evidence was saved. Reload this page to see what your project holds before entering it again.",
        "ar": "تعذّر علينا التأكد مما إذا كان دليل التكامل قد حُفظ. أعد تحميل الصفحة لترى ما يحتفظ به مشروعك قبل إدخاله مرة أخرى.",
    },
    "UI_S15_OBS_MSG_NOT_SAVED": {
        "en": "Your observation could not be saved just now. Nothing was changed.",
        "ar": "تعذّر حفظ ملاحظتك الآن. لم يتم تغيير أي شيء.",
    },
    "UI_S15_OBS_MSG_SAVED": {
        "en": "Your observation was saved to your project. It has not been checked or validated by InventorAI, and InventorAI does not decide whether the acceptance criterion was met.",
        "ar": "حُفظت ملاحظتك في مشروعك. لم يفحصها InventorAI ولم يتحقق من صحتها، ولا يقرّر InventorAI ما إذا كان معيار القبول قد استُوفي.",
    },
    "UI_S15_OBS_MSG_INVALID": {
        "en": "Describe in your own words what actually happened when you checked this interaction. Nothing was changed.",
        "ar": "صِف بكلماتك ما الذي حدث فعلًا عندما فحصت هذا التفاعل. لم يتم تغيير أي شيء.",
    },
    "UI_S15_OBS_MSG_TOO_LONG": {
        "en": "An observation can be at most 1000 characters. Nothing was changed.",
        "ar": "يمكن أن تكون الملاحظة 1000 حرف كحدّ أقصى. لم يتم تغيير أي شيء.",
    },
    "UI_S15_OBS_MSG_NOT_CURRENT": {
        "en": "That interaction is not part of this project, so no observation can be recorded or corrected for it here. Nothing was changed.",
        "ar": "هذا التفاعل ليس جزءًا من هذا المشروع، لذا لا يمكن تسجيل ملاحظة له أو تصحيحها هنا. لم يتم تغيير أي شيء.",
    },
    "UI_S15_OBS_MSG_STALE": {
        "en": "That observation has already been corrected, or this page no longer matches what your project holds, so nothing was saved. Review the page and try again.",
        "ar": "صُحّحت هذه الملاحظة من قبل، أو أن هذه الصفحة لم تعد تطابق ما يحتفظ به مشروعك، لذا لم يُحفظ شيء. راجع الصفحة وحاول مرة أخرى.",
    },
    "UI_S15_OBS_MSG_CAP": {
        "en": "This project already holds the maximum of 200 recorded observations, so no new one can be added. Nothing was changed and no earlier entry was removed.",
        "ar": "يحتفظ هذا المشروع بالحدّ الأقصى وهو 200 ملاحظة مُسجَّلة، لذا لا يمكن إضافة ملاحظة جديدة. لم يتم تغيير أي شيء ولم يُحذف أي إدخال سابق.",
    },
    "UI_S15_OBS_MSG_UNKNOWN": {
        "en": "We could not confirm whether your observation was saved. Reload this page to see what your project holds before entering it again.",
        "ar": "تعذّر علينا التأكد مما إذا كانت ملاحظتك قد حُفظت. أعد تحميل الصفحة لترى ما يحتفظ به مشروعك قبل إدخالها مرة أخرى.",
    },
    "UI_S15_IFC_ERR_NOT_SAVED": {
        "en": "That interaction could not be saved just now. Nothing was changed.",
        "ar": "تعذّر حفظ هذا التفاعل الآن. لم يتم تغيير أي شيء.",
    },
    "UI_S15_IFC_ERR_INVALID": {
        "en": "Describe the interaction in your own words and tick the declaration box. Nothing was changed.",
        "ar": "صِف التفاعل بكلماتك وحدّد مربع الإعلان. لم يتم تغيير أي شيء.",
    },
    "UI_S15_IFC_ERR_TOO_LONG": {
        "en": "An interaction description can be at most 300 characters. Nothing was changed - please shorten it and submit again.",
        "ar": "يمكن أن يصل وصف التفاعل إلى 300 حرف على الأكثر. لم يتم تغيير أي شيء — يُرجى تقصير النص وإعادة الإرسال.",
    },
    "UI_S15_IFC_ERR_INVALID_CHAR": {
        "en": "The interaction description contains an invalid character. Nothing was changed - please remove it and submit again.",
        "ar": "يحتوي وصف التفاعل على رمز غير صالح. لم يتم تغيير أي شيء — يُرجى إزالته وإعادة الإرسال.",
    },
    "UI_S15_IFC_ERR_STALE": {
        "en": "This form is no longer current, so nothing was saved. Review the page and record the interaction again.",
        "ar": "لم يعد هذا النموذج حاليًا، لذلك لم يُحفظ أي شيء. راجع الصفحة وسجّل التفاعل مرة أخرى.",
    },
    "UI_S15_IFC_ERR_UNKNOWN": {
        "en": "We could not confirm whether that interaction was saved. It is not shown as saved until that can be confirmed. Submitting it again from here is safe: it will never be recorded twice.",
        "ar": "تعذّر علينا التأكد مما إذا كان هذا التفاعل قد حُفظ. لن يُعرض على أنه محفوظ حتى يمكن التأكد من ذلك. إعادة إرساله من هنا آمنة: لن يُسجَّل مرتين أبدًا.",
    },
    "UI_S15_IFC_UNKNOWN_TITLE": {"en": "Save not confirmed", "ar": "لم يتأكد الحفظ"},
    "UI_S15_IFC_UNKNOWN_RETRY": {
        "en": "Submit the same interaction again",
        "ar": "إعادة إرسال التفاعل نفسه",
    },
    "UI_S15_IFC_UNKNOWN_BACK": {"en": "Back to your project", "ar": "العودة إلى مشروعك"},
    "UI_CSRF_REJECT": {
        "en": "Your session security token was missing or invalid. This request was rejected before any change was made.",
        "ar": "رمز أمان الجلسة مفقود أو غير صالح. رُفض هذا الطلب قبل إجراء أي تغيير.",
    },
    "UI_A1_RECOVERY_TITLE": {"en": "Return to a fresh form", "ar": "العودة إلى نموذج جديد"},
    "UI_A1_RECOVERY_TEXT": {
        "en": "Use the link below to open the form again, review your entries and submit. Do not reload or resubmit this rejected page. If a local draft is available, you can choose to restore it on the form.",
        "ar": "استخدم الرابط أدناه لفتح النموذج من جديد، ومراجعة إدخالاتك ثم إرسالها. لا تُعد تحميل هذه الصفحة المرفوضة أو إرسالها. إذا كانت هناك مسودة محلية متاحة، يمكنك اختيار استعادتها في النموذج."
    },
    "UI_A1_RECOVERY_EMAIL": {
        "en": "For email verification or password reset, reopen the original link from your email. If it has expired, request a new link from your account or the password recovery form.",
        "ar": "للتحقق من البريد أو إعادة تعيين كلمة المرور، افتح الرابط الأصلي في بريدك من جديد. إذا انتهت صلاحيته، اطلب رابطًا جديدًا من حسابك أو نموذج استعادة كلمة المرور."
    },
    "UI_A1_RECOVERY_LINK": {"en": "Open a fresh form", "ar": "فتح نموذج جديد"},
    "UI_A1_ORIGINAL_IDEA": {"en": "Your original description", "ar": "وصفك الأصلي"},
    "UI_A1_UNTITLED": {"en": "Saved project", "ar": "مشروع محفوظ"},
    "UI_A1_DETAILS_UNAVAILABLE": {"en": "Project details could not be loaded. Try reopening it.", "ar": "تعذّر تحميل تفاصيل المشروع. حاول فتحه من جديد."},
    "UI_A1_LIST_UNAVAILABLE": {"en": "Your project list could not be loaded. This does not mean your projects were deleted.", "ar": "تعذّر تحميل قائمة مشاريعك. هذا لا يعني حذف مشاريعك."},
    "UI_A1_RETRY_LIST": {"en": "Try loading your projects again", "ar": "محاولة تحميل مشاريعك من جديد"},
    "UI_A1_PROJECT_ID": {"en": "Project reference", "ar": "مرجع المشروع"},
    "UI_A1_PROJECT_LIST_NOTE": {"en": "Descriptions below are your original words, not independently verified findings. Open a project to review its saved state and unresolved questions.", "ar": "الأوصاف أدناه هي كلماتك الأصلية، وليست نتائج تحقّق مستقل. افتح مشروعًا لمراجعة حالته المحفوظة والأسئلة التي لم تُحسم."},
    "UI_PROJECT_FILTER_SEARCH": {"en": "Find a saved project", "ar": "البحث عن مشروع محفوظ"},
    "UI_PROJECT_FILTER_DOMAIN": {"en": "Domain", "ar": "المجال"},
    "UI_PROJECT_FILTER_ALL_DOMAINS": {"en": "All domains", "ar": "كل المجالات"},
    "UI_PROJECT_FILTER_HELP": {"en": "Filters only the description excerpts and project references shown below, not the full project contents.", "ar": "يقتصر البحث على مقتطفات الأوصاف ومراجع المشاريع المعروضة أدناه، ولا يشمل محتويات المشاريع كاملةً."},
    "UI_PROJECT_FILTER_CLEAR": {"en": "Clear filters", "ar": "مسح عوامل التصفية"},
    "UI_PROJECT_FILTER_COUNT": {"en": "Showing {shown} of {total} projects.", "ar": "المشاريع المعروضة: {shown} من أصل {total}."},
    "UI_PROJECT_FILTER_NO_MATCH": {"en": "No projects match these filters. Clear the filters to see all your saved projects.", "ar": "لا توجد مشاريع تطابق عوامل التصفية هذه. امسح عوامل التصفية لعرض جميع مشاريعك المحفوظة."},
    "UI_A1_NEXT_ACTION": {"en": "Your next action", "ar": "خطوتك التالية"},
    "UI_A1_ANSWER_NEXT": {"en": "Answer the current question", "ar": "الإجابة عن السؤال الحالي"},
    "UI_A1_ANSWER_NOTE": {"en": "One question at a time. You can give an answer or explicitly record what you do not know yet.", "ar": "سؤال واحد في كل مرة. يمكنك الإجابة أو تسجيل ما لا تعرفه بعد بشكل صريح."},
    "UI_A1_READ_ONLY": {"en": "Saved view. Continue only when the continuation option is available below.", "ar": "عرض محفوظ. يمكنك المتابعة فقط عندما يتوفر خيار المتابعة أدناه."},
    "UI_A1_REVIEW_HANDOFF": {"en": "Review the current handoff", "ar": "مراجعة حزمة التسليم الحالية"},
    "UI_A1_HANDOFF_NOTE": {"en": "Review the recorded evidence and gaps before using the handoff. A completed question flow is not engineering, manufacturing or commercial validation.", "ar": "راجع الأدلة والفجوات المسجّلة قبل استخدام حزمة التسليم. اكتمال مسار الأسئلة لا يعني تحقّقًا هندسيًا أو تصنيعيًا أو تجاريًا."},
    "UI_A1_REVIEW_REQUIREMENT": {"en": "Review the current requirement", "ar": "مراجعة المتطلب الحالي"},
    "UI_A1_SAVED": {"en": "Your answer was saved to this project.", "ar": "تم حفظ إجابتك في هذا المشروع."},
    "UI_A1_PROJECT_SAVED": {"en": "Your project was saved. Continue with the next action below.", "ar": "تم حفظ مشروعك. تابع بالخطوة التالية أدناه."},
    "UI_A1_SENDING": {"en": "Submitting… Saving is not confirmed yet.", "ar": "جارٍ الإرسال… لم يتأكد الحفظ بعد."},
    "UI_A1_WAITING": {"en": "Still waiting for a response. Saving is not confirmed. Keep your text until the result is shown.", "ar": "ما زلنا ننتظر الرد. لم يتأكد الحفظ. احتفظ بنصك إلى أن تظهر النتيجة."},
    "UI_A1_DESCRIPTION_NOTE": {"en": "Original description; not a validation result.", "ar": "الوصف الأصلي؛ وليس نتيجة تحقّق."},
    "UI_VERIFY_CONFIRM_TITLE": {
        "en": "Verify your email", "ar": "التحقق من بريدك الإلكتروني",
    },
    "UI_VERIFY_CONFIRM_ACTION": {
        "en": "Confirm email verification", "ar": "تأكيد التحقق من البريد",
    },
    "UI_DW_START_TITLE": {
        "en": "Decision workspace", "ar": "مساحة عمل القرار",
    },
    "UI_DW_START_ACTION": {
        "en": "Create a decision workspace", "ar": "إنشاء مساحة عمل للقرار",
    },
    # --- shared shell (base.html) + language selector --------------------------
    "UI_LANG_MENU_LABEL": {"en": "Language", "ar": "اللغة"},
    "UI_B_BASE_001": {"en": "Skip to content", "ar": "تخطَّ إلى المحتوى"},
    "UI_B_BASE_002": {"en": "Temporary session", "ar": "جلسة مؤقتة"},
    "UI_B_BASE_003": {"en": "Learn more", "ar": "معرفة المزيد"},

    # --- index.html ------------------------------------------------------------
    "UI_B_INDEX_001": {
        "en": ("InventorAI helps you develop an early invention idea. It asks a "
               "few focused questions, one at a time, and organizes your answers "
               "into a clear, readable assessment you can revisit."),
        "ar": ("يساعدك InventorAI على تطوير فكرة اختراع في مراحلها المبكرة. يطرح "
               "عليك بضعة أسئلة مركّزة، واحدًا تلو الآخر، وينظّم إجاباتك في تقييم "
               "واضح وسهل القراءة يمكنك العودة إليه."),
    },
    # The "How it works:" lead renders bold; the body follows (same full sentence
    # as the finalized UI-SENS-INDEX-02 copy, split only for the existing emphasis).
    "UI_B_INDEX_002_LEAD": {"en": "How it works:", "ar": "كيف يعمل:"},
    "UI_B_INDEX_002": {
        "en": ("you describe your idea, answer one guided question per step, and "
               "build up a snapshot of what your idea is, what it needs, and what "
               "to do next."),
        "ar": ("تصف فكرتك، وتجيب عن سؤال موجَّه واحد في كل خطوة، فتبني لقطة توضّح "
               "ما هي فكرتك، وما الذي تحتاجه، وما ينبغي فعله لاحقًا."),
    },
    "UI_B_INDEX_003": {
        "en": "Describe your invention idea to begin.",
        "ar": "صف فكرة اختراعك للبدء.",
    },
    "UI_B_INDEX_004": {
        "en": ("Electronics and electrical ideas are currently supported. Before "
               "starting, please confirm that your idea belongs to this supported "
               "domain."),
        "ar": ("الأفكار في مجال الإلكترونيات والكهرباء مدعومة حاليًا. قبل البدء، "
               "يرجى تأكيد أن فكرتك تنتمي إلى هذا المجال المدعوم."),
    },
    "UI_B_INDEX_005": {"en": "Describe your idea", "ar": "صف فكرتك"},
    "UI_B_INDEX_006": {
        "en": "Describe your electronics or electrical invention...",
        "ar": "صف اختراعك في الإلكترونيات أو الكهرباء...",
    },
    "UI_B_INDEX_007": {
        "en": "I confirm that this idea is primarily an electronics or electrical idea.",
        "ar": "أؤكد أن هذه الفكرة هي في الأساس فكرة في الإلكترونيات أو الكهرباء.",
    },
    "UI_B_INDEX_008": {"en": "Start", "ar": "ابدأ"},
    "UI_B_INDEX_009": {
        "en": "Currently supported: electronics and electrical ideas.",
        "ar": "المدعوم حاليًا: الأفكار في الإلكترونيات والكهرباء.",
    },

    # --- index.html: CF-2 Arabic-localization remainder — activation-aware -----
    # /start copy (web/app.py `_unsupported_domain_message`,
    # `_confirmation_required_message`, `_present_confirm_message`, and the
    # `_render_start_page` generalized-context strings). English is UNCHANGED
    # (composed dynamically as before, byte-identical); these keys supply the
    # Arabic side ONLY, consulted directly by those functions. Per the CF-2
    # Fast Track boundary, the broadened-activation (2+ domains) Arabic copy is
    # deliberately DOMAIN-NEUTRAL — it never names a specific non-electronics
    # domain in Arabic (that would require new Tier-1 label translation work,
    # out of scope here and explicitly forbidden by the governing contract) —
    # with ONE later, separately authorized exception: UXAR-01's present-confirm
    # paragraph/checkbox templates (UI_B_START_032 / UI_B_START_024) identify
    # the review path by formatting in the EXISTING canonical Tier-1 label from
    # `web/domain_label.py` at render time (no new translation; the catalogue
    # entries themselves still name no domain) —
    # while still truthfully describing the real state (never an
    # electronics-only claim, never a false single-domain implication). The
    # empty-activation Arabic copy needs no domain name at all. Both broadened
    # and empty-activation states are reachable only via a bounded activation
    # test double today (real activation remains `['electronics_electrical']`).
    # --- /start-flow raw error-path constants (web/app.py `_MESSAGE_KEYS`) ----
    # Registered via `localize_message()`, same mechanism as UI_B_SESSION_039/040
    # above — the English source constant is the dict key; these are its
    # Arabic (and, redundantly but harmlessly, restated English) variants.
    "UI_B_START_010": {  # UNSUPPORTED_DOMAIN_MESSAGE
        "en": ("InventorAI currently supports electronics and electrical ideas only. "
               "Please describe an electronics or electrical invention."),
        "ar": ("يدعم InventorAI حاليًا أفكار الإلكترونيات والكهرباء فقط. يرجى وصف "
               "اختراع في مجال الإلكترونيات أو الكهرباء."),
    },
    "UI_B_START_011": {  # CONFIRMATION_REQUIRED_MESSAGE
        "en": ("Please confirm that your idea is an electronics or electrical idea "
               "before starting."),
        "ar": "يرجى تأكيد أن فكرتك هي فكرة في الإلكترونيات أو الكهرباء قبل البدء.",
    },
    "UI_B_START_012": {  # MECHANISM_GUIDANCE_MESSAGE
        "en": ("InventorAI currently supports electronics and electrical ideas only. Your "
               "description does not yet clearly show the electrical mechanism. Try adding a "
               "simple phrase describing how it works electrically — for example that it uses "
               "a sensor, current, switch, circuit, power, plug, or microcontroller."),
        "ar": ("يدعم InventorAI حاليًا أفكار الإلكترونيات والكهرباء فقط. لا يوضح وصفك "
               "بعد الآلية الكهربائية بشكل واضح. حاول إضافة عبارة بسيطة تصف كيف تعمل "
               "كهربائيًا — على سبيل المثال أنها تستخدم مستشعرًا أو تيارًا أو مفتاحًا أو "
               "دائرة أو طاقة أو قابسًا أو متحكمًا دقيقًا."),
    },
    "UI_B_START_013": {  # DOMAIN_CHOICE_MESSAGE
        "en": ("Your description did not clearly match one supported domain. Please choose "
               "the domain that best fits your idea, then confirm it."),
        "ar": ("لم يتطابق وصفك بوضوح مع مجال مدعوم واحد. يرجى اختيار المجال الأنسب "
               "لفكرتك، ثم تأكيده."),
    },
    "UI_B_START_014": {  # SERVICE_UNAVAILABLE_MESSAGE
        "en": "This service is temporarily unavailable. Please try again in a moment.",
        "ar": "هذه الخدمة غير متاحة مؤقتًا. يرجى المحاولة مرة أخرى بعد قليل.",
    },

    "UI_B_START_020": {  # unsupported-domain, empty activation
        "en": "InventorAI has no specialist domain available right now. Please try again later.",
        "ar": "لا يتوفر لدى InventorAI أي مجال متخصص حاليًا. يرجى المحاولة لاحقًا.",
    },
    "UI_B_START_021": {  # unsupported-domain, broadened (2+) activation — domain-neutral
        "en": "InventorAI currently supports more than one specialist domain. Please describe an invention in a supported domain.",
        "ar": "يدعم InventorAI حاليًا أكثر من مجال متخصص واحد. يرجى وصف اختراع ضمن أحد المجالات المدعومة.",
    },
    "UI_B_START_022": {  # confirmation-required, broadened single-non-electronics-domain activation — domain-neutral
        "en": "Please confirm that your idea belongs to the supported domain before starting.",
        "ar": "يرجى تأكيد أن فكرتك تنتمي إلى المجال المدعوم قبل البدء.",
    },
    "UI_B_START_023": {  # present-confirm, electronics-only (byte-content-equivalent to the EN concatenation)
        "en": "Your idea appears to belong to the Electronics Electrical domain. Please confirm this domain to start, or revise your description.",
        "ar": "يبدو أن فكرتك تنتمي إلى مجال الإلكترونيات والكهرباء. يرجى تأكيد هذا المجال للبدء، أو تعديل الوصف.",
    },
    "UI_B_START_024": {  # present-confirm CHECKBOX consent (AR, both activated domains)
        # L10N-RH-01 Observation #3 remediation: first-person consent
        # affirmation (matching UI_B_START_030's register) rather than
        # prompt/instruction wording. UXAR-01 role split: the Arabic value is
        # now a `{review_label}` TEMPLATE consumed ONLY by the checkbox label
        # (`start_present_confirm_label`); the paragraph role moved to
        # UI_B_START_032. The review-path label is injected at render time
        # from the canonical `web/domain_label.py` resolver — the catalogue
        # itself still names no domain. English is byte-unchanged.
        "en": "I confirm that this idea belongs to the domain that was recognized for it.",
        "ar": "أؤكد أنني أرغب في متابعة فكرتي عبر «{review_label}».",
    },
    "UI_B_START_025": {  # start_scope_sentence, empty activation
        "en": "No specialist domain is currently available.",
        "ar": "لا يتوفر حاليًا أي مجال متخصص.",
    },
    "UI_B_START_026": {  # start_scope_sentence, broadened (2+) activation — domain-neutral
        "en": "More than one specialist domain is currently supported. Before starting, please confirm the domain your idea belongs to.",
        "ar": "يُدعم حاليًا أكثر من مجال متخصص واحد. قبل البدء، يرجى تأكيد المجال الذي تنتمي إليه فكرتك.",
    },
    "UI_B_START_027": {  # start_placeholder, any non-electronics-only activation state
        "en": "Describe your invention...",
        "ar": "صف اختراعك...",
    },
    "UI_B_START_028": {  # start_supported_note, empty activation
        "en": "Currently supported: none.",
        "ar": "المدعوم حاليًا: لا شيء.",
    },
    "UI_B_START_029": {  # start_supported_note, broadened (2+) activation — domain-neutral
        "en": "Currently supported: more than one specialist domain.",
        "ar": "المدعوم حاليًا: أكثر من مجال متخصص واحد.",
    },
    "UI_B_START_030": {  # start_confirm_label, broadened single-non-electronics-domain activation — domain-neutral
        "en": "I confirm that this idea is primarily a supported-domain idea.",
        "ar": "أؤكد أن هذه الفكرة هي في الأساس فكرة ضمن المجال المدعوم.",
    },
    "UI_B_START_031": {  # start_choice_prompt (domain-neutral already in English; unchanged, added for AR)
        "en": "Choose your idea's domain:",
        "ar": "اختر مجال فكرتك:",
    },
    # UXAR-01: present-confirm explanatory PARAGRAPH (`<p class="error">`), a
    # `{review_label}` template formatted with the canonical Arabic review-path
    # label for BOTH activated domains and both route origins (D1 classifier-
    # selected, D2 user-chosen). Deliberately says "selected review path" and
    # never who selected it. Consumed directly through `ui_text.text()`; it is
    # NOT a `_MESSAGE_KEYS` member (no English server-message constant owns it —
    # the English runtime branch still composes its own sentence).
    "UI_B_START_032": {
        "en": (
            "The selected review path for your idea is “{review_label}”. "
            "Please confirm this path to start, or revise your description."
        ),
        "ar": (
            "المسار المحدد لمراجعة فكرتك هو «{review_label}». "
            "يرجى تأكيد هذا المسار للبدء، أو تعديل وصفك."
        ),
    },

    # --- index.html + data_session.html + success_criteria.html: sensitive -----
    # (truth-corrected, owner-approved product-truth copy)
    "UI_SENS_INDEX_03": {
        "en": ("This is an advisory tool to sharpen your own thinking. The "
               "assessment is a work-in-progress snapshot — not a validation, "
               "verification, score, approval, certification, patent opinion, "
               "legal opinion, or final technical judgment. You remain responsible "
               "for verifying any technical claim."),
        "ar": ("هذه أداة استشارية لصقل تفكيرك. التقييم لقطة قيد الإنجاز — وليس "
               "تحقّقًا أو تدقيقًا أو درجةً أو موافقةً أو اعتمادًا أو رأيًا بشأن "
               "براءة اختراع أو رأيًا قانونيًا أو حكمًا تقنيًا نهائيًا. تبقى مسؤولًا "
               "عن التحقّق من أي ادعاء تقني."),
    },
    "UI_SENS_INDEX_04": {
        "en": ("You can start anonymously, or create an account and sign in to "
               "keep and reopen your projects. Your current working session may "
               "still contain temporary state."),
        "ar": ("يمكنك البدء دون تسجيل، أو إنشاء حساب وتسجيل الدخول للاحتفاظ "
               "بمشاريعك وإعادة فتحها. وقد تظل جلسة العمل الحالية تحتوي على حالة "
               "مؤقتة."),
    },
    "UI_SENS_INDEX_05": {
        "en": ("Unfinished text may be kept temporarily on this device/browser so "
               "you can recover it here if you leave and return. It is not saved "
               "to an account or another device, expires after 7 days, and can be "
               "discarded. Anyone using this browser profile may be able to see it."),
        "ar": ("قد يُحفَظ النص غير المكتمل مؤقتًا على هذا الجهاز/المتصفّح حتى "
               "تتمكّن من استعادته هنا إذا غادرت ثم عدت. لا يُحفَظ في حساب أو على "
               "جهاز آخر، وتنتهي صلاحيته بعد 7 أيام، ويمكن حذفه. قد يتمكّن أي شخص "
               "يستخدم ملفّ هذا المتصفّح من الاطّلاع عليه."),
    },

    # --- data_session.html -----------------------------------------------------
    "UI_B_DATA_TITLE": {
        "en": "Data & Session information",
        "ar": "معلومات البيانات والجلسة",
    },
    "UI_B_DATA_BACK": {"en": "Back to InventorAI", "ar": "العودة إلى InventorAI"},
    "UI_SENS_DATA_01": {
        "en": ("Your idea and accepted answers are saved as part of your project "
               "so the tool can prepare and reload your assessment. Some "
               "in-progress working state remains temporary to the current session."),
        "ar": ("تُحفَظ فكرتك وإجاباتك المقبولة كجزء من مشروعك حتى تتمكّن الأداة من "
               "إعداد تقييمك وإعادة تحميله. وتبقى بعض حالة العمل الجارية مؤقتةً "
               "ضمن الجلسة الحالية."),
    },
    "UI_SENS_DATA_02": {
        "en": ("Signed-in accounts can keep and reopen saved projects. Version "
               "history and branching are not currently provided."),
        "ar": ("يمكن للحسابات المسجَّل دخولها الاحتفاظ بالمشاريع المحفوظة وإعادة "
               "فتحها. أما سِجلّ الإصدارات والتفرّع فغير متوفّرين حاليًا."),
    },
    "UI_SENS_DATA_03": {
        "en": ("To help you recover unfinished text if you leave and return, text "
               "you are typing may be kept temporarily in this browser on this "
               "device only (local browser storage). It is not saved to an account "
               "or to any server, and is not available on another device or "
               "browser. It expires after 7 days, is removed once the matching "
               "answer is submitted, and can be discarded at any time. Because it "
               "is kept in this browser profile, anyone who can use this browser "
               "(including browser-profile sync) may be able to see it — please "
               "avoid this feature on a shared or public device, or discard your "
               "draft when you finish."),
        "ar": ("لمساعدتك على استعادة النص غير المكتمل إذا غادرت ثم عدت، قد يُحفَظ "
               "النص الذي تكتبه مؤقتًا في هذا المتصفّح وعلى هذا الجهاز فقط (تخزين "
               "محلي في المتصفّح). لا يُحفَظ في حساب ولا على أي خادم، ولا يتوفّر "
               "على جهاز أو متصفّح آخر. تنتهي صلاحيته بعد 7 أيام، ويُزال بمجرّد "
               "إرسال الإجابة المقابلة، ويمكن حذفه في أي وقت. ولأنه محفوظ في ملفّ "
               "هذا المتصفّح، فقد يتمكّن أي شخص يستطيع استخدام هذا المتصفّح (بما في "
               "ذلك مزامنة ملفّ المتصفّح) من الاطّلاع عليه — يُرجى تجنّب هذه الميزة "
               "على جهاز مشترك أو عام، أو حذف مسوّدتك عند الانتهاء."),
    },
    "UI_SENS_DATA_04": {
        "en": ("You can use InventorAI anonymously, or create an account and sign "
               "in. Having an account or a saved project does not create or prove "
               "legal ownership of your idea."),
        "ar": ("يمكنك استخدام InventorAI دون تسجيل، أو إنشاء حساب وتسجيل الدخول. "
               "ووجود حساب أو مشروع محفوظ لا يُنشئ ملكية قانونية لفكرتك ولا "
               "يُثبتها."),
    },
    "UI_SENS_DATA_05": {
        "en": ("Your accepted answers are saved as part of your project so the "
               "tool can prepare and reload your assessment. This does not provide "
               "a complete resumable record of every interaction in your session."),
        "ar": ("تُحفَظ إجاباتك المقبولة كجزء من مشروعك حتى تتمكّن الأداة من إعداد "
               "تقييمك وإعادة تحميله. غير أن ذلك لا يوفّر سجلًّا كاملًا وقابلًا "
               "للاستئناف لكل تفاعل في جلستك."),
    },
    "UI_SENS_DATA_06": {
        "en": ("Confidentiality and staff-access details are not finalized on this "
               "screen. Do not rely on this screen as a promise that information "
               "can never be accessed or reviewed."),
        "ar": ("لم تُحدَّد نهائيًا على هذه الشاشة تفاصيل السرّية ووصول الموظفين. لا "
               "تعتمد على هذه الشاشة كوعدٍ بأن المعلومات لا يمكن الوصول إليها أو "
               "مراجعتها إطلاقًا."),
    },
    "UI_SENS_DATA_07": {
        "en": "Privacy Policy and Terms content is not provided on this information screen.",
        "ar": "لا يُقدَّم محتوى سياسة الخصوصية والشروط على شاشة المعلومات هذه.",
    },

    # --- success_criteria.html -------------------------------------------------
    "UI_SC_CONTEXT": {
        "en": "Experiment context",
        "ar": "سياق التجربة",
    },
    "UI_SC_EDIT_EXPERIMENT": {
        "en": ("Edit this experiment’s criterion, hypothesis, variable / condition "
               "and measurement method"),
        "ar": "تعديل معيار هذه التجربة وفرضيتها ومتغيّرها / شرطها وطريقة قياسها",
    },
    # F-09: the limit counts the text as the browser submits it, where every
    # line break is sent as two characters (CRLF); say so, truthfully.
    "UI_SC_LIMIT": {
        "en": ("Optional. Limit: {limit} characters; each line break counts as "
               "two characters."),
        "ar": "اختياري. الحد الأقصى: {limit} حرف، ويُحتسب كل فاصل أسطر بحرفين.",
    },
    # F-09: shown only when a submission was refused and the inventor's own
    # entries are re-shown in the form — they are NOT saved.
    "UI_SC_DRAFT_UNSAVED": {
        "en": ("Your entries are still shown in the form below, but they have "
               "not been saved. Correct them and choose Save planning entries "
               "to save them."),
        "ar": ("لا تزال إدخالاتك معروضة في النموذج أدناه، لكنها لم تُحفظ. "
               "صحّحها ثم اختر حفظ إدخالات التخطيط لحفظها."),
    },
    "UI_SC_SAVE_CLEAR": {
        "en": ("Edits apply only when you choose Save planning entries. To "
               "remove an existing entry, clear its box and choose Save planning "
               "entries."),
        "ar": ("لا تُطبَّق التعديلات إلا عند اختيار حفظ إدخالات التخطيط. لإزالة "
               "إدخال موجود، أفرغ خانته ثم اختر حفظ إدخالات التخطيط."),
    },
    "UI_B_SC_001": {
        "en": ("InventorAI — Define Success Criteria, Test Hypotheses, Test "
               "Variables / Conditions and Measurement Methods"),
        "ar": ("InventorAI — تحديد معايير النجاح وفرضيات الاختبار ومتغيّرات / شروط "
               "الاختبار وطرق القياس"),
    },
    "UI_SENS_SC_01": {
        "en": ("For each proposed experiment below, you may enter one success "
               "criterion: a target you decide on for judging whether that test "
               "succeeded. A criterion is your own planning target — it is not a "
               "test result, and saving it does not validate, demonstrate, or "
               "approve anything. Leave a box blank to keep that criterion "
               "undefined."),
        "ar": ("لكل تجربة مقترحة أدناه، يمكنك إدخال معيار نجاح واحد: هدف تحدّده "
               "بنفسك للحكم على نجاح ذلك الاختبار. المعيار هو هدفك التخطيطي الخاص — "
               "وليس نتيجة اختبار، ولا يُعدّ حفظه إثباتًا لأي شيء أو برهانًا عليه "
               "أو موافقةً عليه. اترك الخانة فارغة لإبقاء ذلك المعيار غير محدّد."),
    },
    "UI_B_SC_002": {
        "en": "Success criterion (your target):",
        "ar": "معيار النجاح (هدفك):",
    },
    "UI_B_SC_003": {
        "en": "Optional — define how you will judge this test.",
        "ar": "اختياري — حدّد كيف ستحكم على هذا الاختبار.",
    },
    "UI_B_SC_004": {"en": "Save planning entries", "ar": "حفظ إدخالات التخطيط"},
    "UI_B_SC_005": {
        "en": "No proposed experiments are currently available for this session.",
        "ar": "لا توجد حاليًا تجارب مقترحة متاحة لهذه الجلسة.",
    },
    "UI_B_SC_006": {"en": "Back to the assessment", "ar": "العودة إلى التقييم"},
    # CF-2 Arabic-localization remainder: the two raw `_reject()` rejection
    # messages (web/app.py `save_success_criteria`) previously bypassed
    # localization entirely. Registered via `_MESSAGE_KEYS` (storage stays
    # English; only display localises), same pattern as UI_B_SESSION_039/040.
    "UI_B_SC_007": {
        "en": "A submitted experiment is not part of the current plan. No changes were saved.",
        "ar": "التجربة المُرسلة ليست جزءًا من الخطة الحالية. لم يتم حفظ أي تغييرات.",
    },
    "UI_B_SC_008": {
        "en": "A criterion exceeds the 1000-character limit. No changes were saved.",
        "ar": "يتجاوز أحد المعايير الحد الأقصى البالغ 1000 حرف. لم يتم حفظ أي تغييرات.",
    },
    # Stage 19 / CAP-09 durable SuccessCriterion — registered via
    # `_MESSAGE_KEYS` (storage stays English; only display localises).
    "UI_SC_ERR_NOT_SAVED_PROJECT": {
        "en": (
            "Success criteria, test hypotheses, test variables / conditions and "
            "measurement methods can only be kept for a saved project. This session "
            "is not saved as a project, so they cannot be saved here. Nothing was "
            "changed."),
        "ar": (
            "لا يمكن الاحتفاظ بمعايير النجاح وفرضيات الاختبار ومتغيّرات / شروط "
            "الاختبار وطرق القياس إلا لمشروع محفوظ. هذه الجلسة غير محفوظة كمشروع، "
            "لذلك لا يمكن حفظها هنا. لم يتم تغيير أي شيء."),
    },
    "UI_SC_ERR_PLAN_UNAVAILABLE": {
        "en": (
            "The current Prototype & Test Plan is not available from this saved "
            "project, so success criteria, test hypotheses, test variables / "
            "conditions and measurement methods cannot be shown or changed from "
            "this page. Nothing was changed."),
        "ar": (
            "خطة النموذج الأولي والاختبار الحالية غير متاحة من هذا المشروع المحفوظ، "
            "لذلك لا يمكن عرض معايير النجاح وفرضيات الاختبار ومتغيّرات / شروط "
            "الاختبار وطرق القياس أو تغييرها من هذه الصفحة. لم يتم تغيير أي شيء."),
    },
    "UI_SC_ERR_CRITERIA_UNAVAILABLE": {
        "en": (
            "Your saved success criteria, test hypotheses, test variables / "
            "conditions and measurement methods could not be read, so they cannot "
            "be shown or changed from this page. Nothing was changed."),
        "ar": (
            "تعذّرت قراءة معايير النجاح وفرضيات الاختبار ومتغيّرات / شروط الاختبار "
            "وطرق القياس المحفوظة، لذلك لا يمكن عرضها أو تغييرها من هذه الصفحة. لم "
            "يتم تغيير أي شيء."),
    },
    "UI_SC_ERR_NOT_SAVED": {
        "en": (
            "Your success criteria, test hypotheses, test variables / conditions "
            "and measurement methods could not be saved just now. Nothing was "
            "changed."),
        "ar": (
            "تعذّر حفظ معايير النجاح وفرضيات الاختبار ومتغيّرات / شروط الاختبار "
            "وطرق القياس الآن. لم يتم تغيير أي شيء."),
    },
    "UI_SC_ERR_SAVED_NOT_SHOWN": {
        "en": (
            "Your success criteria, test hypotheses, test variables / conditions "
            "and measurement methods were saved to your project, but this page "
            "could not show them. Reload this page to see what your project holds."),
        "ar": (
            "تم حفظ معايير النجاح وفرضيات الاختبار ومتغيّرات / شروط الاختبار وطرق "
            "القياس في مشروعك، لكن تعذّر عرضها في هذه الصفحة. أعد تحميل الصفحة "
            "لرؤية ما يحفظه مشروعك."),
    },
    # CORRECTION-01 (F-04): the durable outcome of a failed write could not be
    # established — neither a save nor a rollback is asserted.
    "UI_SC_ERR_OUTCOME_UNKNOWN": {
        "en": (
            "We could not confirm whether your success criteria, test hypotheses, "
            "test variables / conditions and measurement methods were saved. Reload "
            "this page to see what your project currently holds before entering "
            "them again."),
        "ar": (
            "لم نتمكن من التأكد مما إذا كانت معايير النجاح وفرضيات الاختبار "
            "ومتغيّرات / شروط الاختبار وطرق القياس قد حُفظت. أعد تحميل هذه الصفحة "
            "لرؤية ما يحفظه مشروعك حاليًا قبل إدخالها مرة أخرى."),
    },
    # Stage 19 / CAP-09 SLICE-02 — the inventor-written measurement method.
    "UI_SC_ERR_METHOD_TOO_LONG": {
        "en": "A measurement method exceeds the 1000-character limit. No changes were saved.",
        "ar": "تتجاوز إحدى طرق القياس الحد الأقصى البالغ 1000 حرف. لم يتم حفظ أي تغييرات.",
    },
    "UI_SC_METHOD_INTRO": {
        "en": ("You may also describe one measurement method for each experiment: "
               "how you plan to measure or check it, in your own words. It is your "
               "plan only — not a measurement, a test result or evidence — and "
               "saving it does not validate, demonstrate, or approve anything."),
        "ar": ("يمكنك أيضًا وصف طريقة قياس واحدة لكل تجربة: كيف تخطط لقياسها أو "
               "التحقق منها، بكلماتك الخاصة. إنها خطتك فقط — وليست قياسًا ولا نتيجة "
               "اختبار ولا دليلًا — ولا يُعدّ حفظها إثباتًا لأي شيء أو برهانًا عليه "
               "أو موافقةً عليه."),
    },
    "UI_SC_METHOD_LABEL": {
        "en": "Measurement method (how you will measure or check it):",
        "ar": "طريقة القياس (كيف ستقيس ذلك أو تتحقق منه):",
    },
    "UI_SC_METHOD_PLACEHOLDER": {
        "en": "Optional — describe how you plan to measure or check this experiment.",
        "ar": "اختياري — صِف كيف تخطط لقياس هذه التجربة أو التحقق منها.",
    },
    "UI_SC_METHOD_STALE": {
        "en": ("A previously entered measurement method no longer matches a current "
               "proposed experiment. It has been preserved but is not applied."),
        "ar": ("لم تعد إحدى طرق القياس المُدخلة سابقًا مطابقة لتجربة مقترحة حالية. "
               "تم الاحتفاظ بها لكنها غير مطبّقة."),
    },
    "UI_DELIV_METHOD_DEFINED": {
        "en": "Measurement method — user-defined:",
        "ar": "طريقة القياس — مُعرَّفة من المستخدم:",
    },
    "UI_DELIV_METHOD_ABSENT_LABEL": {"en": "Measurement method:", "ar": "طريقة القياس:"},
    "UI_DELIV_METHOD_ABSENT": {
        "en": "Not yet described by you.",
        "ar": "لم تَصِفها بعد.",
    },
    # Stage 19 / CAP-09 SLICE 3 — the inventor-written test hypothesis: what the
    # inventor expects to happen. Planning metadata only; never a result,
    # evidence, validation or a readiness input.
    "UI_SC_ERR_HYPOTHESIS_TOO_LONG": {
        "en": "A test hypothesis exceeds the 1000-character limit. No changes were saved.",
        "ar": "تتجاوز إحدى فرضيات الاختبار الحد الأقصى البالغ 1000 حرف. لم يتم حفظ أي تغييرات.",
    },
    "UI_SC_HYPOTHESIS_INTRO": {
        "en": ("You may also state one test hypothesis for each experiment: what "
               "you expect to happen in this test, in your own words. Recording a "
               "hypothesis does not make it correct or validated — it is your "
               "expectation only, not a test result or evidence."),
        "ar": ("يمكنك أيضًا صياغة فرضية اختبار واحدة لكل تجربة: ما تتوقع أن يحدث في "
               "هذا الاختبار، بكلماتك الخاصة. تسجيل الفرضية لا يجعلها صحيحة ولا "
               "مُتحقَّقًا منها — إنها توقّعك فقط، وليست نتيجة اختبار ولا دليلًا."),
    },
    "UI_SC_HYPOTHESIS_LABEL": {
        "en": "Test hypothesis (what you expect to happen):",
        "ar": "فرضية الاختبار (Test Hypothesis) — ما تتوقع أن يحدث:",
    },
    "UI_SC_HYPOTHESIS_PLACEHOLDER": {
        "en": "Optional — state what you expect to happen in this test.",
        "ar": "اختياري — اذكر ما تتوقع أن يحدث في هذا الاختبار.",
    },
    "UI_SC_HYPOTHESIS_STALE": {
        "en": ("A previously entered test hypothesis no longer matches a current "
               "proposed experiment. It has been preserved but is not applied."),
        "ar": ("لم تعد إحدى فرضيات الاختبار المُدخلة سابقًا مطابقة لتجربة مقترحة "
               "حالية. تم الاحتفاظ بها لكنها غير مطبّقة."),
    },
    "UI_DELIV_HYPOTHESIS_DEFINED": {
        "en": "Test hypothesis — user-defined (your expectation, not a result):",
        "ar": "فرضية الاختبار — مُعرَّفة من المستخدم (توقّعك، وليست نتيجة):",
    },
    "UI_DELIV_HYPOTHESIS_ABSENT_LABEL": {
        "en": "Test hypothesis:",
        "ar": "فرضية الاختبار:",
    },
    "UI_DELIV_HYPOTHESIS_ABSENT": {
        "en": "Not yet stated by you.",
        "ar": "لم تذكرها بعد.",
    },
    # Stage 19 / CAP-09 SLICE 4 — the inventor-written test variable / condition:
    # what the inventor plans to change or compare in one experiment. ONE
    # free-text planning field; never a formal variable model, a result,
    # evidence, validation or a readiness input.
    "UI_SC_ERR_VARIABLE_TOO_LONG": {
        "en": "A test variable / condition exceeds the 1000-character limit. No changes were saved.",
        "ar": "يتجاوز أحد متغيّرات / شروط الاختبار الحد الأقصى البالغ 1000 حرف. لم يتم حفظ أي تغييرات.",
    },
    "UI_SC_VARIABLE_INTRO": {
        "en": ("You may also describe one test variable / condition for each "
               "experiment: what you will change, compare or set differently in "
               "that test, in your own words. It is your plan only — not a result "
               "or evidence — and it is not checked, graded or treated as a formal "
               "experimental design."),
        "ar": ("يمكنك أيضًا وصف متغيّر / شرط اختبار واحد لكل تجربة: ما الذي ستغيّره "
               "أو تقارنه أو تضبطه بشكل مختلف في ذلك الاختبار، بكلماتك الخاصة. إنه "
               "خطتك فقط — وليس نتيجة ولا دليلًا — ولا يُراجَع أو يُقيَّم أو يُعامَل "
               "كتصميم تجريبي رسمي."),
    },
    "UI_SC_VARIABLE_LABEL": {
        "en": "Test variable / condition (what will you change or compare in this test?):",
        "ar": ("متغيّر / شرط الاختبار (Test Variable / Condition) — ما الذي "
               "ستغيّره أو تقارنه في هذا الاختبار؟"),
    },
    "UI_SC_VARIABLE_PLACEHOLDER": {
        "en": "Optional — for example, compare two thicknesses, or run at low and high voltage.",
        "ar": "اختياري — مثلًا: قارن بين سماكتين، أو اختبر عند جهد منخفض وجهد مرتفع.",
    },
    "UI_SC_VARIABLE_NOT_RESULT": {
        "en": "This is what you plan to vary or compare, not the result.",
        "ar": "هذا ما تخطط لتغييره أو مقارنته، وليس النتيجة.",
    },
    "UI_SC_VARIABLE_STALE": {
        "en": ("A previously entered test variable / condition no longer matches a "
               "current proposed experiment. It has been preserved but is not applied."),
        "ar": ("لم يعد أحد متغيّرات / شروط الاختبار المُدخلة سابقًا مطابقًا لتجربة "
               "مقترحة حالية. تم الاحتفاظ به لكنه غير مطبّق."),
    },
    "UI_DELIV_VARIABLE_DEFINED": {
        "en": "Test variable / condition — user-defined (what you plan to change or compare):",
        "ar": "متغيّر / شرط الاختبار — مُعرَّف من المستخدم (ما تخطط لتغييره أو مقارنته):",
    },
    "UI_DELIV_VARIABLE_ABSENT_LABEL": {
        "en": "Test variable / condition:",
        "ar": "متغيّر / شرط الاختبار:",
    },
    "UI_DELIV_VARIABLE_ABSENT": {
        "en": "Nothing entered yet.",
        "ar": "لم تُدخِل شيئًا بعد.",
    },

    # --- PVCG-R4 explicit correction / withdrawal (web/app.py correct_answer) --
    # Storage stays English; only display localises — the UI_B_SC_007/008
    # pattern. Fail-closed and success wording are both registered so the
    # correction path is EN/AR equivalent end to end (PVCG-R4-C §13 E-1).
    "UI_B_CORRECT_001": {
        "en": "That correction could not be applied just now. Nothing was changed.",
        "ar": "تعذّر تطبيق هذا التصحيح الآن. لم يتم تغيير أي شيء.",
    },
    "UI_B_CORRECT_002": {
        "en": "Select which of your earlier answers to withdraw, and enter the corrected answer.",
        "ar": "اختر أي إجابة سابقة تريد سحبها، ثم اكتب الإجابة المصحّحة.",
    },
    # The closing clause is deliberately CONDITIONAL ("whenever ... can be"),
    # never "on the next load": a project at MAX_ACCEPTED_ANSWER_REPLAY crosses
    # the bound when the correction append takes the stream to limit + 1, and
    # every later reconstruction then fails, so an unconditional promise would
    # be false. Both languages carry the same conditional force.
    "UI_B_CORRECT_004": {
        "en": ("Your correction was saved, but the page could not be updated just now. "
               "What you see below has not changed yet. The saved correction will be "
               "reflected whenever this project can be rebuilt successfully."),
        "ar": ("تم حفظ تصحيحك، لكن تعذّر تحديث الصفحة الآن. "
               "وما تراه بالأسفل لم يتغيّر بعد. وسيظهر أثر التصحيح المحفوظ "
               "متى أمكن إعادة بناء المشروع بنجاح."),
    },
    "UI_B_CORRECT_003": {
        "en": ("Your earlier answer was withdrawn and kept in the project history. "
               "Everything shown has been recomputed from your remaining answers."),
        "ar": ("تم سحب إجابتك السابقة مع الاحتفاظ بها في سجل المشروع. "
               "وأُعيد حساب كل ما يظهر هنا من إجاباتك المتبقية."),
    },

    # --- login.html (Category A) ----------------------------------------------
    "UI_A_LOGIN_001": {"en": "Sign in", "ar": "تسجيل الدخول"},
    "UI_A_LOGIN_002": {"en": "Email address", "ar": "البريد الإلكتروني"},
    "UI_A_LOGIN_003": {"en": "Password", "ar": "كلمة المرور"},
    "UI_A_LOGIN_004": {"en": "Forgot your password?", "ar": "هل نسيت كلمة المرور؟"},
    "UI_A_LOGIN_005": {"en": "Create an account", "ar": "إنشاء حساب"},
    "UI_A_MSG_LOGIN": {
        "en": "Those sign-in details did not match. Please try again.",
        "ar": "بيانات تسجيل الدخول غير متطابقة. يرجى المحاولة مرة أخرى.",
    },

    # --- register.html (Category A) -------------------------------------------
    "UI_A_REG_001": {"en": "Create your account", "ar": "أنشئ حسابك"},
    "UI_A_REG_002": {
        "en": ("Registering creates an account and sends an email verification "
               "code. You are not signed in yet, and this does not create or save "
               "a project."),
        "ar": ("إنشاء حساب يرسل رمز تحقق إلى بريدك الإلكتروني. لن يتم تسجيل دخولك "
               "بعد، ولا يؤدي ذلك إلى إنشاء مشروع أو حفظه."),
    },
    "UI_A_REG_003": {
        "en": "Back to the registration form",
        "ar": "العودة إلى نموذج التسجيل",
    },
    "UI_A_REG_004": {
        "en": "Please enter a valid email address.",
        "ar": "يرجى إدخال عنوان بريد إلكتروني صالح.",
    },
    "UI_A_REG_005": {
        "en": "Password must be at least 12 characters.",
        "ar": "يجب أن تتكوّن كلمة المرور من 12 حرفًا على الأقل.",
    },
    "UI_A_REG_006": {
        "en": "The two passwords do not match.",
        "ar": "كلمتا المرور غير متطابقتين.",
    },
    "UI_A_REG_007": {
        "en": "Password (at least 12 characters)",
        "ar": "كلمة المرور (12 حرفًا على الأقل)",
    },
    "UI_A_REG_008": {"en": "Confirm password", "ar": "تأكيد كلمة المرور"},
    "UI_A_REG_009": {"en": "Create account", "ar": "إنشاء حساب"},
    # ATTEMPT-TRUTHFUL (OD-INFRA-6). Was: "verification instructions have been
    # sent." / "فسيتم إرسال تعليمات التحقق." Those asserted an external delivery
    # the application cannot know: a configured provider can reject or be
    # unreachable, and that failure is swallowed so the response stays identical
    # for every address. This wording is true under every outcome and remains ONE
    # constant string, so non-enumeration is preserved.
    "UI_A_MSG_REGISTER": {
        # OD-INFRA-6 outbox: the request records the message and sends nothing,
        # so "queued for delivery" is the exact truth at response time.
        "en": ("If the address can be used, a verification message has been "
               "queued for delivery to it. If nothing arrives shortly, request "
               "a new message."),
        "ar": ("إذا كان بالإمكان استخدام هذا العنوان، فقد تمت جدولة رسالة تحقق "
               "للإرسال إليه. إذا لم تصل أي رسالة قريبًا، فاطلب رسالة جديدة."),
    },

    # --- reset.html (Category A) ----------------------------------------------
    "UI_A_RESET_001": {"en": "Set a new password", "ar": "تعيين كلمة مرور جديدة"},
    "UI_A_RESET_002": {
        "en": ("Your password has been reset. All previous sessions have been "
               "signed out. Please sign in with your new password."),
        "ar": ("تمت إعادة تعيين كلمة المرور. تم تسجيل الخروج من جميع الجلسات "
               "السابقة. يرجى تسجيل الدخول بكلمة المرور الجديدة."),
    },
    "UI_A_RESET_003": {"en": "Go to sign in", "ar": "الذهاب إلى تسجيل الدخول"},
    "UI_A_RESET_004": {
        "en": "This reset link is invalid, has expired, or has already been used.",
        "ar": "رابط إعادة التعيين هذا غير صالح أو منتهي الصلاحية أو تم استخدامه من قبل.",
    },
    "UI_A_RESET_005": {
        "en": "New password (at least 12 characters)",
        "ar": "كلمة المرور الجديدة (12 حرفًا على الأقل)",
    },
    "UI_A_RESET_006": {
        "en": "Confirm new password",
        "ar": "تأكيد كلمة المرور الجديدة",
    },
    "UI_A_RESET_007": {"en": "Set new password", "ar": "تعيين كلمة المرور الجديدة"},

    # --- recover.html (Category A) --------------------------------------------
    "UI_A_RECOVER_001": {"en": "Reset your password", "ar": "إعادة تعيين كلمة المرور"},
    "UI_A_RECOVER_002": {"en": "Back to sign in", "ar": "العودة إلى تسجيل الدخول"},
    "UI_A_RECOVER_003": {
        "en": ("Enter your email address and we will send password-reset "
               "instructions if it matches an account."),
        "ar": ("أدخل بريدك الإلكتروني وسنرسل تعليمات إعادة التعيين إذا كان مطابقًا "
               "لحساب."),
    },
    "UI_A_RECOVER_004": {
        "en": "Send reset instructions",
        "ar": "إرسال تعليمات إعادة التعيين",
    },
    # ATTEMPT-TRUTHFUL (OD-INFRA-6), same reasoning as UI_A_MSG_REGISTER.
    # Was: "password-reset instructions have been sent." / "فقد أُرسلت ...".
    "UI_A_MSG_RECOVER": {
        "en": ("If that address matches an account, a password-reset message "
               "has been queued for delivery to it. If nothing arrives shortly, "
               "request a new message."),
        "ar": ("إذا كان هذا العنوان مطابقًا لحساب، فقد تمت جدولة رسالة إعادة "
               "تعيين كلمة المرور للإرسال إليه. إذا لم تصل أي رسالة قريبًا، "
               "فاطلب رسالة جديدة."),
    },

    # --- verify_result.html (Category A) --------------------------------------
    "UI_A_VERIFY_001": {"en": "Email verified", "ar": "تم التحقق من البريد"},
    "UI_A_VERIFY_002": {
        "en": "Your email address has been verified.",
        "ar": "تم التحقق من عنوان بريدك الإلكتروني.",
    },
    "UI_A_VERIFY_003": {"en": "Verification unavailable", "ar": "التحقق غير متاح"},
    "UI_A_VERIFY_004": {
        "en": "This verification link is invalid, has expired, or has already been used.",
        "ar": "رابط التحقق هذا غير صالح أو منتهي الصلاحية أو تم استخدامه من قبل.",
    },

    # --- account.html (Category A) --------------------------------------------
    "UI_A_ACCOUNT_001": {"en": "Signed in", "ar": "تم تسجيل الدخول"},
    "UI_A_ACCOUNT_002": {"en": "Signed in as", "ar": "مسجّل الدخول باسم"},
    "UI_A_ACCOUNT_003": {
        "en": "Your email is verified.",
        "ar": "تم التحقق من بريدك الإلكتروني.",
    },
    "UI_A_ACCOUNT_004": {
        "en": "Your email is not verified yet. Check your email for the verification link.",
        "ar": "لم يتم التحقق من بريدك بعد. تحقق من بريدك للحصول على رابط التحقق.",
    },
    "UI_A_ACCOUNT_005": {"en": "Resend verification", "ar": "إعادة إرسال التحقق"},
    "UI_A_ACCOUNT_006": {"en": "Your projects", "ar": "مشاريعك"},
    "UI_A_ACCOUNT_007": {"en": "Open project", "ar": "فتح المشروع"},
    "UI_A_ACCOUNT_008": {
        "en": "You have no account-owned projects yet.",
        "ar": "لا توجد لديك مشاريع مملوكة للحساب بعد.",
    },
    "UI_A_ACCOUNT_009": {"en": "Sign out", "ar": "تسجيل الخروج"},
    "UI_A_ACCOUNT_010": {
        "en": "Sign out of all sessions",
        "ar": "تسجيل الخروج من كل الجلسات",
    },
    # P10-D3a: truthful PROJECT-SCOPED export label (contract §5). Deliberately
    # names one project only — never "my data" / "account" / "all my data".
    "UI_A_ACCOUNT_012": {"en": "Export project", "ar": "تصدير بيانات المشروع"},
    # P10-D3b: truthful DEACTIVATION vocabulary (contract §4). Deliberately says
    # deactivate/disable — never delete/erase; data is explicitly NOT removed.
    "UI_A_DEACT_001": {"en": "Deactivate Account", "ar": "تعطيل الحساب"},
    "UI_A_DEACT_002": {
        "en": ("Deactivating disables sign-in for this account. Your projects "
               "and account data are not removed."),
        "ar": ("تعطيل الحساب يوقف تسجيل الدخول إلى هذا الحساب. لا تتم إزالة "
               "مشاريعك وبيانات حسابك."),
    },
    "UI_A_DEACT_003": {"en": "Current password", "ar": "كلمة المرور الحالية"},
    "UI_A_DEACT_004": {
        "en": ("Account deactivation was not performed. Please check your "
               "password and try again."),
        "ar": ("لم يتم تعطيل الحساب. يرجى التحقق من كلمة المرور والمحاولة "
               "مرة أخرى."),
    },
    "UI_A_DEACT_005": {
        "en": "Your account has been deactivated. Sign-in is now disabled for it.",
        "ar": "تم تعطيل حسابك. تسجيل الدخول إليه معطّل الآن.",
    },
    "UI_A_ACCOUNT_011": {
        "en": ("Signing in manages your account only. It does not save, own, or "
               "move any project to your account — projects remain accessed by "
               "their session link on this device."),
        "ar": ("تسجيل الدخول يدير حسابك فقط. لا يحفظ أي مشروع في حسابك ولا يملكه "
               "ولا ينقله؛ تبقى المشاريع متاحة عبر رابط الجلسة على هذا الجهاز."),
    },
    # The AUTHENTICATED resend surface keeps its conditional success wording: it
    # is now shown only when a message was actually accepted, or when
    # verification was no longer needed (then the conditional is vacuous). The
    # signed-in identity is already known to the caller, so a truthful outcome
    # here is not an account-existence oracle.
    "UI_A_MSG_RESEND": {
        "en": ("If verification is still needed, a new verification message has "
               "been queued for delivery."),
        "ar": "إذا كان التحقق لا يزال مطلوبًا، فقد تمت جدولة رسالة تحقق جديدة للإرسال.",
    },
    # Shown when nothing went out: a provider rejection or outage, a rate limit,
    # or a non-active account. It names no provider, no reason and no token.
    "UI_A_MSG_RESEND_FAILED": {
        "en": ("A new verification message could not be sent just now. "
               "Please try again in a few minutes."),
        "ar": ("لم يتمكن النظام من إرسال رسالة تحقق جديدة الآن. "
               "يرجى المحاولة مرة أخرى بعد بضع دقائق."),
    },
    "UI_A_SESSION_BANNER": {
        "en": "Project saved to your account.",
        "ar": "تم حفظ المشروع في حسابك.",
    },

    # --- session.html chrome (Category B) -------------------------------------
    "UI_B_SESSION_001": {"en": "Next Development Step", "ar": "خطوة التطوير التالية"},
    "UI_B_SESSION_002": {"en": "Do next:", "ar": "الخطوة التالية:"},
    "UI_B_SESSION_003": {"en": "Reference:", "ar": "المرجع:"},
    # Increment-3 generated-output language disclosure (Owner decision, Option B:
    # generated substantive content stays English by rule; the surrounding
    # interface and this disclosure follow the selected UI language). Shared by
    # the session callout and Deliverable Section 12; it translates NO generated
    # content and asserts nothing about the content itself.
    "UI_B_GENOUT_DISCLOSURE": {
        "en": ("Generated substantive content is intentionally presented in "
               "English; the surrounding interface is localized."),
        "ar": ("يُعرض المحتوى الجوهري المُولَّد عمدًا باللغة الإنجليزية؛ أما واجهة "
               "الاستخدام المحيطة فمترجمة."),
    },
    "UI_B_SESSION_004": {
        "en": "View FDC-001 Deliverable",
        "ar": "عرض مُخرَج FDC-001",
    },
    "UI_B_SESSION_005": {
        "en": "View In-Progress Assessment Snapshot",
        "ar": "عرض لقطة التقييم قيد التقدم",
    },
    "UI_B_SESSION_006": {
        "en": "What You Have Marked as Not Yet Known",
        "ar": "ما وضعتَ علامة عليه بأنه غير معروف بعد",
    },
    "UI_B_SESSION_007": {
        "en": ("These items remain open for later clarification. Recording an "
               "unknown does not resolve it."),
        "ar": ("تبقى هذه العناصر مفتوحة لتوضيحها لاحقًا. تسجيل أمر غير معروف لا "
               "يحلّه."),
    },
    "UI_B_SESSION_008": {"en": "Idea:", "ar": "الفكرة:"},
    "UI_B_SESSION_009": {"en": "Iteration:", "ar": "التكرار:"},
    "UI_B_SESSION_010": {"en": "Review type:", "ar": "نوع المراجعة:"},
    "UI_B_SESSION_011A": {"en": "Progress — Stage ", "ar": "التقدّم — المرحلة "},
    "UI_B_SESSION_011B": {"en": " of 3", "ar": " من 3"},
    "UI_B_SESSION_012": {"en": "Your Progress Areas", "ar": "مجالات تقدّمك"},
    "UI_B_SESSION_013": {"en": "ACTIVE", "ar": "نشط"},
    "UI_B_SESSION_014": {"en": "DONE", "ar": "منجز"},
    "UI_B_SESSION_015": {"en": "UPCOMING", "ar": "قادم"},
    "UI_B_SESSION_016": {"en": "◄ now", "ar": "◄ الآن"},
    "UI_B_SESSION_017": {"en": "Good progress", "ar": "تقدّم جيد"},
    "UI_B_SESSION_018": {"en": "More detail needed", "ar": "يلزم مزيد من التفاصيل"},
    "UI_B_SESSION_019": {"en": "Not enough to continue", "ar": "غير كافٍ للمتابعة"},
    "UI_B_SESSION_020": {"en": "Response recorded", "ar": "تم تسجيل الرد"},
    "UI_B_SESSION_021": {"en": "Result details", "ar": "تفاصيل النتيجة"},
    "UI_B_SESSION_022": {"en": "Direction:", "ar": "الاتجاه:"},
    "UI_B_SESSION_023": {"en": "Current question", "ar": "السؤال الحالي"},
    "UI_B_SESSION_024": {"en": "Currently addressing:", "ar": "يجري تناول:"},
    "UI_B_SESSION_025": {
        "en": "Answer in the box below, or choose one of the response options.",
        "ar": "أجب في المربع أدناه، أو اختر أحد خيارات الرد.",
    },
    # Bounded assessment/progression limitation, disclosed beside the answer
    # box it concerns (Owner decision: accept the known residual and disclose
    # it). It says only what is true of the shipped rules: assessment and
    # progression are fixed automated language rules, wording can be read
    # differently at similar meaning, and rephrasing is the user's recourse.
    # It does NOT say any language is less reliable than another, does NOT
    # claim the limitation is solved, and does NOT put the cause on the user.
    "UI_ASSESSMENT_WORDING_NOTE": {
        "en": ("InventorAI uses fixed automated language rules to assess answers "
               "and decide progress. Wording can sometimes be read differently "
               "even when the intended meaning is similar. If an answer seems to "
               "be read differently from what you meant, or progress does not "
               "change as you expected, rephrase the technical meaning or add "
               "detail."),
        "ar": ("يستخدم InventorAI قواعد لغوية آلية ثابتة لتقييم الإجابات وتحديد "
               "التقدم. وقد تُقرأ بعض الصياغات بشكل مختلف حتى عندما يكون المعنى "
               "المقصود متشابهًا. وإذا بدا أن إجابتك قُرئت على غير ما قصدت، أو لم "
               "يتغيّر التقدم كما توقعت، فأعد صياغة المعنى الفني أو أضف تفصيلًا."),
    },
    "UI_B_SESSION_026": {
        "en": "Help me understand this question",
        "ar": "ساعدني على فهم هذا السؤال",
    },
    "UI_B_SESSION_027": {"en": "System guidance", "ar": "إرشاد النظام"},
    "UI_B_SESSION_028": {"en": "What would help:", "ar": "ما الذي سيساعد:"},
    "UI_B_SESSION_029": {
        "en": "A good answer looks like:",
        "ar": "الإجابة الجيدة تبدو هكذا:",
    },
    "UI_B_SESSION_030": {"en": "Optional guidance", "ar": "إرشاد اختياري"},
    "UI_B_SESSION_031": {"en": "Your answer", "ar": "إجابتك"},
    "UI_B_SESSION_032": {
        "en": "Describe your thinking here, or pick an option below...",
        "ar": "صف تفكيرك هنا، أو اختر خيارًا أدناه...",
    },
    "UI_B_SESSION_033": {
        "en": "How do you want to respond?",
        "ar": "كيف تريد أن تردّ؟",
    },
    "UI_B_SESSION_034": {"en": "Submit", "ar": "إرسال"},
    # RVR-1 (Wave-1): accept-as-known-risk affordance. Truthful copy — accepted
    # is never presented as resolved or validated.
    "UI_RVR1_RISK_HEADING": {
        "en": "Accept this as a known risk",
        "ar": "قبول هذا كمخاطرة معروفة"},
    "UI_RVR1_RISK_EXPLAIN": {
        "en": ("If you honestly cannot resolve this now, you can accept it as a "
               "known risk. It will stay visible as an unresolved, unvalidated "
               "risk in your assessment - accepting is not resolving - and the "
               "journey moves on to the next area."),
        "ar": ("إذا كنت لا تستطيع بصدق حسم هذا الأمر الآن، يمكنك قبوله كمخاطرة "
               "معروفة. سيبقى ظاهرًا كمخاطرة غير محسومة وغير مُتحقق منها في "
               "تقييمك — القبول ليس حلًا — وتنتقل الرحلة إلى المجال التالي.")},
    "UI_RVR1_RISK_CONFIRM": {
        "en": ("I understand this stays an unresolved known risk and is not "
               "resolved or validated."),
        "ar": ("أفهم أن هذا يبقى مخاطرة معروفة غير محسومة، وأنه غير محلول وغير "
               "مُتحقق منه.")},
    "UI_RVR1_RISK_REASON": {
        "en": "Optional: why you are accepting this risk",
        "ar": "اختياري: لماذا تقبل هذه المخاطرة"},
    "UI_RVR1_RISK_BUTTON": {
        "en": "Accept as known risk",
        "ar": "قبول كمخاطرة معروفة"},
    # RVR-5 (Wave-1): rendered correction affordance over the existing route.
    # W2-D (Wave-2 contract §K, W1-N4) — correction-lapse transparency notice.
    # Platform UI chrome under the existing governed EN/AR catalog mechanism
    # (current localization infrastructure, NOT RVR-7 / Arabic substantive
    # parity, which remains Wave-3 and unauthorized).
    "UI_W2D_LAPSE_HEADING": {
        "en": "A previous risk acceptance no longer applies",
        "ar": "قبول سابق للمخاطرة لم يعد ساريًا"},
    "UI_W2D_LAPSE_EXPLAIN": {
        "en": ("Your correction changed the recorded evidence, so everything "
               "was deterministically re-evaluated. A risk you had accepted "
               "earlier could not be carried over to the corrected state. "
               "Nothing was deleted - the original acceptance stays in your "
               "project history."),
        "ar": ("غيّر تصحيحُك الأدلة المسجّلة، فأُعيد تقييم كل شيء بشكل حتمي. "
               "مخاطرة كنت قد قبلتها سابقًا تعذّر نقلها إلى الحالة المصحّحة. "
               "لم يُحذف شيء — يبقى القبول الأصلي في سجل مشروعك.")},
    "UI_W2D_LAPSE_ACTION": {
        "en": ("No longer covered - will need a new answer or a new explicit "
               "decision when it is asked again:"),
        "ar": ("لم يعد مشمولًا — سيتطلب إجابة جديدة أو قرارًا صريحًا جديدًا "
               "عند طرحه مجددًا:")},
    "UI_W2D_LAPSE_RESOLVED": {
        "en": ("Resolved by your corrected answers - no further action "
               "needed:"),
        "ar": "حُلّ بفضل إجاباتك المصحّحة — لا حاجة لإجراء آخر:"},
    # --- W2-A / RVR-4 decision capture (authoritative contract §14/§15) ---
    # Governed EN/AR pairs for W2-A's OWN new UI only (no RVR-7 expansion);
    # single-language rendering via the existing t()/ui_lang mechanism.
    "UI_W2A_SECTION_HEADING": {
        "en": "Decision capture",
        "ar": "تسجيل القرارات"},
    "UI_W2A_SECTION_EXPLAIN": {
        "en": ("Declare a technical decision you are working through, list the "
               "alternatives you are considering, and refine or withdraw them "
               "as your thinking evolves. Everything is kept in your project "
               "history and rebuilt exactly on reload."),
        "ar": ("سجّل قرارًا تقنيًا تعمل عليه، واذكر البدائل التي تفكّر فيها، "
               "وحسّنها أو اسحبها مع تطوّر تفكيرك. يُحفظ كل شيء في سجل مشروعك "
               "ويُعاد بناؤه بدقة عند إعادة التحميل.")},
    "UI_W2A_DECLARE_CONTEXT_LABEL": {
        "en": "Declare a decision to work on (state it as a question)",
        "ar": "سجّل قرارًا للعمل عليه (صِغه كسؤال)"},
    "UI_W2A_DECLARE_CONTEXT_BUTTON": {
        "en": "Declare decision",
        "ar": "تسجيل القرار"},
    "UI_W2A_QUESTION_LABEL": {
        "en": "Decision question",
        "ar": "سؤال القرار"},
    "UI_W2A_ALTERNATIVES_LABEL": {
        "en": "Alternatives under consideration",
        "ar": "البدائل قيد الدراسة"},
    "UI_W2A_NO_ALTERNATIVES": {
        "en": "No active alternatives yet.",
        "ar": "لا توجد بدائل نشطة بعد."},
    "UI_W2A_DECLARE_ALT_LABEL": {
        "en": "Add an alternative",
        "ar": "أضف بديلًا"},
    "UI_W2A_DECLARE_ALT_BUTTON": {
        "en": "Add alternative",
        "ar": "إضافة البديل"},
    "UI_W2A_REFINE_LABEL": {
        "en": "Refine this alternative (keeps its identity and history)",
        "ar": "حسّن هذا البديل (يحافظ على هويته وسجله)"},
    "UI_W2A_REFINE_BUTTON": {
        "en": "Refine",
        "ar": "تحسين"},
    "UI_W2A_WITHDRAW_LABEL": {
        "en": "Withdraw this alternative (kept in project history)",
        "ar": "اسحب هذا البديل (يبقى في سجل المشروع)"},
    "UI_W2A_WITHDRAW_BUTTON": {
        "en": "Withdraw",
        "ar": "سحب"},
    "UI_W2A_READINESS_NOTE": {
        "en": ("Comparison has not started: these alternatives are recorded, "
               "and the inputs needed to compare them can be added at a later "
               "stage. This is the expected state for a newly declared "
               "decision - not a problem with your idea."),
        "ar": ("لم تبدأ المقارنة بعد: هذه البدائل مسجّلة، ويمكن إضافة المدخلات "
               "اللازمة لمقارنتها في مرحلة لاحقة. هذه هي الحالة المتوقعة لقرار "
               "مسجّل حديثًا — وليست مشكلة في فكرتك.")},
    "UI_W2A_DELIV_HEADING": {
        "en": "Recorded decision state",
        "ar": "حالة القرارات المسجّلة"},
    # --- G-3 bounded decision-value repair (authoritative contract PR #598;
    # Owner decisions OD-G3-1-WITHDRAWAL / OD-G3-2-REFINEMENT, PR #599).
    # Governed EN/AR pairs for G-3's OWN new chrome only. Truthfulness rules
    # these strings are bound by: a user withdrawal is a LIFECYCLE act and is
    # never worded as an evidence-based system elimination; nothing claims a
    # comparison, ranking, winner or engineering superiority; a missing reason
    # is stated plainly and never invented.
    "UI_G3_STATE_ACTIVE": {
        "en": "still under consideration",
        "ar": "ما زال قيد الدراسة"},
    "UI_G3_STATE_WITHDRAWN": {
        "en": "withdrawn by you",
        "ar": "سحبتَه بنفسك"},
    "UI_G3_REASON_LABEL": {
        "en": "Your reason",
        "ar": "سببك"},
    "UI_G3_REASON_NOT_RECORDED": {
        "en": "No reason was recorded with this withdrawal.",
        "ar": "لم يُسجَّل أي سبب مع هذا السحب."},
    # Renders the derived `candidate_not_yet_comparable` blocking reason. It
    # must stay truthful ALONGSIDE UI_G3_EVIDENCE_RECORDED: what the inventor
    # writes about an alternative is their own description and is deliberately
    # NOT decision-evidence (D-G3-2), so "you recorded detail" and "not yet
    # comparable" are both true at once and the string must say why.
    "UI_G3_NOT_COMPARABLE": {
        "en": ("Not yet comparable: what you have written about this "
               "alternative is kept as your own description of it, not as "
               "comparison input, so no comparison can use it yet."),
        "ar": ("غير قابل للمقارنة بعد: ما كتبتَه عن هذا البديل محفوظ بوصفه "
               "وصفك أنت له، لا كمُدخل للمقارنة، لذلك لا يمكن لأي مقارنة أن "
               "تستخدمه بعد.")},
    "UI_G3_EVIDENCE_NONE": {
        "en": "Nothing recorded about it yet",
        "ar": "لم يُسجَّل عنه شيء بعد"},
    "UI_G3_EVIDENCE_RECORDED": {
        "en": "You have recorded detail about it",
        "ar": "لقد سجّلت تفاصيل عنه"},
    "UI_G3_WITHDRAW_REASON_LABEL": {
        "en": "Why are you withdrawing it? (optional)",
        "ar": "لماذا تسحبه؟ (اختياري)"},
    "UI_G3_HISTORY_NOTE": {
        "en": ("Alternatives you withdrew stay listed here so your own "
               "history remains complete. A withdrawn alternative takes no "
               "part in comparison, and withdrawing one is your decision "
               "about direction - it is not a judgement that the alternative "
               "would not work."),
        "ar": ("تبقى البدائل التي سحبتَها مدرجة هنا كي يظل سجلك كاملًا. "
               "لا يشارك البديل المسحوب في المقارنة، وسحبه قرارٌ منك بشأن "
               "الاتجاه — وليس حكمًا بأن البديل لن ينجح.")},
    "UI_W2A_ERR_001": {
        "en": ("That decision entry could not be saved just now. "
               "Nothing was changed."),
        "ar": "تعذّر حفظ هذا الإدخال القراري الآن. لم يتغيّر أي شيء."},
    # --- W2-B / RVR-6a Option-C serving cues (Contract Amendment 1 §4/§10/
    # §16, authoritative via PR #575). Governed EN/AR pairs for W2-B's OWN
    # new strings only (no RVR-7 expansion); display chrome rendered via the
    # existing t()/ui_lang mechanism. Truthfulness rule (§16): no string may
    # overstate engine behavior — never "served first", "comparable",
    # "completed", or "resolved" claims.
    "UI_W2B_CUE_RISK_NOT_REASKED": {
        "en": ("Areas you accepted as known risks are not asked again. They "
               "stay recorded as open risks, and they reopen only if a later "
               "correction lapses an acceptance."),
        "ar": ("المجالات التي قبلتَها كمخاطر معروفة لا يُعاد سؤالك عنها. "
               "تبقى مسجّلة كمخاطر قائمة، ولا يُعاد فتحها إلا إذا أبطل "
               "تصحيحٌ لاحق قبولًا سابقًا.")},
    "UI_W2B_CUE_REOPENED_LAPSE": {
        "en": ("This area is being asked again because a correction lapsed "
               "its earlier risk acceptance. The earlier acceptance stays in "
               "the project history."),
        "ar": ("يُطرح هذا المجال من جديد لأن تصحيحًا أبطل قبول المخاطرة "
               "السابق الخاص به. يبقى القبول السابق محفوظًا في سجل "
               "المشروع.")},
    "UI_W2B_CUE_CRITICAL_REPHRASED": {
        "en": ("This area is still unresolved and is what currently blocks "
               "your idea's progression, so the question has been rephrased "
               "to help you move it forward."),
        "ar": ("هذا المجال ما زال غير محسوم وهو ما يمنع تقدّم فكرتك حاليًا، "
               "لذلك أُعيدت صياغة السؤال لمساعدتك على المضي قدمًا.")},
    "UI_W2B_CUE_INTENT_SKIP": {
        "en": ("You already gave a substantive answer to the prepared "
               "question for this area, so it is not repeated word for word. "
               "Add genuinely new information or use the options below - "
               "this area is still open, not settled."),
        "ar": ("سبق أن قدّمتَ إجابة جوهرية على السؤال المعدّ لهذا المجال، "
               "لذلك لن يُكرَّر حرفيًا. أضف معلومات جديدة فعلًا أو استخدم "
               "الخيارات أدناه — هذا المجال ما زال مفتوحًا ولم يُحسم.")},
    "UI_W2B_ACTION_DECISION_EVIDENCE": {
        "en": ("You have declared more than one alternative for a decision. "
               "Recording what you know about each alternative - using the "
               "refine option in the decision section - gathers the evidence "
               "a future comparison will need. No comparison has started "
               "yet."),
        "ar": ("لقد سجّلت أكثر من بديل لقرارٍ ما. تدوين ما تعرفه عن كل "
               "بديل — عبر خيار التحسين في قسم القرارات — يجمع الأدلة التي "
               "ستحتاجها المقارنة مستقبلًا. لم تبدأ المقارنة بعد.")},
    "UI_W2B_ACTION_DECISION_LINK": {
        "en": "Go to the decision section",
        "ar": "الانتقال إلى قسم القرارات"},
    "UI_RVR5_CORRECT_HEADING": {
        "en": "Correct an earlier answer",
        "ar": "تصحيح إجابة سابقة"},
    "UI_RVR5_CORRECT_EXPLAIN": {
        "en": ("Correcting an answer keeps the original in your project "
               "history as a withdrawn record - nothing is erased - and "
               "everything shown is deterministically recomputed from your "
               "remaining answers."),
        "ar": ("تصحيح إجابة يُبقي الأصل في سجل مشروعك كإجابة مسحوبة — لا يُمحى "
               "شيء — ويُعاد حساب كل ما يُعرض بشكل حتمي من إجاباتك المتبقية.")},
    "UI_RVR5_CORRECT_SELECT": {
        "en": "Choose the answer to correct",
        "ar": "اختر الإجابة المراد تصحيحها"},
    "UI_RVR5_CORRECT_NEW": {
        "en": "Your corrected answer",
        "ar": "إجابتك المصحَّحة"},
    "UI_CORRECTION_PREVIEW_HEADING": {
        "en": "Selected recorded answer",
        "ar": "الإجابة المسجَّلة المحددة"},
    "UI_CORRECTION_PREVIEW_HELP": {
        "en": ("Read the full recorded answer before correcting it. This is your "
               "answer in this loaded view, not a verified fact. You can also "
               "expand all eligible recorded answers below."),
        "ar": ("اقرأ الإجابة المسجَّلة كاملة قبل تصحيحها. هذه إجابتك في الصفحة "
               "المحمَّلة، وليست حقيقة متحقَّقًا منها. يمكنك أيضًا توسيع قائمة "
               "الإجابات المسجَّلة المتاحة للتصحيح أدناه.")},
    "UI_CORRECTION_PREVIEW_ALL": {
        "en": "Read full recorded answers available for correction",
        "ar": "قراءة الإجابات المسجَّلة الكاملة المتاحة للتصحيح"},
    "UI_CORRECTION_PREVIEW_UPDATED": {
        "en": "Recorded-answer preview updated: {reference}.",
        "ar": "تم تحديث معاينة الإجابة المسجَّلة: {reference}."},
    "UI_RVR5_CORRECT_BUTTON": {
        "en": "Withdraw and replace this answer",
        "ar": "سحب هذه الإجابة واستبدالها"},
    "UI_RVR5_WITHDRAWN_LABEL": {
        "en": "Corrected (withdrawn) answers kept in history",
        "ar": "إجابات مصحَّحة (مسحوبة) محفوظة في السجل"},
    # RVR-5 withdrawn-source note. English is VERBATIM from the assembler constant
    # engine/deliverable_assembler.py::_WITHDRAWN_SOURCE_NOTE (parity-preserving):
    # the constant and the JSON payload stay English and unchanged, and only the
    # rendered paragraph follows the selected UI language. It states the same
    # meaning in both languages and adds no claim.
    "UI_RVR5_WITHDRAWN_NOTE": {
        "en": ("The inventor explicitly withdrew earlier answer(s). Everything "
               "shown here was recomputed from the remaining answers only; the "
               "withdrawn text is kept in the project history and is no longer "
               "used as current support. This is not a judgement that any "
               "earlier conclusion was wrong."),
        "ar": ("سحب المخترع الإجابة/الإجابات السابقة صراحةً. أُعيد حساب كل ما "
               "يظهر هنا بالاعتماد على الإجابات المتبقية فقط؛ ويظل النص المسحوب "
               "محفوظًا في سجل المشروع ولا يُستخدم بعد ذلك كدعم حالي. ولا يُعد "
               "ذلك حكمًا بأن أي استنتاج سابق كان خاطئًا."),
    },
    "UI_B_SESSION_035": {
        "en": "You have worked through the key questions for your idea.",
        "ar": "لقد عملتَ على الأسئلة الأساسية لفكرتك.",
    },
    "UI_B_SESSION_036A": {"en": "Areas still open (", "ar": "المجالات التي ما زالت مفتوحة ("},
    "UI_B_SESSION_036B": {"en": "):", "ar": "):"},
    "UI_B_SESSION_037A": {
        "en": "Areas you have addressed (",
        "ar": "المجالات التي تناولتها (",
    },
    "UI_B_SESSION_037B": {"en": ")", "ar": ")"},
    "UI_B_SESSION_038": {"en": "Start a new idea", "ar": "ابدأ فكرة جديدة"},
    "UI_B_SESSION_039": {
        "en": "Enter an answer, or choose one of the response options below.",
        "ar": "أدخل إجابة، أو اختر أحد خيارات الرد أدناه.",
    },
    "UI_B_SESSION_049": {
        "en": "That response could not be saved just now. Please try again.",
        "ar": "تعذّر حفظ هذا الرد الآن. يرجى المحاولة مرة أخرى.",
    },
    "UI_B_SESSION_040": {
        "en": "That answer could not be saved just now. Please try again.",
        "ar": "تعذّر حفظ هذه الإجابة الآن. يرجى المحاولة مرة أخرى.",
    },
    # P10-PC1: cold-load Level-1 reconstructed review-state panel. The 042
    # English sentence is the EXACT product claim authorized by the merged
    # P4-2 Level-1 gate (engine/session_reconstruction.py module contract);
    # the Arabic rendering is the same claim localized, adding no new claim.
    "UI_B_SESSION_041": {
        "en": "Saved project — read-only reconstructed review state",
        "ar": "مشروع محفوظ — حالة مراجعة مُعاد بناؤها للقراءة فقط",
    },
    "UI_B_SESSION_042": {
        "en": ("View a read-only reconstruction of this idea's current review "
               "state, recomputed from its saved inputs and accepted answers. "
               "This is not a resumed session."),
        "ar": ("اعرض إعادة بناء للقراءة فقط لحالة المراجعة الحالية لهذه الفكرة، "
               "محسوبة من مدخلاتها المحفوظة وإجاباتها المقبولة. "
               "هذه ليست جلسة مستأنفة."),
    },
    "UI_B_SESSION_043": {
        "en": "Open gaps:",
        "ar": "الفجوات المفتوحة:",
    },
    "UI_B_SESSION_044": {
        "en": "Current question (read-only):",
        "ar": "السؤال الحالي (للقراءة فقط):",
    },
    "UI_B_SESSION_045": {
        "en": "Accepted answers replayed:",
        "ar": "الإجابات المقبولة المُعاد تشغيلها:",
    },
    "UI_B_SESSION_046": {
        "en": "Answering is unavailable in this reconstructed view.",
        "ar": "الإجابة غير متاحة في هذا العرض المُعاد بناؤه.",
    },
    # P10-PC3: truthful writable-resume wording (Owner-approved semantics —
    # "reconstructed continuation", never "restored original session").
    "UI_B_SESSION_047": {
        "en": "Resumed project — reconstructed continuation",
        "ar": "تم استئناف المشروع — متابعة مُعاد بناؤها",
    },
    "UI_B_SESSION_048": {
        "en": "Resume this project and continue answering",
        "ar": "استئناف هذا المشروع ومتابعة الإجابة",
    },

    # --- deliverable.html chrome (Category B) ---------------------------------
    "UI_B_DELIV_001": {"en": "Package version:", "ar": "إصدار الحزمة:"},
    "UI_B_DELIV_002": {"en": "Schema:", "ar": "المخطط:"},
    "UI_B_DELIV_003": {"en": "Generated:", "ar": "تم الإنشاء:"},
    "UI_B_DELIV_004": {"en": "Session:", "ar": "الجلسة:"},
    "UI_B_DELIV_005": {"en": "FDC-001 Deliverable", "ar": "مُخرَج FDC-001"},
    "UI_B_DELIV_006": {"en": "Eligible assessment package", "ar": "حزمة تقييم مؤهَّلة"},
    "UI_B_DELIV_007": {
        "en": "Assessment Snapshot — In Progress",
        "ar": "لقطة التقييم — قيد التقدم",
    },
    "UI_B_DELIV_008": {
        "en": ("This is not a final deliverable. Continue developing the idea to "
               "reach eligibility."),
        "ar": ("هذا ليس مُخرَجًا نهائيًا. واصِل تطوير الفكرة للوصول إلى الأهلية."),
    },
    "UI_B_DELIV_009": {"en": "Maturity", "ar": "النضج"},
    "UI_B_DELIV_010A": {"en": "Derived readiness", "ar": "الجاهزية المشتقّة"},
    "UI_B_DELIV_010B": {
        "en": "(recomputed separately from stored maturity; not a validation or resolved status)",
        "ar": "(تُحتسب بشكل منفصل عن النضج المخزَّن؛ ليست تحققًا ولا حالة محسومة)",
    },
    "UI_B_DELIV_011": {
        "en": "Derived readiness signal met (still not technically verified)",
        "ar": "تحقّقت إشارة الجاهزية المشتقّة (وما زالت غير مُتحقَّق منها تقنيًا)",
    },
    "UI_B_DELIV_012": {
        "en": "Not derived-ready — recorded evidence is not technically verified",
        "ar": "غير جاهزة وفق الاشتقاق — الأدلة المسجَّلة غير مُتحقَّق منها تقنيًا",
    },
    "UI_B_DELIV_013": {
        "en": "Inventor-Stated Safety Signals",
        "ar": "إشارات السلامة كما ذكرها المخترِع",
    },
    "UI_B_DELIV_014": {"en": "Safety subject:", "ar": "موضوع السلامة:"},
    "UI_B_DELIV_015": {
        "en": "Failure condition stated by inventor:",
        "ar": "حالة الفشل كما ذكرها المخترِع:",
    },
    "UI_B_DELIV_016": {"en": "Possible consequence:", "ar": "العاقبة المحتملة:"},
    "UI_B_DELIV_017": {"en": "Source:", "ar": "المصدر:"},
    "UI_B_DELIV_018": {"en": "Provenance:", "ar": "المنشأ:"},
    "UI_B_DELIV_019": {"en": "Validation:", "ar": "التحقق:"},
    "UI_REPORT_CONTENTS": {"en": "Report contents", "ar": "محتويات التقرير"},
    "UI_REPORT_BACK_CONTENTS": {"en": "Back to contents", "ar": "العودة إلى المحتويات"},
    "UI_B_DELIV_020": {"en": "What your idea is", "ar": "ما هي فكرتك"},
    "UI_B_DELIV_021": {
        "en": ("A plain restatement of the invention as we currently understand "
               "it from your inputs."),
        "ar": "إعادة صياغة مبسّطة للاختراع كما نفهمه حاليًا من مدخلاتك.",
    },
    "UI_B_DELIV_022": {"en": "Invention Summary", "ar": "ملخص الاختراع"},
    "UI_B_DELIV_023": {"en": "Assessment Completeness", "ar": "اكتمال التقييم"},
    "UI_B_DELIV_024": {"en": "Known Problem", "ar": "المشكلة المعروفة"},
    "UI_B_DELIV_025": {"en": "Known Mechanism", "ar": "الآلية المعروفة"},
    "UI_B_DELIV_026": {"en": "What we assessed", "ar": "ما الذي قيّمناه"},
    "UI_B_DELIV_027": {
        "en": "The areas we looked at, and how far each one has been developed so far.",
        "ar": "المجالات التي نظرنا فيها، ومدى تطوّر كل منها حتى الآن.",
    },
    "UI_B_DELIV_028": {"en": "Assessment Overview", "ar": "نظرة عامة على التقييم"},
    "UI_B_DELIV_029": {"en": "Maturity:", "ar": "النضج:"},
    "UI_B_DELIV_030": {
        "en": "Gaps total/open/resolved:",
        "ar": "الفجوات الإجمالية/المفتوحة/المحلولة:",
    },
    "UI_B_DELIV_031": {"en": "What it needs", "ar": "ما الذي تحتاجه"},
    "UI_B_DELIV_032": {
        "en": "The inputs we captured and the open areas that still have to be worked out.",
        "ar": "المدخلات التي التقطناها والمجالات المفتوحة التي ما زال يتعيّن معالجتها.",
    },
    "UI_B_DELIV_033": {
        "en": "Captured Inputs and Assessment Status",
        "ar": "المدخلات الملتقطة وحالة التقييم",
    },
    "UI_B_DELIV_034": {
        "en": ("These are inputs captured from your answers, not tested "
               "conclusions. The suggested checks further down show what could "
               "help firm them up."),
        "ar": ("هذه مدخلات ملتقطة من إجاباتك، وليست استنتاجات مختبَرة. تُظهر "
               "الفحوصات المقترحة أدناه ما قد يساعد على ترسيخها."),
    },
    "UI_B_DELIV_035": {"en": "No requirements recorded yet.", "ar": "لم تُسجَّل أي متطلبات بعد."},
    "UI_B_DELIV_036": {"en": "Requirement Landscape", "ar": "مشهد المتطلبات"},
    "UI_B_DELIV_037": {"en": "Status:", "ar": "الحالة:"},
    "UI_B_DELIV_038": {"en": "Criticality:", "ar": "الأهمية:"},
    "UI_B_DELIV_039": {"en": "Rationale:", "ar": "المبرّر:"},
    "UI_B_DELIV_040": {"en": "Resolving action:", "ar": "الإجراء الحلّي:"},
    "UI_B_DELIV_041": {"en": "Supporting references:", "ar": "المراجع الداعمة:"},
    "UI_B_DELIV_042A": {"en": "(shared by ", "ar": "(مشترَك بين "},
    "UI_B_DELIV_042B": {"en": " entries)", "ar": " عنصرًا)"},
    "UI_B_DELIV_043": {
        "en": "What is assumed vs still unknown",
        "ar": "ما هو مُفترَض مقابل ما لا يزال مجهولًا",
    },
    "UI_B_DELIV_044": {
        "en": ("Things currently taken as given, alongside items you have flagged "
               "as not yet known."),
        "ar": ("أمور تُؤخذ حاليًا كمُسلَّمات، إلى جانب عناصر أشرتَ إلى أنها غير "
               "معروفة بعد."),
    },
    "UI_B_DELIV_045": {
        "en": "Assumptions & Inventor-Stated Unknowns",
        "ar": "الافتراضات والمجهولات كما ذكرها المخترِع",
    },
    "UI_B_DELIV_046": {"en": "No assumptions recorded yet.", "ar": "لم تُسجَّل أي افتراضات بعد."},
    "UI_B_DELIV_047": {"en": "Why this matters:", "ar": "لماذا يهم هذا:"},
    "UI_B_DELIV_048": {"en": "Unresolved Items", "ar": "العناصر غير المحلولة"},
    "UI_B_DELIV_049": {"en": "Acknowledged unknown:", "ar": "مجهول مُقرّ به:"},
    "UI_B_DELIV_050": {"en": "No unresolved items.", "ar": "لا توجد عناصر غير محلولة."},
    "UI_B_DELIV_051": {
        "en": ("No stored gaps remain open, but evidence validation or readiness "
               "items are still unresolved. The recorded evidence is not "
               "technically verified."),
        "ar": ("لم تعد هناك فجوات مخزَّنة مفتوحة، لكن لا تزال هناك عناصر تحقق من "
               "الأدلة أو جاهزية غير محلولة. الأدلة المسجَّلة غير مُتحقَّق منها "
               "تقنيًا."),
    },
    "UI_B_DELIV_052": {"en": "What could go wrong", "ar": "ما الذي قد يسوء"},
    "UI_B_DELIV_053": {
        "en": ("Risks recorded from the current state. This is not a safety "
               "judgement and is not exhaustive."),
        "ar": ("مخاطر مسجَّلة من الحالة الراهنة. هذا ليس حكمًا على السلامة وليس "
               "شاملًا."),
    },
    "UI_B_DELIV_054": {"en": "Risks", "ar": "المخاطر"},
    "UI_B_DELIV_055": {"en": "No risks recorded.", "ar": "لم تُسجَّل أي مخاطر."},
    "UI_B_DELIV_056": {"en": "The reasoning behind it", "ar": "المنطق وراء ذلك"},
    "UI_B_DELIV_057": {
        "en": "The recorded reasoning and evidence behind the assessment above.",
        "ar": "المنطق والأدلة المسجَّلة وراء التقييم أعلاه.",
    },
    "UI_B_DELIV_058": {"en": "Stage 3 Reasoning", "ar": "منطق المرحلة 3"},
    "UI_B_DELIV_059": {
        "en": "No Stage 3 reasoning areas are recorded for this session.",
        "ar": "لا توجد مجالات منطق للمرحلة 3 مسجَّلة لهذه الجلسة.",
    },
    "UI_B_DELIV_060": {
        "en": "What we recommend and what to do next",
        "ar": "ما نوصي به وما يجب فعله تاليًا",
    },
    "UI_B_DELIV_061": {
        "en": ("A suggested direction and concrete next steps you can act on. "
               "Advisory only."),
        "ar": ("اتجاه مقترَح وخطوات تالية ملموسة يمكنك اتخاذها. استرشادي فقط."),
    },
    "UI_B_DELIV_062": {"en": "Recommendations", "ar": "التوصيات"},
    "UI_B_DELIV_063": {"en": "Verdict", "ar": "الحكم"},
    "UI_B_DELIV_064": {"en": "Rationale", "ar": "المبرّر"},
    "UI_B_DELIV_065": {"en": "Open Items", "ar": "العناصر المفتوحة"},
    "UI_B_DELIV_067": {"en": "Next action", "ar": "الإجراء التالي"},
    "UI_B_DELIV_068": {"en": "Evidence needed", "ar": "الأدلة المطلوبة"},
    "UI_B_DELIV_069": {"en": "Suggested provider", "ar": "الجهة المقترَحة"},
    "UI_B_DELIV_070": {"en": "Sufficiency condition", "ar": "شرط الكفاية"},
    "UI_B_DELIV_071": {
        "en": ("No actionable next development step. The recorded state shows "
               "nothing outstanding to develop next."),
        "ar": ("لا توجد خطوة تطوير تالية قابلة للتنفيذ. تُظهر الحالة المسجَّلة عدم "
               "وجود ما يستوجب التطوير تاليًا."),
    },
    "UI_B_DELIV_072": {"en": "Recommended Next Steps", "ar": "الخطوات التالية الموصى بها"},
    "UI_B_DELIV_073": {"en": "(high priority)", "ar": "(أولوية عالية)"},
    "UI_B_DELIV_074": {
        "en": "Prototype & Test Plan",
        "ar": "خطة النموذج الأولي والاختبار",
    },
    "UI_B_DELIV_075": {"en": "Objective:", "ar": "الهدف:"},
    "UI_B_DELIV_076": {"en": "Based on:", "ar": "بناءً على:"},
    "UI_B_DELIV_077": {"en": "Minimum prototype:", "ar": "الحد الأدنى للنموذج الأولي:"},
    "UI_B_DELIV_078": {"en": "Observe:", "ar": "لاحِظ:"},
    "UI_B_DELIV_079": {
        "en": "Success criterion — user-defined:",
        "ar": "معيار النجاح — مُعرَّف من المستخدم:",
    },
    "UI_B_DELIV_080": {"en": "Success criterion:", "ar": "معيار النجاح:"},
    "UI_B_DELIV_081": {"en": "Failure / revise if:", "ar": "الفشل / أعِد النظر إذا:"},
    "UI_B_DELIV_082": {"en": "Evidence upgrade target:", "ar": "هدف ترقية الأدلة:"},
    "UI_B_DELIV_083": {
        "en": "Shared expertise and tools identified by the inventor",
        "ar": "الخبرات والأدوات المشتركة التي حدّدها المخترِع",
    },
    "UI_B_DELIV_084": {
        "en": ("Define or edit success criteria, test hypotheses, test variables / "
               "conditions and measurement methods"),
        "ar": ("تحديد معايير النجاح وفرضيات الاختبار ومتغيّرات / شروط الاختبار وطرق "
               "القياس أو تعديلها"),
    },
    "UI_B_DELIV_085": {"en": "Validation Plan", "ar": "خطة التحقق"},
    "UI_B_DELIV_086": {
        "en": ("Suggested checks that would help firm up this idea. None has been "
               "carried out yet — these are proposals, not results. Each check "
               "keeps its supporting details on one line below it."),
        "ar": ("فحوصات مقترَحة قد تساعد على ترسيخ هذه الفكرة. لم يُنفَّذ أي منها "
               "بعد — هذه اقتراحات وليست نتائج. يحتفظ كل فحص بتفاصيله الداعمة في "
               "سطر واحد أسفله."),
    },
    "UI_B_DELIV_087": {"en": "Checks you can do yourself", "ar": "فحوصات يمكنك إجراؤها بنفسك"},
    "UI_B_DELIV_088": {"en": "Needs specialist input", "ar": "يحتاج إلى مدخلات متخصّص"},
    "UI_B_DELIV_089": {
        "en": "Needs a physical test or evidence",
        "ar": "يحتاج إلى اختبار فعلي أو دليل",
    },
    "UI_B_DELIV_090": {"en": "Other suggested checks", "ar": "فحوصات مقترَحة أخرى"},
    "UI_B_DELIV_091A": {"en": "(applies to ", "ar": "(ينطبق على "},
    "UI_B_DELIV_091B": {"en": " recorded answers)", "ar": " إجابة مسجَّلة)"},
    "UI_B_DELIV_092": {
        "en": "Responsibility has not yet been assigned.",
        "ar": "لم تُسنَد المسؤولية بعد.",
    },
    "UI_B_DELIV_093": {
        "en": "Choose who will own this validation step before relying on the result.",
        "ar": "اختر من سيتولّى خطوة التحقق هذه قبل الاعتماد على النتيجة.",
    },
    "UI_B_DELIV_094": {"en": "Responsibility:", "ar": "المسؤولية:"},
    "UI_B_DELIV_095": {"en": "Evidence needed:", "ar": "الأدلة المطلوبة:"},
    "UI_B_DELIV_096": {"en": "Closure:", "ar": "الإغلاق:"},
    "UI_B_DELIV_097": {"en": "Confidence:", "ar": "الثقة:"},
    "UI_B_DELIV_098": {"en": "Blocked items", "ar": "العناصر المحجوبة"},
    "UI_B_DELIV_099": {"en": "Missing:", "ar": "المفقود:"},
    "UI_B_DELIV_100": {"en": "Output review", "ar": "مراجعة المُخرَج"},
    "UI_B_DELIV_101": {
        "en": ("This is a working snapshot of your idea in the current temporary "
               "session. It has not been permanently saved or approved. Choose "
               "what to do next."),
        "ar": ("هذه لقطة عمل لفكرتك في الجلسة المؤقتة الحالية. لم تُحفظ بشكل دائم "
               "ولم تُعتمد. اختر ما تريد فعله تاليًا."),
    },
    "UI_B_DELIV_102": {"en": "Refine this idea", "ar": "تحسين هذه الفكرة"},
    "UI_B_DELIV_103": {"en": "Keep current snapshot", "ar": "الاحتفاظ باللقطة الحالية"},
    "UI_B_DELIV_104": {"en": "Back to session", "ar": "العودة إلى الجلسة"},
    "UI_B_DELIV_105": {
        "en": ("Current working snapshot selected for this temporary session. It "
               "has not been permanently saved or approved."),
        "ar": ("تم اختيار لقطة العمل الحالية لهذه الجلسة المؤقتة. لم تُحفظ بشكل "
               "دائم ولم تُعتمد."),
    },

    # --- D-P6-18 bounded-review remediation ----------------------------------
    # Answer-action choice controls (session.html response fieldset). Owner
    # ruling: these are ordinary UI chrome, NOT canonical question text and NOT
    # Translation-Assistant content, so they follow the selected UI language.
    "UI_ACT_ANSWERED": {
        "en": "Answer this question (using the text above)",
        "ar": "الإجابة عن هذا السؤال (باستخدام النص أعلاه)",
    },
    "UI_ACT_UNKNOWN": {"en": "I do not know this yet", "ar": "لا أعرف هذا بعد"},
    "UI_ACT_DEFERRED": {
        "en": "Defer this question for now", "ar": "تأجيل هذا السؤال الآن",
    },
    "UI_ACT_PROVISIONAL": {
        "en": "Record a provisional assumption (not verified — optional note above)",
        "ar": "تسجيل افتراض مبدئي (غير مُتحقَّق منه — ملاحظة اختيارية أعلاه)",
    },
    "UI_ACT_SPECIALIST": {
        "en": "A specialist needs to answer this",
        "ar": "يحتاج متخصّص إلى الإجابة عن هذا",
    },
    "UI_ACT_EVIDENCE": {
        "en": "Evidence or a test is needed for this",
        "ar": "يلزم دليل أو اختبار لهذا",
    },
    # UQTR-01 Step 2B: Owner-supplied EN/AR stale-response-form refusal (one
    # high-level message for every target/freshness failure).
    "UI_UQTR_FORM_STALE": {
        "en": ("This response form is no longer current, so nothing was saved. "
               "Please review the current question and respond there."),
        "ar": ("هذا النموذج لم يعد هو النموذج الحالي، لذلك لم يتم حفظ أي شيء. "
               "يرجى مراجعة السؤال الحالي والإجابة عنه."),
    },
    # UQTR-01: gap-scoped non-answer serving suppression + the 4+2 response
    # group. Truthful chrome only: suppression stops the AUTOMATIC re-ask; it
    # resolves nothing, assumes no technical answer and supplies nothing.
    "UI_UQTR_MORE_CHOICES": {
        "en": "More response options",
        "ar": "خيارات رد إضافية",
    },
    "UI_UQTR_TEXT_HINT": {
        "en": ("Text is required if you choose to answer the question. For the "
               "other options, you may add an optional note."),
        "ar": ("النص مطلوب إذا اخترت الإجابة عن السؤال. في الخيارات الأخرى، يمكنك "
               "إضافة ملاحظة اختيارية."),
    },
    "UI_UQTR_SUPPRESSED_HEADING": {
        "en": "This technical point is still unresolved.",
        "ar": "هذه النقطة التقنية لا تزال غير محسومة.",
    },
    "UI_UQTR_MEANING_UNKNOWN": {
        "en": "You recorded that this point is not known yet.",
        "ar": "سجّلت أن هذه النقطة غير معروفة بعد.",
    },
    "UI_UQTR_MEANING_DEFERRED": {
        "en": ("You deferred this point for now. Deferring it does not mean it has "
               "been resolved."),
        "ar": "أجّلت هذه النقطة في الوقت الحالي. التأجيل لا يعني أنها حُسمت.",
    },
    "UI_UQTR_MEANING_SPECIALIST_REQUESTED": {
        "en": ("You recorded that this point needs specialist input. Choosing this "
               "option does not mean specialist input has already been provided."),
        "ar": ("سجّلت أن هذه النقطة تحتاج إلى رأي مختص. اختيار هذا الخيار لا يعني "
               "أن رأيًا متخصصًا قد قُدّم."),
    },
    "UI_UQTR_MEANING_EVIDENCE_REQUESTED": {
        "en": ("You recorded that this point needs evidence or a test. Requesting it "
               "does not mean evidence or a test result is already available."),
        "ar": ("سجّلت أن هذه النقطة تحتاج إلى دليل أو اختبار. مجرد طلب ذلك لا يعني "
               "أن دليلًا أو نتيجة اختبار قد أصبح متاحًا."),
    },
    "UI_UQTR_MEANING_PROVISIONAL_ASSUMPTION": {
        "en": ("You recorded a provisional assumption. It is unverified and is not "
               "an established fact."),
        "ar": "سجّلت افتراضًا مبدئيًا. هذا الافتراض غير متحقق منه ولا يُعد حقيقة مثبتة.",
    },
    "UI_UQTR_SUPPRESSED_NEXT": {
        "en": ("Your choice was recorded and no technical answer has been assumed. "
               "This question will not be asked again automatically. Your current "
               "assessment shows what is still needed, and you can revisit this "
               "question whenever you want."),
        "ar": ("تم تسجيل اختيارك ولم يُفترض أي جواب تقني. لن يُطرح هذا السؤال "
               "تلقائيًا مرة أخرى. يوضّح التقييم الحالي ما لا يزال مطلوبًا، ويمكنك "
               "العودة إلى هذا السؤال متى شئت."),
    },
    "UI_UQTR_REVISIT": {
        "en": "Revisit this technical question",
        "ar": "العودة إلى هذا السؤال التقني",
    },
    "UI_UQTR_JOURNEY_NOTE": {
        "en": ("Your choice for this technical point was recorded; the point "
               "remains unresolved."),
        "ar": "تم تسجيل اختيارك لهذه النقطة التقنية، وهي لا تزال غير محسومة.",
    },
    # Safe Question Reduction Slice 1 — a routed need (not a mandatory
    # inventor question; still unresolved). The need wording itself is domain
    # content from the committed Path-N artifact, never from this catalogue.
    "UI_NR_HEADING_SPECIALIST": {
        "en": "Specialist input required",
        "ar": "مدخلات مختص مطلوبة",
    },
    "UI_NR_HEADING_EVIDENCE": {
        "en": "Evidence or measurement required",
        "ar": "دليل أو قياس مطلوب",
    },
    "UI_NR_NOT_ASKED": {
        "en": ("You are not asked to answer this point yourself. It stays open "
               "until specialist input is recorded; no technical answer has "
               "been assumed."),
        "ar": ("لا يُطلب منك الإجابة عن هذه النقطة بنفسك. تبقى مفتوحة إلى أن "
               "تُسجَّل مدخلات مختص، ولم يُفترض أي جواب تقني."),
    },
    "UI_NR_NOT_ASKED_EVIDENCE": {
        "en": ("You are not asked to answer this point yourself. It stays open "
               "until evidence or a measurement is recorded; no technical "
               "answer has been assumed."),
        "ar": ("لا يُطلب منك الإجابة عن هذه النقطة بنفسك. تبقى مفتوحة إلى أن "
               "يُسجَّل دليل أو قياس، ولم يُفترض أي جواب تقني."),
    },
    "UI_NR_OPTIONAL_NOTE": {
        "en": ("Optional. What you add is saved as your own note; it does not "
               "establish the technical limit and does not replace specialist "
               "input."),
        "ar": ("اختياري. ما تضيفه يُحفظ كملاحظة منك، ولا يحدّد الحد التقني ولا "
               "يحلّ محل مدخلات المختص."),
    },
    "UI_NR_SAVE": {
        "en": "Save note",
        "ar": "حفظ الملاحظة",
    },
    # Slice 1 journey safety — no question is served and a routed need blocks
    # the next stage. Truthful: nothing is resolved, assumed or accepted here.
    "UI_NR_RECOVERY_HEADING": {
        "en": "No question is waiting for you right now",
        "ar": "لا يوجد سؤال بانتظارك الآن",
    },
    "UI_NR_RECOVERY_TEXT": {
        "en": ("A point above still needs specialist input, so the next stage "
               "stays locked. Your earlier answer on it did not describe how it "
               "would work, so accepting it as a known risk is not available "
               "yet. You do not have to invent technical details."),
        "ar": ("ما زالت نقطة أعلاه تحتاج إلى مدخلات مختص، لذلك تبقى المرحلة "
               "التالية مغلقة. إجابتك السابقة عنها لم تصف كيف سيعمل ذلك، لذلك "
               "لا يتاح قبولها كمخاطرة معروفة بعد. لست مضطرًا لاختلاق تفاصيل تقنية."),
    },
    "UI_NR_RECOVERY_CORRECT": {
        "en": ("If you can now describe it in your own words, correct your "
               "earlier answer. After that you may choose to accept this point "
               "as a known, unresolved risk."),
        "ar": ("إذا كنت تستطيع الآن وصفها بكلماتك، صحّح إجابتك السابقة. بعد ذلك "
               "يمكنك أن تختار قبول هذه النقطة كمخاطرة معروفة غير محسومة."),
    },
    "UI_NR_RECOVERY_LINK": {
        "en": "Correct your earlier answer",
        "ar": "تصحيح إجابتك السابقة",
    },
    "UI_NR_RECOVERY_WAIT": {
        "en": ("Otherwise this point stays open until specialist input is "
               "recorded. You can still add your own note or review the "
               "current handoff."),
        "ar": ("وإلا تبقى هذه النقطة مفتوحة إلى أن تُسجَّل مدخلات مختص. ما زال "
               "بإمكانك إضافة ملاحظتك أو مراجعة ملف التسليم الحالي."),
    },
    "UI_NR_RECOVERY_JOURNEY_NOTE": {
        "en": ("No question is waiting. One point still needs specialist input "
               "before the next stage."),
        "ar": "لا يوجد سؤال بانتظارك. ما زالت نقطة تحتاج إلى مدخلات مختص قبل المرحلة التالية.",
    },
    "UI_NR_RECOVERY_CTA": {
        "en": "See your options",
        "ar": "عرض خياراتك",
    },
    "UI_NO_QUESTION_NOTE": {
        "en": "No question is waiting for you right now.",
        "ar": "لا يوجد سؤال بانتظارك الآن.",
    },
    "UI_UQTR_CTA": {
        "en": "Review what is still needed",
        "ar": "مراجعة ما لا يزال مطلوبًا",
    },
    # Correction free-text placeholder (criticality correction stage). UI chrome.
    "UI_CRIT_CORR_PLACEHOLDER": {
        "en": "Describe the change or the missing part in your own words...",
        "ar": "صف التغيير أو الجزء الناقص بكلماتك الخاصة...",
    },
    # Criticality correction/summary chrome literals (session.html). These are UI
    # chrome/instructions/controls — NOT the canonical clarification ask (which
    # stays English) and NOT echoed user content.
    "UI_CRIT_CORR_H": {
        "en": "Tell me in your own words", "ar": "أخبرني بكلماتك الخاصة",
    },
    "UI_CRIT_CORR_T": {
        "en": ("Describe what should change or what is missing, and it will be "
               "used to update the picture of your idea."),
        "ar": "صف ما ينبغي تغييره أو ما هو ناقص، وسيُستخدم لتحديث صورة فكرتك.",
    },
    "UI_CRIT_CLAR_REASON": {
        "en": ("Your reason, in your own words (already filled in from what you "
               "said — keep it or edit it):"),
        "ar": "سببك، بكلماتك الخاصة (مملوء مسبقًا مما قلته — أبقِه أو عدّله):",
    },
    "UI_CRIT_SAVE": {"en": "Save this", "ar": "احفظ هذا"},
    "UI_CRIT_YOUSAID": {"en": "You said:", "ar": "لقد قلت:"},
    "UI_CRIT_CORRECT_Q": {"en": "Is that correct?", "ar": "هل هذا صحيح؟"},
    # Active page <title> values. The "InventorAI" brand stays Latin in both
    # languages; only the descriptive portion (or a bare data-screen title) is
    # localised. Canonical question text is never a page title.
    "UI_TITLE_INDEX": {"en": "InventorAI", "ar": "InventorAI"},
    "UI_TITLE_ACCOUNT": {"en": "InventorAI — Your account",
                         "ar": "InventorAI — حسابك"},
    "UI_TITLE_LOGIN": {"en": "InventorAI — Sign in",
                       "ar": "InventorAI — تسجيل الدخول"},
    "UI_TITLE_REGISTER": {"en": "InventorAI — Create account",
                          "ar": "InventorAI — إنشاء حساب"},
    "UI_TITLE_RECOVER": {"en": "InventorAI — Reset your password",
                         "ar": "InventorAI — إعادة تعيين كلمة المرور"},
    "UI_TITLE_RESET": {"en": "InventorAI — Set a new password",
                       "ar": "InventorAI — تعيين كلمة مرور جديدة"},
    "UI_TITLE_VERIFY": {"en": "InventorAI — Email verification",
                        "ar": "InventorAI — التحقق من البريد الإلكتروني"},
    "UI_TITLE_SESSION": {"en": "InventorAI — Session",
                         "ar": "InventorAI — الجلسة"},
    "UI_TITLE_DELIVERABLE": {"en": "InventorAI — Deliverable",
                             "ar": "InventorAI — المُخرَج"},
    "UI_TITLE_SUCCESS": {"en": "InventorAI — Define Success Criteria and Measurement Methods",
                         "ar": "InventorAI — تحديد معايير النجاح وطرق القياس"},
    "UI_TITLE_DATA": {"en": "Data & Session information",
                      "ar": "معلومات البيانات والجلسة"},

    # --- DIRECT-OUTPUT-PDF: on-demand, in-memory PDF download of the current
    # report. UI chrome only. The wording states exactly what the action does —
    # it never implies finality, validation, approval, technical verification,
    # or a durable save, because none of those occur: the PDF is generated
    # synchronously in memory from the report as it stands and is never stored.
    "UI_PDF_DOWNLOAD": {"en": "Download PDF",
                        "ar": "تنزيل ملف PDF"},
    "UI_PDF_DOWNLOAD_HELP": {
        "en": "Downloads the current report with its current status.",
        "ar": "ينزّل التقرير الحالي بحالته الحالية.",
    },
    "UI_PDF_TOO_LARGE": {
        "en": ("This report is too large to generate as a PDF safely. "
               "The report remains available on this page."),
        "ar": ("هذا التقرير كبير جدًا بحيث لا يمكن إنشاء ملف PDF منه بأمان. "
               "يظل التقرير متاحًا في هذه الصفحة."),
    },
    "UI_PDF_UNAVAILABLE": {
        "en": "We could not generate the PDF. Nothing was saved. Please try again.",
        "ar": "تعذر إنشاء ملف PDF. لم يتم حفظ أي شيء. يُرجى المحاولة مرة أخرى.",
    },

    # --- T2-A Quantified Requirements Slice 1: presentation chrome ONLY. The
    # stored values are canonical tokens (the closed ``quantity_kind`` and the
    # exact ``value_text``) owned by engine/requirement_quantity.py; these
    # entries are the localized DISPLAY of the kind tokens (``UI_T2A_KIND_<TOKEN>``),
    # the statuses and the block's plain-language framing. Inventor value text
    # is NEVER localized and never passes through localize_deep. Optional and
    # progressive: the block is collapsed by default and the journey completes
    # without entering a single value. The wording claims recording only —
    # never validation, attainability, feasibility, safety or compliance.
    "UI_T2A_HEADING": {"en": "Add a value to a requirement (optional)",
                       "ar": "أضف قيمة إلى متطلب (اختياري)"},
    "UI_T2A_EXPLAIN": {
        "en": ("If you already know a value for one of your recorded requirements — "
               "a target, a minimum, a maximum, a range or a count — you can record "
               "it here in your own words, with its unit. This is optional. What you "
               "enter is kept as stated and is not checked, validated, or assessed for "
               "feasibility, attainability, safety, or compliance. Recording a new value "
               "for the same item replaces the earlier one and keeps it in your project "
               "history. You will be asked to confirm before anything is saved."),
        "ar": ("إذا كنت تعرف بالفعل قيمة لأحد المتطلبات المسجّلة — هدفًا أو حدًا أدنى أو "
               "حدًا أقصى أو نطاقًا أو عددًا — يمكنك تسجيلها هنا بكلماتك مع وحدتها. "
               "هذا اختياري. ما تدخله يُحفظ كما ذكرته ولا يُفحص ولا يُتحقق منه ولا يُقيَّم "
               "من حيث الجدوى أو إمكانية التحقيق أو السلامة أو الامتثال. تسجيل قيمة "
               "جديدة للعنصر نفسه يحل محل القيمة السابقة مع الاحتفاظ بها في سجل مشروعك. "
               "سيُطلب منك التأكيد قبل حفظ أي شيء."),
    },
    "UI_T2A_CURRENT": {"en": "Recorded value:", "ar": "القيمة المسجّلة:"},
    "UI_T2A_NONE": {"en": "No value recorded for this item.",
                    "ar": "لا توجد قيمة مسجّلة لهذا العنصر."},
    "UI_T2A_KIND_LABEL": {"en": "Kind of value", "ar": "نوع القيمة"},
    "UI_T2A_VALUE_LABEL": {"en": "Value, in your own words", "ar": "القيمة بكلماتك"},
    "UI_T2A_VALUE_HINT": {
        "en": "Short plain text with the unit, for example 12 V or 0.5 mm. Up to 120 characters, on one line.",
        "ar": "نص قصير مع الوحدة، مثل 12 V أو 0.5 mm. حتى 120 حرفًا في سطر واحد.",
    },
    "UI_T2A_BUTTON": {"en": "Review this value", "ar": "راجع هذه القيمة"},
    "UI_T2A_REPLACE_BUTTON": {"en": "Review a replacement value",
                              "ar": "راجع قيمة بديلة"},
    "UI_T2A_CONFIRM_HEADING": {"en": "Confirm this value before it is saved",
                               "ar": "أكّد هذه القيمة قبل حفظها"},
    "UI_T2A_CONFIRM_EXPLAIN": {
        "en": ("Nothing has been saved yet. Confirm to record this value as stated, "
               "or discard it. It will not be checked or verified."),
        "ar": ("لم يُحفظ أي شيء بعد. أكّد لتسجيل هذه القيمة كما ذكرتها، أو تجاهلها. "
               "لن تُفحص ولن يُتحقق منها."),
    },
    "UI_T2A_CONFIRM_REPLACES": {"en": "This will replace the recorded value:",
                                "ar": "سيحل هذا محل القيمة المسجّلة:"},
    "UI_T2A_CONFIRM_BUTTON": {"en": "Confirm and save", "ar": "أكّد واحفظ"},
    "UI_T2A_DISCARD_BUTTON": {"en": "Discard", "ar": "تجاهل"},
    "UI_T2A_STATUS_UNVALIDATED": {"en": "Inventor-stated, not validated",
                                  "ar": "بحسب إفادة المخترع، غير مُتحقَّق منه"},
    "UI_T2A_REPLACED": {"en": "Replaced values:", "ar": "القيم المستبدَلة:"},
    "UI_T2A_WITHDRAWN_ANCHOR": {"en": "Value attached to a withdrawn answer",
                                "ar": "قيمة مرتبطة بإجابة مسحوبة"},
    "UI_T2A_WITHDRAWN_NOTE": {
        "en": ("The answer this value was attached to has been withdrawn. The value is "
               "kept in your project history and is no longer current."),
        "ar": ("سُحبت الإجابة التي كانت هذه القيمة مرتبطة بها. تُحفظ القيمة في سجل "
               "مشروعك ولم تعد حالية."),
    },
    "UI_T2A_DELIV_HEADING": {"en": "Quantities you recorded",
                             "ar": "الكميات التي سجّلتها"},
    "UI_T2A_DISCLAIMER": {
        "en": ("These values were entered by the inventor for the listed requirements. "
               "They are recorded as stated and have not been checked, validated, or "
               "assessed for feasibility, attainability, safety, or compliance."),
        "ar": ("أدخل المخترع هذه القيم للمتطلبات المدرجة. وهي مسجّلة كما ذُكرت ولم "
               "تُفحص ولم يُتحقق منها ولم تُقيَّم من حيث الجدوى أو إمكانية التحقيق أو "
               "السلامة أو الامتثال."),
    },
    "UI_T2A_PROVENANCE": {"en": "Recorded by the inventor (not yet verified)",
                          "ar": "سجّله المخترع (لم يُتحقق منه بعد)"},
    "UI_T2A_ERR_NOT_SAVED": {
        "en": "That quantity could not be saved just now. Nothing was changed.",
        "ar": "تعذر حفظ هذه الكمية الآن. لم يتغير أي شيء.",
    },
    "UI_T2A_ERR_INVALID": {
        "en": ("Choose what kind of value this is and enter it as short plain text for "
               "the selected item. Nothing was changed."),
        "ar": "اختر نوع القيمة وأدخلها كنص قصير للعنصر المحدد. لم يتغير أي شيء.",
    },
    "UI_T2A_ERR_CONFLICT": {
        "en": ("The recorded values for this item changed while you were confirming, so "
               "that quantity was not saved. Nothing was changed. Review the values shown "
               "here and enter it again if you still want it."),
        "ar": ("تغيرت القيم المسجّلة لهذا العنصر أثناء تأكيدك، لذلك لم تُحفظ هذه الكمية. "
               "لم يتغير أي شيء. راجع القيم المعروضة هنا وأدخلها مرة أخرى إذا كنت "
               "لا تزال تريدها."),
    },
    "UI_T2A_ERR_UNKNOWN": {
        "en": ("We could not confirm whether that quantity was saved. Reload this page to "
               "see the values your project currently holds before entering it again."),
        "ar": ("تعذر علينا تأكيد ما إذا كانت هذه الكمية قد حُفظت. أعد تحميل هذه الصفحة "
               "لرؤية القيم التي يحتفظ بها مشروعك حاليًا قبل إدخالها مرة أخرى."),
    },
    "UI_T2A_ERR_SAVED_NOT_SHOWN": {
        "en": ("Your quantity was saved to your project, but it could not be shown here "
               "just now. Reload this page shortly to see it."),
        "ar": ("حُفظت الكمية في مشروعك، لكن تعذر عرضها هنا الآن. أعد تحميل هذه الصفحة "
               "بعد قليل لرؤيتها."),
    },
    # Kind tokens (engine QUANTITY_KINDS, accepted design delta §6) -> display,
    # keyed ``UI_T2A_KIND_<TOKEN>`` (token upper-cased); one entry per token.
    "UI_T2A_KIND_TARGET_VALUE": {"en": "Target value", "ar": "قيمة مستهدفة"},
    "UI_T2A_KIND_MINIMUM_VALUE": {"en": "Minimum value", "ar": "حد أدنى"},
    "UI_T2A_KIND_MAXIMUM_VALUE": {"en": "Maximum value", "ar": "حد أقصى"},
    "UI_T2A_KIND_RANGE": {"en": "Range", "ar": "نطاق"},
    "UI_T2A_KIND_COUNT": {"en": "Count", "ar": "عدد"},
    "UI_T2A_KIND_OTHER_QUANTITY": {"en": "Other quantity", "ar": "كمية أخرى"},

    # --- T1-D / T2-B' (OD-PDVG-12 + OD-PDVG-13, exercised for this bounded
    # increment only): presentation chrome ONLY.
    #
    # T2-B' — "Why this question?". ONE short, fixed, bilingual line per
    # COMMITTED question identity. This is approved DISPLAY COPY authored for
    # users; it is NOT the WS10 registry's internal English, which is never
    # rendered. Each line is traceable to the semantics of the registry record
    # carrying the same question_id (its primary intent / answer objective),
    # restated in plain language. No identifier, gap token, registry path,
    # reason code, marker, completion condition, scoring or progression rule
    # appears in any of them, and none claims an answer is correct, sufficient,
    # verified, complete or accepted. Selection is by exact committed identity
    # (see QUESTION_EXPLANATION_KEYS below); nothing here is generated,
    # translated at runtime, or interpolated with user content.
    "UI_T1D_WHY_HEADING": {"en": "Why this question?", "ar": "لماذا هذا السؤال؟"},

    # electronics_electrical
    "UI_T2B_WHY_N_MC_1": {
        "en": ("So your report can describe how the idea notices the problem and "
               "what it does in response."),
        "ar": ("لكي يصف تقريرك كيف تلاحظ الفكرة المشكلة وماذا تفعل استجابةً لها."),
    },
    "UI_T2B_WHY_N_MC_2": {
        "en": "So the parts of the idea, and what each part does, are recorded together.",
        "ar": "لكي تُسجَّل أجزاء الفكرة ودور كل جزء منها معًا.",
    },
    "UI_T2B_WHY_N_MC_3": {
        "en": ("So the steps from the problem starting to the response happening are "
               "recorded in order."),
        "ar": "لكي تُسجَّل الخطوات من بدء المشكلة حتى حدوث الاستجابة بالترتيب.",
    },
    "UI_T2B_WHY_N_MC_4": {
        "en": "So the part you are least sure about is recorded as open, not assumed.",
        "ar": "لكي يُسجَّل الجزء الأقل يقينًا لديك بوصفه مفتوحًا، لا مفترضًا.",
    },
    "UI_T2B_WHY_N_PF_1": {
        "en": ("So the conditions the idea depends on to work safely in the real world "
               "are written down."),
        "ar": "لكي تُدوَّن الظروف التي تعتمد عليها الفكرة لتعمل بأمان في الواقع.",
    },
    "UI_T2B_WHY_N_PF_2": {
        "en": "So what the idea needs in order to keep working over time is recorded.",
        "ar": "لكي يُسجَّل ما تحتاجه الفكرة كي تستمر في العمل مع مرور الوقت.",
    },
    "UI_T2B_WHY_N_PF_3": {
        "en": ("So real-world conditions that could disturb the idea are recorded "
               "instead of assumed away."),
        "ar": "لكي تُسجَّل ظروف الواقع التي قد تُربك الفكرة بدل تجاهلها بالافتراض.",
    },
    "UI_T2B_WHY_N_PF_4": {
        "en": "So the check most worth doing first is recorded as a next step.",
        "ar": "لكي يُسجَّل الفحص الأجدر بالبدء به بوصفه خطوة تالية.",
    },
    "UI_T2B_WHY_N_BA_1": {
        "en": "So the situations the idea is meant to handle are stated, not left open.",
        "ar": "لكي تُذكر المواقف التي يُفترض أن تتعامل معها الفكرة، لا أن تُترك مفتوحة.",
    },
    "UI_T2B_WHY_N_BA_2": {
        "en": "So what the idea is responsible for is separated from what it is not.",
        "ar": "لكي يُفصل ما تتحمله الفكرة من مسؤولية عمّا لا تتحمله.",
    },
    "UI_T2B_WHY_N_BA_3": {
        "en": ("So the difference between when the idea should act and when it should "
               "stay quiet is recorded."),
        "ar": "لكي يُسجَّل الفرق بين الحالة التي تتصرف فيها الفكرة والحالة التي تبقى فيها صامتة.",
    },

    # mechanical
    "UI_T2B_WHY_MECHANICAL_MECHANISM_COMPLETENESS_Q1": {
        "en": "So the physical steps the mechanism takes to do its job are recorded in order.",
        "ar": "لكي تُسجَّل الخطوات المادية التي تؤديها الآلية لإنجاز وظيفتها بالترتيب.",
    },
    "UI_T2B_WHY_MECHANICAL_MECHANISM_COMPLETENESS_Q2": {
        "en": "So the parts that move, connect, or carry force through the idea are recorded.",
        "ar": "لكي تُسجَّل الأجزاء التي تتحرك أو تتصل أو تنقل القوة داخل الفكرة.",
    },
    "UI_T2B_WHY_MECHANICAL_MECHANISM_COMPLETENESS_Q3": {
        "en": "So each mechanical part, and what it contributes, are recorded together.",
        "ar": "لكي يُسجَّل كل جزء ميكانيكي وما يسهم به معًا.",
    },
    "UI_T2B_WHY_MECHANICAL_MECHANISM_COMPLETENESS_Q4": {
        "en": "So the physical detail a builder would still need is recorded as open.",
        "ar": "لكي تُسجَّل التفصيلة المادية التي سيظل يحتاجها من يبني الفكرة بوصفها مفتوحة.",
    },
    "UI_T2B_WHY_MECHANICAL_PHYSICAL_FEASIBILITY_Q1": {
        "en": "So the physical principle the idea relies on is stated rather than assumed.",
        "ar": "لكي يُذكر المبدأ الفيزيائي الذي تعتمد عليه الفكرة بدل افتراضه.",
    },
    "UI_T2B_WHY_MECHANICAL_PHYSICAL_FEASIBILITY_Q2": {
        "en": "So the material and force limits the idea works within are recorded.",
        "ar": "لكي تُسجَّل حدود المواد والقوى التي تعمل الفكرة ضمنها.",
    },
    "UI_T2B_WHY_MECHANICAL_BOUNDARY_AMBIGUITY_Q1": {
        "en": "So what the idea does not do is stated, not left open.",
        "ar": "لكي يُذكر ما لا تفعله الفكرة، لا أن يُترك مفتوحًا.",
    },
    "UI_T2B_WHY_MECHANICAL_BOUNDARY_AMBIGUITY_Q2": {
        "en": "So at least one clear limit of the idea is recorded.",
        "ar": "لكي يُسجَّل حدٌّ واضح واحد للفكرة على الأقل.",
    },
    "UI_T2B_WHY_MECHANICAL_BOUNDARY_AMBIGUITY_Q3": {
        "en": "So an existing approach close to yours is recorded for comparison.",
        "ar": "لكي يُسجَّل أسلوب قائم قريب من أسلوبك لأجل المقارنة.",
    },
    "UI_T2B_WHY_MECHANICAL_BOUNDARY_AMBIGUITY_Q4": {
        "en": "So the concrete physical difference from that approach is recorded.",
        "ar": "لكي يُسجَّل الفرق المادي الملموس عن ذلك الأسلوب.",
    },

    # T1-D — two truthful limitation disclosures. Each states what this version
    # does and does not do, in the established style of UI_B_SESSION_026
    # ("...are not currently provided"). Neither says the product does nothing,
    # that validation is impossible in principle, or that higher evidence states
    # are permanently unavailable; neither changes any label, status value,
    # readiness computation or selection behaviour.
    "UI_T1D_QUESTION_SET": {
        "en": ("These questions come from a fixed, reviewed set. This version chooses "
               "which one to show from what your project already records, using fixed "
               "rules — it does not read the meaning of your answers to create new "
               "follow-up questions."),
        "ar": ("تأتي هذه الأسئلة من مجموعة ثابتة ومراجَعة. ويختار هذا الإصدار أيها "
               "يعرض بناءً على ما سجّله مشروعك فعلًا، وفق قواعد ثابتة — وهو لا يقرأ "
               "معنى إجاباتك لينشئ أسئلة متابعة جديدة."),
    },
    # T2-G (`T2G-VERSIONED-IMPLEMENT-01`): shown ONLY on projects recorded under
    # the T2-G engine-contract version, where the bounded rule actually applies.
    # `UI_T1D_QUESTION_SET` above is RETAINED verbatim and stays the accurate
    # disclosure for every earlier project. This wording states the fixed set,
    # the fixed rules, the BOUNDED uncertainty recognition and its limits, that
    # no new questions are generated, and that engineering correctness is not
    # verified. It claims no general semantic understanding.
    "UI_T2G_QUESTION_SET": {
        "en": ("These questions come from a fixed, reviewed set. This version "
               "chooses which one to show from what your project already "
               "records, using fixed rules — including recognising some ways "
               "of saying you do not know something yet. That recognition "
               "covers only certain phrasings, so it will miss others. No new "
               "questions are generated, and whether your idea is "
               "engineering-correct is not checked."),
        "ar": ("تأتي هذه الأسئلة من مجموعة ثابتة ومراجَعة. ويختار هذا الإصدار "
               "أيها يعرض بناءً على ما سجّله مشروعك فعلًا، وفق قواعد ثابتة — "
               "بما في ذلك تمييز بعض صيغ قولك إنك لا تعرف شيئًا بعد. ولا يشمل "
               "هذا التمييز إلا صيغًا معيّنة، لذلك ستفوته صيغ أخرى. ولا تُنشأ "
               "أسئلة جديدة، ولا يُتحقَّق من صحة فكرتك هندسيًا."),
    },
    # T2-G-2 (`T2G-CONCISE-MIXED-IMPLEMENT-02`): shown ONLY on projects recorded
    # under the T2-G-2 engine-contract version. `UI_T1D_QUESTION_SET` and
    # `UI_T2G_QUESTION_SET` above are RETAINED byte-unchanged and stay the
    # accurate disclosures for the projects they already describe. This wording
    # adds the bounded concise/mixed recognition and its limits; it claims no
    # general understanding and no engineering verification.
    "UI_T2G2_QUESTION_SET": {
        "en": ("These questions come from a fixed, reviewed set. This version "
               "chooses which one to show from what your project already "
               "records, using fixed rules — including recognising some ways "
               "of saying you do not know something yet, and some short "
               "explanations or ones written in the same sentence as an "
               "uncertainty. That recognition covers only certain phrasings, "
               "so it will miss others. No new questions are generated, it "
               "does not understand your writing in general, and whether your "
               "idea is engineering-correct is not checked."),
        "ar": ("تأتي هذه الأسئلة من مجموعة ثابتة ومراجَعة. ويختار هذا الإصدار "
               "أيها يعرض بناءً على ما سجّله مشروعك فعلًا، وفق قواعد ثابتة — "
               "بما في ذلك تمييز بعض صيغ قولك إنك لا تعرف شيئًا بعد، وبعض "
               "الشروح القصيرة أو المكتوبة في الجملة نفسها مع عبارة عدم "
               "المعرفة. ولا يشمل هذا التمييز إلا صيغًا معيّنة، لذلك ستفوته "
               "صيغ أخرى. ولا تُنشأ أسئلة جديدة، وهو لا يفهم كتابتك بشكل عام، "
               "ولا يُتحقَّق من صحة فكرتك هندسيًا."),
    },
    # --- T2-D: optional contextual feedback on the displayed question -------
    # Copy describes SAVING TO THIS PROJECT and nothing more. It never promises
    # that a team receives or reviews it, never claims anonymity, never implies
    # automatic learning, and never describes a retention or erasure policy that
    # is not implemented.
    "UI_T2D_PROMPT": {
        "en": "Was this question useful for your idea? (optional)",
        "ar": "هل كان هذا السؤال مفيدًا لفكرتك؟ (اختياري)",
    },
    "UI_T2D_NOTE": {
        "en": ("Your choice is saved to this project so you can see it later. "
               "It does not change the questions you are asked, and you can "
               "skip it."),
        "ar": ("يُحفظ اختيارك في هذا المشروع لتراه لاحقًا. وهو لا يغيّر الأسئلة "
               "التي تُطرح عليك، ويمكنك تخطّيه."),
    },
    "UI_T2D_CHOICE_HELPFUL": {"en": "Helpful", "ar": "مفيد"},
    "UI_T2D_CHOICE_UNCLEAR": {"en": "Unclear", "ar": "غير واضح"},
    "UI_T2D_CHOICE_NOT_RELEVANT": {
        "en": "Not relevant to my idea", "ar": "لا يناسب فكرتي",
    },
    "UI_T2D_SELECTED": {"en": "Your saved choice:", "ar": "اختيارك المحفوظ:"},
    "UI_T2D_NONE_CHOSEN": {"en": "No choice saved.", "ar": "لم يُحفظ أي اختيار."},
    "UI_T2D_CHANGE": {"en": "You can change it.", "ar": "يمكنك تغييره."},
    "UI_T2D_ACK_SAVED": {"en": "Saved to this project.",
                         "ar": "حُفظ في هذا المشروع."},
    # A historical replay acknowledges that the earlier request WAS recorded,
    # and deliberately does not claim that its choice is the current one — the
    # current choice is shown separately, only from validated readback.
    "UI_T2D_ACK_REPLAY": {
        "en": ("That request was already recorded earlier, so nothing was "
               "added. Your current saved choice is shown above."),
        "ar": ("سُجِّل ذلك الطلب سابقًا بالفعل، لذلك لم يُضف شيء. ويظهر اختيارك "
               "المحفوظ الحالي أعلاه."),
    },
    "UI_T2D_COLD_SELECTED": {
        "en": "Your saved choice for this question:",
        "ar": "اختيارك المحفوظ لهذا السؤال:",
    },
    "UI_T2D_COLD_NOTE": {
        "en": ("This is a read-only view of your saved project. Resume the "
               "session to change it."),
        "ar": ("هذا عرض للقراءة فقط لمشروعك المحفوظ. استأنف الجلسة لتغييره."),
    },
    "UI_T2D_ACK_UNCHANGED": {
        "en": "That is already your saved choice. Nothing changed.",
        "ar": "هذا هو اختيارك المحفوظ بالفعل. لم يتغير شيء.",
    },
    # --- T2-G legacy migration: explicit confirmed engine-version adoption ---
    # (`T2G-LEGACY-MIGRATION-IMPLEMENT-01`, Owner policy B). Copy is truthful
    # and bounded: it never says upgraded, improved, corrected, invalid, stale
    # or engineering-verified. BEFORE confirmation it states that the project
    # was created under earlier rules, what adopting the current rules can
    # change, that nothing is deleted or rewritten, and that adoption can be
    # reversed. AFTER adoption it states only that the project now runs under
    # the adopted current rules and that earlier questions and answers were
    # recorded under the earlier rules.
    "UI_EVA_HEADING": {
        "en": "Run this project under the current rules (optional)",
        "ar": "تشغيل هذا المشروع وفق القواعد الحالية (اختياري)",
    },
    "UI_EVA_BEFORE_CREATED": {
        "en": ("This project was created under an earlier version of the rules "
               "that choose which question to show and decide when an answer "
               "counts."),
        "ar": ("أُنشئ هذا المشروع وفق إصدار أسبق من القواعد التي تختار السؤال "
               "المعروض وتحدد متى تُحتسب الإجابة."),
    },
    "UI_EVA_BEFORE_CHANGE": {
        "en": ("If you adopt the current rules, everything is recomputed from "
               "your saved answers under those rules. Mechanism knowledge that "
               "was previously counted can change, and an earlier question may "
               "be asked again."),
        "ar": ("إذا اعتمدت القواعد الحالية، يُعاد حساب كل شيء من إجاباتك "
               "المحفوظة وفق تلك القواعد. وقد تتغير معرفة الآلية التي احتُسبت "
               "سابقًا، وقد يُطرح سؤال سابق مرة أخرى."),
    },
    "UI_EVA_BEFORE_KEEP": {
        "en": ("No answer, evidence or recorded history is deleted or "
               "rewritten. The version this project was created under stays "
               "recorded."),
        "ar": ("لا تُحذف أي إجابة أو دليل أو سجل محفوظ ولا يُعاد كتابته. ويبقى "
               "الإصدار الذي أُنشئ به هذا المشروع مسجّلًا."),
    },
    "UI_EVA_BEFORE_REVERSE": {
        "en": "You can later return this project to the earlier rules.",
        "ar": "يمكنك لاحقًا إعادة هذا المشروع إلى القواعد السابقة.",
    },
    "UI_EVA_CONFIRM_LABEL": {
        "en": "I understand what can change, and I want this project to run under the current rules.",
        "ar": "أفهم ما قد يتغير، وأريد تشغيل هذا المشروع وفق القواعد الحالية.",
    },
    "UI_EVA_BUTTON": {
        "en": "Adopt the current rules",
        "ar": "اعتمد القواعد الحالية",
    },
    "UI_EVA_AFTER": {
        "en": ("This project now runs under the adopted current rules. Its "
               "earlier questions and answers were originally recorded under "
               "the earlier rules."),
        "ar": ("يعمل هذا المشروع الآن وفق القواعد الحالية المعتمدة. وقد سُجّلت "
               "أسئلته وإجاباته السابقة أصلًا وفق القواعد السابقة."),
    },
    "UI_EVA_REVERT_EXPLAIN": {
        "en": ("Returning to the earlier rules recomputes everything from your "
               "saved answers under those rules again. Nothing is deleted or "
               "rewritten; the adoption history stays recorded."),
        "ar": ("العودة إلى القواعد السابقة تعيد حساب كل شيء من إجاباتك المحفوظة "
               "وفق تلك القواعد مرة أخرى. لا يُحذف شيء ولا يُعاد كتابته، ويبقى "
               "سجل الاعتماد محفوظًا."),
    },
    "UI_EVA_REVERT_CONFIRM_LABEL": {
        "en": "I understand what can change, and I want this project to return to the earlier rules.",
        "ar": "أفهم ما قد يتغير، وأريد إعادة هذا المشروع إلى القواعد السابقة.",
    },
    "UI_EVA_REVERT_BUTTON": {
        "en": "Return to the earlier rules",
        "ar": "العودة إلى القواعد السابقة",
    },
    "UI_EVA_COLD_NOTE": {
        "en": ("This saved project runs under rules it adopted after it was "
               "created; its earlier questions and answers were recorded under "
               "the earlier rules."),
        "ar": ("يعمل هذا المشروع المحفوظ وفق قواعد اعتمدها بعد إنشائه؛ وقد سُجّلت "
               "أسئلته وإجاباته السابقة وفق القواعد السابقة."),
    },
    "UI_EVA_ACK_ADOPTED": {
        "en": ("This project now runs under the current rules. Everything "
               "shown has been recomputed from your saved answers."),
        "ar": ("يعمل هذا المشروع الآن وفق القواعد الحالية. وقد أُعيد حساب كل ما "
               "يظهر من إجاباتك المحفوظة."),
    },
    "UI_EVA_ACK_REVERTED": {
        "en": ("This project has returned to the earlier rules. Everything "
               "shown has been recomputed from your saved answers."),
        "ar": ("عاد هذا المشروع إلى القواعد السابقة. وقد أُعيد حساب كل ما يظهر "
               "من إجاباتك المحفوظة."),
    },
    "UI_EVA_ACK_REPLAY": {
        "en": ("That request was already recorded earlier, so nothing was "
               "added."),
        "ar": "سُجِّل ذلك الطلب سابقًا بالفعل، لذلك لم يُضف شيء.",
    },
    "UI_EVA_ERR_NOT_APPLIED": {
        "en": ("That change could not be applied just now. Nothing was "
               "changed."),
        "ar": "تعذّر تطبيق ذلك التغيير الآن. لم يتغير شيء.",
    },
    "UI_EVA_ERR_SAVED_NOT_SHOWN": {
        "en": ("Your choice of rules was saved, but the page could not be "
               "updated just now. What you see below has not changed yet. It "
               "will be reflected whenever this project can be rebuilt "
               "successfully."),
        "ar": ("حُفظ اختيارك للقواعد، لكن تعذّر تحديث الصفحة الآن. ما تراه أدناه "
               "لم يتغير بعد، وسينعكس متى أمكن إعادة بناء هذا المشروع بنجاح."),
    },
    "UI_EVA_ERR_UNKNOWN": {
        "en": ("We could not confirm whether that change was saved. Reload this "
               "page to see which rules your project currently runs under."),
        "ar": ("تعذّر التأكد مما إذا كان ذلك التغيير قد حُفظ. أعد تحميل هذه الصفحة "
               "لترى القواعد التي يعمل بها مشروعك حاليًا."),
    },
    "UI_T2D_ERR_NOT_SAVED": {
        "en": "That could not be saved just now. Nothing was changed.",
        "ar": "تعذّر حفظ ذلك الآن. لم يتغير أي شيء.",
    },
    "UI_T2D_ERR_MOVED_ON": {
        # Says only that THIS request changed nothing. It never claims that an
        # earlier request saved nothing — a genuinely recorded earlier event is
        # acknowledged by UI_T2D_ACK_REPLAY instead.
        "en": ("This page has moved on since that choice was shown, so this "
               "request changed nothing. Reload the page to see your current "
               "saved choice and choose again."),
        "ar": ("تغيّرت هذه الصفحة منذ عرض ذلك الاختيار، لذلك لم يغيّر هذا الطلب "
               "شيئًا. أعد تحميل الصفحة لترى اختيارك المحفوظ الحالي واختر من "
               "جديد."),
    },
    "UI_T2D_ERR_UNKNOWN": {
        "en": ("We could not confirm whether that was saved. Reload this page "
               "and check before choosing again."),
        "ar": ("لم نتمكن من تأكيد ما إذا كان ذلك قد حُفظ. أعد تحميل هذه الصفحة "
               "وتحقق قبل الاختيار من جديد."),
    },
    "UI_T2D_ERR_SAVED_NOT_SHOWN": {
        "en": "That was saved, but it cannot be shown right now. Reload this page.",
        "ar": "حُفظ ذلك، لكن يتعذّر عرضه الآن. أعد تحميل هذه الصفحة.",
    },
    "UI_T2D_ERR_CAP": {
        "en": ("This project has reached the limit for saved question feedback. "
               "Nothing was changed and nothing earlier was removed."),
        "ar": ("بلغ هذا المشروع الحد الأقصى لملاحظات الأسئلة المحفوظة. لم يتغير "
               "شيء ولم يُحذف أي شيء سابق."),
    },
    # --- T2-E Option B: owner-recorded, explicitly UNVERIFIED evidence ------
    # Every line below states, in both languages, that this is something the
    # inventor recorded and that InventorAI has verified none of it. No line
    # implies regulatory approval, completed testing, independent verification,
    # specialist review as an established fact, certification, or proof. Copy
    # exists ONLY for the state this increment actually makes reachable.
    "UI_T2E_HEADING": {
        "en": "Recorded external review or support (not verified)",
        "ar": "مراجعة أو إسناد خارجي مُسجَّل (غير مُتحقَّق منه)",
    },
    "UI_T2E_INTRO": {
        "en": ("You can record who you say reviewed or supports one of your "
               "answers, when that happened, what it covered, and what it did "
               "not cover. InventorAI has not contacted that person or source, "
               "has not seen the material, and has not checked any of it. This "
               "is kept as your own recorded statement."),
        "ar": ("يمكنك تسجيل من تقول إنه راجع أحد إجاباتك أو يدعمها، ومتى حدث "
               "ذلك، وما الذي غطّاه، وما الذي لم يغطّه. لم تتواصل InventorAI مع "
               "ذلك الشخص أو المصدر، ولم تطّلع على المادة، ولم تتحقق من أي منها. "
               "ويُحفظ ذلك بوصفه إفادتك المسجّلة أنت."),
    },
    "UI_T2E_STATUS_UNVERIFIED": {
        "en": "Recorded by the inventor — not verified by InventorAI",
        "ar": "سجّله المخترع — لم تتحقق منه InventorAI",
    },
    "UI_T2E_NOT_CERTIFICATION": {
        "en": ("Recording this does not make the answer specialist-reviewed, "
               "empirically demonstrated, independently verified, certified, or "
               "validated. Its evidence status is unchanged."),
        "ar": ("تسجيل ذلك لا يجعل الإجابة «مراجَعة من مختص» أو «مُثبَتة تجريبيًا» "
               "أو «مُتحقَّقًا منها باستقلال» أو معتمَدة أو مُتحقَّقة. وحالة أدلتها "
               "لم تتغير."),
    },
    "UI_T2E_SOURCE_LABEL": {"en": "Who you say reviewed or supports it:",
                            "ar": "من تقول إنه راجعها أو يدعمها:"},
    "UI_T2E_DATE_LABEL": {"en": "When it happened (YYYY-MM-DD):",
                          "ar": "متى حدث ذلك (سنة-شهر-يوم):"},
    "UI_T2E_SCOPE_LABEL": {"en": "What it covered:", "ar": "ما الذي غطّاه:"},
    "UI_T2E_LIMITATION_LABEL": {
        "en": "What it did NOT cover (required):",
        "ar": "ما الذي لم يغطّه (مطلوب):",
    },
    "UI_T2E_LIMITATION_HINT": {
        "en": ("Say plainly what was left out. A record with no stated limit "
               "cannot be saved."),
        "ar": ("اذكر بوضوح ما الذي استُثني. لا يمكن حفظ سجل بلا حدّ مذكور."),
    },
    "UI_T2E_ANCHOR_LABEL": {"en": "Which answer this is about:",
                            "ar": "أي إجابة يتعلق بها ذلك:"},
    "UI_T2E_SUBMIT": {"en": "Record this", "ar": "سجّل ذلك"},
    "UI_T2E_WITHDRAW": {"en": "Withdraw this record", "ar": "اسحب هذا السجل"},
    "UI_T2E_WITHDRAWN": {
        "en": "Withdrawn by the inventor — kept in history, no longer current",
        "ar": "سحبه المخترع — محفوظ في السجل ولم يعد ساريًا",
    },
    "UI_T2E_REPLACES": {
        "en": "This replaces an earlier record; the earlier one is kept in history.",
        "ar": "يحل هذا محل سجل أسبق؛ والسجل الأسبق محفوظ في التاريخ.",
    },
    "UI_T2E_CONFIRM_HEADING": {"en": "Confirm what will be recorded",
                               "ar": "أكّد ما سيُسجَّل"},
    "UI_T2E_CONFIRM": {"en": "Confirm", "ar": "تأكيد"},
    "UI_T2E_DISCARD": {"en": "Discard", "ar": "تجاهل"},
    "UI_T2E_NONE_RECORDED": {
        "en": "Nothing recorded for this answer.",
        "ar": "لا يوجد شيء مسجّل لهذه الإجابة.",
    },
    # --- outcomes. Rejected input is NOT kept: each message names the field
    #     and asks for re-entry, and never echoes what was typed.
    "UI_T2E_ACK_SAVED": {"en": "Recorded.", "ar": "تم التسجيل."},
    "UI_T2E_ACK_WITHDRAWN": {
        "en": "Withdrawn. The earlier record is kept in your project history.",
        "ar": "تم السحب. والسجل الأسبق محفوظ في تاريخ مشروعك.",
    },
    "UI_T2E_ACK_DISCARDED": {"en": "Discarded. Nothing was recorded.",
                             "ar": "تم التجاهل. لم يُسجَّل أي شيء."},
    "UI_T2E_ERR_NOT_SAVED": {
        "en": "That could not be recorded just now. Nothing was changed.",
        "ar": "تعذّر تسجيل ذلك الآن. لم يتغير أي شيء.",
    },
    "UI_T2E_ERR_CONFLICT": {
        "en": ("What is recorded for this answer changed while you were "
               "confirming, so nothing was recorded. Review it and enter it "
               "again."),
        "ar": ("تغيّر ما هو مسجّل لهذه الإجابة أثناء تأكيدك، لذلك لم يُسجَّل شيء. "
               "راجعه وأدخله من جديد."),
    },
    "UI_T2E_ERR_OUTCOME_UNKNOWN": {
        "en": ("We could not confirm whether that was recorded. Reload this "
               "page and check before entering it again."),
        "ar": ("لم نتمكن من تأكيد ما إذا كان ذلك قد سُجِّل. أعد تحميل هذه الصفحة "
               "وتحقق قبل إدخاله من جديد."),
    },
    "UI_T2E_ERR_SAVED_NOT_SHOWN": {
        "en": ("That was recorded, but it cannot be shown right now. Reload "
               "this page."),
        "ar": "سُجِّل ذلك، لكن يتعذّر عرضه الآن. أعد تحميل هذه الصفحة.",
    },
    "UI_T2E_ERR_SOURCE": {
        "en": ("Enter who you say reviewed or supports it, as short plain "
               "text. Nothing was saved — please enter it again."),
        "ar": ("أدخل من تقول إنه راجعها أو يدعمها، كنص قصير. لم يُحفظ شيء — "
               "يُرجى إدخاله من جديد."),
    },
    "UI_T2E_ERR_DATE": {
        "en": ("Enter when it happened as a real date in the form YYYY-MM-DD. "
               "Nothing was saved — please enter it again."),
        "ar": ("أدخل تاريخ حدوثه كتاريخ حقيقي بصيغة سنة-شهر-يوم. لم يُحفظ شيء "
               "— يُرجى إدخاله من جديد."),
    },
    "UI_T2E_ERR_SCOPE": {
        "en": ("Enter what it covered, as short plain text. Nothing was saved "
               "— please enter it again."),
        "ar": ("أدخل ما الذي غطّاه، كنص قصير. لم يُحفظ شيء — يُرجى إدخاله من "
               "جديد."),
    },
    "UI_T2E_ERR_LIMITATION": {
        "en": ("Enter what it did NOT cover, as short plain text. This is "
               "required. Nothing was saved — please enter it again."),
        "ar": ("أدخل ما الذي لم يغطّه، كنص قصير. وهذا مطلوب. لم يُحفظ شيء — "
               "يُرجى إدخاله من جديد."),
    },
    "UI_T1D_EVIDENCE_PROGRESSION": {
        "en": ("This version records evidence status conservatively. The guided journey "
               "here does not move your statements into the specialist-reviewed, "
               "empirically demonstrated, or independently verified states, so those "
               "labels should not be read as certification, completed validation, or "
               "proof."),
        "ar": ("يسجّل هذا الإصدار حالة الأدلة بتحفّظ. والرحلة الموجَّهة هنا لا تنقل "
               "إفاداتك إلى حالات «مراجَع من مختص» أو «مُثبَت تجريبيًا» أو «مُتحقَّق "
               "منه باستقلال»، لذا لا ينبغي قراءة تلك التسميات على أنها اعتماد أو "
               "تحقق مكتمل أو إثبات."),
    },
    # T3-A "Project record" (T3A-PROJECT-RECORD-IMPLEMENT-01; OD-PDVG-02(b)
    # narrowed to input-history rendering). Chrome for the ONE read-only
    # record of what the inventor recorded, in saved order, with what was
    # later replaced or withdrawn and any rule change. Truthfulness rules
    # these strings are bound by: a withdrawal or replacement is the
    # inventor's own act and is never worded as a judgement that an earlier
    # entry was wrong; no entry claims an evaluation consequence; a missing
    # reason is stated plainly; no wall-clock order is implied for ledger
    # entries. Event labels are keyed UI_T3A_EVENT_<KIND> (kind upper-cased),
    # one entry per kind of `web/app.py::T3A_EVENT_KINDS`.
    # Manufacturing Evidence Capture (MANUFACTURING-EVIDENCE-OWNER-IMPLEMENT-01).
    # The wording carries the same boundary as the Commercial block, against a
    # sharper temptation: a list of materials, processes and tooling reads like
    # a production plan. It is not one. Nothing here says manufacturable,
    # prototype-ready, production-ready, cheap to make, tooling-ready,
    # supplier-ready, scalable or BOM-complete, and no string judges whether the
    # recorded evidence is enough — this lane produces no Manufacturing
    # Readiness conclusion and has no opinion to offer.
    # Topic labels are keyed UI_MEV_TOPIC_<TOPIC> (topic upper-cased), one per
    # member of `engine.commercial_evidence.MANUFACTURING_TOPICS`.
    "UI_MEV_HEADING": {
        "en": "Manufacturing evidence you recorded",
        "ar": "أدلة التصنيع التي سجّلتها",
    },
    "UI_MEV_EXPLAIN": {
        "en": ("What you know, or believe, about making this idea — what it "
               "would be made from, how, and with what. This evidence is "
               "recorded from your project information and has not been "
               "independently checked. It is not a plan for making the thing, "
               "and it does not say the thing can be made."),
        "ar": ("ما تعرفه، أو تعتقده، عن صنع هذه الفكرة — مما ستُصنع، وكيف، "
               "وبأي وسائل. هذه الأدلة مسجَّلة من معلومات مشروعك ولم يجرِ "
               "التحقق منها بشكل مستقل. ليست خطة للتصنيع، ولا تقول إن الشيء "
               "يمكن صنعه."),
    },
    "UI_MEV_EMPTY": {
        "en": ("No Manufacturing evidence has been recorded yet. That is simply "
               "a blank page, not a finding about how hard this would be to "
               "make."),
        "ar": ("لم تُسجَّل أي أدلة تصنيع بعد. هذه مجرد صفحة فارغة، وليست نتيجةً "
               "بشأن مدى صعوبة صنع هذا."),
    },
    "UI_MEV_ADD_HEADING": {
        "en": "Record one more item", "ar": "سجّل عنصرًا آخر"},
    "UI_MEV_FIELD_TOPIC": {"en": "Topic", "ar": "الموضوع"},
    "UI_MEV_FIELD_SUBJECT": {
        "en": "What this concerns", "ar": "ما يتعلق به هذا"},
    "UI_MEV_FIELD_STATEMENT": {
        "en": "What you know or believe", "ar": "ما تعرفه أو تعتقده"},
    "UI_MEV_FIELD_SOURCE": {
        "en": "Where this came from", "ar": "من أين جاء هذا"},
    "UI_MEV_FIELD_DATE": {
        "en": "Date, if you know it (YYYY-MM-DD)",
        "ar": "التاريخ، إن كنت تعرفه (YYYY-MM-DD)"},
    "UI_MEV_FIELD_SCOPE": {"en": "What it covers", "ar": "ما الذي يغطّيه"},
    "UI_MEV_FIELD_LIMITATION": {
        "en": "What it does NOT cover", "ar": "ما الذي لا يغطّيه"},
    "UI_MEV_LIMITATION_NOTE": {
        "en": ("Saying what your evidence does not cover is required. With "
               "manufacturing it matters most: a figure that held for one "
               "supplier, one quantity or one process is not a figure for all "
               "of them."),
        "ar": ("ذِكر ما لا تغطّيه أدلتك مطلوب. وفي التصنيع هو الأهم: رقم صحَّ "
               "مع مورّد واحد، أو كمية واحدة، أو عملية واحدة ليس رقمًا لها "
               "جميعًا."),
    },
    "UI_MEV_SUBMIT": {"en": "Record this", "ar": "سجّل هذا"},
    "UI_MEV_META_SOURCE": {"en": "Source", "ar": "المصدر"},
    "UI_MEV_META_DATE": {"en": "Date", "ar": "التاريخ"},
    "UI_MEV_META_SCOPE": {"en": "Covers", "ar": "يغطّي"},
    "UI_MEV_META_LIMITATION": {"en": "Does not cover", "ar": "لا يغطّي"},
    "UI_MEV_META_ORIGIN": {"en": "Recorded by", "ar": "سجّله"},
    "UI_MEV_META_ORIGIN_VALUE": {
        "en": "you, from your own knowledge", "ar": "أنت، من معرفتك الخاصة"},
    "UI_MEV_META_STANDING": {"en": "Standing", "ar": "الحالة"},
    "UI_MEV_META_STANDING_VALUE": {
        "en": "recorded, not checked by anyone",
        "ar": "مسجَّل، ولم يتحقق منه أحد"},
    "UI_MEV_META_NOTE": {
        "en": ("These two lines describe where each item came from and how far "
               "it has been checked. They are not settings and you cannot "
               "change them: everything you record here is your own statement, "
               "and this version of InventorAI verifies none of it."),
        "ar": ("يصف هذان السطران من أين جاء كل عنصر وإلى أي مدى جرى التحقق "
               "منه. ليسا إعدادات ولا يمكنك تغييرهما: كل ما تسجّله هنا هو "
               "قولك أنت، وهذه النسخة من إنفنتوراي لا تتحقق من أي منه."),
    },
    "UI_MEV_NOT_A_CONCLUSION": {
        "en": ("Recording this does not assess whether your idea can be made. "
               "This version does not evaluate manufacturing at all."),
        "ar": ("تسجيل هذا لا يقيّم ما إذا كان يمكن صنع فكرتك. هذه النسخة لا "
               "تقيّم التصنيع إطلاقًا."),
    },
    "UI_MEV_NOTICE_SAVED": {
        "en": "Recorded and saved to your project.",
        "ar": "سُجِّل وحُفِظ في مشروعك."},
    "UI_MEV_NOTICE_REPLAY": {
        "en": ("That item was already recorded earlier, so nothing was added a "
               "second time."),
        "ar": "سُجِّل ذلك العنصر سابقًا، فلم يُضَف مرة ثانية."},
    "UI_MEV_NOTICE_NOT_SAVED": {
        "en": "That item was not recorded. Nothing was changed.",
        "ar": "لم يُسجَّل ذلك العنصر. لم يتغير شيء."},
    "UI_MEV_NOTICE_TEXT_REJECTED": {
        "en": ("That text is too long, empty, or contains an invalid "
               "character. Nothing was saved - please correct it and try "
               "again."),
        "ar": ("ذلك النص طويل جدًا، أو فارغ، أو يحتوي على رمز غير صالح. لم "
               "يُحفظ شيء — يُرجى تصحيحه والمحاولة من جديد."),
    },
    "UI_MEV_NOTICE_UNKNOWN": {
        "en": ("We could not confirm whether that item was recorded. Reload "
               "this page to see the current list before trying again."),
        "ar": ("تعذّر علينا تأكيد ما إذا كان ذلك العنصر قد سُجِّل. أعد تحميل "
               "هذه الصفحة لرؤية القائمة الحالية قبل المحاولة مجددًا."),
    },
    "UI_MEV_NOTICE_CAP": {
        "en": ("This project already holds as many evidence items as it can. "
               "Nothing was saved."),
        "ar": ("يحتوي هذا المشروع بالفعل على أقصى عدد ممكن من عناصر الأدلة. لم "
               "يُحفظ شيء."),
    },
    "UI_MEV_TOPIC_PROTOTYPE_MATURITY": {
        "en": "How far the prototype has got", "ar": "إلى أين وصل النموذج الأولي"},
    "UI_MEV_TOPIC_MATERIAL": {
        "en": "What it would be made from", "ar": "مما ستُصنع"},
    "UI_MEV_TOPIC_COMPONENT": {
        "en": "A part it would need", "ar": "جزء ستحتاجه"},
    "UI_MEV_TOPIC_SPECIFICATION": {
        "en": "A figure it has to meet", "ar": "رقم يجب أن تحققه"},
    "UI_MEV_TOPIC_TOLERANCE": {
        "en": "How exact something must be", "ar": "مدى الدقة المطلوبة"},
    "UI_MEV_TOPIC_PROCESS": {
        "en": "How it would be made", "ar": "كيف ستُصنع"},
    "UI_MEV_TOPIC_TOOLING": {
        "en": "Tools or moulds it would need", "ar": "أدوات أو قوالب ستحتاجها"},
    "UI_MEV_TOPIC_SUPPLIER": {
        "en": "Who could supply or make it", "ar": "من يمكنه التوريد أو التصنيع"},
    "UI_MEV_TOPIC_COST": {
        "en": "What making it would cost", "ar": "كم سيكلّف صنعها"},
    "UI_MEV_TOPIC_MANUFACTURABILITY": {
        "en": "Something that makes it harder or easier to make",
        "ar": "ما يجعل صنعها أصعب أو أسهل"},
    # Readiness Snapshot (READINESS-SNAPSHOT-RUNTIME-01) — the first runtime
    # presentation of Readiness. Every string below is about the state of the
    # EVIDENCE, never about the idea. The hardest thing this copy has to do is
    # stop a reader converting an absence into a negative: "no Commercial
    # evidence recorded" must not read as "no market", "not assessed" must not
    # read as "hard to manufacture", and "not verified" must not read as "does
    # not work". Each row therefore says what is missing AND says plainly what
    # that does not mean. Only INSUFFICIENT_EVIDENCE is reachable in this
    # version, so no wording for a positive state exists here to be reached by
    # accident.
    "UI_RS_HEADING": {
        "en": "Evidence so far",
        "ar": "الأدلة حتى الآن",
    },
    "UI_RS_EXPLAIN": {
        "en": ("What evidence your project currently holds for each area. This "
               "is a summary of what has been recorded — it is not a judgement "
               "about your idea, and it does not tell you whether to continue. "
               "Your project's own recommendation is shown separately."),
        "ar": ("ما الأدلة التي يحتويها مشروعك حاليًا في كل مجال. هذا ملخّص لما "
               "جرى تسجيله — وليس حكمًا على فكرتك، ولا يخبرك إن كنت ستتابع أم "
               "لا. توصية مشروعك تُعرض على حدة."),
    },
    "UI_RS_DISPOSITION_INSUFFICIENT_EVIDENCE": {
        "en": "Insufficient evidence",
        "ar": "الأدلة غير كافية",
    },
    "UI_RS_NO_OVERALL": {
        "en": ("These rows are reported separately and are not added up. There "
               "is no overall readiness result, because none of them is a "
               "score and combining them would invent a judgement none of them "
               "makes."),
        "ar": ("تُعرض هذه الصفوف بشكل منفصل ولا تُجمع. لا توجد نتيجة جاهزية "
               "إجمالية، لأن أيًا منها ليس درجة، وجمعها سيخترع حكمًا لا يصدر "
               "عن أي منها."),
    },
    "UI_RS_DIM_TECHNICAL": {"en": "Technical", "ar": "التقني"},
    "UI_RS_DIM_COMMERCIAL": {"en": "Commercial", "ar": "التجاري"},
    "UI_RS_DIM_MANUFACTURING": {"en": "Manufacturing", "ar": "التصنيع"},
    "UI_RS_DIM_INTEGRATION": {"en": "Integration", "ar": "التكامل"},
    # --- Technical -----------------------------------------------------------
    "UI_RS_TECHNICAL_WHY": {
        "en": ("You have recorded technical reasoning, and it is kept at the "
               "level it was given: stated, or reasoned. This version of "
               "InventorAI has no way for anyone — a specialist, a test result, "
               "or the system itself — to mark technical evidence as checked, "
               "so no project can reach a verified technical result here."),
        "ar": ("لقد سجّلت تعليلًا تقنيًا، وهو محفوظ بالمستوى الذي قُدّم به: "
               "مذكور، أو معلَّل. لا تتيح هذه النسخة من إنفنتوراي لأي جهة — "
               "أخصائي، أو نتيجة اختبار، أو النظام نفسه — وضع علامة على الأدلة "
               "التقنية بأنها مُتحقَّق منها، لذلك لا يمكن لأي مشروع بلوغ نتيجة "
               "تقنية مُتحقَّقة هنا."),
    },
    "UI_RS_TECHNICAL_NOT_A_VERDICT": {
        "en": ("This is a limit of this version, not a finding about your idea. "
               "It does not mean your idea will not work."),
        "ar": ("هذا قيد في هذه النسخة، وليس نتيجة بشأن فكرتك. لا يعني أن فكرتك "
               "لن تنجح."),
    },
    "UI_RS_TECHNICAL_COUNTS": {
        "en": "Recorded entries: %(items)s · Areas covered: %(areas)s",
        "ar": "الإدخالات المسجَّلة: %(items)s · المجالات المشمولة: %(areas)s",
    },
    "UI_RS_TECHNICAL_NOT_A_CONCLUSION": {
        "en": ("This counts what you recorded. It is not a view on whether your "
               "idea works."),
        "ar": "هذا يحصي ما سجّلته. وليس رأيًا في ما إذا كانت فكرتك تعمل.",
    },
    "UI_RS_TECHNICAL_NONE": {
        "en": "No technical reasoning has been recorded yet.",
        "ar": "لم يُسجَّل أي تعليل تقني بعد.",
    },
    # --- Commercial ----------------------------------------------------------
    "UI_RS_COMMERCIAL_NOTHING": {
        "en": "No Commercial evidence has been recorded yet.",
        "ar": "لم تُسجَّل أي أدلة تجارية بعد.",
    },
    "UI_RS_COMMERCIAL_NOTHING_NOT_A_VERDICT": {
        "en": ("Nothing has been recorded here yet, which says nothing about "
               "your market. It is a blank page, not a finding."),
        "ar": ("لم يُسجَّل شيء هنا بعد، وهذا لا يقول شيئًا عن سوقك. إنها صفحة "
               "فارغة، وليست نتيجة."),
    },
    "UI_RS_COMMERCIAL_RECORDED": {
        "en": ("Commercial evidence has been recorded, but it has not yet been "
               "independently checked."),
        "ar": ("سُجِّلت أدلة تجارية، لكنها لم تخضع بعد لفحص مستقل."),
    },
    "UI_RS_COMMERCIAL_COUNTS": {
        "en": "Recorded items: %(items)s · Topics covered: %(topics)s",
        "ar": "العناصر المسجَّلة: %(items)s · المواضيع المشمولة: %(topics)s",
    },
    "UI_RS_COMMERCIAL_ALL_UNCHECKED": {
        "en": "Every item is your own statement, recorded as you gave it.",
        "ar": "كل عنصر هو قولك أنت، مسجَّل كما قدّمته.",
    },
    "UI_RS_COMMERCIAL_TOPICS_LABEL": {
        "en": "Topics recorded", "ar": "المواضيع المسجَّلة"},
    "UI_RS_COMMERCIAL_NOT_A_CONCLUSION": {
        "en": ("This counts what you recorded. It is not a view on your market, "
               "your pricing, or whether anyone will buy."),
        "ar": ("هذا يحصي ما سجّلته. وليس رأيًا في سوقك، ولا في تسعيرك، ولا في "
               "ما إذا كان أحد سيشتري."),
    },
    # --- Manufacturing (MANUFACTURING-READINESS-SNAPSHOT-01) -----------------
    # Manufacturing joins as an EVIDENCE-SUFFICIENCY dimension. The row now
    # reports a disposition where it previously reported "not assessed", and the
    # entire risk of that change is a reader hearing "insufficient evidence
    # about manufacturing" as "this would be hard to manufacture". Every string
    # below is written against that reading.
    "UI_RS_MANUFACTURING_NOTHING": {
        "en": "No Manufacturing evidence has been recorded yet.",
        "ar": "لم تُسجَّل أي أدلة تصنيع بعد.",
    },
    "UI_RS_MANUFACTURING_NOTHING_NOT_A_VERDICT": {
        "en": ("Nothing has been recorded here yet, which says nothing about "
               "how hard this would be to make. It is a blank page, not a "
               "finding."),
        "ar": ("لم يُسجَّل شيء هنا بعد، وهذا لا يقول شيئًا عن مدى صعوبة صنع "
               "هذا. إنها صفحة فارغة، وليست نتيجة."),
    },
    "UI_RS_MANUFACTURING_RECORDED": {
        "en": ("Manufacturing evidence has been recorded, but it has not yet "
               "been independently checked."),
        "ar": "سُجِّلت أدلة تصنيع، لكنها لم تخضع بعد لفحص مستقل.",
    },
    "UI_RS_MANUFACTURING_COUNTS": {
        "en": "Recorded items: %(items)s · Topics covered: %(topics)s",
        "ar": "العناصر المسجَّلة: %(items)s · المواضيع المشمولة: %(topics)s",
    },
    "UI_RS_MANUFACTURING_ALL_UNCHECKED": {
        "en": "Every item is your own statement, recorded as you gave it.",
        "ar": "كل عنصر هو قولك أنت، مسجَّل كما قدّمته.",
    },
    "UI_RS_MANUFACTURING_TOPICS_LABEL": {
        "en": "Topics recorded", "ar": "المواضيع المسجَّلة"},
    "UI_RS_MANUFACTURING_NOT_A_CONCLUSION": {
        "en": ("This counts what you recorded. It is not a view on whether your "
               "idea can be made, how easily, or at what cost — this version "
               "does not judge that at all."),
        "ar": ("هذا يحصي ما سجّلته. وليس رأيًا في ما إذا كان يمكن صنع فكرتك، "
               "ولا في مدى سهولة ذلك، ولا في تكلفته — هذه النسخة لا تحكم في "
               "ذلك إطلاقًا."),
    },
    # --- Integration (Stage 15 closure — the IRL-compatible view) ------------
    # The risk is a reader hearing "insufficient integration evidence" as "the
    # parts do not work together", or reading the row as an integration
    # readiness level. Every string below is written against both readings.
    "UI_RS_INTEGRATION_NOTHING": {
        "en": "No integration evidence has been recorded yet.",
        "ar": "لم تُسجَّل أي أدلة تكامل بعد.",
    },
    "UI_RS_INTEGRATION_NOTHING_NOT_A_VERDICT": {
        "en": ("Nothing has been recorded here yet, which says nothing about "
               "whether the parts of your invention work together. It is a "
               "blank page, not a finding. Integration evidence applies only "
               "when your invention combines a mechanical and an electrical / "
               "electronic part and you have declared how they interact."),
        "ar": ("لم يُسجَّل شيء هنا بعد، وهذا لا يقول شيئًا عن ما إذا كانت "
               "أجزاء اختراعك تعمل معًا. إنها صفحة فارغة، وليست نتيجة. أدلة "
               "التكامل تخصّ فقط اختراعًا يجمع جزءًا ميكانيكيًا وجزءًا "
               "كهربائيًا / إلكترونيًا صرّحتَ بكيفية تفاعلهما."),
    },
    "UI_RS_INTEGRATION_RECORDED": {
        "en": ("Integration evidence has been recorded, but it has not yet been "
               "independently checked."),
        "ar": "سُجِّلت أدلة تكامل، لكنها لم تخضع بعد لفحص مستقل.",
    },
    "UI_RS_INTEGRATION_COUNTS": {
        "en": "Recorded items: %(items)s · Topics covered: %(topics)s",
        "ar": "العناصر المسجَّلة: %(items)s · المواضيع المشمولة: %(topics)s",
    },
    "UI_RS_INTEGRATION_ALL_UNCHECKED": {
        "en": "Every item is your own statement, recorded as you gave it.",
        "ar": "كل عنصر هو قولك أنت، مسجَّل كما قدّمته.",
    },
    "UI_RS_INTEGRATION_TOPICS_LABEL": {
        "en": "Topics recorded", "ar": "المواضيع المسجَّلة"},
    "UI_RS_INTEGRATION_NOT_A_CONCLUSION": {
        "en": ("This counts what you recorded. It is not an integration "
               "readiness level and not a view on whether the parts are "
               "compatible — this version does not judge that at all. Your "
               "recorded checks of each interaction are not evidence and are "
               "not counted here."),
        "ar": ("هذا يحصي ما سجّلته. وليس مستوى جاهزية للتكامل، ولا رأيًا في "
               "ما إذا كان الجزآن متوافقين — هذه النسخة لا تحكم في ذلك "
               "إطلاقًا. الفحوص التي سجّلتها لكل تفاعل ليست أدلة ولا تُحتسب "
               "هنا."),
    },
    # --- Manufacturing -------------------------------------------------------
    # Commercial Evidence Capture (COMMERCIAL-EVIDENCE-CAPTURE-IMPLEMENT-01).
    # The wording carries the whole product boundary: this block shows what the
    # inventor RECORDED about their market, never what is true about it. No
    # string here says validated, proven, strong, attractive, marketable or
    # ready, and no string judges how much evidence is enough — because this
    # lane computes no Commercial Readiness and has no opinion to offer.
    # Topic labels are keyed UI_CEV_TOPIC_<TOPIC> (topic upper-cased), one per
    # member of `engine.commercial_evidence.COMMERCIAL_TOPICS`.
    "UI_CEV_HEADING": {
        "en": "Commercial evidence you recorded",
        "ar": "الأدلة التجارية التي سجّلتها",
    },
    "UI_CEV_EXPLAIN": {
        # The Owner's §5 example wording used "has not been independently
        # validated". The plainer "checked" is used instead for one concrete
        # reason: `test_g3_decision_value.py::test_a22` bans the bare token
        # `validated` anywhere on this page, so that a withdrawn decision
        # alternative can never read as a validated one. That guard is worth
        # more than the word, and weakening it to fit this copy would trade a
        # real product-truth protection for a synonym.
        "en": ("What you know, or believe, about the market for this idea — "
               "who it is for, what it would replace, what it might cost. "
               "This evidence is recorded from your project information and "
               "has not been independently checked. InventorAI has verified "
               "none of it, and recording it does not make it true."),
        "ar": ("ما تعرفه، أو تعتقده، عن السوق لهذه الفكرة — لمن هي، وما الذي "
               "ستحلّ محلّه، وكم قد تُكلّف. هذه الأدلة مسجَّلة من معلومات "
               "مشروعك ولم يجرِ التحقق منها بشكل مستقل. لم يتحقق إنفنتوراي من "
               "أي منها، وتسجيلها لا يجعلها صحيحة."),
    },
    "UI_CEV_EMPTY": {
        "en": ("No Commercial evidence has been recorded yet. That is simply "
               "a blank page, not a finding about your market."),
        "ar": ("لم تُسجَّل أي أدلة تجارية بعد. هذه مجرد صفحة فارغة، وليست "
               "نتيجةً بشأن سوقك."),
    },
    # --- Commercial evidence GAPS (Stage 17 bounded presentation) -----------
    # These three strings carry the whole truth boundary of the gap block, so
    # they are worded to be unusable as a finding. "Not yet recorded" is a fact
    # about the page; "no market", "no demand" and "not viable" are claims about
    # the world, and this product makes none of them. The EN and AR say the same
    # thing, including the disclaimer — a gap list that warned in one language
    # only would be worse than no list.
    # --- D1 lifecycle: correct, withdraw, and the history that results -------
    # The lifecycle words carry the whole meaning of this slice, so EN and AR
    # must say the same thing about the same three states. "Replaced" and
    # "withdrawn" are statements about the RECORD, never about the market and
    # never about the owner who wrote it: an earlier version is not a mistake
    # and a withdrawal is not a failure.
    # --- D2 quantitative structure -------------------------------------
    # The wording carries the rule: an amount needs a basis, and "Not
    # established" is offered as an ANSWER rather than as a blank. Neither
    # language may imply that a recorded estimate has been checked or agreed.
    "UI_CEV_Q_HEADING": {
        "en": "Amount",
        "ar": "\u0627\u0644\u0645\u0628\u0644\u063a",
    },
    "UI_CEV_Q_EXPLAIN": {
        "en": "Record an amount only if you can say where it came from. If you cannot, leave this as \u201cNot established\u201d \u2014 that is a real answer, not a gap to fill with a guess. An estimate recorded here is still your own estimate: InventorAI has checked none of it.",
        "ar": "\u0633\u062c\u0651\u0644 \u0645\u0628\u0644\u063a\u064b\u0627 \u0641\u0642\u0637 \u0625\u0630\u0627 \u0643\u0627\u0646 \u0628\u0625\u0645\u0643\u0627\u0646\u0643 \u0628\u064a\u0627\u0646 \u0645\u0635\u062f\u0631\u0647. \u0648\u0625\u0630\u0627 \u0644\u0645 \u062a\u0633\u062a\u0637\u0639\u060c \u0641\u0627\u062a\u0631\u0643 \u0627\u0644\u062d\u0642\u0644 \u0639\u0644\u0649 \u201c\u063a\u064a\u0631 \u0645\u062d\u062f\u064e\u0651\u062f\u201d \u2014 \u0641\u0647\u0630\u0647 \u0625\u062c\u0627\u0628\u0629 \u062d\u0642\u064a\u0642\u064a\u0629 \u0648\u0644\u064a\u0633\u062a \u0641\u0631\u0627\u063a\u064b\u0627 \u064a\u064f\u0645\u0644\u0623 \u0628\u0627\u0644\u062a\u062e\u0645\u064a\u0646. \u0648\u0627\u0644\u062a\u0642\u062f\u064a\u0631 \u0627\u0644\u0645\u0633\u062c\u064e\u0651\u0644 \u0647\u0646\u0627 \u064a\u0638\u0644 \u062a\u0642\u062f\u064a\u0631\u0643 \u0623\u0646\u062a: \u0644\u0645 \u064a\u062a\u062d\u0642\u0642 \u0625\u0646\u0641\u0646\u062a\u0648\u0631\u0627\u064a \u0645\u0646 \u0623\u064a \u0645\u0646\u0647.",
    },
    "UI_CEV_Q_STATE": {
        "en": "Amount status",
        "ar": "\u062d\u0627\u0644\u0629 \u0627\u0644\u0645\u0628\u0644\u063a",
    },
    "UI_CEV_Q_STATE_NONE": {
        "en": "Not established",
        "ar": "\u063a\u064a\u0631 \u0645\u062d\u062f\u064e\u0651\u062f",
    },
    "UI_CEV_Q_STATE_EXACT": {
        "en": "Exact",
        "ar": "\u0645\u0628\u0644\u063a \u0645\u062d\u062f\u064e\u0651\u062f",
    },
    "UI_CEV_Q_STATE_ESTIMATED_RANGE": {
        "en": "Estimated range",
        "ar": "\u0646\u0637\u0627\u0642 \u062a\u0642\u062f\u064a\u0631\u064a",
    },
    "UI_CEV_Q_EXACT": {
        "en": "Amount",
        "ar": "\u0627\u0644\u0645\u0628\u0644\u063a",
    },
    "UI_CEV_Q_MIN": {
        "en": "Lowest",
        "ar": "\u0627\u0644\u062d\u062f \u0627\u0644\u0623\u062f\u0646\u0649",
    },
    "UI_CEV_Q_MAX": {
        "en": "Highest",
        "ar": "\u0627\u0644\u062d\u062f \u0627\u0644\u0623\u0639\u0644\u0649",
    },
    "UI_CEV_Q_CURRENCY": {
        "en": "Currency",
        "ar": "\u0627\u0644\u0639\u0645\u0644\u0629",
    },
    "UI_CEV_Q_BASIS": {
        "en": "Per",
        "ar": "\u0644\u0643\u0644",
    },
    "UI_CEV_Q_ESTIMATE_BASIS": {
        "en": "Where the amount comes from",
        "ar": "\u0645\u0635\u062f\u0631 \u0627\u0644\u0645\u0628\u0644\u063a",
    },
    "UI_CEV_Q_RATIONALE": {
        "en": "Why this amount",
        "ar": "\u0633\u0628\u0628 \u0647\u0630\u0627 \u0627\u0644\u0645\u0628\u0644\u063a",
    },
    "UI_CEV_Q_RATIONALE_HELP": {
        "en": "What you based it on, and what it assumes.",
        "ar": "\u0645\u0627 \u0627\u0644\u0630\u064a \u0627\u0639\u062a\u0645\u062f\u062a \u0639\u0644\u064a\u0647\u060c \u0648\u0645\u0627 \u0627\u0644\u0630\u064a \u064a\u0641\u062a\u0631\u0636\u0647.",
    },
    "UI_CEV_Q_NOT_VALIDATED": {
        "en": "Recording an amount does not make it checked, agreed or final.",
        "ar": "\u062a\u0633\u062c\u064a\u0644 \u0627\u0644\u0645\u0628\u0644\u063a \u0644\u0627 \u064a\u062c\u0639\u0644\u0647 \u0645\u062a\u062d\u0642\u064e\u0651\u0642\u064b\u0627 \u0645\u0646\u0647 \u0648\u0644\u0627 \u0645\u062a\u064e\u0651\u0641\u0642\u064b\u0627 \u0639\u0644\u064a\u0647 \u0648\u0644\u0627 \u0646\u0647\u0627\u0626\u064a\u064b\u0627.",
    },
    "UI_CEV_BASIS_PER_UNIT": {
        "en": "Unit",
        "ar": "\u0648\u062d\u062f\u0629",
    },
    "UI_CEV_BASIS_PER_MONTH": {
        "en": "Month",
        "ar": "\u0634\u0647\u0631",
    },
    "UI_CEV_BASIS_PER_PROJECT": {
        "en": "Project",
        "ar": "\u0645\u0634\u0631\u0648\u0639",
    },
    "UI_CEV_BASIS_PER_INSTALLATION": {
        "en": "Installation",
        "ar": "\u062a\u0631\u0643\u064a\u0628",
    },
    "UI_CEV_BASIS_OTHER": {
        "en": "Other",
        "ar": "\u0623\u062e\u0631\u0649",
    },
    "UI_CEV_EB_SUPPLIER_QUOTE": {
        "en": "A supplier quote",
        "ar": "\u0639\u0631\u0636 \u0633\u0639\u0631 \u0645\u0646 \u0645\u0648\u0631\u0651\u062f",
    },
    "UI_CEV_EB_COMPARABLE_PRODUCT_PRICE": {
        "en": "A comparable product's price",
        "ar": "\u0633\u0639\u0631 \u0645\u0646\u062a\u062c \u0645\u0645\u0627\u062b\u0644",
    },
    "UI_CEV_EB_PRELIMINARY_COMPONENT_COST": {
        "en": "A preliminary component cost",
        "ar": "\u062a\u0643\u0644\u0641\u0629 \u0645\u0628\u062f\u0626\u064a\u0629 \u0644\u0644\u0645\u0643\u0648\u0651\u0646\u0627\u062a",
    },
    "UI_CEV_EB_MANUFACTURING_COST_ESTIMATE": {
        "en": "A manufacturing cost estimate",
        "ar": "\u062a\u0642\u062f\u064a\u0631 \u0644\u062a\u0643\u0644\u0641\u0629 \u0627\u0644\u062a\u0635\u0646\u064a\u0639",
    },
    "UI_CEV_EB_WILLINGNESS_TO_PAY_EVIDENCE": {
        "en": "Something a buyer told you",
        "ar": "\u0645\u0627 \u0623\u062e\u0628\u0631\u0643 \u0628\u0647 \u0645\u0634\u062a\u0631\u064d",
    },
    "UI_CEV_EB_REFERENCE_MARKET_PRICE": {
        "en": "A reference market price",
        "ar": "\u0633\u0639\u0631 \u0633\u0648\u0642 \u0645\u0631\u062c\u0639\u064a",
    },
    "UI_CEV_EB_OWNER_ASSUMPTION": {
        "en": "Your own assumption",
        "ar": "\u0627\u0641\u062a\u0631\u0627\u0636 \u0645\u0646\u0643",
    },
    "UI_CEV_EB_PRIOR_PROTOTYPE_COST": {
        "en": "A previous prototype's cost",
        "ar": "\u062a\u0643\u0644\u0641\u0629 \u0646\u0645\u0648\u0630\u062c \u0623\u0648\u0644\u064a \u0633\u0627\u0628\u0642",
    },
    "UI_CEV_EB_CHANNEL_MARGIN_ASSUMPTION": {
        "en": "A channel or margin assumption",
        "ar": "\u0627\u0641\u062a\u0631\u0627\u0636 \u0639\u0646 \u0642\u0646\u0627\u0629 \u0627\u0644\u0628\u064a\u0639 \u0623\u0648 \u0627\u0644\u0647\u0627\u0645\u0634",
    },
    "UI_CEV_EB_OTHER_DOCUMENTED": {
        "en": "Another documented basis",
        "ar": "\u0623\u0633\u0627\u0633 \u0645\u0648\u062b\u064e\u0651\u0642 \u0622\u062e\u0631",
    },
    "UI_CEV_CORRECT_HEADING": {
        "en": "Correct this item",
        "ar": "\u0635\u062d\u0651\u062d \u0647\u0630\u0627 \u0627\u0644\u0639\u0646\u0635\u0631",
    },
    "UI_CEV_CORRECT_EXPLAIN": {
        "en": ("A correction records a new version beside the old one. The "
               "earlier version is kept exactly as you wrote it and stays "
               "visible below as history \u2014 nothing is overwritten or deleted. "
               "The topic stays the same; to file an item under a different "
               "topic, withdraw it and record it again."),
        "ar": ("\u0627\u0644\u062a\u0635\u062d\u064a\u062d \u064a\u0633\u062c\u0651\u0644 \u0646\u0633\u062e\u0629 \u062c\u062f\u064a\u062f\u0629 \u0625\u0644\u0649 \u062c\u0627\u0646\u0628 \u0627\u0644\u0642\u062f\u064a\u0645\u0629. "
               "\u0648\u062a\u064f\u062d\u0641\u0638 \u0627\u0644\u0646\u0633\u062e\u0629 \u0627\u0644\u0633\u0627\u0628\u0642\u0629 \u0643\u0645\u0627 \u0643\u062a\u0628\u062a\u0647\u0627 \u062a\u0645\u0627\u0645\u064b\u0627 \u0648\u062a\u0628\u0642\u0649 \u0638\u0627\u0647\u0631\u0629 \u0623\u062f\u0646\u0627\u0647 "
               "\u0636\u0645\u0646 \u0627\u0644\u0633\u062c\u0644\u0651 \u2014 \u0644\u0627 \u0634\u064a\u0621 \u064a\u064f\u0633\u062a\u0628\u062f\u0644 \u0623\u0648 \u064a\u064f\u062d\u0630\u0641. \u0648\u064a\u0628\u0642\u0649 \u0627\u0644\u0645\u0648\u0636\u0648\u0639 \u0643\u0645\u0627 \u0647\u0648\u061b "
               "\u0648\u0644\u062a\u0633\u062c\u064a\u0644 \u0639\u0646\u0635\u0631 \u062a\u062d\u062a \u0645\u0648\u0636\u0648\u0639 \u0622\u062e\u0631\u060c \u0627\u0633\u062d\u0628\u0647 \u062b\u0645 \u0633\u062c\u0651\u0644\u0647 \u0645\u0646 \u062c\u062f\u064a\u062f."),
    },
    "UI_CEV_CORRECT_SUBMIT": {
        "en": "Record the correction",
        "ar": "\u0633\u062c\u0651\u0644 \u0627\u0644\u062a\u0635\u062d\u064a\u062d",
    },
    "UI_CEV_WITHDRAW_SUBMIT": {
        "en": "Withdraw this item",
        "ar": "\u0627\u0633\u062d\u0628 \u0647\u0630\u0627 \u0627\u0644\u0639\u0646\u0635\u0631",
    },
    "UI_CEV_WITHDRAW_EXPLAIN": {
        "en": ("Withdrawing says this item no longer stands. It is kept in the "
               "history below exactly as you wrote it, and it stops counting as "
               "something recorded for its topic."),
        "ar": ("\u0627\u0644\u0633\u062d\u0628 \u064a\u0639\u0646\u064a \u0623\u0646 \u0647\u0630\u0627 \u0627\u0644\u0639\u0646\u0635\u0631 \u0644\u0645 \u064a\u0639\u062f \u0642\u0627\u0626\u0645\u064b\u0627. \u0648\u064a\u064f\u062d\u0641\u0638 \u0641\u064a "
               "\u0627\u0644\u0633\u062c\u0644\u0651 \u0623\u062f\u0646\u0627\u0647 \u0643\u0645\u0627 \u0643\u062a\u0628\u062a\u0647 \u062a\u0645\u0627\u0645\u064b\u0627\u060c \u0648\u064a\u062a\u0648\u0642\u0641 \u0639\u0646 \u0627\u0644\u0627\u062d\u062a\u0633\u0627\u0628 \u0643\u0634\u064a\u0621 "
               "\u0645\u064f\u0633\u062c\u0651\u0644 \u0644\u0645\u0648\u0636\u0648\u0639\u0647."),
    },
    "UI_CEV_HISTORY_HEADING": {
        "en": "Earlier versions and withdrawn items",
        "ar": "\u0627\u0644\u0646\u0633\u062e \u0627\u0644\u0633\u0627\u0628\u0642\u0629 \u0648\u0627\u0644\u0639\u0646\u0627\u0635\u0631 \u0627\u0644\u0645\u0633\u062d\u0648\u0628\u0629",
    },
    "UI_CEV_HISTORY_EXPLAIN": {
        "en": ("Everything you recorded is kept, in the order you recorded it. "
               "An earlier version is not a mistake and a withdrawn item is not "
               "a failure \u2014 both are what you wrote at the time, and they are "
               "shown so the record stays honest about how it changed."),
        "ar": ("\u064a\u064f\u062d\u0641\u0638 \u0643\u0644 \u0645\u0627 \u0633\u062c\u0651\u0644\u062a\u0647\u060c \u0628\u0627\u0644\u062a\u0631\u062a\u064a\u0628 \u0627\u0644\u0630\u064a \u0633\u062c\u0651\u0644\u062a\u0647 \u0628\u0647. \u0648\u0627\u0644\u0646\u0633\u062e\u0629 "
               "\u0627\u0644\u0633\u0627\u0628\u0642\u0629 \u0644\u064a\u0633\u062a \u062e\u0637\u0623\u060c \u0648\u0627\u0644\u0639\u0646\u0635\u0631 \u0627\u0644\u0645\u0633\u062d\u0648\u0628 \u0644\u064a\u0633 \u0625\u062e\u0641\u0627\u0642\u064b\u0627 \u2014 \u0643\u0644\u0627\u0647\u0645\u0627 \u0645\u0627 "
               "\u0643\u062a\u0628\u062a\u0647 \u0641\u064a \u062d\u064a\u0646\u0647\u060c \u0648\u064a\u064f\u0639\u0631\u0636\u0627\u0646 \u0644\u064a\u0628\u0642\u0649 \u0627\u0644\u0633\u062c\u0644\u0651 \u0635\u0627\u062f\u0642\u064b\u0627 \u0639\u0646 \u0643\u064a\u0641 \u062a\u063a\u064a\u0651\u0631."),
    },
    "UI_CEV_STATE_REPLACED": {
        "en": "Replaced by a later version",
        "ar": "\u0627\u0633\u062a\u064f\u0628\u062f\u0644\u062a \u0628\u0646\u0633\u062e\u0629 \u0644\u0627\u062d\u0642\u0629",
    },
    "UI_CEV_STATE_WITHDRAWN": {
        "en": "Withdrawn",
        "ar": "\u0645\u0633\u062d\u0648\u0628",
    },
    "UI_CEV_NOTICE_CORRECTED": {
        "en": "Your correction was recorded. The earlier version is kept below.",
        "ar": "\u0633\u064f\u062c\u0651\u0644 \u062a\u0635\u062d\u064a\u062d\u0643. \u0648\u0627\u0644\u0646\u0633\u062e\u0629 \u0627\u0644\u0633\u0627\u0628\u0642\u0629 \u0645\u062d\u0641\u0648\u0638\u0629 \u0623\u062f\u0646\u0627\u0647.",
    },
    "UI_CEV_NOTICE_WITHDRAWN": {
        "en": "That item was withdrawn. It is kept below as history.",
        "ar": "\u0633\u064f\u062d\u0628 \u0630\u0644\u0643 \u0627\u0644\u0639\u0646\u0635\u0631. \u0648\u0647\u0648 \u0645\u062d\u0641\u0648\u0638 \u0623\u062f\u0646\u0627\u0647 \u0636\u0645\u0646 \u0627\u0644\u0633\u062c\u0644\u0651.",
    },
    # --- D3 supporting-evidence linkage -------------------------------------
    # A link is a TRAVERSAL: it names the item this one was recorded against.
    # Nothing here says checked, verified, validated, proven, certified,
    # accepted, strong or sufficient, in either language, because a reference
    # existing establishes none of those. There is no count, badge, score,
    # ranking or percentage anywhere in this group.
    "UI_CEV_LINK_LABEL": {
        "en": "Supporting item (optional)",
        "ar": "\u0627\u0644\u0639\u0646\u0635\u0631 \u0627\u0644\u0645\u0633\u0627\u0646\u062f (\u0627\u062e\u062a\u064a\u0627\u0631\u064a)",
    },
    "UI_CEV_LINK_NONE": {
        "en": "No supporting item selected",
        "ar": "\u0644\u0645 \u064a\u064f\u062e\u062a\u0631 \u0639\u0646\u0635\u0631 \u0645\u0633\u0627\u0646\u062f",
    },
    "UI_CEV_LINK_SUPPORTED_BY": {
        "en": "Supported by",
        "ar": "\u0645\u0633\u0646\u0648\u062f \u0625\u0644\u0649",
    },
    "UI_CEV_LINK_WAS_SUPPORTED_BY": {
        "en": "Was supported by",
        "ar": "\u0643\u0627\u0646 \u0645\u0633\u0646\u0648\u062f\u064b\u0627 \u0625\u0644\u0649",
    },
    "UI_CEV_LINK_EXPLAIN": {
        "en": ("You can point this item at ONE other item you recorded, as "
               "the one it was written against. That is all a link does: it "
               "says where to look next. It does not check either item, does "
               "not make either one agreed or final, and adds nothing to "
               "either. An item with no link is not weaker than one with a "
               "link \u2014 nothing here is counted, rated or ranked."),
        "ar": ("\u064a\u0645\u0643\u0646\u0643 \u0623\u0646 \u062a\u0631\u0628\u0637 \u0647\u0630\u0627 \u0627\u0644\u0639\u0646\u0635\u0631 \u0628\u0639\u0646\u0635\u0631 \u0648\u0627\u062d\u062f \u0622\u062e\u0631 "
               "\u0633\u062c\u0651\u0644\u062a\u0647\u060c \u0628\u0627\u0639\u062a\u0628\u0627\u0631\u0647 \u0627\u0644\u0639\u0646\u0635\u0631 \u0627\u0644\u0630\u064a \u0643\u064f\u062a\u0628 \u0641\u064a \u0645\u0642\u0627\u0628\u0644\u0647. \u0647\u0630\u0627 \u0643\u0644 \u0645\u0627 "
               "\u064a\u0641\u0639\u0644\u0647 \u0627\u0644\u0631\u0628\u0637: \u064a\u062f\u0644\u0651 \u0639\u0644\u0649 \u0645\u0648\u0636\u0639 \u0627\u0644\u0646\u0638\u0631 \u0627\u0644\u062a\u0627\u0644\u064a. \u0648\u0647\u0648 \u0644\u0627 \u064a\u0641\u062d\u0635 "
               "\u0623\u064a\u064b\u0627 \u0645\u0646 \u0627\u0644\u0639\u0646\u0635\u0631\u064a\u0646\u060c \u0648\u0644\u0627 \u064a\u062c\u0639\u0644 \u0623\u064a\u064b\u0627 \u0645\u0646\u0647\u0645\u0627 \u0645\u062a\u0641\u0642\u064b\u0627 \u0639\u0644\u064a\u0647 \u0623\u0648 "
               "\u0646\u0647\u0627\u0626\u064a\u064b\u0627\u060c \u0648\u0644\u0627 \u064a\u0636\u064a\u0641 \u0625\u0644\u0649 \u0623\u064a\u064d \u0645\u0646\u0647\u0645\u0627 \u0634\u064a\u0626\u064b\u0627. \u0648\u0627\u0644\u0639\u0646\u0635\u0631 \u0628\u0644\u0627 "
               "\u0631\u0628\u0637 \u0644\u064a\u0633 \u0623\u0636\u0639\u0641 \u0645\u0646 \u0639\u0646\u0635\u0631 \u0645\u0631\u0628\u0648\u0637 \u2014 \u0644\u0627 \u0634\u064a\u0621 \u0647\u0646\u0627 \u064a\u064f\u0639\u062f\u0651 \u0623\u0648 "
               "\u064a\u064f\u0642\u064a\u0651\u0645 \u0623\u0648 \u064a\u064f\u0631\u062a\u0651\u0628."),
    },
    "UI_CEV_GAP_HEADING": {
        "en": "Commercial topics you have not recorded anything for yet",
        "ar": "\u0645\u0648\u0636\u0648\u0639\u0627\u062a \u062a\u062c\u0627\u0631\u064a\u0629 \u0644\u0645 \u062a\u0633\u062c\u0651\u0644 \u0639\u0646\u0647\u0627 \u0634\u064a\u0626\u064b\u0627 \u0628\u0639\u062f",
    },
    "UI_CEV_GAP_EXPLAIN": {
        "en": ("These are the topics this page can hold that have nothing "
               "recorded against them yet. An empty topic means only that "
               "\u2014 nothing has been written down about it so far. It is not a "
               "conclusion about your idea, your buyers or your market, and it "
               "is not a measurement: nothing here is counted or weighed, and "
               "the order below is simply the order these topics are listed "
               "in."),
        "ar": ("\u0647\u0630\u0647 \u0647\u064a \u0627\u0644\u0645\u0648\u0636\u0648\u0639\u0627\u062a \u0627\u0644\u062a\u064a \u064a\u0645\u0643\u0646 \u0644\u0647\u0630\u0647 \u0627\u0644\u0635\u0641\u062d\u0629 \u0623\u0646 \u062a\u062d\u062a\u0648\u064a\u0647\u0627 \u0648\u0644\u0645 "
               "\u064a\u064f\u0633\u062c\u064e\u0651\u0644 \u0639\u0646\u0647\u0627 \u0634\u064a\u0621 \u0628\u0639\u062f. \u0627\u0644\u0645\u0648\u0636\u0648\u0639 \u0627\u0644\u0641\u0627\u0631\u063a \u064a\u0639\u0646\u064a \u0630\u0644\u0643 \u0641\u0642\u0637 \u2014 "
               "\u0644\u0645 \u064a\u064f\u0643\u062a\u0628 \u0639\u0646\u0647 \u0634\u064a\u0621 \u062d\u062a\u0649 \u0627\u0644\u0622\u0646. \u0648\u0647\u0648 \u0644\u064a\u0633 \u0627\u0633\u062a\u0646\u062a\u0627\u062c\u064b\u0627 \u0639\u0646 \u0641\u0643\u0631\u062a\u0643 \u0648\u0644\u0627 \u0639\u0646 "
               "\u0627\u0644\u0645\u0634\u062a\u0631\u064a\u0646 \u0648\u0644\u0627 \u0639\u0646 \u0627\u0644\u0633\u0648\u0642\u060c \u0648\u0644\u064a\u0633 \u0642\u064a\u0627\u0633\u064b\u0627: \u0644\u0627 \u0634\u064a\u0621 \u0647\u0646\u0627 \u064a\u064f\u0639\u062f\u0651 \u0623\u0648 "
               "\u064a\u064f\u0648\u0632\u064e\u0646\u060c \u0648\u0627\u0644\u062a\u0631\u062a\u064a\u0628 \u0623\u062f\u0646\u0627\u0647 \u0647\u0648 \u062a\u0631\u062a\u064a\u0628 \u0633\u0631\u062f \u0647\u0630\u0647 "
               "\u0627\u0644\u0645\u0648\u0636\u0648\u0639\u0627\u062a \u0641\u062d\u0633\u0628."),
    },
    "UI_CEV_ADD_HEADING": {
        "en": "Record one more item",
        "ar": "سجّل عنصرًا آخر",
    },
    "UI_CEV_FIELD_TOPIC": {"en": "Topic", "ar": "الموضوع"},
    "UI_CEV_FIELD_SUBJECT": {
        "en": "What this concerns", "ar": "ما يتعلق به هذا"},
    "UI_CEV_FIELD_STATEMENT": {
        "en": "What you know or believe", "ar": "ما تعرفه أو تعتقده"},
    "UI_CEV_FIELD_SOURCE": {
        "en": "Where this came from", "ar": "من أين جاء هذا"},
    "UI_CEV_FIELD_DATE": {
        "en": "Date, if you know it (YYYY-MM-DD)",
        "ar": "التاريخ، إن كنت تعرفه (YYYY-MM-DD)"},
    "UI_CEV_FIELD_SCOPE": {
        "en": "What it covers", "ar": "ما الذي يغطّيه"},
    "UI_CEV_FIELD_LIMITATION": {
        "en": "What it does NOT cover", "ar": "ما الذي لا يغطّيه"},
    "UI_CEV_LIMITATION_NOTE": {
        "en": ("Saying what your evidence does not cover is required, and it "
               "is the most useful part: it is what stops you, later, from "
               "trusting it further than it goes."),
        "ar": ("ذِكر ما لا تغطّيه أدلتك مطلوب، وهو الجزء الأنفع: فهو ما يمنعك "
               "لاحقًا من الوثوق بها أبعد مما تصل إليه."),
    },
    "UI_CEV_SUBMIT": {"en": "Record this", "ar": "سجّل هذا"},
    "UI_CEV_META_SOURCE": {"en": "Source", "ar": "المصدر"},
    "UI_CEV_META_DATE": {"en": "Date", "ar": "التاريخ"},
    "UI_CEV_META_SCOPE": {"en": "Covers", "ar": "يغطّي"},
    "UI_CEV_META_LIMITATION": {"en": "Does not cover", "ar": "لا يغطّي"},
    "UI_CEV_META_ORIGIN": {"en": "Recorded by", "ar": "سجّله"},
    "UI_CEV_META_ORIGIN_VALUE": {
        "en": "you, from your own knowledge",
        "ar": "أنت، من معرفتك الخاصة"},
    "UI_CEV_META_STANDING": {"en": "Standing", "ar": "الحالة"},
    "UI_CEV_META_STANDING_VALUE": {
        "en": "recorded, not checked by anyone",
        "ar": "مسجَّل، ولم يتحقق منه أحد"},
    "UI_CEV_META_NOTE": {
        "en": ("These two lines describe where each item came from and how far "
               "it has been checked. They are not settings and you cannot "
               "change them: everything you record here is your own statement, "
               "and this version of InventorAI verifies none of it."),
        "ar": ("يصف هذان السطران من أين جاء كل عنصر وإلى أي مدى جرى التحقق "
               "منه. ليسا إعدادات ولا يمكنك تغييرهما: كل ما تسجّله هنا هو "
               "قولك أنت، وهذه النسخة من إنفنتوراي لا تتحقق من أي منه."),
    },
    "UI_CEV_NOTICE_SAVED": {
        "en": "Recorded and saved to your project.",
        "ar": "سُجِّل وحُفِظ في مشروعك.",
    },
    "UI_CEV_NOTICE_REPLAY": {
        "en": ("That item was already recorded earlier, so nothing was added "
               "a second time."),
        "ar": "سُجِّل ذلك العنصر سابقًا، فلم يُضَف مرة ثانية.",
    },
    "UI_CEV_NOTICE_NOT_SAVED": {
        "en": "That item was not recorded. Nothing was changed.",
        "ar": "لم يُسجَّل ذلك العنصر. لم يتغير شيء.",
    },
    "UI_CEV_NOTICE_TEXT_REJECTED": {
        "en": ("That text is too long or contains an invalid character. "
               "Nothing was saved - please shorten or clean it and try again."),
        "ar": ("ذلك النص أطول من اللازم أو يحتوي على رمز غير صالح. لم يُحفظ "
               "شيء — يُرجى تقصيره أو تنظيفه والمحاولة من جديد."),
    },
    "UI_CEV_NOTICE_UNKNOWN": {
        "en": ("We could not confirm whether that item was recorded. Reload "
               "this page to see the current list before trying again."),
        "ar": ("تعذّر علينا تأكيد ما إذا كان ذلك العنصر قد سُجِّل. أعد تحميل "
               "هذه الصفحة لرؤية القائمة الحالية قبل المحاولة مجددًا."),
    },
    "UI_CEV_NOTICE_CAP": {
        "en": ("This project already holds as many Commercial evidence items "
               "as it can. Nothing was saved."),
        "ar": ("يحتوي هذا المشروع بالفعل على أقصى عدد ممكن من عناصر الأدلة "
               "التجارية. لم يُحفظ شيء."),
    },
    "UI_CEV_TOPIC_TARGET_CUSTOMER": {
        "en": "Who it is for", "ar": "لمن هي"},
    "UI_CEV_TOPIC_PROBLEM_SEVERITY": {
        "en": "How badly the problem is felt", "ar": "مدى حدّة المشكلة"},
    "UI_CEV_TOPIC_MARKET_ALTERNATIVE": {
        "en": "What people use instead today", "ar": "ما يستخدمه الناس بدلًا منها اليوم"},
    "UI_CEV_TOPIC_DIFFERENTIATION": {
        "en": "How this differs", "ar": "بماذا تختلف هذه"},
    "UI_CEV_TOPIC_PRICE": {"en": "Price", "ar": "السعر"},
    "UI_CEV_TOPIC_WILLINGNESS_TO_PAY": {
        "en": "What someone would pay", "ar": "ما قد يدفعه شخص ما"},
    "UI_CEV_TOPIC_DEMAND": {"en": "Who wants it", "ar": "من يريدها"},
    "UI_CEV_TOPIC_CUSTOMER_EVIDENCE": {
        "en": "What a customer told you", "ar": "ما أخبرك به عميل"},
    "UI_CEV_TOPIC_MARKET_ENTRY": {
        "en": "How it would reach the market", "ar": "كيف ستصل إلى السوق"},
    "UI_CEV_TOPIC_CHANNEL": {"en": "Who would sell it", "ar": "من سيبيعها"},
    "UI_CEV_TOPIC_LICENSING": {"en": "Licensing", "ar": "الترخيص"},
    "UI_CEV_TOPIC_REVENUE_MODEL": {
        "en": "How it would earn", "ar": "كيف ستحقق دخلًا"},
    "UI_CEV_TOPIC_COST_REVENUE_ASSUMPTION": {
        "en": "A cost or revenue you are assuming",
        "ar": "تكلفة أو إيراد تفترضه"},
    "UI_CEV_TOPIC_FUNDING_NEED": {
        "en": "Money it would need", "ar": "المال الذي ستحتاجه"},
    "UI_CEV_TOPIC_FIRST_SALE_VIABILITY": {
        "en": "What a first sale would take", "ar": "ما يتطلبه أول بيع"},
    "UI_T3A_HEADING": {
        "en": "Project record",
        "ar": "سجل المشروع",
    },
    "UI_T3A_EXPLAIN": {
        "en": ("Everything you recorded in this project, in the order it was "
               "saved, including entries you later replaced or withdrew and "
               "any change of rules. Nothing is erased: a replaced or withdrawn "
               "entry stays listed as part of your own history, and listing it "
               "is not a judgement that it was wrong."),
        "ar": ("كل ما سجّلته في هذا المشروع، بترتيب حفظه، بما في ذلك الإدخالات "
               "التي استبدلتها أو سحبتها لاحقًا وأي تغيير في القواعد. لا يُمحى "
               "شيء: يبقى الإدخال المستبدَل أو المسحوب مدرجًا بوصفه جزءًا من "
               "سجلك أنت، وإدراجه ليس حكمًا بأنه كان خاطئًا."),
    },
    "UI_T3A_EMPTY": {
        "en": "Nothing has been recorded in this project yet.",
        "ar": "لم يُسجَّل شيء في هذا المشروع بعد.",
    },
    "UI_T3A_ORDER_NOTE": {
        "en": ("Steps are numbered in the order they were saved. Values and "
               "references are shown with the answer they belong to. Rule "
               "changes are listed separately with the step they followed, "
               "because their exact place among the entries of that same "
               "step was not recorded."),
        "ar": ("تُرقَّم الخطوات بترتيب حفظها. وتُعرض القيم والمراجع مع الإجابة "
               "التي تنتمي إليها. وتُدرج تغييرات القواعد على حدة مع الخطوة "
               "التي تلتها، لأن موضعها الدقيق بين إدخالات تلك الخطوة نفسها "
               "لم يُسجَّل."),
    },
    "UI_T3A_STEP": {
        "en": "Step",
        "ar": "الخطوة",
    },
    "UI_T3A_SHOW_FULL": {
        "en": "Show the full text",
        "ar": "عرض النص الكامل",
    },
    "UI_T3A_REPLACES": {
        "en": "Replaces step",
        "ar": "يحل محل الخطوة",
    },
    "UI_T3A_REPLACED_BY": {
        "en": "Replaced by step",
        "ar": "استُبدل بالخطوة",
    },
    "UI_T3A_WITHDRAWS": {
        "en": "Withdraws step",
        "ar": "يسحب الخطوة",
    },
    "UI_T3A_WITHDRAWN_IN": {
        "en": "Withdrawn at step",
        "ar": "سُحب في الخطوة",
    },
    "UI_T3A_REPLACES_EARLIER": {
        "en": "replaces an earlier entry on this answer",
        "ar": "يحل محل إدخال سابق على هذه الإجابة",
    },
    "UI_T3A_WITHDRAWN_KEPT": {
        "en": ("Withdrawn by you and kept in the project history; it is no "
               "longer used as current support."),
        "ar": ("سحبتَه بنفسك وبقي محفوظًا في سجل المشروع؛ ولم يعد يُستخدم "
               "كدعم حالي."),
    },
    "UI_T3A_RULES_HEADING": {
        "en": "Rule changes",
        "ar": "تغييرات القواعد",
    },
    "UI_T3A_AFTER_STEP": {
        "en": "After step",
        "ar": "بعد الخطوة",
    },
    "UI_T3A_RECORDED_ON": {
        "en": "Recorded on",
        "ar": "سُجّل في",
    },
    "UI_T3A_ADOPTION_KEPT": {
        "en": "Earlier answers were kept exactly as recorded.",
        "ar": "بقيت الإجابات السابقة كما سُجّلت تمامًا.",
    },
    "UI_T3A_EVENT_CONTRADICTION_DECLARED": {
        "en": "Conflict you declared between two answers",
        "ar": "تعارض أعلنته بين إجابتين",
    },
    "UI_T3A_DECLARES_CONFLICT": {
        "en": "Marks as conflicting: step",
        "ar": "يعلّم كمتعارض: الخطوة",
    },
    # CAP-10 Slice 1 — the inventor's explicit conflict declaration. Truthful:
    # the inventor's own belief, not validated, no winner, no progress effect.
    "UI_CAP10_HEADING": {
        "en": "Mark two answers as conflicting",
        "ar": "تعليم إجابتين على أنهما متعارضتان",
    },
    "UI_CAP10_EXPLAIN": {
        "en": ("If you believe two of your recorded answers conflict, you can "
               "record that here. The system does not decide which answer is "
               "right, and recording it does not change your progress."),
        "ar": ("إذا كنت ترى أن إجابتين من إجاباتك المسجّلة متعارضتان، يمكنك "
               "تسجيل ذلك هنا. لا يقرّر النظام أيّ الإجابتين صحيحة، ولا يغيّر "
               "التسجيل تقدّمك."),
    },
    "UI_CAP10_SELECT": {
        "en": "Choose exactly two of your current answers",
        "ar": "اختر إجابتين بالضبط من إجاباتك الحالية",
    },
    "UI_CAP10_NOTE": {
        "en": "Optional note (kept exactly as you write it)",
        "ar": "ملاحظة اختيارية (تُحفظ كما تكتبها تمامًا)",
    },
    "UI_CAP10_CONFIRM": {
        "en": ("I believe these two recorded answers conflict. I understand "
               "this declaration is not validated."),
        "ar": ("أرى أن هاتين الإجابتين المسجّلتين متعارضتان. وأفهم أن هذا "
               "الإعلان غير مُتحقَّق منه."),
    },
    "UI_CAP10_BUTTON": {
        "en": "Record the conflict",
        "ar": "تسجيل التعارض",
    },
    "UI_CAP10_ERR_NOT_SAVED": {
        "en": "That conflict could not be saved just now. Nothing was changed.",
        "ar": "تعذّر حفظ هذا التعارض الآن. لم يتم تغيير أي شيء.",
    },
    "UI_CAP10_ERR_INVALID": {
        "en": ("Choose exactly two of your current recorded answers and confirm "
               "that you believe they conflict. Nothing was changed."),
        "ar": ("اختر إجابتين بالضبط من إجاباتك المسجّلة الحالية وأكّد أنك ترى "
               "أنهما متعارضتان. لم يتم تغيير أي شيء."),
    },
    "UI_CAP10_ERR_STALE": {
        "en": ("One of those answers is no longer current, or that conflict is "
               "already recorded, so nothing was saved. Review your current "
               "answers and try again."),
        "ar": ("إحدى هاتين الإجابتين لم تعد حالية، أو أن هذا التعارض مسجّل "
               "مسبقًا، لذلك لم يُحفظ شيء. راجع إجاباتك الحالية وحاول مجددًا."),
    },
    "UI_CAP10_ERR_UNKNOWN": {
        "en": ("We could not confirm whether that conflict was saved. Reload "
               "this page to see what your project holds before recording it "
               "again."),
        "ar": ("لم نتمكّن من التأكد مما إذا كان هذا التعارض قد حُفظ. أعد تحميل "
               "هذه الصفحة لترى ما يحتويه مشروعك قبل تسجيله مرة أخرى."),
    },
    # Stage 21 closure — the read-only session view of the conflicts the
    # inventor declared (CAP-10). Truthful: declared by the inventor, not
    # validated, neither answer assumed correct, no winner chosen.
    "UI_S21_HEADING": {
        "en": "Conflicts you declared",
        "ar": "التعارضات التي أعلنتها",
    },
    "UI_S21_NOTE": {
        "en": ("You declared that the two answers in each pair below conflict. "
               "These declarations have not been validated, neither answer is "
               "assumed correct, and InventorAI does not choose which answer "
               "is right."),
        "ar": ("أعلنتَ أن الإجابتين في كل زوج أدناه متعارضتان. هذه الإعلانات غير "
               "مُتحقَّق منها، ولا تُعدّ أيٌّ من الإجابتين صحيحة، ولا يختار "
               "InventorAI أيّ الإجابتين هي الصحيحة."),
    },
    "UI_S21_STEP": {"en": "Step", "ar": "الخطوة"},
    "UI_S21_NOTE_LABEL": {"en": "Your note", "ar": "ملاحظتك"},
    "UI_S21_CORRECT_INTRO": {
        "en": "If one answer no longer reflects your intent, correct it here:",
        "ar": "إذا لم تعد إحدى الإجابتين تعبّر عن قصدك، صحّحها هنا:",
    },
    "UI_S21_INACTIVE_N": {
        "en": ("Earlier conflict declarations that are no longer active (kept "
               "in your project record):"),
        "ar": "إعلانات تعارض سابقة لم تعد نشطة (محفوظة في سجل مشروعك):",
    },
    "UI_S21_UNAVAILABLE": {
        "en": ("Your declared conflicts cannot be shown right now. This does "
               "not mean there are none."),
        "ar": ("لا يمكن عرض التعارضات التي أعلنتها الآن. ولا يعني ذلك أنه لا "
               "توجد تعارضات."),
    },
    "UI_S21_COMPASS_LINK": {
        "en": "See the conflicts you declared",
        "ar": "عرض التعارضات التي أعلنتها",
    },
    "UI_T3A_CONFLICT_INACTIVE": {
        "en": ("No longer active: one of its two answers was later replaced. "
               "Kept as history."),
        "ar": "لم يعد نشطًا: استُبدلت إحدى إجابتيه لاحقًا. محفوظ ضمن السجل.",
    },
    # CAP-08 Slice 1 — the inventor's explicit assumption -> answer dependency
    # declaration. Truthful: declared by the inventor, not validated, never a
    # confirmation or rejection of the assumption, no progress effect.
    "UI_T3A_EVENT_ASSUMPTION_DEPENDENCY_DECLARED": {
        "en": "Dependency you declared on an assumption",
        "ar": "اعتماد أعلنته على افتراض",
    },
    "UI_T3A_DEPENDS_ON_ASSUMPTION": {
        "en": "Assumption: step",
        "ar": "الافتراض: الخطوة",
    },
    "UI_T3A_DECLARES_DEPENDENT": {
        "en": "Answer declared dependent: step",
        "ar": "الإجابة المعلَن اعتمادها: الخطوة",
    },
    "UI_T3A_DEPENDENCY_INACTIVE": {
        "en": ("No longer active: one of its two records was later replaced. "
               "Kept as history."),
        "ar": "لم يعد نشطًا: استُبدل أحد سجليه لاحقًا. محفوظ ضمن السجل.",
    },
    "UI_CAP08_VIEW_HEADING": {
        "en": "Answers you declared dependent on an assumption",
        "ar": "إجابات أعلنتَ أنها تعتمد على افتراض",
    },
    "UI_CAP08_VIEW_NOTE": {
        "en": ("You declared that these recorded answers depend on this "
               "provisional assumption. This dependency has not been "
               "validated."),
        "ar": ("أعلنتَ أن هذه الإجابات المسجّلة تعتمد على هذا الافتراض المؤقت. "
               "هذا الاعتماد غير مُتحقَّق منه."),
    },
    "UI_CAP08_ASSUMPTION_LABEL": {
        "en": "Provisional assumption:",
        "ar": "افتراض مؤقت:",
    },
    "UI_CAP08_NONE": {
        "en": "No dependency recorded.",
        "ar": "لم تُسجَّل علاقة اعتماد.",
    },
    # Astra F2: declarations exist historically, none is currently active.
    "UI_CAP08_INACTIVE_HISTORY": {
        "en": ("Dependency declarations were recorded previously, but none is "
               "currently active."),
        "ar": ("تم تسجيل علاقات اعتماد سابقًا، ولكن لا توجد علاقة اعتماد نشطة "
               "حاليًا."),
    },
    "UI_CAP08_HEADING": {
        "en": "Mark answers that depend on an assumption",
        "ar": "تعليم إجابات تعتمد على افتراض",
    },
    "UI_CAP08_EXPLAIN": {
        "en": ("If some of your recorded answers depend on one of your "
               "provisional assumptions, you can record that here. The system "
               "does not check the assumption or the answers, and recording it "
               "does not change your progress."),
        "ar": ("إذا كانت بعض إجاباتك المسجّلة تعتمد على أحد افتراضاتك المؤقتة، "
               "يمكنك تسجيل ذلك هنا. لا يفحص النظام الافتراض ولا الإجابات، ولا "
               "يغيّر التسجيل تقدّمك."),
    },
    "UI_CAP08_SELECT_ASSUMPTION": {
        "en": "Choose one of your provisional assumptions",
        "ar": "اختر افتراضًا واحدًا من افتراضاتك المؤقتة",
    },
    "UI_CAP08_SELECT_ANSWERS": {
        "en": "Choose the current answers that depend on it",
        "ar": "اختر الإجابات الحالية التي تعتمد عليه",
    },
    "UI_CAP08_CONFIRM": {
        "en": ("I declare that these recorded answers depend on this "
               "assumption. I understand this dependency is not validated."),
        "ar": ("أُعلن أن هذه الإجابات المسجّلة تعتمد على هذا الافتراض. وأفهم أن "
               "هذا الاعتماد غير مُتحقَّق منه."),
    },
    "UI_CAP08_BUTTON": {
        "en": "Record the dependency",
        "ar": "تسجيل الاعتماد",
    },
    "UI_CAP08_ERR_NOT_SAVED": {
        "en": "That dependency could not be saved just now. Nothing was changed.",
        "ar": "تعذّر حفظ هذا الاعتماد الآن. لم يتم تغيير أي شيء.",
    },
    "UI_CAP08_ERR_INVALID": {
        "en": ("Choose one of your provisional assumptions and at least one of "
               "your current recorded answers, and tick the declaration box. "
               "Nothing was changed."),
        "ar": ("اختر افتراضًا واحدًا من افتراضاتك المؤقتة وإجابة واحدة على الأقل "
               "من إجاباتك المسجّلة الحالية، وحدّد مربع الإعلان. لم يتم تغيير أي "
               "شيء."),
    },
    "UI_CAP08_ERR_STALE": {
        "en": ("One of those records is no longer current, or that dependency is "
               "already recorded, so nothing was saved. Review your current "
               "records and try again."),
        "ar": ("أحد هذه السجلات لم يعد حاليًا، أو أن هذا الاعتماد مسجّل مسبقًا، "
               "لذلك لم يُحفظ شيء. راجع سجلاتك الحالية وحاول مجددًا."),
    },
    "UI_CAP08_ERR_UNKNOWN": {
        "en": ("We could not tell whether that dependency was saved. Reload "
               "this page to see what your project holds before recording it "
               "again."),
        "ar": ("لم نتمكّن من معرفة ما إذا كان هذا الاعتماد قد حُفظ. أعد تحميل "
               "هذه الصفحة لترى ما يحتويه مشروعك قبل تسجيله مرة أخرى."),
    },
    # --- Stage 20 closure: revise / replace a provisional assumption ---
    'UI_S20_HEADING': {
        "en": 'Your provisional assumptions',
        "ar": 'افتراضاتك المؤقتة',
    },
    'UI_S20_EXPLAIN': {
        "en": 'You can revise one of your provisional assumptions, or replace it with your own answer. The earlier entry stays in your project history, nothing is validated, and any dependency you declared on it stops applying and is not moved to the new entry.',
        "ar": 'يمكنك تعديل أحد افتراضاتك المؤقتة، أو استبداله بإجابتك. يبقى الإدخال السابق في سجل مشروعك، ولا يُتحقَّق من شيء، وأي اعتماد أعلنته عليه يتوقف عن الانطباق ولا يُنقل إلى الإدخال الجديد.',
    },
    'UI_S20_REVISE_SUMMARY': {
        "en": 'Revise this assumption',
        "ar": 'تعديل هذا الافتراض',
    },
    'UI_S20_REVISE_LABEL': {
        "en": 'Your revised assumption',
        "ar": 'افتراضك المعدَّل',
    },
    'UI_S20_REVISE_BUTTON': {
        "en": 'Save revised assumption',
        "ar": 'حفظ الافتراض المعدَّل',
    },
    'UI_S20_REPLACE_SUMMARY': {
        "en": 'Replace it with my answer',
        "ar": 'استبداله بإجابتي',
    },
    'UI_S20_REPLACE_NOTE': {
        "en": 'Your answer replaces this assumption as your response to the same question. It is recorded as your own answer and is not validated.',
        "ar": 'تحلّ إجابتك محلّ هذا الافتراض كردّك على السؤال نفسه. وتُسجَّل كإجابتك أنت ولا يُتحقَّق منها.',
    },
    'UI_S20_REPLACE_LABEL': {
        "en": 'Your answer',
        "ar": 'إجابتك',
    },
    'UI_S20_REPLACE_BUTTON': {
        "en": 'Replace with my answer',
        "ar": 'الاستبدال بإجابتي',
    },
    'UI_S20_REPLACE_ROUTED': {
        "en": 'This assumption is your note on a question that is waiting for specialist or evidence input, so it cannot be replaced by your own answer. You can still revise it.',
        "ar": 'هذا الافتراض هو ملاحظتك على سؤال ينتظر مدخلات متخصّص أو دليلًا، لذلك لا يمكن استبداله بإجابتك. لا يزال بإمكانك تعديله.',
    },
    'UI_S20_REPLACE_UNAVAILABLE': {
        "en": 'Replacing this assumption with your answer is not available just now. You can still revise it.',
        "ar": 'استبدال هذا الافتراض بإجابتك غير متاح الآن. لا يزال بإمكانك تعديله.',
    },
    'UI_S20_ERR_NOT_SAVED': {
        "en": 'That change to your assumption could not be saved just now. Nothing was changed.',
        "ar": 'تعذّر حفظ هذا التغيير على افتراضك الآن. لم يتم تغيير أي شيء.',
    },
    'UI_S20_ERR_INVALID': {
        "en": 'Enter your revised assumption or your answer. Nothing was changed.',
        "ar": 'أدخل افتراضك المعدَّل أو إجابتك. لم يتم تغيير أي شيء.',
    },
    'UI_S20_ERR_STALE': {
        "en": 'That assumption is no longer current, or this page no longer matches what your project holds, so nothing was saved. Review your current assumptions and try again.',
        "ar": 'لم يعد هذا الافتراض حاليًا، أو لم تعد هذه الصفحة مطابقة لما يحتويه مشروعك، لذلك لم يُحفظ شيء. راجع افتراضاتك الحالية وحاول مجددًا.',
    },
    'UI_S20_ERR_ROUTED': {
        "en": 'This assumption is your note on a question that is waiting for specialist or evidence input, so it cannot be replaced by your own answer. You can still revise it. Nothing was changed.',
        "ar": 'هذا الافتراض هو ملاحظتك على سؤال ينتظر مدخلات متخصّص أو دليلًا، لذلك لا يمكن استبداله بإجابتك. لا يزال بإمكانك تعديله. لم يتم تغيير أي شيء.',
    },
    'UI_S20_ERR_UNKNOWN': {
        "en": 'We could not confirm whether that change was saved. Reload this page to see what your project holds before trying again.',
        "ar": 'لم نتمكّن من التأكد مما إذا كان هذا التغيير قد حُفظ. أعد تحميل هذه الصفحة لترى ما يحتويه مشروعك قبل المحاولة مرة أخرى.',
    },
    'UI_S20_ERR_REVISION_NOT_SHOWN': {
        "en": 'Your revised assumption was saved to your project, but this page could not show it just now. Reload this page to see what your project holds.',
        "ar": 'حُفظ افتراضك المعدَّل في مشروعك، لكن تعذّر عرضه في هذه الصفحة الآن. أعد تحميل هذه الصفحة لترى ما يحتويه مشروعك.',
    },
    'UI_S20_ERR_REPLACEMENT_NOT_APPLIED': {
        "en": 'Your replacement was saved, but it could not be applied to this page just now. What you see below has not changed yet. The saved replacement will be reflected whenever this project can be rebuilt successfully.',
        "ar": 'حُفظ الاستبدال، لكن تعذّر تطبيقه على هذه الصفحة الآن. ما تراه أدناه لم يتغيّر بعد. سيظهر الاستبدال المحفوظ متى أمكن إعادة بناء هذا المشروع بنجاح.',
    },
    "UI_CAP08_REPORT_HEADING": {
        "en": "Dependencies you declared on your provisional assumptions",
        "ar": "اعتمادات أعلنتها على افتراضاتك المؤقتة",
    },
    "UI_CAP08_REPORT_NOT_REQUIREMENT": {
        "en": ("Declared by you; not validated. These are not requirements and "
               "do not change readiness."),
        "ar": ("أعلنتها أنت؛ غير مُتحقَّق منها. هذه ليست متطلبات ولا تغيّر "
               "الجاهزية."),
    },
    "UI_CAP08_REPORT_COUNT": {
        "en": "recorded answer(s) declared dependent",
        "ar": "إجابة (إجابات) مسجّلة أُعلن أنها تعتمد عليه",
    },
    # --- Stage 22 / CAP-05 + CAP-07 Slice 1: read-only decision trace and the
    # separated project-context panel. Presentation only: no key here names a
    # relationship between a decision and any other record, an evidence
    # strength, a confidence or a preferred option.
    "UI_DT_HISTORY_SUMMARY": {
        "en": "Recorded history of this alternative",
        "ar": "السجل المدوَّن لهذا البديل",
    },
    "UI_DT_HISTORY_NOTE": {
        "en": ("Every wording you recorded for this alternative, in the order "
               "you recorded it."),
        "ar": "كل صيغة سجّلتها لهذا البديل، بالترتيب الذي سجّلتها به.",
    },
    "UI_DT_EVENT_DECLARED": {"en": "Declared", "ar": "أُعلِن"},
    "UI_DT_EVENT_REFINED": {"en": "Refined to", "ar": "عُدِّل إلى"},
    "UI_DT_EVENT_WITHDRAWN": {"en": "Withdrawn", "ar": "سُحِب"},
    "UI_DT_TRACE_UNAVAILABLE": {
        "en": ("The recorded history of this alternative could not be shown "
               "right now. Nothing was changed."),
        "ar": "تعذّر عرض السجل المدوَّن لهذا البديل الآن. لم يتغيّر أي شيء.",
    },
    "UI_DT_CTX_HEADING": {
        "en": "Project context — not linked to any decision above",
        "ar": "سياق المشروع — غير مرتبط بأي قرار أعلاه",
    },
    "UI_DT_CTX_NOTE": {
        "en": ("These items are recorded elsewhere in your project. InventorAI "
               "has not linked any of them to a specific decision or "
               "alternative. They are shown for orientation only and say "
               "nothing about which alternative to choose."),
        "ar": ("هذه البنود مسجّلة في مواضع أخرى من مشروعك. لم يربط InventorAI "
               "أيًّا منها بقرار أو بديل محدد. تُعرض للاطلاع فقط، ولا تقول "
               "شيئًا عن البديل الذي ينبغي اختياره."),
    },
    "UI_DT_CAT_DECLARED_CONTRADICTIONS": {
        "en": "Conflicts you declared between recorded answers",
        "ar": "تعارضات أعلنتها بين إجابات مسجّلة",
    },
    "UI_DT_CAT_ASSUMPTION_DEPENDENCIES": {
        "en": "Answer dependencies you declared on an assumption",
        "ar": "علاقات اعتماد أعلنتها بين إجابات وافتراض",
    },
    "UI_DT_CAT_PROVISIONAL_ASSUMPTIONS": {
        "en": "Provisional assumptions", "ar": "افتراضات مؤقتة"},
    "UI_DT_CAT_RECORDED_UNKNOWNS": {
        "en": "Recorded unknowns", "ar": "أمور مجهولة مسجّلة"},
    "UI_DT_CAT_DEFERRED_ITEMS": {
        "en": "Deferred items", "ar": "بنود مؤجَّلة"},
    "UI_DT_CAT_PENDING_EVIDENCE": {
        "en": "Pending evidence requests", "ar": "طلبات أدلة معلّقة"},
    "UI_DT_CAT_PENDING_SPECIALIST": {
        "en": "Waiting for specialist input", "ar": "بانتظار مدخلات متخصص"},
    "UI_DT_CAT_OPEN_GAPS": {
        "en": "Open information gaps", "ar": "فجوات معلومات مفتوحة"},
    "UI_DT_CAT_NEXT_STEP": {
        "en": "Next development step", "ar": "خطوة التطوير التالية"},
    "UI_DT_STATE_CURRENT": {"en": "currently", "ar": "حاليًا"},
    "UI_DT_STATE_EMPTY": {"en": "none at present", "ar": "لا يوجد حاليًا"},
    "UI_DT_STATE_HISTORICAL": {
        "en": "recorded earlier; none is active now",
        "ar": "سُجِّل سابقًا؛ لا يوجد ما هو نشط الآن",
    },
    "UI_DT_STATE_UNAVAILABLE": {
        "en": "could not be shown here", "ar": "تعذّر عرضه هنا"},
    "UI_DT_NEXT_STEP_AVAILABLE": {
        "en": "one is currently shown for your project",
        "ar": "تُعرض حاليًا خطوة لمشروعك",
    },
    "UI_DT_NEXT_STEP_NONE": {
        "en": "none is currently shown", "ar": "لا تُعرض خطوة حاليًا"},
    "UI_DT_SEE": {"en": "see", "ar": "انظر"},
    "UI_DT_LINK_NEXT_STEPS": {
        "en": "the next-steps section", "ar": "قسم الخطوات التالية"},
    # --- Stage 22 / CAP-05 + CAP-07 Slice 2: the read-only project-level action
    # summary. Presentation chrome only: it names no decision, alternative,
    # recommendation, confidence, evidence strength or completed result.
    "UI_AS_HEADING": {
        "en": "What the project currently calls for",
        "ar": "ما يتطلّبه المشروع حاليًا",
    },
    "UI_AS_NOTE": {
        "en": ("These actions come from the current project state. InventorAI has "
               "not linked them to a specific decision or alternative. Listing an "
               "action does not mean it has been carried out."),
        "ar": ("تأتي هذه الإجراءات من حالة المشروع الحالية. لم يربطها InventorAI "
               "بقرار أو بديل محدد. إدراج إجراء هنا لا يعني أنه قد نُفِّذ."),
    },
    "UI_AS_GROUP_OWNER": {
        "en": "You can do these yourself",
        "ar": "يمكنك القيام بها بنفسك",
    },
    "UI_AS_GROUP_SPECIALIST": {
        "en": "Needs specialist input",
        "ar": "يحتاج إلى مدخلات متخصّص",
    },
    "UI_AS_GROUP_EVIDENCE": {
        "en": "Needs evidence or a test",
        "ar": "يحتاج إلى دليل أو اختبار",
    },
    "UI_AS_GROUP_SYSTEM": {
        "en": "System analysis is the current responsibility",
        "ar": "التحليل الآلي هو المسؤولية الحالية",
    },
    "UI_AS_GROUP_CLARIFICATION": {
        "en": "Needs clarification before an action can be assigned",
        "ar": "يحتاج إلى توضيح قبل إسناد إجراء",
    },
    "UI_AS_REPEAT_A": {"en": "(applies to ", "ar": "(ينطبق على "},
    "UI_AS_REPEAT_B": {"en": " recorded items)", "ar": " من العناصر المسجَّلة)"},
    "UI_AS_EMPTY": {
        "en": "The current project state lists no actions at present.",
        "ar": "لا تتضمّن حالة المشروع الحالية أي إجراءات في الوقت الحاضر.",
    },
    "UI_AS_UNAVAILABLE": {
        "en": "This summary could not be shown here. Nothing was changed.",
        "ar": "تعذّر عرض هذا الملخّص هنا. لم يتغيّر أي شيء.",
    },
    "UI_AS_NEXT_STEP": {
        "en": "Current next development step",
        "ar": "خطوة التطوير التالية الحالية",
    },
    "UI_AS_SEE_PLAN": {
        "en": "See the full Validation Plan",
        "ar": "اطّلع على خطة التحقق الكاملة",
    },
    "UI_AS_SEE_PLAN_REPORT": {
        "en": "See the full Validation Plan in the report",
        "ar": "اطّلع على خطة التحقق الكاملة في التقرير",
    },
    # --- CAP-04 Slice 1: the read-only Actionable Gap Pack. Presentation chrome
    # only: no key names a severity, rank, recommendation, provider, completed
    # test, readiness or progression outcome.
    "UI_GP_HEADING": {"en": "Gap action packs", "ar": "حِزم إجراءات الفجوات"},
    "UI_GP_INTRO": {
        "en": ("One package for each open or partially addressed gap, built from "
               "your current project state. It asks you nothing new and changes "
               "nothing."),
        "ar": ("حزمة واحدة لكل فجوة مفتوحة أو معالَجة جزئيًا، مبنية على حالة "
               "مشروعك الحالية. لا تطرح عليك أي سؤال جديد ولا تغيّر أي شيء."),
    },
    "UI_GP_STATE_OPEN": {
        "en": "this recorded gap remains open",
        "ar": "لا تزال هذه الفجوة المسجّلة مفتوحة",
    },
    "UI_GP_STATE_PARTIAL": {
        "en": "this recorded gap remains partially addressed",
        "ar": "لا تزال هذه الفجوة المسجّلة معالَجة جزئيًا",
    },
    "UI_GP_ACTION": {"en": "Required action", "ar": "الإجراء المطلوب"},
    "UI_GP_RESPONSIBILITY": {"en": "Who provides the input",
                             "ar": "مَن يقدّم المدخلات"},
    "UI_GP_RESP_OWNER_EXECUTABLE": {"en": "You can provide it yourself",
                                    "ar": "يمكنك تقديمها بنفسك"},
    "UI_GP_RESP_SPECIALIST_REQUIRED": {"en": "Specialist input is required",
                                       "ar": "مطلوب مدخلات متخصّص"},
    "UI_GP_RESP_EMPIRICAL_EVIDENCE_REQUIRED": {"en": "Empirical evidence is required",
                                               "ar": "مطلوب دليل تجريبي"},
    "UI_GP_RESP_SYSTEM_DERIVABLE": {
        "en": "System analysis is the current responsibility",
        "ar": "التحليل الآلي هو المسؤولية الحالية"},
    "UI_GP_RESP_UNDETERMINED": {
        "en": "Not yet assigned from the current project state",
        "ar": "لم تُحدَّد بعد من حالة المشروع الحالية"},
    "UI_GP_INPUT": {"en": "Input currently required", "ar": "المدخلات المطلوبة حاليًا"},
    "UI_GP_CLOSURE": {"en": "Closure condition", "ar": "شرط الإغلاق"},
    "UI_GP_ROUTED_HEADING": {"en": "Routed need for this gap",
                             "ar": "احتياج موجَّه لهذه الفجوة"},
    "UI_GP_NO_ROUTE": {
        "en": ("No specific acquisition route has been assigned from the current "
               "project state."),
        "ar": "لم يُحدَّد من حالة المشروع الحالية مسار محدد للحصول على هذه المدخلات.",
    },
    "UI_GP_ROUTE_UNAVAILABLE": {
        "en": "Details of this routed need could not be shown here.",
        "ar": "تعذّر عرض تفاصيل هذا الاحتياج الموجَّه هنا.",
    },
    "UI_GP_AFTER": {
        "en": ("What comes next is decided only after the required information is "
               "recorded and the project state is derived again. Recording it does "
               "not by itself close the gap or change readiness."),
        "ar": ("لا يتحدد ما يأتي بعد ذلك إلا بعد تسجيل المعلومات المطلوبة وإعادة "
               "اشتقاق حالة المشروع. تسجيلها لا يُغلق الفجوة ولا يغيّر الجاهزية "
               "بحد ذاته."),
    },
    "UI_GP_EMPTY": {
        "en": ("No open or partially addressed gaps are recorded in the current "
               "project state."),
        "ar": "لا توجد في حالة المشروع الحالية فجوات مفتوحة أو معالَجة جزئيًا.",
    },
    "UI_GP_ACCEPTED_RISK": {
        "en": "These gaps carry an accepted risk and are not treated as resolved:",
        "ar": "هذه الفجوات تحمل مخاطرة مقبولة ولا تُعامَل على أنها محلولة:",
    },
    "UI_GP_UNAVAILABLE": {
        "en": "The gap action packs could not be shown here. Nothing was changed.",
        "ar": "تعذّر عرض حِزم إجراءات الفجوات هنا. لم يتغيّر أي شيء.",
    },
    "UI_GP_SEE_DETAIL": {"en": "See the detail:", "ar": "اطّلع على التفاصيل:"},
    "UI_GP_SEE_DETAIL_REPORT": {"en": "See the detail in the report:",
                                "ar": "اطّلع على التفاصيل في التقرير:"},
    # CAP-02 Slice 1 — Project Compass (session only). Plain four-row chrome;
    # counts are shown per category and never presented as a total.
    "UI_PC_HEADING": {"en": "Where your project stands",
                      "ar": "أين يقف مشروعك الآن"},
    "UI_PC_RECORDED": {"en": "Recorded so far", "ar": "ما سجّلته حتى الآن"},
    "UI_PC_ANSWERS_N": {"en": "Answers recorded:", "ar": "الإجابات المسجّلة:"},
    "UI_PC_ANSWERS_NONE": {"en": "No answers recorded yet.",
                           "ar": "لم تُسجَّل أي إجابة بعد."},
    "UI_PC_RECORDED_NOTE": {
        "en": "These are your own statements as recorded; recording an answer "
              "does not confirm it.",
        "ar": "هذه أقوالك كما سُجّلت؛ وتسجيل الإجابة لا يعني تأكيد صحتها."},
    "UI_PC_UNRESOLVED": {"en": "Still unresolved", "ar": "ما لم يُحسم بعد"},
    "UI_PC_CAT_GAPS": {"en": "Open or partly addressed gaps",
                       "ar": "فجوات مفتوحة أو معالَجة جزئيًا"},
    "UI_PC_CAT_UNKNOWNS": {"en": "Questions you answered as not known yet",
                           "ar": "أسئلة أجبتَ عنها بأنها غير معروفة بعد"},
    "UI_PC_CAT_NOTED_UNKNOWNS": {"en": "Unknowns you mentioned within your answers",
                                 "ar": "أمور غير معروفة ذكرتَها ضمن إجاباتك"},
    "UI_PC_CAT_DEFERRED": {"en": "Items you deferred", "ar": "بنود أجّلتها"},
    "UI_PC_CAT_SPECIALIST": {"en": "Specialist input pending",
                             "ar": "بانتظار مدخلات من مختص"},
    "UI_PC_CAT_EVIDENCE": {"en": "Empirical evidence pending",
                           "ar": "بانتظار أدلة تجريبية"},
    "UI_PC_CAT_CONTRADICTIONS": {"en": "Conflicting recorded answers",
                                 "ar": "إجابات مسجّلة متعارضة"},
    "UI_PC_NOT_SUMMED": {
        "en": "These counts can refer to the same issue, so they are not added "
              "together.",
        "ar": "قد تشير هذه الأعداد إلى المسألة نفسها، لذلك لا تُجمع معًا."},
    "UI_PC_UNRESOLVED_NONE": {
        "en": "Nothing is listed as unresolved at the moment. This does not "
              "mean the project is finished.",
        "ar": "لا يوجد حاليًا ما هو مُدرج على أنه لم يُحسم. وهذا لا يعني أن "
              "المشروع قد اكتمل."},
    "UI_PC_SEE_PACKS": {"en": "Details for each open gap",
                        "ar": "تفاصيل كل فجوة مفتوحة"},
    "UI_PC_WHY": {"en": "Why it matters now", "ar": "لماذا يهمّ هذا الآن"},
    "UI_PC_ADDRESSED_BY": {"en": "How it is addressed:",
                           "ar": "طريقة معالجته:"},
    "UI_PC_WHY_NONE": {
        "en": "No current development focus is derived from what is recorded.",
        "ar": "لا يوجد حاليًا محور تطوير مستخلص مما سُجّل."},
    "UI_PC_UNAVAILABLE": {"en": "Not available right now.",
                          "ar": "غير متاح حاليًا."},
    "UI_PC_DO_NOW": {"en": "What to do now", "ar": "ما الذي تفعله الآن"},
    # CAP-11 Slice 1 — Evidence Details (report Section 2 only). Three
    # independent axes, each on its own row; neutral labels with no order,
    # score or strength verdict (docs/governance/
    # CAP11_EVIDENCE_DETAILS_ENTRY_CONTRACT.md §§6-9).
    "UI_ED_HEADING": {"en": "About this evidence", "ar": "عن هذا الدليل"},
    "UI_ED_FORM": {"en": "Form", "ar": "الصيغة"},
    "UI_ED_SOURCE": {"en": "Source", "ar": "المصدر"},
    "UI_ED_VALIDATION": {"en": "Validation", "ar": "التحقق"},
    "UI_ED_FORM_ASSERTED": {"en": "Asserted", "ar": "تقرير مباشر (Asserted)"},
    "UI_ED_FORM_REASONED": {"en": "Reasoned", "ar": "تعليل منطقي (Reasoned)"},
    "UI_ED_FORM_DEMONSTRATED": {"en": "Demonstrated",
                                "ar": "عرض عملي (Demonstrated)"},
    "UI_ED_FORM_NOTE": {
        "en": "Form describes how the evidence is structured and reasoned. It "
              "is not a validation result.",
        "ar": "تصف الصيغة بنية الدليل وطريقة تعليله، وهي ليست نتيجة تحقق."},
    "UI_ED_SOURCE_OWNER_STATED": {"en": "You", "ar": "أنت"},
    "UI_ED_SOURCE_SYSTEM_INFERRED": {"en": "System-derived",
                                     "ar": "مستخلَص من النظام"},
    "UI_ED_SOURCE_EXPERT_SUPPLIED": {"en": "Expert-supplied",
                                     "ar": "مقدَّم من خبير"},
    "UI_ED_SOURCE_EXTERNAL_EVIDENCE": {"en": "External evidence",
                                       "ar": "دليل خارجي"},
    "UI_ED_SOURCE_LEGACY_UNSPECIFIED": {"en": "Source metadata not available",
                                        "ar": "بيانات المصدر غير متاحة"},
    "UI_ED_VALIDATION_UNVALIDATED": {"en": "No validation recorded",
                                     "ar": "لا يوجد تحقق مسجّل"},
    "UI_ED_VALIDATION_SPECIALIST_REVIEWED": {"en": "Reviewed by a specialist",
                                             "ar": "راجعه مختص"},
    "UI_ED_VALIDATION_EMPIRICALLY_DEMONSTRATED": {
        "en": "Empirically demonstrated", "ar": "مُثبَت تجريبيًا"},
    "UI_ED_VALIDATION_INDEPENDENTLY_VERIFIED": {
        "en": "Independently verified", "ar": "تحقّق منه طرف مستقل"},
    "UI_ED_NA": {"en": "Not available", "ar": "غير متاح"},
    "UI_T3A_EVENT_ANSWER_RECORDED": {
        "en": "Answer recorded",
        "ar": "إجابة مسجَّلة",
    },
    "UI_T3A_EVENT_ANSWER_WITHDRAWN_REPLACED": {
        "en": "Answer withdrawn and replaced",
        "ar": "إجابة مسحوبة ومستبدَلة",
    },
    "UI_T3A_EVENT_NOT_KNOWN_YET": {
        "en": "Not known yet",
        "ar": "غير معروف بعد",
    },
    "UI_T3A_EVENT_DEFERRED": {
        "en": "Deferred",
        "ar": "مؤجَّل",
    },
    "UI_T3A_EVENT_PROVISIONAL_ASSUMPTION": {
        "en": "Provisional assumption",
        "ar": "افتراض مؤقت",
    },
    "UI_T3A_EVENT_SPECIALIST_REQUESTED": {
        "en": "Specialist input requested",
        "ar": "طُلبت مدخلات متخصّص",
    },
    "UI_T3A_EVENT_EVIDENCE_REQUESTED": {
        "en": "Evidence requested",
        "ar": "طُلب دليل",
    },
    "UI_T3A_EVENT_RISK_ACCEPTED": {
        "en": "Risk accepted",
        "ar": "مخاطرة مقبولة",
    },
    "UI_T3A_EVENT_DECISION_CONTEXT_DECLARED": {
        "en": "Decision context declared",
        "ar": "سياق قرار مُعلَن",
    },
    "UI_T3A_EVENT_ALTERNATIVE_DECLARED": {
        "en": "Alternative declared",
        "ar": "بديل مُعلَن",
    },
    "UI_T3A_EVENT_ALTERNATIVE_REFINED": {
        "en": "Alternative refined",
        "ar": "بديل مُنقَّح",
    },
    "UI_T3A_EVENT_ALTERNATIVE_WITHDRAWN": {
        "en": "Alternative withdrawn",
        "ar": "بديل مسحوب",
    },
    "UI_T3A_EVENT_VALUE_RECORDED": {
        "en": "Value recorded",
        "ar": "قيمة مسجَّلة",
    },
    "UI_T3A_EVENT_VALUE_REPLACED": {
        "en": "Value replaced",
        "ar": "قيمة مستبدَلة",
    },
    "UI_T3A_EVENT_REFERENCE_RECORDED": {
        "en": "Reference recorded",
        "ar": "مرجع مسجَّل",
    },
    "UI_T3A_EVENT_REFERENCE_REPLACED": {
        "en": "Reference replaced",
        "ar": "مرجع مستبدَل",
    },
    "UI_T3A_EVENT_REFERENCE_WITHDRAWN": {
        "en": "Reference withdrawn",
        "ar": "مرجع مسحوب",
    },
    "UI_T3A_EVENT_RULES_ADOPTED": {
        "en": "Newer rules adopted",
        "ar": "اعتُمدت قواعد أحدث",
    },
    "UI_T3A_EVENT_RULES_RETURNED": {
        "en": "Returned to earlier rules",
        "ar": "عودة إلى القواعد السابقة",
    },
    "UI_T3A_EVENT_RULES_CHANGED": {
        "en": "Rules changed",
        "ar": "تغيّرت القواعد",
    },
    "UI_T3A_EVENT_OTHER": {
        "en": "Entry recorded",
        "ar": "إدخال مسجَّل",
    },

    # --- Stage 18 / CAP-01 — first authorized bounded guidance profile ------
    # Owner-elected Category-C exception (module docstring). These keys are the
    # COPY of the CAP01_ELECTRONICS_INTERFACE_V1 profile; the domain -> profile
    # table lives below the catalogue. The copy is class-general and CONDITIONAL
    # by construction: it never asserts that the reader's project belongs to the
    # interface class, never says a field is present or missing, carries no
    # numeric value/threshold/equation, no compatibility or safety verdict, no
    # conditioning recommendation, no specialist classification and no named
    # vendor/product/tool/laboratory/standard. Each entry renders through t() so
    # exactly ONE language reaches the reader.
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_TITLE": {
        "en": "Technical information to check — when applicable",
        "ar": "معلومات فنية للمراجعة — عند انطباقها",
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_INTRO": {
        "en": (
            "If your idea involves a low-voltage, non-safety-critical, single-signal "
            "sensor-to-microcontroller interface, useful technical information to provide "
            "or check may include:"
        ),
        "ar": (
            "إذا كانت فكرتك تتضمن واجهة إشارة واحدة بين مستشعر ومتحكم دقيق، ضمن تطبيق منخفض "
            "الجهد وغير حرج للسلامة، فقد تشمل المعلومات الفنية المفيدة التي يمكن توفيرها أو "
            "مراجعتها ما يلي:"
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_ITEM_1": {
        "en": "Sensor output type: analog voltage, single-ended digital logic, or pulse/frequency.",
        "ar": "نوع خرج المستشعر: جهد تماثلي، أو منطق رقمي أحادي الطرف، أو نبضات/تردد.",
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_ITEM_2": {
        "en": "Sensor output voltage or logic-level range.",
        "ar": "نطاق جهد خرج المستشعر أو مستويات المنطق.",
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_ITEM_3": {
        "en": (
            "Microcontroller input requirements, including logic thresholds or ADC "
            "reference/input range when applicable."
        ),
        "ar": (
            "متطلبات دخل المتحكم الدقيق، بما في ذلك عتبات المنطق أو مرجع/نطاق دخل محول ADC "
            "عند انطباق ذلك."
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_ITEM_4": {
        "en": "Source impedance when relevant to the input interface.",
        "ar": "معاوقة المصدر عندما تكون ذات صلة بواجهة الدخل.",
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_ITEM_5": {
        "en": "Pulse/frequency range when the sensor output uses pulses or frequency.",
        "ar": "نطاق النبضات/التردد عندما يعتمد خرج المستشعر على النبضات أو التردد.",
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_ITEM_6": {
        "en": (
            "Governing technical documentation, such as the device datasheet "
            "electrical-characteristics information."
        ),
        "ar": "الوثائق الفنية الحاكمة، مثل معلومات الخصائص الكهربائية في ورقة بيانات الجهاز.",
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_BOUNDARY": {
        "en": (
            "InventorAI is presenting a class-general checklist only. In this first "
            "increment, it does not determine that your project belongs to this interface "
            "class and does not inspect your record to decide which of these items are "
            "present or missing."
        ),
        "ar": (
            "يعرض InventorAI هنا قائمة عامة مرتبطة بهذه الفئة الفنية فقط. في هذا الإصدار "
            "الأول، لا يقرر النظام أن مشروعك ينتمي إلى هذا النوع من الواجهات، ولا يفحص سجلك "
            "ليحدد أيًا من هذه المعلومات موجود أو مفقود."
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_LIMIT": {
        "en": (
            "It does not determine compatibility, safe limits, device-specific values, "
            "circuit correctness, signal-conditioning method, or specialist suitability. "
            "Device-specific values require appropriate governing technical documentation "
            "and independent verification."
        ),
        "ar": (
            "لا يحدد النظام التوافق، أو الحدود الآمنة، أو القيم الخاصة بالجهاز، أو صحة "
            "الدائرة، أو طريقة تكييف الإشارة، أو ملاءمة فئة أخصائي. وتتطلب القيم الخاصة "
            "بالجهاز الرجوع إلى الوثائق الفنية الحاكمة المناسبة والتحقق المستقل."
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_EVIDENCE": {
        "en": (
            "These topics come from the accepted bounded D13 technical knowledge package. "
            "They are based on corroborated/reasoned evidence and are not primary-verified "
            "device-specific conclusions."
        ),
        "ar": (
            "تستند هذه الموضوعات إلى حزمة المعرفة التقنية D13 المقبولة والمحدودة النطاق. "
            "وهي مبنية على أدلة مؤيدة/استدلالية، وليست استنتاجات خاصة بجهاز تم التحقق منها "
            "من مصدر أولي."
        ),
    },

    # --- Stage 18 / CAP-01 second bounded increment: research-direction addendum --
    # Owner-authorized copy for the SAME CAP01_ELECTRONICS_INTERFACE_V1 profile. It
    # tells the reader WHERE to look and WHICH generic search terms may help find the
    # information the checklist above names. It is navigation aid only: no web or
    # datasheet retrieval, no evidence, no numeric value, no threshold, no vendor,
    # product, laboratory, standard or specialist, and no claim that any item applies
    # to, or is missing from, the reader's project. The profile's BOUNDARY, LIMIT and
    # EVIDENCE copy above governs this addendum too.
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_RESEARCH_TITLE": {
        "en": "Where to look next — research direction",
        "ar": "أين تبحث لاحقًا — توجيه البحث",
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_RESEARCH_INTRO": {
        "en": (
            "If one of the checklist items is relevant to your idea, use the matching "
            "documentation category and search terms below to locate the governing "
            "technical information. These are research aids only; they do not establish "
            "that your project needs a specific value, method, component, or specialist."
        ),
        "ar": (
            "إذا كان أحد بنود القائمة مناسبًا لفكرتك، فاستخدم فئة الوثائق وعبارات البحث "
            "المقابلة أدناه للوصول إلى المعلومات الفنية الحاكمة. هذه وسائل مساعدة للبحث "
            "فقط؛ ولا تثبت أن مشروعك يحتاج قيمة أو طريقة أو مكوّنًا أو مختصًا بعينه."
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_RESEARCH_ITEM_1": {
        "en": (
            "Sensor output type — look in the sensor datasheet sections describing output "
            "or signal characteristics. Search terms: “sensor output signal type”, "
            "“analog digital pulse frequency output”."
        ),
        "ar": (
            "نوع خرج المستشعر — راجع أقسام ورقة بيانات المستشعر التي تصف الخرج أو خصائص "
            "الإشارة. عبارات بحث مقترحة: «نوع إشارة خرج المستشعر»، «خرج تماثلي رقمي نبضي "
            "ترددي»."
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_RESEARCH_ITEM_2": {
        "en": (
            "Sensor output voltage or logic levels — look in sections such as Output "
            "Characteristics, Electrical Characteristics, or DC Characteristics. Search "
            "terms: “sensor output voltage range”, “logic output VOH VOL”."
        ),
        "ar": (
            "جهد خرج المستشعر أو مستويات المنطق — راجع أقسامًا مثل خصائص الخرج أو الخصائص "
            "الكهربائية أو خصائص التيار المستمر. عبارات بحث مقترحة: «نطاق جهد خرج "
            "المستشعر»، «مستويات خرج المنطق VOH VOL»."
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_RESEARCH_ITEM_3": {
        "en": (
            "Microcontroller input requirements — look in I/O Pin Characteristics, "
            "Electrical Characteristics, and ADC/Reference sections when applicable. "
            "Search terms: “MCU input voltage range”, “ADC reference voltage”, “VIH VIL "
            "input threshold”."
        ),
        "ar": (
            "متطلبات دخل المتحكم الدقيق — راجع خصائص أطراف الإدخال/الإخراج والخصائص "
            "الكهربائية وأقسام محول ADC أو الجهد المرجعي عند انطباقها. عبارات بحث مقترحة: "
            "«نطاق جهد دخل المتحكم الدقيق»، «الجهد المرجعي ADC»، «عتبات الدخل VIH VIL»."
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_RESEARCH_ITEM_4": {
        "en": (
            "Source impedance — look in sensor Output Impedance or Output Characteristics "
            "and in the MCU/ADC Input or Acquisition Characteristics. Search terms: "
            "“sensor output impedance”, “ADC source impedance”, “input loading”."
        ),
        "ar": (
            "معاوقة المصدر — راجع معاوقة الخرج أو خصائص الخرج في ورقة بيانات المستشعر، "
            "وخصائص الدخل أو الاكتساب الخاصة بالمتحكم الدقيق أو ADC. عبارات بحث مقترحة: "
            "«معاوقة خرج المستشعر»، «معاوقة المصدر ADC»، «تحميل الدخل»."
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_RESEARCH_ITEM_5": {
        "en": (
            "Pulse/frequency — look in the sensor Timing or Frequency Output sections and "
            "the MCU Timer/Counter/Input Capture sections. Search terms: “sensor pulse "
            "frequency range”, “timer input capture”, “pulse counting input”."
        ),
        "ar": (
            "النبضات/التردد — راجع أقسام التوقيت أو خرج التردد في ورقة بيانات المستشعر، "
            "وأقسام المؤقت أو العداد أو التقاط الدخل في المتحكم الدقيق. عبارات بحث "
            "مقترحة: «نطاق تردد نبضات المستشعر»، «التقاط دخل المؤقت»، «دخل عد النبضات»."
        ),
    },
    "UI_CAP01_ELECTRONICS_INTERFACE_V1_RESEARCH_ITEM_6": {
        "en": (
            "Governing documentation — prioritize the applicable device datasheet "
            "sections such as Electrical Characteristics, DC Characteristics, Timing "
            "Characteristics, I/O Characteristics, and ADC Characteristics. When a device "
            "or part number is known, combine it with the relevant section or parameter "
            "in the search terms."
        ),
        "ar": (
            "الوثائق الفنية الحاكمة — أعطِ الأولوية لأقسام ورقة بيانات الجهاز ذات الصلة، "
            "مثل الخصائص الكهربائية وخصائص التيار المستمر وخصائص التوقيت وخصائص "
            "الإدخال/الإخراج وخصائص ADC. عندما يكون اسم الجهاز أو رقم الجزء معروفًا، "
            "ادمجه مع اسم القسم أو المعامل ذي الصلة في عبارة البحث."
        ),
    },

    # --- MECHANICAL CAP-01 — OPEN-GAP TECHNICAL CONTEXT (Owner-authorized bounded
    # slice). Gap-scoped explanatory copy for the governed Mechanical package
    # (domains/mechanical/domain.json: gap_type_mappings, rule_nuances,
    # capability_declaration, coverage_declaration). Each context states, at
    # concept level, what the EXACT canonical gap concerns and what InventorAI does
    # NOT conclude from it. Explanatory only: no question, action, responsibility,
    # required input, closure rule or next action (Path-N and CAP-04 keep those).
    # The D13 Electronics package is NOT a source of any line below. Selection is
    # owned by web/cap01_guidance.py by exact canonical gap identity + lifecycle
    # state; these entries are copy only and never bind anything.
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_TITLE": {
        "en": "Technical context for the unresolved mechanical gaps",
        "ar": "سياق فني للفجوات الميكانيكية غير المحسومة",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_INTRO": {
        "en": (
            "Each note below explains, at concept level only, what one currently open "
            "or partially addressed gap concerns within InventorAI's mechanical coverage, "
            "and what InventorAI does not conclude from it. These notes are explanatory "
            "context only: they add no question, no action, no responsibility and no "
            "closure rule, and they do not replace the gap action packs or the "
            "Validation Plan."
        ),
        "ar": (
            "توضّح كل ملاحظة أدناه، على المستوى المفاهيمي فقط، ما تتعلق به فجوة واحدة "
            "مفتوحة حاليًا أو مُعالَجة جزئيًا ضمن التغطية الميكانيكية في InventorAI، "
            "وما الذي لا يستنتجه InventorAI منها. هذه الملاحظات سياق توضيحي فقط: لا "
            "تضيف سؤالًا ولا إجراءً ولا مسؤولية ولا شرط إغلاق، ولا تحل محل حِزم إجراءات "
            "الفجوات أو خطة التحقق (Validation Plan)."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_TITLE": {
        "en": "Mechanism completeness — what this gap concerns",
        "ar": "اكتمال الآلية (Mechanism Completeness) — ما تتعلق به هذه الفجوة",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_MEANING": {
        "en": (
            "This gap concerns the concept-level description of how the mechanism works "
            "physically: the sequence of physical steps it takes to achieve its function; "
            "what moves, connects or transfers force; and the individual mechanical "
            "components and how each one contributes to the overall motion or function. "
            "Where such physical detail is still missing from the description, mechanism "
            "completeness remains unresolved at concept level."
        ),
        "ar": (
            "تتعلق هذه الفجوة بالوصف المفاهيمي لكيفية عمل الآلية فيزيائيًا: تسلسل الخطوات "
            "الفيزيائية التي تؤدي بها وظيفتها؛ وما الذي يتحرك أو يتصل أو ينقل القوة؛ "
            "والمكوّنات الميكانيكية المنفردة وكيف يساهم كل منها في الحركة أو الوظيفة "
            "الكلية. وحيث يظل هذا التفصيل الفيزيائي غائبًا عن الوصف، يبقى اكتمال الآلية "
            "غير محسوم على المستوى المفاهيمي."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_LIMIT": {
        "en": (
            "InventorAI does not conclude from this gap, or from its later closure, that "
            "the mechanism is engineering-complete, buildable, dimensionally correct, "
            "physically fitting, structurally adequate or made of suitable materials, and "
            "it does not conclude how the mechanism would perform in the real world. "
            "Mechanism completeness here is a concept-level reasoning assessment, not "
            "detailed engineering."
        ),
        "ar": (
            "لا يستنتج InventorAI من هذه الفجوة، ولا من إغلاقها لاحقًا، أن الآلية مكتملة "
            "هندسيًا، أو قابلة للبناء، أو صحيحة الأبعاد، أو متوافقة فيزيائيًا في التركيب، "
            "أو كافية إنشائيًا، أو مصنوعة من مواد مناسبة، ولا يستنتج كيف ستعمل الآلية في "
            "الواقع. اكتمال الآلية هنا تقييم استدلالي على المستوى المفاهيمي، وليس هندسة "
            "تفصيلية."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_TITLE": {
        "en": "Physical feasibility — what this gap concerns",
        "ar": "الجدوى الفيزيائية (Physical Feasibility) — ما تتعلق به هذه الفجوة",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_MEANING": {
        "en": (
            "This gap concerns, at concept level, the physical principle the inventor says "
            "the mechanism relies on — for example leverage, spring tension, gear ratio or "
            "friction — and the material or force constraints the inventor states the "
            "mechanism must operate within. Where that principle or those constraints are "
            "not yet stated or clarified, physical feasibility remains an unresolved "
            "concept-level gap."
        ),
        "ar": (
            "تتعلق هذه الفجوة، على المستوى المفاهيمي، بالمبدأ الفيزيائي الذي يقول المخترع إن "
            "الآلية تعتمد عليه — مثل الرافعة، أو شدّ النابض، أو نسبة التروس، أو الاحتكاك — "
            "وبقيود المواد أو القوى التي يذكر المخترع أن الآلية يجب أن تعمل ضمنها. وحيث لم "
            "يُذكر هذا المبدأ أو لم تُوضَّح هذه القيود بعد، تبقى الجدوى الفيزيائية فجوة غير "
            "محسومة على المستوى المفاهيمي."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_LIMIT": {
        "en": (
            "This note explains an unresolved concept-level gap; it does not establish, "
            "and InventorAI does not conclude, that the mechanism is physically feasible. "
            "Real-world loads, wear, environmental conditions and failure behavior remain "
            "unknown unless separately evidenced, and it cannot be established in software "
            "whether the mechanism performs as intended. InventorAI calculates or "
            "recommends no load, limit, value, material or dimension."
        ),
        "ar": (
            "توضّح هذه الملاحظة فجوة غير محسومة على المستوى المفاهيمي؛ وهي لا تثبت، ولا "
            "يستنتج InventorAI، أن الآلية ممكنة فيزيائيًا. تبقى الأحمال الواقعية، والتآكل، "
            "والظروف البيئية، وسلوك الفشل مجهولةً ما لم تُدعَم بأدلة مستقلة، ولا يمكن "
            "إثبات أن الآلية تعمل كما هو مقصود عبر البرمجيات. ولا يحسب InventorAI ولا يوصي "
            "بأي حمل أو حدّ أو قيمة أو مادة أو بُعد."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_BOUNDARY_AMBIGUITY_TITLE": {
        "en": "Scope and boundaries — what this gap concerns",
        "ar": "النطاق والحدود (Boundary Ambiguity) — ما تتعلق به هذه الفجوة",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_BOUNDARY_AMBIGUITY_MEANING": {
        "en": (
            "This gap concerns, at concept level, what the mechanism does and does not do "
            "or cover, whether a clear mechanical boundary has been stated, and the "
            "concrete physical way in which the inventor describes it as different from an "
            "existing mechanical approach. Where that scope or that distinction is not yet "
            "stated, the boundary remains ambiguous at concept level."
        ),
        "ar": (
            "تتعلق هذه الفجوة، على المستوى المفاهيمي، بما تفعله الآلية وما لا تفعله أو لا "
            "تغطيه، وبما إذا كان قد ذُكر حدّ ميكانيكي واضح، وبالطريقة الفيزيائية الملموسة "
            "التي يصف بها المخترع اختلافها عن نهج ميكانيكي قائم. وحيث لم يُذكر هذا النطاق أو "
            "هذا الاختلاف بعد، يبقى الحدّ غامضًا على المستوى المفاهيمي."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_BOUNDARY_AMBIGUITY_LIMIT": {
        "en": (
            "InventorAI does not conclude from this gap, or from its later closure, that "
            "the mechanism is novel or patentable, superior to an existing approach, "
            "differentiated in a validated way, compliant with any regulation or "
            "standard, or ready for production. The distinction described is the "
            "inventor's own concept-level statement."
        ),
        "ar": (
            "لا يستنتج InventorAI من هذه الفجوة، ولا من إغلاقها لاحقًا، أن الآلية جديدة أو "
            "قابلة للحماية ببراءة اختراع، أو أنها أفضل من نهج قائم، أو أن تمايزها مُتحقَّق "
            "منه، أو أنها متوافقة مع أي لائحة أو معيار، أو جاهزة للإنتاج. والاختلاف "
            "الموصوف هو بيان المخترع نفسه على المستوى المفاهيمي."
        ),
    },

    # --- MECHANICAL TECHNICAL DEEPENING SLICE 1 — FORCE, MOMENT & PRESSURE FUNDAMENTALS
    # (Owner-authorized bounded reference fundamentals). OPTIONAL sub-view of the
    # Mechanical CAP-01 PHYSICAL_FEASIBILITY gap context above: the SAME bounded
    # reference set renders only while the exact canonical PHYSICAL_FEASIBILITY gap is
    # OPEN or PARTIAL (selection owned by web/cap01_guidance.py; these entries bind
    # nothing). Four bounded claims declared in domains/mechanical/domain.json
    # (reference_fundamentals / force_moment_pressure_v1) with exact source
    # provenance mechanical:PR006–PR009 and source-use-policy provenance
    # mechanical:PR010–PR011. Factual paraphrase only: no copied NASA / NIST
    # explanatory prose, no image / logo / media, no endorsement implication, no
    # project-specific calculation, no formula selection. Equations and unit
    # symbols live in their own EQUATION keys so the template can isolate them
    # with dir="ltr"; they are language-neutral and identical in EN and AR.
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_TITLE": {
        "en": "Reference fundamentals that may help with this gap",
        "ar": "أساسيات مرجعية قد تساعد في فهم هذه الفجوة",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_INTRO": {
        "en": (
            "These relationships are reference fundamentals that may be relevant. InventorAI has "
            "not determined that any of them applies to your design. Use only a relationship that "
            "matches your actual mechanism and verified inputs."
        ),
        "ar": (
            "هذه علاقات مرجعية قد تكون ذات صلة. لم يحدد InventorAI أن أيًا منها ينطبق على تصميمك. "
            "استخدم فقط العلاقة التي تطابق آليتك الفعلية ومدخلاتك المتحقق منها."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_TITLE": {
        "en": "Torque / moment",
        "ar": "العزم / عزم القوة",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_LEAD": {
        "en": "For a perpendicular force about a pivot:",
        "ar": "في حالة قوة عمودية حول نقطة ارتكاز:",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_EQUATION": {
        "en": "T = F × L⊥",
        "ar": "T = F × L⊥",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_NOTE": {
        "en": (
            "L⊥ is the perpendicular moment arm. This is a reference relationship, not a "
            "calculation for your project."
        ),
        "ar": "حيث L⊥ هو ذراع العزم العمودي. هذه علاقة مرجعية وليست حسابًا لمشروعك.",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_2_TITLE": {
        "en": "Ideal static moment balance",
        "ar": "اتزان العزوم الساكن المثالي",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_2_LEAD": {
        "en": "For an ideal statically balanced pivot with perpendicular forces:",
        "ar": "في نظام مثالي متزن ساكنًا حول نقطة ارتكاز ومع قوى عمودية:",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_2_EQUATION": {
        "en": "F₁L₁ = F₂L₂",
        "ar": "F₁L₁ = F₂L₂",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_2_NOTE": {
        "en": (
            "This ideal relationship does not account for friction, deformation, acceleration, "
            "dynamic response or structural adequacy."
        ),
        "ar": (
            "لا تشمل هذه العلاقة المثالية الاحتكاك أو التشوه أو التسارع أو الاستجابة الديناميكية "
            "أو الكفاية الإنشائية."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_3_TITLE": {
        "en": "Pressure / force / area",
        "ar": "الضغط / القوة / المساحة",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_3_LEAD": {
        "en": "For uniform pressure acting over an effective area:",
        "ar": "عند تأثير ضغط منتظم على مساحة فعالة:",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_3_EQUATION": {
        "en": "F = pA",
        "ar": "F = pA",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_3_NOTE": {
        "en": (
            "This reference relationship does not establish hydraulic-system performance, "
            "pressure losses, seal behaviour, component ratings, fluid suitability or safety."
        ),
        "ar": (
            "لا تثبت هذه العلاقة المرجعية أداء نظام هيدروليكي أو فواقد الضغط أو سلوك الأختام أو "
            "تصنيفات المكونات أو ملاءمة المائع أو السلامة."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_4_TITLE": {
        "en": "SI units",
        "ar": "وحدات SI",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_4_LEAD": {
        "en": "Torque / moment is expressed in",
        "ar": "يُعبَّر عن العزم / عزم القوة بوحدة",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_4_EQUATION": {
        "en": "N·m",
        "ar": "N·m",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_4_NOTE": {
        "en": "Pressure is expressed in Pa or kPa. Correct units do not validate a design.",
        "ar": "يُعبَّر عن الضغط بوحدة Pa أو kPa. صحة الوحدات لا تعني صحة التصميم.",
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_SOURCE": {
        "en": (
            "Reference source material: NASA Glenn Research Center — Torque (Moment), Balance Of "
            "Forces, Aerodynamic Forces; NIST Guide to the SI, SP 811 Appendix B.9."
        ),
        "ar": (
            "مواد مرجعية: مركز غلين للأبحاث التابع لناسا — Torque (Moment)، Balance Of Forces، "
            "Aerodynamic Forces؛ ودليل NIST للنظام الدولي للوحدات، SP 811 Appendix B.9."
        ),
    },
    "UI_CAP01_MECHANICAL_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_BOUNDARY": {
        "en": (
            "These reference fundamentals do not satisfy the physical feasibility gap, perform a "
            "project calculation, prove that the mechanism works, establish safety or structural "
            "adequacy, or validate the invention."
        ),
        "ar": (
            "هذه الأساسيات المرجعية لا تغلق فجوة الجدوى الفيزيائية (Physical Feasibility)، ولا "
            "تنفذ حسابًا خاصًا بالمشروع، ولا تثبت أن الآلية تعمل أو أن التصميم آمن أو كافٍ "
            "إنشائيًا، ولا تثبت أن الاختراع تم التحقق منه."
        ),
    },

    # --- ELECTRICAL / ELECTRONICS TECHNICAL DEEPENING SLICE 1 — BASIC ELECTRICAL
    # REFERENCE FUNDAMENTALS (Owner-authorized bounded reference fundamentals). ONE
    # gap-scoped context for the EXACT canonical Electronics PHYSICAL_FEASIBILITY gap,
    # grounded in the governed Electronics package (domains/electronics_electrical/
    # domain.json: its PHYSICAL_FEASIBILITY gap mapping, rule nuance RN002 and
    # coverage declaration), plus its OPTIONAL reference-fundamentals sub-view: three
    # bounded claims declared in the pack (reference_fundamentals /
    # basic_electrical_reference_v1) with source provenance
    # electronics_electrical:PR004–PR005 and source-use-policy provenance
    # electronics_electrical:PR006–PR007. The handbook writes E for voltage; the
    # SAME relationships are shown with V (notation normalization only). Factual
    # paraphrase only: no copied DOE / NIST prose, figure, diagram, photograph or
    # logo, no endorsement implication, no IEC / IPC text, no project-specific
    # calculation, no formula selection. This is separate from, and does not repeat,
    # the domain-level CAP01_ELECTRONICS_INTERFACE_V1 checklist above. Selection is
    # owned by web/cap01_guidance.py by exact canonical gap identity + lifecycle
    # state; these entries bind nothing. Equations and unit symbols live in their
    # own EQUATION keys (language-neutral, identical in EN and AR) so the template
    # isolates them with dir="ltr". The Stage-18 closure adds the
    # MECHANISM_COMPLETENESS / BOUNDARY_AMBIGUITY contexts of this group (at the end
    # of this catalogue), so the group title and intro now speak of the gaps.
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_TITLE": {
        "en": "Technical context for the unresolved electrical / electronics gaps",
        "ar": "سياق فني للفجوات الكهربائية / الإلكترونية غير المحسومة",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_INTRO": {
        "en": (
            "Each note below explains, at concept level only, what one currently open or "
            "partially addressed gap concerns within InventorAI's electronics / electrical "
            "coverage, and what InventorAI does not conclude from it. These notes are explanatory "
            "context only: they add no question, action, responsibility or closure rule, and they "
            "do not replace the technical-information checklist, the gap action packs or the "
            "Validation Plan."
        ),
        "ar": (
            "توضّح كل ملاحظة أدناه، على المستوى المفاهيمي فقط، ما تتعلق به فجوة واحدة مفتوحة حاليًا "
            "أو مُعالَجة جزئيًا ضمن تغطية الإلكترونيات / الكهرباء في InventorAI، وما الذي لا "
            "يستنتجه InventorAI منها. هذه الملاحظات سياق توضيحي فقط: لا تضيف سؤالًا ولا إجراءً ولا "
            "مسؤولية ولا شرط إغلاق، ولا تحل محل قائمة المعلومات الفنية أو حِزم إجراءات الفجوات أو "
            "خطة التحقق (Validation Plan)."
        ),
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_TITLE": {
        "en": "Electrical feasibility — what this gap concerns",
        "ar": "الجدوى الكهربائية (Physical Feasibility) — ما تتعلق به هذه الفجوة",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_MEANING": {
        "en": (
            "This gap concerns, at concept level, what provides the energy or power for the "
            "design to operate, and the electrical requirements or constraints — such as "
            "voltage, current or frequency — that the inventor states the design depends on or "
            "must stay within. Where that power source or those requirements are not yet stated "
            "or clarified, electrical feasibility remains an unresolved concept-level gap."
        ),
        "ar": (
            "تتعلق هذه الفجوة، على المستوى المفاهيمي، بما يوفّر الطاقة أو القدرة اللازمة لتشغيل "
            "التصميم، وبالمتطلبات أو القيود الكهربائية — مثل الجهد أو التيار أو التردد — التي يذكر "
            "المخترع أن التصميم يعتمد عليها أو يجب أن يبقى ضمنها. وحيث لم يُذكر مصدر القدرة هذا أو "
            "لم تُوضَّح هذه المتطلبات بعد، تبقى الجدوى الكهربائية فجوة غير محسومة على المستوى "
            "المفاهيمي."
        ),
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_LIMIT": {
        "en": (
            "This note explains an unresolved concept-level gap; it does not establish, and "
            "InventorAI does not conclude, that the design is electrically feasible, compatible "
            "or safe. InventorAI does not calculate or recommend any voltage, current, power, "
            "limit, component value or rating."
        ),
        "ar": (
            "توضّح هذه الملاحظة فجوة غير محسومة على المستوى المفاهيمي؛ وهي لا تثبت، ولا يستنتج "
            "InventorAI، أن التصميم ممكن كهربائيًا أو متوافق أو آمن. ولا يحسب InventorAI ولا يوصي "
            "بأي جهد أو تيار أو قدرة أو حدّ أو قيمة مكوّن أو تصنيف."
        ),
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_TITLE": {
        "en": "Reference fundamentals that may help with this electrical feasibility gap",
        "ar": "أساسيات مرجعية قد تساعد في فهم فجوة الجدوى الكهربائية هذه",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_INTRO": {
        "en": (
            "These are basic electrical reference relationships. InventorAI has not determined "
            "that these relationships apply to your design. Use a relationship only where it "
            "matches your actual circuit and verified values."
        ),
        "ar": (
            "هذه علاقات كهربائية مرجعية أساسية. لم يحدد InventorAI أن هذه العلاقات تنطبق على "
            "تصميمك. استخدم العلاقة فقط حيث تطابق دائرتك الفعلية وقيمك المتحقق منها."
        ),
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_TITLE": {
        "en": "Ohm's law (resistive reference)",
        "ar": "قانون أوم (Ohm's law) — مرجع للعناصر المقاومية",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_LEAD": {
        "en": "For a resistive element, where V is voltage, I is current and R is resistance:",
        "ar": "لعنصر مقاومي، حيث V الجهد و I التيار و R المقاومة:",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_EQUATION": {
        "en": "V = I × R",
        "ar": "V = I × R",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_1_NOTE": {
        "en": (
            "A bounded Ohm's-law / resistive reference relationship, not a calculation for your "
            "circuit. InventorAI has not determined that your device, component or circuit "
            "behaves this way."
        ),
        "ar": (
            "علاقة مرجعية محدودة لقانون أوم / العناصر المقاومية، وليست حسابًا لدائرتك. لم يحدد "
            "InventorAI أن جهازك أو مكوّنك أو دائرتك تتصرف بهذه الطريقة."
        ),
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_2_TITLE": {
        "en": "Basic electrical power",
        "ar": "القدرة الكهربائية الأساسية",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_2_LEAD": {
        "en": "Basic reference form, where P is power, V is voltage and I is current:",
        "ar": "الصيغة المرجعية الأساسية، حيث P القدرة و V الجهد و I التيار:",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_2_EQUATION": {
        "en": "P = V × I",
        "ar": "P = V × I",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_2_NOTE": {
        "en": (
            "A basic power reference relationship. It does not establish component rating, "
            "power-supply suitability, battery sizing, efficiency, thermal adequacy or safety."
        ),
        "ar": (
            "علاقة مرجعية أساسية للقدرة. لا تثبت تصنيف المكوّنات، ولا ملاءمة مصدر التغذية، ولا "
            "تحديد سعة البطارية، ولا الكفاءة، ولا الكفاية الحرارية، ولا السلامة."
        ),
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_3_TITLE": {
        "en": "SI units",
        "ar": "وحدات SI",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_3_LEAD": {
        "en": "Voltage, current, resistance and power are expressed in volts, amperes, ohms and watts:",
        "ar": "يُعبَّر عن الجهد والتيار والمقاومة والقدرة بوحدات الفولت والأمبير والأوم والواط:",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_3_EQUATION": {
        "en": "V, A, Ω, W",
        "ar": "V, A, Ω, W",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_ITEM_3_NOTE": {
        "en": "Correct units do not validate a circuit or design.",
        "ar": "صحة الوحدات لا تعني صحة الدائرة أو التصميم.",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_SOURCE": {
        "en": (
            "Reference source material: U.S. Department of Energy — Electrical Science, "
            "DOE-HDBK-1011/1-92; NIST Guide to the SI, SP 811 Appendix B.9."
        ),
        "ar": (
            "مواد مرجعية: وزارة الطاقة الأمريكية (U.S. Department of Energy) — Electrical "
            "Science، DOE-HDBK-1011/1-92؛ ودليل NIST للنظام الدولي للوحدات، SP 811 Appendix B.9."
        ),
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_PHYSICAL_FEASIBILITY_FUNDAMENTALS_BOUNDARY": {
        "en": (
            "These reference fundamentals do not close the electrical feasibility gap, calculate "
            "your design, establish compatibility or safe voltage / current limits, prove that the "
            "circuit works, size any component, prove electrical safety or validate the invention."
        ),
        "ar": (
            "هذه الأساسيات المرجعية لا تغلق فجوة الجدوى الكهربائية، ولا تحسب تصميمك، ولا تثبت "
            "التوافق أو حدود الجهد / التيار الآمنة، ولا تثبت أن الدائرة تعمل، ولا تحدد مقاسات أي "
            "مكوّن، ولا تثبت السلامة الكهربائية، ولا تثبت أن الاختراع تم التحقق منه."
        ),
    },
    # Stage 18 — Gap-Scoped Technical Next-Step Guidance — Closure. The Electronics
    # MECHANISM_COMPLETENESS / BOUNDARY_AMBIGUITY contexts (grounded only in the
    # governed Electronics pack questions) and, per authorized (domain, gap), ONE
    # optional next-steps sub-view: a bounded summary of the gap's own canonical
    # questions, what to look into, generic search terms (language-neutral English
    # tokens, identical in EN and AR, rendered dir="ltr"), class-level measure /
    # check / document categories and an explicit specialist abstention. Selection
    # and source anchors live in web/cap01_guidance.py; these entries bind nothing.
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_TITLE": {
        "en": "Circuit mechanism completeness — what this gap concerns",
        "ar": "اكتمال آلية الدائرة (Mechanism Completeness) — ما تتعلق به هذه الفجوة",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_MEANING": {
        "en": "This gap concerns, at concept level, how the circuit achieves its intended function: what happens electrically from input to output, the signal or energy transformation it performs, and the electronic components central to it and the role each plays. Where that electrical sequence or those roles are not yet described, circuit mechanism completeness remains unresolved at concept level.",
        "ar": "تتعلق هذه الفجوة، على المستوى المفاهيمي، بكيفية تحقيق الدائرة لوظيفتها المقصودة: ما الذي يحدث كهربائيًا من المدخل إلى المخرج، وتحويل الإشارة أو الطاقة الذي تؤديه، والمكوّنات الإلكترونية المحورية فيها ودور كل منها. وحيث لم يُوصف هذا التسلسل الكهربائي أو هذه الأدوار بعد، يبقى اكتمال آلية الدائرة غير محسوم على المستوى المفاهيمي.",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_MECHANISM_COMPLETENESS_LIMIT": {
        "en": "InventorAI does not conclude from this gap, or from its later closure, that the circuit works, is correctly designed, uses suitable components or is ready to build, and it makes no safety determination. Circuit mechanism completeness here is a concept-level reasoning assessment, not circuit design or verification.",
        "ar": "لا يستنتج InventorAI من هذه الفجوة، ولا من إغلاقها لاحقًا، أن الدائرة تعمل، أو أنها مصممة بشكل صحيح، أو أنها تستخدم مكوّنات مناسبة، أو أنها جاهزة للبناء، ولا يُصدر أي حكم بشأن السلامة. اكتمال آلية الدائرة هنا تقييم استدلالي على المستوى المفاهيمي، وليس تصميمًا للدائرة أو تحققًا منها.",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_BOUNDARY_AMBIGUITY_TITLE": {
        "en": "Electronic design boundaries — what this gap concerns",
        "ar": "حدود التصميم الإلكتروني (Boundary Ambiguity) — ما تتعلق به هذه الفجوة",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_BOUNDARY_AMBIGUITY_MEANING": {
        "en": "This gap concerns, at concept level, what the electronic design does and does not do or handle, where it stops and another system or component begins, and which external systems, components or interfaces it depends on to function. Where that scope or those dependencies are not yet stated, the design's boundary remains ambiguous at concept level.",
        "ar": "تتعلق هذه الفجوة، على المستوى المفاهيمي، بما يفعله التصميم الإلكتروني وما لا يفعله أو لا يتعامل معه، وبالنقطة التي يتوقف عندها ويبدأ نظام أو مكوّن آخر، وبالأنظمة أو المكوّنات أو الواجهات الخارجية التي يعتمد عليها ليعمل. وحيث لم يُذكر هذا النطاق أو هذه الاعتمادات بعد، يبقى حدّ التصميم غامضًا على المستوى المفاهيمي.",
    },
    "UI_CAP01_ELECTRONICS_GAP_CONTEXT_V1_BOUNDARY_AMBIGUITY_LIMIT": {
        "en": "InventorAI does not conclude from this gap, or from its later closure, that the design is compatible with any external system, component or interface, meets any regulation or standard, is novel or is ready for production. The boundary described is the inventor's own concept-level statement.",
        "ar": "لا يستنتج InventorAI من هذه الفجوة، ولا من إغلاقها لاحقًا، أن التصميم متوافق مع أي نظام أو مكوّن أو واجهة خارجية، أو أنه يستوفي أي لائحة أو معيار، أو أنه جديد، أو جاهز للإنتاج. والحدّ الموصوف هو بيان المخترع نفسه على المستوى المفاهيمي.",
    },
    "UI_CAP01_NEXT_STEPS_V1_TITLE": {
        "en": "Technical next steps for this gap",
        "ar": "خطوات فنية تالية لهذه الفجوة",
    },
    "UI_CAP01_NEXT_STEPS_V1_MISSING_LABEL": {
        "en": "Information still missing:",
        "ar": "المعلومات التي لا تزال ناقصة:",
    },
    "UI_CAP01_NEXT_STEPS_V1_LOOK_LABEL": {
        "en": "What to look into",
        "ar": "ما الذي يمكن البحث فيه",
    },
    "UI_CAP01_NEXT_STEPS_V1_SEARCH_LABEL": {
        "en": "Generic search terms (in English)",
        "ar": "مصطلحات بحث عامة (بالإنجليزية)",
    },
    "UI_CAP01_NEXT_STEPS_V1_MEASURE_LABEL": {
        "en": "What could be measured, checked or documented",
        "ar": "ما الذي يمكن قياسه أو فحصه أو توثيقه",
    },
    "UI_CAP01_NEXT_STEPS_V1_SPECIALIST_LABEL": {
        "en": "Specialist input:",
        "ar": "المدخلات المتخصصة:",
    },
    "UI_CAP01_NEXT_STEPS_V1_BOUNDARY": {
        "en": "These next steps are navigation aids for this gap only. InventorAI has not determined that any topic or category applies to your design, retrieves nothing, and sets no value, range, threshold or pass / fail criterion. They add no question, action, responsibility or closure rule — the gap action packs and the Validation Plan keep those — and they do not plan a test: your own experiment planning stays in the Prototype & Test Plan.",
        "ar": "هذه الخطوات التالية أدوات إرشاد لهذه الفجوة فقط. لم يحدد InventorAI أن أي موضوع أو فئة ينطبق على تصميمك، ولا يسترجع أي شيء، ولا يضع أي قيمة أو نطاق أو حدّ أو معيار نجاح / فشل. ولا تضيف سؤالًا ولا إجراءً ولا مسؤولية ولا شرط إغلاق — فهذه تبقى لحِزم إجراءات الفجوات ولخطة التحقق (Validation Plan) — ولا تخطط لاختبار: يبقى تخطيطك لتجاربك في خطة النموذج الأولي والاختبار.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_MISSING": {
        "en": "The questions for this gap ask for the physical steps the mechanism takes, what moves, connects or transfers force, each component and how it contributes, and any physical detail still missing for someone to build it.",
        "ar": "تسأل أسئلة هذه الفجوة عن الخطوات الفيزيائية التي تتخذها الآلية، وما الذي يتحرك أو يتصل أو ينقل القوة، وكل مكوّن وكيف يساهم، وأي تفصيل فيزيائي لا يزال ناقصًا ليتمكن شخص من بنائها.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_TOPIC_1": {
        "en": "The sequence of physical steps from the input motion or force to the intended function.",
        "ar": "تسلسل الخطوات الفيزيائية من الحركة أو القوة الداخلة إلى الوظيفة المقصودة.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_TOPIC_2": {
        "en": "The force-transfer path: which parts move, connect or pass force to the next part.",
        "ar": "مسار نقل القوة: أي الأجزاء تتحرك أو تتصل أو تنقل القوة إلى الجزء التالي.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_TOPIC_3": {
        "en": "The role of each mechanical component in the overall motion or function.",
        "ar": "دور كل مكوّن ميكانيكي في الحركة أو الوظيفة الكلية.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_SEARCH_1": {
        "en": "mechanism motion sequence",
        "ar": "mechanism motion sequence",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_SEARCH_2": {
        "en": "force transfer path",
        "ar": "force transfer path",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_SEARCH_3": {
        "en": "mechanical component function",
        "ar": "mechanical component function",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_MEASURE_1": {
        "en": "A step-by-step description or sketch of the mechanism showing each component and how motion or force passes between them.",
        "ar": "وصف خطوة بخطوة أو رسم تخطيطي للآلية يُظهر كل مكوّن وكيف تنتقل الحركة أو القوة بينها.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_MEASURE_2": {
        "en": "An observation record of how the mechanism, or a simple model of it, moves through those steps.",
        "ar": "سجل ملاحظة لكيفية تحرك الآلية، أو نموذج بسيط منها، عبر تلك الخطوات.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_MEASURE_3": {
        "en": "A note of any physical detail that is still missing for someone to build the mechanism.",
        "ar": "ملاحظة بأي تفصيل فيزيائي لا يزال ناقصًا ليتمكن شخص من بناء الآلية.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_SPECIALIST": {
        "en": "InventorAI does not name a specialist category for this gap: no governed mapping supports one from this guidance alone.",
        "ar": "لا يسمّي InventorAI فئة مختصين لهذه الفجوة: لا يوجد ربط خاضع للحوكمة يدعم ذلك من هذا الإرشاد وحده.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_MISSING": {
        "en": "The questions for this gap ask which physical principle the mechanism relies on, and which material or force constraints it must operate within.",
        "ar": "تسأل أسئلة هذه الفجوة عن المبدأ الفيزيائي الذي تعتمد عليه الآلية، وعن قيود المواد أو القوى التي يجب أن تعمل ضمنها.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_TOPIC_1": {
        "en": "The physical principle the mechanism relies on, such as leverage, spring tension, gear ratio or friction.",
        "ar": "المبدأ الفيزيائي الذي تعتمد عليه الآلية، مثل الرافعة أو شدّ النابض أو نسبة التروس أو الاحتكاك.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_TOPIC_2": {
        "en": "The operating constraints: the forces the mechanism must produce or withstand and the material constraints it depends on.",
        "ar": "قيود التشغيل: القوى التي يجب أن تُنتجها الآلية أو تتحملها، وقيود المواد التي تعتمد عليها.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_TOPIC_3": {
        "en": "Where they match your actual mechanism, the reference fundamentals above for torque / moment, static moment balance and pressure / force / area.",
        "ar": "حيث تطابق آليتك الفعلية، الأساسيات المرجعية أعلاه للعزم، واتزان العزوم الساكن، والضغط / القوة / المساحة.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_1": {
        "en": "leverage principle",
        "ar": "leverage principle",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_2": {
        "en": "spring tension",
        "ar": "spring tension",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_3": {
        "en": "gear ratio",
        "ar": "gear ratio",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_4": {
        "en": "friction force",
        "ar": "friction force",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_5": {
        "en": "torque moment arm",
        "ar": "torque moment arm",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_6": {
        "en": "pressure force area",
        "ar": "pressure force area",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_MEASURE_1": {
        "en": "A statement of the forces the mechanism must produce or withstand under its intended use conditions.",
        "ar": "بيان بالقوى التي يجب أن تُنتجها الآلية أو تتحملها في ظروف الاستخدام المقصودة.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_MEASURE_2": {
        "en": "Measured or documented force, torque or pressure quantities relevant to the stated principle, recorded with their units.",
        "ar": "كميات قوة أو عزم أو ضغط مقيسة أو موثّقة ذات صلة بالمبدأ المذكور، مسجّلة مع وحداتها.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_MEASURE_3": {
        "en": "Documentation of the material or force constraints the mechanism depends on, noting where each came from.",
        "ar": "توثيق لقيود المواد أو القوى التي تعتمد عليها الآلية، مع ذكر مصدر كل منها.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_MEASURE_4": {
        "en": "Observation evidence of real-world loads, wear or environmental conditions, where you have it.",
        "ar": "أدلة ملاحظة عن الأحمال الواقعية أو التآكل أو الظروف البيئية، حيثما توفرت لديك.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SPECIALIST": {
        "en": "InventorAI does not name a specialist category for this gap: no governed mapping supports one from this guidance alone. If specialist input has already been requested for this gap's operating limits, that request appears in this gap's action pack; this guidance does not change it or identify which specialist.",
        "ar": "لا يسمّي InventorAI فئة مختصين لهذه الفجوة: لا يوجد ربط خاضع للحوكمة يدعم ذلك من هذا الإرشاد وحده. وإذا كانت مدخلات متخصصة قد طُلبت بالفعل لحدود التشغيل في هذه الفجوة، فإن هذا الطلب يظهر في حزمة إجراءات هذه الفجوة؛ ولا يغيّره هذا الإرشاد ولا يحدد المختص.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_MISSING": {
        "en": "The questions for this gap ask what the mechanism does not do or cover, at least one clear mechanical boundary, one similar existing mechanical approach, and what makes yours different in a concrete, physical way.",
        "ar": "تسأل أسئلة هذه الفجوة عمّا لا تفعله الآلية أو لا تغطيه، وعن حدّ ميكانيكي واضح واحد على الأقل، وعن نهج ميكانيكي قائم مشابه، وعمّا يجعل آليتك مختلفة بطريقة فيزيائية ملموسة.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_TOPIC_1": {
        "en": "The scope of the mechanism: what it does and does not do or cover.",
        "ar": "نطاق الآلية: ما تفعله وما لا تفعله أو لا تغطيه.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_TOPIC_2": {
        "en": "Its mechanical boundary: where the mechanism ends and another part or system begins.",
        "ar": "حدّها الميكانيكي: أين تنتهي الآلية ويبدأ جزء أو نظام آخر.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_TOPIC_3": {
        "en": "An existing mechanical approach similar to yours, and the concrete physical way yours differs.",
        "ar": "نهج ميكانيكي قائم مشابه لآليتك، والطريقة الفيزيائية الملموسة التي تختلف بها آليتك.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_SEARCH_1": {
        "en": "mechanism scope boundary",
        "ar": "mechanism scope boundary",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_SEARCH_2": {
        "en": "system boundary definition",
        "ar": "system boundary definition",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_SEARCH_3": {
        "en": "existing mechanism comparison",
        "ar": "existing mechanism comparison",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_MEASURE_1": {
        "en": "A written scope statement listing what the mechanism does and does not do or cover.",
        "ar": "بيان نطاق مكتوب يذكر ما تفعله الآلية وما لا تفعله أو لا تغطيه.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_MEASURE_2": {
        "en": "A sketch or description marking where the mechanism ends and what lies outside it.",
        "ar": "رسم تخطيطي أو وصف يحدد أين تنتهي الآلية وما يقع خارجها.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_MEASURE_3": {
        "en": "A side-by-side description of one similar existing mechanical approach and the concrete physical difference of yours, as your own concept-level statement — not a novelty or patentability assessment.",
        "ar": "وصف متقابل لنهج ميكانيكي قائم مشابه وللاختلاف الفيزيائي الملموس في آليتك، بوصفه بيانك أنت على المستوى المفاهيمي — وليس تقييمًا للجِدّة أو لقابلية الحماية ببراءة اختراع.",
    },
    "UI_CAP01_MECHANICAL_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_SPECIALIST": {
        "en": "InventorAI does not name a specialist category for this gap: no governed mapping supports one from this guidance alone.",
        "ar": "لا يسمّي InventorAI فئة مختصين لهذه الفجوة: لا يوجد ربط خاضع للحوكمة يدعم ذلك من هذا الإرشاد وحده.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_MISSING": {
        "en": "The questions for this gap ask what happens electrically from input to output, which components are central and what role each plays, what signal or energy transformation the circuit performs, and which part is most critical and why.",
        "ar": "تسأل أسئلة هذه الفجوة عمّا يحدث كهربائيًا من المدخل إلى المخرج، وعن المكوّنات المحورية ودور كل منها، وعن تحويل الإشارة أو الطاقة الذي تؤديه الدائرة، وعن الجزء الأكثر أهمية ولماذا.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_TOPIC_1": {
        "en": "The circuit's input-to-output function: what happens electrically from input to output.",
        "ar": "وظيفة الدائرة من المدخل إلى المخرج: ما الذي يحدث كهربائيًا من المدخل إلى المخرج.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_TOPIC_2": {
        "en": "The signal or energy transformation the circuit performs.",
        "ar": "تحويل الإشارة أو الطاقة الذي تؤديه الدائرة.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_TOPIC_3": {
        "en": "The role of each central component, described by its underlying principle rather than only by a platform or product name.",
        "ar": "دور كل مكوّن محوري، موصوفًا بمبدئه الأساسي لا باسم منصة أو منتج فقط.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_SEARCH_1": {
        "en": "circuit input output function",
        "ar": "circuit input output function",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_SEARCH_2": {
        "en": "signal transformation circuit",
        "ar": "signal transformation circuit",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_SEARCH_3": {
        "en": "electronic component role",
        "ar": "electronic component role",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_MEASURE_1": {
        "en": "A block description or simple diagram of the circuit from input to output, naming each central component and its role.",
        "ar": "وصف بالكتل أو مخطط بسيط للدائرة من المدخل إلى المخرج، يسمّي كل مكوّن محوري ودوره.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_MEASURE_2": {
        "en": "The technical documentation of each central component describing what it does.",
        "ar": "الوثائق الفنية لكل مكوّن محوري التي تصف ما يفعله.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_MEASURE_3": {
        "en": "A note of which part is most critical to the intended function, and why.",
        "ar": "ملاحظة بالجزء الأكثر أهمية لتحقيق الوظيفة المقصودة، ولماذا.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_MECHANISM_COMPLETENESS_SPECIALIST": {
        "en": "InventorAI does not name a specialist category for this gap: no governed mapping supports one from this guidance alone.",
        "ar": "لا يسمّي InventorAI فئة مختصين لهذه الفجوة: لا يوجد ربط خاضع للحوكمة يدعم ذلك من هذا الإرشاد وحده.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_MISSING": {
        "en": "The questions for this gap ask what provides the energy or power, which electrical requirements the design depends on — such as voltage, current or frequency — and which electrical constraints it must stay within.",
        "ar": "تسأل أسئلة هذه الفجوة عمّا يوفّر الطاقة أو القدرة، وعن المتطلبات الكهربائية التي يعتمد عليها التصميم — مثل الجهد أو التيار أو التردد — وعن القيود الكهربائية التي يجب أن يبقى ضمنها.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_TOPIC_1": {
        "en": "The power or energy source the design relies on, and its energy budget where energy is converted or delivered.",
        "ar": "مصدر القدرة أو الطاقة الذي يعتمد عليه التصميم، وميزانية الطاقة حيث تُحوَّل الطاقة أو تُوصَّل.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_TOPIC_2": {
        "en": "The electrical requirements the design depends on, such as voltage, current or frequency.",
        "ar": "المتطلبات الكهربائية التي يعتمد عليها التصميم، مثل الجهد أو التيار أو التردد.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_TOPIC_3": {
        "en": "The electrical constraints the design must stay within to function, and where the information to determine them would come from.",
        "ar": "القيود الكهربائية التي يجب أن يبقى التصميم ضمنها ليعمل، ومن أين ستأتي المعلومات اللازمة لتحديدها.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_TOPIC_4": {
        "en": "Where they match your actual circuit, the reference fundamentals above for Ohm's law, basic electrical power and SI units.",
        "ar": "حيث تطابق دائرتك الفعلية، الأساسيات المرجعية أعلاه لقانون أوم، والقدرة الكهربائية الأساسية، ووحدات النظام الدولي (SI).",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_1": {
        "en": "power source energy budget",
        "ar": "power source energy budget",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_2": {
        "en": "operating voltage current requirements",
        "ar": "operating voltage current requirements",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_3": {
        "en": "electrical operating constraints",
        "ar": "electrical operating constraints",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_4": {
        "en": "Ohm's law",
        "ar": "Ohm's law",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SEARCH_5": {
        "en": "electrical power voltage current",
        "ar": "electrical power voltage current",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_MEASURE_1": {
        "en": "A statement of the power or energy source and the energy budget the design needs, where energy is converted or delivered.",
        "ar": "بيان بمصدر القدرة أو الطاقة وميزانية الطاقة التي يحتاجها التصميم، حيث تُحوَّل الطاقة أو تُوصَّل.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_MEASURE_2": {
        "en": "Measured or documented voltage, current or frequency quantities the design depends on, recorded with their units.",
        "ar": "كميات جهد أو تيار أو تردد مقيسة أو موثّقة يعتمد عليها التصميم، مسجّلة مع وحداتها.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_MEASURE_3": {
        "en": "Documentation of the electrical constraints the design must stay within, such as the technical documentation of the components or power source involved, noting where each came from.",
        "ar": "توثيق للقيود الكهربائية التي يجب أن يبقى التصميم ضمنها، مثل الوثائق الفنية للمكوّنات أو لمصدر القدرة المعنيّ، مع ذكر مصدر كل منها.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_PHYSICAL_FEASIBILITY_SPECIALIST": {
        "en": "InventorAI does not name a specialist category for this gap: no governed mapping supports one from this guidance alone.",
        "ar": "لا يسمّي InventorAI فئة مختصين لهذه الفجوة: لا يوجد ربط خاضع للحوكمة يدعم ذلك من هذا الإرشاد وحده.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_MISSING": {
        "en": "The questions for this gap ask what the design does not do or handle, where it stops and another system or component begins, and which external systems, components or interfaces it depends on.",
        "ar": "تسأل أسئلة هذه الفجوة عمّا لا يفعله التصميم أو لا يتعامل معه، وعن النقطة التي يتوقف عندها ويبدأ نظام أو مكوّن آخر، وعن الأنظمة أو المكوّنات أو الواجهات الخارجية التي يعتمد عليها.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_TOPIC_1": {
        "en": "The scope of the electronic design: what it does and does not do or handle.",
        "ar": "نطاق التصميم الإلكتروني: ما يفعله وما لا يفعله أو لا يتعامل معه.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_TOPIC_2": {
        "en": "The interface boundary: where the design stops and another system or component begins.",
        "ar": "حدّ الواجهة: أين يتوقف التصميم ويبدأ نظام أو مكوّن آخر.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_TOPIC_3": {
        "en": "The external systems, components or interfaces the design depends on to function.",
        "ar": "الأنظمة أو المكوّنات أو الواجهات الخارجية التي يعتمد عليها التصميم ليعمل.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_SEARCH_1": {
        "en": "system boundary definition",
        "ar": "system boundary definition",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_SEARCH_2": {
        "en": "electronic interface description",
        "ar": "electronic interface description",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_SEARCH_3": {
        "en": "external interface dependency",
        "ar": "external interface dependency",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_MEASURE_1": {
        "en": "A written scope statement of what the design does and does not do or handle.",
        "ar": "بيان نطاق مكتوب بما يفعله التصميم وما لا يفعله أو لا يتعامل معه.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_MEASURE_2": {
        "en": "A boundary sketch or description marking where the design stops and each external system or component begins.",
        "ar": "رسم تخطيطي أو وصف للحدود يحدد أين يتوقف التصميم ويبدأ كل نظام أو مكوّن خارجي.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_MEASURE_3": {
        "en": "Interface information for each external system, component or interface the design depends on, such as its technical documentation.",
        "ar": "معلومات الواجهة لكل نظام أو مكوّن أو واجهة خارجية يعتمد عليها التصميم، مثل وثائقها الفنية.",
    },
    "UI_CAP01_ELECTRONICS_NEXT_STEPS_V1_BOUNDARY_AMBIGUITY_SPECIALIST": {
        "en": "InventorAI does not name a specialist category for this gap: no governed mapping supports one from this guidance alone.",
        "ar": "لا يسمّي InventorAI فئة مختصين لهذه الفجوة: لا يوجد ربط خاضع للحوكمة يدعم ذلك من هذا الإرشاد وحده.",
    },
}


# T2-B' — the ONE projection from a committed question identity to its approved
# display copy. Presentation-only: it stores no content of its own, is never
# persisted, and is consulted only after the identity has been resolved from
# canonical state and confirmed against the committed WS10 registry. A question
# identity that is absent here renders NO explanation (fail closed).
QUESTION_EXPLANATION_KEYS = {
    "N-MC-1": "UI_T2B_WHY_N_MC_1",
    "N-MC-2": "UI_T2B_WHY_N_MC_2",
    "N-MC-3": "UI_T2B_WHY_N_MC_3",
    "N-MC-4": "UI_T2B_WHY_N_MC_4",
    "N-PF-1": "UI_T2B_WHY_N_PF_1",
    "N-PF-2": "UI_T2B_WHY_N_PF_2",
    "N-PF-3": "UI_T2B_WHY_N_PF_3",
    "N-PF-4": "UI_T2B_WHY_N_PF_4",
    "N-BA-1": "UI_T2B_WHY_N_BA_1",
    "N-BA-2": "UI_T2B_WHY_N_BA_2",
    "N-BA-3": "UI_T2B_WHY_N_BA_3",
    "mechanical:MECHANISM_COMPLETENESS:Q1":
        "UI_T2B_WHY_MECHANICAL_MECHANISM_COMPLETENESS_Q1",
    "mechanical:MECHANISM_COMPLETENESS:Q2":
        "UI_T2B_WHY_MECHANICAL_MECHANISM_COMPLETENESS_Q2",
    "mechanical:MECHANISM_COMPLETENESS:Q3":
        "UI_T2B_WHY_MECHANICAL_MECHANISM_COMPLETENESS_Q3",
    "mechanical:MECHANISM_COMPLETENESS:Q4":
        "UI_T2B_WHY_MECHANICAL_MECHANISM_COMPLETENESS_Q4",
    "mechanical:PHYSICAL_FEASIBILITY:Q1":
        "UI_T2B_WHY_MECHANICAL_PHYSICAL_FEASIBILITY_Q1",
    "mechanical:PHYSICAL_FEASIBILITY:Q2":
        "UI_T2B_WHY_MECHANICAL_PHYSICAL_FEASIBILITY_Q2",
    "mechanical:BOUNDARY_AMBIGUITY:Q1":
        "UI_T2B_WHY_MECHANICAL_BOUNDARY_AMBIGUITY_Q1",
    "mechanical:BOUNDARY_AMBIGUITY:Q2":
        "UI_T2B_WHY_MECHANICAL_BOUNDARY_AMBIGUITY_Q2",
    "mechanical:BOUNDARY_AMBIGUITY:Q3":
        "UI_T2B_WHY_MECHANICAL_BOUNDARY_AMBIGUITY_Q3",
    "mechanical:BOUNDARY_AMBIGUITY:Q4":
        "UI_T2B_WHY_MECHANICAL_BOUNDARY_AMBIGUITY_Q4",
}


# --- D-P6-18 final UI-chrome boundary: EXACT English->Arabic map for the
# deterministic guidance/criticality chrome (source English lives in the guidance
# modules; this maps it at the presentation boundary via localize_deep). Actual
# questions, the criticality clarification ask, and user content are deliberately
# ABSENT. Populated below; kept as the single owner-approved Arabic registry.
_DEEP_AR = {
    # --- Stage 15 Slice 2 interaction-declaration acknowledgement (web.app) ---
    "Saved. You recorded how these two parts interact. This declaration has "
    "not been validated, and compatibility between the parts has not been "
    "assessed. One preparation step was added to your Validation Plan.":
        "تم الحفظ. سجّلتَ كيف يتفاعل هذان الجزآن. هذا الإعلان غير مُتحقَّق منه، "
        "ولم يُقيَّم التوافق بين الجزأين. وأُضيفت خطوة تحضير واحدة إلى خطة "
        "التحقق (Validation Plan).",
    # --- Stage 20 closure assumption-action acknowledgements (web.app) ---
    'Saved. Your provisional assumption was revised, and the earlier wording is kept in your project history. It is still a provisional assumption and has not been validated.':
        'تم الحفظ. عُدِّل افتراضك المؤقت، والصياغة السابقة محفوظة في سجل مشروعك. لا يزال افتراضًا مؤقتًا ولم يُتحقَّق منه.',
    'Saved. Your provisional assumption was replaced by your answer, and the assumption is kept in your project history. Everything shown has been recomputed. Your answer has not been validated.':
        'تم الحفظ. استُبدل افتراضك المؤقت بإجابتك، والافتراض محفوظ في سجل مشروعك. أُعيد حساب كل ما يظهر هنا. لم يُتحقَّق من إجابتك.',
    'Replacement recorded. This answer was not replayed for progression because its historical question/area was not currently eligible. It remains unvalidated.':
        'سُجّل الاستبدال. لم تُعَد معالجة هذه الإجابة للتقدّم لأن سؤالها أو مجالها التاريخي لم يكن مؤهلًا حاليًا. ولا تزال غير مُتحقَّق منها.',
    'Your replacement is already recorded in your project. It has not been validated.':
        'استبدالك مسجّل بالفعل في مشروعك. ولم يُتحقَّق منه.',
    # --- CAP-08 Slice 1 dependency-declaration acknowledgement (web.app) ---
    "Saved. You declared that these recorded answers depend on this "
    "provisional assumption. This dependency has not been validated.":
        "تم الحفظ. أعلنتَ أن هذه الإجابات المسجّلة تعتمد على هذا الافتراض "
        "المؤقت. هذا الاعتماد غير مُتحقَّق منه.",
    # --- CAP-10 Slice 1 conflict-declaration acknowledgement (web.app) ---
    "Saved. You believe these two recorded answers conflict. This declaration "
    "has not been validated, and neither answer is assumed correct.":
        "تم الحفظ. أنت ترى أن هاتين الإجابتين المسجّلتين متعارضتان. هذا الإعلان "
        "غير مُتحقَّق منه، ولا تُفترض صحة أيٍّ من الإجابتين.",
    # --- W2-A decision-capture acknowledgement (web.app constant) ---
    "Your decision entry was recorded and saved to your project.":
        "تم تسجيل إدخالك القراري وحفظه في مشروعك.",
    # --- RVR-1 accepted-risk acknowledgement / failure (web.app constants) ---
    "Recorded as an accepted risk. This gap is explicitly accepted by you as "
    "a known, unresolved risk - it is NOT resolved and NOT validated, and it "
    "stays visible in your assessment.":
        "تم التسجيل كمخاطرة مقبولة. هذه الفجوة مقبولة منك صراحةً كمخاطرة معروفة "
        "غير محسومة — وهي غير محلولة وغير مُتحقق منها، وستبقى ظاهرة في تقييمك.",
    # --- 4.5 clarification_labels.py (_CLARIFICATION / _FALLBACK) ---
    "What this question is asking": "ما الذي يسأل عنه هذا السؤال",
    "This is asking you to walk through how your idea works from start to finish — what happens first, what happens next, and how those steps lead to the result you want.": "هذا يطلب منك أن تستعرض كيف تعمل فكرتك من البداية إلى النهاية — ما الذي يحدث أولًا، وما الذي يحدث بعده، وكيف تؤدّي تلك الخطوات إلى النتيجة التي تريدها.",
    "A step-by-step description, in your own words, of how the idea turns its starting point into the outcome.": "وصف خطوة بخطوة، بكلماتك الخاصة، لكيفية تحويل الفكرة نقطة انطلاقها إلى النتيجة.",
    "A few plain sentences describing the sequence of steps. Everyday language is fine; exact technical figures are not required.": "بضع جُمل بسيطة تصف تسلسل الخطوات. اللغة اليومية كافية؛ الأرقام التقنية الدقيقة ليست مطلوبة.",
    "If part of the chain is still unclear, you can describe the parts you know and mark the rest as not yet known.": "إذا كان جزء من السلسلة ما زال غير واضح، يمكنك وصف الأجزاء التي تعرفها ووضع علامة على الباقي بأنه غير معروف بعد.",
    "This is asking you to describe the edges of your idea — what it is meant to cover, and what it deliberately leaves out.": "هذا يطلب منك وصف حدود فكرتك — ما الذي يُفترض أن تغطّيه، وما الذي تتركه عمدًا خارجها.",
    "What problem it handles, who it is for, and where it stops or does not apply.": "ما المشكلة التي تتناولها، ولمن هي، وأين تتوقّف أو لا تنطبق.",
    "A short description of what is inside and outside the idea's scope. No legal or patent wording is needed.": "وصف قصير لما هو داخل نطاق الفكرة وما هو خارجه. لا حاجة إلى صياغة قانونية أو خاصة ببراءات الاختراع.",
    "If a boundary is still undecided, you can say so rather than guessing.": "إذا كان أحد الحدود لم يُحسم بعد، يمكنك قول ذلك بدلًا من التخمين.",
    "This is asking which things you are currently taking for granted about your idea that you have not yet checked.": "هذا يسأل عن الأمور التي تعدّها حاليًا من المسلَّمات بشأن فكرتك ولم تتحقق منها بعد.",
    "Conditions, materials, or behaviors you expect to hold true but have not confirmed.": "الظروف أو المواد أو السلوكيات التي تتوقّع صحّتها لكن لم تؤكّدها.",
    "A short list of things you are assuming, in plain words, and which ones would matter most if they turned out to be wrong.": "قائمة قصيرة بالأمور التي تفترضها، بكلمات بسيطة، وأيّها سيكون الأهم لو تبيّن خطؤه.",
    "Listing an assumption does not commit you to it; it just records what still needs checking.": "ذكر افتراض لا يُلزمك به؛ إنه فقط يسجّل ما لا يزال يحتاج إلى تحقّق.",
    "This is asking you to describe the problem on its own, and then how your idea is meant to address it.": "هذا يطلب منك وصف المشكلة بمفردها، ثم كيف يُفترض أن تعالجها فكرتك.",
    "Who has the problem and why it matters, described separately from how your idea works, plus where the match might be weaker.": "من لديه المشكلة ولماذا تهمّ، موصوفة بمعزل عن كيفية عمل فكرتك، إضافة إلى المواضع التي قد يكون فيها التوافق أضعف.",
    "First describe the problem in plain language, then describe how you intend the idea to help. It is fine to leave the strength of that relationship as uncertain.": "صف المشكلة أولًا بلغة بسيطة، ثم صف كيف تنوي أن تساعد الفكرة. لا بأس بترك قوة تلك العلاقة غير مؤكّدة.",
    "You only need to describe the problem and your intent; you do not need to prove the fit yourself.": "يكفي أن تصف المشكلة ونيّتك؛ لست مضطرًا لإثبات التوافق بنفسك.",
    "This is asking what makes your idea actually work — the basic principle, components, or process behind it.": "هذا يسأل عمّا يجعل فكرتك تعمل فعليًا — المبدأ الأساسي أو المكوّنات أو العملية وراءها.",
    "The working principle in plain terms. Whether it truly holds may later need a measurement, test, or outside evidence.": "المبدأ العامل بعبارات بسيطة. أما صحّته فعلًا فقد تحتاج لاحقًا إلى قياس أو اختبار أو دليل خارجي.",
    "A plain description of the principle you expect to make it work. Exact measurements are not required here.": "وصف بسيط للمبدأ الذي تتوقّع أن يجعلها تعمل. القياسات الدقيقة ليست مطلوبة هنا.",
    "If confirming it would need a test or evidence you do not have, you can note that and continue.": "إذا كان تأكيده يحتاج إلى اختبار أو دليل لا تملكه، يمكنك تدوين ذلك والمتابعة.",
    "This is asking which areas of know-how someone would need to actually build your idea — not what you personally know.": "هذا يسأل عن مجالات الدراية التي سيحتاجها أحدهم لبناء فكرتك فعليًا — لا ما تعرفه أنت شخصيًا.",
    "The kinds of technical fields or skills the build would demand.": "أنواع المجالات أو المهارات التقنية التي سيتطلبها البناء.",
    "A short list of the areas of expertise involved. You do not need to have that expertise yourself.": "قائمة قصيرة بمجالات الخبرة المعنيّة. لست مضطرًا لامتلاك تلك الخبرة بنفسك.",
    "If a particular area clearly needs a specialist, you can note that and request specialist input rather than answering it.": "إذا كان مجال معيّن يحتاج بوضوح إلى متخصّص، يمكنك تدوين ذلك وطلب مدخلات متخصّص بدلًا من الإجابة عنه.",
    "This is asking you to describe this part of your idea in your own words.": "هذا يطلب منك وصف هذا الجزء من فكرتك بكلماتك الخاصة.",
    "Whatever you currently know about this part of the idea.": "كل ما تعرفه حاليًا عن هذا الجزء من الفكرة.",
    "A few plain sentences. It is fine to describe only what you know and mark the rest as not yet known.": "بضع جُمل بسيطة. لا بأس بوصف ما تعرفه فقط ووضع علامة على الباقي بأنه غير معروف بعد.",
    "You can answer with what you know or choose any of the available actions that truthfully reflects what you need next.": "يمكنك الإجابة بما تعرفه أو اختيار أي من الإجراءات المتاحة التي تعكس بصدق ما تحتاجه تاليًا.",

    # --- 4.6 scaffolding_guidance.py ---
    "What kind of detail to add": "أي نوع من التفاصيل يجب إضافته",
    "These are prompts to help you add detail. They do not change or grade your answer — you write it in your own words.": "هذه توجيهات تساعدك على إضافة التفاصيل. إنها لا تُغيّر إجابتك ولا تقيّمها — أنت تكتبها بكلماتك الخاصة.",
    "What physical part or mechanism does this use?": "ما الجزء المادي أو الآلية التي يستخدمها هذا؟",
    "What condition triggers the action?": "ما الشرط الذي يُطلق الإجراء؟",
    "What does the device sense or detect?": "ما الذي يستشعره الجهاز أو يكشفه؟",
    "What output or response happens?": "ما المخرَج أو الاستجابة التي تحدث؟",
    "What evidence or observation supports this?": "ما الدليل أو الملاحظة التي تدعم هذا؟",
    "What is in scope, and what does this deliberately NOT do?": "ما الداخل في النطاق، وما الذي لا يفعله هذا عمدًا؟",
    "Where are the limits or boundaries of where it applies?": "أين حدود أو تخوم انطباقه؟",
    "What operating conditions or assumptions does it depend on?": "ما ظروف التشغيل أو الافتراضات التي يعتمد عليها؟",
    "What edge cases or exceptions are handled?": "ما الحالات الحدّية أو الاستثناءات التي يُتعامل معها؟",
    "What evidence or observation supports these limits?": "ما الدليل أو الملاحظة التي تدعم هذه الحدود؟",
    "What physical limits or operating range does this work within?": "ما الحدود المادية أو نطاق التشغيل الذي يعمل هذا ضمنه؟",
    "What conditions or constraints must hold for it to work?": "ما الظروف أو القيود التي يجب أن تتحقق ليعمل؟",
    "What assumptions about the environment does it rely on?": "ما الافتراضات حول البيئة التي يعتمد عليها؟",
    "What could physically prevent it from working?": "ما الذي قد يمنعه ماديًا من العمل؟",
    "What evidence or observation supports that it can work?": "ما الدليل أو الملاحظة التي تدعم أنه يمكن أن يعمل؟",
    "Make the physical or functional chain more explicit: what condition is detected, what part responds, what happens next, and why that response produces the intended effect.": "اجعل السلسلة المادية أو الوظيفية أكثر وضوحًا: ما الشرط الذي يُكتشَف، وما الجزء الذي يستجيب، وما الذي يحدث بعد ذلك، ولماذا تُنتج تلك الاستجابة الأثر المقصود.",
    "Make the reason for the boundary more explicit: identify the technical limit, what falls outside the intended use, and why it is excluded.": "اجعل سبب الحدّ أكثر وضوحًا: حدّد القيد التقني، وما الذي يقع خارج الاستخدام المقصود، ولماذا هو مستبعَد.",
    "State the operating conditions, constraints, and dependencies more explicitly: what must hold, what may fail, and why.": "اذكر ظروف التشغيل والقيود والاعتماديات بشكل أكثر وضوحًا: ما الذي يجب أن يتحقق، وما الذي قد يفشل، ولماذا.",
    "Add the specific details requested for this area. Name the relevant items, state why each matters, and note anything that is still uncertain or would need specialist input.": "أضِف التفاصيل المحدّدة المطلوبة لهذا المجال. سمِّ العناصر ذات الصلة، واذكر لماذا يهم كل منها، ونوّه إلى ما لا يزال غير مؤكّد أو يحتاج إلى مدخلات متخصّص.",
    "Good — this answer was accepted and counts toward this point. The system needs one more specific answer about how it works before it can close, so add one more concrete detail — a part, a trigger condition, or what it senses.": "جيد — قُبِلت هذه الإجابة وتُحسب لصالح هذه النقطة. يحتاج النظام إلى إجابة محدّدة أخرى حول كيفية عمله قبل أن يُغلق، فأضِف تفصيلًا ملموسًا واحدًا آخر — جزءًا، أو شرط تشغيل، أو ما يستشعره.",
    "Good — this answer was accepted and counts toward this point. The system needs one more specific answer about scope or limits before it can close, so add one more concrete detail — what it does not do, or a condition where it stops applying.": "جيد — قُبِلت هذه الإجابة وتُحسب لصالح هذه النقطة. يحتاج النظام إلى إجابة محدّدة أخرى حول النطاق أو الحدود قبل أن يُغلق، فأضِف تفصيلًا ملموسًا واحدًا آخر — ما لا يفعله، أو شرطًا يتوقّف عنده عن الانطباق.",
    "Good — this answer was accepted and counts toward this point. The system needs one more specific answer about the physical limits or conditions before it can close, so add one more concrete detail — a constraint or operating range.": "جيد — قُبِلت هذه الإجابة وتُحسب لصالح هذه النقطة. يحتاج النظام إلى إجابة محدّدة أخرى حول الحدود أو الظروف المادية قبل أن يُغلق، فأضِف تفصيلًا ملموسًا واحدًا آخر — قيدًا أو نطاق تشغيل.",
    "Good — this answer was accepted and counts toward this point. The system needs one more specific answer on the same point before it can close, so add one more concrete detail.": "جيد — قُبِلت هذه الإجابة وتُحسب لصالح هذه النقطة. يحتاج النظام إلى إجابة محدّدة أخرى حول النقطة نفسها قبل أن يُغلق، فأضِف تفصيلًا ملموسًا واحدًا آخر.",
    "The idea is not fully described yet. Say what problem it solves and, in plain words, how it solves it.": "لم توصف الفكرة بالكامل بعد. اذكر ما المشكلة التي تحلّها، وبعبارات بسيطة، كيف تحلّها.",
    "This answer needs more detail. Add a specific point about the mechanism, the trigger condition, the operating boundary, or a supporting observation.": "تحتاج هذه الإجابة إلى مزيد من التفصيل. أضِف نقطة محدّدة حول الآلية، أو شرط الإطلاق، أو حدّ التشغيل، أو ملاحظة داعمة.",

    # --- 4.7 answer_coauthoring_prompts.py ---
    "Optional: what you could include in your answer": "اختياري: ما الذي يمكنك تضمينه في إجابتك",
    "These prompts are optional. You write your own answer in your own words — they are not a required format. This guidance is not validation, and it is not safety, compliance, patent, or engineering approval; it only helps you think through what details you might add.": "هذه التوجيهات اختيارية. أنت تكتب إجابتك بكلماتك الخاصة — وهي ليست صيغة إلزامية. هذا الإرشاد ليس تحققًا، وليس موافقة تتعلق بالسلامة أو الامتثال أو براءات الاختراع أو الهندسة؛ إنه فقط يساعدك على التفكير في التفاصيل التي قد تضيفها.",
    "The main parts or steps involved, in the order they happen.": "الأجزاء أو الخطوات الرئيسية المعنيّة، بالترتيب الذي تحدث به.",
    "What starts the process, and what it produces at the end.": "ما الذي يبدأ العملية، وما الذي تُنتجه في النهاية.",
    "What the idea senses, detects, or responds to, if anything.": "ما الذي تستشعره الفكرة أو تكشفه أو تستجيب له، إن وُجد.",
    "Anything you have observed that suggests it behaves this way.": "أي شيء لاحظته يشير إلى أنها تتصرف بهذه الطريقة.",
    "What the idea is meant to cover, and what it deliberately does not do.": "ما الذي يُفترض أن تغطّيه الفكرة، وما الذي لا تفعله عمدًا.",
    "Who or what it is for, and the situations where it applies.": "لمن أو لماذا هي، والمواقف التي تنطبق فيها.",
    "Conditions or limits where it would stop applying.": "الظروف أو الحدود التي تتوقّف عندها عن الانطباق.",
    "Any point where you are still deciding the boundary.": "أي نقطة ما زلت تحسم فيها الحدّ.",
    "Things you are currently taking for granted but have not checked.": "أمور تعدّها حاليًا من المسلَّمات لكن لم تتحقق منها.",
    "Which of those assumptions would matter most if they were wrong.": "أي تلك الافتراضات سيكون الأهم لو كان خاطئًا.",
    "Conditions, materials, or behaviors you expect to hold true.": "الظروف أو المواد أو السلوكيات التي تتوقّع ثباتها.",
    "Anything you already know still needs checking.": "أي شيء تعرف مسبقًا أنه لا يزال يحتاج إلى تحقّق.",
    "The problem on its own — who has it and why it matters.": "المشكلة بمفردها — من لديه ولماذا تهمّ.",
    "How you intend the idea to address that problem.": "كيف تنوي أن تعالج الفكرة تلك المشكلة.",
    "Where the match between problem and idea might be weaker.": "أين قد يكون التوافق بين المشكلة والفكرة أضعف.",
    "Anything you have seen that suggests the idea helps.": "أي شيء رأيته يشير إلى أن الفكرة تساعد.",
    "The basic working principle you expect makes it work.": "المبدأ العامل الأساسي الذي تتوقّع أنه يجعلها تعمل.",
    "The conditions or operating range it would need to work within.": "الظروف أو نطاق التشغيل الذي ستحتاج للعمل ضمنه.",
    "What could physically get in the way of it working.": "ما الذي قد يعترض ماديًا عملها.",
    "Any observation or test that speaks to whether it can work.": "أي ملاحظة أو اختبار يتعلق بإمكانية عملها.",
    "The kinds of technical skills or fields the build would involve.": "أنواع المهارات أو المجالات التقنية التي سينطوي عليها البناء.",
    "Which parts you could describe yourself, in plain words.": "أي الأجزاء يمكنك وصفها بنفسك، بكلمات بسيطة.",
    "Which parts clearly need a specialist's input.": "أي الأجزاء تحتاج بوضوح إلى مدخلات متخصّص.",
    "Anything you are unsure how to describe yet.": "أي شيء لست متأكدًا بعد من كيفية وصفه.",
    "What you currently know about this part of the idea, in your own words.": "ما تعرفه حاليًا عن هذا الجزء من الفكرة، بكلماتك الخاصة.",
    "The parts you are confident about, and the parts still uncertain.": "الأجزاء التي تثق بها، والأجزاء التي ما زالت غير مؤكّدة.",
    "Anything you have observed that is relevant.": "أي شيء لاحظته وله صلة.",
    "What you would still need to find out.": "ما الذي ستظل بحاجة إلى معرفته.",

    # --- 4.8 result_feedback.py ---
    "The current demo did not recognize enough explicit reasoning structure in your answer to move this area forward yet. Making the cause-and-effect relationship more explicit may help.": "لم يتعرّف العرض التوضيحي الحالي على بنية استدلال صريحة كافية في إجابتك لدفع هذا المجال قُدُمًا بعد. قد يساعد جعل علاقة السبب والنتيجة أكثر وضوحًا.",
    "You addressed part of this, but more detail is still needed.": "لقد تناولت جزءًا من هذا، لكن لا يزال يلزم مزيد من التفصيل.",
    "This point is supported well enough to move forward in the current demo flow.": "هذه النقطة مدعومة بما يكفي للمضي قدمًا في العرض التوضيحي الحالي.",
    "Your follow-up added enough reasoning to continue in the current demo flow.": "أضافت متابعتك استدلالًا كافيًا للمتابعة في العرض التوضيحي الحالي.",
    "This point is not established yet, so the idea cannot move forward on this item.": "هذه النقطة غير مثبتة بعد، لذا لا يمكن للفكرة المضي قدمًا في هذا العنصر.",
    "This point has reached the highest maturity level supported by the current MVP demo.": "بلغت هذه النقطة أعلى مستوى نضج يدعمه العرض التوضيحي الحالي للحد الأدنى من المنتج.",
    "An earlier required step needs to be addressed first before this can move forward.": "يلزم تناول خطوة سابقة مطلوبة أولًا قبل أن يمضي هذا قُدُمًا.",
    "This needs more reasoning or supporting detail before it can move forward.": "يحتاج هذا إلى مزيد من الاستدلال أو التفاصيل الداعمة قبل أن يمضي قُدُمًا.",
    # PVCG-R3-I (R3-C §8.1): the truthful not-addressed disclosure. Both
    # supported UI languages, through the existing localize_deep seam.
    "This answer was not recognized as responding to the question that was asked, so it did not move this point forward. Answering the question directly, in the words the question uses, is what the current demo can recognize.": "لم يتم التعرف على هذه الإجابة كردٍّ على السؤال المطروح، لذلك لم تُحرِّك هذه النقطة إلى الأمام. الإجابة عن السؤال مباشرةً، وبالكلمات التي يستخدمها السؤال، هي ما يستطيع العرض الحالي التعرف عليه.",
    "Your statement that this is not known yet has been saved with your project. It does not describe how the mechanism works, so this point has not moved forward. You can answer it later, or describe the part you do know.": "تم حفظ قولك إن هذا غير معروف بعد مع مشروعك. وهو لا يصف كيف تعمل الآلية، لذلك لم تتقدّم هذه النقطة. يمكنك الإجابة عنها لاحقًا، أو وصف الجزء الذي تعرفه.",
    "This point cannot move forward yet. Review the result details for the specific reason.": "لا يمكن لهذه النقطة المضي قدمًا بعد. راجِع تفاصيل النتيجة لمعرفة السبب المحدّد.",

    # --- 4.9 gap_labels.py GAP_LABELS (heading / guidance / stage_note) ---
    "Does your idea have a clear working principle?": "هل لفكرتك مبدأ عمل واضح؟",
    "Describe what makes your idea work — the components, materials, forces, or processes involved. Be as specific as you can about the mechanism, not just the goal.": "صف ما يجعل فكرتك تعمل — المكوّنات أو المواد أو القوى أو العمليات المعنيّة. كن محدّدًا قدر الإمكان بشأن الآلية، لا الهدف فحسب.",
    "Exploring feasibility": "استكشاف الجدوى",
    "What does your idea do — and what doesn't it do?": "ما الذي تفعله فكرتك — وما الذي لا تفعله؟",
    "Define the scope clearly: what problem it solves, who it's for, and where it stops. Clear boundaries help identify what is truly novel and what still needs development.": "حدّد النطاق بوضوح: ما المشكلة التي تحلّها، ولمن هي، وأين تتوقّف. الحدود الواضحة تساعد على تحديد ما هو مبتكَر حقًا وما لا يزال يحتاج إلى تطوير.",
    "Defining scope": "تحديد النطاق",
    "How does it work, step by step?": "كيف تعمل، خطوة بخطوة؟",
    "Walk through the operating mechanism — the causal chain from input to output. What happens at each stage? What converts, controls, or transforms the inputs into the desired result?": "استعرض آلية العمل — السلسلة السببية من المدخل إلى المخرج. ما الذي يحدث في كل مرحلة؟ ما الذي يحوّل المدخلات أو يتحكم بها أو يبدّلها إلى النتيجة المرجوّة؟",
    "Developing mechanism": "تطوير الآلية",
    "How does your idea address the problem?": "كيف تعالج فكرتك المشكلة؟",
    "Describe the problem on its own terms first — who experiences it and why it matters — without describing your idea. Then explain how your idea is intended to address that problem, and identify situations where the match may be weaker.": "صف المشكلة بشروطها الخاصة أولًا — من يعانيها ولماذا تهمّ — دون وصف فكرتك. ثم اشرح كيف يُقصد بفكرتك معالجة تلك المشكلة، وحدّد المواقف التي قد يكون التوافق فيها أضعف.",
    "Checking problem fit": "التحقق من ملاءمة المشكلة",
    "What are you assuming that hasn't been tested yet?": "ما الذي تفترضه ولم يُختبَر بعد؟",
    "List anything you are taking for granted about your idea that you have not yet verified — materials, conditions, or behaviors you expect to hold true. Then note which of these would be most serious if they turned out to be wrong.": "اذكر أي شيء تعدّه من المسلَّمات بشأن فكرتك ولم تتحقق منه بعد — مواد أو ظروف أو سلوكيات تتوقّع صحّتها. ثم نوّه إلى أيّها سيكون الأخطر لو تبيّن خطؤه.",
    "Surfacing assumptions": "إظهار الافتراضات",
    "What expertise would building this require?": "ما الخبرة التي سيتطلبها بناء هذا؟",
    "List the areas of technical knowledge someone would need to build your idea — not what you personally know, but what the implementation itself demands. Then identify which areas require specialist input.": "اذكر مجالات المعرفة التقنية التي سيحتاجها أحدهم لبناء فكرتك — لا ما تعرفه أنت شخصيًا، بل ما يتطلبه التنفيذ نفسه. ثم حدّد المجالات التي تحتاج إلى مدخلات متخصّص.",
    "Identifying expertise needs": "تحديد احتياجات الخبرة",
    "Tell us more about this aspect of your idea": "أخبرنا بالمزيد عن هذا الجانب من فكرتك",
    "Provide as much specific detail as you can. Concrete descriptions help more than general ones.": "قدّم أكبر قدر ممكن من التفاصيل المحدّدة. الأوصاف الملموسة تساعد أكثر من العامة.",
    "Exploring": "استكشاف",

    # --- 4.10 responsibility_labels.py (label + guidance) ---
    "You can answer this": "يمكنك الإجابة عن هذا",
    "You can answer this from your intended design or current understanding. Exact engineering values are not required.": "يمكنك الإجابة عن هذا من تصميمك المقصود أو فهمك الحالي. القيم الهندسية الدقيقة ليست مطلوبة.",
    "The system can help with this": "يمكن للنظام المساعدة في هذا",
    "The system can help examine this relationship. You may still mark what is uncertain.": "يمكن للنظام المساعدة في فحص هذه العلاقة. لا يزال بإمكانك وضع علامة على ما هو غير مؤكّد.",
    "Specialist input may help": "قد تساعد مدخلات متخصّص",
    "This usually needs input from a relevant technical specialist. You can request specialist input and continue.": "يحتاج هذا عادةً إلى مدخلات من متخصّص تقني معنيّ. يمكنك طلب مدخلات متخصّص والمتابعة.",
    "Evidence or a test may be needed": "قد يلزم دليل أو اختبار",
    "This usually needs a measurement, test, or external evidence. You can request evidence and continue.": "يحتاج هذا عادةً إلى قياس أو اختبار أو دليل خارجي. يمكنك طلب دليل والمتابعة.",
    "Who answers this is not yet clear": "من يجيب عن هذا غير واضح بعد",
    "It is not yet clear who should answer this. You can answer, defer, or mark it as unknown.": "ليس واضحًا بعد من ينبغي أن يجيب عن هذا. يمكنك الإجابة، أو التأجيل، أو وضع علامة عليه بأنه غير معروف.",

    # --- 4.12b PVCG-R4 correction acknowledgement (web/app.py correct_answer) ---
    # `show_session` renders `_interaction_ack` through `localize_deep`, NOT
    # through `localize_message`, so the correction ack MUST be registered here
    # as well as in `_MESSAGE_KEYS` — otherwise it reaches an Arabic reader in
    # English and the correction path is language-asymmetric at the ACTUAL
    # render path (PVCG-R4-C §13 E-1). Same seam the R3 D-4 disclosure lesson
    # identified: register in the map the render path really consults.
    ("Your earlier answer was withdrawn and kept in the project history. "
     "Everything shown has been recomputed from your remaining answers."):
        ("تم سحب إجابتك السابقة مع الاحتفاظ بها في سجل المشروع. "
         "وأُعيد حساب كل ما يظهر هنا من إجاباتك المتبقية."),

    # --- T2-A quantity acknowledgement (web/app.py record_requirement_quantity):
    # rendered through `_interaction_ack` -> localize_deep, so it lives HERE.
    ("Your quantity was recorded and saved to your project. It is kept as "
     "stated and has not been checked or verified."):
        ("تم تسجيل الكمية وحفظها في مشروعك. وهي محفوظة كما ذكرتها ولم تُفحص "
         "ولم يُتحقق منها."),
    "The proposed quantity was discarded. Nothing was saved.":
        "تم تجاهل الكمية المقترحة. لم يُحفظ أي شيء.",

    # --- 4.12 non-answer acknowledgements (web/app.py _NON_ANSWER_ACK) ---
    "Recorded that you do not know this yet. It is kept as an open unknown and does not resolve the question.": "تم تسجيل أنك لا تعرف هذا بعد. يُحفظ كأمر غير معروف مفتوح ولا يحلّ السؤال.",
    "Recorded as deferred. The question remains open and unresolved.": "تم التسجيل كمؤجَّل. يبقى السؤال مفتوحًا وغير محلول.",
    "Recorded as a provisional assumption (not verified). It does not resolve the question or count as evidence.": "تم التسجيل كافتراض مبدئي (غير مُتحقَّق منه). لا يحلّ السؤال ولا يُحتسب دليلًا.",
    "Recorded that specialist input is needed. No technical answer has been assumed.": "تم تسجيل أنه يلزم مدخلات متخصّص. لم يُفترَض أي إجابة تقنية.",
    "Recorded that evidence is needed. No evidence or result has been recorded.": "تم تسجيل أنه يلزم دليل. لم يُسجَّل أي دليل أو نتيجة.",

    # --- 4.13 criticality (web/app.py) + session.html correction/summary chrome ---
    "This is what I understood from your explanation:": "هذا ما فهمته من شرحك:",
    "The idea may not work without this": "قد لا تعمل الفكرة بدون هذا",
    "The idea would still work, but this adds important value": "ستظل الفكرة تعمل، لكن هذا يضيف قيمة مهمة",
    "This mainly improves or refines the idea": "هذا يحسّن الفكرة أو يصقلها بشكل أساسي",
    "I am not sure yet": "لست متأكدًا بعد",
    "Yes, that is correct": "نعم، هذا صحيح",
    "Change this part": "غيّر هذا الجزء",
    "Something is missing": "هناك شيء ناقص",
    "Decide later": "قرّر لاحقًا",
    "Tell me in your own words": "أخبرني بكلماتك الخاصة",
    "Describe what should change or what is missing, and it will be used to update the picture of your idea.": "صف ما ينبغي تغييره أو ما هو ناقص، وسيُستخدم لتحديث صورة فكرتك.",
    "Your reason, in your own words (already filled in from what you said — keep it or edit it):": "سببك، بكلماتك الخاصة (مملوء مسبقًا مما قلته — أبقِه أو عدّله):",
    "Save this": "احفظ هذا",
    "You said:": "لقد قلت:",
    "Is that correct?": "هل هذا صحيح؟",
}
