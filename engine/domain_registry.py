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
    if not isinstance(data["classification_signals"], list):
        raise RegistryLoadError(
            f"Field 'classification_signals' must be a list in {path}"
        )
    if not isinstance(data["substance_signals"], list):
        raise RegistryLoadError(
            f"Field 'substance_signals' must be a list in {path}"
        )



def load_registry(domains_dir: str) -> MappingProxyType:
    if not os.path.isdir(domains_dir):
        raise FileNotFoundError(f"domains_dir does not exist or is not a directory: {domains_dir}")
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
        registry[data["pack_id"]] = data
    return MappingProxyType(registry)


def get_domain(registry: MappingProxyType, capability_id: str) -> dict:
    if capability_id not in registry:
        raise DomainNotFoundError(
            f"capability_id '{capability_id}' not found in registry. "
            f"Available: {sorted(registry.keys())}")
    return registry[capability_id]


def list_domains(registry: MappingProxyType) -> list:
    return sorted(registry.keys())
