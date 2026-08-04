"""
InventorAI Web Interface (Phase H-A)
Thin web shell only. Engine called as library.
SESSION_STORE: in-memory, non-production, temporary.
"""
import os
import re
import secrets
import tempfile
import uuid
from flask import Flask, request, redirect, url_for, render_template
from engine.domain_rules import infer_domain
from engine.idea_state import (
    IdeaState, SuccessCriterion,
    CRITICALITY_FEASIBILITY_THREATENING, CRITICALITY_VALUE_ENHANCING,
    CRITICALITY_REFINEMENT, CRITICALITY_ACTION_CONFIRMED,
    CRITICALITY_ACTION_DEFERRED,
)
# Workstream 4 (structured criticality): the same pure landscape derivation
# that feeds Section 13, used read-only to select the confirmation focus.
from engine.requirement_landscape import derive_requirement_landscape
from engine.progression_loop import (
    run_iteration, select_next_gap, get_question, get_display_question,
)
from web.gap_labels import GAP_LABELS, get_gap_label, get_maturity_label, SESSION_DISCLOSURE, friendly_gap_name
from engine.deliverable_assembler import assemble_deliverable
# P4-1b-1 (G-P4-1B-1-DOC-01 / PR #358): the merged P4-1a durable store and the
# P4-0 record contract, used ONLY to durably create and cold-load a NEW project
# envelope keyed by the unified sid==project_id capability. No accepted-input
# append, Keep/Refine durability, transcript/last_result persistence, or replay
# is introduced here (those are P4-1b-2 / P4-2).
from engine.record_store import SqliteRecordStore
from engine.record_contract import ProjectRecordContract
# Increment 3 (R-5): the SAME shared public derivation that feeds the deliverable
# section, imported as a module-level name so one selection feeds both surfaces.
from engine.idea_development_outputs import derive_next_development_step
from web.responsibility_labels import get_responsibility  # Increment 1B: advisory only
from web.clarification_labels import get_clarification  # Increment 1B: display-only clarification
from web.scaffolding_guidance import get_scaffolding_guidance  # MDN: display-only WARN guidance
from web.answer_coauthoring_prompts import get_answer_coauthoring_prompts  # GACA Increment 1: display-only advisory prompts
from web.uncertainty_guidance import get_uncertainty_guidance  # GUS: display-only supportive uncertainty guidance
from web.result_feedback import get_result_feedback  # PLRF: display-only plain-language result feedback

# --- G-SC0 Bounded Security Containment: runtime security configuration -------
# Runtime debug, host, and the Flask secret are environment-controlled with safe
# defaults. No secret value is hard-coded in source. See README "Runtime security
# configuration". No accounts/authentication/authorization are introduced here.
_TRUTHY = frozenset({"1", "true", "yes", "on"})


def _debug_enabled():
    """Debug is OFF unless INVENTORAI_DEBUG is an explicit recognized truthy value.
    Ambiguous or unknown values never enable debug."""
    return os.environ.get("INVENTORAI_DEBUG", "").strip().lower() in _TRUTHY


def _resolve_host():
    """Host defaults to loopback (127.0.0.1); override only via INVENTORAI_HOST."""
    return os.environ.get("INVENTORAI_HOST", "").strip() or "127.0.0.1"


def _is_production():
    return os.environ.get("INVENTORAI_ENV", "").strip().lower() == "production"


def _resolve_secret_key():
    """Return the Flask secret. Sourced from INVENTORAI_SECRET_KEY. When explicit
    production mode is enabled and the secret is missing, fail clearly. For local
    development only, an ephemeral random secret is generated (never persisted or
    logged). No fixed secret value is stored in source."""
    secret = os.environ.get("INVENTORAI_SECRET_KEY", "")
    if secret:
        return secret
    if _is_production():
        raise RuntimeError(
            "INVENTORAI_SECRET_KEY must be set to a non-empty value when "
            "INVENTORAI_ENV=production."
        )
    return secrets.token_hex(32)


app = Flask(__name__)
app.secret_key = _resolve_secret_key()
# Presentation-only Jinja filter: translate an internal gap-type ID to a short
# inventor-friendly label for the few session-page surfaces that render raw
# reference/context IDs. Non-gap values pass through unchanged. Display only.
app.jinja_env.filters["gap_display"] = friendly_gap_name
SESSION_STORE = {}

# --- P4-1b-1: durable project store (construction, configuration, cold-load) --
# The in-memory SESSION_STORE remains the active working state within a live
# process; SQLite is the durable project-envelope mirror and cold-reload source,
# keyed by the unified `sid`==`project_id` pre-account capability. There is NO
# sid->project_id mapping table, no project_ids() scan, and no reversible mapping
# layer. project_ids() is never exposed through any route/API/UI surface. This
# capability is an unguessable lookup only — not authentication, ownership,
# account authorization, or verified identity (Phase 5). No cache framework or
# invalidation platform is introduced.
_STORE = None
# Generic, non-disclosing message for a durable-store failure at /start. It never
# reveals project existence, capability validity, contract state, or DB detail.
SERVICE_UNAVAILABLE_MESSAGE = (
    "This service is temporarily unavailable. Please try again in a moment.")


def _resolve_db_path():
    """Resolve the SQLite database path from INVENTORAI_DB_PATH.

    Explicit env value wins. In explicit production mode a missing value is a
    hard fail (no silent fallback). For local development only, an explicit,
    app-namespaced temp path is used (never a repository-tracked file; the
    envelope carries no verbatim user content — R6 is preserved)."""
    path = os.environ.get("INVENTORAI_DB_PATH", "").strip()
    if path:
        return path
    if _is_production():
        raise RuntimeError(
            "INVENTORAI_DB_PATH must be set to a writable path when "
            "INVENTORAI_ENV=production.")
    return os.path.join(tempfile.gettempdir(), "inventorai_dev",
                        "inventorai_p4_1b1.sqlite")


def _get_store():
    """Return the one application-scoped SqliteRecordStore (single-process MVP),
    building it on first use from the resolved path. Multi-worker topology,
    pooling, per-request connections, WAL tuning, and production datastore
    selection are deferred. Raises on an unusable path (caller fails closed)."""
    global _STORE
    if _STORE is None:
        path = _resolve_db_path()
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        _STORE = SqliteRecordStore(path)
    return _STORE


