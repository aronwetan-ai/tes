#!/usr/bin/env python3
"""
dep_audit.py — Surface outdated / vulnerable dependencies in this repo.

Wraps language-native auditors (read-only, --dry-run-equivalent):
- Python: pip list --outdated + pip-audit (if installed)
- Node:   npm outdated + npm audit (if package.json present)
- (placeholders for go, rust if those land later)

Usage:
    tools/dep_audit.py
    tools/dep_audit.py --json
    tools/dep_audit.py --only python
    tools/dep_audit.py --workdir path/to/project

Behavior:
- Read-only. Does NOT install, upgrade, or modify anything.
- Combines per-language results into one report.
- Exit 0 = no issues. Exit 1 = outdated or vulnerable found. Exit 2 = arg/IO.

Risk: Low (read-only; no install; auditors only inspect lockfiles).

Used by: `@nexusai.devops`, `@nexusai.security`, weekly cron, pre-release.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def _run(cmd: list[str], cwd: Path | None = None) -> dict[str, Any]:
    """Run a command, capture output, never raise. Returns dict."""
    if not shutil.which(cmd[0]):
        return {
            "cmd": " ".join(cmd),
            "ran": False,
            "reason": f"command not found: {cmd[0]}",
        }
    try:
        r = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        return {
            "cmd": " ".join(cmd),
            "ran": True,
            "exit_code": r.returncode,
            "stdout": r.stdout,
            "stderr": r.stderr,
        }
    except subprocess.TimeoutExpired:
        return {
            "cmd": " ".join(cmd),
            "ran": False,
            "reason": "timeout (120s)",
        }
    except OSError as e:
        return {
            "cmd": " ".join(cmd),
            "ran": False,
            "reason": str(e),
        }


def audit_python(workdir: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"language": "python"}

    # pip list --outdated --format json
    r = _run([sys.executable, "-m", "pip", "list", "--outdated", "--format", "json"], cwd=workdir)
    out["outdated"] = r
    if r.get("ran") and r.get("exit_code") == 0:
        try:
            packages = json.loads(r["stdout"] or "[]")
            out["outdated_count"] = len(packages)
            out["outdated_packages"] = packages
        except json.JSONDecodeError:
            out["outdated_count"] = -1

    # pip-audit (vulnerability scanner, optional)
    if shutil.which("pip-audit"):
        r2 = _run(["pip-audit", "--format", "json"], cwd=workdir)
        out["vulnerabilities"] = r2
        if r2.get("ran"):
            try:
                payload = json.loads(r2["stdout"] or "{}")
                deps = payload.get("dependencies", [])
                vulns = sum(1 for d in deps if d.get("vulns"))
                out["vulnerability_count"] = vulns
            except json.JSONDecodeError:
                out["vulnerability_count"] = -1
    else:
        out["vulnerabilities"] = {"ran": False, "reason": "pip-audit not installed"}

    return out


def audit_node(workdir: Path) -> dict[str, Any]:
    pkg = workdir / "package.json"
    out: dict[str, Any] = {"language": "node"}
    if not pkg.exists():
        out["skipped"] = "no package.json"
        return out

    r = _run(["npm", "outdated", "--json"], cwd=workdir)
    out["outdated"] = r
    if r.get("ran"):
        try:
            payload = json.loads(r["stdout"] or "{}")
            out["outdated_count"] = len(payload)
            out["outdated_packages"] = payload
        except json.JSONDecodeError:
            out["outdated_count"] = -1

    r2 = _run(["npm", "audit", "--json"], cwd=workdir)
    out["vulnerabilities"] = r2
    if r2.get("ran"):
        try:
            payload = json.loads(r2["stdout"] or "{}")
            meta = payload.get("metadata", {}).get("vulnerabilities", {})
            out["vulnerability_count_by_severity"] = meta
            out["vulnerability_count"] = sum(meta.values())
        except json.JSONDecodeError:
            out["vulnerability_count"] = -1

    return out


def render_report(reports: list[dict[str, Any]]) -> tuple[str, bool]:
    """Build human-readable report; return (text, has_issue)."""
    lines: list[str] = []
    has_issue = False

    for rep in reports:
        lang = rep["language"]
        lines.append(f"=== {lang.upper()} ===")
        if rep.get("skipped"):
            lines.append(f"  skipped: {rep['skipped']}")
            lines.append("")
            continue

        out_info = rep.get("outdated", {})
        if not out_info.get("ran"):
            lines.append(f"  outdated check: not run ({out_info.get('reason')})")
        else:
            n = rep.get("outdated_count", -1)
            if n == -1:
                lines.append("  outdated check: parse error")
            elif n == 0:
                lines.append("  outdated:  0  ✓")
            else:
                has_issue = True
                lines.append(f"  outdated:  {n}")
                pkgs = rep.get("outdated_packages")
                if isinstance(pkgs, list):
                    for p in pkgs[:10]:
                        lines.append(
                            f"    - {p.get('name', '?')} "
                            f"{p.get('version', '?')} → {p.get('latest_version', '?')}"
                        )
                    if len(pkgs) > 10:
                        lines.append(f"    (and {len(pkgs) - 10} more)")
                elif isinstance(pkgs, dict):
                    for name, info in list(pkgs.items())[:10]:
                        cur = info.get("current", "?") if isinstance(info, dict) else "?"
                        lat = info.get("latest", "?") if isinstance(info, dict) else "?"
                        lines.append(f"    - {name} {cur} → {lat}")
                    if len(pkgs) > 10:
                        lines.append(f"    (and {len(pkgs) - 10} more)")

        vuln_info = rep.get("vulnerabilities", {})
        if not vuln_info.get("ran"):
            lines.append(f"  vulnerability check: not run ({vuln_info.get('reason')})")
        else:
            n = rep.get("vulnerability_count", -1)
            sev = rep.get("vulnerability_count_by_severity")
            if n == -1:
                lines.append("  vulnerabilities: parse error")
            elif n == 0:
                lines.append("  vulnerabilities: 0  ✓")
            else:
                has_issue = True
                detail = f" ({sev})" if sev else ""
                lines.append(f"  vulnerabilities: {n}{detail}")
        lines.append("")

    return "\n".join(lines), has_issue


def main() -> int:
    p = argparse.ArgumentParser(
        description="Surface outdated / vulnerable dependencies in this repo.")
    p.add_argument("--workdir", default=".",
                   help="Project directory (default: cwd).")
    p.add_argument("--only", choices=("python", "node"),
                   help="Limit to one language.")
    p.add_argument("--json", action="store_true",
                   help="Output structured JSON instead of human report.")
    args = p.parse_args()

    workdir = Path(args.workdir).resolve()
    if not workdir.is_dir():
        print(f"ERROR: workdir not found: {workdir}", file=sys.stderr)
        return 2

    reports: list[dict[str, Any]] = []
    if args.only in (None, "python"):
        reports.append(audit_python(workdir))
    if args.only in (None, "node"):
        reports.append(audit_node(workdir))

    if args.json:
        print(json.dumps({"workdir": str(workdir), "reports": reports},
                         ensure_ascii=False, indent=2))
        # Exit code based on issue presence
        any_issue = any(
            r.get("outdated_count", 0) > 0 or r.get("vulnerability_count", 0) > 0
            for r in reports
        )
        return 1 if any_issue else 0

    text, any_issue = render_report(reports)
    print(text)
    return 1 if any_issue else 0


if __name__ == "__main__":
    sys.exit(main())
