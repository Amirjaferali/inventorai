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
    SESSION_STORE[sid] = {"state": state, "last_result": None}
    return redirect(url_for("show_session", sid=sid))

@app.route("/session/<sid>", methods=["GET"])
def show_session(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    last_result = entry.get("last_result")
    gap_type = select_next_gap(state)
    question = None
    if gap_type:
        gap = state.get_gap(gap_type)
        iterations_open = gap.iterations_open if gap else 0
        question = get_question(state.domain, gap_type, iterations_open)
    open_gaps = [g for g in state.gaps if g.status == "OPEN"]
    return render_template("session.html",
        sid=sid,
        state=state,
        question=question,
        open_gaps=open_gaps,
        gap_type=gap_type,
        last_result=last_result,
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
    return redirect(url_for("show_session", sid=sid))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
