"""
Domain Rules — lightweight electronics/electrical only.
MVP: 3 rules maximum per MVP_SCOPE_FREEZE.md
"""

ELECTRONICS_SIGNALS = [
    "circuit", "sensor", "voltage", "current", "resistor",
    "capacitor", "microcontroller", "arduino", "esp32", "led",
    "wifi", "bluetooth", "iot", "pcb", "transistor",
    "كهربائي", "دائرة", "مستشعر", "جهد", "تيار",
    "ميكروكنترولر", "لوحة", "إلكترونيات"
]

MECHANICAL_SIGNALS = [
    "gear", "hinge", "spring", "clamp", "lever", "pulley",
    "bearing", "shaft", "linkage", "mechanism",
    "torque", "friction", "joint", "actuator", "piston",
    "valve", "bracket", "fastener", "locking",
]

def infer_domain(idea_text: str) -> str | None:
    text = idea_text.lower()
    scores = {
        "electronics_electrical": sum(1 for s in ELECTRONICS_SIGNALS if s in text),
        "mechanical":             sum(1 for s in MECHANICAL_SIGNALS if s in text),
        "medical_device":         sum(1 for s in MEDICAL_SIGNALS if s in text),
    }
    if max(scores.values()) == 0:
        return None
    # Tie-breaker priority: medical_device > electronics_electrical > mechanical
    priority = ["medical_device", "electronics_electrical", "mechanical"]
    best_score = max(scores.values())
    for domain in priority:
        if scores[domain] == best_score:
            return domain
    return None

def get_active_rules(domain: str) -> list:
    if domain == "electronics_electrical":
        return [
            "PHYSICAL_PRINCIPLE_REQUIRED",
            "POWER_ACKNOWLEDGMENT_IF_ENERGY",
            "NO_PLATFORM_SPECIFIC_NAMING",
        ]
    if domain == "mechanical":
        return [
            "MECHANISM_COMPLETENESS",
            "PHYSICAL_FEASIBILITY",
            "BOUNDARY_AMBIGUITY",
        ]
    if domain == "medical_device":
        return [
            "MECHANISM_COMPLETENESS",
            "PHYSICAL_FEASIBILITY",
            "BOUNDARY_AMBIGUITY",
        ]
    return []

# ------------------------------------
# Domain-specific question registry
# ------------------------------------

MECHANICAL_QUESTIONS = {
    "MECHANISM_COMPLETENESS": [
        "Describe the physical steps your mechanism takes to achieve its function. "
        "What moves, connects, or transfers force?",
        "What are the individual mechanical components and how does each one contribute "
        "to the overall motion or function?",
        "If someone tried to build your mechanism tomorrow with no further explanation, "
        "what physical detail would be missing?",
    ],
    "PHYSICAL_FEASIBILITY": [
        "What physical principle does your mechanism rely on? "
        "(e.g. leverage, spring tension, gear ratio, friction)",
        "What are the material or force constraints your mechanism must operate within?",
    ],
    "BOUNDARY_AMBIGUITY": [
        "What does your mechanism specifically NOT do or NOT cover? "
        "State at least one clear mechanical boundary.",
        "Name one existing mechanical approach similar to yours. "
        "What makes yours different in a concrete, physical way?",
    ],
}

_DOMAIN_QUESTIONS = {
    "mechanical": MECHANICAL_QUESTIONS,
}


MEDICAL_SIGNALS = [
    "implantable", "clinical_trial", "patient_monitoring", "diagnosis", "therapeutic",
    "implant", "wearable", "prosthetic", "surgical", "rehabilitation",
    "glucose", "insulin", "cardiac", "heart", "pulse", "blood",
    "monitoring", "biosensor", "catheter", "stent", "orthopedic",
    "neural", "retinal", "hearing", "respiratory", "drug delivery",
]

MEDICAL_QUESTIONS = {
    "MECHANISM_COMPLETENESS": [
        "Describe specifically how your medical device interacts with the body. "
        "What biological or physiological process does it target?",
        "What are the individual components of your device and what does each one do "
        "in contact with or proximity to the patient?",
        "If a clinician tried to use your device tomorrow with no further explanation, "
        "what critical detail about its mechanism would be missing?",
    ],
    "PHYSICAL_FEASIBILITY": [
        "What physical or biological principle does your device rely on? "
        "(e.g. electrical stimulation, optical sensing, mechanical compression)",
        "What are the biocompatibility or safety constraints your device must meet "
        "to operate safely in or on the human body?",
    ],
    "BOUNDARY_AMBIGUITY": [
        "What does your medical device specifically NOT diagnose, treat, or cover? "
        "State at least one clear clinical boundary.",
        "Name one existing medical device or approach similar to yours. "
        "What makes yours different in a specific, clinically meaningful way?",
    ],
}

_DOMAIN_QUESTIONS["medical_device"] = MEDICAL_QUESTIONS

def get_domain_question(domain: str, gap_type: str, iterations_open: int) -> str | None:
    """
    Return a domain-specific question for gap_type, or None to trigger generic fallback.
    Domain layer owns questions. Engine must not contain domain-specific question logic.
    """
    domain_bank = _DOMAIN_QUESTIONS.get(domain)
    if not domain_bank:
        return None
    variants = domain_bank.get(gap_type)
    if not variants:
        return None
    index = min(iterations_open, len(variants) - 1)
    return variants[index]
