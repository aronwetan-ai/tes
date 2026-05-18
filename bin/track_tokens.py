#!/usr/bin/env python3
<<<<<<< HEAD
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

=======
"""Track token usage per heartbeat cycle for Paperclip budget."""
>>>>>>> b58e15b (ndak tau)
import json
import os
from datetime import datetime, timezone

<<<<<<< HEAD
DEFAULT_BUDGET_LOG = os.path.expanduser(
    "~/.local/share/ai-holding/budget-log.jsonl"
)
BUDGET_LOG = os.getenv("PAPERCLIP_BUDGET_LOG", DEFAULT_BUDGET_LOG)
=======
BUDGET_LOG = os.path.expanduser("~/.paperclip/companies/ai-holding/budget-log.jsonl")
>>>>>>> b58e15b (ndak tau)

def log_usage(employee: str, tokens_used: int, task_summary: str):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "employee": employee,
        "tokens_used": tokens_used,
        "task_summary": task_summary,
    }
    os.makedirs(os.path.dirname(BUDGET_LOG), exist_ok=True)
    with open(BUDGET_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        log_usage(sys.argv[1], int(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "")
