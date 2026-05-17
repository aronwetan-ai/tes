#!/usr/bin/env python3
"""
secret_scanner.py — Scan files for credential / secret leaks.

Greps for patterns that look like API keys, tokens, private keys, etc.
Designed to run in pre-commit hooks, CI, and manual audits.

Usage:
    tools/secret_scanner.py .
    tools/secret_scanner.py --staged              # git-staged files only
    tools/secret_scanner.py --json src/
    tools/secret_scanner.py --since HEAD~10..HEAD # scan recent commits

Risk: Low (read-only local FS / git inspection; no network).

Used by: `@nexusai.security`, pre-commit hook, CI on every PR.
Reference: knowledge/security/opsec-multi-account.md.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

# Heuristic patterns. Order: more-specific first to reduce duplicates.
PATTERNS: list[tuple[str, re.Pattern[str], str]] = [
    # AWS
    ("aws_access_key_id",
     re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"),
     "AWS access key ID"),
    ("aws_secret",
     re.compile(r"(?i)aws.{0,20}(secret|sk).{0,5}['\"]([0-9a-zA-Z/+]{40})['\"]"),
     "AWS secret access key (heuristic)"),

    # GCP
    ("gcp_api_key",
     re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"),
     "Google API key"),
    ("gcp_oauth_client",
     re.compile(r"\b[0-9]{6,}-[0-9a-z]{32}\.apps\.googleusercontent\.com\b"),
     "GCP OAuth client ID"),

    # GitHub
    ("github_pat",
     re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,251}\b"),
     "GitHub token (PAT/OAuth/Server/User/Refresh)"),
    ("github_classic",
     re.compile(r"(?i)github.{0,20}(token|pat).{0,5}['\"]([a-f0-9]{40})['\"]"),
     "Classic GitHub token (heuristic)"),

    # Slack
    ("slack_token",
     re.compile(r"\bxox[abprs]-[0-9A-Za-z\-]{10,}\b"),
     "Slack token"),
    ("slack_webhook",
     re.compile(r"\bhttps://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]{20,}\b"),
     "Slack incoming webhook"),

    # Stripe
    ("stripe_live_secret",
     re.compile(r"\bsk_live_[0-9a-zA-Z]{24,}\b"),
     "Stripe live secret key"),
    ("stripe_live_publishable",
     re.compile(r"\bpk_live_[0-9a-zA-Z]{24,}\b"),
     "Stripe live publishable key"),

    # Anthropic / OpenAI
    ("anthropic_key",
     re.compile(r"\bsk-ant-[a-zA-Z0-9-]{20,}\b"),
     "Anthropic API key"),
    ("openai_key",
     re.compile(r"\bsk-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}\b"),
     "OpenAI API key (legacy)"),
    ("openai_proj_key",
     re.compile(r"\bsk-proj-[A-Za-z0-9_\-]{40,}\b"),
     "OpenAI project key"),

    # Meta / Facebook
    ("fb_access_token",
     re.compile(r"\bEAA[A-Za-z0-9]{20,}\b"),
     "Facebook / Meta access token"),

    # JWT
    ("jwt",
     re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
     "JWT (could be example or real)"),

    # SSH / GPG private keys
    ("rsa_private_key",
     re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
     "Private key block"),

    # Generic high-confidence
    ("env_secret_assignment",
     re.compile(
         r"(?i)\b(secret|password|passwd|api[_-]?key|token|access[_-]?key|"
         r"client[_-]?secret)\s*[:=]\s*['\"]([^'\"\s]{16,})['\"]"
     ),
     "Suspicious secret assignment"),

    # Generic high-entropy strings (last resort, noisier)
    ("high_entropy_b64",
     re.compile(r"['\"]([A-Za-z0-9+/]{40,}={0,2})['\"]"),
     "High-entropy base64-like string (review)"),
]

# Files / dirs we don't bother scanning.
EXCLUDE_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".tox", ".pytest_cache", ".mypy_cache",
    "vendor", "target",
}
EXCLUDE_EXTS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico",
    ".pdf", ".zip", ".gz", ".tar", ".7z", ".bin",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".mp4", ".mp3", ".wav", ".webm",
    ".pyc", ".pyo", ".so", ".dll", ".class",
}

# Lines containing one of these markers we treat as documented/test/example.
ANNOTATION_ALLOW = (
    "secret-scanner: ignore",
    "secret_scanner: ignore",
    "pragma: allowlist secret",
)


class Finding(NamedTuple):
    path: str
    line: int
    pattern_name: str
    description: str
    snippet: str


def is_textfile(path: Path) -> bool:
    if path.suffix.lower() in EXCLUDE_EXTS:
        return False
    try:
        with path.open("rb") as fh:
            sample = fh.read(2048)
        if b"\x00" in sample:
            return False
    except OSError:
        return False
    return True


def scan_text(path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[str, int, str]] = set()  # dedupe (path,line,pattern)
    for lineno, line in enumerate(text.splitlines(), 1):
        # Honor ignore comments.
        if any(marker in line for marker in ANNOTATION_ALLOW):
            continue
        for name, pat, desc in PATTERNS:
            for m in pat.finditer(line):
                key = (path, lineno, name)
                if key in seen:
                    continue
                seen.add(key)
                snippet = m.group(0)
                if len(snippet) > 80:
                    snippet = snippet[:77] + "..."
                findings.append(Finding(path, lineno, name, desc, snippet))
    return findings


def expand_targets(targets: list[str]) -> list[Path]:
    out: list[Path] = []
    for t in targets:
        p = Path(t)
        if p.is_file():
            if is_textfile(p):
                out.append(p)
        elif p.is_dir():
            for f in p.rglob("*"):
                if not f.is_file():
                    continue
                if any(part in EXCLUDE_DIRS for part in f.parts):
                    continue
                if is_textfile(f):
                    out.append(f)
    return sorted(set(out))


def staged_files() -> list[Path]:
    try:
        r = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True, check=False, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"ERROR: cannot run git: {e}", file=sys.stderr)
        return []
    paths = [Path(p) for p in r.stdout.strip().splitlines() if p]
    return [p for p in paths if p.is_file() and is_textfile(p)]


def commits_range_files(rev: str) -> list[Path]:
    try:
        r = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACM", rev],
            capture_output=True, text=True, check=False, timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as e:
        print(f"ERROR: cannot run git: {e}", file=sys.stderr)
        return []
    paths = [Path(p) for p in r.stdout.strip().splitlines() if p]
    return [p for p in paths if p.is_file() and is_textfile(p)]


def main() -> int:
    p = argparse.ArgumentParser(
        description="Scan files for credential / secret leaks.")
    p.add_argument("targets", nargs="*", default=["."],
                   help="Files or directories (default: cwd).")
    p.add_argument("--staged", action="store_true",
                   help="Scan git-staged files only.")
    p.add_argument("--since", default=None,
                   help="Scan files changed in <rev range>, e.g. HEAD~10..HEAD.")
    p.add_argument("--json", action="store_true",
                   help="JSON output.")
    p.add_argument("--quiet", action="store_true",
                   help="Print only summary.")
    args = p.parse_args()

    if args.staged:
        files = staged_files()
    elif args.since:
        files = commits_range_files(args.since)
    else:
        files = expand_targets(args.targets)

    if not files:
        if not args.quiet:
            print("(no files to scan)")
        return 0

    all_findings: list[Finding] = []
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"WARN: cannot read {f}: {e}", file=sys.stderr)
            continue
        all_findings.extend(scan_text(str(f), text))

    if args.json:
        print(json.dumps(
            {
                "scanned_files":  len(files),
                "finding_count":  len(all_findings),
                "findings": [
                    {
                        "path":         fi.path,
                        "line":         fi.line,
                        "pattern":      fi.pattern_name,
                        "description":  fi.description,
                        "snippet":      fi.snippet,
                    } for fi in all_findings
                ],
            },
            ensure_ascii=False, indent=2,
        ))
    else:
        if not args.quiet:
            for fi in all_findings:
                print(f"{fi.path}:{fi.line}  [{fi.pattern_name}]  "
                      f"{fi.description}: {fi.snippet}")
        print(
            f"\nSummary: {len(all_findings)} finding(s) "
            f"in {len(files)} scanned file(s)."
        )

    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main())
