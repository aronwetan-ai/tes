#!/usr/bin/env bash
#
# log-task.sh — Thin ergonomic wrapper around bin/log_task.py.
#
# Usage:
#   bin/log-task.sh <company> <to-agent> "<task description>" [priority]
#
# Examples:
#   bin/log-task.sh nexusai @nexusai.backend "Design REST API for user-service" HIGH
#   bin/log-task.sh brandflow @brandflow.copywriter "Caption IG launch sprint"
#   bin/log-task.sh crypto-consultant @crypto.research "Riset narasi BTC weekly"
#
# Defaults:
#   priority = MEDIUM
#   from     = USER
#
# For full options (context JSON, custom from, custom ID, --quiet) use log_task.py directly.

set -e

if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
  echo "Usage: $0 <company> <to-agent> \"<task description>\" [priority]" >&2
  echo "  priority: LOW | MEDIUM | HIGH | URGENT (default MEDIUM)" >&2
  exit 2
fi

COMPANY="$1"
TO="$2"
TASK="$3"
PRIORITY="${4:-MEDIUM}"

DIR="$(cd "$(dirname "$0")" && pwd)"

exec python3 "$DIR/log_task.py" \
  --company "$COMPANY" \
  --to "$TO" \
  --task "$TASK" \
  --priority "$PRIORITY"