def _cold_load_entry(sid):
    """P4-1b-1 durable cold-load: rebuild the MINIMUM runtime entry for `sid`
    from the durable project envelope (the `sid` IS the durable `project_id`).

    Returns the minimal entry, or None on any missing/malformed/unsupported/
    unavailable durable state — the caller then falls through to the existing
    generic unavailable behaviour, disclosing nothing. Readiness is re-derived
    by the render path from the reconstructed ledger; transcript and cached
    last_result are NOT restored as authoritative. No mapping lookup or
    project_ids() scan is used."""
    try:
        contract = _get_store().load_contract(sid)   # scoped by sid==project_id
        state = contract.to_state()
    except Exception:
        # Fail closed. Storage/contract errors are translated to the generic
        # unavailable behaviour at this web boundary; no user content is logged.
        return None
    return {"state": state, "last_result": None, "transcript": []}


# Production fail-fast (mirrors the R16 secret-key policy): in explicit
# production mode the durable store must be constructable at startup — a missing
# or unusable INVENTORAI_DB_PATH makes the app refuse to start rather than
# silently degrade per request. Local/development stays lazy so tests and dev
# runs are unaffected (no eager database file is created outside production).
if _is_production():
    _get_store()

# --- Increment 1A: structured owner actions (conformance correction) ---------
# Non-specialist owners respond through explicit, structured actions instead of
# being forced to invent technical prose. ONLY `answered` enters the existing
# assessment path (run_iteration -> assess/integrate/transition); its behavior
# and the ILT-002 transcript record are unchanged. The five non-answer actions
# still never assess, score, close or alter a gap, advance maturity, satisfy a
# transition gate, or create an evidence record, and the SESSION_STORE entry
# keeps its additive in-memory display metadata.
#
# --- Increment 2: durable, truthful disposition records -----------------------
# In addition (Increment 2 truthful-state correction), every owner action now
# also appends a durable in-memory record to the IdeaState interaction ledger
# (state.record_interaction). This ledger is NOT progression state: it does not
# assess, score, advance maturity, alter the gap lifecycle, satisfy a gate, or
# create Evidence; it carries the truthful provenance/validation/disposition of
# what the owner did. It remains persistence-independent — no durable persistence
# is used, the transcript schema is untouched, and the frozen engine.session_store
# is never imported.
ACTION_ANSWERED = "answered"
INTERACTION_ACTIONS = {
    ACTION_ANSWERED,
    "unknown",
    "deferred",
    "provisional_assumption",
    "specialist_requested",
    "evidence_requested",
}
# Honest, non-progress acknowledgements for the five non-answer actions. None of
# these implies the question is resolved, verified, or answered.
_NON_ANSWER_ACK = {
    "unknown": "Recorded that you do not know this yet. It is kept as an open unknown and does not resolve the question.",
    "deferred": "Recorded as deferred. The question remains open and unresolved.",
    "provisional_assumption": "Recorded as a provisional assumption (not verified). It does not resolve the question or count as evidence.",
    "specialist_requested": "Recorded that specialist input is needed. No technical answer has been assumed.",
    "evidence_requested": "Recorded that evidence is needed. No evidence or result has been recorded.",
}
# G-UX-ANSWER-VALIDATION: shown only when the owner chooses to answer but submits
# a whitespace-normalized empty response. Position-neutral; echoes no user content.
ANSWER_REQUIRED_MESSAGE = "Enter an answer, or choose one of the response options below."
# G-UX-SNAPSHOT-DECISION: truthful, temporary-session acknowledgement for the
# "Keep current snapshot" post-output decision. It selects the CURRENT deterministic
# working snapshot for this temporary session only — it does not serialize, duplicate,
# version, persist, approve, or create ownership. Echoes no idea/snapshot content.
KEEP_SNAPSHOT_ACK = (
    "Current working snapshot selected for this temporary session. "
    "It has not been permanently saved or approved."
)

# --- Workstream 4: structured criticality confirmation flow -------------------
# (docs/governance/STRUCTURED_CRITICALITY_CAPTURE_INCREMENT_CONTRACT.md §7;
# owner GREEN authorization.) A lightweight, summary-first step on the existing
# completion-stage session surface — no new route. One contextually supported
# requirement at a time (grouped confirmation is NOT implemented, per the
# owner's deliberate minimum-risk restriction). The server re-derives the
# current focus from authoritative session state on every request and never
# trusts a browser-supplied target: stale, mismatched, or manipulated
# submissions are rejected with NOTHING stored. All inventor-facing wording is
# plain language — no raw category, authority, provenance, or requirement-id
# token ever renders.
import hashlib as _crit_hashlib

CRITICALITY_SUMMARY_LEAD = "This is what I understood from your explanation:"
CRITICALITY_CLARIFICATION = (
    "Would the idea still achieve its purpose if this part changed?")
# Exact owner-mandated plain-language choices and their internal mapping. The
# mapping happens server-side only; the raw category never reaches the page.
CRITICALITY_CHOICES = (
    ("essential",  "The idea may not work without this"),
    ("value",      "The idea would still work, but this adds important value"),
    ("refinement", "This mainly improves or refines the idea"),
    ("unsure",     "I am not sure yet"),
)
_CRITICALITY_CHOICE_CATEGORY = {
    "essential":  CRITICALITY_FEASIBILITY_THREATENING,
    "value":      CRITICALITY_VALUE_ENHANCING,
    "refinement": CRITICALITY_REFINEMENT,
}
# Exact owner-mandated five lightweight actions (contract §7.2).
CRITICALITY_SUMMARY_ACTIONS = (
    ("summary_correct", "Yes, that is correct"),
    ("summary_change",  "Change this part"),
    ("summary_missing", "Something is missing"),
    ("summary_unsure",  "I am not sure yet"),
    ("summary_later",   "Decide later"),
)
_CRITICALITY_SUMMARY_VALUES = {v for v, _ in CRITICALITY_SUMMARY_ACTIONS}


def _criticality_focus(state):
    """The single current focus: the first landscape requirement, in the
    stable derivation order, that (a) has understanding context — its primary
    anchor is an inventor ledger record with verbatim content — and (b) has
    no recorded confirmation/deferral yet. Requirements without understanding
    context are never offered for classification (contract §7.1): they keep
    the untouched never-interacted default."""
    landscape = derive_requirement_landscape(state)
    for req in landscape.requirements:
        if state.current_criticality_confirmation(req.requirement_id):
            continue
        if req.primary_anchor.anchor_kind != "assertion":
            continue
        record = next(
            (a for a in state.assertions
             if a.record_id == req.primary_anchor.anchor_reference), None)
        if record is not None and (record.content or "").strip():
            return req, record
    return None, None


