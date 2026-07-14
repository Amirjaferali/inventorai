"""WS6 evidence validator — deterministic, read-only, exit 2 on any failure.

File: docs/governance/evidence/workstream6_requirement_landscape_synthesis/
      validate_ws6_evidence.py
Purpose: machine-verify the committed WS6 evidence package: required files,
JSON parseability, BASE/HEAD repetition counts, exact disposition wordings,
metadata/HTML parity flags, criticality-split evidence, expected test totals
recorded in the regression record, and the presence of every known
limitation. Input contract: run from the repository root. Output contract:
prints one OK line per check and exits 0, or prints FAIL and exits 2.
Prohibited behaviors: modifies nothing; imports no production code.
"""
import json, os, sys

E = os.path.dirname(os.path.abspath(__file__))
def fail(m): print("FAIL: " + m); sys.exit(2)
def ok(m): print("OK: " + m)

REQUIRED = [
    "WS6_HEAD_IDENTITY.md", "WS6_BASE_HEAD_COMPARISON.md",
    "WS6_RED_GREEN_TEST_RECORD.md", "WS6_PROTECTED_REGRESSION_RECORD.md",
    "WS6_REQUIREMENT_LANDSCAPE_JSON_COMPARISON.md",
    "WS6_REQUIREMENT_LANDSCAPE_HTML_COMPARISON.md",
    "WS6_METADATA_PARITY_RECORD.md", "WS6_DISPOSITION_WORDING_RECORD.md",
    "WS6_SECTION14_PASS_THROUGH_RECORD.md",
    "WS6_PROTECTED_TEST_AMENDMENT_RECORD.md",
    "WS6_PRODUCT_OUTPUT_ASSESSMENT.md", "WS6_KNOWN_LIMITATIONS.md",
    "generate_ws6_artifacts.py", "ws6_case_inputs.json",
    "ws6_repetition_counts_base.json", "ws6_repetition_counts_head.json",
    "ws6_metadata_parity.json", "ws6_critdefer_split.json",
    "head_critdefer_before_meta.json", "head_critdefer_after_meta.json",
] + ["%s_%s_deliverable.%s" % (m, c, x)
     for m in ("base", "head")
     for c in ("ws1", "unknown", "deferred", "provisional", "emptycontent")
     for x in ("json", "html")]
for f in REQUIRED:
    if not os.path.exists(os.path.join(E, f)): fail("missing " + f)
ok("all %d required files exist" % len(REQUIRED))

def J(name): return json.load(open(os.path.join(E, name)))
for f in REQUIRED:
    if f.endswith(".json"): J(f)
ok("all JSON artifacts parse")

ident = open(os.path.join(E, "WS6_HEAD_IDENTITY.md")).read()
for sha in ("721b4613618d74e49707ced4d80b0571e5a2073f",
            "4f89d1ae37c8d8b59a76ef358ec9ef9d72c44176",
            "9a3fc6cffcb40bff2c4a83ea0ae3d8a9c46e8cbe",
            "9da70edae18d253b117a3c892add78ed7a3d8fac"):
    if sha not in ident: fail("identity SHA missing: " + sha)
ok("identity SHAs recorded")

b, h = J("ws6_repetition_counts_base.json"), J("ws6_repetition_counts_head.json")
if not (b["ws1"]["html_core_standalone_renderings"] == 8
        and b["ws1"]["html_repetition_sentence_count"] == 0
        and b["ws1"]["metadata_present"] is False): fail("BASE ws1 profile")
if not (h["ws1"]["html_core_standalone_renderings"] == 1
        and h["ws1"]["html_repetition_sentence_count"] == 1
        and h["ws1"]["html_owner_sentence_for_8_present"] is True
        and h["ws1"]["metadata_present"] is True): fail("HEAD ws1 profile")
if not all(v == 1 for v in
           h["ws1"]["html_distinct_statement_renderings"].values()):
    fail("HEAD distinct statements not rendered once")
if b["ws1"]["json_row_total"] != 13 or h["ws1"]["json_row_total"] != 13:
    fail("row totals changed")
ok("BASE/HEAD repetition counts match (8->1; sentence 0->1; rows 13==13)")

EXPECT = {
 "unknown": ("Recorded unknown", "You indicated that this is not known yet.",
             "This item remains unresolved. It may later be addressed "
             "through additional information, evidence, or specialist input."),
 "deferred": ("Deferred decision", "You chose to defer this item.",
              "This item remains unresolved and can be revisited when you "
              "are ready to decide."),
 "provisional": ("Provisional assumption",
                 "This assumption was recorded as a temporary direction and "
                 "has not been validated.",
                 "Validate, revise, or replace it before relying on it."),
}
for case, (lab, st, act) in EXPECT.items():
    c = h[case]
    if (c["s13_provenance"], c["s13_status"], c["s13_resolving_action"]) != (lab, st, act):
        fail("HEAD wording mismatch: " + case)
    if b[case]["s13_provenance"] != "Recorded answer":
        fail("BASE %s not legacy" % case)
    if c["s14_provenance"] != lab or c["s14_statement"] != act:
        fail("S14 pass-through mismatch: " + case)
placeholder = ("Insufficient information was recorded to organize this item "
               "reliably.\nThis does not indicate that the idea is invalid; "
               "the item remains unresolved.")
if h["emptycontent"]["s13_statement"] != placeholder: fail("D7 wording")
if b["emptycontent"]["s13_statement"] != "Recorded answer awaiting restatement.":
    fail("BASE placeholder not legacy")
ok("all disposition and placeholder wordings byte-exact (BASE legacy / HEAD approved)")

p = J("ws6_metadata_parity.json")
if not (p["parity_ok"] and p["repeated_group_total"] == 1
        and p["html_sentence_total_equals_repeated_group_total"]
        and p["internal_metadata_keys_leaked_to_html"] is False):
    fail("metadata parity record")
ok("metadata/HTML parity: parity_ok=true, no internal key leakage")

s = J("ws6_critdefer_split.json")
if not (s["before_core_counts"] == [8] and s["after_core_counts"] == [1, 7]
        and s["unrelated_session_meta_keys_byte_identical"]
        and s["unrelated_sections_byte_identical"]
        and s["row_total_unchanged"]): fail("criticality split evidence")
ok("criticality deferral split 8 -> 7 + 1 with unrelated keys byte-identical")

reg = open(os.path.join(E, "WS6_PROTECTED_REGRESSION_RECORD.md")).read()
for token in ("12 passed", "34 passed", "249 passed, 1 skipped",
              "31 failed, 1408 passed, 1 skipped, 1 xfailed, 24 xpassed",
              "test_domain_registry.py"):
    if token not in reg: fail("regression record missing: " + token)
ok("expected test totals recorded")

lim = open(os.path.join(E, "WS6_KNOWN_LIMITATIONS.md")).read()
for l in ("L1", "L2", "L3", "L4", "L5"):
    if ("%s —" % l) not in lim: fail("limitation missing: " + l)
ok("all known limitations recorded (L1-L5)")
print("VALIDATION PASSED")
