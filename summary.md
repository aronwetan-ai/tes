# AI Holding Project Summary

Tanggal: 17 Mei 2026 — Update 5
Owner: Fathur
Environment: WSL2 + Hermes + Telegram Bot + Online Provider API Key
Repository: aronwetan-ai/tes

---

## Update 5 — Tier 3 Agent SOULs + New Specialist Roles (17 Mei 2026)

Branch: `feat/tier3-agent-souls`

### A. Tujuan

Sebelum Update 5:
- Tier 0/1/2 SOUL sudah ada, tapi setiap **agent individu** masih generic (warisan boilerplate).
- `@nexusai.backend` dan `@nexusai.frontend` punya jiwa yang sama persis (cuma role-nya beda).
- Beberapa role kritikal **belum ada** sama sekali: Security di NexusAI (padahal SaaS), Designer di BrandFlow, On-chain Analyst di Crypto.

Update 5 menyelesaikan dua hal sekaligus:
1. **Tier 3 SOUL** untuk 18 agent (6 per perusahaan, role yang paling sering dipanggil).
2. **Tambahan 6 role baru** untuk mengisi gap fungsional yang teridentifikasi dari analisis.

### B. Role Baru yang Ditambahkan

#### NexusAI (+2 role: 8 → 10 agent)
| Role | Slug | Alasan ditambahkan |
|---|---|---|
| Security Engineer | `@nexusai.security` | SaaS tanpa security = breach waiting to happen. Threat modeling, auth, OPSEC tidak fit ke backend atau devops. Juga handle offensive enablement (OPSEC untuk automation/multi-account work Fathur). |
| AI / ML Engineer | `@nexusai.ml` | Fokus perusahaan menyebut "AI agents". Tanpa role ini, agent design jatuh ke backend yang tidak punya konteks ML / prompt engineering / eval. |

#### BrandFlow (+2 role: 9 → 11 agent)
| Role | Slug | Alasan ditambahkan |
|---|---|---|
| Designer | `@brandflow.designer` | Marketing tanpa visual = incomplete. Copywriter handle copy, social handle calendar, tapi tidak ada yang own visual concept / layout / type / color spec. |
| Community Manager | `@brandflow.community` | Social plan kalender; tidak handle real-time DM, comments, mentions, sentiment monitoring, crisis early warning. Skill berbeda. |

#### Crypto Consultant (+2 role: 8 → 10 agent)
| Role | Slug | Alasan ditambahkan |
|---|---|---|
| On-chain Analyst | `@crypto.onchain` | `@crypto.data` generik (struktur data umum). On-chain itu skill spesifik: wallet flows, exchange flows, whale activity, smart money tracking, supply dynamics. |
| Macro Analyst | `@crypto.macro` | Cycle analysis butuh konteks DXY, Fed, M2, yields, equities — tidak fit ke market analyst yang fokus teknikal. Macro liquidity adalah primary cycle driver. |

### C. Tier 3 SOULs yang Dibuat (18 file)

Struktur: `companies/<company>/agents/<agent>.md`

```
NexusAI (6):
  agents/ceo.md, agents/cto.md, agents/backend.md
  agents/devops.md, agents/security.md (NEW), agents/ml.md (NEW)

BrandFlow (6):
  agents/ceo.md, agents/cmo.md, agents/copywriter.md
  agents/social.md, agents/designer.md (NEW), agents/community.md (NEW)

Crypto Consultant (6):
  agents/ceo.md, agents/research.md, agents/market.md
  agents/risk.md, agents/onchain.md (NEW), agents/macro.md (NEW)
```

Role lain (PM, QA, Writer, Frontend, SEO, Analytics, Data, Report) **belum** punya Tier 3 SOUL — mereka tetap inherit dari Tier 2 SOUL perusahaan dan SOP knowledge yang relevan. Ini standar; Tier 3 dibuat ketika role butuh spesifisitas tambahan.

### D. Struktur Konsisten Tiap Tier 3 SOUL

Setiap Tier 3 SOUL punya struktur 8-10 section:

1. Inheritance Note (eksplisit warisi Root SOUL → Company SOUL)
2. Identity (siapa agent ini, siapa BUKAN)
3. Voice (cara bicara, default style)
4. Specific Responsibilities (tugas konkret, bukan generic)
5. Decision Authority (boleh decide vs harus escalate)
6. Default Approach / Process (langkah default per task)
7. Output Format (structured templates per task type)
8. What I Do NOT Do (anti-pattern eksplisit)
9. Cross-Agent Routing (kapan delegate ke agent lain)
10. (Optional) Boundary reminders untuk role rawan (security, community, onchain, risk)

### E. Update File Lain

