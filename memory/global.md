# memory/global.md — AI Holding Operational Memory

Versi: 2.1
Update terakhir: 2026-05-17 (post Update 8 — Task Logger JSONL)
Dikelola oleh: Main Assistant
Scope: Tagged operational log. **Read this when starting work that touches existing decisions.**

---

## Peran File Ini vs `MEMORY.md` (root)

Lihat `MEMORY.md` di root untuk pembagian tugas. Singkatnya:

- `MEMORY.md` (root) = strategic / narrative — big picture.
- `memory/global.md` (this file) = operational / tagged — day-to-day durable log.

Format wajib pakai tag (lihat `knowledge/agent-design/memory-rules.md`):
`[DECISION] [TASK] [DONE] [TOOL] [ARCH] [INSIGHT] [NOTE]`

---

## Profil Owner

```
Nama       : Fathur
System     : WSL2 + Hermes + Telegram Bot
Workspace  : /home/fatur/ai-holding
```

---

## Perusahaan Aktif

```
@nexusai      → IT Software Company (cloud, DevOps, AI agents, SaaS)
@brandflow    → Marketing & Content Company (branding, content, social media)
@crypto       → Crypto Research Company (market research, risk, reporting)
```

Total agent: 32. Tier 3 SOULs: 18.

---

## Decisions

[DECISION] 2026-05-17 — Routing pakai pseudo-mention (`@company`) bukan slash command (`/company`). Slash command ditolak Hermes/Telegram.
[DECISION] 2026-05-17 — "perusahaan" tanpa konteks = perusahaan AI Holding milik Fathur (bukan dunia nyata). "perusahaan nyata/publik/di dunia" → baru konteks dunia luar.
[DECISION] 2026-05-17 — Knowledge management dibangun manual oleh Fathur, bukan di-generate Hermes secara penuh.
[DECISION] 2026-05-17 — Tool Risk Low tidak perlu approval; Risk Medium perlu konfirmasi; Risk High wajib konfirmasi eksplisit.
[DECISION] 2026-05-17 — SOUL hierarchy 4-tier ditetapkan: Root (SOUL.md) → Main (MAIN_SOUL.md) → Company (Tier 2) → Agent (Tier 3).
[DECISION] 2026-05-17 — Boundary #4 (tidak bicara atas nama Fathur di publik) diamplify khusus di BrandFlow community + Crypto onchain/risk/reporting.
[DECISION] 2026-05-17 — Skill specialization model: per-company skill set, hapus boilerplate yang tidak relevan, bukan satu skill set seragam.
[DECISION] 2026-05-17 — Memory dipecah: `MEMORY.md` (root) = strategic narrative; `memory/global.md` = operational tagged log.
[DECISION] 2026-05-17 — Task Logger pakai single-file `inbox.jsonl` + status field, BUKAN 3-file move pattern (inbox/active/done). Alasan: idempoten, no race condition, mudah query.
[DECISION] 2026-05-17 — Task Logger state machine eksplisit & divalidasi: NEW → IN_PROGRESS → DONE / FAILED / CANCELLED. Transisi tidak valid ditolak script.
[DECISION] 2026-05-17 — `logs.jsonl` adalah append-only audit trail, tidak boleh diedit / dihapus tanpa konfirmasi user.

---

## Architecture Changes

