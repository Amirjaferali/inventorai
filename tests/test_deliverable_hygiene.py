"""Workstream 3 Deliverable Hygiene — RED coverage (contract §10).

File: tests/test_deliverable_hygiene.py
Purpose: prove, against the current authoritative implementation, that the
final inventor-facing deliverable does not yet satisfy the canonical
Workstream 3 contract (docs/governance/DELIVERABLE_HYGIENE_INCREMENT_CONTRACT.md):
Defect 3 (raw internal machine-state leakage into the Final Deliverable JSON
and HTML) and Defect 4 (count basis and relationship clarity for sections 4,
13, and 14) — each proven independently. These tests are the contract's RED
gate; they are EXPECTED TO FAIL on the pre-implementation base and to pass
only when the separately owner-gated implementation lands.
Input contract: run under pytest from the repository root; exercises the real
deliverable generation path only (Flask test client journeys ->
engine.deliverable_assembler.assemble_deliverable and the committed
/session/<sid>/deliverable route). Deterministic fixtures; no network, no
randomness in assertions, no external service.
Output contract: standard pytest results. Guard tests (safety-signal
invariance, WS1/WS2 evidence-tree immutability, fixture integrity) must PASS
on the base; every test named test_defect3_* / test_defect4_* must FAIL on
the base for the mapped contract reason.
Prohibited behaviors: MUST NOT modify production source, templates, any other
test, evidence, or repository state; MUST NOT mock away the behavior under
review; MUST NOT weaken an assertion to force execution or failure. Counts in
sections other than 4, 13, and 14 are observation-only under contract §10 and
are deliberately NOT asserted here.

Prohibited-token list (contract §8.1): the nine pinned tokens, plus disclosed
same-class additions permitted by §8.1 only as unambiguous syntactic
equivalents of already-pinned tokens (each addition's class has a pinned
exemplar): remaining raw gap-type enums (class exemplar: PROBLEM_MECHANISM_FIT),
the remaining raw evidence-quality constant DEMONSTRATED (class exemplars:
ASSERTED, REASONED), and the remaining raw responsibility constants (class
exemplar: OWNER_EXECUTABLE). No semantically ambiguous token was added.
Observed-but-not-added (reported for owner review, per contract §10 and §8.1:
observation, not repair): raw lifecycle status values such as "OPEN" /
"PARTIAL" / "CLOSED" in machine `status` fields and the raw validation-status
constant "UNVALIDATED" — their classes have no pinned exemplar in §8.1.
"""
import hashlib
import os
import re

import pytest

from web.app import app, SESSION_STORE, DOMAIN_CONFIRM_VALUE
from engine.deliverable_assembler import assemble_deliverable
from engine.idea_state import IdeaState, Gap, OPEN
from engine.safety_signal import derive_inventor_stated_safety_signals

# --------------------------------------------------------------------------
# Contract-bound identifiers (contract §7; owner authorization §4)
# --------------------------------------------------------------------------
SECTION_4_COUNT_BASIS = "evidence_derived_requirements"
SECTION_13_COUNT_BASIS = "requirement_landscape"
SECTION_14_PLAN_SOURCE = "requirement_landscape"

# --------------------------------------------------------------------------
# Exact inventor-facing public values for the Section 12 serialization
# boundary (Finding F1 corrective contract). The six gap-type values are the
# already-committed inventor-facing gap labels; the five provider values are
# the owner-approved public provider wordings. These are asserted byte-exact
# (never by absence scanning alone) so a wrong or partial mapping cannot pass.
# --------------------------------------------------------------------------
SECTION_12_GAP_PUBLIC = {
    "PHYSICAL_FEASIBILITY":    "Physical Feasibility",
    "BOUNDARY_AMBIGUITY":      "Boundary and Scope",
    "MECHANISM_COMPLETENESS":  "Mechanism Completeness",
    "PROBLEM_MECHANISM_FIT":   "Problem–Mechanism Fit",
    "ASSUMPTION_INVENTORY":    "Assumption Inventory",
    "EXPERTISE_GAP_AWARENESS": "Expertise-Gap Awareness",
}
SECTION_12_PROVIDER_PUBLIC = {
    "OWNER_INPUT":        "You (the inventor)",
    "SYSTEM_ANALYSIS":    "System analysis",
    "SPECIALIST_INPUT":   "A relevant technical specialist",
    "EMPIRICAL_EVIDENCE": "A measurement, test, or other empirical evidence",
    "UNDETERMINED":       "Not yet determined",
}