def _criticality_focus_token(sid, requirement_id):
    """Opaque per-focus token: lets the server detect a submission rendered
    against a different (stale) focus without ever exposing the raw
    requirement id in the page."""
    digest = _crit_hashlib.sha256(
        ("ws4:" + sid + ":" + requirement_id).encode("utf-8")).hexdigest()
    return digest[:16]


def _criticality_step_context(entry, state, sid):
    """Read-only render context for the completion-stage block, or None when
    the step does not apply (journey not complete, or no contextually
    supported unconfirmed requirement remains). Mutates nothing."""
    if state.maturity_level < 2 or state.get_open_gaps():
        return None
    if entry.get("criticality_correction"):
        return {"stage": "correction"}
    req, record = _criticality_focus(state)
    if req is None:
        return None
    stage_state = entry.get("criticality_stage") or {}
    stage = ("clarify"
             if stage_state.get("requirement_id") == req.requirement_id
             else "summary")
    return {
        "stage": stage,
        "summary_lead": CRITICALITY_SUMMARY_LEAD,
        "statement": req.statement,
        "you_said": record.content,
        "clarification": CRITICALITY_CLARIFICATION,
        "choices": CRITICALITY_CHOICES,
        "summary_actions": CRITICALITY_SUMMARY_ACTIONS,
        "proposed_rationale": record.content,
        "focus_token": _criticality_focus_token(sid, req.requirement_id),
    }


def _handle_criticality_action(entry, state, sid):
    """POST branch for the structured criticality actions. Never calls
    run_iteration; never touches gaps, maturity, the ledger, the transcript,
    scoring, or any unrelated state. Every rejection returns HTTP 400 with
    NOTHING stored."""
    def _reject():
        return ("This confirmation step is no longer current. "
                "No change was made.", 400)

    crit_action = (request.form.get("criticality_action") or "").strip()
    # Server-side focus protection (owner rule 5): re-derive the authoritative
    # focus and require the rendered token to match it.
    req, record = _criticality_focus(state)
    if req is None:
        return _reject()
    if request.form.get("focus_token", "") != \
            _criticality_focus_token(sid, req.requirement_id):
        return _reject()

    if crit_action in _CRITICALITY_SUMMARY_VALUES:
        entry.pop("criticality_stage", None)
        if crit_action == "summary_correct":
            # Understanding confirmed — advance to the single clarification.
            # No criticality is stored by this action (no silent adoption).
            entry["criticality_stage"] = {"requirement_id": req.requirement_id}
        elif crit_action in ("summary_unsure", "summary_later"):
            state.record_criticality_confirmation(
                requirement_id=req.requirement_id,
                action=CRITICALITY_ACTION_DEFERRED,
                iteration=state.iteration)
        else:
            # Change this part / Something is missing: store nothing; return
            # the inventor to the existing free-text answer path (owner rule 6).
            entry["criticality_correction"] = True
        return redirect(url_for("show_session", sid=sid))

    if crit_action == "clarify_choice":
        if (entry.get("criticality_stage") or {}).get("requirement_id") \
                != req.requirement_id:
            return _reject()
        choice = (request.form.get("category_choice") or "").strip()
        if choice == "unsure":
            entry.pop("criticality_stage", None)
            state.record_criticality_confirmation(
                requirement_id=req.requirement_id,
                action=CRITICALITY_ACTION_DEFERRED,
                iteration=state.iteration)
            return redirect(url_for("show_session", sid=sid))
        category = _CRITICALITY_CHOICE_CATEGORY.get(choice)
        rationale = request.form.get("rationale", "")
        if category is None or not rationale.strip():
            return _reject()
        source = ("reused_statement:" + record.record_id
                  if rationale == record.content else "inventor_edited")
        try:
            state.record_criticality_confirmation(
                requirement_id=req.requirement_id,
                action=CRITICALITY_ACTION_CONFIRMED, category=category,
                rationale_verbatim=rationale, rationale_source=source,
                iteration=state.iteration)
        except ValueError:
            return _reject()
        entry.pop("criticality_stage", None)
        return redirect(url_for("show_session", sid=sid))

    return _reject()

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

# --- Domain Gate / Entry UX Increment (post-PR #100 Increment Contract) --------
# Bounded ambiguity resolution for the /start domain gate. The problem being
# fixed (see the merged evidence record + Increment Contract §3, §7.C, §10):
# `infer_domain()` matches classification signals as SUBSTRINGS, so ordinary lay
# wording produces spurious *conflicting-supported-domain* classifications that
# the gate then hard-rejects even though the idea is a genuine electronics/
# electrical one and the owner explicitly confirmed that domain — e.g. "app" is a
# substring of "appliance" (-> software), and the generic word "monitoring" ->
# medical_device. This increment lets the explicit confirmation resolve such
# WEAK/ambiguous conflicts, while STRONG unsupported-domain evidence is never
# overridden. It adds NO domain, activates no technology family, changes no
# classifier/registry/domain pack, and makes no safety/feasibility/compliance
# claim. Matching is word/token based (not substring) precisely so that markers
# like "app" cannot fire inside "appliance" and "medical" cannot fire inside
# "medicine".
_TOKEN_RE = re.compile(r"[a-z0-9]+")

