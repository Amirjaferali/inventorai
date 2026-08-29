#!/usr/bin/env python3
"""S2-PATHN-DCS-001 — supplemental decision-capture measurement slice runner.

Executes the authoritative frozen design
(docs/benchmarks/S2_PATHN_DECISION_CAPTURE_SLICE_DESIGN.md) EXACTLY ONCE at the
authorized product SHA. Evidence collection only. Lives OUTSIDE the repository,
changes no repository file, drives only committed served routes.
"""
import os, sys, json, re, hashlib, html as htmllib
from datetime import datetime, timezone

SCRATCH = "/tmp/claude-0/-home-user-inventorai/c90ac8ea-d0a7-5397-b2ad-0a9c096e3004/scratchpad"
REPO = "/home/user/inventorai"
EV = os.path.join(SCRATCH, "dcs001_evidence")
HTML_DIR = os.path.join(EV, "html")
os.makedirs(HTML_DIR, exist_ok=True)

EVALUATED_SHA = "d867b92eaa69221b1884a9a2eef25cd74225bb86"
SLICE_ID = "S2-PATHN-DCS-001"

os.environ["INVENTORAI_SECRET_KEY"] = "dcs001-evidence-local-only"
os.environ["INVENTORAI_DB_PATH"] = os.path.join(EV, "dcs001_store.sqlite3")
sys.path.insert(0, REPO)
os.chdir(REPO)

from web.app import app, SESSION_STORE            # noqa: E402
from engine.decision_composition import (         # noqa: E402
    compose_decision_records, decision_capture_view)
from engine.domain_rules import classify_domain, DomainResultKind  # noqa: E402
from engine import ai_advisor                     # noqa: E402
from web import ui_text                           # noqa: E402

assert ai_advisor.AI_ADVISORY_ENABLED is False, "AI advisory must be OFF"

# ---- frozen inputs: run-001 committed evidence blob, verbatim ----
AM = json.load(open(os.path.join(SCRATCH, "run001", "answer_maps.json")))
SEEDS = AM["seeds"]
ANSWERS = AM["answers"]

# §5 exact extracted candidate strings, as recorded in the frozen design.
CANDS = {
 ("E-1", "en"): ["a wired brake-lever switch",
                 "accelerometer-based inference of deceleration",
                 "wheel-speed-based inference"],
 ("E-1", "ar"): ["مفتاح سلكي على ذراع الفرامل",
                 "استدلال بالتسارع عبر مقياس تسارع",
                 "استدلال عبر سرعة العجلة"],
 ("M-1", "en"): ["over-centre toggle latch",
                 "spring-loaded detent pin",
                 "gravity-drop gate latch"],
 ("M-1", "ar"): ["مزلاج قلاب متجاوز للمركز",
                 "دبوس تعشيق بنابض",
                 "مزلاج بوابة يسقط بالجاذبية"],
}

RECORDS = [("D1","E-1","en","electronics_electrical"),
           ("D2","E-1","ar","electronics_electrical"),
           ("D3","M-1","en","electronics_electrical"),
           ("D4","M-1","ar","mechanical")]
RECORDS[2] = ("D3","M-1","en","mechanical")

TOKEN_RE = re.compile(r'name="answer_token"\s+value="([^"]+)"')

def sha256(b): return hashlib.sha256(b).hexdigest()
def save_html(name, text):
    open(os.path.join(HTML_DIR, name), "w", encoding="utf-8").write(text)
    return sha256(text.encode("utf-8"))

def payloads(case, lang):
    """§5 provenance: every payload verbatim from the frozen corpus."""
    a = ANSWERS[f"{case}|expert|{lang}"]["MECHANISM_COMPLETENESS"]
    p = {"CTX": a[0], "REF": a[1], "REASON": a[2],
         "ALT": list(CANDS[(case, lang)])}
    # fail-closed provenance assertion: every candidate string must be a
    # verbatim substring of the frozen answer [0]
    for n in p["ALT"]:
        assert n in a[0], f"candidate not verbatim in frozen corpus: {n!r}"
    return p

def token(c, sid):
    m = TOKEN_RE.search(c.get(f"/session/{sid}").get_data(as_text=True))
    return htmllib.unescape(m.group(1)) if m else None

