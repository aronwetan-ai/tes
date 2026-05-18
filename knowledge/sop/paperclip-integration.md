# Paperclip Integration — Full Org Setup

Versi: 1.0
Created: 2026-05-18
Owner: Main Assistant (Drayco/Rei) + Operator
Source: https://paperclip.ing | https://github.com/paperclipai/paperclip | https://github.com/NousResearch/hermes-paperclip-adapter

---

## Overview

Paperclip = control plane untuk AI agents. Org chart, budget, heartbeat scheduling, delegation flow, audit log.

**Scope:** Full org — map 3 companies + hierarchy ke Paperclip
**Budget:** Token per hari (tracked via RTK + LLM call logs)
**Heartbeat:** 1 jam

---

## Architecture

```
Paperclip (control plane)
├── Company: AI Holding
│   ├── CEO: Drayco/Rei (Hermes Main Assistant)
│   │   ├── Employee: @nexusai (NexusAI CTO)
│   │   │   └── Sub-employees: 10 agents
│   │   ├── Employee: @brandflow (BrandFlow CMO)
│   │   │   └── Sub-employees: 11 agents
│   │   └── Employee: @crypto (Crypto Consultant CEO)
│   │       └── Sub-employees: 11 agents
│   │
│   ├── Budget: token/day tracking
│   ├── Heartbeat: every 1 hour
│   └── Governance: Fathur = Board Member (approval for Tier 3)
```

**Key principle:** Paperclip manages scheduling + budget + delegation.
Hermes manages internal routing (pseudo-mentions, SOUL hierarchy, tools).
They coexist, not replace each other.

---

## Prerequisites

```bash
# Node.js 20+ (check)
node --version  # v20+

# pnpm 9.15+ (install if missing)
npm install -g pnpm
pnpm --version  # 9.15+

# Hermes running (existing)
hermes --version
```

---

## Step 1: Install Paperclip

```bash
# Onboard (fastest path — sets up everything)
npx paperclipai onboard --yes

# Atau manual install
pnpm create paperclip@latest

# Verify
npx paperclipai --version
```

Paperclip installs to `~/.paperclip/` by default.

---

## Step 2: Create Company — AI Holding

```bash
# Create company
npx paperclipai company create "AI Holding" \
  --description "Fathur's AI workforce — IT, Marketing, Crypto Research" \
  --goal "Operate 3 companies (NexusAI, BrandFlow, Crypto Consultant) with 32 agents"
```

Atau via config file `~/.paperclip/companies/ai-holding/company.yaml`:

```yaml
name: AI Holding
description: "Fathur's AI workforce — IT, Marketing, Crypto Research"
goal: "Operate 3 companies (NexusAI, BrandFlow, Crypto Consultant) with 32 agents autonomously"
board_members:
  - name: Fathur
    role: owner
    approval_required_for:
      - budget_increase
      - new_employee_hire
      - tier_3_actions
governance:
  approval_mode: async  # Fathur approve via Telegram/Discord
  budget_period: daily
  audit_frequency: weekly
```

---

## Step 3: Add Hermes as CEO Employee

```bash
# Install Hermes-Paperclip adapter
npm install -g hermes-paperclip-adapter
# Atau:
npx paperclipai add-employee hermes \
  --role ceo \
  --adapter hermes-paperclip-adapter \
  --budget-daily 500000  # 500k tokens/day
```

Adapter config `~/.paperclip/companies/ai-holding/employees/rei/employee.yaml`:

```yaml
name: Drayco (Rei)
role: ceo
adapter: hermes-paperclip-adapter
description: "Gen Z Main Assistant — routes, manages memory, coordinates all companies"
budget:
  daily_limit: 500000  # tokens
  alert_threshold: 0.8  # alert at 80% usage
  hard_stop: false      # don't kill mid-task, just warn
heartbeat:
  interval: 3600        # 1 hour (seconds)
  on_wake:
    - check_inbox       # cek tasks/inbox.jsonl
    - check_messages    # cek tasks/messages.jsonl
    - run_recap         # daily recap kalau waktunya
    - check_monitoring  # monitoring dashboard
standing_orders:
  - "Route incoming tasks to correct company/agent"
  - "Update memory when strategic decisions made"
  - "Run system audit every Friday"
  - "Offer skill capture after complex workflows"
tools:
  inherit_from: hermes  # semua Hermes tools available
permissions:
  tier_1: autonomous    # per autonomy-tiers.md
  tier_2: autonomous_log
  tier_3: require_approval
reports_to: Fathur
```

---

## Step 4: Add Company Employees (3 CEOs)

### NexusAI CTO

