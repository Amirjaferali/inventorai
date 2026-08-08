"""P7-I1 — Internal Read/Export Service Boundary.

A small, Flask-free internal application/use-case seam exposing exactly two
read-side use cases so future internal consumers (the web UI, the future P7-I2
public API, future adapters) can use a governed application seam instead of
coupling directly to persistence or presentation-layer internals:

    * ``get_authorized_project_read``  — an authorized durable Project Read.
    * ``produce_project_export``       — a distinct, deterministic internal
                                         Structured Export.

This seam is INTERNAL ONLY; it exposes no public API/route and freezes no public
wire schema or export version identity (those remain P7-I2 concerns).

Established contract:
``docs/governance/P7_I1_INTERNAL_READ_EXPORT_SERVICE_BOUNDARY_INCREMENT_CONTRACT.md``
(P7-C §8 first slice; PR #402). Binding rules honoured here:

* IR-1 — the caller supplies an ALREADY-ESTABLISHED store; this module never
  constructs or initializes a datastore. Non-mutation applies to the service
  operation itself; the store lifecycle is outside P7-I1.
* IR-2 — reads use the durable validated ``store.load_contract`` path, never
  ``ProjectRecordContract.from_state(live_state)``.
* IR-3 — authorization CONSUMES the existing Flask-free durable ownership fact
  source ``store.load_owner``; no new authorization framework is created.
* IR-5 — the durable service authorizes ONLY the explicit caller that matches a
  present durable owner; a NULL durable owner is NOT automatic authorization. It
  fails closed on every other case. (Existing web legacy/anonymous behaviour is
  unchanged and out of this module's scope.)
* IR-6 — the Structured Export is semantically distinct from the Project Read (a
  data-minimized, deterministic outward projection composed from durable record
  data AND the canonical domain support-state), and freezes no public/export
  version or field names.

The Structured Export's domain support-state is derived from the EXISTING
canonical sources only — the durable ``confirmed_domain``
(``store.load_reconstruction_inputs``) classified by the canonical activation
policy (``engine.domain_activation.support_state``). No domain is activated, no
registry or activation behaviour is modified, and no support-state value is
invented (a NULL/legacy ``confirmed_domain`` yields the canonical
``UNKNOWN_OR_UNSUPPORTED`` state truthfully).

Caller identity and the store dependency are passed explicitly, so the seam is
independently callable and depends on no Flask request/session/``SESSION_STORE``.
"""

from engine import domain_activation


class ProjectAccessDenied(Exception):
    """Generic, non-enumerating denial for the internal durable read/export
    service. Raised identically for every unauthorized case (cross-owner,
    missing/None caller identity, NULL durable owner, missing durable project,
    ownership-lookup failure) so a denial never discloses whether the project
    exists, who owns it, or why access failed."""


def _is_authorized(store, project_id, account_id):
    """True only when durable canonical ownership establishes that the explicit
    caller owns ``project_id``: the durable project exists, a durable owner is
    present, and it equals ``account_id``. Fails closed on anything else,
    including any ownership-lookup error and a NULL durable owner (IR-3, IR-5)."""
    if not account_id:
        return False
    try:
        exists, owner = store.load_owner(project_id)
    except Exception:
        return False                       # fail closed on lookup failure
    if not exists or owner is None:
        return False                       # missing project or NULL owner → deny
    return owner == account_id


def get_authorized_project_read(store, project_id, account_id):
    """Return the authorized durable Project Read representation for
    ``project_id`` — the validated :class:`ProjectRecordContract` loaded via the
    durable ``store.load_contract`` path (IR-2) — or raise
    :class:`ProjectAccessDenied` if authorization is not established (fail
    closed). Performs no mutation."""
    if not _is_authorized(store, project_id, account_id):
        raise ProjectAccessDenied()
    return store.load_contract(project_id)


def produce_project_export(store, project_id, account_id):
    """Return a distinct, deterministic internal Structured Export for the
    authorized ``project_id``, composed from canonical durable record data AND
    the canonical domain support-state. Raises :class:`ProjectAccessDenied` if
    unauthorized. Performs no mutation and freezes no public/export version or
    field names (IR-6)."""
    if not _is_authorized(store, project_id, account_id):
        raise ProjectAccessDenied()
    contract = store.load_contract(project_id)
    support_state = _domain_support_state(store, project_id)
    return _compose_export(contract, support_state)


def _domain_support_state(store, project_id):
    """The canonical domain support-state for ``project_id`` derived from
    existing canonical sources only: the durable ``confirmed_domain`` (or ``None``
    when the project is legacy / has no reconstruction inputs) classified by
    ``engine.domain_activation.support_state``. Read-only; activates nothing and
    modifies no registry/activation behaviour. A NULL/legacy domain yields the
    canonical ``UNKNOWN_OR_UNSUPPORTED`` value truthfully."""
    inputs = store.load_reconstruction_inputs(project_id)
    domain = inputs.get("confirmed_domain") if inputs else None
    return domain_activation.support_state(domain)


def _compose_export(contract, domain_support_state):
    """Deterministic, data-minimized outward projection composed from the
    canonical record AND the canonical domain support-state.

    Semantically distinct from the Project Read: instead of the lossless record
    serialization it selects a governed per-assertion subset, adds derived
    counts, and carries the canonical domain support-state. Every value is
    grounded in an existing canonical source; no data is invented, no timestamp
    is introduced, and no public/export version identity is frozen. Given
    unchanged canonical state it is byte-stable."""
    assertions = list(getattr(contract, "assertions", []))
    projected = [
        {
            "record_id": a.record_id,
            "disposition": a.disposition,
            "provenance": a.provenance,
            "validation_status": a.validation_status,
        }
        for a in assertions
    ]
    validation_summary = {}
    provenance_summary = {}
    for a in assertions:
        validation_summary[a.validation_status] = (
            validation_summary.get(a.validation_status, 0) + 1)
        provenance_summary[a.provenance] = (
            provenance_summary.get(a.provenance, 0) + 1)
    return {
        "idea_id": contract.idea_id,
        "domain_support_state": domain_support_state,
        "assertion_count": len(assertions),
        "validation_summary": dict(sorted(validation_summary.items())),
        "provenance_summary": dict(sorted(provenance_summary.items())),
        "assertions": projected,
    }
