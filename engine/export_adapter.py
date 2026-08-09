"""P7-I3 — Canonical Export + Local/Reference Adapter Proof.

A single, local, deterministic, network-free, vendor-neutral **reference** adapter
(test-harness quality — NOT a production connector) that proves InventorAI can
transfer a canonical export through an integration/export boundary without
coupling Core to any vendor:

    canonical P7-I1 Structured Export
      → ReferenceExportAdapter.transform(...)   (deterministic, pure)
      → structurally distinct transformed representation
      → validate_equivalence(...)               (semantic, independent of transform)

Established contract:
``docs/governance/P7_I3_CANONICAL_EXPORT_LOCAL_REFERENCE_ADAPTER_PROOF_INCREMENT_CONTRACT.md``
(PR #408). Binding properties honoured here:

* Consumes the canonical **P7-I1 Structured Export** payload (shape
  ``{idea_id, domain_support_state, assertion_count, validation_summary,
  provenance_summary, assertions[{record_id, disposition, provenance,
  validation_status}]}``). No second canonical export/output model is created.
* **No invented export-version identity** — P7-I1 has none. Source provenance
  names the "P7-I1 Structured Export seam"; an OPTIONAL explicit
  ``source_version`` may be supplied at the boundary and is checked only when
  present (§3), against a caller-supplied recognized set.
* **Mandatory NON-EMPTY preservation floor** owned by this contract (§5):
  top-level ``idea_id`` / ``domain_support_state`` / ``assertion_count``; per
  assertion ``record_id`` / ``disposition`` / ``provenance`` / ``validation_status``.
* **Integrity/tamper detection** (§6): the validator fails on a changed floor
  field, a missing/duplicate assertion, a ``record_id`` collision, an
  ``assertion_count`` / ``validation_summary`` / ``provenance_summary`` row
  inconsistency, or a malformed representation — and it derives its expectations
  from the CANONICAL source (never by re-running ``transform``), so it detects
  adapter corruption.
* **Outbound-only, non-mutating, network-free, vendor-neutral.** The adapter/
  validator touch no store, no Flask/session, no network; they never persist,
  import, trust, or promote adapter output; adapter output is UNTRUSTED BY
  DEFAULT and has no effect on progression / evidence / domain activation.
"""

_FLOOR_TOP = ("idea_id", "domain_support_state", "assertion_count")
_FLOOR_ROW = ("record_id", "disposition", "provenance", "validation_status")


class AdapterError(Exception):
    """Bounded, explicit adapter/validation failure. Raised for invalid canonical
    input, unsupported explicit source version, transform error, malformed
    transformed result, or equivalence/integrity failure. Never mutates state and
    never promotes adapter output to trusted."""


def _require_canonical(canonical):
    """Validate the canonical P7-I1 Structured Export shape (fail closed)."""
    if not isinstance(canonical, dict):
        raise AdapterError("canonical export must be a dict")
    if "idea_id" not in canonical or "assertions" not in canonical:
        raise AdapterError("canonical export missing required fields")
    if not isinstance(canonical["assertions"], list):
        raise AdapterError("canonical assertions must be a list")
    for a in canonical["assertions"]:
        if not isinstance(a, dict) or not set(_FLOOR_ROW) <= set(a):
            raise AdapterError("canonical assertion missing floor field(s)")
    return canonical


def _summaries_from_rows(rows, status_key, prov_key):
    validation = {}
    provenance = {}
    for r in rows:
        validation[r[status_key]] = validation.get(r[status_key], 0) + 1
        provenance[r[prov_key]] = provenance.get(r[prov_key], 0) + 1
    return dict(sorted(validation.items())), dict(sorted(provenance.items()))


