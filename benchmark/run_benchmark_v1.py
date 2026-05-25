import json, time, os, sys
from datetime import datetime
import urllib.request
import re

print("RUNNER VERSION 1.1 ACTIVE")

MODEL          = "claude-3-5-sonnet-20241022"
SCHEMA_VERSION = "1.1"

def load_files():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt = open(os.path.join(base, "prompts/iot_electronics_system_prompt.md"), encoding="utf-8").read()
    schema = json.load(open(os.path.join(base, "schemas/iot_electronics_output.schema.json"), encoding="utf-8"))
    return prompt, schema

SYSTEM_PROMPT, OUTPUT_SCHEMA = load_files()
REQUIRED_FIELDS = OUTPUT_SCHEMA["required"]

def get_api_key():
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        print("  create .env with: ANTHROPIC_API_KEY=sk-ant-api03-...")
        sys.exit(1)
    if key.startswith("sk-ant-sk-ant"):
        print("ERROR: doubled prefix 'sk-ant-sk-ant'. Paste key only once.")
        sys.exit(1)
    if " " in key:
        print("ERROR: API key contains spaces.")
        sys.exit(1)
    preview = key[:12] + "..." + key[-4:] if len(key) > 16 else key[:4] + "..."
    print(f"API key loaded: {preview}")
    return key

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

ENUM_MAP = {
    "confidence_level": ["LOW","MEDIUM","HIGH"],
    "feasibility_signal": ["APPEARS_FEASIBLE","APPEARS_FEASIBLE_WITH_CAVEATS",
                           "FEASIBILITY_UNCLEAR","SIGNIFICANT_CONCERNS_IDENTIFIED","INSUFFICIENT_INPUT"],
    "prototype_path_clarity": ["DESCRIBED_PATH_EXISTS","PARTIAL_PATH_ONLY","INSUFFICIENT_INFO"],
    "component_specificity": ["USER_SPECIFIED","CLEARLY_IMPLIED_TYPE","UNCLEAR"],
}

def normalize_output(obj):
    if not isinstance(obj, dict):
        return obj
    def nv(key, val):
        if isinstance(val, str):
            val = val.strip()
            if key in ENUM_MAP:
                upper = val.upper().replace(" ","_").replace("-","_")
                for v in ENUM_MAP[key]:
                    if upper == v:
                        return v
        if isinstance(val, dict):
            return {k: nv(k, w) for k, w in val.items()}
        if isinstance(val, list):
            return [nv(key, item) for item in val]
        return val
    return {k: nv(k, v) for k, v in obj.items()}

