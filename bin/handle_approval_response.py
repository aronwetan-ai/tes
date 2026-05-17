#!/usr/bin/env python3
"""
handle_approval_response.py — Process Fathur's approval reply from Telegram.

Designed to be called by the Telegram bot (tools/templates/telegram_bot.js)
when Fathur replies to an APPROVAL REQUEST. Or invoked manually:

    bin/handle_approval_response.py --ref FL-2026-05-19-001 --reply "yes"
    bin/handle_approval_response.py --ref FL-2026-05-19-001 --reply "revise: change the hook"

Maps reply → status → triggers downstream action:
    yes / approved / lanjut / go      → status=approved → trigger publish
    no / cancel / batal               → status=rejected → archive
    revise / ubah: <feedback>         → status=revise → re-route to copywriter
    hold / nanti                      → status=hold → defer to next reminder cycle

Per knowledge/sop/approval-workflow.md.

Exit codes:
    0  processed successfully
    1  unknown reply / parse failed
    2  ref not found / already resolved
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime, timezone


HOLDING_ROOT = os.environ.get("HOLDING_ROOT", os.getcwd())
LOG_PATH = os.path.join(HOLDING_ROOT, "memory", "approvals.jsonl")


# Reply patterns (case-insensitive)
APPROVE_PATTERNS = re.compile(r"^\s*(yes|y|ok|approved|lanjut|go|✅)\s*$", re.IGNORECASE)
REJECT_PATTERNS = re.compile(r"^\s*(no|n|cancel|batal|jangan|❌)\s*$", re.IGNORECASE)
HOLD_PATTERNS = re.compile(r"^\s*(hold|nanti|later|⏸)\s*$", re.IGNORECASE)
REVISE_PATTERNS = re.compile(r"^\s*(revise|ubah)[:\s]\s*(.+)$", re.IGNORECASE | re.DOTALL)


def classify_reply(text: str) -> tuple[str, str]:
    """Return (status, feedback). status in: approved, rejected, hold, revise, unknown."""
    if APPROVE_PATTERNS.match(text):
        return "approved", ""
    if REJECT_PATTERNS.match(text):
        return "rejected", ""
    if HOLD_PATTERNS.match(text):
        return "hold", ""
    m = REVISE_PATTERNS.match(text)
    if m:
        return "revise", m.group(2).strip()
    return "unknown", text


def find_pending(ref: str) -> dict | None:
    """Find the latest 'sent' record for ref that hasn't been resolved."""
    if not os.path.exists(LOG_PATH):
        return None
    target = None
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("ref") != ref:
                continue
            status = rec.get("status")
            if status == "sent":
                target = rec
            elif status in ("approved", "rejected", "timed_out"):
                return None  # already resolved
    return target


def append_response(record: dict) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def trigger_downstream(status: str, ref: str, feedback: str) -> None:
    """Fire the next action based on approval status."""
    print(f"\n[downstream] ref={ref} status={status}")
    if status == "approved":
        print(f"  → schedule publish (TODO: wire to BrandFlow social calendar)")
    elif status == "rejected":
        print(f"  → archive draft, no publish")
    elif status == "revise":
        print(f"  → re-route to @brandflow.copywriter with feedback:")
        print(f"    \"{feedback}\"")
    elif status == "hold":
        print(f"  → defer; check_pending_approvals will resend reminder later")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", required=True, help="Reference ID of approval request")
    parser.add_argument("--reply", required=True, help="Fathur's reply text")
    parser.add_argument("--user", default="fathur", help="User who replied (audit)")
    args = parser.parse_args()

    status, feedback = classify_reply(args.reply.strip())
    if status == "unknown":
        print(f"ERROR: cannot parse reply: {args.reply!r}", file=sys.stderr)
        return 1

    pending = find_pending(args.ref)
    if not pending:
        print(f"ERROR: no pending approval for ref={args.ref}", file=sys.stderr)
        return 2

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ref": args.ref,
        "type": pending.get("type"),
        "status": status,
        "feedback": feedback,
        "user": args.user,
        "reply_raw": args.reply,
    }
    append_response(record)
    print(f"OK: ref={args.ref} status={status}")

    trigger_downstream(status, args.ref, feedback)
    return 0


if __name__ == "__main__":
    sys.exit(main())