# --------------------------------------------------------------------------
# Prohibited Tokens (contract §8.1). Nine pinned tokens first, then the
# disclosed unambiguous same-class additions described in the module docstring.
# Matching is case-sensitive with machine-token boundaries so honest
# inventor-facing English ("Asserted (inventor-stated…)", "Responsibility
# undetermined", "Reasoned -> Demonstrated") is NOT flagged — only the raw
# machine forms are.
# --------------------------------------------------------------------------
PROHIBITED_TOKENS = (
    # pinned (contract §8.1)
    "UNDETERMINED",
    "system-derived",
    "REASONED",
    "ASSERTED",
    "OWNER_EXECUTABLE",
    "LEGACY_UNSPECIFIED",
    "CONFIDENCE_UNDETERMINED",
    "PROBLEM_MECHANISM_FIT",
    "MECHANISM_COMPLETENESS",
    # disclosed additions — remaining raw gap-type enums (same class as
    # PROBLEM_MECHANISM_FIT / MECHANISM_COMPLETENESS)
    "PHYSICAL_FEASIBILITY",
    "BOUNDARY_AMBIGUITY",
    "ASSUMPTION_INVENTORY",
    "EXPERTISE_GAP_AWARENESS",
    # disclosed addition — remaining raw evidence-quality constant (same class
    # as ASSERTED / REASONED)
    "DEMONSTRATED",
    # disclosed additions — remaining raw responsibility constants (same class
    # as OWNER_EXECUTABLE)
    "SYSTEM_DERIVABLE",
    "SPECIALIST_REQUIRED",
    "EMPIRICAL_EVIDENCE_REQUIRED",
    # disclosed additions (Finding F1 corrective contract) — the remaining raw
    # suggested-provider vocabulary values (same owner-approved five-value
    # class as the pinned exemplar UNDETERMINED; engine-resident provider
    # grounding in engine.idea_development_outputs)
    "OWNER_INPUT",
    "SYSTEM_ANALYSIS",
    "SPECIALIST_INPUT",
    "EMPIRICAL_EVIDENCE",
    # disclosed additions (Workstream 4 structured criticality hardening) —
    # the raw criticality category tokens (same single-uppercase-token class
    # as the pinned exemplar UNDETERMINED) and the raw owner-confirmed
    # authority token (same hyphenated-machine-form class as the pinned
    # exemplar system-derived). The lowercase `undetermined` authority is
    # deliberately NOT a blanket token (it is legitimate English prose,
    # e.g. "Responsibility undetermined"); it is covered by the field-aware
    # criticality-value rule below.
    "FEASIBILITY-THREATENING",
    "VALUE-ENHANCING",
    "REFINEMENT",
    "owner-confirmed",
)

_TOKEN_RES = {
    t: re.compile(r"(?<![A-Za-z0-9_])" + re.escape(t) + r"(?![A-Za-z0-9_])")
    for t in PROHIBITED_TOKENS
}

# Machine-status fields where the raw internal values "stated" / "recorded"
# are prohibited as FIELD VALUES (contract §5.3 / §8.2: the rule is
# field-aware — these words remain permitted inside ordinary prose).
MACHINE_STATUS_FIELD_KEYS = ("resolution_status", "status")
MACHINE_STATUS_PROHIBITED_VALUES = ("stated", "recorded")

# Workstream 4 hardening: criticality machine fields where RAW internal
# vocabulary is prohibited as FIELD VALUES (field-aware, mirroring the
# stated/recorded rule above): the section_13 criticality and
# criticality_authority fields must carry only the committed public wordings.
# Lowercase "undetermined" remains permitted in ordinary prose.
CRITICALITY_FIELD_KEYS = ("criticality",)
CRITICALITY_PROHIBITED_VALUES = (
    "FEASIBILITY-THREATENING", "VALUE-ENHANCING", "REFINEMENT", "UNDETERMINED")
CRITICALITY_AUTHORITY_FIELD_KEYS = ("criticality_authority",)
CRITICALITY_AUTHORITY_PROHIBITED_VALUES = (
    "owner-confirmed", "undetermined", "system-derived")

# --------------------------------------------------------------------------
# Verbatim-exemption discipline (contract §8.3). An output value is exempt
# from prohibited-token scanning ONLY when BOTH hold:
#   (a) its JSON path matches one of the enumerated candidate paths below
#       ("*" matches one list index), AND
#   (b) it is PROVABLY byte-derived from the fixture's inventor input — i.e.
#       the value (stripped) occurs verbatim inside the concatenated inventor
#       inputs of the journey under test.
# Nothing else is exempt: generated prose, labels, metadata, status,
# authority, provenance, confidence, scoring vocabulary, count explanations,
# and enum-derived values are never exempt. This is the exhaustive candidate
# exemption-path list for the current package shape; the implementation
# report must re-prove the final list (contract §8.3).
# --------------------------------------------------------------------------
EXEMPT_VERBATIM_PATHS = (
    ("_session_meta", "idea_summary"),
    ("_session_meta", "evidence_registry", "*", "content"),
    ("_session_meta", "unknown_registry", "*", "content"),
    ("_session_meta", "inventor_stated_safety_signals", "signals", "*", "statement"),
    ("section_2_invention_summary", "known_problem", "content"),
    ("section_2_invention_summary", "known_mechanism", "content"),
    ("section_2_invention_summary", "known_boundaries", "*", "content"),
    ("section_5_assumptions", "inventor_unknowns", "*", "statement"),
    ("section_9_stage3_reasoning", "items", "*", "evidence", "*", "content"),
    ("section_11_prototype_test_plan", "items", "*", "traceability", "content"),
    ("section_11_prototype_test_plan", "items", "*", "success_criterion"),
    # Disclosed candidate verbatim path (Finding F1 corrective contract):
    # pending-evidence Section 12 payloads carry the record's verbatim content
    # as evidence_needed.
    ("section_12_next_development_step", "evidence_needed"),
    ("section_13_requirement_landscape", "requirements", "*", "statement"),
    ("section_13_requirement_landscape", "requirements", "*", "resolving_action"),
    ("section_14_validation_plan", "steps", "*", "statement"),
)

