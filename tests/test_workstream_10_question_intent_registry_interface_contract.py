"""
test_workstream_10_question_intent_registry_interface_contract.py
Workstream 10 — Interface-Contract BASE RED (D31).

Governance basis (merged, authoritative):
    docs/governance/WORKSTREAM_10_QUESTION_INTENT_REGISTRY_INCREMENT_CONTRACT.md
    docs/governance/WORKSTREAM_10_V1_RECORD_SHAPE_OWNER_DECISIONS.md            (D1–D17)
    docs/governance/WORKSTREAM_10_LOADER_INTERFACE_AND_BASE_RED_SEQUENCE_OWNER_DECISIONS.md (D18–D33)

Purpose (D31):
    Encode the approved D18–D32 PUBLIC INTERFACE CONTRACT for the future loader
    module `engine/question_intent_registry.py` BEFORE Minimal Interface GREEN.

    This is the Interface-Contract RED gate ONLY. It does NOT encode the D33
    Behavioral Validation RED (valid load, ID-set equality, duplicates, metadata,
    source references, ordering, no-fallback execution) — those are a later gate.

Controlled-RED discipline (D31 / acceptable-RED):
    The approved production module does not exist yet, so every essential test
    must fail as a DELIBERATE, clearly-messaged WS10 contract assertion — never as
    an uncontrolled collection/import error. Therefore:
      * this test module imports ONLY the standard library at top level;
      * it never imports `engine.question_intent_registry` at module scope;
      * each test resolves the production module through `_require_module()`, which
        converts a missing module/symbol into `pytest.fail(...)` with an explicit
        WS10 contract message;
      * all six test items collect and the module imports cleanly.

Constraints honored (D26/§6): no dependencies; no temporary/fake production
module; no `sys.modules` monkeypatching; no fake implementation; no registry
JSON; no dataclass-field or exception-constructor invention beyond D18–D32; no
human-readable error-message assertions; no D33 behavioral checks.
"""

import dataclasses
import importlib
import inspect
import subprocess
import sys
from pathlib import Path

import pytest

# Approved contract (D18–D22).
_MODULE_NAME = "engine.question_intent_registry"
_PUBLIC_SYMBOLS = (
    "load_question_intent_registry",
    "QuestionIntentRegistry",
    "QuestionIntentRecord",
    "QuestionIntentRegistryMetadata",
    "QuestionIntentRegistryLoadError",
    "QuestionIntentNotFoundError",
)
_REPO_ROOT = Path(__file__).resolve().parent.parent


def _require_module():
    """Import the approved production module or fail as a controlled WS10 RED.

    A missing module is an ACCEPTABLE Interface-Contract RED (D31), but only when
    surfaced as a deliberate assertion failure with a clear message — not as a
    raw traceback or a collection error."""
    try:
        return importlib.import_module(_MODULE_NAME)
    except ModuleNotFoundError as exc:
        pytest.fail(
            f"WS10 Interface-Contract RED (D18): approved production module "
            f"'{_MODULE_NAME}' does not yet exist "
            f"(Minimal Interface GREEN not authorized/started): {exc}"
        )


def _require_symbol(module, name):
    if not hasattr(module, name):
        pytest.fail(
            f"WS10 Interface-Contract RED: approved public symbol "
            f"'{_MODULE_NAME}.{name}' is not exposed (D18–D22)."
        )
    return getattr(module, name)


# ── 1. Module + public-symbol contract (D18/D22) ──
def test_question_intent_registry_module_contract_exists():
    module = _require_module()
    missing = [s for s in _PUBLIC_SYMBOLS if not hasattr(module, s)]
    assert not missing, (
        f"WS10 Interface-Contract RED: '{_MODULE_NAME}' missing approved public "
        f"symbols {missing} (D18–D22)."
    )


# ── 2. Load-function explicit two-path signature (D19/D24) ──
def test_load_function_has_explicit_two_path_signature():
    module = _require_module()
    fn = _require_symbol(module, "load_question_intent_registry")
    sig = inspect.signature(fn)
    params = list(sig.parameters.values())
    names = [p.name for p in params]
    assert names == ["registry_path", "source_artifact_path"], (
        f"WS10 D19: load signature must be exactly "
        f"(registry_path, source_artifact_path); got {names}."
    )
    for p in params:
        assert p.default is inspect.Parameter.empty, (
            f"WS10 D24: parameter '{p.name}' must be required (no default)."
        )
        assert p.kind not in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD,
        ), f"WS10 D19/D24: parameter '{p.name}' must not be *args/**kwargs."


