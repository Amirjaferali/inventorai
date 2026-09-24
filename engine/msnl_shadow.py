"""MSNL local-only shadow — Candidate 01 (proposal-only, no provider).

File path      : engine/msnl_shadow.py
Purpose        : the local, side-effect-free SHADOW seam of the existing
                 Stage-18 semantic-normalization item (MSNL). It (a) captures an
                 ALREADY-ACCEPTED owner event as a detached immutable observation,
                 and (b) offers a pure local evaluation harness that maps that
                 observation to a normalization PROPOSAL against the EXISTING
                 governed concept inventory of ``engine.semantic_registry``.
Authority      : Owner authorization "MSNL LOCAL-ONLY SHADOW IMPLEMENTATION
                 CANDIDATE 01" (incorporating the Astra architecture verdict PASS
                 WITH REQUIRED CORRECTIONS). No external provider, no model call,
                 no network, no persistence, no user-visible output.

CAPTURE IS NOT EVALUATION
-------------------------
The live web request may call ``capture_accepted_event`` ONLY. Capture builds a
detached observation and hands it to a sink; the production switch is OFF and the
Candidate-01 sink discards. Nothing here is persisted, logged, queued, threaded
or retained. Adapters and ``evaluate`` are exercised only by the local
test/evaluation harness — never by the web layer, and never by the deterministic
engine or its replay.

WHAT A PROPOSAL IS NOT
----------------------
A proposal is never OWNER_STATED, never evidence, never a gap/maturity/readiness/
validation input, and never an ``AssertionRecord`` or ``Evidence`` field. The
deterministic engine continues to consume the accepted owner text exactly as
before; no engine module imports this one (machine-checked in
``tests/test_msnl_shadow.py``).

CLOSED VOCABULARY
-----------------
Candidate concepts are derived HERE from ``semantic_registry.CONCEPTS`` for the
served gap only. A caller-supplied inventory has no authority, a proposed id
outside the served gap's registered concepts is discarded, and this module adds
no concept, no surface and no ownership change.

Prohibited     : I/O, logging, network, clock, randomness, persistence, state
                 mutation of any engine object, import of ``engine.ai_advisor``.
"""

from dataclasses import dataclass

from engine.semantic_registry import CONCEPTS, GOVERNED_OWNERS, activated_concepts

#: The local shadow schema identity. Deliberately distinct from, and never
#: derived from, a project's engine-contract version.
SHADOW_SCHEMA_VERSION = "msnl-shadow-local-01"

# Accepted-event kinds and correction application status.
EVENT_ANSWERED = "ANSWERED"
EVENT_CORRECTION = "CORRECTION"
CORRECTION_APPLIED = "APPLIED"
CORRECTION_SAVED_NOT_APPLIED = "SAVED_NOT_APPLIED"

# Adapter outcomes.
PROPOSED = "PROPOSED"
ABSTAIN = "ABSTAIN"
NO_MAPPING = "NO_MAPPING"
ERROR = "ERROR"
OUTCOMES = frozenset({PROPOSED, ABSTAIN, NO_MAPPING, ERROR})

# Local policy dispositions (assigned by ``evaluate``, never by an adapter).
DISPOSITION_PROPOSAL = "PROPOSAL"
DISPOSITION_ABSTAINED = "ABSTAINED"
DISPOSITION_NO_MAPPING = "NO_MAPPING"
DISPOSITION_ADAPTER_ERROR = "ADAPTER_ERROR"
DISPOSITION_DISCARDED_UNSUPPORTED = "DISCARDED_UNSUPPORTED"


def _nonempty_str(value):
    return isinstance(value, str) and value != ""


# ─────────────────────────────────────────────────────────────────────────────
# 1. THE DETACHED ACCEPTED EVENT
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class LocalRef:
    """Project-scoped local correlation. ``record_id`` alone is not globally
    unique, so the project/session reference is always carried with it. Never
    part of a shadow request."""

    project_ref: str
    record_id: str

    def __post_init__(self):
        if not (_nonempty_str(self.project_ref) and _nonempty_str(self.record_id)):
            raise ValueError("local reference needs a project ref and a record id")


