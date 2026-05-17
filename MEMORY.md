# MEMORY.md — AI Holding Strategic Memory

Versi: 2.2
Update terakhir: 2026-05-17 (post Update 9 — Tahap G complete)
Owner: Fathur
Scope: Holding-level strategic state. **Read this at session start.**

---

## Peran File Ini vs `memory/global.md`

Ada dua file memory di tingkat holding. Sengaja dipisah, jangan digabung:

| File | Sifat | Format | Kapan Ditulis |
|---|---|---|---|
| **`MEMORY.md`** (this file) | Strategic / high-level | Narrative paragraphs | Saat ada keputusan arah / arsitektur / migrasi besar |
| **`memory/global.md`** | Operational / durable log | Tagged entries `[DECISION]`, `[TASK]`, `[ARCH]`, `[TOOL]`, `[INSIGHT]` | Saat ada keputusan, task, atau perubahan operasional |

**Read order**: `MEMORY.md` first (gives big picture), then `memory/global.md` if you need operational detail.

---

## Current Setup

Fathur is building an AI Holding system using Hermes on WSL2.

- **Mode**: Option A portable.
- **Surface**: One Telegram bot.
- **Brain**: One Main Assistant (Hermes-driven).
- **Workspace**: `~/ai-holding`.
- **Future migration**: Option C (Telegram Group Topics, one topic per company).

---

## SOUL Hierarchy (Active)

```
Tier 0: SOUL.md                         — Root constitution (loyalty, execute stance, 4 boundaries)
Tier 1: MAIN_SOUL.md                    — Main Assistant personality + decision authority
Tier 2: companies/<co>/SOUL.md          — 3 perusahaan (NexusAI, BrandFlow, Crypto Consultant)
Tier 3: companies/<co>/agents/<role>.md — 18 agent SOULs (key roles)
```

Inheritance: Root → Company → Agent. Konflik prinsip → atas menang. Konflik spesifik → bawah menang (selama tidak melanggar root).

---

## Strategic Decisions (Durable)

1. **Main Assistant first** — fokus stabilkan single entry point sebelum scale.
2. **Pseudo-mention routing** — `@company` dan `@company.agent`. Slash command `/company` ditolak Hermes.
3. **Companies isolated** — setiap perusahaan punya MEMORY.md sendiri, tidak boleh dicampur.
4. **Knowledge compact** — Markdown, ringkas, bukan article dump.
5. **Tasks pakai JSONL** — schema sudah didefinisi di `companies/nexusai/skills/automation/SKILL.md`. **Implementasi production di `bin/log_task.py`, `update_task.py`, `list_tasks.py`, `log_message.py` (post Update 8).**
6. **Knowledge management dibangun manual** oleh Fathur, bukan delegated penuh ke Hermes.
7. **Tool risk levels** — Low (read-only) tidak butuh approval; Medium butuh konfirmasi; High wajib konfirmasi eksplisit.
8. **Boundary #4 amplified** untuk role rawan (BrandFlow community, Crypto onchain, Crypto risk, Crypto reporting).
9. **Task Logger model**: single `inbox.jsonl` + status field (bukan 3-file move pattern). Append-only `logs.jsonl` untuk audit. State machine eksplisit dengan transisi yang divalidasi script.
10. **Tier 3 SOUL coverage**: setiap role aktif di `AGENTS.md` punya Tier 3 SOUL (32 file total, post Update 9). Tidak ada lagi role yang fall-back ke Tier 2 boilerplate.
11. **Hermes whitelist policy**: Risk=Low + read-only + no-secrets + no-mutation = auto-approve. Risk=Medium/High selalu konfirmasi. Detail di `knowledge/tools/hermes-whitelist.md`.
12. **Archival workflow**: terminal task (DONE/CANCELLED) > 30 hari → `archive/<YYYY-MM>.jsonl` per company. `logs.jsonl` NEVER diarsipkan (audit trail). Idempotent + dry-run support.

---

## Architecture (Active)

```
Telegram Bot
    ↓
Hermes (Main Assistant)
    ↓
AI Holding Workspace (~/ai-holding)
    ↓
┌─────────────────────────────────────────┐
│ Tier 0/1 SOUL (Root + Main)            │
│ knowledge/ (8 files: core, agent-      │
│   design, tools, software, marketing,  │
│   crypto, sop, karpathy)               │
│ companies/                              │
│   nexusai/ (10 agents, 7 skills)       │
│   brandflow/ (11 agents, 7 skills)     │
│   crypto-consultant/ (11 agents, 7     │
│     skills)                             │
│ tools/ (3 active: fear_greed.py,        │
│   btc_price.py, news_sentiment.py)      │
│ tasks/ (company-index.jsonl)            │
│ memory/ (global.md — operational log)  │
│ bin/ (create-company.sh,                │
│       log_task.py, update_task.py,      │
│       list_tasks.py, log_message.py,    │
│       task_logger.py [lib],             │
│       log-task.sh,                      │
│       archive_tasks.py,                 │
│       archive_messages.py,              │
│       recap_manager.py)                 │
│ templates/ (company scaffold)           │
└─────────────────────────────────────────┘
```

---

## Companies Active

| Slug | Type | Focus |
|---|---|---|
| `@nexusai` | IT Software | cloud, DevOps, AI agents, SaaS |
| `@brandflow` | Marketing & Content | branding, content, social media, campaign |
| `@crypto` | Crypto Research | market research, cycle analysis, risk, reporting |

Total agent: 32 (10 NexusAI + 11 BrandFlow + 11 Crypto Consultant).
Tier 3 SOULs: 32 dari 32 — full coverage post Update 9.

---

## Knowledge Layout (Reference)

| Folder | File / Purpose |
|---|---|
| `knowledge/core/` | `principles.md` — cara berpikir umum semua agent |
| `knowledge/agent-design/` | `memory-rules.md`, `tool-use-rules.md`, `task-logger-rules.md` |
| `knowledge/tools/` | `tool-registry.md`, `hermes-whitelist.md` |
| `knowledge/software/` | `software-development-sop.md` (NexusAI domain) |
| `knowledge/marketing/` | `marketing-sop.md` (BrandFlow domain) |
| `knowledge/crypto/` | `crypto-research-framework.md` (Crypto domain) |
| `knowledge/sop/` | `README.md` — reusable skill library |
| `knowledge/karpathy.md` | Karpathy-inspired principles |

---

## Migration Plan

**Current** (Option A):
```
Telegram Bot → Main Assistant → command routing
```

**Future** (Option C):
```
Telegram Group + Topics:
  Topic NexusAI    → companies/nexusai
  Topic BrandFlow  → companies/brandflow
  Topic Crypto     → companies/crypto-consultant
```

Migrate when Option A is stable and `tasks/` JSONL pipeline is operational.

---

## When To Update This File

Write here when:
- A **strategic** decision changes the holding's direction.
- A **new company** is added (or removed).
- An **architecture-level** change happens (folder restructure, migration, big tool swap).
- A **migration milestone** completes.

For everything else (day-to-day decisions, task tracking, tool registry changes, insight recording), use `memory/global.md`.

If a decision is **both** strategic AND operational, write the strategic summary here and the tagged entry in `memory/global.md` — they're not mutually exclusive.
