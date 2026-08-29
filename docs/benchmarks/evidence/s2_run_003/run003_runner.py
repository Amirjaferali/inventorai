#!/usr/bin/env python3
"""RVR-8 / S2-PATHN-RUN-002 runner — evidence collection only.

Mirrors the S2-PATHN-RUN-001 method exactly (in-process Flask test client at the
frozen RC tree; INVENTORAI_DB_PATH bound to an external run store; frozen seeds
and answer corpus reused verbatim from the run-001 evidence pack; 24-interaction
bound per record; 8 records = 2 cases x 2 languages x 2 perspectives).

This script lives OUTSIDE the repository, changes no repository file, and makes
no product change. It drives only committed, served routes plus read-only
introspection for capture (SESSION_STORE state, assemble_deliverable, the
durable store's read API) exactly as run-001 did.
"""
import os, sys, json, re, hashlib, html as htmllib
from datetime import datetime, timezone

SCRATCH = "/tmp/claude-0/-home-user-inventorai/c90ac8ea-d0a7-5397-b2ad-0a9c096e3004/scratchpad"
REPO = "/home/user/inventorai"
EV = os.path.join(SCRATCH, "run003_evidence")
HTML_DIR = os.path.join(EV, "html")
os.makedirs(HTML_DIR, exist_ok=True)

RC_SHA = "5a392f0cfd7d6b19874382441f78fee61cee1a26"

os.environ["INVENTORAI_SECRET_KEY"] = "s2-run003-evidence-local-only"
os.environ["INVENTORAI_DB_PATH"] = os.path.join(EV, "run003_store.sqlite3")
sys.path.insert(0, REPO)
os.chdir(REPO)

from web.app import app, SESSION_STORE           # noqa: E402
from web import app as appmod                    # noqa: E402
from engine.progression_loop import select_next_gap  # noqa: E402
from engine.deliverable_assembler import assemble_deliverable  # noqa: E402
from engine.domain_rules import classify_domain, DomainResultKind  # noqa: E402
from engine import ai_advisor                    # noqa: E402

assert ai_advisor.AI_ADVISORY_ENABLED is False, "AI advisory must be OFF"

# ---- frozen inputs: reused verbatim from the run-001 evidence pack ----
AM1 = json.load(open(os.path.join(SCRATCH, "run001", "answer_maps.json")))
SEEDS = AM1["seeds"]              # E-1|en, M-1|en, E-1|ar, M-1|ar — frozen
ANSWERS = AM1["answers"]          # per case|perspective|lang, keyed by gap type

# Evaluator-authored honest-unknown fallback for any gap type the frozen corpus
# does not carry (a NEW question class would be adaptive-interaction behaviour
# absent at run 001). Case facts only; perspective register; recorded verbatim.
UNKNOWN_FALLBACK = {
    ("novice", "en"): "I honestly do not know that - nothing I have tells me the answer yet.",
    ("expert", "en"): "Unknown at this stage; the case specification does not state it and I have no measured data.",
    ("novice", "ar"): "بصراحة لا أعرف ذلك — لا أملك معلومات تجيب عن هذا بعد.",
    ("expert", "ar"): "غير معروف في هذه المرحلة؛ لا تذكر مواصفات الحالة ذلك ولا أملك بيانات مقاسة.",
}

RECORDS = [
    ("R1", "E-1", "en", "novice", "electronics_electrical"),
    ("R2", "E-1", "en", "expert", "electronics_electrical"),
    ("R3", "E-1", "ar", "novice", "electronics_electrical"),
    ("R4", "E-1", "ar", "expert", "electronics_electrical"),
    ("R5", "M-1", "en", "novice", "mechanical"),
    ("R6", "M-1", "en", "expert", "mechanical"),
    ("R7", "M-1", "ar", "novice", "mechanical"),
    ("R8", "M-1", "ar", "expert", "mechanical"),
]

