#!/usr/bin/env python3
"""
send_approval.py — Send APPROVAL REQUEST to Fathur via Telegram.

Per knowledge/sop/approval-workflow.md.

Usage:
    bin/send_approval.py --type content-publish --priority routine --message "..."

    # With timeout reminder:
    bin/send_approval.py --type publish --priority urgent --message "..." --remind-after 2h

Env vars required:
    TELEGRAM_BOT_TOKEN  — from @BotFather
    TELEGRAM_CHAT_ID    — chat ID for Fathur (use bin/get_chat_id.py to find)

Exit codes:
    0  sent successfully
    1  config error (missing env)
    2  network error
    3  Telegram API rejected message

Source: knowledge/sop/approval-workflow.md + tools/templates/telegram_bot.js pattern.
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime, timezone

try:
    import requests
except ImportError:
    print("ERROR: requests library required. pip install requests", file=sys.stderr)
    sys.exit(1)


TELEGRAM_API = "https://api.telegram.org/bot{token}/sendMessage"

# Log file for approval audit trail (per autonomous-boundaries.md Tier 3 logging)
LOG_PATH = os.environ.get(
    "APPROVAL_LOG",
    os.path.join(os.environ.get("HOLDING_ROOT", "."), "memory", "approvals.jsonl"),
)


def send_telegram(token: str, chat_id: str, message: str, parse_mode: str = "Markdown") -> dict:
    """Send a message via Telegram Bot API. Returns response dict or raises."""
    url = TELEGRAM_API.format(token=token)
    body = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True,
    }
    r = requests.post(url, json=body, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")
    return data


def log_approval_request(record: dict) -> None:
    """Append approval request to audit log."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send approval request to Fathur via Telegram")
    parser.add_argument("--type", required=True,
                        choices=["content-publish", "new-client", "budget", "deploy",
                                 "strategic", "other"],
                        help="Approval request type per approval-workflow.md")
    parser.add_argument("--priority", default="routine",
                        choices=["routine", "time-sensitive", "urgent"])
    parser.add_argument("--message", required=True, help="Full approval message body")
    parser.add_argument("--from", dest="from_agent", default="system",
                        help="Originating agent (e.g., @crypto.research)")
    parser.add_argument("--deadline", default=None, help="ISO timestamp deadline if any")
    parser.add_argument("--ref", default=None, help="Reference ID (e.g., FL-2026-05-19-001)")
    args = parser.parse_args()

    # Verify config
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("ERROR: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars required",
              file=sys.stderr)
        return 1

    # Build message with header
    header = f"🔒 *APPROVAL REQUEST*\n\nType: `{args.type}`\nPriority: `{args.priority}`\nFrom: `{args.from_agent}`"
    if args.deadline:
        header += f"\nDeadline: `{args.deadline}`"
    if args.ref:
        header += f"\nRef: `{args.ref}`"

    full_message = f"{header}\n\n{args.message}"

    # Send
    timestamp = datetime.now(timezone.utc).isoformat()
    record = {
        "timestamp": timestamp,
        "type": args.type,
        "priority": args.priority,
        "from": args.from_agent,
        "ref": args.ref,
        "message_len": len(full_message),
        "status": "sending",
    }

    try:
        resp = send_telegram(token, chat_id, full_message)
        record["status"] = "sent"
        record["telegram_message_id"] = resp.get("result", {}).get("message_id")
        log_approval_request(record)
        print(f"OK: approval request sent (msg_id={record['telegram_message_id']})")
        return 0
    except requests.exceptions.RequestException as e:
        record["status"] = "network_error"
        record["error"] = str(e)
        log_approval_request(record)
        print(f"ERROR: network — {e}", file=sys.stderr)
        return 2
    except Exception as e:
        record["status"] = "api_error"
        record["error"] = str(e)
        log_approval_request(record)
        print(f"ERROR: API — {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
