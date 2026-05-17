#!/bin/bash
# install_cron.sh — Install/update cron jobs for AI Holding autonomous cadence
# =============================================================================
# Per knowledge/sop/weekly-cadence.md.
# Idempotent: safely re-runnable; replaces our cron entries without duplicating.
#
# Usage:
#   sudo bin/install_cron.sh             # install for current user
#   bin/install_cron.sh --user fatur     # install for specific user
#   bin/install_cron.sh --uninstall      # remove all our entries
#   bin/install_cron.sh --show           # display current crontab
#
# All times converted to UTC (server timezone). WIB = UTC+7.
#
set -euo pipefail

HOLDING_ROOT="${HOLDING_ROOT:-/home/fatur/ai-holding}"
TARGET_USER="${USER}"
ACTION="install"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --user)        TARGET_USER="$2"; shift 2 ;;
        --uninstall)   ACTION="uninstall"; shift ;;
        --show)        ACTION="show"; shift ;;
        *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done

# Marker comments for our entries (used to find/remove them)
MARKER_START="# === AI HOLDING AUTONOMOUS CADENCE — START ==="
MARKER_END="# === AI HOLDING AUTONOMOUS CADENCE — END ==="

build_cron_entries() {
cat <<EOF
${MARKER_START}
# Per knowledge/sop/weekly-cadence.md — managed by bin/install_cron.sh

# Daily 07:00 WIB (00:00 UTC) — refresh all crypto tools
0 0 * * * cd ${HOLDING_ROOT} && bash bin/run_crypto_tools.sh >> logs/cron.log 2>&1

# Monday 07:00 WIB (00:00 UTC, dow=1) — weekly crypto brief
0 0 * * 1 cd ${HOLDING_ROOT} && bash bin/run_weekly_brief.sh >> logs/cron.log 2>&1

# Wednesday 07:00 WIB (00:00 UTC, dow=3) — mid-week refresh check
0 0 * * 3 cd ${HOLDING_ROOT} && bash bin/run_midweek_check.sh >> logs/cron.log 2>&1

# Friday 09:00 WIB (02:00 UTC, dow=5) — weekly recap
0 2 * * 5 cd ${HOLDING_ROOT} && bash bin/run_weekly_recap.sh >> logs/cron.log 2>&1

# Approval timeout reminder (every 2h between 06:00-22:00 WIB) — chase pending Tier 3 requests
0 23,1,3,5,7,9,11,13,15 * * * cd ${HOLDING_ROOT} && python3 bin/check_pending_approvals.py >> logs/cron.log 2>&1
${MARKER_END}
EOF
}

case "$ACTION" in
    show)
        crontab -u "$TARGET_USER" -l 2>/dev/null || echo "(no crontab for $TARGET_USER)"
        ;;
    uninstall)
        echo "Removing AI Holding cron entries for $TARGET_USER..."
        existing=$(crontab -u "$TARGET_USER" -l 2>/dev/null || echo "")
        if [[ -z "$existing" ]]; then
            echo "(no crontab to clean)"
            exit 0
        fi
        # Remove block between markers
        cleaned=$(echo "$existing" | awk -v s="$MARKER_START" -v e="$MARKER_END" '
            $0 == s {skip=1; next}
            $0 == e {skip=0; next}
            !skip {print}
        ')
        echo "$cleaned" | crontab -u "$TARGET_USER" -
        echo "Done."
        ;;
    install)
        echo "Installing AI Holding cron for user: $TARGET_USER"
        echo "Holding root: $HOLDING_ROOT"

        # Verify HOLDING_ROOT exists
        if [[ ! -d "$HOLDING_ROOT" ]]; then
            echo "ERROR: $HOLDING_ROOT does not exist" >&2
            exit 1
        fi

        # Build new crontab: existing entries minus our block + new block
        existing=$(crontab -u "$TARGET_USER" -l 2>/dev/null || echo "")

        # Remove old AI Holding block if present
        cleaned=$(echo "$existing" | awk -v s="$MARKER_START" -v e="$MARKER_END" '
            $0 == s {skip=1; next}
            $0 == e {skip=0; next}
            !skip {print}
        ')

        # Append new block
        new_crontab=$(printf "%s\n\n%s\n" "$cleaned" "$(build_cron_entries)")

        echo "$new_crontab" | crontab -u "$TARGET_USER" -

        echo ""
        echo "Installed. Verify:"
        echo "  crontab -u $TARGET_USER -l"
        echo ""
        echo "Logs will be written to: $HOLDING_ROOT/logs/cron.log"
        echo "Make sure logs/ exists and is writable."
        mkdir -p "${HOLDING_ROOT}/logs"
        echo "  ✓ logs/ directory ready"
        ;;
esac
