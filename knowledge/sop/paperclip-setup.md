# Paperclip Setup — Fresh Install + Hermes Adapter

Versi: 2.0 (fresh rewrite — supersedes paperclip-integration.md + paperclip-rebuild.md)
Created: 2026-05-18
Owner: @nexusai.devops + Operator
Status: READY (tested-path)
Sources verified:
- https://github.com/paperclipai/paperclip (README, master branch)
- https://github.com/NousResearch/hermes-paperclip-adapter (README)
- https://paperclipai-paperclip.mintlify.app/ (official docs)
- https://github.com/paperclipai/paperclip/blob/master/docs/adapters/creating-an-adapter.md

---

## What This SOP Does

Setup Paperclip server + register `hermes_local` adapter dari nol, lalu create company "AI Holding" dengan Rei (Drayco) sebagai CEO. Identity sudah disetup separately via `bin/install-rei-persona.sh` — file ini fokus purely di Paperclip.

**Outcome:** Paperclip jalan di `http://localhost:3100`, Rei bisa wake on heartbeat, full org chart bisa di-expand setelah Rei stable.

---

## Architecture (Verified)

```
Paperclip Server (localhost:3100, Node + React)
├── Identity & Access (board users, agent API keys, JWT)
├── Org Chart & Agents (roles, reporting lines, budgets)
├── Work & Issues (atomic checkout, comments, documents)
├── Heartbeat Execution (DB-backed wakeup queue)
├── Governance & Approvals (review/approval gates)
├── Budget & Cost Control (token + cost tracking, hard stops)
├── Routines (cron, webhook, API triggers)
└── Adapters (Claude Code, Codex, hermes_local, custom)
       │
       └─► hermes_local (NousResearch/hermes-paperclip-adapter v0.3.x)
              │
              └─► spawns `hermes chat -q` per heartbeat
                     │
                     └─► Hermes runtime (~/.hermes/) + 30+ tools + skills
```

**Key principle:** Paperclip = control plane (scheduling, governance, budget). Hermes = execution. Mereka coexist, bukan replace.

---

## Prerequisites

```bash
# Required
node --version          # ≥ v20
pnpm --version          # ≥ 9.15  (install: npm i -g pnpm)
hermes --version        # Hermes Agent CLI installed (pip install hermes-agent)
python3 --version       # ≥ 3.10 (untuk Hermes)

# Optional tapi recommended
pm2 --version           # untuk persistent running di production
```

**Identity prerequisite:** `bin/install-rei-persona.sh --apply` udah dijalankan, persona Drayco/Rei udah aktif di Hermes config (`~/.hermes/config.yaml` + `~/.hermes/SOUL.md`). Verify: kirim "siapa lo" ke Telegram, harus jawab "Gue Drayco".

---

## Step 0: Cleanup Sisa Install Lama (KALAU ADA)

Kalau lo sebelumnya pernah coba install Paperclip dan ada sisa state yang corrupt/broken, run cleanup script dulu:

```bash
cd ~/ai-holding

# Preview dulu (lihat apa yang akan dihapus)
bash bin/paperclip-cleanup.sh --dry-run

# Apply cleanup (interactive — minta konfirmasi)
bash bin/paperclip-cleanup.sh

# Atau auto-apply (untuk scripted runs)
bash bin/paperclip-cleanup.sh --apply
```

**Yang dibersihin:**
- PM2 paperclip processes
- Running paperclip / pnpm dev processes (port 3100 freed)
- `~/.paperclip/` (data dir) — backed up dulu ke `~/.paperclip-cleanup-backup-<timestamp>/`
- `~/paperclip-src/` (source clone) — backed up dulu (tanpa `node_modules`)
- Global npm packages (`paperclipai`, `hermes-paperclip-adapter`)
- pnpm store cache untuk paperclip packages
- `paperclip:` section di `~/.hermes/config.yaml` (commented out)

