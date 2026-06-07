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

app = Flask(__name__)
app.secret_key = "inventorai-dev-only"
SESSION_STORE = {}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    idea_text = request.form.get("idea", "").strip()
    if not idea_text:
        return redirect(url_for("index"))
    domain = infer_domain(idea_text)
    if not domain:
        return render_template("index.html", error="Domain not recognized. Please describe an electronics, mechanical, medical, or software invention.")
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = domain
    state.domain_signal = domain
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
        question = get_question(state.domain, gap_type, iterations_open)
    elif (
        state.maturity_level == 0
        and len(state.gaps) == 0
        and last_result is not None
        and last_result.get("transition") == "WARN"
        and "not yet established" in (last_result.get("reason") or "")
    ):
        question = INTAKE_QUESTION
    open_gaps = [g for g in state.gaps if g.status == "OPEN"]
    closed_gaps = [g for g in state.gaps if g.status == "CLOSED"]
    gap_labels = {g.gap_type: GAP_LABELS.get(g.gap_type, GAP_LABELS["__default__"]) for g in state.gaps}
    current_gap_label = GAP_LABELS.get(gap_type, GAP_LABELS["__default__"]) if gap_type else None
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
    # Transcript capture: store the question computed in GET
    # so POST handler can record it with the response.
    # No engine effect. Evidence preservation only.
    if entry is not None and question is not None:
        entry["last_question"] = question

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
        entry["transcript"].append({
            "iteration": state.iteration,
            "question":  entry.get("last_question", ""),
            "response":  response,
        })
        import sys
        for g in state.gaps:
                    pass
    return redirect(url_for("show_session", sid=sid))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
