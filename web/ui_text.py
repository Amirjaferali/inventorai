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
    copy are intentionally excluded and remain English.
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
}


def localize_message(english, lang):
    """Return the selected-language variant of a KNOWN English server message.
    Unknown/None text passes through unchanged (fail-open, never raises)."""
    if not isinstance(english, str):
        return english
    key = _MESSAGE_KEYS.get(english)
    return text(key, lang) if key else english


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
# copy are deliberately absent.
UI_STRINGS = {
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
    "UI_B_START_024": {  # present-confirm, broadened (non-electronics) activation — domain-neutral
        # L10N-RH-01 Observation #3 remediation: first-person consent
        # affirmation (matching UI_B_START_030's register) rather than
        # prompt/instruction wording. Still domain-neutral (no Tier-1
        # translation) and truthful.
        "en": "I confirm that this idea belongs to the domain that was recognized for it.",
        "ar": "أؤكد أن هذه الفكرة تنتمي إلى المجال الذي تم التعرف عليه لها.",
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
    "UI_B_SC_001": {
        "en": "InventorAI — Define Success Criteria",
        "ar": "InventorAI — تحديد معايير النجاح",
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
    "UI_B_SC_004": {"en": "Save criteria", "ar": "حفظ المعايير"},
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
    "UI_A_MSG_REGISTER": {
        "en": "If the address can be used, verification instructions have been sent.",
        "ar": "إذا كان بالإمكان استخدام هذا العنوان، فسيتم إرسال تعليمات التحقق.",
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
    "UI_A_MSG_RECOVER": {
        "en": ("If that address matches an account, password-reset instructions "
               "have been sent."),
        "ar": ("إذا كان هذا العنوان مطابقًا لحساب، فقد أُرسلت تعليمات إعادة تعيين "
               "كلمة المرور."),
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
    "UI_A_MSG_RESEND": {
        "en": "If verification is still needed, a new verification message has been sent.",
        "ar": "إذا كان التحقق لا يزال مطلوبًا، فقد أُرسلت رسالة تحقق جديدة.",
    },
    "UI_A_SESSION_BANNER": {
        "en": "Project saved to your account.",
        "ar": "تم حفظ المشروع في حسابك.",
    },

    # --- session.html chrome (Category B) -------------------------------------
    "UI_B_SESSION_001": {"en": "Next Development Step", "ar": "خطوة التطوير التالية"},
    "UI_B_SESSION_002": {"en": "Do next:", "ar": "الخطوة التالية:"},
    "UI_B_SESSION_003": {"en": "Reference:", "ar": "المرجع:"},
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
    "UI_W2A_ERR_001": {
        "en": ("That decision entry could not be saved just now. "
               "Nothing was changed."),
        "ar": "تعذّر حفظ هذا الإدخال القراري الآن. لم يتغيّر أي شيء."},
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
    "UI_RVR5_CORRECT_BUTTON": {
        "en": "Withdraw and replace this answer",
        "ar": "سحب هذه الإجابة واستبدالها"},
    "UI_RVR5_WITHDRAWN_LABEL": {
        "en": "Corrected (withdrawn) answers kept in history",
        "ar": "إجابات مصحَّحة (مسحوبة) محفوظة في السجل"},
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
        "en": "Define or edit success criteria",
        "ar": "تحديد معايير النجاح أو تعديلها",
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
    "UI_TITLE_SUCCESS": {"en": "InventorAI — Define Success Criteria",
                         "ar": "InventorAI — تحديد معايير النجاح"},
    "UI_TITLE_DATA": {"en": "Data & Session information",
                      "ar": "معلومات البيانات والجلسة"},
}


# --- D-P6-18 final UI-chrome boundary: EXACT English->Arabic map for the
# deterministic guidance/criticality chrome (source English lives in the guidance
# modules; this maps it at the presentation boundary via localize_deep). Actual
# questions, the criticality clarification ask, and user content are deliberately
# ABSENT. Populated below; kept as the single owner-approved Arabic registry.
_DEEP_AR = {
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