**Yang TIDAK dibersihin (penting!):**
- `~/.hermes/` — Hermes runtime, persona Drayco/Rei live di sini
- `~/ai-holding/` — repo workspace
- `~/.agent/credentials/` — credentials lo
- System binaries (Node, pnpm, pm2)

**Skip Step 0 kalau:** lo belum pernah install Paperclip sama sekali (fresh machine). Lanjut ke Step 1.

**Verify Hermes masih jalan setelah cleanup:**
```bash
systemctl --user restart hermes-gateway
# Test di Telegram: kirim "siapa lo?" — expected "Gue Drayco — bisa lo panggil Rei..."
```

Kalau Hermes broken setelah cleanup, restore config:
```bash
ls ~/.hermes/config.yaml.pre-paperclip-cleanup-* 2>/dev/null
# Copy backup yang paling baru kembali ke ~/.hermes/config.yaml
```

---

## Setup Strategy: Fork-and-Register (Recommended)

`hermes-paperclip-adapter` adalah **external adapter plugin** — dua opsi register:

| Opsi | Cara | Effort | Rekomendasi |
|------|------|--------|-------------|
| **A. Built-in (fork Paperclip)** | Edit `server/src/adapters/registry.ts`, build sendiri | ~30 min | ✅ **Pakai ini** — stable, full control |
| **B. External plugin loader** | Auto-load via plugin convention | ~10 min | ⚠️ Plugin loader masih maturing, bisa break |

SOP ini pakai **Opsi A** karena lebih predictable dan persona Drayco/Rei ke-bind solid.

---

## Step 1: Clone Paperclip Source

```bash
cd ~
git clone https://github.com/paperclipai/paperclip.git paperclip-src
cd paperclip-src

# Pastikan dapat versi stable terbaru (cek releases)
git tag | tail -5
# Kalau mau pin ke specific tag:
# git checkout v0.X.X

pnpm install
```

**Expected:** Install sukses, no errors. Kalau ada peer-dependency warning, OK.

---

## Step 2: Install hermes-paperclip-adapter sebagai Server Dependency

```bash
cd ~/paperclip-src
pnpm add hermes-paperclip-adapter --filter @paperclip/server
# Catatan: nama filter mungkin beda di versi terbaru — kalau gagal, coba:
# pnpm add hermes-paperclip-adapter --filter server
# atau langsung: cd server && pnpm add hermes-paperclip-adapter
```

**Verify** di `server/package.json`:

```json
{
  "dependencies": {
    "hermes-paperclip-adapter": "^0.3.0"
  }
}
```

---

## Step 3: Register Adapter di Server Registry

Edit `server/src/adapters/registry.ts`:

```bash
# Cari file
find ~/paperclip-src -name "registry.ts" -path "*/adapters/*"
# Expected output (3 files):
#   server/src/adapters/registry.ts   ← edit ini dulu (mandatory)
#   ui/src/adapters/registry.ts       ← edit ini juga (untuk tool cards di dashboard)
#   cli/src/adapters/registry.ts      ← optional (untuk pretty CLI output)
```

### 3a. Server registry (mandatory)

Tambahkan di bagian imports + registration:

```typescript
// === IMPORTS ===
import * as hermesLocal from "hermes-paperclip-adapter";
import {
  execute,
  testEnvironment,
  detectModel,
  listSkills,
  syncSkills,
  sessionCodec,
} from "hermes-paperclip-adapter/server";

// === REGISTRY (tambahkan setelah adapter built-in lain) ===
registry.set("hermes_local", {
  ...hermesLocal,
  execute,
  testEnvironment,
  detectModel,
  listSkills,
  syncSkills,
  sessionCodec,
});
```

### 3b. UI registry (recommended — supaya tool cards muncul rapi)

Edit `ui/src/adapters/registry.ts`:

