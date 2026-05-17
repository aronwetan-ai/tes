#!/usr/bin/env python3
"""
update_task.py — Transition an existing task's status.

Usage:
    bin/update_task.py --company nexusai --id T001 --status IN_PROGRESS
    bin/update_task.py --company nexusai --id T001 --status DONE \
                       --note "merged in PR #12" --actor @nexusai.backend

State machine:
    NEW         → IN_PROGRESS, CANCELLED
    IN_PROGRESS → DONE, FAILED, CANCELLED
    FAILED      → RETRY, CANCELLED
    RETRY       → IN_PROGRESS, CANCELLED
    DONE        → (terminal)
    CANCELLED   → (terminal)

Exit codes:
    0  status updated
    2  invalid arguments / illegal transition / task not found
    3  filesystem / I/O error
"""

from __future__ import annotations

import argparse
import json
import sys

import task_logger as tl


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Transition an existing task's status.")
    p.add_argument("--company", required=True)
    p.add_argument("--id", required=True, dest="task_id",
                   help="Task ID, e.g. T001.")
    p.add_argument("--status", required=True,
                   choices=sorted(tl.VALID_STATUSES),
                   help="Target status.")
    p.add_argument("--note", default=None,
                   help="Free-form note recorded in audit log + task history.")
    p.add_argument("--actor", default="MAIN",
                   help="Who performed the transition (default: MAIN).")
    p.add_argument("--quiet", action="store_true",
                   help="On success, only print 'OK <id> <old> -> <new>'.")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    try:
        entry = tl.update_task_status(
            company=args.company,
            task_id=args.task_id,
            new_status=args.status,
            note=args.note,
            actor=args.actor,
        )
    except tl.TaskLoggerError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"IO ERROR: {e}", file=sys.stderr)
        return 3

    if args.quiet:
        print(f"OK {entry['id']} -> {entry['status']}")
    else:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
