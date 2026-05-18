# Paperclip Rebuild — Register hermes_local Adapter

Versi: 1.0
Created: 2026-05-18
Owner: @nexusai.devops + Operator
Status: BLOCKED — requires Paperclip server source modification
Effort: 2-4 jam engineering
Source: https://github.com/NousResearch/hermes-paperclip-adapter (README.md)
        https://github.com/paperclipai/paperclip/blob/master/docs/adapters/creating-an-adapter.md

---

## Problem Statement

Paperclip server yang di-install via `npx paperclipai onboard` **tidak include** adapter `hermes_local` di registry-nya. Adapter `hermes-paperclip-adapter` (v0.3.0) sudah ter-install sebagai npm package, tapi Paperclip server nggak recognize `adapterType: "hermes_local"` tanpa di-register manual.

**Root cause:** `hermes-paperclip-adapter` adalah **external adapter plugin** — perlu di-register di Paperclip server source code (`server/src/adapters/registry.ts`).

---

## Prerequisites

```bash
# Sudah terinstall:
node --version          # v20+
pnpm --version          # 9.15+
hermes --version        # Hermes Agent CLI
npm list -g hermes-paperclip-adapter  # v0.3.0

# Paperclip server location (dari npx onboard):
ls ~/.paperclip/        # atau tempat Paperclip ter-install
```

---

## Step 1: Clone Paperclip Source

```bash
cd ~
git clone https://github.com/paperclipai/paperclip.git paperclip-src
cd paperclip-src
pnpm install
```

---

## Step 2: Register hermes_local Adapter

Edit `server/src/adapters/registry.ts`:

```bash
nano server/src/adapters/registry.ts
```

Tambahkan import + registration:

```typescript
// === TAMBAHKAN DI BAGIAN IMPORTS ===
import * as hermesLocal from "hermes-paperclip-adapter";
import {
  execute,
  testEnvironment,
  detectModel,
  listSkills,
  syncSkills,
  sessionCodec,
} from "hermes-paperclip-adapter/server";

// === TAMBAHKAN DI BAGIAN REGISTRY (setelah adapter lain) ===
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

---

## Step 3: Add hermes-paperclip-adapter sebagai Dependency

```bash
cd ~/paperclip-src
pnpm add hermes-paperclip-adapter --filter server
# Atau:
# cd server && pnpm add hermes-paperclip-adapter
```

Verify di `server/package.json`:
```json
{
  "dependencies": {
    "hermes-paperclip-adapter": "^0.3.0"
  }
}
```

---

## Step 4: Register UI Parser (Optional tapi Recommended)

Untuk transcript parsing (tool cards di dashboard), tambahkan ke `ui/src/adapters/registry.ts`:

```typescript
// Di UI registry file
import { parseStdout } from "hermes-paperclip-adapter/ui-parser";

uiRegistry.set("hermes_local", {
  parseStdout,
});
```

Dan CLI formatter di `cli/src/adapters/registry.ts`:

```typescript
import { formatStdoutEvent } from "hermes-paperclip-adapter/cli";

cliRegistry.set("hermes_local", {
  formatStdoutEvent,
});
```

**NOTE:** Kalau ini terlalu ribet untuk pertama kali, skip UI + CLI registry — server registry aja cukup untuk heartbeat + execution. Dashboard bakal tampil raw text tanpa formatted tool cards.

---

## Step 5: Build Paperclip

```bash
cd ~/paperclip-src
pnpm build
# Atau build server aja:
# pnpm build --filter server
```

Kalau ada TypeScript error, cek:
```bash
# Pastikan types compatible
pnpm tsc --noEmit --filter server
```

---

## Step 6: Start Rebuilt Server

```bash
# Stop existing Paperclip instance
pm2 stop paperclip 2>/dev/null
pkill -f "paperclipai" 2>/dev/null

# Start rebuilt version
cd ~/paperclip-src
pnpm dev
# Atau production:
# pnpm start
```

Server harusnya jalan di `http://localhost:3100`.

