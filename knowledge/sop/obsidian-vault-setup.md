# Obsidian Vault Setup — Option B (Folder-as-Vault)

Versi: 1.0
Created: 2026-05-18
Owner: Fathur + Main Assistant (Drayco/Rei)

---

## Konsep

`~/ai-holding` sudah seluruhnya markdown — **langsung buka sebagai Obsidian vault.**
Zero migration, zero config tambahan yang rumit.

```
~/ai-holding/          ← ini = Obsidian vault-nya
├── SOUL.md
├── MAIN_SOUL.md
├── knowledge/
│   ├── persona/
│   ├── sop/
│   └── ...
├── companies/
├── memory/
└── .obsidian/         ← config Obsidian (minimal, sudah dibuat)
    ├── app.json
    └── workspace.json
```

---

## Setup Awal

### 1. Install Obsidian

Download dari https://obsidian.md — tersedia untuk Windows, Mac, Linux, Android, iOS.

### 2. Buka sebagai vault

```
Obsidian → "Open folder as vault"
→ Pilih: ~/ai-holding (atau \\wsl$\Ubuntu\home\fatur\ai-holding dari Windows)
```

### 3. Minimal recommended plugins

Buka Obsidian → Settings → Community plugins → Browse:

| Plugin | Fungsi | Install |
|--------|--------|---------|
| **Git** | Auto-commit changes ke repo | Wajib |
| **Templater** | Template untuk file baru | Recommended |
| **Dataview** | Query markdown files kayak database | Recommended |
| **Obsidian to GitHub Pages** | Kalau mau publish | Optional |

### 4. Git plugin config

```
Settings → Git:
- Auto pull interval: 10 minutes
- Auto commit interval: 5 minutes
- Commit message: "vault: auto-sync {{date}}"
```

---

## Workflow Sehari-hari

```
Fathur edit note di Obsidian (laptop/HP)
    ↓
Git plugin auto-commit + push ke GitHub
    ↓
Di WSL: git pull (manual atau cron)
    ↓
Hermes baca file yang diupdate
```

---

## Catatan Penting

### Files yang jangan diedit dari Obsidian tanpa hati-hati

| File | Kenapa |
|------|--------|
| `SOUL.md` | Root constitution — perubahan affect semua agents |
| `MAIN_SOUL.md` | Main persona — edit dengan intention |
| `companies/*/SOUL.md` | Company constitution |
| `memory/global.md` | Operational log — append only |

**Best practice:** Edit file-file di atas dari terminal/IDE yang lebih sadar context, bukan dari Obsidian casual editing.

### Untuk files yang aman diedit bebas dari Obsidian

- `knowledge/` semua files — boleh edit, tambah, refactor
- `credentials/templates/` — boleh update schema
- Notes baru di `memory/` yang bukan global.md

---

## Migration ke Option A (MCP Server) — Kapan?

Option A layered on top of B — folder tidak berubah, cuma tambah programmatic access.

**Trigger untuk migrate ke A:**
- Perlu auto-tag notes dari agent
- Perlu search by frontmatter property
- Perlu Hermes create/update notes secara programmatic (bukan cuma read)
- Perlu graph traversal dari agent

**Setup Option A (preview, eksekusi nanti):**

```bash
# 1. Install Obsidian Local REST API plugin
# Obsidian → Community plugins → "Local REST API"

# 2. Install MCP server
npm install -g obsidian-mcp-server
# atau
npx cyanheads/obsidian-mcp-server

# 3. Hermes config.yaml
# mcp:
#   servers:
#     - name: obsidian
#       command: npx
#       args: ["obsidian-mcp-server"]
#       env:
#         OBSIDIAN_API_KEY: "dari Local REST API plugin settings"
#         OBSIDIAN_BASE_URL: "http://localhost:27123"
```

Kalau sudah siap migrate → update file ini dan buat PR.

---

## Verify Setup

```bash
# Cek .obsidian folder sudah ada
ls -la ~/ai-holding/.obsidian/

# Cek Obsidian bisa buka vault
# (manual: buka Obsidian app, pilih folder)

# Cek Git plugin berfungsi
cd ~/ai-holding && git log --oneline -3
```

---

## Reference

- Obsidian: https://obsidian.md
- Git plugin: https://github.com/denolehov/obsidian-git
- MCP server (Option A future): https://github.com/cyanheads/obsidian-mcp-server
