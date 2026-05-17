#!/usr/bin/env python3
"""
archive_messages.py — Move messages older than N days from messages.jsonl
                      to companies/<co>/tasks/messages-archive/<YYYY-MM>.jsonl.

Behavior:
  - Scan all companies (default) or a single company (--company).
  - Cutoff: messages whose created_at is older than --older-than days
    (default: 30).
  - Archive bucket: companies/<co>/tasks/messages-archive/<YYYY-MM>.jsonl.
  - Idempotent: rerun without duplicating entries (matches on
    "company|from|to|created_at|message" tuple).
  - Dry-run supported.

Notes:
  - logs.jsonl is NEVER archived (audit trail).
  - inbox.jsonl is handled by archive_tasks.py.

Exit codes:
  0  success
  2  invalid arguments
  3  I/O error
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import task_logger as tl


def parse_iso(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


def discover_companies() -> List[str]:
    root = tl.workspace_root()
    cd = root / "companies"
    if not cd.is_dir():
        return []
    return sorted(c.name for c in cd.iterdir() if c.is_dir() and (c / "tasks").is_dir())


def archive_path(company: str, when: datetime) -> Path:
    return tl.company_tasks_dir(company) / "messages-archive" / f"{when.strftime('%Y-%m')}.jsonl"


def msg_key(m: dict) -> str:
    return f"{m.get('company','')}|{m.get('from','')}|{m.get('to','')}|{m.get('created_at','')}|{m.get('message','')[:80]}"


def load_existing_keys(path: Path) -> set[str]:
    out: set[str] = set()
    if not path.is_file():
        return out
    for entry in tl.iter_jsonl(path):
        out.add(msg_key(entry))
    return out


def archive_company(company: str,
                    cutoff: datetime,
                    *,
                    dry_run: bool) -> Tuple[int, int]:
    msg_file = tl.file_path(company, "messages")
    entries = tl.read_all(msg_file)
    if not entries:
        return (0, 0)

    keep: List[dict] = []
    by_path: Dict[Path, List[dict]] = defaultdict(list)
    for m in entries:
        ts = parse_iso(m.get("created_at", ""))
        if ts and ts < cutoff:
            by_path[archive_path(company, ts)].append(m)
        else:
            keep.append(m)

    archived = sum(len(v) for v in by_path.values())

    if dry_run or archived == 0:
        return (len(keep), archived)

    for path, batch in by_path.items():
        existing = load_existing_keys(path)
        for m in batch:
            if msg_key(m) in existing:
                continue
            tl.append_jsonl(path, m)

    tl.rewrite_jsonl(msg_file, keep)
    return (len(keep), archived)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Archive old agent-to-agent messages to monthly buckets.")
    p.add_argument("--company", default=None,
                   help="Limit to one company slug (default: all).")
    p.add_argument("--older-than", type=int, default=30, dest="older_than",
                   help="Age threshold in days (default: 30).")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would be archived without writing.")
    p.add_argument("--quiet", action="store_true",
                   help="Print only a one-line summary.")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    if args.older_than < 1:
        print("ERROR: --older-than must be >= 1", file=sys.stderr)
        return 2

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.older_than)
    companies = [args.company] if args.company else discover_companies()
    if not companies:
        print("(no companies found)")
        return 0

    total_archived = total_kept = 0
    report: Dict[str, Tuple[int, int]] = {}

    try:
        for co in companies:
            kept, archived = archive_company(co, cutoff, dry_run=args.dry_run)
            report[co] = (kept, archived)
            total_kept     += kept
            total_archived += archived
    except OSError as e:
        print(f"IO ERROR: {e}", file=sys.stderr)
        return 3

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    if args.quiet:
        print(f"{mode}: messages_archived={total_archived} kept={total_kept} cutoff={cutoff.strftime('%Y-%m-%d')}")
        return 0

    print(f"=== Message Archival ({mode}) ===")
    print(f"Cutoff: messages older than {cutoff.strftime('%Y-%m-%d %H:%M UTC')} ({args.older_than} days)")
    for co, (kept, archived) in report.items():
        print(f"[{co}]  archived={archived}  kept={kept}")
    print(f"\nTOTAL archived={total_archived}  TOTAL kept={total_kept}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