# Strong, unambiguous NON-electronics evidence. When present, the idea clearly
# belongs to an unsupported domain (medical / mechanical / software / drone /
# solar / robotics / agriculture); the explicit electronics confirmation must
# NOT override it (Increment Contract §7.C, §10, §15). Matched against word
# tokens. Words that ALSO carry ordinary electronics meanings are deliberately
# EXCLUDED so valid electronics ideas are not rejected (independent-review
# boundary fix): NOT "pulse" (pulse circuits/signals), NOT "algorithm"
# (embedded/electronics control wording), NOT "diagnostic"/"diagnostics"
# (electronics self-diagnostics) — only the medical noun/verb forms
# diagnosis/diagnose/diagnoses/diagnosing are strong.
_STRONG_UNSUPPORTED_WORDS = frozenset({
    # medical_device / health (note: NOT "monitoring" — that is a weak/ambiguous
    # term per §10 — and NOT "medicine")
    "medical", "cardiac", "heart", "blood", "insulin", "glucose",
    "clinical", "surgical", "surgery", "implant", "implantable", "prosthetic",
    "catheter", "stent", "biosensor", "patient", "dementia", "therapeutic",
    "respiratory", "neural", "retinal", "orthopedic",
    "diagnosis", "diagnose", "diagnoses", "diagnosing",
    "hearing", "wearable", "fever", "rehabilitation",
    # mechanical
    "mechanical", "gear", "gearbox", "gearing", "shaft", "bearing", "torque",
    "piston", "pulley", "hydraulic", "crankshaft", "camshaft",
    # software
    "software", "api", "backend", "frontend", "database", "sql",
    # drone / solar / robotics / agriculture (non-activated families, §6/§15)
    "drone", "solar", "crop", "crops", "agriculture", "agricultural",
    "pesticide", "herbicide", "irrigation", "farm", "farms",
    "robot", "robots", "robotic", "robotics",
})
# Strong multi-word markers; matched as substrings of the full text.
_STRONG_UNSUPPORTED_SUBSTRINGS = (
    "machine learning", "neural network", "body temperature",
)

# Lay household-electrical MECHANISM evidence. Presence indicates a genuine
# electrical mechanism written in non-specialist words, so the idea is admitted
# under the explicit confirmation even if the deterministic classifier missed it
# or returned a weak conflicting supported domain (Increment Contract §7.B).
# Deliberately EXCLUDES bare "appliance"/"alert"/"device" (which carry no
# electrical mechanism on their own — see §9.B, which must NOT be admitted).
# "power"/"powers" are matched ONLY as whole word tokens (independent-review
# boundary fix): the previous "power" SUBSTRING marker fired inside unrelated
# words such as "powerful", "empowers", and "hand-powered", falsely admitting
# software-only and mechanical-only ideas. "powered" is deliberately NOT a
# marker because it frequently names a non-electrical energy source
# ("hand-powered", "spring-powered") and carries no electrical mechanism alone.
_LAY_ELECTRICAL_WORDS = frozenset({
    "plug", "socket", "outlet", "switch", "circuit", "wire", "wiring",
    "voltage", "sensor", "sensors", "charger", "chargers", "battery",
    "batteries", "relay", "electric", "electrical", "electronic",
    "electronics", "electricity", "current", "currents", "transistor",
    "microcontroller", "arduino", "esp32", "led", "wifi", "bluetooth",
    "power", "powers",
})

# Bounded medical-conflict corroboration bar (independent-review boundary fix):
# when the unchanged deterministic classifier returns `medical_device`, ONE lay
# electrical token must not flip the conflict toward electronics/electrical
# (Increment Contract §7.C: confirmation helps resolve ambiguity but is not an
# unconditional override). At least TWO distinct lay electrical mechanism words
# are required; otherwise the owner is guided to name the mechanism instead.
_MEDICAL_CONFLICT_LAY_MINIMUM = 2

# User-facing guidance shown when an idea does not yet clearly show an electrical
# mechanism (Increment Contract §7.E). Advisory only: it makes NO validation,
# safety, feasibility, compliance, or build-readiness claim, and does NOT admit
# the idea (no session is created).
MECHANISM_GUIDANCE_MESSAGE = (
    "InventorAI currently supports electronics and electrical ideas only. Your "
    "description does not yet clearly show the electrical mechanism. Try adding a "
    "simple phrase describing how it works electrically — for example that it uses "
    "a sensor, current, switch, circuit, power, plug, or microcontroller."
)


def _has_strong_unsupported_evidence(lowered_text: str) -> bool:
    """True when the text carries clear, unambiguous NON-electronics evidence.

    Word/token based so short markers never fire inside unrelated words (e.g.
    "app" inside "appliance", "medical" inside "medicine"). Read-only; no state.
    """
    tokens = set(_TOKEN_RE.findall(lowered_text))
    if tokens & _STRONG_UNSUPPORTED_WORDS:
        return True
    return any(s in lowered_text for s in _STRONG_UNSUPPORTED_SUBSTRINGS)


def _lay_electrical_evidence_count(lowered_text: str) -> int:
    """Number of DISTINCT lay household-electrical MECHANISM words in the text.

    Word/token based only (no substrings) so markers never fire inside
    unrelated words ("power" inside "powerful"/"empowers"). Read-only.
    """
    tokens = set(_TOKEN_RE.findall(lowered_text))
    return len(tokens & _LAY_ELECTRICAL_WORDS)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/data-and-session", methods=["GET"])
