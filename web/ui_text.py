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
    ("Current working snapshot selected for this temporary session. It has not "
     "been permanently saved or approved."): "UI_B_DELIV_105",
}


def localize_message(english, lang):
    """Return the selected-language variant of a KNOWN English server message.
    Unknown/None text passes through unchanged (fail-open, never raises)."""
    if not isinstance(english, str):
        return english
    key = _MESSAGE_KEYS.get(english)
    return text(key, lang) if key else english


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
    "UI_B_SESSION_040": {
        "en": "That answer could not be saved just now. Please try again.",
        "ar": "تعذّر حفظ هذه الإجابة الآن. يرجى المحاولة مرة أخرى.",
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
