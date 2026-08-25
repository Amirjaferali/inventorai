"""P4-0 — Readiness and Storage-Contract Proof (datastore-neutral record contract).

A provider-free, datastore-neutral, versioned record contract that serializes
and losslessly restores the minimum readiness-relevant Phase 4 accepted-source
data as JSON-compatible dictionaries, using only the Python standard library.

Governed by the P4-0 Increment Contract Candidate in
`docs/governance/ACTIVE_INCREMENT_CONTRACT.md` (G-P4-0-DOC-01, merged PR #352).

This module is a CONTRACT PROOF, not a persistence implementation. It
introduces no datastore, ORM, driver, provider, network, credentials, or
external dependency, and no durable storage. Scope boundary:

  * P4-0 (here) proves contract representation, versioning, JSON round-trip,
    authoritative-field fidelity, identifier preservation, relationship
    validation, and a FRESH `derive_readiness` call over restored
    readiness-relevant state.
  * P4-1 owns durable storage, adapters, transactions, runtime integration,
    migration, persistent isolation, the durable identifier strategy, and
    provenance mapping.
  * P4-2 owns full deterministic rebuild/replay from accepted source inputs,
    deterministic output records, and stale-output invalidation.

Authoritative accepted-source values are preserved verbatim (including the
current provenance vocabulary `OWNER_STATED` / `LEGACY_UNSPECIFIED`). No
mapping to any future vocabulary is performed, and no AI provenance values are
introduced — that mapping is deferred to P4-1. Derived/cached conclusions
(readiness, last_result) are NOT serialized and NOT treated as authoritative;
readiness is always freshly derived from restored records.
"""
import json
from dataclasses import dataclass, field

from engine.idea_state import (
    AssertionRecord, IdeaState,
    DECISION_ACTION_DISPOSITIONS, LEGACY_INTERACTION_DISPOSITIONS,
    DISPOSITION_DECISION_CONTEXT_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_DECLARED,
    DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN,
)

# One minimal supported contract version. Unknown versions fail explicitly.
CONTRACT_VERSION = "p4-0-record-contract-v1"


class ContractError(ValueError):
    """Base class for record-contract validation failures."""


class UnknownVersionError(ContractError):
    """Raised when a serialized contract carries an unsupported version."""


class UnknownFieldError(ContractError):
    """Raised when serialized data omits a required field or carries an
    unknown field (prevents silent field loss in either direction)."""


class InvalidReferenceError(ContractError):
    """Raised when a relationship reference targets a nonexistent record or a
    record references itself for supersession."""


class RelationshipCycleError(ContractError):
    """Raised when the supersession graph contains a cycle."""


# Exact authoritative field set of one accepted-input (assertion) record. The
# round-trip is lossless over exactly these fields; anything else is rejected.
_ASSERTION_FIELDS = (
    "record_id", "disposition", "content", "gap_context", "iteration",
    "provenance", "validation_status", "quality", "pending", "responsibility",
    "resolves_gap", "contradicts", "supersedes", "superseded_by",
    # W2-A (authoritative contract §3/§4, PR #567): explicit decision-context
    # attachment. The ONLY loader relaxation is the bounded legacy rule in
    # `assertion_from_dict` below; decision-action payloads get no escape.
    "decision_context_root",
)

_ENVELOPE_FIELDS = ("contract_version", "idea_id", "assertions")


def assertion_to_dict(record):
    """Serialize one AssertionRecord to a JSON-compatible dict (all
    authoritative fields; verbatim values; link lists copied)."""
    return {
        "record_id": record.record_id,
        "disposition": record.disposition,
        "content": record.content,
        "gap_context": record.gap_context,
        "iteration": record.iteration,
        "provenance": record.provenance,
        "validation_status": record.validation_status,
        "quality": record.quality,
        "pending": record.pending,
        "responsibility": record.responsibility,
        "resolves_gap": record.resolves_gap,
        "contradicts": list(record.contradicts),
        "supersedes": list(record.supersedes),
        "superseded_by": record.superseded_by,
        "decision_context_root": record.decision_context_root,
    }


