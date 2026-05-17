# AI Holding Project Summary

Tanggal: 17 Mei 2026 — Update 3
Owner: Fathur
Environment: WSL2 + Hermes + Telegram Bot + Online Provider API Key
Repository: aronwetan-ai/tes

---

## Update 3 — Audit Repository & Quick Wins (17 Mei 2026)

Section ini ditambahkan setelah audit menyeluruh terhadap repository dan eksekusi
"Quick Wins" pada branch `chore/quickwins-cleanup-and-knowledge-fix`.

### A. Hasil Audit Repository

Audit menyoroti tujuh area dengan status berbeda:

| Area                       | Status sebelum audit | Catatan |
|----------------------------|----------------------|---------|
| Top-level governance       | 95% baik             | SOUL.md, MAIN_SOUL.md, MAIN.md sudah Tier 0/1 yang benar |
| Knowledge (root)           | 60% baik             | Hanya 3 dari 7 folder yang dirujuk benar-benar ada |
| SOUL hierarchy             | 50% baik             | Tier 0/1 selesai; Tier 2/3 masih boilerplate generik |
| Companies (struktur)       | 90% baik             | Struktur folder lengkap |
| Companies (depth)          | 30% baik             | Isi 80% generik copy-paste dari template |
| Templates                  | 40% baik             | Belum reflect Tier-2 design + tidak ada Direct Routing |
| Skills                     | 20% baik             | 23 dari 24 SKILL.md identik (boilerplate) |
| Tools                      | 25% baik             | 1 active dari 4 entry registry |
| Task logger                | 5% baik              | Semua JSONL kosong, tidak ada writer |
| Kebersihan repo            | 70% baik             | 13 file sampah (.bak + Zone.Identifier + duplikat) |

### B. Gap Kritis yang Ditemukan

1. **Broken knowledge references.** `MAIN.md`, `AGENTS.md`, `companies/nexusai/COMMANDS.md`,
   dan `companies/brandflow/COMMANDS.md` menunjuk ke folder/file yang belum dibuat:
   - `knowledge/core/`
   - `knowledge/software/software-development-sop.md`
   - `knowledge/marketing/marketing-sop.md`
   - `knowledge/sop/`
2. **Template tidak reflect desain terbaru.** Generator perusahaan akan menghasilkan
   company tanpa Direct Agent Routing, tanpa Knowledge Loading rules, dan tanpa
   inheritance dari Root SOUL.
3. **File sampah Windows + backup.** 9 file `.bak/.bak2/.bak3`, 2 Zone.Identifier
   stream, dan 1 duplikat `summary.txt`.
4. **Skill files generik.** 23 dari 24 file SKILL.md identik dengan template — agent
   tidak benar-benar mendapat skill yang spesifik untuk perannya.
5. **Tier 2 dan Tier 3 SOUL belum ada.** Ketiga `companies/*/SOUL.md` masih copy-paste
   generik, tidak menyebut inheritance dari Root SOUL.

### C. Quick Wins yang Sudah Dieksekusi

Branch: `chore/quickwins-cleanup-and-knowledge-fix`

#### C.1 Cleanup (13 file dihapus)

```
SOUL.md.bak
COMMANDS.md.bak
summary.txt
summary.md:Zone.Identifier
summary - Copy.md:Zone.Identifier
companies/brandflow/AGENTS.md.bak
companies/nexusai/AGENTS.md.bak
companies/crypto-consultant/AGENTS.md.bak
companies/crypto-consultant/AGENTS.md.bak2
companies/crypto-consultant/AGENTS.md.bak3
companies/crypto-consultant/MEMORY.md.bak
companies/crypto-consultant/TOOLS.md.bak
companies/crypto-consultant/skills/research/SKILL.md.bak
```

#### C.2 Knowledge Files Baru (4 file)