Q_RE = re.compile(r'<p class="question" lang="([^"]*)" dir="([^"]*)">(.*?)</p>', re.S)
TOKEN_RE = re.compile(r'name="answer_token"\s+value="([^"]+)"')
BOUND = 24

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def save_html(name: str, text: str) -> str:
    p = os.path.join(HTML_DIR, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    return sha256(text.encode("utf-8"))

def gap_snapshot(state):
    out = []
    for g in getattr(state, "gaps", []):
        out.append({"gap_type": g.gap_type, "status": g.status,
                    "iterations_open": getattr(g, "iterations_open", None)})
    return out

def extract_question(page_html):
    m = Q_RE.search(page_html)
    if not m:
        return None, None, None
    lang, direc, text = m.group(1), m.group(2), m.group(3)
    return lang, direc, htmllib.unescape(re.sub(r"\s+", " ", text)).strip()

def run_record(rid, case, lang, persp, target):
    seed = SEEDS[f"{case}|{lang}"]
    akey = f"{case}|{persp}|{lang}"
    amap = ANSWERS[akey]
    used_answers = {}          # gap_type -> list of answers actually submitted
    idx = {}                   # gap_type -> next index
    client = app.test_client()
    rec = {"record_id": rid, "case": case, "language": lang, "perspective": persp,
           "anomalies": [], "admission_steps": [], "interactions": [],
           "seed_exact": seed, "new_gap_types_encountered": []}

    # UI language (both set explicitly; presentation preference in signed session)
    client.post("/ui-language", data={"lang": lang, "next": "/"})

    cls = classify_domain(seed)
    rec["classifier_result"] = {"kind": cls.kind.name,
                                "selected_domain": getattr(cls, "selected_domain", None)}

    # ---- admission (generic: idea -> [choice] -> confirm -> 302) ----
    r = client.post("/start", data={"idea": seed})
    rec["admission_steps"].append({"step": "POST /start (idea only)", "status": r.status_code})
    if r.status_code != 302:
        r = client.post("/start", data={"idea": seed, "domain_choice": target})
        rec["admission_steps"].append(
            {"step": f"POST /start + domain_choice={target}", "status": r.status_code})
    if r.status_code != 302:
        r = client.post("/start", data={"idea": seed, "domain_choice": target,
                                        "domain_confirm": target})
        rec["admission_steps"].append(
            {"step": f"POST /start + choice+confirm={target}", "status": r.status_code,
             "location": r.headers.get("Location")})
    if r.status_code != 302:
        rec["anomalies"].append("ADMISSION FAILED: no 302 after confirm")
        rec["execution_status"] = "ADMISSION_FAILED"
        return rec
    sid = r.headers["Location"].rstrip("/").split("/")[-1]
    rec["sid"] = sid
    rec["admission_route"] = ("classifier SINGLE -> explicit confirmation"
                              if cls.kind is DomainResultKind.SINGLE
                              else "NONE -> D2 explicit choice -> explicit confirmation")
    state = SESSION_STORE[sid]["state"]
    rec["confirmed_domain"] = state.domain
    rec["path"] = state.path

    first_html = None
    last_html = None
    q_langs = []
    reached_no_open_gap = False

    for n in range(BOUND):
        page = client.get(f"/session/{sid}")
        page_html = page.get_data(as_text=True)
        if n == 0:
            first_html = page_html
        last_html = page_html
        qlang, qdir, qtext = extract_question(page_html)
        state = SESSION_STORE[sid]["state"]
        gap = select_next_gap(state)
        if gap is None:
            reached_no_open_gap = True
            break
        q_langs.append({"n": n, "gap": gap, "q_lang": qlang, "q_dir": qdir})
        # answer selection: frozen corpus first; evaluator honest-unknown fallback
        if gap in amap:
            lst = amap[gap]
            i = idx.get(gap, 0)
            answer = lst[min(i, len(lst) - 1)]
            idx[gap] = i + 1
        else:
            answer = UNKNOWN_FALLBACK[(persp, lang)]
            if gap not in rec["new_gap_types_encountered"]:
                rec["new_gap_types_encountered"].append(gap)
        used_answers.setdefault(gap, [])
        if not used_answers[gap] or used_answers[gap][-1] != answer:
            used_answers[gap].append(answer)
        tok = TOKEN_RE.search(page_html)
        form = {"response": answer}
        if tok:
            form["answer_token"] = tok.group(1)
        else:
            rec["anomalies"].append(f"no answer_token on session page at n={n}")
        pr = client.post(f"/session/{sid}", data=form)
        state = SESSION_STORE[sid]["state"]
        rec["interactions"].append({
            "n": n, "gap_type": gap,
            "question_displayed": qtext, "question_lang": qlang, "question_dir": qdir,
            "answer": answer, "post_status": pr.status_code,
            "answer_error": None if pr.status_code == 302 else pr.get_data(as_text=True)[:300],
            "gaps_after": gap_snapshot(state),
            "maturity_after": getattr(state, "maturity_level", None),
            "stage_after": getattr(state, "stage", None),
            "iteration_after": getattr(state, "iteration", None),
        })
        if pr.status_code != 302:
            rec["anomalies"].append(f"POST answer at n={n} returned {pr.status_code}")

    rec["interaction_count"] = len(rec["interactions"])
    rec["reached_no_open_gap"] = reached_no_open_gap
    state = SESSION_STORE[sid]["state"]
    rec["final_gaps"] = gap_snapshot(state)
    rec["final_maturity"] = getattr(state, "maturity_level", None)
    rec["final_stage"] = getattr(state, "stage", None)
    rec["final_iteration"] = getattr(state, "iteration", None)
    rec["question_language_trace"] = q_langs

    # ---- deliverable (served route + read-only assembly for meta) ----
    dr = client.get(f"/session/{sid}/deliverable")
    rec["deliverable_http_status"] = dr.status_code
    deliverable_html = dr.get_data(as_text=True)
    package = assemble_deliverable(state)
    meta = package["_session_meta"]
    rec["deliverable_eligible"] = meta.get("deliverable_eligible")
    rec["deliverable_meta"] = {k: meta.get(k) for k in
        ("total_iterations", "total_gaps", "open_gap_count", "closed_gap_count",
         "maturity_level", "maturity_label", "direction", "domain_signal",
         "evidence_quality", "idea_summary")}
    rec["deliverable_sections"] = sorted(k for k in package.keys() if k.startswith("section"))

    # correction-path reachability on rendered surfaces (criteria 11/14)
    rec["correct_affordance_in_session_html"] = ("/correct" in (last_html or ""))
    rec["correct_affordance_in_deliverable_html"] = ("/correct" in deliverable_html)

    # durable envelope capture (read-only store API)
    store = appmod._get_store()
    contract = store.load_contract(sid)
    cj = contract.to_dict() if hasattr(contract, "to_dict") else str(contract)
    ledger = store.load_accepted_answer_evidence(sid)
    rec["envelope"] = {
        "contract_keys": sorted(cj.keys()) if isinstance(cj, dict) else None,
        "contract_version": (cj.get("contract_version") if isinstance(cj, dict) else None),
        "engine_contract_version": (cj.get("engine_contract_version") if isinstance(cj, dict) else None),
        "seed_idea_text_matches": (isinstance(cj, dict) and cj.get("seed_idea_text") == seed),
        "ledger_record_count": len(ledger),
    }

    # evidence html capture
    rec["html_sha256"] = {
        f"{rid}_session_first.html": save_html(f"{rid}_session_first.html", first_html or ""),
        f"{rid}_session_last.html": save_html(f"{rid}_session_last.html", last_html or ""),
        f"{rid}_deliverable.html": save_html(f"{rid}_deliverable.html", deliverable_html),
    }
    rec["answers_used"] = used_answers
    rec["execution_status"] = "EXECUTED"
    return rec


def main():
    started = datetime.now(timezone.utc).isoformat()
    all_records = {}
    for spec in RECORDS:
        rid = spec[0]
        print(f"=== executing {rid} {spec[1]} {spec[2]} {spec[3]} ===", flush=True)
        all_records[rid] = run_record(*spec)
        r = all_records[rid]
        print(f"  status={r['execution_status']} interactions={r.get('interaction_count')} "
              f"no_open_gap={r.get('reached_no_open_gap')} "
              f"eligible={r.get('deliverable_eligible')} "
              f"final_stage={r.get('final_stage')} maturity={r.get('final_maturity')} "
              f"new_gaps={r.get('new_gap_types_encountered')}", flush=True)
    out = {
        "run_id": "S2-PATHN-RUN-003",
        "post_g3_t1a_prime_reverification": True,
        "evaluated_rc_sha": RC_SHA,
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "records": all_records,
    }
    with open(os.path.join(EV, "all_records.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    # Baseline A (E-1 only): FDC-001 decision-workspace export at the RC
    client = app.test_client()
    lw = client.get("/decision-workspace")
    dids = re.findall(r'/decision-workspace/([A-Za-z0-9\-_]+)', lw.get_data(as_text=True))
    ba = {"list_status": lw.status_code, "dids_found": sorted(set(d for d in dids if d != "")),
          "export": None, "export_status": None}
    did = next((d for d in ba["dids_found"] if "export" not in d), None)
    if did:
        ex = client.get(f"/decision-workspace/{did}/export")
        ba["export_status"] = ex.status_code
        if ex.status_code == 200:
            try:
                ba["export"] = json.loads(ex.get_data(as_text=True))
            except Exception:
                ba["export"] = {"raw_head": ex.get_data(as_text=True)[:400]}
    with open(os.path.join(EV, "baselineA_E1_export_run002.json"), "w", encoding="utf-8") as f:
        json.dump(ba, f, ensure_ascii=False, indent=1)
    print("DONE")

if __name__ == "__main__":
    main()