def reconcile_supersession_edges(assertions):
    """PVCG-R4-C §6 C-3 — derive the INVERSE supersession edge on load.

    The durable store is INSERT-only (``SqliteRecordStore.append_record`` issues a
    single INSERT and the adapter contains no UPDATE statement at all), so when a
    correction supersedes an earlier accepted record only the NEW row can carry the
    relationship. It carries it FORWARD as ``supersedes=[prior_id]``; the prior
    row's persisted payload still says ``superseded_by=None`` because it was never
    — and must never be — rewritten (§6 C-2, §7 S-1).

    This function restores the inverse deterministically, so the ONE canonical
    active-set concept already consumed by ``derived_readiness``,
    ``requirement_landscape``, ``idea_development_outputs``, ``validation_plan`` and
    ``safety_signal`` (``superseded_by is None``) keeps working unchanged. R4
    introduces no second active-set model (§7 S-4).

    Strictly ADDITIVE and IDEMPOTENT:
      * a ``superseded_by`` that is already set is NEVER overwritten;
      * it is filled in ONLY when it is ``None`` and some record names this one in
        its ``supersedes`` list;
      * a stored value that CONTRADICTS the forward edge is a corruption and raises
        ``InvalidReferenceError`` — it is never silently repaired;
      * two different records superseding the same prior record is likewise
        rejected: the inverse edge must be single-valued.

    It repairs nothing else, deletes nothing, reorders nothing, and renumbers
    nothing. ``validate()`` still runs afterwards with its existing strength intact
    (unknown references, self-supersession, and cycles all still fail closed —
    §14 P-4)."""
    forward = {}
    for record in assertions:
        for prior_id in record.supersedes:
            if prior_id in forward and forward[prior_id] != record.record_id:
                raise InvalidReferenceError(
                    "record %r is superseded by more than one record: %r and %r"
                    % (prior_id, forward[prior_id], record.record_id))
            forward[prior_id] = record.record_id
    for record in assertions:
        by_id = forward.get(record.record_id)
        if by_id is None:
            continue
        if record.superseded_by is None:
            record.superseded_by = by_id
        elif record.superseded_by != by_id:
            raise InvalidReferenceError(
                "supersession edges disagree for record %r: stored %r, "
                "forward edge %r"
                % (record.record_id, record.superseded_by, by_id))
    return assertions


def assertion_from_dict(data):
    """Reconstruct one AssertionRecord, rejecting unknown or missing fields so
    nothing is silently dropped. Values are restored verbatim."""
    if not isinstance(data, dict):
        raise UnknownFieldError("assertion record must be a dict")
    keys = set(data)
    unknown = keys - set(_ASSERTION_FIELDS)
    if unknown:
        raise UnknownFieldError(
            "unknown assertion field(s): %s" % sorted(unknown))
    missing = set(_ASSERTION_FIELDS) - keys
    if missing == {"decision_context_root"} \
            and data.get("disposition") in LEGACY_INTERACTION_DISPOSITIONS:
        # W2-A contract §4 — the ONE bounded compatibility relaxation: a
        # pre-W2-A payload (legacy disposition) may omit exactly the new
        # optional field and loads with None. Decision-action payloads never
        # take this branch; every other missing field still fails below.
        data = dict(data, decision_context_root=None)
        missing = set()
    if missing:
        raise UnknownFieldError(
            "missing required assertion field(s): %s" % sorted(missing))
    return AssertionRecord(
        record_id=data["record_id"],
        disposition=data["disposition"],
        content=data["content"],
        gap_context=data["gap_context"],
        iteration=data["iteration"],
        provenance=data["provenance"],
        validation_status=data["validation_status"],
        quality=data["quality"],
        pending=data["pending"],
        responsibility=data["responsibility"],
        resolves_gap=data["resolves_gap"],
        contradicts=list(data["contradicts"]),
        supersedes=list(data["supersedes"]),
        superseded_by=data["superseded_by"],
        decision_context_root=data["decision_context_root"],
    )


