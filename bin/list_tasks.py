#!/usr/bin/env python3
"""
list_tasks.py — Filter and list tasks in a company's inbox.jsonl.

Usage:
    bin/list_tasks.py --company nexusai
    bin/list_tasks.py --company nexusai --status IN_PROGRESS
    bin/list_tasks.py --company crypto-consultant --agent @crypto.research
    bin/list_tasks.py --company brandflow --priority HIGH --active-only
    bin/list_tasks.py --company nexusai --format json
    bin/list_tasks.py --company nexusai --format jsonl

Output formats:
    table  (default) — compact one-line-per-task summary
    json             — pretty-printed JSON array
    jsonl            — one JSON object per line (machine-readable)
"""

from __future__ import annotations

import argparse
import json
import sys

import task_logger as tl


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Filter and list tasks from a company's inbox.jsonl.")
    p.add_argument("--company", required=True)
    p.add_argument("--status", default=None,
                   choices=sorted(tl.VALID_STATUSES))
    p.add_argument("--priority", default=None,
                   choices=sorted(tl.VALID_PRIORITIES))
    p.add_argument("--agent", default=None,
                   help="Match against either 'to' or 'from' field.")
    p.add_argument("--active-only", action="store_true",
                   help="Hide DONE / FAILED / CANCELLED.")
    p.add_argument("--format", default="table",
                   choices=("table", "json", "jsonl"))
    return p.parse_args()


def render_table(rows):
    if not rows:
        print("(no tasks)")
        return
    # Compact, fixed-width-ish table for terminals.
    header = f"{'ID':<5} {'STATUS':<12} {'PRIO':<7} {'TO':<28} TASK"
    print(header)
    print("-" * len(header))
    for e in rows:
        task = e.get("task", "")
        if len(task) > 60:
            task = task[:57] + "..."
        print(f"{e.get('id',''):<5} "
              f"{e.get('status',''):<12} "
              f"{e.get('priority',''):<7} "
              f"{e.get('to',''):<28} "
              f"{task}")


def main() -> int:
    args = parse_args()

    try:
        rows = tl.list_tasks(
            company=args.company,
            status=args.status,
            agent=args.agent,
            priority=args.priority,
            include_terminal=not args.active_only,
        )
    except tl.TaskLoggerError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"IO ERROR: {e}", file=sys.stderr)
        return 3

    if args.format == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif args.format == "jsonl":
        for e in rows:
            print(json.dumps(e, ensure_ascii=False, separators=(",", ":")))
    else:
        render_table(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