# Pinned immutable-evidence content hashes (guard, contract §10 item 11 and
# §17/F4): SHA-256 over sorted (relative path + file bytes) of each canonical
# evidence directory at the authoritative Workstream 3 contract tip.
WS1_EVIDENCE_DIR = "docs/governance/evidence/workstream1_deliverable_baseline"
WS1_EVIDENCE_CONTENT_SHA256 = (
    "8803ff9356b21c1be6082123c63bf1a552ed8e95f1113e32432818be2e32f60b")
WS2_EVIDENCE_DIR = "docs/governance/evidence/workstream2_safety_stabilization"
WS2_EVIDENCE_CONTENT_SHA256 = (
    "432972f72ca0fbeaa3ad18872a71570f33806973dedf50e112b9eda281889091")

# --------------------------------------------------------------------------
# Fixture journeys — the REAL generation path, deterministic inputs.
# The false-negative-resistant journey below is byte-identical to the
# committed Workstream 1 baseline inputs
# (docs/governance/evidence/workstream1_deliverable_baseline/
#  inputs_false_negative_journey.json), so its deliverable is directly
# comparable with the immutable WS1 evidence.
# --------------------------------------------------------------------------
IDEA_WS1 = (
    "A smart plug-in safety device that senses appliance current and voltage "
    "with a microcontroller and disconnects a relay to warn about dangerous "
    "appliances"
)
BASE_ANSWER = (
    "The current sensor detects an abnormal rise because the shunt "
    "resistor voltage increases, therefore the microcontroller opens the "
    "relay to disconnect the appliance.")
DANGER_BY_ITERATION = {
    3: " If the sensing is wrong, the dangerous appliance could remain powered.",
    4: (" If it trips the wrong branch, the wrong appliance could be "
        "disconnected and it would fail to isolate the actual source of danger."),
    6: (" If the relay sticks, damage or overheating could continue and the "
        "fire risk could continue until someone notices."),
    7: (" The current sensing accuracy is essential; the buzzer volume and "
        "alert timing are adjustable."),
}
UNKNOWN_ITERATION = 5
UNKNOWN_TEXT = "I don't know yet."
MAX_ITERATIONS = 30

IDEA_POSITIVE = (
    "A smart plug-in safety device for home appliances using current and "
    "voltage sensing, a microcontroller, Wi-Fi, an LED buzzer warning, and a "
    "plug housing"
)
POSITIVE_STATEMENT = (
    "If insulation cannot be safely achieved inside the plug housing, the "
    "device should not be used because it could create a safety risk."
)

# Dedicated ASSERTED-quality fixture (contract §10 item 3): same idea, but
# every answer is assertion-only (no causal connector), so the recorded
# evidence grades ASSERTED and the deliverable exercises the `_s6` ASSERTED
# prose branch.
ASSERTED_ANSWER = (
    "The device detects the abnormal current rise. The microcontroller "
    "opens the relay and disconnects the appliance. The alert is loud.")
ASSERTED_ITERATIONS = 4


def _run_journey(idea, answer_for_iteration, max_iterations):
    """Drive the committed Flask session flow to (at most) max_iterations and
    return (inventor_inputs, state, package, deliverable_html). Uses only the
    real committed routes and the real assembler — nothing is mocked."""
    client = app.test_client()
    resp = client.post("/start", data={"idea": idea,
                                       "domain_confirm": DOMAIN_CONFIRM_VALUE})
    assert resp.status_code == 302, resp.status_code
    sid = resp.headers["Location"].rsplit("/", 1)[-1]
    inputs = [idea]
    for i in range(2, max_iterations + 2):
        page = client.get(f"/session/{sid}").get_data(as_text=True)
        if '<p class="complete">' in page:
            break
        action, text = answer_for_iteration(i)
        if action is None:
            break
        inputs.append(text)
        client.post(f"/session/{sid}", data={"response": text, "action": action})
    state = SESSION_STORE[sid]["state"]
    package = assemble_deliverable(state)
    html = client.get(f"/session/{sid}/deliverable").get_data(as_text=True)
    SESSION_STORE.pop(sid, None)
    return inputs, state, package, html


