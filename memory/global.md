# memory/global.md — AI Holding Operational Memory

Versi: 2.0
Update terakhir: 2026-05-17 (post Update 6)
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

---

## Tools

[TOOL] fear_greed.py — Active — `/home/fatur/ai-holding/tools/fear_greed.py` — fetches Crypto Fear & Greed Index from Alternative.me.
[TOOL] create-company.sh — Active — `/home/fatur/ai-holding/bin/create-company.sh` — generates new company from template.
[TOOL] btc_price.py — PLANNED — belum dibuat. Reference: CoinGecko API.
[TOOL] news_sentiment.py — PLANNED — belum dibuat.

---

## Active Tasks

[TASK] Belum ada task aktif saat ini.

---

## Insights / Notes

[NOTE] 2026-05-17 — Setup knowledge management Tahap 1 selesai (Update 3).
[NOTE] 2026-05-17 — Tier 2 + Tier 3 + skill specialization selesai (Update 4-6).
[NOTE] 2026-05-17 — Memory reference inkonsistensi diselesaikan: MAIN.md & AGENTS.md sekarang konsisten merefer kedua file dengan peran yang jelas.
[NOTE] 2026-05-17 — Tahap berikutnya: Task Logger JSONL implementation, btc_price.py, news_sentiment.py.

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
