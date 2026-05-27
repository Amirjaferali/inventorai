"""
tests/test_extract_json_contract.py
Behavioral contract for extract_json — captures current behavior before extraction.
Run: python3 tests/test_extract_json_contract.py
"""
import sys, os, json, re
sys.path.insert(0, '.')

def extract_json(text):
    if not text or not text.strip():
        return None, "none", "empty_response"
    try:
        return json.loads(text.strip()), "direct", ""
    except json.JSONDecodeError:
        pass
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence:
        try:
            return json.loads(fence.group(1).strip()), "fence_strip", ""
        except json.JSONDecodeError:
            pass
    brace = re.search(r"\{.*\}", text, re.DOTALL)
    if brace:
        try:
            return json.loads(brace.group(0).strip()), "brace_extract", ""
        except json.JSONDecodeError as e:
            return None, "brace_extract_failed", str(e)
    return None, "no_json_found", f"no JSON object in {len(text)}-char response"

FIXTURE_DIR = "tests/fixtures/malformed"
errors = []
passed = 0

print("=== extract_json contract tests ===")
for fname in sorted(os.listdir(FIXTURE_DIR)):
    if not fname.endswith(".json"):
        continue
    with open(f"{FIXTURE_DIR}/{fname}", encoding="utf-8") as f:
        fixture = json.load(f)

    name = fixture["name"]
    inp  = fixture["input"]
    exp_mode = fixture["expected_mode"]
    exp_has  = fixture["expected_has_json"]

    result, mode, err = extract_json(inp)
    has_json = result is not None

    ok = True
    if has_json != exp_has:
        errors.append(f"FAIL {name}: has_json expected={exp_has} got={has_json}")
        ok = False
    if exp_mode != "none" and mode != exp_mode:
        errors.append(f"FAIL {name}: mode expected={exp_mode} got={mode}")
        ok = False
    if ok:
        print(f"  PASS: {name} mode={mode}")
        passed += 1

print()
if errors:
    print(f"FAILURES ({len(errors)}):")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
else:
    print(f"ALL PASSED ({passed}/{passed})")
