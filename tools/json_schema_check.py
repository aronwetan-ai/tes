#!/usr/bin/env python3
"""
json_schema_check.py — Validate JSON files against a JSON Schema.

Usage:
    tools/json_schema_check.py --schema schema.json --data data.json
    tools/json_schema_check.py --schema schema.json --data 'dir/*.json' --recursive
    tools/json_schema_check.py --schema schema.json --stdin

Risk: Low (read-only local FS, no network).

Used by: any agent validating structured output against a contract — task
logger entries, AI agent JSON output, config files, API response samples.

Notes:
- Uses jsonschema if installed; falls back to stdlib lightweight check
  (top-level type + required keys) if not.
- Exit 0 = all valid. Exit 1 = at least one validation error. Exit 2 = arg/IO
  error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Try to use jsonschema if available; otherwise fall back to a tiny validator.
try:
    import jsonschema  # type: ignore[import-untyped]
    HAVE_JSONSCHEMA = True
except ImportError:
    HAVE_JSONSCHEMA = False


def fallback_validate(data: Any, schema: dict) -> list[str]:
    """Minimal validator: top-level `type` + `required` + property `type`.

    Not a full JSON Schema implementation. Used only when jsonschema is not
    installed. Catches the most common contract violations.
    """
    errors: list[str] = []

    expected_type = schema.get("type")
    if expected_type:
        type_map = {
            "object":  dict,
            "array":   list,
            "string":  str,
            "number":  (int, float),
            "integer": int,
            "boolean": bool,
            "null":    type(None),
        }
        py_type = type_map.get(expected_type)
        if py_type and not isinstance(data, py_type):
            errors.append(f"top-level type: expected {expected_type}, got {type(data).__name__}")
            return errors

    if expected_type == "object" and isinstance(data, dict):
        for key in schema.get("required", []):
            if key not in data:
                errors.append(f"missing required key: {key!r}")
        props = schema.get("properties", {})
        for key, val in data.items():
            if key in props and "type" in props[key]:
                expected = props[key]["type"]
                py_type = {
                    "object":  dict, "array":   list, "string":  str,
                    "number":  (int, float), "integer": int,
                    "boolean": bool, "null":    type(None),
                }.get(expected)
                if py_type and not isinstance(val, py_type):
                    errors.append(f"key {key!r}: expected {expected}, got {type(val).__name__}")
    return errors


def validate_one(path: str | None, data: Any, schema: dict) -> list[str]:
    """Validate one JSON document. Returns list of error strings (empty = ok)."""
    if HAVE_JSONSCHEMA:
        try:
            jsonschema.validate(instance=data, schema=schema)
            return []
        except jsonschema.ValidationError as e:
            loc = "/".join(str(p) for p in e.absolute_path) or "<root>"
            return [f"{loc}: {e.message}"]
    else:
        return fallback_validate(data, schema)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def expand_data_paths(pattern: str, recursive: bool) -> list[Path]:
    """Resolve --data argument: literal path, glob, or directory."""
    p = Path(pattern)
    if p.is_file():
        return [p]
    if p.is_dir():
        return sorted(p.rglob("*.json") if recursive else p.glob("*.json"))
    # Glob pattern.
    parent = Path(pattern).parent if "/" in pattern else Path(".")
    glob = Path(pattern).name
    return sorted(parent.rglob(glob) if recursive else parent.glob(glob))


def main() -> int:
    p = argparse.ArgumentParser(
        description="Validate JSON files against a JSON Schema.")
    p.add_argument("--schema", required=True, help="Path to JSON Schema file.")
    p.add_argument("--data",  help="Path to JSON file, glob, or directory.")
    p.add_argument("--stdin", action="store_true", help="Read JSON from stdin.")
    p.add_argument("--recursive", action="store_true",
                   help="When --data is a directory or glob, recurse.")
    p.add_argument("--quiet", action="store_true",
                   help="Print only summary (count valid / invalid).")
    args = p.parse_args()

    if not args.data and not args.stdin:
        print("ERROR: provide --data or --stdin", file=sys.stderr)
        return 2

    try:
        schema = load_json(Path(args.schema))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot load schema: {e}", file=sys.stderr)
        return 2

    if not HAVE_JSONSCHEMA and not args.quiet:
        print("note: jsonschema lib not installed; using fallback (limited).",
              file=sys.stderr)

    inputs: list[tuple[str | None, Any]] = []
    if args.stdin:
        try:
            inputs.append(("<stdin>", json.loads(sys.stdin.read())))
        except json.JSONDecodeError as e:
            print(f"ERROR: stdin not valid JSON: {e}", file=sys.stderr)
            return 2
    if args.data:
        try:
            for path in expand_data_paths(args.data, args.recursive):
                try:
                    inputs.append((str(path), load_json(path)))
                except (OSError, json.JSONDecodeError) as e:
                    print(f"ERROR: cannot load {path}: {e}", file=sys.stderr)
                    return 2
        except OSError as e:
            print(f"ERROR: cannot expand --data: {e}", file=sys.stderr)
            return 2

    if not inputs:
        print("(no inputs found)")
        return 0

    n_valid = n_invalid = 0
    for path, data in inputs:
        errs = validate_one(path, data, schema)
        if errs:
            n_invalid += 1
            if not args.quiet:
                print(f"FAIL {path}")
                for e in errs:
                    print(f"  - {e}")
        else:
            n_valid += 1
            if not args.quiet:
                print(f"OK   {path}")

    print(f"\nSummary: {n_valid} valid / {n_invalid} invalid / {len(inputs)} total")
    return 0 if n_invalid == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
