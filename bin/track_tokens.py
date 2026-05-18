#!/usr/bin/env python3
"""
Supplementary token usage tracker for Paperclip integration.

NOTE: Paperclip natively tracks budget via embedded Postgres
(`spentMonthlyCents` field per agent, accessible via API). This script is
SUPPLEMENTARY — useful for custom labels/task summaries that Paperclip's
native tracking doesn't capture, OR for periods when Paperclip is offline.

For native Paperclip budget query:
    curl http://localhost:3100/api/agents/<agent-id> -H "Authorization: Bearer $KEY"
    # → look at spentMonthlyCents / budgetMonthlyCents fields

Usage:
    python3 bin/track_tokens.py <employee> <tokens_used> [task_summary]

Examples:
    python3 bin/track_tokens.py rei 1500 "routed 3 tasks to @nexusai"
    python3 bin/track_tokens.py nexusai-cto 8000 "code review + deploy"
    python3 bin/track_tokens.py brandflow-cmo 5000 "content calendar update"

Output: Appends JSON entry to ~/.local/share/ai-holding/budget-log.jsonl
        (NOT inside ~/.paperclip/ to avoid conflicting with Paperclip's
         own data dir — keep our supplementary log separate)
Exit codes: 0 = success, 2 = arg error
"""

import json
import os
import sys
from datetime import datetime, timezone

DEFAULT_BUDGET_LOG = os.path.expanduser(
    "~/.local/share/ai-holding/budget-log.jsonl"
)
BUDGET_LOG = os.getenv("PAPERCLIP_BUDGET_LOG", DEFAULT_BUDGET_LOG)


def log_usage(employee: str, tokens_used: int, task_summary: str = ""):
    """Append token usage entry to budget log."""
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "employee": employee,
        "tokens_used": tokens_used,
        "task_summary": task_summary,
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
    }
    os.makedirs(os.path.dirname(BUDGET_LOG), exist_ok=True)
    with open(BUDGET_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def get_daily_usage(employee: str = None, date: str = None):
    """Get total token usage for today (or specified date)."""
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    total = 0
    if not os.path.exists(BUDGET_LOG):
        return total

    with open(BUDGET_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("date") == date:
                    if employee is None or entry.get("employee") == employee:
                        total += entry.get("tokens_used", 0)
            except json.JSONDecodeError:
                continue
    return total


def main():
    if len(sys.argv) < 3:
        print("Usage: track_tokens.py <employee> <tokens_used> [task_summary]", file=sys.stderr)
        print("       track_tokens.py --status [employee]", file=sys.stderr)
        sys.exit(2)

    # Status check mode
    if sys.argv[1] == "--status":
        employee = sys.argv[2] if len(sys.argv) > 2 else None
        usage = get_daily_usage(employee)
        label = f" ({employee})" if employee else " (all)"
        print(f"Daily token usage{label}: {usage:,}")
        return

    # Log mode
    employee = sys.argv[1]
    try:
        tokens_used = int(sys.argv[2])
    except ValueError:
        print(f"ERROR: tokens_used must be integer, got: {sys.argv[2]}", file=sys.stderr)
        sys.exit(2)

    task_summary = sys.argv[3] if len(sys.argv) > 3 else ""

    entry = log_usage(employee, tokens_used, task_summary)
    daily_total = get_daily_usage(employee)

    print(json.dumps({
        "logged": entry,
        "daily_total": daily_total,
    }, indent=2))


if __name__ == "__main__":
    main()
