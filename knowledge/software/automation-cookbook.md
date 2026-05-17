# Automation Cookbook — Runnable Templates

Versi: 1.0
Created: 2026-05-17
Owner: NexusAI (`@nexusai.automation` patterns)
Source: Adapted from SUPERAGENT v2 m4.md

---

## Purpose

Production-ready automation templates yang **paste-and-run**. Cocok untuk:
- Tier 1 autonomous execution layer (Hermes weekly cadence triggers)
- Telegram bot untuk approval workflow (`approval-workflow.md`)
- Webhook receivers untuk cross-company event routing
- Cron schedules untuk weekly cadence (`weekly-cadence.md`)

---

## Templates Tersedia

| Template | File | Use Case |
|----------|------|----------|
| Telegram Bot | `tools/templates/telegram_bot.js` | Approval flow, /status, /run commands |
| Cron Patterns | `tools/templates/cron_examples.txt` | Weekly cadence triggers, daily schedules |
| FastAPI Webhook | `tools/templates/fastapi_webhook.py` | Event-driven triggers, GitHub webhooks |

---

## Pattern A: Telegram Approval Bot

Mapping ke `approval-workflow.md`:
1. Hermes generate APPROVAL REQUEST
2. Bot kirim ke Fathur via Telegram
3. Fathur reply yes/no/revise
4. Bot capture response, return ke Hermes via shared file/state

Setup minimum:
```bash
npm install node-telegram-bot-api dotenv
echo "TOKEN=<from-botfather>" > .env
node tools/templates/telegram_bot.js
```

Production:
```bash
pm2 start tools/templates/telegram_bot.js --name approval-bot
pm2 save
```

---

## Pattern B: Weekly Cadence via Cron

Per `knowledge/sop/weekly-cadence.md`, schedule ini di server Hermes:

```bash
# crontab -e (server in UTC)

# Monday 07:00 WIB = 00:00 UTC — weekly crypto brief production
0 0 * * 1 /opt/ai-holding/bin/run_weekly_brief.sh >> /var/log/weekly.log 2>&1

# Friday 09:00 WIB = 02:00 UTC — weekly recap
0 2 * * 5 /opt/ai-holding/bin/run_weekly_recap.sh >> /var/log/recap.log 2>&1

# Daily 07:00 WIB — crypto tools refresh
0 0 * * * /opt/ai-holding/bin/run_crypto_tools.sh >> /var/log/tools.log 2>&1
```

---

## Pattern C: Webhook Receiver for Cross-Company Events

FastAPI receiver untuk handle:
- GitHub webhook (PR merged → trigger update on Hermes)
- External API callbacks
- Inter-company event triggers

Setup:
```bash
pip install fastapi uvicorn
uvicorn tools.templates.fastapi_webhook:app --host 0.0.0.0 --port 8000
```

Production:
```bash
pm2 start "uvicorn tools.templates.fastapi_webhook:app --host 0.0.0.0 --port 8000" \
  --name webhook-receiver
```

Reverse proxy via Nginx → Lihat `knowledge/software/devops-cookbook.md`.

---

## Distribution Pipeline Pattern

Untuk weekly content yang ada di BrandFlow:

```
QUEUE (BrandFlow tasks/inbox.jsonl)
   ↓
SCHEDULER (cron + queue worker)
   ↓
DELIVERY_LAYER (Telegram → Fathur approval → publish)
   ↓
CONFIRMATION + LOG (memory/global.md + tasks/logs.jsonl)
   ↑
GENERATOR (Crypto Consultant research → BrandFlow translation)
```

---

## Constraints

- Selalu pakai `.env` untuk secrets (jangan hardcode)
- Production deploy = Tier 3 (Fathur approval)
- Validate user authorization sebelum eksekusi command via bot
- Log semua trigger ke `tasks/logs.jsonl` per task-logger-rules
- Webhook receivers WAJIB signature verification (lihat fastapi_webhook.py optional secret)

---

## Reference

- Source: `update/v2/openclaw/skills/m4.md`
- Templates: `tools/templates/`
- DevOps: `knowledge/software/devops-cookbook.md`
- Approval: `knowledge/sop/approval-workflow.md`
- Cadence: `knowledge/sop/weekly-cadence.md`