@dataclass(frozen=True)
class AcceptedEvent:
    """An already-accepted owner event, detached from every live object.

    ``accepted_text`` is the text the route accepted AFTER its existing
    ``.strip()`` — not a claim about the raw HTTP field. ``gap_type`` and
    ``question_target`` are None only when genuinely absent."""

    ref: LocalRef
    accepted_text: str
    gap_type: object
    question_target: object
    domain: str
    kind: str
    correction_status: object = None

    def __post_init__(self):
        if not isinstance(self.ref, LocalRef):
            raise ValueError("ref must be a LocalRef")
        if not _nonempty_str(self.accepted_text):
            raise ValueError("accepted_text must be non-empty text")
        if self.gap_type is not None and self.gap_type not in GOVERNED_OWNERS:
            raise ValueError("gap_type must be a governed gap or None")
        # The durable record contract: None, or a non-empty string. Never
        # normalized, trimmed or inferred here.
        if self.question_target is not None and not _nonempty_str(self.question_target):
            raise ValueError("question_target must be None or non-empty text")
        if not _nonempty_str(self.domain):
            raise ValueError("domain must be the admitted domain id")
        if self.kind == EVENT_ANSWERED:
            if self.correction_status is not None:
                raise ValueError("an answered event has no correction status")
        elif self.kind == EVENT_CORRECTION:
            if self.correction_status not in (CORRECTION_APPLIED,
                                              CORRECTION_SAVED_NOT_APPLIED):
                raise ValueError("a correction needs APPLIED or SAVED_NOT_APPLIED")
        else:
            raise ValueError("unknown event kind")


# ─────────────────────────────────────────────────────────────────────────────
# 2. THE LIVE CAPTURE SEAM (the ONLY entry point the web layer may call)
# ─────────────────────────────────────────────────────────────────────────────

#: Production/default switch. OFF. Enabling it still only reaches the sink.
MSNL_CAPTURE_ENABLED = False


def _discard(event):
    """The Candidate-01 sink: retains nothing."""
    return None


#: The capture sink. Candidate 01 discards; tests may inject a collector.
_capture_sink = _discard


def capture_accepted_event(*, project_ref, record_id, accepted_text, gap_type,
                           question_target, domain, kind, correction_status=None):
    """Hand one already-accepted event to the local sink. Returns None.

    Performs no I/O, logging, persistence, adapter evaluation or engine
    mutation, receives only plain values (never a state, request, store or
    session object), and never raises: an invalid event or a failing sink is
    dropped silently so the product path is unaffected."""
    if not MSNL_CAPTURE_ENABLED:
        return None
    try:
        event = AcceptedEvent(
            ref=LocalRef(project_ref=project_ref, record_id=record_id),
            accepted_text=accepted_text, gap_type=gap_type,
            question_target=question_target, domain=domain, kind=kind,
            correction_status=correction_status)
        _capture_sink(event)
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────────────────────────────────────
# 3. PROVIDER-NEUTRAL REQUEST / RESPONSE CONTRACTS (local harness only)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class CandidateConcept:
    """One closed-vocabulary target: a registered concept id and its
    governed-question provenance, copied from ``semantic_registry``."""

    concept_id: str
    provenance: str


def candidate_concepts(gap_type):
    """The served gap's registered concepts, in committed registry order.

    Derived from ``semantic_registry.CONCEPTS`` only; a None or ungoverned gap
    yields no candidates (fail-closed)."""
    if gap_type not in GOVERNED_OWNERS:
        return ()
    return tuple(CandidateConcept(c.concept_id, c.provenance)
                 for c in CONCEPTS if c.owner == gap_type)


@dataclass(frozen=True)
class ShadowRequest:
    """The minimal adapter-facing payload. Carries no project, account, session
    or record identifier, no seed/summary/transcript, no engine state and no
    UI language. ``candidates`` must equal the registry-derived set for
    ``gap_type`` — a caller-supplied inventory is refused."""

    accepted_text: str
    gap_type: object
    question_target: object
    domain: str
    candidates: tuple
    schema_version: str = SHADOW_SCHEMA_VERSION

    def __post_init__(self):
        if self.candidates != candidate_concepts(self.gap_type):
            raise ValueError("candidates must be derived from the registry")
        if self.schema_version != SHADOW_SCHEMA_VERSION:
            raise ValueError("unknown shadow schema version")