@pytest.fixture(scope="module")
def ws1_journey():
    """The Workstream 1 false-negative baseline journey (byte-identical
    inputs) run to the true completion branch, then through the real
    deliverable generation path. False-negative-resistant by construction:
    every assertion below scans ALL serialized values recursively, so merely
    relabeling, renaming, or duplicating raw values cannot satisfy it."""
    def answers(i):
        if i == UNKNOWN_ITERATION:
            return "unknown", UNKNOWN_TEXT
        return "answered", BASE_ANSWER + DANGER_BY_ITERATION.get(i, "")
    inputs, state, package, html = _run_journey(IDEA_WS1, answers, MAX_ITERATIONS)
    return {"inputs": inputs, "state": state, "package": package, "html": html}


@pytest.fixture(scope="module")
def asserted_journey():
    """Assertion-only journey: recorded evidence grades ASSERTED, exercising
    the `_s6` ASSERTED prose branch (contract §10 item 3)."""
    def answers(i):
        if i >= 2 + ASSERTED_ITERATIONS:
            return None, None
        return "answered", ASSERTED_ANSWER
    inputs, state, package, html = _run_journey(IDEA_WS1, answers, MAX_ITERATIONS)
    return {"inputs": inputs, "state": state, "package": package, "html": html}


@pytest.fixture(scope="module")
def positive_journey():
    """The committed PR #122 positive safety-signal baseline journey (one
    verbatim inventor safety statement), reaching deliverable generation."""
    def answers(i):
        if i > 2:
            return None, None
        return "answered", POSITIVE_STATEMENT
    inputs, state, package, html = _run_journey(IDEA_POSITIVE, answers, 1)
    return {"inputs": inputs, "state": state, "package": package, "html": html}


@pytest.fixture(scope="module")
def no_answer_journey():
    """No-substantive-answer journey (Finding F1 corrective contract): the
    session is started with the WS1 idea and NO owner response of any kind is
    submitted, so no ledger record exists and the shared next-development-step
    derivation reaches its open-gap path — the state in which the unpatched
    Section 12 exports a raw gap enum and the raw UNDETERMINED provider."""
    def answers(i):
        return None, None
    inputs, state, package, html = _run_journey(IDEA_WS1, answers, 1)
    return {"inputs": inputs, "state": state, "package": package, "html": html}


@pytest.fixture(scope="module")
def unknown_action_journey():
    """Unknown-action journey (Finding F1 corrective contract): the owner takes
    exactly one structured 'unknown' action and never answers, so the only
    ledger record is a non-answer disposition and the shared derivation again
    reaches its open-gap path through the real committed routes."""
    def answers(i):
        return "unknown", UNKNOWN_TEXT
    inputs, state, package, html = _run_journey(IDEA_WS1, answers, 1)
    return {"inputs": inputs, "state": state, "package": package, "html": html}


# --------------------------------------------------------------------------
# Field-aware scanning helpers
# --------------------------------------------------------------------------

def _walk(node, path=()):
    """Yield (path, key_or_None, value) for every leaf value in the package."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _walk(v, path + (str(k),))
    elif isinstance(node, (list, tuple)):
        for i, v in enumerate(node):
            yield from _walk(v, path + (str(i),))
    else:
        yield path, (path[-1] if path else None), node


def _path_matches(path, pattern):
    if len(path) != len(pattern):
        return False
    for p, q in zip(path, pattern):
        if q == "*":
            if not p.isdigit():
                return False
        elif p != q:
            return False
    return True


def _is_exempt(path, value, inventor_inputs):
    """Contract §8.3: exempt only when the path is enumerated AND the value is
    provably byte-derived from the inventor's verbatim inputs."""
    if not isinstance(value, str) or not value.strip():
        return False
    if not any(_path_matches(path, pat) for pat in EXEMPT_VERBATIM_PATHS):
        return False
    joined = "\n".join(inventor_inputs)
    return value.strip() in joined


def _prohibited_token_hits(package, inventor_inputs):
    """All (path, token) pairs where a Prohibited Token appears in a
    non-exempt serialized value of the final inventor-facing package."""
    hits = []
    for path, _key, value in _walk(package):
        if not isinstance(value, str):
            continue
        if _is_exempt(path, value, inventor_inputs):
            continue
        for token, rx in _TOKEN_RES.items():
            if rx.search(value):
                hits.append((".".join(path), token))
    return hits


def _machine_status_hits(package):
    """All (path, value) pairs where a machine-status field carries a raw
    'stated'/'recorded' internal value (contract §5.3 / §8.2 field-aware rule)."""
    hits = []
    for path, key, value in _walk(package):
        if key in MACHINE_STATUS_FIELD_KEYS and value in MACHINE_STATUS_PROHIBITED_VALUES:
            hits.append((".".join(path), value))
    return hits


