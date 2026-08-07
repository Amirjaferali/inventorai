# gap_labels.py
# Translation layer: internal gap type constants -> inventor-facing guidance.
# Drop into web/ directory. No engine changes required.

GAP_LABELS = {
    "PHYSICAL_FEASIBILITY": {
        "heading": "Does your idea have a clear working principle?",
        "guidance": (
            "Describe what makes your idea work — the components, materials, "
            "forces, or processes involved. Be as specific as you can about "
            "the mechanism, not just the goal."
        ),
        "stage_note": "Exploring feasibility",
    },
    "BOUNDARY_AMBIGUITY": {
        "heading": "What does your idea do — and what doesn't it do?",
        "guidance": (
            "Define the scope clearly: what problem it solves, who it's for, "
            "and where it stops. Clear boundaries help identify what is truly "
            "novel and what still needs development."
        ),
        "stage_note": "Defining scope",
    },
    "MECHANISM_COMPLETENESS": {
        "heading": "How does it work, step by step?",
        "guidance": (
            "Walk through the operating mechanism — the causal chain from "
            "input to output. What happens at each stage? What converts, "
            "controls, or transforms the inputs into the desired result?"
        ),
        "stage_note": "Developing mechanism",
    },
    "PROBLEM_MECHANISM_FIT": {
        "heading": "How does your idea address the problem?",
        "guidance": (
            "Describe the problem on its own terms first — who experiences it "
            "and why it matters — without describing your idea. Then explain how "
            "your idea is intended to address that problem, and identify situations "
            "where the match may be weaker."
        ),
        "stage_note": "Checking problem fit",
    },
    "ASSUMPTION_INVENTORY": {
        "heading": "What are you assuming that hasn't been tested yet?",
        "guidance": (
            "List anything you are taking for granted about your idea that you "
            "have not yet verified — materials, conditions, or behaviors you "
            "expect to hold true. Then note which of these would be most "
            "serious if they turned out to be wrong."
        ),
        "stage_note": "Surfacing assumptions",
    },
    "EXPERTISE_GAP_AWARENESS": {
        "heading": "What expertise would building this require?",
        "guidance": (
            "List the areas of technical knowledge someone would need to build "
            "your idea — not what you personally know, but what the implementation "
            "itself demands. Then identify which areas require specialist input."
        ),
        "stage_note": "Identifying expertise needs",
    },
    "__default__": {
        "heading": "Tell us more about this aspect of your idea",
        "guidance": (
            "Provide as much specific detail as you can. "
            "Concrete descriptions help more than general ones."
        ),
        "stage_note": "Exploring",
    },
}

MATURITY_LABELS = {
    0: {
        "label": "Getting started",
        "meaning": "Share your idea — what it does and the problem it addresses.",
    },
    1: {
        "label": "Problem established",
        "meaning": (
            "You have described the core problem and your idea's direction. "
            "Now let's develop the mechanism."
        ),
    },
    2: {
        "label": "Ready for structured review",
        "meaning": (
            "You have worked through the key questions. This is a good point "
            "to seek technical feedback from domain experts."
        ),
    },
}

SESSION_DISCLOSURE = (
    "This platform helps you structure your thinking through guided questions. "
    "It tracks how you have addressed key areas — external technical validation "
    "remains a separate step."
)

# --- D-P6-18 Global UI Language: Arabic variants for the Category-B labels that
# reach the session surface (maturity labels, the session disclosure, and the
# short gap display names). Presentation only; the internal ids, GAP_LABELS
# question framing (Category-D, stays English), engine, and state are unchanged.
# The English structures above remain the source of truth and default.
MATURITY_LABELS_AR = {
    0: {
        "label": "البدء",
        "meaning": "شارك فكرتك — ما الذي تفعله والمشكلة التي تعالجها.",
    },
    1: {
        "label": "تحديد المشكلة",
        "meaning": ("لقد وصفت المشكلة الجوهرية واتجاه فكرتك. لنطوّر الآن الآلية."),
    },
    2: {
        "label": "جاهز للمراجعة المنظَّمة",
        "meaning": ("لقد عملت على الأسئلة الأساسية. هذه نقطة مناسبة لالتماس "
                    "ملاحظات تقنية من خبراء المجال."),
    },
}