[ARCH] 2026-05-17 — Folder `knowledge/` dibuat dengan 8 file aktif (core, agent-design, tools, software, marketing, crypto, sop, karpathy).
[ARCH] 2026-05-17 — `tool-registry.md` dibuat di `knowledge/tools/`.
[ARCH] 2026-05-17 — `tool-use-rules.md` + `memory-rules.md` dibuat di `knowledge/agent-design/`.
[ARCH] 2026-05-17 — `crypto-research-framework.md` dibuat di `knowledge/crypto/` (6-layer format).
[ARCH] 2026-05-17 — Tier 2 Company SOULs ditulis untuk 3 perusahaan dengan culture & decision authority spesifik.
[ARCH] 2026-05-17 — Tier 3 Agent SOULs (18 file) ditulis untuk role utama tiap perusahaan.
[ARCH] 2026-05-17 — 6 role baru ditambahkan: `@nexusai.security`, `@nexusai.ml`, `@brandflow.designer`, `@brandflow.community`, `@crypto.onchain`, `@crypto.macro`.
[ARCH] 2026-05-17 — Skill files specialized per company (21 file aktif, 16 boilerplate dihapus). 3 SKILLS.md index dibuat.
[ARCH] 2026-05-17 — `bin/create-company.sh` updated untuk substitusi `{{COMPANY_SLUG}}`. Template di `templates/company/` updated ke Tier-2 design.
[ARCH] 2026-05-17 — `MEMORY.md` (root) + `memory/global.md` direstrukturisasi: split jelas strategic vs operational.
[ARCH] 2026-05-17 — Task Logger JSONL diimplementasi: 4 script (`log_task.py`, `update_task.py`, `list_tasks.py`, `log_message.py`) + shared library (`task_logger.py`) + bash wrapper (`log-task.sh`) di `bin/`.
[ARCH] 2026-05-17 — `knowledge/agent-design/task-logger-rules.md` ditulis sebagai authoritative rules: schema, state machine, filter rules, anti-pattern.
[ARCH] 2026-05-17 — `companies/nexusai/skills/automation/SKILL.md` di-reconcile dengan reality file structure (4-file: inbox/logs/messages/recap), bukan struktur 3-file move yang awal.

---

## Tools

[TOOL] fear_greed.py — Active — `/home/fatur/ai-holding/tools/fear_greed.py` — fetches Crypto Fear & Greed Index from Alternative.me.
[TOOL] create-company.sh — Active — `/home/fatur/ai-holding/bin/create-company.sh` — generates new company from template.
[TOOL] log_task.py — Active — `/home/fatur/ai-holding/bin/log_task.py` — append task ke inbox.jsonl + audit ke logs.jsonl.
[TOOL] update_task.py — Active — `/home/fatur/ai-holding/bin/update_task.py` — transition status existing task (state machine validated) + audit.
[TOOL] list_tasks.py — Active — `/home/fatur/ai-holding/bin/list_tasks.py` — filter & list tasks (table/json/jsonl).
[TOOL] log_message.py — Active — `/home/fatur/ai-holding/bin/log_message.py` — agent-to-agent durable message ke messages.jsonl.
[TOOL] task_logger.py — Active (library) — `/home/fatur/ai-holding/bin/task_logger.py` — shared schema/validation/I/O.
[TOOL] log-task.sh — Active — `/home/fatur/ai-holding/bin/log-task.sh` — bash wrapper 3-arg untuk log_task.py.
[TOOL] btc_price.py — PLANNED — belum dibuat. Reference: CoinGecko API.
[TOOL] news_sentiment.py — PLANNED — belum dibuat.

---

## Active Tasks

[TASK] Belum ada task aktif saat ini.

---

## Insights / Notes

[NOTE] 2026-05-17 — Setup knowledge management Tahap 1 selesai (Update 3).
[NOTE] 2026-05-17 — Tier 2 + Tier 3 + skill specialization selesai (Update 4-6).
[NOTE] 2026-05-17 — Memory reference inkonsistensi diselesaikan: MAIN.md & AGENTS.md sekarang konsisten merefer kedua file dengan peran yang jelas (Update 7).
[NOTE] 2026-05-17 — Task Logger JSONL operasional: 4 script production + shared library + bash wrapper + rules doc (Update 8). Smoke test full lifecycle: create → list → transition (state machine validated) → DONE → message hand-off.
[NOTE] 2026-05-17 — Tahap berikutnya (Tahap G): tools tambahan (`btc_price.py`, `news_sentiment.py`) + Tier 3 SOULs untuk role sisa on-demand + Hermes hardening (whitelist tool read-only).

---

## When to Update This File

Tulis entry tagged baru saat:
- **[DECISION]** keputusan operasional yang durable diambil.
- **[ARCH]** perubahan struktur file/folder, perubahan SOUL hierarchy, role baru.
- **[TOOL]** tool ditambah/diubah/dihapus dari registry.
- **[TASK]** task baru yang penting masuk ke tracker.
- **[DONE]** task tracked sebelumnya selesai.
- **[INSIGHT]** temuan dari kerja yang punya implikasi durable.
- **[NOTE]** catatan operasional lain yang tidak fit kategori atas.

Jangan tulis basa-basi, klarifikasi ringan, atau task tanpa keputusan.

Detail: `knowledge/agent-design/memory-rules.md`.
