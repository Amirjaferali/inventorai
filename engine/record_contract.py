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

from engine.idea_state import AssertionRecord, IdeaState

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
    }


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