```typescript
import { parseStdout } from "hermes-paperclip-adapter/ui-parser";

uiRegistry.set("hermes_local", {
  parseStdout,
});
```

### 3c. CLI registry (optional — pretty output untuk `paperclipai run --watch`)

Edit `cli/src/adapters/registry.ts`:

```typescript
import { formatStdoutEvent } from "hermes-paperclip-adapter/cli";

cliRegistry.set("hermes_local", {
  formatStdoutEvent,
});
```

**Skip 3b/3c kalau lo cuma butuh dapur jalan dulu.** Server registry aja cukup untuk heartbeat + execution. Dashboard akan tampil raw text tanpa formatted tool cards.

---

## Step 4: Build Paperclip

```bash
cd ~/paperclip-src
pnpm build

# Kalau ada TypeScript error:
pnpm typecheck
# Fix import paths dulu, build ulang
```

**Expected:** Build sukses. Kalau gagal di step ini, **STOP** — masalah type compatibility antara adapter version dan Paperclip version. Cek issue di GitHub adapter repo, atau pin adapter version yang compatible.

---

## Step 5: Start Paperclip Server

### Development mode (untuk first run)

```bash
cd ~/paperclip-src
pnpm dev
# API + UI di http://localhost:3100
# Embedded Postgres auto-spawn (no setup needed)
```

**Expected output:**
```
✓ Server listening on http://localhost:3100
✓ UI available at http://localhost:3100
✓ Database migrations applied
```

### Verify adapter registered

Di tab terpisah:

```bash
curl http://localhost:3100/api/adapters | python3 -m json.tool | grep hermes_local
# Expected: ada entry "hermes_local" di list
```

Kalau **tidak muncul** → balik ke Step 3, cek registry.ts udah di-save dan rebuild.

---

## Step 6: Initial Onboarding (Web UI)

Buka browser ke `http://localhost:3100`.

**Trusted local mode** (default untuk localhost) — nggak perlu password. Lo langsung masuk sebagai board user.

Kalau pertama kali, UI akan minta:
1. Name: `Fathur`
2. Bind preset: `loopback` (default — cuma localhost), atau `lan` / `tailnet` kalau mau akses dari device lain

---

## Step 7: Create Company "AI Holding"

### Via Web UI (recommended untuk first time)

1. Click **"+ New Company"**
2. Form:
   - **Name:** `AI Holding`
   - **Issue Prefix:** `AIH` (auto-generates `AIH-1`, `AIH-2`, dst)
   - **Monthly Budget (cents):** `500000` (= $5000/month, adjust sesuai mau)
3. Click Create

### Via API (alternative)

```bash
# Get instance admin API key dari UI: Settings → API Keys
export PAPERCLIP_API_KEY="your-instance-admin-key"

curl -X POST http://localhost:3100/api/companies \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Holding",
    "issuePrefix": "AIH",
    "budgetMonthlyCents": 500000
  }'
```

**Save the company ID** dari response — dipakai di step berikutnya.

---

## Step 8: Create Rei (Drayco) sebagai CEO Agent

### Via Web UI

1. Masuk ke company AI Holding
2. Click **"+ Add Agent"**
3. Form:
   - **Name:** `Rei`
   - **Title:** `Drayco — Main Assistant / CEO`
   - **Role:** `ceo`
   - **Adapter Type:** `hermes_local` ← harus muncul di dropdown setelah register di Step 3
   - **Adapter Config (JSON):**

```json
{
  "model": "anthropic/claude-sonnet-4",
  "timeoutSec": 300,
  "graceSec": 10,
  "persistSession": true,
  "quiet": true,
  "enabledToolsets": ["terminal", "file", "web", "browser", "mcp"]
}
```

   - **Monthly Budget (cents):** `200000` (= $2000/month untuk Rei sebagai router utama)
4. Click Create

### Via API

