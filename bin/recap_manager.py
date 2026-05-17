#!/usr/bin/env python3
"""
recap_manager.py — Generate a periodic recap entry from inbox.jsonl + logs.jsonl
                   into companies/<co>/tasks/recap.jsonl.

A recap entry summarizes work done in a window:
  - Tasks created
  - Tasks completed (DONE)
  - Tasks cancelled
  - Tasks failed
  - Tasks still in progress (NEW + IN_PROGRESS + RETRY)
  - Top agents by completed-task count
  - Priority distribution of DONE tasks

Usage:
    bin/recap_manager.py --company nexusai --window weekly
    bin/recap_manager.py --company brandflow --window monthly
    bin/recap_manager.py --window weekly        # all companies
    bin/recap_manager.py --company nexusai --since 2026-05-01 --until 2026-05-17

Windows:
    daily    last 24h
    weekly   last 7d (default)
    monthly  last 30d
    custom   --since + --until (ISO date YYYY-MM-DD)

Behavior:
  - Reads logs.jsonl (CREATE / UPDATE events) for the window.
  - Reads inbox.jsonl for current state (still-active count).
  - Appends one recap entry per company per run to recap.jsonl.
  - Does NOT mutate inbox.jsonl or logs.jsonl.

Exit codes:
  0  success
  2  invalid arguments
  3  I/O error
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import task_logger as tl

WINDOWS = {
    "daily":   1,
    "weekly":  7,
    "monthly": 30,
}


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


def build_recap(company: str,
                since: datetime,
                until: datetime) -> Dict:
    """Build one recap entry for `company` over [since, until)."""
    logs_path = tl.file_path(company, "logs")
    inbox_path = tl.file_path(company, "inbox")

    log_entries = tl.read_all(logs_path)
    in_window = []
    for ev in log_entries:
        ts = parse_iso(ev.get("at", ""))
        if ts and since <= ts < until:
            in_window.append(ev)

    created   = [e for e in in_window if e.get("event") == "CREATE"]
    updates   = [e for e in in_window if e.get("event") == "UPDATE"]

    completed = [e for e in updates if e.get("new_status") == "DONE"]
    cancelled = [e for e in updates if e.get("new_status") == "CANCELLED"]
    failed    = [e for e in updates if e.get("new_status") == "FAILED"]

    # Top agents by task closures (DONE).
    agent_counter: Counter = Counter()
    for e in completed:
        actor = e.get("actor") or e.get("to") or "?"
        agent_counter[actor] += 1
    top_agents = [{"agent": a, "done": n} for a, n in agent_counter.most_common(5)]

    # Priority distribution of DONE tasks (lookup via inbox + archive in current snapshot).
    # Cheap path: read priority from logs by joining task_id with inbox; if not in inbox,
    # priority is unknown.
    inbox_by_id: Dict[str, dict] = {x.get("id"): x for x in tl.read_all(inbox_path)}
    priority_counter: Counter = Counter()
    for e in completed:
        tid = e.get("task_id")
        prio = (inbox_by_id.get(tid) or {}).get("priority", "UNKNOWN")
        priority_counter[prio] += 1

    # Active count (snapshot, not windowed).
    active = [x for x in inbox_by_id.values()
              if x.get("status") not in ("DONE", "CANCELLED")]

    return {
        "company":       company,
        "window_from":   since.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "window_to":     until.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generated_at":  datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totals": {
            "created":         len(created),
            "completed":       len(completed),
            "cancelled":       len(cancelled),
            "failed":          len(failed),
            "active_snapshot": len(active),
        },
        "top_agents":            top_agents,
        "priority_distribution": dict(priority_counter),
    }


def render_human(recap: Dict) -> str:
    t = recap["totals"]
    lines = [
        f"=== Recap: {recap['company']} ===",
        f"Window: {recap['window_from']} → {recap['window_to']}",
        f"Generated: {recap['generated_at']}",
        "",
        f"Tasks created:    {t['created']}",
        f"Completed (DONE): {t['completed']}",
        f"Cancelled:        {t['cancelled']}",
        f"Failed:           {t['failed']}",
        f"Active (now):     {t['active_snapshot']}",
        "",
    ]
    if recap["top_agents"]:
        lines.append("Top agents (by DONE):")
        for a in recap["top_agents"]:
            lines.append(f"  {a['agent']:<32} {a['done']}")
        lines.append("")
    if recap["priority_distribution"]:
        lines.append("Priority distribution (DONE):")
        for k, v in recap["priority_distribution"].items():
            lines.append(f"  {k:<10} {v}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate periodic recap from inbox + logs and append to recap.jsonl.")
    p.add_argument("--company", default=None,
                   help="Limit to one company slug (default: all companies).")
    p.add_argument("--window", default="weekly",
                   choices=("daily", "weekly", "monthly", "custom"),
                   help="Predefined window (default: weekly).")
    p.add_argument("--since", default=None,
                   help="Custom window start (YYYY-MM-DD). Required if --window=custom.")
    p.add_argument("--until", default=None,
                   help="Custom window end (YYYY-MM-DD). Defaults to now if --window=custom.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the recap without appending to recap.jsonl.")
    p.add_argument("--quiet", action="store_true",
                   help="Print one-line summary only.")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    now = datetime.now(timezone.utc)
    if args.window == "custom":
        if not args.since:
            print("ERROR: --window=custom requires --since YYYY-MM-DD", file=sys.stderr)
            return 2
        try:
            since = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            until = (datetime.strptime(args.until, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                     if args.until else now)
        except ValueError as e:
            print(f"ERROR: invalid date: {e}", file=sys.stderr)
            return 2
    else:
        since = now - timedelta(days=WINDOWS[args.window])
        until = now

    if since >= until:
        print("ERROR: window 'since' must be earlier than 'until'", file=sys.stderr)
        return 2

    companies = [args.company] if args.company else discover_companies()
    if not companies:
        print("(no companies found)")
        return 0

    try:
        for co in companies:
            recap = build_recap(co, since, until)
            if not args.dry_run:
                tl.append_jsonl(tl.file_path(co, "recap"), recap)
            if args.quiet:
                t = recap["totals"]
                print(f"[{co}] created={t['created']} done={t['completed']} active={t['active_snapshot']}")
            else:
                print(render_human(recap))
                print()
    except OSError as e:
        print(f"IO ERROR: {e}", file=sys.stderr)
        return 3

    return 0


if __name__ == "__main__":
    sys.exit(main())
