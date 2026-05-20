"""
Domain Rules — lightweight electronics/electrical only.
MVP: 3 rules maximum per MVP_SCOPE_FREEZE.md
"""

ELECTRONICS_SIGNALS = [
    "circuit", "sensor", "voltage", "current", "resistor",
    "capacitor", "microcontroller", "arduino", "esp32",
    "wifi", "bluetooth", "iot", "pcb", "transistor",
    "كهربائي", "دائرة", "مستشعر", "جهد", "تيار",
    "ميكروكنترولر", "لوحة", "إلكترونيات"
]

def infer_domain(idea_text: str) -> str | None:
    text = idea_text.lower()
    for signal in ELECTRONICS_SIGNALS:
        if signal in text:
            return "electronics_electrical"
    return None

def get_active_rules(domain: str) -> list:
    if domain == "electronics_electrical":
        return [
            "PHYSICAL_PRINCIPLE_REQUIRED",
            "POWER_ACKNOWLEDGMENT_IF_ENERGY",
            "NO_PLATFORM_SPECIFIC_NAMING",
        ]
    return []
