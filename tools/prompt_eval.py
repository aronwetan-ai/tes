#!/usr/bin/env python3
"""
prompt_eval.py — Local YAML-driven eval runner for AI agent prompts.

Reads an eval cases YAML file + an outputs file (your agent's actual responses)
and grades each case against expected behavior. Produces summary by category +
per-case pass/fail.

This tool DOES NOT call any LLM. It just runs deterministic graders against
outputs you've already produced. The pattern lets you:
1. Run your agent locally / via API on your eval inputs.
2. Save outputs to a JSON file.
3. Run this tool to grade.

Risk: Low (read-only local FS, no network, no LLM calls).

Used by: `@nexusai.ml`, `@nexusai.qa`, CI on prompt-change PR.

See `companies/nexusai/skills/ml-agent/prompt-eval.md` for methodology.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# Try yaml; fall back to JSON-only if not available.
try:
    import yaml  # type: ignore[import-untyped]
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False


# ---------------------------------------------------------------------------
# Graders
# ---------------------------------------------------------------------------

def grade_regex(output: str, pattern: str) -> tuple[bool, str]:
    if re.search(pattern, output):
        return True, "match"
    return False, f"no match for {pattern!r}"


def grade_regex_must_not(output: str, pattern: str) -> tuple[bool, str]:
    m = re.search(pattern, output)
    if m:
        return False, f"forbidden match: {m.group(0)!r}"
    return True, "absent"


def grade_must_contain(output: str, needle: str) -> tuple[bool, str]:
    if needle in output:
        return True, "contains"
    return False, f"missing {needle!r}"


def grade_must_not_contain(output: str, needle: str) -> tuple[bool, str]:
    if needle in output:
        return False, f"forbidden substring {needle!r} present"
    return True, "absent"


def grade_must_not_contain_any(output: str, needles: list[str]) -> tuple[bool, str]:
    found = [n for n in needles if n in output]
    if found:
        return False, f"forbidden substrings present: {found}"
    return True, "all absent"


def grade_length_max(output: str, max_chars: int) -> tuple[bool, str]:
    if len(output) <= max_chars:
        return True, f"{len(output)} chars"
    return False, f"length {len(output)} > {max_chars}"


def grade_length_min(output: str, min_chars: int) -> tuple[bool, str]:
    if len(output) >= min_chars:
        return True, f"{len(output)} chars"
    return False, f"length {len(output)} < {min_chars}"


def grade_json_valid(output: str, _arg: Any = None) -> tuple[bool, str]:
    try:
        json.loads(output)
        return True, "valid JSON"
    except json.JSONDecodeError as e:
        return False, f"invalid JSON: {e}"


def grade_json_has_keys(output: str, keys: list[str]) -> tuple[bool, str]:
    try:
        obj = json.loads(output)
    except json.JSONDecodeError as e:
        return False, f"not JSON: {e}"
    if not isinstance(obj, dict):
        return False, "not a JSON object"
    missing = [k for k in keys if k not in obj]
    if missing:
        return False, f"missing keys: {missing}"
    return True, "all keys present"


def grade_exact(output: str, expected: str) -> tuple[bool, str]:
    if output.strip() == expected.strip():
        return True, "exact match"
    return False, "differs from expected"


GRADERS = {
    "regex":                 grade_regex,
    "regex_must_not":        grade_regex_must_not,
    "must_contain":          grade_must_contain,
    "must_not_contain":      grade_must_not_contain,
    "must_not_contain_any":  grade_must_not_contain_any,
    "length_max":            grade_length_max,
    "length_min":            grade_length_min,
    "json_valid":            grade_json_valid,
    "json_has_keys":         grade_json_has_keys,
    "exact":                 grade_exact,
}


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_cases(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        if not HAVE_YAML:
            raise RuntimeError("YAML cases file but pyyaml not installed.")
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)

    if isinstance(data, dict) and "cases" in data:
        cases = data["cases"]
    elif isinstance(data, list):
        cases = data
    else:
        raise ValueError("Cases file must be a list or {'cases': [...]}")

    if not all("id" in c for c in cases):
        raise ValueError("Every case must have an 'id'.")
    return cases


def load_outputs(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if isinstance(data, dict):
        return {k: str(v) for k, v in data.items()}
    if isinstance(data, list):
        return {str(item["id"]): str(item.get("output", "")) for item in data
                if "id" in item}
    raise ValueError("Outputs must be {id: output} or [{id, output}].")


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def run_case(case: dict[str, Any], output: str) -> dict[str, Any]:
    """Apply all graders for a case. Pass = all graders pass."""
    expected = case.get("expected", {})
    if isinstance(expected, list):
        # support [{grader_name: arg}, ...] shape
        results = []
        for entry in expected:
            for grader_name, arg in entry.items():
                results.append(_apply_grader(grader_name, arg, output))
    elif isinstance(expected, dict):
        results = [_apply_grader(name, arg, output) for name, arg in expected.items()]
    else:
        return {
            "id":       case["id"],
            "category": case.get("category", "uncategorized"),
            "passed":   False,
            "graders":  [],
            "error":    f"unsupported 'expected' shape: {type(expected).__name__}",
        }

    passed = all(r["passed"] for r in results) if results else True
    return {
        "id":       case["id"],
        "category": case.get("category", "uncategorized"),
        "passed":   passed,
        "graders":  results,
    }


def _apply_grader(name: str, arg: Any, output: str) -> dict[str, Any]:
    fn = GRADERS.get(name)
    if not fn:
        return {
            "name":   name,
            "passed": False,
            "msg":    f"unknown grader: {name}",
        }
    try:
        passed, msg = fn(output, arg)
        return {"name": name, "passed": passed, "msg": msg}
    except (TypeError, ValueError, re.error) as e:
        return {
            "name":   name,
            "passed": False,
            "msg":    f"grader raised: {type(e).__name__}: {e}",
        }


def summarize(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    by_cat: dict[str, dict[str, int]] = {}
    for r in case_results:
        cat = r["category"]
        slot = by_cat.setdefault(cat, {"total": 0, "passed": 0})
        slot["total"] += 1
        if r["passed"]:
            slot["passed"] += 1

    total = len(case_results)
    passed = sum(1 for r in case_results if r["passed"])

    return {
        "case_count":    total,
        "pass_count":    passed,
        "fail_count":    total - passed,
        "pass_rate":     round(passed / total, 4) if total else 1.0,
        "by_category":   {
            cat: {**slot, "pass_rate": round(slot["passed"] / slot["total"], 4)}
            for cat, slot in by_cat.items()
        },
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Local YAML-driven eval runner for AI agent prompts.")
    p.add_argument("--cases", required=True,
                   help="Eval cases file (YAML or JSON).")
    p.add_argument("--outputs", required=True,
                   help="Outputs file (JSON: {case_id: output}).")
    p.add_argument("--baseline", default=None,
                   help="Optional baseline summary JSON to compare against.")
    p.add_argument("--regression-threshold", type=float, default=0.02,
                   help="Pass-rate drop threshold to flag regression "
                        "(default 0.02 = 2pp).")
    p.add_argument("--json", action="store_true",
                   help="Emit JSON instead of human report.")
    args = p.parse_args()

    try:
        cases = load_cases(Path(args.cases))
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as e:
        print(f"ERROR: cases: {e}", file=sys.stderr)
        return 2

    try:
        outputs = load_outputs(Path(args.outputs))
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"ERROR: outputs: {e}", file=sys.stderr)
        return 2

    case_results: list[dict[str, Any]] = []
    for case in cases:
        out = outputs.get(case["id"])
        if out is None:
            case_results.append({
                "id":       case["id"],
                "category": case.get("category", "uncategorized"),
                "passed":   False,
                "graders":  [],
                "error":    "no output provided for this case id",
            })
            continue
        case_results.append(run_case(case, out))

    summary = summarize(case_results)

    # Compare against baseline.
    regression = None
    if args.baseline:
        try:
            base = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
            base_pass = base.get("pass_rate", 0.0)
            delta = summary["pass_rate"] - base_pass
            regression = {
                "baseline_pass_rate": base_pass,
                "current_pass_rate":  summary["pass_rate"],
                "delta":              round(delta, 4),
                "is_regression":      delta < -args.regression_threshold,
            }
        except (OSError, json.JSONDecodeError) as e:
            print(f"WARN: baseline load failed: {e}", file=sys.stderr)

    if args.json:
        print(json.dumps({
            "summary":     summary,
            "regression":  regression,
            "cases":       case_results,
        }, ensure_ascii=False, indent=2))
    else:
        print(f"=== Eval Run ===")
        print(
            f"cases: {summary['case_count']}  "
            f"pass: {summary['pass_count']}  "
            f"fail: {summary['fail_count']}  "
            f"rate: {summary['pass_rate']:.2%}"
        )
        print("\nBy category:")
        for cat, slot in summary["by_category"].items():
            print(
                f"  {cat:<24} {slot['passed']}/{slot['total']}  "
                f"({slot['pass_rate']:.2%})"
            )
        if regression:
            sign = "↓" if regression["delta"] < 0 else "↑"
            tag  = " REGRESSION" if regression["is_regression"] else ""
            print(
                f"\nBaseline: {regression['baseline_pass_rate']:.2%} → "
                f"{regression['current_pass_rate']:.2%} "
                f"({sign}{abs(regression['delta']):.2%}){tag}"
            )
        fails = [c for c in case_results if not c["passed"]]
        if fails:
            print("\nFailures:")
            for c in fails:
                err = c.get("error")
                if err:
                    print(f"  - {c['id']} [{c['category']}]: {err}")
                else:
                    msgs = [g["msg"] for g in c["graders"] if not g["passed"]]
                    print(f"  - {c['id']} [{c['category']}]: {'; '.join(msgs)}")

    if regression and regression["is_regression"]:
        return 1
    if summary["fail_count"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
