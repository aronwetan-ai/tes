#!/usr/bin/env python3
"""
markdown_lint.py — Lint Markdown for common doc-quality issues.

Checks (read-only — does NOT modify files):
- Heading hierarchy (no jumps from H1 to H3 without H2).
- Internal links resolve to existing files.
- Trailing whitespace.
- Tabs used for indentation (use spaces).
- Code fences balanced (unclosed ``` blocks).
- Excessive consecutive blank lines.
- Long lines (>120 chars; configurable).
- Empty or stub headings.

Usage:
    tools/markdown_lint.py knowledge/ companies/
    tools/markdown_lint.py --max-line 100 README.md
    tools/markdown_lint.py --quiet --fail-on warning .

Risk: Low (read-only local FS, no network).

Used by: `@nexusai.writer`, `@nexusai.qa`, doc reviewers, CI.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

LEVELS = {"info": 0, "warning": 1, "error": 2}


class Issue:
    __slots__ = ("path", "line", "level", "msg")

    def __init__(self, path: str, line: int, level: str, msg: str):
        self.path = path
        self.line = line
        self.level = level
        self.msg = msg

    def __str__(self) -> str:
        loc = f"{self.path}:{self.line}" if self.line else self.path
        return f"{loc} [{self.level}] {self.msg}"


def _check_headings(lines: list[str], path: str, issues: list[Issue]) -> None:
    """Headings must not skip levels (H1 → H3 without H2)."""
    prev_level = 0
    for i, line in enumerate(lines, 1):
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if not m:
            continue
        level = len(m.group(1))
        text = m.group(2).strip()
        if not text:
            issues.append(Issue(path, i, "warning", "empty heading"))
        if prev_level and level > prev_level + 1:
            issues.append(Issue(
                path, i, "warning",
                f"heading jumps from H{prev_level} to H{level}",
            ))
        prev_level = level


def _check_internal_links(lines: list[str], path: str, root: Path,
                          issues: list[Issue]) -> None:
    """`](relative/path.md)` links must resolve. External links skipped."""
    pat = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    file_dir = Path(path).parent
    for i, line in enumerate(lines, 1):
        for m in pat.finditer(line):
            target = m.group(1).split("#", 1)[0].strip()
            if (
                not target
                or target.startswith(("http://", "https://", "mailto:", "tel:"))
                or target.startswith("#")
            ):
                continue
            # Only resolve relative paths ending in .md
            if not target.endswith(".md"):
                continue
            resolved = (file_dir / target).resolve()
            try:
                resolved.relative_to(root.resolve())
            except ValueError:
                # outside repo — skip
                continue
            if not resolved.exists():
                issues.append(Issue(
                    path, i, "warning",
                    f"broken internal link to {target!r}",
                ))


def _check_trailing_ws(lines: list[str], path: str, issues: list[Issue]) -> None:
    for i, line in enumerate(lines, 1):
        if line.rstrip("\n") != line.rstrip():
            issues.append(Issue(path, i, "info", "trailing whitespace"))


def _check_tabs(lines: list[str], path: str, issues: list[Issue]) -> None:
    for i, line in enumerate(lines, 1):
        if line.startswith("\t"):
            issues.append(Issue(path, i, "info", "tab indentation (use spaces)"))


def _check_code_fences(lines: list[str], path: str, issues: list[Issue]) -> None:
    open_fence_line = 0
    in_fence = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            if in_fence:
                in_fence = False
            else:
                in_fence = True
                open_fence_line = i
    if in_fence:
        issues.append(Issue(
            path, open_fence_line, "error",
            "unclosed code fence",
        ))


def _check_blank_lines(lines: list[str], path: str, issues: list[Issue]) -> None:
    """3+ consecutive blank lines."""
    blank = 0
    start = 0
    for i, line in enumerate(lines, 1):
        if line.strip() == "":
            if blank == 0:
                start = i
            blank += 1
        else:
            if blank >= 3:
                issues.append(Issue(
                    path, start, "info",
                    f"{blank} consecutive blank lines",
                ))
            blank = 0


def _check_line_length(lines: list[str], path: str, max_len: int,
                       issues: list[Issue]) -> None:
    in_fence = False
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue  # don't lint long lines inside code blocks
        # Don't count trailing newline.
        if len(line.rstrip("\n")) > max_len:
            issues.append(Issue(
                path, i, "info",
                f"line length {len(line.rstrip())} > {max_len}",
            ))


def lint_file(path: Path, root: Path, max_len: int) -> list[Issue]:
    issues: list[Issue] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return [Issue(str(path), 0, "error", f"cannot read: {e}")]

    lines = text.splitlines(keepends=False)
    spath = str(path)

    _check_headings(lines, spath, issues)
    _check_internal_links(lines, spath, root, issues)
    _check_trailing_ws(lines, spath, issues)
    _check_tabs(lines, spath, issues)
    _check_code_fences(lines, spath, issues)
    _check_blank_lines(lines, spath, issues)
    _check_line_length(lines, spath, max_len, issues)
    return issues


def expand_targets(targets: list[str]) -> list[Path]:
    out: list[Path] = []
    for t in targets:
        p = Path(t)
        if p.is_file():
            if p.suffix.lower() in (".md", ".markdown"):
                out.append(p)
        elif p.is_dir():
            for f in p.rglob("*.md"):
                out.append(f)
            for f in p.rglob("*.markdown"):
                out.append(f)
        else:
            print(f"WARN: target not found: {t}", file=sys.stderr)
    return sorted(set(out))


def main() -> int:
    p = argparse.ArgumentParser(
        description="Lint Markdown for common doc-quality issues.")
    p.add_argument("targets", nargs="+",
                   help="Files or directories to lint.")
    p.add_argument("--max-line", type=int, default=120,
                   help="Maximum line length warning (default 120).")
    p.add_argument("--root", default=".",
                   help="Repo root for resolving internal links (default cwd).")
    p.add_argument("--fail-on", choices=("info", "warning", "error"),
                   default="warning",
                   help="Minimum severity that causes nonzero exit "
                        "(default warning).")
    p.add_argument("--quiet", action="store_true",
                   help="Print only summary line.")
    args = p.parse_args()

    files = expand_targets(args.targets)
    if not files:
        print("(no markdown files found)")
        return 0

    root = Path(args.root)
    threshold = LEVELS[args.fail_on]

    all_issues: list[Issue] = []
    for f in files:
        all_issues.extend(lint_file(f, root, args.max_line))

    if not args.quiet:
        for issue in all_issues:
            print(issue)

    counts = {k: 0 for k in LEVELS}
    for issue in all_issues:
        counts[issue.level] += 1

    print(
        f"\nSummary: {counts['error']} error, "
        f"{counts['warning']} warning, "
        f"{counts['info']} info "
        f"across {len(files)} file(s)."
    )

    fail = any(LEVELS[i.level] >= threshold for i in all_issues)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