```
knowledge/core/principles.md
  → Cara berpikir umum + hierarchy SOUL/knowledge.
  → Wajib dibaca oleh semua agent saat sesi baru.

knowledge/software/software-development-sop.md
  → SOP untuk @nexusai.* — API design, code review, deployment,
    output formats, internal routing.

knowledge/marketing/marketing-sop.md
  → SOP untuk @brandflow.* — copywriting framework (AIDA/PAS/BAB),
    hook patterns, per-channel standards, KPI tables.

knowledge/sop/README.md
  → Skill library reusable lintas perusahaan, planned skill list.
```

Setelah perubahan ini, semua referensi dari `MAIN.md`, `AGENTS.md`, dan
`companies/*/COMMANDS.md` mengarah ke file yang **ada**.

#### C.3 Template Update (3 file)

```
templates/company/AGENTS.md (rewritten)
  → Tambah Core Roles dengan deskripsi lebih jelas.
  → Tambah Direct Agent Routing block dengan format @{{COMPANY_SLUG}}.<agent>.
  → Tambah Knowledge Loading block (7 file mandatory).
  → Tambah Memory Rules + Safety Rules.
  → Tambah catatan untuk operator setelah create-company.

templates/company/COMMANDS.md (rewritten)
  → Replace /slash commands dengan @company keyword namespacing.
  → Tambah Knowledge Loading Rules block.
  → Tambah Direct Agent Routing block.
  → Tambah Domain Commands placeholder yang tinggal di-customize.

templates/company/SOUL.md (rewritten - Tier 2 design)
  → Header eksplisit: "Inherits Root SOUL".
  → Identity tied to {{COMPANY_NAME}} + {{COMPANY_TYPE}} + {{COMPANY_FOCUS}}.
  → Section Culture & Tone (default + customization guidance).
  → Operating Behavior 6-step flow.
  → Decision Authority — CEO bisa decide vs must escalate ke Fathur.
  → Memory & Tool discipline pointing to root knowledge files.
  → Loyalty Reminder repeated supaya tidak terlupa.
```

#### C.4 Generator Script Update

```
bin/create-company.sh
  → Tambah substitusi {{COMPANY_SLUG}} → $SLUG.
  → Sebelumnya hanya substitusi {{COMPANY_NAME}} / {{COMPANY_TYPE}} / {{COMPANY_FOCUS}}.
```

### D. Yang Belum Selesai (untuk sesi berikutnya)

Quick Wins selesai. Yang berikutnya berdasarkan urutan dampak:

1. **Tier 2 — Company SOULs** untuk NexusAI, BrandFlow, Crypto Consultant.
   Saat ini ketiga `companies/*/SOUL.md` masih copy-paste generik.
2. **Tier 3 — Agent SOULs** minimal untuk role yang paling sering dipanggil
   (CEO, CTO/CMO/Research, dan 1 specialist per company).
3. **Specialize skill files** — buang yang tidak relevan, perdalam yang relevan.
4. **Fix inkonsistensi memory reference** — `MAIN.md` baca `MEMORY.md`,
   `AGENTS.md` baca `memory/global.md`. Perlu klarifikasi peran.
5. **Update `MEMORY.md` (root)** — belum reflect keputusan SOUL hierarchy
   dan knowledge management terbaru (hanya `memory/global.md` yang di-update).
6. **Task Logger JSONL** — schema + writer + filter.
7. **Tools tambahan** — `btc_price.py`, `news_sentiment.py` (sudah PLANNED di registry).

---

## 1. Tujuan Project

Project ini bertujuan membangun sistem **AI Holding Company** berbasis Hermes, di mana satu Main Assistant dapat mengatur beberapa perusahaan AI agent yang memiliki peran, memory, skill, tool, dan workflow masing-masing.

Target akhirnya:

- Satu bot Telegram sebagai pintu masuk utama.
- Main Assistant sebagai personal assistant dan router.
- Beberapa perusahaan AI agent dengan fokus berbeda.
- Setiap perusahaan memiliki agent/departemen sendiri.
- Task bisa dikirim ke perusahaan atau agent spesifik.
- Memory dan knowledge management tersusun rapi.
- Setup saat ini siap dimigrasikan ke opsi Telegram Topic di masa depan.