# ── 3. Public types are frozen (immutable) dataclasses (D21) ──
def test_registry_public_types_are_frozen_dataclasses():
    module = _require_module()
    for name in (
        "QuestionIntentRecord",
        "QuestionIntentRegistryMetadata",
        "QuestionIntentRegistry",
    ):
        cls = _require_symbol(module, name)
        assert dataclasses.is_dataclass(cls), (
            f"WS10 D21: '{name}' must be a dataclass."
        )
        params = getattr(cls, "__dataclass_params__", None)
        assert params is not None and params.frozen is True, (
            f"WS10 D21: '{name}' must be an immutable (frozen) dataclass."
        )


# ── 4. Registry public API is read-only: get + list_records, no mutation (D20) ──
def test_registry_public_api_is_read_only():
    module = _require_module()
    registry_cls = _require_symbol(module, "QuestionIntentRegistry")
    # Inspect the class contract statically — do NOT instantiate (constructor
    # fields are not approved in this gate).
    for method in ("get", "list_records"):
        attr = inspect.getattr_static(registry_cls, method, None)
        assert callable(attr), (
            f"WS10 D20: QuestionIntentRegistry must expose a callable '{method}'."
        )
    _FORBIDDEN_MUTATORS = (
        "add", "set", "put", "insert", "append", "extend", "update",
        "delete", "remove", "pop", "clear", "replace", "mutate", "write",
        "add_record", "set_record", "put_record", "remove_record",
    )
    public = {n for n in dir(registry_cls) if not n.startswith("_")}
    leaked = sorted(public.intersection(_FORBIDDEN_MUTATORS))
    assert not leaked, (
        f"WS10 D20: QuestionIntentRegistry must expose no public mutation API; "
        f"found {leaked}."
    )


# ── 5. Approved exception contract with stable reason_code (D22/D26) ──
def test_approved_exception_contract_exists():
    module = _require_module()
    load_err = _require_symbol(module, "QuestionIntentRegistryLoadError")
    not_found = _require_symbol(module, "QuestionIntentNotFoundError")
    for name, cls in (
        ("QuestionIntentRegistryLoadError", load_err),
        ("QuestionIntentNotFoundError", not_found),
    ):
        assert isinstance(cls, type) and issubclass(cls, Exception), (
            f"WS10 D22: '{name}' must be an exception class."
        )
    # D26: the load error exposes a stable `reason_code`. Inspect the class
    # contract (attribute / annotation / property / __init__ parameter) WITHOUT
    # inventing a constructor.
    has_reason_code = (
        hasattr(load_err, "reason_code")
        or "reason_code" in getattr(load_err, "__annotations__", {})
        or "reason_code" in inspect.signature(load_err.__init__).parameters
    )
    assert has_reason_code, (
        "WS10 D26: QuestionIntentRegistryLoadError must expose a stable "
        "'reason_code' (as attribute, annotation, property, or __init__ param)."
    )


# ── 6. Import has no registry I/O side effect (D19/D25) ──
def test_import_has_no_registry_io_side_effect():
    """Import the approved module in an ISOLATED subprocess (defeats import
    caching, D25) and prove the import performs no registry/artifact I/O and no
    registry loading. A missing module is surfaced as a controlled WS10 RED."""
    probe = (
        "import sys\n"
        "_opened = []\n"
        "def _hook(event, args):\n"
        "    if event == 'open' and args and args[0] is not None:\n"
        "        _opened.append(str(args[0]))\n"
        "sys.addaudithook(_hook)\n"
        "import importlib\n"
        "try:\n"
        "    importlib.import_module('engine.question_intent_registry')\n"
        "except ModuleNotFoundError:\n"
        "    print('WS10_MODULE_ABSENT'); sys.exit(42)\n"
        "_bad = [p for p in _opened if ('question_intent_registry' in p and p.endswith('.json'))"
        " or 'electronics_electrical_path_n_questions' in p]\n"
        "if _bad:\n"
        "    print('WS10_IMPORT_IO:' + ';'.join(_bad)); sys.exit(43)\n"
        "print('WS10_IMPORT_CLEAN'); sys.exit(0)\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=str(_REPO_ROOT),
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    if proc.returncode == 42:
        pytest.fail(
            "WS10 Interface-Contract RED (D18): approved production module "
            "'engine.question_intent_registry' does not yet exist, so its "
            "import-time no-I/O contract (D19/D25) cannot yet be satisfied."
        )
    assert proc.returncode == 0, (
        "WS10 D19/D25: importing engine.question_intent_registry must perform no "
        f"registry/artifact I/O and no registry loading. Probe output: {out!r}"
    )