---

## Step 7: Create Hermes Agent via API/UI

### Via Web UI (http://localhost:3100):

1. Navigate ke company "AI Holding"
2. Add Employee → Agent
3. Set:
   - Name: `Rei (Drayco)`
   - Adapter Type: `hermes_local` (harusnya muncul di dropdown setelah rebuild)
   - Config:

```json
{
  "model": "kr/claude-haiku-4.5",
  "maxIterations": 50,
  "timeoutSec": 300,
  "persistSession": true,
  "enabledToolsets": ["terminal", "file", "web", "browser", "code_execution"]
}
```

### Via API:

```bash
curl -X POST http://localhost:3100/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rei (Drayco)",
    "companyId": "<your-company-id>",
    "adapterType": "hermes_local",
    "adapterConfig": {
      "model": "kr/claude-haiku-4.5",
      "maxIterations": 50,
      "timeoutSec": 300,
      "persistSession": true,
      "enabledToolsets": ["terminal", "file", "web"]
    }
  }'
```

---

## Step 8: Configure Heartbeat

Via Web UI atau API:

```bash
curl -X PATCH http://localhost:3100/api/agents/<agent-id>/heartbeat \
  -H "Content-Type: application/json" \
  -d '{
    "intervalSeconds": 3600,
    "enabled": true
  }'
```

---

## Step 9: Test Heartbeat

```bash
# Manual trigger (via API)
curl -X POST http://localhost:3100/api/agents/<agent-id>/wake \
  -H "Content-Type: application/json" \
  -d '{"reason": "manual_test"}'

# Cek logs
curl http://localhost:3100/api/agents/<agent-id>/runs?limit=1 | python3 -m json.tool
```

Expected: Hermes CLI di-spawn in single-query mode (`hermes chat -q`), execute task, return result ke Paperclip.

---

## Step 10: Verify Full Integration

```bash
# 1. Adapter registered
curl http://localhost:3100/api/adapters | python3 -m json.tool | grep hermes_local
# Expected: hermes_local di list

# 2. Agent status
curl http://localhost:3100/api/agents/<agent-id> | python3 -m json.tool
# Expected: status "active", adapterType "hermes_local"

# 3. Heartbeat running
curl http://localhost:3100/api/agents/<agent-id>/heartbeat | python3 -m json.tool
# Expected: enabled true, intervalSeconds 3600

# 4. Dashboard visual
# Open: http://localhost:3100
# → Company "AI Holding" → Agent "Rei" → should show heartbeat status
```

---

## Agent Config Reference (hermes_local)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `model` | string | `anthropic/claude-sonnet-4` | Model in provider/model format |
| `provider` | string | auto | API provider override |
| `timeoutSec` | number | 300 | Execution timeout |
| `graceSec` | number | 10 | Grace period before SIGKILL |
| `toolsets` | string | all | Comma-separated toolsets |
| `persistSession` | boolean | true | Resume across heartbeats |
| `worktreeMode` | boolean | false | Git worktree isolation |
| `checkpoints` | boolean | false | Filesystem checkpoints |
| `hermesCommand` | string | hermes | Custom CLI path |
| `verbose` | boolean | false | Verbose output |
| `quiet` | boolean | true | Quiet mode |
| `extraArgs` | string[] | [] | Additional CLI arguments |
| `env` | object | {} | Extra env vars |
| `promptTemplate` | string | built-in | Custom prompt |
| `paperclipApiUrl` | string | http://127.0.0.1:3100/api | API base URL |

Available toolsets: `terminal`, `file`, `web`, `browser`, `code_execution`, `vision`, `mcp`, `creative`, `productivity`

---

## How It Works (Architecture)