def build_request(event):
    """The shadow request for one detached accepted event."""
    return ShadowRequest(
        accepted_text=event.accepted_text, gap_type=event.gap_type,
        question_target=event.question_target, domain=event.domain,
        candidates=candidate_concepts(event.gap_type))


@dataclass(frozen=True)
class ShadowResponse:
    """What an adapter returns. No correlation, rationale or timestamp.

    ``confidence`` is recorded as reported and has NO authority; the local
    policy never reads it. Membership of ``concept_ids`` in the closed
    candidate set is checked by the local policy, not trusted here."""

    outcome: str
    concept_ids: tuple = ()
    confidence: object = None

    def __post_init__(self):
        if self.outcome not in OUTCOMES:
            raise ValueError("unknown adapter outcome")
        if not isinstance(self.concept_ids, tuple) or not all(
                _nonempty_str(i) for i in self.concept_ids):
            raise ValueError("concept_ids must be a tuple of non-empty ids")
        if len(set(self.concept_ids)) != len(self.concept_ids):
            raise ValueError("concept_ids must not repeat")
        if self.outcome == PROPOSED and not self.concept_ids:
            raise ValueError("PROPOSED needs at least one concept id")
        if self.outcome != PROPOSED and self.concept_ids:
            raise ValueError(self.outcome + " must carry no concept ids")


# ─────────────────────────────────────────────────────────────────────────────
# 4. THE TWO LOCAL ADAPTERS
# ─────────────────────────────────────────────────────────────────────────────

class NullAdapter:
    """Always abstains."""

    name = "null"

    def propose(self, request):
        return ShadowResponse(ABSTAIN)


class LexicalBaselineAdapter:
    """UNCALIBRATED LEXICAL BASELINE over the registered surfaces.

    Returns ``semantic_registry.activated_concepts(accepted_text, gap_type)``.
    It is not an AI model, not semantic understanding, not ground truth and not
    evidence. It detects registered surfaces wherever they occur — including
    under negation — so a registered hit is NOT an owner-asserted fact. It
    reports no confidence."""

    name = "lexical-baseline-uncalibrated"

    def propose(self, request):
        hits = activated_concepts(request.accepted_text, request.gap_type)
        ids = tuple(c.concept_id for c in request.candidates if c.concept_id in hits)
        if not ids:
            return ShadowResponse(NO_MAPPING)
        return ShadowResponse(PROPOSED, ids, confidence=None)


# ─────────────────────────────────────────────────────────────────────────────
# 5. THE LOCAL EVALUATION HARNESS (never called by web or engine)
# ─────────────────────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ShadowResult:
    """The local adjudication of one proposal. Ephemeral; never persisted."""

    ref: LocalRef
    adapter_name: str
    outcome: str
    disposition: str
    concept_ids: tuple = ()
    schema_version: str = SHADOW_SCHEMA_VERSION


def evaluate(event, adapter):
    """Run one adapter on one detached event and apply the local policy.

    Precision first: an adapter failure or malformed reply is ADAPTER_ERROR; a
    proposal naming any id outside the served gap's registered concepts is
    DISCARDED_UNSUPPORTED as a whole (never trimmed or repaired); confidence is
    ignored. Nothing here touches engine state."""
    if not isinstance(event, AcceptedEvent):
        raise ValueError("evaluate needs an AcceptedEvent")
    name = getattr(adapter, "name", None)
    name = name if _nonempty_str(name) else "unnamed"
    request = build_request(event)
    try:
        response = adapter.propose(request)
    except Exception:
        response = None
    if not isinstance(response, ShadowResponse) or response.outcome == ERROR:
        return ShadowResult(event.ref, name, ERROR, DISPOSITION_ADAPTER_ERROR)
    if response.outcome == ABSTAIN:
        return ShadowResult(event.ref, name, ABSTAIN, DISPOSITION_ABSTAINED)
    if response.outcome == NO_MAPPING:
        return ShadowResult(event.ref, name, NO_MAPPING, DISPOSITION_NO_MAPPING)
    allowed = {c.concept_id for c in candidate_concepts(event.gap_type)}
    if not set(response.concept_ids) <= allowed:
        return ShadowResult(event.ref, name, PROPOSED,
                            DISPOSITION_DISCARDED_UNSUPPORTED)
    return ShadowResult(event.ref, name, PROPOSED, DISPOSITION_PROPOSAL,
                        response.concept_ids)