- **3× AGENTS.md** (per company) — daftar role lengkap, direct routing block dengan role baru, knowledge loading order updated, safety rules.
- **3× COMMANDS.md** (per company) — command baru untuk role baru, knowledge loading rule updated.
- **3× IDENTITY.md** (per company) — refresh active departments list, tambah inheritance note.

### F. Dampak Operasional

Sebelum:
- `@nexusai.backend buatkan API`, `@nexusai.frontend buatkan UI` → kedua agent jawab dengan persona yang sama.
- `@brandflow.copywriter` jawab dengan persona generic, sama dengan `@brandflow.cmo`.
- `@crypto.market` analisis chart pakai bahasa generic, tidak ada cycle awareness.
- Tidak ada agent untuk security review, designer brief, community management, on-chain forensics, atau macro overlay.

Sesudah:
- Setiap agent punya **voice, principles, decision authority, output format** yang khas peran.
- 6 role baru mengisi gap fungsional — tidak lagi ada task yang "jatuh" ke role yang salah.
- Boundary #4 diamplify spesifik di role rawan (community, onchain, risk).

### G. Yang Belum Selesai (untuk PR berikutnya)

1. **Tier 3 untuk role sisanya** — PM, QA, Writer, Frontend, SEO, Analytics, Data, Report. Bisa ditambahkan saat Fathur mulai sering pakai role-role ini dan butuh spesifisitas.
2. **Skill files specialization** — 23 dari 24 SKILL.md masih boilerplate. Sebaiknya hapus skill folder yang tidak relevan per perusahaan (mis. devops di brandflow).
3. **Fix memory reference** + update root MEMORY.md.
4. **Task Logger JSONL** — schema + writer + filter.
5. **Tools tambahan** — btc_price.py, news_sentiment.py.

---

## Update 4 — Tier 2 Company SOULs (17 Mei 2026)

Branch: `feat/tier2-company-souls`

### A. Tujuan

Sebelum Update 4, ketiga `companies/*/SOUL.md` masih copy-paste boilerplate dari template lama — agent NexusAI, BrandFlow, dan Crypto Consultant punya "jiwa" yang identik. Update ini memberi setiap perusahaan **kepribadian, prinsip, dan decision authority** yang spesifik untuk domainnya.

### B. Yang Dieksekusi

3 file SOUL ditulis ulang dari nol dengan struktur Tier-2 yang konsisten:

```
companies/nexusai/SOUL.md
  Nuansa: engineering-precise, pragmatic, zero fluff.
  - 7 engineering principles (working code beats perfect, boring tech, dst).
  - 7-step operating behavior untuk setiap task.
  - Decision authority eksplisit: CEO / CTO / PM / Specialist (boleh decide vs harus escalate).
  - Cross-company collaboration: kapan loop in BrandFlow / Crypto.

companies/brandflow/SOUL.md
  Nuansa: creative-confident, audience-aware, sharp copy, slightly playful.
  - 7 marketing principles (audience first, hook earns the read, dst).
  - 6-step operating behavior dengan emphasis pada KPI.
  - Decision authority + Boundary #4 reminder (BrandFlow paling sering brush dengan rule "tidak bicara atas nama Fathur di publik").
  - Memory discipline: hanya simpan campaign decisions, bukan setiap draft.

companies/crypto-consultant/SOUL.md
  Nuansa: analyst-cautious, data-first, skeptical, bedakan fakta vs opini.
  - 7 research principles (fact > interpretation > scenario, no determinism, source everything).
  - Decision authority + Boundary #4 amplified (financial advice posture).
  - Wajib disclaimer pada @crypto.report output.
  - Time-stamp & source citation non-negotiable.
```

### C. Struktur Konsisten Tiap SOUL

Setiap Tier-2 SOUL punya 14 section dengan urutan sama:

1. Inheritance Note (eksplisit warisi Root SOUL)
2. Identity (siapa perusahaan ini, siapa BUKAN)
3. Culture & Tone (bagaimana suara perusahaan, bagaimana TIDAK)
4. Principles (non-negotiable)
5. Operating Behavior (langkah default per task)
6. Decision Authority (boleh decide vs harus escalate ke Fathur)
7. Boundary Reminder (jika domain rawan)
8. Memory Discipline
9. Tool Discipline
10. Knowledge Loading (mandatory file order)
11. What This Company Is NOT
12. Cross-Company Collaboration
13. Loyalty Reminder (diulang agar tidak drift)

### D. Dampak Operasional

Sebelum:
- @nexusai.ceo dan @brandflow.ceo dan @crypto.ceo menjawab dengan tone yang sama.
- Tidak ada kejelasan kapan CEO boleh decide sendiri vs harus tanya Fathur.
- Tidak ada kejelasan boundary spesifik per domain (mis. financial advice di Crypto).