```
Paperclip (localhost:3100)           Hermes Agent
┌──────────────────┐                ┌──────────────────┐
│  Heartbeat       │                │                  │
│  Scheduler       │───execute()──▶ │  hermes chat -q  │
│                  │                │                  │
│  Issue System    │                │  30+ Tools       │
│  Comment Wakes   │◀──results──── │  Memory System   │
│                  │                │  Session DB      │
│  Cost Tracking   │                │  Skills          │
│                  │                │  MCP Client      │
│  Skill Sync      │◀──snapshot─── │  ~/.hermes/skills│
│  Org Chart       │                │                  │
└──────────────────┘                └──────────────────┘
```

Adapter spawns Hermes CLI in single-query mode (`-q`). Hermes processes task, exits. Adapter:
1. Captures stdout/stderr → parse token usage, session IDs, cost
2. Parses into structured TranscriptEntry objects
3. Reports back to Paperclip with cost, usage, session state
4. Session persistence via `--resume` flag

---

## Full Org Mapping (Setelah Rei Works)

Setelah Rei (CEO) berhasil, tambah 3 company employees:

```json
[
  {
    "name": "NexusAI CTO",
    "adapterType": "hermes_local",
    "adapterConfig": {
      "model": "kr/claude-haiku-4.5",
      "maxIterations": 50,
      "timeoutSec": 300,
      "enabledToolsets": ["terminal", "file", "web", "code_execution"]
    }
  },
  {
    "name": "BrandFlow CMO",
    "adapterType": "hermes_local",
    "adapterConfig": {
      "model": "kr/claude-haiku-4.5",
      "maxIterations": 30,
      "timeoutSec": 180,
      "enabledToolsets": ["terminal", "file", "web"]
    }
  },
  {
    "name": "Crypto Consultant CEO",
    "adapterType": "hermes_local",
    "adapterConfig": {
      "model": "kr/claude-haiku-4.5",
      "maxIterations": 30,
      "timeoutSec": 180,
      "enabledToolsets": ["terminal", "file", "web"]
    }
  }
]
```

Budget per agent: set via Web UI → Agent Settings → Budget.

---

## Troubleshooting

### "hermes_local not found in adapter registry"

Adapter belum ke-register. Cek:
```bash
grep -r "hermes_local" ~/paperclip-src/server/src/
```
Kalau kosong → Step 2 belum dijalanin.

### TypeScript build error

```bash
cd ~/paperclip-src
pnpm tsc --noEmit --filter server 2>&1 | head -20
# Fix type errors, usually import path issues
```

### Hermes CLI not found by adapter

```bash
which hermes
# Kalau bukan di PATH, set di adapterConfig:
# "hermesCommand": "/full/path/to/hermes"
```

### Session not persisting across heartbeats

Cek `persistSession: true` di adapterConfig + verify Hermes session dir:
```bash
ls ~/.hermes/sessions/
```

---

## PM2 Persistent Setup (Production)

```bash
cd ~/paperclip-src
pm2 start "pnpm start" --name paperclip-rebuilt --cwd ~/paperclip-src
pm2 save
pm2 startup
```

---

## Rollback

```bash
# Stop rebuilt server
pm2 stop paperclip-rebuilt

# Start original Paperclip (kalau masih ada)
npx paperclipai start --company ai-holding
# Atau: disable Paperclip entirely di ~/.hermes/config.yaml
```

---

## Decision Log

- 2026-05-18: Agent report — adapter v0.3.0 installed, server needs rebuild
- 2026-05-18: Fathur decision — proceed with rebuild (long-term orchestration value)
- Blocker: server/src/adapters/registry.ts code change required
- Effort estimate: 2-4 jam (clone + modify + build + test)
- Risk: Low (additive change, rollback = stop rebuilt server)

---

## Reference

- Adapter README: https://github.com/NousResearch/hermes-paperclip-adapter
- Creating adapters: https://github.com/paperclipai/paperclip/blob/master/docs/adapters/creating-an-adapter.md
- Paperclip docs: https://paperclipai-paperclip.mintlify.app/
- Previous SOP: `knowledge/sop/paperclip-integration.md` (high-level, pre-rebuild)