def _criticality_field_hits(package):
    """All (path, value) pairs where a section_13 criticality machine field
    carries a raw internal category/authority value (Workstream 4 field-aware
    hardening rule)."""
    hits = []
    for path, key, value in _walk(package):
        if key in CRITICALITY_FIELD_KEYS and value in CRITICALITY_PROHIBITED_VALUES:
            hits.append((".".join(path), value))
        if (key in CRITICALITY_AUTHORITY_FIELD_KEYS
                and value in CRITICALITY_AUTHORITY_PROHIBITED_VALUES):
            hits.append((".".join(path), value))
    return hits


def _dir_content_sha256(root):
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in sorted(os.walk(root)):
        dirnames.sort()
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, root)
            h.update(rel.encode("utf-8") + b"\x00")
            with open(p, "rb") as f:
                h.update(f.read() + b"\x00")
    return h.hexdigest()


# ==========================================================================
# Defect 3 — inventor-facing raw internal state leakage (contract §10 items
# 1–3; owner Decision 1: JSON AND HTML are both inventor-facing; Decision 2:
# raw values live in internal state only; §6: no Safety-Signal carve-out —
# the scans below cover the Safety-Signal block with ONLY the enumerated
# verbatim `statement` exemption).
# ==========================================================================

def test_defect3_json_field_aware_token_absence(ws1_journey):
    """RED: the Final Deliverable JSON must contain no Prohibited Token in any
    non-exempt value (contract §8.2). The scan is recursive over the whole
    package (including _session_meta and the Safety-Signal block), so labels
    added alongside raw values cannot mask a leak."""
    hits = _prohibited_token_hits(ws1_journey["package"], ws1_journey["inputs"])
    assert hits == [], (
        "Raw internal machine-state values are exported in the final "
        "inventor-facing Deliverable JSON (contract §8.2 violated): %r" % hits)


def test_defect3_html_token_absence(ws1_journey):
    """RED: the rendered Final Deliverable HTML must contain no Prohibited
    Token outside content traced to the §8.3 verbatim exemptions (contract
    §8.4). The fixture's inventor inputs contain no Prohibited Token (see the
    fixture-integrity guard), so a plain boundary scan is exact here."""
    html = ws1_journey["html"]
    hits = [t for t, rx in _TOKEN_RES.items() if rx.search(html)]
    assert hits == [], (
        "Raw internal machine-state values are rendered in the final "
        "inventor-facing Deliverable HTML (contract §8.4 violated): %r" % hits)


def test_defect3_machine_status_fields_hold_no_raw_stated_recorded(ws1_journey):
    """RED: 'stated' / 'recorded' are prohibited as machine-status FIELD
    VALUES ('resolution_status'-class; contract §5.3 / §8.2), while remaining
    permitted inside ordinary prose. Currently section_4 requirements carry
    resolution_status='stated' and section_13 requirements carry
    status='recorded'."""
    hits = _machine_status_hits(ws1_journey["package"])
    assert hits == [], (
        "Machine-status fields expose raw internal status values in the "
        "final inventor-facing Deliverable JSON (contract §5.3/§8.2): %r" % hits)


def test_ws4_criticality_fields_hold_no_raw_internal_values(ws1_journey):
    """Workstream 4 protective hardening (WS4 contract §9/§16.3): the
    section_13 criticality and criticality_authority machine fields must
    carry only the committed public wordings — never a raw category or
    authority token. The lowercase `undetermined` authority is checked here
    field-aware (it remains permitted in ordinary inventor-facing prose and
    is therefore not a blanket Prohibited Token)."""
    hits = _criticality_field_hits(ws1_journey["package"])
    assert hits == [], (
        "Raw internal criticality vocabulary exported as section_13 machine "
        "field values (Workstream 4 hardening): %r" % hits)


def test_defect3_asserted_prose_path(asserted_journey):
    """RED (contract §10 item 3): the dedicated ASSERTED-quality fixture must
    show that the `_s6` ASSERTED prose branch does not embed the raw quality
    token, in JSON or HTML. Currently section_6 renders 'All evidence is
    ASSERTED (inventor-stated, unvalidated).'"""
    package, html = asserted_journey["package"], asserted_journey["html"]
    risks = package["section_6_risks"]["risks"]
    quality_rows = [r for r in risks if r.get("category") == "evidence_quality"]
    assert quality_rows, (
        "fixture integrity: the ASSERTED journey must produce a section_6 "
        "evidence_quality risk row — the fixture no longer exercises the "
        "branch under test")
    rx = _TOKEN_RES["ASSERTED"]
    json_hits = [r["description"] for r in quality_rows if rx.search(r["description"] or "")]
    assert json_hits == [] and not rx.search(html), (
        "The section_6 ASSERTED prose branch embeds the raw quality token in "
        "the inventor-facing deliverable (contract §9.4/§8): JSON hits=%r, "
        "HTML hit=%r" % (json_hits, bool(rx.search(html))))


