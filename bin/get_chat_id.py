#!/usr/bin/env python3
"""
get_chat_id.py — One-time helper to discover your Telegram chat_id.

Use this AFTER:
1. Created bot via @BotFather, set TELEGRAM_BOT_TOKEN
2. Sent ANY message to your bot from the chat you want to receive notifications

Usage:
    export TELEGRAM_BOT_TOKEN="..."
    bin/get_chat_id.py

Output: list of recent chat_ids that messaged the bot. Pick yours, set TELEGRAM_CHAT_ID.
"""

import os
import sys
import json

try:
    import requests
except ImportError:
    print("pip install requests", file=sys.stderr)
    sys.exit(1)


def main() -> int:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN not set", file=sys.stderr)
        return 1

    url = f"https://api.telegram.org/bot{token}/getUpdates"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()

    if not data.get("ok"):
        print(f"API error: {data}", file=sys.stderr)
        return 2

    updates = data.get("result", [])
    if not updates:
        print("No messages yet. Send any message to the bot from your chat first, then re-run.")
        return 0

    seen = {}
    for upd in updates:
        msg = upd.get("message") or upd.get("edited_message") or {}
        chat = msg.get("chat") or {}
        cid = chat.get("id")
        if cid and cid not in seen:
            name = chat.get("first_name") or chat.get("title") or "?"
            chat_type = chat.get("type", "?")
            seen[cid] = (name, chat_type)

    print("Chats that messaged your bot:")
    print("-" * 50)
    for cid, (name, ctype) in seen.items():
        print(f"  chat_id={cid}  type={ctype}  name='{name}'")
    print("-" * 50)
    print("\nSet: export TELEGRAM_CHAT_ID=<id-yours>")
    return 0


if __name__ == "__main__":
    sys.exit(main())