SESSION_DISCLOSURE_AR = (
    "تساعدك هذه المنصة على تنظيم تفكيرك عبر أسئلة موجَّهة. وهي تتتبّع كيف تناولت "
    "المجالات الأساسية — ويبقى التحقق التقني الخارجي خطوة منفصلة."
)


def get_gap_label(gap_type: str) -> dict:
    return GAP_LABELS.get(gap_type, GAP_LABELS["__default__"])


def get_maturity_label(level: int, lang: str = "en") -> dict:
    """Return the ``{"label", "meaning"}`` pair for a maturity level. English by
    default; the Arabic variant when ``lang == "ar"`` (D-P6-18). Backward
    compatible: existing single-arg callers still receive English."""
    if lang == "ar":
        return MATURITY_LABELS_AR.get(level, MATURITY_LABELS_AR[0])
    return MATURITY_LABELS.get(level, MATURITY_LABELS[0])


def get_session_disclosure(lang: str = "en") -> str:
    """The session-page disclosure sentence. English by default; Arabic when
    ``lang == "ar"`` (D-P6-18). ``SESSION_DISCLOSURE`` stays the English source."""
    return SESSION_DISCLOSURE_AR if lang == "ar" else SESSION_DISCLOSURE


# Presentation-only short names for the internal gap-type IDs. Used to translate
# the raw identifiers that leak into a few session-page surfaces (the Next
# Development Step "Reference:" line and acknowledged-unknown gap contexts).
# This changes display text only; internal IDs, state, and engine behavior are
# unchanged. Non-gap references (e.g. "rec_1", "maturity_level_0") pass through.
GAP_DISPLAY_NAMES = {
    "MECHANISM_COMPLETENESS": "Working mechanism",
    "PHYSICAL_FEASIBILITY": "Practical feasibility",
    "BOUNDARY_AMBIGUITY": "Scope and boundaries",
    "PROBLEM_MECHANISM_FIT": "Problem–solution fit",
    "ASSUMPTION_INVENTORY": "Untested assumptions",
    "EXPERTISE_GAP_AWARENESS": "Expertise needed",
}

# D-P6-18: Arabic variants of the short gap display names (Category B).
GAP_DISPLAY_NAMES_AR = {
    "MECHANISM_COMPLETENESS": "الآلية العاملة",
    "PHYSICAL_FEASIBILITY": "الجدوى العملية",
    "BOUNDARY_AMBIGUITY": "النطاق والحدود",
    "PROBLEM_MECHANISM_FIT": "ملاءمة الحل للمشكلة",
    "ASSUMPTION_INVENTORY": "الافتراضات غير المختبَرة",
    "EXPERTISE_GAP_AWARENESS": "الخبرة المطلوبة",
}


def _active_ui_lang():
    """Resolve the selected UI language from the current request's signed session,
    defaulting to English. Safe outside a request context (returns ``"en"``), so
    direct (non-Flask) callers and unit tests keep the English behaviour."""
    try:
        from flask import has_request_context, session as _flask_session
    except Exception:  # pragma: no cover - Flask always present in this app
        return "en"
    if not has_request_context():
        return "en"
    return "ar" if _flask_session.get("ui_lang") == "ar" else "en"


def friendly_gap_name(value):
    """Display-only translation of an internal gap-type ID to a short,
    inventor-friendly label, in the selected UI language (D-P6-18). Any value that
    is not a known gap ID (e.g. a record id like ``rec_1`` or ``maturity_level_0``,
    or None) is returned unchanged. English outside a request context."""
    if isinstance(value, str):
        if _active_ui_lang() == "ar" and value in GAP_DISPLAY_NAMES_AR:
            return GAP_DISPLAY_NAMES_AR[value]
        return GAP_DISPLAY_NAMES.get(value, value)
    return value