def test_defect3_labels_alongside_raw_values_insufficient(ws1_journey):
    """RED (owner Decision 1: labels-alongside is insufficient). Section 14
    already emits responsibility_label / confidence_label next to the raw
    responsibility / confidence tokens; the raw tokens must nevertheless be
    absent from the inventor-facing package. This test scans ONLY the
    section_14 subtree, proving independently that relabeling without removal
    does not satisfy the contract."""
    s14 = ws1_journey["package"]["section_14_validation_plan"]
    hits = _prohibited_token_hits(s14, ws1_journey["inputs"])
    labelled = [s for s in s14["steps"] if s.get("responsibility_label")]
    assert labelled, "fixture integrity: expected labelled section_14 steps"
    assert hits == [], (
        "section_14 carries human labels ALONGSIDE raw machine tokens; the "
        "raw tokens are still exported, which owner Decision 1 rules "
        "insufficient (contract §5.1): %r" % hits)


# --------------------------------------------------------------------------
# Finding F1 corrective contract — Section 12 serialization-boundary coverage.
# Exact rendered-field extraction for the deliverable HTML: the template
# renders the suggested provider as a labelled field-value pair.
# --------------------------------------------------------------------------
_HTML_PROVIDER_RE = re.compile(
    r'<div class="field-label">Suggested provider</div>\s*'
    r'<div class="field-value">([^<]*)</div>')


def _html_provider_value(html):
    """The exact rendered Suggested-provider field value, or None when the
    deliverable HTML renders no suggested provider."""
    m = _HTML_PROVIDER_RE.search(html)
    return m.group(1) if m else None


def test_defect3_no_answer_state_json_token_absence(no_answer_journey):
    """RED (F1): the no-substantive-answer state must export no Prohibited
    Token in any non-exempt value of the Final Deliverable JSON. On the
    unpatched base, Section 12 exports the raw open-gap enum as reference_id
    and the raw UNDETERMINED provider token as suggested_provider."""
    hits = _prohibited_token_hits(no_answer_journey["package"],
                                  no_answer_journey["inputs"])
    assert hits == [], (
        "Raw internal machine-state values are exported in the no-answer "
        "state Deliverable JSON (contract §8.2; Finding F1): %r" % hits)


def test_defect3_no_answer_state_html_token_absence(no_answer_journey):
    """RED (F1): the rendered no-substantive-answer Deliverable HTML must
    contain no Prohibited Token. The fixture's only inventor input is the
    idea text, which contains no Prohibited Token, so a plain boundary scan
    is exact here."""
    html = no_answer_journey["html"]
    hits = [t for t, rx in _TOKEN_RES.items() if rx.search(html)]
    assert hits == [], (
        "Raw internal machine-state values are rendered in the no-answer "
        "state Deliverable HTML (contract §8.4; Finding F1): %r" % hits)


def test_defect3_unknown_action_state_token_absence(unknown_action_journey):
    """RED (F1): the unknown-action state must export no Prohibited Token in
    the Final Deliverable — neither in any non-exempt JSON value nor in the
    rendered HTML. The fixture's inventor inputs contain no Prohibited Token,
    so the HTML boundary scan is exact here."""
    json_hits = _prohibited_token_hits(unknown_action_journey["package"],
                                       unknown_action_journey["inputs"])
    html = unknown_action_journey["html"]
    html_hits = [t for t, rx in _TOKEN_RES.items() if rx.search(html)]
    assert json_hits == [] and html_hits == [], (
        "Raw internal machine-state values are exported in the unknown-action "
        "state Deliverable (contract §8.2/§8.4; Finding F1): JSON=%r HTML=%r"
        % (json_hits, html_hits))


def test_defect3_section12_open_gap_exact_public_values(no_answer_journey):
    """RED (F1, exact values): the open-gap Section 12 payload must carry the
    exact committed public gap label as reference_id and the exact public
    provider wording as suggested_provider — verified byte-exact in the JSON
    package AND in the rendered HTML field, not by absence scanning."""
    s12 = no_answer_journey["package"]["section_12_next_development_step"]
    assert s12["actionable"] is True and s12["issue_type"] == "open_gap", (
        "fixture integrity: the no-answer journey must reach the open-gap "
        "next-development-step payload — the fixture no longer exercises the "
        "state under test")
    assert s12["reference_id"] == SECTION_12_GAP_PUBLIC["MECHANISM_COMPLETENESS"], (
        "Section 12 open-gap reference_id is not the exact committed public "
        "gap label (Finding F1): %r" % (s12["reference_id"],))
    assert s12["suggested_provider"] == SECTION_12_PROVIDER_PUBLIC["UNDETERMINED"], (
        "Section 12 open-gap suggested_provider is not the exact public "
        "provider wording (Finding F1): %r" % (s12["suggested_provider"],))
    rendered = _html_provider_value(no_answer_journey["html"])
    assert rendered == SECTION_12_PROVIDER_PUBLIC["UNDETERMINED"], (
        "The rendered HTML Suggested-provider field is not the exact public "
        "provider wording (Finding F1): %r" % (rendered,))


