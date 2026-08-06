#!/usr/bin/env python3
"""Workstream 7 evidence validator.

File: docs/governance/evidence/workstream7_actionable_validation_plan/validate_ws7_evidence.py
Purpose: deterministically validate the Workstream 7 evidence package by
re-deriving every claimed count and wording from the RAW artifacts in this
directory (never from narrative summaries), and by verifying the manifest.
Input contract: run from the repository root: `python <this file>`. Reads only
files inside this evidence directory plus `git rev-parse` for identity checks
when run inside a checkout containing the commits.
Output contract: prints one PASS/STOP line per check and a final verdict;
exits 0 only if every check passes (final line `VALIDATOR RESULT: PASS`),
non-zero otherwise (`VALIDATOR RESULT: STOP`).
Prohibited behaviors: MUST NOT modify any file; MUST NOT trust any summary
value it can re-derive from raw artifacts.
"""
import hashlib
import json
import os
import re
import sys

EV = os.path.dirname(os.path.abspath(__file__))
BASE_SHA = "e1e71b3b089cd41fc90ca4f2c0b7ce6a37e37268"
HEAD_SHA = "52b1960fc99af6e746c522b9b32509df1a45076d"

RESP1 = "Responsibility has not yet been assigned."
RESP2 = "Choose who will own this validation step before relying on the result."
ADV_E = ("Additional evidence is still required for this item.\n"
         "Prepare or obtain the evidence identified in the recorded request "
         "before treating the item as validated.")
ADV_S = ("Specialist input is still required for this item.\n"
         "The appropriate specialist has not yet been identified by the system.")
LEGACY = "Validate the recorded answer against the available evidence."
PREFIX = "Validate this recorded answer against the available evidence: "

FAILURES = []


def check(name, cond, detail=""):
    print(f"[{'PASS' if cond else 'STOP'}] {name}" + (f" | {detail}" if detail else ""))
    if not cond:
        FAILURES.append(name)


def read(name):
    with open(os.path.join(EV, name)) as f:
        return f.read()


def jload(name):
    return json.loads(read(name))


REQUIRED = [
    "README.md", "BASE_IDENTITY.txt", "HEAD_IDENTITY.txt",
    "BASE_FOCUSED_PYTEST.txt", "HEAD_FOCUSED_PYTEST.txt",
    "AFFECTED_SUITES_HEAD.txt",
    "PROTECTED_BATTERY_BASE.txt", "PROTECTED_BATTERY_HEAD.txt",
    "FULL_SUITE_BASE.txt", "FULL_SUITE_HEAD.txt",
    "FAILURE_DISTRIBUTION_BASE.txt", "FAILURE_DISTRIBUTION_HEAD.txt",
    "BASE_WS1_JSON.json", "HEAD_WS1_JSON.json",
    "BASE_WS1_HTML.html", "HEAD_WS1_HTML.html",
    "BASE_MINIMAL_ANSWERED_JSON.json", "HEAD_MINIMAL_ANSWERED_JSON.json",
    "BASE_MINIMAL_ANSWERED_HTML.html", "HEAD_MINIMAL_ANSWERED_HTML.html",
    "BASE_PENDING_EVIDENCE_JSON.json", "HEAD_PENDING_EVIDENCE_JSON.json",
    "BASE_PENDING_EVIDENCE_HTML.html", "HEAD_PENDING_EVIDENCE_HTML.html",
    "BASE_PENDING_SPECIALIST_JSON.json", "HEAD_PENDING_SPECIALIST_JSON.json",
    "BASE_PENDING_SPECIALIST_HTML.html", "HEAD_PENDING_SPECIALIST_HTML.html",
    "BASE_NON_PENDING_CASES.json", "HEAD_NON_PENDING_CASES.json",
    "BASE_PROTECTED_INVARIANTS.txt", "HEAD_PROTECTED_INVARIANTS.txt",
    "INVENTION_TOKEN_SCAN.txt", "D13_NON_IMPLEMENTATION_AUDIT.txt",
    "PROTECTED_BATTERY_FILE_LIST.txt",
    "MANIFEST.sha256", "EVIDENCE_VALIDATION_REPORT.txt",
    "generate_ws7_artifacts.py", "validate_ws7_evidence.py",
]


