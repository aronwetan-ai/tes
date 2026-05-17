#!/usr/bin/env python3
"""
log_task.py — Create a new task in a company's inbox.jsonl.

Usage:
    bin/log_task.py --company nexusai \
                    --to @nexusai.backend \
                    --task "Design REST API for user-service" \
                    [--from USER] \
                    [--priority HIGH] \
                    [--context '{"sprint":"S1"}']

Exit codes:
    0  task created
    2  invalid arguments / schema error
    3  filesystem / I/O error

See knowledge/agent-design/task-logger-rules.md for what to log and what NOT.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

import task_logger as tl


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Create a new task in a company's inbox.jsonl.")
    p.add_argument("--company", required=True,
                   help="Company slug (nexusai | brandflow | crypto-consultant | holding).")
    p.add_argument("--to", required=True, dest="to",
                   help="Target agent (e.g. @nexusai.backend) or company (@nexusai).")
    p.add_argument("--task", required=True,
                   help="One-line task description (min 8 chars).")
    p.add_argument("--from", default="USER", dest="from_",
                   help="Originator (default: USER).")
    p.add_argument("--priority", default="MEDIUM",
                   choices=sorted(tl.VALID_PRIORITIES),
                   help="Task priority (default: MEDIUM).")
    p.add_argument("--context", default=None,
                   help="Optional JSON object string with extra context.")
    p.add_argument("--id", default=None, dest="task_id",
                   help="Force a specific task ID (default: auto T001, T002...).")
    p.add_argument("--quiet", action="store_true",
                   help="On success, only print the task ID, not the full JSON.")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    context: Dict[str, Any] = {}
    if args.context:
        try:
            context = json.loads(args.context)
            if not isinstance(context, dict):
                raise ValueError("context must be a JSON object")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"ERROR: --context invalid JSON object: {e}", file=sys.stderr)
            return 2

    try:
        entry = tl.create_task(
            company=args.company,
            from_=args.from_,
            to=args.to,
            task=args.task,
            priority=args.priority,
            context=context,
            task_id=args.task_id,
        )
    except tl.TaskLoggerError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"IO ERROR: {e}", file=sys.stderr)
        return 3

    if args.quiet:
        print(entry["id"])
    else:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