```bash
export COMPANY_ID="<from-step-7>"

curl -X POST "http://localhost:3100/api/companies/${COMPANY_ID}/agents" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rei",
    "title": "Drayco — Main Assistant / CEO",
    "role": "ceo",
    "capabilities": "Routing, memory management, workflow coordination across 3 companies (NexusAI, BrandFlow, Crypto Consultant). Gen Z persona, autonomous execution per Tier 1/2 boundaries.",
    "adapterType": "hermes_local",
    "adapterConfig": {
      "model": "anthropic/claude-sonnet-4",
      "timeoutSec": 300,
      "graceSec": 10,
      "persistSession": true,
      "quiet": true,
      "enabledToolsets": ["terminal", "file", "web", "browser", "mcp"]
    },
    "budgetMonthlyCents": 200000
  }'
```

Save the agent ID dari response.

---

## Step 9: Configure Heartbeat for Rei

### Via Web UI

Agent Rei → **Settings** → **Heartbeat**:
- Enabled: `true`
- Interval: `1 hour` (3600 seconds)
- Schedule: leave default (continuous wake-on-heartbeat)

### Via API

```bash
export AGENT_ID="<from-step-8>"

curl -X PATCH "http://localhost:3100/api/agents/${AGENT_ID}/heartbeat" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "intervalSeconds": 3600,
    "enabled": true
  }'
```

---

## Step 10: Test Heartbeat (Smoke Test)

### Manual wakeup trigger

```bash
curl -X POST "http://localhost:3100/api/agents/${AGENT_ID}/wakeup" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "source": "manual",
    "reason": "smoke_test",
    "triggerDetail": "first-run-verification"
  }'
```

**Expected response:**
```json
{
  "id": "run-uuid",
  "status": "queued"
}
```

### Watch the run

```bash
export RUN_ID="<from-wakeup-response>"

# Poll run status
curl "http://localhost:3100/api/heartbeat-runs/${RUN_ID}" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" | python3 -m json.tool

# Watch live events
curl "http://localhost:3100/api/heartbeat-runs/${RUN_ID}/events?afterSeq=0&limit=200" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" | python3 -m json.tool
```

**Expected:** Hermes CLI di-spawn (`hermes chat -q`), Rei process the wake reason, exit clean. Status berubah `queued → running → done`.

### Verify session persisted

```bash
ls ~/.hermes/sessions/ | head
# Should show new session file from Paperclip-triggered run
```

---

## Step 11: Production Setup (PM2 Persistent)

```bash
cd ~/paperclip-src

# Build production
pnpm build

# Start with PM2
pm2 start "pnpm start" --name paperclip --cwd ~/paperclip-src

# Verify running
pm2 status
pm2 logs paperclip --lines 50

# Save PM2 process list (auto-restart on reboot)
pm2 save
pm2 startup    # follow the printed command to enable systemd integration
```

---

## Step 12: Add Company Heads (After Rei Stable)

Setelah Rei jalan stable minimal 1-2 hari, expand ke 3 company heads.

```bash
# Template untuk NexusAI CTO
curl -X POST "http://localhost:3100/api/companies/${COMPANY_ID}/agents" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "NexusAI CTO",
    "title": "Engineering Lead",
    "role": "manager",
    "reportsTo": "'"$AGENT_ID"'",
    "capabilities": "Cloud, DevOps, AI agents, SaaS engineering. Manages 10 NexusAI agents.",
    "adapterType": "hermes_local",
    "adapterConfig": {
      "model": "anthropic/claude-sonnet-4",
      "timeoutSec": 300,
      "persistSession": true,
      "enabledToolsets": ["terminal", "file", "web", "code_execution"]
    },
    "budgetMonthlyCents": 100000
  }'
```

Repeat untuk:
- **BrandFlow CMO** (`role: manager`, budget 80k cents = $800/month — content gen heavy tapi shorter context)
- **Crypto CEO** (`role: manager`, budget 80k cents)

---

## Step 13: Verify Full Setup

