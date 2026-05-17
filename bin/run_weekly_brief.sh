#!/bin/bash
# run_weekly_brief.sh — Weekly Crypto Brief Orchestrator
# =======================================================
#
# Triggered by cron Senin 07:00 WIB (00:00 UTC).
# Chains: tools refresh → research → handoff → BrandFlow draft → QA → approval request.
#
# Per knowledge/sop/weekly-cadence.md.
# Output dilog ke /var/log/weekly.log (cron) atau ./logs/weekly-YYYY-MM-DD.log (manual).
#
# Exit codes:
#   0 — completed successfully (approval request sent to Fathur)
#   1 — pre-flight check failed
#   2 — tool execution failed (research blocked)
#   3 — research synthesis failed
#   4 — handoff/QA failed
#   5 — approval send failed (Telegram down)
#
# Usage:
#   bin/run_weekly_brief.sh                    # production run
#   bin/run_weekly_brief.sh --dry-run          # skip Telegram, log only
#   bin/run_weekly_brief.sh --skip-tools       # use cached tool data
#
set -euo pipefail

# ============================================================
# CONFIG
# ============================================================
HOLDING_ROOT="${HOLDING_ROOT:-/home/fatur/ai-holding}"
WEEK_OF="$(date -u +%Y-%m-%d)"
LOG_DIR="${HOLDING_ROOT}/logs"
LOG_FILE="${LOG_DIR}/weekly-${WEEK_OF}.log"
mkdir -p "$LOG_DIR"

DRY_RUN=false
SKIP_TOOLS=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)    DRY_RUN=true; shift ;;
        --skip-tools) SKIP_TOOLS=true; shift ;;
        *) echo "Unknown arg: $1" >&2; exit 1 ;;
    esac
done

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$LOG_FILE"
}

fail() {
    log "FAIL: $*"
    exit "${2:-1}"
}

# ============================================================
# STEP 0 — PRE-FLIGHT
# ============================================================
log "=== WEEKLY BRIEF START — week of ${WEEK_OF} ==="
cd "$HOLDING_ROOT" || fail "cannot cd to $HOLDING_ROOT" 1

# Verify on main
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
[[ "$BRANCH" == "main" ]] || fail "expected main branch, got: $BRANCH" 1

# Verify clean tree
if ! git diff --quiet || ! git diff --cached --quiet; then
    fail "working tree dirty — commit or stash first" 1
fi

log "pre-flight OK (branch=$BRANCH, week=$WEEK_OF, dry_run=$DRY_RUN)"

# ============================================================
# STEP 1 — RUN CRYPTO TOOLS
# ============================================================
if [[ "$SKIP_TOOLS" == "true" ]]; then
    log "[1/6] tools: SKIPPED (--skip-tools)"
else
    log "[1/6] tools: running fear_greed.py, btc_price.py, funding_rates.py, onchain_metrics.py, news_scraper.py, pattern_detector.py"
    TOOLS_OUT="${LOG_DIR}/tools-${WEEK_OF}.json"

    # Each tool is independent; aggregate output to JSON for research stage
    {
        echo "{"
        echo "  \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\","
        echo "  \"week_of\": \"${WEEK_OF}\","
        echo "  \"tools\": {"

        for tool in fear_greed btc_price funding_rates onchain_metrics news_scraper pattern_detector; do
            tool_path="tools/${tool}.py"
            if [[ -f "$tool_path" ]]; then
                output=$(python3 "$tool_path" --json 2>>"$LOG_FILE" || echo '{"error":"tool failed"}')
                echo "    \"${tool}\": ${output},"
            else
                log "WARN: $tool_path not found"
            fi
        done | sed '$s/,$//'  # remove trailing comma

        echo "  }"
        echo "}"
    } > "$TOOLS_OUT" 2>>"$LOG_FILE"

    log "[1/6] tools: output saved to $TOOLS_OUT"
fi

# ============================================================
# STEP 2 — RESEARCH SYNTHESIS (via @crypto.research)
# ============================================================
log "[2/6] research: producing weekly synthesis (6-layer + 3-Lens)"

RESEARCH_OUT="${HOLDING_ROOT}/companies/crypto-consultant/tasks/weekly-${WEEK_OF}.md"

# Use llm_client.py with research synthesis prompt
RESEARCH_PROMPT="$(cat <<'EOF'
Generate weekly crypto market synthesis using 6-layer format (FACT, SOURCE, TREND, INTERPRET, SCENARIO, RISK NOTE).
Apply 3-Lens Convergence Test (Price/TA, On-chain, Derivatives).
Bear case FIRST in scenarios.
Include Forecast Ledger entry with decay window.
Include [BRANDFLOW HANDOFF] and [NEXUSAI HANDOFF] blocks at end.
Source: tools output below. Refer to knowledge/crypto/crypto-research-framework.md.
EOF
)"

if [[ "$DRY_RUN" == "true" ]]; then
    log "[2/6] research: DRY-RUN — using template stub"
    cat > "$RESEARCH_OUT" <<EOF
# Weekly Crypto Brief — Week of ${WEEK_OF}

[DRY-RUN STUB] Real research would be generated here via llm_client.py.