Sesudah:
- Setiap perusahaan punya tone, principles, dan rules sendiri yang spesifik.
- Decision authority terstruktur: CEO / VP / PM / Specialist masing-masing tahu otoritas dan escalation path.
- Boundary #4 dari Root SOUL diamplify khusus di BrandFlow & Crypto (domain paling rawan).
- Cross-company collaboration jelas: NexusAI tidak bikin copy, BrandFlow tidak invent fakta crypto, dst.

### E. Yang Belum Selesai (untuk PR berikutnya)

1. **Tier 3 Agent SOULs** — minimal untuk role utama (CEO, CTO/CMO/Research, dan 1 spesialis per company).
2. **Specialize skill files** — 23 dari 24 SKILL.md masih boilerplate.
3. **Fix memory reference inkonsistensi** + update root MEMORY.md.
4. **Task Logger JSONL** — schema + writer + filter.
5. **Tools tambahan** — btc_price.py, news_sentiment.py.

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
Tier 0: SOUL.md                                    ← konstitusi global (semua entitas)
        ↓
Tier 1: MAIN_SOUL.md                               ← Main Assistant personality
        ↓
Tier 2: companies/<co>/SOUL.md                     ← per perusahaan (3 perusahaan, post Update 4)
        ↓
Tier 3: companies/<co>/agents/<role>.md            ← per agent (18 file, post Update 5)
```

---

## 3. Perusahaan yang Sudah Dibuat

### 3.1 NexusAI

Path: `/home/fatur/ai-holding/companies/nexusai`
Tipe: IT Software Company
Fokus: cloud, DevOps, AI agents, SaaS

Agent aktif (10 role, post Update 5):
- CEO, CTO, Project Manager, Backend, Frontend, DevOps, **Security (NEW)**, **ML (NEW)**, QA, Technical Writer

Tier 3 SOULs ada untuk: ceo, cto, backend, devops, security, ml.

Routing contoh:
```
@nexusai.ceo buatkan strategi produk
@nexusai.cto buatkan arsitektur teknis
@nexusai.backend buatkan desain API
@nexusai.security review auth flow                (NEW)
@nexusai.ml design prompt untuk agent             (NEW)
```

Knowledge domain: `knowledge/software/software-development-sop.md` (Update 3)

### 3.2 BrandFlow

Path: `/home/fatur/ai-holding/companies/brandflow`
Tipe: Marketing and Content Company
Fokus: branding, content, social media, campaign strategy

Agent aktif (11 role, post Update 5):
- CEO, CMO, Project Manager, Copywriter, Social, **Community (NEW)**, **Designer (NEW)**, SEO, Analytics, QA, Writer

Tier 3 SOULs ada untuk: ceo, cmo, copywriter, social, community, designer.

Routing contoh:
```
@brandflow.cmo buatkan strategi campaign
@brandflow.copywriter buatkan caption
@brandflow.designer buatkan visual concept       (NEW)
@brandflow.community draft reply DM ini          (NEW)
```

Knowledge domain: `knowledge/marketing/marketing-sop.md` (Update 3)

### 3.3 Crypto Consultant

Path: `/home/fatur/ai-holding/companies/crypto-consultant`
Tipe: Crypto Research Company
Fokus: market research, cycle analysis, risk management, reporting

Agent aktif (11 role, post Update 5):
- CEO, Research Lead, Project Manager, Market, Risk, **On-chain (NEW)**, **Macro (NEW)**, Data, QA, Report, Writer

Tier 3 SOULs ada untuk: ceo, research, market, risk, onchain, macro.

Routing contoh:
```
@crypto.research cek Fear & Greed Index hari ini
@crypto.market analisis trend BTC weekly
@crypto.onchain trace exchange flows BTC          (NEW)
@crypto.macro overlay DXY + Fed posture           (NEW)
@crypto.risk buatkan risk assessment
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

### 4.10 Tier 2 Company SOULs (post Update 4)
Setiap perusahaan punya SOUL.md spesifik dengan:
- Identity, culture & tone unik per domain.
- Principles non-negotiable per perusahaan.
- Decision authority eksplisit (CEO/VP/PM/Specialist).
- Boundary reminder spesifik domain (terutama BrandFlow & Crypto).

### 4.11 Tier 3 Agent SOULs + 6 Role Baru (post Update 5)
- 18 Tier 3 SOULs (6 per perusahaan, role utama).
- 6 role baru ditambahkan: `@nexusai.security`, `@nexusai.ml`, `@brandflow.designer`, `@brandflow.community`, `@crypto.onchain`, `@crypto.macro`.
- Setiap Tier 3 SOUL punya voice, principles, decision authority, output format yang spesifik per role.
- AGENTS.md, COMMANDS.md, IDENTITY.md per company di-update untuk reflect role baru.