```bash
# 1. List all agents
curl "http://localhost:3100/api/companies/${COMPANY_ID}/agents" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" | python3 -m json.tool

# 2. Get org chart
curl "http://localhost:3100/api/companies/${COMPANY_ID}/org" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" | python3 -m json.tool

# 3. Get org chart visual
curl "http://localhost:3100/api/companies/${COMPANY_ID}/org.svg" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" -o ~/ai-holding/assets/org-chart.svg
```

**Expected org chart:**
```
Rei (CEO)
├── NexusAI CTO
├── BrandFlow CMO
└── Crypto CEO
```

---

## Configuration Reference (hermes_local Adapter)

Dari `hermes-paperclip-adapter` README:

### Core
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `model` | string | `anthropic/claude-sonnet-4` | Format `provider/model` |
| `provider` | string | auto-detect | `auto`, `openrouter`, `anthropic`, `nous`, `openai-codex`, `zai`, `kimi-coding`, `minimax` |
| `timeoutSec` | number | `300` | Execution timeout |
| `graceSec` | number | `10` | Grace before SIGKILL |

### Tools
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabledToolsets` | string[] | all | `terminal`, `file`, `web`, `browser`, `code_execution`, `vision`, `mcp`, `creative`, `productivity` |

### Session
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `persistSession` | boolean | `true` | Resume across heartbeats via `--resume` |
| `worktreeMode` | boolean | `false` | Git worktree isolation |
| `checkpoints` | boolean | `false` | Filesystem checkpoints (rollback safety) |

### Advanced
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `hermesCommand` | string | `hermes` | Custom CLI path |
| `quiet` | boolean | `true` | Clean output (no banner/spinner) |
| `extraArgs` | string[] | `[]` | Extra CLI args |
| `env` | object | `{}` | Extra env vars |
| `promptTemplate` | string | built-in | Custom prompt template |

---

## Budget & Cost Notes

**Format:** Paperclip pakai **`budgetMonthlyCents`** (US cents, monthly), bukan `tokens/day` seperti SOP lama.

| Agent | Recommended Budget | USD/month |
|-------|-------------------|-----------|
| Rei (CEO) | 200000 cents | $2000 |
| NexusAI CTO | 100000 cents | $1000 |
| BrandFlow CMO | 80000 cents | $800 |
| Crypto CEO | 80000 cents | $800 |
| **Company total** | 500000 cents | **$5000/month** |

Adjust based on actual usage. Paperclip auto-tracks `spentMonthlyCents` per agent.

**Hard stop:** When `spent ≥ budget`, agent paused otomatis sampai bulan baru atau budget di-increase.

---

## Identity Coexistence (Hermes ↔ Paperclip)

Identity Drayco/Rei **udah di-bind di Hermes layer** lewat `install-rei-persona.sh`. Paperclip nggak override identity — adapter cuma spawn `hermes chat -q`, dan Hermes-nya udah know dia adalah Drayco.

**Verifikasi setelah Paperclip wake:**
```bash
# Trigger wakeup, lalu inspect run log
curl "http://localhost:3100/api/heartbeat-runs/${RUN_ID}/log" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY"

