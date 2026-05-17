#!/bin/bash
# run_crypto_tools.sh — Daily refresh of crypto data tools
# =========================================================
# Triggered daily 07:00 WIB (00:00 UTC) per weekly-cadence.md.
#
# Runs each tool, captures output, logs failures.
# Output cached in: companies/crypto-consultant/tasks/cache/
#
set -euo pipefail

HOLDING_ROOT="${HOLDING_ROOT:-/home/fatur/ai-holding}"
DATE="$(date -u +%Y-%m-%d)"
CACHE_DIR="${HOLDING_ROOT}/companies/crypto-consultant/tasks/cache"
LOG_DIR="${HOLDING_ROOT}/logs"
LOG_FILE="${LOG_DIR}/crypto-tools-${DATE}.log"

mkdir -p "$CACHE_DIR" "$LOG_DIR"

cd "$HOLDING_ROOT"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_FILE"
}

log "=== DAILY CRYPTO TOOLS REFRESH — ${DATE} ==="

declare -a TOOLS=(
    "fear_greed"
    "btc_price"
    "funding_rates"
    "onchain_metrics"
    "news_scraper"
    "pattern_detector"
)

failed=0
for tool in "${TOOLS[@]}"; do
    tool_path="tools/${tool}.py"
    out_path="${CACHE_DIR}/${tool}-${DATE}.json"

    if [[ ! -f "$tool_path" ]]; then
        log "  ${tool}: SKIP (file not found)"
        continue
    fi

    if python3 "$tool_path" --json > "$out_path" 2>>"$LOG_FILE"; then
        size=$(wc -c < "$out_path")
        log "  ${tool}: OK (${size} bytes)"
    else
        log "  ${tool}: FAIL"
        failed=$((failed + 1))
    fi
done

log "=== DONE — ${failed} failures ==="
exit "$failed"
