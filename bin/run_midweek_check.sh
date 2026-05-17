#!/bin/bash
# run_midweek_check.sh — Wednesday mid-week refresh check
# =========================================================
# Triggered Wednesday 07:00 WIB (00:00 UTC) per weekly-cadence.md.
#
# Tasks:
# 1. Refresh crypto tools (delegates to run_crypto_tools.sh)
# 2. Check if anything materially changed since Monday brief
# 3. If material change → produce update brief (queue for approval)
#
set -euo pipefail

HOLDING_ROOT="${HOLDING_ROOT:-/home/fatur/ai-holding}"
DATE="$(date -u +%Y-%m-%d)"
LOG_DIR="${HOLDING_ROOT}/logs"
LOG_FILE="${LOG_DIR}/midweek-${DATE}.log"

mkdir -p "$LOG_DIR"
cd "$HOLDING_ROOT"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_FILE"
}

log "=== MID-WEEK CHECK — ${DATE} ==="

# 1. Refresh tools
log "[1/3] refreshing crypto tools"
bash bin/run_crypto_tools.sh >> "$LOG_FILE" 2>&1 || log "WARN: tools refresh had failures"

# 2. Detect material change vs Monday baseline
log "[2/3] comparing vs Monday baseline"
MONDAY_DATE="$(date -u -d 'last monday' +%Y-%m-%d 2>/dev/null || date -u -v-mon +%Y-%m-%d 2>/dev/null || echo "")"
if [[ -n "$MONDAY_DATE" ]]; then
    MONDAY_FG="${HOLDING_ROOT}/companies/crypto-consultant/tasks/cache/fear_greed-${MONDAY_DATE}.json"
    TODAY_FG="${HOLDING_ROOT}/companies/crypto-consultant/tasks/cache/fear_greed-${DATE}.json"

    if [[ -f "$MONDAY_FG" ]] && [[ -f "$TODAY_FG" ]]; then
        # Simple diff: compare F&G value (assuming JSON has "value" key)
        m_val=$(python3 -c "import json; print(json.load(open('$MONDAY_FG')).get('value', 0))" 2>/dev/null || echo 0)
        t_val=$(python3 -c "import json; print(json.load(open('$TODAY_FG')).get('value', 0))" 2>/dev/null || echo 0)
        delta=$((t_val - m_val))
        abs_delta=${delta#-}

        log "  F&G: Monday=${m_val}, Today=${t_val}, delta=${delta}"

        if [[ "$abs_delta" -gt 20 ]]; then
            log "  MATERIAL CHANGE detected (|delta| > 20)"
            log "  TODO: trigger update brief"
        else
            log "  no material change"
        fi
    else
        log "  baseline files missing — skip comparison"
    fi
fi

# 3. (Future) Auto-trigger update brief if change material
log "[3/3] no automatic update brief triggered (manual decision for now)"

log "=== MID-WEEK CHECK COMPLETE ==="
exit 0
