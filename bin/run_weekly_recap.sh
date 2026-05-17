#!/bin/bash
# run_weekly_recap.sh — Friday Weekly Recap
# ==========================================
# Triggered by cron Jumat 09:00 WIB (02:00 UTC).
# Per knowledge/sop/weekly-cadence.md Friday slot.
#
# Tasks:
# 1. Each company CEO produces weekly recap
# 2. System Audit Protocol runs (knowledge/sop/system-audit.md)
# 3. Cross-company smoke test
# 4. Send recap summary to Fathur via Telegram
#
set -euo pipefail

HOLDING_ROOT="${HOLDING_ROOT:-/home/fatur/ai-holding}"
WEEK_OF="$(date -u +%Y-%m-%d)"
LOG_DIR="${HOLDING_ROOT}/logs"
LOG_FILE="${LOG_DIR}/recap-${WEEK_OF}.log"
mkdir -p "$LOG_DIR"

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_FILE"
}

cd "$HOLDING_ROOT"
log "=== WEEKLY RECAP START — week of ${WEEK_OF} ==="

# ============================================================
# STEP 1 — Smoke test (cross-company integration health)
# ============================================================
log "[1/4] smoke test"
SMOKE_RESULTS="${LOG_DIR}/smoke-${WEEK_OF}.txt"
{
    echo "=== Cross-Company Smoke Test (${WEEK_OF}) ==="
    for f in \
        knowledge/sop/cross-company-handoff.md \
        knowledge/sop/cross-company-qa-routing.md \
        knowledge/sop/approval-workflow.md \
        knowledge/sop/autonomous-boundaries.md \
        knowledge/sop/weekly-cadence.md \
        knowledge/sop/debug-protocol.md \
        knowledge/sop/system-audit.md \
        knowledge/sop/strategic-thinking.md \
        knowledge/sop/data-analysis-protocol.md \
        knowledge/agent-design/reflection-loop.md \
        tools/llm_client.py \
        tools/templates/telegram_bot.js \
        tools/templates/fastapi_webhook.py
    do
        if [[ -f "$f" ]]; then
            echo "✅ $f"
        else
            echo "❌ MISSING: $f"
        fi
    done
} | tee "$SMOKE_RESULTS"

MISSING=$(grep -c "^❌" "$SMOKE_RESULTS" || echo 0)
log "[1/4] smoke test: ${MISSING} missing files"

# ============================================================
# STEP 2 — Aggregate weekly task logs
# ============================================================
log "[2/4] aggregating task logs"
TASKS_SUMMARY="${LOG_DIR}/tasks-summary-${WEEK_OF}.txt"
{
    echo "=== Weekly Task Summary (${WEEK_OF}) ==="
    for company in brandflow crypto-consultant nexusai; do
        log_file="companies/${company}/tasks/logs.jsonl"
        if [[ -f "$log_file" ]]; then
            count=$(wc -l < "$log_file")
            echo "${company}: ${count} task entries"
        fi
    done
} > "$TASKS_SUMMARY"
cat "$TASKS_SUMMARY" | tee -a "$LOG_FILE"

# ============================================================
# STEP 3 — System audit (per knowledge/sop/system-audit.md)
# ============================================================
log "[3/4] system audit (Friday slot)"
AUDIT_OUT="${LOG_DIR}/audit-${WEEK_OF}.md"
{
    echo "# System Audit — ${WEEK_OF}"
    echo ""
    echo "## Layer 1 — Output Quality"
    echo "(Manual review of $TASKS_SUMMARY needed)"
    echo ""
    echo "## Layer 2 — Skill Coverage"
    echo "Active SOPs: $(ls knowledge/sop/*.md | wc -l) files"
    echo "Active tools: $(ls tools/*.py | wc -l) tools"
    echo ""
    echo "## Layer 3 — Routing Precision"
    echo "Cross-QA pending review: TBD (manual)"
    echo ""
    echo "## Layer 4 — Token Efficiency"
    echo "MEMORY.md size: $(wc -c < MEMORY.md 2>/dev/null || echo 'n/a') bytes"
    echo "memory/global.md: $(wc -c < memory/global.md 2>/dev/null || echo 'n/a') bytes"
} > "$AUDIT_OUT"
log "[3/4] audit saved: $AUDIT_OUT"

# ============================================================
# STEP 4 — Send recap to Fathur
# ============================================================
log "[4/4] sending recap to Fathur"

RECAP_MSG=$(cat <<EOF
📋 *WEEKLY RECAP — ${WEEK_OF}*

*Smoke Test:* ${MISSING} missing files
*Tasks logged:* see ${TASKS_SUMMARY}
*Audit:* see ${AUDIT_OUT}

Full logs: ${LOG_DIR}/

Have a good weekend!
EOF
)

if [[ "$DRY_RUN" == "true" ]]; then
    log "DRY-RUN — would send:"
    echo "$RECAP_MSG" | tee -a "$LOG_FILE"
elif [[ -f "bin/send_approval.py" ]] && [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]]; then
    python3 bin/send_approval.py \
        --type "other" \
        --priority "routine" \
        --message "$RECAP_MSG" \
        --from "system" \
        2>>"$LOG_FILE" || log "WARN: Telegram recap send failed"
else
    log "no Telegram config — recap shown in log only"
    echo "$RECAP_MSG" | tee -a "$LOG_FILE"
fi

log "=== WEEKLY RECAP COMPLETE ==="
exit 0