def test_defect3_section12_all_gap_types_public_mapping():
    """RED (F1, exact values): for each of the six committed gap types, the
    real assembler's open-gap Section 12 payload must carry exactly the
    committed inventor-facing gap label and exactly the public UNDETERMINED
    provider wording. Exercises the real assemble_deliverable path with a
    minimal one-open-gap state per gap type."""
    for raw, public in SECTION_12_GAP_PUBLIC.items():
        state = IdeaState(idea_id="hygiene-f1-gap-mapping")
        state.gaps.append(Gap(gap_type=raw, status=OPEN, opened_at=1))
        s12 = assemble_deliverable(state)["section_12_next_development_step"]
        assert s12["issue_type"] == "open_gap", (
            "fixture integrity: a single open %s gap must reach the open-gap "
            "payload" % raw)
        assert s12["reference_id"] == public, (
            "Section 12 reference_id for gap type %s is not the exact "
            "committed public label (Finding F1): %r" % (raw, s12["reference_id"]))
        assert s12["suggested_provider"] == SECTION_12_PROVIDER_PUBLIC["UNDETERMINED"], (
            "Section 12 suggested_provider for gap type %s is not the exact "
            "public wording (Finding F1): %r" % (raw, s12["suggested_provider"]))


def test_defect3_section12_owner_input_public_value(ws1_journey):
    """RED (F1, exact values): the owner-unvalidated Section 12 payload must
    keep its rec_N reference id UNCHANGED while the OWNER_INPUT provider token
    is exported as the exact public wording — verified byte-exact in the JSON
    package AND in the rendered HTML field."""
    s12 = ws1_journey["package"]["section_12_next_development_step"]
    assert s12["actionable"] is True and s12["issue_type"] == "owner_unvalidated", (
        "fixture integrity: the WS1 journey must reach the owner-unvalidated "
        "next-development-step payload — the fixture no longer exercises the "
        "state under test")
    assert re.fullmatch(r"rec_\d+", s12["reference_id"] or ""), (
        "Section 12 owner-unvalidated reference_id must remain the unchanged "
        "rec_N record id (Finding F1): %r" % (s12["reference_id"],))
    assert s12["suggested_provider"] == SECTION_12_PROVIDER_PUBLIC["OWNER_INPUT"], (
        "Section 12 owner-unvalidated suggested_provider is not the exact "
        "public wording (Finding F1): %r" % (s12["suggested_provider"],))
    rendered = _html_provider_value(ws1_journey["html"])
    assert rendered == SECTION_12_PROVIDER_PUBLIC["OWNER_INPUT"], (
        "The rendered HTML Suggested-provider field is not the exact public "
        "wording (Finding F1): %r" % (rendered,))


# ==========================================================================
# Defect 4 — count basis and relationship clarity, sections 4/13/14 ONLY
# (contract §7 and §10 items 4–9; owner authorization §4). Counts in other
# sections are observation-only and are deliberately not asserted.
# ==========================================================================

def test_defect4_section4_count_basis_and_total(ws1_journey):
    """RED (contract §10 item 4): section_4 must declare
    count_basis == 'evidence_derived_requirements' and its total must equal
    the length of exactly that collection."""
    s4 = ws1_journey["package"]["section_4_requirements"]
    assert s4.get("count_basis") == SECTION_4_COUNT_BASIS, (
        "section_4 declares no contract-bound count basis (expected "
        "count_basis=%r, found %r) — contract §7.1" % (
            SECTION_4_COUNT_BASIS, s4.get("count_basis")))
    assert s4["total"] == len(s4["requirements"])


def test_defect4_section13_count_basis_and_total(ws1_journey):
    """RED (contract §10 item 5): section_13 must declare
    count_basis == 'requirement_landscape' and its total must equal the
    length of exactly that collection."""
    s13 = ws1_journey["package"]["section_13_requirement_landscape"]
    assert s13.get("count_basis") == SECTION_13_COUNT_BASIS, (
        "section_13 declares no contract-bound count basis (expected "
        "count_basis=%r, found %r) — contract §7.2" % (
            SECTION_13_COUNT_BASIS, s13.get("count_basis")))
    assert s13["total"] == len(s13["requirements"])


def test_defect4_section14_validation_plan_source(ws1_journey):
    """RED (contract §7.4): section_14 must declare
    validation_plan_source == 'requirement_landscape'."""
    s14 = ws1_journey["package"]["section_14_validation_plan"]
    assert s14.get("validation_plan_source") == SECTION_14_PLAN_SOURCE, (
        "section_14 declares no contract-bound validation_plan_source "
        "(expected %r, found %r) — contract §7.4" % (
            SECTION_14_PLAN_SOURCE, s14.get("validation_plan_source")))


def test_defect4_section14_step_total(ws1_journey):
    """RED (contract §10 item 6): section_14 must expose
    validation_step_total == len(steps)."""
    s14 = ws1_journey["package"]["section_14_validation_plan"]
    assert "validation_step_total" in s14, (
        "section_14 exposes no validation_step_total field — contract §7.4")
    assert s14["validation_step_total"] == len(s14["steps"])


