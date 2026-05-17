#!/usr/bin/env python3
"""
check_pending_approvals.py — Scan approvals.jsonl, send timeout reminders.

Per knowledge/sop/approval-workflow.md timeout policy:
- routine: reminder at +24h, +48h
- time-sensitive: reminder at +6h
- urgent: reminder at +2h
- After +72h: log TIMED_OUT, do NOT proceed

Triggered every 2 hours by cron (during waking hours).

Usage:
    bin/check_pending_approvals.py           # production
    bin/check_pending_approvals.py --dry-run # log decisions without sending
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta
from typing import Optional


HOLDING_ROOT = os.environ.get("HOLDING_ROOT", os.getcwd())
LOG_PATH = os.path.join(HOLDING_ROOT, "memory", "approvals.jsonl")

# Timeout thresholds (hours since send)
REMINDER_RULES = {
    "routine":        [24, 48],   # remind at +24h, +48h
    "time-sensitive": [6, 12, 24],
    "urgent":         [2, 4, 6],
}
TIMEOUT_AT = {
    "routine":        72,
    "time-sensitive": 48,
    "urgent":         24,
}


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def hours_since(ts: str) -> float:
    return (datetime.now(timezone.utc) - parse_iso(ts)).total_seconds() / 3600


def load_approvals() -> list:
    if not os.path.exists(LOG_PATH):
        return []
    items = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items


def append_record(record: dict) -> None:
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def send_reminder(record: dict, hours: float, dry_run: bool) -> None:
    ref = record.get("ref", "?")
    type_ = record.get("type", "?")
    msg = (
        f"⏰ *REMINDER — {type_.upper()}*\n\n"
        f"Approval pending {hours:.0f}h.\n"
        f"Ref: `{ref}`\n\n"
        f"Reply yes/no/revise/hold."
    )
    if dry_run:
        print(f"[DRY] would remind: {ref} ({hours:.0f}h)")
        return

    # Use send_approval.py for consistency
    import subprocess
    res = subprocess.run([
        "python3", os.path.join(HOLDING_ROOT, "bin", "send_approval.py"),
        "--type", "other",
        "--priority", "urgent" if hours > 24 else "time-sensitive",
        "--message", msg,
        "--ref", ref or "",
    ], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"reminder send failed for {ref}: {res.stderr}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    records = load_approvals()
    if not records:
        print("no approval records yet")
        return 0

    # Group by ref: find latest "sent" without resolution
    pending: dict[str, dict] = {}
    for r in records:
        ref = r.get("ref")
        status = r.get("status")
        if not ref:
            continue
        if status == "sent":
            pending[ref] = r
        elif status in ("approved", "rejected", "timed_out"):
            pending.pop(ref, None)

    if not pending:
        print("no pending approvals")
        return 0

    now = datetime.now(timezone.utc)
    actions = 0
    for ref, rec in pending.items():
        priority = rec.get("priority", "routine")
        sent_at = rec.get("timestamp")
        if not sent_at:
            continue

        elapsed_h = hours_since(sent_at)

        # Check timeout
        timeout_h = TIMEOUT_AT.get(priority, 72)
        if elapsed_h >= timeout_h:
            timeout_record = {
                "timestamp": now.isoformat(),
                "ref": ref,
                "type": rec.get("type"),
                "priority": priority,
                "status": "timed_out",
                "elapsed_hours": round(elapsed_h, 1),
            }
            append_record(timeout_record)
            print(f"TIMED OUT: {ref} (elapsed {elapsed_h:.1f}h)")
            actions += 1
            continue

        # Check reminders due
        reminder_thresholds = REMINDER_RULES.get(priority, [24, 48])
        last_reminder_h = rec.get("_last_reminder_h", 0)

        for threshold in reminder_thresholds:
            if elapsed_h >= threshold > last_reminder_h:
                send_reminder(rec, elapsed_h, args.dry_run)
                # Mark reminder sent
                if not args.dry_run:
                    append_record({
                        "timestamp": now.isoformat(),
                        "ref": ref,
                        "status": "reminder_sent",
                        "elapsed_hours": round(elapsed_h, 1),
                    })
                actions += 1
                break

    print(f"checked {len(pending)} pending, {actions} actions taken")
    return 0


if __name__ == "__main__":
    sys.exit(main())
