import os
import sys

ANCHOR_FILE = "docs/governance/ILT-002_GOVERNANCE_ANCHOR.md"

REQUIRED_SECTIONS = [
    "BOOT ENFORCEMENT LAYER",
    "CORE RULE",
    "FORBIDDEN OPERATIONS",
    "AGENT BOOT REQUIREMENT",
]

REQUIRED_RULES = [
    "No global state reconstruction is allowed",
    "Only per-session evidence is valid",
    "Absence of evidence = UNKNOWN",
]


def main() -> int:
    if not os.path.exists(ANCHOR_FILE):
        print("❌ BOOT FAILED - governance anchor file not found")
        return 1

    with open(ANCHOR_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    missing_sections = [s for s in REQUIRED_SECTIONS if s not in content]
    missing_rules = [r for r in REQUIRED_RULES if r not in content]

    if missing_sections or missing_rules:
        print("❌ BOOT FAILED - governance anchor incomplete")

        if missing_sections:
            print("\nMissing sections:")
            for item in missing_sections:
                print("-", item)

        if missing_rules:
            print("\nMissing rules:")
            for item in missing_rules:
                print("-", item)

        return 1

    print("✅ BOOT OK - ILT-002 governance anchor loaded and complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