def data_and_session():
    # G-UX-TRUST (S15): static informational Data & Session trust surface.
    # GET-only; takes no session id; reads no session data; mutates nothing;
    # calls no engine function; performs no logging, persistence, or redirect;
    # renders only the static template.
    return render_template("data_session.html")

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
    lowered = idea_text.lower()
    # Domain Gate / Entry UX Increment (post-PR #100 Increment Contract). Bounded
    # ambiguity resolution, ordered so that explicit confirmation resolves only
    # WEAK/ambiguous conflicts and never overrides strong unsupported evidence.
    if _has_strong_unsupported_evidence(lowered):
        # Clearly a non-electronics idea (medical / mechanical / software /
        # drone / solar / robotics / agriculture). The confirmation checkbox
        # cannot override this; refuse with the stable unsupported message
        # (§7.C, §10, §15).
        return render_template("index.html", error=UNSUPPORTED_DOMAIN_MESSAGE)
    if domain != "electronics_electrical":
        if domain in CONFLICTING_SUPPORTED_DOMAINS:
            # A weak/ambiguous conflicting supported-domain classification
            # (e.g. the generic word "monitoring", or the substring "app"
            # inside "appliance") with no strong unsupported evidence. Resolve
            # toward electronics ONLY with corroborating lay electrical
            # mechanism evidence; a medical_device conflict requires MORE
            # corroboration than one lay token (§7.C, §10 — confirmation is
            # never an unconditional override). Otherwise guide the owner
            # toward naming the electrical mechanism instead of a bare hard
            # rejection (§7.B, §7.E). No session is created on guidance.
            required = (_MEDICAL_CONFLICT_LAY_MINIMUM
                        if domain == "medical_device" else 1)
            if _lay_electrical_evidence_count(lowered) < required:
                return render_template("index.html", error=MECHANISM_GUIDANCE_MESSAGE)
        elif domain is not None:
            # Unexpected / unknown classifier value — refuse defensively,
            # regardless of any lay wording.
            return render_template("index.html", error=UNSUPPORTED_DOMAIN_MESSAGE)
        # domain is None: preserve the existing explicit-confirmation fallback
        # admission (unchanged behavior).
    # electronics_electrical, sufficiently corroborated lay electrical
    # mechanism, or None-fallback is admitted under explicit confirmation
    # (None covers functional electronics ideas the signal classifier misses).
    # Admit: the session's domain is the explicitly confirmed supported domain.
    state = IdeaState(idea_id=str(uuid.uuid4()))
    state.domain = DOMAIN_CONFIRM_VALUE
    state.domain_signal = DOMAIN_CONFIRM_VALUE
    # Increment 1 (Owner-Expert Question Boundary): the general /start flow is the
    # non-specialist owner flow and must use the committed Path N non-specialist-safe
    # question provider (NON_SPECIALIST_QUESTIONING_POLICY). This is the same
    # provider already used by the governed _path_n route; no new question bank,
    # mode selector, role, or engine-state field is introduced. The named ILT
    # routes below are deliberately left on their existing default behavior.
    state.path = "N"
    # P4-1b-1 unified capability: ONE uuid4 is used as both the route `sid` and
    # the durable `project_id` (`idea_id` stays a separate uuid4, set above).
    sid = str(uuid.uuid4())
    initial_result = run_iteration(state, idea_text)
    # P4-1b-1 creation order: durably create the project envelope BEFORE any live
    # session is advertised. Durable creation is the commit point for /start; on
    # failure we fail closed — no SESSION_STORE entry, generic unavailable, no
    # user content logged. The envelope carries only the accepted-input ledger
    # (empty at creation) + idea_id; readiness/gaps/last_result are NOT persisted.
    try:
        contract = ProjectRecordContract.from_state(state)
        _get_store().create_project(contract, project_id=sid)
    except Exception:
        return render_template("index.html", error=SERVICE_UNAVAILABLE_MESSAGE), 503
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
        # P4-1b-1 durable cold-load: after memory loss, rebuild the minimum
        # runtime entry from the durable project envelope keyed by sid. On any
        # missing/malformed/unavailable durable state this returns None and we
        # fall through to the existing generic unavailable behaviour (no
        # disclosure of whether the project ever existed).
        entry = _cold_load_entry(sid)
        if not entry:
            return redirect(url_for("index"))
        SESSION_STORE[sid] = entry
    state = entry["state"]
    last_result = entry.get("last_result")
    INTAKE_QUESTION = "Describe your invention in more detail — what specific problem does it solve, and how does it solve it?"

    gap_type = select_next_gap(state)
    question = None
    if gap_type:
        gap = state.get_gap(gap_type)
        iterations_open = gap.iterations_open if gap else 0
        # Increment 1 (Owner-Expert Question Boundary): render via the display
        # selector so an exhausted non-specialist Path N gap shows the
        # deterministic plain-language reframe instead of repeating the final
        # question verbatim. Pure selection — no engine/state/maturity effect.
        # `domain` is attached by the /start routes for live sessions; guard the
        # read so render-context construction never raises if it is absent (the
        # value is unchanged for every real session). No routing/method/state
        # change; the displayed question is identical when `domain` is present.
        question = get_display_question(getattr(state, "domain", None), gap_type,
                                        iterations_open, path=state.path)
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
    # Increment 3 (R-5): compute the one prioritized next development step from the
    # ALREADY-LOADED in-memory IdeaState via the shared pure derivation, and pass
    # it to the presentation-only session callout. Read-only: no route/method
    # change, no state mutation, no persistence, no scoring/progression.
    next_development_step = derive_next_development_step(state)
    # Guided Uncertainty Support (Increment Contract PR #134): derive, READ-ONLY,
    # the user's most recent submitted text from already-existing session state —
    # the last transcript response (an `answered` submission) or the last
    # non-answer interaction text (e.g. the "I do not know this yet" action) —
    # choosing the more recent by iteration. This reads existing structures only;
    # it mutates nothing, adds no field, and never re-scores. The text feeds the
    # pure display-only helper below; the saved answer is unaffected.
    _uncertainty_candidates = []
    _tx = entry.get("transcript") or []
    if _tx:
        _uncertainty_candidates.append(
            (_tx[-1].get("iteration", 0), _tx[-1].get("response", "") or ""))
    _actions = entry.get("interaction_actions") or []
    if _actions:
        _uncertainty_candidates.append(
            (_actions[-1].get("iteration", 0), _actions[-1].get("text", "") or ""))
    _uncertainty_text = (
        max(_uncertainty_candidates, key=lambda c: c[0])[1]
        if _uncertainty_candidates else "")
    return render_template("session.html",
        sid=sid,
        state=state,
        # Workstream 4: read-only render context for the completion-stage
        # structured criticality step (None while the journey is in progress
        # or when no contextually supported unconfirmed requirement remains).
        criticality_step=_criticality_step_context(entry, state, sid),
        next_development_step=next_development_step,
        question=question,
        open_gaps=open_gaps,
        gap_type=gap_type,
        last_result=last_result,
        gap_labels=gap_labels,
        current_gap_label=current_gap_label,
        maturity_label=get_maturity_label(state.maturity_level),
        session_disclosure=SESSION_DISCLOSURE,
        closed_gaps=closed_gaps,
        interaction_ack=entry.pop("_interaction_ack", None) if entry else None,
        # G-UX-ANSWER-VALIDATION: single-use empty-answer validation error, popped
        # here so it renders exactly once after the Post/Redirect/Get and never
        # repeats on a later plain GET. None on every normal load.
        answer_error=entry.pop("_answer_error", None) if entry else None,
        # Increment 1B: advisory, derived, read-only responsibility guidance for
        # the current gap. Computed at render time; never stored, never affects
        # gates/scoring/maturity/closure/transcript/IdeaState. None when no gap.
        current_responsibility=get_responsibility(gap_type) if gap_type else None,
        # Increment 1B clarification display: deterministic, owner-invoked,
        # display-only guidance explaining the current question. Derived from the
        # same gap_type at render time; never stored, never affects
        # gates/scoring/maturity/closure/transcript/IdeaState/persistence; adds no
        # owner action and no POST handling. None when no gap (intake path).
        current_clarification=get_clarification(gap_type) if gap_type else None,
        # More Detail Needed / Guided Answer Scaffolding (Increment Contract PR
        # #106): deterministic, display-only guidance naming the KIND of missing
        # detail to add when the ALREADY-computed engine outcome for the current
        # answer is WARN. Derived at render time from the existing `last_result`
        # (unchanged) and the current gap; never stored, never rewrites/mutates
        # the answer, never closes a gap, never advances maturity, never creates
        # evidence, and never alters the PASS/WARN/BLOCK outcome. None unless WARN.
        current_scaffolding_guidance=get_scaffolding_guidance(last_result, gap_type),
        # Plain-Language Result Feedback (Increment Contract PR #155): deterministic,
        # display-only, content-free plain-language explanation of the ALREADY-computed
        # result for the PRIMARY visible feedback line, derived at render time from the
        # existing `last_result` (transition + raw reason) alone. It never mutates
        # `last_result`, never rewrites `last_result.reason`, never re-scores, and never
        # alters the PASS/WARN/BLOCK outcome; the truthful badge and the raw reason (as
        # non-primary provenance) are rendered by the template independently. None when
        # there is no result / no recognized transition.
        current_result_feedback=get_result_feedback(last_result),
        # Guided Answer Co-Authoring Increment 1 — Advisory Prompt Support
        # (Increment Contract PR #127): deterministic, display-only, content-free
        # OPTIONAL prompts naming the KIND of information the inventor could add to
        # their OWN answer for the current question. Derived at render time from
        # the current gap_type alone; never stored, never reads/rewrites/mutates
        # the answer, never closes a gap, never advances maturity/readiness, never
        # changes scoring/criticality, never touches the transcript/IdeaState/
        # persistence, and adds no owner action, save/approve flow, or form field.
        # None when there is no gap (intake path). The inventor remains the sole
        # author of any saved answer.
        current_answer_coauthoring=get_answer_coauthoring_prompts(gap_type) if gap_type else None,
        # Guided Uncertainty Support (Increment Contract PR #134): deterministic,
        # display-only, content-free SUPPORTIVE prompts shown when the user's most
        # recent submitted text expresses uncertainty ("I don't know" / "لا أعرف").
        # Derived at render time from the read-only `_uncertainty_text` signal
        # above; never stored, never reads/rewrites/mutates the answer, never
        # closes a gap, never marks uncertainty as sufficient, never advances
        # maturity/readiness, never changes scoring/criticality, never touches the
        # transcript/IdeaState/persistence, and adds no owner action, save/approve
        # flow, or form field. None when the text is not uncertainty. The inventor
        # remains the sole author of any saved answer.
        current_uncertainty_guidance=get_uncertainty_guidance(_uncertainty_text),
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
        # G-UX-SNAPSHOT-DECISION: single-use, per-sid "Keep current snapshot"
        # acknowledgement, popped here so it renders once after the Post/Redirect/Get
        # and never repeats on a later plain GET. None on every normal load.
        snapshot_kept_ack=entry.pop("_snapshot_kept_ack", None) if entry else None,
    )


