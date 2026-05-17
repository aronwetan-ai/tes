# memory/global.md — AI Holding Operational Memory

Versi: 2.3
Update terakhir: 2026-05-17 (post Update 10 — NexusAI deepening)
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
[DECISION] 2026-05-17 — Tier 3 SOUL coverage diselesaikan untuk SEMUA role aktif (32/32). Tidak ada lagi role yang fall-back ke Tier 2 boilerplate. Update 9 / Tahap G.
[DECISION] 2026-05-17 — Hermes whitelist policy: hanya Risk=Low + read-only + no-secrets + no-external-mutation + bounded-cost yang boleh auto-approve. Detail di `knowledge/tools/hermes-whitelist.md`.
[DECISION] 2026-05-17 — Task archival: DONE/CANCELLED > 30 hari pindah ke `archive/<YYYY-MM>.jsonl`. FAILED tidak auto-archive (mungkin retry). `logs.jsonl` NEVER diarsipkan.
[DECISION] 2026-05-17 — Recap pakai windowed model (daily/weekly/monthly/custom) dengan output append-only ke `recap.jsonl`. Recap adalah aggregate snapshot, BUKAN source of truth — truth tetap di `logs.jsonl`.
[DECISION] 2026-05-17 — Agency-context-driven output untuk NexusAI: Fathur jalankan digital agency Indonesia (performance marketing + AI automation, target 20–50 client). NexusAI engineering default ke multi-tenancy, credential compartmentalization, anti-leak, OPSEC-aware, sustainable rate. Detail di `companies/nexusai/SOUL.md` v1.1 section "Agency Context".
[DECISION] 2026-05-17 — Two tool categories declined regardless of framing — generic face recognition + mass-spam-via-proxy. Substitutes tersedia (EXIF + reverse-image + OSINT identifier-pivot untuk yang pertama; sustainable outreach + load-test against own infra untuk yang kedua). Documented at `knowledge/scope/declined-tools.md`.
[DECISION] 2026-05-17 — Skill split convention NexusAI: parent skill (multi-agent, broad) + agent-specific deep skill (extends parent, owned by one agent). Front-matter `agent_specific` + `parent_skill`. Three deep skills shipped Update 10: security/threat-modeling, qa/acceptance-criteria-templates, ml-agent/prompt-eval.

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
[ARCH] 2026-05-17 — Tier 3 SOULs lengkap: 14 file baru (Update 9). NexusAI: pm/frontend/qa/writer. BrandFlow: pm/seo/analytics/qa/writer. Crypto: pm/data/qa/report/writer. Total agent SOULs: 32 (was 18).
[ARCH] 2026-05-17 — Tools tambahan diimplementasi: `tools/btc_price.py` (CoinGecko) + `tools/news_sentiment.py` (CryptoPanic + keyword sentiment heuristic). Both Risk=Low, whitelisted.
[ARCH] 2026-05-17 — Task lifecycle ops: `bin/archive_tasks.py` + `bin/archive_messages.py` + `bin/recap_manager.py`. All use shared `task_logger.py` library. Dry-run support across all three.
[ARCH] 2026-05-17 — `knowledge/tools/hermes-whitelist.md` ditulis sebagai authoritative policy untuk Hermes auto-approval. Registry (`tool-registry.md`) gain Whitelisted column.
[ARCH] 2026-05-17 — Update 10: NexusAI deepening shipped. (1) `knowledge/scope/declined-tools.md` written — documents 2 declined tool categories with substitute mapping. (2) `companies/nexusai/SOUL.md` v1.1 — agency-context section added. (3) 7 parent skill files deepened with "Senior Patterns (Deep Dive)" section. (4) 3 agent-specific deep skill files added: `skills/security/threat-modeling.md`, `skills/qa/acceptance-criteria-templates.md`, `skills/ml-agent/prompt-eval.md`. (5) 20 knowledge cheatsheets added (12 software, 4 security, 2 agile, 2 ml). (6) 10 tools added (5 utility: json_schema_check, markdown_lint, dep_audit, api_health, prompt_eval; 5 agency-context: cred_vault, secret_scanner, exif_extract, reverse_image_lookup, osint_lookup). (7) `tool-registry.md` v1.3 — 22 entries. (8) `companies/nexusai/SKILLS.md` v1.1.

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
[TOOL] btc_price.py — Active (post Update 9) — `/home/fatur/ai-holding/tools/btc_price.py` — CoinGecko BTC price + 24h change. Whitelisted.
[TOOL] news_sentiment.py — Active (post Update 9) — `/home/fatur/ai-holding/tools/news_sentiment.py` — CryptoPanic headlines + keyword sentiment. Whitelisted.
[TOOL] archive_tasks.py — Active (post Update 9) — `/home/fatur/ai-holding/bin/archive_tasks.py` — move DONE/CANCELLED > N days to archive/<YYYY-MM>.jsonl. Risk=Medium, dry-run whitelistable.
[TOOL] archive_messages.py — Active (post Update 9) — `/home/fatur/ai-holding/bin/archive_messages.py` — same for messages.jsonl. Risk=Medium, dry-run whitelistable.
[TOOL] recap_manager.py — Active (post Update 9) — `/home/fatur/ai-holding/bin/recap_manager.py` — windowed recap append to recap.jsonl. Risk=Medium, dry-run whitelistable.
[TOOL] json_schema_check.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/json_schema_check.py` — validate JSON files against schema. Risk=Low, whitelisted.
[TOOL] markdown_lint.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/markdown_lint.py` — Markdown doc-quality lint. Risk=Low, whitelisted.
[TOOL] dep_audit.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/dep_audit.py` — pip/npm outdated + vulnerability audit. Risk=Low, whitelisted.
[TOOL] api_health.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/api_health.py` — single-URL GET probe + p50/p95/max latency. Risk=Low, whitelisted.
[TOOL] prompt_eval.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/prompt_eval.py` — local YAML/JSON eval runner with 10 grader types. Risk=Low, whitelisted.
[TOOL] cred_vault.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/cred_vault.py` — AES-256-GCM per-client credential vault. Mixed risk per subcommand; read-only sub-cmds whitelistable.
[TOOL] secret_scanner.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/secret_scanner.py` — 18-pattern secret leak scan. Risk=Low, whitelisted.
[TOOL] exif_extract.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/exif_extract.py` — EXIF metadata + GPS DMS→decimal. Risk=Low, whitelisted.
[TOOL] reverse_image_lookup.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/reverse_image_lookup.py` — Google Lens / Yandex / TinEye / Bing / SauceNAO URL builder. Risk=Low, whitelisted (without --open).
[TOOL] osint_lookup.py — Active (post Update 10) — `/home/fatur/ai-holding/tools/osint_lookup.py` — phone/email/username pivot + 30-platform Sherlock probe. Risk=Low, whitelisted.

---

## Active Tasks

[TASK] Belum ada task aktif saat ini.

---

## Insights / Notes

[NOTE] 2026-05-17 — Setup knowledge management Tahap 1 selesai (Update 3).
[NOTE] 2026-05-17 — Tier 2 + Tier 3 + skill specialization selesai (Update 4-6).
[NOTE] 2026-05-17 — Memory reference inkonsistensi diselesaikan: MAIN.md & AGENTS.md sekarang konsisten merefer kedua file dengan peran yang jelas (Update 7).
[NOTE] 2026-05-17 — Task Logger JSONL operasional: 4 script production + shared library + bash wrapper + rules doc (Update 8). Smoke test full lifecycle: create → list → transition (state machine validated) → DONE → message hand-off.
[NOTE] 2026-05-17 — Tahap G selesai (Update 9): 4 tools/scripts baru (btc_price, news_sentiment, archive_tasks, archive_messages, recap_manager), 14 Tier 3 SOULs (32/32 coverage), Hermes whitelist policy authored. Smoke test: archival idempoten, recap windowing benar, btc_price + news_sentiment fetch dari API live.
[NOTE] 2026-05-17 — Tahap berikutnya (Tahap H): Hermes config apply (Fathur eksekusi di WSL berdasarkan `hermes-whitelist.md`); cron setup untuk archival + recap weekly; migration prep ke Telegram Topics (Option C).
[NOTE] 2026-05-17 — Update 10: NexusAI deepening selesai. Agent depth meningkat dari "generic engineer" ke "senior engineer with agency context". Skills, knowledge, dan tools sekarang map ke aktivitas agency konkret (multi-account, scraping, outreach, OPSEC, multi-tenant SaaS). Two tools declined dengan substitusi penuh. Total: 1 SOUL update, 7 parent skill deepen, 3 deep skill new, 20 knowledge new, 10 tools new, 1 SKILLS.md update, 1 tool-registry update. Next: BrandFlow + Crypto deepening (Update 11 + 12).

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
