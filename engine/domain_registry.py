"""
engine/domain_registry.py

Phase 5 Step 3 — Domain Registry Loader
"""

import json
import os
import re
from types import MappingProxyType


class RegistryLoadError(Exception):
    pass


class DomainNotFoundError(KeyError):
    pass


_TOP_LEVEL_REQUIRED = (
    "taxonomy_group", "capability_id", "display_name", "description",
    "domain_signals", "gaps", "notes", "governance",
)

_GOVERNANCE_REQUIRED = (
    "source", "license", "owner", "review_date", "version", "deprecation_status",
)

_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
_ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_VALID_DEPRECATION_STATUSES = {"active", "deprecated", "sunset"}

# §5-I1 / D-P6-14 — Domain Registry validation hardening (governed by the accepted
# §5-C1 contract-of-record). These enforce the previously-unvalidated pack contract
# WITHOUT activating any domain and WITHOUT changing evaluation behavior.

# Pack `version` accepts MAJOR.MINOR or MAJOR.MINOR.PATCH (existing packs use "1.0";
# D-S5-C1 §8 keeps the smallest stable format that leaves current packs valid).
_PACK_VERSION_RE = re.compile(r"^\d+\.\d+(\.\d+)?$")

# Pack lifecycle/loader status (D-S5-03): this is LIFECYCLE ONLY and is NEVER
# runtime/user-facing activation (activation is a separate, unchanged concern).
# Canonical lifecycle values are `registered` / `deprecated`. Legacy `active` is
# accepted as a DEPRECATED compatibility alias for the registered lifecycle state so
# the four shipped v1.0 packs remain valid; it is not reinterpreted as activation.
# (Non-blocking observation for a future doc-sync: §5-C1 §8 names a per-pack
# governance block; per D-FPC-MAP-06 provenance is validated against the canonical
# domains/domain_provenance.json instead of duplicating a block into each pack.)
_VALID_PACK_STATUSES = {"registered", "deprecated", "active"}

_PROVENANCE_FILENAME = "domain_provenance.json"


def _validate_domain(data: dict, path: str) -> None:
    for field in _TOP_LEVEL_REQUIRED:
        if field not in data:
            raise RegistryLoadError(f"Missing required field '{field}' in {path}")
    if not isinstance(data["capability_id"], str) or not data["capability_id"].strip():
        raise RegistryLoadError(f"Field 'capability_id' must be a non-empty string in {path}")
    if not isinstance(data["domain_signals"], list) or len(data["domain_signals"]) == 0:
        raise RegistryLoadError(f"Field 'domain_signals' must be a non-empty list in {path}")
    if not isinstance(data["gaps"], list) or len(data["gaps"]) == 0:
        raise RegistryLoadError(f"Field 'gaps' must be a non-empty list in {path}")
    if not isinstance(data["governance"], dict):
        raise RegistryLoadError(f"Field 'governance' must be an object in {path}")
    gov = data["governance"]
    for field in _GOVERNANCE_REQUIRED:
        if field not in gov:
            raise RegistryLoadError(f"Missing required governance field '{field}' in {path}")
    if not _SEMVER_RE.match(str(gov["version"])):
        raise RegistryLoadError(
            f"governance.version '{gov['version']}' is not valid semver "
            f"(expected MAJOR.MINOR.PATCH) in {path}")
    if not _ISO_DATE_RE.match(str(gov["review_date"])):
        raise RegistryLoadError(
            f"governance.review_date '{gov['review_date']}' is not a valid "
            f"ISO-8601 date (expected YYYY-MM-DD) in {path}")
    if gov["deprecation_status"] not in _VALID_DEPRECATION_STATUSES:
        raise RegistryLoadError(
            f"governance.deprecation_status '{gov['deprecation_status']}' is not "
            f"a valid value {_VALID_DEPRECATION_STATUSES} in {path}")
    for field in ("source", "license", "owner"):
        if not isinstance(gov[field], str) or not gov[field].strip():
            raise RegistryLoadError(f"governance.{field} must be a non-empty string in {path}")


_V1_REQUIRED = (
    "schema_version", "pack_id", "version", "status",
    "display_name", "classification_signals", "substance_signals",
    "gap_type_mappings", "rule_nuances",
)


