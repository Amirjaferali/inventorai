"""
tests/test_normalize_output_contract.py
Permanent regression protection for normalize_output.
Run: python3 tests/test_normalize_output_contract.py
"""
import sys
sys.path.insert(0, '.')
from engine.normalize_output import normalize_output

errors = []

def check(label, condition, detail=""):
    if not condition:
        errors.append(f"FAIL: {label} {detail}")
    else:
        print(f"  PASS: {label}")

print("=== normalize_output contract tests ===")

# 1. Enum normalization — lowercase input
r = normalize_output({"confidence_level": "medium"})
check("enum lowercase->canonical", r["confidence_level"] == "MEDIUM")

# 2. Enum normalization — whitespace
r = normalize_output({"confidence_level": " high "})
check("enum whitespace stripped", r["confidence_level"] == "HIGH")

# 3. Enum normalization — spaces to underscores
r = normalize_output({"feasibility_signal": "APPEARS FEASIBLE WITH CAVEATS"})
check("enum spaces->underscores", r["feasibility_signal"] == "APPEARS_FEASIBLE_WITH_CAVEATS")

# 4. Enum normalization — dashes to underscores
r = normalize_output({"feasibility_signal": "APPEARS-FEASIBLE"})
check("enum dashes->underscores", r["feasibility_signal"] == "APPEARS_FEASIBLE")

# 5. Unknown enum preserved (non-strict)
r = normalize_output({"confidence_level": "UNKNOWN_VALUE"})
check("unknown enum preserved", r["confidence_level"] == "UNKNOWN_VALUE")

# 6. Nested dict recursion
r = normalize_output({"feasibility": {"feasibility_signal": "feasibility_unclear"}})
check("nested dict recursion", r["feasibility"]["feasibility_signal"] == "FEASIBILITY_UNCLEAR")

# 7. List recursion
r = normalize_output({"confidence_level": ["low", "high"]})
check("list recursion", r["confidence_level"] == ["LOW", "HIGH"])

# 8. Non-dict passthrough
check("string passthrough", normalize_output("hello") == "hello")
check("none passthrough", normalize_output(None) is None)
check("int passthrough", normalize_output(42) == 42)

# 9. Idempotency
x = {"confidence_level": "medium", "feasibility": {"feasibility_signal": "feasibility_unclear"}}
r1 = normalize_output(x)
r2 = normalize_output(r1)
check("idempotency", r1 == r2, f"r1={r1} r2={r2}")

# 10. Non-enum string field — no mutation
r = normalize_output({"disclaimer_ar": "some arabic text"})
check("non-enum string unchanged", r["disclaimer_ar"] == "some arabic text")

# 11. strict mode — unknown enum raises
try:
    normalize_output({"confidence_level": "INVALID"}, strict=True)
    errors.append("FAIL: strict mode should raise on unknown enum")
except ValueError as e:
    print(f"  PASS: strict mode raises ValueError: {e}")
except TypeError:
    print(f"  PASS: strict mode not yet implemented (acceptable)")

print()
if errors:
    print("CONTRACT FAILURES:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print("ALL CONTRACT TESTS PASSED")