def main():
    # 1. required files exist (the report file is created by this run's caller;
    #    tolerate absence only for it during a first pass).
    for f in REQUIRED:
        if f == "EVIDENCE_VALIDATION_REPORT.txt" and not os.path.exists(os.path.join(EV, f)):
            print(f"[NOTE] {f} will be written from this run's output")
            continue
        check(f"file exists: {f}", os.path.exists(os.path.join(EV, f)))

    # 2. identities (raw artifact content).
    check("BASE identity records expected SHA", BASE_SHA in read("BASE_IDENTITY.txt"))
    check("HEAD identity records expected SHA", HEAD_SHA in read("HEAD_IDENTITY.txt"))
    check("HEAD parent is BASE", f"parents: {BASE_SHA}" in read("HEAD_IDENTITY.txt"))

    # 3. focused counts, re-derived from raw pytest output.
    bf, hf = read("BASE_FOCUSED_PYTEST.txt"), read("HEAD_FOCUSED_PYTEST.txt")
    check("BASE focused 6 failed / 12 passed", "6 failed, 12 passed" in bf)
    check("HEAD focused 18 passed", re.search(r"= 18 passed", hf) is not None)
    for t in ("r1", "r2", "r3", "r4", "r5", "r6"):
        red = re.search(rf"test_{t}\w+ FAILED", bf)
        green = re.search(rf"test_{t}\w+ PASSED", hf)
        check(f"{t.upper()} RED on BASE and GREEN on HEAD", bool(red and green))
    for i in range(1, 13):
        pb = re.search(rf"test_p{i}_\w+ PASSED", bf)
        ph = re.search(rf"test_p{i}_\w+ PASSED", hf)
        check(f"P{i} PASS on BASE and HEAD", bool(pb and ph))
    check("BASE focused: no skips/xfails/errors",
          not re.search(r"\d+ (skipped|xfailed|error)", bf.splitlines()[-1]))
    check("HEAD focused: no skips/xfails/errors",
          not re.search(r"\d+ (skipped|xfailed|error)", hf.splitlines()[-1]))

    # 4. protected battery, both sides, same fixed list.
    for mode in ("BASE", "HEAD"):
        t = read(f"PROTECTED_BATTERY_{mode}.txt")
        check(f"{mode} protected battery 259 passed, 1 skipped",
              "259 passed, 1 skipped" in t)
    check("battery commands identical (modulo checkout dir)",
          read("PROTECTED_BATTERY_BASE.txt").splitlines()[0].split(")")[-1]
          == read("PROTECTED_BATTERY_HEAD.txt").splitlines()[0].split(")")[-1])
    check("known WPS001 skip named in file list",
          "test_closed_gap_does_not_reopen" in read("PROTECTED_BATTERY_FILE_LIST.txt"))

    # 5. full suite, re-derived failure distribution.
    fsb, fsh = read("FULL_SUITE_BASE.txt"), read("FULL_SUITE_HEAD.txt")
    check("BASE full suite 37 failed / 1420 passed / 1 skipped / 1 xfailed / 24 xpassed",
          "37 failed, 1420 passed, 1 skipped, 1 xfailed, 24 xpassed" in fsb)
    check("HEAD full suite 31 failed / 1426 passed / 1 skipped / 1 xfailed / 24 xpassed",
          "31 failed, 1426 passed, 1 skipped, 1 xfailed, 24 xpassed" in fsh)

    def dist(txt):
        d = {}
        for line in txt.splitlines():
            m = re.match(r"^FAILED (\S+?)::", line)
            if m:
                d[m.group(1)] = d.get(m.group(1), 0) + 1
        return d

    db, dh = dist(fsb), dist(fsh)
    check("BASE distribution: 31 domain-registry + 6 WS7 RED, nothing else",
          db == {"tests/test_domain_registry.py": 31,
                 "tests/test_actionable_validation_plan.py": 6}, str(db))
    check("HEAD distribution: 31 domain-registry only",
          dh == {"tests/test_domain_registry.py": 31}, str(dh))

    # 6. exact public wordings and user-output truthfulness, from raw JSON/HTML.
    bmin = jload("BASE_MINIMAL_ANSWERED_JSON.json")
    hmin = jload("HEAD_MINIMAL_ANSWERED_JSON.json")
    bstmt = bmin["package"]["section_14"]["steps"][0]["statement"]
    hstmt = hmin["package"]["section_14"]["steps"][0]["statement"]
    src = hmin["package"]["section_13"]["requirements"][0]["statement"]
    check("BASE answered statement is the legacy generic", bstmt == LEGACY)
    check("HEAD answered statement is the exact owner wording with byte-verbatim embed",
          hstmt == PREFIX + "“" + src + "”")
    check("HEAD Section 13 statement byte-equal to BASE Section 13 statement",
          src == bmin["package"]["section_13"]["requirements"][0]["statement"])

    bws1, hws1 = jload("BASE_WS1_JSON.json"), jload("HEAD_WS1_JSON.json")
    ba = [s for s in bws1["engine"]["steps"] if s["provenance_label"] == "Recorded answer"]
    ha = [s for s in hws1["engine"]["steps"] if s["provenance_label"] == "Recorded answer"]
    check("WS1: twelve answered steps on both sides", len(ba) == len(ha) == 12)
    check("WS1 BASE: all twelve share the generic statement",
          all(s["statement"] == LEGACY for s in ba))
    s13map = {r["statement"]: r for r in hws1["package"]["section_13"]["requirements"]}
    check("WS1 HEAD: every answered step embeds a Section 13 statement byte-verbatim",
          all(s["statement"].startswith(PREFIX + "“")
              and s["statement"].endswith("”")
              and s["statement"][len(PREFIX) + 1:-1] in s13map for s in ha))
    check("WS1 Section 13 byte-equal BASE vs HEAD",
          bws1["package"]["section_13"] == hws1["package"]["section_13"])
    check("WS1 step-id order equal BASE vs HEAD",
          [s["step_id"] for s in bws1["engine"]["steps"]]
          == [s["step_id"] for s in hws1["engine"]["steps"]])
    check("WS1 arithmetic tie on both sides",
          all(w["package"]["section_14"]["validation_step_total"]
              + w["package"]["section_14"]["blocked_item_total"]
              == w["package"]["section_13"]["total"] for w in (bws1, hws1)))
    check("responsibility tokens preserved (engine, BASE==HEAD)",
          [s["responsibility_token"] for s in bws1["engine"]["steps"]]
          == [s["responsibility_token"] for s in hws1["engine"]["steps"]])
    check("confidence token UNDETERMINED everywhere on both sides",
          all(s["confidence_token"] == "UNDETERMINED"
              for w in (bws1, hws1) for s in w["engine"]["steps"]))

    bh, hh = read("BASE_WS1_HTML.html"), read("HEAD_WS1_HTML.html")

    def sec14(html):
        i = html.find("<h3>Validation Plan</h3>")
        j = html.find("back-link", i)
        return html[i:j]

    check("BASE HTML renders the confidence line", "Confidence:" in sec14(bh))
    check("HEAD HTML suppresses the confidence line", "Confidence:" not in sec14(hh))
    check("BASE HTML shows 'Responsibility undetermined'",
          "Responsibility undetermined" in sec14(bh))
    check("HEAD HTML shows the exact two-line responsibility wording",
          RESP1 in sec14(hh) and RESP2 in sec14(hh))
    check("HEAD JSON confidence fields byte-unchanged",
          all(s["confidence"] == "Confidence undetermined"
              and s["confidence_label"] == "Confidence undetermined"
              for s in hws1["package"]["section_14"]["steps"]))

    bpe = jload("BASE_PENDING_EVIDENCE_JSON.json")["package"]["section_14"]["steps"][0]
    hpe = jload("HEAD_PENDING_EVIDENCE_JSON.json")["package"]["section_14"]["steps"][0]
    bps = jload("BASE_PENDING_SPECIALIST_JSON.json")["package"]["section_14"]["steps"][0]
    hps = jload("HEAD_PENDING_SPECIALIST_JSON.json")["package"]["section_14"]["steps"][0]
    check("BASE pending_evidence has no advisory", bpe.get("advisory") is None)
    check("HEAD pending_evidence advisory exact", hpe.get("advisory") == ADV_E)
    check("BASE pending_specialist has no advisory", bps.get("advisory") is None)
    check("HEAD pending_specialist advisory exact", hps.get("advisory") == ADV_S)
    hpeh = sec14(read("HEAD_PENDING_EVIDENCE_HTML.html"))
    hpsh = sec14(read("HEAD_PENDING_SPECIALIST_HTML.html"))
    check("HEAD pending_evidence advisory rendered",
          all(l in hpeh for l in ADV_E.split("\n")))
    check("HEAD pending_specialist advisory rendered",
          all(l in hpsh for l in ADV_S.split("\n")))
    check("advisory scoped: null on all WS1 (non-pending) HEAD steps",
          all(s.get("advisory") is None
              for s in hws1["package"]["section_14"]["steps"]))

    hnp = jload("HEAD_NON_PENDING_CASES.json")
    bnp = jload("BASE_NON_PENDING_CASES.json")
    for k in ("unknown", "deferred", "provisional_assumption"):
        brow = bnp[k]["package"]["section_13"]["requirements"][0]
        hrow = hnp[k]["package"]["section_13"]["requirements"][0]
        hstep = hnp[k]["package"]["section_14"]["steps"][0]
        check(f"{k}: pass-through byte-identical and BASE==HEAD",
              brow["resolving_action"] == hrow["resolving_action"]
              == hstep["statement"])
        check(f"{k}: advisory null", hstep.get("advisory") is None)
    check("contradiction statement unchanged BASE==HEAD",
          bnp["contradiction"]["package"]["section_14"]["steps"][0]["statement"]
          == hnp["contradiction"]["package"]["section_14"]["steps"][0]["statement"])
    check("criticality preserved on HEAD",
          hnp["criticality_linked"]["package"]["section_13"]["requirements"][0]
          ["criticality_rationale"] == "Without the right fuse the device fails.")
    check("risk/safety linkage present on both sides",
          bool(bnp["risk_safety_linked"]["risk_safety_linkage"])
          and bool(hnp["risk_safety_linked"]["risk_safety_linkage"])
          and bnp["risk_safety_linked"]["safety_signal_total"]
          == hnp["risk_safety_linked"]["safety_signal_total"] == 3)

    # 7. scans and audits carry PASS verdicts and required statements.
    check("invention-token scan PASS with zero hits",
          "RESULT: 0 unauthorized token(s) found -> PASS" in read("INVENTION_TOKEN_SCAN.txt"))
    d13 = read("D13_NON_IMPLEMENTATION_AUDIT.txt")
    for phrase in ("NOT designed", "NOT implemented", "NOT approximated",
                   "has not yet been identified by the system",
                   "No specialist taxonomy", "No routing"):
        check(f"D13 audit states: {phrase}", phrase in d13)

    # 8. manifest integrity.
    manifest = {}
    for line in read("MANIFEST.sha256").splitlines():
        if line.strip():
            digest, name = line.split(None, 1)
            manifest[name.strip().lstrip("*")] = digest
    listed = set(manifest)
    ondisk = {f for f in os.listdir(EV)
              if f not in ("MANIFEST.sha256",) and not f.startswith(".")}
    check("manifest covers every evidence file (no missing)",
          ondisk - listed == set(), str(sorted(ondisk - listed)))
    check("manifest has no extra entries", listed - ondisk == set(),
          str(sorted(listed - ondisk)))
    bad = []
    for name, digest in manifest.items():
        if name == "EVIDENCE_VALIDATION_REPORT.txt":
            continue  # the report is finalized after this run; its hash is
            # verified by the standalone `sha256sum -c` reproduction check.
        h = hashlib.sha256(open(os.path.join(EV, name), "rb").read()).hexdigest()
        if h != digest:
            bad.append(name)
    check("manifest hashes verify (report file excluded; see note)", not bad, str(bad))

    print()
    if FAILURES:
        print(f"VALIDATOR RESULT: STOP ({len(FAILURES)} failed checks)")
        return 1
    print("VALIDATOR RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