class ReferenceExportAdapter:
    """One local/reference adapter producing a deterministic, structurally
    distinct **flattened reference DTO** from the canonical export. Pure: it reads
    no store, opens no network, and mutates nothing."""

    adapter_id = "reference-flatten"
    adapter_version = "1"
    output_type = "flattened_reference_dto"

    def transform(self, canonical, source_version=None):
        c = _require_canonical(canonical)
        assertions = list(c["assertions"])
        # Deterministic rows in canonical assertion order; keys renamed so the
        # representation is structurally distinct from the canonical shape.
        records = [
            {
                "id": a["record_id"],
                "disposition": a["disposition"],
                "provenance": a["provenance"],
                "validation_status": a["validation_status"],
            }
            for a in assertions
        ]
        validation_summary, provenance_summary = _summaries_from_rows(
            records, "validation_status", "provenance")
        return {
            "adapter": {
                "adapter_id": self.adapter_id,
                "adapter_version": self.adapter_version,
                "output_type": self.output_type,
                "source": "P7-I1 Structured Export seam",
                "source_version": source_version,
            },
            "project": {
                "idea_id": c["idea_id"],
                "domain_support_state": c.get("domain_support_state"),
                "assertion_count": len(records),
                "validation_summary": validation_summary,
                "provenance_summary": provenance_summary,
            },
            "records": records,
        }


def validate_equivalence(canonical, transformed, recognized_source_versions=None):
    """Semantic inverse/equivalence check of ``transformed`` against the CANONICAL
    source on the mandatory floor. Returns ``"valid"`` or raises
    :class:`AdapterError`. Derives all expectations from ``canonical`` (never by
    re-running the transform), so adapter corruption is detected."""
    c = _require_canonical(canonical)

    # Structural shape.
    if not isinstance(transformed, dict):
        raise AdapterError("transformed representation must be a dict")
    for section in ("adapter", "project", "records"):
        if section not in transformed:
            raise AdapterError("transformed missing section: %s" % section)
    project = transformed["project"]
    rows = transformed["records"]
    if not isinstance(project, dict) or not isinstance(rows, list):
        raise AdapterError("transformed project/records malformed")
    if not set(_FLOOR_TOP) <= set(project):
        raise AdapterError("transformed project missing floor field(s)")
    for r in rows:
        if not isinstance(r, dict) or not {"id", "disposition", "provenance",
                                           "validation_status"} <= set(r):
            raise AdapterError("transformed record missing floor field(s)")

    # Optional explicit source version — checked ONLY when supplied.
    supplied_version = transformed["adapter"].get("source_version")
    if supplied_version is not None:
        recognized = recognized_source_versions or frozenset()
        if supplied_version not in recognized:
            raise AdapterError("unsupported source version: %r" % (supplied_version,))

    # Top-level floor equivalence with canonical.
    if project["idea_id"] != c["idea_id"]:
        raise AdapterError("idea_id mismatch")
    if project["domain_support_state"] != c.get("domain_support_state"):
        raise AdapterError("domain_support_state mismatch")

    # Population + duplicate/collision detection (never collapse by record_id).
    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        raise AdapterError("record_id collision / duplicate assertion")
    canonical_by_id = {}
    for a in c["assertions"]:
        if a["record_id"] in canonical_by_id:
            raise AdapterError("canonical contains duplicate record_id")
        canonical_by_id[a["record_id"]] = a
    if len(ids) != len(canonical_by_id):
        raise AdapterError("assertion population mismatch (missing/extra rows)")
    if project["assertion_count"] != len(rows):
        raise AdapterError("assertion_count inconsistent with rows")
    if len(rows) != c.get("assertion_count", len(canonical_by_id)):
        raise AdapterError("assertion_count inconsistent with canonical")

    # Per-record floor equivalence.
    for r in rows:
        src = canonical_by_id.get(r["id"])
        if src is None:
            raise AdapterError("transformed record has no canonical source: %r" % (r["id"],))
        if (r["disposition"] != src["disposition"]
                or r["provenance"] != src["provenance"]
                or r["validation_status"] != src["validation_status"]):
            raise AdapterError("preservation-floor field changed for %r" % (r["id"],))

    # Summary consistency: derive from the transformed rows and require agreement
    # with both the transformed's declared summaries AND the canonical summaries.
    row_validation, row_provenance = _summaries_from_rows(
        rows, "validation_status", "provenance")
    if "validation_summary" in project and project["validation_summary"] != row_validation:
        raise AdapterError("validation_summary inconsistent with rows")
    if "provenance_summary" in project and project["provenance_summary"] != row_provenance:
        raise AdapterError("provenance_summary inconsistent with rows")
    if "validation_summary" in c and row_validation != dict(sorted(c["validation_summary"].items())):
        raise AdapterError("validation_summary inconsistent with canonical")
    if "provenance_summary" in c and row_provenance != dict(sorted(c["provenance_summary"].items())):
        raise AdapterError("provenance_summary inconsistent with canonical")

    return "valid"
