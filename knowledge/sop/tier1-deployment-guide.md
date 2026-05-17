# Tier 1 Autonomous Execution — Deployment Guide

Versi: 1.0
Created: 2026-05-17
Owner: Operator + NexusAI DevOps
Scope: Cara deploy + verify orchestrator + cron + Telegram bot di mesin Hermes

---

## Apa Yang Dibangun di PR Ini

| File | Fungsi |
|------|--------|
| `bin/run_weekly_brief.sh` | ⭐ Master orchestrator — chain tools→research→handoff→QA→approval |
| `bin/run_weekly_recap.sh` | Friday recap + system audit |
| `bin/run_crypto_tools.sh` | Daily refresh fear_greed/btc/onchain/funding/news/pattern |
| `bin/run_midweek_check.sh` | Wednesday material-change detector |
| `bin/check_pending_approvals.py` | Timeout reminder scanner (cron 2h) |
| `bin/send_approval.py` | Telegram sender untuk APPROVAL REQUEST |
| `bin/handle_approval_response.py` | Parse Fathur reply → trigger downstream |
| `bin/get_chat_id.py` | One-time helper: discover Telegram chat_id |
| `bin/install_cron.sh` | Idempotent cron installer (with `--show` and `--uninstall`) |

---

## 5-Minute Setup di Hermes

### 1. Pull terbaru

```bash
cd /home/fatur/ai-holding && git pull origin main
```

### 2. Setup Telegram bot (one-time)

```bash
# Step 1: Buat bot via @BotFather di Telegram
#   /newbot → ikuti prompts → simpan token

# Step 2: Set token sementara
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."

# Step 3: Kirim 1 message ke bot dari Telegram pribadi kamu

# Step 4: Discover chat_id
python3 bin/get_chat_id.py
# Output: chat_id=987654321 type=private name='Fathur'

# Step 5: Set chat_id permanent
echo 'export TELEGRAM_BOT_TOKEN="123456:ABC..."' >> ~/.bashrc
echo 'export TELEGRAM_CHAT_ID="987654321"' >> ~/.bashrc
echo 'export HOLDING_ROOT="/home/fatur/ai-holding"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Setup LLM API key (minimum 1)

Pilih SATU provider gratis dulu untuk test:

```bash
# Option A: Groq (gratis, cepat, recommended untuk testing)
echo 'export GROQ_API_KEY="gsk_..."' >> ~/.bashrc

# Option B: Anthropic (paling akurat, berbayar)
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc

# Set default LLM provider
echo 'export LLM_PROVIDER="groq"' >> ~/.bashrc

source ~/.bashrc
```

### 4. Smoke test (no Telegram, no LLM commitment)

```bash
# Test 1: tools refresh (akan jalan tools yang ada)
bash bin/run_crypto_tools.sh
ls logs/crypto-tools-*.log

# Test 2: weekly brief dry-run (no Telegram, no LLM call)
bash bin/run_weekly_brief.sh --dry-run --skip-tools
cat logs/weekly-*.log

# Test 3: Telegram send (kirim test message)
python3 bin/send_approval.py \
    --type other --priority routine \
    --message "🧪 Test message from autonomous system" \
    --from "system"
# Cek Telegram — harus ada message masuk
```

### 5. Install cron schedule

```bash
# Preview saja dulu (lihat current crontab):
bin/install_cron.sh --show

# Install:
bin/install_cron.sh

# Verifikasi:
crontab -l | grep -A 20 "AI HOLDING"
```

Cron jobs yang terinstall:
```
0 0 * * *     daily   crypto tools refresh (07:00 WIB)
0 0 * * 1     Mon     weekly crypto brief production (07:00 WIB)
0 0 * * 3     Wed     mid-week material change check
0 2 * * 5     Fri     weekly recap + system audit (09:00 WIB)
0 23,1,3,5,7,9,11,13,15 * * *  every 2h  approval timeout reminders
```

### 6. Kirim test approval (full flow)

```bash
python3 bin/send_approval.py \
    --type "content-publish" \
    --priority "time-sensitive" \
    --message "🧪 Test approval flow.\n\nReply 'yes', 'no', atau 'revise: <feedback>'" \
    --from "system" \
    --ref "TEST-001"
```

Reply di Telegram. Lalu test parser:

```bash
python3 bin/handle_approval_response.py --ref TEST-001 --reply "yes"
```

Output harus: `OK: ref=TEST-001 status=approved`

---

## Verifikasi Health

### Cek crontab

```bash
crontab -l | grep "AI HOLDING" -A 20
```

### Cek logs

```bash
ls -la logs/
tail -50 logs/cron.log
```

### Cek approval audit trail

```bash
cat memory/approvals.jsonl | tail -5
```

### Test pending approvals scanner

```bash
python3 bin/check_pending_approvals.py --dry-run
```

---

## Operational Modes

### Mode Manual (kamu jalankan sendiri)

```bash
# Setiap Senin kamu jalanin manually:
bash bin/run_weekly_brief.sh

# Setiap Jumat:
bash bin/run_weekly_recap.sh
```

### Mode Cron (autonomous)

Setelah `bin/install_cron.sh` jalan, semua otomatis. Kamu cuma:
- Senin sore: cek Telegram, reply approval (5 min)
- Jumat sore: baca recap (3 min, optional)

### Mode Hybrid

Bisa kombinasi: cron jalan, tapi pause via:

```bash
bin/install_cron.sh --uninstall
```

Re-enable kapan saja:
```bash
bin/install_cron.sh
```

---

## Troubleshooting

### Telegram message tidak sampai

1. Cek bot token: `echo $TELEGRAM_BOT_TOKEN`
2. Cek chat_id: `echo $TELEGRAM_CHAT_ID`
3. Test API: `curl "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe"`
4. Cek `memory/approvals.jsonl` untuk error message

### LLM call gagal di run_weekly_brief.sh

1. Cek API key: `python3 tools/llm_client.py --provider groq --message ping`
2. Cek `logs/weekly-*.log` untuk error spesifik
3. Set default provider: `export LLM_PROVIDER=groq`

### Cron tidak jalan

1. `systemctl status cron` (atau `crond` di RHEL/CentOS)
2. Test manual: `bash -x bin/run_crypto_tools.sh` lihat error
3. Cek timezone: cron pakai UTC, weekly-cadence pakai WIB

### Pending approval menumpuk

```bash
python3 bin/check_pending_approvals.py --dry-run
```

Output: lihat ref mana yang stuck. Manual mark:

```bash
python3 bin/handle_approval_response.py --ref FL-XXX --reply "no"
```

---

## Boundary #4 Reminder

- Tier 1 (autonomous): crypto tools refresh, research synthesis, BrandFlow draft generation, internal QA, task logging
- Tier 3 (Fathur required): publish ke public surface, deploy production, new client, budget

Tier 1 cron jobs **tidak akan publish apapun** tanpa Fathur reply "yes" lewat Telegram.

---

## Reference

- `knowledge/sop/weekly-cadence.md` — kapan apa jalan
- `knowledge/sop/approval-workflow.md` — bagaimana approval flow
- `knowledge/sop/autonomous-boundaries.md` — Tier 1/2/3
- `tools/templates/telegram_bot.js` — bot interaktif (advanced, optional)
- `tools/templates/fastapi_webhook.py` — webhook receiver (advanced, optional)
