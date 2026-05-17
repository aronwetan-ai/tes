#!/usr/bin/env python3
"""
archive_tasks.py — Move terminal tasks older than N days from inbox.jsonl
                   to companies/<co>/tasks/archive/<YYYY-MM>.jsonl.

Behavior:
  - Scan all companies (companies/*/tasks/inbox.jsonl) by default,
    or one company via --company.
  - Terminal statuses considered for archival: DONE, CANCELLED.
    FAILED is NOT auto-archived (it might be retried).
  - Cutoff: tasks whose updated_at is older than --older-than days
    (default: 30).
  - Archive bucket: companies/<co>/tasks/archive/<YYYY-MM>.jsonl
    where YYYY-MM is taken from the task's updated_at.
  - Audit: every ARCHIVE event is appended to logs.jsonl
    (logs.jsonl is itself NEVER archived — it's the audit trail).
  - Dry-run supported via --dry-run.
  - Idempotent: if a task is already in the archive file, it won't
    be re-added; it will only be removed from inbox.

Exit codes:
  0  success (rows may be 0)
  2  invalid arguments
  3  I/O error
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import task_logger as tl

ARCHIVABLE_STATUSES = {"DONE", "CANCELLED"}


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
    """Return list of company slugs that have a tasks/ folder."""
    root = tl.workspace_root()
    companies_dir = root / "companies"
    if not companies_dir.is_dir():
        return []
    out = []
    for child in sorted(companies_dir.iterdir()):
        if child.is_dir() and (child / "tasks").is_dir():
            out.append(child.name)
    return out


def archive_path(company: str, when: datetime) -> Path:
    bucket = when.strftime("%Y-%m")
    return tl.company_tasks_dir(company) / "archive" / f"{bucket}.jsonl"


def load_existing_ids(path: Path) -> set[str]:
    """Load IDs from an existing archive file (for idempotency)."""
    out: set[str] = set()
    if not path.is_file():
        return out
    for entry in tl.iter_jsonl(path):
        tid = entry.get("id")
        if isinstance(tid, str):
            out.add(tid)
    return out


def archive_company(company: str,
                    cutoff: datetime,
                    *,
                    dry_run: bool) -> Tuple[int, int, Dict[str, int]]:
    """Archive eligible tasks for one company.

    Returns (kept_count, archived_count, by_bucket).
    """
    inbox = tl.file_path(company, "inbox")
    entries = tl.read_all(inbox)
    if not entries:
        return (0, 0, {})

    keep: List[dict] = []
    to_archive_by_path: Dict[Path, List[dict]] = defaultdict(list)

    for e in entries:
        status     = e.get("status", "")
        updated_ts = parse_iso(e.get("updated_at", ""))
        if status in ARCHIVABLE_STATUSES and updated_ts and updated_ts < cutoff:
            target = archive_path(company, updated_ts)
            to_archive_by_path[target].append(e)
        else:
            keep.append(e)

    archived_count = sum(len(v) for v in to_archive_by_path.values())
    by_bucket = {p.name: len(v) for p, v in to_archive_by_path.items()}

    if dry_run or archived_count == 0:
        return (len(keep), archived_count, by_bucket)

    # Write each bucket (idempotent: skip IDs already present).
    for path, batch in to_archive_by_path.items():
        existing_ids = load_existing_ids(path)
        for entry in batch:
            if entry.get("id") in existing_ids:
                continue
            tl.append_jsonl(path, entry)
            tl.audit("ARCHIVE", entry,
                     prev_status=entry.get("status"),
                     new_status=entry.get("status"),
                     actor="archive_tasks.py",
                     note=f"moved to {path.relative_to(tl.workspace_root())}")

    # Rewrite inbox without the archived rows.
    tl.rewrite_jsonl(inbox, keep)
    return (len(keep), archived_count, by_bucket)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Archive terminal tasks older than N days to monthly buckets.")
    p.add_argument("--company", default=None,
                   help="Limit to a single company slug (default: all companies).")
    p.add_argument("--older-than", type=int, default=30, dest="older_than",
                   help="Age threshold in days (default: 30).")
    p.add_argument("--dry-run", action="store_true",
                   help="Show what would be archived, don't write anything.")
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

    total_kept = total_archived = 0
    report: Dict[str, dict] = {}

    try:
        for co in companies:
            kept, archived, by_bucket = archive_company(co, cutoff, dry_run=args.dry_run)
            report[co] = {"kept": kept, "archived": archived, "by_bucket": by_bucket}
            total_kept     += kept
            total_archived += archived
    except OSError as e:
        print(f"IO ERROR: {e}", file=sys.stderr)
        return 3

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    if args.quiet:
        print(f"{mode}: archived={total_archived} kept_active={total_kept} cutoff={cutoff.strftime('%Y-%m-%d')}")
        return 0

    print(f"=== Task Archival ({mode}) ===")
    print(f"Cutoff: tasks updated before {cutoff.strftime('%Y-%m-%d %H:%M UTC')} ({args.older_than} days ago)")
    print(f"Statuses eligible: {sorted(ARCHIVABLE_STATUSES)}")
    print()
    for co, r in report.items():
        print(f"[{co}]  archived={r['archived']}  kept_in_inbox={r['kept']}")
        for bucket, n in sorted(r["by_bucket"].items()):
            print(f"    -> archive/{bucket}: {n} task(s)")
    print()
    print(f"TOTAL archived={total_archived}  TOTAL kept={total_kept}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
