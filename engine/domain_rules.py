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
    for signal in ELECTRONICS_SIGNALS:
        if signal in text:
            return "electronics_electrical"
    for signal in MECHANICAL_SIGNALS:
        if signal in text:
            return "mechanical"
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
    return []