def test_defect4_section14_blocked_total(ws1_journey):
    """RED (contract §10 item 7): section_14 must expose
    blocked_item_total == len(blocked_items)."""
    s14 = ws1_journey["package"]["section_14_validation_plan"]
    assert "blocked_item_total" in s14, (
        "section_14 exposes no blocked_item_total field — contract §7.4")
    assert s14["blocked_item_total"] == len(s14["blocked_items"])


def test_defect4_arithmetic_tie_to_section13(ws1_journey):
    """RED (contract §10 item 8): the bound arithmetic relationship
    validation_step_total + blocked_item_total == section_13 total must hold
    via the declared fields."""
    pkg = ws1_journey["package"]
    s13 = pkg["section_13_requirement_landscape"]
    s14 = pkg["section_14_validation_plan"]
    assert "validation_step_total" in s14 and "blocked_item_total" in s14, (
        "section_14 does not declare the totals required for the bound "
        "arithmetic tie to section_13 — contract §7.4")
    assert s14["validation_step_total"] + s14["blocked_item_total"] == s13["total"]


def test_defect4_relationship_metadata_distinct_sets(ws1_journey):
    """RED (contract §7.3 / §9.6; contract §10 item 9): the package must carry
    machine-checkable §4<->§13 relationship metadata declaring that the
    evidence-derived set is a narrower view and NOT the same collection as
    the Requirement Landscape. This test requires the two bound count_basis
    identifiers to be present and DISTINCT and a machine-readable
    count_relationship declaration referencing both; it deliberately does NOT
    require section_4 total == section_13 total (the sets must never be
    artificially collapsed)."""
    pkg = ws1_journey["package"]
    s4 = pkg["section_4_requirements"]
    s13 = pkg["section_13_requirement_landscape"]
    assert s4.get("count_basis") == SECTION_4_COUNT_BASIS, (
        "section_4 count_basis missing — contract §7.1")
    assert s13.get("count_basis") == SECTION_13_COUNT_BASIS, (
        "section_13 count_basis missing — contract §7.2")
    assert s4.get("count_basis") != s13.get("count_basis")
    relationship = s4.get("count_relationship") or s13.get("count_relationship")
    assert relationship, (
        "no machine-checkable section_4<->section_13 count_relationship "
        "metadata is declared — contract §7.3/§9.6")
    blob = str(relationship)
    assert SECTION_4_COUNT_BASIS in blob and SECTION_13_COUNT_BASIS in blob, (
        "count_relationship metadata does not reference both bound "
        "identifiers — contract §7.3")


# ==========================================================================
# Guards (contract §10 items 10–11) — expected to PASS on the base and to
# keep passing after implementation. Not RED.
# ==========================================================================

def test_guard_safety_signal_block_matches_direct_derivation(ws1_journey,
                                                             positive_journey):
    """Guard (contract §6): the Safety-Signal block embedded in the package
    must be semantically identical to the direct engine derivation — the
    deliverable boundary must not alter signal content, count, or ordering.
    Verified on both the false-negative and the positive baseline journeys."""
    for journey in (ws1_journey, positive_journey):
        state = journey["state"]
        block = journey["package"]["_session_meta"]["inventor_stated_safety_signals"]
        direct = derive_inventor_stated_safety_signals(state)
        assert block["total"] == len(direct)
        for rendered, signal in zip(block["signals"], direct):
            for field in ("signal_id", "source", "provenance", "safety_subject",
                          "failure_condition", "possible_consequence",
                          "domain_context", "validation_status", "display_label",
                          "caution_text", "statement"):
                assert rendered[field] == getattr(signal, field), (
                    "Safety-Signal semantic delta at deliverable boundary: "
                    "field %r differs (contract §6.1 STOP condition)" % field)


def test_guard_ws1_ws2_evidence_trees_untouched():
    """Guard (contract §10 item 11 / §17): the immutable Workstream 1 and
    Workstream 2 evidence trees are byte-identical to their canonical pinned
    content."""
    assert _dir_content_sha256(WS1_EVIDENCE_DIR) == WS1_EVIDENCE_CONTENT_SHA256
    assert _dir_content_sha256(WS2_EVIDENCE_DIR) == WS2_EVIDENCE_CONTENT_SHA256


def test_guard_fixture_inputs_contain_no_prohibited_token(ws1_journey,
                                                          asserted_journey,
                                                          positive_journey):
    """Guard (fixture integrity): the controlled inventor inputs of every
    journey contain no Prohibited Token, so every token found by the Defect 3
    scans is necessarily system-generated leakage, never inventor text — the
    scans cannot be satisfied or defeated through the exemption rule."""
    for journey in (ws1_journey, asserted_journey, positive_journey):
        joined = "\n".join(journey["inputs"])
        for token, rx in _TOKEN_RES.items():
            assert not rx.search(joined), (
                "fixture integrity violated: inventor input contains "
                "prohibited token %r" % token)