def call_claude(tc, api_key):
    result = dict(http_status=None, http_error_body=None, raw_text=None,
                  extraction_method=None, extraction_failure=None,
                  parsed_output=None, normalized_output=None,
                  error_category=None, error_detail=None)

    msg = f"""[IDEA_INPUT]
الفكرة: {tc['idea']}
المشكلة: {tc['problem']}
الحل: {tc['solution']}
المستفيد: {tc['beneficiary']}
المجال: {tc['domain']}

[COMPLETENESS_CONTEXT]
نتيجة فحص الاكتمال: auto/100
تحذيرات: []

[TASK]
أنتج تحليلاً أولياً منظماً وفق الـ JSON schema المحدد.
أخرج JSON صالح فقط. بدون markdown. بدون شرح. بدون نص قبل JSON أو بعده."""

    payload = json.dumps({
        "model": MODEL, "max_tokens": 2000,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": msg}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=payload,
        headers={"Content-Type": "application/json",
                 "anthropic-version": "2023-06-01",
                 "x-api-key": api_key}
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            result["http_status"] = r.status
            body = json.loads(r.read().decode("utf-8"))
            result["raw_text"] = body["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        result["http_status"]     = e.code
        result["http_error_body"] = e.read().decode("utf-8", errors="replace")
        result["error_category"]  = f"http_{e.code}"
        result["error_detail"]    = str(e)
        if e.code == 401:
            print("  HTTP 401 — key rejected. Create fresh key at console.anthropic.com")
            print("  Confirm billing is active. Do not reuse keys from screenshots.")
        elif e.code == 429:
            print("  HTTP 429 — rate limit. Wait 60s and retry.")
        elif e.code == 404:
            print(f"  HTTP 404 — model not found: {MODEL}")
        return result
    except Exception as e:
        result["error_category"] = type(e).__name__
        result["error_detail"]   = str(e)
        return result

    parsed, method, failure = extract_json(result["raw_text"])
    result["extraction_method"]  = method
    result["extraction_failure"] = failure
    if parsed is None:
        result["error_category"] = "json_parse_failure"
        result["error_detail"]   = failure
        return result
    result["parsed_output"]     = parsed
    result["normalized_output"] = normalize_output(parsed)
    return result

TC = [
 {"id":"TC-01","sig":"PASS","idea":"جهاز يقيس درجة حرارة الثلاجة كل 5 دقائق ويرسل تنبيهاً للهاتف عبر WiFi إذا تجاوزت 8 درجات","problem":"تلف الطعام بسبب ارتفاع الحرارة","solution":"حساس DHT22 متصل بـ ESP32 يرسل تنبيه عبر WiFi لتطبيق Blynk","beneficiary":"أصحاب المنازل والمطاعم","domain":"IoT منزلي، حساسات حرارة","exp_conf":["MEDIUM","HIGH"],"exp_sig":["APPEARS_FEASIBLE","APPEARS_FEASIBLE_WITH_CAVEATS"],"exp_gaps":False},
 {"id":"TC-02","sig":"PASS","idea":"جهاز يراقب استهلاك الكهرباء لكل جهاز في المنزل ويعرضه على لوحة تحكم","problem":"فواتير الكهرباء مرتفعة دون معرفة المصدر","solution":"حساسات تيار على كل مقبس، ESP32، dashboard على الويب","beneficiary":"ملاك المنازل","domain":"إلكترونيات، قياس طاقة، IoT","exp_conf":["MEDIUM"],"exp_sig":["APPEARS_FEASIBLE","APPEARS_FEASIBLE_WITH_CAVEATS"],"exp_gaps":False},
 {"id":"TC-03","sig":"PASS","idea":"سقاية نباتات آلية تعمل بالبطارية تقيس رطوبة التربة وتفتح صمام الماء عند الجفاف","problem":"نسيان سقي النباتات أثناء السفر","solution":"حساس رطوبة تربة + Arduino + صمام كهربائي + بطارية 9V","beneficiary":"محبو النباتات","domain":"إلكترونيات، أتمتة، زراعة","exp_conf":["MEDIUM","HIGH"],"exp_sig":["APPEARS_FEASIBLE"],"exp_gaps":False},
 {"id":"TC-04","sig":"PASS","idea":"جهاز تتبع GPS للدراجات يرسل موقعها كل دقيقة لتطبيق الهاتف","problem":"سرقة الدراجات شائعة","solution":"وحدة GPS SIM808 + SIM card + بطارية قابلة للشحن + تطبيق موبايل","beneficiary":"أصحاب الدراجات","domain":"IoT، GPS، GSM","exp_conf":["MEDIUM"],"exp_sig":["APPEARS_FEASIBLE","APPEARS_FEASIBLE_WITH_CAVEATS"],"exp_gaps":False},
 {"id":"TC-05","sig":"PASS","idea":"نظام إنذار مبكر لتسرب الغاز في المطابخ يصدر صوتاً وينبه الهاتف","problem":"تسربات الغاز خطيرة وتحدث دون إنذار","solution":"حساس MQ-2 + ESP8266 + buzzer + إشعار WiFi","beneficiary":"أصحاب المنازل والفنادق","domain":"إلكترونيات، سلامة، IoT","exp_conf":["MEDIUM","HIGH"],"exp_sig":["APPEARS_FEASIBLE","APPEARS_FEASIBLE_WITH_CAVEATS"],"exp_gaps":False},
 {"id":"TC-06","sig":"PASS","idea":"جهاز مراقبة نوم الأطفال يقيس درجة الحرارة والرطوبة في الغرفة","problem":"بيئة النوم غير المناسبة تؤثر على جودة نوم الطفل","solution":"حساس SHT31 + ESP32 + تطبيق موبايل + شحن USB","beneficiary":"الأهل حديثو الولادة","domain":"IoT، حساسات بيئية","exp_conf":["MEDIUM"],"exp_sig":["APPEARS_FEASIBLE","APPEARS_FEASIBLE_WITH_CAVEATS"],"exp_gaps":False},
 {"id":"TC-07","sig":"PASS","idea":"جهاز يحسب عدد الأشخاص الداخلين والخارجين من محل تجاري","problem":"أصحاب المحلات لا يعرفون حركة العملاء","solution":"حساسا PIR عند الباب + ESP32 + شاشة LCD + dashboard","beneficiary":"أصحاب المحلات الصغيرة","domain":"إلكترونيات، حساسات، بيانات","exp_conf":["MEDIUM"],"exp_sig":["APPEARS_FEASIBLE","APPEARS_FEASIBLE_WITH_CAVEATS"],"exp_gaps":False},
 {"id":"TC-08","sig":"PASS","idea":"مقياس جودة هواء محمول يعرض مستوى CO2 والغبار على شاشة OLED","problem":"جودة الهواء الداخلي تؤثر على التركيز والصحة","solution":"حساس CO2 SCD40 + حساس غبار PMS5003 + Arduino Nano + OLED","beneficiary":"موظفون وطلاب","domain":"إلكترونيات، حساسات، جودة هواء","exp_conf":["MEDIUM","HIGH"],"exp_sig":["APPEARS_FEASIBLE"],"exp_gaps":False},
 {"id":"TC-09","sig":"WARN","idea":"روبوت صغير يتحرك داخل أنابيب المنازل ويكتشف التسربات","problem":"التسربات تُكتشف متأخرة","solution":"روبوت مع كاميرا وحساسات","beneficiary":"أصحاب المنازل","domain":"روبوتيات، إلكترونيات","exp_conf":["LOW","MEDIUM"],"exp_sig":["SIGNIFICANT_CONCERNS_IDENTIFIED","FEASIBILITY_UNCLEAR"],"exp_gaps":True},
 {"id":"TC-10","sig":"WARN","idea":"جهاز يراقب صحة الأغنام عن بُعد ويرسل تنبيهات عند المرض","problem":"الأمراض تنتشر في القطعان قبل اكتشافها","solution":"جهاز على الرقبة مع حساسات وLoRa","beneficiary":"أصحاب المزارع","domain":"IoT، زراعة، LoRaWAN","exp_conf":["LOW","MEDIUM"],"exp_sig":["FEASIBILITY_UNCLEAR","SIGNIFICANT_CONCERNS_IDENTIFIED"],"exp_gaps":True},
 {"id":"TC-11","sig":"WARN","idea":"نظام ري ذكي للمزارع الكبيرة يعمل بالطاقة الشمسية ويتحكم في 50 صمام","problem":"هدر المياه في الري التقليدي","solution":"حساسات تربة + LoRa + لوح شمسي + تحكم مركزي","beneficiary":"المزارعون","domain":"IoT زراعي، طاقة شمسية، LoRaWAN","exp_conf":["MEDIUM"],"exp_sig":["APPEARS_FEASIBLE_WITH_CAVEATS","FEASIBILITY_UNCLEAR"],"exp_gaps":False},
 {"id":"TC-12","sig":"WARN","idea":"جهاز طبي منزلي يقيس ضغط الدم والسكر وSPO2 ويرسلها للطبيب","problem":"المرضى المزمنون لا يتابعون قراءاتهم","solution":"أجهزة قياس متكاملة + Bluetooth + تطبيق + اتصال بالطبيب","beneficiary":"مرضى الضغط والسكر","domain":"أجهزة طبية، IoT، Bluetooth","exp_conf":["LOW"],"exp_sig":["FEASIBILITY_UNCLEAR","SIGNIFICANT_CONCERNS_IDENTIFIED"],"exp_gaps":True},
 {"id":"TC-13","sig":"WARN","idea":"صندوق توصيل ذكي يحافظ على حرارة الطعام ولا يفتح إلا بكود OTP","problem":"الطعام يبرد أثناء التوصيل","solution":"صندوق معزول + عنصر تسخين + قفل إلكتروني + OTP عبر SMS","beneficiary":"شركات توصيل الطعام","domain":"إلكترونيات، ميكانيكا، IoT","exp_conf":["MEDIUM"],"exp_sig":["APPEARS_FEASIBLE_WITH_CAVEATS"],"exp_gaps":False},
 {"id":"TC-14","sig":"WARN","idea":"جهاز يكتشف النعاس عند السائق ويصدر تنبيهاً صوتياً","problem":"النعاس أثناء القيادة يسبب حوادث","solution":"كاميرا تراقب العينين + معالج + تنبيه صوتي","beneficiary":"السائقون","domain":"Computer Vision، إلكترونيات، سلامة","exp_conf":["LOW","MEDIUM"],"exp_sig":["SIGNIFICANT_CONCERNS_IDENTIFIED","FEASIBILITY_UNCLEAR"],"exp_gaps":True},
 {"id":"TC-15","sig":"WARN","idea":"نظام مراقبة جودة الماء في الخزانات المنزلية","problem":"تلوث الماء لا يُكتشف بالعين","solution":"حساسات pH وعكارة وكلور + ESP32 + تنبيه للهاتف","beneficiary":"أصحاب المنازل","domain":"حساسات كيميائية، IoT","exp_conf":["MEDIUM"],"exp_sig":["APPEARS_FEASIBLE_WITH_CAVEATS"],"exp_gaps":False},
 {"id":"TC-16","sig":"WARN","idea":"جهاز يترجم لغة الإشارة إلى نص عبر قفازات بها حساسات","problem":"التواصل بين الصم والمجتمع صعب","solution":"قفازات بحساسات flex وIMU + Bluetooth + تطبيق يترجم","beneficiary":"الصم","domain":"حساسات، Bluetooth، ML","exp_conf":["LOW"],"exp_sig":["SIGNIFICANT_CONCERNS_IDENTIFIED"],"exp_gaps":True},
 {"id":"TC-17","sig":"BLOCK","idea":"جهاز يعالج السرطان بالموجات الكهرومغناطيسية في المنزل","problem":"العلاج الكيميائي مكلف","solution":"جهاز يبث موجات على المنطقة المصابة","beneficiary":"مرضى السرطان","domain":"طبي، إلكترونيات","exp_conf":["LOW"],"exp_sig":["SIGNIFICANT_CONCERNS_IDENTIFIED","FEASIBILITY_UNCLEAR"],"exp_gaps":True},
 {"id":"TC-18","sig":"BLOCK","idea":"شيء إلكتروني مفيد","problem":"مشكلة","solution":"حل تقني","beneficiary":"الناس","domain":"إلكترونيات","exp_conf":["LOW"],"exp_sig":["INSUFFICIENT_INPUT"],"exp_gaps":True},
 {"id":"TC-19","sig":"BLOCK","idea":"جهاز يولد طاقة كهربائية من هواء الغرفة بكميات تكفي لشحن الهاتف","problem":"نقص مصادر الطاقة","solution":"جمع الطاقة من الهواء المحيط","beneficiary":"الجميع","domain":"طاقة، إلكترونيات","exp_conf":["LOW"],"exp_sig":["SIGNIFICANT_CONCERNS_IDENTIFIED"],"exp_gaps":False},
 {"id":"TC-20","sig":"BLOCK","idea":"جهاز إلكتروني لمنع الزلازل","problem":"الزلازل تسبب خسائر فادحة","solution":"جهاز يبث إشارات تمنع حدوث الزلزال","beneficiary":"سكان المناطق الزلزالية","domain":"إلكترونيات، جيولوجيا","exp_conf":["LOW"],"exp_sig":["SIGNIFICANT_CONCERNS_IDENTIFIED"],"exp_gaps":False},
 {"id":"TC-A2","sig":"WARN","idea":"جهاز يعمل بالبطارية لمدة سنة كاملة ويبث WiFi كل ثانية","problem":"انقطاع الاتصال المتكرر","solution":"بطارية عالية الكثافة مع WiFi مستمر","beneficiary":"المستخدمون الصناعيون","domain":"IoT، WiFi، طاقة","exp_conf":["LOW","MEDIUM"],"exp_sig":["SIGNIFICANT_CONCERNS_IDENTIFIED","FEASIBILITY_UNCLEAR"],"exp_gaps":False,"adversarial":"contradiction"},
 {"id":"TC-A4","sig":"WARN","idea":"فكرتي ممتازة وناجحة بالتأكيد، أحتاج تأكيداً فقط. الجهاز يستخدم ESP32 وLoRa ويراقب درجة حرارة المستودعات","problem":"لا توجد مشكلة واضحة","solution":"ESP32 + LoRa","beneficiary":"غير محدد","domain":"IoT","exp_conf":["LOW","MEDIUM"],"exp_sig":["FEASIBILITY_UNCLEAR","INSUFFICIENT_INPUT"],"exp_gaps":True,"adversarial":"no_validation"},
  {"id":"TC-23","sig":"DIAGNOSTIC","idea":"short idea","problem":"short problem","solution":"","beneficiary":"","domain":"GENERAL","exp_conf":["HIGH"],"exp_sig":["APPEARS_FEASIBLE"],"exp_gaps":False},
  {"id":"TC-24","sig":"DIAGNOSTIC","idea":"task management app simple interface","problem":"people forget tasks lack simple tools","solution":"","beneficiary":"","domain":"GENERAL","exp_conf":["MEDIUM"],"exp_sig":["APPEARS_FEASIBLE"],"exp_gaps":False},
  {"id":"TC-25","sig":"DIAGNOSTIC","idea":"specialized learning platform Arab beginners","problem":"no high quality Arabic learning platform for beginners","solution":"","beneficiary":"","domain":"GENERAL","exp_conf":["LOW"],"exp_sig":["APPEARS_FEASIBLE"],"exp_gaps":True}
]

def c1_schema(out, tc):
    iss = []
    for f in REQUIRED_FIELDS:
        if f not in out: iss.append(f"MISSING_FIELD:{f}")
    if out.get("schema_version") != SCHEMA_VERSION:
        iss.append(f"WRONG_SCHEMA_VERSION:got={out.get('schema_version')}")
    if out.get("domain") != "IOT_ELECTRONICS":
        iss.append(f"WRONG_DOMAIN:got={out.get('domain')}")
    return not iss, iss

def c2_no_invented(out, tc):
    iss = []
    for comp in out.get("observations",{}).get("apparent_components_ar",[]):
        if not comp.get("basis_ar"): iss.append(f"COMPONENT_NO_BASIS:{comp.get('component_ar','?')[:30]}")
    if not out.get("feasibility",{}).get("signal_basis_ar"): iss.append("MISSING:feasibility.signal_basis_ar")
    return not iss, iss

def c3_missing_info(out, tc):
    iss = []
    mi = out.get("missing_information",{})
    if tc.get("exp_gaps") and not mi.get("has_critical_gaps"): iss.append("EXPECTED_CRITICAL_GAPS:got=False")
    GENERIC = ["أضف تفاصيل","يرجى التوضيح","تفاصيل أكثر","معلومات إضافية"]
    for i, item in enumerate(mi.get("items",[])):
        how = item.get("how_to_provide_ar","").strip()
        if not how: iss.append(f"ITEM[{i}]:MISSING:how_to_provide_ar")
        elif any(g in how for g in GENERIC) and len(how)<40: iss.append(f"ITEM[{i}]:GENERIC_GUIDANCE")
        if not item.get("why_it_matters_ar"): iss.append(f"ITEM[{i}]:MISSING:why_it_matters_ar")
    return not iss, iss

def c4_confidence(out, tc):
    iss = []
    conf = out.get("input_assessment",{}).get("confidence_level")
    exp = tc.get("exp_conf",[])
    if exp and conf not in exp: iss.append(f"CONFIDENCE:got={conf},expected={exp}")
    return not iss, iss

def c5_groundedness(out, tc):
    iss = []
    f = out.get("feasibility",{})
    if f.get("assessment_possible") and not f.get("signal_basis_ar"): iss.append("SIGNAL_WITHOUT_BASIS")
    for i, c in enumerate(out.get("identified_concerns",{}).get("items",[])):
        if not c.get("basis_ar"): iss.append(f"CONCERN[{i}]:MISSING:basis_ar")
    return not iss, iss

def c6_gate_utility(out, tc):
    iss = []
    VALID = {"APPEARS_FEASIBLE","APPEARS_FEASIBLE_WITH_CAVEATS","FEASIBILITY_UNCLEAR",
             "SIGNIFICANT_CONCERNS_IDENTIFIED","INSUFFICIENT_INPUT"}
    sig = out.get("feasibility",{}).get("feasibility_signal","")
    if sig not in VALID: iss.append(f"INVALID_SIGNAL:got={sig}")
    raw = json.dumps(out, ensure_ascii=False)
    for w in ["PASS","WARN","BLOCK"]:
        if f'"{w}"' in raw: iss.append(f"FORBIDDEN_GATE_WORD:{w}")
    if not out.get("disclaimer_ar"): iss.append("MISSING:disclaimer_ar")
    return not iss, iss

def c7_restraint(out, tc):
    iss = []
    conf = out.get("input_assessment",{}).get("confidence_level")
    sig  = out.get("feasibility",{}).get("feasibility_signal")
    exp  = tc.get("exp_sig",[])
    if tc["id"]=="TC-18" and conf=="HIGH": iss.append("OVERCONFIDENT_ON_EMPTY_INPUT")
    if exp and sig not in exp: iss.append(f"SIGNAL:got={sig},expected={exp}")
    adv = tc.get("adversarial")
    if adv=="contradiction" and not out.get("identified_concerns",{}).get("has_concerns"):
        iss.append("CONTRADICTION_NOT_DETECTED")
    if adv=="no_validation" and sig=="APPEARS_FEASIBLE":
        iss.append("UNWARRANTED_POSITIVE_SIGNAL")
    return not iss, iss

CRITERIA = [
    ("Schema Compliance",       c1_schema,        18),
    ("No Invented Info",        c2_no_invented,   18),
    ("Missing Info + Recovery", c3_missing_info,  14),
    ("Confidence Calibration",  c4_confidence,    14),
    ("Groundedness",            c5_groundedness,  14),
    ("Gate Engine Utility",     c6_gate_utility,   9),
    ("Restraint Check",         c7_restraint,     13),
]
assert sum(w for _,_,w in CRITERIA) == 100

def run():
    api_key = get_api_key()
    print("="*65)
    print("BENCHMARK v1.0 — IoT + Electronics  [runner v1.1]")
    print(f"Model: {MODEL}  |  Cases: {len(TC)}")
    print(f"Started: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print("="*65)

    results = []
    for tc in TC:
        print(f"\n[{tc['id']}] {tc['sig']} — {tc['idea'][:52]}...")
        api_result = call_claude(tc, api_key)

        rec = {
            "id": tc["id"], "sig": tc["sig"],
            "http_status":        api_result["http_status"],
            "http_error_body":    api_result["http_error_body"],
            "raw_text":           api_result["raw_text"],
            "extraction_method":  api_result["extraction_method"],
            "extraction_failure": api_result["extraction_failure"],
            "parsed_output":      api_result["parsed_output"],
            "normalized_output":  api_result["normalized_output"],
            "error_category":     api_result["error_category"],
            "error_detail":       api_result["error_detail"],
            "error":              api_result["parsed_output"] is None,
            "scores": {}, "weighted_score": 0, "overall": False,
        }

        if api_result["parsed_output"] is None:
            cat    = api_result["error_category"] or "unknown"
            method = api_result["extraction_method"] or "none"
            detail = api_result["error_detail"] or api_result["http_error_body"] or "no detail"
            print(f"  ERROR category={cat} extraction={method}")
            print(f"    detail: {str(detail)[:200]}")
            raw = api_result["raw_text"]
            if raw:
                print(f"    raw_text[0:300]: {raw[:300].replace(chr(10),' ')}")
            else:
                print(f"    raw_text: None")
            results.append(rec)
            time.sleep(2)
            continue

        out    = api_result["normalized_output"]
        method = api_result["extraction_method"]
        print(f"  extraction={method} http={api_result['http_status']}")

        weighted = 0
        for name, fn, weight in CRITERIA:
            passed, iss = fn(out, tc)
            rec["scores"][name] = {"passed": passed, "weight": weight, "issues": iss}
            if passed: weighted += weight
            print(f"  {'✓' if passed else '✗'} {name}" + (f" — {iss[0]}" if iss else ""))
        rec["weighted_score"] = weighted
        rec["overall"] = all(rec["scores"][n]["passed"] for n,_,_ in CRITERIA)
        results.append(rec)
        time.sleep(1.5)

    print("\n"+"="*65+"\nSUMMARY\n"+"="*65)
    errors = [r for r in results if r["error"]]
    valid  = [r for r in results if not r["error"]]
    n = len(valid)

    if errors:
        from collections import Counter
        cats = Counter(r.get("error_category","unknown") for r in errors)
        print(f"\nERRORS: {len(errors)}/{len(results)}")
        for cat, count in cats.most_common():
            print(f"  {cat}: {count}")

    cstats = {name: sum(1 for r in valid if r["scores"].get(name,{}).get("passed"))
              for name,_,_ in CRITERIA}
    overall_pass = sum(1 for r in valid if r.get("overall"))
    avg_weighted = sum(r.get("weighted_score",0) for r in valid) // max(n,1)

    print(f"\nValid: {n}/{len(results)}  |  All-criteria pass: {overall_pass}/{n}  |  Avg weighted: {avg_weighted}/100\n")
    for name, _, weight in CRITERIA:
        p = cstats[name]; pct = 100*p//max(n,1)
        print(f"  {name:<26} {'█'*(pct//5)+'░'*(20-pct//5)} {pct:3d}%  (w={weight})")

    sc      = 100*cstats["Schema Compliance"]//max(n,1)
    res     = 100*cstats["Restraint Check"]//max(n,1)
    rec_pct = 100*cstats["Missing Info + Recovery"]//max(n,1)
    verdict = sc >= 90 and res >= 85

    print(f"\nSchema: {sc}%  Restraint: {res}%  Recovery: {rec_pct}%")
    print("✓ PASSED" if verdict else "✗ FAILED — see results file")

    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(os.path.dirname(__file__), f"results_{ts}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {
                "runner_version": "1.1",
                "model":          MODEL,
                "schema_version": SCHEMA_VERSION,
                "timestamp":      ts,
                "total":          len(results),
                "valid":          n,
                "errors":         len(errors),
                "schema_pct":     sc,
                "restraint_pct":  res,
                "recovery_pct":   rec_pct,
                "avg_weighted":   avg_weighted,
                "passed":         verdict,
            },
            "cases": results
        }, f, ensure_ascii=False, indent=2)
    print(f"Saved: {path}")

if __name__ == "__main__":
    run()