# Expected: log mention "Drayco" / "Rei", bukan "Kiro" atau generic AI
```

Kalau Hermes masih jawab "Kiro" → run `bin/install-rei-persona.sh --apply` lagi.

---

## Troubleshooting

### `hermes_local not found in adapter registry`

Adapter belum ke-register. Cek:
```bash
grep -r "hermes_local" ~/paperclip-src/server/src/
# Kalau kosong → Step 3 belum complete. Edit registry.ts, rebuild.
```

### TypeScript build error di Step 4

Type incompatibility. Coba:
```bash
cd ~/paperclip-src
pnpm tsc --noEmit --filter server 2>&1 | head -20
# Lihat error message — biasanya import path salah, atau adapter version too new/old
```

Solution: pin adapter ke version yang compatible dengan Paperclip version lo:
```bash
pnpm add hermes-paperclip-adapter@0.3.0 --filter server
```

### Hermes CLI not found by adapter

```bash
which hermes
# Kalau bukan di PATH, set di adapterConfig:
# "hermesCommand": "/full/path/to/hermes"
```

### Session not persisting across heartbeats

Cek:
```bash
# 1. persistSession: true di adapterConfig
# 2. Hermes session dir writable
ls -la ~/.hermes/sessions/
# 3. Adapter version supports session codec (≥ 0.3.0)
npm list hermes-paperclip-adapter
```

### Budget hit terlalu cepat

Tighten model atau increase budget:
```bash
# Switch ke cheaper model di adapterConfig
"model": "anthropic/claude-haiku-4.5"  # ~5x cheaper than sonnet

# Atau increase budget via UI / API
curl -X PATCH "http://localhost:3100/api/agents/${AGENT_ID}" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"budgetMonthlyCents": 300000}'
```

### Paperclip server crashes / port already in use

```bash
# Cek apa yang pakai port 3100
lsof -i :3100
# Kill old process kalau perlu
pkill -f "paperclip"

# Restart
pm2 restart paperclip
```

---

## Rollback Plan

Kalau Paperclip bermasalah, system Hermes tetap jalan 100% standalone:

```bash
# 1. Stop Paperclip
pm2 stop paperclip

# 2. Hermes tetap functional via Telegram
#    Routing, memory, tools — semua intact karena Paperclip = enhancement layer
```

Identity (`install-rei-persona.sh`) udah self-sufficient. Paperclip cuma nambah:
- Scheduling (heartbeat)
- Budget tracking
- Issue/ticket system
- Org chart visualization

Hermes punya internal pseudo-mention routing, memory, dan SOUL hierarchy yang nggak depend ke Paperclip.

---

## Anti-Patterns

❌ Skip Step 3 build verification → adapter dropdown nggak muncul, waste time debug
❌ Set `budgetMonthlyCents` < 50000 ($500) → agent stuck di middle of complex task
❌ Heartbeat interval < 30 menit → token waste di wake-up overhead
❌ Pakai model expensive (`opus`) untuk routing simple → budget habis cepat
❌ Skip `install-rei-persona.sh` → Paperclip jalan tapi Hermes masih jawab "Kiro"
❌ Modify `~/.paperclip/` data directly → corrupt DB, hancurin company state
❌ Run multiple Paperclip instances di port sama → silent state corruption

---

## Reference

- **Paperclip docs:** https://paperclipai-paperclip.mintlify.app/
- **Paperclip source:** https://github.com/paperclipai/paperclip
- **Adapter source:** https://github.com/NousResearch/hermes-paperclip-adapter
- **Adapter creating guide:** https://github.com/paperclipai/paperclip/blob/master/docs/adapters/creating-an-adapter.md
- **Discord:** https://discord.gg/m4HZY7xNG3
- **Identity setup (prerequisite):** `bin/install-rei-persona.sh` + `MAIN_SOUL.md`
- **Token tracking script:** `bin/track_tokens.py` (optional — Paperclip auto-tracks via `spentMonthlyCents`)

---

## Decision Log

- 2026-05-18: Reset Paperclip integration. SOP lama (`paperclip-integration.md` + `paperclip-rebuild.md`) banyak inaccuracies (port 4040 instead of 3100, fictional `npx paperclipai start --company` flag, wrong budget format `tokens/day` instead of `cents/month`). Fresh rewrite based on verified official sources.
- 2026-05-18: Identity sudah disetup separately (PR #23 + #24). Paperclip setup nggak perlu touch identity layer — Hermes runtime udah know Drayco/Rei.
- 2026-05-18: Strategy = Fork Paperclip source + register adapter built-in (more stable than external plugin loader).