```yaml
# ~/.paperclip/companies/ai-holding/employees/nexusai-cto/employee.yaml
name: NexusAI CTO
role: cto
adapter: hermes-paperclip-adapter
description: "IT Software — cloud, DevOps, AI agents, SaaS"
budget:
  daily_limit: 200000  # tokens
  alert_threshold: 0.8
heartbeat:
  interval: 3600
  on_wake:
    - check_inbox
    - check_build_status
    - run_dep_audit
standing_orders:
  - "Review and assign incoming engineering tasks"
  - "Monitor API health for active projects"
  - "Run dependency audit weekly"
reports_to: rei
manages:
  - "@nexusai.devops"
  - "@nexusai.backend"
  - "@nexusai.frontend"
  - "@nexusai.ml"
  - "@nexusai.security"
  - "@nexusai.qa"
  - "@nexusai.writer"
  - "@nexusai.pm"
  - "@nexusai.uiux"
```

### BrandFlow CMO

```yaml
# ~/.paperclip/companies/ai-holding/employees/brandflow-cmo/employee.yaml
name: BrandFlow CMO
role: cmo
adapter: hermes-paperclip-adapter
description: "Marketing & Content — branding, social media, campaigns"
budget:
  daily_limit: 150000  # tokens (content gen is token-heavy)
  alert_threshold: 0.8
heartbeat:
  interval: 3600
  on_wake:
    - check_inbox
    - check_content_calendar
    - monitor_social_metrics
standing_orders:
  - "Review content pipeline and assign to writers/designers"
  - "Monitor social engagement metrics"
  - "Ensure brand voice consistency across platforms"
reports_to: rei
manages:
  - "@brandflow.copywriter"
  - "@brandflow.designer"
  - "@brandflow.social"
  - "@brandflow.community"
  - "@brandflow.seo"
  - "@brandflow.analytics"
  - "@brandflow.writer"
  - "@brandflow.qa"
  - "@brandflow.pm"
```

### Crypto Consultant CEO

```yaml
# ~/.paperclip/companies/ai-holding/employees/crypto-ceo/employee.yaml
name: Crypto Consultant CEO
role: ceo_subsidiary
adapter: hermes-paperclip-adapter
description: "Crypto Research — market analysis, cycle analysis, risk assessment"
budget:
  daily_limit: 150000  # tokens
  alert_threshold: 0.8
heartbeat:
  interval: 3600
  on_wake:
    - check_inbox
    - run_market_scan
    - check_fear_greed
    - check_funding_rates
standing_orders:
  - "Daily market scan at heartbeat"
  - "Route research requests to specialist agents"
  - "Maintain Forecast Ledger accuracy"
  - "Flag high-conviction signals to Fathur"
reports_to: rei
manages:
  - "@crypto.research"
  - "@crypto.market"
  - "@crypto.onchain"
  - "@crypto.macro"
  - "@crypto.risk"
  - "@crypto.report"
  - "@crypto.writer"
  - "@crypto.data"
  - "@crypto.qa"
  - "@crypto.pm"
```

---

## Step 5: Configure Heartbeat

### Hermes config.yaml addition

```yaml
# ~/.hermes/config.yaml (tambahkan section ini)
paperclip:
  enabled: true
  company: ai-holding
  employee: rei
  heartbeat_interval: 3600  # 1 hour
  budget_tracking: true
  budget_metric: tokens      # track token usage
  adapter_path: ~/.paperclip/companies/ai-holding/employees/rei/
```

### Heartbeat flow (setiap 1 jam)

```
Paperclip sends heartbeat signal
    ↓
Hermes adapter receives wake-up
    ↓
Rei executes on_wake tasks:
  1. Check inbox.jsonl (all companies)
  2. Check messages.jsonl (agent-to-agent)
  3. Run recap if scheduled
  4. Check monitoring alerts
    ↓
Rei delegates tasks to company employees
    ↓
Results logged to Paperclip audit trail
    ↓
Budget usage updated
    ↓
Sleep until next heartbeat (1 hour)
```

---

## Step 6: Budget Tracking Integration

### Token tracking hook (add ke Hermes)

Buat `bin/track_tokens.py`:

```python
#!/usr/bin/env python3
"""Track token usage per heartbeat cycle for Paperclip budget."""
import json
import os
from datetime import datetime, timezone

BUDGET_LOG = os.path.expanduser("~/.paperclip/companies/ai-holding/budget-log.jsonl")

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
```

### RTK savings → budget offset

```bash
# RTK savings reduce effective budget usage
# Actual tokens = raw_tokens - rtk_savings
# Track via: rtk gain --json | jq '.total_saved'
```

---

## Step 7: Start Paperclip

