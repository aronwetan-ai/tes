# Global Memory — AI Holding

Versi: 1.0  
Update terakhir: 2026-05-17  
Dikelola oleh: Main Assistant  

---

## Profil Owner
Nama    : Fathur
System  : WSL2 + Hermes + Telegram Bot
Workspace: /home/fatur/ai-holding

---

## Arsitektur Aktif
1 Telegram Bot
↓
Hermes Main Assistant
↓
AI Holding Workspace
↓
Companies / Agents / Tools / Knowledge

---

## Perusahaan Aktif
@nexusai      → IT Software Company (cloud, DevOps, AI agents, SaaS)
@brandflow    → Marketing & Content Company (branding, content, social media)
@crypto       → Crypto Research Company (market research, risk, reporting)

---

## Keputusan yang Sudah Final
[DECISION] 2026-05-17 — Routing pakai pseudo-mention (@company) bukan slash command (/company)
[DECISION] 2026-05-17 — "perusahaan" tanpa konteks = perusahaan AI Holding milik Fathur
[DECISION] 2026-05-17 — Knowledge management dibangun manual, bukan di-generate Hermes semua
[DECISION] 2026-05-17 — Tool Risk Low tidak perlu approval, Risk Medium perlu konfirmasi

---

## Perubahan Arsitektur
[ARCH] 2026-05-17 — Folder knowledge/ dibuat dengan 7 subfolder
[ARCH] 2026-05-17 — tool-registry.md dibuat di knowledge/tools/
[ARCH] 2026-05-17 — tool-use-rules.md dibuat di knowledge/agent-design/
[ARCH] 2026-05-17 — memory-rules.md dibuat di knowledge/agent-design/
[ARCH] 2026-05-17 — crypto-research-framework.md dibuat di knowledge/crypto/

---

## Tool Aktif
[TOOL] fear_greed.py — Active — /home/fatur/ai-holding/tools/fear_greed.py
[TOOL] create-company.sh — Active — /home/fatur/ai-holding/bin/create-company.sh
[TOOL] btc_price.py — PLANNED — belum dibuat
[TOOL] news_sentiment.py — PLANNED — belum dibuat

---

## Task Aktif
[TASK] Belum ada task aktif saat ini.

---

## Catatan Tambahan
[NOTE] 2026-05-17 — Setup knowledge management selesai tahap pertama.
[NOTE] 2026-05-17 — Tahap berikutnya: SOP software + SOP marketing via Hermes.