## Status
- Tools data: $([ -f "${LOG_DIR}/tools-${WEEK_OF}.json" ] && echo "available" || echo "missing")
- Pipeline: dry-run mode

## Disclaimer
DRY-RUN. Not for production use.
EOF
else
    # Real call (requires ANTHROPIC_API_KEY or fallback)
    if [[ -f "tools/llm_client.py" ]] && [[ -n "${ANTHROPIC_API_KEY:-${GROQ_API_KEY:-${OPENAI_API_KEY:-}}}" ]]; then
        TOOLS_DATA="$(cat "${LOG_DIR}/tools-${WEEK_OF}.json" 2>/dev/null || echo '{}')"
        PROVIDER="${LLM_PROVIDER:-anthropic}"

        python3 tools/llm_client.py \
            --provider "$PROVIDER" \
            --system "You are @crypto.research. Output 6-layer crypto research." \
            --message "$(echo "$RESEARCH_PROMPT"; echo; echo "Tools data:"; echo "$TOOLS_DATA")" \
            > "$RESEARCH_OUT" 2>>"$LOG_FILE" \
            || fail "LLM research call failed" 3
    else
        log "[2/6] research: SKIP (no API key set, no llm_client.py)"
        fail "no LLM provider configured" 3
    fi
fi

log "[2/6] research: saved to $RESEARCH_OUT"

# ============================================================
# STEP 3 — HANDOFF TO BRANDFLOW
# ============================================================
log "[3/6] handoff: routing research → BrandFlow"

# Log task to BrandFlow inbox
if [[ -f "bin/log_task.py" ]]; then
    python3 bin/log_task.py \
        --company brandflow \
        --to "@brandflow.copywriter" \
        --task "Weekly crypto brief: translate ${RESEARCH_OUT} to Twitter thread + IG carousel" \
        --from "system" \
        --priority "HIGH" \
        --context "{\"source_handoff\":\"FL-${WEEK_OF}\",\"source_report\":\"${RESEARCH_OUT}\"}" \
        2>>"$LOG_FILE" || fail "log_task to brandflow failed" 4
fi

log "[3/6] handoff: BrandFlow notified"

# ============================================================
# STEP 4 — BRANDFLOW DRAFT (currently manual — Hermes will pick up from inbox)
# ============================================================
log "[4/6] brandflow: draft pending — Hermes/agent picks up from inbox.jsonl"
# In production: poll for completion or require Hermes to finish before proceeding
# For now: assume drafts will be ready by step 5 cutoff

# ============================================================
# STEP 5 — CROSS-COMPANY QA
# ============================================================
log "[5/6] cross-qa: routing @crypto.qa to verify BrandFlow draft accuracy"

if [[ -f "bin/log_task.py" ]]; then
    python3 bin/log_task.py \
        --company crypto-consultant \
        --to "@crypto.qa" \
        --task "Cross-QA: verify factual accuracy of BrandFlow weekly content from FL-${WEEK_OF}" \
        --from "system" \
        --priority "HIGH" \
        --context "{\"checklist\":\"factual-accuracy\",\"source_report\":\"${RESEARCH_OUT}\"}" \
        2>>"$LOG_FILE" || log "WARN: cross-QA log failed (non-blocking)"
fi

log "[5/6] cross-qa: routing complete"

# ============================================================
# STEP 6 — APPROVAL REQUEST (Telegram)
# ============================================================
log "[6/6] approval: sending request to Fathur via Telegram"

APPROVAL_MSG=$(cat <<EOF
🔒 APPROVAL REQUEST

Type:       content-publish (weekly batch)
From:       Weekly cadence orchestrator
Priority:   routine
Week of:    ${WEEK_OF}

SUMMARY:
Weekly crypto brief siap untuk publish.
Research: ${RESEARCH_OUT}
Pending: Twitter thread + IG carousel (BrandFlow drafts)

Reply:
✅ "yes"      — approve all, schedule publish
✏️ "revise"   — kembalikan dengan feedback
❌ "no"       — cancel batch
⏸️ "hold"     — tahan sampai response berikutnya
EOF
)

if [[ "$DRY_RUN" == "true" ]]; then
    log "[6/6] approval: DRY-RUN — would send Telegram message:"
    echo "---" >> "$LOG_FILE"
    echo "$APPROVAL_MSG" >> "$LOG_FILE"
    echo "---" >> "$LOG_FILE"
elif [[ -f "bin/send_approval.py" ]] && [[ -n "${TELEGRAM_BOT_TOKEN:-}" ]] && [[ -n "${TELEGRAM_CHAT_ID:-}" ]]; then
    python3 bin/send_approval.py \
        --type "content-publish" \
        --priority "routine" \
        --message "$APPROVAL_MSG" \
        2>>"$LOG_FILE" || fail "Telegram approval send failed" 5
else
    log "[6/6] approval: SKIP (no Telegram config)"
    log "MANUAL: kirim approval request ke Fathur via channel lain"
    echo "$APPROVAL_MSG" | tee -a "$LOG_FILE"
fi

# ============================================================
# DONE
# ============================================================
log "=== WEEKLY BRIEF COMPLETE — week of ${WEEK_OF} ==="
log "Status: awaiting Fathur approval (Tier 3)"
log "Log saved: $LOG_FILE"

exit 0