```bash
# Start Paperclip daemon (background)
npx paperclipai start --company ai-holding

# Verify running
npx paperclipai status

# Dashboard (web UI)
npx paperclipai dashboard
# → Opens http://localhost:4040

# Start Hermes gateway (integrates with Paperclip via adapter)
hermes gateway
```

### PM2 for persistent running

```bash
# Paperclip
pm2 start "npx paperclipai start --company ai-holding" --name paperclip

# Hermes gateway (already running, just verify)
pm2 status

# Save
pm2 save
pm2 startup
```

---

## Step 8: Verify Integration

```bash
# 1. Check Paperclip sees all employees
npx paperclipai employees list

# 2. Check heartbeat is ticking
npx paperclipai heartbeat status

# 3. Check budget tracking
npx paperclipai budget status --employee rei

# 4. Manual heartbeat trigger (test)
npx paperclipai heartbeat trigger --employee rei

# 5. Check Hermes received the heartbeat
# → Should see Rei execute on_wake tasks in hermes logs
hermes logs --last 10
```

---

## Delegation Flow (Full Org)

```
Fathur kirim task via Telegram
    ↓
Hermes (Rei) receives → identifies company
    ↓
Rei delegates via Paperclip ticketing:
  npx paperclipai task create \
    --assignee nexusai-cto \
    --title "Deploy API v2" \
    --priority high
    ↓
Paperclip routes ticket to NexusAI CTO
    ↓
NexusAI CTO (on next heartbeat) picks up task
    ↓
CTO delegates to @nexusai.devops (internal routing via Hermes)
    ↓
Result flows back up:
  @nexusai.devops → CTO → Rei → Fathur (Telegram notification)
```

---

## Budget Alerts

```yaml
# When employee hits 80% daily budget:
# Paperclip sends alert to Rei
# Rei forwards to Fathur:
#   "⚠️ @nexusai budget 80% — 160k/200k tokens used. Throttle or increase?"

# When 100% hit:
# Agent stops non-essential work (heartbeat still runs)
# Only critical/escalated tasks proceed
# Fathur can override: "increase budget" or "continue anyway"
```

---

## Mapping ke Existing System

| Existing (Hermes) | Paperclip Equivalent | Who Manages |
|---|---|---|
| `@company` pseudo-mention | Employee in org chart | Paperclip |
| `tasks/inbox.jsonl` | Paperclip ticket queue | Both (sync) |
| `HEARTBEAT.md` checklist | Heartbeat on_wake | Paperclip triggers, Hermes executes |
| `MEMORY.md` decisions | Audit trail | Both (Paperclip logs, Hermes writes) |
| Risk tiers (Low/Med/High) | Governance approval flow | Paperclip enforces |
| Boundary #4 | Board approval required | Paperclip governance |

**Coexistence rule:** Paperclip adds scheduling + budget + governance layer ON TOP of existing system. Does NOT replace SOUL hierarchy, pseudo-mention routing, or internal agent logic.

---

## Credentials

```bash
# Paperclip credentials (kalau pakai cloud dashboard)
# Simpan di:
~/.agent/credentials/paperclip.env

# Template sudah dibuat di:
credentials/templates/paperclip.env.example
```

---

## Anti-Patterns

❌ Replace existing Hermes routing dengan Paperclip-only — mereka complement, bukan replace
❌ Set budget terlalu rendah — agent terhenti mid-task, worse outcome
❌ Heartbeat terlalu sering (<15 min) — token waste di wake-up overhead
❌ Skip governance for Tier 3 — Paperclip harus enforce Boundary #4
❌ Semua agent di level yang sama — tetap hierarchy (CEO → CTO/CMO → agents)

---

## Rollback Plan

Kalau Paperclip integration bermasalah:

```bash
# 1. Stop Paperclip
pm2 stop paperclip

# 2. Disable di Hermes config
# ~/.hermes/config.yaml:
# paperclip:
#   enabled: false

# 3. Hermes tetap jalan normal tanpa Paperclip
# Semua routing, memory, tools tetap berfungsi
# Hanya kehilangan: automated heartbeat + budget tracking + delegation ticketing
```

Existing system tetap jalan 100% tanpa Paperclip. Paperclip adalah **enhancement**, bukan dependency.

---

## Reference

- Paperclip docs: https://paperclipai-paperclip.mintlify.app/
- Paperclip GitHub: https://github.com/paperclipai/paperclip
- Hermes adapter: https://github.com/NousResearch/hermes-paperclip-adapter
- BetterStack guide: https://betterstack.com/community/guides/ai/paperclip-multi-agent/
- Heartbeat protocol: https://github.com/paperclipai/paperclip/blob/master/docs/guides/agent-developer/heartbeat-protocol.md