---

## 2. Arsitektur Saat Ini

Mode saat ini:

```text
Option A Portable
1 Telegram Bot
↓
Hermes Main Assistant
↓
AI Holding Workspace
↓
Companies / Agents / Tools / Knowledge
```

Workspace utama:

```text
/home/fatur/ai-holding
```

Struktur utama (post Update 3):

```text
ai-holding/
├── SOUL.md           ← Tier 0 (Root constitution)
├── MAIN_SOUL.md      ← Tier 1 (Main Assistant personality)
├── MAIN.md           ← Loader (urutan baca file)
├── AGENTS.md         ← Routing rules
├── COMMANDS.md       ← Command surface
├── MEMORY.md         ← Durable memory root
├── HEARTBEAT.md      ← Self-check loop
├── knowledge/
│   ├── core/         ← principles.md
│   ├── agent-design/ ← memory-rules.md, tool-use-rules.md
│   ├── tools/        ← tool-registry.md
│   ├── software/     ← software-development-sop.md (NexusAI)
│   ├── marketing/    ← marketing-sop.md (BrandFlow)
│   ├── crypto/       ← crypto-research-framework.md
│   ├── sop/          ← skill library reusable
│   └── karpathy.md
├── templates/
│   └── company/      ← updated to Tier-2 design
├── companies/
│   ├── nexusai/
│   ├── brandflow/
│   └── crypto-consultant/
├── tasks/
├── memory/
├── tools/
└── bin/
```

### Hierarki SOUL (Inheritance)

```
Tier 0: SOUL.md                  ← konstitusi global (semua entitas)
        ↓
Tier 1: MAIN_SOUL.md             ← Main Assistant personality
        ↓
Tier 2: companies/<co>/SOUL.md   ← per perusahaan (BELUM diisi spesifik)
        ↓
Tier 3: agents/<role>/SOUL.md    ← per agent (BELUM ada)
```

---

## 3. Perusahaan yang Sudah Dibuat

### 3.1 NexusAI

Path: `/home/fatur/ai-holding/companies/nexusai`
Tipe: IT Software Company
Fokus: cloud, DevOps, AI agents, SaaS

Agent aktif:
- CEO, CTO, Project Manager, Backend Engineer, Frontend Engineer,
  DevOps Engineer, QA Engineer, Technical Writer

Routing contoh:
```
@nexusai.ceo buatkan strategi produk
@nexusai.cto buatkan arsitektur teknis
@nexusai.backend buatkan desain API
@nexusai.devops buatkan deployment plan
```

Knowledge domain: `knowledge/software/software-development-sop.md` (Update 3)

### 3.2 BrandFlow

Path: `/home/fatur/ai-holding/companies/brandflow`
Tipe: Marketing and Content Company
Fokus: branding, content, social media, campaign strategy

Agent aktif:
- CEO, CMO, Project Manager, Copywriter, Social Media,
  SEO, Analytics, QA, Writer

Routing contoh:
```
@brandflow.cmo buatkan strategi campaign
@brandflow.copywriter buatkan caption
@brandflow.social buatkan kalender konten
@brandflow.analytics buatkan KPI campaign
```

Knowledge domain: `knowledge/marketing/marketing-sop.md` (Update 3)

### 3.3 Crypto Consultant

Path: `/home/fatur/ai-holding/companies/crypto-consultant`
Tipe: Crypto Research Company
Fokus: market research, cycle analysis, risk management, reporting

Agent aktif:
- CEO, Research Lead, Project Manager, Market Analyst, Risk Analyst,
  Data Analyst, QA, Writer

Routing contoh:
```
@crypto.research cek Fear & Greed Index hari ini
@crypto.market analisis trend BTC
@crypto.risk buatkan risk assessment
@crypto.report buatkan laporan market
```