def run_record(rid, case, lang, target):
    seed = SEEDS[f"{case}|{lang}"]
    p = payloads(case, lang)
    c = app.test_client()
    rec = {"record_id": rid, "slice_id": SLICE_ID, "case": case, "language": lang,
           "perspective": "experienced-technical", "evaluated_sha": EVALUATED_SHA,
           "seed_exact": seed, "payloads": p, "actions": [], "anomalies": []}
    c.post("/ui-language", data={"lang": lang, "next": "/"})
    cls = classify_domain(seed)
    rec["classifier_result"] = cls.kind.name
    r = c.post("/start", data={"idea": seed})
    if r.status_code != 302:
        r = c.post("/start", data={"idea": seed, "domain_choice": target})
    if r.status_code != 302:
        r = c.post("/start", data={"idea": seed, "domain_choice": target,
                                   "domain_confirm": target})
    if r.status_code != 302:
        rec["anomalies"].append("ADMISSION FAILED"); rec["execution_status"]="ADMISSION_FAILED"
        return rec
    sid = r.headers["Location"].rstrip("/").split("/")[-1]
    rec["sid"] = sid
    st = SESSION_STORE[sid]["state"]
    rec["confirmed_domain"] = st.domain

    def act(n, label, route, data):
        data = dict(data); data["answer_token"] = token(c, sid)
        resp = c.post(f"/session/{sid}/decision/{route}", data=data)
        rec["actions"].append({"n": n, "action": label, "route": route,
                               "payload": {k: v for k, v in data.items()
                                           if k != "answer_token"},
                               "status": resp.status_code})
        if resp.status_code != 302:
            rec["anomalies"].append(f"action {n} ({label}) returned {resp.status_code}")
        return resp

    # §4 action matrix, in order
    act(1, "declare context", "declare-context", {"content": p["CTX"]})
    st = SESSION_STORE[sid]["state"]
    ctx_root = [a for a in st.assertions
                if a.disposition == "decision_context_declared"][0].record_id
    rec["context_root"] = ctx_root
    for i, name in enumerate(p["ALT"], start=2):
        act(i, f"declare alternative {i-1}", "declare-alternative",
            {"content": name, "context_root": ctx_root})
    view = decision_capture_view(SESSION_STORE[sid]["state"])
    heads = {a["name"]: a["head_record_id"] for a in view[0]["alternatives"]}
    act(5, "refine alternative 1", "refine-alternative",
        {"content": p["REF"], "supersedes_record_id": heads[p["ALT"][0]]})
    act(6, "withdraw alternative 2 WITH reason", "withdraw-alternative",
        {"supersedes_record_id": heads[p["ALT"][1]], "reason": p["REASON"]})
    act(7, "withdraw alternative 3 WITHOUT reason", "withdraw-alternative",
        {"supersedes_record_id": heads[p["ALT"][2]], "reason": ""})
    act(8, "re-declare alternative 2", "declare-alternative",
        {"content": p["ALT"][1], "context_root": ctx_root})

    st = SESSION_STORE[sid]["state"]
    rec["decision_capture_view"] = decision_capture_view(st)
    rec["composed_records"] = [r_.to_record_dict() for r_ in compose_decision_records(st)]
    rec["ledger_decision_records"] = [
        {"record_id": a.record_id, "disposition": a.disposition,
         "content": a.content, "supersedes": list(a.supersedes),
         "superseded_by": getattr(a, "superseded_by", None),
         "provenance": getattr(a, "provenance", None)}
        for a in st.assertions if a.disposition.startswith("decision_")]
    s_html = c.get(f"/session/{sid}").get_data(as_text=True)
    d_html = c.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    rec["deliverable_http_status"] = 200 if d_html else None
    rec["html_sha256"] = {f"{rid}_session.html": save_html(f"{rid}_session.html", s_html),
                          f"{rid}_deliverable.html": save_html(f"{rid}_deliverable.html", d_html)}
    rec["execution_status"] = "EXECUTED"
    return rec

def main():
    started = datetime.now(timezone.utc).isoformat()
    out = {"slice_id": SLICE_ID, "evaluated_sha": EVALUATED_SHA,
           "started_utc": started, "records": {}}
    for spec in RECORDS:
        print(f"=== executing {spec[0]} {spec[1]} {spec[2]} ===", flush=True)
        out["records"][spec[0]] = run_record(*spec)
        r = out["records"][spec[0]]
        print(f"   status={r['execution_status']} actions={len(r['actions'])} "
              f"anomalies={len(r['anomalies'])}", flush=True)
    out["finished_utc"] = datetime.now(timezone.utc).isoformat()
    json.dump(out, open(os.path.join(EV, "all_records.json"), "w"),
              ensure_ascii=False, indent=1)
    print("DONE")

if __name__ == "__main__":
    main()
