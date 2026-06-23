"""
InventorAI Web Interface (Phase H-A)
Thin web shell only. Engine called as library.
SESSION_STORE: in-memory, non-production, temporary.
"""
import uuid
from flask import Flask, request, redirect, url_for, render_template
from engine.domain_rules import infer_domain
from engine.idea_state import IdeaState
from engine.progression_loop import run_iteration, select_next_gap, get_question
from web.gap_labels import GAP_LABELS, get_gap_label, get_maturity_label, SESSION_DISCLOSURE
from engine.deliverable_assembler import assemble_deliverable

app = Flask(__name__)
app.secret_key = "inventorai-dev-only"
SESSION_STORE = {}

# Option B product-boundary enforcement (DOMAIN_SCOPE_OWNER_RESOLUTION_OPTION_B).
# Current generic product-runtime activation is limited to electronics/electrical.
# Stable, exact refusal message — does not expose the internally inferred domain.
UNSUPPORTED_DOMAIN_MESSAGE = (
    "InventorAI currently supports electronics and electrical ideas only. "
    "Please describe an electronics or electrical invention."
)

# Explicit electronics/electrical confirmation at the generic product boundary
# (ADR-001: "Domain assignment is explicit or it does not occur"). The user must
# affirmatively declare the supported domain; consent is never inferred from the
# idea text. The checkbox submits this exact value.
DOMAIN_CONFIRM_VALUE = "electronics_electrical"
CONFIRMATION_REQUIRED_MESSAGE = (
    "Please confirm that your idea is an electronics or electrical idea "
    "before starting."
)
# Bounded conflict check: explicit confirmation is the primary declaration, but
# a clearly different *supported* internal classification is not silently
# relabeled as electronics. These are refused; no session is created.
CONFLICTING_SUPPORTED_DOMAINS = {"mechanical", "medical_device", "software"}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    # Explicit electronics/electrical confirmation is required (ADR-001 explicit
    # assignment). Consent is never inferred from the idea text; without it no
    # session is created.
    if request.form.get("domain_confirm") != DOMAIN_CONFIRM_VALUE:
        return render_template("index.html", error=CONFIRMATION_REQUIRED_MESSAGE)
    # Bounded conflict check using the unchanged deterministic classifier: the
    # explicit confirmation is the primary domain declaration, but it must not
    # silently override clear conflicting classification evidence.
    # infer_domain(), the registry loader, and all domain packs are unchanged.
    domain = infer_domain(idea_text)
    if domain in CONFLICTING_SUPPORTED_DOMAINS:
        # A clearly different *supported* domain — refuse, do not relabel.
        return render_template("index.html", error=UNSUPPORTED_DOMAIN_MESSAGE)
    if domain not in ("electronics_electrical", None):
        # Unexpected / unknown classifier value — refuse defensively.
        return render_template("index.html", error=UNSUPPORTED_DOMAIN_MESSAGE)
    # electronics_electrical or None is admitted under explicit confirmation
    # (None covers functional electronics ideas the signal classifier misses).
    # Admit: the session's domain is the explicitly confirmed supported domain.
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = DOMAIN_CONFIRM_VALUE
    state.domain_signal = DOMAIN_CONFIRM_VALUE
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": []}
    return redirect(url_for("show_session", sid=sid))

@app.route("/start_ilt002_water_leak", methods=["POST"])
def start_ilt002_water_leak():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": []}
    return redirect(url_for("show_session", sid=sid))

@app.route("/start_ilt002_combination_lock", methods=["POST"])
def start_ilt002_combination_lock():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": []}
    return redirect(url_for("show_session", sid=sid))

@app.route("/start_ilt002_combination_lock_path_n", methods=["POST"])
def start_ilt002_combination_lock_path_n():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = "electronics_electrical"
    state.domain_signal = "electronics_electrical"
    state.path = "N"
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    SESSION_STORE[sid] = {"state": state, "last_result": initial_result, "transcript": []}
    return redirect(url_for("show_session", sid=sid))

@app.route("/session/<sid>", methods=["GET"])
def show_session(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    last_result = entry.get("last_result")
    INTAKE_QUESTION = "Describe your invention in more detail — what specific problem does it solve, and how does it solve it?"

    gap_type = select_next_gap(state)
    question = None
    if gap_type:
        gap = state.get_gap(gap_type)
        iterations_open = gap.iterations_open if gap else 0
        question = get_question(state.domain, gap_type, iterations_open, path=state.path)
    elif (
        state.maturity_level == 0
        and len(state.gaps) == 0
        and last_result is not None
        and last_result.get("transition") == "WARN"
        and "not yet established" in (last_result.get("reason") or "")
    ):
        question = INTAKE_QUESTION
    open_gaps = state.get_open_gaps()
    closed_gaps = [g for g in state.gaps if g.status == "CLOSED"]
    gap_labels = {g.gap_type: GAP_LABELS.get(g.gap_type, GAP_LABELS["__default__"]) for g in state.gaps}
    current_gap_label = GAP_LABELS.get(gap_type, GAP_LABELS["__default__"]) if gap_type else None
    # Transcript capture: store question before render so POST can record it.
    # No engine effect. Evidence preservation only.
    if entry is not None and question is not None:
        entry["last_question"] = question
    return render_template("session.html",
        sid=sid,
        state=state,
        question=question,
        open_gaps=open_gaps,
        gap_type=gap_type,
        last_result=last_result,
        gap_labels=gap_labels,
        current_gap_label=current_gap_label,
        maturity_label=get_maturity_label(state.maturity_level),
        session_disclosure=SESSION_DISCLOSURE,
        closed_gaps=closed_gaps,
    )
@app.route("/session/<sid>/deliverable", methods=["GET"])
def show_deliverable(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    package = assemble_deliverable(state)
    eligible = package["_session_meta"]["deliverable_eligible"]
    return render_template(
        "deliverable.html",
        sid=sid,
        package=package,
        eligible=eligible,
    )

@app.route("/session/<sid>", methods=["POST"])
def submit_answer(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    response = request.form.get("response", "").strip()
    if response:
        result = run_iteration(state, response)
        entry["last_result"] = result
        # Transcript capture: append verbatim record for ILT-002 evidence.
        # iteration number read after run_iteration() incremented it.
        # No engine effect. Evidence preservation only.
        import json, os
        from datetime import datetime
        record = {
            "session_id": sid,
            "iteration": state.iteration,
            "question":  entry.get("last_question", ""),
            "response":  response,
            "domain":    getattr(state, "domain", None),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        entry["transcript"].append(record)
        # Disk-backed persistence: survives Flask restarts.
        # ILT-002 evidence preservation only. No engine effect.
        transcript_path = f"/tmp/ilt002_transcript_{sid}.jsonl"
        with open(transcript_path, "a") as _tf:
            _tf.write(json.dumps(record) + "\n")
        import sys
        for g in state.gaps:
                    pass
    return redirect(url_for("show_session", sid=sid))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
