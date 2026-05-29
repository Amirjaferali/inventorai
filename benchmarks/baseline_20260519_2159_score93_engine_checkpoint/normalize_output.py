"""
engine/normalize_output.py
Schema normalization — idempotent, no side effects, no HTTP, no env vars.
Verbatim copy from benchmark/run_benchmark_v1.py lines 65-82.
No behavior changes during extraction.
"""

from engine.enums import ENUM_MAP


def normalize_output(obj):
    if not isinstance(obj, dict):
        return obj
    def nv(key, val):
        if isinstance(val, str):
            val = val.strip()
            if key in ENUM_MAP:
                upper = val.upper().replace(" ","_").replace("-","_")
                for v in ENUM_MAP[key]:
                    if upper == v:
                        return v
        if isinstance(val, dict):
            return {k: nv(k, w) for k, w in val.items()}
        if isinstance(val, list):
            return [nv(key, item) for item in val]
        return val
    return {k: nv(k, v) for k, v in obj.items()}