@app.route("/session/<sid>/keep-snapshot", methods=["POST"])
def keep_snapshot(sid):
    # G-UX-SNAPSHOT-DECISION: "Keep current snapshot" — a meaningful but bounded
    # post-output decision within the CURRENT temporary session. It records a
    # single-use, per-sid presentation acknowledgement only and preserves
    # Post/Redirect/Get. It NEVER serializes/duplicates/versions the snapshot,
    # writes any durable store, mutates deterministic IdeaState/results/gaps/
    # maturity/transcript/evidence/interaction-ledger, or leaks across session ids.
    # The current deterministic state itself remains the working snapshot.
    entry = SESSION_STORE.get(sid)
    if not entry:
        # Generic behavior: does not disclose whether the session previously existed.
        return redirect(url_for("index"))
    entry["_snapshot_kept_ack"] = KEEP_SNAPSHOT_ACK
    return redirect(url_for("show_deliverable", sid=sid))

# Per-experiment owner-defined success criteria (planning metadata only).
# Field name on the form is "criterion__<experiment_id>". A criterion is a
# user-defined target, never a test result; this route never runs progression,
# never calls submit_answer, and never writes the ILT-002 transcript.
MAX_CRITERION_LENGTH = 1000
_CRITERION_FIELD_PREFIX = "criterion__"