def _validate_domain_v1(data: dict, path: str) -> None:
    for field in _V1_REQUIRED:
        if field not in data:
            raise RegistryLoadError(
                f"Missing required v1.0 field '{field}' in {path}"
            )
    if not isinstance(data["pack_id"], str) or not data["pack_id"].strip():
        raise RegistryLoadError(
            f"Field 'pack_id' must be a non-empty string in {path}"
        )
    if not isinstance(data["classification_signals"], list) or len(data["classification_signals"]) == 0:
        raise RegistryLoadError(
            f"Field 'classification_signals' must be a non-empty list in {path}"
        )
    if not isinstance(data["substance_signals"], list) or len(data["substance_signals"]) == 0:
        raise RegistryLoadError(
            f"Field 'substance_signals' must be a non-empty list in {path}"
        )
    if not isinstance(data["gap_type_mappings"], list):
        raise RegistryLoadError(
            f"Field 'gap_type_mappings' must be a list in {path}"
        )
    if not isinstance(data["rule_nuances"], list):
        raise RegistryLoadError(
            f"Field 'rule_nuances' must be a list in {path}"
        )
    # --- §5-I1 / D-P6-14 element & value hardening -------------------------
    # version format
    if not _PACK_VERSION_RE.match(str(data["version"])):
        raise RegistryLoadError(
            f"Field 'version' '{data['version']}' is not a valid "
            f"MAJOR.MINOR[.PATCH] version in {path}"
        )
    # allowed lifecycle status values (lifecycle only — NOT activation)
    if data["status"] not in _VALID_PACK_STATUSES:
        raise RegistryLoadError(
            f"Field 'status' '{data['status']}' is not an allowed lifecycle "
            f"value {sorted(_VALID_PACK_STATUSES)} in {path}"
        )
    # gap_type_mappings element structure (matches the current consumer
    # engine.domain_rules.get_domain_question: gap_type_id + optional questions[].text)
    for i, mapping in enumerate(data["gap_type_mappings"]):
        if not isinstance(mapping, dict):
            raise RegistryLoadError(
                f"gap_type_mappings[{i}] must be an object in {path}"
            )
        gid = mapping.get("gap_type_id")
        if not isinstance(gid, str) or not gid.strip():
            raise RegistryLoadError(
                f"gap_type_mappings[{i}].gap_type_id must be a non-empty "
                f"string in {path}"
            )
        if "questions" in mapping:
            if not isinstance(mapping["questions"], list):
                raise RegistryLoadError(
                    f"gap_type_mappings[{i}].questions must be a list in {path}"
                )
            for j, q in enumerate(mapping["questions"]):
                if not isinstance(q, dict):
                    raise RegistryLoadError(
                        f"gap_type_mappings[{i}].questions[{j}] must be an "
                        f"object in {path}"
                    )
                txt = q.get("text")
                if not isinstance(txt, str) or not txt.strip():
                    raise RegistryLoadError(
                        f"gap_type_mappings[{i}].questions[{j}].text must be a "
                        f"non-empty string in {path}"
                    )
    # rule_nuances element structure — minimum: each element is an object.
    # modifier_value is deliberately NOT frozen (the governed minimal pack omits it).
    for i, rn in enumerate(data["rule_nuances"]):
        if not isinstance(rn, dict):
            raise RegistryLoadError(
                f"rule_nuances[{i}] must be an object in {path}"
            )



def _load_provenance_pack_ids(domains_dir: str):
    """§5-I1 / D-P6-14 — reuse the canonical provenance artifact (D-FPC-MAP-06).

    Returns the set of ``pack_id`` values that have at least one provenance record in
    ``domains/domain_provenance.json``, or ``None`` when no provenance manifest is
    present (isolated unit directories load unchanged — provenance coverage is
    soft-gated on the manifest's presence, never duplicated per pack).
    """
    prov_path = os.path.join(domains_dir, _PROVENANCE_FILENAME)
    if not os.path.isfile(prov_path):
        return None
    with open(prov_path, encoding="utf-8") as fh:
        try:
            prov = json.load(fh)
        except json.JSONDecodeError as exc:
            raise RegistryLoadError(f"Invalid JSON in {prov_path}: {exc}") from exc
    records = prov.get("records", [])
    if not isinstance(records, list):
        raise RegistryLoadError(f"'records' must be a list in {prov_path}")
    return {r.get("pack_id") for r in records if isinstance(r, dict)}


def load_registry(domains_dir: str) -> MappingProxyType:
    if not os.path.isdir(domains_dir):
        raise FileNotFoundError(f"domains_dir does not exist or is not a directory: {domains_dir}")
    provenance_ids = _load_provenance_pack_ids(domains_dir)
    registry = {}
    subdirs = sorted(entry.name for entry in os.scandir(domains_dir) if entry.is_dir())
    for subdir in subdirs:
        domain_path = os.path.join(domains_dir, subdir, "domain.json")
        if not os.path.isfile(domain_path):
            continue
        with open(domain_path, encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except json.JSONDecodeError as exc:
                raise RegistryLoadError(f"Invalid JSON in {domain_path}: {exc}") from exc
        schema_ver = data.get("schema_version")
        if schema_ver != "1.0":
            import warnings
            warnings.warn(
                f"domain_registry: skipping {domain_path} "
                f"(schema_version={schema_ver!r}, expected '1.0')",
                stacklevel=2,
            )
            continue
        _validate_domain_v1(data, domain_path)
        pack_id = data["pack_id"]
        # Deterministic pack_id collision (no silent last-wins).
        if pack_id in registry:
            raise RegistryLoadError(
                f"Duplicate pack_id '{pack_id}' in {domain_path} "
                f"(already loaded from another pack)"
            )
        # Provenance coverage against the canonical manifest (soft-gated).
        if provenance_ids is not None and pack_id not in provenance_ids:
            raise RegistryLoadError(
                f"pack_id '{pack_id}' has no provenance record in "
                f"{os.path.join(domains_dir, _PROVENANCE_FILENAME)}"
            )
        registry[pack_id] = data
    # Cross-pack alias uniqueness (structural only — no runtime alias resolution is
    # introduced). An alias may equal its OWN pack_id; it may not be claimed by two
    # packs, nor collide with a different pack's canonical pack_id.
    alias_owner = {}
    for pack_id, data in registry.items():
        for alias in (data.get("aliases") or []):
            if alias == pack_id:
                continue
            if alias in registry and alias != pack_id:
                raise RegistryLoadError(
                    f"Alias '{alias}' (pack '{pack_id}') collides with another "
                    f"pack's pack_id"
                )
            if alias in alias_owner and alias_owner[alias] != pack_id:
                raise RegistryLoadError(
                    f"Alias '{alias}' claimed by both packs "
                    f"'{alias_owner[alias]}' and '{pack_id}'"
                )
            alias_owner[alias] = pack_id
    return MappingProxyType(registry)


def get_domain(registry: MappingProxyType, capability_id: str) -> dict:
    if capability_id not in registry:
        raise DomainNotFoundError(
            f"capability_id '{capability_id}' not found in registry. "
            f"Available: {sorted(registry.keys())}")
    return registry[capability_id]


def list_domains(registry: MappingProxyType) -> list:
    return sorted(registry.keys())