Knowledge domain: `knowledge/crypto/crypto-research-framework.md`

---

## 4. Fitur yang Sudah Berhasil

### 4.1 Telegram Bot Berjalan
Hermes sudah berjalan via Telegram. Bot dapat menerima dan membalas instruksi user.

### 4.2 Main Assistant Berjalan
Membaca konteks AI Holding, memahami perusahaan milik Fathur, routing, baca file
di workspace.

### 4.3 Routing Perusahaan & Direct Agent Routing
Format `@company` dan `@company.agent` keduanya berjalan.

### 4.4 Company Generator
`bin/create-company.sh` — sekarang juga mensubstitusi `{{COMPANY_SLUG}}` (Update 3).

### 4.5 Tool Crypto Fear & Greed
`tools/fear_greed.py` — production-grade dengan error handling.

### 4.6 SOUL Hierarchy Tier 0 + Tier 1
- `SOUL.md` (Root) — loyalty + execute stance + 4 boundaries.
- `MAIN_SOUL.md` — personality Main Assistant + routing rules + decision authority.

### 4.7 Knowledge Management (post Update 3)
8 file knowledge aktif:
```
knowledge/core/principles.md                     (NEW)
knowledge/agent-design/memory-rules.md
knowledge/agent-design/tool-use-rules.md
knowledge/tools/tool-registry.md
knowledge/software/software-development-sop.md   (NEW)
knowledge/marketing/marketing-sop.md             (NEW)
knowledge/crypto/crypto-research-framework.md
knowledge/sop/README.md                          (NEW)
knowledge/karpathy.md
```

### 4.8 Format Output Standar
- @crypto.research mengikuti format 6 lapisan (FACT, SOURCE, TREND, INTERPRET, SCENARIO, RISK NOTE).
- Disclaimer crypto otomatis di setiap output laporan.

### 4.9 Template Perusahaan (post Update 3)
Template di `templates/company/` sudah:
- AGENTS.md punya Direct Agent Routing block.
- COMMANDS.md pakai `@company keyword` namespacing.
- SOUL.md pakai Tier-2 inheritance design.

### 4.10 Test Integrasi Berhasil
- @crypto.research jalankan fear_greed.py + output 6 lapisan.
- @nexusai.backend buat desain API terstruktur.
- @brandflow.copywriter buat caption Instagram dengan 2 variasi tone.

---

## 5. Masalah yang Sudah Diselesaikan

### 5.1 Slash Command Tidak Cocok → Pseudo-Mention
Format `/nexusai` dianggap native command oleh Hermes/Telegram.
Solusi: pakai `@nexusai`, `@brandflow`, `@crypto`.

### 5.2 Natural Command Diperkuat
Rule:
- "perusahaan" tanpa konteks → AI Holding milik Fathur.
- "perusahaan nyata / publik / di dunia" → real-world company.

### 5.3 Knowledge Management → Sudah Lengkap (Update 3)
Sebelumnya broken references. Sekarang semua knowledge yang dirujuk ada.

### 5.4 Tool Execution Approval
Hermes meminta approval saat menjalankan script lokal — aman untuk sekarang.
Whitelist read-only untuk masa depan.

---

## 6. Prinsip Project

Prinsip utama:
```text
Prompt is program.
Context is source code.
Memory is persistent state.
Skill is reusable module.
Tool is external capability.
Human remains supervisor.
```

Knowledge:
- `knowledge/karpathy.md` — Karpathy-inspired principles.
- `knowledge/core/principles.md` — operational version untuk semua agent (Update 3).

---

## 7. Yang Perlu Dilakukan Dalam Waktu Dekat (Updated)

### Prioritas 1 — Tier 2 Company SOULs
Tulis SOUL khas untuk NexusAI, BrandFlow, Crypto Consultant.
Inheritance + budaya unik per perusahaan.