@app.route("/session/<sid>/success-criteria", methods=["GET"])
def success_criteria(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    package = assemble_deliverable(entry["state"])
    plan = package["section_11_prototype_test_plan"]
    return render_template(
        "success_criteria.html",
        sid=sid,
        experiments=plan["items"],
        stale_notice=plan.get("stale_criteria_notice"),
        field_prefix=_CRITERION_FIELD_PREFIX,
        max_length=MAX_CRITERION_LENGTH,
    )


@app.route("/session/<sid>/success-criteria", methods=["POST"])
def save_success_criteria(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    package = assemble_deliverable(state)
    plan = package["section_11_prototype_test_plan"]
    current_ids = {it["experiment_id"] for it in plan["items"]}

    # Collect submitted criteria, namespaced by experiment_id.
    submitted = {name[len(_CRITERION_FIELD_PREFIX):]: val
                 for name, val in request.form.items()
                 if name.startswith(_CRITERION_FIELD_PREFIX)}

    def _reject(message):
        return render_template(
            "success_criteria.html", sid=sid, experiments=plan["items"],
            stale_notice=plan.get("stale_criteria_notice"),
            field_prefix=_CRITERION_FIELD_PREFIX, max_length=MAX_CRITERION_LENGTH,
            error=message,
        ), 400

    # Validate before any write: reject unknown/stale ids and over-limit input.
    for eid in submitted:
        if eid not in current_ids:
            return _reject("A submitted experiment is not part of the current plan. "
                           "No changes were saved.")
    for eid, raw in submitted.items():
        if len(raw.strip()) > MAX_CRITERION_LENGTH:
            return _reject(f"A criterion exceeds the {MAX_CRITERION_LENGTH}-character "
                           "limit. No changes were saved.")

    # Apply: trim only; whitespace-only removes; idempotent upsert.
    if not isinstance(getattr(state, "success_criteria", None), dict):
        state.success_criteria = {}
    for eid, raw in submitted.items():
        text = raw.strip()
        if text:
            state.success_criteria[eid] = SuccessCriterion(criterion=text)
        else:
            state.success_criteria.pop(eid, None)
    return redirect(url_for("show_deliverable", sid=sid))


@app.route("/session/<sid>", methods=["POST"])
def submit_answer(sid):
    entry = SESSION_STORE.get(sid)
    if not entry:
        return redirect(url_for("index"))
    state = entry["state"]
    # Workstream 4: the structured criticality actions are handled by their
    # own guarded branch (additive; the six frozen dispositions below are
    # untouched). Any OTHER post leaves the criticality step, so its transient
    # UI stage is cleared — recorded confirmations are unaffected.
    if request.form.get("criticality_action") is not None:
        return _handle_criticality_action(entry, state, sid)
    entry.pop("criticality_stage", None)
    entry.pop("criticality_correction", None)
    # Increment 1A: resolve the explicit structured action. Legacy-compatibility
    # rule (chosen, explicit): a submission with NO `action` field is treated as
    # `answered` — exactly the pre-1A behavior, where a non-empty `response` is
    # assessed and an empty one is a no-op. An explicit but UNRECOGNIZED action is
    # rejected with HTTP 400 (never silently assessed), so a malformed client can
    # not smuggle an unknown action into the assessment path.
    action = request.form.get("action", ACTION_ANSWERED).strip().lower()
    if action not in INTERACTION_ACTIONS:
        return ("Unrecognized session action. No change was made.", 400)
    response = request.form.get("response", "").strip()

    if action != ACTION_ANSWERED:
        # Non-answer action: record as additive in-memory metadata only. This
        # path NEVER calls run_iteration, never assesses/scores, never closes or
        # alters a gap, never advances maturity, never satisfies a gate, and never
        # creates an evidence record. select_next_gap() is a read-only selector
        # used only to label which question the action was taken against. Optional
        # owner text is retained verbatim as metadata, not as an assessed response
        # or evidence. The journey truthfully redisplays the same (still-open)
        # question with an honest acknowledgement rather than feigning progress.
        gap_ctx = select_next_gap(state)
        entry.setdefault("interaction_actions", []).append({
            "action": action,
            "iteration": state.iteration,
            "gap_type": gap_ctx,
            "text": response or None,
        })
        entry["_interaction_ack"] = _NON_ANSWER_ACK[action]
        # Increment 2: durable disposition record on the IdeaState ledger. This
        # adds NO epistemic movement (no assess/score/gap/maturity/transcript
        # change) — it only records, truthfully and durably, that the owner took
        # this non-answer action against the still-open question.
        state.record_interaction(
            action=action, content=response or "",
            gap_context=gap_ctx, iteration=state.iteration,
        )
        return redirect(url_for("show_session", sid=sid))

    # ANSWERED — unchanged existing assessment path and transcript record.
    if response:
        targeted_gap = select_next_gap(state)   # gap this answer addresses (pre-iteration)
        result = run_iteration(state, response)
        entry["last_result"] = result
        # Transcript capture: append the answered record to the IN-MEMORY session
        # transcript only. iteration number read after run_iteration() incremented
        # it. No engine effect.
        # G-SC0 (R6): the previous automatic verbatim write to a world/group-
        # readable temporary file has been REMOVED (it exposed verbatim user input
        # on disk). No replacement disk write, log, cache, or durable store is
        # introduced; durable transcript persistence is deferred to Phase 4. The
        # in-memory behavior is unchanged.
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
        # Increment 2: durable answered record on the IdeaState ledger.
        # OWNER_STATED provenance (the owner authored it), UNVALIDATED status
        # (never auto-verified by the act of answering), carrying the current
        # leading evidence quality where available. Additive only: the existing
        # assessment path, transcript, and gap lifecycle above are unchanged.
        state.record_interaction(
            action=ACTION_ANSWERED, content=response,
            gap_context=targeted_gap, iteration=state.iteration,
            quality=getattr(getattr(state, "known_mechanism", None), "quality", None)
                    or getattr(getattr(state, "known_problem", None), "quality", None),
        )
        import sys
        for g in state.gaps:
                    pass
    else:
        # G-UX-ANSWER-VALIDATION: the owner chose to answer (action == answered)
        # but the whitespace-normalized response is empty. Set a SINGLE-USE
        # transient error and preserve Post/Redirect/Get. The empty string is
        # never assessed, scored, or written to transcript/gap/maturity/evidence/
        # engine state (the assessment branch above is skipped). show_session GET
        # pops the transient, so it displays once and is not repeated on refresh.
        entry["_answer_error"] = ANSWER_REQUIRED_MESSAGE
    return redirect(url_for("show_session", sid=sid))


# ---------------------------------------------------------------------------
# FDC-001 first increment — Technical Decision Workspace.
# In-memory only. Distinct from SESSION_STORE; imports no session_store; writes
# no durable state; performs no benchmark run. Activation-only lane surface.
# ---------------------------------------------------------------------------
from engine import decision_workspace as fdc001_dw

# Dedicated in-memory store for FDC-001 decision records (non-durable).
FDC001_DECISIONS = {}


@app.route("/decision-workspace", methods=["GET"])
def decision_workspace_start():
    record = fdc001_dw.DecisionRecord()
    FDC001_DECISIONS[record.decision_id] = record
    return redirect(url_for("decision_workspace_view", did=record.decision_id))


def _render_decision_workspace(record, error=None, status=200):
    """Render the workspace, optionally with a bounded user-visible validation
    error. The error is a concise message only — never a traceback."""
    html = render_template(
        "decision_workspace.html",
        view=record.to_record_dict(),
        candidate_names=list(fdc001_dw.CANDIDATE_NAMES),
        limitations=list(fdc001_dw.EXPORT_LIMITATIONS),
        error=error,
    )
    return (html, status)


@app.route("/decision-workspace/<did>", methods=["GET"])
def decision_workspace_view(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    return _render_decision_workspace(record)


@app.route("/decision-workspace/<did>/input", methods=["POST"])
def decision_workspace_add_input(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    candidate_id = request.form.get("candidate_id", "").strip()
    candidate_ids = [candidate_id] if candidate_id else []
    try:
        record.add_input(
            request.form.get("text", "").strip(),
            request.form.get("claim_class", "").strip(),
            request.form.get("provenance", "").strip(),
            decision_relevant=request.form.get("decision_relevant") == "on",
            candidate_ids=candidate_ids,
        )
    except fdc001_dw.DecisionError as exc:
        # The record is left unmodified; show a concise bounded error.
        return _render_decision_workspace(
            record, error="Input rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/constraint", methods=["POST"])
def decision_workspace_add_constraint(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    candidate_id = request.form.get("candidate_id", "").strip()
    candidate_ids = [candidate_id] if candidate_id else []
    try:
        record.add_constraint(
            request.form.get("text", "").strip(),
            request.form.get("constraint_strength", "").strip(),
            request.form.get("provenance", "").strip(),
            confirmed=request.form.get("confirmed") == "on",
            candidate_ids=candidate_ids,
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Constraint rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/gap", methods=["POST"])
def decision_workspace_gap_action(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    action = request.form.get("action", "").strip()
    gap_id = request.form.get("gap_id", "").strip()
    try:
        if action in ("resolve", "reclassify"):
            # FDC-002 user-facing route guard (reconciled contract, spec §12.1 /
            # guarantee #31): the legacy bare-text resolve/reclassify route must
            # NOT clear or reclassify a physical/calibration blocker. Reject
            # BEFORE invoking the legacy domain mutation, so the rejection is
            # bounded (HTTP 400) and atomic — no gap, revision, history,
            # readiness, blocker, or change-impact mutation. The FDC-002
            # evidence-assessment workflow is the sole user-facing path for that
            # blocker. (gap_blocker_code is read-only and raises for unknown ids.)
            if (record.gap_blocker_code(gap_id)
                    == fdc001_dw.MISSING_PHYSICAL_OR_CALIBRATION_INFORMATION):
                return _render_decision_workspace(
                    record,
                    error=("Gap action rejected: the "
                           "missing_physical_or_calibration_information blocker "
                           "can be cleared only through the evidence-assessment "
                           "workflow (record evidence, then assess and decide), "
                           "not this route."),
                    status=400)
            if action == "resolve":
                record.resolve_gap(gap_id)
            else:
                record.reclassify_gap(
                    gap_id, request.form.get("rationale", "").strip())
        else:
            raise fdc001_dw.DecisionError("unknown gap action: %r" % action)
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Gap action rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/evidence", methods=["POST"])
def decision_workspace_add_evidence(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    candidate_id = request.form.get("candidate_id", "").strip()
    candidate_ids = [candidate_id] if candidate_id else []
    try:
        # verification_status is NEVER read from the form: it is system-set to
        # `unverified` inside add_evidence (§7.4). Any posted value is ignored.
        record.add_evidence(
            request.form.get("gap_id", "").strip(),
            request.form.get("text", "").strip(),
            request.form.get("claim_class", "").strip(),
            request.form.get("provenance", "").strip(),
            method=request.form.get("method", "").strip() or None,
            source_label=request.form.get("source_label", "").strip() or None,
            evidence_version=request.form.get("evidence_version", "").strip() or None,
            limitations=request.form.get("limitations", "").strip() or None,
            candidate_ids=candidate_ids,
            decision_relevant=request.form.get("decision_relevant") == "on",
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Evidence rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/gap-assessment", methods=["POST"])
def decision_workspace_gap_assessment(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    evidence_ids = [e.strip() for e in request.form.getlist("evidence_ids")
                    if e.strip()]
    try:
        record.assess_gap(
            request.form.get("gap_id", "").strip(),
            evidence_ids,
            request.form.get("assessment", "").strip(),
            request.form.get("rationale", "").strip(),
            request.form.get("resolution_decision", "").strip(),
            resolution_rationale=(
                request.form.get("resolution_rationale", "").strip() or None),
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Gap assessment rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/preference", methods=["POST"])
def decision_workspace_preference(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    action = request.form.get("action", "").strip()
    try:
        if action == "set":
            record.set_owner_preference(
                request.form.get("candidate_id", "").strip(),
                request.form.get("rationale", "").strip() or None)
        elif action == "clear":
            record.clear_owner_preference()
        else:
            raise fdc001_dw.DecisionError("unknown preference action: %r" % action)
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Preference action rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/candidate", methods=["POST"])
def decision_workspace_dispose_candidate(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    try:
        record.dispose_candidate(
            request.form.get("candidate_id", "").strip(),
            request.form.get("option_status", "").strip(),
            request.form.get("disposition_reason", "").strip(),
            request.form.get("disposition_basis", "").strip(),
        )
    except fdc001_dw.DecisionError as exc:
        return _render_decision_workspace(
            record, error="Candidate disposition rejected: %s" % exc, status=400)
    return redirect(url_for("decision_workspace_view", did=did))


@app.route("/decision-workspace/<did>/export", methods=["GET"])
def decision_workspace_export(did):
    record = FDC001_DECISIONS.get(did)
    if record is None:
        return redirect(url_for("decision_workspace_start"))
    # Deterministic, safe attachment filename derived from the decision id.
    filename = "fdc001-decision-%s.json" % record.decision_id
    response = app.response_class(
        response=record.to_json(),
        status=200,
        mimetype="application/json",
    )
    response.headers["Content-Disposition"] = (
        'attachment; filename="%s"' % filename)
    return response


def _run_config():
    """Explicit run configuration for the bounded single-threaded P4-1b-1 MVP
    (G-P4-1B-1-AMEND-01 / D-P4-1B-1-AMEND-01). `threaded` is pinned **False** so
    requests are served one at a time, matching the single application-scoped
    `SqliteRecordStore` connection (which is thread-bound); the runtime must NOT
    rely on Flask's default threaded serving. This is a bounded MVP decision, NOT
    a claim that Flask's built-in server is a production deployment architecture;
    multi-worker/threaded topology is deferred. No `engine/record_store.py`
    change and no `check_same_thread` override is used. Exposed as a small helper
    so the selected serving boundary is inspectable and testable."""
    return {
        "debug": _debug_enabled(),
        "host": _resolve_host(),
        "port": 5000,
        "threaded": False,
    }


if __name__ == "__main__":
    app.run(**_run_config())
