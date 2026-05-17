#!/usr/bin/env python3
"""
log_message.py — Append an agent-to-agent durable message to messages.jsonl.

Usage:
    bin/log_message.py --company nexusai \
                       --from @nexusai.backend \
                       --to @nexusai.devops \
                       --message "Endpoint /v1/users ready, please deploy to staging" \
                       [--ref-task T001]

Use this only for durable cross-agent comms that the receiving agent should
see at session start. Don't log basa-basi here either.
"""

from __future__ import annotations

import argparse
import json
import sys

import task_logger as tl


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Append agent-to-agent message to messages.jsonl.")
    p.add_argument("--company", required=True)
    p.add_argument("--from", required=True, dest="from_")
    p.add_argument("--to", required=True)
    p.add_argument("--message", required=True)
    p.add_argument("--ref-task", default=None, dest="ref_task",
                   help="Optional task ID this message refers to.")
    p.add_argument("--quiet", action="store_true")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    try:
        entry = tl.log_message(
            company=args.company,
            from_=args.from_,
            to=args.to,
            message=args.message,
            ref_task=args.ref_task,
        )
    except tl.TaskLoggerError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    except OSError as e:
        print(f"IO ERROR: {e}", file=sys.stderr)
        return 3

    if args.quiet:
        print("OK")
    else:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