@dataclass
class ProjectRecordContract:
    """Datastore-neutral, versioned envelope of authoritative accepted-source
    records for one project/idea. Round-trips losslessly via to_dict/from_dict
    (and to_json/from_json) and validates relationship integrity on restore."""

    idea_id: str
    assertions: list = field(default_factory=list)
    contract_version: str = CONTRACT_VERSION

    # --- construction from live in-memory state (read-only) -----------------
    @classmethod
    def from_state(cls, state):
        """Build a contract from an IdeaState WITHOUT mutating it. Only
        authoritative accepted-source records are captured; derived/cached
        fields (maturity, gaps, readiness, last_result) are intentionally
        excluded."""
        return cls(
            idea_id=state.idea_id,
            assertions=list(getattr(state, "assertions", [])),
            contract_version=CONTRACT_VERSION,
        )

    # --- serialization ------------------------------------------------------
    def to_dict(self):
        return {
            "contract_version": self.contract_version,
            "idea_id": self.idea_id,
            "assertions": [assertion_to_dict(r) for r in self.assertions],
        }

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), sort_keys=True, **kwargs)

    # --- deserialization ----------------------------------------------------
    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise UnknownFieldError("contract must be a dict")
        unknown = set(data) - set(_ENVELOPE_FIELDS)
        if unknown:
            raise UnknownFieldError(
                "unknown contract field(s): %s" % sorted(unknown))
        version = data.get("contract_version")
        if version != CONTRACT_VERSION:
            raise UnknownVersionError(
                "unsupported contract_version: %r (supported: %r)"
                % (version, CONTRACT_VERSION))
        if "idea_id" not in data or "assertions" not in data:
            raise UnknownFieldError(
                "missing required contract field(s): %s"
                % sorted({"idea_id", "assertions"} - set(data)))
        assertions = [assertion_from_dict(d) for d in data["assertions"]]
        reconcile_supersession_edges(assertions)
        contract = cls(idea_id=data["idea_id"], assertions=assertions,
                       contract_version=version)
        contract.validate()
        return contract

    @classmethod
    def from_json(cls, text):
        return cls.from_dict(json.loads(text))

    # --- integrity invariants ----------------------------------------------
    def validate(self):
        """Validate relationship integrity: every reference targets an existing
        record, no record supersedes itself, and the supersession graph is
        acyclic. Fails explicitly; never mutates or repairs records."""
        by_id = {}
        for r in self.assertions:
            by_id[r.record_id] = r
        ids = set(by_id)
        for r in self.assertions:
            for ref in r.contradicts:
                if ref not in ids:
                    raise InvalidReferenceError(
                        "contradiction reference to unknown record: %r" % ref)
            for ref in r.supersedes:
                if ref not in ids:
                    raise InvalidReferenceError(
                        "supersession reference to unknown record: %r" % ref)
            if r.superseded_by is not None and r.superseded_by not in ids:
                raise InvalidReferenceError(
                    "superseded_by reference to unknown record: %r"
                    % r.superseded_by)
            if r.superseded_by == r.record_id or r.record_id in r.supersedes:
                raise InvalidReferenceError(
                    "a record cannot supersede itself: %r" % r.record_id)
        # Acyclic supersession graph (follow superseded_by edges).
        for start in ids:
            node = start
            seen = set()
            while node is not None:
                if node in seen:
                    raise RelationshipCycleError(
                        "supersession cycle detected at record: %r" % node)
                seen.add(node)
                node = by_id[node].superseded_by
        # W2-A (contract §4) — load-side structural validation of persisted
        # decision-action records. Fail closed: an invalid persisted decision
        # payload never becomes live state. Mirrors the carrier mint rules
        # (structural legality only; decision semantics stay with FDC-001).
        for r in self.assertions:
            root_ref = getattr(r, "decision_context_root", None)
            if r.disposition not in DECISION_ACTION_DISPOSITIONS:
                if root_ref is not None:
                    raise InvalidReferenceError(
                        "legacy record %r carries a decision_context_root"
                        % r.record_id)
                for ref in r.supersedes:
                    if by_id[ref].disposition in DECISION_ACTION_DISPOSITIONS:
                        raise InvalidReferenceError(
                            "legacy record %r supersedes a decision-action "
                            "record" % r.record_id)
                continue
            if r.gap_context is not None:
                raise InvalidReferenceError(
                    "decision-action record %r carries a gap_context"
                    % r.record_id)
            if len(r.supersedes) > 1:
                raise InvalidReferenceError(
                    "decision-action record %r supersedes more than one "
                    "record (ID-11)" % r.record_id)
            if r.disposition == DISPOSITION_DECISION_CONTEXT_DECLARED:
                if root_ref is not None:
                    raise InvalidReferenceError(
                        "decision_context_declared record %r carries a "
                        "non-null decision_context_root" % r.record_id)
                for ref in r.supersedes:
                    if by_id[ref].disposition \
                            != DISPOSITION_DECISION_CONTEXT_DECLARED:
                        raise InvalidReferenceError(
                            "context refinement %r supersedes a non-context "
                            "record" % r.record_id)
                continue
            if root_ref is None or root_ref not in ids:
                raise InvalidReferenceError(
                    "decision-action record %r has a missing/unknown "
                    "decision_context_root" % r.record_id)
            root = by_id[root_ref]
            if root.disposition != DISPOSITION_DECISION_CONTEXT_DECLARED \
                    or root.supersedes:
                raise InvalidReferenceError(
                    "decision-action record %r does not reference a FOUNDING "
                    "context record" % r.record_id)
            if r.disposition == DISPOSITION_DECISION_ALTERNATIVE_WITHDRAWN \
                    and len(r.supersedes) != 1:
                raise InvalidReferenceError(
                    "withdrawal %r must supersede exactly one alternative"
                    % r.record_id)
            for ref in r.supersedes:
                target = by_id[ref]
                if target.disposition \
                        != DISPOSITION_DECISION_ALTERNATIVE_DECLARED:
                    raise InvalidReferenceError(
                        "decision-action record %r supersedes a record of "
                        "the wrong class" % r.record_id)
                if target.decision_context_root != root_ref:
                    raise InvalidReferenceError(
                        "cross-context decision supersession at record %r"
                        % r.record_id)
        return self

    # --- reconstruction of a state suitable for a FRESH readiness call ------
    def to_state(self):
        """Rebuild a minimal IdeaState carrying the restored append-only
        ledger, suitable for a FRESH `derive_readiness` call. No cached
        readiness is restored; readiness is recomputed by the engine. This is
        NOT full deterministic replay (that is P4-2)."""
        state = IdeaState(idea_id=self.idea_id)
        state.assertions = list(self.assertions)
        return state