### Prioritas 2 — Tier 3 Agent SOULs
Minimal untuk: @nexusai.ceo, @nexusai.cto, @brandflow.cmo, @brandflow.copywriter,
@crypto.research, @crypto.risk.

### Prioritas 3 — Specialize Skill Files
Saat ini 23 dari 24 SKILL.md generik. Buang yang tidak relevan, perdalam yang relevan.

### Prioritas 4 — Fix Memory Reference
`MAIN.md` baca `MEMORY.md` (root), `AGENTS.md` baca `memory/global.md`.
Perlu klarifikasi peran masing-masing dan update `MEMORY.md` root agar sinkron
dengan keputusan terbaru.

### Prioritas 5 — Task Logger JSONL
Schema + writer + filter untuk `companies/*/tasks/inbox.jsonl`.

### Prioritas 6 — Tools Tambahan
- `btc_price.py` (PLANNED di registry).
- `news_sentiment.py` (PLANNED di registry).

### Prioritas 7 — Hermes Service Hardening
Cek `hermes-gateway.service` warning bersih, no double process, restart membaca config.

---

## 8. Roadmap Pendek

### Tahap A — Stabilkan Main Assistant ✓
Done — natural command, routing, pseudo-mention konsisten.

### Tahap B — Bangun Knowledge Management ✓ (selesai Update 3)
Done — folder lengkap, SOP per domain, tool registry, memory rules.

### Tahap C — Buat Tier 2/3 SOULs (NEXT)
Belum — masih boilerplate generik.

### Tahap D — Specialize Skills
Belum — masih boilerplate.

### Tahap E — Task Logger
Belum.

### Tahap F — Tools Tambahan
1 dari 4 active. 3 PLANNED.

### Tahap G — Migrasi Option C (Telegram Topic)
Nanti setelah B–F stabil.

---

## 9. Status Terakhir

Status project: **Usable Prototype with Knowledge Layer**

Yang sudah siap:
```
- Hermes Telegram bot
- Main Assistant
- AI Holding workspace
- Company generator (sudah handle SLUG substitution)
- 3 perusahaan awal
- Direct agent routing
- Crypto Fear & Greed tool
- SOUL Tier 0 + Tier 1
- Knowledge management lengkap (8 file aktif)
- Template Tier-2 ready
- Repo bersih (no .bak, no Zone.Identifier)
```

Yang belum:
```
- Tier 2 Company SOULs (per perusahaan)
- Tier 3 Agent SOULs
- Skill files spesifik (saat ini boilerplate)
- Task logger JSONL writer
- btc_price.py
- news_sentiment.py
- Whitelist tool read-only
```

---

## 10. Next Immediate Action

Setelah Update 3 (Quick Wins) selesai, langkah berikutnya:

```
1. Tier 2 Company SOULs — NexusAI, BrandFlow, Crypto Consultant.
2. Tier 3 Agent SOULs — minimal untuk role utama tiap perusahaan.
3. Specialize skill files per perusahaan.
4. Fix memory reference inkonsistensi.
5. Task logger JSONL implementation.
```

---

## 11. Prompt untuk Melanjutkan Setup

Gunakan prompt ini ke Hermes / Kiro jika ingin melanjutkan:

```text
Baca summary.md (Update 3 section) lalu lanjutkan dari "Next Immediate Action".
Mulai dari Tier 2 Company SOULs satu per satu.
Pelan-pelan, satu tahap per response, tunggu konfirmasi sebelum lanjut.
```

---

## 12. Catatan Branch & Commit

| Branch                                          | Status   | Isi |
|-------------------------------------------------|----------|-----|
| `main`                                          | base     | Semua progress sebelum Update 3 |
| `chore/quickwins-cleanup-and-knowledge-fix`     | active   | Update 3 — cleanup + knowledge + template |

Setelah branch ini di-merge, lanjut ke branch berikutnya untuk Tier 2/3 SOULs.