### 4.12 Test Integrasi Berhasil
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

### Prioritas 1 — Tier 3 untuk Role Sisanya
Saat ini 18 dari ~30 agent punya Tier 3 SOUL. Yang belum:
- NexusAI: pm, frontend, qa, writer
- BrandFlow: pm, seo, analytics, qa, writer
- Crypto: pm, data, qa, report, writer

Tambah Tier 3 untuk role yang sering dipanggil oleh Fathur, on-demand.

### Prioritas 2 — Specialize Skill Files + Cleanup
- Hapus skill folder yang tidak relevan per perusahaan (mis. `devops/` di brandflow, `coding/` di crypto).
- Perdalam skill yang relevan dengan referensi ke Tier 3 SOUL.

### Prioritas 3 — Fix Memory Reference + Update Root MEMORY.md
`MAIN.md` baca `MEMORY.md` (root), `AGENTS.md` baca `memory/global.md`.
Klarifikasi peran masing-masing dan update `MEMORY.md` root agar sinkron
dengan keputusan terbaru (SOUL hierarchy + knowledge management + Tier 2/3 SOULs + role baru).

### Prioritas 4 — Task Logger JSONL
Schema + writer + filter untuk `companies/*/tasks/inbox.jsonl`.

### Prioritas 5 — Tools Tambahan
- `btc_price.py` (PLANNED di registry).
- `news_sentiment.py` (PLANNED di registry).

### Prioritas 6 — Hermes Service Hardening
Cek `hermes-gateway.service` warning bersih, no double process, restart membaca config.

---

## 8. Roadmap Pendek

### Tahap A — Stabilkan Main Assistant ✓
Done — natural command, routing, pseudo-mention konsisten.

### Tahap B — Bangun Knowledge Management ✓ (selesai Update 3)
Done — folder lengkap, SOP per domain, tool registry, memory rules.

### Tahap C — Buat Tier 2/3 SOULs
Tier 2 ✓ (Update 4). Tier 3 — 18 dari ~30 agent done (Update 5). Sisanya on-demand.

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
- SOUL Tier 2 (semua 3 perusahaan, post Update 4)
- SOUL Tier 3 (18 agent untuk role utama, post Update 5)
- 6 role baru: security, ml, designer, community, onchain, macro
- Knowledge management lengkap (8 file aktif)
- Template Tier-2 ready
- Repo bersih (no .bak, no Zone.Identifier)
```

Yang belum:
```
- Tier 3 untuk role sisa (PM, QA, Writer, Frontend, SEO, Analytics, Data, Report)
- Skill files spesifik (saat ini boilerplate)
- Task logger JSONL writer
- Root MEMORY.md update agar sinkron dengan keputusan terbaru
- btc_price.py
- news_sentiment.py
- Whitelist tool read-only
```

---

## 10. Next Immediate Action

Setelah Update 5 (Tier 3 + 6 role baru) selesai, langkah berikutnya:

```
1. Specialize skill files — buang folder skill yang tidak relevan per perusahaan,
   perdalam yang relevan, link ke Tier 3 SOULs.
2. Fix memory reference + update root MEMORY.md agar sinkron.
3. Task logger JSONL implementation.
4. Tools tambahan: btc_price.py, news_sentiment.py.
5. Tier 3 untuk role sisa (on-demand saat Fathur sering pakai).
```

---

## 11. Prompt untuk Melanjutkan Setup

Gunakan prompt ini ke Hermes / Kiro jika ingin melanjutkan:

```text
Baca summary.md (Update 5 section terbaru) lalu lanjutkan dari "Next Immediate Action".
Mulai dari specialize skill files atau fix memory reference.
Pelan-pelan, satu tahap per response, tunggu konfirmasi sebelum lanjut.
```

---

## 12. Catatan Branch & Commit

| Branch                                          | Status   | Isi |
|-------------------------------------------------|----------|-----|
| `main`                                          | base     | Update 3 + 4 sudah merged |
| `chore/quickwins-cleanup-and-knowledge-fix`     | merged   | Update 3 — cleanup + knowledge + template (PR #1) |
| `feat/tier2-company-souls`                      | merged   | Update 4 — Tier 2 SOULs untuk 3 perusahaan (PR #2) |
| `feat/tier3-agent-souls`                        | active   | Update 5 — Tier 3 SOULs (18) + 6 role baru |

Setelah branch ini di-merge, lanjut ke specialize skills atau task logger.
